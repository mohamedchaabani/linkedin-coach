# Positionnement : onboarding, stockage, mise à jour

Le positionnement est la base de tout conseil. Sans lui, pas d'audit, pas de réécriture,
pas de post. Format exact : `templates/positionnement.md`.

## 1. Retrouver le positionnement (à chaque demande)

Chercher dans cet ordre et s'arrêter au premier trouvé :

1. **Fichier local** (Claude Code) : `$LINKEDIN_COACH_HOME/positionnement.md` si la variable
   existe, sinon `~/.linkedin-coach/positionnement.md` (Windows :
   `%USERPROFILE%\.linkedin-coach\positionnement.md`).
2. **Bloc dans les instructions du projet Claude** ou **dans la conversation** : texte entre
   `<!-- linkedin-coach:positionnement v1 -->` et `<!-- /linkedin-coach:positionnement -->`.

Ne jamais chercher ni écrire ce fichier dans le dossier du skill : une mise à jour
l'effacerait.

États possibles :

| État | Action |
|---|---|
| absent | Onboarding (section 2) |
| partiel (au moins un `{{à confirmer}}`) | Utiliser ; signaler une fois les champs manquants utiles à la demande |
| complet | Utiliser |
| illisible (balises absentes ou cassées) | Le dire, reprendre les valeurs encore lisibles, ne reposer que les questions manquantes |

## 2. Onboarding : au plus 7 questions, en un seul message

Poser ces questions ensemble, numérotées, puis attendre les réponses :

1. **Rôle et séniorité** (ex. « Architecte AEM, 12 ans »)
2. **Expertises clés** : 3 à 5 domaines
3. **Certifications**, avec la date d'obtention au format `AAAA-MM` et la date
   d'expiration si elle existe
4. **URL** du profil LinkedIn ou du site
5. **Cible** : postes visés, types de contrat, villes, remote (oui / non / hybride)
6. **Terrain réel à raconter** : projets, outils, chiffres **vrais** (ils nourriront les posts)
7. **Langue** préférée des textes : `fr` ou `en`

Règles :

- Réponse vide, « je ne sais pas », « passe » → `{{à confirmer}}`. Jamais de supposition.
- Ne pas poser de 8e question. Les détails viendront plus tard, au fil des demandes.
- Clients cités : les noter anonymisés dans « Références clients » (voir
  `references/confidentialite.md`).
- Puis enregistrer (section 3) et seulement ensuite traiter la demande de départ.

## 3. Enregistrer

Remplir `templates/positionnement.md` avec les réponses, « Mis à jour le » = date du jour
(`AAAA-MM-JJ`).

**Mode local** (Claude Code, accès aux fichiers de l'utilisateur) :

1. Demander l'accord une fois : « J'enregistre ton positionnement dans
   `~/.linkedin-coach/positionnement.md` ? » (ou le dossier de `LINKEDIN_COACH_HOME`).
2. Créer le dossier s'il n'existe pas, écrire le fichier en UTF-8.
3. Confirmer le chemin exact.

**Mode projet** (app Claude, ou fichier impossible à écrire ou non persistant) :

1. Afficher le bloc complet, balises comprises, dans un bloc de code.
2. Donner la marche à suivre : « Ouvre ou crée un projet Claude “LinkedIn Coach” →
   Instructions du projet → colle ce bloc → enregistre. Ouvre ensuite tes conversations
   dans ce projet : je ne te reposerai plus ces questions. »
3. Hors projet : « Tu peux aussi recoller ce bloc au début d'une conversation. »

## 4. Mettre à jour (« mets à jour mon positionnement »)

1. Montrer les valeurs actuelles.
2. Ne modifier que les champs que l'utilisateur change ; garder tous les autres à
   l'identique, y compris les `{{à confirmer}}` et les lignes inconnues.
3. Mettre à jour « Mis à jour le ».
4. Mode local : réécrire le fichier. Mode projet : redonner le **bloc complet** à coller à la
   place de l'ancien.

Le mode POSTS ajoute les piliers dans le champ « Piliers » de la même façon.

## 5. Compatibilité entre versions du skill

- La balise porte la version du format (`v1`). Une version du skill sait lire tout bloc `v1`.
- Une ligne inconnue est conservée telle quelle à la réécriture.
- Si un futur format (`v2`) apparaît, proposer la migration à l'utilisateur et montrer le
  résultat ; ne jamais migrer en silence.
