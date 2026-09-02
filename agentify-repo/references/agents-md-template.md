# AGENTS.md Template

The section skeleton below is a menu, not a mandate — include a section only
when there's real content for it. Order matters: orientation first, rules
last, so an agent skimming top-down gets the map before the law.

Remember the test for every line: *could an agent derive this from the code in
reasonable time?* If yes, cut it.

Writing rules throughout: state each rule with its reason — capable models
extrapolate correctly from a why and blindly from a bare rule. Reserve
MUST/NEVER for security boundaries and irreversible operations. Never
include generic best practices a capable model already follows.

Write for the model after next. The file outlives whatever reads it today,
so it describes the repo and its reasons, never the reader's quirks:

- No model names, and no workarounds for a current model's weakness — those
  expire with the next release. If one is unavoidable, make it a dated
  gotcha so it can be pruned.
- No time-bound facts (user counts, "currently", "new", "this quarter") and
  no tool versions the repo does not pin.
- Commands are task-runner targets, not raw pipelines — targets survive
  refactors; pipelines rot.
- Every path and command named in the file must exist. Every gotcha names
  the issue or commit it came from, so a later pass can check whether the
  sharp edge is still there.

Sizing: a simple repo lands around 30–60 lines with four sections (intro,
quality gates, gotchas stub, see also). A complex multi-surface repo lands
near 150. Past ~300, move content out rather than compressing.

The repo file holds team agreements only. Personal taste — package-manager
preference, model choices, tone — belongs in each contributor's user-level
global config, where it doesn't bind everyone else's agents.

```markdown
# AGENTS.md — AI Agent Contributor Guide

One or two sentences: what this file covers (agent-specific context) and
where general contributor info lives (link CONTRIBUTING.md if it exists —
never duplicate its content here). Then the reading contract in one or two
lines: these are good defaults, not hard rules — the developer's instructions
override anything here, and if a rule fights the task at hand, say so and
get sign-off before breaking it. That escape hatch is what keeps a default
from hardening into a stale rule.

## Project Map

When the structure is non-obvious, open with one paragraph on how the system
works — the request path, the two or three key abstractions — and link the
deep doc. A short inline summary beats a cold link in an always-loaded file.
Skip it when the directory names tell the story.

Annotated tree, ONE line per non-obvious entry, only where it materially reduces
orientation time. Skip this section when the directory names and build files
already make the shape clear. Group related entries with comment headers if the
list is long.

    src/
      core/        # domain types and validation — start here for data model
      api/         # HTTP surface — thin, delegates to core
    migrations/    # SQL, auto-applied on startup
    scripts/       # dev tooling

## Glossary

Only when the repo's domain terms are ambiguous or overloaded — especially
meta-projects where words like "user" or "agent" mean different things in
different sentences (the person using the product vs. the person directing
you vs. an agent the product itself runs). One line per term, defined
operationally:

    - **user** — the person using the product; NOT the maintainer directing you
    - **provider** — the runtime the product talks to (Claude, Codex, ...)

Keep it to the terms that have actually caused confusion or that the code
uses inconsistently. Skip when the domain vocabulary is unambiguous.

## Getting Started

The 3–5 commands from clean checkout to running system. Prefer task-runner
targets (`just setup`) over raw command pipelines. The commands themselves
live in README or CONTRIBUTING (one fact, one place — this holds even when
you're writing all the files at once); here, link them and show only the
agent-specific delta (e.g. env activation agents tend to miss). If there is
no delta, this section is just the link.

## Quality Gates

The exact commands that must pass before a PR, and when to run which. Two
gate models exist; the interview picks one and the file states it plainly:

    # Full gate — small repos, fast suites:
    just ci      # before every PR: fmt + lint + unit tests + build
    just test    # integration suite — needed if you touched X or Y (requires Postgres)

    # Smallest proof — large repos where CI owns the full suite:
    just test <files>   # the tests you touched, plus targeted lint/typecheck
    # No repo-wide runs unless asked; CI runs the full suite.

Plus hard rules that gates don't catch mechanically — both code rules and
operational constraints from the interview:
- e.g. "no new unwrap() in production paths", "public API needs doc comments"
- e.g. "never run commands against the real database file", "agents must not
  run `flutter run` / deploys"

And the project's non-negotiables: the few things never to compromise on,
even when a task would be easier without them — each with its reason (e.g.
"never send user data off-device — local-first is the product"). This is
where MUST/NEVER belongs; keep the list short so it stays absolute. When
they are product-level values rather than code rules ("open at the core",
"performance without compromise"), give them their own short section right
after the intro so they frame everything below; keep them here when they are
code rules.

## Key Patterns

Conventions an agent cannot infer from reading one file — the repo's grain:
- Where new features go ("model it as an event kind, not a new endpoint")
- Cross-cutting invariants ("all queries must scope to the tenant tag")
- Where each kind of change belongs ("agent-facing features go in the CLI
  crate first")

3–8 patterns. Each states the rule AND the why in a sentence or two — agents
extrapolate correctly from reasons, and blindly from bare rules.

## Common Gotchas

Numbered list of empirically discovered traps — things that actually cost an
agent or human real time in this repo:

1. **Kind 39000 for channel metadata, not 41** — 41 looks right but is unused.
2. **Queries must specify `kinds`** — omitting them triggers a 403.

Rules for this section: only add entries born from real incidents (never
speculative "be careful with..."); state the trap, the symptom, and the
correct move; prune entries when the underlying sharp edge is fixed. This
section is append-mostly — tell the user it should grow over time as agents
hit walls, and that adding to it is the repo's cheapest productivity
investment. On a fresh repo with no incidents yet, keep the section as a
two-line stub stating exactly that contract — the one allowed exception to
"docs are earned", because it teaches future sessions where hard-won lessons
belong.

## Working Agreements

Parallel agents are the norm — even one human runs several at once. The
contract that keeps parallel work reviewable and mergeable:

- Commit small and often: each commit self-contained, passing the gates, and
  reviewable on its own; the message says why, not just what.
- Branch/PR conventions: how work is claimed and merged (e.g. one branch per
  task, PRs reference their issue, never rewrite shared history). One concern
  per PR — if the description needs an "also", split it.
- Start from current main and rebase your own branch before opening a PR.
  Parallel agents diverge, and a change built on a stale base reintroduces
  fixed bugs or conflicts at merge. Skip when the harness gives each task a
  fresh worktree or sandbox — the base is already current there.
- Evidence expectations, if the team has them: e.g. UI changes carry
  before/after screenshots, motion changes carry video.
- Coordination rules that prevent agents stepping on each other (e.g. "check
  for an open PR touching the same module before starting").
- Where work artifacts go: plans, research notes, and scratch files stay
  outside the worktree or in a gitignored directory; durable decisions go to
  the repo's ADR location. Skip when no agent here produces plans.

Keep it to what was actually agreed — skip the section only when the repo
genuinely has no conventions beyond the quality gates.

## <Surface-specific sections>

Only for multi-surface repos (backend + desktop + mobile): one section per
surface with its non-obvious rules (framework constraints, commands that are
unsafe for agents to run, sizing/style rules). Prefer native scoped instruction
files when the guidance matters only while editing that surface; keep it at the
root only when cross-surface work needs it. Single-surface repos skip this.

For multi-surface repos, also add a short "hit every surface" checklist: when
shared code changes, which surfaces/integrations must be verified (each
client, each provider adapter, the wire contract). Agents reliably test the
surface they edited and reliably forget the siblings.

## See Also

One line per linked doc, saying what question it answers:
- [CONTRIBUTING.md](CONTRIBUTING.md) — setup, style, PR process
- [ARCHITECTURE.md](ARCHITECTURE.md) — system design
```

## After writing

For a new cross-tool repo, create the Claude adapter and verify it:

```bash
test ! -e CLAUDE.md && ln -s AGENTS.md CLAUDE.md
ls -la CLAUDE.md
```

On Windows or anywhere symlinks are impractical, make `CLAUDE.md` contain the
real import `@AGENTS.md`; an ordinary Markdown link does not load the file.
Preserve a different established canonical convention when it already works.

For scoped guidance, create compatible native files for every active tool.
For example, a nested `AGENTS.md` needs a sibling nested `CLAUDE.md` import (or
an equivalent `.claude/rules/` rule) when Claude must see it. Copilot may need
`.github/instructions/*.instructions.md` for path-specific IDE or review
surfaces. Verify actual loading behavior instead of assuming a pointer works.

For recurring procedures, preserve a working canonical skill tree; for a new
multi-tool repo, `.agents/skills/` is a useful default. Expose individual skills
through the native directories of tools already used by the repo
(`.claude/skills/`, `.codex/skills/`, `.github/skills/`) only with adapters that
those tools actually support.

After writing, verify every relative link and symlink, then search all agent
entry points for duplicated setup commands and rules. The root file should
contain only guidance relevant to nearly every task; everything else should be
scoped or loaded on demand.
