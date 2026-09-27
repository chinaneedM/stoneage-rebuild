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


## 7. Cross-version persistence result — 2.5 bridge vs archived 2003 corpus

A complete path/hash comparison of the two recovered later map corpora is now available in:

- `research/recovered/STONEAGE-TW10-FIELDMAP-LINEAGE-R1.txt`.

Results:

- shared valid map paths: **995 / 995**;
- same path + identical SHA-256: **980**;
- same path + changed SHA-256: **15**;
- identical across both corpora **and** Taiwan-v1 resource-compatible in both: **761**;
- changed between corpora but Taiwan-v1 resource-compatible in both: **8**;
- map paths unique to either corpus: **0**.

This materially strengthens the reconstruction value of the later map surface.

### STABLE_LATER_MAP_CANDIDATE

A map may be tagged `STABLE_LATER_MAP_CANDIDATE` when:

1. the same map path exists in both recovered later corpora;
2. the full payload SHA-256 is identical across both;
3. the payload is asset-compatible with the accepted Taiwan-v1 graphics/profile.

There are **761** such candidates in the current comparison.

This label means **strong later-lineage persistence + early-asset compatibility**. It still does **not** mean the concrete layout existed in Taiwan v1.

The 15 changed maps are especially valuable controlled-diff targets because their dimensions remain directly comparable while concrete map bytes evolved. They should be retained as explicit version deltas rather than normalized away.

Operational consequence: world reconstruction should prioritize the 761 stable candidates for names/warps/NPC/encounter/provenance binding before spending effort on later-only or changed maps.


## 8. Engine-neutral provenance enforcement — 2026-09-28

The policy above is now enforced by executable reconstruction code rather than
remaining documentation-only.

Implementation:

- `tools/stoneage_singleplayer_world.py`
- `tools/stoneage_world_map_library.py`
- `tests/test_stoneage_world_map_library.py`

Concrete map provenance is represented by `WorldMapProvenance` with separate
axes for:

- content role:
  - `EARLY_MEMBERSHIP_PROVEN`;
  - `LATER_RECOVERED`;
  - `DESIGN_RECONSTRUCTED`;
- resource relation:
  - `V1_RESOURCE_COMPATIBLE`;
  - `LATER_ONLY_RESOURCE_DEPENDENCY`;
  - `RESOURCE_RELATION_UNKNOWN`;
- optional qualifiers such as `STABLE_LATER_MAP_CANDIDATE`;
- explicit source-version labels;
- explicit evidence references;
- concrete payload SHA-256 where historical recovered bytes are claimed.

The following invariants are executable:

1. `EARLY_MEMBERSHIP_PROVEN` and `LATER_RECOVERED` concrete maps require
   source-version evidence, evidence references and a payload SHA-256.
2. `STABLE_LATER_MAP_CANDIDATE` may only be attached to
   `LATER_RECOVERED + V1_RESOURCE_COMPATIBLE` content with at least two source
   versions.
3. A stable later candidate therefore cannot be silently promoted to
   `EARLY_MEMBERSHIP_PROVEN`.
4. `HistoricalWorldTopology.from_provenance_maps()` is the strict modern-world
   entry point and rejects map definitions carrying only an ambiguous free-text
   evidence label.
5. Legacy low-level topology construction remains available for older tests and
   already-reconstructed mechanics, but new world-content ingestion must use
   the strict provenance-bearing path.

The complete derived lineage report is parsed by
`parse_stable_later_map_manifest()`. The parser rejects sample-limited reports
whose emitted detail rows do not match their declared counts.

Current repository manifest assertions:

- shared later paths: **995**;
- byte-identical later paths: **980**;
- full stable candidate details: **761**;
- changed path details: **15**;
- strict topology produced from stable candidates: **761 maps**;
- every stable candidate remains `LATER_RECOVERED`, never v1 membership.

Validation:

- gameplay model Actions run **36333478060 = PASS**.

**WORLD_MAP_PROVENANCE_CONTRACT_R1 = IMPLEMENTED.**
