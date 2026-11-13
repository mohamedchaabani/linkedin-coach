# Implementation Plan: LinkedIn Coach — skill open source pour Claude

**Branch**: `001-linkedin-coach-skill` | **Date**: 2026-11-12 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-linkedin-coach-skill/spec.md`

## Summary

Livrer un skill Claude unique, `linkedin-coach`, qui audite un profil LinkedIn (note /100) et
des posts (note /20), réécrit le profil, rédige des posts humanisés, et peut appliquer des
modifications de profil via un navigateur déjà connecté, avec une validation par action.

Approche technique : le skill est surtout du **contenu** (un `SKILL.md` court et des
références Markdown chargées à la demande), complété par deux outils locaux **optionnels** en
Python standard : l'humanizer bilingue et l'import de l'archive LinkedIn. Le dépôt sert à la
fois de marketplace et de plugin Claude Code. Il est aussi installable par `npx skills add`
et par copie, et il est publié en .zip pour l'app Claude. Les données de l'utilisateur
(positionnement, historique) vivent dans `~/.linkedin-coach/`, ou dans les instructions d'un
projet Claude. Détails et alternatives : [research.md](research.md).

## Technical Context

**Language/Version**: Markdown (contenu du skill) ; Python ≥ 3.9, bibliothèque standard uniquement (outils locaux optionnels, R1)

**Primary Dependencies**: aucune dépendance d'exécution ; Claude Code ou l'app Claude ; outil de navigation déjà connecté (optionnel, ex. Claude in Chrome)

**Storage**: fichiers Markdown dans `~/.linkedin-coach/` (surchargeable par `LINKEDIN_COACH_HOME`) ; instructions de projet Claude dans l'app (R3, R4)

**Testing**: `unittest` (stdlib) pour les scripts et la validation du skill ; `claude plugin eval` pour le comportement du skill (R8)

**Target Platform**: Claude Code sur macOS, Windows, Linux ; app Claude (web, desktop, iPhone/iPad, Android)

**Project Type**: skill / plugin Claude Code (contenu + petits outils CLI)

**Performance Goals**: installation < 2 min (NFR-001) ; `SKILL.md` ≤ 150 lignes ; humanizer < 1 s pour 3 000 caractères ; résumé d'archive borné (30 posts par défaut)

**Constraints**: aucun appel réseau ajouté ; aucun prérequis obligatoire au-delà de Claude Code (repli manuel sans Python) ; aucun script limité à un OS ; UTF-8 partout, y compris la console Windows

**Scale/Scope**: 1 skill, 3 modes ; environ 10 références ; 2 scripts ; 2 outils de dev ; 3 workflows CI ; documentation FR/EN

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe | Verdict (avant / après conception) | Comment le plan le respecte |
|---|---|---|
| I. Respect du compte et des CGU (NON NÉGOCIABLE) | ✅ / ✅ | Sources : archive, PDF, copier-coller, Analytics, navigateur sur son propre profil. Aucun code d'automatisation du navigateur ni de lecture de tiers (R7). `archive.py` ne suit aucun lien. |
| II. L'humain garde la main (NON NÉGOCIABLE) | ✅ / ✅ | Protocole d'une validation par modification, avec avant/après, relecture et annonce au réseau désactivée ([browser-write-protocol.md](contracts/browser-write-protocol.md)). Publication, messages et invitations interdits. Prouvé par des évaluations (R8). |
| III. Zéro invention | ✅ / ✅ | `{{à confirmer}}` dans le positionnement, les réécritures et les posts. Note sur le maximum atteignable si des critères ne sont pas évalués. Indicateurs « non calculables » plutôt qu'estimés ([data-model.md](data-model.md)). |
| IV. Vie privée locale | ✅ / ✅ | Données dans `~/.linkedin-coach/`, hors du skill. Historique sans texte du profil. Aucune télémétrie. Test qui bloque `socket` et vérification statique des imports. |
| V. Contenu tiers = donnée | ✅ / ✅ | Règle transverse du skill, signalement normalisé ([skill-interface.md](contracts/skill-interface.md)). Fixtures d'injection en évaluation (SC-009). |
| VI. Honnêteté avant flatterie | ✅ / ✅ | Grille reprise du prototype (« un premier passage tombe souvent entre 35 et 55 »). Incohérences, mode manuel ou outillé, limites des réécritures. |
| VII. Sonner humain FR/EN | ✅ / ✅ | Humanizer à 5 critères avec lexiques FR et EN séparés et critère « voix » bilingue (R6). Tests FR et EN en CI (SC-006). |
| VIII. Multiplateforme, installation simple | ⚠️ / ✅ justifié | Python n'est pas un prérequis de Claude Code : les outils sont optionnels, avec repli manuel annoncé (voir Complexity Tracking). Un seul langage, CI sur 3 OS, 4 canaux d'installation. |
| IX. Concision, chargement progressif | ✅ / ✅ | `SKILL.md` ≤ 150 lignes, vérifié par `validate_skill.py`. Références par mode (R10). Posts de 700 à 900 caractères. |
| X. Open source et attribution | ✅ / ✅ | MIT, `THIRD_PARTY_LICENSES.md`, crédits dans les README, en-têtes des fichiers adaptés (R11). Aucune dépendance. |
| Contraintes : SKILL.md standard, un langage, docs FR/EN, semver | ✅ / ✅ | R2, R1, `docs/fr` + `docs/en`, `release.yml` vérifie la cohérence des versions. |
| Workflow : CI 3 OS, Constitution Check, tests validation et réseau | ✅ / ✅ | `ci.yml` (3 OS × 2 versions de Python), `evals.yml`, `test_no_network`. |

**Résultat** : gate franchie. Un seul écart, justifié ci-dessous.

**Vérifié après implémentation (2026-11-12, T077)** :

- I : aucune lecture de tiers ni du fil ; `navigateur.md` et `posts.md` l'interdisent
  explicitement ; `archive.py` ne suit aucun lien (rendu texte testé).
- II : « une validation = une modification » dans `SKILL.md` et `navigateur.md` ; 6 cas
  d'évaluation `tests/evals/navigateur/`. **Reste à faire** : exécuter ces évaluations et le
  test manuel du quickstart §6.
- III : `{{à confirmer}}` partout ; affichage sur le maximum atteignable (FR-031) ;
  « non calculable » pour les indicateurs.
- IV : `test_no_network.py` (socket bloqué, imports interdits) et `validate_skill.py` ;
  données dans `~/.linkedin-coach/` (`test_isolation_donnees.py`).
- V : signalement normalisé dans `confidentialite.md` ; cas `import/a-injection`,
  `posts/g-commentaire-post-colle`.
- VI : sévérité dans `grille-profil.md` ; incohérences ; mode manuel/outillé annoncé.
- VII : humanizer bilingue, voix FR testée (SC-006 : `fr-naturel` voix 20/20, écart paire
  FR/EN 2 points).
- VIII : Python optionnel avec repli manuel ; CI 3 OS × 2 versions de Python ;
  `claude plugin validate .` passe.
- IX : `SKILL.md` 111 lignes ; 11 références chargées à la demande.
- X : MIT, `THIRD_PARTY_LICENSES.md` avec les deux notices, crédits dans les README.

## Project Structure

### Documentation (this feature)

```text
specs/001-linkedin-coach-skill/
├── plan.md              # Ce fichier
├── research.md          # Phase 0 : décisions R1 à R11
├── data-model.md        # Phase 1 : entités, états, règles
├── quickstart.md        # Phase 1 : scénarios de validation
├── contracts/
│   ├── skill-interface.md         # Déclenchement, modes, formats de sortie
│   ├── user-files.md              # positionnement.md, historique-audits.md
│   ├── scripts-cli.md             # humanizer.py, archive.py, outils de dev
│   └── browser-write-protocol.md  # Écriture validée via navigateur
├── checklists/requirements.md
└── tasks.md             # Phase 2 (/speckit-tasks)
```

### Source Code (repository root)

```text
.claude-plugin/
├── marketplace.json            # Marketplace pointant vers le plugin "./"
└── plugin.json                 # Métadonnées du plugin (nom, version, licence)

commands/                       # Commandes Claude Code (FR-008, ajoutées en 0.2.0)
├── audit.md                    # /linkedin-coach:audit
├── improve.md                  # /linkedin-coach:improve
├── post.md                     # /linkedin-coach:post
└── positioning.md              # /linkedin-coach:positioning

skills/linkedin-coach/          # Unique source du skill (plugin, npx, copie, .zip)
├── SKILL.md                    # ≤ 150 lignes : règles, détection mode/environnement, renvois
├── references/
│   ├── onboarding.md           # 7 questions, formats de bloc, mode local vs projet
│   ├── sources-profil.md       # Archive, PDF, copier-coller, Analytics, navigateur (lecture)
│   ├── grille-profil.md        # 12 critères, barème /100, non évalué
│   ├── audit-posts.md          # Note /20, indicateurs, seuil 10 posts, historique
│   ├── ameliorer.md            # Titre, Infos, expériences, compétences, sélection, bannière
│   ├── posts.md                # Piliers, cadence, règles de rédaction, fiche POST PRÊT
│   ├── formules-accroche.md    # ≥ 16 formules
│   ├── humanizer.md            # Passe manuelle et usage de l'outil
│   ├── navigateur.md           # Protocole d'écriture validée
│   └── confidentialite.md      # Anonymisation, contenu tiers = donnée
├── scripts/
│   ├── humanizer.py            # detect / clean, FR + EN
│   ├── archive.py              # Résumé Markdown de l'archive LinkedIn
│   └── data/
│       ├── lexique-ia.fr.txt
│       └── lexique-ia.en.txt
└── templates/
    ├── positionnement.md
    └── historique-audits.md

tests/
├── fixtures/                   # Archives anonymisées, textes FR/EN, injections
├── test_humanizer.py
├── test_archive.py
├── test_validate_skill.py
├── test_no_network.py
└── evals/                      # Suites claude plugin eval (validation, invention, injection)

tools/
├── validate_skill.py
└── build_zip.py

docs/
├── fr/  (installation.md, utilisation.md, depannage.md)
└── en/  (installation.md, usage.md, troubleshooting.md)

.github/workflows/
├── ci.yml                      # PR : 3 OS × Python 3.9/3.12
├── release.yml                 # Tag : .zip + release GitHub
└── evals.yml                   # Manuel : évaluations comportementales

README.md  README.en.md  LICENSE  THIRD_PARTY_LICENSES.md  CHANGELOG.md  CONTRIBUTING.md
.gitignore                      # .claude/settings.local.json, dist/, __pycache__/
```

**Structure Decision** : un seul dossier source, `skills/linkedin-coach/`, alimente les quatre
canaux d'installation (R2). Le prototype `SKILL.md` à la racine sera découpé dans
`references/`, puis supprimé de la racine. Sinon, deux `SKILL.md` du même nom coexisteraient,
et `npx skills add` pourrait choisir le mauvais. Les fichiers Spec Kit (`.specify/`,
`specs/`, `.claude/skills/speckit-*`) restent dans le dépôt comme outillage de
développement. Ils ne sont pas inclus dans le .zip.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Python ≥ 3.9 pour les outils, alors que le principe VIII interdit tout prérequis au-delà de Claude Code | Un score humanizer reproductible et testable en FR/EN (FR-061, SC-006, NFR-004), et un import d'archive borné. Python est le seul langage disponible à la fois dans l'app Claude et sur les 3 OS. | « Tout dans le modèle » : score non reproductible, non testable en CI. Node.js : absent de l'installeur natif de Claude Code et non garanti dans l'app. Écart limité : outils **optionnels**, repli manuel annoncé (FR-062), aucune fonctionnalité bloquée sans Python. |
