"""Bounded source-and-privacy regression for StoneAge INTEGRATION70."""
import copy
import json
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
SOURCE=ROOT/"research/recovered/STONEAGE-INTEGRATION70-HARU-EVENT15-TWO-STAGE-NPC-EIGHT-ITEM-TW1-PIXEL-SOURCE-R1.json"
CHAR=ROOT/"research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json"
QUEST=ROOT/"research/recovered/STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json"
ITEM=ROOT/"research/recovered/item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-01-R1.json"
MAP=ROOT/"research/recovered/STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json"

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

def validate(x):
    assert x["schema"]=="stoneage.integration70.haru_event15_two_stage_npc_item_pixel_static_bridge.r1"
    assert x["original_remote_baseline"]["current_blob"]=="c89e0e33537990aa2132b47c40fef49a985a935c"
    assert x["original_remote_baseline"]["current_modified"] is False
    assert [(a["floor"],a["graphic_alias"],a["linked_script"]) for a in x["create_rows"]]==[(11006,16024,"sainasu/event/event15_1"),(11006,16046,"sainasu/event/event15_2")]
    a,b=x["original_stage_15"],x["original_stage_16"]
    assert (a["exact_condition"],a["exact_DelPet"],a["exact_GetRandItem"],a["exact_EndSetFlg"])==("NOWEV=15&PET>14-74","PET>14-74*1","1350,1351,1352,1354,700,1455,1102,1122","15")
    assert (b["exact_condition"],b["exact_DelPet"],b["exact_GetPet"],b["exact_EndSetFlg"])==("ENDEV=15&NOWEV=16&PET>29-191","PET>29-191*1","95","16")
    assert x["script_blocks_prior_index"]==["ACCEPT","ACCEPT","REQUEST","REQUEST","MESSAGE","MESSAGE","MESSAGE","MESSAGE"]
    p=x["source_item_candidates"]
    assert [v["item_id"] for v in p]==[1350,1351,1352,1354,700,1455,1102,1122]
    assert [v["mixed25_itemset_image_alias"] for v in p]==[22010,22008,22016,22001,20503,22013,21039,21034]
    assert [v["retail_TW1_ADRN_physical_bitmapno"] for v in p]==[6477,6475,6483,6468,6235,6480,6340,6335]
    assert all(v["original_two_itemset_rows_identical"] and v["real_PNG_bytes_and_RGBA_rechecked"] for v in p)
    assert all(len(v[k])==64 for v in p for k in ("both_original_itemset_94_field_row_sha256","previously_qualified_original_TW1_RD_sha256","preserved_candidate_png_sha256","rechecked_candidate_RGBA_sha256"))
    assert all(v is False for v in x["negative_proofs"].values())
    assert x["new_evidence_count"]["new_original_TW1_RD_binary_decoded"]==0
    assert x["new_evidence_count"]["new_original_scripts_discovered"]==0
    assert x["provenance"]["private_zip_independently_retrieved_full_sha256_match"] is True
    assert (x["provenance"]["private_zip_members"],x["provenance"]["private_zip_members_crc_verified"])==(12,12)
    assert x["status"]["stage_A"]=={"PARTIAL":7,"OPEN":2} and x["status"]["overall_percent"] is None

class TestIntegration70(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=load(SOURCE)

    def test_source_contract(self):
        validate(self.data)

    def test_native_or_same_deployment_promotion_is_rejected(self):
        a=copy.deepcopy(self.data); a["negative_proofs"]["same_official_early_deployment_verified"]=True
        with self.assertRaises(AssertionError): validate(a)

    def test_pet_literal_order_is_conserved(self):
        a=copy.deepcopy(self.data); a["original_stage_15"]["exact_GetRandItem"]="1350,1351"
        with self.assertRaises(AssertionError): validate(a)

    def test_wrong_adrn_namespace_is_rejected(self):
        a=copy.deepcopy(self.data); a["source_item_candidates"][0]["retail_TW1_ADRN_physical_bitmapno"]=22010
        with self.assertRaises(AssertionError): validate(a)

    def test_fake_new_rd_decode_is_rejected(self):
        a=copy.deepcopy(self.data); a["new_evidence_count"]["new_original_TW1_RD_binary_decoded"]=8
        with self.assertRaises(AssertionError): validate(a)

    def test_private_custody_must_be_verified(self):
        a=copy.deepcopy(self.data); a["provenance"]["private_zip_members_crc_verified"]=11
        with self.assertRaises(AssertionError): validate(a)

    def test_existing_full_original_index_crosschecks(self):
        char=load(CHAR);quest=load(QUEST);item=load(ITEM);m=load(MAP)
        for a in self.data["create_rows"]:
            orig=next(y for y in char["create_rows"] if y[0]=="sainasu/event/event15.create" and y[1]==a["ordinal"])
            self.assertEqual((orig[4],orig[5],orig[6],orig[7]),(a["source_sha256"],a["floor"],a["graphic_alias"],a["borncorner"]))
            self.assertEqual(orig[15][0][0],a["linked_script"])
        for a in self.data["source_files"][1:]:
            orig=next(y for y in quest["source_scripts"] if y["path"]==a["path"])
            self.assertEqual((orig["original_sha256"],orig["original_size"]), (a["sha256"],a["bytes"]))
        for row in self.data["source_item_candidates"]:
            orig=next(a for a in item["rows"] if a[0]==row["item_id"])
            self.assertEqual((orig[1],orig[2],orig[3]), (row["both_original_itemset_94_field_row_sha256"],row["both_original_itemset_94_field_row_sha256"],row["mixed25_itemset_image_alias"]))
        self.assertEqual(m["maps"]["11006"]["source_sha256"],self.data["actual_preserved_MAP09_DAT_11006"]["source_sha256"])

if __name__=="__main__":
    unittest.main()
