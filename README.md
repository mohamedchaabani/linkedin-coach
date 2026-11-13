# LinkedIn Coach

*[Version française](README.fr.md)*

**A LinkedIn coach that remembers you, scores you, tracks your progress, and writes posts
that don't sound like AI.**

An open source skill for Claude that helps you **get found and contacted by recruiters and
clients** on LinkedIn: a scored audit of your profile and posts, ready-to-paste rewrites,
and short posts built on your real work.

Free, MIT-licensed, no paid service and no dependencies. Works with Claude Code (macOS,
Windows, Linux) and in the Claude app (web, desktop, iPhone/iPad, Android). Paired with
**Claude in Chrome**, it can read your own profile and apply the changes you approve.

## Why not just ask Claude?

You still talk to Claude in plain language. The skill changes what Claude does with it:

| | Claude on its own | With LinkedIn Coach |
|---|---|---|
| **Memory** | Asks who you are in every conversation | 7 questions once; your positioning is saved and reused |
| **Scoring** | A different, vague opinion each time | Profile out of 100 on a fixed 12-criteria rubric, posts out of 20 |
| **Progress** | No history | Every audit is logged; you see your score move from one audit to the next |
| **AI-sounding text** | Generic phrasing, AI vocabulary | Humanizer pass with a before/after score (5 criteria, FR and EN lexicons) |
| **Facts** | Tends to embellish ("+40% performance") | Nothing made up: missing data becomes `{{à confirmer}}` |
| **Your data** | You paste sections by hand | Reads the official LinkedIn data archive directly |
| **Acting on your profile** | — | With Claude in Chrome: applies each change after your "yes", then checks it on the page. Never publishes |
| **Shortcuts** | Free-form chat only | Dedicated commands: `/linkedin-coach:audit`, `:improve`, `:post`, `:positioning` |
| **Method** | General advice | 20 hook formulas, LinkedIn format rules, fixes ordered by points lost, strict scores |

## Before / after: a real profile

The author ran the skill on their own LinkedIn profile (AEM architect, November 2026),
then applied the changes through Claude in Chrome. Employer names are anonymized. Every
number below was **supplied by the author**: the skill asked for them instead of making
them up.

### Score

| Criterion | Before | After | What changed |
|---|---|---|---|
| About: body | 9/10 | **10/10** | A measured result added |
| Featured | 3/8 | **8/8** | 1 item → 3: best post, a proof, a contact |
| Other criteria | 67 | 67 | Unchanged |
| **Profile score** | **79/100** | **85/100** | |

Still open, and the skill says so: results with numbers for the current role (+6) and a
headline that says who the work was for (+3).

### Experience: tasks become results

| | Before | After |
|---|---|---|
| Hotel group | Designed the target architecture and a new middleware layer, improving site performance | Designed the target architecture and a new middleware layer: **a daily job dropped from 6 h to 5 min** and no longer ties up the AEM author instances |
| Luxury brand | *(nothing on delivery)* | Set up a GitLab CI/CD delivery workflow: **preparing a release dropped from 2 days to half a day**, from release creation to production deployment |

### About: one proof with a number

- Before: *At [hotel group], I moved the international hotel brands' websites from legacy
  CMS platforms to AEM as a Cloud Service.*
- After: *At [hotel group], I moved the international hotel brands' websites from legacy
  CMS platforms to AEM as a Cloud Service, **with a middleware layer that cut a daily job
  from 6 hours to 5 minutes**.*

### Featured

| Before | After |
|---|---|
| Portfolio link | 1. Best post by engagement (certification announcement, 3.5% engagement) |
| | 2. Proof: this open source project |
| | 3. Portfolio link (contact) |

### A post (in French: the skill writes in your language)

The weakest of the author's recent posts, before and after the humanizer pass (changed
lines only). No fact was added. Scores measured by `scripts/humanizer.py`.

| Before: **82/100** | After: **93/100** |
|---|---|
| Je viens de découvrir un outil open source qui vaut le détour : OmniRoute. | Je viens de découvrir OmniRoute. Un outil open source qui vaut le détour. |
| Ce qui change tout : dès que tu tapes dans un quota, il bascule automatiquement sur un autre modèle. Fini de s'arrêter en plein milieu d'une session de code. | Ce qui m'intéresse le plus : quand tu atteins un quota, il bascule tout seul sur un autre modèle, et tu ne t'arrêtes plus en pleine session de code. |
| 100 % open source, tout tourne en local, rien n'est envoyé ailleurs. | 100 % open source. Tout tourne en local. |
| Ça montre bien à quelle vitesse évolue **l'écosystème** autour du coding assisté par IA. | Pour moi, ça montre la vitesse à laquelle bougent les outils de code assisté par IA. |
| *(no question)* | Et vous, vous changez de modèle à la main quand le quota tombe ? |

What changed: "écosystème" (a typical AI word) removed, a first-person voice, more varied
sentence lengths, and a closing question that invites comments.

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
when you write "audit my LinkedIn profile", or you can use its commands:

| Command | What it does |
|---|---|
| `/linkedin-coach:audit` | Scored audit of your profile and posts |
| `/linkedin-coach:improve [section and goal]` | Rewrite a section, e.g. `headline for architect roles in Geneva` |
| `/linkedin-coach:post [fact]` | Write a post, e.g. `the AEM migration we finished last week` |
| `/linkedin-coach:positioning [change]` | Show or update your positioning, e.g. `add Geneva` |

In the Claude app, commands aren't available: just write your request in plain language.

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

In Claude Code you can also type `/linkedin-coach:audit`. Each step below gives the
matching command.

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

Command: `/linkedin-coach:improve headline for solution architect roles in Geneva`.

It works **one section at a time**, starting with the one that lost the most points. For
each one you get a ready-to-paste block. If Claude in Chrome is connected:

1. It shows the **current** text (read on the page) and the **proposed** text.
2. It asks: *"Shall I apply this new headline to your profile? (yes / no)"*
3. Only a clear **"yes"** to that exact question counts. "ok", "apply everything" or
   silence do not: "apply everything" means it asks again, change by change.
4. It applies the text, re-reads the page and tells you "matches" or shows the difference.

### Step 6: write posts

> Write a post about the migration we finished last week

Command: `/linkedin-coach:post the migration we finished last week`.

If the idea is vague, it asks one grouped question to get a **true, specific fact**. You
get 3 hooks, a 700–900 character post and a "POST READY" card with the humanizer score.
**You publish it yourself**: the skill never posts.

### Step 7: track your progress

Run "Audit my LinkedIn profile" again in a few weeks. The skill compares with your last
audit and shows what improved. To change your target or details at any time:

> Update my positioning: add Geneva

Command: `/linkedin-coach:positioning add Geneva`.

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
