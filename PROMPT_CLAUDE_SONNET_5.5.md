# PROMPT COMPLET À DONNER À CLAUDE SONNET 5.5

## RÔLE

Tu es un consultant senior en transformation digitale agricole, en administration publique et en systèmes d'information, avec une expertise vérifiée sur le Burundi. Tu as accès au web. Ta mission est de vérifier la réalité des données et du fonctionnement d'une application de gestion des engrais appelée « FOMI Stock », puis de produire un rapport de correction directement exploitable.

Tu ne dois pas te contenter de confirmer ce que je te donne. Tu dois chercher, recouper, critiquer et corriger. Si une information n'est pas publique ou pas vérifiable, tu dois l'écrire clairement au lieu de l'inventer.

## RÈGLES ABSOLUES

1. Ne jamais inventer un fait, un nom de province, une commune, une zone, une colline, un prix, un sigle ou une procédure.
2. Pour chaque fait important, donner : la source (URL), l'organisme, la date de publication et la date de consultation.
3. Classer chaque affirmation :
   - ✅ VÉRIFIÉ : confirmé par au moins une source officielle ou deux sources fiables.
   - ⚠️ PLAUSIBLE NON CONFIRMÉ : cohérent mais sans source suffisante.
   - ❌ FAUX / INVENTÉ : contredit par les sources.
   - ❓ NON TROUVÉ : information introuvable publiquement.
4. Si une information est introuvable, ne pas la remplacer par une supposition. Indiquer qui pourrait la fournir (FOMI, Ministère de l'Agriculture, INS, commune, zone, coopérative) et sous quelle forme (document, appel, email).
5. Répondre en français, avec des tableaux lisibles et des phrases simples.
6. Ne pas prétendre avoir testé l'application : tu n'as pas accès à `localhost`. Tu travailles à partir du snapshot fourni ci-dessous.
7. Ne jamais utiliser les données personnelles d'une personne réelle dans les exemples. Les noms proposés doivent être fictifs mais réalistes.
8. Être critique : signaler les incohérences, les risques juridiques, les données trop détaillées pour un simple stage, et les fonctionnalités surdimensionnées.
9. Prioriser les corrections : P0 (donnée fausse ou bloquante), P1 (UX ou métier important), P2 (amélioration).
10. Citer les sources dans le texte avec des numéros [S1], [S2], etc., puis les lister à la fin.

## CONTEXTE DE L'APPLICATION

Application web « FOMI Stock » destinée à la gestion des engrais au Burundi.

- Backend : Spring Boot 3, Java 21, PostgreSQL, API REST, authentification JWT.
- Frontend : React + Vite, mode clair et mode sombre, responsive.
- Rôles : `ADMIN`, `SUPERVISEUR`, `AGENT_ZONE`, `AGENT_COLLINE`, `AGENT_LOGISTIQUE`.
- Modèle géographique cible : `Province → Commune → Zone → Colline`.
- Deux niveaux de dépôts seulement : `PROVINCE` (logistique) et `ZONE` (distribution).
- Les collines sont des lieux de résidence des agriculteurs, pas des lieux de stockage.
- Modules : tableau de bord, dépôts, tickets, distributions, agriculteurs, mouvements de stock, alertes, utilisateurs, journal d'audit, suivi public d'un ticket.
- Notifications email aux agriculteurs, export CSV, journal d'audit.

## SNAPSHOT EXACT DES DONNÉES À VÉRIFIER

### Provinces actuellement en base (3 seulement)

| Code | Nom |
|---|---|
| GIT | Gitega |
| BUB | Bubanza |
| NGO | Ngozi |

### Communes actuellement en base (5)

| Code | Nom | Province |
|---|---|---|
| GIT-CO-GIT | Gitega | Gitega |
| GIT-CO-BUG | Bugendana | Gitega |
| BUB-CO-BUB | Bubanza | Bubanza |
| BUB-CO-MUS | Musigati | Bubanza |
| NGO-CO-NGO | Ngozi | Ngozi |

### Zones actuellement en base (4)

| Code | Nom | Commune |
|---|---|---|
| GIT-C | Gitega Centre | Gitega |
| GIT-N | Gitega Nord | Bugendana |
| BUB-O | Bubanza Ouest | Bubanza |
| NGO-C | Ngozi Centre | Ngozi |

### Collines actuellement en base (6)

| Code | Nom | Zone |
|---|---|---|
| GIT-C-MUT | Mutaho | Gitega Centre |
| GIT-C-BIS | Bisoro | Gitega Centre |
| GIT-N-GIS | Gisozi | Gitega Nord |
| BUB-O-MUS | Musigati | Bubanza Ouest |
| BUB-O-RUG | Rugazi | Bubanza Ouest |
| NGO-C-MWE | Mwendo | Ngozi Centre |

### Dépôts actuellement en base (9)

| Code | Nom | Niveau | Province | Zone | Seuil d'alerte (sacs) |
|---|---|---|---|---|---|
| DEP-GIT-P | Dépôt Provincial Gitega | PROVINCE | Gitega | — | 500 |
| DEP-BUB-P | Dépôt Provincial Bubanza | PROVINCE | Bubanza | — | 300 |
| DEP-NGO-P | Dépôt Provincial Ngozi | PROVINCE | Ngozi | — | 200 |
| DEP-GIT-Z | Dépôt Zone Gitega Centre | ZONE | — | Gitega Centre | 200 |
| DEP-BUB-Z | Dépôt Zone Bubanza Ouest | ZONE | — | Bubanza Ouest | 150 |
| DEP-MUT | Dépôt Zone Mutaho | ZONE | — | Mutaho | 50 |
| DEP-BIS | Dépôt Zone Bisoro | ZONE | — | Bisoro | 50 |
| DEP-MUS | Dépôt Zone Musigati | ZONE | — | Musigati | 50 |
| DEP-MWE | Dépôt Zone Mwendo | ZONE | — | Mwendo | 50 |

### Engrais actuellement en base (3)

| Code | Nom | Poids du sac | Prix subventionné (BIF) |
|---|---|---|---|
| UREE | Urée | 50 kg | 25 000 |
| NPK | NPK 17-17-17 | 50 kg | 30 000 |
| DAP | DAP | 50 kg | 35 000 |

### Exemples de stocks affichés à l'écran

| Dépôt | Engrais | Disponible | Seuil | État |
|---|---|---|---|---|
| Dépôt Provincial Gitega | NPK 17-17-17 | 800 | 500 | OK |
| Dépôt Provincial Gitega | Urée | 1 500 | 500 | OK |
| Dépôt Provincial Bubanza | Urée | 1 200 | 300 | OK |
| Dépôt Provincial Ngozi | Urée | 0 | 200 | Rupture |
| Dépôt Zone Gitega Centre | Urée | 400 | 200 | OK |
| Dépôt Zone Mutaho | Urée | 80 | 50 | OK |
| Dépôt Zone Musigati | Urée | 40 | 50 | Bas |

### Tickets actuellement en base (9)

| Numéro | Agriculteur | Engrais | Quantité commandée | Quantité servie | Statut |
|---|---|---|---|---|---|
| TKT-2026-1247 | Ndayisaba Jean | UREE | 5 | 3 | PARTIEL |
| TKT-2026-1248 | Niyonkuru Marie | UREE | 3 | 0 | EN_ATTENTE |
| TKT-2026-1249 | Havyarimana Pierre | NPK | 2 | 2 | SERVI |
| TKT-2026-1250 | Nshimirimana Alice | UREE | 4 | 0 | RECLAMATION |
| TKT-2026-1251 | Bizimana Emmanuel | UREE | 6 | 0 | PAYE |
| TKT-MAIL-DEMO-1 | Ndayisaba Jean | UREE | 1 | 0 | EN_ATTENTE_DE_VALIDATION |
| TKT-E2E-VAL-20261102211426 | Havyarimana Pierre | UREE | 2 | 2 | SERVI |
| TKT-E2E-REJ-20261102211426 | Bizimana Emmanuel | NPK | 1 | 0 | REJETE |
| TKT-E2E-EXPIRE-20261103034146 | Nshimirimana Alice | DAP | 3 | 0 | EXPIRE |

Les montants payés en base correspondent à `quantité × prix du sac` : 5 × 25 000 = 125 000 BIF, 3 × 25 000 = 75 000 BIF, etc. L'interface affiche pourtant « Quantité commandée (kg) ». Il faut vérifier si la vraie unité est le sac de 50 kg ou le kg.

### Statuts de ticket implémentés

`EN_ATTENTE_DE_VALIDATION`, `ACTIF`, `REJETE`, `EXPIRE`, `PAYE`, `EN_ATTENTE`, `PARTIEL`, `SERVI`, `RECLAMATION`, `ANNULE`.

### Règles actuelles dans le code

- `Activer` et `Rejeter` : réservés aux rôles `ADMIN` et `SUPERVISEUR`.
- `Modifier` : réservé à `ADMIN` et `AGENT_ZONE`, et seulement si `quantiteServie = 0`.
- `Rejeter` : possible uniquement depuis le statut `EN_ATTENTE_DE_VALIDATION`, avec un motif optionnel.
- Aucun écran ne permet de créer une réclamation : le statut `RECLAMATION` n'existe que dans les données de démonstration.
- Les tickets `TKT-MAIL-DEMO-1` et `TKT-E2E-*` sont des artefacts de test (test d'email et tests automatisés), pas des tickets réels.
- 500 agriculteurs de démonstration portent les noms `Nom1 Prenom1`, `Nom2 Prenom2`, etc.

## MISSION 1 — VÉRIFIER LE DÉCOUPAGE ADMINISTRATIF DU BURUNDI

Recherche et réponds précisément :

1. Combien de provinces le Burundi compte-t-il officiellement aujourd'hui ? Donne la liste complète des 18 provinces avec leurs codes officiels si disponibles.
2. Combien de communes ? Donne le nombre officiel et, si possible, la liste complète ou un fichier CSV.
3. La hiérarchie officielle est-elle bien `Province → Commune → Zone → Colline` ? La « zone » est-elle un niveau administratif officiel dans toutes les provinces, ou seulement dans certaines villes ? La « colline » est-elle le quatrième niveau officiel ?
4. Quels sont les termes officiels en kirundi et en français : province, commune, zone, colline ?
5. Les entités suivantes existent-elles réellement, et à quel niveau ?
   - Gitega, Bugendana, Bubanza, Musigati, Ngozi (communes ?)
   - Gitega Centre, Gitega Nord, Bubanza Ouest, Ngozi Centre (zones ?)
   - Mutaho, Bisoro, Gisozi, Musigati, Rugazi, Mwendo (collines ? communes ? zones ?)
6. Pour les provinces de Gitega, Bubanza et Ngozi, donne la liste réelle des communes, puis des zones et collines si les sources le permettent.
7. Les noms `Mutaho`, `Bisoro`, `Gisozi`, `Musigati`, `Rugazi`, `Mwendo` sont-ils utilisés au bon niveau dans l'application ? Par exemple, `Musigati` est-il une commune, une zone ou une colline ? `Rugazi` ? `Mwendo` ? `Gisozi` ?
8. Existe-t-il des codes administratifs officiels (code province, code commune, code colline) utilisés par l'INS ou le Ministère de l'Intérieur ? Si oui, donne le format.
9. Sources à privilégier : textes officiels du Burundi, INS (Institut National de la Statistique), RGPH, annuaires statistiques, documents de la Présidence, du Ministère de l'Intérieur, du Ministère de l'Agriculture, Banque mondiale, FAO, PNUD, IFDC. Cite les URLs et les dates.

## MISSION 2 — VÉRIFIER FOMI

1. Que signifie exactement le sigle FOMI ? Donne le nom complet officiel en français et en anglais s'il existe.
2. Quel est le statut juridique de FOMI : projet, programme, société publique, office, agence, partenariat public-privé ?
3. Quelle est sa mission exacte dans la filière des engrais et intrants agricoles au Burundi ?
4. Quel est son lien avec le Ministère de l'Agriculture et de l'Élevage ? Est-elle sous tutelle directe ?
5. Depuis quand existe-t-elle ? Quels textes ou accords l'ont créée ?
6. Quels sont ses partenaires : État, bailleurs, importateurs, banques, coopératives, OTB, etc. ?
7. Comment FOMI organise-t-elle physiquement la distribution : dépôts provinciaux, dépôts de zone, points de vente, coopératives ? Le modèle « dépôt provincial + dépôt de zone » est-il réel ?
8. Existe-t-il un système d'information officiel de FOMI ? Si oui, lequel, et l'application devrait-elle s'y intégrer ?
9. Quels sont les canaux de contact officiels de FOMI : adresse, téléphone, email, site web, bureaux provinciaux ?
10. Si le sigle FOMI est ambigu ou recouvre plusieurs entités, signale-le clairement.

## MISSION 3 — VÉRIFIER LES ENGRAIS, LES UNITÉS, LES PRIX ET LES SEUILS

1. La FOMI distribue-t-elle réellement de l'Urée, du NPK 17-17-17 et du DAP ? Les trois sont-ils disponibles aux agriculteurs ?
2. Le sac standard est-il de 50 kg ? Existe-t-il d'autres conditionnements (25 kg, 1 kg) ?
3. Les prix subventionnés de 25 000 BIF (Urée), 30 000 BIF (NPK) et 35 000 BIF (DAP) sont-ils réels pour 2024, 2025 ou 2026 ? Donne les prix officiels par sac et par kg, avec la source et la date. Si les prix ont changé, donne l'historique.
4. Le DAP est-il réellement distribué par la FOMI, ou est-il plutôt utilisé par d'autres cultures/filières ?
5. L'unité utilisée dans les tickets est-elle le sac de 50 kg, le kg, ou les deux ? Explique l'incohérence entre les montants (5 × 25 000 = 125 000 BIF) et le libellé « kg ».
6. Les seuils d'alerte de 500, 300, 200, 150 et 50 sacs sont-ils réalistes ? Comment un responsable FOMI calcule-t-il réellement un seuil de sécurité : consommation moyenne, délai de réapprovisionnement, stock de sécurité, saisonnalité ?
7. Le seuil doit-il être défini par dépôt et par engrais, ou globalement par dépôt ? L'application utilise aujourd'hui un seul seuil par dépôt, identique pour l'Urée et le NPK. Est-ce correct ?
8. Les saisons agricoles `2026A` et `2026B` sont-elles les bonnes notations au Burundi ? Quelles sont les saisons officielles (A, B, C) et leurs périodes ?
9. Quelles sont les quantités maximales par agriculteur : par hectare, par saison, par culture ? Existe-t-il des quotas ou des cartes d'agriculteur ?
10. Quels sont les modes de paiement réels : espèces, banque, mobile money (Lumicash, Ecobank, etc.), coopérative ? Un reçu est-il obligatoire ?
11. Comment les prix, subventions et quotas sont-ils annoncés officiellement chaque saison ?
12. Sources à privilégier : communiqués du Ministère de l'Agriculture, de la FOMI, de l'ABN, de la Banque mondiale, de la FAO, de l'IFDC, de l'USAID, de l'Union européenne, presse burundaise fiable (Iwacu, Burundi Eco, etc.).

## MISSION 4 — VÉRIFIER LE PROCESSUS TICKET, VALIDATION, REJET ET RÉCLAMATION

1. Décris le circuit réel d'un ticket FOMI, de l'inscription de l'agriculteur jusqu'au retrait de l'engrais.
2. Qui crée le ticket : l'agriculteur, la coopérative, l'agent de zone, l'agent FOMI, la commune ?
3. Qui valide le paiement et qui valide le ticket ? Quel rôle exact : agent de zone, agronome communal, responsable FOMI, superviseur ?
4. Qui peut rejeter un ticket ? Le rejet est-il une pratique courante ou exceptionnelle ?
5. Quels sont les motifs légitimes de rejet : paiement non confirmé, doublon, quota dépassé, identité erronée, hors saison, stock indisponible, dossier incomplet, fraude ?
6. Existe-t-il un droit de recours après rejet ? Sous quel délai ? Auprès de qui ?
7. Les statuts `EN_ATTENTE_DE_VALIDATION`, `ACTIF`, `REJETE`, `EXPIRE`, `PAYE`, `EN_ATTENTE`, `PARTIEL`, `SERVI`, `RECLAMATION`, `ANNULE` correspondent-ils au processus réel ? Lesquels sont inventés ou redondants ? Propose une machine à états simplifiée et réaliste.
8. Que signifie concrètement `EN_ATTENTE_DE_VALIDATION` ? Qu'est-ce qui est validé : le paiement, l'identité, le quota, la disponibilité du stock ? Quel est le délai normal ?
9. Le ticket `TKT-MAIL-DEMO-1` est un ticket de démonstration créé pour tester l'envoi d'email. Dans la vraie vie, un tel ticket devrait-il exister ? Comment le distinguer des vrais tickets ?
10. Le ticket `TKT-E2E-REJ-20261102211426` est un artefact de test automatisé. Comment éviter que des données de test polluent la base de production et les écrans de démonstration ?
11. Une réclamation est-elle un statut de ticket, une entité séparée, ou un ticket de type « réclamation » ? Où l'agriculteur dépose-t-il sa réclamation : au dépôt, à la zone, à la commune, au bureau FOMI, par téléphone, par SMS, par email ?
12. Quelles preuves ou informations sont demandées : numéro de ticket, reçu de paiement, carte d'identité, carte d'agriculteur, nom de la colline ?
13. Quels sont les délais de traitement d'une réclamation ? Qui instruit ? Qui décide ? Quelles issues possibles : remboursement, remplacement, distribution complémentaire, rejet motivé ?
14. Le suivi public d'un ticket sans connexion (`/suivi`) est-il réaliste ? Quels risques de confidentialité ? Quelles informations minimales faut-il demander pour éviter qu'un tiers consulte le dossier d'un agriculteur ?
15. Les notifications par email sont-elles réalistes pour les agriculteurs burundais ? Le SMS ou l'appel téléphonique serait-il plus pertinent ? Quelle proportion d'agriculteurs dispose d'un email fiable ?
16. Comment fonctionne une distribution partielle (`PARTIEL`) ? Qui décide de servir moins que la quantité commandée ? Comment le reliquat est-il suivi ?
17. Comment un ticket expire-t-il (`EXPIRE`) ? Après combien de temps ? Qui le clôture ?
18. Comment un ticket est-il annulé (`ANNULE`) ? Qui peut l'annuler et pour quel motif ?
19. Le retrait doit-il se faire obligatoirement au dépôt de zone ou peut-il se faire dans un autre dépôt ? Comment gérer le transfert entre dépôts ?
20. Quels reçus, bons de livraison ou signatures sont utilisés sur le terrain ?

## MISSION 5 — VÉRIFIER LES DONNÉES DE DÉMONSTRATION, LES NOMS ET LA SÉCURITÉ

1. Les 500 agriculteurs `Nom1 Prenom1` à `Nom500 Prenom500` doivent être remplacés. Propose au moins 30 noms burundais fictifs mais réalistes, équilibrés entre hommes et femmes, avec nom et prénom.
2. Explique les conventions de nommage au Burundi : noms kirundi, prénoms français/chrétiens, ordre nom/prénom, particules éventuelles. Évite les noms qui seraient offensants ou invraisemblables.
3. Propose une stratégie SQL PostgreSQL pour remplacer les 500 noms sans casser les contraintes d'unicité, les tickets existants et les références. Donne un exemple de requête ou de script de migration.
4. Est-il légal et éthique d'utiliser des noms de personnes réelles dans une démonstration ? Recommande explicitement des noms fictifs et explique pourquoi.
5. Les comptes de démonstration (`admin`, etc.) ne doivent jamais être affichés sur l'écran de connexion. Confirme les bonnes pratiques : pas d'identifiants en clair, pas de placeholder révélant un compte, pas de mot de passe dans le code frontend, révocation des secrets exposés.
6. Le bouton « X » en haut à gauche, à côté de « FOMI Stock / Gestion des engrais », est un bouton de fermeture du menu latéral sur mobile (`sidebar-close`). Est-ce une bonne UX ? Faut-il le garder, le masquer sur desktop, ajouter une infobulle, ou le remplacer ?
7. Comment séparer proprement les données de démonstration des données de production : profil Spring `demo`, préfixe `DEMO-`, script de nettoyage, base séparée, feature flag ?
8. Quelles données personnelles l'application collecte-t-elle : nom, prénom, téléphone, email, numéro d'identité, colline, coopérative ? Quelles sont les obligations légales au Burundi en matière de protection des données personnelles ? Cite la loi applicable et l'autorité de contrôle.
9. Quelles sont les bonnes pratiques de sécurité pour une application publique : mots de passe, JWT, rôles, journal d'audit, limitation des tentatives, chiffrement, sauvegardes, secrets hors du dépôt Git ?
10. Quels risques si l'application est hébergée localement avec des coupures d'électricité et un réseau instable ? Faut-il un mode hors ligne, une synchronisation différée, un serveur local ?

## MISSION 6 — UX, ONBOARDING ET UTILISABILITÉ POUR UN NOUVEL UTILISATEUR

1. Un nouvel agent FOMI doit pouvoir comprendre l'application en moins de 10 minutes. Propose un parcours d'accueil adapté à chaque rôle.
2. Propose un glossaire intégré (infobulles ou page d'aide) pour : dépôt provincial, dépôt de zone, commune, zone, colline, seuil, stock disponible, état Rupture/Bas/OK, ticket, validation, rejet, réclamation, distribution partielle, lot, mouvement.
3. Comment expliquer simplement le tableau `Engrais | Disponible | Seuil | État` à un utilisateur non technique ?
4. Comment expliquer la différence entre le « niveau » d'un dépôt (`PROVINCE` / `ZONE`) et les niveaux administratifs (province, commune, zone, colline) ?
5. Où et comment ajouter les 18 provinces proprement : écran d'administration du référentiel, import CSV officiel, migration SQL, ou les deux ? Pourquoi ne faut-il pas laisser l'utilisateur saisir librement des noms de provinces ?
6. Propose des états vides utiles, des messages d'erreur clairs, des confirmations avant suppression, et des libellés en français simple.
7. Faut-il ajouter le kirundi ? Quelles parties de l'interface traduire en priorité ? Comment gérer les deux langues ?
8. Propose des améliorations pour mobile, faible bande passante, petits écrans, contraste, taille de police et accessibilité.
9. Le mode sombre est-il utile pour ce public ? Quels contrastes vérifier ?
10. Comment signaler clairement que les données affichées sont des données de démonstration et non des données réelles ?
11. Propose une aide contextuelle de première connexion : visite guidée, encart « Commencer ici », checklist, ou vidéo courte.
12. Comment former les agents sans documentation lourde : fiches d'une page, tutoriels, aide intégrée, personas ?

## MISSION 7 — ALLER AU-DELÀ DES QUESTIONS POSÉES

Réponds aussi aux questions que je n'ai pas posées mais qui comptent pour la crédibilité de l'application :

1. Le modèle de données est-il complet ? Manque-t-il des entités : fournisseur/importateur, bon de commande, réception, contrôle qualité, inventaire physique, ajustement, retour, perte, transfert, quota, subvention, reçu, coopérative, carte d'agriculteur, saison, culture, parcelle ?
2. Le suivi des lots et des dates de péremption est-il réaliste pour la FOMI ? Faut-il du FIFO/FEFO ?
3. Les mouvements de stock couvrent-ils tous les cas : entrée, transfert province → zone, distribution, retour, perte, ajustement, annulation ?
4. Les alertes sont-elles pertinentes : rupture, seuil bas, stock excédentaire, lot proche de la péremption, ticket non servi, réclamation en attente ?
5. Les indicateurs du tableau de bord sont-ils ceux qui intéressent vraiment la FOMI : stock par province, taux de service, délai de distribution, taux de réclamation, couverture des besoins, taux de perte ?
6. Le journal d'audit est-il nécessaire ? Quelles actions tracer ? Combien de temps conserver ?
7. L'export CSV est-il suffisant, ou faut-il des états PDF officiels, des bons de livraison imprimables, des reçus ?
8. Quelles sont les contraintes d'impression et de signature sur le terrain ?
9. Quelles integrations sont réalistes : SMS, mobile money, registre national des agriculteurs, système du Ministère, ERP de la FOMI ?
10. Quels sont les risques de fraude et comment les limiter : faux tickets, doublons, quotas détournés, agents corrompus, stocks fictifs ?
11. Quelles sont les exigences de sauvegarde, de restauration et de continuité de service ?
12. Quelle gouvernance des données : qui administre les provinces/communes/zones/collines, qui corrige une colline mal orthographiée, qui valide un nouveau dépôt ?
13. Quelles sont les erreurs les plus probables dans les données de démonstration actuelles, et comment les corriger sans casser l'application ?
14. Quelles fonctionnalités sont surdimensionnées pour un projet de stage et devraient être simplifiées ou retirées ?
15. Quelles fonctionnalités manquent absolument pour que la démonstration soit crédible devant un jury et devant la FOMI ?
16. Peut-on montrer l'application telle quelle à la FOMI ? Donne un verdict go / no-go et la liste des corrections indispensables avant la démonstration.
17. Quelles questions faut-il poser directement à la FOMI pour combler les informations non publiques ? Rédige une fiche d'entretien de 15 questions maximum.
18. Quels documents officiels faut-il demander : organigramme, liste des dépôts, procédures de distribution, formulaire de réclamation, grille de prix, calendrier des saisons, liste des communes/zones/collines ?
19. Quelles sources sont les plus fiables et lesquelles sont à éviter (blogs, sites d'actualité non vérifiés, Wikipédia seule) ?
20. Quelles informations sont datées et doivent être revalidées chaque saison (prix, seuils, quotas, liste des dépôts) ?

## LIVRABLES ATTENDUS

Produis un rapport structuré avec les sections suivantes :

### A. Résumé exécutif
10 lignes maximum : ce qui est vrai, ce qui est faux, ce qui manque, et les 5 corrections prioritaires.

### B. Tableau de vérification
Colonnes : Élément | Valeur actuelle | Réalité vérifiée | Verdict (✅/⚠️/❌/❓) | Source | Correction proposée.
Couvre au minimum : les 3 provinces, les 5 communes, les 4 zones, les 6 collines, les 9 dépôts, les 3 engrais, les prix, les seuils, les unités, les 10 statuts, les rôles, les tickets de démonstration.

### C. Référentiel officiel corrigé
- Liste des 18 provinces avec codes.
- Nombre officiel de communes.
- Pour Gitega, Bubanza et Ngozi : communes, zones et collines réellement attestées.
- Format CSV ou SQL PostgreSQL prêt à intégrer, avec les sources.
- Si une information n'est pas disponible, écrire `NON TROUVÉ` et ne pas inventer.

### D. Réponses aux 10 questions de l'utilisateur
Réponds une par une, dans l'ordre :
1. Identifiants affichés sur le login.
2. Bouton X à côté de « FOMI Stock / Gestion des engrais ».
3. Noms `Nom1 Prenom1` et noms réels.
4. Réalité de l'écran `/#/depots`.
5. Signification de niveau, province, commune, zone, et du tableau `Engrais | Disponible | Seuil | État`.
6. Où ajouter toutes les provinces.
7. Comment rendre l'application utilisable par un nouvel utilisateur.
8. Où se font les réclamations (cas `TKT-2026-1250`).
9. Fonctionnement de `TKT-MAIL-DEMO-1` et des boutons Détails / Modifier / Activer / Rejeter.
10. Qui peut rejeter et si le rejet est justifié (cas `TKT-E2E-REJ`).

### E. Workflow ticket recommandé
Machine à états simple, réaliste, avec les acteurs, les conditions de transition, les délais et les motifs de rejet.

### F. Procédure de réclamation recommandée
Canal, informations à fournir, étapes, délais, acteurs, issues possibles, traçabilité.

### G. Modèle de données et corrections techniques
Entités manquantes, champs à corriger, contraintes, unités, seuils, séparation démo/production, migrations SQL.

### H. Données de démonstration
- 30 noms burundais fictifs réalistes.
- Stratégie de remplacement des 500 noms.
- Exemple de requête SQL.
- Règles pour ne plus jamais afficher d'identifiants sur le login.
- Nettoyage des tickets de test.

### I. UX et onboarding
10 recommandations concrètes, classées P0/P1/P2, avec une maquette textuelle ou une description des écrans.

### J. Sécurité, droit et éthique
Protection des données, consentement, comptes de démonstration, secrets, journal d'audit, risques.

### K. Plan de correction
Tableau : Priorité | Problème | Correction | Fichier/écran concerné | Effort | Responsable.

### L. Contacts et sources
- Contacts officiels FOMI / Ministère.
- Liste des sources [S1]…[Sn] avec URL, date de publication, date de consultation, fiabilité.
- Questions restantes à faire confirmer par la FOMI.

## FORMAT DE RÉPONSE

- Français clair, phrases courtes.
- Tableaux Markdown.
- Distinguer visuellement ✅, ⚠️, ❌, ❓.
- Mettre les citations de sources entre crochets [S1].
- Ne pas dépasser 6 000 mots, mais ne pas sacrifier les faits essentiels.
- Terminer par : « Ce que je n'ai pas pu vérifier » et « Les 5 questions à poser à la FOMI ».

## RAPPEL FINAL

Je préfère une réponse honnête avec des `NON TROUVÉ` plutôt qu'une réponse inventée. Si tu dois choisir entre faire plaisir et dire la vérité, dis la vérité et explique comment obtenir l'information.
