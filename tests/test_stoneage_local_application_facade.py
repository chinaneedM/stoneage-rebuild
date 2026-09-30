import inspect
import unittest
from pathlib import Path
from types import MappingProxyType, SimpleNamespace

from tools.stoneage_local_application_facade import (
    LOCAL_APPLICATION_FACADE_PROFILE,
    LocalApplicationFacade,
)
from tools.stoneage_local_runtime_core import (
    LocalRuntimeSessionState,
    MaterializedWorldRegion,
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
                maps={1: HistoricalMapDefinition(1, 3, 3)},
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

    def create_fresh_start(self, ordinal):
        return SimpleNamespace(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=int(ordinal),
            position=MapPosition(1, 0, 0),
            player_state=PersistentPlayerState(
                character=PlayerState(
                    MappingProxyType({"name": "facade-test", "level": 1})
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
        raise AssertionError("no interaction expected in facade base smoke")

    def evaluate_transition(self, transition_id, session):
        raise AssertionError("no interaction expected in facade base smoke")


class LocalApplicationFacadeTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.profile = load_runtime_bootstrap_file(
            ROOT / "game" / "RUNTIME-BOOTSTRAP-RECOVERED25-R1.json"
        )

    def setUp(self):
        stack = _Stack(self.profile)
        self.coordinator = LocalRuntimeSessionCoordinator(
            stack=stack,
            persistence=InMemoryLocalPersistenceStore(),
        )
        self.facade = LocalApplicationFacade(self.coordinator)

    def test_facade_is_engine_neutral_and_does_not_import_recovered25_modules(self):
        source = inspect.getsource(
            __import__(
                "tools.stoneage_local_application_facade",
                fromlist=["*"],
            )
        )
        self.assertNotIn("stoneage_recovered25", source)
        self.assertNotIn("Recovered25", source)
        self.assertEqual(
            self.facade.profile_id,
            LOCAL_APPLICATION_FACADE_PROFILE,
        )

    def test_new_save_continue_and_read_region_share_authoritative_session(self):
        session = self.facade.new_game(1)
        self.assertEqual(session.player_position, MapPosition(1, 0, 0))
        view = self.facade.read_view(session)
        self.assertEqual(view.session, session)
        self.assertEqual(view.region.payload["cell"], (1, 0, 0))
        self.assertEqual(view.interactions, ())

        flagged = LocalRuntimeSessionState(
            contract_id=session.contract_id,
            world_profile=session.world_profile,
            hometown_ordinal=session.hometown_ordinal,
            player_position=session.player_position,
            player_state=session.player_state,
            world_flags=frozenset({"facade-save"}),
        )
        self.facade.save_game("slot", flagged)
        restored = self.facade.continue_game("slot")
        self.assertEqual(restored.world_flags, frozenset({"facade-save"}))

    def test_one_cell_move_uses_unified_runtime_collision_entrypoint(self):
        session = self.facade.new_game(1)
        result = self.facade.move_one_cell(
            session,
            destination=MapPosition(1, 1, 0),
        )
        self.assertTrue(result.resolution.moved)
        self.assertEqual(result.session.player_position, MapPosition(1, 1, 0))
        self.assertEqual(result.collision_provider_kind, "TEST_STATIC")

    def test_wrong_coordinator_type_is_rejected(self):
        with self.assertRaisesRegex(
            TypeError,
            "requires LocalRuntimeSessionCoordinator",
        ):
            LocalApplicationFacade(SimpleNamespace())


if __name__ == "__main__":
    unittest.main()
