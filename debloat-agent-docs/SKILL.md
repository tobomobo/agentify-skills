---
name: debloat-agent-docs
description: >
  Audit and slim down a repository's agent-facing markdown (CLAUDE.md,
  AGENTS.md, cursor rules, copilot instructions, contributing/testing docs)
  without losing load-bearing guidance. Use whenever the user says their agent
  docs or CLAUDE.md are bloated, too long, stale, duplicated, contradictory,
  or need cleanup/consolidation — and proactively suggest it when you notice
  an always-loaded agent file well past ~500 lines or full of outdated
  instructions. Also use when the user asks to merge multiple agent
  instruction files into one.
version: 1
---

# De-bloat Agent Docs

Shrink a repository's agent-facing documentation while keeping every rule
that actually earns its place. The always-loaded agent file costs context on
every session forever; stale instructions are worse than missing ones because
agents follow them off a cliff. But careless deletion is the opposite failure:
gotcha lists and constraints usually encode real incidents you can't see from
the text alone. So this skill is an audit with evidence, not a rewrite.

## Step 1: Inventory

Find everything agents read and measure it:

```bash
ls CLAUDE.md AGENTS.md .cursorrules .github/copilot-instructions.md 2>/dev/null
ls .cursor/rules .claude/skills/ docs/ 2>/dev/null
wc -l CLAUDE.md AGENTS.md *.md docs/*.md 2>/dev/null | sort -rn
```

Check for parallel agent files with divergent content (a CLAUDE.md and an
AGENTS.md that are *not* symlinked and say different things is the worst kind
of bloat — contradiction). `ls -la` reveals which are symlinks.

Use git history for staleness signals: `git log -1 --format=%ci -- <file>`
per file, and `git log --follow -p` on suspicious sections when you need to
know whether a rule predates a refactor. When history is shallow or useless
(squashed imports, single-commit repos), fall back to code-existence
evidence: does the thing the doc describes exist in the codebase right now?

## Step 2: Classify every section

Go through the always-loaded file(s) section by section — and within long
sections, claim by claim. Assign each one a verdict:

- **KEEP** — load-bearing and non-derivable: quality-gate commands, invariants,
  incident-born gotchas, security constraints, product direction. KEEP still
  permits tightening the prose in place — padded restatements around a
  load-bearing fact are bloat too.
- **LINK** — the content exists (or belongs) in another doc: replace with a
  one-line pointer. Setup instructions duplicated from CONTRIBUTING/README are
  the most common case.
- **MOVE** — right content, wrong place for always-loaded context:
  procedures agents will execute repeatedly → a repo skill
  (`.claude/skills/<name>/SKILL.md`); deep reference material, and
  occasional or human-run procedures (a release checklist run twice a year)
  → `docs/`. When in doubt, `docs/` — a skill earns its overhead only
  through recurrence. Moving is the main lever — it keeps the knowledge
  while freeing the per-session budget.
- **FIX** — needed but wrong: commands that error, renamed paths, rules
  referring to removed code.
- **CUT** — derivable from the code in seconds (restating the directory tree,
  explaining what a standard tool does), speculative advice that never bit
  anyone ("be careful when..."), or obsolete (the thing it warns about no
  longer exists).

**Verify before you sentence.** A verdict of FIX or CUT requires evidence, not
vibes:

- Commands: run them (or `--help`/dry-run) — an "obviously stale" command that
  still works stays KEEP. Static contradiction also counts as evidence: a
  documented script missing from package.json/Justfile convicts the command
  without executing anything (and without downloading tools just to watch
  them fail).
- Paths and file references: check they exist.
- Gotchas: check whether the sharp edge is still in the code. A gotcha whose
  underlying bug was fixed is CUT; one you can't verify either way stays KEEP
  with a note — gotchas encode paid-for pain and deserve the benefit of the
  doubt.

## Step 3: Propose the diff

Present the user a verdict table before changing anything: section → verdict →
one-line justification (with the evidence for FIX/CUT), plus projected line
counts (e.g. "CLAUDE.md 812 → ~290 lines"). Deletions need sign-off because
docs can encode incidents and team agreements invisible in the text; flag any
CUT you're less than certain about. Security-related rules and incident-born
gotchas are never cut on your own judgment — only with explicit user
confirmation.

Bundle the consolidation proposal here too, if applicable: canonical AGENTS.md
with CLAUDE.md symlinked to it, and other agent-tool files reduced to
pointers.

Present the table in chat — it's a conversation artifact, not a deliverable.
Don't commit an audit file to the repo unless the user asks to keep the
record.

## Step 4: Apply and verify

After approval, apply everything in one pass, then verify:

- Every command remaining in the docs runs; every link and path resolves.
- MOVEd content actually landed in its new home before the old copy was
  removed — moving must never silently become deleting.
- No fact now lives in two places (search for key phrases across the doc set).
- Report before/after line counts per file and a one-line summary of what
  moved where.

If the result is still over ~500 lines of always-loaded content, say so and
identify the next candidates to MOVE — don't compress prose into cryptic
fragments to hit a number; unreadable-but-short is not the goal.
