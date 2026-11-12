# Using LinkedIn Coach

Just talk normally: the skill picks the mode from your request. On first use it asks at
most 7 questions to learn your positioning. The skill works in French or English, based on
the language you choose during onboarding.

## Audit

- "Audit my LinkedIn profile" + your LinkedIn data archive (.zip), PDF export or a
  copy-paste.
- "Analyze my last 20 posts" + the Analytics export (or screenshots).

You get a profile score (out of 100, or out of the reachable maximum when sections are
missing), a post score out of 20, inconsistencies, the top 3 fixes and your progress since
the last audit.

## Improve

- "Rewrite my headline"
- "Improve my About section for architect roles in Geneva"
- "Rewrite my experience as results"
- "Draft 3 recommendation requests"

Texts are ready to paste. If a browser tool (Claude in Chrome) is connected to your
account, the skill can apply a change **after your explicit "yes" for that specific
change**.

## Posts

- "Write a post about <a specific fact>"
- "Suggest a content strategy"
- "Draft a comment for this post: <pasted post>"

## Positioning

- "Update my positioning: add Geneva"

## What the skill refuses, and why

| Request | Answer | Why |
|---|---|---|
| "Publish this post" | Ready-to-paste text | You stay in control (principle II) |
| "Read X's profile" | Refusal, alternative offered | No third-party reading (principle I) |
| "Find posts to comment on" | What to look for; you paste the posts | No feed reading (principle I) |
| "Say 30% gain" without a source | `{{à confirmer}}` ("to be confirmed") | Nothing made up (principle III) |
| "Apply everything" | One approval per change | One approval = one change |

## Where is my data?

- Claude Code: `~/.linkedin-coach/positionnement.md` and `historique-audits.md` (Windows:
  `%USERPROFILE%\.linkedin-coach\`), or the `LINKEDIN_COACH_HOME` folder.
- Claude app: in your dedicated Claude project's instructions.

Nothing is sent anywhere except your conversation with Claude. No telemetry.
