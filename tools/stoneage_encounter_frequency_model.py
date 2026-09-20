#!/usr/bin/env python3
"""Stable-descendant StoneAge movement-side encounter-frequency (CEP) model.

CEP = Current Encounter Probability in the inspected descendant connection
state. This module preserves the observed clamp / roll / reset / increment
ordering with explicit randomness. It is descendant evidence, not yet an
independent Taiwan-v1.0/JSS server fact.
"""

from __future__ import annotations

from dataclasses import dataclass

from tools.stoneage_tw10_25_encounter_bridge import EncounterAreaBridge


ROLL_MODULUS = 120


@dataclass(frozen=True)
class EncounterFrequencyState:
    current: int = 0
    minimum: int = 0
    maximum: int = 0

    def __post_init__(self) -> None:
        current = int(self.current)
        minimum = int(self.minimum)
        maximum = int(self.maximum)
        if minimum < 0 or maximum < 0:
            raise ValueError("encounter probability bounds must be >= 0")
        if minimum > maximum:
            raise ValueError("encounter probability minimum exceeds maximum")
        object.__setattr__(self, "current", current)
        object.__setattr__(self, "minimum", minimum)
        object.__setattr__(self, "maximum", maximum)


@dataclass(frozen=True)
class EncounterFrequencyDecision:
    before: EncounterFrequencyState
    clamped_current: int
    roll: int | None
    roll_hit: bool
    encounter_triggered: bool
    encounter_suppressed: bool
    after: EncounterFrequencyState


def refresh_frequency_bounds(
    state: EncounterFrequencyState,
    area: EncounterAreaBridge | None,
) -> EncounterFrequencyState:
    """Replace bounds only when a zone lookup succeeds."""
    if area is None:
        return state
    return EncounterFrequencyState(
        current=state.current,
        minimum=int(area.probability_min),
        maximum=int(area.probability_max),
    )


def resolve_frequency_step(
    state: EncounterFrequencyState,
    *,
    roll: int | None,
    encounter_enabled: bool = True,
    eligible: bool = True,
) -> EncounterFrequencyDecision:
    """Resolve one movement-side CEP update.

    Observed stable-descendant order:
    1. clamp CEP to [min,max];
    2. if processing is eligible, test rand()%120 < CEP;
    3. an unsuppressed hit triggers encounter and resets CEP=min;
    4. a hit suppressed by ordinary Warp leaves CEP at its clamped value;
    5. a miss increments CEP by one up to max.

    eligible=False models the no-processing path after the clamp.
    """
    clamped = min(max(int(state.current), state.minimum), state.maximum)

    if not eligible:
        after = EncounterFrequencyState(
            current=clamped,
            minimum=state.minimum,
            maximum=state.maximum,
        )
        return EncounterFrequencyDecision(
            before=state,
            clamped_current=clamped,
            roll=None,
            roll_hit=False,
            encounter_triggered=False,
            encounter_suppressed=False,
            after=after,
        )

    if roll is None:
        raise ValueError("eligible encounter-frequency step requires roll")
    roll = int(roll)
    if not 0 <= roll < ROLL_MODULUS:
        raise ValueError(f"roll must be in 0..{ROLL_MODULUS - 1}")

    hit = roll < clamped
    triggered = hit and bool(encounter_enabled)
    suppressed = hit and not bool(encounter_enabled)

    if triggered:
        next_current = state.minimum
    elif hit:
        next_current = clamped
    else:
        next_current = clamped + 1 if clamped < state.maximum else clamped

    after = EncounterFrequencyState(
        current=next_current,
        minimum=state.minimum,
        maximum=state.maximum,
    )
    return EncounterFrequencyDecision(
        before=state,
        clamped_current=clamped,
        roll=roll,
        roll_hit=hit,
        encounter_triggered=triggered,
        encounter_suppressed=suppressed,
        after=after,
    )
