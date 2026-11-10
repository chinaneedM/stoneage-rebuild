"""INTEGRATION40: replay source-bound published metadata only; raw assets remain private."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/recovered/STONEAGE-INTEGRATION40-FOUR-CAVE-FLAG-BYPASS-FLOOR2000-SOURCE-R1.json"

def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

class Integration40(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(REPORT.read_text(encoding="utf-8"))
        cls.up = {}
        for name, pin in cls.r["upstream_indexes"].items():
            raw = (ROOT / pin["path"]).read_bytes()
            assert git_blob(raw) == pin["git_blob"], name
            cls.up[name] = json.loads(raw)

    def test_history_prefix_preserved(self):
        x = self.r["remote_start"]
        raw = (ROOT/"docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(x["original_CURRENT_bytes"],2709173)
        self.assertEqual(git_blob(raw[:2709173]), x["original_CURRENT_blob"])

    def test_real_source_file_sha_and_previous_i39_create_map(self):
        old = {x["path"]:x for x in self.up["quest01"]["source_scripts"]}
        files = {x[0]:x for x in self.up["char01"]["source_files"]}
        previous = {x["arg_path"]:x for x in self.up["i39"]["selected_five_original_CREATE_to_script_refs"]}
        rows = self.r["original_same_archive_exact_flag_setter_pairs"]
        self.assertEqual([x["flag"] for x in rows],[4,39,40,42,46])
        for x in rows:
            short = x["shortcut"]
            other = x["different_source_flag_setter"]
            s0 = old[short["original_arg_path"]]
            s1 = old[other["path"]]
            self.assertEqual([short["original_bytes"],short["original_sha256"],short["original_crc32"]],
                             [s0["original_size"],s0["original_sha256"],s0["original_crc32"]])
            self.assertEqual([other["original_bytes"],other["original_sha256"],other["original_crc32"]],
                             [s1["original_size"],s1["original_sha256"],s1["original_crc32"]])
            for path, digest in ((short["original_arg_path"],short["original_sha256"]),(other["path"],other["original_sha256"])):
                self.assertEqual(files[path][2],digest)
            prev = previous[short["original_arg_path"]]
            self.assertEqual([short["floor"],short["xy"],short["graphic"],short["source_CREATE_ordinal"]],
                             [prev["floor"],prev["original_borncenter_xy"],prev["original_graphic_alias"],prev["create_ordinal"]])
            self.assertEqual(short["direct_raw_Has_GetItem_or_DelItem"],False)

    def test_replay_two_flag_setter_source_segments(self):
        rows=self.r["original_same_archive_exact_flag_setter_pairs"]
        q=self.up["quest01"]
        for x in rows:
            other=x["different_source_flag_setter"]
            matches=[b for b in q["source_event_blocks"] if b["script_path"]==other["path"] and b["script_block_ordinal"]==other["source_ENDSET_block_ordinal"]]
            self.assertEqual(len(matches),1)
            b=matches[0]
            self.assertEqual(b["end_set_flags"],[x["flag"]])
            self.assertEqual(b["raw_type"],"ACCEPT")
            self.assertEqual(b["source_section_decoded_cp950_normalized_UTF8_sha256"],other["source_ENDSET_block_sha256"])
            self.assertEqual(b["item_numeric_refs"]["DelItem"],other["literal_DelItem_IDs"])
            self.assertEqual(b["item_numeric_refs"]["GetItem"],other["literal_GetItem_IDs"])
            refs=[r for r in q["source_creation_references"] if r["original_script_path"]==other["path"]]
            self.assertIn((other["original_CREATE_path"],other["original_CREATE_ordinal"]),
                          [(r["create_source_path"],r["create_brace_ordinal"]) for r in refs])
        self.assertEqual([r["shortcut"]["direct_raw_EVENT_predicate_verified"] for r in rows],
                         ["LV>29"]+["LV>139"]*4)
        self.assertEqual([r["shortcut"]["direct_raw_Charm_literal"] for r in rows],[None,"1","1","1","1"])

    def test_whole_floor_remains_excluded_and_original_DAT_pinned(self):
        d=self.r["original_preserved_map2000_DAT"]
        m=self.up["map04"]
        g=self.up["map09_gap"]["excluded_maps"]["2000.dat"]
        exact=[x for x in m["per_floor_source_rows"] if x[0]=="2000.dat"]
        self.assertEqual(len(exact),1)
        self.assertEqual(exact[0],d["prior_map04_exact_row"])
        self.assertEqual(d["source_sha256"],exact[0][2])
        self.assertEqual(d["geometry"],[150,150])
        self.assertEqual(g["source_sha256"],d["source_sha256"])
        self.assertEqual(g["unqualified_gt99_alias_occurrences"],d["whole_floor_existing_unmatched_gt99_aliases"])
        self.assertEqual(g["unqualified_gt99_occurrences"],14)
        self.assertFalse(d["existing_map09_full_atlas_qualifying"])

    def test_six_original_cells_and_qualified_candidate_RD_sources(self):
        d=self.r["original_preserved_map2000_DAT"]
        pixels={row[0]:row for row in self.up["map04"]["source_TW1_real_RD_rows"]}
        rows=d["private_newly_queried_original_ground_at_six_NPC_cells"]
        self.assertEqual([x["original_DAT_xy"] for x in rows],[[54,50],[47,58],[48,58],[49,58],[50,58],[51,58]])
        self.assertEqual([x["original_DAT_three_planes_u16"] for x in rows],
                         [[6002,0,49152],[6022,0,49152],[6001,0,49152],[6006,0,49152],[6005,0,49152],[6006,0,49152]])
        for x in rows:
            p=pixels[x["original_floor_ground_alias"]]
            self.assertEqual(p[5],x["crosscarrier_original_TW1_RD_sha256"])
            self.assertEqual(p[6],x["crosscarrier_TW1_indexed_pixels_sha256"])
            self.assertEqual([p[2],p[3]],x["png_candidate_size"])
            self.assertEqual(len(x["crosscarrier_source_Palet1_candidate_PNG_sha256"]),64)

    def test_local_region_not_entire_floor_is_qualified(self):
        d=self.r["original_preserved_map2000_DAT"]
        windows=d["local_window_TW1_crosscarrier_original_RD_pixel_source_qualification"]
        six=windows["six_point_region18x19"]
        full=windows["whole_floor"]
        self.assertEqual([six["rect"],six["cells"],six["gt99_total"],six["gt99_qualified_TW1_pixel_occurrences"],six["positive_1_to_99_not_render_qualified_occurrences"]],
                         [[42,44,59,62],342,353,353,60])
        self.assertEqual(full["gt99_total"]-full["gt99_qualified_TW1_pixel_occurrences"],14)
        self.assertEqual(full["gt99_missing_occurrences"],14)
        self.assertGreater(full["positive_1_to_99_occurrences"],0)

    def test_negative_historical_and_private_evidence_guards(self):
        x=self.r["negative_limits"]
        for k in ("proven_official_original_early_release_task_or_mechanic",
                  "actual_original_player_adulthood_or_rebirth_executed",
                  "native_EndSetFlg_state_effect_verified",
                  "native_battle_pet_or_player_reset_verified",
                  "original_TW1_with_mixed25_DAT_same_server_deployment",
                  "full_floor2000_original_pixel_qualified",
                  "full_map2000_native_renderer_collision_or_game_world_entered",
                  "full_original_NPC_dialogues_or_original_MAP_DAT_or_sprites_published",
                  "new_original_static_script_files_discovered"):
            self.assertFalse(x[k])
        self.assertEqual(x["stage_A"],"7_PARTIAL_2_OPEN")
        self.assertEqual(x["stage_B_wiki"],"GATED")
        self.assertEqual(x["R79"],"PAUSED_NON_BLOCKING")
        self.assertIsNone(x["overall_percent"])

if __name__ == "__main__":
    unittest.main()
