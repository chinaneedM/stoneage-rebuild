"""Integration01 original source-edge conservation, not actual game execution."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import re
import unittest

R=Path(__file__).resolve().parents[1]/"research"/"recovered"
INT=R/"STONEAGE-INTEGRATION01-NPC-PET-QUEST-ITEM-MAP-SOURCE-GRAPH-R1.json"
MAP=R/"STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json"
QUEST=R/"STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json"
GAMEPLAY=R/"STONEAGE-GAMEPLAY07-GETPET-NPCENEMY-ORIGINAL-SKILL-SOURCE-R1.json"
NPC=R/"STONEAGE-CHARACTER-NPC-MODULE-09-ORIGINAL-NPCENEMY-ROSTER-BRIDGE-R1.json"
ITEMS=[R/"item-module-01"/f"STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{i:02d}-R1.json" for i in range(1,8)]

def verify(d,m,q,g,n,shards):
    assert d["schema"]=="stoneage.integration_module01_source_conserved_npc_pet_quest_item_map_chain.r1"
    assert d["source_class"]=="COMMUNITY_PRESERVED_MIXED25_ARCHIVE_CROSS_MODULE_BYTE_SOURCE_ONLY"
    assert d["source_main_HEAD_at_start"]=="ec0e214528bb1ceb8329335d5f18cbfd510c5585"
    blobs=d["source_blobs"]
    assert blobs["map01"]=="03675ee98d391f9ef0246315b2426f2a8b721fd3"
    assert blobs["quest01"]=="52db8b4b6cd43cd2afa4a8d2e8460f214933f5e2"
    assert blobs["gameplay07"]=="6218d88450953684dafcf19a9f85ba94d907772a"
    assert blobs["char09"]=="3d827b98d00c3caa6e779f34a36d28bd70945b75"
    assert len(blobs["item01_seven_shards"])==7
    orig=d["source_original_mixed25_RAR_identity"]
    assert orig["bytes"]==m["original_rar_bytes"]==q["source"]["original_RAR_bytes"]==n["original_rar_size_bytes"]==361255180
    assert orig["sha256"]==m["original_rar_sha256"]==q["source"]["original_RAR_sha256"]==n["original_rar_sha256"]=="d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5"
    assert orig["original_parent_RAR_reopened_this_unit"] is False

    physical={}
    mfiles=[x for x in m["original_decoded_source_rows"] if x[0]==0]
    for raw in mfiles:
        mname=re.fullmatch(r"(\d+)\.(map|dat)",raw[1],re.I)
        if not mname:continue
        ident=int(mname.group(1));suffix=mname.group(2).lower()
        assert (ident,suffix) not in physical
        physical[(ident,suffix)]=raw
    err={}
    for raw in m["source_extraction_errors_not_reclassified_as_corruption"]:
        if raw[0]!=0:continue
        mat=re.fullmatch(r"(\d+)\.(map|dat)",raw[1],re.I)
        if not mat:continue
        fl=int(mat.group(1));err.setdefault(fl,[]).append({
          "source_original_path":raw[1],
          "source_original_bytes_expected":raw[2],
          "original_libarchive_error":raw[4]})
    def ptr(raw):
        return None if raw is None else {
          "original_path":raw[1],
          "source_member_bytes":raw[2],
          "source_sha256":raw[3],
          "source_crc32":raw[4],
          "floor_id_from_original_row":raw[5],
          "width":raw[6],
          "height":raw[7],
          "source_shape_flag":raw[8]}
    floors=d["source_original_main_client_floor_files_with_disqualified_read_errors"]
    assert [x["floor_id"] for x in floors]==sorted({x["floor_id"] for x in floors})
    byfloor={x["floor_id"]:x for x in floors}
    for floor,rec in byfloor.items():
        assert rec["original_main_client_MAP"]==ptr(physical.get((floor,"map")))
        assert rec["original_main_client_DAT"]==ptr(physical.get((floor,"dat")))
        assert rec["original_extractor_read_error_members"]==err.get(floor,[])
        assert rec["source_mapset_master_membership_not_proven_from_this_join"] is True
        assert all(src is None or src["floor_id_from_original_row"]==floor for src in [
          rec["original_main_client_MAP"],rec["original_main_client_DAT"]])

    qrefs={(r["create_source_path"],r["create_brace_ordinal"],r["original_script_path"]):r
       for r in q["source_creation_references"]}
    scriptfiles={x["original_source_relative_path"]:x for x in g["source_GetPet_original_NPC_files"]
       if x["changeevent_static_file_reference_creates"]}
    expectedcreate={}
    for script in scriptfiles.values():
        for ref in script["changeevent_static_file_reference_creates"]:
            key=(ref["create_file"],ref["ordinal"],script["original_source_relative_path"])
            expectedcreate[key]=(script,ref)
    createjoin=d["source_GetPet_CREATE_QUEST_script_AND_floor_joins"]
    assert len(createjoin)==len(expectedcreate)==24
    seen=set()
    for j in createjoin:
        k=(j["original_CREATE_file"],j["original_CREATE_ordinal"],j["script_path"])
        assert k in expectedcreate and k not in seen
        seen.add(k)
        script,ref=expectedcreate[k]
        qref=qrefs[k]
        assert j["source_CREATE_block_sha256"]==ref["create_block_sha256"]
        assert j["script_original_sha256"]==qref["original_script_sha"]==script["source_sha256"]
        assert j["floor_id"]==qref["floorid"] and j["floor_id"] in byfloor
        assert j["source_quest_origin_class"]==qref["origin_class"]=="UNRESOLVED"
        assert j["source_GETPET_command_lines"]==[x["original_source_physical_line"] for x in script["script_commands"]]
        assert j["source_GETPET_numeric_literals_ordered"]==[
          v for x in script["script_commands"] for v in x["source_integer_tokens_ordered"]]
    assert seen==set(expectedcreate)
    srcblocks={}
    for b in q["source_event_blocks"]:
        srcblocks.setdefault(b["script_path"],[]).append(b)
    scriptitem={x["script_path"]:x for x in d["source_GetPet_distinct_QUEST_script_item_number_source_catalog"]}
    assert set(scriptitem)==set(scriptfiles) and len(scriptitem)==23
    allids=set();kindcounts=Counter();nitemrefs=0
    for path,record in scriptitem.items():
        s=scriptfiles[path];blocks=srcblocks[path];counts=Counter();refs=[]
        assert record["source_file_sha256"]==s["source_sha256"]
        assert len(blocks)==record["source_quest_block_count"]
        for b in blocks:
            assert b["source_file_sha"]==s["source_sha256"]
            for kind,vals in b["item_numeric_refs"].items():
                counts[kind]+=len(vals)
                refs.extend(vals)
                kindcounts[kind]+=len(vals)
        assert dict(counts)==record["source_item_ref_type_occurrences"]
        assert len(refs)==record["source_item_number_occurrences"]
        assert sorted(set(refs))==record["distinct_source_item_numeric_candidates"]
        allids.update(refs);nitemrefs+=len(refs)
    index={}
    for shard in shards:
        for r in shard["rows"]:
            assert r[0] not in index
            index[r[0]]=r
    assert len(index)==13915
    receipts=d["source_GetPet_QUEST_scripts_item_numeric_candidate_two_itemset_receipts"]
    assert [r["numeric_ID"] for r in receipts]==sorted(allids)
    for v in receipts:
        i=v["numeric_ID"]; original=index.get(i)
        assert original is not None
        assert v["source_itemset_A_row_sha256"]==original[1]
        assert v["source_itemset_B_row_sha256"]==original[2]
        assert v["source_master_choice_verified"] is False
    s=d["summary"]
    assert len(createjoin)==s["original_static_GetPet_QUEST_create_ref_joins"]==24
    assert len(scriptitem)==s["source_GetPet_distinct_script_joins"]==23
    assert len(set(x["floor_id"] for x in createjoin))==s["source_GetPet_distinct_create_floor_ids"]==19
    assert sum(x["source_quest_block_count"] for x in scriptitem.values())==s["source_QUEST01_control_blocks_for_23_scripts"]==116
    assert nitemrefs==s["source_item_token_occurrences_from_QUEST01_script_control_blocks"]==309
    assert len(allids)==len(receipts)==s["source_item_numeric_IDs_distinct"]==101
    assert sum(bool(x["source_itemset_A_row_sha256"]) and bool(x["source_itemset_B_row_sha256"]) for x in receipts)==s["source_item_numeric_IDs_present_in_both_itemsets"]==101
    assert dict(kindcounts)==s["source_item_numeric_refs_by_kind"]=={
       "DelItem":74,"GetItem":18,"predicate_ITEM":135,"GetRandItem":82}

    argmap={x[0]:x for x in n["argument_files"]}
    originalcreats={(x[0],x[1]):x for x in n["create_refs"]}
    contentref=n["source_enemy_number_to_paired_template_and_spr"]
    valid_ids={x[0] for x in contentref}
    np=d["source_NPCEnemy_CREATE_ARG_floor_AND_candidate_enemy_ID_joins"]
    assert len(np)==s["source_NPCEnemy_original_create_arg_floor_refs"]==279
    seen=set();tokens_main=0;tokens_comp=0
    for r in np:
        key=(r["original_CREATE_file"],r["source_CREATE_ordinal"])
        assert key in originalcreats and key not in seen
        seen.add(key);src=originalcreats[key];a=argmap[src[7]]
        assert (r["source_CREATE_block_sha256"],r["floor_id"])==(src[2],src[3])
        assert (r["source_ARG_file"],r["source_ARG_file_sha256"])==(src[7],src[8])==(a[0],a[1])
        assert r["floor_id"] in byfloor
        assert r["original_ENEMYNO_numeric_ref_count"]==len(a[3])
        assert r["original_ENEMYPETNO_numeric_ref_count"]==len(a[4])
        ids=sorted(set(a[3]+a[4]))
        assert set(ids)<=valid_ids
        assert r["original_qualifying_230_instance_IDs"]==ids
        tokens_main+=len(a[3]);tokens_comp+=len(a[4])
    assert seen==set(originalcreats)
    assert len({r["source_ARG_file"] for r in np})==s["source_NPCEnemy_unique_ARG_files"]==260
    assert tokens_main==s["source_NPCEnemy_main_numeric_enemy_reference_occurrences"]==3930
    assert tokens_comp==s["source_NPCEnemy_companion_numeric_enemy_reference_occurrences"]==7000
    assert len(byfloor)==s["total_distinct_floor_refs_in_both_content_cohorts"]==60
    assert sum(1 for x in mfiles if x[1].lower().endswith(".map"))==s["source_main_client_MAP_file_count"]==1019
    assert sum(1 for x in mfiles if x[1].lower().endswith(".dat"))==s["source_main_client_DAT_file_count"]==971
    def statuses(links):
        z=Counter({"both":0,"map_only":0,"dat_only":0,"neither":0,"with_map":0,"with_dat":0,"with_source_extraction_errors":0})
        for v in links:
            f=byfloor[v["floor_id"]];has_m=f["original_main_client_MAP"] is not None
            has_d=f["original_main_client_DAT"] is not None
            z[("both" if has_m and has_d else "map_only" if has_m else "dat_only" if has_d else "neither")]+=1
            z["with_map"]+=int(has_m);z["with_dat"]+=int(has_d)
            z["with_source_extraction_errors"]+=bool(f["original_extractor_read_error_members"])
        return dict(z)
    assert statuses(createjoin)==s["source_GetPet_CREATE_map_DAT_coverage"]=={
       "both":21,"map_only":1,"dat_only":0,"neither":2,
       "with_map":22,"with_dat":21,"with_source_extraction_errors":3}
    assert statuses(np)==s["source_NPCEnemy_CREATE_map_DAT_coverage"]=={
       "both":168,"map_only":100,"dat_only":6,"neither":5,
       "with_map":268,"with_dat":174,"with_source_extraction_errors":111}
    for r in createjoin:
        f=byfloor[r["floor_id"]]
        if f["original_main_client_MAP"] is None or f["original_main_client_DAT"] is None:
            assert f["original_extractor_read_error_members"],"Don't silently claim source file was absent"
    for r in np:
        f=byfloor[r["floor_id"]]
        if f["original_main_client_MAP"] is None or f["original_main_client_DAT"] is None:
            assert f["original_extractor_read_error_members"],"Don't silently claim source file was absent"
    bounds=d["source_boundaries"]
    for name in (
       "original_same_RAR_archive_identity_does_not_authenticate_same_deployed_server",
       "source_MAP_DAT_extraction_failures_are_not_proof_original_files_absent",
       "source_MAP_DAT_access_not_native_game_collision_or_renderer",
       "source_GETPET_CREATE_QUEST_source_SHA_same_is_not_executed_quest",
       "source_ITEM_numeric_collisions_not_actual_condition_reward_or_payment",
       "source_NPCEnemy_EnemyAndPetNumbers_are_candidate_roster_only",
       "source_NPCEnemy_ARG_ID_to_paired_template_has_no_native_capture_exec"):
       assert bounds[name] is True
    for name in (
       "source_actual_original_MAP_DAT_member_bytes_reextracted_this_work_unit",
       "source_original_official_JSS1999_TW10_CN182_equivalence_verified",
       "source_later_mixed_archive_original_world_executed",
       "source_any_commercial_original_text_assets_published"):
       assert bounds[name] is False
    assert bounds["stage_A"]=="7_PARTIAL_2_OPEN" and bounds["stage_B_and_wiki"]=="GATED"
    assert bounds["R79"]=="PAUSED_NON_BLOCKING" and bounds["overall_percent"] is None
    assert d["next"].startswith("INTEGRATION-MODULE-02")
    return True

class TestIntegration01(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.args=[
          json.loads(p.read_text(encoding="utf-8"))
          for p in [INT,MAP,QUEST,GAMEPLAY,NPC,*ITEMS]]
    def test_complete_cross_source_join(self):
        self.assertTrue(verify(*self.args[:5],self.args[5:]))
    def reject(self,act):
        args=[deepcopy(x) for x in self.args];act(args[0])
        with self.assertRaises((AssertionError,KeyError,IndexError,TypeError)):
            verify(*args[:5],args[5:])
    def test_source_create_SHA_swap_rejected(self):
        self.reject(lambda d:d["source_GetPet_CREATE_QUEST_script_AND_floor_joins"][0].__setitem__("source_CREATE_block_sha256","0"*64))
    def test_false_map_restoration_rejected(self):
        self.reject(lambda d:next(x for x in d["source_original_main_client_floor_files_with_disqualified_read_errors"] if x["floor_id"]==3000).__setitem__("original_extractor_read_error_members",[]))
    def test_reassigned_script_floor_rejected(self):
        self.reject(lambda d:d["source_GetPet_CREATE_QUEST_script_AND_floor_joins"][0].__setitem__("floor_id",999999))
    def test_fake_original_item_presence_rejected(self):
        self.reject(lambda d:d["source_GetPet_QUEST_scripts_item_numeric_candidate_two_itemset_receipts"][0].__setitem__("source_itemset_A_row_sha256",None))
    def test_ARG_enemy_ID_fabrication_rejected(self):
        self.reject(lambda d:d["source_NPCEnemy_CREATE_ARG_floor_AND_candidate_enemy_ID_joins"][0]["original_qualifying_230_instance_IDs"].append(999999))
    def test_false_quest_execution_rejected(self):
        self.reject(lambda d:d["source_boundaries"].__setitem__("source_GETPET_CREATE_QUEST_source_SHA_same_is_not_executed_quest",False))
    def test_false_official_build_rejected(self):
        self.reject(lambda d:d["source_boundaries"].__setitem__("source_original_official_JSS1999_TW10_CN182_equivalence_verified",True))

if __name__=="__main__":unittest.main()
