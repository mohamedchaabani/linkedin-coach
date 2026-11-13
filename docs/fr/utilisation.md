# Utiliser LinkedIn Coach

Parlez normalement : le skill reconnaît le mode à partir de votre demande. Au tout premier
usage, il vous pose au plus 7 questions pour connaître votre positionnement.

Dans Claude Code, chaque mode a aussi sa commande : `/linkedin-coach:audit`,
`/linkedin-coach:improve [section et objectif]`, `/linkedin-coach:post [fait]` et
`/linkedin-coach:positioning [changement]`.

## Audit

- « Audite mon profil LinkedIn » + votre archive LinkedIn (.zip), votre export PDF ou un
  copier-coller.
- « Analyse mes 20 derniers posts » + l'export Analytics (ou des captures).

Vous obtenez une note du profil (sur 100, ou sur le maximum atteignable si des sections
manquent), une note des posts sur 20, les incohérences, 3 corrections prioritaires et votre
progression depuis le dernier audit.

## Améliorer

- « Réécris mon titre »
- « Améliore ma section Infos pour des postes d'architecte à Genève »
- « Réécris mes expériences au format résultat »
- « Prépare 3 demandes de recommandation »

Les textes sont prêts à copier. Si un outil de navigation (Claude in Chrome) est connecté à
votre compte, le skill peut appliquer une modification **après votre « oui » explicite pour
cette modification précise**.

## Posts

- « Écris un post sur <un fait précis> »
- « Propose-moi une stratégie de contenu »
- « Rédige un commentaire pour ce post : <post collé> »

## Positionnement

- « Mets à jour mon positionnement : j'ajoute Genève »

## Ce que le skill refuse, et pourquoi

| Demande | Réponse | Pourquoi |
|---|---|---|
| « Publie ce post » | Texte prêt à copier | Vous gardez la main (principe II) |
| « Lis le profil de X » | Refus, alternative proposée | Pas de lecture de tiers (principe I) |
| « Trouve des posts à commenter » | Quoi chercher ; vous collez les posts | Pas de lecture du fil (principe I) |
| « Mets 30 % de gain » sans source | `{{chiffre à confirmer}}` | Zéro invention (principe III) |
| « Applique tout » | Une validation par modification | Une validation = une modification |

## Où sont mes données ?

- Claude Code : `~/.linkedin-coach/positionnement.md` et `historique-audits.md` (Windows :
  `%USERPROFILE%\.linkedin-coach\`), ou le dossier de `LINKEDIN_COACH_HOME`.
- App Claude : dans les instructions de votre projet Claude dédié.

Rien n'est envoyé ailleurs que dans votre conversation avec Claude. Aucune télémétrie.
