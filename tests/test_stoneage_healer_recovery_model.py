import unittest

from tools.stoneage_healer_recovery_model import (
    DEFAULT_HP_RATE_UNITS,
    DEFAULT_MP_RATE_UNITS,
    PARTY_CLIENT,
    PARTY_LEADER,
    PARTY_NONE,
    WINDOW_MODE_ALL,
    WINDOW_MODE_HP,
    WINDOW_MODE_MP,
    WINDOW_MODE_PET_ONLY,
    free_healer_all_heal,
    healer_targets,
    hp_cost,
    mp_cost,
    pet_healer_check,
    window_healer_apply,
    window_healer_cost,
    window_healer_level_is_free,
    window_healer_transaction,
)


def player():
    return {
        "level": 20,
        "hp": 10,
        "max_hp": 100,
        "mp": 3,
        "max_mp": 50,
        "dead": True,
        "poison": 4,
    }


def pets():
    return (
        {"hp": 1, "max_hp": 80, "mp": 2, "max_mp": 30, "dead": True},
        {"hp": 60, "max_hp": 60, "mp": 0, "max_mp": 25, "dead": False},
        None,
    )


class HealerRecoveryModelTests(unittest.TestCase):
    def test_free_healer_target_scope(self):
        self.assertEqual(healer_targets(10, PARTY_NONE), (10,))
        self.assertEqual(healer_targets(20, PARTY_CLIENT), (20,))
        self.assertEqual(
            healer_targets(10, PARTY_LEADER, (10, 20, None, 40, None)),
            (10, 20, 40),
        )

    def test_free_healer_fills_player_and_revives_all_valid_pets(self):
        out = free_healer_all_heal(player(), pets())
        self.assertEqual(out["player"]["hp"], 100)
        self.assertEqual(out["player"]["mp"], 50)
        self.assertTrue(out["player"]["dead"])
        self.assertEqual(out["player"]["poison"], 4)
        self.assertFalse(out["pets"][0]["dead"])
        self.assertEqual(out["pets"][0]["hp"], 80)
        self.assertEqual(out["pets"][0]["mp"], 30)
        self.assertEqual(out["pets"][1]["mp"], 25)
        self.assertTrue(out["pets"][0]["parameters_recomputed"])

    def test_window_healer_free_threshold_is_strictly_below_configured_level(self):
        self.assertTrue(window_healer_level_is_free(9, 10))
        self.assertFalse(window_healer_level_is_free(10, 10))

    def test_default_costs_are_half_level_for_hp_and_double_level_for_mp(self):
        self.assertEqual(DEFAULT_HP_RATE_UNITS, 500)
        self.assertEqual(DEFAULT_MP_RATE_UNITS, 2000)
        self.assertEqual(hp_cost(20), 10)
        self.assertEqual(mp_cost(20), 40)

    def test_hp_cost_has_minimum_one(self):
        self.assertEqual(hp_cost(1), 1)

    def test_all_mode_only_charges_for_missing_player_resources(self):
        self.assertEqual(
            window_healer_cost(
                player_level=20,
                free_below_level=10,
                mode=WINDOW_MODE_ALL,
                hp=100,
                max_hp=100,
                mp=3,
                max_mp=50,
            ),
            40,
        )
        self.assertEqual(
            window_healer_cost(
                player_level=20,
                free_below_level=10,
                mode=WINDOW_MODE_ALL,
                hp=100,
                max_hp=100,
                mp=50,
                max_mp=50,
            ),
            0,
        )

    def test_pet_only_mode_is_free(self):
        self.assertEqual(
            window_healer_cost(
                player_level=99,
                free_below_level=1,
                mode=WINDOW_MODE_PET_ONLY,
                hp=1,
                max_hp=100,
                mp=1,
                max_mp=50,
            ),
            0,
        )

    def test_pet_need_check_only_looks_at_hp_not_mp_or_death_flag(self):
        full_hp_low_mp = (
            {"hp": 80, "max_hp": 80, "mp": 0, "max_mp": 30, "dead": True},
        )
        self.assertFalse(pet_healer_check(full_hp_low_mp))
        hurt = (
            {"hp": 79, "max_hp": 80, "mp": 30, "max_mp": 30, "dead": False},
        )
        self.assertTrue(pet_healer_check(hurt))

    def test_window_hp_mode_heals_player_hp_but_always_full_heals_pets(self):
        out = window_healer_apply(player(), pets(), WINDOW_MODE_HP)
        self.assertEqual(out["player"]["hp"], 100)
        self.assertEqual(out["player"]["mp"], 3)
        self.assertTrue(out["player"]["dead"])
        self.assertEqual(out["pets"][0]["hp"], 80)
        self.assertEqual(out["pets"][0]["mp"], 30)
        self.assertFalse(out["pets"][0]["dead"])

    def test_window_mp_mode_does_not_restore_player_hp(self):
        out = window_healer_apply(player(), pets(), WINDOW_MODE_MP)
        self.assertEqual(out["player"]["hp"], 10)
        self.assertEqual(out["player"]["mp"], 50)

    def test_window_pet_only_mode_leaves_player_resources_unchanged(self):
        out = window_healer_apply(player(), pets(), WINDOW_MODE_PET_ONLY)
        self.assertEqual(out["player"]["hp"], 10)
        self.assertEqual(out["player"]["mp"], 3)
        self.assertEqual(out["pets"][0]["hp"], 80)

    def test_payment_happens_before_heal_and_insufficient_gold_changes_nothing(self):
        p = player()
        out = window_healer_transaction(
            player=p,
            pets=pets(),
            mode=WINDOW_MODE_ALL,
            free_below_level=10,
            gold=49,
        )
        self.assertFalse(out["success"])
        self.assertEqual(out["charge"], 50)
        self.assertEqual(out["gold_after"], 49)
        self.assertEqual(out["player"]["hp"], 10)
        self.assertTrue(out["pets"][0]["dead"])

    def test_successful_paid_transaction_deducts_exact_charge_then_heals(self):
        out = window_healer_transaction(
            player=player(),
            pets=pets(),
            mode=WINDOW_MODE_ALL,
            free_below_level=10,
            gold=100,
        )
        self.assertTrue(out["success"])
        self.assertEqual(out["charge"], 50)
        self.assertEqual(out["gold_after"], 50)
        self.assertEqual(out["player"]["hp"], 100)
        self.assertEqual(out["player"]["mp"], 50)

    def test_below_threshold_transaction_is_free(self):
        p = player()
        p["level"] = 5
        out = window_healer_transaction(
            player=p,
            pets=pets(),
            mode=WINDOW_MODE_ALL,
            free_below_level=10,
            gold=0,
        )
        self.assertTrue(out["success"])
        self.assertEqual(out["charge"], 0)
        self.assertEqual(out["gold_after"], 0)


if __name__ == "__main__":
    unittest.main()
