import inspect
import unittest
from pathlib import Path
from types import MappingProxyType, SimpleNamespace

from tools.stoneage_local_application_facade import LocalApplicationFacade
from tools.stoneage_local_engine_adapter import (
    LOCAL_ENGINE_ADAPTER_PROFILE,
    ContinueGameIntent,
    DispatchInteractionIntent,
    LocalEngineAdapter,
    MoveIntent,
    NewGameIntent,
    RefreshViewIntent,
    SaveGameIntent,
)
from tools.stoneage_local_runtime_core import (
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
from tools.stoneage_map_collision_model import CollisionDecision
from tools.stoneage_singleplayer_domain import (
    MapPosition,
    PersistentPlayerState,
    PlayerState,
)
from tools.stoneage_singleplayer_world import (
    HistoricalMapDefinition,
    HistoricalWorldTopology,
)

ROOT = Path(__file__).resolve().parents[1]


class _Stack:
    def __init__(self, profile):
        self.profile = profile
        self.world_adapter = SimpleNamespace(
            topology=HistoricalWorldTopology(
                maps={1: HistoricalMapDefinition(1, 4, 4)},
                legacy_warps=(),
            )
        )
        self.collision_router = SimpleNamespace(
            routed_step_verdict=lambda **_kwargs: SimpleNamespace(
                decision=CollisionDecision(True, "test_static_allowed"),
                route=SimpleNamespace(
                    provider_kind="TEST_STATIC",
                    evidence_class="TEST",
                    semantic_profile="TEST_STATIC_R1",
                    exact_recovered25_binary_proof=None,
                ),
            )
        )
        self.bindings = {
            transition_id: ResolvedTransitionBinding(
                transition_id=transition_id,
                source=MapPosition(1, 1, 0),
                destination=MapPosition(1, 2, 2),
                predicate_payload={
                    "interaction_kind": "DIALOGUE_WARPMAN",
                    "source_rect": (1, 0, 1, 0),
                },
                provenance={"source_profile": "test"},
            )
            for transition_id in profile.transitions
        }

    def create_fresh_start(self, ordinal):
        return SimpleNamespace(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=int(ordinal),
            position=MapPosition(1, 0, 0),
            player_state=PersistentPlayerState(
                character=PlayerState(
                    MappingProxyType({"name": "adapter-test", "level": 1})
                )
            ),
        )

    def materialize_player_position(self, session):
        p = session.player_position
        return MaterializedWorldRegion(
            request=WorldRegionRequest(
                floor_id=p.floor_id,
                x1=p.x,
                y1=p.y,
                x2=p.x,
                y2=p.y,
                world_profile=session.world_profile,
            ),
            payload={"cell": (p.floor_id, p.x, p.y)},
            provenance={"profile": "test"},
        )

    def resolve_transition(self, transition_id):
        return self.bindings[str(transition_id)]

    def evaluate_transition(self, transition_id, session):
        return TransitionGateDecision(
            allowed=True,
            reason="test gate allowed",
            consumed_state={},
        )


class LocalEngineAdapterTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.profile = load_runtime_bootstrap_file(
            ROOT / "game" / "RUNTIME-BOOTSTRAP-RECOVERED25-R1.json"
        )

    def setUp(self):
        coordinator = LocalRuntimeSessionCoordinator(
            stack=_Stack(self.profile),
            persistence=InMemoryLocalPersistenceStore(),
        )
        self.adapter = LocalEngineAdapter(
            LocalApplicationFacade(coordinator)
        )

    def test_adapter_contract_has_no_recovered25_or_engine_dependency(self):
        source = inspect.getsource(
            __import__(
                "tools.stoneage_local_engine_adapter",
                fromlist=["*"],
            )
        )
        import_surface = "\n".join(
            line
            for line in source.splitlines()
            if line.startswith("from ") or line.startswith("import ")
        )
        self.assertNotIn("stoneage_recovered25", import_surface)
        self.assertNotIn("Recovered25", import_surface)
        self.assertNotIn("godot", import_surface.lower())
        self.assertNotIn("unity", import_surface.lower())
        self.assertEqual(
            self.adapter.profile_id,
            LOCAL_ENGINE_ADAPTER_PROFILE,
        )

    def test_start_move_discover_and_dispatch_produce_semantic_updates(self):
        started = self.adapter.handle(NewGameIntent(1))
        self.assertEqual(started.event_kind, "NEW_GAME")
        self.assertEqual(started.view.session.player_position, MapPosition(1, 0, 0))
        self.assertEqual(started.view.interactions, ())

        moved = self.adapter.handle(MoveIntent(1, 0))
        self.assertEqual(moved.event_kind, "MOVE")
        self.assertIsNotNone(moved.walk_result)
        self.assertEqual(moved.view.session.player_position, MapPosition(1, 1, 0))
        self.assertEqual(
            tuple(row.transition_id for row in moved.view.interactions),
            tuple(sorted(self.profile.transitions)),
        )

        transition_id = moved.view.interactions[0].transition_id
        dispatched = self.adapter.handle(
            DispatchInteractionIntent(transition_id)
        )
        self.assertEqual(dispatched.event_kind, "INTERACTION")
        self.assertIsNotNone(dispatched.transition_result)
        self.assertTrue(dispatched.transition_result.decision.allowed)
        self.assertEqual(
            dispatched.view.session.player_position,
            MapPosition(1, 2, 2),
        )

    def test_save_continue_and_refresh_keep_adapter_session_authoritative(self):
        self.adapter.handle(NewGameIntent(1))
        self.adapter.handle(MoveIntent(1, 0))
        saved = self.adapter.handle(SaveGameIntent("slot"))
        self.assertEqual(saved.event_kind, "SAVE_GAME")
        self.assertEqual(saved.save_key, "slot")

        self.adapter.handle(MoveIntent(1, 0))
        self.assertEqual(
            self.adapter.session.player_position,
            MapPosition(1, 2, 0),
        )
        restored = self.adapter.handle(ContinueGameIntent("slot"))
        self.assertEqual(restored.event_kind, "CONTINUE_GAME")
        self.assertEqual(restored.save_key, "slot")
        self.assertEqual(
            restored.view.session.player_position,
            MapPosition(1, 1, 0),
        )
        refreshed = self.adapter.handle(RefreshViewIntent())
        self.assertEqual(refreshed.event_kind, "REFRESH")
        self.assertEqual(refreshed.view.session, self.adapter.session)

    def test_session_required_commands_fail_before_start(self):
        with self.assertRaisesRegex(RuntimeError, "no active session"):
            self.adapter.handle(RefreshViewIntent())
        with self.assertRaisesRegex(RuntimeError, "no active session"):
            self.adapter.handle(SaveGameIntent("slot"))
        with self.assertRaisesRegex(RuntimeError, "no active session"):
            self.adapter.handle(MoveIntent(1, 0))

    def test_move_intent_is_one_cell_semantics(self):
        with self.assertRaisesRegex(ValueError, "zero-length"):
            MoveIntent(0, 0)
        with self.assertRaisesRegex(ValueError, "one cell"):
            MoveIntent(2, 0)


if __name__ == "__main__":
    unittest.main()
