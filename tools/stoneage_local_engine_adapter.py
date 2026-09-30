#!/usr/bin/env python3
"""Semantic input/update adapter above the engine-neutral local application facade.

This module defines the command/event boundary a future Godot, Unity, desktop,
or other presentation adapter may implement against. It deliberately contains
no renderer, input-library, or recovered25-specific dependency.
"""

from __future__ import annotations

from dataclasses import dataclass

from tools.stoneage_local_application_facade import (
    LocalApplicationFacade,
    LocalApplicationView,
)
from tools.stoneage_local_runtime_core import LocalRuntimeSessionState
from tools.stoneage_local_runtime_session_coordinator import (
    LocalRuntimeTransitionResult,
    LocalRuntimeWalkResult,
)
from tools.stoneage_singleplayer_domain import MapPosition


LOCAL_ENGINE_ADAPTER_PROFILE = "STONEAGE_LOCAL_ENGINE_ADAPTER_CONTRACT_R1"


def _nonempty(value: object, label: str) -> str:
    text = str(value).strip()
    if not text:
        raise ValueError(f"{label} must be non-empty")
    return text


@dataclass(frozen=True)
class NewGameIntent:
    hometown_ordinal: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "hometown_ordinal", int(self.hometown_ordinal))


@dataclass(frozen=True)
class ContinueGameIntent:
    save_key: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "save_key",
            _nonempty(self.save_key, "continue save_key"),
        )


@dataclass(frozen=True)
class SaveGameIntent:
    save_key: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "save_key",
            _nonempty(self.save_key, "save save_key"),
        )


@dataclass(frozen=True)
class MoveIntent:
    dx: int
    dy: int

    def __post_init__(self) -> None:
        dx = int(self.dx)
        dy = int(self.dy)
        if dx == 0 and dy == 0:
            raise ValueError("move intent cannot be zero-length")
        if abs(dx) > 1 or abs(dy) > 1:
            raise ValueError("move intent must be one cell")
        object.__setattr__(self, "dx", dx)
        object.__setattr__(self, "dy", dy)


@dataclass(frozen=True)
class DispatchInteractionIntent:
    transition_id: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "transition_id",
            _nonempty(self.transition_id, "transition_id"),
        )


@dataclass(frozen=True)
class RefreshViewIntent:
    pass


LocalInputIntent = (
    NewGameIntent
    | ContinueGameIntent
    | SaveGameIntent
    | MoveIntent
    | DispatchInteractionIntent
    | RefreshViewIntent
)


@dataclass(frozen=True)
class LocalEngineUpdate:
    """One semantic output frame for a presentation adapter."""

    event_kind: str
    view: LocalApplicationView
    walk_result: LocalRuntimeWalkResult | None = None
    transition_result: LocalRuntimeTransitionResult | None = None
    save_key: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "event_kind",
            _nonempty(self.event_kind, "event_kind"),
        )
        if not isinstance(self.view, LocalApplicationView):
            raise TypeError("engine update view must be LocalApplicationView")
        if self.save_key is not None:
            object.__setattr__(
                self,
                "save_key",
                _nonempty(self.save_key, "update save_key"),
            )


@dataclass
class LocalEngineAdapter:
    """Stateful semantic driver for a future concrete presentation engine."""

    facade: LocalApplicationFacade
    session: LocalRuntimeSessionState | None = None

    profile_id = LOCAL_ENGINE_ADAPTER_PROFILE

    def __post_init__(self) -> None:
        if not isinstance(self.facade, LocalApplicationFacade):
            raise TypeError(
                "local engine adapter requires LocalApplicationFacade"
            )
        if self.session is not None:
            self.facade.read_view(self.session)

    def _require_session(self) -> LocalRuntimeSessionState:
        if self.session is None:
            raise RuntimeError(
                "local engine adapter has no active session; "
                "start or continue a game first"
            )
        return self.session

    def _update(
        self,
        event_kind: str,
        *,
        walk_result: LocalRuntimeWalkResult | None = None,
        transition_result: LocalRuntimeTransitionResult | None = None,
        save_key: str | None = None,
    ) -> LocalEngineUpdate:
        session = self._require_session()
        return LocalEngineUpdate(
            event_kind=event_kind,
            view=self.facade.read_view(session),
            walk_result=walk_result,
            transition_result=transition_result,
            save_key=save_key,
        )

    def handle(self, intent: LocalInputIntent) -> LocalEngineUpdate:
        if isinstance(intent, NewGameIntent):
            self.session = self.facade.new_game(intent.hometown_ordinal)
            return self._update("NEW_GAME")

        if isinstance(intent, ContinueGameIntent):
            self.session = self.facade.continue_game(intent.save_key)
            return self._update(
                "CONTINUE_GAME",
                save_key=intent.save_key,
            )

        if isinstance(intent, SaveGameIntent):
            session = self._require_session()
            self.facade.save_game(intent.save_key, session)
            return self._update(
                "SAVE_GAME",
                save_key=intent.save_key,
            )

        if isinstance(intent, MoveIntent):
            session = self._require_session()
            p = session.player_position
            destination = MapPosition(
                int(p.floor_id),
                int(p.x) + intent.dx,
                int(p.y) + intent.dy,
            )
            result = self.facade.move_one_cell(
                session,
                destination=destination,
            )
            self.session = result.session
            return self._update(
                "MOVE",
                walk_result=result,
            )

        if isinstance(intent, DispatchInteractionIntent):
            session = self._require_session()
            result = self.facade.dispatch_interaction(
                session,
                intent.transition_id,
            )
            self.session = result.session
            return self._update(
                "INTERACTION",
                transition_result=result,
            )

        if isinstance(intent, RefreshViewIntent):
            return self._update("REFRESH")

        raise TypeError(f"unsupported local input intent: {type(intent).__name__}")
