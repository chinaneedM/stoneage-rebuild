# Current State

Last updated: 2026-09-18

## Current phase

**Phase 0 — StoneAge Origin Archaeology**

The independent GitHub repository and continuity scaffold are established on remote `main`. GitHub read/write continuity has been verified, and the current workstream is primary-source recovery for the 1999 JSS client, beta, package, update system, and original Gamer's Dream service layer.

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
- PC Watch reported on 1999-09-17 that the JSS title was scheduled for release on **1999-10-15**.
- A photographed period retail advertisement gives Windows 95/98 as platform, **1999-10-15** as scheduled release date, **8,800 yen before tax** as planned price, and prints the period domains `www.titan.co.jp` and `www.gamersdream.ne.jp`.
- The same advertisement visibly promotes an original mug as a reservation bonus and a `STONEAGE` special CD as an initial-edition bonus/feature.
- An archived first-party Gamer's Dream StoneAge product page independently lists **1999-10-15** as release date, package price 8,800 yen, a 4x or faster CD-ROM drive, at least 400 MB HDD, 64 MB RAM, MMX Pentium 200 MHz+, 33.6 Kbps+ Internet access, 2 MB+ VRAM, DirectX 6.1-compatible video/sound, mouse and keyboard.
- The same first-party product page tells users to **purchase the software package first and then register for Gamer's Dream service**, materially confirming a normal package-based install/client path.
- A 2009 4Gamer retrospective states that Japanese service actually started on **1999-10-15**; together with the contemporary PC Watch report and archived Gamer's Dream product page, this date is the high-confidence working commercial start date.
- JSS's archived official version-up page contains an automatic update history beginning **1999-10-18**, only three days after launch. Therefore the retail disc, post-launch client states and later JSS builds must be treated as distinct archaeological states.
- The original JSS StoneAge startup/launcher executable filename is now confirmed as **`stoneage.exe`**. JSS offered a replacement launcher advertised as **212 KB** and instructed users to overwrite the same-named file in the existing StoneAge installation directory.
- The JSS launcher-replacement page describes the replacement as addressing startup network errors, version-up errors and failure to transition to the new program after an update.
- Wayback exposes an archived original path for `http://www.titan.co.jp/stoneage/stoneage.exe` and reports two captures; the available extraction interface identifies the archived object as `application/octet-stream`. The current environment has not obtained the binary bytes, so no checksum/PE metadata has been claimed.
- Archived Gamer's Dream notices from the JSS collapse period state that JSS handled the StoneAge game-application side, including software corrections and version upgrades, while Gamer's Dream handled server/service operation and billing. After JSS failed in October 2000, Gamer's Dream could continue only reduced service and package sales/version upgrades ceased under the prior arrangement.
- Taiwan and Mainland Chinese versions followed later and introduced localization/iteration layers.

Precise claims are tied to `docs/SOURCE-REGISTRY.md`. Detailed research is split across:

- `research/origin/JSS-1999-ORIGIN-EVIDENCE-R1.md`
- `research/origin/GAMERSDREAM-JSS-ARCHIVE-EVIDENCE-R1.md`
- `research/clients/JSS-CLIENT-VERSION-ARCHAEOLOGY-R1.md`

### HYPOTHESIS

- The earliest StoneAge concept may have been much simpler in macro-lore than later versions, even though resource/community/village-life themes are directly attested in May 1999 design coverage.
- Much of the later macro-lore may have been progressively added to explain and extend an initially simpler world.
- Some mechanics remembered as "core StoneAge" by later players may not have existed for normal players in the earliest Japanese operation.
- The strongest current media model is that the retail package contained normal install/client media and the initial edition additionally included a separate special/bonus CD. This is **not FACT** until an original first-edition package or first-party contents list proves the disc layout.

## Highest-priority research questions

1. **Locate and verify the earliest recoverable JSS retail install/client medium or provenance-preserving image.**
   - Progress: a surviving `STONEAGE 初回限定版` physical-package lead is recorded as `SRC-JP-1999-RETAIL-MERCARI-01`; contemporaneous retail advertising is recorded as `SRC-JP-1999-AD-YAHOO-01`; an archived first-party Gamer's Dream product page is recorded as `SRC-JP-GD-STONEAGE-INTRO-ARCHIVE-01`.
   - Confirmed retail/client clues: package price 8,800 yen, 1999-10-15 release, CD-ROM drive requirement, 400 MB+ HDD, package purchase before Gamer's Dream registration, and installed launcher filename **`stoneage.exe`**.
   - Still missing: provenance-preserving retail disc image/dump, exact disc count, file tree, hashes, retail `stoneage.exe` PE metadata, disc matrix identifiers, product/JAN code, disc-label photos, manual/insert capture.
2. **Recover and fingerprint the archived JSS `stoneage.exe` replacement launcher.**
   - Progress: exact original JSS path is known; JSS advertised the file as 212 KB; Wayback reports two archived captures and exposes the object as binary content.
   - Current limitation: this environment has not extracted the bytes.
   - Still needed: exact byte size, SHA-256/SHA-1/MD5, PE timestamp, version resources, imports and strings; compare against any future retail-disc launcher.
3. **Determine the identity and contents of the initial-edition `STONEAGE` special CD.**
   - Progress: the special-CD claim is corroborated by contemporaneous advertising and a surviving sealed-package listing.
   - Important distinction: official package/CD-ROM requirements strengthen the case for keeping normal install media and the special CD separate as research objects until proven identical.
   - OPEN: exact contents, whether physically separate from install/client media, filesystem/audio tracks, identifiers and hashes.
4. **Locate the September 1999 beta client or reliable binary/media evidence.**
   - Progress: beta recruitment deadline is **1999-08-20** and test period **1999-09-01 through 1999-09-30**.
   - Still missing: exact application URL, recruitment page, installer/client filename, distribution method/media, hashes, internal version and beta-to-retail diff.
5. **Mine the surviving JSS/Gamer's Dream web archives for the original update protocol and 1999 paths.**
   - Progress: JSS `verup.html`, `updater.html` and `stoneage.exe` paths are now known; Gamer's Dream archive coverage begins before beta/launch.
   - Priority targets: update manifests/package names/endpoints; August 1999 beta application/tester pages; product/shop pages; registration; download/install instructions; support/version pages.
6. Recover JSS launch manual/box inserts and original world-setting text.
7. Determine the earliest documented appearance of:
   - the name "Nies / ニース / 尼斯";
   - the island-continent geography;
   - elemental/spirit lore;
   - pet riding for normal players;
   - major villages and early map topology.
8. Determine JSS-era internal numeric client version numbering.
9. Locate the earliest Taiwan client/manual/site and compare it with JSS material.
10. Locate a clean Mainland early/1.82 client/data set for later diff archaeology.

## Completed in the latest work pass

- Read and obeyed `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` from the remote repository and resumed from the highest-priority unfinished item.
- Verified repository `chinaneedM/stoneage-rebuild`, default branch `main`, and live write access.
- Inspected current remote state and commit history before continuing.
- Added and expanded `research/origin/JSS-1999-ORIGIN-EVIDENCE-R1.md`.
- Added `research/origin/GAMERSDREAM-JSS-ARCHIVE-EVIDENCE-R1.md`.
- Added `research/clients/JSS-CLIENT-VERSION-ARCHAEOLOGY-R1.md`.
- Expanded `docs/SOURCE-REGISTRY.md` with structured evidence for the March 1999 TGS showing, May 1999 design coverage, August/September beta recruitment/test window, September TGS, retail advertising, archived Gamer's Dream product page, JSS/Gamer's Dream operational boundary, JSS version-up page, JSS launcher replacement page/binary path, 2000 JSS cessation coverage, 2009 start-date retrospective and surviving first-edition package lead.
- Tightened `docs/HISTORICAL-TIMELINE.md` with sourced 1999 milestones, the active update stream beginning 1999-10-18, the confirmed `stoneage.exe` launcher filename and the 2000 operating-boundary evidence.
- Promoted resource/community/cooperative-village themes from broad hypothesis to FACT only at the narrower level of documented May 1999 pre-launch design intent.
- Recovered an original Gamer's Dream StoneAge product page from Wayback and confirmed the normal package-purchase/CD-ROM retail path.
- Recovered archived first-party Gamer's Dream notices that separate JSS client/application responsibilities from Gamer's Dream server/service/billing responsibilities.
- Recovered JSS's archived StoneAge version-up page and established that active post-launch client updates began no later than 1999-10-18.
- Recovered the original JSS launcher/update page and confirmed **`stoneage.exe`** as the installed startup-program filename.
- Located the archived JSS executable object in Wayback; byte extraction remains blocked by the current environment, so no fabricated hash or metadata has been recorded.

## Immediate next actions

1. Continue mining JSS's archived `/stoneage/` site for update manifests, patch/download filenames, automatic-update endpoints, version strings and support documentation linked to `stoneage.exe`.
2. Mine Gamer's Dream archive **backward into August-October 1999**, beginning with registration, announcements, beta/application, shop/product, support/download and StoneAge-specific paths.
3. Recover the exact **1999-08-20 beta application URL** printed in `Play Online` issue 015 and match it to a Wayback capture if possible.
4. Continue the **physical-media recovery track** using the confirmed filename `stoneage.exe`: identify product/JAN codes, standard-versus-initial-edition disc count, disc-label photographs, matrix codes, manuals/inserts and lawful provenance-preserving image/dump leads.
5. Keep the **normal retail install/client medium** and **initial-edition special CD** as separate evidence objects until direct evidence establishes their relationship.
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

The project still lacks a verified 1999 JSS retail disc image and September 1999 beta binary. However, the artifact search is now anchored to a confirmed JSS executable name (`stoneage.exe`), an original update history beginning 1999-10-18, and a surviving archived executable object. The remaining binary blocker is therefore narrower and more concrete than at session start.
