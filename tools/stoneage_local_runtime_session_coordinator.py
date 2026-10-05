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

from dataclasses import dataclass, field, replace
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from tools.stoneage_enemy_spawn_model import (
    EnemyBirthRolls,
    SpawnedEnemy,
)
from tools.stoneage_attack_magic_action_model import EnemyAttackMagicActionRolls
from tools.stoneage_attack_magic_state_model import AttackMagicRoundOverlay
from tools.stoneage_enemy_ai_attack_magic_bridge import (
    ATTACK_MAGIC_CALLBACK,
    EnemyAiAttackMagicSubmission,
    resolve_enemy_ai_attack_magic_submission,
)
from tools.stoneage_enemy_ai_rehp_bridge import (
    EnemyAiReHpSubmission,
    resolve_enemy_ai_rehp_submission,
)
from tools.stoneage_enemy_ai_relife_bridge import (
    EnemyAiReLifeSubmission,
    resolve_enemy_ai_relife_submission,
)
from tools.stoneage_enemy_ai_damage_to_hp_bridge import (
    EnemyAiDamageToHpSubmission,
    resolve_enemy_ai_damage_to_hp_submission,
)
from tools.stoneage_enemy_ai_mp_damage_bridge import (
    EnemyAiMpDamageSubmission,
    resolve_enemy_ai_mp_damage_submission,
)
from tools.stoneage_enemy_ai_fall_ground_bridge import (
    EnemyAiFallGroundSubmission,
    resolve_enemy_ai_fall_ground_submission,
)
from tools.stoneage_enemy_ai_battle_tear_bridge import (
    EnemyAiBattleTearSubmission,
    resolve_enemy_ai_battle_tear_submission,
)
from tools.stoneage_enemy_ai_nocast_bridge import (
    EnemyAiNocastSubmission,
    resolve_enemy_ai_nocast_submission,
)
from tools.stoneage_enemy_ai_barrier_bridge import (
    EnemyAiBarrierSubmission,
    resolve_enemy_ai_barrier_submission,
)
from tools.stoneage_enemy_ai_guard_break2_bridge import (
    EnemyAiGuardBreak2Submission,
    resolve_enemy_ai_guard_break2_submission,
)
from tools.stoneage_enemy_ai_battletimid_bridge import (
    EnemyAiBattleTimidSubmission,
    resolve_enemy_ai_battletimid_submission,
)
from tools.stoneage_enemy_ai_lighttakeed_bridge import (
    CALLBACK_NAME as LIGHTTAKEED_CALLBACK,
    EnemyAiLighttakeedSubmission,
    resolve_enemy_ai_lighttakeed_submission,
)
from tools.stoneage_battletimid_model import (
    CALLBACK_NAME as BATTLETIMID_CALLBACK,
)
from tools.stoneage_enemy_ai_combined_bridge import (
    EnemyAiCombinedSubmission,
    resolve_enemy_ai_combined_submission,
)
from tools.stoneage_combined_model import CALLBACK_NAME as COMBINED_CALLBACK
from tools.stoneage_enemy_ai_vary_bridge import (
    EnemyAiVarySubmission,
    resolve_enemy_ai_vary_submission,
)
from tools.stoneage_vary_runtime_state import CALLBACK_NAME as VARY_CALLBACK
from tools.stoneage_combined_runtime_state import (
    CombinedActionRolls,
    CombinedRuntimeOverlay,
)
from tools.stoneage_guard_break2_model import (
    CALLBACK_NAME as GUARD_BREAK2_CALLBACK,
)
from tools.stoneage_nocast_model import CALLBACK_NAME as NOCAST_CALLBACK
from tools.stoneage_barrier_model import CALLBACK_NAME as BARRIER_CALLBACK
from tools.stoneage_barrier_runtime_state import BarrierActionRolls
from tools.stoneage_enemy_ai_weaken_bridge import EnemyAiWeakenSubmission, resolve_enemy_ai_weaken_submission
from tools.stoneage_weaken_runtime_state import WeakenActionRolls
from tools.stoneage_weaken_model import CALLBACK_NAME as WEAKEN_CALLBACK
from tools.stoneage_enemy_ai_refresh_bridge import (
    EnemyAiRefreshSubmission,
    resolve_enemy_ai_refresh_submission,
)
from tools.stoneage_refresh_runtime_state import RefreshActionRolls
from tools.stoneage_refresh_model import CALLBACK_NAME as REFRESH_CALLBACK
from tools.stoneage_enemy_ai_setmagicpet_bridge import (
    EnemyAiSetMagicPetSubmission,
    resolve_enemy_ai_setmagicpet_submission,
)
from tools.stoneage_setmagicpet_runtime_state import (
    SetMagicPetActionRolls,
    SetMagicPetRoundOverlay,
)
from tools.stoneage_setmagicpet_model import (
    CALLBACK_NAME as SETMAGICPET_CALLBACK,
)
from tools.stoneage_nocast_runtime_state import (
    NocastActionRolls,
    NocastRoundOverlay,
)
from tools.stoneage_fall_ground_model import (
    CALLBACK_NAME as FALL_GROUND_CALLBACK,
)
from tools.stoneage_battle_tear_damage_model import (
    CALLBACK_NAME as BATTLE_TEAR_CALLBACK,
)
from tools.stoneage_mp_damage_model import CALLBACK_NAME as MP_DAMAGE_CALLBACK
from tools.stoneage_damage_to_hp_model import (
    CALLBACK_NAME as DAMAGE_TO_HP_CALLBACK,
)
from tools.stoneage_enemy_rehp_model import (
    CALLBACK_NAME as ENEMY_REHP_CALLBACK,
    EnemyReHpRolls,
)
from tools.stoneage_enemy_relife_model import (
    CALLBACK_NAME as ENEMY_RELIFE_CALLBACK,
    EnemyReLifeRolls,
)
from tools.stoneage_enemy_ai_petskill_bridge import (
    resolve_enemy_ai_supported_petskill_command,
)
from tools.stoneage_enemy_ai_model import (
    ATTACK as ENEMY_AI_ATTACK,
    ESCAPE as ENEMY_AI_ESCAPE,
    GUARD as ENEMY_AI_GUARD,
    SKILL as ENEMY_AI_SKILL,
    EnemyAiTarget,
    resolve_common_normal_enemy_ai,
)
from tools.stoneage_enemy_ai_attack_crazed_bridge import (
    EnemyAiAttackCrazedSubmission, resolve_enemy_ai_attack_crazed_submission,
)
from tools.stoneage_attack_crazed_model import CALLBACK_NAME as ATTACK_CRAZED_CALLBACK
from tools.stoneage_enemy_ai_wildviolent_bridge import (
    EnemyAiWildViolentSubmission,
    resolve_enemy_ai_wildviolent_submission,
)
from tools.stoneage_wildviolent_model import CALLBACK_NAME as WILDVIOLENT_CALLBACK
from tools.stoneage_enemy_ai_modifyattack_bridge import (
    EnemyAiModifyAttackSubmission, resolve_enemy_ai_modifyattack_submission,
)
from tools.stoneage_enemy_ai_mdfyattack_bridge import EnemyAiMdfyAttackSubmission, resolve_enemy_ai_mdfyattack_submission
from tools.stoneage_mdfyattack_model import CALLBACK_NAME as MDFYATTACK_CALLBACK
from tools.stoneage_battle_round_model import (
    AttackCrazedRolls,
    WildViolentRolls,
    BATTLE_COM_ATTACK,
    BATTLE_COM_CAPTURE,
    BATTLE_COM_ESCAPE,
    BATTLE_COM_GUARD,
    BATTLE_COM_S_CHARGE,
    BATTLE_COM_S_EARTHROUND0,
    BATTLE_COM_S_RENZOKU,
    BATTLE_COM_S_STATUSCHANGE,
    BATTLE_COM_S_ABDUCT,
    BATTLE_COM_S_STEAL,
    BATTLE_COM_S_ATTACK_MAGIC,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
    BattleCommandSetupEffects,
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
)
from tools.stoneage_battle_status_model import (
    BaseStatusCombatProfile,
    BaseStatusTurnRolls,
)
from tools.stoneage_battle_state_model import (
    PersistentBattleState,
    PersistentRoundResult,
    begin_persistent_battle,
    participant_snapshot,
    resolve_persistent_ordinary_round,
)
from tools.stoneage_encounter_frequency_model import (
    EncounterFrequencyDecision,
    EncounterFrequencyState,
    refresh_frequency_bounds,
    resolve_frequency_step,
)
from tools.stoneage_map_collision_model import (
    CollisionDecision,
    DynamicOccupant,
)
from tools.stoneage_player_death_model import (
    death_transition,
    resurrect_transition,
)
from tools.stoneage_runtime_dynamic_occupancy import (
    resolve_runtime_collision_with_occupancy,
)
from tools.stoneage_runtime_occupancy_registry import (
    RuntimeDynamicOccupancyRegistry,
)
from tools.stoneage_local_runtime_core import (
    LOCAL_SESSION_SCHEMA,
    LocalPersistenceStore,
    LocalRuntimeSessionState,
    MaterializedWorldRegion,
    TransitionGateDecision,
    decode_local_runtime_session,
)
from tools.stoneage_local_runtime_save import (
    LOCAL_RUNTIME_SAVE_SCHEMA,
    LocalRuntimeSaveSnapshot,
    build_initial_occupancy_registry,
    build_local_runtime_occupancy_delta,
    decode_local_runtime_save,
    encode_local_runtime_save,
    local_runtime_payload_schema,
    restore_local_runtime_occupancy_registry,
)
from tools.stoneage_singleplayer_battle import (
    BattleOutcome,
    BattleSession,
    apply_battle_outcome,
    begin_group_battle,
)
from tools.stoneage_singleplayer_domain import (
    EncounterRequest,
    EncounterRolls,
    GroupEncounterRequest,
    MapPosition,
    PetActor,
    SinglePlayerHistoricalDomain,
)
from tools.stoneage_singleplayer_runtime import (
    SinglePlayerHistoricalRuntime,
)
from tools.stoneage_singleplayer_persistence import (
    decode_persistent_state,
    encode_persistent_state,
)
from tools.stoneage_singleplayer_world import (
    WalkResolution,
    place_player_on_topology,
    resolve_player_walk,
)
from tools.stoneage_tw10_25_encounter_bridge import (
    active_encounter_area,
)


@dataclass(frozen=True)
class LocalRuntimeWalkResult:
    session: LocalRuntimeSessionState
    resolution: WalkResolution
    collision: CollisionDecision | None = None
    collision_provider_kind: str | None = None
    collision_evidence_class: str | None = None
    collision_semantic_profile: str | None = None
    collision_exact_binary_proof: bool | None = None
    static_collision: CollisionDecision | None = None
    dynamic_collision: CollisionDecision | None = None
    dynamic_occupancy_profile: str | None = None
    dynamic_occupancy_evidence_class: str | None = None
    live_occupancy_registry_profile: str | None = None
    live_occupancy_object_ids: tuple[str, ...] = ()
    live_occupancy_provenance: tuple[str, ...] = ()


@dataclass(frozen=True)
class LocalRuntimeEncounterWalkResult:
    """One ordinary movement result plus descendant CEP/encounter resolution."""

    walk: LocalRuntimeWalkResult
    frequency: EncounterFrequencyDecision | None
    group_encounter: GroupEncounterRequest | None = None
    encounter: EncounterRequest | None = None

    @property
    def session(self) -> LocalRuntimeSessionState:
        return self.walk.session


@dataclass(frozen=True)
class LocalRuntimeBattleContext:
    """Transient local battle shell over a cloned persistent-state snapshot."""

    contract_id: str
    world_profile: str
    hometown_ordinal: int
    origin_position: MapPosition
    world_flags: frozenset[str]
    persistent_state_payload: str
    battle: BattleSession
    spawned_enemies: tuple[SpawnedEnemy, ...]
    persistent_battle_state: PersistentBattleState | None = None
    working_persistent_state_payload: str | None = None
    attack_magic_overlay: AttackMagicRoundOverlay | None = None

    def __post_init__(self) -> None:
        if not str(self.contract_id).strip():
            raise ValueError("battle context contract_id must be non-empty")
        if not str(self.world_profile).strip():
            raise ValueError("battle context world_profile must be non-empty")
        if int(self.hometown_ordinal) not in {1, 2, 3, 4}:
            raise ValueError("battle context hometown ordinal must be 1..4")
        if self.battle.origin_position != self.origin_position:
            raise ValueError("battle context origin/battle position drift")
        object.__setattr__(
            self,
            "world_flags",
            frozenset(str(x) for x in self.world_flags),
        )
        object.__setattr__(
            self,
            "spawned_enemies",
            tuple(self.spawned_enemies),
        )
        if self.persistent_battle_state is not None:
            if (
                self.persistent_battle_state.session.origin_position
                != self.origin_position
            ):
                raise ValueError("persistent battle origin drift")
            if (
                self.persistent_battle_state.session.player.participant_id
                != self.battle.player.participant_id
            ):
                raise ValueError("persistent battle player identity drift")
        if self.working_persistent_state_payload is not None:
            if not str(self.working_persistent_state_payload).strip():
                raise ValueError("working persistent payload must be non-empty")
        if (
            self.attack_magic_overlay is not None
            and not isinstance(self.attack_magic_overlay,AttackMagicRoundOverlay)
        ):
            raise TypeError("battle context AttackMagic overlay has wrong type")


@dataclass(frozen=True)
class LocalRuntimePlayerDeathPlan:
    """Explicit core_Dying plan; world drop/party actions remain external."""

    session: LocalRuntimeSessionState
    party_discharged: bool
    item_drop_mode: str
    requested_item_drop_slots: tuple[int, ...]
    random_item_drop_candidates: tuple[int, ...]
    random_item_drop_count: int
    requested_ground_gold: int
    final_carried_gold: int
    dead_count_after: int
    cleared_statuses: tuple[str, ...]
    is_dead: bool
    is_attacked: bool


@dataclass(frozen=True)
class LocalRuntimePlayerResurrectionResult:
    """In-place CHAR_playerresurrect projection without warp or MP refill."""

    session: LocalRuntimeSessionState
    base_image_restored: bool
    is_dead: bool
    is_attacked: bool
    is_overed: bool
    mp_unchanged: bool
    location_unchanged: bool


@dataclass(frozen=True)
class LocalRuntimeTransitionResult:
    session: LocalRuntimeSessionState
    decision: TransitionGateDecision


@dataclass(frozen=True)
class LocalRuntimeInteraction:
    """Presentation-safe view of one spatially available recovered interaction."""

    transition_id: str
    interaction_kind: str
    allowed: bool
    reason: str
    provenance: Mapping[str, Any]
    execution_supported: bool

    def __post_init__(self) -> None:
        transition_id = str(self.transition_id).strip()
        interaction_kind = str(self.interaction_kind).strip()
        reason = str(self.reason).strip()
        if not transition_id:
            raise ValueError("runtime interaction transition_id must be non-empty")
        if not interaction_kind:
            raise ValueError("runtime interaction kind must be non-empty")
        if not reason:
            raise ValueError("runtime interaction reason must be non-empty")
        object.__setattr__(self, "transition_id", transition_id)
        object.__setattr__(self, "interaction_kind", interaction_kind)
        object.__setattr__(self, "allowed", bool(self.allowed))
        object.__setattr__(self, "reason", reason)
        object.__setattr__(
            self,
            "provenance",
            MappingProxyType(dict(self.provenance)),
        )
        object.__setattr__(
            self,
            "execution_supported",
            bool(self.execution_supported),
        )


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


@dataclass(frozen=True)
class EnemyAiCommonCommandBatch:
    commands: Mapping[str, BattleCommand]
    setup_effects: Mapping[str, BattleCommandSetupEffects]
    abduct_contexts: Mapping[str, OrdinaryAbductContext] = field(
        default_factory=dict
    )
    attack_magic_submissions: Mapping[
        str,EnemyAiAttackMagicSubmission
    ] = field(default_factory=dict)
    enemy_rehp_submissions: Mapping[
        str,EnemyAiReHpSubmission
    ] = field(default_factory=dict)
    enemy_relife_submissions: Mapping[
        str,EnemyAiReLifeSubmission
    ] = field(default_factory=dict)
    damage_to_hp_submissions: Mapping[
        str,EnemyAiDamageToHpSubmission
    ] = field(default_factory=dict)
    mp_damage_submissions: Mapping[
        str,EnemyAiMpDamageSubmission
    ] = field(default_factory=dict)
    fall_ground_submissions: Mapping[
        str,EnemyAiFallGroundSubmission
    ] = field(default_factory=dict)
    battle_tear_submissions: Mapping[
        str,EnemyAiBattleTearSubmission
    ] = field(default_factory=dict)
    nocast_submissions: Mapping[
        str,EnemyAiNocastSubmission
    ] = field(default_factory=dict)
    guard_break2_submissions: Mapping[
        str,EnemyAiGuardBreak2Submission
    ] = field(default_factory=dict)
    battletimid_submissions: Mapping[
        str,EnemyAiBattleTimidSubmission
    ] = field(default_factory=dict)
    lighttakeed_submissions: Mapping[
        str,EnemyAiLighttakeedSubmission
    ] = field(default_factory=dict)
    combined_submissions: Mapping[
        str,EnemyAiCombinedSubmission
    ] = field(default_factory=dict)
    vary_submissions: Mapping[
        str,EnemyAiVarySubmission
    ] = field(default_factory=dict)
    barrier_submissions: Mapping[
        str,EnemyAiBarrierSubmission
    ] = field(default_factory=dict)
    weaken_submissions: Mapping[str,EnemyAiWeakenSubmission] = field(default_factory=dict)
    refresh_submissions: Mapping[str,EnemyAiRefreshSubmission] = field(default_factory=dict)
    setmagicpet_submissions: Mapping[
        str,EnemyAiSetMagicPetSubmission
    ] = field(default_factory=dict)
    modifyattack_submissions: Mapping[str,EnemyAiModifyAttackSubmission] = field(default_factory=dict)
    mdfyattack_submissions: Mapping[str,EnemyAiMdfyAttackSubmission] = field(default_factory=dict)
    attack_crazed_submissions: Mapping[str,EnemyAiAttackCrazedSubmission] = field(default_factory=dict)
    wildviolent_submissions: Mapping[str,EnemyAiWildViolentSubmission] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "commands",
            MappingProxyType({
                str(key): value for key, value in self.commands.items()
            }),
        )
        object.__setattr__(
            self,
            "setup_effects",
            MappingProxyType({
                str(key): value for key, value in self.setup_effects.items()
            }),
        )
        unknown = sorted(set(self.setup_effects) - set(self.commands))
        if unknown:
            raise ValueError(
                "enemy AI setup effects lack matching command actors: "
                + ",".join(unknown)
            )
        contexts={
            str(key):value for key,value in self.abduct_contexts.items()
        }
        object.__setattr__(
            self,
            "abduct_contexts",
            MappingProxyType(contexts),
        )
        abduct_command_ids={
            str(pid) for pid,command in self.commands.items()
            if int(command.command1)==BATTLE_COM_S_ABDUCT
        }
        if set(contexts) != abduct_command_ids:
            raise ValueError(
                "enemy AI Abduct contexts must match exactly S_ABDUCT actors"
            )
        if any(
            not isinstance(value,OrdinaryAbductContext)
            for value in contexts.values()
        ):
            raise TypeError("enemy AI Abduct context has wrong type")
        magic_submissions={
            str(key):value
            for key,value in self.attack_magic_submissions.items()
        }
        object.__setattr__(
            self,
            "attack_magic_submissions",
            MappingProxyType(magic_submissions),
        )
        magic_command_ids={
            str(pid) for pid,command in self.commands.items()
            if int(command.command1)==BATTLE_COM_S_ATTACK_MAGIC
        }
        if set(magic_submissions) != magic_command_ids:
            raise ValueError(
                "enemy AI AttackMagic submissions must match exactly "
                "command-2002 actors"
            )
        for participant_id,submission in magic_submissions.items():
            if not isinstance(submission,EnemyAiAttackMagicSubmission):
                raise TypeError(
                    f"enemy AI AttackMagic submission has wrong type for "
                    f"{participant_id}"
                )
            if str(submission.participant_id) != participant_id:
                raise ValueError(
                    "enemy AI AttackMagic submission participant drift"
                )

        rehp_submissions={
            str(key):value
            for key,value in self.enemy_rehp_submissions.items()
        }
        object.__setattr__(
            self,
            "enemy_rehp_submissions",
            MappingProxyType(rehp_submissions),
        )
        for participant_id,submission in rehp_submissions.items():
            if participant_id not in self.commands:
                raise ValueError(
                    "enemy AI ReHP submission lacks ordering carrier command"
                )
            if not isinstance(submission,EnemyAiReHpSubmission):
                raise TypeError(
                    f"enemy AI ReHP submission has wrong type for {participant_id}"
                )
            if str(submission.participant_id) != participant_id:
                raise ValueError("enemy AI ReHP submission participant drift")
            carrier=self.commands[participant_id]
            if (
                int(carrier.command1) != BATTLE_COM_ATTACK
                or int(carrier.command2) != int(submission.source_target_slot)
            ):
                raise ValueError(
                    "enemy AI ReHP ordering carrier must be ATTACK/source-target"
                )
        if set(rehp_submissions) & set(magic_submissions):
            raise ValueError("enemy AI ReHP/AttackMagic submissions overlap")

        relife_submissions={
            str(key):value
            for key,value in self.enemy_relife_submissions.items()
        }
        object.__setattr__(
            self,
            "enemy_relife_submissions",
            MappingProxyType(relife_submissions),
        )
        for participant_id,submission in relife_submissions.items():
            if participant_id not in self.commands:
                raise ValueError(
                    "enemy AI ReLife submission lacks ordering carrier command"
                )
            if not isinstance(submission,EnemyAiReLifeSubmission):
                raise TypeError(
                    f"enemy AI ReLife submission has wrong type for "
                    f"{participant_id}"
                )
            if str(submission.participant_id) != participant_id:
                raise ValueError("enemy AI ReLife submission participant drift")
            carrier=self.commands[participant_id]
            if (
                int(carrier.command1) != BATTLE_COM_ATTACK
                or int(carrier.command2)
                != int(submission.source_attack_target_slot)
            ):
                raise ValueError(
                    "enemy AI ReLife carrier must be ATTACK/source-target"
                )
        if set(relife_submissions) & (
            set(rehp_submissions) | set(magic_submissions)
        ):
            raise ValueError(
                "enemy AI ReLife semantic submissions overlap another skill"
            )

        damage_submissions={
            str(key):value
            for key,value in self.damage_to_hp_submissions.items()
        }
        object.__setattr__(
            self,
            "damage_to_hp_submissions",
            MappingProxyType(damage_submissions),
        )
        for participant_id,submission in damage_submissions.items():
            if participant_id not in self.commands:
                raise ValueError(
                    "enemy AI DamageToHp submission lacks carrier command"
                )
            if not isinstance(submission,EnemyAiDamageToHpSubmission):
                raise TypeError(
                    f"enemy AI DamageToHp submission has wrong type for "
                    f"{participant_id}"
                )
            if str(submission.participant_id) != participant_id:
                raise ValueError("enemy AI DamageToHp participant drift")
            carrier=self.commands[participant_id]
            if (
                int(carrier.command1) != BATTLE_COM_ATTACK
                or int(carrier.command2) != int(submission.source_target_slot)
            ):
                raise ValueError(
                    "enemy AI DamageToHp carrier must be ATTACK/source-target"
                )
        if set(damage_submissions) & (
            set(relife_submissions) | set(rehp_submissions) | set(magic_submissions)
        ):
            raise ValueError(
                "enemy AI DamageToHp semantic submissions overlap another skill"
            )

        mp_submissions={
            str(key):value for key,value in self.mp_damage_submissions.items()
        }
        object.__setattr__(
            self,"mp_damage_submissions",MappingProxyType(mp_submissions)
        )
        for participant_id,submission in mp_submissions.items():
            if participant_id not in self.commands:
                raise ValueError("enemy AI MpDamage submission lacks carrier command")
            if not isinstance(submission,EnemyAiMpDamageSubmission):
                raise TypeError(
                    f"enemy AI MpDamage submission has wrong type for "
                    f"{participant_id}"
                )
            if str(submission.participant_id) != participant_id:
                raise ValueError("enemy AI MpDamage participant drift")
            carrier=self.commands[participant_id]
            if (
                int(carrier.command1) != BATTLE_COM_ATTACK
                or int(carrier.command2) != int(submission.source_target_slot)
            ):
                raise ValueError(
                    "enemy AI MpDamage carrier must be ATTACK/source-target"
                )
        if set(mp_submissions) & (
            set(damage_submissions) | set(relife_submissions) | set(rehp_submissions)
            | set(magic_submissions)
        ):
            raise ValueError(
                "enemy AI MpDamage semantic submissions overlap another skill"
            )

        fall_submissions={
            str(key):value
            for key,value in self.fall_ground_submissions.items()
        }
        object.__setattr__(
            self,"fall_ground_submissions",MappingProxyType(fall_submissions)
        )
        for participant_id,submission in fall_submissions.items():
            if participant_id not in self.commands:
                raise ValueError(
                    "enemy AI FallGround submission lacks carrier command"
                )
            if not isinstance(submission,EnemyAiFallGroundSubmission):
                raise TypeError(
                    f"enemy AI FallGround submission has wrong type for "
                    f"{participant_id}"
                )
            if str(submission.participant_id) != participant_id:
                raise ValueError("enemy AI FallGround participant drift")
            carrier=self.commands[participant_id]
            if (
                int(carrier.command1) != BATTLE_COM_ATTACK
                or int(carrier.command2) != int(submission.source_target_slot)
            ):
                raise ValueError(
                    "enemy AI FallGround carrier must be ATTACK/source-target"
                )
        if set(fall_submissions) & (
            set(mp_submissions) | set(damage_submissions)
            | set(relife_submissions) | set(rehp_submissions) | set(magic_submissions)
        ):
            raise ValueError(
                "enemy AI FallGround semantic submissions overlap another skill"
            )


        tear_submissions={
            str(key):value for key,value in self.battle_tear_submissions.items()
        }
        object.__setattr__(
            self,"battle_tear_submissions",MappingProxyType(tear_submissions)
        )
        for participant_id,submission in tear_submissions.items():
            if participant_id not in self.commands:
                raise ValueError(
                    "enemy AI BattleTear submission lacks carrier command"
                )
            if not isinstance(submission,EnemyAiBattleTearSubmission):
                raise TypeError(
                    f"enemy AI BattleTear submission has wrong type for "
                    f"{participant_id}"
                )
            if str(submission.participant_id) != participant_id:
                raise ValueError("enemy AI BattleTear participant drift")
            carrier=self.commands[participant_id]
            if (
                int(carrier.command1) != BATTLE_COM_ATTACK
                or int(carrier.command2) != int(submission.source_target_slot)
            ):
                raise ValueError(
                    "enemy AI BattleTear carrier must be ATTACK/source-target"
                )
        if set(tear_submissions) & (
            set(fall_submissions) | set(mp_submissions)
            | set(damage_submissions) | set(relife_submissions) | set(rehp_submissions)
            | set(magic_submissions)
        ):
            raise ValueError(
                "enemy AI BattleTear semantic submissions overlap another skill"
            )

        nocast_submissions={
            str(key):value for key,value in self.nocast_submissions.items()
        }
        object.__setattr__(
            self,"nocast_submissions",MappingProxyType(nocast_submissions)
        )
        for participant_id,submission in nocast_submissions.items():
            if participant_id not in self.commands:
                raise ValueError("enemy AI Nocast submission lacks carrier command")
            if not isinstance(submission,EnemyAiNocastSubmission):
                raise TypeError(
                    f"enemy AI Nocast submission has wrong type for {participant_id}"
                )
            if str(submission.participant_id) != participant_id:
                raise ValueError("enemy AI Nocast participant drift")
            carrier=self.commands[participant_id]
            if (
                int(carrier.command1) != BATTLE_COM_ATTACK
                or int(carrier.command2) != int(submission.source_target_slot)
            ):
                raise ValueError(
                    "enemy AI Nocast carrier must be ATTACK/source-target"
                )
        if set(nocast_submissions) & (
            set(tear_submissions) | set(fall_submissions) | set(mp_submissions)
            | set(damage_submissions) | set(relife_submissions) | set(rehp_submissions)
            | set(magic_submissions)
        ):
            raise ValueError(
                "enemy AI Nocast semantic submissions overlap another skill"
            )

        guard_break2_submissions={
            str(key):value
            for key,value in self.guard_break2_submissions.items()
        }
        object.__setattr__(
            self,
            "guard_break2_submissions",
            MappingProxyType(guard_break2_submissions),
        )
        for participant_id,submission in guard_break2_submissions.items():
            if participant_id not in self.commands:
                raise ValueError(
                    "enemy AI GuardBreak2 submission lacks carrier command"
                )
            if not isinstance(submission,EnemyAiGuardBreak2Submission):
                raise TypeError(
                    f"enemy AI GuardBreak2 submission has wrong type for "
                    f"{participant_id}"
                )
            if str(submission.participant_id) != participant_id:
                raise ValueError("enemy AI GuardBreak2 participant drift")
            carrier=self.commands[participant_id]
            if (
                int(carrier.command1) != BATTLE_COM_ATTACK
                or int(carrier.command2) != int(submission.source_target_slot)
            ):
                raise ValueError(
                    "enemy AI GuardBreak2 carrier must be ATTACK/source-target"
                )
        if set(guard_break2_submissions) & (
            set(nocast_submissions) | set(tear_submissions)
            | set(fall_submissions) | set(mp_submissions)
            | set(damage_submissions) | set(relife_submissions) | set(rehp_submissions)
            | set(magic_submissions)
        ):
            raise ValueError(
                "enemy AI GuardBreak2 semantic submissions overlap another skill"
            )

        barrier_submissions={
            str(key):value for key,value in self.barrier_submissions.items()
        }
        object.__setattr__(
            self,
            "barrier_submissions",
            MappingProxyType(barrier_submissions),
        )
        for participant_id,submission in barrier_submissions.items():
            if participant_id not in self.commands:
                raise ValueError(
                    "enemy AI Barrier submission lacks carrier command"
                )
            if not isinstance(submission,EnemyAiBarrierSubmission):
                raise TypeError(
                    f"enemy AI Barrier submission has wrong type for "
                    f"{participant_id}"
                )
            if str(submission.participant_id) != participant_id:
                raise ValueError("enemy AI Barrier participant drift")
            carrier=self.commands[participant_id]
            if (
                int(carrier.command1) != BATTLE_COM_ATTACK
                or int(carrier.command2) != int(submission.source_target_slot)
            ):
                raise ValueError(
                    "enemy AI Barrier carrier must be ATTACK/source-target"
                )
        if set(barrier_submissions) & (
            set(guard_break2_submissions) | set(nocast_submissions)
            | set(tear_submissions) | set(fall_submissions)
            | set(mp_submissions) | set(damage_submissions)
            | set(relife_submissions) | set(rehp_submissions) | set(magic_submissions)
        ):
            raise ValueError(
                "enemy AI Barrier semantic submissions overlap another skill"
            )

        attack_crazed_submissions={
            str(key):value for key,value in self.attack_crazed_submissions.items()
        }
        object.__setattr__(
            self,
            "attack_crazed_submissions",
            MappingProxyType(attack_crazed_submissions),
        )
        for participant_id,submission in attack_crazed_submissions.items():
            if participant_id not in self.commands:
                raise ValueError(
                    "enemy AI AttackCrazed submission lacks carrier command"
                )
            if not isinstance(submission,EnemyAiAttackCrazedSubmission):
                raise TypeError(
                    f"enemy AI AttackCrazed submission has wrong type for "
                    f"{participant_id}"
                )
            if str(submission.participant_id) != participant_id:
                raise ValueError("enemy AI AttackCrazed participant drift")
            carrier=self.commands[participant_id]
            if (
                int(carrier.command1) != BATTLE_COM_ATTACK
                or int(carrier.command2) != int(submission.source_target_slot)
            ):
                raise ValueError(
                    "enemy AI AttackCrazed carrier must be ATTACK/source-target"
                )
        if set(attack_crazed_submissions) & (
            set(barrier_submissions) | set(guard_break2_submissions) | set(nocast_submissions)
            | set(tear_submissions) | set(fall_submissions)
            | set(mp_submissions) | set(damage_submissions)
            | set(relife_submissions) | set(rehp_submissions) | set(magic_submissions)
        ):
            raise ValueError(
                "enemy AI AttackCrazed semantic submissions overlap another skill"
            )


        mdfyattack_submissions={str(k):v for k,v in self.mdfyattack_submissions.items()}
        object.__setattr__(self,"mdfyattack_submissions",MappingProxyType(mdfyattack_submissions))
        for pid,submission in mdfyattack_submissions.items():
            if not isinstance(submission,EnemyAiMdfyAttackSubmission):
                raise TypeError("enemy AI Mdfyattack submission has wrong type")
            if pid not in self.commands or submission.participant_id!=pid:
                raise ValueError("enemy AI Mdfyattack participant/carrier drift")
            command=self.commands[pid]
            if command.command1!=BATTLE_COM_ATTACK or command.command2!=submission.source_target_slot:
                raise ValueError("enemy AI Mdfyattack carrier must be ATTACK/source-target")
        if set(mdfyattack_submissions) & (
            set(attack_crazed_submissions) | set(barrier_submissions) | set(guard_break2_submissions)
            | set(nocast_submissions) | set(tear_submissions) | set(fall_submissions)
            | set(mp_submissions) | set(damage_submissions) | set(relife_submissions) | set(rehp_submissions) | set(magic_submissions)
        ):
            raise ValueError("enemy AI Mdfyattack semantic submissions overlap another skill")

        weaken_submissions={str(k):v for k,v in self.weaken_submissions.items()}
        object.__setattr__(self,"weaken_submissions",MappingProxyType(weaken_submissions))
        for pid,submission in weaken_submissions.items():
            if not isinstance(submission,EnemyAiWeakenSubmission):
                raise TypeError("enemy AI Weaken submission has wrong type")
            if pid not in self.commands or submission.participant_id!=pid:
                raise ValueError("enemy AI Weaken participant/carrier drift")
            command=self.commands[pid]
            if command.command1!=BATTLE_COM_ATTACK or command.command2!=submission.source_target_slot:
                raise ValueError("enemy AI Weaken carrier must be ATTACK/source-target")
        if set(weaken_submissions) & (
            set(mdfyattack_submissions) | set(attack_crazed_submissions) | set(barrier_submissions)
            | set(guard_break2_submissions) | set(nocast_submissions) | set(tear_submissions)
            | set(fall_submissions) | set(mp_submissions) | set(damage_submissions)
            | set(relife_submissions) | set(rehp_submissions) | set(magic_submissions)
        ):
            raise ValueError("enemy AI Weaken semantic submissions overlap another skill")

        wildviolent_submissions={
            str(key):value
            for key,value in self.wildviolent_submissions.items()
        }
        object.__setattr__(
            self,
            "wildviolent_submissions",
            MappingProxyType(wildviolent_submissions),
        )
        for participant_id,submission in wildviolent_submissions.items():
            if participant_id not in self.commands:
                raise ValueError(
                    "enemy AI WildViolentAttack submission lacks carrier command"
                )
            if not isinstance(submission,EnemyAiWildViolentSubmission):
                raise TypeError(
                    "enemy AI WildViolentAttack submission has wrong type"
                )
            if str(submission.participant_id)!=participant_id:
                raise ValueError(
                    "enemy AI WildViolentAttack participant drift"
                )
            carrier=self.commands[participant_id]
            if (
                int(carrier.command1)!=BATTLE_COM_ATTACK
                or int(carrier.command2)!=int(submission.source_target_slot)
                or int(carrier.command3)!=int(submission.setup.packed_com3)
            ):
                raise ValueError(
                    "enemy AI WildViolentAttack carrier must preserve "
                    "ATTACK/source-target/setup COM3"
                )
            effects=self.setup_effects.get(participant_id)
            if effects is None or (
                effects.attack_power,effects.defense_power
            ) != (
                submission.setup.attack_power,submission.setup.defense_power
            ):
                raise ValueError(
                    "enemy AI WildViolentAttack callback work-power setup drift"
                )
        wild_overlap=(
            set(magic_submissions) | set(relife_submissions) | set(rehp_submissions)
            | set(damage_submissions) | set(mp_submissions)
            | set(fall_submissions) | set(tear_submissions)
            | set(nocast_submissions) | set(guard_break2_submissions)
            | set(barrier_submissions) | set(attack_crazed_submissions)
            | set(mdfyattack_submissions) | set(weaken_submissions)
        )
        if set(wildviolent_submissions) & wild_overlap:
            raise ValueError(
                "enemy AI WildViolentAttack semantic submissions overlap another skill"
            )

        refresh_submissions={
            str(key):value for key,value in self.refresh_submissions.items()
        }
        object.__setattr__(
            self,
            "refresh_submissions",
            MappingProxyType(refresh_submissions),
        )
        for participant_id,submission in refresh_submissions.items():
            if participant_id not in self.commands:
                raise ValueError("enemy AI Refresh submission lacks carrier command")
            if not isinstance(submission,EnemyAiRefreshSubmission):
                raise TypeError(
                    f"enemy AI Refresh submission has wrong type for {participant_id}"
                )
            if str(submission.participant_id) != participant_id:
                raise ValueError("enemy AI Refresh participant drift")
            carrier=self.commands[participant_id]
            if (
                int(carrier.command1) != BATTLE_COM_ATTACK
                or int(carrier.command2) != int(submission.source_target_slot)
            ):
                raise ValueError(
                    "enemy AI Refresh carrier must be ATTACK/source-target"
                )
        refresh_overlap=(
            set(magic_submissions) | set(relife_submissions) | set(rehp_submissions)
            | set(damage_submissions) | set(mp_submissions)
            | set(fall_submissions) | set(tear_submissions)
            | set(nocast_submissions) | set(guard_break2_submissions)
            | set(barrier_submissions) | set(attack_crazed_submissions)
            | set(mdfyattack_submissions) | set(weaken_submissions)
            | set(wildviolent_submissions)
        )
        if set(refresh_submissions) & refresh_overlap:
            raise ValueError(
                "enemy AI Refresh semantic submissions overlap another skill"
            )

        setmagicpet_submissions={
            str(key):value
            for key,value in self.setmagicpet_submissions.items()
        }
        object.__setattr__(
            self,
            "setmagicpet_submissions",
            MappingProxyType(setmagicpet_submissions),
        )
        for participant_id,submission in setmagicpet_submissions.items():
            if participant_id not in self.commands:
                raise ValueError(
                    "enemy AI SetMagicPet submission lacks carrier command"
                )
            if not isinstance(submission,EnemyAiSetMagicPetSubmission):
                raise TypeError(
                    "enemy AI SetMagicPet submission has wrong type for "
                    + participant_id
                )
            if str(submission.participant_id)!=participant_id:
                raise ValueError("enemy AI SetMagicPet participant drift")
            carrier=self.commands[participant_id]
            if (
                int(carrier.command1)!=BATTLE_COM_ATTACK
                or int(carrier.command2)!=int(submission.source_target_slot)
            ):
                raise ValueError(
                    "enemy AI SetMagicPet carrier must be ATTACK/source-target"
                )
        setmagicpet_overlap=(
            set(magic_submissions) | set(relife_submissions) | set(rehp_submissions)
            | set(damage_submissions) | set(mp_submissions)
            | set(fall_submissions) | set(tear_submissions)
            | set(nocast_submissions) | set(guard_break2_submissions)
            | set(barrier_submissions) | set(attack_crazed_submissions)
            | set(mdfyattack_submissions) | set(weaken_submissions)
            | set(wildviolent_submissions) | set(refresh_submissions)
        )
        if set(setmagicpet_submissions) & setmagicpet_overlap:
            raise ValueError(
                "enemy AI SetMagicPet semantic submissions overlap another skill"
            )

        battletimid_submissions={
            str(key):value
            for key,value in self.battletimid_submissions.items()
        }
        object.__setattr__(
            self,
            "battletimid_submissions",
            MappingProxyType(battletimid_submissions),
        )
        for participant_id,submission in battletimid_submissions.items():
            if participant_id not in self.commands:
                raise ValueError(
                    "enemy AI BattleTimid submission lacks carrier command"
                )
            if not isinstance(submission,EnemyAiBattleTimidSubmission):
                raise TypeError(
                    "enemy AI BattleTimid submission has wrong type for "
                    + participant_id
                )
            if str(submission.participant_id)!=participant_id:
                raise ValueError("enemy AI BattleTimid participant drift")
            carrier=self.commands[participant_id]
            if (
                int(carrier.command1)!=BATTLE_COM_ATTACK
                or int(carrier.command2)!=int(submission.source_target_slot)
            ):
                raise ValueError(
                    "enemy AI BattleTimid carrier must be ATTACK/source-target"
                )
            effects=self.setup_effects.get(participant_id)
            if effects is None or (
                effects.attack_power,effects.defense_power
            ) != (
                submission.setup.attack_power,
                submission.setup.defence_power,
            ):
                raise ValueError(
                    "enemy AI BattleTimid callback work-power setup drift"
                )
        battletimid_overlap=(
            set(magic_submissions) | set(relife_submissions) | set(rehp_submissions)
            | set(damage_submissions) | set(mp_submissions)
            | set(fall_submissions) | set(tear_submissions)
            | set(nocast_submissions) | set(guard_break2_submissions)
            | set(barrier_submissions) | set(attack_crazed_submissions)
            | set(mdfyattack_submissions) | set(weaken_submissions)
            | set(wildviolent_submissions) | set(refresh_submissions)
            | set(setmagicpet_submissions)
        )
        if set(battletimid_submissions) & battletimid_overlap:
            raise ValueError(
                "enemy AI BattleTimid semantic submissions overlap another skill"
            )

        lighttakeed_submissions={
            str(key):value
            for key,value in self.lighttakeed_submissions.items()
        }
        object.__setattr__(
            self,
            "lighttakeed_submissions",
            MappingProxyType(lighttakeed_submissions),
        )
        for participant_id,submission in lighttakeed_submissions.items():
            if participant_id not in self.commands:
                raise ValueError(
                    "enemy AI Lighttakeed submission lacks carrier command"
                )
            if not isinstance(submission,EnemyAiLighttakeedSubmission):
                raise TypeError(
                    "enemy AI Lighttakeed submission has wrong type for "
                    + participant_id
                )
            if str(submission.participant_id)!=participant_id:
                raise ValueError("enemy AI Lighttakeed participant drift")
            carrier=self.commands[participant_id]
            if (
                int(carrier.command1)!=BATTLE_COM_ATTACK
                or int(carrier.command2)!=int(submission.source_target_slot)
            ):
                raise ValueError(
                    "enemy AI Lighttakeed carrier must be ATTACK/source-target"
                )
            effects=self.setup_effects.get(participant_id)
            if effects is None or (
                effects.attack_power,effects.defense_power
            ) != (
                submission.attack_power,submission.defense_power
            ):
                raise ValueError(
                    "enemy AI Lighttakeed callback work-power setup drift"
                )
        lighttakeed_overlap=battletimid_overlap | set(battletimid_submissions)
        if set(lighttakeed_submissions) & lighttakeed_overlap:
            raise ValueError(
                "enemy AI Lighttakeed semantic submissions overlap another skill"
            )

        combined_submissions={
            str(key):value
            for key,value in self.combined_submissions.items()
        }
        object.__setattr__(
            self,
            "combined_submissions",
            MappingProxyType(combined_submissions),
        )
        for participant_id,submission in combined_submissions.items():
            if participant_id not in self.commands:
                raise ValueError(
                    "enemy AI Combined submission lacks carrier command"
                )
            if not isinstance(submission,EnemyAiCombinedSubmission):
                raise TypeError(
                    "enemy AI Combined submission has wrong type for "
                    + participant_id
                )
            if str(submission.participant_id)!=participant_id:
                raise ValueError("enemy AI Combined participant drift")
            carrier=self.commands[participant_id]
            if (
                int(carrier.command1)!=BATTLE_COM_ATTACK
                or int(carrier.command2)!=int(submission.source_target_slot)
            ):
                raise ValueError(
                    "enemy AI Combined carrier must be ATTACK/source-target"
                )
        combined_overlap=(
            lighttakeed_overlap
            | set(battletimid_submissions)
            | set(lighttakeed_submissions)
        )
        if set(combined_submissions) & combined_overlap:
            raise ValueError(
                "enemy AI Combined semantic submissions overlap another skill"
            )

        vary_submissions={
            str(key):value
            for key,value in self.vary_submissions.items()
        }
        object.__setattr__(
            self,
            "vary_submissions",
            MappingProxyType(vary_submissions),
        )
        for participant_id,submission in vary_submissions.items():
            if participant_id not in self.commands:
                raise ValueError(
                    "enemy AI Vary submission lacks carrier command"
                )
            if not isinstance(submission,EnemyAiVarySubmission):
                raise TypeError(
                    "enemy AI Vary submission has wrong type for "
                    + participant_id
                )
            if str(submission.participant_id)!=participant_id:
                raise ValueError("enemy AI Vary participant drift")
            carrier=self.commands[participant_id]
            if (
                int(carrier.command1)!=BATTLE_COM_ATTACK
                or int(carrier.command2)!=int(
                    submission.source_target_carrier
                )
            ):
                raise ValueError(
                    "enemy AI Vary carrier must be ATTACK/source-target"
                )
        vary_overlap=(
            combined_overlap
            | set(battletimid_submissions)
            | set(combined_submissions)
        )
        if set(vary_submissions) & vary_overlap:
            raise ValueError(
                "enemy AI Vary semantic submissions overlap another skill"
            )

        modifyattack_submissions={str(pid):value for pid,value in self.modifyattack_submissions.items()}
        object.__setattr__(self,"modifyattack_submissions",MappingProxyType(modifyattack_submissions))
        for pid,submission in modifyattack_submissions.items():
            if not isinstance(submission,EnemyAiModifyAttackSubmission):
                raise TypeError("enemy AI Modifyattack submission has wrong type")
            if pid not in self.commands or submission.participant_id!=pid:
                raise ValueError("enemy AI Modifyattack participant/carrier drift")
            carrier=self.commands[pid]
            if carrier.command1!=BATTLE_COM_ATTACK or carrier.command2!=submission.source_target_slot:
                raise ValueError("enemy AI Modifyattack carrier must be ATTACK/source-target")
            if self.setup_effects.get(pid,BattleCommandSetupEffects())!=BattleCommandSetupEffects():
                raise ValueError("Modifyattack callback does not mutate work powers")
        for field_name in self.__dataclass_fields__:
            if field_name.endswith("_submissions") and field_name!="modifyattack_submissions":
                if set(modifyattack_submissions) & set(getattr(self,field_name)):
                    raise ValueError("enemy AI Modifyattack semantic submissions overlap another skill")


@dataclass
class LocalRuntimeSessionCoordinator:
    """Application-service boundary for one authoritative local play session."""

    stack: object
    persistence: LocalPersistenceStore
    occupancy_registry: RuntimeDynamicOccupancyRegistry = field(
        default_factory=RuntimeDynamicOccupancyRegistry
    )
    encounter_frequency: EncounterFrequencyState = field(
        default_factory=EncounterFrequencyState
    )

    def __post_init__(self) -> None:
        initial_occupancy = self._initial_occupancy()
        if initial_occupancy is not None:
            initial_occupancy.populate_registry(self.occupancy_registry)

    def _initial_occupancy(self):
        return getattr(self.stack, "npc_initial_occupancy", None)

    def _validate_occupancy_registry(
        self,
        registry: RuntimeDynamicOccupancyRegistry,
    ) -> RuntimeDynamicOccupancyRegistry:
        if not isinstance(registry, RuntimeDynamicOccupancyRegistry):
            raise TypeError("session coordinator occupancy registry type mismatch")
        invalid = tuple(
            obj.object_id
            for obj in registry.objects.values()
            if not self.topology.is_valid_position(obj.position)
        )
        if invalid:
            raise ValueError(
                "session coordinator occupancy object outside topology: "
                + ",".join(invalid[:5])
            )
        return registry

    def _reset_occupancy_to_initial(self) -> None:
        self.occupancy_registry = self._validate_occupancy_registry(
            build_initial_occupancy_registry(self._initial_occupancy())
        )

    def _reset_encounter_frequency(self) -> None:
        # CEP is stable-descendant connection/runtime state, not player save data.
        self.encounter_frequency = EncounterFrequencyState()

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
        session = self._validate_session(session)
        self._reset_occupancy_to_initial()
        self._reset_encounter_frequency()
        return session

    def save_game(
        self,
        key: str,
        session: LocalRuntimeSessionState,
    ) -> None:
        session = self._validate_session(session)
        self._validate_occupancy_registry(self.occupancy_registry)
        snapshot = LocalRuntimeSaveSnapshot(
            session=session,
            occupancy=build_local_runtime_occupancy_delta(
                registry=self.occupancy_registry,
                initial_occupancy=self._initial_occupancy(),
            ),
        )
        self.persistence.save(
            _nonempty_key(key),
            encode_local_runtime_save(snapshot),
        )

    def continue_game(self, key: str) -> LocalRuntimeSessionState:
        payload = self.persistence.load(_nonempty_key(key))
        if payload is None:
            raise KeyError(f"local save does not exist: {key}")

        schema = local_runtime_payload_schema(payload)
        if schema == LOCAL_RUNTIME_SAVE_SCHEMA:
            snapshot = decode_local_runtime_save(
                payload,
                expected_contract_id=self.profile.contract_id,
                expected_world_profile=self.profile.runtime_world_profile,
            )
            session = self._validate_session(snapshot.session)
            restored = restore_local_runtime_occupancy_registry(
                delta=snapshot.occupancy,
                initial_occupancy=self._initial_occupancy(),
            )
            self.occupancy_registry = self._validate_occupancy_registry(restored)
            self._reset_encounter_frequency()
            return session

        if schema == LOCAL_SESSION_SCHEMA:
            session = decode_local_runtime_session(
                payload,
                expected_contract_id=self.profile.contract_id,
                expected_world_profile=self.profile.runtime_world_profile,
            )
            session = self._validate_session(session)
            self._reset_occupancy_to_initial()
            self._reset_encounter_frequency()
            return session

        raise ValueError(f"unsupported local persistence schema: {schema}")

    def plan_player_core_dying(
        self,
        session: LocalRuntimeSessionState,
        *,
        attacker_class: str,
        equipped_slots: Sequence[int],
        dead_count_before: int,
    ) -> LocalRuntimePlayerDeathPlan:
        """Apply only representable core_Dying persistence and return world actions.

        The historical callback's party discharge, equipment-drop requests,
        hidden death/status flags and dead-count mutation are returned
        semantically because the current local session has no authoritative
        party/equipment/hidden-player-state container. The v1-direct carried
        gold field is representable and is set to zero on a cloned session.
        """

        session = self._validate_session(session)
        if session.player_state.character is None:
            raise ValueError("player death requires persistent character state")
        fields = dict(session.player_state.character.fields)
        if "gold" not in fields:
            raise ValueError("player death requires v1-direct gold field")

        transition = death_transition(
            int(fields["gold"]),
            tuple(int(x) for x in equipped_slots),
            str(attacker_class),
            dead_count=int(dead_count_before),
        )

        working = decode_persistent_state(
            encode_persistent_state(session.player_state)
        )
        if working.character is None:
            raise ValueError("player death clone lost character state")
        next_fields = dict(working.character.fields)
        next_fields["gold"] = int(transition["final_carried_gold"])
        working.character = replace(
            working.character,
            fields=MappingProxyType(next_fields),
        )
        updated = replace(
            session,
            player_state=working,
        )
        self._validate_session(updated)

        return LocalRuntimePlayerDeathPlan(
            session=updated,
            party_discharged=bool(transition["party_discharged"]),
            item_drop_mode=str(transition["item_drop_mode"]),
            requested_item_drop_slots=tuple(
                int(x) for x in transition["requested_item_drop_slots"]
            ),
            random_item_drop_candidates=tuple(
                int(x) for x in transition["random_item_drop_candidates"]
            ),
            random_item_drop_count=int(
                transition["random_item_drop_count"]
            ),
            requested_ground_gold=int(
                transition["requested_ground_gold"]
            ),
            final_carried_gold=int(transition["final_carried_gold"]),
            dead_count_after=int(transition["dead_count"]),
            cleared_statuses=tuple(
                str(x) for x in transition["cleared_statuses"]
            ),
            is_dead=bool(transition["is_dead"]),
            is_attacked=bool(transition["is_attacked"]),
        )

    def resurrect_player_in_place(
        self,
        session: LocalRuntimeSessionState,
        *,
        requested_hp: int,
    ) -> LocalRuntimePlayerResurrectionResult:
        """Apply explicit in-place CHAR_playerresurrect HP semantics only."""

        session = self._validate_session(session)
        if session.player_state.character is None:
            raise ValueError("player resurrection requires character state")
        fields = dict(session.player_state.character.fields)
        if "max_hp" not in fields or "hp" not in fields:
            raise ValueError("player resurrection requires hp/max_hp fields")

        transition = resurrect_transition(
            int(requested_hp),
            int(fields["max_hp"]),
        )
        working = decode_persistent_state(
            encode_persistent_state(session.player_state)
        )
        if working.character is None:
            raise ValueError("player resurrection clone lost character state")
        next_fields = dict(working.character.fields)
        next_fields["hp"] = int(transition["hp"])
        working.character = replace(
            working.character,
            fields=MappingProxyType(next_fields),
        )
        updated = replace(
            session,
            player_state=working,
        )
        self._validate_session(updated)

        return LocalRuntimePlayerResurrectionResult(
            session=updated,
            base_image_restored=bool(
                transition["base_image_restored"]
            ),
            is_dead=bool(transition["is_dead"]),
            is_attacked=bool(transition["is_attacked"]),
            is_overed=bool(transition["is_overed"]),
            mp_unchanged=bool(transition["mp_unchanged"]),
            location_unchanged=bool(
                transition["location_unchanged"]
            ),
        )

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

    def walk_one_cell_with_runtime_collision(
        self,
        session: LocalRuntimeSessionState,
        *,
        destination: MapPosition,
        destination_occupants: Sequence[DynamicOccupant] = (),
        map_objmove_ok: bool = True,
    ) -> LocalRuntimeWalkResult:
        """Resolve static routed collision, then independent live occupancy."""
        session = self._validate_session(session)
        router = getattr(self.stack, "collision_router", None)
        if router is None:
            raise ValueError("runtime stack has no unified collision router")
        live_query = self.occupancy_registry.query(destination)
        layered = resolve_runtime_collision_with_occupancy(
            router=router,
            origin=session.player_position,
            destination=destination,
            destination_occupants=(
                live_query.occupants + tuple(destination_occupants)
            ),
        )
        routed = layered.static
        result = self.walk_one_cell(
            session,
            destination=destination,
            entry_allowed=layered.decision.allowed,
            map_objmove_ok=bool(map_objmove_ok),
        )
        return LocalRuntimeWalkResult(
            session=result.session,
            resolution=result.resolution,
            collision=layered.decision,
            collision_provider_kind=routed.route.provider_kind,
            collision_evidence_class=routed.route.evidence_class,
            collision_semantic_profile=routed.route.semantic_profile,
            collision_exact_binary_proof=(
                routed.route.exact_recovered25_binary_proof
            ),
            static_collision=routed.decision,
            dynamic_collision=layered.dynamic,
            dynamic_occupancy_profile=layered.dynamic_profile,
            dynamic_occupancy_evidence_class=layered.dynamic_evidence_class,
            live_occupancy_registry_profile=self.occupancy_registry.profile_id,
            live_occupancy_object_ids=live_query.object_ids,
            live_occupancy_provenance=live_query.provenances,
        )

    def walk_one_cell_with_runtime_collision_and_encounter_frequency(
        self,
        session: LocalRuntimeSessionState,
        *,
        destination: MapPosition,
        frequency_roll: int | None,
        encounter_rolls: EncounterRolls,
        destination_occupants: Sequence[DynamicOccupant] = (),
        map_objmove_ok: bool = True,
        encounter_eligible: bool = True,
    ) -> LocalRuntimeEncounterWalkResult:
        """Compose ordinary movement with the reconstructed descendant CEP loop.

        Random values remain explicit caller inputs. CEP is transient runtime
        state and is not serialized into the local player/session save.
        """

        session = self._validate_session(session)
        encounter_runtime = getattr(self.stack, "encounter_runtime", None)
        if encounter_runtime is None:
            raise ValueError("runtime stack has no encounter runtime")
        if not isinstance(encounter_rolls, EncounterRolls):
            raise TypeError("encounter_rolls must be EncounterRolls")

        origin = session.player_position
        walk = self.walk_one_cell_with_runtime_collision(
            session,
            destination=destination,
            destination_occupants=destination_occupants,
            map_objmove_ok=bool(map_objmove_ok),
        )
        if not walk.resolution.moved:
            return LocalRuntimeEncounterWalkResult(
                walk=walk,
                frequency=None,
            )

        source_area = active_encounter_area(
            encounter_runtime.encounter_areas,
            floor=origin.floor_id,
            x=origin.x,
            y=origin.y,
        )
        refreshed = refresh_frequency_bounds(
            self.encounter_frequency,
            source_area,
        )
        frequency = resolve_frequency_step(
            refreshed,
            roll=frequency_roll,
            encounter_enabled=not walk.resolution.encounter_suppressed,
            eligible=bool(encounter_eligible),
        )
        self.encounter_frequency = frequency.after

        group_encounter = None
        encounter = None
        if frequency.encounter_triggered:
            group_encounter = self.stack.request_encounter_group(
                walk.session,
                group_roll=encounter_rolls.group_roll,
            )
            encounter = self.stack.request_encounter(
                walk.session,
                group_roll=encounter_rolls.group_roll,
                enemy_roll=encounter_rolls.enemy_roll,
                level_roll=encounter_rolls.level_roll,
            )

        return LocalRuntimeEncounterWalkResult(
            walk=walk,
            frequency=frequency,
            group_encounter=group_encounter,
            encounter=encounter,
        )

    @staticmethod
    def _battle_working_persistent_payload(
        context: LocalRuntimeBattleContext,
    ) -> str:
        return (
            context.persistent_state_payload
            if context.working_persistent_state_payload is None
            else context.working_persistent_state_payload
        )

    def start_group_battle(
        self,
        session: LocalRuntimeSessionState,
        encounter: GroupEncounterRequest,
        *,
        entry_count_roll: int,
        selection_rolls: Sequence[int],
        birth_rolls: Sequence[EnemyBirthRolls],
        allied_pet_slots: Sequence[int] = (),
        ride_pet_slot: int | None = None,
    ) -> LocalRuntimeBattleContext:
        """Start a transient group battle from explicit recovered spawn rolls."""

        session = self._validate_session(session)
        if encounter.position != session.player_position:
            raise ValueError(
                "group encounter position does not match authoritative session"
            )
        encounter_runtime = getattr(self.stack, "encounter_runtime", None)
        if encounter_runtime is None:
            raise ValueError("runtime stack has no encounter runtime")

        persistent_payload = encode_persistent_state(session.player_state)
        working_state = decode_persistent_state(persistent_payload)
        domain = SinglePlayerHistoricalDomain(
            static=encounter_runtime.static_data,
            persistent=working_state,
        )
        domain.move_player(
            floor_id=session.player_position.floor_id,
            x=session.player_position.x,
            y=session.player_position.y,
        )

        spawned = tuple(
            self.stack.spawn_group_enemies(
                encounter,
                entry_count_roll=int(entry_count_roll),
                selection_rolls=tuple(int(x) for x in selection_rolls),
                birth_rolls=tuple(birth_rolls),
            )
        )
        battle = begin_group_battle(
            domain,
            encounter,
            enemies=tuple(row.participant for row in spawned),
            allied_pet_slots=tuple(int(x) for x in allied_pet_slots),
            ride_pet_slot=(
                None if ride_pet_slot is None else int(ride_pet_slot)
            ),
        )
        return LocalRuntimeBattleContext(
            contract_id=session.contract_id,
            world_profile=session.world_profile,
            hometown_ordinal=session.hometown_ordinal,
            origin_position=session.player_position,
            world_flags=session.world_flags,
            persistent_state_payload=persistent_payload,
            battle=battle,
            spawned_enemies=spawned,
        )

    def settle_group_battle(
        self,
        context: LocalRuntimeBattleContext,
        outcome: BattleOutcome,
    ) -> LocalRuntimeSessionState:
        """Apply one explicit outcome to the battle snapshot and return a new session."""

        if context.contract_id != self.profile.contract_id:
            raise ValueError("battle context bootstrap contract mismatch")
        if context.world_profile != self.profile.runtime_world_profile:
            raise ValueError("battle context world-profile mismatch")
        if not self.topology.is_valid_position(context.origin_position):
            raise ValueError("battle context origin is outside topology")

        encounter_runtime = getattr(self.stack, "encounter_runtime", None)
        if encounter_runtime is None:
            raise ValueError("runtime stack has no encounter runtime")

        working_state = decode_persistent_state(
            self._battle_working_persistent_payload(context)
        )
        domain = SinglePlayerHistoricalDomain(
            static=encounter_runtime.static_data,
            persistent=working_state,
        )
        domain.move_player(
            floor_id=context.origin_position.floor_id,
            x=context.origin_position.x,
            y=context.origin_position.y,
        )
        apply_battle_outcome(
            domain,
            context.battle,
            outcome,
        )
        updated = LocalRuntimeSessionState(
            contract_id=context.contract_id,
            world_profile=context.world_profile,
            hometown_ordinal=context.hometown_ordinal,
            player_position=context.origin_position,
            player_state=domain.persistent,
            world_flags=context.world_flags,
        )
        return self._validate_session(updated)

    def begin_persistent_group_battle(
        self,
        context: LocalRuntimeBattleContext,
        *,
        slots: Mapping[str, int],
        pet_noreturn_by_participant_id: Mapping[str,bool] | None = None,
        attack_magic_overlay: AttackMagicRoundOverlay | None = None,
        nocast_overlay: NocastRoundOverlay | None = None,
        setmagicpet_overlay: SetMagicPetRoundOverlay | None = None,
        combined_overlay: CombinedRuntimeOverlay | None = None,
    ) -> LocalRuntimeBattleContext:
        """Promote a transient group battle shell into multi-round state."""

        if context.persistent_battle_state is not None:
            raise ValueError("battle context already has persistent state")
        persistent=decode_persistent_state(
            self._battle_working_persistent_payload(context)
        )
        default_pet_slot=(
            None
            if persistent.default_pet_slot is None
            else int(persistent.default_pet_slot.value)
        )
        state = begin_persistent_battle(
            context.battle,
            slots={str(key): int(value) for key, value in slots.items()},
            default_pet_slot=default_pet_slot,
            pet_noreturn_by_participant_id=pet_noreturn_by_participant_id,
            nocast_overlay=nocast_overlay,
            setmagicpet_overlay=setmagicpet_overlay,
            combined_overlay=combined_overlay,
        )
        if (
            attack_magic_overlay is not None
            and not isinstance(attack_magic_overlay,AttackMagicRoundOverlay)
        ):
            raise TypeError("initial AttackMagic overlay has wrong type")
        return replace(
            context,
            persistent_battle_state=state,
            attack_magic_overlay=attack_magic_overlay,
        )

    def persistent_actor_direct_magic_blocked(
        self,
        context: LocalRuntimeBattleContext,
        participant_id: str,
    ) -> bool:
        """Expose fixed MAGIC_DirectUse's positive WORKNOCAST gate."""
        state=context.persistent_battle_state
        if state is None:
            raise ValueError("battle context has no persistent battle state")
        if state.nocast_overlay is None:
            return False
        return state.nocast_overlay.blocks_direct_magic(str(participant_id))

    def _build_persistent_enemy_common_batch(
        self,
        context: LocalRuntimeBattleContext,
        *,
        mode_rolls_by_enemy_id: Mapping[str, int],
        target_rolls_by_enemy_id: Mapping[str, int] | None = None,
        allow_escape: bool = False,
        allow_basic_skill: bool = False,
        allow_statuschange_skill: bool = False,
        allow_powerbalance_skill: bool = False,
        allow_mighty_skill: bool = False,
        allow_guardbreak_skill: bool = False,
        allow_guardian_skill: bool = False,
        allow_continuationattack_skill: bool = False,
        allow_chargeattack_skill: bool = False,
        allow_noguard_skill: bool = False,
        allow_abduct_skill: bool = False,
        allow_earthround_skill: bool = False,
        allow_steal_skill: bool = False,
        allow_attackmagic_skill: bool = False,
        allow_rehp_skill: bool = False,
        allow_relife_skill: bool = False,
        allow_damage_to_hp_skill: bool = False,
        allow_mp_damage_skill: bool = False,
        allow_fall_ground_skill: bool = False,
        allow_battle_tear_skill: bool = False,
        allow_nocast_skill: bool = False,
        allow_guard_break2_skill: bool = False,
        allow_battletimid_skill: bool = False,
        allow_lighttakeed_skill: bool = False,
        lighttakeed_profiles_by_enemy_id: Mapping[str,str] | None = None,
        allow_combined_skill: bool = False,
        combined_selection_draws_by_enemy_id: Mapping[str,int] | None = None,
        allow_vary_skill: bool = False,
        vary_profiles_by_enemy_id: Mapping[str,str] | None = None,
        allow_weaken_skill: bool = False,
        allow_refresh_skill: bool = False,
        allow_setmagicpet_skill: bool = False,
        allow_barrier_skill: bool = False,
        allow_modifyattack_skill: bool = False,
        allow_mdfyattack_skill: bool = False,
        allow_attack_crazed_skill: bool = False,
        allow_wildviolent_skill: bool = False,
    ) -> EnemyAiCommonCommandBatch:
        """Derive the evidence-closed common enemy-AI command subset.

        ATTACK/GUARD are always available here. ESCAPE is emitted only when the
        caller explicitly opens that execution seam; its probability context
        and RAND(1,100) input are handled separately by the round coordinator.
        A selected wa slot is admitted only when its explicitly enabled
        pet-skill execution seam is closed. Command-submission setup effects
        remain separate from COM1/COM2/COM3 and are returned in the batch.
        All other skill, magic-failure and extension paths remain fail-closed.
        """

        state = context.persistent_battle_state
        if state is None:
            raise ValueError("battle context has no persistent battle state")
        if state.phase != "active":
            raise ValueError("cannot derive enemy AI after battle termination")

        participants = (
            state.session.player,
            *state.session.allied_pets,
            *state.session.enemies,
        )
        inactive_ids=set(state.ultimate_exited_participant_ids)
        inactive_ids.update(state.battle_exited_participant_ids)
        living = {
            str(participant.participant_id): participant
            for participant in participants
            if (
                str(participant.participant_id) in state.hp_by_participant_id
                and str(participant.participant_id) not in inactive_ids
                and int(
                    state.hp_by_participant_id[
                        str(participant.participant_id)
                    ]
                ) > 0
            )
        }
        living_enemy_ids = tuple(
            str(enemy.participant_id)
            for enemy in state.session.enemies
            if str(enemy.participant_id) in living
        )
        carried_enemy_ids={
            enemy_id
            for enemy_id in living_enemy_ids
            if (
                enemy_id in state.carried_commands_by_participant_id
                and int(
                    state.carried_commands_by_participant_id[
                        enemy_id
                    ].command1
                ) in {
                    BATTLE_COM_S_CHARGE,
                    BATTLE_COM_S_EARTHROUND0,
                }
            )
        }
        ai_enemy_ids=tuple(
            enemy_id
            for enemy_id in living_enemy_ids
            if enemy_id not in carried_enemy_ids
        )
        supplied_mode_ids = {str(key) for key in mode_rolls_by_enemy_id}
        if supplied_mode_ids != set(ai_enemy_ids):
            missing = sorted(set(ai_enemy_ids) - supplied_mode_ids)
            extra = sorted(supplied_mode_ids - set(ai_enemy_ids))
            raise ValueError(
                "enemy AI mode rolls must cover exactly non-carried living "
                f"enemies; missing={missing}, extra={extra}"
            )

        target_rolls = {
            str(key): int(value)
            for key, value in (target_rolls_by_enemy_id or {}).items()
        }
        unknown_target_rolls = sorted(
            set(target_rolls) - set(ai_enemy_ids)
        )
        if unknown_target_rolls:
            raise ValueError(
                "enemy AI target rolls reference non-AI enemies: "
                + ",".join(unknown_target_rolls)
            )

        spawn_by_participant_id = {}
        for spawned in context.spawned_enemies:
            participant_id = str(spawned.participant.participant_id)
            if participant_id in spawn_by_participant_id:
                raise ValueError(
                    "duplicate spawned-enemy participant identity: "
                    + participant_id
                )
            spawn_by_participant_id[participant_id] = spawned

        targets = []
        for participant in (
            state.session.player,
            *state.session.allied_pets,
        ):
            participant_id = str(participant.participant_id)
            if participant_id not in living:
                continue
            if participant_id not in state.slots:
                raise ValueError(
                    "living enemy-AI target lacks battle slot: "
                    + participant_id
                )
            slot = int(state.slots[participant_id])
            if not 0 <= slot < 10:
                raise ValueError(
                    "enemy-AI opposing target is outside player-side slots: "
                    + participant_id
                )
            kind = (
                participant.kind
                if participant.kind in {"player", "pet"}
                else "other"
            )
            targets.append(
                EnemyAiTarget(
                    slot=slot,
                    participant_id=participant_id,
                    kind=kind,
                    hp=int(state.hp_by_participant_id[participant_id]),
                    alive=True,
                    rescue_mode=False,
                )
            )

        commands = {
            enemy_id:state.carried_commands_by_participant_id[enemy_id]
            for enemy_id in carried_enemy_ids
        }
        setup_effects = {
            enemy_id:state.carried_setup_effects_by_participant_id[enemy_id]
            for enemy_id in carried_enemy_ids
        }
        abduct_contexts={}
        attack_magic_submissions={}
        enemy_rehp_submissions={}
        enemy_relife_submissions={}
        damage_to_hp_submissions={}
        mp_damage_submissions={}
        fall_ground_submissions={}
        battle_tear_submissions={}
        nocast_submissions={}
        guard_break2_submissions={}
        battletimid_submissions={}
        lighttakeed_submissions={}
        combined_submissions={}
        vary_submissions={}
        lighttakeed_profiles={
            str(key):str(value)
            for key,value in (
                lighttakeed_profiles_by_enemy_id or {}
            ).items()
        }
        vary_profiles={
            str(key):str(value)
            for key,value in (
                vary_profiles_by_enemy_id or {}
            ).items()
        }
        combined_selection_draws={
            str(key):int(value)
            for key,value in (
                combined_selection_draws_by_enemy_id or {}
            ).items()
        }
        if any(value < 0 for value in combined_selection_draws.values()):
            raise ValueError("Combined reduced selection draw cannot be negative")
        weaken_submissions={}
        refresh_submissions={}
        setmagicpet_submissions={}
        barrier_submissions={}
        modifyattack_submissions={}
        mdfyattack_submissions={}
        attack_crazed_submissions={}
        wildviolent_submissions={}
        for enemy_id in ai_enemy_ids:
            if enemy_id not in spawn_by_participant_id:
                raise ValueError(
                    "living enemy lacks recovered spawn provenance: "
                    + enemy_id
                )
            spawned = spawn_by_participant_id[enemy_id]
            variant = spawned.variant
            if int(variant.tactics) != 1:
                raise ValueError(
                    f"enemy {enemy_id} uses unsupported TACTICS mode "
                    f"{variant.tactics}"
                )
            if not str(variant.tactics_option):
                raise ValueError(
                    "enemy lacks TACTICSOPTION provenance: " + enemy_id
                )

            decision = resolve_common_normal_enemy_ai(
                str(variant.tactics_option),
                tuple(targets),
                mode_roll=int(mode_rolls_by_enemy_id[enemy_id]),
                target_roll=target_rolls.get(enemy_id),
            )
            if decision is None:
                raise ValueError(
                    "enemy AI produced no executable common decision: "
                    + enemy_id
                )
            if decision.kind == ENEMY_AI_ATTACK:
                commands[enemy_id] = BattleCommand(
                    BATTLE_COM_ATTACK,
                    command2=int(decision.target_slot),
                )
                continue
            if decision.kind == ENEMY_AI_GUARD:
                commands[enemy_id] = BattleCommand(BATTLE_COM_GUARD)
                continue
            if decision.kind == ENEMY_AI_ESCAPE and bool(allow_escape):
                commands[enemy_id] = BattleCommand(BATTLE_COM_ESCAPE)
                continue
            if decision.kind == ENEMY_AI_SKILL and (
                bool(allow_basic_skill)
                or bool(allow_statuschange_skill)
                or bool(allow_powerbalance_skill)
                or bool(allow_mighty_skill)
                or bool(allow_guardbreak_skill)
                or bool(allow_guardian_skill)
                or bool(allow_continuationattack_skill)
                or bool(allow_chargeattack_skill)
                or bool(allow_noguard_skill)
                or bool(allow_abduct_skill)
                or bool(allow_earthround_skill)
                or bool(allow_steal_skill)
                or bool(allow_attackmagic_skill)
                or bool(allow_rehp_skill)
                or bool(allow_damage_to_hp_skill)
                or bool(allow_mp_damage_skill)
                or bool(allow_fall_ground_skill)
                or bool(allow_battle_tear_skill)
                or bool(allow_nocast_skill)
                or bool(allow_guard_break2_skill)
                or bool(allow_battletimid_skill)
                or bool(allow_lighttakeed_skill)
                or bool(allow_combined_skill)
                or bool(allow_vary_skill)
                or bool(allow_weaken_skill)
                or bool(allow_refresh_skill)
                or bool(allow_setmagicpet_skill)
                or bool(allow_barrier_skill)
                or bool(allow_modifyattack_skill)
                or bool(allow_mdfyattack_skill)
                or bool(allow_attack_crazed_skill)
                or bool(allow_wildviolent_skill)
            ):
                petskill_runtime = getattr(self.stack, "petskill_runtime", None)
                if petskill_runtime is None:
                    raise ValueError(
                        "enemy AI pet-skill selection requires recovered "
                        "pet-skill runtime"
                    )
                skill_ids=tuple(int(x) for x in spawned.template.skill_slot_ids)
                selected_skill_id=skill_ids[int(decision.skill_slot)]
                selected_skill=petskill_runtime.skills.get(selected_skill_id)
                if (
                    selected_skill is not None
                    and selected_skill.function_name == "PETSKILL_Modifyattack"
                    and bool(allow_modifyattack_skill)
                ):
                    submission=resolve_enemy_ai_modifyattack_submission(
                        spawned,skill_slot=int(decision.skill_slot),
                        target_slot=int(decision.target_slot),petskill_runtime=petskill_runtime,
                    )
                    commands[enemy_id]=BattleCommand(BATTLE_COM_ATTACK,command2=submission.source_target_slot)
                    modifyattack_submissions[enemy_id]=submission
                    continue

                if (
                    selected_skill is not None
                    and selected_skill.function_name == MDFYATTACK_CALLBACK
                    and bool(allow_mdfyattack_skill)
                ):
                    submission=resolve_enemy_ai_mdfyattack_submission(
                        spawned,skill_slot=int(decision.skill_slot),
                        target_slot=int(decision.target_slot),petskill_runtime=petskill_runtime,
                    )
                    # Scheduling carrier only; symbolic native COM1 remains
                    # distinct for attributes, combo and counter eligibility.
                    commands[enemy_id]=BattleCommand(BATTLE_COM_ATTACK,command2=submission.source_target_slot)
                    mdfyattack_submissions[enemy_id]=submission
                    continue

                if (
                    selected_skill is not None
                    and selected_skill.function_name == WILDVIOLENT_CALLBACK
                    and bool(allow_wildviolent_skill)
                ):
                    baseline=living[enemy_id]
                    current=participant_snapshot(state,enemy_id)
                    weaken_prepared=(
                        None if state.nocast_overlay is None else
                        state.nocast_overlay.runtime_by_participant_id[
                            enemy_id
                        ].prepared_weaken_powers
                    )
                    magic_prepared=(
                        None if state.setmagicpet_overlay is None else
                        state.setmagicpet_overlay.runtime_by_participant_id[
                            enemy_id
                        ].prepared_powers
                    )
                    prepared_powers=(
                        weaken_prepared
                        if weaken_prepared is not None
                        else magic_prepared
                    )
                    # Normal compliance rebuilds WORKFIXSTR/WORKFIXTOUGH as
                    # well as attack/defense powers. In this admitted baseline
                    # domain the prepared values are equal; immutable session
                    # stats remain the next preparation's reconstruction input.
                    fixed_strength=(baseline.attack if prepared_powers is None else prepared_powers.attack)
                    fixed_toughness=(baseline.defense if prepared_powers is None else prepared_powers.defense)
                    # The scheduling carrier starts with no asserted historical
                    # LOW(COM3) meaning.  The callback preserves that LOW exactly
                    # and writes only the proved HIGH dodge modifier.
                    submission=resolve_enemy_ai_wildviolent_submission(
                        spawned,
                        skill_slot=int(decision.skill_slot),
                        target_slot=int(decision.target_slot),
                        petskill_runtime=petskill_runtime,
                        fixed_strength=int(fixed_strength),
                        fixed_toughness=int(fixed_toughness),
                        attack_power_before=int(current.attack),
                        defense_power_before=int(current.defense),
                        packed_com3_before=0,
                    )
                    commands[enemy_id]=BattleCommand(
                        BATTLE_COM_ATTACK,
                        command2=int(submission.source_target_slot),
                        command3=int(submission.setup.packed_com3),
                    )
                    setup_effects[enemy_id]=BattleCommandSetupEffects(
                        attack_power=submission.setup.attack_power,
                        defense_power=submission.setup.defense_power,
                    )
                    wildviolent_submissions[enemy_id]=submission
                    continue

                if (
                    selected_skill is not None
                    and selected_skill.function_name == ATTACK_CRAZED_CALLBACK
                    and bool(allow_attack_crazed_skill)
                ):
                    submission=resolve_enemy_ai_attack_crazed_submission(
                        spawned,skill_slot=int(decision.skill_slot),
                        target_slot=int(decision.target_slot),petskill_runtime=petskill_runtime,
                    )
                    # ATTACK is an internal ordering carrier, never a claimed
                    # recovered25 AttackCrazed numeric command.
                    commands[enemy_id]=BattleCommand(BATTLE_COM_ATTACK,command2=submission.source_target_slot)
                    work=submission.callback_setup(fixed_strength=spawned.participant.attack,fixed_toughness=spawned.participant.defense)
                    setup_effects[enemy_id]=BattleCommandSetupEffects(attack_power=work.attack_power,defense_power=work.defense_power)
                    attack_crazed_submissions[enemy_id]=submission
                    continue

                if (
                    selected_skill is not None
                    and selected_skill.function_name == WEAKEN_CALLBACK
                    and bool(allow_weaken_skill)
                ):
                    submission=resolve_enemy_ai_weaken_submission(
                        spawned,
                        skill_slot=int(decision.skill_slot),
                        target_slot=int(decision.target_slot),
                        petskill_runtime=petskill_runtime,
                    )
                    # Scheduling carrier only; native WEAKEN stays symbolic.
                    commands[enemy_id]=BattleCommand(
                        BATTLE_COM_ATTACK,
                        command2=int(submission.source_target_slot),
                    )
                    weaken_submissions[enemy_id]=submission
                    continue

                if (
                    selected_skill is not None
                    and selected_skill.function_name == REFRESH_CALLBACK
                    and bool(allow_refresh_skill)
                ):
                    submission=resolve_enemy_ai_refresh_submission(
                        spawned,
                        skill_slot=int(decision.skill_slot),
                        target_slot=int(decision.target_slot),
                        petskill_runtime=petskill_runtime,
                    )
                    # Internal scheduling carrier only. The fixed source proves
                    # symbolic S_REFRESH but no recovered25 numeric COM1.
                    commands[enemy_id]=BattleCommand(
                        BATTLE_COM_ATTACK,
                        command2=int(submission.source_target_slot),
                    )
                    refresh_submissions[enemy_id]=submission
                    continue

                if (
                    selected_skill is not None
                    and selected_skill.function_name == SETMAGICPET_CALLBACK
                    and bool(allow_setmagicpet_skill)
                ):
                    submission=resolve_enemy_ai_setmagicpet_submission(
                        spawned,
                        skill_slot=int(decision.skill_slot),
                        target_slot=int(decision.target_slot),
                        petskill_runtime=petskill_runtime,
                    )
                    # Internal action-order carrier only. Descendant numeric
                    # S_SETMAGICPET differs by compile profile and is not a
                    # recovered25 COM1 assertion.
                    commands[enemy_id]=BattleCommand(
                        BATTLE_COM_ATTACK,
                        command2=int(submission.source_target_slot),
                    )
                    setmagicpet_submissions[enemy_id]=submission
                    continue

                if (
                    selected_skill is not None
                    and selected_skill.function_name == BARRIER_CALLBACK
                    and bool(allow_barrier_skill)
                ):
                    submission=resolve_enemy_ai_barrier_submission(
                        spawned,
                        skill_slot=int(decision.skill_slot),
                        target_slot=int(decision.target_slot),
                        petskill_runtime=petskill_runtime,
                    )
                    # Internal scheduling carrier only. Pinned source profiles
                    # disagree on numeric BARRIER COM1 (2024 vs 2023), so no
                    # recovered25 historical command number is asserted.
                    commands[enemy_id]=BattleCommand(
                        BATTLE_COM_ATTACK,
                        command2=int(submission.source_target_slot),
                    )
                    barrier_submissions[enemy_id]=submission
                    continue

                if (
                    selected_skill is not None
                    and selected_skill.function_name == GUARD_BREAK2_CALLBACK
                    and bool(allow_guard_break2_skill)
                ):
                    submission=resolve_enemy_ai_guard_break2_submission(
                        spawned,
                        skill_slot=int(decision.skill_slot),
                        target_slot=int(decision.target_slot),
                        petskill_runtime=petskill_runtime,
                    )
                    # Internal scheduling carrier only. The fixed-source
                    # command symbol is proven, but no recovered25 numeric
                    # COM1 mapping is asserted.
                    commands[enemy_id]=BattleCommand(
                        BATTLE_COM_ATTACK,
                        command2=int(submission.source_target_slot),
                    )
                    guard_break2_submissions[enemy_id]=submission
                    continue

                if (
                    selected_skill is not None
                    and selected_skill.function_name == VARY_CALLBACK
                    and bool(allow_vary_skill)
                ):
                    if enemy_id not in vary_profiles:
                        raise ValueError(
                            "Vary requires explicit descendant profile for "
                            + enemy_id
                        )
                    if (
                        state.vary_overlay is not None
                        and enemy_id
                        in state.vary_overlay.runtime_by_participant_id
                    ):
                        raise ValueError(
                            "Vary recast blocked while actor is transformed"
                        )
                    baseline=living[enemy_id]
                    submission=resolve_enemy_ai_vary_submission(
                        spawned,
                        skill_slot=int(decision.skill_slot),
                        target_carrier=int(decision.target_slot),
                        petskill_runtime=petskill_runtime,
                        profile=vary_profiles[enemy_id],
                        fixed_attack=int(baseline.attack),
                        fixed_defense=int(baseline.defense),
                        fixed_quick=int(baseline.quick),
                    )
                    commands[enemy_id]=BattleCommand(
                        BATTLE_COM_ATTACK,
                        command2=int(submission.source_target_carrier),
                    )
                    vary_submissions[enemy_id]=submission
                    continue

                if (
                    selected_skill is not None
                    and selected_skill.function_name == COMBINED_CALLBACK
                    and bool(allow_combined_skill)
                ):
                    if enemy_id not in combined_selection_draws:
                        raise ValueError(
                            "Combined callback selection requires explicit "
                            "reduced draw for " + enemy_id
                        )
                    submission=resolve_enemy_ai_combined_submission(
                        spawned,
                        skill_slot=int(decision.skill_slot),
                        target_slot=int(decision.target_slot),
                        petskill_runtime=petskill_runtime,
                        draw_index=int(combined_selection_draws[enemy_id]),
                    )
                    commands[enemy_id]=BattleCommand(
                        BATTLE_COM_ATTACK,
                        command2=int(submission.source_target_slot),
                    )
                    combined_submissions[enemy_id]=submission
                    continue

                if (
                    selected_skill is not None
                    and selected_skill.function_name == BATTLETIMID_CALLBACK
                    and bool(allow_battletimid_skill)
                ):
                    baseline=living[enemy_id]
                    weaken_prepared=(
                        None if state.nocast_overlay is None else
                        state.nocast_overlay.runtime_by_participant_id[
                            enemy_id
                        ].prepared_weaken_powers
                    )
                    if weaken_prepared is not None:
                        raise ValueError(
                            "BattleTimid with prepared Weaken powers is outside R1"
                        )
                    magic_prepared=(
                        None if state.setmagicpet_overlay is None else
                        state.setmagicpet_overlay.runtime_by_participant_id[
                            enemy_id
                        ].prepared_powers
                    )
                    fixed_strength=(
                        int(baseline.attack)
                        if magic_prepared is None
                        else int(magic_prepared.attack)
                    )
                    fixed_toughness=(
                        int(baseline.defense)
                        if magic_prepared is None
                        else int(magic_prepared.defense)
                    )
                    fixed_dex=(
                        int(baseline.quick)
                        if magic_prepared is None
                        else int(magic_prepared.dexterity)
                    )
                    submission=resolve_enemy_ai_battletimid_submission(
                        spawned,
                        skill_slot=int(decision.skill_slot),
                        target_slot=int(decision.target_slot),
                        petskill_runtime=petskill_runtime,
                        fixed_strength=fixed_strength,
                        fixed_toughness=fixed_toughness,
                        fixed_dex=fixed_dex,
                    )
                    commands[enemy_id]=BattleCommand(
                        BATTLE_COM_ATTACK,
                        command2=int(submission.source_target_slot),
                    )
                    setup_effects[enemy_id]=BattleCommandSetupEffects(
                        attack_power=int(submission.setup.attack_power),
                        defense_power=int(submission.setup.defence_power),
                    )
                    battletimid_submissions[enemy_id]=submission
                    continue

                if (
                    selected_skill is not None
                    and selected_skill.function_name == LIGHTTAKEED_CALLBACK
                    and bool(allow_lighttakeed_skill)
                ):
                    if enemy_id not in lighttakeed_profiles:
                        raise ValueError(
                            "Lighttakeed callback requires explicit descendant "
                            "profile for " + enemy_id
                        )
                    baseline=living[enemy_id]
                    weaken_prepared=(
                        None if state.nocast_overlay is None else
                        state.nocast_overlay.runtime_by_participant_id[
                            enemy_id
                        ].prepared_weaken_powers
                    )
                    if weaken_prepared is not None:
                        raise ValueError(
                            "Lighttakeed with prepared Weaken powers is outside R1"
                        )
                    magic_prepared=(
                        None if state.setmagicpet_overlay is None else
                        state.setmagicpet_overlay.runtime_by_participant_id[
                            enemy_id
                        ].prepared_powers
                    )
                    if magic_prepared is not None:
                        raise ValueError(
                            "Lighttakeed with prepared SetMagicPet powers is outside R1"
                        )
                    submission=resolve_enemy_ai_lighttakeed_submission(
                        spawned,
                        skill_slot=int(decision.skill_slot),
                        target_slot=int(decision.target_slot),
                        petskill_runtime=petskill_runtime,
                        profile=lighttakeed_profiles[enemy_id],
                        fixed_strength=int(baseline.attack),
                        fixed_toughness=int(baseline.defense),
                    )
                    commands[enemy_id]=BattleCommand(
                        BATTLE_COM_ATTACK,
                        command2=int(submission.source_target_slot),
                    )
                    setup_effects[enemy_id]=BattleCommandSetupEffects(
                        attack_power=int(submission.attack_power),
                        defense_power=int(submission.defense_power),
                    )
                    lighttakeed_submissions[enemy_id]=submission
                    continue

                if (
                    selected_skill is not None
                    and selected_skill.function_name == NOCAST_CALLBACK
                    and bool(allow_nocast_skill)
                ):
                    submission=resolve_enemy_ai_nocast_submission(
                        spawned,
                        skill_slot=int(decision.skill_slot),
                        target_slot=int(decision.target_slot),
                        petskill_runtime=petskill_runtime,
                    )
                    # Internal scheduling carrier only. The guarded reference
                    # does not prove a recovered25 numeric Nocast COM1.
                    commands[enemy_id]=BattleCommand(
                        BATTLE_COM_ATTACK,
                        command2=int(submission.source_target_slot),
                    )
                    nocast_submissions[enemy_id]=submission
                    continue

                if (
                    selected_skill is not None
                    and selected_skill.function_name == BATTLE_TEAR_CALLBACK
                    and bool(allow_battle_tear_skill)
                ):
                    submission=resolve_enemy_ai_battle_tear_submission(
                        spawned,
                        skill_slot=int(decision.skill_slot),
                        target_slot=int(decision.target_slot),
                        petskill_runtime=petskill_runtime,
                    )
                    commands[enemy_id]=BattleCommand(
                        BATTLE_COM_ATTACK,
                        command2=int(submission.source_target_slot),
                    )
                    callback_setup=submission.callback_setup(
                        fixed_strength=int(spawned.participant.attack),
                        fixed_toughness=int(spawned.participant.defense),
                    )
                    setup_effects[enemy_id]=BattleCommandSetupEffects(
                        attack_power=int(callback_setup.attack_power),
                        defense_power=int(callback_setup.defense_power),
                    )
                    battle_tear_submissions[enemy_id]=submission
                    continue

                if (
                    selected_skill is not None
                    and selected_skill.function_name == FALL_GROUND_CALLBACK
                    and bool(allow_fall_ground_skill)
                ):
                    submission=resolve_enemy_ai_fall_ground_submission(
                        spawned,
                        skill_slot=int(decision.skill_slot),
                        target_slot=int(decision.target_slot),
                        petskill_runtime=petskill_runtime,
                    )
                    commands[enemy_id]=BattleCommand(
                        BATTLE_COM_ATTACK,
                        command2=int(submission.source_target_slot),
                    )
                    # Fixed callback mutates WORKATTACKPOWER at submission
                    # time, before later status/confusion execution checks.
                    setup_effects[enemy_id]=BattleCommandSetupEffects(
                        attack_power=submission.callback_attack_power(
                            int(spawned.participant.attack)
                        )
                    )
                    fall_ground_submissions[enemy_id]=submission
                    continue

                if (
                    selected_skill is not None
                    and selected_skill.function_name == MP_DAMAGE_CALLBACK
                    and bool(allow_mp_damage_skill)
                ):
                    submission=resolve_enemy_ai_mp_damage_submission(
                        spawned,
                        skill_slot=int(decision.skill_slot),
                        target_slot=int(decision.target_slot),
                        petskill_runtime=petskill_runtime,
                    )
                    commands[enemy_id]=BattleCommand(
                        BATTLE_COM_ATTACK,
                        command2=int(submission.source_target_slot),
                    )
                    mp_damage_submissions[enemy_id]=submission
                    continue

                if (
                    selected_skill is not None
                    and selected_skill.function_name == DAMAGE_TO_HP_CALLBACK
                    and bool(allow_damage_to_hp_skill)
                ):
                    submission=resolve_enemy_ai_damage_to_hp_submission(
                        spawned,
                        skill_slot=int(decision.skill_slot),
                        target_slot=int(decision.target_slot),
                        petskill_runtime=petskill_runtime,
                    )
                    commands[enemy_id]=BattleCommand(
                        BATTLE_COM_ATTACK,
                        command2=int(submission.source_target_slot),
                    )
                    damage_to_hp_submissions[enemy_id]=submission
                    continue

                if (
                    selected_skill is not None
                    and selected_skill.function_name == ENEMY_REHP_CALLBACK
                    and bool(allow_rehp_skill)
                ):
                    submission=resolve_enemy_ai_rehp_submission(
                        spawned,
                        skill_slot=int(decision.skill_slot),
                        target_slot=int(decision.target_slot),
                        petskill_runtime=petskill_runtime,
                    )
                    # Modern internal ordering carrier only. It is not a
                    # historical assertion that ReHP COM1 == ATTACK.
                    commands[enemy_id]=BattleCommand(
                        BATTLE_COM_ATTACK,
                        command2=int(submission.source_target_slot),
                    )
                    enemy_rehp_submissions[enemy_id]=submission
                    continue

                if (
                    selected_skill is not None
                    and selected_skill.function_name == ENEMY_RELIFE_CALLBACK
                    and bool(allow_relife_skill)
                ):
                    submission=resolve_enemy_ai_relife_submission(
                        spawned,
                        skill_slot=int(decision.skill_slot),
                        target_slot=int(decision.target_slot),
                        petskill_runtime=petskill_runtime,
                    )
                    # Internal ATTACK is only the source COM2/initiative and
                    # physical-fallback carrier. ReLife itself stays symbolic.
                    commands[enemy_id]=BattleCommand(
                        BATTLE_COM_ATTACK,
                        command2=int(
                            submission.source_attack_target_slot
                        ),
                    )
                    enemy_relife_submissions[enemy_id]=submission
                    continue

                if (
                    selected_skill is not None
                    and selected_skill.function_name == ATTACK_MAGIC_CALLBACK
                    and bool(allow_attackmagic_skill)
                ):
                    attack_magic_runtime=getattr(
                        self.stack,"attack_magic_runtime",None
                    )
                    if attack_magic_runtime is None:
                        raise ValueError(
                            "enemy AI AttackMagic selection requires recovered "
                            "AttackMagic runtime"
                        )
                    submission=resolve_enemy_ai_attack_magic_submission(
                        spawned,
                        skill_slot=int(decision.skill_slot),
                        target_slot=int(decision.target_slot),
                        petskill_runtime=petskill_runtime,
                        attack_magic_runtime=attack_magic_runtime,
                    )
                    commands[enemy_id]=BattleCommand(
                        int(submission.command.command1),
                        command2=int(submission.command.command2),
                        command3=int(submission.command.command3),
                    )
                    attack_magic_submissions[enemy_id]=submission
                    continue

                bridged = resolve_enemy_ai_supported_petskill_command(
                    spawned,
                    skill_slot=int(decision.skill_slot),
                    target_slot=int(decision.target_slot),
                    petskill_runtime=petskill_runtime,
                    actor_slot=int(state.slots[enemy_id]),
                    allow_status_change=bool(allow_statuschange_skill),
                    allow_power_balance=bool(allow_powerbalance_skill),
                    allow_mighty=bool(allow_mighty_skill),
                    allow_guard_break=bool(allow_guardbreak_skill),
                    allow_guardian=bool(allow_guardian_skill),
                    allow_continuation_attack=bool(
                        allow_continuationattack_skill
                    ),
                    allow_charge_attack=bool(allow_chargeattack_skill),
                    allow_no_guard=bool(allow_noguard_skill),
                    allow_abduct=bool(allow_abduct_skill),
                    allow_earth_round=bool(allow_earthround_skill),
                    allow_steal=bool(allow_steal_skill),
                )
                commands[enemy_id] = bridged.command
                if bridged.setup_effects != BattleCommandSetupEffects():
                    setup_effects[enemy_id] = bridged.setup_effects
                if bridged.abduct_ai_threshold is not None:
                    abduct_contexts[enemy_id]=OrdinaryAbductContext(
                        skill_array=int(bridged.skill_id),
                        ai_threshold=int(bridged.abduct_ai_threshold),
                        # Local reconstructed ordinary group battles have no
                        # event WinFunc seam; special WinFunc battles remain
                        # outside this coordinator subset.
                        has_win_func=False,
                    )
                continue
            allowed_parts = ["ATTACK", "GUARD"]
            if bool(allow_escape):
                allowed_parts.append("ESCAPE")
            if bool(allow_basic_skill):
                allowed_parts.append("basic-petskill")
            if bool(allow_statuschange_skill):
                allowed_parts.append("StatusChange")
            if bool(allow_powerbalance_skill):
                allowed_parts.append("PowerBalance")
            if bool(allow_mighty_skill):
                allowed_parts.append("Mighty")
            if bool(allow_guardbreak_skill):
                allowed_parts.append("GuardBreak")
            if bool(allow_guardian_skill):
                allowed_parts.append("Guardian")
            if bool(allow_continuationattack_skill):
                allowed_parts.append("ContinuationAttack")
            if bool(allow_chargeattack_skill):
                allowed_parts.append("ChargeAttack")
            if bool(allow_noguard_skill):
                allowed_parts.append("NoGuard")
            if bool(allow_abduct_skill):
                allowed_parts.append("Abduct")
            if bool(allow_earthround_skill):
                allowed_parts.append("EarthRound")
            if bool(allow_steal_skill):
                allowed_parts.append("Steal")
            if bool(allow_attackmagic_skill):
                allowed_parts.append("AttackMagic")
            if bool(allow_rehp_skill):
                allowed_parts.append("ENEMYSKILL_ReHP")
            if bool(allow_relife_skill):
                allowed_parts.append("ENEMYSKILL_ReLife")
            if bool(allow_damage_to_hp_skill):
                allowed_parts.append("PETSKILL_DamageToHp")
            if bool(allow_mp_damage_skill):
                allowed_parts.append("PETSKILL_MpDamage")
            if bool(allow_fall_ground_skill):
                allowed_parts.append("PETSKILL_FallGround")
            if bool(allow_battle_tear_skill):
                allowed_parts.append("PETSKILL_BattleTearDamage")
            if bool(allow_nocast_skill):
                allowed_parts.append("PETSKILL_Nocast")
            if bool(allow_guard_break2_skill):
                allowed_parts.append("PETSKILL_GuardBreak2")
            if bool(allow_battletimid_skill):
                allowed_parts.append("PETSKILL_BattleTimid")
            if bool(allow_lighttakeed_skill):
                allowed_parts.append("PETSKILL_Lighttakeed")
            if bool(allow_combined_skill):
                allowed_parts.append("PETSKILL_Combined")
            if bool(allow_vary_skill):
                allowed_parts.append("PETSKILL_Vary")
            if bool(allow_weaken_skill):
                allowed_parts.append("PETSKILL_Weaken")
            if bool(allow_refresh_skill):
                allowed_parts.append("PETSKILL_Refresh")
            if bool(allow_setmagicpet_skill):
                allowed_parts.append("PETSKILL_SetMagicPet")
            if bool(allow_barrier_skill):
                allowed_parts.append("PETSKILL_Barrier")
            if bool(allow_modifyattack_skill):
                allowed_parts.append("PETSKILL_Modifyattack")
            if bool(allow_mdfyattack_skill):
                allowed_parts.append("PETSKILL_Mdfyattack")
            if bool(allow_attack_crazed_skill):
                allowed_parts.append("PETSKILL_AttackCrazed")
            if bool(allow_wildviolent_skill):
                allowed_parts.append("PETSKILL_WildViolentAttack")
            allowed = "/".join(allowed_parts)
            raise ValueError(
                "enemy AI selected command outside coordinator "
                f"{allowed} subset: {enemy_id}:{decision.kind}"
            )

        unused_lighttakeed_profiles=sorted(
            set(lighttakeed_profiles)-set(lighttakeed_submissions)
        )
        if unused_lighttakeed_profiles:
            raise ValueError(
                "Lighttakeed profile supplied for non-selected actors: "
                + ",".join(unused_lighttakeed_profiles)
            )

        unused_combined_draws=sorted(
            set(combined_selection_draws)-set(combined_submissions)
        )
        if unused_combined_draws:
            raise ValueError(
                "Combined selection RNG supplied for non-selected actors: "
                + ",".join(unused_combined_draws)
            )
        unused_vary_profiles=sorted(
            set(vary_profiles)-set(vary_submissions)
        )
        if unused_vary_profiles:
            raise ValueError(
                "Vary profile supplied for non-selected actors: "
                + ",".join(unused_vary_profiles)
            )

        return EnemyAiCommonCommandBatch(
            commands=commands,
            setup_effects=setup_effects,
            abduct_contexts=abduct_contexts,
            attack_magic_submissions=attack_magic_submissions,
            enemy_rehp_submissions=enemy_rehp_submissions,
            enemy_relife_submissions=enemy_relife_submissions,
            damage_to_hp_submissions=damage_to_hp_submissions,
            mp_damage_submissions=mp_damage_submissions,
            fall_ground_submissions=fall_ground_submissions,
            battle_tear_submissions=battle_tear_submissions,
            nocast_submissions=nocast_submissions,
            guard_break2_submissions=guard_break2_submissions,
            battletimid_submissions=battletimid_submissions,
            lighttakeed_submissions=lighttakeed_submissions,
            combined_submissions=combined_submissions,
            vary_submissions=vary_submissions,
            weaken_submissions=weaken_submissions,
            refresh_submissions=refresh_submissions,
            setmagicpet_submissions=setmagicpet_submissions,
            barrier_submissions=barrier_submissions,
            modifyattack_submissions=modifyattack_submissions,
            mdfyattack_submissions=mdfyattack_submissions,
            attack_crazed_submissions=attack_crazed_submissions,
            wildviolent_submissions=wildviolent_submissions,
        )

    def build_persistent_enemy_common_commands(
        self,
        context: LocalRuntimeBattleContext,
        *,
        mode_rolls_by_enemy_id: Mapping[str, int],
        target_rolls_by_enemy_id: Mapping[str, int] | None = None,
        allow_escape: bool = False,
        allow_basic_skill: bool = False,
    ) -> Mapping[str, BattleCommand]:
        """Backward-compatible commands-only view of the common AI batch."""

        return self._build_persistent_enemy_common_batch(
            context,
            mode_rolls_by_enemy_id=mode_rolls_by_enemy_id,
            target_rolls_by_enemy_id=target_rolls_by_enemy_id,
            allow_escape=allow_escape,
            allow_basic_skill=allow_basic_skill,
            allow_statuschange_skill=False,
            allow_powerbalance_skill=False,
            allow_mighty_skill=False,
            allow_guardbreak_skill=False,
            allow_guardian_skill=False,
            allow_chargeattack_skill=False,
            allow_noguard_skill=False,
            allow_abduct_skill=False,
            allow_earthround_skill=False,
            allow_steal_skill=False,
            allow_attackmagic_skill=False,
            allow_wildviolent_skill=False,
        ).commands

    def build_persistent_enemy_attack_guard_commands(
        self,
        context: LocalRuntimeBattleContext,
        *,
        mode_rolls_by_enemy_id: Mapping[str, int],
        target_rolls_by_enemy_id: Mapping[str, int] | None = None,
    ) -> Mapping[str, BattleCommand]:
        """Backward-compatible ATTACK/GUARD-only enemy-AI boundary."""

        return self.build_persistent_enemy_common_commands(
            context,
            mode_rolls_by_enemy_id=mode_rolls_by_enemy_id,
            target_rolls_by_enemy_id=target_rolls_by_enemy_id,
            allow_escape=False,
            allow_basic_skill=False,
        )

    def resolve_persistent_attack_guard_wait_round_with_enemy_ai(
        self,
        context: LocalRuntimeBattleContext,
        *,
        player_side_commands: Mapping[str, BattleCommand],
        enemy_mode_rolls: Mapping[str, int],
        enemy_target_rolls: Mapping[str, int] | None,
        initiative_random_subtracts: Mapping[str, int],
        profiles: Mapping[str, BattleCombatProfile],
        attack_rolls: Mapping[str, OrdinaryAttackRolls],
        defense_profile: str,
        no_risk: bool = False,
        field_attr: str = "none",
        field_power: int = 0,
        tie_break_order: Sequence[str] | None = None,
    ) -> tuple[LocalRuntimeBattleContext, PersistentRoundResult]:
        """Advance one ATTACK/GUARD/WAIT round with recovered enemy AI.

        Player-side commands remain explicit. Enemy commands are derived from
        each spawned variant's recovered TACTICS/TACTICSOPTION with explicit
        caller-provided AI rolls.
        """

        state = context.persistent_battle_state
        if state is None:
            raise ValueError("battle context has no persistent battle state")

        living_player_side_ids = {
            str(participant.participant_id)
            for participant in (
                state.session.player,
                *state.session.allied_pets,
            )
            if (
                str(participant.participant_id)
                in state.hp_by_participant_id
                and str(participant.participant_id)
                not in set(state.ultimate_exited_participant_ids)
                and str(participant.participant_id)
                not in set(state.battle_exited_participant_ids)
                and int(
                    state.hp_by_participant_id[
                        str(participant.participant_id)
                    ]
                ) > 0
            )
        }
        normalized_player_commands = {
            str(key): value
            for key, value in player_side_commands.items()
        }
        if set(normalized_player_commands) != living_player_side_ids:
            missing = sorted(
                living_player_side_ids - set(normalized_player_commands)
            )
            extra = sorted(
                set(normalized_player_commands) - living_player_side_ids
            )
            raise ValueError(
                "player-side commands must cover exactly living player-side "
                f"actors; missing={missing}, extra={extra}"
            )

        enemy_commands = self.build_persistent_enemy_attack_guard_commands(
            context,
            mode_rolls_by_enemy_id=enemy_mode_rolls,
            target_rolls_by_enemy_id=enemy_target_rolls,
        )
        commands = {
            **normalized_player_commands,
            **dict(enemy_commands),
        }
        return self.resolve_persistent_attack_wait_round(
            context,
            commands=commands,
            initiative_random_subtracts=initiative_random_subtracts,
            profiles=profiles,
            attack_rolls=attack_rolls,
            defense_profile=defense_profile,
            no_risk=no_risk,
            field_attr=field_attr,
            field_power=field_power,
            tie_break_order=tie_break_order,
        )

    def resolve_persistent_attack_guard_escape_wait_round_with_enemy_ai(
        self,
        context: LocalRuntimeBattleContext,
        *,
        player_side_commands: Mapping[str, BattleCommand],
        enemy_mode_rolls: Mapping[str, int],
        enemy_target_rolls: Mapping[str, int] | None,
        enemy_escape_rolls: Mapping[str, OrdinaryEscapeRolls],
        opponent_abio_by_participant_id: Mapping[str, bool],
        initiative_random_subtracts: Mapping[str, int],
        profiles: Mapping[str, BattleCombatProfile],
        attack_rolls: Mapping[str, OrdinaryAttackRolls],
        defense_profile: str,
        counter_rolls_by_attack_id: Mapping[
            str, Sequence[CounterAttemptRolls]
        ] | None = None,
        attack_crazed_rolls_by_attack_id: Mapping[str,AttackCrazedRolls] | None = None,
        wildviolent_rolls_by_attack_id: Mapping[str,WildViolentRolls] | None = None,
        continuation_rolls_by_attack_id: Mapping[
            str, ContinuationAttackRolls
        ] | None = None,
        abduct_rolls_by_attack_id: Mapping[
            str, OrdinaryAbductRolls
        ] | None = None,
        steal_rolls_by_attack_id: Mapping[
            str, OrdinaryStealRolls
        ] | None = None,
        counter_abio_by_participant_id: Mapping[str, bool] | None = None,
        base_status_rolls_by_participant_id: Mapping[
            str, BaseStatusTurnRolls
        ] | None = None,
        base_status_combat_profiles_by_participant_id: Mapping[
            str, BaseStatusCombatProfile
        ] | None = None,
        status_application_rolls_by_attack_id: Mapping[str, int] | None = None,
        attack_magic_rolls_by_attack_id: Mapping[
            str,EnemyAttackMagicActionRolls
        ] | None = None,
        attack_magic_retarget_rolls_by_attack_id: Mapping[
            str,Sequence[int]
        ] | None = None,
        enemy_rehp_rolls_by_attack_id: Mapping[
            str,EnemyReHpRolls
        ] | None = None,
        enemy_rehp_retarget_rolls_by_attack_id: Mapping[
            str,int | None
        ] | None = None,
        enemy_relife_rolls_by_attack_id: Mapping[
            str,EnemyReLifeRolls
        ] | None = None,
        enemy_relife_retarget_rolls_by_attack_id: Mapping[
            str,int | None
        ] | None = None,
        fall_ground_rolls_by_attack_id: Mapping[
            str,int | None
        ] | None = None,
        fall_ground_equipment_resistance_by_participant_id: Mapping[
            str,int
        ] | None = None,
        nocast_rolls_by_attack_id: Mapping[
            str,NocastActionRolls
        ] | None = None,
        weaken_rolls_by_attack_id: Mapping[str,WeakenActionRolls] | None = None,
        refresh_rolls_by_attack_id: Mapping[str,RefreshActionRolls] | None = None,
        setmagicpet_rolls_by_attack_id: Mapping[
            str,SetMagicPetActionRolls
        ] | None = None,
        battletimid_rolls_by_attack_id: Mapping[
            str,int | None
        ] | None = None,
        modifyattack_rand_by_attack_id: Mapping[str,int | None] | None = None,
        lighttakeed_profiles_by_enemy_id: Mapping[
            str,str
        ] | None = None,
        combined_selection_draws_by_enemy_id: Mapping[
            str,int
        ] | None = None,
        combined_rolls_by_attack_id: Mapping[
            str,CombinedActionRolls
        ] | None = None,
        vary_profiles_by_enemy_id: Mapping[
            str,str
        ] | None = None,
        barrier_rolls_by_attack_id: Mapping[
            str,BarrierActionRolls
        ] | None = None,
        no_risk: bool = False,
        field_attr: str = "none",
        field_power: int = 0,
        tie_break_order: Sequence[str] | None = None,
    ) -> tuple[LocalRuntimeBattleContext, PersistentRoundResult]:
        """Advance the currently executable common enemy-AI round.

        ATTACK/GUARD are direct. ESCAPE uses recovered enemybase RARE plus
        explicit RAND/ABIO inputs. wa slots admit None/NormalAttack/NormalGuard
        plus recovered Abduct, AttackMagic, ENEMYSKILL_ReHP, ENEMYSKILL_ReLife, PETSKILL_DamageToHp, PETSKILL_MpDamage, PETSKILL_FallGround, ChargeAttack, ContinuationAttack,
        EarthRound, GuardBreak, Mighty, NoGuard, PowerBalance, StatusChange and
        Steal.
        Steal mutates only the working persistent player Gold/inventory clone
        and uses explicit sub-rolls. EarthRound
        carries phase 1 into S_EARTHROUND0 without a fresh AI roll, then uses
        ordinary physical RNG on phase 2. Abduct carries the recovered OPTION
        atoi threshold and explicit RAND input. NoGuard keeps S_NOGUARD selected for its
        own NoAction turn so later same-round dodge/counter checks can consume
        COM3; ChargeAttack carries its countdown across rounds. GuardBreak
        preserves its dedicated guard-only hit gate and source-shaped Guardian
        settlement quirk; Mighty preserves packed damage-multiplier / dodge
        modifiers; PowerBalance carries immediate work attack/defense setup
        effects; StatusChange keeps setup effects and all status/application RNG
        explicit. Every other callback remains fail-closed.
        """

        state = context.persistent_battle_state
        if state is None:
            raise ValueError("battle context has no persistent battle state")
        if state.phase != "active":
            raise ValueError("cannot execute another round after battle termination")

        living_player_side_ids = {
            str(participant.participant_id)
            for participant in (
                state.session.player,
                *state.session.allied_pets,
            )
            if (
                str(participant.participant_id)
                in state.hp_by_participant_id
                and str(participant.participant_id)
                not in set(state.ultimate_exited_participant_ids)
                and str(participant.participant_id)
                not in set(state.battle_exited_participant_ids)
                and int(
                    state.hp_by_participant_id[
                        str(participant.participant_id)
                    ]
                ) > 0
            )
        }
        normalized_player_commands = {
            str(key): value
            for key, value in player_side_commands.items()
        }
        if set(normalized_player_commands) != living_player_side_ids:
            missing = sorted(
                living_player_side_ids - set(normalized_player_commands)
            )
            extra = sorted(
                set(normalized_player_commands) - living_player_side_ids
            )
            raise ValueError(
                "player-side commands must cover exactly living player-side "
                f"actors; missing={missing}, extra={extra}"
            )
        invalid_player_commands = tuple(
            sorted(
                participant_id
                for participant_id, command
                in normalized_player_commands.items()
                if not isinstance(command, BattleCommand)
                or int(command.command1)
                not in {BATTLE_COM_ATTACK, BATTLE_COM_GUARD, BATTLE_COM_WAIT}
            )
        )
        if invalid_player_commands:
            raise ValueError(
                "enemy-AI escape round accepts player-side "
                "ATTACK/GUARD/WAIT only: "
                + ",".join(invalid_player_commands)
            )

        enemy_batch = self._build_persistent_enemy_common_batch(
            context,
            mode_rolls_by_enemy_id=enemy_mode_rolls,
            target_rolls_by_enemy_id=enemy_target_rolls,
            allow_escape=True,
            allow_basic_skill=True,
            allow_statuschange_skill=True,
            allow_powerbalance_skill=True,
            allow_mighty_skill=True,
            allow_guardbreak_skill=True,
            allow_guardian_skill=True,
            allow_continuationattack_skill=True,
            allow_chargeattack_skill=True,
            allow_noguard_skill=True,
            allow_abduct_skill=True,
            allow_earthround_skill=True,
            allow_steal_skill=True,
            allow_attackmagic_skill=True,
            allow_rehp_skill=True,
            allow_relife_skill=True,
            allow_damage_to_hp_skill=True,
            allow_mp_damage_skill=True,
            allow_fall_ground_skill=True,
            allow_battle_tear_skill=True,
            allow_nocast_skill=True,
            allow_guard_break2_skill=True,
            allow_battletimid_skill=True,
            allow_lighttakeed_skill=True,
            lighttakeed_profiles_by_enemy_id=(
                lighttakeed_profiles_by_enemy_id
            ),
            allow_combined_skill=True,
            combined_selection_draws_by_enemy_id=(
                combined_selection_draws_by_enemy_id
            ),
            allow_vary_skill=True,
            vary_profiles_by_enemy_id=vary_profiles_by_enemy_id,
            allow_weaken_skill=True,
            allow_refresh_skill=True,
            allow_setmagicpet_skill=True,
            allow_barrier_skill=True,
            allow_modifyattack_skill=True,
            allow_mdfyattack_skill=True,
            allow_attack_crazed_skill=True,
            allow_wildviolent_skill=True,
        )
        enemy_commands = enemy_batch.commands
        normalized_wildviolent_rolls={
            str(key):value
            for key,value in (wildviolent_rolls_by_attack_id or {}).items()
        }
        unexpected_wild=sorted(
            set(normalized_wildviolent_rolls)
            - set(enemy_batch.wildviolent_submissions)
        )
        if unexpected_wild:
            raise ValueError(
                "enemy WildViolentAttack RNG references non-selected actors: "
                + ",".join(unexpected_wild)
            )
        if not all(
            isinstance(value,WildViolentRolls)
            for value in normalized_wildviolent_rolls.values()
        ):
            raise TypeError("enemy WildViolentAttack RNG wrong type")
        normalized_attack_crazed_rolls=dict(attack_crazed_rolls_by_attack_id or {})
        if set(normalized_attack_crazed_rolls)!=set(enemy_batch.attack_crazed_submissions):
            raise ValueError("enemy AttackCrazed RNG actors mismatch")
        if not all(isinstance(v,AttackCrazedRolls) for v in normalized_attack_crazed_rolls.values()):
            raise TypeError("enemy AttackCrazed RNG wrong type")
        combined_enemy_ids=set(enemy_batch.combined_submissions)
        normalized_combined_rolls={
            str(key):value
            for key,value in (combined_rolls_by_attack_id or {}).items()
        }
        if set(normalized_combined_rolls)!=combined_enemy_ids:
            missing=sorted(
                combined_enemy_ids-set(normalized_combined_rolls)
            )
            extra=sorted(
                set(normalized_combined_rolls)-combined_enemy_ids
            )
            raise ValueError(
                "enemy Combined action RNG actors mismatch; "
                f"missing={missing}, extra={extra}"
            )
        if any(
            not isinstance(value,CombinedActionRolls)
            for value in normalized_combined_rolls.values()
        ):
            raise TypeError("enemy Combined action RNG wrong type")

        normalized_modifyattack_rand={str(key):value for key,value in (modifyattack_rand_by_attack_id or {}).items()}
        if set(normalized_modifyattack_rand)!=set(enemy_batch.modifyattack_submissions):
            raise ValueError("enemy Modifyattack helper RNG actors mismatch")
        if any(value is not None and (type(value) is not int or not 0<=value<2**31) for value in normalized_modifyattack_rand.values()):
            raise ValueError("enemy Modifyattack requires raw nonnegative signed-int rand")

        battletimid_enemy_ids=set(enemy_batch.battletimid_submissions)
        normalized_battletimid_rolls={
            str(key):(None if value is None else int(value))
            for key,value in (
                battletimid_rolls_by_attack_id or {}
            ).items()
        }
        if set(normalized_battletimid_rolls)!=battletimid_enemy_ids:
            missing=sorted(
                battletimid_enemy_ids-set(normalized_battletimid_rolls)
            )
            extra=sorted(
                set(normalized_battletimid_rolls)-battletimid_enemy_ids
            )
            raise ValueError(
                "enemy BattleTimid RNG actors mismatch; "
                f"missing={missing}, extra={extra}"
            )
        if any(
            value is not None and not 0 <= int(value) <= 99
            for value in normalized_battletimid_rolls.values()
        ):
            raise ValueError("enemy BattleTimid reduced rand draw must be 0..99")

        rehp_enemy_ids=set(enemy_batch.enemy_rehp_submissions)
        normalized_rehp_rolls={
            str(key):value
            for key,value in (enemy_rehp_rolls_by_attack_id or {}).items()
        }
        if set(normalized_rehp_rolls) != rehp_enemy_ids:
            missing=sorted(rehp_enemy_ids-set(normalized_rehp_rolls))
            extra=sorted(set(normalized_rehp_rolls)-rehp_enemy_ids)
            raise ValueError(
                "enemy ReHP effect RNG mismatch; "
                f"missing={missing}, extra={extra}"
            )
        for participant_id,rolls in normalized_rehp_rolls.items():
            if not isinstance(rolls,EnemyReHpRolls):
                raise TypeError(
                    f"enemy ReHP RNG has wrong type for {participant_id}"
                )
        normalized_rehp_retarget_rolls={
            str(key):(None if value is None else int(value))
            for key,value in (
                enemy_rehp_retarget_rolls_by_attack_id or {}
            ).items()
        }
        if set(normalized_rehp_retarget_rolls) != rehp_enemy_ids:
            missing=sorted(rehp_enemy_ids-set(normalized_rehp_retarget_rolls))
            extra=sorted(set(normalized_rehp_retarget_rolls)-rehp_enemy_ids)
            raise ValueError(
                "enemy ReHP TargetAdjust RNG mismatch; "
                f"missing={missing}, extra={extra}"
            )

        relife_enemy_ids=set(enemy_batch.enemy_relife_submissions)
        normalized_relife_rolls={
            str(key):value
            for key,value in (enemy_relife_rolls_by_attack_id or {}).items()
        }
        if set(normalized_relife_rolls) != relife_enemy_ids:
            missing=sorted(relife_enemy_ids-set(normalized_relife_rolls))
            extra=sorted(set(normalized_relife_rolls)-relife_enemy_ids)
            raise ValueError(
                "enemy ReLife effect RNG mismatch; "
                f"missing={missing}, extra={extra}"
            )
        for participant_id,rolls in normalized_relife_rolls.items():
            if not isinstance(rolls,EnemyReLifeRolls):
                raise TypeError(
                    f"enemy ReLife RNG has wrong type for {participant_id}"
                )
        normalized_relife_retarget_rolls={
            str(key):(None if value is None else int(value))
            for key,value in (
                enemy_relife_retarget_rolls_by_attack_id or {}
            ).items()
        }
        if set(normalized_relife_retarget_rolls) != relife_enemy_ids:
            missing=sorted(
                relife_enemy_ids-set(normalized_relife_retarget_rolls)
            )
            extra=sorted(
                set(normalized_relife_retarget_rolls)-relife_enemy_ids
            )
            raise ValueError(
                "enemy ReLife TargetAdjust RNG mismatch; "
                f"missing={missing}, extra={extra}"
            )

        fall_ground_enemy_ids=set(
            enemy_batch.fall_ground_submissions
        )
        normalized_fall_ground_rolls={
            str(key):(None if value is None else int(value))
            for key,value in (
                fall_ground_rolls_by_attack_id or {}
            ).items()
        }
        if set(normalized_fall_ground_rolls) != fall_ground_enemy_ids:
            missing=sorted(
                fall_ground_enemy_ids-set(normalized_fall_ground_rolls)
            )
            extra=sorted(
                set(normalized_fall_ground_rolls)-fall_ground_enemy_ids
            )
            raise ValueError(
                "enemy FallGround RNG mismatch; "
                f"missing={missing}, extra={extra}"
            )
        expected_fall_resistance_ids=(
            set(living_player_side_ids)
            if fall_ground_enemy_ids
            else set()
        )
        normalized_fall_resistance={
            str(key):int(value)
            for key,value in (
                fall_ground_equipment_resistance_by_participant_id or {}
            ).items()
        }
        if set(normalized_fall_resistance) != expected_fall_resistance_ids:
            missing=sorted(
                expected_fall_resistance_ids-set(normalized_fall_resistance)
            )
            extra=sorted(
                set(normalized_fall_resistance)-expected_fall_resistance_ids
            )
            raise ValueError(
                "enemy FallGround equipment-resistance inputs mismatch; "
                f"missing={missing}, extra={extra}"
            )
        if any(value != 0 for value in normalized_fall_resistance.values()):
            raise ValueError(
                "enemy FallGround nonzero equipment resistance remains "
                "compile-profile dependent"
            )

        nocast_enemy_ids=set(enemy_batch.nocast_submissions)
        normalized_nocast_rolls={
            str(key):value
            for key,value in (nocast_rolls_by_attack_id or {}).items()
        }
        if set(normalized_nocast_rolls) != nocast_enemy_ids:
            missing=sorted(nocast_enemy_ids-set(normalized_nocast_rolls))
            extra=sorted(set(normalized_nocast_rolls)-nocast_enemy_ids)
            raise ValueError(
                "enemy Nocast RNG mismatch; "
                f"missing={missing}, extra={extra}"
            )
        for participant_id,rolls in normalized_nocast_rolls.items():
            if not isinstance(rolls,NocastActionRolls):
                raise TypeError(
                    f"enemy Nocast RNG has wrong type for {participant_id}"
                )
        if nocast_enemy_ids and state.nocast_overlay is None:
            raise ValueError(
                "enemy Nocast requires explicit persistent battle overlay"
            )

        barrier_enemy_ids=set(enemy_batch.barrier_submissions)
        normalized_barrier_rolls={
            str(key):value
            for key,value in (barrier_rolls_by_attack_id or {}).items()
        }
        if set(normalized_barrier_rolls) != barrier_enemy_ids:
            missing=sorted(barrier_enemy_ids-set(normalized_barrier_rolls))
            extra=sorted(set(normalized_barrier_rolls)-barrier_enemy_ids)
            raise ValueError(
                "enemy Barrier RNG mismatch; "
                f"missing={missing}, extra={extra}"
            )
        for participant_id,rolls in normalized_barrier_rolls.items():
            if not isinstance(rolls,BarrierActionRolls):
                raise TypeError(
                    f"enemy Barrier RNG has wrong type for {participant_id}"
                )
        if barrier_enemy_ids and state.nocast_overlay is None:
            raise ValueError(
                "enemy Barrier requires explicit persistent late-status overlay"
            )

        weaken_enemy_ids=set(enemy_batch.weaken_submissions)
        normalized_weaken_rolls={
            str(key):value
            for key,value in (weaken_rolls_by_attack_id or {}).items()
        }
        if set(normalized_weaken_rolls) != weaken_enemy_ids:
            missing=sorted(weaken_enemy_ids-set(normalized_weaken_rolls))
            extra=sorted(set(normalized_weaken_rolls)-weaken_enemy_ids)
            raise ValueError(
                "enemy Weaken RNG mismatch; "
                f"missing={missing}, extra={extra}"
            )
        for participant_id,rolls in normalized_weaken_rolls.items():
            if not isinstance(rolls,WeakenActionRolls):
                raise TypeError(
                    f"enemy Weaken RNG has wrong type for {participant_id}"
                )
        if weaken_enemy_ids and state.nocast_overlay is None:
            raise ValueError(
                "enemy Weaken requires explicit persistent late-status overlay"
            )

        refresh_enemy_ids=set(enemy_batch.refresh_submissions)
        normalized_refresh_rolls={
            str(key):value
            for key,value in (refresh_rolls_by_attack_id or {}).items()
        }
        if set(normalized_refresh_rolls) != refresh_enemy_ids:
            missing=sorted(refresh_enemy_ids-set(normalized_refresh_rolls))
            extra=sorted(set(normalized_refresh_rolls)-refresh_enemy_ids)
            raise ValueError(
                "enemy Refresh RNG mismatch; "
                f"missing={missing}, extra={extra}"
            )
        for participant_id,rolls in normalized_refresh_rolls.items():
            if not isinstance(rolls,RefreshActionRolls):
                raise TypeError(
                    f"enemy Refresh RNG has wrong type for {participant_id}"
                )
        if refresh_enemy_ids and state.nocast_overlay is None:
            raise ValueError(
                "enemy Refresh requires explicit persistent status overlay"
            )

        setmagicpet_enemy_ids=set(enemy_batch.setmagicpet_submissions)
        normalized_setmagicpet_rolls={
            str(key):value
            for key,value in (
                setmagicpet_rolls_by_attack_id or {}
            ).items()
        }
        if set(normalized_setmagicpet_rolls) != setmagicpet_enemy_ids:
            missing=sorted(
                setmagicpet_enemy_ids-set(normalized_setmagicpet_rolls)
            )
            extra=sorted(
                set(normalized_setmagicpet_rolls)-setmagicpet_enemy_ids
            )
            raise ValueError(
                "enemy SetMagicPet RNG mismatch; "
                f"missing={missing}, extra={extra}"
            )
        for participant_id,rolls in normalized_setmagicpet_rolls.items():
            if not isinstance(rolls,SetMagicPetActionRolls):
                raise TypeError(
                    "enemy SetMagicPet RNG has wrong type for "
                    + participant_id
                )
        if (
            setmagicpet_enemy_ids
            and state.setmagicpet_overlay is None
        ):
            raise ValueError(
                "enemy SetMagicPet requires explicit persistent overlay"
            )

        attack_magic_enemy_ids={
            str(participant_id)
            for participant_id,command in enemy_commands.items()
            if int(command.command1)==BATTLE_COM_S_ATTACK_MAGIC
        }
        if set(enemy_batch.attack_magic_submissions) != attack_magic_enemy_ids:
            raise ValueError(
                "enemy AttackMagic submission/command actor mismatch"
            )
        if attack_magic_enemy_ids and context.attack_magic_overlay is None:
            raise ValueError(
                "enemy AttackMagic round requires explicit battle overlay"
            )
        normalized_attack_magic_rolls={
            str(key):value
            for key,value in (attack_magic_rolls_by_attack_id or {}).items()
        }
        extra_attack_magic_rolls=sorted(
            set(normalized_attack_magic_rolls)-attack_magic_enemy_ids
        )
        if extra_attack_magic_rolls:
            raise ValueError(
                "enemy AttackMagic RNG references non-AttackMagic actors: "
                + ",".join(extra_attack_magic_rolls)
            )
        for participant_id,rolls in normalized_attack_magic_rolls.items():
            if not isinstance(rolls,EnemyAttackMagicActionRolls):
                raise TypeError(
                    f"enemy AttackMagic RNG has wrong type for {participant_id}"
                )
        normalized_attack_magic_retarget_rolls={
            str(key):tuple(int(x) for x in values)
            for key,values in (
                attack_magic_retarget_rolls_by_attack_id or {}
            ).items()
        }
        extra_attack_magic_retarget=sorted(
            set(normalized_attack_magic_retarget_rolls)-attack_magic_enemy_ids
        )
        if extra_attack_magic_retarget:
            raise ValueError(
                "enemy AttackMagic retarget RNG references non-AttackMagic "
                "actors: " + ",".join(extra_attack_magic_retarget)
            )

        escaping_enemy_ids = {
            str(participant_id)
            for participant_id, command in enemy_commands.items()
            if int(command.command1) == BATTLE_COM_ESCAPE
        }
        continuation_enemy_ids = {
            str(participant_id)
            for participant_id, command in enemy_commands.items()
            if int(command.command1) == BATTLE_COM_S_RENZOKU
        }
        abduct_enemy_ids = {
            str(participant_id)
            for participant_id, command in enemy_commands.items()
            if int(command.command1) == BATTLE_COM_S_ABDUCT
        }
        steal_enemy_ids = {
            str(participant_id)
            for participant_id, command in enemy_commands.items()
            if int(command.command1) == BATTLE_COM_S_STEAL
        }
        normalized_steal_rolls={
            str(key):value
            for key,value in (steal_rolls_by_attack_id or {}).items()
        }
        if set(normalized_steal_rolls) != steal_enemy_ids:
            missing=sorted(steal_enemy_ids-set(normalized_steal_rolls))
            extra=sorted(set(normalized_steal_rolls)-steal_enemy_ids)
            raise ValueError(
                "enemy Steal RNG mismatch; "
                f"missing={missing}, extra={extra}"
            )
        for participant_id,rolls in normalized_steal_rolls.items():
            if not isinstance(rolls,OrdinaryStealRolls):
                raise TypeError(
                    f"enemy Steal RNG has wrong type for {participant_id}"
                )

        normalized_abduct_rolls={
            str(key):value
            for key,value in (abduct_rolls_by_attack_id or {}).items()
        }
        extra_abduct_rolls=sorted(
            set(normalized_abduct_rolls)-abduct_enemy_ids
        )
        if extra_abduct_rolls:
            raise ValueError(
                "enemy Abduct RNG references non-Abduct actors: "
                + ",".join(extra_abduct_rolls)
            )
        for participant_id,rolls in normalized_abduct_rolls.items():
            if not isinstance(rolls,OrdinaryAbductRolls):
                raise TypeError(
                    f"enemy Abduct RNG has wrong type for {participant_id}"
                )
        if set(enemy_batch.abduct_contexts) != abduct_enemy_ids:
            raise ValueError(
                "enemy Abduct context/command actor mismatch"
            )

        normalized_continuation_rolls = {
            str(key): value
            for key, value in (
                continuation_rolls_by_attack_id or {}
            ).items()
        }
        if set(normalized_continuation_rolls) != continuation_enemy_ids:
            missing=sorted(
                continuation_enemy_ids-set(normalized_continuation_rolls)
            )
            extra=sorted(
                set(normalized_continuation_rolls)-continuation_enemy_ids
            )
            raise ValueError(
                "enemy ContinuationAttack RNG mismatch; "
                f"missing={missing}, extra={extra}"
            )
        for participant_id,rolls in normalized_continuation_rolls.items():
            if not isinstance(rolls,ContinuationAttackRolls):
                raise TypeError(
                    "enemy ContinuationAttack RNG has wrong type for "
                    f"{participant_id}"
                )

        statuschange_enemy_ids = {
            str(participant_id)
            for participant_id, command in enemy_commands.items()
            if int(command.command1) == BATTLE_COM_S_STATUSCHANGE
        }
        normalized_status_application_rolls = {
            str(key): int(value)
            for key, value in (
                status_application_rolls_by_attack_id or {}
            ).items()
        }
        extra_status_rolls = sorted(
            set(normalized_status_application_rolls)
            - statuschange_enemy_ids
        )
        if extra_status_rolls:
            raise ValueError(
                "enemy StatusChange RNG references non-StatusChange actors: "
                + ",".join(extra_status_rolls)
            )

        normalized_escape_rolls = {
            str(key): value
            for key, value in enemy_escape_rolls.items()
        }
        if set(normalized_escape_rolls) != escaping_enemy_ids:
            missing = sorted(
                escaping_enemy_ids - set(normalized_escape_rolls)
            )
            extra = sorted(
                set(normalized_escape_rolls) - escaping_enemy_ids
            )
            raise ValueError(
                "enemy escape rolls must cover exactly AI-selected escaping "
                f"enemies; missing={missing}, extra={extra}"
            )
        for enemy_id, rolls in normalized_escape_rolls.items():
            if not isinstance(rolls, OrdinaryEscapeRolls):
                raise TypeError(
                    f"enemy escape rolls for {enemy_id} must be "
                    "OrdinaryEscapeRolls"
                )

        normalized_abio = {
            str(key): bool(value)
            for key, value in opponent_abio_by_participant_id.items()
        }
        expected_abio_ids = (
            living_player_side_ids if escaping_enemy_ids else set()
        )
        if set(normalized_abio) != expected_abio_ids:
            missing = sorted(expected_abio_ids - set(normalized_abio))
            extra = sorted(set(normalized_abio) - expected_abio_ids)
            raise ValueError(
                "enemy escape ABIO inputs must cover exactly current living "
                f"opponents when ESCAPE is selected; missing={missing}, "
                f"extra={extra}"
            )

        spawn_by_participant_id = {
            str(spawned.participant.participant_id): spawned
            for spawned in context.spawned_enemies
        }
        escape_contexts = {}
        for enemy_id in escaping_enemy_ids:
            if enemy_id not in spawn_by_participant_id:
                raise ValueError(
                    "escaping enemy lacks recovered spawn provenance: "
                    + enemy_id
                )
            spawned = spawn_by_participant_id[enemy_id]
            if spawned.template.rare is None:
                raise ValueError(
                    "escaping enemy lacks enemybase RARE provenance: "
                    + enemy_id
                )
            if enemy_id not in state.escape_count_by_participant_id:
                raise ValueError(
                    "escaping enemy lacks persistent escape counter: "
                    + enemy_id
                )
            escape_contexts[enemy_id] = OrdinaryEscapeContext(
                stored_escape_count_before=int(
                    state.escape_count_by_participant_id[enemy_id]
                ),
                actor_rare=int(spawned.template.rare),
                opponent_abio_by_participant_id=normalized_abio,
                pvp=False,
                forced_exit=False,
            )

        commands = {
            **normalized_player_commands,
            **dict(enemy_commands),
        }

        working_persistent=None
        steal_gold_state=None
        steal_item_state=None
        mp_state=None
        player_id=str(state.session.player.participant_id)
        mp_damage_enemy_ids=set(enemy_batch.mp_damage_submissions)
        if steal_enemy_ids or mp_damage_enemy_ids:
            working_persistent=decode_persistent_state(
                self._battle_working_persistent_payload(context)
            )
            if working_persistent.character is None:
                raise ValueError(
                    "enemy Steal/MpDamage requires persistent player "
                    "character state"
                )
            fields=dict(working_persistent.character.fields)
            if steal_enemy_ids:
                if "gold" not in fields:
                    raise ValueError(
                        "enemy Steal requires persistent player gold field"
                    )
                steal_gold_state={player_id:int(fields["gold"])}
                steal_item_state={
                    player_id:tuple(
                        sorted(
                            int(slot.value)
                            for slot in working_persistent.inventory
                        )
                    )
                }
            if mp_damage_enemy_ids:
                if "mp" not in fields:
                    raise ValueError(
                        "enemy MpDamage requires persistent player MP field"
                    )
                mp_state={player_id:int(fields["mp"])}

        result = resolve_persistent_ordinary_round(
            state,
            commands=commands,
            initiative_random_subtracts={
                str(key): int(value)
                for key, value in initiative_random_subtracts.items()
            },
            profiles=profiles,
            attack_rolls=attack_rolls,
            counter_rolls_by_attack_id=counter_rolls_by_attack_id,
            continuation_rolls_by_attack_id=normalized_continuation_rolls,
            attack_crazed_rolls_by_attack_id=normalized_attack_crazed_rolls,
            wildviolent_rolls_by_attack_id=normalized_wildviolent_rolls,
            modifyattack_submissions_by_participant_id=enemy_batch.modifyattack_submissions,
            modifyattack_rand_by_participant_id=normalized_modifyattack_rand,
            mdfyattack_submissions_by_participant_id=enemy_batch.mdfyattack_submissions,
            attack_crazed_submissions_by_participant_id=enemy_batch.attack_crazed_submissions,
            wildviolent_submissions_by_participant_id=enemy_batch.wildviolent_submissions,
            abduct_contexts=enemy_batch.abduct_contexts,
            abduct_rolls=normalized_abduct_rolls,
            steal_rolls=normalized_steal_rolls,
            steal_player_gold_by_participant_id=steal_gold_state,
            steal_player_item_slots_by_participant_id=steal_item_state,
            counter_abio_by_participant_id=counter_abio_by_participant_id,
            escape_contexts=escape_contexts,
            escape_rolls=normalized_escape_rolls,
            base_status_rolls_by_participant_id=(
                base_status_rolls_by_participant_id
            ),
            base_status_combat_profiles_by_participant_id=(
                base_status_combat_profiles_by_participant_id
            ),
            status_application_rolls_by_attack_id=(
                normalized_status_application_rolls
            ),
            command_setup_effects_by_participant_id=(
                enemy_batch.setup_effects
            ),
            attack_magic_runtime=(
                getattr(self.stack,"attack_magic_runtime",None)
                if attack_magic_enemy_ids
                else None
            ),
            attack_magic_submissions_by_participant_id=(
                enemy_batch.attack_magic_submissions
            ),
            attack_magic_rolls_by_participant_id=(
                normalized_attack_magic_rolls
            ),
            attack_magic_overlay=context.attack_magic_overlay,
            attack_magic_retarget_rolls_by_participant_id=(
                normalized_attack_magic_retarget_rolls
            ),
            enemy_rehp_submissions_by_participant_id=(
                enemy_batch.enemy_rehp_submissions
            ),
            enemy_rehp_rolls_by_participant_id=normalized_rehp_rolls,
            enemy_rehp_retarget_rolls_by_participant_id=(
                normalized_rehp_retarget_rolls
            ),
            enemy_relife_submissions_by_participant_id=(
                enemy_batch.enemy_relife_submissions
            ),
            enemy_relife_rolls_by_participant_id=(
                normalized_relife_rolls
            ),
            enemy_relife_retarget_rolls_by_participant_id=(
                normalized_relife_retarget_rolls
            ),
            damage_to_hp_submissions_by_participant_id=(
                enemy_batch.damage_to_hp_submissions
            ),
            mp_damage_submissions_by_participant_id=(
                enemy_batch.mp_damage_submissions
            ),
            mp_by_participant_id=mp_state,
            battle_tear_submissions_by_participant_id=(
                enemy_batch.battle_tear_submissions
            ),
            guard_break2_submissions_by_participant_id=(
                enemy_batch.guard_break2_submissions
            ),
            battletimid_submissions_by_participant_id=(
                enemy_batch.battletimid_submissions
            ),
            battletimid_rolls_by_participant_id=(
                normalized_battletimid_rolls
            ),
            lighttakeed_submissions_by_participant_id=(
                enemy_batch.lighttakeed_submissions
            ),
            combined_submissions_by_participant_id=(
                enemy_batch.combined_submissions
            ),
            combined_rolls_by_participant_id=(
                normalized_combined_rolls
            ),
            vary_submissions_by_participant_id=(
                enemy_batch.vary_submissions
            ),
            fall_ground_submissions_by_participant_id=(
                enemy_batch.fall_ground_submissions
            ),
            fall_ground_rolls_by_participant_id=(
                normalized_fall_ground_rolls
            ),
            fall_ground_equipment_resistance_by_participant_id=(
                normalized_fall_resistance
            ),
            nocast_submissions_by_participant_id=(
                enemy_batch.nocast_submissions
            ),
            nocast_rolls_by_participant_id=normalized_nocast_rolls,
            weaken_submissions_by_participant_id=enemy_batch.weaken_submissions,
            weaken_rolls_by_participant_id=normalized_weaken_rolls,
            refresh_submissions_by_participant_id=enemy_batch.refresh_submissions,
            refresh_rolls_by_participant_id=normalized_refresh_rolls,
            setmagicpet_submissions_by_participant_id=(
                enemy_batch.setmagicpet_submissions
            ),
            setmagicpet_rolls_by_participant_id=(
                normalized_setmagicpet_rolls
            ),
            barrier_submissions_by_participant_id=(
                enemy_batch.barrier_submissions
            ),
            barrier_rolls_by_participant_id=normalized_barrier_rolls,
            defense_profile=str(defense_profile),
            no_risk=bool(no_risk),
            field_attr=str(field_attr),
            field_power=int(field_power),
            tie_break_order=(
                None
                if tie_break_order is None
                else tuple(str(x) for x in tie_break_order)
            ),
        )
        next_working_payload=context.working_persistent_state_payload
        if working_persistent is not None:
            if working_persistent.character is None:
                raise AssertionError(
                    "Steal/MpDamage working persistence disappeared"
                )
            fields=dict(working_persistent.character.fields)
            if steal_enemy_ids:
                if player_id not in result.round.steal_gold_by_player_id:
                    raise ValueError("Steal round omitted final player gold state")
                if player_id not in result.round.steal_item_slots_by_player_id:
                    raise ValueError("Steal round omitted final player item state")
                fields["gold"]=int(
                    result.round.steal_gold_by_player_id[player_id]
                )
                allowed_slots=set(
                    int(x)
                    for x in result.round.steal_item_slots_by_player_id[
                        player_id
                    ]
                )
                working_persistent.inventory={
                    slot:item
                    for slot,item in working_persistent.inventory.items()
                    if int(slot.value) in allowed_slots
                }
            if mp_damage_enemy_ids:
                if player_id not in result.round.mp_by_participant_id:
                    raise ValueError(
                        "MpDamage round omitted final player MP state"
                    )
                fields["mp"]=int(
                    result.round.mp_by_participant_id[player_id]
                )
            working_persistent.character=replace(
                working_persistent.character,
                fields=MappingProxyType(fields),
            )
            next_working_payload=encode_persistent_state(
                working_persistent
            )

        return (
            replace(
                context,
                persistent_battle_state=result.after,
                working_persistent_state_payload=next_working_payload,
                attack_magic_overlay=result.attack_magic_overlay_after,
            ),
            result,
        )

    def resolve_persistent_attack_wait_round(
        self,
        context: LocalRuntimeBattleContext,
        *,
        commands: Mapping[str, BattleCommand],
        initiative_random_subtracts: Mapping[str, int],
        profiles: Mapping[str, BattleCombatProfile],
        attack_rolls: Mapping[str, OrdinaryAttackRolls],
        defense_profile: str,
        no_risk: bool = False,
        field_attr: str = "none",
        field_power: int = 0,
        tie_break_order: Sequence[str] | None = None,
    ) -> tuple[LocalRuntimeBattleContext, PersistentRoundResult]:
        """Advance one explicit ordinary ATTACK/GUARD/WAIT round.

        Capture, escape, item, skill/combo and automatic enemy-AI selection
        remain outside this low-level coordinator seam. The dedicated AI bridge
        above may generate only ATTACK/GUARD before entering this method.
        """

        state = context.persistent_battle_state
        if state is None:
            raise ValueError("battle context has no persistent battle state")

        normalized_commands = {
            str(key): value
            for key, value in commands.items()
        }
        invalid_commands = tuple(
            sorted(
                participant_id
                for participant_id, command in normalized_commands.items()
                if not isinstance(command, BattleCommand)
                or int(command.command1)
                not in {BATTLE_COM_ATTACK, BATTLE_COM_GUARD, BATTLE_COM_WAIT}
            )
        )
        if invalid_commands:
            raise ValueError(
                "persistent coordinator R1 accepts ATTACK/GUARD/WAIT only: "
                + ",".join(invalid_commands)
            )

        result = resolve_persistent_ordinary_round(
            state,
            commands=normalized_commands,
            initiative_random_subtracts={
                str(key): int(value)
                for key, value in initiative_random_subtracts.items()
            },
            profiles=profiles,
            attack_rolls=attack_rolls,
            defense_profile=str(defense_profile),
            no_risk=bool(no_risk),
            field_attr=str(field_attr),
            field_power=int(field_power),
            tie_break_order=(
                None
                if tie_break_order is None
                else tuple(str(x) for x in tie_break_order)
            ),
        )
        return (
            replace(
                context,
                persistent_battle_state=result.after,
            ),
            result,
        )

    def resolve_persistent_capture_round(
        self,
        context: LocalRuntimeBattleContext,
        *,
        commands: Mapping[str, BattleCommand],
        initiative_random_subtracts: Mapping[str, int],
        profiles: Mapping[str, BattleCombatProfile],
        attack_rolls: Mapping[str, OrdinaryAttackRolls],
        capture_context: OrdinaryCaptureContext,
        capture_rolls: OrdinaryCaptureRolls,
        captured_pets_by_target_id: Mapping[str, PetActor],
        defense_profile: str,
        no_risk: bool = False,
        field_attr: str = "none",
        field_power: int = 0,
        tie_break_order: Sequence[str] | None = None,
    ) -> tuple[LocalRuntimeBattleContext, PersistentRoundResult]:
        """Advance one explicit player-capture round transactionally."""

        state = context.persistent_battle_state
        if state is None:
            raise ValueError("battle context has no persistent battle state")

        player_id = str(state.session.player.participant_id)
        normalized_commands = {
            str(key): value
            for key, value in commands.items()
        }
        if player_id not in normalized_commands:
            raise ValueError("capture round requires an explicit player command")
        if int(normalized_commands[player_id].command1) != BATTLE_COM_CAPTURE:
            raise ValueError("capture round requires player CAPTURE command")

        invalid_commands = tuple(
            sorted(
                participant_id
                for participant_id, command in normalized_commands.items()
                if not isinstance(command, BattleCommand)
                or int(command.command1)
                not in {BATTLE_COM_ATTACK, BATTLE_COM_WAIT, BATTLE_COM_CAPTURE}
                or (
                    int(command.command1) == BATTLE_COM_CAPTURE
                    and participant_id != player_id
                )
            )
        )
        if invalid_commands:
            raise ValueError(
                "capture coordinator accepts player CAPTURE and ATTACK/WAIT only: "
                + ",".join(invalid_commands)
            )
        if not isinstance(capture_context, OrdinaryCaptureContext):
            raise TypeError("capture_context must be OrdinaryCaptureContext")
        if not isinstance(capture_rolls, OrdinaryCaptureRolls):
            raise TypeError("capture_rolls must be OrdinaryCaptureRolls")

        encounter_runtime = getattr(self.stack, "encounter_runtime", None)
        if encounter_runtime is None:
            raise ValueError("runtime stack has no encounter runtime")

        working_state = decode_persistent_state(
            self._battle_working_persistent_payload(context)
        )
        domain = SinglePlayerHistoricalDomain(
            static=encounter_runtime.static_data,
            persistent=working_state,
        )
        domain.move_player(
            floor_id=context.origin_position.floor_id,
            x=context.origin_position.x,
            y=context.origin_position.y,
        )
        runtime = SinglePlayerHistoricalRuntime(
            domain=domain,
            topology=self.topology,
        )
        result = runtime.resolve_persistent_battle_round(
            state,
            commands=normalized_commands,
            initiative_random_subtracts={
                str(key): int(value)
                for key, value in initiative_random_subtracts.items()
            },
            profiles=profiles,
            attack_rolls=attack_rolls,
            capture_contexts={player_id: capture_context},
            capture_rolls={player_id: capture_rolls},
            captured_pets_by_target_id={
                str(key): value
                for key, value in captured_pets_by_target_id.items()
            },
            defense_profile=str(defense_profile),
            no_risk=bool(no_risk),
            field_attr=str(field_attr),
            field_power=int(field_power),
            tie_break_order=(
                None
                if tie_break_order is None
                else tuple(str(x) for x in tie_break_order)
            ),
        )
        return (
            replace(
                context,
                persistent_battle_state=result.after,
                working_persistent_state_payload=encode_persistent_state(
                    domain.persistent
                ),
            ),
            result,
        )

    def resolve_persistent_escape_round(
        self,
        context: LocalRuntimeBattleContext,
        *,
        commands: Mapping[str, BattleCommand],
        initiative_random_subtracts: Mapping[str, int],
        profiles: Mapping[str, BattleCombatProfile],
        attack_rolls: Mapping[str, OrdinaryAttackRolls],
        escape_context: OrdinaryEscapeContext,
        escape_rolls: OrdinaryEscapeRolls,
        defense_profile: str,
        no_risk: bool = False,
        field_attr: str = "none",
        field_power: int = 0,
        tie_break_order: Sequence[str] | None = None,
    ) -> tuple[LocalRuntimeBattleContext, PersistentRoundResult]:
        """Advance one explicit player-escape round without synthesizing AI."""

        state = context.persistent_battle_state
        if state is None:
            raise ValueError("battle context has no persistent battle state")

        player_id = str(state.session.player.participant_id)
        normalized_commands = {
            str(key): value
            for key, value in commands.items()
        }
        if player_id not in normalized_commands:
            raise ValueError("escape round requires an explicit player command")
        if int(normalized_commands[player_id].command1) != BATTLE_COM_ESCAPE:
            raise ValueError("escape round requires player ESCAPE command")

        invalid_commands = tuple(
            sorted(
                participant_id
                for participant_id, command in normalized_commands.items()
                if not isinstance(command, BattleCommand)
                or int(command.command1)
                not in {BATTLE_COM_ATTACK, BATTLE_COM_WAIT, BATTLE_COM_ESCAPE}
                or (
                    int(command.command1) == BATTLE_COM_ESCAPE
                    and participant_id != player_id
                )
            )
        )
        if invalid_commands:
            raise ValueError(
                "escape coordinator accepts player ESCAPE and ATTACK/WAIT only: "
                + ",".join(invalid_commands)
            )
        if not isinstance(escape_context, OrdinaryEscapeContext):
            raise TypeError("escape_context must be OrdinaryEscapeContext")
        if not isinstance(escape_rolls, OrdinaryEscapeRolls):
            raise TypeError("escape_rolls must be OrdinaryEscapeRolls")

        result = resolve_persistent_ordinary_round(
            state,
            commands=normalized_commands,
            initiative_random_subtracts={
                str(key): int(value)
                for key, value in initiative_random_subtracts.items()
            },
            profiles=profiles,
            attack_rolls=attack_rolls,
            escape_contexts={player_id: escape_context},
            escape_rolls={player_id: escape_rolls},
            defense_profile=str(defense_profile),
            no_risk=bool(no_risk),
            field_attr=str(field_attr),
            field_power=int(field_power),
            tie_break_order=(
                None
                if tie_break_order is None
                else tuple(str(x) for x in tie_break_order)
            ),
        )
        return (
            replace(
                context,
                persistent_battle_state=result.after,
            ),
            result,
        )

    def settle_persistent_defeat(
        self,
        context: LocalRuntimeBattleContext,
    ) -> LocalRuntimeSessionState:
        """Settle one terminal defeat through the recovered battle-exit seam."""

        state = context.persistent_battle_state
        if state is None:
            raise ValueError("battle context has no persistent battle state")
        if state.phase != "finished" or state.result != "defeat":
            raise ValueError("defeat settlement requires terminal defeat state")
        return self.settle_persistent_group_battle_without_level_crossing(
            context
        )

    def settle_persistent_escape(
        self,
        context: LocalRuntimeBattleContext,
    ) -> LocalRuntimeSessionState:
        """Settle terminal player escape without normal battle profit."""

        state = context.persistent_battle_state
        if state is None:
            raise ValueError("battle context has no persistent battle state")

        encounter_runtime = getattr(self.stack, "encounter_runtime", None)
        if encounter_runtime is None:
            raise ValueError("runtime stack has no encounter runtime")

        working_state = decode_persistent_state(
            self._battle_working_persistent_payload(context)
        )
        domain = SinglePlayerHistoricalDomain(
            static=encounter_runtime.static_data,
            persistent=working_state,
        )
        domain.move_player(
            floor_id=context.origin_position.floor_id,
            x=context.origin_position.x,
            y=context.origin_position.y,
        )
        runtime = SinglePlayerHistoricalRuntime(
            domain=domain,
            topology=self.topology,
        )
        returned = runtime.finish_persistent_escape(state)
        updated = LocalRuntimeSessionState(
            contract_id=context.contract_id,
            world_profile=context.world_profile,
            hometown_ordinal=context.hometown_ordinal,
            player_position=returned.world_position,
            player_state=domain.persistent,
            world_flags=context.world_flags,
        )
        return self._validate_session(updated)

    def settle_persistent_group_battle_without_level_crossing(
        self,
        context: LocalRuntimeBattleContext,
    ) -> LocalRuntimeSessionState:
        """Settle a terminal persistent battle into a new authoritative session."""

        state = context.persistent_battle_state
        if state is None:
            raise ValueError("battle context has no persistent battle state")

        encounter_runtime = getattr(self.stack, "encounter_runtime", None)
        if encounter_runtime is None:
            raise ValueError("runtime stack has no encounter runtime")

        working_state = decode_persistent_state(
            self._battle_working_persistent_payload(context)
        )
        domain = SinglePlayerHistoricalDomain(
            static=encounter_runtime.static_data,
            persistent=working_state,
        )
        domain.move_player(
            floor_id=context.origin_position.floor_id,
            x=context.origin_position.x,
            y=context.origin_position.y,
        )
        runtime = SinglePlayerHistoricalRuntime(
            domain=domain,
            topology=self.topology,
        )
        returned = runtime.finish_persistent_battle_without_level_crossing(
            state
        )
        updated = LocalRuntimeSessionState(
            contract_id=context.contract_id,
            world_profile=context.world_profile,
            hometown_ordinal=context.hometown_ordinal,
            player_position=returned.world_position,
            player_state=domain.persistent,
            world_flags=context.world_flags,
        )
        return self._validate_session(updated)

    def settle_persistent_group_battle_with_progression(
        self,
        context: LocalRuntimeBattleContext,
        *,
        player_exp_profile: str,
        next_player_max_exp_by_level: Mapping[int, int],
        pet_exp_profile: str | None = None,
        next_pet_max_exp_by_slot: Mapping[int, Mapping[int, int]] | None = None,
        pet_level_growth_rolls_by_slot: Mapping[int, Sequence[Any]] | None = None,
    ) -> LocalRuntimeSessionState:
        """Settle terminal battle EXP through the closed explicit progression seam.

        The coordinator owns no threshold table and generates no pet growth RNG.
        Profiles, future thresholds and every pet level-growth roll remain explicit
        caller inputs so unresolved launch-era progression cannot be invented here.
        """

        state = context.persistent_battle_state
        if state is None:
            raise ValueError("battle context has no persistent battle state")

        encounter_runtime = getattr(self.stack, "encounter_runtime", None)
        if encounter_runtime is None:
            raise ValueError("runtime stack has no encounter runtime")

        working_state = decode_persistent_state(
            self._battle_working_persistent_payload(context)
        )
        domain = SinglePlayerHistoricalDomain(
            static=encounter_runtime.static_data,
            persistent=working_state,
        )
        domain.move_player(
            floor_id=context.origin_position.floor_id,
            x=context.origin_position.x,
            y=context.origin_position.y,
        )
        runtime = SinglePlayerHistoricalRuntime(
            domain=domain,
            topology=self.topology,
        )
        returned = runtime.finish_persistent_battle_with_progression(
            state,
            player_exp_profile=player_exp_profile,
            next_player_max_exp_by_level=next_player_max_exp_by_level,
            pet_exp_profile=pet_exp_profile,
            next_pet_max_exp_by_slot=next_pet_max_exp_by_slot,
            pet_level_growth_rolls_by_slot=pet_level_growth_rolls_by_slot,
        )
        updated = LocalRuntimeSessionState(
            contract_id=context.contract_id,
            world_profile=context.world_profile,
            hometown_ordinal=context.hometown_ordinal,
            player_position=returned.world_position,
            player_state=domain.persistent,
            world_flags=context.world_flags,
        )
        return self._validate_session(updated)

    @staticmethod
    def _binding_source_rect(binding) -> tuple[int, int, int, int]:
        if binding.predicate_payload.get("interaction_kind") != "DIALOGUE_WARPMAN":
            raise ValueError("state-gated coordinator currently requires dialogue WarpMan")
        raw = binding.predicate_payload.get("source_rect")
        if not isinstance(raw, tuple) or len(raw) != 4:
            raise ValueError("state-gated binding lacks recovered source rectangle")
        x1, y1, x2, y2 = (int(v) for v in raw)
        return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)

    @staticmethod
    def _position_in_binding_source(
        position: MapPosition,
        binding,
    ) -> bool:
        x1, y1, x2, y2 = LocalRuntimeSessionCoordinator._binding_source_rect(
            binding
        )
        return (
            int(position.floor_id) == int(binding.source.floor_id)
            and x1 <= int(position.x) <= x2
            and y1 <= int(position.y) <= y2
        )

    def discover_state_gated_interactions(
        self,
        session: LocalRuntimeSessionState,
    ) -> tuple[LocalRuntimeInteraction, ...]:
        """Return semantic interaction views available at the current coordinate.

        Raw recovered source rectangles and legacy NPC argument strings remain
        inside the binding layer; presentation code receives only stable
        transition identity, live eligibility, and provenance.
        """

        session = self._validate_session(session)
        rows = []
        for transition_id in sorted(self.profile.transitions):
            binding = self.stack.resolve_transition(str(transition_id))
            self._binding_source_rect(binding)
            if not self._position_in_binding_source(
                session.player_position,
                binding,
            ):
                continue
            decision = self.stack.evaluate_transition(
                str(transition_id),
                session,
            )
            rows.append(
                LocalRuntimeInteraction(
                    transition_id=str(transition_id),
                    interaction_kind=str(
                        binding.predicate_payload["interaction_kind"]
                    ),
                    allowed=bool(decision.allowed),
                    reason=decision.reason,
                    provenance=binding.provenance,
                    execution_supported=not bool(decision.consumed_state),
                )
            )
        return tuple(rows)

    def dispatch_state_gated_interaction(
        self,
        session: LocalRuntimeSessionState,
        transition_id: str,
    ) -> LocalRuntimeTransitionResult:
        """Dispatch a semantic interaction id through the canonical executor."""

        return self.execute_state_gated_transition(
            session,
            str(transition_id),
        )

    def execute_state_gated_transition(
        self,
        session: LocalRuntimeSessionState,
        transition_id: str,
    ) -> LocalRuntimeTransitionResult:
        """Evaluate and, if allowed, execute one recovered dialogue transition."""

        session = self._validate_session(session)
        binding = self.stack.resolve_transition(str(transition_id))
        spatially_eligible = self._position_in_binding_source(
            session.player_position,
            binding,
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
