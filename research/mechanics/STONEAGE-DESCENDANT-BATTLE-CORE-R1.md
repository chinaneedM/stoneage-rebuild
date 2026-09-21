# StoneAge Descendant Battle Core — R1

Date: 2026-09-18

## Purpose

This document reconstructs the **stable descendant battle core** that is useful as an archaeological reference for later StoneAge reimplementation.

It is **not** promoted to a 1999 JSS retail fact. No original JSS server source has been recovered.

Evidence is separated into:

- **stable descendant core** — behavior independently preserved in multiple StoneAge server-source lineages;
- **compiled descendant branch** — behavior enabled by a known macro in the inspected source;
- **preserved older branch** — code still present under an inactive/alternate macro path;
- **later extension** — behavior explicitly tied to later itemset/profession/pet-skill features;
- **source divergence / suspected branch bug** — incompatible behavior across descendants that must not be silently normalized.

## Source lineages

Primary inspected lineages:

1. `BismarckDD/stoneage`
   - commit `999ffdf1d220ec6666eb65339180689c9caf1876`
   - `server/gmsv/battle/battle.c`
   - `server/gmsv/battle/battle_event.c`
   - `server/gmsv/include/version.h`

2. `gavinlinasd/StoneAge`
   - commit `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
   - `gmsv/src/battle/battle.c`
   - `gmsv/src/battle/battle_event.c`
   - `gmsv/src/include/version.h`

Independent controls:

3. `iriselia/StoneAge`
   - commit `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
   - `Source/gmsv/battle/battle.c`
   - `Source/gmsv/battle/battle_event.c`

4. `chuyiwen/chuyiwen_gmsv`
   - commit `426cf0ccab33d38aa3b0118889a13bb38e26f7b9`
   - `battle/battle.c`
   - preserves Japanese comments such as “素早さを計算する” and “素早さは値が大きい方が優れている。降順ソートである。”

## 1. Stable numeric constants

The inspected older lineages preserve the same constants:

```text
DAMAGE_RATE       = 2.0
D_16              = 1 / 16
D_8               = 1 / 8
KAWASHI_MAX_RATE  = 75
gKawashiPara      = 0.02
gCounterPara      = 0.08
gCriticalPara     = 0.09
```

These are strong source-lineage anchors.

They remain **descendant evidence**, not a claim that the October 1999 retail server used exactly these values.

## 2. Turn action value / initiative

### 2.1 Stable older base behavior

Three older lineages preserve the same ordinary-command shape:

```text
work = QUICK + 20
action_value = work - RAND(0, work * 0.30)
```

Ride-pet branches replace `QUICK` with a ride-adjusted quick value before adding 20.

The older code then clamps a non-positive result to at least 1. One source explicitly comments that this was the official negative-speed treatment before a later modification changed it to a random 1–5 result.

The result is therefore not simply “higher DEX always moves first.” It is:

1. derive current battle `QUICK`;
2. add 20;
3. apply command-specific random/order modifiers;
4. sort the resulting action values in descending order.

This creates deliberate turn-order uncertainty while still strongly favoring faster units.

### 2.2 Item use

Older descendants preserve:

```text
work = QUICK + 20
action_value = work - RAND(0, work * 0.30) + work * 0.15
```

Item use therefore receives an approximately +15% offset relative to the same random base.

### 2.3 Sorting and execution

The battle loop:

1. creates one `BATTLE_CHARLIST` entry per battle participant;
2. assigns `dex = BATTLE_DexCalc(...)`;
3. sorts the list with `EntrySort`;
4. performs combo detection over the sorted list;
5. iterates the sorted list from index 0 upward and executes each unit's action.

The Japanese-comment source explicitly says the speed comparison is a **descending sort where larger speed values are better**.

### 2.4 Later `sequence` extension

`_EQUIT_SEQUENCE` is annotated as an equipment action-order feature requiring **itemset5**.

Some descendants sort by:

```text
dex + sequence
```

rather than just `dex`.

This is a later equipment extension and should not be projected backward into the base combat model.

### 2.5 Source divergences

Do not normalize these away:

- `gavinlinasd` and `iriselia` preserve ordinary `0–30%` random subtraction.
- `chuyiwen` also preserves 30% as the non-`_DEX_FIX` path.
- `BismarckDD` changes the ordinary/item path to **0–10%**, and its attack-magic order path to a fixed `0–15` subtraction.
- `BismarckDD`'s `_EQUIT_SEQUENCE` comparator returns only a boolean 0/1 expression instead of a negative/zero/positive ordering difference. This is incompatible with normal `qsort` comparator semantics and is retained as a **suspected descendant branch bug**, not an ancestral rule.
- `chuyiwen` comments out the `sequence` comparator and sorts only by `dex`, even while carrying the surrounding sequence extension code.

For reconstruction, the safest historical baseline is therefore:

**base action order = descending randomized speed; equipment sequence is a later optional layer.**

## 3. Physical damage core

### 3.1 Defense construction has two preserved generations

All three major server branches inspected define `_BATTLE_NEWPOWER`.

Under that compiled descendant branch:

```text
effective_defense = DEFENCEPOWER * 0.70
```

The source also preserves an alternate older branch:

```text
effective_defense =
    DEFENCEPOWER * 0.45
  + QUICK        * 0.20
  + FIXVITAL     * 0.10
```

For a ride-pet defense path the preserved older branch uses a smaller vital contribution.

Important: the mere presence of the older branch does not prove which formula JSS 1999 used.

### 3.2 Base damage is piecewise

After attack/effective-defense construction, the stable descendant formula has three regions.

If attack is below defense:

```text
damage = RAND(0, 1)
```

If:

```text
defense <= attack < defense * 8/7
```

then:

```text
damage = RAND(0, attack / 16)
```

If:

```text
attack >= defense * 8/7
```

then:

```text
K0 = RAND(0, attack / 8) - attack / 16
damage = 2 * (attack - defense) + K0
```

The result is then passed through elemental adjustment.

This is materially different from a simple `attack - defense` game.

### 3.3 Stone status

A petrified defender doubles effective defense before the piecewise physical calculation:

```text
defense *= 2
```

### 3.4 Later modifiers

Multiple later compile-time extensions can add:

- enemy random power changes;
- ignore-defense percentages;
- extra damage / extra defense;
- profession effects;
- ride-pet adjustments;
- item effects.

These are not part of the minimal stable model.

## 4. Elemental adjustment

The physical result is passed to `BATTLE_AttrAdjust`.

The descendant battle model retains the familiar four attributes:

- earth
- water
- fire
- wind

The routine:

1. reads attacker and defender elemental values;
2. applies optional battle-property callbacks in later branches;
3. computes elemental matchup through `BATTLE_AttrCalc`;
4. applies battlefield elemental power adjustment.

Therefore element is not an independent second attack. It modifies the already calculated physical damage result in this path.

Exact JSS-era matchup coefficients remain a separate reconstruction target.

## 5. Dodge / hit relationship

The stable `BATTLE_DuckCheck` core uses attacker and defender fixed dexterity, plus defender luck for player defenders.

Relationship modifiers include:

- enemy → pet: attacker DEX × 0.8;
- non-enemy → pet: defender DEX × 0.8;
- non-player → player: attacker DEX × 0.6;
- player → non-player: defender DEX × 0.6.

Then:

```text
Big   = max(adjusted attacker DEX, adjusted defender DEX)
Small = min(...)
```

If defender DEX is at least attacker DEX, `wari = 1`.

Otherwise:

```text
wari = Small / Big
```

Base dodge work:

```text
Work = (Big - Small) / 0.02
per  = sqrt(Work) * wari
per += defender_luck
```

The result is converted to a 1–10000 scale and capped at **75%**.

Later code adds command, drunkenness, bow, hit-right, profession and passive-skill modifiers. Some bow additions differ across descendants, so they are not part of the minimal cross-lineage model.

## 6. Critical

The stable player-style critical routine uses:

- attacker fixed DEX;
- defender fixed DEX;
- attacker luck when attacker is a player;
- weapon `ITEM_CRITICAL` value.

Default divisor:

```text
gCriticalPara = 0.09
```

The same attacker/defender-type asymmetries appear again. In ordinary root-mode cases:

```text
Work = (Big - Small) / 0.09
per = (sqrt(Work) + weapon_critical * 0.5) * wari
per += attacker_luck
per *= 100
```

The final check uses a 1–10000 random scale.

Certain enemy↔pet / non-player→player branches switch to a linear `Work` form with divisor 10 instead of the square-root form.

### Critical damage

Stable descendant code first calculates normal damage, then adds:

```text
DEFENCEPOWER
* attacker_level / defender_level
* 0.5
```

Bow handling diverges from ordinary melee critical damage in the inspected attack sequence.

## 7. Counter

The counter check has now been re-read directly from two pinned independent
descendant trees:

- `gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`;
- `iriselia/StoneAge@9e6c8ce2cd8ed532a7157773acd1c61582c178b5`.

Both preserve the same `BATTLE_CounterCalc`, `BATTLE_CounterCheckPlayer`,
`BATTLE_CounterCheckPet`, weapon mapper and counter table.

The DEX basis uses:

```text
gCounterPara = 0.08
```

and the same type asymmetries already modeled by `raw_counter_basis()`.
One C-semantic detail is important: `Work` is an **int**, so

```text
Work = (Big - Small) / divisor
```

truncates toward zero *before* the square-root or linear branch. The returned
counter basis is also an int.

### 7.1 Weapon categories and source anomaly

The source enum contains NONE / CLAW / AXE / CLUB / SPEAR / BOW / THROW /
OTHER, and the literal `CounterTbl` contains these seven stored rows:

```text
10  9  8  8  5  0  0  0
10  9  7  7  6  0  0  0
 9  8 10 10  7  0  0  0
 8  8 10 10  7  0  0  0
 6  6  8  8  9  0  0  0
 0  0  0  0  0  0  0  0
 0  0  0  0  0  0  0  0
```

`BATTLE_ItemType2ItemMap()` maps fist→CLAW, axe→AXE, club→CLUB,
bow→BOW and boomerang/bound-throw/break-throw→THROW. **ITEM_SPEAR is not
mapped in either pinned source**, despite the SPEAR enum/table column existing;
it therefore falls through to NONE. This is preserved as a descendant-source
behavior/anomaly rather than silently repaired.

`BATTLE_IsThrowWepon()` independently rejects bow, boomerang, break-throw
and bound-throw on **either** counter participant before the random check.

### 7.2 Player counter actor

For a player counter actor the stable base branch is:

```text
basis   = BATTLE_CounterCalc(counter_actor, target)
matchup = CounterTbl[actor_weapon][target_weapon]
per     = basis * matchup * 0.1 + actor_FIXLUCK
threshold = per * 100
RAND(1,10000) < threshold
```

The comparison is strict `<`. The later `_SUIT_ADDENDUM` counter modifier
is explicitly excluded from the base reconstruction.

### 7.3 Non-player counter actor

The non-player branch does **not** apply the weapon matchup table or player
luck. After the throwing-weapon gate it uses the raw DEX basis, caps it above
100, multiplies by 100 and compares with **inclusive** `<=`:

```text
per = min(100, BATTLE_CounterCalc(...))
threshold = per * 100
if threshold <= 0: threshold = 1
RAND(1,10000) <= threshold
```

That literal lower-bound handling gives a zero-basis non-player counter a
1-in-10000 success boundary. It is preserved rather than normalized away.

The probability/check seam is deterministic. The base status-free
`BATTLE_Counter()` execution seam is also now modeled behind explicit counter
RNG inputs:

- the first candidate counter actor is the defender from the main attack;
- only an ATTACK-command actor can counter in the base seam;
- ABIO candidates are rejected;
- a successful check reuses ordinary dodge / critical / physical / attribute
  resolution;
- positive counter damage is truncated after multiplication by `0.75`, with
  the source minimum of 1 preserved;
- MISS and CRITICAL stop the chain, as does killing the target;
- DODGE and surviving NORMAL results may continue;
- the battle loop alternates the two actors for at most five counter attempts.

Main-attack continuation is likewise source-shaped for the supported seam:
critical, guarding target, or target death suppress the chain; ordinary
NORMAL/MISS/DODGE against a surviving non-guarding target permit it.

Guardian interception, damage-reaction systems, abnormal statuses and the
later special `BATTLE_COM_S_NOGUARD` modifier remain excluded. Counter EXP
continues to flow through the already-closed actual-counter-actor profit
attribution rather than a new reward rule.

## 8. Guard

The stable guard routine draws `RAND(1,100)` and multiplies incoming damage by:

| Roll | Damage multiplier |
| --- | ---: |
| 1–25 | 0.00 |
| 26–50 | 0.10 |
| 51–70 | 0.20 |
| 71–85 | 0.30 |
| 86–95 | 0.40 |
| 96–100 | 0.50 |

Guard is therefore a stochastic mitigation distribution, not a single fixed percentage.

## 9. Attack resolution order

The stable `BATTLE_AttackSeq` chain is approximately:

1. dodge check, except selected combo handling;
2. guardian substitution;
3. critical-rate calculation;
4. critical or normal physical damage calculation;
5. command/skill-specific damage modifiers;
6. guard reduction where applicable;
7. if result is below 1, fallback random 0/1 behavior;
8. later branch-specific modifiers/equipment effects.

This ordering matters. For example, guardian substitution occurs before the critical/damage calculation against the final defender.

## 10. Encounter-to-battle bridge already recovered

The recovered server data chain established immediately before this combat pass is:

```text
map position
  -> encount region
  -> weighted group
  -> weighted enemy instance
  -> enemybase template
  -> battle
```

The movement-side encounter mechanism is also source-backed:

```text
CEP is clamped to zone min/max
each eligible step tests rand() % 120 < CEP
success -> encounter, CEP resets to zone min
failure -> CEP increments toward zone max
```

This means battle frequency uses an increasing-probability / soft-pity mechanism rather than a fixed independent percentage per step.

## 11. Battle EXP and progression bridge

Three independent descendant server lineages preserve the same per-enemy reward constants and level-gap rule:

```text
EXPGET_MAXLEVEL = 5
EXPGET_DIV      = 15
```

Each defeated enemy supplies its own `CHAR_EXP` value. In the recovered server-data lineage that value originates from the `EXP` field in `enemy.txt` when the enemy instance is created.

For each eligible battle participant:

```text
level_diff = receiver_level - enemy_level

if level_diff <= 5:
    award = enemy_exp
else:
    factor = 5 + 15 - level_diff

    if factor > 15:
        factor = 15

    if factor <= 0:
        award = 1
    else:
        award = enemy_exp * factor / 15

    if award < 1:
        award = 1
```

Therefore:

- a receiver from any lower level through **+5 levels above the enemy** receives full enemy EXP;
- at **+6** the reward becomes `14/15`;
- the reward falls linearly through **+19**, where it is `1/15`;
- at **+20 or more** the base path gives the minimum **1 EXP**;
- fighting an enemy above the receiver does not create an extra over-level bonus in this core formula.

In the inspected inner reward loop, the adjusted enemy EXP is added to every eligible participant's `CHAR_WORKGETEXP`; this particular step does **not** divide one enemy's EXP pool by participant count.

### Ride pet

The ride pet runs the same level-gap calculation and then:

```text
ride_pet_award *= 0.60
```

Because the variable is an integer, this truncates. The code does not reapply the minimum-one rule after the 60% multiplication, so a far-overlevel ride pet whose base award became 1 can receive **0**.

### Progression chain

The recovered/server-source chain is now:

```text
enemy.txt EXP
  -> spawned enemy CHAR_EXP
  -> per-defeated-enemy level-gap adjustment
  -> CHAR_WORKGETEXP accumulation
  -> BATTLE_GetExp / CHAR_AddMaxExp
  -> exp.txt level thresholds
```

This distinguishes two different pieces of progression data that should remain separate in a modern rebuild:

- **enemy reward value** — how much a defeated enemy is worth;
- **level threshold table** — how much accumulated experience is required to level.

Later descendants add many optional modifiers such as equipment EXP boosts, server-wide multipliers, special pets and other private-server adjustments. One Bismarck branch even contains very recent custom minimum-EXP logic. Those layers are explicitly excluded from this stable core.

Evidence grade: **strong multi-lineage descendant evidence**, with recovered `enemy.txt` and `exp.txt` providing the corresponding data-side anchors. Exact JSS-1999 reward coefficients remain OPEN.

## 12. Reconstruction guidance

When the modern rebuild begins, preserve these concepts separately:

- **historical baseline model** — the best-supported early mechanism;
- **descendant active model** — what a particular recovered/private server branch actually compiled;
- **modern design model** — the version we deliberately choose after discussion.

Do not silently copy descendant bugs.

In particular:

- keep base initiative randomness as a configurable rule;
- make later equipment `sequence` a distinct modifier;
- express physical damage, element, critical, counter and guard as separate stages;
- retain deterministic tests for whichever historical profile is selected;
- do not hard-code private-server profession extensions into the base StoneAge combat layer.

## Evidence-grade summary

- base randomized initiative concept: **strong multi-lineage descendant evidence**
- ordinary `QUICK+20 - RAND(0, 30%)` profile: **strong older-lineage convergence; Bismarck later divergence exists**
- descending initiative execution: **strong multi-lineage descendant evidence**
- equipment `sequence` modifier: **later extension, explicitly tied to itemset5**
- Bismarck boolean qsort comparator: **descendant branch anomaly / suspected bug**
- `DAMAGE_RATE=2`, `D_16`, `D_8`, dodge/critical/counter constants: **strong multi-lineage descendant evidence**
- `_BATTLE_NEWPOWER` defense = 70% DEFENCEPOWER: **compiled descendant branch**
- 45% DEF + 20% QUICK + 10% VITAL defense: **preserved alternate/older branch; original-version status OPEN**
- three-region physical damage formula: **strong multi-lineage descendant evidence**
- elemental adjustment after physical base damage: **strong multi-lineage descendant evidence**
- dodge, critical and counter DEX asymmetries: **strong multi-lineage descendant evidence**
- guard multiplier distribution: **strong multi-lineage descendant evidence**
- battle EXP full-through-+5 / 15-level decay / minimum-one rule: **strong multi-lineage descendant evidence**
- ride-pet EXP = 60% after the same level-gap rule: **strong multi-lineage descendant evidence**
- enemy reward data -> battle award -> exp.txt threshold chain: **descendant-source + recovered-data corroborated**
- exact 1999 JSS combat/progression coefficients: **OPEN pending original server/binary evidence**
