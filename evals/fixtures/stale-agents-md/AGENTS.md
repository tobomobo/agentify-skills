# AGENTS.md

Guide for agents changing Tiny Timer. General contributor info is in
[README.md](README.md).

## Getting started

    make setup
    make test

## Quality gates

    make ci    # before every PR

## Key patterns

- Claude Sonnet 3.5 tends to forget the trailing newline in fixtures; always
  add it explicitly.
- All time math lives in `src/clock.py`; never duplicate it in the CLI layer
  so a rounding fix lands in one place.
- Use GPT-4-style step-by-step reasoning before editing parser code.

## Common gotchas

1. **`make test` needs `TZ=UTC`** — fixed in #12 by setting it inside the
   Makefile; kept here for reference.
2. **Argument parsing lives in `src/args.py`** — not `src/cli.py`.

## Status

We currently have about 400 users and are migrating to Python 3.12 this
quarter.
