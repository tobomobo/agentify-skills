# Agentify Skills

Agent Skills for setting up repositories for AI-assisted coding — and for
keeping the resulting documentation lean.

Two skills, two halves of the same discipline:

- **`agentify-repo`** — initialize a fresh repository, or retrofit an existing
  one, with agent-facing documentation (`AGENTS.md` with a `CLAUDE.md`
  symlink, vision, architecture, testing, security docs). Interview-driven:
  the agent asks about your project's direction and constraints, proposes a
  documentation plan, and only creates documents that have real content —
  no empty placeholders.
- **`debloat-agent-docs`** — audit and slim down existing agent-facing
  markdown. Classifies every section (keep / link / move / fix / cut) with
  evidence — stale commands are convicted by running them, gotchas survive
  unless the sharp edge is verifiably gone — and asks for sign-off before
  deleting anything.

## Philosophy

The always-loaded agent file costs context on every session, forever. These
skills encode a few principles:

- Document the **delta**, not the codebase — only what an agent can't derive
  from the code.
- One fact, one place — everything else links to it.
- Docs are earned, not scaffolded.
- Gotchas come from real incidents, never speculation.
- Recurring procedures become skills, not sections.

## Contents

- `agentify-repo/` — the init/retrofit skill (`SKILL.md` + document catalog
  and `AGENTS.md` template under `references/`)
- `debloat-agent-docs/` — the cleanup skill

## Install

```bash
npx skills add tobomobo/agentify-skills
```

Manual install for Claude Code:

```bash
git clone https://github.com/tobomobo/agentify-skills.git
cp -R agentify-skills/agentify-repo ~/.claude/skills/agentify-repo
cp -R agentify-skills/debloat-agent-docs ~/.claude/skills/debloat-agent-docs
```

For other agent harnesses, copy the two skill directories into wherever your
tool discovers skills (e.g. `~/.agents/skills/`).

## Usage

In any repository:

- "Set up this repo for agentic coding" / `/agentify-repo`
- "My CLAUDE.md is bloated, clean it up" / `/debloat-agent-docs`

## License

MIT. See [LICENSE](LICENSE).
