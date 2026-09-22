# Current State

Last updated: 2026-09-22

## Current phase

**Phase 0 — Earliest Clean Client Recovery & Reverse Engineering (Taiwan 1.0 clean baseline accepted; technical extraction active)**

The independent GitHub repository and continuity scaffold are established on remote `main`. The project has now recovered and byte-verified its first early provenance-preserving retail client specimen: **Taiwan Waei/JSS StoneAge v1.0, Redump disc 104630**. This artifact is not the 1999 JSS origin, but it is early, publicly obtainable, physically attributable and complete enough to activate the protocol's next stage: use it as the primary current reverse-engineering specimen while continuing targeted recovery of the 1999 JSS and Korean operator branches for lineage comparison.

Historical archaeology remains useful only when it helps authenticate, date, compare, or interpret a recovered client. Package price, retail product-number, staff-history, and similar research are **not primary objectives** unless they directly improve client recovery or technical attribution.

## Confirmed project direction

- **Primary path: recover the earliest clean client first, then reverse engineer it.**
- "Clean client" means an original/operator-distributed or otherwise provenance-preserving client, installer, disc image, or complete file tree with no known private-server repack, injected launcher, custom patcher, replaced assets, or undocumented modification. If absolute purity cannot be proven, candidates must be graded and compared rather than silently accepted.
- Search priority remains **earliest freely/publicly obtainable artifact**, not the historically earliest version at any cost. A provenance-preserving **Taiwan Waei/JSS v1.0 retail disc** is now recovered and accepted as the primary current technical baseline. Korean **Inium 2000** exact distribution tokens remain high-value cross-region recovery targets, and JSS 1999 remains the historical-origin target; neither may be treated as byte-identical to Taiwan 1.0 without direct comparison.
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

## Korean retail game-CD/package recovery lead — 2026-09-19

- Contemporary DailyGame / Daily eSports reporting dated **2000-10-27** says Inium had signed a supply contract with Samsung PC-education-center operator **Mentec (`멘테크`) for roughly 60,000 sale packages (`판매용 패키지`)**, with planned nationwide retail distribution through **Yongsan PC-game wholesalers**. This moves the physical-package track back into the original October 2000 Korean trial/distribution period. The contract proves a mass-distribution plan, not that every contracted unit was ultimately manufactured or sold.
- Contemporary Electronic Times reporting dated **2001-05-04** says StoneAge users could buy a **game CD in Yongsan and similar retail locations with a two-month free-use coupon included**: https://www.etnews.com/200104300317
- Independent GameMeca reporting dated **2001-07-09** says Inium's registered StoneAge population included **paid members, trial-version registrants, and package purchasers (`패키지 구입자`)**: https://www.gamemeca.com/view.php?gid=3718
- Together these establish an independently sold, mass-distribution Korean StoneAge retail/package game-CD channel from **October 2000 through 2001**. Do **not** merge this object with the GameTime Perfect Guide bonus CD without artifact-level evidence.
- The retail package's exact publisher/SKU/catalog number, price, box art, disc label/matrix code, client version/build, installer filename, filesystem, checksum and relationship to Hananet/CNET/GameTime copies remain unresolved.
- Canonical target record: `research/clients/STONEAGE-KOREA-2001-RETAIL-GAME-CD-R1.md`.
- Status: **TARGET-A — mass-distribution physical-media bridge; exact media identity/public bytes not yet recovered.**

## Korea 2000 recovery-surface narrowing — 2026-09-19

- Contemporary references resolve **CNET Korea's download root** to `http://korea.cnet.com/downloads/` and the **Hananet software repository** to `http://pds.hananet.net`.
- **CNET StoneAge child-record and payload identity are now recovered:** preserved 2000-11-10 and 2001-01-24 download-index snapshots point StoneAge to `Software_Id=200009263856`; archived detail pages resolve the file-size label **257MB** and the download target **`/pc/games/online/stoneage.zip`**, with maker homepage `stoneage.enium.co.kr`. Exact Wayback Availability checks for that ZIP path currently return zero archived payload snapshots, so the remaining CNET gap is the actual ZIP bytes / surviving mirror, not the filename or historical portal path.
- **Hananet StoneAge child-site and distribution records are now recovered:** the GamePlus chain resolves to **`http://stoneage.hananet.net/main.htm`**, and all menu pages `1.htm`, `2.htm`, `2_2.htm`, `2_3.htm`, `2_4.htm`, `2_5.htm` have now been replayed. The archived `2.htm` explicitly instructs users to insert the StoneAge **CD into the CD-ROM**, wait for the automatic install menu, follow Setup, and notes DirectX 6.1. The recovered `2_5.htm` exposes StoneAge boards `GAM2:STAD`, `STAF`, `STAN`.
- **Hananet STAD provides two exact distribution records dated 2001-02-10 and now directly maps both records to file paths in its archived HTML source:** record **8119**, `온라인게임 스톤에이지 정식 버전` (official/full version), **260 M** → `http://stoneage.hananet.net/down/sa.exe`; record **8120**, `온라인게임 스톤에이지 체험 버전` (trial version), **240 M** → `http://stoneage.hananet.net/down/sa_demo.exe`. In the 2001-08-14 preserved STAD source these two direct-file button rows are inside an **HTML comment block**, so they establish historical title/size/file mapping but must not be described as visible/clickable buttons at that snapshot. The individual 8119/8120 post bodies still replay 404. The 260 M full-version size is close to CNET's 257MB `stoneage.zip`, but byte identity or identical packaging must not be assumed without a file/hash match.
- **Inium's own archived download page now resolves the official mirror topology and Hananet file identities.** `down.htm` on 2000-11-09 links CNET record `Software_Id=200009263856` and Hananet through `flashlinks.cgi` to the exact PDS record **`view.asp?app_id=20001031524596220&type=C03`**. By 2001-04 the page explicitly says the listed downloads are **formal-version** programs and trial service uses a separate menu. By 2001-08 the same official download page directly exposes **`http://stoneage.hananet.net/down/sa.exe`**, plus Gagamel `http://www.gagamel.com/web_data/download/stoneagebeta.zip` and GameTime `download.asp?GW_IDX=9&GW_Name=Online`. Because the official page classifies the listed downloads as formal-version mirrors, the `stoneagebeta.zip` filename alone must not be treated as proof of trial-client content.
- **Current archive boundary for the exact Korean mirror targets:** the Hananet flashlink wrapper is archived and frames the exact PDS record, but the inner PDS record variants replay 404. Wayback gives 24 zero-error Availability queries and zero snapshots for the mapped Hananet payload pair (`sa.exe` / 260 M formal, `sa_demo.exe` / 240 M trial), and direct replay of bare/`www` variants at the 2001-08-14 STAD timestamp is 404; earlier exact checks for Gagamel `stoneagebeta.zip` likewise produced no recoverable binary prefix. A separate Arquivo.pt CDX pass now covers **18 exact mirror URLs with 0 request errors and 0 indexed captures** for 2000–2005, including both bare/`www` variants of GameTime `onlStoneAge.zip` and `stone_demo.exe`. These are archive-service-specific negative controls, not proof that republished mirrors or physical-media copies no longer survive elsewhere.
- **Inium separate-trial-menu probe is now a bounded partial negative control, not a closed route.** Final R5 queried 45 Availability combinations across the known sitemap/main-menu surface; 34 unique snapshots were reported available, 20 replayed successfully in raw `id_` form, and those 20 yielded zero genuine child-page candidates and zero trial/demo/download-token hits after Wayback toolbar links were excluded. Fourteen seed snapshots still failed to replay, so this does not prove the separate trial menu never existed. Do not rerun the same page/date matrix unless replay health improves or a new specific path/date appears.
- **Common Crawl remains inconclusive, not negative evidence.** The updated R3 exact/prefix probe now includes the GameTime `onlStoneAge.zip`, `stone_demo.exe` and `/images/Online/pds/2001/02/` directory targets. It attempted **112 queries** across the eight oldest listed indexes, but **109 failed** with HTTP 503 or transport timeout; the three non-error queries returned no relevant rows. Zero recovered rows therefore cannot be interpreted as “not archived”. Retry only when the Common Crawl index service is healthy.
- **GameTime's exact record-9 payload path is now recovered from archived HTTP 302 response headers, but the payload bytes are not.** The archived 2000-12-08 GameTime StoneAge article still provides the older `/webzine/online/download.asp?name=스톤에이지` surface, and the legacy list binds the 2000-10-11 StoneAge Beta client to `num=9`. More importantly, archived replays of the later `/data/download.asp?GW_IDX=9&GW_Name=Online` endpoint at **2001-06-14, 2001-08-06, 2001-12-15 and 2002-02-08** all return HTTP 302 with the same Location target: **`http://www.gametime.co.kr/images/Online/pds/2001/02/onlStoneAge.zip`**. The control record `GW_IDX=76` similarly redirects to **`.../images/Online/pds/2001/02/stone_demo.exe`**. This resolves the record-9 filename/path as **`onlStoneAge.zip`** while leaving its size, version/build, checksum, internal tree and bytes unresolved. The stable record key and stable 2001/2002 redirect do not prove that the attachment is byte-identical to the 2000-10-11 Beta payload; Inium later classifies the mirror among formal-version programs, so replacement under a persistent record key remains possible. A long-window exact CDX pass covering **2000–2012** then queried 16 scheme/host/`:80` variants with zero request errors: all **8 `onlStoneAge.zip` variants return 0 rows**, while all 8 `stone_demo.exe` variants canonicalize to one **2003-04-26 HTTP 404** capture (`www.gametime.co.kr:80`, 2,112-byte HTML error object). Thus the record-9 file has no Wayback CDX capture even in the extended window, and the trial payload path is explicitly dead by 2003-04-26; neither result proves off-Wayback copies are lost.
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
- Internet Archive exact-token reverse search now checks **222 item records with 0 request errors**. The exact `stone_demo.exe` query produced 7 search-index hits, but file-list verification still produced **0 exact target filename matches**; all **11** 180–320 MiB candidates are size-only false positives. The newly recovered **`onlStoneAge.zip`** basename and full `images/Online/pds/2001/02/onlStoneAge.zip` path each return **0 IA search results**. Treat this as a closed IA metadata/file-list route for the current exact token set, not proof the payload is globally lost.
- A zero-error 2000–2002 Wayback CDX prefix census returned **362 rows / 181 unique URLs** across 12 distribution-directory variants. Exact Hananet `/down/` and CNET `/pc/games/online/` prefixes returned **0 rows**, while Gagamel, GameTime and Inium prefixes returned real archived records; therefore the Hananet/CNET results are meaningful Wayback directory-level negative controls for those exact prefixes/date range, not a global absence claim.
- The **GameTime PDS host** was then added as a 13th CDX prefix. `pds.gametime.co.kr` returns only **11 archived URLs** in 2000–2002, all image/JPEG assets; none is a client executable/archive. After recovering the exact redirect target, both `www` and bare **`/images/Online/pds/2001/02/`** prefixes were added as two further queries; both completed successfully with **0 rows**. The latest census therefore covers **15 prefixes / 373 rows / 192 unique URLs**; one transient timeout affects only `www.stoneage.hananet.net/down/` and does not weaken the two successful GameTime image-PDS zero-row results. This closes the current Wayback prefix-enumeration route for the exact GameTime payload directory while leaving off-Wayback mirrors/reposts open.
- **GameTime StoneAge record lineage and the migrated record-9 payload path are now materially resolved.** The 2001-07-01 `스톤에이지` search page identifies `GW_IDX=76` as `스톤에이지 체험판 클라이언트`, filename **`stone_demo.exe`**, registered **2001-02-12 19:45:00**, list size **234MB**; its description says the formal version is roughly 260MB and the trial version roughly 240MB, with five-day trial access and separate trial characters/pets. `GW_IDX=34` is a **manual update**, filename **`StoneAge.zip`**, registered **2000-11-06 11:21:00**, list size **0.4MB**; an independent 2001-04-17 GameTime page labels it **0.42MB** and tells users to delete `sa_*.exe`, `server_*.ini` and `stoneage.exe` before copying it. The older GameTime webzine archive adds a **2000-10-11 `스톤 에이지 베타 버젼용 클라이언트`** row with count **7,898**, machine-bound directly to `content.asp?name=&num=9&ref=37&page=4`. The same legacy system machine-binds the StoneAge manual update to `num=34`, while the migrated data center preserves that same object as `GW_IDX=34`, strongly supporting record-key continuity. Archived HTTP 302 headers now close the next layer: **`GW_IDX=9` redirects consistently to `/images/Online/pds/2001/02/onlStoneAge.zip`**, while **`GW_IDX=76` redirects to `/images/Online/pds/2001/02/stone_demo.exe`**. Exact Wayback Availability checks for both payload paths return zero available captures for the tested dates; `onlStoneAge.zip` CDX returns zero rows, while `stone_demo.exe` CDX attempts timed out and remain inconclusive. Thus record-9 filename/path is resolved, but its size/version/checksum/tree/bytes and possible attachment replacement between the 2000 Beta listing and later formal-mirror use remain unresolved.
- **Cross-archive boundary for the newly exact GameTime payloads:** Wayback Availability returns zero captures for the tested `onlStoneAge.zip` and `stone_demo.exe` dates; exact CDX returns zero rows for `onlStoneAge.zip`, while the two `stone_demo.exe` exact-CDX attempts timed out and remain inconclusive. IA item/file-list search returns zero `onlStoneAge.zip` hits and zero exact filename matches across the 222 inspected items. Arquivo.pt returns zero indexed captures across all 18 exact mirror targets, including both GameTime payloads. Wayback prefix enumeration of both bare/`www` `/images/Online/pds/2001/02/` directories succeeds with zero rows. The updated Common Crawl run explicitly includes the new exact payload URLs, but **109/112 queries failed** with 503/timeout errors; it remains inconclusive and must not be counted as an archive-negative.

- **Current SourceForge mirror/repost lane is now classified, not promoted.** A bounded HTTP-Range scan of all six root archives in the current SourceForge project `stoneage` (`patch_0.zip` through `patch_5.zip`) read only ZIP tail/central-directory metadata: **6/6 archives scanned, 0 failures, 1,285,465 bytes requested total, 0 exact target hits and 164 StoneAge resource-container hits**. The archives expose large split resource trees dominated by `map/`, `data/`, `lua/` and `path/` plus `real.bin` / `adrn.bin` / `spr.bin` families, but no `stoneage.exe`, `sa.exe`, `sa_demo.exe`, `stone_demo.exe`, `onlStoneAge.zip`, `stoneagebeta.zip` or full-client `StoneAge.zip` entry. Treat this 2026-hosted project as a **descendant resource/patch corpus only** unless independent provenance appears; it does not satisfy clean-client recovery and should not be re-searched as an exact-client mirror. Derived metadata: `research/recovered/STONEAGE-SOURCEFORGE-ZIP-INDEX-R1.txt`.

- **Descendant executable false-positive control:** a public ANY.RUN report exposes a later `StoneAge.exe` with `OriginalFileName=Sa.exe`, MD5 `A1A524D45C90ED3B7537A254B8757740`, SHA1 `8C89E619399AFDF7F0F706722C3E648FA2A99654` and SHA256 `9C019D9FAB9C0DC37A37A67519CA5080AE43EC2B2A84B915A24B742512A6A7CA`. Its reported PE/version metadata is Chinese Simplified, `Copyright c 2010`, version `1.0.0.1` and a 2019 PE timestamp; GitHub exact-hash search returns zero mirrors. Treat these hashes as a **descendant exclusion fingerprint**, not as evidence for the 2000–2001 Korean client. Record: `research/recovered/STONEAGE-DESCENDANT-EXECUTABLE-HASH-CONTROL-R1.md`.

- Canonical corpus record: `research/clients/STONEAGE-KOREA-2000-2001-PUBLIC-MEDIA-CORPUS-R1.md`.

### Korean NetPower public-carrier resolution — 2026-09-19

- A later preserved NetPower contents index is now used only as a **carrier-target map**, not as proof of supplement contents. It places StoneAge coverage in **2000-09 p.87, 2000-11 p.99, 2000-12 p.173, 2001-01 p.185 and 2001-02 p.189**.
- Internet Archive uploader-neighborhood discovery identified exact public carrier items for **NetPower 2000-09, 2000-11 and 2001-02** under the same preservation uploader that hosts the known Korean PCGM/GamePia corpus.
- Those three exact NetPower items have now been recursively enumerated at ISO-9660/Joliet directory level through HTTP Range reads only. Each issue exposes **two disc volumes represented as IMG + ISO (four image representations per issue)**. Across all twelve representations: **0 scan errors, 0 truncation and 0 StoneAge/sa_demo/sa.exe/enium path hits**. These are strong file-level negative controls for those exact preserved carriers; they do not prove every physical pressing or another supplement edition was identical.
- The earlier **NetPower 2001.12** public pair remains a separate exact-carrier negative control: two ISO images, 0 scan errors, 0 truncation and 0 StoneAge-path hits.
- A corrected R2 Internet Archive metadata probe now isolates the still-missing **2000-12 and 2001-01** issues. Across the two known preservation-uploader neighborhoods plus exact global identifier/title/description searches, both months return **0 exact carrier items with 0 query errors**. This closes the current IA metadata route for those two issues only; it is not evidence that the discs no longer survive in private collections or another preservation account.
- The active Korean classic-CD collector lane therefore remains useful primarily for **NetPower 2000-12 / 2001-01** and other unindexed carriers, while the **GameTime StoneAge Perfect Guide CD** remains the stronger direct carrier target because surviving bibliographic evidence explicitly describes a StoneAge installation/demo disc.
- Derived records: `research/recovered/STONEAGE-NETPOWER-2000-09-DISC-SCAN-R1.txt`, `research/recovered/STONEAGE-NETPOWER-EXACT-TARGET-DISC-SCAN-R1.txt`, and `research/recovered/STONEAGE-NETPOWER-IA-UPLOADER-NEIGHBORHOOD-R2.txt`.
- **Operational consequence:** do not rerun the exact public NetPower 2000-09 / 2000-11 / 2001-02 / 2001.12 carriers unless a new parser or byte-level question changes the task. Pursue 2000-12 / 2001-01 through new holder/account evidence, and prioritize the GameTime guide CD plus the exact operator-distribution payload tokens.

## Taiwan 1.0 clean-client acceptance — 2026-09-19

- **A provenance-preserving early retail specimen is now recovered and accepted for technical reverse engineering.** Internet Archive item `stoneage_tw_2000_win` contains packaging/disc photographs and the original preservation archive `CD_DIC.rar` (842,125,501 bytes; MD5 `b37a4a47f4eb608cac67e4ddf7a1621a`; SHA1 `b8cf92720b6ec8b3f46ea2e9bfcda986d21e7ded`). The archive is non-solid, unencrypted and contains a DiscImageCreator dump set including `STONEAGE.bin`, CUE/CCD/SUB/SCM and dump logs.
- **Physical/media identity is independently pinned.** Redump disc **104630** identifies an IBM-PC CD game, **Version 1.0 / Original**, one MODE1/2352 track. The mastering ring is `華義國際股份有限公司 石器時代 V1.0 P-RPG-0008`, with mastering SID `IFPI LE92`, mould SID `IFPI·9W10`, barcode `4 710739 350098`, publisher Waei International and developer Japan System Supply. The DiscImageCreator submission reports **0 errors** and `None found` for copy protection.
- **Recovered track bytes match Redump exactly.** `STONEAGE.bin` is 523,449,360 bytes with CRC32 `e4638c81`, MD5 `b477bfc2b62527b255ab9f822349dc14`, SHA1 `d0f270163772eb587185a65e24a3f7e565263f2f` and repository-derived SHA256 `905ee6ad89b8ca7f55a5c1132eede99a15ee7cb1b868f9b0b398fb0c76cfd159`. Redump's SHA1/MD5/SFV/CUE exports reproduce the same track identity.
- **The disc contains a complete directly readable StoneAge client tree.** ISO/Joliet enumeration yields **421 entries: 10 directories + 411 files**, with 454,864,199 logical file bytes. Autorun launches `Install.exe`; the StoneAge subtree includes `Setup.exe`, `Setup.ini`, `StoneAge.exe`, `sa_3.exe`, resources, BGM/SFX and battle-map assets. The separately packaged bonus game `人在江湖` and music previews are distinct directories and are not silently folded into the StoneAge client.
- **Core executable identities are now pinned:** `StoneAge/StoneAge.exe` = 409,600 bytes, MD5 `c93093692fefa9b2d2823c3eda3c38ea`, SHA1 `54654ec46212883b2bb61aeb950fdc2ce4c049b7`, SHA256 `9b280068063b4398e5c8901b881daa1f13576201e475efede3127b59cdad2867`; `StoneAge/sa_3.exe` = 425,984 bytes, MD5 `6b1574332f42261151826a7039ad4f2c`, SHA1 `f3999d1331374abe60c1a11a70c08bc9108d6873`, SHA256 `cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a`. Both are x86 PE files and their PE timestamps fall on 2000-04-11 UTC.
- **The early client independently confirms runtime/search traits that were previously descendant-derived only.** The accepted v1.0 disc contains both `StoneAge.exe` and an `sa_3.exe` executable. Bounded string extraction recovers `stoneage.waei.net`, `www.waei.net` and `mail.hwaei.com`. `StoneAge/Setup.ini` identifies `AppName=石器時代` and leaves `UpdateURL=` empty.
- **The early resource generation is concrete and immediately comparable with the 2.5 bridge corpus:** `StoneAge/data/real_1.bin` (315,842,228 bytes), `adrn_1.bin` (10,079,680), `spr_1.bin` (2,889,630), `spradrn_1.bin` (5,568), plus `battle_1.bin`, 218 small `battle*.sab` map records, BGM/SFX WAVs and text address tables.
- **Acceptance classification:** this artifact is accepted as a **clean Taiwan 1.0 retail client baseline / S-grade media specimen** for reverse engineering. It is an early localized JSS-derived branch, not proof of byte identity with the 1999 Japanese retail/beta or the Korean 2000 clients. Those branches remain comparison/recovery targets rather than blockers on technical extraction.
- Canonical derived records: `research/recovered/STONEAGE-IA-EXACT-ARTIFACT-AUDIT-R1.txt`, `research/recovered/STONEAGE-TW2000-PRESERVATION-R1.txt`, and `research/recovered/STONEAGE-TW2000-CLEAN-CLIENT-ACCEPTANCE-R1.txt`.

## Taiwan 1.0 runtime/resource technical resolution — 2026-09-19

- The accepted Taiwan v1.0 disc has now been probed directly with two reproducible, derived-only CI passes: `STONEAGE-TW10-TECHNICAL-PROBE-R1.txt` and `STONEAGE-TW10-RUNTIME-DEEP-R1.txt`. All proprietary bytes remain transient.
- **Executable roles are now materially resolved.** `StoneAge.exe` imports `WININET.dll` and `CreateProcessA`; its code has direct references to `stoneage.waei.net`, `/saupdate/newest.txt`, `/saupdate/%s`, the `data\\*_*.bin` generation patterns and the `updated` marker. Treat it as the early Waei **update/launch front-end**, not the game runtime. `sa_3.exe` imports DirectDraw/DirectInput/WinMM-era runtime libraries, contains `ClientLogin` / `CharLogin`, battle-map paths and core resource paths, and is the **game runtime**.
- `StoneAge.exe` and `sa_3.exe` are not rename variants: the minimum-length same-position byte ratio is only **0.029995**, all four PE section hashes differ, and the runtime has roughly twice the raw `.text` size.
- A dedicated PE import-table parser resolves a discrepancy in the generic `objdump` text parser: `sa_3.exe` **does statically import `WSOCK32.dll`**, with 15 functions including `WSAStartup`, `socket`, `gethostbyname`, `inet_addr`, `connect`, `select`, `send`, `recv` and `closesocket`; it also imports `DSOUND.dll` by ordinal. Together with `ClientLogin` / `CharLogin` code references, this pins the early game runtime's direct Winsock networking path. The earlier deep-probe line that omitted WSOCK32/DSOUND is a parser limitation, not historical evidence.
- **The core graphics/resource container schema is already continuous from v1.0 to the recovered 2.5 bridge.** The existing 2.5 REAL/ADRN parser consumes Taiwan `real_1.bin / adrn_1.bin` unchanged: 80-byte ADRN records, 125,996 active records, fully contiguous REAL coverage, zero gaps/overlaps/tail. The same eight flag-0 special/uncompressed records and two signed-dimension anomalies seen in 2.5 are already present structurally in v1.0.
- The existing SPR/SPRADRN parser likewise consumes Taiwan `spr_1.bin / spradrn_1.bin` unchanged: **464/464 records parse successfully**, with exact next-offset boundaries and the same 3,492 sentinel bitmap frames later observed in 2.5. This establishes schema continuity; exact content inheritance still requires byte-level cross-generation diffing.
- `battle_1.bin` is now proven to be a strict concatenation container: **233/233** address-table entries match their individual `battle*.sab` files byte-for-byte, with no gaps, overlaps or tail.
- `sound_1.bin` is also structurally contiguous across 114 address-table entries, but only 107 match the separately stored WAV files exactly. Seven `sak_*` entries differ; several differ immediately after the WAV header and/or have different lengths, while two same-sized entries diverge later. Treat the container and loose WAV directory as distinct audio variants for those records, not as parser failure.
- **Operational consequence:** the next technical priority is a direct Taiwan v1.0 ↔ preserved 2.5 resource diff using verified transient bytes, beginning with ADRN/REAL and SPR/SPRADRN prefix/content inheritance. Runtime network-path resolution remains a parallel narrow task, not a blocker on resource archaeology.

## Taiwan v1.0 -> 2.5 direct resource inheritance — 2026-09-19

- A verified transient-byte diff now compares the accepted Taiwan v1.0 retail resource generation directly against the preserved 2.5 bridge bundle; neither proprietary corpus is committed.
- **ADRN is an exact prefix inheritance.** Taiwan v1.0 has 125,996 80-byte ADRN records; all **125,996/125,996** are byte-for-byte identical to the first 125,996 records of 2.5 `adrn_15.bin`. Every v1.0 bitmap number is present in 2.5, with identical geometry and an identical referenced REAL payload.
- **REAL is an exact byte prefix inheritance.** The full **315,842,228 bytes** of Taiwan `real_1.bin` are exactly the first 315,842,228 bytes of 2.5 `real_15.bin`; 2.5 then extends the container to 763,908,374 bytes. No v1.0 REAL payload is altered in this comparison.
- **SPR/SPRADRN is likewise an exact prefix inheritance.** All **464/464** Taiwan SPRADRN records and every corresponding animation segment are byte-identical to the first 464 records/segments in the 2.5 corpus. The full **2,889,630 bytes** of Taiwan `spr_1.bin` are exactly the prefix of 2.5 `spr_4.bin`, which grows to 5,588,120 bytes.
- This upgrades the previous schema-continuity finding to a direct lineage result for these resources: the preserved 2.5 bridge retains the complete Taiwan v1.0 graphics/animation corpus and extends it by appending later records/data. It does **not** by itself prove that every other client subsystem or regional branch followed the same append-only policy.
- Canonical derived report: `research/recovered/STONEAGE-TW10-VS-25-RESOURCE-DIFF-R1.txt`.
- **Operational consequence:** use Taiwan v1.0 resource IDs as stable ancestral IDs when comparing later preserved client data, while separately testing maps, battle maps, audio, executables and server-side tables rather than assuming append-only inheritance globally.

## Taiwan v1.0 installer/map-cache narrowing — 2026-09-19

- The InstallShield hypothesis has now been tested directly against the verified Taiwan v1.0 retail disc. `StoneAge/data1.cab` is readable by `unshield`, but its extracted contents are **13 InstallShield 6 engine/support files only** (runtime DLLs, language/support files and palette); it contains **0 map-like game files**. `data1.hdr`, `data2.cab`, `layout.bin`, `setup.inx` and `Setup.exe` are installer control/support material, not a hidden ordinary map payload.
- Therefore the runtime literal **`map\\%d.dat` must not be explained as an installer-extracted disc asset without further evidence**. The accepted disc tree contains no ordinary `map/` directory, while `sa_3.exe` imports `CreateFileA`, `ReadFile`, `WriteFile`, `SetFilePointer`, `SetEndOfFile` and `CreateDirectoryA`; this keeps runtime cache/download/generated-file hypotheses open.
- A first bounded xref probe finds a direct code reference to **`waei.bin`** and two direct references to **`data\\auto.dat`**. The plain `map\\%d.dat`, `ClientLogin`, `CharLogin`, `data\\mail.dat`, `data\\chatreg.dat` and `data\\album.dat` strings have no direct absolute code xref in that pass. This is a binary-analysis limitation, not evidence of non-use; pointer-table indirection is being probed separately.
- Canonical derived records: `research/recovered/STONEAGE-TW10-INSTALLSHIELD-R1.txt` and `research/recovered/STONEAGE-TW10-MAPCACHE-BINARY-R1.txt`.
- **Operational consequence:** do not spend further work trying to extract maps from the InstallShield support cabinet unless a new installer-specific record points to another cabinet/object. Prioritize the runtime file/network call chain and pointer indirection around `map\\%d.dat`, `waei.bin`, `ClientLogin` and `CharLogin`.

## Taiwan v1.0 exact runtime xref resolution — 2026-09-19

- The earlier broad proximity-callgraph result is now treated as **exploratory only**, because its ±0x800 address heuristic expanded several targets to the 320-node cap and therefore over-connected unrelated runtime subsystems. Do not use those broad GRAPH_API hits as direct proof of a target's semantics.
- A replacement exact-xref probe uses the raw little-endian VA references already proven by the deep runtime scan, recovers the actual containing x86 instruction, and follows only direct calls forward from that concrete point with bounded return/tail-jump termination.
- **`map\\%d.dat` has six real code references, all recovered exactly:** pointer RVAs `0x1d847`, `0x1da51`, `0x1dda1`, `0x21307`, `0x21722`, `0x218ff`; each is a five-byte `push` of the exact string address. All six call roots share internal targets `0x4856c`, `0x48748` and `0x487ba`; four additionally share `0x48e54`. Four of the six exact graphs reach **KERNEL32 `CreateDirectoryA` at graph depth 1**. Combined with the verified retail-disc absence of any `map/` directory or numeric map DAT files, this directly establishes that the Taiwan v1.0 runtime contains code that creates the map-cache directory at runtime. It does **not yet** by itself prove which network handler supplies the tile/parts/event bytes.
- **`ClientLogin` has two exact references:** a five-byte `push` at instruction RVA `0x19365` and a five-byte `mov` at `0x1a6d5`. **`CharLogin` likewise has a `push` at `0x19615` and a `mov` at `0x1a89b`.** The two push-side roots share the same four internal call targets `0x1b060`, `0x1b0f0`, `0x1b3f0`, `0x1b480`, while the mov-side roots diverge to `0x1a70b` and `0x1a8d1`. This is strong binary evidence for a common login-protocol construction pipeline plus per-message dispatch branches; exact helper names/roles remain OPEN until further signature matching.
- The exact five-level ClientLogin/CharLogin graphs do **not** reach imported Winsock calls. Given the independently confirmed WSOCK32 import set and later source lineage, this most likely means the protocol builder hands off through an indirect/static wrapper not captured by the current direct-call graph; it is not evidence that login is non-networked.
- **`waei.bin` has one exact five-byte `push` reference** at instruction RVA `0xd4f2`, followed by direct internal targets `0x9da0`, `0xb400`, `0x405c0`; the bounded exact graph still reaches no named file/network import. The retail disc contains no `waei.bin`, so its source and exact role remain OPEN.
- Canonical derived records: `research/recovered/STONEAGE-TW10-EXACT-XREF-R1.txt`, `research/recovered/STONEAGE-TW10-RUNTIME-DEEP-R1.txt`, and the earlier exploratory `research/recovered/STONEAGE-TW10-RECURSIVE-RELATIONS-R1.txt`.
- Descendant-source comparison remains a **lineage control**, not a substitute for the v1.0 binary: the later client source constructs `map\\%d.dat` as width/height plus three uint16 tile/parts/event layers and writes server `M` map rectangles into that persistent cache. The Taiwan v1.0 exact xrefs now independently confirm runtime map-directory creation, but the precise v1.0 network-handler-to-cache-write join is still being resolved.

## Taiwan v1.0 protocol-generator lineage — 2026-09-19

- Exact-xref expansion across the continuous login-character protocol sequence now resolves five v1.0 protocol utility helpers by **binary call count and call order**, not by symbol-name guessing:
  - `0x1b480 = lssproto_CreateHeader`
  - `0x1b060 = lssproto_strcatsafe`
  - `0x1b0f0 = lssproto_mkstr_string`
  - `0x1b0b0 = lssproto_mkstr_int`
  - `0x1b3f0 = lssproto_Send`
- Six consecutive protocol builders are reproduced in Taiwan v1.0: `ClientLogin`, `CreateNewChar`, `CharDelete`, `CharLogin`, `CharList`, `CharLogout`. Each has a push-side send-builder reference and a separate mov-side dispatch reference.
- The strongest signature is `CreateNewChar`: Taiwan v1.0 calls the integer converter **12 times**, the string converter once, the append helper **13 times**, with header first and send last. This exactly reproduces the later preserved generator's twelve integer fields plus one `charname` string. ClientLogin's 2 string conversions/appends, CharDelete/CharLogin's 1 each, and CharList/CharLogout's literal-empty append pattern also match exactly.
- This establishes direct protocol-generator lineage for these messages between the accepted v1.0 runtime and the later preserved source family. The later source remains a control corpus; the exact counts/order are independently observed in the v1.0 bytes.
- **The generated-protocol -> socket handoff is now closed directly from v1.0 bytes.** `0x1b3f0 = lssproto_Send` calls through `.data` slot `0x598e0`; init helper `0x1ac10` installs default target `0x1b3d0` and conditionally replaces it with its first argument; its sole caller at `0x2ebe3` passes callback `0x2eca0`.
- Callback `0x2eca0` reads and updates pending-length global `0x13ede20`. The runtime's unique WSOCK32 `send` business call is `0x2eb33`, which reads that same length, uses socket global `0x13ede24`, buffer address `0x13f1e34`, flags `0`, then calls linker thunk `0x48466` -> `send` IAT `0x52254`.
- This independently confirms the descendant source's buffered `write_func` architecture without using the descendant source as historical proof. Canonical derived evidence: `research/recovered/STONEAGE-TW10-PROTOCOL-HANDOFF-R1.txt`.
- **Operational consequence:** the network-handoff subtask is complete. The highest-priority unresolved protocol work is now the six mov-side receive/dispatch branches and their join to incoming `recv`; in parallel, resolve the six `map\\%d.dat` callsites into create/read/write/check roles and connect the map-write path to receive/dispatch.
- Canonical technical record: `research/clients/STONEAGE-TW10-LSSPROTO-GENERATOR-LINEAGE-R1.md`. Derived xref evidence: `research/recovered/STONEAGE-TW10-EXACT-XREF-R1.txt`.


## Taiwan v1.0 receive dispatcher and map-protocol join — 2026-09-19

- A dedicated derived-only binary probe now closes the **incoming Winsock receive -> LSSPROTO string dispatcher** chain in the accepted Taiwan v1.0 runtime. The unique WSOCK32 `recv` business call is at RVA `0x2ea8a`, through thunk `0x48472` to IAT RVA `0x5224c`.
- The same network path has exactly one direct call to dispatcher root RVA **`0x19730`** at callsite **`0x2eae3`**. Starting from the `recv` call, the direct-call graph reaches `0x19730` at depth 2.
- `0x19730` is independently fingerprinted as the string-protocol dispatcher: its opening direct calls are `0x1b010`, `0x1b300`, and `0x1afb0`, and its contiguous dispatch region contains exact protocol-name references including `EV`, `EN`, `RS`, and `RD`. This closes the earlier unresolved `recv -> protocol dispatcher` join without relying on descendant source addresses.
- The six login/character mov-side branches are now structurally resolved:
  - `ClientLogin` -> final receive callback `0x2f200`
  - `CreateNewChar` -> `0x31e90`
  - `CharDelete` -> `0x31f90`
  - `CharLogin` -> `0x2f530`
  - `CharList` -> `0x2f320`
  - `CharLogout` -> `0x2f610`
  Their shared string-decode/copy pair is `0x1b140 -> 0x1b4c0`. Binary control shape and independently matching descendant semantics identify these as the v1.0 equivalents of `lssproto_demkstr_string` and `lssproto_wrapStringAddr`. The integer decoder is `0x1b120`: the `MC` branch calls it exactly eight times and the `M` branch exactly five times, reproducing their observed integer field counts.
- The map protocol branches are now exact:
  - `MC` mov-side dispatch xref at `0x19e2e` -> eight integer decodes + one string decode/copy -> callback **`0x30d20`**.
  - `M` mov-side dispatch xref at `0x19f54` -> five integer decodes + one string decode/copy -> callback **`0x30ef0`**.
- The **server map-data -> local map-cache file join is now binary-proven.** `M` callback `0x30ef0` reaches function `0x1da40` at graph depth 3; that function contains exact `map\\%d.dat` xref `0x1da50` and references file modes `rb+`, `wb`, `rb+`, proving a writable/update map-file path. This independently reproduces the role later preserved as the map rectangle write path.
- `MC` callback `0x30d20` reaches function `0x1dd90` at graph depth 4; that function contains exact `map\\%d.dat` xref `0x1dda0` and references `rb`, `wb`, `rb`, proving a read/check/create-if-missing path. This independently matches the later checksum/read-control role, while the exact historical v1.0 symbolic function name remains unclaimed.
- Canonical derived evidence: `research/recovered/STONEAGE-TW10-RECEIVE-MAP-JOIN-R1.txt`. Canonical interpretation record: `research/clients/STONEAGE-TW10-RECEIVE-MAP-LINEAGE-R1.md`.
- **All six exact `map\\%d.dat` code paths are now fingerprinted by v1.0 file-mode behavior.** In ascending code order: `0x1d846 = rb,wb`; `0x1da50 = rb+,wb,rb+`; `0x1dda0 = rb,wb,rb`; `0x21306 = rb,wb,rb`; `0x21721 = rb`; `0x218fe = rb+`. The six-path count, code order, and mode signatures reproduce the later preserved sequence `createMap / writeMap / readMap / createAutoMap / readAutoMapSeeFlag / writeAutoMapSeeFlag`. Exact later symbol names remain lineage mappings rather than recovered v1.0 symbols, but the create/write/read/automap/read-flag/write-flag roles are now sufficiently constrained for reconstruction work.
- **Operational consequence:** the receive/dispatch/map-cache subtrack is complete at the current archaeology level. Highest priority moves to server-selection and endpoint provenance: identify exactly where v1.0 gets host/IP/port data and close the path through `inet_addr / gethostbyname / connect`.


## Taiwan v1.0 server selection and launcher endpoint provenance — 2026-09-19

- The accepted Taiwan v1.0 runtime has a single game-server endpoint connection path. The selected server index is read from global RVA `0x5c860`; getter RVA `0x2e950` copies the selected host and converts its port; the connection path then reaches `socket 0x2eeaa -> htons 0x2ef2e -> inet_addr 0x2ef3d`, falls back to `gethostbyname 0x2ef50` when needed, and calls `connect 0x2efa4`.
- The runtime server table is a 10-slot virtual `.data` structure at RVA `0x13f5e40`, with **193 bytes per slot = used byte + 128-byte host field + 64-byte port field**. It is not file-backed in the executable image and therefore is populated at runtime.
- Server-table writer RVA **`0x2e890`** receives the same text source used by the runtime's startup-option parser. It searches for literal **`IP:`**, decodes a single decimal slot index, copies host bytes into the slot's host field, copies the following port into the port field, and marks the slot used with ASCII **`'1'`**. The writer's only direct caller is at RVA `0x1c7e4`.
- The writer argument comes from global RVA **`0x139b758`**. The same global is independently consumed by exact startup tokens `realbin:`, `adrnbin:`, `sprbin:`, `spradrnbin:`, `windowmode`, `nodelay`, and `updated`, establishing one shared startup-command source rather than a separate hidden server table.
- The initialization function beginning at RVA **`0x1c4c0`** is WinMain-shaped binary code: before local stack allocation it reads the third and fourth incoming stack arguments, stores the third argument to `0x139b758` and the fourth to another startup global, then immediately performs GUI-process initialization through `CreateMutexA`, `GetLastError`, `MessageBoxA`, `LoadIconA`, and `LoadCursorA`; its early exits use `ret 0x10`, matching four incoming arguments. Thus the Taiwan v1.0 bytes directly establish that `0x139b758` is the process command-line parameter.
- The same retail disc's **`StoneAge.exe` has exactly one `CreateProcessA` business call**, at RVA `0x43c3`. Immediately before it, the launcher constructs a command line with a 17-string format and runtime buffers. Static fragments in the same construction region include `realbin:%d`, `adrnbin:%d`, `sprbin:%d`, `spradrnbin:%d`, `updated`, and executable patterns `sa_%d.exe` / `%ssa_%d.exe`. This directly joins the updater/launcher role to the runtime's startup-parameter family.
- **Limit:** literal `IP:` is not statically embedded in `StoneAge.exe`; the exact operator-era upstream source that supplies the dynamic endpoint fragment before the launch string is assembled remains unresolved. That upstream detail is now an operator/config provenance question, not a blocker for reconstructing the game: the runtime delivery channel and endpoint parser are already binary-proven.
- The separately observed `waei.bin` path does not join the server-table or Winsock endpoint graph in the bounded exact analysis, and the disc contains no `waei.bin`. It is therefore not used as the endpoint-source explanation for the proven v1.0 path.
- Canonical interpretation: `research/clients/STONEAGE-TW10-SERVER-SELECTION-LINEAGE-R1.md`. Derived binary evidence: `research/recovered/STONEAGE-TW10-SERVER-SELECTION-R1.txt`.
- **Operational consequence:** login/server-selection endpoint provenance is complete at the current archaeology level. Do not extend this branch into obsolete billing/operator infrastructure unless a future recovered artifact makes it necessary for historical comparison. Highest priority moves to deterministic client-data boundaries and inventories.

## Taiwan v1.0 deterministic client-data boundary — 2026-09-19

- A deterministic file-level inventory now covers the accepted Taiwan v1.0 retail client: **411 total disc files, 383 core StoneAge files, 373,564,663 core bytes**. The derived inventory records SHA-256 for every core file and separates 19 bundled non-core bonus-content files plus 9 files outside the core `StoneAge/` tree.
- Core deterministic categories are now bounded: REAL/ADRN graphics (2 files), SPR/SPRADRN animation (2), battle resources (220), palettes (16), BGM (11), SFX/container/index resources (118), runtime executables (2), explicit branding/UI-shell files (3), local-state seed (1) and installer/support files (8).
- **Ordinary field maps are not retail-disc assets in this specimen.** The inventory finds 0 ordinary field-map/cache files, while the already proven runtime path creates `map\\%d.dat` and joins incoming `M` / `MC` protocol data to writable/readable map-cache functions. Field maps therefore belong to the runtime-generated/downloaded side of the v1.0 boundary; battle maps remain separately disc-resident.
- The battle resource count is now reconciled exactly. `battletxt_1.txt` has **233 unique address-table records**, but they are not 233 maps: **218** resolve to `battle00.sab` through `battle217.sab`, and **15** resolve to `Palet_1.sap` through `Palet_15.sap`. Their sizes close `battle_1.bin` exactly: `218 × 804 + 15 × 708 = 185,892` bytes. `Palet_0.sap` is disc-resident but outside that address table.
- The sound address table has **114 unique records**, all present in `data/se/`; two additional loose WAVs, **`sak_91.wav` and `sak_92.wav`**, are not referenced by that table. Existing container diagnostics remain authoritative: 107 indexed `sound_1.bin` records match loose counterparts exactly and 7 are variants, so container and loose-audio provenance must remain separate.
- Filename-level scanning finds **0 obvious standalone master-table candidates** under the bounded terms pet/item/skill/magic/NPC/enemy/quest/shop. This is not promoted to “server-side only”: such data may still be executable/container-embedded or protocol-delivered. Character/pet/item/skill/NPC provenance therefore remains OPEN until protocol-visible fields are correlated against the preserved 2.5 bridge and descendant controls.
- Canonical interpretation: `research/clients/STONEAGE-TW10-CLIENT-DATA-BOUNDARY-R1.md`. Derived inventory: `research/recovered/STONEAGE-TW10-CLIENT-INVENTORY-R1.txt`.
- **Operational consequence:** the file-boundary/inventory task is complete enough to leave discovery mode. Highest priority is now reconstruction-ready semantic datasets: battle scene + palette crosswalk first, then stable REAL/ADRN and SPR/SPRADRN ID metadata, then audio, followed by protocol/server-master correlation.

## Taiwan v1.0 battle reconstruction dataset and format boundary — 2026-09-19

- The battle reconstruction index is now explicit in `research/recovered/STONEAGE-TW10-BATTLE-DATASET-R1.txt`: all **233** historical `battle_1.bin` address records retain original table order, offset, size, resolved disc path, resource class and SHA-256. This closes the earlier ambiguity between address-record count and map count.
- Direct v1.0 disc-byte probing establishes **218 / 218 SAB files = 804 bytes** with exact four-byte header `SAB ` and exactly **800 payload bytes = 400 16-bit units** per file. Across the corpus this is 87,200 units.
- The 233-record container consists of **218 SAB maps + 15 battle-indexed SAP palettes**; the palette records are interleaved in historical table order and must not be re-sorted for byte-exact container reconstruction. `Palet_0.sap` is a sixteenth disc-resident palette outside the address table.
- Direct v1.0 probing establishes **16 / 16 SAP files = 708 bytes**. The pinned descendant client source independently preserves a loader that reads 224 sequential B/G/R triplets (672 bytes) from these palette files, leaving a 36-byte suffix. v1.0 suffix semantics remain OPEN; six distinct suffix hashes occur, so it must not be discarded as a universal constant.
- The pinned descendant client source also preserves a SAB reader that consumes four header bytes, reads each subsequent pair as big-endian `(c1 << 8) | c2`, and retains an older 20×20 drawing branch. Because `4 + 20×20×2 = 804`, **20×20 big-endian graphic IDs are the current lineage-supported reconstruction interpretation**, not yet promoted to direct original-`sa_3.exe` runtime FACT.
- A simple ADRN-range test cannot decide byte order: both BE and LE interpretations happen to resolve all 87,200 units into the very broad v1.0 bitmap-number set. This failed discriminator is retained explicitly to prevent false certainty.
- Canonical interpretation: `research/clients/STONEAGE-TW10-BATTLE-RESOURCE-FORMAT-R1.md`.
- **Operational consequence:** the battle-scene dataset/file-format boundary is complete enough to leave the critical path. Highest priority is now the full REAL/ADRN + SPR/SPRADRN reconstruction metadata export; audio follows after that.

## Taiwan v1.0 graphics/animation reconstruction metadata — 2026-09-19

- A dedicated deterministic exporter now reconstructs the full v1.0 REAL/ADRN + SPR/SPRADRN identity layer from the hash-verified retail disc and emits **derived metadata only** under `research/recovered/tw10-resource-metadata/`.
- The export was independently executed by GitHub Actions run **35451600908**, which completed successfully through unit tests, preservation-archive hash verification, metadata generation, gzip integrity checks, deletion of transient proprietary bytes and derived-data commit.
- `ADRN-R1.tsv.gz` contains all **125,996** unique v1.0 bitmap records. Their spans have **125,995 contiguous transitions** and cover the full **315,842,228-byte REAL** payload with no missing tail. Per-record metadata includes bitmap number, REAL offset/size, x/y offsets, dimensions, RD flag/size metadata and hashes rather than payload bytes.
- RD flags are fully classified at this layer: **125,988 flag-1 records** and **8 flag-0 records**; two records retain special/implausible dimensions for later semantic interpretation rather than being normalized away.
- `SPR-GROUP-R1.tsv.gz`, `SPR-ANIMATION-R1.tsv.gz` and `SPR-FRAME-R1.tsv.gz` preserve the complete animation hierarchy: **464 groups, 39,065 animations and 242,085 frames**. All 464 group spans close exactly at the next recorded offset; **3,492 frames** retain the historical `0xffffffff` bitmap sentinel.
- Source hashes in the manifest match the accepted Taiwan v1.0 anchors already established for `adrn_1.bin`, `real_1.bin`, `spradrn_1.bin` and `spr_1.bin`. Generated dataset hashes are fixed in `research/recovered/tw10-resource-metadata/MANIFEST-R1.txt`.
- **Operational consequence:** graphics/animation ID recovery is no longer the critical-path discovery task. Highest priority moves to the deterministic audio reconstruction crosswalk.

## Taiwan v1.0 audio reconstruction crosswalk — 2026-09-20

- The deterministic audio crosswalk is now generated and verified in `research/recovered/STONEAGE-TW10-AUDIO-DATASET-R1.txt`, with interpretation fixed in `research/clients/STONEAGE-TW10-AUDIO-PROVENANCE-R1.md`.
- GitHub Actions run **35451761733** completed successfully through unit tests, preservation-archive hash verification, audio metadata export, strict historical-count assertions, deletion of transient proprietary bytes and derived-data commit.
- The accepted retail disc contains **114 indexed `sound_1.bin` records, 116 loose SFX WAVs and 11 BGM WAVs**. The indexed/loose relationship is now partitioned as **107 byte-identical full files, 1 wrapper-only variant with identical PCM payload, 6 genuine PCM-different variants, 0 missing loose counterparts and 2 unindexed loose SFX files**.
- The sole wrapper-only variant is indexed record 45, `sak_09a.wav`: container and loose files have different RIFF metadata/order but the same 30,080-byte PCM payload and PCM SHA-256.
- The six genuine payload variants are indexed `sak_01.wav`, `sak_02.wav`, `sak_04.wav`, `sak_05.wav`, `sak_10.wav` and `sak_11.wav`; these must remain separate historical resources rather than being normalized.
- The two unindexed loose files have exact alias relationships: **`sak_91.wav` is byte-identical to indexed record 37 named `sak_01.wav`**, and **`sak_92.wav` is byte-identical to indexed record 38 named `sak_02.wav`**. The byte identity is FACT; the historical naming/editorial reason remains OPEN.
- The 11 BGM WAVs are outside `soundaddr_1.txt` / `sound_1.bin` and remain a separate historical namespace.
- **Operational consequence:** the deterministic client-side resource recovery path (battle, graphics/animation and audio) is sufficiently complete to move the critical path to protocol-visible gameplay/master-data correlation. Do not re-open audio archaeology unless new provenance or an implementation question requires it.

## Taiwan v1.0 gameplay protocol / master-data matrix — 2026-09-20

- A new original-client protocol inventory now derives the accepted Taiwan v1.0 generated-protocol surface directly from `sa_3.exe`: **20 unique C→S builder names** in RVA `0x18c00..0x19730` and **33 unique S→C dispatch names** in `0x19730..0x1aa8a`. Canonical derived report: `research/recovered/STONEAGE-TW10-GAMEPLAY-PROTOCOL-R1.txt`.
- GitHub Actions run **35505024289** completed successfully against the hash-verified retail disc after the workflow was corrected to preserve control drift rather than forcing every descendant-control message to exist in the compiled v1 client.
- Exact v1 field-type shapes independently match the early generated lineage for key gameplay messages including `C`, `CA`, `CD`, `S`, `I`, `SI`, `KS`, `PS`, `SKUP`, `WN`, `PME`, `M`, `MC`, `RS`, `RD`, `B`, `D` and `CreateNewChar`.
- Especially strong direct anchors are: C→S `PS = 3 ints + 1 string`; S→C `PS = 4 ints`; C→S `WN = 5 ints + 1 string`; S→C `WN = 4 ints + 1 string`; S→C `PME = 7 ints + 1 string`; C→S `CreateNewChar = 12 ints + 1 string`.
- The bounded v1 send-builder region does not expose separate lineage-control builders `S` or `MI`, and the bounded receive region does not expose `EF` or `SE`. This is recorded only as **not observed in this compiled v1 surface**; it is not promoted to proof that the logical operations never existed.
- `research/clients/STONEAGE-TW10-GAMEPLAY-DATA-MATRIX-R1.md` now correlates the direct v1 protocol surfaces with the early generated 2000 lineage and the preserved 2.5 server/master-data bridge. It explicitly labels evidence as **V1 DIRECT / EARLY LINEAGE / 2.5 BRIDGE / VERSIONED-OPEN**.
- The matrix defines the first reconstruction-safe gameplay schemas for `CharacterState`, `WorldObject`, `PetState`, `PetSkillView`, `ItemView/ItemInstance` and `NPCWindowSession`, while quarantining later 2.5-only fields from the v1 baseline.
- **Operational consequence:** broad protocol-name inventory and first-pass server-table correlation are complete enough to leave the critical path. Highest priority is now v1 callback-internal parsing for `S`, `C`, `I` and `WN`, so selected inner string fields can be promoted from EARLY LINEAGE to V1 DIRECT.

## Taiwan v1.0 field-level gameplay schema — 2026-09-20

- The callback-internal parsing pass is now complete enough to define a reconstruction baseline directly from the accepted Taiwan v1.0 client.
- The original `S` status dispatcher is binary-decoded as exactly ten implemented categories: **C, D, E, I, J, K, M, N, P, W**. `F,G,H,L,O,Q,R,S,T,U,V` share the default branch in this compiled client.
- Shared original-client token helpers are structurally fingerprinted: string-token extraction `0x46c70`, decimal-token conversion role `0x46da0`, base-62 token conversion role `0x46e70`, and escape-decoding role `0x46ff0`.
- Direct v1 full player state `S:P` ends at token **26**: base-62 update mask, decimal tokens 2..24, escaped strings 25..26. Later transmigration/ride/base-graphic extensions are outside this compiled layout.
- Direct v1 full pet state `S:K` ends at token **21**: base-62 update mask, decimal tokens 2..19, escaped strings 20..21. Later pet transmigration/fusion/ride/bless extensions are outside this compiled layout.
- The v1 `C` callback is now bounded directly into three legacy world-record variants:
  - character/object record = **12 fields**;
  - ground-item record = **6 fields**;
  - ground-money record = **4 fields**.
  The later character-field `POPUPNAMECOLOR` at token 13 is not read by this v1 character path.
- The v1 inventory/pet-skill layouts are now binary-direct:
  - full inventory `S:I` = **20 slots × 9 fields**;
  - incremental `I` = **10 fields per record** including explicit slot index;
  - pet-skill view `S:W` = **7 skill slots × 5 fields**.
  Neither v1 item layout contains the later durability/damage field.
- The v1 `WN` callback is proven as a five-value forwarding boundary into target RVA `0x12930`, preserving the server-driven window/session architecture.
- Canonical derived binary evidence: `research/recovered/STONEAGE-TW10-GAMEPLAY-CALLBACKS-R1.txt`. Canonical interpretation: `research/clients/STONEAGE-TW10-GAMEPLAY-DATA-MATRIX-R1.md`.
- A canonical machine-readable baseline now exists at `research/clients/STONEAGE-TW10-GAMEPLAY-SCHEMA-R1.json`. It separates **V1_DIRECT position/type/count evidence** from **EARLY_LINEAGE semantic names**, preserves explicit 2.5 bridge policy and lists direct version exclusions.
- Schema validation is enforced by `tests/test_stoneage_tw10_gameplay_schema.py` and `.github/workflows/validate-stoneage-tw10-gameplay-schema.yml`; GitHub Actions run **35506265458** completed successfully.
- **Operational consequence:** broad client protocol and first-pass field-layout archaeology are no longer the critical path. The project can now start constructing reconstruction-side gameplay models and explicit v1-runtime ↔ server-master bridge mappings without importing later 2.5-only fields into the historical baseline.

## Reconstruction gameplay bridge/model baseline — 2026-09-20

- The Taiwan v1.0 client field schema is now consumed by executable reconstruction code rather than remaining documentation-only.
- `research/clients/STONEAGE-TW10-25-GAMEPLAY-BRIDGE-R1.json` is the canonical explicit bridge from the v1 client/runtime schema to the recovered 2.5 server/master-data specimen. It preserves four hard identity separations: runtime object ID != template ID, inventory slot != item template ID, pet slot != enemybase TEMPNO, and 2.5 fields must not be backfilled into the v1 wire baseline.
- `tools/stoneage_tw10_gameplay_model.py` provides schema-driven `CharacterState`, `PetState`, `ItemView`, `PetSkillView`, `WorldObject` and `NPCWindowSession` records. Widths, names and wire conversions are loaded from `STONEAGE-TW10-GAMEPLAY-SCHEMA-R1.json`, including the historical base-62 alphabet and escape decoder.
- `tools/stoneage_tw10_25_bridge_model.py` provides explicit template bridge objects for enemybase, petskill, itemset and NPC template/create identities. Template references remain separate objects and never overwrite v1 runtime/slot identities.
- Pet-template bridging is now split into:
  - direct copied/runtime-visible fields such as graphic ID, MODAI, elements, skill-slot count and pet-skill IDs;
  - growth/formula inputs such as INITNUM, LVUPPOINT and BASEVITAL/STR/TGH/DEX.
- The convergent descendant pet birth path is executable as a **BRIDGE_2_5 formula layer**:
  - fixed descendant enemybase loader uses `atoi`, so textual `LVUPPOINT=5.00` is stored as integer 5;
  - PETRANK is calculated from the unmodified template four-stat sum;
  - each growth component receives an explicit -2..+2 birth offset and is packed into `CHAR_ALLOCPOINT`;
  - a distinct ten-roll allocation adds exactly ten spawn-stat points;
  - current internal four stats use `(((level-1)*LVUPPOINT)+INITNUM) * current_base`;
  - derived combat projection remains separate from the historical v1 wire evidence.
- NPC runtime derivation is now closed to the first reconstruction-safe boundary:
  - NPCCREATE spawn area supplies runtime floor/X/Y and DIR;
  - NPCTEMPLATE supplies image/name with NPCCREATE override support;
  - CHAR instance creation is followed by OBJECT allocation, and that newly allocated object index becomes `CHAR_WORKOBJINDEX`;
  - v1 `C.runtime_object_id` and `WN.source_object_index` therefore refer to the same runtime object identity;
  - `WN.sequence_number` remains an independent window/session state ID;
  - level/title/walkable/height and comparable presentation fields remain explicit default/runtime CHAR inputs rather than being falsely attributed to static NPC template rows.
  This boundary is implemented in `build_npc_runtime_bridge()` and validated in the combined model suite.
- `tools/stoneage_tw10_25_encounter_bridge.py` now models the strict server identity chain:
  `encount.INDEX -> group.GROUP_ID -> enemy.ID -> enemybase.TEMPNO -> runtime state`.
  It accepts the exact field names emitted by the recovered probes as well as the normalized documentation names.
- Group and enemy weighting remain separate stages; z-order overlap, item gates, concrete enemy level ranges and `CREATEMAXNUM` bounding are modeled explicitly. Unresolved positive references raise hard errors rather than reproducing the old C code's possible negative-array indexing.
- The recovered active 2.5 specimen's **39 positively weighted unresolved group references across 32 encount rows** are encoded as `SPECIMEN_DEFECT`, not gameplay behavior; reconstruction code must not synthesize missing groups.
- Validation is layered and green:
  - gameplay baseline/schema tests;
  - v1↔2.5 bridge-schema tests;
  - schema-driven runtime model tests;
  - executable template/pet-birth bridge tests;
  - strict encounter-chain tests.
  Latest relevant successful runs: **35507294753** (bridge schema) and **35507294756** (combined model suite).
- **Operational consequence:** the first reconstruction-safe gameplay domain layer now exists. The critical path moves from broad data archaeology to closing the few remaining runtime derivation seams needed for an actual single-player engine prototype.

- ItemTemplate -> ItemInstance -> v1 ItemView is now closed to the first reconstruction-safe boundary:
  - canonical item field 2 is `secondary_display_text`, not a second secret-name field;
  - fixed descendant senders source field 1 from instance `ITEM_SECRETNAME` and field 2 from runtime `paramshow/name2` (empty on the active base path);
  - `ItemInstanceBridge` derives v1 color and base send/use flags from instance/template state instead of treating them as raw itemset columns;
  - base color derivation is white=0, bound/nonempty CDKEY -> green=5, otherwise merge flag -> yellow=4;
  - base sendFlag bits are CANPETMAIL=bit0, CANMERGEFROM=bit1, DISH=bit2; later inlay/damage bits remain quarantined;
  - schema/bridge/model suites are green at runs **35507746385**, **35507746366**, **35507746369**.
- Enemy variant + pet template + birth formula -> v1 PetState is now composed:
  - `build_reconstructed_pet_state()` validates `enemy.TEMPNO == enemybase.TEMPNO`;
  - concrete `enemy.ID`, template `enemybase.TEMPNO`, owner pet slot and optional world runtime object ID remain four distinct namespaces;
  - bridge-derived v1 fields are combined with explicit unresolved runtime inputs for MP/EXP/rename/free-name rather than inventing later formulas;
  - the output field set/order is checked against the canonical 21-field v1 `S:K` schema;
  - latest combined model validation **35507842293** and bridge validation **35507842310** both pass.
## Engine-facing single-player historical domain boundary — 2026-09-20

- `tools/stoneage_singleplayer_domain.py` now defines the first engine-facing, in-process historical domain boundary. It intentionally has no socket, packet, account-server or network-server dependency; recovered v1 wire/protocol structures enter only through explicit evidence adapters.
- Historical identity namespaces are now typed separately at the domain edge: runtime object ID, inventory slot, item template ID, pet slot, enemy variant ID, enemybase pet template ID and NPC template ID cannot be silently substituted for one another.
- Deterministic adapters now cover the previously recovered bridge seams:
  - v1 `CharacterState` -> engine-facing player snapshot;
  - `ItemInstanceBridge` -> inventory item;
  - composed enemy/template/birth `ReconstructedPetBridgeState` + petskill templates -> pet actor + skill views;
  - `NpcRuntimeState` -> world NPC and in-process NPC window/session state;
  - encounter area/group/enemy bridge tables + current position/inventory -> deterministic `EncounterRequest`.
- Runtime state is explicitly partitioned into `HistoricalStaticData`, `PersistentPlayerState`, `TransientWorldState` and `InteractionState`. This prevents future engine selection from inheriting the old network-server process architecture.
- `SinglePlayerSimulation.step()` provides the minimal deterministic simulation shell. It advances only a local tick index and snapshots state; optional `EncounterRolls` are supplied explicitly by the caller so no new RNG, movement, timing, collision or battle mechanics are invented.
- Remote validation is green:
  - **35508501840** validates the initial in-process historical domain boundary;
  - **35508543992** validates the deterministic simulation-tick implementation;
  - **35508555419** validates the final domain + tick test suite.
- **Operational consequence:** the former immediate actions 1–3 (engine-facing domain boundary, deterministic bridge adapters, and minimal single-player state/tick shell) are complete to the first reconstruction-safe boundary. The critical path can now move from architecture scaffolding to a playable deterministic chain using already recovered map/warp and battle models.

## First end-to-end in-process historical simulation slice — 2026-09-20

- `tools/stoneage_singleplayer_world.py` connects recovered map dimensions and classic overlap-Warp semantics to the single-player world domain.
  - map floor/width/height bounds are explicit;
  - ordinary walk attempts cannot silently change floor;
  - collision/object-overability remains an explicit `entry_allowed` input until exact MAP/DAT collision semantics are independently closed;
  - classic Warp executes only after the player has entered the overlap cell;
  - ordinary Warp steps suppress same-step random encounter dispatch;
  - the documented legacy non-transactional `MAP_objmove` failure boundary is preserved as evidence rather than silently rewritten.
- `tools/stoneage_singleplayer_battle.py` connects `EncounterRequest` to a minimal battle lifecycle:
  - player, explicitly selected allied pets and explicit enemy spawns become typed battle participants;
  - enemy variant/template/level identities are validated against the encounter request;
  - descendant battle-core initiative and physical-damage formulas are callable only with explicit randomness and an explicit defense-profile choice;
  - unresolved enemy count, birth rolls, commands, AI, drops and result semantics remain explicit inputs;
  - battle outcomes may update only existing persistent state fields and return to the unchanged world position.
- `tools/stoneage_singleplayer_runtime.py` composes the first end-to-end deterministic runtime slice:
  `world walk -> Warp -> encounter -> battle -> outcome -> world`.
  Blocked walks do not generate encounters, and Warp steps preserve the recovered encounter-suppression ordering.
- Remote validation is green:
  - **35508914734** validates the single-player map/Warp integration together with the recovered Warp model;
  - **35509025827** validates encounter-to-battle lifecycle integration together with the descendant battle-core model;
  - **35509083296** validates the full end-to-end historical runtime slice.
- **Operational consequence:** the previous immediate actions 1–3 are now closed to the first reconstruction-safe executable boundary. We have moved beyond architecture scaffolding into an actual in-process single-player historical game loop skeleton without requiring a network server.

## Standalone single-player persistence boundary — 2026-09-20

- `tools/stoneage_singleplayer_persistence.py` now defines versioned local save schema `stoneage.singleplayer.persistence.r1`.
- This is explicitly a **DESIGN** persistence format, not a recovered historical account/save format.
- Only player-owned persistent state is serialized:
  - player field snapshot;
  - inventory slot + item-template identity + current reconstructed item view;
  - pet slot + enemy-variant identity + enemybase-template identity + current pet state + skill views.
- Static master data, transient world objects, NPC/window sessions, active battle state and all network/account-server concepts are excluded from the payload.
- Pet/runtime world object identity is deliberately not persisted; restored pets return with `runtime_object_id=None` so a future world load allocates fresh transient identity instead of aliasing an old runtime object.
- Payload shape and schema are strict, duplicate inventory/pet slots are rejected, and deterministic JSON encoding is covered by regression tests.
- Remote validation **35509162758** passes with the persistence tests integrated into the combined single-player/gameplay model suite.
- **Operational consequence:** the former immediate persistence action is complete to the first versioned local boundary. The single-player runtime now has a clean save/load direction without reconstructing historical login/account-server architecture.

## Map collision / object-overability algorithm seam — 2026-09-20

- `research/mechanics/STONEAGE-MAP-COLLISION-OVERABILITY-R1.md` records the recovered stable-descendant collision chain.
- `tools/stoneage_map_collision_model.py` now models the evidence-backed algorithm:
  - a map cell supplies tile image id + object/parts image id;
  - per-image `WALKABLE` / `HAVEHEIGHT` metadata determines static entry;
  - object WALKABLE modes 0/1/2 mean block / defer-to-tile / force-walkable;
  - flying uses tile+object HAVEHEIGHT rather than ordinary WALKABLE;
  - diagonal movement requires both orthogonal side cells to pass static walkability;
  - target-cell non-overable characters/items are a separate dynamic blocking layer.
- Unknown image metadata raises instead of receiving a guessed/default walkability value.
- `SinglePlayerHistoricalRuntime.walk_step_with_collision()` can consume a validated collision map/profile and calculate the movement verdict itself.
- This older 2026-09-20 collision-algorithm milestone was subsequently superseded on the data side by direct Taiwan-v1 retail-disc ADRN recovery. `research/mechanics/STONEAGE-TW10-ADRN-COLLISION-R1.md` and `research/recovered/tw10-resource-metadata/COLLISION-ATTR-R1.tsv.gz` now provide the provenance-safe Taiwan-v1 map-number collision-property dataset and the v1 `readHitMap` interpretation.
- The remaining collision-content gap is **not** the image-property table. It is the provenance-complete Taiwan-v1/JSS field-map tile/parts/event plane corpus itself: the accepted Taiwan-v1 retail disc contains zero ordinary field-map DAT files, while the recovered mixed 2.5 DAT corpus remains a later bridge/specimen and must not be promoted into the early baseline.
- Remote validation **35509951036** passes with collision-model and runtime-integration regression coverage; later ADRN/hit-map validations are recorded in the dedicated Taiwan-v1 collision milestone.
- **Operational consequence:** movement no longer requires inventing either the collision algorithm or Taiwan-v1 image collision attributes. A provenance-safe field-map plane source is the only missing data layer before the early-client collision path can be populated end to end.

## Movement-side encounter frequency / CEP loop — 2026-09-20

- `research/mechanics/STONEAGE-ENCOUNTER-FREQUENCY-CEP-R1.md` records the stable-descendant movement-side encounter-frequency loop and explicitly keeps its earliest-commercial provenance OPEN.
- `tools/stoneage_encounter_frequency_model.py` models runtime CEP independently from encounter-content selection:
  - current CEP is clamped to the active min/max bounds;
  - the base random domain is `0..119` from `rand()%120`;
  - misses increment CEP by one up to max;
  - an actual encounter resets CEP to min;
  - an ordinary Warp-suppressed random hit neither resets nor enters the miss-increment branch;
  - missing zone lookup preserves prior bounds, matching the inspected replace-only-on-success behavior.
- `SinglePlayerHistoricalRuntime` now owns `EncounterFrequencyState` directly instead of recreating a network connection object.
- New runtime paths preserve the fixed-source ordering: refresh encounter bounds from the departure coordinate after a successful walk, resolve CEP with explicit randomness, then request encounter content at the current world position only when the CEP decision actually dispatches an encounter.
- The older direct encounter-selection path remains available as a deterministic bridge/test entry point and is not silently reinterpreted as CEP behavior.
- Remote validation **35510186803** passes with CEP unit tests and runtime soft-pity/Warp-suppression regression coverage.
- **Operational consequence:** encounter frequency and encounter content selection are now separate deterministic subsystems. The remaining combat-side critical path is enemy-count/birth orchestration and the first battle-round command boundary.

## Group-level enemy spawn + first battle command boundary — 2026-09-20

- Stable descendant `ENEMY_getEnemy()` evidence corrected the earlier single-variant encounter simplification:
  - encounter area selects a group first;
  - total enemy target count is drawn from `1..min(ENEMY_MAX_NUM, sum(slot CREATEMAXNUM))`;
  - each enemy position independently reselects a weighted group slot;
  - duplicate enemy-ID slots multiply that variant's effective create cap;
  - the selection loop retains the 100-attempt guard;
  - `CREATEMINNUM` is retained as source data but is not enforced because the inspected stable generation path does not read it.
- Recovered `enemybase.SIZE` (0 normal / 1 big) is now retained in `PetTemplateBridge.size_class`.
  - at most five big enemies are placed;
  - a sixth big selection reduces the target count;
  - a big enemy selected after position 4 swaps into the first five with an earlier normal enemy when possible.
- `tools/stoneage_enemy_spawn_model.py` materializes every selected enemy with independent level, four birth offsets and ten allocation rolls before producing battle participants.
- A new group-level encounter request is exposed alongside the older single-variant compatibility projection. Mixed-variant enemy groups can now enter one `BattleSession`.
- `tools/stoneage_battle_command_model.py` defines the first ordinary player round-command boundary for `H|target` attack, `G` guard, `N` wait, `E` escape and `T|target` capture.
  - target positions use the stable 20-slot domain;
  - invalid attack/capture targets preserve the source's `-1` sentinel;
  - error-status fallback maps checked commands to `N`;
  - initiative uses the recovered explicit-randomness profile.
- Later profession/pet-skill/item/magic/AI/effect/victory logic remains outside this boundary.
- `research/mechanics/STONEAGE-ENEMY-SPAWN-BATTLE-COMMAND-R1.md` records the evidence and exclusions.
- Remote combined validation **35510677772** passes with spawn, mixed-battle, command and runtime coverage.
- **Operational consequence:** immediate action 1 is closed to the first reconstruction-safe group/birth/command boundary. The runtime no longer assumes one enemy variant per random encounter.

## Taiwan v1 native image collision dataset — 2026-09-20

- The accepted Taiwan Waei/JSS v1.0 retail client's 80-byte ADRN records are now parsed as the independently established 28-byte image/index header plus the stable-descendant 52-byte `MAP_ATTR` tail.
- Deterministic resource export now produces `research/recovered/tw10-resource-metadata/COLLISION-ATTR-R1.tsv.gz` directly from verified `StoneAge/data/adrn_1.bin`; no descendant `mapset.txt` values are substituted.
- Verified source: `adrn_1.bin` = **10,079,680 bytes**, SHA-256 `47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8`, **125,996** records.
- Recovered nonzero map-number collision mappings: **9,286**, with **3** duplicate source-order assignments. The exporter mirrors client initialization by retaining the last assignment.
- Native ADRN hit-flag distribution across all records: `0=122,639`, `1=3,295`, `2=62`. Priority-type distribution: `0=125,803`, `2=88`, `3=105`.
- `tools/stoneage_tw10_hit_map_model.py` now mirrors the v1-compatible client `readHitMap()` ordering and preserves:
  - `hit == 0` blocking;
  - `hit == 1` normally passable;
  - `hit == 2` as the distinct local override marker;
  - `atari_x/atari_y` parts collision footprints;
  - the active `15680..15732` origin-only special case;
  - reserved small map codes, the 60..79 ADRN exception and final NPC-event blocking.
- `height_flag` is recovered as source metadata but is **not** silently promoted into movement semantics because the recovered client `readHitMap()` path does not consume it.
- Retail-disc inventory still reports `field_map_disc_files=0`: the collision-property dataset is now closed, while the provenance-complete field-map plane corpus remains a separate runtime/cache recovery question.
- The provenance-gated cache-plane software bridge is now closed without fabricating field content: `StoneAgeDatMapCache` strictly parses the descendant-source-corroborated 8-byte width/height + uint16 tile/parts/event DAT layout; `load_taiwan_v10_collision_profile()` verifies and loads the committed derived Taiwan-v1 collision TSV; and the cache/DAT composition helpers feed those planes directly into the recovered v1 hit-map algorithm. The parser performs no provenance inference, so mixed 2.5 DAT payloads remain later bridge specimens rather than Taiwan-v1 evidence.
- The single-player runtime now keeps the early-client collision path explicitly separate from the descendant-server collision model: `walk_step_with_taiwan_v10_hit_map()` and its CEP-frequency variant bind a recovered Taiwan-v1 hit map to the active floor and consume only the v1 `checkHitMap` verdict. They do not silently add descendant `WALKABLE/HAVEHEIGHT`, diagonal-corner or dynamic-overability rules.
- Evidence and boundary are recorded in `research/mechanics/STONEAGE-TW10-ADRN-COLLISION-R1.md`.
- Remote validation:
  - gameplay/model run **35511074585** — success;
  - repaired real-disc export **35511391125** — success;
  - export with explicit collision-dataset integrity requirement **35511442265** — success;
  - provenance-gated cache-plane adapter commit `1d1f5a69574c855ad06f211ebaf0241b51249764`, gameplay/model run **35726829348** — success;
  - Taiwan-v1 runtime collision-path separation commit `e1d684fb299a011126525e0989094e48de783079`, gameplay/model run **35727710528** — success.
- **Operational consequence:** the implementation path from authenticated field-cache bytes through Taiwan-v1 ADRN metadata to the v1 hit map and then into the single-player movement runtime is closed without merging later server semantics. The only remaining early collision-content gap is recovery/authentication of a provenance-safe Taiwan-v1/JSS field-map plane corpus itself; later 2.5/SACH data must not be substituted.

## Ordinary attack / guard / wait round resolution — 2026-09-20

- The stable descendant battle loop is now executable through the first status-free ordinary effect seam:
  - explicit COM1/COM2/COM3 command envelope;
  - recovered ordinary action-value generation;
  - descending action order;
  - explicit caller tie order when equal values hit the source's undefined C-`qsort` tie case;
  - execution-time dead/invalid-target check and random opponent retarget;
  - guard stance active from submitted commands before the guard actor's own sorted turn;
  - dodge, critical, physical damage, four-element adjustment, guard reduction and direct HP subtraction.
- Stable random comparison details are preserved:
  - dodge: `RAND(1,10000) <= per`;
  - critical: `RAND(1,10000) < per`.
- Stable four-attribute coefficients are now executable: same **1.0**, advantage **1.5**, disadvantage **0.6**, with neutral remainder and explicit battlefield element scalar.
- The earliest defense branch remains provenance-sensitive, so round execution still requires explicit `newpower_70pct` vs `preserved_old_mixed` profile selection.
- `BattleCombatProfile` keeps fixed DEX/LUCK/elements/weapon-critical explicit instead of silently equating early client display labels with server WORK fields.
- `tools/stoneage_singleplayer_runtime.py` now exposes `resolve_ordinary_battle_round()`, allowing a spawned group battle to run one deterministic attack/guard/wait round entirely in-process.
- Deliberately excluded: AI selection, counter/combo/guardian, bows/boomerangs, ride-pet sharing, reactions/statuses, skills/items/magic, capture/escape, battle termination and reward settlement.
- Evidence: `research/mechanics/STONEAGE-ORDINARY-BATTLE-ROUND-R1.md`.
- Remote validation:
  - battle-core run **35512116840** — success;
  - full gameplay/runtime run **35512186213** — success.
- **Operational consequence:** former immediate battle action is closed to the first deterministic effect boundary; the next battle problem is persistent multi-round state/termination, not first-hit arithmetic.

## Persistent multi-round battle state and first termination boundary — 2026-09-20

- `tools/stoneage_battle_state_model.py` now promotes a `BattleSession` into immutable multi-round battle state with:
  - current HP by participant;
  - completed turn count;
  - active/finished phase;
  - victory/defeat result and winning side;
  - previous submitted command set;
  - persistent participant-slot identity.
- Successive ordinary rounds now consume only currently living actors, while dead participant identity remains retained in battle state for target invalidation/history.
- Stable descendant `BATTLE_OnlyRescue()` termination semantics are preserved:
  - pets are explicitly skipped when determining whether a side still has a survival-bearing actor;
  - therefore an allied pet **does not** keep the player side alive after the player dies;
  - side 0 is checked first, then side 1, so the source's asymmetric both-zero edge ordering is preserved instead of inventing a draw.
- Rescue/join-battle mode remains outside this R1 boundary rather than being guessed.
- `tools/stoneage_singleplayer_runtime.py` now exposes `start_persistent_battle_state()` and `resolve_persistent_battle_round()`; real spawned group battles can carry HP from round to round until terminal state.
- Reward/post-battle settlement remains separate: no EXP, drops, money, death penalties, healing, capture/escape or post-battle warp is inferred from termination.
- Evidence: `research/mechanics/STONEAGE-BATTLE-STATE-TERMINATION-R1.md`.
- Remote validation:
  - battle-core run **35512820440** — success;
  - gameplay state run **35512816199** — success;
  - runtime multi-round integration run **35512877215** — success.
- **Operational consequence:** former immediate action 1 is closed to the first persistent victory/defeat boundary. The next highest-priority unresolved implementation seam is the combat-profile bridge for fixed DEX/LUCK and elemental work values.

## Combat-profile provenance bridge — 2026-09-20

- `tools/stoneage_combat_profile_bridge.py` now provides an evidence-bounded bridge from provenance-bearing reconstructed state into `BattleCombatProfile`.
- Stable-descendant status/work-stat evidence closes the following numeric mappings without treating similarly named client fields as interchangeable:
  - player v1 status `dexterity` -> fixed DEX numeric projection;
  - player v1 status `luck` -> fixed LUCK;
  - player v1 status earth/water/fire/wind -> fixed elemental work values;
  - pet/enemy reconstructed birth internal DEX -> fixed DEX;
  - reconstructed birth raw attributes -> fixed elemental projection using the preserved opposite-element overwrite order and nonnegative battle clamp.
- A generic persisted pet `quick` field is deliberately **not** accepted as fixed DEX provenance. Allied pets require their preserved reconstructed birth source; enemy profiles require their concrete `SpawnedEnemy` source.
- `SinglePlayerHistoricalRuntime.build_group_battle_combat_profiles()` now derives the complete profile map from player state plus provenance-bearing allied-pet/enemy sources.
- A regression at `124f382826fff48842afa6526478c9741565a8a0` exposed an incorrect test assumption that a later-mutated participant `quick` should overwrite the birth-derived fixed DEX. The test was corrected without weakening provenance semantics.
- Remote validation **35513757842** passes at `0fa2fc22133dddf41686053079a53adf5d75df31`.
- Evidence boundary: these mappings are stable-descendant/reconstruction bridges; byte-level proof of every corresponding JSS-1999 server work field remains OPEN.

## Terminal battle HP settlement boundary — 2026-09-20

- `SinglePlayerHistoricalRuntime.finish_persistent_battle()` now projects a **finished** `PersistentBattleState` back into the single-player persistent domain.
- The R1 settlement boundary writes only state already produced by the validated battle state machine:
  - battle result (`victory` / `defeat`);
  - terminal player HP;
  - terminal HP for allied pets that actually participated.
- The existing `apply_battle_outcome()` guard remains authoritative:
  - world position must still equal the battle origin;
  - only existing persistent fields may be updated;
  - no new reward/state key can be invented during settlement.
- Active/nonterminal battle state is rejected.
- Regression coverage proves player and pet EXP remain unchanged while HP is settled.
- Explicitly still excluded: EXP award/level-up orchestration, drops, money, capture, escape, death penalties, healing/revival, post-battle warp and later extension rewards.
- Remote validation **35513868341** passes at `6212cd394646778b2c47c07c931b5415efbec94e`.
- **Operational consequence:** combat-profile provenance and direct terminal HP/result return are closed to the first reconstruction-safe boundary. The next combat-side priority is to recover the exact ordinary EXP settlement orchestration before implementing rewards.

## Ordinary battle EXP accumulation and safe persistence boundary — 2026-09-20

- Stable-descendant `BATTLE_ClearGetExp()` / `BATTLE_AddExpItem()` / `BATTLE_GetExpGold()` ordering has now been recovered far enough to separate battle-local EXP accumulation from persistent EXP application.
- Ordinary single-hit R1 now preserves enemy reward provenance from `enemy.EXP` on each spawned `BattleParticipant`.
- `PersistentBattleState.pending_exp_by_participant_id` mirrors the descendant battle-local `CHAR_WORKGETEXP` seam:
  - initialized to zero for player-side participants;
  - an enemy reward is added only when an ordinary event first moves that enemy from `HP > 0` to `HP == 0`;
  - for ordinary single-target attack, only the acting player-side participant receives the award;
  - the existing level-gap formula is applied per defeated enemy;
  - no party-wide sharing is invented.
- `SinglePlayerHistoricalRuntime.finish_persistent_battle_without_level_crossing()` now permits EXP persistence only where both recovered descendant progression regimes agree: `current_exp + pending_exp < max_exp`.
- Reaching or crossing `max_exp` is rejected **before any HP/EXP mutation**, because two descendant progression regimes diverge at level transition:
  - legacy path: cumulative `CHAR_EXP` compared with cumulative next-level threshold;
  - later `_NEWOPEN_MAXEXP` path: current-level EXP compared with an external per-level requirement, then consumed on level-up.
- Stable `BATTLE_GetExpGold()` behavior is also preserved at this boundary:
  - dead player receives no EXP;
  - if the player is dead, the owned-pet EXP loop is never entered;
  - living pets are eligible only from the living-player result path.
- Player threshold crossing is now versioned instead of guessed:
  - `LEGACY_CUMULATIVE_EXP` preserves cumulative EXP and cumulative thresholds;
  - `PER_LEVEL_EXP` preserves later current-level EXP consumption;
  - every crossed player level yields +3 free-stat points and `new_level * 10` DP;
  - battle-result charm is +2 once when one or more levels are gained, not +2 per level;
  - threshold values after a crossing remain explicit caller inputs, so no later table is silently promoted to JSS.
- `finish_persistent_battle_with_player_progression()` applies those player transitions only when the caller selects the profile and supplies future thresholds; it also requires existing `free_stat_points`, `charm`, and `duel_point_like_state` fields.
- Pet threshold crossing is now closed to an explicit deterministic descendant boundary:
  - `PetGrowthState` persists PETRANK, individualized ALLOCPOINT, current internal V/S/T/D, and hidden VARIABLEAI;
  - persistence schema r3 stores VARIABLEAI, with explicit r1/r2 migration behavior;
  - `PetLevelGrowthRolls` carries all ten allocation draws plus the rank-band draw for one gained level;
  - `resolve_pet_exp_growth_transition()` requires exactly one roll bundle per level gained and composes it with the selected cumulative/per-level EXP profile;
  - `finish_persistent_battle_with_progression()` can now settle player and pet threshold crossings atomically;
  - pet level-up recalculates the already-closed max-HP/attack/defense/quick projection while preserving terminal battle HP rather than auto-healing;
  - hidden VARIABLEAI receives the stable +500-per-level update; visible pet AI remains a separate compliance seam and is not guessed.
- EXP side-path attribution is now closed to the stable-descendant boundary:
  - player kill profit can resolve an owned ride pet independently of the active allied-actor list;
  - ride-pet EXP uses that pet's own level-gap calculation, then 60% truncation, and can settle even when the pet never occupied a battle slot;
  - counter profit uses the actual counter actor as a one-entry attack list;
  - combo profit uses the complete eligible combo attack list and does not split EXP between members in the pinned enabled branch;
  - `BATTLE_AddExpItem()` source-shaped scanning is explicit: every `HP <= 0 && ISDIE == false` reward enemy is claimed by the current profit trigger, so deferred status deaths are **not** reassigned to an invented DoT owner.
- Battle item-drop mechanics and the current single-player runtime seam are now closed to the strong stable-descendant boundary:
  - enemy variants now preserve all ten \`ITEMn / ITEMPROBn\` source slots;
  - pinned Gavin \`version.h\` enables \`_FIX_ITEMPROB\`, so that build uses \`RAND(0,999) < ITEMPROB\`; the preserved \`0..99\` branch remains separately modeled because exact JSS-1999 selection is OPEN;
  - enemy-held items are instantiated at spawn, not invented at final victory settlement;
  - kill profit randomly selects an attack-list ticket, maps pet tickets to the owning player entry, and preserves duplicate-owner tickets rather than deduplicating them;
  - each player battle entry has a three-item pending reward buffer; overflow either destroys the new item or replaces/destroys one random old pending item;
  - concrete spawned `BattleDropItem` snapshots now flow through enemy participants, `PersistentBattleState`, ordinary-kill allocation and all persistent finish paths into the existing 20-slot `PersistentPlayerState.inventory`;
  - final item settlement takes the first empty persistent bag slot; no-space items are destroyed, and a dead player does not settle pending items;
  - detailed evidence is recorded in \`research/mechanics/STONEAGE-BATTLE-DROP-SETTLEMENT-R1.md\`.
- Battle money is now closed as a **negative stable-descendant invariant**, not as an invented reward formula:
  - Gavin and independent iriselia descendants both retain `BATTLE_GetExpGold()` but perform no battle `CHAR_GOLD` mutation and expose no `ENEMY_GOLD`, `WORKGETGOLD`, `_BATTLE_GOLD` or `getBattleGold` base path;
  - the ordinary economy still has persistent `CHAR_GOLD`, so this is specifically a battle-reward absence rather than a missing currency system;
  - a later Bismarck derivative adds an explicitly macro/config-gated `_BATTLE_GOLD / BATTLEGOLD` fixed bonus; it is treated as a later private-server extension and excluded from the base reconstruction;
  - the runtime regression fixture now preserves `gold=1234` unchanged across terminal battle and EXP-settlement paths;
  - exact JSS-1999 absence remains OPEN until original server evidence is recovered; detailed evidence is in `research/mechanics/STONEAGE-BATTLE-MONEY-R1.md`.
- Battle capture is now closed to the strong stable-descendant mechanics boundary and the current explicit single-player persistence boundary:
  - \`BATTLE_COM_CAPTURE\` / \`T|target\` now executes inside the ordinary action-order seam rather than remaining parse-only;
  - target adjustment keeps a still-valid submitted target or uses an explicit opposite-side retarget roll; capture-specific enemy/PETFLG eligibility remains in the capture check rather than being conflated with generic target validity;
  - capture requires an enemy target with PETFLG enabled and, unless \`PickAllPet\` is active, rejects targets more than five levels above the player before RNG;
  - \`enemybase.GET\` is preserved as \`capture_default\`; the stable formula uses current HP squared over max HP, level gap, fixed-DEX gap, target GET, fixed luck, fixed charm, temporary capture modifier and sleep +15, caps only above 99, then uses strict \`RAND(1,100) < WorkGet\`;
  - temporary capture modifier resets after the attempt;
  - five pet slots are scanned 0→4 for the first empty slot **after** a successful capture roll, so a full pet array can consume a successful RNG result and still fail;
  - success removes the enemy battle entry through a BATTLE_Exit-shaped transition without setting HP to zero, so it awards neither kill EXP nor held-item drops;
  - ordinary-round capture now requires a complete source-identified \`PetActor\` and validates slot, variant/template, level, HP and max-HP before atomically updating persistent pets;
  - both pinned Gavin and independent iriselia builds enable later \`_CAPTURE_FREES\` required-item extensions; those hard-coded conditions remain profile-specific/OPEN for early JSS and are not silently promoted into the base rule;
  - detailed evidence is recorded in \`research/mechanics/STONEAGE-BATTLE-CAPTURE-R1.md\`.
- Battle escape is now closed to the strong stable-descendant probability/action-state boundary, with final recovery deliberately isolated:
  - \`E\` maps to \`BATTLE_COM_ESCAPE\`; pet entries do not execute the ordinary escape branch;
  - \`BATTLE_ENTRY.escape\` initializes at 0, \`BATTLE_Escape()\` increments it before calling \`BATTLE_EscapeCheck()\`, and the check reads \`escape+1\`; the first ordinary attempt therefore uses effective attempt count 2 and this source off-by-one is preserved;
  - player fixed luck is clamped to 1..5; enemy escape luck maps RARE 0/1/other to 1/3/5;
  - opponent average level includes the source ABIO -100 adjustment before C-style truncating division;
  - ordinary probability uses the stable luck bands and strict \`RAND(1,100) < Esc\`, clamps only the lower end to 1 and does not cap the upper end;
  - PvP escape succeeds before RNG; forced escape still executes the probability check/RNG first but exits regardless of check failure;
  - successful player escape performs a BATTLE_Exit-shaped action exit, removes the active allied pet entry from subsequent action execution, and is represented as a distinct persistent \`escape\` terminal rather than victory/defeat;
  - stored escape-attempt counters are persistent battle-entry state and caller-provided contexts are checked against them, so failed attempts affect later attempts deterministically;
  - stable \`BATTLE_Finish()\` calls \`BATTLE_GetProfit()\` only for entries still present at finish, while successful escape has already cleared the player entry through \`BATTLE_Exit()\`; runtime victory/EXP/drop finishers therefore reject escape terminals instead of accidentally awarding pending battle profit;
  - exact BATTLE_Exit recovery/status cleanup is still a separate seam and has not been guessed into the escape return path;
  - dedicated `finish_persistent_escape()` now returns a successful escape to world state without calling the normal drop/EXP settlement path; player HP is preserved, active-pet battle HP is preserved, and every carried non-mail pet at HP≤0 is restored to HP=1, matching the stable player `BATTLE_Exit()` loop in the current no-pet-mail single-player scope;
  - detailed evidence is recorded in \`research/mechanics/STONEAGE-BATTLE-ESCAPE-R1.md\`.
- Common base status acquisition and its ordinary physical interaction seams are now closed to the pinned descendant boundary:
  - ordinary magic and item StatusChange delegate to the shared base status core and write their requested duration directly;
  - pet StatusChange (`BATTLE_COM_S_STATUSCHANGE=1008`) executes through the ordinary physical path, requires positive resolved damage, uses the stable `PerOffset=30 / Range=40 / Bai=2.0` profile, writes `turn+1`, and preserves the physical DRUNK post-write halving;
  - COM3 LOW/HIGH packing is reconstructed exactly and a stable pet-skill bridge now carries handler-side attack/defense work-power mutations into the round core without reparsing skill text;
  - Guardian eligibility is shared and deterministic; interception occurs after original-target dodge and before critical/damage, redirects physical status application to the guardian, forces redirected zero damage to 1 NORMAL, and suppresses the ordinary counter continuation;
  - `BATTLE_COM_S_GUARDIAN_ATTACK=1003` auto-registers the paired front-row owner; the defensive Guardian branch uses ordinary `GUARD` plus turn-local registration; enum-only `1004` has no common executable handler in the three pinned lineages;
  - active common statuses now interact with the alternating counter chain without a synthetic blanket block; positive counter damage uses the common damage-wakeup runtime;
  - Combo formation now uses pre-tick `CanMoveCheck`, later members run one early `StatusSeq` inside the starter branch, immobilized members are consumed/excluded, the source one-member-combo behavior is retained, and every positive combo member applies target damage-wakeup semantics.
- Still OPEN / deliberately excluded:
  - exact JSS-1999 choice of level-threshold regime/table;
  - maximum-level and pet-limit-level behavior;
  - complete visible pet AI/loyalty compliance projection;
  - early-JSS confirmation of the descendant `_Item_ReLifeAct` combo-profit compile path;
  - base DamageReact (VANISH > ABSROB > REFLEC) is closed for ordinary and Combo paths, including ride-pet immediate/deferred split interaction, continuation/status/wakeup ordering; later macro-gated TRAP/ACUPUNCTURE/BATTLE_MODEL variants remain excluded;
  - ride-pet physical damage sharing is closed to the stable-descendant boundary: ordinary `BATTLE_DamageSub`, Combo `BATTLE_DamageSubCale/BATTLE_DamageSub2`, ABSROB/REFLEC immediate split, ride-pet death unmount/PETFALL, persistent battle runtime and final owned-pet HP settlement are integrated without making the ride pet an active battle entry;
  - stable ultimate/knock-away handling is closed for ordinary attacks, no-DamageReact base Combo settlement, and Counter through the full base exit boundary: exact `maxHP * 1.2 + 20` classification, cross-hit `CHAR_WORKULTIMATE` accumulation/reset, ABIO/critical overrides, distinct ultimate-death penalties, immediate per-attack/per-counter `BATTLE_AddProfit` scanning, `BATTLE_UltimateExtra` entry removal, same-round later-action suppression, player HP=1/common-status/PETFALL/carried-pet exit recovery, and final profit eligibility are integrated; player PvE elder return is explicit rather than fabricated. Detailed evidence: `research/mechanics/STONEAGE-BATTLE-ULTIMATE-EXIT-R1.md`;
  - Combo + DamageReact ultimate coupling is closed to the literal pinned-source base behavior: immediate REFLEC/ABSROB/VANISH `BATTLE_DamageSub` calls keep HP/reaction/ride/`CHAR_WORKULTIMATE` side effects while their returned `IsUltimate` is discarded; final `BATTLE_DamageSub2` uses only deferred damage, and stale final-member REFLEC can rewrite the subsequent death-check/entry-flag target from the defender to the attacker. The round-local `BENT_FLG_ULTIMATE` lifetime and post-Combo AddProfit scan are preserved without normalization. Detailed evidence: `research/mechanics/STONEAGE-BATTLE-COMBO-DAMAGEREACT-ULTIMATE-R1.md`;
  - counter-with-ride is closed to the stable-descendant base boundary: positive Counter damage is first reduced to 75%, then passed through the same ordinary `BATTLE_DamageSub` ride split; rider/ride-pet HP, immediate unmount/PETFALL, subsequent same-chain no-share behavior and raw-damage-vs-rider-HP ultimate quantities are integrated. Detailed evidence: `research/mechanics/STONEAGE-BATTLE-COUNTER-RIDE-R1.md`;
  - later macro-gated status families remain open outside the reconstructed common poison/paralysis/sleep/stone/drunk/confusion runtime;
- Code validations:
  - `81e9572f1ff309982d13c7f1979a51516a5593a8` — pending ordinary kill EXP accumulation; runs **35514277568** and **35514277633** both success.
  - `b3207d71bc8dafa557e31d3450be2d6efb00bd29` — no-level-cross EXP persistence; run **35514525635** success.
  - `509ac9fa68e67ce3e962bb700eae7e1817aee578` — explicit player EXP transition profiles; run **35514947237** success.
  - `1a48e8f57d3673c3a902351a754b5c6e5d8907f4` — explicit player threshold-crossing settlement; run **35515032705** success.
  - `250a328660dcd070b0116880f4212c895818b0e8` — explicit multi-level pet growth/VARIABLEAI model; run **35515398842** success.
  - `95f7e1e36f06eb4f9a00f3a35088dba32f56acc8` — persistent pet loyalty-growth identity and staged atomic battle outcome; run **35515685028** success.
  - `687240810018cf5448daeef2e07d79f0e94dc3d3` — explicit pet threshold-crossing settlement; gameplay **35515940125**, pet-growth **35515940131**, and recovery probe **35515940173** all success.
  - `ab9d3d90b87fcb857bc5f6ee24a10f2d816ad793` — player-kill ride-pet attribution; battle-core **35516458527** and gameplay **35516458580** success.
  - `dce9ccc6a25f8135a5bad2145b1505c24b99528a` — reward-only ride-pet persistent settlement; gameplay **35516543065** success.
  - `56fdb2c17aa96b51252b4ee939b2a99664a09487` — counter/combo/deferred-status source-shaped profit scanning; battle-core **35516770864** and gameplay **35516770753** success.
  - `82692a51e05f1ca607178e901abd296bd84fa87b` — source-shaped battle-drop core; battle-core **35517467464** and gameplay **35517467477** success.
  - `cd1206d069c9fb2e61414996748ee24070e5cadd` — concrete pending-drop state plus persistent-inventory settlement; battle-core **35517775715** and gameplay **35517775683** success.
  - `bebb6c6fc8ddbf495cb8a9f159f63dd0e6f475e3` — normalized runtime/drop round signature ordering; battle-core **35517829479** and gameplay **35517829457** success.
  - `a5f27d5dd792406e653ded8f4e1dce770851a710` — preserve the stable no-battle-money runtime invariant; gameplay **35518043576** success.
  - `d832b32741ecf6d097be5f4640c55d4dfd4a3720` — capture gates/formula, strict RNG boundary and enemybase GET bridge; battle-core **35549443783** and gameplay **35549443834** success.
  - `7d321792543a537ea9318eb14b504c147518a843` — non-kill persistent capture transition and explicit captured-pet installation; battle-core **35549610051** and gameplay **35549610032** success.
  - `882a124471bda8ae31a22dfa6f75c3998afd4aaa` — capture execution inside ordinary action order / exited-target tracking; battle-core **35549871944** and gameplay **35549871985** success.
  - `cb7d57cbc6488f9c815c0043c72c99dce9672a4c` — atomic captured-pet persistence from ordinary battle rounds; gameplay **35549951206** success.
  - `cfa3f855f09e8147ba241d66428377ce3e1df20e` — stable escape probability/counter/PvP/forced-exit core; battle-core **35550194003** and gameplay **35550194001** success.
  - `454952adfbbef33090719bb2d45162481c188da7` — escape execution inside ordinary action order; battle-core **35550379184** and gameplay **35550379230** success.
  - `a8c228e946c1c810a1cf32c7cbba76aa0611f830` — persistent escape attempt counters and distinct player-escape terminal; battle-core **35550479374** and gameplay **35550479386** success.
  - `1502f77ff0e98892364368a280e0e085e78306e9` — stable normal-death penalty model; battle-core **35551474239** and gameplay **35551474260** success.
  - `cb0380b0445007dffe02f328786c50e9a07c3545` — accumulate normal-death battle penalties; battle-core **35551570877** and gameplay **35551570910** success.
  - `baeb1ac13c1f821f851d86598c804812dba4bbc6` — settle normal-death penalties and exit recovery; battle-core **35551877523** and gameplay **35551877522** success.
  - `0f45ed769fd171636b8d860ce171e3bde700c127` — stable counter probability, weapon matchup/gate and C-integer boundary; battle-core **35552584700** and gameplay **35552584734** success.
  - `c775b5780c69d52f6a19e297b610d30d602fac9f` — validated status-free alternating counter execution chain and actual-counter-actor profit routing; battle-core **35553042492** and gameplay **35553042493** success.
  - `be823c662f300ca6cefaba5de20deb7058c825c3` — stable post-sort base combo formation; battle-core **35553360554** and gameplay **35553360547** success.
  - `1bcbf15a07652f194d78b20c29a59a452f6b00cf` — stable status-free combo accumulated damage plus full attack-list EXP/drop routing; battle-core **35670646011** and gameplay **35670645876** success.
  - `badeba6934d07a9c0605bdac13fd8b32b31501c1` — common poison/paralysis/sleep/stone/drunk/confusion timing model; battle-core **35671000903** success.
  - `9c79098637943d8101a612e8e5ee80de6b694656` — integrate common statuses into ordinary/persistent rounds, including poison persistence, immobilization, confusion rewrite, stone defense and positive-damage sleep wake-up; battle-core **35671549996** and gameplay **35671550039** success.
  - `c06bff3e10610cb7b035ccb847bf235ecf620f37` — unify pet status-hit probability with the shared base-status core; pet-skill **35672999246**, battle-core **35672998977**, magic **35672999058**, item **35672998940** success.
  - `9b12bacf010281b8bffa51da1192ab742d9cf433` — execute pet StatusChange (`1008`) through ordinary/persistent rounds with source same-round decrement timing; battle-core **35673677261** and gameplay **35673677219** success.
  - `a1ac32a02870a475aad4bcdc13f8d30b647d69eb` — shared stable Guardian eligibility core; battle-core **35674077053** and pet-skill **35674077050** success.
  - `19138a26430b58e35f475f4f644d8dcf14d7dbb0` — Guardian interception in ordinary/persistent rounds; battle-core **35689247554** and gameplay **35689247544** success.
  - `11b264a3e1293a06f33845ea847109a859f02d76` — derive `S_GUARDIAN_ATTACK=1003` registration from the submitted command; battle-core **35689434766** and gameplay **35689434791** success.
  - `2fa7c2bde4ca882a2275f507d6f2a0e6f3a3d514` — bridge stable Guardian/StatusChange handler outputs into numeric round commands plus setup effects; pet-skill **35689840680** and battle-core **35689840660** success.
  - `a11cbc5693d220635000a156f4f499ea86d1aa6a` — integrate active common statuses with alternating counter execution and damage wake-up; battle-core **35690243546** and gameplay **35690243482** success.
  - `a86701f3afb09552b789c386abea6ad730c0ec2c` — integrate source-shaped common status timing with Combo formation/execution, including early later-member `StatusSeq` and one-member combo behavior; pet-skill **35690533578**, battle-core **35690533588**, gameplay **35690533586** success.
  - `466505c6f2f95b17431bdb5d8964a99a56bb7fab` — integrate stable base DamageReact into ordinary and per-member Combo execution, including Reflect redirection, Absorb/Vanish, continuation suppression, reaction charge persistence and explicit Combo aggregate settlement; battle-core **35692745170**, gameplay **35692745208**, pet-skill **35692745206** success.
  - `cb18f95f8023488698fbc7a171e19535377591a2` — repair ordinary ride-damage integration regressions and restore capture/counter/ride runtime consistency; battle-core **35705885777**, gameplay **35705885952**, pet-skill **35705885946** success.
  - `a3d8f4333a3f27f163ac76e2c6d398ccf18181a8` — integrate ride-pet sharing with Combo deferred settlement and ABSROB/REFLEC immediate reactions; battle-core **35706892102**, gameplay **35706892101**, pet-skill **35706892110** success.
  - `fe23831896c6654475df1d9b7648b3d08319d2f6` — persist non-entry ride-pet battle HP/PETFALL outcome through final owned-pet battle-exit settlement; gameplay **35707126569** success.
  - `a06b876b3beeb437c2f558103a802dc91472d99e` — recover the pure stable ultimate threshold/overkill accumulator, ABIO/critical override and distinct ultimate-death penalty core; battle-core **35709542102** and gameplay **35709542070** success.
  - `5b5c1c69da1f40a5ecf520b50f493a6677a9be5e` — integrate ordinary-attack ultimate resolution with explicit conditional RNG; battle-core **35710287966** and gameplay **35710287840** success.
  - `33cb29c89ae04cee751c138da087dc0de1ad181f` — persist ordinary ultimate accumulation and player/pet ultimate-death penalties through battle state; battle-core **35710773444** and gameplay **35710773551** success.
  - `a9ae37d232cb326f43bc7feeb23876627b032f8c` — integrate no-DamageReact base Combo final-settlement ultimate semantics with Combo's enemy-only critical override scope; battle-core **35711243416**, gameplay **35711243461**, pet-skill **35711243440** success.
  - `2f503cae53d88683871098fd5c625eda30876809` — integrate stable Counter ultimate threshold/accumulator and non-player critical-death override; battle-core **35712053357** and gameplay **35712053423** success.
  - `cc26b0ae30058caa01ed454d848326be0375d15b` — prove persistent Combo and Counter ultimate deaths select ultimate penalties rather than normal-death penalties; battle-core **35712203367** and gameplay **35712203319** success.
  - `2419c9c2119899764231ea334985f0cf4cac7041` — apply source-timed ultimate battle-entry exits immediately after attack/counter profit scans, including player/default-pet same-round removal and base exit cleanup; validated at descendant head `3d2163d26df3bb7403c3fed992c1fd171aecd9ea` by battle-core **35720347532** and gameplay **35720347455**, both success.
  - `cddb50c8b20bd0400fe8c6d6f72fc9a1e6dfe24a` — separate player-ultimate final settlement from ordinary finish, prevent restored HP=1 from re-enabling pending EXP/drop profit, and require explicit elder-return lookup outcome; gameplay **35720731472** success.
  - `fdc12106fa91a45d8cc08224e3d662b6685abdba` — represent source round-local `BENT_FLG_ULTIMATE` writes separately from damage classification and make persistent ultimate penalties depend on actual UltimateExtra exit; battle-core **35723010783**, gameplay **35723010759**, pet-skill **35723010689** success.
  - `17eae020746968f18cc8aa5cdd2839f9b7346fca` — close Combo + DamageReact ultimate coupling exactly as pinned: discarded immediate returns retain accumulator side effects, final `DamageSub2` uses deferred damage, and stale Reflect can misroute the entry ultimate flag; battle-core **35723491402**, gameplay **35723491531**, pet-skill **35723491375** success.
  - `ecdfcbb9404cc1593b0299fa50c47f720760aec0` / `80aad145d0a2945791c7480043bec71e4f137ca8` — close Counter + ride-pet through the source-shared `BATTLE_DamageSub` path, including 75%-scaled raw damage, rider/pet split, immediate unmount/PETFALL and later same-chain no-share behavior; battle-core **35724103327** and gameplay **35724103367** success.

## Japanese 1.74a Hangame launch-install chain — 2026-09-22

- The generic archive scan is now complemented by exact official Hangame launch-window evidence.
- `research/recovered/STONEAGE-JAPAN-174A-EXACT-INSTALL-CHAIN-R1.txt` records:
  - `sasetup.asp` snapshot **2003-12-14 05:55:53 UTC**;
  - `sasetup2.asp` snapshot **2003-12-15 09:53:20 UTC**;
  - both pages belong to the official `www.hangame.co.jp/publish/sa/` StoneAge subtree active during the 1.74a open-beta launch window;
  - `sasetup.asp` links to `sasetup2.asp` and the official download page `sadl.asp`;
  - archived `HgSA.cab` is a small Hangame control package, not the game client: recovered CAB metadata exposes `HgSA.dll` (38,400 bytes, timestamp **2003-12-14 21:20:46**) and `HgSA.inf` (233 bytes, timestamp **2003-12-14 21:05:14**).
- The later 2004 `HgSA.cab` captures share one Wayback digest, but the project does **not** infer byte identity with an unarchived 2003-12 response merely from the internal member timestamps.
- The launch-window official download page is now directly recovered: `sadl.asp` snapshot **2003-12-14 05:10:53 UTC** independently replays successfully and references the exact client URL **`http://hangame.gamania.co.jp/stoneage/sa174hg.exe`**. It also contains the secondary relative token `stoneage.exe`.
- The Japanese 1.74a **payload bytes** remain unrecovered until the exact URL's archive metadata/prefix is verified; installer-name discovery itself is no longer open.
- Source registration: `SRC-JP-2003-HANGAME-174A-INSTALL-CHAIN-01`.
- Validation:
  - exact-install workflow run **35730448438** — success;
  - focused `sadl.asp` run **35731811512** — success and independently reproduces the launch-client URL.

## Immediate next actions

1. **Populate the now-wired Taiwan-v1 cache → collision-profile → hit-map path when a provenance-safe early field-map corpus is recovered.** The strict DAT plane parser, derived collision-profile loader and composition adapter are already closed; until authentic bytes exist, do not substitute the mixed 2.5/SACH map corpus or fabricate absent retail-disc field maps.
2. **Close remaining default/runtime presentation gaps only when an implementation path actually needs them.** Exact early object-type numeric values and default NPC title/walkable/height behavior remain explicit/versioned until required.
3. **Use Taiwan 1.0 as the comparison anchor for future artifact recovery, but do not let broad archaeology block implementation.** JSS 1999 and Korean 1.74 remain high-value provenance targets; for Japanese 1.74a, validate and recover the now-exact official launch payload `http://hangame.gamania.co.jp/stoneage/sa174hg.exe`, keeping payload bytes/hashes separate from the already-proven launch-page URL.
4. **Treat the recovered mixed 2.5 bundle strictly as a bridge/specimen and keep historical reconstruction separate from redesign.** Never repair missing references by inventing data; later optimization/automation remains an explicit DESIGN layer.


## Continuity status

- Repository: `chinaneedM/stoneage-rebuild`
- Default branch: `main`
- Visibility: public
- Authority: latest GitHub remote state is the single source of truth for project continuity.
- Canonical restart protocol: `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`

## Blockers

No repository or workflow blocker.

The project still lacks a provenance-preserving **publicly obtainable** 1999 JSS retail disc image/dump and September 1999 beta binary. The Korean **Inium/Hananet/CNET 2000–2001** recovery track now has CNET's exact payload path/name (`/pc/games/online/stoneage.zip`, 257MB) and Hananet's exact full/trial mappings (`8119` / 260 M / `sa.exe`; `8120` / 240 M / `sa_demo.exe`), but still lacks recoverable client bytes, hashes/file tree, and byte-level equivalence evidence between the independently packaged mirrors. Korean `1.74` and the Japanese `1.74a` **game payload bytes** likewise remain unrecovered, so neither bridge target has yet established byte-level relationship to JSS. The Japanese launch-time Hangame installation/download chain itself is no longer unknown: official `sasetup.asp` / `sasetup2.asp` / `sadl.asp` snapshots and the small `HgSA.cab` control lineage are recovered, and the 2003-12-14 official download page directly identifies the client URL `http://hangame.gamania.co.jp/stoneage/sa174hg.exe`. LIFESTORM II and StoneAge JANs are directly resolved from public package photographs, but the StoneAge physical-package blocker remains the missing exact model/type code, disc identities and matrix identifiers; exact JAN/model searches still yield no trustworthy `JV...` field and the 13 Mercari originals are HTTP-403-blocked here. The beta web-recovery blocker remains a nearly complete application-page path; the Retromags No.015 object is identified down to filename, size, MD5 and seedbox target, but the scan body is still unreachable. Direct Wayback binary retrieval is independently blocked in the execution environment by DNS resolution failure, so the archived JSS `stoneage.exe` still has no recovered bytes. The developer-lineage track now has a named, independently cross-checked JSS/StoneAge staff lead in Yuki Tamura, but the original StoneAge credit list and exact staff-role mapping remain unresolved. The retail/client search retains `sa.exe`, `updated`, and `CheckForUpdate` only as descendant-derived search traits until original JSS material confirms each one independently. The missing 1999 JSS and Korean operator binaries remain lineage/recovery constraints, but they no longer block technical reverse engineering: the accepted Taiwan Waei/JSS v1.0 retail disc now provides a provenance-preserving early client baseline.
