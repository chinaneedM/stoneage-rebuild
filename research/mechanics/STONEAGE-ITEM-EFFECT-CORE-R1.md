# StoneAge Common Item Effect Core R1

Status: **fixed-descendant common item semantics reconstructed and regression-modeled**  
Evidence boundary: three pinned descendant source revisions plus the verified recovered 2.5 active item table. This is a descendant-common semantic layer, **not proof of September/October 1999 launch behavior**.

Pinned source revisions:

- gavinlinasd/StoneAge `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
- iriselia/StoneAge `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
- BismarckDD/stoneage `999ffdf1d220ec6666eb65339180689c9caf1876`

## Why dispatch presence is not enough

The item registry has an important distinction that the magic layer did not expose as strongly:

1. a callback token can be registered without a preprocessor guard;
2. the referenced function can still be only a macro-controlled shell;
3. therefore “unguarded dispatch” does not by itself establish an ordinary common semantic implementation.

The final probe checks both:

- dispatch-table guard state in `function.c`;
- substantive unguarded function-body code across `item/item_event.c` and `battle/battle_item.c`.

Commented-out dispatch lines are stripped before classification.

## Active recovered USE boundary

The active recovered itemset contains 957 USE rows / 52 unique USE callback tokens.

At dispatch-table level:

- 17 unique tokens / 818 rows are unguarded in all three pinned lineages;
- 19 tokens / 86 rows are guarded in all three;
- 16 tokens / 53 rows have partial source-lineage coverage;
- none are absent from all three.

After function-body refinement, the 17 unguarded-dispatch candidates split into:

- **15 stable-body tokens / 816 rows**;
- **2 macro-shell tokens / 2 rows**;
- 0 mixed-body tokens;
- 0 partial-body-source tokens.

The two macro-shell rows are profession-skill callbacks: their registry entries are unguarded, but their substantive bodies are inside `_PROFESSION_SKILL`. They therefore remain a later/versioned system and are not promoted into this common item core.

### Active stable USE families

The recovered stable/common layer contains:

- battle recovery — 1 token / 643 rows;
- ordinary status application — 1 / 52;
- ordinary status recovery — 1 / 27;
- capture-rate increase — 1 / 26;
- warp/travel — 1 / 37;
- pet follow — 1 / 7;
- resurrection — 1 / 5;
- field-attribute change — 1 / 4;
- encounter suppression — 1 / 3;
- microphone toggle — 1 / 3;
- item rename UI/workflow — 1 / 3;
- forced encounter — 1 / 2;
- ordinary skill-up point — 1 / 2;
- pet-owner/rename-lock release — 1 / 1;
- ToHelos encounter-effect item — 1 / 1.

The active table does not require an unguarded ordinary MagicDef, ParamChange, or AttReverse USE row, although the fixed source contains stable ordinary implementations for those item functions. Their semantics are retained in the reference model as source-common auxiliary behavior, not claimed as active rows in this specimen.

## Common item routing

Ordinary item wrappers reject an invalid caster and suppress use during battle-init mode.

Recovery is field/battle dual-route.

The ordinary battle-only item families simply do nothing when used outside battle. Unlike ordinary magic, there is no MP transaction layer, so there is no corresponding “MP spent before not-battling failure” behavior.

Once a concrete battle item parser succeeds and calls its effect primitive, the common handlers normally delete the item afterward even if the primitive ultimately changes no selected target.

## Battle recovery

The unguarded ordinary recovery parser checks HP before MP.

The historical source keys are two-byte Chinese characters. Expressions such as `p+2` advance over that two-byte key itself; R1 therefore parses the number immediately after the key rather than inventing an extra separator.

Recovery power is randomized through:

```
RAND(power * 0.9, power * 1.1)
```

HP recovery uses the same fixed descendant VITAL multiplier as ordinary magic:

```
player:     1.0 + 0.00010 * VITAL
non-player: 1.0 + 0.00005 * VITAL
```

MP recovery does not apply that VITAL multiplier.

The base common item branch does not set percentage mode. Later guarded item extensions can add combined HP/MP and other special recovery forms and remain versioned.

## Field recovery

The unguarded field recovery path can mutate:

- HP;
- player MP;
- player charm;
- pet loyalty / variable-AI storage.

The “all” marker requests effectively full HP and player MP.

Explicit values are randomized ±10% when successfully parsed. HP then receives the VITAL recovery multiplier.

Bounds are historical state bounds:

- HP / MP: source performs max-cap then minimum 1;
- charm: 0..100;
- pet loyalty backing storage: -10000..10000, with displayed loyalty changes stored ×100.

No applicable recovery key means the common field path returns without consuming the item.

## Ordinary status application and recovery

Item StatusChange differs materially from magic StatusChange:

- default duration is **0 turns** for the item handler;
- default success parameter remains 15.

Optional `turn` and success fields override those defaults.

Status resolution then delegates to the same battle status primitive.

StatusRecovery shares the old primitive behavior already reconstructed for magic: the battle helper scans active ordinary statuses, retains the highest-index active candidate, and clears only that candidate when the requested recovery rule matches. It is not a clear-all operation.

## Field attribute, defense, parameter and reverse helpers

Stable fixed-source item helpers reuse the same battle primitives as magic, but with item-specific defaults:

- FieldChange delegates to `BATTLE_FieldAttChange`.
- Item MagicDef defaults duration to 0 rather than magic’s 3.
- ParamChange defaults power to 30.
- Flat attack/defense/quick modifiers are stored in x100 work scale.
- Percent attack/defense/quick mode multiplies the fixed work value directly by the integer power.
- Charm percent mode applies a 0.01 factor.
- Capture-kind parameter change uses ordinary units.
- AttReverse reuses the same XOR reverse flag and element-remap behavior reconstructed in the magic core.

FieldChange deletes the item after invoking the shared parser even if that parser later returns failure.

## Resurrection

Item resurrection uses the same fixed `BATTLE_MultiRessurect` primitive as ordinary magic:

- living targets are not changed;
- PvP player resurrection is skipped;
- power 0 produces full-MAXHP behavior from the normal dead baseline;
- nonzero power’s earlier percentage-derived amount is overwritten by the ±10% random power roll;
- final nonzero gain is at least 1.

The percent-overwrite quirk is therefore shared by ordinary magic and item resurrection.

## Capture-rate item

The common item parser defaults power to 5 when numeric parsing fails.

The battle primitive:

1. expands ordinary living targets;
2. skips non-player targets;
3. skips dead players;
4. rolls ±10% around power;
5. adds the result to `CHAR_WORKMODCAPTURE`.

## Warp item

The stable warp item parses exactly four integers:

```
flag floor x y
```

The shared helper rejects:

- use during battle;
- floor 117 in the stable common branch;
- a party leader attempting the single-person flag;
- a party client attempting to use the item.

For a solo player, the caster is warped.

For a party leader with the group flag, valid party slots are iterated and warped.

The consumable is deleted only after the warp helper returns success.

Later blocked-floor, cargo and repeat-use additions remain macro/version layers.

## Pet-follow item

The stable pet-follow item:

- rejects when a currently valid follow pet is already out;
- requires a valid target and item;
- parses a follow-level ceiling;
- rejects a target above that ceiling;
- requires the target to be found in the first five carried-pet slots;
- delegates the actual drop/follow operation.

The visible loyalty-under-80 rejection is commented out in the fixed source.

A successful pet-follow use **does not delete the item** in this function.

## Encounter-control items

The ordinary no-enemy consumable sets connection-level no-enemy state and deletes the item.

The ordinary encounter consumable sets connection-level stay-encounter state and deletes the item.

Later loop-function scheduling around forced encounters is macro-controlled and remains versioned.

### Equipment no-enemy hooks

The stable attach hook parses a `noen` level and quantizes it to 200 / 120 / 80 / 40 / 0.

The connection-level value is written before floor-specific messaging, so a “nothing happened” message does not imply that the state was not set.

The detach hook clears the equipment no-enemy state.

## Microphone item

Ordinary use toggles runtime mic mode only outside battle and does not consume the item.

Dropping a valid mic item forces mic mode off.

## Skill-up item

The ordinary skill-up consumable increments `CHAR_SKILLUPPOINT` by exactly one and deletes itself.

This stable descendant behavior is recorded as such; comments/feature chronology do not prove launch-era presence.

## Pet-owner / rename-lock release item

The item applies only to a valid pet target.

It refuses when the pet’s owner marker is already empty or already equals the current player account marker.

Otherwise it clears the pet `CHAR_NPCARGUMENT` owner marker, refreshes pet rename status, and consumes the item.

## ToHelos effect item

This handler removes the item from the inventory slot **before** parsing its two pipe-delimited integer fields.

Therefore malformed arguments still destroy the item.

Negative cut-rate and count values are clamped to zero.

When the user is a party client, the work-state target is the party leader; otherwise it is the caster.

The resulting cut-rate/count pair is written to the target’s ToHelos work fields.

## Rename-item workflow

Initial use opens the selection UI and stores:

- selected target slot = -1;
- catalyst item slot = the used rename item.

It is not consumed at this stage.

Final name validation uses C `strlen`, so the authoritative limit is **1..26 source bytes**, not Unicode code points. The UI describes this as 13 full-width or 26 half-width characters.

The source rejects:

- ASCII spaces;
- full-width spaces;
- the pipe delimiter.

On accepted input, the target item’s secret name and account marker are written **before** the catalyst is revalidated.

This creates a historical ordering hazard: if the catalyst becomes invalid at that point, the rename can remain committed without decrementing the catalyst.

Catalyst remaining-use behavior:

- argument 0: no decrement, effectively unlimited in this path;
- positive >1: decrement by one;
- 1: delete after use;
- nonzero negative values also enter the decrement/delete branch and delete.

## Stable non-USE callbacks

The recovered active non-USE layer is sparse and cleanly separable.

### ATTACH

51 active rows / 5 tokens:

- 2 unguarded/stable common tokens / 5 rows;
- 3 guarded tokens / 46 rows.

The two stable families are:

- equipment encounter-control attach — 3 rows;
- PickAllPet equipment attach — 2 rows.

### DETACH

51 active rows / 5 tokens:

- 2 unguarded/stable common tokens / 5 rows;
- 3 guarded tokens / 46 rows.

Stable families mirror attach:

- encounter-control removal — 3 rows;
- PickAllPet removal — 2 rows.

### DROP

40 active rows / 3 tokens:

- 2 unguarded/stable common tokens / 5 rows;
- 1 guarded token / 35 rows.

Stable DROP families:

- microphone cleanup — 3 rows;
- dice visualization — 2 rows.

### PICKUP

2 active rows / 1 token:

- 1 unguarded/stable token / 2 rows;
- no guarded token.

The dice pickup hook restores the saved original image and normal item name.

### RELIFE

3 active rows / 1 token:

- 0 unguarded common tokens;
- 1 all-three guarded token / 3 rows.

The relife hook is therefore kept in the versioned extension layer rather than promoted into the ordinary common item core.

## Dice drop / pickup

Dropping the ordinary dice:

1. stores the original base image in item VAR1;
2. rolls one of six faces;
3. swaps to the matching face image;
4. replaces the secret name with the face label.

Picking it up restores:

- base image from VAR1;
- secret name from the normal item name.

## PickAllPet equipment hook

The stable attach/detach pair is unusually direct:

- attach sets `CHAR_PickAllPet = TRUE`;
- detach sets `CHAR_PickAllPet = FALSE`.

The old commented item-ID condition is not executable and is not reconstructed as a rule.

## Excluded/versioned item layers

R1 deliberately does not flatten later extensions into the ordinary common layer.

Examples include:

- profession-skill item bodies;
- relife equipment;
- magic-defense equipment;
- suit systems;
- later encounter-rate equipment;
- transformation/pig cures;
- level-cap stones;
- pet EXP stones;
- attack-magic items;
- later repeat-use warp items;
- feature-specific battle consumables.

A token’s presence in a descendant registry or in the mixed recovered 2.5 data is not proof of launch-era presence.

## Reference model and validation

Artifacts:

- `tools/stoneage_item_effect_model.py`
- `tests/test_stoneage_item_effect_model.py`
- `.github/workflows/validate-stoneage-item-effect-model.yml`
- `tools/stoneage_effect_callback_coverage_probe.py`
- `research/recovered/STONEAGE-25-EFFECT-CALLBACK-COVERAGE-R1.txt`

The deterministic model covers the stable active USE mechanisms plus the stable non-USE hooks and several source-common auxiliary item battle helpers.

Randomness is injected as already-rolled values so tests verify historical state transitions without coupling the model to a PRNG implementation.

GitHub Actions:

- item effect model run `35373496535`: **68 tests, success**;
- final dispatch/body callback probe run `35373534098`: **success**.

## Evidence boundary

- **FACT:** 15 active USE callback tokens / 816 rows have both all-three unguarded dispatch and all-three substantive unguarded bodies.
- **FACT:** two active USE tokens / two rows are unguarded registry entries whose substantive bodies are entirely profession-macro controlled.
- **FACT:** all unguarded active ATTACH/DETACH/DROP/PICKUP candidates also have stable all-three bodies.
- **FACT:** active RELIFE is entirely guarded in all three fixed lineages.
- **FACT:** the stable source-common item layer contains several implementation quirks that should be preserved as historical behavior before modern redesign.
- **OPEN:** exact introduction date of each stable-descendant family relative to 1999 JSS launch and early 1.x releases.

## Next seam

With ordinary magic and common item effects reconstructed, the next deterministic semantic layer is **pet skills**.

The three fixed pet-skill dispatch tables share 68 textual callback families, but only 15 are unguarded in all three fixed lineages; the other common entries are feature-macro gated. The active recovered pet-skill table must therefore receive the same guard/body treatment before any large “65 common tokens” set is promoted into an early/common semantic core.
