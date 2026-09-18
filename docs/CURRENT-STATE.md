# Current State

Last updated: 2026-09-18

## Current phase

**Phase 0 — Earliest Clean Client Recovery & Reverse Engineering**

The independent GitHub repository and continuity scaffold are established on remote `main`. The operational objective is now explicit: recover the **earliest freely/publicly obtainable, provenance-preserving and minimally modified StoneAge client / installer / complete file tree**, verify it at file level, then use it as the primary reverse-engineering specimen for reconstructing the game's systems and data.

Historical archaeology remains useful only when it helps authenticate, date, compare, or interpret a recovered client. Package price, retail product-number, staff-history, and similar research are **not primary objectives** unless they directly improve client recovery or technical attribution.

## Confirmed project direction

- **Primary path: recover the earliest clean client first, then reverse engineer it.**
- "Clean client" means an original/operator-distributed or otherwise provenance-preserving client, installer, disc image, or complete file tree with no known private-server repack, injected launcher, custom patcher, replaced assets, or undocumented modification. If absolute purity cannot be proven, candidates must be graded and compared rather than silently accepted.
- Search priority is **earliest freely/publicly obtainable artifact**, not the historically earliest version at any cost. If a 1999 JSS client is unavailable but a later clean 1.74/1.74a/Taiwan/early-Mainland client is recoverable, use the earliest verified available artifact as a bridge specimen and continue diffing backward when older material appears.
- Once a usable client is recovered, priority immediately shifts from historical research to technical extraction: file tree, hashes, executable metadata, resource/container formats, maps, characters, pets, attributes, skills, items, UI, text tables, animation/sprite indexes, update/runtime structure, and other deterministic game data.
- Single-player game, not a commercial MMORPG operation.
- Historical clients and materials are research samples, not code/assets to copy directly into the new game.
- **Research must not depend on the user buying or manually acquiring physical material.** No bidding, purchasing, shipping, opening, installing, or personally dumping original discs/packages is part of the project plan. Auction/marketplace pages are evidence surfaces only; free/public digital recovery is the operational path.
- Start from the earliest traceable JSS-era StoneAge rather than assuming Mainland China 1.82 is the absolute origin.
- Mainland 1.82 remains a major reference point because it is close to the user's childhood experience and is commonly remembered as a classic early form.
- Later systems/content may ultimately be integrated, but through coherent progression rather than a feature dump.
- Emotional milestones such as first pet capture, first ride, first major exploration, etc. are part of the design target.

## Future reconstruction note — historical automation and scripting

- The user's long-term original play experience is preserved as **DESIGN input**: late-game StoneAge progression could become impractically slow if every repeated encounter used only the full manual turn-based battle flow, while third-party fast-battle/automation tools and community-authored scripts became an important part of actual player practice.
- This does **not** change the current clean-client standard. Official runtime/resources and third-party automation remain separated during archaeology.
- When reconstruction begins, progression pacing, encounter frequency, battle duration, fast battle/auto-battle, and a possible official sandboxed scripting system must be evaluated together rather than assuming either "copy the grind exactly" or "remove the grind completely."
- The implementation decision is deliberately deferred until real client/data analysis exposes the underlying progression and combat structure.
- Canonical design record: `DD-010`.

## Latest clean-client correction — 2026-09-18

- **Version labels are not byte provenance.** A server/download label such as "1.82" must not be promoted to a client-build fact until the installer/file tree/executable is recovered and inspected.
- A contemporaneous Beijing Wayi statement materially changes the Sina interpretation: its 2003 anniversary **1.82 server** accepted the then-current `宠物进化史` client, so the Sina `1.82 安装包` label is now a TARGET-B recovery clue rather than an assumed 2001 1.82 baseline.
- Korean `1.74` and Japanese `1.74a` are now prioritized because each has contemporaneous operator-era/free-distribution evidence tied to an explicit client/service version.
- No 1.74, 1.74a or Sina-labelled "1.82" installer bytes have yet been recovered; therefore no clean-client bridge specimen has yet been accepted.

## New 2.5 byte-recovery path — 2026-09-18

- Recovered a public preservation thread for a **StoneAge 2.5 client + server + login-tool bundle** with two exact MediaFire IDs and an explicit archive layout containing a separate `SA2.5主程式` directory. A 2012 follow-up confirms the two files were successfully re-uploaded and downloadable at that time.
- This combined bundle is **not accepted as clean**: the thread itself distinguishes the main client from private-server tooling, and a user explicitly noted that many circulating 2.5 copies were modified. If recovered, only the isolated client directory will be evaluated and it must pass contamination checks.
- Found a separate indexed preservation thread titled **`〖2.5纯净〗石器客户端`** (`tid=2132`). Its title makes it the highest-value current 2.5 lead, but the download body is still access-restricted; `纯净` is a source label, not yet a verified conclusion.
- Found a later **Wayi official 8.5 client** preservation set with six exact MediaFire IDs. It is too late for the preferred bridge baseline but is valuable as a clean later control.
- Found the exact Korean preservation token **`NetmarbleStoneAge120`** (`tid=2117`). Its version is not yet tied to Korean 1.74, so it remains a later Korean control/search key.
- Operational strategy is now dual-track: pursue **actual 2.5 bytes immediately** because they may be recoverable sooner, while continuing the earlier and better-provenanced Korean 1.74 / Japanese 1.74a searches in parallel.

## Active clean-client recovery leads — 2026-09-18

- **Korean 1.74 — TARGET-A:** a preserved 2003-07-21 Netmarble-era response explicitly gives the service start as 2003-07-28 and the version as `1.74`. The original installer/file tree/hash is not yet recovered, but this is now the strongest exact operator-era bridge-version target.
- **Japanese 1.74a — TARGET-A:** contemporaneous Mado no Mori metadata identifies `1.74a` dated 2003-12-12 as a free beta client, and 4Gamer independently records official-site client pre-download beginning on 2003-12-12 before open beta. Installer identity/bytes remain unrecovered.
- **Mainland "1.82" / Sina period mirror — TARGET-B pending byte verification:** Sina's historical download page has an explicit `石器时代1.82客户端下载` / `安装包` label, but a contemporaneous Beijing Wayi statement says its 2003 anniversary 1.82 server could be entered with the then-current `宠物进化史` client. Therefore the page label is not proof of an original 1.82 client build; href/bytes remain useful only as a candidate to identify by file-level analysis.
- **JSS `stoneage.exe` — TARGET-A partial artifact:** exact first-party path is known, but binary extraction remains blocked.

Canonical recovery ledger: `docs/SOURCE-REGISTRY-CLIENT-RECOVERY-R1.md`.

## Priority reset — 2026-09-18

The user reconfirmed the original project method: **find the earliest free clean client we can actually obtain, understand how the game is built from its real files, and then reconstruct it with modern technology**.

Consequences:
- historical chronology is subordinate to artifact recovery;
- product-price/package archaeology is paused;
- a later but clean and freely obtainable client is more operationally valuable than an earlier version known only from articles;
- reverse engineering begins as soon as a sufficiently trustworthy client artifact is recovered;
- the project should progressively reconstruct the whole game model from real data: maps, characters, attributes, skills, pets, items, UI, resources, update/runtime structure and other systems.

## Current historical working picture

### FACT / high-confidence working facts

- StoneAge was developed by Japan System Supply (JSS).
- `STONEAGE` was publicly exhibited at Tokyo Game Show '99 Spring by **1999-03-19** in NTT Data's Gamer's Dream booth.
- Wayback reports archived captures of the original Gamer's Dream index beginning **1999-04-22**, so the pre-beta/pre-launch web layer is at least partially recoverable.
- By May 1999, contemporaneous `Play Online` coverage described the planned game as a relaxed Stone Age RPG emphasizing food/resources, community, cooperative village development, and intended life/resource activities including **hunting, gathering and farming**. The same pre-launch coverage frames the design as trying to minimize the usual online-game focus on fighting, destroying and taking from others. These are FACTS for **published pre-launch design intent**, not automatic proof that every mechanic shipped in the September beta or October retail build.
- Beta recruitment closed **1999-08-20**; the beta itself ran **1999-09-01 through 1999-09-30**, supported by contemporaneous `Play Online` issue 015.
- The preserved `Play Online` issue 015 is now searchable deeply enough to recover the beta-application URL host as `www.dp.gamersdream.ne.jp` and its path tail as `PO/sa_apply.html`. One character immediately before `PO` remains OCR-ambiguous and is **not** normalized or guessed in the factual record.
- PC Watch reported on 1999-09-17 that the JSS title was scheduled for release on **1999-10-15**.
- A photographed period retail advertisement gives Windows 95/98 as platform, **1999-10-15** as scheduled release date, **8,800 yen before tax** as planned price, and prints the period domains `www.titan.co.jp` and `www.gamersdream.ne.jp`.
- The same advertisement visibly promotes an original mug as a reservation bonus and a `STONEAGE` special CD as an initial-edition bonus/feature.
- An archived first-party Gamer's Dream StoneAge product page independently lists **1999-10-15** as release date, package price 8,800 yen, a 4x or faster CD-ROM drive, at least 400 MB HDD, 64 MB RAM, MMX Pentium 200 MHz+, 33.6 Kbps+ Internet access, 2 MB+ VRAM, DirectX 6.1-compatible video/sound, mouse and keyboard.
- The same first-party product page tells users to **purchase the software package first and then register for Gamer's Dream service**, materially confirming a normal package-based install/client path.
- The archived official JSS manual confirms that the normal retail path used a StoneAge **game CD**, with DirectX 6.1 on that disc and an auto-start installer. Installation modes were standard, minimum and custom; `map` was a selectable component.
- The same JSS manual confirms a physical **CD NUMBER card** whose CD NUMBER was required for Gamer's Dream service registration/contracting. The manual also documents `[Stoneage]` -> `[stoneage]` as the Start-menu path and a `screenshot` subdirectory under the StoneAge folder.
- JSS product-identifier archaeology now has three directly grounded Windows online-RPG JAN anchors. **LIFESTORM** is cataloged as model **`JV02005`**, JAN **`4909476301016`**; surviving package photographs directly expose **LIFESTORM II JAN `4909476302013`** and early JSS **STONEAGE JAN `4909476303010`**. The StoneAge value is read from a preserved Yahoo! Auctions back-box photograph, so it is no longer a numerical candidate. LIFESTORM II and StoneAge model/type codes remain unresolved. Other JSS-associated Windows products occupy different `4909476...` subranges, so the observed `30101 → 30201 → 30301` run is recorded as product evidence rather than generalized into an undocumented numbering rule.
- A later collector-photo set now visibly depicts an early JSS/Gamer's Dream `STONEAGE` box/manual together with **two separate optical discs**. Because the project has not directly inspected the object or established an unbroken provenance chain, this is not S-grade package proof; however, combined with the first-party game-CD manual and contemporaneous bonus-CD advertising, it materially strengthens the separate game-CD + bonus-CD model.
- The same community article is not reliable as a blanket provenance source: its second Japanese package is visibly branded **BOTHTEC / DigiPark** and supports Windows 98SE/Me/2000/XP, despite wording that implies both packages are JSS-issued. Artifact-level visual evidence therefore takes precedence over that caption.
- A later first-person professional profile by **Yuki Tamura** states JSS employment from **May 1996 through October 2000**, role `3D Artist`, and explicitly lists **StoneAge** among JSS projects. Preserved 1997 JSS `Chameleon Twist` credits independently list Yuki Tamura under **Computer Arts** and **Game Design**, materially corroborating the named person's JSS identity. This is strong later staff evidence, not a contemporaneous StoneAge staff-credit list.
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
- A near-contemporary 2003 4Gamer revival report states that in the former Japanese StoneAge operation **only GMs could ride dinosaurs**. This is B-level retrospective baseline evidence rather than 1999 primary documentation, but it materially narrows the working original-Japanese baseline: **normal-player pet riding is treated as absent unless stronger JSS evidence contradicts it**.
- At TGS 2003, revival staff told 4Gamer that the immediate restored game was **basically the same** as the former version and was then focused on restoration/bug fixing. The same report identifies a dedicated **item trade window as a minor change that the original did not have**, with ground-drop exchange described as the older context. This creates a controlled JSS→2003 UI/mechanics diff anchor.
- Version-lineage archaeology now has two concrete near-descendant anchors: a contemporaneously preserved Netmarble answer identifies its **2003 Korean launch as version `1.74`**, while Mado no Mori's contemporary Japanese revival metadata identifies the **2003-12-12 Japanese beta client as `1.74a`**. The numeric proximity makes a shared/related version lineage a high-value **HYPOTHESIS and recovery target**, but does not establish identical binaries, regional data parity, or that `1.74` was JSS's final internal version.

Precise first-party claims are tied to `docs/SOURCE-REGISTRY.md`. Detailed research is split across:

- `research/origin/JSS-1999-ORIGIN-EVIDENCE-R1.md`
- `research/origin/GAMERSDREAM-JSS-ARCHIVE-EVIDENCE-R1.md`
- `research/origin/JSS-DEVELOPER-RECOLLECTION-LINEAGE-R1.md`
- `research/origin/JSS-NAMED-STAFF-EVIDENCE-R1.md`
- `research/clients/JSS-CLIENT-VERSION-ARCHAEOLOGY-R1.md`
- `research/clients/JSS-RETAIL-PACKAGE-PHOTO-EVIDENCE-R1.md`
- `research/clients/DESCENDANT-CLIENT-SOURCE-LINEAGE-R1.md` — explicitly lower-confidence later-source lineage clues, not 1999 JSS facts.
- `research/clients/STONEAGE-EXE-NEGATIVE-CONTROLS-R1.md` — fingerprints later same-name executables so false positives are excluded before JSS provenance analysis.
- `research/clients/JSS-PRODUCT-IDENTIFIER-ARCHAEOLOGY-R1.md` — reconstructs JSS JAN/model-number families to narrow the 1999 StoneAge retail-package search without assigning inferred identifiers.
- `research/clients/JSS-RESOURCE-CONTAINER-LINEAGE-R1.md` — tests the possible LIFESTORM II → StoneAge JSS resource-pipeline ancestry through REAL/ADRN filenames, index semantics and the StoneAge `RD` run-length/literal codec.
- `research/evolution/JSS-TO-2003-REVIVAL-DELTA-R1.md` — uses the earliest Japanese revival as a near-descendant comparison anchor to separate original-Japanese mechanics from 2003 UI/content additions.
- `research/evolution/STONEAGE-174-VERSION-LINEAGE-R1.md` — isolates Korean `1.74` and Japanese revival `1.74a` as controlled early-client recovery targets without assuming numerical equality means byte/content identity.

Supplemental source ledgers:

- `docs/SOURCE-REGISTRY-DEVELOPER-RECOLLECTIONS-R1.md`
- `docs/SOURCE-REGISTRY-NAMED-STAFF-R1.md`
- `docs/SOURCE-REGISTRY-PHYSICAL-MEDIA-R1.md`
- `docs/SOURCE-REGISTRY-PRESERVATION-CONTROLS-R1.md`
- `docs/SOURCE-REGISTRY-JSS-PRODUCT-IDENTIFIERS-R1.md`
- `docs/SOURCE-REGISTRY-RESOURCE-CONTAINERS-R1.md`

### HYPOTHESIS / lower-confidence search leads

- The earliest StoneAge concept may have been much simpler in macro-lore than later versions, even though resource/community/village-life themes are directly attested in May 1999 design coverage.
- Much of the later macro-lore may have been progressively added to explain and extend an initially simpler world.
- Some mechanics remembered as "core StoneAge" by later players may not have existed for normal players in the earliest Japanese operation.
- The strongest current media model is now **strongly corroborated but not S-grade**: the 1999 initial-edition retail package likely contained a normal game/install CD and a physically separate special/bonus CD. The collector photograph visibly depicts two discs beside the early JSS box/manual, but direct inspection or first-party package-contents documentation is still required before the exact layout is promoted to unqualified FACT.
- The earlier product-number hypothesis has been resolved for the three online-RPG packages: direct catalog/package evidence now binds LIFESTORM `4909476301016`, LIFESTORM II `4909476302013`, and STONEAGE `4909476303010`. The remaining identifier uncertainty is the missing LIFESTORM II/StoneAge **model/type codes**; no further JAN sequence is inferred beyond observed products.
- **New technical lineage lead:** later LIFESTORM II preservation material names `adrn_1.bin` as an image-address file and `real_1.bin` as an image-data file. Later StoneAge source lineages independently preserve an ADRN index / REAL image-data architecture with a concrete `RD` block header and custom run-length/literal decoder. This makes a shared JSS-era resource pipeline plausible, but the LIFESTORM II bytes have not been recovered and the StoneAge editor reportedly failed to align those LIFESTORM II files. Keep this as **HYPOTHESIS**, not engine-reuse fact.
- **CrossGate technical-format corroboration:** an older preserved technical article and multiple modern CrossGate parsers independently converge on the same 16-byte `RD` block layout and nine-class RLE control scheme seen in the StoneAge descendant encoder/decoder family. This materially strengthens a shared JSS-era image-resource codec lineage. It does **not** establish which title introduced it or prove LIFESTORM II compatibility.
- **LS2MAP correction:** `LS2MAP` is observed in later StoneAge/CrossGate **server-map** code/tooling. Older client-format documentation describes client maps differently, so `LS2MAP` must not be used as proof of the original client map format or expanded to “LIFESTORM II MAP” without direct evidence.
- The updater probably used a manifest/protocol that mapped downloadable files to checksum values, but the manifest filename, checksum algorithm, endpoint and payload format remain unresolved.
- The OCR-ambiguous character immediately before `PO/sa_apply.html` could be an old-style user-directory marker such as `~`, but this remains a **search hypothesis only** and is not the registered exact beta URL.
- Multiple later community-preserved client-source trees retain JSS/Gamer's Dream title identifiers and updater-related traits, but the traits are now weighted separately. **`CheckForUpdate`** survives in BismarckDD, Signally and anson1788 client trees despite differing startup/build architecture, making it the strongest descendant updater-coordination search fingerprint. **`sa.exe`** is explicit in Signally and anson1788 project/debug metadata and is independently named by later Taiwan `cksum:...:File:sa.exe` failures, keeping it a high-value runtime candidate without establishing 1999 use. Signally's `updated` + user-facing `StoneAge.exe` launcher gate is narrower, and its conditional `PARAM_ARGS = "HASH___________@@@@@@@@"` placeholder is currently branch-specific/low-priority rather than a generic JSS hypothesis.
- **Version-lineage bridge:** Korean `1.74` and Japanese revival `1.74a` are now independently documented historical version labels. Their relationship to one another—and to the last JSS client—is **OPEN**. Treat them as high-value bridge artifacts for recovery/diffing, not substitutes for the 1999 retail/beta baseline.
- **Yuki Tamura** is now a plausible named candidate for at least part of the StoneAge 3D art/animation role described in the preserved anonymous project-leader recollections because Tamura self-reports JSS 3D art work and StoneAge participation. This remains **HYPOTHESIS**, not an identification of the recollection's unnamed `3D animator`.

## Highest-priority research questions

1. **Locate and verify the earliest recoverable JSS retail install/client medium or provenance-preserving image.**
   - Progress: contemporaneous retail advertising, official Gamer's Dream product page, official JSS manual, a later collector-photo set and a surviving Mercari initial-edition listing now independently constrain the artifact.
   - The collector photo visibly shows an early JSS box/manual with **two separate optical discs**, materially corroborating the game-CD + bonus-CD model while remaining below S-grade provenance.
   - The Mercari listing is now confirmed **sold**, but its live page exposes all **13 exact original-image URLs** and explicitly states that the unopened initial edition contains an initial-edition bonus CD-ROM. Those thirteen image targets are preserved in `docs/SOURCE-REGISTRY-PHYSICAL-MEDIA-R1.md`; their image bodies remain inaccessible through the current extraction path.
   - Confirmed JSS retail/client anchors: normal **game CD**, physical **CD NUMBER card**, `stoneage.exe`, `ProgramFiles\jss\stoneage`, `map` install component, CD-based auto-start installer, 1999-10-15 release and 8,800-yen package price.
   - Search lead from descendant lineages: inspect recovered media for `sa.exe` separately from `stoneage.exe`, plus `updated` and `CheckForUpdate`; these are not yet confirmed JSS-1999 strings.
   - Product-identifier progress: JSS Windows `LIFESTORM` is cataloged as `JV02005` / JAN `4909476301016`; public package photographs now directly fix **LIFESTORM II JAN `4909476302013`** and **STONEAGE JAN `4909476303010`**. The StoneAge evidence comes from Yahoo! Auctions listing `k1131932809`, whose preserved early JSS package-back photo exposes the barcode. LIFESTORM II and StoneAge model/type codes remain unresolved.
   - Still missing: S-grade confirmation of the two-disc identities/layout, provenance-preserving retail disc image/dump, file tree, hashes, retail executable PE metadata, **StoneAge model/type code**, readable disc-label/matrix identifiers and complete package/manual/insert capture.
2. **Recover and fingerprint the archived JSS `stoneage.exe` replacement launcher.**
   - Progress: exact original JSS path is known; JSS advertised the file as 212 KB; Wayback reports two archived captures and exposes the object as binary content.
   - Current limitation: this environment has not extracted the bytes.
   - A known later false-positive `StoneAge.exe` is now fingerprinted and excluded: SHA-256 `9C019D9FAB9C0DC37A37A67519CA5080AE43EC2B2A84B915A24B742512A6A7CA` (2019 PE timestamp; 2010 copyright resource; Simplified-Chinese product metadata; `OriginalFileName=Sa.exe`).
   - Still needed: exact JSS byte size, SHA-256/SHA-1/MD5, PE timestamp, version resources, imports and strings; test `sa.exe`, `updated`, and `CheckForUpdate` independently rather than assuming they form one inseparable descendant architecture.
3. **Recover the automatic-update manifest/protocol and payload naming.**
   - Progress: first-party updater anchors include `data\download`, `cksum:xxxxxxxxx`, `MFC42.DLL`, Windows Temporary Internet Files/proxy behavior and `stoneage.exe`. Much later Taiwan troubleshooting records a descendant checksum error targeting `sa.exe`, showing that filename-bearing `cksum` records existed in a later lineage.
   - Still needed from JSS evidence: manifest/config filename, update host/path, checksum algorithm, payload filenames/extensions, the original `cksum` record structure and whether whole files or deltas were delivered.
4. **Determine the identity and contents of the initial-edition `STONEAGE` special CD.**
   - Progress: contemporaneous advertising proves the bonus-CD offer; the official manual separately proves a normal game CD; a later physical-package photograph depicts two separate discs alongside the early JSS box/manual; the sold Mercari initial-edition listing independently states that a bonus CD-ROM is included and exposes thirteen original-photo targets.
   - OPEN: S-grade confirmation that the photographed second disc is the advertised bonus CD, exact disc label/matrix identifier, filesystem/audio tracks, contents and hashes.
5. **Locate the September 1999 beta client or reliable binary/media evidence.**
   - Progress: beta recruitment deadline is **1999-08-20** and test period **1999-09-01 through 1999-09-30**; official FAQ confirms that data from an earlier StoneAge test could persist under `ProgramFiles\jss\stoneage`; the printed application URL is narrowed to host `www.dp.gamersdream.ne.jp` with path tail `PO/sa_apply.html`.
   - A second preservation path is now registered: Retromags independently catalogs `Play Online No.015 (September 1999)` (submitted 2023-12-14). It is a second scan route, not an independent historical source. The current extraction layer cannot yet fetch the file-detail/download body for visual comparison.
   - Still missing: the single OCR-ambiguous character before `PO`, an archived copy of the application page, tester/download instructions, installer/client filename, distribution method/media, hashes, internal version and beta-to-retail diff.
6. **Test the LIFESTORM II → StoneAge REAL/ADRN resource-lineage hypothesis using free/public evidence.**
   - Progress: LIFESTORM II community preservation names `adrn_1.bin` / `real_1.bin` with address-data / image-data roles; two StoneAge descendant source trees preserve the same conceptual split, a concrete ADRN record structure, `RD` image-block signature, and matching legacy run-length/literal decoder implementation. A public StoneAge sample reverse engineering independently reports **80-byte ADRN records** beginning with image/file number, REAL offset and block length; the descendant source's Win32 layout independently totals the same 80 bytes. Separately, older CrossGate/StoneAge technical documentation plus three modern CrossGate decoder implementations converge on the same 16-byte `RD` header and nine-class RLE scheme, strongly corroborating a shared image-codec family.
   - Current limitation: the old free ASUS WebStorage backup links are unreachable from the present environment, so no LIFESTORM II byte-level validation has been performed. `LS2MAP` has now been separated as a later **server-map** format lineage and is not treated as evidence for LIFESTORM II client data.
   - Next proof target: a freely retrievable LIFESTORM II data copy or equivalent historical bytes; test `RD` headers and decoder compatibility separately from ADRN/map-index compatibility.
7. **Mine the surviving JSS/Gamer's Dream web archives for 1999 paths and support/update artifacts.**
   - Progress: JSS `manual.html`, `manual01.html`, `faqstart.html`, `verup.html`, `updater.html` and `stoneage.exe` paths are known; Gamer's Dream archive coverage begins before beta/launch; beta application matching can now target `*PO/sa_apply.html` rather than the whole domain.
   - Priority targets: update manifests/package names/endpoints; the exact August 1999 beta application capture and sibling tester/download pages; product/shop pages; registration; download/install instructions; support/version pages; any original occurrence of `sa.exe`, `updated` or `CheckForUpdate`.
8. Recover JSS launch box/manual inserts and original world-setting text not already represented by the archived online manual.
9. Determine the earliest documented appearance of:
   - the name "Nies / ニース / 尼斯";
   - the island-continent geography;
   - elemental/spirit lore;
   - normal-player pet riding: **working Japanese-original boundary now narrowed** — 2003 near-contemporary 4Gamer evidence says the former Japanese service allowed dinosaur riding only for GMs; still seek primary JSS confirmation and the earliest regional/build appearance of normal-player riding;
   - major villages and early map topology.
10. **Determine JSS-era internal numeric client version numbering and resolve the new `1.74 / 1.74a` bridge.**
   - Progress: Korean Netmarble launch evidence explicitly names `1.74`; contemporary Japanese revival metadata explicitly names `1.74a`.
   - OPEN: whether either label descends directly from a JSS version number, whether the Japanese/Korean builds share a code/data branch, and what the 1999 retail / 2000 final-JSS internal versions were.
   - Recovery target: authentic/public Korean `1.74` or Japanese `1.74a` installer/file tree for external hashing and controlled diffing.
11. Locate the earliest Taiwan client/manual/site and compare it with JSS material.
12. Locate a clean Mainland early/1.82 client/data set for later diff archaeology.
13. **Recover an original StoneAge staff-credit list and resolve named JSS roles.**
   - Progress: Yuki Tamura is now a named later first-person StoneAge/JSS staff lead with independent JSS-credit corroboration on `Chameleon Twist`; Hiroyuki Morioka remains a strong but unresolved project-leader identity hypothesis derived from the anonymous recollection lineage and `Chameleon Twist 2` credits.
   - Still needed: original StoneAge credits, staff page, period interview, or project-specific first-person statements that assign exact roles.

## Completed in the latest work pass
- Closed the main **ADRN-unresolved DAT graphic-ID** question for this mixed bundle. All **158,938 tile** and **48,707 parts** unresolved references fall inside the recovered ADRN `bmpnumber` domain 100–41000; they are namespace holes rather than simple IDs beyond the resource maximum.
- Localized the missing-resource problem: **`817.dat` alone contributes 82.52% of unresolved tile refs and 89.49% of unresolved parts refs**. Its event layer is normal, but the bundled server corpus contains **no LS2MAP map ID 817**.
- Cross-linked that byte evidence to descendant source: floor 817 is grouped with 8007/8015/8027/8028/8029/8100/8101 in `_STATUS_WATERWORD`, `_NEWDRAWBATTLEMAP` and `_AniCrossFrame` branches. Several of those same floors also have missing graphics in the recovered DAT corpus. Current classification is **mixed/cross-revision content-resource skew**, not a DAT-format defect.
- Identified the dominant missing ranges: tile **5150–5421** (272 consecutive IDs / 133,014 refs) plus smaller early map ranges; parts gaps cluster heavily through the **11xxx** namespace. Exact source version remains OPEN.
- Completed a recovered **DAT ↔ server LS2MAP static-layer crosscheck**: 637 numeric DAT caches have same-ID/same-dimension server maps; **280** match both static layers exactly, **421** match tile exactly, and **361** match parts/object exactly. This strongly corroborates server `tile / obj` → client `tile / parts` while proving the mixed bundle contains multiple map revisions.
- Closed the main `1021.DAT` diagnosis boundary: its same-ID 407×144 server map differs in **39,456 tile cells** and **32,706 parts/object cells**, while DAT also contains **43,952 non-enum event cells**. It is therefore not an event-only hidden encoding; the whole cache is quarantined as a stale/different/modified revision-source anomaly pending a clean specimen.
- Traced descendant-source sub-100 DAT controls: collision codes `1,2,5,6,9,10` and `4`; effective environment tones **20–37**; base-branch map BGM **40–53** (54–55 later macro); and **60–79** as special collision-resolved IDs rather than ordinary rendered graphics.
- Completed the first full **DAT runtime-semantics pass** on the entire case-insensitive recovered corpus: **1,011 DAT files = 995 normal three-layer caches + 16 special/invalid normal-parser entries**, covering **8,354,525 cells**.
- Resolved the descendant client/server map-data chain: server `tile / obj / CHAR_WORKEVENTTYPE` is serialized to client `tile / parts / event`; the client persists it in `map\\%d.dat`, adds local read/see flag bits, and refreshes rectangles from the server on checksum mismatch.
- Resolved the collision boundary: DAT contains no fourth hit layer. The client derives `hitMap` from tile/parts graphic attributes and parts footprints plus event occupancy, while the server independently evaluates authoritative tile/object walkability.
- Cross-checked recovered DAT graphic references against `adrn_15.bin`: **3,599,419 / 3,758,357 tile graphic references (95.77%)** and **277,037 / 325,744 parts graphic references (85.05%)** resolve through recovered `attr.bmpnumber`; unresolved IDs remain explicit version/resource-lineage evidence.
- Isolated the event anomaly instead of expanding the event model: **994 of 995 valid DAT caches contain only low-12 event values 0–8**; every one of the **43,952** non-enum cells occurs in **`1021.DAT` (407×144)**. That file is now quarantined for corruption/version/private-server analysis.
- Added `research/clients/STONEAGE-25-DAT-RUNTIME-SEMANTICS-R1.md`, promoted the DAT and completed SPR findings into `STONEAGE-25-VERIFIED-RESOURCE-FORMATS-R1.md`, and refreshed the archaeology-tool index.
- Completed the recovered SPR/SPRADRN structural pass: all **847** 12-byte SPRADRN records parse successfully; frame references overwhelmingly resolve directly into the recovered ADRN bitmap index, with explicit `0xffffffff` sentinel frames retained rather than coerced.
- Corrected recovered map provenance. `stoneage2.5/map` contains **1,030 MAP + 1,011 DAT**, not 2,041 MAP files. Cross-hash analysis against `SACH-MX0.30/MAP` finds **1,008 same-name maps, 905 byte-identical same-name files, and 910 client-directory MAP hashes present anywhere in the SACH corpus**. The one-layer MAP family is therefore reclassified as **external-tool/SACH-coupled**, not clean-client map evidence.
- Descendant client source independently establishes `map\\%d.dat` as the client runtime map cache with three `uint16` layers: **tile / parts / event**. Reverse-engineering priority now moves to those DAT layer semantics and their rendering/collision/network roles.
- Promoted the recovered 2.5 resource work from structural inference to **real-byte validation**: `adrn_15.bin` is exactly 234,564 × 80-byte records; every record points to an in-bounds `RD` block in `real_15.bin`; the blocks are fully contiguous with zero gaps/overlaps and cover the entire REAL payload.
- Validated the independently written legacy RD decoder against **4,225 real client blocks with 4,225 successes and 0 failures**, including all eight raw `flag=0` blocks. Those eight confirm the historical raw-branch quirk: ADRN size is authoritative while the RD header size field is not a true block length.
- Verified all **1,030** recovered single-layer `.MAP` files use `uint32 width + uint32 height + one uint16 per cell`, but their provenance is now corrected: they are strongly coupled to the bundled SACH external-tool corpus and are **not promoted as official client-map format evidence**.
- Separated the recovered map families. The directory contains **1,030 MAP + 1,011 DAT** files; descendant source establishes DAT as a three-layer `tile / parts / event` client runtime-cache structure. Byte-level MAP↔DAT comparison found **995 valid same-stem pairs and zero cases where MAP equals DAT tile, parts or event**, which is now expected because they belong to different technical layers.
- Completed full SPR/SPRADRN validation: `spradrn_5.bin` is exactly **10,164 bytes = 847 × 12-byte records**, all 847 parse successfully, and the recovered frame stream links back into ADRN at large scale.
- **Recovered and hash-verified the preserved two-part StoneAge 2.5 bundle** through GitHub Actions. MediaFire hashes match the downloaded bytes; the reassembled 361,255,180-byte RAR was extracted successfully and a 29,845-line derived static inventory was committed without committing proprietary payloads.
- Classified the recovered 2.5 package as **RECOVERED-C for runtime / B-grade for resource archaeology**. The core `stoneage2.5` tree contains 2,302 files / ~863 MB, including `real_15.bin` (~764 MB), `adrn_15.bin` (~18.8 MB), SPR/sound containers and 2,041 map-related files (1,030 MAP + 1,011 DAT).
- Found direct runtime contamination evidence: `sa_2903.exe` and `sa_2903网通.exe` contain fixed server IPs plus `cary` / `12345678` community-lineage strings. They are negative controls, not clean-version proof. A separate `StoneAge.exe` contains Wayi/WGS/stoneage.com.cn operator-era URLs and is retained as a plausible operator-launcher component pending cross-copy verification.
- Separated the unrelated `SACH-MX0.30` scripting/helper corpus from the actual `stoneage2.5` resource tree. The recovered resource corpus is now eligible for deterministic REAL/ADRN/MAP parser validation even though the runtime bundle is not a clean mother client.
- Tightened clean-client validation around actual technical fingerprints. A 2010 StoneAge technical thread labels `ttttttttt / 20041215` as an original-2.5 PKEY/RUNKEY pair, but a 2015 source discussion shows the same pair labeled 7.5 and explicitly notes that login-packet formats also differ by client version. Therefore keys are now a **multi-factor contamination/lineage clue, not version proof**.
- Expanded the 2.5 byte-recovery path beyond the preserved MediaFire IDs: the old combined bundle previously lived on **Megaupload**, was re-uploaded as two MediaFire parts in April 2012, and was again reported unavailable by December 2012. Both host generations/reposts are now recovery targets.
- Re-opened the highest-priority JSS retail-package track from the current remote state and preserved the two direct ~1200-pixel Yahoo original-image targets behind `SRC-JP-1999-AD-YAHOO-01`, reducing dependence on marketplace-page rendering for that period advertisement.
- Rechecked all **13** exact Mercari original-image targets: every direct request currently returns **HTTP 403 Forbidden** in the available extraction path. The seller's suggestion that the bonus disc might play BGM remains explicitly classified as speculation, not disc-content evidence.
- Corrected stale continuity text in the package/identifier research notes: StoneAge retail JAN **`4909476303010`** is already resolved; the active identifier gap is the model/type code plus disc labels/matrix fields, and recovery must use public mirrors/caches rather than seller/collector contact or user-side acquisition.
- Surfaced and then **resolved the Suruga-ya StoneAge catalog lead**. Suruga's dated 1999-10-15 archive directly lists `Windows95/98 CDソフト/ストーンエイジ[初回版]`, and the linked product record identifies JSS, management number **`145026779`**, release date 1999-10-15, displayed list price 9,680円 and CD media. The page exposes no `型番`; `145026779` is therefore recorded strictly as a Suruga management ID, not a StoneAge model code. The current product image is a no-photo placeholder.
- Resolved the apparent Suruga price conflict at the evidence-classification level. StoneAge's period advertisement prints **8,800円（税別）**, while current Suruga displays **9,680円**. Two JSS controls show the same exact ×1.10 current-catalog transformation: `チャルボ55` 3,800→4,180 and `カメレオンツイスト` 6,980→7,678. This strongly indicates modern tax-inclusive catalog normalization rather than a competing historical MSRP. It is kept as an interpretation—not an undocumented Suruga policy claim—and **8,800円（税別） remains the historical StoneAge price baseline**.
- Opened a dedicated **StoneAge `1.74 / 1.74a` version-lineage archaeology** track rather than assuming Mainland 1.82 is the earliest practical bridge client.
- Recovered a same-period 2003 Korean Netmarble service answer naming its launch version **`1.74`**, and separately recovered contemporary Mado no Mori metadata naming the Japanese revival beta client **`1.74a`** with date 2003-12-12.
- Preserved an older Inium-era transition clue placing Korean `1.74` before the `2.0` family/riding update, while keeping the later preservation source below primary-evidence status.
- Recorded the strict boundary that `1.74` ≠ `1.74a` ≠ final JSS by assumption: byte identity, regional parity and direct ancestry remain OPEN until an actual client/file tree is recovered and diffed.
- Exact web/GitHub searches for a provenance-preserving `1.74` or `1.74a` installer, file tree or binary hash produced no credible artifact in this pass, so the newly identified version labels are recovery keys rather than recovered clients.
- Opened a **JSS → 2003 Japanese revival delta** track using near-contemporary 4Gamer coverage rather than modern player memory.
- Recovered a strong working boundary for riding: July 2003 revival coverage states that in the former Japanese service **only GMs could ride dinosaurs**. Normal-player riding is therefore not part of the working JSS/Japanese-original baseline unless direct primary evidence later overturns this.
- Recovered an original UI/mechanics boundary from TGS 2003: revival staff said the restored build was basically the same and then in bug-fixing/restoration mode; the report identifies the dedicated **item trade window as absent from the original**, with ground-drop exchange as the earlier context.
- Added `research/evolution/JSS-TO-2003-REVIVAL-DELTA-R1.md` and registered both 2003 4Gamer sources with explicit retrospective-evidence limits.
- Tried direct temporary-workspace retrieval of the archived JSS `stoneage.exe` through Wayback CDX/raw-object URLs. The present execution environment fails at DNS resolution for `web.archive.org`, so no binary bytes were obtained and no hashes/PE claims were made.
- Added a third descendant client-source control, `anson1788/stoneage` at `1997fc20456dbda36d181b9680ae10bed2e9cdf9`: it preserves `CheckForUpdate` and later `sa.exe` build/debug targets but not the Signally `updated` / `StoneAge.exe` direct-start gate or `PARAM_ARGS` placeholder in focused search.
- Reweighted updater archaeology fingerprints accordingly: `CheckForUpdate` strongest descendant source fingerprint; `sa.exe` strong later runtime candidate; `updated` / launcher message narrower; `HASH___________@@@@@@@@` low-priority Signally-local probe.
- Re-ran exact JAN/title/model web searches for StoneAge `4909476303010` and LIFESTORM II `4909476302013`; no retailer/catalog result exposing a trustworthy `JV...` model code was recovered, so both model/type codes remain OPEN rather than numerically inferred.
- Rechecked all **13** exact Mercari original-image targets for the sold initial-edition listing. Every `static.mercdn.net` original-image request is blocked with HTTP 403 in the current extraction path, so the package back/disc faces cannot be inspected from that set yet. This is recorded as a whole-set access limitation rather than treated as missing individual images.
- Preserved an older, higher-resolution Yahoo! Auctions LIFESTORM II package/manual/disc set (`c771109001`). It independently confirms JAN `4909476302013` and the physical disc appearance, but still does **not** expose a model/type code or disc matrix text clearly enough to promote either.
- Traced the Retromags `Play Online No.015 (September 1999)` record through its actual download layer: filename `Play Online No.015 (September 1999).cbr`, listed size **349 MB**, MD5 **`e009cc707810c4361c849f26248593af`**, and a concrete Retromags seedbox target. The present environment cannot resolve the seedbox host, so the second scan body has not yet been visually compared with the Kingpin scan.
- Recovered a preserved 2024 Yahoo! Auctions listing for a seller-described **unopened early JSS STONEAGE package** (`k1131932809`) with surviving front, side and back original-image URLs.
- Read the back-box barcode directly as **`4909476303010`**. This matches the previously generated `30301` search candidate but is now promoted solely because the StoneAge package photograph binds the number directly.
- The JSS Windows online-RPG retail JAN sequence is now artifact-grounded across three products: LIFESTORM `4909476301016` → LIFESTORM II `4909476302013` → STONEAGE `4909476303010`.
- Preserved the boundary that StoneAge's model/type code, disc labels/matrix text and S-grade media provenance remain OPEN despite the JAN resolution.
- Recovered an active Yahoo! Auctions listing for a surviving **LIFESTORM II ～光と闇の継承者～** package/CD (`v1234885585`) and preserved its three full-resolution public image targets in the product-identifier source ledger.
- Read the package-back barcode directly as **`4909476302013`**, matching a previously generated but deliberately unassigned candidate. This is now package-evidenced LIFESTORM II JAN data, not a numerical inference.
- Preserved the evidence boundary: the LIFESTORM II model/type code is still unresolved; `4909476303010` is not promoted to StoneAge merely because the two observed LIFESTORM bodies are `30101` and `30201`.
- Separated `LS2MAP` server-map evidence from client-map/resource evidence. StoneAge descendant server code, the `xgate` CrossGate reconstruction and `CrossGateData` all preserve `LS2MAP` as a server-map header; this is no longer allowed to stand in for an original client-map format.
- Recovered older CrossGate/StoneAge format documentation (Fanicer article lineage, preserved at cgsword/Omega) that explicitly compares the two clients: CrossGate `GraphicInfo/Graphic`, StoneAge `Adrn/Real`, shared 16-byte `RD` image blocks and a JSS-attributed Run-Length codec.
- Cross-validated that codec against three modern CrossGate implementations: `HonorLee-cn/CGTool`, `x-gate/xgtool`, and `kacoro/crossgate-tools`. All implement the same literal `00/10/20`, repeated-value `80/90/A0`, and repeated-zero `C0/D0/E0` families with 4/12/20-bit lengths.
- Identified a subtle StoneAge descendant-source asymmetry: its encoder supports the `0x20` 20-bit literal form, while the inspected decoder literal branch does not symmetrically handle it. This is retained as a possible later branch/source bug and is not projected back into the 1999 executable.
- Established that the StoneAge descendant `RD_HEADER` compiles to the same 16-byte on-disk shape described by CrossGate tooling: two-byte `RD`, compression/version byte, one padding/unknown byte, width, height, size.
- Kept the name origin of `LS2MAP` OPEN; no source found that explicitly expands `LS2` to LIFESTORM II.
- Added an independent public-data cross-check for the StoneAge ADRN specification: a 2022 ZenHAX sample analysis reports 80-byte ADRN entries whose leading values are image/file number, REAL offset and block length.
- Verified that the descendant source's intended Win32 `ADRNBIN + MAP_ATTR` layout independently totals exactly 80 bytes, materially strengthening the format reconstruction.
- Preserved an evidence-quality caveat: the forum's full pseudo-structure has an internal size inconsistency, so only the 80-byte record size and mutually consistent leading fields are retained; unknown padding fields are not copied as fact.

- Opened a new **resource-container lineage** track without changing the zero-purchase constraint.
- Recovered a 2013 Omega preservation thread stating that a 2007 LIFESTORM II backup contained `adrn_1.bin`, `real_1.bin` and map data; the poster explicitly described ADRN as image-address data and REAL as image-data.
- Preserved the negative detail that the StoneAge SAForever map editor could display LIFESTORM II maps but did not correctly align those LIFESTORM II image files. This prevents overclaiming direct format compatibility.
- Cross-checked two later StoneAge source lineages. Both preserve essentially the same `ADRNBIN` index structure and `initRealbinFileOpen` / `realGetImage` architecture: ADRN supplies bitmap number, offset, size, dimensions and attributes; REAL supplies the encoded image block.
- Recovered the StoneAge block-level format signature from both trees: `RD_HEADER` begins with `RD`, followed by compression flag, width, height and size.
- Recovered the matching legacy codec implementation in both trees: a custom run-length/literal scheme using flags `0x80 / 0x40 / 0x10 / 0x20`. Later zlib/high-color branches are kept separate from the undated legacy path.
- Global GitHub fingerprint search found the exact decoder/ADRN implementation only in the circulated StoneAge code family and ports/forks, not in an independently identified JSS title.
- Recovered a dated 2006 community technical note that observed `real_136.bin / adrn_136.bin` and referred to what the author called JSS's RLE compression algorithm.
- Attempted the two free ASUS WebStorage links preserved by the LIFESTORM II thread; the current environment cannot resolve/access the host, so no binary was treated as recovered.
- Defined a reproducible zero-cost byte-validation plan: if freely accessible LIFESTORM II data appears, hash externally, scan REAL for plausible `RD` blocks, test the legacy decoder, then separately test ADRN offset/size semantics. Negative results are to be recorded rather than forced into an engine-reuse narrative.
- Added dedicated research and source-registry documents; no LIFESTORM II/StoneAge shared-engine claim was promoted to FACT.


- User resource constraint was made explicit and promoted to a durable project rule: archaeology must not require buying, bidding on, shipping, opening, installing, or personally dumping physical StoneAge material.
- Marketplace/auction pages remain useful for public photographs, identifiers, package descriptions and provenance clues, but are **evidence surfaces only**, not acquisition opportunities.
- Added DD-008 so future conversations do not drift back into recommending purchase of rare clients/packages.
- Reframed immediate actions around free/public digital recovery, archived scans, public listings/catalogs, preservation sites, source trees and any freely retrievable original media.


- Re-verified remote `main` before continuing and confirmed `9d19112ae18ad9fb878def5b972b1ea8fbc133cf` / tree `75f16ea3b233f43fc86647abbac823eb4dffa17e` remained authoritative.
- Continued the highest-priority physical-media/product-identifier search rather than guessing a StoneAge JAN.
- Recovered a high-value same-medium anchor from Suruga-ya: JSS Windows 95 `LIFESTORM` = model `JV02005`, JAN `4909476301016`.
- Recovered two additional JSS-associated Windows catalog identifiers: `古都の旅 京都` = `4909476502031`; `四柱推命入門 しゃべる桃源郷` = `4909476603011`.
- Rechecked JSS console identifiers: `チャルボ55` = `4909476802018`, `カメレオンツイスト` = `4909476803015`, `カメレオンツイスト2` = `4909476804012`.
- Established the controlled observation that the shared `4909476` stem spans several product families, while the following ranges differ. This invalidates the prior shortcut of treating `4909476805019` as a likely StoneAge code merely because it follows the console sequence.
- Located a preserved period `LIFESTORM II` advertisement showing Windows 95/98, `1999年2月20日発売`, and 8,800 yen. Its currently accessible scan does not reveal a readable JAN/model number.
- Earlier in the same-day identifier pass, `4909476302013` and `4909476303010` were generated only as check-digit-valid search candidates. Public Yahoo! Auctions package-back photographs later **directly bound `4909476302013` to LIFESTORM II and `4909476303010` to STONEAGE**, so both are now observed retail JANs rather than inferred assignments.
- Added dedicated product-identifier research and source-ledger files so future searches can distinguish verified identifiers from merely syntactically valid candidates.
- StoneAge JAN **`4909476303010`** was promoted only after direct package-back evidence; the StoneAge model/type code remains OPEN.

## Player creation core reconstruction — 2026-09-18

- Cross-checked three preserved descendant server lineages at fixed revisions and reconstructed the ordinary player-creation contract.
- Ordinary VITAL / STR / TOUGH / DEX creation allocation is now modeled as exactly 20 total points, each input in 0..20, persisted at x100.
- Ordinary elemental creation allocation is now modeled as exactly 10 total points, each input in 0..10, at most two nonzero elements, with Earth/Fire and Water/Wind mutually exclusive; persisted at x10.
- Stable defaults recorded for the ordinary path: level 1, EXP 0, free stat points 0, charm 60, MP/max-MP 100.
- Test-server / configurable new-player overrides were explicitly separated from the baseline instead of being merged into historical rules.
- Added `tools/stoneage_player_creation_model.py`, deterministic regression coverage, dedicated CI, and `research/mechanics/STONEAGE-PLAYER-CREATION-CORE-R1.md`.
- Exact 1999/JSS identity remains **OPEN**; this milestone is strong convergent descendant evidence, not direct launch-client proof.
- Highest-value adjacent progression seam is now **transmigration/reset semantics**, with starter-pet/hometown linkage kept as a separate creation-side track.

## Player transmigration core reconstruction — 2026-09-18

- Reconstructed the common pre-sixth-transmigration player core across three preserved descendant server lineages.
- Stable ordinary gate: level >= 80, all pending stat points spent, event flags 39/40/42/46 complete; first four transmigrations require pet IDs 693/694/695/696 respectively, fifth requires all four.
- `CHAR_TRANSEQUATION` is now modeled as cumulative qualifying-quest count plus cumulative transmigration levels, with each level contribution capped at 130.
- Recovered the common inherited-point equation and literal source `Rounding(...,1)` behavior, then proportional redistribution to VITAL/STR/TOUGH/DEX.
- Final ordinary reset is modeled as level 1, EXP 0 and free stat points = new transmigration count * 10.
- Preserved a real version divergence instead of flattening it: gavinlinasd/iriselia and BismarckDD disagree on the last two IDs in the 20-entry quest-count table, so the deterministic core accepts `quest_count` rather than inventing one canonical flag list.
- Added `tools/stoneage_player_transmigration_model.py`, six deterministic regression tests, dedicated CI, and `research/mechanics/STONEAGE-PLAYER-TRANSMIGRATION-CORE-R1.md`.
- Sixth/seventh-transmigration, hero/angel, teacher/profession and other later branches remain separate version-diff evidence.
- Highest-value adjacent seam is now **starter-pet / hometown creation linkage**, especially separating the original four-village mapping from later unified-newbie-village and configurable starter-pet branches.

## Player birth / hometown core reconstruction — 2026-09-18

- Reconstructed the ordinary four-hometown creation linkage from descendant client/server code.
- Stable hometown input is 0..3; it maps to elder/spawn floors 1006/2006/3006/4006, preserves the corresponding savepoint bit, and maps in Bismarck client UI to 萨姆吉尔村 / 玛丽娜丝村 / 加加村 / 卡鲁它那村.
- gavinlinasd and iriselia preserve the ordinary starter-pet rule `enemy ID = hometown + 1`; the created pet is initialized for level 1.
- Descendant comments associate IDs 1..4 with 乌力 / 凯比 / 克克尔 / 威伯, but R1 treats the numeric IDs as stronger evidence and keeps the names as source hints pending authoritative launch enemy-table confirmation.
- Later `_UNIFIDE_MALINASI`, 6.0 `_DELBORNPLACE` and `_NEW_PLAYER_CF` branches are explicitly separated from the four-village baseline.
- Added `tools/stoneage_player_birth_model.py`, six deterministic regression tests, dedicated CI, and `research/mechanics/STONEAGE-PLAYER-BIRTH-CORE-R1.md`.
- The ordinary deterministic chain now begins at hometown/character creation and runs through player growth, encounters/battle/rewards and transmigration.
- Next priority: inventory remaining unmodeled deterministic state transitions before selecting the next seam; favor end-to-end loop closures such as death/revival/savepoint, capture/taming, or party/formation over isolated content-list expansion.

## Player death / revival core reconstruction — 2026-09-18

- Reconstructed the ordinary player `core_Dying -> CHAR_die` callback across three preserved descendant server lineages.
- Stable death transition now models: party discharge; enemy/unknown deaths requesting drops for every equipped slot; valid non-enemy attacker deaths selecting one random occupied equipment slot; half-gold ground-drop request followed by zero final carried gold; dead-count increment; paralysis/sleep/stone/drunk/confusion/poison cleanup; `ISDIE=1`; `ISATTACKED=0`.
- Drop helpers can fail because of world-placement constraints, so the model distinguishes requested world drops from guaranteed final carried-state changes.
- Reconstructed `CHAR_playerresurrect` as a separate in-place operation: base image restore, death flag clear, `ISATTACKED=1`, `ISOVERED=0`, HP clamped to 1..MAXHP; no MP refill and no movement.
- Preserved login sanitation separately: persisted death flag is cleared and non-positive HP is repaired to 1.
- Verified that later/new `CharLogout(flg=1)` means return-to-record-point through `LASTTALKELDER`, but no direct Bismarck client death-screen call to `charLogoutStart()` was found at the fixed revision; death -> automatic record-point choreography remains OPEN.
- Added `tools/stoneage_player_death_model.py`, seven deterministic regression tests, dedicated CI, and `research/mechanics/STONEAGE-PLAYER-DEATH-REVIVAL-CORE-R1.md`.
- Next priority: **capture/taming core**, because it closes the existing wild-enemy -> battle -> pet-roster/growth loop before party/formation work.

## Pet capture core reconstruction — 2026-09-18

- Reconstructed the ordinary battle capture gate and probability equation across three preserved descendant server lineages.
- Stable gate requires a target of enemy type with nonzero PETFLG; without the later `PickAllPet` bypass flag, target level may be at most attacker level + 5.
- Recovered the literal capture score: `(10 - HP²/MAXHP + level-difference/2 + dex-difference/15 + target capture-default + attacker luck) * attacker charm / 50`, then add temporary capture modifier and +15 for sleeping targets, with upper cap 99 and no lower clamp.
- Confirmed `RAND(1,100)` is inclusive and success uses strict `roll < score`; therefore capped score 99 yields 98 successful integer outcomes, not 99.
- Temporary capture modifier is cleared after the check regardless of result.
- Required capture-item tables are conditional/versioned; R1 accepts them as external version data rather than inventing one canonical table.
- All three branches define five carried-pet slots. Server pet creation searches the first empty slot only after the probability succeeds, so a full roster can still turn a successful roll into a final failure.
- Successful capture copies the wild enemy's current HP/MP, core stats, level, abnormal statuses, attributes, rarity/rank, pet ID, skills and other common fields into a new pet; enemy EXP is not copied and max EXP is recomputed from level.
- Success then records PETGETLV, consumes version-specific condition items, increments GETPETCOUNT, removes the original enemy from battle and normalizes the new pet AI/state.
- Capture command passes `20` to `BATTLE_MpDown`, but the active implementation is a no-op in all three fixed descendants; R1 records active MP cost as zero and the 20 only as source intent/provenance.
- Added `tools/stoneage_pet_capture_model.py`, nine deterministic regression tests, dedicated CI, and `research/mechanics/STONEAGE-PET-CAPTURE-CORE-R1.md`.
- Next priority: **party / formation state**, especially field party creation/join/leave, leader/client modes, ordering, default-pet coupling and projection into battle sides.

## Party / formation core reconstruction — 2026-09-18

- Reconstructed the ordinary field-party state machine and field-to-battle projection across three preserved descendant lineages.
- Common party modes are NONE / LEADER / CLIENT. The authoritative ordinary roster is leader-owned; client members store a leader pointer.
- Common baseline is five party slots. Slot 0 is leader-only; first join promotes a standalone target to leader and writes leader self into slot 0; clients fill the first free slot 1..4.
- Client leave creates a hole and does not compact higher slots. The next join reuses the first hole. Last-client leave changes the leader back to logical NONE even though raw slot 0 may still temporarily hold the leader self-index.
- Leader discharge dissolves the whole ordinary party.
- Field formation is a slot-ordered follow chain: leader movement propagates through valid clients in roster order, skipping holes. Ordinary clients cannot independently submit positional walking, though turn-only input remains allowed.
- Battle projection compacts valid field-party members into player battle slots 0..4 in party order. Each player's selected default pet is fixed to that player's local battle slot + 5, producing the ordinary ten-entry paired layout.
- Only the selected default pet auto-enters. If it is invalid/dead/non-positive-HP, DEFAULTPET is cleared; active code does not auto-search another carried pet.
- PvP party identity resolves leader -> self, client -> leader pointer, standalone -> none; two combatants resolving to the same leader are rejected as same party.
- Bismarck retains an optional `_MULTIPLAYER_` six-player extension, while the generic pet-placement code at the fixed revision still uses a hard-coded +5 pairing offset. R1 therefore excludes six-player support from the convergent old core and marks it for a separate extension audit.
- Added `tools/stoneage_party_formation_model.py`, eleven deterministic regression tests, dedicated CI, and `research/mechanics/STONEAGE-PARTY-FORMATION-CORE-R1.md`.
- Next priority: re-audit remaining deterministic loop gaps and select the seam that closes the largest loop, with trading/economy transfer, healing/status-service semantics, and item equip/use transitions as current candidates.

## Item use / equip core reconstruction — 2026-09-18

- Reconstructed the ordinary item-use dispatch and equipment movement layer across three preserved descendant lineages.
- Common old equipment baseline is five slots: head, body, arm/weapon, decoration 1, decoration 2. Belt/shield/shoes/glove are macro-controlled later extensions.
- `CHAR_ItemUse` routes every item type except `ITEM_OTHER` and `ITEM_DISH` into equipment placement and returns before `ITEM_USEFUNC`; OTHER/DISH use the ordinary callback path.
- Direct client inventory/equipment move packets are blocked during battle, but this is not generalized into a ban on battle-time `CHAR_ItemUse`, because battle execution itself invokes it.
- Un-reborn characters must meet ITEM_LEVEL; that specific common check is bypassed after transmigration. Later STR/DEX/profession/rookie/token restrictions remain versioned extensions.
- Non-decoration equipment must match its declared slot. Decoration items may use either accessory slot, but two items of the same ITEM_TYPE cannot occupy both decoration slots.
- Bag -> equip replacement swaps the displaced equipment back into the source bag slot and runs callbacks in stable order: detach old, then attach new.
- Equip -> empty bag detaches normally. Equip -> occupied bag recursively attempts to equip the bag item into the original equipment slot, producing an indirect exchange only if legal.
- Direct equipment-slot -> equipment-slot movement is rejected. Baseline bag -> bag behavior is a direct swap; optional pile/stack merging remains macro-controlled.
- Equipment movement feeds into `CHAR_complianceParameter` and refreshes derived HP/MP/ATK/DEF/QUICK/CHARM/LUCK/elements. Attach/detach callbacks are preserved as separate event hooks rather than being conflated with base stat recomputation.
- Added `tools/stoneage_item_use_equip_model.py`, fourteen deterministic regression tests, dedicated CI, and `research/mechanics/STONEAGE-ITEM-USE-EQUIP-CORE-R1.md`.
- Next priority: **healing / recovery service semantics**, to close battle damage/death/status -> NPC/payment -> restored player/pet state before economy/trading transfer work.

## Immediate next actions

1. **Continue recovered-byte reverse engineering.** REAL/ADRN/RD, SPR/SPRADRN, DAT runtime semantics, `1021.DAT`, and the major unresolved-graphic skew are now bounded as far as the mixed 2.5 bundle permits. Move the primary technical target outward into **character / pet / item / skill / stat / combat / progression data tables** in the recovered client/server corpus. First build a provenance-preserving inventory of candidate gameplay-data files and identify which tables are authoritative server data versus client display/cache data; then parse one family at a time with deterministic tests. Keep map 817/water-world missing assets as a version-diff target for the first clean comparison client. Continue `〖2.5纯净〗`, Korean **1.74**, Japanese **1.74a**, and JSS recovery in parallel.
2. **Reject repacks before analysis.** For every candidate, record source/provenance, archive filename, size, hashes, timestamps, installer metadata, executable names, unexpected patchers/loaders, and signs of private-server modification. Do not call a client "clean" merely because its title/version string looks old.
3. **The first verified usable client becomes the bridge specimen.** Immediately build a reproducible extraction inventory: complete file tree, hashes, PE metadata, strings/resources, directories, update components, graphics containers, maps, data tables, audio, UI assets, and executable/resource relationships.
4. **Reverse engineer data before recreating gameplay.** Determine resource/container formats and indexes; decode graphics/animations; map character/pet/item/skill/stat records; reconstruct map formats and event/NPC data; identify combat and progression tables where present; document which behavior is client-side versus server-dependent.
5. **Build tooling around recovered bytes.** Put parsers, validators, extractors and diff tools in `tools/`; put deterministic format tests in `tests/`. Do not commit proprietary original client payloads by default—commit hashes, metadata, schemas, derived inventories, test fixtures where legally appropriate, and independently written tooling.
6. **Use later/earlier clients comparatively.** When a second clean artifact is recovered, perform file- and data-level diffs to identify inherited versus added maps, pets, skills, UI, systems and format revisions. This is the main route for reconstructing evolution; historical articles are secondary corroboration.
7. **De-prioritize nontechnical archaeology.** Package price, JAN/model numbers, collector accessories, staff biography and similar topics are paused unless they directly unlock a client, prove provenance, or resolve a technical ambiguity.

## Continuity status

- Repository: `chinaneedM/stoneage-rebuild`
- Default branch: `main`
- Visibility: public
- Authority: latest GitHub remote state is the single source of truth for project continuity.
- Canonical restart protocol: `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`

## Blockers

No repository or workflow blocker.

The project still lacks a provenance-preserving **publicly obtainable** 1999 JSS retail disc image/dump and September 1999 beta binary. The newly isolated Korean `1.74` and Japanese `1.74a` bridge targets also lack a recovered original installer/file tree/hash, so their relationship to each other and to JSS remains unproven. LIFESTORM II and StoneAge JANs are directly resolved from public package photographs, but the StoneAge physical-package blocker remains the missing exact model/type code, disc identities and matrix identifiers; exact JAN/model searches still yield no trustworthy `JV...` field and the 13 Mercari originals are HTTP-403-blocked here. The beta web-recovery blocker remains a nearly complete application-page path; the Retromags No.015 object is identified down to filename, size, MD5 and seedbox target, but the scan body is still unreachable. Direct Wayback binary retrieval is independently blocked in the execution environment by DNS resolution failure, so the archived JSS `stoneage.exe` still has no recovered bytes. The developer-lineage track now has a named, independently cross-checked JSS/StoneAge staff lead in Yuki Tamura, but the original StoneAge credit list and exact staff-role mapping remain unresolved. The retail/client search retains `sa.exe`, `updated`, and `CheckForUpdate` only as descendant-derived search traits until original JSS material confirms each one independently. The binary/media blocker remains the principal Phase 0 constraint.
