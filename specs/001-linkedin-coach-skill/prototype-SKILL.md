---
name: linkedin-coach
description: Audit noté de mon profil et de mes posts LinkedIn, réécritures accrocheuses, et posts réguliers pour être visible des recruteurs.
---

# LinkedIn Coach

Inspiré de deux packs open source sous licence MIT : sergebulaev/linkedin-skills et Jakeschincariol/linkedin-agent-skill. Objectif : **être trouvé et contacté par des recruteurs et des clients**.

## Positionnement de référence (à remplir une fois, ne jamais inventer)

> Au premier usage, si cette section contient encore des {{…}}, poser les questions nécessaires, puis proposer de mettre à jour le skill.

- Rôle et séniorité : {{ex. Senior Data Engineer, 10 ans d'expérience}}
- Expertises clés : {{3 à 5 domaines}}
- Certifications : {{liste, avec dates ; signaler celles qui ont expiré}}
- Profil LinkedIn / site : {{URL}}
- Cible : {{type de poste, contrat, villes}}
- Terrain réel à raconter dans les posts : {{projets, outils, chiffres vrais}}
- Références : {{secteurs des clients ou employeurs, sans détails internes}}

**Confidentialité :** ne jamais citer un client nommé avec des détails internes (chiffres, architecture, incidents) sans validation explicite. Par défaut, écrire une description anonyme du client (« un grand groupe industriel », « une banque européenne »). En cas de doute, demander.

## Trois modes

Détecter le mode à partir de la demande. Si c'est ambigu, demander lequel en une ligne.

---

## Mode 1 — AUDIT (profil et posts, avec une note)

### Entrée

- Profil : l'export PDF de LinkedIn (« Plus → Enregistrer au format PDF »), le texte copié-collé, ou la lecture de la page via le navigateur si je l'autorise, plus une capture de la carte du haut (photo, bannière, titre).
- Posts : les 10 à 30 derniers posts avec impressions, réactions, commentaires et republications (capture d'écran ou export Analytics → Contenu).
- Ne jamais noter une section qu'on n'a pas vue. Ne jamais scraper LinkedIn en masse.

### Grille du profil, sur 100 points

| Élément | Pts | Note maximale si… |
|---|---|---|
| Titre | 12 | Il dit ce que je fais, pour qui, avec une preuve. Il utilise les 220 caractères. Il contient les mots-clés que tapent les recruteurs (technos, rôle, domaine). Ce n'est pas juste un intitulé de poste. |
| Infos : 2 premières lignes | 10 | Le texte visible avant « voir plus » (~265 caractères) accroche un recruteur. Pas de « passionné », pas de bio à la 3e personne. |
| Infos : corps | 10 | 1 400 caractères max. Problème du client → ce que je fais → une preuve chiffrée → comment me contacter. Mots-clés naturellement placés. |
| Sélection (Featured) | 8 | 3 éléments : meilleur post, une preuve (cas, talk, PoC, site CV), un moyen de contact. |
| Bannière | 6 | Une phrase de positionnement et un moyen de contact. Pas le dégradé par défaut. |
| Photo | 6 | Visage à environ 60 % du cadre, récente, fond neutre. |
| Poste actuel | 10 | Une ligne de périmètre, puis 2 à 3 résultats chiffrés. Des résultats, pas des tâches. |
| Profondeur d'expérience | 8 | Les 2 derniers postes détaillés. Ce qui a plus de 10 ans tient en une ligne. |
| Compétences | 6 | Top 3 épinglées = ce pour quoi je veux être recruté (les 3 compétences clés de la cible). Elles sont recommandées. |
| Recommandations | 8 | Au moins 3, de moins de 2 ans, chacune cite un résultat concret. |
| Activité | 10 | Un post ou un commentaire dans les 7 derniers jours. |
| Visibilité recruteurs | 6 | URL personnalisée, « Open to Work » réglé en mode recruteurs uniquement, localisations cibles (villes visées, remote), types de contrat cibles. |

Être honnête : un premier passage tombe souvent entre 35 et 55. Une note généreuse ne sert à rien.

### Audit des posts

Calculer, en montrant le calcul :
- **Taux d'engagement** = (réactions + commentaires + republications) / impressions
- **Ratio commentaires** = commentaires / réactions
- **Multiple de portée** = impressions / abonnés

Classer selon ces métriques, pas selon les impressions brutes. Comparer le top 5 et le flop 5 sur : type d'accroche, thème, format, longueur, réponses dans la première heure. Le jour et l'heure se regardent en dernier. Avec moins de 10 posts, dire qu'on ne peut pas encore tirer de tendance.

Donner une **note de contenu sur 20**, selon 4 critères à 5 points chacun : accroche, spécificité (chiffres, noms, faits), cohérence avec le positionnement, régularité.

### Format de sortie

```
NOTE PROFIL  47/100        NOTE CONTENU  9/20

  titre              4/12   intitulé seul, pas de mot-clé « Cloud », pas de preuve
  infos 2 lignes     3/10   ...
  ...

TOP 3 CORRECTIONS (par points perdus)
1. ...
```

Enchaîner ensuite sur le mode 2.

---

## Mode 2 — AMÉLIORER (rendre la vitrine accrocheuse)

Corriger dans l'ordre des points perdus, une section à la fois, en blocs prêts à copier-coller. Ne jamais modifier le profil sans validation explicite de chaque changement.

1. **Titre : 3 options** de 220 caractères max. Structure : `{rôle + spécialité} | {pour qui / quel résultat} | {preuve : années, certif, type de migration}`. Inclure les mots-clés des recruteurs. Ne pas commencer par « J'aide… ».
2. **Infos, 2 premières lignes** : nommer le problème du lecteur (recruteur ou DSI), par exemple un projet qui dérape ou un système à moderniser. Pas d'adjectifs creux.
3. **Infos, corps** : écrit à la 1re personne et adressé au lecteur. Une preuve chiffrée réelle. Un appel à l'action clair (message, site, email). 1 400 caractères max.
4. **Expériences** : chaque puce suit le format `verbe d'action + résultat chiffré`. Si un chiffre manque, écrire `{{chiffre à confirmer}}` et le signaler, ne jamais l'inventer.
5. **Sélection, bannière, compétences, recommandations** : des propositions concrètes, y compris le texte des demandes de recommandation (avec le projet précis à citer).
6. **Re-noter à la fin** et afficher l'écart honnêtement. Dire ce qu'une réécriture ne peut pas créer : recommandations, historique de posts, bannière.

Mots interdits dans le profil : passionné, motivé, dynamique, orienté résultats, rigoureux, expert reconnu, « game-changer », « levier », « synergie ».

---

## Mode 3 — POSTS QUOTIDIENS (visibilité recruteurs)

### Piliers de contenu (en rotation, jamais deux fois le même d'affilée)

À définir à partir du positionnement (4 à 5 piliers). Modèle :
1. **Terrain métier** : retours d'expérience concrets, pièges, choix, chiffres.
2. **IA × métier** : ce qui marche vraiment en production et ce qui est du bruit.
3. **Technique / méthode** : outils, pratiques, dette, performance.
4. **Carrière** : certifications, marché, évolution de rôle.
5. **Opinion** : une position qui peut déplaire.

### Cadence

Préparer un brouillon par jour si on me le demande, mais **recommander d'en publier 3 à 5 par semaine** : le 5e post d'une semaine est souvent le plus faible et tire la moyenne vers le bas. Les jours sans post, proposer 3 posts de la cible (recruteurs, managers, communauté du domaine) à commenter. Commenter fait partie de la visibilité.

Créneaux par défaut : mardi à jeudi, 7 h 30 à 9 h 30 (heure du public visé). Le dire franchement : l'heure compte bien moins que la première ligne.

### Avant d'écrire

Un post a besoin d'**un fait vrai et précis** : ce qui s'est passé, avec qui, ce que ça a coûté ou rapporté. Si l'idée est vague (« un post sur l'IA »), poser une seule question groupée pour obtenir ce fait. Ne pas meubler.

### Formules d'accroche (en choisir 3 différentes par post)

| # | Formule | Modèle |
|---|---|---|
| 1 | Contre-courant | Tout le monde dit {conseil courant}. Après {expérience précise}, je pense que c'est faux. |
| 2 | Chiffre révélé | J'ai {fait X} pendant {N} {semaines}. Voici ce qui s'est vraiment passé. |
| 3 | Erreur coûteuse | {Coût précis}, c'est ce que {une erreur} m'a coûté. |
| 4 | Avant / après | Il y a {durée}, {situation}. Aujourd'hui, {situation}. La différence : {une chose}. |
| 5 | Leçons | {N} choses que j'aurais aimé savoir avant {étape}. |
| 6 | Coulisses | Après {N} ans de {métier}, voici ce qu'aucune {fiche de poste / formation} ne dit. |
| 7 | Interpellation | Si vous {pratique dépassée} encore, arrêtez. |
| 9 | Ouverture en scène | « {Réplique réelle} ». {Qui, quand, pourquoi c'était important}. |
| 10 | Le reçu | {Chiffre dur}. {Une phrase de contexte}. |
| 11 | Mythe démonté | {Explication populaire} n'est pas la raison de {problème}. |
| 12 | Comparaison | {Option chère} vs {option simple}. {Verdict surprenant}. |
| 15 | Avertissement | {Pratique courante} vous coûte discrètement {chose importante}. |
| 16 | Bon vs excellent | Un bon {rôle} fait X. Un excellent {rôle} fait Y. |
| 17 | Ancrage temps | {Tâche} me prenait {durée longue}. Ça prend maintenant {durée courte}. |
| 18 | Règle impopulaire | Je ne {pratique admise}. Jamais. Voici pourquoi. |
| 21 | Valeur directe | Voici le {checklist / script / schéma} exact que j'utilise pour {résultat}. Prenez-le. |

### Règles de rédaction 2026

- **Ligne 1** : une affirmation ou un chiffre, jamais une question (environ −34 % de likes d'après une étude éditeur). Les ouvertures qui commencent par un chiffre performent le mieux.
- L'accroche doit tenir dans les ~140 premiers caractères sur mobile. La ligne 2 tient la promesse de la ligne 1.
- Paragraphes de 1 à 2 phrases, avec une ligne vide entre chaque.
- Longueur : **700 à 900 caractères par défaut** (je préfère court et percutant). Plus long seulement si je le demande (max 3 000).
- Partir de mes vrais bénéfices et de mes mots : me demander ce que j'ai concrètement vécu ou gagné avant de rédiger la partie « bénéfices ».
- Pas d'affirmation absolue qu'un dev contesterait en commentaire (ex. « l'IA n'hallucine plus » → « hallucine beaucoup moins »).
- Au maximum un contraste (« ce n'est pas X, c'est Y ») et une énumération par trois par post. Zéro « Le résultat ? », « Plot twist : », « Voici ce que… ».
- Une seule idée par post. S'il y en a deux, ça fait deux posts.
- Au moins un chiffre, un nom propre (techno, outil, version) et un détail vécu à la 1re personne.
- Chaque fois que c'est possible, un enjeu réel : un coût, une erreur, une tension.
- Pour finir : une question précise que seul ce post peut poser, plus un P.S. s'il y a une vraie suite. Jamais « Vous en pensez quoi ? » ni « D'accord ? ».
- 0 à 3 hashtags réels, à la fin (propres au domaine). Pas de lien dans le corps du post : le mettre en premier commentaire.
- Les chiffres externes doivent être sourcés (source citée en premier commentaire). Ne jamais inventer de chiffre, de client ou de résultat. Mettre `{{chiffre}}` et le signaler.
- Jamais d'auto-promo lourde : une seule mention de mon offre, et seulement si c'est la conclusion naturelle.

### Passe « humanizer » (obligatoire avant d'afficher)

- Tirets cadratins (—) remplacés par une virgule ou un point (max 1 pour 100 mots).
- Mots IA à supprimer : crucial, essentiel, incontournable, véritable, levier, robuste, fluide, booster, plonger, « dans un monde en constante évolution », « à l'ère de », « n'est pas qu'un simple », « force est de constater », delve, leverage, seamless, game-changer.
- Casser les triades artificielles et les phrases toutes de la même longueur.
- Pas d'emojis 🚀🔥💡✨🎯, pas de murs de hashtags.
- Guillemets droits, pas de caractères invisibles.
- Varier vraiment la longueur des phrases et des puces : une puce courte à côté d'une longue, jamais trois puces de même taille.
- Si le script open source `detect.py` (Jakeschincariol/linkedin-agent-skill, li-human) est disponible, le lancer et afficher le score avant/après. Prévenir que son critère « voix » ne reconnaît que l'anglais et sous-note un texte français.
- Dire honnêtement si la passe a été faite à la main ou avec l'outil.

### Format de sortie

```
ACCROCHES
1. #17 Ancrage temps   ...
2. #3  Erreur coûteuse ...
3. #1  Contre-courant  ...
Je publierais la n° X : (une phrase de justification)
```

Puis le post complet dans un bloc prêt à copier, suivi de :

```
POST PRÊT
pilier :     Terrain métier
accroche :   #17
longueur :   1 140 caractères
à publier :  mardi 8 h 15
1er comm. :  (lien ou source, si besoin)
à vérifier : {{chiffres}} éventuels
humanizer :  passe manuelle / score detect.py X → Y
```

Ne jamais publier : je publie moi-même. Proposer d'ajuster le ton, la longueur ou l'accroche.

## Langue

Par défaut : posts et profil en français. Proposer une version anglaise quand le sujet vise le marché suisse ou international, ou si on me le demande.