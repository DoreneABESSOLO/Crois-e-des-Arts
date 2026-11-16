"""Génération des données d'entrée du POC.

- Profils utilisateurs 100 % synthétiques (aucune donnée réelle, aucune photo).
- Catalogue : on utilise styles.csv de Kaggle s'il est présent dans data/raw/,
  sinon un catalogue de substitution au même schéma est généré.

Des défauts sont injectés volontairement (doublons, valeurs manquantes,
incohérences, champs sur-collectés) pour que le pipeline ait quelque chose
à corriger et que le rapport de qualité soit démonstratif.
"""
from __future__ import annotations

import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

FIRST = ["Lina", "Yanis", "Sarah", "Adam", "Inès", "Lucas", "Nora", "Hugo", "Maya", "Rayan",
         "Chloé", "Nael", "Léa", "Ilyes", "Jade", "Tom", "Amel", "Noah", "Zoé", "Sami"]
LAST = ["Martin", "Bernard", "Haddad", "Petit", "Moreau", "Benali", "Garcia", "Roux",
        "Fontaine", "Mansouri", "Lefebvre", "Nguyen", "Diallo", "Rossi", "Durand"]
STYLES = ["casual", "streetwear", "chic", "sport", "boheme", "minimaliste", "vintage"]
SIZES = ["XS", "S", "M", "L", "XL", "XXL"]
COUNTRIES = ["FR"] * 8 + ["BE", "ES", "IT", "DE"]


def generate_profiles(n: int, seed: int, ref: date) -> pd.DataFrame:
    rng = random.Random(seed)
    rows = []
    for i in range(n):
        fn, ln = rng.choice(FIRST), rng.choice(LAST)
        # Distribution d'âge volontairement déséquilibrée (biais à détecter)
        age = int(min(75, max(12, rng.gauss(27, 9))))
        created = ref - timedelta(days=rng.randint(1, 365 * 6))
        last_act = created + timedelta(days=rng.randint(0, max(0, (ref - created).days)))
        rows.append({
            "email": f"{fn}.{ln}{i}@example.test".lower(),
            "full_name": f"{fn} {ln}",
            "phone": f"+3360000{i:04d}",
            "birth_year": ref.year - age,
            "declared_age": age,
            # 70 % de préférences « femme » : déséquilibre à signaler
            "gender_pref": rng.choices(["femme", "homme", "mixte"], [0.70, 0.22, 0.08])[0],
            "style_prefs": "|".join(rng.sample(STYLES, rng.randint(1, 3))),
            "size": rng.choice(SIZES),
            "country": rng.choice(COUNTRIES),
            "street_address": f"{rng.randint(1, 200)} rue Synthétique",   # sur-collecte
            "selfie_uri": f"s3://fm-v1-photos/{i}.jpg",                     # sur-collecte (V1)
            "consent_personalisation": rng.random() < 0.82,
            "consent_training": rng.random() < 0.35,
            "created_at": created.isoformat(),
            "last_activity_at": last_act.isoformat(),
        })
    df = pd.DataFrame(rows)

    # Défauts injectés
    idx = df.sample(frac=0.04, random_state=seed).index
    df.loc[idx, "size"] = None                                   # complétude
    idx = df.sample(frac=0.02, random_state=seed + 1).index
    df.loc[idx, "birth_year"] = df.loc[idx, "birth_year"] + 9    # incohérence âge déclaré / année
    idx = df.sample(frac=0.01, random_state=seed + 2).index
    df.loc[idx, "country"] = "France"                            # format non normalisé
    dups = df.sample(frac=0.03, random_state=seed + 3)
    dups = dups.assign(email=dups["email"].str.upper())          # doublons « cachés »
    return pd.concat([df, dups], ignore_index=True)


def substitute_catalogue(seed: int, n: int = 3000) -> pd.DataFrame:
    rng = random.Random(seed)
    cats = {
        "Apparel": ["Tshirts", "Shirts", "Jeans", "Dresses", "Tops", "Trousers", "Swimwear"],
        "Footwear": ["Casual Shoes", "Sports Shoes", "Heels", "Sandals"],
        "Accessories": ["Watches", "Bags", "Belts", "Sunglasses"],
    }
    rows = []
    for i in range(n):
        mc = rng.choices(list(cats), [0.55, 0.25, 0.20])[0]
        rows.append({
            "id": 10000 + i,
            "gender": rng.choices(["Men", "Women", "Unisex", "Boys", "Girls"], [0.48, 0.38, 0.06, 0.04, 0.04])[0],
            "masterCategory": mc,
            "subCategory": mc,
            "articleType": rng.choice(cats[mc]),
            "baseColour": rng.choice(["Black", "White", "Blue", "Red", "Green", "Navy Blue", None]),
            "season": rng.choice(["Summer", "Winter", "Fall", "Spring"]),
            "year": rng.choice([2015, 2016, 2017, 2018]),
            "usage": rng.choice(["Casual", "Formal", "Sports", "Ethnic"]),
            "productDisplayName": f"Produit synthétique {i}",
        })
    df = pd.DataFrame(rows)
    return pd.concat([df, df.sample(frac=0.01, random_state=seed)], ignore_index=True)


def load_catalogue(raw_dir: Path, seed: int) -> tuple[pd.DataFrame, str]:
    kaggle = raw_dir / "styles.csv"
    if kaggle.exists():
        # Le fichier Kaggle contient quelques lignes mal formées : on les écarte et on les compte
        df = pd.read_csv(kaggle, on_bad_lines="skip")
        return df, "kaggle:fashion-product-images-small/styles.csv"
    return substitute_catalogue(seed), "catalogue de substitution (styles.csv absent)"
