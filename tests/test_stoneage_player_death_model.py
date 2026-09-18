import unittest

from tools.stoneage_player_death_model import (
    CLEAR_ON_DEATH,
    death_transition,
    login_sanitize,
    resurrect_transition,
)


class PlayerDeathModelTests(unittest.TestCase):
    def test_enemy_death_requests_all_equipped_items(self):
        out = death_transition(101, (0, 2, 4), "enemy", dead_count=7)
        self.assertEqual(out["item_drop_mode"], "all_equipped")
        self.assertEqual(out["requested_item_drop_slots"], (0, 2, 4))
        self.assertEqual(out["random_item_drop_count"], 0)
        self.assertEqual(out["requested_ground_gold"], 50)
        self.assertEqual(out["final_carried_gold"], 0)
        self.assertEqual(out["dead_count"], 8)
        self.assertTrue(out["party_discharged"])
        self.assertTrue(out["is_dead"])
        self.assertFalse(out["is_attacked"])

    def test_unknown_attacker_uses_same_item_penalty_as_enemy(self):
        out = death_transition(10, (1, 3), "unknown")
        self.assertEqual(out["item_drop_mode"], "all_equipped")
        self.assertEqual(out["requested_item_drop_slots"], (1, 3))

    def test_non_enemy_attacker_requests_one_random_equipped_item(self):
        out = death_transition(200, (0, 1, 5), "non_enemy")
        self.assertEqual(out["item_drop_mode"], "one_random_equipped")
        self.assertEqual(out["requested_item_drop_slots"], ())
        self.assertEqual(out["random_item_drop_candidates"], (0, 1, 5))
        self.assertEqual(out["random_item_drop_count"], 1)

    def test_non_enemy_with_no_equipment_requests_no_item_drop(self):
        out = death_transition(0, (), "non_enemy")
        self.assertEqual(out["random_item_drop_count"], 0)
        self.assertEqual(out["requested_ground_gold"], 0)

    def test_death_clears_stable_status_set(self):
        self.assertEqual(
            CLEAR_ON_DEATH,
            ("paralysis", "sleep", "stone", "drunk", "confusion", "poison"),
        )

    def test_resurrection_clamps_hp_and_does_not_move_or_refill_mp(self):
        self.assertEqual(resurrect_transition(-5, 100)["hp"], 1)
        self.assertEqual(resurrect_transition(50, 100)["hp"], 50)
        capped = resurrect_transition(150, 100)
        self.assertEqual(capped["hp"], 100)
        self.assertTrue(capped["mp_unchanged"])
        self.assertTrue(capped["location_unchanged"])
        self.assertFalse(capped["is_dead"])
        self.assertTrue(capped["is_attacked"])
        self.assertFalse(capped["is_overed"])

    def test_login_sanitize_clears_persisted_death_and_repairs_nonpositive_hp(self):
        self.assertEqual(login_sanitize(True, 0), {"is_dead": False, "hp": 1})
        self.assertEqual(login_sanitize(False, 25), {"is_dead": False, "hp": 25})


if __name__ == "__main__":
    unittest.main()
