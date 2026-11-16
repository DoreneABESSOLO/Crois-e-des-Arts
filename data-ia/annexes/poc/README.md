# POC — Pipeline de données conforme FashMatch V2

Démonstration, sur un périmètre limité (module **Match** + éligibilité d'âge **Pay3x**),
qu'un traitement conforme au RGPD est implémentable. **Aucune donnée réelle, aucune photo.**

## Lancer en 3 commandes

```bash
pip install -r requirements.txt
make test      # 8 tests de conformité
make run       # génère reports/rapport_qualite.md et .json
```

Ou sans Python local : `make docker`.

Pour utiliser le vrai catalogue, déposer `styles.csv` du dataset Kaggle
[Fashion Product Images (Small)](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small)
dans `data/raw/` (non versionné, licence Kaggle). Sans ce fichier, un catalogue de substitution
au même schéma est généré pour que le POC reste exécutable par un tiers.

## Ce que fait le pipeline

| # | Étape | Mesure | Exigence | Source |
|---|---|---|---|---|
| 1 | Extraction | Profils 100 % synthétiques (seed fixe) | EX-02 | Sujet ; RGPD art. 5.1.c |
| 2 | Nettoyage | Dédoublonnage sur email normalisé, quarantaine des âges incohérents | EX-10 | RGPD art. 5.1.d |
| 3 | Pseudonymisation | HMAC-SHA256, clé en variable d'environnement, coffre séparé (chmod 600) | EX-03 | RGPD art. 4.5, 25, 32 |
| 4 | Contrôle d'âge | < 15 ans exclus, Pay3x réservé aux 18 ans et plus | EX-04 | RGPD art. 8 ; loi I&L art. 45 ; Code civil (capacité) |
| 5 | Purge | Comptes inactifs > 3 ans supprimés | EX-05 | RGPD art. 5.1.e ; référentiel CNIL |
| 6 | Minimisation | Liste blanche de champs par finalité | EX-01 | RGPD art. 5.1.c, 25 |
| 7 | Consentements | Tables séparées personnalisation / entraînement | EX-06 | RGPD art. 6.1.a, 7 |
| 8 | Chargement | SQLite zone analytique, sans identifiant direct | EX-03 | RGPD art. 32 |
| 9 | Journalisation | Journal JSONL chaîné par hash, sans donnée personnelle | EX-09 | RGPD art. 5.2, 30 ; ISO 27701 |
| 10 | Qualité | Complétude, doublons, cohérence, déséquilibres, représentativité du jeu d'entraînement | EX-10 | AI Act art. 10 (bonne pratique) ; ISO 42001 |

Toutes les règles sont paramétrées dans [`config/pipeline.yaml`](config/pipeline.yaml) : le DPO
peut relire et modifier une durée sans toucher au code.

## Arborescence

```
poc/
├── config/pipeline.yaml        règles de conformité (allowlist, durées, âges)
├── src/fashmatch_poc/
│   ├── generate.py             profils synthétiques + catalogue
│   ├── privacy.py              minimisation, pseudonymisation, âge, purge, consentements
│   ├── audit.py                journal chaîné + vérification d'intégrité
│   ├── quality.py              indicateurs de qualité et de biais
│   ├── report.py               rapport Markdown lisible par un tiers
│   └── pipeline.py             orchestration
├── tests/test_pipeline.py      tests de conformité (unittest)
├── reports/                    rapport de qualité versionné
├── Dockerfile · Makefile · requirements.txt
```

`output/` (base SQLite, journal) et `vault/` (table de correspondance) sont exclus du dépôt.

## Limites assumées

- Le contrôle d'âge simule un âge vérifié par un tiers ; l'intégration réelle (prestataire
  de vérification, double anonymat recommandé par la CNIL) est hors périmètre.
- La clé de pseudonymisation est éphémère si `FASHMATCH_PSEUDO_KEY` n'est pas définie :
  acceptable en démonstration, remplacée par le KMS en V2.
- Le POC ne traite ni photo ni conversation : Cabine et Stella sont couverts par le cahier des charges.
