# Source Registry Supplement — Preservation and Search Controls R1

Date: 2026-09-18

Purpose: register preservation redundancy and search-triage sources that improve the archaeology workflow without promoting derivative copies or later binaries into primary historical evidence.

## Evidence rule

- Two hosts preserving the same historical magazine are **two preservation paths, not two independent contemporaneous sources**.
- A modern public sandbox report can fingerprint a later file and help reject false positives, but it cannot establish JSS-era behavior by itself.
- Filename equality is never sufficient for provenance.

## SRC-JP-1999-PLAYONLINE-015-RETROMAGS-01

- Title: `Play Online No.015 (September 1999)`
- Historical issue date: September 1999
- Retromags submission date shown by catalog: 2023-12-14
- Contributor shown by catalog: `kitsunebi`
- Catalog URL: https://www.retromags.com/files/category/230-play-online/
- File-detail path exposed by the catalog link: https://www.retromags.com/files/file/7018-play-online-no015-september-1999/
- Retrieval date: 2026-09-18
- Source type: independent modern preservation host for the same contemporaneous magazine issue already registered from the Kingpin mirror
- Confidence: **A for the underlying contemporaneous printed issue once scan identity is verified; preservation-host metadata itself is B/C-level archival metadata**
- Supports:
  - an independent preservation path exists for `Play Online No.015 (September 1999)` outside the Kingpin host;
  - Retromags catalog explicitly identifies the issue number/month and uploader/preservation entry;
  - the issue is part of a broader Retromags `Play Online` run that also includes No.014 (August 1999) and No.016 (October 1999).
- Does not provide independent historical corroboration for the beta dates merely by being a second host; both digital copies represent the same printed issue.
- Current retrieval limitation:
  - the current web extraction layer can read the Retromags catalog but returns a cache miss for the file-detail/download body;
  - therefore this pass has **not** visually compared the Retromags scan against the Kingpin scan and has not used it to resolve the OCR-ambiguous character before `PO/sa_apply.html`.
- Research value:
  - reduces dependence on a single preservation host;
  - provides a second scan target that may resolve the beta-application URL if obtained at higher/cleaner resolution.

## CTRL-SA-EXE-ANYRUN-2019-01

- Public report title: `StoneAge.exe`
- Report URL: https://any.run/report/9c019d9fab9c0dc37a37a67519ca5080ae43ec2b2a84b915a24b742512a6a7ca/a36313b7-be88-42a2-a913-2a62f8edccb7
- Analysis date shown by report: 2019-10-21
- Source type: modern public sandbox report / binary fingerprint
- Classification: **NEGATIVE CONTROL; not JSS-1999/2000 evidence**
- Fingerprints:
  - SHA-256 `9C019D9FAB9C0DC37A37A67519CA5080AE43EC2B2A84B915A24B742512A6A7CA`
  - SHA-1 `8C89E619399AFDF7F0F706722C3E648FA2A99654`
  - MD5 `A1A524D45C90ED3B7537A254B8757740`
- Reported static metadata:
  - PE timestamp 2019-10-08;
  - version 1.0.0.1;
  - Simplified-Chinese resource language;
  - `LegalCopyright = Copyright c 2010`;
  - `OriginalFileName = Sa.exe`;
  - output/string material references Themida Professional `(c)2012 Oreans Technologies`.
- Supports:
  - a demonstrably later file can circulate or be indexed under `StoneAge.exe` while its resource says the original filename is `Sa.exe`;
  - filename-only searches for the JSS launcher have a real false-positive risk.
- Excludes:
  - this exact hash set from the JSS launcher candidate pool.
- Does not establish:
  - direct descent from JSS;
  - that the original 1999 runtime filename was `sa.exe`;
  - that JSS used Themida, these resource versions, or this localization.
- Detailed triage note: `research/clients/STONEAGE-EXE-NEGATIVE-CONTROLS-R1.md`.

## SRC-SA-DESCENDANT-ANSON-UPDATER-LINEAGE-01

- Repository: https://github.com/anson1788/stoneage
- Observed source anchor: `1997fc20456dbda36d181b9680ae10bed2e9cdf9`
- Relevant paths:
  - `石器时代8.5客户端最新源代码/石器源码/system/main.cpp`
  - `石器时代8.5客户端最新源代码/石器源码/石器源码.vcxproj`
  - `石器时代8.5客户端最新源代码/石器源码/石器源码.vcxproj.user`
- Retrieval date: 2026-09-18
- Source type: later community-preserved StoneAge client-source lineage
- Classification: **C / LINEAGE SEARCH CONTROL; not JSS primary evidence**
- Directly observed descendant traits:
  - client code creates mutex `CheckForUpdate` with a comment that it is used by the update program to detect whether StoneAge is running;
  - project output/debug metadata explicitly uses `sa.exe` in later configurations, with a separate `sa25.exe` variant also present.
- Negative/differentiating observations from focused public-source search:
  - no Signally-style `updated` direct-start gate was recovered;
  - no user-facing `StoneAge.exe` launcher instruction was recovered;
  - no `PARAM_ARGS` / `HASH___________@@@@@@@@` occurrence was recovered.
- Research value:
  - independently strengthens `CheckForUpdate` as a persistent updater-coordination fingerprint;
  - independently corroborates `sa.exe` as a later runtime filename;
  - demonstrates that those two traits can survive without Signally's narrower launcher-gate strings.
- Does not establish:
  - any 1999 JSS executable name beyond the already first-party-confirmed `stoneage.exe`;
  - that JSS used `CheckForUpdate`, `sa.exe`, `updated`, or any later source architecture;
  - when any descendant trait first appeared.

## CTRL-SA-SIGNALLY-PATCHER-ARG-01

- Repository: https://github.com/Signally190/sking-sacli
- Observed source anchor: `40cb67ef090ebc0cffd57ca947871bdfd0b18331`
- Relevant path: `system/main.cpp`
- Retrieval date: 2026-09-18
- Source type: branch-local later client-source search control
- Classification: **LOW-PRIORITY C / BRANCH-SPECIFIC LEAD**
- Observed:
  - a patcher-related conditional compares the process command line against `PARAM_ARGS`;
  - `PARAM_ARGS` is defined as `HASH___________@@@@@@@@`.
- Cross-search result:
  - focused global public-code search in this pass found this exact placeholder string only in the Signally tree among the inspected StoneAge source lineages.
- Research consequence:
  - keep the string as a low-cost original-binary search probe if JSS bytes are recovered;
  - do **not** give it the same weight as `CheckForUpdate`, `sa.exe` or the first-party `cksum` vocabulary.
- Does not establish:
  - that the placeholder or patcher gate existed in any JSS-era binary;
  - that it is related to the 1999 updater rather than a later private branch.

## Operational consequence

For future `stoneage.exe` recovery:

1. provenance first;
2. hashes second;
3. PE/resource chronology third;
4. only then deeper static/dynamic comparison.

The positive target remains the archived JSS object at `http://www.titan.co.jp/stoneage/stoneage.exe`, advertised by JSS as a 212 KB replacement startup program.
