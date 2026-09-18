import unittest

from tools.stoneage_pool_storage_model import (
    DEFAULT_ITEM_POOL_COST,
    deposit_item_pool_handler,
    deposit_pet_pool,
    item_pool_capacity,
    item_ui_marks_nonpoolable,
    later_depot_item_deposit_allowed,
    persistence_domains,
    pet_pool_capacity,
    pet_pool_cost,
    withdraw_item_pool,
    withdraw_pet_pool,
)


class PoolStorageModelTests(unittest.TestCase):
    def test_pet_pool_capacity_grows_two_per_transmigration_and_caps(self):
        self.assertEqual(pet_pool_capacity(0), 5)
        self.assertEqual(pet_pool_capacity(1), 7)
        self.assertEqual(pet_pool_capacity(9), 10)

    def test_item_pool_capacity_grows_four_per_transmigration_and_caps(self):
        self.assertEqual(item_pool_capacity(0), 10)
        self.assertEqual(item_pool_capacity(1), 14)
        self.assertEqual(item_pool_capacity(9), 20)

    def test_pet_pool_cost_is_level_scaled(self):
        self.assertEqual(pet_pool_cost(1), 54)
        self.assertEqual(pet_pool_cost(50), 250)

    def test_pet_deposit_moves_same_pet_charges_and_clears_default(self):
        carried = ["p0", "p1", None, None, None]
        pool = [None] * 10
        out = deposit_pet_pool(
            carried=carried,
            pool=pool,
            selected_slot=1,
            transmigration=0,
            level=20,
            gold=1000,
            default_pet_slot=1,
        )
        self.assertTrue(out["ok"])
        self.assertIsNone(out["carried"][1])
        self.assertEqual(out["pool"][0], "p1")
        self.assertEqual(out["gold"], 1000 - pet_pool_cost(20))
        self.assertEqual(out["default_pet_slot"], -1)

    def test_pet_deposit_rejects_ridden_pet(self):
        out = deposit_pet_pool(
            carried=["p0", None, None, None, None],
            pool=[None] * 10,
            selected_slot=0,
            transmigration=0,
            level=1,
            gold=1000,
            ride_pet_slot=0,
        )
        self.assertFalse(out["ok"])
        self.assertEqual(out["reason"], "riding_pet")

    def test_pet_deposit_rejects_insufficient_gold_at_window_path(self):
        out = deposit_pet_pool(
            carried=["p0", None, None, None, None],
            pool=[None] * 10,
            selected_slot=0,
            transmigration=0,
            level=50,
            gold=1,
        )
        self.assertFalse(out["ok"])
        self.assertEqual(out["reason"], "insufficient_gold")

    def test_pet_pool_capacity_uses_only_unlocked_prefix(self):
        pool = ["a", "b", "c", "d", "e", None, None, None, None, None]
        out = deposit_pet_pool(
            carried=["p0", None, None, None, None],
            pool=pool,
            selected_slot=0,
            transmigration=0,
            level=1,
            gold=1000,
        )
        self.assertFalse(out["ok"])
        self.assertEqual(out["reason"], "pool_full")

    def test_pet_withdraw_uses_first_carried_slot_and_compacts_pool(self):
        out = withdraw_pet_pool(
            carried=["a", None, "c", None, None],
            pool=["p0", "p1", "p2", None],
            selected_pool_slot=1,
        )
        self.assertTrue(out["ok"])
        self.assertEqual(out["carried"][1], "p1")
        self.assertEqual(out["pool"], ("p0", "p2", None, None))

    def test_item_ui_marks_historical_restricted_flags(self):
        self.assertTrue(
            item_ui_marks_nonpoolable(
                drop_at_logout=True,
                vanish_at_drop=False,
                can_petmail=True,
            )
        )
        self.assertTrue(
            item_ui_marks_nonpoolable(
                drop_at_logout=False,
                vanish_at_drop=False,
                can_petmail=False,
            )
        )
        self.assertFalse(
            item_ui_marks_nonpoolable(
                drop_at_logout=False,
                vanish_at_drop=False,
                can_petmail=True,
            )
        )

    def test_item_pool_handler_ignores_failed_gold_debit(self):
        out = deposit_item_pool_handler(
            carried=["item", None],
            pool=[None] * 20,
            selected_slot=0,
            transmigration=0,
            gold=0,
            cost=DEFAULT_ITEM_POOL_COST,
        )
        self.assertTrue(out["ok"])
        self.assertFalse(out["payment_succeeded"])
        self.assertTrue(out["historical_unpaid_move"])
        self.assertEqual(out["gold"], 0)
        self.assertIsNone(out["carried"][0])
        self.assertEqual(out["pool"][0], "item")

    def test_item_pool_handler_does_not_recheck_ui_restriction_flags(self):
        self.assertTrue(
            item_ui_marks_nonpoolable(
                drop_at_logout=True,
                vanish_at_drop=False,
                can_petmail=True,
            )
        )
        out = deposit_item_pool_handler(
            carried=["restricted-item"],
            pool=[None] * 20,
            selected_slot=0,
            transmigration=0,
            gold=1000,
        )
        self.assertTrue(out["ok"])
        self.assertEqual(out["pool"][0], "restricted-item")

    def test_item_withdraw_has_no_fee_and_compacts_pool(self):
        out = withdraw_item_pool(
            carried=["a", None, "c"],
            pool=["i0", "i1", "i2", None],
            selected_pool_slot=1,
        )
        self.assertTrue(out["ok"])
        self.assertEqual(out["carried"][1], "i1")
        self.assertEqual(out["pool"], ("i0", "i2", None, None))
        self.assertNotIn("gold", out)

    def test_later_depot_rechecks_restrictions_and_payment(self):
        self.assertFalse(
            later_depot_item_deposit_allowed(
                drop_at_logout=True,
                vanish_at_drop=False,
                can_petmail=True,
                enough_gold=True,
            )
        )
        self.assertFalse(
            later_depot_item_deposit_allowed(
                drop_at_logout=False,
                vanish_at_drop=False,
                can_petmail=True,
                enough_gold=False,
            )
        )
        self.assertTrue(
            later_depot_item_deposit_allowed(
                drop_at_logout=False,
                vanish_at_drop=False,
                can_petmail=True,
                enough_gold=True,
            )
        )

    def test_persistence_domains_do_not_conflate_pool_and_depot(self):
        domains = persistence_domains()
        self.assertEqual(domains["character_inline"], ("pool_items", "pool_pets"))
        self.assertEqual(domains["later_shared_depot"], ("depot_items", "depot_pets"))


if __name__ == "__main__":
    unittest.main()
