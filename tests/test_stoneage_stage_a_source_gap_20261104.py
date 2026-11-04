"""Stage A source-gap audit: replay exact archived evidence, not original game execution."""
from collections import Counter
from copy import deepcopy
import json,re,unittest
from pathlib import Path

R=Path(__file__).resolve().parents[1]/"research"/"recovered"
OUT=R/"STONEAGE-STAGE-A-ORIGINAL-DAT-AND-SAME-BUILD-SOURCE-GAP-R1.json"
MAP=R/"STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json"
I1=R/"STONEAGE-INTEGRATION01-NPC-PET-QUEST-ITEM-MAP-SOURCE-GRAPH-R1.json"
I2=R/"STONEAGE-INTEGRATION02-ORIGINAL-SCENE-DAT-RD-CROSSMODULE-R1.json"
I3=R/"STONEAGE-INTEGRATION03-ORIGINAL-NPC-SPR-DAT-VISUAL-SOURCE-R1.json"
STAGE=R/"STONEAGE-STAGE-A-CONSOLIDATED-REVIEW-R2.json"

def validate(d,m,i1,i2,i3,s):
    assert d["schema"]=="stoneage.stage_a_integrated_original_map_source_gap_replay.r1"
    assert d["source_main_HEAD"]=="7bf3d859835cca9689f6de46ecf8ab60f2cabfa5"
    assert d["source_current_historical_blob_preserved"]=="c89e0e33537990aa2132b47c40fef49a985a935c"
    assert d["source_git_blobs"]=={
        "map01":"03675ee98d391f9ef0246315b2426f2a8b721fd3",
        "int01":"5e526512c0277e19ca41dfcd934c230404d1dfb4",
        "int02":"2303f1df3749ca28a4f9539869359666021b8783",
        "int03":"55bca6e505b647065d5318005fcceb3f821b0917",
        "stage":"72f3bbee8de2728db7955001f2c9567ad165a3fc"}
    assert d["preserved_archive"]["source_original_RAR_sha256"]==m["original_rar_sha256"]
    assert d["preserved_archive"]["source_original_RAR_bytes"]==m["original_rar_bytes"]
    assert d["preserved_archive"]["source_kind"]==m["source_scope"]
    assert "NO_RAR_REEXTRACTION" in d["method"]
    source=m["original_decoded_source_rows"]
    failed=m["source_extraction_errors_not_reclassified_as_corruption"]
    source_rows=lambda floor,group,ext:[x for x in source if x[0]==group and re.fullmatch(str(floor)+r"\."+ext,x[1],re.I)]
    fail_rows=lambda floor,group,ext:[x for x in failed if x[0]==group and re.fullmatch(str(floor)+r"\."+ext,x[1],re.I)]
    src_creates=i1["source_GetPet_CREATE_QUEST_script_AND_floor_joins"]
    npc_creates=i1["source_NPCEnemy_CREATE_ARG_floor_AND_candidate_enemy_ID_joins"]
    gaps=i2["per_floor_source_qualification"]
    pending={x["floor_id"] for x in gaps if x["source_DAT_qualification"]=="COMPLETE_SOURCE_DAT_UNVERIFIED"}
    assert pending=={100,200,3000,3021}
    assert len(d["priority_qualified_floor_gaps"])==4
    assert [x["floor_id"] for x in d["priority_qualified_floor_gaps"]]==[3021,100,3000,200]
    for x in d["priority_qualified_floor_gaps"]:
        floor=x["floor_id"]
        assert floor in pending
        parts=x["source_archived_member_presence"]
        ok=lambda raw:{"path":raw[1],"size_bytes":raw[2],"sha256":raw[3],"crc32":raw[4],"width":raw[6],"height":raw[7]}
        err=lambda raw:{"path":raw[1],"expected_member_bytes":raw[2],"emitted_bytes_before_error":raw[3],"error_tag":raw[4]}
        assert parts["group0_client_MAP_verified"]==list(map(ok,source_rows(floor,0,"MAP")))
        assert parts["group0_client_MAP_read_failures"]==list(map(err,fail_rows(floor,0,"MAP")))
        assert parts["group0_client_DAT_verified"]==list(map(ok,source_rows(floor,0,"DAT")))==[]
        assert parts["group0_client_DAT_read_failures"]==list(map(err,fail_rows(floor,0,"DAT")))
        assert parts["group1_addon_MAP_verified"]==list(map(ok,source_rows(floor,1,"MAP")))
        assert parts["group1_addon_MAP_read_failures"]==list(map(err,fail_rows(floor,1,"MAP")))
        assert parts["group1_addon_DAT_not_present_in_MAP01_group1"] is True
        assert len(parts["group0_client_MAP_verified"])+len(parts["group0_client_MAP_read_failures"])==1
        assert len(parts["group0_client_DAT_read_failures"])==1
        assert len(parts["group1_addon_MAP_verified"])+len(parts["group1_addon_MAP_read_failures"])==1
        original_map_expected=(parts["group0_client_MAP_verified"] or parts["group0_client_MAP_read_failures"])[0]
        maplen=original_map_expected.get("size_bytes",original_map_expected.get("expected_member_bytes"))
        datlen=parts["group0_client_DAT_read_failures"][0]["expected_member_bytes"]
        assert datlen==8+3*(maplen-8)
        assert x["source_expected_DAT_bytes_from_MAP_member_length_formula"]==datlen
        assert x["source_expected_DAT_matches_8_plus_three_times_MAP_payload_size"] is True
        assert x["original_DAT_header_and_all_cells_actually_verified"] is False
        m0=parts["group0_client_MAP_verified"]
        m1=parts["group1_addon_MAP_verified"]
        assert x["group0_and_group1_MAP_both_complete_and_identical_full_SHA"]==bool(m0 and m1 and m0[0]["sha256"]==m1[0]["sha256"])
        assert x["release_authentication"].startswith("PRESERVED_COMMUNITY")
        assert x["original_game_world_missing_this_floor_proven"] is False
        expected_gp=[{
            "original_CREATE_file":r["original_CREATE_file"],
            "source_CREATE_ordinal":r["original_CREATE_ordinal"],
            "source_CREATE_block_sha256":r["source_CREATE_block_sha256"],
            "original_script_path":r["script_path"],
            "source_script_SHA256":r["script_original_sha256"]
        } for r in src_creates if r["floor_id"]==floor]
        expected_npc=[{
            "original_CREATE_file":r["original_CREATE_file"],
            "source_CREATE_ordinal":r["original_CREATE_ordinal"],
            "source_CREATE_block_sha256":r["source_CREATE_block_sha256"],
            "original_ARG_path":r["source_ARG_file"],
            "source_ARG_sha256":r["source_ARG_file_sha256"]
        } for r in npc_creates if r["floor_id"]==floor]
        assert x["original_GetPet_CREATE_references"]==expected_gp
        assert x["original_NPCEnemy_CREATE_references"]==expected_npc
        c=x["static_reference_counts"]
        assert c=={
           "original_GetPet_CREATE_refs":len(expected_gp),
           "original_NPCEnemy_CREATE_refs":len(expected_npc),
           "different_original_NPCEnemy_CREATE_files":len({r["original_CREATE_file"] for r in expected_npc}),
           "different_original_NPCEnemy_ARG_files":len({r["original_ARG_path"] for r in expected_npc})}
    ss=d["summary"]
    assert ss["source_cohort_distinct_floors"]==i2["summary"]["unique_NPC_or_GetPet_source_floors"]==60
    assert ss["floors_MAP04_original_DAT_whole_SHA_qualified"]==55
    assert ss["floors_MAP02_independently_verified_original_DAT"]==1
    assert ss["floors_currently_missing_qualified_complete_original_DAT"]==4
    assert ss["original_GetPet_CREATE_static_refs_total"]==len(src_creates)==24
    assert ss["original_NPCEnemy_CREATE_static_refs_total"]==len(npc_creates)==279
    assert ss["original_GetPet_CREATE_static_refs_on_DAT_unqualified_floors"]==2
    assert ss["original_NPCEnemy_CREATE_static_refs_on_DAT_unqualified_floors"]==105
    assert ss["original_3021_NPCEnemy_CREATE_static_refs"]==100
    assert ss["original_3021_NPCEnemy_unique_ARG_files"]==100
    assert ss["original_3021_NPCEnemy_unique_CREATE_files"]==1
    assert ss["all_four_archived_MAP_DAT_header_size_relationships_consistent"] is True
    assert ss["prior_INTEGRATION03_exact_SPR_byte_identical_source_groups"]==i3["summary"]["source_distinct_full_SPR_SHA_groups_with_equality_to_TW10"]==3
    assert ss["new_original_MAP_DAT_SPR_source_bytes_recovered_by_this_gap_audit"]==0
    counts=dict(Counter(x["gate"] for x in s["families"]))
    assert counts==ss["existing_STAGE_A_family_counts"]=={"PARTIAL":7,"OPEN":2}
    assert d["stage_A_remaining_historical_primary_source_gates"]==[
      {"id":r["id"],"priority":r["priority"],"reopen":r["reopen"],"remaining_unproven":True}
      for r in s["blockers"]]
    assert d["bounds"]["overall_percent"] is None
    for k,v in d["bounds"].items():
      if k not in {"stage_A","stage_B_wiki","R79","overall_percent"}:
        assert v is False,(k,v)
    assert d["bounds"]["stage_A"]=="7PARTIAL_2OPEN"
    assert d["bounds"]["stage_B_wiki"]=="GATED"
    assert d["bounds"]["R79"]=="PAUSED_NON_BLOCKING"
    assert d["next"].startswith("SOURCE_READY_ORIGINAL_CLIENT")

class SourceGapAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
      cls.data=[json.loads(p.read_text(encoding="utf-8")) for p in (OUT,MAP,I1,I2,I3,STAGE)]
    def check(self,over):validate(over,*self.data[1:])
    def test_source_exact_replay(self):self.check(self.data[0])
    def test_reject_claim_that_3021_DAT_is_decoded(self):
      d=deepcopy(self.data[0]);d["priority_qualified_floor_gaps"][0]["original_DAT_header_and_all_cells_actually_verified"]=True
      with self.assertRaises(AssertionError):self.check(d)
    def test_reject_3021_100_refs_as_100_species(self):
      d=deepcopy(self.data[0]);d["bounds"]["source_CHAR09_100_original_CREATE_refs_equal_100_historical_enemy_species"]=True
      with self.assertRaises(AssertionError):self.check(d)
    def test_reject_promotion_of_crc_error_to_absent_world(self):
      d=deepcopy(self.data[0]);d["priority_qualified_floor_gaps"][1]["original_game_world_missing_this_floor_proven"]=True
      with self.assertRaises(AssertionError):self.check(d)
    def test_reject_forged_complete_MAP_DAT_size(self):
      d=deepcopy(self.data[0]);d["priority_qualified_floor_gaps"][0]["source_expected_DAT_bytes_from_MAP_member_length_formula"]+=2
      with self.assertRaises(AssertionError):self.check(d)
    def test_reject_suppressed_original_source_create_ref(self):
      d=deepcopy(self.data[0]);d["priority_qualified_floor_gaps"][0]["original_NPCEnemy_CREATE_references"].pop()
      with self.assertRaises(AssertionError):self.check(d)

if __name__=="__main__":unittest.main()
