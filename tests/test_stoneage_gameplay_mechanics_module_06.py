"""GAMEPLAY06 derived source-only contract. Public CI does not bundle original NPC bytes."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import unittest

RECOVERED=Path(__file__).resolve().parents[1]/"research"/"recovered"
META=RECOVERED/"STONEAGE-GAMEPLAY06-ORIGINAL-TRANSPORT-WINDOW-AND-ITEMPOOL-SOURCE-R1.json"
CHAR=RECOVERED/"STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json"
FAMILIES={"airplane":5,"bankman":8,"bus":7,"duelranking":8,
          "npcgen_poolitemshop":5,"transman":7,"windowman":17}

def verify(d,c):
    assert d["schema"]=="stoneage.gameplay_mechanics_module06_preserved_transit_window_original_source.r1"
    assert d["source_scope"]=="COMMUNITY_PRESERVED_MIXED25_NPC_BYTE_SOURCE_ONLY_NOT_AUTHENTICATED_OFFICIAL_SERVER"
    assert d["original_private_npc_zip_sha256"]=="c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f"
    assert (d["original_private_npc_zip_bytes"],d["original_npc_archive_file_count"],
            d["original_npc_archive_uncompressed_bytes"])==(995176,2205,1930332)
    assert (c["npc_subtree_source_files"],c["npc_subtree_source_bytes"])==(2205,1930332)
    assert d["original_char01_manifest_git_blob"]=="a088b61a3212f7049e7793f587123ffb29bebad7"
    assert d["original_parent_RAR_reopened_this_unit"] is False
    source={r[0]:r for r in c["source_files"]}
    originals={(r[0],r[1]):r for r in c["create_rows"] if r[11] in FAMILIES}
    assert len(originals)==57
    s=d["summary"]
    params=d["original_parameter_source_receipts"]
    assert len(params)==s["source_param_distinct_referenced"]==29
    assert len({r["source_parameter_path"] for r in params})==29
    receipts={r["source_parameter_path"]:r for r in params}
    missing=[]
    for r in params:
        path=r["source_parameter_path"]
        if r["source_status"]=="ORIGINAL_FILE_VERIFIED":
            assert path in source
            sr=source[path]
            assert (r["source_member_bytes"],r["source_member_sha256"],r["source_member_crc32"])==tuple(sr[1:4])
            assert r["original_derived_numeric"] is not None
        else:
            assert r["source_status"]=="MISSING_IN_CURRENT_ORIGINAL_NPC_ARCHIVE"
            assert path not in source
            assert r["source_member_bytes"] is None and r["source_member_sha256"] is None
            assert r["source_member_crc32"] is None and r["original_derived_numeric"] is None
            missing.append(path)
    assert missing==[s["source_missing_conf_path"]]==["sainasu/jujutu01.conf"]
    assert len(params)-len(missing)==s["source_parameter_original_file_count"]==28
    assert sum(r["source_member_bytes"] or 0 for r in params)==s["source_parameter_actual_total_bytes"]==27840
    bykind=Counter(); created=Counter();seen=set(); misses=0
    for r in d["original_CREATE_refs"]:
        key=(r["source_CREATE_path"],r["source_CREATE_ordinal"])
        assert key not in seen and key in originals
        seen.add(key)
        orig=originals[key];kind=r["source_argument_token_kind"]
        assert (r["source_CREATE_block_sha256"],r["source_floorid_integer"],r["source_graphic_integer"])==(orig[4],orig[5],orig[6])
        assert r["source_FUNCTION_literal"]==orig[11] and orig[11] in FAMILIES
        assert r["source_argument_SHA256"]==orig[14]
        path=r["source_parameter_path"]
        if kind=="FILE_TOKEN":
            assert r["source_FUNCTION_literal"] in ("bus","transman","airplane","npcgen_poolitemshop")
            assert path in receipts and receipts[path]["source_status"]=="ORIGINAL_FILE_VERIFIED"
            assert orig[15]==[[path,"EXACT_SAME_NPC_SUBTREE_PATH",receipts[path]["source_member_sha256"]]]
        elif kind=="CONFF_TOKEN":
            assert r["source_FUNCTION_literal"] in ("bankman","windowman")
            assert not orig[15] and path in receipts
            assert r["source_parameter_status"]==receipts[path]["source_status"]
            misses+=int(r["source_parameter_status"]=="MISSING_IN_CURRENT_ORIGINAL_NPC_ARCHIVE")
        else:
            assert kind=="NO_FILE_OR_CONFF" and r["source_FUNCTION_literal"]=="duelranking"
            assert not orig[15] and path is None and r["source_parameter_status"] is None
        bykind[kind]+=1;created[orig[11]]+=1
    assert seen==set(originals)
    assert len(d["original_CREATE_refs"])==s["original_CREATE_blocks"]==57
    assert dict(sorted(created.items()))==s["by_function"]==dict(sorted(FAMILIES.items()))
    assert bykind==Counter({"FILE_TOKEN":24,"CONFF_TOKEN":25,"NO_FILE_OR_CONFF":8})
    assert (s["source_file_argument_CREATE_count"],s["source_conff_argument_CREATE_count"],
            s["source_none_argument_CREATE_count"])==(24,25,8)
    assert misses==s["source_windowman_missing_conf_referenced_CREATE_count"]==4
    bus=[];plane=[];trans=[];pool=[];bank=[];window=[]
    bad403=[];bad2403=[];denied_missing=[]
    for r in params:
        p=r["original_derived_numeric"]
        if p is None:continue
        kind=p["source_type"]
        if kind in ("bus","airplane"):
            assert p["original_routenum_literal"]==1
            assert p["original_routeto_count"]>0
            width=2 if kind=="bus" else 3
            assert p["original_coordinate_word_width"]==width
            assert len(p["first_route_word_tuple"])==width
            assert len(p["last_route_word_tuple"])==width
            assert all(isinstance(x,int) and x>=0 for x in p["first_route_word_tuple"]+p["last_route_word_tuple"])
            assert p["original_waittime_literal"]>0 and p["original_needstone_literal"]>=0
            if p["denieditem_original_field_present"]:
                assert p["denieditem_source_includes_numeric_403"] != p["denieditem_source_includes_numeric_2403"]
            else:
                assert not p["denieditem_source_includes_numeric_403"]
                assert not p["denieditem_source_includes_numeric_2403"]
                denied_missing.append(r["source_parameter_path"])
            if p["denieditem_source_includes_numeric_403"]:bad403.append(r["source_parameter_path"])
            if p["denieditem_source_includes_numeric_2403"]:bad2403.append(r["source_parameter_path"])
            (bus if kind=="bus" else plane).append(p)
        elif kind=="transman":
            assert len(p["source_FREE_literals"])==len(p["original_warppoint_triples"])
            assert all(v=="LV>0" for v in p["source_FREE_literals"])
            assert all(len(v)==3 and all(isinstance(a,int) for a in v) for v in p["original_warppoint_triples"])
            assert p["actual_warp_executed"] is False
            trans.append(p)
        elif kind=="npcgen_poolitemshop":
            assert p["original_cost_literal"]==50 and p["original_source_key_count"]==5
            pool.append(p)
        elif kind in ("bankman","windowman"):
            assert p["source_window_IDs"] and len(p["source_window_IDs"])==len(set(p["source_window_IDs"]))
            assert p["actual_window_click_executed"] is False
            if kind=="bankman":
                assert p["source_window_IDs"]==[1]
                assert p["source_bank_referenced_unlisted_window_IDs"]==[5,6]
                assert all(i not in p["source_window_IDs"] for i in [5,6])
                bank.append(p)
            else:
                assert p["source_bank_referenced_unlisted_window_IDs"]==[]
                window.append(p)
        else:
            raise AssertionError("unknown source kind")
    assert len(bus)==s["source_bus_parameter_count"]==7
    assert sum(r["original_routeto_count"] for r in bus)==s["source_bus_route_coordinate_tuples"]==311
    assert sorted(r["original_needstone_literal"] for r in bus)==[0,20,25,30,40,50,50]
    assert len([r for r in bus if r["original_waittime_literal"]==120])==s["source_bus_waittime_literal_120_count"]==1
    assert len([r for r in bus if r["original_waittime_literal"]==180])==s["source_bus_waittime_literal_180_count"]==6
    assert len(plane)==s["source_airplane_parameter_count"]==5
    assert sum(r["original_routeto_count"] for r in plane)==s["source_airplane_route_coordinate_triples"]==61
    assert sorted(r["original_needstone_literal"] for r in plane)==[1000,1000,1000,3000,3000]
    assert sum(r["original_oneway_literal"]==1 for r in plane)==s["source_airplane_oneway_literal_1_count"]==2
    assert len(trans)==s["source_transman_parameter_count"]==3
    assert sum(len(r["original_warppoint_triples"]) for r in trans)==s["source_transman_WARPPOINT_target_triples"]==7
    assert sum(len(r["source_FREE_literals"]) for r in trans)==s["source_transman_FREE_literal_LV_gt_0_count"]==7
    assert s["source_transman_CREATE_count"]==7
    assert len(pool)==s["source_poolitemshop_original_parameter_count"]==4
    assert s["source_poolitemshop_cost_literal_50_file_count"]==4
    assert s["source_poolitemshop_CREATE_count"]==5
    a,b=s["source_duplicate_complete_poolitemshop_file_pair"]
    assert [a,b]==["genout/pis_3009_18_40","genout/pis_4009_15_13"]
    assert receipts[a]["source_member_sha256"]==receipts[b]["source_member_sha256"]
    assert len(bank)==1 and s["source_bankman_CREATE_count"]==8
    assert sum(len(r["source_window_IDs"]) for r in bank)==s["source_bankman_conf_windows_count"]==1
    assert s["source_bankman_conf_references_windows_not_in_same_file"]==[5,6]
    assert len(window)==s["source_windowman_qualifying_original_conf_files"]==8
    assert sum(len(r["source_window_IDs"]) for r in window)==s["source_windowman_actual_conf_winno_count"]==61
    assert s["source_windowman_CREATE_count"]==17 and s["source_duelranking_inline_no_parameter_CREATE_count"]==8
    assert len(bad403)==s["source_transport_denieditem_literal_403_file_count"]==5
    assert len(bad2403)==s["source_transport_denieditem_literal_2403_file_count"]==6
    assert denied_missing==["giiru/banam.arg"]
    assert len(denied_missing)==s["source_transport_missing_denieditem_file_count"]==1
    limits=d["evidence_limits"]
    for k in ("source_bus_airplane_coords_are_config_data_not_observed_movement",
              "all_values_from_original_saved_source_text_not_live_server",
              "same_archive_source_SHA_does_not_prove_all_files_enabled_in_one_server",
              "source_missing_conf_not_recreated",
              "source_403_and_2403_denieditem_values_not_normalized_or_equated"):
        assert limits[k] is True
    for k in ("native_transport_fee_debit_or_wait_seconds_executed",
              "native_transman_warp_or_LV_condition_evaluated",
              "native_poolitemshop_item_storage_or_payment_executed",
              "native_bankman_balance_or_deposit_executed",
              "native_windowman_UI_or_duelranking_display_executed",
              "native_pet_capture_and_battle_callback_executed",
              "official_JSS1999_TW10_CN182_source_equivalence_proven",
              "original_commercial_content_or_assets_in_public_git"):
        assert limits[k] is False
    assert limits["stage_A"]=="7_PARTIAL_2_OPEN"
    assert limits["stage_B_and_wiki"]=="GATED" and limits["R79"]=="PAUSED_NON_BLOCKING"
    assert limits["overall_percent"] is None
    assert d["next"].startswith("GAMEPLAY-MECHANICS-MODULE-07")
    return True

class TestGameplay06(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=json.loads(META.read_text(encoding="utf-8"))
        cls.c=json.loads(CHAR.read_text(encoding="utf-8"))
    def test_entire_original_source_graph(self):
        self.assertTrue(verify(self.e,self.c))
    def reject(self,edit):
        x=deepcopy(self.e)
        edit(x)
        with self.assertRaises((AssertionError,KeyError,TypeError)):
            verify(x,self.c)
    def test_create_block_sha_mismatch_rejected(self):
        self.reject(lambda x:x["original_CREATE_refs"][0].__setitem__("source_CREATE_block_sha256","0"*64))
    def test_false_missing_config_recovery_rejected(self):
        self.reject(lambda x:next(r for r in x["original_parameter_source_receipts"] if r["source_parameter_path"]=="sainasu/jujutu01.conf").__setitem__("source_status","ORIGINAL_FILE_VERIFIED"))
    def test_false_route_coord_rejected(self):
        self.reject(lambda x:next(r for r in x["original_parameter_source_receipts"] if r["source_parameter_path"]=="chatroom/airplane.arg")["original_derived_numeric"].__setitem__("original_routeto_count",999))
    def test_source_403_not_silent_rewrite(self):
        self.reject(lambda x:next(r for r in x["original_parameter_source_receipts"] if r["source_parameter_path"]=="chatroom/bus.arg")["original_derived_numeric"].__setitem__("denieditem_source_includes_numeric_403",False))
    def test_false_native_transport_execution_rejected(self):
        self.reject(lambda x:x["evidence_limits"].__setitem__("native_transman_warp_or_LV_condition_evaluated",True))
    def test_false_bank_execution_rejected(self):
        self.reject(lambda x:x["evidence_limits"].__setitem__("native_bankman_balance_or_deposit_executed",True))
    def test_false_official_build_rejected(self):
        self.reject(lambda x:x["evidence_limits"].__setitem__("official_JSS1999_TW10_CN182_source_equivalence_proven",True))
    def test_wrong_original_source_bytes_rejected(self):
        self.reject(lambda x:next(r for r in x["original_parameter_source_receipts"] if r["source_status"]=="ORIGINAL_FILE_VERIFIED").__setitem__("source_member_sha256","a"*64))
if __name__=="__main__":unittest.main()
