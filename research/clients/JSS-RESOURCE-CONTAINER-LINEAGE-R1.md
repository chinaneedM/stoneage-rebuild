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

## 5A. Independent public-sample corroboration of ADRN record size

A 2022 ZenHAX thread preserved a freely shared StoneAge sample whose file set was:

- `adrn.bin`
- `real.bin`
- `spr.bin`
- `spradrn.bin`

Archived/current discussion routes:

- https://zenhax.com/viewtopic.php%40t%3D17201.html
- https://reshax.com/topic/10614-an-old-game-stoneage-bin/

A responder independently reverse-engineered the sample and reported:

- ADRN is an index for REAL;
- each ADRN entry is **80 bytes**;
- the first three 32-bit values are file/image number, REAL file offset, and file length.

Classification: **C / public sample reverse-engineering corroboration**.

### Why 80 bytes matters

The descendant StoneAge source definition independently predicts the same record width under the Win32 32-bit layout used by the client:

- `ADRNBIN` fixed fields before `MAP_ATTR`: 28 bytes;
- `MAP_ATTR`: 52 bytes after normal 32-bit alignment;
- total: **80 bytes**.

This is a useful cross-check because the 80-byte result comes from analysis of a public data sample rather than only from reading the source code.

### Precision limit

The pseudo-structure reproduced in the ZenHAX/ResHax post contains a padding-array description that does not arithmetically reconcile with its own stated 80-byte record size. Therefore this project uses only the parts that are mutually consistent with the sample description and descendant source:

- 80-byte record size;
- record starts with number / REAL offset / REAL length.

Do **not** copy the forum's entire unknown-field pseudo-structure as an authenticated layout.

A separate later StoneAge technical article also describes ADRN as 80-byte / 20-parameter image headers with the early fields corresponding to image ID, REAL address and block length. Multiple mirrors repeat that article, so they are treated as one derivative source lineage rather than independent corroboration.



## 5B. CrossGate client-resource corroboration

A later technical-format article preserved at multiple mirrors explicitly compares CrossGate and StoneAge client resources.

Primary surviving mirrors used in this pass:

- https://cgsword.com/fanicer.htm
- https://omega.idv.tw/kdb120/viewthread.php?page=1&threadid=4437

The mirror identifies the original as `http://www.fanicer.com/gallery/FileFmt.htm`, credits the original author as 梦见草 and says 野風信子整理和完善.

Classification: **C / later technical documentation preserved from an older article lineage**.

The article distinguishes:

- CrossGate image index: `GraphicInfo*_*.bin`, 40-byte records;
- StoneAge image index: `Adrn_*.bin`, 80-byte records;
- CrossGate image data: `Graphic*_*.bin`;
- StoneAge image data: `Real_*.bin`.

It describes both games' image blocks as having a 16-byte header beginning with magic `RD`, followed by a version/compression byte, one unknown byte, width, height and total block size.

The article explicitly calls the compression a **JSS-defined Run-Length algorithm used by StoneAge and CrossGate** and documents these control-byte families:

- literal: `0x0n / 0x1n / 0x2n`;
- repeated value: `0x8n / 0x9n / 0xAn`;
- repeated background/zero: `0xCn / 0xDn / 0xEn`.

This is later technical documentation, not first-party JSS source, but it independently matches the descendant StoneAge codec structure at a byte-semantic level.

### Modern CrossGate parser cross-check

Three modern CrossGate tool implementations were examined as implementation-level corroboration:

1. `HonorLee-cn/CGTool` at `b4d08112524aa16b9fdb416ef865f8c196ffac20`
   - `CrossgateToolkit/GraphicData.cs`
   - reads a 16-byte header: 2-byte `RD`, version byte, unknown byte, width, height, data length;
   - implements all nine legacy RLE control families.

2. `x-gate/xgtool` at `a5176dbf107f2f1567951476f652391b76f7f702`
   - `internal/codec.go`
   - `docs/formats/codec.md`
   - independently groups control bytes as literal `00/10/20`, repeated byte `80/90/A0`, repeated zero `C0/D0/E0`;
   - uses 4-bit, 12-bit and 20-bit length forms.

3. `kacoro/crossgate-tools` at `050480c0bf879a460cccd040358ed6c201e0f638`
   - `src/Utils/cgCoder.ts`
   - explicitly labels the implementation as a JSS-defined Run-Length algorithm;
   - implements the same nine control families.

These projects are not independent historical sources for JSS authorship, but they materially corroborate that real CrossGate data in the preservation/tooling ecosystem uses the same codec family described by the older technical article.

## 5C. RD header binary-layout correspondence

The StoneAge descendant `RD_HEADER` source definition contains:

- `id[2]`;
- one-byte `compressFlag`;
- `unsigned int width`;
- `unsigned int height`;
- `unsigned int size`.

Under the intended 32-bit MSVC default structure alignment, one padding byte falls after `compressFlag`, producing a 16-byte structure:

- offset 0–1: `RD`;
- offset 2: compression/version byte;
- offset 3: padding/unspecified byte;
- offset 4–7: width;
- offset 8–11: height;
- offset 12–15: size.

The CrossGate format article and modern CrossGate parsers explicitly represent byte 3 as an “unknown” byte, yielding the same observable 16-byte disk layout.

This is a strong format-family correspondence, but it still does not prove which title first introduced the layout.

## 5D. StoneAge descendant decoder asymmetry

The preserved StoneAge **encoder** supports the three intended literal-length classes:

- short literal via high nibble `0x0`;
- 12-bit literal via `0x1`;
- 20-bit literal via `0x2`.

However, the inspected descendant StoneAge `decoder()` literal branch tests the `0x10` extension but does not symmetrically test the `0x20` literal extension before falling back to the low nibble.

By contrast, the older CrossGate/StoneAge technical article and multiple modern CrossGate decoders handle `0x20` as the 20-bit literal-length form.

Research consequence:

- do not blindly treat every line of the circulated StoneAge source as the canonical historical codec specification;
- the intended legacy codec is better reconstructed from the **encoder + old format documentation + multiple working decoders**;
- the StoneAge decoder discrepancy should be retained as a possible later source-copy bug, branch-specific bug, or code path that rarely encountered very long literal runs.

No claim is made that the bug existed in the 1999 JSS executable.

## 6A. LS2MAP correction — server map format, not client-resource proof

A separate research branch found the literal magic:

`LS2MAP`

in later StoneAge and CrossGate-related code.

### StoneAge server lineage

`BismarckDD/stoneage`:

`server/gmsv/map/readmap.c`

defines:

`#define MAP_MAGIC "LS2MAP"`

and `MAP_IsMapFile` reads the first six bytes and requires that magic.

The server loader then reads:

- 2-byte map ID;
- 32-byte map display/name field;
- 2-byte X size;
- 2-byte Y size;
- tile layer;
- object layer.

### CrossGate preservation/tooling lineage

`esxgx/xgate` identifies itself in its README as a “魔力宝贝复刻版”.

Its `readmap_SA.c` explicitly comments:

“石器、魔力服务器地图档 魔数”

then defines:

`MAP_MAGIC "LS2MAP"`

and labels its detector as checking an `SA/CG` map file.

The same file documents the same basic 44-byte pre-layer layout.

`zhanxj/CrossGateData` also defines:

`SERVER_HEAD = "LS2MAP"`

in `MapInfo.java`, and its `gmsvReader/CMapReader.java` explicitly reads files under `server/map`.

### Critical distinction from client maps

The older CrossGate/StoneAge file-format article describes **client map files** differently:

- CrossGate client maps: a 12-byte header beginning with `MAP` followed by zero bytes;
- StoneAge client maps: no such header;
- the subsequent map content is described as otherwise closely related.

Therefore:

**Do not conflate the later/private-server `LS2MAP` format with the original client map format.**

In particular, the existence of the string `LS2MAP` does **not** by itself prove:

- that LIFESTORM II used that header;
- that `LS2` expands to “LIFESTORM II”;
- that the 1999 StoneAge retail client's own map files began with `LS2MAP`;
- that CrossGate's official JSS client used `LS2MAP` client files.

The expansion/origin of the literal name `LS2MAP` remains **OPEN**.

The valid conclusion is narrower:

**C / later server-format lineage:** StoneAge server descendants and CrossGate reconstruction/data tooling share a server-map format identified by the magic `LS2MAP`.


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
