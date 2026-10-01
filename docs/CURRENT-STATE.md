# Current State

Last updated: 2026-09-30

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
- **JSS `stoneage.exe` — TARGET-A recovered executable artifact:** the exact first-party path is known and the archived 2001 replacement object has now been replayed and analyzed transiently as a **217,088-byte x86 PE** (SHA-256 `6795d9349168f77aa025d7c4ea05d005c5bbfe33dd4b227eb7731802fa7eb82b`). It is not evidence of byte identity with the 1999 retail launcher, but it is the first recovered original-JSS executable byte artifact and directly exposes the updater host/path/resource-generation scheme.

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
   - Archive-path recovery is now bounded more precisely: the 1999 wildcard/index probe is **PARTIAL_NO_MATCH** with 0 literal tail matches on successful queries and multiple Wayback/network failures; a separate Availability pass completes **30/30** checks of the evidence-motivated `/~PO/`, `/%7EPO/`, `/PO/` and bare-host variants across six August/September dates and finds **0 archive captures**. These negative results are archive-coverage evidence only and do not resolve the printed glyph.
   - A second preservation path is registered: Retromags catalogs `Play Online No.015 (September 1999)` (submitted 2023-12-14), filename `Play Online No.015 (September 1999).cbr`, listed size **349 MB**, listed MD5 `e009cc707810c4361c849f26248593af`, and exact final seedbox object `https://seedbox.retromags.com:19918/Retromags%20Collection%202023/Play%20Online%20No.015%20(September%201999).cbr`. Current execution still fails DNS for the seedbox host, so no second-scan bytes or independent MD5 verification exist yet.
   - Still missing: the single OCR-ambiguous character before `PO`, an archived copy of the application page, tester/download instructions, installer/client filename, distribution method/media, hashes, internal version and beta-to-retail diff. Blind enumeration of more candidate characters is no longer a priority; prefer scan visual evidence or preserved URL lists.
6. **Test the LIFESTORM II → StoneAge REAL/ADRN resource-lineage hypothesis using free/public evidence.**
   - Progress: LIFESTORM II community preservation names `adrn_1.bin` / `real_1.bin` with address-data / image-data roles; two StoneAge descendant source trees preserve the same conceptual split, a concrete ADRN record structure, `RD` image-block signature, and matching legacy run-length/literal decoder implementation. A public StoneAge sample reverse engineering independently reports **80-byte ADRN records** beginning with image/file number, REAL offset and block length; the descendant source's Win32 layout independently totals the same 80 bytes. Separately, older CrossGate/StoneAge technical documentation plus three modern CrossGate decoder implementations converge on the same 16-byte `RD` header and nine-class RLE scheme, strongly corroborating a shared image-codec family.
   - Current limitation: the old free ASUS WebStorage backup links are unreachable from the present environment, so no LIFESTORM II byte-level validation has been performed. `LS2MAP` has now been separated as a later **server-map** format lineage and is not treated as evidence for LIFESTORM II client data.
   - Next proof target: a freely retrievable LIFESTORM II data copy or equivalent historical bytes; test `RD` headers and decoder compatibility separately from ADRN/map-index compatibility.
7. **Mine the surviving JSS/Gamer's Dream web archives for 1999 paths and support/update artifacts.**
   - Progress: JSS `manual.html`, `manual01.html`, `faqstart.html`, `verup.html`, `updater.html` and `stoneage.exe` paths are known; Gamer's Dream archive coverage begins before beta/launch; beta application matching can target the known `*PO/sa_apply.html` tail, but current wildcard/index coverage is partial and the tested exact `~PO`/plain-`PO` spellings have no 1999 Availability capture.
   - Priority targets: a scan-visual or preserved-URL-list resolution of the beta application path; linked tester/download instructions; update manifests/package names/endpoints; product/shop pages; registration; support/version pages; any original occurrence of `sa.exe`, `updated` or `CheckForUpdate`.
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
- Cross-linked that byte evidence to descendant source: floor 817 is grouped with 8007/8015/8027/8028/8029/8100/8101 in `_STATUS_WATERWORD`, `_NEWDRAWBATTLEMAP` and `_AniCrossFrame` branches. Several of those same floors also have missing graphics in the recovered DAT corpus. Exact whole-file equality of `817.dat` with the independently archived 2003-06-10/23 historical `map.exe` copy now shows the map file itself is not a later mixed-bundle mutation. The remaining mismatch is classified as **cross-revision map/resource skew** against the recovered `adrn_15.bin` / server-map set, not a DAT-format defect.
- Identified the dominant missing ranges: tile **5150–5421** (272 consecutive IDs / 133,014 refs) plus smaller early map ranges; parts gaps cluster heavily through the **11xxx** namespace. Exact source version remains OPEN.
- Completed a recovered **DAT ↔ server LS2MAP static-layer crosscheck**: 637 numeric DAT caches have same-ID/same-dimension server maps; **280** match both static layers exactly, **421** match tile exactly, and **361** match parts/object exactly. This strongly corroborates server `tile / obj` → client `tile / parts` while proving the mixed bundle contains multiple map revisions.
- Closed the main `1021.DAT` diagnosis boundary: its same-ID 407×144 server map differs in **39,456 tile cells** and **32,706 parts/object cells**, while DAT also contains **43,952 non-enum event cells**. It is therefore not an event-only hidden encoding. Exact whole-file equality with the independently archived 2003-06-10/23 historical `map.exe` corpus now rules out later mutation inside the recovered mixed bundle as the origin of this anomaly; its event semantics remain unresolved and it stays excluded from the canonical event model.
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
- Traced the Retromags `Play Online No.015 (September 1999)` record through its actual download layer: filename `Play Online No.015 (September 1999).cbr`, listed size **349 MB**, MD5 **`e009cc707810c4361c849f26248593af`**, and exact final object `https://seedbox.retromags.com:19918/Retromags%20Collection%202023/Play%20Online%20No.015%20(September%201999).cbr`. A fresh 2026-09-23 direct transient-workspace attempt still fails at DNS resolution for `seedbox.retromags.com`; no CBR bytes were obtained and the second scan body has not yet been visually compared with the Kingpin scan.
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
- **Exact Korean payload-filename preservation indexes are now bounded for the six recovered filenames.** A file-level/index pass tested GameTime `onlStoneAge.zip` and `stone_demo.exe`, Hananet `sa.exe` and `sa_demo.exe`, Gagamel `stoneagebeta.zip`, and CNET `stoneage.zip` against DiscMaster, Internet Archive item/file metadata, and the public old-disc torrent-path snapshot. Result: **0 strict DiscMaster hits, 0 Internet Archive items with strict file matches, 0 strict torrent-path hits, 0 errors**. Generic `sa.exe`/ `stoneage.zip` rows were deliberately rejected unless they had the required size or StoneAge/operator context. Reopen these filename-index surfaces only from a new preservation corpus, exact mirror/file token, checksum, or carrier identity. Derived report: `research/recovered/STONEAGE-KOREA-PAYLOAD-FILENAME-INDEX-R1.txt`.

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
  - enemy variants now preserve all ten `ITEMn / ITEMPROBn` source slots;
  - pinned Gavin `version.h` enables `_FIX_ITEMPROB`, so that build uses `RAND(0,999) < ITEMPROB`; the preserved `0..99` branch remains separately modeled because exact JSS-1999 selection is OPEN;
  - enemy-held items are instantiated at spawn, not invented at final victory settlement;
  - kill profit randomly selects an attack-list ticket, maps pet tickets to the owning player entry, and preserves duplicate-owner tickets rather than deduplicating them;
  - each player battle entry has a three-item pending reward buffer; overflow either destroys the new item or replaces/destroys one random old pending item;
  - concrete spawned `BattleDropItem` snapshots now flow through enemy participants, `PersistentBattleState`, ordinary-kill allocation and all persistent finish paths into the existing 20-slot `PersistentPlayerState.inventory`;
  - final item settlement takes the first empty persistent bag slot; no-space items are destroyed, and a dead player does not settle pending items;
  - detailed evidence is recorded in `research/mechanics/STONEAGE-BATTLE-DROP-SETTLEMENT-R1.md`.
- Battle money is now closed as a **negative stable-descendant invariant**, not as an invented reward formula:
  - Gavin and independent iriselia descendants both retain `BATTLE_GetExpGold()` but perform no battle `CHAR_GOLD` mutation and expose no `ENEMY_GOLD`, `WORKGETGOLD`, `_BATTLE_GOLD` or `getBattleGold` base path;
  - the ordinary economy still has persistent `CHAR_GOLD`, so this is specifically a battle-reward absence rather than a missing currency system;
  - a later Bismarck derivative adds an explicitly macro/config-gated `_BATTLE_GOLD / BATTLEGOLD` fixed bonus; it is treated as a later private-server extension and excluded from the base reconstruction;
  - the runtime regression fixture now preserves `gold=1234` unchanged across terminal battle and EXP-settlement paths;
  - exact JSS-1999 absence remains OPEN until original server evidence is recovered; detailed evidence is in `research/mechanics/STONEAGE-BATTLE-MONEY-R1.md`.
- Battle capture is now closed to the strong stable-descendant mechanics boundary and the current explicit single-player persistence boundary:
  - `BATTLE_COM_CAPTURE` / `T|target` now executes inside the ordinary action-order seam rather than remaining parse-only;
  - target adjustment keeps a still-valid submitted target or uses an explicit opposite-side retarget roll; capture-specific enemy/PETFLG eligibility remains in the capture check rather than being conflated with generic target validity;
  - capture requires an enemy target with PETFLG enabled and, unless `PickAllPet` is active, rejects targets more than five levels above the player before RNG;
  - `enemybase.GET` is preserved as `capture_default`; the stable formula uses current HP squared over max HP, level gap, fixed-DEX gap, target GET, fixed luck, fixed charm, temporary capture modifier and sleep +15, caps only above 99, then uses strict `RAND(1,100) < WorkGet`;
  - temporary capture modifier resets after the attempt;
  - five pet slots are scanned 0→4 for the first empty slot **after** a successful capture roll, so a full pet array can consume a successful RNG result and still fail;
  - success removes the enemy battle entry through a BATTLE_Exit-shaped transition without setting HP to zero, so it awards neither kill EXP nor held-item drops;
  - ordinary-round capture now requires a complete source-identified `PetActor` and validates slot, variant/template, level, HP and max-HP before atomically updating persistent pets;
  - both pinned Gavin and independent iriselia builds enable later `_CAPTURE_FREES` required-item extensions; those hard-coded conditions remain profile-specific/OPEN for early JSS and are not silently promoted into the base rule;
  - detailed evidence is recorded in `research/mechanics/STONEAGE-BATTLE-CAPTURE-R1.md`.
- Battle escape is now closed to the strong stable-descendant probability/action-state boundary, with final recovery deliberately isolated:
  - `E` maps to `BATTLE_COM_ESCAPE`; pet entries do not execute the ordinary escape branch;
  - `BATTLE_ENTRY.escape` initializes at 0, `BATTLE_Escape()` increments it before calling `BATTLE_EscapeCheck()`, and the check reads `escape+1`; the first ordinary attempt therefore uses effective attempt count 2 and this source off-by-one is preserved;
  - player fixed luck is clamped to 1..5; enemy escape luck maps RARE 0/1/other to 1/3/5;
  - opponent average level includes the source ABIO -100 adjustment before C-style truncating division;
  - ordinary probability uses the stable luck bands and strict `RAND(1,100) < Esc`, clamps only the lower end to 1 and does not cap the upper end;
  - PvP escape succeeds before RNG; forced escape still executes the probability check/RNG first but exits regardless of check failure;
  - successful player escape performs a BATTLE_Exit-shaped action exit, removes the active allied pet entry from subsequent action execution, and is represented as a distinct persistent `escape` terminal rather than victory/defeat;
  - stored escape-attempt counters are persistent battle-entry state and caller-provided contexts are checked against them, so failed attempts affect later attempts deterministically;
  - stable `BATTLE_Finish()` calls `BATTLE_GetProfit()` only for entries still present at finish, while successful escape has already cleared the player entry through `BATTLE_Exit()`; runtime victory/EXP/drop finishers therefore reject escape terminals instead of accidentally awarding pending battle profit;
  - exact BATTLE_Exit recovery/status cleanup is still a separate seam and has not been guessed into the escape return path;
  - dedicated `finish_persistent_escape()` now returns a successful escape to world state without calling the normal drop/EXP settlement path; player HP is preserved, active-pet battle HP is preserved, and every carried non-mail pet at HP≤0 is restored to HP=1, matching the stable player `BATTLE_Exit()` loop in the current no-pet-mail single-player scope;
  - detailed evidence is recorded in `research/mechanics/STONEAGE-BATTLE-ESCAPE-R1.md`.
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

## Original JSS launcher and updater archive — 2026-09-23

- The archived first-party replacement path `http://www.titan.co.jp/stoneage/stoneage.exe` is no longer metadata-only. Wayback CDX exposes captures at **2001-05-03 01:38:34 UTC** and **2001-07-09 04:19:51 UTC** with one archive digest; bounded transient replay recovers the same **217,088-byte** PE from both.
- Verified hashes: MD5 `8a5dc8b64f57574ffdd139a762a41aaa`, SHA-1 `43d4f038aca05d055b0f59cac26fd7fae4dbc099`, SHA-256 `6795d9349168f77aa025d7c4ea05d005c5bbfe33dd4b227eb7731802fa7eb82b`. PE timestamp: **2000-02-10 07:58:33 UTC**. The executable itself is **not committed**; only derived metadata is retained.
- Deep PE/resource analysis refines the artifact's identity:
  - VERSION CompanyName: **`日本システムサプライ株式会社`**;
  - FileVersion and ProductVersion: **`1.0.0.1`**;
  - FileDescription: **`SaUpdate`**;
  - OriginalFilename: **`SaUpdate.EXE`**;
  - copyright string: **`Copyright (C) 1999`**;
  - dialog title: **`ＳＴＯＮＥＡＧＥ 起動プログラム Ver 1.01`**;
  - UI actions include **`アップデートして起動`** and **`中断/キャンセル`**;
  - resource string ID 103 reports **`Windows ｿｹｯﾄの初期化に失敗しました。`**, directly confirming socket/network initialization belongs to this updater/startup program.
- Therefore the archived object should be described precisely as the **JSS StoneAge SaUpdate startup/update program distributed under the replacement path `stoneage.exe`**, not as proven game-client main executable bytes. The external replacement filename and the internal original filename are distinct facts.
- Resource-tree analysis finds six ordinary resource types (bitmap, dialog, icon, group icon, string table, VERSION), no embedded PE/CAB/ZIP payload, no overlay and no known packer marker. The very large zero-filled `.data` tail alone is **not** evidence of packing/self-extraction.
- First-party binary strings directly confirm:
  - updater host `update.gamersdream.ne.jp`;
  - manifest path `/~stoneage/newest.txt`;
  - remote payload template `/~stoneage/%s`;
  - local staging path `data\\download\\%s`;
  - checksum-error shape `(cksum:%u : File : %s)`;
  - generation-numbered payload/resource families including `sa_%d.exe`, `real_%d.bin`, `adrn_%d.bin`, `spr_%d.bin`, `spradrn_%d.bin`, `battle_%d.bin`, `battletxt_%d.txt`, `sound_%d.bin`, and `soundaddr_%d.txt`;
  - the literal state token `updated`.
- Reverse engineering now closes several updater semantics directly from the recovered SaUpdate bytes:
  - the manifest/update transport is implemented through MFC42 Internet classes: `CInternetSession`, `GetHttpConnection`, `OpenRequest`, `SendRequest` and `QueryInfoStatusCode`; the recovered `newest.txt` host/path therefore belongs to a concrete HTTP update path rather than a generic string-only lead;
  - the local resource-generation scanner uses the complete selector set **1–9**: **1=sa**, **2=real**, **3=sound**, **4=spr**, **5=spradrn**, **6=adrn**, **7=soundaddr**, **8=battle**, **9=battletxt**. This mapping is grounded by all 23 direct callers plus the scanner's wildcard/prefix branches;
  - selector 7 resolves `data\\soundaddr_%d.txt` and selector 9 resolves `data\\battletxt_%d.txt`; neither selector function references either of the two unresolved launch-control buffers;
  - final process launch is an `_execl` vector beginning with the generated `sa_%d.exe` path and literal `updated`, followed by state strings for `realbin`, `adrnbin`, `sprbin`, `spradrnbin`, then two manifest-derived IP control arguments. The parser copies the **complete first two `IP` manifest lines** in encounter order into globals `0x85c2fc` and `0x85befc`; those exact globals are `_execl` arguments 8 and 9;
  - the no-import helper at RVA `0x3c60` has been executed under bounded x86 emulation. Its verified call shape is **source string, 1-based token index, destination buffer, maximum length**; it splits on **space, tab and colon**, collapses repeated delimiters, and returns an empty destination when the requested field is absent. It is used by later `data\\se` / `battleMap` / `pal` parsers and is **not promoted to the `newest.txt` parser without direct evidence**;
  - the file checksum helper at RVA `0x3f20` has been isolated with stubbed CRT I/O and verified on eight synthetic byte sequences. Its observed 32-bit checksum is **`Σ(byte[i] + i)` with zero-based `i`**; this candidate matches **8/8** bounded emulation cases, while CRC32, Adler32, plain byte sum, XOR and length do not.
- The checksum-error string `(cksum:%u : File : %s)` can therefore now be tied to a concrete recovered checksum routine.
- The **core parser grammar of `newest.txt` is now materially closed from first-party code plus bounded helper emulation**:
  - RVA `0x1f80` is a verified delimiter-driven **1-based field extractor**; 21/21 synthetic emulation cases return deterministically;
  - the manifest parser first uses delimiter **`0x0a` (LF)** to select successive records, then delimiter **`0x3a` (`:`)** to extract fields **1 through 5** from each non-empty record;
  - empty colon fields are preserved and whitespace is not trimmed by the helper; splitting CRLF text on LF leaves the preceding CR in the selected field;
  - the parser compares colon field 1 against `EXE`, `SPRBIN`, `SPRADRNBIN`, `REALBIN`, `ADRNBIN`, `SOUNDBIN`, `SOUNDADDRTXT`, `BATTLEBIN`, `BATTLETXT`, `IP`, `IP:1` and `MESSAGE`;
  - the nine resource records resolve to the **same selector map independently recovered from local resource scanning**: `EXE=1`, `REALBIN=2`, `SOUNDBIN=3`, `SPRBIN=4`, `SPRADRNBIN=5`, `ADRNBIN=6`, `SOUNDADDRTXT=7`, `BATTLEBIN=8`, `BATTLETXT=9`;
  - for the nine resource keys, the core record grammar is now **`TYPE:FILENAME:SIZE_BYTES:CHECKSUM:FIELD5`**;
  - the parsed resource record has fixed stride **`0x114`**: filename text at `+0x000..+0x0ff`, selector at `+0x100`, expected checksum at `+0x104`, byte size at `+0x108`, filename-derived generation at `+0x10c`, and a later-consumed control/update flag at `+0x110`;
  - field 2 is the resource/payload **filename**; field 3 is converted with `atoi`, stored at `+0x108`, rendered as `%d bytes`, and accumulated into the download-byte total, proving **SIZE_BYTES** semantics;
  - field 4 is converted with `atoi`, stored at `+0x104`, and directly compared against the return value of checksum helper RVA `0x3f20` after download, proving **expected CHECKSUM** semantics;
  - helper RVA `0x2060` derives the resource generation from the field-2 filename. Bounded emulation now passes **10/10** synthetic cases, including `real_12.bin -> 12`, `spr_0017.bin -> 17` and `real_beta_9.bin -> 9`; this value is stored at record `+0x10c`;
  - record `+0x110` is now closed as the **selected-for-update/download flag**. Helper RVA `0x2530` takes `selector, min_generation, max_generation` and writes `+0x110=1` for matching records whose filename-derived generation is inside that inclusive interval; later download loops skip zero-flag records;
  - helper RVA `0x2570` takes a selector and returns the maximum filename-derived generation among matching manifest records, or `-1` when none exists. The focused semantic probe verified all **15/15** required normalized instruction patterns.
- The control-record roles are now materially separated:
  - `IP`: the first two matching records copy their **full original manifest line** into the two final launch-control buffers; the inner payload syntax/value remains OPEN until an authentic `newest.txt` sample is recovered;
  - `MESSAGE`: colon field 2 is routed to **MFC42 `CWnd::SetWindowTextA`** (ordinal 6199, mapped from the pinned VC6 `MFC42.DEF`), so this is updater presentation text and is **not** a final launch-control argument;
  - a literal `IP:1` comparison branch exists, but the verified ordinary field-1 extraction is colon-delimited index 1, meaning a normal `IP:1:...` line first dispatches as `IP`. Direct reachability of the separate `IP:1` branch is therefore not demonstrated.
- Field 5 is now closed at the **consumer-side parser boundary**: it is extracted into a temporary buffer, but the normalized manifest function contains exactly **one** reference in the relevant stack window—the extraction destination at RVA `0x1aad`—and **zero post-extraction references**. This SaUpdate build therefore parses but does not consume field 5 and creates no persistent record member from it. The historical manifest producer-side meaning, if any, remains OPEN.
- **Still OPEN:** the exact payload contents carried by the two historical `IP` lines and any producer-side meaning of the ignored fifth column require a surviving authentic manifest; these are evidence-value questions, not blockers for reconstructing this updater build's behavior.
- This promotes the updater host/manifest/payload-template/resource-family model from descendant inference to **first-party JSS binary evidence**. It does **not** prove that the archived 2001 launcher is byte-identical to the 1999 retail or beta launcher.
- A follow-on 1999–2002 Wayback CDX probe tested exact `newest.txt` targets plus prefix neighborhoods for `update.gamersdream.ne.jp/~stoneage/` and a separately labeled source-derived `www.titan.co.jp/~stoneage/` candidate. All **6** tested exact/prefix queries completed with **0 errors**, **0 saturation**, and **0 index rows**.
- Evidence boundary: the zero-row archive-index result does **not** disprove the historical updater paths exposed by the launcher. It only means the tested Wayback CDX surface currently provides no manifest/resource capture to replay.
- Derived reports:
  - `research/recovered/STONEAGE-JSS-LAUNCHER-ARCHIVE-PROBE-R1.txt`;
  - `research/recovered/STONEAGE-JSS-LAUNCHER-DEEP-PROBE-R1.txt`;
  - `research/recovered/STONEAGE-JSS-SAUPDATE-SEMANTIC-R1.txt`;
  - `research/recovered/STONEAGE-JSS-SAUPDATE-XREF-R1.txt`;
  - `research/recovered/STONEAGE-JSS-SAUPDATE-HTTP-FLOW-R1.txt`;
  - `research/recovered/STONEAGE-JSS-SAUPDATE-FUNCTION-FLOW-R1.txt`;
  - `research/recovered/STONEAGE-JSS-SAUPDATE-GLOBAL-BUFFERS-R1.txt`;
  - `research/recovered/STONEAGE-JSS-SAUPDATE-CALL-ARGS-R1.txt`;
  - `research/recovered/STONEAGE-JSS-SAUPDATE-HELPER-SEMANTICS-R1.txt`;
  - `research/recovered/STONEAGE-JSS-SAUPDATE-TOKEN-EMULATION-R1.txt`;
  - `research/recovered/STONEAGE-JSS-SAUPDATE-CHECKSUM-EMULATION-R1.txt`;
  - `research/recovered/STONEAGE-JSS-SAUPDATE-LAUNCH-PARAMETERS-R1.txt`;
  - `research/recovered/STONEAGE-JSS-SAUPDATE-MANIFEST-GRAMMAR-R1.txt`;
  - `research/recovered/STONEAGE-JSS-SAUPDATE-MANIFEST-LINE-EMULATION-R1.txt`;
  - `research/recovered/STONEAGE-JSS-SAUPDATE-MANIFEST-GRAMMAR-SUMMARY-R1.txt`;
  - `research/recovered/STONEAGE-JSS-SAUPDATE-GENERATION-SUFFIX-EMULATION-R1.txt`;
  - `research/recovered/STONEAGE-JSS-SAUPDATE-MANIFEST-RECORD-R1.txt`;
  - `research/recovered/STONEAGE-JSS-SAUPDATE-MANIFEST-RECORD-LAYOUT-R1.txt`;
  - `research/recovered/STONEAGE-JSS-UPDATE-ARCHIVE-PROBE-R1.txt`.
- Validation includes launcher **35781291855**, deep structure **35948368684**, semantic **35948545627**, xref **35948787670**, parser/call-argument **35951460845 / 35951653442**, helper semantics **35951664729**, token emulation **35951529320**, checksum-rule verification **35951872034**, launch-parameter **35951951617**, manifest grammar **35954056510**, manifest-line emulation **35954129823**, generation-suffix emulation **35954573651**, manifest-record consumers **35954509013**, record-layout **35954899766**, update-selection semantics **35954929935**, MESSAGE window mapping **35955249881**, manifest-control semantics **35955281338**, field5 consumption **35955406349**, and updater-path **35781723407** — all successful final runs. Earlier failed/cancelled CI attempts are not evidence.

## Korean 1.74 archive-recovery evidence boundary — 2026-09-22

- The Netmarble 2003 launch-version target remains historically valid: same-period evidence names the 2003-07-28 service version as `1.74`.
- A separate contemporaneous ETNews report dated **2003-07-11** records Netmarble's launch strategy as starting from StoneAge's **`개발초기 버전` (early-development version)** and upgrading afterward. Read together, these sources prove an early-state launch strategy plus the public label `1.74`; they do **not** establish byte identity with Inium/JSS or any other regional client carrying the same numerical label.
- The bounded dual-index/root probe now distinguishes requested dates from the actual capture dates returned by Wayback Availability. Its corrected R2 result is **`PARTIAL_NO_HITS`** for the target period:
  - indexed URLs in the 2003–2004 bounded query: **0**;
  - launch-window root snapshots (2003-07 through 2003-09): **0**;
  - all 2003–2004 root snapshots: **0**;
  - early interesting links: **0**;
  - later candidate root snapshots: **6**;
  - later candidate links: **11**.
- The later official Netmarble candidate surface includes the 2006 `/cp_site/stoneage/down/down_load.asp` and `down_debugler.asp` routes. These are useful descendant path clues only; they are **not** evidence that the same paths or payloads existed for the 2003 1.74 launch.
- The former report behavior that allowed a nearest-later Availability capture to produce generic `HITS` has been removed. Only evidence inside the bounded early period can now advance the Korean 1.74 result.
- Derived report: `research/recovered/STONEAGE-KOREA-174-ARCHIVE-CLIENT-PROBE-R1.txt`.
- A separate Internet Archive item/file-list metadata pass now closes that bounded surface for the known 2003 launch anchors:
  - exact queries for Korean `스톤에이지 + 1.74`, English `StoneAge + 1.74`, Korean `넷마블 + 스톤에이지`, the historical `game3.netmarble.net/stoneage` host, and `20030728 + StoneAge` return **0 target items**;
  - `Netmarble + StoneAge` returns two 2002 Mainland-China Waei CD-ROM items whose modern descriptions mention Netmarble as IP owner; they are description-level false positives for this Korean-2003 recovery question and are not promoted into the 1.74 lineage;
  - the scan finds **0 exact-name payload matches** and no size-window candidate attributable to a Korean 1.74 query.
- Derived report: `research/recovered/STONEAGE-ARCHIVE-CANDIDATE-FILES-R1.txt` R4, bot commit `37cfe42571f1cd712f2e7fe6b6fa24f19664ca2f`.
- Validation: Korea archive run **35734946655** and high-precision IA metadata run **35778883888** — success.

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
- A second deterministic pass over that same archived page retains no page prose but derives a **248MB** client-size token, **2** occurrences of `sa174hg.exe`, **1** occurrence of `stoneage.exe`, and a normalized visible-text SHA-256 `990aec04c1a078ac4255bb4cc9a5eed69fda2cff3329ccfc9ed110e6b9a9f92b`. No explicit version token is present in the page's normalized visible text; the 1.74a version remains independently anchored by the contemporaneous Mado no Mori release metadata.
- The Japanese 1.74a **payload bytes** remain unrecovered; installer-name and launch-page size discovery are no longer open. The exact-payload recovery surface is now bounded more tightly:
  - Wayback exact CDX: no recovered row in the current probe; some requests time out;
  - Wayback Availability: no exact `sa174hg.exe` capture found for the launch/near-launch key dates;
  - Wayback Memento TimeMap for the exact URL: **0 mementos**;
  - Arquivo.pt exact target: **0 results**;
  - Internet Archive metadata/file scan: exact `sa174hg.exe`, exact official URL, `StoneAge + 1.74a`, and `STONE AGE + 248MB` queries all return **0 target items**, with **0 exact-name file matches**;
  - Common Crawl exact/prefix probe is **INCONCLUSIVE**, not a no-hit result: all 128 requests in that bounded run failed with 503/timeouts.
  - Wayback CDX prefix-neighborhood scan over **8** HTTP/HTTPS and www/non-www official-host prefixes for 2003–2005 completed with **0 errors** and **0 saturated prefixes**. The four `hangame.gamania.co.jp/stoneage/` variants return **0 indexed rows**; the four `hangame.co.jp/publish/sa/` variants each canonicalize to the same **1,046** indexed rows / **98** relevant launch-or-binary rows, but contain **0 indexed `sa174hg.exe` rows**. This is a bounded archive-index result only and does **not** disprove an unindexed original payload or historical mirror.
  - Redump's current public PC contents index has now also been tested directly: **8/8** Japanese/global coverdisc/demo/content queries completed successfully with **0 indexed `StoneAge` / `sa174hg.exe` rows**. This closes only the tested Redump contents-index surface; it is not evidence that no historical magazine/demo carrier existed.
  - DiscMaster's public file-level index was independently schema-discovered rather than queried with guessed parameters. Exact/deep searches return **0 direct matches** for `sa174hg.exe` (filename and indexed content), `WR-04156`, and JAN `4988609011565`; the Japanese title query likewise returns 0 in the bounded 2003–2004 content search. Generic `Hangame AND StoneAge` / `Gamania AND StoneAge` searches return three text co-occurrences whose root carriers are **CHIP 2005 November**, **Retro Gamer 5**, and a French `ftp.ac-grenoble.fr` mirror; their indexed paths are unrelated to a StoneAge Japanese client/disc, so they are retained as **false-positive co-occurrences**, not carrier hits.
- These negative/indeterminate surfaces now close the useful official-host Wayback index neighborhood for the known filename. The next recovery step should prioritize historical mirrors, physical carriers and exact-size/name secondary distribution evidence rather than repeating official-host filename guesses.
- Source registration: `SRC-JP-2003-HANGAME-174A-INSTALL-CHAIN-01`.
- Validation:
  - exact-install workflow run **35730448438** — success;
  - focused `sadl.asp` run **35731811512** — success and independently reproduces the launch-client URL;
  - structured launch-page metadata run **35733850300** — success and derives the 248MB package-size anchor without retaining page prose;
  - exact-payload TimeMap fallback run **35734544741** — success, exact `sa174hg.exe` TimeMap rows = 0;
  - high-precision Internet Archive metadata run **35734351311** — success, no exact Japan-1.74a target item/file match;
  - Common Crawl run **35733694437** — workflow success but all 128 index requests failed, therefore evidence status remains INCONCLUSIVE on that backend.
  - Wayback prefix-neighborhood run **35781109170** — success; 8/8 prefixes completed, 0 errors, 0 saturation, 0 indexed `sa174hg.exe` rows. Derived report: `research/recovered/STONEAGE-JAPAN-174A-WAYBACK-PREFIX-R1.txt`.
  - Redump contents-index run **35956457024** — success; 8/8 tested queries completed with 0 matching rows. Derived report: `research/recovered/STONEAGE-JAPAN-174A-REDUMP-CONTENTS-R1.txt`.
  - DiscMaster schema run **35964684411** and bounded target run **35964968496** — success. Derived reports: `research/recovered/STONEAGE-DISCMASTER-SEARCH-SCHEMA-R1.txt` and `research/recovered/STONEAGE-JAPAN-DISCMASTER-TARGETS-R1.txt`.

## Japanese 2004 retail-package carrier target — 2026-09-22

- A contemporaneous 4Gamer report dated **2004-05-20** states that the Japanese retail package went on sale that day before the 2004-06-03 formal service launch.
- The package is explicitly described as containing **two CD-ROMs with the game client**, two 30-day tickets, an installation/game-guide manual and an Upopo dinosaur strap.
- The same article's retailer link resolves to the exact official path **`http://stoneage.to/package.html`**; the formal-service link resolves to `service.html`.
- The official package page is now independently recovered at Wayback timestamp **20040604192109**. Its derived, prose-free metadata closes the physical-product identity:
  - JAN/EAN-13: **`4988609011565`**;
  - package/model code: **`WR-04156`**;
  - one CD-ROM token, one Upopo token and two 30-day tokens in normalized visible text;
  - normalized visible-text SHA-256 `4a1187b9aa876442e99828437836a5dec3e0b7185f6785c4faaf6b66f1802f39`.
- The page also recovers the period retailer target **Item City product_id=423** and package-art asset `/image/package/illust_01.jpg`.
- This package is now a uniquely searchable high-value **near-descendant physical carrier**. It may provide a complete Japanese client and therefore a controlled diff target against Taiwan v1.0 and the 2003-12 1.74a install chain.
- The older collector-photo chain is now re-openable through its article mirror and adds disc-level corroboration: the package back explicitly lists **2 game CDs + 2 game tickets**, while one photographed game-disc face itself carries `WR-04156`, `CD-ROM`, Windows 98SE/Me/2000/XP, DigiPark and BOTHTEC. No readable disc ordinal, matrix/mastering string or IFPI code is available from that image.
- Evidence boundary: the May/June 2004 package must **not** be treated as byte-identical to the December 2003 1.74a client without disc-image comparison. The two packaged CDs must likewise not be assumed byte-identical merely because one photographed disc shares the package model code.
- A modern Redump public-index probe now checks the Japanese PC catalogue using the current `redump.info` query schema recovered from the open-source `superg/vgindex` implementation. All **7/7** completed title/model/barcode queries returned valid Disc Database pages with **0 results**, including exact serial `WR-04156` and exact barcode `4988609011565`. This closes the **currently indexed Redump Japan-PC identifier surface only**; it does not prove the two physical discs do not exist or have never been dumped elsewhere. The legacy `redump.org` host is connection-refused in CI and is not used as negative evidence.
- Derived Redump report: `research/recovered/STONEAGE-JAPAN-2004-REDUMP-PROBE-R1.txt`.
- Validation: Redump modern-index run **35956304228** — success; resolution `REDUMP_NO_IDENTIFIER_HIT`.
- Derived reports: `research/recovered/STONEAGE-JAPAN-2004-PACKAGE-PROBE-R1.txt` and `research/recovered/STONEAGE-JAPAN-2004-REDUMP-PROBE-R1.txt`.
- Source registrations: `SRC-JP-2004-4GAMER-RETAIL-PACKAGE-01` and `SRC-JP-2004-STONEAGE-PACKAGE-PAGE-01`.
- Validation: package-page run **35735602501** — success.

## Taiwan v1 field-map recovery boundary — 2026-09-24

- The accepted Taiwan Waei/JSS v1.0 retail disc remains authoritative for early client resources, but it contains **zero ordinary field-map/cache files**. The v1 runtime independently proves that ordinary fields are delivered/maintained through the runtime `M` / `MC` protocol paths and persisted as `map\\%d.dat`; the strict three-plane DAT parser and Taiwan-v1 ADRN collision-profile composition path are already implemented.
- A new DiscMaster file-index probe searched six distinctive early-client filenames — `sa_3.exe`, `adrn_1.bin`, `spradrn_1.bin`, `battletxt_1.txt`, `soundaddr_1.txt`, and `waei.bin`. All **6/6** searches completed with **0 exact signature carriers**, therefore no multi-signature installed-tree candidate and no `map/<n>.dat` candidate was available on that tested DiscMaster surface. Derived report: `research/recovered/STONEAGE-TW10-DISCMASTER-MAPCACHE-R1.txt`; validation run **35966819067** — success.
- A broader Internet Archive item/file-list metadata pass tested the same six signatures plus StoneAge / Traditional-Chinese / Waei query neighborhoods. It enumerated **454 unique candidate items** and successfully fetched **453** in the primary pass; none contained any target signature or `map/<n>.dat`. The only timeout, `NPWK19720801`, was independently retried and resolved as the unrelated text item **華僑日報 1972-08-01**, with **0** target signatures and **0** map-cache rows. Read together, the primary scan plus timeout retry close the tested IA metadata surface with no qualified installed-tree carrier. Derived reports: `STONEAGE-TW10-IA-INSTALLED-TREE-R1.txt` and `STONEAGE-TW10-IA-INSTALLED-TREE-TIMEOUT-R1.txt`; validation runs **35966952301** and **35967915007** — success.
- The S-grade preservation seed `stoneage_tw_2000_win` was also expanded through its uploader/creator/collection neighborhood. The bounded neighborhood resolves six related preservation items, including the StoneAge seed and other Waei/Hwaei titles, but **0** items contain map-cache rows or Taiwan-v1 installed-tree signatures. This closes the most direct “same preservation chain” expansion route. Derived report: `research/recovered/STONEAGE-TW10-IA-PRESERVATION-NEIGHBORHOOD-R1.txt`; final redacted-query run **35967848938** — success.
- The preserved mixed 2.5 bridge corpus was classified only as a **necessary-condition / HYPOTHESIS prioritization surface** against the Taiwan-v1 ADRN map-number set. Of **995 parseable DAT maps**, **769** use only ADRN-resolvable tile/parts IDs and **226** reference at least one ID absent from the v1 collision profile; **16** additional DAT files are not valid three-plane map caches. The 226 incompatible maps can be excluded from any byte-identical v1 hypothesis. The 769 compatible maps are **not promoted to Taiwan-v1 history**: resource-ID compatibility cannot establish map age, layout identity, event-plane identity, or provenance. Derived report: `research/recovered/STONEAGE-TW10-25-FIELDMAP-COMPAT-R1.txt`; validation run **35967312558** — success.
- External exact-hash / exact-filename searches for the accepted v1 runtime/resource fingerprints produced no new public installed-tree lead. Later technical/map corpora such as StoneAge 8.0-derived documentation or unrelated LIFESTORM II map backups may corroborate file-format lineage only; they must **not** be substituted for Taiwan-v1 field-map evidence.
- **OPEN:** recover a provenance-preserving early StoneAge installed/running directory, server-captured `M`/ `MC` map stream, authenticated cache backup, or another early client branch whose field maps can be version-diffed. Until then, the map-cache adapter remains intentionally unpopulated for the Taiwan-v1 historical baseline.



## 2001–2002 StoneAge 2.x / 2.5 distribution recovery — 2026-09-24

- Two contemporaneous Mainland portal records independently anchor the **2.5 rollout**: retail availability on **2002-01-20**, server migration beginning in early February (Sina gives **2002-02-04**), and an **8.25 MB** upgrade program for existing 2.x installs. They disagree slightly on the full-package size — **575 MB** in Sina versus **580 MB** in 17173 — so the size is retained as a source conflict rather than normalized.
- Both records state that Beijing Waei hosted a downloadable complete 2.5 package and the 8.25 MB updater, and both enumerate period magazine/guide cover-disc distribution channels. Public DiscMaster/Internet Archive searches over those named carriers currently produce **0 strict 2.5 carrier hits**; broad lexical hits were filtered as unrelated.
- The archived official Beijing-Waei `/ZHUANQU/stoneage2/` site is real and richly preserved. Three independently replayed February-2002 official pages point to `/ZHUANQU/stoneage2/tyro/upgrade.asp`; however, the exact February-2002 destination body is not preserved in the tested CDX surface.
- Wayback Availability exposes an older capture of that same path at **2001-12-04 16:57:11 UTC**. A clean `id_` replay is **75,141 bytes**, SHA-256 `73fde66ffb3c92261d66715f873fa9b9f54166e4443d5d29924fe137cdcb8d35`, and explicitly identifies **石器时代2.0**. Its visible content is the guide page **“升级所需经验”** (experience required to level up), not a client/software upgrade page. Structural extraction yields **99 candidate site references and 0 strong payload references**.
- **CORRECTION / EVIDENCE BOUNDARY:** the historical pathname `tyro/upgrade.asp` cannot be interpreted as “software updater” merely from the English word `upgrade`. In the preserved 2001 body it means character level-up/experience. Therefore the 2001 page does **not** identify any 2.5 installer, updater filename, download host, or payload topology. The February-2002 links prove only that Waei linked that pathname at rollout time; without the 2002 destination body we must not assume its content was unchanged or that it became a software-download page.
- A bounded Jan–Mar 2002 CDX scan of the Waei domain family for `.exe/.zip/.cab/.rar` artifacts found **23 candidate URLs** but **0 strict StoneAge 2.5 client/updater candidates** after excluding StoneAge2 self-executing Flash showcases and unrelated Waei titles. The tested direct Waei binary-index surface is therefore substantially bounded, but external FTP/CDN targets and unindexed cover-disc copies remain OPEN.
- A second exact-carrier pass tested **19 source-derived physical identities** (three official 2.5 package families plus named Jan/Feb-2002 magazine/guide carriers) against DiscMaster and Internet Archive. It returned **0 strict DiscMaster hits, 0 strict IA items, 0 preserved media-file hits, 0 query errors**. This closes the currently tested public-index route for those exact carrier names.
- **New physical recovery lead:** current public marketplace pages show a surviving boxed Mainland `石器时代2.5 精灵王传说 新手报到包` with original box, game disc and reply card, plus separate 2.5 optical-disc listings. Independently, the surviving 17173 product page states that both `春满钱坤包` and `延年益兽包` contained a **2.5 client CD**. These are now the shortest concrete carrier leads, but remain **LEAD/HYPOTHESIS** until a read-only disc image or file tree is obtained and hashed. Price/commercial value is out of scope. Derived lead report: `research/recovered/STONEAGE-SA25-LIVE-PHYSICAL-LEADS-R1.md`.
- **Modern public 2.5 candidate closed as a clean-client lead:** the currently downloadable `https://99ds.com/downloads/windows/Stoneage2.5-Windows.rar` was recovered transiently and fingerprinted without committing proprietary bytes. The served RAR is **553,320,338 bytes**, SHA-256 `0e157c0fcfe2bcf91826907d580d4403138d86fab9488aa39cd9494af17449ae`, with response filename `SA2.5-20260823.rar` and a 2026 Last-Modified timestamp. Its extracted corpus is **5,009 files / 1,421,974,641 bytes** and includes `SACH-MX0.30` plus a **113,106,052-byte x86-64 `OnlineUpdater-自动更新.exe` timestamped 2026-06-16**. The site's “original/unmodified” wording is therefore retained only as a modern source claim, not provenance.
- Normalized client-tree comparison against the already recovered mixed 2.5 bridge proves direct descendant/common-corpus relationship: **2,299 shared paths; 2,286 byte-identical; 13 changed; 170 candidate-only; 3 bridge-only**. All four large resource generations (`real_15.bin`, `adrn_15.bin`, `spr_4.bin`, `spradrn_5.bin`) contain the known bridge files as **exact byte prefixes**. `StoneAge.exe` is byte-identical to the bridge copy, while `sa_2903.exe` is same-size but changed.
- The client DAT map ID set is exactly the same **1,011 IDs** as the bridge: **1,009 byte-identical**, with only `map/2000.DAT` and `map/3000.dat` changed. The public archive therefore does **not** move field-map provenance earlier; it is classified as a **modern descendant/community distribution control**, useful for resource-evolution comparison but not as a clean 2002 baseline.
- Derived reports: `research/recovered/STONEAGE-SA25-PUBLIC-CANDIDATE-R1.txt` and `research/recovered/STONEAGE-SA25-PUBLIC-VS-BRIDGE-R1.txt`.
- **2009 standalone-client mirror route bounded:** a 2009-12-17 preservation/private-server thread exposes the exact historical client URL `http://download1.92ysa.com/YSA2.5.8.rar` and reports roughly **420 MB**. The surrounding instructions explicitly use a private-server/single-player environment, so this is not clean-client proof. An exact preservation probe found **0 Wayback HTTP/HTTPS 200 captures, 0 Wayback Availability snapshot, 0 Internet Archive exact-filename items and 0 DiscMaster rows**. No payload recovery was possible. Keep the exact URL/filename as a historical mirror token, but do not spend primary effort repeating the same public-index queries. Derived report: `research/recovered/STONEAGE-YSA25-ARCHIVE-PROBE-R1.txt`.
- **WeLoveSA `tid=2132` public surface bounded without bypassing access controls:** the forum index publicly lists `〖2.5纯净〗石器客户端`, author `rayrix`, date **2012-09-26**, and sale price **5 石币**. Anonymous page 1/printable responses expose the title shell but no client filename, size, hash, attachment ID, or download URL. Anonymous pages **2–5** all resolve to the login/permission shell; the dedicated reply probe extracted **0 download or attachment references**. The tested Wayback surface yielded no relevant `tid=2132` capture. Therefore `纯净` remains only the community title label, and the thread remains a high-value lead only if an independent repost/mirror or legitimately accessible artifact token appears. Derived reports: `research/recovered/STONEAGE-WELOVESA-25-CLEAN-THREAD-R1.txt` and `research/recovered/STONEAGE-WELOVESA-25-CLEAN-REPLIES-R1.txt`.

- **StoneAge 2.5 source-named carrier set corrected from 19 to 20:** contemporaneous 2002 Sina/17173 upgrade instructions also name **《轰炸鸡》游戏** as a medium from which owners could obtain either the 2.5 full package or the 8.25 MB updater. Independent Beijing-Waei 2003 StoneAge 6.0 product records later bundle an 《轰炸鸡》 game disc with StoneAge, confirming that this is a real Waei-channel carrier identity rather than an isolated list typo. A later collector catalogue supplies search-only aliases `哇靠轰炸鸡完美中文版` and local ID `2001C226` with literal publisher string `华议国际`; these are not silently normalized to `华义国际` and are not contemporaneous provenance. The refined exact-carrier probe now covers **20 targets** and completed with **0 strict DiscMaster hits / 0 strict Internet Archive items / 0 interesting IA carrier files / 0 errors**. For the 《轰炸鸡》 target specifically, eight DiscMaster and eight IA alias/association queries all returned no strict Waei/StoneAge carrier hit; generic IA `轰炸鸡` metadata returned 18 items but none carried the required Waei/StoneAge association. Keep this identity OPEN for Chinese/Waei disc scans, package photos, catalogues, file trees or independent reposts, but do not repeat the same exact DiscMaster/IA metadata pass. Foreign `Chicken Shoot` media are controls only. Derived records: `research/clients/STONEAGE-SA25-BOMBING-CHICKEN-CARRIER-R1.md` and `research/recovered/STONEAGE-SA25-EXACT-CARRIERS-R1.txt`.

- **Beijing-Waei historical FTP resource route bounded at the tested 2000–2002 surface:** CDX/domain and resource-prefix probing resolves only one early topology row, `http://ftp.stoneage.com.cn:80/battlemap/battle218.sab` at **2001-05-16**, and that row is HTTP **404**, not payload bytes. A follow-up exact-resource Availability sweep covered **128 HTTP/HTTPS URL×date queries** across `StoneAge.exe`, `sa_3.exe`, `Setup.ini`, the known resource-bin names, `data/` variants, `battlemap/battle218.sab`, `battletxt_1.txt` and `soundaddr_1.txt`, with **0 bounded status-200 captures / 0 replayed payloads / 28 API-rate-limit errors**. Therefore the tested exact/prefix route is now BOUNDED but not a global negative on the historical FTP host. Do not repeat the same guessed path set; reopen only when an independent historical page, cache, installer or mirror supplies a new path/filename token. Derived reports: `research/recovered/STONEAGE-SA25-FTP-DOMAIN-R1.txt`, `research/recovered/STONEAGE-FTP-RESOURCE-PATHS-R1.txt`, and `research/recovered/STONEAGE-FTP-RESOURCE-AVAILABILITY-R1.txt`.

- Derived reports: `research/recovered/STONEAGE-SA25-DISTRIBUTION-CARRIERS-R1.txt`, `research/recovered/STONEAGE-WAEI-SA25-DOWNLOAD-R1.txt`, `research/recovered/STONEAGE-WAEI-SA25-PAYLOAD-INDEX-R1.txt`, `research/recovered/STONEAGE-WAEI-SA25-KEYPAGES-R1.txt`, `research/recovered/STONEAGE-WAEI-SA25-TYRO-SUBTREE-R1.txt`, `research/recovered/STONEAGE-WAEI-2002-PAYLOAD-DOMAIN-R1.txt`, and `research/recovered/STONEAGE-WAEI-PRE25-UPGRADE-CAPTURE-R1.txt`.

- **New photographed Mainland 2.5 physical-disc identity:** a public collector photograph exposes a disc labeled **`永远的石器时代 2.5 精灵王传说`**, **万方数据电子出版社**, ISBN **`7-900096-07-8/Z.03`**, with visible barcode **`9787900096074`**. This is a uniquely searchable physical-media lead, but it is **not** promoted to Beijing-Waei official-client provenance: the disc face alone does not establish whether it contains the full client, the 8.25 MB updater, multimedia/guide content, or a combination. An exact DiscMaster/Internet Archive preservation pass over ISBN/barcode/title/publisher variants completed with **0 strict DiscMaster hits / 0 strict IA items / 0 interesting IA carrier files / 0 errors**. The single raw DiscMaster row returned by the ISBN query was inspected and is an unrelated Brockhaus Multimedia 2007 update path, so it is closed as a false positive. Derived records: `research/clients/STONEAGE-SA25-WANFANG-DISC-R1.md` and `research/recovered/STONEAGE-SA25-WANFANG-DISC-PROBE-R1.txt`.
- **Old-disc collector catalogue / torrent route now bounded for client-media recovery on the tested surface:** the recovered CHM/RTF catalogue directly preserves `2001C226 哇靠轰炸鸡完美中文版`, approximately **210M**, shooting genre, with literal publisher string `华议国际`; this remains later preservation metadata and `华议` is not silently normalized to `华义`. Expanded CHM/RTF scanning found no catalogued StoneAge Online / `精灵王传说` / `StoneAge` / Wanfang client item; occurrences of `石器时代` were ordinary prose/historical-era wording and `华义` hits belonged to other games. The public `allseeds.zip` corpus contains **89 torrent metadata entries**. R1 initially misclassified an unrelated `读者 2002年第11期（总第280期）` path as strong; corrected R2 completes with **0 exact target strong hits / 81 weak catalogue-neighborhood hits / 0 errors**. A second signature-level pass over exact early-client/resource names (`StoneAge.exe`, `sa_3.exe`, `adrn_1.bin`, etc.) plus StoneAge title/ISBN signatures finds **0 exact-signature paths / 0 multi-exact client candidates / 5 lexical paths / 0 errors**. The five lexical paths reduce to unrelated historical uses, a same-name mini-game, and one secondary-documentation lead `大软石器时代特刊纪念册.pdf`; none is a provenance-preserving client or map source. Reopen this client-media route only if a new exact catalogue ID, disc image filename, checksum, package identity, installed-tree token or repost appears. Derived reports: `research/recovered/STONEAGE-SA25-OLD-DISC-CATALOG-NEIGHBORHOOD-R4.txt`, `research/recovered/STONEAGE-SA25-OLD-DISC-TORRENTS-R2.txt`, and `research/recovered/STONEAGE-OLD-DISC-TORRENT-SIGNATURES-R1.txt`.

## 2.5 physical-media carrier classification gate — 2026-09-24

- A specialist StoneAge collector series now supplies a **source-type classification baseline** for physical discs: official client media, magazine-gift media and strategy-book-gift media are explicitly separated, with mainland/Taiwan variants.
- For the **2.5 精靈王傳說** segment specifically, the collector identifies a pictured disc as the **mainland client unified-artwork disc**, paired with a distinct Taiwan disc. Separate package posts also identify a 2.5-period disc in the `延年益壽包` and document multiple Waei-era 2.5 client-package variants.
- A crucial nuance is retained: the collector states that some mainland strategy-book gift discs are still simply client installer packages. Therefore **secondary carrier provenance != technically useless bytes**; such media may preserve a useful installer but must receive a lower provenance grade until compared with an operator/official anchor.
- The photographed **Wanfang** ISBN/barcode disc is therefore reclassified only as **OPEN / UNCLASSIFIED-CARRIER**. It is neither promoted to official Beijing-Waei client media nor rejected. The next high-value test is artwork/package linkage to the known mainland unified-client-disc family, followed by read-only file-tree/hash comparison if bytes become publicly recoverable.
- Physical-media intake should now record `carrier_class = official_client | magazine_gift | strategy_book_gift | other_publisher | unknown` before any clean-client promotion.
- Canonical source record: `SRC-CN-COLLECTOR-SA25-DISC-CLASSIFICATION-01` in `docs/SOURCE-REGISTRY-PHYSICAL-MEDIA-R1.md`.

## StoneAge 2.5 physical-image evidence deduplication — 2026-09-24

- R2 visual fingerprinting successfully loaded **11 Ruten full-size listing images** and **3 large Wanfang collector images** without committing image bytes.
- The two standalone Ruten disc listings (`21926883918096` and `22242541948520`) collapse into a **single strong visual-source cluster** despite different image SHA-256 values: **1,605 ORB matches / 1,538 good<=64 / 743 RANSAC inliers / 0.4831 inlier ratio**. They must not be counted as two independent surviving-disc observations unless separate physical provenance is established.
- The boxed/new-user-package listing (`22632305238624`) is not a whole-frame near-duplicate of the standalone source cluster; its strongest boxed-vs-standalone comparison is **50 inliers / 0.0472**. This does **not** prove different carrier artwork because the disc may occupy only a cropped/occluded region of a package photograph.
- The Wanfang page yields three large recoverable images; no Ruten-vs-Wanfang pair approaches the standalone near-duplicate signal (maximum **27 inliers / 0.0322**). Therefore the Wanfang photographs are treated as an **independent visual-source cluster**, while their carrier class and client-byte relationship remain OPEN.
- The known mainland unified-client reference at `cos.stoneage.cn` remained connection-refused, so R2 makes no official-reference match claim. Next useful image work is **disc-localized/crop-aware comparison plus a working collector-reference mirror**, not additional whole-frame marketplace counting.
- Canonical derived analysis: `research/clients/STONEAGE-SA25-PHYSICAL-IMAGE-LINEAGE-R1.md`; raw derived metrics: `research/recovered/STONEAGE-SA25-PHYSICAL-IMAGE-FINGERPRINTS-R2.txt`.



## StoneAge 2.5 local disc-region comparison — 2026-09-24

- A new SIFT+RANSAC local-region probe removes the main weakness of prior whole-frame comparison by treating the standalone Ruten disc photographs as query templates and searching for local artwork inside boxed-package / Wanfang / collector images.
- Positive control remains strong: standalone Ruten disc `21926883918096` -> `22242541948520` gives **290 good matches / 231 RANSAC inliers / 0.7966 inlier ratio**, with broad query/target coverage and a sane homography.
- The best boxed-new-user-package relation is materially weaker: **32 inliers / 0.3107**, covering only **7.47%** of the standalone query and **3.94%** of the boxed target. A second query direction yields **22 inliers / 0.2619** with broader coverage. This supports shared local visual elements but does **not** prove that the boxed package contains the same disc artwork as the standalone listings.
- Wanfang remains unlinked: its best nominal row reaches **21 inliers / 0.2727**, but only **0.3%** query coverage and an invalid/exploded homography. No robust local-region evidence ties Wanfang to the standalone disc cluster.
- Collector-mirror rows with superficially high **95–99** inlier counts are rejected because target coverage collapses to near zero and the projected quadrilateral is invalid; they are treated as repeated-text/logo false positives.
- Therefore the physical-media evidence model remains: **one deduplicated standalone-disc visual cluster + one boxed new-user-package lead + one independent Wanfang visual-source lead**, with no byte-level equivalence claim between them.
- Canonical interpretation: `research/clients/STONEAGE-SA25-PHYSICAL-IMAGE-LINEAGE-R1.md`; derived metrics: `research/recovered/STONEAGE-SA25-DISC-REGION-MATCH-R1.txt`.

## 2002–2003 field-map lineage bridge — 2026-09-24

- The contemporaneous Sina **2002-11-08 StoneAge 4.0 map patch** remains the earliest concrete complete-map package target currently identified: download record `aid=61620`, source-derived basename `shiqi4updatex_02_11_08.zip`, stated size 3440K. Its bytes are **not recovered**. Exact filename/stem searches found **0** carriers in DiscMaster and Internet Archive, and a bounded Wayback scan of **2,149** archived Sina `download.pl` URLs from 2002-11 through 2005 found **0** rows containing `aid=61620` or the target basename. Source-page Availability replay is currently rate-limited (HTTP 429), so this target remains OPEN rather than declared lost.
- A Wayback replay of the contemporaneously linked mirror `http://www.wuxitianlong.com/sa/map.exe` at **2003-06-23 23:44:51 UTC** is byte-recoverable and hash-locked as SHA-256 `372426e46765a1cf479041bdafc1d3e58fb019117d00d0b43d6a5f796620776e`. It contains **1,008 numeric DAT map IDs**, with **995** valid strict three-plane maps and **13** numeric parser-invalid files. Taiwan-v1 ADRN necessary-condition classification gives **773 compatible / 222 incompatible** among the 995 parseable maps.
- A second capture of the same historical mirror at **2003-12-10 09:24:26 UTC** is independently byte-recoverable as SHA-256 `5f7f58e0d26d596e926a7d551d7c24e8a9a27824d5bdc53be3955b19b0e13abc`. It extracts successfully with `unar` and contains **1,011 numeric DAT maps**, of which **998** parse strictly and **13** do not. Relative to June, **698** common maps are byte-identical, **310** common maps changed, and **3** IDs were added: `8008`, `8100`, `8101`. Taiwan-v1 resource classification gives **772 compatible / 226 incompatible** among the 998 parseable maps.
- Archive file mtimes survive and are not flattened. The June package's 1,008 map entries span mtime years **1997:10, 2000:129, 2001:278, 2002:419, 2003:172**; the December package has **337 map entries stamped 2003-10-20**. These timestamps are useful stratification metadata only — the presence of pre-StoneAge dates such as 1997 proves they cannot be treated mechanically as map release dates or provenance dates.
- Three-state comparison of **June 2003 / December 2003 / separately preserved 2.5** corrects the earlier implicit linear chronology. Across the 1,008 IDs common to all three: **698 are byte-stable in all three**, **295 are June=preserved-2.5 with December alone divergent**, and **15 have three distinct byte states**. Therefore the preserved 2.5 map directory is **not** a simple temporal successor to the December 2003 package; it preserves a different branch/state that is much closer byte-for-byte to the June corpus.
- Taiwan-v1 compatibility patterns across the same 1,008 common IDs are: **768 C→C→C**, **4 C→C→I**, **1 C→I→C**, **222 I→I→I**, and **13 X→X→X** (C=resource-compatible, I=incompatible, X=strict-parser invalid). The four C→C→I maps are **1000, 2000, 3000, 4000**: both dated 2003 snapshots remain v1-resource-compatible, while the separately preserved 2.5 state introduces IDs absent from the v1 profile. Map **60306** is the inverse branch signal, **C→I→C**, with the December state alone introducing missing resource ID `10940`.
- Maps **1000/2000/3000/4000** are three-distinct, not a simple “later overlay” sequence. All four are rewritten in the December package with mtime **2003-10-20**, but their December SHA-256 values match neither June nor preserved-2.5. The preserved-2.5-only absent-v1 IDs cluster around `11208`, `22310/22356/22413/22434`, and `24305–24322`. Their semantic identity remains OPEN.
- **EVIDENCE BOUNDARY:** asset compatibility is a necessary-condition filter only. Neither a 2003 map, an old-looking archive mtime, nor byte equality between descendant corpora proves Taiwan-v1 map membership. The Taiwan-v1 historical map adapter remains intentionally unpopulated until a provenance-preserving pre-/near-v1 field-map source is recovered.
- Derived reports: `research/recovered/STONEAGE-HISTORICAL-MAP-CAPTURE-R1.txt`, `research/recovered/STONEAGE-2003-MAP-VS-25-R1.txt`, `research/recovered/STONEAGE-TW10-2003-FIELDMAP-COMPAT-R1.txt`, `research/recovered/STONEAGE-2003-MAP-TIMELINE-R1.txt`, `research/recovered/STONEAGE-SA40-MAP-FILENAME-ARCHIVE-R1.txt`, `research/recovered/STONEAGE-SA40-MAP-CARRIER-R1.txt`, and `research/recovered/STONEAGE-SA40-SINA-AID-61620-R1.txt`.


## Old-disc torrent signature surface bounded — 2026-09-24

- The new metadata-only scanner ran successfully in GitHub Actions against the public 老光盘群 `allseeds.zip` snapshot (**89 torrent entries**).
- It found **0 exact StoneAge client/resource signature paths** and **0 multi-signature client candidates**. Only **5 lexical title matches** appeared across 4 torrents; the only directly game-related title was a later `大软石器时代特刊纪念册.pdf`, not client/media bytes.
- The preceding StoneAge-2.5 catalogue-neighborhood scan likewise produced **0 strong target hits**. The `2001 NEW GAME 093（总第280期）2CD` / `2001C226 哇靠轰炸鸡完美中文版` clue is now explicitly classified as a **later collector/pirate-compilation search token**, not the original Waei 《轰炸鸡》 carrier.
- Therefore the tested 老光盘群 torrent-metadata surface is **BOUNDED** for direct 2.5 clean-client recovery. Do not repeat the same path scan unless the upstream torrent index materially changes or a new exact filename/disc identity appears.
- Derived reports: `research/recovered/STONEAGE-SA25-OLD-DISC-TORRENTS-R2.txt` and `research/recovered/STONEAGE-OLD-DISC-TORRENT-SIGNATURES-R1.txt`.


## StoneAge 2.5 source-named carrier torrent boundary — 2026-09-24

- The exact carrier list was revalidated against contemporaneous Sina/17173 StoneAge 2.5 upgrade instructions before interpreting old-disc hits: the named magazine discs are issue-specific, predominantly **2002-02**, with `计算机与航空` explicitly **2002-01** and `中学生电脑` a 2002 strategy special.
- The 89-entry 老光盘群 torrent snapshot then produced **0 strict source-named carrier paths**. It contains 37 lexical-neighborhood paths across 12 torrents, but all are wrong-month/year or generic-title neighbors under the source boundary.
- In particular, `电脑报配套光盘之游戏世界200201.iso` is **not** the target; the StoneAge source names `《电脑报——游戏世界》2002年2月号`.
- Exact public-web follow-up likewise produced no inspectable exact issue image on the tested search surface.
- Therefore this current torrent/index route is **BOUNDED** and should not be rescanned until the upstream snapshot changes or a new exact issue/disc token appears.
- Canonical note: `research/clients/STONEAGE-SA25-NAMED-CARRIER-TORRENT-BOUNDARY-R1.md`; derived scan: `research/recovered/STONEAGE-SA25-NAMED-CARRIER-TORRENTS-R1.txt`.

- **Adjacent `电脑报·游戏世界` preservation anchor:** an independent modern preservation catalogue identifies the January-2002 issue as `GAMEWORLD200201.iso`, **657,821,696 bytes**, SHA1 **`6241658796F0DF05199F39154E2F4E8D18330837`**. This corroborates the old-disc torrent's `...游戏世界200201.iso` path as a real issue family. The February token `GAMEWORLD200202.iso` is retained only as an **inferred exact-search token**, not a recovered filename fact. Use it for one bounded DiscMaster/IA exact-token pass; do not generate further guessed filenames without independent evidence.

- **Adjacent-token closure:** a bounded DiscMaster + Internet Archive metadata pass over `GAMEWORLD200202`, `GAMEWORLD200202.iso` and Chinese February-2002 variants returned **0 DiscMaster hits / 0 IA items / 0 candidate files / 0 errors**. The inferred filename route is therefore BOUNDED; `GAMEWORLD200201.iso` remains the verified adjacent control, while `GAMEWORLD200202.iso` is not a recovered historical filename. Derived report: `research/recovered/STONEAGE-SA25-GAMEWORLD-200202-PROBE-R1.txt`.


## StoneAge 2.5 bridge installer-residue boundary — 2026-09-24

- The recovered mixed 2.5 bundle has now been checked specifically for original installer residue. Its `stoneage2.5/` root is already a fully expanded runtime/resource tree and contains `UNWISE.EXE`, but **no client-root INSTALL.LOG / SETUP.EXE / SETUP.INI / AUTORUN.INF / CAB / MSI / HDR / INX / ISS package layer**.
- Embedded PE timestamps are also heterogeneous: `Startup.exe` **2001-07-13**, operator-looking `StoneAge.exe` **2002-01-11**, contaminated `sa_2903.exe` **2002-04-10**. These timestamps are lineage metadata only, not authenticated release dates.
- Operational classification: treat the subtree as an **installed/deployed client directory later repackaged**, not as the original January-2002 installer-media layout. Therefore stop using this bridge to guess the original 575/580 MB full-package filename or 8.25 MB updater filename.
- Canonical interpretation: `research/clients/STONEAGE-SA25-BRIDGE-INSTALL-RESIDUE-R1.md`.


## StoneAge 2.5 exact historical download token: `sa25up.zip` — 2026-09-25

- A surviving third-party software-link mirror explicitly labels **`石器時代2.5—精靈王傳說`** and points it to the exact historical-looking URL **`http://202.104.32.168/file/game/maoxian/sa25up.zip`**. The mirror itself states it was copied from `http://pcpc.idv.tw/soft/soft.htm`; its original publication date and the payload's operator provenance are not established; the historical IP host is now identified separately as 21CN.COM download infrastructure.
- This exact filename/path is a legitimate new recovery token because it was not previously present in the repository and it is independently sourced rather than guessed from the 575/580 MB full-package or 8.25 MB updater descriptions.
- A bounded metadata-only preservation probe checked Wayback Availability at four period anchors, Arquivo.pt exact-URL CDX, eight Common Crawl index generations, DiscMaster exact filename search, and Internet Archive item/file metadata. Result: **0 preservation hits / 0 errors**.
- Therefore the current exact-URL/file-index route is **BOUNDED**. Reopen it only from a new hostname/IP mapping, mirror URL, directory/file token, capture identifier, or preservation source.
- **EVIDENCE BOUNDARY:** `sa25up.zip` was initially only a filename/path lead and the `up` suffix alone was not evidence. **This ambiguity is now superseded by native 21CN record `20165`, which explicitly classifies the linked file as a `客户端升级包` with size `8473 k` / later `8.27M`.** The remaining boundary is byte identity/integrity: the ZIP itself is still unrecovered, so exact equality to the contemporaneously reported **8.25 MB** operator updater remains unproven.
- Derived report: `research/recovered/STONEAGE-SA25-SA25UP-EXACT-R1.txt`.
- Canonical source record: `SRC-CN-SA25-SA25UP-LINK-MIRROR-01` in `docs/SOURCE-REGISTRY.md`.



## StoneAge 2.5 sa25up archival-neighborhood chronology — 2026-09-25

- The independently sourced exact path `http://202.104.32.168/file/game/maoxian/sa25up.zip` now has a bounded Wayback neighborhood chronology.
- Wayback CDX contains malformed/suffixed URL records at **2002-07-12** (`sa25up.zip+`), **2002-09-29** (`sa25up.zip&nbsp`) and **2003-06-23** (`sa25up.zip%20`), plus an exact unsuffixed URL record at **2006-01-05**. **Every one of these payload-path records is HTTP 404**, so they are URL-circulation/crawler evidence only and provide no archived client/update bytes.
- The Geocities-attributed source `pcpc.idv.tw/soft/soft.htm` has successful Wayback source-page captures beginning with a currently identified **2003-06-05 10:48:51 UTC** snapshot, followed by 2003-12-03 and 2005-01-01 captures.
- Arquivo.pt produced no relevant exact/prefix rows. The Common Crawl branch is **inconclusive**, not negative: all 32 tested queries failed with service 503/504/timeouts.
- The dated source-page body has now been replayed successfully. The **2003-06-05 10:48:51 UTC** capture is HTTP 200, 406,274 bytes, SHA-256 `604304bd2c931c463ccb575f3920dd096a340441825a58274d9f6e897dc966c5`, and its raw bytes directly match Big5/CP950 `下載`, `石器時代2.5`, and `精靈王傳說`.
- The page literally contains **`[下載]石器時代2.5—精靈王傳說`** linked to `http://202.104.32.168/file/game/maoxian/sa25up.zip`. The same exact row/href survives in the 2003-12-03 and 2005-01-01 source captures.
- Therefore **2003-06-05 is now the terminus-ante-quem for the link text on the archived source page**. This does not prove the linked payload was live, official, clean, or equal to either the documented 8.25 MB updater or 575/580 MB full package; all currently recovered payload-path Wayback records remain HTTP 404.
- Derived reports: `research/recovered/STONEAGE-SA25-SA25UP-NEIGHBORHOOD-R1.txt` and `research/recovered/STONEAGE-SA25-PCPC-SOURCE-REPLAY-R1.txt`.
- Canonical dated source record: `SRC-CN-2003-PCPC-SA25UP-SOURCE-ARCHIVE-01`.

## StoneAge 2.5 DiscMaster file-signature boundary — 2026-09-25

- A direct file-index search used bridge-byte-verified distinctive resource names `adrn_15.bin`, `real_15.bin`, and `spradrn_5.bin`, plus supporting `StoneAge.exe`, `Startup.exe`, and `UNWISE.EXE`.
- All three distinctive resource names returned **0 exact DiscMaster rows**. Generic names produced many unrelated weak rows but **0 candidate carriers / 0 strong carriers / 0 errors**.
- Therefore the current DiscMaster “hidden client tree by verified filename” route is **BOUNDED**. Reopen only from a new distinctive verified filename/hash, exact carrier identity, or materially changed preservation index.
- Derived report: `research/recovered/STONEAGE-SA25-DISCMASTER-SIGNATURE-CARRIERS-R1.txt`.



## StoneAge 2.5 `sa25up.zip` historical host identity — 2026-09-25

- Archived pages from **2001-12-27** and **2002-02-01** establish that historical IP `202.104.32.168` served the **21CN.COM download site**. The archived root is titled `21CN.COM - 下载`; archived software-detail pages expose `download.21cn.com`, license string `粤ICP证010001`, and the copyright notice `世纪龙信息网络有限责任公司版权所有`.
- Therefore the host identity is no longer OPEN: the IP behind `/file/game/maoxian/sa25up.zip` belongs to the 21CN software-download infrastructure in the relevant period, **not to a demonstrated Beijing-Waei operator host**.
- This improves provenance classification. Native record 20165 now resolves the mirrored object's catalogue identity, Beijing-Waei attribution and expected size, but 21CN remains a third-party distribution surface; the project still lacks the ZIP bytes, byte hash, archive tree and proof of operator-to-mirror byte identity.
- The native StoneAge 2.5 detail record has now been located as `list.php?id=20165`; its catalogue metadata and delivery topology are recovered. The next high-information step is exact recovery of one of its evidence-derived ZIP mirror generations.
- Derived reports: `research/recovered/STONEAGE-SA25-HOST-IDENTITY-R1.txt`, `research/recovered/STONEAGE-SA25-HOST-NEIGHBORHOOD-R1.txt`.



## StoneAge 2.5 `sa25up` 21CN same-stem sidecar — 2026-09-25

- The evidence-derived 21CN hostname archive contains an HTTP-200 object at **2002-05-17 23:58:42 UTC**: `http://download.21cn.com:80/file/game/maoxian/sa25up.jpg`.
- The JPEG body is directly replayable: **9,312 bytes**, SHA-256 `7b475f1b3613d87e4e5747bb98d68ac186da265518359ac819b97c19b3b8b80e`, 120×169, 8-bit / 3-component JPEG. Its metadata contains the comment `ACD Systems Digital Imaging`.
- A transient visual inspection shows a small full-colour illustrated game-art panel with multiple stylised human figures and dinosaur / prehistoric-fantasy creatures. At 120×169 there is **no reliably readable edition title, version number, publisher/operator mark or product code**.
- This is the strongest surviving **21CN-native same-stem evidence** for the `sa25up` object family and moves the recoverable provenance surface back to May 2002. It does **not** recover or authenticate `sa25up.zip`; all current archived ZIP-path records remain 404 or absent.
- The former crawl-proximity candidate `list.php?id=8831` has now been replayed and identified as Quick Heal antivirus, so it is closed as unrelated. Native record `20165` explicitly embeds both `sa25up.jpg` and `sa25up.zip`, directly resolving the sidecar-to-StoneAge-2.5 catalogue relationship.
- Canonical reports: `research/recovered/STONEAGE-SA25-21CN-JPG-R1.txt`, `research/recovered/STONEAGE-SA25-21CN-CRAWL-NEIGHBORHOOD-R1.txt`, and `research/clients/STONEAGE-SA25-21CN-SA25UP-JPG-VISUAL-R1.md`.



## StoneAge 2.5 native 21CN record 20165 resolves `sa25up.zip` identity — 2026-09-25

- **FACT:** 21CN native catalogue record `list.php?id=20165` is preserved from **2002-02-12 01:05:02 UTC** onward. The earliest replayed page is HTTP 200, 36,495 bytes, SHA-256 `962145dbcd7b8e4c7e627be3787455aa554de7f2ab4d39592255d1a4d19d5d28`, and is titled **`石器时代2.5—精灵王传说 - 下载 - 21CN.COM`**.
- The same native page explicitly identifies:
  - 软件版本：**客户端升级包**
  - 整理日期：**2002-01-31** — catalogue metadata, not an archive-capture timestamp
  - 文件大小：**8473K** in early pages; later normalized as **8.27M**
  - 软件公司：**北京华义**
  - exact ZIP: `http://download.21cn.com/file/game/maoxian/sa25up.zip`
  - exact sidecar: `http://download.21cn.com/file/game/maoxian/sa25up.jpg`
- Therefore `sa25up.zip` is no longer merely a filename hypothesis: it is directly identified by a contemporaneous 21CN native catalogue page as the **StoneAge 2.5《精灵王传说》客户端升级包**. It is **not** the documented 575/580 MB complete client package.
- The archived delivery topology later moved through `downit.php?id=20165&num=0`; a **2002-10-17** router replay explicitly references `http://images.21cn.com/download/file/game/maoxian/sa25up.zip`. Later 2004 router/pages expose additional `dg.download.21cn.com/file1_21cn/`, `file1xzm/`, `file1/` and `file1xjy/` variants.
- **OPEN / byte-provenance boundary:** the ZIP bytes themselves remain unrecovered. We still do not have its cryptographic hash, archive members, resource delta, or proof that the bytes on 21CN were byte-identical to the operator-distributed updater. Thus this resolves **package identity and expected size**, not clean-byte provenance.
- `id=22318` is a separate **564K** Beijing-Waei/华义 update for a Beijing Netcom 9 free-test server, dated by the page to 2002-07-17; it is not `sa25up.zip`.
- `id=8831`, previously identified only by crawl proximity to `sa25up.jpg`, has been replayed and is **Quick Heal antivirus**; it is closed as a false discovery candidate.
- The 21CN router/mirror recovery pass is now also bounded. The **2002-10-17** archived `downit.php?id=20165&num=0` wrapper explicitly executes `window.open("http://images.21cn.com/download/file/game/maoxian/sa25up.zip")`. Later native pages expose `file1/`, `dg.download.21cn.com/file1_21cn/`, `file1xjy/`, and `file1xzm/` generations. Seven evidence-derived exact ZIP URLs were queried in Wayback: **0 HTTP-200 ZIP captures / 0 recoverable ZIP bodies / 0 probe errors**; the `images.21cn.com` URL has only two December-2005 HTTP-404 rows. Arquivo returns 0 rows; the supplemental Common Crawl pass is partial because five tested indexes returned 504, while the successful indexes returned 0 rows.
- Therefore the 21CN updater branch is **RESOLVED FOR IDENTITY / BOUNDED FOR BYTES**. Reopen it only from a new exact mirror, archive, hash, P2P token, or preservation corpus. Highest information gain returns to provenance-preserving **full-client/physical-disc reads and contemporaneous installed-tree backups**, because those can actually move the field-map provenance anchor earlier than June 2003.
- Canonical reports:
  - `research/recovered/STONEAGE-SA25-21CN-RANKING-ID-R1.txt`
  - `research/recovered/STONEAGE-SA25-21CN-RECORD-20165-R1.txt`
  - `research/recovered/STONEAGE-SA25-21CN-DOWNIT-20165-R1.txt`
  - `research/recovered/STONEAGE-SA25-21CN-REDIRECT-HEADERS-R1.txt`
  - `research/recovered/STONEAGE-SA25-21CN-MIRROR-RECOVERY-R1.txt`
  - `research/recovered/STONEAGE-SA25-21CN-IMAGES-MIRROR-R1.txt`
  - `research/recovered/STONEAGE-SA25-21CN-JPG-R1.txt`
- Canonical source: `SRC-CN-2002-21CN-SA25-UPDATER-01`.


## StoneAge 2.5 collector-disc visual identity control — 2026-09-25

- A live Bahamut collector article by **stoneage2017 / 寂寞如風**, published **2021-01-07 10:50:13**, is now resolved as `石器時代華義國際石器周邊收藏光碟篇（二）` (`snA=81429`).
- **MODERN COLLECTOR EVIDENCE:** the article explicitly transitions to **2.5《精靈王傳說》** and states that the **upper disc is the Mainland client “统一图案” disc**, while the **lower disc is the Taiwan disc**, described as having a laser/reflective appearance. The same article separately identifies a distinctive Mainland `養羊得益包` disc and a Taiwan magazine disc, which prevents those earlier images from being conflated with the 2.5 pair.
- The 2.5 comparison panel is textually mapped by article order to the exact image URL `https://cos.stoneage.cn/uploads/article/minisnsimg/20201222/5fe128b2e6b0a.jpg`. Its image body is currently unreachable from the CI environment, so the project records the URL and body-order association but does **not** claim a recovered image hash or visual pixel match.
- The older mirror/article image family under `shiqifabu.fszye.com` was checked by exact Wayback CDX. The five relevant 2020-12-22 image URLs returned **0 archive rows**; a broader 28-image collector pass recovered **0 archived photograph bodies**. That dead-image recovery route is therefore **BOUNDED** unless a new mirror/cache/image hash appears.
- **USE:** this collector article is now a physical-carrier **visual identity control** for future exposed 2.5 discs/listings. It can help classify Mainland-vs-Taiwan artwork families and avoid mixing the 2.0 exception or `養羊得益包` disc into the 2.5 baseline.
- **EVIDENCE BOUNDARY:** collector text/image ordering does **not** establish disc filesystem contents, matrix/mastering/IFPI identifiers, manufacturing identity, original package-to-disc chain, clean-client bytes, or byte equality with any recovered specimen.
- Highest information gain therefore remains a **public provenance-preserving disc image/read or file tree**, or an independently preserved contemporaneous installed-tree backup. Do not spend additional cycles on the now-bounded dead-image URL family unless a new exact recovery token appears.
- Derived reports:
  - `research/recovered/STONEAGE-SA25-BAHAMUT-DISC-PART2-R1.txt`
  - `research/recovered/STONEAGE-SA25-BAHAMUT-DISC-IMAGES-R1.txt`
  - `research/recovered/STONEAGE-SA25-COLLECTOR-ARCHIVE-R1.txt`
- Canonical source: `SRC-CN-2021-BAHAMUT-SA25-DISC-COLLECTOR-01`.



## StoneAge 2.5 client-package carrier controls + 2013 descendant branch — 2026-09-25

- The live Bahamut collector article `snA=81400` is now structurally recovered. It explicitly documents the Mainland 2.5 client-package family as including **many different-cover new-user packages**, a **green WGS gift box** (contrasted with the orange 2.0 WGS box), and a **simplified client package**. It also places the already separately documented `延年益壽包` / `春滿乾坤包` in the same 2.5 period.
- An independent mirror at `https://www.shiqi.club/shiqi2712.html` reproduces the same package text and is itself preserved by Wayback from **2022-01-21** onward. The 2022 replay is hash-locked as SHA-256 `48874043e3621052fd81fe938dee81522f643f0d30372b12dd45b110b0be1ca6`.
- The mirror resolves **11 exact article-body package photographs** under the contiguous `202011152141*.jpg` upload family. Text/order analysis separates them into: **7 new-user-package photos**, **2 previously discussed 2.5 package examples**, **1 WGS gift-box-positioned photo**, and **1 simplified-client-package-positioned photo**. These are now exact visual-recovery targets, not guessed filenames.
- This materially improves the physical-carrier search vocabulary: future disc/ISO/file-tree claims can be checked against explicit package classes instead of treating all 2.5 media as one edition. However these modern collector sources remain **visual/package provenance only**; they do not establish package-to-disc chain, disc mastering, filesystem, installer filename, hash or clean-client bytes.
- Canonical source records: `SRC-CN-2020-BAHAMUT-SA25-CLIENT-PACKAGES-01` and `SRC-CN-2020-SHIQICLUB-SA25-CLIENT-PACKAGE-MIRROR-01`.
- Derived reports: `research/recovered/STONEAGE-SA25-BAHAMUT-CLIENT-PACKAGE-R1.txt`, `research/recovered/STONEAGE-SA25-SHIQICLUB-PACKAGE-MIRROR-R1.txt`, and `research/recovered/STONEAGE-SA25-SHIQICLUB-BODY-IMAGES-R1.txt`.
- A separate **2013 Xunlei standalone-client token** was also recovered from a surviving one-click/private-server post: client URL `http://kuai.xunlei.com/d/DX1fAAJeiQBWT-tR9ee`. Exact/prefix Wayback, Availability and Arquivo probes produced **0 payload-preservation hits**; the source itself describes paired server/client distribution and local `elize.ini` modification. Therefore this is retained only as a **descendant/private-server lineage token**, not as 2002 clean-client provenance, and it does not outrank physical-disc/full-client recovery.
- Derived Xunlei report: `research/recovered/STONEAGE-SA25-XUNLEI-CLIENT-R1.txt`.
- An **independent 2016 physical-survival control** now comes from the SMZDM collector post `此情可待成追忆：记那些年的石器时代`: its install-disc section explicitly says the author still had **2.5 / 3.0 / 4.0 / 5.0 / 疯狂原始人 installation discs**. The exact section contains six recoverable 1080×607 photographs; all six were hash-locked with 0 fetch errors. Automatic comparison against current Ruten 2.5 photographs is **not strong enough to assert same-artwork identity** (best RANSAC result: 40 inliers, ~3.96% ratio), so this source is used only as a second independent survival/visual-control chain, not as a pressing or byte-equivalence claim.
- Derived independent-disc report: `research/recovered/STONEAGE-SA25-SMZDM-DISC-R1.txt`.
- Canonical independent-disc source: `SRC-CN-2016-SMZDM-SA25-INSTALL-DISCS-01`.





## StoneAge 2.5 independent install-disc photo order resolved — 2026-09-25

- The existing SMZDM 2016 survivor source now has a generated HTML-order report. The source itself states that the author had preserved **2.5, 3.0, 4.0, 5.0 and 疯狂原始人 installation discs**, after separately describing the first pictured disc as the 2.0 new-user-package disc.
- The recovered install-disc section contains **6** image URLs. Photo 1 is tied to the 2.0 description; five later photos follow the literal version list. On that article-order basis, photo 2 — `https://am.zdmimg.com/201606/16/5762764a03643.jpg_e1080.jpg` — becomes the current **high-confidence visual candidate for the 2.5 installation disc**.
- **EVIDENCE BOUNDARY:** this is an HTML/text/order association, not disc-byte provenance. It does not establish the disc filesystem, installer filename, volume label, matrix/mastering/IFPI, clean-client status or equality with another 2.5 distribution.
- The earlier SMZDM recovery already hash-locked all six photo bodies; the new order report adds positional attribution without downloading game payloads.
- Operational consequence: use the second-photo visual identity as another exact comparison target for future public disc listings/dumps, alongside the Bahamut Mainland 2.5 unified-disc control and the 延年益壽 package specimen.
- Canonical source: `SRC-CN-2016-SMZDM-SA25-INSTALL-DISCS-01`.
- Derived order report: `research/recovered/STONEAGE-SA25-SMZDM-DISC-ORDER-R1.txt`.

## StoneAge 2.5 延年益壽包 exact surviving-disc photo locked — 2026-09-25

- A dedicated Bahamut collector article (`snA=81388`, **2020-09-01**) identifies the package as **延年益壽包**, labels a photographed object as **`2.5時期的光碟`**, and labels the following object as **`2.5版本的說明書`**.
- The first automated forum-page probe was found to be too permissive: its context window could associate an **延伸閱讀** thumbnail with the earlier disc label. That result is **superseded**. The corrected R2 probe restricts extraction to the HTML interval physically between the disc label and manual label, preferring the Bahamut creator page and using the forum page as a fallback.
- Both corrected pages resolve the same one article-body image URL: `https://truth.bahamut.com.tw/s01/202009/1eabce5c4adf3b26366bebea7d788c74.JPG`.
- The exact public photograph body is now recovered and fingerprinted: **160,151 bytes**, **1128×774**, photo SHA-256 `385071cb52f3e9af540823ff8a1833cfba4dad04ee8ab2ee9beebfa67dadea6a`, dHash `f070e0606068a1c0`.
- This aligns with contemporaneous 2.5 rollout evidence: 17173 names the early-February **春满钱坤包 / 延年益兽包** acquisition route and the 580 MB complete client upgrade, while a Sina Technology interview dated **2002-02-08** states that a limited **石器时代延年益寿包** would be issued on **2002-02-09**.
- Cross-source visual ranking now has a stronger candidate: the exact Yan-Nian disc photograph versus Ruten carrier `22632305238624` image 3 yields **112 RANSAC inliers / 0.1181 inlier ratio**. Against the independent SMZDM article-order 2.5 candidate it yields only **10 / 0.0111**. These are visual discovery metrics only; they are not proof of identical discs or bytes.
- **EVIDENCE BOUNDARY:** the SHA-256 above hashes the **photograph**, not a CD/ISO/client payload. We still lack the disc filesystem, installer filename, ISO/client hash, volume label, matrix/mastering/IFPI identity and proof of equality with the 575/580 MB complete-client distribution.
- An exact indexed-web pass combining the package/article identifiers with **ISO / 光盘镜像 / 光碟 / 客户端 / 下载** exposed no verifiable byte-bearing artifact tied to this specimen. This is bounded only for the tested surfaces.
- The literal name forms **益壽 / 益寿 / 益兽** remain separate recovery tokens.
- Operational consequence: the exact source-labelled photo is now a high-value visual identity key for any future public disc listing/read/dump. Near-duplicate or matching media should be prioritized for file-tree/hash recovery, but this **does not yet move the field-map byte-provenance anchor earlier than June 2003**.
- Canonical source: `SRC-CN-2020-BAHAMUT-SA25-YANNIAN-PHYSICAL-01`.
- Derived reports:
  - `research/recovered/STONEAGE-SA25-BAHAMUT-YANNIAN-PHYSICAL-R1.txt`
  - `research/recovered/STONEAGE-SA25-BAHAMUT-YANNIAN-DISC-PHOTO-R1.txt`.

## StoneAge 2.5 public surviving-disc set — Ruten control — 2026-09-25

- The public marketplace control set now contains **seven separately addressable StoneAge 2.5 listing IDs**, but they must not be counted as seven independently proven physical specimens:
  - `22632305238624`: boxed **2.5 精靈王傳說新手報到包**, original-package/game-disc wording, 9 full-size photos;
  - `21926883918096`: loose **2.5版 精靈王傳說** disc, listed 2019-06-28;
  - `22242541948520`: separate loose **2.5版 精靈王傳說 PC GAME** listing, listed 2022-10-19;
  - `22615474551866`: **`精靈王傳說 石器時代2.5版 遊戲片+外盒`**, listed 2026-04-11, sold quantity 1 / stock 0, with three full-size photos `_647.jpg / _438.jpg / _740.jpg`;
  - `22445165101247`: **`石器時代 2.5版 精靈王傳說 全新完整版`**, same seller account `alixson7` as `22242541948520`, one full-size photo `_815.jpg`;
  - `22637629794063`: exact **`石器時代2.5，精靈王傳說`** listing, one full-size photo `_117.jpg`, 600×800, SHA-256 `c6d6e985acadb0b9ce1e9f1aad48522b386015d57a17918e8fb8511e48570abe`;
  - `22625938678558`: literal Taiwan multi-disc collection **`臺版 石器時代 精靈王傳說 瑪蕾菲雅許願盒 家族開拓史 電腦遊戲光碟 合集（20張不分）收藏`**, seven full-size public photos.
- **Independence correction:** separate listing IDs/dates do not prove independent physical discs. The fifth listing makes this concrete: `22445165101247` and `22242541948520` use the same seller account, so they are one seller/listing lineage unless physical evidence proves otherwise.
- Updated R4 visual fingerprinting materially tightens the duplicate-family boundary:
  - `22242541948520:0` vs `22445165101247:0`: **1,581 RANSAC inliers / 0.7543**;
  - `21926883918096:0` vs `22445165101247:0`: **977 / 0.5586**;
  - `22445165101247:0` photograph SHA-256: `f7835bb1c544ee3de89578f5161f5169edc2ee1e495de0368161f8d0dfb9fc78`;
  - these values make `22445165101247` a **same-seller/near-duplicate visual control**, not a fifth independent specimen.
- The previously identified R4 visual cluster also remains:
  - `21926883918096:0` vs `22242541948520:0`: **743 RANSAC inliers / 0.4831**;
  - new disc+box `22615474551866:1` (`_438.jpg`) vs those two loose-disc images: **266 / 0.2323** and **253 / 0.2202**.
- Taken together, the high-overlap listings support a **shared disc-face/artwork/photographic family** and reduce the defensible independent-specimen count. They do not establish same physical disc, same pressing or same mastering.
- The exact source-labelled Yan-Nian disc photograph gives an important negative separator: new `22615474551866` images score only **11 / 0.0118**, **11 / 0.0120** and **7 / 0.0091** against it. By contrast the existing `22632305238624` image 3 remains the strongest Yan-Nian Ruten comparison at **112 / 0.1181**.
- Consequence: **do not merge the new disc+box/loose-disc visual cluster with the Yan-Nian source-labelled disc family.** Collector evidence says Mainland/Taiwan 2.5 disc artwork differed, but current image metrics are not enough to assign the new cluster to a region or pressing.
- Expanded seven-listing visual rerun adds two useful controls:
  - `22637629794063:0` shows only low-strength overlap with the old high-overlap family (maximum cited comparisons **25 / 0.0248** and **24 / 0.0221**), so it remains a **separate visual candidate** rather than being collapsed into that duplicate family;
  - collection image `22625938678558:3` (`_730.jpg`) matches `22445165101247:0` at **136 / 0.1339**, `22242541948520:0` at **74 / 0.0729**, and `21926883918096:0` at **37 / 0.0364**. This supports a related carrier/artwork object being present in the collection photograph, not same-disc/pressing/mastering identity.
- The expanded Ruten run resolved **23 full-size images**; all Ruten targets loaded. Provenance run **36094031445**, physical-media run **36094173065**, and visual-fingerprint run **36094173076** all completed **successfully**.
- Current Ruten/provenance reports still expose **no matrix/IFPI, volume label, filesystem, installer hash, disc image or payload checksum**. Therefore this materially improves carrier-family discrimination but **does not move the field-map byte-provenance anchor earlier than June 2003**.
- Operational next gate: a public read/dump/file tree tied to one of these exact carrier IDs/photos, or another original 2.5 disc with comparable provenance. No purchase, seller contact or user-side dump is required.
- Canonical source: `SRC-TW-2026-RUTEN-SA25-PHYSICAL-01`.
- Derived reports:
  - `research/recovered/STONEAGE-SA25-RUTEN-PROVENANCE-METADATA-R1.txt`
  - `research/recovered/STONEAGE-SA25-PHYSICAL-IMAGE-FINGERPRINTS-R4.txt`
  - `research/recovered/STONEAGE-SA25-BAHAMUT-YANNIAN-DISC-PHOTO-R1.txt`.



## StoneAge 2.5 Mainland/Taiwan source-labelled comparison image bounded — 2026-09-25

- The collector-mirror context is now mapped at **exact between-image granularity**, removing the earlier broad-context ambiguity.
- On `https://blog.shiqi.so/shiqi273.htm`, the segment between article-body image 3 and image 4 reads literally: **`到2.5精灵王传说版本啦 上面是大陆版客户端统一图案的光盘 下面是台版盘，有点镭射反光的感觉，很好看`**.
- Therefore image 4 — `https://shiqifabu.fszye.com/zb_users/upload/2020/12/20201222082537160859673711005.jpg` — is the article-order **source-labelled 2.5 Mainland/Taiwan comparison image**. The next interval is already the article closing text.
- The corresponding Bahamut collector source independently exposes `https://cos.stoneage.cn/uploads/article/minisnsimg/20201222/5fe128b2e6b0a.jpg` for the same Mainland/Taiwan 2.5 comparison context.
- Dedicated recovery run **36091418849** completed successfully, but recovered **0 image bodies**:
  - blog image direct read: connection refused;
  - blog image exact Wayback HTTP/HTTPS CDX: **0 rows**;
  - Bahamut/COS direct read: connection refused;
  - Bahamut/COS CDX requests failed transport, so that archive path remains **inconclusive**, not negative.
- R5 visual fingerprinting now rejects unqualified collector/sidebar images and retains only source-qualified body references. Since the exact source-labelled bodies remain unavailable, the current Ruten disc cluster is **not assigned to Mainland or Taiwan by visual inference**.
- **EVIDENCE BOUNDARY:** text/order association is now strong; pixel-level inspection, pressing/mastering identity, filesystem and optical-disc bytes remain unrecovered. This does not move the pre-June-2003 byte provenance anchor.
- Canonical source: `SRC-CN-2020-SHIQIBLOG-SA25-DISC-MIRROR-01`.
- Derived reports:
  - `research/recovered/STONEAGE-SA25-COLLECTOR-MIRROR-CONTEXT-R1.txt`
  - `research/recovered/STONEAGE-SA25-SOURCE-LABELLED-COMPARISON-IMAGE-R1.txt`
  - `research/recovered/STONEAGE-SA25-PHYSICAL-IMAGE-FINGERPRINTS-R4.txt`.


## Japanese 1.74a recovery gains a second exact client identity — 2026-09-25

- The Japanese bridge track now has a second exact filename/path in addition to first-party Hangame `sa174hg.exe`: a 2008 public Japanese-service repost gives `http://file2.gamania.co.jp/sa/sa174gm.exe`.
- This token has independent survival corroboration: a 2017 Japanese-player thread refers to an old-HDD client as `SA174gm` and an indexed post offers to upload `sa174gm.exe`.
- A 2020 shiqi.la preservation thread exposes an access-controlled installer archive `sa174gm[解压密码www.shiqi.la].rar` (**194.24 MB**, attachment-id **675**) and installed-tree archive `Stoneage.rar` (**174.72 MB**, attachment-id **676**). The project does not bypass its points/access controls.
- **EVIDENCE BOUNDARY:** official launch-window Hangame `sa174hg.exe` remains separately proven by first-party archived HTML. `sa174gm.exe` is a historical Gamania-hosted recovery token, but its exact build/version and original introduction date remain OPEN.
- The 2020 title's **2003-12-11** date is retained only as a later-source claim until independently confirmed.
- The suffix interpretation `hg=Hangame`, `gm=Gamania` is a working HYPOTHESIS, not a historical fact; no equality claim is permitted without recovered bytes.
- A dedicated exact-URL public-archive probe and CI workflow have been added. No client payload is committed; any public Wayback object is only transiently streamed for derived hash/size under a 400 MiB cap.
- Canonical sources:
  - `SRC-JP-2008-IPVE-SA174GM-MIRROR-01`
  - `SRC-CN-2020-SHIQILA-SA174GM-ATTACHMENT-01`.
- Canonical note: `research/clients/STONEAGE-JAPAN-SA174GM-GAMANIA-RECOVERY-R1.md`.
- This improves the Japanese bridge recovery surface but **does not supersede the project's primary 2.5 pre-June-2003 field-map provenance objective**.


- Exact/prefix public-archive pass **R2** is complete for `sa174gm.exe`: Wayback exact HTTP/HTTPS exposes only a **2013-02-10 10:10:13 UTC HTTP 503 / 399-byte HTML** object; four launch/early-era Availability anchors return no snapshot; the entire tested `file2.gamania.co.jp/sa/*` Wayback prefix returns **0 rows**; Arquivo HTTP and HTTPS both return **0 rows**; IA exact search returns **0 documents**.
- Exact/prefix HTTP-200 payload candidates are **0**. Therefore this branch improves **identity and recovery vocabulary**, not byte provenance: no `sa174gm.exe` bytes, checksum or file tree have been recovered.
- Current Gamania host DNS failure in CI is recorded only as a live-host transport fact and is not interpreted as historical loss.
- Discuz attachment-token correction: only attachment IDs **675/676** are stable; embedded token hash/time fields vary across requests and must not be recorded as permanent identifiers.
- R2 workflow run **36089113796** completed successfully; canonical derived report: `research/recovered/STONEAGE-JAPAN-174A-GAMANIA-MIRROR-R1.txt`.

## StoneAge 2.5 clean-client public-lead refresh — 2026-09-25

- The dedicated WeLoveSA **`〖2.5纯净〗石器客户端` / `tid=2132`** lead remains publicly indexed and active: **45 replies / 991 views**, latest listed reply **2026-09-16 01:02** by `mh713`. A fresh exact public-index pass still exposes no client filename, attachment ID, share ID, size or checksum. No paid/login bypass was attempted; `纯净` remains only a source title.
- CangBaoWan thread `9642` contributed exact Baidu share ID **`1a2cOmPxo5GjFPFfU5Mj2Ug`**, but direct anonymous probing now conclusively reaches a Baidu page titled **`链接不存在`**. Successful tested Wayback exact/prefix calls return 0 rows and IA exact search returns 0 docs; one timed-out archive request remains inconclusive. The direct Baidu route is therefore **bounded/dead**, while the share ID remains a repost/mirror token.
- The 2022 **246SA 石器时代2.5大屏版** share `1cHlV27B0rckWGC2cH21dGg` / code `7ck4` also now returns **`链接不存在`**. Its source explicitly describes a client+server set with de-verification changes around `gmsv`, so it is a descendant/private-server control rather than a clean-client candidate.
- A separate Judingwan distribution chain is now precisely resolved and deliberately deprioritized:
  - 2017 public source: `〖飓鼎玩〗石器时代 v2.5版`, legacy share `1eS9MzOe` / code `qnsv`;
  - later share `1nu7DLcX` / code `ylru`;
  - both published codes verify normally without login and expose the same **`石器时代v2.5一键端.exe`**, **441,183,848 bytes**, Baidu **`fs_id=146116179281676`**;
  - the later share additionally exposes **`【飓鼎玩】石器时代2.5安装教程.rar`**, **17,963,524 bytes**, `fs_id=802517119665785`;
  - the 2017 source separately lists **石器时代2.5GM工具全套**, reinforcing one-click/private-server packaging context.
- Exact filename / `fs_id` / size searches surfaced no operator-era/disc provenance or cryptographic hash for the Judingwan main EXE. It is therefore classified **DESCENDANT ONE-CLICK CONTROL**; downloading 441 MB of known descendant integration is not a current high-value use of recovery effort.
- **EVIDENCE BOUNDARY:** none of these modern share routes moves the pre-June-2003 field-map provenance anchor. The active high-value 2.5 recovery routes remain `tid=2132`, surviving physical discs, contemporaneous installed-tree backups and provenance-bearing early mirrors.
- Canonical sources:
  - `SRC-CN-2012-WELOVESA-SA25-CLEAN-TID2132-REFRESH-01`
  - `SRC-CN-2025-CANGBAOWAN-SA25-BAIDU-01`
  - `SRC-CN-2017-JUDINGWAN-SA25-ONECLICK-01`
  - `SRC-CN-2022-246SA-SA25-ONECLICK-01`
- Derived reports:
  - `research/recovered/STONEAGE-SA25-PUBLIC-CLEAN-LEADS-REFRESH-R1.txt`
  - `research/recovered/STONEAGE-SA25-CANGBAOWAN-BAIDU-R1.txt`
  - `research/recovered/STONEAGE-SA25-BAIDU-SHARE-METADATA-R1.txt`.



## StoneAge 2.5 2009→2011 descendant distribution lineage bounded — 2026-09-25

- The existing 2009 `YSA2.5.8.rar` source has now been separated cleanly from a newly recovered **2011 one-click derivative** rather than conflating the two packages.
- 2009 source `thread-16615099`:
  - client: `http://download1.92ysa.com/YSA2.5.8.rar`, about 420 MB;
  - the post describes server/login tooling in a **separate** RayFile package;
  - its publicly indexed text does not expose `SACH-MX0.30` or `sa_2903.exe`.
- 2011 source `thread-16731619`:
  - explicitly thanks `love198959` for the earlier post but says it is a newly assembled one-click installation;
  - explicitly names `石器时代WIN版服务端管理器.exe`, `SACH-MX0.30/STW0.30.exe`, and `D:/csa/gmsv/stoneage2.5/sa_2903.exe`;
  - exposes exact 115 token **`clnrsbsc`** and filename **`石器时代2.5精灵王的传说一键.zip`**.
- A contemporary reply states the extracted package lacked `GMSV.EXE` and that the user copied a 2.5 Windows server executable from another site. This is direct evidence against treating the one-click package as a clean or self-contained baseline.
- Preservation probe **36092086106** completed successfully. Successful Wayback/Arquivo/IA surfaces returned **0 payload-preservation hits**; two Wayback variants timed out and remain inconclusive.
- **EVIDENCE BOUNDARY:** the source lineage proves that the private/single-player engineering ecosystem was publicly circulating by 2009 and being rebuilt with SACH/`sa_2903.exe` by 2011. It does **not** prove byte identity with the 2009 YSA client, the recovered 2012 MediaFire bridge, or any 2002 operator client, and it does not move the pre-June-2003 field-map byte anchor.
- Operational consequence: retain `clnrsbsc` and the exact ZIP filename as lineage keys only; stop primary recovery effort on this route unless new public bytes/hash/file-tree evidence appears.
- Canonical source: `SRC-CN-2011-CANGBAOWAN-SA25-ONECLICK-115-01`.
- Derived records:
  - `research/recovered/STONEAGE-SA25-115-LINEAGE-PROBE-R1.txt`
  - `research/clients/STONEAGE-SA25-2009-2011-DESCENDANT-LINEAGE-R1.md`



## Early Taiwan/Mainland physical-carrier control set expanded — 2026-09-25

- A dedicated public Ruten early-carrier probe now preserves derived metadata for six regional/package leads and transiently hashed **25/25 full-size images with 0 errors**; no marketplace image bodies are committed.
- Taiwan listing `22625938996449` exposes a Traditional-Chinese StoneAge package with visible WGS billing-system support. Listing `22631285251243` is **not independent carrier evidence**: its first five photographs are reused/re-encoded copies of the same source set. Corresponding dHashes are identical; RANSAC gives **3,609–4,702 inliers / 0.9904–1.0000** for those five pairs, including one byte-identical image.
- The Taiwan package is **not** promoted to the accepted Taiwan Waei/JSS v1.0 Redump 104630 identity. Its public photographs have not yet yielded the baseline's exact `P-RPG-0008` or `4710739350098` identifiers.
- Mainland listing `22636573895893` exposes a photographed Simplified-Chinese WAEI/WGS StoneAge retail box. Its small back-panel identifier area was initially transcribed as **`7-900032-57-0` / `9787900032570`**, but both transcriptions fail the corresponding ISBN-10/EAN-13 checksum. If the preceding digits are correct, checksum-consistent final-digit hypotheses are **`7-900032-57-6` / `9787900032577`**. Neither pair is independently confirmed from the current photograph, so the printed identifier final digit is **OPEN**, not FACT.
- Mainland listing `22638643800877` exposes a boxed disc photograph with visible **`www.waei.com.cn`** on the disc face. It is useful Beijing-Waei carrier context but does not establish version, filesystem, mastering or byte identity.
- Preservation R1 run **36096287039 attempt 2** bounded the initial photo-transcription strings. R2 run **36097696696** then separately tested checksum-consistent hypotheses `7-900032-57-6` / `7900032576` / `9787900032577` while keeping them explicitly hypothetical. Across the eight R2 initial/hypothesis/context queries: **0 strict DiscMaster hits / 0 strict Internet Archive items / 0 errors**. Therefore the tested preservation-index surfaces are closed for both string families, while the actual printed final digit remains **OPEN**. Reopen only from a clearer photograph, independent catalogue source, new corpus or exact media/file token.
- Cross-package ORB/RANSAC similarities outside the exact Taiwan reused-photo pairs are treated only as shared StoneAge artwork/logo signal; they are **not** used to infer same carrier or region.
- Canonical source: `SRC-TW-2026-RUTEN-EARLY-REGIONAL-CARRIERS-01`.
- Canonical note: `research/clients/STONEAGE-EARLY-RUTEN-REGIONAL-CARRIERS-R1.md`.
- Derived reports:
  - `research/recovered/STONEAGE-EARLY-RUTEN-CARRIERS-R1.txt`
  - `research/recovered/STONEAGE-EARLY-RUTEN-CARRIER-FINGERPRINTS-R1.txt`
  - `research/recovered/STONEAGE-MAINLAND-RETAIL-ISBN-PROBE-R1.txt`.
- **EVIDENCE BOUNDARY:** this expands regional carrier attribution and exact search vocabulary but still does not provide a provenance-preserving disc image/file tree, matrix/IFPI, volume label, installer checksum, release-version proof or pre-June-2003 field-map bytes.


## Mainland 2.0 package visual-family bridge recovered — 2026-09-25

- The public mirror `https://www.sa85.com.cn/shiqi2710.html` is explicitly titled **`石器时代周边收藏客户端礼包篇（五）2.0版本礼盒`**. This is a later collector source, not contemporaneous operator evidence.
- Its first article-body package image (`mirror-20:2`, SHA-256 `bf736ab3ba6d860c0faece641ae8a199a35ed5e6616ddc883ad001b5301e6c6f`) strongly overlaps all four photographs from Ruten Beijing-Waei/new-user-package control `22631284715652`: **400 / 328 / 317 / 129 RANSAC inliers**, with first-three reference-image coverage **0.9070 / 0.9054 / 0.8793**.
- This is materially stronger than normal shared StoneAge logo/artwork overlap and establishes a **strong shared package/photo-artwork family** relationship. It still does **not** prove the same physical box, the same optical disc, identical installer bytes, or an independently authenticated 2.0 release identity; the strongest rows fail the homography sanity flag because of crop/embedding/perspective geometry.
- The 1.x comparison page `https://shiqi.ws/post/10248.html` was re-probed with raw HTML/CSS/escaped-URL discovery. GitHub Actions run **36097423535** completed successfully; the only additional image-like object was a **1×31** plugin background and was skipped. No usable source-labelled 1.x package photograph was recovered from the tested current page surface.
- Operational consequence: treat `22631284715652` as a **strong 2.0-labelled visual-family lead**, not a version-proven carrier. Reopen the 1.x visual-control route only from an alternate mirror, explicit article-image URL, archived body or another source-labelled 1.x package photograph.
- Canonical sources/records:
  - `SRC-CN-2020-SA85-SA20-PACKAGE-MIRROR-01`;
  - `research/clients/STONEAGE-EARLY-RUTEN-REGIONAL-CARRIERS-R1.md`;
  - `research/recovered/STONEAGE-MAINLAND-PACKAGE-MIRROR-MATCH-R1.txt`.
- **EVIDENCE BOUNDARY:** this narrows physical-package lineage only. It does not move the pre-June-2003 field-map byte-provenance anchor.



## `sa-arena` full optical false-positive eliminated — 2026-09-25

- The generic Internet Archive candidate scan had surfaced item `sa-arena` because its current catalogue title is **`疯狂原始人 Stoneage Arena Online CD-ROM 2002`** and the current creator field names 北京华义.
- A dedicated bounded optical probe now reaches the archived object itself without downloading the full disc:
  - original `CD [SA_ARENA].bin`: **721,431,312 bytes**, MD5 `f4e7b6ec2b27282d67f6b3982310cc2e`, SHA-1 `f21da5f459db55cc5e09fccadc09f00a7b115177`;
  - original `CD [SA_ARENA].cue`: **299 bytes**, one `MODE1/2352` track;
  - ISO9660 volume label **`SA_ARENA`**;
  - root includes `AUTORUN.INF`, `README.TXT`, `SAARENA.EXE` and `DIRECTX8/`.
- The preserved 22,009-byte README (SHA-256 `b4a7145830418692f73030e8b6f6561458bbe272252f23178ec538e107cdd3ab`) decodes cleanly as GB18030 and identifies the product as **`疯狂原始人`**. It gives default installation directory `C:\Program Files\Waei\疯狂原始人`, Beijing-Waei/WGS URLs and registration/charging instructions.
- The decisive product-separation line says WGS points can be used for **`《石器时代》、《大法师》、《疯狂原始人》`**. Therefore the preserved bytes themselves treat StoneAge and 疯狂原始人 as distinct WGS products. This independently agrees with the SMZDM survivor list that separately names `2.5 / 3.0 / 4.0 / 5.0 / 疯狂原始人`.
- **CLASSIFICATION:** `sa-arena` is a **same-operator / same-WGS-ecosystem negative control**, **not** a StoneAge 2.5 client candidate. It is removed from the 2.5 recovery queue; no deeper extraction of its 599,802,752-byte Wise installer is justified for the current objective.
- The current IA `date=2002-05-29` and creator fields remain **catalogue/uploader metadata**, not independently verified contemporaneous publication facts.
- Actions run **36098498332** completed successfully after the Chinese README decoder was regression-tested.
- Canonical source: `SRC-CN-IA-SA-ARENA-OPTICAL-01`.
- Canonical note: `research/clients/STONEAGE-SA-ARENA-NEGATIVE-CONTROL-R1.md`.
- Derived report: `research/recovered/STONEAGE-SA-ARENA-IA-OPTICAL-R1.txt`.
- **PROVENANCE CONSEQUENCE:** useful false-positive elimination and WGS control only; the StoneAge 2.5 pre-June-2003 field-map byte anchor is unchanged.


## 2000 full-map recovery lead — 2026-09-25

- A surviving Sina map-download page now exposes an earlier exact recovery token than the 2001-11 package:
  - record date: **2000-12-20**;
  - `aid=23223`;
  - `filename=samap_1220.zip`;
  - stated size: **1410K**;
  - encoded title parameter decodes to `石器时代！全地图`;
  - encoded author parameter decodes to `游民部落`.
- The source page is still reachable and has historical Wayback availability, but no indexed exact CGI response/payload body has yet been recovered on the tested route.
- **Major routing breakthrough:** an archived replay of the exact Sina download CGI at **2001-01-26 07:46:00 UTC** exposes the historical direct file URL `http://202.106.184.193/downfiles/map_1212/samap_1220.zip`. The archived page labels it `石器时代—全地图下载` and repeats the **1410K** size. This is now the primary recovery token; it is direct first-party routing evidence, not a synthesized path.
- The dedicated exact-route archive probe and bounded transient recovery workflow both completed successfully. Wayback availability returned **zero exact snapshots** for the direct ZIP URL across the tested 2000-12-20 through 2005-11-03 dates, and exact/prefix CDX queries likewise returned zero target rows. No ZIP bytes were recovered.
- The parent directory `http://202.106.184.193/downfiles/map_1212/` is nevertheless archived with **76 CDX rows**, proving that this download directory itself was crawled. Its rows are mostly unrelated game-map files plus later 404s; `southisland_1228.zip` appears as a 2001-06-28 **404**, while `samap_1220.zip` is absent. This bounds the exact Wayback route but leaves host-wide aliases and independent archives open.
- A bounded host-wide filename scan of `202.106.184.193/downfiles/` found **no `samap_1220` alias** across the tested 2000–2006 Wayback index. The only related rows were sibling naming/topology controls: `desktop_1212/stoneage_800_1219.zip` and two unrelated `1220`-named files under `map_1212` / `updatex_1212`, all preserved only as later **404** responses. Therefore the Sina-IP/Wayback alias surface is now bounded; sibling directory names are topology evidence only, not target-package substitutes.
- The surviving source description says to **unzip the package into the installed client's `map` subdirectory**, after which maps become fully visible in-game. This classifies the target as a field-map/cache-content distribution rather than a full client installer; the exact internal file list still requires recovered bytes.
- Attribution has been tightened: `游民部落` is a Sina game-community/editorial label on contemporaneous pages. Unlike the 2001 package, the 2000 author token contains no `xinhaonanhai` link, so a 2000→xinhaonanhai provenance claim is unsupported. The bounded xinhaonanhai archive test remains discovery-only and produced no matching contributor URL.
- Same-backend controls are now known eight days later: `northisland_1228.zip` (aid=23680) and `southisland_1228.zip` (aid=23681). The south-island CGI has a preserved 2005-11-03 HTTP 302.
- The preserved 302 has now been replayed with redirects disabled: its `Location` is **only a Sina login gateway** at `login.games.sina.com.cn/index.php?reurl=...`, with the original CGI embedded in `reurl`. It exposes no historical ZIP/file-server path, so this branch is bounded and must not be treated as payload-topology evidence.
- Independent public-archive coverage now includes the exact filename and the recovered direct IP URL. Common Crawl returned **zero target rows** across the tested indexes; Arquivo.pt text search returned zero rows where reachable, while its exact source/CGI/direct version/CDX endpoints encountered transient network-unreachable errors in the latest run. This is **no current independent-archive hit**, not proof that every Arquivo surface is permanently empty; retry only when that endpoint becomes reachable or a new mirror token appears.
- A full bounded Wayback census of the Sina `download.pl` prefix across 2000–2003 is now complete for topology purposes: 2000/2001 expose zero prefix rows on the tested index; 2002 exposes **906** rows but **zero `col=map`** rows; 2003 exposes **1,746** rows with only **3 `col=map`** rows. Replaying the bounded map sample recovered no direct binary URL. The earlier apparent direct hit was only a Macromedia Flash CAB and has been explicitly excluded/regression-tested. **Conclusion:** broad `download.pl` corpus mining does not currently expose a usable late-2000 StoneAge file-server template and should not be repeated without a new exact token or archive surface.
- Exact Internet Archive filename/stem searches expose no carrier. DiscMaster broad `samap` searches produce large unrelated result sets; the recovery probe has therefore been tightened so only an **exact leaf filename `samap_1220.zip`** (or an independently verified exact filename/stem carrier in another preservation index) can promote the result to a preservation candidate.
- **Priority consequence:** this 2000 package now precedes the 2001-11-27 `Estoneage2.0map_1127.exe` package in the field-map recovery queue. If bytes are recovered, extract/hash first and compare against Taiwan v1.0, June-2003 and mixed-2.5 corpora before making any historical-equivalence claim.
- Canonical source: `SRC-CN-2000-SINA-FULLMAP-01`.
- Derived reports:
  - `research/recovered/STONEAGE-2000-FULLMAP-PRESERVATION-R1.txt`;
  - `research/recovered/STONEAGE-2000-SINA-AID-23223-R1.txt`;
  - `research/recovered/STONEAGE-2000-INDEPENDENT-ARCHIVES-R1.txt`;
  - `research/recovered/STONEAGE-2000-SINA-MAP-NEIGHBORHOOD-R1.txt`;
  - `research/recovered/STONEAGE-2000-SINA-ARCHIVED302-R1.txt`;
  - `research/recovered/STONEAGE-2000-SINA-DIRECT-ROUTE-R1.txt`;
  - `research/recovered/STONEAGE-2000-SINA-DIRECT-RECOVERY-R1.txt`;
  - `research/recovered/STONEAGE-2000-SINA-HOSTWIDE-R1.txt`;
  - `research/recovered/STONEAGE-SINA-DOWNLOAD-CGI-TOPOLOGY-R1.txt`.

## 2001 xinhaonanhai contributor-lineage classification — 2026-09-25

- The active 2001-11-27 `Estoneage2.0map_1127.exe` target now has a tighter provenance classification. Surviving Sina StoneAge community pages show the alias `xinhaonanhai` active on the StoneAge community surface in 2002 and explicitly call it `斑竹xinhaonanhai` in November event text.
- Sina's **2002-11-08** `《石器时代4.0》最新地图补丁` independently uses the same alias as contributor (`游民部落网xinhaonanhai`) and exposes the already-known exact later package token `aid=61620` / `shiqi4updatex_02_11_08.zip`.
- **Provenance consequence:** the 2001 full-map package is now explicitly treated as a **contemporaneous community-contributed field-map/cache distribution artifact carried by Sina**, not as an operator-original client component. It remains high-value evidence for what map/cache bytes were circulating by late 2001 because the source claims `1.X，2.0通用`, but it cannot by itself prove retail/client-shipping state.
- **Recovery result:** the filtered same-contributor/two-generation carrier census R2 returned **0 relevant Internet Archive items**, **0 DiscMaster rows**, **0 strict filename rows**, and **0 errors**. The 25 broad Chinese-query IA rows were unrelated modern metadata noise and were explicitly excluded. Together with the already-bounded generic Sina/Wayback, contributor-domain, Common Crawl/Arquivo and exact-filename surfaces, this closes the currently known public carrier surface for the 2001 map target without recovering bytes.
- **Recovery consequence:** retain `Estoneage2.0map_1127.exe` / `aid=43172` as an exact reopen-on-new-token TARGET-A, but do not repeat the bounded searches. Operational priority now advances to the 2001-11-02 Sina-labelled 2.0 client `stoneage2.0setup.exe` / `aid=41967`. Shared alias/function still does not prove byte ancestry to the 2002 package.
- Derived report: `research/recovered/STONEAGE-XINHAONANHAI-CARRIER-CENSUS-R2.txt`.
- Canonical note: `research/clients/STONEAGE-2001-XINHAONANHAI-CONTRIBUTOR-LINEAGE-R1.md`.
- Canonical source: `SRC-CN-2002-SINA-XINHAONANHAI-COMMUNITY-01`.

## 2001 StoneAge 2.0 client carrier expansion — 2026-09-25

- A contemporaneous preserved `《大众软件》2001年11月B（2001年第22期）` text adds one exact carrier identity not present in the surviving 17173 2.0 upgrade page: **`《CHIP 新电脑》11月号`**. The operational carrier union for the November-2001 complete-upgrade route therefore expands from the previously recorded 13 names to **14 source-supported carrier identities**, while preserving that this is a **union of two surviving period sources**, not a single canonical “official 14-item list”.
- The same Popsoft text contains a useful packaging correction: `《晶合秘藏Ⅱ之红宝石》` carried an **upgrade version**, not the formally activated retail version. This reinforces the existing rule that recovered installer/client bytes and product activation/serial entitlement are separate provenance questions.
- Dedicated CHIP R2 preservation probing returned **0 relevant Internet Archive items, 0 relevant DiscMaster rows, 0 errors**. The available 2001-11 CHIP discs on IA are foreign editions; DiscMaster `新电脑0508.iso` is August 2005. Neither is a Mainland 2001 carrier.
- **Recovery consequence:** retain `《CHIP 新电脑》11月号` as a precise reopen-on-new-token carrier, but do not repeat the bounded IA/DiscMaster title/filename pass. The active target remains the 2001-11-02 complete-upgrade client lineage (`stoneage2.0setup.exe`, aid=41967), using remaining period carrier/filesystem evidence or a newly recovered Beijing-Waei download path.
- Canonical source: `SRC-CN-2001-POPSOFT-SA20-CARRIER-LIST-01`.
- Canonical note: `research/clients/STONEAGE-SA20-CHIP-NEWCOMPUTER-CARRIER-R1.md`.
- Derived report: `research/recovered/STONEAGE-2001-CHIP-NEWCOMPUTER-CARRIER-R2.txt`.

## Mainland 2.0 physical client-disc anchors — 2026-09-25

- The surviving 17173 2.0 product page explicitly states that both **`石器时代2.0新手报到包`** and **`石器时代2.0老手削暴包`** contained a **《石器时代2.0》客户端光盘** and lists both on the 2001-11-01 product surface. These are now exact physical-carrier classes for the active 2.0 client-recovery track.
- The 2016 SMZDM collector source maps install-disc photo 1 directly after the author's statement that the first purchased package was a **2.0 新手报到包**. Its public photograph replays byte-for-byte at SHA-256 **`98ad75b6eb5fa5aca6fa7e37095bd207779321ea4991ccf0754117cfaf3884c3`**.
- Dedicated visual R2 loaded **9/9** early Mainland controls with **0 errors**. The two strongest geometrically valid matches both come from Beijing-Waei/new-user control `22631284715652`, each at **64 RANSAC inliers** with inlier ratios **0.3902 / 0.4324** and valid quadrilateral geometry. This is a coherent shared visual-family signal but remains below the project's strong-closure threshold.
- The earlier R1 visual report is explicitly an **environment failure** caused by missing OpenCV; it carries no negative historical conclusion. R2 supersedes it for visual results.
- **Recovery consequence:** prioritize any publicly recoverable read/dump/file tree tied specifically to the **2.0 新手报到包 / 老手削暴包** carrier classes, while continuing to test whether such media can be linked to `stoneage2.0setup.exe`. Do not assume both package discs share the same pressing or installer bytes.
- Canonical product source: `SRC-CN-2001-17173-SA20-PRODUCT-01`.
- Canonical collector control: `SRC-CN-2016-SMZDM-SA25-INSTALL-DISCS-01`.
- Derived visual report: `research/recovered/STONEAGE-SA20-SMZDM-RUTEN-MATCH-R2.txt`.

## Mainland 2.0 retail-client preservation-index boundary — 2026-09-25

- The two source-supported physical client-disc classes—**2.0 新手报到包** and **2.0 老手削暴包**—plus literal `客户端光盘` wording and Sina `stoneage2.0setup.exe` were searched as a dedicated retail-media recovery surface.
- Raw R1 preservation census: **312 unique Internet Archive metadata items / 0 strict IA candidates; 0 DiscMaster rows / 0 strict DiscMaster candidates**. One broad `老手削暴包` IA response exceeded the bounded JSON body, so R1 alone was not used to close that query.
- Field-limited residual R2 then tested `老手削暴包`, full `石器时代2.0老手削暴包`, and `stoneage2.0setup` in IA title/description/identifier software fields: **0 unique items / 0 strict items / 0 errors**.
- **Recovery consequence:** the tested IA/DiscMaster exact package-name/setup-name surface is now bounded. Do not repeat it without a new identifier, collection, disc label, matrix/IFPI, mirror path or uploader token. The physical-disc identities remain historically valid targets; they are simply not recovered on these public indexes.
- The next information-gain route for the 2001-11-02 client is therefore the **period Beijing-Waei direct download topology / exact historical path**, followed by any newly surfaced physical-media identifier or independently preserved installed tree. Do not infer a Waei path from Sina server naming.
- Derived reports:
  - `research/recovered/STONEAGE-SA20-RETAIL-CARRIER-CENSUS-R1.txt`;
  - `research/recovered/STONEAGE-SA20-RETAIL-CARRIER-CENSUS-SUMMARY-R1.txt`;
  - `research/recovered/STONEAGE-SA20-RETAIL-CARRIER-RESIDUAL-R2.txt`.

## Immediate next actions

1. **The pre-2002 exact map/client targets remain chronologically highest-value but are bounded on their currently known public surfaces; the newly reconstructed 2002-11-08 StoneAge 4.0 Sina route is now also bounded without target bytes.** Preserve the following reopen-only tokens: 2000-12-20 `samap_1220.zip`, 2001-11-27 `Estoneage2.0map_1127.exe`, 2001-11-02 `stoneage2.0setup.exe`, the six exact failed Beijing-Waei Q4 pages, and 2002-11-08 `shiqi4updatex_02_11_08.zip`. For the 4.0 target, Sina's exact record is `col=updatex` / `aid=61620` / `size=3440`; archived same-category HTML proves the direct-server family `http://202.106.185.223/updatex_1024/<filename>`, and Wayback has a successful file capture in that directory on **2002-11-06**, two days before the target publication date. The synthesized exact target URL nevertheless has **0 Wayback rows**, the archived directory has **14 rows but none for the target**, five target Availability checks are zero, the strict 2002-2004 Internet Archive software-metadata pass has zero strict candidates, and exact direct-URL Arquivo.pt / bounded early Common Crawl searches expose zero indexed target rows. Therefore do **not** repeat generic Sina/Wayback/IA/DiscMaster/Arquivo/Common-Crawl scans for these targets. Reopen them only from a genuinely new mirror, cache, carrier, checksum, file-tree, directory or archived-page token. With those network routes bounded, the next highest-information field-map/provenance path is **publicly recoverable provenance-preserving data from surviving 2.5 physical discs**, followed by independently preserved contemporaneous installed-tree backups, mirror copies or server-captured caches. The project does not require the user to purchase, open, install or manually dump physical media. Continue moving the field-map provenance anchor earlier without back-projecting descendant bytes; June/December mtimes and CRC strata remain prioritization aids, not release dates.
2. **Close remaining default/runtime presentation gaps only when an implementation path actually needs them.** Exact early object-type numeric values and default NPC title/walkable/height behavior remain explicit/versioned until required.
3. **Use Taiwan 1.0 as the comparison anchor for future artifact recovery, but do not let broad archaeology block implementation.** JSS SaUpdate's HTTP topology, complete 1–9 resource selector map, launch vector, reusable token helpers, checksum rule, and the `newest.txt` line/colon structural grammar are now materially recovered from first-party bytes. The next JSS archaeology target is therefore **actual 1999 retail/beta bytes or a surviving `newest.txt` / version payload that can supply real generation values, the two historical IP control-line payloads, and any producer-side meaning of the parser-ignored fifth column**; do not repeat the already bounded official Wayback prefixes. Korean 1.74 remains a high-value provenance target. For Japanese 1.74a, continue through historical mirrors, secondary distribution evidence and physical carriers keyed by exact `sa174hg.exe` plus the **248MB** size anchor.
4. **Treat the recovered mixed 2.5 bundle strictly as a bridge/specimen and keep historical reconstruction separate from redesign.** Never repair missing references by inventing data; later optimization/automation remains an explicit DESIGN layer.


## Continuity status

- Repository: `chinaneedM/stoneage-rebuild`
- Default branch: `main`
- Visibility: public
- Authority: latest GitHub remote state is the single source of truth for project continuity.
- Canonical restart protocol: `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`

## Beijing-Waei 2.0 launch-route boundary — 2026-09-27

- Re-ran the current highest-priority 2001-11-02 client-recovery branch against the **period Beijing-Waei official web surface** rather than repeating the already bounded Sina/IA/DiscMaster exact-name searches.
- A launch-window census over the official `/ZHUANQU/stoneage2/` subtree for **2001-10-24 through 2001-11-12** recovered **465 CDX rows**, narrowed to **69 non-noise HTML candidates**, and successfully replayed **26** selected pages. Two pages carry direct 2.0 distribution/release semantics, but the successful captures expose **zero binary routes and zero `stoneage2.0setup.exe` references**:
  - `20011027113916` — `stnews/st_news_nr.asp?id=17`: an official-hosted Taiwan 2.0 release article states that the Waei game site would still provide a **2.0 update-program download**, while recommending optical-media acquisition because the program exceeded 600 MB; it names the `免费更新包`, `新手报到包` and `老手削暴包` distribution classes. This proves a Waei web-download concept, not the mainland download filename/path.
  - `20011109212146` — `stbulletin/st_bulletin_nr.asp?id=311`: a Beijing-Waei notice says 2.0 `新手报到包` / `升级版` product registration opened on **2001-10-29 09:00** and the new 2.0 servers / `老手削暴包` registration opened on **2001-11-01 09:00**. It exposes no client binary route.
- A second pass over those two semantic pages inspected normal links plus `src`, `action`, inline absolute URLs and simple JavaScript navigation. It found **no binary reference and no exact setup filename**. The only external Waei navigation roots were generic hosts such as `games.waei.com.cn` and `product.waei.com.cn`; `tyro/upgrade.asp` remains a known **level-up guide**, not a software-upgrade endpoint.
- The evidence-linked external-host census then queried `games.waei.com.cn` (**112 launch-window CDX rows**) and `product.waei.com.cn` (**22 rows**). The sole StoneAge-named row was an advertisement image, `/adv_img/other/zixun/stoneage.GIF`; there were **zero binary hits, zero strong client/download topology hits and zero exact setup hits**. The later 2002 `games.waei.com.cn/accessories/download/` executable topology therefore cannot be back-projected into November 2001.
- The high-relevance residual retry set contains seven earlier timeout/refusal targets. `stbulletin_nr.asp?id=296` replayed successfully and exposed no client binary route; the remaining **six exact targets** are still archive-access failures, not evidence of absence:
  - `stbulletin/st_bulletin_nr.asp?id=277`
  - `stnews/st_news_nr.asp?id=16`
  - `stnews/st_news_nr.asp?id=22`
  - `stnews/st_news_nr.asp?id=20`
  - `stnews/st_news_nr.asp`
  - `stbulletin/st_bulletin_nr.asp`
- **Operational consequence:** the broad Beijing-Waei Q4 page/domain search surface is now bounded. Future Waei work is limited to opportunistic replay of those six exact failed captures or a genuinely new path/carrier token. Do not repeat whole-prefix/page-domain scans. The active 2.0 client recovery branch should move to a **new physical-media/file-tree identifier**; absent such a token, advance to the **2002-11-08 4.0 map package** according to the existing priority chain.
- Derived reports:
  - `research/recovered/STONEAGE-WAEI-2001Q4-LAUNCH-WINDOW-R1.txt`
  - `research/recovered/STONEAGE-WAEI-2001Q4-SEMANTIC-PAGES-R1.txt`
  - `research/recovered/STONEAGE-WAEI-2001Q4-EXTERNAL-HOSTS-R1.txt`
  - `research/recovered/STONEAGE-WAEI-2001Q4-LAUNCH-RESIDUAL-R1.txt`


## Sina 4.0 map-package direct-route reconstruction — 2026-09-27

- The surviving Sina source page for `《石器时代4.0》最新地图补丁` remains the target authority: **2002-11-08**, **3440K**, contributor string `游民部落网xinhaonanhai`, and exact download-center parameters `col=updatex`, `aid=61620`, `filename=shiqi4updatex_02_11_08.zip`, `size=3440`.
- A new body-level replay of archived contemporaneous Sina `download.pl` pages proves that the CGI rendered **direct file-server URLs in its HTML**, rather than relying only on HTTP redirects. Four sampled `bizhi` rows independently converge on `http://202.106.185.224/bizhi_1024/<filename>`.
- Category-specific replay then recovers the historical routing split directly:
  - `col=updatex` → `http://202.106.185.223/updatex_1024/` from archived aid `15055` / `f99adidasball_629.zip`;
  - `col=demo` → `http://202.106.185.221/demo_1024/`;
  - `col=tools` → `http://202.106.185.221/tools_0327/`;
  - `col=littlegame` → `http://202.106.185.223/littlegame_1024/`;
  - `col=bizhi` → `http://202.106.185.224/bizhi_1024/`.
  These are category-specific facts; directories must not be transferred across `col` values.
- The same-category evidence permits exactly one bounded target synthesis: `http://202.106.185.223/updatex_1024/shiqi4updatex_02_11_08.zip`. The base is not merely a later inference: Wayback's directory census contains a successful `200` capture of `kjking2002102520.EXE` under `updatex_1024` at **2002-11-06 20:05:48**, establishing that this file-server directory was active before the StoneAge target's 2002-11-08 publication.
- The target itself remains unrecovered:
  - exact Wayback CDX on the synthesized URL: **0 rows**;
  - `updatex_1024/` prefix: **14 archived rows**, **0 target rows**;
  - Wayback Availability checks at 2002-11-08, 11-09, 11-16, 12-01 and 2003-01-01: **0 target captures**;
  - bounded 2002-2004 Internet Archive software-metadata search for the exact filename/stem, StoneAge 4.0 title variants, `新九大家族`, `新满意足/新滿意足`, `新高采烈` and `xinhaonanhai`: **0 strict StoneAge candidates**;
  - Arquivo.pt exact direct URL and explicit-`:80` variant: **0 rows**;
  - six bounded early Common Crawl indexes: **0 rows** on successful queries; four requests returned 502/504 and are availability failures, not negative evidence.
- A broader 2002 `col=updatex` timeline probe completed H1/Q3 with zero filename-bearing rows but suffered a Q4 archive refusal. It does not weaken the stronger Q4 category replay and direct-directory evidence above.
- **Operational consequence:** the 4.0 Sina network-recovery branch is now bounded at a substantially stronger level than filename-only search: the historical delivery family and pre-target directory existence are reconstructed, but no public target bytes survive on the tested indexes. Reopen only from a new independent mirror/cache/carrier or exact directory/file token. The field-map recovery priority therefore returns to provenance-bearing 2.5 physical-media / installed-tree / mirror-cache evidence while preserving the earlier 2000/2001 exact targets for immediate reopening when new tokens appear.
- Derived reports:
  - `research/recovered/STONEAGE-SA40-SINA-NEIGHBOR-BODY-R1.txt`
  - `research/recovered/STONEAGE-SA40-SINA-CATEGORY-ROUTES-R1.txt`
  - `research/recovered/STONEAGE-SA40-SINA-SYNTHESIZED-ROUTE-R1.txt`
  - `research/recovered/STONEAGE-SA40-SINA-UPDATEX-TIMELINE-R1.txt`
  - `research/recovered/STONEAGE-SA40-STRICT-IA-R1.txt`
  - `research/recovered/STONEAGE-SA40-DIRECT-ARCHIVE-R1.txt`

## Blockers

No repository or workflow blocker.

The project still lacks a provenance-preserving **publicly obtainable** 1999 JSS retail disc image/dump and September 1999 beta binary. The Korean **Inium/Hananet/CNET 2000–2001** recovery track now has CNET's exact payload path/name (`/pc/games/online/stoneage.zip`, 257MB) and Hananet's exact full/trial mappings (`8119` / 260 M / `sa.exe`; `8120` / 240 M / `sa_demo.exe`), but still lacks recoverable client bytes, hashes/file tree, and byte-level equivalence evidence between the independently packaged mirrors. Korean `1.74` and the Japanese `1.74a` **game payload bytes** likewise remain unrecovered, so neither bridge target has yet established byte-level relationship to JSS. The Japanese launch-time Hangame installation/download chain itself is no longer unknown: official `sasetup.asp` / `sasetup2.asp` / `sadl.asp` snapshots and the small `HgSA.cab` control lineage are recovered, and the 2003-12-14 official download page directly identifies the client URL `http://hangame.gamania.co.jp/stoneage/sa174hg.exe` with a derived launch-page package-size anchor of **248MB**. LIFESTORM II and StoneAge JANs are directly resolved from public package photographs, and the Japanese StoneAge package identity is now anchored by JAN `4988609011565` plus model `WR-04156`. The remaining physical-carrier blocker is the **two individual disc identities, matrix/mastering/IFPI identifiers and recoverable disc images/file trees**. The current Redump Japan-PC index has no title/model/barcode hit for this package, and DiscMaster likewise has no exact indexed `WR-04156` or `4988609011565` content hit; the 13 Mercari originals remain HTTP-403-blocked here. The beta web-recovery blocker remains a nearly complete application-page path; the Retromags No.015 object is identified down to filename, size, MD5 and seedbox target, but the scan body is still unreachable. The archived JSS replacement `stoneage.exe` is now byte-recoverable through the CI environment and has been transiently analyzed, removing the old launcher-byte blocker. The remaining JSS blocker is earlier provenance: the project still lacks the **1999 retail/beta client bytes** and the `newest.txt` / version-payload archive surface; the launcher-derived 1999–2002 Wayback CDX exact/prefix probe returns zero index rows. The developer-lineage track now has a named, independently cross-checked JSS/StoneAge staff lead in Yuki Tamura, but the original StoneAge credit list and exact staff-role mapping remain unresolved. The recovered JSS launcher now confirms `updated` and the `sa_%d.exe` / `sa_*.exe` generation pattern as first-party strings. Exact `sa.exe` and `CheckForUpdate` remain descendant-derived search traits until original JSS material confirms them independently. The missing 1999 JSS and Korean operator binaries remain lineage/recovery constraints, but they no longer block technical reverse engineering: the accepted Taiwan Waei/JSS v1.0 retail disc now provides a provenance-preserving early client baseline.

## Stoneage-5 preserved optical / battle-lineage milestone — 2026-09-25

- Recovered and boundedly inspected Internet Archive item Stoneage-5 without downloading the full 733,057,248-byte BIN or committing proprietary payloads. CD [STA5].bin is MD5 61a8b9f2e7db18c3e3e95c6c12e3674b, SHA1 6053dce3df2723250ddb52a98b3e8cf2552cd791; ISO9660 volume label STA5.
- Byte-derived installer identity is concrete: STA5.MSI is SHA-256 0ed62503861d4fc3f715c060402d101150020d54e5d294af40a8412232ba4f63, ProductName=石器时代宠物进化史, ProductVersion=5.00.0000, Manufacturer=北京华义联合软件开发有限公司, install root Program Files\Waei\stoneage5.0.
- The MSI declares 413 files. Core generations are real_31.bin / adrn_31.bin and spr_17.bin / spradrn_17.bin; battle data uses battle_2.bin plus battletxt_2.txt. It declares 220 destination battle000..219.sab files and 16 palette SAP files. No client field-cache .DAT or single-layer .MAP files appear in the MSI File table.
- DATA1.CAB is 612,584,670 bytes, CAB v1.3, with 26 LZX folders / 413 cabinet files. Only directory metadata plus an 8 MiB prefix were read; selected early files were extracted transiently and deleted by CI.
- Direct byte-lineage closure: 5.0 battle_2.bin is 187,500 bytes, SHA-256 1046a66cbf34088a15f99146263f166be68991c9e01b48dcbbc81d82d1569642. Its first 185,892 bytes exactly equal the accepted Taiwan 1.0 battle_1.bin SHA-256 d99be6475982cf6098b90ff5dfd81ab275ec8c9271fa83daceb95e3fd4bb8859. The remaining 1,608 bytes are exactly two 804-byte records.
- The text index independently matches: 5.0 battletxt_2.txt is 5,844 bytes and its first 5,792 bytes exactly equal Taiwan 1.0 battletxt_1.txt; the appended rows are battle218.sab and battle219.sab. The resulting table is 235 contiguous entries ending exactly at byte 187,500.
- Embedded file times show cross-generation packaging: battle_2.bin / battletxt_2.txt carry 2001-06-25 DOS timestamps; real_31.bin / adrn_31.bin carry 2002-12-25; sa_5000.exe is 2002-12-26; root INSTALL.EXE PE timestamp is 2002-12-27 02:21:08 UTC. These are internal artifact timestamps, not independent release-date proof.
- Independent contemporaneous publication closes the broad distribution date separately: 17173 on 2003-01-16 states 石器时代5.0:宠物进化史 was newly on sale and the starter pack included a 完整版客户端; Sina's 2003-04-03 download hub explicitly lists 石器时代5.0客户端下载. This proves Mainland 5.0 public distribution before June 2003, but does not by itself prove this exact archived BIN is the same pressing sold on either date.
- Archaeology consequence: the v1.0 -> Mainland 5.0 battle-map container lineage is now proven at exact-byte level, while the higher-priority pre-June-2003 field-map DAT/MAP byte anchor remains OPEN. Because the 5.0 installer contains no DAT/MAP field cache, the next highest-information route remains the contemporaneous separate map package / installed-cache / physical-media path.
- Derived evidence: research/recovered/STONEAGE-STONEAGE5-IA-OPTICAL-R1.txt, STONEAGE-STONEAGE5-MSI-INVENTORY-R1.txt, STONEAGE-STONEAGE5-CAB-DIRECTORY-R1.txt, and STONEAGE-STONEAGE5-BATTLE-LINEAGE-R1.txt.

## Historical Jun10 field-map corpus refinement — 2026-09-25

- Replayed the already identified Wayback capture of `http://www.wuxitianlong.com/sa/map.exe` at `20030623234451` through a bounded/full transient recovery. The archived HTTP response reports original length **4,223,728 bytes** and `X-Archive-Orig-Last-Modified: Tue, 10 Jun 2003 10:01:06 GMT`; recovered SHA-256 remains **372426e46765a1cf479041bdafc1d3e58fb019117d00d0b43d6a5f796620776e**.
- The executable is a PE32 / UPX / RAR self-extracting package. The RAR starts at offset 23,040 and contains one `map/` directory plus **1,011 DAT files**: **1,008 numeric DATs + BGM0/BGM1/BGM2**. Under the strict three-plane parser this is **995 valid normal DATs + 16 special/invalid entries**.
- Whole-file comparison against the recovered mixed-2.5 `stoneage2.5/map` directory finds **1,011/1,011 same names, zero one-sided files, 995 exact whole-file SHA-256 matches, 16 differences**. In the prior numeric-only accounting this is the already known **993 exact / 15 changed** across 1,008 numeric IDs; adding the three BGM files contributes exact BGM0/BGM2 and differing BGM1.
- Of the 16 differences, **15 are normal three-layer DATs and one is 2-byte BGM1.DAT**. Across the 15 normal differences: tile changes total **11,500 cells**, parts changes **678**, raw event changes **4,593**. Only **5 event cells change in low-12 event payload** while **4,588 change only in high read/see-flag state**. This strongly corroborates runtime-cache mutation for much of the event-layer divergence without erasing genuine static-map changes in the 15 files.
- Two prior risk controls are now materially reclassified:
  - `1021.DAT` is **byte-identical** in both corpora, SHA-256 **92abd0a38c5e876d985c33437a252358d1aaa812ce1da99f18752d0a97c81197** (407×144). Its 43,952 non-enum low-12 event cells therefore pre-exist the later mixed-bundle preservation state; later private-server/runtime mutation inside that bundle is no longer a viable primary explanation.
  - `817.dat` is **byte-identical**, SHA-256 **ca29cdf04f9f750712ef9afffe14aebfd571a0c6011eac2c7eff67dfde8cc380** (400×600). Its unresolved graphic-ID concentration against `adrn_15.bin` is therefore a **map/resource-generation mismatch**, not evidence that this DAT was introduced or modified only in the mixed bundle.
- **Evidence boundary:** the Wayback observation is 2003-06-23; the preserved origin `Last-Modified` is 2003-06-10. Neither can prove that identical bytes were served from the same URL on the 2003-04-03 5.0 download page. The highest-priority **pre-June-2003 field-map byte anchor remains OPEN**; the exact 2002-11-08 4.0 map package / earlier installed-cache / physical-media path remains the next target.
- New derived reports:
  - `research/recovered/STONEAGE-HISTORICAL-MAPEXE-WAYBACK-R1.txt`
  - `research/recovered/STONEAGE-HISTORICAL-MAPEXE-INVENTORY-R1.txt`
  - `research/recovered/STONEAGE-HISTORICAL-MAPEXE-SA25-LINEAGE-R1.txt`
  - `research/recovered/STONEAGE-HISTORICAL-MAPEXE-SA25-LAYER-DIFF-R1.txt`

## 2001 field-map / client recovery priority correction — 2026-09-25

- A surviving contemporaneous Sina download record moves the earliest concrete field-map recovery target substantially earlier than the previously prioritized 2002-11-08 4.0 package.
- **2001-11-27 full-map target:** Sina record `《石器时代》全地图`, stated size **1911K**, contributor `xinhaonanhai`, with explicit instructions to unpack into the `\stoneage` directory and the compatibility statement **“1.X，2.0通用”**.
  - exact Sina download token: `col=map`, `aid=43172`, `filename=Estoneage2.0map_1127.exe`, `size=1911`;
  - surviving source page and exact CGI parameter set are recovered;
  - current Wayback exact/predicted-path queries, Internet Archive item search and DiscMaster filename searches expose **no exact payload carrier yet**;
  - the contributor domain `xinhaonanhai.com` has Wayback root captures at **2001-12-03** and **2002-07-19**, but the currently indexed/replayed surface exposes no package URL.
  - For the 2001 map target, the recovered Sina host-alias census finds **56 `col=map` rows** on `games.sina.com.cn` in 2001 but no exact aid/filename row. Small replays of the nearest usable records recover the older direct map topology `http://202.106.184.193/downfiles/map_1212/`; substituting `Estoneage2.0map_1127.exe` into that directory yields **zero CDX rows**. Therefore `map_1212` is only an early-2001 topology control, not the proven 2001-11 target route.
  - A bounded live numeric-neighborhood scan around source page `11271899.shtml` checked **73 page IDs** and found only five map records: the target plus four immediately preceding Delta Force map packages (`aid=43124/43127/43129/43130`, filenames ending `_1119.zip`). A dedicated dual-host Wayback prefix replay then found **zero archived CGI rows for all four sibling tokens** on both `games1.sina.com.cn` and `games.sina.com.cn`. Consequently the same-page batch is useful as a bounded control but does **not** recover a late-November-2001 binary host/directory template.
  - The three non-strict DiscMaster rows previously returned by the broad query `estoneage` are now fully classified as unrelated false positives: one `Chapter2-TheStoneAge.mid` inside an RPG Maker resource disc and two `QueensOfTheStoneAge.jpg` files inside PlayStation 2 artwork discs. Exact `Estoneage2.0map` / `Estoneage2.0map_1127` queries remain zero. This DiscMaster naming branch is closed unless a new exact file/carrier token appears.
- **2001-11-02 client target:** Sina separately records `石器时代2.0客户端`, stated size **524377K**, described as an upgrade client for existing StoneAge users.
  - exact Sina token: `col=demo`, `aid=41967`, `filename=stoneage2.0setup.exe`, `size=524377`;
  - current exact Wayback / IA / DiscMaster probes expose no verified payload carrier.
  - For the 2001 client target, a dual-host `col=demo` neighborhood probe replays one archived neighbor (`monkeybrain.exe`, aid=25443) to `http://202.108.44.24/demo_1118/monkeybrain.exe`. Substituting `stoneage2.0setup.exe` into that directory yields **zero CDX rows**. This establishes a historical Sina demo-server family only; it does not establish the StoneAge 2.0 installer path.
  - A preserved 17173 2.0 upgrade guide independently expands the client-recovery surface: it states that the **完整升级版** was downloadable from Beijing Waei and was also distributed free with **13 named November-2001 magazine/book/disc carriers**; a contemporaneous preserved Popsoft November-B issue independently adds **《CHIP 新电脑》11月号**, bringing the cross-source carrier union to **14 identities** (`PC任我行`, `大众软件CD`, `电脑`, `电脑爱好者—玩游戏`, `电脑报—游戏世界`, `电脑校园`, `晶合秘藏Ⅱ之红宝石`, `少年电世界`, `网上俱乐部—游戏吧`, `新游戏人`, `游戏原动力`, plus two StoneAge guide-book discs). This is now a concrete carrier route independent of the missing Sina payload.
  - Carrier census R1 produced 86 noisy IA full-text rows and zero DiscMaster rows; R2 restricted IA to title/software metadata and found **no direct 2001-11 carrier** and zero global `石器时代2.0` / `StoneAge 2.0` software item. `大众软件CD` exposed an authentic preserved **Popsoft CD identifier family**, but direct namespace enumeration now closes that lead: only **20 `popsoftcd-*` items** exist on the tested IA namespace, spanning **1996–1998** (1 in 1996, 5 in 1997, 14 in 1998). Exact metadata requests for `popsoftcd-2001-11` plus five plausible suffix variants all return empty objects. Reopen this route only from a new 2001 Popsoft identifier/uploader/collection token, not by further identifier guessing.
- **Priority consequence:** the 2000-12-20 `samap_1220.zip` target remains chronologically first. Once its currently known Sina/Wayback surfaces are bounded, `Estoneage2.0map_1127.exe` is the next highest-information executable field-map target because its contemporaneous page explicitly brackets the package to the **1.X / 2.0** client family. The 2002-11-08 `shiqi4updatex_02_11_08.zip` target remains valuable but is later.
- **Evidence boundary:** the Sina record proves that this named package was advertised/distributed on 2001-11-27 with a 1.X/2.0 compatibility claim. It does not by itself prove the contents are operator-original, unchanged, or identical to Taiwan v1.0 caches. The executable must be recovered and its extracted DAT bytes compared before any field-map provenance gate can be closed.
- Derived reports:
  - `research/recovered/STONEAGE-2001-FULLMAP-PRESERVATION-R1.txt`
  - `research/recovered/STONEAGE-2001-CLIENT-PRESERVATION-R1.txt`
  - `research/recovered/STONEAGE-XINHAONANHAI-ARCHIVE-R1.txt`
  - `research/recovered/STONEAGE-2001-SINA-HOST-ALIAS-R1.txt`
  - `research/recovered/STONEAGE-2001-SINA-MAP-TOPOLOGY-R1.txt`
  - `research/recovered/STONEAGE-2001-SINA-CLIENT-TOPOLOGY-R1.txt`
  - `research/recovered/STONEAGE-2001-SINA-SAMEBATCH-R1.txt`
  - `research/recovered/STONEAGE-2001-SINA-SAMEBATCH-ROUTE-R1.txt`
  - `research/recovered/STONEAGE-2001-DISCMASTER-ESTONEAGE-R1.txt`
  - `research/recovered/STONEAGE-2001-SA20-COVERDISC-CENSUS-R1.txt`
  - `research/recovered/STONEAGE-2001-SA20-COVERDISC-CENSUS-R2.txt`
  - `research/recovered/STONEAGE-2001-POPSOFT-PRESERVATION-R1.txt`


## StoneAge 2.5 Popsoft February-2002 carrier residual bounded — 2026-09-27

- The contemporaneous 17173 upgrade guide names **`《大众软件CD——大众游戏》2002年2月号`** as one of the physical distribution channels for the 2.5 complete package/updater. A dedicated residual probe now expands the Internet Archive surfaces that the earlier broad carrier census left unresolved.
- The single IA software item returned by broad `"大众软件" AND year:2002` metadata search is **not a target**: `start-modem-5600d` is a Fujian Start/实达 5600D modem driver disc. Its `START_MODEM.iso` is therefore an unrelated lexical/description collision and is explicitly blocked from promotion.
- The genuine Popsoft preservation family `popsoft-magazine_202403` contains original scans for **2002年02月A** and **2002年02月B**. Current IA metadata exposes **6,809 files / 990 originals / 0 optical images**, with 26 February-2002 A/B files.
- Transient OCR-only inspection finds **5** StoneAge-2.5/Spirit-King proximity hits in the February-A scan and **0** in February-B under the same detector. This corroborates surviving 2.5-period editorial content, but **does not prove which issue or physical disc carried the client**.
- Operational conclusion: this route is **SCAN-ONLY / OPTICAL-RESIDUAL-BOUNDED**. Do not treat magazine PDF/EPUB/OCR files as cover-disc evidence. Reopen only from a new exact optical identifier, disc photograph/label, ISO/BIN/CUE/file tree, checksum, torrent/archive member list or independent mirror.
- Separately, the surviving contemporaneous 17173 2.5 product page still exposes exact new-user-package visual asset names **`sa03.gif`**, **`st25_new_02.jpg`**, and **`st25_new_03.jpg`** in the three-package-variant block. Retain these as visual/package-search tokens only; they are not disc filenames or client payload identities.
- New derived evidence:
  - `research/recovered/STONEAGE-SA25-POPSOFT-2002-RESIDUAL-R1.txt`;
  - `research/clients/STONEAGE-SA25-POPSOFT-2002-CARRIER-BOUNDARY-R1.md`.


## StoneAge 2.5 `中学生电脑 2002攻略特刊` institutional-catalogue lead — 2026-09-27

- After bounding the Popsoft scan-only route, a new independent carrier-resolution lead was found for another exact contemporaneous 2.5 distribution identity: **`《中学生电脑》2002年攻略特刊`**.
- Public search indexing of a catalogue PDF on the official 湖南石油化工职业技术学院 domain exposes at least five records titled `中学生电脑`, publisher `课堂内外杂志社出版`, under exact call-number tokens **`TP3-794/12.2`**, **`.3`**, **`.5`**, **`.12`**, and **`.14`**.
- This is **OPEN / catalogue-level only**. The indexed rows do not expose year/issue mapping, and the source PDF was not replayable in the current web environment. None of the five holdings may be identified as the 2002攻略特刊 or StoneAge carrier without another metadata join.
- Priority consequence: resolve the `TP3-794/12.*` sequence through public institutional catalogue/OPAC/export metadata. If a call number maps to the 2002攻略特刊, use that exact catalogue identity to reopen optical-preservation searches. No purchase/manual acquisition is required.
- Canonical note: `research/clients/STONEAGE-SA25-ZHONGXUESHENGDIANNAO-LIBRARY-LEAD-R1.md`.


## StoneAge 2.5 institutional-call-number correction and old-disc directory closure — 2026-09-27

- The 湖南石油化工职业技术学院 catalogue route has been corrected: multiple `中学生电脑` / `课堂内外杂志社出版` electronic-media rows exist under `TP3-794/12.*`, but their publication-date field is blank. Observed suffixes include at least **.2/.3/.5/.8/.9/.10/.12/.13/.14**.
- **Do not interpret those suffixes as months or issue numbers.** A neighboring record in the same electronic-media class, `TP3-794/20.14`, is explicitly `《电脑迷》2009年第7月号下配刊光盘` with date `2009.7`; therefore a trailing `.14` is a local holding/item sequence, not a direct calendar encoding.
- The institutional holdings remain an OPEN catalogue lead because no public row currently binds a `TP3-794/12.*` item to **`《中学生电脑》2002年攻略特刊`**.
- The live public 老光盘群 Directory Lister route is now fully bounded at path/filename level: **29 roots / 5,173 pages / 97,708 links / 38,826 file links / 0 target-name matches / 0 errors / 0 remaining frontier**. No file body was downloaded.
- Operational consequence: stop rescanning this current Directory-Lister tree and stop trying to decode the school call-number suffix. Reopen only from a new exact accession/issue token, readable disc/package photo, optical image/file tree/checksum, torrent member, preservation catalogue or mirror.
- Canonical note: `research/clients/STONEAGE-SA25-ZHONGXUESHENGDIANNAO-LIBRARY-LEAD-R1.md`.
- Derived report: `research/recovered/STONEAGE-SA25-OLD-DISC-DIRECTORY-R1.txt`.


## StoneAge 2.5 Wanfang disc carrier-provenance refinement — 2026-09-27

- The exact photographed Wanfang disc remains **OPEN / UNCLASSIFIED-CARRIER**: `永远的石器时代 2.5 精灵王传说`, 万方数据电子出版社, ISBN `7-900096-07-8/Z.03`, barcode `9787900096074`.
- New publisher-family evidence: a 2005 新闻出版总署 enforcement list records 万方数据电子出版社 on game/electronic publication `战神3000`, ISBN **`7-900096-34-5`**. This proves Wanfang used the `7-900096-*` range for game/electronic publications but does not identify `07-8`.
- A current second-hand index also exposes a seller-generated Wanfang title string for a `石器时代3.0攻略宝典...` item. Treat this only as a **search lead** suggesting a Wanfang StoneAge guide/publication line; it is not period bibliographic proof.
- More importantly, a contemporaneous 2003 Beijing-Waei warning about a different StoneAge 5.0 guide product states that its bundled client CD was a **network-download version and not an official Waei product disc**. This closes a methodological ambiguity: **payload content and physical-carrier provenance must be graded independently**.
- Exact public-web searches for the Wanfang 2.5 ISBN/barcode/title recovered no independent exact bibliographic/CIP record in this pass. The bibliographic route remains OPEN, not disproven.
- Operational consequence: the secondary-publication/guide hypothesis is now higher-value, but not promoted to fact. Next decisive evidence is an exact catalogue/CIP record, a package/book-to-disc photo chain, or a read-only optical image/file tree with hashes.
- Canonical analysis: `research/clients/STONEAGE-SA25-WANFANG-DISC-R1.md`.
- New source controls: `SRC-CN-2003-WAEI-SECONDARY-GUIDE-CLIENT-CD-WARNING-01` and `SRC-CN-2005-GAPP-WANFANG-GAME-PUBLICATION-01`.



## Early Mainland official physical-carrier priority upgrade — 2026-09-27

- A new high-information recovery branch is now registered for the **2001-01-10 Mainland launch carrier**.
- Contemporaneous Sina identifies the chain as **JSS production -> Beijing Waei authorization -> Zhiguan Electronics (Beijing) agency -> 广西金海湾电子音像出版社 publication/distribution**, and explicitly states that the Mainland release used **four different package variants**.
- A 2002 Peking University paper independently corroborates the **2001-01-10** Guangxi-Jinhaiwan publication relationship and separates Zhiguan technical-support / Waei sales-service roles.
- Current public JD indexes expose surviving second-hand title strings `石器时代网络游戏 广西金海湾电子音像出版社` and `STONEAGE 石器时代 北京华义联合软件开发有限公司 广西金海湾电子音像...`. These are **modern survival leads only**, not authenticated first-pressing evidence.
- Priority consequence: this route now **outranks the Wanfang 2.5 carrier for early-client recovery**, because an authenticated public Guangxi-Jinhaiwan optical object would be tied to the initial Mainland official publication chain and could materially move the Mainland client/map/resource provenance anchor earlier.
- Immediate target: recover a public package-back/disc-face image, exact ISBN/ISRC/catalogue number, or read-only ISO/file tree. Do not purchase or ask the user to acquire an object.
- Canonical analysis: `research/clients/STONEAGE-2001-MAINLAND-LAUNCH-PHYSICAL-R1.md`.
- Source records: `SRC-CN-2001-SINA-STONEAGE-MAINLAND-LAUNCH-01`, `SRC-CN-2002-PKU-STONEAGE-MAINLAND-DISTRIBUTION-01`, `SRC-CN-2026-JD-STONEAGE-JINHAIWAN-SURVIVAL-LEAD-01`.



## Early Mainland client-disc photographs recovered; exact preservation index bounded — 2026-09-27

- The exact Guangxi-Jinhaiwan preservation-index probe completed successfully: **5 source-derived query identities / 0 strict IA items / 0 strict DiscMaster hits / 0 interesting media files / 0 errors**. The tested generic publisher-title index route is now BOUNDED.
- A substantially stronger public physical-survival source was then recovered: the 2016 SHIQI.ME first-person preservation page `pt_51.htm` directly photographs retained **1.x/1.82, 2.0 and 2.5 client discs**.
- The author labels the first disc as a **`石器时代1.82的客户端`**. Its photograph visibly carries **北京华义联合软件开发有限公司** and **广西金海湾电子音像出版社** text and a physical serial-label sticker. This is now the project's strongest direct visual lead for an early Mainland Waei/Jinhaiwan client carrier, though it is still later-photo evidence rather than byte provenance.
- The same page labels the second disc as a **2.0 client** and states it was obtained with an **老手削暴包**; the disc face reads `石器时代2.0 家族开拓史`. This independently coheres with the contemporaneous 17173 product record that the old-user pack contained a 2.0 client disc.
- The third disc face reads **`石器时代2.5 精灵王传说`** and carries Waei/operator branding. This provides a concrete Mainland client-disc visual control against the separately photographed Wanfang disc.
- **Wanfang classification refinement:** the Wanfang `7-900096-07-8/Z.03` disc and the Waei-branded 2.5 client disc are now proven to be **different physical printed-carrier identities/artworks**. This does not prove different payload bytes, but it materially strengthens the Wanfang disc's classification as a secondary/publisher-bundle candidate rather than the same official client pressing.
- Priority consequence: stop repeating generic `石器时代 + 广西金海湾` preservation searches. Highest-information next step is to recover a **higher-resolution 1.x/1.82 disc/package-back image** yielding an exact ISBN/ISRC/catalogue number, or a public optical image/file tree keyed from that artifact.
- New source records: `SRC-CN-2016-SHIQIME-MAINLAND-CLIENT-DISCS-01`, `SRC-CN-2016-SHIQIME-WANFANG-SA25-DISC-01`.
- Derived report: `research/recovered/STONEAGE-2001-MAINLAND-JINHAIWAN-PRESERVATION-R1.txt`.



## Early Mainland disc publication-number refinement — 2026-09-27

- The same early Mainland Waei/Jinhaiwan client-disc photograph has a clearer Sohu mirror. Its small publication-number line can now be **provisionally transcribed** as **`ISBN 7-900323-57-0/TP·026`**.
- The transcription is deliberately split into confidence layers:
  - **FACT / independently corroborated:** 中国音乐著作权协会's electronic-publication publisher-code table assigns **`ISBN 7-900323` to 金海湾电子音像出版社**;
  - **PROVISIONAL VISUAL TRANSCRIPTION:** the photographed item suffix **`57-0/TP·026`** still lacks an independent bibliographic/catalogue record.
- Internal consistency is strong but not dispositive: `7-900323-57-0` passes ISBN-10 Mod-11, and the corresponding `978-7-900323-57-6` passes ISBN-13 checksum validation.
- The corrected exact-token probe now includes **`TP026`** rather than the earlier conservative `P026` placeholder and completed with **7 query identities / 0 strict IA items / 0 strict DiscMaster hits / 0 errors**. The current exact preservation-index route is therefore BOUNDED for this provisional identifier.
- A separate 2020 specialist collector index describes the `1.82时期的客户端新手礼包` as containing the CDK on the manual back plus **one installation disc**, and references **four common package variants**. This is consistent with contemporaneous Sina's statement that the Mainland launch used four package designs, but exact one-to-one identity between those two sets remains OPEN.
- Operational consequence: stop guessing further ISBN suffixes. Highest-value evidence is now an **independent catalogue/CIP record or higher-resolution package/disc image** that confirms or rejects `57-0/TP·026`. Until then, keep the whole number as a search token only.
- New source records:
  - `SRC-CN-2020-SOHU-EARLY-MAINLAND-DISC-MIRROR-01`;
  - `SRC-CN-MCSC-JINHAIWAN-ISBN-PREFIX-01`;
  - `SRC-CN-2020-SHIQISO-SA182-NEWBIE-PACK-01`.
- Derived evidence: `research/recovered/STONEAGE-EARLY-MAINLAND-PROVISIONAL-ISBN-R1.txt`.



## Early Mainland 1.82 package/disc family narrowed — 2026-09-27

- A later physical-media collector provides a useful **same-collection control** for the current Mainland carrier hunt.
- In a 2020 1.82 package post, the collector shows four common new-user package-front variants and states that **their backs are identical**; the package composition is described as CDK on the manual back plus one installation disc. A separate `上网包` variant is distinguished.
- In a 2021 optical-media inventory, the same collector describes the familiar Beijing-Waei 1.82 client disc as the **standard/unified disc across ordinary Mainland package variants**, while separately identifying a less-common `上网包` disc.
- This does **not** prove byte identity, January-2001 first-press identity, or that the collector's four packages are exactly Sina's four launch designs. Because both posts come from the same collector, they are not independent corroboration of each other.
- Search consequence: a readable **package back from any of the four ordinary 1.82 packages** is now a high-value target because it may expose the shared template/publication identity; keep the `上网包` as a separate carrier branch.
- A fresh public-web pass over the exact provisional ISBN-10/ISBN-13/`TP026` tokens still exposed **no independent StoneAge bibliographic/CIP record** in this pass, so the full `7-900323-57-0/TP·026` remains provisional.
- New source records:
  - `SRC-CN-2020-GAMER-SA182-PACKAGE-COLLECTOR-01`;
  - `SRC-CN-2021-GAMER-SA182-DISC-COLLECTOR-01`.
- Canonical note: `research/clients/STONEAGE-2001-MAINLAND-PACKAGE-FAMILY-R1.md`.


## Mainland pre-release/test carrier and manual-print discriminator — 2026-09-27

- The early-Mainland recovery surface has moved earlier than the ordinary 1.82 package family.
- A preserved mirror of a **2001-01-05 China.com / 中华网游戏频道** mail-order notice explicitly says registered users who had participated in the site's **`《石器时代》试玩版赠送活动`** could buy the formal retail release at a discounted price. This independently establishes that a pre-retail trial-copy giveaway existed before the 2001-01-12 nationwide formal-sale date; the surviving notice does **not** identify the trial carrier format or magazine.
- Separately, the same 2020 physical-media collector who documented the 1.82 package family states that the **Mainland 1.0 test package** he obtained was not boxed: it consisted of a **test manual carrying a disc and was distributed as a magazine insert**. This is a later first-person collector claim and remains **OPEN / UNAUTHENTICATED** until the manual/disc is photographed with provenance or its magazine identity is independently resolved.
- This route now deserves independent tracking because an authenticated trial disc could predate the ordinary Mainland retail carrier and become the earliest known Mainland byte-diff anchor against Taiwan v1.0.
- A second new physical discriminator comes from a preserved transcription of Beijing Waei's **2001-03-12 manual-errata apology**. Waei says a manual editing error caused players to believe 50 hours had been removed, that **second-batch newly printed manuals would be corrected**, and that **first-batch manuals would only receive a web erratum**. Users registered before 2001-03-13 09:00 were granted an extra **300 points = 50 hours**.
- A surviving 17173 StoneAge 1.0 charging page independently preserves the corrected rule: product registration grants **300 points = 50 hours**.
- A 2003 17173 first-person player retrospective explicitly recalls that what had previously been stated as **600 points became 300 points**. This strongly supports, but does not yet prove from a first-batch manual itself, the working hypothesis that the first printing advertised **600 points / 100 hours** and the corrected printing used **300 points / 50 hours**.
- Keep a three-way evidence distinction:
  - contemporaneous Sina launch copy says the package included **45 hours** of free time;
  - the corrected charging standard is **300 points / 50 hours**;
  - **600 points / 100 hours as the first-print manual wording remains HYPOTHESIS** pending a scan/photo or contemporaneous source that quotes the printed line directly.
- Highest-value next evidence:
  1. photograph/scan of the pre-release Mainland test manual and disc, plus the magazine identity;
  2. first-batch and/or second-batch retail manual page containing the registration-time claim;
  3. package-to-manual-to-disc photo chain, publication number, matrix/IFPI, ISO/file tree or hashes.
- New canonical note: `research/clients/STONEAGE-MAINLAND-SA10-TEST-CARRIER-AND-MANUAL-R1.md`.


## Mainland official test CD confirmed on surviving China.com legacy site — 2026-09-27

- **CORRECTION / EVIDENCE PROMOTION:** the earlier record only established a generic pre-retail trial-copy giveaway from later mirrors. A still-live legacy **China.com / 中华网游戏频道** StoneAge page now preserves the original activity page itself: `https://game.china.com/hotspot/shiqi/answer/index.html`.
- The page title/body explicitly says **`石器时代游戏测试光盘免费大赠送`**. This promotes the existence of a pre-retail Mainland **physical test CD** from OPEN to **FACT / surviving contemporaneous portal page**.
- The activity page states:
  - outside Beijing, players completed the questionnaire and supplied a detailed mailing address to receive the **disc for free while supplies lasted**;
  - Beijing players were instructed to collect it at **晶合软件销售点**;
  - activity deadline: **2000-12-31**;
  - official test period: **2000-12-15 through 2001-01-10**.
- A separate still-live China.com legacy product page, `https://game.china.com/hotspot/shiqi/news/1.html`, identifies the formal Mainland retail product as **载体：1 CD-ROM**, nationwide release **2001-01-12**, and gives the JSS -> Beijing Waei -> Zhiguan -> Guangxi-Jinhaiwan publication chain.
- The legacy news archive `https://game.china.com/hotspot/shiqi/news/2.html` also directly preserves the January mail-order/trial-participant discount notices and the March manual-errata/charging announcements. The previous modern mirror sources remain useful fallbacks, but are no longer the best surviving surface.
- Independent channel corroboration: a surviving 晶合时代 corporate profile on OurGame says the company organized the **free distribution of StoneAge test-version software** and operated the 晶合 software retail chain. This coheres with China.com's instruction that Beijing users collect test discs from 晶合 outlets.
- **Priority change:** the **2000-12 Mainland official test CD** now outranks ordinary 2001 retail package archaeology as the earliest Mainland physical-client recovery target. The 2001 retail disc remains the next provenance anchor and comparison target.
- The 2020 collector's separate statement that a Mainland 1.0 test manual+disc was bundled with a magazine remains **OPEN**. Current evidence does not prove that his magazine-insert specimen is identical to the China.com/Jinghe giveaway disc.
- A constrained search of `大众软件` + StoneAge + 2000/test-disc combinations found **no direct issue/disc record tying the collector's magazine insert to 《大众软件》**. Jinghe's close corporate/media relationship with 《大众软件》 is therefore only a search hypothesis, not a carrier identification.
- Immediate target is now a public photograph, file tree, ISO/BIN/CUE, volume label, matrix/IFPI, hash, or exact magazine/disc catalogue identity for the **2000-12 test CD**.
- New source records:
  - `SRC-CN-2000-CHINADOTCOM-SA-TEST-CD-GIVEAWAY-01`;
  - `SRC-CN-2001-CHINADOTCOM-SA-LEGACY-PRODUCT-01`;
  - `SRC-CN-2001-CHINADOTCOM-SA-LEGACY-NEWS-ARCHIVE-01`;
  - `SRC-CN-EARLY-JINGHE-SA-TEST-DISTRIBUTION-01`.


## Mainland 2000 official test-CD preservation-index route bounded — 2026-09-27

- The dedicated **metadata-only** preservation probe for the now-confirmed December-2000 Mainland official test CD has completed.
- R1 used **10 source-derived query identities** across Internet Archive and DiscMaster:
  - Chinese identities: `石器时代 测试光盘`, `测试版 光盘`, `试玩版 光盘`, `晶合 测试`, `晶合`;
  - English/channel identities: `StoneAge test CD`, `StoneAge beta Waei`, `StoneAge trial Waei`, `StoneAge Jinghe`, `StoneAge jhpop`.
- R1 results:
  - **0 strict Internet Archive items** across all ten identities;
  - **0 strict DiscMaster hits** on the five Chinese identities;
  - the five English DiscMaster full-text searches timed out under the original parallel run and were therefore deliberately left OPEN rather than misreported as zero.
- R2 retried **only those five English DiscMaster residual identities**, sequentially and in two distinct scopes:
  - filename/name index;
  - full-text deep index.
- R2 completed **10 / 10 surfaces, 0 strict hits, 0 errors**.
- Therefore the currently tested direct preservation-index identity route is now **BOUNDED**. Do not repeat these same IA/DiscMaster query combinations unless a new artifact token appears.
- This negative index result does **not** negate the contemporaneously documented physical test CD. Highest-value reopen tokens are now: disc-face text/photo, magazine identity, exact filename, volume label, matrix/IFPI, catalogue/publication number, ISO/BIN/CUE/file tree, or checksum.
- Provenance-control refinement: a 2002 17173 first-person retrospective states that on Christmas during the Mainland test period the author began playing from a **disc burned/copied by a friend**. This is useful evidence that player-made copies circulated during testing, but is not evidence of an official pressing.
- Consequence for future recovery: classify any found test client independently on two axes:
  1. **payload lineage** — does the client/file tree match the Dec-2000 test build?;
  2. **physical carrier provenance** — official China.com/Jinghe giveaway original, magazine carrier, or player-burned copy.
- Derived reports:
  - `research/recovered/STONEAGE-MAINLAND-2000-TEST-CD-PRESERVATION-R1.txt`;
  - `research/recovered/STONEAGE-MAINLAND-2000-TEST-CD-DISCMASTER-RESIDUAL-R2.txt`.
- New source record: `SRC-CN-2002-17173-SA-TEST-CD-BURNED-COPY-RECOLLECTION-01`.


## China.com giveaway-result archive recovered; Popsoft carrier candidate downgraded — 2026-09-27

- The live China.com test-CD giveaway page's post-activity link has now been archive-resolved to exact historical article **`63271`**:
  - original URL: `http://game.china.com/zh_cn/news/news1/444/20001220/63271.html`;
  - Wayback exposes **8 HTTP-200 text/html captures** from 2001-03-09 through 2003-09-01;
  - earliest capture timestamp: **2001-03-09 22:31:37 UTC**.
- A privacy-safe replay of that earliest capture succeeded:
  - raw replay body: **44,048 bytes**, SHA-256 `a26933f2cdcf2d5e2fcd6c808000ae8c37af4c9999bcb17bda04feac3c68d403`;
  - decoded as GB18030;
  - page-level archaeology tokens include **`石器时代`**, **`赠送`**, **`名单`**, and **`光盘`**;
  - the page also contains historical participant contact fields, so raw HTML and participant rows are intentionally **not committed or reproduced**.
- Classification: **FACT / archived giveaway-results page**. It confirms the live activity page's “名单地址” target and the giveaway-result topology, but does not expose a disc filename, volume label, serial, matrix, ISO, or other optical identity.
- Asset-topology follow-up:
  - parsed **11 first-party image/background paths**;
  - **9 replayed successfully**, all small generic China.com logos/navigation/UI assets;
  - **0 large/page-specific candidate assets**;
  - the two unreplayed paths are generic UI filenames `close.gif` and `chinacom_logo.gif`;
  - therefore the current `63271` HTML/image surface yields **no StoneAge/test-CD-specific artifact token** and is operationally bounded unless a different capture/source exposes additional assets.
- The source-driven `《大众软件》` carrier hypothesis was separately tested against the preserved IA scan family `popsoft-magazine_202403`:
  - six OCR files covering **2000-11 A/B, 2000-12 A/B, 2001-01 A/B** were inspected;
  - the scan family exposes **0 optical-image files**;
  - only **one StoneAge anchor** appears across the six issues: `Stone Age` once in **2000-12A**;
  - that occurrence has **0 nearby carrier/test-context flags**;
  - result: **EDITORIAL-ONLY / NO CARRIER SIGNAL** for the tested launch window.
- Consequence: do **not** continue treating `《大众软件》` as the leading test-disc magazine carrier merely because of Jinghe's corporate relationship. It remains a weak ecosystem lead only.
- Current highest-value OPEN targets remain:
  1. an independent public photo/scan of the collector-described Mainland 1.0 **test manual + disc**;
  2. the exact magazine title/issue that carried it;
  3. any official/burned test-client file tree, installer filename, volume label, matrix/IFPI or checksum;
  4. a first-print retail manual page resolving the 600→300 point misprint hypothesis.
- Derived evidence:
  - `research/recovered/STONEAGE-CHINA2000-TEST-CD-LEGACY-ARCHIVE-R1.txt`;
  - `research/recovered/STONEAGE-CHINA2000-63271-REPLAY-R1.txt`;
  - `research/recovered/STONEAGE-CHINA2000-63271-ASSET-TOPOLOGY-R1.txt`;
  - `research/recovered/STONEAGE-POPSOFT-2000-LAUNCH-WINDOW-R1.txt`.


## Waei.net archived StoneAge `spr_1.bin` byte anchor — 2026-09-27

- The early Waei download investigation has produced the project's first newly recovered **byte-level StoneAge resource artifact** from the 2001 Waei.net central-download archive.
- A fast Wayback CDX census over `http://www7.waei.net/download/` for 2000-12 through 2001-06 recovered **119 unique URL rows**, including **69 `/download/file/` rows**, **57 binary-extension rows**, and detail-page IDs **1–6**.
- Among those rows is:
  - capture: **2001-06-05 17:45:50 UTC**;
  - archived path: `/download/file/<Big5 修補程式>/spr_1.bin`;
  - MIME: `application/octet-stream`;
  - Wayback CDX digest: `5ADTXXSBOAQLKL7URZHYKWOJHDEQ7SOM`.
- **Important correction:** the CDX `length=391581` is not the original payload size. A privacy/copyright-safe transient replay recovered the binary only long enough to hash it, yielding:
  - bytes: **2,889,630**;
  - SHA-256: `864fa3f6aaeb7d8d2dc9bdee46cecdc7dcee1af0c8f1ed949e09c0526e6aa17e`;
  - SHA-1: `e8073bde417020b52ff48e4f8559c938c90fc9cc`;
  - MD5: `7b40970c8f2a11a523f4a314c78b459e`;
  - recovered SHA-1/Base32 matches the Wayback CDX digest exactly.
- Comparison against the accepted Taiwan v1.0 retail client's `StoneAge/data/spr_1.bin`:
  - both files are **exactly 2,889,630 bytes**;
  - hashes differ;
  - the Waei file parses **perfectly under Taiwan v1.0's unchanged `spradrn_1.bin` index geometry**: **464 groups / 39,065 animations / 242,085 frames / full span closure**.
- The byte difference is exceptionally small and structured:
  - **16 changed bytes / 2,889,630 = 0.000554%**;
  - four 4-byte runs, all inside **group 102 / `spr_no=100102`**;
  - **463 / 464 groups are byte-identical**.
- Semantic field mapping shows the only changes are four frame `bmp_no` values:
  - anim 82 frame 0: `0xFFFFFFFF -> 126235`;
  - anim 83 frame 0: `0xFFFFFFFF -> 126236`;
  - anim 83 frame 1: `0xFFFFFFFF -> 126237`;
  - anim 84 frame 1: `0xFFFFFFFF -> 126238`.
  All coordinates, sound IDs, animation counts, frame counts and all other bytes remain unchanged.
- A lookup against the accepted Taiwan v1.0 `adrn_1.bin` derived metadata finds **none of bitmap IDs 126235–126238**. Therefore the Waei `spr_1.bin` activates four image references that are not present in the Taiwan v1.0 image-address table.
- **Strong inference / not yet direct artifact recovery:** this resource change likely belonged with additional `ADRN/REAL` image-resource additions. Exact CDX probes for same-directory `spradrn_1.bin`, `adrn_1.bin` and `real_1.bin` currently return zero rows, so those companion bytes are not recovered.
- Evidence classification:
  - **FACT / strong byte-level StoneAge resource-lineage evidence:** same exact container length, same Taiwan v1.0 sprite index geometry, 99.999446% byte identity, coherent four-frame bitmap-reference delta, Waei.net `修補程式` archive provenance;
  - **OPEN:** exact product/version label, region/client branch, download-detail title, and whether this artifact was part of a Mainland client update.
- Regional boundary: `www7.waei.net` is the Waei International / Big5 web surface. Do **not** silently relabel this 2001-06 archive as Beijing-Waei/Mainland media. It is a Waei-hosted StoneAge resource anchor whose branch binding remains OPEN.
- Separately, a near-period 17173 player diary published 2001-06-13 recalls that on **2001-01-04** the author visited the Waei homepage and saw a **StoneAge trial download of roughly 274 MB**. This supports an online trial-client distribution route in addition to the confirmed Mainland physical test-CD giveaway, but supplies no filename or byte identity.
- The failed broad Waei central-download replay is explicitly **not a negative result**: it was cancelled after the 15-minute runner limit while replaying many pages. The replacement metadata census succeeded and should be the basis for targeted probes.
- Derived evidence:
  - `research/recovered/STONEAGE-WAEI-DOWNLOAD-CENTER-INDEX-CENSUS-R1.txt`;
  - `research/recovered/STONEAGE-WAEI-SPR1-BYTE-METADATA-R2.txt`;
  - `research/recovered/STONEAGE-WAEI-VS-TW10-SPR1-DIFF-R1.txt`;
  - `research/recovered/STONEAGE-WAEI-VS-TW10-SPR1-FIELD-DIFF-R2.txt`;
  - `research/recovered/STONEAGE-TW10-BITMAP-126235-126238-R1.txt`.
- Canonical technical note: `research/clients/STONEAGE-WAEI-2001-SPR1-DIFF-R1.md`.
- Priority after recording this milestone returns to **full-client recovery**: resolve the ~274 MB Jan-2001 Waei trial-download filename/route or the Dec-2000 Mainland official test-CD bytes, while using this `spr_1.bin` as an early resource-diff control.


## Waei `spr_1.bin` official patch-title binding closed — 2026-09-27

- The previously OPEN human-readable title association for the archived Waei `spr_1.bin` is now **directly closed by archived Waei catalogue and redirect evidence**.
- Waei central-download category **ID=1 = 修補程式**. Its preserved 2001-06 catalogue page explicitly lists:
  - title: **`石器隱形人無所遁形修正檔`**;
  - displayed date: **2001/4/26**;
  - instructions: save into the StoneAge execution directory, e.g. `C:\\Program Files\\Waei\\石器時代\\data`, and overwrite the existing file;
  - displayed size: **2,822 KB**;
  - download control: **`download.asp?fileid=133`**.
- Wayback preserves `download.asp?fileid=133` at **2001-06-05 17:42:13 UTC** as an HTTP 302. A no-follow replay recovers the historical `Location` target directly as:
  - `http://www7.waei.net/download/file/<Big5 修補程式>/spr_1.bin`.
- The target `spr_1.bin` is independently preserved three minutes later at **17:45:50 UTC** and transiently recovers to:
  - **2,889,630 bytes = 2,821.904 KiB**, consistent with the catalogue's rounded **2,822 KB** display;
  - SHA-256 `864fa3f6aaeb7d8d2dc9bdee46cecdc7dcee1af0c8f1ed949e09c0526e6aa17e`.
- Classification upgrade:
  - **FACT:** this exact byte artifact is the payload served by Waei fileid 133 for the named StoneAge patch `石器隱形人無所遁形修正檔`;
  - **FACT:** official Waei StoneAge patch provenance is now direct, no longer inferred only from container geometry;
  - **OPEN:** exact client version/build and regional branch to which the patch was intended to apply.
- Regional boundary remains unchanged: the source is **Waei.net / Big5**. Do not relabel it as Beijing-Waei/Mainland test or retail media without explicit regional evidence.
- New derived evidence:
  - `research/recovered/STONEAGE-WAEI-DOWNLOAD-ID12-R1.txt`;
  - `research/recovered/STONEAGE-WAEI-ID1-PATCH-CONTROLS-R1.txt`;
  - `research/recovered/STONEAGE-WAEI-FILEID133-ROUTE-R1.txt`;
  - `research/recovered/STONEAGE-WAEI-FILEID133-HEADER-R1.txt`.
- Full-client recovery remains higher priority than further analysis of this patch: the unresolved primary target is still the ~274 MB Jan-2001 Waei trial client and/or the Dec-2000 Mainland official test-CD bytes.

## Jinghe/Yegame StoneAge retail-catalog binding — 2026-09-27

- A source-grounded archive chain now connects the proven Mainland test-CD distributor **晶合时代 / JHPOP** to its historical commerce site:
  - the archived **2000-12-04** `www.jhpop.com` root directly redirects to `http://www.yegame.com`;
  - archived Yegame pages identify the site as **晶合软商网 / 晶合商机网** and expose a dedicated `/product/game/` catalog.
- The recovered **2001-04-06** Yegame network-game category page directly lists:
  - product name: **石器时代**;
  - product code/link: **`EN0ZGKJ0002`** -> `product/detail.asp?prodencode=EN0ZGKJ0002`;
  - product medium: **`1-CD`**;
  - catalog **更新日期: 2001-1-16**;
  - retail price: **¥29.00**;
  - wholesale price: **¥26.00**.
- The same catalog independently exposes **石器时代-WGS620点会员卡**, product code **`EZ0JHSD0003`**.
- Evidence classification:
  - **FACT:** by 2001-04-06 the historical Jinghe/Yegame catalog represented Mainland `石器时代` as a **1-CD** product under exact catalog key `EN0ZGKJ0002`;
  - **FACT:** the catalog recorded `2001-1-16` in its **更新日期** field and ¥29/¥26 retail/wholesale values;
  - **BOUNDARY:** `2001-1-16` is a catalog update field, **not automatically a release date**;
  - **BOUNDARY:** this retail-catalog record does **not** identify or authenticate the earlier **2000-12 Mainland official test CD**, nor does it recover retail bytes.
- Cross-source consequence: the **1-CD** catalog medium coheres with the already recovered China.com formal-product record `载体：1 CD-ROM`, providing an independent commerce-channel carrier check.
- Recovery consequence: the exact product code `EN0ZGKJ0002` is now a high-value search token for archived detail pages, cover images, catalog mirrors and physical-media listings. Full-client recovery still outranks price/package archaeology.
- Derived reports:
  - `research/recovered/STONEAGE-JHPOP-2000-ROOT-REPLAY-R2.txt`;
  - `research/recovered/STONEAGE-YEGAME-2000-TEST-CD-ARCHIVE-R1.txt`;
  - `research/recovered/STONEAGE-YEGAME-EXACT-PAGE-REPLAY-R1.txt`;
  - `research/recovered/STONEAGE-YEGAME-GAME-CATALOG-R1.txt`.

## Jinghe/Yegame StoneAge product-detail closure — 2026-09-27

- The exact Yegame product route for **`EN0ZGKJ0002 = 石器时代`** is now archive-bound by **three HTTP-200 captures**:
  - 2001-04-15 16:23:00 UTC;
  - 2001-07-17 23:54:14 UTC;
  - 2001-08-16 20:35:29 UTC.
- The 2001-08-16 capture replayed successfully and directly preserves the historical product-detail body:
  - title/product: **石器时代**;
  - code: **`EN0ZGKJ0002`**;
  - medium: **`1-CD`**;
  - retail: **¥29.00**;
  - preferential price: **¥26.00**;
  - promotional statement: **随游戏赠送45小时免费时间，2001年1月至2月期间贺岁免费畅游**;
  - catalog copy also describes pet capture/growth, more than 100 creatures, 12 base character designs x 4 colors, and 12 expressive character actions.
- The detail page carries a historical product-image reference:
  - **`/product_images/EN0ZGKJ0002.jpg`**.
  Its exact image CDX query failed transiently in this run, so image preservation remains **OPEN**.
- The same probe binds **`EZ0JHSD0003 = 石器时代-WGS620点会员卡`** by three HTTP-200 captures. The replayed page states:
  - **620 points**;
  - medium **单卡**;
  - retail **¥30.00**;
  - preferential price **¥27.00**;
  - usable for games under WGS, with billing depending on period/game type.
- Evidence boundary:
  - this is direct historical commerce/catalog evidence from Jinghe's Yegame surface;
  - it is **not** client-byte provenance and does not identify the Dec-2000 official test CD;
  - the detail page's printed minimum-configuration values are preserved as catalog text and must not override byte/manual-derived technical facts if they conflict.
- Recovery consequence: `EN0ZGKJ0002` and `product_images/EN0ZGKJ0002.jpg` are now exact physical-media/cover search tokens. After one bounded cover-image archive probe, priority returns to **full-client byte recovery**.
- Derived report: `research/recovered/STONEAGE-YEGAME-STONEAGE-PRODUCT-DETAIL-R1.txt`.

## Waei first-party runtime-generation byte chain — 2026-09-27

- Accepted Taiwan v1.0 already establishes the first-party updater/runtime split: launcher `StoneAge.exe` embeds `stoneage.waei.net`, `/saupdate/newest.txt`, `/saupdate/%s` and child token `updated`; its runtime is `sa_3.exe` (425,984 bytes, SHA-256 `cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a`).
- Wayback now yields two byte-recoverable first-party Waei runtime executables:
  - `sa_40.exe`: 528,384 bytes; SHA-256 `d54a6c109644dd4842f61bdd42a95362fda7a16f5e9b9dbd829d6b97c678fde1`; SHA-1 `6eafbf9a886021291cde16b7c9baf22192bae32a`; MD5 `9b9820b6e3e4578a93c20ba34309bd21`; PE timestamp 2001-09-27 08:31:27 UTC.
  - `sa_42.exe`: 557,056 bytes; SHA-256 `744fc0557f024930f351ef31b6adac0dbe41968625105d5f0eba45be1a048df6`; SHA-1 `45b0f0a3de4d04961cd0a43c3d70209d35089724`; MD5 `608f5b92c5de42496e839d59d23ad12d`; PE timestamp 2001-11-01 02:54:29 UTC.
- Both are ordinary Win32 PE game runtimes, not installer/SFX wrappers. Their version resources identify `CompanyName=Waei`, `FileDescription/InternalName=SaDeb`, `OriginalFilename=SaDeb.exe`, `ProductName=Waei SaDeb`, version `1.0.0.1`.
- Both contain `updated`, `StoneAge.exe` and `yStoneAge.exe` but not the update-host URL strings, directly reinforcing the launcher -> child-runtime architecture already present in Taiwan v1.0.
- Runtime evolution: both later runtimes reference battle maps through `battle219` whereas accepted Taiwan v1.0 `sa_3.exe` stops at `battle217`; `sa_42` retains the `sa_40` path set and adds `data\\AISetting.dat` and `data\\album_2.dat`.
- Critical version-number correction: Waei's own 2003 public prospectus dates marketing releases as 2.0=2001-08-01, 2.5=2001-11-01, 3.0=2002-03-01, 4.0=2002-07-01. Therefore filenames `sa_40.exe` / `sa_42.exe` do NOT mean marketing StoneAge 4.0 / 4.2.
- A later community chronology explicitly records `SA_24` on 2001-04-24 as the update that added trading, independently supporting `SA_N` as an internal update/runtime-generation naming series rather than a marketing-version series.
- `sa_42`'s PE timestamp falls on 2001-11-01, exactly Waei's corporate date for StoneAge 2.5. Classification: STRONG TEMPORAL 2.5-ERA ANCHOR, but exact 2.5 launch/base-runtime identity remains OPEN because no first-party manifest names `sa_42` as the 2.5 base executable.
- Exact first-party generation census, 2000-2002: `sa_3` 0 rows; `sa_23` 404 only; `sa_24` 0 rows; `sa_25` 0 rows after dedicated retry; `sa_40` repeated HTTP-200 captures with stable digest; `sa_41` 404 only; `sa_42` repeated HTTP-200 captures with stable digest.
- The archived 2001-05-30 `/saupdate/?M=D` page contains only `石器時代更新專用目錄` and no file links; it cannot recover the missing generation list.
- Regional boundary: these binaries are Taiwan/Waei first-party `stoneage.waei.net` artifacts. Do not relabel them as Beijing-Waei/Mainland test or retail binaries.
- Priority remains FULL-CLIENT RECOVERY: use this recovered filename/runtime grammar as a control while pursuing the ~274 MB Jan-2001 Waei trial client and Dec-2000 Mainland official test-CD bytes. Reopen missing `SA_N` generations only when a new first-party manifest/page/filename token appears.
- Derived reports: `STONEAGE-WAEI-SUBDOMAIN-LAUNCH-CDX-R1.txt`, `STONEAGE-WAEI-SA40-SA42-PAYLOAD-CLASSIFIER-R1.txt`, `STONEAGE-WAEI-SA40-SA42-LINEAGE-R1.txt`, `STONEAGE-WAEI-SAUPDATE-DIRECTORY-R1.txt`, `STONEAGE-WAEI-RUNTIME-GENERATIONS-R1.txt`, `STONEAGE-WAEI-SA25-GENERATION-RESIDUAL-R1.txt`.

## Launch-window download-route residuals bounded — 2026-09-27

- The source-derived Waei www9 dynamic-download hypothesis is now operationally **BOUNDED**:
  - preserved 2000-12-06 Waei download catalogue uses trial-category IDs 33 and 34;
  - exact launch-window probes covered downloading.php?ID=35..60;
  - R1/R2/R3 provide at least one successful exact CDX query for every ID in that range, including final port80/noport recovery of IDs 59/60;
  - **0 archived rows / 0 redirect targets / 0 filename tokens** were recovered.
- Consequence: do **not** continue expanding sequential www9 IDs without a new first-party filename, route, category or manifest token. ID adjacency was only a search heuristic and produced no StoneAge evidence.
- Derived reports:
  - research/recovered/STONEAGE-WAEI-WWW9-EXACT-POSTDEC6-IDS-R1.txt;
  - research/recovered/STONEAGE-WAEI-WWW9-EXACT-POSTDEC6-IDS-RESIDUAL-R2.txt;
  - research/recovered/STONEAGE-WAEI-WWW9-EXACT-POSTDEC6-IDS-FINAL-R3.txt.

- The archived China.com giveaway-results page directly exposed two historical first-party paths, /zh_cn/hotspot/shiqi/index.html and /zh_cn/download/index.html, so those route families were tested separately for **2000-12-01..2001-01-20**.
- Result:
  - /zh_cn/hotspot/shiqi/ exposes **0 indexed rows** in the tested launch window;
  - /zh_cn/download/ exposes exactly **one** preserved row, 2000-12-19 /zh_cn/download/pic/a_1.html;
  - residual replay identifies that page as an **艾尔达传奇** image-download page: displayed size **824K**, format **JPG**, description **9 images**, with link /zh_cn/download/pic/ws2000.zip;
  - the page contains **0 StoneAge semantic tokens**.
- Classification: the sole China.com /zh_cn/download/ launch-window object is **UNRELATED** to StoneAge. The tested /zh_cn/ StoneAge/download route family is therefore **BOUNDED** unless a new exact historical path or filename appears.
- Derived reports:
  - research/recovered/STONEAGE-CHINA2000-ZHCN-SHIQI-DOWNLOAD-R1.txt;
  - research/recovered/STONEAGE-CHINA2000-ZHCN-DOWNLOAD-RESIDUAL-R2.txt;
  - research/recovered/STONEAGE-CHINA2000-ZHCN-DOWNLOAD-CLASSIFICATION-R3.txt.

- A separate 17173 launch-download archive probe produced **0 rows** on its completed exact routes and no payload/link recovery; several prefix/metadata requests failed transiently. It is not promoted over the first-party Waei/China.com evidence and remains a low-priority residual unless a source-derived 17173 filename/path appears.
- **Priority remains FULL-CLIENT RECOVERY.** The unresolved high-value targets are still:
  1. the exact filename/route or preserved mirror of the **~274 MB Jan-2001 Waei StoneAge trial client**;
  2. byte-level recovery of the **Dec-2000 Mainland official test CD** (ISO/BIN/CUE, file tree, volume label, matrix/IFPI, checksum or an installed-tree copy).
- Next-search rule: prefer **independent mirror/carrier evidence or newly recovered exact tokens**. Do not repeat the bounded Waei-ID or China.com /zh_cn/ surfaces.

## DiscMaster early-client signature surface bounded — 2026-09-27

- DiscMaster public indexing was tested against the accepted Taiwan v1.0 client in two complementary modes for the early **1999..2002** window:
  1. filename signatures: `real_1.bin`, `adrn_1.bin`, `spr_1.bin`, `spradrn_1.bin`, `battletxt_1.txt`, `soundaddr_1.txt`, with `sa_3.exe`, `StoneAge.exe` and `setup.inx` as supporting signals;
  2. full-text/internal strings: `stoneage.waei.net`, `/saupdate/newest.txt`, `spradrn_1.bin`, `battletxt_1.txt`, `soundaddr_1.txt`, plus supporting `StoneAge.exe`.
- All filename queries completed. No multi-signal early-client carrier was found; generic `setup.inx` hits are InstallShield noise and have no StoneAge-resource co-occurrence.
- Full-text R1 initially timed out on four terms; R2 retried only those residuals sequentially. All completed with **0 rows / 0 carriers / 0 errors**. The updater anchors `stoneage.waei.net` and `/saupdate/newest.txt` both expose zero indexed rows.
- Classification: **DiscMaster early-client filename + full-text signature surface = BOUNDED**. Do not repeat equivalent queries without a new exact filename, hash, archive-member path, volume label or installer token.
- Derived closure: `research/recovered/STONEAGE-EARLY-CLIENT-DISCMASTER-CLOSURE-R3.txt`.
- This is a preservation-index negative only. It does **not** negate the documented Dec-2000 Mainland test CD or the Jan-2001 ~274 MB Waei trial download.
- Full-client recovery remains highest priority; next work should seek a new exact token from historical page routing, independent mirrors/carriers or physical-media provenance.

## China.com Jan-2001 mail-order route correction — 2026-09-27

- A later preserved historical text identifies a **2001-01-05** article titled `中华网游戏频道 特别推出《石器时代》的邮购服务`, but mirror-rewritten links are not accepted as historical href provenance.
- The proven first-party China.com `news1/444/YYYYMMDD/<id>.html` namespace was tested for **2001-01-04..06**:
  - Jan-05 prefix: **0 indexed rows**;
  - Jan-04: IDs `78771 / 78775 / 78779 / 78782`;
  - Jan-06: ID `80570`.
- R1 initially overclassified three Jan-04 pages because their **global site footer** contains `游戏《石器时代》专题` and `下载指南`. That is not article-body evidence.
- R2 retried every failed neighbor capture with a strict rule requiring `邮购 / 试玩版 / 赠送活动 / 注册名单` semantics:
  - 3 / 3 residual pages replayed;
  - strict matches **0**;
  - errors **0**.
- Correction: R1 `CHINACOM_JAN5_STONEAGE_ARTICLE_RECOVERED` is **REJECTED** as a footer-derived false positive.
- A complete launch-window Wayback prefix census of `game.china.com/hotspot/shiqi/` also returns **0 indexed rows**. Current/live legacy China.com StoneAge pages may survive, but they cannot be assigned a 2001 archive timestamp without a historical capture.
- Classification: **original Jan-05 China.com article URL/hrefs remain UNRECOVERED**. Do not repeat Jan4–6 `news1/444` or legacy `/hotspot/shiqi/` Wayback-prefix searches unless a new exact article ID/path appears.
- Derived classification: `research/recovered/STONEAGE-CHINA2001-JAN5-MAILORDER-CLASSIFICATION-R3.txt`.
- Priority remains **FULL-CLIENT RECOVERY** through contemporaneous independent mirrors/carriers or newly recovered first-party binary/path tokens.


## Recovery strategy correction — online-recoverable bytes first — 2026-09-27

- User direction: the project is not trying to build a museum-grade catalogue of physical StoneAge media. The practical goal is to recover game/client data that can actually be obtained online and used for reverse engineering and reconstruction.
- **New hard gate:** primary recovery work must target digitally retrievable artifacts: downloadable installers/archives, public disc images, installed-client trees/file sets, byte-recoverable first-party files, or exact filenames/URLs/archive identifiers/hashes/manifests that directly lead to such bytes.
- **Physical-only archaeology is downgraded:** magazines, newspaper articles, package photos, disc photos, auction listings and collector descriptions are supporting context only. Do not expand these tracks merely to identify packaging, publication title, artwork, distribution anecdotes or physical provenance.
- Reopen a physical/publication lead only if it produces a direct online acquisition bridge such as an exact filename, downloadable URL, public archive ID, freely accessible ISO/BIN/CUE/IMG, checksum, volume label/file tree tied to a retrievable copy, or a mirror that exposes actual client contents.
- The Dec-2000 Mainland official test CD remains historically documented but is **no longer a blocking primary target if only physical provenance survives**. Do not spend further cycles identifying its magazine, package or disc appearance unless that information directly locates online bytes.
- The ~274 MB Jan-2001 Waei trial client remains high-value specifically because it was an **online download**. Continue seeking its exact filename, historical URL, preservation mirror or surviving downloadable copy.
- The project already has an accepted Taiwan/Waei v1.0 clean baseline. Therefore, if no earlier downloadable client is presently recoverable, immediately continue technical reverse engineering of that baseline rather than stalling on physical-media archaeology.
- Current technical priority order:
  1. recover any earlier or parallel clean client that is directly downloadable online;
  2. otherwise deepen Taiwan/Waei v1.0 reverse engineering: complete file tree, executables/runtime/updater, resource containers/indexes, maps, characters, pets, items, skills, combat, UI/text/data tables and network/update behavior;
  3. use recovered first-party patches/runtime/resources as controlled version-diff anchors;
  4. integrate earlier artifacts later if/when online-recoverable bytes surface.
- Any magazine/periodical/physical-carrier census started before this correction is non-blocking and must not spawn further speculative expansion unless it yields a direct downloadable-byte lead.
- Governing decision: docs/DESIGN-DECISIONS.md DD-011.


## Reconstruction scope clarification — early baseline + selective later-version integration — 2026-09-27

- The project does **not** need an absolute-earliest historical client before reconstruction can begin.
- A sufficiently early, official, clean, complete and technically usable client may serve as the reconstruction foundation baseline.
- The baseline is used to recover the original game's core architecture, data organization, rules, systems and experiential DNA; it is **not** a requirement that the final game remain locked to that historical version.
- Later official StoneAge releases should be studied as a **content/system library and evolutionary record**. Maps, pets, quests, mechanics, convenience features, progression ideas and world content may be selectively reused, adapted, merged, redesigned or rejected.
- Final inclusion criterion is project coherence: single-player suitability, world consistency, pacing, system quality, emotional milestones and technical cleanliness—not historical chronology alone.
- This means large future changes are expected and acceptable. The goal is a modern reconstruction informed by official StoneAge history, not a cumulative museum clone of every official release.
- Operational consequence: once the current earliest usable official clean baseline is confirmed complete enough, research effort should shift decisively from open-ended client hunting into technical recovery and specification. Newer official versions can then be brought in later as structured comparison/input sources.
- Governing decision: docs/DESIGN-DECISIONS.md DD-012.


## Product architecture clarification — private single-player delivery, MMORPG-style play — 2026-09-27

- Current product/deployment boundary: develop for **private single-player use**, not as an unauthorized public online service.
- Gameplay direction remains intentionally **MMORPG-like**: persistent long-form progression, pet collection/growth, repeatable combat, large-world exploration, economy-like loops, quests/unlocks, convenience/automation and other systems may preserve the feel and depth of an online RPG even though execution is local/single-player.
- `Single-player` therefore describes the deployment/access model, not a requirement to turn StoneAge into a short or linear conventional standalone RPG.
- Architecture should preserve future optionality without prematurely building an MMO backend: separate deterministic core rules/data from UI and transport; use explicit world/player/pet/item/combat state models; keep local persistence authoritative now; avoid unnecessary coupling that would make a future authorized client/server split difficult.
- No current requirement exists for accounts, public servers, live ops, multiplayer sync, anti-cheat or social-service infrastructure.
- Historical network/server analysis remains valid only where it helps recover original rules, state boundaries or data behavior.
- Long-term possibility: if the project becomes mature enough, it may someday be presented to or discussed with the relevant StoneAge rights-holder as a prototype/foundation for an officially authorized product. This is future optionality only; the project currently makes no claim of authorization or official status.
- Governing decision: docs/DESIGN-DECISIONS.md DD-013.


## Foundation baseline acceptance and phase transition — 2026-09-27

- Formal acceptance record added: `research/clients/STONEAGE-TW10-FOUNDATION-BASELINE-ACCEPTANCE-R1.md`.
- **TAIWAN_V1_FOUNDATION_BASELINE_R1 = ACCEPTED.** The accepted Taiwan Waei/JSS v1.0 retail-disc specimen (Redump 104630) is sufficient to anchor technical reconstruction and the future independent single-player implementation.
- Deterministic client boundary now established at 411 filesystem files / 383 core StoneAge files / 373,564,663 core-client bytes, with SHA-256 provenance anchors for every core file.
- Major baseline domains already have reconstruction-grade evidence: graphics/ADRN+REAL, animation/SPR+SPRADRN, battle SAB/palette corpus, indexed/loose audio, launcher/runtime split, gameplay protocol/state surfaces, map-cache receive/write behavior and controlled v1↔2.5 gameplay/master-data bridges.
- Important boundary: this is a **complete-enough historical foundation client**, not a claim that the retail disc contains the original MMO's complete server/world/master-data corpus. Ordinary field maps were runtime/server delivered; no obvious standalone v1 pet/item/NPC/quest master tables exist on disc. These are known architectural boundaries, not specimen failures.
- The recovered 2.5 server/master-data corpus remains a version-tagged bridge only. Later fields/data must not be silently projected backward into Taiwan v1.0 FACT.
- The v1 `data/savedata.dat` R1 probe recovered the exact 128-byte seed identity and runtime pathname; direct text xrefs are absent, so pointer/table indirection remains a non-blocking reverse-engineering detail. A follow-up pointer-trace workflow has already been added to the technical track.
- **Critical-path correction:** older statements in this file saying `FULL-CLIENT RECOVERY remains highest priority` are superseded by this dated milestone and DD-011/DD-012. Open-ended earliest-client hunting is now NON-BLOCKING.
- The ~274 MB Jan-2001 Waei online trial client remains a valuable opportunistic diff target, but the project must not delay reconstruction while searching for it.
- Physical-only test-CD / magazine / packaging work remains outside the primary path unless it directly produces digitally retrievable bytes.
- README phase advanced to **Phase 1 — Foundation Baseline Technical Reconstruction & Specification**.
- Current highest-priority work is now:
  1. close remaining v1 runtime/gameplay semantics that materially affect deterministic game rules;
  2. consolidate character/pet/item/skill/NPC/battle/encounter/world state into engine-neutral specifications;
  3. reconstruct/version-tag field-map and server-authoritative world content from recoverable official/later evidence;
  4. explicitly mark DESIGN substitutions where exact early server content cannot be recovered;
  5. prepare a local-first single-player implementation architecture with MMORPG-style systems, without building premature public-server/live-service infrastructure.


## Phase 1 world-map lineage closure — 2026-09-27

- World reconstruction policy added: `research/clients/STONEAGE-WORLD-MAP-RECONSTRUCTION-POLICY-R1.md`.
- A complete cross-version comparison of the recovered 2.5 map corpus and the archived 2003 map package is now recorded in `research/recovered/STONEAGE-TW10-FIELDMAP-LINEAGE-R1.txt`.
- Both later corpora expose the same **995 valid map paths**.
- **980 / 995** paths have byte-identical payloads (same SHA-256) across both corpora; only **15** changed.
- **761** maps are simultaneously:
  1. same path in both later corpora;
  2. byte-identical across both;
  3. fully renderable through the accepted Taiwan-v1 ADRN/resource profile.
- New reconstruction label: **STABLE_LATER_MAP_CANDIDATE**. These 761 maps are high-priority world-content candidates because they combine later-lineage persistence with v1 asset compatibility.
- Boundary: this still does **not** prove concrete Taiwan-v1 map membership. Resource compatibility and later persistence cannot be promoted to v1 historical membership without independent early evidence.
- The 15 changed maps are controlled map-evolution diff targets and must remain version-tagged rather than normalized.
- Operational consequence: the project no longer depends on recovering the historical v1 map server before building the modern world. V1 supplies the map/cache runtime foundation; stable later maps supply a versioned content library; DESIGN reconstruction fills remaining gaps.


## Phase 1 Taiwan v1 battle-receive closure — 2026-09-27

- Direct Taiwan-v1 battle receive-state reconstruction is now recorded in:
  - `research/clients/STONEAGE-TW10-BATTLE-RECEIVE-STATE-R1.md`;
  - `research/recovered/STONEAGE-TW10-GAMEPLAY-CALLBACKS-R1.txt`;
  - `research/clients/STONEAGE-TW10-GAMEPLAY-SCHEMA-R1.json` under `protocol_state_machines.battle_receive`.
- The v1 generated receive dispatcher directly proves `B(string command) -> callback RVA 0x32c70`.
- The original `sa_3.exe` callback directly discriminates command byte 1 as:
  - `C`;
  - `P`;
  - `A`;
  - `U`;
  - default/fallthrough.
- `C` directly writes the full command into a **4-slot × 4096-byte** status ring; write index wraps with mask `3`.
- Default/fallthrough directly writes the full command into a second **4-slot × 4096-byte** battle-command ring; write index also wraps with mask `3`.
- `P` directly parses three hexadecimal fields from `command + 3`; original v1 format literal is **`%X|%X|%X`** at RVA `0x5c98c`.
- `A` directly parses two hexadecimal fields from `command + 3`; original v1 format literal is **`%X|%X`** at RVA `0x5c984`, followed by conditional turn-number synchronization and clearing of the one-shot receive flag.
- `U` directly sets one battle-state global to `1`; pinned descendant lineage corroborates its semantic role as the battle escape flag.
- Pinned descendant source remains semantic corroboration for human variable names only. The command discriminator, queue geometry, parse arities, parser formats and state mutations are now **V1_DIRECT**.
- Later descendant conditional `Z/F/O` receive branches are explicitly excluded from v1-direct baseline evidence.
- Important architecture distinction:
  - existing player command model = **player -> authoritative resolver/server intent**;
  - v1 `B` receive state = **authoritative result -> client state/presentation stream**.
  They are not conflated archaeologically.
- Reconstruction consequence: the modern local-first engine should replace historical string/network queues with typed deterministic boundaries:
  `BattleIntent -> resolver -> BattleStateSnapshot / BattleEvent -> presentation`.
- The machine-readable battle state machine was deliberately placed under top-level `protocol_state_machines`, not `records`, preserving the invariant that `records` contains only dense fixed-position record layouts.
- Validation after integration is clean:
  - gameplay schema run **36331944401 = PASS**;
  - gameplay model run **36331944395 = PASS**;
  - v1↔2.5 bridge run **36331944375 = PASS**.
- **TW10_BATTLE_RECEIVE_STATE_R1 = CLOSED.**
- Next battle implementation seam: define the engine-neutral typed event/state contract that preserves the proven v1 separation between submitted intent, authoritative battle state, execution/animation events, turn synchronization and battle termination, without retaining the original online string protocol as an internal dependency.


## Phase 1 typed battle event/state contract — 2026-09-28

- Engine-neutral battle transition contract added:
  - `tools/stoneage_battle_event_contract.py`;
  - `tests/test_stoneage_battle_event_contract.py`;
  - `research/mechanics/STONEAGE-BATTLE-EVENT-CONTRACT-R1.md`.
- This is a **DESIGN / implementation layer** grounded in the closed Taiwan-v1 battle-receive evidence; it is not promoted as an original historical packet or server-memory layout.
- The contract preserves the proven conceptual separation without retaining the historical `B` string protocol:
  - submitted `BattleIntent`;
  - authoritative `BattleStateSnapshot` wrapping the existing immutable `PersistentBattleState`;
  - ordered `BattleExecutionEvent` stream wrapping existing typed `OrdinaryRoundEvent` values;
  - `BattleTurnSync` requiring exactly one authoritative turn of progress;
  - optional `BattleTermination` that must exactly match the terminal authoritative state.
- `build_battle_round_transition(PersistentRoundResult)` is an adapter only. It does not recalculate combat. Existing `battle_*_model.py` code remains the sole rule authority.
- Submitted intents are normalized by historical battle-slot order rather than mapping insertion order; command identities absent from the before-state slot map are rejected.
- Active transitions cannot emit termination; finished transitions cannot omit it. Terminal result/winning-side/turn must match the after-state.
- Historical BC/default-command/BA/BU network-era mechanisms now have explicit typed local equivalents without recreating the online queue/string transport internally.
- Regression coverage pins active layering, terminal emission, slot-order normalization, turn-drift rejection and invalid-command-identity rejection.
- **BATTLE_TYPED_EVENT_STATE_CONTRACT_R1 = IMPLEMENTED.**
- Next implementation seam: expose this transition directly through the single-player runtime battle-loop API, then define the first deterministic presentation/replay consumer above the contract without feeding presentation concerns back into battle rules.


## Phase 1 battle runtime typed handoff + replay consumer — 2026-09-28

- `SinglePlayerHistoricalRuntime.resolve_persistent_battle_transition()` now exposes the typed battle contract directly above the existing persistent round resolver.
- The new runtime API delegates to `resolve_persistent_battle_round()` first and only then converts its `PersistentRoundResult`; successful-capture persistence and all existing combat semantics therefore remain in the established rule path.
- Existing callers remain compatible because `resolve_persistent_battle_round()` is unchanged.
- Runtime handoff regression coverage added in `tests/test_stoneage_singleplayer_battle_transition_runtime.py`.
- First downstream deterministic consumer added in `tools/stoneage_battle_replay.py`:
  - immutable transition timeline;
  - strict before/after authoritative-state continuity;
  - no append after terminal state;
  - stable event-order flattening;
  - no damage/target/state recalculation and no historical protocol decoding.
- Replay regression coverage added in `tests/test_stoneage_battle_replay.py`.
- Contract record updated: `research/mechanics/STONEAGE-BATTLE-EVENT-CONTRACT-R1.md`.
- **BATTLE_RUNTIME_TYPED_HANDOFF_R1 = IMPLEMENTED.**
- **BATTLE_REPLAY_CONSUMER_R1 = IMPLEMENTED.**
- Presentation-specific animation/audio/UI mapping now stays downstream of typed events and is not allowed to become a second combat-rule layer.
- Next technical priority: perform a fresh Phase-1 deterministic-gap audit against the accepted foundation baseline and current engine-neutral models, then close the highest-value remaining gameplay/world semantic gap rather than continuing network-era transport reconstruction.


## Phase 1 typed battle contract CI closure — 2026-09-28

- Gameplay CI workflow `.github/workflows/validate-stoneage-tw10-gameplay-model.yml` now watches:
  - `tools/stoneage_battle_event_contract.py`;
  - `tools/stoneage_battle_replay.py`;
  - the three new contract/runtime-handoff/replay regression modules.
- The workflow's `python3 -m unittest` matrix now executes:
  - `tests.test_stoneage_battle_event_contract`;
  - `tests.test_stoneage_singleplayer_battle_transition_runtime`;
  - `tests.test_stoneage_battle_replay`.
- Validation run **36332961344 = PASS** on commit `e982d01fcaccf65e0ba0243afa37aa1aa1cd8182`.
- This closes the typed battle contract milestone at implementation + regression + CI level.
- Fresh deterministic-gap audit indicates battle transport/presentation should now leave the critical path. The strongest next Phase-1 implementation target is the **version/provenance-safe world-map content boundary**: the project already has a v1-direct map runtime format and 761 stable later-map candidates, but runtime map definitions still need an explicit engine-neutral provenance/version contract before later map content is admitted into the modern world.


## Phase 1 complete stable-later field-map lineage manifest — 2026-09-28

- The earlier derived `STONEAGE-TW10-FIELDMAP-LINEAGE-R1.txt` was intentionally sample-limited to 100 `STABLE_COMPATIBLE` detail rows even though its aggregate count declared 761 stable candidates. That sample was sufficient for research classification but was **not** a complete engine-ingestible candidate manifest.
- `.github/workflows/probe-stoneage-tw10-fieldmap-lineage.yml` now emits the full derived metadata surface and hard-validates the expected corpus closure:
  - shared valid paths = **995**;
  - same path + same SHA-256 = **980**;
  - changed SHA-256 = **15**;
  - same SHA-256 + Taiwan-v1 resource compatibility in both corpora = **761**;
  - emitted `STABLE_COMPATIBLE` detail rows = **761**;
  - emitted `CHANGED` rows = **15**.
- Actions run **36333127087 = PASS**. It recovered both already-verified source corpora transiently, compared them, validated the full counts, deleted transient proprietary payloads, and committed **derived metadata only**.
- Bot commit `93a0ff2c0e74b076bb8e6f7cb7e98f56c944a4f8` regenerated `research/recovered/STONEAGE-TW10-FIELDMAP-LINEAGE-R1.txt`; direct post-run inspection confirms the file itself contains **761** `STABLE_COMPATIBLE` rows and **15** `CHANGED` rows.
- `STABLE_LATER_MAP_CANDIDATE` therefore now has a complete path/dimension/hash metadata manifest for all 761 candidates rather than a 100-row sample.
- Evidence boundary is unchanged: stable later-lineage byte identity + Taiwan-v1 resource compatibility is **not** Taiwan-v1 historical membership.
- Next implementation seam: enforce the world-map provenance policy in engine-neutral code so later recovered maps, early-membership-proven maps, later-only resource maps and DESIGN reconstructed maps cannot be admitted to runtime topology under an ambiguous free-text evidence label.


## Phase 1 world-map provenance contract — 2026-09-28

- World-map provenance policy is now enforced in engine-neutral code:
  - `WorldMapProvenance` added to `tools/stoneage_singleplayer_world.py`;
  - complete lineage ingestion added in `tools/stoneage_world_map_library.py`;
  - regression coverage added in `tests/test_stoneage_world_map_library.py`.
- Concrete map content now has separate, validated axes for historical/content role and resource compatibility. In particular, `STABLE_LATER_MAP_CANDIDATE` is permitted only for `LATER_RECOVERED + V1_RESOURCE_COMPATIBLE` content supported by at least two source versions and a concrete payload SHA-256.
- Stable later candidates cannot be labeled `EARLY_MEMBERSHIP_PROVEN`; this directly encodes the project rule that later persistence + v1 asset compatibility does not prove Taiwan-v1 map membership.
- `HistoricalWorldTopology.from_provenance_maps()` is the strict modern-world ingestion boundary and rejects maps carrying only free-text evidence.
- The complete derived report parser rejects truncated/sample manifests whose emitted rows do not match declared counts.
- Repository-level regression reads the real committed lineage report and verifies:
  - **761** stable candidates;
  - **15** changed paths;
  - **761** strict topology maps;
  - zero implicit early-membership promotion.
- Gameplay-model Actions run **36333478060 = PASS** on the provenance-library CI integration.
- `research/clients/STONEAGE-WORLD-MAP-RECONSTRUCTION-POLICY-R1.md` now records the executable enforcement boundary.
- **WORLD_MAP_PROVENANCE_CONTRACT_R1 = IMPLEMENTED.**
- Next world-content seam: bind the provenance-safe map library to versioned world semantics (names, warps, NPC placements and encounter areas) without assuming that a later server/master-data row proves Taiwan-v1 membership. Prefer a deterministic cross-domain world-content manifest over ad hoc direct joins.


## Phase 1 versioned world-content manifest — 2026-09-28

- The complete 761-map stable-later library is now joined to the derived recovered-2.5 floor-level world-semantic coverage through `tools/stoneage_versioned_world_manifest.py`.
- The join is strict and engine-neutral:
  - map path, dimensions and payload SHA-256 must match the provenance-safe stable map manifest exactly;
  - per-floor world semantic coverage is tagged `source_version=recovered25` and `LATER_RECOVERED`;
  - recovered 2.5 NPC/warp/encounter coverage cannot promote any map to Taiwan-v1 membership;
  - a floor with zero recovered NPC and encounter rows is classified as a **semantic gap**, not asserted to be an historically empty map.
- Repository-level regression reads the real committed lineage and coverage reports and verifies the current recovered-2.5 coverage over 761 stable candidates:
  - stable with recovered server map = **572**;
  - stable with NPC semantics = **553**;
  - stable with Warp/WarpMan/FMWarpMan functionset presence = **544**;
  - stable with encounter semantics = **361**;
  - stable with both NPC and encounter semantics = **359**;
  - stable with neither currently recovered NPC nor encounter semantics = **206**.
- Main gameplay-model Actions run **36334349824 = PASS** for the real-report cross-domain manifest.
- `tools/stoneage_versioned_world_geometry.py` now defines the downstream typed geometry boundary and a conservative classic-Warp projection policy. Main gameplay-model Actions run **36334787061 = PASS** for that typed layer using deterministic fixtures.
- Full recovered-2.5 geometry extraction is still being validated separately before its counts are promoted to project facts.
- **VERSIONED_WORLD_CONTENT_MANIFEST_R1 = IMPLEMENTED.**
- Current highest-priority seam remains the full derived world-geometry closure: numeric NPC placement regions, classic overlap-Warp geometry and encounter rectangles, with WarpMan/FMWarpMan conditional/script behavior kept separate rather than flattened.


## Phase 1 versioned world-geometry closure — 2026-09-28

- Full recovered-2.5 numeric world geometry is now derived only from verified transient source bytes and committed as metadata in `research/recovered/STONEAGE-25-STABLE-WORLD-GEOMETRY-R1.txt`.
- Extraction deliberately excludes NPC names, template names, dialogue, arbitrary NPC arguments and map payload bytes. It retains only reconstruction-relevant numeric structure:
  - effective NPC create birth/move regions and basic spawn controls;
  - classic `functionset=Warp` source-region -> destination geometry;
  - encounter rectangles and numeric encounter envelope.
- NPC create geometry is accepted only when its floor exists in the recovered server-map set and is one of the 761 provenance-safe stable map candidates.
- Historical `getFourIntsFromString()` behavior was recovered and pinned: missing 3rd/4th `borncenter` fields are zero, so two-field `borncenter=x,y` means a single-cell region rather than malformed data.
- Full derived counts:
  - stable map candidates = **761**;
  - effective NPC placement blocks = **3,856**;
  - classic Warp edges = **2,264**;
  - classic Warp single-cell sources = **2,264**;
  - classic Warp edges with time condition = **5**;
  - classic Warp destinations inside stable candidates = **1,909**;
  - encounter areas = **402**.
- `WarpMan` / `FMWarpMan` and other conditional/scripted transport families are intentionally **not** flattened into classic overlap Warp edges.
- The typed engine-side parser `tools/stoneage_versioned_world_geometry.py` cross-checks geometry against the 761-map `VersionedWorldManifest` and requires per-floor NPC/encounter detail counts to match the recovered coverage manifest.
- Conservative executable classic-Warp projection:
  1. source must be a single cell;
  2. no unresolved time condition;
  3. destination must be in the stable candidate world;
  4. source and destination coordinates must be in bounds;
  5. source cell must have exactly one eligible edge.
- Of the 1,909 stable-destination classic Warp edges, **5** are time-conditional. The remaining **1,904** have valid source/destination coordinates. **52** source cells are ambiguous, covering **120** edges. Therefore **1,784** edges are currently safe for automatic deterministic projection into `HistoricalWorldTopology`.
- Full geometry derivation Actions run **36335051269 = PASS** and committed derived metadata only; transient proprietary payloads were deleted by the workflow.
- Main gameplay-model real-report integration run **36335179673 = PASS**; it rebuilds the 761-map versioned world manifest, parses all 3,856 placements / 2,264 classic warps / 402 encounter areas and constructs the 1,784-edge strict topology.
- Every concrete map and recovered semantic row remains versioned `LATER_RECOVERED`; none is promoted to Taiwan-v1 historical membership.
- **VERSIONED_WORLD_GEOMETRY_R1 = CLOSED.**
- Next deterministic world seam: bind the recovered encounter rectangles to the already reconstructed encounter/group/enemy resolver through an explicit versioned runtime adapter, while preserving the known recovered-2.5 dangling group-reference specimen defects as hard errors rather than silently repairing them.


## Phase 1 versioned encounter-runtime adapter — 2026-09-28

- `tools/stoneage_versioned_encounter_runtime.py` now binds the versioned stable-world encounter geometry to the existing strict `EncounterAreaBridge -> GroupBridge -> EnemyVariantBridge` resolver without duplicating encounter selection rules.
- The adapter requires every one of the **402** stable-world encounter rows to match recovered master data exactly on:
  - encounter index/floor;
  - rectangle;
  - encounter probability min/max;
  - enemy maximum;
  - z-order;
  - count of positively weighted group references.
- Recovered master semantics remain `source_version=recovered25 / LATER_RECOVERED`; the join does not promote server rows or concrete world population to Taiwan-v1 facts.
- Positive-weight missing group references are not dropped, reweighted or synthesized. They are retained as `UnresolvedPositiveGroupReference` specimen defects, and the existing resolver still raises a hard `KeyError` if runtime reaches an affected area.
- Full transient-source audit is committed as `research/recovered/STONEAGE-25-STABLE-ENCOUNTER-RUNTIME-R1.txt`.
- Stable-world integrity result:
  - stable encounter areas = **402**;
  - positively weighted unresolved group refs = **23**;
  - affected stable encounter areas = **19**;
  - distinct positively referenced groups = **469**;
  - missing enemy refs inside those existing referenced groups = **0**;
  - referenced groups affected by missing enemy refs = **0**.
- Thus the full recovered-2.5 specimen has 39 unresolved positive group refs across 32 rows, but the provenance-safe 761-map stable-world subset contains **23 refs across 19 encounter rows**. The remaining stable-world referenced group→enemy chain is complete at this integrity boundary.
- Adapter unit/integration behavior is locked in the main gameplay suite, including order-independent defect inventory and proof that an affected area hard-fails through the existing resolver rather than being repaired.
- Full source audit Actions run **36335679946 = PASS**; main gameplay real-report boundary run **36335789340 = PASS**.
- **VERSIONED_ENCOUNTER_RUNTIME_ADAPTER_R1 = CLOSED.**
- Next deterministic world seam: promote recovered NPC placement geometry into an engine-neutral versioned spawn catalogue (placement identity/region/count/direction only), while keeping NPC template behavior, dialogue and conditional function logic as separately versioned layers.


## Phase 1 versioned NPC spawn catalogue — 2026-09-28

- `tools/stoneage_versioned_npc_spawn_catalogue.py` now promotes the **3,856** recovered stable-world NPC create placements into an engine-neutral, provenance-bearing spawn catalogue.
- The catalogue intentionally contains only create-layer semantics:
  - floor + placement identity;
  - inclusive birth rectangle;
  - movement rectangle;
  - simultaneous population cap (`createnum`);
  - raw direction plus the fixed-descendant `VALIDATEDIR` modulo-8 projection;
  - respawn delay in milliseconds;
  - boundary flag;
  - invincible-area spawn override.
- NPC template identity/behavior, names, dialogue, arbitrary arguments and functionset logic remain outside this catalogue and are not silently imported.
- Fixed descendant source semantics were revalidated:
  - `createnum` is the maximum simultaneously alive population for a create block;
  - `time` is compared as milliseconds in the spawn throttle;
  - birth point selection is random within the inclusive born rectangle and is separately checked for map walkability/invincible-area conditions;
  - the generated character records its source `NPCCREATEINDEX`;
  - `VALIDATEDIR(x)` normalizes directional consumers to modulo 8, but create loading/generation first preserves the raw `dir` value in `CHAR_DIR`.
- Real recovered stable-world placement distribution:
  - placements = **3,856** across **553** stable-map floors;
  - every placement has `createnum=1`;
  - every placement has `boundary=1`;
  - all **3,856** birth rectangles are single-cell;
  - respawn delay distribution = **3,199 × 0 ms**, **642 × 60,000 ms**, **15 × 200,000 ms**;
  - `ignore_invincible=1` on **3,040**, `0` on **816**;
  - **3,854** birth points are inside the admitted stable-map dimensions;
  - **2** birth points are outside those current stable-map dimensions and are quarantined rather than repaired;
  - **3,772** movement rectangles lie fully inside map bounds, while **84** extend outside; this is retained as raw movement-bound metadata and is **not** treated as a spawn defect because actual movement remains map/collision constrained;
  - **2** raw direction values are outside 0..7 (`46` and `8`); both are preserved and quarantined for direct projection rather than normalized in-place.
- Direct modern-runtime projection policy blocks only:
  - birth rectangles outside the admitted stable map;
  - non-octant raw directions;
  - create rows whose population cap/respawn gate disables generation.
- Current result: **3,852 / 3,856** placements are direct-projection eligible; **4** are quarantined with explicit issue codes. No source row is deleted or modified.
- Main gameplay-model Actions run **36362411761 = PASS** over the real lineage + coverage + geometry reports.
- Every placement remains `source_version=recovered25 / LATER_RECOVERED`; none is promoted to Taiwan-v1 historical membership.
- **VERSIONED_NPC_SPAWN_CATALOGUE_R1 = CLOSED.**
- Next deterministic NPC seam: bind spawn placements to an anonymous/versioned NPC template identity layer without importing dialogue or assuming later template behavior existed unchanged in Taiwan v1. The identity join must preserve template/functionset provenance and keep conditional behavior as a separate layer.


## Phase 1 anonymous/versioned NPC template identity — 2026-09-28

- Stable-world NPC spawn placements are now joined to an **anonymous recovered template-name identity namespace** without publishing template names, NPC names, dialogue, concrete arguments or original source rows.
- Transient-source derivation:
  - `tools/stoneage_versioned_npc_template_binding_probe.py`;
  - `research/recovered/STONEAGE-25-STABLE-NPC-TEMPLATE-BINDINGS-R1.txt`.
- Engine-side contract:
  - `tools/stoneage_versioned_npc_template_binding.py`.
- Anonymous identity key is a deterministic SHA-256 over the case-normalized template-name namespace. It is an opaque join key, not a published template name.
- Duplicate template-name definitions remain **load-order ambiguous**. The reconstruction does not select a concrete duplicate block merely because the analysis traversal happens to encounter one first.
- Real stable-world result:
  - placement bindings = **3,856**;
  - unique referenced anonymous template identities = **73**;
  - placements whose template name is unique = **3,853**;
  - placements referencing duplicate template-name identities = **3**;
  - referenced duplicate anonymous identities = **3**;
  - placements with functionset ambiguity across duplicate variants = **0**.
- The 3 duplicate-name placement bindings are:
  - placement **2512**: 4 concrete variants, common functionset `Quiz`;
  - placement **3539**: 3 concrete variants, common functionset `transmigration`;
  - placement **3634**: 2 concrete variants, common functionset `TranserMan`.
  Functionset agreement does **not** make the concrete template block unique; these remain duplicate-name identity ambiguities.
- Classic Warp integrity cross-check:
  - classic-Warp geometry placements = **2,264**;
  - all **2,264** have `Warp` as the template-name identity's functionset consensus;
  - duplicate-template ambiguity affects **0** classic-Warp placements;
  - therefore the previously closed classic-Warp geometry/runtime projection is not contaminated by recovered duplicate-template load-order ambiguity.
- Combining the spawn-catalogue quarantine with concrete-template uniqueness leaves **3,850 / 3,856** placements eligible for direct spawn + concrete anonymous identity projection. Six unique placement IDs are held back across the two independent integrity gates.
- Full transient-source binding workflow **36362658876 = PASS**; main gameplay real-report parser/integration run **36362804605 = PASS**.
- All identities, bindings and functionset consensus remain `recovered25 / LATER_RECOVERED`; none implies Taiwan-v1 content membership.
- **ANONYMOUS_NPC_TEMPLATE_IDENTITY_R1 = CLOSED.**
- Next deterministic NPC seam: derive anonymous **non-text template runtime profiles** keyed by the 73 identities (type/graphic/stat ranges/generation flags/loop timing and similar structural fields), while keeping display names, dialogue, opaque arguments and function-specific secondary content excluded and keeping duplicate concrete variants explicit.


## Phase 1 anonymous NPC template runtime profiles — 2026-09-28

- `tools/stoneage_versioned_npc_template_profile_probe.py` now derives non-text runtime structure for every anonymous template identity referenced by the 3,856 stable-world spawn placements.
- Committed derived metadata: `research/recovered/STONEAGE-25-STABLE-NPC-TEMPLATE-PROFILES-R1.txt`.
- Engine-side parser/contract: `tools/stoneage_versioned_npc_template_profile.py`.
- The profile layer deliberately excludes template names, NPC display names, dialogue, callback names, create arguments, item payload rows and original recovered source rows.
- Fixed-descendant template semantics were revalidated:
  - `hp/mp/str/tough=a,b` is represented as normalized min/max because the loader stores the lower value plus an absolute random width;
  - `makeatnobody`, `makeatnosee`, `fly` and `loopfunctime` are direct structural values;
  - missing `graphicname` retains the template default zero;
  - missing `type` is normalized by the fixed loader to `SPR_pet001` at block close;
  - numeric graphic/type tokens are direct integers;
  - symbolic graphic/type tokens are kept as opaque SHA-256 identities in R1 rather than assuming one descendant source's conversion table is canonical for the recovered 2.5 data.
- Real stable-world profile result:
  - referenced anonymous identities = **73**;
  - recovered source profile rows = **79**;
  - identities with multiple source definitions = **3**;
  - distinct normalized source-block fingerprints = **73**;
  - direct callback override count = **0 on all 79 profiles**;
  - graphic resolution: **49 default-zero**, **7 numeric**, **23 opaque-symbolic**;
  - type resolution: **32 default-SPR_pet001**, **40 numeric**, **7 opaque-symbolic**;
  - profiles with any symbolic graphic/type token = **30**;
  - all **79** have `makeatnobody=1`, `makeatnosee=1`, and `fly=0`;
  - loop interval distribution = **76 × -1**, **3 × 4000 ms**.
- The three duplicate-name identities are source/provenance duplicates but **runtime-byte-equivalent**:
  - Quiz: 4 source variants, one block fingerprint;
  - transmigration: 3 source variants, one block fingerprint;
  - TranserMan: 2 source variants, one block fingerprint.
  The project therefore preserves the duplicate-name provenance fact while permitting a runtime-equivalent profile representative; no load-order-dependent behavioral difference is asserted where the source bytes are identical.
- With runtime-equivalent duplicate handling, **all 3,856 template bindings have an unambiguous generic runtime profile**. Combined with the spawn-catalogue geometry/direction gate, **3,852 / 3,856** placements are eligible for generic runtime projection; only the four previously quarantined spawn rows remain blocked.
- Full transient-source profile derivation Actions run **36363004589 = PASS**; main gameplay real-report parser/integration run **36363313244 = PASS**.
- All profile data remains `recovered25 / LATER_RECOVERED`; no template profile is promoted to Taiwan-v1 historical membership.
- **ANONYMOUS_NPC_TEMPLATE_RUNTIME_PROFILE_R1 = CLOSED.**
- Next deterministic NPC seam: compose spawn placement + anonymous runtime-equivalent template profile into an engine-neutral **generic NPC spawn intent** that can feed the existing in-process NPC runtime boundary without importing display text or executing function-specific secondary content. Symbolic graphic/type tokens must remain unresolved/quarantined until a provenance-safe token resolver exists.


## Phase 1 generic versioned NPC runtime spawn projection — 2026-09-28

- `tools/stoneage_versioned_npc_runtime_projection.py` now composes the recovered-later NPC layers into one engine-neutral generic runtime intent:
  `spawn placement -> anonymous template identity -> runtime-equivalent template profile -> generic spawn intent`.
- The intent remains deliberately earlier than function-specific INITFUNC behavior and presentation:
  - it does **not** invent NPC display names;
  - it does **not** execute functionset-specific secondary content;
  - it does **not** infer the post-INITFUNC world object type;
  - it does **not** coerce opaque graphic/type tokens into guessed numeric IDs.
- Every one of the **3,856** stable-world placements now has a generic runtime intent. All current recovered born rectangles are single-cell, so every intent has a deterministic recovered birth coordinate before collision/invincible-area acceptance.
- Spawn integrity remains independently enforced:
  - **3,852 / 3,856** intents pass the existing stable-map birth/direction/generation gate;
  - the same four source rows remain quarantined and are not repaired.
- Graphic resolution weighted by actual placements:
  - intrinsically resolved graphic (default zero or numeric) = **2,976 / 3,856**;
  - spawn-safe + intrinsically resolved graphic = **2,974**;
  - opaque symbolic graphic = **880** total / **878** spawn-safe.
- Type selector weighted by actual placements:
  - opaque symbolic type = **89**;
  - the remainder are either numeric or the recovered template default semantic `SPR_pet001`.
- Symbolic graphic or type affects **969** placements total / **967** spawn-safe placements. These stay explicitly unresolved until a provenance-safe token resolver exists.
- The in-process historical domain now accepts both:
  - legacy `npc.templatename` identities; and
  - anonymous `npc.template.sha256` identities.
  This lets a generic intent feed the existing `NpcRuntimeState -> WorldNpc -> SinglePlayerHistoricalDomain.place_npc()` boundary after the caller explicitly supplies:
  - display text from a presentation layer;
  - functionset/INITFUNC-dependent object type;
  - and, only when needed, a provenance-resolved graphic ID.
- A symbolic graphic cannot materialize silently: `resolved_graphic_id` is mandatory. Quarantined spawn rows cannot materialize at all.
- Anonymous template SHA identities remain visible only as reconstruction identifiers; they are not claimed to be historical template-name strings.
- Main gameplay integration Actions:
  - anonymous-namespace domain compatibility **36363544440 = PASS**;
  - full real-report generic spawn projection **36363581367 = PASS**.
- **GENERIC_VERSIONED_NPC_RUNTIME_SPAWN_PROJECTION_R1 = CLOSED.**
- Next deterministic NPC seam: build a provenance-safe resolver for the small recovered symbolic graphic/type token set. First compare token-to-ID mappings across fixed descendant source families and recovered client/resource evidence; only mappings that are stable enough for the intended version boundary may be promoted. Otherwise retain the opaque token and require explicit design/runtime resolution.


## Phase 1 symbolic NPC graphic/type provenance audit — 2026-09-28

- The generic NPC runtime projection has only **4 distinct anonymous symbolic graphic/type token identities** left:
  - 3 graphic-token identities covering **880** placement uses;
  - 1 type-token identity covering **89** placement uses.
- The repository now contains two independent provenance checks:
  - `research/recovered/STONEAGE-25-STABLE-NPC-SYMBOL-RESOLUTION-R1.txt`: raw recovered token strings are used transiently and compared against the project's pinned fixed descendant animation tables; only anonymous SHA-256 token identities and numeric mapping evidence are retained.
  - `research/recovered/STONEAGE-25-RUNTIME-GRAPHIC-MAPPING-R1.txt`: the verified recovered-2.5 preservation bundle is scanned for an actual runtime `ls2data.dat` count + name/id mapping file, again retaining only anonymous token hashes and numeric IDs.
- Fixed-source symbol audit result: none of the four recovered opaque token identities obtains a safe fixed-source bridge under the current pinned source evidence.
- Verified recovered-bundle runtime result:
  - parseable runtime mapping files = **0**;
  - opaque token identities = **4**;
  - `RECOVERED25_MAPPING_ABSENT` = **4**;
  - unresolved graphic placement uses = **880**;
  - unresolved type placement uses = **89**.
- This explicitly distinguishes **missing preservation evidence** from an invalid token. The project does not coerce these aliases to guessed SPR IDs.
- Taiwan-v1 SPR metadata remains a resource-compatibility validator only; numeric resource presence by itself would not prove that a recovered-2.5 symbolic token name belonged to Taiwan v1.
- Full symbol-provenance world-content workflow **36364230560 = PASS**.
- Full recovered-runtime-mapping audit workflow **36364479121 = PASS**.
- The evidence boundary is hard-locked in workflow **36364806935 = PASS**: the current verified bundle must continue to report 0 runtime mapping files and all 4 token identities unresolved, so newly recovered mapping evidence cannot change the result silently.
- **SYMBOLIC_NPC_GRAPHIC_TYPE_PROVENANCE_AUDIT_R1 = CLOSED_WITH_EXPLICIT_EVIDENCE_GAP.**
- Runtime policy remains unchanged: opaque graphic placements require an explicit provenance-resolved `resolved_graphic_id`; no guessed mapping is admitted.

## Phase 1 placement-weighted NPC behavior coverage — 2026-09-28

- `tools/stoneage_versioned_npc_behavior_coverage.py` now projects the **3,856** stable-world NPC placements onto the project's existing NPC-core closure/defer registry.
- This is a coverage layer only: it does not reimplement functionsets, execute secondary argument content, or promote recovered-2.5 behavior to Taiwan-v1 membership.
- Stable-world placement-weighted result:
  - **3,710** placements -> `CLOSED_ORDINARY_CORE`;
  - **84** placements -> `NO_DISPATCH_PROFILE`;
  - **62** placements -> `DEFERRED_VERSIONED_PACKAGE`;
  - **0** placements -> `UNCLASSIFIED`.
- The 84 `<none>` functionset placements are not assumed inert from the token alone. Their anonymous runtime profiles are cross-checked and all have **zero direct callback overrides**, so they are explicitly classified as no-dispatch generic profiles.
- The 62 deferred placements are confined to already-deferred family/later/versioned classes:
  `Familyman`, `FmDengon`, `FmHealer`, `FmLetter`, `FMPKCallMan`, `FMPKMan`, `FMWarpMan`, `Raceman`, `Scheduleman`, and `TranserMan`.
- Therefore **3,794 / 3,856** recovered stable-world placements are now covered by either an already reconstructed ordinary core or an explicitly verified no-dispatch profile. The remaining 62 are known deferred packages rather than unidentified behavior holes.
- Main gameplay-model integration run **36364968527 = PASS**.
- **VERSIONED_NPC_BEHAVIOR_COVERAGE_R1 = CLOSED.**
- Priority consequence: ordinary NPC-core archaeology is no longer the critical path. Keep the four symbolic graphic/type aliases and 62 later/family placements explicit, but return primary effort to provenance-safe client/world-content reconstruction instead of reopening already closed NPC mechanics.

## Phase 1 versioned-world recovered-name overlay — 2026-09-29

- The stable-world map-name decode report is now consumed by an engine-neutral, provenance-safe semantic overlay: `tools/stoneage_versioned_world_names.py`.
- The overlay binds name evidence only after cross-domain validation against the existing `VersionedWorldManifest`:
  - stable world floors = **761**;
  - floors with dimension-matched recovered server-map name evidence = **572**;
  - conflict-free recovered name-text rows = **571**;
  - unresolved name rows = **1**;
  - floors with no recovered name evidence = **189**;
  - floors without a conflict-free recovered name = **190**.
- The evidence-floor set is required to equal the manifest's existing `server_map_present` floor set exactly. Unknown floors, missing server-map floors, extra name floors, count drift, source-version drift and truncated reports are rejected rather than tolerated.
- Floor **31001** remains explicitly unresolved because the recovered server copies disagree between `加特洛的洞窟１樓|0` and `加都洛的洞窟１樓|0`. No candidate is selected automatically.
- Recovered strings such as `薩姆吉爾的武器店|0` intentionally preserve the legacy `|0` suffix. The project currently treats this as **recovered name text**, not a presentation-cleaned display label; stripping/interpreting the suffix would require separate evidence.
- Every name row remains `SEMANTIC_SOURCE_VERSION=recovered25` / `LATER_RECOVERED`. The overlay cannot promote recovered-2.5 text into Taiwan-v1 membership or naming evidence.
- Full gameplay-model regression including the new overlay tests: GitHub Actions **36503374942 = PASS**.
- **VERSIONED_WORLD_RECOVERED_NAME_OVERLAY_R1 = CLOSED.**
- Next deterministic world-content seam: use the conflict-free recovered name text to annotate world/warp diagnostics and graph inspection while preserving source-version provenance. Do **not** turn these strings into canonical UI labels or Taiwan-v1 names until earlier-version/client evidence independently supports that promotion.

## Phase 1 recovered-name warp-graph diagnostics — 2026-09-29

- The 2,264 recovered classic `Warp` edges are now joined read-only to the provenance-safe recovered-name overlay in `tools/stoneage_versioned_world_warp_names.py`.
- This layer does **not** modify warp behavior, clean recovered text into UI labels, select conflicting names, or promote recovered-2.5 semantics into Taiwan-v1 evidence.
- Placement-weighted classic-warp name coverage:
  - total classic warp edges = **2,264**;
  - source name resolved = **2,261**;
  - source name unresolved = **3**;
  - destination name resolved = **1,908**;
  - destination name unresolved = **1**;
  - destination outside the current 761-floor stable-world candidate set = **355**;
  - resolved -> resolved edges = **1,907**;
  - resolved -> outside-stable-world edges = **353**;
  - unresolved -> outside-stable-world edges = **2**;
  - unresolved -> resolved edges = **1**;
  - resolved -> unresolved edges = **1**;
  - distinct source/destination floor pairs = **985**.
- Example only as recovered diagnostic text: the heavily repeated `3021 -> 3022` edge can now be inspected as `百人聯手道場|0 -> 加加的道場醫務室|0` while retaining both floor IDs and recovered25 provenance.
- Floor **31001** remains conflict-preserving: any warp touching it reports the corresponding name state as unresolved and exposes no selected text.
- Full gameplay-model regression including the new warp/name diagnostic tests: GitHub Actions **36503610189 = PASS**.
- **VERSIONED_WORLD_WARP_NAME_DIAGNOSTICS_R1 = CLOSED.**
- Next deterministic world-topology seam: classify the **355 classic-warp edges whose destinations are outside the current 761 stable map candidates**. Determine whether those destination floors are present in other recovered map generations/corpora, later-only content, duplicate/changed map rows, or genuinely missing payloads. Do not synthesize destination maps or assume absence means invalid warp.

## Phase 1 outside-stable warp destination corpus closure — 2026-09-29

- The **355** classic-`Warp` edges whose destinations fall outside the 761-floor stable-world candidate set are now classified directly against the hash-verified recovered-2.5 client DAT corpus by `tools/stoneage_warp_destination_corpus_probe.py`.
- Those 355 edges reference only **30 distinct destination floor IDs**:
  - **13 IDs / 283 edges** are `CHANGED`: the same map path exists in recovered-2.5 and archived-2003 but the bytes differ across those later corpora;
  - **13 IDs / 68 edges** are `SAME_SHA_NONSTABLE`: the recovered-2.5 DAT exists and persists byte-identically across the later lineage, but it is not in the provenance-safe Taiwan-v1-compatible stable subset;
  - **4 IDs / 4 edges** are `CLIENT_DAT_MISSING`: floors **20002, 20004, 20006, 20009**.
- Among the 26 destination IDs with recovered-2.5 DAT payloads, **6 IDs / 98 edges** are Taiwan-v1 resource-ID compatible and **20 IDs / 253 edges** are not. This remains necessary-not-sufficient asset compatibility only and is **not** Taiwan-v1 membership evidence.
- The four missing-DAT IDs form one coherent recovered warp cluster rather than unrelated errors:
  - `20001 -> 20002`;
  - `20005 -> 20004`;
  - `20005 -> 20006`;
  - `20010 -> 20009`.
  Their source recovered texts are `拉多拉山嶺洞窟１樓|0`, `拉多拉山嶺洞窟５樓|0`, and `拉多拉山嶺洞窟１０樓|0`.
- Independent historical-map evidence agrees with the client-DAT gap: the archived 2003 `map.exe` inventory contains `20001.dat`, `20005.dat`, and `20010.DAT`, but not 20002/20004/20006/20009.
- A second direct payload-surface audit, `tools/stoneage_missing_warp_destination_payload_probe.py`, closes the four apparent gaps:
  - all **4 IDs / 4 edges** are `SERVER_MAP_ONLY`;
  - recovered-2.5 client `.MAP` present = **0/4**;
  - recovered-2.5 server LS2MAP present = **4/4**;
  - floor 20002: `jyaruga/dungeon/dan_2-00-02`, **50x100**;
  - floor 20004: `jyaruga/dungeon/dan_2-00-04`, **80x80**;
  - floor 20006: `jyaruga/dungeon/dan_2-00-06`, **80x40**;
  - floor 20009: `jyaruga/dungeon/dan_2-00-09`, **100x100**.
- The first verification initially used an incorrectly escaped regex and therefore did not reject the unexpected four DAT-missing rows. That verification defect was corrected to exact evidence locks plus literal guards; the corrected end-to-end world-content run **36504358575 = PASS** and generated the committed second-stage report.
- **OUTSIDE_STABLE_WARP_DESTINATION_CORPUS_R1 = CLOSED.**
- **MISSING_DAT_WARP_DESTINATION_PAYLOAD_SURFACES_R1 = CLOSED.**
- Next deterministic seam: determine how the classic client enters/renders these **server-only LS2MAP** floors. Audit the client/server map-transfer and map-transition protocol before deciding how the single-player reconstruction should materialize them. Do not synthesize client DAT/MAP payloads merely because the server copy exists.

## Phase 1 server-authoritative runtime map materialization — 2026-09-29

- The classic map-delivery seam is now closed across direct Taiwan-v1 client evidence and a fixed descendant server control, with the evidence classes kept separate in `research/mechanics/STONEAGE-MAP-DELIVERY-MATERIALIZATION-R1.md`.
- **Taiwan-v1 direct runtime FACT**:
  - the accepted retail-disc tree contains no ordinary preinstalled field-map/cache files;
  - the v1 runtime has create/read/write/update paths for `map\\%d.dat`;
  - client -> server `M` is a floor + rectangle request;
  - server -> client `M` is floor + rectangle + map payload;
  - server -> client `MC` adds tile/object/event checksum/control fields;
  - v1 `M` receive reaches the writable cache path and v1 `MC` reaches the read/check/create-if-missing path.
- **Pinned descendant CONTROL** (`BismarckDD/Stoneage@999ffdf1d220ec6666eb65339180689c9caf1876`) closes the server-side semantic loop without being promoted to launch-era proof:
  - `GmsvServer_M_recv` accepts the requested rectangle and calls `MAP_getdataFromRECT`;
  - `MAP_getdataFromRECT` clips against the authoritative server floor and serializes map display data plus tile/object/event planes;
  - `GmsvServer_M_send` returns that rectangle;
  - descendant `MC` sends region checksum/control data, and the client requests `M` when its cache disagrees;
  - descendant walking code incrementally checks newly exposed map strips rather than requiring one monolithic preinstalled client map.
- Therefore the durable reconstruction boundary is **authoritative map state -> runtime map materialization**, not the historical socket transport.
- `tools/stoneage_map_delivery_model.py` now models the transport-independent semantic contract:
  - MC/check match -> accept cached/internal region;
  - MC/check mismatch -> request/materialize the same region;
  - M/payload -> materialize the rectangle;
  - server-only recovered floors -> local engine-neutral materialization plans with no network requirement and no fabricated historical client-file claim.
- The real four-floor payload report is regression-bound into that model:
  - 20002 = 50x100;
  - 20004 = 80x80;
  - 20006 = 80x40;
  - 20009 = 100x100;
  - all remain `LATER_RECOVERED`;
  - all materialize under `SERVER_AUTHORITY_INTERNAL_MAP`;
  - no legacy cache file is required by the modern single-player runtime.
- A provenance-promotion regression test explicitly rejects an input that relabels these rows as `EARLY_MEMBERSHIP_PROVEN`.
- DD-014 records the production rule: preserve the authoritative-map/materialization semantics, but do not reproduce obsolete networking merely to emulate historical transport. Any future legacy `map\\%d.dat` compatibility cache must be labeled derived/transient rather than original evidence.
- Full gameplay-model regression including the materialization model: GitHub Actions **36505111919 = PASS**.
- **SERVER_AUTHORITY_RUNTIME_MAP_MATERIALIZATION_R1 = CLOSED.**
- Next deterministic world-content seam: audit gameplay/content coverage **inside the four server-only floors**. Their terrain can now be materialized, but they must not enter the reconstructed world as dead-end geometry if their NPC, classic Warp, encounter or exit content was excluded by the current 761-floor stable-world filter.

## Phase 1 server-only floor gameplay closure — 2026-09-29

- The four recovered `SERVER_MAP_ONLY` warp targets are now audited directly against the full recovered-2.5 NPC/create and active encounter corpora by `tools/stoneage_server_only_floor_gameplay_probe.py`.
- Corrected end-to-end world-content run **36505538394 = PASS**. An earlier run (**36505383481**) failed only in the new unit-test stage because absent encounter counts were indexed as a normal dict instead of defaulting to zero; no preservation payload was downloaded in that failed attempt. The probe was corrected so an absent encounter-floor entry is explicitly `0`.
- All four floors have recovered gameplay semantics:
  - **20002**: 2 effective NPC creates, both classic Warp; exits to `20001 @ 11,40` and `20003 @ 34,25`;
  - **20004**: 2 effective NPC creates, both classic Warp; exits to `20003 @ 57,44` and `20005 @ 27,3`;
  - **20006**: 2 effective NPC creates, both classic Warp; exits to `20005 @ 56,85` and `20007 @ 74,6`;
  - **20009**: 2 effective NPC creates, both classic Warp; exits to `20008 @ 69,37` and `20010 @ 6,59`.
- Aggregate coverage:
  - target floors = **4**;
  - effective NPC creates = **8**;
  - Warp-functionset creates = **8**;
  - parsed classic Warp edges = **8**;
  - floors with NPC semantics = **4/4**;
  - floors with classic Warp semantics = **4/4**;
  - encounter rows = **0**;
  - active encounter rows = **0**.
- This closes the concern that materializing the server-only floors would create topology-only dead ends. They are recovered transit floors with bidirectional/adjacent-floor portal semantics and no recovered random-encounter rows.
- The evidence remains `SEMANTIC_SOURCE_VERSION=recovered25` / `LATER_RECOVERED`; none of these four floors is promoted into Taiwan-v1 historical membership.
- **SERVER_ONLY_FLOOR_GAMEPLAY_COVERAGE_R1 = CLOSED.**
- Next deterministic seam: decode the four LS2MAP payloads into an engine-neutral map representation suitable for the local single-player world. Reuse the already established client/server map relation and collision semantics; preserve original server-map hashes/metadata, but commit only derived non-proprietary structure needed for validation.

## Phase 1 server-only static map materialization — 2026-09-29

- The four first-wave `SERVER_MAP_ONLY` warp targets are now decoded into the engine-neutral static collision boundary by `tools/stoneage_server_static_map.py`.
- Direct recovered LS2MAP format used by the model:
  - 44-byte header;
  - embedded 16-bit floor ID;
  - 16-bit width/height;
  - full big-endian 16-bit tile plane;
  - full big-endian 16-bit object plane.
- The recovered server `mapset.txt` is parsed with the stable descendant loader's relevant column semantics: image ID at token 1, `WALKABLE` at token 4, `HAVEHEIGHT` at token 5, source defaults when omitted, and last-definition-wins duplicate behavior. Missing image metadata is never guessed.
- Corrected end-to-end world-content run **36507457038 = PASS**.
- Recovered `mapset.txt` identity and coverage:
  - SHA-256 = `efc0b793c901509e6387697c6b2c2a706bd7b9a2af09f1260b592566299cc7a6`;
  - rows = **20,157**;
  - unique image IDs = **20,157**;
  - duplicate image IDs = **0**.
- Across the four server-only maps:
  - total cells = **24,600**;
  - floors with missing image metadata = **0/4**;
  - ordinary walkable cells = **7,534**;
  - ordinary blocked cells = **17,066**;
  - flying walkable cells = **24,600**;
  - flying blocked cells = **0**.
- Floor identities are now hash-locked:
  - 20002 — 50x100, ordinary walkable 1,675 / 5,000, SHA-256 `c18dc72b8cb3e3d0e5ad2b881905f4709ea5a854ec480ac49cfd53c2dcfb6948`;
  - 20004 — 80x80, ordinary walkable 2,132 / 6,400, SHA-256 `7b7c401c64125556fe9037a207a42c54bb6d3880d969ee692305ca9354a326d9`;
  - 20006 — 80x40, ordinary walkable 1,053 / 3,200, SHA-256 `cdc77c1896ef42dbd7e0b681840b2709381cac41e218c42017c7bab6176fc360`;
  - 20009 — 100x100, ordinary walkable 2,674 / 10,000, SHA-256 `5779c3b8cf102130e187c008af5f63eadaad70bec2e7ff40ca295cd1fe7e66cb`.
- The recovered server loader itself rejects LS2MAP tile/object IDs absent from its map-image metadata table; the project's zero-missing-metadata gate therefore preserves an original validity condition rather than inventing a new one.
- All content remains `recovered25 / LATER_RECOVERED`; static materializability does not prove Taiwan-v1 membership.
- **SERVER_ONLY_STATIC_MAP_MATERIALIZATION_R1 = CLOSED.**
- New topology consequence: first-wave supplemental floors expose destinations **20003, 20007, 20008**, which are not in the current stable-world manifest. The next priority is a recursive reachable-world closure, not a fixed four-floor patch.

## Phase 1 runtime-valid recovered world reachability closure — 2026-09-29

- The recovered-2.5 classic-Warp graph is now expanded recursively from all **761** stable later-map candidates by `tools/stoneage_recovered_world_reachability_probe.py`.
- The first syntax-only pass produced 67 supplemental floors, including floor 40. That was intentionally **not** accepted as the runtime result because the already-closed classic Warp rule requires `MAP_IsValidCoordinate(floor,x,y)` during initialization and again before execution.
- The probe was tightened so a Warp edge is traversable only when:
  - the destination floor has a recovered server LS2MAP; and
  - the destination coordinate is inside at least one recovered server-map copy for that floor.
- Corrected runtime-valid world-content run **36508451472 = PASS**.
- Runtime-valid closure:
  - stable seed floors = **761**;
  - reachable floor IDs including seeds = **827**;
  - supplemental reachable floor IDs = **66**;
  - maximum supplemental depth = **23**;
  - syntactically parseable classic Warp edges from server-backed sources = **2,903**;
  - runtime-valid server-source classic Warp edges = **2,899**;
  - runtime-valid Warp edges encountered from the reachable closure = **2,830**.
- Supplemental floor provenance/status:
  - **14** = `CHANGED`;
  - **45** = `CLIENT_DAT_PRESENT_NONSTABLE`;
  - **7** = `SERVER_ONLY`;
  - **0** runtime-reachable supplemental floors lack a server map.
- The seven recursively reachable server-only floors are exactly:
  **20002, 20003, 20004, 20006, 20007, 20008, 20009**.
  The first four discovered earlier were therefore only the first wave; the recursive closure correctly adds 20003/20007/20008.
- Floor 40 is **not** runtime reachable under the recovered server state. Four syntactic Warp rows target it:
  - 6000 -> 40 @ 6,3;
  - 31301 -> 40 @ 12,1;
  - 31401 -> 40 @ 1,9;
  - 31501 -> 40 @ 11,18.
  All four are classified `NO_SERVER_MAP` and excluded from BFS traversal.
- The long supplemental chains around floors 800–831 and 840–850 account for the deep **23-hop** reachability and demonstrate why one-hop outside-stable classification was insufficient.
- Every supplemental node remains `recovered25 / LATER_RECOVERED`. Runtime reachability does not promote a floor into Taiwan-v1 membership.
- **RECOVERED25_RUNTIME_CLASSIC_WARP_REACHABILITY_R1 = CLOSED.**
- Next deterministic seam: construct a provenance-safe **supplemental world extension** for the 66 runtime-reachable later floors while leaving the 761-floor stable manifest unchanged. First audit server-map copy uniqueness, payload hashes/dimensions, mapset collision closure, and floor-level gameplay coverage for all 66 nodes; do not select among divergent duplicate server copies without evidence.

## Phase 1 runtime-reachable supplemental world audit — 2026-09-29

- The **66** recovered25 floors reached beyond the 761-floor stable seed manifest are now audited as an independent supplemental layer by `tools/stoneage_supplemental_world_audit_probe.py`.
- End-to-end world-content run **36594645500 = PASS** and committed `research/recovered/STONEAGE-25-SUPPLEMENTAL-WORLD-AUDIT-R1.txt`.
- Server-map copy identity:
  - **65** supplemental floors have exactly one recovered server-map copy;
  - **0** have multiple byte-identical copies;
  - **1** has divergent duplicate server copies: floor **130**.
- Floor **130** is deliberately unresolved:
  - `extra/130`, 60x60, SHA-256 `b62fca539743b5ac91f38b344e34e4655a287d4e71582d8e3547c83fc0ee8fa2`;
  - `family/130`, 60x60, SHA-256 `8f6e5e1983830694f090decbb32417ea1b6ba3ac0f61953495a910d513e2fe7d`;
  - both share the same embedded floor ID and dimensions but differ in payload bytes;
  - no copy is selected automatically, so its static collision/materialization fields remain unknown.
- Static map closure for the other **65** floors:
  - static-materializable floors = **65**;
  - unresolved floors = **1**;
  - floors with missing mapset image metadata among materialized floors = **0**;
  - materialized cells = **2,972,075**;
  - ordinary walkable cells = **885,753**;
  - flying walkable cells = **2,972,075**.
- Supplemental gameplay coverage is substantial rather than topology-only:
  - floors with effective NPC semantics = **66/66**;
  - floors with Warp-functionset semantics = **66/66**;
  - effective NPC creates = **1,042**;
  - Warp-functionset creates = **668**;
  - floors with encounter rows = **50/66**;
  - floors with active encounter rows = **50/66**;
  - encounter rows = **247**, all **247** active.
- The audit preserves each floor's reachability depth/status plus recovered server path, SHA-256, dimensions, collision closure, and derived gameplay counts, while retaining `recovered25 / LATER_RECOVERED`.
- **RECOVERED25_SUPPLEMENTAL_WORLD_AUDIT_R1 = CLOSED.**
- Next deterministic seam: construct an engine-neutral supplemental-world manifest that references the 761-floor stable manifest without mutating it. The extension may expose **65 resolved/materializable supplemental floors** plus **1 unresolved duplicate-copy floor (130)**, but must never silently select a floor-130 payload or promote any supplemental floor into Taiwan-v1 membership.

## Phase 1 provenance-safe supplemental world manifest — 2026-09-29

- `tools/stoneage_supplemental_world_manifest.py` now consumes the closed 66-floor supplemental audit as a separate engine-neutral extension over the existing stable `VersionedWorldManifest`.
- The stable manifest remains immutable in scope:
  - stable floors = **761** before and after extension construction;
  - no supplemental floor may overlap or replace a stable floor ID.
- Supplemental state is represented explicitly as:
  - resolved/materializable supplemental floors = **65**;
  - unresolved supplemental floors = **1** (floor **130**);
  - total runtime-reachable floor IDs represented = **827**;
  - map definitions safe to materialize today = **826**.
- Every resolved supplemental map definition:
  - remains `LATER_RECOVERED`;
  - uses `RESOURCE_RELATION_UNKNOWN` rather than claiming Taiwan-v1 resource compatibility;
  - carries only recovered25 as its source version;
  - binds the server LS2MAP SHA-256 from the supplemental audit;
  - cannot claim early historical membership.
- Floor 130 is represented as an unresolved candidate set, not a map definition. Its two server paths, dimensions and divergent SHA-256 values are preserved, and `materializable_map_topology()` excludes it.
- Regression tests explicitly reject:
  - promotion of the supplemental audit to `EARLY_MEMBERSHIP_PROVEN`;
  - silent materialization of a `DUPLICATE_DIVERGENT` floor;
  - any overlap that would replace a stable-world map.
- Full gameplay-model regression including the supplemental manifest: GitHub Actions **36595225971 = PASS**.
- **RECOVERED25_SUPPLEMENTAL_WORLD_MANIFEST_R1 = CLOSED.**
- Next deterministic seam: resolve or intentionally preserve the floor-130 duplicate-copy conflict. Stable descendant server code is last-loaded-wins for duplicate floor IDs, but recursive file enumeration uses unsorted `readdir()`; path-name ordering therefore cannot establish the historical active copy. Compare both recovered server copies directly against recovered25 client `130.dat` / client-map surfaces and floor-130 runtime content before selecting either candidate.

## Phase 1 floor-130 duplicate-copy arbitration — 2026-09-29

- Floor **130** is no longer an unexplained duplicate: two focused derived audits establish a genuine version fork while deliberately preserving `selected_path = NONE`.
- Recovered25 candidate audit (world-content run **36596045127 = PASS**):
  - client `130.dat` = 60x60, SHA-256 `85d710a270c6b945de21de53c9257ebaf38647cb54e77071db194cf5c5e203f3`;
  - `extra/130`: DAT tile diffs **1,067**, parts/object diffs **60**;
  - `family/130`: DAT tile diffs **1,733**, parts/object diffs **53**;
  - neither candidate is an exact client-DAT static-layer match;
  - candidate-to-candidate difference = **2,800 tile cells + 113 object cells**.
- The recovered25 classic-Warp geometry supplies an independent runtime discriminator:
  - two reachable Warp destinations enter floor 130 and two classic Warp sources leave it;
  - `family/130`: all **2/2 incoming destination points + 2/2 outgoing Warp source cells** are statically walkable under the recovered25 mapset;
  - `extra/130`: all corresponding **4/4** diagnostic points are statically blocked.
- Archived-2003 -> recovered25 DAT lineage audit (run **36596552717 = PASS**) shows an exact temporal split on every changed static cell:
  - DAT generations differ at **1,186 tile cells + 53 parts cells**; event plane difference = **0**;
  - `family/130` matches the archived-2003 value on **all 1,186 + 53 changed cells**, and the recovered25 value on none;
  - `extra/130` matches the recovered25 value on **all 1,186 + 53 changed cells**, and the archived-2003 value on none;
  - neither server copy is a whole-map exact static match to either DAT generation.
- Stable descendant loader behavior is last-loaded-wins for duplicate floor IDs, but recursive discovery is unsorted `readdir()`; therefore filesystem/path-name ordering cannot prove which copy was active historically.
- `tools/stoneage_floor130_arbitration.py` encodes the only provenance-safe conclusion:
  - `family/130 = ARCHIVED2003_ALIGNED + WARP_RUNTIME_CONSISTENT`;
  - `extra/130 = RECOVERED25_ALIGNED + WARP_RUNTIME_CONFLICTING`;
  - resolution = `PRESERVE_VERSION_FORK`;
  - default selected payload = **none**.
- The arbitration intentionally refuses to convert “runtime-consistent” or “temporally newer” into a hidden winner. If later evidence creates an exact static match or changes either diagnostic relation, regression requires re-arbitration.
- Full gameplay-model regression locking the fork: GitHub Actions **36597019931 = PASS**.
- **FLOOR_130_VERSION_FORK_ARBITRATION_R1 = CLOSED.**
- Next deterministic seam: construct the strict **826-floor materializable recovered runtime geometry/topology** while quarantining floor 130 and all edges touching it. Preserve full classic-Warp source rectangles first; only collapse to a single `MapPosition` when the recovered source geometry is actually a single cell.

## Phase 1 floor-130 duplicate-copy version-fork arbitration — 2026-09-29

- The sole unresolved supplemental floor, **130**, has now been compared directly across recovered25 client/server surfaces and an archived-2003 -> recovered25 DAT lineage.
- Recovered25 candidate audit `research/recovered/STONEAGE-25-FLOOR-130-CANDIDATE-AUDIT-R1.txt`:
  - client DAT = 60x60, SHA-256 `85d710a270c6b945de21de53c9257ebaf38647cb54e77071db194cf5c5e203f3`;
  - two server candidates remain byte-divergent;
  - neither server candidate is an exact tile+parts match to the recovered25 DAT;
  - `family/130` is walkable at all 2 incoming classic-Warp destinations and both outgoing Warp source cells;
  - `extra/130` blocks all four corresponding Warp diagnostic cells;
  - automatic candidate selection remains `NONE`.
- Archived-2003 -> recovered25 DAT lineage audit `research/recovered/STONEAGE-2003-25-FLOOR-130-CANDIDATE-LINEAGE-R1.txt`:
  - DAT static change = **1,186 tile cells + 53 parts cells**; event plane change = **0**;
  - on every changed tile/parts cell, `family/130` matches the archived-2003 side and never the recovered25 side;
  - on every changed tile/parts cell, `extra/130` matches the recovered25 side and never the archived-2003 side;
  - neither candidate is a complete exact static match to either DAT generation.
- `tools/stoneage_floor130_arbitration.py` therefore records two independent dimensions rather than collapsing them into a synthetic winner:
  - `family/130` = `ARCHIVED2003_ALIGNED` + `WARP_RUNTIME_CONSISTENT`;
  - `extra/130` = `RECOVERED25_ALIGNED` + `WARP_RUNTIME_CONFLICTING`.
- Resolution is deliberately **`PRESERVE_VERSION_FORK`** with `selected_path=None`. Temporal alignment is evidence of version evolution; Warp consistency is a separate runtime-consistency signal. Neither is sufficient to silently replace the other.
- Stable descendant duplicate-floor loading remains last-loaded-wins, but its recursive directory enumeration is unsorted `readdir()`; filesystem enumeration order cannot establish a historical canonical candidate.
- Full gameplay-model regression with the arbitration lock: GitHub Actions **36597019931 = PASS**.
- **RECOVERED25_FLOOR130_VERSION_FORK_R1 = CLOSED.**
- Next deterministic seam: bind the explicit floor-130 arbitration into the supplemental-world extension so unresolved floor 130 carries its two named version candidates and evidence dimensions as structured data, while retaining **no default materialization choice**.

## Phase 1 materializable recovered Warp geometry — 2026-09-29

- `tools/stoneage_materializable_world_geometry_probe.py` now projects recovered25 classic-Warp geometry across the represented **827-floor** world while quarantining unresolved or invalid edges.
- End-to-end world-content run **36597563574 = PASS** and committed `research/recovered/STONEAGE-25-MATERIALIZABLE-WORLD-WARP-GEOMETRY-R1.txt`.
- Represented/map boundary:
  - stable floors = **761**;
  - resolved supplemental floors = **65**;
  - unresolved supplemental floors = **1** (floor 130);
  - represented floor IDs = **827**;
  - default materializable floor IDs = **826**.
- Classic-Warp geometry:
  - classic Warps from represented sources = **2,834**;
  - materializable classic Warps = **2,826**;
  - quarantined classic Warps = **8**;
  - conditional-time tokens preserved on **14** materializable Warps but still not interpreted.
- The eight quarantined edges are fully classified:
  - **4** = `OUTSIDE_REPRESENTED_WORLD`, all targeting floor **40**, which remains excluded because no recovered server map exists;
  - **2** = `UNRESOLVED_SOURCE`, both floor **130 -> 141**;
  - **2** = `UNRESOLVED_DESTINATION`, both floor **141 -> 130**.
- Therefore the floor-130 fork is topologically localized to its two reciprocal portal pairs with floor 141; it does not silently enter default materializable Warp geometry.
- **RECOVERED25_MATERIALIZABLE_WARP_GEOMETRY_R1 = CLOSED.**
- Next deterministic seam: recompute reachability using only the 2,826 materializable Warp edges and the 761 stable seeds. Prove whether all **65** resolved supplemental floors remain reachable when floor 130 and the four floor-40 edges are quarantined; any orphaned supplemental floor must be reported rather than assumed reachable.

## Phase 1 strict 826-floor materializable Warp geometry — 2026-09-29

- `tools/stoneage_materializable_world_geometry_probe.py` now joins the immutable 761-floor stable manifest with the 65 resolved supplemental maps and audits classic-Warp geometry against the resulting **826 materializable maps** while preserving floor 130 as unresolved.
- End-to-end world-content run **36597563574 = PASS** and committed `research/recovered/STONEAGE-25-MATERIALIZABLE-WORLD-WARP-GEOMETRY-R1.txt`.
- Represented world = **827** floor IDs:
  - stable = **761**;
  - resolved supplemental = **65**;
  - unresolved supplemental = **1** (floor 130).
- Classic Warp records from represented source floors = **2,834**:
  - materializable/bounds-valid records = **2,826**;
  - quarantined records = **8**;
  - non-single source rectangles = **0**;
  - source out-of-bounds = **0**;
  - destination out-of-bounds = **0**.
- The eight quarantined records are fully explained:
  - **4** edges target floor 40, which is outside the represented runtime world because no recovered server map supports that destination;
  - **2** edges originate on unresolved floor 130;
  - **2** edges target unresolved floor 130.
- Materializable Warp geometry contains **14** conditional-time records. Their condition presence is retained but not interpreted.
- Source-cell multiplicity audit over the 2,826 materializable records:
  - unique source cells = **2,738**;
  - duplicate source cells = **71**;
  - **39** source cells contain only exact-equivalent duplicate definitions (**90 raw records**) and are safe to deduplicate;
  - **32** source cells have genuinely different destinations (**69 raw records**) and cannot be converted into one active Warp without additional arbitration;
  - none of the 71 duplicate-source groups contains a conditional-time Warp.
- **MATERIALIZABLE_RECOVERED_WORLD_WARP_GEOMETRY_R1 = CLOSED.**
- Next deterministic seam: construct a strict 826-map `HistoricalWorldTopology` with only unambiguous unconditional Warp edges active. Collapse exact duplicate definitions, retain 32 multi-destination source groups as explicit unresolved candidates, and retain the 14 conditional-time edges as deferred/inactive evidence until their original time tokens and condition semantics are bound.

## Phase 1 strict materializable runtime topology and Warp create-order closure — 2026-09-29

- The default recovered runtime world now has three distinct topology layers that must not be conflated:
  1. **materializable geometry evidence** = 2,826 classic-Warp records across 826 maps;
  2. **strict unambiguous/unconditional runtime topology** = 2,692 active Warp edges;
  3. deferred evidence = 32 multi-destination source groups + 14 conditional-time Warp records, with 8 non-materializable/quarantined records outside the default topology.
- Materializable-world reachability over all 2,826 bounds-valid geometry records is closed by `research/recovered/STONEAGE-25-MATERIALIZABLE-WORLD-REACHABILITY-R1.txt`:
  - materializable floor IDs = **826**;
  - reachable floor IDs = **826**;
  - resolved supplemental floors = **65/65 reachable**;
  - orphan resolved supplemental floors = **0**;
  - maximum supplemental depth = **23**.
- `tools/stoneage_materializable_world_topology.py` then applies the stricter executable boundary:
  - active unconditional/unambiguous Warp edges = **2,692**;
  - exact-equivalent duplicate source groups = **39**, safely collapsed;
  - multi-destination ambiguous source groups = **32**;
  - conditional-time Warp records = **14**, retained as deferred evidence;
  - unresolved floor 130 and its touching edges remain quarantined;
  - active runtime sources are unique and no active edge carries an uninterpreted time token.
- Full gameplay-model regression for the strict topology: GitHub Actions **36598302387 = PASS**.
- A dedicated recovered create-order audit, `research/recovered/STONEAGE-25-AMBIGUOUS-WARP-CREATE-ORDER-R1.txt`, then closes the relative ordering question for all 32 ambiguous source cells:
  - ambiguous sources = **32**;
  - candidate records = **69**;
  - **32/32 = SAME_FILE_ORDERED**;
  - **0/32 = CROSS_FILE_UNORDERED**.
- Pinned descendant controls support the ordering mechanism: map objects are tail-appended, overlap-event dispatch scans from the list head and stops at the first matching event object, and NPC generation processes create indices in ascending order. Because each competing group is in one create file, relative block order is deterministic even though cross-file discovery uses unsorted `readdir()`.
- Critical 810 gateway:
  - source `810,28,27`: first placement **3139** -> `809,18,13` at `genout/quiz.create` block **71**; later placement **3197** -> `829,18,13` at block **132**;
  - source `810,29,27`: first placement **3141** -> `809,19,13` at block **73**; later placement **3199** -> `829,19,13` at block **134**.
- End-to-end world-content run generating the create-order report: GitHub Actions **36599414334 = PASS**.
- **MATERIALIZABLE_WORLD_REACHABILITY_R1 = CLOSED.**
- **STRICT_MATERIALIZABLE_RUNTIME_TOPOLOGY_R1 = CLOSED.**
- **AMBIGUOUS_WARP_CREATE_ORDER_R1 = CLOSED.**
- Next deterministic seam: apply same-file first-match ordering to the 32 ambiguous source groups as an explicit runtime arbitration layer. Activate exactly one first candidate per ordered source, retain the other **37** candidate records as shadowed evidence, keep all 14 conditional-time records deferred, and recompute stable-seed reachability. Do not delete or rewrite shadowed Warp definitions.

## Phase 1 create-order-resolved classic-Warp runtime — 2026-09-29

- The recovered same-file create-order evidence is now applied to the default 826-map runtime by `tools/stoneage_ordered_warp_runtime.py`.
- Runtime arbitration results:
  - strict unambiguous active Warp edges = **2,692**;
  - same-file ambiguous source groups resolved by first-create/first-match order = **32**;
  - cross-file ambiguous source groups remaining unresolved = **0**;
  - later candidates retained as shadowed evidence = **37** records;
  - deferred conditional-time Warp records = **14**;
  - total active classic-Warp edges after ordering = **2,724**.
- The critical quiz gateway resolves deterministically under the recovered create order:
  - `810,28,27` activates placement **3139 -> 809,18,13** and shadows placement **3197 -> 829,18,13**;
  - `810,29,27` activates placement **3141 -> 809,19,13** and shadows placement **3199 -> 829,19,13**.
- Active classic-Warp reachability from all 761 stable seeds is therefore:
  - reachable maps = **815 / 826**;
  - reachable resolved supplemental maps = **54 / 65**;
  - resolved supplemental maps outside the active classic-Warp closure = **11**:
    **820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 831**.
- These eleven maps are not empty or internally disconnected: each has active incoming and outgoing classic-Warp edges inside the branch. The missing active ingress is localized to the two shadowed `810 -> 829` candidates above.
- The eleven floors remain materializable recovered25 content; “outside the active classic-Warp closure” must **not** yet be promoted to “unreachable in the full game”, because non-classic transport functions such as `WarpMan` / `FMWarpMan` and other scripted movement have not yet been folded into this reachability calculation.
- Full gameplay-model validation for create-order-resolved runtime: GitHub Actions **36599963621 = PASS**.
- End-to-end world-content report generation: GitHub Actions **36600092879 = PASS**, report `research/recovered/STONEAGE-25-ORDERED-WARP-RUNTIME-R1.txt`.
- **CREATE_ORDER_RESOLVED_CLASSIC_WARP_RUNTIME_R1 = CLOSED.**
- Next deterministic seam: audit all recovered non-classic player-transport semantics for the 11-floor shadowed branch, especially `WarpMan` and `FMWarpMan`, before deciding whether those floors are truly unreachable or only absent from the classic-Warp closure.



## Phase 1 shadowed-branch non-classic ingress gate closure — 2026-09-30

- Revalidated the 11-floor branch outside the active ordered classic-Warp closure: **820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 831**.
- Recovered non-classic transport audit over the currently reconstructed transport families finds exactly **one** potential ingress from a classic-reachable floor into that branch: **WarpMan 811 -> 820**.
- FMWarpMan contributes **0** such ingress edges; Airplane contributes **0**; recovered Bus route data is x/y-only and contributes **0** cross-floor edges.
- The sole WarpMan route is not an unconditional classic-style portal. Its ordinary payment route is disabled by the recovered negative-money configuration and its remaining route is condition-dependent.
- The recovered FREE expression is structurally one OR-clause containing one three-atom AND group: **2 level predicates + 1 item predicate**; operators present are one each of >, <, and =.
- Fixed-descendant runtime semantics were rechecked: comma is OR, & is AND; all LV atoms share the same player level, while ITEM predicates scan carried item IDs existentially.
- New privacy-preserving domain audit uses the recovered server's configured MAXLEVEL plus the configured active itemset catalog transiently while withholding raw operands and item IDs from committed output.
- Real recovered25 result: ingress rows = **1**; atoms = **3**; atoms with a domain witness = **3 / 3**; satisfiable clauses = **1 / 1**; domain-satisfiable ingress rows = **1 / 1**; unsupported atoms = **0**.
- Therefore **811 -> 820 is configuration-domain satisfiable** in recovered25. This is stronger than a merely syntactic candidate, but it is still **not yet a full gameplay-reachability proof**: the matching item definition existing in the active item catalog does not prove that a player can legitimately acquire that item, retain it, and present it at the WarpMan.
- New deterministic artifacts: tools/stoneage_shadowed_branch_warpman_satisfiability_probe.py; tests/test_stoneage_shadowed_branch_warpman_satisfiability_probe.py; research/recovered/STONEAGE-25-SHADOWED-BRANCH-WARPMAN-SATISFIABILITY-R1.txt.
- Validation: relevant transport/domain unit suite **18 tests PASS**; real preservation-bundle workflow GitHub Actions **36604872593 = PASS**; derived report commit **7c481beefd158ca6dc1359550c8b868a97a00f23**.
- **SHADOWED_BRANCH_WARPMAN_FREE_DOMAIN_R1 = CLOSED.**
- Next deterministic seam: resolve the required ITEM predicate against legitimate recovered gameplay acquisition surfaces (shop inventory, NPC/event reward, battle/drop or other item-grant paths) without committing the proprietary item ID. Only after an acquisition path is proven should the 11-floor branch be promoted from “condition-gated ingress with catalog witness” to player-reachable runtime content.


## Phase 1 shadowed-branch key-item ordinary-shop audit — 2026-09-30

- The unique ITEM equality predicate required by the condition-gated WarpMan ingress was resolved transiently against every recovered ItemShop placed on a floor in the ordered classic-Warp reachable set.
- Fixed-descendant ItemShop semantics were reproduced for screening: ItemList supports IDs/ranges, undefined item IDs are skipped, and only the first 33 valid entries are exposed.
- Recovered25 result: **212** candidate reachable ItemShop instances; **0** list the target item; **0** expose it after the 33-entry truncation; missing argument files = **0**.
- Therefore the required key item has **no ordinary reachable ItemShop acquisition path** in the recovered specimen.
- Artifact: research/recovered/STONEAGE-25-SHADOWED-BRANCH-KEY-ITEM-SHOP-R1.txt.
- Validation: GitHub Actions **36605691297 = PASS**; derived report commit **2fb4c13987f6bb6692b46552818969ffc7be0dda**.
- **SHADOWED_BRANCH_KEY_ITEM_SHOP_R1 = CLOSED / NO_WITNESS.**
- Next deterministic seam: test the same withheld item identity against reachable NPC/event AddItem rewards and reachable encounter enemy drop slots before making any claim about full player reachability of floor 820 and the 11-floor branch.


## Phase 1 shadowed branch joined progression closure — 2026-09-30

- The previously isolated 11-floor resolved supplemental branch is now closed through a state-gated runtime progression witness rather than being treated as dead/orphan content.
- Key-item acquisition is concrete in recovered25: **2 reachable ExChangeMan ACCEPT records on floor 2020** call the fixed-source GetItem -> NPC_EventAddItem path and award the withheld key item.
- Both award records have only a level gate plus DelStone payment; they require **no other item**, **no pet**, do **not** require the target item itself, and do **not** delete the target item as a prerequisite.
- Recovered MAXLEVEL plus fixed-descendant zero-trans carried-gold cap produce legal state witnesses for both records: **2/2 level-domain satisfiable, 2/2 zero-trans affordable, 2/2 combined state-domain satisfiable**. Exact level/cost operands remain withheld.
- Ordinary alternative acquisition paths were separately excluded in this specimen: reachable ItemShop witness **0**, reachable positive battle-drop witness **0**, ordinary fixed-source-covered AddItem reward witness **0**.
- Directed progression ordering is now joined: after acquisition on floor **2020**, the classic Warp graph reaches the WarpMan source floor **811** in **1 floor-level hop**.
- The acquisition level domain and the 811 WarpMan level window have both **same-level** and **non-decreasing-level** witnesses; therefore independent satisfiability is no longer being mistaken for an ordered progression.
- With the withheld key item carried, WarpMan **811 -> 820** has a combined state progression witness.
- Starting from **820**, the active classic Warp graph reaches **all 11 / 11** formerly orphaned floors: **820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 831**.
- The post-ingress branch has classic maximum floor-level depth **23** and contains a classic return path into the pre-existing reachable world; it is a connected gated branch, not a one-way dead end.
- Artifact: research/recovered/STONEAGE-25-SHADOWED-BRANCH-PROGRESSION-R1.txt; tool: tools/stoneage_shadowed_branch_progression_witness_probe.py; tests: tests/test_stoneage_shadowed_branch_progression_witness_probe.py.
- Validation: transport/progression workflow GitHub Actions **36609564588 = PASS**; derived report commit **8146bbbd4fc98be7861526226b71f05ccda2f751**.
- **SHADOWED_BRANCH_STATE_GATED_RUNTIME_R1 = CLOSED.**
- Important scope boundary: this proves existence of a legal player state with enough carried stone, not a fresh-character economic earning route for the fee. Economic provenance remains separate and must not be silently folded into map reachability.
- Next deterministic seam: recompute the complete materializable world reachability with this validated state-gated WarpMan edge included, measure any remaining floor-level gaps, and only then choose the next unresolved world-content seam.


## Phase 1 state-gated materializable world reachability closure — 2026-09-30

- Corrected the auxiliary legal-state probe after fixed-descendant source revalidation: `EventNo=-1` is an explicit **ungated event sentinel**. `NPC_EventCheckFlg(...,-1)` returns FALSE and event setters ignore `-1`; it must not be treated as a failed event prerequisite.
- Recovered25 legal-state join now reports **2 / 2** reachable ExChangeMan key-item award records as state-domain satisfiable; each awards one withheld target item, has no keyword gate, shares **20** legal level values with the WarpMan gate, and reaches floor 811 in one directed classic-Warp floor hop.
- The world-level reachability model now preserves two separate layers instead of flattening the gate:
  - **classic-only ordered Warp reachability = 815 / 826 materializable floors**;
  - **existential state-gated runtime reachability = 826 / 826 materializable floors**.
- The single validated state-gated transport edge is **811 -> 820**. It makes exactly the previously isolated **11** floors newly reachable: **820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 831**.
- Resolved supplemental coverage therefore changes from **54 / 65 classic-only** to **65 / 65 state-gated**. Remaining materializable floor-level gaps = **0**.
- This is an existential legal-player-state statement, not an unconditional portal statement and not a fresh-character economic progression proof. The classic-only 815 count remains a first-class invariant.
- Artifacts: `tools/stoneage_state_gated_runtime_world_reachability_probe.py`; `tests/test_stoneage_state_gated_runtime_world_reachability_probe.py`; `research/recovered/STONEAGE-25-STATE-GATED-RUNTIME-WORLD-REACHABILITY-R1.txt`; corrected `research/recovered/STONEAGE-25-SHADOWED-BRANCH-LEGAL-STATE-REACHABILITY-R1.txt`.
- Validation: legal-state workflow GitHub Actions **36610271589 = PASS**; state-gated world workflow **36610480622 = PASS**; derived world report commit **71ac195a0c1ef9b8aa3063cd75e6c74612ea8433**.
- **STATE_GATED_MATERIALIZABLE_WORLD_REACHABILITY_R1 = CLOSED.**
- Next deterministic seam: floor-level world reachability is exhausted. Audit **coordinate-level accessibility of the two critical state-gated interaction points** (the reachable ExChangeMan award NPC and WarpMan 811 ingress) against the recovered map/collision/path topology. Keep floor-level reachability and same-floor walkability distinct; if the necessary collision plane is not provenance-safe for those floors, record that boundary rather than synthesizing a path.


## Phase 1 shadowed-branch static coordinate accessibility closure — 2026-09-30

- Floor-level progression was tightened to recovered25 **coordinate-level static accessibility** using the server-authoritative LS2MAP tile/object planes plus the recovered `mapset.txt` WALKABLE/HAVEHEIGHT metadata. Taiwan-v1 ADRN substitution was not used for this recovered25 proof.
- Exact progression records were rebound rather than searched by loose item-number occurrence: the coordinate audit consumes the same closed ExChangeMan award records and the same unique `811 -> 820` WarpMan ingress already validated by the progression probes.
- Fixed-descendant interaction distance was revalidated as Chebyshev distance `max(|dx|,|dy|) <= 2` for both ExChangeMan and WarpMan.
- Recovered25 result:
  - award placements = **2**;
  - gated WarpMan placements = **1**;
  - active classic hops from the award floor to the ingress floor = **2**;
  - statically walkable award-interaction cells = **24**;
  - statically walkable WarpMan-interaction cells = **16**;
  - award-floor server-map copy status = **UNIQUE**;
  - ingress-floor server-map copy status = **UNIQUE**;
  - missing recovered mapset metadata = **0 / 0**;
  - shortest static path from a valid award interaction cell to a qualifying classic-Warp source = **4 steps**;
  - shortest static path from the corresponding classic-Warp landing coordinate to a valid WarpMan interaction cell = **7 steps**;
  - `STATIC_COORDINATE_CHAIN|witness=1`.
- Movement uses the recovered descendant eight-direction rule, including diagonal corner rejection when either orthogonal side cell is statically blocked.
- Dynamic transient occupants remain a separate runtime layer. This milestone proves a static coordinate route through recovered25 authoritative map/collision data; it does not assert that every instantaneous live-object arrangement is obstruction-free.
- Artifact: `tools/stoneage_shadowed_branch_coordinate_access_probe.py`; `tests/test_stoneage_shadowed_branch_coordinate_access_probe.py`; `research/recovered/STONEAGE-25-SHADOWED-BRANCH-COORDINATE-ACCESS-R1.txt`.
- Validation: GitHub Actions **36611860401 = PASS**; derived report commit **88ce0f15fa31a13251eae52e7d71d7d955ccad3b**. CI is further tightened to require `STATIC_COORDINATE_CHAIN|witness=1` on future runs.
- **SHADOWED_BRANCH_STATIC_COORDINATE_ACCESS_R1 = CLOSED.**
- Next deterministic seam: audit the **dynamic-object occupancy boundary** along this critical coordinate chain. Distinguish fixed/non-overable recovered NPC or item occupants from transient/moving occupants, and verify that at least one static route remains executable without inventing despawn/movement assumptions. If fixed occupant overability cannot be resolved from recovered25 data, record that exact boundary rather than treating static walkability as full live-world reachability.


## Phase 1 shadowed-branch deterministic dynamic occupancy closure — 2026-09-30

- The coordinate-level progression witness is now extended through the deterministic dynamic-object boundary instead of assuming an empty live map.
- Fixed-descendant movement semantics were revalidated and kept explicit:
  - classic Warp characters are overable;
  - `OBJTYPE_GOLD` does **not** block `CHAR_walk`;
  - `OBJTYPE_ITEM` blocks only when `ITEM_ISOVERED == false`;
  - item default `ITEM_ISOVERED` is true, but per-item data may override it;
  - legacy normal ground-object persistence restores only the exact file `itemgold`; `itemgold_extra` is an emergency non-normal-save filename.
- Recovered25 preservation-bundle census finds:
  - normal `itemgold` files = **0**;
  - `itemgold_extra` files = **0**;
  - persisted critical-floor ITEM rows = **0**;
  - persisted critical-floor GOLD rows = **0**;
  - persisted critical-floor CHAR rows = **0**.
- The prerequisite coordinate audit already treats every recovered **non-Warp NPC birth cell as blocking**, yet both critical local paths remain reachable at the same shortest lengths (**4 steps** and **7 steps**). Thus fixed recovered NPC placement does not require any movement/despawn assumption.
- Result: `DETERMINISTIC_INITIAL_DYNAMIC_OCCUPANCY_CHAIN|witness=1` and `PERSISTED_CRITICAL_BLOCKER_FREE|witness=1`.
- Scope boundary remains explicit: arbitrary later live-session states can introduce moving characters/pets or non-overable dropped items, so **universal reachability across every possible live state is intentionally not claimed**. Those objects are transient session state, not deterministic recovered static-world content.
- Artifact: `tools/stoneage_shadowed_branch_dynamic_occupancy_probe.py`; tests: `tests/test_stoneage_shadowed_branch_dynamic_occupancy_probe.py`; derived report: `research/recovered/STONEAGE-25-SHADOWED-BRANCH-DYNAMIC-OCCUPANCY-R1.txt`.
- Validation: transport workflow GitHub Actions **36676771400 = PASS**; derived report commit **4b11a1be9afd8aedd998192746f1a9c98ad4241e**.
- **SHADOWED_BRANCH_DETERMINISTIC_DYNAMIC_OCCUPANCY_R1 = CLOSED.**
- Next deterministic seam: close the remaining **fresh-character economic provenance** for the gated branch. The current progression proves only that the exchange fee fits inside the legal carried-Stone domain. Audit whether a newly initialized single-player character can legally acquire the required Stone through recovered gameplay sources before claiming the branch is fresh-start reachable; preserve the existing legal-state witness independently if a complete earning chain cannot be proven.


## Phase 1 shadowed-branch fresh-start Stone closure — 2026-09-30

- The previously open economic provenance seam is now closed without inventing any earning loop.
- Fixed-descendant new-character initialization was revalidated: `CHAR_GOLD` is initialized from `getNewplayergivegold()`, whose recovered configuration key is `setup.cf` `GOLD`.
- The new probe reads the recovered25 `setup.cf` birth-Stone value and compares it directly against the real `DelStone` fee over each already-valid ExChangeMan award level state. Exact Stone amounts and thresholds remain withheld from derived reports.
- Recovered25 result:
  - matching key-item award records = **2**;
  - award records with valid computable fees = **2**;
  - award records whose fee is already covered by new-character starting Stone = **2 / 2**;
  - `FRESH_START_STONE|positive=1|covers_minimum_valid_fee=1`;
  - `FRESH_START_ECONOMIC_CHAIN|witness=1`.
- No battle-income, shop-sale, quest-reward, bank, external-player transfer, farming or despawn assumption is required for the fee. A valid route may simply retain the recovered starting Stone until the exchange.
- Artifact: `tools/stoneage_shadowed_branch_fresh_start_stone_probe.py`; tests: `tests/test_stoneage_shadowed_branch_fresh_start_stone_probe.py`; derived report: `research/recovered/STONEAGE-25-SHADOWED-BRANCH-FRESH-START-STONE-R1.txt`.
- Validation: transport workflow GitHub Actions **36677139842 = PASS**; derived report commit **b557bac186ce83900f5d3f5fe2f0e1abb5a0838b**.
- **SHADOWED_BRANCH_FRESH_START_STONE_R1 = CLOSED.**
- Next deterministic seam: close **fresh-character spatial provenance**. Recover the actual new-character spawn floor/coordinate rule from recovered25/fixed source, then test directed runtime reachability from those birth positions to the key-item award floor and through the already closed coordinate/progression chain. Do not equate the existing 761-floor world seed set with a real player birth state.


## Phase 1 fresh-start spatial provenance and direct-level boundary — 2026-09-30

- Fresh-character spatial provenance is now separated into floor-level, coordinate-level existential, and all-hometown claims.
- Pinned fixed-descendant source control for this baseline keeps `_DELBORNPLACE` and `_MUSEUM` disabled, so the four normal hometown entries in `CHAR_getInitElderPosition` are the applicable new-character spawn candidates. Two later compile-time variant floors were tested only as a sensitivity check and are not promoted into the baseline.
- Recovered25 floor-level result:
  - normal hometown candidates = **4**;
  - normal hometowns with directed classic-Warp floor reachability to the key-item award floor = **4 / 4**;
  - shortest floor-hop counts = **4, 2, 9, 9**;
  - later source-known compile-time variants tested = **2**, reachable = **0 / 2**.
- Recovered25 coordinate-level result uses server-authoritative LS2MAP + mapset collision, diagonal corner rejection, active classic-Warp source/landing coordinates and conservative non-Warp NPC birth blockers:
  - normal hometown coordinate-reachable to a valid award interaction cell = **2 / 4**;
  - static-only comparison is also **2 / 4**, so the two failures are not caused by the conservative NPC blocker model;
  - unresolved map floors on all four searches = **0**;
  - `FRESH_START_EXISTENTIAL_COORDINATE_CHAIN|witness=1`;
  - `FRESH_START_ALL_HOMETOWNS_COORDINATE_CHAIN|witness=0`.
- Interpretation: a legal new-game start **exists** from at least two selectable hometowns and reaches the award NPC through recovered coordinate topology. The stronger statement that every normal hometown reaches that progression chain is not supported and remains explicitly false for this recovered topology model.
- Artifacts: `tools/stoneage_shadowed_branch_fresh_start_spatial_probe.py`, `tools/stoneage_shadowed_branch_fresh_start_coordinate_probe.py`; reports: `research/recovered/STONEAGE-25-SHADOWED-BRANCH-FRESH-START-SPATIAL-R1.txt`, `research/recovered/STONEAGE-25-SHADOWED-BRANCH-FRESH-START-COORDINATE-R1.txt`.
- Validation: GitHub Actions **36677647678**, **36678032381**, **36678205216**, and **36678452071** all PASS; latest derived coordinate report is preserved on remote main.
- **SHADOWED_BRANCH_FRESH_START_SPATIAL_EXISTENCE_R1 = CLOSED.**

- Direct birth-level sufficiency was audited separately. Fixed-descendant `_NEW_PLAYER_CF` initializes `CHAR_LV` from recovered `setup.cf` `LV` via `getNewplayerlv()`.
- Recovered25 direct-level result:
  - matching key-item award records = **2**;
  - records with nonempty award/gate joint level domain = **2**;
  - unique WarpMan legal level values = **20**;
  - records whose joint domain contains the exact birth level = **0 / 2**;
  - `FRESH_START_DIRECT_LEVEL_CHAIN|witness=0`.
- Therefore fresh-start progression is **not yet closed end-to-end**: the character must legally gain levels before the already-closed award -> key item -> 811 -> 820 branch chain can execute.
- Artifact: `tools/stoneage_shadowed_branch_fresh_start_level_probe.py`; report: `research/recovered/STONEAGE-25-SHADOWED-BRANCH-FRESH-START-LEVEL-R1.txt`.
- Validation: GitHub Actions **36679638307 = PASS**; derived report commit **28a961dad0b7d65a858486ae28f6ab204d6d12a3**.
- Next deterministic seam: prove **fresh-start leveling provenance**. Reuse recovered EXP, encounter, group and enemy data plus fixed-descendant battle EXP semantics. Prefer an existential repeatable positive-EXP route from one of the two coordinate-valid hometown starts; preserve combat-victory feasibility as a separate boundary if the data only proves reward mechanics rather than a winnable encounter.

## Phase 1 fresh-start leveling, combat, ordered award continuation and full-world promotion closure — 2026-09-30

- The previously open fresh-start leveling provenance seam is now closed end-to-end as an **existential recovered25 progression witness**, while keeping guarantee/balance/all-hometown claims separate.
- Repeatable reward-source audit:
  - coordinate-reachable positive-EXP encounter sources = **2022**;
  - sources able to spawn an enemy at or below recovered birth level = **106**;
  - recovered EXP rows from birth to the minimum joint ExChangeMan/WarpMan legal level are complete and strictly positive;
  - fixed-descendant battle settlement keeps defeated-enemy EXP at **at least 1** after level-gap reduction.
- Combat-feasibility audit was tightened against fixed-descendant enemy AI rather than treating every template with skills as unusable:
  - coordinate-valid hometown low-level source rows = **44**;
  - unique low-level candidate variants = **16**;
  - candidates whose normal AI has a positive ordinary-attack branch = **16 / 16**;
  - legal fresh-character player-first ordinary one-hit-KO witnesses = **16 / 16**;
  - `FRESH_START_EXISTENTIAL_COMBAT_VICTORY|witness=1`.
  - The report now correctly records that merely having pet skills does not force skill use; a lethal first hit also ends the target before the counter chain.
- Ordered leveling-to-award sequencing is separately proven rather than joining unrelated reachability facts:
  - each combat witness is bound to a concrete walkable recovered encounter cell;
  - that exact cell must be coordinate-reachable from the same normal hometown **and** lie in a component with a directed recovered classic-Warp continuation to a valid key-item award interaction cell;
  - ordered source-to-award witnesses = **16 / 16**;
  - ordered witness hometowns = **1**;
  - ambiguous encounter keys = **0**;
  - unresolved reverse-map floors = **0**;
  - `FRESH_START_LEVELING_TO_TARGET|witness=1`.
- Repetition remains an existential proof, not a pacing claim:
  - the same legal one-enemy / weak-enemy-roll / player-first / successful-hit outcome may recur for a finite sequence;
  - every qualifying kill remains positive EXP;
  - level-up grants free allocation points without forcing them to be spent, so leaving them unspent preserves the STR/DEX values used by the one-hit witness;
  - ordinary PvE battle preserves the world position used for the encounter source.
- The fresh-start chain is now joined with the already-closed initial-Stone, ExChangeMan award, key-item, directed classic-Warp, WarpMan gate and post-ingress branch evidence:
  - `fresh_start_stone_chain=1`;
  - `fresh_start_leveling_to_target=1`;
  - `award_to_gate_progression_chain=1`;
  - `post_ingress_branch_full_closure=1`.
- Full recovered25 materializable-world promotion:
  - materializable floor ids = **826**;
  - fresh-start state-gated reachable floor ids = **826**;
  - fresh-start remaining unreachable floor ids = **0**;
  - `FRESH_START_STATE_GATED_RUNTIME_WORLD|witness=1`.
- Scope boundary remains explicit:
  - this does **not** promote the gated WarpMan edge to an unconditional edge;
  - it does **not** prove guaranteed RNG, efficient leveling, or universal combat victory;
  - it does **not** prove all four normal hometowns can execute the same progression.
  - Existing coordinate evidence remains **2 / 4** normal hometowns to the award interaction chain, and the static-only comparison is also **2 / 4**. Therefore `ALL_HOMETOWNS_FULL_WORLD|closed=0` remains correct.
- New artifacts:
  - `tools/stoneage_shadowed_branch_fresh_start_combat_probe.py`;
  - `tests/test_stoneage_shadowed_branch_fresh_start_combat_probe.py`;
  - `research/recovered/STONEAGE-25-SHADOWED-BRANCH-FRESH-START-COMBAT-R1.txt`;
  - `tools/stoneage_shadowed_branch_fresh_start_leveling_closure_probe.py`;
  - `tests/test_stoneage_shadowed_branch_fresh_start_leveling_closure_probe.py`;
  - `research/recovered/STONEAGE-25-SHADOWED-BRANCH-FRESH-START-LEVELING-CLOSURE-R1.txt`;
  - `tools/stoneage_shadowed_branch_fresh_start_world_closure_probe.py`;
  - `tests/test_stoneage_shadowed_branch_fresh_start_world_closure_probe.py`;
  - `research/recovered/STONEAGE-25-FRESH-START-STATE-GATED-RUNTIME-WORLD-REACHABILITY-R1.txt`.
- Validation:
  - GitHub Actions **36684786971 = PASS** closed the ordered fresh-start leveling-to-target witness;
  - GitHub Actions **36685235362 = PASS** closed the strict fresh-start-to-full-world join;
  - derived-report remote HEAD before this state update = `18e6d530688c4c679f9aa0b638cd8d8cfb7254d8`.
- **SHADOWED_BRANCH_FRESH_START_LEVELING_TO_TARGET_R1 = CLOSED.**
- **FRESH_START_STATE_GATED_RUNTIME_WORLD_REACHABILITY_R1 = CLOSED.**
- Next deterministic seam: resolve the **all-hometowns coordinate viability gap** without reopening the existential closure. The two failing normal hometowns already fail under the static-only coordinate model, so do not blame conservative NPC occupancy. Classify whether their missing award route is caused by a genuinely disconnected recovered coordinate component, a required non-classic transport/interaction omitted from the classic-Warp graph, or another recovered movement/transition semantic. Only promote all-hometown reachability if an explicit recovered path exists.

## Phase 1 all-hometowns coordinate-gap classification — 2026-09-30

- The two failed normal hometowns are now classified from recovered25 coordinate topology rather than floor-only reachability.
- Both fail for the same reason under conservative-NPC and static-only models: `CLASSIC_WARP_SOURCE_COMPONENT_DISCONNECTED`.
- At each failed start's closest coordinate-reachable frontier, the award remains **5 classic floor hops** away; exactly **1** progressive classic-Warp source component is disconnected, while invalid progressive destinations = **0** and usable progressive edges from the reached component = **0**.
- Because the static-only result is identical, conservative NPC birth occupancy is not the cause.
- Fixed-descendant Bus route movement was rechecked: it advances through `CHAR_walk(...,0)`, whose movement path enforces `MAP_walkAble` and diagonal corner checks. Bus therefore cannot be treated as a bypass across a genuinely disconnected static walk component.
- Artifact: `tools/stoneage_shadowed_branch_fresh_start_coordinate_gap_probe.py`; test: `tests/test_stoneage_shadowed_branch_fresh_start_coordinate_gap_probe.py`; report: `research/recovered/STONEAGE-25-SHADOWED-BRANCH-FRESH-START-COORDINATE-GAP-R1.txt`.
- Validation: the test-fixture mismatch on the first classification commit was corrected without changing probe semantics; GitHub Actions **36686985711 = PASS**.
- **FRESH_START_ALL_HOMETOWNS_COORDINATE_GAP_CLASSIFICATION_R1 = CLOSED.**
- **ALL_HOMETOWNS_FULL_WORLD remains OPEN.**
- Next deterministic seam: audit coordinate-level recovered **WarpMan/FMWarpMan spatial bridge candidates** from the actually reachable fresh-start components. Dialogue facing, FREE/action/fee, family and schedule gates remain separate; a spatial candidate must not be promoted to a legal fresh-start route until those gates are proven. If no dialogue-warp bridge exists, advance to Airplane boarding/route component geometry.

## Phase 1 all-hometowns legal fresh-start full-world closure — 2026-09-30

- The previously OPEN all-hometowns gap is now closed by an ordered recovered25 state search rather than by joining independent floor-level facts.
- The two normal hometowns that fail the classic-Warp coordinate model each have exactly one selected recovered `WarpMan` spatial bridge into the award-reachable component. Both selected bridges use the same single `ITEM = ...` FREE predicate; their WarpMan fee is disabled, no schedule gate is present, and fresh-login party state is `CHAR_PARTY_NONE`.
- Legitimate bridge-item acquisition is closed through recovered ItemShop state:
  - target-visible ItemShop placements = **2**;
  - normal-purchase ItemShop placements = **2**;
  - each failed hometown has exactly **1** ordered fresh-start route from spawn to an affordable qualifying shop and onward to its selected WarpMan;
  - starting Stone covers both the bridge-item purchase and the later already-proven ExChangeMan award fee on both routes;
  - unresolved map floors on both ordered shop routes = **0**.
- Purchase/execution prerequisites are closed without assuming an empty backpack:
  - fixed descendant fresh-character inventory capacity = **15** slots;
  - recovered25 exposes all **15** starter ITEM configuration keys, of which **13** are positive;
  - therefore at least **2** item slots remain guaranteed empty even if every configured starter item is created successfully;
  - both selected WarpMan arguments contain `FreeMsg`;
  - both selected WarpMan arguments contain **0** `Action_RunDoEventAction` side-effect fields;
  - `FRESH_START_ALL_FAILED_HOMETOWNS_WARPMAN_EXECUTION_PREREQUISITES|witness=1`.
- The final all-hometowns probe preserves combat witness identity per spawn and searches a component/state graph from each real hometown coordinate. It requires a legal repeatable positive-EXP / one-hit existential combat witness before the award; the two bridged hometowns must additionally obtain the shop item and traverse the exact selected WarpMan edge before reaching the award interaction component.
- Recovered25 ordered results:
  - hometown **1**: **16** combat witnesses; ordered = **1**; milestones = `COMBAT`; visited states = **107**; unresolved maps = **0**;
  - hometown **2**: **16** combat witnesses; ordered = **1**; milestones = `COMBAT`; visited states = **107**; unresolved maps = **0**;
  - hometown **3**: **28** combat witnesses; ordered = **1**; milestones = `COMBAT > SHOP > WARPMAN`; visited states = **446**; unresolved maps = **0**;
  - hometown **4**: **28** combat witnesses; ordered = **1**; milestones = `SHOP > COMBAT > WARPMAN`; visited states = **442**; unresolved maps = **0**.
- Joined prerequisites are all positive:
  - bridge shop/execution = **1**;
  - fresh-start leveling reward chain = **1**;
  - downstream award-to-shadowed-branch progression = **1**;
  - materializable recovered world closure = **1**.
- Final recovered25 result:
  - `FRESH_START_ALL_HOMETOWNS_ORDERED_PROGRESSION|witness=1`;
  - `ALL_HOMETOWNS_FULL_WORLD|closed=1`.
- Scope remains existential and version-tagged. This does **not** make WarpMan unconditional, does not prove guaranteed combat or transport RNG, and does not make an efficiency/pacing claim. It proves that each of the four normal recovered25 fresh-start hometowns has at least one legal ordered progression into the complete **826-floor materializable recovered world** under the pinned descendant semantics and recovered data.
- New/updated artifacts:
  - `tools/stoneage_shadowed_branch_fresh_start_warpman_bridge_shop_route_probe.py`;
  - `tests/test_stoneage_shadowed_branch_fresh_start_warpman_bridge_shop_route_probe.py`;
  - `research/recovered/STONEAGE-25-SHADOWED-BRANCH-FRESH-START-WARPMAN-BRIDGE-SHOP-ROUTE-R1.txt`;
  - `tools/stoneage_shadowed_branch_fresh_start_all_hometown_progression_probe.py`;
  - `tests/test_stoneage_shadowed_branch_fresh_start_all_hometown_progression_probe.py`;
  - `research/recovered/STONEAGE-25-SHADOWED-BRANCH-FRESH-START-ALL-HOMETOWN-PROGRESSION-R1.txt`.
- Validation:
  - GitHub Actions **36703000224 = PASS** closed the strict shop / inventory / WarpMan execution prerequisites;
  - GitHub Actions **36705174632 = PASS** closed the four-hometown ordered state search;
  - derived-report remote commit = `8be51231c8b417ee5f9c19f5e900f8cbca750fb1`.
- **FRESH_START_ALL_HOMETOWNS_ORDERED_PROGRESSION_R1 = CLOSED.**
- **ALL_HOMETOWNS_FULL_WORLD = CLOSED.**
- Next Phase-1 priority: stop extending this transport proof unless contradictory evidence appears. Promote the now-closed recovered world + four-hometown start/progression semantics into a single engine-neutral, version-tagged runtime bootstrap contract suitable for the local-first single-player implementation. Keep Taiwan-v1 historical membership separate from recovered25/later bridge content and preserve every state-gated transition explicitly.



## Phase 1 engine-neutral runtime bootstrap contract — 2026-09-30

- The closed recovered25 world + four-hometown progression proof is now promoted into a single engine-neutral implementation-facing contract without changing historical provenance.
- New machine-readable contract: `game/RUNTIME-BOOTSTRAP-RECOVERED25-R1.json`.
- Human-readable specification: `docs/RUNTIME-BOOTSTRAP-CONTRACT-R1.md`.
- Provenance boundary is explicit and machine-validated:
  - historical foundation = **Taiwan/Waei v1.0**;
  - runtime world profile = **recovered25**;
  - recovered25 evidence role = **LATER_RECOVERED**;
  - recovered25 membership in Taiwan v1.0 = **UNPROVEN**;
  - later recovered content may supply reconstruction bootstrap semantics but may **not** be relabelled as Taiwan-v1 historical content.
- Local-first architecture boundary is fixed:
  - authoritative state = local world model;
  - legacy network transport = not required;
  - account service = not required;
  - engine binding = none;
  - historical map delivery is preserved as authoritative region materialization semantics, not mandatory socket/protocol topology.
- Contracted recovered25 runtime surface:
  - materializable floors = **826**;
  - fresh-start state-gated reachable floors = **826**;
  - remaining unreachable floors = **0**;
  - normal fresh-start hometowns = **4**;
  - classic direct hometown routes = **2**;
  - state-gated WarpMan hometown routes = **2**;
  - all four ordered progression routes = **closed**.
- State-gated topology is preserved explicitly:
  - shadowed-branch ingress `811 -> 820` remains conditional;
  - hometown 3/4 selected WarpMan bridges remain conditional ITEM-gated transitions;
  - no gated edge is promoted into the unconditional classic world graph.
- Starter runtime constraints are versioned in the contract:
  - inventory capacity = **15**;
  - positive configured starter items = **13**;
  - guaranteed empty slots = **2**;
  - starting Stone covers the closed award fee and, for bridged starts, bridge-item purchase + award fee.
- New architecture decision: **DD-015** requires version-tagged bootstrap contracts, provenance-preserving adapters and explicit conditional transitions.
- `game/README.md` now points implementation work at the bootstrap contract while keeping production engine selection deferred.
- Validation:
  - GitHub Actions **36708333152 = PASS**;
  - contract commit = `b8cfa017dd7fcac1d86e2d23f2d0f6dc175ba14f`.
- **RUNTIME_BOOTSTRAP_CONTRACT_R1 = CLOSED.**
- Next Phase-1 priority: define the **minimal engine-neutral local runtime core interfaces/data model** that consume the bootstrap contract. Required boundaries should cover versioned world-profile loading, authoritative world/player state, region materialization, unconditional vs state-gated transition evaluation, fresh-start creation, deterministic progression/economy mutation and local persistence. Do not choose a rendering engine and do not recreate legacy MMO services.


## Phase 1 minimal engine-neutral local runtime core interfaces — 2026-09-30

- The runtime-bootstrap contract now has an executable engine-neutral consumer boundary instead of remaining documentation-only.
- Existing deterministic historical runtime modules were reused rather than replaced:
  - `tools/stoneage_singleplayer_domain.py`;
  - `tools/stoneage_singleplayer_world.py`;
  - `tools/stoneage_singleplayer_runtime.py`;
  - `tools/stoneage_singleplayer_persistence.py`.
- New interface/data-model layer: `tools/stoneage_local_runtime_core.py`.
- New specification: `docs/RUNTIME-CORE-INTERFACES-R1.md`.
- R1 adds:
  - strict typed loading of `stoneage.runtime-bootstrap.r1`;
  - executable provenance guards that reject recovered25→Taiwan-v1 promotion;
  - `VersionedWorldProfileProvider` region-materialization port;
  - `TransitionBindingResolver` for raw/versioned state-gated edge binding;
  - `TransitionGateEvaluator` for conditional traversal decisions;
  - `FreshStartFactory` for the four preserved hometown choices;
  - `LocalPersistenceStore` backend boundary;
  - `ResolvedTransitionBinding`, `TransitionGateDecision`, `FreshStartSeed` and region request/materialization records.
- A modern local session envelope is now defined as `stoneage.local-runtime-session.r1`:
  - persists bootstrap contract/profile identity;
  - selected hometown ordinal;
  - current map position;
  - persistent local world/progression flags;
  - the existing R3 player-owned persistence payload;
  - does **not** persist runtime object IDs, active NPC sessions, battle sessions, renderer state, account/network state or other transient objects.
- This local session envelope is a **DESIGN** persistence layer and does not overwrite the documented historical SAAC save/logout behavior.
- State-gated transition topology remains separate from `HistoricalWorldTopology.legacy_warps`; the new interfaces deliberately require an explicit resolver/evaluator rather than silently flattening conditional edges into classic Warp.
- RNG remains explicit input at the mechanics boundary; the engine may own a seeded RNG service later, but deterministic mechanics continue to receive concrete rolls/decisions.
- Validation:
  - GitHub Actions **36708875326 = PASS** (bootstrap contract);
  - GitHub Actions **36708875386 = PASS** (local runtime core + existing world/persistence/runtime regression suite);
  - implementation commit = `aa1ca51702a0c7a6e5d0080fea495edacdd9f552`.
- **LOCAL_RUNTIME_CORE_INTERFACES_R1 = CLOSED.**
- Next Phase-1 priority: implement a provenance-bearing **recovered25 world-profile adapter** behind these interfaces. It must materialize the closed 826-floor manifest into engine-neutral topology/region inputs, keep each concrete map's provenance, bind the three current state-gated transition contracts (hometown 3, hometown 4, 811→820), expose all four fresh-start seeds, and support an in-process bootstrap→fresh-start→materialize→transition→save/load smoke test. Raw recovered identifiers must remain version-bound; do not claim Taiwan-v1 membership.


## Phase 1 recovered25 concrete region payload source — 2026-09-30

- A concrete engine-neutral recovered25 region payload source now sits behind the versioned world/profile layer:
  - `tools/stoneage_recovered25_region_payload.py`;
  - `tools/stoneage_recovered25_region_payload_smoke.py`;
  - `docs/RECOVERED25-REGION-PAYLOAD-SOURCE-R1.md`.
- The default 826-floor materializable world is deliberately split by authentic recovered format rather than flattened:
  - **761** stable floors -> recovered client DAT **three-plane** payloads (tile + object/parts + event);
  - **65** resolved supplemental floors -> recovered server LS2MAP **two-plane** payloads (tile + object);
  - unresolved floor **130** remains outside the default materializable profile.
- Every concrete payload is checked against the committed materializable manifest for floor identity, dimensions and SHA-256.
- Critical event-layer boundary:
  - client DAT floors preserve their recovered event plane;
  - server LS2MAP floors expose `event_ids = None`;
  - the runtime must **not** synthesize an all-zero event plane for LS2MAP merely to make formats uniform;
  - NPC/warp/encounter/event semantics remain a separate authoritative world-content layer.
- The region API returns inclusive row-major tile/object/event slices plus source kind, event-plane status, payload SHA and the existing structured `LATER_RECOVERED` provenance.
- No raw map plane bytes are retained in the repository report.
- Bundle-backed validation:
  - materializable floors = **826**;
  - client DAT three-plane floors = **761**;
  - server LS2MAP two-plane floors = **65**;
  - event-plane-present floors = **761**;
  - event-layer-separate floors = **65**;
  - `RESOLUTION|RECOVERED25_REGION_PAYLOAD_SOURCE_CLOSED`.
- Validation workflow: GitHub Actions **36711418355 = PASS**.
- Derived report: `research/recovered/STONEAGE-25-REGION-PAYLOAD-SOURCE-R1.txt`.
- **RECOVERED25_REGION_PAYLOAD_SOURCE_R1 = CLOSED.**
- This closure does not establish Taiwan-v1 membership for recovered25 maps. It only supplies concrete later-recovered payloads behind the already engine-neutral local runtime boundary.
- Current primary seam remains the recovered25 world-profile adapter's **latest bundle-backed state-gated transition smoke** on the current remote HEAD. Only after that run passes should the adapter itself be marked CLOSED.


## Phase 1 recovered25 world-profile adapter closure — 2026-09-30

- The previously pending bundle-backed adapter seam is now closed on the verified recovered25 preservation bundle.
- GitHub Actions **36711569243 = PASS** completed the full recovered transport workflow, including the dedicated `Smoke recovered25 local runtime adapter` step.
- The derived aggregate report is committed as `research/recovered/STONEAGE-25-LOCAL-RUNTIME-ADAPTER-SMOKE-R1.txt`.
- Closed runtime-adapter facts:
  - materializable floors = **826**;
  - active ordered classic Warp edges = **2724**;
  - deferred conditional classic Warp records = **14**;
  - dynamic recovered FREE-gate bindings = **3**;
  - state-gated bindings = **3**;
  - fresh-start seeds = **4**;
  - provenance-bearing region descriptors materialized in the adapter smoke = **4**;
  - state-gated allow decisions from legal current-player witnesses = **3 / 3**;
  - local runtime-session encode/decode round-trip = **closed**.
- Provenance separation remains enforced: Taiwan/Waei v1.0 is the historical foundation, while recovered25 remains `LATER_RECOVERED` and is not promoted to Taiwan-v1 membership.
- **RECOVERED25_WORLD_PROFILE_ADAPTER_R1 = CLOSED.**
- The concrete recovered25 map-plane source is already independently closed as `RECOVERED25_REGION_PAYLOAD_SOURCE_R1`.
- Next Phase-1 priority: compose these two closed layers into a single engine-neutral **recovered25 local runtime stack**. The stack must use the concrete DAT/LS2MAP region provider rather than descriptor-only materialization, retain all three dynamic state-gated transition bindings, expose all four fresh starts, and pass one bundle-backed bootstrap -> fresh-start -> concrete region -> gate evaluation -> local save/load smoke. Do not choose a rendering engine and do not recreate legacy MMO services.


## Phase 1 concrete recovered25 local runtime stack — 2026-09-30

- The closed runtime-bootstrap contract, recovered25 world-profile adapter and concrete DAT/LS2MAP region source are now composed behind one engine-neutral implementation entry point:
  - `tools/stoneage_recovered25_local_runtime_stack.py`;
  - `tools/stoneage_recovered25_local_runtime_stack_smoke.py`;
  - `tests/test_stoneage_recovered25_local_runtime_stack.py`.
- The stack owns no renderer and recreates no legacy MMO/account transport. It composes:
  - the version-tagged `recovered25` bootstrap profile;
  - the provenance-bearing **826-floor** topology;
  - the concrete recovered map-plane provider;
  - all **4** fresh-start seeds;
  - all **3** current recovered dynamic state-gated transition bindings/evaluations;
  - the versioned local runtime-session envelope.
- Bundle-backed validation uses the hash-pinned preservation bundle and exercises actual recovered data rather than descriptor-only fixtures:
  - fresh-start concrete regions materialized = **4 / 4**;
  - representative recovered payload formats exercised = **2 / 2** (client DAT three-plane + server LS2MAP two-plane);
  - state-gated legal witness decisions = **3 / 3**;
  - local session encode/decode round-trip = **closed**;
  - materializable floors remain **826**.
- Derived aggregate report: `research/recovered/STONEAGE-25-LOCAL-RUNTIME-STACK-R1.txt`.
- Validation: GitHub Actions **36714435213 = PASS**; derived-report commit = `4a497ae24006f217fffda07ce8ac839700682d81`.
- Provenance boundary remains unchanged: historical foundation = Taiwan/Waei v1.0; runtime world = recovered25; recovered25 evidence role = `LATER_RECOVERED`.
- **RECOVERED25_LOCAL_RUNTIME_STACK_R1 = CLOSED.**
- Next Phase-1 priority: add a minimal engine-neutral **local runtime session coordinator** above this stack. It should provide new-game/continue/save boundaries, materialize the current concrete region, execute ordinary one-cell movement only from an explicit collision verdict, preserve existing classic overlap-Warp semantics, and execute a state-gated dialogue transition only when the current coordinate lies inside its recovered source rectangle and the live gate evaluator allows it. Do not invent collision metadata, renderer behavior, UI, network services or account services.


## Phase 1 local runtime session coordinator — 2026-09-30

- A minimal engine-neutral application-service layer now sits above the closed recovered25 local runtime stack:
  - `tools/stoneage_local_runtime_session_coordinator.py`;
  - `tests/test_stoneage_local_runtime_session_coordinator.py`;
  - `docs/LOCAL-RUNTIME-SESSION-COORDINATOR-R1.md`.
- The authoritative state remains `stoneage.local-runtime-session.r1`; the coordinator provides:
  - new game from one of the four versioned hometown seeds;
  - save/continue through the existing `LocalPersistenceStore` port;
  - concrete current-region materialization;
  - same-floor non-zero one-cell walk commands;
  - reuse of the existing classic overlap-Warp implementation;
  - state-gated dialogue transition execution.
- Collision remains evidence-safe: ordinary walking requires an explicit `entry_allowed` verdict from a validated collision layer. The coordinator does **not** guess WALKABLE/HAVEHEIGHT semantics from raw DAT/LS2MAP IDs.
- State-gated dialogue transitions now require two independent conditions:
  1. current player coordinate lies inside the recovered binding source rectangle on the correct floor;
  2. the live transition evaluator allows the current player state.
- A future gate that reports non-empty `consumed_state` is rejected until its mutation semantics are implemented explicitly; no item/state consumption can be silently discarded.
- Validation: GitHub Actions **36715358875 = PASS**.
- **LOCAL_RUNTIME_SESSION_COORDINATOR_R1 = CLOSED.**
- Next Phase-1 priority: close the concrete **recovered25 collision-verdict coverage** needed by the coordinator. First audit all 826 materializable floors against recovered server LS2MAP + recovered `mapset.txt`, distinguishing uniquely resolvable server collision, no-server-map floors, divergent duplicate server copies and missing image metadata. Do not substitute Taiwan-v1 ADRN values or guess collision for uncovered recovered25 floors. Use the audit to decide whether a server-backed provider is sufficient or a separate recovered-client collision bridge is still required.


## Phase 1 recovered25 server collision coverage census — 2026-09-30

- The coordinator's collision seam has now been measured against the full **826-floor** materializable recovered25 runtime world using only recovered server LS2MAP + recovered `mapset.txt` WALKABLE/HAVEHEIGHT metadata.
- Bundle-backed validation: GitHub Actions **36715881079 = PASS**.
- Derived report: `research/recovered/STONEAGE-25-SERVER-COLLISION-COVERAGE-R1.txt`.
- Coverage:
  - materializable floors = **826**;
  - server-collision closed floors = **635**;
  - uncovered floors = **191**;
  - stable floors = **761**, of which **570** are server-collision closed;
  - supplemental floors = **65**, and **65 / 65** are server-collision closed;
  - server-collision closed cells = **5,042,761**;
  - ordinary walkable cells in those closed maps = **1,520,277**.
- Explicit uncovered classes:
  - **189** floors = `NO_SERVER_MAP`;
  - **2** floors = `DIVERGENT_SERVER_DUPLICATE`: **5540** and **31001**;
  - **0** = server dimension mismatch;
  - **0** = missing recovered mapset metadata.
- The two divergent duplicate floors are not silently selected. The 189 no-server floors are not assigned Taiwan-v1 ADRN collision semantics merely because they have client DAT payloads.
- The census therefore proves that a server-only collision provider can safely cover **635 / 826** floors, but cannot close the runtime-wide movement seam by itself.
- **RECOVERED25_SERVER_COLLISION_COVERAGE_R1 = CLOSED_WITH_EXPLICIT_GAPS.**
- Next Phase-1 priority: implement a provenance-safe recovered25 **server-backed collision provider** for exactly the 635 closed floors and bind it as an optional movement-verdict source above the local runtime stack/coordinator. It must fail closed on all 191 uncovered floors and on any future dimension/hash/metadata drift. After that provider passes bundle-backed movement smoke, investigate a separately versioned recovered-client collision bridge for the remaining client-DAT floors; do not substitute Taiwan-v1 ADRN data without direct recovered25 provenance.


## Phase 1 recovered25 server-backed collision provider — 2026-09-30

- The 635-floor server-collision closure is now executable at runtime through `tools/stoneage_recovered25_server_collision_provider.py`.
- The provider is composed into `Recovered25LocalRuntimeStack` and exposed to the application layer through `LocalRuntimeSessionCoordinator.walk_one_cell_with_server_collision()`.
- Runtime policy is strict:
  - only `SERVER_COLLISION_CLOSED` floors are accepted;
  - recovered LS2MAP bytes are SHA-verified again at use time;
  - topology dimensions must remain identical;
  - recovered `mapset.txt` must resolve every used image id;
  - divergent duplicate server maps and no-server-map floors fail closed;
  - dynamic character/item overability remains an explicit runtime input rather than being assumed absent.
- Bundle-backed provider validation:
  - materializable floors = **826**;
  - server-backed collision floors = **635**;
  - uncovered floors = **191**;
  - `NO_SERVER_MAP` = **189**;
  - `DIVERGENT_SERVER_DUPLICATE` = **2**;
  - coordinator server-backed movement witness = **PASS**;
  - uncovered-floor hard-reject witness = **PASS**.
- GitHub Actions **36717025634 = PASS**.
- Derived report: `research/recovered/STONEAGE-25-SERVER-COLLISION-PROVIDER-R1.txt`.
- **RECOVERED25_SERVER_COLLISION_PROVIDER_R1 = CLOSED_WITH_EXPLICIT_GAPS.**
- Next Phase-1 priority: audit the **191 server-uncovered stable DAT floors** against the same recovered25 client's `adrn_15.bin` collision attributes. Establish whether every tile/parts id that requires ADRN lookup is resolvable from recovered25 resources. This is a provenance/coverage audit only: do not yet declare Taiwan-v1 `readHitMap` semantics to be the recovered25 runtime algorithm unless version-appropriate algorithm evidence is separately established.


## Phase 1 recovered25 client ADRN collision-resource coverage — 2026-09-30

- The **191** materializable floors not covered by the unambiguous recovered server collision provider have now been audited against the **same recovered25 client's** `adrn_15.bin` rather than against Taiwan-v1 metadata.
- Bundle-backed validation: GitHub Actions **36718602902 = PASS**.
- Verified recovered25 ADRN surface used by the audit:
  - SHA-256 = `92d0137590d35a7a1f4fb11af3ad13bbc585813a4b0e1e3f933c397007fbff74`;
  - bytes = **18,765,120**;
  - 80-byte records = **234,564**;
  - final map-number index size = **10,159**;
  - duplicate nonzero map-number assignments retained by source-order last-write behavior = **514**.
- Coverage result over the 191 server-uncovered stable DAT floors:
  - client-ADRN collision-resource closed floors = **191 / 191**;
  - unresolved floors = **0**;
  - tile references requiring ADRN lookup = **501,781**;
  - parts references requiring ADRN lookup = **16,179**;
  - unresolved unique-id floor sum = **0**.
- Derived report: `research/recovered/STONEAGE-25-CLIENT-ADRN-COLLISION-COVERAGE-R1.txt`.
- The earlier unintegrated duplicate probe `stoneage_recovered25_client_collision_metadata_probe.py` was removed after this richer audited implementation superseded it; one canonical coverage path remains.
- This closes the **resource/metadata availability** question only. It does not yet assert that Taiwan-v1 `readHitMap/checkHitMap` behavior is byte-identical to recovered25 runtime behavior.
- **RECOVERED25_CLIENT_ADRN_COLLISION_RESOURCE_COVERAGE_R1 = CLOSED.**
- Next Phase-1 priority: establish a version-appropriate **recovered25 client hit-map algorithm provenance**. Use the recovered runtime binary/source-lineage evidence to decide whether the long-lived client `readHitMap/checkHitMap` algorithm can be promoted for recovered25. Keep this separate from the already closed resource coverage. If direct recovered25 proof remains unavailable, record the algorithm as an explicit descendant-stable reconstruction profile rather than silently claiming exact 2.5 binary semantics.


## Phase 1 recovered25 client hit-map algorithm provenance — 2026-09-30

- The remaining client-collision algorithm question has been audited against **three pinned public StoneAge client source lineages** at immutable Git commits:
  - BismarckDD/Stoneage `2f736808...`;
  - Signally190/sking-sacli `40cb67ef...`;
  - anson1788/stoneage `1997fc20...`.
- Automated audit: `tools/stoneage_client_hitmap_lineage_probe.py`; GitHub Actions **36720265401 = PASS**; derived report `research/recovered/STONEAGE-CLIENT-HITMAP-LINEAGE-R1.txt`.
- All **3 / 3** lineages expose one identical audited semantic feature signature for the active client `readHitMap/checkHitMap` family:
  - tile ADRN lookup for IDs > 99 plus the 60..79 exception;
  - small-code block set 1/2/5/6/9/10 and override code 4;
  - hit=0 block while preserving override, hit=2 override;
  - parts collision footprints;
  - the 15680..15732 hit=1 origin-only special case;
  - final EVENT_NPC blocking;
  - `checkHitMap` blocks value 1.
- All **3 / 3** also expose one identical audited `ADRNBIN/MAP_ATTR` structural feature signature. **2 / 3** pinned lineages explicitly retain an `_SA_VERSION_25` compile-time marker in the same client resource header family.
- This aligns with direct recovered25 resource evidence already closed in this repository: three-plane client DAT caches plus same-bundle 80-byte `adrn_15.bin`, whose collision-required IDs resolve for **191 / 191** server-gap floors.
- Evidence classification is deliberately bounded:
  - reconstruction profile = `RECOVERED25_DESCENDANT_STABLE_CLIENT_HITMAP_R1`;
  - status = **SUPPORTED_FOR_RECONSTRUCTION**;
  - exact recovered25 `sa_2903.exe` machine-code identity proof = **not established**.
- **RECOVERED25_CLIENT_HITMAP_ALGORITHM_PROVENANCE_R1 = CLOSED_AS_DESCENDANT_STABLE_RECONSTRUCTION_PROFILE.**
- Next Phase-1 priority: implement a recovered25 client-DAT collision provider for the **191** server-uncovered floors using this explicitly versioned descendant-stable profile and the same-bundle `adrn_15.bin`. Keep its provenance distinct from the exact server LS2MAP provider. Then compose a unified collision router that yields a verdict for all **826** materializable floors without silently changing evidence class.


## Phase 1 unified recovered25 collision routing — 2026-09-30

- The recovered25 runtime collision seam now closes across the entire **826-floor** materializable topology without flattening evidence classes.
- Canonical implementation layers:
  - `tools/stoneage_client_hitmap_core.py` — provenance-neutral audited descendant-stable client hit-map semantics;
  - `tools/stoneage_recovered25_client_collision_provider.py` — same-bundle recovered25 DAT + `adrn_15.bin` adapter for server gaps;
  - `tools/stoneage_recovered25_collision_router.py` — provenance-bearing floor router;
  - `Recovered25LocalRuntimeStack` — composes server provider + client fallback + router when the recovered ADRN path is supplied;
  - `LocalRuntimeSessionCoordinator.walk_one_cell_with_runtime_collision()` — the single unified movement entry point.
- Routing is strict and disjoint:
  - server-routed floors = **635**;
  - client descendant-stable reconstruction floors = **191**;
  - total routed floors = **826**;
  - provider overlap = **0**;
  - unrouted floors = **0**.
- Server routing retains recovered LS2MAP + recovered `mapset.txt` semantics where that path is unambiguous.
- Client fallback retains a different evidence class:
  - recovered25 DAT tile/parts/event planes = same-bundle direct evidence;
  - recovered25 `adrn_15.bin` = same-bundle direct evidence;
  - algorithm profile = `RECOVERED25_DESCENDANT_STABLE_CLIENT_HITMAP_R1`;
  - exact recovered25 `sa_2903.exe` machine-code identity proof = **0 / not claimed**.
- Full bundle-backed validation: GitHub Actions **36721791457 = PASS**.
- Updated derived stack report: `research/recovered/STONEAGE-25-LOCAL-RUNTIME-STACK-R1.txt` records **635 + 191 = 826**, **0** unrouted floors and a legal client-reconstruction movement witness.
- Existing server-provider smoke independently retains a legal server-backed coordinator movement witness and fail-closed witness for its 191 unsupported floors.
- Duplicate implementation seams introduced during parallel composition were removed: one neutral client hit-map core, one unified router, one canonical unified coordinator movement method remain.
- **RECOVERED25_UNIFIED_COLLISION_ROUTING_R1 = CLOSED.**
- Next Phase-1 priority: close the **dynamic occupancy / overability seam** above static collision routing. The unified router currently selects authoritative/reconstruction static collision by floor, while runtime characters/items/NPCs are a separate live-object layer. Audit the already recovered runtime placement/object model against the established character/item overability rules, then compose destination occupancy into unified movement without relabelling client static hit-map semantics as server semantics. Keep static collision provenance and dynamic object-overlap provenance separately inspectable.

## Phase 1 recovered25 initial NPC occupancy composition — 2026-09-30

- The runtime dynamic-occupancy seam above unified static collision routing now has a deterministic recovered25 **initial NPC population source** instead of starting from an empty live-object registry.
- Static and dynamic evidence remain separate:
  - static floor-entry collision is still routed across **635** recovered server LS2MAP/mapset floors plus **191** recovered client-DAT/ADRN descendant-stable reconstruction floors = **826 / 826**;
  - NPC destination overlap remains a live CHARACTER occupancy decision using the independently audited CHAR_ISOVERED lineage.
- The recovered25 NPC overability audit closes the initial state for all **3,856** stable-world placements across **33** functionsets:
  - Warp = **2,264** placements, STATIC_OVERABLE;
  - remaining **1,592** placements across 32 functionsets = INHERITED_DEFAULT_OVERABLE;
  - STATIC_BLOCKING = **0** placements;
  - DYNAMIC / UNRESOLVED / LINEAGE_DIVERGENT = **0** placements;
  - descendant default CHAR_ISOVERED = 1 is stable across all **3** pinned lineages;
  - direct template callback overability overrides = **0**.
- New canonical composition layer: tools/stoneage_recovered25_npc_initial_occupancy.py.
  - It composes the already-versioned recovered25 placement/template projection with tools/stoneage_versioned_npc_overability_profile.py.
  - Every row keeps recovered25 / LATER_RECOVERED placement provenance plus the separate pinned-descendant overability classification.
  - Stable runtime object identity is npc-placement:<placement_id>.
- Existing spawn-integrity policy is preserved rather than bypassed:
  - recovered placement rows = **3,856**;
  - deterministic initial occupancy rows with closed overability = **3,856 / 3,856**;
  - registry-seedable rows = **3,852 / 3,856**;
  - existing spawn quarantines = **4** (the previously recorded geometry/direction integrity cases);
  - all four quarantined rows still have closed overability; they are omitted only because their existing spawn projection is not runtime-admissible, not because occupancy semantics are unknown.
- Recovered25LocalRuntimeStack.from_verified_bundle() now composes the initial NPC occupancy manifest, and LocalRuntimeSessionCoordinator seeds it automatically into RuntimeDynamicOccupancyRegistry.
- Unified movement already queries that registry on every destination cell. Current recovered25 initial NPC rows are overable, so they remain inspectable live occupants without becoming invented blockers. Runtime mutations such as moved characters or future non-overable objects still update the registry explicitly.
- Validation:
  - local runtime session coordinator GitHub Actions **36733347708 = PASS**;
  - NPC overability lineage/runtime-composition GitHub Actions **36733353261 = PASS**;
  - full preservation-bundle region/runtime-stack regression GitHub Actions **36733284202 = PASS**, including deterministic runtime-stack tests, concrete bundle stack construction, **826-floor** region payload validation and collision-provider regressions.
- **RECOVERED25_INITIAL_NPC_OCCUPANCY_R1 = CLOSED_WITH_EXISTING_4_SPAWN_QUARANTINES.**
- Next Phase-1 priority: close the **live dynamic-occupancy lifecycle and persistence boundary**. The current stoneage.local-runtime-session.r1 save envelope serializes player/session state but not the mutable occupancy registry. Define a versioned, provenance-bearing way to rehydrate deterministic initial NPC seeds and persist only explicit live mutations that must survive save/load (for example moved characters, overability changes and future dropped non-overable items), without serializing static collision as dynamic state or inventing behavior-driven NPC movement/despawn semantics.



## Phase 1 live dynamic-occupancy save lifecycle — 2026-09-30

- The mutable live-object layer now has a versioned local-save contract instead of being lost across save/load.
- New canonical envelope: `stoneage.local-runtime-save.r1`, implemented by `tools/stoneage_local_runtime_save.py`.
- The existing `stoneage.local-runtime-session.r1` player/session payload remains embedded unchanged as the authoritative session sub-envelope; the new wrapper adds only dynamic-occupancy deltas.
- Occupancy persistence is baseline-relative and provenance-bearing:
  - deterministic recovered25 initial NPC occupancy is rehydrated from `RECOVERED25_INITIAL_NPC_OCCUPANCY_R1` rather than serialized wholesale;
  - unchanged initial occupancy produces **zero** removed IDs and **zero** upserts;
  - moved objects, explicit overability changes, removed baseline objects and newly created live objects are persisted as explicit deltas;
  - each upsert retains object identity, kind, position, overability and provenance;
  - the save records both the deterministic base-profile id and the live-registry semantic profile.
- Static collision is intentionally excluded from the save schema. The 635-server / 191-client-reconstruction collision routing remains reconstructed from the runtime stack, not copied into mutable session state.
- Restore is fail-closed:
  - base-profile drift is rejected;
  - live-registry profile drift is rejected;
  - duplicate removed IDs and duplicate upsert identities are rejected;
  - an object cannot be both removed and upserted;
  - removal of an ID absent from the deterministic base is rejected;
  - restored live positions are revalidated against the runtime topology before the coordinator accepts them.
- Coordinator lifecycle is now explicit:
  - `new_game()` resets occupancy to the deterministic initial baseline;
  - `save_game()` writes the session plus occupancy delta;
  - `continue_game()` rebuilds the deterministic baseline and reapplies the saved delta;
  - legacy `stoneage.local-runtime-session.r1` saves remain readable and rehydrate the current deterministic initial baseline with no invented live mutations.
- Recovered25 integration test proves the real **3,852-object** seedable initial NPC registry serializes as an empty occupancy delta, while an explicit mutation produces exactly the corresponding upsert.
- Validation on remote main:
  - local runtime session coordinator GitHub Actions **36735552707 = PASS**;
  - NPC overability / recovered25 initial-occupancy regression GitHub Actions **36735552760 = PASS**.
- Contract document: `docs/LOCAL-RUNTIME-SAVE-R1.md`.
- **LOCAL_RUNTIME_DYNAMIC_OCCUPANCY_SAVE_R1 = CLOSED.**
- Next Phase-1 priority: implement a minimal durable **filesystem-backed LocalPersistenceStore** for the single-player runtime. It must be engine-neutral, UTF-8 exact, atomic-replace on save, path-traversal safe, deterministic by logical save key, and schema-transparent so both current and legacy versioned payloads remain coordinator concerns rather than storage concerns. Do not add cloud sync, accounts, network services or renderer dependencies.


## Phase 1 durable local filesystem persistence — 2026-09-30

- The engine-neutral persistence port now has a durable local implementation: `tools/stoneage_local_filesystem_persistence.py`.
- `LocalFilesystemPersistenceStore` remains deliberately schema-transparent. It stores and returns opaque UTF-8 text; `stoneage.local-runtime-save.r1` versus legacy `stoneage.local-runtime-session.r1` dispatch remains owned by `LocalRuntimeSessionCoordinator`.
- Logical save keys are never inserted into a path. The normalized logical key is SHA-256 mapped to a fixed `<digest>.save.json` filename inside the configured root, so path-like keys cannot traverse outside that root.
- Save replacement is crash-resistant at the storage boundary:
  - write a same-directory temporary file;
  - flush and `fsync` the file;
  - atomically replace the destination with `os.replace`;
  - best-effort directory `fsync` where the platform permits it;
  - failed writes clean up their temporary file.
- Load behavior is fail-closed for non-regular/symlink slots and invalid UTF-8. Missing slots return `None`, matching the existing `LocalPersistenceStore` protocol.
- Deterministic tests cover protocol conformance, exact Unicode/newline round-trip, overwrite semantics, distinct logical keys, path-traversal resistance, missing slots and invalid input.
- Validation is wired into `.github/workflows/validate-stoneage-local-runtime-session-coordinator.yml`.
- Design record: `docs/LOCAL-FILESYSTEM-PERSISTENCE-R1.md`.
- Remote validation: local runtime session coordinator GitHub Actions **36736500216 = PASS**.
- **LOCAL_FILESYSTEM_PERSISTENCE_R1 = CLOSED.**
- The next application-state mutation seam was audited immediately after filesystem closure; see the following section.


## Phase 1 current state-gated transition mutation audit and restart persistence smoke — 2026-09-30

- The current recovered25 runtime bootstrap contains exactly **3** state-gated dialogue WarpMan transitions: the shadowed-branch ingress plus the two fresh-start hometown bridge transitions.
- All three are eligibility gates over normalized recovered `FREE` predicates. The runtime evaluator reads only current player level and held item template identities and returns an empty `consumed_state` map for both allowed and denied decisions.
- The two fresh-start hometown bridge bindings additionally carry explicit recovered audit metadata `event_action_side_effect_fields = 0`; their bootstrap records also keep money gating disabled and schedule/party gates absent.
- No current binding therefore requires item consumption, Stone deduction, flag mutation or grant mutation at transition execution time. Implementing a generic mutation engine here would be speculative infrastructure, not recovery-driven work.
- The coordinator's existing rejection of future non-empty `consumed_state` remains intentionally fail-closed. If a later recovered binding proves an action-stage mutation, that exact mutation type must be modeled before execution is enabled.
- Regression coverage now asserts empty `consumed_state` on the current recovered25 item and level+item gate evaluator paths.
- Durable persistence is also tested across **coordinator reconstruction**, not merely within one process object: a first coordinator writes `stoneage.local-runtime-save.r1` through `LocalFilesystemPersistenceStore`; a newly constructed stack/coordinator reads the same disk slot and restores both session flags and live occupancy delta.
- **CURRENT_RECOVERED25_TRANSITION_MUTATION_REQUIREMENT_R1 = CLOSED_NO_MUTATION_REQUIRED.**
- Next Phase-1 priority: add an engine-neutral **interaction discovery/dispatch boundary** above the coordinator. A presentation layer should be able to ask which recovered state-gated dialogue interactions are spatially available at the current player coordinate, inspect their provenance/eligibility, and execute a selected transition without hard-coding raw recovered coordinates or legacy NPC arguments in UI code. Keep discovery separate from execution, keep unconditional classic overlap-Warp movement unchanged, and do not choose a rendering engine yet.


## Phase 1 engine-neutral interaction discovery/dispatch — 2026-09-30

- The local runtime coordinator now exposes a presentation-safe discovery surface for recovered state-gated dialogue interactions without leaking recovered NPC argument strings or raw coordinate rectangles into UI code.
- `discover_state_gated_interactions(session)`:
  - validates the authoritative session first;
  - resolves the versioned recovered binding for each declared state-gated transition;
  - returns only bindings whose recovered source rectangle contains the current player coordinate;
  - evaluates the current live gate state without mutating player/session state;
  - returns semantic transition id, interaction kind, eligibility/reason, binding provenance and an `execution_supported` flag;
  - intentionally omits source rectangles, destinations and legacy NPC argument payloads from the presentation-facing object.
- `dispatch_state_gated_interaction(session, transition_id)` delegates to the existing canonical executor, which **repeats** spatial and live-gate checks. Discovery is therefore not an authorization token and cannot become stale permission.
- A future allowed gate with non-empty `consumed_state` may still be discovered but is marked `execution_supported = false`; canonical execution continues to fail closed until that exact recovered mutation semantics is implemented.
- Classic overlap-Warp remains exclusively in ordinary movement; no second unconditional Warp path was introduced.
- Deterministic tests cover: no interaction outside source geometry, semantic/provenance-only discovery inside source geometry, denied/allowed eligibility, non-mutation during discovery, dispatch through the canonical executor, and future-mutation unsupported signaling.
- Remote validation: local runtime session coordinator GitHub Actions **36737733087 = PASS**.
- **LOCAL_RUNTIME_INTERACTION_DISCOVERY_DISPATCH_R1 = CLOSED.**
- The application command/result facade was implemented immediately after interaction-discovery closure; see the following section.


## Phase 1 engine-neutral local application facade — 2026-09-30

- A narrow presentation/input boundary now sits above `LocalRuntimeSessionCoordinator`: `tools/stoneage_local_application_facade.py`.
- The facade has no recovered25-specific imports. A future engine adapter can drive the runtime without importing world-profile adapters, collision providers, recovered NPC parsers, bootstrap derivation tools or save codecs.
- R1 facade surface is intentionally small:
  - new game;
  - continue;
  - save;
  - current-region read;
  - combined read view = authoritative session + materialized current region + discovered semantic interactions;
  - one-cell movement through the canonical unified collision/occupancy path;
  - state-gated interaction discovery;
  - semantic interaction dispatch.
- Movement cannot bypass collision authority: the facade does not expose the lower-level explicit `entry_allowed` seam and always calls `walk_one_cell_with_runtime_collision()`.
- Interaction dispatch cannot bypass recovered geometry/gates: it delegates to the coordinator dispatcher, which revalidates source geometry and live eligibility.
- The facade exposes no raw recovered source rectangle, NPC argument string, collision decoder or direct mutable runtime registry.
- No renderer, window toolkit, scene graph, input library, audio layer or asset pipeline has been selected.
- Design record: `docs/LOCAL-APPLICATION-FACADE-R1.md`.
- Remote validation: local runtime session coordinator GitHub Actions **36738166002 = PASS**.
- **LOCAL_APPLICATION_FACADE_R1 = CLOSED.**
- The semantic engine-adapter contract was implemented immediately after facade closure; see the following section.


## Phase 1 semantic engine-adapter contract — 2026-09-30

- The first presentation/input contract is now implemented without selecting an engine: `tools/stoneage_local_engine_adapter.py`.
- Semantic input intents are limited to: new game, continue, save, one-cell directional move, interaction dispatch and view refresh.
- `MoveIntent(dx,dy)` is a one-cell direction intent, **not** an authoritative destination write. The adapter derives the destination from the current authoritative session and delegates movement to the application facade's unified-collision path.
- Every accepted intent yields `LocalEngineUpdate`: semantic event kind + fresh `LocalApplicationView`, with walk/transition result details attached only when relevant.
- The adapter owns only the active immutable session reference needed for presentation flow. New game/continue replace it; movement/interaction replace it with the canonical result returned from the core. Save/refresh/move/interaction fail closed when no active session exists.
- Dependency boundary is enforced by regression: this module imports neither recovered25-specific modules nor Godot/Unity/input/rendering frameworks.
- Design record: `docs/LOCAL-ENGINE-ADAPTER-CONTRACT-R1.md`.
- Remote validation: local runtime session coordinator GitHub Actions **36738656157 = PASS**.
- **LOCAL_ENGINE_ADAPTER_CONTRACT_R1 = CLOSED.**
- The presentation-engine requirements audit was completed immediately after semantic-adapter closure; see the following section.


## Phase 1 presentation-engine requirements audit — 2026-09-30

- Current official engine/toolchain evidence was re-checked on 2026-09-30 rather than relying on old assumptions.
- Audit candidates: Godot 4.7.2 stable, Unity 6.3 LTS/current Unity 6 update stream, Defold 1.13.x, MonoGame 3.8.5.1.
- All four can technically deliver a Windows 2D single-player game. The decisive differences are editor/tooling burden, licensing/autonomy, runtime language fit and how much infrastructure the project must own.
- **Godot 4.7.2 is the primary presentation spike candidate**, not yet a production lock-in:
  - dedicated 2D renderer/tooling, tile maps, sprites and animation;
  - first-class Windows builds;
  - MIT engine license;
  - Standard and .NET builds, preserving a possible C# production-core route;
  - low pressure to move deterministic authority into the renderer because the semantic facade/adapter is already closed.
- Defold is retained as the lightweight secondary candidate; Unity as the mature proprietary/C# fallback; MonoGame as the high-control/high-tooling-burden baseline rather than the first presentation choice.
- Full evidence, requirement matrix and official-source snapshot: `docs/PRESENTATION-ENGINE-REQUIREMENTS-AUDIT-R1.md`.
- **PRESENTATION_ENGINE_REQUIREMENTS_AUDIT_R1 = CLOSED.**
- Next Phase-1 priority: close the **production runtime language/hosting boundary** before writing engine-specific scenes. Determine which Python modules remain reconstruction/reference tooling and define a parity-safe path for a production deterministic core. Explicitly evaluate a standalone C# core because Godot .NET, Unity and MonoGame can all host it, while preserving Python as an executable oracle through versioned golden fixtures. Do not embed Python in the shipped runtime by default and do not start a Godot production port until this boundary is documented.


## Phase 1 production runtime language/hosting boundary — 2026-09-30

- Repository composition confirms that Python is primarily the reconstruction/evidence laboratory, not a sensible monolithic shipping runtime: approximately **1,093** Python files at this snapshot, including **546** tests and roughly **404** probe/scan/audit/extract-style tools by filename; only a small subset is direct local/runtime infrastructure.
- The language boundary is now explicit:
  - **Python archaeology/build-time tooling remains Python**;
  - closed Python deterministic models remain the **executable reference oracle** during migration;
  - the preferred production deterministic target is a **standalone engine-agnostic C# core**;
  - a future concrete presentation engine stays downstream of that core/facade.
- C# is preferred because the current primary spike candidate (Godot .NET), Unity fallback and MonoGame control baseline can all host the same language/core, preserving engine optionality.
- Raw recovered StoneAge bundles/probe parsers are not intended gameplay-runtime dependencies. Production consumes normalized versioned artifacts generated/audited at build time with provenance intact.
- Embedding Python in the shipped game is **not** the default architecture; it requires a future measured justification if ever reconsidered.
- No big-bang rewrite: each production subsystem must pass cross-language golden semantic fixtures before it supersedes its Python reference counterpart.
- Architecture record: `docs/PRODUCTION-RUNTIME-LANGUAGE-HOSTING-R1.md`.
- **PRODUCTION_RUNTIME_LANGUAGE_HOSTING_R1 = CLOSED.**
- Next Phase-1 priority: implement `STONEAGE_RUNTIME_GOLDEN_CONTRACT_R1`, a copyright-safe versioned semantic fixture set generated/verified by the Python reference and designed to be consumed unchanged by future standalone C# parity tests. Cover session serialization, movement/Classic Warp, dynamic occupancy/save delta and semantic intent sequencing without depending on proprietary recovered bundle bytes.


## Restoration-first priority lock — 2026-10-01

- Project sequencing is now explicitly locked: **finish historical/gameplay reconstruction first; discuss and choose the new StoneAge production engine/content redesign only after reconstruction reaches an agreed acceptance point.**
- The completed Godot/C#/golden-contract work remains valid architecture research and migration protection, but it is **not the active development critical path**.
- Do not create a standalone C# production port, Godot scenes, final UI/assets, or redesigned gameplay while the restoration backlog still contains material core-game gaps.
- Current restoration evidence is already broad: the accepted Taiwan-v1 foundation client anchors direct client behavior, while recovered25 and pinned descendant source provide explicitly version-tagged bridge evidence for world/master/server semantics.
- Placement-weighted recovered NPC audit currently classifies **3,856** stable-world placements: **3,710 CLOSED_ORDINARY_CORE**, **84 NO_DISPATCH_PROFILE**, **62 DEFERRED_VERSIONED_PACKAGE**, **0 unclassified**. This means the priority is runtime integration of already-closed semantics, not another broad NPC archaeology sweep.
- The current recovered25 local runtime stack already composes: world materialization, provenance-safe static collision routing, Classic Warp/state-gated WarpMan, 3,852 seedable live NPC occupancy rows, local save/continue, and presentation-neutral application boundaries.
- The largest immediate gameplay restoration gap is that the already reconstructed **encounter -> enemy group spawn -> battle -> settlement** path still lives beside, rather than inside, the recovered25 local runtime stack/coordinator.
- **ACTIVE RESTORATION PRIORITY:** integrate versioned encounter data into the recovered25 runtime composition, then bridge movement-triggered encounter requests into the existing deterministic single-player battle shell without inventing RNG/AI/content. Preserve the known stable-world 23 positive unresolved group references across 19 encounter areas as fail-closed evidence defects.
- Production-engine/C# migration remains deferred until restoration acceptance.


## Cross-language golden contract CI closure — 2026-10-01

- The auxiliary migration-safety contract `stoneage.runtime-golden.r1` is now remotely validated.
- GitHub Actions **36741335484 = PASS** at commit `1e7a751a0a84d18e5529ca65511d1d454ca332c1`.
- The previous failed run **36741219902** was a CI invocation-path defect only: both unittest cases passed, while direct file execution lacked the repository module root. The workflow was corrected to execute the verifier with `python3 -m tools.stoneage_runtime_golden_contract`.
- **STONEAGE_RUNTIME_GOLDEN_CONTRACT_R1 = CLOSED.**
- Under DD-018 this remains migration protection only; C# production-port work is deferred while restoration gaps remain.


## Phase 1 recovered25 encounter runtime composition — 2026-10-01

- Restoration priority has moved from presentation/production architecture back to original-gameplay integration.
- New loader: `tools/stoneage_recovered25_encounter_runtime.py`.
- It composes the already verified stable-later map lineage + versioned world geometry with the active recovered25 `encount/group/enemy` files selected by `setup.cf`.
- The full recovered25 local-runtime composition supplies the verified server data directory and carries a `VersionedEncounterRuntimeAdapter` alongside map/collision/Warp/NPC occupancy services; subsystem-only stack smokes may omit encounter composition.
- New stack-level deterministic encounter calls:
  - `historical_domain_for_session()`;
  - `request_encounter_group(..., group_roll)`;
  - `request_encounter(..., group_roll, enemy_roll, level_roll)`.
- No RNG is generated internally and no missing content is synthesized.
- The known stable-world specimen defects remain fail-closed: **402** encounter areas, **23** positive unresolved group references, **19** affected encounter areas.
- Bundle-backed runtime smoke now requires both a legal group-resolution witness and a legal enemy-variant/level-resolution witness.
- Design record: `docs/RECOVERED25-ENCOUNTER-RUNTIME-R1.md`.
- Remote bundle validation: GitHub Actions **36745555249 = PASS**. The real stack smoke proved **402** stable encounter areas, **23** positive unresolved group refs across **19** affected areas, plus legal group and enemy-variant/level runtime witnesses.
- **RECOVERED25_ENCOUNTER_RUNTIME_R1 = CLOSED.**
- Next restoration priority after CI closure: connect the already reconstructed movement-side encounter frequency/CEP loop to the local session coordinator, preserving explicit deterministic rolls and Classic-Warp encounter suppression. Then attach the existing battle shell; do not invent AI/RNG or redesign content.


## Phase 1 movement-side CEP integration — 2026-10-01

- The recovered encounter content layer is now joined to the local movement coordinator through the separately reconstructed descendant **CEP (Current Encounter Probability)** loop.
- New coordinator result: `LocalRuntimeEncounterWalkResult`, containing the canonical walk result plus CEP decision and optional resolved group/enemy encounter requests.
- New deterministic coordinator entry point: `walk_one_cell_with_runtime_collision_and_encounter_frequency()`.
- Ordering is preserved from the closed descendant model:
  - static + live-occupancy movement resolves first;
  - blocked movement does not advance CEP;
  - after a successful step, encounter min/max is refreshed from the **departure coordinate** when an encounter area exists;
  - CEP clamps before the explicit `0..119` roll;
  - ordinary Classic Warp still performs the CEP roll but suppresses encounter dispatch;
  - a miss increments toward max;
  - an actual unsuppressed hit resets CEP to min and resolves group/enemy/level using explicit caller-supplied rolls.
- CEP remains **transient runtime/connection state**. It is not added to `stoneage.local-runtime-session.r1` or `stoneage.local-runtime-save.r1`; new-game and continue-game runtime establishment reset CEP to zero.
- This does not promote CEP to Taiwan-v1/JSS launch fact. Exact CEP provenance remains strong stable-descendant evidence with earliest-commercial presence still open.
- No RNG is generated inside the coordinator; frequency/group/enemy/level rolls remain explicit deterministic inputs.
- Regression coverage includes miss→increment, hit→reset+encounter, Classic-Warp suppression, blocked-walk no-op, and save/continue exclusion/reset of CEP.
- Remote validation: GitHub Actions **36746339200 = PASS**, **36746339083 = PASS**, and full bundle-backed recovered25 validation **36746339177 = PASS**.
- **LOCAL_RUNTIME_CEP_ENCOUNTER_BRIDGE_R1 = CLOSED.**
- Next restoration priority after CI closure: connect the resolved encounter request to the existing deterministic enemy-spawn/battle shell, preserving explicit birth/spawn/AI/round rolls and returning battle settlement to the authoritative local session without inventing new combat rules.


## Phase 1 enemybase text-encoding audit — 2026-10-01

- The next battle-integration seam requires concrete recovered25 `enemybase` templates because enemy spawn materialization depends on template identity, SIZE, growth bases, elements, skill slots and the real enemy/pet display name.
- Numeric identity is already structurally strong: active `enemybase.txt` contains **988 rows and 988 unique TEMPNO values** in the committed probe.
- The first of six string columns is already treated as NAME by the executable enemybase fixture/model, but runtime decoding must not be guessed from locale.
- Existing stable-map header audit independently shows all 572 admitted recovered25 server-map names are strictly decodable as both CP950 and Big5, but this evidence is **not automatically promoted** to enemybase.
- New anonymous audit: `tools/stoneage_enemybase_name_encoding_probe.py`.
- It records only row counts, strict-decoding counts, raw-name hashes and CP950-vs-Big5 equivalence; it emits no raw or decoded names.
- Closure rule for runtime use: all 988 active names must decode strictly under CP950 and Big5, and the decoded text must be identical row-for-row. Otherwise enemybase runtime naming remains OPEN.
- Remote bundle audit **36748411361 = PASS**. Results: CP950 **988/988**, Big5 **988/988**, but **2 rows decode to different Unicode text**; therefore automatic text-decoder selection remains unresolved.
- **RECOVERED25_ENEMYBASE_NAME_ENCODING_R1 = OPEN_CP950_BIG5_TWO_ROW_AMBIGUITY.**
- If closed, next restoration step is a version-tagged enemybase template loader feeding the existing enemy-spawn/birth/battle shell. No placeholder enemy names may be invented.


## Phase 1 recovered25 numeric enemybase runtime — 2026-10-01

- Enemy/pet display-name decoding is explicitly separated from combat mechanics.
- New loader: `tools/stoneage_recovered25_enemybase_runtime.py`.
- It loads the active recovered25 enemybase numeric/template prefix into `PetTemplateBridge` values while forcing `name=None`; no CP950/Big5 choice and no placeholder name is invented.
- Provenance remains `LATER_RECOVERED` / source profile `recovered25`.
- Runtime validation requires unique TEMPNO identity and checks the stable encounter closure from positive encounter groups -> enemy IDs -> enemybase TEMPNO.
- The full recovered25 stack now carries `enemybase_runtime` whenever `server_data_dir` is supplied.
- Bundle smoke requires **988** loaded enemybase templates and **0** unresolved enemybase template identities across the stable encounter runtime.
- Enemy names remain a presentation-layer OPEN issue until the two CP950/Big5 divergent rows are independently disambiguated.
- First bundle run **36749082734** reached the completed stack execution without any template-gap exception; it failed only in the final reporter because a run-local template-count variable was referenced from `main()`. The reporter scope bug is corrected in the next validation.
- Corrected bundle validation **36750049192 = PASS**. The stack smoke proves **988** loaded enemybase templates and **0** unresolved enemybase TEMPNO identities across the stable encounter runtime.
- **RECOVERED25_NUMERIC_ENEMYBASE_RUNTIME_R1 = CLOSED.**
- If the template join closes, proceed to group spawn/birth materialization and battle-shell integration with names nullable for enemy-side participants only; player and owned-pet names remain mandatory.


## Phase 1 recovered25 group spawn/birth bridge — 2026-10-01

- The next restoration seam now composes the existing closed models rather than inventing new combat behavior:
  `GroupEncounterRequest -> plan_enemy_spawns -> recovered25 enemybase template -> build_pet_birth_bridge -> SpawnedEnemy/BattleParticipant`.
- New stack entry point: `spawn_group_enemies(...)`.
- All random values remain explicit inputs:
  - requested enemy count;
  - weighted enemy-variant selection rolls;
  - per-enemy level roll;
  - four birth offsets;
  - ten spawn-allocation rolls.
- The bridge validates encounter area identity, position, group identity, enemy-count boundary and enemybase TEMPNO before materialization.
- Because enemybase name decoding still has a two-row CP950/Big5 ambiguity, enemy-side `BattleParticipant.name` is now allowed to remain `None`. Player and owned-pet names are still mandatory through the existing `_require_name()` path.
- No synthetic/fallback enemy name is emitted.
- Bundle smoke is extended to require a real stable-world one-enemy spawn/birth witness using the hash-pinned recovered25 specimen.
- Remote validation: gameplay model **36750049233 = PASS**, coordinator regression **36750049393 = PASS**, and full hash-pinned bundle validation **36750049192 = PASS**. The concrete stack smoke produced a real `ENEMY_SPAWN_BIRTH_RUNTIME_WITNESS`.
- **RECOVERED25_GROUP_SPAWN_BIRTH_BRIDGE_R1 = CLOSED.**
- After closure, connect the spawned participants to `begin_group_battle()` in the local session coordinator, then return explicit battle settlement into a newly cloned persistent session state.


## Phase 1 transactional local group battle context — 2026-10-01

- The recovered movement/encounter/spawn chain is now connected to the existing group-battle shell at the authoritative local-session boundary.
- New transient contract: `LocalRuntimeBattleContext`.
- `start_group_battle()`:
  - validates current session and encounter position;
  - snapshots persistent player-owned state through the existing versioned persistence codec;
  - works on a decoded clone rather than the caller's session object;
  - delegates explicit group spawn/birth rolls to `stack.spawn_group_enemies()`;
  - enters the existing `begin_group_battle()` shell.
- `settle_group_battle()` accepts only the transient context plus an explicit `BattleOutcome`; it reapplies the snapshot to a fresh domain and returns a **new** local session.
- The original input session remains unchanged, so incomplete/aborted battle work cannot silently mutate the authoritative save state.
- Active battle state remains transient and is not added to `stoneage.local-runtime-save.r1`.
- No AI, commands, initiative randomness, attack rolls, capture/escape rolls, drops or outcome are generated here.
- Coordinator CI is widened so enemy-spawn, battle, persistence and numeric enemybase changes rerun this integration boundary.
- Remote validation: coordinator **36751047244 = PASS** and runtime golden contract **36751047462 = PASS**; the parallel full recovered25 bundle regression remains an additional data-stack check rather than a prerequisite for the transaction semantics.
- **LOCAL_RUNTIME_GROUP_BATTLE_CONTEXT_R1 = CLOSED.**
- Next restoration priority after CI closure: attach the already reconstructed persistent ordinary-round battle state to this context using explicit commands/initiative/attack rolls, then return its validated terminal settlement through the same cloned-session transaction boundary. Do not invent enemy AI.


## Phase 1 persistent ATTACK/WAIT battle rounds — 2026-10-01

- The local battle context is extended with optional `PersistentBattleState`.
- New coordinator entries:
  - `begin_persistent_group_battle(context, slots=...)`;
  - `resolve_persistent_attack_wait_round(...)`;
  - `settle_persistent_group_battle_without_level_crossing(context)`.
- R1 intentionally accepts only explicit ATTACK/WAIT commands. Capture, escape, items, skills, guard/combo and AI-command generation remain outside this seam.
- Every ordinary round still requires caller-supplied commands, initiative random subtracts, combat profiles and attack rolls. No RNG or enemy decision is generated by the coordinator.
- The existing persistent battle model remains authoritative for cross-round HP, turn count, status runtime, pending EXP, enemy removal and terminal victory/defeat.
- Terminal settlement reconstructs the pre-battle persistent-state snapshot and returns a new local session; the input session is never mutated.
- Below-threshold EXP may settle through the existing `finish_persistent_battle_without_level_crossing()` path. Level-threshold crossing remains fail-closed until the progression seam is explicitly connected.
- Regression target: a deterministic multi-round player ATTACK vs enemy WAIT battle must survive at least one nonterminal round, reach automatic victory later, carry pending EXP, and settle into a new session while the original session remains unchanged.
- Coordinator workflow now watches/runs the battle-round, persistent-state, single-player runtime and group-battle regression surfaces.
- Remote validation after correcting the terminal enemy-HP assertion: coordinator **36752621438 = PASS**; the prior `36752505766` failure was test expectation only, while golden contract **36752505709 = PASS**.
- **LOCAL_RUNTIME_PERSISTENT_ATTACK_WAIT_R1 = CLOSED.**
- Next restoration priority after CI closure: connect explicit escape and capture seams one at a time, then expose already-recovered AI selection only after its evidence boundary is separately audited. Do not synthesize enemy commands.


## Phase 1 explicit player escape round — 2026-10-01

- Escape is selected as the next battle branch because its strong stable-descendant mechanics and dedicated settlement are already closed, and it does not require unresolved enemy-name decoding or construction of a complete captured-pet record.
- New coordinator entries:
  - `resolve_persistent_escape_round(...)`;
  - `settle_persistent_escape(context)`.
- R1 requires the player command to be explicit `BATTLE_COM_ESCAPE`; all other living actors remain caller-supplied ATTACK/WAIT commands.
- The caller supplies `OrdinaryEscapeContext`, `OrdinaryEscapeRolls`, initiative inputs, profiles and any attack rolls. No RNG or enemy decision is generated.
- The source counter ordering is preserved: first stored count 0 increments to 1 before the check; success retains stored count 1.
- Successful escape produces terminal result `escape` and uses the existing dedicated escape settlement, which does **not** award normal pending EXP or item profit.
- The original pre-battle local session remains immutable; settlement returns a new session.
- Enemy escape remains outside this local R1 boundary until AI/behavior evidence is connected.
- Remote validation: coordinator **36753012126 = PASS** and golden contract **36753012150 = PASS**.
- **LOCAL_RUNTIME_PLAYER_ESCAPE_R1 = CLOSED.**
- Next after CI: connect capture as a separate transaction because successful capture requires a complete provenance-bearing `PetActor`; do not fabricate MP, skills, name, EXP threshold or visible-AI/compliance fields.


## Phase 1 transactional player capture round — 2026-10-01

- Capture is connected after escape because the stable-descendant capture equation, target/slot ordering and persistent-pet install path are already closed, while complete captured-pet data must still remain caller/provenance supplied.
- `LocalRuntimeBattleContext` gains optional `working_persistent_state_payload` so battle-time persistent mutations such as successful capture survive later settlement without modifying the original pre-battle session.
- New coordinator entry: `resolve_persistent_capture_round(...)`.
- R1 requires an explicit player `BATTLE_COM_CAPTURE`; all other living actors remain caller-supplied ATTACK/WAIT commands.
- Capture context, capture roll, combat profiles and any attack rolls remain explicit inputs.
- A successful capture requires `captured_pets_by_target_id` containing the complete source-identified `PetActor`; the existing runtime verifies first-empty slot, source variant/template identity and copied level/current HP/max HP before installing it.
- Missing/extra captured-pet mappings fail atomically. The original local session and the input battle context remain unchanged.
- All coordinator battle settlement paths now use the working persistent payload when one exists, so successful captures survive battle completion.
- No placeholder MP, skill list, EXP threshold, display name or AI/compliance state is fabricated.
- Coordinator CI now watches/runs the standalone capture model and capture research seams in addition to the persistent group-battle regression.
- Remote validation after the syntax-only test fix: coordinator **36753606390 = PASS**; golden contract on the capture commit **36753460790 = PASS**. The prior **36753460775** failure was an unmatched-parenthesis test syntax defect only.
- **LOCAL_RUNTIME_PLAYER_CAPTURE_R1 = CLOSED.**
- Next after CI: audit whether the existing capture-to-owned-pet adapter can be populated from recovered25 enemy/birth/petskill/EXP data without guessing fields; if not, keep complete captured-pet construction outside runtime and move to explicit defeat/death recovery integration.


## Captured-pet automatic construction audit — 2026-10-01

- The runtime transaction for capture is CLOSED, but automatic construction of a complete owned `PetActor` from the current recovered25 wild-enemy battle object is **not** closed.
- Existing recovered bridges can reconstruct template identity, birth/growth identity, current combat HP/attack/defense/quick, elements, skill template IDs and PETRANK/ALLOCPOINT lineage.
- However `build_reconstructed_pet_state()` still requires explicit unresolved runtime values including MP, max MP, EXP, max EXP, rename flag, free name and a resolved display name; capture evidence also copies current status/skill runtime fields that are not carried by the current `BattleParticipant`.
- Enemybase name decoding remains OPEN for two CP950/Big5-divergent rows.
- Therefore the coordinator continues to require a complete provenance-bearing caller-supplied `PetActor` on successful capture.
- **CAPTURED_PET_AUTOCONSTRUCTION_R1 = OPEN_MISSING_CURRENT_STATE_FIELDS.**
- No MP, skill runtime, EXP threshold, display name or visible-AI/compliance state may be fabricated to close this gap.


## Phase 1 explicit battle defeat settlement — 2026-10-01

- The next restoration seam is battle defeat/death recovery, not automatic captured-pet construction.
- New coordinator entry: `settle_persistent_defeat(context)`, which accepts only terminal result `defeat`.
- Regression drives an actual ordinary enemy ATTACK against a player WAIT with all commands/initiative/attack rolls explicit.
- For the level-5 no-active-pet fixture, the already recovered stable normal-death model applies `CH_FIX_PLAYERDEAD=-2` with the <=10 level divisor 2, producing pending charm delta **-1**.
- Terminal defeat must retain player HP 0 in battle state; settlement returns persistent HP **1**, applies charm 5 -> **4**, awards no pending EXP, preserves world position/flags, and leaves the original pre-battle session unchanged.
- This closes only the battle/BATTLE_Exit defeat boundary.
- Separate `core_Dying` field/player death behavior remains its own reconstruction seam: party discharge, equipment/gold drop requests, death count/status flags and resurrection are modeled, but exact launch-era client death-screen / return-to-record-point choreography remains OPEN.
- Coordinator CI now watches/runs the player death/revival core.
- Remote validation after correcting the fixture below the Ultimate threshold: coordinator **36754751074 = PASS**; the earlier **36754415152** failure used attack=10000 and therefore exercised Ultimate/overkill rather than normal death.
- **LOCAL_RUNTIME_BATTLE_DEFEAT_R1 = CLOSED.**
- Next after CI: integrate the closed `core_Dying` transition as a separate field-death transaction without inventing automatic savepoint movement; keep return-to-record-point as an explicit/open presentation/world-flow choice until direct evidence closes it.


## Phase 1 explicit core_Dying / resurrection boundary — 2026-10-01

- Battle defeat and field/player death remain separate operations; no automatic chaining is asserted.
- New coordinator result contracts:
  - `LocalRuntimePlayerDeathPlan`;
  - `LocalRuntimePlayerResurrectionResult`.
- New explicit methods:
  - `plan_player_core_dying(...)`;
  - `resurrect_player_in_place(...)`.
- `plan_player_core_dying()` delegates the convergent descendant `death_transition()` model using explicit attacker class, equipped slots and prior hidden death count.
- The current local persistent model has no authoritative party/equipment container and no dedicated hidden player-death/status structure. Therefore those core_Dying effects are returned as semantic/world-action requests instead of being fabricated into unrelated fields.
- The Taiwan-v1 direct player `gold` field **is** representable. Death planning clones the persistent state, requests half carried gold for ground placement, and sets carried gold to **0** even if the world-drop request later cannot be placed.
- Regression fixture: gold 101 -> requested ground gold 50 -> carried gold 0; enemy death requests all explicit equipped slots; hidden dead count 7 -> 8; six stable statuses are reported cleared.
- `resurrect_player_in_place()` applies only the recovered HP clamp/image/death-flag semantics that can be represented safely: requested HP <=0 -> HP 1, same position, MP unchanged. Hidden image/dead/attacked/overed flags are returned semantically rather than silently added to the save schema.
- Exact commercial `battle defeat -> core_Dying` invocation and death-screen / return-to-record-point choreography remain OPEN.
- **LOCAL_RUNTIME_CORE_DYING_RESURRECTION_R1 = IMPLEMENTED_PENDING_REMOTE_CI.**
- Next after CI: audit authoritative equipment/party/local hidden-player-state containers before applying the remaining core_Dying mutations. If those containers are not ready, move to the already recovered player/pet EXP progression settlement rather than inventing death-flow persistence.


## Phase 1 death-state container audit and explicit progression coordinator bridge — 2026-10-01

- Remote HEAD `3afd0301595e0cca1a2a241a3032725b6256ee05` was revalidated before continuation; its three relevant workflows were green: runtime golden contract **36755288378**, local runtime session coordinator **36755288256**, and recovered25 region payload **36755288531**. This closes the prior `LOCAL_RUNTIME_CORE_DYING_RESURRECTION_R1` remote-CI condition.
- The authoritative local persistent domain was audited before applying the remaining `core_Dying` effects. `PersistentPlayerState` currently owns only character, inventory, pets and dead-pet count. Party formation and equipment use/equip are reconstructed as separate reference models, but neither is yet an authoritative local-session persistence container; there is also no dedicated hidden player death/status container.
- Therefore party discharge, equipped-item drop mutation and hidden player-death/status counters remain semantic/world-action requests. They are **not** fabricated into unrelated persistent fields.
- Per the previous branch condition, restoration priority moved to the already-closed EXP progression settlement rather than expanding the save schema speculatively.
- New coordinator entry: `settle_persistent_group_battle_with_progression(...)`. It composes the existing atomic `SinglePlayerHistoricalRuntime.finish_persistent_battle_with_progression()` path into the authoritative local-session transaction boundary.
- Player EXP profile, future player thresholds, pet EXP profile, per-pet future thresholds and every pet growth-roll bundle remain explicit caller inputs. The coordinator owns no threshold table and generates no RNG.
- Implementation commit: `4b08287d3f4eabd3baca41ac1561c4948f6e2fe8`.
- **LOCAL_RUNTIME_DEATH_CONTAINER_AUDIT_R1 = CLOSED_NO_AUTHORITATIVE_CONTAINER.**
- **LOCAL_RUNTIME_BATTLE_PROGRESSION_COORDINATOR_R1 = IMPLEMENTED_PENDING_REMOTE_CI.**
- Next after CI: add/extend coordinator regression for a real terminal victory whose pending EXP crosses the player threshold, proving atomic level/EXP/max-EXP/free-point/charm/duel-state mutation while the original pre-battle session remains unchanged. Then cover pet threshold crossing only with explicit hidden growth identity and explicit growth rolls; do not infer the JSS-1999 threshold table.

## Phase 1 explicit battle progression coordinator transaction closure — 2026-10-01

- The progression coordinator implementation commit `4b08287d3f4eabd3baca41ac1561c4948f6e2fe8` passed local-runtime coordinator validation **36756571650**.
- Real terminal-victory player threshold crossing is now covered through the coordinator, not by a synthetic direct state edit. The regression begins from level 5 / EXP 950 / max EXP 1000, earns the actual pending **100 EXP** from the battle round, explicitly selects the descendant `legacy_cumulative` profile and supplies level-6 max EXP **1500**.
- Player settlement proves one atomic cloned-session transition: level 5 -> 6, EXP 950 -> 1050, max EXP 1000 -> 1500, free stat points 4 -> 7, charm 5 -> 7 and duel-point-like state 12 -> 72. The original pre-battle session remains unchanged. Commit `a1815293947fcf3692036c40ecab49b8be1dfbff`; coordinator validation **36756837107 = PASS**.
- Reward-only ride-pet threshold crossing is also covered through a real player kill. The player receives the source-shaped **100 EXP** award and the owned ride pet receives its recovered **60% = 60 EXP** side award without being promoted into an active allied battle actor.
- The ride-pet regression starts the pet at level 5 / EXP 950 / max EXP 1000 with explicit hidden `PetGrowthState`. It supplies the `legacy_cumulative` pet profile, explicit level-6 max EXP **1500**, and exactly one explicit `PetLevelGrowthRolls` bundle. No threshold table or growth RNG is generated by the coordinator.
- The deterministic growth bundle advances internal VITAL/STR/TOUGH/DEX **2000/2000/2000/2000 -> 2115/2110/2115/2110**, hidden VARIABLEAI **0 -> 500**, and projects max HP/attack/defense/quick to **147/26/26/21** while preserving terminal HP **100**. The original owned-pet snapshot remains unchanged. Commit `400fe3e269e4466188db938ef3cd9fe0634f2a2a`; coordinator validation **36757383029 = PASS**.
- These regressions validate explicit descendant progression profiles only. They do **not** promote either profile or the caller-supplied threshold numbers to an exact JSS-1999 progression table.
- **LOCAL_RUNTIME_BATTLE_PROGRESSION_COORDINATOR_R1 = CLOSED.**
- Restoration priority now returns to the deferred **enemy AI / enemy-command selection evidence boundary** identified after persistent ATTACK/WAIT closure. Audit the already recovered descendant enemy command-selection semantics and recovered25 `enemy.TACTICS` bridge before generating any enemy command in the coordinator. Keep caller-supplied enemy commands authoritative until that evidence boundary is explicitly versioned and tested.

## Phase 1 recovered enemy AI command-selection/runtime bridge — 2026-10-01

- The deferred enemy-command boundary identified after persistent ATTACK/WAIT closure has now been audited against the fixed stable-descendant source and the recovered25 `enemy.TACTICS/TACTICSOPTION` data path.
- The coordinator still generates no hidden randomness. Enemy AI mode rolls, target rolls, initiative inputs, ordinary attack rolls, escape rolls and ABIO inputs remain explicit caller inputs.
- `TACTICS == 1` common-normal AI is the only admitted enemy selector. Unsupported TACTICS modes and unresolved decision paths fail closed.
- ATTACK/GUARD closure:
  - recovered `at/gu` selection is converted to existing `BattleCommand` values;
  - GUARD execution is routed through the ordinary persistent-round resolver;
  - the source-shaped guard damage check continues to consume explicit `OrdinaryAttackRolls.guard_roll_1_100`;
  - coordinator validation after the RNG fixture correction: **36760656396 = PASS**.
- Enemy ESCAPE closure:
  - recovered `enemybase.RARE` is now preserved as numeric provenance in `PetTemplateBridge`;
  - fixed-source lineage confirms enemy creation writes enemybase RARE to `CHAR_RARE`, and the ordinary escape check reads that value;
  - enemy escape requires explicit `OrdinaryEscapeRolls` plus exact living-opponent ABIO coverage;
  - missing RARE, missing/extra escape rolls or incomplete ABIO mappings fail closed;
  - successful enemy escape removes the enemy without creating normal kill EXP;
  - coordinator validation: **36761759048 = PASS**.
- Recovered pet-skill runtime index:
  - new `tools/stoneage_recovered25_petskill_runtime.py` keeps only execution-facing ID/FIELD/TARGET/COST/ILLEGAL, callback and raw OPTION bytes; display name/comment strings are not retained;
  - fixed-source `petskillfile1/petskillfile2` ambiguity is fail-closed if the two configured paths resolve to different existing files;
  - hash-pinned recovered25 full-stack validation proves **147 active pet-skill entries**, **111 enemybase-referenced positive skill IDs**, and **0 unresolved referenced skill IDs**;
  - the full stack remains **RESOLUTION|RECOVERED25_LOCAL_RUNTIME_STACK_CLOSED**.
- Enemy skill-slot identity audit found that compacting positive `PETSKILL1..7` values is semantically unsafe:
  - active `enemybase.txt` contains **15 rows with positive skills after an empty earlier slot**;
  - sparse masks include cases where only slot 2, only slot 3, slots 3-7, or slots 2-7 are populated;
  - `PetTemplateBridge.skill_slot_ids` now preserves all seven positional IDs, while legacy `skill_ids` remains only a compact compatibility projection.
- Basic `wa` execution bridge:
  - AI `wa[0..6]` is interpreted as the exact seven-slot index, never as an index into compacted positive skill IDs;
  - `PETSKILL_NormalAttack` -> source-shaped ATTACK(target);
  - `PETSKILL_NormalGuard` -> source-shaped GUARD(target);
  - `PETSKILL_None` -> source-shaped `BATTLE_COM_NONE` with the selected target retained in COM2;
  - `BATTLE_COM_NONE` is now admitted by the ordinary resolver as an explicit no-action command rather than being rewritten to WAIT;
  - every other callback, empty selected slot, unresolved skill ID and missing recovered pet-skill runtime remains fail-closed.
- Relevant remote validation:
  - basic wa coordinator bridge **36763034120 = PASS**;
  - explicit NONE battle-core validation **36763545262 = PASS**;
  - standalone NONE pet-skill bridge **36763591375 = PASS**;
  - final coordinator import-fix validation **36763738745 = PASS**;
  - the prior **36763641544** failure was a test-only missing `BATTLE_COM_NONE` import, not a runtime defect.
- **LOCAL_RUNTIME_ENEMY_AI_ATTACK_GUARD_ESCAPE_BASIC_WA_R1 = CLOSED.**
- Remaining enemy-AI work is deliberately narrower than “implement all pet skills”: quantify which of the 111 recovered enemy-used skill IDs/slot uses map to the 15 already reconstructed common callbacks, then extend only callbacks whose command setup + ordinary-round execution contracts are already evidence-closed. OPTION encoding-dependent or stateful callbacks remain OPEN until their exact data/runtime requirements are carried explicitly.
- Immediate next priority: use the hash-pinned recovered25 aggregate coverage to choose the highest-impact next common callback. Reuse existing reconstructed Guardian/StatusChange/etc. seams where complete; do not invent generalized skill execution or silently downgrade unsupported skills to ATTACK/WAIT.

## Stable pet-skill NoGuard cross-action correction — 2026-10-01

- A continuation audit found that the earlier `STONEAGE-PETSKILL-CORE-R1.md` claim that NoGuard's packed COM3 parameters had no fixed common consumer was incorrect.
- All three pinned descendant lineages agree on the active cross-action behavior:
  - the NoGuard actor's own `BATTLE_COM_S_NOGUARD` turn still resolves through `BATTLE_NoAction`;
  - while defending, `HIGH(COM3)` is added to the dodge probability;
  - in the counter path, the upper byte of `LOW(COM3)` is added to counter probability;
  - `BATTLE_Counter` explicitly admits S_NOGUARD alongside ordinary ATTACK;
  - the lower-byte critical modifier is only read inside a `#if 0` disabled `BATTLE_CriticalCheckPet` helper, so it is not active in the pinned common execution path.
- The odd source sign rule is preserved exactly: extracted byte values above 127 are multiplied by -1 rather than converted as conventional signed bytes.
- `tools/stoneage_petskill_core_model.py`, its regression tests and `research/mechanics/STONEAGE-PETSKILL-CORE-R1.md` were corrected.
- Dedicated stable pet-skill validation **36764551385 = PASS**. The earlier **36764484553** failure was the expected intermediate commit where the corrected model preceded the updated regression expectation.
- NoGuard remains **not admitted** to the recovered enemy-AI runtime bridge because exact recovered OPTION parsing and its cross-action round integration have not yet been closed. It must not be downgraded to ordinary WAIT/NONE.
- **PETSKILL_NOGUARD_DEAD_PARAMETER_CLAIM = SUPERSEDED.**
- **PETSKILL_NOGUARD_CROSS_ACTION_SEMANTICS_R1 = CLOSED_REFERENCE_MODEL_ONLY.**

## Phase 1 recovered StatusChange enemy-AI execution — 2026-10-01

- Hash-pinned recovered25 aggregate evidence selected `PETSKILL_StatusChange` as the highest-impact remaining stable-common callback whose ordinary-round execution seam was already closed:
  - **6** referenced StatusChange skill IDs;
  - **174** positive enemybase skill-slot uses;
  - all **6/6** OPTION byte strings decode identically under strict CP950 and Big5;
  - **0** codec divergences and **0** strict-decode failures.
- The bundle-backed grammar probe now proves:
  - `unique_ids=6`;
  - `matched_status_ids=6`;
  - recovered source turn values span **3..5**;
  - all **6** rows carry attack-power modifiers;
  - **0** carry defense-power modifiers.
- This 6/6 grammar closure is now a hard runtime-stack/CI condition rather than a descriptive report only.
- Recovered OPTION text remains fail-closed: non-ASCII mechanics may consume it only through `unambiguous_cp950_big5_option()`; decoder disagreement is an execution error.
- New StatusChange enemy-skill bridge:
  - preserves the exact seven-slot `wa[n]` identity;
  - derives FIXSTR/FIXTOUGH-equivalent attack/defense values from the already preserved enemy birth projection rather than adding duplicate battle-participant fields;
  - parses only the fixed common ordinary status token set;
  - delegates command formation to the existing stable pet-skill model and round bridge;
  - emits `BATTLE_COM_S_STATUSCHANGE`, packed COM3 status/turn, and explicit command-setup effects.
- The common enemy-AI round now carries command setup effects separately from commands and admits recovered StatusChange in addition to None/NormalAttack/NormalGuard.
- Status application remains fully explicit:
  - target VITAL/STR/TOUGH/DEX and status resistances are caller-supplied `BaseStatusCombatProfile` values;
  - eligible `RAND(1,100)` status application is caller-supplied;
  - existing-status turn RNG remains caller-supplied when needed;
  - the battle core consumes no status RNG on dodge/zero-damage/ineligible status paths.
- Fixed-source `PETSKILL_Use` was re-audited before enabling the callback:
  - it resolves the selected pet-skill slot and callback;
  - it does **not** consume `FIELD`, `TARGET`, `COST` or MP before dispatch;
  - the common `ILLEGAL` check rejects `CHAR_TYPEPET` only, not `CHAR_TYPEENEMY`;
  - therefore no enemy MP/cost model is required or invented for this closure.
- End-to-end coordinator regression proves recovered AI selection -> StatusChange command -> positive physical hit -> explicit status check -> persistent poison state, and separately proves an eligible check without explicit RAND fails closed.
- Remote validation:
  - StatusChange bridge implementation **36766286297 = PASS**;
  - bridge regression **36766349167 = PASS**;
  - command/setup batch refactor coordinator **36766665030 = PASS** and golden contract **36766664730 = PASS**;
  - full hash-pinned recovered25 validation **36766665111 = PASS**;
  - integrated runtime commit coordinator **36767747307 = PASS** and golden contract **36767747363 = PASS**;
  - end-to-end StatusChange coordinator regression **36767877345 = PASS**.
- Executable recovered stable-common pet-skill slot-use coverage is now **1529 / 2486 = ~61.5%** when counting NormalAttack + NormalGuard + StatusChange slot uses. This is a skill-slot semantic coverage metric, **not** an encounter-frequency or action-probability estimate.
- **LOCAL_RUNTIME_ENEMY_AI_STATUSCHANGE_R1 = CLOSED.**
- Next priority: rank the remaining stable-common callbacks by recovered25 slot-use impact and execution-gap size. Current leading candidates are ContinuationAttack (**139** uses), Mighty (**120**), ChargeAttack (**90**), NoGuard (**74**), PowerBalance (**62**) and GuardBreak (**60**). Do not choose by count alone: Continuation requires multi-hit/retarget/counter-loop closure; NoGuard requires cross-action dodge/counter COM3 integration.

## Phase 1 recovered PowerBalance + Mighty enemy-AI execution — 2026-10-01

- Recovered25 aggregate evidence now closes two additional stable-common enemy `wa` callbacks.
- `PETSKILL_PowerBalance`:
  - **3** referenced skill IDs and **62** positive enemybase skill-slot uses;
  - all **3/3** OPTION rows have strict CP950/Big5 decode consensus;
  - all **3/3** contain both `攻%` and `防%`;
  - **0/3** contain the later/unclosed `敏%` extension marker;
  - recovered enemy birth projection supplies the FIXSTR/FIXTOUGH-equivalent attack/defense basis;
  - `BATTLE_COM_S_POWERBALANCE=1007` executes through the ordinary physical attack path with immediate work attack/defense mutations carried as explicit setup effects.
- `PETSKILL_Mighty`:
  - **2** referenced skill IDs and **120** positive enemybase skill-slot uses;
  - both OPTION rows have strict CP950/Big5 decode consensus;
  - **2/2** contain the fixed `倍` multiplier marker and **2/2** contain the `避` dodge marker;
  - **2/2** pass the strict numeric grammar probe for both multiplier and dodge values;
  - `BATTLE_COM_S_MIGHTY=1006` preserves LOW(COM3)=damage multiplier x100 and HIGH(COM3)=dodge modifier;
  - dodge modification is applied before the original-target dodge check; damage multiplication is applied after ordinary damage/guard/minimum-damage handling and before damage reaction / ride sharing;
  - counter execution does not inherit Mighty modifiers.
- Runtime OPTION handling is fail-closed:
  - PowerBalance rejects rows outside the proven attack/defense marker grammar;
  - Mighty rejects missing or malformed multiplier/dodge numeric grammar instead of falling back to old handler defaults.
- End-to-end recovered enemy AI now admits:
  `None + NormalAttack + NormalGuard + StatusChange + PowerBalance + Mighty`.
- Validation:
  - corrected Mighty physical baseline comparison: battle core **36771733005 = PASS**, Taiwan v1.0 gameplay **36771733178 = PASS**;
  - enabled Mighty runtime: golden contract **36772731716 = PASS**;
  - final end-to-end coordinator on HEAD `3a6858fa30528c76be8b662746369b7359c1110e`: **36772788312 = PASS**;
  - final hash-pinned recovered25 region/runtime-stack workflow: **36772788450 = PASS**.
- The earlier Mighty exact-damage assertion failure (**36771562662 / 36771562742**) was a test expectation error: the fixture's ordinary physical baseline was 95, so x2 correctly produced 190; implementation order was unchanged and the corrected baseline-relative regression passed.
- Executable recovered stable-common pet-skill slot-use coverage is now **1711 / 2486 = ~68.8%** when counting NormalAttack + NormalGuard + StatusChange + PowerBalance + Mighty. This remains a skill-slot semantic coverage metric, not an encounter-frequency/action-probability estimate.
- **LOCAL_RUNTIME_ENEMY_AI_POWERBALANCE_R1 = CLOSED.**
- **LOCAL_RUNTIME_ENEMY_AI_MIGHTY_R1 = CLOSED.**
- Next priority: `PETSKILL_GuardBreak` (**1 referenced ID / 60 slot uses**). Its recovered OPTION is ASCII-only, while the fixed common handler's only data marker is non-ASCII `攻%`, so recovered25 cannot trigger that optional attack-percent rewrite. The remaining closure is the dedicated GuardBreak execution contract: command 1002, guard-only hit gate, no ordinary GUARD damage reduction, and fail/miss when the resolved target is not actively guarding or is confused. ChargeAttack/ContinuationAttack remain deferred because they require cross-turn or multi-hit state/execution closure.
## Phase 1 recovered GuardBreak enemy-AI execution — 2026-10-01

- `PETSKILL_GuardBreak` is now closed for recovered25 enemy AI:
  - **1** referenced GuardBreak skill ID;
  - **60** positive enemybase skill-slot uses;
  - bundle-backed hard probe proves **1/1 ASCII OPTION** and **0** recovered `攻%` markers;
  - therefore the fixed handler's optional attack-percent rewrite cannot activate for this recovered row, and attack setup remains the recovered FIXSTR-equivalent birth projection.
- `BATTLE_COM_S_GBREAK=1002` now has a dedicated ordinary-round execution path preserving the fixed source behavior:
  - `BATTLE_AttackSeq`-shaped dodge / Guardian / critical / base-damage work occurs first;
  - damage is retained only when the original target is using ordinary GUARD and is not confused;
  - GuardBreak bypasses ordinary GUARD damage reduction;
  - otherwise final damage is forced to zero and the result becomes MISS;
  - if Guardian redirects inside AttackSeq, damage calculation can use the Guardian while `BATTLE_DamageSub` / HP settlement still applies to the original guarded target, matching the fixed old implementation.
- Recovered runtime bridge is fail-closed outside the proven ASCII-only subset.
- Validation:
  - dedicated GuardBreak source-quirk battle tests: battle core **36774405578 = PASS**, Taiwan v1.0 gameplay **36774405611 = PASS**;
  - recovered GuardBreak bridge/coordinator enablement: coordinator **36774519456 = PASS**, golden contract **36774519705 = PASS**;
  - end-to-end recovered `wa[6]` -> GuardBreak -> guarded player round: coordinator **36774570763 = PASS**;
  - bundle-backed GuardBreak OPTION closure: recovered25 workflow **36774689850**, concrete local runtime-stack step = **PASS**.
- The earlier **36774283411 / 36774283327** and inherited **36774315248** red runs were test-fixture errors: the new confused-GUARD regression omitted the already-required explicit confusion action RNG. Runtime logic was unchanged; the corrected explicit-RNG fixture passed.
- Executable recovered stable-common pet-skill slot-use coverage is now **1771 / 2486 = ~71.2%** when counting NormalAttack + NormalGuard + StatusChange + PowerBalance + Mighty + GuardBreak.
- **LOCAL_RUNTIME_ENEMY_AI_GUARDBREAK_R1 = CLOSED.**
- Next priority: `PETSKILL_ChargeAttack` (**3 referenced IDs / 90 slot uses**). The fixed command encoding and one-step `BATTLE_Charge` model already exist, but runtime admission remains OPEN because charge state must persist COM1/COM3 across rounds. Current persistent battle state stores submitted `last_commands`, while each new round still requires fresh commands; it does not yet preserve the decremented LOW(COM3) / S_CHARGE -> S_CHARGE_OK transition. Reconstruct that persistent command-state seam before enabling recovered ChargeAttack. ContinuationAttack remains deferred behind its multi-hit/divisor/retarget/counter-loop closure.

## Phase 1 recovered ChargeAttack enemy-AI execution — 2026-10-01

- `PETSKILL_ChargeAttack` is now closed for recovered25 enemy AI:
  - **3** referenced ChargeAttack skill IDs;
  - **90** positive enemybase skill-slot uses;
  - all **3/3** OPTION rows decode identically under strict CP950 and Big5;
  - bundle-backed hard grammar proves **3/3** leading integer wait counts, all in the fixed **1..10** range, and **3/3** numeric `攻%` parameters;
  - recovered wait counts span **1..3** and recovered attack percentages span **90..150**.
- The persistent battle state now preserves source-shaped charge execution across rounds:
  - `BATTLE_COM_S_CHARGE=1005` carries the decremented LOW(COM3) countdown plus the original target;
  - latent ready attack power is preserved separately from COM1/COM2/COM3;
  - while charge carry is active, the enemy does **not** consume fresh AI mode/target rolls;
  - when LOW reaches zero, the next charge turn promotes to `BATTLE_COM_S_CHARGE_OK=1015`, applies `FIXSTR + FIXSTR * attack_percent / 100 + MODATTACK`, executes the ordinary physical path, then clears the carried state.
- Recovered enemy execution reconstructs ready power from the preserved birth FIXSTR-equivalent attack projection and uses `MODATTACK=0`; no unproven enemy equipment/modifier layer is invented.
- OPTION parsing is fail-closed: missing/malformed leading wait count, missing/malformed `攻%`, codec disagreement, or a wait count outside 1..10 rejects execution.
- End-to-end coordinator regression proves recovered `wa[n]` selection -> ChargeAttack -> two carried no-action countdown rounds -> automatic CHARGE_OK hit, with no AI reroll while carried.
- Validation:
  - persistent Charge state battle core **36776422452 / 36776475416 = PASS** and Taiwan v1.0 gameplay **36776422580 / 36776475341 = PASS**;
  - carry-aware coordinator **36776700346 = PASS**, golden contract **36776700417 = PASS**, recovered25 workflow **36776700334 = PASS**;
  - recovered bridge **36815994396 = PASS** and bridge regression **36816020673 = PASS**;
  - recovered runtime enablement coordinator **36816051805 = PASS** and golden contract **36816051829 = PASS**;
  - three-round recovered enemy-AI regression **36816143741 = PASS**;
  - latest hard bundle grammar run **36816252519**, concrete recovered25 local-runtime-stack step = **PASS**.
- Executable recovered stable-common pet-skill slot-use coverage is now **1861 / 2486 = ~74.9%** when counting NormalAttack + NormalGuard + StatusChange + PowerBalance + Mighty + GuardBreak + ChargeAttack.
- **LOCAL_RUNTIME_ENEMY_AI_CHARGEATTACK_R1 = CLOSED.**
- Next priority: `PETSKILL_NoGuard` (**3 referenced IDs / 74 slot uses**). Its fixed own turn is NoAction, but S_NOGUARD must remain selected for the rest of the same round because HIGH(COM3) modifies defending dodge and the upper byte of LOW(COM3) modifies non-player counter probability. First close the recovered OPTION grammar for `避%` / counter-token / `心%`; then add same-round S_NOGUARD dodge/counter consumption without introducing cross-round carry. ContinuationAttack (**139** uses) remains deferred behind its multi-hit/divisor/retarget/counter-loop closure.

## Phase 1 recovered NoGuard enemy-AI execution — 2026-10-01

- `PETSKILL_NoGuard` is now closed for recovered25 enemy AI:
  - **3** referenced NoGuard skill IDs;
  - **74** positive enemybase skill-slot uses;
  - all **3/3** OPTION rows decode identically under strict CP950 and Big5;
  - all **3/3** contain numeric `避%`, traditional `擊%`, and `心%` markers;
  - recovered values span dodge **30..50**, counter **50..70**, critical **20..40**;
  - **0/3** use the simplified `击%` token in the recovered25 bundle.
- The fixed same-round semantics are preserved:
  - `BATTLE_COM_S_NOGUARD=1014` resolves as own-turn NoAction without rewriting COM1/COM3 to WAIT/NONE;
  - while the NoGuard actor is defending, HIGH(COM3) adds to dodge probability;
  - when the NoGuard actor is the non-player counter actor, the upper byte of LOW(COM3) adds to counter probability before the 100-percent cap;
  - the source's nonstandard byte rule is preserved exactly: values above 127 are multiplied by -1;
  - the packed critical byte remains inactive because the common critical consumer is inside disabled `#if 0` source.
- Runtime admission is fail-closed:
  - recovered execution requires the proven traditional-token grammar and proven value ranges;
  - command formation delegates to the existing NoGuard reference model and stable round bridge;
  - no cross-round carry state is introduced.
- The enemy-AI round exposes explicit counter-chain RNG so NoGuard's same-round counter eligibility can be exercised without hidden randomness.
- Validation:
  - NoGuard counter modifier model **23f19b2f = committed**;
  - cross-action round execution and dedicated dodge/counter regressions **f90a4c88 / 56276cd1 / 634d0d45 / c6ca3d79**;
  - bundle grammar hard closure **ab7523dd** and regenerated aggregate report **ef63f17b**;
  - stable NoGuard round bridge **414bba83**, recovered enemy bridge **69da8a60 / 7cd6b324**, runtime admission **c6aa2d26**;
  - the first end-to-end fixture at **eeee0569** exposed the missing explicit counter-RNG coordinator input; no hidden RNG fallback was added;
  - final HEAD `17b650ffefa8ceccf34ee3760a5496d22542c403` passes coordinator **36817983797**, golden contract **36817983929**, and full recovered25 region/runtime-stack **36817983879**.
- Executable recovered stable-common pet-skill slot-use coverage is now **1935 / 2486 = ~77.8%** when counting NormalAttack + NormalGuard + StatusChange + PowerBalance + Mighty + GuardBreak + ChargeAttack + NoGuard.
- **LOCAL_RUNTIME_ENEMY_AI_NOGUARD_R1 = CLOSED.**
- Next priority: `PETSKILL_ContinuationAttack` (**139 slot uses**). Its fixed handler stores the attack count in LOW(COM3), and battle execution sets the same count as the damage divisor. The remaining closure is the multi-hit loop itself: hit count, per-hit target adjustment/retarget behavior, damage division, Guardian/reaction interaction and counter-chain placement must be reconstructed before recovered enemy-AI admission.

## Phase 1 recovered ContinuationAttack enemy-AI execution — 2026-10-01

- `PETSKILL_ContinuationAttack` is now closed for recovered25 enemy AI:
  - **4** referenced ContinuationAttack skill IDs;
  - **139** positive enemybase skill-slot uses;
  - all **4/4** recovered OPTION rows are ASCII, begin with a valid integer, and satisfy the fixed **1..10** handler range;
  - recovered counts are exactly four distinct values spanning **2..5**.
- Fixed command/setup semantics are preserved:
  - `BATTLE_COM_S_RENZOKU=1001`;
  - the handler writes the attack count into LOW(COM3) while preserving HIGH(COM3);
  - recovered runtime admission initializes the inactive HIGH half to zero rather than inventing prior packed-state residue.
- Fixed multi-hit execution is reconstructed rather than approximated as N full-damage attacks:
  - LOW(COM3) is both the hit cap and `gDamageDiv`;
  - positive physical damage is divided by N after AttackSeq-shaped dodge/critical/GUARD/Guardian processing and before DamageSub-shaped reactions/ride sharing;
  - non-bow target-list setup repeats the originally submitted COM2, so after that original target dies each later hit independently re-checks it and may consume a fresh default-target retarget roll;
  - Guardian eligibility is re-evaluated on every hit;
  - damage reaction, ride split/petfall, positive-damage wakeup, death/ultimate accumulation and immediate ultimate exits are resolved per hit and therefore can change the state seen by later hits;
  - the counter chain starts only after the multi-hit loop and is gated by the final `BATTLE_Attack` continuation boolean / final counter target.
- RNG remains explicit and fail-closed:
  - `ContinuationAttackRolls` requires exactly one ordinary-attack RNG bundle per recovered hit;
  - the coordinator requires an exact participant-key match for enemies that actually selected S_RENZOKU;
  - no hidden retarget, hit, damage, critical, dodge or counter RNG fallback was introduced.
- Runtime plumbing is complete:
  - stable command bridge -> ordinary round resolver -> persistent battle state -> recovered enemy `wa[n]` bridge -> local runtime coordinator;
  - unsupported/malformed callback or OPTION data remains an error rather than ATTACK/WAIT fallback.
- Validation:
  - baseline multi-hit battle core **36820169804 = PASS** and Taiwan gameplay **36820169769 = PASS**;
  - Guardian extension **36820385361 / 36820385299 = PASS**;
  - per-hit damage reaction **36820516236 / 36820516168 = PASS**;
  - final isolated main-round/counter-chain regression: battle core **36825541838 = PASS**, Taiwan gameplay **36825541884 = PASS**;
  - runtime admission golden contract **36825016807 = PASS** and coordinator **36825016962 = PASS**;
  - end-to-end recovered ContinuationAttack coordinator **36825205100 = PASS**;
  - full recovered25 region/runtime-stack workflow **36825205097 = PASS**.
- Executable recovered stable-common pet-skill slot-use coverage is now **2074 / 2486 = ~83.4%** when counting NormalAttack + NormalGuard + StatusChange + PowerBalance + Mighty + GuardBreak + ChargeAttack + NoGuard + ContinuationAttack.
- **LOCAL_RUNTIME_ENEMY_AI_CONTINUATIONATTACK_R1 = CLOSED.**
- Next priority: `PETSKILL_Abduct` (**2 referenced IDs / 14 slot uses**). It ties EarthRound at 14 uses, but recovered25 Abduct OPTION rows are **2/2 ASCII** and the stable base action does not require EarthRound's two-phase cross-round carry or stale-COM3 damage state. Close target eligibility, explicit RAND(1,100), success/failure exit semantics and persistent battle-entry removal before runtime admission. EarthRound remains behind it.

## Stable Abduct active-branch correction — 2026-10-01

- Re-audit of the three pinned fixed descendant builds found that all three define both `_BATTLE_ABDUCTII` and `_PETSKILL_OPTIMUM`.
- This supersedes the earlier reference-model assumption that ABDUCTII was outside the active fixed build.
- Active command identity:
  - `PETSKILL_Abduct` writes the resolved pet-skill array to LOW(COM3) and preserves HIGH;
  - with `_PETSKILL_OPTIMUM`, pet-skill rows are loaded directly at their skill-ID index, so the active fixed array identity is recoverable from the pet-skill ID itself.
- Active probability branch:
  - PLAYER defender -> return FALSE before an attempt;
  - PET defender with `atoi(OPTION) > 0` -> probability 200 iff `FIXAI < AiPer`, otherwise 0;
  - non-PET defender or non-positive AiPer -> old level formula with minimum 50;
  - non-null WinFunc -> probability 0.
- A valid non-player attempt makes the attacker exit whether the roll succeeds or fails; successful PET/ENEMY targets also exit through their source-specific path.
- Runtime admission remains OPEN until recovered25 Abduct OPTION/AiPer values and persistent target/attacker exit semantics are bundle-backed and executable.
- **PETSKILL_ABDUCT_ACTIVE_ABDUCTII_REFERENCE_R1 = CLOSED_REFERENCE_MODEL_ONLY.**

## Phase 1 recovered Abduct enemy-AI execution — 2026-10-01

- `PETSKILL_Abduct` is now closed for recovered25 enemy AI:
  - **2** referenced Abduct skill IDs;
  - **14** positive enemybase skill-slot uses;
  - both OPTION rows are ASCII;
  - the bundle-backed hard probe proves exactly **1/2** rows with a leading integer, exactly **1/2** with a positive `atoi(OPTION)`, and the exact threshold set **{0,80}**.
- Fixed command identity and execution were re-audited before runtime admission:
  - the pinned `battle.h` sequence is `S_EARTHROUND0=1009`, `S_EARTHROUND1=1010`, `S_LOSTESCAPE=1011`, **`S_ABDUCT=1012`**, `S_STEAL=1013`, `S_NOGUARD=1014`;
  - `battle.c` runs `BATTLE_TargetAdjust` before `BATTLE_Abduct`;
  - the handler preserves HIGH(COM3) and stores the recovered pet-skill array/ID in LOW(COM3).
- The active `_BATTLE_ABDUCTII` probability branch is executable rather than reference-only:
  - PLAYER defender returns before an attempt and consumes no Abduct success RNG;
  - PET defender with positive AiPer uses **200** when `FIXAI < AiPer`, otherwise **0**;
  - non-PET defenders or non-positive AiPer use the fixed level formula with minimum **50**;
  - the reconstructed ordinary local group seam pins `has_win_func=False`; special WinFunc battles remain outside this admission rather than being guessed.
- Recovered FIXAI is now preserved on battle participants:
  - enemy FIXAI comes from the recovered enemy birth projection;
  - allied-pet FIXAI comes from the persistent pet `ai` field when present.
- Abduct has a dedicated explicit-RNG round path:
  - dead/invalid submitted targets use the already reconstructed `BATTLE_TargetAdjust`-shaped retarget seam;
  - valid non-player attempts require explicit `RAND(1,100)`;
  - successful PET/ENEMY targets exit battle;
  - a valid PET/ENEMY attacker exits whether the roll succeeds or fails;
  - HP is unchanged by Abduct itself.
- Persistent battle state now distinguishes **non-death battle-entry exit** from physical removal:
  - Abduct-exited pets/enemies remain in the session identity graph with HP/state intact;
  - they are excluded from later action/target/living counts;
  - they do not produce kill EXP/drop profit;
  - CAPTURE and ordinary enemy ESCAPE retain their existing physical-removal semantics.
- The recovered enemy pet-skill bridge is fail-closed:
  - runtime admission requires exactly the hard-probed two Abduct callback IDs;
  - the OPTION population must remain ASCII with threshold values exactly **0 and 80**;
  - LOW(COM3) must equal the recovered skill ID under the active `_PETSKILL_OPTIMUM` table identity.
- End-to-end regression proves recovered enemy AI `wa[n]` selection -> Abduct ID with AiPer=80 -> player pet with FIXAI=79 -> probability 200 -> successful target + attacker battle exits, while both identities/HP remain and no kill EXP is awarded.
- Validation:
  - stable Abduct core / bridge commit `24723cdba7d9ab5abdd43aca9e0c96674a17f3a3`: battle core **36829173067 = PASS**, local runtime coordinator **36829173106 = PASS**, stable pet-skill core **36829173108 = PASS**, Taiwan v1.0 gameplay **36829173129 = PASS**, full recovered25 payload/runtime-stack **36829173114 = PASS**;
  - persistent non-death exit seam `e16c478e08a3c52abf35adbed2c6357b8d5b95d2`: battle core **36829403059 = PASS**, local runtime coordinator **36829402550 = PASS**, Taiwan v1.0 gameplay **36829402642 = PASS**;
  - recovered Abduct AI bridge `f993725a011ee03d8af1befb616b4ec54b132f1f`: local runtime coordinator **36829720935 = PASS**;
  - end-to-end runtime commit `09991ef179066fdd69ae5d09c7e41c759a5f504c`: local runtime coordinator **36829954993 = PASS**, runtime golden contract **36829954981 = PASS**; its duplicate full recovered25 run **36829954966** remains in progress at this state-writing point, while the same hard bundle probe already passed in **36829173114**.
- Executable recovered stable-common pet-skill slot-use coverage is now **2088 / 2486 = ~84.0%** when counting NormalAttack + NormalGuard + StatusChange + PowerBalance + Mighty + GuardBreak + ChargeAttack + NoGuard + ContinuationAttack + Abduct.
- **LOCAL_RUNTIME_ENEMY_AI_ABDUCT_R1 = CLOSED.**
- Next priority: `PETSKILL_EarthRound` (**14 positive slot uses**). Its remaining gap is structurally different from Abduct: reconstruct and persist the two-phase `S_EARTHROUND1 -> S_EARTHROUND0` command transition, preserve the fixed stale-full-COM3 hazard when the optional attack-percent marker is absent, and apply `1 + 0.01 * COM3` only on the phase-2 ordinary physical attack before recovered enemy-AI admission.

## Phase 1 recovered EarthRound enemy-AI execution — 2026-10-01

- `PETSKILL_EarthRound` is now closed for recovered25 enemy AI:
  - **1** referenced EarthRound skill ID;
  - **14** positive enemybase skill-slot uses;
  - the OPTION row is non-ASCII but strict CP950/Big5 decoding agrees exactly;
  - bundle-backed probe `36830879270 = PASS` produced `attack_marker_ids=1`, `attack_numeric_ids=1`, and exact attack-percent range **90.0..90.0**.
- Fixed command and two-phase execution are reconstructed:
  - `BATTLE_COM_S_EARTHROUND0=1009` and `BATTLE_COM_S_EARTHROUND1=1010`;
  - phase 1 hides/does no damage, clears the source attacked flag semantically, and carries `S_EARTHROUND0` with the original target/full COM3;
  - phase 2 enters the ordinary physical path, applies `1 + 0.01 * COM3`, then clears the command to NONE;
  - carried phase 2 overrides newly submitted commands and consumes **no new enemy AI mode/target roll**.
- The historical stale-full-COM3 hazard remains preserved in the generic stable handler: missing `攻%` leaves the old full COM3 untouched. The recovered25 row does not enter that branch because its only OPTION is hard-probed as numeric **`攻%90`**.
- Damage-order fidelity is preserved: the EarthRound 1.90 multiplier is applied after ordinary guard/minimum-damage/Guardian zero-damage correction and before damage-reaction settlement; it does not leak into the later counter chain.
- Recovered runtime admission is fail-closed:
  - exactly one EarthRound callback ID is required;
  - strict CP950/Big5 OPTION consensus is required;
  - numeric `攻%` must be present and must equal **90**.
- Validation:
  - two-phase round core `cc1192c762f0d50b3e1699e0b43f1e2fa6ef637a`: battle core **36831665599 = PASS**, stable pet-skill **36831665622 = PASS**, Taiwan gameplay **36831665422 = PASS**, local runtime **36831665403 = PASS**;
  - persistent `S_EARTHROUND0` carry `3bc5baea14852a5977567848708045883ac61b15`: battle core **36831689093 = PASS**, Taiwan gameplay **36831689032 = PASS**, local runtime **36831689038 = PASS**;
  - stable round bridge/regression `0cdfa9734a315ad76caf5af555de90900a22e3de`: stable pet-skill **36831744844 = PASS**, battle core **36831744962 = PASS**;
  - two-phase battle/persistent regressions `6f50627cb89da735280f50c2e255b1d5cedd23a0` / `0b561def4caea7677653dbe3c5ab512104901a5a`: battle core **36831778341 / 36831814501 = PASS**, Taiwan gameplay **36831778423 / 36831814336 = PASS**;
  - recovered bridge `0cc455b36aab19fb59a72b4de8a910997e8d94d3` and bridge regression `63128c2cf5109867de66e82b641747f69b7558a8`: coordinator **36832119661 / 36832084800 = PASS**;
  - coordinator carry admission `17d964b648721c7378be0a8fb7427206ebf918fc`: runtime golden contract **36832307359 = PASS**, local runtime coordinator **36832307370 = PASS**;
  - end-to-end recovered AI two-round regression `3808d9cf842989099ebc4e59e5d8696e3f6bf88b`: local runtime coordinator **36832389539 = PASS**; duplicate full recovered25 validation **36832389259** is still in progress at this state-writing point.
- Executable recovered stable-common pet-skill slot-use coverage is now **2102 / 2486 = ~84.6%**.
- **LOCAL_RUNTIME_ENEMY_AI_EARTHROUND_R1 = CLOSED.**
- Next priority: `PETSKILL_Steal` (**1 referenced ID / 12 positive slot uses**). Its core RNG formula already exists, but runtime admission requires a transactional player Gold/inventory mutation seam plus success-only attacker battle exit; do not model it as ordinary damage or as item transfer to the attacker.


## Phase 1 recovered Steal enemy-AI execution — 2026-10-01

- `PETSKILL_Steal` is closed for recovered25 enemy AI:
  - **1** referenced skill ID / **12** positive enemybase skill-slot uses;
  - the sole OPTION row is ASCII and the hard probe requires exactly that one callback population.
- Fixed `BATTLE_Steal` semantics are preserved rather than normalized into a conventional transfer:
  - only PLAYER defenders receive the **50%** entry chance; non-player defenders have probability **0**;
  - successful entry uses a second 50% split for gold vs ordinary-item mode;
  - gold mode removes **RAND(8,12)%** of defender Gold and credits **nothing** to the attacker;
  - item mode selects one occupied ordinary inventory slot, removes the slot item and ends that item instance; it does **not** transfer the item to the attacker;
  - zero gold / no eligible item converts the attempt back to failure;
  - the stealing attacker exits battle only when the final steal result succeeds.
- The local runtime applies Steal against the battle's working persistent clone:
  - player Gold/inventory mutation is visible to later rounds in the same battle;
  - the pre-battle persistence payload is not mutated in place;
  - normal settlement/commit remains the transaction boundary.
- Validation:
  - stable battle mutation seam `eaa8fc63...` / `0a8caf1c...`: battle-core regressions remain green;
  - stable command bridge `2606c228...` plus command regression `41b88237ae76a6005a137bad5ae11bd570942933`: stable pet-skill **36833681260 = PASS**, battle core **36833681131 = PASS**;
  - recovered bridge `1efaaf1b...` / regression `310b9c5c...`: local runtime coordinator **36833382378 / 36833413967 = PASS**;
  - transactional coordinator `82b3fe20bce1e04edf9d41266e0874c714d30ac9`: runtime golden **36833505390 = PASS**, local runtime **36833505356 = PASS**;
  - end-to-end Steal transaction `cc9da4734a4d326a3e3d92f938abbf12205b7a3e`: local runtime **36833626994 = PASS**;
  - full hard-probed recovered25 bundle validation including the pinned one-row Steal population: **36833909945 = PASS**.
- Executable recovered stable-common slot-use coverage after Steal is **2114 / 2486 = ~85.0%**.
- **LOCAL_RUNTIME_ENEMY_AI_STEAL_R1 = CLOSED.**

## Phase 1 recovered Guardian enemy-AI execution — 2026-10-01

- `PETSKILL_Guardian` is closed for recovered25 enemy AI:
  - **1** referenced Guardian skill ID / **4** positive enemybase skill-slot uses;
  - strict CP950/Big5 decoding agrees for the non-ASCII OPTION;
  - hard probe proves the recovered row is attack-mode only: exactly **`攻%-20`**, no `防%`, and no defensive `COM:...防御`.
- Fixed attack-branch semantics are retained:
  - work attack is rebuilt as FIXSTR + trunc(FIXSTR × -20%), i.e. 80% for positive FIXSTR;
  - work defense remains the fixed defense;
  - the Guardian flag is retained;
  - authoritative battle slot is passed into the bridge so a back-row actor can register the corresponding same-side front-row protected slot using the fixed source formula rather than a guessed position.
- Runtime admission is fail-closed:
  - exactly one recovered Guardian callback ID is required;
  - OPTION must remain the exact recovered attack-mode subset;
  - enemy actor slot must come from persistent battle state and be on the enemy side.
- End-to-end coordinator regression exercises a recovered enemy in battle slot 15 and confirms `S_GUARDIAN_ATTACK` executes through the ordinary physical path with the reconstructed setup effects.
- Validation:
  - recovered bridge `29b55be181cfec8aca31e20589d2732600cac64f`: local runtime **36835022656 = PASS**;
  - bridge regression `9ad6a1ba646681237b0e7e5c7c4e71698f30f2a0`: local runtime **36835054828 = PASS**;
  - coordinator admission `48752047c4003817059df8cb11d12c1ef0be5aea`: local runtime **36835086215 = PASS**, runtime golden **36835086316 = PASS**;
  - end-to-end recovered Guardian regression `bcc78817377bb59764367c7e7831f018a513f53b`: local runtime **36835215844 = PASS**;
  - exact Guardian bundle grammar hardened in `d79b236b...` / `311571b4c6d9a312fe6bb0bc9e6b5fa6c82d09b9`, with full recovered25 validation **36835322303 = PASS**.
- Executable recovered stable-common slot-use coverage after Guardian is **2118 / 2486 = ~85.2%**.
- **LOCAL_RUNTIME_ENEMY_AI_GUARDIAN_R1 = CLOSED.**

## Phase 1 recovered Merge historical-UB closure — 2026-10-01

- `PETSKILL_Merge` is closed as a **historical undefined-behavior boundary**, not admitted as executable recovered enemy AI:
  - **2** referenced IDs / **3** positive enemybase skill-slot uses;
  - the real preservation bundle is hard-probed as **2/2 FIELD=MAP**, **2/2 ILLEGAL=1**, **2/2 ASCII**, **2/2 empty OPTION**;
  - nevertheless, fixed `BATTLE_ai_normal` does **not** filter `PETSKILL_FIELD` before a `wa[n]` call; it directly invokes `PETSKILL_Use(enemy, slot, target, NULL)`;
  - active `_PETSKILL_CHECKTYPE` does not save this path because that gate applies only to `CHAR_TYPEPET`, while encounter actors are `CHAR_TYPEENEMY`.
- Fixed owner/data flow was re-audited:
  - ordinary enemies start with all work integers zero and do not replace `CHAR_WORKPLAYERINDEX`, so Merge resolves nominal owner index **0**;
  - `data=NULL` is accepted by the delimiter helper but yields at most one empty/zero material token;
  - true item merge requires `cnt > 1`, so this enemy-AI path never enters a legitimate merge transaction.
- Descendant divergence proves this was a historical bug rather than a deterministic game rule:
  - gavinlinasd and iriselia both fall off the end of `ITEM_mergeItem_merge(int ...)` with no return when `cnt <= 1`, yielding C-level undefined return data;
  - Bismarck later repairs the path with an explicit final `return result;`, making the same NULL-data path deterministically FALSE;
  - the later repair is bug-fix evidence and is **not** back-projected as the exact result of the earlier code.
- The undefined return is observably relevant in battle:
  - each round first clears non-carried COM1 to NONE and sets actors to `C_WAIT`;
  - if the garbage callback return happens to equal TRUE, `BATTLE_ai_normal` promotes the enemy to `C_OK + COM_NONE`;
  - otherwise it remains `C_WAIT`;
  - `BATTLE_Battling` skips actors not in `C_OK`, so this can alter per-actor status-sequence timing even though no attack command is produced.
- Modern reconstruction policy:
  - recovered enemy Merge is rejected with a dedicated historical-UB fail-closed error;
  - the runtime does not touch global character index 0, does not invent one compiler/ABI's garbage return value, and does not normalize the action to WAIT/NONE/ATTACK.
- Validation:
  - dedicated bridge boundary `85f7843e389483fe9a997bd1c6820b314694f3c7`: local runtime coordinator **36837156954 = PASS**;
  - bridge regression `5b8c640c0d728599e237739eefb1baf99b2ca5b9`: local runtime coordinator **36837179586 = PASS**;
  - coordinator end-to-end negative regression `98ea48149fcdf9883235d8611cff9cd8b856eaba`: local runtime coordinator **36837398997 = PASS**;
  - exact Merge specimen hard probe at the same HEAD: full recovered25 payload/runtime-stack **36837399052 = PASS**.
- Executable recovered stable-common slot-use coverage therefore remains **2118 / 2486 = ~85.2%**; the remaining **3** stable-common slot uses are intentionally classified-but-nonexecuted historical UB, not an implementation backlog.
- All **31 referenced stable-common pet-skill IDs** are now either executable or explicitly closed at a no-guess boundary.
- **LOCAL_RUNTIME_ENEMY_AI_MERGE_HISTORICAL_UB_R1 = CLOSED.**

## Phase 1 recovered non-common pet-skill inventory — 2026-10-01

- The remaining recovered enemybase pet-skill surface is now explicitly inventoried rather than treated as one opaque later-version bucket:
  - **80** referenced non-common pet-skill IDs;
  - **365** positive enemybase slot uses;
  - **38** distinct callback tokens in that referenced subset.
- Full preservation-bundle validation **36838204361 = PASS** at source commit `1194408d5bb8c90b50a651ecfd29e8af25179a63`; bot report write-back advanced `main` to `8071abf23671581d148ee5afbb58d4216ee497c5`.
- Highest-frequency families are:
  - `PETSKILL_AttackMagic`: **25 IDs / 106 slot uses**;
  - `ENEMYSKILL_ReHP`: **1 / 31**;
  - `PETSKILL_DamageToHp`: **3 / 30**;
  - `PETSKILL_MpDamage`: **3 / 25**;
  - `PETSKILL_FallGround`: **1 / 23**.
- `PETSKILL_AttackMagic` is selected as the next family because it is both the dominant recovered non-common callback and fixed-source backed:
  - all **25/25** recovered rows are FIELD=BATTLE, ILLEGAL=0 and ASCII;
  - OPTION decoding is identical under strict CP950 and Big5 for all 25 rows;
  - gavin/iris guard the handler with `__ATTACK_MAGIC` and both define it;
  - Bismarck renames the guard to `_ATTACK_MAGIC` and also defines it;
  - therefore AttackMagic is compile-active in all three pinned descendants, but remains a **guarded version layer**, not part of the unguarded stable-common set.
- Fixed handler convergence/divergence already identified:
  - all three write `BATTLE_COM_S_ATTACK_MAGIC`, target COM2 and magic ID to LOW(COM3);
  - gavin/iris additionally parse an `item` token and write it to HIGH(COM3);
  - Bismarck comments out the item parse/high-half write and invokes the same magic execution with whatever HIGH(COM3) state remains;
  - battle execution remaps target shape by magic ID and calls `MAGIC_DirectUse`;
  - this descendant drift must be resolved against the recovered25 OPTION population before runtime admission.
- **RECOVERED25_NONCOMMON_PETSKILL_INVENTORY_R1 = CLOSED.**
- Next priority: hard-probe all 25 recovered AttackMagic OPTION rows for source-shaped `magic` / `item` markers, ordering and numeric ranges; then reconstruct the appropriate recovered25 command/target/magic execution boundary without flattening the Bismarck high-half drift.

## Phase 1 recovered25 AttackMagic command boundary — 2026-10-01

- The hard probe requested by the preceding milestone is now closed against the
  real preservation bundle:
  - **25/25** AttackMagic rows contain numeric `magic` followed by numeric
    `item`;
  - magic IDs are exactly **301..325**, 25 distinct;
  - item IDs are exactly **19647..19671**, 25 distinct;
  - same-row numeric pairing is **25/25**;
  - observed `item - magic` is uniformly **19346**, but is retained as an
    observation rather than promoted to a derivation rule.
- Probe source `ccb037e4ae105c48a2dc44fb514eae84dd5ca9c7` passed full recovered25
  validation **36842103889**; automatic report write-back advanced `main` to
  `537d98ae3088e457cb028d4eccf815556bc40559`.
- The three pinned descendant sources establish the versioned command boundary:
  - guarded `BATTLE_COM_S_ATTACK_MAGIC` is numeric **2002**;
  - COM2 is the requested target and LOW(COM3) is the magic ID;
  - gavin/iris parse/write the item into HIGH(COM3);
  - Bismarck removes that write and therefore preserves prior HIGH(COM3)
    residue;
  - the battle executor applies the exact 25-entry magic-ID target table before
    `MAGIC_DirectUse`;
  - for non-player casters, `MAGIC_DirectUse` consumes the passed item number
    directly as the global item index, so the high-half divergence is material.
- Added a separate guarded-version reference layer rather than contaminating
  the stable-common pet-skill model:
  - `tools/stoneage_attack_magic_model.py`;
  - `tests/test_stoneage_attack_magic_model.py`;
  - `research/mechanics/STONEAGE-ATTACK-MAGIC-BOUNDARY-R1.md`;
  - dedicated AttackMagic CI.
- Recovered25 policy is explicit and fail-closed: require numeric magic/item
  markers, use the recovered explicit item value, preserve the Bismarck residue
  branch as a distinct descendant profile, and stop at the `MAGIC_DirectUse`
  request boundary rather than guessing attack-magic damage.
- **RECOVERED25_ATTACKMAGIC_COMMAND_BOUNDARY_R1 = CLOSED.**
- Next priority: cross-link recovered magic IDs **301..325** through
  `magic.txt`, corresponding item metadata and `attmagic.bin`
  indices/footprints, then reconstruct the active `_FIX_MAGICDAMAGE`
  execution core before admitting AttackMagic into recovered enemy-AI runtime.

## Phase 1 recovered25 AttackMagic cross-link + fixed damage core — 2026-10-01

- AttackMagic data cross-link is now closed by full preservation-bundle run
  **36844577483 = PASS**; bot report write-back advanced `main` to
  `ded5d20debde9ccde2ffd3254be9f7f9c6afbb5d`.
- Exact recovered25 cross-link:
  - **25/25** skill rows -> explicit magic/item numeric pair;
  - **25/25** magic IDs -> `MAGIC_AttMagic`;
  - **25/25** valid `MAGIC_IDX`, with 25 distinct IDX values in **2..26**;
  - attribute distribution earth/water/fire/wind = **6/6/7/6**;
  - power **100..350** across 7 distinct values;
  - magic level **1..5** across 5 distinct values;
  - **25/25** active item rows exist and their `magicid` matches;
  - all 25 item `magicusemp` values are **5**;
  - all 25 IDX values have valid adjacent records in the 54-record /
    27-effective-index `attmagic.bin`.
- **RECOVERED25_ATTACKMAGIC_CROSSLINK_R1 = CLOSED.**
- Three pinned descendant implementations were then re-audited for their
  actually enabled AttackMagic formula. All three define
  `_EQUIT_DEFMAGIC`, `_FIX_MAGICDAMAGE` and
  `_MAGIC_DEFMAGICATT`; the primary fixed-damage path converges on:
  cast proficiency check, per-target magic dodge, Kmagic/Mmagic/Amagic base
  damage, elemental traction, field adjustment, 0.7 failure attenuation,
  dedicated riding split, sleep clearing, and attack/defense magic training.
- Added fixed-source deterministic candidate:
  - `tools/stoneage_attack_magic_damage_model.py`;
  - `tests/test_stoneage_attack_magic_damage_model.py`;
  - `research/mechanics/STONEAGE-ATTACK-MAGIC-DAMAGE-CORE-R1.md`;
  - dedicated damage-core CI.
- The damage model keeps RNG externally injected and preserves source quirks,
  including the riding-overkill negative-share behavior and the strict
  `pet_hp < 0` unmount condition.
- Dedicated AttackMagic damage-core CI **36845772672 = PASS** at
  `e8e705ff75fe8aaf908b33359495a12b6aaa6480`.
- **FIXED_DESCENDANT_ATTACKMAGIC_DAMAGE_CORE_R1 = CLOSED.**
- The damage core remains deliberately **not wired** into recovered25 enemy AI
  until target-footprint geometry is independently closed.
- Next priority: reconstruct `attmagic.bin` IDX-side selection and 3x5
  footprint expansion, including dead-target retargeting and the historical
  `SortLoc` ordering behavior; only then compose footprint + damage core at
  the recovered enemy-AI runtime boundary.

## Phase 1 AttackMagic footprint geometry candidate — 2026-10-01

- Damage-core acceptance is now formally closed: dedicated CI **36845772672 = PASS** at `e8e705ff75fe8aaf908b33359495a12b6aaa6480`.
- Fixed descendant battle-slot geometry converges exactly across gavin/iris/Bismarck: the same 4x5 `CharTable`, inverse `CharTableIdx`, selector constants and `BATTLE_MultiAttMagic` matrix expansion.
- Corrected a prior probe interpretation: the 54 `attmagic.bin` records are **27 adjacent side-specific pairs**, not 27 effective records plus a second half. Runtime chooses `IDX*2+1` for attacker slots 0..9 and `IDX*2` for attacker slots 10..19.
- Added candidate footprint reconstruction with explicit dead-target retarget rolls, row fallback, 3x5 matrix expansion, and side-record selection.
- The convergent historical `SortLoc` right-down branch is not a valid portable ordering relation (`ele2basex - ele1basey`). Because target order controls later RNG consumption, exact right-down multi-target execution remains fail-closed rather than guessed.
- Corrected AttackMagic binary probe R2 passed against the real preservation bundle: **36846955696 = PASS**. It confirms 54 raw records = **27 adjacent side-specific pairs**, all **27/27 pairs differ**, all 27 magic indices are referenced, and field-matrix cells remain binary 0/1.
- Dedicated footprint geometry CI **36846956075 = PASS**; bot report write-back advanced `main` to `4cdb426b2649c0ec2e272200352c2e85b1e45957`.
- **FIXED_DESCENDANT_ATTACKMAGIC_FOOTPRINT_GEOMETRY_R1 = CLOSED.**
- Added a recovered25 real-matrix coverage probe for the actual local-runtime orientation (player slots 0..9, enemy slots 10..19): enemy AttackMagic uses even `IDX*2` records against player side 0. The probe evaluates all 25 magic IDs across all ten possible initial player target slots under a fully alive side and measures exact target counts plus source-sort portability without storing payload text.
- Coverage probe run **36847455747 = PASS**; report write-back advanced `main` to `0226f17c0498bd029681aa2d0c4c4e0952ab3f94`.
- Fully alive enemy->player scenarios: **250 total = 110 source-sort portable + 140 nonportable**. This exactly matches **110 single-target + 140 multi-target** scenarios in the recovered population; target-count distribution is 1:110, 2:8, 3:16, 4:6, 5:50, 10:60.
- Eleven magic IDs are portable across all ten fully alive source targets: **301,302,307,308,309,310,313,314,319,320,322**. The other fourteen remain dynamically admissible if current living-target membership collapses to a portable set.
- **RECOVERED25_ATTACKMAGIC_FOOTPRINT_COVERAGE_R1 = CLOSED.**
- A deeper fixed-source audit corrected the earlier HIGH(COM3) risk assessment: recovered `item 196xx` values are configuration IDs, not guaranteed dynamic existing-item indexes, but the resulting MP value is **execution-dead for non-player AttackMagic**. `MAGIC_DirectUse` does not abort on negative MP, non-player `MAGIC_AttMagic` skips MP consumption, and `MAGIC_AttMagic_Battle` ignores `mp`.
- Added a recovered25 AttackMagic runtime-index candidate that validates all 25 skill->magic->item-config->IDX->side-pair links, retains item IDs only as provenance/cross-link data, and dynamically fails closed when historical `SortLoc/qsort` target order is nonportable.
- Runtime-index validation **36850584056 = PASS**; all unit tests, fixed-bundle recovery, footprint coverage and runtime-index smoke passed. Bot report write-back advanced `main` to `99a6fa36b9c916696b3791618866377b17baa998`.
- Runtime report reconfirms **25 entries**, **250 full-side scenarios = 110 portable + 140 nonportable**, the eleven fully-alive always-portable magic IDs, `magicusemp={5}`, item-token role `CONFIG_CROSSLINK_ONLY_MP_EXECUTION_DEAD`, and the dynamic magic-305 one-alive portability witness.
- **RECOVERED25_ATTACKMAGIC_RUNTIME_INDEX_R1 = CLOSED.**
- Integrated the closed AttackMagic runtime index into the recovered25 local runtime stack as a typed optional component loaded with `server_data_dir`; stack validation requires exact equality with the recovered `PETSKILL_AttackMagic` skill population and exposes a fail-closed `resolve_enemy_attack_magic_footprint(...)` delegate.
- Full preservation-bundle local-stack rerun **36851295344 = PASS** after a smoke-only witness scope fix. Every stage passed: deterministic stack tests, verified bundle recovery, all materializable maps, local stack, AttackMagic cross-link, server collision coverage/provider, client ADRN coverage, and aggregate report write-back.
- Bot report write-back advanced `main` to `0dc65140f6cf5acb9dd8724408818b083f3f98c3`; the local-stack report contains all 25 AttackMagic entries, execution-dead non-player item role, exact magic-301 witness, dynamic magic-305 witness, and `RECOVERED25_LOCAL_RUNTIME_STACK_CLOSED`.
- **RECOVERED25_ATTACKMAGIC_STACK_INTEGRATION_R1 = CLOSED.**
- Added a separate enemy AttackMagic action-composer candidate. It combines only exact portable runtime plans with the closed damage core and explicit magic combat state/RNG; command code 2002, enemy-AI dispatch, profit/death flags and ordinary-round event integration remain outside this layer.
- The composer preserves source RNG order: one cast roll; then per ordered target one dodge roll; damage `rand()%20` only for non-dodged targets.
- It also composes fixed defender resistance/training, sleep clearing and dedicated AttackMagic ride attribute averaging/splitting without reusing physical ride-sharing formulas.
- Dedicated action-composer CI **36852504553 = PASS** at `316ae9a78869acf2cbcf852804ea1d539e0b92b1`; the damage-core, footprint, runtime-index and composer suites all passed together.
- **RECOVERED25_ENEMY_ATTACKMAGIC_ACTION_COMPOSER_R1 = CLOSED.**
- The existing `stoneage_attack_magic_model.py` already owns the authoritative 2002 / COM2 / COM3 encoding, so no duplicate command schema was added.
- Added a separate enemy-AI AttackMagic submission bridge candidate that resolves the selected seven-slot pet-skill identity, requires `PETSKILL_AttackMagic`, cross-checks it against the closed AttackMagic runtime index, and emits the existing `AttackMagicCommand` + deterministic `MagicDirectUseRequest`.
- The submission deliberately does **not** return `BattleCommand`; command 2002 remains outside the ordinary round enum until round-time magic-state synchronization is closed.
- Enemy AttackMagic submission-bridge CI **36852877820 = PASS** at `ac7d993dd09f9ff61fe7bebf90d5cd4413bd203f`; action-composer regression CI **36852877777 = PASS** on the same HEAD.
- **RECOVERED25_ENEMY_ATTACKMAGIC_SUBMISSION_BRIDGE_R1 = CLOSED.**
- Added a typed AttackMagic round-state adapter candidate. Existing `PersistentBattleState` remains authoritative for HP, sleep/base status and ride state; a dedicated `AttackMagicRoundOverlay` owns only the four resistance levels/EXP counters and magic equipment/status modifiers not yet present in the persistent battle model.
- The adapter consumes the closed enemy submission, derives current living player-side slots, requires exact portable footprint ordering, composes action RNG/damage, then writes HP/sleep/ride plus both selected/opposed resistance-training counters back without advancing turn or performing profit/death settlement.
- Mounted ride pets require an explicit elemental combat profile, including the historical exact-zero-HP mounted quirk where attribute averaging can still occur while HP sharing does not.
- Round-state adapter CI **36853623595 = PASS** at `53678ab4d27313ca95846163f834a09ae29a0357`; subsequent no-target RNG refinement kept the adapter regression green and action-composer CI **36854070168 = PASS**.
- **RECOVERED25_ATTACKMAGIC_ROUND_STATE_ADAPTER_R1 = CLOSED.**
- Fixed-source follow-up on `BATTLE_MultiList` closed a no-target RNG distinction: dead single/row selectors with no fallback return `-1` before AttackMagic proficiency/dodge/damage RNG, while side-wide selectors can retain an empty footprint without that early return. The action composer now represents the former with `normalized_selector=None`, requires zero RNG, and reports no cast-success result.
- Registered command **2002** as a guarded round command only for closed recovered25 enemy AttackMagic submissions. The ordinary action loop now resolves footprint/action state at execution time from current HP/status/ride state, emits per-target events, updates the four-element overlay, and leaves physical Guardian/reaction/counter/Ultimate paths untouched.
- Existing persistent death-penalty/profit/termination processing consumes those events; `PersistentRoundResult` carries AttackMagic overlay before/after while `PersistentBattleState` retains HP/base-status/ride/turn ownership.
- Exact retarget RNG validation rejects row/side-selector RNG, live-target RNG, and trailing unused single-target retarget rolls.
- Command-2002 round-execution CI **36854873316 = PASS** at `a2740b084422453b8f661d655ec93d5c26a4e32f`; local-session, Taiwan gameplay, battle-core, pet-skill-core and round-state-adapter regressions also passed on the same HEAD.
- **RECOVERED25_ATTACKMAGIC_COMMAND2002_ROUND_EXECUTION_R1 = CLOSED.**
- Integrated the closed enemy AttackMagic submission into `LocalRuntimeSessionCoordinator`: common enemy AI can now emit verified command 2002 plus its typed submission, and the full persistent round passes explicit AttackMagic RNG/retarget inputs into the closed round executor.
- `LocalRuntimeBattleContext` now carries the battle-local AttackMagic resistance/training overlay across rounds. The coordinator refuses to synthesize missing resistance state; a selected AttackMagic without an explicit overlay fails closed.
- Enemy AttackMagic coordinator CI **36855399645 = PASS** at `945a87b71ef79ba2432e7f774a7b1ad5d2674c76`; local-session, command-2002 round, runtime-golden and recovered25-region regressions also passed.
- **RECOVERED25_ENEMY_ATTACKMAGIC_COORDINATOR_INTEGRATION_R1 = CLOSED.**
- Added a preservation-bundle AttackMagic enemy-AI round witness to the existing recovered25 local-runtime smoke. It dynamically selects a real stable encounter/group/enemy whose recovered TACTICS/wa[] can select a real AttackMagic skill, derives weighted rolls from recovered data, spawns that enemy, then executes AI -> submission -> command 2002 -> persistent round and verifies overlay carry-forward.
- The witness intentionally supplies an explicit battle-local zeroed magic-resistance overlay; it does not infer missing resistance/training fields from the current save schema.
- Preservation-bundle workflow **36856905249 = PASS** for `94d13f14f730b65b53b869692bc3b3ac334ee4cf`; verified bundle recovery, map materialization, concrete runtime-stack witness, AttackMagic cross-links and both collision-provider audits all passed. Workflow report write-back produced `11cb491b2f97876cd4fb88b837226a5b717f9401` and added exactly the expected `ATTACKMAGIC_ENEMY_AI_ROUND_WITNESS|1|portable=1|target_events=1|overlay_carried=1|round_turn=1` marker.
- **RECOVERED25_ATTACKMAGIC_PRESERVATION_BUNDLE_ACCEPTANCE_R1 = CLOSED.**
- Persistence audit found a convergent fixed-descendant **16-field** AttackMagic server-state layout: four proficiency levels (`CHAR_*_EXP`), four resistance levels (`CHAR_*_RESIST`), four attack-training EXP counters (`CHAR_*_ATTMAGIC_EXP`) and four defense-training EXP counters (`CHAR_*_DEFMAGIC_EXP`). Generic player and embedded-pet save/load loops persist all `CHAR_DATAINTNUM` entries, so this is real descendant persistence state rather than display-only protocol data.
- Current `AttackMagicResistanceRuntime.levels` corresponds only to `CHAR_*_RESIST`; its `exps` corresponds only to `CHAR_*_DEFMAGIC_EXP`. The trainable player/pet caster's `CHAR_*_EXP` + `CHAR_*_ATTMAGIC_EXP` pair is a separate future seam.
- The Taiwan-v1 client gameplay schema exposes ordinary four-element attributes but no AttackMagic proficiency/resistance/training fields. Therefore the later server fields are **not** injected into v1 `PlayerState.fields` or `PetActor.state`; the battle-local overlay remains authoritative for the currently admitted enemy-caster path.
- **DESCENDANT_ATTACKMAGIC_16FIELD_SAVE_LAYOUT_R1 = CLOSED.**
- **RECOVERED25_ATTACKMAGIC_LOCAL_SAVE_MAPPING_R1 = OPEN.**
- Next priority: keep AttackMagic local-save migration fail-closed and resume the recovered non-common pet-skill backlog from the callback census, selecting the highest-impact still-unexecuted battle callback whose OPTION grammar and fixed-source handler can be closed without speculative semantics.

## Phase 1 recovered ENEMYSKILL_ReHP guarded reference boundary — 2026-10-01

- The non-common callback census makes `ENEMYSKILL_ReHP` the current next family: **1 referenced ID / 31 positive enemybase slot uses**.
- All three pinned fixed descendants compile `_PRO_BATTLEENEMYSKILL`; the callback itself ignores OPTION/data, writes symbolic `BATTLE_COM_S_ENEMYREHP`, copies the submitted target into COM2, marks the actor ready and returns TRUE.
- Battle execution target-adjusts COM2 first. If no valid opponent remains, the action stops before ReHP. If the ReHP effect returns FALSE, the dispatcher falls back to ordinary physical `BATTLE_Attack` against the already-adjusted opponent target rather than WAIT/NONE.
- The enemy-caster effect scans enemy-side slots **10..19** in ascending order and admits only alive entries with `HP < floor(MAXHP * 2 / 3)`; the threshold is strict.
- Successful ReHP consumes source RNG after caller-side target adjustment in exact order:
  1. eligible-ally index `RAND(0,n-1)`;
  2. base power `RAND(100,target_max_hp)`;
  3. `BATTLE_MultiRecovery` variance `RAND(power*0.9,power*1.1)`.
- All three pinned builds define `_MAGIC_REHPAI`; the active HP branch therefore bypasses ordinary percentage/recovery-rate scaling. HP is capped at max HP while the source reports the pre-cap recovery amount.
- Guarded command numbering is **compile-profile specific**: pinned gavin/iris resolve ReHP to **2014**, while pinned Bismarck resolves it to **2013** because `_SHOOTCHESTNUT` is disabled there. No universal recovered25 COM1 value is asserted.
- Added `tools/stoneage_enemy_rehp_model.py`, `tests/test_stoneage_enemy_rehp_model.py`, `research/mechanics/STONEAGE-ENEMY-REHP-R1.md` and dedicated CI. The reference model keeps an unknown recovered25 command profile fail-closed and rejects the unresolved reversed `RAND(100,max_hp)` edge for max HP below 100.
- Validation: dedicated ReHP reference workflow **36861530391 = PASS**; runtime bootstrap contract **36861530272 = PASS** at the same source commit `0a58b4911202f20a8aa02f11224256deb5b0e49e`.
- **ENEMYSKILL_REHP_GUARDED_REFERENCE_R1 = CLOSED_REFERENCE_MODEL_ONLY.**
- Next priority: hard-probe the single recovered ReHP row plus all **31** references, prove the referenced max-HP domain, then integrate exact target-adjust -> ReHP RNG -> ordinary-attack fallback ordering into recovered enemy AI / round / coordinator without inventing a historical numeric COM1 value.


## Phase 1 recovered ENEMYSKILL_ReHP runtime admission — 2026-10-01

- The preservation-bundle hard probe closed the ReHP data domain:
  - exact recovered callback population: **1 skill ID, 501**;
  - **31** positive enemybase slot references across **31** templates;
  - **28** runtime caster variants in **2** reachable groups;
  - **7** potential same-group heal-target variants;
  - minimum possible reachable target max HP is **602**, so the fixed
    `RAND(100,target_max_hp)` call never enters a reversed range in the
    admitted recovered25 encounter graph.
- Dedicated recovered bundle probe **36862737415 = PASS**.
- Runtime admission preserves the guarded-command uncertainty rather than
  guessing a historical numeric COM1:
  - the enemy-AI bridge emits a typed ReHP submission bound to recovered skill
    ID 501;
  - ordinary ATTACK is an explicitly modern **ordering carrier only** and is
    intercepted before physical execution;
  - `BATTLE_TargetAdjust`-shaped target repair occurs first with its own
    explicit RNG;
  - successful heal consumes explicit eligible-index -> base-power ->
    MultiRecovery-variance RNG in source order;
  - no eligible ally produces the fixed ordinary-attack fallback against the
    already-adjusted opponent and rejects any second retarget RNG;
  - status suppression/confusion remains ordered before ReHP execution and
    unused semantic RNG is rejected;
  - successful heal writes directly through the ordinary round HP map into
    persistent multi-round state.
- Validation:
  - ReHP semantic runtime **36865350487 = PASS**;
  - battle core **36865230127 = PASS**;
  - local runtime coordinator **36865229998 = PASS**;
  - Taiwan-v1 gameplay **36865230219 = PASS**;
  - runtime golden contract **36865230075 = PASS**.
- Executable recovered pet-skill slot-use coverage is now approximately
  **2255 / 2486 = 90.7%** when the previously closed stable-common families,
  AttackMagic (**106**) and ReHP (**31**) are counted; the separate **3** Merge
  uses remain intentionally classified historical UB rather than executable.
- **RECOVERED25_ENEMY_REHP_RUNTIME_R1 = CLOSED.**
- Next priority: `PETSKILL_DamageToHp` (**3 referenced IDs / 30 positive
  enemybase slot uses**). Re-audit its fixed-source callback/command/execution
  path, hard-probe all three recovered OPTION rows, then admit only the
  evidence-closed RNG/damage/HP-conversion semantics. Do not infer a guarded
  numeric COM1 from a different compile profile.


## Phase 1 recovered PETSKILL_DamageToHp runtime admission — 2026-10-01

- Fixed-source audit separates the older `_SKILL_DAMAGETOHP`
  `PETSKILL_DamageToHp` handler from the later
  `_PETSKILL_DAMAGETOHP` / `DamageToHp2` variant. They are not flattened.
- The older callback contains a real integer-arithmetic quirk:
  `atoi(token1) / 100` executes as C integer division before assignment to
  float.
- Preservation-bundle hard probe **36866862704 = PASS** and closes all three
  recovered rows:
  - ID **503**: token1=30 -> integer ratio 0; recovery **50%**;
  - ID **504**: token1=20 -> integer ratio 0; recovery **70%**;
  - ID **505**: token1=10 -> integer ratio 0; recovery **100%**;
  - all are ASCII two-field OPTIONs;
  - total pressure is **30** positive enemybase slot uses across **30**
    templates.
- Recovered25 runtime admission uses a typed semantic submission rather than a
  guessed guarded numeric COM1.
- Exact physical ordering now represented:
  - one ordinary TargetAdjust;
  - specialized Guardian quirk where AttackSeq may calculate against the
    Guardian but DamageSub still settles against the original adjusted target;
  - pre-existing DamageReact on that original target disables HP conversion;
  - otherwise ordinary physical damage resolves;
  - post-hit conversion uses source-returned `damage + petdamage`;
  - mounted targets therefore use rider amount + ride-pet amount, preserving
    the source split's two +1 terms;
  - attacker HP recovery is integer-truncated and max-HP capped before the
    persistent round advances.
- Validation at `59e85a8a9531206ce1465ba7ce805f408571716f`:
  - DamageToHp runtime **36868357706 = PASS**;
  - battle core **36868357723 = PASS**;
  - stable pet-skill core **36868357938 = PASS**;
  - local runtime coordinator **36868357914 = PASS**;
  - runtime golden **36868357741 = PASS**;
  - Taiwan-v1 gameplay **36868357811 = PASS**;
  - ReHP and AttackMagic coordinator/state regressions also PASS.
- Executable recovered pet-skill slot-use coverage is now approximately
  **2285 / 2486 = 91.9%**. The separate **3** Merge uses remain intentionally
  classified historical UB rather than executable.
- **RECOVERED25_DAMAGETOHP_RUNTIME_R1 = CLOSED.**
- Next priority: `PETSKILL_MpDamage` (**3 referenced IDs / 25 positive
  enemybase slot uses**). Re-audit the fixed callback, OPTION grammar, guarded
  command identity, target/MP mutation and any physical fallback/secondary
  effects; then hard-probe all three recovered rows before runtime admission.


## Phase 1 recovered PETSKILL_MpDamage runtime admission — 2026-10-01

- Fixed-source audit across the pinned gavin/iriselia/Bismarck descendants
  converges on the guarded `_Skill_MPDAMAGE` callback and
  `BATTLE_S_MpDamage` helper.
- The callback repeats the same source arithmetic quirk as the older
  DamageToHp handler: `(float)(atoi(token1)/100)` performs integer division
  first.
- Preservation-bundle hard probe **36869183326 = PASS** closes all three
  referenced recovered25 rows:
  - ID **506**: token1=50 -> callback integer ratio 0; MP loss **50%**;
  - ID **507**: token1=50 -> callback integer ratio 0; MP loss **75%**;
  - ID **508**: token1=50 -> callback integer ratio 0; MP loss **100%**;
  - all three are FIELD=1, TARGET=6, COST=2, ASCII two-field OPTIONs;
  - total pressure is **25** positive enemybase slot uses across **25**
    templates.
- Fixed post-hit semantics are now represented:
  - ordinary TargetAdjust runs once;
  - specialized Guardian calculation/original-defindex settlement is
    preserved;
  - pre-existing DamageReact on the original adjusted target suppresses MP
    loss;
  - `damage < 1` suppresses MP loss;
  - ENEMY and PET targets are excluded by the fixed helper;
  - PLAYER current MP must be positive;
  - MP loss is `int(current_mp * percent / 100)`, independent of physical
    damage magnitude.
- Runtime admission remains semantic/typed rather than inventing the guarded
  numeric COM1.
- Round-local MP is ordered state. Two admitted attackers therefore operate on
  the successively reduced current MP, not independently on the round-start
  value; the dedicated test verifies 40 -> 20 -> 5 for 50% then 75%.
- The local-session coordinator seeds player MP from the working persistent
  clone and writes the round's final MP back to that clone only; the original
  session snapshot remains unchanged.
- Current repaired HEAD
  `0e0917d320faa9eda90d4e9f315400713c14a753` passes:
  - MpDamage runtime **36870364373** (**67 tests**);
  - local runtime coordinator **run 163**;
  - enemy AttackMagic coordinator **run 8**;
  - enemy ReHP runtime **run 7**;
  - DamageToHp runtime **run 4**.
- Executable recovered pet-skill slot-use coverage is now approximately
  **2310 / 2486 = 92.9%**. The separate **3** Merge uses remain intentionally
  classified historical UB rather than executable.
- **RECOVERED25_MPDAMAGE_RUNTIME_R1 = CLOSED.**
- Next priority: `PETSKILL_FallGround` (**1 referenced ID / 23 positive
  enemybase slot uses**). Re-audit its fixed-source callback/command/execution
  path and OPTION grammar, hard-probe the exact recovered row and usage
  context, then admit only source-backed target/state/RNG semantics.


## Phase 1 recovered PETSKILL_FallGround runtime admission — 2026-10-01

- Fixed-source audit confirms a dedicated `BATTLE_S_FallGround` executor
  rather than the generic pet physical wrapper.
- Preservation-bundle hard probe **36871586479 = PASS**:
  - exactly **1** recovered callback row, skill ID **210**;
  - **23** positive enemybase slot uses across **23** templates;
  - FIELD=1, TARGET=6, COST=2, ILLEGAL=3000;
  - OPTION decodes identically under strict CP950/Big5 and contains the exact
    `攻%-30` mechanic;
  - callback attack power is therefore exactly 70% of recovered FIXSTR for the
    positive integral enemy domain.
- Runtime admission uses a typed semantic submission and does not guess the
  guarded numeric FALLRIDE command value.
- Dedicated physical/fall ordering is represented:
  - TargetAdjust once;
  - callback attack-power mutation before physical calculation;
  - DamageReact blocks fall;
  - positive post-DamageSub player damage gates `RAND(0,100)`;
  - zero-resistance cross-descendant threshold is strict `roll > 50`;
  - nonzero equipment fall resistance remains fail-closed because
    gavin/iriselia and Bismarck compile profiles diverge;
  - successful fall unmounts the battle-local ride pet and sets PETFALL.
- Historical bug preserved: none of the three pinned descendants enables
  `_FIXPETFALL`; PLAYER unmount therefore tests `CHAR_RIDEPET > 0`.
  A ride pet in source slot **0** remains mounted even after a successful fall
  roll.
- Integration regression repairs:
  - `ebd497e15d08ddd7bb2b6985310faf03520fe020` moved setup-effect
    initialization before FallGround validation;
  - `9e6a4c2687c184b1a0b336aeb5ee06ac970a7331` scoped source-slot
    requirements to FallGround actions;
  - `e62c938fe782e24eedad80c575ba034752312f96` restored ordinary ride-pet
    provenance compatibility outside FallGround rounds.
- Final repaired validation at `e62c938fe782e24eedad80c575ba034752312f96`:
  FallGround **36874842586**, battle core **36874842626**, local runtime
  **36874842540**, DamageToHp **36874842608**, MpDamage **36874842676**,
  ReHP **36874842571**, AttackMagic coordinator **36874842524**, AttackMagic
  round **36874842784**, Taiwan-v1 gameplay **36874842624**, and recovered25
  region/runtime-stack **36874842303** all PASS.
- Executable recovered pet-skill slot-use coverage is now approximately
  **2333 / 2486 = 93.8%**. The separate Merge historical-UB uses remain
  intentionally non-executable.
- **RECOVERED25_FALLGROUND_RUNTIME_R1 = CLOSED.**
- Next priority is no longer hand-maintained: the new preservation-bundle
  callback-pressure probe will select the highest-pressure remaining OPEN
  callback directly from active recovered25 `petskill + enemybase` data.
