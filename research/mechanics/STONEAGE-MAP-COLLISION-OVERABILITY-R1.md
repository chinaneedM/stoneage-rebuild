# StoneAge Map Collision / Object Overability Core — R1

Date: 2026-09-20

Status: **strong stable-descendant collision semantics; historical image-property dataset still unresolved**

## Purpose

This record closes the algorithmic seam between recovered map cells and the
single-player movement boundary without guessing that an arbitrary MAP/DAT
numeric value directly means walkable or blocked.

The key result is that static movement is a two-stage lookup:

```
map cell
  -> tile image id + object/parts image id
  -> per-image WALKABLE / HAVEHEIGHT metadata
  -> static point walkability
  -> target-cell dynamic object overability
```

The exact image-property table used by JSS 1999 / Taiwan v1.0 is not yet
independently recovered. Therefore this report closes the **algorithm**, not
the final early-version content table.

## Evidence anchors

Stable descendant lineages inspected:

- `gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
  - `gmsv/src/map/map_deal.c`
  - `gmsv/src/map/readmap.c`
  - `gmsv/src/char/char_walk.c`
  - `gmsv/setup.cf`
- `iriselia/StoneAge@9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
  - `Source/gmsv/map/map_deal.c`
  - `Source/gmsv/map/readmap.c`
  - `Source/gmsv/char/char_walk.c`
- client control:
  - `BismarckDD/stoneage@999ffdf1d220ec6666eb65339180689c9caf1876`
  - `client/stoneage/system/map.cpp`

The two server lineages independently preserve the same core walkability and
target-overlap ordering.

## 1. Map cells are not boolean collision cells

Server maps preserve two static image-number planes:

- tile;
- object.

The server `MAP_getTileAndObjData` resolves both values for one floor/x/y
coordinate. The map protocol exports the same logical pair as tile and object
planes.

The recovered client runtime cache independently has three planes:

- tile;
- parts;
- event.

Existing project work already established that the client `parts` plane is
the protocol-side counterpart of the server static object plane. This does
**not** mean `parts != 0` is a collision test.

## 2. Image ids are interpreted through a metadata table

The descendant server loads a configured map-image property file through:

```
maptilefile=data/map/mapset.txt
```

Each image number maps to metadata including at least:

- `MAP_WALKABLE`;
- `MAP_HAVEHEIGHT`;
- later/other fields such as defense, battle-map assignment and status effects.

Missing/default image data initializes `MAP_WALKABLE=TRUE` in these
descendants, but the modern reconstruction MUST NOT use that as a fallback for
unknown recovered early image ids. The exact early property table is still a
data-provenance requirement.

## 3. Non-flying static walkability

`MAP_walkAbleFromPoint` first resolves the tile and object image ids, then
switches on the **object image's** `MAP_WALKABLE` value:

- object walkable = 0 -> blocked;
- object walkable = 1 -> allowed only if tile walkable == 1;
- object walkable = 2 -> allowed;
- any other value -> blocked.

Therefore collision is compositional. Neither the tile id nor the object/parts
id alone is sufficient.

## 4. Flying branch

For a flying actor, the same stable function does not use the ordinary
`WALKABLE` combination. Instead both tile and object images are tested for
`MAP_HAVEHEIGHT`.

If either has height, movement is blocked; otherwise it is allowed.

Later bus/skywalker/transparent shortcuts exist around this core and are not
promoted into the early historical baseline here.

## 5. Diagonal movement checks corners

The stable `CHAR_walk` path checks the target point. For a diagonal step it
also calls `MAP_walkAble` on both orthogonal side cells:

```
origin (x,y) -> diagonal (x+dx,y+dy)

must also allow:
  (x+dx,y)
  (x,y+dy)
```

If either side fails, the diagonal step is rejected.

This is a static-map corner rule. The inspected path does not run the later
same-coordinate dynamic-object overlap loop on those two side cells.

## 6. Dynamic object overability is a second gate

After static map walkability succeeds, the destination cell's live objects are
enumerated.

In the stable path:

- a character with `CHAR_ISOVERED == false` blocks;
- an item with `ITEM_ISOVERED == false` blocks;
- gold does not set the blocking flag;
- other object types in the inspected switch do not set the blocking flag.

Only when no blocker is found does the code run PREOVER callbacks, mutate the
character/object coordinate, then run POSTOVER callbacks.

This is why classic Warp can be invisible and overable: it is a character-like
event object whose overability permits entry, after which POSTOVER performs the
warp.

## 7. Relationship to the recovered Taiwan v1.0 client cache

Taiwan v1.0 binary work has already established:

```
network map protocol
 -> map\%d.dat
 -> tile / parts / event cache planes
```

The client descendant source also derives a separate `hitMap` after loading
tile/parts/event data. That supports the architectural conclusion that raw
DAT plane values should not be directly treated as a final one-bit collision
map.

The remaining early-version seam is the exact image-number property mapping
used to turn tile/parts image ids into collision attributes.

## 8. Reconstruction implementation

Deterministic artifact:

- `tools/stoneage_map_collision_model.py`
- `tests/test_stoneage_map_collision_model.py`

The model deliberately requires explicit per-image metadata and raises on an
unknown image id. It covers:

- object WALKABLE modes 0/1/2;
- tile dependency under object mode 1;
- flying HAVEHEIGHT behavior;
- target dynamic character/item overability;
- one-cell movement constraint;
- diagonal orthogonal-side static checks.

It does **not** invent:

- Taiwan v1.0 / JSS image-property table contents;
- pathfinding behavior beyond one historical step;
- modern collision simplifications;
- bus/transparent/private-server movement bypasses as baseline behavior.

## Evidence status

- **STRONG DESCENDANT FACT:** static map cells supply tile + object image ids.
- **STRONG DESCENDANT FACT:** walkability is obtained from image metadata, not
  by testing whether a raw map cell id is zero/nonzero.
- **STRONG DESCENDANT FACT:** object WALKABLE 0/1/2 has block/defer/force
  semantics.
- **STRONG DESCENDANT FACT:** flying uses HAVEHEIGHT on both tile and object.
- **STRONG DESCENDANT FACT:** diagonal steps require both orthogonal side cells
  to pass static walkability.
- **STRONG DESCENDANT FACT:** target characters/items may independently block
  overlap through their overable flags.
- **EARLY CLIENT CORROBORATED:** Taiwan v1.0 receives tile/parts/event and stores
  them in the three-plane DAT cache.
- **OPEN:** exact Taiwan v1.0/JSS image-property table and whether every
  descendant edge case above is unchanged from the earliest commercial build.

## Consequence

The single-player runtime can now use a correct collision **algorithm** once a
validated image-property dataset is supplied. Until that dataset is recovered,
the explicit collision verdict remains the safe default at the historical
runtime boundary.
