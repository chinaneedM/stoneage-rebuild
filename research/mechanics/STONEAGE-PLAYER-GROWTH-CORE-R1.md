# StoneAge Descendant Player Growth Core — R1

Date: 2026-09-18

## Purpose

This note reconstructs the stable descendant **player level-up, free-stat allocation, and base derived-stat formulas**.

It is an archaeological reference for the later modern rebuild. It is not yet promoted to an exact 1999 JSS retail-server fact.

## 1. Source convergence

The following independent StoneAge server-source lineages preserve the same base rules:

- `BismarckDD/stoneage` — commit `999ffdf1d220ec6666eb65339180689c9caf1876`
- `gavinlinasd/StoneAge` — commit `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
- `iriselia/StoneAge` — commit `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`

The earlier two lineages agree directly on the fixed three-point level-up rule. Bismarck keeps the same default path but also contains a later configurable override.

## 2. Experience threshold versus stat-point reward

The recovered descendant progression chain is:

```text
enemy EXP
  -> battle-local WORKGETEXP accumulation
  -> persistent CHAR_EXP application
  -> level-threshold check
  -> one or more level-ups
```

The threshold/EXP representation is **versioned** rather than singular:

- the legacy compiled path keeps cumulative `CHAR_EXP` and compares it with a
  cumulative next-level entry from the built-in `LevelUpTbl`;
- the later `_NEWOPEN_MAXEXP` path loads external per-level requirements,
  treats `CHAR_EXP` as current-level progress and subtracts the requirement
  at each level-up.

The mixed 2.5 external `exp.txt` therefore must not be described as the
default threshold source for the older path or silently promoted to a JSS-1999
fact.

When a player gains `UpLevel` levels, the stable older rule awards:

```text
free_stat_points += UpLevel * 3
```

The free points are stored in:

```text
CHAR_SKILLUPPOINT
```

Despite the name, this field is the ordinary player **free base-stat allocation pool** in this code path.

Bismarck later supports:

```text
UpLevel * getSkup()
```

behind a configuration feature; its setup defaults to 3. That configurable layer is a later server extension. The cross-lineage baseline remains **3 points per level**.

## 3. Four allocatable player stats

The allocation table is exactly:

| skillid | Internal stat | Conventional meaning |
| ---: | --- | --- |
| 0 | `CHAR_VITAL` | vitality / 体 |
| 1 | `CHAR_STR` | strength / 腕力 |
| 2 | `CHAR_TOUGH` | toughness / 耐久 |
| 3 | `CHAR_DEX` | dexterity / 速度 |

A point can be spent only when `CHAR_SKILLUPPOINT > 0`.

Spending one point performs:

```text
CHAR_SKILLUPPOINT -= 1
selected_internal_stat += 100
```

The status protocol displays the four values as:

```text
internal_value / 100
```

Therefore:

**one free point = +1 displayed unit of the selected base stat.**

## 4. Base derived-stat formulas

The stable `CHAR_initcharWorkInt` code first converts the four internal base stats into fixed work values.

Let displayed/raw logical stats be:

```text
V = CHAR_VITAL / 100
S = CHAR_STR   / 100
T = CHAR_TOUGH / 100
D = CHAR_DEX   / 100
```

The source uses floating arithmetic and then stores the result into integer work fields, so fractional results truncate.

### Fixed vitality

```text
FIXVITAL = int(V)
```

### Fixed dexterity / quick basis

```text
FIXDEX = int(D)
```

### Fixed strength / attack basis

```text
FIXSTR = int(
    S
  + 0.10 * T
  + 0.10 * V
  + 0.05 * D
)
```

### Fixed toughness / defense basis

```text
FIXTOUGH = int(
    T
  + 0.10 * S
  + 0.10 * V
  + 0.05 * D
)
```

### Maximum HP

```text
MAXHP = int(
    4 * V
  + S
  + T
  + D
)
```

Equivalently in the source's ×100 internal representation:

```text
MAXHP =
    (4*VITAL + STR + TOUGH + DEX) * 0.01
```

### Maximum MP

In this base recalculation path:

```text
WORKMAXMP = CHAR_MAXMP
```

It is copied from the stored max-MP field rather than derived from the four ordinary base stats here.

## 5. Base battle work values

Before equipment:

```text
ATTACKPOWER  = FIXSTR
DEFENCEPOWER = FIXTOUGH
QUICK        = FIXDEX
```

`CHAR_complianceParameter` then:

1. rebuilds base work values;
2. applies `ITEM_equipEffect`;
3. copies the resulting fixed STR / TOUGH / DEX work values back into final attack / defense / quick;
4. applies additional later work modifiers;
5. clamps current HP/MP to recalculated maxima.

This separation matters for a modern architecture:

- base stats are persistent character attributes;
- derived base work stats are calculated;
- equipment modifies the work layer;
- final combat values are produced after equipment/effect application.

## 6. What one displayed stat point contributes

Ignoring integer-threshold effects and equipment, one displayed point has the following continuous-form contributions:

| +1 stat | MAXHP | Attack basis | Defense basis | Quick basis |
| --- | ---: | ---: | ---: | ---: |
| Vitality | +4 | +0.10 | +0.10 | 0 |
| Strength | +1 | +1.00 | +0.10 | 0 |
| Toughness | +1 | +0.10 | +1.00 | 0 |
| Dexterity | +1 | +0.05 | +0.05 | +1 |

Because the derived work fields are integers, fractional contributions appear only after enough points accumulate to cross an integer boundary.

This is important when reproducing old character-build breakpoints.

## 7. Commented alternate formulas are not active rules

The source retains commented-out alternatives around `_BATTLE_NEWPOWER`, for example forms where fixed attack/defense receive only smaller VITAL/DEX cross-contributions.

Those lines are comments in all inspected branches and are **not the compiled formula used by the reconstructed path**.

They are useful historical residue, but must not be merged into the active formula.

## 8. Later profession restrictions are separate

Bismarck and related later branches add profession-specific caps such as restrictions on fighter/wizard/hunter allocations.

Those checks are under the later profession system and are explicitly excluded from the base player-growth reconstruction.

Likewise, configurable per-level stat-point rewards are treated as later policy overrides, not historical baseline facts.

## 9. Reconstruction model

The historical-descendant growth pipeline is best represented as:

```text
exp.txt threshold crossed
  -> levels gained
  -> +3 free points per level
  -> player spends each point on V/S/T/D
  -> selected stat += 100 internal units
  -> recompute:
       FIXSTR
       FIXTOUGH
       FIXDEX
       MAXHP
  -> apply equipment/effects
  -> final ATK / DEF / QUICK / MAXHP
```

For the modern rebuild, these should remain separable:

- level threshold policy;
- free-points-per-level policy;
- persistent base stats;
- base derived-stat formula;
- equipment modifier layer;
- later profession or progression caps.

That lets us reproduce the legacy baseline first and then deliberately redesign any one layer without accidentally changing all the others.

## 10. Evidence grade

Strong multi-lineage descendant evidence:

- 3 free base-stat points per level;
- four allocation targets VITAL / STR / TOUGH / DEX;
- one point consuming one pool point and adding 100 internal units;
- UI/base stat scale of 100 internal units per displayed point;
- FIXSTR / FIXTOUGH cross-contribution formulas;
- FIXDEX = displayed DEX;
- MAXHP = 4V + S + T + D;
- equipment applied after base work initialization.

Later descendant extension:

- configurable stat points per level;
- profession-specific stat caps;
- itemset5/6 work fields and later equipment systems.

OPEN:

- exact proof that the earliest 1999 JSS retail server used these same coefficients;
- original character-creation starting allocation and any launch-era hard caps;
- exact launch-era transmigration effects on the four base stats.
