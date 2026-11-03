"""GAMEPLAY04 source-derived metadata checks. CI does not execute or bundle original binaries."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]/"research"/"recovered"
NEW=ROOT/"STONEAGE-GAMEPLAY04-TW10-NATIVE-SAB-LOADER-SOURCE-R1.json"
OLD16=ROOT/"STONEAGE-O16-TW10-BATTLE-NATIVE-PALETTE-INTERLEAVE-R1.json"
OLD40=ROOT/"STONEAGE-O40-TW10-NATIVE-BATTLE-PATH-SOURCE-R1.json"

def verify(d,o16,o40):
    assert d["schema"]=="stoneage.gameplay_mechanics_module04_tw10_native_battle_sab_loader_static_callsite.r1"
    src=d["source"]; exe=d["native_loader"]; sab=d["original_battle_SAB_replay"]
    assert src["scope"]=="PRESERVED_AUTHENTICATED_TW10_CLIENT_STATIC_DISASSEMBLY_NOT_ORIGINAL_GAME_EXECUTION"
    assert src["original_private_P3H_zip_bytes"]==o16["original_source"]["archive_bytes"]==372626292
    assert src["original_private_P3H_zip_sha256"]==o16["original_source"]["archive_sha256"]
    assert src["game_binary_sha256"]==o40["native_game_executable"]["sha256"]
    assert src["game_binary_bytes"]==o40["native_game_executable"]["bytes"]==425984
    assert src["actual_zip_member_CRC_all_379_valid"] is True
    assert src["earlier_O16_218_original_sab_source_blob"]=="7266f87fe38ca4f4caa886f30bf577957bb59662"
    assert src["earlier_O40_native_literal_static_join_blob"]=="788f31e97b52ec6b07f2747d7a1665083513dad8"
    assert src["earlier_O40_open_file_callsite_resolved_before_this_work"] is False
    assert o40["native_game_executable"]["actual_open_file_call_for_each_literal_traced"] is False
    assert src["original_binary_or_server_launched_this_unit"] is False
    assert exe["address"]=="0x00401260"
    assert (exe["code_file_offset_begin"],exe["code_file_offset_end_exclusive"],exe["native_code_bytes"])==(0x1260,0x13df,383)
    assert exe["static_code_sha256"]=="93969b92f21b728ae59cc5a6e8fa166c541d40c1761fcc2e434d39ca32c09ce9"
    assert exe["callsites"]==["0x00404a67","0x00404c22","0x0040d34e","0x0041ca62","0x0041cc94","0x0041ce23","0x0041cf63","0x0041d0f4"]
    assert exe["eight_calls_static_rel32_target_verified"] is True
    assert exe["path_pointer_table_va"]=="0x00454070"
    assert exe["path_pointer_table_file_offset"]==0x54070
    assert exe["table_entries"]*exe["table_pointer_stride_bytes"]==exe["table_bytes"]==872
    assert exe["table_sha256"]=="5fedbc3e503d4ade32bb9ad60a51d446f366e568ce4a64eac8d8e7ba9b054b71"
    assert exe["path_pointer_table_va"]=="0x00454070"
    assert exe["source_path_template"]==r"data\battleMap\battleNN.sab"
    assert exe["file_open_mode_source_literal"]=="rb"
    assert exe["open_file_failure_message_box_and_returns_zero"] is True
    assert exe["source_header_token_to_search"]=="SAB"\n    assert exe["native_header_search_function_va"]=="0x004485e0"\n    assert exe["source_header_search_is_substring_function_not_strict_header_comparison"] is True
    assert exe["original_read_four_bytes_then_terminate_at_offset_four"] is True
    assert exe["malformed_header_warning_branch_aborts_processing"] is False
    assert exe["index_ge_218_normalizes_to_0_in_this_entry"] is True
    assert exe["index_negative_explicitly_guarded_in_this_entry"] is False
    assert exe["source_400_word_read_low_then_high_bytes"] is True
    assert exe["source_tile_words_per_row"]*exe["source_tile_rows"]==400
    assert (exe["integer_render_loop_step_x"],exe["integer_render_loop_step_y"])==(32,24)
    assert exe["source_400_per_cell_dispatch_target_va"]=="0x004407a0"
    assert exe["static_loader_success_result_one_on_post_open_path"] is True
    second=d["secondary_native_render_branch"]
    assert second["address"]=="0x004013e0"
    assert second["inclusive_integer_gate_for_distinct_branch"]==[148,150]
    assert second["actual_original_visual_effect_or_battle_rule_verified"] is False
    assert sab["actual_source_files_reopened_and_crc_valid"]==218
    assert sab["native_pointer_paths_case_sensitive_match_zip_members"]==0
    assert sab["native_pointer_paths_casefold_match_zip_members"]==218
    assert (sab["source_file_bytes_each"],sab["source_words_after_header_per_file"])==(804,400)
    assert sab["native_source_header_hex"]=="53414220"
    assert sab["original_source_header_first_three_ASCII"]=="SAB"
    assert sab["total_source_word_occurrences"]==87200
    old=o16["source_bitmap_coverage"]
    assert (sab["distinct_numeric_word_values"],sab["unique_original_source_file_sha256"])==(
        old["distinct_original_bitmap_ids_in_218_sabs"],old["distinct_original_sab_SHA256"])
    assert sab["already_known_duplicate_content_file_ids"]==old["duplicate_index_group"]
    assert sab["previous_O16_sab_total_and_duplicate_not_new_historical_findings"] is True
    records=o16["battle_sab_records"]
    assert len(records)==218 and [r["id"] for r in records]==list(range(218))
    ordered="".join(f'{r["id"]}:{r["sha256"]}\n' for r in records)
    assert hashlib.sha256(ordered.encode("ascii")).hexdigest()==sab["original_source_sab_ids_sha256_in_order_digest"]
    for i,digest in sab["illustrative_exact_raw_sab_sha256"]:
        assert records[i]["sha256"]==digest
    b=d["source_evidence_limits"]
    assert b["proven"]=="STATIC_COMPILED_CLIENT_FUNCTION_LINKED_TO_ALL_218_ARCHIVED_SAB_MEMBER_BYTES"
    assert b["commercial_client_file_io_executed"] is False
    assert b["live_client_battle_world_entered"] is False
    assert b["battle_encounter_event_to_sab_id_rule_recovered"] is False
    assert b["native_palette_and_tile_visuals_replayed_this_unit"] is False
    assert b["commercial_battle_skill_callback_executed"] is False
    assert b["JSS1999_or_CN182_identical_behavior_proven"] is False
    assert b["original_game_assets_or_binary_in_public_git"] is False
    assert b["stage_A"]=="7_PARTIAL_2_OPEN" and b["overall_percent"] is None
    assert d["next"].startswith("GAMEPLAY-MECHANICS-MODULE-05")
    return True

class TestNativeSABProvenance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(NEW.read_text("utf-8"))
        cls.o16=json.loads(OLD16.read_text("utf-8"))
        cls.o40=json.loads(OLD40.read_text("utf-8"))
    def test_loader_and_218_source_ref_integrity(self):
        self.assertTrue(verify(self.d,self.o16,self.o40))
    def reject(self,action):
        d=deepcopy(self.d);action(d)
        with self.assertRaises((AssertionError,KeyError,TypeError)):
            verify(d,self.o16,self.o40)
    def test_false_native_execution_rejected(self):
        self.reject(lambda d:d["source_evidence_limits"].__setitem__("commercial_client_file_io_executed",True))
    def test_wrong_header_rejected(self):
        self.reject(lambda d:d["original_battle_SAB_replay"].__setitem__("native_source_header_hex","53414200"))
    def test_wrong_native_caller_rejected(self):
        self.reject(lambda d:d["native_loader"]["callsites"].__setitem__(0,"0x00404a66"))
    def test_wrong_original_source_sha_rejected(self):
        self.reject(lambda d:d["original_battle_SAB_replay"]["illustrative_exact_raw_sab_sha256"][0].__setitem__(1,"0"*64))
    def test_wrong_special_branch_rejected(self):
        self.reject(lambda d:d["secondary_native_render_branch"].__setitem__("inclusive_integer_gate_for_distinct_branch",[0,217]))
    def test_false_gameplay_selector_rejected(self):
        self.reject(lambda d:d["source_evidence_limits"].__setitem__("battle_encounter_event_to_sab_id_rule_recovered",True))
    def test_218_to_217_content_group_dedup_rejected(self):
        self.reject(lambda d:d["original_battle_SAB_replay"].__setitem__("unique_original_source_file_sha256",218))

if __name__=="__main__":unittest.main()
