# StoneAge base battle-status timing — R1

Date: 2026-09-22

Status: stable-descendant FACT / deterministic common-status seam; later
magic/profession extensions and JSS-1999 provenance remain separate.

## Evidence boundary

The common status order is identical in the pinned gavinlinasd and iriselia
descendant trees:

1. poison
2. paralysis
3. sleep
4. stone
5. drunk
6. confusion

Later weaken, deep-poison, barrier, silence, SARS and profession statuses are
kept outside this base seam even where the inspected descendants compile them.

## Turn-order semantics

The stable battle loop checks movement capability before decrementing status
counters. Paralysis, stone and sleep block movement. If blocked, COM1 is set to
NONE before the status loop runs.

Each active status counter is then decremented. A counter that reaches zero
expires immediately and does not execute its per-turn switch body.

The outer battle loop checks movement capability again after status processing.
This produces a source-shaped edge case: a one-turn paralysis can expire but
the already-cleared command remains NONE. A still-active confusion status can
rewrite that cleared command to ATTACK after the decrement; if no movement
blocker remains, that rewritten attack survives the second movement check.

## Poison

Common poison uses Compute_Down on the actor's raw VITAL + STR + DEX + TOUGH
sum. Integer division follows C truncation toward zero:

    down = (((stat_sum / 100) - 20) / 4)
    down = max(1, down)

If current HP is less than or equal to down, down becomes HP - 1. Poison
therefore cannot reduce a living actor below 1 HP in this base path.

Because the counter is decremented before the switch body, poison with counter
1 expires without another damage tick.

Ride-pet poison uses the same formula independently, but ride-pet HP coupling
is not yet connected to the current no-ride battle execution model.

## Confusion

After decrement, a still-active confusion status performs RAND(1,100). Values
1..80 rewrite the command to ATTACK. Values 81..100 leave the command as-is.

The target side is RAND(0,1). The starting position is RAND(0,9), then the
source increments the position before each target probe, wraps at 10, skips the
actor's own battle slot, and accepts the first valid target found in up to ten
probes. Failure stores target -1.

## Drunk expiration

When drunk reaches zero, the stable source restores work QUICK:

- without a ride pet: current QUICK * 2;
- with a ride pet: current QUICK + ride-pet QUICK.

The model requires those work-QUICK inputs explicitly instead of guessing them
from display QUICK.

## Sleep wake-up

Positive non-absorbed/non-vanished damage calls BATTLE_DamageWakeUp. That call
increments CHAR_DAMAGECOUNT and clears sleep immediately. Zero damage does not
wake the target.

## Implementation

- tools/stoneage_battle_status_model.py
- tests/test_stoneage_battle_status_model.py

## Ordinary and persistent battle integration

The base status runtime is now connected to the ordinary and persistent battle
layers. A living actor's status tick executes when that sorted actor reaches
its turn. The resulting HP/status/work-QUICK state is written back into
`PersistentBattleState` for the next round.

The integration preserves several source-order details:

- a one-count paralysis/sleep/stone can expire during the tick but the command
  it already cleared stays suppressed for that turn;
- a still-active confusion entry can rewrite that command later in the same
  status loop;
- positive damage can wake a sleeping actor before that actor's own turn, so
  its original submitted command can still execute;
- stone is projected into the ordinary physical-defense path;
- dead allied entries remain in persistent status storage even though the next
  round's executable entry list contains living actors only.

Counter/combo execution with active base statuses is intentionally rejected by
the current API and remains a separate source-recovery seam rather than an
implicit composition.

Validation:

- pure status model: commit `badeba6934d07a9c0605bdac13fd8b32b31501c1`, battle-core run **35671000903**;
- integrated effective state: commit `9c79098637943d8101a612e8e5ee80de6b694656`, battle-core **35671549996** and gameplay **35671550039**.

No later status family is implicitly enabled. The next status milestone is to
recover the ordinary status-application/resistance paths that create these
base counters.
