# StoneAge terminal battle settlement — R1

Date: 2026-09-20

Status: **reconstruction-safe state-return boundary; reward semantics remain OPEN unless separately evidenced**

## Purpose

The persistent battle model already determines terminal HP and the ordinary
`victory` / `defeat` result. This R1 closes the smallest safe bridge from
that terminal battle state back into the single-player persistent domain.

It is intentionally not a reward system.

## 1. Settlement accepts only a finished battle

Implementation:

- `SinglePlayerHistoricalRuntime.finish_persistent_battle()`

The adapter rejects any state whose phase is not `finished` or whose result
is missing.

This prevents an in-progress battle snapshot from being committed as an
ordinary world-state return.

## 2. Direct state projected back

R1 copies only values that are already authoritative in the terminal battle
state:

- battle result;
- player terminal HP;
- terminal HP for each allied pet that participated.

Allied-pet updates are keyed through their preserved source pet slot. Missing
source-slot or terminal-HP identity fails explicitly.

Enemy HP is transient battle state and is not written into player persistence.

## 3. Existing world-return guards remain authoritative

The settlement adapter delegates the actual persistent mutation to the
existing `apply_battle_outcome()` boundary.

That preserves two important safety properties:

- the player's world position must still equal the original battle position;
- settlement may update only fields that already exist in the persistent
  player/pet state.

Therefore this seam cannot introduce an unverified reward field simply by
including it in a battle result object.

## 4. EXP is now a separate, narrower settlement seam

The direct HP-only adapter remains unchanged.

A second explicit runtime adapter,
`finish_persistent_battle_without_level_crossing()`, may additionally apply
battle-local pending EXP when the award remains strictly below the currently
exposed `max_exp` boundary.

That restriction is intentional. Taiwan v1 exposes separate EXP/max-EXP
status fields, while descendant server source preserves two incompatible
level-transition regimes. Below the threshold both simply add the award; at
the threshold their EXP-state mutation diverges.

Canonical EXP reconstruction record:

- `research/mechanics/STONEAGE-BATTLE-EXP-SETTLEMENT-R1.md`

Still not inferred or applied here:

- threshold-crossing player or pet level-up;
- level-up stat/growth side effects;
- item drops;
- money;
- capture;
- escape;
- death penalties;
- automatic healing/revival;
- post-battle warp;
- equipment durability;
- later private-server reward modifiers.

## 5. Regression coverage

`tests/test_stoneage_group_battle_runtime.py` verifies that:

- active battle state cannot be settled;
- a finished player victory returns the terminal player HP;
- an allied participant's terminal HP returns to its persistent pet slot;
- player and pet EXP remain unchanged;
- the world position remains the battle origin.

Remote validation:

- commit `6212cd394646778b2c47c07c931b5415efbec94e`;
- workflow run **35513868341** — success.

## Consequence

The in-process path now has a deterministic lifecycle through:

`world -> encounter -> spawned group battle -> multi-round HP -> termination -> direct HP/result return -> world`

Ordinary single-hit EXP provenance, kill attribution, pending accumulation and
below-threshold persistence are now closed to a reconstruction-safe boundary.

The next EXP problem is specifically the **level-transition profile**. The
legacy cumulative-threshold path and later per-level-consumption path must stay
versioned until original-era evidence selects one for the early baseline.
