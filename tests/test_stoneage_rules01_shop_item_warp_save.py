"""RULES-01 bounded shop -> owned item -> conditional WarpMan -> local save.

All item IDs, amounts, coordinates and the in-memory NPC fixture are invented.
The real descendant-evidence shop model, recovered25 ITEM/FREE gate evaluator,
coordinator dispatch and local persistence codecs execute together. This is
NOT an original commercial NPC/quest/server replay or a TW1.0 membership claim.
"""
import unittest
from pathlib import Path
from types import MappingProxyType, SimpleNamespace

from tools.stoneage_item_shop_model import simulate_purchase
from tools.stoneage_local_runtime_core import (
    FreshStartSeed, ResolvedTransitionBinding, load_runtime_bootstrap_file,
)
from tools.stoneage_local_runtime_session_coordinator import (
    InMemoryLocalPersistenceStore, LocalRuntimeSessionCoordinator,
)
from tools.stoneage_recovered25_world_profile_adapter import (
    HOMETOWN_TRANSITION_IDS, Recovered25TransitionGateEvaluator,
)
from tools.stoneage_rules01_shop_item_ownership import apply_reference_normal_shop_purchase
from tools.stoneage_singleplayer_domain import (
    InventoryItem, InventorySlot, ItemTemplateId, MapPosition,
    PersistentPlayerState, PlayerState,
)
from tools.stoneage_singleplayer_world import (
    HistoricalMapDefinition, HistoricalWorldTopology,
)

ROOT = Path(__file__).resolve().parents[1]
PROFILE = load_runtime_bootstrap_file(
    ROOT / "game" / "RUNTIME-BOOTSTRAP-RECOVERED25-R1.json"
)
TEST_ITEM = 99901  # invented test token; not an original item identity


class _SyntheticSourceStack:
    """Two tiny invented maps, one source-shaped item-gated transition."""

    def __init__(self):
        self.profile = PROFILE
        self.world_adapter = SimpleNamespace(
            topology=HistoricalWorldTopology(
                maps={
                    1: HistoricalMapDefinition(1, 3, 3),
                    2: HistoricalMapDefinition(2, 3, 3),
                },
                legacy_warps=(),
            )
        )
        self.transition_id = HOMETOWN_TRANSITION_IDS[3]
        self.contract = PROFILE.transitions[self.transition_id]
        self.binding = ResolvedTransitionBinding(
            transition_id=self.transition_id,
            source=MapPosition(1, 1, 1),
            destination=MapPosition(2, 1, 1),
            predicate_payload={
                "interaction_kind": "DIALOGUE_WARPMAN",
                "source_rect": (1, 1, 1, 1),
                "gate_kind": "FREE_CLAUSES",
                "free_clauses": (({"key": "ITEM", "operator": "=", "operand": TEST_ITEM},),),
                "item_template_id": TEST_ITEM,
            },
            provenance={
                "source_profile": "recovered25",
                "evidence_role": "SYNTHETIC_RULES01_FIXTURE",
            },
        )
        # Discovery enumerates all declared transitions. Unselected entries
        # have valid but offscreen synthetic bindings, not missing contracts.
        self.bindings = {self.transition_id: self.binding}
        for tid in PROFILE.transitions:
            if tid == self.transition_id:
                continue
            self.bindings[tid] = ResolvedTransitionBinding(
                transition_id=tid,
                source=MapPosition(2, 2, 2),
                destination=MapPosition(2, 1, 1),
                predicate_payload={
                    "interaction_kind": "DIALOGUE_WARPMAN",
                    "source_rect": (2, 2, 2, 2),
                    "gate_kind": "FREE_CLAUSES",
                    "free_clauses": (({"key": "ITEM", "operator": "=", "operand": TEST_ITEM},),),
                },
                provenance={"source_profile": "recovered25",
                            "evidence_role": "SYNTHETIC_RULES01_FIXTURE"},
            )
        self.evaluator = Recovered25TransitionGateEvaluator(PROFILE)

    def create_fresh_start(self, ordinal):
        if ordinal != 3:
            raise ValueError("fixture only supports ordinal 3")
        return FreshStartSeed(
            contract_id=PROFILE.contract_id,
            world_profile="recovered25",
            hometown_ordinal=ordinal,
            position=MapPosition(1, 1, 1),
            player_state=PersistentPlayerState(
                character=PlayerState(MappingProxyType({
                    "name": "invented-player", "level": 10,
                    "gold": 300, "exp": 7,
                }))
            ),
        )

    def resolve_transition(self, transition_id):
        return self.bindings[transition_id]

    def evaluate_transition(self, transition_id, session):
        return self.evaluator.evaluate_transition(
            PROFILE.transitions[transition_id], self.resolve_transition(transition_id), session
        )


def _purchase(session, **overrides):
    kw = dict(
        item_template_id=TEST_ITEM,
        item_view={"synthetic_test_marker": True},
        base_cost=80,
        buy_rate=1.25,
        inventory_capacity=15,
        source_ref="SYNTHETIC_FIXTURE_NOT_ORIGINAL_ITEMSHOP",
        source_profile="recovered25",
        evidence_role="LATER_RECOVERED",
    )
    kw.update(overrides)
    return apply_reference_normal_shop_purchase(session, **kw)


class Rules01ShopItemGateSave(unittest.TestCase):
    def setUp(self):
        self.stack = _SyntheticSourceStack()
        self.store = InMemoryLocalPersistenceStore()
        self.coordinator = LocalRuntimeSessionCoordinator(
            stack=self.stack, persistence=self.store,
        )
        self.start = self.coordinator.new_game(3)

    def test_purchase_unlocks_gate_and_survives_save_reload_without_reward_invention(self):
        tid = self.stack.transition_id
        denied = self.coordinator.execute_state_gated_transition(self.start, tid)
        self.assertFalse(denied.decision.allowed)
        self.assertIs(denied.session, self.start)

        bought = _purchase(self.start)
        self.assertTrue(bought.purchased)
        self.assertEqual(bought.item_slot, 0)
        self.assertEqual(bought.total_price, 100)
        owned = bought.session
        self.assertEqual(owned.player_state.character.fields["gold"], 200)
        self.assertEqual(self.start.player_state.character.fields["gold"], 300)
        self.assertFalse(self.start.player_state.inventory)
        self.assertEqual(
            owned.player_state.inventory[InventorySlot(0)].template_id.value,
            TEST_ITEM,
        )
        self.assertEqual(owned.player_state.character.fields["exp"], 7)
        self.assertEqual(owned.world_flags, frozenset())

        live = self.coordinator.discover_state_gated_interactions(owned)
        selected = next(x for x in live if x.transition_id == tid)
        self.assertTrue(selected.allowed)
        self.assertTrue(selected.execution_supported)

        self.coordinator.save_game("before-gate", owned)
        restarted = LocalRuntimeSessionCoordinator(self.stack, self.store)
        loaded = restarted.continue_game("before-gate")
        self.assertEqual(loaded.player_state.character.fields["gold"], 200)
        self.assertEqual(
            loaded.player_state.inventory[InventorySlot(0)].template_id.value,
            TEST_ITEM,
        )
        self.assertTrue(
            restarted.stack.evaluate_transition(tid, loaded).allowed
        )
        reached = restarted.dispatch_state_gated_interaction(loaded, tid)
        self.assertTrue(reached.decision.allowed)
        self.assertEqual(dict(reached.decision.consumed_state), {})
        self.assertEqual(reached.session.player_position, MapPosition(2, 1, 1))
        self.assertEqual(reached.session.player_state.character.fields["exp"], 7)
        self.assertEqual(reached.session.world_flags, frozenset())
        restarted.save_game("after-gate", reached.session)
        again = LocalRuntimeSessionCoordinator(self.stack, self.store)
        after = again.continue_game("after-gate")
        self.assertEqual(after.player_position, MapPosition(2, 1, 1))
        self.assertEqual(after.player_state.character.fields["gold"], 200)
        self.assertEqual(
            after.player_state.inventory[InventorySlot(0)].template_id.value,
            TEST_ITEM,
        )

    def test_unaffordable_failed_purchase_cannot_grant_gate_access(self):
        from dataclasses import replace
        fields = dict(self.start.player_state.character.fields)
        fields["gold"] = 99
        poor = replace(self.start, player_state=PersistentPlayerState(
            character=PlayerState(MappingProxyType(fields)),
        ))
        result = _purchase(poor)
        self.assertFalse(result.purchased)
        self.assertEqual(result.reason, "not_enough_gold")
        self.assertIs(result.session, poor)
        self.assertFalse(
            self.stack.evaluate_transition(self.stack.transition_id, result.session).allowed
        )

    def test_capacity_and_wrong_item_do_not_invent_unlock(self):
        full = self.start.player_state
        for i in range(15):
            slot = InventorySlot(i)
            full.inventory[slot] = InventoryItem(
                slot, ItemTemplateId(80000 + i), MappingProxyType({})
            )
        denied = _purchase(self.start)
        self.assertFalse(denied.purchased)
        self.assertEqual(denied.reason, "no_capacity_or_invalid_quantity")
        self.assertIs(denied.session, self.start)
        self.assertEqual(self.start.player_state.character.fields["gold"], 300)
        self.assertFalse(
            self.stack.evaluate_transition(self.stack.transition_id, self.start).allowed
        )

    def test_explicit_source_identity_and_price_requirements(self):
        for change in (
            {"source_ref": ""},
            {"source_profile": "taiwan-v1.0"},
            {"evidence_role": "V1_DIRECT"},
            {"buy_rate": -1},
            {"inventory_capacity": 21},
            {"base_cost": -5},
        ):
            with self.subTest(change=change), self.assertRaises(ValueError):
                _purchase(self.start, **change)
        with self.assertRaises(ValueError):
            from dataclasses import replace
            _purchase(replace(self.start, player_state=PersistentPlayerState(
                character=PlayerState(MappingProxyType({"level": 10}))
            )))
        wrong = _purchase(self.start, item_template_id=TEST_ITEM + 1)
        self.assertTrue(wrong.purchased)
        self.assertFalse(
            self.stack.evaluate_transition(self.stack.transition_id, wrong.session).allowed
        )

    def test_legacy_partial_failure_remains_separate_from_success_only_adapter(self):
        legacy = simulate_purchase(
            gold=300, base_cost=80, requested_quantity=3,
            empty_inventory_slots=3, buy_rate=1.0, fail_add_at=1,
        )
        self.assertFalse(legacy["success"])
        self.assertEqual(legacy["items_added"], 1)
        self.assertEqual(legacy["gold_after"], 300)
        self.assertNotEqual(legacy["reason"], "purchased")
        # This deliberately does not run through the successful-only adapter.


if __name__ == "__main__":
    unittest.main()
