#!/usr/bin/env python3
"""Engine-neutral typed contract for deterministic StoneAge battle transitions.

The historical Taiwan v1 client used string-serialized receive queues. The
modern single-player core does not. This module binds the already reconstructed
typed battle intent, persistent authoritative state, execution events, turn
synchronization, and terminal result into one immutable transition envelope.

It is an implementation contract, not a claim that these Python types existed
in the historical client or server.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from tools.stoneage_battle_round_model import BattleCommand, OrdinaryRoundEvent
from tools.stoneage_battle_state_model import (
    FINISHED,
    PersistentBattleState,
    PersistentRoundResult,
)


@dataclass(frozen=True)
class BattleIntent:
    """One participant's submitted typed battle command for the next round."""

    participant_id: str
    slot: int
    command: BattleCommand

    def __post_init__(self) -> None:
        participant_id = str(self.participant_id)
        slot = int(self.slot)
        if not participant_id:
            raise ValueError("battle intent requires participant_id")
        if not 0 <= slot < 20:
            raise ValueError("battle intent slot must be in 0..19")
        if not isinstance(self.command, BattleCommand):
            raise TypeError("battle intent command must be BattleCommand")
        object.__setattr__(self, "participant_id", participant_id)
        object.__setattr__(self, "slot", slot)


@dataclass(frozen=True)
class BattleStateSnapshot:
    """Immutable authoritative-state boundary.

    PersistentBattleState is already immutable and owns every reconstructed
    battle-local rule field. Wrapping it avoids duplicating or flattening those
    fields merely for presentation/transport.
    """

    state: PersistentBattleState

    def __post_init__(self) -> None:
        if not isinstance(self.state, PersistentBattleState):
            raise TypeError("battle state snapshot requires PersistentBattleState")

    @property
    def turn(self) -> int:
        return int(self.state.turn)

    @property
    def phase(self) -> str:
        return str(self.state.phase)

    @property
    def result(self) -> str | None:
        return self.state.result

    @property
    def winning_side(self) -> int | None:
        return self.state.winning_side


@dataclass(frozen=True)
class BattleExecutionEvent:
    """Ordered typed execution/presentation event emitted by the resolver."""

    sequence: int
    event: OrdinaryRoundEvent

    def __post_init__(self) -> None:
        sequence = int(self.sequence)
        if sequence < 0:
            raise ValueError("battle event sequence cannot be negative")
        if not isinstance(self.event, OrdinaryRoundEvent):
            raise TypeError("battle execution event requires OrdinaryRoundEvent")
        object.__setattr__(self, "sequence", sequence)


@dataclass(frozen=True)
class BattleTurnSync:
    """Local deterministic replacement for historical client/server turn sync."""

    previous_turn: int
    completed_turn: int
    action_order: Tuple[str, ...]

    def __post_init__(self) -> None:
        previous_turn = int(self.previous_turn)
        completed_turn = int(self.completed_turn)
        if previous_turn < 0:
            raise ValueError("previous battle turn cannot be negative")
        if completed_turn != previous_turn + 1:
            raise ValueError("battle turn sync must advance exactly one round")
        action_order = tuple(str(pid) for pid in self.action_order)
        if len(action_order) != len(set(action_order)):
            raise ValueError("battle action order cannot contain duplicates")
        object.__setattr__(self, "previous_turn", previous_turn)
        object.__setattr__(self, "completed_turn", completed_turn)
        object.__setattr__(self, "action_order", action_order)


@dataclass(frozen=True)
class BattleTermination:
    """Typed terminal state emitted only when the authoritative state finishes."""

    turn: int
    result: str
    winning_side: int | None

    def __post_init__(self) -> None:
        turn = int(self.turn)
        result = str(self.result)
        winning_side = self.winning_side
        if turn < 0:
            raise ValueError("termination turn cannot be negative")
        if not result:
            raise ValueError("battle termination requires result")
        if winning_side is not None:
            winning_side = int(winning_side)
            if winning_side not in {0, 1}:
                raise ValueError("winning_side must be 0, 1, or None")
        object.__setattr__(self, "turn", turn)
        object.__setattr__(self, "result", result)
        object.__setattr__(self, "winning_side", winning_side)


@dataclass(frozen=True)
class BattleRoundTransition:
    """One complete protocol-free deterministic battle round contract."""

    intents: Tuple[BattleIntent, ...]
    before: BattleStateSnapshot
    events: Tuple[BattleExecutionEvent, ...]
    turn_sync: BattleTurnSync
    after: BattleStateSnapshot
    termination: BattleTermination | None = None

    def __post_init__(self) -> None:
        intents = tuple(self.intents)
        events = tuple(self.events)
        if not all(isinstance(intent, BattleIntent) for intent in intents):
            raise TypeError("battle transition intents must be BattleIntent")
        if not all(isinstance(event, BattleExecutionEvent) for event in events):
            raise TypeError(
                "battle transition events must be BattleExecutionEvent"
            )
        if not isinstance(self.before, BattleStateSnapshot):
            raise TypeError("battle transition before must be BattleStateSnapshot")
        if not isinstance(self.after, BattleStateSnapshot):
            raise TypeError("battle transition after must be BattleStateSnapshot")
        if not isinstance(self.turn_sync, BattleTurnSync):
            raise TypeError("battle transition turn_sync must be BattleTurnSync")
        if self.turn_sync.previous_turn != self.before.turn:
            raise ValueError("turn sync previous turn does not match before state")
        if self.turn_sync.completed_turn != self.after.turn:
            raise ValueError("turn sync completed turn does not match after state")

        finished = self.after.phase == FINISHED
        if finished and self.termination is None:
            raise ValueError("finished battle transition requires termination")
        if not finished and self.termination is not None:
            raise ValueError("active battle transition cannot emit termination")
        if self.termination is not None:
            if self.termination.turn != self.after.turn:
                raise ValueError("termination turn does not match after state")
            if self.termination.result != self.after.result:
                raise ValueError("termination result does not match after state")
            if self.termination.winning_side != self.after.winning_side:
                raise ValueError(
                    "termination winning side does not match after state"
                )

        object.__setattr__(self, "intents", intents)
        object.__setattr__(self, "events", events)


def snapshot_battle_state(state: PersistentBattleState) -> BattleStateSnapshot:
    return BattleStateSnapshot(state=state)


def build_battle_round_transition(
    result: PersistentRoundResult,
) -> BattleRoundTransition:
    """Bind one resolved persistent round into the engine-facing contract.

    Intents are ordered by historical battle slot, not by mapping insertion
    order. Execution events retain the resolver's event order. No historical
    B/BC/BA/BP/BU wire string is retained or regenerated.
    """
    if not isinstance(result, PersistentRoundResult):
        raise TypeError("battle round transition requires PersistentRoundResult")

    commands = result.after.last_commands
    if commands is None:
        raise ValueError("resolved persistent round has no submitted commands")

    intents = []
    for participant_id, slot in sorted(
        result.before.slots.items(),
        key=lambda item: (int(item[1]), str(item[0])),
    ):
        participant_id = str(participant_id)
        if participant_id not in commands:
            continue
        intents.append(
            BattleIntent(
                participant_id=participant_id,
                slot=int(slot),
                command=commands[participant_id],
            )
        )

    extra_command_ids = set(str(pid) for pid in commands) - {
        intent.participant_id for intent in intents
    }
    if extra_command_ids:
        raise ValueError(
            "submitted command participants are absent from before-state slots: "
            + ", ".join(sorted(extra_command_ids))
        )

    before = snapshot_battle_state(result.before)
    after = snapshot_battle_state(result.after)
    events = tuple(
        BattleExecutionEvent(sequence=index, event=event)
        for index, event in enumerate(result.round.events)
    )
    turn_sync = BattleTurnSync(
        previous_turn=before.turn,
        completed_turn=after.turn,
        action_order=tuple(result.round.action_order),
    )

    termination = None
    if result.after.phase == FINISHED:
        if result.after.result is None:
            raise ValueError("finished battle has no result")
        termination = BattleTermination(
            turn=after.turn,
            result=result.after.result,
            winning_side=result.after.winning_side,
        )

    return BattleRoundTransition(
        intents=tuple(intents),
        before=before,
        events=events,
        turn_sync=turn_sync,
        after=after,
        termination=termination,
    )
