# Historical Timeline — Working Draft

This timeline intentionally distinguishes confirmed evidence from unresolved interpretation. It will be revised as primary sources are recovered.

## 1999 — JSS origin period

### March 1999 — public exhibition context

**FACT:** Contemporary PC Watch coverage of Tokyo Game Show '99 Spring records `STONEAGE` being prominently exhibited in NTT Data's `Gamer's Dream` booth as the platform's third title. This establishes that the title was already being publicly promoted by **1999-03-19**. [`SRC-JP-1999-PCWATCH-TGS-SPRING`]

**OPEN:** Determine which build was shown, whether it was playable, and whether any event/demo media or screenshots survive with provenance.

### April 1999 onward — Gamer's Dream web archive exists

**FACT:** The Wayback record for the original Gamer's Dream index path reports captures beginning **1999-04-22**, before the later StoneAge beta and commercial launch. [`SRC-JP-GD-INDEX-ARCHIVE-01`]

**RESEARCH CONSEQUENCE:** The 1999 web layer is not presumed lost. Recovery should continue by historical path/timestamp, especially product, registration, beta, download, shop and support pages.

### May 1999 — published design intent

**FACT:** `Play Online` issue 012 describes Japan System Supply's then-in-development `STONEAGE` as a relaxed Stone Age RPG whose published design pitch emphasized food/resources, community, and player cooperation contributing to village development. [`SRC-JP-1999-PLAYONLINE-012`]

**IMPORTANT LIMIT:** This is evidence for **pre-launch design intent**, not automatic proof that every described mechanic shipped unchanged in the final October client.

**RESEARCH CONSEQUENCE:** The project's earlier hypothesis that resource/community/village-life ideas may belong to the original JSS conception is now partially promoted to FACT at the level of documented May 1999 design intent.

### August 1999 — beta recruitment closes

**FACT:** `Play Online` issue 015 records **1999-08-20** as the beta application deadline, with 200 reader accounts and lottery selection if oversubscribed. [`SRC-JP-1999-PLAYONLINE-015`]

**OPEN:** Recover the exact application URL printed on the page and the corresponding August 1999 Gamer's Dream/JSS recruitment page.

### September 1999 — beta test

**FACT:** A `STONEAGE` beta test ran from **1999-09-01 through 1999-09-30** according to contemporaneous `Play Online` issue 015. [`SRC-JP-1999-PLAYONLINE-015`]

**OPEN:** Recover beta client, installer filename, distribution instructions/media, internal version number, file hashes, and beta-to-retail differences.

### 1999-09-17 — Tokyo Game Show '99 Autumn

**FACT:** PC Watch reported `STONEAGE` at the Gamer's Dream booth and identified Japan System Supply as publisher. It gave **1999-10-15** as the scheduled release date. [`SRC-JP-1999-PCWATCH-TGS-AUTUMN`]

**FACT:** The same report describes the contemporary experience in terms of living as a Stone Age inhabitant, hunting dinosaurs, chatting with other players, and adventuring with companions in a deliberately gentle atmosphere. [`SRC-JP-1999-PCWATCH-TGS-AUTUMN`]

### 1999 retail advertising

**FACT:** A photographed period magazine advertisement for JSS `STONEAGE` gives Windows 95/98 as the platform, **1999-10-15** as the scheduled release date, and **8,800 yen before tax** as the planned price. It also prints the period domains `www.titan.co.jp` and `www.gamersdream.ne.jp`. [`SRC-JP-1999-AD-YAHOO-01`]

**FACT:** The same advertisement visibly promotes an original mug as a reservation bonus and a `STONEAGE` special CD as an initial-edition bonus/feature. This materially strengthens the separate marketplace lead for a surviving first-edition package with bonus CD. [`SRC-JP-1999-AD-YAHOO-01`, `SRC-JP-1999-RETAIL-MERCARI-01`]

**OPEN:** Identify the original magazine issue/page and determine whether the advertised special CD is distinct from the game install/client disc, and what it contains.

### 1999 retail package identifier

**FACT (surviving-package photograph):** A preserved Yahoo! Auctions listing for a seller-described unopened early JSS `STONEAGE` package exposes front/side/back photographs. The back-box barcode is directly readable as **JAN `4909476303010`**. This assignment is based on the photographed StoneAge package itself, not on numerical extrapolation from other JSS products. [`SRC-JP-1999-RETAIL-YAHOO-UNOPENED-01`]

**EVIDENCE LIMIT:** The marketplace photograph supports the literal visible package field at B-level; it does not provide S-grade chain of custody, the still-unresolved package model/type code, disc matrix identifiers, or client filesystem/binary evidence.

### 1999 commercial product requirements

**FACT (archived first-party product page):** An original Gamer's Dream StoneAge product page preserved by Wayback lists:

- release date **1999-10-15**;
- package price 8,800 yen;
- MMX Pentium 200 MHz or better;
- at least 400 MB HDD free space;
- at least 64 MB RAM;
- 4x-speed or faster CD-ROM drive;
- 33.6 Kbps or faster modem / Internet access;
- at least 2 MB VRAM;
- DirectX 6.1-compatible video and sound hardware;
- mouse and keyboard. [`SRC-JP-GD-STONEAGE-INTRO-ARCHIVE-01`]

**FACT:** The same first-party page tells prospective users to purchase the software package first and then register for Gamer's Dream service. [`SRC-JP-GD-STONEAGE-INTRO-ARCHIVE-01`]

**RESEARCH CONSEQUENCE:** The retail release had a normal package-based client/install path. The separately advertised initial-edition special CD must remain a distinct artifact hypothesis until package contents prove otherwise.

### Retail installation and registration architecture

**FACT (archived first-party JSS manual):** The official manual explicitly tells users to insert the StoneAge **game CD**, from which the installer starts automatically. DirectX 6.1 is stated to be included on the game CD. Installation modes were standard (StoneAge + DirectX), minimum (StoneAge only), and custom; a documented workaround could omit the `map` component. [`SRC-JP-JSS-STONEAGE-MANUAL-ARCHIVE-01`]

**FACT:** The same manual documents a physical **CD NUMBER card** whose CD NUMBER was required when contracting/registering for Gamer's Dream service. It also shows `[Stoneage]` -> `[stoneage]` as the Windows Start-menu path and a `screenshot` subdirectory beneath the StoneAge folder for F12 captures. [`SRC-JP-JSS-STONEAGE-MANUAL-ARCHIVE-01`]

**RESEARCH CONSEQUENCE:** Physical-media recovery should independently seek the normal game CD, CD NUMBER card, manuals/inserts, and the advertised initial-edition special CD. Singular wording `game CD` does not establish the total package disc count.

### 1999-10-15 — Japanese commercial start

**FACT (working, high confidence):** The best current evidence supports **1999-10-15** as the Japanese JSS commercial service start date. A contemporaneous 1999-09-17 PC Watch report lists that date as scheduled release, an archived Gamer's Dream product page lists it as the release date, and a 2009 4Gamer tenth-anniversary/service-end retrospective states that service started on that date. [`SRC-JP-1999-PCWATCH-TGS-AUTUMN`, `SRC-JP-GD-STONEAGE-INTRO-ARCHIVE-01`, `SRC-JP-2009-4GAMER-10TH`]

**OPEN:** Recover the first retail install/client CD-ROM / initial-edition package with provenance, image/dump the media, and extract internal executable/version metadata.

### 1999-10-18 onward — active JSS version-up stream

**FACT (archived first-party JSS):** JSS's preserved StoneAge version-up page contains an automatic update history beginning **1999-10-18**, only three days after commercial launch. The history continues with frequent fixes and additions through the original JSS service period. [`SRC-JP-JSS-STONEAGE-VERUP-ARCHIVE-01`]

**RESEARCH CONSEQUENCE:** The 1999 Japanese client cannot be modeled as a single immutable build. At minimum the archaeology must distinguish the September beta, the 1999-10-15 retail-disc baseline, and post-launch patched states.

### Confirmed JSS launcher filename

**FACT (archived first-party JSS):** JSS published a replacement StoneAge startup program named **`stoneage.exe`**, advertised as **212 KB**, with instructions to overwrite the same-named file in the existing StoneAge installation directory. [`SRC-JP-JSS-STONEAGE-LAUNCHER-ARCHIVE-01`]

**FACT:** The replacement launcher was documented as addressing startup network errors, version-up errors, and failure to transition to the new program after updating. [`SRC-JP-JSS-STONEAGE-LAUNCHER-ARCHIVE-01`]

**OPEN:** Wayback exposes an archived `stoneage.exe` binary path, but the current environment has not extracted the bytes. Hashes, PE metadata, version resources and exact binary relationship to the 1999 retail launcher therefore remain unresolved.

### JSS updater filesystem/checksum architecture

**FACT (archived first-party JSS FAQ):** Update troubleshooting instructs users to clear files from the StoneAge installation's **`data\download`** directory, clear Windows `Temporary Internet Files`, then restart StoneAge and retry the update. The FAQ documents repeated-download/save failures and an update-download error containing **`cksum:xxxxxxxxx`**, and discusses proxy settings in the same context. [`SRC-JP-JSS-STONEAGE-FAQ-ARCHIVE-01`]

**FACT:** Cleanup instructions for data left by an earlier StoneAge test tell users to uninstall the game, completely remove **`ProgramFiles\jss\stoneage`**, and then install the retail product. The exact name/label of that earlier test is not reconstructed from damaged archive text. [`SRC-JP-JSS-STONEAGE-FAQ-ARCHIVE-01`]

**RESEARCH CONSEQUENCE:** `data\download`, `ProgramFiles\jss\stoneage`, `cksum`, `MFC42.DLL`, `stoneage.exe` and the Windows cache/proxy references are now concrete anchors for locating update manifests, payloads, configuration and surviving client trees.

### Surviving physical-media lead

**OPEN / acquisition lead:** A marketplace listing preserves photographs/descriptive evidence for a purported unopened Japan System Supply `STONEAGE` initial limited edition package, including a seller-described bonus CD-ROM and 1999 Tokyo Game Show promotional material. This is not yet treated as verified original media. [`SRC-JP-1999-RETAIL-MERCARI-01`]

**NEXT VERIFICATION STEP:** obtain direct package/disc imagery or a provenance-preserving dump, then record product identifiers, disc matrix text, file tree, hashes, PE metadata, README/version strings, CD NUMBER card, and package documentation. `stoneage.exe` is now a confirmed filename to check immediately on any recovered disc/file tree.

## 2000 — JSS collapse and service boundary evidence

### 2000-10-16 — JSS business cessation reported

**FACT:** 4Gamer contemporaneously reported that JSS had effectively ceased business, that LIFESTORM/LIFESTORM2 service and support ended, and that StoneAge support had ended while Gamer's Dream was determining whether the StoneAge service itself could continue. [`SRC-JP-2000-4GAMER-JSS-STOP`]

### 2000-11-10 — Gamer's Dream transition notice

**FACT (archived first-party):** Gamer's Dream's own transition notice states that JSS had handled the StoneAge game-application side, including software corrections and version upgrades, while Gamer's Dream handled server/service operation and billing. [`SRC-JP-GD-JSS-TRANSITION-2000-01`]

**FACT:** After JSS's failure, Gamer's Dream could continue only a reduced service; JSS-dependent technical support/content-event support/version upgrades could no longer continue in the same way, and package sales through the Gamer's Dream online shop were stopped. [`SRC-JP-GD-JSS-TRANSITION-2000-01`]

**RESEARCH CONSEQUENCE:** Recovered executable/data/version-update artifacts should be classified as JSS client/application lineage unless evidence shows they are platform infrastructure; Gamer's Dream account/billing/server pages are service-platform evidence rather than automatically part of the client.

## 2000 — Taiwan branch

**FACT (working):** Taiwan operation followed the Japanese launch and represents an early localization/evolution branch.

**OPEN:** Determine exactly which systems, assets, text, maps, pets, and lore were inherited, localized, modified, or newly added.

## 2001 — Mainland China early era

**FACT (working):** Mainland operation followed, with 1.82 becoming an important early/classic reference point for Chinese players.

**OPEN:** Determine exact relationship between JSS/Taiwan version numbering and Mainland 1.82; avoid assuming a single linear version-number tree until evidence proves it.

## 2003 — Japanese revival as a near-descendant comparison anchor

### 2003-07-26 — revival announcement and former-service riding boundary

**RETROSPECTIVE FACT / B-level:** In its 2003 revival coverage, 4Gamer describes the former Japanese StoneAge as already having monster capture/pets, turn-based combat, and parties of up to five players. [`SRC-JP-2003-4GAMER-OGF-REVIVAL-01`]

**RETROSPECTIVE FEATURE BOUNDARY / B-level:** The same report states that during the former Japanese operation, **only GMs could ride dinosaurs**. The project's working JSS/Japanese-original baseline therefore treats normal-player pet riding as **not available**, unless stronger primary JSS evidence later contradicts this. [`SRC-JP-2003-4GAMER-OGF-REVIVAL-01`]

**IMPORTANT LIMIT:** This is a near-contemporary specialist-media retrospective, not a recovered 1999 client/manual/patch note. It constrains feature availability but does not date the GM-only riding implementation to an exact JSS build.

### 2003-09-27 — TGS revival hands-on and original trade-UI boundary

**DIRECT 2003 STAFF COMMENT / A-B level:** When 4Gamer asked on-site staff whether the revival was completely the same as the earlier game, the response was that it was **basically the same**, with restoration/bug fixing being the immediate focus and larger map/character additions planned after open beta. [`SRC-JP-2003-4GAMER-TGS-REVIVAL-01`]

**RETROSPECTIVE FEATURE BOUNDARY / B-level:** The report identifies the dedicated **item trade window as a minor change that the original did not have**, and describes the older exchange context as placing items on the ground. [`SRC-JP-2003-4GAMER-TGS-REVIVAL-01`]

**RESEARCH CONSEQUENCE:** A recovered 2003 Japanese revival client is useful as a near-descendant diff anchor, but later UI additions—especially the dedicated trade window—must not be projected backward into the JSS baseline.

## Later evolution

Major later releases added systems and lore that should be studied as historical layers rather than retroactively assumed to have existed in 1999.

Research categories include:

- pet riding;
- family/guild systems;
- spirit-king lore;
- ancient civilization / mechanical civilization lore;
- new continents;
- additional pets, maps, and progression systems.

## Rule for this file

Every precise date, version number, feature-first-appearance claim, and lore-first-appearance claim should reference a source record ID from `SOURCE-REGISTRY.md` once a structured record exists.
