#!/usr/bin/env python3
"""Create a deterministic ZIP archive of the canonical skill directory."""

from __future__ import annotations

import argparse
import hashlib
import zipfile
from pathlib import Path


def package(skill_dir: Path, output: Path) -> str:
    skill_dir = skill_dir.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(skill_dir.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            relative = Path(skill_dir.name) / path.relative_to(skill_dir)
            info = zipfile.ZipInfo(relative.as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED)
    return hashlib.sha256(output.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    digest = package(args.skill, args.output)
    print(f"PASS archive={args.output} sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

