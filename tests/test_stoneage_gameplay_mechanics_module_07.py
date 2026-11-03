"""GAMEPLAY07: derived original source crosswalk checks, not a native pet-capture simulation."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import re
import unittest

RECOVERED=Path(__file__).resolve().parents[1]/"research"/"recovered"
D=RECOVERED/"STONEAGE-GAMEPLAY07-GETPET-NPCENEMY-ORIGINAL-SKILL-SOURCE-R1.json"
CHAR01=RECOVERED/"STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json"
CHAR09=RECOVERED/"STONEAGE-CHARACTER-NPC-MODULE-09-ORIGINAL-NPCENEMY-ROSTER-BRIDGE-R1.json"
PET10=RECOVERED/"STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json"
O59=RECOVERED/"STONEAGE-O59-NAMED-WILD-CAPTURE-SOURCE-R1.json"
SHOP03=RECOVERED/"STONEAGE-GAMEPLAY03-ORIGINAL-21-PET-SKILL-SHOP-SOURCE-R1.json"

def verify(d, c, n, pet, wild, shop):
    assert d["schema"]=="stoneage.gameplay_mechanics_module07_getpet_npcenemy_skill_boundary.r1"
    assert d["material_scope"]=="MIXED25_COMMUNITY_PRESERVED_STATIC_SOURCE_GRAPH_NOT_AUTHENTICATED_JSS1999_TW1_CN182_OR_EXECUTABLE_SERVER"
    s=d["summary"]; prov=d["provenance_git_blobs"]
    assert prov=={
        "char01":"a088b61a3212f7049e7793f587123ffb29bebad7",
        "char09":"3d827b98d00c3caa6e779f34a36d28bd70945b75",
        "pet10":"25a37aeb134fb180e322e7dc335029b7374452d8",
        "o59":"fa9a6f64e889d4ad4ac932f9ce1aa42d084847c5",
        "gameplay03":"5735ddc1117a8a6fb2f9417327ec242e4fd06192"
    }
    zp=d["source_original_private_npc_zip"]
    assert zp["size"]==995176
    assert zp["sha256"]=="c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f"
    assert (zp["subtree_files"],zp["subtree_bytes"])==(
        c["npc_subtree_source_files"],c["npc_subtree_source_bytes"])==(2205,1930332)
    assert zp["whole_archive_and_all_original_files_SHA_CRC_replayed_in_this_work"] is True
    orig=d["source_original_RAR_from_existing_pet10_not_reopened_this_unit"]
    assert orig["size"]==pet["preserved_original_rar"]["bytes"]==361255180
    assert orig["sha256"]==pet["preserved_original_rar"]["sha256"]
    assert len(d["source_GetPet_original_NPC_files"])==s["source_getpet_script_files"]==27
    fs={r[0]:r for r in c["source_files"]}
    scripts=d["source_GetPet_original_NPC_files"]
    assert len({r["original_source_relative_path"] for r in scripts})==27
    nums=[];lines=0;backup=0;with_refs=0;ref_count=0;not_refs=[]
    for r in scripts:
        path=r["original_source_relative_path"];origfile=fs[path]
        assert (r["original_bytes"],r["source_sha256"],r["source_crc32"])==tuple(origfile[1:4])
        assert re.fullmatch(r"[a-f0-9]{64}",r["source_sha256"])
        is_backup=bool(re.search(r"\.(?:old|bak)$",path,re.I))
        assert r["source_status"]==("BACKUP_NOT_ASSUMED_DEPLOYED" if is_backup else "PRIMARY_PATH_NOT_PROVEN_DEPLOYED")
        backup+=int(is_backup)
        true_refs=[{"create_file":x[0],"ordinal":x[1],"source_function":x[11],
                    "create_block_sha256":x[4]} for x in c["create_rows"] if any(y[0]==path for y in x[15])]
        assert r["changeevent_static_file_reference_creates"]==true_refs
        assert all(x["source_function"]=="changeevent" for x in true_refs)
        ref_count+=len(true_refs);with_refs+=bool(true_refs)
        if not true_refs:not_refs.append(path)
        for ln in r["script_commands"]:
            assert ln["original_source_physical_line"]>0
            assert re.fullmatch(r"[a-f0-9]{64}",ln["source_line_sha256"])
            assert ln["source_literal_keyword"]=="GetPet"
            assert ln["source_exact_text_disclosed"] is False
            ids=ln["source_integer_tokens_ordered"]
            assert ids and all(isinstance(x,int) and x>=0 for x in ids)
            nums.extend(ids)
            lines+=1
    assert (backup,lines,len(nums),len(set(nums)))==(
        s["source_getpet_backup_files"],s["source_getpet_directive_lines"],
        s["source_getpet_numeric_occurrences"],s["source_getpet_distinct_numeric_ids"])==(2,29,44,36)
    assert (with_refs,ref_count)==(
        s["source_getpet_files_with_direct_changeevent_refs"],
        s["source_getpet_direct_changeevent_create_refs"])==(23,24)
    assert not_refs==s["source_getpet_paths_without_direct_file_ref"]==[
        "giiru/event/event30_5","giiru/event/event30_5.old",
        "giiru/event/sink/equiz_04","quiz/equiz_04.BAK"]
    def find(path):return next(x for x in scripts if x["original_source_relative_path"]==path)
    assert find("quiz/equiz_04")["script_commands"][0]["source_integer_tokens_ordered"]==[351]
    assert find("quiz/equiz_04.BAK")["script_commands"][0]["source_integer_tokens_ordered"]==[352]
    assert find("giiru/event/event30_5")["script_commands"][0]["source_integer_tokens_ordered"]==[355]
    assert find("giiru/event/event30_5.old")["script_commands"][0]["source_integer_tokens_ordered"]==[355]
    assert find("jaruga/event/oev_edb")["script_commands"][0]["source_integer_tokens_ordered"].count(482)==2
    assert Counter(nums)[482]==3
    tp={r[1]:r for r in pet["source_rows"]["enemybase.txt"]}
    ta={r[1]:r for r in pet["source_rows"]["enemybase2.txt"]}
    collision=d["source_GetPet_numeric_ID_collisions_only"]
    assert [r["literal_numeric_id"] for r in collision]==sorted(set(nums))
    for x in collision:
        i=x["literal_numeric_id"]
        assert x["primary_enemybase_line"]==(tp[i][0] if i in tp else None)
        assert x["alternate_enemybase_line"]==(ta[i][0] if i in ta else None)
        assert x["numeric_ID_collisions_do_not_prove_GetPet_ID_namespace"] is True
    assert sum(x["primary_enemybase_line"] is not None for x in collision)==s["source_getpet_ids_colliding_primary_enemybase_templates"]==26
    assert sum(x["alternate_enemybase_line"] is not None for x in collision)==s["source_getpet_ids_colliding_alternate_enemybase_templates"]==7

    source_edges=n["source_enemy_number_to_paired_template_and_spr"]
    edges=d["source_NPCEnemy_enemy_instance_to_template_numeric_IDs"]
    assert edges==[x[:4] for x in source_edges]
    assert len(edges)==s["source_npcenemy_distinct_enemy_instance_IDs"]==230
    assert s["source_npcenemy_original_create_refs"]==n["counts"]["NPCEnemy_config_refs"]==279
    assert len(set(e[0] for e in edges))==230
    assert len(set(e[2] for e in edges))==s["source_npcenemy_graphic_IDs"]==117
    assert sum(e[3]==0 for e in edges)==s["source_npcenemy_template_petflag_zero_instance_rows"]==142
    assert sum(e[3]==1 for e in edges)==s["source_npcenemy_template_petflag_one_instance_rows"]==88
    assert set(e[3] for e in edges)=={0,1}
    pairs=d["source_NPCEnemy_distinct_original_template_pairs"]
    assert len(pairs)==s["source_npcenemy_distinct_template_IDs"]==214
    assert [q["template_id"] for q in pairs]==sorted(set(e[1] for e in edges))
    bypair={q["template_id"]:q for q in pairs}
    diff=[];positive=[[],[]]
    for q in pairs:
        i=q["template_id"];a=tp[i];b=ta[i]
        assert q["source_graphic_no"]==a[2]==b[2]
        assert q["PETFLG_template_source_flag"]==a[3]==b[3]
        assert (q["primary_original_row_sha256"],q["alternate_original_row_sha256"])==(a[16],b[16])
        coreequal=a[1:16]==b[1:16]
        assert q["original_numeric_core_sources_agree"]==coreequal
        assert q["primary_seven_skill_slot_literals"]==a[15]
        assert q["alternate_seven_skill_slot_literals"]==b[15]
        assert len(a[15])==len(b[15])==7
        assert q["source_master_selector_verified"] is False
        if not coreequal:diff.append(i)
        for ix,r in enumerate([a,b]):
            positive[ix].extend(x for x in r[15] if isinstance(x,int) and x>0)
    assert len(pairs)-len(diff)==s["source_npcenemy_primary_alternative_numeric_field_equal_template_ids"]==213
    assert diff==s["source_npcenemy_primary_alternative_diff_template_ids"]==[651]
    q=bypair[651]
    assert q["primary_seven_skill_slot_literals"]==s["source_npcenemy_template_651_original_skill_slots_primary"]==[0,None,None,None,None,None,None]
    assert q["alternate_seven_skill_slot_literals"]==s["source_npcenemy_template_651_original_skill_slots_alternative"]==[50,51,52,None,None,None,None]
    primary_weighted=sum(sum(isinstance(v,int) and v>0 for v in bypair[e[1]]["primary_seven_skill_slot_literals"]) for e in edges)
    alternate_weighted=sum(sum(isinstance(v,int) and v>0 for v in bypair[e[1]]["alternate_seven_skill_slot_literals"]) for e in edges)
    assert primary_weighted==s["source_npcenemy_positive_template_skill_occurrences_primary_weighted_instances"]==530
    assert alternate_weighted==s["source_npcenemy_positive_template_skill_occurrences_alternative_weighted_instances"]==533
    up=set(positive[0]);ua=set(positive[1])
    assert len(up)==s["source_npcenemy_distinct_positive_skill_ids_primary"]==39
    assert len(ua)==s["source_npcenemy_distinct_positive_skill_ids_alternative"]==39
    assert up==ua
    masterp={r[1] for r in pet["source_rows"]["petskill.txt"]}
    mastera={r[1] for r in pet["source_rows"]["petskill1.txt"]}
    assert sum(i in masterp for i in up)==s["source_npcenemy_skill_id_defined_in_primary_petskill_master"]==39
    assert sum(i in mastera for i in up)==s["source_npcenemy_skill_id_defined_in_alternative_petskill_master"]==39
    shop_ids={r["skill_id"] for r in shop["source_skill_id_master_presence_candidates"]}
    assert len(shop_ids)==shop["summary"]["distinct_skill_IDs"]==23
    same=sorted(up&shop_ids)
    assert same==s["source_npcenemy_skillshop_intersection_IDs"]
    assert len(same)==s["source_npcenemy_39_distinct_skill_ids_overlapping_original_21_skillshop_23_ids"]==19
    given=d["source_O59_existing_two_named_wild_candidates"]
    assert len(given)==len(wild["selected_named_wild_enemy_gates"])==2
    distinct_enemy_ids={e[0] for e in edges}
    for z,w in zip(given,wild["selected_named_wild_enemy_gates"]):
        assert z["source_enemy_id"]==w["source_group_enemy_id"]
        assert z["template_id"]==w["source_enemy_template_no"]
        assert z["source_encounter_group"]==w["source_encounter_group_id"]
        assert z["instance_PETFLG"]==w["source_instance_ENEMY_PETFLG"]==1
        assert z["template_PETFLG"]==w["source_template_E_T_PETFLG"]==1
        assert z["source_template_GET_modifier"]==w["source_template_E_T_GET"]
        assert z["source_primary_template_SHA256"]==tp[z["template_id"]][16]
        assert z["source_alternative_template_SHA256"]==ta[z["template_id"]][16]
        assert z["primary_alt_published_numeric_core_equal"]==(tp[z["template_id"]][1:16]==ta[z["template_id"]][1:16])
        assert z["already_documented_O59_not_new_wild_encounter"] is True
        assert z["source_enemy_id"] not in distinct_enemy_ids
    assert s["source_O59_wild_candidates_outside_NPCEnemy_enemy_instance_cohort"]==2
    limits=d["source_limits"]
    for k in [
        "source_GetPet_literal_file_line_directly_replayed_in_private_original_NPC_source",
        "source_GetPet_may_be_grant_not_caught_wild_but_actual_runtime_operation_unknown",
        "source_NPCEnemy_template_PETFLG_does_not_prove_instance_PETFLG_or_capture_eligibility",
        "source_template_skills_having_definition_does_not_prove_skill_execution",
        "source_O59_wild_existing_does_not_prove_this_GETPET_or_NPCEnemy_cohort_capturable"]:
        assert limits[k] is True
    for k in [
        "source_GetPet_ID_number_namespace_proven_same_as_enemybase_template",
        "source_GetPet_script_executed_or_pet_granted","source_CHANGE_EVENT_direct_file_ref_proves_npc_execution",
        "source_backup_scripts_assumed_active","source_npcenemy_instance_raw_flag_fields_present_in_published_char09",
        "source_alternative_enemybase_selected_in_running_server",
        "source_gametime_catch_probability_proven","source_official_early_build_equivalence",
        "source_skill_shop_definition_or_numeric_intersection_proves_pets_trained_or_learned",
        "source_original_private_dialogue_binaries_or_images_published"]:
        assert limits[k] is False
    assert limits["stage_A"]=="7_PARTIAL_2_OPEN"
    assert limits["stage_B_and_wiki"]=="GATED" and limits["R79"]=="PAUSED_NON_BLOCKING"
    assert limits["overall_percent"] is None
    assert d["next"].startswith("INTEGRATION-MODULE-01")
    return True

class TestGameplay07(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(D.read_text(encoding="utf-8"))
        cls.c=json.loads(CHAR01.read_text(encoding="utf-8"))
        cls.n=json.loads(CHAR09.read_text(encoding="utf-8"))
        cls.pet=json.loads(PET10.read_text(encoding="utf-8"))
        cls.wild=json.loads(O59.read_text(encoding="utf-8"))
        cls.shop=json.loads(SHOP03.read_text(encoding="utf-8"))
    def test_source_relationships(self):
        self.assertTrue(verify(self.d,self.c,self.n,self.pet,self.wild,self.shop))
    def reject(self,modify):
        d=deepcopy(self.d);modify(d)
        with self.assertRaises((AssertionError,KeyError,IndexError,TypeError)):
            verify(d,self.c,self.n,self.pet,self.wild,self.shop)
    def test_getpet_source_file_sha_mismatch_rejected(self):
        self.reject(lambda d:d["source_GetPet_original_NPC_files"][0].__setitem__("source_sha256","0"*64))
    def test_getpet_backup_not_promoted(self):
        self.reject(lambda d:next(x for x in d["source_GetPet_original_NPC_files"] if x["original_source_relative_path"]=="quiz/equiz_04.BAK").__setitem__("source_status","PRIMARY_PATH_NOT_PROVEN_DEPLOYED"))
    def test_silent_changeevent_execution_promoted_rejected(self):
        self.reject(lambda d:d["source_limits"].__setitem__("source_CHANGE_EVENT_direct_file_ref_proves_npc_execution",True))
    def test_getpet_integer_namespace_assumption_rejected(self):
        self.reject(lambda d:d["source_limits"].__setitem__("source_GetPet_ID_number_namespace_proven_same_as_enemybase_template",True))
    def test_variant_template_651_skill_rewrite_rejected(self):
        self.reject(lambda d:next(x for x in d["source_NPCEnemy_distinct_original_template_pairs"] if x["template_id"]==651).__setitem__("alternate_seven_skill_slot_literals",[0,None,None,None,None,None,None]))
    def test_wrong_instance_template_reference_rejected(self):
        self.reject(lambda d:d["source_NPCEnemy_enemy_instance_to_template_numeric_IDs"][0].__setitem__(1,999999))
    def test_false_skill_learn_proof_rejected(self):
        self.reject(lambda d:d["source_limits"].__setitem__("source_skill_shop_definition_or_numeric_intersection_proves_pets_trained_or_learned",True))
    def test_false_official_deployment_rejected(self):
        self.reject(lambda d:d["source_limits"].__setitem__("source_official_early_build_equivalence",True))
if __name__=="__main__":unittest.main()
