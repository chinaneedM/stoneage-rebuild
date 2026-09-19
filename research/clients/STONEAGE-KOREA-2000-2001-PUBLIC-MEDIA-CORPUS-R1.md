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

The selected GamePia sequence covers issues No.58 through No.64, crossing the Korean StoneAge trial/formal distribution period. Twelve carrier images were scanned.

Result:

- 12 images scanned;
- 0 scan errors;
- 0 StoneAge-path hits;
- no truncation.

Date-bearing carrier names include:

- No.58 CD2 `0007101814.bin`;
- No.60 CD2 `0009081414.bin`;
- No.61 CD2 `0010121137.bin`;
- No.64 CD2 explicitly labeled `2001-02`.

Large directory trees were fully enumerated, including 3,212 entries on No.58 CD2 and 3,943 entries on No.61 CD1.

Interpretation: No.58–64 are closed as exact-carrier negative controls. Other GamePia issues remain distinct candidates and are not covered by this conclusion.

## Internet Archive exact-token reverse search

Derived report:

- `research/recovered/STONEAGE-ARCHIVE-CANDIDATE-FILES-R1.txt`

The archive metadata/file-list probe searched both general StoneAge terms and exact historical recovery tokens:

- `sa_demo.exe`
- `stoneagebeta.zip`
- `20001031524596220`
- `200009263856`
- `GW_IDX=9`
- `/pc/games/online/stoneage.zip`

Result:

- 216 unique items;
- 216 item metadata records fetched;
- 0 request errors;
- 9 size-window candidates;
- **0 exact target filename matches**.

The 9 file candidates are size-only false positives. Search hits for `sa_demo.exe` and `GW_IDX=9` were also shown by file-list verification to be unrelated tokenization/substring matches.

Interpretation: this exact Internet Archive metadata-query set is closed as a negative control. Repeating the same queries without a new identifier or search surface is low value.

## Wayback distribution-directory prefix census

Derived report:

- `research/recovered/STONEAGE-KOREAN-DISTRIBUTION-CDX-PREFIXES-R1.txt`

A 2000–2002 Wayback CDX prefix enumeration queried twelve bare/www distribution-directory variants.

Aggregate result:

- 12 prefix queries;
- 0 request errors;
- 362 returned rows;
- 181 unique archived URLs.

### Hananet and CNET directory boundary

The exact Hananet `/down/` and CNET `/pc/games/online/` prefixes return **0 rows** for both tested host variants.

Because the same probe returns substantial records for Gagamel, GameTime, and Inium, these zero-row results are useful Wayback directory-level negative controls for those exact prefixes and date window.

They do not prove that `sa.exe`, `sa_demo.exe`, or `stoneage.zip` never survived on other mirrors or outside Wayback.

### Gagamel

The Gagamel `/web_data/download/` prefix returns five archived payload URLs, all unrelated to StoneAge in the enumerated set. The historically known `stoneagebeta.zip` does not appear in the returned 2000–2002 prefix census.

### Inium

The Inium `/down` / `/download` prefix has archived web hierarchy and later material. A 2002 payload named `/download/material/sa4_21.exe` is indexed at 268,080 bytes, but this is a later material object and is not evidence of the 2000 clean client.

### GameTime — new high-value route

GameTime's archived `/data/` namespace contains a preserved StoneAge-specific search page:

- timestamp: **2001-07-01 05:34:12 UTC**
- URL search term: `%bd%ba%c5%e6%bf%a1%c0%cc%c1%f6`
- CP949/EUC-KR decoding: **`스톤에이지`**
- category: `online`

This is a concrete archived GameTime StoneAge result surface, not merely a generic portal root. It is now the highest-value unresolved branch from this corpus because it may expose the underlying GameTime record ID, detail endpoint, and relationship to the independently known `GW_IDX=9` mirror token.

Focused resolver:

- `tools/stoneage_gametime_stoneage_record_probe.py`
- expected derived record: `research/recovered/STONEAGE-GAMETIME-2001-RECORD-RESOLUTION-R1.txt`

Until that resolver finishes, no new GameTime payload identity beyond the already known historical `GW_IDX=9` may be claimed.

## Operational consequence

The public-media route is now materially narrower:

1. Do not repeat the closed NetPower 2001.12, PCGM 2000-09..2001-12, GamePia No.58..64, or exact IA-token scans unless a new token or materially better parser changes the question.
2. Prioritize the archived GameTime StoneAge search/result chain.
3. Continue expanded public-disc scanning only where the carrier dates or metadata materially overlap the 2000–2001 Korean distribution window.
4. On any concrete installer/archive hit, stop broad enumeration and run the clean-client acceptance pipeline: provenance, archive hash, full file tree/per-file hashes, executable metadata, updater/endpoints, resource generations, and contamination checks.

## Current status

**OPEN / narrowed recovery surface.**

No provenance-preserving 2000–2001 Korean StoneAge client bytes have yet been recovered by this corpus pass. The main gain is reproducible elimination of specific public carriers and discovery of the archived 2001-07-01 GameTime StoneAge search surface.
