"""RULES-01 eight-source-join preflight: boundaries and immutable reference checks."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "research/recovered/STONEAGE-RULES01-CROSSSYSTEM-PREFLIGHT-R1.json"


class Rules01Preflight(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(DATA.read_text(encoding="utf-8"))

    def test_eight_unique_source_boundaries(self):
        d = self.report
        self.assertEqual("RULES01_SOURCE_QUALIFIED_PREFLIGHT_NOT_CLOSED", d["package_status"])
        self.assertEqual("PARTIAL_OPEN", d["stage_a"])
        self.assertEqual("GATED", d["stage_b"])
        self.assertEqual(8, len(d["seams"]))
        self.assertEqual(8, len({v["id"] for v in d["seams"]}))
        for s in d["seams"]:
            self.assertTrue(s["refs"] and s["inputs"] and s["open"] and s["impact"])
            self.assertFalse(s["class"].startswith("V1_PROVEN_COMPLETE"))

    def test_exact_committed_evidence_blobs(self):
        for key, o in self.report["source_pins"].items():
            payload = (ROOT / o["path"]).read_bytes()
            self.assertEqual(len(payload), o["bytes"], key)
            digest = hashlib.sha1(b"blob " + str(len(payload)).encode() + bytes([0]) + payload).hexdigest()
            self.assertEqual(digest, o["blob"], key)

    def test_two_exp_regimes_not_collapsed(self):
        text = (ROOT / self.report["source_pins"]["exp"]["path"]).read_text(encoding="utf-8")
        self.assertIn("Legacy compiled cumulative path", text)
        self.assertIn("Later external per-level path", text)
        self.assertIn("JSS-1999 threshold representation and exact table", text)
        self.assertIn("STONEAGE-BATTLE-EXP-SETTLEMENT", self.report["source_pins"]["exp"]["path"])

    def test_quest_gate_and_saving_are_not_early_promotions(self):
        d = {s["seam"]: s for s in self.report["seams"]}
        self.assertIn("normal item purchase", d["ITEM_OWNERSHIP_TO_WARPMAN_AND_AWARD"]["known"])
        self.assertIn("unlock precedes known durable write", d["PERSISTENT_FIELDS_TO_SAVE_AND_LOGIN"]["known"])
        self.assertIn("R79_PAUSED_NON_BLOCKING", self.report["blocked_savedata_track"])


if __name__ == "__main__":
    unittest.main()
