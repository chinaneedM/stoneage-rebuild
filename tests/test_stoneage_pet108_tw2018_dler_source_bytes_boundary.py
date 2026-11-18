"""PET108: third-party Taiwan client candidate checksum is not recovered original source bytes."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "research/recovered/STONEAGE-PET108-TW-CLIENT-DLER-170423-CHECKSUM-ACCESS-BOUNDARY-R1.json"
QUEUE = ROOT / "research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
REPORT = ROOT / "docs/continuity/STONEAGE-PET108-TW-2018-DLER-CLIENT-HASH-AND-2016-SOURCE-ACCESS-20261118.md"


class TestPet108ThirdPartyClientBoundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = json.loads(AUDIT.read_text(encoding="utf-8"))
        cls.q = json.loads(QUEUE.read_text(encoding="utf-8"))

    def test_2016_frontier_stays_open(self):
        a, q = self.a, self.q
        y = next(x for x in q["yearly_work_queue"] if x["year"] == 2016)
        self.assertEqual(q["active_module"], "PET")
        self.assertEqual(a["module"], "PET")
        self.assertEqual((a["year_frontier_before"], a["year_frontier_after"]), (2016, 2016))
        self.assertEqual(q["current_frontier"]["year"], 2016)
        self.assertEqual(y["research_gate"], "NOT_YEAR_AUDITED")
        self.assertFalse(a["historically_complete"])
        self.assertFalse(a["year_source_bounded_reviewed"])
        self.assertIn(a["id"], [x["id"] for x in y["partial_source_review_receipts"]])  # retained history
        self.assertTrue(a["next"].startswith("PET109:"))  # historical next is not the live next
        self.assertIsNone(a["year2016_species_count"])
        self.assertIsNone(a["year2016_first_release_count"])
        self.assertIn("PET108", REPORT.read_text(encoding="utf-8"))

    def test_exact_web_claim_not_recomputed_native_sha(self):
        a = self.a
        d = a["candidate"]
        self.assertTrue(a["prior_dler_2018_listing_already_known"])
        self.assertEqual(d["declared_file_size_bytes"], 1039663798)
        self.assertEqual(d["declared_md5"], "510f9811a3341d5023ecdd3b55c15482")
        self.assertEqual(len(d["declared_md5"]), 32)
        self.assertEqual(d["portal_file_date"], "2018-07-23")
        self.assertEqual(d["portal_update_date"], "2018-07-24")
        self.assertEqual(d["label_token"], "170423")
        self.assertTrue(d["label_token_not_authenticated_build_date"])
        self.assertIn("StoneAge.rar", d["download_target_url"])
        self.assertIn("404", d["download_target_web_fetch_result"])
        self.assertFalse(d["original_download_file_obtained"])
        self.assertFalse(d["actual_file_md5_recomputed"])
        self.assertIsNone(d["actual_file_sha256"])
        self.assertFalse(d["archive_crc_validated"])
        self.assertFalse(d["original_operator_build_authenticated"])
        self.assertFalse(d["original_2016_client_identity_proven"])
        self.assertTrue(all(a["negative_controls"].values()))

    def test_client_unavailable_original_state_and_module(self):
        a, q = self.a, self.q
        for name in (
            "new_original_2016_client_bytes", "new_original_2016_patch_bytes",
            "new_original_2016_same_build_pet_ids", "new_original_2016_spr_pixels",
            "new_native_pet_skills", "new_native_live_grant_logs",
        ):
            self.assertEqual(a[name], 0)
        raw = (ROOT / "docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw), a["current_state_bytes_unchanged"])
        calc = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest()
        self.assertEqual(calc, a["current_state_blob_unchanged"])
        self.assertEqual(
            (a["stage_A"], a["stage_B_wiki"], a["r79"], a["overall_game_completion_percent"]),
            (q["stage_A"], q["stage_B_wiki"], q["r79"], q["overall_game_completion_percent"])
        )


if __name__ == "__main__":
    unittest.main()
