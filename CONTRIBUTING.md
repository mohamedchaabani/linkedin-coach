# Contribuer à LinkedIn Coach

*English below.*

Merci ! Le projet suit une [constitution](.specify/memory/constitution.md) : relisez les
principes I à X avant de proposer un changement. **Les principes I (pas de scraping) et II
(une validation par action) ne sont pas négociables** : une PR qui ajoute du scraping, de la
lecture de profils tiers, une publication automatique ou une écriture sans validation sera
refusée.

## Ajouter une formule d'accroche

1. Ouvrez `skills/linkedin-coach/references/formules-accroche.md`.
2. Ajoutez une ligne au tableau, numérotée à la suite :
   `| 21 | Nom court | Modèle avec {variables} | Exemple fictif |`
   - le modèle contient au moins une `{variable}` ;
   - l'exemple est fictif et ne finit pas par une question.
3. `python -m unittest discover -s tests -p "test_formules.py"`.

## Ajouter un terme au lexique de l'humanizer

1. Ajoutez une ligne en minuscules dans `skills/linkedin-coach/scripts/data/lexique-ia.fr.txt`
   ou `lexique-ia.en.txt` (un terme ou une expression par ligne).
2. Vérifiez qu'il ne pénalise pas un texte naturel :
   `python skills/linkedin-coach/scripts/humanizer.py detect tests/fixtures/humanizer/fr-naturel.txt`
3. `python -m unittest discover -s tests -p "test_humanizer.py"`. Un critère qui ne marche
   que dans une langue est un défaut (principe VII) : testez en FR **et** en EN.

## Avant d'ouvrir une PR

```
python tools/validate_skill.py --strict
python -m unittest discover -s tests -v
```

- Changement de comportement visible → une ligne dans `CHANGELOG.md`.
- Dans la description de la PR : une courte « Constitution Check » (quels principes sont
  concernés, et pourquoi c'est conforme).
- `SKILL.md` reste sous 150 lignes ; les détails vont dans `references/`.
- Aucune dépendance : Python, bibliothèque standard uniquement ; aucun accès réseau.
- Une évolution importante passe par Spec Kit : `/speckit-specify` → `/speckit-clarify` →
  `/speckit-plan` → `/speckit-tasks` → `/speckit-implement`.

---

# Contributing (English)

Thanks! The project follows a [constitution](.specify/memory/constitution.md): read
principles I to X before proposing a change. **Principles I (no scraping) and II (one
approval per action) are non-negotiable**: a PR adding scraping, third-party profile
reading, automatic publishing or writing without approval will be declined.

## Add a hook formula

Add a row to `skills/linkedin-coach/references/formules-accroche.md`, numbered in sequence,
with a `{variable}` in the template and a fictional example that doesn't end with a
question. Run `python -m unittest discover -s tests -p "test_formules.py"`.

## Add a humanizer lexicon term

Add a lowercase line to `skills/linkedin-coach/scripts/data/lexique-ia.en.txt` (or `.fr.txt`),
check it doesn't penalize a natural text, then run
`python -m unittest discover -s tests -p "test_humanizer.py"`. Test in English **and**
French (principle VII).

## Before opening a PR

Run `python tools/validate_skill.py --strict` and `python -m unittest discover -s tests -v`,
add a `CHANGELOG.md` line for any visible change, and include a short Constitution Check in
the PR description. No dependencies, no network access, `SKILL.md` under 150 lines.
