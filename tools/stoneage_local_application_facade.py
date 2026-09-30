#!/usr/bin/env python3
"""Engine-neutral application facade for the local StoneAge runtime.

Presentation/input adapters should depend on this boundary rather than on
recovered25-specific composition modules. Historical/recovered semantics remain
behind LocalRuntimeSessionCoordinator.
"""

from __future__ import annotations

from dataclasses import dataclass

from tools.stoneage_local_runtime_core import (
    LocalRuntimeSessionState,
    MaterializedWorldRegion,
)
from tools.stoneage_local_runtime_session_coordinator import (
    LocalRuntimeInteraction,
    LocalRuntimeSessionCoordinator,
    LocalRuntimeTransitionResult,
    LocalRuntimeWalkResult,
)
from tools.stoneage_singleplayer_domain import MapPosition


LOCAL_APPLICATION_FACADE_PROFILE = "STONEAGE_LOCAL_APPLICATION_FACADE_R1"


@dataclass(frozen=True)
class LocalApplicationView:
    """Read-side state useful to a future renderer without recovered bindings."""

    session: LocalRuntimeSessionState
    region: MaterializedWorldRegion
    interactions: tuple[LocalRuntimeInteraction, ...]


@dataclass
class LocalApplicationFacade:
    """Minimal command/read facade over one authoritative local coordinator."""

    coordinator: LocalRuntimeSessionCoordinator

    profile_id = LOCAL_APPLICATION_FACADE_PROFILE

    def __post_init__(self) -> None:
        if not isinstance(self.coordinator, LocalRuntimeSessionCoordinator):
            raise TypeError(
                "local application facade requires LocalRuntimeSessionCoordinator"
            )

    def new_game(self, hometown_ordinal: int) -> LocalRuntimeSessionState:
        return self.coordinator.new_game(int(hometown_ordinal))

    def continue_game(self, save_key: str) -> LocalRuntimeSessionState:
        return self.coordinator.continue_game(str(save_key))

    def save_game(
        self,
        save_key: str,
        session: LocalRuntimeSessionState,
    ) -> None:
        self.coordinator.save_game(str(save_key), session)

    def read_current_region(
        self,
        session: LocalRuntimeSessionState,
    ) -> MaterializedWorldRegion:
        return self.coordinator.materialize_current_region(session)

    def discover_interactions(
        self,
        session: LocalRuntimeSessionState,
    ) -> tuple[LocalRuntimeInteraction, ...]:
        return self.coordinator.discover_state_gated_interactions(session)

    def read_view(
        self,
        session: LocalRuntimeSessionState,
    ) -> LocalApplicationView:
        return LocalApplicationView(
            session=session,
            region=self.read_current_region(session),
            interactions=self.discover_interactions(session),
        )

    def move_one_cell(
        self,
        session: LocalRuntimeSessionState,
        *,
        destination: MapPosition,
        map_objmove_ok: bool = True,
    ) -> LocalRuntimeWalkResult:
        """Move only through the coordinator's canonical unified collision path."""

        return self.coordinator.walk_one_cell_with_runtime_collision(
            session,
            destination=destination,
            map_objmove_ok=bool(map_objmove_ok),
        )

    def dispatch_interaction(
        self,
        session: LocalRuntimeSessionState,
        transition_id: str,
    ) -> LocalRuntimeTransitionResult:
        return self.coordinator.dispatch_state_gated_interaction(
            session,
            str(transition_id),
        )
