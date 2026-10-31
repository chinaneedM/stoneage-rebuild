import copy
import json
import unittest
from tools.stoneage_o14_sot_cd_source import REPORT, validate

class O14SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=json.loads(REPORT.read_text(encoding="utf-8"))
    def reject(self,cb):
        d=copy.deepcopy(self.source); cb(d)
        with self.assertRaises((ValueError,KeyError,TypeError,AssertionError)):
            validate(d)
    def test_real_contract(self):
        self.assertEqual(validate(self.source)["checkpoints"],24)
    def test_no_fake_native_sot(self):
        self.reject(lambda x:x.__setitem__("evidence_class","TW1_NATIVE_CONFIRMED"))
    def test_no_seasonal_event_claim(self):
        self.reject(lambda x:x["source_task_classification"].__setitem__("limited_time_event_verified",True))
    def test_preserve_repeated_characteristic(self):
        self.reject(lambda x:x["source_task_classification"].__setitem__("reader_submission_claims_repeatable",False))
    def test_route_inversion(self):
        self.reject(lambda x:x["route_choice"].__setitem__("C","not_completed"))
    def test_no_fake_real_sha(self):
        self.reject(lambda x:x["sources"]["C"].__setitem__("raw_source_sha256","abc"))
    def test_duplicate_checkpoint(self):
        self.reject(lambda x:x["checkpoints"]["D"][3].__setitem__("sequence",3))
    def test_dropped_checkpoint(self):
        self.reject(lambda x:x["checkpoints"]["C"].pop())
    def test_answer_corruption(self):
        self.reject(lambda x:x["checkpoints"]["C"][6].__setitem__("player_guide_answer","BAR Silky CLUB"))
    def test_no_source_floor_id_invention(self):
        self.reject(lambda x:x["checkpoints"]["D"][7].__setitem__("historical_map_floor_id",1001))
    def test_preserve_distinct_floors(self):
        self.reject(lambda x:x["checkpoints"]["D"][7].__setitem__("floor_or_scope","四楼"))
    def test_reward_probability_not_known(self):
        self.reject(lambda x:x["completion"].__setitem__("reward_probability",0.25))
    def test_no_game_entry_claim(self):
        self.reject(lambda x:x["unknowns"].__setitem__("world_entered",False))
    def test_no_false_project_percent(self):
        self.reject(lambda x:x["status_gates"].__setitem__("overall_percent",99))
    def test_no_source_citation_promotion(self):
        self.reject(lambda x:x["sources"]["index"].__setitem__("original_server_build_verified",True))
if __name__=="__main__":
    unittest.main()
