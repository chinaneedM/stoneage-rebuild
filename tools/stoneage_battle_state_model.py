#!/usr/bin/env python3
"""Persistent multi-round state for the first reconstructed StoneAge battle seam.

The stable descendant checks battle termination after a completed round through
BATTLE_OnlyRescue(). That function explicitly skips CHAR_TYPEPET and counts
living non-pet actors. R1 models the ordinary single-player subset:
- side 0: player plus optional allied pets;
- side 1: enemy actors;
- rescue/spectator modes are not yet represented.

Persistent EXP application, escape and post-battle recovery remain outside
this state machine. Capture now has an explicit transition seam after its
source-shaped eligibility/probability result; R1 also preserves the stable battle-local
WORKGETEXP seam and the three-slot pending item buffer: ordinary enemy deaths
can accumulate pending EXP
for the player-side actor that caused the death, without applying it to
persistent character EXP or level state.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Mapping, Sequence

from tools.stoneage_battle_core_model import (
    BATTLE_PENDING_DROP_MAX,
    BattleCaptureInputs,
    BattleCaptureResolution,
    BattleDropItem,
    DropAllocationRoll,
    DropRecipientTicket,
    KillProfitRecipient,
    allocate_battle_drop_items,
    battle_kill_profit,
    resolve_battle_capture_attempt,
    BattleNormalDeathInputs,
    resolve_battle_normal_death_penalty,
    BattleUltimateDeathInputs,
    resolve_battle_ultimate_death_penalty,
)
from tools.stoneage_battle_round_model import (
    BattleCombatProfile,
    BattleCommand,
    BattleCommandSetupEffects,
    ComboExecutionRolls,
    CounterAttemptRolls,
    OrdinaryAttackRolls,
    OrdinaryCaptureContext,
    OrdinaryCaptureRolls,
    OrdinaryEscapeContext,
    OrdinaryEscapeRolls,
    ResolvedOrdinaryRound,
    apply_base_combo_rewrite,
    prepare_battle_round,
    resolve_ordinary_round,
)
from tools.stoneage_battle_damage_react_model import BaseDamageReactState
from tools.stoneage_battle_guardian_model import GuardianRegistration
from tools.stoneage_battle_ride_damage_model import RidePetRuntime
from tools.stoneage_battle_status_model import (
    BaseBattleStatusRuntime,
    BaseStatusApplicationResolution,
    BaseStatusCombatProfile,
    BaseStatusTurnRolls,
)
from tools.stoneage_singleplayer_battle import BattleParticipant, BattleSession


ACTIVE = "active"
FINISHED = "finished"

PLAYER_WIN = "victory"
ENEMY_WIN = "defeat"
PLAYER_ESCAPE = "escape"


@dataclass(frozen=True)
class PersistentBattleState:
    session: BattleSession
    slots: Mapping[str, int]
    hp_by_participant_id: Mapping[str, int]
    pending_exp_by_participant_id: Mapping[str, int]
    pending_pet_variable_ai_by_participant_id: Mapping[str, int]
    pending_drop_items_by_player_entry_id: Mapping[str, tuple[BattleDropItem, ...]]
    pending_player_charm_delta: int = 0
    pending_player_dead_pet_count_delta: int = 0
    destroyed_drop_items: tuple[BattleDropItem, ...] = ()
    turn: int = 0
    phase: str = ACTIVE
    result: str | None = None
    winning_side: int | None = None
    last_commands: Mapping[str, BattleCommand] | None = None
    escape_count_by_participant_id: Mapping[str,int] | None = None
    base_status_runtime_by_participant_id: Mapping[
        str,BaseBattleStatusRuntime
    ] | None = None
    base_damage_react_state_by_participant_id: Mapping[
        str,BaseDamageReactState
    ] | None = None
    ride_pet_runtime: RidePetRuntime | None = None
    ultimate_overkill_by_participant_id: Mapping[str,int] | None = None

    def __post_init__(self) -> None:
        if self.phase not in {ACTIVE, FINISHED}:
            raise ValueError(f"unknown battle phase: {self.phase}")
        if self.phase == ACTIVE:
            if self.result is not None or self.winning_side is not None:
                raise ValueError("active battle cannot already have a result")
        else:
            if self.result == PLAYER_ESCAPE:
                if self.winning_side is not None:
                    raise ValueError("escape finish must not claim a winning side")
            else:
                if self.result not in {PLAYER_WIN, ENEMY_WIN}:
                    raise ValueError(
                        "finished battle requires victory/defeat/escape result"
                    )
                if self.winning_side not in {0, 1}:
                    raise ValueError(
                        "victory/defeat finish requires winning_side 0 or 1"
                    )

        participants = _participant_map(self.session)
        expected_status_ids=set(participants)
        if self.base_status_runtime_by_participant_id is None:
            object.__setattr__(
                self,
                "base_status_runtime_by_participant_id",
                _freeze_mapping({
                    pid:BaseBattleStatusRuntime(
                        work_quick=int(participant.quick)
                    )
                    for pid,participant in participants.items()
                }),
            )
        else:
            normalized_status={
                str(pid):runtime
                for pid,runtime in (
                    self.base_status_runtime_by_participant_id.items()
                )
            }
            if set(normalized_status) != expected_status_ids:
                missing=sorted(expected_status_ids-set(normalized_status))
                extra=sorted(set(normalized_status)-expected_status_ids)
                raise ValueError(
                    f"base-status participants mismatch; "
                    f"missing={missing}, extra={extra}"
                )
            for pid,runtime in normalized_status.items():
                if not isinstance(runtime,BaseBattleStatusRuntime):
                    raise TypeError(
                        f"base status runtime for {pid} has wrong type"
                    )
            object.__setattr__(
                self,
                "base_status_runtime_by_participant_id",
                _freeze_mapping(normalized_status),
            )

        expected_react_ids=set(participants)
        if self.base_damage_react_state_by_participant_id is None:
            object.__setattr__(
                self,
                "base_damage_react_state_by_participant_id",
                _freeze_mapping({
                    pid:BaseDamageReactState()
                    for pid in participants
                }),
            )
        else:
            normalized_react={
                str(pid):react_state
                for pid,react_state in (
                    self.base_damage_react_state_by_participant_id.items()
                )
            }
            if set(normalized_react) != expected_react_ids:
                missing=sorted(expected_react_ids-set(normalized_react))
                extra=sorted(set(normalized_react)-expected_react_ids)
                raise ValueError(
                    f"damage-react participants mismatch; "
                    f"missing={missing}, extra={extra}"
                )
            for pid,react_state in normalized_react.items():
                if not isinstance(react_state,BaseDamageReactState):
                    raise TypeError(
                        f"damage-react state for {pid} has wrong type"
                    )
            object.__setattr__(
                self,
                "base_damage_react_state_by_participant_id",
                _freeze_mapping(normalized_react),
            )

        ride=self.session.ride_pet
        rider_id=str(self.session.player.participant_id)
        if ride is None:
            if self.ride_pet_runtime is not None:
                raise ValueError(
                    "ride runtime exists without BattleSession.ride_pet"
                )
        else:
            if ride.side != "player" or ride.kind != "pet":
                raise ValueError(
                    "ride runtime requires player-side pet provenance"
                )
            if self.ride_pet_runtime is None:
                object.__setattr__(
                    self,
                    "ride_pet_runtime",
                    RidePetRuntime(
                        rider_id=rider_id,
                        pet_id=str(ride.participant_id),
                        hp=max(0,int(ride.hp)),
                        max_hp=int(ride.max_hp),
                        defense_power=int(ride.defense),
                        mounted=True,
                        petfall=False,
                    ),
                )
            else:
                runtime=self.ride_pet_runtime
                if not isinstance(runtime,RidePetRuntime):
                    raise TypeError(
                        "ride_pet_runtime must be RidePetRuntime or null"
                    )
                if runtime.rider_id != rider_id:
                    raise ValueError("ride runtime rider identity drift")
                if runtime.pet_id != str(ride.participant_id):
                    raise ValueError("ride runtime pet identity drift")
                if int(runtime.max_hp) != int(ride.max_hp):
                    raise ValueError("ride runtime max-HP provenance drift")

        expected_escape_ids={            pid for pid,participant in participants.items()
            if participant.kind != "pet"
        }
        if self.escape_count_by_participant_id is None:
            object.__setattr__(
                self,
                "escape_count_by_participant_id",
                _freeze_mapping({
                    pid:0 for pid in sorted(expected_escape_ids)
                }),
            )
        else:
            normalized_escape={
                str(pid):int(value)
                for pid,value in self.escape_count_by_participant_id.items()
            }
            actual_escape_ids=set(normalized_escape)
            if actual_escape_ids != expected_escape_ids:
                missing=sorted(expected_escape_ids-actual_escape_ids)
                extra=sorted(actual_escape_ids-expected_escape_ids)
                raise ValueError(
                    f"escape-count participants mismatch; "
                    f"missing={missing}, extra={extra}"
                )
            if any(value < 0 for value in normalized_escape.values()):
                raise ValueError("stored escape count cannot be negative")
            object.__setattr__(
                self,
                "escape_count_by_participant_id",
                _freeze_mapping(normalized_escape),
            )
        expected_ultimate_ids=set(participants)
        if self.ultimate_overkill_by_participant_id is None:
            object.__setattr__(
                self,
                "ultimate_overkill_by_participant_id",
                _freeze_mapping({
                    pid:0 for pid in sorted(expected_ultimate_ids)
                }),
            )
        else:
            normalized_ultimate={
                str(pid):int(value)
                for pid,value in (
                    self.ultimate_overkill_by_participant_id.items()
                )
            }
            if set(normalized_ultimate) != expected_ultimate_ids:
                missing=sorted(
                    expected_ultimate_ids-set(normalized_ultimate)
                )
                extra=sorted(
                    set(normalized_ultimate)-expected_ultimate_ids
                )
                raise ValueError(
                    f"ultimate accumulator participants mismatch; "
                    f"missing={missing}, extra={extra}"
                )
            if any(value < 0 for value in normalized_ultimate.values()):
                raise ValueError("ultimate accumulator cannot be negative")
            object.__setattr__(
                self,
                "ultimate_overkill_by_participant_id",
                _freeze_mapping(normalized_ultimate),
            )

        expected_exp_ids = set(_exp_recipient_ids(self.session))
        actual_exp_ids = {str(pid) for pid in self.pending_exp_by_participant_id}
        if actual_exp_ids != expected_exp_ids:
            missing = sorted(expected_exp_ids - actual_exp_ids)
            extra = sorted(actual_exp_ids - expected_exp_ids)
            raise ValueError(
                f"pending EXP participants mismatch; missing={missing}, extra={extra}"
            )
        if any(int(value) < 0 for value in self.pending_exp_by_participant_id.values()):
            raise ValueError("pending EXP cannot be negative")

        expected_pet_ids = {
            pid for pid, participant in participants.items()
            if participant.side == "player" and participant.kind == "pet"
        }
        actual_pet_ids = {
            str(pid) for pid in self.pending_pet_variable_ai_by_participant_id
        }
        if actual_pet_ids != expected_pet_ids:
            missing = sorted(expected_pet_ids - actual_pet_ids)
            extra = sorted(actual_pet_ids - expected_pet_ids)
            raise ValueError(
                f"pending pet VARIABLEAI participants mismatch; "
                f"missing={missing}, extra={extra}"
            )
        if int(self.pending_player_dead_pet_count_delta) < 0:
            raise ValueError("pending player dead-pet count delta cannot be negative")

        expected_drop_ids={str(self.session.player.participant_id)}
        actual_drop_ids={
            str(pid) for pid in self.pending_drop_items_by_player_entry_id
        }
        if actual_drop_ids != expected_drop_ids:
            missing=sorted(expected_drop_ids-actual_drop_ids)
            extra=sorted(actual_drop_ids-expected_drop_ids)
            raise ValueError(
                f"pending drop player entries mismatch; missing={missing}, extra={extra}"
            )
        for player_id,items in self.pending_drop_items_by_player_entry_id.items():
            if len(tuple(items)) > BATTLE_PENDING_DROP_MAX:
                raise ValueError(
                    f"pending drop pool for {player_id} exceeds source buffer"
                )
            if any(not isinstance(item,BattleDropItem) for item in items):
                raise TypeError("pending drop pools must contain BattleDropItem")
        if any(not isinstance(item,BattleDropItem) for item in self.destroyed_drop_items):
            raise TypeError("destroyed drop audit must contain BattleDropItem")


@dataclass(frozen=True)
class PersistentRoundResult:
    before: PersistentBattleState
    round: ResolvedOrdinaryRound
    after: PersistentBattleState


@dataclass(frozen=True)
class PersistentBaseStatusApplicationResult:
    before: PersistentBattleState
    target_id: str
    application: BaseStatusApplicationResolution
    after: PersistentBattleState


@dataclass(frozen=True)
class PersistentCaptureResult:
    before: PersistentBattleState
    resolution: BattleCaptureResolution
    captured_target: BattleParticipant | None
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


def _exp_recipient_ids(session: BattleSession) -> tuple[str, ...]:
    ids=[
        str(participant.participant_id)
        for participant in _session_participants(session)
        if participant.side == "player"
    ]
    ride=session.ride_pet
    if ride is not None:
        if ride.side != "player" or ride.kind != "pet":
            raise ValueError("ride EXP recipient must be a player-side pet")
        if ride.source_pet_slot is None:
            raise ValueError("ride EXP recipient lacks source pet slot")
        ride_id=str(ride.participant_id)
        if ride_id not in ids:
            ids.append(ride_id)
    return tuple(ids)


def _freeze_mapping(values: Mapping) -> Mapping:
    return MappingProxyType(dict(values))


def begin_persistent_battle(
    session: BattleSession,
    *,
    slots: Mapping[str, int],
    base_status_runtime_by_participant_id: Mapping[
        str,BaseBattleStatusRuntime
    ] | None = None,
    base_damage_react_state_by_participant_id: Mapping[
        str,BaseDamageReactState
    ] | None = None,
    ride_pet_runtime: RidePetRuntime | None = None,
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
        for pid in _exp_recipient_ids(session)
    }
    pending_pet_variable_ai = {
        pid: 0
        for pid, participant in participants.items()
        if participant.side == "player" and participant.kind == "pet"
    }
    pending_drops={
        str(session.player.participant_id): ()
    }
    state = PersistentBattleState(
        session=session,
        slots=_freeze_mapping(normalized_slots),
        hp_by_participant_id=_freeze_mapping(hp),
        pending_exp_by_participant_id=_freeze_mapping(pending_exp),
        pending_pet_variable_ai_by_participant_id=_freeze_mapping(
            pending_pet_variable_ai
        ),
        pending_drop_items_by_player_entry_id=_freeze_mapping(pending_drops),
        escape_count_by_participant_id=_freeze_mapping({
            pid:0
            for pid,participant in participants.items()
            if participant.kind != "pet"
        }),
        base_status_runtime_by_participant_id=(
            base_status_runtime_by_participant_id
        ),
        base_damage_react_state_by_participant_id=(
            base_damage_react_state_by_participant_id
        ),
        ride_pet_runtime=ride_pet_runtime,
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
    runtime=state.base_status_runtime_by_participant_id[participant_id]
    return replace(
        participant,
        hp=int(state.hp_by_participant_id[participant_id]),
        quick=(
            int(participant.quick)
            if runtime.work_quick is None
            else int(runtime.work_quick)
        ),
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


def apply_persistent_base_status_application(
    state: PersistentBattleState,
    *,
    target_id: str,
    application: BaseStatusApplicationResolution,
) -> PersistentBaseStatusApplicationResult:
    """Persist one already-resolved common base-status application.

    The status hit formula remains in the pure status/magic layer. This seam
    only commits its result after checking target identity, liveness and the
    exact pre-application status snapshot.
    """
    if state.phase != ACTIVE:
        raise ValueError("cannot apply battle status after battle termination")
    target_id=str(target_id)
    participants=_participant_map(state.session)
    if target_id not in participants:
        raise KeyError(f"unknown battle status target {target_id}")
    if int(state.hp_by_participant_id[target_id]) <= 0:
        raise ValueError("common status application target must be alive")
    if not isinstance(application,BaseStatusApplicationResolution):
        raise TypeError("application must be BaseStatusApplicationResolution")

    runtime=state.base_status_runtime_by_participant_id[target_id]
    if runtime.status != application.status_before:
        raise ValueError("base status application pre-state drift")

    if not application.check.success:
        return PersistentBaseStatusApplicationResult(
            before=state,
            target_id=target_id,
            application=application,
            after=state,
        )

    runtimes=dict(state.base_status_runtime_by_participant_id)
    runtimes[target_id]=replace(
        runtime,
        status=application.status_after,
    )
    after=replace(
        state,
        base_status_runtime_by_participant_id=_freeze_mapping(runtimes),
    )
    return PersistentBaseStatusApplicationResult(
        before=state,
        target_id=target_id,
        application=application,
        after=after,
    )


def resolve_persistent_capture_transition(
    state: PersistentBattleState,
    *,
    attacker_id: str,
    target_id: str,
    inputs: BattleCaptureInputs,
    roll_1_100: int | None,
) -> PersistentCaptureResult:
    """Apply only the post-BATTLE_CaptureCheck battle-entry transition.

    Command initiative/target-adjust dispatch is intentionally outside this
    seam. On success the enemy is removed like BATTLE_Exit(), while HP is not
    forced to zero and no kill-profit scan runs; capture therefore cannot
    manufacture EXP or drop ownership.
    """
    if state.phase != ACTIVE:
        raise ValueError("cannot capture after battle termination")
    participants=_participant_map(state.session)
    attacker_id=str(attacker_id)
    target_id=str(target_id)
    if attacker_id not in participants:
        raise KeyError(f"unknown capture attacker {attacker_id}")
    if target_id not in participants:
        raise KeyError(f"unknown capture target {target_id}")
    attacker=participants[attacker_id]
    target=participants[target_id]
    if attacker.side != "player" or attacker.kind != "player":
        raise ValueError("capture attacker must be the player battle entry")
    if target.side != "enemy" or target.kind != "enemy":
        raise ValueError("capture target must be an enemy battle entry")
    current_hp=int(state.hp_by_participant_id[target_id])
    if current_hp <= 0:
        raise ValueError("cannot capture a non-living battle target")
    if int(inputs.attacker_level) != int(attacker.level):
        raise ValueError("capture attacker level drift")
    if int(inputs.target_level) != int(target.level):
        raise ValueError("capture target level drift")
    if int(inputs.target_hp) != current_hp:
        raise ValueError("capture target current HP drift")
    if int(inputs.target_max_hp) != int(target.max_hp):
        raise ValueError("capture target max HP drift")
    if target.capturable is None:
        raise ValueError("capture target lacks PETFLG provenance")
    if bool(inputs.target_capturable) != bool(target.capturable):
        raise ValueError("capture PETFLG provenance drift")
    if target.capture_default is None:
        raise ValueError("capture target lacks enemybase GET provenance")
    if int(inputs.target_capture_default) != int(target.capture_default):
        raise ValueError("capture default provenance drift")

    resolution=resolve_battle_capture_attempt(inputs,roll_1_100=roll_1_100)
    if not resolution.success:
        return PersistentCaptureResult(
            before=state,
            resolution=resolution,
            captured_target=None,
            after=state,
        )

    captured=participant_snapshot(state,target_id)
    remaining_enemies=tuple(
        enemy for enemy in state.session.enemies
        if str(enemy.participant_id) != target_id
    )
    if len(remaining_enemies) != len(state.session.enemies)-1:
        raise ValueError("capture target was not uniquely present in enemy entries")
    next_session=replace(state.session,enemies=remaining_enemies)
    slots=dict(state.slots)
    hp=dict(state.hp_by_participant_id)
    slots.pop(target_id)
    hp.pop(target_id)
    next_state=PersistentBattleState(
        session=next_session,
        slots=_freeze_mapping(slots),
        hp_by_participant_id=_freeze_mapping(hp),
        pending_exp_by_participant_id=state.pending_exp_by_participant_id,
        pending_pet_variable_ai_by_participant_id=(
            state.pending_pet_variable_ai_by_participant_id
        ),
        pending_drop_items_by_player_entry_id=(
            state.pending_drop_items_by_player_entry_id
        ),
        pending_player_charm_delta=state.pending_player_charm_delta,
        pending_player_dead_pet_count_delta=(
            state.pending_player_dead_pet_count_delta
        ),
        destroyed_drop_items=state.destroyed_drop_items,
        turn=state.turn,
        phase=ACTIVE,
        result=None,
        winning_side=None,
        last_commands=state.last_commands,
        escape_count_by_participant_id=_freeze_mapping({
            pid:count
            for pid,count in state.escape_count_by_participant_id.items()
            if pid != target_id
        }),
        base_status_runtime_by_participant_id=_freeze_mapping({
            pid:runtime
            for pid,runtime in (
                state.base_status_runtime_by_participant_id.items()
            )
            if pid != target_id
        }),
        base_damage_react_state_by_participant_id=_freeze_mapping({
            pid:react_state
            for pid,react_state in (
                state.base_damage_react_state_by_participant_id.items()
            )
            if pid != target_id
        }),
        ride_pet_runtime=state.ride_pet_runtime,
        ultimate_overkill_by_participant_id=_freeze_mapping({
            pid:value
            for pid,value in (
                state.ultimate_overkill_by_participant_id.items()
            )
            if pid != target_id
        }),
    )
    next_state=_with_termination(next_state)
    return PersistentCaptureResult(
        before=state,
        resolution=resolution,
        captured_target=captured,
        after=next_state,
    )


def _pending_profit_after_ordinary_round(
    state: PersistentBattleState,
    round_result: ResolvedOrdinaryRound,
    *,
    no_risk: bool = False,
    drop_rolls_by_enemy_id: Mapping[str,Sequence[DropAllocationRoll]] | None = None,
) -> tuple[
    Mapping[str,int],
    Mapping[str,int],
    Mapping[str,tuple[BattleDropItem,...]],
    int,
    int,
    tuple[BattleDropItem,...],
]:
    """Apply ordinary-kill EXP/loyalty and the source-shaped item buffer."""
    participants = _participant_map(state.session)
    participant_id_by_slot = {
        int(slot): str(pid)
        for pid, slot in state.slots.items()
    }
    pending_exp = {
        str(pid): int(value)
        for pid, value in state.pending_exp_by_participant_id.items()
    }
    pending_variable_ai = {
        str(pid): int(value)
        for pid, value in state.pending_pet_variable_ai_by_participant_id.items()
    }
    pending_drops={
        str(pid): tuple(items)
        for pid,items in state.pending_drop_items_by_player_entry_id.items()
    }
    pending_player_charm_delta=int(state.pending_player_charm_delta)
    pending_player_dead_pet_count_delta=int(
        state.pending_player_dead_pet_count_delta
    )
    destroyed=list(state.destroyed_drop_items)
    drop_rolls={
        str(enemy_id): tuple(rolls)
        for enemy_id,rolls in (drop_rolls_by_enemy_id or {}).items()
    }
    consumed_drop_rolls=set()
    ride_runtime=state.ride_pet_runtime
    ride_mounted=bool(
        ride_runtime is not None and ride_runtime.mounted
    )
    ride_rider_id=(
        None if ride_runtime is None else str(ride_runtime.rider_id)
    )

    for event in round_result.events:
        if event.ride_pet_fell_rider_id is not None:
            if (
                ride_rider_id is None
                or str(event.ride_pet_fell_rider_id) != ride_rider_id
            ):
                raise ValueError("ride-pet fall event references unknown rider")
            ride_mounted=False
        if event.target_hp_before is None or event.target_hp_after is None:
            continue
        if int(event.target_hp_before) <= 0 or int(event.target_hp_after) != 0:
            continue
        if event.resolved_target_slot is None:
            continue
        target_id = participant_id_by_slot.get(int(event.resolved_target_slot))
        if target_id is None:
            raise ValueError("resolved death target slot has no participant")
        target = participants[target_id]

        if target.side == "player" and target.kind in {"player","pet"}:
            if target.kind == "player":
                allied=tuple(state.session.allied_pets)
                if len(allied) > 1:
                    raise ValueError(
                        "player-death penalty requires a unique active/default pet"
                    )
                default_pet_id=(
                    None if not allied else str(allied[0].participant_id)
                )
                if int(event.ultimate_kind) > 0:
                    penalty=resolve_battle_ultimate_death_penalty(
                        BattleUltimateDeathInputs(
                            victim_kind="player",
                            victim_level=int(target.level),
                            no_risk=bool(no_risk),
                            default_pet_present=(
                                default_pet_id is not None
                            ),
                        )
                    )
                else:
                    penalty=resolve_battle_normal_death_penalty(
                        BattleNormalDeathInputs(
                            victim_kind="player",
                            victim_level=int(target.level),
                            no_risk=bool(no_risk),
                            default_pet_present=(
                                default_pet_id is not None
                            ),
                        )
                    )
                pending_player_charm_delta+=int(
                    penalty.player_charm_delta
                )
                if default_pet_id is not None:
                    if default_pet_id not in pending_variable_ai:
                        raise ValueError(
                            "player-death pet penalty references unknown allied pet"
                        )
                    pending_variable_ai[default_pet_id]+=int(
                        penalty.default_pet_variable_ai_delta
                    )
            else:
                if int(event.ultimate_kind) > 0:
                    penalty=resolve_battle_ultimate_death_penalty(
                        BattleUltimateDeathInputs(
                            victim_kind="pet",
                            victim_level=int(target.level),
                            owner_level=int(
                                state.session.player.level
                            ),
                            no_risk=bool(no_risk),
                        )
                    )
                else:
                    penalty=resolve_battle_normal_death_penalty(
                        BattleNormalDeathInputs(
                            victim_kind="pet",
                            victim_level=int(target.level),
                            owner_level=int(
                                state.session.player.level
                            ),
                            no_risk=bool(no_risk),
                        )
                    )
                if target_id not in pending_variable_ai:
                    raise ValueError(
                        "pet-death penalty references unknown allied pet"
                    )
                pending_variable_ai[target_id]+=int(
                    penalty.victim_pet_variable_ai_delta
                )
                pending_player_dead_pet_count_delta+=int(
                    penalty.owner_dead_pet_count_delta
                )

        actor_id = str(event.participant_id)
        actor = participants[actor_id]
        if actor.side != "player":
            continue
        if target.kind != "enemy":
            continue
        if target.reward_exp is None:
            raise ValueError(
                f"enemy {target_id} lacks reward EXP provenance"
            )

        profit_actor_ids=(
            tuple(str(pid) for pid in event.profit_participant_ids)
            if event.profit_participant_ids
            else (actor_id,)
        )
        if len(profit_actor_ids) != len(set(profit_actor_ids)):
            raise ValueError("profit attack-list contains duplicate participant ids")
        profit_recipients=[]
        for profit_actor_id in profit_actor_ids:
            if profit_actor_id not in participants:
                raise ValueError(
                    f"profit attack-list references unknown actor {profit_actor_id}"
                )
            profit_actor=participants[profit_actor_id]
            if profit_actor.side != "player":
                raise ValueError(
                    "enemy death profit attack-list crossed battle sides"
                )
            ride=(
                state.session.ride_pet
                if (
                    profit_actor.kind == "player"
                    and ride_mounted
                    and ride_rider_id == profit_actor_id
                )
                else None
            )
            profit_recipients.append(
                KillProfitRecipient(
                    profit_actor_id,
                    int(profit_actor.level),
                    str(profit_actor.kind),
                    ride_pet_id=(
                        None if ride is None else str(ride.participant_id)
                    ),
                    ride_pet_level=(
                        None if ride is None else int(ride.level)
                    ),
                )
            )
        profit=battle_kill_profit(
            int(target.reward_exp),
            int(target.level),
            tuple(profit_recipients),
        )
        for participant_id,award in profit.direct_exp_by_participant_id.items():
            pending_exp[participant_id]+=int(award)
        for participant_id,award in profit.ride_exp_by_participant_id.items():
            if participant_id not in pending_exp:
                raise ValueError(
                    f"ride kill profit references unknown EXP recipient {participant_id}"
                )
            pending_exp[participant_id]+=int(award)
        for participant_id,delta in (
            profit.pet_variable_ai_delta_by_participant_id.items()
        ):
            if participant_id not in pending_variable_ai:
                raise ValueError(
                    f"pet kill profit references non-allied pet {participant_id}"
                )
            pending_variable_ai[participant_id]+=int(delta)

        reward_items=tuple(target.reward_items)
        if reward_items:
            if target_id not in drop_rolls:
                raise ValueError(
                    f"enemy {target_id} drop allocation requires explicit RNG rolls"
                )
            allocation=allocate_battle_drop_items(
                reward_items,
                tuple(
                    DropRecipientTicket(
                        profit_actor_id,
                        str(state.session.player.participant_id),
                    )
                    for profit_actor_id in profit_actor_ids
                ),
                drop_rolls[target_id],
                pending_by_player_entry_id=pending_drops,
            )
            pending_drops={
                str(pid): tuple(items)
                for pid,items in allocation.pending_by_player_entry_id.items()
            }
            destroyed.extend(allocation.destroyed_items)
            consumed_drop_rolls.add(target_id)
        elif target_id in drop_rolls:
            if drop_rolls[target_id]:
                raise ValueError(
                    f"enemy {target_id} has no reward items but drop rolls were supplied"
                )
            consumed_drop_rolls.add(target_id)

    unused=sorted(set(drop_rolls)-consumed_drop_rolls)
    if unused:
        raise ValueError(f"drop RNG supplied for enemies not killed this round: {unused}")

    return (
        _freeze_mapping(pending_exp),
        _freeze_mapping(pending_variable_ai),
        _freeze_mapping(pending_drops),
        int(pending_player_charm_delta),
        int(pending_player_dead_pet_count_delta),
        tuple(destroyed),
    )
def resolve_persistent_ordinary_round(
    state: PersistentBattleState,
    *,
    commands: Mapping[str, BattleCommand],
    initiative_random_subtracts: Mapping[str, int],
    profiles: Mapping[str, BattleCombatProfile],
    attack_rolls: Mapping[str, OrdinaryAttackRolls],
    defense_profile: str,
    capture_contexts: Mapping[str, OrdinaryCaptureContext] | None = None,
    capture_rolls: Mapping[str, OrdinaryCaptureRolls] | None = None,
    escape_contexts: Mapping[str, OrdinaryEscapeContext] | None = None,
    escape_rolls: Mapping[str, OrdinaryEscapeRolls] | None = None,
    counter_rolls_by_attack_id: Mapping[
        str,Sequence[CounterAttemptRolls]
    ] | None = None,
    counter_abio_by_participant_id: Mapping[str,bool] | None = None,
    battle_abio_by_participant_id: Mapping[str,bool] | None = None,
    combo_start_rolls_1_100: Mapping[str,int] | None = None,
    combo_rolls_by_starter_id: Mapping[
        str,ComboExecutionRolls
    ] | None = None,
    base_status_rolls_by_participant_id: Mapping[
        str,BaseStatusTurnRolls
    ] | None = None,
    base_status_combat_profiles_by_participant_id: Mapping[
        str,BaseStatusCombatProfile
    ] | None = None,
    status_application_rolls_by_attack_id: Mapping[str,int] | None = None,
    guardian_registrations_by_defender_slot: Mapping[
        int,GuardianRegistration
    ] | None = None,
    command_setup_effects_by_participant_id: Mapping[
        str,BattleCommandSetupEffects
    ] | None = None,
    no_risk: bool = False,
    drop_rolls_by_enemy_id: Mapping[
        str,Sequence[DropAllocationRoll]
    ] | None = None,
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

    normalized_escape_contexts=dict(escape_contexts or {})
    for participant_id,context in normalized_escape_contexts.items():
        participant_id=str(participant_id)
        if participant_id not in state.escape_count_by_participant_id:
            raise ValueError(
                f"escape context references non-escape battle entry {participant_id}"
            )
        expected=int(state.escape_count_by_participant_id[participant_id])
        if int(context.stored_escape_count_before) != expected:
            raise ValueError(
                f"escape counter drift for {participant_id}: "
                f"state={expected}, context={context.stored_escape_count_before}"
            )

    prepared = prepare_battle_round(
        participants,
        commands,
        initiative_random_subtracts,
        tie_break_order=tie_break_order,
    )
    prepared = apply_base_combo_rewrite(
        prepared,
        profiles,
        combo_start_rolls_1_100,
        base_status_runtime_by_participant_id=_freeze_mapping({
            participant_id:
                state.base_status_runtime_by_participant_id[participant_id]
            for participant_id in living_ids
        }),
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
        capture_contexts=capture_contexts,
        capture_rolls=capture_rolls,
        escape_contexts=normalized_escape_contexts,
        escape_rolls=escape_rolls,
        counter_rolls_by_attack_id=counter_rolls_by_attack_id,
        counter_abio_by_participant_id=counter_abio_by_participant_id,
        battle_abio_by_participant_id=battle_abio_by_participant_id,
        ultimate_overkill_by_participant_id=_freeze_mapping({
            participant_id:
                state.ultimate_overkill_by_participant_id[participant_id]
            for participant_id in living_ids
        }),
        combo_rolls_by_starter_id=combo_rolls_by_starter_id,
        base_status_runtime_by_participant_id=_freeze_mapping({
            participant_id:
                state.base_status_runtime_by_participant_id[participant_id]
            for participant_id in living_ids
        }),
        base_status_rolls_by_participant_id=(
            base_status_rolls_by_participant_id
        ),
        base_status_combat_profiles_by_participant_id=(
            base_status_combat_profiles_by_participant_id
        ),
        status_application_rolls_by_attack_id=(
            status_application_rolls_by_attack_id
        ),
        guardian_registrations_by_defender_slot=(
            guardian_registrations_by_defender_slot
        ),
        command_setup_effects_by_participant_id=(
            command_setup_effects_by_participant_id
        ),
        base_damage_react_state_by_participant_id=_freeze_mapping({
            participant_id:
                state.base_damage_react_state_by_participant_id[participant_id]
            for participant_id in living_ids
        }),
        ride_pet_runtime=state.ride_pet_runtime,
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
    (
        pending_exp,
        pending_variable_ai,
        pending_drops,
        pending_player_charm_delta,
        pending_player_dead_pet_count_delta,
        destroyed_drops,
    )=_pending_profit_after_ordinary_round(
        state,
        round_result,
        no_risk=bool(no_risk),
        drop_rolls_by_enemy_id=drop_rolls_by_enemy_id,
    )
    exited_ids={str(pid) for pid in round_result.exited_participant_ids}
    enemy_ids={str(enemy.participant_id) for enemy in state.session.enemies}
    invalid_exits=sorted(exited_ids-enemy_ids)
    if invalid_exits:
        raise ValueError(f"ordinary round exited non-enemy entries: {invalid_exits}")

    escaped_ids={str(pid) for pid in round_result.escaped_participant_ids}
    player_id=str(state.session.player.participant_id)
    allied_pet_ids={
        str(pet.participant_id) for pet in state.session.allied_pets
    }
    invalid_escapes=sorted(
        escaped_ids-({player_id}|allied_pet_ids|enemy_ids)
    )
    if invalid_escapes:
        raise ValueError(
            f"ordinary round escaped unknown entries: {invalid_escapes}"
        )
    if (escaped_ids & allied_pet_ids) and player_id not in escaped_ids:
        raise ValueError("allied pet escaped without its player entry")

    escape_counts=dict(state.escape_count_by_participant_id)
    for event in round_result.events:
        if event.escape_resolution is None:
            continue
        pid=str(event.participant_id)
        if pid not in escape_counts:
            raise ValueError(f"escape event has no stored counter for {pid}")
        escape_counts[pid]=int(
            event.escape_resolution.stored_escape_count_after
        )

    escaped_enemy_ids=escaped_ids & enemy_ids
    removed_enemy_ids=exited_ids | escaped_enemy_ids
    next_session=(
        replace(
            state.session,
            enemies=tuple(
                enemy for enemy in state.session.enemies
                if str(enemy.participant_id) not in removed_enemy_ids
            ),
        )
        if removed_enemy_ids
        else state.session
    )
    next_slots=dict(state.slots)
    next_status_runtime=dict(
        state.base_status_runtime_by_participant_id
    )
    next_status_runtime.update(
        dict(round_result.base_status_runtime_by_participant_id)
    )
    next_damage_react=dict(
        state.base_damage_react_state_by_participant_id
    )
    next_damage_react.update(
        dict(round_result.base_damage_react_state_by_participant_id)
    )
    next_ultimate_overkill=dict(
        state.ultimate_overkill_by_participant_id
    )
    next_ultimate_overkill.update(
        dict(round_result.ultimate_overkill_by_participant_id)
    )
    for pid in removed_enemy_ids:
        next_slots.pop(pid,None)
        hp.pop(pid,None)
        escape_counts.pop(pid,None)
        next_status_runtime.pop(pid,None)
        next_damage_react.pop(pid,None)
        next_ultimate_overkill.pop(pid,None)

    next_state = PersistentBattleState(
        session=next_session,
        slots=_freeze_mapping(next_slots),
        hp_by_participant_id=_freeze_mapping(hp),
        pending_exp_by_participant_id=pending_exp,
        pending_pet_variable_ai_by_participant_id=pending_variable_ai,
        pending_drop_items_by_player_entry_id=pending_drops,
        pending_player_charm_delta=pending_player_charm_delta,
        pending_player_dead_pet_count_delta=(
            pending_player_dead_pet_count_delta
        ),
        destroyed_drop_items=destroyed_drops,
        turn=int(state.turn) + 1,
        phase=ACTIVE,
        result=None,
        winning_side=None,
        last_commands=_freeze_mapping(commands),
        escape_count_by_participant_id=_freeze_mapping(escape_counts),
        base_status_runtime_by_participant_id=_freeze_mapping(
            next_status_runtime
        ),
        base_damage_react_state_by_participant_id=_freeze_mapping(
            next_damage_react
        ),
        ride_pet_runtime=round_result.ride_pet_runtime,
        ultimate_overkill_by_participant_id=_freeze_mapping(
            next_ultimate_overkill
        ),
    )
    if player_id in escaped_ids:
        next_state=replace(
            next_state,
            phase=FINISHED,
            result=PLAYER_ESCAPE,
            winning_side=None,
        )
    else:
        next_state = _with_termination(next_state)
    return PersistentRoundResult(
        before=state,
        round=round_result,
        after=next_state,
    )
