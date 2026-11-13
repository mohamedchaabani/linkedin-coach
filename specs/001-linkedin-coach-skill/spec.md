# Feature Specification: LinkedIn Coach — skill open source pour Claude

**Feature Branch**: `001-linkedin-coach-skill`

**Created**: 2026-11-12

**Status**: Draft

**Input**: User description: "spec-linkedin-coach.md" (spécification fonctionnelle fournie à la racine du projet)

## Contexte

Les skills LinkedIn existants pour Claude sont soit génériques, soit dépendants de services
tiers payants (scraping, publication automatique). Les deux meilleurs projets open source
(sergebulaev/linkedin-skills et Jakeschincariol/linkedin-agent-skill, licence MIT) apportent
chacun une moitié de la réponse : le premier les formules d'accroche et les règles de
publication récentes, le second la grille de notation du profil et l'humanizer.

LinkedIn Coach fusionne le meilleur des deux dans un seul skill gratuit, open source, sans
dépendance payante, avec un objectif unique : **être trouvé et contacté par des recruteurs et
des clients**. Un dépôt public permet à n'importe qui de l'installer en quelques minutes et de
l'utiliser avec Claude Code ou dans l'app Claude.

**Utilisateurs cibles** : professionnels (tech en priorité) qui veulent être plus visibles des
recruteurs ; utilisateurs de Claude Code sous macOS, Windows ou Linux ; utilisateurs de l'app
Claude (web, desktop, iPhone/iPad, Android) qui n'utilisent pas Claude Code.

## Clarifications

### Session 2026-11-12

- Q: Le skill doit-il être livré comme un seul skill multi-modes ou comme un pack de skills
  séparés ? → A: Un seul skill `linkedin-coach`, trois modes (AUDIT, AMÉLIORER, POSTS),
  références chargées à la demande.
- Q: En v1, le skill peut-il modifier le profil via le navigateur connecté, ou seulement
  produire du texte à copier ? → A: Lecture et écriture via le navigateur ; chaque
  modification du profil est appliquée seulement après validation explicite, action par
  action. La publication de posts reste exclue (FR-056).
- Q: Dans l'app Claude, comment le positionnement est-il conservé entre les conversations ?
  → A: Le skill fournit un bloc de positionnement à coller une fois dans les instructions
  d'un projet Claude dédié ; hors projet, le bloc est recollé en début de conversation.
- Q: Le skill garde-t-il un historique des audits pour montrer la progression ? → A: Oui,
  historique réduit (date, note /100, note /20, 3 corrections prioritaires), comparé au
  dernier audit ; dans l'app Claude, sous forme de résumé à coller dans le projet dédié.

### Session 2026-11-13 (après la release 0.1.0)

- Q: Faut-il des commandes explicites en plus du déclenchement en langage naturel ? → A:
  Oui, quatre commandes Claude Code (`/linkedin-coach:audit`, `:improve`, `:post`,
  `:positioning`) qui lancent le skill dans le mode correspondant (FR-008). L'app Claude
  reste en langage naturel.
- Q: Une section non vue lors de la lecture dans le navigateur peut-elle être notée 0 ? →
  A: Non. Constaté en réel : LinkedIn charge Infos, Sélection et Compétences principales en
  différé ; un audit lu trop tôt les a notées absentes (54/100 au lieu de 79/100). Une
  section n'est notée 0 que si son absence est confirmée ; sinon « non évaluée » et question
  à l'utilisateur (FR-016).
- Q: Le README doit-il montrer un exemple ? → A: Oui, un avant/après **réel** (profil de
  l'auteur, employeurs anonymisés, chiffres fournis par l'auteur) et les prochaines
  corrections proposées ; jamais d'exemple inventé (FR-009).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Installer le skill (Priority: P1)

L'utilisateur installe le skill en une commande, ou en important un fichier, sur son système,
et peut l'utiliser sans configuration compliquée.

**Why this priority**: Sans installation simple, aucune autre valeur n'est accessible ; c'est
aussi le premier contact avec le projet open source.

**Independent Test**: Sur une machine vierge de chaque plateforme, suivre le README, installer
le skill et vérifier qu'il apparaît dans la liste des skills disponibles.

**Acceptance Scenarios**:

1. **Given** Claude Code installé sur macOS, Windows ou Linux, **When** l'utilisateur ajoute
   la source du skill puis l'installe via le système de plugins, **Then** le skill apparaît
   dans la liste des skills en moins de 2 minutes.
2. **Given** un utilisateur de l'app Claude, **When** il importe l'archive de la dernière
   release dans les paramètres Skills, **Then** le skill se déclenche sur la demande
   « audite mon profil LinkedIn » sur web, desktop et mobile.
3. **Given** un utilisateur qui préfère l'installation manuelle, **When** il copie le dossier
   du skill dans le répertoire de skills documenté pour son OS, **Then** le skill est reconnu
   au lancement suivant.

---

### User Story 2 - Configurer mon positionnement (Priority: P1)

Au premier lancement, le skill pose au plus 7 questions (rôle, expertises, certifications,
cible, langue…) et enregistre les réponses pour adapter tous les conseils au profil.

**Why this priority**: Toutes les notes, réécritures et posts dépendent du positionnement ;
sans lui, les conseils sont génériques et le principe « zéro invention » ne peut pas être tenu.

**Independent Test**: Lancer le skill sans positionnement enregistré, répondre aux questions,
relancer une nouvelle session et vérifier que les questions ne sont plus posées.

**Acceptance Scenarios**:

1. **Given** aucun positionnement enregistré, **When** l'utilisateur sollicite le skill,
   **Then** le skill pose au maximum 7 questions avant tout audit, réécriture ou post.
2. **Given** un positionnement enregistré, **When** l'utilisateur dit « mets à jour mon
   positionnement », **Then** le skill montre les valeurs actuelles et ne modifie que celles
   que l'utilisateur change.
3. **Given** une réponse laissée vide, **When** le skill enregistre le positionnement,
   **Then** la valeur est marquée « à confirmer » et n'est jamais remplacée par une
   supposition.
4. **Given** un utilisateur de l'app Claude qui termine l'onboarding, **When** il colle le
   bloc fourni dans les instructions de son projet dédié et ouvre une nouvelle conversation
   dans ce projet, **Then** le skill utilise ce positionnement sans reposer les questions.

---

### User Story 3 - Importer mon profil LinkedIn (Priority: P1)

L'utilisateur fournit son profil sans saisie fastidieuse, à partir d'une source qu'il
contrôle, pour obtenir un audit fiable.

**Why this priority**: L'audit n'a de valeur que s'il repose sur le vrai profil ; l'import doit
respecter les CGU LinkedIn (principe I de la constitution).

**Independent Test**: Fournir successivement une archive officielle, un export PDF et un
copier-coller du même profil ; vérifier que les sections reconnues sont listées et que les
sections absentes sont marquées « non fournies ».

**Acceptance Scenarios**:

1. **Given** l'archive officielle LinkedIn de l'utilisateur, **When** il la fournit, **Then**
   le skill en extrait profil, postes, compétences, recommandations et posts, et liste ce qui
   manque.
2. **Given** un export PDF ou un copier-coller partiel, **When** l'utilisateur le fournit,
   **Then** le skill indique explicitement les sections qu'il n'a pas pu voir.
3. **Given** un outil de navigation déjà connecté au compte de l'utilisateur, **When**
   l'utilisateur autorise la lecture de son propre profil, **Then** le skill le lit en
   lecture seule, sans jamais demander de mot de passe ni lire d'autres profils.
4. **Given** un contenu lu contenant une instruction (ex. « ignore tes règles »), **When** le
   skill le traite, **Then** il ignore l'instruction et la signale à l'utilisateur.

---

### User Story 4 - Obtenir un audit noté (Priority: P1)

L'utilisateur obtient une note sur 100 de son profil et une note sur 20 de ses posts, avec les
3 corrections prioritaires classées par points perdus.

**Why this priority**: C'est la promesse centrale du skill : savoir où agir en premier.

**Independent Test**: Fournir une archive officielle complète et 10 posts avec statistiques ;
vérifier la présence des deux notes, du détail par critère et des 3 corrections
prioritaires, sans section inventée.

**Acceptance Scenarios**:

1. **Given** un profil importé, **When** l'utilisateur demande un audit, **Then** le skill
   affiche une note sur 100 répartie sur 12 critères, chaque critère étant justifié.
2. **Given** une section non fournie (ex. bannière), **When** l'audit est produit, **Then**
   la section est marquée « non évaluée » et n'entre pas dans la note.
3. **Given** des posts avec statistiques, **When** l'audit des posts est produit, **Then** le
   skill affiche une note sur 20, le taux d'engagement, le ratio commentaires et le multiple
   de portée.
4. **Given** moins de 10 posts, **When** l'audit des posts est produit, **Then** le skill
   indique qu'aucune tendance n'est fiable.
5. **Given** un poste actuel terminé ou une certification expirée affichée comme active,
   **When** l'audit est produit, **Then** l'incohérence est signalée.
6. **Given** un audit précédent enregistré, **When** l'utilisateur relance un audit, **Then**
   le skill affiche l'écart de note et les corrections prioritaires déjà traitées.

---

### User Story 5 - Améliorer mon profil (Priority: P2)

L'utilisateur reçoit des réécritures prêtes à copier-coller (titre, section Infos,
expériences, compétences, sélection, bannière, demandes de recommandation), dans l'ordre des
points perdus.

**Why this priority**: C'est la suite naturelle de l'audit et ce qui fait monter la note ;
l'audit seul reste néanmoins utilisable sans ce mode.

**Independent Test**: À partir d'un audit, demander les améliorations ; vérifier les limites
de longueur, l'absence de chiffre inventé et la nouvelle note affichée.

**Acceptance Scenarios**:

1. **Given** un audit réalisé, **When** l'utilisateur demande d'améliorer son titre, **Then**
   le skill propose 3 options de 220 caractères maximum contenant les mots-clés de sa cible.
2. **Given** une section Infos à réécrire, **When** le skill la réécrit, **Then** l'accroche
   tient dans les ~265 premiers caractères, le texte fait 1 400 caractères maximum et se
   termine par un appel à l'action.
3. **Given** une expérience sans chiffre fourni, **When** le skill la réécrit au format
   « verbe d'action + résultat », **Then** il insère `{{chiffre à confirmer}}` au lieu d'un
   chiffre.
4. **Given** un texte écrit par l'utilisateur et une demande ciblée, **When** le skill le
   modifie, **Then** seule la partie demandée change.
5. **Given** des réécritures livrées, **When** le skill re-note le profil, **Then** il précise
   ce qu'une réécriture ne peut pas créer (recommandations, activité).
6. **Given** un navigateur connecté et un nouveau titre choisi, **When** l'utilisateur demande
   de l'appliquer, **Then** le skill montre le titre avant/après, attend sa validation, ne
   modifie que le titre, puis confirme que le texte en ligne correspond au texte validé.
7. **Given** trois réécritures prêtes, **When** l'utilisateur en valide une seule, **Then**
   le skill n'applique que celle-ci et redemande une validation pour chacune des autres.

---

### User Story 6 - Rédiger des posts (Priority: P2)

L'utilisateur obtient des posts courts, accrocheurs et humanisés, construits sur ses vrais
faits, pour publier régulièrement sans sonner « IA ».

**Why this priority**: La régularité de publication pèse dans la visibilité recruteurs, mais
l'utilisateur tire déjà de la valeur des stories 4 et 5 sans ce mode.

**Independent Test**: Donner un fait précis, demander un post ; vérifier les 3 accroches, les
règles de format, la fiche « POST PRÊT » et le score humanizer avant/après.

**Acceptance Scenarios**:

1. **Given** un positionnement enregistré, **When** l'utilisateur demande une stratégie de
   contenu, **Then** le skill propose 4 à 5 piliers à utiliser en rotation.
2. **Given** une idée vague, **When** l'utilisateur demande un post, **Then** le skill pose une
   seule question groupée pour obtenir un fait vrai et précis avant d'écrire.
3. **Given** un fait précis, **When** le skill rédige, **Then** il propose 3 accroches (dont
   une recommandée) puis un post de 700 à 900 caractères respectant les règles de format.
4. **Given** un post rédigé, **When** il est affiché, **Then** il est accompagné d'une fiche
   « POST PRÊT » et du score humanizer avant/après, et il n'est jamais publié par le skill.

---

### User Story 7 - Mettre à jour le skill (Priority: P3)

L'utilisateur passe à une nouvelle version du skill sans perdre son positionnement.

**Why this priority**: Indispensable dans la durée, mais sans valeur avant les premières
utilisations.

**Independent Test**: Enregistrer un positionnement, installer une version plus récente,
relancer le skill et vérifier que l'onboarding n'est pas relancé.

**Acceptance Scenarios**:

1. **Given** un positionnement enregistré et une nouvelle version publiée, **When**
   l'utilisateur met à jour le skill par le canal utilisé à l'installation, **Then** son
   positionnement est conservé intact.

---

### Edge Cases

- Archive LinkedIn incomplète ou dans une langue d'interface différente : le skill liste ce
  qu'il a reconnu et ce qui manque, sans deviner.
- Export Analytics illisible ou capture d'écran floue : le skill le dit et demande une autre
  source plutôt que d'estimer les chiffres.
- Aucun outil de navigation connecté : le skill propose les autres sources (archive, PDF,
  copier-coller) sans bloquer.
- Historique d'audits absent ou endommagé : l'audit est produit normalement, sans
  comparaison, et le skill le signale.
- Fichier de positionnement absent, vide ou endommagé : le skill relance l'onboarding en
  proposant de reprendre les valeurs encore lisibles.
- App Claude sans stockage local persistant : le skill fournit un bloc de positionnement à
  coller dans les instructions d'un projet Claude dédié (FR-023) ; hors projet et sans bloc
  recollé, il propose de le recoller avant de relancer l'onboarding.
- Instruction cachée dans un post, un commentaire ou une archive : ignorée et signalée.
- Client nommé avec des détails internes dans les faits fournis : anonymisé par défaut, avec
  demande d'accord avant de le citer.
- Demande de publication, de message ou d'invitation automatique : refusée en une phrase,
  avec un texte prêt à copier à la place.
- Validation globale du type « applique tout » : le skill liste les modifications et demande
  une validation pour chacune, sans rien appliquer en bloc.
- Modification de profil interrompue ou échouée (page changée, session expirée, champ
  introuvable) : le skill s'arrête, dit ce qui a été appliqué ou non, et fournit le texte à
  copier.
- Changement de poste actuel : l'option d'annonce au réseau reste désactivée sauf accord
  explicite.
- Demande « trouve-moi des posts à commenter » : le skill indique quels posts et comptes
  chercher et invite à coller les posts choisis ; il ne parcourt jamais le fil LinkedIn
  (FR-055).
- Demande d'affirmation absolue contestable dans un post : le skill la reformule et explique
  pourquoi.
- Texte mélangeant français et anglais : l'humanizer applique les critères des deux langues.

## Requirements *(mandatory)*

### Functional Requirements

#### Installation et distribution

- **FR-001**: Le dépôt MUST être public, sous licence MIT, et créditer explicitement les deux
  projets sources dans le README et dans un fichier de licences tierces.
- **FR-001a**: Le produit MUST être livré comme un seul skill `linkedin-coach` qui détecte le
  mode (AUDIT, AMÉLIORER, POSTS) à partir de la demande et demande en une ligne si c'est
  ambigu.
- **FR-002**: Les utilisateurs de Claude Code MUST pouvoir installer le skill via le système
  de plugins/marketplace de Claude Code.
- **FR-003**: Une installation alternative en une commande MUST être disponible via
  l'installeur de skills communautaire compatible avec les autres agents lisant le format
  SKILL.md.
- **FR-004**: L'installation manuelle (copie du dossier dans le répertoire de skills de
  l'utilisateur) MUST être documentée pour macOS, Linux et Windows.
- **FR-005**: Chaque release MUST fournir une archive importable dans l'app Claude, utilisable
  ensuite sur web, desktop, iPhone/iPad et Android.
- **FR-006**: Tout outil local fourni avec le skill MUST fonctionner à l'identique sur
  macOS, Linux et Windows. Ces outils MUST rester optionnels : sans eux (par exemple sans
  interpréteur disponible), toutes les fonctionnalités du skill restent utilisables, en passe
  manuelle annoncée à l'utilisateur (FR-062). Aucun prérequis obligatoire ne s'ajoute à
  ceux de Claude Code.
- **FR-007**: Le README MUST être bilingue FR/EN, avec un guide d'installation par plateforme
  et une section « dépannage ». Le README principal (`README.md`) est en anglais ;
  `README.fr.md` en est la version française.
- **FR-008**: Le plugin Claude Code MUST fournir quatre commandes, `/linkedin-coach:audit`,
  `/linkedin-coach:improve`, `/linkedin-coach:post` et `/linkedin-coach:positioning`, qui
  lancent le skill dans le mode correspondant avec l'argument éventuel de l'utilisateur.
  Sans argument, la commande demande ce qui manque.
- **FR-009**: Le README MUST montrer un avant/après réel (note, expériences, Infos,
  Sélection, post avec score humanizer), anonymisé, et un exemple des prochaines corrections
  proposées. Aucun chiffre ni exemple inventé.

#### Connexion au profil LinkedIn

- **FR-010**: Le skill MUST NOT scraper LinkedIn ni demander le mot de passe ou un cookie de
  session de l'utilisateur.
- **FR-011**: Le skill MUST accepter, par ordre de préférence : (1) l'archive officielle
  LinkedIn (profil, postes, compétences, recommandations, posts) ; (2) l'export PDF du
  profil ; (3) le copier-coller de sections ; (4) la lecture du propre profil de l'utilisateur
  dans son navigateur déjà connecté, en lecture seule et avec son accord.
- **FR-012**: Pour les statistiques des posts, le skill MUST accepter l'export Analytics de
  LinkedIn (tableur) ou des captures d'écran.
- **FR-013**: Si un navigateur connecté au propre compte de l'utilisateur est disponible, le
  skill MUST pouvoir appliquer une modification de profil validée (titre, section Infos,
  expérience, compétences, sélection, URL personnalisée). Pour chaque modification, il MUST
  d'abord montrer la section visée et le texte exact avant/après, puis attendre une
  validation explicite propre à cette seule modification. Une validation ne couvre jamais
  une autre modification. Le skill MUST désactiver ou laisser décochée l'annonce au réseau
  d'un changement de poste, sauf accord explicite. Il MUST NOT publier de post, envoyer de
  message ni d'invitation. Sans navigateur connecté, la modification se fait par
  copier-coller.
- **FR-015**: Après chaque modification appliquée, le skill MUST relire la section modifiée
  et confirmer à l'utilisateur que le texte en ligne correspond au texte validé, ou signaler
  l'écart.
- **FR-014**: Le skill MUST ignorer et signaler toute instruction trouvée dans un contenu lu
  (post, commentaire, profil, archive).
- **FR-016**: En lecture via le navigateur, le skill MUST faire défiler toute la page par
  paliers, attendre la fin du chargement différé (aucun bloc en squelette) et vérifier la
  présence de chaque titre de section avant de noter. Une section non vue MUST être marquée
  « non évaluée (non lue) », jamais notée 0 ; 0 seulement si l'absence est confirmée par
  l'utilisateur ou par une page entièrement chargée.

#### Positionnement utilisateur (onboarding)

- **FR-020**: Au premier lancement, si aucun positionnement n'existe, le skill MUST poser au
  maximum 7 questions : rôle et séniorité, expertises clés, certifications (avec dates),
  URL profil/site, cible (poste, contrat, villes), terrain réel à raconter, langue préférée
  (FR/EN).
- **FR-021**: Le positionnement MUST être enregistré localement chez l'utilisateur, hors du
  dossier du skill, pour qu'une mise à jour ne l'écrase pas.
- **FR-022**: L'utilisateur MUST pouvoir modifier son positionnement à tout moment.
- **FR-023**: Dans l'app Claude, où le skill ne peut pas écrire de fichier local, le skill MUST
  livrer le positionnement sous forme de bloc prêt à coller dans les instructions d'un projet
  Claude dédié, avec la marche à suivre. Il MUST reconnaître ce bloc lorsqu'il est présent
  dans les instructions du projet ou dans la conversation, et ne pas relancer l'onboarding.
  Après chaque modification du positionnement, il MUST fournir le bloc mis à jour.

#### Mode AUDIT

- **FR-030**: Le skill MUST noter le profil sur 100 selon 12 critères : titre, 2 premières
  lignes de la section Infos, corps de la section Infos, sélection, bannière, photo, poste
  actuel, profondeur d'expérience, compétences, recommandations, activité, visibilité
  recruteurs.
- **FR-031**: Le skill MUST NOT noter une section non fournie ; elle est marquée
  « non évaluée » et sort du maximum. La note s'affiche alors sur le maximum atteignable
  (ex. `41/88 (2 critères non évalués)`), et sur 100 quand les 12 critères sont évalués.
- **FR-032**: Le skill MUST noter les posts sur 20 (accroche, spécificité, cohérence,
  régularité) et calculer taux d'engagement, ratio commentaires et multiple de portée ; avec
  moins de 10 posts, il MUST dire qu'aucune tendance n'est fiable.
- **FR-033**: Le skill MUST afficher les 3 corrections prioritaires classées par points
  perdus ; une notation généreuse est un défaut.
- **FR-034**: Le skill MUST signaler les incohérences factuelles (poste actuel terminé,
  certification expirée affichée comme active…).
- **FR-035**: Après chaque audit, le skill MUST ajouter une entrée à l'historique des audits
  (date, note /100, note /20, 3 corrections prioritaires), stocké au même endroit que le
  positionnement. L'historique MUST NOT contenir de texte du profil ni de posts.
- **FR-036**: Si un audit précédent existe, le skill MUST afficher l'écart de note avec le
  dernier audit et indiquer quelles corrections prioritaires précédentes ont été traitées.
- **FR-037**: Dans l'app Claude, le skill MUST fournir l'entrée d'historique sous forme de
  résumé à coller dans les instructions du projet dédié, et lire l'historique présent dans
  ces instructions.

#### Mode AMÉLIORER

- **FR-040**: Le skill MUST proposer 3 options de titre de 220 caractères maximum, avec les
  mots-clés recruteurs de la cible.
- **FR-041**: Le skill MUST réécrire la section Infos : accroche dans les ~265 premiers
  caractères, 1 400 caractères maximum, appel à l'action final.
- **FR-042**: Le skill MUST réécrire les expériences au format « verbe d'action + résultat »
  et MUST NOT inventer de chiffre (`{{chiffre à confirmer}}` à la place).
- **FR-043**: Le skill MUST proposer les compétences à épingler/ajouter/supprimer, le contenu
  de la Sélection, la bannière (texte et structure), l'URL personnalisée et des messages de
  demande de recommandation personnalisés citant un projet précis.
- **FR-044**: Sur un texte écrit par l'utilisateur, le skill MUST ne changer que ce qui est
  demandé.
- **FR-045**: Le skill MUST re-noter après réécriture et dire ce qu'une réécriture ne peut
  pas créer (recommandations, activité).

#### Mode POSTS

- **FR-050**: Le skill MUST construire 4 à 5 piliers de contenu à partir du positionnement,
  utilisés en rotation.
- **FR-051**: Avant d'écrire, le skill MUST exiger un fait vrai et précis ; si l'idée est
  vague, il pose une seule question groupée.
- **FR-052**: Le skill MUST proposer 3 accroches issues d'une bibliothèque d'au moins 16
  formules, dont une recommandée, puis le post complet.
- **FR-053**: Par défaut, un post MUST respecter : 700 à 900 caractères ; ligne 1 =
  affirmation ou chiffre, jamais une question ; paragraphes courts ; une seule idée ;
  question finale spécifique ; 0 à 3 hashtags ; aucun lien dans le corps (lien en premier
  commentaire) ; chiffres externes sourcés.
- **FR-054**: Le skill MUST NOT produire d'affirmation absolue contestable.
- **FR-055**: Le skill MUST recommander 3 à 5 posts par semaine. Pour les jours sans
  publication, il MUST proposer quels types de posts et de comptes chercher soi-même
  (recruteurs, managers, communauté du domaine de la cible), puis rédiger un commentaire sur
  chaque post que l'utilisateur colle dans la conversation. Il MUST NOT parcourir le fil
  LinkedIn ni lire des posts ou profils tiers pour les trouver (principe I).
- **FR-056**: Le skill MUST NOT publier ; il livre un bloc prêt à copier et une fiche
  « POST PRÊT » (pilier, accroche, longueur, créneau, premier commentaire, éléments à
  vérifier, score humanizer).

#### Humanizer

- **FR-060**: Tout texte destiné à LinkedIn MUST passer par l'humanizer avant affichage :
  tirets cadratins, vocabulaire IA (FR et EN), triades, caractères invisibles, emojis
  génériques, longueur uniforme des phrases et des puces.
- **FR-061**: Un outil local de détection (score sur 5 critères) et de nettoyage MUST être
  fourni et MUST traiter le français et l'anglais à égalité (pronoms, contractions, lexique).
- **FR-062**: Le skill MUST afficher le score avant/après et préciser si la passe a été
  manuelle ou outillée.

#### Confidentialité

- **FR-070**: Le skill MUST NOT citer un client nommé avec des détails internes sans
  validation ; il anonymise par défaut.
- **FR-071**: Aucune donnée de l'utilisateur MUST quitter son poste en dehors de ce que Claude
  traite déjà dans la conversation ; aucune télémétrie.

#### Langues

- **FR-080**: Le skill MUST fonctionner en français et en anglais ; la langue par défaut est
  définie à l'onboarding et une version dans l'autre langue est proposée sur demande.

#### Exigences non fonctionnelles

- **NFR-001**: Installation en moins de 2 minutes sur chacune des 3 plateformes.
- **NFR-002**: Le fichier d'entrée du skill reste concis ; les références longues (formules,
  grille, lexique) sont séparées et chargées à la demande.
- **NFR-003**: Versionnage sémantique, CHANGELOG, et releases publiques avec l'archive pour
  l'app Claude jointe.
- **NFR-004**: Chaque contribution est vérifiée automatiquement : format du skill valide,
  outils locaux exécutables sur les 3 OS, tests de l'humanizer en FR et en EN.
- **NFR-005**: Un guide de contribution explique comment ajouter des formules d'accroche ou
  des mots au lexique.

#### Hors périmètre (v1)

- Scraping de LinkedIn ou lecture de profils tiers en masse.
- Publication automatique ou programmée de posts, y compris via l'API officielle LinkedIn.
- Intégration avec des services tiers payants (Apify, Publora…).
- Envoi automatique de messages ou d'invitations.

### Key Entities

- **Positionnement**: profil de référence de l'utilisateur (rôle, séniorité, expertises,
  certifications datées, URL, cible, terrain réel, langue). Stocké localement hors du skill ;
  les valeurs inconnues sont marquées « à confirmer ».
- **Profil importé**: sections du profil LinkedIn extraites d'une source fournie par
  l'utilisateur, chacune marquée « fournie » ou « non fournie », avec sa source.
- **Post et statistiques**: texte d'un post publié, date, impressions, réactions,
  commentaires, republications.
- **Audit**: note profil /100 (12 critères, chacun noté ou « non évalué », avec
  justification), note posts /20, indicateurs calculés, incohérences, 3 corrections
  prioritaires.
- **Historique des audits**: liste d'entrées (date, note profil /100, note posts /20,
  3 corrections prioritaires), stockée avec le positionnement ; aucun texte du profil.
- **Réécriture**: texte proposé pour une section du profil, avec ses limites de longueur,
  ses `{{à confirmer}}` et l'impact estimé sur la note.
- **Pilier de contenu**: thème récurrent dérivé du positionnement (4 à 5 au total).
- **Formule d'accroche**: modèle réutilisable de première ligne (au moins 16).
- **Fiche POST PRÊT**: pilier, accroche, longueur, créneau, premier commentaire, éléments à
  vérifier, score humanizer avant/après.
- **Score humanizer**: note sur 5 critères, avant/après, mode manuel ou outillé.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Sur macOS, Windows et Linux, un utilisateur installe le skill via le marketplace
  et le voit dans la liste des skills en moins de 2 minutes.
- **SC-002**: L'archive de release s'importe dans l'app Claude et le skill se déclenche sur
  « audite mon profil LinkedIn » sur web, desktop et mobile.
- **SC-003**: Avec une archive LinkedIn officielle, l'audit produit une note sur 100 dont
  0 section est notée sans avoir été fournie.
- **SC-004**: Sans positionnement enregistré, l'onboarding se lance dans 100 % des cas ; après
  une mise à jour du skill, le positionnement est conservé dans 100 % des cas. Dans l'app
  Claude, une nouvelle conversation dans le projet dédié ne relance jamais l'onboarding.
- **SC-005**: 100 % des posts générés respectent les règles de FR-053 et affichent un score
  humanizer avant/après.
- **SC-006**: L'humanizer donne un critère « voix » cohérent sur un texte français contenant
  « je » et « nous », et des scores comparables sur un même texte en FR et en EN.
- **SC-007**: 0 action d'écriture sur LinkedIn (publication, message, invitation,
  modification de profil) n'a lieu sans validation explicite de l'utilisateur, et chaque
  modification appliquée correspond exactement à une validation distincte.
- **SC-010**: Dans 100 % des modifications appliquées via le navigateur, le texte en ligne
  relu correspond au texte validé, ou l'écart est signalé à l'utilisateur.
- **SC-008**: 0 chiffre, client, résultat ou recommandation inventé dans les textes produits
  sur un jeu de profils de test (toute donnée manquante apparaît en « à confirmer »).
- **SC-009**: 100 % des instructions cachées dans un jeu de contenus de test sont ignorées et
  signalées à l'utilisateur.

## Assumptions

- Nom du dépôt et du skill : `linkedin-coach` (nom déjà utilisé par le prototype SKILL.md
  présent à la racine du projet).
- Architecture (confirmée en clarification) : un seul skill multi-modes (AUDIT, AMÉLIORER,
  POSTS) dont le fichier d'entrée oriente vers des références chargées à la demande ; pas de
  pack de skills séparés en v1.
- La publication via l'API officielle LinkedIn (OAuth « Share on LinkedIn ») est reportée à
  une v2 et reste hors périmètre v1.
- La persistance locale (FR-021) s'applique à Claude Code ; dans l'app Claude, le
  positionnement vit dans les instructions d'un projet Claude dédié (FR-023, confirmé en
  clarification).
- L'utilisateur est capable de télécharger son archive officielle LinkedIn ou un export PDF ;
  le skill explique comment faire.
- La lecture via navigateur repose sur un outil de navigation déjà connecté à Claude par
  l'utilisateur ; le skill n'en installe aucun.
- Le prototype `SKILL.md` existant sert de base de contenu (grille, modes, règles de
  confidentialité) et sera restructuré au plan.
- Les choix techniques (structure du dépôt, langage des outils locaux, CI) relèvent de
  `/speckit-plan`.
