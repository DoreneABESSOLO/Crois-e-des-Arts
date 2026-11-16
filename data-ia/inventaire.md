# Étape 1 — Inventaire des données

Une ligne par donnée, pour chaque module, au format du how-to (étape 1). Les cases « à voir avec Anta » sont des questions pour notre DPO, pas des trous dans le travail.

Version tableur : [`inventaire_donnees_FashMatch.xlsx`](annexes/inventaire_donnees_FashMatch.xlsx) (onglets Inventaire et Flux).

| Donnée | Module | Personnelle ? | Sensible ? | Qui la produit | Durée de conservation (V1) | Durée de conservation (V2) | Commentaire |
|---|---|---|---|---|---|---|---|
| Historique de navigation | Match | Oui (cookie, identifiant) | Non | Appli | 5 ans (par défaut) | 13 mois, si l'utilisateur accepte | Passe par un cookie donc il faut le consentement |
| Historique d'achats | Match, Pay3x | Oui | Non | Appli | 5 ans (par défaut) | Compte + 3 ans d'inactivité | Utilisé aussi pour le score Pay3x en V1 |
| Préférences déclarées | Match | Oui | Non | Utilisateur | 5 ans (par défaut) | Durée du compte |  |
| Tendances du moment | Match | Non (statistique agrégée) | Non | Appli | - | - | Pas personnelles si les groupes sont assez grands |
| Selfie ou photo en pied | Cabine, Insight | Oui | à voir avec Anta | Utilisateur | 5 ans (par défaut), stocké en clair | Pas stocké, traité en mémoire | Peut être la photo de quelqu'un d'autre (cas de la femme sur le forum) |
| Tenue choisie | Cabine | Oui, liée au compte | Non | Utilisateur | 5 ans (par défaut) | Durée courte, à fixer avec Anta |  |
| Image générée | Cabine | Oui | à voir avec Anta | Modèle génératif | 5 ans (par défaut) | Durée courte, à fixer avec Anta | Partagée sur les réseaux sans mention IA en V1 |
| Messages à Stella | Stella | Oui | à voir avec Anta | Utilisateur | 5 ans (par défaut), gardés pour améliorer le service | Durée courte, à fixer avec Anta | Texte libre, la personne peut parler de sa santé, religion... |
| Réponses de Stella | Stella | Oui, liées à la conversation | Non | Fournisseur du modèle d'IA | 5 ans (par défaut) | Durée courte, à fixer avec Anta |  |
| Photo du visage | Âge | Oui | à voir avec Anta | Utilisateur | 5 ans (par défaut) | Pas stockée, traitée en mémoire | Une ado de 14 ans est passée avec une photo retouchée |
| Âge estimé | Âge | Oui (donnée déduite) | Non | Modèle | 5 ans (par défaut) | On garde seulement oui/non 15 ans et + |  |
| Âge déclaré | Âge | Oui | Non | Utilisateur | 5 ans (par défaut) | Durée du compte | En V1 il ne sert à rien, l'estimation passe devant |
| Refus d'inscription | Âge | Oui | Non | Modèle | 5 ans (par défaut) | Durée du compte | Pas d'explication ni de recours en V1 |
| Incidents de paiement | Pay3x | Oui | Non | Prestataire de paiement | 5 ans (par défaut) | Restent chez le prestataire |  |
| Données envoyées par le prestataire | Pay3x | Oui | Non | Prestataire de paiement | 5 ans (par défaut) | On ne les reçoit plus | Le sujet ne dit pas lesquelles |
| Score Pay3x | Pay3x | Oui | Non | Modèle FashMatch | 5 ans (par défaut) | Plus calculé chez nous | C'est le prestataire qui décide en V2 |
| Décision Pay3x | Pay3x | Oui | Non | Modèle FashMatch | 5 ans (par défaut) | Chez le prestataire, durée du paiement | Refus sans motif en V1 |
| Religion, orientation sexuelle, origine (déduites) | Insight | Oui (donnée déduite) | Oui (art. 9) | Modèle Insight | 5 ans (par défaut) | Supprimé | Interdit, module retiré |
| Segments marketing | Insight | Oui | Oui (art. 9) | Modèle Insight | 5 ans (par défaut) | Supprimé | Faits à partir des données au-dessus |
| Données clients utilisées pour l'entraînement | Match, Cabine, Stella | Oui | Selon les données copiées | Copie des données | 5 ans (par défaut) | Supprimées, opt-in pour la suite | Question du journaliste |

**Rappels du cours appliqués**

- Une donnée pseudonymisée (`user_id`) reste personnelle ; seule une statistique agrégée sur des groupes assez grands ne l'est plus (tendances du moment).
- Un identifiant technique ou un cookie qui renvoie à quelqu'un est une donnée personnelle (historique de navigation).

**Notes**

- On a mis uniquement les données décrites dans le sujet (6 modules).
- Le sujet dit que les données sont conservées 5 ans par défaut : on l'applique à toutes les données V1.
- Durées V2 marquées "à fixer avec Anta" : c'est la DPO qui les fixe, on ne les invente pas.
- Email, adresse... pas mis ici, c'est dans le registre d'Anta.
- Sensible : 4 cases en rouge pour Anta. Pour nous les photos ne sont pas de l'art. 9 car pas de reconnaissance faciale.
- Données pseudonymisées (user_id) : restent personnelles. Seules les statistiques agrégées ne le sont pas.
