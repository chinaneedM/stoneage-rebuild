import copy
import importlib.util
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("acc",ROOT/"tools/stoneage_cn_dragon_flight_acceptance_r109.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
D=json.loads(mod.PATH.read_text(encoding="utf-8"))
class TestAcceptance(unittest.TestCase):
    def test_actual_pins(self): self.assertTrue(mod.verify(copy.deepcopy(D)))
    def reject(self,edit):
        d=copy.deepcopy(D);edit(d)
        with self.assertRaises((AssertionError,KeyError)): mod.verify(d,check_local=False)
    def test_no_invented_html_sha(self):self.reject(lambda d:d["source_custody"].__setitem__("source_html_sha256","invented"))
    def test_no_raw_capture_claim(self):self.reject(lambda d:d["source_custody"].__setitem__("original_raw_html_retrieved",True))
    def test_no_visual_claim(self):self.reject(lambda d:d["source_custody"].__setitem__("original_image_bytes_retrieved",True))
    def test_no_fake_replay(self):self.reject(lambda d:d["source_custody"].__setitem__("source_byte_replay_performed",True))
    def test_missing_run(self):self.reject(lambda d:d["acceptance"]["candidate_run_ids"].pop())
    def test_fake_job(self):self.reject(lambda d:d["acceptance"].__setitem__("main_dedicated_job_id",1))
    def test_commit_swap(self):self.reject(lambda d:d["research"].__setitem__("candidate_accepted_commit","f"*40))
    def test_prefix_erasure(self):self.reject(lambda d:d["historical_prefix"].__setitem__("preserved",False))
    def test_wrong_blob_pin(self):
        d=copy.deepcopy(D);d["file_pins"][0]["git_blob_sha"]="0"*40
        with self.assertRaises(AssertionError):mod.verify(d,check_local=True)
    def test_unlock(self):self.reject(lambda d:d["continuation"].__setitem__("stage_b_and_wiki","OPEN"))
    def test_false_percent(self):self.reject(lambda d:d["continuation"].__setitem__("overall_restoration_percent",100))
if __name__=="__main__":unittest.main()
