# Agentify Skills

Agent Skills for setting up repositories for AI-assisted coding — and for
keeping the resulting documentation lean.

Two skills, two halves of the same discipline:

- **`agentify-repo`** — initialize a fresh repository, or retrofit an existing
  one, with agent-facing documentation (one canonical root instruction file,
  compatible tool adapters, scoped instructions, repo skills, vision,
  architecture, testing, security docs). Interview-driven: the agent asks
  about your project's direction and constraints, proposes a documentation
  plan, and only creates documents that have real content — no empty
  placeholders.
- **`debloat-agent-docs`** — audit and slim down existing agent-facing
  markdown. Classifies every section (keep / link / move / fix / cut) with
  evidence — static CI and manifest evidence exposes stale commands without
  executing untrusted repo code, while gotchas survive unless the sharp edge
  is verifiably gone — scopes conditional guidance into nested instructions or
  skills, and asks for sign-off before deleting anything.

## Philosophy

The always-loaded agent file costs context on every session, forever. These
skills encode a few principles:

- Document the **delta**, not the codebase — only what an agent can't derive
  from the code.
- One fact, one place — everything else links to it.
- Docs are earned, not scaffolded.
- Gotchas come from real incidents, never speculation.
- Recurring procedures become skills, not sections.
- Shared guidance has one canonical source with thin adapters for each tool.

## Contents

- `agentify-repo/` — the init/retrofit skill (`SKILL.md` + document catalog
  and `AGENTS.md` template under `references/`)
- `debloat-agent-docs/` — the cleanup skill
- `evals/cases/` and `evals/fixtures/` — trigger and behavioral evaluation
  contracts backed by concrete repositories
- `scripts/validate.py` — dependency-free structural validation

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

## Validate

```bash
python3 -m unittest discover -s tests
python3 scripts/validate.py
```

The tests exercise strict frontmatter parsing. The validator checks skill
frontmatter, the line budget, relative Markdown links, and the shape of each
behavioral eval manifest.

## Influences

- Anthropic's
  [`claude-md-improver`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-md-management/skills/claude-md-improver)
  and [`skill-creator`](https://github.com/anthropics/skills/tree/main/skills/skill-creator):
  quality reports, targeted updates, and eval-driven iteration.
- HumanLayer's
  [`improve-claude-md`](https://github.com/humanlayer/skills/tree/main/plugins/improve-claude-md/skills/improve-claude-md):
  conditional relevance, translated here into portable structural scoping
  instead of Claude-specific markup.
- Addy Osmani's
  [`documentation-and-adrs`](https://github.com/addyosmani/agent-skills/tree/main/skills/documentation-and-adrs):
  convention-first decision records.
- [Agentic Bootstrap](https://github.com/sciensoft/agentic-bootstrap): a
  tool-agnostic canonical spine and safe re-runs.

## Usage

In any repository:

- "Set up this repo for agentic coding" / `/agentify-repo`
- "My CLAUDE.md is bloated, clean it up" / `/debloat-agent-docs`

## License

MIT. See [LICENSE](LICENSE).
