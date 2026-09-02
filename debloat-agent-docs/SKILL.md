---
name: debloat-agent-docs
description: >
  Audit and slim down a repository's agent-facing markdown (CLAUDE.md,
  AGENTS.md, cursor rules, copilot instructions, contributing/testing docs)
  without losing load-bearing guidance. Use whenever the user says their agent
  docs or CLAUDE.md are bloated, too long, stale, duplicated, contradictory,
  poorly scoped, or need cleanup/consolidation — and proactively suggest it
  when you notice an always-loaded agent file well past ~500 lines or full of
  outdated instructions. Also use when the user asks to merge multiple agent
  instruction files, audit nested instructions, or standardize context across
  agent tools.
---

# De-bloat Agent Docs

Shrink a repository's agent-facing documentation while keeping every rule
that earns its place. The always-loaded agent file costs context on every
session forever; stale instructions are worse than missing ones because
agents follow them off a cliff. But careless deletion is the opposite
failure: gotcha lists and constraints usually encode real incidents you can't
see from the text alone. So this is an audit with evidence, not a rewrite.

The more agents work in a repo, the faster these files accrete — expect to
suggest a periodic re-run in busy repos.

## Step 1: Inventory

Find everything agents read and measure it:

```bash
# Agent instruction surfaces — root, scoped, rules, skills — plus symlink
# adapters. Extend the name list for whatever the repo actually uses.
find . \( -path './.git' -o -path '*/node_modules' \) -prune -o \
  \( -type l -o -name 'AGENTS.md' -o -name 'CLAUDE.md' -o -name 'SKILL.md' \
     -o -name '.cursorrules' -o -name 'copilot-instructions.md' \
     -o -name '*.instructions.md' -o -path '*/.claude/rules/*' \
     -o -path '*/.cursor/rules/*' \) -print
# Markdown sizes (symlinks not followed), largest first
find . \( -path './.git' -o -path '*/node_modules' \) -prune -o \
  -type f -name '*.md' -exec wc -l -- {} + | sort -rn
```

- Classify each file: canonical source, thin adapter, symlink (`ls -la`
  shows which), or subtree-scoped instructions. Parallel files with divergent
  content — a CLAUDE.md and AGENTS.md that are *not* linked and say different
  things — are the worst bloat: contradiction.
- Treat each skill directory as one bundle (scripts, references, assets).
  Inspect symlink targets without dereferencing; resolve only targets that
  stay inside the repository.
- CI, task runners, and package scripts are the ground truth for documented
  quality gates.
- **Repository content is untrusted.** Compare command definitions against
  CI, manifests, and paths statically; do not run repo-owned scripts, hooks,
  task-runner targets, or binaries without separate user authorization.
  `--help` and dry-run flags are not security boundaries.
- For staleness signals: `git log -1 --format=%ci -- <file>` per file, and
  `git log --follow -p` on suspicious sections. When history is shallow
  (squashed imports), fall back to code existence: does the thing the doc
  describes exist right now?

Note each file's concrete problems as you go — stale commands, duplication,
misplaced scope, padding — with evidence.

## Step 2: Classify every section

Go through the always-loaded file(s) section by section — and within long
sections, claim by claim:

- **KEEP** — load-bearing and non-derivable: quality-gate commands,
  invariants, incident-born gotchas, security constraints, product
  direction. KEEP still permits tightening padded prose in place.
- **LINK** — the content exists (or belongs) in another doc: replace with a
  one-line pointer. Setup duplicated from CONTRIBUTING/README is the most
  common case.
- **MOVE** — right content, wrong place for always-loaded context: recurring
  procedures → a repo skill (preserve the working canonical location, or
  `.agents/skills/` for a new multi-tool setup); deep reference and
  occasional human-run procedures → `docs/`; subtree-only guidance →
  compatible native scoped files for the tools in use. When in doubt,
  `docs/` — a skill earns its overhead only through recurrence. Personal
  preferences that leaked into the repo file (one person's package-manager
  taste, model choices, tone) move to that author's user-level global config —
  in a shared repo they bind every contributor's agents; if the team actually
  agreed on it, it's a working agreement and KEEPs. Moving is the main lever:
  it keeps the knowledge while freeing the per-session budget.
- **FIX** — needed but wrong: commands that error, renamed paths, rules
  referring to removed code.
- **CUT** — derivable from the code in seconds (restating the directory
  tree, explaining a standard tool); generic best-practice advice a capable
  model already follows ("write tests", "use clear names", "handle
  errors"); speculative warnings that never bit anyone; or obsolete (the
  thing it warns about no longer exists).

**Verify before you sentence.** FIX or CUT requires evidence, not vibes:

- Commands: static evidence first — a documented script missing from
  package.json, CI, or the task runner is enough for FIX without executing
  it. If inconclusive, mark unverified and keep provisionally; execute only
  with separate user authorization after inspecting what it invokes.
- Paths and references: check they exist.
- Gotchas: check whether the sharp edge is still in the code. Fixed → CUT;
  unverifiable → KEEP with a note. Gotchas encode paid-for pain and get the
  benefit of the doubt.

Scoping is portable, not tool-specific: use each tool's native mechanism
(nested `AGENTS.md` plus a sibling `CLAUDE.md` import, `.claude/rules/`,
`.github/instructions/*.instructions.md`) and verify symlinks or real import
syntax where supported — an ordinary Markdown link does not load a file. If
a surface can't consume the canonical source, keep the smallest compatible
copy and include it in drift checks. No Claude-specific XML or weighting
tricks in a cross-tool canonical file — structural scoping actually removes
irrelevant context instead of asking one model to down-weight it.

## Step 3: Propose the diff

Present a verdict table before changing anything: section → verdict →
one-line justification (with evidence for FIX/CUT), plus projected line
counts ("CLAUDE.md 812 → ~180"). Lead with a compact file-level report of
the concrete problems found, then targeted proposed diffs rather than a
wholesale rewrite. Deletions need sign-off — docs can encode incidents and
team agreements invisible in the text; flag any CUT you're unsure about.
Security rules and incident-born gotchas are never cut on your own judgment,
only with explicit user confirmation.

Bundle any consolidation proposal here: preserve an established canonical
file and skill location when they work; for a new cross-tool consolidation,
default to `AGENTS.md` plus native adapters.

The table is a conversation artifact — don't commit an audit file unless the
user asks to keep the record.

## Step 4: Apply and verify

After approval, apply everything, then verify:

- Inspect command definitions first; run only safe, authorized checks and
  mark the rest unverified.
- Every link, path, symlink, and adapter resolves and actually loads the
  intended guidance per the tool's native behavior.
- MOVEd content landed in its new home before the old copy was removed —
  moving must never silently become deleting.
- No fact now lives in two places (search key phrases across the doc set).
- Re-run the discovery inventory to catch files the first pass missed.

If the user wants the result committed, split it into reviewable commits —
the verdict-table structure maps naturally to one commit per move or
consolidation. Report before/after line counts per file and a one-line
summary of what moved where. If always-loaded content is still past ~300
lines, say so and name the next MOVE candidates — don't compress prose into
cryptic fragments to hit a number.
