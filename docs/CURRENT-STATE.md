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
- The archived official JSS manual now confirms that the normal retail path used a StoneAge **game CD**, with DirectX 6.1 on that disc and an auto-start installer. Installation modes were standard, minimum and custom; `map` was a selectable component.
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

Precise claims are tied to `docs/SOURCE-REGISTRY.md`. Detailed research is split across:

- `research/origin/JSS-1999-ORIGIN-EVIDENCE-R1.md`
- `research/origin/GAMERSDREAM-JSS-ARCHIVE-EVIDENCE-R1.md`
- `research/clients/JSS-CLIENT-VERSION-ARCHAEOLOGY-R1.md`

### HYPOTHESIS

- The earliest StoneAge concept may have been much simpler in macro-lore than later versions, even though resource/community/village-life themes are directly attested in May 1999 design coverage.
- Much of the later macro-lore may have been progressively added to explain and extend an initially simpler world.
- Some mechanics remembered as "core StoneAge" by later players may not have existed for normal players in the earliest Japanese operation.
- The strongest current media model is that the retail package contained normal install/client media and the initial edition additionally included a separate special/bonus CD. This is **not FACT** until an original first-edition package or first-party contents list proves the disc layout.
- The updater probably used a manifest/protocol that mapped downloadable files to checksum values, but the manifest filename, checksum algorithm, endpoint and payload format remain unresolved.
- The OCR-ambiguous character immediately before `PO/sa_apply.html` could be an old-style user-directory marker such as `~`, but this remains a **search hypothesis only** and is not the registered exact beta URL.

## Highest-priority research questions

1. **Locate and verify the earliest recoverable JSS retail install/client medium or provenance-preserving image.**
   - Progress: a surviving `STONEAGE 初回限定版` physical-package lead, contemporaneous retail advertising, official Gamer's Dream product page and official JSS manual now independently constrain the artifact.
   - Confirmed retail/client anchors: normal **game CD**, physical **CD NUMBER card**, `stoneage.exe`, `ProgramFiles\jss\stoneage`, `map` install component, CD-based auto-start installer, 1999-10-15 release and 8,800-yen package price.
   - Still missing: provenance-preserving retail disc image/dump, exact disc count, file tree, hashes, retail `stoneage.exe` PE metadata, disc matrix identifiers, product/JAN code, disc-label photos and complete package/manual/insert capture.
2. **Recover and fingerprint the archived JSS `stoneage.exe` replacement launcher.**
   - Progress: exact original JSS path is known; JSS advertised the file as 212 KB; Wayback reports two archived captures and exposes the object as binary content.
   - Current limitation: this environment has not extracted the bytes.
   - Still needed: exact byte size, SHA-256/SHA-1/MD5, PE timestamp, version resources, imports and strings; compare against any future retail-disc launcher.
3. **Recover the automatic-update manifest/protocol and payload naming.**
   - Progress: updater anchors now include `data\download`, `cksum:xxxxxxxxx`, `MFC42.DLL`, Windows Temporary Internet Files/proxy behavior and `stoneage.exe`.
   - Still needed: manifest/config filename, update host/path, checksum algorithm, payload filenames/extensions and whether whole files or deltas were delivered.
4. **Determine the identity and contents of the initial-edition `STONEAGE` special CD.**
   - Progress: the special-CD claim is corroborated by contemporaneous advertising and a surviving sealed-package listing; the official manual separately confirms a normal game CD.
   - OPEN: exact contents, whether physically separate from install/client media, filesystem/audio tracks, identifiers and hashes.
5. **Locate the September 1999 beta client or reliable binary/media evidence.**
   - Progress: beta recruitment deadline is **1999-08-20** and test period **1999-09-01 through 1999-09-30**; official FAQ confirms that data from an earlier StoneAge test could persist under `ProgramFiles\jss\stoneage`; the printed application URL is narrowed to host `www.dp.gamersdream.ne.jp` with path tail `PO/sa_apply.html`.
   - Still missing: the single OCR-ambiguous character before `PO`, an archived copy of the application page, tester/download instructions, installer/client filename, distribution method/media, hashes, internal version and beta-to-retail diff.
6. **Mine the surviving JSS/Gamer's Dream web archives for 1999 paths and support/update artifacts.**
   - Progress: JSS `manual.html`, `manual01.html`, `faqstart.html`, `verup.html`, `updater.html` and `stoneage.exe` paths are known; Gamer's Dream archive coverage begins before beta/launch; beta application matching can now target `*PO/sa_apply.html` rather than the whole domain.
   - Priority targets: update manifests/package names/endpoints; the exact August 1999 beta application capture and sibling tester/download pages; product/shop pages; registration; download/install instructions; support/version pages.
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

- Re-read the latest remote `main` before continuing and detected that the repository had advanced beyond the prior chat checkpoint; resumed from the newer GitHub state rather than stale chat memory.
- Expanded `research/origin/GAMERSDREAM-JSS-ARCHIVE-EVIDENCE-R1.md` with the newly recovered beta-application URL evidence.
- Recovered, from searchable text extraction of the preserved 1999 *Play Online* issue, the beta application's **Gamer's Dream host** `www.dp.gamersdream.ne.jp` and path tail **`PO/sa_apply.html`**.
- Explicitly preserved the unresolved character immediately before `PO` as OCR ambiguity instead of silently converting it to `~`, `/` or another character.
- Narrowed the next Wayback search target from the whole Gamer's Dream domain to archived paths matching **`*PO/sa_apply.html`** and sibling beta/tester/download resources.
- Previously recovered retail/install/update anchors remain authoritative: normal game CD, CD NUMBER card, `stoneage.exe`, `ProgramFiles\jss\stoneage`, `data\download`, `cksum:xxxxxxxxx`, `MFC42.DLL`, archived launcher path and update history beginning 1999-10-18.

## Immediate next actions

1. Resolve the one OCR-ambiguous character in the beta application URL and match **`*PO/sa_apply.html`** to an August 1999 Wayback capture if one exists; then enumerate sibling paths and links for tester instructions/client delivery.
2. Mine archived JSS pages and paths using the concrete strings `data/download`, `cksum`, `MFC42.DLL`, `ProgramFiles/jss/stoneage`, `map` and `stoneage.exe` to recover manifest/config/payload names and update-server URLs.
3. Continue the **physical-media recovery track** using the confirmed normal game CD and CD NUMBER card: identify product/JAN codes, standard-versus-initial-edition disc count, disc-label photographs, matrix codes, manuals/inserts and lawful provenance-preserving image/dump leads.
4. Keep the **normal retail game CD** and **initial-edition special CD** as separate evidence objects until direct evidence establishes their relationship.
5. If the archived JSS launcher bytes become obtainable, analyze them outside the repository and record only hashes/metadata/derived findings.
6. Once any original retail/beta binary or media is recovered, establish the reproducible client-archaeology pipeline: hashes, PE metadata, file tree, resource inventory, strings, asset IDs, update-state labeling and cross-version diff.

## Continuity status

- Repository: `chinaneedM/stoneage-rebuild`
- Default branch: `main`
- Visibility: public
- Authority: latest GitHub remote state is the single source of truth for project continuity.
- Canonical restart protocol: `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`

## Blockers

No repository or workflow blocker.

The project still lacks a verified 1999 JSS retail disc image and September 1999 beta binary. The beta web-recovery blocker has nevertheless narrowed materially: the application page is now anchored to `www.dp.gamersdream.ne.jp` and the path tail `PO/sa_apply.html`, with only one preceding character still unresolved from the indexed scan. The binary/media blocker remains the principal Phase 0 constraint.
