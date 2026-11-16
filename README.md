# Croisée des Arts 2026 — FashMatch V2

Projet commun MSc DPO × MSc Data/IA — La Plateforme_.
Sujet : arbitrer, encadrer et reconcevoir une IA générative de recommandation de mode pour la rendre conforme au RGPD et à l'AI Act, aujourd'hui et à l'horizon 2027.

Un seul dépôt pour le groupe, partagé avec notre DPO et avec l'équipe pédagogique. **Le dépôt fait foi.**

## Équipe

| Membre | Filière | Rôle | Livrables |
|---|---|---|---|
| Anta | DPO | Qualification RGPD et AI Act, veille, registre, inventaire IA, gestion de crise | L1 (juridique), L3, L4, L5, L6 (relecture) |
| Kahina HINNI | Data/IA | Conception : justification technique, schémas, architecture, cahier des charges | L1 (technique), pipeline, architecture, L7 |
| Dorène | Data/IA | Données : inventaire, carte des flux, analyse de risques, preuve de concept | inventaire, flux, L6, PoC |

## Planning (L0)

Planning détaillé et suivi : [`commun/L0_planning_groupe.xlsx`](commun/L0_planning_groupe.xlsx).

| Jour | Jalon | Responsable | Statut |
|---|---|---|---|
| Lun. 9/11 | Kick-off, rôles, planning | Tous | Fait |
| Mar. 10/11 | How-to tech : inventaire et premier jet de la carte des flux, revue par la DPO | Dorène, Anta | Fait |
| Mer. 11/11 | Matrice de tri L1 (partie juridique) | Anta | Fait |
| Jeu. 12/11 | Schémas avant / après et architecture, point client | Kahina | Fait |
| Ven. 13/11 | Analyse de risques L6, PoC, checklist du vendredi | Dorène, Anta | Fait |
| Lun. 16/11 | Relecture croisée DPO ↔ Data/IA, cahier des charges L7, répétition de la soutenance | Tous | En cours |
| Mar. 17/11 | **Gel du dépôt le soir**, envoi des livrables DPO par e-mail | Tous | À faire |

## Organisation du dépôt

Organisation demandée dans le how-to tech :

```
croisee-des-arts-2026/
├── README.md                 planning du groupe
├── commun/                   matrice de tri, présentation
├── dpo/                      audit, registres, AIPD
└── data-ia/
    ├── inventaire.md         étape 1
    ├── flux.md               étape 2
    ├── pipeline.md           étape 3
    ├── architecture.md       étape 4
    └── cahier-des-charges.md étape 5
```

Les fichiers qui accompagnent les étapes Data/IA sont rangés dans `data-ia/annexes/` : images des schémas et leur source (`annexes/schemas/`), inventaire en tableur, cahier des charges en PDF et preuve de concept (`annexes/poc/`). Dans `commun/`, l'analyse de risques (L6) est mise en commun avec la DPO, comme le demande le sujet, et le planning détaillé (L0) complète ce README.

Les schémas sont versionnés avec leur source, pas seulement en capture : Graphviz (`.dot`) pour la carte des flux, scripts qui génèrent des fichiers PowerPoint modifiables pour le pipeline et l'architecture.

Code couleur commun à tous les schémas : **orange** = problème V1 ou point de vigilance, **bleu** = mesure V2, rien d'autre ; tout le reste est en noir, blanc et gris. Même légende partout : acteur (ovale), traitement (rectangle arrondi), stockage (cylindre), tiers externe (hexagone), frontière (pointillés).

## Checklist du vendredi (how-to tech)

| Point | Où le vérifier | Statut |
|---|---|---|
| Chaque donnée de chaque module est dans l'inventaire | [inventaire](data-ia/inventaire.md) : 20 données, 6 modules | Fait |
| Chaque flux, interne et externe, est sur la carte | [flux](data-ia/flux.md) : 15 flux numérotés, tous les tiers | Fait |
| Le pipeline V1 et V2 ont les mêmes étapes | [pipeline](data-ia/pipeline.md) : 6 étapes des deux côtés | Fait |
| Chaque mesure V2 a une source validée par le DPO | [pipeline](data-ia/pipeline.md), colonne Source | À valider par Anta |
| L'architecture montre les frontières et le transverse | [architecture](data-ia/architecture.md) | Fait |
| Les modules retirés n'apparaissent plus | Insight absent de l'architecture | Fait |
| Chaque exigence du cahier des charges est vérifiable | [cahier des charges](data-ia/cahier-des-charges.md), colonne Vérification | Fait |
| Votre DPO a relu et compris chaque schéma | Relecture du lundi 16/11 | À faire avec Anta |

## Points ouverts pour la DPO

- Colonne « Sensible ? » de l'inventaire : selfie, image générée, photo du visage et messages à Stella (cases en rouge).
- Durées courtes notées [durée] : images générées, tenues choisies, conversations.
- Validation de la colonne Source du pipeline et de la matrice de traçabilité.
