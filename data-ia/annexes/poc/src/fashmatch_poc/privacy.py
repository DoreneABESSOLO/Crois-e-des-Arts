"""Mesures de protection des données appliquées par le pipeline."""
from __future__ import annotations

import hashlib
import hmac
import os
from datetime import date, timedelta
from pathlib import Path

import pandas as pd


def get_key(env_var: str) -> bytes:
    key = os.environ.get(env_var)
    if not key:
        # Clé éphémère : acceptable pour une démo, interdit en production
        # (en V2 la clé vient du KMS, cf. cahier des charges EX-12).
        key = os.urandom(32).hex()
        os.environ[env_var] = key
    return key.encode()


def normalise_email(s: pd.Series) -> pd.Series:
    return s.str.strip().str.lower()


def pseudonymise(df: pd.DataFrame, key: bytes, vault_path: Path, direct_ids: list[str]) -> pd.DataFrame:
    """EX-03 : remplace l'identité par un jeton HMAC-SHA256.

    La table de correspondance (jeton -> email) est écrite dans un « coffre »
    séparé ; la zone analytique ne contient plus aucun identifiant direct.
    Le jeton est déterministe pour une même clé : il permet la jointure et
    l'exercice des droits (retrouver la personne via le coffre).
    """
    out = df.copy()
    email = normalise_email(out["email"])
    out["user_id"] = email.map(lambda e: hmac.new(key, e.encode(), hashlib.sha256).hexdigest()[:24])
    vault_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"user_id": out["user_id"], "email": email}).drop_duplicates().to_csv(vault_path, index=False)
    os.chmod(vault_path, 0o600)
    return out.drop(columns=[c for c in direct_ids if c in out.columns])


def minimise(df: pd.DataFrame, allowlist: list[str]) -> tuple[pd.DataFrame, list[str]]:
    """EX-01 : ne garde que les champs nécessaires à la finalité (liste blanche)."""
    dropped = [c for c in df.columns if c not in allowlist]
    return df[[c for c in allowlist if c in df.columns]].copy(), dropped


def age_gate(df: pd.DataFrame, ref: date, min_age: int, min_credit: int) -> tuple[pd.DataFrame, int]:
    """EX-04 : exclut les moins de 15 ans ; calcule l'éligibilité au crédit (18 ans).

    Pas d'estimation faciale : on travaille sur l'âge déclaré et vérifié
    par un tiers de confiance (simulé ici par birth_year).
    """
    age = ref.year - df["birth_year"]
    keep = age >= min_age
    out = df[keep].copy()
    out["pay3x_age_ok"] = (ref.year - out["birth_year"]) >= min_credit
    return out, int((~keep).sum())


def purge(df: pd.DataFrame, ref: date, max_inactive_days: int) -> tuple[pd.DataFrame, int]:
    """EX-05 : purge automatique des comptes inactifs au-delà de la durée fixée."""
    limit = ref - timedelta(days=max_inactive_days)
    last = pd.to_datetime(df["last_activity_at"]).dt.date
    keep = last >= limit
    return df[keep].copy(), int((~keep).sum())


def consent_split(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """EX-06 : seuls les profils ayant consenti alimentent la personnalisation,
    et seuls ceux ayant consenti à l'entraînement alimentent le jeu d'entraînement."""
    return {
        "personnalisation": df[df["consent_personalisation"]].copy(),
        "entrainement": df[df["consent_training"]].copy(),
    }
