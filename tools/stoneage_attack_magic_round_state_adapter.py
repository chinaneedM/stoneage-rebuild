#!/usr/bin/env python3
"""Round-time state adapter for recovered25 enemy AttackMagic.

This seam connects:
- an already-validated enemy AttackMagic submission,
- the recovered25 footprint runtime,
- the exact-order AttackMagic action composer,
- existing PersistentBattleState HP/base-status/ride state,
- a dedicated four-element resistance/training overlay.

It deliberately does not advance the round, run death/profit settlement, or
admit command 2002 into the ordinary BattleCommand resolver.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Mapping, Sequence

from tools.stoneage_attack_magic_action_model import (
    AttackMagicDefenderState,
    AttackMagicRideTargetState,
    EnemyAttackMagicActionResolution,
    EnemyAttackMagicActionRolls,
    EnemyAttackMagicCasterState,
    resolve_enemy_attack_magic_action,
)
from tools.stoneage_attack_magic_damage_model import (
    ElementAttrs,
    MagicExpState,
)
from tools.stoneage_battle_ride_damage_model import RidePetRuntime
from tools.stoneage_battle_round_model import BattleCombatProfile
from tools.stoneage_battle_state_model import PersistentBattleState
from tools.stoneage_enemy_ai_attack_magic_bridge import (
    ATTACK_MAGIC_CALLBACK,
    EnemyAiAttackMagicSubmission,
)
from tools.stoneage_recovered25_attack_magic_runtime import (
    Recovered25AttackMagicRuntime,
    Recovered25EnemyAttackMagicPlan,
)


FIELD_ELEMENT_BY_NAME = {
    "none": None,
    "earth": 0,
    "water": 1,
    "fire": 2,
    "wind": 3,
}


@dataclass(frozen=True)
class AttackMagicResistanceRuntime:
    """Four-element magic resistance/training state plus battle modifiers."""

    levels: tuple[int, int, int, int] = (0, 0, 0, 0)
    exps: tuple[int, int, int, int] = (0, 0, 0, 0)
    equipment_resistance: tuple[int, int, int, int] = (0, 0, 0, 0)
    equipment_quimagic: int = 0
    magic_defense_percent: int | None = None

    def __post_init__(self) -> None:
        levels=tuple(int(x) for x in self.levels)
        exps=tuple(int(x) for x in self.exps)
        equip=tuple(int(x) for x in self.equipment_resistance)
        if len(levels) != 4 or len(exps) != 4 or len(equip) != 4:
            raise ValueError("AttackMagic resistance runtime requires four elements")
        if any(not 0 <= x <= 100 for x in levels):
            raise ValueError("AttackMagic resistance levels must be in 0..100")
        if any(x < 0 for x in exps):
            raise ValueError("AttackMagic resistance experience cannot be negative")
        object.__setattr__(self,"levels",levels)
        object.__setattr__(self,"exps",exps)
        object.__setattr__(self,"equipment_resistance",equip)
        object.__setattr__(
            self,"equipment_quimagic",int(self.equipment_quimagic)
        )
        if self.magic_defense_percent is not None:
            object.__setattr__(
                self,
                "magic_defense_percent",
                int(self.magic_defense_percent),
            )

    def state_for(self, element: int) -> MagicExpState:
        element=int(element)
        if element not in range(4):
            raise ValueError("AttackMagic resistance element must be 0..3")
        opposed=(element+1)%4
        return MagicExpState(
            self.levels[element],
            self.exps[element],
            self.levels[opposed],
            self.exps[opposed],
        )

    def with_state(
        self,
        element: int,
        state: MagicExpState,
    ) -> "AttackMagicResistanceRuntime":
        element=int(element)
        if element not in range(4):
            raise ValueError("AttackMagic resistance element must be 0..3")
        opposed=(element+1)%4
        levels=list(self.levels)
        exps=list(self.exps)
        levels[element]=int(state.level)
        exps[element]=int(state.exp)
        levels[opposed]=int(state.opposed_level)
        exps[opposed]=int(state.opposed_exp)
        return replace(self,levels=tuple(levels),exps=tuple(exps))


@dataclass(frozen=True)
class AttackMagicRoundOverlay:
    resistance_by_participant_id: Mapping[
        str,AttackMagicResistanceRuntime
    ]

    def __post_init__(self) -> None:
        normalized={}
        for participant_id,runtime in self.resistance_by_participant_id.items():
            participant_id=str(participant_id)
            if not participant_id:
                raise ValueError("AttackMagic overlay participant id cannot be empty")
            if not isinstance(runtime,AttackMagicResistanceRuntime):
                raise TypeError(
                    "AttackMagic overlay values must be resistance runtimes"
                )
            normalized[participant_id]=runtime
        object.__setattr__(
            self,
            "resistance_by_participant_id",
            MappingProxyType(normalized),
        )


@dataclass(frozen=True)
class PersistentEnemyAttackMagicStateResult:
    before: PersistentBattleState
    overlay_before: AttackMagicRoundOverlay
    plan: Recovered25EnemyAttackMagicPlan
    action: EnemyAttackMagicActionResolution
    after: PersistentBattleState
    overlay_after: AttackMagicRoundOverlay


def _participants(state: PersistentBattleState):
    result={}
    for participant in (
        state.session.player,
        *state.session.allied_pets,
        *state.session.enemies,
    ):
        participant_id=str(participant.participant_id)
        if participant_id in result:
            raise ValueError(
                f"duplicate persistent battle participant {participant_id}"
            )
        result[participant_id]=participant
    return result


def _element_attrs(profile: BattleCombatProfile) -> ElementAttrs:
    if not isinstance(profile,BattleCombatProfile):
        raise TypeError("AttackMagic combat profile has wrong type")
    return ElementAttrs(
        int(profile.earth),
        int(profile.water),
        int(profile.fire),
        int(profile.wind),
    )


def _field_element(field_attr: str) -> int | None:
    key=str(field_attr)
    if key not in FIELD_ELEMENT_BY_NAME:
        raise ValueError(f"unknown AttackMagic field attribute: {key}")
    return FIELD_ELEMENT_BY_NAME[key]


def resolve_persistent_enemy_attack_magic_state(
    state: PersistentBattleState,
    *,
    submission: EnemyAiAttackMagicSubmission,
    attack_magic_runtime: Recovered25AttackMagicRuntime,
    profiles: Mapping[str,BattleCombatProfile],
    overlay: AttackMagicRoundOverlay,
    rolls: EnemyAttackMagicActionRolls,
    retarget_rolls_0_9: Sequence[int] = (),
    field_attr: str = "none",
    field_power: int = 0,
) -> PersistentEnemyAttackMagicStateResult:
    """Apply only AttackMagic HP/resistance/sleep/ride state for one enemy cast."""
    if state.phase != "active":
        raise ValueError("cannot resolve AttackMagic state after battle termination")
    if not isinstance(submission,EnemyAiAttackMagicSubmission):
        raise TypeError("AttackMagic round adapter requires enemy submission")
    if submission.callback != ATTACK_MAGIC_CALLBACK:
        raise ValueError("AttackMagic submission callback drift")
    if not isinstance(attack_magic_runtime,Recovered25AttackMagicRuntime):
        raise TypeError("AttackMagic round adapter requires recovered25 runtime")
    if not isinstance(overlay,AttackMagicRoundOverlay):
        raise TypeError("AttackMagic round adapter requires typed overlay")
    if not isinstance(rolls,EnemyAttackMagicActionRolls):
        raise TypeError("AttackMagic round adapter requires typed RNG")

    participants=_participants(state)
    caster_id=str(submission.participant_id)
    if caster_id not in participants:
        raise KeyError(f"AttackMagic caster is not in battle: {caster_id}")
    caster_participant=participants[caster_id]
    if caster_participant.side != "enemy" or caster_participant.kind != "enemy":
        raise ValueError("recovered enemy AttackMagic caster must be enemy entry")
    if caster_id not in state.slots:
        raise ValueError("AttackMagic caster lacks authoritative battle slot")
    actor_slot=int(state.slots[caster_id])
    if not 10 <= actor_slot <= 19:
        raise ValueError("enemy AttackMagic caster must occupy slot 10..19")
    inactive=set(state.ultimate_exited_participant_ids)
    inactive.update(state.battle_exited_participant_ids)
    if caster_id in inactive or int(state.hp_by_participant_id[caster_id]) <= 0:
        raise ValueError("enemy AttackMagic caster must be living and active")

    try:
        indexed=attack_magic_runtime.entries[int(submission.skill_id)]
    except KeyError as exc:
        raise ValueError(
            f"AttackMagic runtime lacks submission skill {submission.skill_id}"
        ) from exc
    if int(indexed.magic_id) != int(submission.command.magic_id):
        raise ValueError("AttackMagic submission/runtime magic-id drift")

    alive_player_slots=tuple(
        sorted(
            int(state.slots[participant_id])
            for participant_id,participant in participants.items()
            if (
                participant.side == "player"
                and participant_id not in inactive
                and int(state.hp_by_participant_id[participant_id]) > 0
                and 0 <= int(state.slots[participant_id]) <= 9
            )
        )
    )
    plan=attack_magic_runtime.resolve_enemy_footprint(
        skill_id=int(submission.skill_id),
        actor_slot=actor_slot,
        target_slot=int(submission.direct_use_request.source_target),
        alive_player_slots=alive_player_slots,
        retarget_rolls_0_9=tuple(int(x) for x in retarget_rolls_0_9),
        require_exact_source_order=True,
    )
    if int(plan.magic_id) != int(submission.command.magic_id):
        raise ValueError("AttackMagic resolved plan/submission magic-id drift")

    profile_by_id={str(pid):value for pid,value in profiles.items()}
    if caster_id not in profile_by_id:
        raise KeyError(f"missing AttackMagic caster profile for {caster_id}")
    caster=EnemyAttackMagicCasterState(
        participant_id=caster_id,
        level=int(caster_participant.level),
        pure_attrs=_element_attrs(profile_by_id[caster_id]),
    )

    participant_id_by_slot={
        int(slot):str(participant_id)
        for participant_id,slot in state.slots.items()
    }
    defenders={}
    target_ids=[]
    for slot in plan.source_target_order or ():
        slot=int(slot)
        participant_id=participant_id_by_slot.get(slot)
        if participant_id is None:
            raise ValueError(f"AttackMagic target slot {slot} has no participant")
        participant=participants[participant_id]
        if participant.side != "player":
            raise ValueError("enemy AttackMagic target crossed battle sides")
        if participant_id not in profile_by_id:
            raise KeyError(
                f"missing AttackMagic defender profile for {participant_id}"
            )
        try:
            resistance_runtime=overlay.resistance_by_participant_id[
                participant_id
            ]
        except KeyError as exc:
            raise KeyError(
                f"missing AttackMagic resistance runtime for {participant_id}"
            ) from exc

        ride_state=None
        ride_runtime=state.ride_pet_runtime
        if (
            participant.kind == "player"
            and ride_runtime is not None
            and str(ride_runtime.rider_id) == participant_id
            and bool(ride_runtime.mounted)
        ):
            ride_id=str(ride_runtime.pet_id)
            ride_source=state.session.ride_pet
            if ride_source is None:
                raise ValueError("mounted AttackMagic ride lacks session provenance")
            if str(ride_source.participant_id) != ride_id:
                raise ValueError("AttackMagic ride session/runtime identity drift")
            if ride_id not in profile_by_id:
                raise KeyError(
                    f"missing AttackMagic ride-pet profile for {ride_id}"
                )
            ride_state=AttackMagicRideTargetState(
                pet_id=ride_id,
                hp=int(ride_runtime.hp),
                max_hp=int(ride_runtime.max_hp),
                pure_attrs=_element_attrs(profile_by_id[ride_id]),
                mounted=bool(ride_runtime.mounted),
                petfall=bool(ride_runtime.petfall),
            )

        status_runtime=state.base_status_runtime_by_participant_id[
            participant_id
        ]
        profile=profile_by_id[participant_id]
        defenders[slot]=AttackMagicDefenderState(
            participant_id=participant_id,
            kind=str(participant.kind),
            level=int(participant.level),
            hp=int(state.hp_by_participant_id[participant_id]),
            max_hp=int(participant.max_hp),
            pure_attrs=_element_attrs(profile),
            resistance=resistance_runtime.state_for(plan.element),
            luck=int(profile.fixed_luck),
            equipment_resistance=int(
                resistance_runtime.equipment_resistance[plan.element]
            ),
            equipment_quimagic=int(
                resistance_runtime.equipment_quimagic
            ),
            magic_defense_percent=(
                resistance_runtime.magic_defense_percent
            ),
            sleep_turns=int(status_runtime.status.sleep),
            ride=ride_state,
        )
        target_ids.append(participant_id)

    expected_roll_slots=set(int(x) for x in (plan.source_target_order or ()))
    actual_roll_slots=set(int(x) for x in rolls.target_rolls_by_slot)
    if actual_roll_slots != expected_roll_slots:
        missing=sorted(expected_roll_slots-actual_roll_slots)
        extra=sorted(actual_roll_slots-expected_roll_slots)
        raise ValueError(
            "AttackMagic RNG target slots must match exact source order; "
            f"missing={missing}, extra={extra}"
        )

    action=resolve_enemy_attack_magic_action(
        plan=plan,
        caster=caster,
        defenders_by_slot=defenders,
        rolls=rolls,
        field_element=_field_element(field_attr),
        field_power=int(field_power),
    )

    hp=dict(state.hp_by_participant_id)
    status_runtimes=dict(state.base_status_runtime_by_participant_id)
    resistance_after=dict(overlay.resistance_by_participant_id)
    next_ride=state.ride_pet_runtime

    for slot in action.target_order:
        participant_id=participant_id_by_slot[int(slot)]
        defender_after=action.defenders_after[int(slot)]
        hp[participant_id]=int(defender_after.hp)

        runtime=status_runtimes[participant_id]
        status_runtimes[participant_id]=replace(
            runtime,
            status=replace(
                runtime.status,
                sleep=int(defender_after.sleep_turns),
            ),
        )

        resistance_after[participant_id]=resistance_after[
            participant_id
        ].with_state(
            plan.element,
            defender_after.resistance,
        )

        if (
            participant_id == str(state.session.player.participant_id)
            and next_ride is not None
            and str(next_ride.rider_id) == participant_id
            and defender_after.ride is not None
        ):
            ride_after=defender_after.ride
            if str(ride_after.pet_id) != str(next_ride.pet_id):
                raise ValueError("AttackMagic ride result identity drift")
            if int(ride_after.max_hp) != int(next_ride.max_hp):
                raise ValueError("AttackMagic ride result max-HP drift")
            next_ride=replace(
                next_ride,
                hp=int(ride_after.hp),
                mounted=bool(ride_after.mounted),
                petfall=bool(ride_after.petfall),
            )

    after=replace(
        state,
        hp_by_participant_id=MappingProxyType(hp),
        base_status_runtime_by_participant_id=MappingProxyType(
            status_runtimes
        ),
        ride_pet_runtime=next_ride,
    )
    overlay_after=AttackMagicRoundOverlay(resistance_after)
    return PersistentEnemyAttackMagicStateResult(
        before=state,
        overlay_before=overlay,
        plan=plan,
        action=action,
        after=after,
        overlay_after=overlay_after,
    )
