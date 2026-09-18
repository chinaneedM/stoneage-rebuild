# StoneAge Warp / Map Transition Core R1

Status: **fixed-descendant deterministic reconstruction with later transition layers separated**
Scope: classic overlap Warp NPCs, the shared coordinate-warp primitive, party behavior, dialogue WarpMan behavior, later mapwarp objects, and later no-exit login relocation.

## Evidence controls

Fixed descendant revisions:

- `gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
- `iriselia/StoneAge@9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
- `BismarckDD/stoneage@999ffdf1d220ec6666eb65339180689c9caf1876`

Primary files:

- `gmsv/src/npc/npc_warp.c` and equivalents;
- `gmsv/src/char/char_walk.c` and equivalents;
- `gmsv/src/char/char.c` and equivalents;
- `gmsv/src/npc/npc_warpman.c` and equivalents;
- later `gmsv/src/map/map_warppoint.c`;
- later `readmap.c` / `readmap.h` `_MAP_NOEXIT` branch;
- fixed version headers.

The fixed descendants are later than launch. This report distinguishes the longstanding/simple mechanism from later feature layers and does not claim a 1999/JSS chronology without clean early evidence.

## 1. Classic field transition: invisible overlap Warp NPC

The ordinary `NPC_Warp` path represents a map exit/portal as a character/NPC object.

For the simple legacy argument form, initialization parses:

```
floor|x|y|optional-time-token
```

The first three fields are the destination.

Initialization requires `MAP_IsValidCoordinate(floor,x,y)`. If invalid, the Warp NPC is disabled/rejected.

A valid simple Warp NPC is configured as:

- `CHAR_TYPEWARP`;
- invisible;
- overable;
- non-attackable;
- carrying a Warp event type, optionally differentiated by old time token handling.

This means the original transition authority is server-side object state, not a client-only visual tile.

## 2. Walking triggers PREOVER / move / POSTOVER

`CHAR_walk` resolves the destination cell and first rejects non-overable objects.

For overable contents, the ordering is:

```
PREOVER callbacks
 -> write player floor/x/y
 -> move the map object
 -> increment walk count
 -> POSTOVER callbacks
 -> OFF callbacks for the old cell
```

`NPC_WarpPostOver` calls `NPC_WarpWarpCharacter`.

The Warp watch callback also explicitly requires:

- object is a player;
- action is walking;
- the player was not already standing on that same event coordinate.

Therefore the classic portal is an **after-entry overlap transition**: the character first steps onto the Warp NPC cell, then the warp callback changes floor/x/y again.

## 3. Destination validation happens again at execution

Even after initialization, `NPC_WarpWarpCharacter` reparses/resolves the destination and calls `MAP_IsValidCoordinate` before invoking the shared warp primitive.

`floor == -1` is treated as no warp.

The shared `_CHAR_warpToSpecificPoint` also validates the destination before mutating position.

Thus there are multiple validation layers in the ordinary path.

## 4. Shared warp primitive

`_CHAR_warpToSpecificPoint` performs the actual authoritative relocation.

Observed order:

1. validate destination floor/x/y;
2. notify/remove the old visible object state around the previous coordinate;
3. set character `FLOOR/X/Y`;
4. set object `floor/x/y`;
5. call `MAP_objmove` from old coordinate to new coordinate;
6. refresh encounter minimum/maximum if destination lookups return values other than -1;
7. refresh client/status/around-map state;
8. clear walk-array state;
9. for a player who is not a party client, set `CHAR_ISWARP=1`;
10. warp the configured follow-pet object to the same destination;
11. run later optional map/effect hooks.

The function returns TRUE after a valid-destination transition.

### MAP_objmove failure is not transactional

Character and object coordinates are assigned before `MAP_objmove`.

If `MAP_objmove` fails, the old code logs an error but does not roll the coordinate assignments back and still reaches the normal return path.

This is a historical consistency hazard. The modern rebuild should use an atomic/validated map move, but the old behavior remains documented.

## 5. Encounter state is refreshed by warp

After relocation the warp primitive queries destination encounter minimum and maximum.

Each corresponding WORK field is replaced only if the query result is not -1.

This connects map transition semantics to the already reconstructed encounter system: changing maps can immediately change the character's encounter probability bounds.

## 6. Classic overlap Warp does not directly teleport a whole party

The classic `NPC_WarpWarpCharacter` calls the warp primitive for only the player who triggered the overlap.

It does not loop the party array.

Party walking is a separate mechanism: after the leader walks, party followers are advanced along the leader's old path. A follower can therefore enter the same Warp cell and trigger the same Warp NPC independently.

This distinction matters:

> classic Warp party behavior emerges from follow-walking + per-character overlap events, not from one group-teleport transaction.

The shared warp primitive also does not project itself across party membership.

## 7. Dialogue WarpMan has explicit party projection

`NPC_WarpMan` is a different mechanism.

Its `WARP` action resolves a destination, validates it, then examines party mode:

- no party -> warp only the talker;
- party leader -> use the leader as parent;
- party client -> resolve the party leader from the client's first party index.

It then loops the parent's party slots and calls `CHAR_warpToSpecificPoint` for every valid member.

Therefore dialogue WarpMan has explicit same-destination group teleport semantics, unlike the classic overlap Warp.

Later ticket, event, ranking, treasure and conditional branches around WarpMan remain versioned.

## 8. Later _MAP_WARPPOINT / mapwarp.txt layer

The source tree also contains a later `map_warppoint.c` system behind `_MAP_WARPPOINT`.

The fixed gavinlinasd and iriselia version headers enable it in a section annotated around later 6.0-era features; the inspected Bismarck version header does not expose the same enabled define in the corresponding search.

This later layer:

- allocates up to 5000 map warp-point records;
- reads `mapwarp.txt`;
- stores source floor/x/y and destination floor/x/y;
- creates `OBJTYPE_WARPPOINT` map objects;
- checks that the triggering source coordinate exactly matches the record;
- validates the destination;
- suppresses destination floor 777;
- warps the triggering character;
- if that character is party leader, explicitly loops and warps the remaining valid party members.

This is not treated as the launch-era foundation merely because the source exists.

A further fixed-source interaction reinforces the version boundary: when `_MAP_WARPPOINT` is enabled, the simple old `NPC_WarpInit` path can be rejected/replaced while newer FREEMORE handling remains available.

## 9. Random encounters and warp cells

The walking code scans objects on the current coordinate before random-encounter dispatch.

When an event object reports ordinary `CHAR_EVENT_WARP`, the code suppresses the normal random encounter trigger for that step.

This prevents the ordinary warp cell from simultaneously generating a random encounter in the observed path.

Time-specific event variants need not be assumed identical unless independently verified; R1 records only the explicit ordinary `CHAR_EVENT_WARP` check.

## 10. Later _MAP_NOEXIT is a login relocation layer, not a walk portal

The fixed descendants also compile a later `_MAP_NOEXIT` system described in version comments as a special-map “do not resume in place / return to specified point” feature.

`readmap.c` loads `data/map/map_noexit.txt` while loading maps.

For each configured floor it records:

- destination floor;
- destination X;
- destination Y;
- `map_type`.

This does not create a normal walk-triggered portal. It is consulted during login.

### Packed representation

The fixed code stores the configured destination as:

```c
(exfloor << 16) + (ex_X << 8) + ex_Y
```

and later decodes:

- floor from bits above 16;
- X from 8 bits;
- Y from 8 bits.

No pre-pack mask is applied to oversized X/Y values. Therefore the representation safely assumes byte-sized coordinates and can corrupt adjacent packed fields if content violates that assumption.

This is a representation hazard, not a modern design target.

## 11. appear.txt precedes _MAP_NOEXIT during login

In the inspected older login source, the order is:

1. test `CHAR_isAppearPosition(current floor)`;
2. if matched, replace position with `LASTTALKELDER` coordinate;
3. later run the optional `_MAP_NOEXIT` lookup using the **current floor at that moment**.

Therefore, if an original saved floor is in `appear.txt` and appear handling moves the character away first, a no-exit entry keyed only to the original saved floor will not subsequently be consulted.

The two systems are not interchangeable:

- `appear.txt`: older floor-membership -> elder return behavior;
- `_MAP_NOEXIT`: later per-map login relocation policy with configured destination/type.

## 12. _MAP_NOEXIT elder/configured-exit rule

When a no-exit entry exists, the login branch first resolves the player's `LASTTALKELDER` coordinate if available.

If `map_type >= 0`:

- if elder floor equals `map_type`, keep the elder coordinate;
- otherwise use the configured packed exit coordinate.

If `map_type < 0`, the elder coordinate remains preferred.

The resulting floor must pass `CHECKFLOORID` before the character's login coordinates are changed.

This is later/versioned behavior and should not be used to reinterpret the older appear table.

## 13. Deterministic artifacts

- `tools/stoneage_warp_transition_model.py`
- `tests/test_stoneage_warp_transition_model.py`
- `.github/workflows/validate-stoneage-warp-transition.yml`

Regression coverage includes:

- legacy pipe destination parsing;
- invalid legacy destination rejection;
- invisible/overable Warp NPC state;
- after-entry player-walk trigger conditions;
- destination rejection before mutation;
- destination encounter-bound refresh;
- non-transactional `MAP_objmove` failure behavior;
- `CHAR_ISWARP` party-client distinction;
- follow-pet relocation;
- classic overlap Warp single-actor direct target;
- WarpMan explicit party projection;
- later mapwarp source validation / floor-777 suppression / party projection;
- no-exit packed-coordinate assumptions;
- no-exit elder-versus-configured-exit rule;
- appear-before-noexit login ordering.

## Evidence status

- **FACT:** classic simple Warp NPCs store destination floor/x/y in their NPC argument string.
- **FACT:** their destination is validated at initialization and again before warp.
- **FACT:** valid Warp NPCs are invisible, overable and non-attackable.
- **FACT:** walking runs POSTOVER only after position/object movement into the target cell.
- **FACT:** classic Warp directly relocates only the triggering player.
- **FACT:** the shared warp primitive validates destination before mutation.
- **FACT:** the shared warp primitive updates character/object coordinates and then calls `MAP_objmove`.
- **FACT:** failed `MAP_objmove` is logged without state rollback in the fixed source.
- **FACT:** warp refreshes encounter min/max when destination queries succeed.
- **FACT:** non-party-client players get `CHAR_ISWARP=1` in the primitive.
- **FACT:** configured follow pet is warped to the same destination.
- **FACT:** dialogue WarpMan explicitly loops party members.
- **FACT:** ordinary Warp event cells suppress the observed random-encounter dispatch for that step.
- **VERSIONED:** `_NEW_WARPPOINT` conditional/random Warp extensions.
- **VERSIONED:** `_MAP_WARPPOINT` / `mapwarp.txt` object system and its direct leader-party projection.
- **VERSIONED:** `_MAP_NOEXIT` special-map login relocation system.
- **OPEN:** exact 1999/JSS portal content representation and which classic Warp semantics were present at launch.
- **OPEN:** precise commercial-version chronology between simple Warp, WarpMan, new conditional Warp and mapwarp object layers.
- **OPEN:** early clean-client/server content needed to map every historical portal edge.

## Next seam

The ordinary state-transition loop is now connected through:

```
movement
 -> overlap portal
 -> authoritative coordinate warp
 -> encounter-bound refresh
 -> login non-resume policies
```

The next highest-value gap from the Phase 0 audit is the **NPC/world-content graph**:

- creation/template/include relationships;
- NPC class/function dispatch;
- floor/x/y placement;
- argument/config linkage;
- classification of early/core NPC types versus later event/expansion packages.

That graph should be aggregate/provenance-preserving and should not commit the original proprietary NPC content payloads.
