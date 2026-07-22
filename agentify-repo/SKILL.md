---
name: agentify-repo
description: >
  Initialize or retrofit a repository with lean, agent-friendly documentation
  (AGENTS.md/CLAUDE.md, vision, architecture, testing, security docs) through a
  short interview with the user. Use whenever the user wants to set up a new
  repo for agentic coding, make an existing repo more agent-friendly, create or
  restructure CLAUDE.md or AGENTS.md, bootstrap project docs for AI
  contributors, or asks "how should agents work in this repo" — even if they
  don't name a specific file. Also use at the start of a greenfield project
  where AI agents will do most of the coding.
version: 1
---

# Agentify Repo

Set up a repository so AI agents can contribute effectively: the right
documents, with the right content, and nothing more.

## Why lean matters

The agent instructions file (AGENTS.md/CLAUDE.md) is loaded into context at the
start of **every** session, forever. Every sentence in it costs attention on
every future task, so every sentence must pay rent. The failure mode of
agent-doc setup is not "too little documentation" — agents are good at reading
code — it is a 1500-line instructions file full of duplicated, stale, or
derivable content that dilutes the few rules that actually matter.

Three principles drive everything below:

1. **Document the delta, not the codebase.** Agent docs exist for what an agent
   *cannot* derive from the code in reasonable time: quality-gate commands,
   invariants that live in people's heads, empirically discovered gotchas,
   product direction. If an agent can find it by reading the code, don't write
   it down.
2. **One fact, one place.** Each fact lives in exactly one file; everything
   else links to it. Duplicated facts drift apart and then contradict each
   other, which is worse than absence.
3. **Docs are earned, not scaffolded.** Create a document when there is real
   content for it, never as an empty placeholder. An empty ARCHITECTURE.md
   teaches agents that docs in this repo can be ignored.

## Step 1: Detect the mode

Look at the repository before asking anything:

- **Fresh repo** — empty or near-empty (no source tree yet, or only a README):
  skip to Step 3 (interview). The interview carries more weight because
  nothing can be derived from code.
- **Existing repo** — has a source tree: do Step 2 first. Most interview
  questions can be answered from the repo itself; only ask what you couldn't
  find.

## Step 2: Inventory (existing repos only)

Build a picture of what exists before proposing anything:

```bash
# Agent-facing files across tools
ls CLAUDE.md AGENTS.md .cursorrules .cursor/rules .github/copilot-instructions.md 2>/dev/null
ls .claude/skills/ 2>/dev/null
# All top-level docs with sizes
wc -l *.md docs/*.md 2>/dev/null
```

Then:

- Read the existing agent files and top-level docs. Note duplication (same
  setup instructions in three files), staleness candidates (commands or paths
  that may no longer exist), and gaps.
- **Verify, don't trust**: spot-check that documented commands actually run
  (`--help` or dry-run is enough) and referenced paths exist. Stale
  instructions are worse than none — they send agents down dead ends.
- Identify the build/test entry points from the repo itself (Justfile,
  Makefile, package.json scripts, CI workflow files). CI workflows are the
  ground truth for what "passing" means.

If the existing agent docs are large (>~400 lines) or duplicative, the job may
be as much about slimming as adding — consider the `debloat-agent-docs` skill
for that part, or fold its classification pass into your plan.

## Step 3: Interview the user

Ask only what the repo can't answer. Use AskUserQuestion when available; batch
questions rather than interrogating one at a time. Two rounds at most.

**Round 1 — always ask (unless already answered):**

- **Vision / direction**: What is this project, for whom, and where is it
  going? What should exist in 6–12 months that doesn't today? This becomes
  VISION.md — the one document agents can't ever derive from code, and the one
  that most changes how they make judgment calls.
- **Agent role**: What will agents actually do here — full features, bug
  fixes, docs, reviews? Solo-with-agents or a human team plus agents? This
  determines how much process documentation is worth writing.
- **Quality gates**: What must pass before a change is acceptable? (Existing
  repos: confirm what you found in CI; fresh repos: what toolchain and what
  standards.)

**Round 2 — ask only if relevant signals exist:**

- **Sensitive areas**: parts of the codebase agents must not touch or must
  treat carefully (auth, billing, migrations, crypto), commands agents must
  never run (deploys, destructive migrations, `flutter run`-style blockers).
- **Security posture**: is there a vulnerability-reporting path? Any security
  invariants every change must uphold?
- **Release process**: only if they ship versioned artifacts.

Don't ask about things you can decide yourself (file naming, section order,
formatting) — decide and show the result.

## Step 4: Propose a documentation plan

Before writing anything, show the user a short plan: one line per document —
file name, purpose, create/update/skip, and rough size. Distinguish:

- **Core set** (almost every repo): `README.md`, `AGENTS.md` +
  `CLAUDE.md` symlink.
- **Earned docs** (only where the interview/inventory produced real content):
  `VISION.md`, `CONTRIBUTING.md`, `ARCHITECTURE.md`, `TESTING.md`,
  `SECURITY.md`, `RELEASING.md`, `docs/`, `.claude/skills/`.

Read [references/document-catalog.md](references/document-catalog.md) for what
each document is for, when it's earned, and when to skip it. Recommend
skipping more than the user might expect — explain that any doc can be added
later the day it has content.

Get a quick confirmation on the plan, then write everything without further
check-ins.

## Step 5: Write the documents

- **AGENTS.md is canonical; CLAUDE.md is a symlink to it**
  (`ln -s AGENTS.md CLAUDE.md`). This keeps one source of truth while serving
  every agent tool. If the environment can't do symlinks (some Windows
  setups), make CLAUDE.md a two-line file: title + "See [AGENTS.md](AGENTS.md)".
  Read [references/agents-md-template.md](references/agents-md-template.md)
  before writing AGENTS.md — it has the section skeleton and per-section
  guidance.
- Other docs: follow the catalog. Write them for their primary reader
  (CONTRIBUTING/README for humans, AGENTS.md for agents) and cross-link
  instead of repeating.
- **Prefer a task runner.** If the repo has (or the user wants) a Justfile or
  Makefile, docs should say `just ci`, not a four-command pipeline. Short
  commands get run; long ones get retyped wrong. For fresh repos, offer to
  scaffold the task runner with `setup`, `test`, and `ci` targets as part of
  this work — and pick a runner that actually exists in the environment
  (check `which just` before scaffolding a Justfile; a Makefile is the safe
  default), otherwise Step 6's verification is impossible.
- **Fresh repos: scaffold just enough code to make the docs true.** Quality
  gates can't pass against an empty directory. Run the ecosystem's init
  (`cargo init`, `npm init`, etc.) so the documented gate commands genuinely
  run and pass. Documented-but-unrunnable commands are stale docs from day
  one.
- **Procedures become skills, not sections.** A repeatable multi-step
  procedure (screenshot workflow, release dance, data seeding) belongs in
  `.claude/skills/<name>/SKILL.md`, where it loads only when needed — not in
  the always-loaded file.

## Step 6: Verify

Before declaring done:

- Every command in every new/updated doc is copy-paste runnable (spot-check by
  running the cheap ones).
- Every relative link and referenced path resolves.
- No fact appears in two places — search for the setup commands and key terms
  across all docs to catch duplication you introduced.
- The always-loaded file (AGENTS.md) is within budget: aim under ~300 lines,
  and treat 500 as a hard ceiling. If you're over, move content to earned docs
  or skills rather than compressing the prose into unreadability.

Finish with a summary: what was created/updated, the AGENTS.md line count, and
what was deliberately *not* created and what would earn it later.
