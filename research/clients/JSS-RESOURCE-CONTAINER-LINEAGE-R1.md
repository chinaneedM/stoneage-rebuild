# JSS Resource Container Lineage — R1

Date: 2026-09-18

Purpose: record a controlled technical-lineage hypothesis connecting the resource-container naming seen in preserved LIFESTORM II material with the REAL/ADRN resource system preserved in later StoneAge client-source lineages.

This document is **not** proof that LIFESTORM II and the 1999 StoneAge retail client used an identical engine or byte format. It defines what is actually observed and a reproducible way to confirm or falsify the relationship if freely accessible historical bytes become available.

## 1. Evidence classes used here

- **C / COMMUNITY PRESERVATION LEAD** — later community material preserving filenames or technical descriptions.
- **C / DESCENDANT SOURCE LINEAGE** — later public StoneAge source trees with no authenticated Git history back to 1999 JSS.
- **HYPOTHESIS** — a possible shared JSS-era resource pipeline suggested by the evidence.
- Promotion to JSS-era FACT requires period first-party source, authenticated original media/client bytes, or equivalent provenance.

## 2. LIFESTORM II preservation lead

Community preservation thread:

https://forum.omega.idv.tw/viewthread.php?page=1&threadid=4432

Mirror/current route:

https://omega.idv.tw/kdb120/viewthread.php?threadid=4432

The thread was posted in 2013 and explicitly says the material came from an older 2007 backup. It is not a contemporaneous 1999 source.

The relevant post says the backup contained LIFESTORM II `data` and `map` material and names:

- `adrn_1.bin` — described by the poster as the **image address file**;
- `real_1.bin` — described as the **image data file**;
- map `.dat` files.

The poster reports opening the map files with a StoneAge tool, `SAForever 石器時代地圖編輯器`. The maps could be displayed, but the LIFESTORM II `adrn_1.bin` and `real_1.bin` did not line up correctly with that StoneAge tool, so the displayed graphics were wrong.

Two old ASUS WebStorage links are preserved in the thread, including one for the 2007 `ls2 data` / map backup. They are free/public preservation targets, not acquisition targets. The current environment cannot resolve/retrieve the ASUS WebStorage host, so no bytes have been inspected in this pass.

### Evidentiary meaning

The thread supports, at C-grade only, that a preserved Taiwan-version LIFESTORM II data set used a paired `ADRN / REAL` filename convention whose community-described roles match an address/index file plus image-data file.

It does **not** yet establish:

- that the Japanese February 1999 retail build used the same filenames;
- the binary record layout of LIFESTORM II ADRN;
- the compression format inside LIFESTORM II REAL;
- compatibility with StoneAge's decoder;
- direct code reuse between LIFESTORM II and StoneAge.

The reported failure to align the files in a StoneAge map editor is important negative evidence: even if the two games share ancestry, their index schema, numbering, map binding, resource revision, or tool expectations may differ.

## 3. StoneAge descendant REAL/ADRN architecture

### Lineage A — BismarckDD/stoneage

Observed anchor:

`999ffdf1d220ec6666eb65339180689c9caf1876`

Relevant paths:

- `client/stoneage/game/main.cpp`
- `client/stoneage/systeminc/loadrealbin.h`
- `client/stoneage/system/loadrealbin.cpp`
- `client/stoneage/systeminc/unpack.h`
- `client/stoneage/system/unpack.cpp`

This branch currently defaults to versioned resource names:

- `data/real_136.bin`
- `data/adrn_136.bin`
- `data/spr_115.bin`
- `data/spradrn_115.bin`

Its command-line parser can also select `data/real_%d.bin` and `data/adrn_%d.bin`.

### Lineage B — Signally190/sking-sacli

Observed anchor:

`40cb67ef090ebc0cffd57ca947871bdfd0b18331`

Relevant paths:

- `system/main.cpp`
- `systeminc/loadrealbin.h`
- `system/loadrealbin.cpp`
- `systeminc/unpack.h`
- `system/unpack.cpp`

This branch contains the unnumbered defaults:

- `data\\real.bin`
- `data\\adrn.bin`
- `data\\spr.bin`
- `data\\spradrn.bin`

### Independence limit

These are separately published repositories, but they clearly descend from a circulated StoneAge source lineage. Their agreement is useful for reconstructing the **persistent StoneAge format implementation**, not two independent proofs of a 1999 JSS source tree.

Other public StoneAge forks/mobile ports preserve the same structures and decoder, reinforcing code-lineage persistence but not adding independent historical provenance.

## 4. StoneAge ADRN record semantics

Both source trees preserve essentially the same `ADRNBIN` structure. The key fields are:

- `bitmapno`
- `adder`
- `size`
- `xoffset`
- `yoffset`
- `width`
- `height`
- nested `MAP_ATTR`

The nested attribute record includes collision/hit information, height, status/damage-related fields, sound-effect fields, and `bmpnumber`.

The common `initRealbinFileOpen` implementation:

1. opens the ADRN file;
2. opens the REAL file;
3. reads ADRN as sequential fixed-size `ADRNBIN` records;
4. indexes each record by `bitmapno`;
5. creates a reverse/lookup mapping from `bmpnumber` to `bitmapno`.

The common `realGetImage` implementation then:

1. selects one ADRN record;
2. seeks the REAL file to `adrdata.adder`;
3. reads exactly `adrdata.size` bytes;
4. passes that resource block to `decoder()`.

Therefore, inside this StoneAge lineage, the roles are unambiguous:

- **ADRN = address/metadata/index records**
- **REAL = encoded image blocks**

This is notably consistent with the terminology used by the LIFESTORM II preservation post, but terminology alone is not byte-format proof.

## 5. StoneAge image-block signature

The preserved `RD_HEADER` is:

- two-byte identifier `id[2]`;
- `compressFlag`;
- `width`;
- `height`;
- `size`.

The decoder rejects a block unless:

- `id[0] == 'R'`
- `id[1] == 'D'`

This yields a concrete resource-block signature: **`RD`**.

### Custom compression mode

The common encoder/decoder defines:

- `BIT_CMP = 0x80`
- `BIT_ZERO = 0x40`
- `BIT_REP_LARG = 0x10`
- `BIT_REP_LARG2 = 0x20`

For the legacy compressed mode, the byte stream alternates literal runs and repeated-byte runs. Zero runs receive a dedicated flag. Run lengths can be extended across additional bytes.

This is accurately described as a custom **RLE-style / run-length-plus-literal codec**.

Do not label every later decoder branch as original JSS behavior: the same files also contain later conditional extensions such as zlib-backed high-color modes under feature macros. Those additions must be dated independently.

## 6. Independent later community recollection of the codec

A 2006 StoneAge player/developer blog post reports seeing:

- `real_136.bin`
- `adrn_136.bin`

in a then-current StoneAge client and asks rhetorically whether it was “still using JSS's RLE compression algorithm,” then says the author's own image viewer could extract images.

Source:

https://nekotoba.nfshost.com/b/2006/03/370/

Classification: **C / later technical community recollection**.

This does not prove the algorithm's 1999 origin, but it is useful because it predates the modern GitHub imports and shows that the REAL/ADRN + “JSS RLE” association existed in the StoneAge technical community by 2006.

## 7. Controlled cross-game hypothesis

### HYPOTHESIS

LIFESTORM II and StoneAge may share an ancestral JSS image-resource pipeline characterized by a paired address/index file and image-data file convention:

`ADRN + REAL`

Possible relationships, from weakest to strongest:

1. **naming convention only** — same filenames/roles, different byte formats;
2. **shared container concept** — ADRN indexes REAL in both, but record layouts/codecs differ;
3. **shared image-block codec** — both contain compatible `RD` blocks / RLE-style encoding, while indexing differs;
4. **shared resource implementation ancestry** — compatible ADRN records plus compatible REAL blocks;
5. **larger engine/code reuse** — requires much more evidence and must not be inferred merely from resource compatibility.

The current evidence establishes none of levels 2–5 as fact.

## 8. Why the mismatch reported by the LIFESTORM II preservation thread matters

The StoneAge editor reportedly displayed the LIFESTORM II maps but failed to associate `adrn_1.bin` / `real_1.bin` correctly.

That observation is compatible with several competing explanations:

- the LIFESTORM II ADRN structure differs;
- image numbering differs;
- the map format refers to graphics differently;
- the Taiwan version changed the resource layout;
- the preserved files are from different revisions;
- the StoneAge tool assumes later StoneAge patch-number conventions;
- the REAL codec itself may still be compatible even if ADRN/map linkage is not.

Therefore the correct next test is byte-level and layered, not an all-or-nothing “same engine” claim.

## 9. Reproducible free-data validation plan

If the old LIFESTORM II backup, another freely shared historical copy, or equivalent public bytes become retrievable:

1. keep the original files outside this repository;
2. record SHA-256/SHA-1/MD5, byte size, filename, archive provenance and retrieval date;
3. inspect `adrn_1.bin` length and raw record regularity without assuming StoneAge's record width;
4. scan `real_1.bin` for plausible `RD` block headers;
5. validate candidate headers using plausible width/height/size bounds;
6. attempt the StoneAge legacy decoder on isolated candidate blocks in a read-only/offline analysis harness;
7. separately test whether LIFESTORM II ADRN fields can resolve offsets/sizes into those blocks;
8. compare map references only after image-container behavior is understood;
9. record negative results as evidence — incompatibility can date the divergence;
10. do not commit proprietary media/data; commit only hashes, metadata, parsers/specifications independently written for research, and derived findings where appropriate.

## 10. Promotion criteria

Promote the shared-resource-pipeline hypothesis only if free/public historical bytes show at least one of:

- LIFESTORM II REAL blocks carry the same `RD` header and decode correctly with the StoneAge legacy codec;
- LIFESTORM II ADRN records demonstrably expose equivalent offset/size/image-index semantics;
- period JSS documentation/source explicitly connects the formats;
- an authenticated original JSS-era tool/source supports both products.

Until then, the proper label remains:

**HYPOTHESIS / HIGH-VALUE TECHNICAL LINEAGE LEAD.**
