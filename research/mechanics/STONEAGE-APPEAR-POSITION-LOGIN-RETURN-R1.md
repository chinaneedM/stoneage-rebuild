# StoneAge Appear Position / Login Return Table R1

Status: **strong old-descendant schema; runtime use diverges in the newer Bismarck branch**  
Scope: server `appear.txt` loaded by `CHAR_initAppearPosition`.

## Stable file schema

All three fixed source descendants parse the same whitespace-delimited three-integer row:

```
FLOOR X Y
```

Tabs are normalized to spaces and repeated spaces are collapsed before tokenization.

The table is loaded at game-server startup through the configured:

```
appearpositionfile
```

which the preserved setup family points to `data/appear.txt`.

## Lookup behavior

`CHAR_isAppearPosition(floor, &x, &y)` scans from the first loaded row forward.

On the first row whose FLOOR matches:

- it writes that row's X and Y to the output pointers;
- returns TRUE immediately.

Consequences:

- multiple rows for the same floor are allowed by the loader;
- only the first duplicate floor is observable through this lookup;
- later duplicate floor rows are shadowed.

The loader itself performs no floor/coordinate range validation.

## What the old fixed login path actually does

In the fixed gavinlinasd and iriselia branches, character login calls:

```
CHAR_isAppearPosition(current_floor, &x, &y)
```

If the floor is present, the code does **not** use the returned x/y values.

Instead it resolves:

```
CHAR_LASTTALKELDER
 -> elder/save-point floor, x, y
```

and overwrites the character's saved location with that record-point position.

Therefore in these fixed descendants the operational rule is:

> if the saved login floor appears in appear.txt, do not resume there; return the player to the last elder/save point.

This makes `appear.txt` a login-return / non-resumable-floor table in the observed runtime, despite its generic "appear position" name.

## Stored X/Y fields are dormant in the observed login call

The parser and lookup preserve an X/Y pair, but the only runtime call found in the fixed gavinlinasd/iriselia tree discards those returned values after the presence test.

No other fixed call to `CHAR_isAppearPosition` was found there.

Therefore R1 distinguishes:

- **FACT:** the table stores FLOOR/X/Y;
- **FACT:** the old fixed login call uses floor membership as the trigger;
- **FACT:** that call returns to LASTTALKELDER rather than the table's X/Y;
- **OPEN:** whether earlier commercial code used the stored X/Y directly;
- **OPEN:** whether X/Y became vestigial after the record-point return logic changed.

## Bismarck divergence

Bismarck's fixed server still:

- declares the same table structure;
- loads it at startup;
- exposes the same `CHAR_isAppearPosition` lookup.

However, repository-wide search at the fixed revision found no active call to `CHAR_isAppearPosition` outside its declaration/definition.

Thus current Bismarck retains the data/parser but appears to have removed or bypassed the older login-return check.

This is a code-version divergence, not evidence that the table never mattered historically.

## Why this is early/core-relevant

The rule determines whether a character can persistently log back into particular floors.

It connects:

```
saved character FLOOR
 + LASTTALKELDER
 + record-point table
 + login reconstruction
```

and is therefore part of world-state persistence, not merely presentation data.

For a modern rebuild we should model the visible behavior explicitly as a "login resume policy" rather than retaining an opaque file whose coordinates are not consumed.

## Provenance-preserving recovered probe

Artifacts:

- `tools/stoneage_appear_position_probe.py`
- `tests/test_stoneage_appear_position_probe.py`
- `.github/workflows/probe-stoneage-25-appear-positions.yml`

The workflow rehydrates the pinned preservation bundle only in CI and commits only aggregate metadata:

- configured file name;
- file SHA-256/size;
- row/field counts;
- unique/duplicate floor counts;
- aggregate floor/x/y ranges;
- negative/zero coordinate row counts.

It does not publish floor IDs, coordinates, comments, or original rows.

## Evidence status

- **FACT:** the three fixed descendants share the same three-integer loader schema.
- **FACT:** lookup returns the first matching floor's coordinates.
- **FACT:** fixed gavinlinasd/iriselia login code uses membership in this table to return the character to LASTTALKELDER.
- **FACT:** that observed login call ignores the table's returned x/y.
- **DIVERGENCE:** fixed Bismarck still loads the table but has no active lookup caller found in this audit.
- **OPEN:** original JSS-1999 meaning of the stored x/y pair.
- **OPEN:** exact version in which the login caller changed or disappeared.

## Next seam

After the recovered aggregate is generated, fold this table into the gameplay-data inventory and continue with the next **server-authoritative early/core** root table, preferring world-state tables over later profession/event systems.
