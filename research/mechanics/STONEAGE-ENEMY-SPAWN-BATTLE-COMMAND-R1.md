# StoneAge Enemy Spawn + First Battle Command Boundary — R1

Date: 2026-09-20

Status: **stable-descendant FACT / 2.5 bridge implementation; earliest JSS/Taiwan-server provenance still open**

## Purpose

This closes the first reconstruction-safe composition seam from a selected
encounter group into concrete enemy battle participants, and defines the first
engine-facing ordinary player-command boundary for a battle round.

It also corrects an earlier project simplification: a StoneAge encounter group
does **not** necessarily resolve to one enemy variant for the whole battle.

## Evidence anchors

Stable descendant source anchors:

- `gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
  - `gmsv/src/char/enemy.c`
  - `gmsv/src/include/enemy.h`
  - `gmsv/src/battle/battle_command.c`
- independently convergent comparison:
  - `iriselia/StoneAge@9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
- recovered project specimen:
  - mixed 2.5 `encount / group / enemy / enemybase` tables;
  - `enemybase.SIZE` is present and observed as the binary domain 0/1.

## 1. Correct encounter composition order

The stable `ENEMY_getEnemy()` path is:

```
position
 -> encounter area
 -> eligible weighted group
 -> effective total enemy capacity
 -> random target enemy count
 -> repeatedly weighted enemy-slot selection
 -> per-variant create cap / size-layout checks
 -> enemy variant list
 -> independent enemy birth for each selected variant
```

This means a single battle can contain multiple enemy variants from one group.

The old reconstruction `EncounterRequest` that preselected one variant is
retained only as a compatibility projection. The engine-facing reconstruction
now also exposes a group-level request before enemy-slot generation.

## 2. Total enemy count

For the selected group the source sums `CREATEMAXNUM` for each populated
enemy slot and then computes:

```
capacity = min(encount.ENEMY_MAX_NUM, sum(slot enemy.CREATEMAXNUM))
target_count = RAND(1, capacity)
```

Duplicate references to the same enemy ID contribute repeatedly to this summed
capacity.

## 3. Each enemy position is selected again

For every enemy position the source runs a new weighted selection using the
group's `CREATEPROB` values.

It does not select one enemy ID once and clone it across the encounter.

Rejected selections still consume an iteration/roll. The source loop has a
hard 100-iteration guard.

## 4. CREATEMAXNUM and duplicate slots

After selecting a candidate variant, the source counts:

- how many of that variant have already been placed;
- how many group slots reference that same variant.

The effective cap is:

```
enemy.CREATEMAXNUM * duplicate_slot_count
```

A candidate at its cap is rejected and the generation loop tries again.

## 5. CREATEMINNUM is not enforced in this stable path

`ENEMY_CREATEMINNUM` exists in the loaded enemy table and is retained by the
project bridge.

However, the inspected stable `ENEMY_getEnemy()` generation path does not
read it when choosing the encounter count or enforcing per-variant counts.

Therefore the reconstruction records it as a declared field but does not invent
a minimum-spawn rule from the field name.

## 6. Normal vs big enemy layout

`enemybase.SIZE` maps onto the stable enum:

- 0 = normal;
- 1 = big.

The stable generation path:

- allows at most five big enemies;
- when a sixth big enemy is selected, reduces the current target count by one;
- if a big enemy is selected after the first five positions, searches the first
  five positions for a normal enemy;
- if one exists, the big enemy is moved into that front position and the
  displaced normal enemy moves to the later slot;
- if no normal enemy exists in the first five, that selection attempt is
  rejected.

The reconstruction requires explicit SIZE data. Unknown SIZE is not silently
treated as normal.

## 7. Each selected enemy receives independent birth randomness

For each final selected enemy variant, stable enemy creation independently
chooses:

- level in `[LV_MIN, LV_MAX]`;
- four base-stat offsets, each equivalent to `RAND(0,4)-2`;
- ten allocation rolls in `0..3`.

The already recovered birth bridge then applies:

```
scale = (level - 1) * LVUPPOINT + INITNUM
stat  = scale * individualized_base
```

before projecting the combat stats.

Thus two enemies of the same template/level may still have different birth
state.

## 8. First ordinary player battle commands

The first reconstruction-safe command boundary covers stable core dispatcher
forms:

- `H|<hex target>` -> physical attack;
- `G` -> guard;
- `N` -> wait;
- `E` -> escape;
- `T|<hex target>` -> capture.

Target indices are constrained to the stable 20-position battle domain
(`0..19`). Invalid parsed attack/capture targets become `-1`, matching the
dispatcher assignment behavior rather than being silently repaired.

For attack/guard/escape/capture, the stable dispatcher checks the actor's error
status and recursively falls back to `N` when action is disallowed.

The action boundary combines the typed command with the already recovered
ordinary initiative formula using an explicit random subtraction.

## 9. MP calls are not promoted as costs

The inspected command dispatcher calls `BATTLE_MpDown(...)` for several
commands, but in the fixed descendant source the compiled `#if 1` branch of
`BATTLE_MpDown` immediately returns 0 and does not mutate MP.

Therefore this R1 boundary does not invent battle-command MP costs from those
call-site constants.

## 10. Deliberately excluded

This first command boundary does not yet claim or execute:

- profession skills;
- pet skill commands;
- item commands;
- magic/equipment command branches;
- boomerang-specific command substitution;
- AI command selection;
- capture success probability;
- escape success probability;
- damage/effect execution;
- victory/drop/EXP settlement.

Those remain separate archaeology/reconstruction seams.

## Implementation

- `tools/stoneage_enemy_spawn_model.py`
- `tools/stoneage_battle_command_model.py`
- group-level request in `tools/stoneage_singleplayer_domain.py`
- mixed-enemy session support in `tools/stoneage_singleplayer_battle.py`
- engine-facing integration in `tools/stoneage_singleplayer_runtime.py`
- regression coverage:
  - `tests/test_stoneage_enemy_spawn_model.py`
  - `tests/test_stoneage_battle_command_model.py`
  - `tests/test_stoneage_group_battle_runtime.py`

Remote combined validation:

- GitHub Actions run **35510677772** — success.

## Consequence

The reconstruction no longer has to pretend that one encounter means one enemy
template. It can now reproduce the stable group-level composition and create
independently individualized enemies before entering a battle session, while
keeping player command selection as an in-process game-domain action rather
than recreating the historical network server dispatcher.
