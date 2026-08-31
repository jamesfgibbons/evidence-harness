#!/usr/bin/env python3
"""Create a reviewable harness decision receipt without executing the requested action."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ACTION_CLASSES = {"observe", "export", "mutate", "destructive"}
FINAL_STATUSES = {
    "drafted",
    "verified-local",
    "published",
    "live-verified",
    "blocked",
    "deferred",
    "unknown",
}


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def compare_expected(
    expected: dict[str, Any], observed: dict[str, Any], prefix: str = ""
) -> list[str]:
    mismatches: list[str] = []
    for key, expected_value in expected.items():
        path = f"{prefix}.{key}" if prefix else key
        if key not in observed:
            mismatches.append(f"missing:{path}")
            continue
        observed_value = observed[key]
        if isinstance(expected_value, dict):
            if not isinstance(observed_value, dict):
                mismatches.append(f"mismatch:{path}")
            else:
                mismatches.extend(compare_expected(expected_value, observed_value, path))
        elif observed_value != expected_value:
            mismatches.append(f"mismatch:{path}")
    return mismatches


def build_receipt(
    task: dict[str, Any],
    authority: dict[str, Any],
    observed: dict[str, Any],
    generated_at: str | None = None,
) -> dict[str, Any]:
    action = task.get("action", {})
    action_class = action.get("class")
    if action_class not in ACTION_CLASSES:
        raise ValueError(f"action.class must be one of {sorted(ACTION_CLASSES)}")

    expected_state = authority.get("expected_state", {})
    if not isinstance(expected_state, dict):
        raise ValueError("authority.expected_state must be an object")

    observed_state = observed.get("state", observed)
    if not isinstance(observed_state, dict):
        raise ValueError("observed state must be an object")

    mismatches = compare_expected(expected_state, observed_state)
    authorization_present = bool(action.get("authorization_present", False))
    authorization_required = action_class in {"mutate", "destructive"}

    reasons = list(mismatches)
    if authorization_required and not authorization_present:
        reasons.append("authorization:missing")

    decision_status = "blocked" if reasons else "allowed"
    final_status = "blocked" if reasons else "drafted"
    timestamp = generated_at or observed.get("observed_at")
    if not timestamp:
        timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    receipt = {
        "schema_version": 1,
        "generated_at": timestamp,
        "task": {
            "id": task.get("id", "unspecified-task"),
            "intent": task.get("intent", ""),
        },
        "selected_references": task.get("selected_references", []),
        "authority": {
            "source": authority.get("source", "unspecified"),
            "expected_state": expected_state,
        },
        "observed_state": observed_state,
        "action": {
            "class": action_class,
            "requested": action.get("requested", ""),
            "authorization_present": authorization_present,
        },
        "decision": {"status": decision_status, "reasons": reasons},
        "verification": {
            "checks": [
                {
                    "id": "authority-state-match",
                    "result": "pass" if not mismatches else "fail",
                },
                {
                    "id": "required-authorization",
                    "result": (
                        "not_applicable"
                        if not authorization_required
                        else "pass" if authorization_present else "fail"
                    ),
                },
            ]
        },
        "artifacts": [],
        "limitations": [
            "This receipt evaluates declared state and authorization only.",
            "It does not execute or verify the requested external action.",
        ],
        "status": final_status,
    }
    validate_receipt(receipt)
    return receipt


def validate_receipt(receipt: dict[str, Any]) -> None:
    required = {
        "schema_version",
        "generated_at",
        "task",
        "selected_references",
        "authority",
        "observed_state",
        "action",
        "decision",
        "verification",
        "artifacts",
        "limitations",
        "status",
    }
    missing = sorted(required - receipt.keys())
    if missing:
        raise ValueError(f"receipt missing required fields: {', '.join(missing)}")
    if receipt["schema_version"] != 1:
        raise ValueError("unsupported schema_version")
    if receipt["status"] not in FINAL_STATUSES:
        raise ValueError("invalid receipt status")
    if receipt["action"].get("class") not in ACTION_CLASSES:
        raise ValueError("invalid action class")
    if receipt["decision"].get("status") not in {"allowed", "blocked", "unknown"}:
        raise ValueError("invalid decision status")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a harness decision receipt without executing the action."
    )
    parser.add_argument("--task", type=Path, required=True)
    parser.add_argument("--authority", type=Path, required=True)
    parser.add_argument("--observed", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--generated-at")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    receipt = build_receipt(
        load_json(args.task),
        load_json(args.authority),
        load_json(args.observed),
        generated_at=args.generated_at,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "receipt": str(args.output),
                "decision": receipt["decision"]["status"],
                "status": receipt["status"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

