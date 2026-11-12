# Évaluations comportementales

Suites `claude plugin eval` qui vérifient le comportement du skill : validation par action
(principe II), zéro invention (principe III), contenu tiers = donnée (principe V), règles
de format. Elles lancent de vraies sessions Claude sur votre compte : elles **coûtent** des
appels au modèle. Ne les lancez pas à chaque modification.

```
claude plugin eval . --eval-dir tests/evals --runs 1 --no-publish
claude plugin eval . --eval-dir tests/evals --case "onboarding/*" --runs 3
```

En CI : `.github/workflows/evals.yml` (déclenchement manuel et avant release).

Structure : un dossier par cas, avec `prompt.md` (demande et frontmatter `max_turns`,
`allowed_tools`) et `graders/*.md` (critères jugés par un modèle). Les fixtures citées sont
dans `tests/fixtures/`.
