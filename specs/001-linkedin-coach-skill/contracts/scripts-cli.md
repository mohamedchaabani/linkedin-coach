# Contrat : outils locaux (CLI)

Tous les outils : Python ≥ 3.9, bibliothèque standard uniquement, **aucun accès réseau**,
UTF-8 en entrée et en sortie (y compris sous Windows : `sys.stdout.reconfigure(encoding="utf-8")`),
codes de sortie `0` = succès, `1` = erreur d'entrée, `2` = erreur d'usage.

Chaque script déclare en en-tête la fixture utilisée par `tests/test_no_network.py` :
`# test-fixture: <chemin relatif à tests/fixtures/> [arguments placés avant le chemin]`.

Invocation depuis le skill (premier interpréteur disponible) :
`python3 <chemin>` → `python <chemin>` → `py -3 <chemin>` ; si aucun : passe manuelle.

---

## `scripts/humanizer.py detect`

```
humanizer.py detect [--lang fr|en|auto] [--json] [FICHIER | -]
```

- Entrée : texte (fichier ou stdin). `--lang auto` par défaut.
- Sortie `--json` :

```json
{
  "lang": "fr",
  "score": 72,
  "criteres": {
    "ponctuation": {"score": 16, "max": 20, "constats": ["2 tirets cadratins pour 140 mots"]},
    "vocabulaire": {"score": 12, "max": 20, "constats": ["« incontournable »", "« levier »"]},
    "tournures":   {"score": 16, "max": 20, "constats": ["triade ligne 4"]},
    "rythme":      {"score": 14, "max": 20, "constats": ["6 phrases de 14 à 16 mots"]},
    "voix":        {"score": 14, "max": 20, "constats": ["1re personne : 3 occurrences"]}
  }
}
```

- Sortie texte (sans `--json`) : une ligne par critère puis `SCORE 72/100`.
- Garanties testées : un texte FR naturel avec « je » et « nous » obtient un score « voix »
  ≥ 14/20 (SC-006) ; un même texte traduit FR/EN obtient des scores à ±10 points.

## `scripts/humanizer.py clean`

```
humanizer.py clean [--lang fr|en|auto] [FICHIER | -]
```

- Corrections mécaniques uniquement : tirets cadratins → virgule ou point selon le contexte,
  guillemets courbes → droits (EN) ou conservation des « » (FR), suppression des caractères
  invisibles, espaces multiples.
- Sortie : texte nettoyé sur stdout ; résumé des changements sur stderr.
- Ne modifie jamais les mots (le reformulage reste fait par Claude).

## `scripts/archive.py`

```
archive.py [--posts N] CHEMIN_ARCHIVE_ZIP_OU_DOSSIER
```

- Lit les CSV de l'archive officielle LinkedIn (voir [research.md](../research.md) R5).
- Sortie Markdown sur stdout :
  - `## Sections reconnues` : une sous-section par critère de la grille alimenté
    (titre, Infos, postes, compétences, certifications, recommandations, formation).
  - `## Posts` : les N derniers posts (défaut 30) avec date et texte.
  - `## Non fournies` : sections de la grille absentes de l'archive (photo, bannière,
    sélection, statistiques…), à fournir autrement.
- Ne suit aucun lien ni URL présent dans les données ; tout contenu est rendu comme texte.

## `tools/validate_skill.py` (développement, CI)

```
validate_skill.py [--strict] [--root RACINE] [CHEMIN_SKILL]   # défaut : skills/linkedin-coach
```

Vérifie : frontmatter YAML avec `name` (minuscules, chiffres, tirets, ≤ 64, égal au nom du
dossier) et `description` (≤ 200 caractères, limite de l'import dans l'app Claude, voir
research.md R2) ; tous les chemins `references/…`, `scripts/…`, `templates/…` cités dans les
`.md` du skill existent ; sans `--strict`, un `plugin.json` ou `CHANGELOG.md` absent est un
avertissement, avec `--strict` (CI, release) une erreur ; `SKILL.md` ≤ 150 lignes ; tous les liens relatifs vers `references/`
et `scripts/` existent ; aucun import réseau interdit dans `scripts/` ; versions identiques
dans `plugin.json` et en tête du CHANGELOG.

## `tools/build_zip.py` (développement, CI, release)

```
build_zip.py [--out dist/]
```

Produit `dist/linkedin-coach-vX.Y.Z.zip` (racine : `linkedin-coach/SKILL.md`), sans fichiers
de test ni caches.
