# Taiwan Wayi 8.5 map payload structure — R1

Date: 2026-10-25 (Asia/Shanghai)

This package restores usable binary map-structure metadata from a real preserved client payload. It does not certify complete world maps or named places.

## Source and bounded carrier stop

Fresh remote startup: main `92b605e4a0d612a7d3a7633dab1137c800d2d856`, tree `dd0fdbe998ac697117cd9a788d92519079f42b4b`; 568 branch refs, 0 open PRs, 0 running workflows, 18 same-HEAD success runs. All eight startup files were read from the exact checkout, with full original bytes pinned. CURRENT was 2,637,603 bytes; the empty file-interface response was not interpreted as an empty file. No AGENTS.md exists in the recursive remote tree.

The preceding highest-priority carrier package received one bounded search unit across Japanese retail/public dumps, the Korean GameTime guide CD and Inium-era mirrors. No new qualified downloadable game payload was found. The already known YES24 catalog still describes the guide and included installation/demo CD; it is not a binary download or new source. Search snippets and the web-extracted product page have no newly acquired source HTML digest. No claim of global absence, holder contact, physical purchase or a complete archive census is made. Per the latest CURRENT stop condition, work rotated to available client map bytes.

The existing six-part community-preserved carrier was genuinely reacquired in source run [40131518031](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40131518031), job 120984031027, source commit `86a1f9fd0ee10c5e53ec085cd3227fbb54f83d2f`. All six downloads were new in that runner, with exact old size/SHA agreement. The 1,145,465,184-byte wrapper and statically decoded MSI match the previously accepted hashes. msitools extracted the 557-file MSI payload; no original installer/game was executed. This is not a newly discovered release and independent original pressing authentication remains OPEN.

## Actual content result

All **42/42** numeric map DAT files, totaling **14,445,606 bytes**, match the previously accepted complete MSI inventory and the exact `8 + width × height × 6` layout. There are 21 distinct dimension pairs and 2,407,545 allocated cells across files. Each file has three ordinal little-endian uint16 planes. The first/second/third planes contain respectively **120,250 / 24,569 / 134,868 nonzero cells**. Zero is a literal decoded value, not an automatically identified unexplored or impassable cell.

For example, map/200.dat declares 800×1200 but its first plane has only 3,581 nonzero values; map/61000.dat and map/61100.dat have entirely zero second planes. **HYPOTHESIS:** some files may represent partial/sparse cache states. The observation does not prove the cause, missing-area percentage, runtime exploration state or walkability. Declared dimensions therefore cannot certify complete world-map recovery.

The compatible old tile/parts/event interpretation is deliberately not promoted to demonstrated runtime semantics for this preserved TW8.5 build. Numeric filename tokens do not authenticate floor IDs, names, teleports, NPCs, encounters or quest conditions.

Existing mixed-2.5 whole-file relationships are retained: 34 same-path byte differences, seven paths absent from that mixed corpus, one exact control (map/40.dat). These are old inventory joins, not newly discovered geography or a chronological patch diff. A later finite actual-plane comparison must determine which ordinal layers differ before any geometry-change claim.

| File token | Dimensions | Plane 1 nonzero | Plane 2 nonzero | Plane 3 nonzero |
|---|---:|---:|---:|---:|
| 100 | 800×800 | 56956 | 3645 | 56956 |
| 1000 | 160×160 | 11143 | 1741 | 11143 |
| 1001 | 30×30 | 107 | 673 | 728 |
| 1003 | 30×30 | 107 | 771 | 840 |
| 1005 | 30×30 | 182 | 733 | 840 |
| 1006 | 30×40 | 209 | 1059 | 1184 |
| 1009 | 40×60 | 601 | 216 | 1340 |
| 1040 | 80×80 | 756 | 186 | 756 |
| 10920 | 100×100 | 1066 | 222 | 1066 |
| 110 | 46×45 | 1256 | 801 | 1848 |
| 1214 | 50×50 | 380 | 148 | 380 |
| 1215 | 25×25 | 625 | 147 | 625 |
| 122 | 300×200 | 3822 | 54 | 3822 |
| 130 | 60×60 | 3530 | 743 | 3598 |
| 141 | 50×50 | 1510 | 147 | 1510 |
| 200 | 800×1200 | 3581 | 519 | 3581 |
| 2000 | 150×150 | 2348 | 353 | 2348 |
| 2006 | 40×30 | 222 | 609 | 756 |
| 2012 | 30×30 | 118 | 828 | 896 |
| 21201 | 120×120 | 729 | 75 | 729 |
| 21308 | 40×40 | 1234 | 168 | 1234 |
| 3000 | 150×150 | 4326 | 716 | 4392 |
| 3004 | 30×30 | 115 | 616 | 672 |
| 3006 | 40×30 | 239 | 576 | 729 |
| 3020 | 25×25 | 162 | 538 | 625 |
| 30691 | 100×100 | 4113 | 1263 | 7555 |
| 32020 | 100×100 | 5811 | 372 | 5811 |
| 3400 | 120×120 | 1662 | 342 | 1662 |
| 40 | 20×20 | 400 | 146 | 400 |
| 4000 | 150×150 | 4678 | 1467 | 4678 |
| 4006 | 30×40 | 209 | 692 | 812 |
| 4020 | 25×25 | 162 | 461 | 550 |
| 5103 | 30×30 | 645 | 292 | 648 |
| 61000 | 400×400 | 1458 | 0 | 1458 |
| 61100 | 600×600 | 2187 | 0 | 2187 |
| 7400 | 160×160 | 729 | 149 | 729 |
| 7405 | 30×30 | 204 | 65 | 676 |
| 7503 | 30×30 | 286 | 364 | 596 |
| 805 | 50×50 | 474 | 928 | 1327 |
| 806 | 50×50 | 474 | 1348 | 1747 |
| 8216 | 40×40 | 448 | 26 | 448 |
| 9000 | 90×90 | 986 | 370 | 986 |

The three two-byte bgm0/bgm1/bgm2 DAT files are explicitly excluded from map counts. No cell grid, original pixels, audio or executable payload is published.

## Verification and durable evidence

The source job passed four parser/inventory tests and actual extraction of all 42 files. Local adjacent acquisition/inventory tests total 22. The downloaded artifact ZIP is independently checked at 86,498 bytes and SHA256 `b1254d6db8e581bd69db093455ce587c9d40ccb091885c05cda5c06a009be450`, matching the Actions API. Exactly two JSON members were unpacked. The map report is 149,924 bytes, SHA256 `aacac89c451305c59adf38cfc6c14ba8a2efb88705607206aee7f63a8e14ead5`; its complete metadata is committed. The accompanying 385,776-byte acquisition manifest is temporary artifact content, with its hash retained in the permanent receipt; it is not claimed to be fully archived in Git.

The offline archive guard checks inventory identity, ordinal order, dimension/byte arithmetic, frequency/zero-count consistency, preserved cross-version joins, explicit negative boundaries and four full historical prefixes. Nine semantic mutations bypassing the report digest are rejected. This is independent metadata acceptance, not a second source-byte execution. Candidate and main Actions are recorded only after observed completion.

Reproduce the archive guard with `python -m tools.stoneage_tw85_map_archive`. Source acquisition is isolated in `.github/workflows/recover-stoneage-tw85-map-payload.yml`; main source execution reacquires bytes rather than treating this metadata as the original binary.

## Next finite material result

**CLIENT-MAP-CROSS-VERSION-PLANE-DIFF-04:** compare the same 35 paths against the genuinely acquired mixed-2.5 corpus, with both input hashes pinned, and separate first/second/third-plane equality from whole-file differences. Retain its mixed/unverified-server provenance. Stop at a content-changing finite comparison or precise acquisition gap; do not repeat package inventories or infer early named places. JSS/Korean carrier recovery reopens only on a concrete new public byte source.

Stage A remains seven PARTIAL/two OPEN; Stage B/wiki production gated; savedata R79 paused; overall restoration percentage null. DD-028 task origin categories remain separate. Original server NPC/quest/pet-growth tables and durable original-package storage remain OPEN.
