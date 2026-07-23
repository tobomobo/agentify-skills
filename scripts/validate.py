#!/usr/bin/env python3
"""Validate skill structure, links, and behavioral eval manifests."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("agentify-repo", "debloat-agent-docs")
LINK_RE = re.compile(r"\[[^]]*]\(([^)]+)\)")
KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(?:\s|$)")
REQUIRED_KEYS = {"name", "description"}
# Optional fields permitted by the skill spec and common harnesses; unknown
# keys still fail so typos ("descripton") are caught.
OPTIONAL_KEYS = {
    "version",
    "license",
    "compatibility",
    "allowed-tools",
    "disallowed-tools",
    "metadata",
    "model",
    "context",
    "arguments",
    "disable-model-invocation",
    "user-invocable",
}


def validate_skill(skill_name: str, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    path = root / skill_name / "SKILL.md"
    text = path.read_text()

    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        return [f"{path}: missing YAML frontmatter"]

    frontmatter, body = text[4:].split("\n---\n", 1)
    fields: dict[str, str] = {}
    field_lines: dict[str, int] = {}
    keys: list[str] = []
    lines = frontmatter.splitlines()
    for line_number, line in enumerate(lines):
        if match := KEY_RE.match(line):
            key = match.group(1)
            keys.append(key)
            fields.setdefault(key, line.split(":", 1)[1].strip())
            field_lines.setdefault(key, line_number)

    if len(keys) != len(set(keys)):
        errors.append(f"{path}: duplicate frontmatter keys are not allowed")
    if missing := REQUIRED_KEYS - set(keys):
        errors.append(f"{path}: missing required frontmatter keys {sorted(missing)}")
    if unknown := set(keys) - REQUIRED_KEYS - OPTIONAL_KEYS:
        errors.append(f"{path}: unknown frontmatter keys {sorted(unknown)}")
    if fields.get("name") != skill_name:
        errors.append(f"{path}: name must match its directory")
    description = fields.get("description", "")
    if description in {">", ">-", ">+", "|", "|-", "|+"}:
        description = " ".join(
            line.strip()
            for line in lines[field_lines["description"] + 1 :]
            if line.startswith((" ", "\t")) and line.strip()
        )
    if not description or description in {"null", "~", "''", '\"\"'}:
        errors.append(f"{path}: description must not be empty")
    if not body.strip():
        errors.append(f"{path}: empty skill body")
    if len(text.splitlines()) > 500:
        errors.append(f"{path}: exceeds the 500-line skill budget")
    return errors


def validate_links() -> list[str]:
    errors: list[str] = []
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        outside_fences: list[str] = []
        in_fence = False
        for line in path.read_text().splitlines():
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if not in_fence:
                outside_fences.append(line)
        for raw_target in LINK_RE.findall("\n".join(outside_fences)):
            target = unquote(raw_target.strip("<>").split("#", 1)[0])
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (path.parent / target).exists():
                errors.append(f"{path}: broken relative link {raw_target}")
    return errors


def validate_evals(skill_name: str, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    path = root / "evals" / "cases" / f"{skill_name}.json"
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path}: {exc}"]

    # Malformed input must produce error messages, never tracebacks — a key
    # present with null (or the wrong type) bypasses dict.get defaults.
    if not isinstance(data, dict):
        return [f"{path}: manifest must be a JSON object"]

    if data.get("skill_name") != skill_name:
        errors.append(f"{path}: skill_name must be {skill_name}")
    trigger = data.get("trigger")
    if not isinstance(trigger, dict):
        trigger = {}
    if not trigger.get("positive") or not trigger.get("negative"):
        errors.append(f"{path}: positive and negative trigger cases are required")
    evals = data.get("evals")
    if not isinstance(evals, list):
        evals = []
    if not evals:
        errors.append(f"{path}: at least one behavioral eval is required")
    for index, case in enumerate(evals):
        if not isinstance(case, dict):
            errors.append(f"{path}: eval at index {index} must be a JSON object")
            continue
        missing = {
            "id",
            "fixture",
            "prompt",
            "expected_output",
            "expectations",
        } - case.keys()
        if missing:
            errors.append(f"{path}: eval {case.get('id', '?')} missing {sorted(missing)}")
        if not case.get("expectations"):
            errors.append(f"{path}: eval {case.get('id', '?')} needs expectations")
        fixture = case.get("fixture")
        fixture_path = root / fixture if isinstance(fixture, str) else None
        if not fixture_path or not fixture_path.is_dir():
            errors.append(f"{path}: eval {case.get('id', '?')} fixture is missing")
        elif not any(item.is_file() for item in fixture_path.rglob("*")):
            errors.append(f"{path}: eval {case.get('id', '?')} fixture is empty")
    return errors


def main() -> int:
    errors = [error for skill in SKILLS for error in validate_skill(skill)]
    errors.extend(validate_links())
    errors.extend(error for skill in SKILLS for error in validate_evals(skill))
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"Validated {len(SKILLS)} skills, Markdown links, and eval manifests.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
