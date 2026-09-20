#!/usr/bin/env python3
"""Stable-descendant first battle-round command/order boundary.

This module reconstructs the command envelope and action-order seam without
inventing player input or enemy AI. Commands are explicit inputs. Later skills,
combo rewriting, profession systems and full action execution remain outside
this R1 boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from tools.stoneage_battle_core_model import (
    early_action_value,
    early_item_action_value,
)
from tools.stoneage_singleplayer_battle import BattleParticipant


BATTLE_COM_NONE = 0
BATTLE_COM_ATTACK = 1
BATTLE_COM_GUARD = 2
BATTLE_COM_CAPTURE = 3
BATTLE_COM_ESCAPE = 4
BATTLE_COM_PETIN = 5
BATTLE_COM_PETOUT = 6
BATTLE_COM_ITEM = 7
BATTLE_COM_BOOMERANG = 8
BATTLE_COM_COMBO = 9
BATTLE_COM_COMBOEND = 10
BATTLE_COM_WAIT = 11

BASE_COMMAND_CODES = frozenset(
    {
        BATTLE_COM_NONE,
        BATTLE_COM_ATTACK,
        BATTLE_COM_GUARD,
        BATTLE_COM_CAPTURE,
        BATTLE_COM_ESCAPE,
        BATTLE_COM_PETIN,
        BATTLE_COM_PETOUT,
        BATTLE_COM_ITEM,
        BATTLE_COM_BOOMERANG,
        BATTLE_COM_COMBO,
        BATTLE_COM_COMBOEND,
        BATTLE_COM_WAIT,
    }
)

NO_ACTION_COMMANDS = frozenset({BATTLE_COM_NONE, BATTLE_COM_WAIT})


@dataclass(frozen=True)
class BattleCommand:
    """Mirrors the stable COM1/COM2/COM3 command storage boundary."""

    command1: int
    command2: int = -1
    command3: int = 0
    input_complete: bool = True

    def __post_init__(self) -> None:
        command1 = int(self.command1)
        if command1 not in BASE_COMMAND_CODES:
            raise ValueError(
                "R1 accepts only stable base command codes 0..11"
            )
        object.__setattr__(self, "command1", command1)
        object.__setattr__(self, "command2", int(self.command2))
        object.__setattr__(self, "command3", int(self.command3))
        object.__setattr__(self, "input_complete", bool(self.input_complete))

    @property
    def produces_action(self) -> bool:
        return self.command1 not in NO_ACTION_COMMANDS


@dataclass(frozen=True)
class RoundEntry:
    participant: BattleParticipant
    command: BattleCommand
    action_value: int
    source_order: int

    @property
    def ready_to_execute(self) -> bool:
        return (
            self.command.input_complete
            and int(self.participant.hp) > 0
        )


@dataclass(frozen=True)
class PreparedBattleRound:
    ordered_entries: tuple[RoundEntry, ...]
    executable_entries: tuple[RoundEntry, ...]
    no_action_entries: tuple[RoundEntry, ...]
    tie_break_was_required: bool


def command_action_value(
    participant: BattleParticipant,
    command: BattleCommand,
    *,
    random_subtract: int,
) -> int:
    """Stable older command-speed profile.

    ITEM has the preserved +15% offset. Other base commands fall through the
    ordinary QUICK+20 minus RAND(0,30%) path in BATTLE_DexCalc.
    """
    if command.command1 == BATTLE_COM_ITEM:
        return early_item_action_value(
            participant.quick,
            int(random_subtract),
        )
    return early_action_value(
        participant.quick,
        int(random_subtract),
    )


def _tie_rank(
    participant_id: str,
    tie_break_order: Sequence[str],
) -> int:
    try:
        return tuple(tie_break_order).index(participant_id)
    except ValueError as exc:
        raise ValueError(
            f"missing explicit tie-break rank for {participant_id}"
        ) from exc


def prepare_battle_round(
    participants: Sequence[BattleParticipant],
    commands: Mapping[str, BattleCommand],
    initiative_random_subtracts: Mapping[str, int],
    *,
    tie_break_order: Sequence[str] | None = None,
) -> PreparedBattleRound:
    """Calculate command-relative action values then sort descending.

    The fixed source uses qsort with comparator pC2->dex - pC1->dex. Its
    ordering for equal values is not a historical contract. If a tie occurs,
    callers must supply an explicit tie_break_order rather than having this
    reconstruction silently invent one.
    """
    entries = []
    seen_ids: set[str] = set()
    for source_order, participant in enumerate(participants):
        participant_id = str(participant.participant_id)
        if participant_id in seen_ids:
            raise ValueError(f"duplicate battle participant id {participant_id}")
        seen_ids.add(participant_id)
        if participant_id not in commands:
            raise KeyError(f"missing command for {participant_id}")
        if participant_id not in initiative_random_subtracts:
            raise KeyError(
                f"missing initiative random result for {participant_id}"
            )
        command = commands[participant_id]
        entries.append(
            RoundEntry(
                participant=participant,
                command=command,
                action_value=command_action_value(
                    participant,
                    command,
                    random_subtract=initiative_random_subtracts[participant_id],
                ),
                source_order=source_order,
            )
        )

    values: dict[int, list[str]] = {}
    for entry in entries:
        values.setdefault(entry.action_value, []).append(
            entry.participant.participant_id
        )
    tied_ids = [
        participant_id
        for ids in values.values()
        if len(ids) > 1
        for participant_id in ids
    ]
    tie_required = bool(tied_ids)

    if tie_required:
        if tie_break_order is None:
            raise ValueError(
                "equal action values require explicit tie_break_order; "
                "fixed-source qsort tie order is unspecified"
            )
        ranking = tuple(str(x) for x in tie_break_order)
        if len(ranking) != len(set(ranking)):
            raise ValueError("tie_break_order contains duplicate ids")
        for participant_id in tied_ids:
            _tie_rank(participant_id, ranking)

        ordered = tuple(
            sorted(
                entries,
                key=lambda entry: (
                    -entry.action_value,
                    _tie_rank(entry.participant.participant_id, ranking)
                    if entry.participant.participant_id in tied_ids
                    else entry.source_order,
                ),
            )
        )
    else:
        ordered = tuple(
            sorted(entries, key=lambda entry: -entry.action_value)
        )

    executable = tuple(
        entry
        for entry in ordered
        if entry.ready_to_execute
    )
    no_action = tuple(
        entry
        for entry in executable
        if not entry.command.produces_action
    )
    return PreparedBattleRound(
        ordered_entries=ordered,
        executable_entries=executable,
        no_action_entries=no_action,
        tie_break_was_required=tie_required,
    )
