# StoneAge 2.5 MAP Provenance Correction — R1

Date: 2026-09-18

## Problem

The recovered 2.5 bundle contains two different map-related families under `SA2.5主程式`:

- `stoneage2.5/map/*.DAT`
- `stoneage2.5/map/*.MAP`

An earlier working note treated the single-layer `.MAP` family as if it were an original-client map format. That promotion was premature.

## Internal bundle evidence

The recovered static inventory contains:

- `stoneage2.5/map`: **2,041 files total**
  - **1,030 `.MAP`**
  - **1,011 `.DAT`**
- `SACH-MX0.30/MAP`: **1,009 `.MAP`**

Hash cross-check between the SACH map corpus and the `stoneage2.5/map` `.MAP` corpus:

- same filename present in both: **1,008**
- same filename + identical SHA-256: **905**
- same filename + different SHA-256: **103**
- `stoneage2.5/map` files whose SHA-256 appears anywhere in SACH MAP corpus: **910**

This is strong evidence that the single-layer `.MAP` family is tightly coupled to the SACH external-tool ecosystem.

## Source-lineage evidence

Two independently published descendant StoneAge client-source trees read and write runtime map cache files as:

`map\\%d.dat`

The client-side layout is explicitly:

1. `uint32 width`
2. `uint32 height`
3. `uint16 tile[width*height]`
4. `uint16 parts[width*height]`
5. `uint16 event[width*height]`

Relevant descendant source anchors:

- `BismarckDD/stoneage` commit `999ffdf1d220ec6666eb65339180689c9caf1876`
  - `client/stoneage/system/map.cpp`
- `Signally190/sking-sacli` commit `40cb67ef090ebc0cffd57ca947871bdfd0b18331`
  - `system/map.cpp`

The inspected client source does not establish the recovered single-layer `.MAP` files as the official runtime map cache.

## External SACH context

Later/community sources explicitly identify **SACH** as a StoneAge external automation/helper tool. A preserved 2.5 single-player setup guide instructs users to open `SACH-MX0.30/STW0.30.exe`, activate StoneAge, and point it at `stoneage2.5/sa_2903.exe`.

Useful public context:

- https://www.iopq.net/thread-16731619-1-1.html
- https://www.sohu.com/a/400016818_120099886
- https://lab.welovesa.com/forumdisplay.php?fid=40

These are community/later sources, not operator documentation. The decisive project evidence is the internal hash coupling plus descendant client source behavior.

## Corrected classification

### `.DAT`

**C / DESCENDANT-SOURCE-CORROBORATED CLIENT RUNTIME FORMAT**

The recovered `.DAT` family matches the three-layer runtime-cache format present in descendant StoneAge client source.

This does not prove each recovered DAT payload is untouched/operator-original, but the format role is technically grounded.

### `.MAP`

**C / EXTERNAL-TOOL-COUPLED DATASET**

The recovered one-layer `.MAP` family must not currently be labeled an official StoneAge client map format.

Working interpretation:

- likely SACH / pathfinding / automation-support map data, or a derivative map representation used by that ecosystem;
- exact cell meaning remains useful to study later as part of historical automation/tooling archaeology;
- it is not part of the clean-client baseline unless independent operator/client evidence later proves otherwise.

## Research consequence

The main reverse-engineering path changes from “decode the single-layer MAP as the client map format” to:

1. use recovered `.DAT` files plus descendant source to reconstruct the client runtime map cache;
2. trace `tile`, `parts`, and `event` through rendering, collision, movement and network-update code;
3. cross-check those semantics against recovered bytes;
4. keep SACH `.MAP` data in a separate automation/tooling track.

This correction also aligns with DD-010: third-party automation is historically important design evidence, but it remains technically separate from the clean official client during archaeology.
