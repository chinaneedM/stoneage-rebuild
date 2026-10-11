# Taiwan StoneAge 8.0 vs 8.5: contemporary launch, expansion, and schedule chronology gate R1

**Date:** 2026-10-11. Research scope: historical game version lineage and authenticated digital client intake. **No original executable bytes acquired in this round.**

## 1. Three different evidentiary events must not collapse into one

**2005-06-08 — original Taiwan 8.0 feature announcement.** Contemporary 巴哈姆特 GNN published the day-of-release account, https://gnn.gamer.com.tw/detail.php?sn=20167. It reports the 8.0 Lost World update was online and offered a new PET equipment subsystem together with ice maps and related features. This is affirmative *contemporaneous reporting about the official feature*, not byte-verified proof of which compiled original executable/source, and does not establish any default-on `_PET_ITEM` in the unrelated pinned Bismarck later descendant.

**2005-07-07 — independent period player feature account.** https://www.gamez.com.tw/t/8-0/170704 reports PET equipment varieties, attributes and combinations, about one month after the initial rollout. It is a player post/repost and does not authenticate any quoted recipe against a specific native client or original server. It supports separating the later publicity from *feature presence* in the June/July era.

**2005-09-08 — later marketing / item expansion, NOT the first PET system launch.** The 2005-09-08 GNN news *index excerpt* at https://acg.gamer.com.tw/search.php?c1=976&c2=3&machine=1%2C0&s=2&type=1 describes a miniature pig spokesperson and enhanced `無敵來吉卡` promotion, **with at least 20 additional pet/profession equipment rewards planned**. A later chronicle faithfully repeats a headline emphasizing new pet equipment, e.g. https://forum.gamer.com.tw/G2.php?bsn=1571&sn=4345 . That headline alone is not evidence that the entire PET equipment feature debuted in September; June release and July player account precede it. The original full September news page was not independently retrieved, so retain *index-excerpt* confidence for the precise planned item count and keep whether/when each promised item actually appeared OPEN.

## 2. 2006 Taiwan 8.5 official release was staged; June 16 is only a filename token

A **second contemporary GNN article** published 2006-06-21, https://gnn.gamer.com.tw/detail.php?sn=23856, reports the operator's **announced** V8.5 魔域大冒險 staged schedule:

| Date | Historical claim | Evidence status |
| --- | --- | --- |
| 2006-06-21 to 2006-07-05 | Public test server window announced | Report of official schedule, not native binary verification |
| 2006-07-05 | 蒼龍 first production server **planned** upgrade | Scheduled, not observed verified completed |
| From 2006-07-12 | Other servers **planned** full rollout | Scheduled, not observed verified completed |

Independent contemporaneous game-media publication https://www.games.idv.tw/news.php?mode=view&nid=615 repeats the announced test/rollout staging, consistent with GNN, but does not provide binary bytes.

The earlier recorded Taiwanese WAYI host filename `STONEAGE20060616.exe` is cited in 2006-08-13 and 2008-02-16 forum posts and appears in a community six-part mirror from 2012. Its `20060616` component predates **the announced June 21 8.5 public test** and later production upgrade dates. Do not treat the filename as proof that a production 8.5 installer existed/released June 16: file naming may encode packaging, an earlier prepared distribution, or something else, **all unknown**. This date relation also does NOT prove that the file is not 8.5; only a provenance-preserved executable metadata scan could resolve the binary identity. The community file SHA and operator-original equivalence are not yet verified.

## 3. Explicit original-client admission status

| Needed item | Status |
| --- | --- |
| Independently downloadable, byte-verified publisher-issued Taiwan 2005 8.0 original installer/patch | **OPEN** |
| Confirmed original update sequence with file-level receipts and unpatched installed snapshots | **OPEN** |
| Exact operator original 8.5 `STONEAGE20060616.exe` and six-part mirror SHA equality | **OPEN** |
| Actual enabled paired PET client and server, live opcode127 and owner/unique-code transfer/persistence | **OPEN** |
| Evidence 8.0 PET belongs in JSS1999 or Taiwan 1.0 | **NO** |

The nearest prior client leads remain disjoint: Mainland China `cdl.wayi.com.cn/sa8_8016.rar` (community-linked, region distinct, original bytes not verified), Taiwanese 8.5 `STONEAGE20060616.exe` (community split mirror unverified), and any later private-server `8.0` labeled repacks (modified package class, not clean historic operator client). Do not use a 2016 private server Google Drive installer as original 2005 byte proof without independent chain of custody; at most it is an alternate candidate for offline identification.

## 4. Reproducibility gate

`research/recovered/STONEAGE-TW80-TW85-PRESS-CHRONOLOGY-R1.json` is a source-specific machine-readable matrix. `tools/stoneage_tw80_tw85_chronology_gate.py` and 15 regression/mutation tests validate exact date, publisher/source URL, stage, region, 2006 rollout **scheduled** status and no-promotion flags.

A source document or press article's date never substitutes for source code release build flags or binary SHA256. A server's planned transition date never proves it actually ran that build. Nothing here amends an accepted original Taiwan v1.0/JSS build, authorizes the modern engine stage, or claims completion of the PET runtime gate.

No copyrighted original assets/executables imported. Historical pressure remains **2486 = 2465 bounded closed + 18 OPEN + 3 historical UB**.

**Next priority:** obtain an original, freely digitally downloadable Taiwan 2005 8.0 clean client or patch and independent publisher manifest/checksum, then use the previously accepted offline file fingerprint/snapshot tools. If no verifiable original bytes exist, keep the binary/runtime gate OPEN rather than treating dates, photos, marketing names or community executables as artifacts.
