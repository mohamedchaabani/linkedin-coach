# Dépannage

## Le skill n'apparaît pas dans Claude Code

- `claude plugin list` : `linkedin-coach@linkedin-coach` doit être `enabled`. Sinon :
  `claude plugin enable linkedin-coach@linkedin-coach`.
- Après une installation ou une copie manuelle, redémarrez la session (ou `/reload-plugins`).
- Copie manuelle : le fichier doit être exactement `~/.claude/skills/linkedin-coach/SKILL.md`
  (pas `…/linkedin-coach/linkedin-coach/SKILL.md`).

## L'app Claude refuse le .zip

- Utilisez le .zip de la release, pas l'archive « Source code » de GitHub : la racine du .zip
  doit être le dossier `linkedin-coach/`.
- Si vous refaites le .zip vous-même, zippez le **dossier** `linkedin-coach`, pas son
  contenu, ou lancez `python tools/build_zip.py`.

## « Python introuvable » / passe manuelle

Le skill essaie `python3`, puis `python`, puis `py -3`. Vérifiez :

```
python3 --version
python --version
py -3 --version
```

Sous Windows, si `python` ouvre le Microsoft Store, installez Python
(`winget install Python.Python.3.12`) puis rouvrez le terminal. Sans Python, tout marche
quand même : seul le score humanizer est remplacé par une passe manuelle.

## Accents cassés dans la console Windows

Les scripts écrivent en UTF-8. Si la console affiche `Ã©` au lieu de `é` :

```
set PYTHONIOENCODING=utf-8          (cmd)
$env:PYTHONIOENCODING = "utf-8"     (PowerShell)
```

## Le skill repose les questions d'onboarding

- Claude Code : vérifiez que `~/.linkedin-coach/positionnement.md` existe (Windows :
  `%USERPROFILE%\.linkedin-coach\positionnement.md`) et commence par
  `<!-- linkedin-coach:positionnement v1 -->`. Si vous utilisez `LINKEDIN_COACH_HOME`,
  vérifiez qu'elle est définie dans la session.
- App Claude : la conversation doit être ouverte **dans** le projet dont les instructions
  contiennent le bloc de positionnement.
