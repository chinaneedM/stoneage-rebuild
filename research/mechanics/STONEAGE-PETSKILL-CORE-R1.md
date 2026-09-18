# StoneAge Stable Pet-Skill Core R1

Status: **active fixed-descendant stable subset reconstructed and regression-modeled**  
Scope: the 15 active pet-skill callbacks that are simultaneously:

1. present in the recovered active `petskill.txt`;
2. present in all three pinned descendant dispatch tables;
3. unguarded in all three dispatch tables;
4. implemented by substantive unguarded function bodies in all three pinned source lineages.

Pinned source revisions:

- gavinlinasd/StoneAge `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
- iriselia/StoneAge `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
- BismarckDD/stoneage `999ffdf1d220ec6666eb65339180689c9caf1876`

This R1 layer is descendant-common evidence, **not proof that all 15 skills existed unchanged in the September/October 1999 launch build**.

## Active-table boundary

Recovered active `petskill.txt`:

- 147 rows;
- 69 unique callback tokens.

Textual fixed-source coverage:

- 65 tokens / 143 rows resolve in all three pinned source tables;
- 4 tokens / 4 rows resolve in none;
- no active token is only a one/two-lineage textual match.

That 65-token figure is **not** the common-core boundary.

Comment-aware guard classification gives:

- **15 unguarded-all-three tokens / 33 active rows**;
- **50 guarded-all-three tokens / 110 rows**;
- 0 mixed-guard;
- 0 partial-source;
- 4 all-source-missing / 4 rows.

Function-body refinement is unusually clean:

- **15 stable-body-all-three tokens / 33 rows**;
- 0 macro shells;
- 0 mixed body;
- 0 partial body source.

The four all-source-missing recovered rows remain quarantined as source/data skew. No behavior is invented for them.

## Stable active families

The 15 stable active callbacks are:

1. no action;
2. normal attack;
3. normal guard;
4. continuation attack;
5. charge attack;
6. guardian;
7. power balance;
8. mighty;
9. ordinary status-change attack;
10. earth round;
11. guard break;
12. abduct;
13. steal;
14. merge;
15. no-guard.

Active row counts by family:

- status change — 6;
- continuation attack — 4;
- charge — 3;
- power balance — 3;
- abduct — 3;
- no-guard — 3;
- mighty — 2;
- merge — 2;
- each remaining family — 1.

## Command-state architecture

Most ordinary pet skills do not execute their full effect inside `pet_skill.c`.

The handler writes battle command state:

- `CHAR_WORKBATTLECOM1` — command kind;
- `CHAR_WORKBATTLECOM2` — target slot;
- `CHAR_WORKBATTLECOM3` — packed skill parameters;
- `CHAR_WORKBATTLEMODE = BATTLE_CHARMODE_C_OK`.

The actual effect occurs later in battle command execution in `battle.c` / `battle_event.c`.

R1 therefore models both:

1. handler-side command encoding;
2. downstream stable execution behavior.

This avoids treating the callback function itself as the whole mechanic.

## None / attack / guard

The three simplest handlers only select ordinary battle commands:

- None -> `BATTLE_COM_NONE`;
- NormalAttack -> `BATTLE_COM_ATTACK`;
- NormalGuard -> `BATTLE_COM_GUARD`.

They set the target and command-ready mode.

## Continuation attack

The handler parses a leading integer attack count:

- valid range: 1..10;
- invalid/missing/out-of-range: 1.

It writes the count to the **low half** of COM3.

The high half is not cleared by the handler, so stale high-half state can survive even though this execution path does not consume it.

Execution:

```
attack_max = LOW(COM3)
gDamageDiv = attack_max
```

The normal attack loop then performs up to that many attacks and uses the attack count as the damage divisor.

So this is not simply “N full-damage attacks”; the fixed old combat layer explicitly sets `gDamageDiv=N`.

## Charge attack

The handler encodes:

- LOW(COM3): charge wait count N, range 1..10, default 1;
- HIGH(COM3): optional attack-percent parameter, default 0.

Each `BATTLE_Charge` execution step behaves as follows:

- while LOW > 0: decrement LOW by one and perform no action;
- when LOW <= 0:
  - rebuild attack power;
  - switch command to `BATTLE_COM_S_CHARGE_OK`.

Ready attack power is:

```
FIXSTR + FIXSTR * attack_percent * 0.01 + MODATTACK
```

The subsequent CHARGE_OK action enters the ordinary attack path and then resets the command.

N=1 therefore means one no-action charge turn before the ready attack.

## Guardian

Guardian can immediately modify the pet’s attack and defense work powers using optional percent parameters:

```
new = FIXED + FIXED * percent / 100
```

It sets `CHAR_BATTLEFLG_GUARDIAN` and registers a guardian slot in the battle entry table.

Two modes exist.

### Guardian attack mode

Default mode uses `BATTLE_COM_S_GUARDIAN_ATTACK` and typically registers the pet as guardian for its paired owner position.

### Defensive guardian mode

When the option contains the defensive COM marker, the skill switches to ordinary guard and registers the selected target as the guarded entry.

### Guardian redirect checks

Attack redirection only succeeds when the registered guardian:

- exists;
- is alive;
- still has the guardian flag;
- is not the defended slot itself;
- is not sleeping;
- is not confused;
- is not paralyzed;
- is not petrified;
- is not under the ordinary barrier status;
- is not the attacker;
- is not trying to intercept a thrown-weapon attack.

Guardian entries and guardian flags are cleared during battle pre-command setup, so registration is turn-local rather than permanent state.

## Power balance

The handler selects `BATTLE_COM_S_POWERBALANCE` and can immediately modify:

- attack power;
- defense power.

Optional attack/defense percentages use the same:

```
FIXED + FIXED * percent / 100
```

If the skill option pointer is null, the old handler returns FALSE **after** it has already written command/target/mode state.

When valid, PowerBalance later participates in the normal attack execution path.

## Mighty

The handler packs:

- LOW(COM3): damage multiplier ×100;
- HIGH(COM3): dodge modifier.

A significant old quirk is preserved.

The source initializes:

```
float fBai = 2.00;
int iBai = 0;
```

but only assigns `iBai = fBai * 100` when the multiplier marker is actually found.

Therefore an option missing the multiplier marker leaves LOW(COM3)=0, even though `fBai` had a nominal 2.00 default.

Execution then does:

```
gBattleDamageModyfy = LOW(COM3) * 0.01
gBattleDuckModyfy   = HIGH(COM3)
```

So missing the multiplier marker can produce a zero damage multiplier in this fixed implementation.

## Ordinary status-change attack

The handler:

- selects `BATTLE_COM_S_STATUSCHANGE`;
- scans ordinary status tokens;
- defaults turn count to 3;
- optionally adjusts attack/defense work powers;
- packs status in LOW(COM3);
- packs turn in HIGH(COM3).

### Invalid-status sentinel quirk

The old handler stores the loop variable `i`, not the separate `status` variable.

If no status token matches, `i` reaches `BATTLE_ST_END` and that sentinel value is still packed into LOW(COM3).

The later status checker rejects statuses outside the valid ordinary range.

### Status application

Before attack execution, COM3 is copied into global status/turn state.

The status can only be applied when the physical attack actually causes positive damage.

The stable `BATTLE_StatusAttackCheck` rejects application when the target already has any ordinary status.

Paralysis uses its special base:

```
20 - status-specific resistance
```

Other ordinary statuses use the fixed-base relationship:

```
PerOffset
+ clamped level delta * multiplier
+ attacker fixed luck
- status-specific resistance
- vitality-ratio penalty
```

where the vitality penalty is based on:

```
(VITAL / (VITAL + STR + TOUGH + DEX)) / 0.25 * 10
```

The normal non-PvP level term is clamped to ±40 in this call path and uses multiplier 2.0.

The stable core caps the final chance at 80 but does not add a corresponding lower clamp.

When application succeeds, the work timer is written as:

```
requested_turn + 1
```

Selected immobilizing statuses also clear the target’s pending command.

Later suit/equipment resistance additions remain macro/version layers and are not part of this base probability model.

## Earth round

EarthRound is a two-phase state machine.

### Phase 1 — hide

The handler selects `BATTLE_COM_S_EARTHROUND1`.

The execution helper:

- emits the hide/backstep state;
- clears `CHAR_ISATTACKED`;
- changes the command to `BATTLE_COM_S_EARTHROUND0`;
- returns FALSE in the fixed helper because its local result flag is never changed.

### Phase 2 — attack

`BATTLE_COM_S_EARTHROUND0` enters the ordinary attack path with:

```
gBattleDamageModyfy = 1.0 + 0.01 * COM3
```

After the attack it resets the command to NONE.

### COM3 stale-state hazard

The EarthRound handler writes COM3 only if its attack-percent marker exists.

If the marker is absent, the entire previous COM3 value survives and becomes the later EarthRound damage percentage.

R1 preserves this historical state-residue behavior rather than clearing COM3 defensively.

## Guard break

GuardBreak selects `BATTLE_COM_S_GBREAK` and can immediately raise/lower attack power via an attack-percent option.

Execution target-adjusts and invokes `BATTLE_S_GBreak`.

The stable old logic only resolves damage when the target:

- is currently using ordinary guard;
- is not confused.

Otherwise damage is forced to zero and the attack result becomes miss.

This makes the ordinary GuardBreak family a conditional anti-guard strike, not a general armor-piercing attack.

## Abduct

The handler stores the pet-skill array index in the low half of COM3 and leaves the high half untouched.

The base unguarded `BATTLE_Abduct` accepts PET or ENEMY attackers and rejects PLAYER defenders.

Without the later ABDUCTII extension, chance is:

```
int((defender_level - attacker_level) * 0.6 + 30)
per = max(per, 50)
```

That is a **minimum** of 50, not a maximum.

A battle with a non-null WinFunc forces chance to zero.

For an otherwise valid attempt:

- success can remove the target pet/enemy;
- the attacker exits battle whether the abduct roll succeeds or fails.

The later loyalty/Ai-based `_BATTLE_ABDUCTII` branch is not part of this stable base.

## Steal

The stable old `BATTLE_Steal` is narrower and stranger than its name suggests.

Target entry chance:

- player target: 50;
- non-player target: 0.

On a successful entry roll, a second 50% split chooses gold vs item mode.

### Gold mode

The target loses:

```
target_gold * RAND(8,12) * 0.01
```

If the result is <=0, the steal becomes failure.

The fixed implementation shown in all three lineages subtracts the gold from the target but does **not** credit matching gold to the stealing pet or owner in this function.

### Item mode

One occupied ordinary inventory slot is selected.

The target slot is cleared and the item instance is ended.

The fixed function does **not** transfer that item into the attacker’s inventory.

Thus the old “steal” implementation behaves as target asset removal/destruction, not a conventional transfer, at this source layer.

When steal remains successful, the stealing pet/enemy exits battle.

Bismarck uses a revised inventory upper-bound helper while preserving the same success/mode/removal semantics; that bound implementation is treated as descendant implementation drift rather than a different core action.

## Merge

Merge is unusual because it is an unguarded pet-skill callback that delegates to field/item logic rather than a battle command.

It checks the pet owner’s battle mode.

If the owner is in battle, the call fails.

Otherwise it delegates to:

```
ITEM_mergeItem_merge(owner, pet_id, data, pet_index, 0)
```

and returns that result.

This stable descendant callback must not be conflated automatically with later macro-gated pet-fusion/egg systems; historical introduction still requires earlier evidence.

## NoGuard

The handler parses and packs:

- HIGH(COM3): dodge value;
- LOW(COM3): `(counter << 8) + critical`.

The counter token is a simplified/traditional text variant across lineages; the packing algorithm is the same.

### Dead-parameter behavior

The stable battle execution switch for `BATTLE_COM_S_NOGUARD` only calls:

```
BATTLE_NoAction(...)
```

No other fixed common execution occurrence consumes those packed dodge/counter/critical values.

R1 therefore records the parsed values but marks them as unused by this old execution path.

### High-half residue

The handler only writes HIGH(COM3) when the dodge marker exists.

Without it, the previous high half remains.

LOW is always overwritten by the packed counter/critical value.

## COM3 residue as a historical implementation property

Several stable handlers use halfword setters rather than resetting the full field:

- ContinuationAttack overwrites LOW only;
- Abduct overwrites LOW only;
- NoGuard conditionally overwrites HIGH;
- EarthRound can leave the entire COM3 untouched.

These stale values are usually irrelevant to the immediate command, but EarthRound can consume stale full COM3 as a damage percentage.

A modern implementation should almost certainly use typed per-command state rather than a reused packed integer, but that is a redesign decision, not a historical reconstruction.

## Excluded pet-skill layer

Active recovered rows outside this R1 core include 50 all-three guarded callback families / 110 rows.

Examples include later feature-macro families for:

- attack magic;
- super-wall/magic status;
- guard-break variants;
- alchemy/fixing;
- mount/fall-ground;
- explosion;
- steal-money revision;
- extended enemy skills;
- timid/property/tear/light-take/crazed/shoot attacks;
- MP damage;
- deep poison;
- barrier;
- silence/no-cast;
- roar/SARS/sonic;
- transformations;
- combined/divide/bat-fly/battle-model families.

Their presence in the mixed recovered 2.5 table is valid content evidence, but they are not flattened into the stable common layer.

The four active all-source-missing callback rows remain quarantined.

## Reference model and validation

Artifacts:

- `tools/stoneage_petskill_core_model.py`
- `tests/test_stoneage_petskill_core_model.py`
- `.github/workflows/validate-stoneage-petskill-core.yml`
- `tools/stoneage_effect_callback_coverage_probe.py`
- `research/recovered/STONEAGE-25-EFFECT-CALLBACK-COVERAGE-R1.txt`

The model separates:

- handler-side command encoding;
- stable battle-execution transitions;
- injected random outcomes;
- later/macro extensions.

Initial dedicated CI run `35374550333` passed 44 tests.

After edge corrections for invalid-status sentinel, steal destruction semantics, and COM3 residue, the synchronized regression suite is expected to supersede that run; project state should cite the latest green run.

## Evidence boundary

- **FACT:** 15 active callback tokens / 33 rows are unguarded and substantive in all three fixed descendant lineages.
- **FACT:** 50 active tokens / 110 rows are guarded in all three.
- **FACT:** four active rows use callbacks absent from all three fixed source tables.
- **FACT:** the core handler formulas and key execution formulas above converge across the three pinned lineages, with text/format variants such as simplified/traditional option markers and Bismarck inventory-bound refactoring.
- **VERSIONED:** macro-gated pet skills remain explicit version layers.
- **OPEN:** which of the 15 stable-descendant skills existed in exactly this form in 1999/JSS and early 1.x.
