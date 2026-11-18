"""PET104: 2015 Taiwan Halloween eight notice prizes, claimed bone egg and open annual gate."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/"research/recovered"
A=REC/"STONEAGE-PET104-TW2015-HALLOWEEN-RELAY-PRIZE-EGG-BOUNDARY-R1.json"
Q=REC/"STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
REPORT=ROOT/"docs/continuity/STONEAGE-PET104-TW2015-HALLOWEEN-OFFICIAL-RELAY-PRIZE-BOX-BOUNDARY-20261118.md"

class Pet104HalloweenOriginalPcSourceBoundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=json.loads(A.read_text(encoding="utf-8"))
        cls.q=json.loads(Q.read_text(encoding="utf-8"))

    def test_still_2015_open_and_forward_receipt(self):
        a,q=self.a,self.q
        self.assertEqual((a["year"],a["year_frontier_before"],a["year_frontier_after"]),(2015,2015,2015))
        self.assertEqual(a["annual_review_status"],"NOT_YEAR_AUDITED")
        self.assertFalse(a["year_closed"])
        self.assertFalse(a["historically_complete"])
        self.assertEqual(a["active_module"],"PET")
        self.assertEqual(q["current_frontier"]["year"],2015)
        self.assertEqual(q["yearly_work_queue"][16]["research_gate"],"NOT_YEAR_AUDITED")
        self.assertEqual(q["yearly_work_queue"][15]["research_gate"],"SOURCE_BOUNDED_REVIEWED")
        self.assertEqual(q["current_frontier"]["latest_partial_root_review"],a["id"])
        self.assertEqual(q["root_source_census_receipts"][-1]["id"],a["id"])
        self.assertEqual(q["root_source_census_receipts"][-2]["id"],a["startup"]["previous_receipt"])
        self.assertEqual(q["yearly_work_queue"][16]["partial_source_review_receipts"][-1]["id"],a["id"])
        self.assertEqual(q["root_source_census_receipts"][-1]["official_reward_label_strings"],8)
        self.assertTrue(a["next"].startswith("PET105:"))
        self.assertTrue(q["current_frontier"]["next"].startswith("PET105:"))
        self.assertIn("PET104",REPORT.read_text(encoding="utf-8"))

    def test_official_notice_relay_eight_strings_not_new_species(self):
        a=self.a
        src=a["sources"][0]
        self.assertEqual(src["quoted_operator_publication"],"2015-10-28 01:22")
        self.assertEqual(src["forum_post_edit_date"],"2015-10-29 19:48:34")
        self.assertEqual(src["announced_event_begin"],"2015-10-28 weekly maintenance")
        self.assertEqual(src["announced_event_end"],"2015-11-04 weekly maintenance")
        self.assertTrue(src["search_index_detailed_text_retrieved"])
        self.assertFalse(src["original_operator_html_retrieved"])
        self.assertFalse(src["original_forum_full_html_retrieved"])
        self.assertFalse(src["original_notice_url_verified"])
        self.assertFalse(src["official_actual_server_issuance_verified"])
        self.assertEqual(len(src["announced_reward_names"]),8)
        self.assertEqual(len(src["announced_reward_kinds"]),8)
        self.assertEqual(src["announced_reward_kinds"].count("NAMED_PET_REWARD_CANDIDATE"),5)
        self.assertEqual(src["announced_reward_kinds"].count("CANNED_SKILL_ITEM"),2)
        self.assertEqual(src["announced_reward_kinds"].count("JEWELLERY_ITEM"),1)
        self.assertNotIn("骨龍蛋",src["announced_reward_names"])
        self.assertEqual(a["evidence_counts"]["announced_reward_strings"],8)
        self.assertEqual(a["evidence_counts"]["announced_nonpet_reward_strings"],3)

    def test_player_egg_owl_box_and_2026_edit_do_not_merge(self):
        a=self.a;s=a["sources"]
        self.assertEqual(s[1]["forum_post_edit_date"],"2015-10-28 20:47:19")
        self.assertEqual(s[1]["reported_sequence"],["南瓜禮盒","骨龍蛋"])
        self.assertFalse(s[1]["literal_bone_dragon_egg_in_announced_rewards"])
        self.assertFalse(s[1]["live_bone_dragon_pet_verified"])
        self.assertFalse(s[1]["egg_equals_史凱勒頓_or_古斯特_verified"])
        self.assertEqual(s[2]["reported_nested_path"],["希林南瓜禮盒","貓頭鷹禮盒","奧樂奇 或 奧特森"])
        self.assertFalse(s[2]["verified_original_box_open_script"])
        self.assertFalse(s[2]["verified_live_pet_grant"])
        self.assertEqual(s[3]["editor_date"],"2026-02-13 00:04:30")
        self.assertFalse(s[3]["independent_2015_original_source"])
        self.assertFalse(s[4]["pet_mechanics_verified"])
        self.assertTrue(a["unresolved_conflict"]["announced_list_does_not_literal_list_bone_dragon_egg"])
        self.assertTrue(a["unresolved_conflict"]["player_reported_bone_dragon_egg_from_pumpkin_box"])
        self.assertTrue(all(a["negative_controls"].values()))

    def test_original_historical_blob_and_native_pet_bounds(self):
        a,q=self.a,self.q
        self.assertEqual(set(a["region_gaps"]),{"CN","TW","HK_MO","KR","JP","OTHER"})
        for k in ["new_authenticated_2015_original_pc_client_bytes","new_authenticated_2015_original_pc_patch_bytes","new_native_pet_ids","new_original_spr_assets","new_native_pet_skills","new_first_party_verified_live_pet_grants"]:
            self.assertEqual(a[k],0)
        self.assertIsNone(a["global_official_2015_pet_species_count"])
        self.assertIsNone(a["first_issued_2015_official_species_count"])
        raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw),a["startup"]["original_current_bytes"])
        blob_sha=hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\x00"+raw).hexdigest()
        self.assertEqual(blob_sha,a["startup"]["original_current_blob"])
        self.assertTrue(a["original_current_state_unchanged"])
        self.assertEqual((q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None))
        self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"],a["overall_percent"]),(q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]))

if __name__=="__main__":
    unittest.main()
