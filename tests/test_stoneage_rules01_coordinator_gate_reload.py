"""RULES-01: real coordinator transition and second local save/reload.

Only invented compact fixture data is used. No original TW1.0/1999 quest or
commercial-server persistence is claimed. Uses the already-accepted shop
adapter (no duplicate shop implementation), actual recovered25 FREE evaluator,
actual coordinator dispatch and two fresh filesystem store instances.
"""
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
from types import MappingProxyType, SimpleNamespace
import unittest

from tools.stoneage_local_filesystem_persistence import LocalFilesystemPersistenceStore
from tools.stoneage_local_runtime_core import (
    FreshStartSeed, ResolvedTransitionBinding, load_runtime_bootstrap_file,
)
from tools.stoneage_local_runtime_session_coordinator import LocalRuntimeSessionCoordinator
from tools.stoneage_recovered25_world_profile_adapter import (
    HOMETOWN_TRANSITION_IDS, Recovered25TransitionGateEvaluator,
)
from tools.stoneage_rules01_shop_gate_reference import (
    BoundedOrdinaryShopOffer, apply_normal_single_item_purchase,
)
from tools.stoneage_singleplayer_domain import (
    InventorySlot, MapPosition, PersistentPlayerState, PlayerState,
)
from tools.stoneage_singleplayer_world import (
    HistoricalMapDefinition, HistoricalWorldTopology,
)

ROOT = Path(__file__).resolve().parents[1]
PROFILE = load_runtime_bootstrap_file(
    ROOT / "game" / "RUNTIME-BOOTSTRAP-RECOVERED25-R1.json"
)
TEST_ITEM = 99901  # invented numeric identity, not recovered commercial data


class _SyntheticCoordinatorStack:
    """All declared transitions are bound, only hometown 3 is in reach."""

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
        self.selected_id = HOMETOWN_TRANSITION_IDS[3]
        self.bindings = {}
        for tid in PROFILE.transitions:
            selected = tid == self.selected_id
            self.bindings[tid] = ResolvedTransitionBinding(
                transition_id=tid,
                source=MapPosition(1, 1, 1) if selected else MapPosition(2, 2, 2),
                destination=MapPosition(2, 1, 1),
                predicate_payload={
                    "interaction_kind": "DIALOGUE_WARPMAN",
                    "source_rect": (1, 1, 1, 1) if selected else (2, 2, 2, 2),
                    "gate_kind": "FREE_CLAUSES",
                    "free_clauses": ((
                        {"key": "ITEM", "operator": "=", "operand": TEST_ITEM},
                    ),),
                    "item_template_id": TEST_ITEM,
                },
                provenance={
                    "source_profile": "recovered25",
                    "source_kind": "INVENTED_RULES01_COORDINATOR_TEST_FIXTURE",
                },
            )
        self.gate = Recovered25TransitionGateEvaluator(PROFILE)

    def create_fresh_start(self, hometown_ordinal):
        if int(hometown_ordinal) != 3:
            raise ValueError("synthetic coordinator supports only ordinal 3")
        return FreshStartSeed(
            contract_id=PROFILE.contract_id,
            world_profile="recovered25",
            hometown_ordinal=3,
            position=MapPosition(1, 1, 1),
            player_state=PersistentPlayerState(
                character=PlayerState(MappingProxyType({
                    "name": "invented-fixture-player", "level": 10,
                    "gold": 300, "exp": 7,
                }))
            ),
        )

    def resolve_transition(self, transition_id):
        return self.bindings[transition_id]

    def evaluate_transition(self, transition_id, session):
        return self.gate.evaluate_transition(
            self.profile.transitions[transition_id],
            self.resolve_transition(transition_id),
            session,
        )


def _synthetic_offer(item_id=TEST_ITEM):
    return BoundedOrdinaryShopOffer(
        source_profile="recovered25",
        evidence_role="LATER_RECOVERED",
        source_receipt="INVENTED_COORDINATOR_SHOP_GATE_TEST_NOT_ORIGINAL",
        offered_item_id=item_id,
        selected_item_id=item_id,
        item_view={"invented_test_only": True},
        base_cost=80,
        buy_rate=1.25,
        usable_slot_count=15,
    )


class Rules01CoordinatorPurchaseWarpSave(unittest.TestCase):
    def setUp(self):
        self.root = TemporaryDirectory()
        self.addCleanup(self.root.cleanup)
        self.folder = Path(self.root.name)
        self.stack = _SyntheticCoordinatorStack()

    def _coordinator(self):
        return LocalRuntimeSessionCoordinator(
            self.stack, LocalFilesystemPersistenceStore(self.folder)
        )

    def test_real_coordinator_purchase_gate_dispatch_double_disk_reload(self):
        coordinator = self._coordinator()
        at_start = coordinator.new_game(3)
        tid = self.stack.selected_id
        self.assertFalse(
            coordinator.dispatch_state_gated_interaction(at_start, tid).decision.allowed
        )
        self.assertEqual(coordinator.discover_state_gated_interactions(at_start)[0].allowed, False)
        self.assertEqual(at_start.player_position, MapPosition(1, 1, 1))

        bought = apply_normal_single_item_purchase(at_start, _synthetic_offer())
        self.assertTrue(bought.purchased)
        self.assertFalse(bought.original_quest_award_proven)
        self.assertFalse(bought.original_commercial_save_proven)
        self.assertEqual(bought.inventory_slot, 0)
        self.assertEqual(at_start.player_state.character.fields["gold"], 300)
        self.assertEqual(bought.session.player_state.character.fields["gold"], 200)
        self.assertEqual(
            bought.session.player_state.inventory[InventorySlot(0)].template_id.value,
            TEST_ITEM,
        )
        coordinator.save_game("purchased", bought.session)

        reopened = self._coordinator()
        from_disk = reopened.continue_game("purchased")
        self.assertEqual(from_disk.player_state.character.fields["gold"], 200)
        self.assertEqual(from_disk.player_state.character.fields["exp"], 7)
        self.assertTrue(reopened.discover_state_gated_interactions(from_disk)[0].allowed)
        transition = reopened.dispatch_state_gated_interaction(from_disk, tid)
        self.assertTrue(transition.decision.allowed)
        self.assertEqual(dict(transition.decision.consumed_state), {})
        self.assertEqual(transition.session.player_position, MapPosition(2, 1, 1))
        self.assertEqual(transition.session.world_flags, frozenset())
        self.assertEqual(transition.session.player_state.character.fields["gold"], 200)
        reopened.save_game("transitioned", transition.session)

        third = self._coordinator()
        final = third.continue_game("transitioned")
        self.assertEqual(final.player_position, MapPosition(2, 1, 1))
        self.assertEqual(final.player_state.character.fields["gold"], 200)
        self.assertEqual(final.player_state.character.fields["exp"], 7)
        self.assertEqual(final.world_flags, frozenset())
        self.assertEqual(
            final.player_state.inventory[InventorySlot(0)].template_id.value,
            TEST_ITEM,
        )
        self.assertEqual(
            final.player_state.inventory[InventorySlot(0)].view["invented_test_only"],
            True,
        )
        self.assertEqual(third.discover_state_gated_interactions(final), ())

    def test_world_flag_cannot_impersonate_owned_item_after_disk_reload(self):
        coordinator = self._coordinator()
        start = coordinator.new_game(3)
        forged = replace(start, world_flags=frozenset({f"ITEM:{TEST_ITEM}"}))
        coordinator.save_game("flag-only", forged)
        again = self._coordinator()
        loaded = again.continue_game("flag-only")
        self.assertFalse(
            again.dispatch_state_gated_interaction(
                loaded, self.stack.selected_id
            ).decision.allowed
        )
        self.assertFalse(loaded.player_state.inventory)
        self.assertEqual(loaded.player_state.character.fields["gold"], 300)

    def test_nonmatching_item_persists_but_does_not_unlock(self):
        coordinator = self._coordinator()
        start = coordinator.new_game(3)
        other = apply_normal_single_item_purchase(start, _synthetic_offer(TEST_ITEM + 1))
        self.assertTrue(other.purchased)
        coordinator.save_game("other-item", other.session)
        again = self._coordinator()
        loaded = again.continue_game("other-item")
        self.assertFalse(
            again.dispatch_state_gated_interaction(
                loaded, self.stack.selected_id
            ).decision.allowed
        )
        self.assertEqual(loaded.player_state.character.fields["gold"], 200)
        self.assertEqual(
            loaded.player_state.inventory[InventorySlot(0)].template_id.value,
            TEST_ITEM + 1,
        )


if __name__ == "__main__":
    unittest.main()
