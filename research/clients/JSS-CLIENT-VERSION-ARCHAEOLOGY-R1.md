# JSS Client Version Archaeology — R1

Date: 2026-09-18

Purpose: record first-party evidence that moves the JSS StoneAge archaeology track from product-level facts into concrete client/install/update artifacts.

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

## 4. Retail installation architecture from the official manual

### Source

`SRC-JP-JSS-STONEAGE-MANUAL-ARCHIVE-01`

Manual index:

`http://www.titan.co.jp/stoneage/manual.html`

Archived installation/start page:

https://web.archive.org/web/20010119071900/http://www.titan.co.jp/stoneage/manual01.html

### FACT

The archived JSS manual confirms the normal retail-install path in more detail:

- DirectX 6.1 was required and was included on the **game CD**;
- installation began by inserting the StoneAge **game CD** into the CD-ROM drive;
- the installer was designed to start automatically;
- the installer offered three modes:
  - standard — StoneAge plus DirectX;
  - minimum — StoneAge only;
  - custom — selectable components;
- for an installation problem, the manual specifically recommends custom installation with the `map` component unchecked;
- the Windows Start-menu path is shown as `[Stoneage]` -> `[stoneage]`;
- game/service registration used an ID NUMBER/password supplied after agreement with Gamer's Dream;
- a physical **CD NUMBER card** contained the CD NUMBER required for the Gamer's Dream service contract/registration and was to be retained;
- F12 saved screenshots under a `screenshot` subdirectory beneath the StoneAge folder;
- Alt+Enter toggled window mode, with the manual limiting supported display color for that mode to 256 colors.

### Research consequence

This confirms two distinct classes of launch artifact that should be sought physically:

1. the normal **game CD** used for installation;
2. the **CD NUMBER card** used for service registration.

It also further weakens any assumption that the separately advertised initial-edition `STONEAGE` special/bonus CD must itself be the install disc. That relationship remains OPEN until package contents are directly documented.

### Important limits

- singular wording `game CD` does **not** prove the package contained only one disc;
- the manual capture does not establish the exact initial-edition versus standard-edition disc count;
- server names visible in damaged/garbled text are not transcribed as facts.

## 5. Update/download architecture from the official FAQ

### Source

`SRC-JP-JSS-STONEAGE-FAQ-ARCHIVE-01`

Archived JSS FAQ/startup troubleshooting page:

https://web.archive.org/web/20010215222514/http://www.titan.co.jp/stoneage/faqstart.html

### FACT

The official JSS FAQ exposes several concrete filesystem and updater behaviors:

- it checks/mentions `MFC42.DLL` during startup troubleshooting;
- reinstall instructions explicitly refer to reinstalling StoneAge from the CD;
- when version-up/network problems persist, users are told to delete files in the StoneAge installation's `data\download` directory;
- users are also told to clear Windows `Temporary Internet Files` and retry StoneAge/version-up;
- update failures include repeated downloading of a file, save failures, and a download failure displaying `cksum:xxxxxxxxx`;
- proxy configuration is discussed in the same update troubleshooting section;
- cleanup instructions for data left by an earlier StoneAge test tell users to uninstall StoneAge, completely remove `ProgramFiles\jss\stoneage`, and then install the retail product;
- CD NUMBER is again described as a value entered when contracting/registering with Gamer's Dream;
- install-error workarounds again include a custom install with the `MAP` component unchecked;
- CD troubleshooting explicitly tells users to inspect/clean the readable side of the StoneAge CD.

### What this establishes about the updater

At minimum, the JSS client/update system had:

- an installation lineage under `ProgramFiles\jss\stoneage` in the documented test-cleanup case;
- a download staging/cache directory at `data\download` under the StoneAge installation;
- a checksum-related error representation `cksum:xxxxxxxxx`;
- interaction with Windows Internet/cache/proxy settings significant enough to appear in official troubleshooting;
- downloadable update files that could fail individually and be retried.

### What remains OPEN

- the checksum algorithm represented by `cksum`;
- manifest filename/format;
- update-server hostname/path;
- names/extensions of downloaded payload files;
- whether Internet Explorer/WinINet APIs were used directly or the Temporary Internet Files dependency arose through another component;
- the exact Japanese label/name of the earlier StoneAge test referred to in the damaged archive text.

The last point is deliberately left unresolved: the existence of earlier test data and the documented cleanup path are FACT; the precise test label is not reconstructed from mojibake.

## 6. Archaeology implications

When a 1999 retail disc is recovered, immediately check for:

- `stoneage.exe` at install root;
- installer/autostart metadata and the `map` install component;
- its disc file size/hash/PE metadata;
- whether the archived 212 KB launcher is a later replacement of the same executable;
- `data\download` creation/use;
- update-related configuration, URLs, manifests, INI files, DLLs or data files referenced by the launcher;
- `MFC42.DLL` dependencies or bundled runtime files;
- embedded strings for `titan.co.jp`, Gamer's Dream hosts, update endpoints, `cksum`, version values and patch filenames;
- a `screenshot` directory or strings/path creation code corresponding to it.

A provenance-preserving package audit should additionally photograph/record:

- game-CD label and matrix code;
- CD NUMBER card;
- any initial-edition special/bonus CD separately;
- all manuals/inserts and product/JAN identifiers.

A reproducible comparison should have at least these states if recoverable:

1. September 1999 beta client;
2. 1999-10-15 retail disc baseline;
3. earliest post-launch updated state (no later than 1999-10-18);
4. archived replacement `stoneage.exe` state;
5. latest pre-JSS-collapse client state.

## 7. Immediate next actions

1. Recover bytes of the archived `stoneage.exe` through a provenance-preserving method outside the current extraction limitation, then record SHA-256/SHA-1/MD5, exact size, PE metadata and strings without committing the executable.
2. Mine archived JSS pages for the update server/manifest/protocol using the newly recovered anchors `data\download`, `cksum`, `MFC42.DLL`, `ProgramFiles\jss\stoneage` and `stoneage.exe`.
3. Search original JSS pages and archive paths for downloaded payload filenames/extensions and updater configuration files.
4. Search surviving retail-disc/package images specifically for the game CD, CD NUMBER card, `stoneage.exe`, and any separately labeled initial-edition special CD.
5. Use the version-up history to build a dated JSS feature/change chronology separately from later Taiwan/Mainland evolution.
