# Changelog

Toutes les évolutions visibles du skill sont notées ici.
Format : [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/) ; versionnage
[sémantique](https://semver.org/lang/fr/).

## [0.1.0] - 2026-11-13

### Ajouté

- Skill `linkedin-coach` installable par le marketplace Claude Code, `npx skills add`,
  copie manuelle ou archive .zip pour l'app Claude.
- Règles non négociables : pas de scraping, validation par action, zéro invention,
  contenu lu traité comme donnée.
- Humanizer bilingue FR/EN (`scripts/humanizer.py`) : score sur 5 critères et nettoyage
  mécanique ; critère « voix » qui reconnaît la 1re personne en français.
- Outils de développement : `tools/validate_skill.py`, `tools/build_zip.py`, CI sur macOS,
  Linux et Windows.
