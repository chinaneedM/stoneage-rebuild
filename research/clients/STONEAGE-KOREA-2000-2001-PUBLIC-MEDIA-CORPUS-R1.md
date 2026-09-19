# StoneAge Korea 2000–2001 Public-Media Recovery Corpus R1

Date: 2026-09-19

## Purpose

This record captures the reproducible public-media search layer used to look for an early Korean StoneAge client without downloading complete carrier images into the repository.

The objective is narrow: determine whether surviving public Korean magazine/software-disc images or archive-directory metadata preserve StoneAge client filenames, directories, installer objects, or download records relevant to the 2000–2001 Inium/Hananet/CNET/GameTime distribution period.

This is a recovery record, not evidence that every scanned carrier is historically related to StoneAge.

## Evidence rules

- **FACT:** a named public carrier was scanned completely at ISO-9660/Joliet directory level when the report shows no scan error and no truncation.
- **NEGATIVE CONTROL:** zero StoneAge-path matches applies only to the exact carrier(s), directory namespace(s), and search tokens scanned.
- **OPEN:** absence from these carriers does not imply that StoneAge was never distributed on another magazine/ISP/guide CD or surviving mirror.
- No complete proprietary disc image is committed by this work. The scanner reads only remote directory sectors through HTTP Range requests and commits derived directory metadata.

## Remote directory-scanning method

Canonical scanner:

- `tools/stoneage_netpower_remote_iso_scan.py`

Supported layouts now include:

- 2048-byte ISO logical sectors;
- 2352-byte raw Mode 1 sectors;
- inferred raw-image layouts by locating consecutive ISO volume descriptors;
- observed Korean MDF carriers with 2448-byte frame spacing and variable logical-data origins.

Directory walks cover both primary ISO-9660 and Joliet namespaces where present, recursively enumerate the file tree, and stop only at explicit safety bounds. A carrier is treated as a complete directory-level negative only when the report records no scan error and no truncation.

Current path-match keys include:

- `stoneage`
- `stone age`
- `스톤에이지`
- `sa_demo`
- path-final `sa.exe`
- `enium`

## NetPower 2001.12 control

Derived report:

- `research/recovered/STONEAGE-NETPOWER-CD-DIRECTORY-SCAN-R1.txt`

Two public NetPower 2001.12 images were parsed successfully at directory level.

Result:

- 2 images scanned;
- 0 scan errors;
- 0 StoneAge-path hits;
- no truncation.

Interpretation: these two specific 2001.12 discs are valid negative controls. They are not evidence against other NetPower issues or other Korean distribution media.

## PC Game Magazine launch-window control

Derived report:

- `research/recovered/STONEAGE-KOREAN-PC-MAGAZINE-LAUNCH-WINDOW-R1.txt`

The final R1 pass covers 21 public PC Game Magazine carriers from 2000-09 through 2001-12.

Result:

- 21 images scanned;
- 0 scan errors;
- 0 StoneAge-path hits;
- no truncation;
- thousands of directory entries were enumerated across the larger discs.

Notable date-proximate carriers include:

- `200009/CD1/BLAZEBLADE.mdf`
- `200009/CD2/PCGM0009.mdf`
- `200010/CD1/990915_1453.mdf`
- `200010/CD2/ED3_CD1.mdf`
- `200011/CD1/PB2.mdf`
- `200011/CD2/NEW.mdf`
- 2001-01 through 2001-12 PCGM carriers.

Interpretation: these exact twenty-one carriers are closed as directory-level negatives for the full 2000-09 through 2001-12 scan window.

## GamePia transition-window control

Derived report:

- `research/recovered/STONEAGE-GAMEPIA-TRANSITION-DISC-SCAN-R1.txt`

The selected GamePia sequence now covers issues No.58 through No.69, crossing and extending beyond the Korean StoneAge trial/formal distribution period. Twenty-three carrier images were scanned.

Result:

- 23 images scanned;
- 0 scan errors;
- 0 StoneAge-path hits;
- no truncation.

Date-bearing carrier names include:

- No.58 CD2 `0007101814.bin`;
- No.60 CD2 `0009081414.bin`;
- No.61 CD2 `0010121137.bin`;
- No.64 CD2 explicitly labeled `2001-02`.

Large directory trees were fully enumerated, including 3,212 entries on No.58 CD2 and 3,943 entries on No.61 CD1.

Interpretation: No.58–69 are closed as exact-carrier negative controls. Other GamePia issues remain distinct candidates and are not covered by this conclusion.

## Internet Archive exact-token reverse search

Derived report:

- `research/recovered/STONEAGE-ARCHIVE-CANDIDATE-FILES-R1.txt`

The archive metadata/file-list probe searched both general StoneAge terms and exact historical recovery tokens:

- `sa_demo.exe`
- **`stone_demo.exe`**
- **`onlStoneAge.zip`**
- **`images/Online/pds/2001/02/onlStoneAge.zip`**
- `stoneagebeta.zip`
- `20001031524596220`
- `200009263856`
- `GW_IDX=9`
- `/pc/games/online/stoneage.zip`

Result:

- 222 unique items;
- 222 item metadata records fetched;
- 0 request errors;
- 11 size-window candidates;
- **0 exact target filename matches**.

The 11 file candidates are size-only false positives. Search hits for `sa_demo.exe` and `GW_IDX=9` were also shown by file-list verification to be unrelated tokenization/substring matches.

The newly recovered `stone_demo.exe` token produced 7 IA search-index hits, but none of those items contains an exact `stone_demo.exe` file in its archive file list. The search-index hits are therefore false-positive/tokenization results, not preserved StoneAge payloads. The exact `onlStoneAge.zip` basename query and the full `images/Online/pds/2001/02/onlStoneAge.zip` path query each return **0 IA search results**.

Interpretation: this exact Internet Archive metadata-query set is closed as a negative control. Repeating the same queries without a new identifier or search surface is low value.

## Wayback distribution-directory prefix census

Derived report:

- `research/recovered/STONEAGE-KOREAN-DISTRIBUTION-CDX-PREFIXES-R1.txt`

A 2000–2002 Wayback CDX prefix enumeration now covers fifteen distribution-directory variants, including the exact GameTime image-PDS directory recovered from the record-9 redirect.

Aggregate result:

- 15 prefix queries;
- 1 request error, limited to a timeout on `www.stoneage.hananet.net/down/`;
- 373 returned rows;
- 192 unique archived URLs.

### Hananet and CNET directory boundary

The bare Hananet `/down/` prefix and both CNET `/pc/games/online/` host variants return **0 rows**; the `www` Hananet variant timed out in the latest run and should remain inconclusive rather than be counted as another zero. Because the same probe returns substantial records for Gagamel, GameTime, and Inium, the successful zero-row results are useful Wayback directory-level negative controls for those exact prefixes and date window.

They do not prove that `sa.exe`, `sa_demo.exe`, or `stoneage.zip` never survived on other mirrors or outside Wayback.

### Gagamel

The Gagamel `/web_data/download/` prefix returns five archived payload URLs, all unrelated to StoneAge in the enumerated set. The historically known `stoneagebeta.zip` does not appear in the returned 2000–2002 prefix census.

### Inium

The Inium `/down` / `/download` prefix has archived web hierarchy and later material. A 2002 payload named `/download/material/sa4_21.exe` is indexed at 268,080 bytes, but this is a later material object and is not evidence of the 2000 clean client.

### GameTime PDS host

The later GameTime StoneAge data-center HTML references **`pds.gametime.co.kr`**, so the PDS host was added as a dedicated 2000–2002 CDX prefix.

Result:

- **11 archived URLs**;
- all preserved objects are image/JPEG resources;
- 0 client executable/archive URLs.

Interpretation: the current Wayback prefix-index route for `pds.gametime.co.kr` is closed as a negative control. In addition, both bare and `www` **`gametime.co.kr/images/Online/pds/2001/02/`** prefix queries complete successfully with **0 rows**, so the exact directory that later housed `onlStoneAge.zip` and `stone_demo.exe` has no Wayback CDX entries in this 2000–2002 census. This does not exclude off-Wayback mirrors or unindexed historical payloads.

### GameTime — archived StoneAge result route

GameTime's archived `/data/` namespace contains a preserved StoneAge-specific search page:

- timestamp: **2001-07-01 05:34:12 UTC**
- URL search term: `%bd%ba%c5%e6%bf%a1%c0%cc%c1%f6`
- CP949/EUC-KR decoding: **`스톤에이지`**
- category: `online`

This route is no longer merely a lead. The resolver completed and exposed `GW_IDX=76 → stone_demo.exe`, `GW_IDX=34 → StoneAge.zip` (manual update), while the legacy webzine plus archived 302 headers resolve record 9 through to **`onlStoneAge.zip`**. The remaining GameTime problem is payload-byte recovery and build identity, not record/filename discovery.

Derived records:

- `research/recovered/STONEAGE-GAMETIME-2001-RECORD-RESOLUTION-R1.txt`
- `research/recovered/STONEAGE-GAMETIME-ONLINE-INDEX-R1.txt`
- `research/recovered/STONEAGE-GAMETIME-LEGACY-WEBZINE-R1.txt`
- `research/recovered/STONEAGE-GAMETIME-REDIRECT-HEADERS-R1.txt`

## GameTime StoneAge data-center identities recovered

The archived GameTime StoneAge search page at **2001-07-01 05:34:12 UTC** now resolves two concrete records:

- **GW_IDX=76 — StoneAge trial client**
  - title: `스톤에이지 체험판 클라이언트`;
  - filename: **`stone_demo.exe`**;
  - registered: **2001-02-12 19:45:00**;
  - list-page size: **234MB**;
  - description says the formal version is roughly **260MB** and the trial version roughly **240MB**;
  - trial access is described as five days and requires a separate trial-account application;
  - trial characters/pets are explicitly described as not linked to the formal server;
  - archived download count is 21,187 on 2001-07-01 and 53,612 on 2001-08-20.

- **GW_IDX=34 — StoneAge manual update**
  - title: `스톤에이지 자동 업데이트가 안된다면 이것을...`;
  - filename: **`StoneAge.zip`**;
  - registered: **2000-11-06 11:21:00**;
  - list-page size: **0.4MB**;
  - an independent 2001-04-17 GameTime webzine record shows **0.42 MB**;
  - the instructions identify it as a **manual update**, not a full client;
  - before copying the update, users are told to delete **`sa_*.exe`**, **`server_*.ini`** and **`stoneage.exe`** from the installed StoneAge directory.

This is a critical filename-collision control: GameTime's **0.4/0.42MB `StoneAge.zip`** is a manual update and must not be conflated with CNET Korea's independently recovered **257MB `/pc/games/online/stoneage.zip`** full-client distribution object.

The same archived 2000-12-08 GameTime StoneAge article links `/webzine/online/download.asp?name=스톤에이지` and describes Inium as the Korean operator. The article says Korean beta service began for general users on October 1 and formal service was planned for December; these article statements are retained as contemporary GameTime reporting rather than silently merged with other launch-date sources.

A broader archived online-list sweep successfully replayed **11 anchors / 52 parsed records with zero replay errors**, including pages 1–10 where available. It repeatedly recovers GW_IDX=76 but does **not** recover **GW_IDX=9**. Therefore GW_IDX=9 is no longer treated as something that can be found merely by continuing current data-center pagination. The remaining branch is the older GameTime webzine/download system and exact historical mirror link preserved on Inium's official page.

Derived records:

- `research/recovered/STONEAGE-GAMETIME-2001-RECORD-RESOLUTION-R1.txt`
- `research/recovered/STONEAGE-GAMETIME-ONLINE-INDEX-R1.txt`

## GameTime record 9 exact payload redirect recovered

The migrated GameTime handler is no longer only a record-level clue.

Archived HTTP 302 responses for:

- `/data/download.asp?GW_IDX=9&GW_Name=Online`

at **2001-06-14**, **2001-08-06**, **2001-12-15** and **2002-02-08** all preserve the same redirect target:

**`http://www.gametime.co.kr/images/Online/pds/2001/02/onlStoneAge.zip`**

The control trial record:

- `GW_IDX=76`

preserves the parallel redirect target:

**`http://www.gametime.co.kr/images/Online/pds/2001/02/stone_demo.exe`**

This creates an exact payload filename/path pair for the two GameTime records and confirms that the download handler redirected to files under the GameTime image/PDS tree.

The legacy evidence remains important:

- old `num=9` is the 2000-10-11 `스톤 에이지 베타 버젼용 클라이언트`;
- old `num=34` is the StoneAge manual update;
- migrated `GW_IDX=34` preserves the same manual-update identity;
- later Inium links `GW_IDX=9` among formal-version mirrors.

Therefore **`onlStoneAge.zip`** is the migrated record-9 payload identity, but the project must still not assume that its bytes remained unchanged from the original 2000 Beta attachment. Persistent record key and persistent attachment filename are not sufficient to prove persistent byte identity.

Direct archive checks:

- `onlStoneAge.zip`: bare/www exact CDX queries return zero rows;
- `stone_demo.exe`: exact CDX requests timed out and remain inconclusive;
- eight exact Wayback Availability checks across the two payloads complete without request errors and return zero available captures;
- both bare/`www` `gametime.co.kr/images/Online/pds/2001/02/` prefix queries complete successfully with zero rows;
- Internet Archive metadata/file-list search returns zero `onlStoneAge.zip` basename/path search hits and zero exact target filename matches across 222 inspected items;
- Arquivo.pt checks 18 exact mirror URLs with zero request errors and zero indexed captures, including bare/`www` `onlStoneAge.zip` and `stone_demo.exe`;
- the updated Common Crawl probe includes both files and their directory prefix, but 109 of 112 queries fail with HTTP 503 or timeout, so Common Crawl remains **inconclusive**, not negative evidence.

No client bytes were recovered by these checks.

Derived records:

- `research/recovered/STONEAGE-GAMETIME-DOWNLOAD-REDIRECT-CDX-R1.txt`
- `research/recovered/STONEAGE-GAMETIME-REDIRECT-HEADERS-R1.txt`
- `research/recovered/STONEAGE-GAMETIME-PAYLOAD-CAPTURES-R1.txt`

## Operational consequence

The public-media route is now materially narrower:

1. Do not repeat the closed NetPower 2001.12, PCGM 2000-09..2001-12, GamePia No.58..69, or exact IA-token scans unless a new token or materially better parser changes the question.
2. Prioritize exact recovery of GameTime **`onlStoneAge.zip`** at `/images/Online/pds/2001/02/onlStoneAge.zip`, now server-bound to `GW_IDX=9`; the current IA, Wayback and Arquivo routes are exhausted for this exact object, while Common Crawl is service-inconclusive. Shift effort toward reposts, old FTP/web mirrors, software-CD indexes and preserved installations; retain `stone_demo.exe` as the independently resolved trial-client token.
3. Continue expanded public-disc scanning only where the carrier dates or metadata materially overlap the 2000–2001 Korean distribution window.
4. On any concrete installer/archive hit, stop broad enumeration and run the clean-client acceptance pipeline: provenance, archive hash, full file tree/per-file hashes, executable metadata, updater/endpoints, resource generations, and contamination checks.

## Current status

**OPEN / narrowed recovery surface.**

No provenance-preserving 2000–2001 Korean StoneAge client bytes have yet been recovered by this corpus pass. The main gain is reproducible elimination of specific public carriers plus recovery of GameTime's exact migrated record-9 payload path **`/images/Online/pds/2001/02/onlStoneAge.zip`** and trial path **`/images/Online/pds/2001/02/stone_demo.exe`**.
