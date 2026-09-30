#!/usr/bin/env python3
"""Copyright-safe cross-language semantic golden-contract verifier."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from types import MappingProxyType, SimpleNamespace
from typing import Any, Mapping

from tools.stoneage_local_application_facade import LocalApplicationFacade
from tools.stoneage_local_engine_adapter import (
    ContinueGameIntent,
    DispatchInteractionIntent,
    LocalEngineAdapter,
    MoveIntent,
    NewGameIntent,
    SaveGameIntent,
)
from tools.stoneage_local_runtime_core import (
    BOOTSTRAP_SCHEMA,
    FreshStartRouteContract,
    FreshStartSeed,
    LocalRuntimeSessionState,
    MaterializedWorldRegion,
    ResolvedTransitionBinding,
    RuntimeBootstrapProfile,
    StateGatedTransitionContract,
    TransitionGateDecision,
    WorldRegionRequest,
    decode_local_runtime_session,
    encode_local_runtime_session,
)
from tools.stoneage_local_runtime_save import (
    LocalRuntimeSaveSnapshot,
    build_initial_occupancy_registry,
    build_local_runtime_occupancy_delta,
    dump_local_runtime_save,
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
    LegacyWarpEdge,
)

GOLDEN_SCHEMA = "stoneage.runtime-golden.r1"
DEFAULT_FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "game"
    / "STONEAGE-RUNTIME-GOLDEN-CONTRACT-R1.json"
)


def _position(raw: list[int] | tuple[int, int, int]) -> MapPosition:
    if len(raw) != 3:
        raise ValueError("golden position must have floor,x,y")
    return MapPosition(int(raw[0]), int(raw[1]), int(raw[2]))


def _position_row(position: MapPosition) -> list[int]:
    return [int(position.floor_id), int(position.x), int(position.y)]


class _GoldenInitialOccupancy:
    def __init__(self, world: Mapping[str, Any]):
        self.profile_id = str(world["initial_occupancy_profile"])
        self.rows = tuple(world["initial_occupancy"])

    def populate_registry(self, registry) -> None:
        for row in self.rows:
            if row["kind"] != "character":
                raise ValueError(
                    "golden initial occupancy currently supports character only"
                )
            registry.register_character(
                object_id=str(row["object_id"]),
                position=_position(row["position"]),
                overable=bool(row["overable"]),
                provenance=str(row["provenance"]),
            )


class _GoldenCollisionRouter:
    def __init__(self, world: Mapping[str, Any]):
        self.denied = {
            tuple(int(v) for v in row)
            for row in world["static_denied_positions"]
        }

    def routed_step_verdict(self, *, origin, destination):
        denied = (
            int(destination.floor_id),
            int(destination.x),
            int(destination.y),
        ) in self.denied
        decision = CollisionDecision(
            not denied,
            "synthetic_static_blocked"
            if denied
            else "synthetic_static_allowed",
        )
        return SimpleNamespace(
            decision=decision,
            route=SimpleNamespace(
                provider_kind="SYNTHETIC_GOLDEN_STATIC",
                evidence_class="DESIGN_FIXTURE",
                semantic_profile="STONEAGE_GOLDEN_STATIC_R1",
                exact_recovered25_binary_proof=False,
            ),
        )


def _profile(fixture: Mapping[str, Any]) -> RuntimeBootstrapProfile:
    transition = fixture["transition"]
    transition_id = str(transition["transition_id"])
    routes = {
        ordinal: FreshStartRouteContract(
            ordinal=ordinal,
            route_class="SYNTHETIC_GOLDEN",
            requires_shop=False,
            requires_warpman=False,
            milestones=("synthetic-start",),
            ordered=True,
        )
        for ordinal in (1, 2, 3, 4)
    }
    transitions = {
        transition_id: StateGatedTransitionContract(
            transition_id=transition_id,
            kind="WARPMAN",
            unconditional=False,
            source_profile="synthetic-golden",
            raw={},
        )
    }
    return RuntimeBootstrapProfile(
        schema_id=BOOTSTRAP_SCHEMA,
        contract_id=str(fixture["contract_id"]),
        historical_foundation="taiwan-v1.0",
        runtime_world_profile="recovered25",
        runtime_world_evidence_role="LATER_RECOVERED",
        materializable_floor_count=len(fixture["world"]["maps"]),
        reachable_floor_count=len(fixture["world"]["maps"]),
        remaining_unreachable_floor_count=0,
        routes=routes,
        transitions=transitions,
        raw={"fixture": GOLDEN_SCHEMA},
    )


class _GoldenStack:
    def __init__(self, fixture: Mapping[str, Any]):
        self.fixture = fixture
        self.profile = _profile(fixture)
        world = fixture["world"]
        maps = {
            int(row["floor_id"]): HistoricalMapDefinition(
                int(row["floor_id"]),
                int(row["width"]),
                int(row["height"]),
            )
            for row in world["maps"]
        }
        warps = tuple(
            LegacyWarpEdge(
                source=_position(row["source"]),
                destination=_position(row["destination"]),
            )
            for row in world["classic_warps"]
        )
        self.world_adapter = SimpleNamespace(
            topology=HistoricalWorldTopology(
                maps=maps,
                legacy_warps=warps,
            )
        )
        self.collision_router = _GoldenCollisionRouter(world)
        self.npc_initial_occupancy = _GoldenInitialOccupancy(world)
        transition = fixture["transition"]
        self.binding = ResolvedTransitionBinding(
            transition_id=str(transition["transition_id"]),
            source=_position(transition["source"]),
            destination=_position(transition["destination"]),
            predicate_payload={
                "interaction_kind": str(transition["interaction_kind"]),
                "source_rect": tuple(
                    int(v) for v in transition["source_rect"]
                ),
            },
            provenance=dict(transition["provenance"]),
        )

    def create_fresh_start(self, ordinal: int) -> FreshStartSeed:
        return FreshStartSeed(
            contract_id=self.profile.contract_id,
            world_profile=self.profile.runtime_world_profile,
            hometown_ordinal=int(ordinal),
            position=_position(self.fixture["world"]["start"]),
            player_state=PersistentPlayerState(
                character=PlayerState(
                    MappingProxyType(
                        {"name": "golden-player", "level": 1}
                    )
                )
            ),
        )

    def materialize_player_position(
        self,
        session: LocalRuntimeSessionState,
    ) -> MaterializedWorldRegion:
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
            payload={"cell": _position_row(p)},
            provenance={"source_profile": "synthetic-golden"},
        )

    def resolve_transition(
        self,
        transition_id: str,
    ) -> ResolvedTransitionBinding:
        if str(transition_id) != self.binding.transition_id:
            raise KeyError(f"unknown golden transition: {transition_id}")
        return self.binding

    def evaluate_transition(
        self,
        transition_id: str,
        session: LocalRuntimeSessionState,
    ) -> TransitionGateDecision:
        self.resolve_transition(transition_id)
        transition = self.fixture["transition"]
        return TransitionGateDecision(
            allowed=bool(transition["allowed"]),
            reason=str(transition["reason"]),
            consumed_state={},
        )


def load_runtime_golden_contract(
    path: Path = DEFAULT_FIXTURE,
) -> Mapping[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, Mapping):
        raise ValueError("runtime golden root must be an object")
    if payload.get("schema") != GOLDEN_SCHEMA:
        raise ValueError("unsupported runtime golden schema")
    return payload


def _summarize_update(update) -> dict[str, Any]:
    interactions = tuple(update.view.interactions)
    row: dict[str, Any] = {
        "event_kind": update.event_kind,
        "position": _position_row(update.view.session.player_position),
        "interaction_ids": [
            item.transition_id for item in interactions
        ],
        "eligible_interaction_ids": [
            item.transition_id
            for item in interactions
            if item.allowed
        ],
    }
    if update.save_key is not None:
        row["save_key"] = update.save_key

    if update.walk_result is not None:
        walk = update.walk_result
        row["walk"] = {
            "moved": bool(walk.resolution.moved),
            "blocked_reason": walk.resolution.blocked_reason,
            "warp_triggered": bool(
                walk.resolution.warp_triggered
            ),
            "collision_allowed": (
                None
                if walk.collision is None
                else bool(walk.collision.allowed)
            ),
            "collision_reason": (
                None
                if walk.collision is None
                else walk.collision.reason
            ),
            "static_reason": (
                None
                if walk.static_collision is None
                else walk.static_collision.reason
            ),
            "dynamic_reason": (
                None
                if walk.dynamic_collision is None
                else walk.dynamic_collision.reason
            ),
            "live_object_ids": list(
                walk.live_occupancy_object_ids
            ),
        }

    if update.transition_result is not None:
        decision = update.transition_result.decision
        row["transition"] = {
            "allowed": bool(decision.allowed),
            "reason": decision.reason,
            "execution_supported": not bool(
                decision.consumed_state
            ),
        }
    return row


def _intent(row: Mapping[str, Any]):
    kind = str(row["kind"])
    if kind == "new_game":
        return NewGameIntent(int(row["hometown_ordinal"]))
    if kind == "move":
        return MoveIntent(int(row["dx"]), int(row["dy"]))
    if kind == "dispatch_interaction":
        return DispatchInteractionIntent(
            str(row["transition_id"])
        )
    if kind == "save":
        return SaveGameIntent(str(row["save_key"]))
    if kind == "continue":
        return ContinueGameIntent(str(row["save_key"]))
    raise ValueError(f"unknown golden intent kind: {kind}")


def _run_scenario(
    fixture: Mapping[str, Any],
    scenario: Mapping[str, Any],
) -> list[dict[str, Any]]:
    coordinator = LocalRuntimeSessionCoordinator(
        stack=_GoldenStack(fixture),
        persistence=InMemoryLocalPersistenceStore(),
    )
    adapter = LocalEngineAdapter(
        LocalApplicationFacade(coordinator)
    )
    return [
        _summarize_update(
            adapter.handle(_intent(intent_row))
        )
        for intent_row in scenario["intents"]
    ]


def _session_from_fixture(
    fixture: Mapping[str, Any],
) -> LocalRuntimeSessionState:
    row = fixture["session_serialization"]["session"]
    return LocalRuntimeSessionState(
        contract_id=str(fixture["contract_id"]),
        world_profile="recovered25",
        hometown_ordinal=int(row["hometown_ordinal"]),
        player_position=_position(row["position"]),
        player_state=PersistentPlayerState(
            character=PlayerState(
                MappingProxyType(dict(row["character"]))
            )
        ),
        world_flags=frozenset(
            str(v) for v in row["world_flags"]
        ),
    )


def _session_serialization_result(
    fixture: Mapping[str, Any],
) -> str:
    session = _session_from_fixture(fixture)
    encoded = encode_local_runtime_session(session)
    restored = decode_local_runtime_session(
        encoded,
        expected_contract_id=str(fixture["contract_id"]),
        expected_world_profile="recovered25",
    )
    if restored != session:
        raise AssertionError(
            "golden session encode/decode did not round-trip"
        )
    return encoded


def _occupancy_delta_result(
    fixture: Mapping[str, Any],
) -> Mapping[str, Any]:
    initial = _GoldenInitialOccupancy(fixture["world"])
    registry = build_initial_occupancy_registry(initial)
    for mutation in fixture["occupancy_delta"]["mutations"]:
        kind = str(mutation["kind"])
        if kind == "move":
            registry.move(
                str(mutation["object_id"]),
                _position(mutation["position"]),
            )
        elif kind == "register_item":
            registry.register_item(
                object_id=str(mutation["object_id"]),
                position=_position(mutation["position"]),
                overable=bool(mutation["overable"]),
                provenance=str(mutation["provenance"]),
            )
        else:
            raise ValueError(
                f"unknown golden occupancy mutation: {kind}"
            )

    snapshot = LocalRuntimeSaveSnapshot(
        session=_session_from_fixture(fixture),
        occupancy=build_local_runtime_occupancy_delta(
            registry=registry,
            initial_occupancy=initial,
        ),
    )
    return dump_local_runtime_save(snapshot)["occupancy"]


def _fail_closed_result(
    fixture: Mapping[str, Any],
    case_id: str,
) -> str:
    if case_id == "wrong-session-contract":
        encoded = _session_serialization_result(fixture)
        try:
            decode_local_runtime_session(
                encoded,
                expected_contract_id="WRONG-CONTRACT",
                expected_world_profile="recovered25",
            )
        except ValueError as exc:
            return str(exc)
        raise AssertionError(
            "wrong session contract did not fail closed"
        )

    if case_id == "zero-length-move-intent":
        try:
            MoveIntent(0, 0)
        except ValueError as exc:
            return str(exc)
        raise AssertionError(
            "zero-length move did not fail closed"
        )

    raise ValueError(
        f"unknown golden fail-closed case: {case_id}"
    )


def verify_runtime_golden_contract(
    fixture: Mapping[str, Any],
) -> dict[str, Any]:
    scenario_results = {}
    for scenario in fixture["scenarios"]:
        actual = _run_scenario(fixture, scenario)
        expected = scenario["expected_updates"]
        if actual != expected:
            raise AssertionError(
                f"golden scenario drift: {scenario['id']}\n"
                f"expected={json.dumps(expected, ensure_ascii=False, sort_keys=True)}\n"
                f"actual={json.dumps(actual, ensure_ascii=False, sort_keys=True)}"
            )
        scenario_results[str(scenario["id"])] = "PASS"

    encoded = _session_serialization_result(fixture)
    expected_encoded = fixture[
        "session_serialization"
    ]["expected_encoded"]
    if encoded != expected_encoded:
        raise AssertionError(
            "golden session serialization drift\n"
            f"expected={expected_encoded}\n"
            f"actual={encoded}"
        )

    occupancy = _occupancy_delta_result(fixture)
    expected_occupancy = fixture[
        "occupancy_delta"
    ]["expected"]
    if occupancy != expected_occupancy:
        raise AssertionError(
            "golden occupancy delta drift\n"
            f"expected={json.dumps(expected_occupancy, ensure_ascii=False, sort_keys=True)}\n"
            f"actual={json.dumps(occupancy, ensure_ascii=False, sort_keys=True)}"
        )

    fail_closed = {}
    for case in fixture["fail_closed"]:
        actual = _fail_closed_result(
            fixture,
            str(case["id"]),
        )
        expected = str(case["expected_error"])
        if actual != expected:
            raise AssertionError(
                "golden fail-closed drift: "
                f"{case['id']}: {actual!r} != {expected!r}"
            )
        fail_closed[str(case["id"])] = "PASS"

    return {
        "schema": GOLDEN_SCHEMA,
        "scenarios": scenario_results,
        "session_serialization": "PASS",
        "occupancy_delta": "PASS",
        "fail_closed": fail_closed,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "fixture",
        nargs="?",
        type=Path,
        default=DEFAULT_FIXTURE,
    )
    args = parser.parse_args()
    result = verify_runtime_golden_contract(
        load_runtime_golden_contract(args.fixture)
    )
    print(
        json.dumps(
            result,
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
