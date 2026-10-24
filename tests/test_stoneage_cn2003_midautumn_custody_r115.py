#!/usr/bin/env python3
import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from verify_stoneage_cn2003_midautumn_custody_r115 import validate
D=json.loads((ROOT/"research/recovered/STONEAGE-CN2003-MIDAUTUMN-CUSTODY-R115.json").read_text(encoding="utf-8"))
class TestR115Custody(unittest.TestCase):
    def bad(self,fn):
        d=copy.deepcopy(D);fn(d)
        with self.assertRaises((AssertionError,KeyError,ValueError)):validate(d)
    def test_valid(self): self.assertTrue(validate(D))
    def test_wrong_head(self):self.bad(lambda d:d.update(candidate_final_commit_and_main_head="fake"))
    def test_wrong_tree(self):self.bad(lambda d:d.update(candidate_final_tree_and_main_tree="fake"))
    def test_old_prefix_size(self):self.bad(lambda d:d["preserved_original_docs"]["docs/CURRENT-STATE.md"].update(bytes=1))
    def test_blob_mutation(self):self.bad(lambda d:d["versioned_github_git_blobs"].update({"docs/CURRENT-STATE.md":"0"*40}))
    def test_fake_original_source_hash(self):self.bad(lambda d:d["source_provenance"].update(original_2003_website_html_sha256="fake"))
    def test_fake_website_archive(self):self.bad(lambda d:d["source_provenance"].update(historical_web_html_bytes_archived=True))
    def test_wrong_derived_sha(self):self.bad(lambda d:d["derived_report_provenance"].update(json_sha256="wrong"))
    def test_skip_ci(self):self.bad(lambda d:d["derived_report_provenance"]["main_workflow_runs"].pop())
    def test_reused_ci(self):self.bad(lambda d:d["derived_report_provenance"]["candidate_final_workflow_runs"].__setitem__(0,D["derived_report_provenance"]["main_workflow_runs"][0]))
    def test_fake_runtime(self):self.bad(lambda d:d["derived_report_provenance"].update(original_server_script_replayed=True))
    def test_research_not_original_npcs(self):self.bad(lambda d:d["scope_guards"].update(narrative_characters_not_validated_original_npcs=False))
    def test_not_completion_percent(self):self.bad(lambda d:d["scope_guards"].update(overall_restoration_percentage=100))
if __name__=="__main__":unittest.main()
