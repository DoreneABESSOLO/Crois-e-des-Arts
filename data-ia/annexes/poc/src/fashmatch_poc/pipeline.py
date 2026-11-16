"""Pipeline ETL conforme FashMatch V2 (POC).

Étapes :
  1. Extraction    catalogue (Kaggle ou substitution) + profils synthétiques
  2. Nettoyage     normalisation, dédoublonnage, correction des incohérences
  3. Pseudonymisation  identifiants directs -> jetons HMAC, coffre séparé
  4. Contrôle d'âge    < 15 ans exclus ; éligibilité Pay3x à 18 ans
  5. Purge             comptes inactifs au-delà de la durée de conservation
  6. Minimisation      liste blanche par finalité
  7. Consentements     séparation personnalisation / entraînement
  8. Chargement        base SQLite (zone analytique) + exports CSV
  9. Rapport qualité   Markdown + JSON, versionnés

Usage : python -m fashmatch_poc.pipeline --config config/pipeline.yaml
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import uuid
from datetime import date
from pathlib import Path

import pandas as pd
import yaml

from . import privacy, quality
from .audit import AuditLog, verify_chain
from .generate import generate_profiles, load_catalogue

# Maillots, lingerie, nuit : essayage sur un avatar uniquement, jamais sur la photo de la personne (EF-07, EX-24)
AVATAR_ONLY_IN_CABINE = {"Swimwear", "Bra", "Briefs", "Lingerie Set", "Innerwear Vests",
                        "Camisoles", "Boxers", "Trunk", "Night suits", "Nightdress"}


def run(cfg_path: Path, root: Path) -> dict:
    cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
    ref = date.fromisoformat(cfg["reference_date"])
    out_dir = root / "output"
    out_dir.mkdir(exist_ok=True)
    run_id = uuid.uuid4().hex[:12]
    audit = AuditLog(root / cfg["audit_log"], run_id)
    m: dict = {"run_id": run_id, "reference_date": str(ref)}

    # 1. Extraction ---------------------------------------------------------
    profiles = generate_profiles(cfg["n_profiles"], cfg["seed"], ref)
    catalogue, cat_source = load_catalogue(root / "data" / "raw", cfg["seed"])
    m["source_catalogue"] = cat_source
    m["brut"] = {
        "profils": len(profiles),
        "catalogue": len(catalogue),
        "completude_profils": quality.completeness(profiles),
        "doublons_profils_email_normalise": int(privacy.normalise_email(profiles["email"]).duplicated().sum()),
        "incoherences_profils": quality.profile_consistency(profiles, ref),
        "doublons_catalogue": quality.duplicates(catalogue, "id"),
        "completude_catalogue": quality.completeness(catalogue),
    }
    audit.log("extract", "POC – démonstration", "aucune donnée réelle (synthétique)",
              profils=len(profiles), catalogue=len(catalogue), source=cat_source)

    # 2. Nettoyage ----------------------------------------------------------
    profiles["email"] = privacy.normalise_email(profiles["email"])
    profiles = profiles.drop_duplicates(subset="email", keep="first")
    profiles["country"] = profiles["country"].replace({"France": "FR"})
    incoherent = (ref.year - profiles["birth_year"] - profiles["declared_age"]).abs() > 1
    # Règle : en cas d'incohérence, on ne devine pas -> le profil est mis en quarantaine
    quarantine = profiles[incoherent]
    profiles = profiles[~incoherent]
    catalogue = catalogue.drop_duplicates(subset="id")
    catalogue["cabine_sur_avatar"] = catalogue["articleType"].isin(AVATAR_ONLY_IN_CABINE)
    audit.log("clean", "qualité des données", "RGPD art. 5.1.d (exactitude)",
              doublons_supprimes=m["brut"]["doublons_profils_email_normalise"],
              quarantaine=int(len(quarantine)))

    # 3. Pseudonymisation ---------------------------------------------------
    key = privacy.get_key(cfg["pseudonymisation"]["key_env_var"])
    profiles = privacy.pseudonymise(profiles, key, root / cfg["pseudonymisation"]["vault_path"],
                                    cfg["direct_identifiers"])
    audit.log("pseudonymise", "sécurité", "RGPD art. 32, art. 25",
              algorithme="HMAC-SHA256", coffre=cfg["pseudonymisation"]["vault_path"])

    # 4. Contrôle d'âge -----------------------------------------------------
    profiles, n_minors = privacy.age_gate(profiles, ref, cfg["age"]["min_inscription"], cfg["age"]["min_pay3x"])
    audit.log("age_gate", "protection des mineurs", "RGPD art. 8 ; loi I&L art. 45",
              exclus_moins_15=n_minors, pay3x_non_eligibles_age=int((~profiles["pay3x_age_ok"]).sum()))

    # 5. Purge --------------------------------------------------------------
    profiles, n_purged = privacy.purge(profiles, ref, cfg["retention"]["compte_inactif_jours"])
    audit.log("purge", "limitation de la conservation", "RGPD art. 5.1.e",
              purges=n_purged, duree_jours=cfg["retention"]["compte_inactif_jours"])

    # 6. Minimisation -------------------------------------------------------
    before_cols = list(profiles.columns)
    match_df, dropped = privacy.minimise(profiles, cfg["allowlist"]["match_recommandation"])
    pay_df, _ = privacy.minimise(profiles, cfg["allowlist"]["pay3x_eligibilite"] + ["pay3x_age_ok"])
    audit.log("minimise", "recommandation (Match)", "RGPD art. 5.1.c, art. 25",
              champs_avant=len(before_cols), champs_apres=match_df.shape[1], champs_supprimes=dropped)

    # 7. Consentements ------------------------------------------------------
    split = privacy.consent_split(match_df)
    audit.log("consent_split", "personnalisation / entraînement", "RGPD art. 6.1.a, art. 7",
              personnalisation=len(split["personnalisation"]), entrainement=len(split["entrainement"]))

    # 8. Chargement ---------------------------------------------------------
    db = out_dir / "fashmatch_v2.sqlite"
    db.unlink(missing_ok=True)
    with sqlite3.connect(db) as con:
        split["personnalisation"].to_sql("profils_personnalisation", con, index=False)
        split["entrainement"].to_sql("profils_entrainement", con, index=False)
        pay_df.to_sql("profils_pay3x", con, index=False)
        catalogue.to_sql("catalogue", con, index=False)
    audit.log("load", "chargement zone analytique", "RGPD art. 32",
              base=str(db.name), tables=4)

    # 9. Qualité après traitement ------------------------------------------
    m["apres"] = {
        "profils_personnalisation": len(split["personnalisation"]),
        "profils_entrainement": len(split["entrainement"]),
        "quarantaine": int(len(quarantine)),
        "exclus_moins_15": n_minors,
        "purges_inactifs": n_purged,
        "champs_supprimes": dropped,
        "completude_profils": quality.completeness(match_df),
        "doublons_user_id": quality.duplicates(match_df, "user_id"),
        "incoherences_profils": quality.profile_consistency(match_df.assign(declared_age=ref.year - match_df["birth_year"]), ref),
        "catalogue": len(catalogue),
        "catalogue_cabine_sur_avatar": int(catalogue["cabine_sur_avatar"].sum()),
    }
    m["biais"] = {
        "profils_gender_pref": quality.distribution(match_df, "gender_pref"),
        "profils_tranches_age": quality.age_bands(match_df, ref),
        "catalogue_gender": quality.distribution(catalogue, "gender"),
        "catalogue_masterCategory": quality.distribution(catalogue, "masterCategory"),
        "entrainement_vs_base_gender_pref": {
            "base": quality.distribution(match_df, "gender_pref"),
            "entrainement": quality.distribution(split["entrainement"], "gender_pref"),
        },
    }
    m["biais"]["ratio_desequilibre_gender_pref"] = quality.imbalance_ratio(m["biais"]["profils_gender_pref"])
    m["biais"]["ratio_desequilibre_catalogue_gender"] = quality.imbalance_ratio(m["biais"]["catalogue_gender"])
    m["audit_log_integre"] = verify_chain(root / cfg["audit_log"])
    audit.log("quality_report", "qualité et biais", "AI Act art. 10 (bonne pratique) ; ISO 42001",
              rapport="reports/rapport_qualite.md")
    return m


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="config/pipeline.yaml")
    p.add_argument("--root", default=".")
    a = p.parse_args()
    root = Path(a.root)
    metrics = run(Path(a.config), root)
    (root / "reports").mkdir(exist_ok=True)
    (root / "reports" / "rapport_qualite.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    from .report import render
    (root / "reports" / "rapport_qualite.md").write_text(render(metrics), encoding="utf-8")
    print(f"OK run {metrics['run_id']} — rapport : reports/rapport_qualite.md")


if __name__ == "__main__":
    main()
