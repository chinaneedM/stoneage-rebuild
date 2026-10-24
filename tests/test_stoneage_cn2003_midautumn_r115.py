#!/usr/bin/env python3
import copy, json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from stoneage_cn2003_midautumn_r115 import validate
D=json.loads((ROOT/"research/recovered/STONEAGE-CN2003-MIDAUTUMN-R115.json").read_text(encoding="utf-8"))

class R115BoundaryTest(unittest.TestCase):
    def bad(self,change):
        d=copy.deepcopy(D);change(d)
        with self.assertRaises((AssertionError,ValueError,KeyError,TypeError)):validate(d)
    def test_valid(self):self.assertTrue(validate(D))
    def test_date(self):self.bad(lambda d:d["source"].update(page_date="2002-09-11"))
    def test_fake_publisher_auth(self):self.bad(lambda d:d["source"].update(byline_independently_authenticated=True))
    def test_fake_raw_html(self):self.bad(lambda d:d["source"].update(current_http_raw_html_sha256="bad"))
    def test_fake_original_html(self):self.bad(lambda d:d["source"].update(original_2003_operator_site_html="official"))
    def test_not_second_source(self):self.bad(lambda d:d["source"]["linked_related_article"].update(independent_source_count_increment=1))
    def test_no_original_build(self):self.bad(lambda d:d["edition"].update(exact_official_patch_version="6.0"))
    def test_no_original_server(self):self.bad(lambda d:d["edition"].update(claimed_game_server_deployment_verified=True))
    def test_no_tw10(self):self.bad(lambda d:d["edition"].update(jss1999_or_tw10_same_version_proven=True))
    def test_no_werewolf_join(self):self.bad(lambda d:d["edition"].update(taiwan2002_werewolf_or_jp2004_christmas_identity_join=True))
    def test_no_npc_ids(self):self.bad(lambda d:d["narrative"].update(original_server_npc_ids=[1,2,3]))
    def test_actor_names(self):self.bad(lambda d:d["narrative"].update(participants_as_text=["后羿","嫦娥"]))
    def test_quest_runtime(self):self.bad(lambda d:d["narrative"].update(actual_quest_replay_verified=True))
    def test_moon_permit(self):self.bad(lambda d:d["narrative"]["steps_as_reported"][2].update(permit_name="吴刚"))
    def test_no_uncensored_asterisks(self):self.bad(lambda d:d["narrative"].update(redacted_terms_restored=True))
    def test_repeatability_only_text(self):self.bad(lambda d:d["narrative"].update(repeatability="PROVEN_SERVER"))
    def test_no_random_probs(self):self.bad(lambda d:d["rewards"].update(random_probabilities=[.25,.25,.25,.25]))
    def test_no_reward_count_assumption(self):self.bad(lambda d:d["rewards"].update(exclusive_one_reward_across_all_categories_proven=True))
    def test_mirror_duration(self):self.bad(lambda d:d["rewards"]["entries"][0].update(stated_effect="变身十分钟"))
    def test_mirror_runtime_unknown(self):self.bad(lambda d:d["rewards"]["entries"][0].update(actual_runtime_duration_verified=True))
    def test_skills_both_unknown(self):self.bad(lambda d:d["rewards"]["entries"][1].update(one_can_teaches_both_proven=True))
    def test_skill_name(self):self.bad(lambda d:d["rewards"]["entries"][1].update(skills_as_reported=["旅途伙伴3","狂乱暴走"]))
    def test_ring_uses(self):self.bad(lambda d:d["rewards"]["entries"][2].update(stated_uses=20))
    def test_no_ring_teleport_formula(self):self.bad(lambda d:d["rewards"]["entries"][2].update(teleport_target_formula="FREE_WARP"))
    def test_weapon_range(self):self.bad(lambda d:d["rewards"]["entries"][3].update(level_range=[12,16]))
    def test_no_exact_item(self):self.bad(lambda d:d["rewards"]["entries"][3].update(precise_item_list=["sword"]))
    def test_not_original_entity(self):self.bad(lambda d:d["classification"].update(new_original_game_entity_identifiers=3))
    def test_no_original_ui(self):self.bad(lambda d:d["classification"].update(documented_ui="ORIGINAL_SCREEN_REPLAY"))
    def test_no_server_reward(self):self.bad(lambda d:d["hard_gates"].update(server_rewards_redeemed=True))
    def test_no_percent(self):self.bad(lambda d:d["hard_gates"].update(overall_completion_percent=95))

if __name__=="__main__":unittest.main()
