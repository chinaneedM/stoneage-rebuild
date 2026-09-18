# StoneAge 2.5 DAT Runtime Semantics — R1

Date: 2026-09-18

## Scope and evidence boundary

This note resolves the current highest-priority map-cache question for the recovered StoneAge 2.5 corpus:

- what the client `.DAT` layers represent;
- how those layers are populated over the network;
- how rendering and collision consume them;
- which observations are direct recovered-byte facts versus descendant-source evidence.

Recovered bundle anchor:

`d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`

The recovered runtime is mixed/modified. Therefore exact behavior in the recovered executable is not inferred solely from later source. The conclusions below are strongest where recovered-byte structure and independent descendant client/server source agree.

## 1. Runtime cache shape — FACT for the recovered corpus

The recovered map directory contains **1,011 DAT files**.

The current probe validates:

- **995** normal three-layer DAT files;
- **16** special/invalid entries under the normal parser:
  - 13 zero-byte numeric placeholders;
  - `BGM0.DAT`, `BGM1.DAT`, `BGM2.DAT`, each two bytes.

Every one of the 995 normal files is exactly:

```text
uint32 width
uint32 height
uint16 tile[width * height]
uint16 parts[width * height]
uint16 event[width * height]
```

Total cells across the 995 normal caches: **8,354,525**.

Derived report:

`research/recovered/STONEAGE-25-DAT-PROBE-R1.txt`

## 2. Network origin of the three client layers — descendant-source verified

Two descendant client trees preserve `map\\%d.dat` as the local map cache.

Primary source-lineage anchor used here:

- `BismarckDD/stoneage` commit `999ffdf1d220ec6666eb65339180689c9caf1876`

Relevant files:

- `client/stoneage/system/map.cpp`
- `client/stoneage/system/netproc.cpp`
- `client/stoneage/system/loadrealbin.cpp`
- `client/stoneage/systeminc/loadrealbin.h`
- `server/gmsv/map/readmap.c`
- `server/gmsv/map/map_deal.c`

Independent client-side structural control:

- `Signally190/sking-sacli` commit `40cb67ef090ebc0cffd57ca947871bdfd0b18331`
- `system/map.cpp`

The server-side `MAP_getdataFromRECT` serializes three rectangular channels in order:

1. `MAP_map[floor].tile[]`
2. `MAP_map[floor].obj[]`
3. per-cell event type obtained from map objects / character `CHAR_WORKEVENTTYPE`

The client `lssproto_M_recv` parses the corresponding three strings into:

1. `tile[]`
2. `parts[]`
3. `event[]`

and writes them with `writeMap`.

Therefore, in this source lineage:

**server `obj` → client `parts`**

This is an important naming boundary. Client `parts` is the map object/overlay graphic channel; it is not the runtime object-list itself.

## 3. DAT is a local cache, not the authoritative world map

The client does not merely open a packaged immutable map.

The source lineage implements the following cycle:

1. client reads its local DAT rectangle;
2. server supplies map checksums for tile / obj / event;
3. client compares the local rectangle;
4. on mismatch or missing data, client sends `M` for the rectangle;
5. server returns tile / obj / event data;
6. client rewrites that rectangle into `map\\%d.dat`.

This makes the DAT family a **persistent client-side runtime cache populated/validated from server map state**.

For reconstruction purposes, the server map representation and the client DAT cache should therefore be modeled as separate layers even when they share the same visual IDs.

## 4. `tile` semantics

### Rendering

The client renders ordinary tile graphic IDs as the base map surface with `DISP_PRIO_TILE`.

### Collision

`readHitMap` also consumes `tile`.

For graphic-like tile values, the client:

1. maps the tile/action number through `realGetNo`;
2. reads ADRN `MAP_ATTR.hit` through `realGetHitFlag`;
3. derives local collision state from that attribute.

Small/control values have explicit special-case handling in `readHitMap`; they must not all be treated as normal ADRN graphic IDs.

### Recovered-byte corroboration

Across the 995 valid DAT caches:

- cells with tile values > `CG_INVISIBLE(99)`: **3,758,357**
- mapped through recovered ADRN `attr.bmpnumber`: **3,599,419**
- unresolved references: **158,938**
- mapped-reference rate: approximately **95.77%**

That high mapping rate materially corroborates the source interpretation that the tile channel stores client graphic/action identifiers, while also showing that this mixed corpus contains IDs not resolvable in the recovered ADRN set.

## 5. `parts` semantics

### Rendering

The client maps ordinary `parts` values through `realGetNo`, obtains image geometry, and inserts them into the parts/display-priority path.

### Collision footprint

Unlike a base tile, a part can occupy a collision footprint extending across multiple grid cells.

`readHitMap` uses:

- `realGetHitFlag`
- `realGetHitPoints`

to project the part's ADRN `atari_x / atari_y` footprint into the derived hit map.

Recovered mapped parts show many non-1×1 footprints, including 3×3, 3×2, 2×3, 1×2 and larger shapes. This directly fits the descendant collision algorithm.

### Recovered-byte corroboration

Across the 995 valid DAT caches:

- `parts > 99` references: **325,744**
- ADRN-mapped references: **277,037**
- unresolved references: **48,707**
- mapped-reference rate: approximately **85.05%**

The lower mapping rate than tile is compatible with the mixed/modified resource lineage and should not be silently normalized away.

## 6. `event` is an event-type channel plus client cache flags

The descendant event enum is:

- 0 — NONE
- 1 — NPC
- 2 — ENEMY
- 3 — WARP
- 4 — DOOR
- 5 — ALTERRATIVE
- 6 — WARP_MORNING
- 7 — WARP_NOON
- 8 — WARP_NIGHT

The server fills the event channel from per-cell map objects whose character work state exposes a non-zero `CHAR_WORKEVENTTYPE`.

The client additionally reserves high bits:

- `0x8000` — `MAP_READ_FLAG`
- `0x4000` — `MAP_SEE_FLAG`

`writeMap` ORs these cache flags into event values when storing received rectangles.

The client checksum path masks event values with `0x0fff` before comparison. Therefore:

**low 12 bits = event payload/type domain; high bits include local cache/read/visibility state.**

High bits must not be modeled as server event-type bits.

## 7. Recovered event data strongly validates the enum, with one quarantined outlier

Across all **8,354,525** cells:

- low-12 event values recognized as 0–8: **8,310,573**
- low-12 values outside 0–8: **43,952**

Crucially, **all 43,952 unknown low-12 values occur in one file only: `1021.DAT`**.

`1021.DAT`:

- dimensions: **407 × 144**
- cells: **58,608**
- unknown low-12 event cells: **43,952**
- unknown ratio: approximately **74.99%**

Therefore the evidence is not “the event layer generally contains thousands of undocumented event types.”

The stronger current reading is:

- **994 of the 995 structurally valid DAT caches have no low-12 event values outside the descendant 0–8 enum**;
- `1021.DAT` is a single exceptional cache and must be quarantined for separate corruption/version/private-server analysis.

Until that outlier is explained, its unknown values must not be promoted into the canonical event model.

Observed recognized event counts over the full corpus are:

- NONE: 8,305,797
- NPC: 11
- ENEMY: 740
- WARP: 3,951
- DOOR: 9
- ALTERRATIVE: 17
- WARP_MORNING: 18
- WARP_NOON: 18
- WARP_NIGHT: 12

## 8. Collision is derived; DAT does not contain a fourth hit layer

The client builds `hitMap` at runtime from:

- tile graphic attributes;
- parts graphic attributes and collision footprints;
- selected small/control values;
- event occupancy, including `EVENT_NPC`.

There is no fourth serialized DAT collision layer in the inspected format.

This matters architecturally: a modern rebuild should keep the canonical map data separate from the **derived navigation/collision representation**.

## 9. Client prediction and server authority are separate concerns

The descendant server does not trust a client-derived hit map as world authority.

Server `MAP_walkAbleFromPoint` evaluates its own:

- tile channel;
- object channel;
- map-image walkability attributes.

Other character/object collision and event handling is performed server-side during movement processing.

Therefore the historical architecture already separates:

- **client-side local render/navigation cache and immediate collision representation**
- **server-side authoritative map/movement state**

That separation should be preserved conceptually in a modern rebuild even if a future single-player architecture hosts both responsibilities in one process.

## 10. Reconstruction model implied by current evidence

For a clean modern implementation, do **not** copy the legacy file/cache arrangement literally.

Use an explicit model such as:

- canonical map tile layer;
- canonical static map-part/object graphic layer;
- event/spawn/warp definitions;
- graphic metadata / collision-footprint registry;
- derived collision/navigation grid;
- runtime entities;
- persistence/cache layer only where actually useful.

A legacy DAT importer can reconstruct those inputs, but the legacy high-bit cache flags should remain import/runtime compatibility metadata rather than canonical world design data.

## 11. Remaining open questions

1. Why `1021.DAT` alone contains 43,952 non-enum low-12 event values.
2. Which unresolved tile/parts IDs are caused by:
   - missing/alternate ADRN resource revisions;
   - private-server additions;
   - version skew;
   - special control semantics.
3. Exact semantics of the small tile/parts control ranges below `CG_INVISIBLE`.
4. How the recovered DAT cache compares with a future clean 2.5 / 1.82 / 1.74 / 1.74a / JSS specimen.
5. Which cache behaviors are original versus later auto-update additions in descendant source.

## Evidence-grade summary

- recovered DAT three-layer byte layout: **FACT for this recovered corpus**
- `tile / parts / event` naming and read/write behavior: **strong descendant-source evidence, directly structure-corroborated**
- server `obj` → client `parts`: **descendant client/server source fact**
- DAT as network-refreshed persistent client cache: **descendant client/server source fact**
- collision derived from tile/parts ADRN attributes: **descendant client source fact, recovered ADRN linkage strongly corroborating**
- 0–8 event domain across 994/995 valid recovered caches: **FACT for this recovered corpus**
- `1021.DAT` unknown-event region: **FACT / quarantined anomaly**
- exact equivalence to 1999 JSS behavior: **OPEN**
