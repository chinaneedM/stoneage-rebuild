import copy, importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("r111_custody",ROOT/"tools/stoneage_jp2009_mystery_custody_r111.py")
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
original=json.loads(mod.RECEIPT.read_text(encoding="utf-8"))
class TestCustodyR111(unittest.TestCase):
    def test_current_files(self): self.assertTrue(mod.verify(copy.deepcopy(original)))
    def bad(self,f):
        d=copy.deepcopy(original);f(d)
        with self.assertRaises(AssertionError): mod.verify(d,inspect_files=False)
    def test_fake_html(self):self.bad(lambda d:d["source_custody"].__setitem__("actual_2009_original_html_sha256","fake"))
    def test_fake_zip(self):self.bad(lambda d:d["source_custody"].__setitem__("ci_source_zip_digest","fake"))
    def test_false_server(self):self.bad(lambda d:d["source_custody"].__setitem__("server_script_or_rewards_verified",True))
    def test_fake_prefix(self):self.bad(lambda d:d["history_prefixes"]["docs/CURRENT-STATE.md"].__setitem__("exact_prefix",False))
    def test_wrong_blob(self):self.bad(lambda d:d["files"]["pins"].__setitem__("docs/CURRENT-STATE.md","bad"))
    def test_missing_run(self):self.bad(lambda d:d["ci"]["main_final"]["runs"].pop())
    def test_fake_head(self):self.bad(lambda d:d["content"].__setitem__("integrated_commit","fake"))
    def test_fake_runtime(self):self.bad(lambda d:d["ci"].__setitem__("actual_game_runtime_executed_by_ci",True))
if __name__=="__main__":unittest.main()
