"""Source-qualified MAP11 room DAT layer-fingerprint regression; private DAT is not in CI."""
from collections import defaultdict
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unittest
R=Path(__file__).resolve().parents[1]
SRC=R/"research/recovered/STONEAGE-MAP07-28-ORIGINAL-DAT-SOURCE-SCENE-RECEIPT-R1.json"
OUT=R/"research/recovered/STONEAGE-MAP11-28-ORIGINAL-DAT-PLANE-FAMILIES-R1.json"
def blob(b):
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def verify(a,s,raw):
    assert a["schema"]=="stoneage.map11.original_DAT_three_plane_identical_source_groups.r1"
    assert a["baseline_main_head"]=="f720bfd502e16aa577d0921d7fdd536781357d27"
    assert a["CURRENT_original_blob_preserved"]=="c89e0e33537990aa2132b47c40fef49a985a935c"
    assert blob(raw)==a["upstream"]["git_blob"]=="f2cba278f4b5a15e50e905a1e6591958fd09dba5"
    assert a["upstream"]["private_MAP07_zip_sha256"]==s["private_deliverable"]["sha256"]
    assert a["upstream"]["private_MAP07_zip_bytes"]==s["private_deliverable"]["bytes"]==34044818
    assert a["upstream"]["private_MAP07_zip_members"]==s["private_deliverable"]["members"]==351
    assert a["upstream"]["private_original_28_DAT_and_member_CRC_reread"] is True
    assert a["original_DAT_layout"]=={"header_2_u32le":[30,30],"header_bytes":8,"u16le_per_plane":900,"original_plane_count":3,"bytes_per_plane":1800,"semantic_labels":"UNKNOWN"}
    rows=a["original_DAT_rows"]
    assert len(rows)==28 and len({x["floor"] for x in rows})==28
    old={x["floor"]:x for x in s["maps"]}
    assert set(old)=={x["floor"] for x in rows}
    actual=[defaultdict(list) for _ in range(3)]
    for row in rows:
        src=old[row["floor"]]
        assert row["original_DAT_sha256"]==src["source_dat_sha256"]
        assert row["original_DAT_bytes"]==src["source_dat_bytes"]==5408
        assert src["source_map_geometry"]==[30,30]
        assert len(row["plane_SHA256"])==len(row["plane_unique_u16_values"])==len(row["plane_nonzero_u16_cells"])==3
        for i,x in enumerate(row["plane_SHA256"]):
            assert len(x)==64 and all(c in "0123456789abcdef" for c in x)
            assert 0<=row["plane_unique_u16_values"][i]<=900
            assert 0<=row["plane_nonzero_u16_cells"][i]<=900
            actual[i][x].append(row["floor"])
        assert len(row["combined_modern_observer_RGBA_SHA256"])==64
    assert len({x["original_DAT_sha256"] for x in rows})==28
    assert [len(x) for x in actual]==[18,28,20]
    saved=a["exact_same_source_plane_classes"]
    for i in range(3):
        part=saved[str(i)]
        assert {x["plane_SHA256"]:x["floor_ids"] for x in part}==dict(actual[i])
    shared0=[x for x in saved["0"] if len(x["floor_ids"])>1]
    shared2=[x for x in saved["2"] if len(x["floor_ids"])>1]
    assert sorted(len(x["floor_ids"]) for x in shared0)==[2,2,2,3,6]
    assert sorted(len(x["floor_ids"]) for x in shared2)==[2,2,3,3,3]
    q=a["summary"]
    assert [q["source_original_DAT_distinct_full_sha"],q["source_original_plane0_distinct_sha"],q["source_original_plane1_distinct_sha"],q["source_original_plane2_distinct_sha"]]==[28,18,28,20]
    assert q["plane0_multi_floor_classes"]==5 and q["plane0_multi_floor_members"]==15
    assert q["plane2_multi_floor_classes"]==5 and q["plane2_multi_floor_members"]==13
    assert q["plane0_shared_classes_floors"]==[x["floor_ids"] for x in shared0]
    assert q["plane2_shared_classes_floors"]==[x["floor_ids"] for x in shared2]
    diffs=[d for x in shared0 for d in x["differences_from_first_floor"]]
    assert len(diffs)==q["modern_full_canvas_RGBA_different_pair_comparisons"]==10
    assert {(d["base_floor"],d["other_floor"]) for d in diffs}=={(g["floor_ids"][0],f) for g in shared0 for f in g["floor_ids"][1:]}
    for d in diffs:
        assert d["plane_u16_differing_cells"][0]==0
        assert 0<d["plane_u16_differing_cells"][1]<=900 and 0<=d["plane_u16_differing_cells"][2]<=900
        assert d["canvas_pixel_count"]==1889*1425
        assert 0<d["combined_modern_RGBA_differing_pixel_count"]<d["canvas_pixel_count"]
    assert q["modern_candidate_source_scenes_reread"]==28
    assert a["private_custody"]["source_contact_sha256"]=="4be0e4a7379d2b16966f27e44170a1ba8f2b6a52a1f49850ae38e9af400a383e"
    assert a["private_custody"]["private_full_numeric_sha256"]=="f713d1d7f14c013eab5db5b4de03358c230a62ada9b3e65bff58ac5371a57d95"
    assert a["private_custody"]["private_Library_roundtrip_exact_SHA_reverified"] is True
    assert a["non_claims"]=={"original_program_executed":False,"original_collision_layer_identified":False,"original_official_village_or_island_classification":False,"original_layer_order_and_drawer_verified":False,"original_same_deployment_DAT_and_RD":False,"new_original_DAT_files_this_unit":0,"new_original_RD_pixel_decodes_this_unit":0,"proprietary_full_DAT_or_pixels_published":False}
    assert a["stage_status"]=={"stage_A":"7_PARTIAL_2_OPEN","stage_B_wiki":"GATED","R79":"PAUSED_NON_BLOCKING","overall_percent":None}
    assert a["source_bound"]=="COMMUNITY_MIXED25_DAT_AND_EARLY_TW10_RD_PIXEL_SOURCES_NOT_VERIFIED_SAME_OFFICIAL_BUILD"
class Map11(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=SRC.read_bytes()
        cls.source=json.loads(cls.raw)
        cls.report=json.loads(OUT.read_text(encoding="utf-8"))
    def test_source_and_hash_groups(self):
        verify(self.report,self.source,self.raw)
    def bad(self,fn):
        a=deepcopy(self.report);fn(a)
        with self.assertRaises((AssertionError,KeyError)):
            verify(a,self.source,self.raw)
    def test_reject_wrong_dat_sha(self):
        self.bad(lambda a:a["original_DAT_rows"][0].__setitem__("original_DAT_sha256","0"*64))
    def test_reject_fake_shared_plane(self):
        self.bad(lambda a:a["original_DAT_rows"][0]["plane_SHA256"].__setitem__(0,"0"*64))
    def test_reject_wrong_group_member(self):
        self.bad(lambda a:a["exact_same_source_plane_classes"]["0"][0]["floor_ids"].append(9999))
    def test_reject_identical_pixels_conflation(self):
        self.bad(lambda a:a["exact_same_source_plane_classes"]["0"][0]["differences_from_first_floor"][0].__setitem__("combined_modern_RGBA_differing_pixel_count",0))
    def test_reject_collisions_inference(self):
        self.bad(lambda a:a["non_claims"].__setitem__("original_collision_layer_identified",True))
    def test_reject_official_provenance(self):
        self.bad(lambda a:a["non_claims"].__setitem__("original_official_village_or_island_classification",True))
    def test_reject_fabricated_new_DAT(self):
        self.bad(lambda a:a["non_claims"].__setitem__("new_original_DAT_files_this_unit",28))
if __name__=="__main__":
    unittest.main()
