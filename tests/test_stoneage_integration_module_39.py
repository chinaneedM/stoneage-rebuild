"""INTEGRATION39: replay existing source-pinned adult/rebirth named-path graph, not native behavior."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/recovered/STONEAGE-INTEGRATION39-ADULT-REBIRTH-EVENT-CREATE-SOURCE-R1.json"

def gitblob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

class Integration39(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = json.loads(OUT.read_text(encoding="utf-8"))
        cls.orig = {}
        for key, meta in cls.result["upstream"].items():
            payload = (ROOT / meta["path"]).read_bytes()
            assert gitblob(payload) == meta["git_blob"], key
            cls.orig[key] = json.loads(payload)

    def test_old_current_exact_prefix(self):
        old = self.result["baseline"]
        full = (ROOT / "docs/CURRENT-STATE.md").read_bytes()
        self.assertGreaterEqual(len(full), old["current_state_bytes"])
        self.assertEqual(gitblob(full[:old["current_state_bytes"]]), old["current_state_git_blob"])

    def test_five_exact_original_create_and_script_references(self):
        old = self.orig["char01"]
        quest = self.orig["quest01"]
        by_create = {(x[0], x[1]): x for x in old["create_rows"]}
        by_file = {x[0]: x for x in old["source_files"]}
        refs = {(x["create_source_path"], x["create_brace_ordinal"]): x
                for x in quest["source_creation_references"]}
        scripts = {x["path"]: x for x in quest["source_scripts"]}
        rows = self.result["selected_five_original_CREATE_to_script_refs"]
        self.assertEqual(len(rows), 5)
        self.assertEqual([r["floor"] for r in rows], [2000] * 5)
        self.assertEqual([r["original_borncenter_xy"] for r in rows],
                         [[54,50],[47,58],[48,58],[49,58],[50,58]])
        self.assertEqual([r["original_graphic_alias"] for r in rows],
                         [16001,100287,100288,100290,100394])
        for r in rows:
            c = by_create[(r["create_path"], r["create_ordinal"])]
            q = refs[(r["create_path"], r["create_ordinal"])]
            s = scripts[r["arg_path"]]
            self.assertEqual([r["original_create_block_sha256"],r["floor"],r["original_graphic_alias"],
                              r["original_direction"],r["function_literal"],r["resolved_template_path"],
                              r["name_text_original_sha256"]],
                             [c[4],c[5],c[6],c[10],c[11],c[13][0][0],c[14]])
            self.assertEqual(c[15][0][0], r["arg_path"])
            self.assertEqual(r["function_literal"], "changeevent")
            self.assertEqual(r["create_source_file_sha256"], by_file[r["create_path"]][2])
            self.assertEqual(r["arg_original_sha256"], by_file[r["arg_path"]][2])
            self.assertEqual([r["arg_original_bytes"],r["arg_original_sha256"],r["arg_original_crc32"]],
                             [s["original_size"],s["original_sha256"],s["original_crc32"]])
            self.assertEqual([r["floor"],r["original_borncenter_xy"],r["original_graphic_alias"]],
                             [q["floorid"],q["borncenter_numeric"],q["graphic_alias_numeric"]])
            self.assertEqual(r["origin_class"], "UNRESOLVED")

    def test_six_precise_source_sections_not_software_execution(self):
        original = self.orig["quest01"]["source_event_blocks"]
        rows = self.result["selected_five_original_CREATE_to_script_refs"]
        self.assertEqual([len(x["old_QUEST01_sections"]) for x in rows],[2,1,1,1,1])
        actual_flags = []
        for r in rows:
            for s in r["old_QUEST01_sections"]:
                matches = [x for x in original if x["script_path"] == r["arg_path"]
                           and x["script_block_ordinal"] == s["ordinal"]]
                self.assertEqual(len(matches), 1)
                old = matches[0]
                self.assertEqual([s["type"],s["event_number"],s["original_type_line"],
                                  s["condition_keywords"],s["condition_cp950_utf8_sha256"],
                                  s["source_section_cp950_utf8_sha256"],s["operation_counts"],
                                  s["original_item_ID_refs"],s["EndSetFlg_numbers"]],
                                 [old["raw_type"],old["event_number"],old["source_type_line"],
                                  old["condition_keywords"],old["condition_expression_decoded_cp950_UTF8_sha256"],
                                  old["source_section_decoded_cp950_normalized_UTF8_sha256"],
                                  old["source_operations"],old["item_numeric_refs"],old["end_set_flags"]])
                actual_flags.extend(s["EndSetFlg_numbers"])
        self.assertEqual(actual_flags,[4,39,40,42,46])
        self.assertEqual(self.result["summary"]["old_indexed_TYPE_sections"], 6)

    def test_two_same_file_but_different_function_neighbors(self):
        rows = self.result["two_other_original_CREATE_in_same_zhuans_create_excluded_from_changeevent"]
        self.assertEqual([(r["ordinal"],r["floor"],r["function_literal"]) for r in rows],
                         [(4,2000,"sb_dou"),(5,32021,"npcgen_petshop")])
        by_create = {(x[0],x[1]):x for x in self.orig["char01"]["create_rows"]}
        by_file = {x[0]:x for x in self.orig["char01"]["source_files"]}
        for r in rows:
            c = by_create[("my/zhuansheng/zhuans.create",r["ordinal"])]
            self.assertEqual([r["original_create_block_sha256"],r["graphic"],r["exact_arg_path"],
                              r["original_arg_sha256"]],
                             [c[4],c[6],c[15][0][0],c[15][0][2]])
            self.assertEqual(r["original_arg_sha256"], by_file[r["exact_arg_path"]][2])

    def test_quest32_negative_coverage_and_map_atlas_boundary(self):
        q32 = self.orig["quest32"]["derived"]["remaining_by_directory"]
        self.assertEqual(q32["my/chengren"],1)
        self.assertEqual(q32["my/zhuansheng"],4)
        self.assertNotIn("2000", self.orig["map09"]["maps"])
        self.assertFalse(self.result["map_reachability_boundary"]["map09_source_qualified_pixel_atlas_for_this_floor"])
        self.assertTrue(self.result["map_reachability_boundary"]["no_claim_DAT_absent_from_preserved_archives_or_historical_game"])

    def test_no_unsupported_historical_promotion(self):
        d = self.result["limits"]
        for name in ("file_paths_do_not_prove_original_historical_quest_name_or_purpose",
                     "original_lv_thresholds_not_recovered_from_public_index",
                     "original_conditions_not_evaluated",
                     "EndSetFlg_not_proven_to_update_runtime_state",
                     "original_adulthood_or_rebirth_mechanic_not_proven"):
            self.assertTrue(d[name])
        for name in ("original_same_build_early_official_deployment_proven",
                     "map2000_original_pixel_scene_proven",
                     "original_asset_pixels_newly_rendered",
                     "original_original_commercial_client_or_server_run",
                     "original_proprietary_dialogue_or_raw_code_published"):
            self.assertFalse(d[name])
        self.assertEqual(self.result["summary"]["new_original_source_files_read"], 0)
        self.assertEqual(d["stage_A"],"7_PARTIAL_2_OPEN")
        self.assertEqual(d["stage_B_wiki"],"GATED")
        self.assertIsNone(d["overall_percent"])

if __name__ == "__main__":
    unittest.main()
