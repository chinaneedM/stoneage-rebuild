"""WORLD19 original item-use source joins; public CI never executes or reads private commercial binaries."""
import copy
import json
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/"research"/"recovered"
REPORT=REC/"STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-19-ITEM-USE-HANDLERS-R1.json"
ITEM01=REC/"STONEAGE-ITEM-EQUIPMENT-SHOP-MODULE-01-TWO-ORIGINAL-ITEMSETS-AND-TW1-RD-SUMMARY-R1.json"
WORLD18=REC/"STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-18-BATTLE-ENTRY-BGM-SOURCE-R1.json"
SHARDS=[REC/"item-module-01"/f"STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{i:02d}-R1.json" for i in range(1,8)]
HEX=re.compile(r"^[0-9a-f]{64}$")


def verify(d):
    assert d["schema"]=="stoneage.stage_a.world19.item_use_handlers.r1"
    s,c=d["source"],d["census"]
    assert s["carrier"]=="community_mixed25_saved_not_official_clean"
    assert (s["archive_bytes"],s["rar_member_count"])==(361255180,7952)
    assert HEX.fullmatch(s["archive_sha256"]) and HEX.fullmatch(s["private_ITEM01_zip_sha256"])
    assert s["all_original_CP950_94column_rows_reverified"] is True
    assert s["zero_based_fields"]=={"id":16,"argument":3,"handler":10,"type":19,"fieldtype":20,"target":21,"useaction":77}
    assert (s["A"]["rows"],s["B"]["rows"])==(13254,13915)
    assert all(HEX.fullmatch(s[k]["sha256"]) for k in ("A","B"))
    assert (c["ids_A"],c["ids_B"],c["shared_ids"],c["B_only_ids"])==(13254,13915,13254,661)
    assert c["shared_handler_unchanged"] is True
    assert (c["handler_rows_A"],c["handler_rows_B"],c["distinct_handlers_A"],c["distinct_handlers_B"],c["new_ids_with_handler"])==(958,1082,52,59,124)
    h=d["handlers"]
    assert len(h)==59 and len(set(x[0] for x in h))==59
    assert h==sorted(h,key=lambda x:x[0])
    assert all(len(x)==3 and x[0].startswith("ITEM_") and 0<=x[1]<=x[2] for x in h)
    assert (sum(x[1] for x in h),sum(x[2] for x in h))==(958,1082)
    assert sum(bool(x[1]) for x in h)==52
    fn={x[0]:(x[1],x[2]) for x in h}
    assert fn["ITEM_useRecovery"]==(644,663)
    assert fn["ITEM_useWarp"]==(37,38) and fn["ITEM_useWarpForNum"]==(5,5)
    assert fn["ITEM_useCaptureUp"]==(26,26) and fn["ITEM_useLearnRideCode"]==(0,16)
    assert fn["ITEM_BattlePK"]==(2,2)
    assert c["useaction_B"]=={"-1":13719,"4":1,"5":1,"6":70,"7":38,"11":86}
    assert sum(c["useaction_B"].values())==13915
    assert c["useaction_nonnegative_without_handler"]==[1480]
    w=d["witnesses"]
    assert len(w)==16 and len(set(x[0] for x in w))==16
    for row in w:
        assert len(row)==5
        i,handler,sha_b,sha_a,action=row
        assert isinstance(i,int) and i>=0
        assert handler is None or handler in fn
        assert HEX.fullmatch(sha_b)
        assert sha_a is None or HEX.fullmatch(sha_a)
        assert action in c["useaction_B"]
    wi={x[0]:x for x in w}
    assert wi[20811][1]==wi[20898][1]=="ITEM_BattlePK"
    assert wi[20811][4]==wi[20898][4]=="-1"
    assert wi[19005][1]==wi[19008][1]=="ITEM_useLearnRideCode"
    assert wi[19005][3] is None and wi[19008][3] is None
    assert wi[1480][1] is None and wi[1480][4]=="7"
    assert all(wi[x][1]=="ITEM_useRecovery" for x in (1230,12530,12555,12500,12823,18545))
    args=d["special_source_arguments"]
    assert args["warp_item_1345"]["raw_space_separated_numeric_cells"]==[0,1000,92,99]
    assert args["warp_item_13041"]["raw_space_separated_numeric_cells"]==[1,1000,92,99]
    assert args["ride_item_19005"]["literal_token"]=="RIDE_PET9"
    ex=d["partial_executable"]
    assert ex["this_attempt_member_read_failed_crc"] is True
    assert ex["whole_member_reverified_this_time"] is False
    assert (ex["this_attempt_prefix_bytes"],ex["previous_WORLD18_complete_member_bytes"])==(1835008,1897867)
    assert all(HEX.fullmatch(ex[x]) for x in ("previous_WORLD18_complete_member_sha256","this_attempt_prefix_sha256"))
    assert ex["bounded_40byte_name_records_observed"]==75
    assert (ex["B_handler_names_seen_in_unqualified_prefix"],ex["B_handler_names_not_seen_in_unqualified_prefix"])==(47,12)
    assert ex["prefix_selected_symbols"]["ITEM_BattlePK"]["observed_va"]>0x400000
    assert ex["prefix_selected_symbols"]["ITEM_useLearnRideCode"] is None
    assert ex["missing_from_prefix_does_not_prove_missing_in_full_exe"] is True
    bridge=d["world18_bridge"]
    assert bridge["source_table"]=="B" and bridge["item_ids"]==[20811,20898]
    assert bridge["both_handler_token"]=="ITEM_BattlePK"
    assert bridge["world18_downstream_function"]=="BATTLE_CreateVsPlayer"
    assert bridge["world18_EN_success_type"]==2 and bridge["world18_client_entry_track_slot"]==6
    assert bridge["world18_client_entry_audio_path"]=="data/bgm/sabgm_b1.wav"
    assert bridge["source_item_handler_to_compiled_function_link_certified"] is False
    assert bridge["native_item_trigger_and_audio_playback_executed"] is False
    b=d["boundaries"]
    assert b["stage_A"]=="7_PARTIAL_2_OPEN" and b["stage_B_wiki"]=="GATED"
    assert b["R79"]=="PAUSED_NON_BLOCKING" and b["overall_percent"] is None
    assert b["primary_handler_token_is_original_static_configuration_not_proven_runtime_dispatch"] is True
    assert b["useaction_animation_code_not_same_as_function_dispatch_field"] is True
    for k in ("itemset0710_filename_proves_operating_date","official_TW1_server_item_table_identity_proven","community_mixed25_sourced_as_pure_original_official_release","original_client_or_server_executed","original_full_exe_verified_in_this_turn","original_proprietary_text_art_or_binary_published"):
        assert b[k] is False
    assert d["next"]=="STAGE-A-OFFLINE-WORLD-CONTENT-20_SOURCE_BOUND_ROTATION"
    return True


class World19SourceAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=json.loads(REPORT.read_text(encoding="utf-8"))

    def test_source_derived_census(self):self.assertTrue(verify(self.data))

    def test_item01_original_id_and_row_sha_link(self):
        self.assertTrue(ITEM01.exists() and all(x.exists() for x in SHARDS))
        src=self.data["source"]
        prev=json.loads(ITEM01.read_text(encoding="utf-8"))["provenance"]
        self.assertEqual(prev["mixed25_community_RAR_sha256"],src["archive_sha256"])
        self.assertEqual(prev["itemset_a"]["sha256"],src["A"]["sha256"])
        self.assertEqual(prev["itemset_b"]["sha256"],src["B"]["sha256"])
        rows={x[0]:x for path in SHARDS for x in json.loads(path.read_text(encoding="utf-8"))["rows"]}
        self.assertEqual(len(rows),13915)
        for id,fn,sha_b,sha_a,action in self.data["witnesses"]:
            with self.subTest(id=id):
                self.assertEqual(rows[id][1],sha_a)
                self.assertEqual(rows[id][2],sha_b)

    def test_world18_same_carrier_player_battle_chain(self):
        parent=json.loads(WORLD18.read_text(encoding="utf-8"))
        b=self.data["world18_bridge"];ex=self.data["partial_executable"]
        self.assertEqual(parent["mixed25_server"]["exe_sha256"],ex["previous_WORLD18_complete_member_sha256"])
        path=next(x for x in parent["mixed25_server"]["positive_source_paths"] if x["symbol"]=="BATTLE_CreateVsPlayer")
        self.assertEqual(path["result"],b["world18_EN_success_type"])
        self.assertIn("ITEM_BattlePK",path["named_incoming_paths"])
        client=next(x for x in parent["client_positive_result_witnesses"] if x["result"]==2)
        self.assertEqual(client["entry_slot_after_this_update"],b["world18_client_entry_track_slot"])
        self.assertEqual(parent["slots"][str(client["entry_slot_after_this_update"])],b["world18_client_entry_audio_path"])

    def test_reject_crc_failure_concealment(self):
        x=copy.deepcopy(self.data);x["partial_executable"]["whole_member_reverified_this_time"]=True
        with self.assertRaises(AssertionError):verify(x)
    def test_reject_native_playback_invention(self):
        x=copy.deepcopy(self.data);x["world18_bridge"]["native_item_trigger_and_audio_playback_executed"]=True
        with self.assertRaises(AssertionError):verify(x)
    def test_reject_wrong_handler_column(self):
        x=copy.deepcopy(self.data);x["source"]["zero_based_fields"]["handler"]=77
        with self.assertRaises(AssertionError):verify(x)
    def test_reject_count_fabrication(self):
        x=copy.deepcopy(self.data);x["handlers"][0][2]+=1
        with self.assertRaises(AssertionError):verify(x)
    def test_reject_false_older_riding_record(self):
        x=copy.deepcopy(self.data);next(r for r in x["witnesses"] if r[0]==19005)[3]="0"*64
        with self.assertRaises(AssertionError):verify(x)
    def test_reject_wrong_world18_track(self):
        x=copy.deepcopy(self.data);x["world18_bridge"]["world18_client_entry_audio_path"]="data/bgm/sabgm_b0.wav"
        with self.assertRaises(AssertionError):verify(x)
    def test_reject_official_early_server_claim(self):
        x=copy.deepcopy(self.data);x["boundaries"]["official_TW1_server_item_table_identity_proven"]=True
        with self.assertRaises(AssertionError):verify(x)


if __name__=="__main__":unittest.main()
