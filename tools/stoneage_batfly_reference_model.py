"""Bounded source-faithful BatFly reference model."""

from dataclasses import dataclass

CALLBACK_NAME="PETSKILL_BatFly"
COMMAND_NAME="BATTLE_COM_S_BAT_FLY"
FEATURE_NAME="_PETSKILL_LER"
SKILL_ID=633


def _i32(value:int) -> int:
    if type(value) is not int or not -(2**31) <= value < 2**31:
        raise ValueError("signed int32 witness required")
    return value


@dataclass(frozen=True)
class BatFlySetup:
    target_slot:int
    packed_com3:int
    command_written:bool=True
    target_written:bool=True
    mode_written:bool=True
    skill_written:bool=True
    command_name:str=COMMAND_NAME


@dataclass(frozen=True)
class BatFlyTarget:
    character_hp:int
    ride_pet_hp:int|None=None


@dataclass(frozen=True)
class BatFlyTargetResolution:
    character_hp_before:int
    character_hp_after:int
    character_drain:int
    ride_pet_hp_before:int|None
    ride_pet_hp_after:int|None
    ride_pet_drain:int
    ride_pet_fell:bool

    @property
    def total_drain(self) -> int:
        return self.character_drain+self.ride_pet_drain


@dataclass(frozen=True)
class BatFlyResolution:
    attacker_hp_before:int
    attacker_max_hp:int
    attacker_hp_after:int
    total_drain:int
    applied_heal:int
    reported_heal:int
    targets:tuple[BatFlyTargetResolution,...]


def resolve_batfly_setup(
    *,
    target_slot:int,
    skill_array:int,
    packed_com3_before:int,
) -> BatFlySetup:
    """The callback writes COM1/COM2/C_OK and LOW(COM3), without OPTION/RNG."""
    target_slot=_i32(target_slot)
    skill_array=_i32(skill_array)
    packed_com3_before=_i32(packed_com3_before)
    packed=(packed_com3_before & 0xffff0000) | (skill_array & 0xffff)
    if packed >= 2**31:
        packed-=2**32
    return BatFlySetup(target_slot=target_slot,packed_com3=packed)


def _positive_hp(value:int,name:str) -> int:
    value=_i32(value)
    if value <= 0:
        raise ValueError(f"{name} must be positive in the living-target R1 domain")
    return value


def resolve_batfly_target(target:BatFlyTarget) -> BatFlyTargetResolution:
    hp=_positive_hp(target.character_hp,"character_hp")
    ride=target.ride_pet_hp
    if ride is None or int(ride) <= 0:
        drain=1 if hp//10 == 0 else hp//10
        return BatFlyTargetResolution(
            character_hp_before=hp,
            character_hp_after=hp-drain,
            character_drain=drain,
            ride_pet_hp_before=None if ride is None else int(ride),
            ride_pet_hp_after=None if ride is None else int(ride),
            ride_pet_drain=0,
            ride_pet_fell=False,
        )

    ride=_positive_hp(int(ride),"ride_pet_hp")
    char_drain=1 if hp//20 == 0 else hp//20
    pet_drain=1 if ride//20 == 0 else ride//20
    pet_after=ride-pet_drain
    return BatFlyTargetResolution(
        character_hp_before=hp,
        character_hp_after=hp-char_drain,
        character_drain=char_drain,
        ride_pet_hp_before=ride,
        ride_pet_hp_after=pet_after,
        ride_pet_drain=pet_drain,
        ride_pet_fell=(pet_after <= 0),
    )


def resolve_batfly_effect(
    *,
    attacker_hp:int,
    attacker_max_hp:int,
    targets:tuple[BatFlyTarget,...],
) -> BatFlyResolution:
    attacker_hp=_i32(attacker_hp)
    attacker_max_hp=_i32(attacker_max_hp)
    if attacker_max_hp <= 0 or not 0 <= attacker_hp <= attacker_max_hp:
        raise ValueError("bounded attacker HP must satisfy 0 <= hp <= max_hp")
    if len(targets) > 10:
        raise ValueError("BatFly side target list exceeds SIDE_OFFSET")
    resolved=tuple(resolve_batfly_target(target) for target in targets)
    total=sum(item.total_drain for item in resolved)
    _i32(total)
    candidate=attacker_hp+total
    _i32(candidate)
    if candidate > attacker_max_hp:
        after=attacker_max_hp
        reported=0
    else:
        after=candidate
        reported=total
    return BatFlyResolution(
        attacker_hp_before=attacker_hp,
        attacker_max_hp=attacker_max_hp,
        attacker_hp_after=after,
        total_drain=total,
        applied_heal=after-attacker_hp,
        reported_heal=reported,
        targets=resolved,
    )
