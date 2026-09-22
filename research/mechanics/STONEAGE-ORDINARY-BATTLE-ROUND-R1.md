# StoneAge ordinary attack / guard / wait round resolution — R1

Date: 2026-09-20

Status: **stable-descendant FACT / reconstruction-safe execution boundary; JSS-era server provenance remains OPEN**

## Purpose

This closes the first deterministic battle-effect seam after encounter and
enemy birth:

```
submitted commands
 -> action values
 -> descending action order
 -> execution-time target validation / retarget
 -> dodge / critical
 -> physical + elemental damage
 -> guard reduction
 -> HP subtraction
```

It deliberately does not invent enemy AI or later battle systems.

## Evidence anchors

Primary stable descendant:

- `gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
  - `gmsv/src/battle/battle.c`
  - `gmsv/src/battle/battle_event.c`

Independent descendant comparison remains available through the previously
recorded StoneAge source lineage.

The implementation remains a bridge/reference model. It is not a claim that
every coefficient has already been proven byte-for-byte for the 1999 JSS
server.

## 1. Action ordering

The stable battle loop calculates each entry's DEX/action value, then calls
`qsort` with a comparator equivalent to:

```
second.dex - first.dex
```

so larger action values execute first.

The recovered ordinary action-value profile remains:

```
work = QUICK + 20
dex  = work - RAND(0, int(work * 0.30))
dex  = max(1, dex)
```

The source comparator returns zero for equal action values. C `qsort` does
not define a historical stable tie order, so the reconstruction refuses to
invent one: equal action values require an explicit caller-supplied
`tie_break_order`.

## 2. Guard is a submitted stance, not a speed-gated activation

`BATTLE_AttackSeq()` inspects the defender's already stored COM1 command.

If COM1 is GUARD:

- `BATTLE_DuckCheck()` immediately returns false;
- the defender therefore does not dodge that ordinary attack;
- critical checking still occurs;
- after damage calculation, `BATTLE_GuardAdjust()` reduces the damage.

Consequently a slow guard actor is already guarding when a faster attacker
acts earlier in the same round. The reconstruction records guard stance from
the submitted command set before executing the sorted action list.

## 3. Dead actors are skipped when their turn arrives

The stable battle loop checks battle/death state again immediately before
executing the sorted entry.

The reconstruction therefore keeps the original sorted order but emits
`skipped_dead` when an earlier action reduced that actor to zero HP.

## 4. Target validation and execution-time retarget

For an ordinary melee command the stable path calls `BATTLE_TargetAdjust()`
at action execution time.

If the submitted target is no longer valid,
`BATTLE_DefaultAttacker()`:

1. scans living entries on the opposing side in battle-slot order;
2. constructs a candidate list;
3. chooses `RAND(0, candidate_count - 1)`.

The deterministic reconstruction therefore requires an explicit
`retarget_roll` only when the original target has become invalid.

Same-side ordinary attacks remain rejected unless the current actor's
source-shaped confusion tick explicitly rewrote the target for that turn.
That provenance is carried per actor and is never inherited by a later entry.

## 5. Dodge and critical order

The stable single-hit path performs:

1. dodge check;
2. guardian check;
3. critical check;
4. damage calculation.

Guardian behavior is not yet promoted into R1, but the relative dodge /
critical order is preserved.

The minimal dodge core uses fixed DEX and player-only fixed LUCK. Its stable
random comparison is:

```
RAND(1, 10000) <= dodge_probability
```

The critical core uses fixed DEX, player-only fixed LUCK and weapon critical.
Its stable random comparison is slightly different:

```
RAND(1, 10000) < critical_probability
```

That one-character difference is retained explicitly.

Guard suppresses the ordinary dodge check but does not suppress critical.

## 6. Physical defense profile remains explicit

Two stable source branches are already preserved by the project:

- compiled descendant `newpower_70pct`;
- preserved older mixed-stat expression.

The project still does not claim which branch belongs to the earliest JSS
server, so round execution requires an explicit `defense_profile`.

No hidden default is used to erase that provenance uncertainty.

## 7. Four-attribute damage

The stable ordinary damage path applies the four elemental attributes after
the physical base calculation.

Constants:

- same: **1.0**
- advantage: **1.5**
- disadvantage: **0.6**
- attribute maximum basis: **100**

Element order is earth / water / fire / wind, with a derived neutral remainder:

```
none = max(0, 100 - earth - water - fire - wind)
```

Recovered relationships include:

- fire > wind; fire < water;
- water > fire; water < earth;
- earth > water; earth < wind;
- wind > earth; wind < fire;
- neutral vs elemental uses the disadvantage coefficient.

The source stores the elemental subtotals in integer lvalues, so the
reconstruction preserves C-style truncation at those assignments.

The battlefield elemental scalar is also retained as an explicit
`field_attr / field_power` input. With no battlefield attribute, attacker and
defender scalars are both 0.5 and cancel.

## 8. Critical damage

For a non-bow ordinary critical, stable `BATTLE_CriDamageCalc()` first runs
normal damage calculation, then adds:

```
defender_WORKDEFENCEPOWER
* attacker_level / defender_level
* 0.5
```

R1 excludes bows, so this additive term is used only in the non-bow ordinary
path.

## 9. Guard reduction and zero damage

After ordinary/critical damage:

`BATTLE_GuardAdjust()` uses the already recovered distribution:

- 1..25 -> 0%
- 26..50 -> 10%
- 51..70 -> 20%
- 71..85 -> 30%
- 86..95 -> 40%
- 96..100 -> 50%

If damage is then below 1, the stable source replaces it with
`RAND(0,1)`.

If the resulting damage is zero:

- ordinary attack -> MISS;
- guarding target -> ALLGUARD.

## 10. HP application

For the no-ride path, post-AttackSeq damage now passes through the stable base
DamageReact layer. VANISH, ABSROB and REFLEC are modeled with source priority,
charge consumption and HP redirection; ordinary Reflect also redirects
wakeup/status to the attacker, while Absorb/Vanish suppress wakeup. Ride-pet
sharing and knock-away/ultimate state remain outside this section.

## 11. Explicit combat profile boundary

The reconstructed round requires a `BattleCombatProfile` containing:

- fixed DEX;
- fixed LUCK;
- earth/water/fire/wind;
- weapon critical.

These values are not automatically inferred from similarly named client
display fields where the exact early server WORK-stat bridge remains
unproven.

This preserves a clean distinction between:

- directly recovered combat arithmetic; and
- still-open client-display -> server-work-stat provenance.

## Implementation

Core arithmetic:

- `tools/stoneage_battle_core_model.py`

Round command/order/effect execution:

- `tools/stoneage_battle_round_model.py`

Single-player runtime bridge:

- `tools/stoneage_singleplayer_runtime.py`

Regression coverage:

- `tests/test_stoneage_battle_core_model.py`
- `tests/test_stoneage_battle_round_model.py`
- `tests/test_stoneage_group_battle_runtime.py`

Validated remote runs:

- battle-core **35512116840** — success;
- gameplay/runtime **35512186213** — success.

## Counter execution extension — 2026-09-21

The ordinary resolver now has an explicit opt-in counter path. Supplying
`counter_rolls_by_attack_id` enables the stable base `BATTLE_Counter()`
continuation loop; leaving it as `None` preserves the earlier no-counter R1
boundary for callers that have not yet supplied counter RNG.

The recovered source order is preserved:

1. a main ordinary attack leaves a continuation flag only when it was not a
   critical, did not strike a guarding target, and did not kill the target;
2. the original defender is the first counter candidate;
3. the candidate must still be alive, use ATTACK, and not carry ABIO;
4. the exact player/non-player counter check runs;
5. on success the ordinary attack sequence resolves and positive damage is
   multiplied by `0.75` with C-style truncation and minimum 1;
6. surviving NORMAL or DODGE may hand control back to the other actor;
7. MISS, CRITICAL, death, failed eligibility/check, or five attempts stop the
   chain.

Counter events carry their actual actor identity. This is intentional: the
persistent battle layer can therefore reuse the existing kill/death/drop seam,
and a player-side counter kill is credited to the counter actor rather than the
original main attacker.

The extension still excludes guardian interception, damage reactions,
abnormal-status effects and later special counter modifiers.

## Combo formation and execution extension — 2026-09-22

The stable base combo seam is now reconstructed through formation, status-free
damage execution and existing reward ownership.

- Formation runs after action-value sorting.
- Base starter chance is `RAND(1,100) <= 20` for enemies and `<= 50` for non-enemies.
- Only contiguous ATTACK entries with the same side and target, movable state and non-throwing weapons join.
- `BATTLE_AttackSeq(..., BATTLE_COM_COMBO)` skips dodge but retains critical/guard/damage handling.
- Each member contributes at least 1 damage after AttackSeq; damage is accumulated and target HP is mutated only when the final member applies the total.
- A group reduced to one viable member falls back to ordinary ATTACK through the recovered `ComboCheck2()` behavior.
- In both pinned descendants `_Item_ReLifeAct` is enabled and combo dispatch passes the complete attack list to `BATTLE_AddProfit()`. The persistent model therefore sends that same full list into the already-closed EXP/loyalty/drop allocation seam rather than inventing a combo-specific reward rule.

Early-JSS confirmation of that later-gated compile path remains a provenance question.

Validated state: commit `1bcbf15a07652f194d78b20c29a59a452f6b00cf`; battle-core run **35670646011** and gameplay run **35670645876** succeeded.

## Common base-status integration — 2026-09-22

The ordinary and persistent battle layers now consume the common six-status runtime recovered in `STONEAGE-BATTLE-STATUS-CORE-R1.md`.

- status processing occurs when the sorted actor reaches its turn;
- paralysis/sleep/stone can clear the current command before counters decrement;
- poison decrements first and, while still active, applies the recovered non-lethal `Compute_Down()` HP loss;
- confusion can rewrite the current command/target with explicit RNG, including same-side targets;
- stone doubles the supported defense profile during ordinary physical resolution;
- positive direct damage clears sleep immediately and increments the damage counter;
- status counters and work QUICK persist across rounds; dead allied entries remain in persistent status state even when omitted from the next active-entry projection.

Base-status interaction with counter/combo is deliberately rejected for now instead of being guessed.

Validated effective state: commit `9c79098637943d8101a612e8e5ee80de6b694656`; battle-core run **35671549996** and gameplay run **35671550039** succeeded.

## Deliberately excluded from R1

- automatic enemy command/AI selection;
- counter variants that require guardian/reaction/status or later special-command extensions;
- combo variants that require guardian/reaction/status/ride-pet or later item bonuses;
- guardian interception;
- bow and boomerang specialized behavior;
- ride-pet damage sharing and ride-pet fall-off;
- macro-gated reaction families such as TRAP/ACUPUNCTURE and later reaction extensions;
- later macro-gated status families and base-status interaction with counter/combo;
- pet/profession skills;
- item/magic actions and their status-application hooks;
- exact JSS-1999 provenance for descendant-only compile switches.

## Consequence

The project now has a deterministic in-process ordinary/persistent battle
execution layer covering attack/guard/capture/escape, status-free counter and
combo, common base-status timing, concrete HP mutation and the existing
source-shaped EXP/drop/death/return seams.

The next battle milestone is status **application/acquisition** and then the
explicit interaction seams between status, counter/combo, guardian and damage
reactions; it is no longer persistent-state scaffolding.

## Base DamageReact integration — 2026-09-22

The common no-ride DamageReact path is now connected to ordinary and Combo
execution.

- Priority is VANISH > ABSROB > REFLEC > NONE.
- Any active reaction on the ordinary main attacker or current defender
  suppresses counter continuation before AttackSeq.
- Guardian redirection happens first; DamageReact then reads the actual
  post-Guardian defender.
- Non-throw Reflect consumes one charge and redirects HP, wakeup and
  StatusChange targeting to the attacker.
- Throwing weapons bypass Reflect without consuming its charge.
- Absorb heals and Vanish preserves HP; both suppress DamageWakeUp, while a
  positive StatusChange attack still performs its later status check.
- Combo evaluates reactions per member. Immediate Reflect/Absorb/Vanish is
  applied member-by-member; only non-reacted member damage enters the final
  aggregate settlement. The settlement event preserves the full combo
  attack-list for reward attribution.

Validated effective state: commit
`466505c6f2f95b17431bdb5d8964a99a56bb7fab`; battle-core
**35692745170**, gameplay **35692745208**, pet-skill **35692745206**.

The next physical-damage seam is ride-pet sharing.
