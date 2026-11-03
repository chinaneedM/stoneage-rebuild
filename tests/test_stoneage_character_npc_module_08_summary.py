"""CHAR08: public bounded source ledger acceptance, not source-binary runtime replay."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"research/recovered"
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def verify(s, earlier, char07):
    assert s["schema"]=="stoneage.character_npc_module08_original_static_exchange_receipt.r1"
    a=s["rar"];b=s["bounds"]
    assert a["sha256"]==earlier["original_private_RAR_sha256"]==char07["source_original_RAR_sha256"]
    assert (a["archive_members"],a["npc_original_files_reextracted"],a["npc_source_bytes"],a["prior_CHAR07_files_sha_checked"])==(7952,2205,1930332,552)
    assert earlier["counts"]["create_blocks"]==s["create_blocks_all"]==4985
    assert earlier["functionset_source_occurrences"]["ExChangeMan"]==s["create_blocks_ExChangeMan"]==315
    assert s["distinct_script_paths"]==295 and s["missing_script_files"]==0
    assert s["distinct_script_bytes"]==434873
    x=s["script_syntax"]
    assert x["TYPE_values"]=={"MESSAGE":769,"ACCEPT":494,"REQUEST":81,"CLEAN":5}
    assert sum(x["TYPE_values"].values())==x["TYPE"]==1349
    assert (x["EventNo"],x["EVENT"],x["EventEnd"],x["GetItem_lines"],x["DelItem_lines"])==(1348,1349,1347,420,442)
    assert (x["unparsed_EVENT_segments"],x["unparsed_item_op_slots"])==(1702,11)
    i=s["items"];p=i["candidate_1"];q=i["candidate_2"]
    assert p["distinct_ids"]==13254 and q["distinct_ids"]==13915
    assert i["id_column_zero_based"]==16 and i["image_number_column_zero_based"]==17
    assert i["common_ids"]==13254 and i["extra_in_candidate_2"]==661
    assert i["common_id_row_sha_equal"]==4303 and i["common_id_row_sha_different"]==8951
    assert i["script_numeric_item_occurrences"]==2878 and i["script_distinct_numeric_item_ids"]==380
    assert i["script_ids_both_same_row_sha"]==372 and i["script_ids_both_different_row_sha"]==[18340]
    assert i["script_ids_only_candidate_2"]==[2054,2391,20570,20571,20572]
    assert i["script_ids_absent_both"]==[2744,2745]
    assert s["private_full_derived_index"]["published_in_this_git_commit"] is False
    assert s["private_full_derived_index"]["bytes"]==338200 and s["private_full_derived_index"]["local_tests_passed"]==12
    assert b["official_TW1_server"] is False and b["runtime_executed"] is False
    assert b["quest_origin"]=="ORIGIN_UNRESOLVED" and b["all_315_origins_unresolved"] is True
    assert b["overall_percent"] is None and b["stage_B"]=="GATED" and b["wiki"]=="GATED"
    assert char07["total_original_source_ref_rows_file_present"]==552
    return True
class TestCHAR08(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=load("STONEAGE-CHARACTER-NPC-MODULE-08-STATIC-SOURCE-SUMMARY-R1.json")
        cls.old=load("STONEAGE-CHARACTER-NPC-MODULE-04-SAME-CARRIER-GRAPHIC-FUNCTION-JOIN-R1.json")
        cls.char07=load("STONEAGE-CHARACTER-NPC-MODULE-07-TOWNPEOPLE-SIGNBOARD-SOURCE-CATALOG-R1.json")
    def test_replay(self):self.assertTrue(verify(self.d,self.old,self.char07))
    def test_never_promote_original(self):
        import copy
        d=copy.deepcopy(self.d);d["bounds"]["official_TW1_server"]=True
        with self.assertRaises(AssertionError):verify(d,self.old,self.char07)
    def test_never_claim_complete_full_directory_uploaded(self):
        import copy
        d=copy.deepcopy(self.d);d["private_full_derived_index"]["published_in_this_git_commit"]=True
        with self.assertRaises(AssertionError):verify(d,self.old,self.char07)
    def test_reject_wrong_item_identifier_column(self):
        import copy
        d=copy.deepcopy(self.d);d["items"]["id_column_zero_based"]=17
        with self.assertRaises(AssertionError):verify(d,self.old,self.char07)
    def test_reject_new_game_completion(self):
        import copy
        d=copy.deepcopy(self.d);d["bounds"]["overall_percent"]=100
        with self.assertRaises(AssertionError):verify(d,self.old,self.char07)
if __name__=="__main__":unittest.main()
