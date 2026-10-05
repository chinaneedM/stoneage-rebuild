"""Persistent battle-local state for bounded PETSKILL_Combined execution."""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_combined_direct_magic_model import RuntimeItemZeroWitness
from tools.stoneage_combined_initiative_model import ADMITTED_PROFILES
from tools.stoneage_magic_effect_model import (
    att_reverse_cast_transition,
    att_reverse_precommand_refresh,
)

STATUS_MAGIC_PROFILE_IRIS_CP950 = "iris_cp950"
ADMITTED_STATUS_MAGIC_PROFILES = (STATUS_MAGIC_PROFILE_IRIS_CP950,)
_RECONSTRUCTION_REVERSE_BIT = 1


@dataclass(frozen=True)
class CombinedActionRolls:
    """Action-time RNG after callback selection and initiative were consumed."""

    retarget_draws_0_9: tuple[int, ...] = ()
    recovery_roll_90_110: int | None = None
    status_roll_1_100: int | None = None

    def __post_init__(self) -> None:
        draws=tuple(int(v) for v in self.retarget_draws_0_9)
        if any(v < 0 or v > 9 for v in draws):
            raise ValueError("Combined retarget draws must be reduced 0..9")
        recovery=(
            None if self.recovery_roll_90_110 is None
            else int(self.recovery_roll_90_110)
        )
        if recovery is not None and not 90 <= recovery <= 110:
            raise ValueError("Combined Recovery draw must be 90..110")
        status=(
            None if self.status_roll_1_100 is None
            else int(self.status_roll_1_100)
        )
        if status is not None and not 1 <= status <= 100:
            raise ValueError("Combined StatusChange draw must be 1..100")
        object.__setattr__(self,"retarget_draws_0_9",draws)
        object.__setattr__(self,"recovery_roll_90_110",recovery)
        object.__setattr__(self,"status_roll_1_100",status)


@dataclass(frozen=True)
class CombinedRuntimeOverlay:
    """Conditional live witnesses and persistent Combined battle state.

    initiative_profile is a later-descendant compile-profile choice, not an
    original-build claim. status_magic_profile is likewise conditional. The
    item-zero object is a live runtime witness and is never inferred from a
    static item configuration ID.
    """

    initiative_profile: str
    status_magic_profile: str
    item_zero: RuntimeItemZeroWitness
    mp_by_participant_id: Mapping[str,int]
    att_reverse_by_participant_id: Mapping[str,bool]

    def __post_init__(self) -> None:
        initiative=str(self.initiative_profile)
        if initiative not in ADMITTED_PROFILES:
            raise ValueError("Combined initiative profile must be explicit")
        status_profile=str(self.status_magic_profile)
        if status_profile not in ADMITTED_STATUS_MAGIC_PROFILES:
            raise ValueError("Combined status-magic profile must be explicit")
        if not isinstance(self.item_zero,RuntimeItemZeroWitness):
            raise TypeError("Combined item-zero witness has wrong type")
        mp={str(pid):int(value) for pid,value in self.mp_by_participant_id.items()}
        if any(value < 0 for value in mp.values()):
            raise ValueError("Combined MP state cannot be negative")
        reverse={
            str(pid):bool(value)
            for pid,value in self.att_reverse_by_participant_id.items()
        }
        object.__setattr__(self,"initiative_profile",initiative)
        object.__setattr__(self,"status_magic_profile",status_profile)
        object.__setattr__(self,"mp_by_participant_id",MappingProxyType(mp))
        object.__setattr__(
            self,"att_reverse_by_participant_id",MappingProxyType(reverse)
        )

    def with_mp(self, participant_id: str, mp: int) -> "CombinedRuntimeOverlay":
        pid=str(participant_id); value=int(mp)
        if pid not in self.mp_by_participant_id:
            raise KeyError(f"Combined MP witness absent for {pid}")
        if value < 0:
            raise ValueError("Combined MP state cannot be negative")
        rows=dict(self.mp_by_participant_id); rows[pid]=value
        return CombinedRuntimeOverlay(
            self.initiative_profile,self.status_magic_profile,self.item_zero,
            rows,self.att_reverse_by_participant_id,
        )

    def validate_participants(self, participant_ids) -> None:
        ids={str(pid) for pid in participant_ids}
        reverse=set(self.att_reverse_by_participant_id)
        if reverse != ids:
            missing=sorted(ids-reverse); extra=sorted(reverse-ids)
            raise ValueError(
                "Combined AttReverse overlay participant mismatch; "
                f"missing={missing}, extra={extra}"
            )
        unknown=sorted(set(self.mp_by_participant_id)-ids)
        if unknown:
            raise ValueError(
                f"Combined MP overlay references unknown participants: {unknown}"
            )

    def precommand_elements(self, participant_id: str, profile):
        """Rebuild baseline fixed attrs then reapply persistent reverse flag."""
        pid=str(participant_id)
        if pid not in self.att_reverse_by_participant_id:
            raise KeyError(f"Combined reverse state absent for {pid}")
        attrs=att_reverse_precommand_refresh(
            battle_flags=(
                _RECONSTRUCTION_REVERSE_BIT
                if self.att_reverse_by_participant_id[pid] else 0
            ),
            reverse_bit=_RECONSTRUCTION_REVERSE_BIT,
            earth=int(profile.earth),water=int(profile.water),
            fire=int(profile.fire),wind=int(profile.wind),
        )
        return attrs

    def cast_att_reverse(self, participant_id: str, profile):
        """Toggle the semantic flag and return same-round fixed attributes.

        Turning the flag off intentionally leaves currently reversed fixed
        attributes unchanged until the next pre-command rebuild, matching the
        accepted BATTLE_MultiAttReverse -> BATTLE_AttReverse ordering.
        """
        pid=str(participant_id)
        if pid not in self.att_reverse_by_participant_id:
            raise KeyError(f"Combined reverse state absent for {pid}")
        was_on=bool(self.att_reverse_by_participant_id[pid])
        out=att_reverse_cast_transition(
            battle_flags=_RECONSTRUCTION_REVERSE_BIT if was_on else 0,
            reverse_bit=_RECONSTRUCTION_REVERSE_BIT,
            earth=int(profile.earth),water=int(profile.water),
            fire=int(profile.fire),wind=int(profile.wind),
        )
        rows=dict(self.att_reverse_by_participant_id)
        rows[pid]=bool(out["battle_flags"] & _RECONSTRUCTION_REVERSE_BIT)
        overlay=CombinedRuntimeOverlay(
            self.initiative_profile,self.status_magic_profile,self.item_zero,
            self.mp_by_participant_id,rows,
        )
        return overlay,out["attributes"]
