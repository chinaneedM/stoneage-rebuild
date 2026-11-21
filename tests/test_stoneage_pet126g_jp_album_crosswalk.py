"""PET126G: cross-source public text consistency; no original art or native ID promotion."""
import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "research/recovered" / name).read_text(encoding="utf-8"))


class JapanOriginalPcAlbumBoundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = load("STONEAGE-PET126G-JP-OPERATOR-PLAYER-ALBUM-2003-2010-CROSSWALK-R1.json")
        cls.official = load("STONEAGE-JP-OFFICIAL-PET-CATALOG-R1.json")
        cls.p26 = load("STONEAGE-PET26-JP-TW-CLASSIC-OFFICIAL-RELEASE-R1.json")
        cls.p72 = load("STONEAGE-PET72-YEAR2005-CN-TW-JP-KR-SOURCE-R1.json")

    def test_early_operator_source_authentication_with_dates(self):
        r = self.r["operator_early"]
        self.assertEqual(r["file"], "research/recovered/STONEAGE-JP-OFFICIAL-PET-CATALOG-R1.json")
        self.assertEqual(len(self.official["records"]), 124)
        self.assertEqual(r["rows"], 124)
        self.assertEqual(r["source_identity"], "HANGAME_JP_OPERATOR_WEB_ORIGINAL_ARCHIVED")
        self.assertTrue(r["web_name_not_same_build_pet_id"])
        timestamps = sorted({
            ref["actual_capture"]
            for record in self.official["records"]
            for ref in record["source_refs"]
        })
        self.assertEqual(timestamps[0], r["archived_capture_range_utc"]["earliest"])
        self.assertEqual(timestamps[-1], r["archived_capture_range_utc"]["latest"])
        self.assertEqual(timestamps[0][:4], "2003")
        self.assertEqual(timestamps[-1][:4], "2004")
        origins = {
            ref["source"]
            for record in self.official["records"]
            for ref in record["source_refs"]
        }
        self.assertEqual(set(r["origins"]), origins)
        self.assertEqual(sorted(x["web_ordinal"] for x in self.official["records"]),
                         list(range(1, 125)))

    def test_full_124_positions_are_recomputable_and_exactly_23_diverge(self):
        comp = self.r["compared_prefix"]
        earlier = self.official["records"]
        later = comp["later_fan_names_by_position_1_to_124"]
        self.assertEqual(len(earlier), 124)
        self.assertEqual(len(later), 124)
        self.assertEqual(comp["operator_web_positions"], 124)
        self.assertEqual(comp["fan_album_positions_manually_read"], 124)
        self.assertEqual(comp["comparison"], "EXACT_STRING_AT_MATCHED_PUBLIC_WEB_ORDINAL_ONLY")
        self.assertEqual(comp["normalization"], "NONE")
        self.assertTrue(comp["changed_names_never_assume_same_species"])
        actual = []
        for i, rec in enumerate(earlier):
            self.assertEqual(rec["web_ordinal"], i + 1)
            if later[i] != rec["name_as_written"]:
                actual.append({
                    "ordinal": i + 1,
                    "earlier_operator_web_name": rec["name_as_written"],
                    "later_fan_album_name": later[i],
                    "early_source_archive_capture_utc": rec["source_refs"][0]["actual_capture"],
                    "interpretation": "SAME_ORDINAL_TEXT_DIVERGENCE_NOT_PROVEN_RENAME_OR_SAME_PET_ID",
                })
        self.assertEqual(len(actual), 23)
        self.assertEqual(len(earlier) - len(actual), 101)
        self.assertEqual(comp["exact_same_unicode_text"], 101)
        self.assertEqual(comp["different_unicode_text"], 23)
        self.assertEqual(actual, comp["differences"])
        self.assertEqual({x["ordinal"] for x in actual} & {40, 41, 42, 43},
                         {40, 41, 42, 43})
        self.assertEqual(comp["transcription_grade"],
                         "MANUALLY_READ_FROM_PUBLIC_FAN_INDEX_PAGES_NOT_PRIVATE_EXE")
        self.assertTrue(comp["public_ci_checks_saved_transcription_not_live_website"])

    def test_fan_site_cannot_be_promoted_to_247_official_species(self):
        fan = self.r["later_fan"]
        self.assertEqual(fan["type"],
                         "THIRD_PARTY_PLAYER_CONTRIBUTED_PET_STATUS_ALBUM_NOT_OFFICIAL_OPERATOR")
        self.assertEqual(fan["site_claim_as_of"], "2010-03-18")
        self.assertEqual(fan["site_claim_registered_pets"], 202)
        self.assertEqual(fan["site_index_highest_number_seen"], 247)
        self.assertEqual(len(fan["source_index_pages"]), 5)
        self.assertFalse(fan["images_downloaded"])
        self.assertFalse(fan["status_screenshots_independently_authenticated_as_original_runtime"])
        self.assertTrue(fan["site_image_reprint_prohibited_by_owner"])
        self.assertTrue(fan["site_registered_count_not_official_count"])
        self.assertTrue(fan["highest_album_ordinal_not_species_total"])

    def test_press_anchors_have_no_auto_joined_pet_id(self):
        a = self.r["release_document_crosswalk"]
        examples = a["examples"]
        self.assertEqual([x["ordinal"] for x in examples], [5, 143, 188, 200, 219, 221])
        self.assertEqual([x["name"] for x in examples], [
            "クロウリ", "ヴァンレム", "ゴルンフット", "フクゥーリ", "ハクエン", "コクエン"
        ])
        self.assertEqual(examples[0]["name"],
                         self.official["records"][4]["name_as_written"])
        self.assertEqual(examples[0]["name"],
                         self.r["compared_prefix"]["later_fan_names_by_position_1_to_124"][4])
        self.assertTrue(a["operator_2008_200th_name_equals_fan_2010_ordinal_200"])
        self.assertFalse(a["official_server_pet_id_link_verified"])
        self.assertTrue(all(x["original_pet_id"] is None for x in examples))
        p26 = {x["id"]: x for x in self.p26["new_japan_classic_official_release_events"]}
        for e in examples[-3:]:
            original = p26[e["pet26_record_id"]]
            self.assertEqual(e["name"], original["official_name_as_written_or_null"])
            self.assertEqual(e["earliest_release_time_verified"],
                             original["first_published_release_date"])
            self.assertEqual(e["original_pet_id"], original["original_client_species_ID_or_null"])
        p72 = {x["id"]: x for x in self.p72["source_records"]}
        vanrem = examples[1]
        self.assertEqual(vanrem["name"], p72[vanrem["pet72_record_id"]]["names"][0])
        self.assertFalse(p72[vanrem["pet72_record_id"]]["actual_customer_grant_verified"])
        self.assertIsNone(vanrem["earliest_release_time_verified"])
        self.assertIsNone(examples[2]["earliest_release_time_verified"])

    def test_pc_only_source_and_next_module_remain_unchanged(self):
        r, p, gate = self.r, self.r["no_promotion"], self.r["gate"]
        self.assertEqual(r["active_module"], "PET")
        self.assertIn("CLASSIC_PC_JAPAN", r["source_scope"])
        self.assertTrue(p["no_official_species_added"])
        self.assertFalse(p["original_server_pet_id_link_found"])
        self.assertTrue(p["no_same_build_graphic_link_found"])
        self.assertTrue(p["no_new_original_client_bytes"])
        self.assertTrue(p["fan_registered_202_not_official_global_species_count"])
        self.assertTrue(p["fan_max_slot_247_not_official_species_count"])
        self.assertTrue(p["earlier_2003_web_ordinal_5_makes_2005_krowri_first_global_release_inference_invalid"])
        self.assertTrue(p["do_not_publish_fan_images"])
        self.assertTrue(p["do_not_auto_correct_2003_operator_names_with_2010_player_names"])
        self.assertEqual(gate["year2026"], "NOT_YEAR_AUDITED")
        self.assertEqual(gate["pet_module"], "SOURCE_BOUNDED_PARTIAL")
        self.assertFalse(gate["source_bounded_closed"])
        self.assertFalse(gate["historically_complete"])
        self.assertFalse(gate["original_native_pet_runtime_verified"])
        self.assertEqual(gate["stage_a"], "7_PARTIAL_2_OPEN")
        self.assertEqual(gate["stage_b_wiki"], "GATED")
        self.assertEqual(gate["r79"], "PAUSED_NON_BLOCKING")
        self.assertIsNone(gate["completion_percent"])
        current = (ROOT / "docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(current), 2709173)
        blob = hashlib.sha1(b"blob " + str(len(current)).encode() + bytes([0]) + current).hexdigest()
        self.assertEqual(blob, gate["original_current_state_git_blob"])


if __name__ == "__main__":
    unittest.main()
