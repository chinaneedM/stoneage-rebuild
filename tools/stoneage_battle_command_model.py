#!/usr/bin/env python3
"""Stable-descendant first battle-round player command boundary.

This intentionally models only the ordinary core commands visible in the
stable BattleCommandDispach path:
- H|hex_target : physical attack
- G            : guard
- N            : wait
- E            : escape
- T|hex_target : capture

Later profession/pet-skill/item/magic extensions remain outside this first
boundary. Random initiative is explicit and uses the independently recovered
older ordinary-command initiative profile.
"""

from __future__ import annotations

from dataclasses import dataclass

from tools.stoneage_singleplayer_battle import BattleParticipant


ATTACK = "attack"
GUARD = "guard"
WAIT = "wait"
ESCAPE = "escape"
CAPTURE = "capture"

_TARGETED = {ATTACK, CAPTURE}
_ERROR_STATUS_FALLBACK = {ATTACK, GUARD, ESCAPE, CAPTURE}


@dataclass(frozen=True)
class PlayerBattleCommand:
    kind: str
    target_slot: int | None
    wire_command: str

    def __post_init__(self) -> None:
        if self.kind not in {ATTACK, GUARD, WAIT, ESCAPE, CAPTURE}:
            raise ValueError(f"unsupported first-round command kind: {self.kind}")
        if self.kind in _TARGETED:
            if self.target_slot is None:
                raise ValueError(f"{self.kind} requires target_slot")
            if not -1 <= int(self.target_slot) < 20:
                raise ValueError("target_slot must be -1 or in 0..19")
        elif self.target_slot is not None:
            raise ValueError(f"{self.kind} does not carry target_slot")


@dataclass(frozen=True)
class BattleRoundAction:
    actor_id: str
    command: PlayerBattleCommand
    initiative: int
    ready: bool = True


def _hex_target_or_minus_one(text: str) -> int:
    try:
        value = int(text, 16)
    except (TypeError, ValueError):
        return -1
    return value if 0 <= value < 20 else -1


def parse_player_battle_command(command: str) -> PlayerBattleCommand:
    """Mirror the fixed dispatcher's first-prefix command interpretation."""
    command = str(command)
    if command.startswith("H|"):
        return PlayerBattleCommand(
            ATTACK,
            _hex_target_or_minus_one(command[2:]),
            command,
        )
    if command.startswith("G"):
        return PlayerBattleCommand(GUARD, None, command)
    if command.startswith("N"):
        return PlayerBattleCommand(WAIT, None, command)
    if command.startswith("E"):
        return PlayerBattleCommand(ESCAPE, None, command)
    if command.startswith("T|"):
        return PlayerBattleCommand(
            CAPTURE,
            _hex_target_or_minus_one(command[2:]),
            command,
        )
    raise ValueError(f"unsupported first-round battle command: {command!r}")


def apply_error_status_fallback(
    command: PlayerBattleCommand,
    *,
    error_status: bool,
) -> PlayerBattleCommand:
    """Stable dispatcher recursively maps checked commands to N on error."""
    if bool(error_status) and command.kind in _ERROR_STATUS_FALLBACK:
        return PlayerBattleCommand(WAIT, None, "N")
    return command


def prepare_player_round_action(
    participant: BattleParticipant,
    command: PlayerBattleCommand,
    *,
    initiative_random_subtract: int,
    error_status: bool = False,
) -> BattleRoundAction:
    if participant.side != "player" or participant.kind != "player":
        raise ValueError("first player command requires the player participant")
    normalized = apply_error_status_fallback(
        command,
        error_status=error_status,
    )
    return BattleRoundAction(
        actor_id=participant.participant_id,
        command=normalized,
        initiative=participant.initiative(int(initiative_random_subtract)),
        ready=True,
    )
