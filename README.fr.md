# LinkedIn Coach

*[English version](README.md)*

**Un coach LinkedIn qui se souvient de vous, vous note, suit votre progression et écrit des
posts qui ne sonnent pas « IA ».**

Un skill open source pour Claude qui vous aide à **être trouvé et contacté par des
recruteurs et des clients** sur LinkedIn : audit noté de votre profil et de vos posts,
réécritures prêtes à copier, posts courts construits sur votre vrai travail.

Gratuit, sous licence MIT, sans service payant ni dépendance. Fonctionne avec Claude Code
(macOS, Windows, Linux) et dans l'app Claude (web, desktop, iPhone/iPad, Android). Associé à
**Claude in Chrome**, il peut lire votre propre profil et appliquer les modifications que
vous validez.

## Pourquoi pas simplement demander à Claude ?

Vous parlez toujours à Claude en langage naturel. Le skill change ce que Claude en fait :

| | Claude seul | Avec LinkedIn Coach |
|---|---|---|
| **Mémoire** | Redemande qui vous êtes à chaque conversation | 7 questions une seule fois ; votre positionnement est enregistré et réutilisé |
| **Notation** | Un avis vague, différent à chaque fois | Profil sur 100 selon une grille fixe de 12 critères, posts sur 20 |
| **Progression** | Aucun historique | Chaque audit est enregistré ; vous voyez votre note évoluer d'un audit à l'autre |
| **Texte « IA »** | Formulations génériques, vocabulaire d'IA | Passe humanizer avec score avant/après (5 critères, lexiques FR et EN) |
| **Faits** | Tendance à enjoliver (« +40 % de performance ») | Rien d'inventé : une donnée manquante devient `{{à confirmer}}` |
| **Vos données** | Vous collez les sections à la main | Lit directement l'archive officielle LinkedIn |
| **Agir sur le profil** | — | Avec Claude in Chrome : applique chaque modification après votre « oui », puis la vérifie sur la page. Ne publie jamais |
| **Raccourcis** | Conversation libre uniquement | Commandes dédiées : `/linkedin-coach:audit`, `:improve`, `:post`, `:positioning` |
| **Méthode** | Conseils généraux | 20 formules d'accroche, règles de format LinkedIn, corrections classées par points perdus, notes sévères |

## Ce que fait le skill

- **Audit** : note du profil sur 100 (12 critères), note des posts sur 20, incohérences
  repérées, 3 corrections prioritaires, progression depuis votre dernier audit.
- **Améliorer** : titre, section Infos, expériences, compétences, Sélection, bannière,
  demandes de recommandation. Avec Claude in Chrome connecté, il peut appliquer une
  modification sur votre profil, **une validation par modification**.
- **Posts** : piliers de contenu, 3 accroches au choix, post de 700 à 900 caractères construit
  sur **vos** faits, fiche « POST PRÊT » et score humanizer avant/après.

## Ce qu'il ne fera jamais

- Scraper LinkedIn, vous demander votre mot de passe, lire des profils tiers ou votre fil.
- Publier, envoyer un message ou une invitation, ou modifier votre profil sans votre
  validation explicite, action par action.
- Inventer un chiffre, un client ou un résultat : ce qui manque devient `{{à confirmer}}`.
- Envoyer vos données ailleurs : votre positionnement reste sur votre poste (ou dans votre
  projet Claude). Aucune télémétrie.

## Prérequis

| Quoi | Pour | Obligatoire ? |
|---|---|---|
| Un compte Claude (Pro, Max, Team ou Enterprise) | Utiliser le skill | Oui |
| [Claude Code](https://docs.claude.com/en/docs/claude-code) **ou** l'app Claude | Faire tourner le skill | L'un des deux |
| Google Chrome + l'extension [Claude in Chrome](https://claude.com/chrome) | Lire votre profil et appliquer les modifications à votre place | Optionnel |
| Python ≥ 3.9 (bibliothèque standard seulement) | Score humanizer et import de l'archive LinkedIn | Optionnel : sans lui, le skill fait ces étapes à la main et le dit |

## Installation

### Claude Code (recommandé)

Dans une session Claude Code :

```
/plugin marketplace add mohamedchaabani/linkedin-coach
/plugin install linkedin-coach@linkedin-coach
```

Vérifiez avec `/plugin` : `linkedin-coach` doit être activé. Le skill se déclenche tout seul
quand vous écrivez « audite mon profil LinkedIn », ou s'utilise avec ses commandes :

| Commande | Ce qu'elle fait |
|---|---|
| `/linkedin-coach:audit` | Audit noté du profil et des posts |
| `/linkedin-coach:improve [section et objectif]` | Réécrire une section, ex. `titre pour des postes d'architecte à Genève` |
| `/linkedin-coach:post [fait]` | Écrire un post, ex. `la migration AEM finie la semaine dernière` |
| `/linkedin-coach:positioning [changement]` | Voir ou mettre à jour le positionnement, ex. `ajoute Genève` |

Dans l'app Claude, les commandes ne sont pas disponibles : écrivez simplement votre demande.

### App Claude (web, desktop, mobile)

1. Téléchargez `linkedin-coach-vX.Y.Z.zip` depuis la
   [dernière release](https://github.com/mohamedchaabani/linkedin-coach/releases/latest).
2. Dans l'app Claude : **Customize → Skills → + → Create skill → Upload a skill**, puis
   choisissez le .zip.
3. Activez le skill.
4. Créez un **projet Claude** « LinkedIn Coach » et ouvrez vos conversations dedans : le
   skill vous demandera une seule fois de coller votre positionnement dans les instructions
   du projet.

Autres méthodes (`npx skills add`, copie manuelle), mises à jour et emplacement de vos
données : [docs/fr/installation.md](docs/fr/installation.md).

### Optionnel : connecter Claude in Chrome

Sans navigateur, le skill vous donne **du texte à copier-coller** vous-même dans LinkedIn.
Avec Claude in Chrome, il peut **ouvrir votre propre profil pour le lire** et **appliquer
chaque modification que vous validez**.

1. Installez l'extension [Claude in Chrome](https://claude.com/chrome) et connectez-vous
   avec le même compte Claude.
2. Dans ce Chrome, connectez-vous vous-même à LinkedIn. Le skill ne demande jamais votre mot
   de passe.
3. Dans Claude Code, lancez `/chrome` (ou démarrez avec `claude --chrome`) pour connecter le
   navigateur.
4. Quand l'extension le demande, autorisez-la sur `linkedin.com`.

Ce qu'il peut faire dans le navigateur : lire **votre** profil, et modifier votre titre, la
section Infos, la description d'une expérience, vos compétences, la Sélection ou l'URL
personnalisée, **après un « oui » pour cette modification précise**. Ce qu'il ne fait
jamais : publier, commenter, réagir, envoyer un message ou une invitation, parcourir
d'autres profils ou votre fil, modifier les paramètres du compte. L'option « annoncer au
réseau » reste désactivée sauf demande explicite.

## Tutoriel pas à pas

### Étape 1 : démarrer

Ouvrez Claude Code (ou votre projet « LinkedIn Coach » dans l'app Claude) et écrivez :

> Audite mon profil LinkedIn

Dans Claude Code, vous pouvez aussi taper `/linkedin-coach:audit`. Chaque étape ci-dessous
donne la commande correspondante.

### Étape 2 : répondre aux questions de positionnement (la première fois)

Le skill pose **au plus 7 questions, en un seul message** :

1. Rôle et séniorité (ex. « Architecte AEM, 12 ans »)
2. 3 à 5 expertises clés
3. Certifications, avec la date d'obtention (`AAAA-MM`) et la date d'expiration s'il y en a
4. **L'URL de votre profil LinkedIn** : voir ci-dessous
5. Cible : postes, types de contrat, villes, remote (oui / non / hybride)
6. Terrain réel à raconter : projets, outils, chiffres **vrais**
7. Langue préférée des textes : `fr` ou `en`

**Trouver votre URL LinkedIn :** sur LinkedIn, cliquez sur **Vous → Voir le profil**, puis
copiez la barre d'adresse. Elle ressemble à `https://www.linkedin.com/in/votre-nom/`.
Collez-la telle quelle.

Passez ce que vous ne savez pas : ça devient `{{à confirmer}}`, jamais une supposition. Le
skill enregistre ensuite votre positionnement :

- **Claude Code** : dans `~/.linkedin-coach/positionnement.md` (il demande d'abord).
- **App Claude** : il vous donne un bloc à coller dans les instructions du projet. Ces
  questions ne vous seront plus posées.

### Étape 3 : lui donner votre profil

Choisissez **une** source. Plus elle est complète, meilleur est l'audit.

| Source | Comment | Ce qu'elle contient |
|---|---|---|
| **Claude in Chrome** (le plus rapide) | Dites « lis mon profil dans Chrome ». Le skill ouvre l'URL de l'étape 2, **lit seulement**, ne clique sur rien | Tout ce qui est visible sur votre profil |
| **Archive LinkedIn** (la plus complète) | LinkedIn → **Vous → Préférences → Confidentialité des données → Obtenir une copie de vos données** → cochez Profil, Postes, Compétences, Recommandations, Certifications, Partages → Demander l'archive. LinkedIn l'envoie par e-mail (quelques minutes à 24 h). Donnez le .zip à Claude | Profil, expériences, compétences, recommandations, vos posts. Pas de photo, bannière, Sélection ni statistiques |
| **Export PDF** | Sur votre profil : **Plus → Enregistrer au format PDF**, puis joignez le fichier | Titre, Infos, expériences, compétences principales, formation |
| **Copier-coller** | Collez les sections dans la conversation | Pratique pour une demande ciblée (« réécris mon titre ») |

Pour les **statistiques des posts**, ajoutez l'export Analytics (**Analytics → Contenu →
Exporter**, enregistré en CSV si le .xlsx ne s'ouvre pas) ou des captures d'écran. Le skill
n'estime jamais un chiffre qu'il ne peut pas lire.

### Étape 4 : lire votre audit

```
NOTE PROFIL  47/100        NOTE POSTS  9/20
(12/12 critères évalués)   (14 posts)

  titre              4/12   intitulé seul, aucun mot-clé de la cible, pas de preuve
  bannière           non évaluée (non fournie)
  ...
INCOHÉRENCES         ...
TOP 3 CORRECTIONS    (par points perdus)
PROGRESSION          (si un audit précédent existe)
```

Les notes sont volontairement sévères. Une section non fournie est marquée « non évaluée »,
jamais devinée.

### Étape 5 : améliorer votre profil

Répondez « oui » quand le skill propose d'enchaîner, ou demandez directement :

> Réécris mon titre pour des postes d'architecte solution à Genève

Commande : `/linkedin-coach:improve titre pour des postes d'architecte solution à Genève`.

Il avance **une section à la fois**, en commençant par celle qui perd le plus de points. Pour
chacune, vous recevez un bloc prêt à copier. Si Claude in Chrome est connecté :

1. Il montre le texte **actuel** (relu sur la page) et le texte **proposé**.
2. Il demande : *« J'applique ce nouveau titre sur ton profil ? (oui / non) »*
3. Seul un **« oui »** clair à cette question précise compte. « ok », « applique tout » ou le
   silence ne valent pas validation : « applique tout » le fait redemander, modification par
   modification.
4. Il applique le texte, relit la page et dit « conforme » ou montre l'écart.

### Étape 6 : écrire des posts

> Écris un post sur la migration qu'on a finie la semaine dernière

Commande : `/linkedin-coach:post la migration qu'on a finie la semaine dernière`.

Si l'idée est vague, il pose une seule question groupée pour obtenir un **fait vrai et
précis**. Vous recevez 3 accroches, un post de 700 à 900 caractères et une fiche « POST
PRÊT » avec le score humanizer. **Vous publiez vous-même** : le skill ne publie jamais.

### Étape 7 : suivre votre progression

Relancez « Audite mon profil LinkedIn » dans quelques semaines. Le skill compare avec votre
dernier audit et montre ce qui a progressé. Pour changer votre cible ou vos infos à tout
moment :

> Mets à jour mon positionnement : ajoute Genève

Commande : `/linkedin-coach:positioning ajoute Genève`.

Plus d'exemples et ce que le skill refuse : [docs/fr/utilisation.md](docs/fr/utilisation.md).

## Dépannage

Voir [docs/fr/depannage.md](docs/fr/depannage.md).

## Pour contribuer

Voir [CONTRIBUTING.md](CONTRIBUTING.md) : ajouter une formule d'accroche, un terme au
lexique de l'humanizer, ou corriger une règle. Le projet suit une
[constitution](.specify/memory/constitution.md) et le workflow
[Spec Kit](https://github.com/github/spec-kit).

## Crédits

LinkedIn Coach s'inspire de deux projets sous licence MIT, crédités dans
[THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) :

- [sergebulaev/linkedin-skills](https://github.com/sergebulaev/linkedin-skills) (Sergey
  Bulaev) : formules d'accroche et règles de publication.
- [Jakeschincariol/linkedin-agent-skill](https://github.com/Jakeschincariol/linkedin-agent-skill)
  (Jake Schincariol) : grille de notation du profil et humanizer.

## Licence

[MIT](LICENSE).
