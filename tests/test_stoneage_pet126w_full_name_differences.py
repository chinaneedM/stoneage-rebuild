"""PET126W: 124 original PC pet-name pairs, orthographic vs nonorthographic, no species promotion."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "research" / "recovered"
NEW = R / "STONEAGE-PET126W-TW10-CN50-ALL-124-ORIGINAL-PC-NAME-VARIANTS-R1.json"

def git_blob(path):
    body = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(body)).encode("ascii") + b"\0" + body).hexdigest()

class PET126WAllOriginalNameRows(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(NEW.read_text(encoding="utf-8"))
        cls.tw = json.loads((R / "STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json").read_text(encoding="utf-8"))
        cls.cn = json.loads((R / "STONEAGE-PET126R-CN50-PC-ORIGINAL-ALBUM-FULL-362-SLOT-SOURCE-CATALOGUE-R1.json").read_text(encoding="utf-8"))
        cls.prior = json.loads((R / "STONEAGE-PET126V-TW10-CN50-WAEI2001-THREE-CARRIER-PET-NAME-VARIANTS-R1.json").read_text(encoding="utf-8"))

    def test_immutable_original_derived_source_blobs(self):
        for k in ("tw10", "cn50", "prior_pet126v"):
            src = self.receipt["sources"][k]
            self.assertEqual(src["git_blob"], git_blob(ROOT / src["path"]))
        b = self.receipt["evidence_limits"]
        current = ROOT / "docs" / "CURRENT-STATE.md"
        self.assertEqual(current.stat().st_size, b["historical_current_size_bytes"])
        self.assertEqual(git_blob(current), b["historical_current_full_blob_untouched"])

    def test_all_124_pairs_are_replayed_from_source_records(self):
        x = self.receipt
        rows = x["records"]
        trans = x["naming_policy"]["explicitly_checked_hant_to_hans_character_substitutions"]
        expected_chars = {
            "魯":"鲁", "寶":"宝", "爾":"尔", "貝":"贝", "烏":"乌", "達":"达",
            "頓":"顿", "諾":"诺", "薩":"萨", "凱":"凯", "龜":"龟", "蘭":"兰",
            "瑪":"玛", "奧":"奥", "綠":"绿", "亞":"亚", "則":"则", "揚":"扬",
            "齊":"齐", "鮑":"鲍", "倫":"伦", "雞":"鸡", "給":"给", "將":"将"
        }
        self.assertEqual(trans, expected_chars)
        self.assertEqual((len(rows), len(self.tw["records"]), len(self.cn["records"])), (124, 124, 362))
        observed = {}
        seen = set()
        for row, t in zip(rows, self.tw["records"]):
            ordinal = t["graphic_number"] - 100250
            c = self.cn["records"][ordinal]
            self.assertNotIn(ordinal, seen)
            seen.add(ordinal)
            self.assertEqual((row["album_ordinal"], row["ordinal_graphic_hypothesis"], c["ordinal"]), (ordinal, t["graphic_number"], ordinal))
            self.assertEqual((row["tw10_original_literal"], row["cn50_preserved_compiled_literal"]), (t["name_as_written"], c["label_as_compiled_GB18030"]))
            self.assertEqual((row["tw10_original_row_sha256"], row["cn50_original_row_sha256"]), (t["source_row_sha256"], c["source_exe_row_sha256"]))
            self.assertEqual(row["shared_full_original_spr_segment_sha256"], t["spr_original_segment_sha256"])
            self.assertEqual(row["shared_full_original_spr_segment_sha256"], c["same_CAB_SPR_group_hash_for_hypothesis"])
            self.assertTrue(c["TW10_retail_exact_same_SPR_segment_at_this_ordinal"])
            norm = "".join(trans.get(ch, ch) for ch in t["name_as_written"])
            self.assertEqual(row["tw10_to_hans_bounded_normalization"], norm)
            rel = ("EXACT_SOURCE_LITERAL" if t["name_as_written"] == c["label_as_compiled_GB18030"]
                   else "TRADITIONAL_SIMPLIFIED_ORTHOGRAPHIC_ONLY" if norm == c["label_as_compiled_GB18030"]
                   else "NON_ORTHOGRAPHIC_SOURCE_LITERAL_VARIANT")
            self.assertEqual(row["relation"], rel)
            observed[rel] = observed.get(rel, 0) + 1
            self.assertIsNone(row["same_server_pet_id"])
            self.assertFalse(row["original_cn50_native_selector_proven"])
            self.assertFalse(row["official_live_pet_issuance_proven"])
        self.assertEqual(observed, {
            "EXACT_SOURCE_LITERAL": 49,
            "TRADITIONAL_SIMPLIFIED_ORTHOGRAPHIC_ONLY": 72,
            "NON_ORTHOGRAPHIC_SOURCE_LITERAL_VARIANT": 3
        })
        self.assertEqual(x["result_counts"]["source_qualified_pairs"], 124)
        self.assertEqual(x["result_counts"]["identical_source_literals"], 49)
        self.assertEqual(x["result_counts"]["orthographic_only_script_differences"], 72)
        self.assertEqual(x["result_counts"]["non_orthographic_literal_variants"], 3)
        self.assertEqual(x["result_counts"]["all_original_full_SPR_segments_sha256_equal"], 124)

    def test_exact_three_nonorthographic_rows_have_prior_player_web_caveat(self):
        expected = {
            70: ("卡搭寶斯", "卡拉宝斯", "卡拉寶斯"),
            133: ("拉可洛斯", "拉可拉斯", "拉可拉斯"),
            134: ("巴洛洛克斯", "邦洛洛克斯", "邦洛洛克斯"),
        }
        three = [r for r in self.receipt["records"] if r["relation"] == "NON_ORTHOGRAPHIC_SOURCE_LITERAL_VARIANT"]
        self.assertEqual(set(r["album_ordinal"] for r in three), set(expected))
        self.assertEqual(len(self.prior["name_variant_relationships"]), 3)
        for r in three:
            ord = r["album_ordinal"]
            tw, cn, museum = expected[ord]
            self.assertEqual((r["tw10_original_literal"], r["cn50_preserved_compiled_literal"], r["web2001_player_museum_third_source"]["web_museum_name"]), (tw, cn, museum))
            p = next(x for x in self.prior["name_variant_relationships"] if x["tw10_original_client"]["album_ordinal"] == ord)
            self.assertEqual(p["tw2001_operator_hosted_player_museum"]["name_as_archived"], museum)
            self.assertFalse(p["tw2001_operator_hosted_player_museum"]["client_pet_identity_confirmed"])
            self.assertFalse(p["cn50_preserved_client"]["native_name_to_sprite_selector_proven"])

    def test_no_invented_pet_population_or_premature_pc_module_switch(self):
        b = self.receipt["evidence_limits"]
        self.assertEqual(self.receipt["scope"], "HISTORICAL_ORIGINAL_CLASSIC_2D_PC_ONLY")
        self.assertEqual(b["new_official_live_species_proven"], 0)
        self.assertIsNone(self.receipt["result_counts"]["overall_official_species_total"])
        self.assertFalse(b["mobile_or_dual_end_included"])
        self.assertFalse(b["private_server_only_pets_included"])
        self.assertFalse(b["original_proprietary_bytes_in_public_git"])
        self.assertFalse(b["pet_module_closed"])
        self.assertFalse(b["npc_module_started"])
        self.assertEqual(b["year_2026"], "NOT_YEAR_AUDITED")
        self.assertEqual(b["stage_A"], "7_PARTIAL_2_OPEN")
        self.assertEqual(b["stage_B_and_wiki"], "GATED")
        self.assertEqual(b["r79"], "PAUSED_NON_BLOCKING")
        self.assertIsNone(b["overall_percent"])

if __name__ == "__main__":
    unittest.main()
