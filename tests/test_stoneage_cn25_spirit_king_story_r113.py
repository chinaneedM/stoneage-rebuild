import copy
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from stoneage_cn25_spirit_king_story_r113 import validate

D=json.loads((ROOT/"research/recovered/STONEAGE-CN25-SPIRIT-KING-STORY-R113.json").read_text(encoding="utf-8"))
class R113SourceBoundaries(unittest.TestCase):
    def test_valid(self): self.assertTrue(validate(D))
    def bad(self, fn):
        q=copy.deepcopy(D)
        fn(q)
        with self.assertRaises((AssertionError,ValueError,KeyError)):validate(q)
    def test_no_fake_author(self):self.bad(lambda x:x["sources"][0].update(source_authorship_authenticated=True))
    def test_no_fake_official_html(self):self.bad(lambda x:x["historical_edition"].update(original_official_operator_html_authenticated=True))
    def test_no_fake_source_sha(self):self.bad(lambda x:x["sources"][1].update(original_html_sha256="fake"))
    def test_no_tw10(self):self.bad(lambda x:x["historical_edition"].update(jss1999_or_tw10_identity_proven=True))
    def test_no_original_build(self):self.bad(lambda x:x["historical_edition"].update(actual_client_build="2.5.0"))
    def test_preserve_seal_conflict(self):self.bad(lambda x:x["story"].update(dark_king_claims_not_reconciled=[]))
    def test_preserve_landmass_name(self):self.bad(lambda x:x["story"]["landmasses_as_written"].__setitem__(1,"萨伊那斯"))
    def test_no_server_rebirth(self):self.bad(lambda x:x["story"].update(original_pet_master_or_rebirth_formula="growth 5.0"))
    def test_no_calendar_year(self):self.bad(lambda x:x["story_time_claims"][0].update(real_world_calendar_year=1500))
    def test_preserve_feng_variants(self):self.bad(lambda x:x["disputed_spellings"].update(s1_story=x["disputed_spellings"]["s2_player"]))
    def test_no_spell_runtime(self):self.bad(lambda x:x["disputed_spellings"].update(original_in_game_chat_trigger_verified=True))
    def test_no_fake_npc_master(self):self.bad(lambda x:x["actors"][0].update(original_npc_id=101))
    def test_no_sprite_join(self):self.bad(lambda x:x["actors"][0].update(same_build_runtime_identity_verified=True))
    def test_no_2001_black_jade_join(self):self.bad(lambda x:x["dedupe"].update(existing_r112_item_label_black_jade_not_joined=False))
    def test_no_duplicated_article_as_independent(self):self.bad(lambda x:x["dedupe"].update(subpage_counted_as_independent_source=True))
    def test_no_source_runtime(self):self.bad(lambda x:x["provenance_boundary"].update(actual_dialogue_runtime_recovered=True))
    def test_no_fake_100_percent(self):self.bad(lambda x:x["provenance_boundary"].update(aggregate_restoration_percentage=100))
    def test_no_false_2002_quest_execution(self):self.bad(lambda x:x["s2_correlated_quest_observations"].update(actual_server_quest_completed_independently=True))
    def test_no_new_entity_claim(self):self.bad(lambda x:x.update(new_archive_claims_not_new_original_entities=False))

if __name__=="__main__":unittest.main()
