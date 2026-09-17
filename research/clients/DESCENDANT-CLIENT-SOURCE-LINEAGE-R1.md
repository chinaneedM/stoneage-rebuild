# Descendant Client Source Lineage — R1

Date: 2026-09-18

Purpose: record **community-preserved later StoneAge client-source lineage clues** that can sharpen searches for original JSS artifacts without confusing descendant code with 1999 primary evidence.

## Evidence boundary

This document is deliberately separate from the first-party JSS archive record.

The repositories and later service-era reports below are not 1999 JSS primary artifacts. Their Git/history provenance does **not** establish a direct chain back to Japan System Supply's launch client. They therefore must not be used to assert original-JSS behavior by themselves.

Classification used here:

- **C / LINEAGE LEAD** — useful community-preserved descendant evidence.
- **HYPOTHESIS** — a concrete original-client search target suggested by descendant continuity.
- Promotion to **FACT** for JSS requires original JSS media/binary/source or contemporaneous first-party documentation.

## 1. Community lineage A — `BismarckDD/stoneage`

Repository:

https://github.com/BismarckDD/stoneage

Observed commit/tree anchor used in this pass:

`999ffdf1d220ec6666eb65339180689c9caf1876`

The repository README describes the tree as including client source and says its server data is compatible with official versions 1.82 through 8.5. This is a modern maintainer statement, not proof that the source itself is an untouched official release.

### C / LINEAGE LEAD — retained JSS / Gamer's Dream title identifiers

The client animation table preserves identifiers:

- `CG_TITLE_JSS_LOGO` = `29017`
- `CG_TITLE_DREAM_LOGO` = `29018`

Source:

https://github.com/BismarckDD/stoneage/blob/999ffdf1d220ec6666eb65339180689c9caf1876/client/stoneage/game/anim_tbl.h

A corresponding title/production source still references the JSS logo and contains a later comment indicating the Gamer's Dream logo display was cancelled on `06/24/2002`.

Source:

https://github.com/BismarckDD/stoneage/blob/999ffdf1d220ec6666eb65339180689c9caf1876/client/stoneage/system/produce.cpp

### Interpretation limit

These identifiers are consistent with code descended from a branch that once represented the JSS/Gamer's Dream presentation layer. They do **not** prove the repository contains the 1999 JSS client source unchanged.

## 2. Community lineage B — `Signally190/sking-sacli`

Repository:

https://github.com/Signally190/sking-sacli

Observed source anchor:

`40cb67ef090ebc0cffd57ca947871bdfd0b18331`

The repository contains extensive later Taiwan/Chinese-era feature switches and dated modifications. Its public Git history is a modern 2021/2022 import/edit history rather than a historical JSS development history. It is therefore used only as descendant lineage evidence.

### C / LINEAGE LEAD — launcher/runtime separation survives in source

In `system/main.cpp`, the descendant runtime:

- rejects direct startup unless its command line contains the token `updated` when the relevant bypass macro is not enabled;
- tells the user to execute `StoneAge.exe` instead;
- creates a mutex named `CheckForUpdate`, with a comment describing it as being for the update program to check whether StoneAge is running.

Source:

https://github.com/Signally190/sking-sacli/blob/40cb67ef090ebc0cffd57ca947871bdfd0b18331/system/main.cpp

This gives three concrete descendant strings worth checking in original artifacts:

- `updated`
- `StoneAge.exe`
- `CheckForUpdate`

### C / LINEAGE LEAD — runtime executable is `sa.exe` in project metadata

The Visual Studio project uses `sa` as a target name in one configuration and `sa_8021` in another. User/debug project settings explicitly point at `sa.exe`.

Sources:

https://github.com/Signally190/sking-sacli/blob/40cb67ef090ebc0cffd57ca947871bdfd0b18331/StoneAge.vcxproj

https://github.com/Signally190/sking-sacli/blob/40cb67ef090ebc0cffd57ca947871bdfd0b18331/StoneAge.vcxproj.user

### C / LINEAGE LEAD — same JSS / DREAM title constants recur

The same `CG_TITLE_JSS_LOGO` and `CG_TITLE_DREAM_LOGO` identifiers occur in this branch and in multiple other public community StoneAge source trees. This repetition suggests a circulated common ancestry, but source circulation itself is not provenance.

## 3. Cross-lineage pattern

Global public-source search finds the JSS/DREAM title constants in multiple separately published StoneAge code trees, including:

- `BismarckDD/stoneage`
- `Signally190/sking-sacli`
- `alrightlook/StoneAgeMobileApp`
- `gavinlinasd/StoneAge`
- `anson1788/stoneage`
- other derivative server/client trees.

This is useful for reconstructing **code lineage persistence**, not for dating the constants to a particular JSS build.

## 4. Later Taiwan updater evidence independently targets `sa.exe`

Later Taiwan-era player support material preserves a concrete updater failure string:

`cksum:0:151797743:File:sa.exe`

It also instructs affected players to run a separately supplied `SaUpdate.exe` from the StoneAge installation directory.

Sources:

- Bahamut troubleshooting archive: https://forum.gamer.com.tw/G2.php?bsn=1571&lorder=2&parent=4967&sn=3957
- Bahamut later troubleshooting post: https://forum.gamer.com.tw/Co.php?bsn=01571&sn=281746

### C / DESCENDANT SERVICE-EVIDENCE significance

This is important because it is independent of the community source repositories yet preserves the same later architecture pattern:

- updater/update program distinct from game runtime;
- checksum validation represented as `cksum`;
- update target `sa.exe`.

The old JSS FAQ independently documents a checksum-related updater error in the form `cksum:xxxxxxxxx`, but does **not** expose `sa.exe` in the currently recovered first-party JSS text. The later Taiwan record therefore provides continuity of the updater vocabulary while still being too late to prove the 1999 target filename.

### Explicit temporal limit

The Taiwan troubleshooting evidence is from the much later service lineage. It proves that `sa.exe` and `cksum` coexisted in a descendant StoneAge updater architecture; it does **not** establish when `sa.exe` first appeared.

## 5. Relationship to first-party JSS evidence

The first-party JSS archive independently establishes as FACT that:

- `stoneage.exe` was an original JSS StoneAge startup/launcher filename;
- JSS distributed a replacement `stoneage.exe` for startup/version-up failures;
- the client used an automatic update system;
- the JSS FAQ documents `data\download` and checksum-related update failures.

The descendant evidence therefore intersects with first-party evidence on the launcher/update concept, but adds a **new unverified runtime candidate**: `sa.exe`.

The correct evidentiary treatment is:

- **FACT:** JSS `stoneage.exe` launcher/startup file existed.
- **C / LINEAGE LEAD:** later descendant sources contain `sa.exe` as the runtime target, a launcher-required `updated` token, and a `CheckForUpdate` mutex.
- **C / DESCENDANT SERVICE EVIDENCE:** later Taiwan updater failure text explicitly names `sa.exe` as a checksum-validated update target.
- **HYPOTHESIS:** an earlier JSS lineage may also have separated launcher/updater `stoneage.exe` from a runtime executable named `sa.exe` (or an ancestor of that naming convention).
- **OPEN:** whether this architecture and filename already existed in the September 1999 beta or 1999-10-15 retail baseline.

## 6. Archaeology consequences

When original JSS media or installations are recovered, do **not** stop after locating `stoneage.exe`. Check separately for:

1. `sa.exe`, `SA.EXE`, or case variants;
2. additional executable(s) launched by `stoneage.exe`;
3. embedded command-line token `updated`;
4. mutex/object string `CheckForUpdate`;
5. command lines constructed by the launcher after version-up;
6. whether `stoneage.exe` and a runtime executable have distinct PE version resources, timestamps and imports;
7. whether `data\download` payloads replace one or both executable layers;
8. whether a `cksum` structure in original binaries/configs associates checksum values with filenames in a form ancestral to the later `cksum:...:File:sa.exe` record;
9. whether the retail disc baseline differs from later JSS patched launcher/runtime pairs.

A positive match in original JSS material would allow these descendant clues to be promoted. A negative match would be equally useful because it would date the launcher/runtime split or filename to a later branch.

## 7. What this document must not be used to claim

Until original JSS evidence is recovered, do **not** state as historical fact that:

- the 1999 JSS runtime executable was `sa.exe`;
- the 1999 launcher passed `updated`;
- the 1999 client used the `CheckForUpdate` mutex;
- the 1999 `cksum` record had the later Taiwan field layout;
- the 1999 retail client had the later source tree's feature macros, protocol stack, assets, or data formats;
- any community repository is an authenticated original JSS source release.

## 8. Immediate next actions

1. Search original JSS archive pages, archived binaries and physical-media listings for `sa.exe` independently of `stoneage.exe`.
2. If archived `stoneage.exe` bytes become obtainable, inspect strings/imports/process-launch behavior for `sa.exe`, `updated` and `CheckForUpdate` without committing the proprietary binary.
3. Search original JSS updater artifacts for a filename-bearing `cksum` record structure rather than assuming the later Taiwan syntax existed unchanged.
4. On any recovered retail/beta disc image, inventory every `.exe`, `.dll`, `.ini`, manifest/config file and the `data\download` path before running anything.
5. Compare descendant source structures only after the original artifact baseline is established; use them as diff/search aids, not as a substitute for provenance.
