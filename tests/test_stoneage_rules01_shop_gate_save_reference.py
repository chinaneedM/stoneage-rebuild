"""RULES-01 concrete model join, using explicitly invented item/gold/NPC data.

The backed-up bytes below prove modern-reference save/reentry, not an original
TW1.0/JSS1999 commercial server, shop catalog, NPC award or dialogue script.
"""
from dataclasses import replace
from pathlib import Path
from types import MappingProxyType
from tempfile import TemporaryDirectory
import unittest

from tools.stoneage_item_shop_model import simulate_purchase
from tools.stoneage_local_filesystem_persistence import LocalFilesystemPersistenceStore
from tools.stoneage_local_runtime_core import (
    LocalRuntimeSessionState, ResolvedTransitionBinding,
    decode_local_runtime_session, encode_local_runtime_session,
    load_runtime_bootstrap_file,
)
from tools.stoneage_recovered25_world_profile_adapter import (
    HOMETOWN_TRANSITION_IDS, Recovered25TransitionGateEvaluator,
)
from tools.stoneage_rules01_shop_gate_reference import (
    BoundedOrdinaryShopOffer, apply_normal_single_item_purchase,
)
from tools.stoneage_singleplayer_domain import (
    InventoryItem, InventorySlot, ItemTemplateId, MapPosition,
    PersistentPlayerState, PlayerState,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ITEM = 12345  # deliberately invented; NOT an actual recovered item ID


class Rules01OwnedItemGateSave(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = load_runtime_bootstrap_file(
            ROOT / "game/RUNTIME-BOOTSTRAP-RECOVERED25-R1.json"
        )
        cls.contract = cls.profile.transitions[HOMETOWN_TRANSITION_IDS[3]]
        cls.binding = ResolvedTransitionBinding(
            transition_id=cls.contract.transition_id,
            source=MapPosition(3006, 1, 1),
            destination=MapPosition(1006, 1, 1),
            predicate_payload={
                "interaction_kind": "DIALOGUE_WARPMAN",
                "gate_kind": "FREE_CLAUSES",
                "free_clauses": (({"key": "ITEM", "operator": "=", "operand": FIXTURE_ITEM},),),
            },
            provenance={"source_profile": "recovered25", "source_kind": "INVENTED_TEST_FIXTURE"},
        )
        cls.evaluator = Recovered25TransitionGateEvaluator(cls.profile)

    def session(self, gold=300, level=5, with_gold=True):
        fields = {"name": "INVENTED_TEST_ACTOR", "level": level}
        if with_gold:
            fields["gold"] = gold
        state = PersistentPlayerState(character=PlayerState(MappingProxyType(fields)))
        return LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile="recovered25",
            hometown_ordinal=3,
            player_position=MapPosition(3006, 1, 1),
            player_state=state,
        )

    def offer(self, *, item_id=FIXTURE_ITEM, offered_id=FIXTURE_ITEM,
              capacity=15, price=70, rate=0.5):
        return BoundedOrdinaryShopOffer(
            source_profile="recovered25",
            evidence_role="LATER_RECOVERED",
            source_receipt="INVENTED_RULES01_TEST_FIXTURE_NOT_HISTORICAL",
            offered_item_id=offered_id,
            selected_item_id=item_id,
            item_view={"fixture": "invented", "not_historical": True},
            base_cost=price,
            buy_rate=rate,
            usable_slot_count=capacity,
        )

    def gate(self, session):
        return self.evaluator.evaluate_transition(
            self.contract, self.binding, session
        )

    def test_purchase_owned_item_gate_real_disk_round_trip_and_revocation(self):
        before = self.session(gold=100)
        self.assertFalse(self.gate(before).allowed)
        self.assertEqual(dict(before.player_state.inventory), {})
        purchased = apply_normal_single_item_purchase(before, self.offer())
        self.assertTrue(purchased.purchased)
        self.assertEqual(purchased.inventory_slot, 0)
        self.assertTrue(self.gate(purchased.session).allowed)
        self.assertEqual(before.player_state.character.fields["gold"], 100)
        self.assertEqual(dict(before.player_state.inventory), {})
        self.assertEqual(purchased.session.player_state.character.fields["gold"], 65)
        self.assertEqual(
            purchased.session.player_state.inventory[InventorySlot(0)].template_id.value,
            FIXTURE_ITEM,
        )
        self.assertEqual(dict(self.gate(purchased.session).consumed_state), {})
        self.assertFalse(purchased.original_commercial_save_proven)
        self.assertFalse(purchased.original_quest_award_proven)

        with TemporaryDirectory() as folder:
            writer = LocalFilesystemPersistenceStore(Path(folder))
            writer.save("INVENTED_CHAR_01", encode_local_runtime_session(purchased.session))
            reader = LocalFilesystemPersistenceStore(Path(folder))
            loaded = reader.load("INVENTED_CHAR_01")
            self.assertIsNotNone(loaded)
            reentered = decode_local_runtime_session(
                loaded,
                expected_contract_id=self.profile.contract_id,
                expected_world_profile="recovered25",
            )
        self.assertEqual(reentered.player_state.character.fields["gold"], 65)
        self.assertTrue(self.gate(reentered).allowed)
        self.assertEqual(
            reentered.player_state.inventory[InventorySlot(0)].view["fixture"],
            "invented",
        )
        del reentered.player_state.inventory[InventorySlot(0)]
        self.assertFalse(self.gate(reentered).allowed)
        self.assertFalse(self.gate(before).allowed)

    def test_insufficient_funds_and_inventory_full_have_no_mutation(self):
        underfunded = self.session(gold=34)
        out = apply_normal_single_item_purchase(underfunded, self.offer())
        self.assertFalse(out.purchased)
        self.assertEqual(out.reason, "not_enough_gold")
        self.assertIs(out.session, underfunded)
        self.assertFalse(self.gate(out.session).allowed)

        full = self.session(gold=100)
        for i in range(2):
            slot = InventorySlot(i)
            full.player_state.inventory[slot] = InventoryItem(
                slot, ItemTemplateId(567 + i), MappingProxyType({"fixture": True})
            )
        result = apply_normal_single_item_purchase(full, self.offer(capacity=2))
        self.assertFalse(result.purchased)
        self.assertEqual(result.reason, "no_capacity_or_invalid_quantity")
        self.assertIs(result.session, full)
        self.assertEqual(full.player_state.character.fields["gold"], 100)
        self.assertFalse(self.gate(full).allowed)

    def test_source_catalog_and_state_gaps_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "shop offer"):
            self.offer(offered_id=99999)
        with self.assertRaisesRegex(ValueError, "later recovered25"):
            replace(self.offer(), source_profile="taiwan-v1.0")
        with self.assertRaisesRegex(ValueError, "later recovered25"):
            replace(self.offer(), evidence_role="V1_DIRECT")
        with self.assertRaisesRegex(ValueError, "receipt"):
            replace(self.offer(), source_receipt="")
        with self.assertRaisesRegex(ValueError, "capacity"):
            self.offer(capacity=21)
        with self.assertRaisesRegex(ValueError, "rate"):
            self.offer(rate=float("nan"))
        with self.assertRaisesRegex(ValueError, "state is unavailable"):
            apply_normal_single_item_purchase(self.session(with_gold=False), self.offer())
        with self.assertRaisesRegex(ValueError, "differs"):
            apply_normal_single_item_purchase(
                replace(self.session(), world_profile="taiwan-v1.0"), self.offer()
            )

    def test_price_rounding_and_item_gate_cannot_be_world_flag(self):
        original = self.session(gold=41)
        forged = replace(original, world_flags=frozenset({"ITEM:12345"}))
        self.assertFalse(self.gate(forged).allowed)
        result = apply_normal_single_item_purchase(forged, self.offer(price=83, rate=0.5))
        self.assertTrue(result.purchased)
        self.assertEqual(result.session.player_state.character.fields["gold"], 0)
        self.assertTrue(self.gate(result.session).allowed)
        self.assertEqual(
            simulate_purchase(
                gold=41, base_cost=83, requested_quantity=1,
                empty_inventory_slots=15, buy_rate=0.5,
            )["gold_after"], 0
        )


if __name__ == "__main__":
    unittest.main()
