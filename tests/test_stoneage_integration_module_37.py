"""Recheck INTEGRATION37 against exact earlier public source-ledger blobs."""
import copy
import hashlib
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-INTEGRATION37-GOA-ULI-LETTERS-MAP-SPR-SCRIPT-SOURCE-R1.json"
def gitblob(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
class Integration37(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads(REPORT.read_text(encoding="utf-8"))
        cls.sources={}
        for name,pin in cls.report["upstream"].items():
            raw=(ROOT/pin["path"]).read_bytes()
            assert gitblob(raw)==pin["git_blob"], name
            cls.sources[name]=json.loads(raw)
    def test_historical_current_prefix_preserved(self):
        data=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(self.report["preserved_full_CURRENT_bytes"],2709173)
        self.assertEqual(gitblob(data[:2709173]),self.report["preserved_full_CURRENT_git_blob"])
    def test_same_preserved_carrier_not_same_official_deployment(self):
        q=self.sources["quest13"];c=self.sources["char05"]
        self.assertEqual(q["original_parent_RAR_sha256"],c["original_RAR_sha256"])
        self.assertEqual(q["source_archive_sha256"],c["original_NPC_ZIP_sha256"])
        self.assertEqual(self.report["same_preserved_parent_RAR_sha256"],q["original_parent_RAR_sha256"])
        self.assertEqual(self.report["same_preserved_original_NPC_zip_sha256"],q["source_archive_sha256"])
        self.assertFalse(self.report["boundaries"]["same_official_client_server_deployment_verified"])
    def test_ten_source_npcs_exact_original_paths_and_spr(self):
        q=self.sources["quest13"];c=self.sources["char05"]
        rows=self.report["original_npc_map_motion_script_crosswalk"]
        self.assertEqual(len(rows),10)
        self.assertEqual([x["create_ordinal"] for x in rows],list(range(10)))
        self.assertEqual(sorted([x["source_graphic_alias"] for x in rows]),[100250]*5+[100252]*5)
        for r in rows:
            z=next(x for x in q["original_create_rows"] if x["path"]==r["original_create_path"] and x["ordinal"]==r["create_ordinal"])
            m=[x for x in c["config_with_existing_real_art"] if x["source_create_path"]==z["path"] and x["source_create_ordinal"]==z["ordinal"]]
            self.assertEqual(len(m),1)
            self.assertEqual((r["source_floor_id"],r["source_xy"],r["source_create_block_sha256"],r["source_graphic_alias"]), (z["floor"],z["xy"],z["original_block_sha256"],z["graphic_alias"]))
            self.assertEqual((r["qualified_same_parent_SPR_segment_sha256"],r["qualified_same_parent_SPR_index"]),(m[0]["source_original_SPR_segment_sha256"],m[0]["source_SPR_group_index"]))
            self.assertEqual(r["source_script_sha256"],z["source_script_sha256"])
            self.assertFalse(r["original_native_render_or_interaction_verified"])
    def test_six_real_map_byte_pins_and_source_point_values(self):
        maps={x["floor"]:x for x in self.sources["quest13"]["original_map_source_observations"]}
        self.assertEqual(set(maps),set(x["floor"] for x in self.report["source_maps"]))
        for m in self.report["source_maps"]:
            z=maps[m["floor"]]
            self.assertEqual((m["source_DAT_sha256"],m["source_DAT_bytes"],m["source_geometry"],m["source_CREATE_count"]),(z["source_DAT_SHA256"],z["original_DAT_bytes"],z["geometry"],len(z["source_points"])))
        for row in self.report["original_npc_map_motion_script_crosswalk"]:
            z=maps[row["source_floor_id"]]
            p=next(v for v in z["source_points"] if v["create_ordinal"]==row["create_ordinal"])
            self.assertEqual(row["source_map_DAT_sha256"],z["source_DAT_SHA256"])
            self.assertEqual(row["source_map_original_three_u16"],p["source_three_u16_values"])
    def test_ten_script_paths_sixteen_previously_indexed_sections(self):
        scripts={x["path"]:x for x in self.sources["quest13"]["scripts"]}
        self.assertEqual(set(scripts),set(x["script_path"] for x in self.report["source_scripts"]))
        self.assertEqual(sum(len(v["source_event_blocks"]) for v in self.report["source_scripts"]),16)
        for v in self.report["source_scripts"]:
            orig=scripts[v["script_path"]]
            self.assertEqual(v["source_script_sha256"],orig["sha256"])
            self.assertEqual([(e["ordinal"],e["event_no"],e["type"],e["source_block_sha256"],e["source_command_names"]) for e in v["source_event_blocks"]],[(e["ordinal"],e["event_number"],e["type"],e["source_block_sha256"],[c["key"] for c in e["commands"]]) for e in orig["events"]])
        for row in self.report["original_npc_map_motion_script_crosswalk"]:
            self.assertEqual(row["source_event_block_count"],len(scripts[row["source_script_path"]]["events"]))
    def test_five_item_ids_exact_original_row_sha(self):
        src={v["item_id"]:v for v in self.sources["quest13"]["item_source_evidence"]}
        self.assertEqual(set(src),set(v["item_id"] for v in self.report["source_items"]))
        self.assertEqual(set(src),{1206,2414,2424,2425,2426})
        for row in self.report["source_items"]:
            z=src[row["item_id"]]
            self.assertEqual(len(z["original_rows"]),2)
            self.assertEqual(z["original_rows"][0]["original_line_without_newline_sha256"],z["original_rows"][1]["original_line_without_newline_sha256"])
            self.assertEqual(row["source_original_itemset_line_sha256"],z["original_rows"][0]["original_line_without_newline_sha256"])
            self.assertEqual(row["original_image_alias"],z["original_image_alias"])
    def test_no_invented_new_raw_or_runtime_status(self):
        c=self.report["count"];self.assertEqual(tuple(c[x] for x in ("source_npc_create_placements","source_floors","source_scripts","already_indexed_original_event_blocks","reused_original_full_SPR_groups","source_original_item_ids","new_original_script_bytes_or_images_acquired_this_work","new_original_runtime_observations")),(10,6,10,16,2,5,0,0))
        self.assertTrue(all(v is False for k,v in self.report["boundaries"].items() if k!="overall_percent"))
        self.assertIsNone(self.report["boundaries"]["overall_percent"])
if __name__=="__main__": unittest.main()
