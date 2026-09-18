# StoneAge 2.5 Verified Resource Formats — R1

Date: 2026-09-18

## Scope and evidence boundary

This specification records format properties **directly validated against the recovered StoneAge 2.5 preservation corpus** whose reassembled bundle SHA-256 is:

`d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`

The recovered runtime bundle is mixed/modified and is **not** a clean runtime baseline. The resource corpus is nevertheless coherent enough for deterministic format archaeology.

These findings are therefore:

- **FACT for this recovered 2.5 resource corpus**;
- strong evidence for persistent StoneAge format lineage;
- **not automatic proof** that every 1999 JSS retail/beta byte used the same revision.

No proprietary source payload is committed. Only hashes, parsers, tests and derived reports are retained.

## 1. ADRN index format — verified

Recovered file:

- `data/adrn_15.bin`
- SHA-256: `92d0137590d35a7a1f4fb11af3ad13bbc585813a4b0e1e3f933c397007fbff74`
- byte size: 18,765,120

Observed:

- record width: **80 bytes**
- record count: **234,564**
- remainder: **0**

The leading Win32 little-endian fields match the descendant `ADRNBIN` layout:

- offset 0: `bitmapno` — uint32
- offset 4: `adder` — uint32 REAL offset
- offset 8: `size` — uint32 authoritative REAL block length
- offset 12: `xoffset` — int32
- offset 16: `yoffset` — int32
- offset 20: `width` — uint32
- offset 24: `height` — uint32
- remaining 52 bytes: attribute structure / metadata

There are **147 repeated bitmap numbers** near the end of the recovered ADRN. Descendant code assigns records sequentially into `adrnbuff[bitmapno]`, so later duplicate IDs are compatible with an override/patch behavior. That semantic is plausible but should remain explicitly tied to the descendant implementation until more original-version comparison data exist.

## 2. REAL block coverage — verified

Recovered file:

- `data/real_15.bin`
- SHA-256: `c7640643804d550bc07e33661103fb7b5f557ee01e68a5a5d92382c5305c2b0d`
- byte size: 763,908,374

All 234,564 ADRN records:

- point within REAL bounds;
- point to blocks beginning with `RD`;
- are ordered nondecreasing by offset;
- are exactly contiguous from the first block through the final byte;
- produce **0 gaps**;
- produce **0 overlaps**;
- leave **0 unreferenced trailing bytes** in REAL.

Thus, for this corpus, ADRN is not merely correlated with REAL: it partitions the complete REAL file into a deterministic sequence of indexed blocks.

## 3. RD header — verified

Each REAL image block begins with a 16-byte header:

- bytes 0–1: ASCII `RD`
- byte 2: compression/version flag
- byte 3: padding/unknown byte
- bytes 4–7: width bit pattern
- bytes 8–11: height bit pattern
- bytes 12–15: stored size field

Observed flags:

- `0x01`: **234,556** blocks
- `0x00`: **8** blocks

The ADRN width/height bit patterns match the corresponding RD width/height bit patterns for all **234,564** records.

Two records contain unusual signed interpretations of the 32-bit height field (`-5` and `-3`) while the ADRN and RD bit patterns still agree exactly. They are treated as special/non-normal image records, not parser misalignment.

## 4. RD flag 0 raw-block behavior — verified

The eight `flag=0` blocks occur at ADRN indices:

`7339, 8603, 9139, 9140, 9141, 9155, 9156, 9157`

For all eight:

- ADRN `size` equals **16 + width × height**;
- the RD header's own stored-size field does **not** equal the block length.

This behavior matches the descendant encoder's raw branch, which writes a pointer-derived value into `header->size` while the decoder ignores that field for flag 0 and reads exactly `width × height` raw indexed pixels after the 16-byte header.

Operational rule:

**For flag 0, ADRN `size` is authoritative; the RD header stored-size field is not a trustworthy block-length field.**

## 5. Legacy RD RLE codec — real-byte validated

Tool:

`tools/stoneage_rd_codec.py`

Deterministic tests cover all nine control families:

- literal: `0x0n / 0x1n / 0x2n`
- repeated byte: `0x8n / 0x9n / 0xAn`
- repeated zero: `0xCn / 0xDn / 0xEn`

with 4-bit, 12-bit and 20-bit run-length forms.

Real-client validation report:

`research/recovered/STONEAGE-25-RD-DECODE-VALIDATION-R1.txt`

Results:

- sampled/selected real records: **4,225**
- decode successes: **4,225**
- decode failures: **0**
- all eight flag-0 blocks included
- aggregate derived sample hash:
  `8fa896927095a931f3f3383291474d5171d25c6291af877b877b5fc4363ccf42`

This is direct recovered-byte evidence that the reconstructed legacy RD decoder is valid for a broad sample of this 2.5 corpus.

## 6. `.MAP` single-layer structure — verified, semantics open

Recovered core map directory contains:

- **1,030 `.MAP` files**

Every one of the 1,030 files matches:

`8-byte header + width × height × 2 bytes`

Header:

- uint32 little-endian width
- uint32 little-endian height

Payload:

- exactly one uint16 value per cell

No structural exceptions were found among the 1,030 `.MAP` files.

Examples:

- `100.MAP`: 800×800 → 1,280,008 bytes
- `1000.MAP`: 160×160 → 51,208 bytes
- `10001.MAP`: 50×50 → 5,008 bytes

**The semantic meaning of the uint16 cell value remains OPEN.**

Do not call this payload "the tile layer" merely because its dimensions look like a map grid.

## 7. `.DAT` three-layer runtime/cache structure — strongly verified

The same directory contains:

- **1,011 `.DAT` files**

Descendant client source `map.cpp` explicitly creates/reads/writes:

- 8-byte width/height header
- uint16 `tile[width×height]`
- uint16 `parts[width×height]`
- uint16 `event[width×height]`

For normal non-empty recovered DAT files, observed sizes match:

`8 + width × height × 2 × 3`

Examples:

- `100.DAT`: 800×800 → 3,840,008 bytes
- `1000.DAT`: 160×160 → 153,608 bytes
- `10001.DAT`: 50×50 → 15,008 bytes

The corpus also contains zero-byte DAT placeholders/special entries. These must not be forced through the normal three-layer parser.

The completed DAT probe now covers the **entire 1,011-file case-insensitive DAT set**:

- structurally valid three-layer caches: **995**
- special/invalid normal-parser entries: **16**
- total cells across valid caches: **8,354,525**

Descendant client/server source additionally resolves the runtime roles:

- server `tile` → client `tile`
- server `obj` → client `parts`
- server per-cell `CHAR_WORKEVENTTYPE` → client `event`
- client `writeMap` adds `MAP_READ_FLAG=0x8000` and `MAP_SEE_FLAG=0x4000` to event values
- client collision is derived at runtime from tile/parts graphic attributes and event occupancy; no fourth DAT hit layer is serialized

Recovered event bytes strongly corroborate the descendant enum: **994 of the 995 valid DAT files contain no low-12 event values outside 0–8**. The sole outlier, `1021.DAT`, contains all **43,952** non-enum low-12 values and is quarantined as a separate corruption/version/private-server anomaly rather than used to expand the canonical event model.

Detailed analysis:

`research/clients/STONEAGE-25-DAT-RUNTIME-SEMANTICS-R1.md`

## 8. `.MAP` is NOT a direct copy of any DAT layer — verified negative result

Byte-level pair report:

`research/recovered/STONEAGE-25-MAP-DAT-RELATION-R1.txt`

Observed:

- MAP files: 1,030
- DAT files: 1,011
- same-stem pairs: 1,007
- structurally valid paired DATs with matching width/height: **995**
- zero-byte/invalid paired DATs: **12**
- MAP-only stems: 23
- DAT-only stems: 4

Across all **995** valid dimension-matched pairs:

- MAP payload == DAT tile layer: **0**
- MAP payload == DAT parts layer: **0**
- MAP payload == DAT event layer: **0**

Therefore:

**The recovered `.MAP` file is a distinct one-layer map-related dataset. It is not simply a serialized copy of any of the three DAT runtime/cache layers.**

This negative result is important. Future work must determine the MAP cell semantics empirically rather than projecting the descendant DAT layer names onto it.

## 9. SPR/SPRADRN — verified

Recovered files:

- `data/spr_4.bin`: 5,588,120 bytes
- `data/spradrn_5.bin`: 10,164 bytes

The recovered SPRADRN is exactly:

`10,164 / 12 = 847 records`

Real-byte validation parses **all 847 records successfully** and walks:

- **70,154 animations**
- **476,378 frame records**
- **472,886** direct ADRN bitmap references
- **3,492** explicit `0xffffffff` sentinel frames

No unresolved non-sentinel bitmap references remain in the current report. Six duplicate SPR numbers/offset groups are retained as observed override/duplicate behavior rather than normalized away.

Derived report:

`research/recovered/STONEAGE-25-SPR-PROBE-R1.txt`

The immediate format target has therefore moved past SPR/SPRADRN to deeper DAT runtime semantics, map-event anomalies and subsequent gameplay-data tables.

## 10. Evidence-grade summary

For recovered StoneAge 2.5 resource corpus:

- ADRN 80-byte record model: **verified**
- ADRN→REAL offset/size semantics: **verified**
- contiguous complete REAL partition: **verified**
- 16-byte RD block header: **verified**
- flag-0 raw-block behavior: **verified**
- legacy RD RLE decoder: **verified on 4,225 real blocks**
- MAP 8-byte header + one uint16/cell: **verified on 1,030 files**
- DAT 8-byte header + three uint16/cell layers: **verified on 995 normal recovered caches; source-backed semantics**
- DAT network/cache role and server `obj` → client `parts`: **descendant client/server source verified**
- DAT event enum 0–8: **recovered-byte corroborated in 994/995 valid caches; `1021.DAT` quarantined anomaly**
- DAT collision as derived runtime state rather than a fourth serialized layer: **descendant client source verified**
- MAP == DAT tile/parts/event: **disproved for all 995 valid paired files**
- MAP cell semantics: **OPEN**
- SPR/SPRADRN 12-byte index + animation/frame stream: **verified across all 847 records**
