"""INTEGRATION71 is bounded original source evidence, not native game execution."""
import copy
import hashlib
import json
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
REC=ROOT/"research/recovered"
TARGET=REC/"STONEAGE-INTEGRATION71-CHAHAN-PRIEST-TIGER-WATER-ORIGINAL-SOURCE-R1.json"
CHAR=REC/"STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json"
QUEST=REC/"STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json"
ITEM02=REC/"item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json"
ITEM07=REC/"item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-07-R1.json"
MAP=REC/"STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def validate(r):
    assert r["schema"]=="stoneage.integration71.chahan_priest_item_exchange_original_source_and_TW1_pixel_candidate.r1"
    assert (r["remote_start"]["CURRENT_git_blob"],r["remote_start"]["CURRENT_bytes"],r["remote_start"]["old_history_modified"])==("c89e0e33537990aa2132b47c40fef49a985a935c",2709173,False)
    creates=r["original_NPC_creates"]
    assert [(x["ordinal"],x["floorid"],x["graphicname"],x["source_template_function"]) for x in creates]==[(0,10007,16001,"windowman"),(1,10007,16170,"changeevent"),(2,10408,16044,"windowman")]
    assert [x["direct_argument_is_tiger_water"] for x in creates]==[False,True,False]
    e=r["original_source_event_blocks"]
    assert [(x["TYPE"],x["type_line_1based"]) for x in e]==[("MESSAGE",7),("MESSAGE",14),("MESSAGE",24)]
    assert [x["EVENT_literal"] for x in e]==["LV>0&ITEM=19563","LV>0&ITEM=2452&ITEM=2440&ITEM=2441&ITEM=2442&ITEM=2400","LV>0"]
    assert [[x["token"],x["literal"],x["line_1based"]] for x in e[1]["source_commands"]]==[["DelItem","2452*1,2440*1,2400*1,2441*1,2442*1",18],["GetItem","19563*1",19]]
    assert all(hashlib.sha256(x["EVENT_literal"].encode("utf8")).hexdigest()==x["condition_UTF8_sha256"] for x in e)
    i=r["original_ITEM_two_table_rows"]
    assert [x["item_id"] for x in i]==[2452,2440,2400,2441,2442,19563]
    assert [x["original_itemset_image_alias"] for x in i]==[24103,21022,23012,20433,21545,23012]
    assert all(x["two_original_itemset_rows_SHA_equal"] is True for x in i)
    p=r["original_TW1_PREVIOUSLY_decoded_pixel_candidates"]
    assert [x["source_image_alias"] for x in p]==[20433,21022,21545,23012,24103]
    assert [x["physical_bitmapno"] for x in p]==[6215,6323,6410,6548,6756]
    assert all(x["actual_full_RD_decode_this_work_unit"] is False for x in p)
    assert all(len(x["rechecked_PNG_SHA256"])==64 and len(x["rechecked_RGBA_SHA256"])==64 for x in p)
    assert r["same_image_alias_for_distinct_items"]["distinct_original_TW1_candidate_images_for_six_items"]==5
    assert r["actual_increment"]["new_original_RD_binary_decodes"]==0
    assert r["actual_increment"]["only_ONE_create_references_exchange_script"] is True
    assert r["private_custody"]["archive_members"]==9
    assert r["private_custody"]["independently_retrieved_from_Library_and_verified_full_bytes_SHA_and_all_9_CRC"] is True
    assert r["private_custody"]["copyright_originals_in_public_git"] is False
    assert all(v is False for v in r["not_proven"].values())
    assert r["status"]=={"stage_A":{"PARTIAL":7,"OPEN":2},"stage_B":"GATED","wiki":"GATED","R79":"PAUSED_NON_BLOCKING","overall_percent":None}

class SourceBound71(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=load(TARGET)

    def test_source_contract(self):validate(self.r)

    def test_do_not_upgrade_MESSAGE_to_ACCEPT(self):
        q=copy.deepcopy(self.r);q["original_source_event_blocks"][1]["TYPE"]="ACCEPT"
        with self.assertRaises(AssertionError):validate(q)

    def test_do_not_merge_two_original_item_IDs_on_single_bitmap(self):
        q=copy.deepcopy(self.r);q["original_ITEM_two_table_rows"].pop()
        with self.assertRaises(AssertionError):validate(q)

    def test_do_not_claim_original_priest_16170_image(self):
        q=copy.deepcopy(self.r);q["not_proven"]["priest_16170_original_TW1_RD_pixel_qualified"]=True
        with self.assertRaises(AssertionError):validate(q)

    def test_do_not_invent_native_execution(self):
        q=copy.deepcopy(self.r);q["not_proven"]["native_game_ACTUAL_item_exchange_execution"]=True
        with self.assertRaises(AssertionError):validate(q)

    def test_do_not_falsely_expand_script_to_other_NPCs(self):
        q=copy.deepcopy(self.r);q["original_NPC_creates"][2]["direct_argument_is_tiger_water"]=True
        with self.assertRaises(AssertionError):validate(q)

    def test_do_not_claim_new_source_RD_decode(self):
        q=copy.deepcopy(self.r);q["actual_increment"]["new_original_RD_binary_decodes"]=5
        with self.assertRaises(AssertionError):validate(q)

    def test_old_public_source_index_replay(self):
        ch=load(CHAR);qs=load(QUEST);items={x[0]:x for p in [ITEM02,ITEM07] for x in load(p)["rows"]};maps=load(MAP)["maps"]
        for x in self.r["original_NPC_creates"]:
            orig=next(v for v in ch["create_rows"] if v[0]=="sainasu/event/event.create" and v[1]==x["ordinal"])
            self.assertEqual((orig[4],orig[5],orig[6],orig[11]),(x["original_CREATE_block_sha256"],x["floorid"],x["graphicname"],x["source_template_function"]))
            self.assertEqual(bool(orig[15]),x["direct_argument_is_tiger_water"])
        original=next(x for x in qs["source_scripts"] if x["path"]=="sainasu/event/tiger_water.arg")
        self.assertEqual((original["original_size"],original["original_sha256"],original["create_source_references"]),(799,self.r["verified_original_inputs"]["source_argument_sha256"],1))
        b=[x for x in qs["source_event_blocks"] if x["script_path"]=="sainasu/event/tiger_water.arg"]
        self.assertEqual(len(b),3)
        for actual,expected in zip(b,self.r["original_source_event_blocks"]):
            self.assertEqual((actual["script_block_ordinal"],actual["raw_type"],actual["source_type_line"],actual["condition_expression_decoded_cp950_UTF8_sha256"],actual["source_section_decoded_cp950_normalized_UTF8_sha256"]),(expected["ordinal"],expected["TYPE"],expected["type_line_1based"],expected["condition_UTF8_sha256"],expected["source_section_CP950_normalized_UTF8_sha256"]))
        for x in self.r["original_ITEM_two_table_rows"]:
            src=items[x["item_id"]]
            self.assertEqual((src[1],src[2],src[3],src[4]),(x["both_original_94_column_line_SHA256"],x["both_original_94_column_line_SHA256"],x["original_itemset_image_alias"],x["original_itemset_image_alias"]))
        for x in self.r["existing_MAP09_source_qualification"]:
            self.assertEqual((maps[str(x["floor"])]["source_sha256"],maps[str(x["floor"])]["source_bytes"],maps[str(x["floor"])]["geometry"]),(x["source_DAT_SHA256"],x["original_DAT_bytes"],x["geometry"]))

if __name__=="__main__":unittest.main()
