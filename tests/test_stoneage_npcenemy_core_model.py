import unittest

from tools.stoneage_npcenemy_core_model import (
    EnemySpec, FreeState, battle_mode, choose_new_warp_segment, encounter_route,
    eval_active_free_expression, gym_enemy_formation, new_warp_application,
    normal_enemy_formation, old_death_action, required_items_present,
    revival_ready, steal_items, steal_phase, trigger_allowed,
)

class NPCEnemyCoreTests(unittest.TestCase):
    def test_entype_routes(self):
        self.assertTrue(trigger_allowed(0, "walk"))
        self.assertFalse(trigger_allowed(0, "talk"))
        self.assertFalse(trigger_allowed(1, "walk"))
        self.assertTrue(trigger_allowed(1, "talk"))
        self.assertTrue(trigger_allowed(2, "walk"))
        self.assertTrue(trigger_allowed(2, "talk"))

    def test_item_duplicate_can_reuse_one_physical_item(self):
        self.assertTrue(required_items_present([5, 5], [5]))

    def test_normal_enemy_list_is_first_ten_and_skips_invalid(self):
        specs = [EnemySpec(i, valid=(i != 2)) for i in range(12)]
        self.assertEqual(normal_enemy_formation(specs), (0, 1, 3, 4, 5, 6, 7, 8, 9))

    def test_big_enemy_is_moved_into_first_five(self):
        specs = [EnemySpec(1), EnemySpec(2), EnemySpec(3), EnemySpec(4), EnemySpec(5), EnemySpec(99, big=True)]
        self.assertEqual(normal_enemy_formation(specs), (99, 2, 3, 4, 5, 1))

    def test_sixth_big_enemy_is_skipped(self):
        specs = [EnemySpec(i, big=True) for i in range(6)]
        self.assertEqual(normal_enemy_formation(specs), (0, 1, 2, 3, 4))

    def test_gym_selects_one_main_and_one_pet(self):
        self.assertEqual(
            gym_enemy_formation([EnemySpec(1), EnemySpec(2)], [EnemySpec(8), EnemySpec(9)], enemy_pick=1, pet_pick=0),
            (2, 8),
        )

    def test_gym_battle_metadata(self):
        self.assertEqual(battle_mode(30)["baselevel"], 30)
        self.assertTrue(battle_mode(30)["norisk"])
        self.assertTrue(battle_mode(30)["skin_leader_from_npc"])
        self.assertEqual(battle_mode(0)["battle_create_mode"], 1)

    def test_hidden_npc_cannot_encounter(self):
        self.assertEqual(encounter_route(image_visible=False, entype=0, trigger="walk")["route"], "hidden")

    def test_prompt_returns_without_starting_battle(self):
        result = encounter_route(image_visible=True, entype=0, trigger="walk", askbattle_prompt=True)
        self.assertFalse(result["accepted"])
        self.assertEqual(result["route"], "prompt")

    def test_party_client_returns_true_without_direct_battle_start(self):
        result = encounter_route(image_visible=True, entype=0, trigger="walk", party_client=True)
        self.assertTrue(result["accepted"])
        self.assertEqual(result["route"], "party_client_no_battle")

    def test_onebattle_blocks_second_battle_from_same_npc(self):
        result = encounter_route(
            image_visible=True, entype=0, trigger="walk", onebattle=1, same_npc_battle_active=True
        )
        self.assertEqual(result["route"], "already_battling")

    def test_item_gate_denies_missing_required_item(self):
        result = encounter_route(
            image_visible=True, entype=0, trigger="walk", required_item_ids=[5], item_slots=[6]
        )
        self.assertEqual(result["route"], "denied_item")

    def test_steal_stops_when_first_target_is_missing(self):
        self.assertEqual(steal_items([1, 2], [9, 2])["deleted_slots"], ())

    def test_steal_found_counter_is_cumulative(self):
        self.assertEqual(steal_items([1, 2, 3], [1, 9, 3])["deleted_slots"], (0, 2))

    def test_steal_phase_zero_is_after_battle_creation(self):
        self.assertEqual(steal_phase(0), "after_battle_created")

    def test_steal_phase_one_is_after_win(self):
        self.assertEqual(steal_phase(1), "after_win")

    def test_dieact_zero_hides_and_schedules_revive(self):
        self.assertEqual(old_death_action(0)["action"], "hide_then_revive")

    def test_dieact_one_warps_winning_entries(self):
        self.assertEqual(old_death_action(1)["action"], "warp_winning_entries")

    def test_revival_is_strictly_greater_than_deadline(self):
        self.assertFalse(revival_ready(130, 10, 120))
        self.assertTrue(revival_ready(131, 10, 120))

    def test_active_free_families(self):
        state = FreeState(level=20, equipment_ids=(7,), end_flags=frozenset({3}), now_flags=frozenset())
        self.assertTrue(eval_active_free_expression("LV>10&EQUIT=7,ENDEV=9", state))
        self.assertTrue(eval_active_free_expression("NOWEV!=2", state))

    def test_event_relational_operator_collapses_to_presence(self):
        self.assertTrue(eval_active_free_expression("ENDEV>3", FreeState(end_flags=frozenset({3}))))

    def test_new_warp_uses_first_passing_newevent_segment(self):
        state = FreeState(level=20)
        segments = [
            {"newevent": True, "free": "LV>99", "warps": [(1, 2, 3)]},
            {"newevent": True, "free": "LV>10", "warps": [(4, 5, 6), (7, 8, 9)]},
        ]
        self.assertEqual(choose_new_warp_segment(segments, state, warp_pick=1)["warp"], (7, 8, 9))

    def test_new_warp_bad_selected_floor_falls_back_to_first(self):
        state = FreeState(level=20)
        segments = [{"newevent": True, "free": "LV>10", "warps": [(5, 1, 1), (0, 2, 2)]}]
        self.assertEqual(choose_new_warp_segment(segments, state, warp_pick=1)["warp"], (5, 1, 1))

    def test_checkparty_false_disables_event_action(self):
        state = FreeState(level=20)
        segments = [{
            "newevent": True, "free": "LV>10", "warps": [(5, 1, 1)], "checkparty_false": True
        }]
        result = choose_new_warp_segment(segments, state)
        self.assertFalse(result["party"])
        self.assertFalse(result["run_event_action"])

    def test_party_false_leader_warps_whole_party_and_returns(self):
        result = new_warp_application(party_flag=False, is_party_leader=True, party_member_count=4)
        self.assertEqual(result["warped_count"], 4)
        self.assertTrue(result["early_return"])

    def test_party_true_warps_individual_after_discharge(self):
        result = new_warp_application(party_flag=True, is_party_leader=True, party_member_count=4)
        self.assertEqual(result["mode"], "individual")
        self.assertTrue(result["discharge_party"])

if __name__ == "__main__":
    unittest.main()
