import json
import unittest
from pathlib import Path

from tools.stoneage_runtime_golden_contract import (
    GOLDEN_SCHEMA,
    load_runtime_golden_contract,
    verify_runtime_golden_contract,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = (
    ROOT
    / "game"
    / "STONEAGE-RUNTIME-GOLDEN-CONTRACT-R1.json"
)


class RuntimeGoldenContractTests(unittest.TestCase):

    def test_committed_fixture_matches_python_oracle(self):
        fixture = load_runtime_golden_contract(FIXTURE)
        result = verify_runtime_golden_contract(fixture)
        self.assertEqual(result["schema"], GOLDEN_SCHEMA)
        self.assertTrue(
            all(
                value == "PASS"
                for value in result["scenarios"].values()
            )
        )
        self.assertEqual(
            result["session_serialization"],
            "PASS",
        )
        self.assertEqual(result["occupancy_delta"], "PASS")
        self.assertTrue(
            all(
                value == "PASS"
                for value in result["fail_closed"].values()
            )
        )

    def test_fixture_is_synthetic_and_has_no_recovered_binary_paths(self):
        payload = FIXTURE.read_text(encoding="utf-8")
        lowered = payload.lower()
        for forbidden in (
            ".dat",
            ".adrn",
            ".map",
            ".bin",
            "sa_25",
            "server/",
            "client/",
        ):
            self.assertNotIn(forbidden, lowered)

        parsed = json.loads(payload)
        self.assertEqual(
            parsed["purpose"],
            "copyright-safe cross-language semantic parity fixture",
        )


if __name__ == "__main__":
    unittest.main()
