#!/usr/bin/env python3
"""Engine-neutral local runtime session coordinator.

This application layer sits above a concrete recovered25 local runtime stack.
It owns session lifecycle and command ordering, but deliberately does not own
rendering, input devices, RNG, legacy networking, account services, or an
unproven collision decoder.

Ordinary movement therefore requires an explicit collision verdict from a
validated collision layer. Classic overlap-Warp resolution is delegated to the
already-tested historical world model. Dialogue/state-gated transitions are
spatially checked against their recovered source rectangle before the live gate
evaluator is consulted.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Mapping, Sequence

from tools.stoneage_map_collision_model import (
    CollisionDecision,
    DynamicOccupant,
)
from tools.stoneage_recovered25_collision_router import (
    Recovered25CollisionRoute,
)
from tools.stoneage_local_runtime_core import (
    LocalPersistenceStore,
    LocalRuntimeSessionState,
    MaterializedWorldRegion,
    TransitionGateDecision,
    decode_local_runtime_session,
    encode_local_runtime_session,
)
from tools.stoneage_singleplayer_domain import (
    MapPosition,
    SinglePlayerHistoricalDomain,
)
from tools.stoneage_singleplayer_world import (
    WalkResolution,
    place_player_on_topology,
    resolve_player_walk,
)


@dataclass(frozen=True)
class LocalRuntimeWalkResult:
    session: LocalRuntimeSessionState
    resolution: WalkResolution
    collision: CollisionDecision | None = None
    collision_route: Recovered25CollisionRoute | None = None


@dataclass(frozen=True)
class LocalRuntimeTransitionResult:
    session: LocalRuntimeSessionState
    decision: TransitionGateDecision


class InMemoryLocalPersistenceStore:
    """Small deterministic LocalPersistenceStore implementation for composition/tests."""

    def __init__(self) -> None:
        self._rows: dict[str, str] = {}

    def save(self, key: str, payload: str) -> None:
        key = _nonempty_key(key)
        self._rows[key] = str(payload)

    def load(self, key: str) -> str | None:
        key = _nonempty_key(key)
        return self._rows.get(key)

    @property
    def rows(self) -> Mapping[str, str]:
        return MappingProxyType(dict(self._rows))


def _nonempty_key(value: str) -> str:
    key = str(value).strip()
    if not key:
        raise ValueError("local save key must be non-empty")
    return key


@dataclass
class LocalRuntimeSessionCoordinator:
    """Application-service boundary for one authoritative local play session."""

    stack: object
    persistence: LocalPersistenceStore

    @property
    def profile(self):
        return self.stack.profile

    @property
    def topology(self):
        return self.stack.world_adapter.topology

    def _validate_session(
        self,
        session: LocalRuntimeSessionState,
    ) -> LocalRuntimeSessionState:
        if session.contract_id != self.profile.contract_id:
            raise ValueError("session coordinator bootstrap contract mismatch")
        if session.world_profile != self.profile.runtime_world_profile:
            raise ValueError("session coordinator world-profile mismatch")
        if not self.topology.is_valid_position(session.player_position):
            raise ValueError("session coordinator player position is outside topology")
        return session

    def new_game(self, hometown_ordinal: int) -> LocalRuntimeSessionState:
        seed = self.stack.create_fresh_start(int(hometown_ordinal))
        session = LocalRuntimeSessionState(
            contract_id=seed.contract_id,
            world_profile=seed.world_profile,
            hometown_ordinal=seed.hometown_ordinal,
            player_position=seed.position,
            player_state=seed.player_state,
        )
        return self._validate_session(session)

    def save_game(
        self,
        key: str,
        session: LocalRuntimeSessionState,
    ) -> None:
        session = self._validate_session(session)
        self.persistence.save(
            _nonempty_key(key),
            encode_local_runtime_session(session),
        )

    def continue_game(self, key: str) -> LocalRuntimeSessionState:
        payload = self.persistence.load(_nonempty_key(key))
        if payload is None:
            raise KeyError(f"local save does not exist: {key}")
        session = decode_local_runtime_session(
            payload,
            expected_contract_id=self.profile.contract_id,
            expected_world_profile=self.profile.runtime_world_profile,
        )
        return self._validate_session(session)

    def materialize_current_region(
        self,
        session: LocalRuntimeSessionState,
    ) -> MaterializedWorldRegion:
        session = self._validate_session(session)
        return self.stack.materialize_player_position(session)

    def walk_one_cell(
        self,
        session: LocalRuntimeSessionState,
        *,
        destination: MapPosition,
        entry_allowed: bool,
        map_objmove_ok: bool = True,
    ) -> LocalRuntimeWalkResult:
        """Execute one ordinary walk attempt from an explicit collision verdict.

        The coordinator refuses to infer collision from raw DAT/LS2MAP ids. The
        caller must supply entry_allowed from the selected validated collision
        adapter. This method enforces the ordinary one-cell command shape and
        delegates classic overlap-Warp behavior to resolve_player_walk().
        """

        session = self._validate_session(session)
        origin = session.player_position
        if int(destination.floor_id) != int(origin.floor_id):
            raise ValueError("ordinary walk command cannot change floor directly")
        dx = int(destination.x) - int(origin.x)
        dy = int(destination.y) - int(origin.y)
        if dx == 0 and dy == 0:
            raise ValueError("ordinary walk command cannot be zero-length")
        if abs(dx) > 1 or abs(dy) > 1:
            raise ValueError("ordinary walk command exceeds one cell")

        domain = SinglePlayerHistoricalDomain(persistent=session.player_state)
        place_player_on_topology(domain, self.topology, origin)
        resolution = resolve_player_walk(
            domain,
            self.topology,
            destination=destination,
            entry_allowed=bool(entry_allowed),
            action_is_walk=True,
            map_objmove_ok=bool(map_objmove_ok),
        )
        updated = replace(session, player_position=resolution.final_position)
        self._validate_session(updated)
        return LocalRuntimeWalkResult(
            session=updated,
            resolution=resolution,
        )

    def walk_one_cell_with_server_collision(
        self,
        session: LocalRuntimeSessionState,
        *,
        destination: MapPosition,
        destination_occupants: Sequence[DynamicOccupant] = (),
        is_flying: bool = False,
        map_objmove_ok: bool = True,
    ) -> LocalRuntimeWalkResult:
        """Resolve one step through the stack's provenance-safe server provider."""
        session = self._validate_session(session)
        provider = getattr(self.stack, "collision_provider", None)
        if provider is None:
            raise ValueError("runtime stack has no server collision provider")
        verdict = provider.ordinary_step_verdict(
            origin=session.player_position,
            destination=destination,
            destination_occupants=tuple(destination_occupants),
            is_flying=bool(is_flying),
        )
        result = self.walk_one_cell(
            session,
            destination=destination,
            entry_allowed=verdict.allowed,
            map_objmove_ok=bool(map_objmove_ok),
        )
        return LocalRuntimeWalkResult(
            session=result.session,
            resolution=result.resolution,
            collision=verdict,
        )

    def walk_one_cell_with_recovered25_collision(
        self,
        session: LocalRuntimeSessionState,
        *,
        destination: MapPosition,
        map_objmove_ok: bool = True,
    ) -> LocalRuntimeWalkResult:
        """Resolve one step through the stack's provenance-bearing router."""
        session = self._validate_session(session)
        router = getattr(self.stack, "collision_router", None)
        if router is None:
            raise ValueError("runtime stack has no recovered25 collision router")
        routed = router.routed_step_verdict(
            origin=session.player_position,
            destination=destination,
        )
        result = self.walk_one_cell(
            session,
            destination=destination,
            entry_allowed=routed.decision.allowed,
            map_objmove_ok=bool(map_objmove_ok),
        )
        return LocalRuntimeWalkResult(
            session=result.session,
            resolution=result.resolution,
            collision=routed.decision,
            collision_route=routed.route,
        )

    @staticmethod
    def _binding_source_rect(binding) -> tuple[int, int, int, int]:
        if binding.predicate_payload.get("interaction_kind") != "DIALOGUE_WARPMAN":
            raise ValueError("state-gated coordinator currently requires dialogue WarpMan")
        raw = binding.predicate_payload.get("source_rect")
        if not isinstance(raw, tuple) or len(raw) != 4:
            raise ValueError("state-gated binding lacks recovered source rectangle")
        x1, y1, x2, y2 = (int(v) for v in raw)
        return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)

    def execute_state_gated_transition(
        self,
        session: LocalRuntimeSessionState,
        transition_id: str,
    ) -> LocalRuntimeTransitionResult:
        """Evaluate and, if allowed, execute one recovered dialogue transition."""

        session = self._validate_session(session)
        binding = self.stack.resolve_transition(str(transition_id))
        x1, y1, x2, y2 = self._binding_source_rect(binding)
        p = session.player_position
        spatially_eligible = (
            int(p.floor_id) == int(binding.source.floor_id)
            and x1 <= int(p.x) <= x2
            and y1 <= int(p.y) <= y2
        )
        if not spatially_eligible:
            return LocalRuntimeTransitionResult(
                session=session,
                decision=TransitionGateDecision(
                    allowed=False,
                    reason="player is outside recovered transition source rectangle",
                    consumed_state={},
                ),
            )

        decision = self.stack.evaluate_transition(
            str(transition_id),
            session,
        )
        if not decision.allowed:
            return LocalRuntimeTransitionResult(
                session=session,
                decision=decision,
            )
        if decision.consumed_state:
            raise ValueError(
                "state-gated transition returned unimplemented consumed_state mutation"
            )
        if not self.topology.is_valid_position(binding.destination):
            raise ValueError("state-gated transition destination is outside topology")

        updated = replace(
            session,
            player_position=binding.destination,
        )
        self._validate_session(updated)
        return LocalRuntimeTransitionResult(
            session=updated,
            decision=decision,
        )
