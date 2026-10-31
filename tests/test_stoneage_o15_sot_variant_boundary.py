import copy
import json
import unittest
from tools.stoneage_o15_sot_variant_boundary import REPORT,validate

class TestO15(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.base=json.loads(REPORT.read_text(encoding="utf-8"))
 def reject(self,modify):
  o=copy.deepcopy(self.base);modify(o)
  with self.assertRaises((ValueError,KeyError,TypeError,AssertionError)):validate(o)
 def test_valid(self):self.assertEqual(validate(self.base)["matched_checkpoints"],24)
 def test_drop(self):self.reject(lambda x:x["all_checkpoints"].pop())
 def test_false_2003_sha(self):self.reject(lambda x:x["earlier_source"].__setitem__("original_html_or_game_script_acquired",True))
 def test_fake_build(self):self.reject(lambda x:x["historical_limits"].__setitem__("repost_does_not_authenticate_1_82_build",False))
 def test_fake_percent(self):self.reject(lambda x:x["historical_limits"].__setitem__("overall_percent",90))
 def test_merge_endpoints(self):self.reject(lambda x:x["entry_and_exit_variants"].__setitem__("later_C_completion","萨姆吉尔村"))
 def test_eligibility(self):self.reject(lambda x:x["entry_and_exit_variants"].__setitem__("earlier_C_gate",x["entry_and_exit_variants"]["later_C_gate"]))
 def test_loss_cave_coordinate(self):self.reject(lambda x:x["all_checkpoints"][2].__setitem__("later_coordinate",[27,42]))
 def test_answer_diff(self):self.reject(lambda x:x["all_checkpoints"][4].__setitem__("answer_text_differs",False))
 def test_coordinate_diff(self):self.reject(lambda x:x["all_checkpoints"][1].__setitem__("coordinate_differs",False))
 def test_unknown_event(self):self.reject(lambda x:x["historical_limits"].__setitem__("timed_event_not_proven",False))
if __name__=="__main__":unittest.main()
