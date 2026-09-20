# StoneAge Movement-Side Encounter Frequency / CEP — R1

Date: 2026-09-20

Status: **stable-descendant deterministic reconstruction; earliest commercial provenance remains open**

## Scope

This record isolates the movement-side encounter-frequency loop that appears in
multiple fixed descendant server lineages.

CEP is explicitly named in the source as **Current Encounter Probability**.

This mechanism is kept separate from:

- encounter-area selection;
- weighted group selection;
- weighted enemy-variant selection;
- enemy birth/stat generation;
- later profession/item encounter modifiers.

## Evidence anchors

Primary fixed descendant source:

- `gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
  - `gmsv/src/char/char_walk.c`
  - `gmsv/src/net.c`

Independent control:

- `iriselia/StoneAge@9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
  - corresponding `char_walk.c` / `net.c` paths preserve the same CEP state accessors and movement loop.

The inspected source comments label CEP handling as an Arminius-era addition.
Therefore this report does **not** promote CEP to a proven 1999 JSS launch
mechanic.

## 1. CEP is connection/runtime state

The fixed connection object contains:

```
int CEP;  // Current Encounter Probability
```

A new connection initializes CEP to zero.

Getter/setter functions expose the value to movement processing.

In the modern single-player reconstruction this state belongs to the runtime
simulation, not to an emulated network connection.

## 2. Encounter bounds are zone-derived

The movement path maintains two character work values:

- encounter probability minimum;
- encounter probability maximum.

After a successful movement, the fixed source calls the encounter lookup using
the **departure** floor/x/y. If a lookup returns `-1`, the previous bound is
left unchanged. Otherwise the stored min/max work value is replaced.

This ordering is preserved as descendant evidence rather than normalized to a
destination-cell lookup.

## 3. Clamp before random test

After reading current CEP:

```
if CEP < min: CEP = min
if CEP > max: CEP = max
```

Only then is the random encounter test executed.

Therefore a newly initialized CEP of zero becomes the zone minimum on the
first eligible movement step.

## 4. Random domain

The stable base branch tests:

```
rand() % 120 < CEP
```

The deterministic reconstruction therefore represents the supplied random
result as an integer in `0..119`.

No artificial normalization to a 0-100 percentage scale is performed.

## 5. Soft-pity increment/reset behavior

If the random test fails:

```
if CEP < max:
    CEP += 1
```

If the random test succeeds and an encounter is actually dispatched:

```
CEP = min
dispatch encounter
```

Thus the base path is an increasing-probability / soft-pity loop:

```
miss -> +1 toward max
actual encounter -> reset to min
```

## 6. Ordinary Warp suppresses the encounter after the roll

Before the CEP roll is resolved, the target movement cell is scanned for event
objects. An ordinary `CHAR_EVENT_WARP` clears the encounter-enable flag.

Crucially, the source still performs the random CEP test.

Consequences:

- if the CEP roll misses on a Warp step, CEP still increments toward max;
- if the CEP roll hits but the ordinary Warp flag suppresses encounter,
  CEP is neither reset nor incremented in that branch;
- no encounter is dispatched on the ordinary Warp step.

This is more precise than treating a Warp step as if encounter processing never
ran.

## 7. Battle/no-processing boundary

The inspected loop only performs the random encounter test when the character
is not already in battle mode.

The deterministic model exposes an explicit eligibility switch. Ineligible
processing still preserves the clamp boundary but performs no random roll and
no increment.

Later no-enemy equipment, profession-skill modifiers, cursed-stone/stay-
encounter behavior and item-specific random-encounter modifiers are excluded
from this R1 base model.

## 8. Runtime integration

Deterministic artifacts:

- `tools/stoneage_encounter_frequency_model.py`
- `tests/test_stoneage_encounter_frequency_model.py`
- `tools/stoneage_singleplayer_runtime.py`

The runtime now carries `EncounterFrequencyState` directly instead of
recreating a network connection object.

The reconstruction-safe path is:

```
successful walk
 -> refresh min/max from departure coordinate when a zone lookup succeeds
 -> clamp CEP
 -> explicit roll in 0..119
 -> apply ordinary-Warp suppression
 -> miss: increment toward max
 -> actual hit: reset to min and request encounter at current world position
```

The older direct `EncounterRolls` path remains as a deterministic bridge/test
entry point and is not silently reinterpreted as CEP behavior.

## Evidence status

- **STRONG DESCENDANT FACT:** runtime CEP state exists and initializes to zero.
- **STRONG DESCENDANT FACT:** CEP is clamped to stored min/max before testing.
- **STRONG DESCENDANT FACT:** base random test is `rand()%120 < CEP`.
- **STRONG DESCENDANT FACT:** misses increment CEP by one up to max.
- **STRONG DESCENDANT FACT:** actual encounters reset CEP to min.
- **STRONG DESCENDANT FACT:** ordinary Warp suppresses encounter after the CEP
  roll; a suppressed hit does not enter the miss-increment branch.
- **STRONG DESCENDANT FACT:** movement refreshes min/max from the departure
  coordinate in the inspected path.
- **VERSIONED/LATER:** profession and equipment encounter modifiers.
- **OPEN:** whether the exact CEP mechanism and constants were present in JSS
  1999 or Taiwan v1.0 server-side logic.

## Consequence

Encounter occurrence can now be modeled independently from encounter content
selection. This keeps two historically distinct questions separate:

1. **Does this movement step produce an encounter?** — CEP frequency loop.
2. **What enemy group/variant appears here?** — encount/group/enemy data chain.

That separation is now explicit in the single-player runtime.
