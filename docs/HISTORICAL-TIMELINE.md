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

### Preserved Taiwan v1.0 retail disc

**FACT / S-level preserved media:** A publicly preserved original Taiwan retail disc is now byte-verified as **StoneAge v1.0**, published by **華義國際股份有限公司 / Waei International Entertainment** and developed by **Japan System Supply Ltd.** The physical mastering ring reads `華義國際股份有限公司 石器時代 V1.0 P-RPG-0008`; Redump record 104630 and DiscImageCreator submission metadata independently pin the same media identity. [`SRC-TW-2000-WAEI-V10-REDUMP-104630`]

**FACT / S-level byte identity:** The one-track MODE1/2352 image is 523,449,360 bytes with CRC32 `e4638c81`, MD5 `b477bfc2b62527b255ab9f822349dc14` and SHA1 `d0f270163772eb587185a65e24a3f7e565263f2f`. The recovered Internet Archive preservation copy matches Redump's exported hashes exactly. [`SRC-TW-2000-WAEI-V10-REDUMP-104630`]

**FACT / direct client tree:** The disc exposes a complete StoneAge subtree with `StoneAge.exe`, `sa_3.exe`, installer files and early resource containers `real_1.bin / adrn_1.bin / spr_1.bin / spradrn_1.bin`, plus battle maps, BGM and SFX. Bounded executable/text inspection also exposes the historical operator host `stoneage.waei.net`. [`SRC-TW-2000-WAEI-V10-REDUMP-104630`]

**IMPORTANT LIMIT:** This establishes a clean early **Taiwan-localized JSS-derived branch**, not byte identity with the 1999 Japanese beta/retail client. Localization, executable changes, server configuration and data additions/removals must be determined by future JSS/Korean diffs rather than assumed.

**RESEARCH CONSEQUENCE:** Taiwan v1.0 is now the project's primary current reverse-engineering specimen. The unresolved question has shifted from “do we have any early clean client?” to “which structures are inherited JSS core versus Taiwan localization/operator additions?”

## 2001 — Mainland China early era

### 2001-01-10 — Mainland launch publication chain

**FACT / contemporaneous launch report:** Sina records the Beijing launch on **2001-01-10** and identifies JSS as producer, Beijing Waei as authorizer, Zhiguan Electronics (Beijing) as agent, and **广西金海湾电子音像出版社** as publisher/distributor. The same report states that **four different package variants** were issued. [`SRC-CN-2001-SINA-STONEAGE-MAINLAND-LAUNCH-01`]

**INDEPENDENT CORROBORATION:** a 2002 Peking University paper independently states that 广西金海湾音像出版社 formally issued StoneAge on **2001-01-10**, with Zhiguan providing technical support and Waei handling sales/service. [`SRC-CN-2002-PKU-STONEAGE-MAINLAND-DISTRIBUTION-01`]

**CURRENT SURVIVAL LEAD / NOT AUTHENTICATION:** modern public indexes contain second-hand title strings naming StoneAge together with 广西金海湾 and, separately, 北京华义. These establish a concrete public search surface for surviving physical material but do not identify a specific first pressing. [`SRC-CN-2026-JD-STONEAGE-JINHAIWAN-SURVIVAL-LEAD-01`]

**PHYSICAL-ID REFINEMENT / 2026-09-27:** a clearer mirror of the surviving early Mainland client-disc photograph exposes a publication-number line provisionally read as `ISBN 7-900323-57-0/TP·026`. The publisher prefix `7-900323` is independently assigned to 金海湾电子音像出版社 by a publisher-code table. The full item suffix remains provisional pending independent bibliographic or higher-resolution physical confirmation; exact IA/DiscMaster searches for the provisional ISBN return zero hits. [`SRC-CN-2020-SOHU-EARLY-MAINLAND-DISC-MIRROR-01`] [`SRC-CN-MCSC-JINHAIWAN-ISBN-PREFIX-01`]

**RECOVERY PRIORITY:** resolve readable package/disc identifiers or a public optical image/file tree. Because this is the initial Mainland official publication chain, a verified specimen would outrank later 2.5 secondary carriers for early Mainland byte provenance.


**FACT (working):** Mainland operation followed, with 1.82 becoming an important early/classic reference point for Chinese players.

**OPEN:** Determine exact relationship between JSS/Taiwan version numbering and Mainland 1.82; avoid assuming a single linear version-number tree until evidence proves it.



## 2001–2002 — Mainland StoneAge 2.x → 2.5 distribution bridge

### 2001-12-04 — official StoneAge2 guide snapshot

**FACT / official preserved page:** Waei's `/ZHUANQU/stoneage2/tyro/upgrade.asp` is replayable at **2001-12-04 16:57:11 UTC**. The clean page body explicitly identifies **石器时代2.0** and is a character-leveling / required-experience guide, not a software update/download page. Its clean replay SHA-256 is `73fde66ffb3c92261d66715f873fa9b9f54166e4443d5d29924fe137cdcb8d35`; structural extraction yields 99 site references and no strong payload reference. [`SRC-CN-2001-2002-WAEI-STONEAGE2-UPGRADE-PATH-01`]

**CORRECTION:** The English pathname `upgrade.asp` previously invited a software-upgrade interpretation. The preserved Chinese body disproves that reading for the 2001 capture: `升级` here refers to leveling. February-2002 official pages later link the same pathname, but the destination body for that rollout period is unpreserved, so no 2.5 payload semantics may be projected from the 2001 snapshot.

### 2002-01/02 — StoneAge 2.5 rollout and distribution

**FACT / contemporaneous portal records:** 17173 and Sina both place the 2.5 retail launch on **2002-01-20**, describe early-February server migration, and report an **8.25 MB** updater for existing 2.x users. Sina gives the server-upgrade start as **2002-02-04**. [`SRC-CN-2002-17173-SA25-UPGRADE-01`] [`SRC-CN-2002-SINA-SA25-UPGRADE-01`]

**SOURCE CONFLICT:** The full package is reported as **580 MB** by 17173 and **575 MB** by Sina. Both values remain preserved pending recovery of first-party bytes or file listings.

**FACT / distribution topology:** Both records say the complete package/updater could be obtained from Beijing Waei and enumerate multiple Jan/Feb-2002 magazine/guide cover-disc channels. Current public DiscMaster/Internet Archive carrier searches return no strict 2.5 carrier, and a bounded Waei-domain Q1-2002 binary-index scan likewise yields no strict 2.5 installer/updater candidate after false-positive filtering.

**PRESERVATION REFINEMENT / 2026-09-27:** one named carrier, `《大众软件CD——大众游戏》2002年2月号`, now has a surviving paper-magazine preservation control: IA item `popsoft-magazine_202403` contains original February-2002 A/B scans, and bounded OCR confirms 2.5-related text in issue A. The same IA item exposes **no optical-disc image**. The only broad 2002 `大众软件` software hit is an unrelated 实达 modem ISO and is rejected. This narrows the unresolved object to the actual cover-disc/optical carrier rather than the magazine issue itself. [`SRC-CN-2002-POPSOFT-SA25-FEB-SCAN-01`]

**RESEARCH CONSEQUENCE:** Exact named cover-disc issues and contemporaneous installed-tree/cache backups now outrank broad Waei-domain filename searches as the next Mainland 2001–2002 recovery surface.




### 2002-01-20 onward — Mainland 2.5 physical client carriers

**FACT / contemporaneous product surface:** The 17173 2.5 product page identifies **延年益兽包** and **春满钱坤包** as products containing a **StoneAge 2.5 client CD**, and states that the **2.5新手报到包** existed in **three package variants**. Combined with the contemporaneous 17173/Sina rollout records placing retail launch on **2002-01-20**, these are concrete operator-era physical-carrier classes for complete-client recovery. [`SRC-CN-2002-17173-SA25-PRODUCT-01`] [`SRC-CN-2002-17173-SA25-UPGRADE-01`] [`SRC-CN-2002-SINA-SA25-UPGRADE-01`]

**MODERN COLLECTOR CONTROL:** A surviving 2020 Bahamut collector article documents the same 2.5 package family, including many new-user cover variants, a green WGS gift box and a simplified client package. This is useful for visual identification of surviving media but is not contemporaneous proof of disc bytes. [`SRC-CN-2020-BAHAMUT-SA25-CLIENT-PACKAGES-01`]

**RECOVERY CONSEQUENCE:** Prioritize public read-only ISO/file-tree recovery from these source-named client-CD package families. Package artwork alone cannot establish pressing identity or byte equivalence.


**PROVENANCE CONTROL / 2003 evidence added 2026-09-27:** Beijing Waei publicly warned about a different secondary StoneAge guide product that bundled a client CD but used a **network-downloaded client rather than an official Waei product disc**. This establishes a project-wide rule for 2.x/2.5 physical-media archaeology: a carrier may contain useful client bytes without inheriting official operator-media provenance. Carrier provenance and payload identity must therefore be tracked independently. [`SRC-CN-2003-WAEI-SECONDARY-GUIDE-CLIENT-CD-WARNING-01`]


**MODERN SURVIVING-SPECIMEN CONTROL (2020):** Bahamut article `snA=81388` separately documents a surviving **延年益壽包** and explicitly labels a photographed item as a **2.5-era disc** and the following item as a **2.5 manual**. A corrected body-window probe now recovers that exact source-labelled disc photograph from both the creator page and forum page as `https://truth.bahamut.com.tw/s01/202009/1eabce5c4adf3b26366bebea7d788c74.JPG` (160,151 bytes; 1128×774; photo SHA-256 `385071cb52f3e9af540823ff8a1833cfba4dad04ee8ab2ee9beebfa67dadea6a`). The initial broad-context association to an `延伸閱讀` thumbnail is superseded and must not be reused. Read together with contemporaneous product/upgrade records, this materially strengthens the physical-carrier identity control, but the recovered hash is the photograph hash only: no disc filesystem, ISO/client checksum, mastering identity or clean-client bytes are established. [`SRC-CN-2020-BAHAMUT-SA25-YANNIAN-PHYSICAL-01`]

**INDEPENDENT SURVIVOR CONTROL (2016):** A separate SMZDM player/collector post states that the author retained installation discs for **2.5, 3.0, 4.0, 5.0 and 疯狂原始人** after a separately described 2.0 disc. The recovered HTML has six install-disc photos; the five post-2.0 images follow that version list in article order, making the second photo a high-confidence visual candidate for the 2.5 disc. This remains visual/order evidence only, not filesystem or byte provenance. [`SRC-CN-2016-SMZDM-SA25-INSTALL-DISCS-01`]

**BYTE-LEVEL NEGATIVE CONTROL (publicly preserved optical object; catalogue date not independently authenticated):** Internet Archive item `sa-arena` preserves a complete BIN/CUE object with ISO9660 volume label **`SA_ARENA`**. Its hash-locked GB18030 README identifies the product as **`疯狂原始人`**, gives the default path `C:\\Program Files\\Waei\\疯狂原始人\\`, and explicitly lists **`《石器时代》、《大法师》、《疯狂原始人》`** as separate games sharing the WGS charging system. This byte-derived distinction confirms that `疯狂原始人` must not be treated as a synonym or carrier label for StoneAge 2.5. The current IA `2002-05-29` date/creator fields remain catalogue metadata rather than independently verified release facts. [`SRC-CN-IA-SA-ARENA-OPTICAL-01`]

## 2002-01-31 / 2002-02-12 — 21CN native catalogue resolves the StoneAge 2.5 updater

**FACT / contemporaneous third-party distribution catalogue:** 21CN native record `list.php?id=20165` has a preserved HTTP-200 capture at **2002-02-12 01:05:02 UTC**. The page itself gives catalogue整理日期 **2002-01-31**, title **`石器时代2.5—精灵王传说`**, software version **`客户端升级包`**, file size **8473K** (later rendered **8.27M**), system platforms Win9x/WinME/WinNT/Win2000/WinXP, and software company **北京华义**. [`SRC-CN-2002-21CN-SA25-UPDATER-01`]

**FACT / exact delivery identity:** The same earliest page directly links `http://download.21cn.com/file/game/maoxian/sa25up.zip` and `sa25up.jpg`. This independently resolves the historical `sa25up.zip` token as the 2.5《精灵王传说》**客户端升级包**, not the 575/580 MB complete client package. The identification no longer depends on interpreting the filename suffix `up`.

**FACT / mirror-topology evolution:** A preserved 2002-10-17 `downit.php?id=20165&num=0` router page references `http://images.21cn.com/download/file/game/maoxian/sa25up.zip`; later 2003–2004 catalogue/router pages migrate the same basename through `file1/`, `dg.download.21cn.com`, `file1_21cn/`, `file1xjy/` and `file1xzm/` path families. [`SRC-CN-2002-21CN-SA25-UPDATER-01`]

**IMPORTANT LIMIT:** These pages establish package identity, expected size, Beijing-Waei attribution in the 21CN catalogue and the historical mirror topology. The ZIP bytes remain unrecovered, so clean-byte provenance, archive members and operator-to-21CN byte identity remain OPEN.

**RESEARCH CONSEQUENCE:** The recovery target is now an exact ~8.27 MB updater with a finite evidence-derived mirror set. If recovered, its file inventory and resource deltas should be compared against the Taiwan-v1 baseline, the mixed 2.5 bridge and June-2003 map snapshot; only real recovered bytes can move the field-map provenance anchor earlier.


## 2003 — Mainland historical map-cache bridge




### 2002-01-31 / 2002-02-12 — 21CN native StoneAge 2.5 upgrade record resolves `sa25up.zip`

**FACT / native 21CN catalogue:** Archived ranking links independently resolve `石器时代2.5-精…` to **`list.php?id=20165`**. The exact record has archived HTTP-200 captures beginning **2002-02-12 01:05:02 UTC**. Its native detail page is titled **`石器时代2.5—精灵王传说`** and records an internal整理 date of **2002-01-31**. [`SRC-CN-2002-21CN-SA25-UPDATER-01`]

**FACT / package classification:** The page explicitly says **`软件版本：客户端升级包`**, file size **`8473 k`** on the earliest replay and **`8.27M`** on later layouts, supported on Win9x/WinME/WinNT/Win2000/WinXP, with **`软件公司：北京华义`**.

**FACT / exact payload topology:** The 2002-02-12 page directly links `http://download.21cn.com/file/game/maoxian/sa25up.zip` and same-stem `sa25up.jpg`. Later captures preserve the same record while the mirror path migrates through `file1/` and `dg.download.21cn.com`.

**RESOLUTION:** The historical filename `sa25up.zip` is now identified at the catalogue-description level as the **StoneAge 2.5 client upgrade package**, not the 575/580 MB complete client package.

**SIZE BOUNDARY:** contemporaneous 17173/Sina reports describe the updater as **8.25 MB**, while 21CN reports this mirror as **8473 k / 8.27M**. Until the ZIP bytes are recovered, treat this as a small source/measurement discrepancy and do not assert byte-for-byte identity with the operator-referenced updater.

**ROUTER / PRESERVATION RESULT:** The archived **2002-10-17** `downit.php?id=20165&num=0` wrapper explicitly opens `http://images.21cn.com/download/file/game/maoxian/sa25up.zip`. Later pages expose several `file1/` / `dg.download.21cn.com` mirror generations. A bounded exact-Wayback pass over seven evidence-derived ZIP URLs finds **0 HTTP-200 ZIP captures**; the router-derived `images.21cn.com` URL survives only as two HTTP-404 rows in December 2005. Arquivo has no exact row; Common Crawl remains partial due service 504s. The updater is therefore **identified but not byte-recovered**.


### 2002-05-17 — 21CN archives the `sa25up.jpg` same-stem StoneAge sidecar

**FACT / recoverable archived object:** Wayback replays `http://download.21cn.com:80/file/game/maoxian/sa25up.jpg` at **2002-05-17 23:58:42 UTC** with HTTP 200. The recovered JPEG is 9,312 bytes, SHA-256 `7b475f1b3613d87e4e5747bb98d68ac186da265518359ac819b97c19b3b8b80e`, and 120×169 pixels. [`SRC-CN-2002-21CN-SA25UP-JPG-01`]

**VISUAL BOUNDARY:** transient inspection shows illustrated prehistoric/game-style character art with humans and dinosaur-like creatures, but the preserved resolution exposes no reliably readable title/version/operator text.

**EVIDENCE CONSEQUENCE:** this moves the recoverable 21CN-native `sa25up` object family back to May 2002, earlier than the 2003-06-05 archived `pcpc.idv.tw` link page. It still does not recover `sa25up.zip` bytes or establish clean byte provenance. The package **type** is now resolved independently by native 21CN record `20165` as a client upgrade package; exact byte identity with the operator-referenced 8.25 MB updater remains unproven.


### 2003-06-05 — dated StoneAge 2.5 `sa25up.zip` link survives

**FACT / dated archived third-party page:** A raw Wayback replay of `http://pcpc.idv.tw/soft/soft.htm` at **2003-06-05 10:48:51 UTC** contains the literal Big5/CP950 text **`[下載]石器時代2.5—精靈王傳說`** and the exact href `http://202.104.32.168/file/game/maoxian/sa25up.zip`. The replay is hash-locked as SHA-256 `604304bd2c931c463ccb575f3920dd096a340441825a58274d9f6e897dc966c5`. [`SRC-CN-2003-PCPC-SA25UP-SOURCE-ARCHIVE-01`]

**IMPORTANT LIMIT:** This establishes a terminus-ante-quem for the **link text and URL on the archived page**, not for live payload availability or official/operator provenance. Separate Wayback records for the payload path are HTTP 404, including malformed/suffixed URL forms indexed in 2002. The filename is now independently tied by native 21CN record `20165` to a client upgrade package, but the payload remains an artifact-recovery clue rather than authenticated client bytes because the ZIP body itself is not preserved.

**RESEARCH CONSEQUENCE:** The later Geocities/PIXNET copies are no longer the earliest evidence for this token. Native 21CN record `20165` now identifies `sa25up.zip` as the client updater; the **575/580 MB full-package filename remains unresolved**. Continue only from new updater mirror/preservation tokens or, preferably, from full-client/physical-media or contemporaneous installed-tree evidence capable of advancing map provenance.



### 2001-12-27 / 2002-02-01 — `sa25up.zip` IP host identified as 21CN download infrastructure

**FACT / dated archived host pages:** The historical IP `202.104.32.168`, later used by the surviving `/file/game/maoxian/sa25up.zip` URL, replays as the **21CN.COM download site**. The 2001-12-27 root is titled `21CN.COM - 下载`; 2002-02-01 software-detail pages expose `download.21cn.com`, `粤ICP证010001`, and `世纪龙信息网络有限责任公司版权所有`. [`SRC-CN-2001-2002-21CN-DOWNLOAD-HOST-01`]

**EVIDENCE CONSEQUENCE:** The payload host should be classified as third-party 21CN download infrastructure, not as a demonstrated Beijing-Waei host. This does not establish whether the mirrored StoneAge file was official, unmodified, complete, or even successfully downloadable at the surviving archive timestamps.

**RECOVERY CONSEQUENCE:** This target has since been resolved as native 21CN record `20165`. The catalogue identity, package class, size and router topology are recovered; the remaining 21CN gap is the absent ZIP body, and the tested exact mirror family is now bounded.


### 2003-06-23 — first recoverable full-map snapshot

**FACT / dated preserved binary:** The StoneAge map mirror `http://www.wuxitianlong.com/sa/map.exe`, independently exposed by contemporaneous Sina StoneAge download-hub material, has a replayable Wayback capture timestamped **2003-06-23 23:44:51 UTC**. The recovered package is hash-locked as SHA-256 `372426e46765a1cf479041bdafc1d3e58fb019117d00d0b43d6a5f796620776e`. [`SRC-CN-2003-WUXITIANLONG-MAP-PACK-ARCHIVE-01`]

**FACT / map corpus:** It contains 1,008 numeric DAT IDs, 995 strict three-plane-valid maps and 13 parser-invalid numeric DATs. The same 1,008 IDs exist in the separately preserved 2.5 bridge corpus; 993 are byte-identical and 15 differ. Direct Taiwan-v1 ADRN necessary-condition classification yields 773 compatible / 222 incompatible among the 995 parseable maps. [`SRC-CN-2003-WUXITIANLONG-MAP-PACK-ARCHIVE-01`]

### 2003-12-10 — second recoverable full-map snapshot

**FACT / dated preserved binary:** A second Wayback capture of the same mirror is byte-recoverable at **2003-12-10 09:24:26 UTC**, SHA-256 `5f7f58e0d26d596e926a7d551d7c24e8a9a27824d5bdc53be3955b19b0e13abc`. It contains 1,011 numeric DAT maps, including three IDs absent from June: `8008`, `8100`, `8101`. Of the 1,008 common IDs, 698 are byte-identical and 310 differ. [`SRC-CN-2003-WUXITIANLONG-MAP-PACK-ARCHIVE-02`]

**FACT / file-metadata stratum:** The archive preserves per-file modification times rather than one flattened package timestamp. A large batch of **337 maps** is stamped `2003-10-20`, including maps 1000, 2000, 3000 and 4000. However, some entries have dates as early as 1997; therefore these mtimes are useful internal stratification metadata but are **not** treated as literal StoneAge release/creation dates. [`SRC-CN-2003-WUXITIANLONG-MAP-PACK-ARCHIVE-02`]

### Three-state lineage correction

**FACT / byte-lineage comparison:** Across the 1,008 IDs common to June 2003, December 2003 and the separately preserved 2.5 map directory, the byte lineage is: **698 stable in all three; 295 June=preserved-2.5 with December alone divergent; 15 three-distinct**. No common map falls into a simple “June=December, then changed only in preserved 2.5” category. [`SRC-CN-2003-WUXITIANLONG-MAP-PACK-ARCHIVE-01`, `SRC-CN-2003-WUXITIANLONG-MAP-PACK-ARCHIVE-02`]

**FACT / resource-compatibility patterns:** Taiwan-v1 necessary-condition states over those same common IDs are **768 C→C→C, 4 C→C→I, 1 C→I→C, 222 I→I→I, 13 X→X→X**. The C→C→I maps are 1000/2000/3000/4000; map 60306 is C→I→C and the December state alone references absent-v1 resource ID `10940`.

**RESEARCH CONSEQUENCE:** The dated December package and the separately preserved 2.5 map directory are not placed on one assumed linear successor chain. They are treated as distinct descendant states/branches whose byte relationships can constrain archaeology. Taiwan-v1 field-map reconstruction still requires a pre-/near-v1 provenance anchor; neither old mtimes nor descendant resource compatibility can substitute for it.


## 2001–2003 — Korean 1.74 lineage control

**PRESERVED VERSION TRANSITION / C-B level:** Later preservation of dated Inium-era material identifies the Korean service state before its 2.0 family/riding preview as **1.74**. This is useful as a version-lineage clue but is not treated as original JSS version proof. [`SRC-KR-2001-INIUM-174-TO-20-PRESERVED-01`]

**CONTEMPORARY PRESERVED OPERATOR ANSWER / B-level:** A 2003-07-21 GameMeca preservation quotes Netmarble's StoneAge homepage answer stating that its 2003-07-28 service launch would use **version 1.74**. [`SRC-KR-2003-NETMARBLE-174-ANNOUNCE-01`]

**RESEARCH CONSEQUENCE:** Korean `1.74` is now a concrete historical client-recovery target. It must not be equated with a JSS internal version solely from the number.

## 2003 — Japanese revival as a near-descendant comparison anchor

### 2003-07-26 — revival announcement and former-service riding boundary

**RETROSPECTIVE FACT / B-level:** In its 2003 revival coverage, 4Gamer describes the former Japanese StoneAge as already having monster capture/pets, turn-based combat, and parties of up to five players. [`SRC-JP-2003-4GAMER-OGF-REVIVAL-01`]

**RETROSPECTIVE FEATURE BOUNDARY / B-level:** The same report states that during the former Japanese operation, **only GMs could ride dinosaurs**. The project's working JSS/Japanese-original baseline therefore treats normal-player pet riding as **not available**, unless stronger primary JSS evidence later contradicts this. [`SRC-JP-2003-4GAMER-OGF-REVIVAL-01`]

**IMPORTANT LIMIT:** This is a near-contemporary specialist-media retrospective, not a recovered 1999 client/manual/patch note. It constrains feature availability but does not date the GM-only riding implementation to an exact JSS build.

### 2003-09-27 — TGS revival hands-on and original trade-UI boundary

**DIRECT 2003 STAFF COMMENT / A-B level:** When 4Gamer asked on-site staff whether the revival was completely the same as the earlier game, the response was that it was **basically the same**, with restoration/bug fixing being the immediate focus and larger map/character additions planned after open beta. [`SRC-JP-2003-4GAMER-TGS-REVIVAL-01`]

**RETROSPECTIVE FEATURE BOUNDARY / B-level:** The report identifies the dedicated **item trade window as a minor change that the original did not have**, and describes the older exchange context as placing items on the ground. [`SRC-JP-2003-4GAMER-TGS-REVIVAL-01`]

**RESEARCH CONSEQUENCE:** A recovered 2003 Japanese revival client is useful as a near-descendant diff anchor, but later UI additions—especially the dedicated trade window—must not be projected backward into the JSS baseline.


### 2003-12-12 / 2003-12-16 — Japanese revival client version anchor

**FACT / A-level contemporary software metadata:** Mado no Mori records the Japanese revival beta client as **version `1.74a`**, with software date **2003-12-12**, and reports it as downloadable from the official StoneAge site and Hangame. The open beta began on **2003-12-16**. [`SRC-JP-2003-MADONOMORI-174A-01`]

**VERSION-LINEAGE HYPOTHESIS:** The proximity of Japanese `1.74a` to the independently documented Korean `1.74` makes a related version lineage worth testing. It does **not** establish identical binaries, regional data parity, or that `1.74` was the final JSS version.

**RECOVERY TARGET:** Find the Japanese `1.74a` installer or Korean `1.74` client/file tree, hash it outside the repository, and compare executables, resource containers, map/data generations, trade UI and riding-related assets against other preserved branches.

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

## 2003-01 — Mainland 5.0 physical carrier and exact inherited battle-map lineage

FACT / contemporaneous distribution: 17173 published on 2003-01-16 that 石器时代5.0:宠物进化史 was newly on sale and that its starter pack included a 完整版客户端. Sina's StoneAge download hub dated 2003-04-03 independently exposed 石器时代5.0客户端下载. This establishes Mainland 5.0 public client distribution before June 2003. [SRC-CN-2003-17173-STA5-LAUNCH-01] [SRC-CN-2003-SINA-SA-DOWNLOAD-HUB-01]

FACT / preserved byte artifact: IA item Stoneage-5 preserves a one-track MODE1/2352 CD [STA5].bin / CUE object. ISO volume is STA5; byte-derived MSI metadata identifies 石器时代宠物进化史, ProductVersion=5.00.0000, Beijing Waei, and the Waei\stoneage5.0 install tree. [SRC-CN-2003-WAEI-STA5-IA-OPTICAL-01]

FACT / exact lineage: recovered 5.0 battle_2.bin begins with the entire accepted Taiwan v1.0 battle_1.bin byte-for-byte: the first 185,892 bytes have the same SHA-256 d99be6475982cf6098b90ff5dfd81ab275ec8c9271fa83daceb95e3fd4bb8859. 5.0 appends exactly 1,608 bytes, two 804-byte records. Its battletxt_2.txt likewise begins with the complete 5,792-byte v1.0 table and appends battle218.sab and battle219.sab. [SRC-CN-2003-WAEI-STA5-IA-OPTICAL-01]

IMPORTANT LIMIT: this closes a battle-map inheritance chain. It is not evidence that client field-cache DAT/MAP bytes are present on the 5.0 disc; the 413-row MSI File table contains no .DAT or single-layer .MAP field-cache files. The pre-June-2003 field-map provenance target remains open.

### 2003-06-10/23 — full-map package response metadata and mixed-2.5 byte-lineage refinement

**FACT / archived response metadata:** the replayable `map.exe` object observed by Wayback on **2003-06-23 23:44:51 UTC** carries preserved origin response metadata `Last-Modified: Tue, 10 Jun 2003 10:01:06 GMT`, original length **4,223,728 bytes**, and SHA-256 **372426e46765a1cf479041bdafc1d3e58fb019117d00d0b43d6a5f796620776e**. The origin Last-Modified is internal HTTP metadata preserved by the archive; it does not prove identical bytes were present at the same URL before June 10. [SRC-CN-2003-WUXITIANLONG-MAP-PACK-ARCHIVE-01]

**FACT / complete package inventory:** the PE/RAR SFX contains **1,011 DAT files = 1,008 numeric + BGM0/BGM1/BGM2**. Against the separately recovered mixed-2.5 map directory, all 1,011 names coincide: **995 whole files are byte-identical and 16 differ**. The numeric subset remains the previously established **993 exact / 15 different**.

**FACT / layer-level divergence:** among the 15 differing normal DATs, changed-cell totals are **11,500 tile / 678 parts / 4,593 event**. Of the event changes, only **5** alter the low-12 event payload; **4,588** alter high read/see-cache flags. This confirms that a large share of event divergence is runtime-cache state while some genuine static map revisions remain.

**FACT / anomaly controls:** `1021.DAT` (407×144, SHA-256 `92abd0a38c5e876d985c33437a252358d1aaa812ce1da99f18752d0a97c81197`) and `817.dat` (400×600, SHA-256 `ca29cdf04f9f750712ef9afffe14aebfd571a0c6011eac2c7eff67dfde8cc380`) are each byte-identical between the dated historical package and the mixed-2.5 corpus. Consequently their previously observed anomalies cannot be attributed primarily to later mutation inside the mixed bundle.

**LIMIT:** this strengthens the June-2003 field-map anchor and the interpretation of the recovered 2.5 map corpus, but does not move the provenance boundary before June 2003. The 2002-11-08 4.0 map package and earlier installed-cache/physical-media routes remain open.

## 2000-12 — Mainland Sina full-map recovery token

**FACT / surviving download record:** Sina's surviving StoneAge map-download page exposes an exact local-download href for a package identified by `aid=23223`, `filename=samap_1220.zip` and stated size **1410K**. The encoded title parameter decodes to `石器时代！全地图`; the encoded author parameter decodes to `游民部落`. The record is dated **2000-12-20**. [SRC-CN-2000-SINA-FULLMAP-01]

**FACT / archived routing page:** a Wayback replay of Sina's exact download CGI at **2001-01-26 07:46:00 UTC** exposes the direct binary route `http://202.106.184.193/downfiles/map_1212/samap_1220.zip`. The archived HTML labels it `石器时代—全地图下载` and repeats the **1410K** size. This upgrades the target from an exact CGI token to an exact historical delivery URL; it still does not prove that the ZIP body itself survives in a public archive.

**RECOVERY STATUS:** the source page survives and historical page captures are known, but the exact CGI response/payload body is not indexed on the tested Wayback route. Exact Internet Archive filename/stem searches expose no carrier. DiscMaster broad `samap` hits are overwhelmingly unrelated; only an exact leaf-name match to `samap_1220.zip` is now allowed to count as a strict preservation candidate.

**RESEARCH CONSEQUENCE:** this target is earlier than the 2001-11-27 `Estoneage2.0map_1127.exe` package and therefore becomes the first recovery attempt for moving the field-map byte-provenance anchor earlier. If recovered, its archive contents must be hashed and compared directly against Taiwan v1.0, the 2001 package if later recovered, the June-2003 historical corpus, and the mixed-2.5 corpus before any equivalence claim is made.

**EVIDENCE BOUNDARY:** the surviving Sina record proves the distribution token and package label, not the byte identity, cleanliness, operator authorship, or actual map contents of the ZIP.

## 2001-11 — Mainland Sina full-map and 2.0-client recovery tokens

**FACT / 2.0 physical client-disc products:** the surviving 17173 2.0 product page states that both **`石器时代2.0新手报到包`** and **`石器时代2.0老手削暴包`** contain a **《石器时代2.0》客户端光盘**, and dates both product entries to **2001-11-01**. These are therefore two exact physical-carrier classes for recovery of a period 2.0 client disc; the page does not prove that their optical pressings are identical to each other or to Sina's `stoneage2.0setup.exe`. [SRC-CN-2001-17173-SA20-PRODUCT-01]

**PHYSICAL-SURVIVAL CONTROL / 2026-09-25:** the 2016 SMZDM collector page maps its first installation-disc photograph directly after the author's statement that the first purchased package was a **2.0 新手报到包**. The photo body is locked as SHA-256 `98ad75b6eb5fa5aca6fa7e37095bd207779321ea4991ccf0754117cfaf3884c3`. A dedicated R2 cross-check against nine early Mainland Ruten images completed with zero errors. Its two strongest geometrically valid matches both belong to Beijing-Waei/new-user control `22631284715652` (64 RANSAC inliers each; ratios 0.3902 / 0.4324), but they remain below the project's strong-closure threshold. Treat this as coherent visual-family evidence and independent physical survival, not same-disc or byte identity.

**PHYSICAL PHOTO CONTROL / 2026-09-27:** an independent 2016 first-person preservation post directly photographs an author-labelled `石器时代2.0客户端` whose disc face reads `石器时代2.0 家族开拓史`; the author states it was purchased in an **老手削暴包**. The same page also photographs author-labelled early/1.82 and 2.5 client discs. This upgrades physical survival from package-name/index evidence to direct photographed media, but still does not supply optical bytes. [SRC-CN-2016-SHIQIME-MAINLAND-CLIENT-DISCS-01]

**PRESERVATION BOUNDARY / 2.0 retail client discs:** an exact retail-carrier census tested the two source-supported 2.0 package classes, literal client-disc wording and the Sina `stoneage2.0setup` identity across Internet Archive metadata and DiscMaster. The raw R1 pass produced **312 unique IA items but 0 strict candidates**, **0 DiscMaster rows**, plus one truncated broad `老手削暴包` query. A field-limited R2 residual pass closed that exception with **0 unique items, 0 strict items and 0 errors**. Accordingly the tested IA/DiscMaster exact-name surface is bounded without a recovered 2.0 client disc; physical-media survival remains OPEN outside those indexes. [SRC-CN-2001-17173-SA20-PRODUCT-01]

**FACT / 2001-11-02 client record:** Sina's surviving download page identifies `石器时代2.0客户端`, dated **2001-11-02**, with stated size **524377K** and text describing it as an upgraded StoneAge client for existing users. The surviving local-download href resolves to the exact token `col=demo&aid=41967&filename=stoneage2.0setup.exe&size=524377`. [SRC-CN-2001-SINA-SA20-CLIENT-01]

**FACT / 2001-11 carrier-list expansion:** the preserved full text of `《大众软件》2001年11月B（2001年第22期）` independently reproduces the StoneAge 2.0 complete-upgrade distribution context and adds **`《CHIP 新电脑》11月号`**, a carrier omitted from the surviving 17173 version of the list. The same magazine text also corrects an earlier `《晶合秘藏Ⅱ之红宝石》` advertisement by distinguishing the bundled **upgrade version** from a formally activated retail version. Preserve the source discrepancy rather than flattening the lists. [SRC-CN-2001-POPSOFT-SA20-CARRIER-LIST-01]

**RECOVERY STATUS / CHIP carrier:** a dedicated R2 preservation-index pass found **0 relevant Internet Archive items, 0 relevant DiscMaster rows and 0 errors** for the Chinese November-2001 carrier. Foreign Polish/Czech/German CHIP 2001-11 discs and a Chinese `新电脑0508.iso` from 2005 were explicitly classified as non-target controls. The CHIP carrier remains a contemporaneous exact recovery token, not a recovered optical specimen.

**FACT / 2001-11-27 complete-map record:** Sina's surviving page identifies `《石器时代》全地图`, dated **2001-11-27**, size **1911K**, contributed by `xinhaonanhai`. It instructs users to place the unpacked files under the StoneAge directory and explicitly states **“1.X，2.0通用”**. The surviving download href resolves to `col=map&aid=43172&filename=Estoneage2.0map_1127.exe&size=1911`. [SRC-CN-2001-SINA-FULLMAP-01]

**PROVENANCE REFINEMENT / 2026-09-25:** surviving Sina StoneAge community pages show the alias `xinhaonanhai` active on the StoneAge forum surface during 2002 and explicitly call it `斑竹xinhaonanhai` in November event text; Sina's 2002-11-08 `《石器时代4.0》最新地图补丁` also names `游民部落网xinhaonanhai` as contributor. This supports a sustained Sina StoneAge contributor/account-name lineage and reclassifies the 2001 full-map target as a **contemporaneous community-contributed field-map/cache distribution artifact carried by Sina**, not evidence of an operator-original client component. Shared alias/function is a discovery key only; it does not prove personal identity or byte ancestry between the 2001 and 2002 packages. [SRC-CN-2002-SINA-XINHAONANHAI-COMMUNITY-01]

**RECOVERY STATUS:** the exact filenames and CGI identities are recovered, but no verified target payload body has yet been found. For the full-map target, `games.sina.com.cn` exposes 56 archived 2001 `col=map` CGI rows but no exact `aid=43172` row; early-2001 neighbor replays recover `202.106.184.193/downfiles/map_1212/`, and the target filename substituted there has zero CDX rows. For the client target, a `col=demo` neighbor exposes `202.108.44.24/demo_1118/`, but the target installer substituted there likewise has zero CDX rows. These are historical Sina server-topology controls only, not target routes. Therefore both remain precise **TARGET-A recovery tokens**, not byte-provenance anchors.

**RECOVERY REFINEMENT / 2026-09-25:** the same-contributor carrier census found **0 relevant Internet Archive items**, **0 DiscMaster rows**, **0 strict filename rows**, and **0 errors** for `xinhaonanhai`, `Estoneage2.0map_1127[.exe]` and `shiqi4updatex_02_11_08[.zip]`; 25 broad Chinese-query IA rows were unrelated modern metadata noise and were explicitly filtered out. Together with the already-bounded Sina/Wayback, contributor-domain, Common Crawl/Arquivo and exact filename surfaces, the 2001 map package has no current public carrier lead. It remains an exact TARGET-A token and must reopen immediately if a new mirror/cache/carrier path appears.

**RESEARCH CONSEQUENCE:** the 2000-12-20 `samap_1220.zip` record remains chronologically earlier and the 2001-11-27 `Estoneage2.0map_1127.exe` remains the best early field-map token, but both current public recovery surfaces are now bounded without bytes. Operational recovery therefore advances to the **2001-11-02 `stoneage2.0setup.exe` client distribution**, while retaining both map targets for token-triggered reopening. If recovered, its DAT corpus must be compared directly against Taiwan v1.0, the 2000 package if later recovered, June-2003 and mixed-2.5 states before any historical equivalence is asserted.


**LATER COLLECTOR CONTROL / 2026-09-27:** a 2020 physical-media collector post shows four common Mainland 1.82 new-user package variants and states that their backs are identical; a 2021 disc inventory by the same collector describes the familiar Beijing-Waei 1.82 disc as the standard/unified disc across ordinary Mainland package variants, while treating an `上网包` disc separately. This narrows the package/disc-family search surface but does not prove byte identity, first-press identity, or that the collector's four packages are exactly Sina's four January-2001 designs. [`SRC-CN-2020-GAMER-SA182-PACKAGE-COLLECTOR-01`] [`SRC-CN-2021-GAMER-SA182-DISC-COLLECTOR-01`]


### 2000-12 / pre-retail Mainland testing — trial-copy distribution lead

**FACT / preserved contemporaneous-channel mirror:** a preserved copy of a 2001-01-05 China.com / 中华网游戏频道 mail-order notice says that registered users who had participated in the site's earlier `《石器时代》试玩版赠送活动` were entitled to a discounted formal copy. This establishes a pre-retail trial-copy giveaway surface, but the surviving notice does not identify the physical carrier or magazine. [`SRC-CN-2001-CHINADOTCOM-SA-TRIAL-GIVEAWAY-MIRROR-01`]

**OPEN / later first-person collector lead:** a 2020 StoneAge physical-media collector states that a Mainland 1.0 test item in his collection was a **test manual with a disc, distributed as a magazine insert and without a retail box**. The claim is high-value because it could identify an earlier Mainland client carrier, but it is not authenticated by a contemporaneous magazine record or public disc/manual photographs yet. [`SRC-CN-2020-GAMER-MAINLAND-SA10-TEST-CARRIER-LEAD-01`]

### 2001-03 — Mainland first/second manual-print split

**FACT / preserved official-announcement transcription:** Beijing Waei's 2001-03-12 apology states that a manual editing error caused a 50-hour dispute, that **second-batch newly printed manuals would be corrected**, and that **first-batch manuals would only be corrected by the website erratum**. Pre-deadline registrants were granted an additional 300 points, explicitly equated to 50 hours. [`SRC-CN-2001-WAEI-SA-MANUAL-ERRATA-MIRROR-01`]

**INDEPENDENT CORRECTED-STANDARD CONTROL:** 17173's surviving StoneAge 1.0 charging page records the corrected registration benefit as **300 points / 50 hours**. [`SRC-CN-2001-17173-SA10-CHARGING-01`]

**HYPOTHESIS / later player recollection:** a 2003 17173 player retrospective says the previously stated **600 points** became **300 points** when charging began. Combined with the official 50-hour errata dispute, this makes `first-print manual = 600 points / 100 hours` a strong working hypothesis, **not FACT** until a first-print page or contemporaneous quotation is recovered. [`SRC-CN-2003-17173-SA-600-TO-300-RECOLLECTION-01`]

**CONFLICT CONTROL:** contemporaneous Sina launch coverage says the four Mainland packages came with **45 hours** of free time. Do not silently equate that launch-promotion number with either the corrected 300-point/50-hour registration standard or the hypothesized first-print 600-point/100-hour statement. [`SRC-CN-2001-SINA-STONEAGE-MAINLAND-LAUNCH-01`]


### 2000-12-15 to 2001-01-10 — Mainland official test CD

**FACT / surviving contemporaneous portal page:** China.com's still-live legacy StoneAge activity page is titled **`石器时代游戏测试光盘免费大赠送`** and explicitly distributes a physical test disc. Outside Beijing, participants supplied an address after completing a questionnaire and received the disc free while supplies lasted; Beijing participants were directed to **晶合软件销售点**. The activity closed **2000-12-31**, while the page explicitly brackets the official test period as **2000-12-15 through 2001-01-10**. [`SRC-CN-2000-CHINADOTCOM-SA-TEST-CD-GIVEAWAY-01`]

**INDEPENDENT CHANNEL CORROBORATION:** a surviving 晶合时代 profile states that the company organized the **free distribution of the StoneAge test-version software**, consistent with China.com's Beijing pickup instruction. [`SRC-CN-EARLY-JINGHE-SA-TEST-DISTRIBUTION-01`]

**RECOVERY CONSEQUENCE:** a surviving authenticated copy of this test CD would predate the January-2001 formal retail carrier and is now the highest-priority Mainland physical-client target. Its relationship to Taiwan v1.0, the January retail disc and later 1.82-labelled media must be established by bytes, not version-label assumptions.

**OPEN / separate carrier possibility:** a 2020 collector says a Mainland 1.0 test manual+disc existed as a magazine insert. No direct evidence currently binds that specimen to the China.com/Jinghe giveaway, and no exact magazine issue has been resolved. Do not merge the two carrier routes yet. [`SRC-CN-2020-GAMER-MAINLAND-SA10-TEST-CARRIER-LEAD-01`]

### 2001-01-12 — formal Mainland retail carrier control

**FACT / surviving China.com legacy product page:** the formal product information identifies **载体：1 CD-ROM**, release date **2001-01-12**, price RMB 29, Simplified Chinese, and the JSS / Beijing-Waei / Zhiguan / Guangxi-Jinhaiwan chain. This gives a direct physical-media control immediately after the official test period. [`SRC-CN-2001-CHINADOTCOM-SA-LEGACY-PRODUCT-01`]

**SOURCE-SURVIVAL CORRECTION:** China.com's legacy StoneAge news pages remain live under `game.china.com/hotspot/shiqi/`. They directly preserve the Jan-2001 trial-participant/mail-order notices and the Mar-2001 charging/manual-errata announcements previously known to the project mainly through later mirrors. [`SRC-CN-2001-CHINADOTCOM-SA-LEGACY-NEWS-ARCHIVE-01`]


**PRESERVATION STATUS / 2026-09-27:** a source-derived metadata probe over ten China.com/Jinghe/test-CD identities found **0 strict Internet Archive items**. DiscMaster returned **0 strict Chinese-identity hits**; a targeted R2 then completed both filename and full-text search for the five initially timed-out English identities with **0 strict hits / 0 errors**. This direct preservation-index route is therefore BOUNDED until a new exact artifact token is recovered.

**LATER FIRST-PERSON COPY-PROVENANCE CONTROL:** a 2002 17173 retrospective by an early Mainland player recalls starting during the test-version Christmas period using a **disc burned by a friend**. This is consistent with rapid informal replication of the client during testing, but it does not identify the official giveaway pressing or its bytes. It establishes a future authentication hazard: test-period content may survive on player-burned media even when original China.com/Jinghe carriers do not. [`SRC-CN-2002-17173-SA-TEST-CD-BURNED-COPY-RECOLLECTION-01`]


**ARCHIVED GIVEAWAY-RESULT CONTROL / recovered 2026-09-27:** the test-CD activity page's linked article `63271` survives in Wayback with eight HTTP-200 captures. The earliest replayable capture (2001-03-09) is a giveaway-results/recipient-list page whose page-level text includes `石器时代`, `赠送`, `名单`, and `光盘`. Participant identities/contact data are deliberately excluded from the project record. The page exposes no test-CD-specific filename or optical identifier. [`SRC-CN-2000-CHINADOTCOM-SA-GIVEAWAY-RESULT-ARCHIVE-01`]

**ASSET-SURFACE BOUNDARY:** eleven first-party image/background paths are present in the earliest archived result page. Nine replayable assets are generic China.com logos/navigation/UI images and there are zero large/page-specific image candidates; the two unreplayed paths are generic UI names. The current archived result-page asset route therefore provides no StoneAge-specific physical-media token.

**MAGAZINE-CANDIDATE CORRECTION:** because Jinghe had close ties to `《大众软件》`, the preserved Popsoft scan family was tested across 2000-11, 2000-12 and 2001-01 A/B issues. Only one editorial `Stone Age` mention appears (2000-12A), with no nearby test/disc/Jinghe/Waei/giveaway context and no optical files in the scan item. This does not disprove a separate magazine-insert carrier, but it **downgrades Popsoft as the leading candidate** absent a new exact issue/disc token. [`SRC-CN-IA-POPSOFT-2000-LAUNCH-WINDOW-01`]


### 2001-01-04 — Waei homepage trial-download recollection

**NEAR-PERIOD FIRST-PERSON EVIDENCE:** a 17173 player diary published on 2001-06-13 explicitly dates an entry to **2001-01-04** and recalls seeing a `石器时代试玩版` on the Waei homepage. The author's download manager reported a size of **“274多兆”** before the download was abandoned because of dial-up telephone cost. This supports an official-homepage online trial distribution surface, but it does not preserve a filename, exact byte count or download URL. [`SRC-CN-2001-17173-WAEI-TRIAL-DOWNLOAD-RECOLLECTION-01`]

**BOUNDARY:** do not equate this online trial payload automatically with the China.com/Jinghe physical test CD, the collector-described magazine-insert test disc, or the January-2001 formal retail CD. They are separate candidate carriers until bytes prove identity.

### 2001-06-05 — Waei.net StoneAge sprite-resource byte anchor

**FACT / archived bytes:** Wayback preserves `spr_1.bin` under Waei.net's Big5 `修補程式` download directory at capture timestamp **2001-06-05 17:45:50 UTC**. Transient recovery produces a **2,889,630-byte** binary with SHA-256 `864fa3f6aaeb7d8d2dc9bdee46cecdc7dcee1af0c8f1ed949e09c0526e6aa17e`; its SHA-1-derived Base32 digest exactly matches the Wayback CDX record. [`SRC-WAEI-2001-SPR1-ARCHIVE-01`]

**FACT / StoneAge resource-lineage closure:** the archived file has exactly the same size as the accepted Taiwan v1.0 `spr_1.bin` and parses perfectly using Taiwan v1.0's `spradrn_1.bin`: **464 groups, 39,065 animations and 242,085 frames** with all group spans closing. Only **16 bytes** differ, all within `spr_no=100102`. [`SRC-WAEI-2001-SPR1-ARCHIVE-01`]

**FACT / semantic delta:** four Taiwan-v1 sentinel bitmap references (`0xFFFFFFFF`) become bitmap IDs **126235–126238** in animations 82–84. Those four bitmap IDs are absent from the accepted Taiwan v1.0 `adrn_1.bin`.

**HYPOTHESIS / companion-resource implication:** the four newly referenced bitmap IDs strongly imply a corresponding later image-resource addition in an `ADRN/REAL` lineage, but same-directory exact archive probes currently expose no `adrn_1.bin`, `real_1.bin` or `spradrn_1.bin` companion. Do not invent those missing bytes.

**REGIONAL LIMIT:** this is a Waei.net / Big5-hosted artifact. It must not be relabelled as an authenticated Mainland retail/test build without an explicit regional/version binding.


**PATCH-TITLE / ROUTE CLOSURE — 2026-09-27:** archived Waei central-download HTML directly identifies fileid **133** as `石器隱形人無所遁形修正檔` (display date **2001/4/26**, **2,822 KB**) and instructs users to overwrite a file in `C:\\Program Files\\Waei\\石器時代\\data`. Wayback preserves `download.asp?fileid=133` at **2001-06-05 17:42:13 UTC**; its historical 302 `Location` directly targets the archived `修補程式/spr_1.bin` URL captured at 17:45:50. The transiently recovered 2,889,630-byte payload is 2,821.904 KiB, matching the catalogue's rounded size. This upgrades the artifact from resource-lineage inference to **direct official Waei StoneAge patch provenance**. Exact client-version/region binding remains OPEN. [`SRC-WAEI-2001-SPR1-ARCHIVE-01`]

**JINGHE/YEGAME RETAIL-CATALOG BINDING — 2001-04-06 archive evidence:** the source chain `www.jhpop.com` (archived 2000-12-04) -> `www.yegame.com` leads to the historical 晶合 commerce catalog. A recovered Yegame network-game category page captured **2001-04-06** lists **石器时代** with exact product code **`EN0ZGKJ0002`**, medium **`1-CD`**, catalog field **更新日期 2001-1-16**, retail **¥29.00**, and wholesale **¥26.00**. It also exposes **石器时代-WGS620点会员卡** as product **`EZ0JHSD0003`**. Treat `2001-1-16` strictly as the catalog's update field, not as an independently established release date. The 1-CD carrier independently coheres with China.com's formal-product `载体：1 CD-ROM` record, but this does not identify the Dec-2000 test-CD carrier or recover client bytes. [`SRC-CN-2001-YEGAME-SA-PRODUCT-CATALOG-01`]

**JINGHE/YEGAME PRODUCT DETAIL — archived 2001 captures:** exact product key **`EN0ZGKJ0002`** has three preserved HTTP-200 detail-page captures (2001-04-15, 2001-07-17, 2001-08-16). The replayable 2001-08-16 page directly identifies **石器时代**, **1-CD**, retail **¥29**, preferential price **¥26**, and states that the game included **45 hours** of free time with a January–February 2001 holiday free-play promotion. Its gameplay copy mentions capturable/growing pets, **more than 100 creatures**, **12 character designs x 4 colors**, and **12 expressive actions**. The page references cover/product image `/product_images/EN0ZGKJ0002.jpg`; preservation of that image remains OPEN after a transient archive-query failure. Separate exact key **`EZ0JHSD0003`** is directly bound to the StoneAge **WGS 620-point membership card**, medium `单卡`. These are commerce/catalog facts, not client-byte or test-CD identity. [`SRC-CN-2001-YEGAME-SA-PRODUCT-DETAIL-01`]

**WAEI FIRST-PARTY RUNTIME GENERATION CHAIN — 2001:**
the archived first-party `stoneage.waei.net/saupdate/` surface now yields byte-recoverable `sa_40.exe` and `sa_42.exe`. `sa_40` is 528,384 bytes (SHA-256 `d54a6c109644dd4842f61bdd42a95362fda7a16f5e9b9dbd829d6b97c678fde1`) with PE timestamp 2001-09-27; `sa_42` is 557,056 bytes (SHA-256 `744fc0557f024930f351ef31b6adac0dbe41968625105d5f0eba45be1a048df6`) with PE timestamp 2001-11-01. Both self-identify as Waei `SaDeb.exe` runtimes and preserve the launcher-child `updated` architecture already seen in Taiwan v1.0. Waei's 2003 public prospectus dates marketing releases 2.0=2001-08-01, 2.5=2001-11-01, 3.0=2002-03-01, 4.0=2002-07-01, proving that suffixes `40/42` are not marketing 4.0/4.2 identifiers. A later community chronology's explicit 2001-04-24 `SA_24` update naming supports an internal update-generation interpretation. `sa_42` is a strong temporal 2.5-era runtime anchor, but exact launch-build identity remains open. Exact first-party probes find no usable `sa_3/23/24/25/41` payloads; only `sa_40/42` survive as HTTP-200 binaries. [SRC-TW-2001-WAEI-SAUPDATE-RUNTIME-BYTES-01; SRC-TW-2003-WAYI-PROSPECTUS-PRODUCT-CHRONOLOGY-01; SRC-TW-COMMUNITY-SA24-CHRONOLOGY-01]


**2026-10-04 technical evidence boundary — AttackCrazed:** three pinned later
descendant profiles and the hash-verified recovered25 preservation bundle
converge on the valid three-hit OPTION domain for recovered data ID 613.
The later source's candidate loop omits side slots 9/19; its first non-bow hit
uses the submitted target, while subsequent hits use later preselected list
entries. Same-side/pointer handling varies by source profile. This audit does
**not** date the skill's introduction or prove Taiwan-v1 membership, and source
macro 608/compiled command 2010 are not a recovered-binary command mapping.
[SRC-DESCENDANT-ATTACKCRAZED-PINNED-PROFILES-R1]


**2026-10-04 technical evidence boundary — Mdfyattack:** the three pinned later descendant profiles separately register Mdfyattack and Modifyattack. Mdfyattack replaces the temporary attacker attribute vector with one selected EA/WA/FI/WI weight and zero neutral weight before property/field calculations. Compiled symbolic command values differ (gavin/iris 2030 vs Bismarck 2028), so none is a recovered25 binary mapping. The safe reference/data audit neither dates this skill's introduction nor establishes Taiwan-v1 membership. [SRC-DESCENDANT-MDFYATTACK-PINNED-PROFILES-R1]


**2026-10-04 technical evidence boundary — Weaken:** pinned later descendants
converge on command-only callback setup, shared status application with turn+1
and self/mutual status-counter freeze. This is not direct attack/defense reduction.
Compiled command values differ (2022 vs 2021); source macro 544 is not recovered
data ID 575/576. No introduction date or Taiwan-v1 membership follows from this
technical audit. [SRC-DESCENDANT-WEAKEN-PINNED-PROFILES-R1]


**2026-10-04 Weaken power-seam clarification:** the preceding observation of no
direct callback/application attack/defense reduction does not mean the status
has no power effect. At explicit character compliance recalculation, later
source reduces freshly rebuilt fixed strength/toughness/dexterity by 20% and
decrements the status counter. The caller schedule must be evidenced separately
from StatusSeq's freeze loop. [SRC-DESCENDANT-WEAKEN-PINNED-PROFILES-R1]


**2026-10-04 Weaken caller-schedule closure:** later pinned battle initialization
and completed battle-command processing invoke BATTLE_PreCommandSeq, which
performs compliance before turn modifiers for valid non-EARTHROUND0 entries.
This resolves the preceding normal battle caller schedule OPEN; it does not
supply Taiwan-v1 membership, an introduction date or recovered binary enum.
The verified recovered25 preservation data separately binds IDs 575/576 to
status 7 / turn 3 / success 50 with differing target/illegal metadata.
[SRC-DESCENDANT-WEAKEN-PINNED-PROFILES-R1]


**2026-10-04 Weaken runtime evidence boundary:** the rebuilt recovered25 path
now composes separate command-only application, base/WEAKEN/BARRIER/NOCAST
visits and normal post-round preparation. The latter rebuilds baseline powers,
reduces fixed strength/toughness/dexterity and decrements positive WEAKEN/BARRIER.
This supersedes an indefinite Barrier duration inferred from StatusSeq alone;
it does not date skill introduction, establish Taiwan-v1 membership or map a
recovered binary enum. [SRC-DESCENDANT-WEAKEN-PINNED-PROFILES-R1]


## 2026-10-04 — WildViolentAttack descendant reference (conditional charset)

**FACT / LATER_RECOVERED:** Three freshly pinned descendants expose callback work-power/HIGH setup and action-time random 3–10 physical hits, a float damage divisor, original-target reset and additive defender dodge. Compiled command 2018/2018/2017 and source macro 540 are profile facts, not recovered data ID 541 or binary identifiers. Actual-source UTF-8 vs explicit CP950 builds diverge at fixed byte offsets; negative/>32767 HIGH packing is signed-shift UB. Native reference and derived probe/spec are reproducible without committing original source. **OPEN:** original execution charset, full real callback metadata/OPTION population, safe ordered runtime and Taiwan-v1 membership. Source comments dated 2002/05/16 are not independently verified introduction dates. See `specs/STONEAGE-WILDVIOLENT-REFERENCE-R1.md`.


### 2026-10-04 — WildViolentAttack full recovered callback population

**FACT / LATER_RECOVERED:** Verified preservation run 37192280455 enumerates two exact callback rows, IDs 541 and 652. Only 541 has positive enemy references (7 uses / 7 templates). Both metadata rows are FIELD 1 / TARGET 6 / COST 2 / ILLEGAL 1000. Their 20-byte OPTION strings converge under strict CP950/Big5 decoding and have defined positive HIGH modifiers 30 / 50; UTF-8 execution differs. No raw rows are stored. **OPEN:** original compiler execution charset, ordered runtime and historical Taiwan-v1 membership. This supersedes earlier unknown full callback population, without promoting a conditional build to original provenance.


### 2026-10-04 — WildViolentAttack conditional source/data accepted

**FACT / LATER_RECOVERED:** Hardened source/data Actions 37192609926 and 37192610005 PASS at `e460037c0214fa795efa8c1e041a8a676eb0bb0b`, derived report `ae9bfa7a4596925e49d82731e1528e7a830cf6cb`. Full population and hashes reproduce; 60 actual recovered-byte callback witnesses match the own reference across three sources and UTF-8/CP950 builds with UBSan. **CLOSED:** explicit conditional charset safe source reference and CP950/Big5 data/defined-shift domain. **OPEN:** original build charset, ordered executable runtime and Taiwan-v1 membership. Seven slot uses remain outside accepted executable coverage, which stays 2415/2486.


### 2026-10-04 — WildViolentAttack conditional runtime evidence boundary

**LATER_RECOVERED:** Typed recovered25 enemy execution and two-round persistence now pass independent/remote acceptance, including exact data/hash gates, all seven authoritative slot selections and corrected compliance-prepared fixed-power use alongside Weaken. This admits an explicit CP950 descendant-reference domain; it neither resolves the original binary execution charset nor dates the skill's introduction or proves Taiwan-v1 membership. See `specs/STONEAGE-WILDVIOLENT-RUNTIME-R1.md`.


## 2026-10-04 — Refresh bounded descendant audit

**FACT / LATER_RECOVERED:** Three fixed descendant source profiles expose a command-only Refresh callback and shared highest-positive-status recovery. Executor success/receive effect depend on the actor, while recovery acts on targets. Wildcard compares a battle status index with the CONFUSION work enum, clearing one highest state including extensions rather than all states. Two tables have 32 labels while scanning to END44; unmatched scans and NULL OPTION are unsafe. Source commands2032/2032/2030 and skill macro575 are profile facts, not recovered data IDs583/592 or binary enums. 9083 transient defined native witnesses and expected sanitizer diagnostics support the bounded reference. **OPEN:** whole recovered callback population/real-byte outcomes until remote verification, original compiler charset, ordered runtime and Taiwan-v1 membership. The source's 2002/08/08 comment is not independently verified introduction evidence. See SRC-DESCENDANT-REFRESH-PINNED-PROFILES-R1 and the R1 reference spec.


## 2026-10-04 — Refresh source/data acceptance boundary

**FACT / LATER_RECOVERED:** dedicated reference Action 37211584308 and preservation-bundle/full-family Action 37211584354 both PASS at `ad4b2e0f2e92594eb71cea63b8a5d330ac45254e`; derived report `fc7dfbdb00ca900716e6799794929bd8ef7a74ad` enumerates exact callback IDs 583/584/591/592/593. Positive recovered25 uses are only ID 583 (4) and ID 592 (2). Conditional iris CP950/Big5 parsing yields status indices 10/8/9/0/7, so the two live rows correspond to silence and the source wildcard branch only inside that conditional descendant-reference domain. **CLOSED:** bounded source reference, exact population, metadata/hash evidence and conditional actual-byte reference. **OPEN:** original recovered compiler charset, live target-list/retarget ordering, executable runtime and historical Taiwan-v1 membership. Coverage remains 2422/2486 until ordered runtime acceptance.


## 2026-10-04 — Refresh ordered runtime accepted and pressure advanced

**LATER_RECOVERED / CONDITIONAL EXECUTION:** typed Refresh execution now passes dedicated runtime, persistent coordinator, golden and full recovered region/resource/collision validation. IDs 583/592 account for six positively referenced recovered25 uses; exact full callback population remains 583/584/591/592/593. Runtime retains the iris CP950 descendant-reference boundary and does not identify the original compiler charset or historical numeric COM1. Silence restoration and wildcard single-highest clear persist across rounds; dead-single retarget RNG is explicit and otherwise absent. Verified pressure **37213544358 PASS** marks Refresh CLOSED_RUNTIME and advances accounted executable slot uses to **2428/2486 (97.67%)**. The next mechanically selected OPEN family is **PETSKILL_SetMagicPet**, ID 601, six uses/six templates. Historical Taiwan-v1 membership and original introduction remain OPEN.


## 2026-10-04 — SetMagicPet source/data boundary accepted

**FACT / LATER_RECOVERED:** fixed-source and verified recovered25 gates close the SetMagicPet family at rows 601–604; only ID 601 is positively referenced (6 uses/6 templates). Source commands compile as 2035/2035/2033 while the later source skill symbol itself is 601 in all three profiles; this numerical match does not prove original-binary identity or Taiwan-v1 introduction. The callback's documented three-use limiter is inert in the pinned descendants because its count is never incremented. STR/TGH/DEX temporary buffs are mutually exclusive and all three recalculate from the same pre-suit toughness basis. **37215723983 PASS / 37215724000 PASS.** Exact recovered metadata/hashes and turn/amount/kind parsing are closed; ordered runtime remains OPEN and accepted executable slot coverage stays 2428/2486.


## 2026-10-05 — SetMagicPet bounded ID-601 runtime accepted, pressure verification pending

**LATER_RECOVERED / EXECUTION:** exact recovered25 ID 601 now has a typed enemy runtime preserving source MultiList retarget ownership, mutual SetDuck/STR/TGH/DEX exclusion, action-ordered counter decrement, non-compounding TGH +15% preparation from baseline toughness, and SetMagicPet-before-Weaken preparation order. Code-level dedicated/coordinator/full-stack regressions pass at `234cfb200ccff06bd97cb29009f81c7406e8f373`; expiry/order supplement **37217473190 PASS**. Rows 602–604 remain data-only. Numeric historical COM1, original binary identity and Taiwan-v1 membership remain OPEN. Pressure reclassification source is committed but hash-verified Action **37217793085 remains queued**, so the old 2428/2486 report remains canonical until regenerated.


## 2026-10-05 — SetMagicPet verified pressure closure and BattleTimid handoff

**LATER_RECOVERED / EXECUTION:** hash-verified pressure Action **37218864011 PASS** after two fixture-only ranking-test corrections. Derived report `ec46a0248e6c64623096d03c14e5ffc156a1193c` reproduces **2486 positive recovered25 enemy skill-slot uses / 0 unresolved IDs**, marks exact SetMagicPet ID 601 **closed_runtime** for six uses/six templates, and advances accepted executable coverage to **2434/2486 (97.91%)**. The next mechanically selected OPEN family is **PETSKILL_BattleTimid**, recovered ID 606, five uses/five templates. Existing BattleTimid observations remain pre-audit only; original introduction, Taiwan-v1 membership and original binary/compiler identity remain OPEN.


## 2026-10-05 — BattleTimid bounded reference closed

**LATER_RECOVERED / REFERENCE:** Action **37220370536 PASS** reproduces three pinned descendant source profiles and the hash-verified recovered25 bundle. The shared bounded reference is enemy/non-player setup with 70% STR / 40% TOUGH / 80% DEX work powers, TargetAdjust → AttackDamage dispatch, one raw `rand()%100` draw, and forced exit only for `draw < 15 && damage > 1`. Pet and non-pet forced exits have distinct persistent consequences. Recovered25 population is exactly ID 606 with five positive uses/five templates and exact row `1/6/2/3000` plus an empty OPTION. Same-side compile gating and OPTION-pointer guarding differ across the pinned descendants and remain explicit boundaries. Original JSS/Taiwan-v1 membership, original compiler/binary identity and historical numeric COM1 remain OPEN.


## 2026-10-05 — Combined bounded source/data reference closed

**LATER_RECOVERED / REFERENCE:** corrected hash-verified Action **37262695753 PASS** establishes the full `PETSKILL_Combined` recovered25 family as seven rows **627/629/630/632/637/646/648**, while only **627/632/637** carry the five positive enemybase references across five templates. Exact-pin Action **37262850204 PASS** and derived report commit `8252a51966450a0b5b515d051e52b3c84d61ae65` close all seven exact metadata/OPTION-hash rows against full `petskill` SHA-256 `f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4`. The three pinned descendants agree on max-10 OPTION parsing, one raw `rand()%count` selection, command 2000, LOW(COM3) selected magic, HIGH(COM3)=0 and `MAGIC_DirectUse` dispatch, but retain real OPTION-guard/count-initialization and initiative-RNG profile differences. Malformed OPTION behavior, original binary/compiler identity, original JSS/Taiwan-v1 membership and ordered runtime remain OPEN.


## 2026-10-05 — Combined direct magic consumes live item-pool MP

**FACT / LATER_RECOVERED:** The three fixed descendant profiles agree that Combined's zero HIGH(COM3) becomes non-player DirectUse runtime item index 0, whose ITEM_MAGICUSEMP is used by the four positively selected ordinary wrappers. A witnessed invalid item returns -1 and can increase caster MP by 1; an unknown item-pool state is not evidence of a free cast. 4800 transient native accessor/DirectUse/wrapper witnesses pass locally with stubbed effect helpers. Selection RNG is owned by the preceding callback, before Nocast. **OPEN:** remote reproduction, live item-pool provenance, actual-byte status parsers, effect mutation, ordered persistence and Taiwan-v1 membership. See `specs/STONEAGE-COMBINED-DIRECT-MAGIC-BOUNDARY-R1.md`.


### 2026-10-05 — Combined direct-wrapper evidence remotely reproduced

**FACT / LATER_RECOVERED:** At `97fb9e5ca78a007f383024b7edc935fd997077e0`, native boundary Action **37265053597 PASS** reproduces all 4800 witnesses and source/report hashes; verified bundle Action **37265053470 PASS** checks all 19 crosslinks and the eight positively selected magic choices with explicit item-state boundaries. This supersedes the previous entry's pending remote-verification status only. Live item-pool provenance, status parsers, effect mutation/persistence and original Taiwan-v1 membership remain **OPEN**.


## 2026-10-05 — Combined actual status-magic parser results remain conditional

**FACT / LATER_RECOVERED:** Verified source/data Actions **37266411923 / 37266742566 PASS** establish 42 explicit parser outcomes for magic 61/139/159/169/179/189. iris CP950 safely yields recovery wildcard 0 and status 1/4/6/5/3 with duration 5 and success input offset 15. gavin UTF-8/GBK and iris UTF-8/GBK overrun their short status-label tables; Bismarck UTF-8/GBK safely reject all six. All 42 classifications/values are independently pinned and native-compared without publishing raw parameters or source. **CLOSED:** conditional byte-parser reference. **OPEN:** original execution charset, target/effect mutation, live-item MP provenance, ordered persistence and Taiwan-v1 membership. No introduction date or whole-project completion is inferred.

## 2026-10-05 — Vary bounded reference and ordered runtime accepted

**LATER_RECOVERED / REFERENCE + EXECUTION:** verified recovered25 data closes `PETSKILL_Vary` to exact ID **600**, four PETSKILL3 uses on TEMPNO 981/982/983/984, with TARGET_NONE and the pinned 22-byte OPTION hash. Three fixed descendant pins agree on wolf image 101428, WORKTURN lifecycle and recast block but differ materially: gavin/iris modify attack+quick and own the visual-effect path; fixed Bismarck also modifies defense and has that visual body compiled out. Verified executable discriminator **37282101502 PASS** cannot choose between them because no Vary symbol carrier is present, so runtime preserves both as explicit conditional profiles. Ordered/persistent/coordinator/full-region/pressure acceptance is green (**37286463853 / 37286420982 / 37286420991 / 37286756850 PASS**). Pressure advances accepted executable slot coverage to **2448/2486 (98.47%)** and mechanically selects **ENEMYSKILL_ReLife / ID500 / 3 uses / 3 templates** next. Original JSS/Taiwan-v1 membership, original executable profile and numeric Vary COM1 remain **OPEN**.

## 2026-10-05 — ReLife bounded source/data reference accepted

**LATER_RECOVERED / REFERENCE:** verified preservation-bundle and three-pin descendant evidence close `ENEMYSKILL_ReLife` to exact recovered25 ID **500**, FIELD1 / TARGET2 / COST2 / ILLEGAL0, empty OPTION, with three positive uses on TEMPNO 39/909/1165. TARGET2 is `PETSKILL_TARGET_ALLMYSIDE`, but enemy-caster resurrection selection is independently owned by the effect helper: it scans non-ultimate actionable dead enemy slots 10..19, consumes one candidate-selection RNG, revives from a WORKMAXHP/2 base with the common 90–110% resurrection variance, caps HP and clears ISDIE. No candidate returns FALSE and the dispatcher falls back to ordinary ATTACK after its prior TargetAdjust. Guarded command values diverge **2013 gavin/iris vs 2012 Bismarck** and remain symbolic only. Actions **37288674220 / 37288913119 PASS**. Original executable profile, numeric COM1 and JSS/Taiwan-v1 membership remain **OPEN**.

## 2026-10-05 — ReLife ordered runtime and pressure closure

**LATER_RECOVERED / RUNTIME:** the bounded recovered25 enemy ReLife path is now executable without assigning an original numeric command. Exact ID500 admission remains three positive template/slot identities. Runtime preserves TargetAdjust-before-effect, enemy dead-slot 10..19 selection, explicit candidate and recovery RNG ownership, same adjusted-target physical fallback, and retained dead-entry semantics across same-round and later-round resurrection. A late regression correction constrains retained ReLife candidates to enemy-side entries only; player-side pet death remains in the previously accepted loyalty/death lifecycle. Dedicated/runtime/core/coordinator/golden/full-region gates are green, and verified pressure **37293804945 PASS** marks ReLife closed. Accepted executable positive-slot coverage is **2451/2486 = 98.59%**. The verified ranking selects **PETSKILL_Lighttakeed / IDs610,611 / 3 uses / 2 templates** next. Original binary/compiler identity, numeric ReLife COM1 and JSS/Taiwan-v1 membership remain **OPEN**.



## 2026-10-05 — PETSKILL_Lighttakeed bounded reference closure

- ReLife runtime pressure selected **PETSKILL_Lighttakeed / positive IDs 610,611 / 3 uses / 2 templates** as the next OPEN family. The fresh reference probe then established that the complete callback population is actually **609/610/611**; ID 609 is a zero-positive-reference row and therefore was correctly absent from pressure ranking.
- Hash-verified recovered25 exact data: all three rows FIELD/TARGET/COST/ILLEGAL **1/7/2/5000**, six-byte non-NUL OPTIONs. Derived marker identity is **609 ABSROB**, **610 REFLEC**, **611 VANISH**. Exact positive placements are TEMPNO **70** graphic **101550** slot4 -> 610 and TEMPNO **157** graphic **101283** slots4,5 -> 610/611.
- Fixed gavin/iris/Bismarck source audit closes the common callback/dispatch seam: symbolic Lighttake command, target + C_OK, temporary attack **70%** and defence **50%**, LOW(COM3) skill carrier, no callback-local OPTION/RNG, TargetAdjust before AttackDamage, and marker-specific neutralization of a matching active damage reaction.
- All three fixed descendants compile numeric command **2009**, but that agreement is not promoted to recovered-original COM1. A stronger semantic divergence remains: gavin/iris assign the matching defender work counter unchanged to the attacker; fixed Bismarck assigns that observed value **+1**.
- Exact source/data workflow **37295790110 attempt 2 PASS**; derived reports committed at `0d002434a5b86e20505ff8b8fd431b3075374c84`. Reference: `specs/STONEAGE-LIGHTTAKEED-REFERENCE-R1.md`.
- **LIGHTTAKEED_REFERENCE_R1 = CLOSED_BOUNDED_RECOVERED25_REFERENCE.** Ordered runtime remains OPEN. Before runtime coding, attempt a bounded recovered-executable/profile discriminator for **copy vs copy+1**; if inconclusive, preserve explicit conditional profiles. Pressure stays **2451/2486 = 98.59%**.


## 2026-10-05 — Lighttakeed ordered runtime accepted

**LATER_RECOVERED / RUNTIME:** recovered25 positive Lighttakeed IDs610/611 (three slot uses/two templates) now close ordered battle, persistence and coordinator admission. Explicit copy/copy+1 profiles remain because the preserved executable cannot discriminate them. The fixed lifecycle audit proves DamageSub consumption and non-throwing REFLEC's post-branch redirection to the attacker; the counter-copy description cannot be read as unconditional defender copying. Cross-round witnesses prove charge exhaustion and retained base attributes. Full-region **37299249771**, coordinator **37299249647**, golden **37299249686**, dedicated **37299772670** and verified pressure **37299752243 PASS**. Local final regression **258 tests PASS**. Pressure report `26afc10ee71572d09fffce2413ff13dc6c590e72` advances executable slot coverage to **2454/2486 = 98.71%** and selects **PETSKILL_Modifyattack / IDs544/545/546 / 3 uses / 3 templates** next. Original binary/profile/numeric COM1 and JSS/Taiwan-v1 membership remain **OPEN**. See `specs/STONEAGE-LIGHTTAKEED-RUNTIME-R1.md`.


## 2026-10-05 — Modifyattack complete data and bounded native reference accepted

**LATER_RECOVERED / REFERENCE:** verified recovered25 complete callback population is544/545/546/547, with ID547 unreferenced and three positive uses on TEMPNO18/19/20. All exact rows use FIELD1/TARGET6/COST2/ILLEGAL2000 and five-byte ASCII OPTIONs deriving earth/water/fire/wind plus20%. Three fixed descendants agree on a post-AttackSeq/pre-DamageSub helper, reaction demotion and one matching-positive-attribute rand draw, including the integer remainder/100 step that must not be rewritten as a fractional percentage. Guarded numeric COM1 differs2029 versus2027 and remains unselected. Exact data/native Action37302178741 PASS; report write-back a696cb5f98812600d7a1c898bf400ebe8dc21909. Native reference covers60 callback/7980 helper cases and all four actual parameters at all three pins;32 related tests PASS. Ordered runtime, original binary/PRNG and JSS/Taiwan-v1 membership remain **OPEN**. Executable pressure remains2454/2486=98.71%. See `specs/STONEAGE-MODIFYATTACK-REFERENCE-R1.md`.


## 2026-10-05 — Modifyattack bounded ordered runtime and pressure accepted

**LATER_RECOVERED / RUNTIME:** recovered25 positive Modifyattack IDs544/545/546 close exact typed admission, ordered damage, persistent state and enemy-AI coordinator execution for three uses/three templates. ID547 remains data-only. The runtime preserves the native post-AttackSeq/pre-DamageSub helper, raw original-defender attribute lookup, integer random-remainder division, explicit one-draw ownership, reaction demotion and specialized Guardian settlement. ATTDOUBLE does not add a second strike, and modern ATTACK-shaped scheduling does not grant ordinary counter/combo eligibility. Cross-round tests prove no retained semantic effect or work-power mutation. Dedicated **37305538911**, battle core **37305538909**, coordinator **37305538741**, golden **37305538906**, full-region **37305538863 PASS**; all29 relevant workflows PASS. Verified pressure **37306407247 PASS**, report `a85f25e492402adceec35594936c0608f1295d52`, advances accepted executable slot coverage to **2457/2486 =98.83%** and selects distinct **PETSKILL_2BattleTimid / ID636 / 2 uses / 2 templates** next. Original numeric command/compiler/PRNG and JSS/Taiwan-v1 membership remain **OPEN**. See `specs/STONEAGE-MODIFYATTACK-RUNTIME-R1.md`.


## 2026-10-05 — 2BattleTimid exact data and conditional native reference accepted

**LATER_RECOVERED / CONDITIONAL REFERENCE:** recovered25 complete PETSKILL_2BattleTimid family is ID636, with two skill3 uses on TEMPNO178/179, graphics101872/101873 and exact17-byte OPTION hash. Three fixed descendant pins pass19 source gates each; exact/native Action37309960471 PASS compares528 callback and53196 post-recall witnesses including actual raw OPTION across two explicit execution-charsets. UTF-8 literals preserve incoming powers/chance0; Big5 literals derive fixed attack50%, quick130%, chance60, preserving defence. No original build charset is inferred. Positive undemoted damage consumes a draw before the damage>1/pet checks; pet recall uses PetIn(defNo-5), with NORETURN preventing withdrawal/default mutation/BS while outer K/KS notifications still occur. This is distinct from BattleTimid's player-exit path. Original numeric COM1/compiler/libc PRNG, wolf/fox/default-pet lifecycle, ordered runtime and JSS/Taiwan-v1 membership remain **OPEN**. Accepted executable coverage stays2457/2486=98.83%. See `specs/STONEAGE-2BATTLETIMID-REFERENCE-R1.md`.


## 2026-10-05 — 2BattleTimid normal-pet lifecycle source audit and inconclusive build assay

**LATER_RECOVERED / SOURCE AUDIT:** verified Action37311978479 PASS closes36 textual gates across the three fixed descendant pins for PetIn -> player-owner PetDefaultExit -> matching BATTLE_Exit entry/escape/FINAL/battleindex changes. Owned pet membership and HP are separate from selected-default and battle occupancy. The preserved service root's sole273-byte ELF exposes neither required symbol, so the bounded UTF-8/Big5 discriminator is inconclusive; no original build is selected. Modern state audit identifies absent independent default-pet/NORETURN state and the need to stop treating retained pet membership as active selection during later player death. Ordered runtime remains OPEN; coverage unchanged2457/2486=98.83%. See `specs/STONEAGE-2BATTLETIMID-RUNTIME-STATE-AUDIT-R1.md`.


### 2026-10-06 — BattleModel descendant status-table correction

**FACT (fixed descendant source comparison):** three pinned profiles retain
BattleModel's two-byte source-order status lookup but differ in literal
spellings and lengths. The reference must retain independent source and
charset witnesses. An original compiler/source profile cannot be inferred from
visual similarity or a successful modern decoder.
[`SRC-BATTLEMODEL-STATUS-PROFILES-R1`]

**OPEN:** hash-verified recovered25 OPTION/status identity and replacement
remote source/native acceptance remain pending; runtime is not promoted.


### 2026-10-06 — BattleModel hit-helper boundary refinement

**FACT (fixed descendant helper):** absorb/vanish explicitly suppress damage
wakeup but do not independently suppress the surviving positive-damage status
check. A nonphysical hit can retain a Guardian notification witness while the
original target remains the actual defender.
[`SRC-BATTLEMODEL-HIT-LIFECYCLE-R1`]

**OPEN (source defect):** the DODGE path can reach presentation formatting
with an uninitialised pet-damage value. Exact original bytes are not accepted.


### 2026-10-06 — BattleModel conditional reference acceptance

**FACT (recovered25 data / fixed descendant bridge):** exact-data37342593141,
source/native37342593073 and helper37344060042 SUCCESS supersede the pending
2026-10-06 records above. Complete callback population638/641/649/650; only638
has two positive placements,1178/101867/slot3 and1179/101868/slot3. Three
Big5 witnesses select paralysis/index2; three UTF-8 witnesses leave that token
unknown. Attack70% versus unchanged attack is similarly conditional.600
native target-plan and1296 controlled helper witnesses close only their bounded
contracts. **OPEN:** original charset/compiler/numeric COM1, exact source
DODGE presentation, original JSS/Taiwan-v1 membership and ordered runtime.
Coverage remains2461/2486. [SRC-BATTLEMODEL-CONDITIONAL-REFERENCE-R1]


### 2026-10-06 — BattleModel native settlement correction

**FACT (reduced fixed-descendant native DamageSub):**1920 calls across the
three established pins prove marker-specific reflect consumes a charge while
preserving both HP and positive reported damage. This supersedes any earlier
interpretation that the marker branch subtracts defender HP. Raw-threshold
ultimate2 can occur without HP loss. **OPEN:** original invalid absent-ride
read behavior, full active build gates, ordered flag-to-exit integration, ride
composition and remote acceptance of this supplemental audit.
[SRC-BATTLEMODEL-BASE-SETTLEMENT-R1]


### 2026-10-06 — BattleModel base settlement remote acceptance

**FACT (bounded native reproduction):**37349075552 SUCCESS on33a8e76a
accepts1920 reduced-feature no-ride DamageSub calls across the three fixed
pins. The preceding remote-pending record is superseded. Both-HP-preserving
reflect, positive reported damage, counter consumption/sentinel bypass and
raw-threshold ultimate2 are accepted only within that contract. Full runtime,
mounted composition, source pet-entry lookup, flag-to-exit behavior and
original executable/profile membership remain **OPEN**.


### 2026-10-06 — reconstructed runtime admission column correction

**FACT (modern reconstruction defect, not a new original-game claim):** the
independently accepted recovered25 2BattleTimid probe places ID636 on source
skill column3 for templates178/179. The modern seven-slot runtime tuple is
zero-based. The existing bridge and integration fixture index3, and the earlier
runtime spec's column4 table, were inconsistent with that evidence. Regression
witnesses reproduced both rejection of the actual placement and acceptance of
the shifted placement. They are repaired to runtime index2; original erroneous
records remain visible and are superseded by the dated spec correction.

**IMPLEMENTED / OPEN:** the first BattleModel admission seam now derives slot
indices from its independent exact probe, validates all four callback rows and
the two exact positive templates, and preserves explicit conditional profiles.
Synthetic local fixture tests pass. Newly extended verified-data and existing
runtime regression Actions must pass before acceptance. No ordered BattleModel
execution, new historical build profile or additional covered slots are claimed.
See `SRC-RUNTIME-ADMISSION-SLOT-BASE-20261006`.


### 2026-10-06 — exact admission correction remotely accepted

**FACT (reconstruction acceptance):** all27 Actions on5c555bf7 succeeded,
including six required actual-data/runtime/core/coordinator/golden/full-region
gates. Hash-verified actual data reproduces24 conditional638 admissions and4
corrected636 admissions. The earlier repair-pending record is superseded.
Only bounded typed BattleModel admission and repaired2BattleTimid admission
are accepted. Full BattleModel execution and its two positive slots remain OPEN.
Independent local post-AttackSeq loop preparation is not part of this acceptance.


### 2026-10-06 — bounded BattleModel loop and literal pet guard witnesses

**FACT (fixed-source reduced experiment):** original hit helpers compiled
transiently at all three established pins, with SIDE_OFFSET10 and shared stubs,
confirm pet targets5..9 guard opposite entries10..14, independently of ordinary
owner entries0..4. All20 cases/profile,60 total pass locally. Original
multiplayer offset12 and original executable/build remain OPEN.

**LOCAL_TESTED (modern implementation):** post-AttackSeq ordered scheduling,
marker-specific settlement, wake/status and distinct command/ultimate state
have81 local tests and480 direct physical marker/native comparisons passing.
Original1920 no-ride native calls still pass. Source TargetCheck does not
independently test ultimate entry flags; a surviving flagged target is not
silently killed/exited by this bounded loop. Full round exit remains OPEN.
AttackSeq, no-ItemCrush, no-ride/nonthrowing/gDamageDiv0 and reduced offset10
limits are explicit. Source surviving-target ItemCrush occurs before status;
its equipment/RNG seam must be closed for complete integration.
See `SRC-BATTLEMODEL-POST-ATTACKSEQ-LOOP-R1`; remote acceptance pending.


### 2026-10-06 — bounded post-AttackSeq seam accepted remotely

**FACT (bounded reconstruction acceptance):**37355987371 SUCCESS onf5568edd,
job111918386052, reproduces the controlled loop/shared tests,1920 native
settlement calls,480 physical marker/model comparisons and60 literal pet
pre-hit guard cases. Earlier remote-pending records are superseded. This
closes only reduced offset10/no-ride/nonthrowing/no-ItemCrush/gDamageDiv0
composition; production AttackSeq, complete round/state/coordinator and
pressure remain OPEN. No original build selection or new covered slots.


### 2026-10-06 — bounded physical AttackSeq composition locally validated

**LOCAL_TESTED:** real shared physical arithmetic is connected to the ordered
BattleModel loop under explicit equipment-free/no-bow/no-later-features/neutral
globals and existing no-ride/no-ItemCrush/reduced-offset10 exclusions.157 tests
and696 transient native original11-function comparisons pass across three
pins/two defense variants. Source Duck gates/drunk RNG precede Guardian;
actual defender drives critical/damage/guard and later status/command changes.
Full ordinary runtime and two638 positive slots remain OPEN.

**FACT (source; scope correction):** gavin's legacy player ItemCrushCheck draws
RAND before equipment lookup. TAKE_ITEMDAMAGE defender slot selection draws
raw rand()%100 before item validation. Empty equipment therefore does not
prove a no-ItemCrush RNG seam. Both feature variants and full chronology require
further native reproduction; original build membership remains OPEN.
See `SRC-BATTLEMODEL-PHYSICAL-ATTACKSEQ-R1`.


### 2026-10-06 — bounded physical AttackSeq accepted remotely

**FACT (bounded reconstruction acceptance):**37359587030 SUCCESS, job
111930531041 on ce4c7a16 reproduces157 tests/696 physical native comparisons
and1920/480/60 accepted settlement/pet checks. Equipment-free physical
composition alone is closed; complete BattleModel runtime/pressure/two638
slots remain OPEN. Earlier pending records are superseded.

**FACT (additional source inspection):** legacy and TAKE_ITEMDAMAGE checks
agree across all three pins about RNG before equipment can eliminate an item.
Bismarck additionally guards pet equipment count and a FIX variant using
rand()%equipnum; these are separate profile choices, not original-build facts.
ItemCrush native acceptance and chronology integration remain OPEN.


### 2026-10-06 — empty-equipment ItemCrush chronology locally validated

**FACT (fixed source/native experiment):** all three source defaults are
400000. Source helper calls ItemCrush on surviving DODGE/MISS/ALLGUARD/zero
damage, routed to actual Guardian before status. Legacy player strict check
draw survives empty equipment; successful empty scan returns before another
RAND. TAKE consumes raw rand before equipment checks; guarded Bismarck
FIX/pet variants retain modulo5 failed-scan increments even for seven slots.
3420 native comparisons pass across separately declared variants; not
original-build/PRNG membership or equipped mutation acceptance.

**LOCAL_TESTED:**170 tests/13 new item witnesses and existing696 physical
comparisons PASS. An explicit empty-equipment loop scope replaces the previous
no-ItemCrush exclusion, including DODGE reachability. Complete ordinary
runtime/state/coordinator/pressure/638 slots remain OPEN; remote gate pending.
See SRC-BATTLEMODEL-EMPTY-EQUIPMENT-ITEMCRUSH-R1.


### 2026-10-06 — empty-equipment ItemCrush remotely accepted

**FACT (bounded reconstruction acceptance):**37411512720 SUCCESS, job
112100761415 on7c7de32d reproduces170 tests/3420 ItemCrush native
comparisons plus696 physical and1920/480/60 settlement/marker/pet checks.
Only declared empty-equipment chronology is closed, including surviving
DODGE/zero damage before status. Full runtime/equipped mutations/original
profile membership/638 slots remain OPEN. Earlier pending records superseded.


### 2026-10-06 — prepared BattleModel handoff locally validated

**LOCAL_TESTED (reconstruction seam):**283 tests PASS, including12 handoff
witnesses and101 existing ordinary round tests. Actual ordinary continuation
confirms successful one-turn paralysis cancels an already prepared attack even
as status expires; failed status preserves action, and completed actors never
repeat ticks. Guardian/current HP/reactions/flags propagate without re-sorting.
Explicit fresh preparation clears round-local cancellation only. New death/
ultimate flags block continuation until exit/profit integration. Original full
command loop, persistent/coordinator integration and638 slots remain OPEN;
no new historical build or Taiwan-v1 membership claim. Remote gate pending.


### 2026-10-06 — bounded prepared handoff accepted remotely

**FACT (bounded reconstruction acceptance):**37412928360 SUCCESS,
job112105158829 on57d21667 reproduces283 tests and existing696/3420/
1920/480/60 native gates. Prepared cancellation and current-work handoff alone
closed; full original command loop/state/coordinator/ultimate exit and638
coverage OPEN. Internal semantic carrier is not a historical numeric COM1.
**OPEN (repository integration review):** ordinary player ultimate exit uses
unique active pet projection; audit against DD-020 before integration. No
historical claim or exit correction accepted here. Pending records superseded.


### 2026-10-06 — nonlethal BattleModel ordinary/state/coordinator locally validated

**LOCAL_TESTED:**31 new actual round/state/coordinator witnesses,428 total
PASS. Actor status tick precedes symbolic638 dispatch; confusion can replace
it with ordinary attack, paralysis expiry never restores cancelled commands,
poison/current drunk QUICK propagate without re-sorting. Actual Guardian and
hit state affect later actors; next preparation resets cancellation. Explicit
coordinator re-admits current spawned/template/skill/work identity. Death or
ultimate composition fails before committing state; full lethal/automatic-AI/
original command-loop/638 slot acceptance OPEN. No original build/Taiwan-v1
membership claim. Existing696/3420/1920/480/60 native reruns PASS; remote
exact input and all shared-workflow regressions pending.


### 2026-10-06 — bounded nonlethal BattleModel round/state/coordinator accepted

**FACT (bounded reconstruction acceptance):** exact a03b8781 passed all32
triggered workflows. Settlement37414798897/job112110945349 reproduces428
tests and696/3420/1920/480/60 native hit checks; artifact11390323818 uploaded.
Status clock/rewrite, current-work cancellation, persistent state and explicit
coordinator transaction closed only for declared nonlethal empty-equipment
scope. Baseline golden/region pass does not certify new BattleModel scenarios.
Full lethal/automatic-AI/native command-loop/638 coverage OPEN. Earlier remote
pending snapshot superseded; no original build/Taiwan-v1 membership claim.


### 2026-10-06 — explicit DEFAULTPET helper audit accepted

**FACT (bounded descendant helper):**37415958204/job112114499031 PASS on
b6ca59eb,486 original-function cases at three clean fixed pins. Controlled
getters/Exit confirm exact selection lookup and unchanged selection, not sole
active-pet inference. **STATIC:** player Exit also has independent Entry[i+5]
cleanup; pet UltimateExtra clears owner DEFAULTPET. Full native cleanup/profit
not certified. **OPEN:** current ordinary/continuation inference and absent
pet-ultimate selection transition require correction before lethal638. Older
"paired/default" terminology superseded; no Taiwan-v1/build membership claim.


### 2026-10-06 — DD-020 ordinary and continuation exit correction local milestone

**LOCAL_TESTED:**22 new actual flow witnesses/535 targeted regressions PASS.
Explicit nullable roster selection and separate i+5 occupancy cleanup replace
sole-pet inference. Pet ultimate clears selection chronologically before later
player-death loyalty, including within multihit; actual Guardian and absent
dead carried entries propagate. Terminal return preserves ownership/HP and
excludes final profit. No full native exit/profit, lethal638 or original build
membership claim. Broad discovery has identical clean-baseline failures and
optional-dependency import errors. Remote exact/shared/full-region gates pending.


### 2026-10-06 — explicit default-pet ultimate state correction accepted

- Modern bounded correction on0a4cecc3/tree97546cab: all33 Actions SUCCESS;
  settlement37417691024 reproduces535 tests including22 new cases and
 486/696/3420/1920/480/60 prior native gates. Full-region37417690927 PASS,
  reports unchanged. Explicit nullable selection and separate occupancy now
  replace sole-active-pet inference; pet ultimate clears DEFAULTPET before
  later player-death loyalty. Ownership and carried HP restoration retained.
- This supersedes correction-pending status, not historical build provenance.
  Full native cleanup/profit, lethal638/AI/pressure and positive slots OPEN.
- Static preflight at the same three clean pins locates PvE death scanning in
  AddExpItem and distinguishes per-hit ordinary profit from post-dispatch
  BattleModel command-tail profit. Scan-order mutation is the next native
  gate; static anchors alone do not certify the full composition.


### 2026-10-06 — original bounded PvE profit/exit composition local audit

- Three clean fixed descendant pins compile seven original profit/death/exit/
  status-clear functions together with original relevant header declarations.
  Declared feature-off PvE/no-item/no-ride/non-mail scope:19656 native cases
  PASS locally,6552 per pin. Exact remote acceptance pending.
- Source-bounded observations: side/slot scan mutations from player ultimate
  can prevent later paired-pet death processing; earlier pet-ultimate profit
  calls clear DEFAULTPET before later owner penalties. BadStatusAllClr also
  clears ISDIE and all ten unconditional StatusTbl fields. Independent modern
  runtime still has separately represented overlays; no full exit/638 claim.
- Original full Battling/638 command-to-profit execution, compiler/feature/
  version membership and hash-verified specific pressure remain unresolved.


### 2026-10-06 — bounded native PvE profit/exit remote acceptance

Exact c1c3209e/tree777d45a0, run37420393572/job112128219849 SUCCESS:
19656 seven-function native cases,535 regressions and prior486/696/3420/
1920/480/60 native gates reproduced. Artifact11392388401 and acceptance
receipt preserve exact source/header hashes and boundaries. Earlier remote
pending status superseded within feature-off PvE/no-item/no-ride/non-mail
scope. No modern runtime code change, lethal638/native full command driver,
original active feature/version or slot-promotion claim. Whole-scan profit
adapter and ten-field/overlay clear are next.


### 2026-10-06 — Immutable PvE scan adapter local comparison

- MODEL/LOCAL_VALIDATED: new independent immutable adapter reproduces19656
  already accepted native death/exit vectors and their recorded writes. This
  adds modern model comparisons, not new original executions or a version claim.
- DESIGN: projecting original counter clear into the modern separate late-status
  overlay requires clearing counters/visit flags and invalidating cached Weaken
  powers. Recalculation is an explicit unresolved caller seam; active deep poison
  and unmodeled statuses are rejected. Existing runtime drivers are not wired.
- OPEN: full command-native chronology, modern lethal638, actual Guardian-to-
  profit composition, sparse rosters/party recipients and specific golden/
  region/pressure gates. Exact remote acceptance pending.


### 2026-10-06 — Isolated immutable PvE scan adapter accepted

- MODEL/FACT within declared domain: input737da287/tree41fc4788, required
  run37422202059/job112133821223 SUCCESS,19656 model/native comparisons
  and560 related tests. Source pins/function hashes retain the prior original
  composition provenance. No new original command execution or version claim.
- DESIGN: reject EXP intermediate overflow; modern status projection emits
  attribute-recalculation requirements instead of fabricating work powers.
  Active deep poison/unmodeled statuses remain outside the admitted schema.
- OPEN: existing drivers still need explicit scan/recalculation integration,
  full native command chronology and Guardian-to-profit witnesses. Modern
  lethal638, original build/version and specific golden/region/pressure OPEN.


### 2026-10-06 — Actual player Exit late-status local bridge

- MODEL/DESIGN: real ordinary and outer continuation player exits now consume
  the admitted late-counter/cache clear. Persistent carried state restores
  original session/independent buff views instead of retained Weaken powers.
- Existing native evidence replays19656 scan comparisons and384 narrow
  Other_DefcharWorkInt recalculation vectors; no new source/version claim.
 15 new actual runtime tests and643 related regressions PASS locally.
- OPEN: full command-native scan integration, original complianceParameter,
  intra-continuation late interactions, lethal638 and exact remote acceptance.

### 2026-10-06 — Actual player Exit late-status bridge remotely accepted

- MODEL/FACT within the declared modern bounded runtime: exact head
  `0425028d5965c76d34106a427c4a47f4a56f620b` passes all triggered remote gates (main 33/33; synchronized
  work branch 31/31). Settlement `37425651218/112144564632` reproduces
  643 tests, 19656 accepted whole-scan/model-native comparisons and 384 bounded
  Weaken attribute-recalculation vectors.
- DESIGN: actual player UltimateExtra/Exit and the outer continuation Exit path
  clear admitted Nocast/Barrier/Weaken counters and stale prepared Weaken powers
  only when explicit owner/default-pet authority and the complete non-mail
  carried roster are available. Missing authority remains fail-closed.
- OPEN: the persistent profit layer still charges deaths from damage-event order.
  Native evidence requires side/slot whole-scan order at each real profit
  boundary. Actual per-hit/ID638 command-tail snapshots, processed-death
  accounting, full command-native chronology, Guardian/multi-victim witnesses
  and lethal638 therefore remain unresolved.

### 2026-10-06 — Pre-settlement profit-boundary runtime trace accepted

- MODEL/FACT within the declared modern bounded runtime: implementation
  `6d4298c40fca439d1dcf153b5630c24d3b4de0d6` passes 31/31 triggered workflows, including settlement and
  recovered25 region. Final test-only input `fe9109a7440caa9c10847eb649c01c28b7348075` passes
  settlement `37427836728/112151449355`: 646 tests, 19656 accepted immutable
  scan/model-native comparisons and 384 bounded Weaken recalculation vectors.
- DESIGN: an immutable `OrdinaryProfitBoundarySnapshot` is now captured at
  actual modern profit-boundary candidates. It separates HP, occupancy,
  round-local ultimate flags, explicit DEFAULTPET authority and prior processed
  deaths. Player-ultimate state is observed before Exit mutates occupancy;
  nonlethal BattleModel638 is grouped once at command tail, not once per hit.
- OPEN: this is observation, not settlement. Persistent
  `_pending_profit_after_ordinary_round()` remains event-order based until the
  next adapter consumes the snapshots through `resolve_profit_exit_scan()`
  and charges only `processed_death_ids`. Counter/BatFly grouping, full
  original command chronology, actual Guardian/multi-victim composition and
  lethal638 remain unresolved.

### 2026-10-06 — Persistent processed-death / ISDIE state accepted

- MODEL/FACT: exact input `55416079254b542c2c792d2848b6d2a493345335` passes 32/32 triggered workflows.
  Settlement `37428752934/112154374994` reports 648 tests, 19656 accepted
  scan/model-native comparisons and 384 bounded Weaken recalculation vectors;
  recovered25 region `37428752792` passes.
- DESIGN: source ISDIE is now persistent runtime state independent from ReLife
  eligibility. It may represent zero-HP player/pet/enemy entries still in the
  battle array, survives rounds, and is cleared by revive or exit/removal.
- OPEN: the state is not yet settlement authority. The persistent pending-profit
  walk remains event-order based until a canonical boundary binder drives
  `resolve_profit_exit_scan()` and consumes `processed_death_ids`.

### 2026-10-06 — Canonical whole-scan runtime binder accepted

- MODEL/FACT: implementation `babf091e66192463cc51ac06a51348b8ef010048` passes 31/31 triggered workflows;
  final test-only input `f9bc6b1688500987562fda89ab347984ab12a684` passes the settlement gate. Settlement
  covers 653 tests plus the existing 19656 immutable scan/model-native
  comparisons and 384 bounded Weaken recalculation vectors; recovered25 region
  also passes.
- DESIGN: supported canonical SIDE_OFFSET10 ordinary per-hit and nonlethal638
  command-tail boundaries now execute the accepted immutable whole scan and
  persist its accounting. Unsupported layouts/recipients/groupings remain
  explicit fallback, not silently coerced.
- CORRECTION: the new integration proves a round-wide event-order bug can
  retroactively misclassify an earlier normal pet death after a later player
  ultimate. Sequential whole-scan boundaries preserve the earlier normal death
  and carry ISDIE forward.
- OPEN: full original command-driver execution with actual Guardian victims and
  multi-victim BattleModel tail remains required before lethal638.

### 2026-10-06 — BattleModel dispatch-tail profit splice accepted

- NATIVE/FACT: exact input `da3512edb89877d0761fde7ddbe083f03237dd0e` passes settlement
  `37433803780/112170605599`. Three pinned source profiles each contribute
  three native splice vectors (**9 total**) while the existing 19656 whole-scan
  native/model comparisons and 653 regressions remain green.
- CHRONOLOGY: exact original BattleModel planner/helper executes before the one
  command-tail original AddProfit. The multi-victim witness records pet damage
  then owner damage before any ISDIE/death write; the scan subsequently follows
  source slot order and repeat profit is idempotent.
- HARNESS CORRECTION: absent Guardian is represented by TargetCheck(-1)==false,
  and BCF result flags retain original bitmask values. Synthetic sequential flag
  IDs had produced a false critical/ultimate branch and were rejected.
- OPEN: original AttackSeq/GuardianCheck is still a controlled seam in this
  splice and full Battling body execution remains a stronger later gate.

### 2026-10-06 — Same-harness original Guardian profit-tail accepted

- NATIVE/FACT: exact input `93bd7fa550eaa99137015109237b78a67815c1fd` passes settlement
  `37436034852/112177967610`: 653 tests, 19656 whole-scan original/model
  comparisons, 384 Weaken recalculation vectors, prior splice 9/9 and new
  same-harness Guardian vectors 9/9 across three pinned profiles.
- CHRONOLOGY: original GuardianCheck/AttackSeq, BattleModel helper and tail
  AddProfit now execute in one transient program. A zero-HP guardian can still
  be returned before ISDIE is written, but BattleModel's post-AttackSeq
  TargetCheck rejects it and actual damage falls back to the requested owner.
  Tail profit runs only after the full hit batch and scans source slot order.
- HARNESS CORRECTION: Guardian/ABIO/NODUCK bits are imported from original
  battle.h (1<<3, 1<<6, 1<<7). A synthesized ABIO value had overlapped the
  Guardian bit and generated a false ultimate path; that evidence was rejected.
- OPEN: same-harness exact DamageSub and full Battling body remain stronger
  gates before lethal638.

### 2026-10-06 — Same-harness exact DamageSub profit-tail accepted

- NATIVE/FACT: exact input `f804d879cc701b0b29c2d3f2adbd1e2b6df1eddc` passes settlement
  `37437282822/112182088944`: 653 tests, 19656 whole-scan original/model
  comparisons, 384 Weaken recalculation vectors and 9/9 new exact-DamageSub
  same-harness witnesses across the three pinned profiles.
- CHRONOLOGY: original GuardianCheck/AttackSeq, exact DamageSub, BattleModel
  helper and tail AddProfit now execute in one transient program. Exact HP
  writes finish before the one tail ISDIE/death scan; multi-victim processing
  still follows source slot order and repeat AddProfit is idempotent.
- BOUNDARY: the source helper's uninitialized iPetDamage presentation input is
  deterministically seeded to zero only at the wrapper boundary; packet or
  historical undefined-value behavior is not certified.
- OPEN: full original `BATTLE_Battling` execution is the next stronger gate
  before lethal638.

### 2026-10-06 — Full BATTLE_Battling BattleModel profit-tail accepted

- NATIVE/FACT: exact input `1fd9866556f9cf0ec338e22c804a4354e2f8c3e0`, tree `533c3554a4ade9a49b52f3263c6b6d584d3fe68a`, passes
  settlement `37441895862/112197395144`: 653 tests, 19656 original PvE
  profit/exit cases, 19656 immutable scan/model-native comparisons, 384 Weaken
  recalculation vectors and **9/9** new full-`BATTLE_Battling` witnesses
  across the three pinned profiles.
- CHRONOLOGY: the exact full command-driver body executes the original
  BattleModel case, original Guardian/AttackSeq, exact DamageSub,
  BattleModel/helper and the common-tail AddProfit/exit scan in one transient
  program. All hit writes precede the one tail death scan.
- RUNTIME DIFFERENTIAL: all **9/9** post-hit native boundaries also directly
  match the accepted canonical BattleModel638 runtime binder for ISDIE,
  death/charm/loyalty state and processed-death order.
- BOUNDARY: nine scheduler/status/presentation command-driver helpers remain
  controlled neutral seams; the historical undefined DamageSub pet-damage
  presentation input is still deterministically zero-seeded. Build/version,
  ride/items, wider recipients, automatic AI and packets remain open.
- OPEN: next gate is lethal638-specific recovered-ID admission through the
  persistent/coordinator runtime boundary; no positive slot is promoted yet.

### 2026-10-06 — ID638 normal-death persistent/coordinator bridge accepted

- RUNTIME/FACT: explicit scope
  `lethal_normal_profit_base_round_empty_equipment_ID638_R1` admits a normal
  death created by recovered ID638 into the BattleModel command-tail profit
  boundary; the older nonlethal scope still rejects death.
- SETTLEMENT: final input `89848f2ed92c4aa4c21c70d68356fe52b951ab40`
  passes BattleModel settlement `37443593822/112202958318` with **655 tests**
  plus the existing native/full-Battling/whole-scan gates.
- PERSISTENCE: coordinator re-admission, immutable whole-scan settlement and
  persistent processed-death authority now compose for the bounded normal-death
  path. Coordinator, golden and recovered25 region pressure all pass at the
  implementation head.
- BOUNDARY: ultimate flags/Exit remain rejected. This is not full lethal638 and
  promotes no recovered positive slots.
- OPEN: next gate is source-slot-ordered BattleModel command-tail
  ultimate/Exit, especially Guardian pet5 hit-before-owner0 versus AddProfit
  owner0→pet5 scan order and default-pet effects.


### 2026-10-06 — ID638 ultimate/Exit full-command-tail bridge accepted

- NATIVE/MODEL within the declared reduced profile: exact input `12f61e06a8e773bf223f37d7be9acc67460571e7`,
  tree `2b7ef3df20b01801a5d80a758a70c5a22baf35eb`, passes settlement `37448704545/112219678935`:
  661 regressions plus 48 original full-Battling ultimate/native-binder vectors.
  Coordinator and generic runtime golden also pass at the same input.
- CHRONOLOGY: actual pet5→owner0 hit order does not define death scan order.
  Source AddProfit processes owner0 first; default-pet and player Exit remove
  slot5 before a separate pet death can charge or clear default selection.
  Standalone pet ultimate clears selection. Normal/ultimate mixed victims,
  accumulated ultimate1, direct ultimate2 and no-risk are native-differential
  witnesses; repeat profit leaves all native gameplay state unchanged.
- BOUNDARY: original active build/version and packet/status/scheduler history
  remain unresolved; native C OPTION effects/presentation are neutral seams.
  Exact recovered OPTION identity is independently enforced by typed admission.
  No positive runtime slots are promoted until specific exact-data/golden/region/
  pressure witnesses cover both recovered ID638 placements.


- **2026-10-06 — FACT (bounded recovered25 experiment):** exact input
  `24b61a6c3f051d7d6f44efb67df34af1c0eff0c5` passes four native/runtime/coordinator/golden/verified-region
  workflows. Both positive ID638 templates pass60 conditional runtime goldens
  and the same60 concrete-stack witnesses;12 current row/template/slot mutations
  reject per suite. Pre-player-clock paralysis is observed separately from final
  state. The complete2486-placement pressure remains2461 closed/22 OPEN/3 UB;
  normal AI selected BattleModel dispatch is still OPEN and no slot is promoted.
  This is LATER_RECOVERED conditional runtime evidence, not Taiwan-v1 membership,
  original active-build or historical encounter/packet proof.
  Receipt: `research/recovered/STONEAGE-BATTLEMODEL-RECOVERED-RUNTIME-GOLDEN-ACCEPTANCE-R1.json`.


- **2026-10-06 — DESIGN / conditional reconstruction (remote acceptance PENDING):**
  normal enemy-AI selected ID638 now has an explicit typed batch/round seam.
  Slot/target/current work are derived by the coordinator;60 independently
  controlled AI cases accompany the prior60 exact-template runtime cases.
  A separate hash-verified active variant census will distinguish real normal
  AI options from controls. This does not prove natural encounter reachability
  or original active-build/Taiwan-v1 membership;0 placements are promoted.


- **2026-10-06 — FACT (bounded recovered25 conditional experiment):**
  exact input `e2f957095a3c5a81133ed720df63dfe11396a2e1` passes four core workflows,
  full826-floor region and850 local tests. The normal-AI selected typed ID638
  seam is accepted with60 control companions plus60 exact-template runtime
  cases, repeated in the concrete stack. Actual active variants2559/2560
  (templates1178/1179) have normal TACTICS1 but wa index2 weight0; both have
  zero actual selected-AI cases. This proves absence from that current common
  weighted selection path, not universal absence of another command entry.
  **No slot promoted**; ledger2461 closed/22 OPEN/3 UB retained.
  Receipt: `research/recovered/STONEAGE-BATTLEMODEL-AI-SELECTION-ACCEPTANCE-R1.json`.

## 2026-10-06 — Pinned descendant BattleModel entry boundary

FACT (version-tagged descendants, not Taiwan-v1/original executable): nonzero
ILLEGAL PET skill admission rejects before callback under the three default
headers; source/native2592 default-header cases and864 separately labelled
Bismarck OPEN_E counterfactual cases. Direct equipment magic forwards a runtime
array without lookup. Default OPTIMUM storage uses numeric IDs as arrays;
legacy storage uses file order, and original executable layout remains OPEN. Default magic feature enabled only
in gavin/iris among these profiles. Actual data magic reachability PENDING;
opaque script/build flags remain OPEN. TemplateAI150 is MODAI, while enemy
TACTICS/wa are separate. See command-entry audit R1; no historical path or
pressure promotion inferred from conditional controls.

## 2026-10-06 — Accepted ID638 negative configured-path census

FACT for exact recovered25 active masters:181 magic rows, zero literal
BattleModel callback OPTION candidates; enemy2559/2560 have zero positive
loader-first group/area references and zero index2 wa weight. These are bounded
configuration facts, not universal unreachability or proof of no NPC/scripts.
All three default descendant headers enable OPTIMUM ID-indexed storage;
legacy row order is a separate layout. This corrects the preceding pending
ordered-only array interpretation. Original active executable flags remain
OPEN.2592 original default-header entry guard controls and864 separately
counterfactual controls pass. Full pressure unchanged2461/22/3,0 promotions.
Accepted receipt is command-entry acceptance R1; scope remains later recovered
material and explicitly pinned descendants, not original Taiwan-v1 membership.

## 2026-10-06 — Conditional capability criterion implementation (not a new historical claim)

The rebuilt analysis can qualify exact ID638 placements as conditional bounded
capability, independent of natural entry. This adds no historical command path:
actual wa index2 weights0, configured magic candidates0 and positive group/area
references0 remain as audited. PET ILLEGAL guard and original build/NPC/script
uncertainties persist. Whole-file and complete semantic binding protect scope;
exact-head pressure promotion evaluation PENDING, predicted +2 capability uses.


## 2026-10-06 — Recovered25 ID638 capability classification accepted; no new historical reachability claim

FACT for the hash-verified later recovered25 specimen: the two exact positive
ID638 placements at templates1178/1179 runtime index2 satisfy the project's
bounded execution-capability gate, raising complete capability pressure to
2463 closed /20 OPEN /3 historical UB out of2486. FACT remains that the active
normal variants have wa index2 weight0 and produce0 actual normal-AI selections
in the verified gate. DESIGN/analysis classification of those placements as
conditional capability does **not** establish how an original active executable,
player/pet command, equipment magic, NPC or script made the skill reachable.
Those provenance questions remain OPEN and Taiwan-v1 membership is not inferred.


## 2026-10-06 — Later recovered25 BecomeFox source/data reference closed

FACT for the hash-verified later recovered25 specimen: PETSKILL_BecomeFox has
one active row, ID625, and exactly two positive enemybase placements at TEMPNO
148/149 report slot3. Three pinned descendant source trees share the bounded
post-attack fox/FOXROUND structure but materially diverge in PetIn FOXROUND
accessor choice. This is later-source/data lineage evidence only; it does not
date the feature, establish JSS/Taiwan-v1 membership or identify the recovered
executable's exact descendant semantics.


## 2026-10-07 — BecomeFox bounded runtime acceptance and BecomePig source divergence

MODEL/FACT within the declared later recovered25 reconstruction slice:
reviewed input698660bc passes35/35 remote workflows and914 unique local tests.
BecomeFox's two exact positive placements are accepted as bounded execution
capability; complete ledger2465 closed/18 OPEN/3 historical UB out of2486.
No original JSS/Taiwan-v1 membership or natural encounter proof follows.
The source/model fox image remains101749; one spec typo was corrected.

FACT for separately pinned descendant source blobs only: BecomePig's callback
queues a command, while its postattack eligibility requires a player and success
adds to an ordinary BECOMEPIG counter. gavin/iris parse OPTION without checking
conversion count; Bismarck instead contains a literal pointer-comparison branch
and different else defaults. These source differences and potential undefined
paths require independent analysis; no BecomePig reference/runtime is accepted.
Exact profiles/blobs and OPEN issues are in the preliminary source observation
receipt. Actual time decrement/lifetime owner and recovered25 OPTION rows remain
OPEN. Do not transfer BecomeFox's pet target or round timer into this skill.


## 2026-10-07 — Later recovered25 BecomePig source/data reference closed

FACT within the hash-verified later recovered25 specimen: complete callback
family628/631/635 includes unused empty-OPTION628 and exactly two positive uses,
631 on template170 and635 on1147, both report slot3. Independent discovery and
pinning Actions37616100623/37616438050 PASS with8 probe tests and24 structural
gates at each fixed source profile. This does not date introduction or establish
original JSS/Taiwan-v1 membership. Native/runtime acceptance and actual OPTION
conversion counts remain OPEN; capability pressure remains2465/18/3 of2486.
Preliminary network/default-header/getter observations also expose separate
source timing profiles; no original executable clock/build is selected.


## 2026-10-07 — Later-source BecomePig isolated native reference closed

FACT within the pinned descendant-source and recovered25 witness domain:
independent Actions37618493394/37618923213 reproduce62720 original-C postattack
and5364 isolated timer/Exit comparisons at O0/O2 with nonrecovering UBSan. Native
actual631 yields2 conversions and635 yields3; gavin/iris counter parameters180
retain image100250/100388 respectively. Bismarck valid-buffer else instead uses
counter60 and image100250. Unused empty628 is not a positive placement and its
gavin/iris uninitialized postattack path is excluded. These source parameters
are not historical wall-clock duration claims. Isolated timers demonstrate
versioned decrement/cleanup differences; full clock/recipient and Exit/compliance
composition remain OPEN. No original executable/build/PRNG or feature date is
identified; no JSS/Taiwan-v1 membership follows. Runtime remains OPEN and pressure
unchanged2465/18/3 out of2486. Receipt: STONEAGE-BECOMEPIG-NATIVE-REFERENCE-ACCEPTANCE-R1.json.


## 2026-10-07 — Descendant BecomePig scheduler ownership independently witnessed

FACT only within exact pinned descendant scheduler controls: Action37621151399
passes419904 sequential O0/O2 native state snapshots. gavin/iris tick by eligible
connection visits without character deduplication; Bismarck ticks valid player
array slots independently of connections. Default service exclusions also differ.
Qualifying polls advance once rather than catching up elapsed gaps; a separate
second time sample becomes the stored clock. These are controlled source-domain
observations, not a deployed server or historical executable reconstruction.
Unrelated subsystem bodies and full compliance/Exit are outside this native
projection. No timing profile is flattened or source anomaly repaired. Pressure
remains2465/18/3 of2486, and feature introduction/JSS/Taiwan-v1 membership stay OPEN.


## 2026-10-07 — Descendant BecomePig complete restoration callers witnessed

FACT within three pinned descendants and controlled helper domains: independent
Action37624829843 passes165900 original complete compliance/Exit comparisons
at O0/O2 GNU99 with nonrecovering UBSan. New rider lookup follows pig-image
preservation in gavin/iris; Bismarck differs. Stat rebuilding precedes later
appearance/ride guards. Unused-battle error can follow appearance/compliance/
notification effects, so it is not a rollback guarantee. PETFALL sends temporary
rider-2 before final-1; ordinary pig counter persists through the bounded exit.
These complete caller bodies run with controlled equipment/stat/ride and recorded
network/badstatus dependencies, not original helper implementations or deployed
executable semantics. Full original composition and historical introduction remain
OPEN. No capability promotions; pressure stays2465/18/3 out of2486.


## 2026-10-07 — Original bad-status dependency narrows BecomePig Exit uncertainty

- FACT/SOURCE under pinned default-header controlled witnesses: full original
  BadStatusAllClr maps clear early status/death state before property-pointer
  validation. NULL returns before later profession work and owned-pet pig reset;
  a valid player property pointer permits owned pets' pig counters to become-1.
  Player's own counter persists; a pet subject does not clear its own pig counter.
  Complete original Exit proceeds after the helper's early return. Neither a
  real-server NULL occurrence nor production runtime behavior is inferred.
- gavin/iris actual selected status table44 vs Bismarck12; magic tables6 each.
  The complete default function and selected maps are transient native inputs;
  derived identities/specification only are retained. Property construction,
  stat/equipment/ride/network bodies and original ABI/build remain OPEN.
- Equipment five-column/category>5 guard leaves category5 matching-row access
  undefined in source inspection; keep it excluded until separately classified.
  Original helper batch gate pending; pressure2486 and0 promotions unchanged.

- Additional FACT in seeded witnesses: Bismarck clears NOCAST after NC but before
  unused-battle return; gavin/iris preserve it at that point. Invalid battle
  prevents this write. Previous zero-seeded caller witness remains valid within
  its scope but did not observe this distinction.


## 2026-10-07 — Original bad-status and complete restoration composition bounded acceptance

- The preceding BadStatus source/order claims reproduce in373272 original native
  comparisons at O0/O2 GNU99+nonrecovering UBSan; exact inputfad7a77ad6b9c1286e0ce574eec18e0587ca0a1d,
  Action37628605267 SUCCESS. Complete callers compose with actual status/magic maps.
  Prior165900 callers/419904 clock snapshots remain byte-for-byte reproducible.
- Property-null early return and seeded Bismarck NOCAST-before-unused-battle-error
  difference are bounded reference facts, not historical deployment observations.
  Original helper bytes/tables transient only; derived report/domain/acceptance
  receipts retained. Equipment/ride/property/stat/full timer/attack/runtime domains
  remain OPEN. Pending superseded only in accepted scope;0 runtime promotions.


## 2026-10-07 — Actual lookup tables preserve default restoration differences

- FACT under pinned default/current-compiler reference: original equipment helper
  uses first matching row; actual duplicate keys are nonconflicting but retained.
  Bismarck live-belt branch preserves current image before table/category guard.
  Equipment category5 matching-row read is undefined and excluded, not repaired.
- Static/default-active new-ride mapping composes inside whole original compliance/
  Exit/BadStatusAllClr. Static first match can use current or base player image;
  following learned-code dynamic match can overwrite it/preserved pig image.
  Item/NPC/death guards and failure dismount/status order stay original.
- gavin/iris active dynamic widths12/10; Bismarck default dynamic/static caller
  path inactive. Its declared296 static table contains104 explicit+192 zero-filled
  rows, verified as physical data without promoting inactive caller capability.
  Original source/table bytes transient only; remote acceptance pending. Stat/
  property/attack/timer/broader ownership/historical deployment/runtime stay OPEN.


## 2026-10-07 — Actual lookup and original restoration composition bounded acceptance

- Preceding actual-table/lookup/order distinctions pass322872 original native
  comparisons on exact input164b0df7f3effd4667567a460d866ac7adf5a793,
  Action37632716905 SUCCESS. Physical C census includes duplicates/zero-fill,
  separately from helper returns and complete compliance/Exit/BadStatus composition.
  Prior373272 badstatus/165900 caller/419904 clock reports reproduce unchanged.
- Bismarck default ride caller remains inactive; static192 zero rows are verified
  data, not feature activation. Real learned-mask/static-to-dynamic overwrite,
  Bismarck belt guard and item/NPC/death ordering hold only under declared fixtures.
  Category5 matching-row undefined read excluded without original repair.
  Original stat/property/attack/timer/ownership and historical deployment/runtime
  remain OPEN. Pending superseded only in accepted scope;0 promotions.
