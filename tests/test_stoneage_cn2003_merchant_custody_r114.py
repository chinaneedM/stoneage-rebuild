import copy
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from verify_stoneage_cn2003_merchant_custody_r114 import validate
D=json.loads((ROOT/"research/recovered/STONEAGE-CN2003-MERCHANT-ELEPHANT-ACCEPTANCE-R114.json").read_text(encoding="utf-8"))

class CustodyBoundary(unittest.TestCase):
    def bad(self,mutation):
        x=copy.deepcopy(D);mutation(x)
        with self.assertRaises((AssertionError,KeyError,TypeError,ValueError)):validate(x)
    def test_valid(self):self.assertTrue(validate(D))
    def test_bad_tree(self):self.bad(lambda x:x.update(content_tree="a"*40))
    def test_bad_previous_head(self):self.bad(lambda x:x.update(previous_main_head="b"*40))
    def test_wrong_file(self):self.bad(lambda x:x["nine_files"][0].update(blob_sha="c"*40))
    def test_missing_history(self):self.bad(lambda x:x["nine_files"][1].update(existing_historical_prefix_blob=None))
    def test_missing_file(self):self.bad(lambda x:x["nine_files"].pop())
    def test_duplicate_candidate_run(self):self.bad(lambda x:x["candidate_continuity_actions"].append(x["candidate_continuity_actions"][0]))
    def test_failed_main_action(self):self.bad(lambda x:x["main_content_actions"][0].update(conclusion="failure"))
    def test_wrong_main_branch(self):self.bad(lambda x:x["main_content_actions"][0].update(head_branch="main2"))
    def test_fake_source_hash(self):self.bad(lambda x:x["provenance_limit"].update(original_2003_html_sha256="fake"))
    def test_fake_original_execution(self):self.bad(lambda x:x["provenance_limit"].update(original_server_execution_proof="pass"))
    def test_claim_original_entities(self):self.bad(lambda x:x["provenance_limit"].update(original_game_entity_count_newly_recovered=3))
    def test_not_append_only(self):self.bad(lambda x:x.update(all_previous_historical_prefixes_byte_preserved=False))
if __name__=="__main__":unittest.main()
