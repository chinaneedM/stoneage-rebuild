"""INTEGRATION63: derived-only water-vessel item-ID and archival script-edge source acceptance."""
import json
import unittest
from collections import Counter
from pathlib import Path
P = Path(__file__).resolve().parents[1]/"research"/"recovered"
REPORT=P/"STONEAGE-INTEGRATION63-BANUM-11-VESSEL-STATES-16-SOURCE-EDGES-R1.json"
Q18=P/"STONEAGE-QUEST18-GIIRU-SINK-SOURCE-R1.json"
ITEM=P/"item-module-01"/"STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json"

class TestWaterVesselOriginalSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(REPORT.read_text(encoding="utf-8"))
        cls.q=json.loads(Q18.read_text(encoding="utf-8"))
        cls.rows={a[0]:a for a in json.loads(ITEM.read_text(encoding="utf-8"))["rows"]}
    def test_original_shop_and_all_eleven_distinct_items_in_two_rows(self):
        r=self.r
        self.assertEqual([x["item_id"] for x in r["original_eleven_source_item_rows"]],list(range(2708,2719)))
        self.assertEqual([x["item_id"] for x in r["original_eleven_source_item_rows"]],[i for i in self.q["item_result"]["source_ids"] if 2708<=i<=2718])
        for x in r["original_eleven_source_item_rows"]:
            a=self.rows[x["item_id"]]
            self.assertEqual(a[1],a[2])
            self.assertEqual(a[1],x["original_A_B_identical_row_sha256"])
            self.assertEqual(a[3:5],[12924,12924])
            self.assertEqual(a[5:7],["500","16"])
            self.assertEqual(a[8:10],["REAL_RD_DECODED_CROSS_CARRIER"]*2)
            self.assertEqual(x["original_94_field_count"],94)
        self.assertEqual(r["original_eleven_source_item_rows"][0]["source_shop_arg_paths"],["genout/ss_30504_10_11"])
        self.assertTrue(all(not x["source_shop_arg_paths"] for x in r["original_eleven_source_item_rows"][1:]))
    def test_duplicate_visible_volume_must_not_dedupe_original_ID(self):
        x=self.r
        self.assertEqual(x["different_IDs_despite_equal_original_description_and_all_other_93_field_values"],[
            {"original_description_label":"4/7","distinct_original_IDs":[2710,2714],"only_original_field_index_differing":16},
            {"original_description_label":"3/7","distinct_original_IDs":[2711,2715],"only_original_field_index_differing":16}])
        d={z["item_id"]:z["original_description_water_quantity_label"] for z in x["original_eleven_source_item_rows"]}
        self.assertEqual([d[n] for n in range(2708,2719)],["EMPTY_CONTAINER","7/7","4/7","3/7","6/7","5/7","4/7","3/7","2/7","1/7","EMPTY_CONTENT"])
        self.assertEqual(len({z["original_A_B_identical_row_sha256"] for z in x["original_eleven_source_item_rows"]}),11)
    def test_eleven_active_original_sinks_exact_source_SHA_bytes(self):
        x=self.r
        old={q["path"]:q for q in self.q["original_script_rows"]}
        active={q["script"] for q in self.q["active_changeevent_npc_rows"]}
        self.assertEqual(len(x["source_original_17_sinks"]),17)
        self.assertEqual(len(active),11)
        self.assertEqual(sum(q["referenced_by_Q18_original_CREATE"] for q in x["source_original_17_sinks"]),11)
        for q in x["source_original_17_sinks"]:
            self.assertEqual(q["referenced_by_Q18_original_CREATE"],q["source_path"] in active)
            if q["source_path"] in active:
                oldrow=old[q["source_path"]]
                self.assertEqual(q["original_bytes"],oldrow["original_bytes"])
                self.assertEqual(q["original_sha256"],oldrow["original_sha256"])
        self.assertEqual(x["source_active_CREATE_referenced_NPC_locations"],[
            {"script":a["script"],"floor":a["floor"],"xy":a["xy"],"source_graphic_alias":a["source_graphic_alias"]} for a in self.q["active_changeevent_npc_rows"]])
    def test_full_source_edge_multiplicity_and_script_anchoring(self):
        x=self.r
        occ=x["original_single_ITEM_replace_event_occurrences"]
        self.assertEqual(len(occ),49)
        self.assertEqual(sum(next(q for q in x["source_original_17_sinks"] if q["name"]==s["script"])["referenced_by_Q18_original_CREATE"] for s in occ),35)
        self.assertEqual(len(set((e["DelItem_single_literal_ID"],e["GetItem_single_literal_ID"]) for e in occ)),16)
        pairs={(e["from"],e["to"]):e for e in x["distinct_source_directed_replacements"]}
        self.assertEqual(len(pairs),16)
        self.assertEqual(set(pairs),{(a["DelItem_single_literal_ID"],a["GetItem_single_literal_ID"]) for a in occ})
        for pair,e in pairs.items():
            matched=[z for z in occ if (z["DelItem_single_literal_ID"],z["GetItem_single_literal_ID"])==pair]
            self.assertEqual(e["original_event_occurrences"],len(matched))
            self.assertEqual(set(e["source_scripts"]),{z["script"] for z in matched})
        self.assertEqual({(a["from"],a["to"]) for a in x["distinct_source_directed_replacements"] if a["from"]==2708},
                         {(2708,2709),(2708,2710),(2708,2711)})
    def test_qualify_bulk_remove_del_only_and_external_reward_separately(self):
        q=self.r["other_original_command_classes"]
        self.assertEqual(len(q["bulk_multi_DelItem_and_GetItem_empty_vessel"]),8)
        self.assertEqual(len(q["DelItem_only_no_GetItem_in_same_sink06_event"]),7)
        self.assertEqual([z["DelItem_literal_ID"] for z in q["DelItem_only_no_GetItem_in_same_sink06_event"]],list(range(2712,2719)))
        for z in q["bulk_multi_DelItem_and_GetItem_empty_vessel"]:
            self.assertEqual(z["DelItem_original_comma_list_numbers"],list(range(2710,2719)))
            self.assertTrue(z["source_not_proven_to_delete_missing_items"])
        ext=q["related_other_item_19292_from_2717"]
        self.assertEqual([ext["TYPE"],ext["original_DelItem_literal"],ext["original_GetItem_literal"]],["MESSAGE","2717*1","19292*1"])
        self.assertIn(19292,self.q["item_result"]["source_ids"])
    def test_actual_original_art_identity_is_one_shared_candidate(self):
        art=self.r["original_separate_early_TW1_original_pixel_candidate"]
        self.assertEqual(art["original_item_graphic_alias"],12924)
        self.assertEqual(art["original_TW1_ADRN_physical_index"],5178)
        self.assertEqual(art["original_RD_candidate_dimensions"],[52,68])
        self.assertEqual(art["original_rd_sha256"],"e254384084f1c68c099968d129737963ccf73bf714ad08321dd5b22a6dc505c3")
        self.assertEqual(art["actual_PNG_sha256_private_reread"],"75bd38c165a57b1aad955c01a36a6fcade56d1223e858e23c4a8079945c01af2")
        self.assertTrue(art["original_graphic_reused_by_all_11_source_item_rows"])
        self.assertEqual(self.q["item_result"]["water_vessel_item_graphic_alias"],12924)
    def test_full_private_custody_and_no_fabricated_runtime(self):
        r=self.r
        self.assertEqual(r["private_replay"]["private_observer_zip_sha256"],"b935332ccae71ec59a863ceb0588f597696e764815cd2e6b8a83646e1c8e3a0c")
        self.assertEqual(r["private_replay"]["private_observer_zip_original_members_CRC"],43)
        self.assertTrue(r["private_replay"]["private_Library_upload_and_independent_full_byte_SHA_CRC_reread"])
        self.assertEqual(r["private_replay"]["original_RD_binary_newly_decoded"],0)
        self.assertFalse(r["method_limits"]["original_getitem_delitem_callbacks_executed"])
        self.assertFalse(r["method_limits"]["mixed25_community_npc_and_TW1_item_art_same_original_official_build"])
        self.assertFalse(r["method_limits"]["duplicate_4_7_and_3_7_states_merged"])
        self.assertIsNone(r["overall_percent"])
        self.assertEqual(r["stage_A"],"7_PARTIAL_2_OPEN")
        self.assertEqual(r["remote_baseline"]["preserved_historical_CURRENT_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")

if __name__=="__main__":
    unittest.main()
