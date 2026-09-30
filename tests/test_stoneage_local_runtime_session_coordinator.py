import unittest
from pathlib import Path
from types import MappingProxyType, SimpleNamespace

from tools.stoneage_map_collision_model import CollisionDecision
from tools.stoneage_local_runtime_core import (
    FreshStartSeed,
    LocalRuntimeSessionState,
    MaterializedWorldRegion,
    ResolvedTransitionBinding,
    TransitionGateDecision,
    WorldRegionRequest,
    load_runtime_bootstrap_file,
)
from tools.stoneage_local_runtime_session_coordinator import (
    InMemoryLocalPersistenceStore,
    LocalRuntimeSessionCoordinator,
)
from tools.stoneage_singleplayer_domain import (
    MapPosition,
    PersistentPlayerState,
    PlayerState,
)
from tools.stoneage_singleplayer_world import (
    HistoricalMapDefinition,
    HistoricalWorldTopology,
    LegacyWarpEdge,
)


ROOT = Path(__file__).resolve().parents[1]


def _player_state() -> PersistentPlayerState:
    return PersistentPlayerState(
        character=PlayerState(
            MappingProxyType({"name": "coordinator-test", "level": 1})
        )
    )


class _FakeStack:
    def __init__(self, profile):
        self.profile = profile
        self.allow = True
        self.evaluation_calls = 0
        topology = HistoricalWorldTopology(
            maps={
                1: HistoricalMapDefinition(1, 3, 3),
                2: HistoricalMapDefinition(2, 3, 3),
            },
            legacy_warps=(
                LegacyWarpEdge(
                    source=MapPosition(1, 1, 0),
                    destination=MapPosition(2, 2, 2),
                ),
            ),
        )
        self.world_adapter = SimpleNamespace(topology=topology)
        self.bindings = {
            transition_id: ResolvedTransitionBinding(
                transition_id=transition_id,
                source=MapPosition(2, 1, 1),
                destination=MapPosition(1, 2, 2),
                predicate_payload={
                    "interaction_kind": "DIALOGUE_WARPMAN",
                    "source_rect": (1, 1, 2, 2),
                    "gate_kind": "TEST",
                },
                provenance={"source_profile": "recovered25"},
            )
            for transition_id in profile.transitions
        }

    def create_fresh_start(self, ordinal):
        return FreshStartSeed(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=int(ordinal),
            position=MapPosition(1, 0, 0),
            player_state=_player_state(),
        )

    def materialize_player_position(self, session):
        p = session.player_position
        request = WorldRegionRequest(
            floor_id=p.floor_id,
            x1=p.x,
            y1=p.y,
            x2=p.x,
            y2=p.y,
            world_profile=session.world_profile,
        )
        return MaterializedWorldRegion(
            request=request,
            payload={"cell": (p.floor_id, p.x, p.y)},
            provenance={"world_profile": session.world_profile},
        )

    def resolve_transition(self, transition_id):
        return self.bindings[str(transition_id)]

    def evaluate_transition(self, transition_id, session):
        self.evaluation_calls += 1
        return TransitionGateDecision(
            allowed=self.allow,
            reason=("test gate allowed" if self.allow else "test gate denied"),
            consumed_state={},
        )


class LocalRuntimeSessionCoordinatorTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.profile = load_runtime_bootstrap_file(
            ROOT / "game" / "RUNTIME-BOOTSTRAP-RECOVERED25-R1.json"
        )

    def setUp(self):
        self.stack = _FakeStack(self.profile)
        self.store = InMemoryLocalPersistenceStore()
        self.coordinator = LocalRuntimeSessionCoordinator(
            stack=self.stack,
            persistence=self.store,
        )

    def test_new_game_and_current_region_share_one_authoritative_session(self):
        session = self.coordinator.new_game(1)
        self.assertEqual(session.player_position, MapPosition(1, 0, 0))
        region = self.coordinator.materialize_current_region(session)
        self.assertEqual(region.payload["cell"], (1, 0, 0))

    def test_save_and_continue_round_trip_through_store_port(self):
        session = self.coordinator.new_game(2)
        session = LocalRuntimeSessionState(
            contract_id=session.contract_id,
            world_profile=session.world_profile,
            hometown_ordinal=session.hometown_ordinal,
            player_position=session.player_position,
            player_state=session.player_state,
            world_flags=frozenset({"opened-test-route"}),
        )
        self.coordinator.save_game("slot-1", session)
        restored = self.coordinator.continue_game("slot-1")
        self.assertEqual(restored.player_position, session.player_position)
        self.assertEqual(restored.world_flags, session.world_flags)
        self.assertIn("slot-1", self.store.rows)
        with self.assertRaises(KeyError):
            self.coordinator.continue_game("missing")

    def test_explicit_collision_verdict_controls_one_cell_walk(self):
        session = self.coordinator.new_game(1)
        blocked = self.coordinator.walk_one_cell(
            session,
            destination=MapPosition(1, 0, 1),
            entry_allowed=False,
        )
        self.assertFalse(blocked.resolution.moved)
        self.assertEqual(blocked.session.player_position, MapPosition(1, 0, 0))

        moved = self.coordinator.walk_one_cell(
            session,
            destination=MapPosition(1, 0, 1),
            entry_allowed=True,
        )
        self.assertTrue(moved.resolution.moved)
        self.assertEqual(moved.session.player_position, MapPosition(1, 0, 1))

        with self.assertRaises(ValueError):
            self.coordinator.walk_one_cell(
                session,
                destination=MapPosition(1, 2, 2),
                entry_allowed=True,
            )
        with self.assertRaises(ValueError):
            self.coordinator.walk_one_cell(
                session,
                destination=MapPosition(2, 0, 0),
                entry_allowed=True,
            )

    def test_server_collision_provider_can_drive_one_cell_walk(self):
        session = self.coordinator.new_game(1)
        self.stack.collision_provider = SimpleNamespace(
            ordinary_step_verdict=lambda **_kwargs: CollisionDecision(
                True,
                "server_static_allowed",
            )
        )
        result = self.coordinator.walk_one_cell_with_server_collision(
            session,
            destination=MapPosition(1, 0, 1),
        )
        self.assertTrue(result.resolution.moved)
        self.assertIsNotNone(result.collision)
        self.assertTrue(result.collision.allowed)
        self.assertEqual(result.session.player_position, MapPosition(1, 0, 1))

        self.stack.collision_provider = None
        with self.assertRaisesRegex(ValueError, "no server collision provider"):
            self.coordinator.walk_one_cell_with_server_collision(
                session,
                destination=MapPosition(1, 0, 1),
            )

    def test_unified_collision_router_preserves_evidence_on_walk_result(self):
        session = self.coordinator.new_game(1)
        self.stack.collision_router = SimpleNamespace(
            routed_step_verdict=lambda **_kwargs: SimpleNamespace(
                decision=CollisionDecision(True, "client_hitmap_allowed"),
                route=SimpleNamespace(
                    provider_kind="RECOVERED25_CLIENT_HITMAP_RECONSTRUCTION",
                    evidence_class=(
                        "LATER_RECOVERED_PLUS_PINNED_DESCENDANT_STABLE_ALGORITHM"
                    ),
                    semantic_profile=(
                        "RECOVERED25_DESCENDANT_STABLE_CLIENT_HITMAP_R1"
                    ),
                    exact_recovered25_binary_proof=False,
                ),
            )
        )
        result = self.coordinator.walk_one_cell_with_runtime_collision(
            session,
            destination=MapPosition(1, 0, 1),
        )
        self.assertTrue(result.resolution.moved)
        self.assertEqual(
            result.collision_provider_kind,
            "RECOVERED25_CLIENT_HITMAP_RECONSTRUCTION",
        )
        self.assertEqual(
            result.collision_semantic_profile,
            "RECOVERED25_DESCENDANT_STABLE_CLIENT_HITMAP_R1",
        )
        self.assertFalse(result.collision_exact_binary_proof)

        self.stack.collision_router = None
        with self.assertRaisesRegex(ValueError, "no unified collision router"):
            self.coordinator.walk_one_cell_with_runtime_collision(
                session,
                destination=MapPosition(1, 0, 1),
            )

    def test_classic_overlap_warp_is_reused_not_reimplemented(self):
        session = self.coordinator.new_game(1)
        result = self.coordinator.walk_one_cell(
            session,
            destination=MapPosition(1, 1, 0),
            entry_allowed=True,
        )
        self.assertTrue(result.resolution.warp_triggered)
        self.assertTrue(result.resolution.encounter_suppressed)
        self.assertEqual(result.session.player_position, MapPosition(2, 2, 2))

    def test_state_gated_transition_requires_spatial_and_live_gate_checks(self):
        transition_id = next(iter(self.profile.transitions))
        session = self.coordinator.new_game(1)

        outside = self.coordinator.execute_state_gated_transition(
            session,
            transition_id,
        )
        self.assertFalse(outside.decision.allowed)
        self.assertEqual(outside.session, session)
        self.assertEqual(self.stack.evaluation_calls, 0)

        at_gate = LocalRuntimeSessionState(
            contract_id=session.contract_id,
            world_profile=session.world_profile,
            hometown_ordinal=session.hometown_ordinal,
            player_position=MapPosition(2, 2, 2),
            player_state=session.player_state,
        )
        self.stack.allow = False
        denied = self.coordinator.execute_state_gated_transition(
            at_gate,
            transition_id,
        )
        self.assertFalse(denied.decision.allowed)
        self.assertEqual(denied.session.player_position, MapPosition(2, 2, 2))

        self.stack.allow = True
        allowed = self.coordinator.execute_state_gated_transition(
            at_gate,
            transition_id,
        )
        self.assertTrue(allowed.decision.allowed)
        self.assertEqual(allowed.session.player_position, MapPosition(1, 2, 2))

    def test_future_consumed_state_cannot_be_silently_ignored(self):
        transition_id = next(iter(self.profile.transitions))
        session = self.coordinator.new_game(1)
        at_gate = LocalRuntimeSessionState(
            contract_id=session.contract_id,
            world_profile=session.world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(2, 2, 2),
            player_state=session.player_state,
        )

        def evaluate_with_consumption(_transition_id, _session):
            return TransitionGateDecision(
                allowed=True,
                reason="future mutation",
                consumed_state={"item": 1},
            )

        self.stack.evaluate_transition = evaluate_with_consumption
        with self.assertRaises(ValueError):
            self.coordinator.execute_state_gated_transition(
                at_gate,
                transition_id,
            )


if __name__ == "__main__":
    unittest.main()
