# Humanizer (passe obligatoire avant d'afficher)

S'applique à tout texte destiné à LinkedIn : titre, section Infos, expériences, posts,
commentaires, demandes de recommandation. Méthode inspirée de li-human
(Jakeschincariol/linkedin-agent-skill, MIT), étendue au français.

## 1. Mesurer (si Python est disponible)

Écrire le texte dans un fichier temporaire, puis :

```
python3 scripts/humanizer.py detect --json brouillon.txt
```

(`python`, puis `py -3` si `python3` n'existe pas.) Le score est sur 100, réparti en 5
critères notés sur 20 : ponctuation, vocabulaire, tournures, rythme, voix. Les `constats`
disent quoi corriger.

## 2. Corriger

**Corrections mécaniques** (sûres, sans changer les mots) :

```
python3 scripts/humanizer.py clean brouillon.txt
```

**Corrections de fond** (à faire soi-même, en gardant le sens et les faits) :

- Tirets cadratins (—) : au plus 1 pour 100 mots ; sinon virgule ou point.
- Mots IA à supprimer ou remplacer par un mot simple et précis. FR : crucial, essentiel,
  incontournable, véritable, levier, robuste, fluide, booster, plonger, « dans un monde en
  constante évolution », « à l'ère de », « n'est pas qu'un simple », « force est de
  constater ». EN : delve, leverage, seamless, game-changer, tapestry, landscape. Liste
  complète : `scripts/data/lexique-ia.fr.txt` et `scripts/data/lexique-ia.en.txt`.
- Casser les triades artificielles (« automatiser, optimiser et transformer »).
- Au plus un contraste « ce n'est pas X, c'est Y » par texte.
- Zéro « Le résultat ? », « Plot twist : », « Voici ce que… ».
- Varier vraiment la longueur des phrases et des puces : une courte à côté d'une longue,
  jamais trois de même taille.
- Pas d'emojis génériques (🚀🔥💡✨🎯), pas de mur de hashtags.
- Écrire à la 1re personne avec un détail vécu (« je », « nous », « on » / « I », « we »).
- Guillemets : « » en français, " " en anglais ; aucun caractère invisible.

## 3. Re-mesurer et afficher

Relancer `detect` sur la version finale et afficher :

```
humanizer :  outillé 52 → 84
```

## Sans Python

Faire la même passe à la main en suivant la liste ci-dessus, et l'annoncer :

```
humanizer :  passe manuelle (Python indisponible)
```

Ne jamais afficher de score inventé quand l'outil n'a pas tourné.
