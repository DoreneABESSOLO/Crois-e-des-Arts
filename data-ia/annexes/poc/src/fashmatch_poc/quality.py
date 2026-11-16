"""Évaluation de la qualité et de la pertinence des données (EX-10)."""
from __future__ import annotations

from datetime import date

import pandas as pd

ISO_COUNTRIES = {"FR", "BE", "ES", "IT", "DE", "PT", "NL", "LU"}


def completeness(df: pd.DataFrame) -> dict[str, float]:
    return {c: round(100 * (1 - df[c].isna().mean()), 2) for c in df.columns}


def duplicates(df: pd.DataFrame, key: str | None = None) -> int:
    return int(df.duplicated(subset=[key] if key else None).sum())


def profile_consistency(df: pd.DataFrame, ref: date) -> dict[str, int]:
    issues = {}
    if {"birth_year", "declared_age"} <= set(df.columns):
        computed = ref.year - df["birth_year"]
        issues["age_declare_vs_annee_naissance"] = int(((computed - df["declared_age"]).abs() > 1).sum())
    if "country" in df.columns:
        issues["pays_non_iso"] = int((~df["country"].isin(ISO_COUNTRIES)).sum())
    if {"created_at", "last_activity_at"} <= set(df.columns):
        issues["activite_avant_creation"] = int((pd.to_datetime(df["last_activity_at"]) < pd.to_datetime(df["created_at"])).sum())
    return issues


def distribution(df: pd.DataFrame, col: str) -> dict[str, float]:
    return {str(k): round(100 * v, 1) for k, v in df[col].value_counts(normalize=True, dropna=False).items()}


def imbalance_ratio(dist: dict[str, float]) -> float:
    vals = [v for v in dist.values() if v > 0]
    return round(max(vals) / min(vals), 1) if vals else 0.0


def age_bands(df: pd.DataFrame, ref: date) -> dict[str, float]:
    age = ref.year - df["birth_year"]
    bands = pd.cut(age, [0, 17, 24, 34, 44, 54, 120], labels=["15-17", "18-24", "25-34", "35-44", "45-54", "55+"])
    return {str(k): round(100 * v, 1) for k, v in bands.value_counts(normalize=True, sort=False).items()}
