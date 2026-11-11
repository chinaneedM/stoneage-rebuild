"""INTEGRATION72 public cross-source audit: original scripts and item indices, not runtime."""
import copy
import json
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
REC=ROOT/"research/recovered"
TARGET=REC/"STONEAGE-INTEGRATION72-DREAM-SAGE-FOUR-ITEM-TW1-ORIGINAL-PIXEL-SOURCE-R1.json"
OLD_QUEST=REC/"STONEAGE-QUEST09-DREAM-CAVE-ORIGINAL-CONTROLS-R1.json"
OLD_ITEM=REC/"item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json"

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

def validate(d):
    assert d["schema"]=="stoneage.integration72.dream_sage_four_source_item_pixel_candidate_crosswalk.r1"
    assert d["fresh_remote"]["current_full_git_blob"]=="c89e0e33537990aa2132b47c40fef49a985a935c"
    assert d["fresh_remote"]["current_bytes"]==2709173
    assert d["fresh_remote"]["current_unchanged"] is True
    assert d["source_scope"]["cross_carrier_same_official_deployment_proven"] is False
    assert [x["source_create_ordinal"] for x in d["original_creates"]]==[0,1,2]
    assert [(x["floor_id"],x["graphic_alias"]) for x in d["original_creates"]]==[(41,16024),(42,16024),(6000,16001)]
    assert [x["event_number"] for x in d["original_source_quest_numeric_routes"]]==[34,33,32]
    assert all(x["elder_GetItem"]==[2603] and x["sage_DelItem"]==[2603] for x in d["original_source_quest_numeric_routes"])
    assert [x["sage_GetItem"] for x in d["original_source_quest_numeric_routes"]]==[[2604],[2605],[2606]]
    assert all(x["elder_source_type"]=="REQUEST" and x["sage_source_type"]=="ACCEPT" for x in d["original_source_quest_numeric_routes"])
    assert all(not x["actual_original_server_execution"] and not x["actual_branch_priority_proven"] for x in d["original_source_quest_numeric_routes"])
    items=d["original_source_item_and_cross_carrier_pixel_candidates"]
    assert [x["item_id"] for x in items]==[2603,2604,2605,2606]
    assert [x["source_item_image_alias"] for x in items]==[14648,21000,21531,24212]
    assert [x["original_TW1_physical_bitmap_number"] for x in items]==[5600,6301,6396,6979]
    assert [(x["width"],x["height"]) for x in items]==[(44,55),(32,46),(44,43),(48,42)]
    assert len(set(x["rechecked_retained_PNG_SHA256"] for x in items))==4
    assert all(x["source_a_full_94_field_row_sha256"]==x["source_b_full_94_field_row_sha256"] for x in items)
    assert all(x["pixel_source_existing_TW1_retail_decoded_candidate"] and not x["source_item_and_TW1_graphics_authenticated_same_official_deployment"] for x in items)
    assert all(len(x[k])==64 for x in items for k in ("original_TW1_RD_SHA256","rechecked_retained_PNG_SHA256","rechecked_retained_RGBA_SHA256"))
    assert d["independently_reread_original_source"]["retail_REAL_original_RD_new_binary_decodes"]==0
    assert d["independently_reread_original_source"]["original_NPC_scripts_newly_discovered"]==0
    assert d["private_original_custody"]["member_count"]==12
    assert d["private_original_custody"]["all_12_crc_verified"] is True
    assert d["private_original_custody"]["independent_Library_download_entire_bytes_and_sha_matched"] is True
    assert not d["private_original_custody"]["original_assets_or_dialogue_placed_in_public_git"]
    assert all(x is False for x in d["not_proven"].values())
    assert d["status"]=={"stage_A":{"PARTIAL":7,"OPEN":2},"stage_B":"GATED","wiki":"GATED","R79":"PAUSED_NON_BLOCKING","overall_percent":None}

class Integration72SourceBound(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=load(TARGET)
        cls.q=load(OLD_QUEST)
        cls.rows={x[0]:x for x in load(OLD_ITEM)["rows"]}

    def test_contract(self):
        validate(self.d)

    def test_old_original_create_and_source_sha_replay(self):
        a=self.q["source_creates"]
        sourcefiles={x["path"]:x for x in self.q["source_files"]}
        for f in self.d["original_NPC_source_files"]:
            self.assertEqual((sourcefiles[f["path"]]["sha256"],sourcefiles[f["path"]]["bytes"]),(f["sha256"],f["bytes"]))
        for x in self.d["original_creates"]:
            old=next(v for v in a if v["file"]=="seimu/event/event01.create" and v["ordinal"]==x["source_create_ordinal"])
            self.assertEqual((old["block_sha256"],old["floor"],old["graphic_alias"],old["borncorner_raw"],old["parameter_references"][0][0]),(x["original_create_block_sha256"],x["floor_id"],x["graphic_alias"],x["borncorner_raw"],x["linked_original_script"]))

    def test_original_sage_quest_sections_are_not_fabricated(self):
        scripts={x["path"]:x for x in self.q["source_event_scripts"]}
        for x in self.d["original_source_quest_numeric_routes"]:
            for s_prefix,ty,cmdfields in (
                ("elder","REQUEST",(("GetItem","elder_GetItem"),)),
                ("sage","ACCEPT",(("DelItem","sage_DelItem"),("GetItem","sage_GetItem")))):
                old=next(v for v in scripts[x["source_"+s_prefix+"_script"]]["events"] if v["event_number"]==x["event_number"])
                self.assertEqual((old["type"],old["event"],old["block_sha256"]),(ty,x[s_prefix+"_literal_condition"],x[s_prefix+"_section_SHA256"]))
                for command,field in cmdfields:
                    self.assertEqual([c["item_id"] for c in old["commands"] if c["name"]==command],x[field])
                self.assertTrue(all(c.get("explicit_quantity") is None for c in old["commands"] if c["name"] in ("GetItem","DelItem")))

    def test_old_public_94_field_item_derived_index(self):
        for x in self.d["original_source_item_and_cross_carrier_pixel_candidates"]:
            old=self.rows[x["item_id"]]
            self.assertEqual((old[1],old[2],old[3],old[4]),(x["source_a_full_94_field_row_sha256"],x["source_b_full_94_field_row_sha256"],x["source_item_image_alias"],x["source_item_image_alias"]))
            self.assertEqual(old[8:10],["REAL_RD_DECODED_CROSS_CARRIER"]*2)

    def test_older_original_quest_map_boundaries(self):
        m={x["source_floor_id"]:x for x in self.q["prior_quest05_map_qualification"]}
        self.assertEqual((m[41]["source_DAT_sha256"],m[42]["source_DAT_sha256"]),(self.d["source_qualified_maps"]["floor_41_DAT_SHA256"],self.d["source_qualified_maps"]["floor_42_DAT_SHA256"]))
        self.assertEqual(m[6000]["map_status"],self.d["source_qualified_maps"]["floor_6000_current_955_DAT_batch"])

    def test_negative_swap_two_reward_item_identifiers(self):
        changed=copy.deepcopy(self.d)
        changed["original_source_quest_numeric_routes"][0]["sage_GetItem"]=[2605]
        with self.assertRaises(AssertionError):validate(changed)

    def test_negative_invent_fifth_bitmap(self):
        changed=copy.deepcopy(self.d)
        changed["original_source_item_and_cross_carrier_pixel_candidates"].append(dict(changed["original_source_item_and_cross_carrier_pixel_candidates"][0]))
        with self.assertRaises(AssertionError):validate(changed)

    def test_negative_upgrade_native_execution(self):
        changed=copy.deepcopy(self.d)
        changed["not_proven"]["native_quest_execution"]=True
        with self.assertRaises(AssertionError):validate(changed)

    def test_negative_invent_new_raw_RD_decodes(self):
        changed=copy.deepcopy(self.d)
        changed["independently_reread_original_source"]["retail_REAL_original_RD_new_binary_decodes"]=4
        with self.assertRaises(AssertionError):validate(changed)

    def test_negative_silently_replace_original_script_floor(self):
        changed=copy.deepcopy(self.d)
        changed["original_creates"][2]["floor_id"]=41
        with self.assertRaises(AssertionError):validate(changed)

if __name__=="__main__":
    unittest.main()
