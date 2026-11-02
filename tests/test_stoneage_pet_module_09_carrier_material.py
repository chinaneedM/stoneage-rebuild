"""PET09 historical original source cross-carrier classification without copying game assets."""
import copy,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"research/recovered"
def load(name): return json.loads((ROOT/name).read_text(encoding="utf-8"))
def certify(o,p1,p8,r28,r30):
    assert o["schema"]=="stoneage.pet_module_09_multi_carrier_original_sprite_material_and_eight_prior_verified_pixels.r1"
    flags=o["source_boundaries"]
    assert all(x is False for key,x in flags.items() if key!="overall_restoration_percent")
    assert flags["overall_restoration_percent"] is None
    assert o["baseline"]["preserved_full_current_state_blob"]=="20050acf279a01555ab06a381dfcdc936bd381a6"
    assert len(o["candidate_rows"])==598
    assert len({r[0] for r in o["candidate_rows"]})==598
    prev={r[0]:r for r in p8["graphic_rows"]}
    source={r[0]:r for r in p1["graphic_registry"]}
    exact={r["spr_no"]:r for r in r28["joins"]["reference_relationships"]["CN50"]}
    bucket={k:0 for k in ("TW1_PET07_PRIVATE_PIXELS","CN50_TW85_EXACT_ORIGINAL_SPR_ONLY","TW85_R30_PRIOR_PRIVATE_PIXELS","TW85_SPR_INDEX_ONLY","NO_INDEX_FOUR_SAMPLES")}
    for key,lines,occ,category,exact_pair,frames in o["candidate_rows"]:
        prior=prev[key];candidate=source[key]
        assert lines==prior[2]==candidate[1] and occ==prior[1]
        tw,cn,t85,mixed=candidate[2:6]
        assert occ==[len(tw),len(cn),len(t85),len(mixed)]
        if tw: expected="TW1_PET07_PRIVATE_PIXELS"
        elif cn: expected="CN50_TW85_EXACT_ORIGINAL_SPR_ONLY"
        elif key==r30["sample"]["original_spr_no"]: expected="TW85_R30_PRIOR_PRIVATE_PIXELS"
        elif t85: expected="TW85_SPR_INDEX_ONLY"
        else: expected="NO_INDEX_FOUR_SAMPLES"
        assert category==expected
        if category=="NO_INDEX_FOUR_SAMPLES": assert not mixed
        bucket[category]+=1
        match=exact.get(key)
        if tw or cn: assert match is not None
        if match:
            assert match["relation"]=="SAME_ID_AND_EXACT_FULL_SPR_SEGMENT"
            assert match["reference_index"] in cn and match["tw85_index"] in t85
            assert exact_pair==[match["reference_index"],match["tw85_index"]]
        else: assert exact_pair is None
        if category=="TW85_R30_PRIOR_PRIVATE_PIXELS":
            assert len(t85)==1 and t85[0]==r30["sample"]["source_group_index"]
            assert frames==[f["bitmapno"] for f in r30["frames"]]
        else: assert frames is None
    assert [bucket[k] for k in bucket]==[130,214,1,197,56]
    assert {k:o["counts"][k] for k in bucket}==bucket
    assert o["counts"]["graph_ids_with_prior_original_source_pixel_observation"]==131
    assert o["counts"]["graph_ids_without_PET07_TW1_pixels"]==468
    assert o["counts"]["tw85_source_original_R30_frames"]==8
    assert r28["joins"]["per_reference_relationship_counts"]["CN50"]["SAME_ID_AND_EXACT_FULL_SPR_SEGMENT"]==1185
    assert r28["joins"]["per_reference_relationship_counts"]["TW10"]["SAME_ID_AND_EXACT_FULL_SPR_SEGMENT"]==464
    s=r30["sample"];t=o["prior_verified_tw85_R30_single_group"]
    assert t["original_spr_graphic_id"]==s["original_spr_no"]==101501
    assert t["original_tw85_spr_physical_group_index"]==s["source_group_index"]==1185
    assert t["original_spr_segment_sha256"]==s["source_group_full_spr_segment_sha256"]
    assert t["source_original_action"]==s["original_action_numeric"]==2
    assert t["source_original_direction"]==s["original_direction_numeric"]==0
    assert len(t["prior_private_actual_frame_source_receipts"])==len(r30["frames"])==8
    for row,f in zip(t["prior_private_actual_frame_source_receipts"],r30["frames"]):
        assert row==[f["index"],f["bitmapno"],f["width"],f["height"],f["source_record_sha256"],f["source_RD_sha256"],f["source_palette_index_sha256"],f["private_png_sha256"]]
    assert t["later_2016_community_template_source_lines"]==[843,1184]
    assert o["module_handoff"]["next_active_module"]=="CHARACTER_NPC_MODULE_01"
class PET09(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=load("STONEAGE-PET-MODULE-09-CROSSCARRIER-ORIGINAL-MATERIAL-RECEIPTS-R1.json")
        cls.p1=load("STONEAGE-PET-MODULE-01-BATCH-SOURCE-SPR-INDEX-R1.json")
        cls.p8=load("STONEAGE-PET-MODULE-08-VISUAL-STATS-SKILLS-SOURCE-CATALOG-R1.json")
        cls.r28=load("tw85-spr137-r28/SOURCE-DERIVED-R28.json")
        cls.r30=load("tw85-rd-private-r30/SOURCE-R30.json")
    def go(self,r): certify(r,self.p1,self.p8,self.r28,self.r30)
    def test_full_material_replay(self): self.go(self.r)
    def test_no_fake_tw85_pixel_rescan(self):
        r=copy.deepcopy(self.r);r["source_boundaries"]["private_8_R30_original_pixel_bytes_reloaded_in_PET09"]=True
        with self.assertRaises(AssertionError):self.go(r)
    def test_no_fake_cn50_tw85_pixel_equivalence(self):
        r=copy.deepcopy(self.r);r["source_boundaries"]["CN50_and_TW85_pixel_payloads_equivalent"]=True
        with self.assertRaises(AssertionError):self.go(r)
    def test_no_false_tw85_species(self):
        r=copy.deepcopy(self.r);r["source_boundaries"]["later_2016_names_stats_skills_are_original_TW85_source"]=True
        with self.assertRaises(AssertionError):self.go(r)
    def test_no_dropped_r30_frame(self):
        r=copy.deepcopy(self.r);r["prior_verified_tw85_R30_single_group"]["prior_private_actual_frame_source_receipts"].pop()
        with self.assertRaises(AssertionError):self.go(r)
    def test_no_crosscarrier_false_same_segment(self):
        r=copy.deepcopy(self.r);row=next(x for x in r["candidate_rows"] if x[3]=="CN50_TW85_EXACT_ORIGINAL_SPR_ONLY")
        row[4][1]+=1
        with self.assertRaises(AssertionError):self.go(r)
if __name__=="__main__":unittest.main()
