"""Stage A sourced, negative-guarded four-room Qikaka integration."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-INTEGRATION32-QIKAKA-FOUR-ROOMS-SOURCE-R1.json"

def git_blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+bytes([0])+raw).hexdigest()

class QikakaFourRooms(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(REPORT.read_text(encoding="utf-8"))
        cls.up={}
        for key,meta in cls.r["upstream"].items():
            raw=(ROOT/meta["path"]).read_bytes()
            assert git_blob(raw)==meta["git_blob"],key
            cls.up[key]=json.loads(raw)

    def test_continuity_and_private_zip_provenance(self):
        c=self.r["fresh_starting_remote"]
        self.assertEqual((c["main"],c["tree"]),(
            "47732f7eed74b5581941c8ced712005dbea78248",
            "e4728fee3fa66051b2f7bc8e822cd8a2e4feee4b"))
        raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
        self.assertGreaterEqual(len(raw),2709173)
        self.assertEqual(git_blob(raw[:2709173]),c["current_git_blob"])
        z=self.r["private_source_zip_verified"]
        self.assertEqual([(x["bytes"],x["members"]) for x in z],
                         [(13292099,373),(995176,2205),(5868386,838)])
        self.assertTrue(all(x["all_member_CRC_pass"] for x in z))
        self.assertEqual(z[0]["sha256"],"da1d0a15a1e5b03a7234f5ba52bbd81fafae380b5ef8ee50759676f44ccec2f8")

    def test_four_original_dat_and_ls2map_sources_not_new_map09_replay(self):
        old=self.up["i28"]["whole_3400_portal_topology"]
        maps=self.up["map09"]["maps"]
        rows=self.r["four_rooms"]
        self.assertEqual([x["floor"] for x in rows],[3404,3405,3409,3412])
        for r in rows:
            f=str(r["floor"])
            original=old["original_DATs"][f]
            s=old["original_indoor_LS2MAP_names"][f]
            m=maps[f]
            self.assertEqual((r["DAT_sha256"],r["DAT_bytes"],r["geometry"]),
                             (original["sha256"],original["bytes"],original["geometry"]))
            self.assertEqual((r["LS2MAP_sha256"],r["LS2MAP_bytes"],r["original_name"]),
                             (s["sha256"],s["bytes"],s["name"]))
            self.assertEqual((r["original_MAP09_candidate_RGBA_by_mode"],r["draw_positions"],r["distinct_source_tiles"]),
                             (m["frame_RGBA_sha256"],m["draw_positions"],m["unique_draw_aliases"]))
            self.assertFalse(r["replayed_original_map_render_in_this_work_unit"])

    def test_sixteen_explicit_original_directions_no_invention(self):
        mine=self.r["original_mapwarp"]
        old=self.up["i28"]
        expected=[x for x in old["whole_3400_portal_topology"]["directions"]
                  if x["start"][0] in (3404,3405,3409,3412)
                  or x["target"][0] in (3404,3405,3409,3412)]
        self.assertEqual(mine["original_directions"],expected)
        self.assertEqual(len(expected),16)
        self.assertEqual([x["mapwarp_line"] for x in expected],
                         [756,757,758,759,760,761,762,763,764,765,766,767,771,772,773,774])
        self.assertTrue(all(x["exact_reverse"] for x in expected))
        self.assertEqual(mine["sha256"],old["mapwarp_sha256"])
        self.assertFalse(mine["native_teleport_execution_verified"])

    def test_seven_real_shop_m2_creates_and_hospital_native_limits(self):
        rows=self.r["shop_m2_create"]["matching_source_blocks"]
        self.assertEqual(len(rows),7)
        self.assertEqual([x["ordinal"] for x in rows],[66,67,68,73,74,75,76])
        self.assertEqual([(x["floor"],x["xy"]) for x in rows],
                         [(3409,[27,26]),(3409,[27,36]),(3409,[27,16]),
                          (3404,[15,13]),(3405,[18,12]),(3405,[18,9]),(3405,[13,8])])
        self.assertEqual([x["function"] for x in rows],
                         ["npcgen_shop"]*3+["npcgen_limitshop","npcgen_winhealer","npcgen_shop","npcgen_man"])
        self.assertEqual([x["cell"] for x in rows if x["floor"]==3405],
                         [[5000,0,49152],[5000,0,49152],[5000,12802,49152]])
        self.assertEqual(self.r["hospital_other_parameters"]["nurse"]["literal_args"],["10","1.4","2.8","2"])
        self.assertFalse(self.r["hospital_other_parameters"]["nurse"]["actual_heal_price_or_execution_verified"])

    def test_shops_explicit_ids_vs_limit_range(self):
        shops=self.r["source_shop_arguments"]
        self.assertEqual([s["category"] for s in shops],
                         ["OFFENCE","DEFENCE","ACCESSORY","UNSPECIFIED_EMPTY"])
        self.assertEqual([len(s["ItemList"]) for s in shops],[16,12,6,12])
        ids=[i for s in shops for i in s["ItemList"]]
        self.assertEqual(len(ids),46)
        self.assertEqual(len(set(ids)),46)
        self.assertEqual([s["buy_rate"] for s in shops],["1.0","1.0","1.0","1.4"])
        self.assertEqual(self.r["source_meat_limitshop"]["original_literal_ItemList_IDs"],[])
        self.assertEqual(self.r["source_meat_limitshop"]["LimitItemNo_literal"],"1234-1249")
        self.assertEqual(self.r["source_meat_limitshop"]["closed_interval_definition_candidates"],16)
        self.assertFalse(self.r["source_meat_limitshop"]["native_buyback_or_stock_verified"])
        self.assertNotIn(1234,ids)

    def test_original_pet_quest_identical_predicate_not_collapsed(self):
        q=self.r["original_kikukuev"]
        self.assertEqual(q["location"],{"floor":3412,"xy":[15,15],"cell_u16":[5002,0,49152]})
        self.assertEqual(q["create"]["bytes"],341)
        parts=q["script"]["parts"]
        self.assertEqual(len(parts),4)
        self.assertEqual([x["TYPE"] for x in parts],["ACCEPT","ACCEPT","MESSAGE","REQUEST"])
        self.assertEqual(parts[0]["EVENT"],parts[1]["EVENT"])
        self.assertNotEqual(parts[0]["sha256"],parts[1]["sha256"])
        self.assertEqual(parts[0]["literal_fields"]["GetRandItem"],"2451,2452,2453,2454")
        self.assertEqual(parts[1]["literal_fields"]["GetItem"],"2455")
        self.assertEqual(parts[3]["literal_fields"]["GetItem"],"2456*1")
        self.assertEqual(parts[0]["literal_fields"]["DelPet"],"PET>14-524")
        self.assertEqual(q["exact_naming_variant"]["script_Pet_Name"],"加特力奴")
        self.assertEqual(q["exact_naming_variant"]["item2456_original_name"],"加特利奴喜愛的食物")
        self.assertFalse(q["branch_precedence_or_native_event_selection_verified"])

    def test_item_table_join_is_source_bounded_and_not_native_shop(self):
        v=self.r["item_join"]
        self.assertEqual((v["direct_shop_ItemList_occurrences"],v["meat_range_derived_candidate_count"],
                          len(v["original_quest_item_IDs"]),v["union_distinct_IDs"]),(46,16,6,68))
        self.assertEqual(v["independent_TW1_retail_original_RD_cross_carrier_candidate_IDs"],68)
        self.assertEqual(v["independent_TW1_retail_original_RD_cross_carrier_distinct_image_aliases"],63)
        self.assertTrue(v["all_68_two_original_item_row_SHA256_identical"])
        self.assertEqual(v["sorted_ID_full_original_itemset_row_sha256_manifest_digest"],
                         "14e7d057898d5a77da9b78b1d74590b2e8db082cb8b7dd821932b0b8a2aedede")
        self.assertEqual([x["id"] for x in v["quest_item_names_and_image_aliases"]],list(range(2451,2457)))
        self.assertTrue(v["meat_items_not_literal_shop_stock"])
        self.assertTrue(v["icon_candidacy_not_native_same_deployment"])

    def test_historical_boundaries_and_category_tags(self):
        b=self.r["bounds"]
        self.assertEqual(self.r["classification"]["region_or_island"],"OPEN_NOT_INFERRED")
        for k in ("native_original_client_or_server_executed","actual_item_shop_selection_or_transaction_verified",
                  "actual_healer_effect_verified","actual_pet_deduction_or_reward_verified",
                  "actual_branch_priority_verified","early_official_JSS1999_or_TW1_same_deployment_verified",
                  "original_npc_graphic_native_render_verified","private_binary_or_full_proprietary_dialogue_in_public_git"):
            self.assertFalse(b[k],k)
        self.assertEqual((b["stage_A"],b["stage_B_wiki"],b["R79"],b["overall_percent"]),
                         ("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None))

if __name__=="__main__":
    unittest.main()
