"""PET126B: official original-classic-PC documentary release events vs candidate sources."""
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "research/recovered"
sys.path.insert(0, str(ROOT / "tools"))
from stoneage_pet16_lookup import official_pc_release_view

P25 = R / "STONEAGE-PET25-OFFICIAL-RELEASE-ROSTER-R1.json"
P26 = R / "STONEAGE-PET26-JP-TW-CLASSIC-OFFICIAL-RELEASE-R1.json"
CNWEB = R / "STONEAGE-WAEI-CN20-NEW-PET-FINITE-CATALOG-R1.json"
JPWEB = R / "STONEAGE-JP-OFFICIAL-PET-CATALOG-R1.json"
CLI = ROOT / "tools/stoneage_pet16_lookup.py"


class OfficialOnlyPETReleaseView(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p25 = json.loads(P25.read_text(encoding="utf-8"))
        cls.p26 = json.loads(P26.read_text(encoding="utf-8"))
        cls.cn = json.loads(CNWEB.read_text(encoding="utf-8"))
        cls.jp = json.loads(JPWEB.read_text(encoding="utf-8"))

    def test_original_pc_event_counts_and_no_species_totals(self):
        out = official_pc_release_view(self.p25, self.p26)
        all_rows = out["records"]
        self.assertEqual(len(all_rows), 9)
        counts = out["counts_all_unfiltered_not_pet_species"]
        self.assertEqual((counts["documentary_release_events"],
                          counts["named_pet_or_form_release_events"],
                          counts["family_or_card_series_events"],
                          counts["unnamed_pair_events_not_two_separate_documentary_events"]),
                         (9, 5, 3, 1))
        self.assertIsNone(counts["unique_original_pc_species_population"])
        self.assertEqual(counts["native_original_pc_species_id_verified"], 0)
        self.assertEqual({x["region"] for x in all_rows}, {"CN", "JP"})
        self.assertEqual({x["source_namespace"] for x in all_rows}, {"PET25", "PET26"})
        self.assertTrue(all(x["product_line"].startswith("STONEAGE_CLASSIC_PC_") for x in all_rows))
        self.assertTrue(all(x["native_original_pc_pet_id"] is None for x in all_rows))
        self.assertTrue(all(x["unique_global_species_contribution"] is None for x in all_rows))
        self.assertTrue(all(not x["first_actual_official_release_date_proven"] for x in all_rows))
        self.assertTrue(all(out["negative_boundaries"].values()))
        for row in all_rows:
            self.assertTrue(row["source_references"])
            self.assertTrue(all(x["url"].startswith("https://") for x in row["source_references"]))

    def test_named_events_remain_separate_from_family_events(self):
        out = official_pc_release_view(self.p25, self.p26)
        indexed = {x["record_id"]: x for x in out["records"]}
        self.assertEqual(indexed["CN-PC-3-YEAR"]["original_name_or_null"], "年兽")
        self.assertEqual(indexed["CN-PC-3-YEAR"]["record_identity_kind"],
                         "FAMILY_OR_CARD_SERIES")
        self.assertEqual(indexed["CN-PC-4-MECHLEOPARD"]["original_name_or_null"],
                         "艾迪希洛")
        self.assertEqual(indexed["CN-PC-4-MECHLEOPARD"]["record_identity_kind"], "NAMED_PET")
        self.assertEqual(indexed["JP-2008-FUKUURI"]["original_name_or_null"], "フクゥーリ")
        self.assertIsNone(indexed["JP-2006-TWO-MYSTERY"]["original_name_or_null"])
        self.assertEqual(indexed["JP-2006-TWO-MYSTERY"]["record_identity_kind"],
                         "UNNAMED_PAIR_ONE_RELEASE_EVENT")

    def test_only_exact_preexisting_web_literal_comparison_without_identity(self):
        out = official_pc_release_view(
            self.p25, self.p26, check_earlier_web_names=True,
            cn_page=self.cn, jp_page=self.jp)
        self.assertEqual((len(self.cn["records"]), len(self.jp["records"])), (104, 124))
        self.assertEqual(out["returned_event_count"], 9)
        self.assertTrue(all(x["earlier_operator_web_exact_literal_matches"] == []
                            for x in out["records"]))
        self.assertTrue(all(x["web_literal_match_is_not_pet_identity"]
                            for x in out["records"]))
        self.assertTrue(all(x["web_archive_is_not_a_later_live_promotion"]
                            for x in out["records"]))

    def test_exact_name_region_filter_and_unmatched_unknown(self):
        cn = official_pc_release_view(self.p25, self.p26, query="蒙奇", region="CN")
        jp = official_pc_release_view(self.p25, self.p26, query="ハクエン", region="JP")
        miss = official_pc_release_view(self.p25, self.p26, query="非官方不存在的新宠")
        self.assertEqual([x["record_id"] for x in cn["records"]], ["CN-PC-MONKEY-2003"])
        self.assertEqual([x["record_id"] for x in jp["records"]], ["JP-2009-HAKUEN"])
        self.assertEqual(miss["returned_event_count"], 0)
        self.assertIsNone(miss["counts_all_unfiltered_not_pet_species"]["unique_original_pc_species_population"])

    def test_cli_official_mode_without_community_catalog_load(self):
        script = [sys.executable, str(CLI), "--official-releases"]
        simple = subprocess.run(script + ["--release-region", "JP", "--query", "コクエン"],
                                cwd=ROOT, capture_output=True, text=True, check=True)
        obj = json.loads(simple.stdout)
        self.assertEqual([x["record_id"] for x in obj["records"]], ["JP-2009-KOKUEN"])
        self.assertEqual(obj["returned_event_count"], 1)
        summary = subprocess.run(script + ["--summary"], cwd=ROOT,
                                 capture_output=True, text=True, check=True)
        stat = json.loads(summary.stdout)
        self.assertEqual(stat["counts_all_unfiltered_not_pet_species"]["documentary_release_events"], 9)
        self.assertEqual(stat["records"], [])
        incompatible = subprocess.run(script + ["--trace-graphic", "100400"], cwd=ROOT,
                                      capture_output=True, text=True)
        self.assertNotEqual(incompatible.returncode, 0)
        self.assertIn("independent", incompatible.stderr)

    def test_historical_current_state_stays_original(self):
        raw = (ROOT / "docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw), 2709173)
        git = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()
        self.assertEqual(git, "c89e0e33537990aa2132b47c40fef49a985a935c")


if __name__ == "__main__":
    unittest.main()
