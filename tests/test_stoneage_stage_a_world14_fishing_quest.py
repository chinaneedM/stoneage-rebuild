"""WORLD14 original source-text literal quantities and prior numeric source references."""
from pathlib import Path
import json, unittest

ROOT=Path(__file__).resolve().parents[1]/"research"/"recovered"
def read(name): return json.loads((ROOT/name).read_text(encoding="utf8"))
def nums(s): return [] if s is None else [int(token.split("*")[0]) for token in s.split(",")]

class World14FishingSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prev=read("STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-13-TWO-SCRIPT-ITEM-CHAIN-R1.json")
        cls.now=read("STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-14-ORIGINAL-FISHING-QUEST-SOURCE-REPLAY-R1.json")
    def test_all_original_blocks_relate_to_prior_source_digest(self):
        old={s["path"]:s for s in self.prev["sources"]}
        self.assertEqual(len(self.now["source_observed_branch_records"]),13)
        for row in self.now["source_observed_branch_records"]:
            src=old[row["script_path"]]["blocks"][row["ordinal"]]
            self.assertEqual(row["type"],src["type"])
            self.assertEqual(row["original_source_derived_block_sha256"],src["source_section_sha256"])
            self.assertEqual(sorted(nums(row["source_original_GetItem_literal"])),sorted(src["get_item_ids"]))
            self.assertEqual(sorted(nums(row["source_original_DelItem_literal"])),sorted(src["del_item_ids"]))
            self.assertEqual(len(row["observer_source_text_section_sha256"]),64)
        for row in self.now["original_source_paths"]:
            src=old[row["path"]]
            self.assertEqual(row["archived_script_sha256"],src["original_sha256"])
            self.assertEqual(row["source_create_maps"],[r["floorid"] for r in src["create_references"]])
            self.assertEqual(row["source_graphic_aliases"],[r["graphic_alias_numeric"] for r in src["create_references"]])
            self.assertTrue(row["src_create_center_numeric_unavailable"])
    def test_preserve_original_order_and_two_quantity(self):
        cases=self.now["source_observed_branch_records"]
        maker,delivery=cases[:9],cases[9:12]
        self.assertEqual(len({c["source_original_DelItem_literal"] for c in maker}),9)
        self.assertTrue(all(c["source_original_condition_literal"].endswith("&TIME!=0") for c in maker))
        self.assertEqual({c["source_original_GetItem_literal"] for c in maker},{"2432","2433","2434"})
        self.assertEqual([c["source_original_GetItem_literal"] for c in delivery],
                         ["2437,11872*2,11863","2436,11873,11863","2435,11874,11863"])
        self.assertEqual([c["source_original_DelItem_literal"] for c in delivery],["2434*1","2433*1","2432*1"])
        self.assertTrue(all("&TIME" not in c["source_original_condition_literal"] for c in delivery))
        self.assertTrue(all(c["raw_GetItem_order_differs_from_prior_ID_catalog"] for c in delivery))
        self.assertEqual(cases[12]["type"],"MESSAGE")
        self.assertEqual(cases[12]["source_original_condition_literal"],"LV>0&TIME!=0")
        self.assertIsNone(cases[12]["source_original_GetItem_literal"])
        self.assertEqual(self.now["correction_to_World13"]["source_literal_quantity_token"],"11872*2")
    def test_all_sixteen_items_and_thirteen_rd_candidate_aliases(self):
        ids=self.now["items_with_source_names_and_previous_original_RD_candidate"]
        self.assertEqual([r["id"] for r in ids],[r["id"] for r in self.prev["item_rows"]])
        for r,old in zip(ids,self.prev["item_rows"]):
            self.assertTrue(r["original_item_name"])
            self.assertEqual(r["itemset_source_row_sha256"],old["source_a_complete_row_sha256"])
            self.assertEqual(r["itemset_image_alias"],old["source_a_image_alias"])
            self.assertEqual(r["original_TW1_RD_status_previously_verified"],"REAL_RD_DECODED_CROSS_CARRIER")
        self.assertEqual(len({r["itemset_image_alias"] for r in ids}),13)
        self.assertEqual(len(ids),16)
    def test_private_public_boundaries(self):
        b=self.now["boundaries"]
        self.assertTrue(b["private_existing_script_text_reread"])
        self.assertFalse(any(v for k,v in b.items() if k!="private_existing_script_text_reread"))
        receipt=self.now["observation_output"]
        self.assertEqual((receipt["packaged_members"],receipt["source_branch_buttons_checked_in_real_Chromium"],
                          receipt["item_illustrations_verified_loaded_in_real_Chromium"]), (3,13,16))
        self.assertEqual((receipt["js_errors"],receipt["external_requests"]),(0,0))
        self.assertIsNone(self.now["continuity"]["overall_percent"])
        self.assertEqual(self.now["continuity"]["unchanged_history_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual((self.now["continuity"]["stage_A"],self.now["continuity"]["stage_B"],
                          self.now["continuity"]["wiki"],self.now["continuity"]["R79"]),
                         ("7_PARTIAL_2_OPEN","GATED","GATED","PAUSED_NON_BLOCKING"))

if __name__=="__main__":unittest.main()
