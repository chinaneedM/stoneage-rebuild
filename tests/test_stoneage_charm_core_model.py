import unittest

from tools.stoneage_charm_core_model import (
    CHARM_HEAL,
    MAX_CHARM,
    charm_cost,
    charm_upgrade,
    normal_confirmation_available,
    normal_yes_flow,
)


class CharmCoreTests(unittest.TestCase):
    def test_common_constants(self):
        self.assertEqual(CHARM_HEAL, 5)
        self.assertEqual(MAX_CHARM, 100)

    def test_cost_uses_integer_charm_division(self):
        self.assertEqual(
            charm_cost(level=20, charm=30, transmigration=0), 2000
        )
        self.assertEqual(
            charm_cost(level=20, charm=32, transmigration=0), 2000
        )
        self.assertEqual(
            charm_cost(level=20, charm=33, transmigration=0), 2200
        )

    def test_transmigration_multiplies_cost(self):
        self.assertEqual(
            charm_cost(level=20, charm=30, transmigration=2), 6000
        )

    def test_charm_zero_and_one_are_substituted_to_three(self):
        self.assertEqual(charm_cost(level=10, charm=0, transmigration=0), 100)
        self.assertEqual(charm_cost(level=10, charm=1, transmigration=0), 100)

    def test_charm_two_is_free_due_to_integer_division(self):
        self.assertEqual(charm_cost(level=10, charm=2, transmigration=0), 0)

    def test_max_charm_returns_minus_one(self):
        self.assertEqual(
            charm_cost(level=99, charm=100, transmigration=9), -1
        )
        self.assertEqual(
            charm_cost(level=99, charm=101, transmigration=9), -1
        )

    def test_upgrade_adds_five(self):
        out = normal_yes_flow(
            level=10, charm=30, transmigration=0, gold=2000
        )
        self.assertTrue(out["success"])
        self.assertEqual(out["charm_after"], 35)

    def test_upgrade_caps_at_one_hundred(self):
        out = normal_yes_flow(
            level=10, charm=98, transmigration=0, gold=100000
        )
        self.assertTrue(out["success"])
        self.assertEqual(out["charm_after"], 100)

    def test_exact_gold_is_accepted(self):
        cost = charm_cost(level=10, charm=30, transmigration=0)
        out = normal_yes_flow(
            level=10, charm=30, transmigration=0, gold=cost
        )
        self.assertTrue(out["success"])
        self.assertEqual(out["gold_after"], 0)

    def test_insufficient_gold_changes_nothing(self):
        out = normal_yes_flow(
            level=10, charm=30, transmigration=0, gold=999
        )
        self.assertFalse(out["success"])
        self.assertEqual(out["gold_after"], 999)
        self.assertEqual(out["charm_after"], 30)

    def test_zero_cost_charm_two_upgrades_without_gold(self):
        out = normal_yes_flow(
            level=10, charm=2, transmigration=0, gold=0
        )
        self.assertTrue(out["success"])
        self.assertEqual(out["gold_after"], 0)
        self.assertEqual(out["charm_after"], 7)

    def test_success_recomputes_player_and_pet_parameters(self):
        out = normal_yes_flow(
            level=10, charm=30, transmigration=0, gold=1000
        )
        self.assertTrue(out["player_parameters_recomputed"])
        self.assertTrue(out["pet_parameters_recomputed"])

    def test_normal_flow_does_not_offer_confirmation_at_max(self):
        self.assertFalse(
            normal_confirmation_available(
                level=10, charm=100, transmigration=0
            )
        )
        out = normal_yes_flow(
            level=10, charm=100, transmigration=0, gold=0
        )
        self.assertFalse(out["success"])
        self.assertEqual(out["reason"], "already_max_charm")

    def test_raw_upgrade_preserves_stale_callback_minus_one_cost_quirk(self):
        out = charm_upgrade(
            level=10, charm=100, transmigration=0, gold=0
        )
        self.assertTrue(out["success"])
        self.assertEqual(out["cost"], -1)
        self.assertEqual(out["gold_after"], 1)
        self.assertEqual(out["charm_after"], 100)


if __name__ == "__main__":
    unittest.main()
