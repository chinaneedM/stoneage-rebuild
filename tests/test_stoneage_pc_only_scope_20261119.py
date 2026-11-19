"""Latest user scope supersession: only genuine classic PC game source records qualify."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "research/recovered"
P25 = R / "STONEAGE-PET25-OFFICIAL-RELEASE-ROSTER-R1.json"
P26 = R / "STONEAGE-PET26-JP-TW-CLASSIC-OFFICIAL-RELEASE-R1.json"
Q = R / "STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
P23 = R / "STONEAGE-PET123-YEAR2023-SIX-REGION-CLASSIC-PC-BOUNDED-AUDIT-R1.json"
P24 = R / "STONEAGE-PET124-YEAR2024-SIX-REGION-CLASSIC-PC-BOUNDED-AUDIT-R1.json"


class PCOnlyProjectScope(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p25 = json.loads(P25.read_text(encoding="utf-8"))
        cls.p26 = json.loads(P26.read_text(encoding="utf-8"))
        cls.q = json.loads(Q.read_text(encoding="utf-8"))
        cls.audit23 = json.loads(P23.read_text(encoding="utf-8"))
        cls.audit24 = json.loads(P24.read_text(encoding="utf-8"))

    def test_project_scope_and_original_pc_roster(self):
        rows = self.p25["confirmed_official_release_records"]
        self.assertEqual(len(rows), 5)
        self.assertEqual(self.p25["counts"]["release_documentary_records"], 5)
        self.assertEqual(self.p25["counts"]["per_product_line"], {"STONEAGE_CLASSIC_PC_CN_HUAYI": 5})
        self.assertTrue(all(x["product_line"] == "STONEAGE_CLASSIC_PC_CN_HUAYI" for x in rows))
        self.assertTrue(all(x["product_line"].startswith("STONEAGE_CLASSIC_PC_") for x in self.p25["remaining_unconfirmed_official_leads"]))
        self.assertEqual(len(self.p25["remaining_unconfirmed_official_leads"]), 2)
        self.assertEqual(len(self.p25["source_register"]), 8)
        self.assertEqual(self.p26["counts"]["prior_PET25_documentary_events"], 5)
        self.assertEqual(self.p26["counts"]["new_japan_release_events"], 4)
        self.assertEqual(self.p26["counts"]["combined_release_events_not_species"], 9)

    def test_chronology_is_pc_only_and_still_oldest_to_latest(self):
        events = self.q["previously_recovered_release_events_ordered_by_evidence_year_not_first_actual_release"]
        self.assertEqual(len(events), 9)
        self.assertEqual(len(set(x["source_id"] for x in events)), 9)
        self.assertTrue(all("CLASSIC_PC" in x["product_line"] for x in events))
        counts = {x["year"]: x["documentary_event_count_NOT_species"] for x in self.q["yearly_work_queue"] if x["documentary_event_count_NOT_species"]}
        self.assertEqual(counts, {2002: 4, 2003: 1, 2006: 1, 2008: 1, 2009: 2})
        self.assertEqual(self.q["current_frontier"]["year"], 2025)
        self.assertTrue(self.q["current_frontier"]["next"].startswith("PET125"))
        self.assertTrue(all(not x.get("documented_release_event_ids_from_existing_PET25_PET26") for x in self.q["yearly_work_queue"] if x["year"] >= 2010))
        self.assertFalse(any(x["research_gate"] == "NOT_YEAR_AUDITED" for x in self.q["yearly_work_queue"] if x["year"] < 2025))
        self.assertTrue(all(not x.get("historically_complete", False) for x in self.q["yearly_work_queue"] if x["research_gate"] == "SOURCE_BOUNDED_REVIEWED"))

    def test_2023_and_2024_audits_have_only_pc_evidence(self):
        for a, count in ((self.audit23, 6), (self.audit24, 3)):
            self.assertEqual(len(a["sources"]), count)
            self.assertTrue(all("CLASSIC_2D_PC" in x["product"] for x in a["sources"]))
            self.assertTrue(a["negative_controls"]["pc_only_source_records"] if a["year"] == 2023 else a["negative_controls"]["no_mobile_product_entries_in_pc_sources"])
            self.assertEqual(set(a["region_reviews"]), {"CN", "TW", "HK_MO", "KR", "JP", "OTHER"})
            self.assertIsNone(a["region_reviews"]["CN"]["pet_population"])
            self.assertEqual(a["new_original_pc_client_bytes"], 0)
        self.assertEqual(self.audit24["year_frontier_after"], 2025)
        self.assertNotIn("separate_product_line_evidence", self.audit24)

    def test_original_current_blob_and_scope_document(self):
        raw = (ROOT / "docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw), 2709173)
        self.assertEqual(hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest(),
                         "c89e0e33537990aa2132b47c40fef49a985a935c")
        p = (ROOT / "docs/PROJECT-CONTINUITY-PROTOCOL-R1.md").read_text(encoding="utf-8")
        self.assertIn("## 26. PC-only StoneAge", p)
        self.assertIn("只研究官方 PC", (ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertIn("只恢复官方 PC", (ROOT / "docs/STONEAGE-PET-OFFICIAL-GLOBAL-INCLUSION-R1.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
