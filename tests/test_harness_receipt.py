from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    ROOT
    / "skills"
    / "evidence-harness"
    / "scripts"
    / "harness_receipt.py"
)
SPEC = importlib.util.spec_from_file_location("harness_receipt", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class HarnessReceiptTests(unittest.TestCase):
    def test_mismatch_and_missing_authorization_block_mutation(self) -> None:
        receipt = MODULE.build_receipt(
            {
                "id": "example",
                "intent": "deploy",
                "selected_references": ["references/authority-and-action.md"],
                "action": {
                    "class": "mutate",
                    "requested": "deploy",
                    "authorization_present": False,
                },
            },
            {"source": "contract", "expected_state": {"project": "alpha"}},
            {"state": {"project": "beta"}},
            generated_at="2026-08-31T20:00:00+00:00",
        )
        self.assertEqual(receipt["decision"]["status"], "blocked")
        self.assertEqual(
            receipt["decision"]["reasons"],
            ["mismatch:project", "authorization:missing"],
        )
        self.assertEqual(receipt["status"], "blocked")

    def test_matching_observation_allows_read_only_decision(self) -> None:
        receipt = MODULE.build_receipt(
            {
                "id": "example",
                "intent": "inspect",
                "action": {
                    "class": "observe",
                    "requested": "read status",
                    "authorization_present": False,
                },
            },
            {"source": "contract", "expected_state": {"project": "alpha"}},
            {"state": {"project": "alpha"}},
            generated_at="2026-08-31T20:00:00+00:00",
        )
        self.assertEqual(receipt["decision"]["status"], "allowed")
        self.assertEqual(receipt["status"], "drafted")

    def test_nested_missing_state_is_explicit(self) -> None:
        receipt = MODULE.build_receipt(
            {
                "id": "example",
                "intent": "inspect",
                "action": {
                    "class": "observe",
                    "requested": "read status",
                    "authorization_present": False,
                },
            },
            {
                "source": "contract",
                "expected_state": {"service": {"name": "web", "region": "east"}},
            },
            {"state": {"service": {"name": "web"}}},
            generated_at="2026-08-31T20:00:00+00:00",
        )
        self.assertEqual(receipt["decision"]["reasons"], ["missing:service.region"])

    def test_unknown_action_class_fails_closed(self) -> None:
        with self.assertRaises(ValueError):
            MODULE.build_receipt(
                {
                    "id": "example",
                    "intent": "act",
                    "action": {
                        "class": "improvise",
                        "requested": "act",
                        "authorization_present": True,
                    },
                },
                {"source": "contract", "expected_state": {}},
                {"state": {}},
            )


if __name__ == "__main__":
    unittest.main()

