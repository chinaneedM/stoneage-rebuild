# StoneAge Waei.net 2001 spr_1.bin Diff — R1

Date: 2026-09-27  
Status: **BYTE-VERIFIED RESOURCE-LINEAGE ANCHOR / EXACT BRANCH OPEN**

## Artifact

Wayback capture timestamp: **2001-06-05 17:45:50 UTC**  
Historical namespace: Waei.net central download / Big5 `修補程式`  
Filename: `spr_1.bin`

Recovered transiently for analysis only:

- bytes: **2,889,630**
- SHA-256: `864fa3f6aaeb7d8d2dc9bdee46cecdc7dcee1af0c8f1ed949e09c0526e6aa17e`
- SHA-1: `e8073bde417020b52ff48e4f8559c938c90fc9cc`
- MD5: `7b40970c8f2a11a523f4a314c78b459e`

The SHA-1-derived Base32 value exactly matches the Wayback CDX digest. Raw payload bytes are not stored in this repository.

## Controlled Taiwan-v1 comparison

Accepted Taiwan v1.0 `spr_1.bin`:

- bytes: **2,889,630**
- SHA-256: `53d5b2d40453a30fd1569637ebf0db7b3010542b00970ec83af0295a3b3ae31a`

The Waei file parses perfectly under the accepted Taiwan v1.0 `spradrn_1.bin`:

- 464 groups;
- 39,065 animations;
- 242,085 frames;
- every group span closes at the same offsets.

Therefore the file is not merely a filename collision: it is a byte-level member of the same StoneAge sprite-resource lineage.

## Delta

Total changed bytes: **16 / 2,889,630 (0.000554%)**.

Only group **102 / spr_no 100102** changes. The changes are four 32-bit `bmp_no` fields:

| Animation | Frame | Taiwan v1.0 | Waei 2001 |
|---:|---:|---:|---:|
| 82 | 0 | `0xFFFFFFFF` | 126235 |
| 83 | 0 | `0xFFFFFFFF` | 126236 |
| 83 | 1 | `0xFFFFFFFF` | 126237 |
| 84 | 1 | `0xFFFFFFFF` | 126238 |

All four target bitmap IDs are absent from the accepted Taiwan v1.0 `adrn_1.bin`.

## Interpretation

**FACT:** a later/different Waei-hosted StoneAge sprite generation activates four image references that Taiwan v1.0 treated as sentinel/no-image frames.

**STRONG HYPOTHESIS:** a companion image-resource update (ADRN/REAL lineage) supplied those four bitmap IDs. The currently indexed same-directory archive has no exact `adrn_1.bin`, `real_1.bin` or `spradrn_1.bin` capture, so the image bytes themselves remain missing.

**OPEN:** exact version, region, download-title binding and relation to the Mainland Dec-2000/Jan-2001 client line.

## Trial-client relation

A 17173 diary published 2001-06-13 recalls a **2001-01-04** Waei-homepage StoneAge trial download of approximately **274 MB**. That online trial route is a separate full-client recovery target. No evidence yet proves that this June `spr_1.bin` was part of that trial build.

## Derived reports

- `research/recovered/STONEAGE-WAEI-DOWNLOAD-CENTER-INDEX-CENSUS-R1.txt`
- `research/recovered/STONEAGE-WAEI-SPR1-BYTE-METADATA-R2.txt`
- `research/recovered/STONEAGE-WAEI-VS-TW10-SPR1-DIFF-R1.txt`
- `research/recovered/STONEAGE-WAEI-VS-TW10-SPR1-FIELD-DIFF-R2.txt`
- `research/recovered/STONEAGE-TW10-BITMAP-126235-126238-R1.txt`
