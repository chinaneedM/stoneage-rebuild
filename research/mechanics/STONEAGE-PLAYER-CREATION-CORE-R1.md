# StoneAge Player Creation Core R1

Status: **strong convergent descendant evidence; launch-era identity remains OPEN**  
Scope: ordinary player creation only. Later test-server / configurable new-player overrides are explicitly excluded.

## Why this note exists

The player-growth reconstruction now defines what one displayed VITAL / STR / TOUGH / DEX point means and how those stats feed derived combat values. The missing upstream link was the ordinary level-1 creation contract: how many points a new player may allocate, how elemental affinity is constrained, and what representation is persisted.

This note reconstructs that contract from three independently preserved descendant server lineages and turns the stable overlap into a deterministic reference model.

## Evidence set

The following source snapshots were read directly at fixed revisions:

- **BismarckDD/stoneage** @ `999ffdf1d220ec6666eb65339180689c9caf1876`
  - `server/gmsv/char/char.c`
  - `server/gmsv/include/defaultPlayer.h`
- **gavinlinasd/StoneAge** @ `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
  - `gmsv/src/char/char.c`
  - `gmsv/src/char/defaultPlayer.h`
- **iriselia/StoneAge** @ `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
  - `Source/gmsv/char/char.c`
  - `Source/gmsv/char/defaultPlayer.h`

All three retain the same ordinary creation structure around `CHAR_makeCharFromOptionAtCreate`, while later forks add separately guarded test/new-player behavior.

## Stable ordinary creation contract

### Base-stat allocation

**FACT — convergent descendant code**

The ordinary creation path accepts four values:

- VITAL
- STR
- TOUGH
- DEX

For each value:

- minimum: `0`
- maximum: `20`

The four values must sum to exactly:

```
VITAL + STR + TOUGH + DEX = 20
```

The server then persists each displayed creation point in x100 internal form:

```
CHAR_VITAL = vital * 100
CHAR_STR   = str * 100
CHAR_TOUGH = tgh * 100
CHAR_DEX   = dex * 100
```

This is the upstream half of the already reconstructed player-growth rule where spending one free point adds `100` internally.

### Element allocation

**FACT — convergent descendant code**

Creation also accepts four elemental point inputs:

- Earth
- Water
- Fire
- Wind

The stable validation rules are:

1. each input is in `0..10`;
2. the four inputs total exactly `10`;
3. no more than two elements may be nonzero;
4. Earth and Fire may not both be nonzero;
5. Water and Wind may not both be nonzero.

The accepted inputs are persisted at x10:

```
CHAR_EARTHAT = earth * 10
CHAR_WATERAT = water * 10
CHAR_FIREAT  = fire * 10
CHAR_WINDAT  = wind * 10
```

Therefore a creation input of `10` in one element becomes the internal value `100`.

### Stable default state around creation

**FACT — convergent descendant code**

The preserved default player template starts at:

- level `1`;
- EXP `0`;
- free stat points `0`.

The normal creation function then explicitly seeds:

- charm = `60`;
- MP = `100`;
- max MP = `100`.

The creation function also assigns HP the large sentinel `0x7fffffff` before the character is serialized. This value is **not modeled as a gameplay starting-HP rule**. Maximum HP belongs to the derived-stat layer already reconstructed in `STONEAGE-PLAYER-GROWTH-CORE-R1.md`; for example `V=10,S=5,T=3,D=2` yields `MAXHP=50` in that model.

## Later branches that must not contaminate the baseline

**FACT — versioned extensions**

The descendant code contains explicitly conditional branches such as:

- `_NEW_TESTSERVER`;
- `_NEW_PLAYER_CF`;
- configurable starting level / transmigration / gold / starter-pet settings;
- test-server paths with level 140 and hundreds of free stat points.

Those branches are useful evidence for later version evolution, but they are not evidence that the ordinary baseline creation contract itself used those values. R1 therefore excludes them.

## Deterministic model

Repository model:

- `tools/stoneage_player_creation_model.py`

The model exposes:

- `validate_base_stats(...)`;
- `validate_element_points(...)`;
- `build_creation_state(...)`.

It intentionally stops before equipment and derived-stat recomputation. The existing player-growth model remains authoritative for the next stage.

Regression coverage:

- `tests/test_stoneage_player_creation_model.py`
- `.github/workflows/validate-stoneage-player-creation.yml`

The tests cover accepted allocations, bad totals/ranges, opposite-element rejection, persistent scaling/defaults, and composition with the existing player-growth formula.

## Reconstruction consequence

The deterministic player progression chain now has an explicit upstream origin:

```
character creation
  -> 20 base points persisted at x100
  -> 10 elemental points persisted at x10
  -> level 1 / EXP 0 / free points 0
  -> derived player stats
  -> battle
  -> rewards
  -> +3 free points per gained level
  -> player point spending
```

This is stronger than treating “20 creation points” as an isolated UI convention: the x100 persistence rule joins directly to the level-up point-spending and derived-stat implementations already recovered.

## Evidence status

- **FACT:** ordinary descendant creation validates a 20-point V/S/T/D total and x100 storage.
- **FACT:** ordinary descendant creation validates a 10-point elemental total, maximum two active elements, and the two opposite-pair exclusions, then stores x10.
- **FACT:** the three descendant lineages agree on level 1 / EXP 0 / free-points 0 defaults and charm 60 / MP 100 creation seeds.
- **FACT:** later test/configuration branches can override baseline creation behavior and are separately guarded in source.
- **HYPOTHESIS:** this stable overlap descends from the early official server rule family.
- **OPEN:** direct 1999/JSS evidence proving that the launch service used this exact allocation contract.
- **OPEN:** launch-era UI affordances for changing/previewing these values before submission.
- **OPEN:** exact launch-era starter-pet/hometown mapping and later changes.
- **OPEN:** exact launch-era transmigration reset/inheritance rules.

## Next technical seam

The highest-value adjacent progression seam is now **transmigration/reset semantics**: determine which player fields are reset, inherited, or converted, and separate stable old-core behavior from later blessing/quest/config extensions. Starter-pet/hometown linkage should remain a separate creation-side evidence track.
