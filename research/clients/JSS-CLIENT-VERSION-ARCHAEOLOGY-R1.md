# JSS Client Version Archaeology — R1

Date: 2026-09-18

Purpose: record first-party evidence that moves the JSS StoneAge archaeology track from product-level facts into concrete client/update artifacts.

## 1. Archived JSS version-up page

### Source

`SRC-JP-JSS-STONEAGE-VERUP-ARCHIVE-01`

Original JSS URL:

`http://www.titan.co.jp/stoneage/verup.html`

Wayback capture used:

https://web.archive.org/web/20001204205900/http://www.titan.co.jp/stoneage/verup.html

### FACT

The archived Japan System Supply page is explicitly a `STONEAGE` update/version-up information page.

It contains an automatic version-up history extending back to **1999-10-18**, only three days after the commercial launch date, and continues through 2000.

The preserved dated history establishes that JSS operated a continuing client/content update mechanism during the original service period. It records repeated event/content additions, bug fixes, map/NPC/item/pet/UI changes, and other application-side updates.

### Research consequence

- the original JSS client had an active update system essentially from launch;
- a retail-disc image alone will represent only a launch baseline and must eventually be paired with recovered update state(s);
- archaeological comparison should distinguish `retail disc baseline`, `post-launch patched client`, and `beta` rather than treating all 1999 JSS installations as one immutable build.

### OPEN

- exact numeric/internal version identifiers for each dated update;
- update package filenames and protocol;
- whether all updates were file-delta patches, whole-file replacements, data downloads, or a mixture;
- server endpoints/manifests used by automatic update.

## 2. Concrete launcher filename recovered

### Source

`SRC-JP-JSS-STONEAGE-LAUNCHER-ARCHIVE-01`

Original JSS URL:

`http://www.titan.co.jp/stoneage/updater.html`

Wayback capture used:

https://web.archive.org/web/20001204205200/http://www.titan.co.jp/stoneage/updater.html

### FACT

The archived JSS page offers a downloadable replacement StoneAge startup program named:

`stoneage.exe`

The page reports a size of **212 KB**.

Its installation instructions tell the user to download the launcher and overwrite/copy it into the directory where `STONEAGE` is installed, replacing the existing file of the same name.

The page describes the replacement launcher as addressing problems including:

- network errors occurring at startup even when server connection should be possible;
- errors during version-up;
- failure to transition to the new program after version-up.

### Research consequence

`stoneage.exe` is now a confirmed JSS-era client launcher/startup-program filename and a concrete anchor for future disc/file-tree searches.

This is the first recovered original-JSS executable filename in the project.

## 3. Archived executable body exists

Following the JSS download link leads to the original path:

`http://www.titan.co.jp/stoneage/stoneage.exe`

Wayback reports two captures of the executable path (May and July 2001). Attempting to follow the archived object through the available web extraction interface returns content type `application/octet-stream`, which is consistent with preservation of the binary body rather than merely an HTML placeholder.

### Status

**Binary-preservation lead; bytes not yet acquired in the current environment.**

The current environment could identify the archived binary object but could not extract/download its bytes through the available web interface. Therefore no checksum, PE timestamp, imports, version resources, strings, or binary comparison is recorded yet.

Do not commit the proprietary executable to the repository if later acquired. Record only research metadata/hashes/analysis unless repository policy is explicitly changed.

## 4. Archaeology implications

When a 1999 retail disc is recovered, immediately check for:

- `stoneage.exe` at install root;
- its disc file size/hash/PE metadata;
- whether the archived 212 KB launcher is a later replacement of the same executable;
- update-related configuration, URLs, manifests, INI files, DLLs or data files referenced by the launcher;
- embedded strings for `titan.co.jp`, Gamer's Dream hosts, update endpoints, version values and patch filenames.

A reproducible comparison should have at least these states if recoverable:

1. September 1999 beta client;
2. 1999-10-15 retail disc baseline;
3. earliest post-launch updated state (no later than 1999-10-18);
4. archived replacement `stoneage.exe` state;
5. latest pre-JSS-collapse client state.

## 5. Immediate next actions

1. Recover bytes of the archived `stoneage.exe` through a provenance-preserving method outside the current extraction limitation, then record SHA-256/SHA-1/MD5, exact size, PE metadata and strings without committing the executable.
2. Search original JSS pages and archive paths for update manifests/packages and any filenames referenced by `stoneage.exe`.
3. Search surviving retail-disc/package images specifically for the confirmed filename `stoneage.exe`.
4. Use the version-up history to build a dated JSS feature/change chronology separately from later Taiwan/Mainland evolution.
