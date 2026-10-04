"""Ordered Refresh state projection over reconstructed battle status storage."""

from __future__ import annotations

from dataclasses import dataclass, replace

from tools.stoneage_battle_status_model import (
    BaseBattleStatusRuntime,
    base_status_name_from_index,
)
from tools.stoneage_nocast_runtime_state import NocastParticipantRuntime


@dataclass(frozen=True)
class RefreshActionRolls:
    """Only the descendant MultiList dead-single retarget path owns RNG."""

    retarget_draws_0_9: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        draws = tuple(int(value) for value in self.retarget_draws_0_9)
        if any(not 0 <= value <= 9 for value in draws):
            raise ValueError("Refresh retarget draws must be in 0..9")
        object.__setattr__(self, "retarget_draws_0_9", draws)

    @property
    def is_empty(self) -> bool:
        return not self.retarget_draws_0_9


def refresh_status_vector(
    base_runtime: BaseBattleStatusRuntime,
    late_runtime: NocastParticipantRuntime,
    *,
    require_complete: bool,
) -> tuple[int, ...]:
    """Project the modeled iris status-work counters into the 44-entry scan.

    Index 8 and later extension statuses are intentionally not guessed.  A
    target with any unmodeled active status cannot be used for highest-status
    recovery because its true maximum index would be ambiguous.
    """

    if not isinstance(base_runtime, BaseBattleStatusRuntime):
        raise TypeError("Refresh base status runtime has wrong type")
    if not isinstance(late_runtime, NocastParticipantRuntime):
        raise TypeError("Refresh late-status runtime has wrong type")
    if require_complete and late_runtime.unmodeled_status_active:
        raise ValueError("Refresh target has an unmodeled active status; highest-index recovery is ambiguous")

    values = [0] * 44
    values[1] = int(base_runtime.status.poison)
    values[2] = int(base_runtime.status.paralysis)
    values[3] = int(base_runtime.status.sleep)
    values[4] = int(base_runtime.status.stone)
    values[5] = int(base_runtime.status.drunk)
    values[6] = int(base_runtime.status.confusion)
    values[7] = int(late_runtime.weaken_counter)
    values[9] = int(late_runtime.barrier_counter)
    values[10] = int(late_runtime.counter)
    return tuple(values)


def apply_refresh_cleared_status(
    base_runtime: BaseBattleStatusRuntime,
    late_runtime: NocastParticipantRuntime,
    cleared_status: int | None,
) -> tuple[BaseBattleStatusRuntime, NocastParticipantRuntime]:
    """Apply one proved source clear while preserving current-command powers."""

    if cleared_status is None:
        return base_runtime, late_runtime
    status = int(cleared_status)
    if 1 <= status <= 6:
        name = base_status_name_from_index(status)
        return (
            replace(base_runtime, status=replace(base_runtime.status, **{name: 0})),
            late_runtime,
        )
    if status == 7:
        # Prepared Weaken powers describe the already prepared current command.
        # Keep them until the normal post-round preparation restores baseline.
        return base_runtime, replace(
            late_runtime,
            weaken_counter=0,
            weaken_active_at_visit=False,
        )
    if status == 9:
        return base_runtime, replace(
            late_runtime,
            barrier_counter=0,
            barrier_active_at_visit=False,
        )
    if status == 10:
        return base_runtime, replace(
            late_runtime,
            counter=0,
            nc_flag=0,
        )
    raise ValueError("Refresh attempted to clear an unmodeled status index")
