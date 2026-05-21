# Contributing to Council

Thanks for wanting to improve Council. It's a small, focused skill — instructions
plus six advisor/Chairman personas — so contributions are easy to reason about.

## Repository layout

- `skills/council/SKILL.md` — the skill: the workflow the orchestrator follows
- `skills/council/prompts/*.md` — the five advisor personas + the Chairman
- `.claude-plugin/` — plugin + marketplace manifests
- `.github/make_og.py` — regenerates the social-preview card

## Local development

There are no build steps or dependencies — it's markdown. To try changes, install
the skill into a project:

```bash
cp -r skills/council ~/.claude/skills/council   # personal, or .claude/skills/ for a project
```

Then invoke it in Claude Code: `council this: <a real decision>`.

## What makes a good change

- **Persona edits** — keep each advisor leaning *fully* into one angle. The value of
  the council is divergence, not balance; don't soften a persona toward the others.
- **Workflow edits (SKILL.md)** — preserve the core invariant: advisors run as
  independent subagents and never see each other except through the anonymized,
  shuffled debate-round cross-feed.
- **Keep it lean.** A new instruction should earn its place; explain the *why*.

## Pull requests

1. Fork and branch.
2. Make the change. If you touched a persona or the workflow, run a real council
   session on a couple of decisions and paste the resulting `session.md` (or a short
   summary) into the PR so reviewers can see the effect.
3. Keep the diff focused. Fill in the PR template.

## Regenerating the social card

```bash
python3 .github/make_og.py   # requires librsvg (rsvg-convert) + Pillow
```

## Reporting bugs and ideas

Use the issue templates. For anything sensitive, see the [Code of Conduct](CODE_OF_CONDUCT.md).
