#!/usr/bin/env python3
"""Stable-descendant base battle-status timing and mutation seam.

This module is deliberately narrower than later magic/profession status
systems. It reconstructs the common poison/paralysis/sleep/stone/drunk/
confusion loop, its command-suppression order, and positive-damage wake-up
behavior without inventing later gated effects.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace


STATUS_POISON="poison"
STATUS_PARALYSIS="paralysis"
STATUS_SLEEP="sleep"
STATUS_STONE="stone"
STATUS_DRUNK="drunk"
STATUS_CONFUSION="confusion"

BASE_STATUS_ORDER=(
    STATUS_POISON,
    STATUS_PARALYSIS,
    STATUS_SLEEP,
    STATUS_STONE,
    STATUS_DRUNK,
    STATUS_CONFUSION,
)

BASE_STATUS_NAME_BY_INDEX={
    1:STATUS_POISON,
    2:STATUS_PARALYSIS,
    3:STATUS_SLEEP,
    4:STATUS_STONE,
    5:STATUS_DRUNK,
    6:STATUS_CONFUSION,
}
BASE_STATUS_INDEX_BY_NAME={
    name:index for index,name in BASE_STATUS_NAME_BY_INDEX.items()
}


def base_status_name_from_index(index: int) -> str:
    index=int(index)
    if index not in BASE_STATUS_NAME_BY_INDEX:
        raise ValueError(f"status index {index} is outside common base statuses")
    return BASE_STATUS_NAME_BY_INDEX[index]


def _c_div(numerator: int, denominator: int) -> int:
    numerator=int(numerator)
    denominator=int(denominator)
    if denominator == 0:
        raise ZeroDivisionError("C-style division by zero")
    sign=-1 if (numerator < 0) ^ (denominator < 0) else 1
    return sign * (abs(numerator) // abs(denominator))


@dataclass(frozen=True)
class BaseBattleStatusState:
    poison: int = 0
    paralysis: int = 0
    sleep: int = 0
    stone: int = 0
    drunk: int = 0
    confusion: int = 0

    def __post_init__(self) -> None:
        for name in BASE_STATUS_ORDER:
            value=int(getattr(self,name))
            if value < 0:
                raise ValueError(f"{name} status counter cannot be negative")
            object.__setattr__(self,name,value)


@dataclass(frozen=True)
class BaseStatusAttackInputs:
    status: str
    attacker_level: int
    defender_level: int
    pvp: bool
    attacker_fixed_luck: int
    defender_vital: int
    defender_str: int
    defender_tough: int
    defender_dex: int
    defender_resistance: int
    per_offset: int
    level_range: int
    level_scale: float

    def __post_init__(self) -> None:
        status=str(self.status)
        if status not in BASE_STATUS_ORDER:
            raise ValueError(f"unsupported common base status: {status}")
        object.__setattr__(self,"status",status)
        for name in (
            "attacker_level","defender_level","attacker_fixed_luck",
            "defender_vital","defender_str","defender_tough",
            "defender_dex","defender_resistance","per_offset",
            "level_range",
        ):
            object.__setattr__(self,name,int(getattr(self,name)))
        if self.level_range < 0:
            raise ValueError("level_range cannot be negative")
        object.__setattr__(self,"pvp",bool(self.pvp))
        object.__setattr__(self,"level_scale",float(self.level_scale))


@dataclass(frozen=True)
class BaseStatusAttackResolution:
    status: str
    eligible: bool
    blocked_by_existing_status: bool
    source_probability_value: int | None
    roll_1_100: int | None
    rng_consumed: bool
    success: bool
    blocked_by_damage_gate: bool = False


def active_base_status_names(status: BaseBattleStatusState) -> tuple[str,...]:
    return tuple(
        name for name in BASE_STATUS_ORDER
        if int(getattr(status,name)) > 0
    )


def apply_base_status_counter(
    current: BaseBattleStatusState,
    *,
    status: str,
    turn: int,
) -> BaseBattleStatusState:
    status=str(status)
    if status not in BASE_STATUS_ORDER:
        raise ValueError(f"unsupported common base status: {status}")
    turn=int(turn)
    if turn < 0:
        raise ValueError("base status turn cannot be negative")
    return replace(current,**{status:turn})


def base_status_attack_probability_value(
    inputs: BaseStatusAttackInputs,
) -> int:
    """Return the source probability value before the strict RAND(1,100) check."""
    if inputs.status == STATUS_PARALYSIS:
        return 20-int(inputs.defender_resistance)

    stat_sum=(
        int(inputs.defender_vital)
        + int(inputs.defender_str)
        + int(inputs.defender_tough)
        + int(inputs.defender_dex)
    )
    if stat_sum <= 0:
        raise ValueError(
            "general base status check requires positive defender stat sum"
        )
    f_vital_p=(
        (float(inputs.defender_vital)/float(stat_sum))
        / 0.25
        * 10.0
    )
    if inputs.pvp:
        level=0
    else:
        level=int(
            (int(inputs.attacker_level)-int(inputs.defender_level))
            * float(inputs.level_scale)
        )
    level=max(-int(inputs.level_range),min(int(inputs.level_range),level))
    per=int(
        int(inputs.per_offset)
        + level
        + int(inputs.attacker_fixed_luck)
        - int(inputs.defender_resistance)
        - f_vital_p
    )
    if per > 80:
        per=80
    return int(per)


def resolve_base_status_attack_check(
    inputs: BaseStatusAttackInputs,
    current_status: BaseBattleStatusState,
    *,
    roll_1_100: int | None,
) -> BaseStatusAttackResolution:
    """Mirror common BATTLE_StatusAttackCheck without later suit/Lua resist."""

    active=active_base_status_names(current_status)
    if active:
        return BaseStatusAttackResolution(
            status=inputs.status,
            eligible=False,
            blocked_by_existing_status=True,
            source_probability_value=None,
            roll_1_100=None,
            rng_consumed=False,
            success=False,
        )

    per=base_status_attack_probability_value(inputs)

    if roll_1_100 is None:
        raise ValueError("eligible base status check requires RAND(1,100)")
    roll=int(roll_1_100)
    if not 1 <= roll <= 100:
        raise ValueError("base status roll must be in 1..100")
    return BaseStatusAttackResolution(
        status=inputs.status,
        eligible=True,
        blocked_by_existing_status=False,
        source_probability_value=int(per),
        roll_1_100=roll,
        rng_consumed=True,
        success=(roll < int(per)),
    )


@dataclass(frozen=True)
class BaseStatusApplicationResolution:
    check: BaseStatusAttackResolution
    status_before: BaseBattleStatusState
    status_after: BaseBattleStatusState
    turn_written: int | None
    command_cleared: bool


def resolve_base_status_application(
    inputs: BaseStatusAttackInputs,
    current_status: BaseBattleStatusState,
    *,
    turn: int,
    roll_1_100: int | None,
) -> BaseStatusApplicationResolution:
    """Run status hit-check then perform the caller-selected exact turn write."""
    turn=int(turn)
    if turn < 0:
        raise ValueError("base status turn cannot be negative")
    check=resolve_base_status_attack_check(
        inputs,
        current_status,
        roll_1_100=roll_1_100,
    )
    after=current_status
    written=None
    if check.success:
        after=apply_base_status_counter(
            current_status,
            status=inputs.status,
            turn=turn,
        )
        written=turn
    return BaseStatusApplicationResolution(
        check=check,
        status_before=current_status,
        status_after=after,
        turn_written=written,
        command_cleared=bool(
            check.success
            and inputs.status in {
                STATUS_PARALYSIS,
                STATUS_SLEEP,
                STATUS_STONE,
            }
        ),
    )


@dataclass(frozen=True)
class BasePhysicalOnHitStatusInputs:
    status: str
    attacker_level: int
    defender_level: int
    pvp: bool
    attacker_fixed_luck: int
    defender_vital: int
    defender_str: int
    defender_tough: int
    defender_dex: int
    defender_resistance: int
    source_turn: int
    per_offset: int = 30

    def __post_init__(self) -> None:
        status=str(self.status)
        if status not in BASE_STATUS_ORDER:
            raise ValueError(f"unsupported common base status: {status}")
        object.__setattr__(self,"status",status)
        for name in (
            "attacker_level","defender_level","attacker_fixed_luck",
            "defender_vital","defender_str","defender_tough",
            "defender_dex","defender_resistance","source_turn",
            "per_offset",
        ):
            object.__setattr__(self,name,int(getattr(self,name)))
        if self.source_turn < 0:
            raise ValueError("physical source_turn cannot be negative")
        object.__setattr__(self,"pvp",bool(self.pvp))


def resolve_base_physical_on_hit_status_application(
    inputs: BasePhysicalOnHitStatusInputs,
    current_status: BaseBattleStatusState,
    *,
    damage_after_resolution: int,
    roll_1_100: int | None,
) -> BaseStatusApplicationResolution:
    """Mirror the common BATTLE_Attack() status payload branch.

    The physical path is gated by positive post-DamageSub damage, calls the
    shared status check with Range=40/Bai=2.0, stores source_turn+1 on success,
    then applies the source's extra DRUNK integer halving.
    """
    damage=int(damage_after_resolution)
    if damage <= 0:
        return BaseStatusApplicationResolution(
            check=BaseStatusAttackResolution(
                status=inputs.status,
                eligible=False,
                blocked_by_existing_status=False,
                source_probability_value=None,
                roll_1_100=None,
                rng_consumed=False,
                success=False,
                blocked_by_damage_gate=True,
            ),
            status_before=current_status,
            status_after=current_status,
            turn_written=None,
            command_cleared=False,
        )

    application=resolve_base_status_application(
        BaseStatusAttackInputs(
            status=inputs.status,
            attacker_level=inputs.attacker_level,
            defender_level=inputs.defender_level,
            pvp=inputs.pvp,
            attacker_fixed_luck=inputs.attacker_fixed_luck,
            defender_vital=inputs.defender_vital,
            defender_str=inputs.defender_str,
            defender_tough=inputs.defender_tough,
            defender_dex=inputs.defender_dex,
            defender_resistance=inputs.defender_resistance,
            per_offset=inputs.per_offset,
            level_range=40,
            level_scale=2.0,
        ),
        current_status,
        turn=int(inputs.source_turn)+1,
        roll_1_100=roll_1_100,
    )
    if not application.check.success or inputs.status != STATUS_DRUNK:
        return application

    final_turn=int(application.status_after.drunk)//2
    return replace(
        application,
        status_after=replace(
            application.status_after,
            drunk=final_turn,
        ),
        turn_written=final_turn,
    )


@dataclass(frozen=True)
class BaseStatusTurnRolls:
    confusion_action_roll_1_100: int | None = None
    confusion_side_roll_0_1: int | None = None
    confusion_pos_roll_0_9: int | None = None


@dataclass(frozen=True)
class BaseBattleStatusRuntime:
    status: BaseBattleStatusState = field(
        default_factory=BaseBattleStatusState
    )
    poison_stat_sum: int | None = None
    work_quick: int | None = None
    ride_work_quick: int | None = None
    damage_count: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.status,BaseBattleStatusState):
            raise TypeError("status must be BaseBattleStatusState")
        if self.poison_stat_sum is not None:
            object.__setattr__(
                self,"poison_stat_sum",int(self.poison_stat_sum)
            )
        if self.work_quick is not None:
            object.__setattr__(self,"work_quick",int(self.work_quick))
        if self.ride_work_quick is not None:
            object.__setattr__(
                self,"ride_work_quick",int(self.ride_work_quick)
            )
        damage_count=int(self.damage_count)
        if damage_count < 0:
            raise ValueError("damage_count cannot be negative")
        object.__setattr__(self,"damage_count",damage_count)


@dataclass(frozen=True)
class BaseStatusTickInputs:
    hp: int
    status: BaseBattleStatusState
    poison_stat_sum: int | None = None
    actor_slot: int | None = None
    valid_target_slots: tuple[int,...] = ()
    confusion_action_roll_1_100: int | None = None
    confusion_side_roll_0_1: int | None = None
    confusion_pos_roll_0_9: int | None = None
    work_quick: int | None = None
    ride_work_quick: int | None = None

    def __post_init__(self) -> None:
        hp=int(self.hp)
        if hp < 0:
            raise ValueError("hp cannot be negative")
        object.__setattr__(self,"hp",hp)
        object.__setattr__(
            self,
            "valid_target_slots",
            tuple(int(slot) for slot in self.valid_target_slots),
        )
        if self.actor_slot is not None:
            slot=int(self.actor_slot)
            if not 0 <= slot <= 19:
                raise ValueError("actor_slot must be in 0..19")
            object.__setattr__(self,"actor_slot",slot)


@dataclass(frozen=True)
class BaseStatusTickResult:
    status_before: BaseBattleStatusState
    status_after: BaseBattleStatusState
    hp_before: int
    hp_after: int
    poison_damage: int
    expired_statuses: tuple[str,...]
    can_move_before_decrement: bool
    can_move_after_tick: bool
    command_override: str | None
    target_override: int | None
    confusion_rewrote_command: bool
    work_quick_after: int | None


@dataclass(frozen=True)
class DamageWakeResult:
    status_after: BaseBattleStatusState
    damage_count_after: int
    sleep_was_cleared: bool
    wakeup_applied: bool


def base_status_can_move(status: BaseBattleStatusState) -> bool:
    return not (
        int(status.paralysis) > 0
        or int(status.stone) > 0
        or int(status.sleep) > 0
    )


def base_stone_defense_multiplier(status: BaseBattleStatusState) -> float:
    return 2.0 if int(status.stone) > 0 else 1.0


def base_poison_damage(hp: int, poison_stat_sum: int) -> tuple[int,int]:
    """Return (damage,hp_after) for the common Compute_Down actor branch."""
    hp=int(hp)
    stat_sum=int(poison_stat_sum)
    if hp < 0:
        raise ValueError("hp cannot be negative")
    down=_c_div(_c_div(stat_sum,100)-20,4)
    if down < 1:
        down=1
    if hp <= down:
        down=hp-1
    if down < 0:
        return 0,hp
    hp_after=max(1,hp-down)
    return int(down),int(hp_after)


def _decrement(status: BaseBattleStatusState, name: str) -> BaseBattleStatusState:
    current=int(getattr(status,name))
    if current <= 0:
        return status
    return replace(status,**{name:current-1})


def _confusion_target(inputs: BaseStatusTickInputs) -> int:
    if inputs.actor_slot is None:
        raise ValueError("confusion target rewrite requires actor_slot")
    if inputs.confusion_side_roll_0_1 is None:
        raise ValueError("confusion side roll is required")
    if inputs.confusion_pos_roll_0_9 is None:
        raise ValueError("confusion position roll is required")
    side=int(inputs.confusion_side_roll_0_1)
    pos=int(inputs.confusion_pos_roll_0_9)
    if side not in (0,1):
        raise ValueError("confusion side roll must be 0 or 1")
    if not 0 <= pos <= 9:
        raise ValueError("confusion position roll must be in 0..9")
    valid=set(inputs.valid_target_slots)
    for _ in range(10):
        pos+=1
        if pos >= 10:
            pos=0
        target=side*10+pos
        if target == int(inputs.actor_slot):
            continue
        if target in valid:
            return target
    return -1


def resolve_base_status_tick(inputs: BaseStatusTickInputs) -> BaseStatusTickResult:
    """Mirror common BATTLE_StatusSeq ordering for the six base statuses."""
    if not isinstance(inputs,BaseStatusTickInputs):
        raise TypeError("inputs must be BaseStatusTickInputs")

    before=inputs.status
    current=before
    hp_before=int(inputs.hp)
    hp_after=hp_before
    poison_damage=0
    expired=[]
    command_override=None
    target_override=None
    confusion_rewrote=False
    work_quick_after=(
        None if inputs.work_quick is None else int(inputs.work_quick)
    )

    can_move_before=base_status_can_move(before)
    if not can_move_before:
        command_override="none"

    for name in BASE_STATUS_ORDER:
        count=int(getattr(current,name))
        if count <= 0:
            continue
        current=_decrement(current,name)
        count_after=int(getattr(current,name))
        if count_after <= 0:
            expired.append(name)
            if name == STATUS_DRUNK:
                if work_quick_after is None:
                    raise ValueError(
                        "drunk expiration requires current work_quick"
                    )
                if inputs.ride_work_quick is None:
                    work_quick_after=int(work_quick_after)*2
                else:
                    work_quick_after=(
                        int(work_quick_after)+int(inputs.ride_work_quick)
                    )
            continue

        if name == STATUS_POISON:
            if inputs.poison_stat_sum is None:
                raise ValueError(
                    "active poison damage tick requires poison_stat_sum"
                )
            poison_damage,hp_after=base_poison_damage(
                hp_after,
                int(inputs.poison_stat_sum),
            )
        elif name == STATUS_CONFUSION:
            if inputs.confusion_action_roll_1_100 is None:
                raise ValueError("active confusion tick requires action roll")
            roll=int(inputs.confusion_action_roll_1_100)
            if not 1 <= roll <= 100:
                raise ValueError("confusion action roll must be in 1..100")
            if roll <= 80:
                command_override="attack"
                target_override=_confusion_target(inputs)
                confusion_rewrote=True

    can_move_after=base_status_can_move(current)
    # The outer battle loop performs BATTLE_CanMoveCheck() again after
    # BATTLE_StatusSeq(). It can suppress a confusion rewrite, but it does not
    # restore an original command that was already cleared before decrement.
    if not can_move_after:
        command_override="none"

    return BaseStatusTickResult(
        status_before=before,
        status_after=current,
        hp_before=hp_before,
        hp_after=hp_after,
        poison_damage=int(poison_damage),
        expired_statuses=tuple(expired),
        can_move_before_decrement=bool(can_move_before),
        can_move_after_tick=bool(can_move_after),
        command_override=command_override,
        target_override=target_override,
        confusion_rewrote_command=bool(confusion_rewrote),
        work_quick_after=work_quick_after,
    )


def resolve_base_damage_wakeup(
    status: BaseBattleStatusState,
    *,
    damage_count_before: int,
    damage: int,
    absorb_or_vanish: bool = False,
) -> DamageWakeResult:
    """Mirror the common positive-damage BATTLE_DamageWakeUp call boundary."""
    damage_count=int(damage_count_before)
    if damage_count < 0:
        raise ValueError("damage_count_before cannot be negative")
    damage=int(damage)
    if damage <= 0 or bool(absorb_or_vanish):
        return DamageWakeResult(
            status_after=status,
            damage_count_after=damage_count,
            sleep_was_cleared=False,
            wakeup_applied=False,
        )

    cleared=int(status.sleep)>0
    after=replace(status,sleep=0) if cleared else status
    return DamageWakeResult(
        status_after=after,
        damage_count_after=damage_count+1,
        sleep_was_cleared=cleared,
        wakeup_applied=True,
    )
