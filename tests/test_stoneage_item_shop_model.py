import unittest

from tools.stoneage_item_shop_model import (
    ShopItem,
    buy_is_transactionally_atomic,
    buy_mutation_order,
    buy_unit_price,
    can_receive_sale_gold,
    clamp_purchase_quantity,
    sell_mutation_order,
    sell_unit_price,
    sell_whitelisted,
    simulate_purchase,
    simulate_sale,
)


class ItemShopModelTests(unittest.TestCase):
    def test_buy_price_multiplies_then_truncates(self):
        self.assertEqual(buy_unit_price(101, 0.5), 50)
        self.assertEqual(buy_unit_price(100, 1.25), 125)

    def test_buy_override_cost_precedes_rate(self):
        self.assertEqual(buy_unit_price(100, 1.5, override_cost=80), 120)

    def test_requested_buy_quantity_is_silently_clamped_to_empty_slots(self):
        self.assertEqual(clamp_purchase_quantity(10, 3), 3)
        self.assertEqual(clamp_purchase_quantity(2, 3), 2)
        self.assertEqual(clamp_purchase_quantity(0, 3), 0)

    def test_purchase_checks_total_gold_before_creating_items(self):
        out = simulate_purchase(
            gold=99,
            base_cost=50,
            requested_quantity=2,
            empty_inventory_slots=2,
        )
        self.assertFalse(out["success"])
        self.assertEqual(out["reason"], "not_enough_gold")
        self.assertEqual(out["items_added"], 0)
        self.assertEqual(out["gold_after"], 99)

    def test_successful_purchase_adds_items_then_deducts_total_gold(self):
        out = simulate_purchase(
            gold=500,
            base_cost=100,
            requested_quantity=3,
            empty_inventory_slots=3,
            buy_rate=0.5,
        )
        self.assertTrue(out["success"])
        self.assertEqual(out["items_added"], 3)
        self.assertEqual(out["total_price"], 150)
        self.assertEqual(out["gold_after"], 350)
        self.assertEqual(
            buy_mutation_order(),
            ("create_and_insert_each_item", "deduct_total_gold"),
        )

    def test_purchase_failure_mid_creation_has_no_rollback_and_no_gold_deduction(self):
        out = simulate_purchase(
            gold=500,
            base_cost=100,
            requested_quantity=3,
            empty_inventory_slots=3,
            fail_create_at=2,
        )
        self.assertFalse(out["success"])
        self.assertEqual(out["items_added"], 2)
        self.assertEqual(out["gold_after"], 500)
        self.assertFalse(buy_is_transactionally_atomic())

    def test_sell_whitelist_accepts_exact_type_group_and_id_range(self):
        axe = ShopItem(item_id=100, item_type=1, base_cost=100)
        ring = ShopItem(item_id=200, item_type=11, base_cost=100)
        other = ShopItem(item_id=350, item_type=16, base_cost=100)

        self.assertTrue(
            sell_whitelisted(
                axe,
                limit_item_types=("AXE",),
                exact_type_labels={"AXE": 1},
            )
        )
        self.assertTrue(
            sell_whitelisted(ring, limit_item_types=("ACCESSORY",))
        )
        self.assertTrue(
            sell_whitelisted(other, limit_item_ids=((300, 400),))
        )

    def test_unmatched_item_is_not_sellable(self):
        item = ShopItem(item_id=999, item_type=16, base_cost=100)
        self.assertFalse(sell_whitelisted(item))

    def test_normal_sell_requires_configured_sell_rate(self):
        self.assertIsNone(sell_unit_price(100, normal_sell_rate=None))
        self.assertEqual(sell_unit_price(100, normal_sell_rate=0.2), 20)

    def test_special_item_defaults_to_one_point_two_when_rate_absent(self):
        self.assertEqual(
            sell_unit_price(100, is_special_item=True, special_rate=None),
            120,
        )
        self.assertEqual(
            sell_unit_price(100, is_special_item=True, special_rate=0.5),
            50,
        )

    def test_sale_that_reaches_exact_gold_cap_is_rejected(self):
        self.assertFalse(can_receive_sale_gold(900, 100, 1000))
        self.assertTrue(can_receive_sale_gold(899, 100, 1000))

    def test_partial_stack_sale_decrements_stack_then_adds_gold(self):
        item = ShopItem(item_id=1, item_type=16, base_cost=100, stack_count=5)
        out = simulate_sale(
            item=item,
            sell_quantity=2,
            current_gold=100,
            max_gold=1000,
            whitelisted=True,
            normal_sell_rate=0.2,
        )
        self.assertTrue(out["success"])
        self.assertEqual(out["stack_after"], 3)
        self.assertEqual(out["proceeds"], 40)
        self.assertEqual(out["gold_after"], 140)
        self.assertFalse(out["item_instance_deleted"])
        self.assertEqual(
            sell_mutation_order(),
            ("delete_or_decrement_item", "add_gold"),
        )

    def test_full_stack_sale_deletes_item_instance(self):
        item = ShopItem(item_id=1, item_type=16, base_cost=100, stack_count=5)
        out = simulate_sale(
            item=item,
            sell_quantity=5,
            current_gold=0,
            max_gold=1000,
            whitelisted=True,
            normal_sell_rate=0.2,
        )
        self.assertTrue(out["item_instance_deleted"])
        self.assertEqual(out["stack_after"], 0)

    def test_sale_rejects_quantity_greater_than_stack(self):
        item = ShopItem(item_id=1, item_type=16, base_cost=100, stack_count=2)
        out = simulate_sale(
            item=item,
            sell_quantity=3,
            current_gold=0,
            max_gold=1000,
            whitelisted=True,
            normal_sell_rate=0.2,
        )
        self.assertFalse(out["success"])
        self.assertEqual(out["reason"], "invalid_quantity")

    def test_sale_requires_both_whitelist_and_price_rule(self):
        item = ShopItem(item_id=1, item_type=16, base_cost=100)
        no_list = simulate_sale(
            item=item,
            sell_quantity=1,
            current_gold=0,
            max_gold=1000,
            whitelisted=False,
            normal_sell_rate=0.2,
        )
        self.assertEqual(no_list["reason"], "not_whitelisted")

        no_rate = simulate_sale(
            item=item,
            sell_quantity=1,
            current_gold=0,
            max_gold=1000,
            whitelisted=True,
            normal_sell_rate=None,
        )
        self.assertEqual(no_rate["reason"], "no_sell_rate")


if __name__ == "__main__":
    unittest.main()
