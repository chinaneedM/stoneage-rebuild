import unittest

from tools.stoneage_trade_economy_model import (
    ItemOffer,
    Offer,
    PetOffer,
    PROTOCOL_OLD,
    PROTOCOL_TRADESYSTEM2,
    TRADE_FREE,
    TRADE_LOCK,
    TRADE_TRADING,
    begin_trade,
    can_modify_offer,
    can_search_trade,
    cancel_trade,
    confirm,
    final_gold_balances,
    incoming_item_slots_needed_source,
    is_transactionally_atomic,
    preflight_trade,
    request_final_lock,
    source_item_slots_freed,
    structured_mutation_order,
    target_trade_eligible,
    transfer_pet_owner,
    validate_gold_offer,
    validate_pet_offer,
)


class TradeEconomyModelTests(unittest.TestCase):
    def test_active_start_enters_trading_directly(self):
        left, right = begin_trade()
        self.assertEqual(left.mode, TRADE_TRADING)
        self.assertEqual(right.mode, TRADE_TRADING)
        self.assertFalse(left.confirmed)

    def test_search_requires_standalone_nonbattle_state(self):
        self.assertTrue(can_search_trade(mode=TRADE_FREE, in_party=False, in_battle=False))
        self.assertFalse(can_search_trade(mode=TRADE_TRADING, in_party=False, in_battle=False))
        self.assertFalse(can_search_trade(mode=TRADE_FREE, in_party=True, in_battle=False))

    def test_target_must_be_player_trade_enabled_free_and_standalone(self):
        self.assertTrue(
            target_trade_eligible(
                is_player=True,
                is_self=False,
                in_party=False,
                in_battle=False,
                trade_enabled=True,
                mode=TRADE_FREE,
            )
        )
        self.assertFalse(
            target_trade_eligible(
                is_player=True,
                is_self=False,
                in_party=False,
                in_battle=False,
                trade_enabled=False,
                mode=TRADE_FREE,
            )
        )

    def test_confirmation_freezes_own_offer(self):
        left, _ = begin_trade()
        self.assertTrue(can_modify_offer(left))
        left = confirm(left)
        self.assertFalse(can_modify_offer(left))

    def test_new_protocol_requires_both_confirm_then_both_lock(self):
        left, right = begin_trade()
        left = confirm(left)
        right = confirm(right)

        left, execute = request_final_lock(left, right, PROTOCOL_TRADESYSTEM2)
        self.assertEqual(left.mode, TRADE_LOCK)
        self.assertFalse(execute)

        right, execute = request_final_lock(right, left, PROTOCOL_TRADESYSTEM2)
        self.assertEqual(right.mode, TRADE_LOCK)
        self.assertTrue(execute)

    def test_old_protocol_k_can_confirm_then_first_lock_after_both_confirms_executes(self):
        left, right = begin_trade()
        left, execute = request_final_lock(left, right, PROTOCOL_OLD)
        self.assertTrue(left.confirmed)
        self.assertFalse(execute)

        right = confirm(right)
        left, execute = request_final_lock(left, right, PROTOCOL_OLD)
        self.assertTrue(execute)
        self.assertEqual(left.mode, TRADE_LOCK)

    def test_cancel_resets_both_sides(self):
        left, right = cancel_trade()
        self.assertEqual(left.mode, TRADE_FREE)
        self.assertEqual(right.mode, TRADE_FREE)
        self.assertFalse(left.confirmed)
        self.assertFalse(right.confirmed)

    def test_gold_offer_cannot_exceed_current_carried_gold(self):
        self.assertTrue(validate_gold_offer(100, 100))
        self.assertFalse(validate_gold_offer(101, 100))
        self.assertFalse(validate_gold_offer(-1, 100))

    def test_old_pet_care_gate_is_plus_five_with_reborn_or_pickall_bypass(self):
        pet = PetOffer(slot=2, level=16)
        self.assertFalse(validate_pet_offer(pet, receiver_level=10, max_level_delta=5))
        self.assertTrue(validate_pet_offer(pet, receiver_level=10, receiver_transmigration=1))
        self.assertTrue(validate_pet_offer(pet, receiver_level=10, receiver_pick_all_pet=True))
        self.assertTrue(validate_pet_offer(pet, receiver_level=10, max_level_delta=20))

    def test_family_guardian_pet_is_not_tradeable(self):
        pet = PetOffer(slot=1, level=1, family_guardian=True)
        self.assertFalse(validate_pet_offer(pet, receiver_level=99))

    def test_only_full_outgoing_stack_frees_inventory_slot(self):
        offer = Offer(
            items=(
                ItemOffer(slot=10, quantity=5, stack_count=5),
                ItemOffer(slot=11, quantity=2, stack_count=5),
            )
        )
        self.assertEqual(source_item_slots_freed(offer), 1)

    def test_source_capacity_formula_overcounts_exact_multiple(self):
        self.assertEqual(incoming_item_slots_needed_source(10, 10), 1)
        self.assertEqual(incoming_item_slots_needed_source(11, 10), 2)
        self.assertEqual(incoming_item_slots_needed_source(20, 10), 3)

    def test_preflight_accounts_for_outgoing_slots_before_incoming_items_and_pets(self):
        left = Offer(
            items=(ItemOffer(slot=10, quantity=1, stack_count=1),),
            pets=(PetOffer(slot=0, level=5),),
            gold=100,
        )
        right = Offer(
            items=(ItemOffer(slot=12, quantity=1, stack_count=1),),
            pets=(PetOffer(slot=1, level=5),),
            gold=50,
        )
        ok, reason = preflight_trade(
            left_offer=left,
            right_offer=right,
            left_empty_item_slots=0,
            right_empty_item_slots=0,
            left_max_pile=10,
            right_max_pile=10,
            left_empty_pet_slots=0,
            right_empty_pet_slots=0,
            left_gold=900,
            right_gold=950,
            left_max_gold=1000,
            right_max_gold=1000,
        )
        self.assertTrue(ok, reason)

    def test_gold_preflight_uses_net_posttrade_capacity(self):
        left = Offer(gold=100)
        right = Offer(gold=300)
        ok, reason = preflight_trade(
            left_offer=left,
            right_offer=right,
            left_empty_item_slots=0,
            right_empty_item_slots=0,
            left_max_pile=10,
            right_max_pile=10,
            left_empty_pet_slots=0,
            right_empty_pet_slots=0,
            left_gold=900,
            right_gold=500,
            left_max_gold=1000,
            right_max_gold=1000,
        )
        self.assertFalse(ok)
        self.assertEqual(reason, "left_gold_overflow")

    def test_successful_gold_transfer_nets_both_offers(self):
        self.assertEqual(final_gold_balances(500, 700, 100, 50), (450, 750))

    def test_execution_is_preflight_then_destructive_not_rollback_atomic(self):
        self.assertFalse(is_transactionally_atomic())
        self.assertEqual(
            structured_mutation_order()[0:6],
            (
                "remove_left_items",
                "remove_right_items",
                "remove_left_pets",
                "remove_right_pets",
                "subtract_left_gold",
                "subtract_right_gold",
            ),
        )

    def test_pet_owner_metadata_moves_to_receiver(self):
        pet = {"id": 1, "player_index": 10, "owner_cdkey": "old", "owner_name": "old"}
        moved = transfer_pet_owner(pet, 20, "newkey", "newname")
        self.assertEqual(moved["player_index"], 20)
        self.assertEqual(moved["owner_cdkey"], "newkey")
        self.assertEqual(moved["owner_name"], "newname")
        self.assertTrue(moved["parameters_recomputed"])


if __name__ == "__main__":
    unittest.main()
