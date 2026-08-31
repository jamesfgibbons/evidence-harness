#!/usr/bin/env python3
"""Run the complete local release check without network access."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "evidence-harness"
EXAMPLE = ROOT / "examples" / "synthetic-infra-mismatch"


def run(*args: str) -> None:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    subprocess.run(args, cwd=ROOT, check=True, env=env)


def main() -> int:
    surface = json.loads((ROOT / "PUBLIC_SURFACE.json").read_text(encoding="utf-8"))
    if surface.get("publication_authorized") is not True:
        raise SystemExit("public surface is not authorized for publication")
    json.loads(
        (ROOT / "schemas" / "completion-receipt.schema.json").read_text(
            encoding="utf-8"
        )
    )
    run(sys.executable, "scripts/validate_skill.py", str(SKILL))
    run(sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v")
    run(sys.executable, "scripts/check_public_hygiene.py", str(ROOT))

    with tempfile.TemporaryDirectory(prefix="evidence-harness-release-check-") as temp:
        temp_dir = Path(temp)
        receipt = temp_dir / "receipt.json"
        archive = temp_dir / "evidence-harness-0.1.0.zip"
        run(
            sys.executable,
            str(SKILL / "scripts" / "harness_receipt.py"),
            "--task",
            str(EXAMPLE / "task.json"),
            "--authority",
            str(EXAMPLE / "authority.json"),
            "--observed",
            str(EXAMPLE / "observed.json"),
            "--output",
            str(receipt),
        )
        result = json.loads(receipt.read_text(encoding="utf-8"))
        expected = json.loads(
            (EXAMPLE / "expected-receipt.json").read_text(encoding="utf-8")
        )
        if result != expected:
            raise SystemExit("synthetic receipt differs from golden fixture")

        run(
            sys.executable,
            "scripts/package_skill.py",
            "--skill",
            str(SKILL),
            "--output",
            str(archive),
        )
        with zipfile.ZipFile(archive) as packaged:
            packaged.extractall(temp_dir / "extracted")
        run(
            sys.executable,
            "scripts/validate_skill.py",
            str(temp_dir / "extracted" / "evidence-harness"),
        )

    print("PASS release=verified-local publication_authorized=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
