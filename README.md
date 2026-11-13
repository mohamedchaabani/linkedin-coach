# LinkedIn Coach

*[Version française](README.fr.md)*

An open source skill for Claude that helps you **get found and contacted by recruiters and
clients** on LinkedIn: a scored audit of your profile and posts, ready-to-paste rewrites,
and short posts that don't sound like AI.

Free, MIT-licensed, no paid service and no dependencies. Works with Claude Code (macOS,
Windows, Linux) and in the Claude app (web, desktop, iPhone/iPad, Android). Paired with
**Claude in Chrome**, it can read your own profile and apply the changes you approve.

## What the skill does

- **Audit**: profile score out of 100 (12 criteria), post score out of 20, inconsistencies
  spotted, top 3 fixes, progress since your last audit.
- **Improve**: headline, About section, experience, skills, Featured, banner,
  recommendation requests. With Claude in Chrome connected, it can apply a change to your
  profile, **one approval per change**.
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

## Requirements

| What | Needed for | Required? |
|---|---|---|
| A Claude account (Pro, Max, Team or Enterprise) | Using the skill | Yes |
| [Claude Code](https://docs.claude.com/en/docs/claude-code) **or** the Claude app | Running the skill | One of the two |
| Google Chrome + the [Claude in Chrome](https://claude.com/chrome) extension | Reading your profile and applying changes for you | Optional |
| Python ≥ 3.9 (standard library only) | Humanizer score and LinkedIn archive import | Optional: without it, the skill does these steps by hand and tells you so |

## Install

### Claude Code (recommended)

In a Claude Code session:

```
/plugin marketplace add mohamedchaabani/linkedin-coach
/plugin install linkedin-coach@linkedin-coach
```

Check with `/plugin`: `linkedin-coach` should be enabled. The skill triggers on its own
when you write "audit my LinkedIn profile", or you can call it with
`/linkedin-coach:linkedin-coach`.

### Claude app (web, desktop, mobile)

1. Download `linkedin-coach-vX.Y.Z.zip` from the
   [latest release](https://github.com/mohamedchaabani/linkedin-coach/releases/latest).
2. In the Claude app: **Customize → Skills → + → Create skill → Upload a skill**, then pick
   the .zip.
3. Turn the skill on.
4. Create a **Claude project** named "LinkedIn Coach" and open your conversations there: the
   skill will ask you to paste your positioning into the project instructions once.

Other methods (`npx skills add`, manual copy), updating, and where your data lives:
[docs/en/installation.md](docs/en/installation.md).

### Optional: connect Claude in Chrome

Without a browser, the skill gives you **text to copy and paste** into LinkedIn yourself.
With Claude in Chrome, it can **open your own profile to read it** and **apply each change
you approve**.

1. Install the [Claude in Chrome](https://claude.com/chrome) extension and sign in with
   the same Claude account.
2. In that Chrome window, log in to LinkedIn yourself. The skill never asks for your
   password.
3. In Claude Code, run `/chrome` (or start with `claude --chrome`) to connect the browser.
4. When the extension asks, allow it on `linkedin.com`.

What it may do in the browser: read **your** profile, and edit your headline, About,
experience descriptions, skills, Featured section or custom URL, **after a "yes" for that
specific change**. What it never does: publish, comment, react, send messages or
invitations, browse other profiles or your feed, or change account settings. The "share
with network" option stays off unless you explicitly ask for it.

## Step-by-step tutorial

### Step 1: start

Open Claude Code (or your "LinkedIn Coach" project in the Claude app) and write:

> Audit my LinkedIn profile

### Step 2: answer the positioning questions (first time only)

The skill asks **at most 7 questions in one message**:

1. Role and seniority (e.g. "AEM architect, 12 years")
2. 3 to 5 key areas of expertise
3. Certifications, with the date earned (`YYYY-MM`) and the expiry date if any
4. **Your LinkedIn profile URL**: see below
5. Target: roles, contract types, cities, remote (yes / no / hybrid)
6. Real work you can talk about: projects, tools, **true** numbers
7. Preferred language for your texts: `fr` or `en`

**Finding your LinkedIn URL:** on LinkedIn, click **Me → View profile**, then copy the
address bar. It looks like `https://www.linkedin.com/in/your-name/`. Paste it as is.

Skip anything you don't know: it becomes `{{à confirmer}}`, never a guess. The skill then
saves your positioning:

- **Claude Code**: in `~/.linkedin-coach/positionnement.md` (it asks first).
- **Claude app**: it gives you a block to paste into the project instructions. You won't be
  asked these questions again.

### Step 3: give it your profile

Pick **one** source. The more complete, the better the audit.

| Source | How | What it contains |
|---|---|---|
| **Claude in Chrome** (fastest) | Say "read my profile in Chrome". The skill opens the URL from step 2, **reads only**, clicks nothing | Everything visible on your profile |
| **LinkedIn data archive** (most complete) | LinkedIn → **Me → Settings & Privacy → Data privacy → Get a copy of your data** → tick Profile, Positions, Skills, Recommendations, Certifications, Shares → Request archive. LinkedIn emails it (minutes to 24 h). Give the .zip to Claude | Profile, experience, skills, recommendations, your posts. No photo, banner, Featured or post stats |
| **PDF export** | On your profile: **More → Save to PDF**, then attach the file | Headline, About, experience, top skills, education |
| **Copy-paste** | Paste the sections into the chat | Good for a targeted request ("rewrite my headline") |

For **post statistics**, add the Analytics export (**Analytics → Content → Export**,
saved as CSV if the .xlsx won't open) or screenshots. The skill never estimates a number it
can't read.

### Step 4: read your audit

```
PROFILE SCORE  47/100        POST SCORE  9/20
(12/12 criteria scored)      (14 posts)

  headline           4/12   job title only, no target keyword, no proof
  banner             not scored (not provided)
  ...
INCONSISTENCIES      ...
TOP 3 FIXES          (by points lost)
PROGRESS             (if a previous audit exists)
```

Scores are strict on purpose. A section you didn't provide is marked "not scored", never
guessed.

### Step 5: improve your profile

Say "yes" when the skill offers to continue, or ask directly:

> Rewrite my headline for solution architect roles in Geneva

It works **one section at a time**, starting with the one that lost the most points. For
each one you get a ready-to-paste block. If Claude in Chrome is connected:

1. It shows the **current** text (read on the page) and the **proposed** text.
2. It asks: *"Shall I apply this new headline to your profile? (yes / no)"*
3. Only a clear **"yes"** to that exact question counts. "ok", "apply everything" or
   silence do not: "apply everything" means it asks again, change by change.
4. It applies the text, re-reads the page and tells you "matches" or shows the difference.

### Step 6: write posts

> Write a post about the migration we finished last week

If the idea is vague, it asks one grouped question to get a **true, specific fact**. You
get 3 hooks, a 700–900 character post and a "POST READY" card with the humanizer score.
**You publish it yourself**: the skill never posts.

### Step 7: track your progress

Run "Audit my LinkedIn profile" again in a few weeks. The skill compares with your last
audit and shows what improved. To change your target or details at any time:

> Update my positioning: add Geneva

More examples and what the skill refuses: [docs/en/usage.md](docs/en/usage.md).

## Troubleshooting

See [docs/en/troubleshooting.md](docs/en/troubleshooting.md).

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
