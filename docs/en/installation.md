# Installing LinkedIn Coach

Four methods; pick one. It takes under 2 minutes.

## 1. Claude Code: marketplace (recommended)

In a Claude Code session:

```
/plugin marketplace add mohamedchaabani/linkedin-coach
/plugin install linkedin-coach@linkedin-coach
```

Or in a terminal:

```
claude plugin marketplace add mohamedchaabani/linkedin-coach
claude plugin install linkedin-coach@linkedin-coach
```

Check with `claude plugin list`: `linkedin-coach@linkedin-coach` should be `enabled`.
The skill triggers on its own when you write, for example, "audit my LinkedIn profile".
The plugin also adds four commands: `/linkedin-coach:audit`, `/linkedin-coach:improve`,
`/linkedin-coach:post` and `/linkedin-coach:positioning`.

## 2. One command, for Claude Code and other agents

```
npx skills add mohamedchaabani/linkedin-coach
```

Requires Node.js. Works with agents that read the SKILL.md format.

## 3. Manual copy

Copy the repository's `skills/linkedin-coach/` folder into your skills folder:

| System | Folder |
|---|---|
| macOS, Linux | `~/.claude/skills/linkedin-coach/` |
| Windows | `%USERPROFILE%\.claude\skills\linkedin-coach\` |

Restart Claude Code.

## 4. Claude app (web, desktop, iPhone/iPad, Android)

1. Download `linkedin-coach-vX.Y.Z.zip` from the repository's latest GitHub release.
2. In the Claude app: **Customize → Skills → + → Create skill → Upload a skill**, then pick
   the .zip.
3. Turn the skill on. It is then available on all your devices.

Tip: create a dedicated **Claude project** ("LinkedIn Coach"). On first use, the skill gives
you a "positioning" block to paste into that project's instructions, so you don't answer
the same questions in every conversation.

## Updating

Use the same method as for installing:

| Method | Update |
|---|---|
| Marketplace | `claude plugin marketplace update linkedin-coach` then `claude plugin update linkedin-coach@linkedin-coach`, and restart the session |
| `npx skills add` | run `npx skills add mohamedchaabani/linkedin-coach` again |
| Manual copy | replace the `linkedin-coach/` folder with the new version's |
| Claude app | delete the old skill, upload the new .zip |

Your positioning and history are **not** touched: they live in `~/.linkedin-coach/` or in
your Claude project, never in the skill folder. If the format ever changes, the skill will
offer the migration and show you the result; it never changes anything silently.

## Python (optional)

The humanizer score and the LinkedIn archive import use Python ≥ 3.9 (no packages to
install). Without Python the skill still works: it does the pass by hand and tells you so.

- macOS, Linux: usually already installed (`python3 --version`).
- Windows: `winget install Python.Python.3.12`, or https://www.python.org/downloads/.

## Where is my data?

Your positioning and audit history are stored **outside the skill folder**, so an update
never erases them:

- Claude Code: `~/.linkedin-coach/` (Windows: `%USERPROFILE%\.linkedin-coach\`), or the
  folder set in the `LINKEDIN_COACH_HOME` environment variable.
- Claude app: in your dedicated Claude project's instructions.

Problem? See [troubleshooting.md](troubleshooting.md).
