# Current State

Last updated: 2026-09-18

## Current phase

**Phase 0 — StoneAge Origin Archaeology**

The independent GitHub repository and continuity scaffold are established on remote `main`. GitHub read/write continuity has been verified, and the current workstream is primary-source recovery for the 1999 JSS client, beta, package, install/update system, and original Gamer's Dream service layer.

## Confirmed project direction

- Single-player game, not a commercial MMORPG operation.
- Historical clients and materials are research samples, not code/assets to copy directly into the new game.
- Start from the earliest traceable JSS-era StoneAge rather than assuming Mainland China 1.82 is the absolute origin.
- Mainland 1.82 remains a major reference point because it is close to the user's childhood experience and is commonly remembered as a classic early form.
- Later systems/content may ultimately be integrated, but through coherent progression rather than a feature dump.
- Emotional milestones such as first pet capture, first ride, first major exploration, etc. are part of the design target.

## Current historical working picture

### FACT / high-confidence working facts

- StoneAge was developed by Japan System Supply (JSS).
- `STONEAGE` was publicly exhibited at Tokyo Game Show '99 Spring by **1999-03-19** in NTT Data's Gamer's Dream booth.
- Wayback reports archived captures of the original Gamer's Dream index beginning **1999-04-22**, so the pre-beta/pre-launch web layer is at least partially recoverable.
- By May 1999, contemporaneous `Play Online` coverage described the planned game as a relaxed Stone Age RPG emphasizing food/resources, community, and cooperative village development. This is FACT for **published pre-launch design intent**, not automatic proof of final shipped implementation.
- Beta recruitment closed **1999-08-20**; the beta itself ran **1999-09-01 through 1999-09-30**, supported by contemporaneous `Play Online` issue 015.
- The preserved `Play Online` issue 015 is now searchable deeply enough to recover the beta-application URL host as `www.dp.gamersdream.ne.jp` and its path tail as `PO/sa_apply.html`. One character immediately before `PO` remains OCR-ambiguous and is **not** normalized or guessed in the factual record.
- PC Watch reported on 1999-09-17 that the JSS title was scheduled for release on **1999-10-15**.
- A photographed period retail advertisement gives Windows 95/98 as platform, **1999-10-15** as scheduled release date, **8,800 yen before tax** as planned price, and prints the period domains `www.titan.co.jp` and `www.gamersdream.ne.jp`.
- The same advertisement visibly promotes an original mug as a reservation bonus and a `STONEAGE` special CD as an initial-edition bonus/feature.
- An archived first-party Gamer's Dream StoneAge product page independently lists **1999-10-15** as release date, package price 8,800 yen, a 4x or faster CD-ROM drive, at least 400 MB HDD, 64 MB RAM, MMX Pentium 200 MHz+, 33.6 Kbps+ Internet access, 2 MB+ VRAM, DirectX 6.1-compatible video/sound, mouse and keyboard.
- The same first-party product page tells users to **purchase the software package first and then register for Gamer's Dream service**, materially confirming a normal package-based install/client path.
- The archived official JSS manual confirms that the normal retail path used a StoneAge **game CD**, with DirectX 6.1 on that disc and an auto-start installer. Installation modes were standard, minimum and custom; `map` was a selectable component.
- The same JSS manual confirms a physical **CD NUMBER card** whose CD NUMBER was required for Gamer's Dream service registration/contracting. The manual also documents `[Stoneage]` -> `[stoneage]` as the Start-menu path and a `screenshot` subdirectory under the StoneAge folder.
- Singular wording `game CD` does not establish total disc count; the advertised initial-edition special CD remains a separate artifact until direct package evidence establishes its relationship to the install disc.
- A 2009 4Gamer retrospective states that Japanese service actually started on **1999-10-15**; together with the contemporary PC Watch report and archived Gamer's Dream product page, this date is the high-confidence working commercial start date.
- JSS's archived official version-up page contains an automatic update history beginning **1999-10-18**, only three days after launch. Therefore the retail disc, post-launch client states and later JSS builds must be treated as distinct archaeological states.
- The original JSS StoneAge startup/launcher executable filename is confirmed as **`stoneage.exe`**. JSS offered a replacement launcher advertised as **212 KB** and instructed users to overwrite the same-named file in the existing StoneAge installation directory.
- The JSS launcher-replacement page describes the replacement as addressing startup network errors, version-up errors and failure to transition to the new program after an update.
- The archived JSS FAQ exposes the update/install filesystem more concretely: `ProgramFiles\jss\stoneage`, `data\download`, `MFC42.DLL`, Windows `Temporary Internet Files`, proxy settings and an update-download error containing **`cksum:xxxxxxxxx`**.
- The FAQ tells users with version-up problems to clear `data\download` and Windows Temporary Internet Files, then retry; this supports a downloaded-file staging/cache model with checksum-related validation, while the exact checksum algorithm and update protocol remain OPEN.
- The FAQ also documents cleanup of data from an earlier StoneAge test by uninstalling, completely deleting `ProgramFiles\jss\stoneage`, then installing the retail product. The exact Japanese name/label of that earlier test is not reconstructed from damaged archive text.
- Wayback exposes an archived original path for `http://www.titan.co.jp/stoneage/stoneage.exe` and reports two captures; the available extraction interface identifies the archived object as `application/octet-stream`. The current environment has not obtained the binary bytes, so no checksum/PE metadata has been claimed.
- Archived Gamer's Dream notices from the JSS collapse period state that JSS handled the StoneAge game-application side, including software corrections and version upgrades, while Gamer's Dream handled server/service operation and billing. After JSS failed in October 2000, Gamer's Dream could continue only reduced service and package sales/version upgrades ceased under the prior arrangement.
- Taiwan and Mainland Chinese versions followed later and introduced localization/iteration layers.

Precise first-party claims are tied to `docs/SOURCE-REGISTRY.md`. Detailed research is split across:

- `research/origin/JSS-1999-ORIGIN-EVIDENCE-R1.md`
- `research/origin/GAMERSDREAM-JSS-ARCHIVE-EVIDENCE-R1.md`
- `research/clients/JSS-CLIENT-VERSION-ARCHAEOLOGY-R1.md`
- `research/clients/DESCENDANT-CLIENT-SOURCE-LINEAGE-R1.md` — explicitly lower-confidence later-source lineage clues, not 1999 JSS facts.

### HYPOTHESIS / lower-confidence search leads

- The earliest StoneAge concept may have been much simpler in macro-lore than later versions, even though resource/community/village-life themes are directly attested in May 1999 design coverage.
- Much of the later macro-lore may have been progressively added to explain and extend an initially simpler world.
- Some mechanics remembered as "core StoneAge" by later players may not have existed for normal players in the earliest Japanese operation.
- The strongest current media model is that the retail package contained normal install/client media and the initial edition additionally included a separate special/bonus CD. This is **not FACT** until an original first-edition package or first-party contents list proves the disc layout.
- The updater probably used a manifest/protocol that mapped downloadable files to checksum values, but the manifest filename, checksum algorithm, endpoint and payload format remain unresolved.
- The OCR-ambiguous character immediately before `PO/sa_apply.html` could be an old-style user-directory marker such as `~`, but this remains a **search hypothesis only** and is not the registered exact beta URL.
- Multiple later community-preserved client-source trees retain JSS/Gamer's Dream title identifiers. One later lineage uses `StoneAge.exe` as a launcher/update-facing program while project/debug metadata names a runtime `sa.exe`; the runtime also contains the strings `updated` and `CheckForUpdate`. Later Taiwan troubleshooting material independently records `cksum:...:File:sa.exe`. This makes **`sa.exe` a high-value original-artifact search target**, but does **not** establish that the filename or launcher/runtime split existed in the 1999 JSS beta or retail client.

## Highest-priority research questions

1. **Locate and verify the earliest recoverable JSS retail install/client medium or provenance-preserving image.**
   - Progress: a surviving `STONEAGE 初回限定版` physical-package lead, contemporaneous retail advertising, official Gamer's Dream product page and official JSS manual independently constrain the artifact.
   - Confirmed JSS retail/client anchors: normal **game CD**, physical **CD NUMBER card**, `stoneage.exe`, `ProgramFiles\jss\stoneage`, `map` install component, CD-based auto-start installer, 1999-10-15 release and 8,800-yen package price.
   - Search lead from descendant lineages: inspect recovered media for `sa.exe` separately from `stoneage.exe`, plus `updated` and `CheckForUpdate`; these are not yet confirmed JSS-1999 strings.
   - Still missing: provenance-preserving retail disc image/dump, exact disc count, file tree, hashes, retail executable PE metadata, disc matrix identifiers, product/JAN code, disc-label/back-box photos and complete package/manual/insert capture.
2. **Recover and fingerprint the archived JSS `stoneage.exe` replacement launcher.**
   - Progress: exact original JSS path is known; JSS advertised the file as 212 KB; Wayback reports two archived captures and exposes the object as binary content.
   - Current limitation: this environment has not extracted the bytes.
   - Still needed: exact byte size, SHA-256/SHA-1/MD5, PE timestamp, version resources, imports and strings; test specifically for process-launch references to `sa.exe`, the token `updated`, and `CheckForUpdate` rather than assuming descendant behavior.
3. **Recover the automatic-update manifest/protocol and payload naming.**
   - Progress: first-party updater anchors include `data\download`, `cksum:xxxxxxxxx`, `MFC42.DLL`, Windows Temporary Internet Files/proxy behavior and `stoneage.exe`. Much later Taiwan troubleshooting records a descendant checksum error targeting `sa.exe`, showing that filename-bearing `cksum` records existed in a later lineage.
   - Still needed from JSS evidence: manifest/config filename, update host/path, checksum algorithm, payload filenames/extensions, the original `cksum` record structure and whether whole files or deltas were delivered.
4. **Determine the identity and contents of the initial-edition `STONEAGE` special CD.**
   - Progress: the special-CD claim is corroborated by contemporaneous advertising and a surviving sealed-package listing; the official manual separately confirms a normal game CD.
   - OPEN: exact contents, whether physically separate from install/client media, filesystem/audio tracks, identifiers and hashes.
5. **Locate the September 1999 beta client or reliable binary/media evidence.**
   - Progress: beta recruitment deadline is **1999-08-20** and test period **1999-09-01 through 1999-09-30**; official FAQ confirms that data from an earlier StoneAge test could persist under `ProgramFiles\jss\stoneage`; the printed application URL is narrowed to host `www.dp.gamersdream.ne.jp` with path tail `PO/sa_apply.html`.
   - Still missing: the single OCR-ambiguous character before `PO`, an archived copy of the application page, tester/download instructions, installer/client filename, distribution method/media, hashes, internal version and beta-to-retail diff.
6. **Mine the surviving JSS/Gamer's Dream web archives for 1999 paths and support/update artifacts.**
   - Progress: JSS `manual.html`, `manual01.html`, `faqstart.html`, `verup.html`, `updater.html` and `stoneage.exe` paths are known; Gamer's Dream archive coverage begins before beta/launch; beta application matching can now target `*PO/sa_apply.html` rather than the whole domain.
   - Priority targets: update manifests/package names/endpoints; the exact August 1999 beta application capture and sibling tester/download pages; product/shop pages; registration; download/install instructions; support/version pages; any original occurrence of `sa.exe`, `updated` or `CheckForUpdate`.
7. Recover JSS launch box/manual inserts and original world-setting text not already represented by the archived online manual.
8. Determine the earliest documented appearance of:
   - the name "Nies / ニース / 尼斯";
   - the island-continent geography;
   - elemental/spirit lore;
   - pet riding for normal players;
   - major villages and early map topology.
9. Determine JSS-era internal numeric client version numbering.
10. Locate the earliest Taiwan client/manual/site and compare it with JSS material.
11. Locate a clean Mainland early/1.82 client/data set for later diff archaeology.

## Completed in the latest work pass

- Re-read the latest remote `main` before continuing and resumed from GitHub rather than stale chat state.
- Expanded `research/origin/GAMERSDREAM-JSS-ARCHIVE-EVIDENCE-R1.md` with the newly recovered beta-application URL evidence.
- Recovered, from searchable text extraction of the preserved 1999 *Play Online* issue, the beta application's **Gamer's Dream host** `www.dp.gamersdream.ne.jp` and path tail **`PO/sa_apply.html`**.
- Explicitly preserved the unresolved character immediately before `PO` as OCR ambiguity instead of silently converting it to `~`, `/` or another character.
- Added `research/clients/DESCENDANT-CLIENT-SOURCE-LINEAGE-R1.md` to quarantine and document later community/source-lineage clues separately from first-party JSS evidence.
- Recorded recurring descendant identifiers `CG_TITLE_JSS_LOGO` / `CG_TITLE_DREAM_LOGO`, and a later launcher/runtime pattern involving `StoneAge.exe`, runtime target `sa.exe`, command-line token `updated` and mutex `CheckForUpdate`.
- Cross-checked that pattern against later Taiwan troubleshooting material whose updater error explicitly targets `sa.exe` using a `cksum` record; retained this only as descendant evidence, not a retroactive 1999 claim.
- Searched indexed Japanese retail/collector material for a product/JAN code; no reliable product/JAN identifier was recovered in this pass.
- The surviving Mercari first-edition listing exposes 13 original-image URLs, but the current retrieval layer cannot fetch those image bodies. No barcode/product code was guessed from inaccessible images.
- Previously recovered first-party anchors remain authoritative: normal game CD, CD NUMBER card, `stoneage.exe`, `ProgramFiles\jss\stoneage`, `data\download`, `cksum:xxxxxxxxx`, `MFC42.DLL`, archived launcher path and update history beginning 1999-10-18.

## Immediate next actions

1. Continue **original-artifact recovery**, now checking for `sa.exe` as well as the confirmed JSS `stoneage.exe`; search physical-media file lists, archived installation screenshots and original support pages rather than treating the descendant name as fact.
2. Resolve the one OCR-ambiguous character in the beta application URL and match **`*PO/sa_apply.html`** to an August 1999 Wayback capture if one exists; then enumerate sibling paths and links for tester instructions/client delivery.
3. Mine archived JSS pages and paths using `data/download`, `cksum`, `MFC42.DLL`, `ProgramFiles/jss/stoneage`, `map`, `stoneage.exe` and the descendant-derived search strings `sa.exe`, `updated`, `CheckForUpdate` to recover manifest/config/payload names and update-server URLs.
4. Continue the **physical-media recovery track** using the confirmed normal game CD and CD NUMBER card. Prefer accessible back-box/disc-label scans or original objects that can expose product/JAN codes and matrix identifiers; do not infer them from unavailable marketplace images.
5. Keep the **normal retail game CD** and **initial-edition special CD** as separate evidence objects until direct evidence establishes their relationship.
6. If the archived JSS launcher bytes become obtainable, analyze them outside the repository and record only hashes/metadata/derived findings.
7. Once any original retail/beta binary or media is recovered, establish the reproducible client-archaeology pipeline: hashes, PE metadata, file tree, resource inventory, strings, asset IDs, update-state labeling and cross-version diff.

## Continuity status

- Repository: `chinaneedM/stoneage-rebuild`
- Default branch: `main`
- Visibility: public
- Authority: latest GitHub remote state is the single source of truth for project continuity.
- Canonical restart protocol: `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`

## Blockers

No repository or workflow blocker.

The project still lacks a verified 1999 JSS retail disc image and September 1999 beta binary. The beta web-recovery blocker has narrowed materially to a nearly complete application-page path; the retail/client search now has a second executable-name hypothesis (`sa.exe`) derived from descendant evidence, but that hypothesis cannot be promoted until original JSS material confirms it. The binary/media blocker remains the principal Phase 0 constraint.
