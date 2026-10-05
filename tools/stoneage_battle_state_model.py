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

from tools.stoneage_attack_magic_action_model import EnemyAttackMagicActionRolls
from tools.stoneage_attack_magic_state_model import AttackMagicRoundOverlay
from tools.stoneage_enemy_ai_attack_magic_bridge import EnemyAiAttackMagicSubmission
from tools.stoneage_enemy_ai_rehp_bridge import EnemyAiReHpSubmission
from tools.stoneage_enemy_ai_relife_bridge import EnemyAiReLifeSubmission
from tools.stoneage_enemy_ai_damage_to_hp_bridge import (
    EnemyAiDamageToHpSubmission,
)
from tools.stoneage_enemy_ai_mp_damage_bridge import EnemyAiMpDamageSubmission
from tools.stoneage_enemy_ai_fall_ground_bridge import (
    EnemyAiFallGroundSubmission,
)
from tools.stoneage_enemy_ai_battle_tear_bridge import (
    EnemyAiBattleTearSubmission,
)
from tools.stoneage_enemy_ai_nocast_bridge import EnemyAiNocastSubmission
from tools.stoneage_enemy_ai_barrier_bridge import EnemyAiBarrierSubmission
from tools.stoneage_enemy_ai_guard_break2_bridge import (
    EnemyAiGuardBreak2Submission,
)
from tools.stoneage_enemy_ai_battletimid_bridge import (
    EnemyAiBattleTimidSubmission,
)
from tools.stoneage_enemy_ai_lighttakeed_bridge import (
    EnemyAiLighttakeedSubmission,
)
from tools.stoneage_enemy_ai_combined_bridge import EnemyAiCombinedSubmission
from tools.stoneage_enemy_ai_vary_bridge import EnemyAiVarySubmission
from tools.stoneage_vary_runtime_state import VaryRuntimeOverlay
from tools.stoneage_combined_runtime_state import (
    CombinedActionRolls,
    CombinedRuntimeOverlay,
)
from tools.stoneage_combined_initiative_model import resolve_combined_initiative
from tools.stoneage_nocast_runtime_state import (
    NocastActionRolls,
    NocastRoundOverlay,
)
from tools.stoneage_barrier_runtime_state import BarrierActionRolls
from tools.stoneage_enemy_ai_weaken_bridge import EnemyAiWeakenSubmission
from tools.stoneage_weaken_runtime_state import WeakenActionRolls
from tools.stoneage_enemy_ai_refresh_bridge import EnemyAiRefreshSubmission
from tools.stoneage_refresh_runtime_state import RefreshActionRolls
from tools.stoneage_enemy_ai_setmagicpet_bridge import EnemyAiSetMagicPetSubmission
from tools.stoneage_setmagicpet_runtime_state import (
    SetMagicPetActionRolls,
    SetMagicPetRoundOverlay,
    prepare_setmagicpet_powers,
)
from tools.stoneage_weaken_model import resolve_weaken_recalculation
from tools.stoneage_nocast_runtime_state import PreparedWeakenPowers
from tools.stoneage_enemy_rehp_model import EnemyReHpRolls
from tools.stoneage_enemy_relife_model import EnemyReLifeRolls
from tools.stoneage_recovered25_attack_magic_runtime import Recovered25AttackMagicRuntime

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
from tools.stoneage_enemy_ai_attack_crazed_bridge import EnemyAiAttackCrazedSubmission
from tools.stoneage_enemy_ai_wildviolent_bridge import EnemyAiWildViolentSubmission
from tools.stoneage_enemy_ai_modifyattack_bridge import EnemyAiModifyAttackSubmission
from tools.stoneage_enemy_ai_mdfyattack_bridge import EnemyAiMdfyAttackSubmission
from tools.stoneage_battle_round_model import (
    AttackCrazedRolls,
    WildViolentRolls,
    BattleCombatProfile,
    BattleCommand,
    BattleCommandSetupEffects,
    BATTLE_COM_S_CHARGE,
    BATTLE_COM_S_EARTHROUND0,
    ComboExecutionRolls,
    ContinuationAttackRolls,
    CounterAttemptRolls,
    OrdinaryAttackRolls,
    OrdinaryCaptureContext,
    OrdinaryCaptureRolls,
    OrdinaryAbductContext,
    OrdinaryAbductRolls,
    OrdinaryStealRolls,
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
    # Commands preserved by fixed BATTLE_AllCharaCWaitSet across rounds.
    # Stable S_CHARGE and phase-2 S_EARTHROUND0 are admitted here.
    carried_commands_by_participant_id: Mapping[
        str,BattleCommand
    ] | None = None
    carried_setup_effects_by_participant_id: Mapping[
        str,BattleCommandSetupEffects
    ] | None = None
    escape_count_by_participant_id: Mapping[str,int] | None = None
    base_status_runtime_by_participant_id: Mapping[
        str,BaseBattleStatusRuntime
    ] | None = None
    base_damage_react_state_by_participant_id: Mapping[
        str,BaseDamageReactState
    ] | None = None
    ride_pet_runtime: RidePetRuntime | None = None
    ultimate_overkill_by_participant_id: Mapping[str,int] | None = None
    ultimate_exited_participant_ids: tuple[str,...] = ()
    # Non-death BATTLE_Exit/PetDefaultExit entries (e.g. Abduct) stay in the
    # battle session identity graph but no longer participate in later rounds.
    battle_exited_participant_ids: tuple[str,...] = ()
    # Ordinary dead entries remain in the battle array and can be selected by
    # ReLife. Ultimate/BATTLE_Exit entries are deliberately excluded.
    revivable_dead_participant_ids: tuple[str,...] = ()
    nocast_overlay: NocastRoundOverlay | None = None
    setmagicpet_overlay: SetMagicPetRoundOverlay | None = None
    combined_overlay: CombinedRuntimeOverlay | None = None
    vary_overlay: VaryRuntimeOverlay | None = None

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
        if self.nocast_overlay is not None:
            if not isinstance(self.nocast_overlay,NocastRoundOverlay):
                raise TypeError("persistent Nocast overlay has wrong type")
            overlay_ids=set(self.nocast_overlay.runtime_by_participant_id)
            if overlay_ids != set(participants):
                missing=sorted(set(participants)-overlay_ids)
                extra=sorted(overlay_ids-set(participants))
                raise ValueError(
                    "persistent Nocast overlay participant mismatch; "
                    f"missing={missing}, extra={extra}"
                )
        if self.setmagicpet_overlay is not None:
            if not isinstance(self.setmagicpet_overlay,SetMagicPetRoundOverlay):
                raise TypeError("persistent SetMagicPet overlay has wrong type")
            overlay_ids=set(
                self.setmagicpet_overlay.runtime_by_participant_id
            )
            if overlay_ids != set(participants):
                missing=sorted(set(participants)-overlay_ids)
                extra=sorted(overlay_ids-set(participants))
                raise ValueError(
                    "persistent SetMagicPet overlay participant mismatch; "
                    f"missing={missing}, extra={extra}"
                )
        if self.combined_overlay is not None:
            if not isinstance(self.combined_overlay,CombinedRuntimeOverlay):
                raise TypeError("persistent Combined overlay has wrong type")
            self.combined_overlay.validate_participants(participants)
        if self.vary_overlay is not None:
            if not isinstance(self.vary_overlay,VaryRuntimeOverlay):
                raise TypeError("persistent Vary overlay has wrong type")
            unknown_vary=sorted(
                set(self.vary_overlay.runtime_by_participant_id)-set(participants)
            )
            if unknown_vary:
                raise ValueError(
                    "persistent Vary overlay references unknown participants: "
                    f"{unknown_vary}"
                )
        normalized_ultimate_exits=tuple(
            str(pid) for pid in self.ultimate_exited_participant_ids
        )
        if len(normalized_ultimate_exits) != len(set(normalized_ultimate_exits)):
            raise ValueError("ultimate-exited participants cannot contain duplicates")
        unknown_ultimate_exits=sorted(
            set(normalized_ultimate_exits)-set(participants)
        )
        if unknown_ultimate_exits:
            raise ValueError(
                "ultimate-exited participants are not in battle session: "
                f"{unknown_ultimate_exits}"
            )
        object.__setattr__(
            self,
            "ultimate_exited_participant_ids",
            normalized_ultimate_exits,
        )
        normalized_battle_exits=tuple(
            str(pid) for pid in self.battle_exited_participant_ids
        )
        if len(normalized_battle_exits) != len(set(normalized_battle_exits)):
            raise ValueError("battle-exited participants cannot contain duplicates")
        unknown_battle_exits=sorted(
            set(normalized_battle_exits)-set(participants)
        )
        if unknown_battle_exits:
            raise ValueError(
                "battle-exited participants are not in battle session: "
                f"{unknown_battle_exits}"
            )
        overlap=sorted(
            set(normalized_battle_exits)&set(normalized_ultimate_exits)
        )
        if overlap:
            raise ValueError(
                "participant cannot be both ordinary battle-exited and "
                f"ultimate-exited: {overlap}"
            )
        object.__setattr__(
            self,
            "battle_exited_participant_ids",
            normalized_battle_exits,
        )
        normalized_revivable=tuple(
            str(pid) for pid in self.revivable_dead_participant_ids
        )
        if len(normalized_revivable) != len(set(normalized_revivable)):
            raise ValueError(
                "revivable-dead participants cannot contain duplicates"
            )
        unknown_revivable=sorted(
            set(normalized_revivable)-set(participants)
        )
        if unknown_revivable:
            raise ValueError(
                "revivable-dead participants are not in battle session: "
                f"{unknown_revivable}"
            )
        invalid_revivable=sorted(
            set(normalized_revivable)
            & (set(normalized_battle_exits)|set(normalized_ultimate_exits))
        )
        if invalid_revivable:
            raise ValueError(
                "battle-exited participants cannot remain revivable: "
                f"{invalid_revivable}"
            )
        nonenemy_revivable=sorted(
            pid for pid in normalized_revivable
            if participants[pid].side != "enemy"
        )
        if nonenemy_revivable:
            raise ValueError(
                "bounded ReLife revivable participants must be enemy-side: "
                f"{nonenemy_revivable}"
            )
        nondead_revivable=sorted(
            pid for pid in normalized_revivable
            if (
                pid not in self.hp_by_participant_id
                or int(self.hp_by_participant_id[pid]) != 0
            )
        )
        if nondead_revivable:
            raise ValueError(
                "revivable-dead participants must have zero HP: "
                f"{nondead_revivable}"
            )
        object.__setattr__(
            self,
            "revivable_dead_participant_ids",
            normalized_revivable,
        )

        if self.carried_commands_by_participant_id is None:
            object.__setattr__(
                self,
                "carried_commands_by_participant_id",
                _freeze_mapping({}),
            )
        else:
            carried_commands={
                str(pid):command
                for pid,command in self.carried_commands_by_participant_id.items()
            }
            unknown=sorted(set(carried_commands)-set(participants))
            if unknown:
                raise ValueError(
                    f"carried commands reference unknown participants: {unknown}"
                )
            for pid,command in carried_commands.items():
                if not isinstance(command,BattleCommand):
                    raise TypeError(
                        f"carried command for {pid} has wrong type"
                    )
                if int(command.command1) not in {
                    BATTLE_COM_S_CHARGE,
                    BATTLE_COM_S_EARTHROUND0,
                }:
                    raise ValueError(
                        "persistent carried-command seam admits only "
                        "S_CHARGE or S_EARTHROUND0"
                    )
            object.__setattr__(
                self,
                "carried_commands_by_participant_id",
                _freeze_mapping(carried_commands),
            )

        if self.carried_setup_effects_by_participant_id is None:
            object.__setattr__(
                self,
                "carried_setup_effects_by_participant_id",
                _freeze_mapping({}),
            )
        else:
            carried_effects={
                str(pid):effects
                for pid,effects in (
                    self.carried_setup_effects_by_participant_id.items()
                )
            }
            if set(carried_effects) != set(
                self.carried_commands_by_participant_id
            ):
                raise ValueError(
                    "carried setup effects must match carried command IDs"
                )
            for pid,effects in carried_effects.items():
                if not isinstance(effects,BattleCommandSetupEffects):
                    raise TypeError(
                        f"carried setup effects for {pid} have wrong type"
                    )
                command=self.carried_commands_by_participant_id[pid]
                if (
                    int(command.command1) == BATTLE_COM_S_CHARGE
                    and effects.charge_ready_attack_power is None
                ):
                    raise ValueError(
                        f"carried S_CHARGE lacks ready attack power: {pid}"
                    )
            object.__setattr__(
                self,
                "carried_setup_effects_by_participant_id",
                _freeze_mapping(carried_effects),
            )

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
    attack_magic_overlay_before: AttackMagicRoundOverlay | None = None
    attack_magic_overlay_after: AttackMagicRoundOverlay | None = None


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
    nocast_overlay: NocastRoundOverlay | None = None,
    setmagicpet_overlay: SetMagicPetRoundOverlay | None = None,
    combined_overlay: CombinedRuntimeOverlay | None = None,
    vary_overlay: VaryRuntimeOverlay | None = None,
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
        nocast_overlay=nocast_overlay,
        setmagicpet_overlay=setmagicpet_overlay,
        combined_overlay=combined_overlay,
        vary_overlay=vary_overlay,
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
    exited=set(state.ultimate_exited_participant_ids)
    exited.update(state.battle_exited_participant_ids)
    for pid, participant in participants.items():
        if pid in exited:
            continue
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
        vary_overlay=None,
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
    magic_powers=(
        None if state.setmagicpet_overlay is None else
        state.setmagicpet_overlay.runtime_by_participant_id[
            participant_id
        ].prepared_powers
    )
    weaken_powers=(
        None if state.nocast_overlay is None else
        state.nocast_overlay.runtime_by_participant_id[
            participant_id
        ].prepared_weaken_powers
    )
    powers=weaken_powers if weaken_powers is not None else magic_powers
    if powers is not None:
        participant=replace(
            participant,attack=powers.attack,defense=powers.defense
        )
    participant=replace(
        participant,
        hp=int(state.hp_by_participant_id[participant_id]),
        quick=(
            powers.dexterity if powers is not None else (
                int(participant.quick) if runtime.work_quick is None else int(runtime.work_quick)
            )
        ),
    )
    vary=(
        None if state.vary_overlay is None else
        state.vary_overlay.runtime_by_participant_id.get(participant_id)
    )
    if vary is not None:
        participant=replace(
            participant,
            attack=int(vary.attack_power),
            defense=int(vary.defense_power),
            quick=int(vary.quick),
        )
    return participant


def active_participants(
    state: PersistentBattleState,
) -> tuple[BattleParticipant, ...]:
    """Return living actors only, retaining original session order."""
    exited=set(state.ultimate_exited_participant_ids)
    exited.update(state.battle_exited_participant_ids)
    return tuple(
        participant_snapshot(state, participant.participant_id)
        for participant in _session_participants(state.session)
        if (
            str(participant.participant_id) not in exited
            and int(state.hp_by_participant_id[participant.participant_id]) > 0
        )
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
        carried_commands_by_participant_id=_freeze_mapping({
            pid:command
            for pid,command in state.carried_commands_by_participant_id.items()
            if pid != target_id
        }),
        carried_setup_effects_by_participant_id=_freeze_mapping({
            pid:effects
            for pid,effects in (
                state.carried_setup_effects_by_participant_id.items()
            )
            if pid != target_id
        }),
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
        ultimate_exited_participant_ids=tuple(
            pid for pid in state.ultimate_exited_participant_ids
            if pid != target_id
        ),
        battle_exited_participant_ids=tuple(
            pid for pid in state.battle_exited_participant_ids
            if pid != target_id
        ),
        revivable_dead_participant_ids=tuple(
            pid for pid in state.revivable_dead_participant_ids
            if pid != target_id
        ),
        nocast_overlay=(
            None if state.nocast_overlay is None else
            NocastRoundOverlay({
                pid:runtime
                for pid,runtime in state.nocast_overlay.runtime_by_participant_id.items()
                if pid != target_id
            })
        ),
        setmagicpet_overlay=(
            None if state.setmagicpet_overlay is None else
            SetMagicPetRoundOverlay({
                pid:runtime
                for pid,runtime in state.setmagicpet_overlay.runtime_by_participant_id.items()
                if pid != target_id
            })
        ),
        combined_overlay=(
            None if state.combined_overlay is None else
            CombinedRuntimeOverlay(
                state.combined_overlay.initiative_profile,
                state.combined_overlay.status_magic_profile,
                state.combined_overlay.item_zero,
                {
                    pid:value
                    for pid,value in state.combined_overlay.mp_by_participant_id.items()
                    if pid != target_id
                },
                {
                    pid:value
                    for pid,value in state.combined_overlay.att_reverse_by_participant_id.items()
                    if pid != target_id
                },
            )
        ),
        vary_overlay=(
            None if state.vary_overlay is None else
            state.vary_overlay.retain_participants(
                {
                    pid
                    for pid in participants
                    if pid != target_id
                }
            )
        ),
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
    ultimate_exited_ids={
        str(pid) for pid in round_result.ultimate_exited_participant_ids
    }
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
                if target_id in ultimate_exited_ids:
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
                if target_id in ultimate_exited_ids:
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
    abduct_contexts: Mapping[str, OrdinaryAbductContext] | None = None,
    abduct_rolls: Mapping[str, OrdinaryAbductRolls] | None = None,
    steal_rolls: Mapping[str, OrdinaryStealRolls] | None = None,
    steal_player_gold_by_participant_id: Mapping[str,int] | None = None,
    steal_player_item_slots_by_participant_id: Mapping[
        str,Sequence[int]
    ] | None = None,
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
    mdfyattack_submissions_by_participant_id: Mapping[str,EnemyAiMdfyAttackSubmission] | None = None,
    modifyattack_submissions_by_participant_id: Mapping[str,EnemyAiModifyAttackSubmission] | None = None,
    modifyattack_rand_by_participant_id: Mapping[str,int | None] | None = None,
    attack_crazed_submissions_by_participant_id: Mapping[str,EnemyAiAttackCrazedSubmission] | None = None,
    attack_crazed_rolls_by_attack_id: Mapping[str,AttackCrazedRolls] | None = None,
    wildviolent_submissions_by_participant_id: Mapping[str,EnemyAiWildViolentSubmission] | None = None,
    wildviolent_rolls_by_attack_id: Mapping[str,WildViolentRolls] | None = None,
    continuation_rolls_by_attack_id: Mapping[
        str,ContinuationAttackRolls
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
    attack_magic_runtime: Recovered25AttackMagicRuntime | None = None,
    attack_magic_submissions_by_participant_id: Mapping[
        str,EnemyAiAttackMagicSubmission
    ] | None = None,
    attack_magic_rolls_by_participant_id: Mapping[
        str,EnemyAttackMagicActionRolls
    ] | None = None,
    attack_magic_overlay: AttackMagicRoundOverlay | None = None,
    attack_magic_retarget_rolls_by_participant_id: Mapping[
        str,Sequence[int]
    ] | None = None,
    enemy_rehp_submissions_by_participant_id: Mapping[
        str,EnemyAiReHpSubmission
    ] | None = None,
    enemy_rehp_rolls_by_participant_id: Mapping[
        str,EnemyReHpRolls
    ] | None = None,
    enemy_rehp_retarget_rolls_by_participant_id: Mapping[
        str,int | None
    ] | None = None,
    enemy_relife_submissions_by_participant_id: Mapping[
        str,EnemyAiReLifeSubmission
    ] | None = None,
    enemy_relife_rolls_by_participant_id: Mapping[
        str,EnemyReLifeRolls
    ] | None = None,
    enemy_relife_retarget_rolls_by_participant_id: Mapping[
        str,int | None
    ] | None = None,
    damage_to_hp_submissions_by_participant_id: Mapping[
        str,EnemyAiDamageToHpSubmission
    ] | None = None,
    mp_damage_submissions_by_participant_id: Mapping[
        str,EnemyAiMpDamageSubmission
    ] | None = None,
    mp_by_participant_id: Mapping[str,int] | None = None,
    battle_tear_submissions_by_participant_id: Mapping[
        str,EnemyAiBattleTearSubmission
    ] | None = None,
    guard_break2_submissions_by_participant_id: Mapping[
        str,EnemyAiGuardBreak2Submission
    ] | None = None,
    battletimid_submissions_by_participant_id: Mapping[
        str,EnemyAiBattleTimidSubmission
    ] | None = None,
    battletimid_rolls_by_participant_id: Mapping[
        str,int | None
    ] | None = None,
    lighttakeed_submissions_by_participant_id: Mapping[
        str,EnemyAiLighttakeedSubmission
    ] | None = None,
    combined_submissions_by_participant_id: Mapping[
        str,EnemyAiCombinedSubmission
    ] | None = None,
    combined_rolls_by_participant_id: Mapping[
        str,CombinedActionRolls
    ] | None = None,
    vary_submissions_by_participant_id: Mapping[
        str,EnemyAiVarySubmission
    ] | None = None,
    fall_ground_submissions_by_participant_id: Mapping[
        str,EnemyAiFallGroundSubmission
    ] | None = None,
    fall_ground_rolls_by_participant_id: Mapping[
        str,int | None
    ] | None = None,
    fall_ground_equipment_resistance_by_participant_id: Mapping[
        str,int
    ] | None = None,
    nocast_submissions_by_participant_id: Mapping[
        str,EnemyAiNocastSubmission
    ] | None = None,
    nocast_rolls_by_participant_id: Mapping[
        str,NocastActionRolls
    ] | None = None,
    weaken_submissions_by_participant_id: Mapping[str,EnemyAiWeakenSubmission] | None = None,
    weaken_rolls_by_participant_id: Mapping[str,WeakenActionRolls] | None = None,
    refresh_submissions_by_participant_id: Mapping[str,EnemyAiRefreshSubmission] | None = None,
    refresh_rolls_by_participant_id: Mapping[str,RefreshActionRolls] | None = None,
    setmagicpet_submissions_by_participant_id: Mapping[str,EnemyAiSetMagicPetSubmission] | None = None,
    setmagicpet_rolls_by_participant_id: Mapping[str,SetMagicPetActionRolls] | None = None,
    barrier_submissions_by_participant_id: Mapping[
        str,EnemyAiBarrierSubmission
    ] | None = None,
    barrier_rolls_by_participant_id: Mapping[
        str,BarrierActionRolls
    ] | None = None,
    field_attr: str = "none",
    field_power: int = 0,
    tie_break_order: Sequence[str] | None = None,
) -> PersistentRoundResult:
    if state.phase != ACTIVE:
        raise ValueError("cannot execute another round after battle termination")

    participants = active_participants(state)
    living_ids = {participant.participant_id for participant in participants}
    round_entry_ids=set(living_ids)
    passive_battle_entries_by_slot={}
    if enemy_relife_submissions_by_participant_id:
        exited_ids=set(state.ultimate_exited_participant_ids)
        exited_ids.update(state.battle_exited_participant_ids)
        for source_participant in _session_participants(state.session):
            participant_id=str(source_participant.participant_id)
            if source_participant.side != "enemy":
                continue
            if participant_id in living_ids or participant_id in exited_ids:
                continue
            if int(state.hp_by_participant_id[participant_id]) != 0:
                raise ValueError(
                    "non-living ReLife battle entry must have zero HP"
                )
            slot=int(state.slots[participant_id])
            passive_battle_entries_by_slot[slot]=participant_snapshot(
                state,participant_id
            )
            round_entry_ids.add(participant_id)
        missing_profiles=sorted(round_entry_ids-set(profiles))
        if missing_profiles:
            raise ValueError(
                "ReLife round lacks combat profiles for retained battle entries: "
                f"{missing_profiles}"
            )
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

    battletimid_submissions={
        str(pid):submission
        for pid,submission in (
            battletimid_submissions_by_participant_id or {}
        ).items()
    }
    unknown_battletimid_ids=sorted(
        set(battletimid_submissions)-living_ids
    )
    if unknown_battletimid_ids:
        raise ValueError(
            "BattleTimid submissions reference inactive actors: "
            f"{unknown_battletimid_ids}"
        )
    for pid,submission in battletimid_submissions.items():
        if not isinstance(submission,EnemyAiBattleTimidSubmission):
            raise TypeError("BattleTimid submission has wrong type")
        if str(submission.participant_id)!=pid:
            raise ValueError("BattleTimid submission participant drift")
        if state.base_status_runtime_by_participant_id[pid].status.drunk>0:
            raise ValueError(
                "BattleTimid with drunk actor is outside R1"
            )
        if (
            state.nocast_overlay is not None
            and state.nocast_overlay.runtime_by_participant_id[
                pid
            ].prepared_weaken_powers is not None
        ):
            raise ValueError(
                "BattleTimid with prepared Weaken powers is outside R1"
            )
    if battletimid_submissions:
        participants=tuple(
            replace(
                participant,
                quick=int(
                    battletimid_submissions[
                        str(participant.participant_id)
                    ].setup.quick
                ),
            )
            if str(participant.participant_id) in battletimid_submissions
            else participant
            for participant in participants
        )

    lighttakeed_submissions={
        str(pid):submission
        for pid,submission in (
            lighttakeed_submissions_by_participant_id or {}
        ).items()
    }
    unknown_lighttakeed_ids=sorted(
        set(lighttakeed_submissions)-living_ids
    )
    if unknown_lighttakeed_ids:
        raise ValueError(
            "Lighttakeed submissions reference inactive actors: "
            f"{unknown_lighttakeed_ids}"
        )
    if set(lighttakeed_submissions) & set(battletimid_submissions):
        raise ValueError("Lighttakeed and BattleTimid submissions overlap")
    for pid,submission in lighttakeed_submissions.items():
        if not isinstance(submission,EnemyAiLighttakeedSubmission):
            raise TypeError("Lighttakeed submission has wrong type")
        if str(submission.participant_id)!=pid:
            raise ValueError("Lighttakeed submission participant drift")
        if state.base_status_runtime_by_participant_id[pid].status.drunk>0:
            raise ValueError("Lighttakeed with drunk work-power state is outside R1")
        if (
            state.nocast_overlay is not None
            and state.nocast_overlay.runtime_by_participant_id[
                pid
            ].prepared_weaken_powers is not None
        ):
            raise ValueError(
                "Lighttakeed with prepared Weaken powers is outside R1"
            )
        if (
            state.setmagicpet_overlay is not None
            and state.setmagicpet_overlay.runtime_by_participant_id[
                pid
            ].prepared_powers is not None
        ):
            raise ValueError(
                "Lighttakeed with prepared SetMagicPet powers is outside R1"
            )

    modifyattack_submissions={str(pid):value for pid,value in (modifyattack_submissions_by_participant_id or {}).items()}
    if set(modifyattack_submissions)-living_ids:
        raise ValueError("Modifyattack submissions reference inactive actors")
    for pid,submission in modifyattack_submissions.items():
        if not isinstance(submission,EnemyAiModifyAttackSubmission):
            raise TypeError("Modifyattack submission has wrong type")
        if submission.participant_id!=pid:
            raise ValueError("Modifyattack participant drift")

    combined_submissions={
        str(pid):submission
        for pid,submission in (
            combined_submissions_by_participant_id or {}
        ).items()
    }
    unknown_combined_ids=sorted(set(combined_submissions)-living_ids)
    if unknown_combined_ids:
        raise ValueError(
            "Combined submissions reference inactive actors: "
            f"{unknown_combined_ids}"
        )
    if set(combined_submissions) & (
        set(battletimid_submissions) | set(lighttakeed_submissions)
    ):
        raise ValueError(
            "Combined overlaps BattleTimid/Lighttakeed submissions"
        )
    for pid,submission in combined_submissions.items():
        if not isinstance(submission,EnemyAiCombinedSubmission):
            raise TypeError("Combined submission has wrong type")
        if str(submission.participant_id)!=pid:
            raise ValueError("Combined submission participant drift")
    if combined_submissions:
        if state.combined_overlay is None:
            raise ValueError(
                "Combined persistent execution requires explicit runtime overlay"
            )
        if state.nocast_overlay is None:
            raise ValueError(
                "Combined persistent execution requires Nocast/status overlay"
            )
        missing_mp=sorted(
            set(combined_submissions)-set(
                state.combined_overlay.mp_by_participant_id
            )
        )
        if missing_mp:
            raise ValueError(
                f"Combined actors lack persistent MP witness: {missing_mp}"
            )

    vary_submissions={
        str(pid):submission
        for pid,submission in (
            vary_submissions_by_participant_id or {}
        ).items()
    }
    unknown_vary_ids=sorted(set(vary_submissions)-living_ids)
    if unknown_vary_ids:
        raise ValueError(
            f"Vary submissions reference inactive actors: {unknown_vary_ids}"
        )
    if set(vary_submissions) & (
        set(combined_submissions) | set(battletimid_submissions)
    ):
        raise ValueError("Vary overlaps Combined/BattleTimid submission")
    for pid,submission in vary_submissions.items():
        if not isinstance(submission,EnemyAiVarySubmission):
            raise TypeError("Vary submission has wrong type")
        if str(submission.participant_id)!=pid:
            raise ValueError("Vary submission participant drift")
        if (
            state.vary_overlay is not None
            and pid in state.vary_overlay.runtime_by_participant_id
        ):
            raise ValueError("Vary recast blocked while actor is transformed")

    working_vary=(
        VaryRuntimeOverlay.empty()
        if state.vary_overlay is None
        else state.vary_overlay
    )
    for pid,submission in vary_submissions.items():
        working_vary=working_vary.with_cast(
            pid,submission.runtime_after_callback
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

    # Prepared work powers belong to the preceding PreCommandSeq, even if
    # StatusSeq will expire WEAKEN later in this round. Baseline session values
    # remain untouched, so the next preparation never compounds 0.8.
    profiles=dict(profiles)
    if state.combined_overlay is not None:
        for pid in living_ids:
            if pid not in profiles:
                raise KeyError(f"missing combat profile for {pid}")
            attrs=state.combined_overlay.precommand_elements(
                pid,profiles[pid]
            )
            profiles[pid]=replace(
                profiles[pid],
                earth=int(attrs["earth"]),
                water=int(attrs["water"]),
                fire=int(attrs["fire"]),
                wind=int(attrs["wind"]),
            )
    if state.nocast_overlay is not None:
        baseline=_participant_map(state.session)
        for pid in living_ids:
            late=state.nocast_overlay.runtime_by_participant_id[pid]
            powers=late.prepared_weaken_powers
            if powers is None:
                continue
            if int(profiles[pid].fixed_dex)!=int(baseline[pid].quick):
                raise ValueError("Weaken preparation requires baseline fixed DEX/QUICK equality")
            if state.ride_pet_runtime is not None or state.base_status_runtime_by_participant_id[pid].status.drunk>0:
                raise ValueError("Weaken preparation with riding/drunk modifiers is outside the admitted domain")
            wild_submission=(wildviolent_submissions_by_participant_id or {}).get(pid)
            for effects in ((command_setup_effects_by_participant_id or {}).get(pid),
                            state.carried_setup_effects_by_participant_id.get(pid)):
                if effects is None or (
                    effects.attack_power is None and effects.defense_power is None
                ):
                    continue
                if wild_submission is None:
                    raise ValueError(
                        "Weaken prepared powers overlap unsupported callback power setup"
                    )
                # Exact recovered WildViolent rows contain both strength and
                # toughness markers.  They overwrite the prepared work values
                # from compliance-prepared FIXSTR/FIXTOUGH; QUICK/DEX remains prepared.
                expected=wild_submission.setup
                if (
                    expected.attack_power is None
                    or expected.defense_power is None
                    or (effects.attack_power,effects.defense_power)
                    != (expected.attack_power,expected.defense_power)
                ):
                    raise ValueError(
                        "WildViolentAttack/Weaken callback power setup drift"
                    )
            profiles[pid]=replace(profiles[pid],fixed_dex=powers.dexterity)

    if working_vary.runtime_by_participant_id:
        if state.ride_pet_runtime is not None:
            raise ValueError("Vary with mounted ride runtime is outside R1")
        for pid in working_vary.runtime_by_participant_id:
            if (
                state.base_status_runtime_by_participant_id[pid].status.drunk>0
            ):
                raise ValueError("Vary with drunk work-power state is outside R1")
            if (
                state.nocast_overlay is not None
                and state.nocast_overlay.runtime_by_participant_id[
                    pid
                ].prepared_weaken_powers is not None
            ):
                raise ValueError("Vary/Weaken prepared-power overlap is outside R1")
            if (
                state.setmagicpet_overlay is not None
                and state.setmagicpet_overlay.runtime_by_participant_id[
                    pid
                ].prepared_powers is not None
            ):
                raise ValueError("Vary/SetMagicPet prepared-power overlap is outside R1")

        participants=tuple(
            replace(
                participant,
                attack=int(
                    working_vary.runtime_by_participant_id[
                        str(participant.participant_id)
                    ].attack_power
                ),
                defense=int(
                    working_vary.runtime_by_participant_id[
                        str(participant.participant_id)
                    ].defense_power
                ),
                quick=int(
                    working_vary.runtime_by_participant_id[
                        str(participant.participant_id)
                    ].quick
                ),
            )
            if str(participant.participant_id)
            in working_vary.runtime_by_participant_id
            else participant
            for participant in participants
        )

    effective_commands=dict(commands)
    for participant_id,carried in (
        state.carried_commands_by_participant_id.items()
    ):
        if participant_id in living_ids:
            effective_commands[participant_id]=carried

    effective_setup_effects={
        str(pid):effects
        for pid,effects in (
            command_setup_effects_by_participant_id or {}
        ).items()
    }
    effective_setup_effects.update({
        str(pid):effects
        for pid,effects in (
            state.carried_setup_effects_by_participant_id.items()
        )
        if pid in living_ids
    })
    for pid,vary in working_vary.runtime_by_participant_id.items():
        if pid not in living_ids:
            continue
        existing=effective_setup_effects.get(
            pid,BattleCommandSetupEffects()
        )
        if (
            existing.attack_power is not None
            and int(existing.attack_power)!=int(vary.attack_power)
        ) or (
            existing.defense_power is not None
            and int(existing.defense_power)!=int(vary.defense_power)
        ):
            raise ValueError("Vary callback setup overlaps another power write")
        effective_setup_effects[pid]=replace(
            existing,
            attack_power=int(vary.attack_power),
            defense_power=int(vary.defense_power),
        )

    for pid,submission in battletimid_submissions.items():
        existing=effective_setup_effects.get(
            pid,BattleCommandSetupEffects()
        )
        if (
            existing.attack_power is not None
            and int(existing.attack_power)!=int(
                submission.setup.attack_power
            )
        ) or (
            existing.defense_power is not None
            and int(existing.defense_power)!=int(
                submission.setup.defence_power
            )
        ):
            raise ValueError("BattleTimid callback setup overlaps power drift")
        effective_setup_effects[pid]=replace(
            existing,
            attack_power=int(submission.setup.attack_power),
            defense_power=int(submission.setup.defence_power),
        )

    for pid,submission in lighttakeed_submissions.items():
        existing=effective_setup_effects.get(
            pid,BattleCommandSetupEffects()
        )
        if (
            existing.attack_power is not None
            and int(existing.attack_power)!=int(submission.attack_power)
        ) or (
            existing.defense_power is not None
            and int(existing.defense_power)!=int(submission.defense_power)
        ):
            raise ValueError("Lighttakeed callback setup overlaps power drift")
        effective_setup_effects[pid]=replace(
            existing,
            attack_power=int(submission.attack_power),
            defense_power=int(submission.defense_power),
        )

    combined_action_overrides={}
    if combined_submissions:
        participant_by_id={
            str(participant.participant_id):participant
            for participant in participants
        }
        for pid in combined_submissions:
            initiative=resolve_combined_initiative(
                profile=state.combined_overlay.initiative_profile,
                work_quick=int(participant_by_id[pid].quick),
                random_subtract=int(initiative_random_subtracts[pid]),
            )
            combined_action_overrides[pid]=int(initiative.action_value)

    prepared = prepare_battle_round(
        participants,
        effective_commands,
        initiative_random_subtracts,
        tie_break_order=tie_break_order,
        action_value_overrides_by_participant_id=combined_action_overrides,
    )
    prepared = apply_base_combo_rewrite(
        prepared,
        profiles,
        combo_start_rolls_1_100,
        semantic_nonattack_ids=tuple(
            set(attack_crazed_submissions_by_participant_id or {})
            | set(wildviolent_submissions_by_participant_id or {})
            | set(modifyattack_submissions)
            | set(mdfyattack_submissions_by_participant_id or {})
            | set(weaken_submissions_by_participant_id or {})
            | set(refresh_submissions_by_participant_id or {})
            | set(setmagicpet_submissions_by_participant_id or {})
            | set(battletimid_submissions)
            | set(lighttakeed_submissions)
            | set(combined_submissions)
            | set(vary_submissions)
        ),
        base_status_runtime_by_participant_id=_freeze_mapping({
            participant_id:
                state.base_status_runtime_by_participant_id[participant_id]
            for participant_id in round_entry_ids
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
        abduct_contexts=abduct_contexts,
        abduct_rolls=abduct_rolls,
        steal_rolls=steal_rolls,
        steal_player_gold_by_participant_id=(
            steal_player_gold_by_participant_id
        ),
        steal_player_item_slots_by_participant_id=(
            steal_player_item_slots_by_participant_id
        ),
        escape_contexts=normalized_escape_contexts,
        escape_rolls=escape_rolls,
        counter_rolls_by_attack_id=counter_rolls_by_attack_id,
        counter_abio_by_participant_id=counter_abio_by_participant_id,
        battle_abio_by_participant_id=battle_abio_by_participant_id,
        ultimate_overkill_by_participant_id=_freeze_mapping({
            participant_id:
                state.ultimate_overkill_by_participant_id[participant_id]
            for participant_id in round_entry_ids
        }),
        combo_rolls_by_starter_id=combo_rolls_by_starter_id,
        continuation_rolls_by_attack_id=continuation_rolls_by_attack_id,
        modifyattack_submissions_by_participant_id=modifyattack_submissions,
        modifyattack_rand_by_participant_id=modifyattack_rand_by_participant_id,
        mdfyattack_submissions_by_participant_id=mdfyattack_submissions_by_participant_id,
        attack_crazed_submissions_by_participant_id=attack_crazed_submissions_by_participant_id,
        attack_crazed_rolls_by_attack_id=attack_crazed_rolls_by_attack_id,
        wildviolent_submissions_by_participant_id=wildviolent_submissions_by_participant_id,
        wildviolent_rolls_by_attack_id=wildviolent_rolls_by_attack_id,
        base_status_runtime_by_participant_id=_freeze_mapping({
            participant_id:
                state.base_status_runtime_by_participant_id[participant_id]
            for participant_id in round_entry_ids
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
        command_setup_effects_by_participant_id=effective_setup_effects,
        base_damage_react_state_by_participant_id=_freeze_mapping({
            participant_id:
                state.base_damage_react_state_by_participant_id[participant_id]
            for participant_id in round_entry_ids
        }),
        ride_pet_runtime=state.ride_pet_runtime,
        attack_magic_runtime=attack_magic_runtime,
        attack_magic_submissions_by_participant_id=(
            attack_magic_submissions_by_participant_id
        ),
        attack_magic_rolls_by_participant_id=(
            attack_magic_rolls_by_participant_id
        ),
        attack_magic_overlay=attack_magic_overlay,
        attack_magic_retarget_rolls_by_participant_id=(
            attack_magic_retarget_rolls_by_participant_id
        ),
        enemy_rehp_submissions_by_participant_id=(
            enemy_rehp_submissions_by_participant_id
        ),
        enemy_rehp_rolls_by_participant_id=(
            enemy_rehp_rolls_by_participant_id
        ),
        enemy_rehp_retarget_rolls_by_participant_id=(
            enemy_rehp_retarget_rolls_by_participant_id
        ),
        enemy_relife_submissions_by_participant_id=(
            enemy_relife_submissions_by_participant_id
        ),
        enemy_relife_rolls_by_participant_id=(
            enemy_relife_rolls_by_participant_id
        ),
        enemy_relife_retarget_rolls_by_participant_id=(
            enemy_relife_retarget_rolls_by_participant_id
        ),
        revivable_dead_participant_ids=(
            state.revivable_dead_participant_ids
        ),
        passive_battle_entries_by_slot=passive_battle_entries_by_slot,
        damage_to_hp_submissions_by_participant_id=(
            damage_to_hp_submissions_by_participant_id
        ),
        mp_damage_submissions_by_participant_id=(
            mp_damage_submissions_by_participant_id
        ),
        mp_by_participant_id=mp_by_participant_id,
        battle_tear_submissions_by_participant_id=(
            battle_tear_submissions_by_participant_id
        ),
        guard_break2_submissions_by_participant_id=(
            guard_break2_submissions_by_participant_id
        ),
        battletimid_submissions_by_participant_id=battletimid_submissions,
        battletimid_rolls_by_participant_id=(
            battletimid_rolls_by_participant_id
        ),
        lighttakeed_submissions_by_participant_id=lighttakeed_submissions,
        combined_submissions_by_participant_id=combined_submissions,
        combined_rolls_by_participant_id=(
            combined_rolls_by_participant_id
        ),
        combined_overlay=state.combined_overlay,
        vary_submissions_by_participant_id=vary_submissions,
        fall_ground_submissions_by_participant_id=(
            fall_ground_submissions_by_participant_id
        ),
        fall_ground_rolls_by_participant_id=(
            fall_ground_rolls_by_participant_id
        ),
        fall_ground_equipment_resistance_by_participant_id=(
            fall_ground_equipment_resistance_by_participant_id
        ),
        nocast_submissions_by_participant_id=(
            nocast_submissions_by_participant_id
        ),
        nocast_rolls_by_participant_id=(
            nocast_rolls_by_participant_id
        ),
        weaken_submissions_by_participant_id=weaken_submissions_by_participant_id,
        weaken_rolls_by_participant_id=weaken_rolls_by_participant_id,
        refresh_submissions_by_participant_id=refresh_submissions_by_participant_id,
        refresh_rolls_by_participant_id=refresh_rolls_by_participant_id,
        setmagicpet_submissions_by_participant_id=(
            setmagicpet_submissions_by_participant_id
        ),
        setmagicpet_rolls_by_participant_id=(
            setmagicpet_rolls_by_participant_id
        ),
        barrier_submissions_by_participant_id=(
            barrier_submissions_by_participant_id
        ),
        barrier_rolls_by_participant_id=(
            barrier_rolls_by_participant_id
        ),
        nocast_overlay=state.nocast_overlay,
        setmagicpet_overlay=state.setmagicpet_overlay,
        ride_pet_source_slot=(
            None
            if state.session.ride_pet is None
            else state.session.ride_pet.source_pet_slot
        ),
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
    player_id=str(state.session.player.participant_id)
    allied_pet_ids={
        str(pet.participant_id) for pet in state.session.allied_pets
    }
    known_ids={player_id}|allied_pet_ids|enemy_ids
    participant_id_by_slot={
        int(slot):str(pid) for pid,slot in state.slots.items()
    }
    captured_enemy_ids=set()
    for event in round_result.events:
        if (
            event.capture_resolution is None
            or not event.capture_resolution.success
        ):
            continue
        if event.resolved_target_slot is None:
            raise ValueError("successful capture lacks resolved target slot")
        target_id=participant_id_by_slot.get(int(event.resolved_target_slot))
        if target_id is None or target_id not in enemy_ids:
            raise ValueError("successful capture target is not an enemy entry")
        captured_enemy_ids.add(target_id)
    if not captured_enemy_ids.issubset(exited_ids):
        raise ValueError("capture exit missing from ordinary exited IDs")
    battletimid_exit_ids=set()
    for event in round_result.events:
        resolution=event.battletimid_resolution
        if resolution is None or not resolution.forced_exit:
            continue
        if event.resolved_target_slot is None:
            raise ValueError("BattleTimid forced exit lacks target slot")
        target_id=participant_id_by_slot.get(
            int(event.resolved_target_slot)
        )
        if target_id is None:
            raise ValueError("BattleTimid forced exit targets unknown slot")
        if resolution.player_battle_exit and target_id != player_id:
            raise ValueError("BattleTimid player-exit target identity drift")
        if (
            resolution.pet_default_exit
            and target_id not in allied_pet_ids
        ):
            raise ValueError("BattleTimid pet-exit target identity drift")
        battletimid_exit_ids.add(target_id)
    if not battletimid_exit_ids.issubset(exited_ids):
        raise ValueError("BattleTimid exit missing from ordinary exited IDs")
    battle_exit_ids=exited_ids-captured_enemy_ids
    allowed_battle_exit_ids=(
        allied_pet_ids | enemy_ids | battletimid_exit_ids
    )
    invalid_exits=sorted(battle_exit_ids-allowed_battle_exit_ids)
    if invalid_exits:
        raise ValueError(
            "ordinary non-capture battle exit lacks admitted provenance: "
            f"{invalid_exits}"
        )
    if (
        player_id in battle_exit_ids
        and player_id not in battletimid_exit_ids
    ):
        raise ValueError(
            "player ordinary battle exit requires BattleTimid provenance"
        )

    escaped_ids={str(pid) for pid in round_result.escaped_participant_ids}
    ultimate_exited_ids={
        str(pid) for pid in round_result.ultimate_exited_participant_ids
    }
    invalid_ultimate_exits=sorted(ultimate_exited_ids-known_ids)
    if invalid_ultimate_exits:
        raise ValueError(
            "ordinary round ultimate-exited unknown entries: "
            f"{invalid_ultimate_exits}"
        )
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
    # BATTLE_Exit resets the entry escape counter for every exiting non-pet.
    for pid in ultimate_exited_ids | battle_exit_ids:
        if pid in escape_counts:
            escape_counts[pid]=0

    escaped_enemy_ids=escaped_ids & enemy_ids
    removed_enemy_ids=captured_enemy_ids | escaped_enemy_ids
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
    next_ultimate_exited=list(state.ultimate_exited_participant_ids)
    for pid in round_result.ultimate_exited_participant_ids:
        pid=str(pid)
        if pid not in next_ultimate_exited:
            next_ultimate_exited.append(pid)
    next_battle_exited=list(state.battle_exited_participant_ids)
    for pid in sorted(battle_exit_ids):
        if pid not in next_battle_exited:
            next_battle_exited.append(pid)
    for pid in removed_enemy_ids:
        next_slots.pop(pid,None)
        hp.pop(pid,None)
        escape_counts.pop(pid,None)
        next_status_runtime.pop(pid,None)
        next_damage_react.pop(pid,None)
        next_ultimate_overkill.pop(pid,None)
        if pid in next_ultimate_exited:
            next_ultimate_exited.remove(pid)
        if pid in next_battle_exited:
            next_battle_exited.remove(pid)

    next_revivable=set(state.revivable_dead_participant_ids)
    for event in round_result.events:
        if (
            event.target_hp_before is not None
            and event.target_hp_after is not None
            and int(event.target_hp_before) > 0
            and int(event.target_hp_after) == 0
            and event.resolved_target_slot is not None
        ):
            target_id=participant_id_by_slot.get(
                int(event.resolved_target_slot)
            )
            if (
                target_id is not None
                and target_id in enemy_ids
            ):
                next_revivable.add(target_id)
        if (
            event.enemy_relife_resolution is not None
            and event.enemy_relife_resolution.success
            and event.enemy_relife_resolution.selected_participant_id
            is not None
        ):
            next_revivable.discard(
                str(
                    event.enemy_relife_resolution.selected_participant_id
                )
            )
    invalid_revivable_ids=(
        set(next_ultimate_exited)
        | set(next_battle_exited)
        | set(removed_enemy_ids)
    )
    next_revivable={
        pid for pid in next_revivable
        if (
            pid in hp
            and int(hp[pid]) == 0
            and pid not in invalid_revivable_ids
        )
    }

    next_nocast_overlay=round_result.nocast_overlay
    if next_nocast_overlay is not None:
        next_session_ids={
            str(participant.participant_id)
            for participant in _session_participants(next_session)
        }
        next_nocast_overlay=NocastRoundOverlay({
            participant_id:runtime
            for participant_id,runtime in (
                next_nocast_overlay.runtime_by_participant_id.items()
            )
            if participant_id in next_session_ids
        })

    next_setmagicpet_overlay=round_result.setmagicpet_overlay
    if next_setmagicpet_overlay is not None:
        next_session_ids={
            str(participant.participant_id)
            for participant in _session_participants(next_session)
        }
        next_setmagicpet_overlay=SetMagicPetRoundOverlay({
            participant_id:runtime
            for participant_id,runtime in (
                next_setmagicpet_overlay.runtime_by_participant_id.items()
            )
            if participant_id in next_session_ids
        })

    next_combined_overlay=round_result.combined_overlay
    if next_combined_overlay is not None:
        next_session_ids={
            str(participant.participant_id)
            for participant in _session_participants(next_session)
        }
        next_combined_overlay=CombinedRuntimeOverlay(
            next_combined_overlay.initiative_profile,
            next_combined_overlay.status_magic_profile,
            next_combined_overlay.item_zero,
            {
                participant_id:value
                for participant_id,value in (
                    next_combined_overlay.mp_by_participant_id.items()
                )
                if participant_id in next_session_ids
            },
            {
                participant_id:value
                for participant_id,value in (
                    next_combined_overlay.att_reverse_by_participant_id.items()
                )
                if participant_id in next_session_ids
            },
        )

    next_vary_overlay=working_vary
    auxiliary_vary_results={
        "status_tick","setmagicpet_tick","weaken_tick","barrier_tick",
        "nocast_tick","skipped_incomplete","skipped_dead","skipped_exited",
    }
    for pid in tuple(next_vary_overlay.runtime_by_participant_id):
        completed=any(
            str(event.participant_id)==pid
            and str(event.result) not in auxiliary_vary_results
            for event in round_result.events
        )
        if completed:
            next_vary_overlay,_=next_vary_overlay.advance_actor_action(pid)
    next_vary_overlay=next_vary_overlay.retain_participants(
        {
            str(participant.participant_id)
            for participant in _session_participants(next_session)
            if (
                str(participant.participant_id) not in next_battle_exited
                and str(participant.participant_id) not in next_ultimate_exited
            )
        }
    )

    # Source BATTLE_PreCommandSeq runs exactly once after BATTLE_Battling.
    # It visits valid entries (including zero-HP entries), except EARTHROUND0.
    # This is not another StatusSeq visit and is not repeated on next call.
    baseline=_participant_map(next_session)
    if next_setmagicpet_overlay is not None:
        prepared_magic={}
        for pid,magic in (
            next_setmagicpet_overlay.runtime_by_participant_id.items()
        ):
            carried=(
                round_result.carried_commands_by_participant_id or {}
            ).get(pid)
            if (
                pid in next_battle_exited
                or pid in next_ultimate_exited
                or (
                    carried is not None
                    and carried.command1==BATTLE_COM_S_EARTHROUND0
                )
            ):
                prepared_magic[pid]=magic
                continue
            active=magic.state.tgh_turn>0
            was_prepared=magic.prepared_powers is not None
            if active or was_prepared:
                if (
                    state.ride_pet_runtime is not None
                    or next_status_runtime[pid].status.drunk>0
                ):
                    raise ValueError(
                        "SetMagicPet preparation with riding/drunk modifiers "
                        "is outside the admitted domain"
                    )
                actor=baseline[pid]
                powers=(
                    prepare_setmagicpet_powers(
                        baseline_attack=actor.attack,
                        baseline_defense=actor.defense,
                        baseline_quick=actor.quick,
                        runtime=magic,
                    )
                    if active
                    else None
                )
                magic=replace(magic,prepared_powers=powers)
            prepared_magic[pid]=magic
        next_setmagicpet_overlay=SetMagicPetRoundOverlay(prepared_magic)

    if next_nocast_overlay is not None:
        prepared_late={}
        for pid,late in next_nocast_overlay.runtime_by_participant_id.items():
            carried=(round_result.carried_commands_by_participant_id or {}).get(pid)
            if (pid in next_battle_exited or pid in next_ultimate_exited
                or (carried is not None and carried.command1==BATTLE_COM_S_EARTHROUND0)):
                prepared_late[pid]=late
                continue
            actor=baseline[pid]
            was_weakened=late.prepared_weaken_powers is not None
            active_weaken=late.weaken_counter>0
            if active_weaken or was_weakened:
                if state.ride_pet_runtime is not None or next_status_runtime[pid].status.drunk>0:
                    raise ValueError("Weaken preparation with riding/drunk modifiers is outside the admitted domain")
                magic_powers=(
                    None
                    if next_setmagicpet_overlay is None
                    else next_setmagicpet_overlay.runtime_by_participant_id[
                        pid
                    ].prepared_powers
                )
                base_attack=(
                    actor.attack
                    if magic_powers is None
                    else magic_powers.attack
                )
                base_defense=(
                    actor.defense
                    if magic_powers is None
                    else magic_powers.defense
                )
                base_quick=(
                    actor.quick
                    if magic_powers is None
                    else magic_powers.dexterity
                )
                recalculated=resolve_weaken_recalculation(
                    base_attack,base_defense,base_quick,
                    weaken_counter=late.weaken_counter,
                    barrier_counter=late.barrier_counter,
                )
                powers=(PreparedWeakenPowers(recalculated.strength,recalculated.toughness,recalculated.dexterity)
                        if active_weaken else None)
                late=replace(late, weaken_counter=recalculated.weaken_counter,
                             barrier_counter=recalculated.barrier_counter, prepared_weaken_powers=powers)
                next_status_runtime[pid]=replace(next_status_runtime[pid],work_quick=recalculated.dexterity)
            elif late.barrier_counter>0:
                late=replace(late,barrier_counter=late.barrier_counter-1)
            prepared_late[pid]=late
        next_nocast_overlay=NocastRoundOverlay(prepared_late)

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
        carried_commands_by_participant_id=_freeze_mapping({
            pid:command
            for pid,command in (
                round_result.carried_commands_by_participant_id or {}
            ).items()
            if (
                pid in next_slots
                and pid not in next_battle_exited
                and pid not in next_ultimate_exited
            )
        }),
        carried_setup_effects_by_participant_id=_freeze_mapping({
            pid:effects
            for pid,effects in (
                round_result.carried_setup_effects_by_participant_id or {}
            ).items()
            if (
                pid in next_slots
                and pid not in next_battle_exited
                and pid not in next_ultimate_exited
            )
        }),
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
        ultimate_exited_participant_ids=tuple(next_ultimate_exited),
        battle_exited_participant_ids=tuple(next_battle_exited),
        revivable_dead_participant_ids=tuple(sorted(next_revivable)),
        nocast_overlay=next_nocast_overlay,
        setmagicpet_overlay=next_setmagicpet_overlay,
        combined_overlay=next_combined_overlay,
        vary_overlay=next_vary_overlay,
    )
    if player_id in escaped_ids:
        next_state=replace(
            next_state,
            phase=FINISHED,
            result=PLAYER_ESCAPE,
            winning_side=None,
            vary_overlay=None,
        )
    else:
        next_state = _with_termination(next_state)
    return PersistentRoundResult(
        before=state,
        round=round_result,
        after=next_state,
        attack_magic_overlay_before=attack_magic_overlay,
        attack_magic_overlay_after=round_result.attack_magic_overlay,
    )
