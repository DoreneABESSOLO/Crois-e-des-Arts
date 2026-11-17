# Rapport de qualité des données — POC FashMatch V2

- **Exécution** : `d4930cb7fd0a` — date de référence 2026-11-13
- **Source catalogue** : kaggle:fashion-product-images-small/styles.csv
- **Profils** : 100 % synthétiques, aucune donnée réelle, aucune photo
- **Journal d'audit** : ✅ intègre

## 1. Synthèse

| Indicateur | Avant | Après |
|---|---|---|
| Profils | 2060 | 1193 (personnalisation) / 515 (entraînement) |
| Doublons de profils | 60 | 0 |
| Incohérences âge | 42 | 0 (40 profils en quarantaine) |
| Pays non normalisés | 21 | 0 |
| Moins de 15 ans exclus | – | 188 |
| Comptes inactifs purgés | – | 299 |
| Doublons catalogue | 0 | 0 |
| Articles essayés sur avatar uniquement dans Cabine (maillots, lingerie…) | – | 2146 / 44424 |

**Champs supprimés par minimisation** : `declared_age`, `street_address`, `selfie_uri`, `pay3x_age_ok`

## 2. Complétude

Champs incomplets avant traitement :

| Champ | % renseigné |
|---|---|
| size | 95.97 |

Après traitement, `size` reste incomplet : la valeur n'est **pas imputée** (une taille inventée
dégraderait la recommandation sans que l'utilisateur le sache). Le parcours V2 la redemande.

## 3. Déséquilibres pouvant créer des biais

**Préférence de genre des profils** (ratio max/min = 10.0) :

| Valeur | % |
|---|---|
| femme | 70.3 |
| homme | 22.7 |
| mixte | 7.0 |

**Tranches d'âge** :

| Tranche | % |
|---|---|
| 15-17 | 7.3 |
| 18-24 | 28.9 |
| 25-34 | 43.7 |
| 35-44 | 17.3 |
| 45-54 | 2.5 |
| 55+ | 0.2 |

**Genre des articles du catalogue** (ratio max/min = 33.3) :

| Valeur | % |
|---|---|
| Men | 49.9 |
| Women | 41.9 |
| Unisex | 4.9 |
| Boys | 1.9 |
| Girls | 1.5 |

**Effet du consentement sur le jeu d'entraînement** : le jeu d'entraînement ne garde que les
profils ayant consenti. Vérifier qu'il reste représentatif de la base :

| Valeur | Base (%) | Entraînement (%) |
|---|---|---|
| femme | 70.3 | 72.0 |
| homme | 22.7 | 21.7 |
| mixte | 7.0 | 6.2 |

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
