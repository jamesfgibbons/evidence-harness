#!/usr/bin/env python3
"""Validate the public skill structure with no third-party dependencies."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)
LINK_RE = re.compile(r"\((?P<path>(?:references|scripts|assets)/[^)#]+)(?:#[^)]+)?\)")


def frontmatter_value(frontmatter: str, key: str) -> str | None:
    for line in frontmatter.splitlines():
        if line.startswith(f"{key}:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return None


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_path = skill_dir / "SKILL.md"
    if not skill_path.is_file():
        return ["missing SKILL.md"]

    text = skill_path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return ["SKILL.md must start with YAML frontmatter"]

    frontmatter = match.group("body")
    name = frontmatter_value(frontmatter, "name")
    description = frontmatter_value(frontmatter, "description")
    if name != skill_dir.name:
        errors.append("frontmatter name must match the skill directory")
    if not description or len(description) < 40:
        errors.append("description must explain capability and trigger")
    if len(name or "") > 64 or not re.fullmatch(r"[a-z0-9-]+", name or ""):
        errors.append("name must be lowercase, hyphenated, and at most 64 characters")
    if "TODO" in text:
        errors.append("SKILL.md contains unfinished TODO text")

    for link in LINK_RE.finditer(text):
        target = skill_dir / link.group("path")
        if not target.exists():
            errors.append(f"missing referenced resource: {link.group('path')}")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.is_file():
        errors.append("missing agents/openai.yaml")
    elif "$evidence-harness" not in openai_yaml.read_text(encoding="utf-8"):
        errors.append("default_prompt must mention $evidence-harness")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_dir", type=Path)
    args = parser.parse_args()
    errors = validate_skill(args.skill_dir.resolve())
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1
    print(f"PASS skill={args.skill_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

