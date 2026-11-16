# L6 — Analyse de risques data/IA (registre commun)

Risques sur tout le cycle de vie, pas seulement réglementaires. Registre partagé DPO × Data/IA.

**Échelles** — Probabilité (P) : 1 rare · 2 possible · 3 probable · 4 quasi certain.
Impact (I) : 1 faible · 2 modéré · 3 grave (préjudice pour les personnes ou sanction) · 4 critique (atteinte grave aux droits, arrêt du service).
**Criticité** = P × I : 1-4 🟢 acceptable · 5-8 🟠 à traiter · 9-16 🔴 inacceptable.
Le risque résiduel est évalué **après** mise en œuvre de la mesure V2.

| ID | Module | Cycle de vie | Source | Risque | P | I | Crit. V1 | Mesure de mitigation V2 | Rés. | Responsable |
|---|---|---|---|---|---|---|---|---|---|---|
| R01 | Cabine | Usage | Usage | Détournement : hypertrucage d'un tiers (photo importée), dont images sexualisées | 4 | 4 | 🔴 16 | Capture en direct + liveness, maillots et lingerie sur avatar, filtre NSFW, marquage C2PA, débit limité | 🟢 1×4 = 4 | Data/IA |
| R02 | Insight | Modèle | Modèle | Inférence de catégories particulières (religion, orientation, origine) | 4 | 4 | 🔴 16 | Retrait du module, purge des attributs inférés | 🟢 0 | DPO |
| R03 | Toutes | Stockage | Infra | Fuite des photos stockées en clair (bucket mal configuré) | 3 | 4 | 🔴 12 | Photo traitée en mémoire (plus de stockage) ; images générées chiffrées KMS en UE, accès par rôle | 🟢 1×4 = 4 | Data/IA |
| R04 | Toutes | Stockage | Infra | Transfert hors UE non encadré | 3 | 3 | 🔴 9 | Régions UE, DPA, clauses types en secours | 🟢 1×3 = 3 | DPO |
| R05 | Toutes | Sécurité | Humain | Accès interne abusif non détecté | 2 | 3 | 🟠 6 | Moindre privilège, MFA, journal protégé, revue mensuelle | 🟢 1×3 = 3 | Data/IA |
| R06 | Stella | Usage | Usage | Injection de prompt (fuite du prompt système, contournement des garde-fous) | 3 | 3 | 🔴 9 | Cloisonnement des instructions, filtres entrée/sortie, aucun outil à privilèges, tests red team | 🟠 2×3 = 6 | Data/IA |
| R07 | Stella | Modèle | Modèle | Hallucination : promesse fausse (prix, retours, matière, allergènes) | 3 | 2 | 🟠 6 | Réponses ancrées sur le catalogue (RAG), refus hors périmètre, renvoi vers les CGV | 🟢 2×2 = 4 | Data/IA |
| R08 | Stella | Déploiement | Tiers | Le fournisseur GPAI conserve ou entraîne sur les conversations | 3 | 3 | 🔴 9 | Contrat zéro rétention / pas d'entraînement, masquage des données sensibles avant envoi | 🟢 1×3 = 3 | DPO |
| R09 | Stella | Usage | Humain | Manipulation commerciale, en particulier des 15-17 ans | 2 | 3 | 🟠 6 | Politique de recommandation non incitative, pas de relance pour les mineurs, mention IA | 🟢 1×3 = 3 | DPO |
| R10 | Âge | Modèle | Modèle | Erreur d'estimation (faux refus / faux accès), biais selon la couleur de peau | 4 | 3 | 🔴 12 | Estimation en mémoire, jamais décisive seule ; croisée avec l'âge déclaré ; tiers de confiance + recours humain | 🟢 2×2 = 4 | Data/IA |
| R11 | Pay3x | Usage | Humain | Crédit accordé à un mineur | 3 | 4 | 🔴 12 | Vérification d'identité 18 ans par le partenaire agréé | 🟢 1×4 = 4 | DPO |
| R12 | Pay3x | Modèle | Données | Score discriminatoire (variables proxy), refus inexplicable | 3 | 3 | 🔴 9 | Scoring délégué ; motif + réexamen humain ; aucune donnée sensible | 🟢 1×3 = 3 | DPO |
| R13 | Match | Données | Données | Biais de représentation (catalogue majoritairement « Men », clientèle majoritairement « femme », seniors rares) | 4 | 2 | 🟠 8 | Indicateurs de couverture par segment (rapport qualité POC), rééchantillonnage | 🟢 2×2 = 4 | Data/IA |
| R14 | Match | Déploiement | Modèle | Dérive : tendances qui changent, performance qui baisse sans alerte | 3 | 2 | 🟠 6 | Monitoring hebdomadaire (taux de clic, couverture), seuil d'alerte, réentraînement planifié | 🟢 2×2 = 4 | Data/IA |
| R15 | Cabine, Match | Entraînement | Données | Réutilisation de données client pour l'entraînement sans base légale | 4 | 3 | 🔴 12 | Jeu d'entraînement séparé, alimenté uniquement par consentement, traçabilité de l'origine | 🟢 1×3 = 3 | DPO |
| R16 | Cabine | Modèle | Modèle | Fuite de données d'entraînement (le modèle régénère des visages de clients) | 2 | 4 | 🟠 8 | Pas d'ajustement fin sur visages clients ; tests d'extraction avant mise en production | 🟢 1×4 = 4 | Data/IA |
| R17 | Toutes | Suppression | Infra | Données conservées au-delà de la durée (5 ans par défaut) | 4 | 2 | 🟠 8 | Purge automatique planifiée, testée (POC), règles de cycle de vie du stockage | 🟢 1×2 = 2 | Data/IA |
| R18 | Toutes | Usage | Humain | Personne en situation de handicap exclue du parcours d'achat | 3 | 2 | 🟠 6 | Audit RGAA, alternative textuelle à Cabine, Stella compatible lecteur d'écran | 🟢 1×2 = 2 | Data/IA |
| R19 | Cabine | Usage | Infra | Abus du service : génération massive automatisée, coûts | 3 | 2 | 🟠 6 | Quotas par compte, captcha, détection d'automatisation | 🟢 2×1 = 2 | Data/IA |
| R20 | Toutes | Gouvernance | Humain | Communication publique de conformité non étayée (risque réputationnel, pratique trompeuse) | 4 | 3 | 🔴 12 | Registre, AIPD, matrice de traçabilité comme preuves ; validation DPO de toute communication | 🟢 1×3 = 3 | DPO |
| R21 | Toutes | Gouvernance | Réglementaire | Échéance manquée (2 déc. 2026 : nudification, marquage ; 2 déc. 2027 : haut risque) | 3 | 3 | 🔴 9 | Feuille de route (cahier des charges §8), veille L3 mensuelle | 🟢 1×3 = 3 | DPO |


## Lecture

- **Risques inacceptables en V1 : 12 sur 21**, dont deux à criticité maximale (Cabine détourné, Insight).
- **Après V2 : aucun risque rouge.** Un seul reste orange : l'injection de prompt (R06), car aucune
  défense n'est complète face à un modèle de langage → **accepté** sous condition de tests red team
  trimestriels. R01 (Cabine) devient acceptable mais garde un impact critique : il est suivi en priorité.
- Les impacts « critiques » (4) ne baissent presque jamais : on agit sur la **probabilité**.
  C'est pourquoi l'architecture V2 supprime les causes (import de photos, score interne, module Insight)
  plutôt que d'empiler des contrôles.
