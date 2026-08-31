#!/usr/bin/env python3
"""Fail closed on public-repository paths or content that require human review."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TEXT_SUFFIXES = {"", ".md", ".txt", ".json", ".yaml", ".yml", ".py"}
FORBIDDEN_PATH_NAMES = {".env", ".env.local", ".DS_Store"}
FORBIDDEN_SUFFIXES = {".pem", ".key"}
CONTENT_RULES = {
    "absolute_macos_user_path": re.compile(r"/Users/[^/\s]+/"),
    "absolute_linux_home_path": re.compile(r"/home/[^/\s]+/"),
    "private_key_block": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "credential_assignment": re.compile(
        r"(?i)(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{16,}"
    ),
    "raw_trace_field": re.compile(r'(?i)["\']raw_(?:prompt|response|command|path)["\']\s*:'),
}


def findings(root: Path) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    this_script = Path(__file__).resolve()
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        relative = path.relative_to(root).as_posix()
        if path.name in FORBIDDEN_PATH_NAMES or path.suffix in FORBIDDEN_SUFFIXES:
            found.append((relative, "forbidden_path"))
            continue
        if path.resolve() == this_script or path.suffix not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            found.append((relative, "unexpected_binary"))
            continue
        for rule_id, pattern in CONTENT_RULES.items():
            if pattern.search(text):
                found.append((relative, rule_id))
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    found = findings(root)
    if found:
        for path, rule_id in found:
            print(f"FAIL path={path} rule={rule_id}")
        return 1
    print(f"PASS root={root} findings=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

