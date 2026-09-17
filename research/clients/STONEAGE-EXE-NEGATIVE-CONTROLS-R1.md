# StoneAge.exe Negative Controls — R1

Date: 2026-09-18

Purpose: maintain explicit fingerprints for later/descendant executables named `StoneAge.exe` that can appear in public search results but are demonstrably not the archived Japan System Supply 1999/2000 launcher target.

This is an artifact-triage document. A filename match is not provenance.

## Why a negative-control ledger is necessary

The original JSS archive establishes that an original StoneAge startup/launcher program named `stoneage.exe` existed and that JSS later offered a replacement copy advertised as 212 KB.

Public malware/sandbox/file indexes also contain unrelated or much later files named `StoneAge.exe`. Searching by filename alone can therefore contaminate the JSS archaeology track.

Any candidate binary must be classified from provenance, hashes, PE metadata, resources, language, dates and relationship to known JSS paths before it is allowed into the original-client evidence set.

## NC-SA-EXE-2019-ANYRUN-01

Public report:

https://any.run/report/9c019d9fab9c0dc37a37a67519ca5080ae43ec2b2a84b915a24b742512a6a7ca/a36313b7-be88-42a2-a913-2a62f8edccb7

### Observed fingerprint

- submitted filename: `StoneAge.exe`
- SHA-256: `9C019D9FAB9C0DC37A37A67519CA5080AE43EC2B2A84B915A24B742512A6A7CA`
- SHA-1: `8C89E619399AFDF7F0F706722C3E648FA2A99654`
- MD5: `A1A524D45C90ED3B7537A254B8757740`
- analysis date: 2019-10-21
- PE timestamp reported by the sandbox: `2019-10-08 12:14:10+02:00`
- PE type: 32-bit Windows GUI executable / Intel 386
- file version: `1.0.0.1`
- product version: `1.0.0.1`
- resource language includes Simplified Chinese; report also detects English and Korean resources
- `LegalCopyright`: `Copyright c 2010`
- `OriginalFileName`: `Sa.exe`
- `FileDescription`: `Stoneage`
- `ProductName`: `石器时代`
- debug/output material includes `Themida Professional` / `(c)2012 Oreans Technologies`

### Classification

**NEGATIVE CONTROL — exclude from JSS-1999/2000 candidate set.**

The 2019 PE timestamp, 2010 copyright resource, Simplified-Chinese localization and Themida-era material are irreconcilable with treating this file as the JSS launcher advertised during the original Japanese service period.

The report is still archaeologically useful because `OriginalFileName = Sa.exe` independently illustrates how a later StoneAge binary can be redistributed or surfaced under the filename `StoneAge.exe`. That observation is consistent with the project's general warning that later `StoneAge.exe` / `sa.exe` naming must never be projected backward into 1999 without provenance.

It does **not** prove any direct code lineage from JSS.

## Search rule created by this control

When a public index returns a file called `StoneAge.exe`:

1. compare SHA-256/SHA-1/MD5 against this ledger;
2. inspect PE timestamp and version resources before spending time on strings or behavior;
3. reject candidates whose publisher/language/version chronology clearly belongs to later Taiwan/Mainland/private-service lineages;
4. do not infer that `OriginalFileName = Sa.exe` existed in 1999 merely because a later file carries that resource;
5. prioritize candidates tied to the original JSS URL, original retail media, a provenance-preserving old installation, or another first-party archival chain.

## Positive JSS target remains unchanged

The target still to recover is the archived original-path object:

`http://www.titan.co.jp/stoneage/stoneage.exe`

Known first-party constraints remain:

- JSS described it as a replacement StoneAge startup program;
- advertised size: **212 KB**;
- it replaced an existing same-named file in the StoneAge installation directory;
- it addressed startup network errors, version-up errors and failure to transition after updating.

No hash, exact byte size, PE timestamp, resource version, imports or strings have yet been authenticated for that JSS object.

## Next actions

- continue extracting the archived JSS binary through a provenance-preserving route;
- add any newly encountered same-name binaries to this ledger only when enough metadata exists to classify them confidently;
- once the JSS binary is recovered, establish its hashes as the positive-control fingerprint and compare all later candidates against it.
