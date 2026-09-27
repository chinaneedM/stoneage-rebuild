# StoneAge World-Map Reconstruction Policy — R1

Date: 2026-09-27

## Purpose

Define how field/world maps enter the modern reconstruction now that Taiwan/Waei v1.0 is accepted as the foundation client.

The project must preserve a strict distinction between:

- what the v1 client proves about the **map runtime/cache format**;
- what later recovered map corpora prove about **concrete map payloads**;
- what is merely **resource-compatible** with the v1 visual namespace;
- what the modern game ultimately chooses to include.

## 1. V1 direct boundary

The accepted Taiwan v1.0 retail disc contains no ordinary field-map cache files.

This is not treated as missing/damaged media. Direct v1 runtime evidence establishes that:

- ordinary maps are addressed as `map\\%d.dat`;
- the runtime creates/uses a writable map-cache surface;
- server→client `M` and `MC` protocol callbacks join to map-cache read/write paths;
- field maps therefore belonged to the runtime/server-delivered side of the historical online product.

**Evidence grade: V1_DIRECT.**

Primary evidence:

- `research/recovered/STONEAGE-TW10-RECEIVE-MAP-JOIN-R1.txt`
- `research/recovered/STONEAGE-TW10-MAPCACHE-BINARY-R1.txt`
- `research/clients/STONEAGE-TW10-CLIENT-DATA-BOUNDARY-R1.md`

## 2. Later recovered field-map corpora

Two recovered later map surfaces have already been tested against the Taiwan-v1 graphics/address namespace.

### Recovered 2.5 corpus

- parsed DAT candidates: **995**
- resource-ID compatible with Taiwan v1 profile: **769**
- resource-ID incompatible: **226**
- invalid/non-map DAT objects: **16**

### Recovered 2003 corpus

- parsed DAT candidates: **995**
- resource-ID compatible with Taiwan v1 profile: **773**
- resource-ID incompatible: **222**
- invalid/non-map DAT objects: **16**

Compatibility means that every tile/parts value requiring an ADRN lookup resolves inside the Taiwan-v1 resource profile.

It does **not** prove that a compatible map existed in Taiwan v1.

Primary evidence:

- `research/recovered/STONEAGE-TW10-25-FIELDMAP-COMPAT-R1.txt`
- `research/recovered/STONEAGE-TW10-2003-FIELDMAP-COMPAT-R1.txt`

## 3. Evidence labels for modern world construction

Every imported or reconstructed map must carry one of the following provenance roles.

### V1_DIRECT_FORMAT

The map/cache structure or runtime behavior is directly proven by Taiwan v1 bytes.

This label does not assert concrete historical map membership.

### EARLY_MEMBERSHIP_PROVEN

A concrete map is independently tied to an early official version by strong artifact/version evidence.

This is the strongest historical-content label and must not be assigned from resource compatibility alone.

### LATER_RECOVERED

The concrete map payload belongs to a recoverable later corpus/version surface.

It may be useful as historical StoneAge content, but remains later/version-tagged.

### V1_RESOURCE_COMPATIBLE

A later recovered map uses only graphic/parts IDs resolvable by the Taiwan-v1 resource profile.

This is a compatibility/prioritization label only.

### LATER_ONLY_RESOURCE_DEPENDENCY

A map requires visual IDs not present in the Taiwan-v1 profile.

This is strong evidence that the exact payload cannot be rendered from the accepted v1 visual namespace without later assets.

### DESIGN_RECONSTRUCTED

A modern map or modified historical map created for the new single-player game.

Its historical inspiration may be cited separately, but it is not represented as an original map payload.

## 4. Reconstruction rule

The project no longer waits for the original v1 map server before world implementation can begin.

The modern world-building sequence is:

1. implement the map reader/runtime from the v1-proven cache/transport structure;
2. use resource-compatible later maps as high-priority historical comparison candidates;
3. attach explicit version/provenance tags to every concrete map;
4. recover names, warps, NPC placement, encounter areas, quests and story roles from versioned server/master evidence where possible;
5. make explicit DESIGN decisions where early authoritative content cannot be recovered;
6. selectively incorporate later official-era world content according to DD-012 rather than pretending it belonged to v1;
7. allow deliberate world redesign when required by the single-player/MMORPG-style product direction.

## 5. Important non-equivalence

The following implication is forbidden:

`V1_RESOURCE_COMPATIBLE -> EARLY_MEMBERSHIP_PROVEN`

A 2.5/2003 map may use only old tile IDs because the old asset namespace remained stable. That makes it technically useful for reconstruction and comparison, but does not date the map.

Likewise:

`LATER_ONLY_RESOURCE_DEPENDENCY -> bad map`

Later-only maps may still be desirable design/library content for the final game. They simply require later/recreated visual assets and remain version-tagged.

## 6. Product consequence

This policy removes the historical server dependency from the critical path while preserving provenance discipline.

Taiwan v1 remains the **technical map-runtime foundation**.

Later recovered maps become a **versioned world-content library**.

The final local-first game may then build a coherent world from:

- early/proven historical maps where available;
- later StoneAge maps selected for quality and world coherence;
- independently redesigned/recreated maps where appropriate.

This is consistent with DD-012 and DD-013: historical evidence defines the design DNA and technical boundaries; it does not freeze the final world to one retail-client timestamp.
