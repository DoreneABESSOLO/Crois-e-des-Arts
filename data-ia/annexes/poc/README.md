# POC — Pipeline de données conforme FashMatch V2

Démonstration, sur un périmètre limité (module **Match** + éligibilité d'âge **Pay3x**),
qu'un traitement conforme au RGPD est implémentable.

**Données utilisées** :

- **Catalogue réel** : `styles.csv` du dataset public Kaggle
  [Fashion Product Images (Small)](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small),
  44 424 articles, aucune donnée personnelle.
- **Profils clients 100 % synthétiques** : 2 000 profils générés par code (seed fixe), aucune photo,
  avec des défauts injectés volontairement (doublons, âges incohérents, champs sur-collectés).
  Utiliser de vrais profils pour une démonstration serait contraire au RGPD (art. 5.1.c).

## Lancer le POC

Toutes les commandes s'exécutent depuis le dossier `data-ia/annexes/poc/`. Python 3.10 ou plus.

### 1. Installer les dépendances

```bash
python -m pip install -r requirements.txt kagglehub
```

### 2. Récupérer le catalogue Kaggle

`styles.csv` n'est pas versionné (licence Kaggle). On ne télécharge que ce fichier (4 Mo),
pas le dataset complet (environ 600 Mo d'images) :

```bash
python -c "import kagglehub, shutil; shutil.copy(kagglehub.dataset_download('paramaggarwal/fashion-product-images-small', path='styles.csv'), 'data/raw/styles.csv')"
```

Sans ce fichier, un catalogue de substitution au même schéma est généré automatiquement pour que
le POC reste exécutable ; le rapport l'indique alors dans « Source catalogue ».

### 3. Tester et exécuter

Windows (PowerShell) :

```powershell
$env:PYTHONPATH = "src"; python -m unittest discover -s tests -v   # 8 tests de conformité
$env:PYTHONPATH = "src"; python -m fashmatch_poc.pipeline          # génère le rapport
```

Linux / macOS (avec `make`) : `make test` puis `make run`. Avec Docker : `make docker`.

Optionnel : définir `FASHMATCH_PSEUDO_KEY` pour une clé de pseudonymisation fixe
(sinon clé éphémère à chaque exécution).

## Résultats obtenus

Exécution avec le catalogue Kaggle : **8 tests sur 8 réussis**, journal d'audit intègre.

| Étape | Résultat |
|---|---|
| Profils bruts | 2 060 (2 000 + 60 doublons injectés) |
| Doublons supprimés | 60 |
| Âges incohérents mis en quarantaine | 40 |
| Moins de 15 ans exclus | 188 |
| Comptes inactifs > 3 ans purgés | 299 |
| Profils de personnalisation (pseudonymisés, minimisés) | 1 193 |
| Profils d'entraînement (consentement spécifique) | 515 |
| Profils vérifiés pour Pay3x | 1 473 |
| Articles du catalogue | 44 424 (0 doublon) |
| Articles réservés à l'essayage sur avatar (maillots, lingerie…) | 2 146 |

Biais mis en évidence : le catalogue réel est majoritairement masculin (49,9 % « Men », 41,9 %
« Women ») alors que la clientèle simulée est à 70 % féminine. Détail complet :
[`reports/rapport_qualite.md`](reports/rapport_qualite.md).

Fichiers produits (non versionnés) : `output/fashmatch_v2.sqlite` (zone analytique),
`output/audit_log.jsonl` (journal chaîné), `vault/correspondance.csv` (coffre de correspondance).

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
