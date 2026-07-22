# Document Catalog

What each document is for, when a repo has earned it, and when to skip it.
The default answer for every non-core document is "skip until it has real
content."

## Core set

### README.md

- **Reader**: humans first (GitHub landing page), agents second.
- **Contains**: what the project is in two sentences, quick start (the 3–5
  commands to get running), pointer to CONTRIBUTING/AGENTS for more.
- **Skip when**: never — every repo gets one.
- **Anti-bloat**: the README is not the manual. Feature tours, full CLI
  references, and architecture essays go elsewhere.

### AGENTS.md (+ CLAUDE.md symlink)

- **Reader**: agents, loaded every session.
- **Contains**: see `agents-md-template.md`. Only the agent-specific delta.
- **Skip when**: never for a repo agents work in — this is the point of the
  exercise.
- **Anti-bloat**: budget ~300 lines, hard ceiling 500. Everything beyond the
  delta gets linked, not inlined.

## Earned documents

### VISION.md

- **Reader**: agents and humans making judgment calls — "should this feature
  bend this way or that way?"
- **Contains**: what the project wants to become, for whom, and what it
  deliberately gives up. Written as narrative, not a feature list. Concrete
  scenarios ("a user does X and Y happens") beat abstractions.
- **Earned when**: the user can articulate direction beyond "it's a tool that
  does X". A greenfield agentic project should almost always have one — it is
  the highest-leverage doc for autonomous agents, because it substitutes for
  the thousand product questions they can't ask mid-task.
- **Growth pattern**: one VISION.md until it exceeds ~250 lines; then split
  per-area files (`VISION_<AREA>.md`) with VISION.md as the overview that
  links to them.
- **Skip when**: the user genuinely has no direction to state — don't invent
  one for them.

### CONTRIBUTING.md

- **Reader**: humans (and agents, for setup/style/PR mechanics).
- **Contains**: environment setup, code style, test commands, PR process, "how
  to add an X" recipes for the repo's common extension points.
- **Earned when**: more than one contributor, or a human/agent split where
  AGENTS.md would otherwise fill up with general contributor info. AGENTS.md
  then links here instead of duplicating setup instructions.
- **Skip when**: solo project where README quick-start covers setup — let
  AGENTS.md carry the delta and revisit when a second contributor shows up.

### ARCHITECTURE.md

- **Reader**: anyone needing the system map before diving into code.
- **Contains**: component/module map with one-line responsibilities, key data
  flows, dependency direction, the "why" behind non-obvious structural
  decisions.
- **Earned when**: the structure isn't obvious from the directory tree — e.g.
  multiple services, a pipeline with stages, a protocol. A single-crate CLI
  doesn't need one.
- **Anti-bloat**: describe the shape, not every file. If it restates what
  `ls` shows, delete it.

### TESTING.md

- **Reader**: agents and humans running or writing tests beyond the basics.
- **Contains**: the test taxonomy (unit/integration/E2E), what infrastructure
  each layer needs, how to run one test vs. the suite, live-testing runbooks.
- **Earned when**: testing needs more explanation than one command. If
  `just test` is the whole story, a line in AGENTS.md suffices.

### SECURITY.md

- **Reader**: vulnerability reporters (policy half) and contributors/agents
  (design-principles half).
- **Contains**: how to report vulnerabilities privately + response
  expectations; optionally the security invariants of the design (auth model,
  trust boundaries) that every change must uphold.
- **Earned when**: the project is public-facing or handles anything
  sensitive. The invariants half is especially valuable for agents — it turns
  "be careful with auth" into checkable rules.

### RELEASING.md

- **Reader**: whoever cuts releases (often an agent, eventually).
- **Contains**: the exact release procedure, versioning scheme, where
  artifacts land.
- **Earned when**: the project ships versioned artifacts. Skip for
  deploy-on-merge services (a CI note in AGENTS.md covers it).

### docs/ directory

- **Reader**: on-demand deep divers.
- **Contains**: topic deep-dives too long for the core docs — design notes,
  subsystem internals, postmortem-derived guides. This is where content
  *moves to* when core docs exceed budget.
- **Earned when**: the first real deep-dive exists.

### .claude/skills/ (repo-scoped skills)

- **Reader**: agents, loaded only when triggered.
- **Contains**: repeatable multi-step procedures with exact commands —
  screenshot-and-post-to-PR workflows, release procedures, CLI usage guides.
- **Earned when**: a procedure is (a) multi-step, (b) recurring, and (c) would
  otherwise bloat AGENTS.md. This is the primary pressure-release valve for
  the always-loaded file.

### GOVERNANCE.md / CODE_OF_CONDUCT.md

- **Earned when**: the project has a real community with decision-making
  questions. Skip for personal and small-team repos.
