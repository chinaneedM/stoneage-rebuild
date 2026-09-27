#!/usr/bin/env python3
"""Deterministic replay/presentation consumer for typed StoneAge battle transitions.

This layer is intentionally downstream of battle resolution. It records and
validates immutable BattleRoundTransition values; it never recalculates combat
and never reads historical network strings.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from tools.stoneage_battle_event_contract import (
    BattleExecutionEvent,
    BattleRoundTransition,
    BattleStateSnapshot,
)
from tools.stoneage_battle_state_model import FINISHED


@dataclass(frozen=True)
class BattleReplay:
    """Immutable contiguous sequence of resolved typed battle transitions."""

    initial: BattleStateSnapshot
    transitions: Tuple[BattleRoundTransition, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.initial, BattleStateSnapshot):
            raise TypeError("battle replay initial state must be BattleStateSnapshot")

        transitions = tuple(self.transitions)
        if not all(
            isinstance(transition, BattleRoundTransition)
            for transition in transitions
        ):
            raise TypeError(
                "battle replay transitions must be BattleRoundTransition"
            )

        expected = self.initial
        for index, transition in enumerate(transitions):
            if transition.before.state != expected.state:
                raise ValueError(
                    f"battle replay state discontinuity before transition {index}"
                )
            expected = transition.after
            if (
                transition.termination is not None
                and index != len(transitions) - 1
            ):
                raise ValueError(
                    "battle replay cannot contain transitions after termination"
                )

        object.__setattr__(self, "transitions", transitions)

    @property
    def current(self) -> BattleStateSnapshot:
        if not self.transitions:
            return self.initial
        return self.transitions[-1].after

    @property
    def finished(self) -> bool:
        return self.current.phase == FINISHED

    @property
    def events(self) -> Tuple[BattleExecutionEvent, ...]:
        return tuple(
            event
            for transition in self.transitions
            for event in transition.events
        )

    def append(self, transition: BattleRoundTransition) -> "BattleReplay":
        if not isinstance(transition, BattleRoundTransition):
            raise TypeError("battle replay append requires BattleRoundTransition")
        if self.finished:
            raise ValueError("cannot append transition after battle termination")
        if transition.before.state != self.current.state:
            raise ValueError("battle replay append state does not match current state")
        return BattleReplay(
            initial=self.initial,
            transitions=self.transitions + (transition,),
        )


def begin_battle_replay(initial: BattleStateSnapshot) -> BattleReplay:
    return BattleReplay(initial=initial)


def battle_replay_from_transition(
    transition: BattleRoundTransition,
) -> BattleReplay:
    if not isinstance(transition, BattleRoundTransition):
        raise TypeError("battle replay requires BattleRoundTransition")
    return BattleReplay(
        initial=transition.before,
        transitions=(transition,),
    )
