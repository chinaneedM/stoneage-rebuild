# StoneAge Descendant Pet Growth Core — R1

Date: 2026-09-18

## Purpose

This note reconstructs the pet-growth chain preserved across multiple StoneAge server-source descendants and connects it to the recovered `enemybase.txt` data.

It is a **descendant-source reconstruction**, not yet a claim that every coefficient is proven for the 1999 JSS retail server.

## 1. Source convergence

The following independent lineages preserve the same core pet-rank and level-up formulas:

- `BismarckDD/stoneage` commit `999ffdf1d220ec6666eb65339180689c9caf1876`
- `gavinlinasd/StoneAge` commit `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
- `iriselia/StoneAge` commit `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`

The iriselia lineage preserves Japanese comments explicitly describing:

- pet rank calculation;
- ten four-sided random allocations;
- rank-based random growth;
- calculation from allocation/growth points.

## 2. Template data anchor

The recovered active `enemybase.txt` exposes the four template growth components:

- `BASEVITAL`
- `BASESTR`
- `BASETGH`
- `BASEDEX`

Those fields already parse deterministically in the recovered enemybase probe.

The pet rank is **not stored directly in enemybase**.

Instead the server calculates:

```text
template_sum =
    BASEVITAL
  + BASESTR
  + BASETGH
  + BASEDEX
```

and maps it to rank:

| Template sum | PETRANK |
| ---: | ---: |
| >= 100 | 0 |
| 95–99 | 1 |
| 90–94 | 2 |
| 85–89 | 3 |
| 80–84 | 4 |
| < 80 | 5 |

Thus a smaller PETRANK number corresponds to the higher template-growth sum.

## 3. Individual growth-base variation at enemy creation

Before the enemy/pet instance is created, each of the four base growth components is independently modified by:

```text
RAND(0,4) - 2
```

Therefore each component receives an individual offset from **-2 through +2**.

The server then packs these four individualized values into `CHAR_ALLOCPOINT`:

```text
bits 31..24 = vital growth base
bits 23..16 = strength growth base
bits 15..8  = toughness growth base
bits 7..0   = dexterity growth base
```

Important distinction:

- `PETRANK` is calculated from the **unmodified template values**;
- `CHAR_ALLOCPOINT` stores the **individualized ±2 values**.

This creates individual growth variance among pets that share the same template and PETRANK.

## 4. Separate initial-stat randomization

After `CHAR_ALLOCPOINT` has already been packed, the server performs ten additional random allocations:

```text
repeat 10 times:
    choose one of vital / str / tgh / dex
    chosen component += 1
```

These values participate in construction of the spawned enemy's current stats.

They are distinct from the already packed growth-base bytes.

Therefore the creation path contains two conceptually separate random layers:

1. **growth-base individuality** — four independent -2..+2 offsets, persisted in `CHAR_ALLOCPOINT`;
2. **spawn/current-stat random allocation** — ten random +1 assignments used when constructing current stats.

## 5. Capture preserves the growth identity

When an enemy is converted into a captured pet, the descendant `pet.c` copies:

- `CHAR_PETRANK`
- `CHAR_ALLOCPOINT`

directly from the enemy instance into the pet instance.

This means the individualized growth base is not regenerated at capture time.

The growth identity generated when the enemy instance was created survives capture.

## 6. PETRANK multiplier ranges

On each pet level-up, the source uses the following rank-dependent random range:

| PETRANK | Random integer | Multiplier |
| ---: | ---: | ---: |
| 0 | 450–500 | 4.50–5.00 |
| 1 | 470–520 | 4.70–5.20 |
| 2 | 490–540 | 4.90–5.40 |
| 3 | 510–560 | 5.10–5.60 |
| 4 | 530–580 | 5.30–5.80 |
| 5 | 550–600 | 5.50–6.00 |

This creates a compensating relationship:

- templates with higher four-stat growth totals receive lower rank numbers and lower multiplier ranges;
- templates with lower growth totals receive higher rank numbers and higher multiplier ranges.

This should not be simplified into “higher PETRANK is simply a better pet.” It is part of a balancing formula.

## 7. Ten-point per-level random allocation

For each level-up:

```text
Param = [0,0,0,0]

repeat 10 times:
    Param[RAND(0,3)] += 1
```

Therefore the ten bonus allocation points are multinomially distributed across:

- vital
- strength
- toughness
- dexterity

The total always remains exactly 10.

## 8. Per-level growth calculation

Let:

- `B[i]` = the pet's individualized growth-base byte from `CHAR_ALLOCPOINT`;
- `P[i]` = how many of the ten random allocation points landed on stat `i`;
- `R` = the rank multiplier randomly selected from the PETRANK range.

Then each stat's raw increment is:

```text
increment[i] = int((B[i] + P[i]) * R)
```

where the C cast truncates toward zero.

The resulting increments are added to:

- `CHAR_VITAL`
- `CHAR_STR`
- `CHAR_TOUGH`
- `CHAR_DEX`

Bismarck later wraps the cast with `max(0,...)`; for normal non-negative growth bases this does not change the core result.

## 8.1 Multi-level transition and loyalty-variable side effect

The battle result path invokes `CHAR_PetLevelUp()` once for each gained level
and immediately follows each call with:

```text
CHAR_PetAddVariableAi(pet, AI_FIX_PETLEVELUP)
```

Cross-lineage constants preserve:

```text
AI_FIX_PETLEVELUP = +5 * 100 = +500
CHAR_VARIABLEAI range = -10000 .. +10000
```

`CHAR_VARIABLEAI` is hidden persistent loyalty variation stored at x100 scale.
It is **not** the v1-visible pet AI value. `CHAR_complianceParameter()` later
combines owner level/charm, pet level, template `MODAI`, and VARIABLEAI to
produce `CHAR_WORKFIXAI`, which is what the pet status protocol sends.

The reconstruction model therefore now represents each gained level with one
`PetLevelGrowthRolls` bundle (ten allocation rolls + one rank roll) and
`advance_pet_growth()` applies all bundles in order while adding/clamping
VARIABLEAI by +500 after every level.

Later family/teacher fame code inside descendant `CHAR_PetLevelUp()` is
explicitly excluded from this stable core.
## 9. Why this matters for reconstruction

The pet system is not merely:

```text
species + level = fixed stats
```

The source-backed model contains persistent individual variance:

```text
enemybase template
  -> template PETRANK
  -> individual ±2 growth-base offsets
  -> packed CHAR_ALLOCPOINT
  -> captured pet preserves rank + allocation point
  -> every level:
       ten random stat allocations
       + rank-range random multiplier
       -> four stat increments
```

This explains why two pets of the same species and level can develop differently even before later training/equipment systems.

For the modern rebuild we should preserve these as separable policy layers:

- template growth values;
- individual birth variance;
- rank-band multiplier;
- per-level random allocation;
- later optional training/modification systems.

That separation lets us reproduce the historical behavior first and later decide which randomness to retain, expose, rebalance or make more transparent.

## 10. Evidence boundaries

Strong multi-lineage descendant evidence:

- rank thresholds 100/95/90/85/80;
- rank multiplier bands 450–600;
- ten four-sided allocations per level;
- four-stat level-up equation;
- `CHAR_ALLOCPOINT` byte packing;
- capture preserving `PETRANK` and `CHAR_ALLOCPOINT`.

Recovered-data corroboration:

- active `enemybase.txt` contains the four template growth fields needed by the formula.

OPEN:

- exact confirmation that the earliest JSS retail server used the same coefficients;
- whether all later-visible training/rank-edit systems existed in the target early historical version;
- precise player-facing scaling/display conversion between internal growth units and UI presentation.
