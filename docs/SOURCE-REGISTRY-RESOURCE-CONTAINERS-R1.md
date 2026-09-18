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

## Source-group conclusion

The StoneAge side now has a stable descendant-code specification for the REAL/ADRN resource architecture and its legacy `RD` run-length/literal decoder.

The LIFESTORM II side currently supplies matching filename roles from a later Taiwan-version preservation record, but no inspected bytes.

Therefore the shared JSS resource-pipeline theory remains **HYPOTHESIS / high-value technical lineage lead**, with a concrete free-data validation plan documented in:

`research/clients/JSS-RESOURCE-CONTAINER-LINEAGE-R1.md`
