"""Rendu Markdown du rapport de qualité, lisible par un tiers non technicien."""
from __future__ import annotations


def _table(d: dict, h1: str, h2: str) -> str:
    rows = "\n".join(f"| {k} | {v} |" for k, v in d.items())
    return f"| {h1} | {h2} |\n|---|---|\n{rows}\n"


def render(m: dict) -> str:
    b, a, bi = m["brut"], m["apres"], m["biais"]
    low = {k: v for k, v in b["completude_profils"].items() if v < 100}
    ok = "✅ intègre" if m["audit_log_integre"] else "❌ chaîne rompue"
    return f"""# Rapport de qualité des données — POC FashMatch V2

- **Exécution** : `{m['run_id']}` — date de référence {m['reference_date']}
- **Source catalogue** : {m['source_catalogue']}
- **Profils** : 100 % synthétiques, aucune donnée réelle, aucune photo
- **Journal d'audit** : {ok}

## 1. Synthèse

| Indicateur | Avant | Après |
|---|---|---|
| Profils | {b['profils']} | {a['profils_personnalisation']} (personnalisation) / {a['profils_entrainement']} (entraînement) |
| Doublons de profils | {b['doublons_profils_email_normalise']} | {a['doublons_user_id']} |
| Incohérences âge | {b['incoherences_profils'].get('age_declare_vs_annee_naissance')} | {a['incoherences_profils'].get('age_declare_vs_annee_naissance')} ({a['quarantaine']} profils en quarantaine) |
| Pays non normalisés | {b['incoherences_profils'].get('pays_non_iso')} | {a['incoherences_profils'].get('pays_non_iso')} |
| Moins de 15 ans exclus | – | {a['exclus_moins_15']} |
| Comptes inactifs purgés | – | {a['purges_inactifs']} |
| Doublons catalogue | {b['doublons_catalogue']} | 0 |
| Articles essayés sur avatar uniquement dans Cabine (maillots, lingerie…) | – | {a['catalogue_cabine_sur_avatar']} / {a['catalogue']} |

**Champs supprimés par minimisation** : {', '.join(f'`{c}`' for c in a['champs_supprimes'])}

## 2. Complétude

Champs incomplets avant traitement :

{_table(low, 'Champ', '% renseigné')}
Après traitement, `size` reste incomplet : la valeur n'est **pas imputée** (une taille inventée
dégraderait la recommandation sans que l'utilisateur le sache). Le parcours V2 la redemande.

## 3. Déséquilibres pouvant créer des biais

**Préférence de genre des profils** (ratio max/min = {bi['ratio_desequilibre_gender_pref']}) :

{_table(bi['profils_gender_pref'], 'Valeur', '%')}
**Tranches d'âge** :

{_table(bi['profils_tranches_age'], 'Tranche', '%')}
**Genre des articles du catalogue** (ratio max/min = {bi['ratio_desequilibre_catalogue_gender']}) :

{_table(bi['catalogue_gender'], 'Valeur', '%')}
**Effet du consentement sur le jeu d'entraînement** : le jeu d'entraînement ne garde que les
profils ayant consenti. Vérifier qu'il reste représentatif de la base :

| Valeur | Base (%) | Entraînement (%) |
|---|---|---|
""" + "\n".join(
        f"| {k} | {v} | {bi['entrainement_vs_base_gender_pref']['entrainement'].get(k, 0)} |"
        for k, v in bi['entrainement_vs_base_gender_pref']['base'].items()
    ) + f"""

## 4. Lecture et recommandations

1. **Déséquilibre de genre** : les profils sont majoritairement « femme » alors que le catalogue est
   majoritairement « Men ». Un modèle Match entraîné tel quel recommanderait un catalogue peu adapté
   à la majorité des clientes. → pondérer l'échantillonnage ou enrichir le catalogue ; suivre un
   indicateur de couverture par segment en production.
2. **Seniors sous-représentés** : la tranche 55+ pèse peu ; les recommandations y seront moins bonnes.
   → métrique de performance par tranche d'âge avant chaque mise en production.
3. **Quarantaine plutôt qu'imputation** pour les âges incohérents : l'âge conditionne l'accès (15 ans)
   et le crédit (18 ans) ; on ne le devine jamais.
4. **Jeu d'entraînement réduit** par le consentement : c'est le prix de la conformité ; à documenter
   dans la fiche du modèle (ISO 42001, AI Act art. 11 si le système devenait à haut risque).

*Rapport généré automatiquement par `fashmatch_poc.pipeline`. Ne contient aucune donnée personnelle.*
"""
