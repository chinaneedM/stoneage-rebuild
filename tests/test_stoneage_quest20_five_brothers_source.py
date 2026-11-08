"""QUEST20 source-only five-brothers dungeon joins; never downloads original commercial bytes."""
from collections import Counter
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
def j(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

class Quest20PublicSourceAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=j("research/recovered/STONEAGE-QUEST20-FIVE-BROTHERS-MODULE-REVIEW-R1.json")
        cls.q=j("research/recovered/STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json")
        cls.maps=j("research/recovered/STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json")["maps"]
        cls.world=j("research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-21-GETPET-QUEST-BRANCHES-R1.json")
        cls.items={row[0]:row for i in range(1,8) for row in j(f"research/recovered/item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{i:02d}-R1.json")["rows"]}
    def test_01_source_create_30_and_original_script_sha_crc(self):
        r=self.r
        c=[x for x in self.q["source_creation_references"] if x["create_source_path"]==r["original_source_create"]["path"]]
        self.assertEqual(len(c),30)
        self.assertEqual({x["create_source_sha"] for x in c},{r["original_source_create"]["sha256"]})
        self.assertEqual({x["origin_class"] for x in c},{"UNRESOLVED"})
        lookup={x["path"]:x for x in self.q["source_scripts"]}
        scripts={x["path"]:x for x in r["original_scripts"]}
        self.assertEqual(len(scripts),30)
        self.assertEqual(set(scripts),{x["original_script_path"] for x in c})
        for p,row in scripts.items():
            original=lookup[p]
            self.assertEqual((row["bytes"],row["sha256"],row["crc32"],row["type_counts"]),(original["original_size"],original["original_sha256"],original["original_crc32"],original["actual_block_type_counts"]))
        orig=sorted(c,key=lambda x:x["create_brace_ordinal"])
        for a,b in zip(r["source_create_positions"],orig):
            self.assertEqual((a["ordinal"],a["script"],a["floor"],a["npc_graphic_alias"]),(b["create_brace_ordinal"],b["original_script_path"],b["floorid"],b["graphic_alias_numeric"]))
    def test_02_eighty_five_preindexed_sections_commands(self):
        r=self.r
        allowed={x["path"] for x in r["original_scripts"]}
        blocks=[x for x in self.q["source_event_blocks"] if x["script_path"] in allowed]
        self.assertEqual(len(blocks),85)
        self.assertEqual(sum(x["event_blocks"] for x in r["original_scripts"]),85)
        counts=Counter()
        for x in blocks:
            self.assertEqual(len(x["source_section_decoded_cp950_normalized_UTF8_sha256"]),64)
            for key in ("GetItem","DelItem","GetPet","EndSetFlg"):
                counts[key]+=x["source_operations"].get(key,0)
        self.assertEqual(dict(counts),r["source_command_totals"])
        self.assertEqual((counts["GetItem"],counts["DelItem"],counts["GetPet"],counts["EndSetFlg"]),(75,52,5,6))
        self.assertTrue(r["uncertainties"]["source_events_already_QUEST01_indexed"])
    def test_03_23_choice_positions_and_terminal_required_five(self):
        r=self.r
        rows=r["source_choice_NPCs"]
        self.assertEqual(len(rows),23)
        self.assertEqual(len({x["source_script"] for x in rows}),23)
        stages=r["five_original_choice_layers"]
        self.assertEqual([x["end"]-x["start"]+1 for x in stages],[5,3,5,5,5])
        self.assertEqual([x["needed"] for x in stages],r["end_exchange"]["required_IDs"])
        blocks=self.q["source_event_blocks"]
        for stage in stages:
            sub=[x for x in rows if x["floor"]==stage["floor"]]
            self.assertEqual(len(sub),stage["end"]-stage["start"]+1)
            self.assertEqual([(x["GetItem_ID"],x["source_script"]) for x in sub if x["terminal_required"]],[(stage["needed"],f"giiru/event/ev28_{stage['correct']}")])
            self.assertTrue(all(x["GetItem_ID"]==stage["other"] for x in sub if not x["terminal_required"]))
        for row in rows:
            bs=[x for x in blocks if x["script_path"]==row["source_script"]]
            self.assertEqual(len(bs),3)
            self.assertEqual({id for b in bs for id in b["item_numeric_refs"].get("GetItem",[])},{row["GetItem_ID"]})
            self.assertEqual(sum(b["source_operations"].get("GetItem",0) for b in bs),row["GetItem_source_lines"])
            self.assertEqual(sum(b["source_operations"].get("DelItem",0) for b in bs),row["DelItem_source_lines"])
        self.assertEqual(r["end_exchange"]["GetItem_ID"],2517)
        self.assertEqual(r["end_exchange"]["EndSetFlg"],28)
    def test_04_30_spawns_inside_six_original_qualified_map_sizes(self):
        r=self.r
        floors={x["floor"]:x for x in r["six_original_map_geometries"]}
        self.assertEqual(sorted(floors),[31701,31702,31703,31704,31705,31706])
        self.assertEqual([floors[f]["original_NPC_count"] for f in sorted(floors)],[6,3,5,5,6,5])
        for floor,v in floors.items():
            self.assertEqual(v["geometry"],self.maps[str(floor)]["geometry"])
            self.assertEqual(v["DAT_sha256"],self.maps[str(floor)]["source_sha256"])
        for a in r["source_create_positions"]:
            w,h=floors[a["floor"]]["geometry"];x,y=a["xy"]
            self.assertTrue(0<=x<w and 0<=y<h)
        self.assertFalse(r["uncertainties"]["actual_game_dungeon_entered"])
    def test_05_old_world21_getpet_instance_template_alias_join(self):
        r=self.r
        w={x["getpet_integer"]:x for x in self.world["original_enemy_instance_to_template_lookups"]}
        a={x["script"]:x for x in r["source_create_positions"]}
        self.assertEqual([x["GetPet_enemy_instance"] for x in r["reward_five_NPCs"]],[54,57,55,56,481])
        self.assertEqual([x["linked_enemy_template"] for x in r["reward_five_NPCs"]],[91,94,92,93,95])
        for x in r["reward_five_NPCs"]:
            row=w[x["GetPet_enemy_instance"]]
            self.assertEqual(x["linked_enemy_template"],row["template_id_via_enemy_field4"])
            self.assertEqual(x["source_npc_graphic_alias"],a[x["script"]]["npc_graphic_alias"])
            self.assertEqual(x["source_enemy_template_graphic_alias"],row["original_template_graphic_id"])
            self.assertEqual(x["source_npc_graphic_alias"],row["original_template_graphic_id"])
            self.assertEqual(x["enemy_master_row_sha256"],row["enemy_master_line_sha256"])
            self.assertEqual(x["template_master_row_sha256"],row["template_master_line_sha256"])
        self.assertTrue(r["previous_indices"]["pet_reward_directives_and_enemy_masters_newly_discovered"] is False)
    def test_06_all_16_original_item_rows_both_tables_ten_same_icon(self):
        r=self.r
        rows=r["source_item_rows"]
        self.assertEqual({x["ID"] for x in rows},set(range(2507,2521))|{2525,2526})
        self.assertEqual(len(rows),16)
        self.assertEqual(len({x["cross_carrier_TW1_bitmap_alias"] for x in rows}),7)
        self.assertEqual({x["cross_carrier_TW1_bitmap_alias"] for x in rows if 2507<=x["ID"]<=2516},{24222})
        for x in rows:
            old=self.items[x["ID"]]
            self.assertEqual(old[1],old[2])
            self.assertEqual(x["original_two_94_column_rows_same_SHA256"],old[1])
            self.assertEqual(x["cross_carrier_TW1_bitmap_alias"],old[4])
            self.assertEqual(x["qualification"],"REAL_RD_DECODED_CROSS_CARRIER")
        self.assertTrue(r["uncertainties"]["source_item_image_same_does_not_mean_same_item"])
    def test_07_original_short_command_sections_not_silently_patched(self):
        r=self.r;ss={x["script"]:x for x in r["original_command_exceptions"]}
        self.assertEqual(set(ss),{"giiru/event/ev28_21","giiru/event/ev28_23"})
        self.assertEqual(ss["giiru/event/ev28_21"]["GetItem_literal_lines"],2)
        self.assertEqual(ss["giiru/event/ev28_23"]["DelItem_literal_lines"],1)
        self.assertTrue(all(x["do_not_infer_missing_line"] for x in ss.values()))
        self.assertFalse(r["verified_private_carriers"]["original_361MB_RAR_rehashed_this_unit"])
        self.assertFalse(r["verified_private_carriers"]["original_private_bytes_published"])
        self.assertFalse(r["uncertainties"]["original_same_build_TW1_official_server_scripts"])
        self.assertEqual(r["stage_A"],"7_PARTIAL_2_OPEN")
        self.assertIsNone(r["overall_percent"])
    def test_08_specialty_portfolio_is_not_historical_completion(self):
        r=self.r["portfolio_dedup"]
        self.assertEqual((len(self.q["source_creation_references"]),len(self.q["source_scripts"]),len(self.q["source_event_blocks"])),(315,295,1349))
        self.assertEqual((r["QUEST08_19_specialty_distinct_script_paths"],r["QUEST08_19_QUEST01_indexed_scripts"],r["QUEST08_19_QUEST01_blocks_belonging_to_78_scripts"],r["QUEST01_scripts_without_QUEST08_19_specialty_analysis"]),(80,78,403,217))
        self.assertEqual(r["QUEST08_19_unindexed_preserved_variants"],["giiru/event/event30_5","giiru/event/event30_5.old"])
        self.assertTrue(r["these_are_not_new_scripts_or_percentage_of_game_complete"])

if __name__=="__main__":unittest.main()
