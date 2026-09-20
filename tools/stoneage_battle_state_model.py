#!/usr/bin/env python3
"""Persistent multi-round state for the first reconstructed StoneAge battle seam.

The stable descendant checks battle termination after a completed round through
BATTLE_OnlyRescue(). That function explicitly skips CHAR_TYPEPET and counts
living non-pet actors. R1 models the ordinary single-player subset:
- side 0: player plus optional allied pets;
- side 1: enemy actors;
- rescue/spectator modes are not yet represented.

Persistent EXP application, drops, escape/capture and post-battle recovery
remain outside this state machine. R1 now preserves the earlier stable
battle-local WORKGETEXP seam: ordinary enemy deaths can accumulate pending EXP
for the player-side actor that caused the death, without applying it to
persistent character EXP or level state.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Mapping, Sequence

from tools.stoneage_battle_core_model import battle_exp_from_enemy
from tools.stoneage_battle_round_model import (
    BattleCombatProfile,
    BattleCommand,
    OrdinaryAttackRolls,
    ResolvedOrdinaryRound,
    prepare_battle_round,
    resolve_ordinary_round,
)
from tools.stoneage_singleplayer_battle import BattleParticipant, BattleSession


ACTIVE = "active"
FINISHED = "finished"

PLAYER_WIN = "victory"
ENEMY_WIN = "defeat"


@dataclass(frozen=True)
class PersistentBattleState:
    session: BattleSession
    slots: Mapping[str, int]
    hp_by_participant_id: Mapping[str, int]
    pending_exp_by_participant_id: Mapping[str, int]
    turn: int = 0
    phase: str = ACTIVE
    result: str | None = None
    winning_side: int | None = None
    last_commands: Mapping[str, BattleCommand] | None = None

    def __post_init__(self) -> None:
        if self.phase not in {ACTIVE, FINISHED}:
            raise ValueError(f"unknown battle phase: {self.phase}")
        if self.phase == ACTIVE:
            if self.result is not None or self.winning_side is not None:
                raise ValueError("active battle cannot already have a result")
        else:
            if self.result not in {PLAYER_WIN, ENEMY_WIN}:
                raise ValueError("finished battle requires victory/defeat result")
            if self.winning_side not in {0, 1}:
                raise ValueError("finished battle requires winning_side 0 or 1")

        participants = _participant_map(self.session)
        expected_exp_ids = {
            pid for pid, participant in participants.items()
            if participant.side == "player"
        }
        actual_exp_ids = {str(pid) for pid in self.pending_exp_by_participant_id}
        if actual_exp_ids != expected_exp_ids:
            missing = sorted(expected_exp_ids - actual_exp_ids)
            extra = sorted(actual_exp_ids - expected_exp_ids)
            raise ValueError(
                f"pending EXP participants mismatch; missing={missing}, extra={extra}"
            )
        if any(int(value) < 0 for value in self.pending_exp_by_participant_id.values()):
            raise ValueError("pending EXP cannot be negative")


@dataclass(frozen=True)
class PersistentRoundResult:
    before: PersistentBattleState
    round: ResolvedOrdinaryRound
    after: PersistentBattleState


def _session_participants(session: BattleSession) -> tuple[BattleParticipant, ...]:
    return (session.player, *session.allied_pets, *session.enemies)


def _participant_map(session: BattleSession) -> dict[str, BattleParticipant]:
    result: dict[str, BattleParticipant] = {}
    for participant in _session_participants(session):
        pid = str(participant.participant_id)
        if pid in result:
            raise ValueError(f"duplicate battle participant id {pid}")
        result[pid] = participant
    return result


def _freeze_mapping(values: Mapping) -> Mapping:
    return MappingProxyType(dict(values))


def begin_persistent_battle(
    session: BattleSession,
    *,
    slots: Mapping[str, int],
) -> PersistentBattleState:
    participants = _participant_map(session)
    normalized_slots = {str(pid): int(slot) for pid, slot in slots.items()}
    if set(normalized_slots) != set(participants):
        missing = sorted(set(participants) - set(normalized_slots))
        extra = sorted(set(normalized_slots) - set(participants))
        raise ValueError(f"battle slots mismatch; missing={missing}, extra={extra}")
    if len(set(normalized_slots.values())) != len(normalized_slots):
        raise ValueError("battle slots must be unique")
    for pid, slot in normalized_slots.items():
        if not 0 <= slot < 20:
            raise ValueError("battle slots must be in 0..19")
        expected_side = "player" if slot < 10 else "enemy"
        if participants[pid].side != expected_side:
            raise ValueError(
                f"slot {slot} belongs to {expected_side}, "
                f"not {participants[pid].side}"
            )

    hp = {
        pid: max(0, int(participant.hp))
        for pid, participant in participants.items()
    }
    pending_exp = {
        pid: 0
        for pid, participant in participants.items()
        if participant.side == "player"
    }
    state = PersistentBattleState(
        session=session,
        slots=_freeze_mapping(normalized_slots),
        hp_by_participant_id=_freeze_mapping(hp),
        pending_exp_by_participant_id=_freeze_mapping(pending_exp),
    )
    return _with_termination(state)


def living_non_pet_count(
    state: PersistentBattleState,
    side: int,
) -> int:
    """R1 projection of stable BATTLE_OnlyRescue() without rescue mode.

    The source skips CHAR_TYPEPET before checking whether a character remains
    alive. In the current single-player subset, HP > 0 is the battle-live
    criterion represented by the ordinary resolver.
    """
    if side not in {0, 1}:
        raise ValueError("side must be 0 or 1")
    participants = _participant_map(state.session)
    count = 0
    for pid, participant in participants.items():
        slot = int(state.slots[pid])
        if (0 if slot < 10 else 1) != side:
            continue
        if participant.kind == "pet":
            continue
        if int(state.hp_by_participant_id.get(pid, 0)) > 0:
            count += 1
    return count


def termination_result(
    state: PersistentBattleState,
) -> tuple[str | None, int | None]:
    """Mirror the stable post-round side-check order.

    Stable BATTLE_Command checks side 0 first:
      if BATTLE_OnlyRescue(side0) == 0 -> winside = 1
      else if BATTLE_OnlyRescue(side1) == 0 -> winside = 0

    That order is preserved for the otherwise-degenerate both-zero case.
    """
    if living_non_pet_count(state, 0) == 0:
        return ENEMY_WIN, 1
    if living_non_pet_count(state, 1) == 0:
        return PLAYER_WIN, 0
    return None, None


def _with_termination(state: PersistentBattleState) -> PersistentBattleState:
    result, winning_side = termination_result(state)
    if result is None:
        return state
    return replace(
        state,
        phase=FINISHED,
        result=result,
        winning_side=winning_side,
    )


def participant_snapshot(
    state: PersistentBattleState,
    participant_id: str,
) -> BattleParticipant:
    participants = _participant_map(state.session)
    participant_id = str(participant_id)
    if participant_id not in participants:
        raise KeyError(f"unknown battle participant {participant_id}")
    participant = participants[participant_id]
    return replace(
        participant,
        hp=int(state.hp_by_participant_id[participant_id]),
    )


def active_participants(
    state: PersistentBattleState,
) -> tuple[BattleParticipant, ...]:
    """Return living actors only, retaining original session order."""
    return tuple(
        participant_snapshot(state, participant.participant_id)
        for participant in _session_participants(state.session)
        if int(state.hp_by_participant_id[participant.participant_id]) > 0
    )


def _pending_exp_after_ordinary_round(
    state: PersistentBattleState,
    round_result: ResolvedOrdinaryRound,
) -> Mapping[str, int]:
    """Mirror the stable ordinary WORKGETEXP accumulation seam.

    BATTLE_AddExpItem() runs after an attack and scans newly dead enemies.
    For an ordinary single-target attack the attack list contains exactly the
    acting participant, so only that player-side actor receives the defeated
    enemy's adjusted EXP. Combo/counter/status and ride-pet reward behavior are
    separate seams and are not inferred here.
    """
    participants = _participant_map(state.session)
    participant_id_by_slot = {
        int(slot): str(pid)
        for pid, slot in state.slots.items()
    }
    pending = {
        str(pid): int(value)
        for pid, value in state.pending_exp_by_participant_id.items()
    }

    for event in round_result.events:
        if event.target_hp_before is None or event.target_hp_after is None:
            continue
        if int(event.target_hp_before) <= 0 or int(event.target_hp_after) != 0:
            continue
        actor_id = str(event.participant_id)
        actor = participants[actor_id]
        if actor.side != "player":
            continue
        if event.resolved_target_slot is None:
            continue
        target_id = participant_id_by_slot.get(int(event.resolved_target_slot))
        if target_id is None:
            raise ValueError("resolved kill target slot has no participant")
        target = participants[target_id]
        if target.kind != "enemy":
            continue
        if target.reward_exp is None:
            raise ValueError(
                f"enemy {target_id} lacks reward EXP provenance"
            )
        pending[actor_id] += battle_exp_from_enemy(
            int(target.reward_exp),
            int(actor.level),
            int(target.level),
        )

    return _freeze_mapping(pending)


def resolve_persistent_ordinary_round(
    state: PersistentBattleState,
    *,
    commands: Mapping[str, BattleCommand],
    initiative_random_subtracts: Mapping[str, int],
    profiles: Mapping[str, BattleCombatProfile],
    attack_rolls: Mapping[str, OrdinaryAttackRolls],
    defense_profile: str,
    field_attr: str = "none",
    field_power: int = 0,
    tie_break_order: Sequence[str] | None = None,
) -> PersistentRoundResult:
    if state.phase != ACTIVE:
        raise ValueError("cannot execute another round after battle termination")

    participants = active_participants(state)
    living_ids = {participant.participant_id for participant in participants}
    if set(commands) != living_ids:
        missing = sorted(living_ids - set(commands))
        extra = sorted(set(commands) - living_ids)
        raise ValueError(
            f"commands must cover exactly living actors; "
            f"missing={missing}, extra={extra}"
        )
    if set(initiative_random_subtracts) != living_ids:
        missing = sorted(living_ids - set(initiative_random_subtracts))
        extra = sorted(set(initiative_random_subtracts) - living_ids)
        raise ValueError(
            f"initiative rolls must cover exactly living actors; "
            f"missing={missing}, extra={extra}"
        )

    prepared = prepare_battle_round(
        participants,
        commands,
        initiative_random_subtracts,
        tie_break_order=tie_break_order,
    )
    current_slots = {
        participant.participant_id: int(state.slots[participant.participant_id])
        for participant in participants
    }
    round_result = resolve_ordinary_round(
        prepared,
        slots=current_slots,
        profiles=profiles,
        attack_rolls=attack_rolls,
        defense_profile=defense_profile,
        field_attr=field_attr,
        field_power=field_power,
    )

    hp = dict(state.hp_by_participant_id)
    hp.update(
        {
            participant_id: int(value)
            for participant_id, value in round_result.hp_by_participant_id.items()
        }
    )
    next_state = PersistentBattleState(
        session=state.session,
        slots=state.slots,
        hp_by_participant_id=_freeze_mapping(hp),
        pending_exp_by_participant_id=_pending_exp_after_ordinary_round(
            state,
            round_result,
        ),
        turn=int(state.turn) + 1,
        phase=ACTIVE,
        result=None,
        winning_side=None,
        last_commands=_freeze_mapping(commands),
    )
    next_state = _with_termination(next_state)
    return PersistentRoundResult(
        before=state,
        round=round_result,
        after=next_state,
    )
