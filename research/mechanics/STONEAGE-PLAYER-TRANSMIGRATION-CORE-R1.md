# StoneAge Player Transmigration Core R1

Status: **strong convergent descendant evidence; launch-era identity remains OPEN**  
Scope: stable player transmigration core before the later sixth/seventh-transmigration extensions.

## Purpose

Player creation and player growth now have deterministic models. This note reconstructs the next progression boundary: the ordinary transmigration gate, the cumulative inheritance equation, proportional stat redistribution, and the final level/EXP/free-point reset.

The reconstruction deliberately separates the common five-transmigration core from later `_TRANS_6`, `_TRANS_7`, VIP, profession, teacher, pet-transmigration and other extension paths.

## Evidence set

Fixed source revisions:

- **BismarckDD/stoneage** @ `999ffdf1d220ec6666eb65339180689c9caf1876`
  - `server/gmsv/npc/npc_transmigration.c`
  - `server/gmsv/char/char_base.c`
- **gavinlinasd/StoneAge** @ `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
  - `gmsv/src/npc/npc_transmigration.c`
  - `gmsv/src/char/char_base.c`
- **iriselia/StoneAge** @ `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
  - `Source/gmsv/npc/npc_transmigration.c`
  - `Source/gmsv/char/char_base.c`

## Stable ordinary gate

**FACT — convergent descendant code**

Before the later sixth-transmigration branch is enabled, the ordinary core permits at most five transmigrations.

A candidate must satisfy:

- level >= `80`;
- no unspent player stat points at the confirmation step;
- event flags `39,40,42,46`;
- for transmigration counts 0..3, carry the corresponding required pet ID:
  - 0 -> `693`
  - 1 -> `694`
  - 2 -> `695`
  - 3 -> `696`
- for the fifth transmigration (old count 4), carry all four IDs `693,694,695,696`.

The old commented pet-level check is not active in the preserved core and is therefore not modeled as a requirement.

## Cumulative history word

**FACT — convergent descendant code**

`CHAR_TRANSEQUATION` packs two cumulative counters:

- upper 16 bits: accumulated qualifying quest count;
- lower 16 bits: accumulated transmigration levels.

At each transmigration:

```
accumulated_quests += current_quest_count
accumulated_levels += min(current_level, 130)
```

The per-transmigration level contribution is therefore capped at `130`.

## Inherited-point equation

The transmigration counter is incremented **before** the status equation is evaluated. Let:

- `P` = old VITAL+STR+TOUGH+DEX internal total / 100;
- `Q` = updated accumulated quest count;
- `L` = updated accumulated capped-level total;
- `N` = new transmigration count.

The common core computes:

```
A = int(P / 12 + Q / 4 + (L - N * 85) / 4)
```

`int` here follows C truncation toward zero.

The value `A` is then distributed back across VITAL/STR/TOUGH/DEX in the same proportions as the old internal stats.

## Preserved rounding helper

All three lineages preserve the same helper:

```c
num--;
p = pow(10, num);
return ((work * p + 0.5) / p);
```

For the actual call `Rounding(tmp, 1)`, this returns `tmp + 0.5`; it is not equivalent to Python `round(tmp)`.

The status path then multiplies that float by `100` and assigns it to an integer stat slot. R1 mirrors the source literally rather than silently replacing it with conventional rounding.

This behavior should remain marked for future validation against an authoritative early binary/client-server pair.

## Reset outcome

**FACT — convergent descendant code**

After status conversion, the ordinary main path:

- sets level to `1`;
- calls `CHAR_setMaxExp(...,0)`, whose implementation writes `CHAR_EXP=0`;
- finally sets free stat points to `new_transmigration_count * 10`;
- runs parameter compliance;
- restores HP to the recomputed maximum.

An older/intermediate status step divides the previous free-point value by 12, but the main path then unconditionally overwrites `CHAR_SKILLUPPOINT` with `N*10`. The deterministic model therefore represents the final persisted outcome, not the transient overwritten value.

## Quest-table version divergence

The inheritance equation consumes a **quest count**, but the exact 20 event IDs are not identical in all preserved descendants.

gavinlinasd and iriselia retain:

```
1,2,4,5,8,12,14,15,16,17,19,22,27,30,31,34,35,38,45,47
```

BismarckDD currently retains:

```
1,2,4,5,8,12,14,15,16,17,19,22,27,30,31,34,35,38,44,45
```

Therefore R1 models `quest_count` as an input and does **not** collapse these divergent event tables into one invented canonical table.

## Later extensions excluded from R1

Examples explicitly kept outside the core:

- `_TRANS_6` and its alternate old-point behavior/pet/item requirements;
- `_TRANS_7`;
- hero/angel requirements;
- pool capacity expansion;
- teacher/profession changes;
- pet-transmigration branches;
- fork-specific quest-table changes;
- configurable rewards/presents.

These remain valid version-diff evidence, not baseline facts.

## Deterministic model

- `tools/stoneage_player_transmigration_model.py`
- `tests/test_stoneage_player_transmigration_model.py`
- `.github/workflows/validate-stoneage-player-transmigration.yml`

The tests cover gate conditions, first/fifth pet requirements, literal source rounding, inheritance math, level-130 accumulation cap, and the final level/EXP/free-point reset.

## Progression chain after this milestone

```
creation
  -> ordinary level growth
  -> battle/reward EXP
  -> stat-point spending
  -> transmigration eligibility
  -> cumulative quest/level history
  -> proportional inherited stats
  -> level 1 / EXP 0 / N*10 free points
  -> ordinary growth resumes
```

## Evidence status

- **FACT:** three preserved descendant lineages agree on the common level-80 / five-transmigration gate structure, core event flags, and pet-ID sequence.
- **FACT:** they agree on the cumulative level cap of 130 and the common inheritance equation.
- **FACT:** they agree on proportional redistribution and the unusual `Rounding(...,1)` helper semantics.
- **FACT:** they agree that the final main-path state resets level/EXP and assigns `10 * transmigration_count` free points.
- **FACT:** exact quest event IDs drift between descendant branches; the count equation is more stable than the table.
- **HYPOTHESIS:** this common core descends from the early official transmigration implementation family.
- **OPEN:** which exact quest-ID table belongs to each historical commercial version.
- **OPEN:** direct JSS/1999 proof for the gate, pet IDs and inheritance constants.
- **OPEN:** authoritative interpretation of the source rounding helper against an early executable.
- **OPEN:** chronology and exact rules of sixth/seventh transmigration extensions.

## Next technical seam

With creation -> growth -> battle/reward -> transmigration now connected, the next high-value creation/progression seam is **starter-pet and hometown linkage**, including which birth village selected which original pet and how later unified-newbie-village/configuration branches changed that mapping.
