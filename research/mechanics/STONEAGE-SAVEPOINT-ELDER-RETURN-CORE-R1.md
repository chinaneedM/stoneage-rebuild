# StoneAge Save Point / Elder / Return-Point Core R1

Status: **source-reconstructed convergent core with explicit lineage divergences**
Scope: ordinary elder registry, save-point activation state, last-record-point selection, and the return path used by older login handling.

## Fixed source controls

This pass compares fixed revisions already used elsewhere in the project:

- `gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`;
- `iriselia/StoneAge@9e6c8ce2cd8ed532a7157773acd1c61582c178b5`;
- `BismarckDD/stoneage@999ffdf1d220ec6666eb65339180689c9caf1876`.

The first two preserve the same older save-point path very closely. Bismarck retains the same core data structures and activation logic but changes interaction and immediate-save behavior.

## Core state is split between server registry and character persistence

The observed design has two different state surfaces.

### Server elder-position registry

`char_data.c` defines:

- `MAXELDERS = 128`;
- a process-local array of `floor / x / y` tuples;
- ordinary built-in elder slots 0..3 for the four hometowns;
- one additional preinitialized slot 4 in all three fixed descendants;
- dynamic writes through `CHAR_ElderSetPosition`.

`ELDERINDEXSTART` evaluates to 4. Dynamic save-point registration therefore accepts:

```
4 <= elder_id < 128
```

and can overwrite the preinitialized value in slot 4.

This registry is **server runtime state**, not the character's saved coordinate list.

### Per-character persistent state

The character stores at least:

- `CHAR_LASTTALKELDER`: one elder/save-point index;
- `CHAR_SAVEPOINT`: a bit field recording unlocked save-point IDs.

The ordinary four-hometown creation path initializes both:

```
LASTTALKELDER = hometown
SAVEPOINT |= 1 << hometown
position = elder[hometown]
```

for hometown values 0..3.

This links the already reconstructed birth system directly to the record-point system.

## Save-point NPC initialization

`NPC_SavePointInit` reads NPC arguments:

- `ID`;
- `Born=floor,x,y`.

It stores ID in the NPC work field, marks the NPC as `CHAR_TYPESAVEPOINT`, then requires both:

1. `MAP_IsValidCoordinate(floor,x,y)`;
2. `CHAR_ElderSetPosition(ID,floor,x,y)`.

Initialization fails if either check fails.

Therefore dynamic save-point coordinates become authoritative through NPC initialization rather than through a separate standalone “record-point table” observed in these fixed sources.

## Unlock and selection are distinct operations

The ordinary interaction has two persistent effects:

1. unlock a save point in `CHAR_SAVEPOINT`;
2. select it as `CHAR_LASTTALKELDER`.

These are related but not identical.

### Already unlocked point

Talking to an unlocked point sets:

```
LASTTALKELDER = this elder ID
```

without changing the unlock mask.

### `NOITEM`

If the NPC argument contains `NOITEM`, the source sets the save-point bit **before** testing whether the point is unlocked.

Consequently the same interaction immediately falls into the activated path and selects that elder as `LASTTALKELDER`.

### Requirement-gated point

If the point is still locked:

- `NPC_UsedCheck(..., flg=0)` tests the configured `GetItem` expression;
- if the requirement cannot be met, no persistent state changes;
- if it can be met, the player is offered a confirmation window;
- choosing YES runs `NPC_UsedCheck(..., flg=1)`, which performs the configured item deletion;
- only after that succeeds does `NPC_MessageDisp(..., 1)` set the unlock bit and `LASTTALKELDER`.

If no `GetItem` key exists, the older source explicitly treats the requirement check as successful.

The concrete item expression is content data; R1 models the gate/result rather than embedding any recovered item IDs.

## The unlock bit field has a structural width mismatch

The elder registry accepts dynamic IDs up to 127, but unlock operations use:

```c
point = point | (1 << shiftbit);
(point & (1 << shiftbit)) == (1 << shiftbit)
```

where `point` and the literal `1` are ordinary signed `int` values in the fixed source.

For a conventional 32-bit signed C `int`, shifting into or beyond the sign bit is not a portable defined way to represent 128 independent flags.

Therefore:

- **FACT:** the coordinate registry has 128 slots;
- **FACT:** save-point unlock state is stored in one integer bit field using the elder ID as the shift count;
- **DO NOT INFER:** that all 128 registry IDs are safely independently unlockable;
- **OPEN:** the exact ID domain used by the original/clean content;
- **ENGINEERING NOTE:** a modern rebuild should preserve historical IDs but use an explicitly sized safe representation.

This is a source representation hazard, not a reason to silently clamp historical data.

## Position lookup is range-only

`CHAR_getElderPosition` checks only:

```
0 <= elder_id < 128
```

It does not validate that the selected slot was actually populated with a meaningful coordinate.

Because the C elder array has static storage duration, an in-range never-written slot is zero-initialized and resolves to:

```
floor=0, x=0, y=0
```

An out-of-range ID returns FALSE.

Several old callers, including the observed appear/login return path, do not check that return value before consuming their local output variables. R1 does not emulate uninitialized-memory behavior; it exposes lookup failure explicitly in the reference model.

## Login return closes the appear-table chain

The previously reconstructed older login behavior is now connected end-to-end:

```
saved FLOOR
  -> is FLOOR present in appear.txt?
       no  -> keep saved position
       yes -> LASTTALKELDER
                -> elder registry
                -> floor/x/y return position
```

The stored X/Y values in `appear.txt` are not used by this old fixed caller.

Thus `appear.txt` is a membership trigger, while the actual return coordinate is owned by the elder/save-point registry.

## Immediate persistence differs by lineage

### gavinlinasd / iriselia

On the fixed older path:

- selecting/revisiting an unlocked save point sends `CHAR_charSaveFromConnectAndChar(..., FALSE)`;
- successful first-time confirmation also saves with `unlock=FALSE`;
- the ordinary revisit block contains two consecutive save calls in the inspected fixed source.

The duplicate send is recorded as observed implementation behavior, not promoted as a required gameplay rule.

### Bismarck

Bismarck changes this layer:

- the same core unlock/last-elder mutations remain;
- ordinary revisit saving is conditional on `_NPC_SAVEPOINT` and the character's `CHAR_ISSAVE` flag;
- the first-time confirmation block no longer contains the older unconditional immediate save.

Therefore “touching a record point always immediately writes twice” is **not** a convergent rule.

The persistent-state mutation and the persistence transport must remain separate concepts.

## Interaction-gate divergence

gavinlinasd/iriselia use the older facing-based talk gate with a same-cell exception. Literally, if facing fails **or the player is dead**, the callback still proceeds when player and NPC occupy the same floor/x/y.

Bismarck changes the gate to:

- reject dead players;
- require distance <= 2;
- not require the older facing test.

This is a real fixed-lineage divergence. R1 exposes both policies rather than choosing one as historical truth.

## Relationship to death/revival

The earlier death/revival pass correctly left automatic death -> record-point choreography OPEN.

This pass establishes the record-point half of that chain, but it does **not** prove that ordinary death in the original game automatically invoked this return path.

Known return callers and later logout/no-exit branches can use `LASTTALKELDER`, but those must not be back-projected into an undocumented launch-era death sequence.

## Deterministic reference model

Artifacts:

- `tools/stoneage_savepoint_elder_model.py`;
- `tests/test_stoneage_savepoint_elder_model.py`;
- `.github/workflows/validate-stoneage-savepoint-elder.yml`.

The tests cover:

- four-hometown initialization;
- dynamic registry bounds;
- coordinate-validation failure;
- static-zero unregistered slots;
- unlock versus last-elder selection;
- `NOITEM` ordering;
- requirement/confirmation gating;
- older appear/login return;
- invalid return lookup exposure;
- interaction-gate divergence;
- 128-slot registry versus signed-int bit-field mismatch;
- lineage-specific immediate-save policy.

## Evidence status

- **FACT:** the three fixed descendants share a 128-entry elder coordinate registry.
- **FACT:** ordinary creation initializes hometown elder indices 0..3 and their save-point bits.
- **FACT:** dynamic `CHAR_ElderSetPosition` accepts IDs 4..127.
- **FACT:** save-point NPC initialization registers its `Born` coordinate into that runtime registry.
- **FACT:** `CHAR_SAVEPOINT` uses `1 << elder_id` bit operations.
- **FACT:** an unlocked point can become `LASTTALKELDER` without being newly unlocked.
- **FACT:** `NOITEM` unlocks before the branch checks the bit.
- **FACT:** requirement-gated activation tests first, then consumes on YES, then sets unlock + last elder.
- **FACT:** the older appear/login caller redirects through `LASTTALKELDER`, not appear-table X/Y.
- **DIVERGENCE:** fixed older and Bismarck interaction gates differ.
- **DIVERGENCE:** fixed older and Bismarck immediate-save behavior differs.
- **SOURCE HAZARD:** registry capacity and signed-int unlock-bit capacity do not match.
- **OPEN:** clean early content's actual dynamic elder-ID domain.
- **OPEN:** exact launch-era use, if any, of the extra preinitialized elder slot 4.
- **OPEN:** automatic death -> record-point choreography in the original baseline.

## Next seam

With birth -> save point -> appear/login return -> persistence now connected, the next largest ordinary deterministic gap is **persistent item/pet storage and pet-shop transfer semantics**.

That work should distinguish early carried/storage behavior from later shared-pool extensions.
