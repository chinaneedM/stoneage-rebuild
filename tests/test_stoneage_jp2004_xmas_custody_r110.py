import copy, importlib.util, json, unittest
from pathlib import Path
r=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("custody",r/"tools/stoneage_jp2004_xmas_custody_r110.py")
custody=importlib.util.module_from_spec(spec);spec.loader.exec_module(custody)
orig=json.loads(custody.PATH.read_text(encoding="utf-8"))
class TestCustodyR110(unittest.TestCase):
    def test_real(self): self.assertTrue(custody.verify(copy.deepcopy(orig),True))
    def rejected(self,alter):
        d=copy.deepcopy(orig);alter(d)
        with self.assertRaises((AssertionError,KeyError,TypeError)):
            custody.verify(d)
    def test_fake_source_hash(self):
        self.rejected(lambda d:d["source_provenance"].__setitem__("original_html_raw_sha256","f"*64))
    def test_false_first_party_capture(self):
        self.rejected(lambda d:d["source_provenance"].__setitem__("operator_page_retrieved",True))
    def test_fake_artifact_zip(self):
        self.rejected(lambda d:d["artifact_custody"].__setitem__("source_artifact_zip_sha256","fake"))
    def test_tamper_file_sha(self):
        self.rejected(lambda d:d["content_files_git_blob_sha"].__setitem__("docs/CURRENT-STATE.md","f"*40))
    def test_run_count(self):
        self.rejected(lambda d:d["main_content_suite"].__setitem__("run_count",13))
    def test_rewrite_run(self):
        self.rejected(lambda d:d["candidate_latest_commit_suite"]["run_ids"].__setitem__(0,7))
    def test_false_web_replay(self):
        self.rejected(lambda d:d["source_provenance"].__setitem__("source_replay_performed",True))
    def test_fake_historical_complete(self):
        self.rejected(lambda d:d["historical_status"].__setitem__("restoration_percent",100))
if __name__=="__main__":unittest.main()
