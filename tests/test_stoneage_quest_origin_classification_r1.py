#!/usr/bin/env python3
import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from validate_stoneage_quest_origin_classification_r1 import validate
D=json.loads((ROOT/"research/recovered/STONEAGE-QUEST-ORIGIN-SEPARATION-R1.json").read_text(encoding="utf-8"))
class OriginSeparation(unittest.TestCase):
    def reject(self,fn):
        x=copy.deepcopy(D);fn(x)
        with self.assertRaises((AssertionError,KeyError,ValueError,TypeError)):validate(x)
    def test_valid_source_references(self):self.assertTrue(validate(D))
    def test_no_event_to_base(self):self.reject(lambda x:x["records"][3].update(origin="BASE_GAME_QUEST"))
    def test_no_unknown_r114_to_base(self):self.reject(lambda x:x["records"][4].update(origin="BASE_GAME_QUEST"))
    def test_no_unknown_r113_to_permanent(self):self.reject(lambda x:x["records"][5].update(origin="PERMANENT_VERSION_QUEST"))
    def test_no_event_activity_as_quest(self):self.reject(lambda x:x["records"][2].update(record_kind="EVENT_QUEST_CLAIM"))
    def test_no_event_to_non_event_view(self):self.reject(lambda x:x["records"][0].update(is_event_archive=False))
    def test_no_quest_into_baseline_denominator(self):self.reject(lambda x:x["records"][3].update(baseline_core_admission=True))
    def test_no_fabricated_r115_end(self):self.reject(lambda x:x["records"][3].update(event_window="2003-09-11/2003-09-12"))
    def test_no_fabricated_r114_event_window(self):self.reject(lambda x:x["records"][4].update(event_window="2003-09-11"))
    def test_original_blob_stays_same(self):self.reject(lambda x:x["records"][3].update(source_git_blob="0"*40))
    def test_event_story_not_universal(self):self.reject(lambda x:x["policy"].update(release_time_is_not_worldline_time=False))
    def test_event_rewards_can_persist(self):self.reject(lambda x:x["policy"].update(event_reward_may_persist_after_event_without_quest_becoming_base_game=False))
    def test_no_fake_completed_entries(self):self.reject(lambda x:x.update(base_game_quest_entries_verified_this_overlay=1))
    def test_no_fake_100pct(self):self.reject(lambda x:x.update(global_restoration_percent=100))
    def test_no_duplicate_records(self):self.reject(lambda x:x["records"].__setitem__(5,copy.deepcopy(x["records"][4])))
    def test_no_relabel_company(self):self.reject(lambda x:x["records"][3].update(source_git_blob=x["records"][4]["source_git_blob"]))
if __name__=="__main__":unittest.main()
