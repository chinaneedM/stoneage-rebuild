# Source Registry Supplement — Resource Container Lineage R1

Date: 2026-09-18

Purpose: register lower-confidence preservation/source-lineage material used to test a possible LIFESTORM II → StoneAge JSS resource-container ancestry.

## SRC-LS2-OMEGA-DATA-PRESERVATION-01

- title: `〖推薦〗樂園;lifestorm2;ライフストーム ２ 素材收集帖`
- thread date: 2013; relevant post says files came from a 2007 backup
- URLs:
  - https://forum.omega.idv.tw/viewthread.php?page=1&threadid=4432
  - https://omega.idv.tw/kdb120/viewthread.php?threadid=4432
- retrieval date: 2026-09-18
- source type: later community preservation / technical note
- confidence: **C**
- supports as later preservation testimony:
  - existence in the preserved LIFESTORM II data set of `adrn_1.bin` and `real_1.bin`;
  - poster's description of ADRN as image-address data and REAL as image-data;
  - map `.dat` files were also present;
  - a StoneAge `SAForever` map editor could display the maps but did not correctly align the LIFESTORM II ADRN/REAL graphics;
  - old ASUS WebStorage public-download targets were published for the backup.
- current limitation:
  - ASUS WebStorage is not reachable/resolvable from the present analysis environment, so the historical bytes have not been retrieved or inspected.
- does not establish:
  - Japanese 1999 retail filenames;
  - binary format compatibility;
  - direct engine reuse;
  - JSS authorship of any later community tool.

## SRC-SA-DESC-REALADRN-BISMARCK-01

- repository: https://github.com/BismarckDD/stoneage
- observed commit: `999ffdf1d220ec6666eb65339180689c9caf1876`
- source type: later community-preserved StoneAge source lineage
- confidence: **C / LINEAGE**
- relevant paths:
  - `client/stoneage/game/main.cpp`
  - `client/stoneage/systeminc/loadrealbin.h`
  - `client/stoneage/system/loadrealbin.cpp`
  - `client/stoneage/systeminc/unpack.h`
  - `client/stoneage/system/unpack.cpp`
- supports within this descendant lineage:
  - versioned `real_136.bin / adrn_136.bin` and `spr_115.bin / spradrn_115.bin`;
  - runtime support for `real_%d.bin / adrn_%d.bin`;
  - ADRN fixed-record indexing with `bitmapno / adder / size / offsets / dimensions / attributes`;
  - REAL block retrieval by ADRN offset+size;
  - `RD` block identifier;
  - custom run-length/literal codec using `BIT_CMP 0x80`, `BIT_ZERO 0x40`, `BIT_REP_LARG 0x10`, `BIT_REP_LARG2 0x20`.
- does not establish the exact 1999 JSS retail format by itself.

## SRC-SA-DESC-REALADRN-SIGNALLY-01

- repository: https://github.com/Signally190/sking-sacli
- observed commit: `40cb67ef090ebc0cffd57ca947871bdfd0b18331`
- source type: later community-preserved StoneAge source lineage
- confidence: **C / LINEAGE**
- relevant paths:
  - `system/main.cpp`
  - `systeminc/loadrealbin.h`
  - `system/loadrealbin.cpp`
  - `systeminc/unpack.h`
  - `system/unpack.cpp`
- supports within this descendant lineage:
  - unnumbered `real.bin / adrn.bin / spr.bin / spradrn.bin`;
  - the same ADRN index structure and REAL offset+size retrieval architecture;
  - the same `RD` header definition;
  - essentially the same legacy run-length/literal decoder.
- independence warning:
  - agreement with other public StoneAge trees is code-lineage persistence, not independent historical provenance.

## SRC-SA-2022-ZENHAX-ADRN-SAMPLE-01

- title: `An old game StoneAge (.bin)`
- original discussion date: 2022-07
- URLs:
  - https://zenhax.com/viewtopic.php%40t%3D17201.html
  - https://reshax.com/topic/10614-an-old-game-stoneage-bin/
- retrieval date: 2026-09-18
- source type: public sample discussion / independent reverse engineering
- confidence: **C**
- supports:
  - the shared sample contained `adrn.bin / real.bin / spr.bin / spradrn.bin`;
  - reverse-engineering response identifies ADRN as an index for REAL;
  - reported ADRN record width is **80 bytes**;
  - reported first fields are file/image number, REAL offset and file length.
- cross-check:
  - the public descendant source `ADRNBIN` + `MAP_ATTR` layout also totals 80 bytes under the intended Win32 32-bit structure layout, independently matching the reported sample record width.
- caution:
  - the forum pseudo-structure's later unknown/padding field listing does not numerically reconcile with its stated 80-byte total; only the mutually consistent record-size and leading-field claims are retained.
- does not establish:
  - JSS-1999 provenance of the shared sample;
  - LIFESTORM II compatibility;
  - exact meaning of every 80-byte field.

## SRC-SA-2006-JSS-RLE-BLOG-01

- title: `一遇到跑过来的长毛象公车.人物会变成怎样?`
- date: 2006-03
- URL: https://nekotoba.nfshost.com/b/2006/03/370/
- source type: later player/developer technical blog
- confidence: **C**
- supports as a dated later technical recollection:
  - author observed `real_136.bin` and `adrn_136.bin` in a StoneAge client;
  - author associated them with what they called JSS's RLE compression algorithm;
  - author said a self-made image viewer extracted images.
- does not establish:
  - source-code provenance;
  - exact 1999 algorithm;
  - LIFESTORM II compatibility.


## SRC-CG-SA-FANICER-FORMAT-LINEAGE-01

- original lineage: `http://www.fanicer.com/gallery/FileFmt.htm`
- surviving mirrors:
  - https://cgsword.com/fanicer.htm
  - https://omega.idv.tw/kdb120/viewthread.php?page=1&threadid=4437
- credited original author: 梦见草
- credited editor/organizer: 野風信子
- retrieval date: 2026-09-18
- source type: later preservation of older technical reverse-engineering article
- confidence: **C**
- supports:
  - CrossGate `GraphicInfo` vs StoneAge `Adrn` index naming;
  - 40-byte CrossGate vs 80-byte StoneAge image-index records;
  - CrossGate `Graphic` vs StoneAge `Real` image-data naming;
  - 16-byte `RD` image block header;
  - nine-class Run-Length control-byte scheme;
  - article's attribution of the codec as JSS-defined and used in both titles;
  - client-map distinction: CrossGate client map has a 12-byte `MAP` header while StoneAge client map is described as lacking that header.
- limitation:
  - not contemporaneous first-party JSS documentation;
  - “same original team” and JSS-authorship statements remain later technical-community testimony unless independently promoted.

## SRC-CG-CGTOOL-RD-CODEC-01

- repository: https://github.com/HonorLee-cn/CGTool
- observed commit: `b4d08112524aa16b9fdb416ef865f8c196ffac20`
- relevant path: `CrossgateToolkit/GraphicData.cs`
- source type: modern CrossGate parser implementation
- confidence: **C / FORMAT CORROBORATION**
- supports:
  - 16-byte CrossGate `RD` header;
  - version byte + unknown byte + width + height + data length;
  - literal/repeat/zero Run-Length families matching the older format article.
- limitation: modern implementation, not JSS source.

## SRC-CG-XGTOOL-RD-CODEC-01

- repository: https://github.com/x-gate/xgtool
- observed commit: `a5176dbf107f2f1567951476f652391b76f7f702`
- relevant paths:
  - `internal/codec.go`
  - `docs/formats/codec.md`
- source type: modern CrossGate codec implementation
- confidence: **C / FORMAT CORROBORATION**
- supports:
  - literal control groups `00/10/20`;
  - repeated-byte groups `80/90/A0`;
  - repeated-zero groups `C0/D0/E0`;
  - 4/12/20-bit run lengths.

## SRC-CG-KACORO-RD-CODEC-01

- repository: https://github.com/kacoro/crossgate-tools
- observed commit: `050480c0bf879a460cccd040358ed6c201e0f638`
- relevant path: `src/Utils/cgCoder.ts`
- source type: modern CrossGate codec implementation
- confidence: **C / FORMAT CORROBORATION**
- supports the same nine-class RLE scheme and labels it a JSS-defined Run-Length algorithm.

## SRC-SA-CG-LS2MAP-SERVER-LINEAGE-01

- StoneAge descendant:
  - repository: https://github.com/BismarckDD/stoneage
  - commit: `999ffdf1d220ec6666eb65339180689c9caf1876`
  - path: `server/gmsv/map/readmap.c`
- CrossGate reconstruction:
  - repository: https://github.com/esxgx/xgate
  - path: `readmap_SA.c`
  - README identifies project as `魔力宝贝复刻版`
- CrossGate data tooling:
  - repository: https://github.com/zhanxj/CrossGateData
  - paths: `src/cg/data/map/MapInfo.java`, `src/cg/data/gmsvReader/CMapReader.java`
- source type: later source/tooling lineage
- confidence: **C / SERVER-FORMAT LINEAGE**
- supports:
  - literal server-map magic `LS2MAP` across StoneAge server descendants and CrossGate reconstruction/tooling;
  - common basic server-map header/layer structure.
- crucial non-establishment:
  - does not establish that `LS2` means LIFESTORM II;
  - does not establish original client-map magic;
  - does not establish first introduction date or title.



## SRC-SA-25-RECOVERED-RESOURCE-CORPUS-01

- recovered bundle SHA-256: `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`
- source lineage: preserved We Love SA / MediaFire two-part StoneAge 2.5 bundle; payload kept outside repository
- source type: recovered public preservation bytes / derived validation
- confidence: **A for literal format properties of this recovered corpus; provenance does not make the runtime a clean operator baseline**
- derived reports:
  - `research/recovered/STONEAGE-25-PRESERVED-BUNDLE-STATIC-INVENTORY-R1.txt`
  - `research/recovered/STONEAGE-25-RESOURCE-PROBE-R1.txt`
  - `research/recovered/STONEAGE-25-RD-DECODE-VALIDATION-R1.txt`
  - `research/recovered/STONEAGE-25-MAP-DAT-RELATION-R1.txt`
- supports directly:
  - 80-byte ADRN record width across 234,564 records;
  - complete ADRN partitioning of REAL into contiguous `RD` blocks;
  - flag-0 and flag-1 legacy RD behavior;
  - 4,225 / 4,225 successful real-block decodes with the independently implemented decoder;
  - 1,030 single-layer `.MAP` files using 8-byte dimensions + uint16 cells;
  - distinct three-layer `.DAT` runtime/cache family;
  - negative result that `.MAP` is not byte-identical to tile, parts or event in any of 995 valid paired files.
- does not establish:
  - 1999 JSS byte identity;
  - purity of the recovered runtime executable layer;
  - semantic meaning of the `.MAP` uint16 cell values;
  - LIFESTORM II binary compatibility.

## Source-group conclusion

The StoneAge side now has both a stable descendant-code specification **and direct recovered-2.5 byte validation** for the REAL/ADRN resource architecture and its legacy `RD` run-length/literal decoder.

The LIFESTORM II side currently supplies matching filename roles from a later Taiwan-version preservation record, but no inspected bytes.

Therefore the shared JSS resource-pipeline theory remains **HYPOTHESIS / high-value technical lineage lead**, with a concrete free-data validation plan documented in:

`research/clients/JSS-RESOURCE-CONTAINER-LINEAGE-R1.md`
