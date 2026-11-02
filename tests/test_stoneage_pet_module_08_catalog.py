"""PET08 strict cross-source catalog conservation and negative historical attribution tests.
Public CI replays preserved derived records only: no proprietary original pixels or game runtime.
"""
import copy,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"research/recovered"
def load(name):
    return json.loads((ROOT/name).read_text(encoding="utf-8"))
REPORT="STONEAGE-PET-MODULE-08-VISUAL-STATS-SKILLS-SOURCE-CATALOG-R1.json"
def certify(out,a,b,prior,pixels):
    assert out["schema"]=="stoneage.pet_module_08_tw1_original_visual_and_2016_later_community_numeric_source_separation.r1"
    for field in ("official_TW1_species_identity_from_later_community_graphic_ids","same_deployed_TW1_and_2016_server_proven","TW1_original_pet_stats_and_skills_from_2016_server_proven","original_runtime_skill_execution_observed","original_native_pet_gameplay_entered","original_bytes_pixel_data_committed_publicly","original_TW1_pixels_redecoded_in_this_PUBLIC_metadata_replay"):
        assert out["boundaries"][field] is False,field
    assert out["boundaries"]["official_TW1_pet_species_count"] is None
    assert out["boundaries"]["overall_restoration_percent"] is None
    assert out["baseline"]["preserved_current_state_git_blob"]=="20050acf279a01555ab06a381dfcdc936bd381a6"
    assert len(out["later_2016_source_named_examples_only"])==6
    assert out["later_2016_source_named_examples_only"]==a["named_source_examples_only"]
    assert out["original_TW1_PET07_strict_RD_failures"]==pixels["source_undecodable_actual_RD_blocks"]
    assert out["original_TW1_PET07_unrenderable_source_sequences"]==pixels["source_renderable_sequences_excluded"]
    assert out["private_observation"]["sha256"]==pixels["private_artifacts"]["catalog"]["sha256"]
    assert out["private_observation"]["published_in_public_repo"] is False
    groups={x[0]:x for x in pixels["source_groups"]}
    assert len(groups)==130
    original={x[0]:x for x in a["graphic_registry"]}
    prior_rows={x[0]:x for x in prior["graphic_rows"]}
    gr=out["graphic_rows"]
    assert len(gr)==len(original)==598 and len({x[0] for x in gr})==598
    n_tw=n_late=n_none=frame=0
    for gid,counts,lines,status,source in gr:
        orig=original[gid]
        assert lines==orig[1]
        assert counts==[len(x) for x in orig[2:6]]
        assert counts==prior_rows[gid][2]
        if gid in groups:
            n_tw+=1
            assert status=="TW1_PET07_PRIVATE_SOURCE_PIXELS"
            x=groups[gid]
            assert source==[x[1],x[2],x[3],x[4],x[5],x[6]]
            frame+=source[3]
        else:
            assert source is None
            if any(counts):
                n_late+=1
                assert status=="LATER_CARRIER_SPR_INDEX_ONLY_NO_PET07_PIXELS"
            else:
                n_none+=1
                assert status=="NO_SPR_INDEX_IN_FOUR_PRESERVED_SAMPLES"
    assert (n_tw,n_late,n_none,frame)==(130,412,56,3255)
    definitions={row[1]:(row[0],row[2]) for row in b["skill_definition_rows"]}
    stats={row[0]:row for row in b["source_template_rows"]}
    old_templates={row[0]:row for row in prior["template_rows"]}
    orig_templates={row[0]:row for row in a["petflag1_template_tuples"]}
    t=out["template_rows"];assert len(t)==1024
    assert len({row[0] for row in t})==1024
    pos=resolved=missing=neg=empty=preview=0
    missing_ids=set();unique_ids=set()
    for line,tid,gid,nums,slots,instances,seen in t:
        source=orig_templates[line]
        assert (line,tid,gid)==tuple(source[:3])
        assert nums==source[3:14]
        assert instances==source[15]==old_templates[line][3]
        assert len(slots)==len(source[14])==7
        assert seen==int(gid in groups)
        preview+=seen
        unique_ids.add(tid)
        for incoming,item in zip(source[14],slots):
            if incoming is None:
                empty+=1
                assert item is None
            elif incoming < 0:
                neg+=1
                assert item==[incoming,None,None]
            else:
                pos+=1
                if incoming in definitions:
                    resolved+=1
                    assert item==[incoming,*definitions[incoming]]
                else:
                    missing+=1
                    missing_ids.add(incoming)
                    assert item==[incoming,None,None]
        ref=stats[line]
        assert (ref[1],ref[2],ref[3],ref[4],ref[5])==(tid,gid,sum(x is not None and x[0]>0 for x in slots),sum(x is not None and x[0]>0 and x[1] is not None for x in slots),sum(x is not None and x[0]>0 and x[1] is None for x in slots))
    assert (preview,pos,resolved,missing,len(missing_ids),neg,empty,len(unique_ids))==(201,2886,2784,102,30,20,4262,1021)
    c=out["counts"]
    assert (c["source_graphic_candidates"],c["later_2016_petflag1_template_rows"],c["later_2016_distinct_template_ids"],c["tw1_pet07_original_graphic_keys"],c["graphic_keys_without_tw1_pet07"],c["later_only_sample_spr_index"],c["no_index_in_four_samples"],c["later_2016_template_rows_with_tw1_private_pixel_reference"],c["original_tw1_selected_three_actions_direction0_frame_positions"],c["positive_later_skill_slot_references"],c["resolved_later_same_source_skill_references"],c["unresolved_later_same_source_skill_references"],c["distinct_unresolved_later_skill_ids"],c["negative_later_skill_literals"],c["empty_later_skill_slots"])==(598,1024,1021,130,468,412,56,201,3255,2886,2784,102,30,20,4262)
    assert out["provenance"]["relationship"]=="NUMERIC_GRAPHIC_CANDIDATE_ONLY_NOT_SAME_DEPLOYMENT"
    return True
class Pet08(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=load("STONEAGE-PET-MODULE-01-BATCH-SOURCE-SPR-INDEX-R1.json")
        cls.b=load("STONEAGE-PET-MODULE-03-SAME-SOURCE-SKILL-JOIN-R1.json")
        cls.prior=load("STONEAGE-PET-MODULE-06-CONSOLIDATED-VISUAL-COVERAGE-R1.json")
        cls.pixels=load("STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json")
        cls.out=load(REPORT)
    def test_full_join(self):self.assertTrue(certify(self.out,self.a,self.b,self.prior,self.pixels))
    def test_no_official_identity_inflation(self):
        bad=copy.deepcopy(self.out);bad["boundaries"]["official_TW1_species_identity_from_later_community_graphic_ids"]=True
        with self.assertRaises(AssertionError):certify(bad,self.a,self.b,self.prior,self.pixels)
    def test_no_fake_proprietary_pixel_replay(self):
        bad=copy.deepcopy(self.out);bad["boundaries"]["original_TW1_pixels_redecoded_in_this_PUBLIC_metadata_replay"]=True
        with self.assertRaises(AssertionError):certify(bad,self.a,self.b,self.prior,self.pixels)
    def test_no_cross_source_skill_alias(self):
        bad=copy.deepcopy(self.out);bad["template_rows"][0][4][0][2]="PETSKILL_FABRICATED"
        with self.assertRaises(AssertionError):certify(bad,self.a,self.b,self.prior,self.pixels)
    def test_no_missing_tw1_sprite_group(self):
        bad=copy.deepcopy(self.out);bad["graphic_rows"][0][4]=None
        with self.assertRaises(AssertionError):certify(bad,self.a,self.b,self.prior,self.pixels)
    def test_no_silent_bad_RD_patch(self):
        bad=copy.deepcopy(self.out);bad["original_TW1_PET07_strict_RD_failures"]=[]
        with self.assertRaises(AssertionError):certify(bad,self.a,self.b,self.prior,self.pixels)
if __name__=="__main__":unittest.main()
