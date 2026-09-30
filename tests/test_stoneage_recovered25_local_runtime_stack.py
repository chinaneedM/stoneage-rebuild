import unittest
from pathlib import Path
from types import MappingProxyType

from tools.stoneage_local_runtime_core import (
    LocalRuntimeSessionState,
    MaterializedWorldRegion,
    ResolvedTransitionBinding,
    TransitionGateDecision,
    WorldRegionRequest,
    load_runtime_bootstrap_file,
)
from tools.stoneage_recovered25_local_runtime_stack import (
    Recovered25LocalRuntimeStack,
)
from tools.stoneage_singleplayer_domain import (
    MapPosition,
    PersistentPlayerState,
    PlayerState,
)

ROOT = Path(__file__).resolve().parents[1]


def _state() -> PersistentPlayerState:
    return PersistentPlayerState(
        character=PlayerState(MappingProxyType({"name": "stack-test", "level": 1}))
    )


class _RegionProvider:
    def __init__(self, profile):
        self.profile = profile

    def materialize_region(self, request):
        return MaterializedWorldRegion(
            request=request,
            payload={"kind": "fake"},
            provenance={"world_profile": request.world_profile},
        )


class _Factory:
    def __init__(self, profile):
        self.profile = profile

    def create_fresh_start(self, profile, ordinal):
        return type("Seed", (), {
            "contract_id": profile.contract_id,
            "world_profile": profile.runtime_world_profile,
            "hometown_ordinal": ordinal,
            "position": MapPosition(1006, 1, 1),
            "player_state": _state(),
        })()


class _Resolver:
    def __init__(self, profile):
        self.bindings = {
            key: ResolvedTransitionBinding(
                transition_id=key,
                source=MapPosition(1006, 1, 1),
                destination=MapPosition(1006, 2, 2),
                predicate_payload={"gate_kind": "FAKE"},
                provenance={"source_profile": "recovered25"},
            )
            for key in profile.transitions
        }

    def resolve_transition(self, contract):
        return self.bindings[contract.transition_id]


class _Evaluator:
    def evaluate_transition(self, contract, binding, session):
        return TransitionGateDecision(
            allowed=contract.transition_id == binding.transition_id,
            reason="fake evaluator",
            consumed_state={},
        )


class _WorldAdapter:
    def __init__(self, profile):
        self.profile = profile


class Recovered25LocalRuntimeStackTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.profile = load_runtime_bootstrap_file(
            ROOT / "game" / "RUNTIME-BOOTSTRAP-RECOVERED25-R1.json"
        )
        cls.stack = Recovered25LocalRuntimeStack(
            profile=cls.profile,
            world_adapter=_WorldAdapter(cls.profile),
            region_provider=_RegionProvider(cls.profile),
            transition_resolver=_Resolver(cls.profile),
            transition_evaluator=_Evaluator(),
            fresh_start_factory=_Factory(cls.profile),
        )

    def test_stack_delegates_fresh_start_and_concrete_region_port(self):
        seed = self.stack.create_fresh_start(1)
        self.assertEqual(seed.hometown_ordinal, 1)
        request = WorldRegionRequest(
            floor_id=1006,
            x1=1,
            y1=1,
            x2=1,
            y2=1,
            world_profile="recovered25",
        )
        region = self.stack.materialize_region(request)
        self.assertEqual(region.payload["kind"], "fake")

    def test_player_position_materializes_through_region_provider(self):
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1006, 3, 4),
            player_state=_state(),
        )
        region = self.stack.materialize_player_position(session)
        self.assertEqual(
            (
                region.request.floor_id,
                region.request.x1,
                region.request.y1,
                region.request.x2,
                region.request.y2,
            ),
            (1006, 3, 4, 3, 4),
        )

    def test_transition_lookup_and_evaluation_remain_contract_bound(self):
        transition_id = next(iter(self.profile.transitions))
        binding = self.stack.resolve_transition(transition_id)
        self.assertEqual(binding.transition_id, transition_id)
        session = LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=1,
            player_position=MapPosition(1006, 1, 1),
            player_state=_state(),
        )
        self.assertTrue(self.stack.evaluate_transition(transition_id, session).allowed)
        with self.assertRaises(KeyError):
            self.stack.resolve_transition("not-declared")


if __name__ == "__main__":
    unittest.main()
