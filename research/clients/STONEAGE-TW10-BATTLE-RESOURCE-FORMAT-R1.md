# StoneAge Taiwan v1.0 Battle Resource Format — R1

Date: 2026-09-19

## Scope

This note fixes the reconstruction boundary for the accepted Taiwan Waei/JSS StoneAge v1.0 retail battle resources.

Primary v1.0 evidence is generated directly from the accepted retail-disc specimen by:

- `tools/stoneage_tw10_client_inventory.py`
- `research/recovered/STONEAGE-TW10-CLIENT-INVENTORY-R1.txt`
- `research/recovered/STONEAGE-TW10-BATTLE-DATASET-R1.txt`

A preserved later client source tree is used only as a lineage control:

- `BismarckDD/stoneage`
- pinned commit `999ffdf1d220ec6666eb65339180689c9caf1876`
- already registered as `SRC-CODE-DESC-STONEAGE-BISMARCKDD-999FFDF1`

No proprietary resource payload bytes are committed.

## FACT — v1.0 battle address/container structure

The v1.0 battle address table contains 233 unique records and partitions `battle_1.bin` exactly and contiguously:

- address records: 233
- total record bytes: 185,892
- container bytes: 185,892
- start offset: 0
- gaps: 0
- overlap: 0
- unresolved names: 0

Those 233 records comprise:

- 218 `battle*.sab` records, totaling 175,272 bytes;
- 15 `Palet_1.sap` through `Palet_15.sap` records, totaling 10,620 bytes.

The palette records are interleaved in the historical address-table order. They must not be re-sorted when reconstructing the exact container.

`Palet_0.sap` is a sixteenth disc-resident palette file but is not referenced by the 233-record battle address table.

## FACT — all 218 v1.0 SAB files have one fixed physical shape

Direct parsing of all 218 disc-resident SAB files establishes:

- 218 / 218 files are exactly 804 bytes;
- 218 / 218 begin with the exact four bytes represented as ASCII `SAB `;
- after those four bytes, 800 bytes remain;
- 800 bytes divide exactly into 400 16-bit units;
- total units across the corpus: 87,200.

Therefore the byte-level v1.0 SAB envelope is:

```text
offset 0x000: 4 bytes  = "SAB "
offset 0x004: 800 bytes = 400 × 16-bit units
total: 804 bytes
```

This is direct original-client evidence.

## LINEAGE-SUPPORTED INTERPRETATION — 20×20 big-endian graphic IDs

The pinned descendant client function `ReadBattleMap` preserves the following behavior:

1. reads four header bytes and checks for `SAB`;
2. reads each following pair as:
   `tile = (c1 << 8) | c2`;
3. preserves an older drawing branch with nested `20 × 20` loops;
4. submits those tile values as graphics IDs to the battle-map renderer.

That source also contains a later enlarged 33×33 branch and later `.sabex` resources, so its active build must not be projected wholesale onto v1.0.

The v1.0 physical shape independently closes the older branch exactly:

```text
4-byte header + (20 × 20 × 2-byte value) = 804 bytes
```

Accordingly the reconstruction profile should treat the v1.0 800-byte payload as a **20×20 grid of big-endian uint16 graphic IDs**, while retaining the evidence label **lineage-supported interpretation** until the same read/shift loop is independently localized in the original `sa_3.exe`.

A simple ADRN-domain check does not independently prove byte order: all 87,200 values resolve to existing v1.0 ADRN bitmap numbers under both byte-order interpretations because the v1.0 bitmap-number domain is broad. The inventory deliberately records this failed discriminator rather than using it as false confirmation.

## FACT — all 16 v1.0 SAP files have one fixed physical size

Direct disc-byte inspection establishes:

- 16 / 16 `Palet_*.sap` files are exactly 708 bytes;
- `Palet_1` through `Palet_15` participate in the battle container;
- `Palet_0` is present separately;
- the 36-byte suffix is not identical across the corpus: six distinct suffix hashes occur.

Thus the entire 708-byte record cannot be replaced by a single shared constant tail.

## LINEAGE-SUPPORTED INTERPRETATION — first 672 SAP bytes are 224 color triplets

The pinned descendant client palette loader preserves a list containing `Palet_1.sap` through `Palet_15.sap`, then `Palet_0.sap`.

Its palette read loop covers palette indices 16 through 239 inclusive and reads three bytes per entry in blue/green/red order:

```text
224 entries × 3 bytes = 672 bytes
```

Applied to each 708-byte v1.0 SAP file this leaves:

```text
708 - 672 = 36 bytes
```

The inventory records separate SHA-256 values for the candidate 672-byte consumed region and the 36-byte suffix for every v1.0 palette.

The reconstruction-safe interpretation is therefore:

- first 672 bytes: strongly lineage-supported as 224 sequential B/G/R color triplets;
- final 36 bytes: **OPEN semantics**;
- do not discard or synthesize the final 36 bytes when preserving historical provenance.

## Reconstruction keys

`research/recovered/STONEAGE-TW10-BATTLE-DATASET-R1.txt` is the canonical reconstruction index for this stage. Each historical address-table record retains:

- address-table index;
- container offset;
- byte length;
- resource name;
- resolved disc path;
- resource class;
- SHA-256.

That key is stable enough to drive a modern importer without committing the original payload.

## Next work

The battle file-boundary/dataset task is complete enough to stop broad inventory work.

The next primary reconstruction dataset is the stable v1.0 graphics/animation identity layer:

1. export REAL/ADRN metadata keyed by all 125,996 v1.0 bitmap IDs;
2. export SPR/SPRADRN group, animation and frame relationships keyed by the 464 v1.0 sprite groups;
3. preserve hashes, offsets, dimensions, compression/format metadata and cross-references without committing proprietary image payloads;
4. then build the audio reconstruction crosswalk.

A later original-`sa_3.exe` binary pass may promote SAB byte order / 20×20 semantics from lineage-supported interpretation to direct v1.0 runtime fact.
