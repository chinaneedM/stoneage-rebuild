"""Bounded non-player Combined -> DirectUse -> ordinary wrapper witness.

This is an executable reference boundary, not an ordered battle executor.
In particular an item configuration ID is never an item-pool instance index.
"""
from dataclasses import dataclass

EFFECTS = ("recovery", "status_change", "status_recovery", "att_reverse")


class CombinedDirectMagicDomain(ValueError):
    """A required source-state witness is absent or outside this boundary."""


def _integer(value):
    if type(value) is not int or not -(2**31) <= value < 2**31:
        raise CombinedDirectMagicDomain("requires signed int32 witness")
    return value


@dataclass(frozen=True)
class RuntimeItemZeroWitness:
    """Observed ITEM_CHECKINDEX(0) and, when valid, ITEM_MAGICUSEMP.

    A missing witness is distinct from a witnessed invalid item slot. The
    latter returns -1 from the actual accessor and can increase caster MP.
    """
    valid: bool
    magic_use_mp: int | None = None

    def __post_init__(self):
        if type(self.valid) is not bool:
            raise CombinedDirectMagicDomain("item validity must be observed boolean")
        if self.valid:
            _integer(self.magic_use_mp)
        elif self.magic_use_mp is not None:
            raise CombinedDirectMagicDomain("invalid item cannot carry a live MP field")

    @property
    def accessor_value(self):
        return self.magic_use_mp if self.valid else -1


@dataclass(frozen=True)
class CombinedDirectMagicRoute:
    accepted: bool
    remaining_mp: int
    item_reads: int
    wrapper_calls: int
    battle_effect_calls: int
    mp_argument: int | None
    reason: str


def resolve_combined_direct_magic_route(
    *, effect, current_mp, item_zero=None, nocast=0, caster_valid=True,
    battle_mode_init=False, battling=True, target_slot=0,
    function_present=True, battle_effect_return=True, family_index=0,
):
    """Audit the no-family-modifier non-player source wrapper sequence.

    Selection RNG belongs to the preceding callback. This route consumes no
    selection draw and must not refund that draw on Nocast or MP rejection.
    The effect seam reports the original wrapper return, not target mutation.
    """
    if effect not in EFFECTS:
        raise CombinedDirectMagicDomain("effect outside positive Combined choices")
    current_mp = _integer(current_mp)
    nocast = _integer(nocast)
    target_slot = _integer(target_slot)
    if family_index != 0:
        raise CombinedDirectMagicDomain("family MP multiplier requires separate evidence")
    if nocast > 0:
        return CombinedDirectMagicRoute(False, current_mp, 0, 0, 0, None, "nocast")
    if not isinstance(item_zero, RuntimeItemZeroWitness):
        raise CombinedDirectMagicDomain("runtime item slot 0 witness required")
    mp = item_zero.accessor_value
    if not function_present:
        return CombinedDirectMagicRoute(False, current_mp, 1, 0, 0, mp, "missing_function")
    if not caster_valid:
        return CombinedDirectMagicRoute(False, current_mp, 1, 1, 0, mp, "invalid_caster")
    if battle_mode_init:
        return CombinedDirectMagicRoute(False, current_mp, 1, 1, 0, mp, "battle_init")
    if current_mp < mp:
        return CombinedDirectMagicRoute(False, current_mp, 1, 1, 0, mp, "insufficient_mp")
    remaining = _integer(current_mp - mp)
    if not battling:
        raise CombinedDirectMagicDomain("field route is outside Combined battle boundary")
    if effect == "recovery" and target_slot == 22:
        return CombinedDirectMagicRoute(False, remaining, 1, 1, 0, mp, "recovery_all_rejected_after_mp")
    # Recovery discards its battle helper's return; the other three propagate it.
    accepted = True if effect == "recovery" else bool(battle_effect_return)
    return CombinedDirectMagicRoute(accepted, remaining, 1, 1, 1, mp, "battle_effect_seam")
