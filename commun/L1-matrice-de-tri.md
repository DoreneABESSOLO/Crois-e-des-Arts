# L1 — Matrice de tri des modules FashMatch

> Co-construite DPO × Data/IA. Les qualifications marquées ⚖️ sont à confirmer par les DPO
> (L3, L5). Date de référence : 13 novembre 2026.

## Synthèse pour la direction

| Module | Décision | En une phrase | Promesse de la direction préservée ? |
|---|---|---|---|
| **Match** | 🟠 ENCADRER | Le moteur reste ; on réduit la conservation et on donne la main à l'utilisateur sur le profilage. | ✅ Recommandation personnalisée |
| **Cabine** | 🟠 ENCADRER (transformer) | Essayage uniquement sur une photo prise en direct par l'utilisateur, jamais sur une photo importée ; maillots et lingerie essayés sur un avatar ; sorties marquées « Générée par IA ». | ✅ Essayage virtuel |
| **Stella** | 🟠 ENCADRER | Stella dit qu'elle est une IA, ne garde pas les conversations par défaut, ne pousse pas de façon manipulatrice. | ✅ (conseil conservé) |
| **Âge** | 🟠 ENCADRER | Estimation traitée en mémoire, jamais décisive seule ; écart → tiers de confiance + recours humain. | ✅ Parcours fluide |
| **Pay3x** | 🟠 ENCADRER (déléguer) | La décision de crédit est confiée à un partenaire agréé ; refus motivé et recours humain ; 18 ans minimum. | ✅ Paiement fluide |
| **Insight** | 🔴 RETIRER immédiatement | Pratique interdite depuis le 2 février 2025 ; remplacé par une segmentation sur données déclarées. | — (non demandé) |

## Matrice détaillée

### Match — Recommandation

| Axe | Analyse |
|---|---|
| Données | Historique de navigation et d'achats, préférences déclarées, tendances (agrégées). Données personnelles, non sensibles. |
| RGPD | **Profilage** (art. 4.4). Bases légales : exécution du contrat pour l'historique d'achats ; consentement pour le traceur de navigation (art. 82 loi I&L, ePrivacy) ; intérêt légitime possible pour la recommandation sur achats, avec **droit d'opposition** (art. 21). Information sur le profilage (art. 13-14). Pas d'art. 22 : pas d'effet juridique ou significatif. **Non-conformité** : conservation 5 ans par défaut contraire à l'art. 5.1.e. |
| AI Act | Système d'IA à **risque minimal** ; FashMatch **fournisseur**. Aucune obligation spécifique hormis maîtrise de l'IA (art. 4). |
| Décision | 🟠 **ENCADRER** |
| Mesures | Durées : compte actif + 3 ans d'inactivité ; événements de navigation 13 mois ; interrupteur « recommandations personnalisées » dans le profil ; exclusion des mineurs 15-17 ans de tout ciblage publicitaire ; pas d'inférence sensible à partir des achats (liste noire de catégories). |
| Source | RGPD art. 5.1.c-e, 6, 13, 21, 25 ; CNIL, référentiel durées de conservation ; DSA art. 28 (mineurs) ⚖️ si FashMatch devient plateforme. |

### Cabine — Essayage virtuel

| Axe | Analyse |
|---|---|
| Données | Selfie / photo en pied, tenue choisie, image générée. Personnelles. Les photos ne sont pas des données biométriques au sens de l'art. 9 tant qu'elles ne passent pas par un traitement technique d'**identification** ⚖️. |
| RGPD | Base légale : exécution du service demandé (art. 6.1.b) pour la génération ; **consentement distinct** pour toute réutilisation à l'entraînement (art. 6.1.a, 7). **Aucune base légale** pour traiter la photo d'un tiers (crise n° 3). Photos en clair, hors UE, accès non tracés → art. 32 et chapitre V. AIPD obligatoire (technologie innovante + traitement à grande échelle de photos) — art. 35. |
| AI Act | Système génératif produisant des **hypertrucages** (deepfakes) d'une personne réelle : **art. 50.2** (marquage lisible par machine, fournisseur — délai de grâce au 2 décembre 2026 pour les systèmes mis sur le marché avant le 2 août 2026) et **art. 50.4** (information, déployeur). **Interdiction « nudification »** introduite par l'Omnibus (UE) 2026/1744, applicable au **2 décembre 2026** : générer une image dénudée/sexualisée d'une personne sans son accord doit être rendu techniquement impossible ⚖️ (le maillot de bain d'une non-cliente est exactement ce scénario). Droit pénal : C. pén. art. 226-8 et 226-8-1 (montages et hypertrucages à caractère sexuel). |
| Décision | 🟠 **ENCADRER** (transformation de la fonctionnalité) |
| Mesures | **Capture en direct dans l'app uniquement** (plus d'import de galerie) + détection du vivant (liveness, sans reconnaissance faciale) ; **maillots, lingerie, sous-vêtements et nuisettes essayés sur un avatar**, jamais sur la photo de la personne ; filtre de sortie (classifieur NSFW) ; marquage **C2PA** + mention visible « Générée par IA » incrustée ; partage désactivé par défaut, activable avec mention ; photo source traitée en mémoire, jamais stockée, image générée purgée après [durée à fixer avec la DPO] sauf sauvegarde explicite ; pas d'entraînement sans consentement distinct ; stockage chiffré en région UE ; génération limitée en débit. |
| Source | RGPD art. 5, 6, 7, 25, 32, 35, chap. V ; AI Act art. 50.2, 50.4 ; Omnibus 2026/1744 (nouvelle interdiction) ; Lignes directrices de la Commission sur l'art. 50 (juillet 2026) ; C2PA. |

### Stella — Styliste conversationnel

| Axe | Analyse |
|---|---|
| Données | Messages (peuvent contenir des données sensibles spontanées : santé, morphologie, religion), métadonnées de session. |
| RGPD | Exécution du service pour la conversation ; **conservation « pour améliorer le service » = finalité distincte** → consentement ou intérêt légitime solidement documenté ⚖️. Fournisseur du modèle GPAI = **sous-traitant** (art. 28) : contrat interdisant l'entraînement sur les données, zéro rétention, région UE ; sinon transfert hors UE (chap. V). |
| AI Act | FashMatch est **fournisseur du système Stella** (mis en service sous son nom), le fournisseur du modèle GPAI est fournisseur en amont (obligations art. 53 depuis le 2 août 2025). **Art. 50.1** applicable depuis le 2 août 2026 : informer clairement qu'on parle à une IA — **le prénom et l'avatar humain sont trompeurs en l'état**. Vigilance art. 5.1.a-b : pas de technique manipulatrice ni d'exploitation de la vulnérabilité liée à l'âge (utilisateurs de 15-17 ans). |
| Décision | 🟠 **ENCADRER** |
| Mesures | Mention permanente « Stella est une IA », avatar non photoréaliste ; prompt système + filtres d'entrée/sortie contre l'injection de prompt (OWASP LLM01) ; détection et masquage des données sensibles avant envoi au modèle ; rétention de [durée à fixer avec la DPO], réutilisation pour amélioration seulement sur opt-in, sur données pseudonymisées ; pas de relance commerciale pour les 15-17 ans ; transfert vers un conseiller humain sur demande. |
| Source | AI Act art. 4, 5.1.a-b, 50.1, 53 ; RGPD art. 5, 6, 9, 28, 44-49 ; OWASP Top 10 LLM ; Code de la consommation (pratiques commerciales trompeuses). |

### Âge — Contrôle à l'inscription

| Axe | Analyse |
|---|---|
| Données | Photo du visage, âge estimé, âge déclaré. |
| RGPD | Décision **exclusivement automatisée** de refus d'accès, sans explication ni recours, qui écrase l'âge déclaré → art. 22 et art. 13-15 non respectés ; précision insuffisante autour du seuil (marge d'erreur de plusieurs années à 15 ans) ; contournée dans la crise n° 2. Traitement disproportionné (art. 5.1.c) pour un enjeu d'inscription. |
| AI Act | Catégorisation biométrique (art. 3.40 ; l'âge figure parmi les catégories visées au considérant 16). **Art. 50.3** : information obligatoire des personnes exposées. Classement à haut risque au titre de l'annexe III 1.b discutable (l'âge comme attribut protégé) ⚖️. |
| Décision | 🟠 **ENCADRER** (décision du groupe ; l'option « retirer » reste la moins intrusive) |
| Mesures | Photo traitée en mémoire, jamais écrite ; seul un oui / non « 15 ans et + » conservé ; estimation croisée avec l'âge déclaré, jamais décisive seule ; en cas d'écart, vérification par tiers de confiance en double anonymat (recommandation CNIL) et recours humain depuis la console ; information art. 50.3 ; 18 ans pour Pay3x vérifiés par le prestataire. |
| Source | RGPD art. 5.1.c, 8, 22 ; loi I&L art. 45 (15 ans) ; AI Act art. 50.3 ; CNIL, recommandations sur la vérification de l'âge ; CEPD, déclaration sur l'age assurance (2025). |

### Pay3x — Paiement fractionné

| Axe | Analyse |
|---|---|
| Données | Historique d'achats, incidents de paiement, données du prestataire de paiement, score. |
| RGPD | **Art. 22** : décision exclusivement automatisée produisant un effet significatif ; admise si nécessaire au contrat (22.2.a) **avec garanties** : intervention humaine, expression du point de vue, contestation (22.3) + information utile sur la logique (CJUE C-634/21 *SCHUFA*, 2023 ; C-203/22 *Dun & Bradstreet*, 2025). Refus sans motif = non conforme. Un mineur ne peut pas contracter un crédit (crise n° 2). |
| AI Act | Évaluation de la solvabilité de personnes physiques = **haut risque, annexe III 5.b**, obligations applicables au **2 décembre 2027** (Omnibus). Si FashMatch calcule le score : **fournisseur** d'un système à haut risque (gestion des risques, gouvernance des données, documentation technique, journalisation, contrôle humain, enregistrement dans la base UE). |
| Autre | Directive (UE) 2023/2225 crédit à la consommation (inclut le paiement fractionné), application au 20 novembre 2026 ⚖️ : évaluation de solvabilité encadrée, droit à l'intervention humaine et à l'explication. |
| Décision | 🟠 **ENCADRER** en **déléguant** le scoring à un partenaire agréé |
| Mesures | FashMatch n'exerce plus le scoring : il transmet le panier et un jeton client ; le partenaire (établissement agréé) décide et porte les obligations de fournisseur/déployeur ; affichage d'un **motif** de refus et d'un lien de **réexamen humain** ; vérification d'âge 18 ans par le partenaire ; aucune donnée Insight ni donnée sensible dans le score. |
| Source | RGPD art. 13-15, 22 ; AI Act annexe III 5.b, art. 113 modifié ; dir. 2023/2225 ; jurisprudence CJUE citée. |

### Insight — Segmentation marketing

| Axe | Analyse |
|---|---|
| Données | Inférences à partir de photos : signes religieux, orientation sexuelle supposée, origine. |
| RGPD | Catégories particulières (art. 9) **inférées** sans aucune exception applicable ; finalité marketing incompatible avec la collecte initiale (art. 5.1.b) ; profilage discriminatoire. |
| AI Act | **Pratique interdite — art. 5.1.g** : catégorisation biométrique déduisant race, convictions religieuses, orientation sexuelle. Interdit depuis le **2 février 2025** ; amende jusqu'à 35 M€ ou 7 % du CA mondial (art. 99). |
| Décision | 🔴 **RETIRER immédiatement** |
| Mesures | Arrêt du service ; **suppression** des segments et attributs inférés, purge des journaux associés ; vérifier qu'aucun modèle n'a été entraîné sur ces attributs (sinon réentraîner) ; notification/consultation à évaluer par le DPO ⚖️. **Remplacement** : segmentation sur préférences déclarées et comportement d'achat, agrégée (seuil minimal de 50 personnes par segment), sans analyse d'image. |
| Source | AI Act art. 5.1.g, 99 ; RGPD art. 5.1.b, 9, 17. |

## Mesures transverses (s'appliquent à toute la V2)

| Constat V1 | Mesure V2 | Source |
|---|---|---|
| Services cloud en partie hors UE | Régions UE uniquement pour les données personnelles ; à défaut, clauses types + analyse d'impact du transfert | RGPD chap. V |
| Photos stockées en clair | Chiffrement au repos (KMS, clés gérées par FashMatch) et en transit (TLS 1.3) | RGPD art. 32 |
| Accès internes non journalisés | Journalisation centralisée, protégée en écriture, revue mensuelle | RGPD art. 32 ; ISO 27701 |
| Ni DPO ni référent IA | Désignation d'un DPO (suivi régulier et systématique à grande échelle) et d'un référent IA ; formation de l'équipe | RGPD art. 37 ; AI Act art. 4 ; ISO 42001 |
| Aucun audit d'accessibilité | Audit RGAA / WCAG 2.1 AA, déclaration d'accessibilité | Dir. (UE) 2019/882 (EAA) ⚖️ exemption microentreprise ; RGAA |
| Aucune AIPD | AIPD sur Cabine, Stella, Pay3x | RGPD art. 35 ; liste CNIL |

## Réponses à la crise (éléments pour la direction)

| Événement | Réponse immédiate | Réponse structurelle (V2) |
|---|---|---|
| Journaliste : photos et entraînement | Réponse factuelle validée par le DPO ; ne pas réaffirmer une conformité non démontrée | Registre L4, consentement distinct à l'entraînement, fiche modèle |
| Mineure de 14 ans + Pay3x | Suspension du compte, annulation du crédit, information des parents | Estimation d'âge encadrée + recours humain ; Pay3x délégué, 18 ans vérifiés |
| Image d'une non-cliente en maillot | Retrait du contenu, demande de déréférencement au forum (DSA), traitement comme violation de données à évaluer (art. 33-34) ⚖️ | Capture en direct uniquement, maillots et lingerie sur avatar, marquage C2PA |
