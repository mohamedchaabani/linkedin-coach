# LinkedIn Coach

*[Version française](README.md)*

An open source skill for Claude that helps you **get found and contacted by recruiters and
clients** on LinkedIn: a scored audit of your profile and posts, ready-to-paste rewrites,
and short posts that don't sound like AI.

Free, MIT-licensed, no paid service and no dependencies. Works with Claude Code (macOS,
Windows, Linux) and in the Claude app (web, desktop, iPhone/iPad, Android).

## What the skill does

- **Audit**: profile score out of 100 (12 criteria), post score out of 20, inconsistencies
  spotted, top 3 fixes, progress since your last audit.
- **Improve**: headline, About section, experience, skills, Featured, banner,
  recommendation requests. With your consent, it can apply a change to your profile through
  your logged-in browser, **one approval per change**.
- **Posts**: content pillars, 3 hooks to choose from, a 700–900 character post built on
  **your** facts, a "POST READY" card and a before/after humanizer score.

## What it will never do

- Scrape LinkedIn, ask for your password, read other people's profiles or your feed.
- Publish, send a message or an invitation, or edit your profile without your explicit
  approval, one action at a time.
- Make up a number, a client or a result: anything missing becomes `{{à confirmer}}`
  ("to be confirmed").
- Send your data anywhere: your positioning stays on your machine (or in your Claude
  project). No telemetry.

## Quick install

Claude Code:

```
/plugin marketplace add mohamedchaabani/linkedin-coach
/plugin install linkedin-coach@linkedin-coach
```

Other methods (`npx skills add`, manual copy, .zip for the Claude app):
[docs/en/installation.md](docs/en/installation.md). Problems:
[docs/en/troubleshooting.md](docs/en/troubleshooting.md).

## Example requests

- "Audit my LinkedIn profile" (with your LinkedIn data archive, a PDF export or a
  copy-paste)
- "Rewrite my headline for solution architect roles in Geneva"
- "Write a post about the migration we finished last week"
- "Update my positioning"

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md): add a hook formula, a humanizer lexicon term, or fix
a rule. The project follows a [constitution](.specify/memory/constitution.md) and the
[Spec Kit](https://github.com/github/spec-kit) workflow.

## Credits

LinkedIn Coach is inspired by two MIT-licensed projects, credited in
[THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md):

- [sergebulaev/linkedin-skills](https://github.com/sergebulaev/linkedin-skills) (Sergey
  Bulaev): hook formulas and publishing rules.
- [Jakeschincariol/linkedin-agent-skill](https://github.com/Jakeschincariol/linkedin-agent-skill)
  (Jake Schincariol): profile scoring rubric and humanizer.

## License

[MIT](LICENSE).
