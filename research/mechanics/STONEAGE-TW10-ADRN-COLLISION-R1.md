# Taiwan StoneAge v1.0 ADRN collision-property recovery — R1

Date: 2026-09-20

Status: **FACT for the accepted Taiwan Waei/JSS v1.0 retail client; JSS 1999 byte-level provenance remains OPEN**

## Result

The early-client image-number collision-property dataset is now recovered
directly from the accepted Taiwan v1.0 retail disc.

This supersedes the need to substitute later server-side `mapset.txt`
`WALKABLE/HAVEHEIGHT` data for the early-client collision layer.

The derived dataset is:

- `research/recovered/tw10-resource-metadata/COLLISION-ATTR-R1.tsv.gz`
- generated deterministically from `StoneAge/data/adrn_1.bin`;
- no original ADRN/REAL proprietary payload bytes are committed.

The source ADRN file is:

- bytes: **10,079,680**
- SHA-256: `47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8`
- records: **125,996**
- record size: **80 bytes**

## 1. The 80-byte record closes structurally

The accepted v1 ADRN record is exactly 80 bytes.

The stable descendant client defines:

```
ADRNBIN
  28-byte image/index header
  52-byte MAP_ATTR
```

The project had already independently established the same 80-byte record
size from the Taiwan v1 resource itself. Parsing the previously opaque final
52 bytes as `MAP_ATTR` closes the record without padding ambiguity.

The recovered collision-relevant fields are:

- `atari_x`
- `atari_y`
- `hit_raw`
- `height_flag`
- `map_number` (the number used by map tile/parts planes)
- derived `hit_flag = hit_raw % 100`
- derived `priority_type = hit_raw // 100`

Other MAP_ATTR fields remain exported in the parser but are not promoted into
movement semantics unless their consumers are separately recovered.

## 2. Map-number -> bitmap record mapping

The stable client initializes:

```
bitmapnumbertable[attr.bmpnumber] = bitmapno
```

while reading ADRN records in file order.

The Taiwan v1 exporter mirrors that behavior for nonzero `map_number`.
If the same map number occurs more than once, the last ADRN record wins.

Observed Taiwan v1 results:

- nonzero map numbers: **9,286**
- duplicate nonzero map-number assignments: **3**

The duplicates are therefore retained as source-order behavior rather than
collapsed by an invented uniqueness rule.

## 3. Native Taiwan v1 hit flag distribution

Across all 125,996 Taiwan v1 ADRN records:

- `hit_flag = 0`: **122,639**
- `hit_flag = 1`: **3,295**
- `hit_flag = 2`: **62**

Recovered priority-type distribution:

- `priority_type = 0`: **125,803**
- `priority_type = 2`: **88**
- `priority_type = 3`: **105**

No later-server collision table is required to obtain these values.

## 4. Client readHitMap semantics

The engine-facing reference implementation is:

- `tools/stoneage_tw10_hit_map_model.py`

It mirrors the active stable-client `readHitMap()` ordering:

1. initialize local hit-map cells to 0;
2. process the tile plane;
3. process the parts/object plane;
4. apply NPC-event blocking last.

For ADRN-backed map numbers:

- `hit_flag == 0` produces blocked collision;
- `hit_flag == 1` is normally passable;
- `hit_flag == 2` writes the source's override marker value 2.

The v1 `checkHitMap()` movement test blocks only local hit-map value 1.
Value 2 is therefore preserved as a distinct source marker rather than
flattened into a boolean.

For parts with `hit_flag == 0` or `2`, `atari_x/atari_y` define the
collision footprint projected from the object's origin up/right in map-plane
coordinates, matching the source loop.

The source also has a special active branch for parts map numbers
`15680..15732` with `hit_flag == 1`; only the origin cell is forced blocked.

Small reserved map values are handled by the client's explicit switch rather
than ADRN lookup. `CG_INVISIBLE` is 99. Values 60..79 are an explicit
exception and still resolve through ADRN collision metadata.

NPC event type 1 forces the final cell blocked.

## 5. Height is recovered but not silently promoted

The 52-byte MAP_ATTR includes `height`, and Taiwan v1 values are now
recoverable per map number.

However the recovered `readHitMap()` movement path uses `hit` and
`atari_x/atari_y`, not `height`.

Therefore `height_flag` remains preserved reconstruction metadata. It is not
invented into a movement rule merely because later server `mapset.txt`
contains a `HAVEHEIGHT` concept.

## 6. Retail-disc map boundary

The accepted Taiwan v1 retail-disc inventory reports:

- `field_map_disc_files = 0`

The runtime client contains `map\\%d.dat` handling and map-cache behavior,
but the retail disc does not carry a complete field-map corpus.

Therefore this milestone closes the early image collision-property dataset,
not the provenance of every field-map plane.

Field maps remain a separate runtime/cache reconstruction layer.

## 7. Provenance-gated field-cache adapter

The reconstruction now has a strict software bridge for the final missing
field-map layer without inventing any field-map content:

- `StoneAgeDatMapCache` and `parse_stoneage_dat_map_cache()` in
  `tools/stoneage_tw10_hit_map_model.py` parse the descendant-source-
  corroborated `map\\%d.dat` layout exactly: an 8-byte little-endian
  width/height header followed by equal-sized uint16 tile, parts and event
  planes;
- `load_taiwan_v10_collision_profile()` consumes only the committed derived
  `COLLISION-ATTR-R1.tsv.gz` surface and verifies its redundant hit/priority
  columns against `hit_raw`;
- `build_taiwan_v10_hit_map_from_cache()` and
  `build_taiwan_v10_hit_map_from_dat()` compose those planes with the
  recovered Taiwan-v1 collision profile and the already closed v1 hit-map
  algorithm.

This closes an **implementation interface**, not the provenance gap. The DAT
parser intentionally performs no historical inference: a mixed 2.5 DAT can
match the cache layout while still being a later bridge specimen. Tests use
synthetic cache bytes plus the committed derived Taiwan-v1 collision metadata;
no later map payload is promoted into the early baseline.

A real Taiwan-v1/JSS field-map corpus must still be authenticated independently
before its tile/parts/event planes can populate this path.

The single-player reconstruction runtime also exposes a separately named
`walk_step_with_taiwan_v10_hit_map()` boundary (plus its CEP-frequency
variant). It binds the hit map to an explicit floor id and consumes only the
v1 `checkHitMap` verdict. It deliberately does **not** layer the descendant
server's `WALKABLE/HAVEHEIGHT`, diagonal-corner or dynamic-overability rules
onto the early-client path. This keeps both evidence lineages executable
without silently merging their semantics.

## 8. Validation

Deterministic exporter:

- `tools/stoneage_tw10_resource_metadata.py`
- `tests/test_stoneage_tw10_resource_metadata.py`

Collision reconstruction:

- `tools/stoneage_tw10_hit_map_model.py`
- `tests/test_stoneage_tw10_hit_map_model.py`

Validated GitHub Actions:

- gameplay/model run **35511074585** — success;
- repaired real-disc resource export run **35511391125** — success.

The resource-export workflow now also requires
`COLLISION-ATTR-R1.tsv.gz` to exist and pass gzip integrity validation.

## Consequence

Autonomous reconstruction no longer needs to borrow descendant
`WALKABLE/HAVEHEIGHT` values for early-client collision.

The provenance-safe early path is now:

```
field map tile/parts/event planes
 -> Taiwan v1 map_number
 -> Taiwan v1 ADRN MAP_ATTR
 -> v1-compatible readHitMap
 -> checkHitMap movement blocking
```

What remains open is the provenance-complete field-map plane corpus itself,
not the image-number collision metadata.
