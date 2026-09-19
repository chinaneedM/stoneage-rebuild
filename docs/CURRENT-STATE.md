# Current State

Last updated: 2026-09-19

## Current phase

**Phase 0 — Earliest Clean Client Recovery & Reverse Engineering**

The independent GitHub repository and continuity scaffold are established on remote `main`. The operational objective is now explicit: recover the **earliest freely/publicly obtainable, provenance-preserving and minimally modified StoneAge client / installer / complete file tree**, verify it at file level, then use it as the primary reverse-engineering specimen for reconstructing the game's systems and data.

Historical archaeology remains useful only when it helps authenticate, date, compare, or interpret a recovered client. Package price, retail product-number, staff-history, and similar research are **not primary objectives** unless they directly improve client recovery or technical attribution.

## Confirmed project direction

- **Primary path: recover the earliest clean client first, then reverse engineer it.**
- "Clean client" means an original/operator-distributed or otherwise provenance-preserving client, installer, disc image, or complete file tree with no known private-server repack, injected launcher, custom patcher, replaced assets, or undocumented modification. If absolute purity cannot be proven, candidates must be graded and compared rather than silently accepted.
- Search priority is **earliest freely/publicly obtainable artifact**, not the historically earliest version at any cost. The newly isolated Korean **Inium 2000** public-distribution track now precedes the 2003 1.74/1.74a bridge targets operationally; any recovered operator-era client must still pass byte-level provenance/contamination checks and remains distinct from JSS-Japan unless hashes prove otherwise.
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

## Healer / recovery core reconstruction — 2026-09-18

- Reconstructed two distinct recovery NPC systems across three preserved descendant lineages: ordinary free healer and selectable window healer.
- Ordinary healer restores player HP/MP to max. Standalone players and party clients heal only themselves; a party leader interaction heals every valid party member.
- Every valid carried pet is always restored to max HP/MP, has its pet death flag cleared, and is parameter-recomputed.
- Neither healer path clears the player's own death flag or calls player resurrection. Ordinary player abnormal statuses are not explicitly cured. Recovery and revival therefore remain separate mechanisms.
- Window healer uses a strict free threshold: configured level > player level is free; equality is already paid.
- Default paid rates are HP = level × 0.5 (minimum 1) and MP = level × 2.0. Combined service charges only player HP/MP components actually below max.
- Payment is checked/deducted before restoration; insufficient gold causes no heal.
- Pet healing is free in every window-healer mode. HP-only, MP-only and combined player healing all fully restore every valid pet as a side effect.
- Explicit pet-only need detection checks pet HP only, not pet MP or death flag, creating a preserved edge case where full-HP/low-MP pets may be reported as not needing healing.
- When a leader talks to a window healer, each party member gets an individual service flow based on their own level, deficits, gold and pets rather than one shared party transaction.
- Added `tools/stoneage_healer_recovery_model.py`, fourteen deterministic regression tests, dedicated CI, and `research/mechanics/STONEAGE-HEALER-RECOVERY-CORE-R1.md`.
- Next priority: **trading / economy transfer semantics** — gold, item and pet offers, confirmation/locking, capacity checks, exchange ordering and cancellation.

## Direct trade / economy transfer core reconstruction — 2026-09-18

- Reconstructed direct player-to-player trade state and asset-transfer semantics across three preserved descendant lineages; market/stall trade remains separate.
- Shared trade modes are FREE / SENDING / TRADING / LOCK. In the fixed active ordinary paths the SENDING assignment is dormant/commented, so valid trades normally enter TRADING directly.
- Trade search requires standalone, non-battle participants. The target must be a player directly in front, trade-enabled, standalone, non-battle and FREE; multiple eligible targets on the same tile are rejected as ambiguous.
- Direct trade supports carried items, carried pets and carried STONE/gold.
- A side's confirmation flag freezes that side's own offer: item/pet/gold handlers reject further edits after confirmation.
- gavinlinasd/iriselia fixed configs enable `_ITEM_PILEFORTRADE + _TRADESYSTEM2`: structured two-side offer records, then confirm/freeze both sides, then each side separately enters LOCK; the second lock triggers swap.
- Bismarck retains those code paths but its fixed server `version.h` does not enable them, so its active lock choreography is the older/simplified variant. Protocol choreography is therefore versioned rather than flattened.
- Structured preflight projects inventory/pet capacity and final gold caps before transfer. Full outgoing item stacks and outgoing pets are counted as capacity they will free.
- Preserved item-capacity formula over-counts exact pile multiples: quantity 20 with receiver max pile 10 requires 3 slots in preflight because source uses `quantity / maxPile + 1` whenever quantity > maxPile.
- Old gavinlinasd/iriselia pet care gate rejects an un-reborn receiver when offered pet level exceeds receiver level + 5 unless PickAllPet is active; Bismarck later changes this trade-specific delta to +20.
- Family guardian pets are rejected in the structured old-core path. Later Bismarck binding/free-trade restrictions remain versioned additions.
- Execution order is destructive: remove both sides' items, pets and offered gold first, then add incoming items, pets and gold. There is no rollback journal/snapshot transaction; safety relies on offer freezing plus preflight checks.
- Transferred pets receive new owner/player identity and are parameter-recomputed.
- Added `tools/stoneage_trade_economy_model.py`, seventeen deterministic regression tests, dedicated CI, and `research/mechanics/STONEAGE-TRADE-ECONOMY-CORE-R1.md`.
- GitHub reported no workflow-run records yet for the new workflow/research commits; no CI success is claimed.
- Next priority: fresh deterministic-loop gap audit, with item shop buy/sell, pet storage/shop and save/logout persistence as current candidates.

## NPC item shop core reconstruction — 2026-09-18

- Reconstructed the ordinary `npc_itemshop.c` buy/resale economy across three preserved descendant lineages.
- Buy unit price is `int(ITEM_COST × buy_rate)` in the ordinary path; missing buy_rate defaults to 1.0. Later changed-cost/fame/tax rules remain version/config layers.
- Buy requests are server-clamped to the current number of empty carried-item slots; zero capacity rejects the purchase.
- `CHAR_addItemSpecificItemIndex` uses the first empty item slot and does not merge existing stacks, so the empty-slot clamp reflects the actual shop insertion path even when pile-count support exists.
- Total affordability is checked before item creation, but purchase execution creates/inserts every requested item first and deducts the total STONE only after all insertions succeed.
- No rollback transaction surrounds the buy loop: an unexpected mid-loop allocation/registration failure can leave earlier inserted units while no purchase gold has yet been deducted.
- Player resale eligibility is a whitelist driven by `LimitItemType` / `LimitItemNo`; unmatched items cannot be sold.
- Grouped sale categories include ACCESSORY (types 8..15), OFFENCE (0..4 and 17..19) and DEFENCE (5..7).
- Ordinary sale price requires configured `sell_rate`; the local 0.2 initializer is not an unconditional fallback because no matching pricing branch leaves cost at -1.
- `special_item` pricing is checked first; if a matching special item has no `special_rate`, the preserved fallback is 1.2 × ITEM_COST.
- With pile support, sale quantity cannot exceed the selected stack count; partial sales decrement the stack and full sales delete the item instance.
- Sell preflight rejects when `current_gold + proceeds >= max_gold`; therefore an exact-cap result is rejected, unlike direct-trade final-cap semantics.
- Sale mutation order is item delete/decrement first, then gold addition.
- Added `tools/stoneage_item_shop_model.py`, fifteen deterministic regression tests, dedicated CI, and `research/mechanics/STONEAGE-ITEM-SHOP-CORE-R1.md`.
- Next priority: re-audit **pet storage/pet shop** versus **save/logout persistence boundaries** and choose the larger remaining deterministic loop closure.

## Save / logout persistence core reconstruction — 2026-09-18

- Reconstructed the ordinary character serialization, periodic/save-point save, normal logout and SAAC acknowledgement path across three preserved descendant lineages.
- Core character serialization persists CHAR_DATAINT/CHAR_DATACHAR fields, persistent flags, skills, concrete carried/equipped items, ordinary Pool items, titles, address-book entries, carried pets and ordinary Pool pets. Generic CHAR_WORK/runtime arrays are not serialized.
- Corrected terminology after the storage audit: ordinary `poolitemN` / `poolpetN` arrays are character-inline persistent state in the fixed descendants. The separate account-shared `Depotitem` / `Depotpet` warehouse channels are the later/versioned surfaces.
- Periodic autosave uses a configurable `CharSaveinterval`; the global sweep itself runs only after more than 10 seconds, and a character save occurs only when the connection is active, state is LOGIN, and `now - lastSave > interval`.
- Periodic and save-point saves use `unlock=FALSE`; they request persistence without ending the account/login lock.
- Save-send functions serialize and dispatch to SAAC asynchronously and return before durability acknowledgement. Their TRUE result is not proof of a successful disk write.
- `ITEM_DROPATLOGOUT` items are destroyed before final logout serialization, so they are intentionally absent from the saved logout snapshot.
- Normal logout first resolves active battle, then deletes logout-only items, discharges party/runtime memberships, converts selected later runtime timers into persistent fields, sets LASTLEAVETIME, and only then sends the final save.
- Fixed ordinary logout/disconnect call sites observed pass `save=TRUE`; no normal fixed `save=FALSE` call site was found.
- Final logout save uses `unlock=TRUE`. On SAAC, account unlock happens before save-envelope construction and before the character-file write.
- Runtime character and pet objects are destroyed immediately after the save request is sent, not after the save acknowledgement returns.
- A failed normal logout-save acknowledgement only reports `Cannot save`; there is no automatic retry, runtime rollback/reconstruction, or lock restoration. The old server therefore has a real last-state loss window.
- Added `tools/stoneage_save_logout_model.py`, thirteen deterministic regression tests, dedicated CI, and `research/mechanics/STONEAGE-SAVE-LOGOUT-PERSISTENCE-CORE-R1.md`.
- The Pool/Depot persistence distinction was corrected in the model/tests/report; GitHub Actions run `35365548551` completed **successfully** after that correction.
- The requested fresh milestone/gap audit is now completed in `docs/PHASE0-MILESTONE-GAP-AUDIT-R1.md`; it separates early/core gaps, later/versioned systems, data/content extraction work, and modern-rebuild engineering.


## Phase 0 deterministic milestone / gap audit — 2026-09-18

- Added `docs/PHASE0-MILESTONE-GAP-AUDIT-R1.md` as the current gap map.
- Corrected the planning boundary: the recovered gameplay-data inventory and coherence probe already exist and are **completed foundations**, not work to rebuild.
- Early/core deterministic mechanics now cover creation/birth, growth/transmigration, enemy/group/encounter chains, battle-adjacent death/capture, party, item use/equip, healing, direct trade, item shop, save/logout, and appear/login-return membership behavior.
- The ordered early/core gaps through savepoint/elder, ordinary Pool storage, field warp/map transitions, the generic NPC/world-content graph, callback joins, and the ordinary magic effect core are now closed at R1. The next deterministic gap is **common item effect semantics**.
- Professions, ordinary-player riding, family/guild, AutoPK, six-player party, account-shared Depot warehouses, pet fusion and similar later branches remain version-diff tracks unless earlier evidence independently requires them.
- Modern transactional persistence, typed import pipelines, engine/network/UI architecture and asset recreation remain DESIGN work and must not be mixed into historical reconstruction.

## Save point / elder / return-point core reconstruction — 2026-09-18

- Reconstructed the elder/save-point state machine across the fixed gavinlinasd, iriselia and Bismarck descendant revisions and connected it to the already recovered `appear.txt` login-return behavior.
- The server owns a 128-slot elder coordinate registry. Ordinary hometowns occupy built-in elder indices 0..3; dynamic `CHAR_ElderSetPosition` accepts indices 4..127.
- Save-point NPC initialization reads its ID and `Born=floor,x,y`, validates the coordinate, then registers that coordinate into the elder array. No separate standalone record-point coordinate table is required by this fixed source path.
- Per-character persistent state is split into `CHAR_LASTTALKELDER` plus the `CHAR_SAVEPOINT` unlock bit field. Ordinary birth sets both the hometown last-elder index and the corresponding hometown bit.
- `NOITEM` save points set the unlock bit before the talk callback checks it, so the same interaction immediately selects that point as `LASTTALKELDER`.
- Requirement-gated points first test `GetItem`; YES confirmation consumes the configured requirement and only then sets the unlock bit + `LASTTALKELDER`. Concrete item IDs remain content data and are not embedded in the core model.
- The 128-slot registry and the unlock representation are structurally mismatched: source uses one signed integer and literal `1 << elder_id`. Do **not** infer that all 128 coordinate slots are safely independent unlock bits.
- `CHAR_getElderPosition` range-checks the index but does not verify that the in-range slot contains a meaningful registered coordinate; unwritten static slots resolve to zero tuples. Older callers can also ignore a failed lookup. The reference model exposes these hazards instead of emulating undefined/uninitialized behavior.
- Older appear/login semantics now close end-to-end: saved floor in `appear.txt` -> `LASTTALKELDER` -> elder registry -> return floor/x/y. The appear-table X/Y fields remain unused by that observed old caller.
- Interaction and immediate-save behavior are versioned: gavinlinasd/iriselia preserve a facing-based gate with a same-cell exception and immediate unlock-false saves; Bismarck uses a distance/death gate and conditional save-point persistence hooks.
- Added `tools/stoneage_savepoint_elder_model.py`, fourteen deterministic regression tests, `research/mechanics/STONEAGE-SAVEPOINT-ELDER-RETURN-CORE-R1.md`, and dedicated CI.
- GitHub Actions run `35365018211` completed **successfully** for the model/report state.
- Persistent item/pet Pool storage has now been reconstructed below. The next priority advances to **field warp / portal / map-transition authority**.

## Ordinary item / pet Pool storage reconstruction — 2026-09-18

- Corrected a prior terminology error: ordinary **Pool** storage and later shared **Depot** storage are different mechanisms. The fixed character object owns ordinary Pool item/pet arrays directly; later Depot arrays use separate macro-gated pointers and SAAC channels.
- Ordinary Pool items (`poolitemN`) and Pool pets (`poolpetN`) are serialized/deserialized inline with the character save in the fixed descendants.
- Fixed carried-pet capacity is 5. Ordinary pet Pool usable capacity is `5 + 2 * transmigration`, capped by the compiled Pool maximum (10 in the ordinary inspected configuration).
- Ordinary item Pool usable capacity is `10 + 4 * transmigration`, capped by the compiled Pool maximum (20 in the ordinary inspected configuration).
- Pet-shop Pool access is controlled by shop `pool_flg`. Deposit cost is `50 + player_level * 4`.
- Pet deposit moves the same pet object/index from carried state into the first usable Pool slot, rejects the currently ridden pet, and clears `CHAR_DEFAULTPET` when the deposited pet was selected as default.
- Pet withdrawal moves the selected Pool pet into the first empty carried slot and compacts the Pool afterward; no ordinary withdrawal fee was observed.
- Pool item shop deposit cost defaults to 200 unless configured otherwise.
- The ordinary Pool-item UI marks `DROPATLOGOUT`, `VANISHATDROP`, or `!CANPETMAIL` items as unavailable, but the authoritative ordinary transfer primitive does not recheck those flags.
- The ordinary Pool-item transfer primitive also ignores the return value from `CHAR_DelGold`. If the debit fails for insufficient gold, the fixed handler can still move the item. This is recorded as a historical implementation defect, not a target modern rule.
- Item withdrawal moves into the first empty carried slot, charges no observed withdrawal fee, and compacts the Pool.
- Later shared Depot item code provides useful contrast: it rechecks restricted-item flags and rejects when `CHAR_DelGold` fails. Depot behavior remains versioned and is not back-projected into the ordinary Pool path.
- Added `tools/stoneage_pool_storage_model.py`, fourteen deterministic regression tests, dedicated CI, and `research/mechanics/STONEAGE-ITEM-PET-POOL-STORAGE-R1.md`.
- GitHub Actions runs `35365665920` and `35365778213` completed **successfully** for the ordinary Pool storage model/report state.
- Field warp / portal / map-transition authority has now been reconstructed below. The next priority advances to the **NPC/world-content graph**, then remaining item/skill effect joins.

## Field warp / portal / map-transition core reconstruction — 2026-09-18

- Reconstructed the classic overlap Warp NPC, shared `CHAR_warpToSpecificPoint` primitive, dialogue WarpMan party behavior, later `mapwarp.txt` layer, and later `_MAP_NOEXIT` login relocation as separate mechanisms.
- The classic field portal is an invisible, overable, non-attackable `CHAR_TYPEWARP` NPC whose simple argument embeds destination `floor|x|y`; initialization rejects invalid destination coordinates.
- `CHAR_walk` executes PREOVER, moves the character/object into the destination cell, then executes POSTOVER. Classic Warp therefore fires after the player actually steps onto the portal cell.
- The classic Warp callback directly warps only the triggering player. Party followers reach the same portal through normal follow-walking and trigger independently; the warp primitive itself does not broadcast to the party.
- Dialogue WarpMan is different: it resolves the party leader and explicitly loops valid party slots, warping the group to one destination.
- `_CHAR_warpToSpecificPoint` validates the destination before mutation, updates character/object coordinates, calls `MAP_objmove`, refreshes destination encounter min/max, updates map/client state, sets `CHAR_ISWARP` for non-client players, and moves the configured follow pet.
- Historical consistency hazard: coordinate fields are assigned before `MAP_objmove`; if map-object movement fails, the old source logs the failure without rolling the coordinate mutation back.
- Ordinary `CHAR_EVENT_WARP` cells suppress the observed random-encounter dispatch for that step.
- Later `_MAP_WARPPOINT` / `mapwarp.txt` creates explicit map-warp objects with source/destination validation and leader-party broadcast. Fixed version headers place this in a later feature layer; it is not promoted into launch-era core.
- Later `_MAP_NOEXIT` is a login relocation layer, not a walk portal. It packs configured exit as `(floor<<16)+(x<<8)+y`, so X/Y are effectively byte-sized representation fields and oversized values can corrupt adjacent packed bits.
- Login ordering is explicit in the fixed older source: `appear.txt` elder redirect runs before the later `_MAP_NOEXIT` lookup. If appear handling changes the floor first, a no-exit entry keyed only to the original saved floor is not subsequently consulted.
- Added `tools/stoneage_warp_transition_model.py`, seventeen deterministic regression tests, dedicated CI, and `research/mechanics/STONEAGE-WARP-MAP-TRANSITION-CORE-R1.md`.
- GitHub Actions run `35366300718` completed **successfully** for the warp-transition model. The report-state rerun was still in progress at the time this block was written.
- Next priority: **NPC/world-content graph** — creation/template/include relationships, class/function dispatch, placement, argument linkage, and early/core versus later content classification.

## NPC / world-content graph reconstruction — 2026-09-18

- Reconstructed the generic server-authoritative NPC world-content assembly chain across the fixed descendant source revisions: recursive file discovery -> magic-identified NPCTEMPLATE blocks -> magic-identified NPCCREATE blocks -> create-by-name template resolution -> map-floor validation -> runtime point selection -> function dispatch -> INITFUNC specialization.
- File extension is not the generic format authority. The fixed loaders identify template/create files by first-line magic; the recovered specimen confirms this with 46 `.template`, 2 misspelled `.templete`, and 1 extensionless template file.
- The recovered 2.5 specimen contains 49 template files / 131 template blocks / 116 unique template-name values, and 187 create files / 4,985 create blocks.
- All 4,985 create blocks define a born area, resolve exactly one template reference, and point to a floor ID present in the recovered server LS2MAP set. This generic NPC graph is internally much more coherent than the mixed enemy/group/encounter snapshot.
- 4,825 / 4,985 create references carry a non-empty opaque NPC argument, confirming that class-specific secondary config/argument semantics are the next content layer rather than part of generic create parsing.
- No recovered template uses a direct callback override; 130 / 131 use a function-set token. Generic runtime therefore derives behavior almost entirely through the function-set dispatch bundle in this specimen.
- The old fixed create structure has only eight template/argument slots and its legacy parser can admit a ninth resolved reference because of a `<= arraysizeof` guard. The recovered specimen does not exercise this hazard: every create block resolves exactly one template.
- Duplicate template names are operationally relevant: 8 duplicate name values exist, 3 are referenced, and 30 create blocks bind through those duplicated names. Since template lookup returns the first loaded matching name, these bindings retain a load-order ambiguity until a cleaner comparison artifact resolves the intended definitions.
- Source/data version skew is explicit: the recovered templates use 58 distinct non-empty function-set tokens; only 44 are present in each of the three fixed descendant source tables, while 13 are absent from all three. `Raceman` / `VipShop` additionally demonstrate branch-specific source coverage. This is preservation-source mismatch evidence, not a historical gameplay rule.
- Added `tools/stoneage_npc_world_graph_probe.py`, deterministic tests, dedicated real-byte CI, `research/recovered/STONEAGE-25-NPC-WORLD-GRAPH-R1.txt`, and `research/mechanics/STONEAGE-NPC-WORLD-CONTENT-GRAPH-R1.md`.
- GitHub Actions run `35367759927` completed **successfully** for the enhanced graph/ambiguity probe.
- Next priority: **item / magic / pet-skill effect callback joins** — reuse the already recovered schemas and measure data-token -> fixed-source dispatch coverage rather than rebuilding the table parsers.

## Item / magic / pet-skill callback coverage — 2026-09-18

- Closed the table-record -> declared-source dispatch join for active recovered `itemset.txt`, `magic.txt` and `petskill.txt` without redoing their existing schemas.
- Item callback strings resolve through the global `getFunctionPointerFromName` registry; magic and pet skills each use their own dedicated hash + exact-string dispatch table.
- Active item callbacks remain sparse outside use-time behavior: 957 USE rows / 52 unique tokens; 51 ATTACH rows / 5 tokens; 51 DETACH rows / 5 tokens; 40 DROP rows / 3 tokens; 2 PICKUP rows / 1 token; 3 RELIFE rows / 1 token; INIT/PREOVER/POSTOVER/WATCH are empty in this recovered active itemset.
- Every recovered non-USE item callback token resolves in all three fixed descendant source tables.
- Item USE source coverage is now separated from preprocessor status:
  - 17 unique tokens / 818 rows are unguarded in all three fixed source lineages;
  - 19 unique tokens / 86 rows are guarded in all three;
  - 16 unique tokens / 53 rows have partial source-lineage coverage;
  - zero active USE tokens are absent from all three.
- Active magic splits into 9 unique tokens / 130 rows unguarded in all three, 7 tokens / 46 rows guarded in all three, and 1 partial-source token / 5 rows (`MAGIC_AttSkill`); there are no mixed-guard or all-source-missing active magic tokens.
- Active pet skills contain 69 unique function tokens across 147 rows: 65 tokens / 143 rows resolve in all three fixed sources, while 4 tokens / 4 rows resolve in none of them. Those four rows remain quarantined as recovered-data / inspected-source skew rather than assigned invented behavior.
- Added guard-aware aggregate classification to `tools/stoneage_effect_callback_coverage_probe.py` without publishing recovered callback strings.
- The item probe now strips C comments, classifies dispatch guards, checks substantive function bodies across `item_event.c` + `battle_item.c`, and emits aggregate semantic families without publishing recovered callback strings.
- Final callback/body probe run `35373534098` completed **successfully**.
- Callback coverage itself is no longer the blocker; common magic and item semantic layers are closed below, and pet-skill guard/body refinement is next.

## Ordinary magic effect core reconstruction — 2026-09-18

- Reconstructed the nine magic callback families that are simultaneously unguarded in all three pinned descendant source revisions: Recovery, OtherRecovery, FieldAttChange, StatusChange, MagicDef, StatusRecovery, Ressurect, AttReverse and ResAndDef.
- The recovered active data independently supports this boundary: those nine tokens account for 130 / 181 active magic rows; 46 rows use seven callbacks guarded in all three fixed source lineages, and five rows use the partial-source `MAGIC_AttSkill` family.
- Common callback mutation order is caster validity -> battle-init rejection -> MP sufficiency -> MP deduction -> battle/field routing. As a result, battle-only common magic can fail for being outside battle **after MP has already been consumed**.
- Recovery and OtherRecovery are the two common field-capable families; field target validity is also checked after MP deduction.
- Old battle target authority is modeled as slots 0..9 and 10..19, with side/all selectors 20/21/22. Ordinary effects expand living targets; resurrection expands dead targets. The old all-target source contains list-termination hazards that are documented but not emulated as unsafe memory behavior.
- Ordinary Recovery additionally enforces `MAGIC_TARGET` packet-side rules and preserves the old battle-time explicit rejection of selector 22 in the Recovery wrapper.
- Recovery amount uses a 90%-110% power roll. Player recovery-rate multiplier is `1 + VITAL × 0.00010`; non-player multiplier is `1 + VITAL × 0.00005`. Percentage battle recovery multiplies by target MAXHP; field recovery has no observed percent branch.
- FieldAttChange parses attribute, power and duration; invalid power outside 0..100 returns to 30 and duration defaults to 3 turns.
- StatusChange parses status plus default 3-turn / success-15 parameters, then delegates resistance/hit resolution to the battle status checker.
- StatusRecovery preserves an old single-candidate behavior: it scans all active ordinary statuses, retains the highest-index one, and can clear only that selected status.
- MagicDef directly writes the selected defense-kind turn counter; later casts overwrite the same kind.
- Resurrection uses dead-target expansion and skips PvP player resurrection. `power == 0` yields full MAXHP behavior. For nonzero power the old code computes a percent-derived amount when `%` is present and then overwrites it with the 90%-110% random power roll, so the percent marker has no final HP effect.
- AttReverse toggles the reverse flag with XOR. Enabling immediately maps earth<-fire, water<-wind, fire<-earth, wind<-water. Disabling the flag does not immediately swap values back; normal fixed attributes are rebuilt during the next battle parameter refresh.
- ResAndDef combines the same resurrection behavior with a magic-defense duration on valid dead targets.
- Macro-gated attack magic, extra status systems, metamorphosis, deep poison, barrier, silence, call-dragon, family/sprite MP modifiers, riding interactions and no-magic-map restrictions remain versioned rather than flattened into this common core.
- Added `tools/stoneage_magic_effect_model.py`, `tests/test_stoneage_magic_effect_model.py`, dedicated CI and `research/mechanics/STONEAGE-MAGIC-EFFECT-CORE-R1.md`.
- The final model has **35 deterministic regression tests**. GitHub Actions runs `35370420953` and report-state rerun `35370877749` completed **successfully**.
- Ordinary magic R1 remains complete; guarded and partial-source extensions remain versioned rather than back-projected into the launch baseline.

## Common item effect core reconstruction — 2026-09-19

- Refined item evidence from dispatch-only matching to a two-stage test: callback registry guard state plus substantive function-body code across both ordinary item source modules.
- Active USE layer: 17 tokens / 818 rows are unguarded in all three dispatch tables, but body refinement reduces that to **15 stable-body tokens / 816 rows** plus **2 profession macro-shell tokens / 2 rows**. The two shells remain later/versioned and are not promoted into the common semantic core.
- Stable active USE families are battle/field recovery, status apply/recover, capture-rate increase, field attribute change, resurrection, warp, pet follow, no-enemy / forced-encounter controls, mic toggle, rename workflow, ordinary skill-up point, pet-owner/rename-lock release, and ToHelos work-state mutation.
- Battle recovery uses the historical two-byte key layout correctly: source `p+2` advances over the Chinese key itself rather than an invented separator. HP uses the VITAL recovery multiplier; MP does not.
- Item StatusChange defaults to **0 turns** (magic defaults to 3) with default success 15. StatusRecovery shares the old highest-index-active-candidate behavior.
- Resurrection shares the common nonzero-percent overwrite quirk and PvP player exclusion.
- Warp parses `flag floor x y`, rejects battle use, stable blocked floor 117, party-client use, and party-leader single-person flag; the item is consumed only after successful warp.
- Pet-follow checks target level and carried-pet ownership but does not consume the item after success; the visible loyalty-under-80 rejection is commented out in the fixed source.
- Rename uses a 1..26 **source-byte** name limit, rejects spaces / full-width spaces / `|`, writes the target rename before catalyst revalidation, treats catalyst argument 0 as unlimited, and decrements/deletes positive remaining counts after successful rename.
- ToHelos detaches the item before argument parsing, so malformed data still destroys it; party clients write the effect state to the party leader.
- Stable non-USE boundary is also closed:
  - ATTACH: 2 stable common tokens / 5 rows; 3 guarded / 46.
  - DETACH: 2 stable / 5; 3 guarded / 46.
  - DROP: 2 stable / 5; 1 guarded / 35.
  - PICKUP: 1 stable / 2.
  - RELIFE: 0 unguarded common; its 3 rows are entirely all-three guarded.
- Stable non-USE semantics cover no-enemy equipment attach/detach, PickAllPet attach/detach, mic cleanup, and dice drop/pickup visual state.
- Added `tools/stoneage_item_effect_model.py`, 68 deterministic tests, dedicated CI, and `research/mechanics/STONEAGE-ITEM-EFFECT-CORE-R1.md`.
- Item model run `35373496535` completed **successfully** with **68 tests**; final real-byte dispatch/body probe `35373534098` also completed **successfully**.
- Next priority: **pet-skill dispatch-guard + body classification**. The active recovered table has 65 all-three textual matches / 143 rows, but the fixed source tables share only 15 unguarded pet-skill callback families overall, so the 65-match set must not be promoted wholesale.

## Stable pet-skill core reconstruction — 2026-09-19

- Refined the recovered 147-row / 69-token pet-skill table through the same comment-aware dispatch/body evidence chain used for item semantics.
- Final active boundary:
  - **15 all-three unguarded + stable-body callback tokens / 33 rows**;
  - **50 all-three guarded tokens / 110 rows**;
  - 0 mixed-guard;
  - 0 partial-source;
  - **4 all-source-missing tokens / 4 rows**, still quarantined.
- The stable 15 families are None, NormalAttack, NormalGuard, ContinuationAttack, ChargeAttack, Guardian, PowerBalance, Mighty, StatusChange, EarthRound, GuardBreak, Abduct, Steal, Merge and NoGuard.
- Reconstructed handler-side COM1/COM2/COM3 encoding and downstream battle execution rather than treating `pet_skill.c` callbacks as complete mechanics by themselves.
- Key stable semantics:
  - continuation attack uses N=1..10 and sets both attack count and damage divisor to N;
  - charge decrements its wait counter through no-action turns, then rebuilds attack power as `FIXSTR + FIXSTR×攻% + MODATTACK` and enters CHARGE_OK;
  - guardian sets turn-local guardian registration and fails redirect under death, ordinary immobilizing statuses, barrier, self-attack or thrown-weapon attack;
  - PowerBalance applies immediate fixed-stat percentage changes before the normal attack path;
  - Mighty encodes multiplier×100 plus dodge modifier, but missing the multiplier marker leaves encoded multiplier 0 despite the local float default 2.00;
  - ordinary StatusChange defaults to 3 turns, applies only after positive physical damage, stores work timer as requested turn + 1, and uses the stable status probability relationship rather than later suit resistance layers;
  - EarthRound is two-phase hide -> attack and can consume stale full COM3 when its attack-percent marker is absent;
  - GuardBreak damages only a guarding, non-confused target;
  - Abduct has a **minimum 50** base chance against non-player targets and makes the attacker leave after any valid attempt, success or failure;
  - old Steal has 50% entry chance only against player targets, subtracts/destroys target assets rather than transferring them to the attacker in this function, and makes the attacker leave only on successful theft;
  - Merge delegates to `ITEM_mergeItem_merge` only when the pet owner is out of battle;
  - NoGuard packs dodge/counter/critical parameters but the fixed battle switch consumes the command only as `BATTLE_NoAction`.
- Preserved old COM3 residue behavior: Continuation and Abduct overwrite only LOW; NoGuard conditionally overwrites HIGH; EarthRound may leave the entire prior COM3 unchanged.
- Three-lineage key-formula spot checks converged; the only observed NoGuard token difference is simplified/traditional counter-marker spelling, not algorithmic behavior. Bismarck also refactors Steal’s inventory upper-bound helper while preserving the same removal semantics.
- Added `tools/stoneage_petskill_core_model.py`, `tests/test_stoneage_petskill_core_model.py`, dedicated CI, and `research/mechanics/STONEAGE-PETSKILL-CORE-R1.md`.
- Pet-skill model run `35374921866` completed **successfully** with **50 deterministic tests**; report-trigger rerun `35375022224` also succeeded.
- B8 is complete. The next deterministic priority is **only the unresolved early/core NPC secondary argument/configuration edges**, not broad NPC re-enumeration and not guarded pet-skill expansion.

## ExChangeMan secondary-argument condition core R1

- Closed the first remaining early/core NPC secondary-argument edge around the common ExChangeMan event-condition interpreter.
- Confirmed the second-stage argument path: file: references are resolved under npcdir, argument-file lines are merged with pipe separators, and field lookup is substring-based rather than exact-key based.
- Reconstructed the stable EVENT grammar: comma OR, ampersand AND, first-matching branch index, plus LV / ITEM / ENDEV / NOWEV / SP / TIME / IMAGE and PET/PETEV predicates.
- Preserved source quirks instead of repairing them: LV!= acts as equality; NOWEV!= is tautological; ITEM less-than/greater-than never succeed; quantity ITEM checks include equipment and pile counts while simple equality is carried-only; IMAGE relational operands are reversed; PET != falls through to equality.
- Reconstructed level-scaled event cost and the NPC-local round-robin NpcWarp selector. The fixed source passes meindex to the warp primitive, so the archaeology model records NPC-object warp behavior rather than silently converting it to player teleport.
- Added tools/stoneage_exchangeman_condition_model.py, tests/test_stoneage_exchangeman_condition_model.py, dedicated CI, and research/mechanics/STONEAGE-EXCHANGEMAN-CONDITION-CORE-R1.md.
- Local reference validation passes 26 deterministic tests.
- The next deterministic seam remains inside ExChangeMan: mutation/accept semantics and then an aggregate recovered-data usage probe.

## ExChangeMan mutation / accept core R1

- Closed the common ExChangeMan mutation/accept control-flow seam after EVENT branch selection.
- Reconstructed `NPC_ItemFullCheck`, `NPC_EventAdd`, `NPC_AcceptDel`, item deletion slot-domain differences, pet/egg random candidate selection, and common event-flag set/toggle/clear helpers across the three pinned source descendants.
- Confirmed active fixed-build compile branches for `_ITEM_PILENUMS` and `_EXCHANGEMAN_REQUEST_DELPET`.
- Preserved source quirks: ordinary non-star DelItem can terminate capacity projection early through reused loop index; starred deletion forecast assumes count == freed slots; active pile-mode non-star EVDEL targets -1; mode 2 becomes mode 0 only after preflight; accept-side item grant failures are ignored; GetStone/DelStone prechecks do not net; pet/egg random list counting reuses first-empty pet slot and can widen the random modulus when that starting index is sufficiently beyond the candidate list; EndSetFlg uses a blind NOWEVENT XOR toggle.
- Added `tools/stoneage_exchangeman_mutation_model.py`, `tests/test_stoneage_exchangeman_mutation_model.py`, dedicated CI, and `research/mechanics/STONEAGE-EXCHANGEMAN-MUTATION-CORE-R1.md`.
- Corrected local reference validation passes 26 deterministic tests.
- ExChangeMan R1 is closed for the fixed descendant core plus recovered 2.5 usage; the next class is selected by the recovered secondary-argument queue.

## Recovered ExChangeMan usage closure — 2026-09-19

- Real-byte probe `35378522791` completed successfully against the verified 2.5 bundle.
- The recovered corpus contains 315 unambiguous ExChangeMan create refs, all file-backed, resolving to 1,429 non-empty EventEnd blocks; 1,424 carry EVENT conditions.
- Source quirks now have data reachability labels rather than being treated uniformly:
  - live in recovered 2.5: 2 ITEM relational terms (the source never-success path), 1 NOWEV!= term (the source tautology), 72 ordinary DelItem blocks capable of the capacity-loop truncation, and 6/6 EVDEL blocks capable of the active pile-mode non-star item deletion defect;
  - dormant in this corpus: LV!=, PET!=, IMAGE relational, GetStone+DelStone same-block non-net precheck, and random-candidate GetEgg.
- Other active mutation surfaces: DelItem 477 blocks, GetItem 445, GetRandItem 65, GetStone 100, DelStone 17, GetPet 26, DelPet 59, EndSetFlg 80, NpcWarp 56.
- ExChangeMan R1 is now closed for the three fixed descendant source lineages plus this recovered 2.5 usage surface. Exact 1999/JSS equivalence remains open pending an earlier clean artifact.
- Corrected pet/egg random-list archaeology after checking the legacy delimiter helper: index 0 is a successful empty token, so first-empty pet slot 0 still counts the full candidate list; widening risk begins only when the reused starting index is sufficiently beyond the configured list.
- Corrected mutation suite now passes **26 deterministic tests**; CI run `35378831677` completed successfully.

## NPC secondary-argument queue — 2026-09-19

- Real-byte queue probe `35378662585` completed successfully over the same hash-pinned 2.5 bundle.
- Across 4,985 create refs, 4,955 resolve through unambiguous template names; 4,795 of those carry secondary arguments, split into 1,773 file-backed and 3,022 inline.
- Existing closed systems remain high-volume but are not reopened: Warp 2,904 refs, ItemShop 221, WarpMan 202, SavePoint 22, PetShop 16, PetSkillShop 21, PoolItemShop 5.
- The highest-volume **unclosed state-changing** class is `NPCEnemy`: **279 refs, all 279 file-backed**. Source pre-audit shows that its secondary config controls enemy groups, item/no-item gates, event flags, single-battle exclusion, battle creation, item theft/deletion, post-battle messages and warp/death actions.
- Bus (7 file-backed) + Airplane (5 file-backed) remain the next ordinary travel/economy seam after NPCEnemy. Airplane's later ticket-deletion and max-level branches are compile-disabled in the fixed gavin build; shared goods restriction is enabled.
- TimeMan has 34 file-backed refs but primarily controls NPC time-window visibility/graphics/messages, so it is lower priority than the player-state/battle/travel seams.
- The queue also records 30 create refs behind duplicate template names and 15 missing secondary argument files, all currently quarantined as preservation/source-order defects rather than silently repaired.

## NPCEnemy active core closure — 2026-09-19

- Real-byte NPCEnemy usage probe 35379672528 succeeded on the verified 2.5 bundle: 279/279 refs are resolved file-backed configs; 200 are gym mode and 79 normal mode.
- All 279 recovered configs normalize to entype=2. dieact=1 is active in 250 configs and hide/revive in 29; 10 configs activate onebattle=1; 78 use the pre-battle Yes/No prompt; 18 use the item gate; one uses steal.
- Reconstructed the fixed-descendant common NPCEnemy state machine without reopening general combat: normal first-10 enemy formation with big-enemy front placement, gym 64-candidate random main/pet selection, battle-mode metadata, item/onebattle/prompt gates, steal timing/deletion, dieact hide/revive, old post-win warp, and recovered NEWNPCENEMY FREE/WARP behavior.
- Preserved source quirks: party clients can return true from encounter routing without directly starting battle; duplicate required-item IDs can reuse one physical item; steal found is cumulative; revival requires strict now > death + delay; ENDEV/NOWEV relational FREE operators collapse to bit presence.
- Recovered gym data validates the separate selector: every one of 200 gym blocks has 17 enemyno candidates and an enemypetno list of 34 or 36 candidates, while recovered normal lists never exceed the ordinary 10-token limit.
- The two recovered NEWNPCENEMY blocks contain three NEWEVENT segments with FREE + WARP; FREE families are only ENDEV / EQUIT / LV / NOWEV and no recovered CHECKPARTY or NEW_ACTION mutation key is present.
- Descendant boundaries remain explicit: _EMENY_CHANCEMAN is enabled in gavin/iriselia but not Bismarck; Bismarck has an extra BattleIn revival guard; _NEW_ITEM_ changes inventory capacity only in Bismarck.
- Added tools/stoneage_npcenemy_core_model.py, tests/test_stoneage_npcenemy_core_model.py, dedicated CI, and research/mechanics/STONEAGE-NPCENEMY-CORE-R1.md.
- Local reference validation passes 25 deterministic tests.
- NPCEnemy R1 is closed for fixed-descendant common core plus recovered 2.5 active surface. Exact 1999/JSS equivalence remains OPEN.

## Bus + Airplane common transport core R1

- Reconstructed the shared fixed-descendant transport state machine: required routes, random route selection, reverse initialization, strict wait/terminal timers, routepoint traversal, terminal roundtrip toggle, whole-party discharge, Bus x/y routing, Air floor/x/y routing, cross-floor passenger warp and Air oneway behavior.
- Confirmed the real party call graph: both Bus and Air are CHAR_TYPEBUS, and generic CHAR_JoinParty calls NPC_BusCheckJoinParty for both. NPC_AirCheckJoinParty is not reached by the generic boarding path in the inspected fixed sources.
- Reconstructed active boarding order: front-position -> waiting-mode -> not-already-party -> capacity -> denieditem -> compile-enabled wares gate -> allowitem -> needlevel -> needstone -> immediate Stone debit -> CHAR_JoinParty_Main.
- Preserved pickupitem lifecycle: boarding preflight does not delete it; individual passenger leave can delete through NPC_BusCheckAllowItem(..., TRUE); normal terminal leader-side whole-party discharge does not call that deletion path.
- Preserved quirks: duplicate allowitem IDs can reuse one item during preflight but require multiple copies in pickup deletion mode; pickup deletion is non-transactional; configured needstone below -1 would add Stone.
- _ITEM_CHECKWARES is enabled in all three fixed descendants. Air delitem/maxlevel extensions are compile-disabled or absent and, more importantly, are not on the active generic CHAR_TYPEBUS join path.
- Added tools/stoneage_transport_core_model.py, tests/test_stoneage_transport_core_model.py, dedicated CI and research/mechanics/STONEAGE-BUS-AIR-TRANSPORT-CORE-R1.md.
- Local reference validation passes 26 deterministic tests.
- Next step is the verified 2.5 Bus/Air payload-free usage probe before closing the transport seam.

## Bus + Airplane recovered active closure — 2026-09-19

- Real-byte transport usage workflow 35381648065 succeeded against the verified 2.5 bundle; aggregate argument SHA-256 is 351409fa154bd289c78c28e86a93ea3151bfc7f2af2ec1eaed67e0e987838f43.
- All 7 Bus and 5 Airplane refs are resolved file-backed configs, and all 12 have routenum=1.
- Active recovered common gates are denieditem + needstone on all 12 transports. Bus fares are 0/20/25/30/40/50 Stone; Air fares are 1000 or 3000 Stone.
- No recovered transport config uses reverse, allowitem or needlevel. Air additionally has no recovered WAVE, delitem or maxlevel.
- Air oneway is active in 2/5 configs; all five Air routes contain floor changes, confirming the cross-floor vehicle/passenger warp path as active behavior.
- Two Air configs contain pickupitem but no allowitem, so pickupitem is inert under the fixed generic boarding code.
- All 311 Bus route points are valid x,y pairs and all 61 Air points are valid floor,x,y triples; no malformed route points were found.
- Bus + Airplane R1 is closed for the fixed-descendant common core plus recovered 2.5 active surface. Exact JSS equivalence remains OPEN.
- Queue triage now selects Janken (9 resolved file-backed refs) as the next unresolved state-changing secondary-argument seam; Action and TimeMan are deterministic but presentation-level, while Scheduleman/family packages remain later-scope.

## Janken active core closure — 2026-09-19

- Real-byte Janken probe 35382078973 succeeded: all 9 refs are resolved file-backed configs; aggregate argument SHA-256 is 491e3784ca8476649788cbbb3c93e13e85af1d0b2af8605e913552515071059c.
- Every recovered Janken config has MainMsg / EntryItem / NoItem / WinWarp / LoseWarp.
- Every recovered EntryItem is exactly one starred token with quantity 1; every Win/Lose Warp is a valid floor,x,y triple; no recovered WinItem or LoseItem exists.
- Reconstructed the common result state machine and item lifecycle across the three fixed descendants.
- Preserved the active historical defect: failed EntryItem validation sends NoItem but does not return, then deletion runs and the Janken selection is still sent. In the recovered quantity-1 shape, having the item consumes one copy; lacking it consumes nothing but still allows play.
- Preserved dormant source quirks: plain EntryItem deletes every matching copy; insufficient multi-count starred deletion can partially consume available copies; duplicate validation tokens can reuse inventory before deletion.
- Ties reopen the choice window without re-running EntryItem, so entry consumption occurs once per accepted start, not once per tied round.
- Win/Lose source order is optional item reward attempt -> result warp -> result action/window; reward return values are ignored. Reward grants are dormant in the recovered 2.5 data.
- Added tools/stoneage_janken_core_model.py, tests/test_stoneage_janken_core_model.py, dedicated CI and research/mechanics/STONEAGE-JANKEN-CORE-R1.md.
- Local reference validation passes 20 deterministic tests.
- Janken R1 is closed for fixed-descendant common behavior plus recovered 2.5 active surface.

## Charm NPC core closure — 2026-09-19

- Reused the recovered NPC census: 4 Charm refs exist in the verified 2.5 specimen and none has a secondary argument, so no extra configuration probe is required.
- Confirmed the same core in all three fixed descendant lineages: RATE=10, CHARMHEAL=5, WARU=3; service adds 5 charm up to 100 and refreshes player plus carried-pet parameters.
- Preserved exact integer cost formula: level × 10 × floor(charm/3) × (transmigration+1), with charm <=1 first replaced by 3.
- Preserved the non-monotonic source edge: charm 2 costs zero while charm 0/1 cost one division unit.
- Normal UI refuses a Yes confirmation at charm >=100, but raw CharmUp would use cost=-1 and add one Stone if reached by a stale/forged callback; normal flow and raw mutation semantics are modeled separately.
- Added tools/stoneage_charm_core_model.py, tests/test_stoneage_charm_core_model.py, dedicated CI and research/mechanics/STONEAGE-CHARM-CORE-R1.md.
- Local reference validation passes 14 deterministic tests.
- Healer/WindowHealer were found to already be closed by STONEAGE-HEALER-RECOVERY-CORE-R1 and were not duplicated.
- Remaining-class triage now selects Riderman ahead of Windowman, Bankman and Raceman.

## Riderman active core closure — 2026-09-19

- Real-byte Riderman probe 35383566011 succeeded: 4/4 refs have inline conff pointers, all 4 resolve, and all 4 share one identical conff content; aggregate conff SHA-256 is 20c87aa00cb82aeb7bde861d900f1dc159f9794a2f9693065186578b6b2a7009.
- Recovered tuition ladder is 5000 -> ride 40, 10000 -> ride 80, 15000 -> ride 120, 20000 -> ride 200, via windows 110/120/130/140 targeting hard-coded actions 6/7/8/9.
- All four tuition windows retain letter1..4 values, but the active trainer's letter/pet prerequisite block is #if 0 in gavin/iriselia and absent from Bismarck's active path. Recovered data has no takeitem/giveitem/checkhaveitem/checkdonthaveitem key.
- Training deducts Stone before writing CHAR_LEARNRIDE. Successful training can additionally credit takegold/5 to a matching manor-family account; that family persistence remains a separate later package.
- Final-tier lineage divergence is explicit: gavin/iriselia only allow exactly learnride=120 into the 200 tier, while Bismarck allows 120..200 inclusive and therefore can repeatedly charge a character already at 200.
- Native riding confirms CHAR_LEARNRIDE as the pet-level ceiling. Stable common mount gates include not-in-battle, valid pet, not already riding, training >= pet level, loyalty/fixed-AI >=100, player level +5 >= pet level, and a direct ridePetTable mapping.
- Later riding extensions are versioned: _NEW_RIDEPETS is enabled in gavin/iriselia but not fixed Bismarck; pet-transmigration limits and Bismarck trade-mode checks also diverge.
- Transmigration dismounts but does not reset CHAR_LEARNRIDE because the reset line is commented out in the fixed source.
- Added tools/stoneage_riderman_core_model.py, tests/test_stoneage_riderman_core_model.py, dedicated CI and research/mechanics/STONEAGE-RIDERMAN-CORE-R1.md.
- Local reference validation passes 19 deterministic tests.
- Riderman R1 is closed for recovered 2.5 trainer configuration plus fixed-descendant common personal riding behavior.

## TimeMan active core closure — 2026-09-19

- Real-byte TimeMan workflow 35384038054 succeeded: all 34 refs are resolved file-backed configs; aggregate argument SHA-256 is 7a3dfbacbaba1137d10052959eb299b0e9c1e1cfa3bff86181b637e5c52aa457.
- StoneAge time is a 5400-real-second / 90-minute day quantized into 1024 internal hour units. The three fixed descendants share the same TimeMan table and strict-boundary Watch logic.
- Recovered 2.5 TimeMan uses only ALLNOON (18), ALLNIGHT (9) and AFTER (7); AM/PM/FORE/EVNING/MORNING/FREE are dormant in this specimen.
- 30 configs omit change_no and therefore use hidden graphic 9999 outside the active window; 4 use numeric alternate graphics. No recovered explicit CLS change value was observed.
- All 34 configs contain main_msg; variant counts are 16x1, 12x2, 3x3 and 3x4. Only 4 configs contain change_msg, each with one variant.
- Preserved strict endpoint behavior, including exact hour 0 exclusion in wrapping/FREE intervals.
- TimeMan is Watch-driven rather than timer-loop-driven: Init stores the rule but does not evaluate current time or explicitly initialize mode/current-graphic state; a nearby player Watch event performs correction.
- Hidden graphic 9999 suppresses talk; mode 0 uses main_msg and nonzero mode uses change_msg, choosing a comma-separated variant randomly.
- Added tools/stoneage_timeman_core_model.py, tests/test_stoneage_timeman_core_model.py, dedicated CI and research/mechanics/STONEAGE-TIMEMAN-CORE-R1.md.
- Local reference validation passes 18 deterministic tests.
- TimeMan R1 is closed for fixed-descendant common behavior plus recovered 2.5 active surface.

## Windowman recovered routing closure — 2026-09-19

- Real-byte Windowman workflow 35384359937 succeeded: 17 refs all carry inline conff pointers; 13 conff files resolve, 4 are missing from the recovered bundle, and the 13 survivors contain 8 distinct config contents. Resolved conff aggregate SHA-256 is 5115e8544aa95014ded26646fbe75c1dbfa25e0aa48dfd10d4eadb29706e2b80.
- Fixed-source Windowman is a deterministic window router: button -> optional item-existence / item-absence tests -> target window -> send target window.
- The 13 surviving 2.5 configs use gotowin routing only. None uses checkhaveitem/haveitemgotowin/checkdonthaveitem/donthaveitemgotowin.
- None of the 13 surviving configs contains takeitem, giveitem, warp or battle.
- Source parses takeitem/giveitem but never executes them in the Windowman callback. warp/battle exist only as initialized struct placeholders and are not parsed by the fixed conff reader.
- Windowman therefore must not be reconstructed as an inventory/warp/battle mechanic from field names alone.
- Preserved source ordering: if both item conditions existed and both passed, the later don't-have target would overwrite the earlier have-item target.
- The 4 missing conff files remain an explicit evidence gap; no claim is made that they match the surviving 13.
- Added tools/stoneage_windowman_core_model.py, tests/test_stoneage_windowman_core_model.py, dedicated CI and research/mechanics/STONEAGE-WINDOWMAN-CORE-R1.md.
- Local reference validation passes 16 deterministic tests.
- Windowman R1 is closed for common routing semantics plus the 13 surviving recovered 2.5 configs.

## Action NPC presentation core closure — 2026-09-19

- Real-byte Action workflow 35384705409 succeeded: all 8 refs resolve to file-backed configs; aggregate argument SHA-256 is 720f1e31ff060c0053e3db70e2f660c822b0a3b4f135e83b82f586c7aa442eed.
- Every recovered config contains normal plus all 11 fixed Watch-action response keys: attack, damage, down, sit, hand, pleasure, angry, sad, guard, nod and throw.
- All 8 recovered configs contain msgcol=1, but literal fixed-source initialization cannot deterministically read it: NPC_ActionInit passes an uninitialized local argstr buffer to NPC_Util_GetNumFromStrWithDelim.
- Talk responds only to a player in front and uses normal. Watch responds only to a face-to-face player and only for an exact action-table match.
- Preserved source/comment mismatch: unsupported Watch actions are silent; normal is not an invalid-action fallback despite the source comment.
- Action performs no inventory, Gold, location, battle, save, pet or persistent-state mutation.
- Added tools/stoneage_action_core_model.py, tests/test_stoneage_action_core_model.py, dedicated CI and research/mechanics/STONEAGE-ACTION-NPC-CORE-R1.md.
- Local reference validation passes 10 deterministic tests.
- Action R1 is closed. SignBoard / TownPeople / Mic are next handled as lightweight presentation/broadcast registrations rather than full state-machine seams.

## SignBoard / TownPeople / Mic presentation registration — 2026-09-19

- Real-byte presentation workflow 35385048916 succeeded; aggregate SHA-256 is 9e5a2919b44412edc812d9b7612346f74dfa8f99f2910d5e9b424083c425fe2f.
- SignBoard: all 181 refs resolve; 177 are plain display and 4 use the active %manorid:...% dynamic manor-owner presentation path.
- TownPeople: 445 refs total; 389 resolved files, 34 inline args, 15 missing files and 7 no-arg refs. Observable dialogue shapes range from 1 to 12 comma-separated variants.
- The 7 no-arg TownPeople refs map to a literal fixed-source defect: GetArgStr failure is ignored and an uninitialized local buffer is subsequently scanned. They are not normalized into empty dialogue.
- Mic: all 4 refs resolve; all use eight-token pipe/rectangle mode, all have family flag zero, exactly one enables FREE, and none enables WIND. Active recovered behavior is same-floor rectangle chat; WIND popup and family-announcement paths are dormant.
- These three classes are presentation/broadcast semantics and do not mutate ordinary player inventory, Gold, location, battle, save, pet or persistent progression in their common paths.
- Added tools/stoneage_presentation_npc_model.py, tests/test_stoneage_presentation_npc_model.py, dedicated CI and research/mechanics/STONEAGE-PRESENTATION-NPC-SEMANTICS-R1.md.
- Local reference validation passes 14 deterministic tests.
- High-volume ordinary presentation NPCs are now removed from core-mechanics priority.

## Dengon / Duelranking persistence-boundary closure — 2026-09-19

- **Dengon is a real persistence seam, but for world/message state rather than character progression.** The common fixed-descendant implementation stores a location-keyed server-local bulletin board as a 1000-slot x 268-byte ring and writes on non-empty submissions.
- The recovered 2.5 snapshot does not contain valid full Dengon boards: all 40 runtime files are 11-byte zero-counter stubs. They are preserved as a specimen-shape gap, not promoted into the live board format.
- **Ordinary Duelranking is read/display only with respect to persistent duel ranking.** It queries `DB_DUELPOINT` through SAAC, pages ten rows at a time and changes only transient `CHAR_WORKSHOPRELEVANT` pagination state.
- The common Duelranking NPC does not write duel points. Later tournament/family-contend branches are compile-gated, package-coupled extensions and remain later-scope.
- Canonical boundary record: `research/mechanics/STONEAGE-DENGON-DUELRANKING-PERSISTENCE-BOUNDARY-R1.md`.
## Personal bank persistence closure — 2026-09-19

- Bankman is the UI adapter: its personal-account path sends `B|G|<CHAR_BANKGOLD>`; the balance mutation itself lives in `FAMILY_Bank` subcommand `G`.
- Signed transfer semantics are now fixed: positive values move `CHAR_GOLD` into `CHAR_BANKGOLD`; negative values withdraw bank Stone into carried Gold, with projected balance bounds enforced.
- Preserved historical family coupling: a non-member with zero personal-bank balance is denied; a former/non-member with residual balance can still withdraw it; new positive deposits require current family membership.
- `CHAR_BANKGOLD` serializes as `bankgld` in the ordinary character record. The `G` mutation branch does **not** call `CHAR_charSave*`; persistence is deferred to the standard periodic/logout/save lifecycle.
- Personal subcommand `G` and shared-family-treasury subcommand `T` are separate persistence domains; the latter goes through SAAC family-data mutation.
- Fixed descendants disagree on the compiled personal-bank ceiling: gavinlinasd/iriselia use **10,000,000**, while Bismarck uses **100,000,000**. This remains VERSIONED evidence rather than a universal constant.
- Added `research/mechanics/STONEAGE-PERSONAL-BANK-PERSISTENCE-R1.md`, `tools/stoneage_personal_bank_model.py`, `tests/test_stoneage_personal_bank_model.py` and dedicated CI.
- Local deterministic validation passes **13 tests**; GitHub Actions run **35387247569** completed successfully.
## Quiz active core closure — 2026-09-19

- Corrected an earlier census interpretation: recovered 2.5 contains **22 Quiz create refs** through one duplicated-but-stable Quiz template-name value; four was the number of Quiz template blocks, not live create references.
- Real-byte Quiz probe run **35419940820** succeeded. All 22 configs resolve; every one uses a single starred `EntryItem` with quantity 1, while **none uses EntryStone**.
- `Party` exists in all 22 configs, and the fixed source only shows the party warning before continuing. Therefore the historical “party warning but no actual block” defect is active in this recovered specimen.
- `Warp` is active in 21/22 configs (36 valid three-field destinations total); `GetItem` is active in 4/22 and each recovered reward has one candidate item.
- The global question table has 150 non-comment source rows; the fixed loader accepts 149 nine-field rows and skips one eight-field row. Loaded answer types are 22 two-choice, 84 three-choice and 43 free-text questions.
- Preserved free-text substring matching, ordered score-threshold evaluation, eight concurrent session slots, 100-entry no-repeat history, and the full-inventory/EntryItem interaction.
- Added `research/mechanics/STONEAGE-QUIZ-CORE-R1.md`, usage probe/model/tests and dedicated CI. Core validation run **35419980296** succeeded.
## Residual ordinary NPC sweep closure — 2026-09-19

- Final LuckyMan/Door probe run **35420226969** succeeded after correcting create→template matching to the server's case-insensitive semantics.
- Recovered 2.5 has **1 LuckyMan template block / 1 stable template name** and **3 Door template blocks / 3 stable template names**, but **zero create references for both classes**. They are defined but not instantiated in this recovered world.
- LuckyMan fixed-source behavior is only a carried-Stone charge plus random fortune text keyed by `CHAR_LUCK`; it grants no item/EXP, changes no luck/progression and performs no travel/battle.
- Door fixed-source behavior mutates only door NPC/world runtime state (graphic, overability, switch count, close timing) and checks key/title/password conditions; it does not consume player items or Gold. Room-admin auction fields belong to the deferred RoomAdmin package.
- Canonical closure: `research/mechanics/STONEAGE-RESIDUAL-NPC-SWEEP-CLOSURE-R1.md`.
- **Ordinary non-family NPC mechanics sweep is now closed.** Thirteen unmatched recovered function-set tokens remain explicit source/data lineage gaps rather than guessed implementations.
## Korean Inium 2000 mass-distribution recovery lead — 2026-09-19

- A new pre-1.74 TARGET-A is established from contemporary sources. DailyGame reports **trial service had begun on 2000-10-04**; later 2000-10-13/14 Electronic Times coverage describes free Korean service through exact host `www.stoneage.enium.co.kr`. These are preserved as distinct chronology points rather than one launch date.
- By late October, contemporary product-launch coverage reported roughly **200,000 downloads**.
- GameMeca on 2000-12-28 reported approximately **400,000 Hananet downloads** and **310,000 CNET downloads**, proving at least two high-volume portal mirror surfaces in addition to the operator site.
- Contemporary launch/distribution coverage also records Samsung PC/education-center channels and a roughly **60,000-unit** package-supply agreement, adding an offline preservation track.
- This does **not** establish the exact 2000 version number, installer filename, size, checksum, mirror URL or byte identity between distribution channels. Korean localization also means a clean Inium client is a bridge specimen, not automatic JSS-Japan byte identity.
- Exact installer/path searches have not yet recovered bytes. The immediate objective is now **filename/path discovery** from Inium, Hananet/GamePlus, CNET Korea, period software catalogs, magazine/ISP CDs and preserved pre-Netmarble installations.
- Archive metadata probes are currently **inconclusive**: Wayback/CDX and Arquivo.pt runs returned request timeouts / network-unreachable errors, so their zero counts must not be read as evidence of no archived captures.
- Canonical record: `research/clients/STONEAGE-KOREA-2000-PUBLIC-DISTRIBUTION-RECOVERY-R1.md` and `docs/SOURCE-REGISTRY-CLIENT-RECOVERY-R1.md`.
## 2001 Korean install-CD recovery sub-track — 2026-09-19

- YES24 and Aladin independently catalog the GameTime `스톤에이지 퍼펙트 가이드`; YES24 dates it **2001-04-30**, lists **CD 1**, and explicitly states that the bonus CD contains the **StoneAge installation program** plus demo-game CD content.
- Exact identifiers: ISBN-13 **9788995182123**, ISBN-10 **8995182121**.
- This creates a concrete near-period Korean installation-media recovery target. It is later than the 2000 Inium/Hananet/CNET online target, but materially earlier and more provenance-specific than the 2003 1.74 bridge.
- No disc image, installer filename, version, size, hash or file tree is recovered yet; equality with the 2000 online client must not be assumed.
- Recovery remains public-only: search exact title/ISBN/CD metadata and preservation/ISO catalogs; no purchase or user-side acquisition dependency.
- Registered in `STONEAGE-KOREA-2000-PUBLIC-DISTRIBUTION-RECOVERY-R1.md` and the clean-client source registry.

## Korea 2000 recovery-surface narrowing — 2026-09-19

- Contemporary references resolve **CNET Korea's download root** to `http://korea.cnet.com/downloads/` and the **Hananet software repository** to `http://pds.hananet.net`.
- **CNET StoneAge child-record and payload identity are now recovered:** preserved 2000-11-10 and 2001-01-24 download-index snapshots point StoneAge to `Software_Id=200009263856`; archived detail pages resolve the file-size label **257MB** and the download target **`/pc/games/online/stoneage.zip`**, with maker homepage `stoneage.enium.co.kr`. Exact Wayback Availability checks for that ZIP path currently return zero archived payload snapshots, so the remaining CNET gap is the actual ZIP bytes / surviving mirror, not the filename or historical portal path.
- **Hananet StoneAge child-site and distribution records are now recovered:** the GamePlus chain resolves to **`http://stoneage.hananet.net/main.htm`**, and all menu pages `1.htm`, `2.htm`, `2_2.htm`, `2_3.htm`, `2_4.htm`, `2_5.htm` have now been replayed. The archived `2.htm` explicitly instructs users to insert the StoneAge **CD into the CD-ROM**, wait for the automatic install menu, follow Setup, and notes DirectX 6.1. The recovered `2_5.htm` exposes StoneAge boards `GAM2:STAD`, `STAF`, `STAN`.
- **Hananet STAD provides two exact distribution records dated 2001-02-10 and now directly maps both records to file paths in its archived HTML source:** record **8119**, `온라인게임 스톤에이지 정식 버전` (official/full version), **260 M** → `http://stoneage.hananet.net/down/sa.exe`; record **8120**, `온라인게임 스톤에이지 체험 버전` (trial version), **240 M** → `http://stoneage.hananet.net/down/sa_demo.exe`. In the 2001-08-14 preserved STAD source these two direct-file button rows are inside an **HTML comment block**, so they establish historical title/size/file mapping but must not be described as visible/clickable buttons at that snapshot. The individual 8119/8120 post bodies still replay 404. The 260 M full-version size is close to CNET's 257MB `stoneage.zip`, but byte identity or identical packaging must not be assumed without a file/hash match.
- **Inium's own archived download page now resolves the official mirror topology and Hananet file identities.** `down.htm` on 2000-11-09 links CNET record `Software_Id=200009263856` and Hananet through `flashlinks.cgi` to the exact PDS record **`view.asp?app_id=20001031524596220&type=C03`**. By 2001-04 the page explicitly says the listed downloads are **formal-version** programs and trial service uses a separate menu. By 2001-08 the same official download page directly exposes **`http://stoneage.hananet.net/down/sa.exe`**, plus Gagamel `http://www.gagamel.com/web_data/download/stoneagebeta.zip` and GameTime `download.asp?GW_IDX=9&GW_Name=Online`. Because the official page classifies the listed downloads as formal-version mirrors, the `stoneagebeta.zip` filename alone must not be treated as proof of trial-client content.
- **Current archive boundary for the exact Korean mirror targets:** the Hananet flashlink wrapper is archived and frames the exact PDS record, but the inner PDS record variants replay 404. Wayback gives 24 zero-error Availability queries and zero snapshots for the mapped Hananet payload pair (`sa.exe` / 260 M formal, `sa_demo.exe` / 240 M trial), and direct replay of bare/`www` variants at the 2001-08-14 STAD timestamp is 404; earlier exact checks for Gagamel `stoneagebeta.zip` likewise produced no recoverable binary prefix. A separate Arquivo.pt CDX pass now covers **14 exact mirror URLs with 0 request errors and 0 indexed captures** for 2000–2005. These are archive-service-specific negative controls, not proof that republished mirrors or physical-media copies no longer survive elsewhere.
- **Inium separate-trial-menu probe is now a bounded partial negative control, not a closed route.** Final R5 queried 45 Availability combinations across the known sitemap/main-menu surface; 34 unique snapshots were reported available, 20 replayed successfully in raw `id_` form, and those 20 yielded zero genuine child-page candidates and zero trial/demo/download-token hits after Wayback toolbar links were excluded. Fourteen seed snapshots still failed to replay, so this does not prove the separate trial menu never existed. Do not rerun the same page/date matrix unless replay health improves or a new specific path/date appears.
- **Common Crawl is currently inconclusive, not negative evidence.** The R3 exact/prefix probe attempted 88 queries across the eight oldest listed indexes, but 83 failed with HTTP 503 or transport/SSL timeout. Zero recovered rows from that run must not be interpreted as “not archived”; retry only when the Common Crawl index service is healthy.
- **GameTime's exact record-9 payload path is now recovered from archived HTTP 302 response headers, but the payload bytes are not.** The archived 2000-12-08 GameTime StoneAge article still provides the older `/webzine/online/download.asp?name=스톤에이지` surface, and the legacy list binds the 2000-10-11 StoneAge Beta client to `num=9`. More importantly, archived replays of the later `/data/download.asp?GW_IDX=9&GW_Name=Online` endpoint at **2001-06-14, 2001-08-06, 2001-12-15 and 2002-02-08** all return HTTP 302 with the same Location target: **`http://www.gametime.co.kr/images/Online/pds/2001/02/onlStoneAge.zip`**. The control record `GW_IDX=76` similarly redirects to **`.../images/Online/pds/2001/02/stone_demo.exe`**. This resolves the record-9 filename/path as **`onlStoneAge.zip`** while leaving its size, version/build, checksum, internal tree and bytes unresolved. The stable record key and stable 2001/2002 redirect do not prove that the attachment is byte-identical to the 2000-10-11 Beta payload; Inium later classifies the mirror among formal-version programs, so replacement under a persistent record key remains possible.
- **Inium root-resource boundary:** archived Inium root HTML explicitly references `main.swf`, but Wayback Availability returns no SWF snapshot and direct replay at the known 2000-11-09 / 2001-02-01 root timestamps returns HTTP 404 for both bare and `www` hosts. Treat the preserved root HTML as evidence of the SWF path, not as recoverable SWF content.
- NetPower public scans provide near-period corroboration: September 2000 StoneAge pages independently show `www.hananet.net`; November 2000 StoneAge pages repeatedly show `enium` + `stoneage` and one OCR mode recovers partial `http://stoneage`. No executable/archive filename was recovered.
- Do **not** interpret the single-mode `32MB` OCR token as client size; its semantic context is unresolved.
- The 2001 GameTime guide CD remains a concrete install-media target, but a reproducible Internet Archive metadata probe returned zero items for both ISBNs and multiple title/GameTime query variants. That closes only the current IA metadata route, not the physical/public-preservation search.
- A 2025 Korean Lost Media preservation post proves that NetPower 2000-10 and other period magazine CDs still survive and can be extracted. The two listed NetPower 2000-10 discs contain many contemporary online clients but **not StoneAge**; no indexed public follow-up download was found. Treat this as preservation feasibility plus a negative control, not a StoneAge hit.
- Follow-up public-scan probes now close three additional near-period StoneAge article ranges without a file-token hit: **NetPower 2000-12 pp.173–176** yielded only cross-PSM `Stone Age`; **NetPower 2001-01 pp.185–190** yielded no StoneAge URL/file token (only an uncertain single-mode `32MB` plus a likely OCR-noise magazine-domain string); **NetPower 2001-02 pp.189–194** yielded only `powerzine.com` / OCR variants. Do not rerun these exact page ranges unless a better OCR/layout method or a specific visual token justifies it.
## GameTime bonus-CD public-library confirmation — 2026-09-19

- RISS formal bibliographic record `M10029631` identifies the GameTime `스톤 에이지 = Stone age` volume as **318 pages + one 12cm compact disc** and lists **National Library of Korea** as a holding institution.
- A reproducible KOLIS/RISS metadata probe now sharpens that record: KOLIS ISBN-10 search returns one 2001 general-book record marked **offline** and reports **2 libraries holding it**; the same result exposes RISS alias `U10029631`. That alias resolves to the same RISS detail record, whose canonical link is `M10029631` and whose detail URL carries control number `9b505f870e768aa6ffe0bdc3ef48d419`.
- The KOLIS holding layer is now resolved through edition key `24118251`, work number `UW20191223432` and `bibKey=10041033`. Its two current catalog holders are **National Library of Korea / 국립중앙도서관** (`recKey=1`, library code `011001`) and **Seogwipo Eastern Library / 서귀포시동부도서관** (`recKey=12909233`, library code `149013`). RISS additionally exposes National Library local bib number **`KMO200119860`**.
- KOLIS MARC closes the bibliographic identity further: `001=UB20011039873`, `012=KMO200119860`, `035=(011001)KMO200119860`, and MARC `300` explicitly records **318 pages + one 12cm compact disc**. The linked contents endpoint is live and starts chapter 1 with `설치하기` / installation on page 8.
- This upgrades the 2001 bonus-CD path from retailer-only evidence to a concrete two-library union-catalog holding with independently replayable MARC and contents metadata. It still does **not** prove that either accompanying CD is presently intact, separately accessioned, digitized or publicly downloadable; holding the bibliographic book object must not be equated with verified physical-disc survival.
- Aladin (`2001-01-01`) and YES24 (`2001-04-30`) use different catalog dates for the same 318-page ISBN-13 `9788995182123` volume; RISS gives year 2001 and ISBN-10 `8995182121`. Treat these as date-metadata variants, not separate guide/CD editions.
- Derived catalog probes: `research/recovered/STONEAGE-GAMETIME-2001-LIBRARY-SUPPLEMENT-R1.txt` and `research/recovered/STONEAGE-GAMETIME-2001-KOLIS-HOLDINGS-R1.txt`.
- **This public union-catalog sub-track is now closed at the bibliographic layer.** Reopen it only if a holder-specific OPAC/accession record, current supplementary-disc status, disc-label image, distinct non-book record or public preservation copy appears. Routine ISBN/title searches are no longer useful.
## Korean public-media recovery corpus narrowing — 2026-09-19

- A reproducible remote directory scanner now reads only ISO-9660/Joliet directory sectors from public carrier images via HTTP Range requests; complete proprietary disc images are not downloaded into or committed to the repository.
- **PC Game Magazine:** 21 public carriers spanning **2000-09 through 2001-12** were fully enumerated with **0 scan errors, 0 truncation and 0 StoneAge/sa_demo/sa.exe/enium path hits**.
- **GamePia:** 23 carriers across issues **No.58–No.69**, crossing and extending beyond the Korean 2000 trial/formal launch window, were fully enumerated with **0 scan errors, 0 truncation and 0 StoneAge-path hits**.
- **NetPower 2001.12:** two public carriers were fully enumerated with **0 StoneAge-path hits**. These are exact-carrier negative controls only; they do not exclude other issues/media.
- Internet Archive exact-token reverse search now checks **222 item records with 0 request errors**, including the newly recovered GameTime trial filename **`stone_demo.exe`**. The exact `stone_demo.exe` query produced 7 search-index hits, but file-list verification still produced **0 exact target filename matches**; all **11** 180–320 MiB candidates are size-only false positives. Treat this as a closed IA metadata/file-list route for the current exact token set, not proof the payload is globally lost.
- A zero-error 2000–2002 Wayback CDX prefix census returned **362 rows / 181 unique URLs** across 12 distribution-directory variants. Exact Hananet `/down/` and CNET `/pc/games/online/` prefixes returned **0 rows**, while Gagamel, GameTime and Inium prefixes returned real archived records; therefore the Hananet/CNET results are meaningful Wayback directory-level negative controls for those exact prefixes/date range, not a global absence claim.
- The **GameTime PDS host** was then added as a 13th CDX prefix. `pds.gametime.co.kr` returns only **11 archived URLs** in 2000–2002, all image/JPEG assets; none is a client executable/archive. The full census is now **373 rows / 192 unique URLs / 0 query errors**. This closes the current Wayback prefix-enumeration route for the PDS host while leaving off-Wayback mirrors/reposts open.
- **GameTime StoneAge record lineage and the migrated record-9 payload path are now materially resolved.** The 2001-07-01 `스톤에이지` search page identifies `GW_IDX=76` as `스톤에이지 체험판 클라이언트`, filename **`stone_demo.exe`**, registered **2001-02-12 19:45:00**, list size **234MB**; its description says the formal version is roughly 260MB and the trial version roughly 240MB, with five-day trial access and separate trial characters/pets. `GW_IDX=34` is a **manual update**, filename **`StoneAge.zip`**, registered **2000-11-06 11:21:00**, list size **0.4MB**; an independent 2001-04-17 GameTime page labels it **0.42MB** and tells users to delete `sa_*.exe`, `server_*.ini` and `stoneage.exe` before copying it. The older GameTime webzine archive adds a **2000-10-11 `스톤 에이지 베타 버젼용 클라이언트`** row with count **7,898**, machine-bound directly to `content.asp?name=&num=9&ref=37&page=4`. The same legacy system machine-binds the StoneAge manual update to `num=34`, while the migrated data center preserves that same object as `GW_IDX=34`, strongly supporting record-key continuity. Archived HTTP 302 headers now close the next layer: **`GW_IDX=9` redirects consistently to `/images/Online/pds/2001/02/onlStoneAge.zip`**, while **`GW_IDX=76` redirects to `/images/Online/pds/2001/02/stone_demo.exe`**. Exact Wayback Availability checks for both payload paths return zero available captures for the tested dates; `onlStoneAge.zip` CDX returns zero rows, while `stone_demo.exe` CDX attempts timed out and remain inconclusive. Thus record-9 filename/path is resolved, but its size/version/checksum/tree/bytes and possible attachment replacement between the 2000 Beta listing and later formal-mirror use remain unresolved.
- Canonical corpus record: `research/clients/STONEAGE-KOREA-2000-2001-PUBLIC-MEDIA-CORPUS-R1.md`.

## Immediate next actions

1. **Recover bytes or surviving mirrors from the now-exact Korean distribution tokens.** Highest-value keys are CNET `/pc/games/online/stoneage.zip` (257MB), Hananet PDS **`app_id=20001031524596220&type=C03`**, Hananet formal-version direct path **`stoneage.hananet.net/down/sa.exe`**, Hananet trial **`sa_demo.exe`**, Gagamel `stoneagebeta.zip`, GameTime trial **`/images/Online/pds/2001/02/stone_demo.exe` / GW_IDX=76**, and GameTime record 9 **`/images/Online/pds/2001/02/onlStoneAge.zip` / GW_IDX=9 / legacy num=9**. Treat GameTime `GW_IDX=34 / StoneAge.zip` as a 0.4/0.42MB manual update, not a full-client candidate. Compare candidate clients only by bytes/hashes and internal trees; reject unrelated arcade/MAME `stoneage.zip` hits.
2. **Recover the bytes behind GameTime `onlStoneAge.zip`.** Archived 302 headers now resolve `GW_IDX=9` to the exact payload URL **`http://www.gametime.co.kr/images/Online/pds/2001/02/onlStoneAge.zip`**. Search that exact basename/path across mirrors, archive file lists, old FTP/web directories, preservation indexes and reposts; use the legacy `num=9` StoneAge Beta row and the later Inium formal-mirror classification as provenance context, not as proof of one unchanged byte object. The GameTime guide union-catalog route remains closed at the bibliographic layer unless new supplementary-disc evidence appears.
3. **Continue JSS 1999 beta/retail/launcher recovery in parallel.** It remains the historical origin target even though Korean 2000 now has stronger mass-replication recovery odds.
4. **Keep `〖2.5纯净〗` `tid=2132`, Korean 1.74 and Japanese 1.74a as secondary clean-client targets.** Version labels and forum labels remain clues, not byte provenance.
5. **On any newly recovered candidate bytes, stop broad searching and run the clean-client acceptance test immediately:** source chain, hashes, complete file tree, executable metadata, endpoints/patchers, resource generations and cross-copy contamination checks.
6. **Treat the recovered mixed 2.5 bundle only as a provenance-safe resource-format bridge.** Do not reopen the ordinary NPC/family/race/VIP/combat queues unless cleaner/earlier evidence exposes a concrete gap.
7. **Keep the thirteen recovered function-set tokens that do not join to any pinned source table as explicit source/data skew.** A similarly named later/unused source file is not enough to invent the missing implementation.
8. **Keep archaeology separate from redesign and de-prioritize nontechnical history** unless it directly unlocks client bytes, provenance or a technical ambiguity.

## Continuity status

- Repository: `chinaneedM/stoneage-rebuild`
- Default branch: `main`
- Visibility: public
- Authority: latest GitHub remote state is the single source of truth for project continuity.
- Canonical restart protocol: `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`

## Blockers

No repository or workflow blocker.

The project still lacks a provenance-preserving **publicly obtainable** 1999 JSS retail disc image/dump and September 1999 beta binary. The Korean **Inium/Hananet/CNET 2000–2001** recovery track now has CNET's exact payload path/name (`/pc/games/online/stoneage.zip`, 257MB) and Hananet's exact full/trial mappings (`8119` / 260 M / `sa.exe`; `8120` / 240 M / `sa_demo.exe`), but still lacks recoverable client bytes, hashes/file tree, and byte-level equivalence evidence between the independently packaged mirrors. Korean `1.74` and Japanese `1.74a` likewise remain unrecovered, so none of these bridge targets has yet established byte-level relationship to JSS. LIFESTORM II and StoneAge JANs are directly resolved from public package photographs, but the StoneAge physical-package blocker remains the missing exact model/type code, disc identities and matrix identifiers; exact JAN/model searches still yield no trustworthy `JV...` field and the 13 Mercari originals are HTTP-403-blocked here. The beta web-recovery blocker remains a nearly complete application-page path; the Retromags No.015 object is identified down to filename, size, MD5 and seedbox target, but the scan body is still unreachable. Direct Wayback binary retrieval is independently blocked in the execution environment by DNS resolution failure, so the archived JSS `stoneage.exe` still has no recovered bytes. The developer-lineage track now has a named, independently cross-checked JSS/StoneAge staff lead in Yuki Tamura, but the original StoneAge credit list and exact staff-role mapping remain unresolved. The retail/client search retains `sa.exe`, `updated`, and `CheckForUpdate` only as descendant-derived search traits until original JSS material confirms each one independently. The binary/media blocker remains the principal Phase 0 constraint.
