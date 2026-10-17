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


## 2026-10-08 — BecomePig item/NPC/map conditional-block native gate ACCEPTED

- Exact input d1f7554336738a518f370ebe69eda0fefe5fa369/tree
  f4adc48861095abaee7286f1e7f865d167c3652e; Action37643425686/job112867901662
  SUCCESS. Three pinned default-source profiles, five scenarios at O0/O2 with
  ASan/nonrecovering UBSan:30 comparisons. Local rerun matches remote report
  byte-for-byte;48 related regressions PASS. Writebackfd20cf3c7ce33b5241ca2ff6aace9c47eacfdc88
  report SHA2569b2150a91e2e5e3a144275d201e0c48c1a86d3dedd9d25a53ee13e10458cd171.
  Artifact11492609019 SHA25640c37ebd165e9699a2ce3001fde41df002866cc17e22dd1cf83ee72d920f55bf.
- FACT within extracted conditional witnesses: active pig blocks item/NPC
  metamorph guards; recovery clears pig before compliance and consumption;
  strict item deadline equality preserves state; item expiry clears item/NPC
  but does not directly clear pig; map timer pauses in battle, otherwise
  decrements10 and expiry calls warp/HP1/charm-3. Item-before-map is a source-order
  check, not a whole-server scheduling claim. Warp destination is statically
  checked; native rows currently observe warp count rather than arguments.
- Scope: exact original conditionals only. Recovery keyword is statically pinned,
  not executed; compliance/presentation/item lookup/warp remain controlled.
  Complete callers/loop/timer-to-compliance composition and deployment/build/ABI/
  PRNG/JSS/Taiwan-v1 remain OPEN. Earlier whole-compliance acceptance is separate.
  Receipt:research/recovered/STONEAGE-BECOMEPIG-ITEM-NPC-MAP-ACCEPTANCE-R1.json.
- Pressure unchanged2486=2465 closed capability+18 OPEN+3 historical UB;
  BecomePig runtime promotions0. Highest priority: bounded player HP1-without-
  death/death-flag full-caller gate, then pet-death/follow/ownership/PvP/watch/enemy
  and actual stat/property/full timer composition before typed631/635 persistence.


## 2026-10-08 — BecomePig player HP/death complete-caller boundary ACCEPTED

- CLOSED_BOUNDED_PLAYER_HP_DEATH_FULL_CALLER_COMPOSITION_ZERO_RUNTIME_PROMOTIONS.
  Exact input47b72d809d487f754c45c1c10bd356d1ea540762/tree
  048672956b95eab6c6651a901968b1866079a802 passes Action37710777903/
  job113095926584:54 tooling/domain/identity tests;36864 native comparisons
  at O0/O2 GNU99+nonrecovering UBSan. Local related60 tests PASS and remote
  report equals local bytes. Timer revalidation Action37710777796 also SUCCESS.
- Complete original compliance/Exit/BadStatusAllClr plus actual accepted
  equipment/ride/status maps/helpers run through the accepted independent
  full-state/entry/property/ordered-trace oracle. Separate loyalty-argument
  oracle checks all matched player Exits. Fixed exact source/header identities.
- FACT within synthetic player HP0/1/2/150 and independent death-flag witnesses:
  gavin/iris HP1 without death invokes loyalty hook10; Bismarck invokes0.
  Death flag invokes10 then clears player death flag and writesHP1 in all profiles.
  Real-world reachability of synthetic combinations and actual loyalty effects
  are not inferred. Work/stat/property construction/ownership/party/network/
  loyalty implementation and symbolic ABI remain controlled as declared.
- Writebackfa9bb5304e1133066b6cd492f74bae86ff127700/tree
  3fd269877e8fa8beadeb5414aba1b41ea5f2a046; report blob
  856e448da43f06bd11b09fcdeefff3626dcce93b, SHA256
  ef0173710d823cc4c6f837bd0949f7b3e4bea0327fa00c1924d8d8a53c69eb57.
  Artifact11521931737 SHA256bddce105821eea31fe18382a73952c9433788f33e746b8d0b0b59c40c5c1bdf7.
  Receipt:research/recovered/STONEAGE-BECOMEPIG-HP-DEATH-ACCEPTANCE-R1.json;
  spec:specs/STONEAGE-BECOMEPIG-HP-DEATH-R1.md. Prior PENDING superseded
  within this bounded player-domain gate only.
- Pressure unchanged2486=2465 closed capability+18 OPEN+3 historical UB;
  BecomePig runtime promotions0. Highest-priority unfinished item now:
  pet-death/follow/broader ownership composition; then PvP/watch/enemy/invalid
  rider, actual stat/property and end-to-end timer/caller interaction before
  typed631/635 persistence/coordinator admission. Original executable/build/ABI/
  PRNG/JSS/Taiwan-v1 remains OPEN. No engine/content-design phase transition.


## 2026-10-08 — Pet death/mail/follow/owned-slot composition ACCEPTED; timing labels corrected

- CLOSED_BOUNDED_PET_DEATH_MAIL_FOLLOW_OWNED_SLOT_BATTLE_OCCUPANCY_COMPOSITION.
  Exact input0df7b503d372d682cd1f3b72c32df575db8c761c/tree
  b81e6506cd40e1c9e16aff1c9369824728521f75 passes Action37712138574/
  job113100233369:58 tooling/domain/regression tests and138240 native comparisons
  (3 pinned profiles x23040 cases xO0/O2 GNU99+nonrecovering UBSan). All tracked
  field/entry/property/ordered traces and added follow/owner writes match the
  independent oracle. Independent pet-return/follow/counter invariants PASS.
- FACT in one-pet/two-valid-actor controlled witnesses: owned nonmail death flag
  or HP<=0 normalizes pet HP1 before badstatus/compliance. Mail skips that roster
  restoration but not earlier player badstatus owned-pet pig-counter clearing
  when its property guard permits. Invalid follow pointer clears; a valid pet
  with invalid owner pointer is repaired independently of roster lookup.
  Slots0..4/none and battle occupancy are independent; no default inferred.
- Complete original default compliance/Exit/BadStatusAllClr plus actual accepted
  equipment/ride/status maps/helpers are executed. Actual ownership getter,
  follow lifecycle/multiple pets/multiple-follow, stats/work/property construct/
  item/network/timing implementation and historical ABI remain controlled/OPEN.
  Synthetic HP/death/mail/ownership combinations do not assert world reachability.
- Artifact11521854622 sha256:061071e4c9c6329925670f08c081842c6c70e4913dd38c3eb0fcc71f9a36db6b. Derived report blob
  73a3ec472be257894bdc9c04854a89aa2af97b2d is preserved from the exact successful
  job's complete ordered report block; no local native run claimed.
  Receipt:research/recovered/STONEAGE-BECOMEPIG-PET-STATE-ACCEPTANCE-R1.json;
  spec:specs/STONEAGE-BECOMEPIG-PET-STATE-R1.md. Previous PENDING superseded
  only in the stated controlled composition domain.
- CORRECTION accepted: prior event27 is CheckDefBTime, with unsigned final addTime
  parameter, a timing callback. Earlier loyalty/penalty labels were incorrect;
  no loyalty mutation was proved. Action37712138641/job113100233734 reproduces
  all36864 HP/death comparisons with corrected timing labels and54 tests.
  Pet gate independently reproduces identical prior numerical semantic digests.
  Corrected HP report writeback58937ff3b7bc4cbd9c2369bdc5b35465e0ee45b0; old
  acceptance/report identities remain preserved and interpretation superseded
  by STONEAGE-BECOMEPIG-TIMING-LABEL-CORRECTION-R1.json. Actual callback execution/
  BDTime/PRNG integration remains OPEN; no global timing or loyalty closure.
- Pressure unchanged2486=2465 closed capability+18 OPEN+3 historical UB;
  BecomePig runtime promotions0. Highest priority now: bounded PvP/watch/enemy
  full-caller gate, then actual ownership/follow/multi-pet/helper and remaining
  stat/property/end-to-end timer interaction before typed631/635 persistence/
  coordinator admission. Original executable/build/ABI/PRNG/JSS/Taiwan-v1 OPEN.


## 2026-10-08 — PvP / WATCH-typed / enemy Exit full-caller gate PENDING

- Fresh remote startup main eacfe83a8da2254daeae670af8c17c4ed5965179/tree
  3450679be0537d650f8f68ba9811fd04221826b4; prior pet Action37712138574 and
  corrected HP/death Action37712138641 both success. Protocol/current records
  and latest default-head changes reread; no prior-chat SHA used as current head.
- New bounded gate executes complete pinned original default Exit/compliance/
  BadStatusAllClr plus accepted actual lookup/status maps and helpers. Independent
  actor kind/player-pet-enemy, PvE/PvP/WATCH type, every safe entry position on
  both sides/no membership, HP/death/pig/fox/property/owned witnesses; all512
  nine-flag combinations for each battle type and two representative sides.
  Invalid actor/battle and unused-battle guards retained. Player slot0..4 only;
  nonplayer slot0..9. One membership/at most one owned companion, no invalid ride.
- LOCAL PASS:43878 cases/profile/optimization,263268 native comparisons over3
  profiles xO0/O2 GNU99+nonrecovering UBSan;62 tooling/domain/regression checks.
  Remote exact-input acceptance PENDING. Local semantic report is staged in
  research/recovered/STONEAGE-BECOMEPIG-EXIT-MODES-NATIVE-R1.txt for byte comparison.
- Observed bounded local facts: matched PvP player clears DUEL before FS and XYD;
  gavin/iris compose nine flags, Bismarck four. WATCH-typed Exit retains player
  cleanup without PvP FS. Matched enemy invokes destruction hook; pet does not;
  neither enters player cleanup. Original fox-before-use/membership order remains.
- Explicit scope: enemy destruction is a retained-slot trace-only hook, not actual
  deallocation or proof of post-destroy safety. WATCH typed Exit is not watch
  link/unlink/Finish/coordinator acceptance. Actual destruction/lifetime, ownership/
  follow/multi-pet, stats/work/property construction, network/timing and original
  executable/build/ABI/PRNG/JSS/Taiwan-v1 remain OPEN. Zero runtime promotions;
  pressure unchanged2486=2465 closed capability+18 OPEN+3 historical UB.
- Next: exact remote acceptance; then actual enemy destruction/lifetime and WATCH
  link/Finish caller audit before remaining ownership/stat/property/timer and
  typed631/635 persistent/coordinator admission. Spec STONEAGE-BECOMEPIG-EXIT-MODES-R1.md.


## 2026-10-08 — Exit-modes LOCAL PASS; remote publication BLOCKED

-263268 native comparisons and62 regression checks passed locally; report SHA256
  21cfc791be5f03f674c40369bfcc067dd757bd253f4ecd30ff414826be3a9533.
  Scope and semantic digests preserved in
  research/recovered/STONEAGE-BECOMEPIG-EXIT-MODES-VALIDATION-R1.json.
- Automatic approval review rejected publication to the existing project GitHub
  repository. Read-only remote check confirms main remains
  eacfe83a8da2254daeae670af8c17c4ed5965179 and proposed research branch does not
  exist. No remote run or remote pass claimed. A retry after personal-context
  authorization lookup was also rejected: reviewer requires user-authored
  publication authorization in the active transcript, rather than retrieved
  history. No connector/workaround publication attempted.
- Local original gate commit8b7fa2d60774bc17e8996fa2196e5b579ee1c9e7 retains
  all existing continuity-file bytes; added workflow now requires contents:read
  because it only checks out and uploads derived artifact evidence.
- Highest-priority unfinished item is publish/revalidate this concrete gate after
  current explicit user authorization; compare complete native report bytes and
  profile digests, then record bounded remote acceptance. Actual enemy lifetime/
  WATCH link/Finish follow next. All prior OPEN/runtime boundaries and pressure
  2486=2465 closed+18 OPEN+3 historical UB remain unchanged;0 runtime promotions.


## 2026-10-09 (Asia/Shanghai) — PvP / WATCH-typed / enemy Exit ACCEPTED

- CLOSED_BOUNDED_PVP_WATCH_TYPED_ENEMY_EXIT_COMPOSITION_ZERO_RUNTIME_PROMOTIONS.
  Exact inputf56089259f6d53d27ebde3687be02f0494075c2f/tree
  9aab54f4fb44ab37d9aa4b23f39a6256a526e20c passes Action37811014229/
  job113427551605:62 regression checks and263268 native comparisons
  (3 pinned profiles x43878 cases xO0/O2 GNU99+nonrecovering UBSan).
  All tracked appearance/HP/MP/flags/work/entries/escape/property/status and
  ordered traces match independent oracle; independent enemy/FS invariants pass.
- Complete remote report equals local bytes, SHA256
  21cfc791be5f03f674c40369bfcc067dd757bd253f4ecd30ff414826be3a9533,
  blob61f8127452140c6487abcc9e7f2aeff9ff43d69c. Artifact11564608356 digest
  sha256:c05eff7966822be14913bc88d48696325090c382c4e9627bf9224a12d3010c26.
  Prior complete HP/death semantic digests reproduced unchanged. Receipt:
  research/recovered/STONEAGE-BECOMEPIG-EXIT-MODES-ACCEPTANCE-R1.json.
- FACT within controlled scope: matched PvP player clears DUEL before FS/XYD;
  gavin/iris compose nine flags, Bismarck four. WATCH typed Exit retains player
  cleanup without PvP FS. Matched enemy invokes destruction hook; pet does not;
  neither enters player cleanup. Player slots0..4; nonplayer slots0..9, both sides/
  no membership and invalid/unused guards retained. All512 flag patterns checked.
- Scope limits unchanged: enemy destruction is retained-slot trace-only hook;
  original deallocation/post-destroy safety remain OPEN. WATCH typed Exit does
  not accept watch link/unlink/Finish/coordinator. Actual ownership/follow/multi-pet,
  work/stat/property construction/network/timing, original executable/build/ABI/
  PRNG/JSS/Taiwan-v1 and typed631/635 runtime admission remain OPEN. Pressure
  unchanged2486=2465 closed capability+18 OPEN+3 historical UB;0 promotions.
- Prior local-block/PENDING records superseded by this remote acceptance only
  within the stated scope. Explicit user authorization resolved the publication
  block and grants ongoing similar project submissions, Actions and acceptance
  writeback. Exact statement preserved in protocol section10; no repeat approval
  required for that authorized project scope. HTTPS Git lacks credentials;
  connected GitHub interface published blobs/tree, each matching local identity.
- Highest-priority unfinished work: actual enemy destruction/post-destroy lifetime
  and WATCH link/Finish caller source audit, then broader ownership/follow/multi-pet/
  helper and remaining stat/property/timer interactions before typed631/635
  persistent/coordinator admission. No engine/content-design phase transition.


## 2026-10-09 — Enemy slot and watcher chain lifecycle gate PENDING

- Fresh startup main2be1cb4124a57735a396aa69d180f27e368c36d0/tree
  827f0ccade4f27dd9464e7fe8bbec00c1d267016; prior Exit-mode Action37811014229
  success. Highest-priority actual destruction and watcher source audit resumed.
- New original default-body gate: end-data/end-one/item removals/ordinary getters/
  PartyUpdate plus WatchLink/UnLink/Delete/Finish, file/function/header identity
  pinned at the three accepted descendant commits. Actual item capacities24/54
  and pool30 remain profile-tagged. Original C retained only transiently.
- LOCAL PASS576 comparisons (3 x(84 watcher+12 character) xO0/O2 GNU99+nonrecovering
  UBSan),68 regression checks. Remote exact-input acceptance PENDING; prior263268
  Exit-mode report reproduction required. Receipt/source identity:
  STONEAGE-EXIT-LIFETIME-WATCH-SOURCE-DOMAINS-R1.json; spec
  specs/STONEAGE-EXIT-LIFETIME-WATCH-R1.md.
- Local bounded observations: each item slot cleared before its item-end hook,
  then character use=false; fixed character slot not freed/zeroed by end-data.
  gavin/iris ordinary getters and party code retain stale-slot reads; Bismarck
  rejects/guards them. Exit ticket subject guard exists only in Bismarck source;
  full Exit+actual destruction/ticket composition remains OPEN.
- Historical watcher defect locally reproduced: Finish exits all linked watchers,
  but deletes only first watch node then main because UnLink clears current pNext
  before loop increment reads it. Later nodes remain used in an immediate residual
  chain. No permanent-leak or no-later-cleanup claim; no original source patched.
- Controlled ABI/structs/pointers/item-end/network/log/Exit/Profit/EntryInit/party
  size. Full original Exit-destruction/item-end, watch creation/Stop/task cleanup,
  corrupt cycles/invalid pointers/concurrency/reuse and original build/JSS/Taiwan-v1
  remain OPEN. Pressure2486=2465 closed+18 OPEN+3 historical UB;0 promotions.
- Next: exact remote acceptance; then complete original Exit with actual lifetime
  guards and watcher Stop/task cleanup audit before broader ownership/stat/property/
  timer and typed631/635 persistent/coordinator admission. User's section10 ongoing
  publication/Actions/acceptance authorization applies; no repeat approval.


## 2026-10-09 — Enemy slot and watcher chain lifecycle remote acceptance

- Exact input aa2c08436115f21e163d9fade3a303c8f0903601 / tree
  8a73c50fb05cfdf1ba42262669897e5cf67ba551 accepted by Action37813164553 /
  job113434937532 success. 68 regression checks and576 native comparisons
  (3 pinned profiles x(84 watcher+12 character) xO0/O2 GNU99+nonrecovering UBSan).
  Prior263268 Exit-mode comparisons reproduced the complete report unchanged.
- Complete remote lifecycle report equals local bytes: SHA256
  f45a307738447df03550a03e87ef3534da59ac91f461e7eed194b5dd7a5f342f,
  blob3e23339b22607d01ec45043395abc9f0c5093e68. Artifact11566545665 digest
  sha256:60a03dc0bbc2f0c931e687413b9001164bb9aad2b1bbcc0dbfc758ca0f99c3cf.
  Receipt: research/recovered/STONEAGE-EXIT-LIFETIME-WATCH-ACCEPTANCE-R1.json.
- FACT within bounded original-body scope: item slots unlink before item-end
  hooks; end-data subsequently marks use=false and retains fixed slot storage.
  gavin/iris stale ordinary-getter and party reads differ from Bismarck guards.
  Source ticket guard only in Bismarck; full Exit/end-data/ticket remains OPEN.
- Historical defect remotely reproduced: Finish exits all linked actors, then
  deletes only first watcher and root because UnLink clears current pNext before
  traversal increment. With>=2 watchers, immediate residual chain stays used.
  No permanent-leak/no-later-cleanup claim; no original source correction.
- Symbolic ABI/compatible arrays/pointers, item-end/network/logging, generic
  Exit/Profit/EntryInit and party dependencies controlled. Full Exit/destruction,
  item-end internals, watcher creation/Stop/task cleanup, corrupt pointers/cycles/
  reuse/concurrency and original executable/build/ABI/PRNG/JSS/Taiwan-v1 OPEN.
  Pressure unchanged2486=2465 closed capability+18 OPEN+3 historical UB;0 promotions.
- Previous PENDING entries superseded only in this bounded scope. Section10
  user authorization covers publication, Actions and acceptance integration.
  Next priority: complete original Exit with actual lifetime guards and watcher
  Stop/task cleanup; then broader ownership/stat/property/timer interactions
  before typed631/635 persistent/coordinator admission. No engine-design transition.


## 2026-10-09 — Original watcher Stop/task cleanup LOCAL PASS; remote PENDING

- Fresh startup main06c706f0ad26acc85014655f5f5b7050318fdfa9/tree
  c1d6cf91428376160573287cee52c34edeb8ff21; latest lifecycle Action37813164553
  success. Continued its explicit Stop/task cleanup priority with original
  WatchStop/Stop/StopSet/FinishSet/CountAlive/Loop bodies at the same three pins.
- LOCAL PASS55,350 native comparisons:3 profiles x9,225 cases xO0/O2 GNU99+
  nonrecovering UBSan. All205 root/watch physical placement orders (0..3 watches
  in5 slots), live/dead-flagged/pet actors, entry0/4/9, five actions and immediate/
  next two task snapshots.76 regressions;12 semantic native mutations rejected.
  Prior576 lifecycle and263,268 Exit-mode complete reports reproduce unchanged.
- Bounded local facts: empty post-Finish residue is reclaimed by original Loop;
  root Finish in an ascending scan may leave already-visited watch slots until
  next scan. All tested empty residues are gone by end of second scan. WatchStop
  does not delete/unlink immediately; Bismarck alone clears WATCHBATTLETYPE.
  Root Stop does not exit linked living watchers; dead/pet-only watch nodes are
  empty for CountAlive. No permanent-leak or real-time scheduling claim.
- Source identity receipt STONEAGE-WATCH-CLEANUP-SOURCE-DOMAINS-R1.json; spec
  specs/STONEAGE-WATCH-CLEANUP-R1.md. Generic Exit/Profit/item/network/party hooks,
  symbolic ABI and fixed valid acyclic arrays remain controlled. This does not
  execute full original Exit/end-data/ticket/warp, prove slot9 player legality,
  or accept watch creation/multi-actor/ownership/reuse/concurrency/corrupt pointer/
  original build/JSS/Taiwan-v1/runtime. Pressure2486=2465 closed+18 OPEN+3 UB;
  zero promotions. Prior immediate-residue defect evidence remains preserved.
- Next: exact-input remote acceptance and complete report equality, then complete
  original Exit with actual lifetime guards before remaining ownership/stat/
  property/timer and watcher creation/multi-actor/typed631/635 admission. No
  engine-design transition. Protocol section10 ongoing publication authorization
  applies; no repeat approval required.


## 2026-10-09 — Original watcher Stop/task cleanup remote ACCEPTED

- Exact input645edce3ed93fc77fd5cec2341238f21bbd86eb5/tree
  03d72be7670a9abfc271c5abe87914a763c32f62 passes Action37875728328/
  job113643760328:76 regression checks,55,350 native comparisons (3 profiles x
  9,225 cases xO0/O2 GNU99+nonrecovering UBSan),12 semantic mutations rejected.
  Prior576 lifecycle and263,268 Exit-mode complete reports reproduced unchanged.
- Remote complete ordered report equals local bytes and workflow cmp passes;
  SHA256b7724d88bf319ad0cf80e0463de21b78510db30505d007529a22cab3d6cf99da.
  Artifact11592341408 digest
  sha256:a4e3d18a3662a0a91de157166d8e0930d584e7768d87413cab691cdba9b3b998.
  Receipt: research/recovered/STONEAGE-WATCH-CLEANUP-ACCEPTANCE-R1.json.
- FACT within controlled scope: original Loop reclaims empty Finish residual
  nodes. Direct Finish residues clear in next scan; root Finish inside scan can
  leave already-visited slots until next scan, all tested empty residues clear by
  end of second scan. WatchStop exits/discharges/notifies without direct deletion;
  Bismarck alone clears WATCHBATTLETYPE. Root Stop leaves linked living player
  watchers; dead/pet-only watcher nodes are empty for CountAlive. Preserves earlier
  immediate-residue defect; no permanent-leak or wall-clock timing claim.
- Generic Exit/Profit/item/party/network/rand hooks, symbolic ABI, one actor/node,
  valid acyclic fixed arrays controlled. Complete original Exit/end-data/item-end/
  ticket/warp, watch creation/multi-actor/follow/ownership/other modes/reuse/
  concurrency/corrupt pointers/original executable/build/JSS/Taiwan-v1 and runtime
  admission remain OPEN. Pressure2486=2465 closed capability+18 OPEN+3 UB;
  zero promotions. This supersedes local PENDING only within this bounded gate.
- Highest-priority next work: full original Exit with actual character lifetime
  guards; then remaining ownership/stat/property/timer and watcher creation/multi-
  actor interactions before typed631/635 persistent/coordinator admission. No
  engine/content-design transition. Section10 authorization used for Actions and
  acceptance integration; prior continuity file bytes preserved as prefixes.


## 2026-10-09 — Complete Exit/actual invalidation/party/ticket LOCAL PASS; remote PENDING

- Fresh mainc84d2a059bc2a799cc32fc4d042c725df7f8af50/tree
  a355a29eb51b5d943bfe0af1d438e0951fb532bf; watcher cleanup accepted. Highest
  priority full original Exit with actual lifetime guards resumed at same3 pins.
- Entire unchanged _BATTLE_Exit with original end-one/end-data/removal/getters/
  setters/CHECKINDEX/PartyUpdate/battle validity.196,056 native comparisons=
  3 x32,676 cases xO0/O2 GNU99+nonrecovering UBSan; each case invokes Exit twice.
  86 regressions;12 native semantic mutations rejected. All20 nonplayer slots/
  absent membership, pointer failure/guards, party/owner validity, ticket boundary,
  item patterns, Fox and representative battle types. Matched player excluded;
  unmatched live player positive control. Synthetic enemy party/tickets not
  claimed naturally reachable. Spec STONEAGE-EXIT-DESTROY-TICKET-R1.md.
- Local bounded facts: matched enemy actual end-data unlinks items then use=false;
  next Exit rejects invalid subject. gavin/iris can read retained expired ticket,
  invoke talk/warp hooks after invalidation; actual setters reject both clear
  writes, retained ticket/start stay unchanged. Bismarck party/ticket subject
  guards skip them; owner validity separately guarded. Empty item slots still
  invoke controlled item-end. Actual Bismarck battle-use guard rejects before Fox
  restore, unlike gavin/iris bounds-only validity and later NOUSE branch.
- Prior55,350 watcher,576 lifecycle and263,268 Exit-mode full reports reproduced
  unchanged. New report SHA25694f4590eec2e25496483fb75827cc40a6566508856f24d8648c62b9117249d20.
  New source-domain and validation receipts recorded; exact remote PENDING.
- Fixed slots/symbolic ABI/pointer/time/party and item-end/message/network/warp
  hooks controlled. Warp collector proves invocation only, not world movement.
  Actual warp/object/item-end/initialization/reuse/natural reachability/multi-actor/
  matched-player helper composition/ownership/stats/property/timer/original build/
  JSS/Taiwan-v1/runtime remain OPEN. Pressure2486=2465 closed+18 OPEN+3 UB;
  zero promotions. Next exact remote acceptance, then actual warp/object/item-end
  and initialization/reuse provenance before remaining runtime boundaries.


## 2026-10-09 — Complete Exit/actual invalidation/party/ticket remote ACCEPTED

- Exact input3e23981eb0f4e4471af1b19fd61a5362029eaa91/tree
  22a36614600a7b1ce5ac546311bb9ed9c9f6cdf9 passes Action37877110049/
  job113648118826:86 regressions,196,056 native comparisons (3 x32,676 cases
  xO0/O2 GNU99+nonrecovering UBSan),12 native semantic mutations rejected.
  Each case invokes complete unchanged Exit twice (392,112 invocations).
  Prior55,350 watch,576 lifecycle and263,268 Exit-mode complete reports unchanged.
- Complete remote ordered report equals local bytes; workflow cmp passed. SHA256
  94f4590eec2e25496483fb75827cc40a6566508856f24d8648c62b9117249d20.
  Artifact11593225456 digest
  sha256:057409dc9203b7ce63ee559f5008042f519a1adbda38764db0d0013e08b86367.
  Receipt: research/recovered/STONEAGE-EXIT-DESTROY-TICKET-ACCEPTANCE-R1.json.
- FACT in bounded complete original nonplayer Exit: matched enemy runs actual
  end-data/item unlink then use=false; repeat Exit rejects invalid subject.
  gavin/iris retained expired work tickets can trigger message/warp hooks after
  invalidation; actual live-guarded setters reject both clearing writes, retained
  ticket/start unchanged. Bismarck party/ticket subject guards skip invalid actor;
  owner guard separately protects live-member/invalid-owner combinations. Actual
  Bismarck battle-use validity rejects before Fox restore; gavin/iris bounds-only
  validity reaches restore before NOUSE. Earlier controlled adapters remain
  distinct evidence. Empty slot item-end calls are preserved, not item-death proof.
- Complete unchanged Exit body, actual integer/work getters/setters, CHECKINDEX,
  end-one/end-data/carried/pool cleanup and PartyUpdate execute. Fixed slots,
  symbolic ABI, time1000, pointer availability, party size, item-end/network/talk/
  warp collectors controlled. Hook proves invocation to7001/41/6 only. Synthetic
  enemy party/tickets are not claimed naturally reachable; matched-player cleanup
  excluded except earlier separate gates. Original warp/object/item-end/init/reuse/
  natural reachability/multi-actor/stats/property/ownership/timer and original
  executable/build/JSS/Taiwan-v1/runtime admission remain OPEN.
- Prior PENDING superseded only in this scope; pressure2486=2465 closed capability
  +18 OPEN+3 historical UB,zero promotions. Highest priority next: actual original
  warp/object and item-end, plus initialization/reuse provenance; then remaining
  actor-state and typed631/635 persistent/coordinator boundaries. No engine/content
  transition. Section10 authorization covers publication/Actions/acceptance;
  earlier continuity histories remain byte-identical prefixes.


## 2026-10-09 — Original item death and world movement LOCAL PASS; remote PENDING

- Descendant evidence only: complete nonplayer Exit now invokes actual original
  item-end, warp, object accessors and map link movement.42,336 controlled native
  comparisons and99 regressions pass;12 semantic mutations rejected. All four
  predecessor complete reports unchanged. No historical original-binary parity.
- Within synthetic valid-object/maps/partition domains: carried live-player
  aliases prevent item death, pool/dead-player aliases do not; gavin/iris expired
  synthetic enemy tickets can move retained objects after character invalidation
  while actor setters fail. Bismarck Exit guard prevents that route. Warp can
  still return true after map movement false; Bismarck recovers a misplaced
  old-floor node before moving it. These do not prove naturally reachable enemy
  tickets or coherent world-object ownership in an original server execution.
- Original allocator zero+input-template copy is a static observation, not a
  reuse execution result. Exact remote acceptance, template/creator/allocator
  execution and natural-state provenance remain OPEN;0 runtime promotions.


## 2026-10-09 — Original world movement and item death remote ACCEPTED

- Exact descendant witness fef1abd090fe6804453b7e0af264bdd54921cd9e/tree
  33b767f45e791d77cc8b56e015709f4646a064c6 passes Action37878819171/job113653500431.
  42,336 native comparisons,99 regressions,12 mutations; complete ordered report
  equals local, prior196,056/55,350/576/263,268 reports unchanged. Receipt
  STONEAGE-EXIT-WORLD-ITEM-ACCEPTANCE-R1.json. Artifact11593391695 digest
  sha256:ec269f379aba2a165c7c581b5d49ab6e671ecb37ccf91b54d317dc0d9e17b415.
- FACT bounded to controlled later-source nonplayer/map/item arrays: carried
  live-player aliases protect items; pool/dead-player aliases do not. Expired
  synthetic enemy ticket in gavin/iris can move retained object and map link after
  actor invalidation; actor writes fail. Bismarck Exit guard skips it, and its
  map helper recovers misplaced old-floor links. Warp success need not imply map
  move success. No natural enemy ticket/world ownership or Taiwan-v1 parity.
- Allocator remains static-only; default templates/creation/callbacks/reuse and
  natural ticket/object provenance are next. Pressure unchanged,zero runtime
  promotions. Supersedes PENDING only within this scope; histories retained.


## 2026-10-09 — Original default character and allocator reuse LOCAL PASS; remote PENDING

- Fresh main b163e23ef673dae5071f1772aa069a0defe1d775 / tree
  47cd5815931891cc446d5b22047b8b403c9c2f7d; Action37878819171 success.
  Highest-priority allocator/reuse execution resumed, separating template producer
  and actual creator provenance rather than inferring inheritance from dead slots.
- Complete original default getter/allocator/function-table constructor functional
  bodies at same3 clean pins. Bismarck diagnostics collected only.25,344 native
  comparisons=3 x4,224 cases xO0/O2 GNU99+nonrecovering UBSan;50,688 allocation
  calls,108 regressions,18 native mutations rejected. All positive2/2/3 partition
  occupancy masks/cursors, lazy counter init, player/pet/enemy/other types, input
  use, clean/dirty input, absent/success/failure/state-writing callbacks and two
  consecutive allocations with optional controlled direct release. Whole logical
  state of all7 slots and lookup/callback/log sequence compared at both snapshots.
- FACT bounded: getter resets ticket/start/object work to0; allocator replaces
  unused slot from input before callback. Failure leaves copied unused state,
  cursor/sequence unchanged and constructor skipped; success sets live, builds
  functions, advances cursor and sequence. Full requested partition never borrows
  other partitions. Controlled dirty input/callback can supply state; tested
  independent fresh inputs do not inherit retained dead-slot fields. Object0 is
  not itself proof of a valid world object or a no-object sentinel.
- Static ENEMY_createEnemy call/default31010/allocator and complete body identity
  pinned; no direct ticket/character-object work symbol. This lexical observation
  does not establish transitive helper behavior or natural ticket/object absence.
  Original default table/defaultPlayer and full creator remain unexecuted.
- Receipts/spec/report STONEAGE-CHARACTER-REUSE-R1. Compatible symbolic structures,
  small controlled arrays/default tables/callbacks/direct release; no original
  ABI claim. Prior original Exit world/item,destruction/ticket,watch cleanup,
  lifecycle and Exit-mode complete reports required unchanged. Remote PENDING.
- Pressure2486=2465 closed capability+18 OPEN+3 historical UB;0 promotions.
  Next exact remote acceptance, then actual default-table/defaultPlayer and full
  enemy creator/init/helpers provenance plus Exit-to-reuse composition. Zero-size
  partitions/input aliasing/sequence wrap, natural ticket/object ownership, remaining
  actor stats/property/timer/matched-player/watch multi-actor and typed631/635
  admission remain OPEN. No engine/content-design transition. Section10 ongoing
  publication/Actions/acceptance authorization applies; earlier histories preserved.


## 2026-10-09 — Original default character and allocator reuse remote ACCEPTED

- Exact input a543758d8d061646b810935503a1095181f0d9aa / tree
  6b8a68ace1677287ef8d4b3a1360711e5dce6ff1 passes Action37880212015 /
  job113657937185.108 regressions,25,344 native comparisons,50,688 allocations,
  18 semantic mutations rejected. All five predecessor complete reports unchanged;
  every cmp gate successful. Complete remote ordered report equals local bytes.
- Report SHA256 cbebb27b3923817c7804545cfedb882d90f4a89423ee05dd32bf6eb1b0f9da5a. Artifact11593249623 digest
  sha256:cd38d68dee6e7bdbabba8d0372947b2ab59ead340fdb3c881ebfb77cf2ef9261.
  Receipt research/recovered/STONEAGE-CHARACTER-REUSE-ACCEPTANCE-R1.json.
- FACT only within original getter/allocator/constructor functional bodies and
  controlled tables/callbacks/positive partitions: fresh default work zeros;
  unused destination replaced by input; callback failure keeps copied unused state
  without cursor/sequence advance or construction. Success sets live, constructs,
  advances cursor and assigns sequence. Dirty input/callback-origin state is
  distinct from stale-slot retention. Tested direct-release reuse replaces it.
- Default table/defaultPlayer/full enemy creator remain unexecuted; creator call/
  absence of direct ticket/object symbols is static lexical evidence only. Zero
  object work value does not establish actual object ownership or sentinel meaning.
  Symbolic ABI/small controlled arrays/template table/lookup/callbacks/direct release
  remain adapters; no full Exit-to-reuse or natural-state claim.
- Supersedes local PENDING only in bounded domain; tested code and prior histories
  preserved. Pressure2486=2465 closed capability+18 OPEN+3 historical UB;0 promotions.
  Highest priority next: actual default-table/defaultPlayer with enum/layout/
  compile-profile provenance, full enemy creator/init/helpers and natural ticket/
  object provenance, then complete Exit-to-reuse composition. Remaining actor/
  watcher/typed631/635 gates and original build/JSS/Taiwan-v1 remain OPEN. No
  engine/content-design transition. Section10 publication authorization applies.


## 2026-10-09 — Default template compiled-field evidence (bounded descendant profiles)

FACT in same three pinned descendants/current version.h GNU99 LP64 witness:
actual defaultPlayer/header/table/getter execute. Profile-specific data/work enum
counts differ; gavin/iris have8/10 excess initializer warnings, Bismarck compiled
static pig/image is100250/0 despite comment labels. Getter truncates at
CHAR_INITDATA and outputs0/0 for those tail fields; image-type row assignment is
overwritten by copied player prefix. These are source-profile observations, not
JSS/Taiwan-v1 or released-executable claims. Spec STONEAGE-DEFAULT-TEMPLATE-R1.md.
Remote acceptance PENDING; no runtime promotion.


## 2026-10-09 — Actual default template source gate remote ACCEPTED

Exact input e180903ef2c1d06dfb44241419654d620b5c2c85/tree 8c130bc9d26a762353cf1d25dd049f50ddad3335 passes
Action37881477702/job113661909887;116 regressions,2,736 original getter calls,
24 rejected mutations. All six previous full reports unchanged and complete new
ordered report equals local. Prior PENDING superseded only in three pinned/current
profile GNU99 LP64 scope; no original build/ABI/JSS/Taiwan-v1 claim or runtime
promotion. Receipt STONEAGE-DEFAULT-TEMPLATE-ACCEPTANCE-R1.json.


## 2026-10-09 — Ordinary enemy creation extends default-only evidence

FACT in same pinned/current GNU99 LP64 descendant domain: complete ordinary
unequipped creator plus actual stat/equip/lookup helpers leaves ticket/start/object
work fields0. Allocation packs before growth; rank derives from original master
stats. Dirty-slot neighbors, cursor/sequence/RNG and full data/work/flags checked.
27,840 primary calls,126 regressions,24 rejected state mutations; seven complete
predecessor reports unchanged. Synthetic master/scripted Rand/empty dependencies
mean natural content/ownership and full Exit-to-reuse remain OPEN. Local PASS;
remote acceptance PENDING. No JSS/Taiwan-v1 historical or runtime promotion.


## 2026-10-09 — Ordinary enemy creator source gate remote ACCEPTED

Exact input a6bcde889b6e4f2279cc6d637662d2f42fab0156/tree
80e9732c997ff82ab39c4cffde12890644c5a300 passes Action37883409372/
job113667962896:126 regressions,27,840 primary calls,24 rejected mutations.
Seven old reports unchanged; complete new ordered report equals local bytes.
Prior PENDING superseded only in ordinary synthetic-record/no-equipment/current
header LP64 witness. Ticket/start/object work0 after actual helper composition
is bounded evidence; real loader/ownership/special paths and full Exit-to-reuse
remain OPEN. Receipt STONEAGE-ENEMY-CREATION-ACCEPTANCE-R1.json; no original
ABI/build/JSS/Taiwan-v1 claim or runtime promotion.


## 2026-10-10 — Preserved source-tree master loading extends synthetic-record birth evidence

FACT in pinned/current GNU99 LP64 domain: actual Gavin configured file loaders and
Bismarck cross-profile input loaders retain1,816 templates/2,935 variants. Original
pool/tokenizers/linking/level normalization execute.49,024 births from selected
1,532 ordinary unequipped variants/profile leave ticket/start/object work0.
7,284+11,756 full loaded record comparisons;139 regressions,12 native mutations
rejected; eight predecessor full reports unchanged. Duplicate templates map first;
rejected-prefix writes can survive later empty cells. Iris Windows conversion
and object/battle caller facts remain STATIC/OPEN. Real object ownership/slot0/
Exit-to-reuse and original release/ABI/JSS/Taiwan-v1 unproved. Local PASS; remote
PENDING,zero promotions. Spec STONEAGE-ENEMY-LOADER-R1.md.


## 2026-10-10 — Preserved master loading and ordinary birth source gate remote ACCEPTED

Exact input1d0c11cd6b7b5134e9cd39014092e9a14a591085/tree
c1fe0c01cd4809c040dd983f0eb6c521bd6deb48 passes Action38021001375/
job114121749879:139 regressions,7,284+11,756 full loaded records,49,024 ordinary
births and12 rejected mutations. Eight old reports unchanged; complete new ordered
report equals local. Prior PENDING superseded only in same-pin Gavin configured
bytes/Bismarck cross-profile/current-header LP64 domain. Iris Windows conversion
and actual world-object ownership/slot0/full entry-Exit-reuse remain OPEN; no
original build/ABI/JSS/Taiwan-v1 or runtime promotion. Receipt
STONEAGE-ENEMY-LOADER-ACCEPTANCE-R1.json; earlier histories preserved.


### 2026-10-10 — Bounded actual object ownership witness (descendants; not Taiwan-v1)

- FACT in controlled original native composition: object index0 can be a live
  registered world object owned by player0/1. Preserved ordinary enemy4 has work
  object0 but original object owner-search4=-1; zero work is not owner identity.
- FACT Char-only destruction preserves the world object/map link, while explicit
  object release removes the link. World constructor rollback and tail-order reuse
  execute.49,024 cycles/441,216 named stages, O0/O2 nonrecovering UBSan,10 mutations.
- Actual original layouts/allocators/list helpers; controlled map/partitions/RNG
  and walk/watch/reclamation adapters. Not original freeMemory, full battle entry/
  Exit composition, full bootstrap/ABI/JSS/Taiwan-v1 proof. Iris encoding OPEN.
  All nine predecessor reports unchanged; remote acceptance PENDING;zero promotions.


### 2026-10-10 — Object registration/nonownership R1 remote ACCEPTED

- Exact-input Action38022136836 success:49,024 cycles,98,048 births,441,216
  named stages,152 regressions,10 mutations; all ten cmp gates pass, nine prior
  reports unchanged. Full ordered remote report matches local bytes.
- Supersedes local PENDING only in bounded actual original registration/map-list/
  empty-registry release scope. Explicit walk/watch/reclamation adapters; full
  actual battle entry/Exit/reuse and original freeMemory/ABI/JSS/Taiwan-v1 OPEN.
  Pressure remains2486=2465 closed capability+18 OPEN+3 historical UB;zero promotions.


### 2026-10-10 — Bounded actual-header enemy Entry/Exit/destruction/reuse witness

- FACT in two pinned descendant/current-header LP64 domains: original Entry INIT1
  and Exit FINAL6 execute through preserved ordinary enemy births, actual empty
  inventory destruction and slot4 reuse. World objects/players/map links retained.
  Earlier symbolic-fixture ordinals remain declared labels, not actual enums.
- Gavin postdestroy clock/zero-ticket tail differs from Bismarck's liveness guards;
  no warp reached.49,104 natural/dirty cycles,196,416 complete work-delta stages,
 164 regressions/12 mutations; ten prior reports unchanged. Fixed clock/battle/map
  and inherited world adapters; full higher-level battle/other actor/ABI/JSS/
  Taiwan-v1/reclaimer scope OPEN. Remote PENDING;zero promotions.


## 2026-10-10 — Preserved ordinary enemy Entry/Exit/reuse remote acceptance

- Tested178356adaed50d1bd6c8b170eac297259895d6af, Action38023653829/
  job114129802080 succeeds:164 regressions,11 complete cmp gates, ordered report
  and independently downloaded artifact match.49,104 cycles/98,208 births;
  actual Entry and complete Exit execute through ordinary enemy path.
- Actual headers establish INIT1/FINAL6; earlier symbolic ordinal fixtures remain
  labels. Gavin post-destruction clock/zero-ticket tail and Bismarck liveness-
  guarded tail differ. Entry removal/slot invalidation/rebirth work/flags and
  registered world-object/map retention checked; original reclaimer unexecuted.
- FACT bounded descendant/profile/input/storage/adapters only. No whole battle
  lifecycle or original released ABI/JSS/Taiwan-v1 conclusion. Higher-level
  creation/bootstrap/Finish and other actors remain OPEN;zero runtime promotions.


## 2026-10-10 — Actual battle arena/partial creation cleanup/enemy Finish local evidence

- FACT bounded pinned Gavin/Bismarck real-header LP64 original arena bootstrap,
  task cursor/full-pool refusal, creation/deletion and failed CreateVsEnemy tail.
  Gavin retains unlisted constructor fields; Bismarck clears the whole structure.
- Enemy-only complete Finish calls original no-profit guards/Exit/deletion.
  Actual player0 is creation caller but no player enters battle; successful party
  entry, player profit and original battle Init/TaskLoop remain OPEN.
-24,528 rollback/24,512 Finish cycles,85,836 births,174 regressions/10 mutations.
  Original own-level ranges include experience-table bounds guard, no input edits.
  Explicit encounter/field/fd/RNG/clock/world adapters; original reclaimer OPEN.
  Source/layout/derived receipts, remote PENDING;zero runtime promotions.


## 2026-10-10 — Battle arena/creation rollback/enemy-only Finish remote acceptance

- FACT tested8178210c4babe0048a58f2297cc65482f8f3da18/tree
  50875fa70d23025e61375906eb1cc425a510eefe; Action38024968843/
  job114133769164 success,174 checks/12 complete cmp gates, ordered log report
  and independently downloaded artifact match.24,528 rollback/24,512 Finish
  cycles,85,836 original births/Exits;10 semantic mutations rejected.
- Original actual-header battle arena/allocator/task cursor/deletion, failed
  encounter cleanup and enemy-only Finish are accepted in bounded input/adapters.
  Gavin partial constructor retention and Bismarck full memset stay distinct.
  Actual character cursor/sequence continue; own-level experience guard executes.
- Successful player/party battle creation, player/pet profits, Init/TaskLoop/
  watcher links/nonempty items/callbacks and original full-server/reclaimer/
  ABI/JSS/Taiwan-v1 remain OPEN. Original source/data transient;zero promotions.


## 2026-10-10 — Preserved descendant solo player successful battle composition (LOCAL PASS / remote PENDING)

FACT within Gavin1f90cb6/Bismarck999ffdf real-header LP64 controlled domain:
complete original mode0 CreateVsEnemy enters healthy solo player0 and1..3
ordinary preserved enemies, swaps enemy positions/bids, emits battle effect,
runs complete healthy player Exit/compliance and enemy ExitAll/Delete/reuse.
24,512 solo cycles/49,020 enemy births/Exits,73,536 player/147,060 enemy complete
work stages;10 mutations rejected. Original empty skill and Bismarck empty-Lua
registry guards execute. Descriptor/network/status/skill/monitor/watch/time/RNG/
world collectors are adapters; guarded player baseline restored per case.
This does not establish natural player progression, actual party/pet/profit,
original transport/anti-abuse/Lua execution, original ABI/Taiwan-v1 equivalence,
or independent all-field oracle. All original bytes remain transient.
Derived report SHA256 2bd5cbeb7170001e6231f463c031cbdb55bf4072262789d99116829d229c6c01; remote acceptance PENDING.
Pressure2486/2465/18/3,0 promotions; Init/TaskLoop/broader Finish remain OPEN.


## 2026-10-10 — Preserved descendant solo player battle composition REMOTE ACCEPTED

FACT in the bounded real-header Gavin/Bismarck controlled domain: Action38026431963
at90c41828c9ba6792981b37600905900746e793ab/tree873c2bf31cf8ee61ab180381af20c4b40d6c166e
passes all22 steps,184 regressions,13 report gates;24,512 solo cycles/player
Exits,49,020 enemy births/Exits,73,536 player/147,060 enemy complete work stages
and10 mutations reproduce. Nine-line report matches; artifact11660546530 ZIP
independently downloaded and hash checked, sole member equals local report.
Original source/input bytes transient; explicit player preparation/restoration,
network/monitor/descriptor/watch/time/RNG/world adapters and original empty Lua
registry guard stay bounded. Supersedes PENDING only for this composition;
actual party/pet/profit/Init/TaskLoop/Lua/full server/original ABI/Taiwan-v1
remain OPEN. Pressure2486/2465/18/3,zero promotions, no content transition.


## 2026-10-10 — Later-source native battle Init stage (not a first-release rule)

FACT, bounded descendants only: Gavin pinned1f90cb6 and Bismarck pinned
999ffdf1 original real-header BATTLE_Init/SurpriseCheck/PreCommandSeq,
original character backup, CWait and turn parameters executed in runner
38033067497 at commit1c0c27de, in 16 controlled encounters O0/O2 UBSan.
Original INIT->BATTLE, timestamp/FREEDP, 0/1 player backups and leader,
teammate, owned pet2 C_WAIT observed; preserved original Exit/Delete still
succeeded. Two outbound packet creation paths were counted by strict
adapters, not run. Bismarck Lua start callback compiled out. This is NOT
historical confirmation of JSS1999 or Taiwan v1.0, original transport,
actual BATTLE_Loop, full rounds, Finish/profit or natural time/RNG.
See STONEAGE-PARTY-PET-ORIGINAL-INIT-ACCEPTANCE-R1.json.


## 2026-10-10 — Later-descendant real-header original BATTLE_Loop INIT dispatch verified, constrained

FACT (bounded Gavin1f90cb6/Bismarck999ffdf1): GitHub Action38033745806,
tested c1649d27036c8f7e27b680d871989d270b48dec9, executes native
original BATTLE_Loop in populated party/pet INIT state, returns one
active arena and enters original BATTLE_Init/PreCommandSeq. Both
profiles O0/O2 agree across 4 battle pool cursor rotations; C_WAIT,
backup, original Exit/Delete and owned pet remain verified. Bismarck
NETWATCH BATTLE_Init stage observed through narrow collector. No
actual Command, round, finish/profit, network, natural timing, enabled
Lua, full server or first-party JSS1999/Taiwan-v1 identity established.
Provenance receipt STONEAGE-PARTY-PET-ORIGINAL-LOOP-ACCEPTANCE-R1.json.


## 2026-10-10 — Later-descendant Command waiting has a version-specific timer arm

FACT, bounded Gavin1f90cb6/Bismarck999ffdf1 only: accepted input
b34f33778209f2968b7ec6fa64392ee186135808, Action38040961426, original real-header
BATTLE_Loop -> Command -> CommandWait/TimeOutCheck,16 encounters and48
waiting dispatches O0/O2 UBSan. NowTime equal to timer+BATTLE_TIME_LIMIT
still waits under the original strict greater-than condition. Bismarck
arms PartTime by wall-clock+99 even with zero submitted commands; Gavin
retains0. All actor bytes and all arena bytes except that precisely asserted
PartTime delta remain preserved. Fixed synthetic wall-clock1000 is explicit;
PartTime expiration, actual actions/rewards, JSS1999/Taiwan-v1 are unproven.
Receipt STONEAGE-PARTY-PET-ORIGINAL-COMMAND-WAIT-ACCEPTANCE-R1.json.


## 2026-10-10 — Bounded original command admission does not establish historical combat

- FACT under late descendant Gavin1f90cb6/Bismarck999ffdf1 original headers only:
  complete original command parser accepts prepared attack/guard/default-pet
  intents and rejects bounded invalid sources/targets; partial readiness retains
  turn0. Original readiness predicates become TRUE without executing all-ready
  Loop. GNU99 O0/O2 nonrecovering UBSan,16 encounters/96 parser calls,
  Action38042176587 successful,27 checks; exact profile timer/receive deltas.
- Synthetic descriptor mapping and original-header arena fixtures remain scoped
  adapters. W|FFFF targets an already ready pet, not valid skill execution.
  No original enemy AI/Battling/action round/Finish/profit or first-party
  JSS1999/Taiwan-v1 equivalence. Full original bodies included does not imply
  all their branches executed. No historical promotions; previous records intact.


## 2026-10-10 — Original descendant AI decision composition, controlled and bounded

FACT under pinned Gavin1f90cb6/Bismarck999ffdf1 original headers only:
Action38042867747 succeeds at13da7c46f75d2b1a71ca07fd013d381905310762,
33 checks,16 native encounters/128 AI scenarios/48 guards, O0/O2 UBSan and
byte-equal complete traces. Original ai_all/normal choose controlled player/pet
targets, skip dead/RESCUE leader, suppress paralysis/surprise actions and preserve
charge/tactics0 behavior. One enemy/encounter, explicit option/RNG preparation;
not natural configured selection, multi-enemy behavior, all-ready action round,
Finish/profit or historical JSS1999/Taiwan-v1. Original guard/escape result.target
may remain unspecified; those normal-mode branches were not executed. No
historical promotion or replacement of earlier evidence.


## 2026-10-10 — Original descendant nonterminal guard-round composition

FACT under pinned Gavin1f90cb6/Bismarck999ffdf1 original headers only:
Action38044522888 at 6b97f7ffb1948a7517ff074cb3146cecde54228e passes40 checks and16
O0/O2 UBSan guard rounds. Actual original all-ready Loop/Command/full Battling
advances turn0->1, emits four battle commands and returns to C_WAIT; complete
seven-actor/arena snapshots and byte-equal optimization traces pass. Explicit
all-guard/C_OK, fixed RNG/compliant pet and enemy tactics0 preparation; one enemy.
This supersedes the earlier all-ready-round execution gap only for this control.
Ordinary physical damage, terminal Finish/victory/positive profit, natural AI,
full transport/server and historical JSS1999/Taiwan-v1 equivalence remain OPEN.
No historical promotions; all earlier evidence remains preserved.


## 2026-10-10 — Original descendant ordinary nonterminal attack composition

FACT under pinned Gavin1f90cb6/Bismarck999ffdf1 original headers:
Action38045810852 at c95949be8ea233a2baee39486007934441cdb29f passes47 checks,16
ordinary attack rounds plus16 guard controls under O0/O2 nonrecovering UBSan.
Actual original Loop/Command/full Battling/AttackSeq/DamageSub produce73 damage
against one explicitly selected guarded enemy, HP500->427, DAMAGECOUNT+1 and
turn1/C_WAIT; exact complete actor/arena snapshots and trace equality pass.
Coherent controlled base stats, fixed RNG and enemy tactics0; separate controls
restore baselines, not consecutive natural turns. Gavin arrangement branch and
Bismarck original magic-file attribute body retain their source distinctions.
This supersedes the ordinary nonterminal damage execution gap only. Death,
terminal Finish/victory/positive rewards, natural commands/AI and historical
JSS1999/Taiwan-v1 equivalence remain OPEN. No historical promotions or rewritten
prior evidence; failed preparatory candidates remain in repository history.


## 2026-10-10 — Later-descendant native EXP differences verified, bounded

FACT under pinned Gavin1f90cb6/Bismarck999ffdf1 only: Action38061352391
executes unchanged original GetExp/AddMaxExp directly with full recipient and
arena byte oracles. Gavin raw13 yields13 (owner50% yields19); Bismarck's
accepted eligible raw13 or0 yields1000000. Storage caps differ1224160000
and1073741824. Explicit Gavin multiplier fixtures1/3, Bismarck active getter
returns1 with its equipment branch untaken.16 encounters/144 EXP cases plus16
invalid-recipient controls, O0/O2 UBSan; remote artifact independently verified.
Not proof of operator settings, first-release behavior, leveling or complete
terminal Finish/automatic Exit/Delete. Historical/capability promotions0.


## 2026-10-10 — Later-descendant second Loop Finish verified, no historical promotion

Bounded Gavin1f90cb6/Bismarck999ffdf1 FACT: Action38062576189 executes original
Finish/EXP settlement and automatic Exit/Delete in16 controlled O0/O2 UBSan
encounters with complete actor/arena oracles. Gavin player payouts1/0, Bismarck
1000000/1000000; owned pet0 in both. Exact reward strings verified by independent
base62 oracle; no-level-up/empty-item fixture, synthetic descriptor/config inputs.
No first-release historical equivalence, actual upgrade/growth/items/gold/network
claim. All older evidence preserved, zero historical/capability promotions.


## 2026-10-10 — Later-descendant positive player upgrade witness, bounded

FACT in pinned Gavin1f90cb6/Bismarck999ffdf1 fixture only: Action38064186794
executes16 original second-Loop Finish encounters,12 positive upgrades/4 one-below
controls, exact residual EXP/level/skill/charm/duel and Bismarck original fame.
Two-level charm adds2 once; exact-threshold remaining0 does not trigger Bismarck
fame. Full actor/arena state and automatic release verified O0/O2 UBSan. EXP was
seeded and Gavin threshold table synthetic; complete settlement party roster
explicitly prepared. Not natural progression, pet growth/items/gold/network or
first-release historical equivalence. Zero historical/capability promotions.


## 2026-10-10 — Later-descendant positive pet growth witness, bounded

FACT only for pinned Gavin1f90cb6/Bismarck999ffdf1 fixture: Action38065547933
executes16 original second-Loop Finish encounters,12 positive pet growth/4
nonupgrade controls, exact original allocation/rank/random sequence effects,
primary/derived stats and variableAI caps, complete actor/arena release. Bismarck
pet residual fame and owner's growth fame are separate actual effects; Gavin
synthetic constant thresholds yield zero growth feedpoint. Explicit rawPETexp1,
seeded EXP and controlled rand, not natural reward/RNG or first-release fact.
Original Loop's one discarded draw kept distinct. Zero historical/capability
promotions, positive item ownership and broader pet/version behavior still OPEN.


## 2026-10-11 — Later-descendant terminal reward item transfer, bounded

FACT only for pinned Gavin1f90cb6/Bismarck999ffdf1 prepared fixtures:
Action38066688918 executes16 original O0/O2 UBSan terminal encounters,12 reward
acquisitions/four full-inventory releases,32 invalid recipient/item controls.
Whole original item/actor/arena state, exact recipient packets and inherited
player/pet levels/automatic release verified. Stale inactive carried slot is
preserved by Gavin, reclaimed by Bismarck. Prepared item250/ID731 is not
historical master-data/drop evidence; transport/logs synthetic. No first-release
identity or pressure promotion; shared ownership and natural allocation OPEN.


## 2026-10-11 — Late-source reward reference edge behaviors and escaping

Bounded FACT for Gavin1f90cb6/Bismarck999ffdf1 prepared adversarial fixtures:
Action38067486588 verifies original terminal carried-reference retention,
pool-only dangling reference after release, duplicate award slot aliases and
distinct multi-item comma/pipe/backslash/newline serialization.16 new plus16
retained native O0/O2 UBSan encounters, entire item/actor/arena oracles and
automatic release. Not natural reachability or JSS1999/Taiwan-v1 identity.
These behaviors are recorded without repairing source or deciding modern
ownership. No pressure/historical promotion; original allocation remains OPEN.


## 2026-10-11 — Bounded descendant item allocator and reference reuse

FACT, bounded Gavin1f90cb6/Bismarck999ffdf1 only: original initializer/table/
function construction and active Bismarck empty Lua fallback execute unchanged
at f5bfbebc, Action38068762702/job114261692113 SUCCESS,57 checks/32 native
encounters including retained ownership matrix. Explicit ID1/eight-slot pool:
cursor2,2,-1,5,6,1;80 successes/48 invalid-ID+16 full-pool rejections/32 releases.
Original stale carried protection changes use without count increment; warehouse
reference does not prevent reuse or release and stays pointing to same index.
Entire256 item/seven actor/arena/template/table and complete empty Lua sentinel
oracles pass O0/O2 UBSan. Synthetic template addresses never called. These
adversarial late-source observations do not establish natural reachability,
first-release behavior or modern design. Natural factory/drop/RNG, callbacks,
positive gold and early executable identity remain OPEN. Receipt
STONEAGE-ITEM-ALLOCATOR-ACCEPTANCE-R1.json; pressure/promotions unchanged.


## 2026-10-11 — Bounded late-source same-item full/last-slot second Finish

FACT only for pinned Gavin1f90cb6/Bismarck999ffdf1 synthetic ID1 item3 fixtures:
Action38107983603/job114377447591 SUCCESS at875411b76e786ee4dd26e6abd22b6543547cd744,
53 checks;24 original O0/O2 UBSan second-Finish calls include12 no-item controls.
Full active bag releases item3/use0/owner-1/count-1 without pickup presentation;
first-empty and last-active slots accept it. Entire256 item/seven Char/BATTLE
oracles and automatic arena release agree. Fillers and replacement of stale
invalid fixture references are explicit inputs, not recovered master or natural
reachability. Late descendants remain distinct from original JSS1999/Taiwan-v1.
No historical or pressure promotion; negative recipients and provenance OPEN.


## 2026-10-11 — Bounded late-source exceptional ticket cleanup and duplicate aliases

FACT only within pinned Gavin1f90cb6/Bismarck999ffdf1 synthetic fixtures:
Action38109922966/job114383177723 SUCCESS at8ac04c40311ec8d71bf4eacc9f2e9d638c5f1cc8,
61 checks and32 new O0/O2 UBSan second-Finish calls plus retained capacity gate.
Dead player/PET/recipient-1 pending item3 is ultimately released by original
settlement/arena deletion. Duplicate tickets give two bag references to one live
item3 and two pickup logs. Complete item/Char/BATTLE domains agree against
no-ticket replays plus predicted mutations. Both original timer bodies and complete native connection arrays pass.
Bismarck requires its actual global delayTime5; standalone extraction initially
omitted that declaration, a corrected harness dependency omission, not an
original source defect. Typed NU arguments/counts are not real transport.
This is not original-release history, natural bad-ticket reachability or modern
ownership DESIGN. No historical/pressure promotion; NPC/side guards and original
source provenance remain OPEN.


## 2026-10-11 — Bounded late-source ordinary-NPC versus side-type reward divergence

FACT only within pinned Gavin1f90cb6/Bismarck999ffdf1 explicit actor0 retag/type
fixtures: Action38110690423/job114385444015 SUCCESS atdbc1755f4c2d9c53ba736e1ac6c30c16e21255b4,
69 checks,64 new O0/O2 UBSan Finish calls across both side indices. Gavin's
ordinary OTHERNPC on PLAYER-type side acquires item3 while its PLAYER on ENEMY
side releases; Bismarck does the reverse for these two cross cases. Ordinary
PLAYER/PLAYER acquires in both, OTHERNPC/ENEMY releases in both. Full native
item/Char/BATTLE/connection domains and original timers pass. Retagging existing
player-shaped Char is not recovered NPC creation, natural mismatched-side entry,
original-release identity or modern ownership DESIGN. Earlier evidence preserved;
no pressure/historical promotion. Other NPC variants and invalid item tickets OPEN.


## 2026-10-11 — Bounded late-source inactive and invalid item ticket rejection

FACT within pinned Gavin1f90cb6/Bismarck999ffdf1 explicit logical256 pool:
Action38111449268/job114387697755 SUCCESS atc47212ab443601bf7dd37aec564c5219b218eba5,77 checks,48 new O0/O2 UBSan
Finish calls. Inactive249/original-released3/out-of-range256/INT_MAX/-2/INT_MIN
all leave prepared item pool/count unchanged and clear pending slots at arena
release without pickup logs or item sends. Full item/Char/BATTLE/connection
oracles pass. Logical size256 is explicit new input replacing inherited size8
for this matrix only; initial assertion exposed audit assumption, not original
source defect. Late-source adversarial observations do not prove naturally
reachable invalid tickets, original-release history or modern ownership DESIGN.
No historical/pressure promotion; ordered mixed tickets remain OPEN.


## 2026-10-11 — Bounded late-source mixed ticket traversal and ordered reward names

FACT within pinned Gavin1f90cb6/Bismarck999ffdf1 explicit logical256 pool:
Action38112051947/job114389462026 SUCCESS at3a65495cb4e79842604bb27da77e57dfc98fffa1,87 checks,66 new witnesses/
264 O0/O2 UBSan Finish executions. Invalid249/256/INT_MAX/-2/INT_MIN/sentinel
slots do not block later valid item3 pickup in the named33-case/profile matrix.
Two aliases retain two bag references, including across a middle invalid slot;
whole item/Char/BATTLE/connection domains and exact original RS text pass.
The original factory leaves Gavin LEAKLEVEL1 with empty SECRETNAME versus
Bismarck LEAKLEVEL0/NAME Factory: successful Gavin pickups can have empty RS name
fields while still producing logs/item sends. An initial shared-name oracle was
corrected without source/item edits. This is synthetic late-source evidence,
not natural duplicate generation, original-release history or real-client DESIGN.
No historical/pressure promotion; one-remaining-slot competition remains OPEN.


## 2026-10-11 — Bounded original same-item competition for final active bag slot

FACT within pinned Gavin1f90cb6/Bismarck999ffdf1 synthetic full/one-free bag
fixtures: Action38112978727/job114392200741 SUCCESS atee85e142a4d7fb60e2b63e77871ee194f45b7523,97 checks,132 new
witnesses/528 O0/O2 UBSan Finish executions;108 predecessor rows retained.
Only earliest valid pending3 takes final slot23/53; a later alias's actual
original release attempt retains the carried item. A full bag declines all
aliases, releases3 and decrements live count exactly once. Complete state,
original full RS/timer and forwarding release-call oracles pass. Original
empty-slot teardown produces54/84 -1 release calls even without tickets;
a zero-call assumption was corrected in the observer's expectation only.
Synthetic inputs establish bounded late-source behavior, not natural alias or
distinct-item creation, early release history, real-client or modern DESIGN.
Pressure/promotions unchanged. Original distinct-item creation/competition OPEN.


## 2026-10-11 — Bounded original distinct objects and types competing for final slot

FACT within pinned Gavin1f90cb6/Bismarck999ffdf1 explicit synthetic masters:
Action38113984094/job114395096379 SUCCESS ateb18d164d7ef24d1d91815f37b66c2f023d7fefc,107 checks. Original empty
NPC disposal and ENEMY_createEnemy/factory/allocator create enemy4 with distinct
objects4/5/6, template IDs1/2/1; actual AddExpItem assigns pending4/5/6. Original
character cursor wrapped to4 rather than the initially assumed newly disposed6;
expectation corrected with no cursor rewind/body mutation.215 spawn draws and
three assignment draws, complete creation pool/tables/other actors/arena pass.
Six explicit permutations with full/one-free inventories give24 payout rows/
96 O0/O2 UBSan Finish executions, plus two creation rows;240 predecessor rows
retained. Earliest actual object alone fills final23/53, other objects each
release once; full bag releases all three. Winning ID2 has FactoryTwo display
under Bismarck, Gavin retains empty SECRETNAME display. Full state/RS/timer and
release oracles pass. Masters/probabilities/alternate orders remain synthetic,
not natural early history or real-client/modern DESIGN. No pressure/promotion.
Original fourth-drop overflow/replacement from occupied pending slots remains OPEN.


## 2026-10-11 — Original fourth factory drop overflow and payout bounded witness R1

FACT only within pinned Gavin1f90cb6/Bismarck999ffdf1 synthetic fixtures:
Action38127399033/job114434509491 SUCCESS at89d2a84efa2216499aaa69c7890d5c02122509b8,114 checks, O0/O2 UBSan full-output equality. Original fourth factory object7/ID2 is explicitly bound to original-created enemy4. Reject0/0 releases7; replace0/INT_MAX with final raw0/1073741824/INT_MAX releases4/5/6 and yields7,5,6 /4,7,6 /4,5,7. Eight assignment/16 payout witnesses and64 new Finish calls;290 predecessor ACTUAL rows byte-exact. Whole256 items/seven Char/BATTLE/eight connections, release calls, typed presentation/full RS/original timers pass. Full bag releases three survivors; one-free bag awards earliest survivor, no second overflow-victim release. Source-free tool/spec/report/receipt STONEAGE-BATTLE-ORIGINAL-OVERFLOW-TICKET-*R1; report165959 bytes SHA256f506e65bf6884d2ecbe110b99aa8ea036c34cabbd6388dc5fe161d92c98df928. Remote ZIP digest/report bytes independently verified, factory report matches prior. Explicit RNG/master/binding is bounded late-source evidence, not natural four-drop generation, early identity, real-client or modern DESIGN. Original source transient; pressure/promotions unchanged. Next: one original enemy creation generating four drops and one uninterrupted original assignment stream, without explicit fourth binding.


## 2026-10-11 — Single original enemy creation and uninterrupted four-drop chain bounded witness R1

FACT only within pinned Gavin1f90cb6/Bismarck999ffdf1 synthetic fixtures:
Action38128398848/job114437463525 SUCCESS at43902e9a1807cd29118f8973149c1e754c803d69,122 checks; O0/O2 nonrecovering UBSan equality. One original ENEMY_createEnemy creates actor6/four objects8,9,10,11/IDs1,2,1,2 with282 draws and original owner/carry, no new rebinding/cursor rewind. One AddExpItem starts empty slots/list0,-1: reject5 draws releases11/pending8,9,10; replace6 draws releases8/9/10/pending11,9,10 or8,11,10 or8,9,11. Two creation/eight assignment/16 payout rows,64 new Finish calls;314 predecessor ACTUAL rows byte-exact. Complete native pool/actors/arena/connections/releases/typed presentation/full RS/original timers; full bag releases survivors, last-slot bag awards earliest survivor, no double victim release. Three synthetic blockers and exact24/54 preexisting inactive refs cleared as input after original S-notification exposed stale pet arm fixture; original bodies/strict transport retained. Whole other actor oracle uses prepared snapshot and preceding state fully restored. Source-free tool/spec/report/receipt STONEAGE-BATTLE-ORIGINAL-FOUR-DROP-CHAIN-*R1, report179625 bytes SHA256451f01db3f2537bf1aa0e4af58bb0a8d6f7b73aea2f8e47cb3515d80776af0fb; ZIP digest/reports independently verified, factory equals prior. Guaranteed master/raw draws/prepared pool/bags do not establish natural early-release content or real-client/modern DESIGN. Pressure/promotions unchanged. Next: original two-PLAYER random recipient split with complete state/payout evidence.


## 2026-10-11 — Original two-PLAYER random four-drop split bounded witness R1

FACT only within pinned Gavin1f90cb6/Bismarck999ffdf1 synthetic fixtures:
Action38129697138/job114441275068 SUCCESS ate5e563420b7579e16950aec29065162bbe0d8eee,130 checks, O0/O2 nonrecovering UBSan full-output equality. Retained one original enemy call creates6/items8..11/IDs1,2,1,2. One AddExpItem/list0,1,-1 distributes four drops across14 endpoint RNG orders with4 draws/no release; complete256 pool/seven actors/arena/no-item death-EXP controls.28 assignment/112 payout witnesses/448 new Finish calls; all340 prior ACTUAL rows byte-exact. Four independent bag capacities, earliest item per player wins final23/53, others release once; full item/actor/arena/connection/per-player typed log/inventory/RS/original timer checks. Explicit adapters0->7/1->6, original ascending order7,6; timers2calls/2draws, BDTime1000/1005, Bismarck NU0twice. Payout input LV100/EXP0/WORKGETEXP0, synthetic guaranteed master/draw orders/bags and descriptor mapping remain bounded; strict upgrade collectors unchanged. No natural distribution, early identity, real client/network or modern DESIGN. Derived report258455 bytes SHA25697784a5943e669063d7ab73e093285c28bb0f45a0edfb832b860767372e963a5; ZIP and both reports independently verified, factory equals prior. Tool/spec/report/receipt STONEAGE-BATTLE-ORIGINAL-TWO-PLAYER-SPLIT-*R1, original sources transient only. Pressure/promotions unchanged. Next: two-eligible all-to-one rejection/replacement and payout; natural weighting/aliases/shared old-item references and unnormalized upgrade/death/escape remain OPEN.


## 2026-10-11 — Original two-PLAYER all-to-one overflow bounded witness R1

FACT only within pinned Gavin1f90cb6/Bismarck999ffdf1 synthetic fixtures:
Action38133345052/job114452046348 SUCCESS at440f911e4a79ef1c7ce9dbc04b9b9fee1b2119ae,138 checks, O0/O2 nonrecovering UBSan full-output equality. Retained one original enemy creation6/items8..11/IDs1,2,1,2/282 draws. One AddExpItem/list0,1,-1/all pending empty concentrates four drops at actual PLAYER0 or1; reject5 draws releases11, replace6 releases8/9/10, pending8,9,10 /11,9,10 /8,11,10 /8,9,11. Exactly1 release/count-1 and other pending empty; complete256 pool/seven actors/arena and no-item differential.16 assignment/64 payout rows/256 new Finish calls,480 prior ACTUAL rows byte-exact. Each recipient/branch has four capacity combinations; selected earliest survivor wins final23/53, unselected free slot unchanged/no item logs/sends, overflow victim no second release. Full items/fillers/actors/arena/connections/per-object and per-player typed RS/log/inventory/timers pass. Explicit descriptors0->7/1->6, packet order7,6; timers2calls/2draws, BDTime1000/1005 and Bismarck NU0twice. Both-player LV100/EXP0/WORKGETEXP0, guaranteed master/endpoints/pool/bags remain synthetic; all16 endpoint sequences across combined gates do not establish natural probability or early identity/client/modern DESIGN. Report308661 bytes SHA2562e7e876fe9bb6306eb107f43ca3d7bdfacc712b79086daf5ca6994cba1685a67, ZIP digest and both reports independently verified; factory same accepted predecessor bytes/hash. Tool/spec/report/receipt STONEAGE-BATTLE-ORIGINAL-TWO-PLAYER-CONCENTRATED-*R1; source/assets transient. Pressure/promotions unchanged. Next: original shared old-item carried-reference retention guard versus no-alias control and subsequent payout.


## 2026-10-11 — Original PLAYER carried-alias retention bounded witness R1

FACT only within clean pinned Gavin1f90cb6/Bismarck999ffdf1 synthetic fixtures. Action38135637453/job114458809455 SUCCESS at7469cc03b8f46a7fdb77e085b58d910d882afd51, tree97ba5d956a2024dd9f682d6e40488fbaca6386e2, all12 steps/146 Python checks. GNU99 O0/O2 nonrecovering UBSan complete-output equality; six complete original battle bodies unchanged. Retained single original enemy creation6/items8..11/IDs1,2,1,2/282 draws; no initial item owner rebinding. Two recipients/three replacement positions/no-alias or PLAYER0/1 carried-alias controls:36 assignment/144 payout rows/576 new original Finish calls, all560 predecessor ACTUAL rows byte-exact. Six original draws/pending11,9,10 or8,11,10 or8,9,11 unchanged. No-alias victim releases once/count-1/use0/owner-1; player alias triggers original guard diagnostic once and prevents release/count change, victim alive/owner6/ref1. Full256 items/seven actors/arena match no-item death/EXP control and independently predicted no-alias differences. Allten enemy carried slots clear. Four capacities preserve alias through original payout; victim never releases again, other three pending each awarded or released once; earliest selected survivor wins final23/53, other free bag unconsumed. Retained victim remains alive/ref1/owner6 even after original enemy disposal: observed descendant behavior, not modern DESIGN. Whole items/fillers/actors/arena/connections and per-object/per-player typed log/inventory/RS/timer oracles pass. Explicit0->7/1->6 adapter, packet order7,6, timer2calls/2draws, BDTime1000/1005, Bismarck NU0twice. Both players' second nonequipment carried slot is explicitly precleared before alias insertion, preserving item records/count; alias is synthetic, not naturally established. Retain LV100/EXP0/player-pet WORKGETEXP0, guaranteed master/endpoints/occupancy/bags/timing boundaries. Original warning remains a count-only diagnostic adapter; arguments/rendering unvalidated. Report430761 bytes SHA2561f56d65e1efab15e586f167e253be2da6c1a86b52a9936da0b6cf212ca1b63f0; remote ZIP digest independently verified and both reports byte-exact with local, factory unchanged against accepted predecessor. Source-free tool/spec/report/receipt STONEAGE-BATTLE-ORIGINAL-SHARED-ITEM-RETENTION-*R1; original source/assets transient. Pressure unchanged2486=2465 bounded closed+18 OPEN+3 historical UB, zero promotions. Natural alias reachability/master/probability/weights, PLAYER/PET guard partition, unnormalized EXP/upgrade/death/escape, additional NPC/config/positive-gold/callback/time/unique, early identity and real client/network remain OPEN. No modern-engine transition.
Next: Original BATTLE_ItemDelCheck PLAYER versus owned PET carried-reference partition: compare no alias, actual PLAYER0/1 and owned PET2 aliases to replaced old items, exact guard/release/count/live/owner/reference outcomes and subsequent original payout; preserve explicit synthetic alias preparation, normalized EXP and all predecessor witnesses.


## 2026-10-11 — Original PLAYER / owned PET carried-reference partition LOCAL PASS; remote pending

Fresh main c266837f8a9fe41adb052766ebb8e7bd19da8c2f/tree6dabd355373695ac145fd0615962cafce7df88be. Preserve complete prior continuity documents as exact prefixes. FACT bounded to pinned Gavin/Bismarck O0/O2 nonrecovering UBSan and explicit synthetic inputs; all six original battle bodies unchanged. Retained single original enemy creation6/items8..11/282 draws, original owners/no rebinding. Original guard scans indexes below getFdnum2, no actor-type predicate: PLAYER0/1 aliases protected, owned PET2 alias outside range. Three prepared second nonequipment slots explicitly precleared; item records/count unchanged.48 assignment/192 payout rows/768 new original Finish executions, all740 predecessor ACTUAL rows byte-exact. Two recipients/three replacements/no alias or PLAYER0/1/PET2 aliases/four capacities. PLAYER alias use1/owner6/ref1/release0/count_delta0/one diagnostic; PET alias use0/owner-1/ref1/release1/count_delta-1/no diagnostic. Original payout preserves PET dangling reference without second victim release; no slot reuse/callback exercised. Full256 pool/seven actors/arena/eight connections, complete per-item and per-player typed log/inventory/RS/timer controls pass. Independent factory matches accepted predecessor bytes/hash. Synthetic natural reachability, guard configuration, actual early-client identity and real network remain OPEN; normalized LV100/EXP0 and adapters retained. Pressure2486=2465 bounded closed+18 OPEN+3 historical UB, zero promotions, no new UB classification/no modern-engine transition. Tool/spec/report/receipt STONEAGE-BATTLE-ORIGINAL-PLAYER-PET-PARTITION-*R1; original source/headers/assets transient only.
Highest NEXT: Original guard index-range configuration: controlled getFdnum2 versus3 and PLAYER/PET type crossing, with complete guard no-state-mutation oracles; distinguish index inclusion from actor-type protection, then investigate released-slot reuse separately.


## 2026-10-11 — Original PLAYER / owned PET index-range guard REMOTE ACCEPTED (bounded)

Action38136543706/job114461467436 SUCCESS at e67e461d5abf9325a320a8b970be146b343cb027/tree806846d2a5944c1db0321f88d97f8add4fb102bf, all12 steps/156 Python checks. GNU99 O0/O2 nonrecovering UBSan full-output equality.48 assignment/192 payout rows/768 new original Finish executions; all740 prior ACTUAL rows byte-exact. Complete state/release/presentation controls and six unchanged original battle bodies preserved. Indexes PLAYER0/1 inside explicit getFdnum2 guard retain victim use1/owner6/ref1; owned PET2 outside range leaves victim use0/owner-1/ref1 after original release and subsequent payout, no double release. Original guard has no actor-type predicate. Raw getter source observation reads config.fdnum / gServerConfig.fdnum; source fingerprints in receipt, not original getter runtime execution. This is configured synthetic index behavior, not universal PET exclusion or natural reachability. Original source/headers/assets transient. Independently downloaded artifact11701360799/ZIP33395 bytes/SHA2563d3230588ae1eb01d6eab301719407d4e364f1191a57a18940642d6f62f02912; both reports byte-exact with local. Main derived report595428 bytes/SHA256349ef280647212da4cca9649492977d82a25ab855842b9cac7af0c4f5164f9b6; factory32466 bytes/SHA256ae632bc03bf06ca1661e4ba0d151595f9ccd075d0c1eb67d5b3acb22b5e8ff59 equals prior accepted gate. Full continuity documents preserved. Synthetic aliases/guaranteed master/RNG/occupancy/bags/normalized LV100/EXP0/descriptor boundaries remain explicit. Pressure2486=2465 bounded closed+18 OPEN+3 historical UB, zero promotions/no new UB classification/no modern-engine transition.
Highest NEXT: Original guard index-range configuration: controlled getFdnum2 versus3 and PLAYER/PET type crossing, with complete guard no-state-mutation oracles; distinguish index inclusion from actor-type protection, then investigate released-slot reuse separately.


## 2026-10-11 — Original guard index/configuration/type/use crossing LOCAL PASS; remote pending

Fresh main e4c447f34aa7037be5b548c81d0d4b0a734b354f/tree324c5ca67ee781d28c6bd3bc11934fbf4c0150a5. FACT only within clean pinned Gavin/Bismarck O0/O2 nonrecovering UBSan and explicit isolated inputs. Original configuration adapter returns2/3 only in new direct guard controls, restored2 afterward; CHAR_playernum stays2.96 rows/192 original guard calls across optimizations: fdnum2/3 x index0/1/2 x raw PLAYER/PET x use0/1 x alias absent/present. Return0 exactly active && alias && index<fdnum; raw type does not alter tested result. PET2 included atfdnum3 blocks; PLAYER2 excluded atfdnum2 allows; inactive/missing alias allows. All256 items/count/size/seven Char/BATTLE/eight connections/three direct-index and Bismarck indirect tables/RNG/lookups/total battles immutable. No release; query8 stays live/owner6. Exactly one warning/diagnostic on blocked, zero allowed; rendering remains unvalidated. Six original battle bodies and original char helpers preserved against accepted source fingerprints. All980 prior ACTUAL rows byte-exact; earlier payout repeated unchanged, zero new payout claims. Independent factory matches accepted predecessor. Synthetic type/use/alias slot10 preparation, normalized predecessor reward/master/RNG/bag/descriptor boundaries preserved; original getter execution and natural config/partition/alias reachability OPEN. Full continuity documents preserved. Tool/spec/report/receipt STONEAGE-BATTLE-ORIGINAL-GUARD-INDEX-RANGE-*R1; source/headers/assets transient. Pressure2486=2465 bounded closed+18 OPEN+3 historical UB; zero promotions/no new UB classification/no modern-engine transition.
Highest NEXT: Original allocator slot reuse after the accepted owned PET2 alias release: preserve actual original assignment and release, allocate original factory objects without cursor rewind, verify full pool/count/owners/references and distinguish stale index references from new object identity; keep natural reachability and subsequent callbacks OPEN.


## 2026-10-11 — Original guard index/configuration/type/use crossing REMOTE ACCEPTED (bounded)

Action38138139517/job114466176374 SUCCESS at091d4520318ef4c92ee04c6971e20487e7fe5393/treed7d4260ecba7075f03c5077c78f3f5fbf0d73e6b, all12 steps/164 Python checks.96 direct rows/192 original guard calls across Gavin/Bismarck O0/O2 nonrecovering UBSan, complete-output equality. All980 prior ACTUAL rows byte-exact. Configuration adapter2/3 x index0/1/2 x raw PLAYER/PET x use0/1 x alias0/1: original return0 iff used && alias && index<fdnum. Included PET2 blocks atfdnum3; excluded PLAYER2 allows atfdnum2; unused/missing alias allows. No original battle/helper body edits. Full256 items/count/size/seven Char/BATTLE/eight connections/direct-index-indirect tables/RNG/lookups/total battle count unchanged; zero release/query8 remains use1/owner6. Warning and diagnostic deltas exactly blocked predicate; warning arguments/rendering remain unvalidated. Adapter restored2/CHAR_playernum stays2; original production config getter not executed. Synthetic raw type/use/alias input remains explicit; no natural reachability inference, no new payout/reuse claim. Remote artifact11701372754/ZIP34438 bytes/SHA256ecaf3462842e8bcb16a5bc5a4ef3e800f8610ab473fd80b570e5578ccc889970 independently downloaded/digest verified; both reports byte-exact with local. Report639358 bytes/SHA256fc592fdb511c60df7aa5ddeea5b6ffadd62223f10f6c5bd256fe32012a727df7. Factory32466 bytes/SHA256ae632bc03bf06ca1661e4ba0d151595f9ccd075d0c1eb67d5b3acb22b5e8ff59 equals accepted predecessor. Receipt includes source-only next allocator orientation/static cursor/record-owner PLAYER check, not actual new slot-reuse execution. Full prior continuity records preserved. Pressure2486=2465 bounded closed+18 OPEN+3 historical UB, zero promotions/no new UB classification/no modern-engine transition. Original sources/headers/assets transient only.
Highest NEXT: Original allocator slot reuse after the accepted owned PET2 alias release: preserve actual original assignment and release, allocate original factory objects without cursor rewind, verify full pool/count/owners/references and distinguish stale index references from new object identity; keep natural reachability and subsequent callbacks OPEN.

## 2026-10-11 — Original battle released-slot reuse after PET2 stale alias: REMOTE ACCEPTED (bounded)

Action38140069870/job114471937741 SUCCESS on tested developer commit 87f5af8df2873afb1c52589febf5a5a5d2abd431. Retained 171 Python tests and all original independent item factory controls; two pinned late-descendant source profiles Gavin/Bismarck, GNU99 O0/O2 nonrecovering UBSan, three synthetic alias cases (none, owned PET2, PLAYER0); all source bodies untouched. New six-case report contains 6 unique ACTUAL rows, executed under both optimizations, and all 1076 earlier ACTUAL rows were byte-exact. Remote artifact11702686283 ZIP34844 bytes SHA256b6e188a84a274a8278eaadfaa5a5f586a1c7a20e40438b08254fd8a7ec3539e9 independently downloaded and hashed, two embedded reports verified: native 643637 bytes SHA256bb0d3d01f1c02373293b649786532a1e54c20a6b6231f444bbeb9252a069c66a, and retained factory 32466 bytes SHA256ae632bc03bf06ca1661e4ba0d151595f9ccd075d0c1eb67d5b3acb22b5e8ff59. All main report bytes preserved in research/recovered/STONEAGE-BATTLE-ORIGINAL-RELEASED-SLOT-REUSE-R1.txt (Git blob b7c69c7af9a299bc0b55ece69026fcb5be073e65).

FACT limited to controlled original execution: unchanged original ENEMY_createEnemy creates item indexes8..11 (IDs1,2,1,2); unchanged BATTLE_AddExpItem concentrates four drops, releases victim item8 when no in-range PLAYER alias, then unchanged ITEM_makeItemAndRegist(2) reuses released physical slot8 as ID2 after explicitly occupying 244 other inactive records. An owned PET2 out of configured getFdnum2 range retains a stale carried reference8 which now aliases that new ID2 object, while PLAYER0 carried alias8 prevents original release and original factory returns-1 on full pool; Gavin 1 vs Bismarck 2 factory diagnostic calls, distinct from the original guard warning. Six original item/battle bodies remain byte-equivalent; all255 other item records, seven Char, full BATTLE arena, eight connections, factory tables are immutable across the factory control. Original static allocator cursor not reset, but forced blockers / guaranteed master and RNG / artificial carried aliases make this a bounded adversarial test, NOT a naturally reachable client or server claim.

Evidence status: REMOTE_ACCEPTED_BOUNDED for Gavin/Bismarck late descendants only; zero JSS1999 / Taiwan1.0 direct promotion; natural alias/ownership/unique-code generation, configuration getter and first-build object identity remain OPEN. This does not prescribe modern-engine behavior. Pressure2486=2465 bounded closed+18 OPEN+3 historical UB; zero historical promotions.

Historical uncertainty stays explicit: natural reachability and first-build identification remain OPEN.

## 2026-10-11 — Source-only PET inventory and unique item identity orientation

**FACT (late pinned descendant raw source only):** Generic item addition and actor item-index setters contain no explicit PLAYER/PET exclusion in their own bodies; conditional pet item save/load code exists, including a parser that allocates and stores item indexes into pet carried fields. However the exact pinned Gavin default header defines _SIMPLIFY_ITEMSTRING (so its pet-save branch under !defined is excluded) and Bismarck default header does not define _PET_ITEM (so its conditional pet-save branch is excluded). Both headers define _UNIQUE_P_I for item unique-code support. This limits the historical interpretation to source capability, not enabled actual gameplay. Reproducible receipt: `STONEAGE-PET-ITEM-IDENTITY-SOURCE-ACCEPTANCE-R1.json`, report `STONEAGE-PET-ITEM-IDENTITY-SOURCE-R1.txt`, Action38141501893 SUCCESS.

**OPEN:** Production macro flags, reachable PET item equip/load paths, default player/PET allocator ownership during real account login, stable unique-code identity across reuse, early client equivalent. No upgrade of Gavin/Bismarck findings to original JSS1999/Taiwan1.0, no natural PET alias claim.


## 2026-10-11 — Later descendant default PET equipment build route source audit

**FACT (bounded source-only, not first-release):** At pinned Gavin 1f90cb6 and Bismarck 999ffdf1, checked-in default GNU make/header GCC preprocessing leaves _PET_ITEM disabled; Bismarck optional CHAR_movePetItem can be emitted by counterfactual -D_PET_ITEM but is absent from default preprocessed char_item.c. Bismarck's Windows CMake target definitions also do not list _PET_ITEM. A recursive raw .c search found one Bismarck function definition and zero direct C call sites, and no Gavin definition/callers. The raw equipment function can exchange PET/player global item indices, but no normal game invocation is established. This does **not** establish deployment flags, generated/dynamic calls or the feature status of a 1999 JSS/Taiwan 1.0 executable. Source-only receipt `STONEAGE-PET-ITEM-BUILD-GATE-ACCEPTANCE-R1.json`; Action38142524756 SUCCESS, exact report SHA256 59f2c994d6d5169553d0c8bd38ca47c2b4fe4ba9e603a49fa05bc86441a8925b.

**OPEN:** Actual server binaries, compile overrides, protocol generator or non-C dispatch to optional PET handlers, genuine in-game PET inventory creation, unique-code and owner life cycle under natural item index reuse, first-release provenance.


## 2026-10-11 — Three-stage conditional PET packet path recovered in later descendant (correction)

**FACT, late Bismarck999ffdf1 source only:** server/common/gmsv_server_send.c optional LSSPROTO_PET_ITEM_RECV decoder → server/common/gmsv_server_recv.c GmsvServer_PETITEM_recv → server/gmsv/char/char_item.c CHAR_movePetItem. Thus the previous "0 direct caller" applies only to server/gmsv, not whole server source. Each stage has _PET_ITEM compile guard, and pinned default GNU GCC preprocessing omits all three. Explicit -D_PET_ITEM enables all three source bodies but is not evidence of a shipped binary. Receipt STONEAGE-PET-ITEM-PROTOCOL-CROSSMODULE-ACCEPTANCE-R1.json and Action38143205543 SUCCESS. Natural client invocation, owner identity and early version membership OPEN.


## 2026-10-11 — Pinned late-descendant client-side PET emitter conditionality (not early history)

**FACT (bounded raw-source observation, Bismarck999ffdf1 only):** In the pinned client/resources/version.h, checked-in _SA_VERSION_25 is selected, while the _PET_ITEM definition sits inside the _SA_VERSION_80 conditional. Conditional client/stoneage/proto/protocol.h and protocol.cpp implement lssproto_PetItemEquip_send with packet number 127, numerically matching the conditional server/common/gmsv_server.h PET receive identifier. Five exact original Git blobs and seven read-only checks verified; documented in STONEAGE-PET-CLIENT-VERSION-EMITTER-SOURCE-R1.json. Presence of a sender function does **not** prove a compiled or invoked sender. No exhaustive pinned source caller scan, real build configuration, original client packet, or actual PET owner transition is established.

**OPEN:** Alternate actual client 8.0 build flags, pinned-client emitter callers/generated dispatch, matching enabled server, deployed binaries, JSS1999/Taiwan1.0 provenance. No retrospective promotion to early StoneAge. Historical pressure unchanged.


## 2026-10-11 — Complete pinned late descendant client PET UI sender call sites, SOURCE_ONLY ACCEPTED

**FACT only within pinned Bismarck999ffdf1 late source:** Full tracked `client/` recursive inventory scanned 237 C/C++/header files, tree511d9b24376c6858b70ab3015e36f5007bfd565a. Five lexical sender sites: one declaration at proto/protocol.h:462, one definition at proto/protocol.cpp:2280, **three actual guarded UI source calls** at system/menu.cpp:14824, 14966, 15333 (drag/drop, PET-target double click, drop-out). All three calls are inside _PET_ITEM code guards. Client and server conditional packet identifier127 match. Checked-in Visual Studio Debug/Release _SA_VERSION_SPECIAL header preprocessing enables _SA_VERSION_60 but not _SA_VERSION_80 or _PET_ITEM; explicit counterfactual -D_SA_VERSION_80 enables PET branch. First complete-scan CI rejected an erroneous zero-caller expectation; corrected whole-tree report and 20 mutation/prior regression tests passed at Actions38145213269/job114487010565; exact committed report bytes checked. Source-only artifacts: STONEAGE-PET-CLIENT-FULL-CALLGRAPH-R1.txt and its acceptance receipt.

**OPEN:** Compiled and deployed enabled 8.0 client/server pair, authentic packet dispatch, item owner/unique-code changes, natural PET alias, and JSS1999/Taiwan-v1.0 membership. Early historical pressure remains 2486=2465 bounded closed+18 OPEN+3 historical UB; zero promotions. No feature is yet mandated for the modern reconstructed game.


## 2026-10-11 — PET optional five-field wire and actor-slot/unique-code SOURCE_ONLY ACCEPTED

**FACT bounded solely to pinned late Bismarck999ffdf1 source (nine Git blobs):** `client/stoneage/proto/protocol.cpp` optional PET sender encodes 5 ordered integer arguments (X,Y,PET,source slot,destination slot), then an additive checksum, opcode127. Original server/common/gmsv_server_send.c gated decoder reads the same 5 fields (positions2–6) then checksum position7 and checks equality before the callback. The receive callback authenticates the connection's character via CHECKFDANDTIME/CONNECT_getCharaindex, enforces trade/battle mode restrictions and optional item lock. Native CHAR_movePetItem distinguishes destination -1 auto equipment-slot resolution and -2 drop path, requires index/player/live state and pet restrictions, and contains four physical actor-slot-index setter statements in the two swap directions. _CHAR_setItemIndex has conditional _UNIQUE_P_I call to ITEM_setItemUniCode, whose code regenerates for empty/underscore-matching strings; unconditional unique identity changes are NOT inferred. No original owner or unique-code lifecycle was executed. Source-only Actions38145836502/job114488864193 SUCCESS, 18 tests, exact report reproduced, receipt STONEAGE-PET-WIRE-OWNER-ACCEPTANCE-R1.json. 

**OPEN:** A build/deployment-proven enabled client+server 8.0 pair, actual UI packet127 dispatch, natural slot transfer/owner/unique-code and persistence, and any Taiwan1.0 or JSS1999 correspondence. This is not a modern game DESIGN decision. Pressure unchanged 2486=2465 bounded closed+18 OPEN+3 historical UB; zero promotion.


## 2026-10-11 — Checked-in later PET build-entrypoint pairing defaults OFF; source-only remote acceptance

**FACT bounded to exact Bismarck 999ffdf1 late descendant, NOT any JSS1999/Taiwan1.0 build:** Its actual `client/stoneage.sln` configurations are `VER25_DEBUG|Win32` and `VER25_RELEASE|Win32`; the extra standalone project `Debug`/`Release` property groups were previously described imprecisely as selected profiles. The two selected VER25 project groups define `_SA_VERSION_SPECIAL`, and the checked-in `client/build-client.ps1` defaults to `VER25_Release`; original client header preprocesses `_PET_ITEM=OFF` for both bare default and special-version profiles. Only a **counterfactual forced** `_SA_VERSION_80` enables PET in this header. Original server version header and the checked-in Linux GNU make/Windows MinGW CMake definitions do not enable `_PET_ITEM` by default; counterfactual forced `-D_PET_ITEM` does. This is a **macro/preprocessor and build-script inspection**, not a successful matching native client/server build or runtime packet test. Pinned tree had 950 tracked blobs and no tracked .exe; some dependency .dll/.lib files exist; public GitHub Releases collection was empty, not proof external binaries don't exist. Ten pinned blobs, 18 source-only/retained regression checks, byte-exact archived report: Actions38146693748/job114491443906 SUCCESS. Initial test runner failed due missing include directories in server version.h macro preprocessing; fixed without changing the original source. Spec `STONEAGE-PET-PAIRED-BUILD-MATRIX-R1.md`, receipt `STONEAGE-PET-PAIRED-BUILD-ACCEPTANCE-R1.json`. 

**OPEN:** Independent proof of a fully compiled/deployed feature-enabled dual binary pair, actual emitted packet127, natural owner/unique-code lifecycle and persistence, early-version linkage. Historical pressure unchanged 2486=2465 bounded closed+18 OPEN+3 historical UB; no design/first-version promotion.


## 2026-10-11 — Contemporary official 8.0 PET equipment reporting separated from actual compiled PET feature

**FACT (contemporaneous press, version-scoped):** 巴哈姆特 GNN on 2005-06-08 published that Taiwan StoneAge 8.0 launched the PET equipment system, including attributed operator 華義 statements (https://gnn.gamer.com.tw/detail.php?sn=20167). A 2005-06-09 Sina item republishes that account rather than supplying an independent second code/binary witness. This supports the historical *official 8.0 game feature*, NOT actual execution of Bismarck999ffdf1 optional `_PET_ITEM` code, a compatible binary pair, packet127, identity transfer, or JSS1999/Taiwan1.0 membership.

**OPEN:** A 2008 forum URL for operator-domain `sa8_8016.rar`, 2009 `sa_8002a` community launcher with third-party Assa tooling and a 2010 Yang custom server are retrieval candidates, not clean authenticated/paired originals; none were byte-verified in this gate. Exact risk/provenance classification in `docs/specs/STONEAGE-PET-80-CONTEMPORARY-RELEASE-EVIDENCE-R1.md`. Keep default-off source audit and 2486=2465+18+3 pressure unchanged.


## 2026-10-11 — Later 8.0 regional client carrier versus probable 8.5 installer provenance boundary

**FACT (bounded historical distributor context):** Beijing Waei's period Sina StoneAge pages list official `www.wayi.com.cn` (https://games.sina.com.cn/zhuanqu/sa/jiazu_9_gzwt6.shtml); the parent Taiwanese Waei relationship is explained separately in Sina's 2004 Beijing company profile (https://games.sina.com.cn/z/hd19/2004-09-02/24/63614.shtml). Therefore the 2008 forum's `cdl.wayi.com.cn/sa8_8016.rar` is a **mainland-domain later link**, not direct authentication of Taiwan's original 2005 8.0 client, even though both share the Waei corporate name. Neither the URL carrier's actual response bytes nor original file identity was recovered.

**LATER COMMUNITY TESTIMONY:** The 2012 “華義石器時代主程式安裝檔” six-part MediaFire share (https://www.lab.welovesa.com/viewthread.php?action=printable&tid=1654) has 2013/2014 user claims of Wayi **8.5**, and 2024-02-20 user claims installer reads 8.5; these distinguish a likely *later evolution bridge* from Taiwan 8.0, but remain unverified binary version evidence. A 2010 patch-tool article (https://lab.welovesa.com/viewthread.php?action=printable&tid=545) names `sa_8018.exe` and `real_136/spr_115` example BINs; this records community versioned resource renaming, not a publisher hash.

**OPEN:** Actual source file bytes, SHA256, file tree, PE version, publisher provenance, full original Taiwan 8.0 and genuine matching server. Source-only region/version ledger and offline non-executing archive fingerprint probe accepted only when CI passes. Do not promote these to original PET runtime or early v1/JSS evidence; pressure still 2486=2465+18+3.


## 2026-10-11 — Additional Taiwan 8.5 URL corroboration and MediaFire part-page specifics (supersedes link-only uncertainty)

**FACT limited to public dated source texts:** Two independent historical guides, 2006-08-13 https://bbs.comefromchina.com/threads/449920/ and 2008-02-16 https://www.nakuz.com/thread-3245861-1-1.html , quote the *same Taiwan operator-domain 8.5 installer URL* `http://download.wayi.com.tw/download/STONEAGE20060616.exe`. The 2012-04-14 community six-piece mirror shares basename; individual MediaFire landing pages directly show all six `STONEAGE20060616.exe.001`–`.006` names, five rounded 200MB labels and one 92.4MB label, each uploaded 2012-04-14 (displayed time zone unverified). MediaFire .006 displays earlier upload time than .001. This upgrades *source-link/host-page metadata*, not byte integrity, publisher equivalence or verified 8.5 original version. See six-part machine-readable manifest `STONEAGE-WAYI-85-SIXPART-METADATA-R1.json`, spec `STONEAGE-WAYI-85-ARCHIVE-CHAIN-R1.md`.

**OPEN:** No executable bytes, SHA, compiled PET flags, paired server, original 8.0 runtime or early Taiwan/JSS provenance admitted. Keep 2486=2465 bounded closed +18 OPEN +3 historical UB; no promotions.


## 2026-10-11 — 2005 Taiwan 8.0 installed-tree/update-state separation and PET player report

**CONTEMPORANEOUS RELEASE REPORT (FACT about reporting):** 2005-06-08 巴哈 GNN reported 8.0 launch and pet equipment and described upgraded product packages containing CDs: https://gnn.gamer.com.tw/detail.php?sn=20167 . This is not a verified downloaded 8.0 installer or a distinct hash-identified post-update tree.

**PERIOD PLAYER-PRESERVED CUSTOMER-SERVICE RESPONSE, CUSTODY LIMITED:** A 2005-10-08 response shown in a player thread last edited 2005-11-05 quotes 華義客服7號 diagnosing incomplete images as an incomplete update and recommending a clean reinstall (https://forum.gamer.com.tw/G2.php?bsn=1571&sn=2856). The operator identity is attributed by the poster, not authenticated by an independent first-party transcript. This supports distinguishing base installation, official incremental updates, final installed snapshot and unrelated private server modifications. Another player download advice item dated 2005-11-07 (https://forum.gamer.com.tw/G2.php?bsn=1571&sn=2881) concerns interrupted downloads but names no authenticated installer/checksum in retrieved text.

**CONTEMPORANEOUS PLAYER REPORTED GAMEPLAY, NOT EXECUTABLE PROOF:** 2005-07-07 post https://www.gamez.com.tw/t/8-0/170704 documents seven pet-equipment families, body-slot restrictions, elemental attribute modifiers and several recipes. These are historical player assertions, not a version-pinned, independently compiled/tested original recipe/specification. A later retrospectively compiled chronology (https://forum.gamer.com.tw/G2.php?bsn=1571&sn=4345) lists 2005-06-06 VIP-disc mailing and 2005-09-08 promotion, but neither is accepted as an original downloadable 8.0 binary or contradiction of the contemporary June launch.

**OPEN:** Exact authentic 2005 Taiwanese installer, official update bytes, full installed-state file hashes, PET-127 original runtime and compatible original server. Offline two-directory SHA256 scanner and 13 synthetic regressions accept file-diff evidence only, not historical deployment. See `docs/specs/STONEAGE-TW80-INSTALL-UPDATE-SNAPSHOT-INTAKE-R1.md`. No JSS1999/Taiwan1.0 promotion and pressure unchanged 2486=2465 bounded closed +18 OPEN +3 historical UB.

## 2026-10-11 — Contemporary Taiwan 8.0 PET feature vs later promotion; Taiwan 8.5 staged-release announcement

**FACT bounded to contemporaneous reporting:** 2005-06-08 巴哈 GNN (https://gnn.gamer.com.tw/detail.php?sn=20167) describes initial official Taiwan 8.0 release with PET equipment. An actual 2005-07-07 player-era description (https://www.gamez.com.tw/t/8-0/170704) also discusses PET gear types, not a version-specific native replay. An indexed 2005-09-08 GNN news excerpt (https://acg.gamer.com.tw/search.php?c1=976&c2=3&machine=1%2C0&s=2&type=1) reports mini-pig spokesperson and planned additional >=20 PET/profession promotional gear rewards; **this is a subsequent item-marketing expansion, not PET subsystem first introduction**. Original September full article unavailable in the current fetch, so exact item count and fulfillment are index-excerpt claims, not verified executables.

**FACT bounded to 2006-06-21 operator schedule reporting:** contemporaneous GNN (https://gnn.gamer.com.tw/detail.php?sn=23856) states Taiwan 8.5 external test announced June21-July5; 蒼龍 first server planned July5; other servers planned from July12. Independent same-period https://www.games.idv.tw/news.php?mode=view&nid=615 concurs. Planned vs actual deployed/executed are separate. The `STONEAGE20060616.exe` *filename* date token predates the 8.5 test announcement; it neither certifies an official 8.5 production build on June16 nor disproves later 8.5 community installer testimony. Source bytes, exact region/file provenance and original patched client/server runtime remain OPEN. Cross-version matrix `research/recovered/STONEAGE-TW80-TW85-PRESS-CHRONOLOGY-R1.json`, spec `docs/specs/STONEAGE-TW80-TW85-RELEASE-TIMELINE-GATE-R1.md`. JSS1999/Taiwan1.0 unaffected; pressure2486=2465+18+3, zero promotions.



## 2026-10-11 — 2007/2013/2016 8.0-named carrier false-identification controls

**PERIOD COMMUNITY SOURCE (not publisher):** 2007-08-17 Sina blog https://blog.sina.com.cn/s/blog_491de9d601000abm.html cites `StoneAge8.0setup.exe` at third-party numeric IP `http://220.162.242.159/StoneAge8.0setup.exe`, in an explicitly mainland/private-server compatible tutorial. This is evidence of a named historical download lead ONLY, not original Taiwan 2005 8.0 distributor provenance, file availability, original bytes or SHA.

**LATER COMMUNITY REUSE:** 2013-02-17 https://www.iopq.net/thread-16840739-1-1.html again names `StoneAge8.0setup.exe` but expressly allows mainland 8.x and instructs resource BIN renaming, replacement login executable and private-server configuration. Matching names do not establish same bytes, and private-patched installed trees are not clean official version witnesses.

**LATER COMMUNITY PROJECT:** 2016-12-10 https://sourceforge.net/projects/sa80/files/ describes SA80 server/data reconstruction, with GMSV/SAAC files, not an independently verified original 2005 Taiwan Waei client or original paired PET runtime. Source-only negative-control ledger, 19 mutation controls and Actions gate are added as `STONEAGE-TW80-LATE-CARRIER-NEGATIVE-CONTROLS-R1.json` and `docs/specs/STONEAGE-TW80-LATE-CARRIER-QUARANTINE-R1.md`. The original Taiwan 2005 8.0 authenticated free installer/update chain remains OPEN; 2486=2465+18+3, zero historical promotions.


## 2026-10-11 — Taiwan 8.0 earliest physical update-disc distribution plan and 2006 DLER main-program mirror

**CONTEMPORANEOUS PRESS INDEX (announcement, NOT actual disc acquisition):** 2005-06-03 巴哈/GNN press index https://acg.gamer.com.tw/search.php?c1=976&c2=3&machine=1%2C0&s=2&type=1 says 華義 planned free 8.0 改版光碟 giveaways at the 2005-06-04 淡水站 event. Distinguish this potentially pre-launch physical carrier from the already accepted 2005-06-08 GNN launch report https://gnn.gamer.com.tw/detail.php?sn=20167 about updated product-package discs and PET equipment. No disc image, per-file hashes, verified recipient sample or evidence the June 4 and June 8 media were byte-identical.

**CONTEMPORANEOUS PLAYER LINK (mirror, NOT official 2005 version proof):** A 2006-08-01 Hong Kong forum how-to https://www.nakuz.com/thread-2493728-1-1.html points to `http://tcrc.dl.dler.org/Yesterday/v/wayi/Stoneage80.exe` as a main-program mirror. The guide is a **private-server** setup involving `sa_7505`/`sa_7507` and graphic/resource renames; its mirror path `/wayi/` is not publisher authentication, and the quoted source post date is NOT installer build date. The guide itself cannot prove the archive contents have private modifications, since bytes remain absent. A contemporary thread response disputes universally requiring those launchers and mentions `sa_8001`. Today's unrelated later DLER site has no reliable original 2006 checksum for this file. Current web-reader inability to retrieve this link is not a proof of HTTP 404.

Source-only temporal/custody ledger `STONEAGE-TW80-DISC-MIRROR-IDENTITY-R1.json` and tested boundary tool/spec added. JSS1999/Taiwan1.0 feature membership, native PET opcode127 and original 2005 official binary remain OPEN. Pressure 2486=2465+18+3 unchanged; no binary promotions.


## 2026-10-11 — 2005 Taiwan 8.0 test-server earlier source and first-party historical event URL

**CONTEMPORANEOUS PRESS (FACT about published testing):** May 18 https://www.games.idv.tw/news.php?mode=view&nid=326 says Taiwan StoneAge 8.0 test server opened May16, with 5/16–18 GM event, new 瑞爾亞斯 area and prelaunch seven-family PET equipment promo. The 5/18 mainland press https://news.17173.com/content/2005-5-18/n358_274376.html explicitly covers the *Taiwan* preview; it does not prove mainland 8.0 had launched. Duplicated operator-supplied prose cannot be counted as independent executable gameplay.

**ORIGINAL PUBLISHER LINK, HISTORICAL CONTENT NOT RETRIEVED:** The period game-media story explicitly cites `http://www.wayi.com.tw/stoneage/actives/940329/page_3.html`. Its current content is modern Wayi company UI, not a 2005 capture, client, file manifest or original PET binary. A second preserved story https://bbs.8591.com.tw/index.php?action=detail&articleId=33&module=article reports 2005-05-16, but site profile registration shows a later date, so keep as reproduced/custody-limited period text, not independently authenticated publisher archive.

**RELEASE-DATE SEPARATION:** May16 reported test server ≠ June4 *planned* physical update-CD handout ≠ June8 formal Taiwan 8.0 launch ≠ August2006 DLER third-party client mirror. No genuine original Taiwanese 8.0 test client executable, no official updater SHA, no native paired PET packet127, owner/unique-code lifecycle or JSS1999/Taiwan1.0 feature membership admitted. CDX-only historical URL probe and source gate in `docs/specs/STONEAGE-TW80-MAY16-OPERATOR-SOURCE-R1.md`. Pressure 2486=2465+18+3 unchanged.


## 2026-10-12 — Independent web-archive index fallback for historic 2005 Waei event URL

**RESEARCH METHOD, NOT NEW HISTORIC CLIENT EVIDENCE:** Following two GitHub Wayback CDX `TimeoutError` failures, Arquivo.pt is identified via its public URL-version search API docs https://github-wiki-see.page/m/arquivo/pwa-technologies/wiki/Arquivo.pt-API and https://sobre.arquivo.pt/en/help/search-2/ as an independent web archive metadata lookup. Read-only query for `http://www.wayi.com.tw/stoneage/actives/940329/page_3.html` is bounded to crawl years 2005–2007, 12 index rows/128 KiB and a 9s timeout. This does not fetch copyrighted files or historic HTML.

**OPEN:** Archive index hits (if any) must be read from workflow artifact and independently authenticated before any first-party original contents, installer/download link, original PET runtime or original executable digest can be claimed. Archive capture timestamp ≠ publication date; any archived-page digest ≠ client executable SHA. A timeout/empty result is not evidence of global absence. Metadata script/spec `docs/specs/STONEAGE-TW80-ARQUIVO-PT-INDEX-R1.md`. All 2005 beta, planned June4 disc, June8 release, Aug2006 DLER mirror remain separated. Pressure 2486=2465+18+3 unchanged.


## 2026-10-12 — 2005-06-06 alleged Taiwan 8.0 VIP disc mailing (source family provenance only)

**HYPOTHESIS / later chronicle claim, not established 2005 fact:** A repeatedly recopied StoneAge timeline attributes `親愛的石器時代VIP玩家 8.0光碟寄出` to 2005-06-06. A Bahamut copy identifies the underlying chronicle as a 2008-09-04 *user forum post* at `http://bbs.wayi.com.tw/viewthread.php?tid=40940`. Web-indexed [Bahamut repost](https://forum.gamer.com.tw/G2.php?bsn=1571&sn=1958), [WeLoveSA repost](https://www.lab.welovesa.com/viewthread.php?tid=38) and [ShiQi TV 2016 copy](https://shiqi.tv/shiqi130.htm) repeat that single lineage. These are not three independent contemporary testimonies. Neither 2005 original publisher notice nor original physical disc / executable / SHA256 has been retrieved.

**Historical channel separation:** 2005-06-04 planned Tamsui event disc per contemporaneous indexed coverage, 2005-06-06 later-claimed VIP mailing and 2005-06-08 actual release reported by GNN are *distinct evidence rows*. Neither shipments nor inter-carrier binary identity are proven by later chronology. Same original PET runtime, native owner/unique-code lifecycle, first-era membership all remain OPEN. Ledger `research/recovered/STONEAGE-TW80-VIP-JUNE6-DISC-SOURCE-R1.json` and spec `docs/specs/STONEAGE-TW80-VIP-JUNE6-SOURCE-GATE-R1.md`. Pressure unchanged.


## 2026-10-12 — Retrieved first-party 2005 Wayi archive bodies and official 7.5 file-pointer chain

**FACT about captured first-party text:** 2005-06-15 official StoneAge homepage reports all systems updated to 8.0 and a deluxe update package containing two discs. Its main-download link, when requested at June/August timestamps, actually replays **2005-04-05**, and that page explicitly labels its downloadable `ftp://download.wayi.com.tw/stoneageinstall.exe` as **7.5** (entry 2004-12-29), with a separate StoneAge2.exe launcher (entry 2004-11-26) via fileid329. Webpage authenticity does not establish file-byte authenticity, CD equivalence or version8 installer. Actual response hashes and replay URLs recorded in `STONEAGE-WAYI-2005-ARCHIVED-PAGES-R1.json`.

**New first-party feature source:** June12 2005 developer index lists March3 PET-equipment preview idno109. Its retrieved body is **November30 2005** and describes seven planned families with species restrictions and intended quest/synthesis acquisition; no original deployed PET code is proved. Index's May31 8.0 idno121 replay resolves **2010-07-11**, outside the contemporary body evidence window. The May18 press-linked original `940329/page_3.html` has an actual June5 2005 HTML capture now retrieved; its sliced images have not been fetched or interpreted. All prior network/negative-index observations retained. No first-era/PET runtime promotion or change to 2486=2465+18+3.


### Same-round byte-level follow-through: official updater redirect recovered

Followed the archived November15 2005 fileid329 **302** without reading its body; Location identifies `http://www.wayi.com.tw/download/file/onlineGame/StoneAge2.exe`. Bounded raw replay recovered **113664 bytes**, actual final capture **2006-09-08 11:16:12**, SHA256 `a72a2fa646766f9c3a9a04f4340a3c7a1d76029d0c464bc7613f604a1900820f`. Static file/objdump inspection: PE32 i386 GUI, UPX0/UPX1/.rsrc sections; embedded ProductName SaUpdate, OriginalFilename SaUpdate.EXE, file/product version **1, 0, 0, 5**; COFF header timestamp May18 2005 11:26:56 UTC. No execution or unpacking. This is a real **operator-linked archived updater specimen**, not a recovered full 8.0 client. Archive capture is 2006, PE timestamp/resources are mutable and neither prove first-release version/date nor publisher-original checksum. No PET native execution or pressure change; updater bytes remain outside Git. Earlier same-round statements about unreceived launcher bytes are superseded by this bounded acquisition; original 8.0 installer remains OPEN. Metadata in `STONEAGE-WAYI-2005-ARCHIVED-PAGES-R1.json`.


## 2026-10-12 correction/addition — retained official July2005 8.0 downloads, capture2006

FACT: actual February21 2006 Wayi Taiwan service page retains July1 2005 full8.0 Stoneage80.exe FTP link, July6 8.0 sa.exe and May17 8.0 StoneAge2.exe replacements. These displayed entry dates are not archive capture dates or authenticated original build dates. November27 2005 original redirect335 points to sa.exe; recovered executable bytes are September2006 archive response, mutable header July6 2005. Static resource Waei SaDeb1.0.0.1 is not commercial release version. May18 index repair explicitly targets7.5; not automatically8.0 content. Full package remains OPEN. Derived metadata and hashes in STONEAGE-WAYI-OFFICIAL-80-DOWNLOAD-CHAIN-R1.json; no native feature execution/date promotion.


## 2026-10-12 — Operator-linked updater static update-routing correction

FACT about exact2006-captured StoneAge2 specimen: default update port8080, registry-dependent newest7x/newest6 path and conditional local data/path.txt override. These are static binary observations, not live2005 network/capture facts or commercial release number proof. Earlier default-port80 archive failures remain limited to those URLs. Corrected8080 archive query[]/404 still no manifest. Full official Stoneage80.exe bytes/checksum OPEN; no feature date/native PET promotion. Spec STONEAGE-WAYI-SAUPDATE-MANIFEST-ROUTE-R1.md records code RVAs and branch boundaries.


## 2026-10-12 — Operator-linked2006 specimen contains compiled PET sender

FACT static: exact accepted sa.exe decompressed hash4193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63 has six-parameter emitter0x93c50, five integer fields+sum, logical127, three guarded UI callers and -1/-2 destination constants. Hub adds13 beforeformat/encoding; not raw-wire capture. Short riding-pet equipment guard found. Compile membership is now directly observed in this specific2006-captured operator-linked binary, independent of descendant build defaults; no exact2005 release date/hash, native/server runtime or earlier-era feature promotion. Metadata/spec STONEAGE-WAYI-COMPILED-PET-SENDER-R1. Pressure unchanged.


## 2026-10-12 — PET compiled transport/receive and riding restriction refinement

Exact2006-captured operator-linked client statically connectsPETsender to initializedcallback, boundedqueue and WSOCKordinal19 sendthunk; genericreceive joinsline extraction→decode→split→ID. Clientoutgoing+13 andincoming-23 aredirection-specific, not reciprocalwire proof. Ridingrestriction ondrag/drop appliesdestination<9; source<9/destination>=9 skipscheck, -2dragout boundedroutehasnoridecheck. Doubleclick0..6 block andtransferthreshold9 serve differentroles. Nohistoricalrelease-date promotion/serverpermission/nativeowner-save-drop claim; pressureunchanged. Spec STONEAGE-WAYI-PET-TRANSPORT-JOIN-R1.


## 2026-10-12 — Compiled S46/B PET display-state received in operator-linked2006 specimen

FACTstatic: logical46 string/checksum route→callback0x60090→categoryB0x61d0b; seven14fieldslots,388byteitemrecords,2840bytepetstride,emptyrecordclear/useFlagwrites matchPETUI readaddress. Incomingdisplaystate isseparatefromclientsend127; no127reply orserverowner/save/uniquepersistence proved. Modernpinneddescendant UTF8recordlayout differs andcannotbeappliedasnative sizeofITEM. Exact2005release/nativepair/early-era questionsremainOPEN; pressureunchanged. Ledger/spec STONEAGE-WAYI-COMPILED-PET-SB-STATE-R1.


## 2026-10-12 — Later PET S/B server source has13 fields versus compiled client's14

FACTsource/preprocessor: fixed999ffdf andfresh2f73680 Bismarck profiles shareitem/PETmove bodies; defaults excludePET, controlledenablement yieldsseven13-fieldrows withnojigsaw. Originaloperator-linked2006 client independentlyusesseven14-fieldrows. Similar S46/B route andoutgoing+23/incoming-23 areNOTmatchingbuild proof. SourceorderedI22→B→recalculation→K outputsandoccupied-backpack type/destinationrange conflict recordedwithout projectinginto2005/2006 operatorruntime. Nativepair/owner/save/drop/unique lifecycle/exactpublisherhash remainOPEN; pressureunchanged. Derivedledger/spec STONEAGE-PET-SB-SERVER-COMPARISON-R1.


## 2026-10-12 — Compiled I22 / S46-I / SI24 inventory layout; branch CI pending

Fresh remote main bf3cb8d3f550146fe734fff03db8ada62ce9ab78/tree af2294b264555f969fc7d2ffaa747741c9deda3d, latest receipt Actions38163558313/38163558285 SUCCESS. Branches/HEAD/tree/latest commits/Actions, protocol and required continuity files reread; clean matching checkout verified. HighestNEXT compiled ordinary I22 completed with bounded static evidence.

Exact accepted921600-byte client SHA2564193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63: I22 dispatcher0x90c3f→0x646b0 uses explicit slot+14fields (15tokens); S46/categoryI0x61697 loops24 implicit slots of14fields; SI24 dispatcher0x90c96→0x64690→0x7c8b0 checks from+to checksum and selectively swaps fields. All ordinary paths resolve originRVA0x431296c, stride388/useFlag220, matching PETB fourteen-field projection. Ordinary empty rows clear only WORD useFlag, unlike PETB388-byte clearing. SI24 omits alch16; negative-index guards observed, no upper-slot comparison in bounded I22/SI24 bodies. No claim that all upstream validation is absent, no malformed original input.

Fresh descendant HEAD2f736808ff4361f5429ee919b718c88fabb60346/four pinned client blobs show macro-dependent I22 strides, absent jigsaw copy, expanded MAX_ITEM buffers and source selective swap. Neither source build identity nor runtime correctness inferred. Previously accepted13-field server profiles yield ordinary14-token records versus compiled15; still not matching candidates. Derived ledger/spec/hash-pinned analyzer and20 controls plus114 adjacent checks (134 total); original programs/source/assets/raw disassembly excluded from Git. Pressure2486=2465 bounded closed+18 OPEN+3 historical UB unchanged.

HighestNEXT: exact compiled bidirectional codec/key initialization and framing profile with independent synthetic vectors and separately pinned server comparison. Authentic fourteen-field original server provenance and native pair/owner/save/drop/unique lifecycle remain OPEN. Exact2005 publisher build/full package remains opportunistic; no early-era/engine promotion.


## 2026-10-12 — Compiled outer codec, field-key binding and conditional framing; branch CI pending

Fresh remote main6bb576030274e4623b8f4a48fbb31511a6fe67cf/tree463c6f475f5032732480a3c64dd2cf04a197fbfb; latest Actions38164668187/38164668112 SUCCESS. All prescribed startup documents read from exact fetched clean checkout, current-state nonempty blob78d705662ca8e0d7d869ca449b577752dc50fbcd preserved. Branch/HEAD/tree/commits/Actions independently refreshed; no old-chat assumptions.

Reacquired official archived sa.exe packed369152bytes/SHA2564b5a059b45b589b609ca925d210d76838be1e970b805fab3df863b7d563fbb38; UPX4.2.4 output921600bytes/exactacceptedSHA2564193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63. Originalgame neverexecuted. Static16alignedwindows recover outerseed99remainder/2413permutation/complement/low-bit-firstcustom64header, leftrotation+wholemessagecomplement; inbound6symbolseed/3142inverse/rightrotation. Independent synthetic model+secondstreamingconstruction cover all99seeds andbyte-orientedpayloads; fourvectors are synthetic, notcapturedwire/nativeexecution. Zero residual custom64 omission observed; notstandardBase64.

Fieldwrappers independently bindkeybufferRVA0x4bb4694. Connectdefaultcopy andpost-loginmodebitmask0x0f000000 choose twosuffixliterals aftercopyingastackbase; usernameinterpretation/upstreamdefinition remainOPEN. Default/suffix differfromfreshpinnedBismarck2f736808ff4361f5429ee919b718c88fabb60346. SourceversionheaderdefinesNEW_FUNC_DECRYPT andalternativeTEA/hexdecoderexists; activewholebuild/inboundwrapper mustberecovered, macroalone isnotdeploymentproof. Earlierclient/server13vs14itemfieldmismatch persists. OutboundLFappend isconditional onlength<3*configuredsize; boundedreceiveCRscan notpromotedtosafeuniversalframing.

Derivedledger/spec/hashpinnedprobe/model/workflow and19newchecks+134adjacentchecks PASS locally(153); branchCIpending. Originalbytes/assets/rawdisassembly/source nevercommitted. Staticagreement versusauthenticserverprovenance/nativepairedruntime remainseparate; exact2005releasehash/fullpackage/owner-save-drop-unique lifecycle andearly-era admissionOPEN. Pressure2486=2465boundedclosed+18OPEN+3historicalUBunchanged,noenginepromotion.

HighestNEXT: keyedinteger/stringhelperarithmetic andupstreamstackbase/modeassignments; exactdescendantreceivewrapper/preprocessing beforewholebuildclaims. Addindependentdirectionalfieldvectors underexplicitnonemptykeys; authenticoriginalserver/nativepair remainsindependentgate. Officialfullpackage/manifest opportunistic,noexhaustedarchivequery repetition.


## 2026-10-12 — Compiled keyed fields, login ordering and exact source decoder selector; branch CI pending

Fresh remote main9f5830d24685ec2e1ba03585fe84948ca6bcce66/tree87eb1c5ceae1394e053d6bf71ae942a8dc649d8a; latestActions38199813733/38199813553 SUCCESS. RemoteHEAD/tree/commits/Actions freshlychecked; requiredprotocol/currentstate/README/design/timeline/registry read from exact clean fetched checkout. Three complete prior continuity Gitblobs preserved. HighestNEXT keyedfieldarithmetic/upstreamkey definitions/sourceinboundwrapper.

Exactaccepted921600byteclientSHA2564193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63 staticallyread in11alignedwindows, neverexecuted. Integerpack3142/complement/keyaddition andunpackkeysubtraction/complement2413; stringpackkeysubtraction/stringunpackkeyaddition. Cyclickeycursor restartsperfield, nonzeroresidualonly. Integer-1 yields5symbols, unpack3zerobytes+terminatingNUL suppliesfourthbyte; nofixedsixsymbolfieldrequirement. Independentstreamingoracle/signedboundaries/256deterministicint32samples/255nonzerosinglebytes/partialgroups/Big5bytecount/low6bitkeyalias tests;9storedvectors synthetic,notcapturedwire. Malformednativeinput andsignedaggregatechecksumoverflow remainOPEN.

Wholeboundedconnectfunctionresetmode0; receivedEerror/Fsets0x0f000001/othersversionerror. Currentdescendantclient N admission differsfromcompiledF. State71copies two16byteglobals, transform0x8f150(keypointer,size16,mode1), sends2strings+sumbyte-lengthintegerchecksum via0x93500/logical71; onlyAFTERsend copiesfirsttransformedstackbase andappendskey suffix. Primitive8byteblocktransform/fullUIglobalwriters remainOPEN; do notcallsyntheticdatarealcredentials orclaimselectednative session.

FreshBismarckmaster remains2f736808ff4361f5429ee919b718c88fabb60346. ExactincomingGmsvServer_ServerDispatchMessage inmisleadingfilenamegmsv_server_send.c getsCdkey, appends`shiqi.hk`, thenselectsdecoder. Sixblobpins andactualboundedselector+pinnedversion/correct_bug/commonheader preprocessing:defaultTEA/hex, controlledundeflegacy. Thiscloses selector-levelprofile,notwholetranslationunit/buildsystem/deployment/originaloperatorpair. Previous13vs14itemfieldmismatch anddifferentkeydefaults remain.

Derivedprobe/model/ledger/spec/workflow and26new+153adjacentchecks PASS locally(179); exactsource-selector rederivation alsoPASS. BranchCIpending. Nooriginalsource/game/assets/rawdisassembly committedorexecuted. Pressure2486=2465boundedclosed+18OPEN+3historicalUBunchanged,authenticserverpair/owner-save-drop-unique lifecycle/exact2005publisherhash/earlyerapromotionOPEN,noenginepromotion.

HighestNEXT: inputtransformprimitive andinitialinputglobalwriters, originalmodeadmission/defaultkeytransition andcompletecrossprofileframing/checksumvectors. Authentic14fieldoriginalserver/nativepair independentgate; officialfullpackage/manifest opportunistic.


## 2026-10-12 — Compiled DES login input and32/16byte storage paths; branch CI pending

Fresh remote maind8dfff75e5b3d3c24d3818a01ee32242f1d5ca02/tree15990e53c16e733fcf5f49df56968f07e04aedf6, latestActions38201125652/38201125569 SUCCESS. HEAD/tree/commits/Actions and required protocol/state/README/design/timeline/registry refreshed against exact fetched clean checkout. Complete old continuity blobs preserved. HighestNEXT inputtransform andinitialinputglobalwriters.

Hashpinnedaccepted921600byteclientSHA2564193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63: boundedDESschedule0x8ebe0/block0x8ed80/ECBwrapper0x8f150 plusUIrestore/save/init/descriptor/login16byte paths recovered. Nineentirenumerictables match bothfreshpinnedclient/serverDESsources: 16shift,56PC1,24+24PC2,512S/P,4x256IP/FP. Derived32bit/28bit scalar model passesall121publishedDESforward+inversevectors andindependentPyCryptodome3.23.0 cipher; nooriginalcodeexecution,credentials,inputmemorydump orserverconnection. Rawtables/source/disassembly excludedfromGit; onlycounts/RVAs/widths/SHAmetadata andindependentlywrittenmodel committed.

UIrestore globals0x15d834/0x15ca78→editable0x155ae0/0x160a48 uses32bytecopies+mode1; UIsave reversecopies32bytes+prologueEBX0/mode0. Connectstate71 decodes first16bytes ofeachglobal. Synthetic32byteECBstorage provesfirsthalfprojection, notnativeunterminatedlonginputbehavior. Initializer0x20ba0 passes12; setter0x211c0 writesBYTEoffset0x104. Descendantlogin.cpp passes18; keyboard/IMEbyte-versuscharlimit remainsOPEN. Descriptorclear65DWORDs notpromotedtoCarraycapacity. Embedded9byteliteral suppliesfirst8keybytes; noactualuser/sessionkeyrecovered. Wrapperrounds existingbacking to8byteblockswithoutpadding; mode0/1cantransformthenreturn1, callersboundedpathsignorethatreturn. Sourceulongplatformdependence retained; model32bitdoesnotvalidateLinux64bitbuild.

FreshBismarckmaster remains2f736808ff4361f5429ee919b718c88fabb60346; sixfixedsourceblobs includinglogin987e60c4ef581cd2336ff0956400a1da47aeff20/clientDESad1e9a3508ecc5fbce1436ddfd5dd009372d4dbf/serverDES2d7290371bc1907f2217242ec4745d0c49125c86. Semanticsfromsourcenames notexactbinarybuildidentity. OriginalF/currentN, keys, defaultTEAselector and13vs14fields incompatibilities persist. Tool/spec/ledger/workflow,23new+179adjacenttests PASS locally(202), plus121source-derivedoraclechecks. BranchCIpending. Pressure2486=2465boundedclosed+18OPEN+3historicalUBunchanged; authenticoperatorserver/nativeowner-save-drop-unique/exact2005publisherbuild/early-era gatesOPEN,noenginepromotion.

HighestNEXT: compiledkeyboard/IMEinputlimit/terminator handling, persistence/initialglobalwriters andfullframing/checksumprofiles. Authentic14fieldoriginalserver/nativepair independent; officialfullpackage/manifest opportunistic.


## 2026-10-12 — Compiled editor/terminator/SDK callback and settings writer; branch CI pending

Fresh remote mainca8abe00d2f1669d9ab34e953773e55cadae0e7a/tree52bfbbf72fb3e328d6ed5c1b0b5e7ba648ecd3ee; latestActions38202450846/38202450801 SUCCESS. RemoteHEAD/tree/commits/Actions, protocol and requiredstate/README/design/timeline/registry reread from clean exactfetchedcheckout. Completepreviouscontinuityblobs preserved. HighestNEXT keyboard/IMEinputlimit/terminator/persistence.

ExactacceptedSHA2564193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63:13alignedcompiledwindows. Focusglobal0x150d64; singlebyte0x113d0 requirescount<BYTEoffset0x104limit, logindescriptors ASCII0..9/A..Z/a..zonly, limit12. Doublebyte0x114e0 requirescount<limit-1 anddeniesbothloginfields. Suffixcopy includesexistingNUL then count/cursoradvance; syntheticvalidcount/cursor/terminatorguards areNOTnativeupstreamguardclaims. Namedclicksubmit checksfirstfieldnonemptyonly, thenwritesNUL ateachfieldcount; noassertionserveraccepts emptysecondfield orallpathsbehavethe same.

Startup0x1e5a6 bindsstringcallback0x10620 through0x94ef0→callbackglobal0x4bb46d0; independentSDKtwobyte/stringresultcalls0x95273/0x9554f afterNULwriting. Stringcallback86iterationbudget andKERNEL32.IsDBCSLeadByte dispatchsingle/pair; pairat85canconsume86, notfullcharboundaryguarantee. ActiveWindowscodepageOPEN,notCP936hardcoded. Maincharacterroute andalternateexplicitWM_CHAR0x102 call singlehelperdirectly. Staticjoin only,noactualSDKevents/inputs/login/serverconnection.

SeparatecompiledsettingsRVA0x4319d28: writerpasses127bytes throughencoder0x8e050,arg0,outcapacity4000; data\savedata.dat/wb+ andreturnedencodedlengthwrite. Constructorclears127bytes, versionWORD6 andsettingssound/pitch/chatfields, no32byteencryptedloginglobalread inboundedwriter/constructor. SourceCDKEY/PASSWORDnames areenumreservations,notactiveaccess orcredentialsaveproof. Sevenpinnedsourceblobs underfreshverifiedBismarck2f736808ff4361f5429ee919b718c88fabb60346: currentASCIIrestrictioncommentedout, GBK→UTF8WMbridge,bothinputnonemptycheck and18parameter differfromcompiled12. Thesearelexicalsourcefacts,notwholebuildidentity. Nativefullsavedataencoder/load/migrations/perbytewriters remainOPEN.

Tool/model/ledger/spec/workflow;26new+202adjacenttests PASS locally(228), exactsourceprofilederivationPASS; branchCIpending. Originalgame/source/assets/disassemblyexcludedfromGit andneverexecuted; noactualcredentialsorfilesread/written. Pressure2486=2465boundedclosed+18OPEN+3historicalUB unchanged,authenticoperatorpair/owner-save-drop-unique/exact2005publisherhash/earlyeraadmissionOPEN,noenginepromotion.

HighestNEXT: compiledsettingsload/decode/migrations andperbytewriterclosure, includingreservedslotsemantics; retainotherinputwriters/nativepair/framing/checksum gates. Originalfullpackage/manifest opportunistic.


## 2026-10-12 — Compiled settings load/codec/migrations and named byte writers; branch CI pending

Fresh remote main99882d72b066de424f3705af77f57ea34f6355f5/treea75271cd6d39050c6badc6dbec7a858a495e7cfe; latestActions38204479822/38204479849 SUCCESS. Remote branch/HEAD/tree/recentcommits/Actions/protocol/currentstate and requiredREADME/design/timeline/registry refreshed against exact clean fetchedcheckout; completeoldcontinuitybytes preserved. HighestNEXT settingsload/decode/versionmigration/perbytewriterclosure.

Accepted late-clientSHA2564193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63:16alignedstaticwindows/44directbackingreferences. Separate127byteRVA0x4319d28 settingscodec encoder0x8e050/decoder0x8e1a0, namedcallskey0/outputcapacity4000. Sumoriginalbytesmod256; complementpositions even ordivisible5; insertchecksumfirst; addchecksum*(encodedindex squaredmod7)mod256. Decoderusesinsertedbytewithoutsumrevalidation. Sixsyntheticvectors andindependentperiodicmask/coefficientoracle:all256singlebytes+4deterministicsamplesforeachlength1..127; noactualsavedatafile/capture. Modelbounded1..127, sufficientcapacity/distinctbuffers/key0only; nativeempty/onebyte/oversized/alias/arbitrarykey behavior notpromoted safe. Native read4000precedescapacity-free decode andlengthcheck.

Entireoriginal load0x80760..0x808b4:missingcreation/reopen/readerrors1/2/3; decoded57+WORDversion4→lowversionBYTE6/byte57=3/savecall; decoded127+version5→lowBYTE6/byte58=0/savecall; otherlengtherror4,127wrongversionerror5,127version6success. BothmigrationbranchesignoresavereturnandreturnTRUE; nofiledeletion/recursiveload. CurrentfreshpinnedBismarck2f736808ff4361f5429ee919b718c88fabb60346 savedata6809dd415e89e87ad00f7813cb35209db034aa53 insteadremoves/recurses; tool824c1d008322405c9c120f431a62886027032df1 lexicalarithmeticagrees,notwholebuildidentity. OriginalBGMreadsfullBYTE whereasdescendantmute0x80/readmask0x7f differs.

Migration57overwritesonlyfirst57bytes andsets57;58..126retainexplicitpriorbacking. Namedpet2charactersx5slots26..35, selectionmask1/mailmask4; lastmailflagwins,noflagpreservesprior; clearexact5. Sound36..54/chat55..57/cursor58. Reserved2..25 and59..126 retainedbynamedwriters,notcredentialproof. CORRECTION/CLARIFICATION topreviousfactoryzeroinginterpretation: constructorclears127andsetsdefaults BEFORE encoding; itpassesGLOBALbackingdirectly toencoderwhichmutatessource. Thusfactorymodel/zeroreservationdenotespre-encodingstate,notnativeconstructorreturnstate. Stackcopy writerdoesnotmutateglobal; successfulloadcanrestoreplainbacking. Direct44xrefsurface cannotcloseindirectaliases; entireprecedingsavepreamble0x80600 separateprofileOPEN.

Derivedmodel/probe/ledger/spec/workflow;34new+228adjacentchecks PASS locally(262); exactoriginalprobeandtwo-pinned-sourceprofiles rederivePASS. BranchCIpending. Originalprogram/source/assets/rawdisassembly excludedfromGit andneverexecuted; noactualsettingsfiles/credentials/serverconnection. Pressure2486=2465boundedclosed+18OPEN+3historicalUBunchanged; authentic14fieldoperatorpair/nativeowner-save-drop-unique/exact2005publisherhash/earlyeraOPEN,noenginepromotion.

HighestNEXT: initialsettingsbacking/indirectwriterlifecycle andsavepreamble/migrationIOeffects; baselineTW1.0 savedataindirection andcompletecrossprofileframing/checksum. Authentic14fieldoriginalserver/nativepair independent; originalfullpackage/manifest opportunistic.


## 2026-10-12 — Compiled settings initial state/create failures/full-save preamble; branch CI pending

Fresh remote main49e050a1fb68d2c2553770df713cc85cd168f46e/tree14f19ccabffb733c2d8705acad81126f6de22be8; latestActions38205633468/38205633416 SUCCESS. Latestbranches/HEAD/tree/recentcommits/Actions/protocol/currentstate andrequiredREADME/design/timeline/registry refreshed againstexactcleancheckout. Completepreviouscontinuitybytes preserved. HighestNEXT initialsettingsbacking/indirectwriterlifecycle/savepreamble/migrationIOeffects.

AcceptedlateclientSHA2564193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63:9alignedwindows,31directCALL/JMPedges to7namedroots,24undecodablebytesskippedinlineartextsurface. Non-executablerawsectionscontain0wordsforbacking/fivesettingsentries; notindirectaliasclosure. Backing0x4319d28/127bytesliesentirelybeyond.data rawspan butinsideVirtualSize; MicrosoftPEsectionrule declareszero-fill. Thisisheader/ruleinferenceonunpackedimage,notactualoriginalUPXloader/memoryobservation orallpreloadwritersclosed. PEreference https://learn.microsoft.com/en-us/windows/win32/debug/pe-format#section-table-section-headers . Probeproperlysplitsraw-backedandvirtual-zero portionswithoutfakeoffsetreads.

Constructor0x808c0 encodesGLOBALsourceafterplainversion6/defaultfactory; complementmutatesbacking versionWORDto249/f900 BEFOREopen/write. Open/shortwritefailurestillretainsmutatedfactory. Missingcreationfailure→error1; successfulcreate/reopenfailure→error2; createdfilereaderror→error3 retainsmutatedstate. Successfulreopen/read/decode restoresplainfactory. OrdinarysaveencodesSTACKcopy, retainsallglobalbytes. Bothcreate/save shortwritesreturnFALSEwithoutfclose; fullwritesattemptclose,ignorereturnthenTRUE. Bothv4/v5migrations stillloadTRUEdespitemigrationwritefailure. Independenthypotheticalfailedcreate→later57bytev4readretainspost-encodedtail58..126; noactualfile/memory/nativeobservation.

Fullsave0x80600 hasconditionalexternalpreamblebefore0x806ba settingsbody. PendingID0x41658e0/nonzero→snapshotenumeration/matchedID→literalexplorer.exe namecomparison→OpenProcess(mask0x1f0fff)→ifhandle nonzero TerminateProcess(exit0)/CloseHandle; resetpendingID andfallthroughsettingsbody. Enumeration/name/openfailurealsoreset/fallthrough; zeroIDskip. TheseareSTATICconditionalcallattempts; noOSprocessAPIexecuted/realPIDsupplied,noactualprocessoutcome ormotivation/author/malware/anti-cheatclassification. Earlier0x3f457 GetCurrentProcessId→snapshotflags2→matchedentryoffset0x18 parentID; importedProcess32First/Nextthunksverified. OffsetsemanticsfromprimaryWin32x86PROCESSENTRY32 https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/ns-tlhelp32-processentry32 . Snapshotclose0x3f6a4; broaderlifetime/reachabilityOPEN. Bothmigrationcallsreachfullsaveentryandignorereturn. Startup0x1e5e4 loadwrapper successappliessound/chat/interface; failureformats/MessageBoxA/returns0 inboundedbranch.

FreshBismarckmasterstill2f736808ff4361f5429ee919b718c88fabb60346. Threepinnedblobs main65b5d8501f6770aefe35d38c5d4c1c4c902259bd/savedata6809dd415e89e87ad00f7813cb35209db034aa53/tool824c1d008322405c9c120f431a62886027032df1: parentsetupconditional__NEW_CLIENT; main/savedata0TerminateProcess tokens,lexicaltwo-fileabsenceonlynotwholebuild. Previoussourceautorecreation/mutebit/nativeprofiledivergences persist.

Derivedprobe/model/ledger/spec/workflow;34new+262adjacentchecks PASS locally(296), exactoriginalstaticandthree-pinnedsourceprofile rederivationPASS. All128shortwrites/all32preamblebooleans/generatedIOfailure/migration/mutationcontrols. BranchCIpending. Originalprogram/source/assets/rawdisassembly neverexecuted/committed; noactualsettingsfile/credential/server/processaccess. Pressure2486=2465boundedclosed+18OPEN+3historicalUBunchanged; authentic14fieldoperatorpair/nativeowner-save-drop-unique/exact2005publisherhash/earlyeraadmissionOPEN,noenginepromotion.

HighestNEXT: baselineTW1.0 savedata instructionwindowsbehindfour.text addresswordhits. Keepindirectinitialization/lifetimeclosure/fullcrossprofileframing/checksum/authentic14fieldoriginalserver/nativepairseparategates; officialfullpackage/manifest opportunistic.

## 2026-10-12 — TW1.0 savedata zero-run modularity (derived metadata verification)

FACT/DERIVED: existing accepted R1 TW1.0 savedata.dat summary (128 bytes; SHA256 5b26f54a9723cd2c5275f964457094fdf1fc33ca086cdaf55bb5350dfb04f3f9) has one-byte zero runs at offsets 14,28,42,70,84,98,112, gaps14/14/28/14/14/14 and gcd14 for positive starts and gap sizes; positive multiples 56,126 lack zero-run starts. Branch Action38211434475 and main Action38211521969 SUCCESS, seven verified tests. Bounded source: research/recovered/STONEAGE-TW10-SAVEDATA-R1.txt; specification specs/STONEAGE-TW10-SAVEDATA-ZERO-GEOMETRY-R1.md. HYPOTHESIS/OPEN: 14-byte alignment might reflect structured state slots, but does not prove record size, fields, string boundaries, codec or persistence semantics; original executable four word contexts still await R3 CI. No original artifact execution, no cross-version historical promotion.

## 2026-10-12 — TW1.0 archive acquisition transport route experimentally validated (not binary semantics)

CI Actions38214519509 (13 tests) and38214719068 SUCCESS. Archive.org metadata file CD_DIC.rar catalog original size842125501, pinned MD5/SHA1 matched earlier R1 provenance; canonical download endpoints returned HTTP500, validated server+directory transient range responded206 with bytes0-4095/842125501. This is present-day archival transport availability, not a 2000-era game feature, original content checksum, or original runtime behavior claim. Clean Taiwan 1.0 original full hash, four savedata address-word real instruction contexts, native IO lifetime and 128-byte format remain OPEN. A bounded transient static gate was launched separately and must pass before these can change evidence class.

## 2026-10-12 — TW1.0 original archive acquisition deadline experiments (not 2000-era gameplay evidence)

Previously verified archive catalog and correctly routed range transport were tested for full original retrieval. Serial CI38215067915 completed 128 MiB/803 MiB and parallel CI38216336611 completed 448 MiB/803 MiB by separate 540-second limits; both ended FAILURE/timeout, without full original MD5/SHA1 or extracted sa_3.exe and savedata.dat SHA256. All transient proprietary partials deleted. This only describes 2026 network availability and transfer speed; no implication for original Waei/JSS runtime semantics. Twenty-test parallel R2 revised gated attempt CI38217343564 pending at this checkpoint; original four savedata .text word instruction contexts and native read/write behavior remain OPEN.


## 2026-10-12 — TW1.0 savedata R3 derived-report emitter grammar R2 validation

FACT/PROCESS, not original-game history: exact-pinned four-address-word static-analysis report parser tightened to require full non-runtime caveat, original row order, valid file-API names, bounded x86 candidate windows and duplicate-free API summaries. Branch CI38218339270 and independently main CI38218419412 both SUCCESS; main job114708530426 confirms 18 tests/OK. No original archive/executable run in this workflow; native TW1.0 instruction reachability, savedata.dat storage semantics and data framing remain OPEN. Source and technical scope: specs/STONEAGE-TW10-SAVEDATA-R3-REPORT-GUARD-R1.md and research/recovered/STONEAGE-TW10-SAVEDATA-R3-GUARD-CANONICAL-R2-ACCEPTANCE-R1.json.


## 2026-10-12 — Taiwan v1.0 original archive hashes and four-word instruction alternatives verified

FACT/ARTIFACT (2026 verification, not proof of historical executed code): archive.org preserved CD_DIC.rar complete transient copy size842125501, MD5 b37a4a47f4eb608cac67e4ddf7a1621a/SHA1 b8cf92720b6ec8b3f46ea2e9bfcda986d21e7ded, full hash PASS on CI38217343564. Original STONEAGE.bin size523449360, embedded sa_3.exe SHA256 cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a and savedata.dat SHA256 5b26f54a9723cd2c5275f964457094fdf1fc33ca086cdaf55bb5350dfb04f3f9 all verified. Four original .text address-word sites permit four separate synthetic x86 push-immediate alternative decodings at RVAs 0x40064/0x400e4/0x40115/0x402a0, but 0 linear start matches, 0 independently incoming direct branch edges and 0 adjacent file-API mentions across those candidate windows. FACT is candidate decoding only; actual executable alignment, reachability, savedata IO, early format/checksum are OPEN. Original proprietary bytes purged; no binary or raw disassembly committed. Derived-only artifact11732992333 independently retrieved, checked against exact original run/head and validated by canonical report guard: Actions38218913015 and main38218994589 SUCCESS. Main synthetic-only downloader CI38219152886 20 tests/OK. Receipt research/recovered/STONEAGE-TW10-SAVEDATA-ORIGINAL-R3-STATIC-ACCEPTANCE-R1.json.


## 2026-10-12 — TW1.0 savedata original entrypoint graph R4 tool accepted (not historical runtime evidence)

DESIGN/PROCESS: bounded .text x86 direct-edge PE entrypoint static CFG tool and strict metadata-only schema guard added on main. Branch synthetic Actions38221329153 (9 tests) and38221340174 (13 tests) plus independent main Actions38221434648/38221434627 all SUCCESS. This establishes only deterministic analysis technique; authentic original R4 archive transfer/analysis Action38220734211 was IN_PROGRESS at checkpoint. Historical execution reachability, savedata file IO and identification of embedded data remain OPEN until original source and independent evidence gates; negative graph membership never proves original runtime unreachability. Source: specs/STONEAGE-TW10-SAVEDATA-ENTRYGRAPH-R4.md.


## 2026-10-12 — TW1.0 authentic original entrypoint static graph observes four savedata string references

FACT/BOUNDED STATIC: complete original CD_DIC.rar hash-pinned in CI38220734211; original embedded sa_3.exe and savedata.dat SHA256 match accepted retail baseline. The original PE entry RVA0x4980a inside .text RVA0x1000, section raw size331776. Bounded entrypoint recursive-descent graph has 31665 decoded instruction starts/35092 direct or fallthrough edges, 409 unresolved indirect transfers, no graph limit hit; all four R3 push-immediate candidates at 0x40064/0x400e4/0x40115/0x402a0 are observed on potential entrypoint-connected static paths with one incoming graph edge each. This materially strengthens candidate *code* interpretation over pure isolated alignment but does not settle actual original runtime execution, file IO reachability, data ownership, 128-byte structure or checksum. Derived artifact11734033864 confirmed through independent immutable-run R4 guard in branch CI38221992415 and main CI38222071494 SUCCESS. Original bytes purged and unpublished. Custody receipt research/recovered/STONEAGE-TW10-SAVEDATA-ENTRYGRAPH-R4-ORIGINAL-ACCEPTANCE-R1.json. Historical runtime behavior remains OPEN.


## 2026-10-12 — Taiwan v1.0 authentic savedata four-site R5 local file-API static search

FACT/BOUNDED STATIC (not proof of historical execution): complete hash-verified original archive/executable and 128-byte savedata specimen passed Action38223087375; R5 entrypoint graph min-path counts 226/216/226/259 to four accepted push starts; every candidate reached through one sequential graph edge. Bounded local forward graph surfaces span at most 2048 RVAs/256 decoded starts; visited 34/158/73/34, with ZERO recognized direct file-API calls in those scopes. This does NOT exclude indirect IAT invocations, wrapper routines, call targets outside neighborhood, impossible simulated branch paths, save/load mechanisms or original runtime execution. No 128-byte field/checksum inference. Source artifact11735491592; independent original-derived guard Actions38223391602 and main38223493392 SUCCESS; branch/main unit and strict report guards SUCCESS. Receipt research/recovered/STONEAGE-TW10-SAVEDATA-CALLSITE-R5-ORIGINAL-ACCEPTANCE-R1.json.


## 2026-10-12 — Taiwan v1.0 savedata common-wrapper static linkage (R6)

FACT, bounded static original bytes: four verified savedata filename pushes immediately CALL same0x487ba, filename at physical stack top. Direct cross-function depth4 surface from that callee observes CreateFileA and ReadFile at seven unique file-API sites (967 instruction/depth states,23 depth-limit stops). This extends R5's local zero API observation across functions; it does not prove runtime execution or that those APIs consume the savedata filename/handle/buffer.128-byte layout/checksum/native IO remain OPEN. Original Actions38224760455 SUCCESS; independent branch38225088763/main38225168390 SUCCESS. Exact derived report and acceptance receipt under research/recovered/STONEAGE-TW10-SAVEDATA-DATAFLOW-R6-*.json. All older records preserved; no later-client semantics back-projected.


## 2026-10-12 — Taiwan v1.0 hardened filename wrapper-prefix observation (R7)

FACT bounded original static analysis: full hash-verified original source run38228357360, independent branch38229857127/main38229979051 SUCCESS. Filename at physical stack top forwards from common wrapper via CALL0x487c4→0x4879a; next stopped helper target0x4b8a4. Corrected analysis136 states/eight CALL rows/no API candidates with explicit unknown memory/call/alias/depth stops. No real execution or complete savedata file IO/format admitted; higher stack slots are not historical ABI parameters. Earlier149-state report superseded, not deleted. Derived report and receipt STONEAGE-TW10-SAVEDATA-ARGTRACE-R7-HARDENED-*.json.


## 2026-10-12 — Taiwan v1.0 helper return-effects diagnostic R8

Bounded static/model FACT: original full-hash source Actions38231508976, independent branch38232149568/main38232296065 all SUCCESS. Helper0x4b8a4 has two modeled balanced return states at same RET0x4b91b, but a potential abstract cycle, unsummarized CALL0x4b8e2→0x4918f and unknown alias write0x4b903 prevent qualified whole-helper effects and caller resumption. No real executable execution, runtime loop behavior, file IO or savedata schema established. Exact derived report and receipt STONEAGE-TW10-SAVEDATA-HELPER-R8-ORIGINAL*.json; unresolved edges preserved.


## 2026-10-12 — Taiwan1.0 ESI-indirect write and structural helper loop R9

Bounded original static FACT: hash-verified source38234280963 and independent branch38235091041/main38235207142 SUCCESS. Selected write0x4b903 is4 bytes via ESI with unknown effective destination; parent structural loop has9 nodes and JE/JE/JL branches, but source predicates/bound/actual looping remain OPEN. Nested helper0x4918f delegates to0x491a1 before a modeled return. No CRT/FILE/object identity, real execution, file IO or savedata128-byte schema inferred from resemblance. Derived R9 frontier report and acceptance receipt preserved under research/recovered.


## 2026-10-12 — TW1.0 original R10 conditional ESI definitions and loop predicates REMOTE ACCEPTED (runtime/object ownership OPEN)

Fresh startup mainabab625de32d962488ad871b2d5bc0e9e837510e/tree073625b6ca4aa7ab1174da9428abdecf8fc17762; remote branches/HEAD/tree/recent commits/Actions/protocol/full current-state refreshed from exact matching fetched checkout. Highest prior NEXT R10 ESI provenance/loop predicates/delegate0x491a1. Every previous continuity byte preserved.

Original source2e66362d2fdfad466942efbe2335b06fb591c8ea, Action38237299847/job114771013775 SUCCESS:10 synthetic tests; complete transient archive842125501 MD5 b37a4a47f4eb608cac67e4ddf7a1621a/SHA1 b8cf92720b6ec8b3f46ea2e9bfcda986d21e7ded MATCH, extracted BIN523449360 and embedded original executable/save SHA256 independently checked. R7/R8/R9 gates rederived before R10. Originals purged; tiny derived-only artifact11741432915 ZIP1263/SHA2568cc94227f87e051c1246f862bbf8c0bfadc7f958706e1930cb07a69a605e667d. No native client execution, original bytes/operand listing/assets published.

Accepted bounded CONDITIONAL STATIC definitions at store0x4b903: two reaching ESI definitions,0x4b8d6 memory load with EBX base/EAX index/scale4/relative offset0, and0x4b8fd full-register copy from EDI. Conservative CALL-clobber and separately labeled syntax-only analyses produce these same two candidates because intervening definitions replace the unknown CALL output; this does NOT establish EBX/EAX/EDI values, pointed object identity, actual path feasibility or effective target. R9 four-byte ESI store remains an alias/ownership gap.

The three loop sites have unique conditional flag definitions: JE0x4b8c4 depends on32-bit ECX-vs-EBP comparison at0x4b8c2; JE0x4b8ca depends on8-bit masked test at0x4b8c6 of memory relative to ECX+12 with mask131(0x83); signed JL0x4b8d2 depends on32-bit EAX-vs-EDX comparison at0x4b8d0. These are transformed limited semantics, not whole disassembly or execution observations. In particular the loop comparison bound is a register value, not an admitted literal20 or128. Branch outcomes/runtime iteration bound remain OPEN. The50-node/55-edge parent graph retains ONE hypothetical returned-CALL continuation.

Delegate0x491a1:6 modeled states,no cap/cycle,one conditional balanced return at0x491cc preserving initial return word/cleanup0 and six general registers EBP/EBX/ECX/EDI/EDX/ESI. One unresolved CALL0x491ac→0x491cd remains. Modeled-return qualification FALSE; delegate effects and parent caller resumption are NOT admitted. A conditional balanced return cannot close unknown call effects.

26 new tests(10 dataflow/source+16 guard)+177 adjacent local regressions PASS(203). Strict R10 guard checks exact source identity, source/barrier semantic distinction, transformed memory widths/regions/offsets, predicate source uniqueness, nested R8 gap/return/qualification consistency and rejects all runtime/ownership/caller promotions. Branch synthetic38237547901 and independent source-run/head/branch/downloaded-derived strict/exact JSON custody38237880424 SUCCESS. Seven additive tooling paths were checked ahead2/behind0 and non-force FF integrated e10c49bdc2147c2aaff3bad35ea8dc2673831e1e; main synthetic38237748042 SUCCESS. Then two additive original-report/verifier paths checked ahead1/behind0 and non-force FF integrated96d431f980ad832cd0d2562ad68ee091a8fc416b/treeca33b58537ce15f490eb0d07cdbf8475926146fb; main independent custody38238013695 SUCCESS. Exact report STONEAGE-TW10-SAVEDATA-PROVENANCE-R10-ORIGINAL.json; receipt STONEAGE-TW10-SAVEDATA-PROVENANCE-R10-ACCEPTANCE-R1.json.

Highest NEXT R11: resolve stopped delegate0x491cd effects, and recover root/helper inputs reaching EBX/EAX/EDI/EDX/ECX/EBP around ESI definitions and loop comparisons (including initialization/update of the EAX-vs-EDX loop operands). Keep branch joins, opaque calls and memory aliases explicit. No CRT/FILE/table ownership inferred from resemblance; any specialized mutation requires exact original identity and independently qualified named effects. Only then consider caller continuation and filename→CreateFileA0x4ed01/handle→ReadFile-WriteFile buffers+length128. Framing/checksum/migrations/native persistence/cross-profile semantics remain separate OPEN; no engine or late codec promotion.


## 2026-10-12 — TW1.0 original R11 parent register definitions REMOTE ACCEPTED; virtual globals and direct/indirect delegate effects OPEN

Fresh startup main63c571ebfa25fdd3308607a9d981b3bef384fb12/tree2ed1eeb32c89a9536aef5b70f8ffc303f6f9745f; remote latest branch/HEAD/tree/commits/Actions/protocol/current-state and required files refreshed against the exact matching fetched checkout. Highest NEXT was R11 parent inputs and delegate0x491cd. Prior evidence and every continuity byte retained.

Original source205bcdc7e112f265c8661c44cbda04679e272507, Action38238943049/job114776451775 SUCCESS:10 synthetic tests; full transient archive842125501 MD5 b37a4a47f4eb608cac67e4ddf7a1621a/SHA1 b8cf92720b6ec8b3f46ea2e9bfcda986d21e7ded MATCH, BIN523449360 and embedded sa_3.exe/savedata.dat exact pinned SHA256 verified. R7/R8/R9/R10 original gates rederived before R11. Originals purged; derived-only artifact11740989842 ZIP1211/SHA2569b0e1a48a57016f5cfe7186bc8dbd5854eda9ef65cb418ec0bfd2305a79c2072. No original executable executed or proprietary bytes/operand listing/assets entered Git.

Accepted CONDITIONAL STATIC inputs in the50-node/55-edge parent graph (one structural returned-CALL assumption): EBX at ESI-load0x4b8d6 reaches four-byte memory-load definition0x4b8b8 from PE RVA0x1721884, writable virtual .data/raw-backed FALSE. EAX at that site has two reaching definitions: zero assignment0x4b8b1 and +1 self-adjustment0x4b8cc. EDI at copy0x4b8fd reaches four-byte load0x4b8f6 with EDI base/EAX index/scale1/offset0. This records immediate input definitions, not their recursively evaluated values, actual object identity or effective destination.

ECX at comparison0x4b8c2 and masked-test0x4b8c6 comes from four-byte memory-load0x4b8c0 through EDI; EBP at0x4b8c2 reaches zero assignment0x4b8ad. EAX at signed comparison0x4b8d0 reaches +1 definition0x4b8cc; EDX reaches four-byte load at root0x4b8a4 from PE RVA0x17228a0, writable virtual .data/raw-backed FALSE. These link R10 comparison inputs to initialization/update/global-load sites, but do NOT prove an actual iteration count. Neither a zero-initialized register candidate nor a non-raw-backed global region establishes runtime global contents, memory ownership or whole-function evaluation.

Delegate0x491cd has16 modeled states,no cap/cycle,no return paths,qualification FALSE. Two unsummarized CALL gaps: direct0x491db→0x49d93 and indirect0x491fb with target UNKNOWN. The latter is NOT presumed to be a particular import/CRT/function pointer. Exact target geometry/import identity and direct helper effects need original evidence. No delegate effects admitted, no caller resumed.

25 new tests(10 input/source+15 strict guard)+203 adjacent tests PASS(228). Fixed-point input queries retain branch joins and recurrence, kill ALL tracked registers at opaque CALL without ABI assumptions, and keep partial-register writes unmodeled. Strict guard checks eight ordered site/register identities, source/barrier semantics, full-width constants/increments/memory geometry and conservative R8 gap/return/qualification consistency; all runtime/ownership/value-completeness promotion flags remain false. Branch synthetic38239094795 and independent immutable source-run/head/branch/strict downloaded-derived exact JSON comparison38239182317 SUCCESS. Ahead3/behind0,nine added paths/no deletions,matching local/remote tree,non-force FF integrated7679adc4e6264aaeb13559bfdbf55c7bb7af2dbf/treed08be8e6364e13881e99cc52df6d25436f9ed53a; main synthetic38239246768 and main independent custody38239247329 SUCCESS. Report STONEAGE-TW10-SAVEDATA-INPUTS-R11-ORIGINAL.json; receipt STONEAGE-TW10-SAVEDATA-INPUTS-R11-ACCEPTANCE-R1.json.

Highest NEXT R12: identify indirect CALL0x491fb operand geometry and any exact original IAT/import association; summarize direct helper0x49d93 with all nested gaps retained. Separately trace EDI/EAX before load0x4b8f6, EDI initialization/stride feeding0x4b8c0, and write/initialization sources of virtual globals0x1721884/0x17228a0. Use bounded references and independently pinned original derived evidence; do not infer CRT/FILE/table identity or fixed loop limit from resemblance. Caller continuation requires exact qualified effects. Filename→CreateFileA0x4ed01, handle→ReadFile/WriteFile buffers+length128, original framing/checksum/migrations/native persistence and cross-profile semantics remain separate OPEN; no engine/late-codec admission.


## 2026-10-12 — TW1.0 original R12 exact HeapAlloc IAT association and bounded global-reference candidates REMOTE ACCEPTED (effects/runtime OPEN)

Fresh startup main56d68b501e8035e9057e59145527f16c9ad14d8b/tree90f983247096a8a0d36b625cc68e1f905954b067; latest remote branch/HEAD/tree/commits/Actions/protocol/full current-state and required files refreshed against exact matching fetched checkout. Highest prior NEXT R12 indirect CALL/direct helper/global and EDI inputs. Every previous continuity byte preserved.

Original source23646a74302d52bfd8d66a3e0a2397074a94041b, Action38240332581/job114781067998 SUCCESS:14 synthetic tests; transient full archive842125501 MD5 b37a4a47f4eb608cac67e4ddf7a1621a/SHA1 b8cf92720b6ec8b3f46ea2e9bfcda986d21e7ded MATCH, BIN523449360 and embedded original executable/save exact pinned SHA256 verified. All earlier R11 gates rederived before R12; originals purged; derived-only artifact11743107077 ZIP1599/SHA25633ca996cec202418434d22481c4ab1dfe0d7a205cf112bb8d8d307eef036c6f3. No original executable executed or proprietary bytes/operand listing/assets entered Git.

Accepted bounded STATIC identity: indirect CALL0x491fb is four-byte absolute unsegmented memory CALL through PE IAT RVA0x520f8 in raw-backed .rdata, exactly associated with original KERNEL32.dll!HeapAlloc. This closes ONLY import-slot association; actual arguments, allocation result/size/ownership, runtime target/effects and any file/format linkage remain unproved. No CRT/FILE object identity follows from this allocator association.

Direct helper0x49d93:32 modeled states,no cap/cycle,no return paths; explicit alias_write gap0x49dca and caller_memory_write gap0x49dec. Qualification FALSE. The mutation diagnostics require a new exact named-effect analysis; do not weaken R8 pure-return criteria or simply ignore these stores. No helper effects or caller resumption admitted.

Parent four conditional input queries: EDI before load0x4b8f6 is UNKNOWN after CALL0x4b8e2, with no ABI preservation assumption. EAX at that load comes from four-byte global memory-load0x4b8f1 at virtual .data RVA0x1721884 (raw-backed FALSE). EDI feeding0x4b8c0 has copy from EBX at0x4b8be and +4 recurrence at0x4b8cd. EAX before increment0x4b8cc retains zero assignment0x4b8b1 and +1 recurrence0x4b8cc. Loop stride/initialization syntax is bounded static evidence; actual bound, values, paths and effective object remain OPEN.

Separate global-reference CANDIDATE scan: full331776 raw .text bytes,104229 decoded instructions/eight undecodable gap bytes with bytewise recovery. This linear candidate universe is distinct from reachable graphs and prior analyzer counts; no reachability/completeness inferred. Global0x1721884 has8 read/2 write/0 address/0 unknown candidates; write sites0x4944a,0x49463. Global0x17228a0 has6 read/2 write/0 address/0 unknown candidates; write sites0x4943c,0x49457. All10/8 samples fit32-row caps/no truncation. These are direct exact-operand candidates, not proof of executed writes or absence of indirect aliases/other references. Runtime initialization and global values remain UNKNOWN.

32 new tests(14 import/reference/source+18 guard)+228 adjacent local tests PASS(260). Strict guard checks CALL shape/IAT geometry/import identity, query identity and unknown sources, bounded scan/count/sample/truncation consistency, nested gap/return/effect qualification and all no-runtime/no-ownership/no-initialization flags. Branch synthetic38240551862 and independent immutable source-run/head/branch/downloaded-derived strict/exact report custody38240746726 SUCCESS. Checked ahead2/behind0/seven added tooling paths and matching tree, non-force FF integratedd885a233ef6a7df78fde4db77826b96eee21014b; main synthetic38240661506 SUCCESS. Then ahead1/behind0/two added report/verifier paths and matching tree, non-force FF integrated3e0d5cf622c9482af7473d24e28d5ce120e21614/tree0cc0f7a3dee877dffcebacfbf27fc46aeb6c712b; main independent custody38240844029 SUCCESS. Exact report STONEAGE-TW10-SAVEDATA-FRONTIER-R12-ORIGINAL.json; receipt STONEAGE-TW10-SAVEDATA-FRONTIER-R12-ACCEPTANCE-R1.json.

Highest NEXT R13: recover exact address/value/frame-relative mutation geometry and input definitions at helper stores0x49dca/0x49dec, preserving all unsummarized effects; separately verify function/path context and value sources around candidate global writes0x4943c/0x4944a/0x49457/0x49463. Use one hash-pinned original derivation plus independent strict custody. A specialized summary must name legitimate caller/global mutations before any wrapper continuation; do not assume HeapAlloc argument size/object ownership or CRT ABI. Filename→CreateFileA0x4ed01, returned handle/stream→ReadFile/WriteFile buffer+length128, original framing/checksum/migrations/native persistence and cross-profile equivalence remain separate OPEN; no engine/late-codec promotion.


## 2026-10-13 — TW1.0 R23 conditional original heap/global/PUSH geometry accepted

FACT (bounded original static syntax only): exact imported HeapCreate0x499d4, HeapAlloc0x49a0c and HeapReAlloc0x4a0c4 structurally link to EAX global stores0x499dc/0x49a14/0x4a0d5. All EAX sources remain unknown after opaque CALL. Absolute global PUSH candidates correlate .data0x172187c with HeapAlloc and both .data0x1721878/.data0x172187c with HeapReAlloc. A limited straight PUSH suffix at HeapReAlloc yields conditional pre-CALL ESP offsets0/4/8/12; no ABI/runtime/ownership inference. Source Action38387323403, independent Action38387607870, exact original-derived equality PASS. Scope and receipt: STONEAGE-TW10-SAVEDATA-UPSTREAM-R23. Native save and common heap ownership OPEN; next R24 prefix/barrier and EAX computation provenance. This is present-day reconstruction evidence, not a newly claimed release event.


## 2026-10-13 — R24 conditional TW1.0 prefix/scalar/flag evidence accepted

Bounded static FACT only: original HeapCreate suffix barrier SETE AL0x499d0; wider HeapAlloc prefixes yield global/0/320 PUSH candidates with local pre-CALL offsets0/4/8. Competing anchors0x499f0/0x49a00 and0x4a0a0 lie inside instruction spans in alternative earlier-start decodes. None is a verified entry or complete original path. Original EAX0x4a0b3 is SHL2, with bounded LEA0x4a0af input geometry ECX+4*ECX+80; JNE0x4a0ad has comparison-source0x4a0ab (32-bit EAX vs ECX), branch outcome unknown. Original source38389572994, independent38389832057 exact derivative custody PASS; report/receipt STONEAGE-TW10-SAVEDATA-UPSTREAM-R24. Runtime values/heap ownership/native save OPEN. This is reconstruction evidence dated today, not a historical release event.


## 2026-10-13 — R25 TW1.0 conditional boundary/caller/input evidence accepted

Full original raw .text linear candidate scan agrees with R24 competing-span warning:0x499ff/0x4a0a1 are scan boundaries while0x49a00/0x4a0a0 are interior offsets. Two windows yield19 direct transfer candidates, including6 CALLs to4 targets0x499a8/0x499c3/0x499ff/0x4a09c. No execution/entry/all-caller claim. New-anchor ECX source is four-byte virtual .data0x1721864 load at0x4a0a1; EAX comparison input remains entry unknown. Prior SETE contexts do not reach the site in their bounded CFGs; sources/full values remain OPEN. Source38392504284 and independent38392864515 exact derived JSON custody SUCCESS. Report/receipt STONEAGE-TW10-SAVEDATA-UPSTREAM-R25. Native save/heap ownership OPEN; next R26 direct CALL-supported contexts. This dates reconstruction evidence, not a historical release event.


## 2026-10-13 — R26 TW1.0 CALL-supported conditional expression evidence accepted

Original direct CALL-backed contexts recover HeapCreate EAX zero-before-SETE and CMP0x499c7 ([ESP+8] versus EAX) flag provenance; named low-byte composition permits conditional EAX0/1, not an actual value or ABI role. ReAlloc comparison reads separate virtual .data0x1721874/0x1721864 globals; unique LEA/SHL linkage gives conditional20*ECX+320 modulo2^32. Actual globals/frames/paths/allocation/ownership/native persistence remain OPEN. Original source38394940020 and independent38395234686 exact original-derived custody SUCCESS; report/receipt STONEAGE-TW10-SAVEDATA-UPSTREAM-R26. Next R27 original CreateFileA/ReadFile/WriteFile boundary/caller/argument evidence. This dates reconstruction evidence only.


## 2026-10-13 — TW1.0 R27 conditional native API evidence

Original source Action38398995246/job115301450444 SUCCESS at branch agent/tw10-savedata-r27-native-io-sites-20261013 HEAD51cbe0b354e5865203c48512348dec74ff4521a1; inherited archive/runtime/savedata identity and exact R26 derivative SHA256ff829f3aa6b1ebfaf2f2d251581293ca734ef4837f7276f54000f364085b2122 rederived/strict guard PASS. Derived-only artifact11813083292 ZIP digest sha256:f6d0664760b93e1df84c7509839e2e8a0915cf51525e266005f753f3292871c7; JSON42859 bytes SHA2561c77b3c327a216729c1a66693d8dcb3be1c82205676365198fc5028239a12548. Final56 local and remote R27+R26 synthetic/guard tests Action38398996562/job115301454794 SUCCESS. Independent immutable run/head/branch/artifact custody, strict tamper constraints and EXACT committed-original-derived JSON equality Action38399287798/job115302439528 SUCCESS at HEAD14bfea543f71c64fd1867192f54dd5dc420b2803; local report equals independently logged JSON. Initial source38398758484 failed on a far CALL outside near-import identity scope, then superseded by an explicit near CALL filter and adversarial far CALL test. No original program executed or proprietary bytes/assets/code payload published; all transient originals purged.

- Full331776-byte raw .text linear candidate scan104229 instructions/eight gap bytes finds CreateFileA0xb1a7/0x4ed01 IAT0x520a0, ReadFile0x4a960/0x4aa31 IAT0x520d8 and WriteFile0x4c68c/0x4c6f1/0x4e42b IAT0x520a4; inventory samples untruncated. This is not all-indirect/control-flow/execution coverage.
- Selected CreateFileA0x4ed01 and first two ReadFile/WriteFile candidates have conditional pre-CALL PUSH suffixes7/5/3/5/5 rows. Offsets reference conditional ESP before CALL only, no Windows ABI parameter assignment. None of those operands has qualified savedata literal0x63634 address syntax; this does not establish absence of an indirect filename relationship.
- CreateFileA candidate PUSH EAX at0x4ecf7 has LEA EBP-28 definition0x4ecf4; PUSH ESI0x4ecf0 is UNKNOWN_CALL from0x4eccd. Local EBP+8/-12/-16/-8 operands are candidate frame-relative syntax, not a verified original frame or filename parameter.
- First ReadFile/WriteFile pre-call EAX sources load memory[EBX], followed by PUSH memory[EAX+ESI]; original EBX/ESI values and handle/table identity unknown. ReadFile0x4aa31 suffix stops at a memory/stack barrier with only three PUSH rows. WriteFile0x4c6f1 has a straight suffix but is NOT reached in candidate graph rooted0x4c692; empty register sources are not proof of missing runtime values.
- Fourteen nearby direct CALL targets include useful candidates0x4eb55,0x4a8dc,0x4c5b4,0x4c4f2 and0x4a820. These are CALL syntax aids, not verified entries, caller completeness, return effects or a savedata chain. Third WriteFile0x4e42b and early CreateFileA0xb1a7 are inventoried only.

FACT is limited to pinned-original static syntax and derivative custody. All actual filename/handle/buffer/128-byte save schema/runtime/ABI/ownership relations remain OPEN. R28: audit direct CALL-supported original contexts0x4eb55 (CreateFileA),0x4a8dc (ReadFile) and0x4c5b4 (WriteFile), with explicit span/path/entry bounds; trace EBP-frame inputs and [EBX]/[EAX+ESI] handle-like syntax as candidates, never actual handle ownership. Correct WriteFile0x4c6f1 unreachable heuristic root before using its sources; extend bounded analysis to third WriteFile0x4e42b if useful. Native savedata filename->returned handle->buffer/length128 remains OPEN.


## 2026-10-13 — TW1.0 R28 CALL-supported native file API input candidates

Original source Action38400713383/job115307314019 SUCCESS at branch agent/tw10-savedata-r28-call-supported-io-20261013 HEADd33cacc472793a38422d9e9cf60107c585e3edf8; complete inherited archive/runtime/savedata identity and exact R27 original JSON SHA2561c77b3c327a216729c1a66693d8dcb3be1c82205676365198fc5028239a12548 rederived/strict guard PASS. Derived-only artifact11814279564 ZIP digest sha256:348ae91b6727a24a2b3db2685d007aace1c814e98eb5c564f7b91e27ef15d967; JSON56581 bytes SHA256296e5754a3eebafc6360cc45000ba73b6bcf1cc0a5d0ee439aa291eb45e0d645. Final58 local and remote R28+R27 synthetic/guard tests Action38400714689/job115307317417 SUCCESS. Independent immutable original-run/head/branch/artifact custody, strict tamper controls and EXACT committed-original-derived JSON equality Action38400948159/job115308122805 SUCCESS at HEAD7b641d78b893f68a3be4e088b16892f05b777205; local report equals independently disclosed JSON. Initial successful source38400524565 superseded by complete-instruction-inside-byte-window hardening and an adversarial spanning-instruction control. Original programs never executed and proprietary bytes/assets/code payload never published; transient originals fully purged.

- Direct CALL syntax0x4b873->0x4eb55,0x486f0->0x4a8dc and0x48c5e->0x4c5b4 revalidated against exact original R27. Bounded graphs at768-byte/256-node caps yield230/271,174/200 and139/156 nodes/edges respectively; no frontier or node cap, but no entry/complete path/actual frame certificate.
- All five selected API sites occur in their candidate graphs. WriteFile0x4c6f1 is now reached from CALL-supported0x4c5b4, superseding the unreachable R27 heuristic0x4c692 context. Straight suffix7/5/3/5/5 rows remains conditional pre-CALL ESP geometry; neither Windows ABI roles nor actual argument values are inferred.
- ReadFile EBX candidate LEA0x4a8ff and WriteFile EBX candidate LEA0x4c5d9 share virtual writable .data displacement0x1721760 (raw-backed FALSE), EAX index scale4. Subsequent EAX loads [EBX]0x4a957/0x4c687 and PUSH memory[EAX+ESI] are physical syntax only. Read index EAX definition0x4a8f9 and Write index0x4c5d3 remain unmodeled; same address syntax is not same runtime table contents/file handle/owner.
- CreateFileA ESI/EBP sources remain UNKNOWN_CALL0x4eccd; EBX copy0x4ecd2 depends on unknown EAX from that call. EAX LEA0x4ecf4 has EBP-28 syntax, with EBP still killed conservatively at the opaque call. ReadFile candidate EBP comes from MOV EBP,ESP0x4a8dd, and EDI input from [EBP+12]0x4a91f; ESP/caller-frame ownership not modeled or proved.
- Recovered WriteFile0x4c6f1 ECX source LEA0x4c6e4 has EBP-12 syntax; EDI candidates are zero definition0x4c5f1 plus UNKNOWN_CALL0x4c60d, and EAX source0x4c617 remains unmodeled. Candidate loops preserve later/self-site UNKNOWN_CALL sources rather than assert runtime order or callee effects.
- Compact register/dependency surfaces15/36/29 queries, no query-limit hit or candidate truncation; at most two dependency levels do not prove closure or memory values. Every immediate conditional post-API EAX query has a single UNKNOWN_CALL at its respective API site. Third WriteFile0x4e42b and early CreateFileA0xb1a7 remain inventory-only.

FACT limited to pinned-original static syntax/custody, not native runtime/API/frame/table/handle ownership. R29: inspect exact original operand shapes and conditional scalar input provenance at ReadFile index definition0x4a8f9/ESI0x4a8fc and WriteFile index0x4c5d3/ESI0x4c5e0 plus EAX0x4c617. Qualify the shared0x1721760+4*EAX addressing candidates without evaluating original values or asserting a handle-table owner; audit bounded writes/references if useful. Continue filename/CreateFileA-return/handle/buffer/length128 linkage with explicit opaque-call, cycle, stack-frame and memory-alias gaps. Native schema/persistence remain OPEN.


## 2026-10-13 — TW1.0 R29 original conditional scalar and shared-address candidates

Original source Action38402348628/job115312903541 SUCCESS at branch agent/tw10-savedata-r29-scalar-address-20261013 HEADdc54d8d72591437b05e2f30b779e7f5b8f041912; complete inherited archive/runtime/savedata identity gates and exact original R28 JSON SHA256296e5754a3eebafc6360cc45000ba73b6bcf1cc0a5d0ee439aa291eb45e0d645 rederived/strict guard PASS. Derived-only artifact11815337939 ZIP digest sha256:1b9a07e2c076bc7e7642810b13a8b8e40973f2ff362c4b4350a9a2e1eb7903a2; JSON25275 bytes SHA256151b846b843165c0cf5002792f4a43904d7f2b6a3683e1d951ea3d6cf5dbe415. Final64 local and remote R29+R28 synthetic/strict tests Action38402348702/job115312903982 SUCCESS. Independent immutable run/head/branch/artifact custody, strict tamper controls and EXACT committed-original-derived JSON equality Action38402645534/job115313933808 SUCCESS at HEAD3e092080f1475d0e53c40858ed81dc58f03bbde1; local report equals independently disclosed JSON. No original runtime program or original-state arithmetic executed; no proprietary byte/asset/code payload published; transient originals fully purged. Intel official SDM Vol2B SAL/SAR/SHL/SHR printed4-584/4-585 checked for conditional shift mathematics; its architecture semantics do not establish historical original values.

- Exact R28 CALL-supported ReadFile root0x4a8dc and WriteFile root0x4c5b4 revalidated; graphs174/200 and139/156 nodes/edges unchanged within768 bytes/256 nodes, no frontier/node cap. Actual entries/paths/frames and returning-call effects remain unproved.
- Original definitions0x4a8f9/0x4c5d3 are SAR EAX by literal5, and0x4a8fc/0x4c5e0 are SHL ESI by literal3, all full32-bit register destinations. WriteFile0x4c617 is ADD EAX,ESI. Five separate conditional u32 models qualified by exact operand shapes; original values/results/flags/index/API roles never evaluated or admitted.
- ReadFile pre-SAR EAX has MOV EAX,ESI candidate0x4a8f4, fed by ESI memory-load0x4a8e4 [EBP+8]. WriteFile pre-SAR EAX has MOV EAX,ECX candidate0x4c5cf, fed by ECX load0x4c5bd [EBP+8]. EBP candidates come from respective MOV EBP,ESP0x4a8dd/0x4c5b5; ESP/frame/parameter identity unknown, matching offsets do not imply matching actual arguments.
- Pre-SHL ESI remains blocked by unmodeled definitions0x4a8f6/0x4c5d6. Write ADD input EAX comes from MOV [EBX]0x4c615; EBX has shared LEA0x4c5d9 or UNKNOWN_CALL0x4c60d candidates, and ESI has SHL0x4c5e0 or the same unknown call. No memory-value, alias or original address composition promoted.
- LEA EBX at0x4a8ff/0x4c5d9 retains common virtual writable raw-unbacked .data displacement0x1721760 with4*EAX index. Compact input/dependency surfaces5/8 queries have no truncation/limits; general reaching-definition semantics still leave SAR/SHL unmodeled, separate symbolic models do not silently change older evidence.
- Full331776-byte raw .text scan104229 instructions/eight gaps finds25 exact displacement/immediate operand candidates, all within32-sample bound. One matching direct four-byte MOV destination at0x4c9da and one immediate address operand at0x4e77f are identified; Other rows are read/address candidates, including direct and indexed operands. This exact-syntax inventory is not exhaustive alias/write/initialization or table/handle owner proof.

FACT limited to pinned original static syntax/custody, not evaluated runtime/index/table/handle/ABI/owner facts. R30: inspect exact input definition shapes0x4a8f6/0x4c5d6 before SHL to qualify any conditional index/offset composition without asserting actual descriptor values, ranges or ownership. Audit direct MOV-to-shared-global candidate0x4c9da source and acquire coherent boundary/direct CALL support before using its context; immediate-address candidate0x4e77f may aid discovery. Continue native CreateFileA returned-handle capture and filename->handle->buffer/length128 with explicit call/stack/alias gaps; no CRT/table/native schema/persistence promotion.


## 2026-10-13 — TW1.0 R30 conditional mask and shared-global writer inputs

Original source Action38404299461/job115319726044 SUCCESS at branch agent/tw10-savedata-r30-mask-writer-20261013 HEAD724838fa88ebbfc381a0deec73edce4e467a8090; complete inherited archive/runtime/savedata identity gates and exact original R29 JSON SHA256151b846b843165c0cf5002792f4a43904d7f2b6a3683e1d951ea3d6cf5dbe415 rederived/strict guard PASS. Derived-only artifact11818650369 ZIP digest sha256:f49a3be1be1014e8cb9d966540c0dbdd5fcc0654f772b1319293013f3cfccf21; JSON12559 bytes SHA256760730dc57c823a7279b22a0944ffaac588e77d4fb6b0d5f5024265345f0b45a. Final61 local and remote R30+R29 synthetic/strict tests Action38404299604/job115319727392 SUCCESS. Independent immutable run/head/branch/artifact custody, strict tamper controls and EXACT committed-original-derived JSON equality Action38404780799/job115321429623 SUCCESS at HEAD7822838f659f76fc140b991b3524bba2280a913d; local report equals independently disclosed JSON. Original runtime/programs and original-state arithmetic never executed; no proprietary byte/asset/code payload published; transient originals fully purged.

- Original full32-bit AND ESI,31 at0x4a8f6/0x4c5d6 followed by SHL ESI,3 at0x4a8fc/0x4c5e0 has unique untruncated graph-local mask-to-shift definition links. Separate conditional u32 expression((pre-mask ESI &31)<<3) mod2^32 qualifies in both contexts, not an evaluated original offset/index range, descriptor or handle role.
- ReadFile mask ESI input comes from memory-load0x4a8e4 [EBP+8], with EBP candidate MOV EBP,ESP0x4a8dd. WriteFile mask ESI input is MOV ESI,ECX0x4c5d1, depending on ECX memory-load0x4c5bd [EBP+8] and EBP copy0x4c5b5. These remain frame-relative candidate syntax, not real caller-frame/parameter ownership or equal original argument values.
- ReadFile/WriteFile graphs174/200 and139/156 nodes/edges, compact inputs3/4 queries, no frontier/node/query/candidate cap. General reaching semantics still mark AND as unmodeled; symbolic composition is separate and retains original input/result/flag/API uncertainty.
- Full331776-byte raw .text linear scan104229 instructions/eight gaps finds eight direct CALL target candidates in[0x4c85a,0x4c9ea), all within32-sample cap. Writer0x4c9da and two selected targets0x4c9ba/0x4c953 are linear scan boundaries only. Root0x4c9ba supported by CALL0x49879; root0x4c953 supported by CALL0x48e73. No complete indirect caller/entry/runtime proof.
- Original MOV0x4c9da stores full-width ESI to absolute virtual .data displacement0x1721760. Candidate root0x4c9ba graph143/164 reaches this writer; ESI sources are MOV ESI,EAX0x4c9cb and UNKNOWN_CALL0x4c9d4, with EAX before copy UNKNOWN_CALL0x4c9c6. Source values, callee returns/preservation, allocation and actual global initialization/owner remain unknown.
- Selected root0x4c953 graph26/29 does NOT reach0x4c9da; empty writer sources do not prove original absence. Its seven direct caller candidates include0x4ed26 in CreateFileA's numeric continuation region, supporting a concrete next native-handle-capture audit without treating0x4c953 as global writer or verified file/CRT helper.

FACT limited to pinned-original static syntax/custody; actual offset/index/descriptor/table initialization/owner/ABI/callee effects remain OPEN. R31: return to original CreateFileA0x4ed01 conditional continuation from0x4ed07 and audit direct CALL0x4ed26->0x4c953 (exact R30 scan candidate). Recover physical PUSH/register sources and bounded callee memory-store candidates, with explicit entry/path/return/stack/alias uncertainty; no actual API EAX/handle success or CRT/FILE owner admission. Retain global writer0x4c9ba's opaque calls0x4c9c6/0x4c9d4 as independent initialization gaps, audit their identities only if useful, and do not block the whole native save chain on generic allocator exhaustion. Filename->returned handle->ReadFile/WriteFile buffer/length128/schema/persistence remain OPEN.


## 2026-10-13 — TW1.0 R31 opaque API copy and distinct helper input provenance

Original source Action38406412226/job115327068789 SUCCESS at branch agent/tw10-savedata-r31-create-capture-20261013 HEADe3b2d5b75668b0823573f499b11f9ee46883f6f0; complete inherited archive/runtime/savedata identity gates and exact original R30 JSON SHA256760730dc57c823a7279b22a0944ffaac588e77d4fb6b0d5f5024265345f0b45a rederived/strict guard PASS. Derived-only artifact11816674613 ZIP digest sha256:296aa126d7f52c4bc8c8ca54183eaaf7868ed0d309bca6bd4531c2173c23a075; JSON13684 bytes SHA256af1e1ee0fb61549e89b6e168e82c5c7b58de170e9a1bb7f9ed2968c095cebdcc. Final59 local and remote R31+R30 synthetic/strict tests Action38406413334/job115327073411 SUCCESS. Independent immutable run/head/branch/artifact custody, strict tamper controls and EXACT committed-original-derived JSON equality Action38406921461/job115328837823 SUCCESS at HEAD51182cbed7eac17731f2c3fe173d0e541ddaca39; local report equals independently disclosed JSON. Original runtime/programs never executed; no proprietary byte/asset/code payload published; transient originals fully purged.

- Original direct CALL syntax0x4b873->0x4eb55 and0x4ed26->0x4c953 independently rechecked; CreateFileA0x4ed01 import/IAT0x520a0 exact association. Parent candidate graph230/271 reaches API,0x4ed07 and helper CALL; no frontier/node cap, but actual entry/path/frame/callee-return effects remain unknown.
- Single full-width MOV ESI,EAX0x4ed07 has unique opaque source UNKNOWN_CALL0x4ed01 at its EAX input. This establishes a graph-local API-token copy candidate only, never a successful actual CreateFileA returned handle/value. The caller source surface has7 queries/no truncation.
- Before helper CALL0x4ed26 the conditional local suffix contains only PUSH EAX0x4ed25 at pre-CALL ESP offset0, stopping at intervening CALL0x4ed1f. EAX before PUSH/CALL is UNKNOWN_CALL0x4ed1f; all sampled pre-call registers conservatively carry that opaque barrier. R30's numeric continuation/helper discovery must not be promoted into direct CreateFileA-handle-to-helper argument linkage.
- Helper0x4c953 graph26/29 contains five recognized explicit unsegmented four-byte MOV store candidates, no sample truncation. ECX from entry-relative [ESP+4]0x4c953 feeds MOV0x4c959 to virtual writable .data0x172120c. Single ESP-relative operand is syntax, not an admitted caller PUSH/parameter binding.
- Other four helper stores target separate virtual writable .data0x1721208: MOV0x4c97d literal13, MOV0x4c98f EAX, MOV0x4c9a3 literal8 and MOV0x4c9af literal22. EAX store source is memory-load0x4c988 from raw-backed writable .data displacement0x6484c with EDX index scale8; EDX has zero-definition0x4c957 and INC0x4c96b loop candidates. No original loop index/table values, meaning or evaluated mapping admitted.
- Helper compact sources4 queries/no truncation/caps. Implicit/segmented/other memory writers and aliases are not complete. Actual memory mutations/global ownership/CRT identity/native save schema remain OPEN; helper's mapping-like syntax is a discovery hypothesis pending intervening CALL identity and branch evidence.

FACT limited to original static syntax and custody; mapping-like helper role is HYPOTHESIS until call/branch evidence, actual handles/globals/frame/ABI/owner/effects remain OPEN. R32: identify original intervening CALL0x4ed1f and the predicate/branch reaching0x4ed26 to qualify the helper's mapping-like role. If justified, audit conditional physical PUSH EAX offset0 -> helper entry [ESP+4] hardware geometry separately from any API return/owner claim. Resume captured ESI0x4ed07 along other candidate parent paths and inspect parent memory-store/call inputs; do not mistake0x4c953's globals for the shared0x1721760 address candidates. Actual filename->CreateFileA result->ReadFile/WriteFile buffer/length128/schema/persistence, alias/frame/return effects and CRT/heap ownership remain OPEN.


## 2026-10-13 — R32 original GetLastError IAT — accepted static-only

TW1.0 original source run38409002824/job115336054231 SUCCESS at head55bb9c76b4d13215332cffc0a649e869c72d0188. R31 exact report SHA256af1e1ee0fb61549e89b6e168e82c5c7b58de170e9a1bb7f9ed2968c095cebdcc rederived and strict-gated. Original not executed; transient bytes purged; derived-only artifact11820641198 ZIP sha256:efa5c1a68f44893654d77c3596afe1bf0f9a4644208c8238013b4bf8ebcfdb46, JSON5153 bytes sha256:24849b161be51b4fbf50fa7fe2c2bb48b6e79a6a83fb012f33ddd961f6336c9c. Independent verify38409252712 and exact canonical equality38409470522 SUCCESS.

FACT, original static only: 0x4ed1f CALL resolves through imported IAT0x5208c to KERNEL32.dll!GetLastError, with execution/result UNKNOWN. Two conditional direct branches are JE0x4ed0b->0x4ed1f and JNE0x4ed16->0x4ed33. Second target is not structurally connected to helper CALL0x4ed26 in bounded returning-call graph, while fallthrough is. Conditional PUSH EAX0x4ed25 and helper entry [ESP+4]0x4c953 have matching hardware slot geometry0/+4 but no actual argument/ABI linkage. EAX before PUSH has UNKNOWN_CALL0x4ed1f; ESI before that call has multiple graph-local candidate definitions including MOV0x4ed07 and UNKNOWN_CALL0x4ed19.

HYPOTHESIS: error-handling/mapping role needs further evidence. OPEN: real branch outcomes, error value, actual API handle, filename, ReadFile/WriteFile buffer/length128, schema, aliases, persistence, ownership. NEXT R33: analyze CALL0x4ed19 and predicate/flag sources. Canonical report research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R32-ORIGINAL.json; scope docs/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R32.md.


## 2026-10-13 — R33 original CloseHandle and ZF operand candidates — accepted static-only

Independent original source run38411584532/job115345021284 SUCCESS on head f0fe4a5491ac031f2bc941de6c335b85a1273ea4. All inherited pinned original client/runtime/savedata and exact R32 SHA25624849b161be51b4fbf50fa7fe2c2bb48b6e79a6a83fb012f33ddd961f6336c9c guards passed. Derived-only artifact11822641076 ZIP sha256:01286152611e96bc6e9dac874422227336b5b8f84397fcb20b9b4560d54894bc; original-derived JSON4772 bytes sha256:1be7d372b0650b9944a12264b612531d46a5326af3628e12363df365ddab98b5. Separate immutable source custody/strict guard Action38411779674 and committed canonical JSON exact equality Action38411925788 SUCCESS. Original code not executed; transient originals deleted; no copyrighted original bytes/assets exported.

FACT conditional static syntax: original memory-indirect CALL0x4ed19 has KERNEL32.dll!CloseHandle import association via IAT0x520a8. This is distinct from R32's GetLastError0x4ed1f/IAT0x5208c and CreateFileA0x4ed01/IAT0x520a0. Bounded ZF may-definition for JE0x4ed0b is CMP ESI,EDI at0x4ed09 (one candidate), and for JNE0x4ed16 is TEST EAX,EAX at0x4ed14 (one candidate). Both ZF predecessor walks bounded within original parent graph, no cap/truncation; four register-source queries, no actual values known. Structural CALL fallthrough remains assumed.

HYPOTHESIS: original branch structure could test invalid handle or cleanup; no EDI sentinel, EAX return, taken branch, successful handle, runtime effects or save persistence established. Highest NEXT R34: trace EDI definition before CMP0x4ed09, EAX before TEST0x4ed14, CloseHandle pre-call PUSH provenance and relevant branch exits. Native filename->handle->ReadFile/WriteFile buffer/length128/schema/persistence remains OPEN. Exact witness research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R33-ORIGINAL.json; scope docs/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R33.md.


## 2026-10-13 — R34 original CloseHandle PUSH and predicate register inputs — accepted static-only

Pinned original Action38413940213/job115353221738 SUCCESS at source HEAD44c96a0a3195fb847b7d443ca4fadb22e8d7e65a. R33 exact original-derived SHA2561be7d372b0650b9944a12264b612531d46a5326af3628e12363df365ddab98b5 rederived/strict guard PASS. Derived-only artifact11822613944 ZIP SHA256:29057dd97c3275122b009c6f205c0585000b49dc0d630460e8ed78a3163d6f4e, original-derived JSON5542 bytes SHA256:e95548eb5e9b60b1f5214ed751c1f3df9b83f27a4d20ebe35a49427cf9b32c34. Independently checked source identity and strict controls Action38414131854/job115353899310 SUCCESS; independently confirmed canonical exact JSON equality Action38414279033/job115354415334 SUCCESS. Originals never executed or published, transient proprietary content purged.

FACT pinned-original conditional static only: CMP ESI,EDI at0x4ed09 has ESI reaching candidate MOV ESI,EAX0x4ed07, with EAX originating from opaque CreateFileA0x4ed01; EDI at the CMP is likewise UNKNOWN_CALL0x4ed01 under conservative whole-register-call killing. TEST EAX,EAX0x4ed14 has EAX source UNKNOWN_CALL0x4ed0e. The bounded pre-CloseHandle0x4ed19 suffix has one PUSH ESI0x4ed18 at conditional pre-call ESP offset0, and ESI source UNKNOWN_CALL0x4ed0e. No original branch predicate, real value, EDI sentinel, actual API parameter/handle/return or persistent native save was evaluated or proved. Two-level register source graph is intentionally conservative; it does not certify callee preservation or actual alias ownership.

HYPOTHESIS file-handle check/cleanup still unconfirmed. NEXT R35 identify original CALL0x4ed0e and its pre-call input geometry. Native filename/returned handle/ReadFile/WriteFile buffer/length128/schema/persistence and cross-version or server-only equivalence remain OPEN. Canonical research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R34-ORIGINAL.json; scope docs/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R34.md.


## 2026-10-13 — R35 original GetFileType import and conditional PUSH ESI — accepted static only

FACT (pinned authenticated Taiwan Waei/JSS 1.0 original executable, never executed): memory-indirect CALL0x4ed0e associates to KERNEL32.dll!GetFileType via original PE import-slot RVA0x52160. One straight suffix PUSH ESI0x4ed0d with conditional pre-call ESP offset0 precedes the opaque call; source candidate before the PUSH is MOV ESI,EAX0x4ed07, itself preceded by conservative opaque CreateFileA CALL0x4ed01. TEST EAX,EAX0x4ed14 has EAX source unknown CALL0x4ed0e; before CloseHandle0x4ed19 ESI provenance is likewise conservatively blocked by that CALL. No actual original values, call execution, ABI binding, return result, branch outcome or persistent save is proved.

Original derived-only source run38418400068 (head a02fd2464424a1974bcdf954aad0894589052614) SUCCESS, independent immutable-artifact/negative validation38418921425 SUCCESS, exact committed JSON equality38419262860 SUCCESS. Artifact11824229823 ZIP SHA256 4c5cdd8677641d5588d738aa3286a0931e4c06590405f61fcffbd7901f483f33; 5348-byte JSON SHA256 5052a3d57b89f1d257846df6cef7c513fe544cadeb420e11f0a18468d3908f23. Original binaries never executed or uploaded and transient files purged.

HYPOTHESIS: a file-type validation path is compatible with the static GetFileType/TEST/JNE arrangement, but actual validation and error handling remain unproven. OPEN native filename, CreateFileA success/return, true API handle, ReadFile/WriteFile buffer/length128/schema/persistence, alias/owner and cross-version/server-only equivalence. NEXT R36 conditional branch and handle-candidate joins with strict static boundaries. Scope docs/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R35.md.


## 2026-10-14 — TW1.0 R36 original branch topology and continuation stores accepted

FACT (bounded original static): TEST EAX,EAX0x4ed14 feeds JNE0x4ed16; direct target0x4ed33 and fallthrough0x4ed18 have separately reproduced structural routes. PUSH ESI spelling matches at0x4ed0d/0x4ed18 but opaque GetFileType CALL separates their conservative provenance. Three continuation stores carry AL/AL/EAX with separate low-byte and address queries; none establishes a real saved handle. Source38488978148, artifact11860393895 and independent exact canonical custody38489210950 all SUCCESS;81 tests PASS. No historical program executed or proprietary payload published.

HYPOTHESIS: file-status/error handling and descriptor helper role. OPEN: actual branch values, callee preservation, filename/handle/buffer/length128/native schema/persistence, ownership, original server authority and cross-version equivalence. NEXT R37 continuation CALL helpers0x4e80a/0x4c761 and unresolved partial-register/address inputs. All historical system-family PARTIAL/OPEN gates remain unchanged.


## 2026-10-14 — TW1.0 R37 continuation helper/static operand candidates accepted

FACT (original static only): direct CALLs0x4ed49->0x4e80a/0x4ed87->0x4c761, two candidate boundaries, shared0x1721760+4*ECX LEA syntax, imported SetStdHandle/SetFilePointer/GetLastError and bounded caller/helper memory/input surfaces independently verified. OR AL,1 at0x4ed57 is a byte write;0x4ed59 SAR ECX,5 and0x4ed69 SHL ESI,3 are full32-bit shifts. This supersedes any literal interpretation of earlier provisional partial-definition grouping; historical records retained. Original source38491613508/artifact11861673941 and independent canonical equality38491820292 SUCCESS;112 tests PASS. Originals unexecuted/unpublished/purged.

HYPOTHESIS: descriptor/handle registration and file-position helper roles. OPEN: actual value/ABI binding, entry/frame/alias/heap/CRT/table owners, successful handles/seek, original filename/ReadFile/WriteFile buffers/length128/native schema/persistence and server/cross-version equivalence. NEXT R38 helper stack-prefix and shared-write exact source qualification. All Stage A system-family gates remain PARTIAL/OPEN.


## 2026-10-14 — TW1.0 R38 conditional stack positions and exact shared-store source accepted

FACT (original bounded static only): caller PUSH EBX/ESI positions match helper entry [ESP+4] and later [ESP+20] after three modeled four-byte pushes, CONDITIONAL on32-bit stack/near-CALL attributes. Original MOV0x4e862 source is EBX/four bytes; SAR ECX5/SHL ESI3/shared LEA syntax independently recovered. Opaque SetStdHandle effects and explicit memory aliases prevent actual value/handle/ownership or executed-write promotion. Source38492935617/artifact11862821367 and independent exact canonical equality38493237867 SUCCESS;139 tests PASS. Originals unexecuted/unpublished/purged.

HYPOTHESIS: descriptor-to-native-handle registration role. OPEN: actual parameter contents, caller/helper frame/ABI/return effects, file/CRT/heap/alias/table owner and original filename/buffer/length128/schema/persistence, server authority and cross-version equivalence. NEXT R39 exact mask and bounded symbolic stack-content candidates, followed by native ReadFile-context buffer/length recovery. All historical system-family gates remain PARTIAL/OPEN.


## 2026-10-14 — TW1.0 R39 mask/token/read-caller candidates accepted; save payload separate

FACT (conditional original static): AND ESI31->SHL3 composition; bounded slot/register-symbol candidates with disjoint callee-prefix pushes; direct caller0x4edb0->0x4a8dc and physical PUSH EBX/EAX/immediate1 suffix; LEA EAX,[EBP+19] plus byte[EBP+19] comparison0x1A. Source38494750030/artifact11862418406 and independent exact canonical equality38495118066 SUCCESS;162 tests PASS. No original program or original-state value evaluated/executed/published.

HYPOTHESIS: text-file end-check handling. No actual EOF/text mode/CRT role or128-byte savedata payload established. OPEN: actual parameter contents, ABI/frame/callee return effects, file/handle/table/alias/owner and savedata filename/buffer/length/schema/persistence, original server authority and cross-version equivalence. NEXT R40 conditional native-read parameter/frame/branch provenance, keeping this possible probe distinct from save payload recovery. All Stage A system-family gates unchanged.


## 2026-10-14 research milestone — TW1.0 R40 read-frame/end-check distinction

Source Action38569997657/job115872382427 SUCCESS at agent/tw10-savedata-r40-read-frame-endcheck-20261014 HEADb9b347825779a861ea45e8c58b97838dd1e88f76. Exact R39 original SHA2569e7648bd716b65a3695c1a1b04461d5863474210f083e5a11df6595e8cdbbd44 rederived/guarded with authenticated original archive/runtime/save identities. Derived-only artifact11898220647 tw10-r40-original-read-frame-endcheck-derived ZIP SHA256996e46965796c005610aeecdb3ff1a2ee2f5a0597d58bda8a60071dbab42dfd0; raw JSON80338 bytes SHA2560ec7fe47a34a77143b446cb02df088d647f4694174d025039abffd8b35066c2f. Independent immutable run/head/branch/artifact custody, pinned digest/size, strict negative controls and exact canonical parsed JSON equality Action38570582335/job115874400290 SUCCESS at HEAD81974e598687264313f8aafeb7c98d66d7898234. Local derivative equals independently disclosed original-derived JSON;192 local/independent R40–R32 tests PASS (source57 R40/R38 tests PASS). Original executable/media transient, unexecuted, unpublished and unconditionally purged.

FACT (bounded static only): original read-context prolog establishes the EBP spelling before SUB/unknown ESP effects. Four-byte EBP+8/+12/+16 accesses have conditional caller-slot0/4/8 geometry; the five early memory reads also include a negative local AND and DEC of the +16 slot. Both ReadFile IAT associations requalified;5/3 physical PUSH candidates retained. Equal caller LEA/CMP address spelling and six nearest ZF-source candidates do not establish executed address/predicate/return effects.

HYPOTHESIS: this parent branch may be a text-file end check. OPEN: its actual role/ABI/contents, all savedata payload/schema/persistence and server/cross-version equivalence. The immediate1 is not a demonstrated native API read length; the slot is subsequently RMW. No era/system-family closure or game implementation follows. Highest NEXT R41: return to savedata-specific original filename PUSH/CALL sites0x40064->0x40069,0x400e4->0x400e9,0x40115->0x4011a,0x402a0->0x402a5, all direct targets0x487ba from accepted R4–R7 evidence. Revalidate their exact immediate address0x63634 and physical pre-CALL suffix, then recover bounded caller continuation buffer/count/size operands and downstream direct CALL identities with coherent original boundary/entry support. These are independent conditional caller contexts; do not assume the0x487ba return or register/frame preservation. Seek savedata-specific payload read/write candidates, keeping generic open/end-check paths separate. No global/table/allocator ownership exhaustion; no literal128 schema promotion. All system-family PARTIAL/OPEN states and Stage A restoration before joint future-engine/game review remain binding.


## 2026-10-14 — TW1.0 R41 savedata-specific continuation discovery

Source Action38572368408/job115880592995 SUCCESS at agent/tw10-savedata-r41-savedata-callers-20261014 HEAD60e22410c5f6f84f6d0ad9f6169ea6b2aa2f5c0b. Authenticated transient retail archive/disc/runtime/save gates and exact hardened R7 derivative SHA25673b965887f0ff391f40abba4649482aa2d832151df5fbb602c4274d356bc71d8 rederived/strict-gated. Derived-only artifact11898143745 tw10-r41-original-savedata-callers-derived ZIP SHA256e7ed8e2afc1f25a6250bafa4622be27613b6e0a6c63f90771c296f3a93e2dbe9; raw JSON120631 bytes SHA2568c8474f75eb6adec5aa3939054f0fce26997152fb8e1f1424e74f18485c2471c. Independent immutable run/head/branch/artifact custody, pinned raw digest/size, strict negative controls and exact committed-original JSON equality Action38572684418 SUCCESS at HEADe0f12565d8cbd3a4503d6428497a0888fef8cf12. Local JSON equals downloaded pinned original-derived JSON.254 local/independent R41-R32 plus hardened R7 tests PASS. Original executables/media unexecuted, unpublished, transient and unconditionally purged.

FACT (original bounded static): four exact savedata filename PUSH/CALL prefixes and their PE-entrypoint CFG boundary support reverified. Separate continuation graphs discover repeated target0x48bbc with four physical PUSH candidates and target0x48660 with literal4000/local address candidates. Open CALLs remain opaque; branch joins retain alternate source candidates. No parameter/handle/buffer/length/schema/persistence or actual runtime execution admitted. HYPOTHESIS: savedata-specific payload write/read wrappers; target bodies and native API links remain for R42.

Highest NEXT R42: inspect savedata-specific direct targets0x48bbc (CALL0x40090/0x402c9) and0x48660 (CALL0x40145) as independent original CALL-supported wrapper candidates. Revalidate their entrygraph/decoder boundaries, bounded branch/memory/PUSH sources and any structurally supported downstream CALL0x48c5e->0x4c5b4 / CALL0x486f0->0x4a8dc already known from native WriteFile/ReadFile contexts. Audit the four physical input slots and literal4000 separately from true ABI roles, actual count/product/buffer contents or fixed128-byte schema. Keep opaque open/API results, ESP/frame/return/alias ownership gaps and the0x400e4 conditional branch/alternate reopen distinct. Avoid generic CRT/allocator exhaustion. Native savedata payload/framing/checksum/migration/persistence, original server authority and cross-version equivalence remain OPEN. Stage A restoration before joint future-engine/game review; all system-family PARTIAL/OPEN gates unchanged.


## 2026-10-14 — TW1.0 R42 savedata-specific native IO path candidates

Source Action38574385118/job115887532644 SUCCESS at agent/tw10-savedata-r42-payload-wrappers-20261014 HEADebd97285d26daaaac51e96115302ea400eee915b. Authenticated transient archive/disc/runtime/save identities and exact R41 original derivative SHA2568c8474f75eb6adec5aa3939054f0fce26997152fb8e1f1424e74f18485c2471c rederived/strict-gated. Derived-only artifact11898767027 tw10-r42-original-payload-wrappers-derived ZIP SHA25610c695b16eb5a1be5d1f3fa8b4852c3c4b3593d6f410317ad0dfccd83da6b501; raw JSON147608 bytes SHA256545901acc97a027fb38a3937e00549b15f45b379c7c059e98ece6133c9541732. Independent immutable source run/head/branch/artifact identity, raw size/digest, negative controls and exact canonical JSON equality Action38574676282 SUCCESS at HEADe0c2dff028af3234fb028b7fa7642b1e92ca9b58.278 local/independent R42-R32 plus hardened R7 tests PASS. Originals transient, unexecuted/unpublished and unconditionally purged; local canonical JSON equals pinned derivative.

FACT (bounded original static): savedata-specific wrappers0x48bbc/0x48660 have coherent direct CFG support and conditional paths to native IO contexts via0x48c5e->0x4c5b4 /0x486f0->0x4a8dc. Four whole stack slots, two IMUL operands and three-slot native-call suffix syntax independently requalified. Opaque CALLs/loop joins block actual frame/owner/value binding; one write-definition shape0x48c93 remains outside the12-row sampler. HYPOTHESIS only: fwrite/fread roles and descriptor-like field. No actual IO/schema/persistence or historical system-family closure.

Highest NEXT R43: qualify early conditional caller-slot/token provenance and exact EDI multiplication source chain0x48bc3->0x48bc6 /0x48667->0x4866a, without evaluating original count/products or promoting literal4000 to an actual API byte count. Recover omitted write input definition0x48c93 and distinguish loop-carried/reentrant CALL barriers. Trace the three physical native-context input slots, especially [ESI+16] versus wrapper [EBP+20] source, and native callee buffer/count slot geometry only where bounded prefix evidence permits. Keep true FILE/CRT/descriptor/handle/alias ownership and return effects OPEN; no generic allocator/CRT exhaustion. Native savedata framing/checksum/migration/schema/persistence, original server authority and cross-version equivalence remain OPEN. Stage A restoration before joint future-engine/game review; all system-family PARTIAL/OPEN gates unchanged.


## 2026-10-14 — TW1.0 R43 conditional prefix symbols and complete sampled native definitions

Source Action38576786023/job115895874751 SUCCESS at agent/tw10-savedata-r43-prefix-product-sources-20261014 HEAD31ee18e7d81077b3b9075c8900c99b8b676b9005. Authenticated transient archive/disc/runtime/save identities and exact R42 derivative SHA256545901acc97a027fb38a3937e00549b15f45b379c7c059e98ece6133c9541732 rederived/strict-gated. Derived-only artifact11899434410 tw10-r43-original-prefix-product-sources-derived ZIP SHA2569f95bae3ada8f5aa74c7e8f9c739be2afd723dd17f20b160f6e8812d77713f86; raw JSON162163 bytes SHA256f5eeaac700c649f92e3fca5e7cbefa465879048f54d84b3896dcdb72115d7b42. Independent immutable source run/head/branch/artifact identity, raw digest/size, negative controls and exact canonical JSON equality Action38577142281 SUCCESS at HEADc63ea157452eecb8eee3b42a5f5a461863d517ee.304 local/independent R43-R32 plus hardened R7 tests PASS. Originals transient, unexecuted/unpublished and unconditionally purged; local canonical JSON equals pinned original derivative.

FACT (original bounded static): the two IMUL instructions have unique early EDI-load sources; bounded prefix/slot audits preserve conditional operand symbols and explicitly record two mutable+8 frame slots. The missing write shape is DEC EBX0x48c93;13/10 native definition shapes are now fully sampled. Loop-region and opaque-CALL alternatives remain distinct from actual input values/effects. Native object/count/buffer/schema/persistence remain OPEN.

Highest NEXT R44: qualify the three physical native-context input slots against independent callee-entry frame/read geometry at0x4c5b4 (CALL0x48c5e) and0x4a8dc (CALL0x486f0), under explicit32-bit stack/near-CALL and bounded alias-prefix conditions. Recover the source/update meaning of mutable wrapper[EBP+8] stores0x48bd2/0x48678 and retain their temporal relationship to initial read0x48bca/0x4866e and later native pushes. Do not assume an entry symbol survives opaque calls, a literal1*4000 is an actual IO byte count, or[ESI+16] is a proven owner/handle. Keep generic end-check caller0x4edb0 distinct from savedata wrapper0x486f0 even though both target0x4a8dc. Native framing/checksum/migration/schema/persistence, original server authority and cross-version equivalence remain OPEN; no generic allocator/CRT exhaustion. Stage A restoration before joint future-engine/game review; all system-family PARTIAL/OPEN gates unchanged.


## 2026-10-14 — TW1.0 R44 native slots, mutable count and buffer-shaped inputs

Final original source Action38579065734/job115903789605 SUCCESS at agent/tw10-savedata-r44-native-slots-mutable-20261014 HEAD8e6df983241cba248ed14e85fd03beb6f4b43171. Authenticated transient archive/disc/runtime/save identities and exact R43 original SHA256f5eeaac700c649f92e3fca5e7cbefa465879048f54d84b3896dcdb72115d7b42 rederived/strict-gated. Derived-only artifact11900549300 tw10-r44-original-native-slots-mutable-derived ZIP SHA25698d01e4a6d28c58dd241241fc9851aa3ddee0fe4e0d14d835714704e086afd14; raw JSON225095 bytes SHA25652c158d5f28f3ea287432e4b8214d306c491f158820808d7c4dd212c0646f5e8. Independent immutable source run/head/branch/artifact identity, raw digest/size, negative controls and exact canonical JSON equality Action38579428156 SUCCESS at HEAD662bb212594d61804db5279c01cffaa97b7d90d4.331 local/independent R44-R32 plus hardened R7 tests PASS. Original executable/media transient, unexecuted/unpublished and unconditionally purged; local canonical JSON equals pinned final derivative.

FACT (bounded original static): native input slot geometry, literal ESP adjustment operands, delayed write buffer-shaped read with opaque CALL barrier, read count-slot DEC-before-PUSH overlap and two different wrapper slot-rewrite source chains independently recovered. Read wrapper EBX->native EDI has only a conditional prefix register-symbol candidate. Third write slot/frame preservation and actual count/descriptor/buffer values remain OPEN; no original IO/schema/persistence accepted.

Highest NEXT R45: qualify original read count-slot DEC0x4a93b->PUSH0x4a959 and its reaching predicate/branch/input sources before native ReadFile0x4a960, keeping requested count, modified candidate count and actual transferred bytes separate. Revalidate that ReadFile import/PUSH identity and recover buffer/descriptor input candidates without actual values. Bound delayed write[EBP+12]0x4c623 behind original CALL0x4c60d: identify that direct/import call syntax if useful, retain frame-preservation unknowns and then inspect physical native WriteFile0x4c68c inputs. Do not pursue generic allocator/CRT owner exhaustion or force the missing write slot closed. Original savedata framing/checksum/migration/schema/persistence, server authority and cross-version equivalence remain OPEN. Stage A restoration before joint future-engine/game review; all system-family PARTIAL/OPEN gates unchanged.


## 2026-10-14 — TW1.0 R45 optional count path and native API operands

Original source Action38581331803/job115911685844 SUCCESS at agent/tw10-savedata-r45-count-api-inputs-20261014 HEADedf452d6fa218961250f400eb294bf4ab7b43fc5. Authenticated transient archive/disc/runtime/save identities and exact final R44 original SHA25652c158d5f28f3ea287432e4b8214d306c491f158820808d7c4dd212c0646f5e8 rederived/strict-gated. Derived-only artifact11904385284 tw10-r45-original-count-api-inputs-derived ZIP SHA2569d8f3eb3b087dc56008fa0ab4df4535f2131ad6f5b86a6b3cbcf2a77954eb015; raw JSON73217 bytes SHA25677919ef7e23f6a25afc66c2bc54b7b0f7da02df1b618e4a50743cda7ad26c21e. Independent immutable source run/head/branch/artifact identity, raw digest/size, negative controls and exact canonical JSON equality Action38581850803 SUCCESS at HEAD0cb7733529bfc76c368751769d36f96a06d2e3f2.353 local/independent R45-R32 plus hardened R7 tests PASS. Original executable/media transient, unexecuted/unpublished and unconditionally purged; local canonical JSON equals pinned original derivative.

FACT (original bounded static): the DEC has a bounded root-to-PUSH bypass; five ZF-source candidates and both first native API imports/five-slot suffixes independently recovered. Read buffer sources include copy and+1 address forms; write uses a local-frame address candidate. Delayed write CALL targets previously accepted helper0x4c761, but its actual effects and post-CALL frame preservation remain unknown. No actual requested/transferred count, file/handle/buffer/schema/persistence proof.

Highest NEXT R46: relate native read DEC0x4a93b, MOV ECX,EDI0x4a926 / LEA ECX,[EDI+1]0x4a942 and any intervening byte-store candidates to the bypass branches0x4a932/0x4a939 and first ReadFile0x4a960, using bounded path/input evidence without original byte/count evaluation. Recover the conditional count/buffer adjustment pairing, not a fictional unconditional decrement or text/pending-byte role. For native write, correlate CALL0x4c60d->0x4c761 caller suffix with the separately accepted R37 helper entry/SetFilePointer syntax only where slot evidence permits; retain opaque callee/seek/frame/alias effects. Keep generic end-check caller0x4edb0 and savedata wrapper0x486f0 distinct. Original savedata framing/checksum/migration/schema/persistence, original server authority and cross-version equivalence remain OPEN; no generic allocator/CRT owner exhaustion. Stage A restoration before joint future-engine/game review; all system-family PARTIAL/OPEN gates unchanged.


## 2026-10-14 — TW1.0 R46 conditional read adjustment and write-helper entry

Final original source Action38585030446/job115924602666 SUCCESS at agent/tw10-savedata-r46-adjustment-helper-slots-20261014 HEAD9f33f148cf7f4f994b435625744e5085c3d975a0. Authenticated transient archive/disc/runtime/save identities and exact R45 derivative SHA25677919ef7e23f6a25afc66c2bc54b7b0f7da02df1b618e4a50743cda7ad26c21e rederived/strict-gated. Independently accepted R37 helper memory/import surface rederived and exactly equal after the established normalized JSON digest a16c858a46d502dec5c99fe43528601f0bc89449c671a717198725c95aa496d0 (committed pretty JSON raw91061 bytes SHA256975e2e6d6014c72e576aa1ba9717843d7f8fc579d9a0d591e18482fe9503acad). Derived-only artifact11905875057 tw10-r46-original-adjustment-helper-slots-derived ZIP SHA2568e815487bdc4715ffb241401a7ddbcf8cdd3ea11fe319ae4c27f349b8e15bcde; raw JSON70648 bytes SHA2569aff27e1dadb33b1df5642e114488b238e83efcb97015a806c9e6527658c560e. Independent immutable source/run/branch/artifact identity, raw size/digest, strict tamper controls and exact canonical JSON equality Action38585353840/job115925764486 SUCCESS at HEAD654c36acf17f1a4f5bf0175f8fff31cc20540b5b.385 local/independent R46-R32 plus hardened R7 tests PASS. Original executable/media transient, unexecuted/unpublished and unconditionally purged.

FACT (bounded original static): optional count decrement, byte store and buffer+1 appear together on first-ReadFile structural paths or are jointly bypassed. The two bypass branch arms and shared local EDI source independently reproduced. Reused write helper entry matches only conditional caller slot0; later SetFilePointer stack reads remain behind an opaque CALL and unbound. No runtime byte/count/text/seek/frame/owner/schema/persistence FACT admitted.

Highest NEXT R47: qualify the one-byte source MOV AL,[EAX+5]0x4a934 and later MOV byte[EAX+ESI+5],10 at0x4a94c using bounded source/partial-register geometry; retain distinct EAX-before-load and EAX-after-reload0x4a940, no displacement-only alias or pending-byte/text-mode FACT. Relate local marker MOV dword[EBP-8],1 at0x4a945 and its earlier initialization to the first ReadFile0x4a960 continuation and local[EBP-12] result candidates, then bound count/return handoff toward the savedata read wrapper. Requested count, prefix adjustment and transferred count remain separate; do not execute or evaluate originals, infer successful IO/ABI/frame preservation, or pursue generic CRT/allocator ownership exhaustion. Native savedata framing/checksum/migration/schema/persistence, server authority and cross-version equivalence remain OPEN. Stage A restoration before joint future-engine/game review; all system-family PARTIAL/OPEN gates unchanged.


## 2026-10-15 — TW1.0 R47 byte slice and native/wrapper result syntax

Final original source Action38650978505/job116149395388 SUCCESS at agent/tw10-savedata-r47-byte-result-return-20261015 HEAD672dd89ac2cbf6b28941ac9156ff51330eaa6833. Authenticated transient archive/disc/runtime/save identities and exact R46 derivative SHA2569aff27e1dadb33b1df5642e114488b238e83efcb97015a806c9e6527658c560e rederived/strict-gated. Derived-only artifact11934900787 tw10-r47-original-byte-result-return-derived ZIP SHA256487e2f9ce520abe0eab1887ca84d1c3b89ec9ea86371e871e4e22c027e9d4418; raw JSON109781 bytes SHA256939d7080b61c2e8b3dc873cf0adec45ffc6b2c6154877aee787af6ab03dcf781. Independent immutable source/run/branch/artifact identity, raw digest/size, strict negative controls and exact canonical JSON equality Action38651158810/job116150004912 SUCCESS at HEADa5eabdbe44864096a04cacd824ec784f89452e48.410 R47-R32 plus hardened R7 tests PASS in both source and independent Actions. Local syntax compilation, raw ZIP/JSON custody and exact parsed/byte equality checked; local runtime tests were unavailable because this session lacks capstone/pefile. No claim of local execution of the410 tests. Original executable/media transient, unexecuted/unpublished and always purged.

FACT (original bounded static): the byte load affects only AL and reaches the byte store; later reset-shaped+5 store uses a separate EAX reload. Native local initialization/marker/result-addition and wrapper zero/-1/remaining-slot/buffer-advance shapes independently recovered. Cross-call EBP/EAX sources remain UNKNOWN_CALL, preventing actual alias, transferred-count, total-return or savedata schema/persistence promotion.

Highest NEXT R48: recover bounded native count/return exits around MOV EDX,[EBP-12]0x4a9a6 -> ADD[EBP-8],EDX0x4a9a9 and MOV EAX,[EBP-8]0x4aab4, with exact register sources, branch routes, memory-write/opaque-call barriers and no original arithmetic or frame-preservation assumption. Connect only the conditional native return syntax to savedata wrapper TEST0x486f8/CMP-1 at0x486fc, SUB[EBP+8],EAX0x48701 and ADD EBX,EAX0x48704; qualify loop/exit or element-count division candidates only where bounded evidence permits. Requested input product, native transferred-count-shaped result, prefix adjustment and wrapper element/remaining count must stay distinct. Do not infer actual byte totals/text/EOF/CRT/ABI/owner/schema/persistence or pursue generic allocator ownership exhaustion. Original server authority/cross-version equivalence remain OPEN. Stage A restoration before joint future-engine/game review; all system-family PARTIAL/OPEN gates unchanged.


## 2026-10-15 — TW1.0 R48 native return alternatives and savedata read loop

Final original source Action38652256320/job116153604235 SUCCESS at agent/tw10-savedata-r48-count-return-loop-20261015 HEADf8f052f85b9e61469d946195a779897b7cc47b92. Authenticated transient archive/disc/runtime/save identities and exact R47 original derivative SHA256939d7080b61c2e8b3dc873cf0adec45ffc6b2c6154877aee787af6ab03dcf781 rederived/strict-gated. Derived-only artifact11935740518 tw10-r48-original-count-return-loop-derived ZIP SHA25679b570f938e04745c452990d434af54492a45e706c0630a7f3b184732f9695ac; raw JSON87512 bytes SHA256f92a652b446a5433fa1afaa5708112c91bd39c1ef2c4fff27e69a419f013ccfa. Independent immutable source/run/branch/artifact identity, raw size/digest, strict negative controls and exact canonical JSON equality Action38652409955/job116154111413 SUCCESS at HEADe9fec63a18da9f430b2af6fefc2b9ec2a66565f5.442 R48-R32 plus hardened R7 tests PASS in both final source and independent Actions. Local syntax, raw ZIP/JSON custody and canonical byte equality checked; local runtime tests unavailable because capstone/pefile are absent, and are not claimed. Original executable/media transient, unexecuted/unpublished and always purged.

FACT (bounded original static): local count-load/add syntax reaches the local return-load region, whose nearest write candidates also include a distinct EDI overwrite. Native and wrapper RET EAX alternatives are enumerated; wrapper remaining-slot/buffer-advance paths loop structurally to the native CALL. Both distinct DIV input sources and EDX:EAX operand geometry are qualified. Actual byte/count/alias/frame/ABI/quotient/return/schema/persistence remain OPEN.

Highest NEXT R49: qualify the native local overwrite MOV[EBP-8],EDI0x4aab1 using exact EDI definitions and bounded predecessor/branch/memory barriers; distinguish it from ADD[EBP-8],EDX0x4a9a9 and other native return-source alternatives without evaluating byte conversion/counts. For the savedata wrapper, recover temporal DIV0x486e4 versus DIV0x48743 numerator/divisor provenance, especially mutable[EBP+20] and store0x4871d, initial product versus remaining-slot[EBP+8], and visible MOV EAX,EDI0x4873c->SUB0x48740. Do not infer permanent ABI roles from frame offsets, merge the two division operations or promote original quotient/return/transferred byte values. Keep unknown CALL/frame/alias effects explicit; native savedata schema/framing/checksum/migration/persistence, server authority and cross-version equivalence remain OPEN. No generic allocator/CRT ownership exhaustion. Stage A restoration before joint future-engine/game review; all system-family PARTIAL/OPEN gates unchanged.


## 2026-10-15 — TW1.0 R49 EDI overwrite and temporal divisor slots

Original source Action38683095588/job116251797902 SUCCESS at agent/tw10-savedata-r49-overwrite-temporal-slots-20261015 HEAD4d1828be1c0af1ce003f0fefd4a3330e162f5e88. Authenticated transient archive/disc/runtime/save identities and exact final R48 original derivative SHA256f92a652b446a5433fa1afaa5708112c91bd39c1ef2c4fff27e69a419f013ccfa rederived/strict-gated. Derived-only artifact11949650069 tw10-r49-original-overwrite-temporal-slots-derived ZIP SHA256824c4a5faff0947e55d79a777cdac0ab8912fbe51f15e1fe272fc9e2b614c942; raw JSON140909 bytes SHA256fbb25583fa019e496fd0f4d06ef1b441731547e559dcb818d5244321cc3f0ab6. Independent immutable source/run/branch/artifact identity, raw size/digest, strict negative controls and exact canonical JSON equality Action38683345301/job116252568395 SUCCESS at HEAD1e1b172418179dd11bd5f367529cc3c7858dd26d.468 R49-R32 plus hardened R7 tests PASS in both source and independent Actions. Local syntax, raw ZIP/JSON custody and canonical byte equality checked; local runtime tests unavailable because capstone/pefile are absent, and are not claimed. Original executable/media transient, unexecuted/unpublished and always purged.

FACT (bounded original static): native EDI overwrite is sourced by a final SUB whose inputs retain INC and opaque-CALL alternatives. A TEST/JE branch can bypass that overwrite. The same wrapper[EBP+20] slot is read then overwritten from two field-load sites or literal4096 before comparison/division candidates; final numerator cannot be bound to the initial product across opaque calls. Actual byte/count/ABI/alias/division/schema/persistence remain OPEN. Helper scope is bounded; next work returns to savedata-specific caller consumers.

Highest NEXT R50: return to original savedata-specific CALL0x40145->0x48660. Requalify its exact caller/decoder/entrygraph support and physical buffer/product inputs against accepted R41/R42 evidence, then inspect a bounded post-wrapper continuation, returned-value predicates and first buffer consumers for application-level field/record/framing checks. Keep opaque wrapper/open results and caller register/frame/alias barriers explicit; do not convert literal4000, a multiplication, a return candidate or historical128-byte observation into a proven read size/schema. Keep the separate write callers0x40090/0x402c9 as distinct contexts if needed for a later read/write correspondence. Native conversion/ABI/owner gaps from R49 remain documented OPEN and off the critical path unless needed for a specific savedata consumer. No generic allocator/CRT ownership exhaustion. Savedata payload/framing/checksum/migration/persistence, original server authority and cross-version equivalence remain OPEN. Stage A restoration before joint future-engine/game review; all system-family PARTIAL/OPEN gates unchanged.


## 2026-10-15 — R50 savedata caller/application consumers accepted

FACT (bounded original static): savedata-specific read caller and processing entry requalified. Postprocessor comparisons57/127, register literals4/5, word checks and byte stores at global base/base+57 are recorded with exact widths. Actual length/tag/migration/alias remain unknown. Processor36 memory/control shapes are sampled to32; the omitted4 are explicit next work. Stage A gates unchanged.

Original source Action38684319450/job116255602386 SUCCESS at HEAD49d1f536710facf1142b5218e05304616f11791a, branch agent/tw10-savedata-r50-caller-consumers-20261015. Artifact11948569898 tw10-r50-original-caller-consumers-derived ZIP SHA25687d1833da95abc1a7977db7c395c132ecd89d09b13b5b61ec8bcbc5ba146eec7; raw JSON163325 bytes SHA2560badd1423f403a9e8a246a40518a68ee5a1bd67d380ea7ab3460fc3c607c3e94. Exact R49 and R41 original-derived reports revalidated before extension. Independent Action38684734727 at HEAD498820d86998f2d7b4dcaa2e7a6a85f38e33bee6 authenticates immutable source/run/branch/artifact identity, exact raw size/digest, strict report, canonical byte equality and separately regenerated application-consumer contract. Source494 tests and independent513 tests (494 plus19 metadata-consumer controls) PASS. Local19 metadata tests/syntax/custody PASS; full local runtime tests unavailable because capstone/pefile are absent. No original program executed/published; transient original media purged.

Highest NEXT R51: qualify savedata application CMP EAX,57 at0x40195 and CMP EAX,127 at0x401c9 using exact stack-load/processor-output sources and bounded flag/control routes; separately qualify word comparisons at0x4019f/0x401e4, register literal4/5 definitions, byte stores at0x401a8/0x401af and their relation to global RVA0x13fbdac. Revisit processor0x47160 with all36 memory/control shapes, including the4 excluded by the R50 sample, and bound its input/output/algorithm structure. Do not assume decoded lengths, tag versions, migration, endianness, buffer alias or executed paths from these literals. Keep read/write callers distinct and opaque CALL/frame barriers explicit. Savedata schema/framing/checksum/persistence, original server authority and cross-version equivalence remain OPEN. Stage A restoration precedes joint future-engine/game review; system-family PARTIAL/OPEN gates unchanged.


## 2026-10-15 — R51 processor and conditional caller geometry accepted

FACT (bounded original static): processor115-node full instruction inventory and all36 memory/control shapes recovered. Normal RET0x47268 yields conditional net near-CALL ESP change0; the caller ECX/pre-CALL+32 coordinate matches post-CALL load[ESP+32] under that bounded model. All seven signed divisions and final byte NOT/subtraction syntax recorded. Source dependencies remain bounded:39 definitions,19 retained,11 pending expansion; schema/algorithm/value/alias/persistence remain OPEN.

Original source Action38719176573/job116369203266 SUCCESS at HEADee32f6d16f3dbfeabbb9d73020b64f83f47924dd, branch agent/tw10-savedata-r51-processor-stack-consumers-20261015. Original archive/disc/runtime/save authenticated transiently; exact accepted R50 derivative rederived. Derived-only artifact11963713395 ZIP SHA2563e02a0c79114b8a3e2817a63ef4c6d280944435f4ad1106a213781484c2b4a8b; raw JSON284533 bytes SHA25615f54e5de8d1d20128fb7d948b54f13a0e3f6cf372eca203cbc7bb8adc473052. Independent Action38719540769/job116370411001 SUCCESS at HEAD26c3fc3698f1f930a0acf8296b145fdbe34fdd0e: immutable run/head/branch/artifact, exact raw size/digest, strict primary replay, canonical byte equality, exact nested R50 canonical bytes, postcall metadata contract regeneration and differential old/new stack-model equality at all115 instruction sites. Source553 tests PASS; independent567 tests PASS. Local36 pure metadata tests plus syntax/custody/prefix checks PASS; local capstone/pefile unavailable, so full local runtime tests are not claimed. Original media/executable never executed or published and always purged.

Highest NEXT R52: qualify the seven processor IDIV sites0x47170/0x4719f/0x471b7/0x471d6/0x471ee/0x4721e/0x4722a with exact CDQ EAX-preservation/EDX-sign-extension syntax and bounded register-source expansion, keeping signed dividend, divisor, quotient and remainder distinct. Resolve the11 source-expansion pending definitions and19-of39 source-definition sample limitation using focused groups rather than suppressing caps. Bind only conditional caller ECX/pre-CALL+32 -> processor entry+20 -> ESI store0x4717c and post-CALL load0x4018e, with stack-slot mutation and memory-alias barriers explicit; qualify LEA EAX-1 -> ECX/store syntax and application57/127 checks without evaluating original bytes. Recover subtractive/NOT byte operations and loop predicates as syntax before assigning a historical algorithm/version/schema meaning. Native schema/framing/checksum/migration/persistence, original server authority and cross-version equivalence remain OPEN; Stage A restoration precedes joint future-engine/game design. System-family PARTIAL/OPEN gates unchanged.


## 2026-10-15 — R52 conditional division/output source graphs accepted

FACT (conditional architecture/source metadata):10 CDQ observations preserved with a separate EAX-preservation/EDX-sign-extension overlay; all7 signed-division source groups and11 legacy-pending register groups close without query caps. All39 legacy definition shapes recovered. Forward/reverse algorithms agree on60 queries; output-store sources, five explicit alias-write barriers and10 processor predicates recorded. Actual memory/arithmetic results, algorithm/schema/tag/migration/persistence remain OPEN.

R52 source Action38721170772/job116375809931 SUCCESS at HEAD5bdf801831f2a8198ce49c5f91c04d583f03a5ec, branch agent/tw10-savedata-r52-cdq-sources-20261015. It authenticates R51 original Action38719176573/HEADee32f6d16f3dbfeabbb9d73020b64f83f47924dd/artifact11963713395 and its284533-byte SHA25615f54e5de8d1d20128fb7d948b54f13a0e3f6cf372eca203cbc7bb8adc473052 canonical metadata before deriving R52. No original archive/disc/executable or savedata bytes were downloaded or evaluated this round. R52 artifact11964589288 ZIP SHA2560c4346b23854cde9452a0f803bfcb5f5d36335563df0276101c08e8422d35d54; raw canonical252332 bytes SHA25699c9252bf3a982db565ab29f43d27e67b2c34978a44990564d74d75949a15179. Independent Action38721359439 at HEAD9e2e0a7cb0170d9e1804272e6be92d522fd0938f SUCCESS authenticates both immutable R51/R52 run/head/branch/artifact chains, exact source/report sizes and SHA256, strict R51 validation, R52 canonical byte regeneration/equality and reverse-predecessor audit. Source and independent611 tests PASS (567 inherited plus44 R52 controls). Local44 pure metadata tests, syntax, ZIP/raw equality, old-prefix and tree checks PASS; full inherited local runtime tests unavailable because capstone/pefile are absent and are not claimed.

Highest NEXT R53: reconstruct a conditional savedata-specific transform specification from the complete pinned R51/R52 numeric metadata. Follow the caller literal0 seed/mode physical slot only under explicit entry/frame/non-alias/normal-return conditions. Qualify the source-byte selection, possible omitted-byte/output-index shift, signed remainder and low-byte IMUL/subtraction paths, final NOT predicates and output-length-shaped LEA/count-minus-one store; connect only conditional results to the application57/127 and word4/5 checks. Prefer bounded symbolic relations and invented-input counterexamples before any algorithm label or engine-neutral reference model is admitted. Keep generic nonzero-seed branches separate, retain divide-error/invalid-count/overflow and memory-alias preconditions, and do not evaluate original save bytes or claim a proven payload schema/version/migration/persistence. Original server authority/cross-version equivalence remain OPEN. Stage A restoration precedes joint future-engine/game design; system-family PARTIAL/OPEN gates unchanged.


## 2026-10-15 — R53 conditional transform specification accepted

FACT (conditional reference only): zero-seed key selection/removal, shifted output-index subtraction and final NOT relation reconstructed from pinned metadata and verified with1029 invented fixtures plus10 generic-seed numerical fixtures. Both models agree;112 observed instructions exercised and3 negative-index repairs explicitly excluded by the model domain. Actual input/output bytes, schema/tag/migration/writer/persistence remain OPEN; invented inverse is not historical writer evidence.

R53 source Action38723269655/job116382826823 SUCCESS at HEAD3b65aaff0d41e8d209c7212eabc1146d97631b96, branch agent/tw10-savedata-r53-conditional-transform-20261015. Authenticates immutable R51 original-derived Action38719176573/artifact11963713395, raw284533-byte SHA25615f54e5de8d1d20128fb7d948b54f13a0e3f6cf372eca203cbc7bb8adc473052; and R52 Action38721170772/artifact11964589288, raw252332-byte SHA25699c9252bf3a982db565ab29f43d27e67b2c34978a44990564d74d75949a15179. R53 artifact11966653083 ZIP SHA2561b6355be01eba8ba96af8c178ee32001770cf9607675482a3e2cc8f18cafd957; canonical spec104275 bytes SHA25626bbdff472638081cd7e26945350598bf89a75a690c5c4205c2d491ad62e8dd5. Independent Action38723447688 at HEAD681c2c76dfe34eec4658ebf11e2f785856765072 SUCCESS verifies all three immutable source/run/head/branch/artifact chains, sizes/digests, exact prior canonical bytes, strict R51/R52 validation and exact R53 reproduction/equality. Source and independent656 tests PASS (611 inherited plus45 R53 controls). Local45 tests, syntax, raw ZIP/spec equality, historical-prefix and tree checks PASS; full inherited local runtime tests unavailable because capstone/pefile are absent and are not claimed. No original archive/executable/save payload retrieved or evaluated this round; only metadata and generated invented fixtures used.

Highest NEXT R54: qualify the savedata application read/write correspondence around conditional57/word4 normalization stores0x401a8/0x401af and direct CALL0x401b6->0x40020. Audit the write-side prefix0x40020 before the already accepted filename-push0x40064/write CALL0x40090, recover its processing-call identity, physical slots, frame/count/buffer sources and bounded entrygraph/control support, then compare any historical write transform with R53 only under explicit preconditions. The invented inverse fixture generator is not historical writer evidence. Existing R51/R52 instruction shapes are sufficient for the read processor but do not contain this write prefix: verify existing metadata first and retrieve authenticated originals only for that identified missing scope. Keep word4/5, lengths57/127, new byte at+57 and possible writer128-byte framing as separate candidates until linked. Do not evaluate original save contents or promote actual ABI/alias, field schema/checksum/migration/persistence, original server authority or cross-version equivalence. Stage A restoration precedes joint future-engine/game design; system-family PARTIAL/OPEN gates unchanged.


## 2026-10-15 — R54 historical writer transform located and conditionally mapped

Original source Action38724589059/job116387179386 SUCCESS at HEAD660a051f9b58ef596fb2fdf8f27bfc9fd321a7a0, branch agent/tw10-savedata-r54-writer-prefix-20261015. Archive/disc/runtime/save identities authenticated transiently; exact accepted R51 report SHA25615f54e5de8d1d20128fb7d948b54f13a0e3f6cf372eca203cbc7bb8adc473052 rederived and validated before extension. Derived-only artifact11967805220 ZIP SHA256a857094d202033ea378406fc3c5dae5580c984416181a80f497a6540466ffa5c; raw JSON132329 bytes SHA256635e80079eb594218c849facd2ea1ba8b0c9160142fc017182d17ba8f1c62387. Independent Action38725044477/job116388679063 SUCCESS at HEADd064e83ae3e14f4b6fede56b0f52f7ba2e7c8215 authenticates immutable source/run/head/branch/artifact, exact raw size/digest, canonical byte equality, strict inventories and separately regenerated pure writer contract. Legacy R38/R44/R50 and R51 stack algorithms agree at all201 instruction sites. Source664 tests PASS; independent688 tests PASS (656 inherited plus32 R54 controls). Local20 pure metadata tests and syntax/custody checks PASS; local capstone/pefile unavailable, so full local runtime tests are not claimed. Original executable/save payload never executed/evaluated or published; transient original media purged.

FACT (authenticated bounded original instruction metadata and conditional geometry):

- Normalization CALL0x401b6->0x40020 is supported by the original entrygraph, alongside exact R51 requalification and unchanged57/word4/global byte-store syntax. Writer graph55nodes/54edges; prefix direct callees0x49160 graph17nodes/18edges and0x47010 graph129nodes/143edges. All three inventories are complete inside768-byte/256-node bounds, without frontier/node caps. Structural traversal assumes returning calls; no executed path is proved.
- Writer prefix MOV EAX,4132 at0x40020/CALL0x40025->0x49160 is followed by PUSH ESI/EDI, MOV ECX,31 and global-immediate25148844 into ESI. REP MOVSD0x4003e, MOVSW0x4004c and MOVSB0x40059 are distinct numeric observations. The conditional expression31*4+2+1=127 requires valid repeat count/direction/segments/registers/addresses; it is not a measured original copy size. The helper writes ESP from ECX, so its actual frame effect remains unknown.
- CALL0x4005a->0x47010 is the historical transform candidate. The earlier generic suffix scanner correctly stops at MOVSB and reports no physical pushes. A separately bounded straight-line0x40040..0x4005a replay retains six pushes across neutral-to-ESP instructions: pre-CALL offsets0:EDX,4:literal127,8:literal0,12:ECX,16:EAX,20:literal4000. Saved ESI/EDI outside that window are not arguments. Local LEAs0x40036/0x4003a/0x40045/0x40052 have conditional pre-CALL coordinates36/32/164/36. This binds numeric coordinates only, not original addresses or ABI values.
- Processor conditional entry coordinates+4/+8/+12/+16/+20/+24 match those six physical slots. Entry+8 load feeds LEA count+1 at0x4701c; entry+24 is capacity-shaped; normal branch stores count+1 through entry+20 at0x47068. Capacity/error branches remain retained. The processor has no CALL and one normal RET0x47155; conditional numeric PUSH/POP balance is0. ESP-relative slot entry+16 is later overwritten at0x470f5; equal slot spelling after that point cannot reuse the initial pointer value.
- All five IDIV sites0x4707a/0x47097/0x470e2/0x47108/0x47134, byte accumulation ADD0x47090, NOT0x470c2, key-shaped insertion0x47124, byte IMUL and additive paths0x47117/0x47140 are retained. The read processor separately retains count-1, subtraction and later NOT. These jointly support a conditional inverse hypothesis; no numerical writer/read equivalence is admitted this round. The writer mutates its input and has an input-dependent byte accumulator, unlike the arbitrary-key R53 invented inverse fixture generator.
- Existing R41 write/close identities and physical suffixes at0x40090/0x400ac compare exactly to R54; all10 prior continuation rows and prior narrow graph nodes/edges are preserved as subsets. Opaque open/write/close effects and actual returned counts remain unknown. Literal127 and conditional count+1=128 do not prove that an original128-byte write occurred.

HYPOTHESIS: a conditional127-byte application snapshot is transformed into128 bytes and may correspond to the R53 read relation under valid zero-seed arguments. OPEN: actual REP/frame/alias/ABI values, arithmetic/error paths and key relation, original bytes/field/tag meanings, normalization/migration/checksum/schema/persistence, original server authority and cross-version equivalence. All Stage A system-family PARTIAL/OPEN gates unchanged.

Highest NEXT R55: derive a conditional historical writer0x47010 reference specification from the exact R54 complete129-row numeric inventory and R51/R52 read metadata. Recover the byte accumulator/key relation before the in-place NOT pass, seed-dependent insertion/index arithmetic, count+1/capacity branches, signed division and byte ADD/IMUL semantics. Qualify the zero-seed127->128 candidate against the read128->127 relation on invented inputs only, with a separately authored formula and bounded numerical instruction-shape model. Preserve writer input mutation, key derived from input rather than arbitrary R53 inverse keys, partial-register rules, aliased/out-of-capacity/error preconditions, and generic seed paths. No original payload evaluation or binary execution. Existing metadata is now sufficient for this arithmetic task; do not retrieve the original archive again without a specific missing-evidence reason. Stack helper0x49160 actual frame effect, REP direction/segments/count validity, opaque open/write/close, native output-length-to-write binding, word4/5 semantics, normalization/migration/schema/checksum/persistence, server authority and cross-version equivalence remain OPEN. Stage A restoration before joint new-game design; system-family PARTIAL/OPEN gates unchanged.


## 2026-10-15 — R55 conditional historical write/read transform relation accepted

R55 source Action38728999042/job116401820264 SUCCESS at HEAD230726474ed0ed9dae228f97da389401b7554b4f, branch agent/tw10-savedata-r55-writer-inverse-20261015. Authenticates immutable R51/R52/R53/R54 source runs/artifacts and exact canonical numeric bytes before extension. R54 source132329-byte SHA256635e80079eb594218c849facd2ea1ba8b0c9160142fc017182d17ba8f1c62387 and R53 spec104275-byte SHA25626bbdff472638081cd7e26945350598bf89a75a690c5c4205c2d491ad62e8dd5 pinned. R55 artifact11969477120 tw10-r55-conditional-writer-read-spec ZIP SHA256569d762983ff27fb19078b825f31d444ec6cee5152efc0fccd78613aa1b3933a; raw spec103165 bytes SHA2569f98d60d00600ffea0838aee7962a1811323eedcc97d02715f3dd846b00fc863. Independent Action38729256210/job116402678124 SUCCESS at HEAD05535ed2621690954c4cb7c6264a80f9065f5bc5 authenticates all five immutable source/run/head/branch/artifact chains, exact sizes/digests, prior canonical bytes, strict R54 inventories/independent201-site stack replay, exact R53 regeneration and exact R55 specification reproduction/equality. Source and independent734 tests PASS (688 inherited plus46 R55 controls). Local46 pure-model tests, syntax, ZIP/raw equality and historical-prefix checks PASS; full inherited local runtime tests unavailable because capstone/pefile are absent and are not claimed. No original archive/disc/executable or save payload downloaded or evaluated; only numeric metadata and invented arrays used.

FACT (conditional metadata-derived arithmetic specification, invented fixtures only):

- Complete129-row/143-edge historical writer candidate0x47010 inventory retained. A separately configured numerical writer model dispatches26 observed mnemonics, six fabricated argument slots, mutable invented input, disjoint output/count/stack and explicit capacity. Existing R53 read model remains unchanged. ADD/JG/JMP support is new; width/signed arithmetic helpers remain shared with R53 and are checked by separate hand vectors/flag controls.
- With valid zero seed,1<=N<=3999 and capacity>=N+1<=4000, the key relation is K=sum(original invented input bytes) mod256. Each byte is accumulated before its optional in-place NOT. T[j]=A[j] XOR255 when j mod5==0 OR j mod2==0, otherwise A[j]. Output[0]=K; output[j+1]=(T[j]+(((j+1)*(j+1)) mod7)*K) mod256; stored count=N+1. These are conditional model relations, not evaluated original bytes. The earlier arbitrary-key R53 invented inverse corresponds to the historical writer only when its key equals this input-dependent sum.
- The R53 read subtraction followed by the same NOT cancels the normal zero-seed write relation. Physical127/count,0/seed,4000/capacity therefore give the conditional127->128->127 model equation. Actual application REP/frame/ABI/alias validity, passed native write count and persistence are not proved. A byte-sum key does not establish a historical checksum-validation mechanism or record field schema.
- Capacity fallback0<=C<N+1 copies input[:C], stores C and does not mutate input or transform. N0/C0 returns empty; N0/C>=1 reaches modeled division by zero. Negative counts/capacities, original alias/invalid-memory cases stay excluded. Fabricated alias/count substitutions are rejected. Key scratch at conditional entry ESP-1 overlaps the high byte of saved ECX; ECX is deliberately not required to preserve its initial sentinel. Entry+16 output-pointer slot is overwritten0x470f5 and later reads use current modeled memory.
- 1292 zero-seed fixtures include all256 derived keys at lengths1/2/3/7/127, additional57/255/3999 and capacity boundaries;7 use capacity fallback. Normal output/count/input mutation agree with an independent compact formula; normal outputs roundtrip through both R53 numerical read and compact read formula. Ten additional signed/nonzero-seed fixtures roundtrip numerically; no general nonzero-seed reference formula is admitted.
- Zero-seed writer/read fixtures total3933134 numerical steps; maximum writer fixture164817. Fixture union exercises126 of129 writer shapes. Three negative-index repair shapes0x470a6/0x470a7/0x470aa remain retained and explicitly domain-excluded: the index is nonnegative below3999. No claim of129 executed instructions or exhaustive/formal all-buffer proof. Hand vector[1,2,3]->[6,4,26,8], all256 single-byte[v]->[v,255], high-bit/wrap keys, wrong-key/divisor/missing-NOT counterexamples, signed JG limits, aliases, error and custody/report corruption supplement the fixtures.

OPEN: actual frame/REP/argument/alias validity, opaque native open/write/close and successful returned counts, original bytes/fields/tags/version meanings, normalization/migration/checksum/schema/persistence, original server authority and cross-version equivalence. All Stage A system-family PARTIAL/OPEN gates unchanged.

Highest NEXT R56: bind conditional R55 writer output/count to the savedata application write request0x40090 using the exact R54 numeric inventory. Qualify the specific frame helper CALL0x40025->0x49160 (EAX literal4132), including its page-probe reads, ESP rewrite, saved ECX/return-address relocation and conditional near-return geometry on invented storage only. Then replay caller REP/MOVS copy127 candidate, six transform pushes, post-transform/open ADD ESP,32, load0x40080, write-buffer LEA0x40086, write physical suffix and post-write count comparison0x4009c. Keep direction flag/segments/address validity and opaque open/write/close preservation/alias effects explicit. Separate conditional output128/write-request correspondence from actual native write/flush/close/persistence success. Prefer pinned metadata; retrieve originals only for an identified missing scope. Do not expand generic CRT ownership work, evaluate original payloads, or promote field schema/tag/version/migration/checksum/server authority/cross-version equivalence. Stage A precedes joint new-game design; all system-family PARTIAL/OPEN gates unchanged.


## 2026-10-15 — R56 conditional helper/application/write-request bridge accepted

R56 source Action38730761697/job116407664800 SUCCESS at HEAD453ff20ca9f30ca9f05b1b42551508c7053f9cb5, branch agent/tw10-savedata-r56-application-frame-20261015. Authenticates immutable R51/R52/R53/R54/R55 metadata custody and exact bytes; R54 raw132329-byte SHA256635e80079eb594218c849facd2ea1ba8b0c9160142fc017182d17ba8f1c62387 and R55 spec103165-byte SHA2569f98d60d00600ffea0838aee7962a1811323eedcc97d02715f3dd846b00fc863 pinned before extension. R56 artifact11969389801 tw10-r56-conditional-application-frame-spec ZIP SHA25695938cabdcd015aa3e273cc541bd38e1fbd7f8cdf91716b895c7b132abf2e028; canonical raw67492 bytes SHA256db5628403b366e706e212bd7627f40861097d78bfb3f3acb0d95598bce70981c. Independent Action38731138905/job116408925725 SUCCESS at HEAD601b5f63bf47c0c1d799ed9fd7b94a3d8d07af94 authenticates all six immutable source/run/head/branch/artifact chains, strict R54 inventory/stack replay, exact R55 regeneration and exact R56 reproduction/equality; a separate all-path caller ESP algebra agrees at55 sites and preserves unknown downstream states without opaque-call stack premises. Source780 tests PASS; independent788 tests PASS (734 inherited plus54 R56 controls). Local54 pure metadata/model/algebra tests plus syntax, ZIP/raw equality and historical-prefix checks PASS; full inherited local runtime tests unavailable because capstone/pefile are absent and are not claimed. No original archive/executable/save payload retrieved, evaluated, executed or published; only numeric metadata and generated invented storage/stubs used.

FACT (conditional numeric metadata specification and invented-storage verification only):

- All17 helper0x49160 shapes/18edges and55 caller0x40020 shapes/54edges retained. Helper and caller numerical models dispatch only observed bounded shapes on fabricated storage. CALL observations dispatch explicit helper/transform model abstractions or invented open/write/close stubs; they do not execute original code or any OS/native API.
- Under valid32-bit memory/near-return geometry, the helper restores saved ECX and relocates the return marker so caller continuation ESP is S-requested_amount. Literal4132 gives conditional S-4132.305 invented helper amounts in0..65536 include0..256, page boundaries and literal4132; all17 shapes exercised. Whole-page probe offsets are followed by -amount, including a duplicate final address for exact page multiples. Failed invented probes stop qualification; actual page-probe/allocation success remains unknown.
- With clear DF, compatible flat source/ES segments, valid initialized/disjoint storage,31 repeated dword copies plus word/byte copies make a127-byte invented snapshot. Conditional S-relative regions are length cell[-4132,-4128), snapshot[-4128,-4001), one-byte padding[-4001,-4000), output capacity[-4000,0). REP validity/actual source values remain conditional.
- Six transform slots map to snapshot,count127,seed0,output,length-cell,capacity4000. With explicit opaque-call stack and live-memory preservation, post-open load0x40080[ESP+8] and post-write load0x40095[ESP+24] share S-4132. Write LEA0x40086 gives S-4000; CALL0x40090 physical slots are buffer(S-4000),literal1,count128,opaque-open-return shape.256 invented snapshots spanning every derived key byte verify requested bytes/count equal R55 model output. No file bytes are written.
- The five witness pre-instruction ESP coordinates at0x4005a/0x40069/0x40080/0x40090/0x40095 are -4164/-4172/-4140/-4156/-4156. Independent all-path ESP algebra checks all55 sites and three exit coordinates0. Without opaque-stack premises it retains the known prefix and marks post-open coordinates unknown, rather than assuming returning calls have zero actual effect.
- Two invented memory-clobber counterexamples preserve stack geometry but change request count128->127 or output content. Thus same address is not sufficient for count/content identity. Without opaque-memory preservation the report explicitly withholds content/count binding; unknown DF/segments/helper validity similarly prevent qualification.
- Seven invented open/write/close-return cases plus successful fixtures cover all55 caller shapes. Unsigned JAE0x4009e follows CMP0x4009c. Short-return path gives literal0 without close-call candidate in this bounded graph; >=count reaches CALL0x400ac then MOV EAX,1 at0x400b4 overwrites the close-return-shaped result. High-bit invented write returns also take the unsigned branch. These are syntax/model control facts, not native error conventions, successful close/flush/persistence or an actual resource-leak claim.

OPEN: actual helper/REP/alias/callee preservation, original wrapper returned-count/error meanings and native write/close/flush success, original payload/fields/tags/version/schema/checksum/migration/persistence, server authority and cross-version equivalence. Stage A system-family PARTIAL/OPEN gates unchanged.

Highest NEXT R57: qualify actual savedata write-wrapper return/count/error syntax at CALL0x40090->0x48bbc and close-wrapper CALL0x400ac->0x4856c, separating the caller's unsigned JAE/literal1 from native write/close success. R42 retains a complete106-node/119-edge write-wrapper graph and106 numeric stack effects but only5 early operand shapes and1 frame definition; this is insufficient to reconstruct all returned EAX/count/control paths. Audit all existing R42-R49 metadata first, then retrieve authenticated originals only for missing complete write-wrapper/close-wrapper numeric inventories. Requalify exact prior original metadata, recover bounded complete instruction/branch/call/return shapes and preserve opaque nested calls, alias/frame and actual return/error-value gaps. Prioritize savedata-specific return/cleanup obligations, not generic CRT ownership exhaustion. Do not evaluate original payloads or promote a successful actual128-byte native write/close/flush, field schema/checksum/migration/persistence, original server authority or cross-version equivalence. Stage A restoration precedes joint new-game design; all system-family PARTIAL/OPEN gates unchanged.


## 2026-10-15 — R57 write/close return syntax and buffering-shaped path accepted

R57 original source Action38739896846/job116438533408 SUCCESS at HEAD1bb5924185c21a73d6e196f9764871b5b3593c08, branch agent/tw10-savedata-r57-write-close-returns-20261015. Original archive/disc/runtime/save identities authenticated transiently; accepted R54 report132329-byte SHA256635e80079eb594218c849facd2ea1ba8b0c9160142fc017182d17ba8f1c62387 rederived and strictly validated before extension. R42 write graph/effects and retained operand shapes match exactly. Derived-only artifact11976200967 tw10-r57-original-write-close-derived ZIP SHA256425595389a34ee483a855bd8669f404dd2c9b65695f54fddeb95b2510da4a042; raw203899 bytes SHA2563e562ab02a80e0f6516f8a91c93b897eef05f606be62f1df5cb48686d64114e6. Independent Action38740708599/job116441358622 SUCCESS at HEAD6254425e4e1f8bc03515022c0a500faf97255359 authenticates all seven immutable R51-R57 source/run/head/branch/artifact chains, sizes/digests, exact canonical bytes, prior R56 reproduction, strict R57 report, independent reverse return sources and separately regenerated contract. Contract3654 bytes SHA2569c35c0d934b7d98503c62c210eb9f216b158ae727dadda7d8323545930cd17d7. Source796 tests PASS; independent826 tests PASS (788 inherited plus38 R57 controls). Local28 pure metadata/contract/reverse controls, syntax, ZIP/raw equality and historical-prefix checks PASS;10 additional primary-guard controls run remotely with capstone/pefile, which remain unavailable locally. Original client/save payload never executed/evaluated or published; transient original media purged.

FACT (authenticated nonexecuting original syntax and conditional return/control contracts):

- Write wrapper0x48bbc has complete106-node/119-edge inventory; close wrapper0x4856c has35nodes/38edges. Both fit768-byte/256-node bounds with no frontier/node cap, and caller-to-root support is present in the original entrygraph. Write has14 conditional predicates/12 explicit-memory-write shapes; close has4 predicates/2 memory-write shapes. Each has one bounded RET candidate. Structural CALL continuation is an assumption, not execution proof.
- Raw-decoder forward and independent reverse register propagation agree on all14 write-return and6 close-return queries, with no focused query cap/pending definitions. Query closure is not memory/value/ABI closure; CALL effects remain opaque and no CDQ overlay is applied.
- Write RET0x48cb1 direct EAX definition candidates are XOR EAX,EAX0x48bd9, MOV EAX,[EBP+16]0x48caa and unsigned DIV[EBP+12]0x48cc1. Conditional initial entry+4/+8/+12/+16 roles are buffer/element-size/count/object shapes under EBP=entry ESP-4 and valid preserved frame/non-alias premises. The object-shaped frame slot is later overwritten with a block quantity. Normal completion loads the count-shaped slot; partial/error syntax subtracts EBX remaining from an EAX snapshot, zeroes EDX and divides by element-size-shaped memory. Actual original products/counts/divisors/quotients and successful division remain unknown.
- Native-context CALL0x48c5e->0x4c5b4 has CMP EAX,-1 at0x48c66 and a separate unsigned short-return-shaped comparison0x48c70/0x48c72. These routes reach OR[ESI+12],0x20 at0x48cb2 and partial-quotient syntax. The -1 pattern is static syntax, not an admitted native return/error convention.
- A verified structural path passes through CALL0x48c1a->0x4aae0 and normal count load0x48caa/RET0x48cb1 while excluding direct native-context CALL0x48c5e. Memory-copy-shaped input/object updates support a buffering hypothesis. Thus a full count-shaped return does not itself establish that the direct native write ran or that bytes reached disk; actual path feasibility remains OPEN.
- Close RET0x485c1 direct EAX source candidates are OR EAX,-1 at0x4857c and MOV EAX,EDI0x485b9. Flag masks0x40/0x83, initial EDI all-ones, first helper CALL0x48586->0x4a657 and MOV EDI,EAX0x4858c, later sign test0x4859e/JGE0x485a0, optional object+28 cleanup and flag clear0x485bb are retained. Later CALLs0x4858e/0x48596/0x485af keep result/register preservation unresolved. The shared0x4a657 target is also reached by write CALL0x48c38. No actual close/flush success or descriptor/FILE ownership inferred.
- R56 outer unsigned count test and close-result overwrite with literal1 remain separate caller observations. A buffering-shaped return and an ignored close-return-shaped value jointly explain why actual persistence cannot yet be accepted. No actual resource-leak or historical bug claim is admitted.

OPEN: actual nested helper effects/return conventions, frame/register/alias preservation, deferred/native write and close/flush success, original payload/fields/tags/version/schema/checksum/migration/persistence, original server authority and cross-version equivalence. All Stage A system-family PARTIAL/OPEN gates unchanged.

Highest NEXT R58: qualify the shared write/close helper0x4a657 (write CALL0x48c38; close CALL0x48586) and close-path helper0x4a53e (CALL0x48596), focusing on return predicates, deferred/native output and close-result propagation needed by R57. Audit existing metadata first: mere rows in an overlapping address window are not a function inventory and no row at either target root was found in the R57 preflight. Retrieve authenticated originals only for missing bounded root/callee/entrygraph evidence. Keep other cleanup helpers0x4a5f1/0x4853d opaque unless their effects are required for a specific live value; avoid generic CRT/allocator ownership exhaustion. Separate conditional full-count/buffer-copy returns from actual native output, shared-helper result and close/flush success. Preserve frame/EDI/ESI/EBP/alias/callee barriers, no original payload evaluation or client execution. Actual persisted bytes, record/tag/version/checksum/migration/schema, original server authority and cross-version equivalence remain OPEN. Stage A restoration before joint new-game design; all system-family PARTIAL/OPEN gates unchanged.



## 2026-10-15 — Taiwan 1.0 savedata R59 static control-flow alternatives (research milestone)

FACT (authenticated original-static syntax, not actual historical runtime trace): After R58 full shared-write/close and close-helper inventories, the R59 independent graph check reconstructs both a structural path through the shared-helper native-context candidate CALL0x4a683 (target0x4c5b4) and a path to RET0x4a6b2 omitting that call. The close-path graph rooted at0x4a53e likewise has structural paths to RET0x4a5f0 omitting memory-indirect CALL0x4a5a3/0x4a5ad and paths that visit these sites. Source-free R59 branch Action38747322728 and main Action38747593076 SUCCESS. This separates full-count-shaped or close-shaped return syntax from any proof of native persistence.

OPEN: path predicate feasibility, call-return/alias/register/ABI premises, actual WriteFile/close/flush operation and return values, disk persistence, schema/version/checksum/migration and ownership or leaks. Structural control-flow is not historical runtime behavior and is not sufficient to promote these claims. Stage A remains PARTIAL/OPEN; no Stage B game design work inferred.

## 2026-10-15 — TW1.0 original WriteFile continuations (R63 authenticated static source)

**FACT (original static syntax only):** Original Taiwanese v1.0 client-derived Win32 `WriteFile` import-slot calls at RVA `0x4c68c` and `0x4c6f1` are followed by original decoded `TEST` instructions (two operands each) at `0x4c692` and `0x4c6f7`. Authenticated, non-executing R63 extraction found bounded windows of 32/28 instruction rows and 32/23 local CFG edges respectively, source-run 38754938642 and independently verified artifact 11983560690; independent main Action 38755871657 PASS. Evidence provenance recorded in SOURCE-REGISTRY as SRC-TW10-R63-WRITEFILE-POSTCALL.

**OPEN:** Neither the `TEST` mnemonic nor local edge syntax establishes the original incoming EAX values, Windows API success, actually transferred bytes, caller-visible count, stack/register preservation, branch feasibility, close/flush or persistent savedata. These remain Stage A restoration gaps, not new-game design decisions.


## 2026-10-15 — Taiwan 1.0 savedata R64 native-result TEST/JE and conditional byte-count output-position static evidence

**FACT (bounded authenticated original-static syntax only):** Both R63 original-derived post-WriteFile windows contain `TEST EAX,EAX` at RVAs 0x4c692 and 0x4c6f7, immediately followed by `JE` at 0x4c694 and 0x4c6f9. R64 independently cross-matches the five original physical PUSH spelling candidates at each call to R28. Under unproven Windows x86 stdcall stack/frame assumptions, pre-CALL ESP+12 would be the fourth argument/output-count-pointer candidate, sourced from PUSH EAX at 0x4c67e on the first call and PUSH ECX at 0x4c6e8 on the second. The first JE has only one successor inside the bounded R63 local window; no outside target is invented.

**Custody:** R63 immutable original-derived report 31,136 bytes/SHA256 91b650db700cf892a7d8c8b2d36a9d49dbeca139be315856d31d59533056c1bd and R64 derived result 7,013 bytes/SHA256 5253b2ebec4a9bfbdda24764ce8af5e0e67fabf9ba8daf7ad0ce22c7b172e43f are permanently preserved in separate provenance-bearing Git blobs. Original source Action38754938642, R64 Action38758669705, independent branch Action38759123587, main Actions38759247737/38759247758 and permanent-derived publication Action38759808251 all SUCCESS.

**OPEN:** Native BOOL return, actual byte-count pointer/contents, actual original caller frame/register preservation, Win32 dispatch, branch feasibility, close/flush, disk persistence, savedata record schema/version/migration/checksum and original server authority. This is Stage A recovery; no Stage B design conclusion.


## 2026-10-16 — TW1.0 R65/R66 original-static count/control evidence

FACT (bounded original-static metadata): R65 joins original JE0x4c694 target VA0x44c6d9 to RVA0x4c6d9 already preserved in the second R63 window; second JE target0x4c706 and three operand-derived cross-window rejoins agree with the retained instructions. TEST EAX,EAX supplies the sole retained local direct flag predecessor. Count-pointer candidate LEAs and postcall reads share EBP-12 spelling but do not establish temporal runtime address or memory identity. R66 traces conditional frame-local count accumulation/assignment and a signed comparison; the second rejoin bypasses nearby zero-EDI syntax. No actual count, OS result or save-field meaning follows.

R66's exact34-report census shows11 tail positions without same-object decoded mnemonic/operand metadata, while LEAVE0x4c75f and RET0x4c760 are already retained in R44. Permanent derived reports, source hashes and accepted branch/main Actions are recorded in STONEAGE-TW10-SAVEDATA-R65-R66-ACCEPTANCE-R1.json. OPEN: native execution, actual BOOL/count/address, preservation, realized paths, persistence, schema/checksum/migration and server authority. Stage A remains PARTIAL/OPEN; no Stage B design change.


## 2026-10-16 — TW1.0 R67/R68 native-tail and conditional return sources

FACT (original-static syntax only): R67 reauthenticates the original runtime and exact R63 report before recovering11 missing tail operand rows and requalifying existing LEAVE/RET. The21-row fixed-tail neighborhood preserves global writes of literals28/9, SUB EAX,[EBP-16], OR EAX,0xffffffff and POP/LEAVE/RET geometry; no OS error meaning or actual output is inferred. Source Action38824599576 and derived-only artifact12014357270 are independently hashed and permanently preserved with custody.

R68 forward and reverse metadata algorithms agree on two decoded full-EAX destination candidates and a third explicitly unknown early instruction0x4c5fe before RET0x4c760. A130-report same-object census retains the exact remaining gap. All candidate arithmetic/frame/native values and branch feasibility remain unknown; this does not close native I/O, persistence, original format/schema/checksum/migration or server authority. Stage A family statuses PARTIAL/OPEN, Stage B gated.


## 2026-10-16 — TW1.0 R69/R70 early-zero and three conditional return definitions

FACT (authenticated original-static syntax): R69 retains38 early-return neighborhood rows on the exact139-node/156-edge graph after reproducing R67/R63. The missing0x4c5fe instruction is XOR EAX,EAX, entered from early JNE fallthrough0x4c5fc and late byte26 JE0x4c72b. A133-report preflight bounds the prior absence claim. R70's independent forward/reverse algorithms agree on zero, SUB EAX,frame[-16], and OR EAX,0xffffffff direct return definitions;103 of139 nodes decoded. Conditional uint32 shapes agree across1011 invented-only arithmetic comparisons. Actual branches, inputs, count/ABI/frame/aliases, historical marker/error meanings and persistence are not established.

Source Action38851405164/job116813227130 and artifact12025561162 have independently verified ZIP/raw/canonical Git custody. R69 raw25466 bytes/SHA25626ff9f92d14a4ef385a279501e456b4bf58156209ad4471aef84109f6e16bfbe/blobd5d4924803dc28de8be00f712eecd11cf9003c66; R70 raw2406 bytes/SHA256c59858b8d35be04c8f37efec8c297d346fd57d6df2496973c75424143881d621/blobcd2782a57c7c131bd938ca5fe29406a486cc6823. Permanent reports/custody/acceptance receipt remain in research/recovered. No proprietary code/assets/save payload archived or executed. Full local124 tests pass; exact remote acceptance anchors are recorded separately in STONEAGE-TW10-SAVEDATA-R69-R70-ACCEPTANCE-R1.json.

OPEN: actual native returns/counts, temporal frame/memory identity, feasible paths, flush/close/persistence, original record schema/checksum/migration/server authority. Stage A families PARTIAL/OPEN; Stage B gated. Highest NEXT R71: retained-first adjustment update/count-to-return relation, especially R44 INC frame[-16]0x4c653 and known count accumulation; no redundant original acquisition before proven gap.


## 2026-10-16 — TW1.0 R71 adjustment predicate and R72 conditional count-unit relation

FACT (authenticated original-static syntax): a138-report retained-first census reuses R44/R45 evidence and identifies11 missing rows in a25-node adjustment-loop focus/29-node one-hop neighborhood. R71 exactly rederives R69/R67/R63 and preserves the139/156 graph. CMP CL,10/JNE qualifies the equality-only frame[-16] increment and extra literal13 store before the shared original-byte store. Input bound uses unsigned JAE; post-store output bound uses signed JL after comparison1024. Decoded graph coverage is128/139, with11 mode/direct-count operand nodes still absent in the registered representations.

Source Action38853018146/original job116818258696 and artifact12026131224 have independent ZIP/raw/permanent-report custody: ZIP3148 bytes/SHA256036e7aa7778d4f8fa778847671ae3dbec57807c26abfa12cecd25c9e7d03d89b; raw21525 bytes/SHA256746c7e64a973b52ca5cf3412342eb68725fcf15dcb5ad4a1e71a8e638ae90af5/blobf2a946ffc93c6a32210f2ebaa9dc9191833aac37. R71 independent branch38853444099 and R72 branch38853447606 SUCCESS; accepted code mainf8138e759c4665427f9680ab83d1acf567e19fd8 has successful R71/R72/R69/R70 Actions. R72 report5600 bytes/SHA256aa21627e0018f2a7d9c01aaa36b6f70f38456f938de31713fee893402070265a/blob94656b8f6c2f830743a6257c1a8abf7aedb00c22. Full local156 tests pass; separate remote suite counts remain41 and110.

R72 invented-only3124 trace-threshold comparisons plus four long cases qualify conditional complete-transfer output-minus-insertions identity. Post-store threshold can produce1025 output units. Partial-write examples disprove a general logical-prefix-count interpretation; no historical native behavior, overflow or memory safety conclusion is claimed. Actual count/BOOL, temporal frame/ABI/aliases, feasible paths, persisted records/schema/checksum/migration/server authority remain OPEN. No original code/assets/payload archived or executed. Stage A families PARTIAL/OPEN; Stage B gated.

Highest NEXT R73: refresh custody, reuse exact142-report/128-node next-gap census in STONEAGE-TW10-SAVEDATA-R73-PREFLIGHT.json, and narrowly resolve the remaining mode/direct-count predicate context. Permanent receipt: STONEAGE-TW10-SAVEDATA-R71-R72-ACCEPTANCE-R1.json; spec: docs/specs/STONEAGE-TW10-R71-R72-ADJUSTMENT-COUNTS.md.


## 2026-10-16 — TW1.0 R73/R74 complete bounded operand census and mode/call barriers

FACT (authenticated original-static syntax): refreshed144-report census retains the11 gaps; R73 recovers17 one-hop rows after exact R71/R69/R67/R63 reproduction. Seven-source R74 union now decodes139/139 bounded graph nodes/156 edges. This closes the operand inventory within that intraprocedural candidate, not callees/runtime. Mask32 skips/enters opaque direct helper0x4c761; later mask128 chooses direct-native-prefix versus the qualified byte-expansion prefix. Literal5 equality writes9 and EAX-shaped5 to globals, while inequality invokes opaque0x4c953 before all-ones return. Historical flag/error meanings remain unproven.

Source Action38885251848/job116921375490 and derived-only artifact12039068385 have independent ZIP/raw/permanent custody: ZIP2915 bytes/SHA2567005037bf04b1ff034b12996dd4fae4dd1c4d37750c7d0bfe808ed01a93b974e; raw14043 bytes/SHA2565cf096089f60f8a6afd80fe2923f214f609ac57a92ab3d9d02aeefb04248013d/blob2a90bf654a723da53f7d6a26008ca660cb89b290. R74 report7076 bytes/SHA256cc7b48b139f64a502eb26bc45fbd5754b1bba202484447b625e5f34a28c32c25/bloba29a6a9b38a86d2f33d9e327d73c9d08cc3fb5ad. Independent R73/R74 branch Actions38886167422/38886173283 and six relevant code main Actions SUCCESS atfb7cb654c1c702cb2400bcf224f60fdcff52e18a. Local192 savedata tests PASS; remote suites44/146 are separate.

Forward/reverse reaching-syntax algorithms agree on eight register queries. All six calls remain register/memory barriers; early mode snapshots and table/frame state are not equated across the optional call. Invented65536 snapshot pairs qualify four conditional predicate combinations, without actual values/path/ABI/count/persistence admission. No original program/API or payload executed or archived. Stage A families PARTIAL/OPEN; Stage B gated.

Highest NEXT R75: reuse R46's already retained0x4c761 entry/51-node55-edge helper graph/three decoded rows/native seek context and R37 boundary;48 helper rows lack registered operands, but only material missing effects should be acquired. R30 already records0x4c953 boundary; its decoded entry remains absent in the registered scope. Exact148-source helper preflight blob73d192eec12cd31e67b5b0fc298ab4c3bdb53189 and STONEAGE-TW10-SAVEDATA-R73-R74-ACCEPTANCE-R1.json preserve next-step evidence. Native BOOL/count/position, frame/alias/preservation, actual close/flush/persistence, original schema/checksum/migration/server authority remain OPEN. Legacy queued attempt37642417333 stays queued; separately accepted successor37643425686 and permanent report are requalified in docs/continuity/STONEAGE-STALE-QUEUED-RUN-AUDIT-20261016.json, without claiming the old attempt succeeded.


## 2026-10-16 — TW1.0 R75 helper effects and R76 conditional seek contracts

FACT (original-static): refreshed150-source census reuses R46/R37's retained helper entry,51/55 graph and three decoded operands;48 missing rows are recovered only to inventory all local caller-visible register/stack/memory/return effects. No descendant call graph or original savedata payload is opened. Runtime/R73 and exact R46/R37 helper surfaces are requalified. Source Action38888448211/job116931879732, artifact12040258731 ZIP2743 bytes/SHA2564cd9097e869802b8bd107f737ac68183c78f42f7a4b9b75a6a639adc3d6e069f; raw25435 bytes/SHA256bcec13f8eb8d0b6182a38aa8b0ba67a7f20ca1d9b33ca1c9a76a1448f62b7d85/blob757c22945d7e18263b154e88f52376d0ab58d42c. Independent download/canonical custody survives artifact expiry.

R76's seven structural paths have conditional EBX/ESI/EDI token restoration and balanced near-return stack under declared call-cleanup and nonaliasing premises; adverse cleanup/clobber controls preserve those limits. EBP, table pointers and intermediate EBX remain opaque across calls. Caller/helper physical argument tokens conditionally reconcile to an opaque handle,0,0,2 at imported SetFilePointer; modern Microsoft API/ABI references support an EOF-request interpretation, without original execution/position/success proof. Local AND253 clears bit2 while preserving masks32/128 on256 invented bytes; whole-table snapshot identity is unproven.

Permanent R76 report7662 bytes/SHA2562a57125d32c3889def89c90d2e99192d94a25bd30b9677d5bfd7b0fd10fa3ead/blob2cdbcb8b95649a0ce610ab93fde5edcd7ef0997b. Local226 savedata tests PASS; remote48/180 are separate. Independent R75/R76 branches38889189883/38889194294 and eight code main gates SUCCESS atcdbb41c9f9b2a25ab7aeb32fbf3eaa666c53f8e4. Receipt STONEAGE-TW10-SAVEDATA-R75-R76-ACCEPTANCE-R1.json and spec docs/specs/STONEAGE-TW10-R75-R76-SEEK-CONTRACTS.md preserve source/contract distinctions. No actual I/O/schema/server-authority admission; Stage A PARTIAL/OPEN, Stage B gated.

Highest NEXT R77: pinned154-report helper-entry census blob38cc620394f21e04ec96c14a883b0510082fca43 separates absent registered decoded entries0x4e8fb/0x4c953 from retained root/numeric references. Prioritize only0x4e8fb handle-source and material caller-visible effects, then0x4c953 where necessary. Preserve ABI/stack/nonaliasing, table/address, native handle/count/position, close/flush/persistence and original record/schema/checksum/migration boundaries.


## 2026-10-16 — TW1.0 R77 handle-source and R78 conditional table-return contracts

FACT (original-static syntax): refreshed156-report retained-first census at mainb49c0d81ad17dc8c5f691e505a9ca817df2a625d reuses R75's direct0x4c78e->0x4e8fb relation. No registered decoded entry exists at0x4e8fb or0x4c953; root objects and numeric references remain distinct. Independent iterative replay checks every source byte/Git blob and the complete historical Git-tree manifest, not merely a file list. Only0x4e8fb's material handle-source local graph is acquired:16nodes/16edges, no frontier/cap, no CALL. Runtime SHA256cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a and exact R75/inherited source chain are requalified. No original savedata payload is opened by this acquisition; no original program/API executes or proprietary bytes enter Git.

Source Action38891577123 atba49bb5ca0dc27d481dcca9ef0a46bb046586dd8 SUCCESS: synthetic116942077884(50 tests), original-static116942132806, independent archive116942430371. Artifact12041483206 ZIP1751 bytes/SHA2563e860fbfca18edb7b3016ec5fedc5c92b26fc341769ee88cd87a718341ade674 was independently downloaded/hashed locally. Sole9830-byte raw JSON SHA2564944a5037e02c5b88b9424b953bcf93254e67560a217663c73b11e42d2827f48 exactly equals permanent blob870b84cb7968d325b37463ca68de1540960e1f5e. Archive3c3b3226192ffe8deb7c55a92f94475da0c1bc16 retains derived report/custody only. Independent R77 branch38892137407/job116943923623 SUCCESS explicitly verifies live-artifact equality and66 tests; invented API-shaped live/expired/unavailable fixtures separately exercise custody-script branches. Bot archival itself is not independent acceptance.

FACT: helper MOV EAX,[ESP+4], unsigned CMP/JAE against global24254560, AND31 and signed SAR5 select table-pointer geometry rooted at displacement24254304. TEST byte[ECX+EAX*8+4],1 controls the table-dword return; intervening LEA preserves flags. The failure-shaped arm has AND global24252940,0; MOV global24252936,9; OR EAX,0xffffffff, followed by plain near RET. No historical CRT/helper/error names assigned. Local decoder writes are only EAX/ECX/flags and RET's ESP; no explicit EBP/EBX/ESI/EDI/EDX write or CALL. Two explicit memory stores occur on the failure-shaped arm. Valid memory/nonaliasing/external-write assumptions are not proven by those spellings.

R78 qualifies exact widths/base/index/scale/offset/literals/topology, and independently authored forward/reverse queries distinguish the two EAX return definitions.4104 invented-word arithmetic comparisons include signed/wrap boundaries;256 invented bytes qualify bit-value1. SAR is not SHR: high-bit inputs can produce negative bucket indices unless the unknown unsigned bound excludes them. Under normal dword near-call, valid nonaliasing stack and stable valid table-memory premises, caller PUSH EAX supplies helper[ESP+4] and its non-allones table-dword result reaches the R76-qualified SetFilePointer hFile suffix. This is conditional provenance of a handle-shaped token, not proof of an actual valid OS handle, realized API/path/position/success or matching temporal snapshots.

R78 report3854 bytes/SHA2568bdb54c09d3ad038cb9149b1ec6d6c7a240778182fa8c69e545e78823c081c14/blob0d2f061dac847871d05c3d38c4b494d583060117. Full local1935 savedata tests PASS after installing missing capstone/pefile; initial broad discovery's75 dependency-import errors are recorded as a resolved environment failure, not called a passing attempt. R78 branch38892142998/job116943943727 SUCCESS has212 tests; R77's66 and source50 are separate counts. Accepted codede9bb83b585f81e106ce3c45b6afaa8ba7ba1b34/tree058b599be98f54961e58680cc8f5542f4aea91fb followed fresh ahead3/behind0/14-path comparison and expected-head nonforced fast-forward. All ten relevant code main gates SUCCESS. Receipt STONEAGE-TW10-SAVEDATA-R77-R78-ACCEPTANCE-R1.json and spec docs/specs/STONEAGE-TW10-R77-R78-HANDLE-CONTRACTS.md preserve full custody and conditional limits.

Highest NEXT R79: exact160-report census at acceptedde9bb83b585f81e106ce3c45b6afaa8ba7ba1b34 preserves0x4c953's three root objects/29 numeric references and zero registered decoded entries. Preflight36634 bytes/SHA256ccb54ea43a16783e7185bc9150751cf369676d8431f51b4a5bd4be3fd085b2f6/blob725b4ebc9671ce3230c59b646e21a9167ccd606f is independently replayed against the complete source Git tree. First reuse retained boundary/caller evidence, then qualify only material error-helper effects on nonzero-error/literal-five-inequality allones routes. No generic helper exhaustion. Actual handle/count/seek results, realized paths, ABI/cleanup/nonaliasing/global-table stability, flush/close/disk persistence, original schema/version/checksum/migration/server authority remain OPEN. All Stage A families PARTIAL/OPEN; Stage B gated.


## 2026-10-16 — Research work-order correction, no historical promotion

The user's request for coherent overall restoration planning triggers the
nine-family source-qualified Roadmap R2. TW1.0 client-local savedata remains
a distinct, non-blocking historical gap; no server-save equivalence inferred.
Deep R79 helper expansion is paused with all prior evidence preserved.
Highest NEXT PET-STATE-01 qualifies capture-to-owned-pet runtime field sources.
The later WORLD-01 review reuses four existing hometown routes; no topology
reproof or new map/NPC/quest membership is asserted.
See docs/RESTORATION-ROADMAP-R2.md and the permanent portfolio index.
Stage A remains PARTIAL/OPEN; joint Stage B review remains required.


## 2026-10-16 — Captured-pet source/copy and modern lifecycle boundary

Existing convergent-descendant capture semantics justify copied known name
and reset hidden VARIABLEAI; both reference-runtime capture entrances now
validate them before installing a supplied pet. This is not new TW1.0 server
execution proof. Six invented-state scenarios include temporary-disk reload,
explicit reentry and controlled growth while retaining MP/skill/growth identity.
Wild-enemy EXP is not copied, and kill reward_exp is not pet EXP. Complete
state construction remains OPEN with explicit inputs. Source/carrier table:
docs/specs/STONEAGE-CAPTURE-STATE-SOURCES-R1.md. NextWORLD-01; R79 paused;
no Stage A family closure or Stage B promotion.


## 2026-10-16 — Consolidated restoration review, no new historical content claim

The Stage A review packet joins existing nine-family specifications, seven
source-qualified playflows and five evidence blockers. Explicitly includes
later skill/equipment/trade/storage/riding and original audio entry points
without transferring their version membership.54 source pins and8 complete
continuity prefixes are preserved. Selective replay checks modern/reference
behavior and retained source custody, not original commercial server execution.
No new early NPC/quest/map/master/save payload acquired; all family gates
remain PARTIAL/OPEN and Stage B GATED pending joint user review.
See docs/STAGE-A-CONSOLIDATED-REVIEW-R1.md.


## 2026-10-17 — Original JSS manual and catalog-dated published quest evidence

JSS official manual02 actual capture20010418083149 supplies bounded save-point,
bus, village-service/work and ground-item semantics. A separately preserved
Sina guide catalog explicitly dates its entry2001-01-18 and names36K ZIP
sqsd-rw3.zip, but current guide HTML is not authenticated as byte-identical
to a2001 capture. Four guide quest profiles remain publication-level evidence,
not recovered original server scripts or TW1.0/JSS1999 exact release facts.
A2003 two-direction delivery comparison preserves distinct operations.
Stage A remains PARTIAL/OPEN; no commercial runtime/persistence or Stage B claim.


## 2026-10-17 — 成人仪式任务段获得实际2001-11-20快照

FACT（限定文本存在）：新浪成人章节实际Wayback捕获20011120063019，14617字节，完整任务段移除空白411字符，与当前新浪/17173任务页同hash d2657655b96da2840fd19e9b663696a140bdb65d7f26653f36cad7e0938b828c。不得将1月下载目录当正文同月证明；也不等于最早快照已穷尽。2001段头盔敏-2与2003页敏-3为未解决来源差异，保留两profile。后期玉销毁/组队细节不倒填早期；原始道具ID、地区/版本、完成事件与服务器实际执行OPEN。详见成人仪式SOURCE-CONTRACT-R1规格及派生报告；网页全文不存Git。


## 2026-10-17 — 伐木任务的实际2003/2004文本与编辑版本归属

FACT（限定来源）：实际存档20031205132111保留新浪详细伐木正文，20040822040357保留汇编；各与当前完整任务段去空白相等。20040218115426索引将详细伐木链接列1.82/南岛，是编辑归属而非原始服务器版本认证。汇编尾刀/许可交回、2003重复路线及手环奖励整理为分源合同。练功文魅+5和详细页魅-5未决，攻35新斧与攻33修复斧为不同阶段。1月目录不认证本轮取得2001正文，原始ID/事件/运行仍OPEN。详见STONEAGE-LOGGING-SOURCE-CONTRACT-R1。
