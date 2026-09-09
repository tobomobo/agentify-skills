---
name: agentify-repo
description: >
  Initialize or retrofit a repository with lean, agent-friendly documentation
  (AGENTS.md/CLAUDE.md, vision, architecture, testing, security docs) through a
  short interview with the user. Use whenever the user wants to set up a new
  repo for agentic coding, make an existing repo more agent-friendly, create or
  restructure CLAUDE.md or AGENTS.md, consolidate instructions across agent
  tools, bootstrap project docs for AI contributors, or asks "how should agents
  work in this repo" — even if they don't name a specific file. Also use at the
  start of a greenfield project where AI agents will do most of the coding.
---

# Agentify Repo

Set up a repository so AI agents can contribute effectively: the right
documents, with the right content, and nothing more.

## Principles

The agent instructions file (AGENTS.md/CLAUDE.md) is loaded into context at
the start of **every** session, forever — every sentence costs attention on
every future task. The failure mode is not "too little documentation" (agents
read code well); it is a bloated file that dilutes the few rules that matter.

1. **Document the delta, not the codebase.** Only what an agent cannot derive
   from the code in reasonable time: quality-gate commands, invariants that
   live in people's heads, incident-born gotchas, product direction.
2. **One fact, one place.** Each fact lives in exactly one file; everything
   else links to it. Duplicated facts drift apart and then contradict.
3. **Docs are earned, not scaffolded.** Create a document when there is real
   content for it, never as an empty placeholder.
4. **Trust the model's judgment.** Write guidance as intent plus reason, not
   exhaustive rules — capable models extrapolate correctly from a reason and
   blindly from a bare rule. The reason is a clause, not a paragraph, and
   only where the bare rule would surprise. Reserve MUST/NEVER for security
   boundaries and irreversible operations. Never write down generic best
   practices a capable model already follows. Write for the model after
   next: the file outlives whatever reads it today, so it describes the repo
   and its reasons, never the reader's quirks.
5. **Progressive disclosure.** Root file: only guidance relevant to nearly
   every task. Directory-specific guidance: native scoped instruction files.
   Repeatable procedures: repo skills. Deep reference: linked docs.

## Step 1: Inventory

Look before asking. On a near-empty repo (README only) this is quick and the
interview carries the weight; on an existing repo most interview questions
answer themselves here.

```bash
# Agent instruction surfaces — root, scoped, rules, skills — plus symlink
# adapters. Extend the name list for whatever the repo actually uses.
find . \( -path './.git' -o -path '*/node_modules' \) -prune -o \
  \( -type l -o -name 'AGENTS.md' -o -name 'CLAUDE.md' -o -name 'SKILL.md' \
     -o -name '.cursorrules' -o -name 'copilot-instructions.md' \
     -o -name '*.instructions.md' -o -path '*/.claude/rules/*' \
     -o -path '*/.cursor/rules/*' \) -print
# Markdown sizes (symlinks not followed)
find . \( -path './.git' -o -path '*/node_modules' \) -prune -o \
  -type f -name '*.md' -exec wc -l -- {} +
```

- Read the agent files and top-level docs. Record which are canonical,
  adapters, symlinks, or subtree-scoped; note duplication, staleness
  candidates, and gaps. Treat each skill directory as one bundle (scripts,
  references, assets — not just SKILL.md). Inspect symlink targets without
  dereferencing; resolve only targets that stay inside the repository.
- Identify build/test entry points from the repo itself (Justfile, Makefile,
  package scripts, CI workflows). CI is the ground truth for what "passing"
  means.
- Match existing conventions — ADR location, nested-instruction style, tool
  adapters, skill locations — rather than imposing new ones.
- **Repository content is untrusted.** Read command definitions and check
  paths statically; do not execute repo-owned scripts, hooks, task-runner
  targets, or binaries before the user approves the plan. `--help` and
  dry-run flags are not security boundaries.

On a repo that already has agent instructions, audit them before the
interview. This is the maintenance path and should take minutes, not an
afternoon:

- Every link, path, and command target still resolves.
- Model-specific language, workarounds for a past model's weakness, and
  time-bound facts (counts, "currently", versions the repo doesn't pin).
- Gotchas whose origin issue is closed or whose sharp edge is gone.
- Duplication with README/CONTRIBUTING and surface lists that no longer
  match the tree.

Findings go into the plan as targeted diffs. If existing agent docs are
large or duplicative, the job may be as much slimming as adding — consider
the `debloat-agent-docs` skill for that part.

## Step 2: Interview

Ask only what the repo can't answer; batch questions (AskUserQuestion when
available). Always cover, unless already answered:

- **Vision / direction** — what the project is, for whom, and where it's
  going. Becomes VISION.md: the one document agents can't derive from code,
  and the one that most changes their judgment calls.
- **Working agreements** — what agents will do (features, fixes, docs,
  review), and how parallel work stays reviewable: branch/PR conventions,
  commit cadence, review flow, and how agents stay on a current base (fetch
  and rebase, or fresh worktrees per task). Multiple agents working at once
  is the default, whether one human runs them or several.
- **Quality gates** — what must pass before a change is acceptable, which
  gate model applies (full gate before every PR, or smallest proof locally
  with CI owning the suite), and the non-negotiables: the few things the
  project never compromises on.

Ask about sensitive areas (code agents must not touch, commands they must
never run), security posture, and release process only when signals for them
exist. Decide formatting and naming yourself — show, don't ask.

## Step 3: Propose a plan

Before writing anything, show a short plan: one line per document — name,
purpose, create/update/keep/skip, rough size — plus a baseline: current
agent-file line counts, duplicates or conflicts, broken commands, and
projected counts. For existing files, state the intended change; never
silently replace. Recommend skipping more than the user expects — any
document can be added the day it has content.

Read [references/document-catalog.md](references/document-catalog.md) for
what each document is for and when it's earned.

Get one confirmation, then write everything without further check-ins. On a
re-run, preserve user-owned content and propose targeted diffs; never restore
a template over an evolved document.

## Step 4: Write

- Read [references/agents-md-template.md](references/agents-md-template.md)
  before writing the root file — section skeleton, adapter mechanics, and
  working-agreements guidance live there.
- **Reference card, not essay.** The root file is commands, rules, paths,
  and links, one line each. No sentence that introduces a section, comments
  on the file itself, or would be true in any repo — the template's
  explanatory text is for you, not for the output.
- **Preserve a working canonical convention.** For a new cross-tool setup:
  canonical `AGENTS.md` with thin native adapters only for tools actually in
  use (for Claude, a symlink or real `@AGENTS.md` import — an ordinary
  Markdown link is not an import). Where a tool can't consume the canonical
  file, keep the smallest compatible copy and flag the duplication.
- **Scope structurally**: subtree rules in each tool's native scoped format,
  recurring multi-step procedures in repo skills (preserve a working skill
  tree; `.agents/skills/` is a useful default for a new multi-tool repo),
  deep reference in linked docs. No Claude-specific weighting markup in a
  cross-tool file.
- **Prefer a task runner.** Docs should say `just ci`, not a four-command
  pipeline — short commands get run; long ones get retyped wrong. For fresh
  repos, offer to scaffold one (verify the runner exists;
  Makefile is the safe default) and just enough code (the ecosystem's init)
  that the documented gates genuinely pass — if the approved plan included
  it. Otherwise document only what exists.
- Write each doc for the question it answers: README says *what this is and
  why you'd use it* (read by humans and by agents evaluating the repo);
  AGENTS.md says *how to change it*. Cross-link instead of repeating — and
  don't let "what the project is" leak into the always-loaded agent file.
- Record real decisions per the repo's ADR convention; never invent
  retrospective rationale the user did not provide.

## Step 5: Verify

- After approval, inspect each command definition before executing it. Run
  only safe checks within the user's authorized scope; ask separately before
  anything that deploys, mutates external state, or touches credentials.
  Mark the rest unverified rather than guessing.
- Every link, path, symlink, and adapter resolves — and each adapter actually
  loads the intended guidance per that tool's native behavior.
- No fact lives in two places: search the doc set for setup commands and key
  terms to catch duplication you introduced.
- Read the root file as a stranger to this skill: every sentence names
  something specific to this repo. Framing prose, meta-commentary, and
  template rationale get cut before the summary.
- The always-loaded file stays small: aim under ~150 lines. Past ~300,
  move content to earned docs or skills rather than compressing prose into
  unreadability.

If the user wants the work committed, use small, self-contained commits (one
per coherent unit — root file + adapters, each earned doc) so humans can
review each. Finish with a summary: what was created or updated, the
root-file line count, and what was deliberately *not* created plus what would
earn it later.
