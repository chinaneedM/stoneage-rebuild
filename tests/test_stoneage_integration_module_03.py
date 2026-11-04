"""INTEGRATION03: strict same-source SHA joins, not native historical deployment."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import unittest

R = Path(__file__).resolve().parents[1]/"research"/"recovered"
I1 = R/"STONEAGE-INTEGRATION01-NPC-PET-QUEST-ITEM-MAP-SOURCE-GRAPH-R1.json"
I2 = R/"STONEAGE-INTEGRATION02-ORIGINAL-SCENE-DAT-RD-CROSSMODULE-R1.json"
C5 = R/"STONEAGE-CHARACTER-NPC-MODULE-05-30-ORIGINAL-MOTION-SOURCE-BRIDGE-R1.json"
C9 = R/"STONEAGE-CHARACTER-NPC-MODULE-09-ORIGINAL-NPCENEMY-ROSTER-BRIDGE-R1.json"
P7 = R/"STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json"
OUT = R/"STONEAGE-INTEGRATION03-ORIGINAL-NPC-SPR-DAT-VISUAL-SOURCE-R1.json"

def verify(d, i1, i2, c5, c9, p7):
    assert d["schema"]=="stoneage.integration_module03_exact_original_SPR_and_candidate_NPCEnemy_visual_to_DAT_source.r1"
    assert d["baseline_main_commit"]=="870de82720bf8c8d9d4868e26c12cd5714690840"
    assert d["preserved_original_CURRENT_state_blob"]=="c89e0e33537990aa2132b47c40fef49a985a935c"
    assert d["source_qualified_git_blobs"]=={
        "integration01":"5e526512c0277e19ca41dfcd934c230404d1dfb4",
        "integration02":"2303f1df3749ca28a4f9539869359666021b8783",
        "char05":"9afacb49d11dd7cc546fabe594170053d49b1f9b",
        "char09":"3d827b98d00c3caa6e779f34a36d28bd70945b75",
        "pet07":"0b5f81b41a642025ab53a12884638fdee887470e"}
    assert d["main_source_original_community_RAR_SHA256"]==c5["original_RAR_sha256"]==c9["original_rar_sha256"]
    assert len(c5["config_with_existing_real_art"])==30
    assert len(c9["source_enemy_number_to_paired_template_and_spr"])==230
    assert len(p7["source_groups"])==130
    floors={x["floor_id"]:x for x in i2["per_floor_source_qualification"]}
    orig_spr={x["spr_no"]:x for x in c5["prior_original_SPR_groups"]}
    src_spr={x[0]:x for x in p7["source_groups"]}
    expected=[]
    for r in c5["config_with_existing_real_art"]:
        if r["source_floorid"] not in floors:continue
        dat=floors[r["source_floorid"]]
        assert dat["source_DAT_qualification"]=="MAP04_EXACT_DAT_FULL_SHA"
        tw1=src_spr[r["source_graphicname"]]
        prior=orig_spr[r["source_graphicname"]]
        assert prior["full_segment_sha256"]==tw1[2]==r["source_original_SPR_segment_sha256"]
        assert prior["index"]==tw1[1]
        expected.append({
            "original_CHAR05_CREATE_path":r["source_create_path"],
            "original_CREATE_ordinal":r["source_create_ordinal"],
            "original_CREATE_block_sha256":r["source_block_sha256"],
            "original_CREATE_floor_id":r["source_floorid"],
            "original_same_RAR_function_literal":r["source_template_function"],
            "original_source_graphic_number":r["source_graphicname"],
            "original_original_source_full_SPR_segment_sha256":r["source_original_SPR_segment_sha256"],
            "original_TW10_PET07_full_SPR_segment_sha256":tw1[2],
            "source_SPR_group_index":tw1[1],
            "source_qualified_mixed25_original_DAT_SHA256":dat["qualified_complete_original_DAT"]["original_dat_sha256"],
            "prior_mixed25_CHAR05_original_RD_motion_observation":r["existing_original_RD_material"],
            "prior_TW10_PET07_retail_RD_pixel_observation":"PRIOR_PRIVATE_REAL_PIXEL_DECODING_WITH_QUALIFIED_SOURCE_BUT_NOT_NATIVE_RENDER",
            "original_native_NPC_placement_or_execution_proven":False,
        })
    expected.sort(key=lambda a:(a["original_CREATE_floor_id"],a["original_CHAR05_CREATE_path"],a["original_CREATE_ordinal"]))
    assert expected==d["source_exact_NPC_CREATES_to_qualified_DAT_and_identical_full_SPR_across_TW10"]
    assert len(expected)==4
    graph={r[0]:r[2] for r in c9["source_enemy_number_to_paired_template_and_spr"]}
    originals=set(graph.values())
    pixelIDs=set(src_spr)
    match=sorted(originals&pixelIDs)
    unknown=sorted(originals-pixelIDs)
    cross=d["numeric_only_candidate_NPCEnemy_original_ARG_template_to_PET07"]
    assert cross["paired_original_enemy_instance_rows"]==len(graph)==230
    assert cross["original_distinct_paired_graphic_numbers"]==len(originals)==117
    assert cross["source_paired_graphic_numbers_with_PET07_TW10_group"]==match
    assert cross["source_paired_graphic_numbers_not_in_PET07_TW10_group"]==unknown
    assert "ONLY_CROSS_CARRIER_NUMERIC" in cross["classification"]
    counts={}
    for x in i1["source_NPCEnemy_CREATE_ARG_floor_AND_candidate_enemy_ID_joins"]:
        floor=floors[x["floor_id"]]
        typ=floor["source_DAT_qualification"]
        row=counts.setdefault(typ,{
            "original_NPCEnemy_CREATE_refs":0,
            "source_creates_with_at_least_one_TW10_graphic_numeric_candidate":0,
            "source_creates_with_all_paired_graphic_numbers_found_in_PET07_TW10":0})
        values={graph[id_] for id_ in x["original_qualifying_230_instance_IDs"]}
        assert values
        row["original_NPCEnemy_CREATE_refs"]+=1
        if values&pixelIDs:row["source_creates_with_at_least_one_TW10_graphic_numeric_candidate"]+=1
        if values<=pixelIDs:row["source_creates_with_all_paired_graphic_numbers_found_in_PET07_TW10"]+=1
    assert cross["original_NPCEnemy_CREATE_ref_counts_by_DAT_source"]==counts
    s=d["summary"]
    assert s["original_CHAR05_private_action0_eight_direction_configs_total"]==30
    assert s["exact_CREATE_SPR_and_MAP04_original_DAT_joins"]==len(expected)==4
    assert s["source_distinct_full_SPR_SHA_groups_with_equality_to_TW10"]==3
    assert s["distinct_crosscohort_original_floor_ids"]==[2000,11006,20401]
    assert s["source_NPCEnemy_ARG_static_CREATE_refs"]==sum(x["original_NPCEnemy_CREATE_refs"] for x in counts.values())==279
    assert s["source_NPCEnemy_paired_candidate_original_graphic_numbers"]==117
    assert s["source_NPCEnemy_graphic_number_candidates_with_prior_TW10_RD_decoding"]==len(match)==96
    assert s["source_NPCEnemy_graphic_number_candidates_without_prior_TW10_RD_decoding"]==len(unknown)==21
    assert s["source_NPCEnemy_CREATE_refs_with_at_least_one_TW10_candidate"]==sum(x["source_creates_with_at_least_one_TW10_graphic_numeric_candidate"] for x in counts.values())==269
    assert s["source_NPCEnemy_CREATE_refs_with_all_TW10_candidates"]==sum(x["source_creates_with_all_paired_graphic_numbers_found_in_PET07_TW10"] for x in counts.values())==54
    assert sum(x["original_NPCEnemy_CREATE_refs"] for x in counts.values())==279
    assert d["boundaries"]["original_SPR_full_segment_sha_equality_proves_shared_bytes_only"] is True
    for k,v in d["boundaries"].items():
        if k.startswith("original_") and k!="original_SPR_full_segment_sha_equality_proves_shared_bytes_only":
            assert v is False, (k,v)
    assert d["boundaries"]["overall_percent"] is None
    assert d["boundaries"]["stage_A"]=="7PARTIAL_2OPEN"
    assert d["next"].startswith("STAGE_A_RESTORATION_")

class Integration03SourceContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads(OUT.read_text())
        cls.i1=json.loads(I1.read_text())
        cls.i2=json.loads(I2.read_text())
        cls.c5=json.loads(C5.read_text())
        cls.c9=json.loads(C9.read_text())
        cls.p7=json.loads(P7.read_text())

    def check(self,d):verify(d,self.i1,self.i2,self.c5,self.c9,self.p7)

    def test_exact_cross_source_replay(self):self.check(self.report)

    def test_reject_same_numeric_id_with_different_SPR_sha(self):
        d=deepcopy(self.report)
        d["source_exact_NPC_CREATES_to_qualified_DAT_and_identical_full_SPR_across_TW10"][0]["original_TW10_PET07_full_SPR_segment_sha256"]="0"*64
        with self.assertRaises(AssertionError):self.check(d)

    def test_reject_unqualified_DAT_as_verified(self):
        d=deepcopy(self.report)
        d["source_exact_NPC_CREATES_to_qualified_DAT_and_identical_full_SPR_across_TW10"][0]["source_qualified_mixed25_original_DAT_SHA256"]="0"*64
        with self.assertRaises(AssertionError):self.check(d)

    def test_reject_numeric_candidate_as_playable_original_NPC(self):
        d=deepcopy(self.report)
        d["boundaries"]["original_original_game_NPC_or_enemy_placed_and_rendered"]=True
        with self.assertRaises(AssertionError):self.check(d)

    def test_reject_missing_PET07_graphic_promoted(self):
        d=deepcopy(self.report)
        d["numeric_only_candidate_NPCEnemy_original_ARG_template_to_PET07"]["source_paired_graphic_numbers_with_PET07_TW10_group"].append(99999999)
        with self.assertRaises(AssertionError):self.check(d)

if __name__=="__main__":
    unittest.main()
