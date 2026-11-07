"""SCENE26-R3 original-only logical aliases: prohibit source version or namespace conflation."""
from copy import deepcopy
from pathlib import Path
import hashlib,json,unittest
from tools.stoneage_npc16122_alias_original_source import build
R=Path(__file__).resolve().parents[1]
P=R/"research/recovered/STONEAGE-SCENE26-R3-NPC16122-16127-ORIGINAL-ALIAS-CROSSVERSION-R1.json"
def gitblob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def verify(j,fresh,scene,char):
    assert j["schema"]=="stoneage.scene26.r3.npc16122_16127.original_alias_crossversion.r1"
    assert j["baseline_main_head"]=="ff08258e3b6fed497b70c291f3bbe400148055e7"
    assert j["CURRENT_original_blob_unchanged"]=="c89e0e33537990aa2132b47c40fef49a985a935c"
    assert j["derived_original_reference_query"]==fresh
    assert fresh["original_derived_reference_count"]==43632
    assert fresh["compressed_REFERENCES_SHA256"]=="3092102e3ee83524ccbf27414ce0cf5bc5579d9a5c8638bfa073f9e62a4db1ea"
    assert fresh["catalog_report_git_sha256"]=="e5dc7249b20a60b13fc4bf12b299d4a6f386fcb928d5d8843017ded58f9c1951"
    pins={x["path"]:x["git_blob"] for x in j["upstream"]}
    assert pins=={
      "research/recovered/STONEAGE-SCENE26-R2-FOUR-ORIGINAL-PET-TUTOR-ROOMS-SOURCE-R1.json":"3446a7006478a748d2f273c85822df84ace893a0",
      "research/recovered/STONEAGE-CHARACTER-NPC-MODULE-04-SAME-CARRIER-GRAPHIC-FUNCTION-JOIN-R1.json":"1c564b07e829bce8360f57e63d32866c03e225e3",
      "research/recovered/logical-alias-catalog-r1/REPORT-R1.json":"3a694c3e6dc2f8bef291381674c53667c9a60507"}
    for p,s in pins.items():assert gitblob((R/p).read_bytes())==s
    assert j["source_original_NPC_CREATE"]["four_pet_tutor_floors"]==[
      {"floor":x["source_floor_id"],"graphicname":x["original_source_graphicname"],
       "borncenter":x["original_borncenter"],"create_ordinal":x["source_CREATE_ordinal"],
       "original_DAT_sha256":x["original_DAT_whole_sha256"]}
      for x in scene["source_tutor_four_CREATE_rows"]]
    assert j["source_original_NPC_CREATE"]["other_original_CREATE_counts_with_source_numeric_graphics"]==[[16122,4],[16127,2]]
    assert [x for x in char["indexed_graphic_source_summary"] if x[0] in (16122,16127)]==[]
    assert j["source_original_NPC_CREATE"]["exact_16122_16127_in_source_SPR_index"] is False
    s=j["source_findings"]
    assert s=={"aliases":[16122,16127],"TW10_retained_logical_alias_count":{"16122":0,"16127":0},
      "CN50_logical_alias_count":{"16122":1,"16127":1},"PATCH129_logical_alias_count":{"16122":1,"16127":1},
      "numeric_physical_identity_not_inferred":True,"two_source_RD_sha256_identity":True,
      "original_NPC_pixels_newly_rendered":0,"new_original_client_carrier_acquired":0}
    expected={16122:(232699,1930,32,87,"70e97c406b2ac784a5b0e0cac7906ab8b044f6f4b9ebe14a92b4e727eb250022"),
              16127:(232704,2089,36,96,"c461402ebd18a9e87277c083f4b62218f99133380b74c26278ef916836aaaeb1")}
    for key,(physical,size,w,h,digest) in expected.items():
        q=fresh["sources"][str(key)]
        assert q["logical_alias_occurrences"]==2 and q["same_integer_physical_occurrences"]==0
        assert q["same_integer_physical_entries"]==[] and q["logical_alias_is_not_physical_bitmapno"] is True
        assert [x["reference"]["profile"] for x in q["logical_alias_entries"]]==["CN50","PATCH129"]
        for row in q["logical_alias_entries"]:
            a=row["reference"];b=row["content"]
            assert a["logical_alias"]==key and a["source_index"]==physical and a["physical_bitmapno"]==physical
            assert a["adrn_size"]==b["bytes"]==size and a["width"]==b["rd_width"]==w and a["height"]==b["rd_height"]==h
            assert b["rd_sha256"]==digest and row["role"]=="UNKNOWN_RESOURCE_ALIAS"
        assert q["logical_alias_entries"][0]["reference"]["source_rd_status"]=="PRIOR_ORIGINAL_BLOCK_METADATA"
        assert q["logical_alias_entries"][1]["reference"]["source_rd_status"]=="HEADER_MATCH"
    assert all(v is False for v in j["negative_boundaries"].values())
    assert all(v is True for v in fresh["not_proven"].values())
    assert j["source_job"]=={"branch_head":"0d70b1d0b9276487166a91615b6eb1226c1d91a3",
      "run_id":42383014954,"job_id":128434443556,"status":"completed","conclusion":"success"}
    assert j["status"]=={"stage_A":"7_PARTIAL_2_OPEN","stage_B_wiki":"GATED","R79":"PAUSED_NON_BLOCKING","overall_percent":None}
class TestAliasSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.j=json.loads(P.read_text())
        cls.a=build()
        cls.scene=json.loads((R/"research/recovered/STONEAGE-SCENE26-R2-FOUR-ORIGINAL-PET-TUTOR-ROOMS-SOURCE-R1.json").read_text())
        cls.char=json.loads((R/"research/recovered/STONEAGE-CHARACTER-NPC-MODULE-04-SAME-CARRIER-GRAPHIC-FUNCTION-JOIN-R1.json").read_text())
    def test_entire_source_equivalence(self):verify(self.j,self.a,self.scene,self.char)
    def reject(self,fn):
        j=deepcopy(self.j);fn(j)
        with self.assertRaises((AssertionError,KeyError)):verify(j,self.a,self.scene,self.char)
    def test_reject_early_alias_invention(self):
        self.reject(lambda j:j["source_findings"]["TW10_retained_logical_alias_count"].__setitem__("16122",1))
    def test_reject_crossversion_digest_change(self):
        self.reject(lambda j:j["derived_original_reference_query"]["sources"]["16127"]["logical_alias_entries"][1]["content"].__setitem__("rd_sha256","0"*64))
    def test_reject_bad_physical_number(self):
        self.reject(lambda j:j["derived_original_reference_query"]["sources"]["16122"]["logical_alias_entries"][0]["reference"].__setitem__("physical_bitmapno",16122))
    def test_reject_imagined_sprite(self):
        self.reject(lambda j:j["negative_boundaries"].__setitem__("source_sprite_pixels_or_anim_16122_16127_rendered",True))
    def test_reject_claimed_same_build(self):
        self.reject(lambda j:j["negative_boundaries"].__setitem__("official_same_deployment_mixed25_config_CN50_PATCH129",True))
    def test_reject_source_NPC_creation_change(self):
        self.reject(lambda j:j["source_original_NPC_CREATE"]["four_pet_tutor_floors"][0].__setitem__("floor",4002))
if __name__=="__main__":unittest.main()
