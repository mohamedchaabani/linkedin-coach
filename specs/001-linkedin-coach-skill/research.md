# Phase 0 — Recherche et décisions : LinkedIn Coach

**Feature** : `001-linkedin-coach-skill` | **Date** : 2026-11-12 | **Plan** : [plan.md](plan.md)

Chaque point résout une inconnue du Technical Context. Les points marqués « à vérifier en
implémentation » reposent sur des formats d'outils tiers susceptibles d'évoluer ; une tâche
dédiée les confirmera sur la version courante avant d'écrire le code.

---

## R1. Langage des outils locaux

- **Décision** : Python ≥ 3.9, **bibliothèque standard uniquement** (aucun `pip install`).
  Les outils sont **optionnels** : si Python est absent, le skill fait la passe à la main et
  le dit (FR-062).
- **Justification** :
  - L'environnement d'exécution de code de l'app Claude (web, desktop, mobile) fournit
    Python : c'est le seul langage utilisable à la fois dans l'app et dans Claude Code.
  - Python est natif sur macOS et la plupart des Linux ; sous Windows il s'installe en une
    commande, et le repli manuel garantit que le skill reste utilisable sans lui
    (principe VIII : aucun prérequis *obligatoire* au-delà de Claude Code).
  - Le `detect.py` de li-human (MIT) est en Python : reprise et extension FR facilitées.
  - Un seul langage pour les 3 OS, conforme à la contrainte « pas de bash seul ni de
    PowerShell seul ».
- **Alternatives rejetées** :
  - Node.js : présent si Claude Code est installé via npm, mais plus via l'installeur
    natif ; disponibilité moins sûre dans le bac à sable de l'app Claude.
  - Bash + PowerShell : deux implémentations à maintenir, interdit par la constitution.
  - Aucun script (tout dans le modèle) : un score humanizer non outillé n'est pas
    reproductible et ne peut pas être testé en CI (NFR-004, SC-006).
- **Invocation multiplateforme** : le SKILL.md essaie `python3`, puis `python`, puis
  `py -3`, et bascule en passe manuelle si aucun ne répond.

## R2. Distribution : plugin Claude Code, `npx skills add`, .zip pour l'app

- **Décision** : le dépôt est à la fois **un marketplace et un plugin** Claude Code, avec le
  skill dans `skills/linkedin-coach/`.
  - `.claude-plugin/marketplace.json` déclare un plugin `linkedin-coach` dont la source est
    la racine du dépôt (`"./"`).
  - `.claude-plugin/plugin.json` décrit le plugin ; Claude Code découvre automatiquement
    `skills/*/SKILL.md`.
  - Installation : `/plugin marketplace add <owner>/linkedin-coach` puis
    `/plugin install linkedin-coach@linkedin-coach`.
  - `npx skills add <owner>/linkedin-coach` détecte `skills/linkedin-coach/SKILL.md`.
  - Installation manuelle : copier `skills/linkedin-coach/` dans `~/.claude/skills/`
    (macOS/Linux) ou `%USERPROFILE%\.claude\skills\` (Windows).
  - Release : `linkedin-coach-vX.Y.Z.zip` dont la racine est le dossier `linkedin-coach/`
    contenant `SKILL.md` (format attendu par l'import Skills de l'app Claude).
- **Justification** : un seul dossier source sert les quatre canaux ; aucune duplication.
- **Alternatives rejetées** : dossier `plugins/linkedin-coach/` séparé (chemin plus long
  pour l'installation manuelle, sans bénéfice pour un seul plugin).
- **À vérifier en implémentation** : schéma exact de `marketplace.json`/`plugin.json` et
  structure attendue du .zip, sur les versions courantes de Claude Code et de l'app.

- **Vérifié le 2026-11-12 (T003, T004)** :
  - `marketplace.json` exige `name`, `owner` (`{name}`) et `plugins[]` (`name`, `source`,
    `description` optionnelle). Un `source` relatif part de la racine du marketplace et ne
    doit pas contenir `..` ; `"./"` est donc admis. Le nom de l'entrée doit être identique au
    `name` du `plugin.json`. Les skills d'un plugin sont préfixés par le nom du plugin
    (`/linkedin-coach:linkedin-coach`). Contrôle : `claude plugin validate .`.
  - Import dans l'app Claude (Customize → Skills → + → Upload a skill) : « The ZIP should
    contain the skill folder as its root (not a subfolder) » ; le nom du dossier doit être
    celui du skill ; `name` ≤ 64 caractères, **`description` ≤ 200 caractères** (limite plus
    stricte que les 1 024 du format SKILL.md : le validateur applique 200).

## R3. Emplacement du positionnement et de l'historique (Claude Code)

- **Décision** : dossier utilisateur `~/.linkedin-coach/` (Windows :
  `%USERPROFILE%\.linkedin-coach\`), surchargeable par la variable d'environnement
  `LINKEDIN_COACH_HOME`. Deux fichiers Markdown lisibles :
  `positionnement.md` et `historique-audits.md` (format : [contracts/user-files.md](contracts/user-files.md)).
- **Justification** :
  - Hors du dossier du skill : une mise à jour par plugin, `npx` ou copie ne l'écrase
    jamais (FR-021, SC-004).
  - Markdown : Claude le lit et l'écrit avec ses outils de fichiers, sans script ; l'utilisateur
    peut l'ouvrir et le corriger.
  - Le même texte sert de bloc à coller dans un projet Claude (FR-023, FR-037) : un seul
    format pour les deux environnements.
- **Alternatives rejetées** : JSON (moins lisible, et inutile car pas de traitement
  machine) ; dossier `~/.claude/` (mélange avec la config de Claude Code) ; mémoire de Claude
  (non garantie, rejetée en clarification).

## R4. Détection de l'environnement (Claude Code ou app Claude)

- **Décision** : le skill tente de lire `~/.linkedin-coach/positionnement.md`. S'il a accès
  au système de fichiers de l'utilisateur, il est en mode **local** ; sinon (ou si le
  dossier personnel est un bac à sable éphémère), il est en mode **projet** et cherche un
  bloc `<!-- linkedin-coach:positionnement -->` dans les instructions du projet ou la
  conversation.
- **Justification** : pas de détection fragile par variable d'environnement ; on se fie à
  ce qui est réellement disponible.
- **À vérifier en implémentation** : comportement de l'écriture de fichiers dans le bac à
  sable de l'app Claude (fichier non persistant) ; le skill doit alors privilégier le bloc.

## R5. Import de l'archive officielle LinkedIn

- **Décision** : script `archive.py` qui lit l'archive (.zip ou dossier extrait) avec
  `zipfile` et `csv`, et produit un **résumé Markdown** des sections reconnues et de la
  liste des sections absentes.
- **Fichiers attendus** (noms anglais de l'archive) : `Profile.csv`, `Positions.csv`,
  `Skills.csv`, `Certifications.csv`, `Recommendations_Received.csv`, `Education.csv`,
  `Shares.csv` ; tolérance aux variantes (casse, espaces, sous-dossiers, BOM UTF-8).
- **Justification** : l'archive peut contenir des milliers de lignes (`Shares.csv`) ; un
  résumé borné évite de saturer le contexte et rend l'import testable.
- **Sans Python** : Claude lit directement les CSV listés ; même règle « non fournie » pour
  ce qui manque.
- **Alternatives rejetées** : demander à l'utilisateur de copier les CSV (fastidieux, US3).
- **À vérifier en implémentation** : noms de fichiers et colonnes sur une archive récente
  (ils changent parfois) ; tests sur fixtures anonymisées.

## R6. Humanizer bilingue FR/EN

- **Décision** : script `humanizer.py` avec deux sous-commandes : `detect` (score) et
  `clean` (corrections mécaniques sûres). Lexiques séparés en fichiers de données
  `lexique-ia.fr.txt` et `lexique-ia.en.txt` (contribuables, NFR-005).
- **5 critères, notés chacun sur 20, total sur 100** :
  1. **Ponctuation** : tirets cadratins (> 1 pour 100 mots), guillemets courbes, caractères
     invisibles, emojis génériques.
  2. **Vocabulaire IA** : occurrences des lexiques FR et EN.
  3. **Tournures** : triades, « ce n'est pas X, c'est Y », « Le résultat ? », « Plot twist »,
     ouvertures en question.
  4. **Rythme** : variance de la longueur des phrases et des puces (uniformité pénalisée).
  5. **Voix** : présence de la 1re personne (`je`, `j'`, `nous`, `on`, `I`, `we`), des
     contractions EN et d'élisions FR ; détection de langue par fréquence de mots outils.
- **`clean`** ne fait que des corrections mécaniques sans changer le sens (tirets cadratins,
  guillemets, invisibles, espaces) ; les reformulations restent faites par Claude.
- **Justification** : corrige le défaut connu de `detect.py` dont le critère « voix » sous-note
  le français (principe VII, SC-006).
- **Alternatives rejetées** : reprendre `detect.py` tel quel (biais anglais) ; dépendance
  NLP (spaCy…) : interdit (stdlib seule, installation < 2 min).

## R7. Écriture sur LinkedIn via le navigateur connecté

- **Décision** : aucun code. Un protocole en référence (`references/navigateur.md`) que
  Claude suit avec l'outil de navigation déjà connecté (ex. Claude in Chrome). Protocole
  détaillé : [contracts/browser-write-protocol.md](contracts/browser-write-protocol.md).
- **Points clés** : une modification = une validation ; avant/après exact affiché ;
  annonce au réseau désactivée ; relecture après écriture (FR-015) ; arrêt et texte à copier
  en cas d'échec ; jamais de publication, message ou invitation.
- **Justification** : les sélecteurs de l'interface LinkedIn changent souvent ; un
  protocole lu par le modèle s'adapte, un script d'automatisation casserait et serait
  assimilable à du scraping (principe I).
- **Alternatives rejetées** : automatisation par script de navigateur (contraire aux
  principes I et VIII) ; API LinkedIn (hors périmètre v1).

## R8. Tests du comportement du skill (validation, zéro invention, injection)

- **Décision** : deux niveaux.
  1. **Tests unitaires** (`unittest`, stdlib) des scripts : humanizer FR/EN, import
     d'archive, validation du SKILL.md, absence d'appel réseau. Exécutés à chaque PR sur
     ubuntu, macOS et Windows.
  2. **Évaluations comportementales** du skill avec `claude plugin eval` : scénarios
     (prompts + contenus de test) et assertions sur la réponse. Couvrent FR-013 (validation
     par action), SC-007, SC-008 (zéro invention), SC-009 (injection), FR-031 (non évaluée).
     Exécutées en déclenchement manuel et avant chaque release (elles consomment des
     appels au modèle et demandent une clé API en secret CI).
- **Preuve « aucun appel réseau caché »** (principe IV) : test qui remplace
  `socket.socket` par une fonction qui lève une erreur pendant l'exécution des scripts,
  plus une vérification statique interdisant les imports `socket`, `urllib`, `http`,
  `ssl`, `ftplib`, `smtplib` dans `skills/`.
- **À vérifier en implémentation** : format des suites `claude plugin eval` et
  possibilité de simuler l'outil de navigation (sinon : scénario simulé où le modèle doit
  produire la demande de validation avant tout appel d'écriture, plus test manuel guidé dans
  [quickstart.md](quickstart.md)).
- **Vérifié le 2026-11-12 (T005)** : `claude plugin eval [target]` (Claude Code 2.1.296)
  lit `<eval dir>/**/prompt.md` (frontmatter `max_turns`, `allowed_tools`) et
  `graders/*.md` (frontmatter `type: llm`, `weight`) ou `case.yaml`. Options utiles :
  `--eval-dir`, `--runs`, `--threshold`, `--trust-plugin` (CI), `--max-cost-usd`,
  `--no-publish`. Les outils MCP (navigateur) sont remplacés par des *mocks* enregistrés
  (`<eval dir>/mocks/`) ; un outil de navigation réel n'est pas lancé par défaut. Décision :
  les suites vivent dans `tests/evals/` et sont lancées avec `--eval-dir tests/evals` ; les
  scénarios d'écriture sont jugés sur la réponse (validation demandée avant toute action) et
  complétés par le test manuel guidé du quickstart §6.
- **Alternatives rejetées** : pytest (dépendance de dev évitable) ; évals à chaque PR
  (coût et secret exposés aux PR externes).

## R9. CI et release

- **Décision** : GitHub Actions.
  - `ci.yml` (chaque PR et push) : matrice `ubuntu-latest`, `macos-latest`,
    `windows-latest` × Python 3.9 et 3.12 ; lance `tools/validate_skill.py`, les tests
    unitaires, et `tools/build_zip.py` (vérifie que le .zip se construit).
  - `release.yml` (tag `vX.Y.Z`) : construit le .zip, vérifie que la version du tag
    correspond à `plugin.json` et au CHANGELOG, crée la release GitHub avec le .zip.
  - `evals.yml` (manuel) : évaluations comportementales.
- **Justification** : couvre NFR-003 et NFR-004 et le workflow de la constitution.

## R10. Découpage du contenu (chargement progressif)

- **Décision** : `SKILL.md` ≤ 150 lignes : objectif, règles non négociables, détection du
  mode et de l'environnement, puis renvois vers `references/`. Le contenu du prototype
  `SKILL.md` actuel est redistribué dans les références (grille, formules, règles de
  rédaction, humanizer). Les références sont rédigées en français ; les textes destinés à
  l'utilisateur suivent sa langue (FR-080).
- **Justification** : principe IX, NFR-002.

## R11. Attribution et licences

- **Décision** : `LICENSE` (MIT), `THIRD_PARTY_LICENSES.md` reprenant les notices MIT de
  sergebulaev/linkedin-skills et Jakeschincariol/linkedin-agent-skill, et section
  « Crédits » dans les deux README. Chaque fichier repris ou adapté le mentionne en en-tête.
- **Vérifié le 2026-11-12 (T006)** : sergebulaev/linkedin-skills : MIT, « Copyright (c) 2026
  Sergey Bulaev » (20 formules d'accroche dans le skill Post Writer).
  Jakeschincariol/linkedin-agent-skill : MIT, « Copyright (c) 2026 Jake Schincariol »
  (`skills/li-post/hooks.json`, `skills/li-human/{slop.json,humanize.py,detect.py}`,
  `skills/li-profile/rubric.json`). Aucun fichier de ces dépôts n'est copié tel quel : la
  grille, les formules et le lexique sont réécrits à partir du prototype, avec attribution.
