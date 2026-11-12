# Troubleshooting

## The skill doesn't show up in Claude Code

- `claude plugin list`: `linkedin-coach@linkedin-coach` should be `enabled`. Otherwise:
  `claude plugin enable linkedin-coach@linkedin-coach`.
- After installing or copying, restart the session (or run `/reload-plugins`).
- Manual copy: the file must be exactly `~/.claude/skills/linkedin-coach/SKILL.md`
  (not `…/linkedin-coach/linkedin-coach/SKILL.md`).

## The Claude app rejects the .zip

- Use the release .zip, not GitHub's "Source code" archive: the .zip root must be the
  `linkedin-coach/` folder.
- If you build the .zip yourself, zip the **folder** `linkedin-coach`, not its contents, or
  run `python tools/build_zip.py`.

## "Python not found" / manual pass

The skill tries `python3`, then `python`, then `py -3`. Check:

```
python3 --version
python --version
py -3 --version
```

On Windows, if `python` opens the Microsoft Store, install Python
(`winget install Python.Python.3.12`) and reopen the terminal. Without Python everything
still works: only the humanizer score is replaced by a manual pass.

## Broken accents in the Windows console

The scripts write UTF-8. If the console shows `Ã©` instead of `é`:

```
set PYTHONIOENCODING=utf-8          (cmd)
$env:PYTHONIOENCODING = "utf-8"     (PowerShell)
```

## The skill keeps asking the onboarding questions

- Claude Code: check that `~/.linkedin-coach/positionnement.md` exists (Windows:
  `%USERPROFILE%\.linkedin-coach\positionnement.md`) and starts with
  `<!-- linkedin-coach:positionnement v1 -->`. If you use `LINKEDIN_COACH_HOME`, make sure
  it is set in the session.
- Claude app: open the conversation **inside** the project whose instructions contain the
  positioning block.
