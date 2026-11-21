"""Cross-check 2001 Waei player-contributed reports against TW1 124 client candidates."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "research" / "recovered"
P = ROOT / "research" / "pets"

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def blob_sha(path):
    b = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\x00" + b).hexdigest()

class PETDetailEvidence01Waei2001(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.web = read(R / "STONEAGE-PET41-TW-EARLY-WGS-MUSEUM-R1.json")
        cls.gap = read(R / "STONEAGE-PET42-TW10-OPERATOR-MUSEUM-BIDIRECTIONAL-GAP-R1.json")
        cls.tw = read(R / "STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json")
        cls.reg = read(P / "PET-ID-REGISTRY-R1.json")
        cls.progress = read(P / "PET-PROGRESS-R1.json")
        cls.out = read(P / "PET-DETAIL-EVIDENCE01-WAEI2001-WITNESSES-R1.json")

    def test_same_exact_source_blobs_and_no_new_official_values(self):
        sources = self.out["pinned_sources"]
        for key, source in (("tw10", self.tw), ("waei2001", self.web), ("name_diff", self.gap), ("registry", self.reg)):
            self.assertEqual(blob_sha(ROOT / sources[key]["path"]), sources[key]["git_blob"])
        self.assertEqual(self.out["source_qualification"], "TW1_AUTHENTICATED_PC_CLIENT_VS_2001_WAEI_OPERATOR_HOSTED_PLAYER_CONTRIBUTIONS_NOT_OFFICIAL_PET_MASTER")
        guard = self.out["evidence_guards"]
        self.assertFalse(guard["exact_name_implies_official_original_pet_species"])
        self.assertFalse(guard["player_contributed_element_numbers_can_fill_original_combat_stats"])
        self.assertFalse(guard["near_name_can_inherit_player_elements_or_acquisition"])
        self.assertFalse(guard["original_gif_equals_client_SPR_or_RD_authenticated"])
        self.assertFalse(guard["original_server_identity_growth_skill_capture_or_reward_proven"])
        self.assertEqual(guard["current_state_original_blob_unmodified"], blob_sha(ROOT / "docs/CURRENT-STATE.md"))
        self.assertEqual(guard["year_2026"], "NOT_YEAR_AUDITED")
        self.assertFalse(guard["pet_module_closed"])

    def test_124_individual_links_and_106_player_rows_rederived_from_sources(self):
        web = self.web["rows"]
        client = self.tw["records"]
        entries = self.out["entries"]
        source_rows = self.reg["catalog_entries"]
        self.assertEqual((len(client), len(web), len(entries), len(source_rows)), (124, 128, 124, 124))
        pages = {p["filename"]: p for p in self.web["pages"]}
        selected = {p["web_ordinal"]: p for p in self.web["selected_contributions"]}
        matched = 0
        matched_profiles = 0
        near_profiles = 0
        selected_count = 0
        element_web_rows = 0
        for i, (source, cat, entry) in enumerate(zip(client, source_rows, entries)):
            self.assertEqual(entry["pet_id"], cat["catalog_pet_id"])
            self.assertEqual(entry["profile_md_path"], cat["visible_dossier_path"])
            self.assertEqual(entry["profile_json_path"], cat["machine_dossier_path"])
            self.assertEqual(entry["tw10_original_name"], source["name_as_written"])
            self.assertEqual(entry["source_tw10_name_row_sha256"], source["source_row_sha256"])
            self.assertEqual(entry["source_tw10_graphic_number"], source["graphic_number"])
            self.assertEqual(entry["tw10_original_portrait_rd_located"], source["portrait_rd"] is not None)
            exact = [r for r in web if r["name_as_written"] == source["name_as_written"]]
            actual = entry["exact_original_printed_name_web_witnesses"]
            self.assertEqual([r["web_ordinal"] for r in actual], [r["web_ordinal"] for r in exact])
            if exact: matched_profiles += 1
            matched += len(actual)
            for deriv, orig in zip(actual, exact):
                page = pages[orig["source_page"]]
                self.assertEqual((deriv["web_original_name"], deriv["source_html_page"]),
                                 (orig["name_as_written"], orig["source_page"]))
                self.assertEqual(deriv["archived_html_replay_url"], page["replay_url"])
                self.assertEqual(deriv["archived_html_sha256"], page["sha256"])
                self.assertEqual(deriv["archived_page_capture_utc"], page["archive_capture"])
                self.assertEqual(deriv["web_gif_url_as_unverified_reference"], orig["web_image_url"])
                self.assertEqual(deriv["player_submitted_four_element_claim_unverified"], orig["contributed_elements"])
                self.assertEqual(deriv["contributed_location_field_sha256"], orig["contributed_location_sha256"])
                self.assertIsNone(deriv["contributed_location_text_for_this_pet_in_source_catalog"])
                self.assertFalse(deriv["original_live_issue_or_native_gameplay_proven"])
                self.assertEqual(deriv["match_grade"], "EXACT_TEXT_NAME_ONLY_NOT_SAME_BUILD_OR_SPECIES")
                if orig["contributed_elements"]: element_web_rows += 1
                note = deriv["selected_player_claim"]
                if orig["web_ordinal"] in selected:
                    selected_count += 1
                    self.assertEqual(note, {"kind": selected[orig["web_ordinal"]]["claim_kind"],
                                            "summary": selected[orig["web_ordinal"]]["summary"]})
                else: self.assertIsNone(note)
            expected_near = []
            for rec in self.gap["website_non_exact_client_name_rows"]:
                possibles = {r["client_graphic_number"] for r in rec["single_edit_client_name_candidates"]}
                if rec["matched_client_base_graphic_candidate"] is not None:
                    possibles.add(rec["matched_client_base_graphic_candidate"])
                if source["graphic_number"] in possibles: expected_near.append(rec)
            actual_near = entry["nonexact_textual_leads_without_identity"]
            self.assertEqual([r["web_ordinal"] for r in actual_near], [r["web_ordinal"] for r in expected_near])
            if actual_near: near_profiles += 1
            for n in actual_near:
                self.assertTrue(n["ambiguous_and_not_identity_certified"])
                self.assertTrue(n["reported_values_not_transferred"])
                self.assertNotIn("player_submitted_four_element_claim_unverified", n)
            self.assertIsNone(entry["official_same_server_pet_id"])
            self.assertFalse(entry["official_living_pet_release_verified"])
            profile = read(ROOT / entry["profile_json_path"])
            self.assertEqual(profile["profile_id"], entry["pet_id"])
            self.assertEqual(profile["version_scope"]["product_line"], "CLASSIC_ORIGINAL_2D_PC")
            self.assertTrue(all(x is None for x in profile["combat_stats"]["elements"].values()))
            self.assertTrue(all(x is None for x in profile["combat_stats"]["level_1"]["values"].values()))
            self.assertIsNone(profile["skills"]["innate_at_acquisition"])
            self.assertIsNone(profile["acquisition"]["original_capture"]["coordinates"])
            self.assertFalse(profile["actual_official_pet_identity"]["official_living_pet_release_proven"])
            self.assertFalse(profile["status"]["all_fields_historically_complete"])
        self.assertEqual((matched, matched_profiles, 124-matched_profiles, near_profiles, selected_count),
                         (106, 105, 19, 15, 8))
        counts = self.out["counts"]
        self.assertEqual(counts["web_rows_with_exact_original_client_name"], matched)
        self.assertEqual(counts["distinct_tw10_client_pet_profiles_with_exact_name"], matched_profiles)
        self.assertEqual(counts["exact_name_web_rows_with_player_element_numbers"], element_web_rows)
        self.assertEqual(counts["all_historically_verified_pet_profiles"], 0)
        self.assertEqual(self.progress["historical_documentary_crosscheck"]["player_element_claim_rows_with_exact_name"], element_web_rows)

    def test_duplicate_web_rows_and_missing_portraits_preserved(self):
        self.assertEqual([e["pet_id"] for e in self.out["entries"]
                          if not e["tw10_original_portrait_rd_located"]],
                         ["PET-000116", "PET-000117", "PET-000118", "PET-000119"])
        duplicate = next(e for e in self.out["entries"] if e["tw10_original_name"] == "克克爾")
        self.assertEqual([x["web_ordinal"] for x in duplicate["exact_original_printed_name_web_witnesses"]],[41,103])
        view = (ROOT / "docs/pets/WAEI-2001-PLAYER-MUSEUM-CROSSWALK.md").read_text(encoding="utf-8")
        for e in self.out["entries"]:
            self.assertIn("[" + e["pet_id"] + "]", view)
        self.assertIn("0041（", view)
        self.assertIn("0103（", view)
        self.assertIn("不是官服", view)
        self.assertIn("玩家", (ROOT / "docs/pets/INDEX.md").read_text(encoding="utf-8"))

if __name__ == "__main__": unittest.main()
