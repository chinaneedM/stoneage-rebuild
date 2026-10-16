"""Stage A finite nine-family source-custody and false-completion safeguards."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/recovered/STONEAGE-STAGE-A-NINE-FAMILY-PREFLIGHT-R1.json"
PORTFOLIO = ROOT / "research/recovered/STONEAGE-RESTORATION-PORTFOLIO-R1.json"


class StageAPreflight(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(REPORT.read_text(encoding="utf-8"))
        cls.portfolio = json.loads(PORTFOLIO.read_text(encoding="utf-8"))

    def test_nine_family_ids_and_gates_are_portfolio_faithful(self):
        p = {x["id"]: x["gate"] for x in self.portfolio["families"]}
        s = {x["id"]: x["portfolio_gate"] for x in self.data["families"]}
        self.assertEqual(9, len(p))
        self.assertEqual(p, s)
        self.assertFalse(self.data["stage_a_accepted"])
        self.assertEqual("GATED", self.data["stage_b_gate"])
        self.assertIsNone(self.data["restoration_percentage"])
        self.assertTrue(all(not f["stage_a_accepted"] for f in self.data["families"]))
        for f in self.data["families"]:
            self.assertTrue(f["existing_evidence_paths"])
            for key in ("representative", "source_status", "material_gap", "replay_scope", "reopen", "decision"):
                self.assertTrue(f[key])

    def test_thirteen_source_blob_pins_are_exact(self):
        self.assertEqual(13, len(self.data["source_pins"]))
        for key, src in self.data["source_pins"].items():
            payload = (ROOT / src["path"]).read_bytes()
            self.assertEqual(src["bytes"], len(payload), key)
            sha = hashlib.sha1(
                b"blob " + str(len(payload)).encode("ascii") + bytes([0]) + payload
            ).hexdigest()
            self.assertEqual(src["git_blob"], sha, key)

    def test_five_taiwan_v1_ui_crosswalk_tasks_not_historical_completion(self):
        x = self.data
        self.assertEqual("UI-SEMANTICS-01", x["next_priority"])
        self.assertEqual("graphics_audio_ui", x["priority_choice"]["family"])
        self.assertTrue(x["priority_choice"]["not_engine_selection"])
        self.assertEqual(5, len(x["ui_surfaces"]))
        self.assertEqual(5, len({z["id"] for z in x["ui_surfaces"]}))
        for entry in x["ui_surfaces"]:
            self.assertIn("V1_DIRECT", entry["version_source"])
            self.assertTrue(entry["direct_anchor"] and entry["need"] and entry["forbidden"])
        self.assertEqual("PAUSED_NON_BLOCKING",
            "PAUSED_NON_BLOCKING" if any("PAUSED_NON_BLOCKING" in s for s in x["deferred_named_gaps"]) else "")

    def test_direct_client_is_not_claimed_original_server(self):
        self.assertIn("does not contain original commercial server",
                      " ".join(self.data["explicit_no_promotions"]))
        self.assertTrue(any("R79" in s for s in self.data["deferred_named_gaps"]))
        self.assertEqual("PREFLIGHT_CLOSED_STAGE_A_NOT_ACCEPTED",
                         self.data["status"])


if __name__ == "__main__":
    unittest.main()
