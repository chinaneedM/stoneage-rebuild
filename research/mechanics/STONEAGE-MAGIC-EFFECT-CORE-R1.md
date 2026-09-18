# StoneAge Ordinary Magic Effect Core R1

Status: **fixed-descendant convergent core reconstructed and regression-modeled**  
Scope: the nine magic callbacks that are present **without compile-time guards in all three pinned descendant source revisions**.

Pinned source lineages used for the R1 convergence boundary:

- gavinlinasd/StoneAge `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
- iriselia/StoneAge `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
- BismarckDD/stoneage `999ffdf1d220ec6666eb65339180689c9caf1876`

The recovered 2.5 data is still a mixed preservation specimen and does **not** prove that these descendant-era implementations equal the 1999/JSS launch build.

## Why this is a clean semantic boundary

The three fixed source dispatch tables share the same nine unguarded callback families:

1. Recovery
2. OtherRecovery
3. FieldAttChange
4. StatusChange
5. MagicDef
6. StatusRecovery
7. Ressurect
8. AttReverse
9. ResAndDef

The other common textual dispatch entries are all behind explicit feature macros in every inspected lineage, including attack magic, extra magic-status systems, metamorphosis, attack-skill magic, weaken, deep poison, barrier, silence and call-dragon extensions.

Therefore R1 does **not** flatten all 17 recovered active callback tokens into one “original core”. The nine unguarded families form the stable descendant common denominator; guarded families remain versioned until earlier evidence promotes them.

## Recovered active-table classification

The enhanced real-byte callback probe confirms that the active recovered `magic.txt` aligns exactly with the source guard boundary:

- 181 active magic rows total;
- 17 unique active callback tokens total;
- **9 unique tokens / 130 rows** map to callbacks that are unguarded in all three pinned source lineages;
- **7 unique tokens / 46 rows** map to callbacks that are guarded in all three pinned source lineages;
- **1 unique token / 5 rows** has partial source-lineage coverage;
- 0 mixed-guard tokens;
- 0 all-source-missing tokens.

This is unusually strong evidence that the nine-function R1 core is not an arbitrary source-code grouping: it is also a major active-data layer in the recovered specimen.

The 46 all-three guarded rows and 5 partial-source rows remain valid recovered content evidence, but their exact historical introduction dates are not inferred from the 2.5 specimen. The partial-source family is `MAGIC_AttSkill`: the fixed gavin/iriselia dispatch entries are commented out, while the fixed Bismarck table retains the callback behind `_ITEM_ATTSKILLMAGIC`.

## Dispatch and MP mutation order

The ordinary item/magic path is:

```
item
 -> ITEM_MAGICID
 -> MAGIC_getMagicArray
 -> MAGIC_FUNCNAME
 -> MAGIC_getMagicFuncPointer
 -> callback(caster, target, magic-array, mp-cost)
```

At callback level, the common wrapper order is:

1. validate caster index;
2. reject battle-init mode;
3. verify enough MP;
4. deduct MP;
5. decide battle versus field route;
6. parse the magic option and mutate battle/character state.

This ordering produces a real historical edge case:

> **battle-only common magic can fail because the caster is not actually battling after MP has already been deducted.**

The model preserves this rather than “fixing” it transactionally.

Recovery and OtherRecovery are the two common field-capable families. Their field target validity check also occurs after MP deduction.

## Target authority

The fixed old battle layout uses:

- slots `0..9` for side 0;
- slots `10..19` for side 1;
- selector `20` for all valid living/dead targets on side 0;
- selector `21` for all valid living/dead targets on side 1;
- selector `22` for all valid living/dead targets on both sides.

Ordinary living-target effects expand through `BATTLE_MultiList`.

Resurrection effects expand through `BATTLE_MultiListDead`, so only dead targets survive the ordinary selector filter.

For ordinary Recovery battle dispatch, `MAGIC_TARGET` adds packet-side validation:

- target mode `0`: only the caster's own battle slot is legal;
- target mode `1`: only a concrete single slot `< 20` is legal;
- other target modes delegate to the normal multi-target selector.

The Recovery wrapper also contains an old explicit `toNo == 22` rejection added as a whole-target bug fix. OtherRecovery does not contain that exact wrapper check.

### Target-list source hazard

The preserved old `TARGET_ALL` list-building path contains revision/macro-sensitive termination logic. In at least one old branch, the list terminator can be written at the loop index rather than the compacted target count.

R1 models the **intended logical target set**, not uninitialized stack-array behavior.

## Recovery

### Option parsing

Recovery parses the beginning of `MAGIC_OPTION` with C `atoi`.

Battle recovery additionally treats the presence of `%` anywhere in the option as a percentage flag.

### Random amount

The ordinary recovery amount starts from:

```
RAND(power * 0.9, power * 1.1)
```

For percentage battle recovery, the rolled value is then multiplied by:

```
target_MAXHP * 0.01
```

The resulting amount is multiplied by `GetRecoveryRate`.

### VITAL recovery multiplier

The fixed descendants share:

```
player:     1.0 + 0.00010 * VITAL
non-player: 1.0 + 0.00005 * VITAL
```

Final HP is capped at work MAXHP.

Field recovery uses the random amount and recovery-rate multiplier but has no `%` branch in the observed field function.

### Descendant riding interaction

The inspected battle recovery code also contains riding-pet HP distribution behavior.

Because ordinary player riding is separately classified as a later/versioned system in this project, the R1 ordinary core model does not promote riding distribution into the early baseline.

## Field attribute change

FieldAttChange is battle-only.

Its option parser searches for one of five attribute classes in source order:

```
none / earth / water / fire / wind
```

It then parses:

- field power, default `30`;
- valid power range `0..100`, otherwise reset to `30`;
- duration marker `turn`, default `3`.

On success the battle object receives:

- selected field attribute;
- attribute power;
- remaining attribute-turn count.

## Ordinary status application

StatusChange is battle-only.

The option parser selects a battle status token and defaults to:

- duration: `3` turns;
- success parameter: `15`.

Optional `turn` and success-marker values override those defaults.

Application delegates probability/resistance calculation to `BATTLE_StatusAttackCheck`. R1 preserves the parsed success input and the state transition, but leaves the deeper hit/resistance formula for the subsequent combat-submechanics layer.

On a successful ordinary status application:

- the target's status work timer is set to the requested duration;
- selected immobilizing statuses clear the target's pending battle command.

## Status recovery

StatusRecovery is battle-only.

A notable old implementation detail is preserved:

1. the source scans all ordinary status slots;
2. every active slot replaces the previous candidate;
3. the final candidate is therefore the **highest-index active status**;
4. only that one selected status can be cleared by this call.

The selected status is cleared when either:

- the requested recovery status exactly matches it; or
- requested status is `0` and the selected status lies within the ordinary bad-status range through confusion.

It does not iterate and clear all matching statuses.

## Magic defense

MagicDef is battle-only.

The option parser resolves a defense kind and a duration:

- default duration: `3` turns.

The target transition is direct:

```
MagicDefTbl[kind] = turn
```

A later cast of the same kind therefore overwrites that duration.

Friendly/enemy-side restrictions visible behind `_PREVENT_TEAMATTACK` are treated as a version/config layer, not part of the unguarded common core.

## Resurrection

Ressurect is battle-only and uses the dead-target selector.

Targets are skipped when:

- they are not dead; or
- the battle is PvP and the target is a player.

Option parsing produces:

- integer power;
- a `%` flag.

### Zero-power resurrection

`power == 0` restores by MAXHP before normal HP capping, effectively yielding full HP from the normal dead-state baseline.

### Nonzero resurrection

For nonzero power the code contains a preserved quirk:

1. it initially computes a percentage-derived value when `%` is present;
2. it then overwrites that value with `RAND(power * 0.9, power * 1.1)`.

Therefore the `%` marker has **no final HP effect for nonzero resurrection power** in this fixed old implementation.

The final gain is at least 1 HP and cannot raise HP above MAXHP.

## Attribute reverse

AttReverse is battle-only.

The cast toggles `CHAR_BATTLEFLG_REVERSE` with XOR.

When the new flag is enabled, `BATTLE_AttReverse` transforms the fixed elemental values:

```
new earth = old fire
new water = old wind
new fire  = old earth
new wind  = old water
```

A second cast toggles the flag off. The immediate helper then returns without another swap because the reverse flag is no longer set.

Normal fixed attributes are subsequently rebuilt by the battle pre-command parameter refresh; that refresh reapplies the element swap only while the reverse flag remains active.

So the historical implementation is not simply “swap on, swap back immediately on second cast”.

## Resurrection + defense

ResAndDef combines dead-target resurrection with a magic-defense duration.

It uses the same broad resurrection target exclusions:

- living targets do not change;
- PvP player targets do not revive.

For a valid dead target it:

1. computes resurrection HP with the same zero/nonzero behavior;
2. clears the death flag;
3. writes the selected magic-defense timer.

The fixed descendant source also contains later friendly-side restriction code in this family. That restriction is kept versioned rather than folded into the unguarded semantic core.

## Cost modifiers deliberately outside R1 core

The inspected descendants contain additional MP-cost modifiers based on family/sprite state and magic-array ranges, plus later no-magic-map and silence restrictions.

Those behaviors are valuable version evidence, but they are not required to define the nine-function unguarded common effect core. The reference model therefore accepts the **effective MP cost** as an input and models mutation ordering from that point onward.

## Reference model and tests

Artifacts:

- `tools/stoneage_magic_effect_model.py`
- `tests/test_stoneage_magic_effect_model.py`
- `.github/workflows/validate-stoneage-magic-effect-model.yml`

The deterministic model covers:

- caster / battle-init / MP gates;
- MP-spend-before-route failure;
- field versus battle routing;
- living/dead target expansion;
- Recovery target-mode validation;
- C-style numeric option parsing;
- VITAL recovery multipliers;
- battle and field recovery arithmetic after deterministic RNG injection;
- field-attribute option semantics;
- status option defaults;
- magic-defense durations;
- resurrection zero/nonzero behavior and the `%` overwrite defect;
- highest-index status-recovery behavior;
- reverse-flag toggling;
- ResAndDef target transition.

Randomness is injected into the model as an already-rolled amount; tests verify the deterministic state transition around the historical RNG rather than hard-coding a PRNG implementation.

GitHub Actions run `35370420953` completed successfully with **35 deterministic regression tests** after the final recovery-target and attribute-reverse additions.

## Evidence boundaries

- **FACT:** all three pinned descendant source tables share the same nine unguarded callback families.
- **FACT:** those nine callbacks account for 130 / 181 active recovered magic rows; 46 rows use seven callbacks guarded in all three source lineages, and five rows use the partial-source `MAGIC_AttSkill` family.
- **FACT:** common wrappers verify MP and deduct it before battle-only field rejection.
- **FACT:** Recovery/OtherRecovery are field-capable; the other seven modeled families are battle-only in the fixed common path.
- **FACT:** the fixed recovery-rate formula differs between player and non-player VITAL scaling.
- **FACT:** common target selectors use the two ten-slot sides plus side/all selector IDs.
- **FACT:** ordinary resurrection selects dead targets and excludes PvP player resurrection.
- **FACT:** nonzero resurrection overwrites its prior percentage-derived amount with the random power roll.
- **FACT:** status recovery acts on the highest-index active status candidate rather than clearing every status.
- **FACT:** attribute reverse is an XOR state toggle with element remapping while active.
- **SOURCE HAZARD:** old all-target list construction contains revision/macro-sensitive list-termination defects; R1 does not emulate unsafe memory contents.
- **VERSIONED:** guarded magic families, family/sprite cost modifiers, riding interactions, friendly-side restriction macros and no-magic-map layers remain outside the early/core promotion boundary.
- **OPEN:** whether each of these nine descendant-common families existed with identical formulas in the September/October 1999 JSS builds.

## Next seam

After CI validates this R1 core, the next deterministic semantic priority is:

1. classify and reconstruct **common item effect families** from the 36 all-three USE callbacks and the already-complete non-use callback set;
2. keep the 16 branch-specific item USE callback tokens in a version-diff track;
3. then reconstruct the 65 all-three pet-skill callback families while leaving the four all-source-missing recovered pet-skill rows quarantined.
