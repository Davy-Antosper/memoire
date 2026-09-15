# Le grand livre d'ITAS
## Mon tout premier guide pour comprendre le projet `itas-gestion-utilisateur-service`

---

# Chapitre 1 — Bonjour ! À quoi sert ce livre ?

Tu viens d'arriver dans une grande équipe. Quelqu'un t'a montré un projet
informatique avec plein de fichiers, de mots bizarres comme « Keycloak »,
« Kafka », « microservice », « JWT »… et tu t'es peut-être senti un peu perdu.
Pas de panique ! Ce livre est fait pour toi.

**Ce livre te raconte une histoire.** L'histoire d'un bâtiment très spécial
qu'on appelle **ITAS**. Dans ce bâtiment, des gens travaillent tous les jours
pour une chose très importante : s'occuper des **impôts**. Oui, les impôts —
ceux qui paient pour les routes, les écoles, les hôpitaux.

Dans ce livre, je vais t'expliquer comment ce bâtiment fonctionne, **comme si
tu avais 7 ans**. Je vais utiliser des images simples :

- l'administration des impôts est une **grande usine** ;
- les ordinateurs qui s'envoient des messages sont des **facteurs** ;
- la carte qui prouve ton identité est un **badge** ;
- et le projet qu'on te donne est **un des ateliers de l'usine**.

À la fin de ce livre, tu sauras répondre à ces questions :

1.  Qu'est-ce que fait notre projet, en une phrase ?
2.  Qui sont les « robots » qui l'aident (Keycloak, Kafka, PostgreSQL) ?
3.  Comment une demande de papiers voyage de A à Z ?
4.  Pourquoi on parle tout le temps de « dossiers » et de « circulation » ?

Pas besoin d'être un génie. Il suffit de lire doucement, **un chapitre à la
fois**, comme une histoire.

```
      LE PLAN DE NOTRE AVENTURE
  ┌──────────────────────────────────────┐
  │  1.  Bonjour ! (tu es ici)           │
  │  2.  La grande usine ITAS            │
  │  3.  Notre atelier                   │
  │  4.  Les 4 briques magiques          │
  │  5.  Le badge magique                │
  │  ... jusqu'au chapitre 19 !          │
  │  PARTIE 7 : la visite des fichiers   │
  │  PARTIE 8 : les erreurs              │
  │  PARTIE 9 : démarrer le projet       │
  │  PARTIE 10 : plus profond            │
  │  PARTIE 11 : la FAQ                  │
  │  PARTIE 12 : le quiz (44 chap.)      │
  │  et le dictionnaire à la fin !       │
  └──────────────────────────────────────┘
```

*Mot compliqué du jour :* **projet informatique** = une boîte pleine de
fichiers que des personnes construisent ensemble pour faire fonctionner un
logiciel.

Allez, c'est parti ! Tourne la page.

# Chapitre 2 — La grande usine ITAS

Imagine un très grand bâtiment. Dedans, plein d'ateliers. Un atelier s'occupe
des **déclarations** (quand un citoyen annonce combien il gagne ou combien il
vend). Un autre atelier s'occupe des **paiements** (quand le citoyen donne
l'argent qu'il doit). Un autre encore s'occupe des **recensements** (qui est
qui, dans le pays).

Ce grand bâtiment, c'est **l'administration fiscale**. Et son nom informatisé,
c'est **ITAS** : le système qui aide tous les ateliers à travailler ensemble,
sans se marcher sur les pieds.

**Mais attention !** Le bâtiment est tellement grand que **un seul ordinateur
géant** serait trop fragile. S'il tombe en panne, tout s'arrête ! Alors les
ingénieurs ont décidé de découper le travail en **petits programmes
indépendants**. Chaque petit programme s'occupe d'une seule chose, vit dans sa
propre petite maison, et peut tomber en panne sans casser les autres.

Chaque petit programme s'appelle un **microservice**. Le mot « micro » veut
dire « tout petit ». Le mot « service » veut dire « un programme qui rend
service ».

```
            LA GRANDE USINE ITAS
    (plusieurs petits programmes, chacun dans sa maison)

  ┌──────────┐   ┌──────────┐   ┌──────────┐
  │ Atelier  │   │ Atelier  │   │ Atelier  │
  │ Paiements│   │Déclarations│ │Immatricu.│
  │ (9002)   │   │  (9004)  │   │   (?)    │
  └──────────┘   └──────────┘   └──────────┘
       └────────────┬─────────────┘
                    │  ils se parlent !
                    ▼
  ┌────────────────────────────────────────┐
  │     Notre atelier :                    │
  │  itas-gestion-utilisateur-service      │
  │  (port 9000)                           │
  └────────────────────────────────────────┘
```

Chaque atelier a un **numéro de porte** : le port. Notre atelier, par exemple,
a la porte numéro **9000**. Quand quelqu'un veut parler à notre atelier, il
frappe à la porte 9000.

*Mot compliqué du jour :* **microservice** = un tout petit programme qui fait
un travail précis et vit dans sa propre maison (sa propre « boîte »).

Maintenant qu'on sait que notre projet est **un atelier de l'usine ITAS**,
allons voir ce que notre atelier fabrique exactement.

# Chapitre 3 — Notre atelier : `itas-gestion-utilisateur-service`

Notre projet s'appelle **`itas-gestion-utilisateur-service`**. Le nom nous dit
déjà beaucoup : c'est le service qui **gère les utilisateurs**. Mais c'est
encore plus riche que ça. Notre atelier fait **quatre métiers**.

**Métier n°1 — Le bureau des badges (les comptes).**
Quand un agent de l'administration ou un contribuable veut entrer dans le
système, il faut lui créer un compte : un nom d'utilisateur, un mot de passe,
des droits. Notre atelier est chargé de créer ces comptes.

**Métier n°2 — Le bureau des équipes (l'organisation).**
L'administration fiscale est organisée en **structures** (des services, des
directions), avec des **fonctionnaires** (les gens) et des **postes** (le
travail qu'ils font). Notre atelier gère tout ça : qui travaille où, et avec
quel titre.

**Métier n°3 — Le bureau des dossiers (le travail qui circule).**
Quand un citoyen demande quelque chose (par exemple : « je veux mon numéro
d'immatriculation fiscale »), on crée un **dossier**. Ce dossier doit passer
de service en service, monter et descendre les étages, comme une feuille de
papier dans une administration. Notre atelier suit ce dossier partout.

**Métier n°4 — Le bureau des copies (les informations des autres).**
Les autres ateliers de l'usine produisent des informations (les contribuables,
les paiements, les déclarations). Notre atelier n'invente pas ces
informations : il en fait une **copie** chez lui, pour pouvoir les utiliser
quand il en a besoin.

```
         LES 4 MÉTIERS DE NOTRE ATELIER

  ┌──────────┬──────────┬──────────┬──────────┐
  │  1.      │  2.      │  3.      │  4.      │
  │ Comptes │ Equipes  │ Dossiers │  Copies  │
  │(badges) │(structures)│(circule)│ (Kafka)  │
  └──────────┴──────────┴──────────┴──────────┘
```

Quand on regarde le projet, on voit qu'il est rangé comme une armoire avec des
tiroirs. Chaque tiroir s'appelle une **feature** (une fonctionnalité). Il y a
un tiroir « contribuable », un tiroir « dossier », un tiroir « circulation »,
un tiroir « fonctionnaire », et ainsi de suite.

*Mot compliqué du jour :* **feature** = un tiroir du projet qui regroupe tout
ce qui sert à faire UNE fonctionnalité précise.

Mais notre atelier ne travaille pas tout seul. Il a besoin de quatre robots
magiques. C'est le sujet du prochain chapitre.

# Chapitre 4 — Les quatre briques magiques

Pour travailler, notre atelier utilise **quatre assistants** très importants.
Apprenons à les connaître : ils reviennent tout le temps dans ce livre.

**1. Le Chef du personnel — Keycloak.**
Keycloak est le robot qui garde **toutes les cartes d'identité** des gens qui
utilisent le système. Il sait qui est qui, qui a le droit de faire quoi. Il
habite dans sa propre maison (à l'adresse `192.168.20.14:8089`).

**2. Le Gardien de l'entrée — Spring Security.**
Quand quelqu'un frappe à la porte de notre atelier, Spring Security est le
gardien qui vérifie son badge avant de le laisser entrer. « C'est bon, cette
personne a le droit de passer ! » ou « Halte ! Badge invalide ! »

**3. L'Entrepôt — PostgreSQL.**
PostgreSQL est le grand **entrepôt à souvenirs** de notre atelier. Toutes les
informations sont rangées là : les dossiers, les contribuables, les
fonctionnaires. Quand on veut se souvenir de quelque chose, on va à
l'entrepôt. Le mot savant pour l'entrepôt, c'est **base de données**.

**4. Le Facteur — Kafka.**
Kafka est le **facteur de l'usine**. Il transporte les messages entre les
ateliers. Notre atelier reçoit des lettres des autres ateliers (Kafka le
facteur les dépose) et il en envoie aussi. Le nom savant des lettres, c'est
des **messages** ou des **événements**.

```
      LES 4 ROBOTS DE NOTRE ATELIER

  Keycloak        Spring Security      PostgreSQL          Kafka
  Chef du         Gardien de           Entrepôt à          Facteur
  personnel       l'entrée             souvenirs           de l'usine
  (qui est qui)   (badge valable ?)    (on y range tout)   (porte les lettres)
```

*Mot compliqué du jour :* **base de données** = un gros classeur informatisé
où le programme range ses informations pour ne pas les oublier.

Chacun de ces quatre robots a son propre chapitre un peu plus loin. On
commence par le plus amusant : le **badge magique**.

# Chapitre 5 — Le badge magique (le JWT)

Dans une grande administration, comment prouves-tu que tu as le droit
d'entrer ? Avec un **badge**, une petite carte avec ta photo et tes
permissions. Eh bien, en informatique, c'est pareil ! Mais le badge est
invisible : c'est une **longue suite de caractères** qu'on appelle un **JWT**
(se prononce « jé-wé-ti »).

**Comment on obtient son badge ?**
Le gardien (Keycloak) est le seul qui peut fabriquer des badges. Pour en avoir
un, on se connecte avec son nom d'utilisateur et son mot de passe. Keycloak
vérifie, puis dit : « Oui, c'est bien toi. Voici ton badge ! » Et il fabrique
le JWT.

```
  Je donne mon nom
  et mon mot de passe
        │
        ▼
  ┌────────────┐      ┌───────────────────────────┐
  │  Keycloak  │─────►│  Le badge (JWT) :          │
  │  (chef du  │      │  un long texte avec        │
  │  personnel)│      │  mon nom, mes rôles,       │
  └────────────┘      │  la date d'expiration      │
                      └───────────────────────────┘
```

**Le badge contient trois secrets importants :**
- **Qui je suis** : mon nom d'utilisateur (le « preferred_username »).
- **Ce que j'ai le droit de faire** : mes rôles (par exemple « je peux créer
  des utilisateurs »).
- **Jusqu'à quand il est valable** : la date d'expiration. Quand le badge est
  périmé, il ne marche plus.

**Le badge a une super-pouvoir : il ne peut pas être copié-faussé.**
Le badge est signé par Keycloak, comme un document signé à la main. Personne
ne peut fabriquer un faux badge, car personne d'autre ne connaît la signature
secrète de Keycloak. Le mot savant pour « signature », c'est **signature
numérique**.

*Mot compliqué du jour :* **JWT** = le badge numérique que Keycloak donne à
une personne connectée. À chaque visite, la personne montre son badge.

Mais attention : avoir un badge, ce n'est que la moitié du travail. Il faut
aussi que **le gardien de l'entrée** le vérifie. C'est l'histoire du prochain
chapitre.

# Chapitre 6 — Le gardien de l'entrée (Spring Security)

Imaginons que tu arrives à la porte de notre atelier. Tu montres ton badge
JWT. Qui vérifie que ton badge est bon ? **Spring Security**, le gardien.

**Le gardien fait trois vérifications :**

1. **« Le badge est-il authentique ? »** Il regarde la signature. Si la
   signature n'est pas celle de Keycloak, le badge est faux → refusé.
2. **« Le badge est-il encore valable ? »** Il regarde la date d'expiration.
   Si elle est dépassée → refusé.
3. **« Le badge vient-il de chez nous ? »** Il vérifie que le badge a bien été
   fabriqué par NOTRE Keycloak (celui du royaume `itas`).

Si tout est bon, le gardien laisse entrer. Sinon, il répond gentiment :
« Non, désolé, tu ne peux pas passer » (le mot savant : une erreur **401** ou
**403**).

```
      UNE VISITE À NOTRE ATELIER

  Visiteur : « Voici mon badge ! »   (JWT)
      │
      ▼
  ┌──────────────────────────────┐
  │  LE GARDIEN (Spring Security)│
  │ 1. signature authentique ?   │
  │ 2. pas expiré ?              │
  │ 3. vient de notre Keycloak ? │
  └──────────────────────────────┘
      │
      ├── Oui ──► « Entre, tu as le droit ! » ➜ les services
      │
      └── Non ──► « Halte ! » ➜ erreur 401/403
```

**Mais le gardien fait encore mieux.** Le badge contient mes **rôles** (mes
permissions). Le gardien les lit et les donne au reste de l'atelier. Le robot
qui lit le badge et en sort les rôles s'appelle **JwtAuthConverter**. C'est
comme un petit décodeur qui traduit le badge en une liste de droits
compréhensibles.

Par exemple, le badge dit : « Ce monsieur a le rôle *creer-utilisateur* ».
Le décodeur le traduit en : « Ce monsieur PEUT créer des utilisateurs. »

*Mot compliqué du jour :* **authentification** = prouver qui tu es avec ton
badge. **Autorisation** = savoir ce que tu as le droit de faire avec tes rôles.

Il y a une petite exception amusante : certaines portes de l'atelier n'ont pas
de gardien. Par exemple, la porte du menu « swagger » (le catalogue des
services) et la porte de connexion (`/authentication`). Tout le monde peut y
passer sans badge.

Maintenant, allons saluer le **chef du personnel** : Keycloak, le fabricant de
badges.

# Chapitre 7 — Le chef du personnel (Keycloak)

Keycloak est LE robot le plus important de l'usine pour la sécurité. C'est lui
qui **fabrique les badges** et qui **garde la liste de toutes les personnes**
qui ont le droit de travailler avec ITAS.

**Keycloak a trois grandes missions :**

**Mission 1 — Faire les badges (les tokens).**
Quand quelqu'un se connecte, Keycloak vérifie son mot de passe et fabrique son
badge (le JWT). Notre atelier ne vérifie JAMAIS les mots de passe : il laisse
Keycloak faire, comme on laisse le chef du personnel vérifier les cartes
d'identité.

**Mission 2 — Garder les comptes des personnes.**
Quand on veut donner un compte à un nouvel agent, c'est notre atelier qui
demande à Keycloak de le créer. Notre atelier utilise un robot-messager
spécial qui parle à Keycloak : la **Keycloak Admin Client**. Grâce à lui,
notre atelier peut dire : « Crée un compte pour monsieur Dupont », « Ajoute-le
au groupe des Directeurs », « Donne-lui le rôle *creer-utilisateur* ».

**Mission 3 — Gérer les groupes et les rôles.**
Dans l'usine, il y a des **groupes** (des équipes) et des **rôles** (des
droits). Petite règle amusante de notre projet : **un poste = un groupe**.
Si on crée un poste appelé « 12 - Directeur », on crée en même temps un groupe
Keycloak du même nom. Les gens du groupe ont les droits du poste.

**Les rôles sont créés tout seuls au démarrage !**
Quand notre atelier s'allume, il demande à Keycloak : « Est-ce que les rôles
*creer-utilisateur*, *modifier-utilisateur*, etc. existent ? » S'ils
n'existent pas, il les crée. On appelle ça **initialiser les rôles**.

```
        LE CHEF DU PERSONNEL (Keycloak)

  Notre atelier ──► « Crée un compte ! » ──► Keycloak
        │                                       │
        │                                       ▼
        │                            crée l'utilisateur + le groupe + les rôles
        │
        └──► envoie un email de bienvenue au nouvel agent
```

*Mot compliqué du jour :* **rôle** = un droit donné à une personne (par
exemple « peut créer un utilisateur »). Les rôles vivent dans Keycloak.

Et pour envoyer les emails de bienvenue ? Notre atelier utilise un autre robot
messager, le **serveur SMTP** (le service qui envoie les emails). On le verra
dans le glossaire, à la fin du livre.

# Chapitre 8 — Le facteur Kafka et les boîtes aux lettres (topics)

Les ateliers de l'usine ne se téléphonent pas directement. Pourquoi ? Parce
que si l'atelier des paiements est occupé, il ne voudrait pas rater
l'information. Alors ils utilisent un facteur très fiable : **Kafka**.

**Kafka transporte des lettres entre les ateliers.** Chaque lettre est un
**message**. Et les messages sont déposés dans des **boîtes aux lettres**
qu'on appelle des **topics**.

```
   Atelier A (le facteur Kafka)         Atelier B
      │  dépose une lettre                 │
      ▼                                   │
  ┌──────────────────┐                    │
  │  BOÎTE AUX       │  ──► Kafka lit ──► │
  │  LETTRES         │    la lettre       │
  │  (le topic)      │    et la donne     │
  └──────────────────┘    à Atelier B     │
                                          
```

**Le topic a un nom qui explique son contenu.** Par exemple, le topic
`personne-physique-events` contient des lettres qui parlent des personnes
physiques. C'est comme une boîte aux lettres marquée « courrier des personnes
physiques ».

**Deux mots importants :**
- **Producer** = celui qui ÉCRIT les lettres dans la boîte. (Un producteur
  écrit, comme on écrit une lettre.)
- **Consumer** = celui qui LIT les lettres. (Un consommateur lit, comme on
  lit son courrier.)

Notre atelier est **les deux à la fois** :
- Il est **consumer** : il lit les lettres des autres ateliers (contribuables,
  déclarations, paiements…).
- Il est **producer** : il écrit des lettres pour les autres (quand un dossier
  circule, quand un fonctionnaire change…).

**Pourquoi c'est génial ?** Parce que l'atelier qui envoie la lettre n'a pas
besoin d'attendre que l'autre soit prêt. Il dépose sa lettre dans la boîte et
il continue son travail. Kafka garde la lettre jusqu'à ce que quelqu'un vienne
la lire. C'est ce qu'on appelle des systèmes **asynchrones** (ils ne se
bloquent pas les uns les autres).

*Mot compliqué du jour :* **topic** = une boîte aux lettres Kafka, avec un
nom, qui contient des messages du même sujet.

Dans le prochain chapitre, on va visiter toutes les boîtes aux lettres de
notre atelier !

# Chapitre 9 — Les boîtes aux lettres du projet

Notre atelier a plusieurs boîtes aux lettres. Certaines, il les LIT
(consumer). D'autres, il les REMPLIT (producer). Faisons la visite.

**Les boîtes que notre atelier LIT (les topics des autres ateliers) :**

| Boîte aux lettres (topic) | Que contient-elle ? |
|---|---|
| `personne-physique-events` | Une personne physique s'est inscrite (immatriculation) |
| `personne-morale-events` | Une société s'est inscrite |
| `contribuable-events` | Un contribuable a reçu son NIF |
| `declaration-events` | Un contribuable a déclaré ses impôts |
| `paiement-events` | Un contribuable a payé |
| `exercice-fiscal-events` | L'année fiscale a changé |
| `secteur-activite-events` | La liste des métiers a changé |
| `region-fiscal-events` | La liste des régions fiscales a changé |

**La boîte que notre atelier REMPLIT (qu'il écrit) :**

| Boîte aux lettres (topic) | Ce que notre atelier y dépose |
|---|---|
| `dossier-events` | « Le dossier n°X est monté d'un étage ! » |
| `fonctionnaire-events` | « Un fonctionnaire a été créé/modifié/supprimé » |
| `structure-administrative-events` | « Une structure a changé » |

```
      LES BOÎTES AUX LETTRES DE L'ATELIER

   Lues par nous :          Écrites par nous :
   personne-physique        dossier-events
   personne-morale          fonctionnaire-events
   contribuable             structure-administrative-events
   declaration
   paiement
   exercice-fiscal
   secteur-activite
   region-fiscal
```

**Que fait notre atelier quand il reçoit une lettre ?** Il la lit, il
comprend ce qui s'est passé, et il **range une copie dans son entrepôt** ou il
**crée un dossier de travail**. Par exemple :

- Une lettre `personne-physique-events` → notre atelier crée un **dossier
  d'immatriculation** et le pose sur le bureau de la structure la moins
  chargée.
- Une lettre `declaration-events` → il garde une copie de la déclaration et
  calcule les pénalités.

Ces boîtes aux lettres sont déclarées dans le fichier `application.yml` de
notre projet. C'est là qu'on écrit le nom de la boîte et le nom du « groupe »
de lecture. Le **groupe** sert à éviter que deux copies du même atelier lisent
la même lettre : dans un groupe, chaque lettre n'est lue qu'UNE fois.

*Mot compliqué du jour :* **consommer** = lire une lettre dans une boîte
Kafka. **Publier** = déposer une lettre dans une boîte Kafka.

Viens, maintenant on monte dans la grande pyramide : les structures de
l'administration.

# Chapitre 10 — La grande pyramide (les structures)

L'administration fiscale est organisée comme une **pyramide**. En haut, il y
a une grande direction. En dessous, des directions moyennes. Encore en
dessous, des centres, puis des services, puis des sous-services.

Chaque étage de la pyramide s'appelle un **niveau**. Dans notre projet, la
pyramide a **dix niveaux** possibles : du niveau 1 jusqu'au niveau 10. Chaque
petit bureau de la pyramide s'appelle une **structure administrative**.

```
        LA GRANDE PYRAMIDE (10 niveaux)

              ▲ Niveau 1  (le sommet)
             / \
            /   \        un bureau = une "structure
           /_____\        administrative"
          /       \
         /  Niveau \
        /    3      \     ← les services qui suivent
       /_____________\      les contribuables
      /               \
     /   Niveau 10     \   (le rez-de-chaussée)
    /___________________\
```

**Deux mots très pratiques :**

- **N+1** = le bureau **juste au-dessus** de moi. C'est mon « parent ».
  Si je suis au niveau 3, mon N+1 est le bureau de niveau 2 directement
  au-dessus.
- **N-1** = un bureau **juste en dessous** de moi. C'est mon « enfant ».

C'est comme un immeuble : si tu es au 3e étage, « monter au niveau
supérieur » veut dire aller au 4e étage (non, attends !). Attention au sens :
dans l'usine, le **niveau 1 est le sommet**. Donc « le niveau supérieur »
d'une structure = un numéro **plus petit** (on monte vers le 1). Le
« niveau inférieur » = un numéro plus grand (on descend vers le 10).

```
  Niveau 2   ←  N+1 (le parent, juste au-dessus)
  Niveau 3   ←  moi, ici !
  Niveau 4   ←  N-1 (un enfant, juste en dessous)
```

**Une règle spéciale :** seuls les bureaux du **niveau 3** peuvent « suivre
les contribuables ». C'est comme une école où seuls les maîtres de CE2 peuvent
s'occuper des élèves : c'est écrit dans les règles !

Chaque structure a un **code** unique (comme un numéro de badge) et un
**sigle** (des lettres courtes). Et on ne peut pas supprimer une structure qui
a encore des enfants en dessous : il faut d'abord déplacer les enfants.

*Mot compliqué du jour :* **structure administrative** = un bureau de la
pyramide, avec un niveau, un code, et peut-être un parent.

Mais une pyramide sans personnes, ça ne sert à rien ! Parlons des gens qui y
travaillent.

# Chapitre 11 — Les personnes de l'usine (fonctionnaires, postes, affectations)

Une administration, ce sont des gens. Dans notre projet, les gens qui
travaillent s'appellent des **fonctionnaires**. Chaque fonctionnaire a un
**matricule** (son numéro personnel, unique comme son badge) et un nom.

Mais un fonctionnaire ne peut pas être partout à la fois. Il faut savoir :
**qui travaille où, et à quel poste ?** C'est le travail de trois petites
choses :

**1. Le fonctionnaire — la personne.**
Monsieur Dupont, matricule 1234.

**2. Le poste — le travail.**
Le poste, c'est le métier : « Directeur », « Vérificateur », « Agent de
bureau ». Chaque poste a un code (des chiffres) et une description. Petite
règle amusante déjà vue : **un poste = un groupe Keycloak**. Et un poste a une
date de début et une date de fin (le poste peut « expirer »).

**3. L'affectation — le lien entre la personne et le bureau.**
L'affectation, c'est la réponse à la question : « Monsieur Dupont travaille
dans quelle structure, à quel poste, depuis quand ? »

```
  Fonctionnaire ────► Affectation ◄──── Poste
  (qui)                  │              (quoi)
                         ▼
                 Structure administrative
                 (où)
```

**Une règle très importante :** un fonctionnaire ne peut avoir qu'**UNE seule
affectation active** à la fois. S'il change de bureau, on met une date de fin
à l'ancienne affectation, et on crée la nouvelle. On ne supprime pas
l'ancienne : on la ferme proprement.

**Et le lien avec les comptes ?** Quand on crée le compte Keycloak d'un
fonctionnaire, on rattache ce compte à son **affectation**. Ainsi, quand le
fonctionnaire se connecte, le système sait immédiatement dans quelle structure
il travaille. C'est grâce à ça qu'un agent ne voit que les dossiers de SON
bureau !

*Mot compliqué du jour :* **affectation** = le lien qui dit qu'une personne
travaille dans une structure à un poste donné, pendant une période.

Maintenant qu'on connaît les personnes et les bureaux, parlons du vrai héros
de notre histoire : le **dossier** et son voyage dans la pyramide.

# Chapitre 12 — Les dossiers et leur voyage

Un citoyen demande quelque chose : « Je veux être immatriculé », « Je conteste
une décision ». L'administration transforme cette demande en **dossier** : une
petite fiche avec une **référence** (son numéro, unique), un **type** (de quel
genre de demande il s'agit), une date de création.

Mais la vraie question, c'est : **OÙ est le dossier en ce moment ?** Dans quel
bureau ? À qui doit-il passer ?

**La grande idée du projet :** le dossier lui-même ne dit pas où il est.
C'est une autre petite fiche qui le dit : la **ligne de circulation**.

À chaque bureau qu'il visite, on crée une ligne de circulation avec :
- le bureau visité (la structure) ;
- la date d'arrivée (**dateDebut**) ;
- la date de départ (**dateFin**) ;
- un petit commentaire.

**Tant que le dossier est dans un bureau, sa ligne n'a PAS de date de
départ.** Dès qu'il quitte le bureau, on écrit la date de départ. La ligne
**active** (sans date de fin) est donc celle qui montre **où le dossier est
maintenant**. C'est simple et malin : pas besoin de stocker la position, on la
déduit.

```
      LE VOYAGE D'UN DOSSIER

  Bureau A   ──► ligne 1 : arrivée le 1er, départ le 3
  Bureau B   ──► ligne 2 : arrivée le 3, départ le 5   ← c'est fait
  Bureau C   ──► ligne 3 : arrivée le 5, PAS de départ ← LE DOSSIER EST ICI !
```

**À l'arrivée dans un bureau, on « affecte » le dossier aux fonctionnaires**
de ce bureau. Les fonctionnaires voient le dossier dans leur liste de travail,
ils le traitent, puis le dossier monte ou descend.

**Les types de dossiers possibles** (dans notre projet) sont :
- Demande d'immatriculation d'un contribuable ;
- Demande d'immatriculation d'un engin (un véhicule, une machine) ;
- Recours d'un contribuable.

*Mot compliqué du jour :* **circulation** = le voyage du dossier de bureau en
bureau. **Ligne active** = la fiche qui montre où il est en ce moment.

Voyons maintenant comment le dossier **monte d'un étage** (on dit : on le
transfère au niveau supérieur).

# Chapitre 13 — Monter le dossier d'un étage (le transfert)

Quand le dossier doit être validé par le bureau du dessus, on l'envoie au
**niveau supérieur**. Dans le code, ce mouvement s'appelle
`transfererNiveauSuperieur`. Décomposons-le comme une recette de cuisine.

**Ingrédients :**
- un dossier (son numéro) ;
- (optionnel) un commentaire et une priorité.

**La recette, étape par étape :**

**Étape 1 — Vérifier que le dossier existe.**
Si le dossier n'existe pas → on répond « introuvable » (erreur 404).

**Étape 2 — Trouver où il est.**
On cherche la ligne de circulation **active** (celle sans date de fin). Son
bureau = l'endroit où est le dossier.

**Étape 3 — Vérifier que l'utilisateur a le droit.**
L'utilisateur qui demande le transfert doit travailler dans le bureau qui
détient le dossier. Sinon → « introuvable » (on fait semblant que le dossier
n'existe pas, pour ne pas donner d'information).

**Étape 4 — Trouver le bureau du dessus.**
Le bureau supérieur = le **parent direct** (N+1). Si le bureau n'a pas de
parent (il est tout en haut de la pyramide) → on refuse, on ne peut pas monter
plus haut.

**Étape 5 — Le grand déplacement :**
1. On ferme les affectations des fonctionnaires actuels (ils ne voient plus
   le dossier).
2. On met une date de fin à la ligne de circulation actuelle.
3. On crée une nouvelle ligne de circulation chez le parent (pas de date de
   fin = dossier actif là-bas).
4. On affecte le dossier aux fonctionnaires du parent.
5. On prévient le facteur Kafka (une lettre `dossier-events` : « le dossier a
   changé de bureau »).

```
   AVANT                          APRÈS
   ┌──────────┐                  ┌──────────┐
   │  Parent  │                  │  Parent  │ ← le dossier arrive ICI
   │          │                  │ ●dossier │
   └──────────┘                  └──────────┘
   ┌──────────┐                  ┌──────────┐
   │  Moi ici │──dossier──►      │  Moi ici │ (ligne clôturée)
   │ ●dossier │                  │          │
   └──────────┘                  └──────────┘
```

**Et la priorité ?** Si l'utilisateur ne donne pas de priorité, on garde
**l'ancienne** priorité du dossier. C'est la règle « on n'oublie pas ce qu'on
savait déjà ».

*Mot compliqué du jour :* **transfererNiveauSuperieur** = la recette pour
faire monter un dossier d'un étage vers le bureau parent.

Et maintenant, la recette inverse : redescendre le dossier.

# Chapitre 14 — Redescendre le dossier (le retour)

Parfois, le dossier doit **redescendre**. Par exemple, le bureau du dessus a
regardé le dossier et dit : « Il manque un papier, renvoyez-le au service en
dessous ! » Ce mouvement s'appelle `retournerNiveauInferieur`.

**La grande différence avec le transfert :**
- Quand on **monte**, le nouveau bureau est **calculé tout seul** (le parent).
- Quand on **redescend**, l'utilisateur doit **dire lui-même** quel bureau
  doit recevoir le dossier (on donne son numéro dans la demande).

**Et une vérification très importante :** le bureau choisi doit être un
**enfant DIRECT** du bureau actuel. On ne peut pas envoyer le dossier à un
bureau qui est deux étages en dessous d'un coup. C'est comme un escalier : on
descend une marche à la fois.

```
   AVANT                          APRÈS
   ┌──────────┐                  ┌──────────┐
   │ Moi ici  │──dossier──►      │ Moi ici  │ (ligne clôturée)
   │ ●dossier │                  │          │
   └──────────┘                  └──────────┘
   ┌──────────┐                  ┌──────────┐
   │ Enfant   │                  │ Enfant   │ ← le dossier arrive ICI
   │          │                  │ ●dossier │
   └──────────┘                  └──────────┘
```

**Le reste de la recette est exactement le même que pour monter :**
1. Vérifier que le dossier existe.
2. Vérifier que l'utilisateur est bien dans le bureau détenteur.
3. Vérifier que la cible existe et qu'elle est un enfant direct.
4. Fermer les affectations et la ligne de circulation actuelle.
5. Créer la nouvelle ligne chez l'enfant.
6. Affecter les fonctionnaires de l'enfant.
7. Prévenir Kafka.

**Un petit détail :** quand on redescend, on peut mettre un **commentaire**
pour expliquer pourquoi (par exemple : « documents incomplets »). C'est le
« motif ». Dans le code, il n'est pas obligatoire, mais c'est une bonne
habitude de l'écrire pour que tout le monde comprenne.

*Mot compliqué du jour :* **retournerNiveauInferieur** = la recette pour faire
descendre un dossier d'un étage vers un bureau enfant choisi.

Notre atelier sait aussi montrer l'**historique** du dossier : la liste de
tous les bureaux visités, avec les dates. C'est comme le carnet de timbres
d'un passeport : chaque tampon raconte une étape du voyage.

Bon, on a vu les agents et les dossiers. Maintenant, allons voir les vrais
clients de l'administration : les **contribuables**.

# Chapitre 15 — Les contribuables (NIF et code secret OTP)

Un **contribuable**, c'est une personne (ou une société) qui doit payer des
impôts. Chaque contribuable a un numéro très spécial : le **NIF** (le numéro
d'immatriculation fiscale). C'est comme son numéro de carte d'identité fiscal.

**Comment un contribuable obtient-il un compte pour se connecter au
portail ?** Là, c'est une petite histoire de confiance. Le système veut être
SÛR que c'est bien le vrai titulaire du NIF qui se connecte, et pas un
imposteur. Alors il utilise un **code secret à 4 chiffres** : l'**OTP**.

**Le plan secret en 2 étapes :**

**Étape 1 — « Je veux créer mon compte. »**
Le contribuable donne son NIF. Notre atelier vérifie que ce contribuable
existe bien. Si oui, il fabrique un **code secret à 4 chiffres** (l'OTP) et le
donne au contribuable. Ce code est caché dans la base (caché = chiffré, on ne
peut pas le lire au hasard).

```
  Étape 1 :
  « Voici mon NIF » ──► Atelier ──► « Oui, tu existes !
                                  Voici ton code secret : 1234 »
```

**Étape 2 — « Voici mon code secret. »**
Le contribuable donne son code. Notre atelier compare le code donné avec le
code caché. Si c'est bon → « Tu es bien le vrai titulaire ! » → on crée son
compte chez Keycloak, dans le groupe « principal » du contribuable.

```
  Étape 2 :
  « Voici mon code : 1234 » ──► Atelier ──► « Parfait ! Je crée ton
                                           compte chez Keycloak. »
```

**Pourquoi 2 étapes ?** Parce que si un imposteur avait le NIF sans le code
secret, il ne pourrait pas créer le compte. Le code secret est la preuve
qu'on est le vrai propriétaire. (Dans la vraie vie, le code est envoyé par
email ou SMS — mais dans notre projet, il est juste retourné par l'API.)

**Deux sortes de comptes :**
- Le compte **principal** : le compte du propriétaire du NIF (créé après le
  code secret).
- Les comptes **secondaires** : d'autres personnes autorisées par la société
  (créés par l'administrateur).

*Mot compliqué du jour :* **OTP** = One Time Password = un code secret à
usage unique, qui sert à prouver qu'on est le vrai propriétaire du compte.

Et une fois le contribuable connecté, que se passe-t-il quand il déclare ses
impôts et qu'il paie ? C'est le prochain chapitre.

# Chapitre 16 — Les déclarations et les paiements (les copies)

Notre atelier ne connaît pas tout du contribuable : il laisse les autres
ateliers faire leur travail. Mais il a besoin de connaître les **déclarations**
(ce que le contribuable annonce gagner ou vendre) et les **paiements** (ce
qu'il donne). Alors… il en fait des **copies** !

**Comment ? Grâce au facteur Kafka.** Quand l'atelier des déclarations a une
nouvelle déclaration, il dépose une lettre dans la boîte `declaration-events`.
Notre atelier la lit et **range une copie dans son entrepôt**.

**Mais notre atelier ne copie pas bêtement.** Il fait un petit calcul malin :
la **pénalité de retard**.

**La règle de la pénalité (racontée simplement) :**
1. Notre atelier demande à un autre service : « À quelle date ce paiement
   était-il attendu ? » (la date d'exigibilité).
2. Il regarde si le contribuable a payé **avant** cette date.
   - S'il a payé à temps → **pas de pénalité**. Ouf !
   - S'il a payé en retard → on calcule une **amende** : plus le retard est
     long, plus l'amende est grosse. L'amende = la base (ce qu'il devait)
     multipliée par un taux qui dépend des jours de retard.

```
   La petite calculatrice des pénalités :

   Payé à temps  ➜  pénalité = 0  (bravo !)
   En retard     ➜  pénalité = base × taux
                    (selon le nombre de jours de retard)
```

**Pareil pour les paiements :** l'atelier des paiements publie `paiement-events`
et notre atelier garde une copie du paiement avec son ordre de paiement (de
quel genre de paiement il s'agit : impôt, amende, etc.).

**Pourquoi garder des copies ?** Parce que notre atelier doit répondre à une
question très importante du contribuable : « Combien me reste-t-il à payer ? »
C'est le prochain chapitre : le Compte Courant Fiscal.

*Mot compliqué du jour :* **pénalité de retard** = une petite amende ajoutée
quand le paiement arrive après la date attendue.

# Chapitre 17 — Le Compte Courant Fiscal (le CCF)

Imagine le carnet de compte de tes parents à la banque : ce qu'ils devaient,
ce qu'ils ont payé, et combien il reste. Pour le contribuable, c'est pareil !
Ce carnet s'appelle le **Compte Courant Fiscal** — abrégé **CCF**.

**Le CCF est organisé par impôt.** Il y a plusieurs sortes d'impôts, chacun
avec un petit nom en code :
- **IRE** : l'impôt sur les revenus des employés ;
- **PF** : la patente (la licence pour travailler) ;
- **IPV** : l'impôt sur la propriété ;
- **TCAA** : l'impôt sur certains métiers ;
- **TPFL** : un autre impôt sur les entreprises.

Pour chaque impôt, on calcule :
- ce que le contribuable **doit** (ses déclarations + les pénalités) ;
- ce qu'il a **payé** ;
- et le **solde** : doit − payé.

**Le grand tableau :**

```
   COMPTE COURANT FISCAL du contribuable

   Impôt   │  Je dois (déclarations)  │  J'ai payé  │  Solde
   ────────┼──────────────────────────┼─────────────┼────────
   IRE     │         100 000          │    50 000   │  +50 000
   PF      │          40 000          │    40 000   │      0
   TCAA    │          30 000          │     0       │  +30 000
   ────────┴──────────────────────────┴─────────────┴────────
   TOTAL                                 Solde général : 80 000
```

Le contribuable peut voir son CCF en demandant au service (l'adresse est
`GET /compte_general/...` avec les dates). Et notre atelier construit ce
tableau en mélangeant :
- ses **copies locales** de déclarations ;
- les **paiements** qu'il va chercher chez l'atelier des paiements (par
  internet, avec son robot WebClient).

**Petit secret à connaître :** ce tableau ne garde pas les montants
historiques dans un tiroir — il les **recalcule** à chaque demande, à partir
des copies. C'est pour ça qu'il a besoin de copies à jour.

*Mot compliqué du jour :* **CCF** = le relevé de compte du contribuable, qui
montre ce qu'il doit, ce qu'il a payé, et ce qui reste, impôt par impôt.

Maintenant, réunissons tout ce qu'on a appris dans une grande histoire de A à
Z !

# Chapitre 18 — L'histoire de A à Z (le scénario complet)

Il est temps de raconter la grande histoire qui rassemble TOUT ce qu'on a
appris. Suis bien, c'est le chapitre le plus important du livre !

**L'histoire de Mireille, une petite boulangerie.**

**Étape 1 — Mireille veut s'inscrire.**
Mireille va au portail et remplit un formulaire d'immatriculation. L'atelier
d'immatriculation enregistre sa demande.

**Étape 2 — Le facteur apporte la nouvelle.**
L'atelier d'immatriculation dépose une lettre dans la boîte
`personne-physique-events`. Notre atelier la lit et **crée un dossier de
travail** : une demande d'immatriculation, posée automatiquement sur le bureau
de la structure **la moins chargée**. C'est le facteur Kafka qui a tout
apporté, sans téléphone.

**Étape 3 — Un agent travaille.**
L'agent se connecte avec son badge (Keycloak fabrique le badge). Il ne voit
que les dossiers de son bureau. Il vérifie la demande et donne le **NIF** de
Mireille. L'atelier d'immatriculation publie une lettre `contribuable-events`.

**Étape 4 — Mireille devient un contribuable connu.**
Notre atelier lit la lettre, garde une **copie** du contribuable en local, et
crée automatiquement un compte Keycloak pour elle.

**Étape 5 — Mireille crée son compte principal (le code secret).**
Mireille donne son NIF → elle reçoit un **code secret OTP** → elle le donne
→ le système vérifie → son compte principal est créé. Elle peut se connecter
au portail.

**Étape 6 — Le dossier circule (si besoin).**
Si la demande doit être validée en haut, l'agent la fait **monter d'un
étage** (transfert au niveau supérieur). Le dossier voyage, avec son
historique. Un jour peut-être il **redescendra** avec un commentaire
« documents incomplets ».

**Étape 7 — Mireille déclare et paie.**
Elle déclare ses ventes (atelier des déclarations) et paie (atelier des
paiements). Des lettres arrivent dans `declaration-events` et
`paiement-events`. Notre atelier fait des copies et calcule les pénalités si
elle a payé en retard.

**Étape 8 — Mireille regarde son CCF.**
Elle demande son Compte Courant Fiscal : elle voit ce qu'elle doit par impôt,
ce qu'elle a payé, et son solde. Tout est là, grâce aux copies.

```
      L'HISTOIRE DE MIREILLE (de A à Z)

  [immatriculation] ──► Kafka ──► dossier de travail créé (structure la moins chargée)
        │                    │
        ▼                    ▼
  NIF donné ──► contribuable-events ──► copie locale + compte Keycloak
        │
        ▼
  Mireille fait le code secret (OTP) ──► compte principal créé
        │
        ▼
  Le dossier circule dans la pyramide (monte / descend)
        │
        ▼
  Déclarations + paiements ──► Kafka ──► copies + pénalités
        │
        ▼
  CCF : « ce que je dois » − « ce que j'ai payé » = solde
```

*Mot compliqué du jour :* **bout en bout** = du début à la fin. Une histoire
« de A à Z » suit tout le chemin, sans rien sauter.

Et si Mireille était un agent qui clique dans l'interface ? Suivons le voyage
d'un simple clic, du bouton jusqu'à la réponse.

# Chapitre 19 — Le voyage d'un clic

Quand un utilisateur clique sur un bouton dans l'application, que se
passe-t-il derrière ? Suivons un clic précis : « Je veux voir la liste de mes
dossiers ».

**Étape 1 — Le clic devient une demande.**
Le clic est transformé en une petite requête qui voyage sur Internet jusqu'à
la porte 9000 de notre atelier. La demande s'appelle une **requête HTTP**. Et
elle porte le badge JWT de l'utilisateur.

**Étape 2 — Le gardien vérifie le badge.**
Spring Security regarde la signature et la date du badge. C'est bon, il
laisse passer. Le décodeur (JwtAuthConverter) lit les rôles.

**Étape 3 — Le chef d'atelier lit la demande.**
La demande arrive chez un **controller** (le chef d'atelier). Il dit : « Ah,
tu veux la liste des dossiers ? Je connais le bon service pour ça. »
Le controller ne fait presque rien lui-même : il transmet.

**Étape 4 — L'ouvrier travaille.**
Le **service** (l'ouvrier) fait le vrai travail : les vérifications, les
calculs. « Je ne vais te montrer que les dossiers de TON bureau », dit-il.

**Étape 5 — L'entrepôt se souvient.**
Le service demande à PostgreSQL (l'entrepôt) les informations. L'entrepôt
cherche et renvoie les lignes de la base.

**Étape 6 — On répond à l'utilisateur.**
Le service transforme les données en une belle réponse, et elle repart sur
Internet jusqu'à l'écran de l'utilisateur. La liste s'affiche. Clic réussi !

```
     LE VOYAGE D'UN CLIC

  Clic (utilisateur)
     │
     ▼
  Requête HTTP + badge JWT ──► 9000
     │
     ▼
  LE GARDIEN (Spring Security) : badge valable ? ✔
     │
     ▼
  LE CHEF (Controller) : quelle action ? ──► "liste des dossiers"
     │
     ▼
  L'OUVRIER (Service) : je filtre selon ta structure
     │
     ▼
  L'ENTREPÔT (PostgreSQL) : voilà les données !
     │
     ▼
  La réponse revient ──► l'écran affiche la liste
```

**Petit rappel des rôles :** le controller ne fait que diriger, le service
fait le travail, le repository parle à l'entrepôt. C'est comme au restaurant :
le serveur (controller) prend la commande, le cuisinier (service) prépare, et
le garde-manger (repository) fournit les ingrédients.

*Mot compliqué du jour :* **HTTP** = la façon dont les ordinateurs se parlent
sur Internet. Une « requête HTTP » est une demande polie qu'un ordinateur
envoie à un autre.

Et voilà ! Tu as fait le tour des règles et des histoires du projet. Il
reste encore quelques parties : on va visiter les fichiers de la maison,
apprendre à lire les erreurs, savoir démarrer le projet, creuser les
métiers, répondre aux questions les plus fréquentes… et finir par un petit
quiz. Bonne route, explorateur !

---

# PARTIE 7 — La visite guidée des fichiers

Tu connais maintenant les personnages de notre histoire. Il est temps de
**mettre le nez dans le projet** et de regarder chaque dossier, chaque fichier,
comme si on visitait un château pièce par pièce. Ne t'inquiète pas si certains
noms te semblent bizarres : à la fin de cette partie, tu sauras te repérer dans
la maison sans te perdre.

```
    LE PLAN DU CHÂTEAU (notre projet)
  ┌──────────────────────────────────────────────┐
  │  Racine  :  pom.xml, application.yml,        │
  │            Dockerfile, docker-compose.yml,   │
  │            Jenkinsfile, schema.sql           │
  │  config  :  les réglages de la maison        │
  │  exceptionHandling : le médecin des erreurs  │
  │  util & helper : la boîte à outils           │
  │  features : les grandes pièces du château    │
  │    └── dossier, circulation, contribuable,   │
  │        kafka, keycloak, personnePhysique...  │
  └──────────────────────────────────────────────┘
```

---

# Chapitre 21 — Le grenier du château : les fichiers de la racine

Quand tu ouvres le projet dans ton éditeur (IntelliJ, VS Code…), tu vois une
liste de fichiers et de dossiers. C'est la **racine** : le point de départ de
tout. On dirait le grenier du château : il y a des choses précieuses, un peu
de tout, et chaque chose a un rôle.

### `pom.xml` : la liste des courses de Maven

Souviens-toi du chapitre 3 : **Maven** est le robot qui achète les briques.
Le fichier `pom.xml` est **la liste des courses** ! Il dit à Maven :

- « Utilise Java 17 » ;
- « Va me chercher Spring Boot 3.2.8 » ;
- « Je veux des briques pour Keycloak, Kafka, PostgreSQL, Swagger… » ;
- « Et un truc magique appelé Lombok pour écrire moins de code ».

```
  pom.xml
  ┌────────────────────────────────────┐
  │  java.version = 17                 │
  │  spring-boot = 3.2.8               │
  │  dépendances : keycloak-admin,     │
  │    spring-kafka, postgresql,       │
  │    swagger (openapi), lombok,      │
  │    validation, security-oauth2...  │
  └────────────────────────────────────┘
```

### `application.yml` : le cahier de réglages

Ce fichier est **le cahier des réglages** du programme. On y trouve :

- le **port** : 9000 ;
- l'adresse de **PostgreSQL** (la base de données) ;
- l'adresse de **Keycloak** (le chef du personnel) et du **realm** `itas` ;
- l'adresse de **Kafka** (le facteur) ;
- les **topics** (les boîtes aux lettres) à écouter ;
- la **whitelist** : la liste des chemins où on n'exige pas de badge.

C'est ici qu'on dit au programme *où* trouver ses amis (Keycloak, Kafka,
PostgreSQL) et *comment* se comporter. Un peu comme le carnet d'adresses des
parents quand on garde un enfant : « la nounou est à cette adresse, l'école à
celle-ci ».

### `application-email.properties` : la boîte des lettres

Un autre cahier de réglages, spécial pour les **emails**. On y trouve
l'adresse du serveur d'envoi (SMTP), le nom de l'application et les sujets
des emails de bienvenue et de réinitialisation de mot de passe. Quand un
nouveau fonctionnaire est créé, c'est grâce à lui que l'email part.

### `Dockerfile` : la recette de cuisine

**Docker** est l'art du carton : on emballe tout le programme (avec sa
caisse de briques) dans une grande boîte appelée **image**, puis on la fait
tourner dans un conteneur. La `Dockerfile` est **la recette** pour fabriquer
cette boîte :

```
  1. Prends une image Maven avec Java 17
  2. Copie le pom.xml
  3. Télécharge les dépendances (mvn dependency:go-offline)
  4. Copie le code source (src)
  5. Fabrique le programme (mvn clean package)
  6. Prends une petite image Java 17 (alpine)
  7. Mets le programme fabriqué (app.jar) dedans
  8. Ouvre le port 9000
  9. Lance : java -jar app.jar
```

### `docker-compose.yml` : la fête des boîtes

Si `Dockerfile` est la recette d'UNE boîte, `docker-compose.yml` est **la
liste des boîtes à faire fonctionner ensemble** : notre service, peut-être
Kafka, etc. On peut tout lancer d'un seul coup avec une commande magique :
`docker compose up -d`. C'est comme inviter tous les invités à une fête et
dire « la porte s'ouvre ! ».

### `Jenkinsfile` : le plan du robot bâtisseur

**Jenkins** est le robot de l'usine qui construit et installe les
programmes tout seul (on appelle ça **l'intégration continue**). Le
`Jenkinsfile` est son **plan de travail** :

```
  Étape 1 : supprimer l'ancien conteneur itas-utilisateur-ms
  Étape 2 : construire l'image (docker build -t itas-utilisateur-ms .)
  Étape 3 : lancer (docker compose up -d)
  À la fin : afficher l'état des conteneurs (docker compose ps)
```

### `schema.sql` : le plan du classeur

Tu te souviens de la base de données, le grand classeur ? `schema.sql`
contient **le plan du classeur** : quelles tables créer (`tbl_dossier`,
`tbl_circulation_dossier`…). Il est utilisé quand on part de zéro.

### `banner.txt` : le dessin de bienvenue

Un petit fichier d'ambiance : quand le programme démarre, il affiche un
grand dessin « ITAS » dans la console. C'est juste pour le plaisir des yeux.

*Mot compliqué du jour :* **dépendance** = une brique qu'un autre robot a déjà
fabriquée, et que notre programme demande à Maven d'aller chercher.

### La liste des pièces : le dossier `features`

À la racine du code, il y a un dossier très important : **`features`**. Il
contient toutes les grandes pièces du château, chacune dans son propre
sous-dossier. Voici la liste des pièces principales (avec leur nom de code) :

```
   features
   ├── authentication      → se connecter (login, OTP, mot de passe)
   ├── keycloak            → le chef du personnel (user, tache, poste)
   ├── personnePhysique    → les personnes (les gens de l'usine)
   ├── personneMorale      → les personnes morales (les entreprises)
   ├── contribuable        → les contribuables (NIF, vérifications)
   ├── exerciceFiscal      → les exercices fiscaux (les années)
   ├── structureAdministrative → la pyramide des structures
   ├── affectation         → « qui travaille où »
   ├── affectationDossier  → lier des dossiers à des fonctionnaires
   ├── dossier             → les dossiers (la pièce qu'on a visitée)
   ├── circulationDossier  → le voyage des dossiers
   ├── paiement            → les paiements (copies Kafka)
   ├── declaration         → les déclarations (copies Kafka)
   ├── compteCourantFiscal → le CCF (le compte du contribuable)
   └── kafka               → le facteur (producer, consumers, topics)
```

Chaque pièce a la même organisation : `controller` (le chef), `services`
(le travail), `repository` (le garde-manger), `entity` (la fiche),
`dtos` (les fiches de transport) et souvent un `mapper` (le traducteur).
Si tu sais lire UNE pièce, tu sais les lire toutes !

---

# Chapitre 22 — Le tiroir des réglages : `config`

Dans le projet, il y a un dossier qui s'appelle `config`. C'est **le tiroir
des réglages avancés** : de petits fichiers Java qui disent au programme
« fais ça au démarrage ». Chaque fichier est comme un interrupteur.

```
   config
   ├── SecurityConfig        → le gardien et sa liste (whitelist)
   ├── JwtAuthConverter      → le lecteur de badges
   ├── WebClientConfig       → les téléphones pour parler aux autres
   ├── OpenApiConfig         → la documentation automatique (Swagger)
   ├── JacksonConfig         → le traducteur des messages
   ├── WebConfig             → le réglage des "spécifications" des requêtes
   └── DossierSchemaMigration → le bricoleur qui répare les tables
```

### `SecurityConfig.java` : le poste du gardien

Nous l'avons rencontré au chapitre 6. C'est **le poste du gardien** : il
liste les chemins où tout le monde peut passer sans badge (Swagger,
`/authentication/**`, la vérification des contribuables par NIF, la
vérification de l'OTP…), et dit « pour tout le reste, il faut un badge ! ».

### `JwtAuthConverter.java` : le lecteur de badges

Souviens-toi du chapitre 5 : le badge est le **JWT**. Ce fichier est **la
machine qui lit les badges** : elle regarde le badge présenté, vérifie qu'il
est bien signé, et transforme les « rôles » du badge (les boutons) en
« autorités » que le gardien comprend.

### `WebClientConfig.java` : les téléphones

Notre atelier doit parler aux autres ateliers de l'usine (par exemple,
demander à Keycloak de créer un utilisateur). Pour cela il utilise
**WebClient** : c'est comme un téléphone portable qu'on tient à la main.
Ce fichier prépare le téléphone avec les bonnes réglages.

### `OpenApiConfig.java` : la documentation automatique

Quand tu ouvres l'URL du projet avec Swagger (par exemple
`http://localhost:9000/swagger-ui`), tu vois **toute la liste des
réglages disponibles**, avec un gros bouton « Authorize » pour coller son
badge. Ce fichier crée cette documentation : il dit « mon API s'appelle
ITAS Utilisateur API, et elle se sécurise avec un badge JWT appelé
bearer-key ».

### `JacksonConfig.java` : le traducteur des messages

**Jackson** est le traducteur qui transforme le texte JSON (les messages que
les ordinateurs s'échangent) en objets Java. Ce fichier le règle pour qu'il
soit gentil : s'il voit une propriété inconnue, il ne crie pas, il l'ignore
(tout simplement) ! Pourquoi ? Parce que Keycloak, dans certaines versions,
envoie des choses bizarres — et on ne veut pas que le programme pleure.

### `WebConfig.java` : le filtre à spécifications

Ce petit fichier ajoute un « tournevis » spécial pour gérer les requêtes
avec des filtres de recherche (le paquet `specification-arg-resolver`).
Pas besoin d'en savoir plus pour l'instant : c'est un accessoire du
château.

### `DossierSchemaMigration.java` : le bricoleur

Ici, un petit héros discret. À chaque démarrage, il **vérifie la forme des
tables** de la base de données et les **répare** si besoin : par exemple, si
une table s'appelait `tbl_dossiern` à cause d'une ancienne erreur, il la
renomme proprement en `tbl_dossier` et corrige les liens (les clés
étrangères). C'est un peu le plombier qui passe chaque matin vérifier que
les tuyaux ne fuient pas !

*Mot compliqué du jour :* **clé étrangère** = un lien dans le classeur qui
dit « cette ligne appartient à cette ligne-là d'une autre table ».

---

# Chapitre 23 — Le médecin des erreurs : `exceptionHandling`

Quand un enfant se fait mal, il y a une infirmerie. Pour notre programme,
l'infirmerie s'appelle **`exceptionHandling`**. C'est ici qu'on décide quoi
faire quand quelque chose tourne mal, et quel message gentil renvoyer.

```
  exceptionHandling
  ├── handler/GlobalExceptionHandler   → le médecin chef
  ├── exceptions/                      → les maladies (les exceptions)
  │     ├── ResourceNotFoundException  → « je n'ai pas trouvé la chose »
  │     ├── ResourceExistException     → « cette chose existe déjà »
  │     ├── AccessDeniedException      → « tu n'as pas le droit »
  │     ├── MyNotFoundException        → un autre « pas trouvé »
  │     └── InvalidInputExceptionMessage
  └── message/                         → les bons de sortie (les réponses)
  ```

### Le médecin chef : `GlobalExceptionHandler`

C'est une classe très spéciale. On la reconnaît avec son étiquette
`@RestControllerAdvice`. Cette étiquette signifie : « je m'occupe des
accidents de TOUT le programme ». Dès qu'une exception arrive n'importe où,
elle atterrit chez le médecin chef, qui regarde de quelle maladie il
s'agit et choisit la réponse à envoyer.

```
        UN ACCIDENT DANS LE PROGRAMME
   Le service lance une exception
               │
               ▼
   GlobalExceptionHandler (le médecin)
               │
               ├── ResourceNotFoundException → 404 « pas trouvé »
               ├── ResourceExistException   → 409 « déjà là ! »
               ├── IllegalArgumentException → 400 « mauvaise demande »
               ├── AccessDeniedException    → 403 « interdit »
               └── (autre chose)            → 500 « oups, erreur interne »
```

### Les maladies (les exceptions)

Une **exception** est un petit panneau d'alarme qu'on lance quand quelque
chose ne va pas. Le programme crie « STOP, problème ! » et le médecin
s'occupe du reste. Regarde dans le code, tu verras souvent ce genre de
phrase :

```
    dossierRepository.findById(id)
        .orElseThrow(() -> new ResourceNotFoundException(
            "Dossier non trouvé avec l'ID: " + id));
```

Ça veut dire : « cherche le dossier ; si tu ne le trouves pas, lance
l'alarme « Dossier non trouvé » ». Et le médecin répondra un beau message
avec le code 404.

*Mot compliqué du jour :* **exception** = une alerte que le programme lance
quand quelque chose ne va pas. Le programme ne s'arrête pas : il appelle le
médecin qui répond poliment à celui qui demandait.

---

# Chapitre 24 — La boîte à outils : `util` et `helper`

Chaque bon bricoleur a une caisse d'outils. Notre projet a **deux caisses** :
`util` et `helper`. Regardons ce qu'il y a dedans.

### `util` : les outils tout simples

- **`SecurityUtils`** : l'outil pour lire le badge de la personne qui
  demande. Il peut donner l'**id de l'utilisateur** (le `sub` du JWT),
  son **organisation**, ou même le **badge complet** en texte. Quand le
  programme doit savoir « qui est-ce qui demande ? », il utilise cet outil.
- **`PasswordGenerator`** : l'outil qui fabrique les mots de passe et les
  codes OTP. Attention, c'est un farceur : dans le code actuel, il répond
  toujours `123456` pour le mot de passe (la vraie génération est
  commentée). Parfait pour tester, mais à changer plus tard !

### `helper` : les assistants du ménage

- **`Constante`** : LE grand dictionnaire des constantes. Tous les nombres
  et textes qui ne changent jamais sont là : les 10 niveaux de structures
  (NIVEAU1 à NIVEAU10), les statuts de dossier, les types d'opérations, les
  modules, les types d'impôt du CCF (IRE, PF, IPV, TCAA, TPFL)… Tout est
  centralisé pour ne pas répéter les mêmes valeurs partout.
- **`FilterHelper`** : l'assistant de la pagination. Quand on liste des
  dossiers, il prépare la réponse avec le nombre total, la page courante,
  etc. (souviens-toi de `getAll` dans le chapitre dossier).
- **`RelationNiveauStructure`** : l'outil qui sait, pour chaque niveau de
  la pyramide, quel est son **parent** (le N+1). C'est lui qui fait
  fonctionner la règle « un dossier va chez le parent direct ».
- **`DateHelper`** : l'outil des dates (transformer, comparer, calculer).
- **`StaticValue`** et **`StaticListOfValues`** : des outils qui fournissent
  des valeurs et des listes « toutes prêtes » pour l'interface.
- **`Mapper`** et les « Mapper » de chaque feature : les traducteurs qui
  transforment un objet de la base (entity) en objet à renvoyer (DTO) et
  vice-versa.

```
  POURQUOI DES OUTILS ?
  Au lieu de réécrire la même recette partout, on la met
  dans un outil et tout le monde l'utilise.
  → moins de copier-coller, moins d'erreurs.
```

*Mot compliqué du jour :* **constante** = une valeur qui ne change jamais,
stockée à un seul endroit pour pouvoir la modifier facilement si besoin.

---

# Chapitre 25 — La visite d'une pièce : la feature `dossier`

On a visité le grenier, les tiroirs, la boîte à outils. Maintenant, entrons
dans une vraie **pièce du château** : la feature `dossier`. C'est l'exemple
parfait pour comprendre comment toutes les pièces fonctionnent, parce
qu'elle a **tout** : controller, service, repository, entity, DTO, mapper.

```
   features/dossier
   ├── controller/DossierController.java   → le chef d'atelier
   ├── services/DossierService.java        → le contrat (la liste des travaux)
   ├── services/DossierServiceImplem.java  → le cuisinier (le vrai travail)
   ├── repository/DossierRepository.java   → le garde-manger
   ├── entity/Dossier.java                 → la fiche du dossier
   ├── dtos/DossierCreateDto.java          → la fiche pour créer
   ├── dtos/DossierUpdateDto.java          → la fiche pour modifier
   ├── dtos/DossierViewDto.java            → la fiche pour regarder
   └── mapper/DossierMapper.java           → le traducteur
```

### Le chef d'atelier : `DossierController`

Regarde le code du controller. Il commence par `@RestController` (je suis un
chef d'atelier) et `@RequestMapping("/dossiers")` (je réponds quand on me
parle de `/dossiers`). Il a 5 grandes actions :

| Action HTTP | Chemin      | Que fait-il ?                       |
|-------------|-------------|-------------------------------------|
| POST        | `/dossiers` | Créer un nouveau dossier (code 201) |
| PUT         | `/dossiers/{id}` | Modifier un dossier             |
| GET         | `/dossiers/{id}` | Regarder un dossier            |
| GET         | `/dossiers` | Lister les dossiers (avec pagination) |
| DELETE      | `/dossiers/{id}` | Supprimer (réponse 204)     |

Le controller **ne fait presque rien** : il reçoit la demande et la passe
au service. C'est le serveur au restaurant : il ne cuisine pas.

### Le cuisinier : `DossierServiceImplem`

C'est ici qu'est **le vrai travail**. Regarde `create` :

```
  1. On vérifie qu'aucun dossier n'a déjà cette référence
     → si oui, on lance ResourceExistException (409)
  2. On cherche la structure administrative (celle fournie, ou
     celle de l'utilisateur connecté grâce à SecurityUtils)
  3. On transforme le DTO en entité (grâce au mapper)
  4. On sauvegarde dans la base (dossierRepository.save)
  5. On crée la circulation initiale du dossier
     (circulationDossierService.creerCirculationInitiale)
  6. On renvoie la fiche de lecture (ViewDto)
```

C'est **grâce à ce service** que la règle « créer un dossier = lui donner
une première circulation » est respectée.

### Le garde-manger : `DossierRepository`

Une toute petite interface : elle dit « je vais chercher des dossiers dans
la base ». Spring Data JPA fabrique tout seul les méthodes comme
`findById`, `findAll`, `existsByReference`… Magique, non ? On écrit juste
le nom de la méthode et le programme comprend ce qu'on veut.

### La fiche : `Dossier` (l'entité)

L'entité décrit **la forme d'une ligne du classeur** `tbl_dossier` :
`id`, `typeDossier`, `reference` (unique !), `description`, `dateCreation`,
`dateFin`. Les petites étiquettes comme `@NotNull`, `@Size(max=100)`
servent de règles de validation : « la référence ne peut pas être vide et
pas plus de 100 lettres ».

### Le traducteur : `DossierMapper`

Il sait transformer :
- `DossierCreateDto` → `Dossier` (pour créer) ;
- `DossierUpdateDto` → `Dossier` (pour modifier) ;
- `Dossier` → `DossierViewDto` (pour renvoyer une réponse propre).

```
   DTO (la fiche papier)
        │
      mapper  ← le traducteur
        │
   ENTITY (la ligne du classeur)
```

*Mot compliqué du jour :* **DTO** = « Data Transfer Object » : une fiche
spéciale qui transporte des informations entre les pièces, sans les
secrets internes de la base de données.

---

# Chapitre 26 — Le tiroir du facteur : `features/kafka`

Nous avons déjà parlé de Kafka au chapitre 8. Maintenant, regardons **les
fichiers** qui s'occupent du facteur dans le projet.

```
   features/kafka
   ├── producer/KafkaEventPublisher.java      → l'expéditeur de lettres
   ├── config/KafkaProducerConfig.java        → réglages de l'expéditeur
   ├── config/KafkaTopicsConfig.java          → réglages des boîtes aux lettres
   ├── topics/KafkaTopics.java                → les noms des boîtes
   └── (les dossiers des consumers)
       ├── AffectationDossier/consummer/PersonnePhysiqueConsummer.java
       ├── consumers/ContribuableConsummer.java
       ├── exerciceFiscal/consummer/ExerciceFiscalConsummer.java
       └── ... (personneMorale, paiement, declaration, etc.)
```

### Les noms des boîtes : `KafkaTopics.java`

Un fichier tout petit qui contient les noms des boîtes aux lettres :
`fonctionnaire-events`, `dossier-events`. Remarque que certains noms sont
**commentés** (avec `//`) : la boîte `secteur-activite-events` par exemple
n'est plus utilisée. Les commentaires sont des notes qu'on laisse pour
soi-même : le programme ne les lit pas.

### L'expéditeur : `KafkaEventPublisher`

C'est lui qui **envoie les lettres**. On lui donne un sujet (le nom de la
boîte) et un message, et il le confie au facteur Kafka pour que les autres
ateliers le reçoivent.

### Les facteurs qui reçoivent : les Consumers

Chaque consumer a une étiquette avec le nom de la boîte qu'il écoute,
par exemple `@KafkaListener(topics = "...")`. Quand une lettre arrive,
le consumer se réveille et **va vérifier dans sa propre base** si le
numéro existe déjà ; si non, il enregistre une copie.

```
     L'atelier des contribuables
          │  (envoie une lettre : "contribuable créé")
          ▼
        KAFKA  (la boîte aux lettres)
          │
     ┌────┴────────────┐
     ▼                 ▼
  Notre service     Autres ateliers
  (crée une copie   (font leur travail)
  du contribuable)
```

*Mot compliqué du jour :* **commentaire** = une note écrite dans le code
(avec `//` ou `/* */`) pour expliquer aux humains. L'ordinateur l'ignore
complètement.

---

# Chapitre 27 — Le tiroir du chef du personnel : `features/keycloak`

Souviens-toi du chapitre 7 : Keycloak est le chef du personnel qui garde
les badges. Dans notre projet, les fichiers qui parlent à Keycloak sont
dans `features/keycloak`.

```
   features/keycloak
   ├── user/
   │     ├── controller/UserController.java   → les demandes "utilisateurs"
   │     ├── service/UserServiceImplem.java   → le vrai travail
   │     └── ...
   ├── tache/
   │     ├── controller/TacheController.java  → les demandes "rôles"
   │     └── service/TacheServiceImplem.java
   └── poste/
         └── ...                              → les postes (les fonctions)
```

### `UserController` et `UserServiceImplem`

C'est ici qu'on **crée les fonctionnaires**. Quand quelqu'un demande
« crée un nouvel utilisateur », le service va :

1. générer un mot de passe temporaire (attention, actuellement c'est
   `123456` dans `PasswordGenerator` !) ;
2. appeler Keycloak pour créer l'utilisateur et son badge ;
3. lui donner son **poste** (son groupe) pour qu'il ait les bons boutons
   sur son badge ;
4. sauvegarder la copie dans notre base (la fiche fonctionnaire) ;
5. envoyer un email de bienvenue.

Le controller commence par `@RequestMapping("/api/users")`. Regarde ses
routes : on retrouve presque **toutes les actions possibles sur un
fonctionnaire** !

| Méthode | Chemin            | Rôle                                  |
|---------|-------------------|---------------------------------------|
| POST    | `/api/users/create` | Créer un utilisateur fonctionnaire    |
| GET     | `/api/users/current` | Récupérer l'utilisateur connecté    |
| GET     | `/api/users/current/structure-administrative` | Sa structure |
| PUT     | `/api/users/{id}`  | Modifier un utilisateur               |
| DELETE  | `/api/users/{id}`  | Supprimer un utilisateur              |
| POST    | `/api/users/{id}/reset-password` | Réinitialiser le mot de passe |
| PATCH   | `/api/users/{id}/status` | Changer le statut (actif/inactif) |
| GET     | `/api/users/search` | Chercher des utilisateurs            |

Et des routes spéciales pour les **contribuables** (`create_group_contribuable`,
`create_user_contribuable`, `affect_contribuable_users_to_group`…) : on voit
bien que le projet gère plusieurs familles de comptes.

### `TacheController` : les rôles et les groupes

Ce controller s'occupe des **rôles** de Keycloak (les boutons des badges).
Regarde ses chemins :

| Méthode | Chemin                       | Rôle                                   |
|---------|------------------------------|----------------------------------------|
| DELETE  | `/taches/roles`              | Supprimer tous les rôles du client     |
| POST    | `/taches/groups/{code}/roles`| Assigner des rôles à un groupe         |
| PUT     | `/taches/groups/{code}/roles`| Mettre à jour les rôles d'un groupe    |
| GET     | `/taches/getTaches`          | Lister les tâches et permissions       |

Tu remarqueras des gros bouts de code **commentés** (les anciennes méthodes
`createInitRoles` et `getGroupPermissions`). C'est très courant dans un
projet : on garde l'ancien code en note au cas où on en aurait besoin.

*Mot compliqué du jour :* **groupe** (chez Keycloak) = une équipe de gens
qui partagent les mêmes boutons sur leur badge. Le poste d'un fonctionnaire,
c'est son groupe.

---

# PARTIE 8 — Les erreurs expliquées simplement

Quand un programme fait un « bruit bizarre », il répond avec un **code à
trois chiffres**. Ces codes ressemblent à une langue secrète. Dans cette
partie, on va apprendre à lire cette langue !

---

# Chapitre 28 — La langue secrète : les codes HTTP

Quand ton programme répond, il dit toujours un **code à trois chiffres**.
C'est comme un panneau de signalisation : chaque panneau a un sens.

```
   LES CODES DE LA ROUTE
   ┌──────────┬──────────────────────────────┐
   │ 200-299  │ TOUT VA BIEN (les feux verts)│
   │ 300-399  │ ON EST REDIRIGÉ              │
   │ 400-499  │ C'EST TA FAUTE (mauvaise demande) │
   │ 500-599  │ C'EST LA FAUTE DU PROGRAMME  │
   └──────────┴──────────────────────────────┘
```

### Les feux verts (2xx) : tout va bien

| Code | Nom          | En clair                                             |
|------|--------------|------------------------------------------------------|
| 200  | OK           | « C'est fait ! Voici le résultat. »                  |
| 201  | CREATED      | « J'ai bien créé la chose ! » (on l'utilise quand on crée un dossier, un utilisateur…) |
| 204  | NO_CONTENT  | « C'est fait, et je n'ai rien à te montrer. » (après une suppression) |

Dans `DossierController`, tu as vu :
`new ResponseEntity<>(..., HttpStatus.CREATED)` pour une création, et
`ResponseEntity.noContent().build()` pour une suppression. Tu les connais
maintenant !

### Les feux orange (4xx) : attention, c'est ta faute

Le programme dit poliment : « ta demande n'est pas bonne ».

| Code | Nom        | En clair                                       |
|------|------------|------------------------------------------------|
| 400  | BAD REQUEST | « Ta demande est mal écrite. »                  |
| 401  | UNAUTHORIZED | « Tu n'as pas de badge, ou il n'est pas valable. » |
| 403  | FORBIDDEN  | « Tu as un badge, mais tu n'as pas le droit. »  |
| 404  | NOT FOUND  | « Je ne trouve pas la chose demandée. »         |
| 405  | METHOD NOT ALLOWED | « Cette action n'est pas possible sur ce chemin. » |
| 409  | CONFLICT   | « Conflit ! La chose existe déjà. »             |

### Les feux rouges (5xx) : oups, c'est notre faute

| Code | Nom                 | En clair                                      |
|------|---------------------|-----------------------------------------------|
| 500  | INTERNAL SERVER ERROR | « Il y a un problème dans le programme. »    |
| 501  | NOT IMPLEMENTED      | « Cette fonction n'existe pas encore. »      |

*Mot compliqué du jour :* **code HTTP** = le numéro que le programme écrit
dans sa réponse pour dire si tout s'est bien passé ou non.

---

# Chapitre 29 — La fée des réponses : le GlobalExceptionHandler

On a vu au chapitre 23 que le `GlobalExceptionHandler` est le médecin des
erreurs. Maintenant, regardons **les fiches de diagnostic** qu'il renvoie,
parce qu'elles sont la clé pour comprendre une erreur.

### La fiche de diagnostic

Quand le médecin répond à une erreur, il envoie une petite fiche avec
plusieurs cases. Regarde cette classe : elle construit un objet
`ErrorMessageResponse` avec :

```
  {
    "timestamp" : "la date et l'heure de l'erreur",
    "error"     : "le nom du problème",
    "path"      : "quel chemin était demandé",
    "message"   : "le message gentil du médecin"
  }
```

### Les cas particuliers

Toutes les erreurs ne donnent pas la même fiche :

- **Les erreurs de validation** (champ manquant, trop long…) donnent une
  fiche spéciale qui liste chaque champ en erreur, avec la valeur qui a été
  refusée et pourquoi. C'est super pratique pour corriger !
- **Si on essaie de trier avec une colonne qui n'existe pas**, le médecin
  répond : « Impossible de trier avec la propriété X ».
- **Si on utilise une méthode interdite** (par exemple DELETE sur un chemin
  qui n'a pas de DELETE), il répond « METHOD_NOT_ALLOWED » (405).
- **Et si c'est une catastrophe inconnue**, le médecin attrape TOUTE erreur
  (`@ExceptionHandler(Exception.class)`) et répond 500 en écrivant aussi la
  trace dans les journaux (`log.error`).

```
   POURQUOI C'EST SI PRATIQUE ?
   Parce que le médecin est CENTRAL. Les services n'ont pas
   besoin de savoir comment répondre : ils lancent juste
   l'exception, et le médecin s'occupe du message.
```

*Mot compliqué du jour :* **trace d'erreur** (stacktrace) = la liste des
étapes que le programme a suivies avant de tomber, pour aider à trouver
le coupable.

---

# Chapitre 30 — Les erreurs qu'on rencontre souvent (et comment les lire)

Voici **les petits accidents les plus fréquents** dans notre projet, et
comment les comprendre quand on les voit dans le terminal ou dans le
navigateur.

### « 404 — Dossier non trouvé avec l'ID: 5 »

**Où on la voit :** quand on demande un dossier qui n'existe pas (ou plus).

**Ce que ça veut dire :** le programme a cherché dans sa base, et il n'a
rien trouvé avec cet ID. Souviens-toi aussi du chapitre 13 : pour certains
voyages de dossiers, le programme répond **volontairement** 404 pour ne
pas révéler qu'un dossier existe ailleurs. Parfois, un 404 est un secret
bien gardé !

### « 409 — Un dossier avec la référence 'ABC' existe déjà »

**Où on la voit :** dans `DossierServiceImplem.create`, quand on crée un
dossier avec une référence déjà utilisée.

**Ce que ça veut dire :** la référence est **unique** (elle doit être
différente pour chaque dossier). C'est comme deux élèves avec le même
numéro de carte d'étudiant : impossible !

### « 400 — Impossible de créer le dossier : aucune structure administrative trouvée »

**Où on la voit :** dans `resolveIdStructureAdministrative`.

**Ce que ça veut dire :** le programme n'a pas reçu de structure dans la
demande, et il a regardé l'utilisateur connecté (avec `SecurityUtils`)…
mais cet utilisateur n'a pas d'affectation dans la base. Il ne sait donc
pas où mettre le dossier au départ. Solution : vérifier que le
fonctionnaire a bien un poste et une affectation.

### « 401 — Unauthorized »

**Où on la voit :** dans le navigateur ou avec Postman quand on appelle
une route protégée sans badge.

**Ce que ça veut dire :** pas de JWT valable dans la requête. Vérifie
qu'on a bien mis le badge (le token) avec « Authorize » dans Swagger, ou
le header `Authorization: Bearer <token>`.

### « 403 — Access denied »

**Ce que ça veut dire :** le badge est présent et valable, mais il ne
contient pas le bouton (le rôle) qui permet cette action. Parfois il faut
créer le rôle dans Keycloak ou l'assigner au bon groupe (souviens-toi de
`TacheController`).

### « Le tri ne marche pas : Could not sort by property »

**Où on la voit :** dans la liste des dossiers (`GET /dossiers?sortedBy=...`).

**Ce que ça veut dire :** on a demandé un tri sur un champ qui n'existe
pas. Le médecin `GlobalExceptionHandler` attrape
`PropertyReferenceException` et répond 400 avec une explication claire.

### « 500 — An unexpected error occurred »

**Ce que ça veut dire :** un accident interne. Le médecin a attrapé une
exception qu'il ne connaissait pas. Le plus utile : regarder la **trace**
dans les journaux du terminal (elle commence souvent par
`java.lang.NullPointerException` ou autre). La trace te montre la ligne
exacte du problème : ton meilleur ami pour le corriger !

### Lire une trace d'erreur : l'exercice du détective

Quand le programme plante, il écrit une **trace** (la pile des étapes
suivies). Elle fait peur au début, mais c'est en fait une carte au trésor !
Regarde cet exemple (un peu raccourci) :

```
  java.lang.NullPointerException: Cannot invoke
      "String.length()" because "dto.getReference()" is null
      at DossierServiceImplem.create(DossierServiceImplem.java:45)
      at DossierController.create(DossierController.java:24)
      at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
      ...
```

Comment la lire ? En deux étapes :

1. **Première ligne** : `NullPointerException` et le message. On apprend
   immédiatement que quelque chose était `null` alors qu'on a essayé de
   l'utiliser (`dto.getReference()`).
2. **Les lignes suivantes** : la liste des appels. La ligne
   `at DossierServiceImplem.create(...:45)` dit : « c'est ici, à la ligne
   45 de ce fichier, que tout a commencé ». Plus la ligne est proche du
   haut, plus elle est proche de l'endroit du problème.

Le détective observe donc : **quoi** (le type d'erreur), **où** (le
fichier et la ligne), et **pourquoi** (le message). Et avec ça, il corrige !

*Mot compliqué du jour :* **journaux** (logs) = le petit carnet où le
programme écrit tout ce qu'il fait, pour qu'on puisse comprendre ce qui
s'est passé. On les voit défiler dans le terminal.

---


# PARTIE 9 — Comment démarrer le projet

Tu as lu toute l'histoire, et maintenant tu te dis : « j'ai envie de **voir
tourner** ce programme sur mon ordinateur ! ». Parfait, c'est exactement le
but de cette partie. On va préparer la maison, allumer la lumière, et faire
nos premiers tests.

---

# Chapitre 31 — Les outils qu'il faut dans sa boîte

Avant de faire tourner le projet, il faut préparer sa boîte à outils.
Voici les briques que tu dois avoir sur ton ordinateur.

### Java 17

Notre programme parle **Java**. La version 17 est écrite dans le
`pom.xml`. Vérifie avec cette commande :

```
    java -version
```

Tu dois voir quelque chose qui contient `17` (ou `21`, ça marche aussi
souvent). Si rien ne s'affiche, il faut installer Java 17 (par exemple la
distribution Eclipse Temurin, qu'on retrouve d'ailleurs dans le
`Dockerfile` !).

### Maven

C'est le robot qui achète les briques et lance le programme. Tu peux
vérifier :

```
    mvn -version
```

Mais bon, il y a un secret : le projet contient un fichier appelé
**`mvnw`** (le « Maven Wrapper »). C'est Maven qui vient tout seul avec le
projet, sans rien installer. On peut donc écrire `./mvnw` au lieu de `mvn` !

### Docker (pour la version emballée)

Si tu veux utiliser Docker (la boîte toute prête du chapitre 21), il faut
installer **Docker Desktop** et le lancer. Vérifie :

```
    docker --version
```

### PostgreSQL (le grand classeur)

Notre programme a besoin de la base de données. Regarde dans
`application.yml` où elle se trouve (adresse, nom de base, utilisateur,
mot de passe). Pour travailler en local, tu peux soit installer PostgreSQL,
soit lancer une petite boîte Docker avec la bonne configuration.

### Keycloak (le chef du personnel)

Le programme a besoin que Keycloak soit démarré et que le **realm** (le
pays des badges) `itas` existe. Sans Keycloak, impossible de se connecter
ou de créer des utilisateurs. C'est souvent l'élément qu'on oublie !

### Kafka (le facteur)

Et bien sûr le facteur : **Kafka** doit tourner pour que les messages
puissent circuler (et ZooKeeper / KRaft selon la version).

### Un outil pour tester (Postman ou Swagger)

Pour envoyer des demandes et voir les réponses, deux options :
- **Swagger** : intégré au projet (regarde `OpenApiConfig`) ;
- **Postman** : un programme à part pour tester les requêtes.

### La liste de contrôle avant de lancer

Voici une petite check-list pour ne rien oublier :

```
  [ ] Java 17 installé (java -version)
  [ ] Maven OK (ou le wrapper ./mvnw est là)
  [ ] PostgreSQL démarré (et les bons réglages dans application.yml)
  [ ] Keycloak démarré, realm "itas" prêt
  [ ] Kafka démarré
  [ ] (optionnel) Docker installé
  [ ] (optionnel) Postman installé
```

Coche les cases une par une, et tu verras : le démarrage devient un jeu
d'enfant.

*Mot compliqué du jour :* **wrapper** = une petite coquille qui enveloppe un
outil pour le rendre plus facile à utiliser. `mvnw` enveloppe Maven.

---

# Chapitre 32 — Allumer la maison : lancer le projet

Toutes les briques sont prêtes ? On allume la maison !

### Étape 1 : Démarrer les amis

Lance d'abord **PostgreSQL**, **Keycloak** et **Kafka**. Selon la
configuration de l'équipe, il peut y avoir un `docker-compose.yml` avec
déjà les bonnes boîtes. S'ils sont sur un autre ordinateur (comme
`192.168.20.14` dans l'exemple du projet), tu n'as rien à lancer : il faut
juste être sur le bon réseau.

### Étape 2 : Lancer le programme

Depuis le dossier du projet, tape :

```
    ./mvnw spring-boot:run
```

ou, si tu préfères fabriquer la boîte puis la lancer :

```
    ./mvnw clean package
    java -jar target/itas-utilisateur-service-0.0.1-SNAPSHOT.jar
```

Au démarrage, tu verras dans le terminal :

- le grand dessin du `banner.txt` (le mot « ITAS ») ;
- plein de lignes de journaux ;
- à la fin, quelque chose comme
  `Tomcat started on port 9000`.

**Félicitations, le programme est allumé !** Il écoute maintenant sur le
port 9000.

### Étape 3 : Ouvrir la documentation

Ouvre ton navigateur sur :

```
    http://localhost:9000/swagger-ui
```

C'est la vitrine de tous les réglages (grâce à `OpenApiConfig`). Tu peux
cliquer sur « Authorize » et coller un badge JWT pour tester les actions
protégées.

### Et avec Docker, comment ça se passe ?

Si l'équipe utilise Docker (souviens-toi de la recette du chapitre 21),
pas besoin de lancer Maven soi-même : on fabrique la boîte et on l'allume.

```
    docker build -t itas-utilisateur-ms .
    docker compose up -d
```

C'est exactement ce que fait le `Jenkinsfile` du robot Jenkins ! Mais pour
apprendre, `./mvnw spring-boot:run` est plus simple : ça démarre plus
vite, et on voit tous les journaux directement dans le terminal.

```
   À quoi ça ressemble pendant le démarrage ?

   .   ____          _            __ _ _
  /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
  ( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
  \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
   '  |____| .__|_| |_|_| |_\__, | / / / /
  =========|_|===============|___/=/_/_/_/
   :: Spring Boot ::               (v3.2.8)
```

*Mot compliqué du jour :* **port** = une porte d'entrée numérotée sur un
ordinateur. Le port 9000 est la porte par laquelle on frappe pour parler à
notre programme.

### Comprendre ce que dit le programme au démarrage

Pendant le démarrage, le terminal se remplit de lignes. Voici comment les
lire, parce que certaines sont de vraies mines d'or :

- **`Starting ItasUtilisateurApplication`** : le programme se prépare
  (c'est la classe principale, le bouton « ON » de la maison) ;
- **`Tomcat started on port 9000`** : « je suis prêt, frappe à ma porte ! »
  Tu peux alors ouvrir Swagger ;
- **`Schema migration: ...`** : le bricoleur `DossierSchemaMigration`
  vérifie et répare les tables (souviens-toi du chapitre 22) ;
- les lignes avec **`INFO`** : des informations normales, pas d'inquiétude ;
- les lignes avec **`WARN`** : des petites alarmes (souvent sans gravité,
  mais à lire quand même) ;
- les lignes avec **`ERROR`** : des problèmes ! Arrête-toi et lis.

Le démarrage est **réussi** quand tu vois que le serveur écoute sur le
port, sans grosse erreur en rouge. C'est le feu vert : l'atelier est
ouvert !

---

# Chapitre 33 — Les pièges du démarrage (et comment les éviter)

Même les grands explorateurs tombent parfois. Voici **les pièges les plus
classiques** au démarrage, et comment les déjouer.

### Piège 1 : « Le port 9000 est déjà utilisé »

Le programme ne peut pas s'ouvrir à sa porte, car quelqu'un d'autre l'a
déjà prise.

**Comment le déjouer :** trouver qui occupe le port (avec `lsof -i :9000`
sur Mac/Linux) ou changer de port dans `application.yml`. Si une ancienne
instance du programme tourne encore, l'arrêter.

### Piège 2 : « Connection refused » avec la base de données

Le programme ne trouve pas PostgreSQL à l'adresse indiquée.

**Comment le déjouer :** vérifier que PostgreSQL est bien démarré, et que
l'adresse, la base, l'utilisateur et le mot de passe du `application.yml`
sont corrects.

### Piège 3 : « Unable to connect to Keycloak »

Le chef du personnel est introuvable.

**Comment le déjouer :** vérifier que Keycloak est démarré, sur la bonne
adresse, et que le realm `itas` existe avec le client bien configuré. Sans
le bon secret du client, le programme ne peut pas parler à Keycloak.

### Piège 4 : Kafka ne répond pas

Les messages ne peuvent pas circuler.

**Comment le déjouer :** vérifier que Kafka est démarré et que l'adresse
du `application.yml` est la bonne. Un consumer qui ne trouve pas sa boîte
aux lettres peut ralentir ou planter le démarrage.

### Piège 5 : `Java 17 required` (ou une erreur de version)

Maven râle parce que la version de Java ne correspond pas à celle du
`pom.xml`.

**Comment le déjouer :** installer Java 17 (ou dire à Maven où il se
trouve). Vérifie avec `java -version` quelle version est utilisée.

### Piège 6 : les dépendances ne se téléchargent pas

Maven n'arrive pas à aller chercher les briques (pas de réseau, ou
proxy).

**Comment le déjouer :** vérifier la connexion Internet, ou configurer le
proxy dans le fichier `settings.xml` de Maven.

### Le réflexe du grand explorateur

Quand quelque chose ne va pas : **lis les journaux du terminal**. Le
programme dit presque toujours ce qui ne va pas. Cherche le mot
`ERROR` ou `Exception` et la ligne qui parle de notre projet (le paquet
`com.asystresources.itas.utilisateur`). C'est là que se cache le coupable !

*Mot compliqué du jour :* **configuration** = tous les réglages qui disent
au programme comment se comporter et où trouver ses amis.

---

# PARTIE 10 — Plus de profondeur par métier

Tu connais maintenant toute la maison. Dans cette dernière grande partie,
on va **creuser un peu plus profond** dans chaque métier, comme des petits
mineurs curieux : on va découvrir des détails précieux qui rendent ITAS
unique.

---

# Chapitre 34 — Plus profond : les comptes et les badges

On a vu au chapitre 5 comment fonctionnent les badges. Allons un peu plus
loin : que contient vraiment un badge, et comment le programme le lit-il ?

### Le contenu du badge (le JWT)

Un JWT est un petit texte en trois morceaux séparés par des points :

```
    en-tête.signe-corps.signature
    ─────── ───────────── ─────────
    1. type et manière de signer
    2. les informations (les "claims")
    3. la preuve que c'est authentique
```

Les **claims** (les informations) les plus importantes dans notre projet :

- **`sub`** : l'identifiant de la personne. C'est lui que `SecurityUtils`
  lit avec `getAuthenticatedUserId()` ;
- **`organisation`** : l'organisation de la personne (lu par
  `getOrganisation()`) ;
- les **`roles`** : les boutons du badge, qui deviennent les autorités du
  gardien grâce à `JwtAuthConverter`.

### Comment le programme sait qui demande ?

Regarde `SecurityUtils` : il va chercher dans le contexte de sécurité
(Spring Security) la personne connectée, prend son token JWT, et lit les
claims. C'est comme un agent qui vérifie le badge à l'entrée avant chaque
action.

### Le rôle des groupes chez Keycloak

Un utilisateur Keycloak appartient à des **groupes** (ses postes). Le
groupe détermine les **rôles** (les boutons). Quand un dossier voyage, le
programme vérifie que le fonctionnaire connecté a bien le droit de faire
l'action. C'est tout le système des permissions.

### Le petit secret du mot de passe

Dans `PasswordGenerator`, la méthode `generatePassword` construit
normalement un mot de passe aléatoire… mais la ligne qui renvoie `"123456"`
est active et le vrai code est en commentaire. En pratique, tous les
nouveaux comptes ont donc le mot de passe `123456` pour l'instant. C'est
très pratique pour tester, mais c'est un point à corriger avant la mise en
production (et à ne jamais mettre en production comme ça !).

*Mot compliqué du jour :* **claim** = une information écrite dans le badge,
par exemple « je m'appelle X » ou « mon organisation est Y ».

---

# Chapitre 35 — Plus profond : les équipes et les postes

Dans ITAS, les gens ne sont pas des robots isolés : ils appartiennent à des
**structures** (la pyramide du chapitre 10) et occupent des **postes**.
Creusons ce sujet.

### Les dix niveaux de la pyramide

Rappelle-toi `Constante`: il y a dix niveaux de structures, du niveau 1
(tout en haut) jusqu'au niveau 10 (tout en bas). Chaque structure a un
**parent** (le niveau juste au-dessus) sauf la toute première.

```
   Niveau 1  (le sommet)
     │
   Niveau 2
     │
   Niveau 3
     │
    ...
     │
   Niveau 10 (la base)
```

La règle du N+1 (chapitre 13) dit : « un dossier monte vers le parent
direct ». Cette règle est rendue possible par l'outil
`RelationNiveauStructure` : il connaît le parent de chaque niveau.

### Les postes (les fonctions)

Un **poste** est une fonction précise : directeur, chef de service,
inspecteur… Chez Keycloak, chaque poste est un **groupe**. En donnant un
groupe à un utilisateur, on lui donne automatiquement les boutons
(rôles) de ce poste.

### L'affectation : qui travaille où

L'**affectation** est le lien « qui travaille où ». Quand un dossier est
créé sans structure précisée, le programme demande à `SecurityUtils` qui
est l'utilisateur, puis cherche son affectation avec
`affectationRepository.findByUserKeycloakIdWithRelations(userId)`, et
utilise sa structure administrative comme point de départ (souviens-toi
du chapitre 25 : `resolveIdStructureAdministrative`).

### Le respect des règles : chaque pièce sait qui peut y travailler

Le programme vérifie sans arrêt que l'utilisateur qui agit a bien le bon
poste (par exemple avec `validateDossierBelongsToCurrentUser` dans la
circulation : si le dossier n'est pas chez cet utilisateur, réponse 404,
pour ne pas révéler d'information). Tout est fait pour que les papiers
n'aillent jamais dans les mauvaises mains.

*Mot compliqué du jour :* **affectation** = le lien qui dit quel
fonctionnaire travaille dans quelle structure, à quel poste.

---

# Chapitre 36 — Plus profond : les dossiers

On a visité la feature `dossier` au chapitre 25. Maintenant, découvrons les
**détails cachés** des dossiers.

### La référence unique

Chaque dossier a une **référence** unique (max 100 caractères). C'est son
numéro de série. Le programme vérifie avant la création :
`dossierRepository.existsByReference(...)` et refuse les doublons avec un
409. Comme deux billets d'avion avec le même numéro : interdit !

### Le type de dossier

Le champ `typeDossier` est une **énumération** (une liste de choix
fermée) : par exemple les types définis dans `Constante.TypeDossierAffecter`.
C'est comme une liste de cases à cocher imposée : on ne peut pas inventer
un type qui n'existe pas.

### Les dates

- **`dateCreation`** : obligatoire (`@NotNull`), posée à la création ;
- **`dateFin`** : optionnelle, posée quand le dossier se termine.

### La création déclenche la circulation

Le point le plus important : dans `create`, après avoir sauvegardé le
dossier, le programme appelle
`circulationDossierService.creerCirculationInitiale(saved, idStructureAdministrative)`.
Cela veut dire : **un dossier ne naît jamais sans voyage**. Dès sa
naissance, il a un point de départ et une boîte dans laquelle il attend.

### La pagination et le tri

La méthode `getAll` accepte des paramètres : `page`, `pageSize`,
`sortedBy`, `sortDirection`. C'est comme feuilleter un classeur : on
choisit la page, le nombre de lignes, et la colonne de tri. Attention aux
noms de colonnes : si on en donne un qui n'existe pas, le médecin répond
400 (on l'a vu au chapitre 30).

*Mot compliqué du jour :* **énumération** (enum) = une liste fermée de
choix possibles. Le programme ne peut choisir que parmi ces choix, ni plus,
ni moins.

---

# Chapitre 37 — Plus profond : la circulation des dossiers

La circulation est le cœur du système : le voyage du dossier. Creusons les
mécanismes internes.

### Les deux sens du voyage

- **Monter** : le dossier part de son bureau vers une structure au-dessus
  (c'est le transfert, chapitre 13). Il faut que le dossier soit **chez
  l'utilisateur** qui le transfère, et on connaît la structure suivante
  grâce à la règle N+1 (le parent direct) ;
- **Descendre** : le dossier redescend vers une structure au-dessous
  (chapitre 14). On précise alors la structure de destination.

### Les vérifications de sécurité

Regarde les méthodes du service de circulation :

- **`getCirculationActiveOrThrow`** : « donne-moi la circulation active du
  dossier, ou lance une erreur ». Il n'y a qu'**une seule** circulation
  active à la fois : le dossier est à un seul endroit, pas à deux ! C'est
  comme un objet précieux : il ne peut pas être chez deux personnes en même
  temps.
- **`validateDossierBelongsToCurrentUser`** : « vérifie que le dossier est
  bien chez l'utilisateur connecté ». Si ce n'est pas le cas, réponse 404
  (volontairement, pour ne pas révéler où se trouve le dossier).

### Le tracé du voyage

Chaque étape est **enregistrée** dans la table de circulation : quand le
dossier a été reçu, par qui, dans quelle structure, dans quel sens. C'est
comme le tampon qu'on met sur une lettre à chaque bureau qu'elle traverse.
À la fin, on peut raconter **toute l'histoire du dossier** : c'est
l'historique.

### Le statut qui change

À chaque étape, le **statut** du dossier est mis à jour (dans `Constante`
tu trouveras les statuts possibles, comme les étapes d'une course :
brouillon, soumis, rejeté, approuvé…). Le dossier avance d'étape en étape
jusqu'à son terme.

*Mot compliqué du jour :* **circulation active** = la seule position
actuelle du dossier. Il y en a toujours une seule, comme l'endroit où se
trouve une lettre en ce moment.

---

# Chapitre 38 — Plus profond : les contribuables et le secret OTP

Les contribuables sont les citoyens qui paient les impôts. Creusons la
machine à NIF et le code secret.

### Le NIF : le numéro d'identité fiscale

Chaque contribuable a un **NIF** : un numéro unique, comme un numéro de
sécurité sociale. Dans les controllers des contribuables, on trouve des
routes pour **vérifier un contribuable par son NIF** (c'est dans la
whitelist : tout le monde peut le faire sans badge, car cette information
est nécessaire à l'accueil du public).

### L'OTP : le code secret à 4 chiffres

Pour certaines actions sensibles, le contribuable doit prouver qu'il est
bien lui. Il reçoit un **OTP** : un code à 4 chiffres, généré par
`PasswordGenerator.generateOTP()`. Ce code est enregistré de façon sûre
(dans notre projet, **encodé avec BCrypt** : jamais en clair dans la
base). Le programme compare ce que le contribuable tape avec la version
encodée. S'ils correspondent, c'est bien lui.

```
   Le contribuable dit son NIF
            │
            ▼
   Le programme vérifie avec l'OTP (code à 4 chiffres)
            │
            ├── bon code → c'est bien lui → OK
            └── mauvais code → refus → 400/401
```

### Pourquoi encodé ?

Si un voleur volait la base de données, il ne verrait que des codes
**chiffrés**, illisibles. C'est une règle d'or de la sécurité : **ne jamais
garder les secrets en clair**. Même toi, tu ne peux pas « lire » le code
dans la base : tu ne peux que vérifier si celui qu'on tape correspond.

*Mot compliqué du jour :* **BCrypt** = une machine à coder les mots de
passe. Même si deux personnes ont le même mot de passe, le codage est
différent — et impossible à « décoder ».

---

# Chapitre 39 — Plus profond : les copies (déclarations et paiements)

Souviens-toi du chapitre 16 : quand un autre atelier crée une déclaration ou
un paiement, notre atelier en reçoit une **copie** par Kafka. Creusons ce
mécanisme.

### Pourquoi des copies ?

Chaque atelier de l'usine a **sa propre base de données**. Notre atelier
n'est PAS connecté à la base de l'atelier des déclarations. Alors comment
savoir si une déclaration existe ? Réponse : le facteur Kafka lui apporte
la nouvelle. Notre service garde une **copie locale** des déclarations et
paiements pour ses propres besoins (par exemple pour calculer le CCF).

### Le travail du consumer

Regarde un consumer (par exemple le consumer des contribuables) :

```
  1. Une lettre arrive dans la boîte (topic)
  2. Le consumer se réveille (l'étiquette @KafkaListener)
  3. Il lit le numéro dans le message
  4. Il vérifie dans SA base : est-ce que j'ai déjà ce numéro ?
  5. Si non : j'enregistre ma copie
     Si oui : j'ignore (je ne fais pas de doublon)
```

Cette vérification évite les doublons. Un message peut arriver deux fois
(Kafka aime parfois rejouer les messages !), mais la copie n'est créée
qu'une seule fois.

### Les événements : les sujets des lettres

Dans `KafkaTopics`, tu as vu `fonctionnaire-events` et `dossier-events`
(et d'autres topics définis dans `application.yml` pour les personnes
physiques, les contribuables, les exercices fiscaux, les paiements, les
déclarations, les dossiers…). Chaque sujet correspond à un type de
nouvelle : « un nouveau fonctionnaire ! », « une nouvelle déclaration ! »…

*Mot compliqué du jour :* **doublon** = une copie en double. Le programme
doit l'éviter, sinon le classeur serait plein de lignes identiques.

---

# Chapitre 40 — Plus profond : le Compte Courant Fiscal (CCF)

On a parlé du CCF au chapitre 17. Maintenant, voyons les détails qui le
rendent juste.

### Un compte par impôt

Le CCF n'est pas un seul compte : c'est **un compte pour chaque impôt**.
Souviens-toi des impôts listés dans `Constante`: **IRE** (impôt sur les
revenus), **PF** (professionnel forfaitaire), **IPV** (impôt sur les
plus-values), **TCAA** (taxe sur les véhicules / activités), **TPFL**…
Chaque impôt a sa petite colonne dans le compte du contribuable.

### Débit et crédit

Comme un compte bancaire, le CCF a deux colonnes :

- **Débit** : ce que le contribuable doit (les impôts calculés) ;
- **Crédit** : ce qu'il a payé (les paiements).

Le **solde** (ce qui reste dû) est la différence. Si on voit une
déclaration (une dette qui apparaît) et un paiement (une somme qui
disparaît), le CCF se met à jour.

### Les opérations tracées

Chaque mouvement du compte est une **opération** avec un type (dans
`Constante.TypeOperation`). On sait toujours si l'opération vient d'une
déclaration, d'un paiement, etc. C'est comme un relevé bancaire détaillé :
on peut retracer chaque mouvement.

### La copie locale

Rappelle-toi le chapitre 39 : notre atelier n'a pas la base de l'atelier
des paiements. C'est grâce aux **copies Kafka** des déclarations et
paiements que notre atelier peut **calculer le CCF**. Sans le facteur,
pas de CCF possible !

*Mot compliqué du jour :* **solde** = la différence entre ce qu'on doit et
ce qu'on a payé. Si le solde est positif, le contribuable doit encore
payer ; s'il est nul, il est à jour.

---

# PARTIE 11 — Le grand rendez-vous des questions (FAQ)

Tout le monde se pose les mêmes questions en arrivant. Dans cette partie,
on répond aux questions que les petits explorateurs posent le plus
souvent. Tu peux revenir ici quand tu doutes !

---

# Chapitre 41 — Les questions que tout le monde pose (première fournée)

### « Par où je commence pour lire le projet ? »

Bonne question ! Mon conseil :

1. Lis `application.yml` : c'est la carte de l'atelier (port, adresses
   des amis, boîtes aux lettres).
2. Ouvre Swagger : tu vois tout ce que le programme sait faire.
3. Suis une histoire simple : crée un dossier et regarde-le circuler.
4. Quand tu tombes sur un mot bizarre, viens voir le dictionnaire
   (chapitre 20) ou cette FAQ !

### « C'est quoi la différence entre une entité et un DTO ? »

- L'**entité** est la photo de la ligne du classeur (la base de données).
  Elle correspond exactement à une table.
- Le **DTO** est la fiche qu'on montre dehors ou qu'on reçoit de dehors.
  Il ne contient que ce qui doit voyager, et jamais les secrets internes.

Le **mapper** fait la traduction entre les deux. C'est comme la différence
entre ton dossier scolaire complet (entité) et la fiche de notes qu'on
montre aux parents (DTO) !

### « Pourquoi il y a un controller ET un service ? »

Pour **séparer les rôles** :

- le **controller** reçoit les demandes (les requêtes HTTP) et répond ;
- le **service** fait le vrai travail (les règles, la logique).

Si on mettait tout dans le controller, le fichier deviendrait énorme et
illisible. En séparant, chaque fichier a UNE seule mission. C'est comme
au restaurant : le serveur ne cuisine pas, le cuisinier ne sert pas !

### « C'est quoi `@RestController` ? »

C'est l'étiquette qui dit à Spring : « cette classe est un chef d'atelier,
elle répond aux demandes venant d'Internet ». Spring voit cette étiquette
et s'occupe de tout le reste automatiquement. Les étiquettes qui
commencent par `@` s'appellent des **annotations**.

### « C'est quoi une annotation ? »

Une **annotation** est une petite note écrite au-dessus du code, qui donne
des instructions à Spring. Par exemple `@Service` dit « cette classe fait
le travail », `@Repository` dit « cette classe parle à la base »,
`@Autowired` dit « donne-moi automatiquement l'outil dont j'ai besoin ».
C'est comme des post-it collés sur le code pour expliquer à Spring ce que
chaque pièce doit faire.

### « Spring, Spring Boot, Spring Security… c'est pareil ? »

Presque, mais pas tout à fait :

- **Spring** est la grande boîte d'outils (le socle) ;
- **Spring Boot** est la version toute prête, qui démarre vite (le robot
  qui allume le programme tout seul) ;
- **Spring Security** est la partie qui s'occupe du gardien et des badges ;
- **Spring Data JPA** est la partie qui parle avec la base de données.

C'est comme une même famille avec plusieurs cousins !

*Mot compliqué du jour :* **annotation** = une étiquette (`@...`) collée sur
le code pour donner des instructions à Spring. Le programme la lit au
démarrage.

---

# Chapitre 42 — Les questions que tout le monde pose (deuxième fournée)

### « Pourquoi Kafka ? Pourquoi pas juste une grande base pour tout le monde ? »

C'est une très bonne question ! L'usine ITAS est **énorme** : il y a plein
d'ateliers, chacun avec sa propre spécialité. Une seule base pour tout le
monde serait trop fragile : si elle tombe en panne, tout s'arrête.

Alors on a décidé que **chaque atelier garde ses propres souvenirs** (sa
propre base), et qu'ils se **préviennent mutuellement** par lettres
(Kafka) quand quelque chose d'important arrive. C'est plus solide, et
chaque atelier reste libre.

### « Comment je fais pour obtenir un badge (un JWT) pour tester ? »

Il faut te connecter à **Keycloak** avec un utilisateur qui existe, et
obtenir son **token**. Concrètement :

1. Va à l'adresse de Keycloak (par exemple
   `http://localhost:8089` ou celle de l'équipe) ;
2. Connecte-toi dans le realm `itas` avec un compte de test ;
3. Récupère le token (ou utilise la page « Admin » / un outil comme
   Postman) ;
4. Colle ce token dans Swagger avec « Authorize », ou mets-le dans le
   header `Authorization: Bearer <token>`.

L'équipe a sûrement un compte de démonstration à te donner.

### « Le mot de passe de test est vraiment 123456 ? »

Pour l'instant, oui : `PasswordGenerator` renvoie toujours `"123456"` (la
vraie génération aléatoire est en commentaire). C'est pratique pour
développer, mais **il ne faut jamais laisser ça en production**. C'est un
de ces « dette technique » qu'on doit corriger un jour — note-le dans ta
tête !

### « C'est quoi une dette technique ? »

Quand on code « vite fait » pour avancer (comme le mot de passe 123456),
ça crée une **dette** : un problème qu'il faudra réparer plus tard, comme
une dette d'argent. Le projet fonctionne, mais on devra « rembourser » un
jour en corrigeant. C'est normal dans tous les projets !

### « Comment je sais si mon code marche ? »

Trois vérifications simples :

1. **Le programme démarre** sans erreur dans le terminal ;
2. **Swagger répond** : tu peux tester les actions ;
3. **Les tests** : lance `./mvnw test` et regarde si tout est vert.

Attention, notre projet a très peu de tests pour l'instant (on l'a vu :
le Jenkinsfile ne lance pas de tests). C'est un point d'amélioration.

### « C'est quoi le secret d'un bon débutant ? »

Cacher ses erreurs ? Non ! Le secret, c'est de **lire les journaux**, de
**poser des questions** (comme tu le fais !) et de **tester petit à
petit**. Personne ne connaît tout d'un coup. Même les grands chefs ont
commencé par un premier « Bonjour ! ».

### « Comment je relis un code que je ne comprends pas ? »

C'est une excellente question, car c'est LE geste de tous les jours.
Voici ma recette en 5 étapes :

1. **Lis le nom** du fichier et la classe : devine son rôle.
2. **Regarde les annotations** (`@RestController`, `@Service`,
   `@Repository`…) : elles disent ce que la classe est.
3. **Lis les méthodes du haut vers le bas** : le controller d'abord
   (il est court), puis le service.
4. **Note les mots inconnus** et va voir le dictionnaire (chapitre 20).
5. **Essaie de l'utiliser** : un exemple qui marche vaut mille lectures.

Et si tu es vraiment bloqué, demande à un collègue de te montrer une fois,
de visu. Ensuite, fais-le tout seul : c'est comme apprendre à faire du
vélo, ça s'apprend en pédalant !

*Mot compliqué du jour :* **dette technique** = un petit raccourci pris
dans le code qu'il faudra réparer plus tard. Comme une petite dette à
rembourser.

---

# PARTIE 12 — Le grand quiz du petit explorateur

Avant de fermer le livre, un petit **jeu** ! Voici des questions pour
vérifier ce que tu as appris. Essaie de répondre sans regarder les
réponses… puis tourne au chapitre 44 pour vérifier. Bon courage !

---

# Chapitre 43 — Les questions du quiz

### Question 1 — Le rôle

Notre microservice `itas-gestion-utilisateur-service` sert principalement
à :
a) cuisiner des repas pour les fonctionnaires ;
b) gérer les utilisateurs, les dossiers et la circulation des papiers ;
c) compter les étoiles dans le ciel.

### Question 2 — Les quatre briques

Quels sont les « quatre briques magiques » qui aident notre projet ?
a) Maven, Docker, Git, Jenkins ;
b) PostgreSQL, Kafka, Keycloak et Spring Boot ;
c) HTML, CSS, JavaScript, Python.

### Question 3 — Le badge

Qu'est-ce qu'un JWT ?
a) Une boîte de jus d'orange ;
b) Un badge numérique qui prouve qui on est ;
c) Un type de table de base de données.

### Question 4 — Le gardien

Qui vérifie que tout le monde a bien un badge avant d'entrer ?
a) Le `DossierController` ;
b) `Spring Security` (le gardien) avec sa whitelist ;
c) Le facteur Kafka.

### Question 5 — Le facteur

À quoi sert Kafka dans notre histoire ?
a) À envoyer et recevoir des messages entre les ateliers ;
b) À imprimer les reçus fiscaux ;
c) À démarrer le serveur.

### Question 6 — Le classeur

Où le programme range-t-il ses souvenirs ?
a) Dans la boîte aux lettres ;
b) Dans la base de données PostgreSQL ;
c) Dans le badge.

### Question 7 — Le voyage du dossier

Quand un dossier monte d'un étage, où va-t-il ?
a) N'importe où, au hasard ;
b) Chez son parent direct (la règle N+1) ;
c) Dans la poubelle.

### Question 8 — Les codes d'erreur

Que veut dire le code 404 ?
a) Tout va bien ;
b) La chose demandée n'a pas été trouvée ;
c) Le programme a planté gravement.

### Question 9 — Le code 409

Quand renvoie-t-on un 409 (CONFLICT) ?
a) Quand on crée un dossier avec une référence déjà existante ;
b) Quand le badge est périmé ;
c) Quand le serveur tombe en panne.

### Question 10 — Le CCF

Que signifie « CCF » ?
a) Code Caché de Fonction ;
b) Compte Courant Fiscal : le relevé des impôts du contribuable ;
c) Centre de Calcul Fiscal.

### Question 11 — Le médecin

Quel fichier s'occupe de répondre gentiment aux erreurs ?
a) `PasswordGenerator` ;
b) `GlobalExceptionHandler` (le médecin chef) ;
c) `schema.sql`.

### Question 12 — L'OTP

À quoi sert le code OTP à 4 chiffres ?
a) À ouvrir le port 9000 ;
b) À prouver que le contribuable est bien lui ;
c) À trier les dossiers.

### Question 13 — Le port

Sur quel port notre programme écoute-t-il par défaut ?
a) 80 ;
b) 8080 ;
c) 9000.

### Question 14 — Le coupable

Quand on voit une erreur 500, où regarde-t-on en premier ?
a) Dans la base de données ;
b) Dans les journaux du terminal (la trace) ;
c) Dans le badge.

### Question 15 — La copie

Pourquoi notre atelier garde-t-il des copies des déclarations ?
a) Pour faire joli ;
b) Parce qu'il n'a pas la base des autres ateliers, et Kafka lui apporte
   les nouvelles ;
c) Pour les revendre.

---

# Chapitre 44 — Les réponses du quiz

Voici les réponses, avec la petite explication et le chapitre où tu peux
revoir la leçon si besoin.

**Réponse 1 : b.** Notre microservice gère les utilisateurs, les dossiers et
leur circulation. (Chapitres 2 et 3.)

**Réponse 2 : b.** PostgreSQL, Kafka, Keycloak et Spring Boot sont les
quatre briques. (Chapitre 4.)

**Réponse 3 : b.** Le JWT est le badge numérique qui prouve qui on est.
(Chapitre 5.)

**Réponse 4 : b.** Spring Security est le gardien, avec sa whitelist.
(Chapitre 6.)

**Réponse 5 : a.** Kafka transporte les messages (les lettres) entre les
ateliers. (Chapitre 8.)

**Réponse 6 : b.** La base de données PostgreSQL est le grand classeur.
(Chapitre 4.)

**Réponse 7 : b.** Le dossier monte chez son parent direct : la règle N+1.
(Chapitre 13.)

**Réponse 8 : b.** 404 = « non trouvé ». (Chapitre 28.)

**Réponse 9 : a.** 409 = conflit, par exemple une référence de dossier déjà
utilisée. (Chapitres 28 et 30.)

**Réponse 10 : b.** CCF = Compte Courant Fiscal. (Chapitre 17.)

**Réponse 11 : b.** `GlobalExceptionHandler` est le médecin chef des
erreurs. (Chapitres 23 et 29.)

**Réponse 12 : b.** L'OTP prouve que le contribuable est bien lui.
(Chapitres 15 et 38.)

**Réponse 13 : c.** Le port 9000. (Chapitre 32.)

**Réponse 14 : b.** On regarde la trace dans les journaux du terminal.
(Chapitres 30 et 33.)

**Réponse 15 : b.** On garde des copies locales car chaque atelier a sa
propre base, et c'est Kafka qui apporte les nouvelles. (Chapitres 16 et
39.)

### Combien as-tu trouvé ?

- **13 à 15 bonnes réponses** : Wouah ! Tu es prêt à explorer le code tout
  seul. Bravo !
- **8 à 12** : Très bien ! Relis les chapitres où tu t'es trompé, puis
  rejoue.
- **Moins de 8** : Pas grave du tout ! Chaque lecture te rend plus fort.
  Refais le quiz dans quelques jours, tu verras la différence.

*Mot compliqué du jour :* **quiz** = un petit jeu de questions pour vérifier
ce qu'on a appris. Se tromper, c'est apprendre !

---

# PARTIE 13 — Les secrets des petits développeurs

La théorie, c'est bien. Mais les **petites astuces des pros**, c'est encore
mieux ! Dans cette dernière partie, on partage les habitudes qui rendent
le code plus propre, les commandes qui font gagner du temps, et un petit
plan d'entraînement pour continuer tout seul.

---

# Chapitre 45 — Les bonnes habitudes (les astuces des pros)

En regardant le code du projet, tu as peut-être remarqué des petites choses
répétées. Ce sont **les habitudes** des développeurs qui ont écrit ce
projet. Voici comment les lire et les imiter.

### Habitude 1 : faire confiance à Lombok

Regarde une classe comme `DossierServiceImplem`. Elle est toute petite à
écrire, pourtant elle fait beaucoup de choses. Le secret : les
annotations de **Lombok** :

- `@RequiredArgsConstructor` : crée tout seul le constructeur qui donne au
  service ses outils (le repository, le mapper…) ;
- `@Slf4j` : ajoute un petit carnet `log` pour écrire dans les journaux ;
- `@Getter` / `@Setter` (sur les entités comme `Dossier`) : créent les
  méthodes « lis-moi » et « change-moi » de chaque champ.

Grâce à Lombok, on écrit **beaucoup moins de code** (Maven va chercher
cette brique dans le `pom.xml`). Mais attention : Lombok fait son travail
**quand on compile**. Dans ton éditeur, pense à activer le traitement des
annotations pour que tout fonctionne.

### Habitude 2 : écrire des journaux à chaque étape

Regarde encore `DossierServiceImplem` :

```
  log.info("create() appelé - reference={}", dto.getReference());
  log.warn("Référence déjà existante - reference={}", dto.getReference());
  log.info("Dossier créé avec succès - id={}", saved.getId());
```

Le développeur écrit ce qu'il fait (`info`), ce qui l'inquiète (`warn`), et
crie quand ça casse (`error`). Pourquoi ? Parce qu'un jour, quelqu'un
(peut-être toi !) devra comprendre ce qui s'est passé. Les journaux sont la
**mémoire du programme**.

### Habitude 3 : découper en petites méthodes

La méthode `create` de `DossierServiceImplem` est courte et lisible. Et le
calcul de la structure administrative est rangé dans sa propre petite
méthode privée (`resolveIdStructureAdministrative`). Chaque méthode fait
**une seule chose**. Si une méthode devient longue, les pros la découpent.

### Habitude 4 : utiliser les transactions

Regarde l'étiquette `@Transactional` sur le service. Elle dit à Spring :
« toutes les opérations de base de données de cette méthode doivent réussir
ENSEMBLE, ou échouer ENSEMBLE ». Si la deuxième étape plante, la première
est annulée. C'est comme préparer un gâteau : si le four explose au
milieu, on ne laisse pas la moitié de la pâte au frigo !

La variante `@Transactional(readOnly = true)` (sur `getById` et `getAll`)
dit : « je ne vais que lire, pas écrire ». C'est plus rapide et plus
sûr.

### Habitude 5 : valider ce qu'on reçoit

Les DTO de création (comme `DossierCreateDto`) portent des étiquettes de
validation : `@NotNull`, `@NotBlank`, `@Size(max=100)`. Et le controller
écrit `@Valid` devant la demande. Résultat : si quelqu'un envoie une fiche
mal remplie, le médecin `GlobalExceptionHandler` répond une belle liste
d'erreurs (on l'a vu au chapitre 29). On refuse le travail sale dès
l'entrée !

### Habitude 6 : ne jamais mettre les secrets dans le code

Dans `application-email.properties`, tu as vu un **mot de passe en clair**
(`Asyst@2024`) et une adresse email. C'est une mauvaise habitude de
sécurité : ces fichiers risquent d'être partagés. Les pros cachent les
secrets dans des variables d'environnement (`${MAIL_PASSWORD}`). Retiens
cette règle : **les secrets ne vont jamais dans le code** (ni dans le
`pom.xml`, ni dans les configs, ni dans Git !).

### Habitude 7 : donner des noms qui parlent

Regarde les méthodes : `creerCirculationInitiale`,
`getCirculationActiveOrThrow`, `resolveIdStructureAdministrative`… Chaque
nom dit EXACTEMENT ce que fait la méthode. Les pros adorent ça, parce que
lire le code devient comme lire une histoire. Astuce : si tu ne sais pas
comment nommer une méthode, c'est qu'elle fait peut-être deux choses —
découpe-la !

### Habitude 8 : garder les fichiers petits

Un fichier qui fait 3000 lignes, c'est dur à lire. Le projet est
construit en **petits fichiers spécialisés** (un controller court, des
services découpés, des DTO minuscules). Quand tu ajoutes du code, pose-toi
la question : « est-ce que je peux le ranger dans un fichier séparé plus
clair ? ». Ta future toi/toi te remerciera !

*Mot compliqué du jour :* **transaction** = un groupe d'opérations qui
réussissent toutes ensemble ou échouent toutes ensemble. On ne laisse
jamais le travail « à moitié fait ».

---

# Chapitre 46 — Les commandes qui font gagner du temps

Voici un petit carnet de **commandes magiques** à garder près de toi.
Elles te feront gagner un temps précieux.

### Pour le projet (Maven)

```
    ./mvnw spring-boot:run      # lancer le programme
    ./mvnw clean package        # fabriquer le programme (le JAR)
    ./mvnw test                 # lancer les tests
    ./mvnw clean                # nettoyer le dossier target
```

### Pour Git (ranger ses fichiers)

```
    git status                  # voir ce qui a changé
    git add <fichier>           # ajouter un fichier au paquet
    git commit -m "message"     # ranger le paquet avec un mot
    git push                    # envoyer chez les autres
    git pull                    # récupérer le travail des autres
    git log --oneline -10       # voir les 10 derniers rangements
```

Règle d'or : on **ne pousse pas** n'importe quoi. On regarde d'abord
`git status`, puis `git diff` pour relire ses changements.

```
    EXEMPLE DE PETITE SÉANCE GIT
    git status              → je vois mes fichiers modifiés
    git add DossierServiceImplem.java
    git commit -m "fix: garder la structure quand on crée un dossier"
    git push                → j'envoie mon travail
```

Pense à écrire des messages de commit **clairs et courts** : dans quelques
mois, quelqu'un (peut-être toi !) lira ces messages pour comprendre
l'histoire du projet.

### Pour Docker (les boîtes)

```
    docker compose up -d        # allumer les boîtes du fichier
    docker compose ps           # voir les boîtes qui tournent
    docker compose down         # éteindre les boîtes
    docker logs <nom>           # voir les journaux d'une boîte
```

### Pour tester avec un outil (curl)

`curl` est un petit robot qui envoie des demandes depuis le terminal :

```
    curl http://localhost:9000/...          # envoyer une demande
    curl -X POST http://localhost:9000/...  # demander une création
    curl -H "Authorization: Bearer <token>" ...   # avec son badge
```

### Pour inspecter le port (sur Mac/Linux)

```
    lsof -i :9000               # qui occupe le port 9000 ?
```

*Mot compliqué du jour :* **JAR** = le paquet tout prêt du programme Java,
fabriqué par Maven. On peut le lancer avec `java -jar`.

---

# Chapitre 47 — Ton plan d'entraînement (par où continuer)

Tu es au bout du livre… mais c'est en fait le **début** de ton aventure !
Voici un plan d'entraînement, étape par étape, pour devenir autonome.

### Étape 1 : manipule le projet (1 à 2 jours)

1. Démarre le projet (Partie 9) et fais-toi plaisir avec **Swagger** :
   regarde les réglages, les descriptions, les boutons.
2. Essaie de **créer un dossier** avec la bonne structure.
3. Essaie de **lister les dossiers** avec des tris différents.
4. Envoie une demande **sans badge** : observe la réponse (401).

### Étape 2 : suis le code d'une histoire (2 à 3 jours)

Prends une action simple (créer un dossier) et suis-la **dans le code** :

```
  controller  →  service  →  repository  →  base de données
        │
        ▼
  mapper (DTO ↔ entité)  et  circulation
```

N'hésite pas à mettre des « points d'arrêt » dans ton éditeur (IntelliJ ou
VS Code) : le programme s'arrête là et tu peux regarder les valeurs.
C'est le super-pouvoir des développeurs !

### Étape 3 : améliore quelque chose de petit (3 à 5 jours)

Par exemple :

- corrige `PasswordGenerator` pour renvoyer vraiment un mot de passe
  aléatoire (au lieu de `123456`) ;
- cache le mot de passe email dans une variable d'environnement ;
- ajoute un `log.info` manquant dans un service ;
- crée une petite route toute simple qui dit « Bonjour ! ».

Rien de grand. Le but est de **modifier quelque chose, le lancer, et voir
le résultat**. C'est comme ça qu'on apprend !

### Étape 4 : écris ton premier test (1 semaine)

Le projet a très peu de tests. Écris un test pour le service des dossiers :
« créer un dossier, puis vérifier qu'on peut le retrouver ». Lance
`./mvnw test` et regarde-le passer (en vert !). Tu viens de faire un pas
de géant.

### Le message des pros

Personne ne comprend tout le code d'un coup. On lit un morceau, on le
manipule, on le casse, on le répare. **Casser, c'est apprendre.** Et
chaque question que tu poses (comme dans ce livre !) te rend plus fort.

Allez, à toi de jouer, petit explorateur ! L'usine ITAS t'attend.

*Mot compliqué du jour :* **point d'arrêt** (breakpoint) = un endroit où tu
dis au programme « arrête-toi ici pour que je regarde ». C'est le
super-pouvoir du débogage.

---

# Chapitre 48 — Le grand récapitulatif (tout le livre en quelques pages)

Avant de fermer le livre, un **grand récapitulatif** : tout ce qu'il faut
retenir, en quelques pages. C'est la fiche de secours à relire dans un
moment de doute !

### L'essentiel en une phrase

**ITAS est une usine qui gère les impôts ; notre projet est un atelier qui
gère les utilisateurs, les dossiers et leur voyage entre les structures.**

### Les personnages (les briques)

| Personnage  | Vrai nom             | Son travail                                  |
|-------------|----------------------|----------------------------------------------|
| Le classeur | PostgreSQL           | Ranger les souvenirs (la base de données)    |
| Le facteur  | Kafka                | Transporter les messages entre ateliers      |
| Le chef     | Keycloak             | Créer et garder les badges (les comptes)     |
| Le chef d'atelier | Spring Boot    | Allumer le programme et gérer les requêtes   |
| Le gardien  | Spring Security      | Vérifier les badges à l'entrée               |
| Le badge    | JWT                  | La carte d'identité numérique                |

### Les 5 grands mouvements

1. **Se connecter** : le badge JWT est vérifié par le gardien.
2. **Créer un dossier** : le dossier naît et sa circulation initiale est
   créée.
3. **Faire circuler** : le dossier monte (parent direct, règle N+1) ou
   descend, avec une seule circulation active.
4. **Recevoir les nouvelles** : le facteur Kafka apporte les copies
   (contribuables, déclarations, paiements…) pour garder la base à jour.
5. **Calculer le CCF** : avec les déclarations et les paiements, le compte
   du contribuable se met à jour (par impôt).

### Les 6 réflexes du développeur

1. **Lis les journaux** du terminal : le programme dit ce qui ne va pas.
2. **Découpe ton code** : petites méthodes, petits fichiers, noms clairs.
3. **Valide à l'entrée** : les DTO et `@Valid` filtrent les mauvaises
   demandes.
4. **Ne mets jamais de secrets en clair** : variables d'environnement !
5. **Teste petit à petit** : modifie, lance, observe.
6. **Pose des questions** : c'est comme ça qu'on apprend le plus vite.

### Le vocabulaire de survie

- **Controller** : le chef qui reçoit les demandes.
- **Service** : le cuisinier qui fait le travail.
- **Repository** : le garde-manger qui parle au classeur.
- **Entity** : la fiche de la ligne du classeur.
- **DTO** : la fiche de transport entre les pièces.
- **Mapper** : le traducteur entre entity et DTO.
- **Exception** : l'alarme quand quelque chose va mal.
- **GlobalExceptionHandler** : le médecin qui répond aux erreurs.
- **Topic** : la boîte aux lettres de Kafka.
- **Consumer / Producer** : celui qui reçoit / celui qui envoie.
- **OTP** : le code secret à 4 chiffres pour vérifier le contribuable.
- **NIF** : le numéro d'identité fiscale du contribuable.
- **CCF** : le compte courant fiscal (ce qui est dû, impôt par impôt).

### La carte des codes HTTP

```
   200  OK            tout va bien
   201  CREATED       la chose a été créée
   204  NO CONTENT    c'est fait (rien à montrer)
   400  BAD REQUEST   ta demande est mal écrite
   401  UNAUTHORIZED  pas de badge (ou invalide)
   403  FORBIDDEN     badge présent, mais pas le droit
   404  NOT FOUND     la chose n'existe pas
   405  METHOD NOT ALLOWED   action impossible ici
   409  CONFLICT      la chose existe déjà
   500  SERVER ERROR  problème interne au programme
```

### Et maintenant ?

Tu as TOUT ce qu'il faut pour commencer : l'histoire, la carte des
fichiers, les erreurs, le démarrage, la FAQ, le quiz. Reviens quand tu
veux, ce livre sera toujours là.

Bonne aventure dans l'usine ITAS, petit explorateur ! Tu vas adorer.

*Mot compliqué du jour :* **récapitulatif** = un résumé qui regroupe
l'essentiel au même endroit, pour se souvenir plus facilement.

---

# Chapitre 20 — Le dictionnaire du petit explorateur

Bravo, tu as parcouru tout le livre ! Voici ton **dictionnaire de poche** :
tous les mots compliqués, expliqués simplement, pour quand tu les
retrouveras dans le projet.

**A**
- **Affectation** : le lien « qui travaille où, à quel poste ».
- **Authentification** : prouver qui on est (avec son badge).

**B**
- **Base de données** : le grand classeur où le programme range ses souvenirs.
- **Badge / JWT** : la carte d'identité numérique qui prouve qui tu es.

**C**
- **CCF (Compte Courant Fiscal)** : le relevé de compte du contribuable.
- **Consumer** : celui qui LIT les messages dans Kafka.
- **Controller** : le chef d'atelier qui reçoit les demandes et les dirige.
- **Circulation** : le voyage d'un dossier de bureau en bureau.

**D**
- **Dossier** : une demande d'un citoyen (immatriculation, recours…).
- **Déclaration** : ce que le contribuable annonce (ses revenus, ses ventes).

**E**
- **Entrepôt** : voir Base de données.
- **Événement / Message** : une lettre que Kafka transporte.

**F**
- **Feature** : un tiroir du projet pour une fonctionnalité précise.
- **Fonctionnaire** : une personne qui travaille dans l'administration.

**G**
- **Groupe (Keycloak)** : une équipe. Règle : un poste = un groupe.

**H**
- **HTTP** : la façon dont les ordinateurs se parlent sur Internet.

**J**
- **JWT** : le badge numérique signé par Keycloak.

**K**
- **Kafka** : le facteur de l'usine qui transporte les messages.
- **Keycloak** : le chef du personnel, fabricant des badges.

**M**
- **Microservice** : un tout petit programme indépendant.
- **N+1 / N-1** : le bureau juste au-dessus / juste en dessous.

**N**
- **NIF** : le numéro fiscal unique d'un contribuable.
- **Niveau** : l'étage d'une structure (de 1 à 10).

**O**
- **OTP** : le code secret à 4 chiffres pour prouver qu'on est le propriétaire.

**P**
- **Pénalité de retard** : l'amende quand on paie après la date.
- **Producer** : celui qui ÉCRIT les messages dans Kafka.
- **Poste** : le travail d'une personne (avec un code et des dates).
- **PostgreSQL** : l'entrepôt à souvenirs.
- **Publier** : déposer une lettre dans une boîte Kafka.

**R**
- **Rôle** : un droit donné à une personne.
- **Repository** : le garde-manger qui fournit les données à l'ouvrier.

**S**
- **Service** : l'ouvrier qui fait le vrai travail.
- **SMTP** : le robot qui envoie les emails.
- **Spring Security** : le gardien de l'entrée.
- **Structure administrative** : un bureau de la pyramide.

**T**
- **Topic** : une boîte aux lettres Kafka.
- **Transfert** : faire monter le dossier d'un étage.

**Par où continuer ?**
1. Lis le fichier `application.yml` : c'est la « carte » de l'atelier
   (portes, boîtes aux lettres, adresses).
2. Ouvre `Swagger` (catalogue des services) pour voir toutes les actions
   possibles.
3. Suis un scénario simple dans le code : crée un dossier et regarde-le
   circuler.
4. N'aie pas peur des mots compliqués : ce sont juste des noms de robots !

**Le mot de la fin :** un grand système, c'est plein de petites pièces qui
travaillent ensemble — comme un orchestre. Toi aussi, bientôt, tu feras partie
de l'orchestre. Bienvenue dans l'équipe ITAS ! 🎉

---

*Fin du livre. Rédigé pour t'expliquer le projet
`itas-gestion-utilisateur-service` simplement, sans prérequis technique.*
