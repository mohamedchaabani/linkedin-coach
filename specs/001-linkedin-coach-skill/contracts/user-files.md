# Contrat : fichiers utilisateur (positionnement et historique)

Ces fichiers sont l'interface stable entre les versions du skill : une mise à jour du skill
MUST savoir lire tout fichier écrit par une version antérieure de même `version_format`.

## Emplacement

| Environnement | Emplacement |
|---|---|
| Claude Code (macOS, Linux) | `$LINKEDIN_COACH_HOME` sinon `~/.linkedin-coach/` |
| Claude Code (Windows) | `%LINKEDIN_COACH_HOME%` sinon `%USERPROFILE%\.linkedin-coach\` |
| App Claude | Instructions du projet Claude dédié (bloc à coller) |

Le skill ne crée ce dossier qu'avec l'accord de l'utilisateur au premier enregistrement.

## `positionnement.md`

Le même texte sert de fichier local et de bloc à coller dans un projet Claude. Les balises de
début et de fin permettent de le retrouver dans des instructions de projet plus longues.

```markdown
<!-- linkedin-coach:positionnement v1 -->
# Positionnement LinkedIn Coach

- Langue : fr
- Rôle et séniorité : Architecte AEM, 12 ans
- Expertises : AEM ; architecture cloud ; IA générative en entreprise
- Certifications :
  - Adobe Certified Expert AEM Sites Architect (obtenue 2023-05, expire 2025-05)
- URL : https://www.linkedin.com/in/exemple
- Cible :
  - Postes : Architecte solution ; Tech lead AEM
  - Contrats : CDI ; freelance
  - Villes : Paris ; Genève
  - Remote : hybride
- Terrain réel :
  - Migration AEM 6.5 → AEM as a Cloud Service pour {{à confirmer}}
- Références clients : une banque européenne ; un grand groupe industriel
- Piliers :
  - Terrain métier : retours d'expérience AEM
  - IA × métier : ce qui marche en production
- Mis à jour le : 2026-11-12
<!-- /linkedin-coach:positionnement -->
```

Règles :
- Les libellés de champ sont fixes (français) quelle que soit la `Langue`.
- Listes sur une ligne séparées par ` ; `, ou en sous-puces.
- Une valeur inconnue s'écrit `{{à confirmer}}`.
- Une ligne inconnue est conservée telle quelle à la réécriture (compatibilité ascendante).

## `historique-audits.md`

```markdown
<!-- linkedin-coach:historique v1 -->
# Historique des audits LinkedIn Coach

| Date | Profil | Critères évalués | Posts | Corrections prioritaires |
|---|---|---|---|---|
| 2026-11-12 | 47/100 | 12/12 | 9/20 | Titre sans mot-clé ; Infos sans preuve ; 0 recommandation récente |
| 2026-12-03 | 64/100 | 12/12 | 12/20 | Bannière par défaut ; activité irrégulière ; compétences non épinglées |
<!-- /linkedin-coach:historique -->
```

Règles :
- Une ligne par audit, ajoutée en fin de tableau ; les lignes passées ne sont jamais modifiées.
- `Profil` = `points/maximum atteignable` (`/100` quand les 12 critères sont évalués, par
  ex. `41/88` sinon) ; vide (`—`) si aucun critère évalué ; `Posts` vide (`—`) si aucun post fourni.
- Aucun extrait du profil ou des posts (FR-035).
- Dans l'app Claude, le skill fournit le bloc complet mis à jour, à coller à la place de
  l'ancien dans les instructions du projet.
