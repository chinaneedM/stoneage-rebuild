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


## 2026-10-17 — 同源后代物品表的伐木候选身份

FACT（限定后代表）：固定hash的itemset.txt/itemset0710.txt各有同五行Big5整名候选，模板2465/2478/2481/2484/20197；两许可图像/标记相同但ID/名字字节/cost不同。手环魅raw双值-5/-5，不认证初代或解决早期+5差异。改造斧未在固定词表命中，不判不存在。原始商业服任务/奖励绑定仍OPEN。来源链见STONEAGE-QUEST-ITEM-CI-DERIVED-R1及ACCEPTANCE，原始表不入Git。


## 2026-10-17 — 后代伐木候选在ExChangeMan同一事件中的两类关联

FACT（严格限定recovered25后代保存包与确切EventEnd语法）：49次合格物品参数引用分属27匿名事件记录；其中2条同记录含2465条件+收回及2484发放，一条含2478条件+收回及2481发放。其余16条单ID多角色、8条单ID单角色。初代台湾1.0的NPC和奖励脚本、玩家是否能执行该条件、每个分支条件真值、任务阶段与持久交易仍OPEN。不能把后代2.5同记录存在当最早版历史事实；许可20197本次未命中不意味不存在。证据见STONEAGE-QUEST-NPC-FLOW-CI-DERIVED-R1.json，Action38997164871和ACCEPTANCE保管凭据；原始脚本不入Git。Stage A仍PARTIAL/OPEN、Stage B GATED。


## 2026-10-17 — Classic StoneAge外挂/辅助工具有年代的首次谱系收录（追加证据，不改旧节点）

FACT（仅限相应2001—2002年**文章当时存在**及作者所言，不保证最早发行日）：2001年6月已有SADE用户意见、8月同期玩家回忆CSS/SADE/SAC与加速及复制冲击、11月出现SaCh1.23使用叙述。2002年1月出现SADE H++/SACH/STA/齿轮对比、3月STA2.52当时功能评测与STA—SACHXP战斗、料理和脚本比较；8月一篇当事者回忆提出LiLiCoCo与SADE 0.1a—0.2h的变化，但自述回忆性质，不能作为未经交叉取证的原始发行年份。2003年6月同时期新浪确认SachXP++ help是电子攻略帮助文档，非自动战斗程序。来源S01—S09永久登记于SOURCE-REGISTRY与新机器包。

后世层（来源年月与历史客户端版本不能混同）：2016以后的石器圣手、2020起ASSA辅助面板、2023起SaSH及不具可靠首发年的STW/NG/StoneBoy/SaxTop等晚期记录只证明各自时代与相关实现/名称可见；无法从这些资料推出1999JSS最早工具完整谱系。相关来源S10—S14及具体否证在`docs/STONEAGE-LEGACY-ASSISTANT-TOOLS-CATALOG-R1.md`。

初版宠物图片/动画和成长区分仍生效：台湾1.0原资源125,996图像号/464动画组/39,065动画和242,085帧是资源规模而非宠物种数或全部宠物画面；后代2.5活动enemybase 988行/备表640行和多后代成长rank不确定全部1999/JSS或TW1.0宠物名单/系数。见`docs/STONEAGE-PET-QUEST-CONTENT-COVERAGE-RECHECK-R1.md`。Stage A已有用户授权的有界检查点继续保留，新需求开启材料字段的有名追踪，不宣称已完成原游戏。


## 2001-06-14（2026-10-17重新鉴别）— StoneAge玩家图像ID类别与原盘交叉证据

17173同期玩家《stonepic的图片编号》称宠物照片区7246—7366、人物照片7367—8566、操作界面9093—9288、人物动作9289—82726、宠物动作95883—125995，并提126766为大陆版登录画面。2026年按台湾1.0原ADRN位图0—125995全集逐号核对：前16段当年玩家标注的低号范围均存在，6段125996以上则不在原版TW1.0；**只认证同号成员，玩家给出的类别未取得原客户端渲染调用证据**。该文一方面补早期真实照片/动作的方向，一方面证明不能用后期126766假装首版登陆。来源SRC-SA-20010614-STONEPIC-CATEGORY-01。

## 2001-07-09（2026-10-17重新鉴别）— 游戏目录和玩家F12截图操作

17173《石器游戏目录的秘密》当时描述map缓存、音效音乐及F12截图路径，代表该大陆玩家在某现成客户端内看到的本地文件行为，不等于JSS1999原盘地图数据或原屏截图档案已被取得。

## 年代不明旧指南（2026-10-17重新鉴别）— 创建人物12外观及WGS流程

17173旧新手指南现存文字描述WGS/服务器、新人物、12角色候选与调色/方向控制，但无可靠文章发表日、无匹配TW1.0实际截图。台湾1.0原客户端CreateNewChar13字段含身体图号/脸图号，为另一独立来源；两层可交叉启发，不能默认同版按钮坐标/图号精确匹配。


## 2026-10-17 — 新取得官方建角说明与原始客户端输入来源

JSS manual01实际2001-04-18 08:23:14快照说明姓名全角8字符、能力20点、属性10点且至多两类，以及转向、换色、脸部、出生村及删除确认。该第一方说明不证明1999或TW1.0同版数值。TW1.0原盘sa_3.exe静态独立核到五登录消息调用及13建角字段装载，身体/头像运行时位置不同，实际图号、画面和原服成功未知。详见STONEAGE-TW10-LOGIN-AVATAR-R1，原有年代/版本界限保留。


## 2026-10-17 — 早期送贝壳见证与后代具名NPC关联

17173诗雨文章发表栏2001-12-10说明弥生/日美子与取得贝壳路径、村落位置参考，当前网页字节并未独立认证2001存档。后代固定保存包精确姓名与地图2000/1000、六EventEnd、活动物品2414贝壳/2415花有来源内静态连接，不据同名或不同坐标反推原始TW1.0版本，完整逻辑/交易/保存未证明。见STONEAGE-WORLD-NPC-QUEST-SOURCE-JOIN-R1，原始版权载荷未入Git。


### 2002-03-10 STA2.52版本功能见证重新分层（2026-10-17归档）

☆阿仇☆同期评测中的报告可用、作者请求、未验证条件、比较、对策及传闻分开保存；不当正式变更日志、发布日期或原版兼容认证。源码/旧软件未运行，新作采用未决。STONEAGE-LEGACY-STA252-FEATURES-R1。


## 2026-10-17归档 — 早期辅助工具版本主张的证据层

2001-11-11发表栏玩家文提到SaCh1.23，仅能见证名称版号，旁文复制争议不自动归于该程序版本。2002-03-21 STA/SACHXP比较无精确构建号：自动逃跑/饰品/详细资料/练功/脚本/料理与未来传闻分项，主观速度不变成实测指标，脚本优劣矛盾保持。2002-08-19 E_skyline回顾SADE部分更新：8列表条目另加0.2g变体，作者回忆不是开发者发布日志；版号不提供发布日期或完整继承链。2002-09-27配置文章见证阈值、复活、动作、断线保护和时间锁，个人阈值非默认，运气效果仅属经验归因。

来源仍是S03/S06/S07/S08当前迁移网页，正文SHA和响应SHA已由Action39033762316固定；不认证历史原字节。详见STONEAGE-EARLY-ASSISTANT-VERSIONS-R1及对应规格/保管回执。只保存派生记录，未执行旧工具，功能好坏不改变来源可信度，也不自动批准新作采用。


## 2026-10-17归档 — JSS 2001原官网链接的实际快照日期

JSS /stoneage/manual.html实际20010417160918有47条到manual01/02段落的链接；两正文实际20010418082314与20010418083149。/stoneage/和index.html实际分别20010425173204、20010406012216，均215字节同SHA的框架壳，引用menu.html和top.html；top实际20010414014135。它们认证有限静态导航，非同一时刻完整官网、视觉呈现或TW1.0原服数据库。menu实际20010414013651回应字节已固定，但未过本包正文品牌门，保留诊断，不据此判不存在。

17173根、index.shtml、guide/guide.htm、jiaoliu/jiaoliu.shtml的本次近2001/2002请求分别实际回放到2004/2006，不能将导航年代倒填。Availability未给closest不等于无快照；本次直接回放找到JSS页面。三源运行和全部有界结果保存在STONEAGE-HISTORICAL-SITE-NAVIGATION系列R1，原网页/图片未入Git。


## 2026-10-17 — 17173历史宠物玩家名称与迁移媒体页面分层

确认现存17173石器栏目中的五篇署名/日期栏2001文章入口，其中2001-06-14《抓一级宠物的心得》保留20条玩家宠物名称与出没地说法，另有送货、捕捉和成长经验、2001-09-11宠物推荐文献。两篇可读文章正文末仍指向旧路径 http://stoneage.17173.com/jingyan/jingyan.shtml 。这些是2026年对迁移网页的观察；早期2001站点快照、当年目录结构、原台湾1.0同版宠物物种身份/属性/抓捕点均未由此证明。20条记录以可审计的PLAYER_REPORT_ONLY候选归档，参见 docs/STONEAGE-EARLY-MEDIA-CONTENT-BRIDGE-R1.md 及对应JSON；不把个人经验算作原服算法事实。



## 2026-10-17 — 17173旧栏目归档请求的真实回放时间（限三次）
原2001日期栏文章现存旧链接 `http://stoneage.17173.com/jingyan/jingyan.shtml` 两个直接Wayback请求（近2001-06-14和2002-12-31）均实返**2006-01-15 04:47:22**；旧宠物目录`http://stoneage.17173.com/chongwu/pet.htm`近2001-12-31实返**2004-02-04 02:49:48**。三个Availability响应均HTTP503；但直接回放成功，证明空/错误查询不可解释为不存在。来源为Action39038286655实际返回及永久派生Git blob0d5ff5dcb8532626ff40891ff76e92cff378ec26（raw SHA256 e50cf9406ba4f057915adf84536dbb6d268d8bdd3303779a7da7b783cb9d6c57）。没有取得1999—2002**这三路径所求**的合格档案，不能据此宣告所有早期媒体站不存在；2001文章日期栏不等于2001原始DOM。无新原版宠物master/身份绑定/原任务执行事实。


## 2026-10-18归档 — JSS2001官方介绍与实际截图的日期分层

原官网top.html已验链接contents.html，本轮取得实际20010417155051快照，正文明确12类人物、含配色48外观、最多携带5宠及5人队；这是日本JSS2001官网说明，不认证1999首发或台湾1.0同构建。15个sakss原图出链中10张取得真实160×120 JPEG，实际快照落在20010618/19；图像与4月正文并非同刻。5条未取得的图链重定向至2021/2022晚期titan主页，不能当早期画面，也不能断言原图从未存在。两次实际抓取/错误与10图逐条观察保留于INTRO-SOURCE-ATTEMPTS和INTRO-VISUAL-CATALOG-R1。

既有JSS manual02实际20010418083149字节SHA仍相同，本轮新增的是12节宠物/战斗/合成结构化解读，不计新官方来源；捕获忠诚最多60、高于主人6级及以上不可捕获/拾取等只按文字年代与原锚点陈述，非原服务端执行证明。Stage A历史状态不因新JSS资料改变。


## 2026-10-18归档 — 原JSS社交活动预告与四村会场指引

官网event实际快照20010417155224，页内栏目自标2000-10-14/09-28/10-02；eventjss实际20010418090522记第二回搞笑比赛与第二回联谊，正文只标11月17日、12月22日，**没有明确活动年**，不可从索引或快照年份倒推。前者公告30000/20000/10000 stone奖项及未具名稀有宠、1—5人/组和5分钟；后者预计10人而非服务器容量，原集合提示22:45与表格21:45冲突、22:00开始，两值均保留。两报名超链接只在HTML注释内，未查询/提交表单；公告不证明实际举办或获奖。

eventmaz实际20010418085855有四村聊天室入口：マリナス东51南72、カルターナ东81南49、サムギル东111南38、ジャジャ东85南73，及领取票→找引导员→聊天室、北侧走廊右端大厅/右起第二婚礼场。是官方位置说明，不是原服floor/NPC ID或已执行路径。6配图为真实160×125编辑标注JPEG，实际快照20010630/0701，不与4月HTML伪装同刻。原世界DAT、NPC脚本、宠物物种映射均未取得新同版认证，原像素/网页未入Git。


## 2026-10-18归档 — JSS官方第一回搞笑比赛报道与第二回预告的分界

官方结果目录实际20010418085802（5041B）有16活动题目、14详情链接；第一回搞笑对应eventj09，不是误预取的第二回决斗07页。正确正文实际20010422015200（2153B），目录/正文标题/后续计划第二回三证相合，顶部模板却写“ねるとん”，原始不一致保留。主办方报道顺利结束，列30000stone＋未具名稀有宠、20000、10000与临时特别个人奖10000四项；获奖者栏是玩家/队伍文字，不认证宠物物种。原活动日期、年份、服务器及真实发奖事务未知；不能与第二回预告拼成同届结果。

三张sass0901/02/03只得到HTML引用及声明尺寸，首次回放全404，逐URL一次Availability查询全429，之后停止。无实际图像取得、不猜画面/宠物，亦不推全网或历史缺席。源原字节摘要、误取纠正、失败请求及拒绝跨届连接永久派生保存；原HTML、图片不入Git。


### 2001-04档案（页面内容具体修复日期未给）— JSS官方FAQ

2026-10-18实取faqmenu20010417155624和faqgame20010424225131，来自此前官方top真实链接；两页时间不同。目录41题目/3出链/无链接的已修正组9项，正文12问答。寄存宠物技能、名称窗差异、沙漠卡南指定宠物与ククロス捕获证书等是运营商缺陷标签，不是本项目执行过修复，也不提供物种ID/任务脚本。正文ヤン＝ミト进度异常当时仍在调查，不借目录修正组晋升成功。

官方说明强者表经决斗刷新，窗口模式256色因为随时间变色使用调色板。原公式、调色板时刻/像素与TW1.0同构建未知。敌/宠不显示的重装建议和入口玩家缓解报告只按历史支持说明保存。faqquest文件名不是任务攻略证据；两个其它正文与sa_se.lzh均未取。具体SHA/请求/边界见STONEAGE-JSS-FIRST-PARTY-PET-FAQ-R1与SOURCE-INTAKE，原HTML/资产不入Git。


### 1999—2000自标更新史（2001-04官网快照保存）— 宠物寄存/技能/邮件

2026-10-18实取verup20010417162544：40日期块，选择7宠物合同。2000-01-31初始村宠物店寄存，02-07竞技场寄存与技能问题修正；01-25DUEL旅は道連れ/换宠；1999-10-25地球一周修正与邮件返回前退出12小时保护/期间登录返回，10-26已返回邮件宠物5分钟变野宠，11-08增加物品合成/调理技能。无构建号，不独立见证部署，不推广上市/TW1.0同版。

泛称修复只连FAQ同功能/技能族，未认证同症状。三具名任务标签此页未见不推全网缺席。同1999-12-20两记录、1999/11/9金与公历火冲突均保留。具体原字节与边界见STONEAGE-JSS-PET-PATCH-HISTORY-R1，原HTML不入Git。


### 2005-06华义官方世界介绍（图像源另在2006-01）

2026-10-18新实取game/game01.asp实际20050614002509，原已验主页20050615023834真实href认证入口。官方回顾把尼斯1.0/2.0/2.5、伊甸3.0/4.0、文化5.0/7.0、海底6.0与冰壁后失落世界8.0关联；原文顺序5/7先于6保留，不作为严格发布顺序或虚构年表。机械文明消失原因和失落世界是遗迹还是新文明仍未解，精灵王无NPC ID；不能反填JSS1999/TW1.0同构建。

正文九切片实际取得8张GIF、逐张目视，图像快照2006-01-05。人物/生物/冰雪插画局部不认证具名宠物、地图或3D模型。第7片502后一次重试成功；第9片404缺失，不补成完整插画。请求/摘要/来源与R4复审永久派生保存，原HTML/像素不入Git。


### 2026-10-18 — 官方冰世界详情：12个原地图名与六场景

按远端main `12d45f491ece5aa53a66b8ce17a64ddab7978cd6`、tree`1af86bcfd66c850024e7fd8e462ecd26667e2ad5`重新启动，核338分支、0开放PR、同HEAD9项main SUCCESS及连续性/完整CURRENT等七文件。TW-WAYI-OFFICIAL-INTRO-DETAIL-01沿真实第一出链，只取game01_01.asp正文及其六张原场景图；实际主题为瑞爾亞斯（冰世界），不从编号预设宠物/任务。

正文实际快照20050614003328，26346B SHA256`f7e10861dd9f8ee3bef19c46863c7bc818d17635ffecab41b0189c63ff2b234c`。取得官方12个新地图原名、冰雪/作物生长困难/居民叙事和“第十大莊園”序位；未恢复地图ID、路线、坐标、NPC/任务/遇敌表。六原JPEG全部220×163并逐张目视，实际快照2006-01-05，与2005正文分开记录；图注分别指冰顫通道、议会厅、24小时便利店、庄园专卖店、训练所和武器店，不能提升为真实交易/全天服务/已知NPC/原生分辨率。

正文“瑞爾亞斯”与三图注“薩爾亞斯”原样保留为UNRESOLVED_VARIANT_OR_TYPO_OR_DISTINCT_NAME，不静默纠错、确认别名或合并实体；骑乘外观仅HYPOTHESIS，无宠物种类或规则。精确客户端构建/首发日期及冰世界等于整个失落世界仍未证，不回填JSS1999/TW1.0。按现有19集合归档合同新增19个研究条目（地区描述1、原地图名12、场景6），不是19张地图，不新增npcs/pets/quests实体。原HTML/JPEG/程序不入Git。

永久派生与规格：`research/recovered/STONEAGE-WAYI-OFFICIAL-ICE-REGION-R1.json`、`STONEAGE-WAYI-OFFICIAL-ICE-REGION-CONTENT-CATALOG-R1.json`、`STONEAGE-WAYI-OFFICIAL-ICE-REGION-SOURCE-INTAKE-R1.json`及`docs/specs/STONEAGE-WAYI-OFFICIAL-ICE-REGION-R1.md`。本地19项边界测试通过；新增独立一正文/六图、两JSON逐字节重放工作流，远端结果与ZIP/raw/Git blob保管链须随后实际验收，未提前宣称。

**最高NEXT `TW-WAYI-OFFICIAL-INTRO-DETAIL-02`**：沿既验介绍页第二条真实未读game01_02.asp，最多一正文，先核题名/内容，形成一份具名宠物/人物/故事/环境或玩法合同即止；若重复、空或有限取源失败，记录具体结果并回全官方22域队列，不自动递归第三/四页。Stage A仍7 PARTIAL+2 OPEN，Stage B/百科GATED，R79暂停，无整体百分比。

 
### 2005-06台湾华义官方系统介绍：宠物装备、导师、任务日志（不等于客户端实装）

官网game01_02.asp实际快照20050614005428/26414B，SHA256 0868e56a81d7037e434a09fd0824a6eb59747494099087f8d1eaeaaa37fb690c。官方文案描述宠物装具七类及脚部分型、乌力五槽和水装备例数、导师关系/5%声望字段及任务日志查看；本页同时含非玩法的商品包意见投票。正文不能推出正式上线日期、原始客户端/原服规则、物种/合成配方ID、具体任务或所有版本同构。详情与来源见STONEAGE-WAYI-OFFICIAL-SYSTEMS-R1，派生源重放Action39121796764 SUCCESS。


### 2005-06-08报道／2005-06-09转载／2005-06-14原运营商网页快照 — 8.0装备导师任务日志对照

巴哈姆特 GNN 2005-06-08 23:04:46 文章 `https://gnn.gamer.com.tw/detail.php?sn=20167`报道台湾8.0失落世界「今日上线」并列宠物装备、导师、任务日志、史卡魯与羅多克雷骑宠、合成11→15等；这是**报道日期和内容，不是可校验原客户端构建/服务器部署时间**。17173同新闻2005-06-09 10:30:41明确注明转载来源巴哈姆特，不能据两页推算两次独立公开发布。华义官网 game01_02 原快照2005-06-14属于独立运营商文案时间锚点，与媒体报道相邻，但网页存档日期不一定是正文首发日。

17173大陆《新石器时代》8.0专题页`newsa/new.shtml`和`about.shtml`当前可见任务日志、导师、宠物装备合成与「爱作画的少女」新增任务线索，但**原发日期不明**且地区运营文字为金山，不能将其排进台湾8.0确切推送时间或宣布一切版本统一配置。新闻与专题源原字节均未独立取得，作为分层文本见证并持续OPEN。资料回链见STONEAGE-80-SYSTEMS-CROSS-VERSION-EVIDENCE-R1，未建立虚构世界内年月或NPC服务器ID。


### 8.0未定原发布时间的大陆任务指南 vs 2012-04-10明确8.5报道 —《爱作画的少女》

17173“石器8.0版本任务全攻略”可认证的当前网页载荷，原发表时间**UNKNOWN**。目录实际href引到任务正文；有14编号步骤、2角色、5只具名宠物按交付换5颜料，结尾记五幅自画像和作画时不能骑宠。2012-04-10新闻内容（明确谈8.5）写此前须完成「无法逃离的审判」并叙述一幅画像。**不能**把当前存活8.0网页当2005同期实录，也不能推两个说法之间必然正式更新过任务或8.0无前置。城市名称简繁与瑞/薩异文、具体原服ID、年份、任务门槛和奖品实体都开放；本轮证据为第三方资料，源字节与版本差异见`STONEAGE-CN80-PORTRAIT-QUEST-R1`与独立source replay记录。


### 2005-07-19编辑标记的《無法逃離的審判》玩家文献（无画作任务前置证据）

巴哈姆特当前存活的精华区页面https://forum.gamer.com.tw/G2.php?bsn=1571&sn=2340 出示2005-07-19 02:36:12「編輯」，玩家指南记载审判任务自身的贝克/黄泉条件与三职业合作；此处日期为网页显示编辑时刻，**不是原服部署、任务首发或可证明全文至今未改**。这与2012年8.5报道声称其为画作任务前置属于不同事实；尚无同版本的官方事件脚本连线证据。来源暂为网页文本观察无原始SHA，归属OPEN。


## 2005-07-19 edited player guide — 《無法逃離的審判》 (2026-10-18 audit)
**Documented page field, not verified publisher timeline:** https://forum.gamer.com.tw/G2.php?bsn=1571&sn=2340 displays 2005-07-19 02:36:12 **EDITED**, author/editor credits and an explicit OURSA source attribution. It describes three-profession cooperation, a guard captain, a thief/research chase and learning books. This does not certify the initial posting date, 2005 deployment or a first-party server script. A current Mainland 8.0-labeled 17173 guide at https://news.17173.com/z/stoneage/renwu/sa80_06.shtml shares the core route and extends details, but its initial publication date and independence are unverified. Cross-quest portrait prerequisite and original IDs remain OPEN. Research bounds: `docs/specs/STONEAGE-CN80-JUDGMENT-NAMED-CONTENT-R1.md`.


## 2006-06-21 — Taiwan 8.5 named official-version story as contemporaneously reported (2026-10-18 audit)
**FACT, limited to reported promotional text:** GNN (https://gnn.gamer.com.tw/detail.php?sn=23856) published 2006-06-21 21:39:50 a contemporary account of the upcoming official Taiwan8.5《魔域大冒險》 and explicitly framed its story as a continuation of 7.5《精靈的召喚》. The reported characters are 雷爾 (subordinate of 艾巴登), 勇者, 族長們 and 魔軍; 伊甸大陸邊境 is a named story geography. The 2006-06-21 GameZone article (https://www.games.idv.tw/news.php?mode=view&nid=615) names «支援前線» as a new quest, alongside daily personal/family events. 17173 (https://news.17173.com/content/2006-06-22/20060622092748047.shtml) openly credits Bahamut and is a reprint, not an independent primary witness.

**EVIDENCE LIMIT:** This is a publisher-attributed period press promise, not a recovered 2006 official Wayi page or commercial game replay. June21–July5 beta and July5/July12 server rollout are published *plans*, not proof of completion. Story continuity to 8.5 does not supply 8.0 plot or NPC/item/quest code. Publication chronology differs from fictional event chronology. Bounded claims in `docs/specs/STONEAGE-TW85-PERIOD-PRESS-WORLDLINE-R1.md`.


## 2006-06-23 editor timestamp — TW8.5 «支援前線» period player guide (research 2026-10-18)

**SOURCE-METADATA FACT (not original-publication proof):** Current Bahamut curated guide <https://forum.gamer.com.tw/G2.php?bsn=1571&sn=3199> displays `2006-06-23 19:00:09 編輯` and a five-step named «支援前線» route. This is an *edited* label of a player guide, not a Wayi official rulebook or independently recovered original 2006 HTML. GameZone on 2006-06-21 already named the same new mission in operator-attributed press; that news does not confirm its script or actual commercial-server transactions.

**CONTENTS LIMITED TO GUIDE CLAIMS:** NPC 伊秋娜, 奏敷, 布克瑟; two six-piece supply types, 魔界之門 guard battles, 詭異洞窟 and 焦熱之地, 魔域前哨營地; parcel turn-in. Final reward unidentified. Undated later Wiki differs at three NPC coordinates and reports a level101/prior-quest condition not stated in this earlier page. No original NPC/map/item IDs or actual final rewards, no new early Taiwan1.0 content. See `docs/specs/STONEAGE-TW85-SUPPORT-FRONT-GUIDE-GATE-R1.md`.


## 2005-06-14 archived Taiwan operator description — marine fusion and social/crafting expansion

**FACT / attributed official description, not deployment:** actual archived Wayi game01_03.asp capture20050614005817 links earlier6.0 marine pets to planned8.0 fusion, names four classes despite a five-class/twenty-pet plan, describes79 ordinary cards plus one mission-role slot and separate retention/overwrite/manual exchange, and outlines five crafting functions. The unidentified fifth class, per-class distribution, original recipes/item IDs and real server transactions remainOPEN. Website capture does not establish first publication, service launch or exact client build. No universal cross-region chronology or early-v1 equivalence is inferred. Derived source: STONEAGE-WAYI-MARINE-SOCIAL-CRAFTING-R1.


## 2003-12-14 Japanese Hangame character-page capture, with separate2006 image capture

**FACT / operator website attribution:** original chara.asp capture20031214051427 explicitly describes characters without fixed names and player-chosen naming. The page contains twelve web positions with24 paired illustration/companion references. This is not a proven client roster, ID map, cross-version equivalence or first-publication date. Only the first illustration was acquired: its actual preserved response is20060619160353, not2003. One GIF avatar illustration is qualified separately; the other23 source references and all game model/animation bindings remainOPEN. Permanent metadata/spec: STONEAGE-JP2003-CHARACTER-VISUAL-SOURCE-R1.


## 2003-12 / 2004-02 Japanese operator pet catalog, with separate2006 image response

**FACT / source attribution:** Hangame's actual pet pagination captures provide45 entries at20031214055443,45 at20031214051259 and34 at20040220221717. The resulting124 named web positions are mixed-capture documentary entries; they do not authenticate a complete2003 live-species census or a specific client build. The operator claims more than100 pets, but published positions/local image suffixes are not server species IDs. One first-entry image was recovered only from20060604065927; its picture/name reference and temporal boundary remain separate. Raw names, including source96ンモモ, are not silently corrected or translated. Permanent evidence: STONEAGE-JP-OFFICIAL-PET-CATALOG-R1.


## Japanese operator pet-image captures2003/2006/2008/2016, reviewed2026-10-19

Twelve actual URLs already linked from the2003/2004 Hangame catalog were acquired as60×65 single-frame GIF illustrations and individually viewed. Five image captures are2003, four2006, two2008 and one2016; position100ノガロン has2004 page provenance but actual image capture20160622101624. Conversely three page3 references resolved to2003 images. These are archived response dates, not creation/deployment dates or evidence of2016 Japanese game operation. Together with the previously qualifiedウーリ image,13 of124 web references have observed pixels;111 remain unacquired. No original species ID, cross-region alias, stats, habitat, riding or client animation is established. Separate per-record dates and metadata: STONEAGE-JP-OFFICIAL-PET-VISUAL-SAMPLE-R1.


## 2003 Japanese operator village descriptions, separately captured2006 building image

The actual town.asp capture20031214052752 names four villages:サムギル村,マリナス村,ジャジャ村,カルターナ村. Source descriptions associate them withサイナス島/サイナス andジャルガ, west/east, beach, forest and small-island settings. Largest/best-ordered are operator descriptions, not measured area/population or a universal four-village census. The sole first illustration actually captured20060618193306 shows a gray stone building with an animal-head motif and surroundings; its function and client map identity remain unknown. Three other image references are unacquired. No cross-region aliases, original map IDs/coordinates/routes/NPC/encounter payload or first-publication date is established. Derived metadata and bounds:STONEAGE-JP-OFFICIAL-TOWN-SOURCE-R1.


## 2003-12-15 Japanese operator facility page capture: thirteen source-described services

Hangame town2.asp actual capture20031215095512 has13 named facilities/services. It explicitly forbids player pet purchases at the pet shop while allowing sales and pet technique teaching; describes HP recovery without specifying actor/full-heal/MP; village-exclusive stock; fee/level-gated quiz/battle events; item-contribution home setting and configured-start totem location; delivery wage/distance prose; paid normal-walking-speed automatic mammoth transport without appearing monsters; and a special-pet first lottery prize with money for other prizes. These are operator prose, not verified runtime transactions or proof of JSS1999/TW1.0/CN1.82 equivalence. Initial arrival at a chief house and configured-home game start remain distinct descriptions, with exact login/death/save phases unknown. The sole attempted first image URL returned404 twice; twelve other image references remain unattempted. No pixels, actual dimensions, building-function crosswalk, exact IDs/fees/prices/routes/probabilities or original execution are inferred. Permanent source metadata:STONEAGE-JP-OFFICIAL-VILLAGE-FACILITIES-R1.


## 2005-06-14 captured Wayi theatre and arcade descriptions, body explicitly labels8.0

The original game01_04.asp response at20050614011214 describes Eden theatre performance/art-value/item redemption and two separate named arcades with point redemption for items or pets. One arcade describes defeating an unnamed boss; the other describes ticket purchase and wagers with points according to stated odds. The actual odds, chance model, point rates, entity IDs and original server execution remainunknown. Theatre fairytales are promotional performance examples, not original world history or recovered scripts; the unnamed boss is not identified with earlier named antagonists. Site title《精靈的召喚》 and body8.0 remain separately attributed, not an authenticated client build or launch date. Identical point wording does not establish a shared wallet. Permanent metadata:STONEAGE-WAYI-THEATRE-ARCADES-R1.


## JSS manual captured2001-04-18: newly structured mail/item/social and shared-venue semantics

The exact already-authenticated manual02.html source was reacquired unchanged; this is no new webpage. Nine additional semantic sections describe conditional item target UI, inventory entry/pickup, ordinary versus pet-mail battle restrictions, returning/uncollected/mail-pet logout and separate unknown stray/grace timers, card-exchange consent reset without contact deletion, a dated local chat-file statement, and shared chat/duel venues. The duel arena lists level≤9 or exact duel ranks77/777 as free-entry cases, four match areas and locally free hospital recovery. Chatroom direct entry is described as free, with three rooms, hall and wedding venue. Special-ticket drop/exit/SP-restart warnings do not prove shared ticket ID, universal chat admission fee, restored tickets or generic immediate ground-item expiry. Prior generic fingerprints3070/7010/8030 remain acknowledged. Runtime, exact timer/fee/ID/save implementation and JSS1999/TW1.0/CN1.82 build equality remainopen. Source contract:STONEAGE-JSS2001-MAIL-ITEMS-SHARED-VENUES-R1.


## Cross-source boundary audit: JSS2001, Hangame2003 and Wayi2005 documentary scopes

Eight finite comparisons of five existing derived reports reference four original bodies; the two JSS2001 reports share one manual and are not independent witnesses. Mail grace/stray/ordinary item timers remain distinct unknowns; special-ticket immediate drop is contextual;2001 duel exemption cases are not transferred to2003 quiz eligibility; early local arena free recovery/chat entry and later unspecified fees do not prove a historical price change.2001 card-consent logout reset is distinct from2005 dedicated-role card retention/overwrite; duel rank is not theatre art-value or arcade balances; pet mail is not mammoth delivery payroll. No new historical source, original entity ID, update chronology, runtime or cross-version identity is established. Derived relation metadata:STONEAGE-EARLY-SOURCE-MAIL-VENUE-CROSSWALK-R1.


### 2026-10-19 — 已知JSS2001手册三节参数/成长/气绝语义

源限定FACT：3040/8020/8060三节说明19状态标签、四主参数UP分配、魅力/DP自动上升、EXP击倒对象概述、战后1复活及伤害相关可能回SP；角色魅力和宠物忠诚后果分开。四元素关系不增写优劣/倍率，未提损失不等于零损失。原文气绝章节体力/状态表耐久力用语保留，不能直接等同原服字段。旧已验20010418同一手册，全部三节早有通用指纹，新增行为语义而非新原件；原1999/台1/陆1.82同构建、数值/保存事务仍未知。规格/派生STONEAGE-JSS2001-PLAYER-STATUS-LEVELUP-KNOCKOUT-R1；原件不入Git。


### 2026-10-19 — 初建、升级、宠物忠诚与DP的有限文献关系

角色三节源合同同HEAD11候选/12主线门实际通过，独立原件与ZIP/raw/Git保管链永久记录。随后仅四份固定报告形成七组来源边界：初建20/10点不是升级奖励，主人魅力/宠物忠诚非同字段，气绝同手册重述不算双证，升级与魅力对忠诚影响不能相加推公式，排名77/777不是DP值，捕获差6/初捕忠诚≤60不是EXP限制/终生忠诚上限。两原正文同运营商，零新取源，规格/派生STONEAGE-JSS2001-PLAYER-PET-CREATION-BOUNDARIES-R1，非七实体或原服实现。


### 2026-10-19 — 日本2003官方世界/生活定位原件

沿已验真实game.asp入口取20031214053427正文，12869B SHA256c3cb0c64811dfd2d83e5ab809119ddcf09b5ce5b709d1e3c8de1e58c3ec91bfb。世界観分栏强调饲养恐龙宠物/狩猎/对战/送信、至少100种宣传及可选图鉴、石币与武器道具店/泛称学校、组队表情聊天及合作轻松氛围。无学校名字/课程/地图，无完整物种册或宏大剧情年表；不把100下界当124目录同构建、不把重交流当无战斗、不拼台湾后期世界史。四段5概念记录见STONEAGE-JP2003-WORLD-PREMISE-R1，原件不入Git，不自动新作设计采纳。


### 2026-10-19 — 日本2003官方外观/五人组队/遇敌界面说明

game2.asp实际20031214050618，17136B SHA2564e92ce95cfb836db9fd78f7b4f64905e60270202d1e2ea0b00cf56b79b6440b0。来源称12外观各4色且类型/颜色不改参数、四属性/可选眼口及名片脸、最多5玩家组队/队长带野外移动/自愿离队、道具合作及遇敌切战斗/行动图标/求助。不是48具名原角色、原服离队执行或遇敌算法；五同列原图仅引用/声明200×150，无像素/实际捕获。永久派生和规格STONEAGE-JP2003-GAME-FEATURES-R1，原件不入Git，不认证TW1.0或1.74a同构建。


### 2026-10-19 — 人物网页位置/外观维度/定制脸与初建的有限参照

五组离线衔接仅三固定报告：12×4外观与12网页位置不作逐序body/色板join；玩家自名非固定角色名字；名片定制脸非静态插画/未验com图；2006唯一图与2003正文分开，23引用未取得；2001初建20/10点/最多2类不填2003四类别说明。已有12record_id/JSON指针引用索引不新造实体，零新原件/资产。规格/派生STONEAGE-JP2003-CREATION-VISUAL-REFERENCE-JOIN-R1；原图与原服模型/字段仍未知。


### 2026-10-19 — 日本官方截图索引与唯一2008捕获界面参照

官方game3.asp实际20031215093733，八个无逐图图注的screeshot1–8引用；仅首GIF取得实际20080819022212，46583B SHA2560565913532b59e930958bbb04bb347a349e6667e02304426a6aa2197f48340b6，275×200单帧并精确目视。见野外斜向地形/海岸、左人物状态/右上地图窗，标签サムギルの村不等于mapID，人物/宠物/数值不猜。不是2003同刻像素、原生分辨率、登录/创建UI或原服执行；另7图无像素。规格/派生STONEAGE-JP-OFFICIAL-SCREENSHOT-REFERENCE-R1；原件不入Git，R10后轮换另一地区/版本材料。


### 2026-10-19 — 台湾官方2003日期新手骑宠计划：动机、适配与计划奖励

华义制作人栏目在2005存档索引将idno66标2003-12-10，正文实际2005-11-17捕获。酷哥说明骑宠入门门槛，计划送适合角色的较弱/忠诚较易升老虎以保护任务宠价值，并计划成人礼后领；另称快递老板任务连升30级。保留“打算”与运营方宣称，不当已实施数值奖励/+30终点30/图说甲子=+60，不补宠物/NPC IDs。定性颜色难易不是概率表；不能回填1999/TW1.0骑乘。永久报告/规格STONEAGE-WAYI2003-NEWBIE-RIDING-PLAN-R1；原件不入Git。R11初次周年页错题预取已纠正/图片Flash规则缺口与转蛋公告404保留，不隐去失败。


### 2026-10-19 — 新手骑宠续篇的工作/地理关系与计划实施边界

idno67索引标2003-12-23，原正文实20051113145307、19686B SHA256caf0ab5a51a87d0ddd6f3f6aea4be77cde4dbaed80b1c6e900f4946da703bea2。作者以成人礼后已骑宠为叙事起点，不明确证前篇赠虎实施。渔村礦石研究者→柯奧山奇怪礦石采集为一方工作线索，非具名NPC/地图ID/已知奖励；前篇快递+30不搬用。石器博物館真假酷哥/PK轶谈非账号认证/普遍PvP规则或世界正史。派生/规格STONEAGE-WAYI2003-RIDING-SUCCESSOR-ORE-WORK-R1；原文/图未入Git，三记录非完整原任务。


### 2026-10-19 — 台湾2003日期职业入门与高阶技能计划

官方制作人索引将idno64《全民就職計劃》标2003-11-14；正文实20041206141244捕获，不证明2003未改原稿或部署。酷哥主张让新手参与老手活动，计划将就职条件从一转成人礼改为八十级成人礼、降低就职任务难度，二级职业技能仍需一转以上。入职与技能学习两门槛分开，80级数字不脱离成人礼、二级不成人物2级/两技能；职业表/费用/树/脚本/实施仍未知。加美航班是文章框架，怀旧计划只是未来讨论；两图引用未取。派生/规格STONEAGE-WAYI2003-PROFESSION-ACCESS-PLAN-R1，五文献记录非五原实体/原服验证，原件不入Git。


### 2026-10-19 — 大陆华义2001捕获2.0官方可见等级经验表

已知北京华义upgrade.asp原件实20011204165711、标题石器时代2.0重取同SHA，非新网页/2.5软件升级。完整可见表有82等级—所需经验数值对，28行三列组（28+28+26）和两空对；派生保留原行/组位置及原数值，不拟合/纠错/外推，82不证等级上限。表体未明增量/累计、当前/目标级、角色/宠物或转生缩放，均UNKNOWN；不移给JSS1999/TW1.0/CN1.82/2.5，原服务端实现未证。一tutorials表非82原实体，规格/派生STONEAGE-WAEI-CN20-LEVEL-EXP-TABLE-R1；原件不入Git。


### 2026-10-19 — 大陆2001捕获2.0无署名新手指南的体验与建议

官方sw/adventure.asp实20011204212409、题石器时代2.0，叙述初生跟随宠、谨慎照料、可能战后肉/换石头、低等级免费治疗/买装备/组队远行，后附20点全耐力、魅-4/药救-1、较高等级捕宠忠诚低/升忠诚、lv20防40重练/$2000到魅100等建议或宣称。官方托管无署名不证运营商原创/原服真值，不把建议作强制规则、-4/-1叠加、100当增量或cap。沙母岛/吉鲁岛原拼写及「捕自己的血」疑似错字保留，原文读作回血仅HYPOTHESIS。十教程文献记录非10实体/任务，规格/派生STONEAGE-WAEI-CN20-NEWCOMER-GUIDE-R1；两图未取、原件不入Git。


### 2026-10-19 — 新手指南与JSS手册的初建/照料八组文献边界

只4固定派生/3原正文离线比较，宠物/角色manual02同一原件不作独立证人。20初建点与全耐力建议不作每级奖励/同字段；CN宠物升级与JSS主人升级忠诚例子保留不同主体，不证公式/补丁。魅力与忠诚分开，差6/初捕<=60仅JSS语境；CN-4/-1不补JSS数值或叠加，20级防40建议非回SP阈值，约3级非固定EXP表。规格/派生STONEAGE-EARLY-NEWCOMER-PET-CARE-BOUNDARIES-R1，8关系非8实体/原件，零原文/图片/程序新增。


### 2026-10-19 — 大陆2001官方新增宠物首目录40网页格

华义new_pet.asp实20011204194619、题石器时代2.0/新增宠物，首1-40网格34具名标签+6原问号占位，同格绑定40图引用，非40原服物种/客户端ID。阿米朵等名称/原大小写/非顺序文件数字保留，重复???不合并；40图未取，仅首4格声明83×90。分页41-80/81-104未读，104非完整原服名册或新加物种数；成长/技能/骑乘/跨版身份均未知。规格/派生STONEAGE-WAEI-CN20-NEW-PET-CATALOG-FIRST-PAGE-R1，原件不入Git。


### 2026-10-19 — 大陆阿米朵网页唯一原图参照

首目录位置7阿米朵真实7.JPG实20011205051046捕获，4831B SHA2567077cef8cfc23d67b34e3ed54ef6c57eca4c1197b44a2c513c4e43dfa1f85b30，JPEG83×90 RGB1帧并精确目视；与20011204正文分开，不回填原无尺寸声明。黄橄榄色头/红口内/浅色角颈与绿黄背景仅网页像素观察，非客户端精灵/动画/模型/宠物ID或跨地区名字认证。1视觉补充引用既有位置非新实体，另39首目录图未取、旧报告40未取历史不改。规格/派生STONEAGE-WAEI-CN20-AMIDUO-VISUAL-REFERENCE-R1，原件不入Git。


## 2026-10-19 — CN2.0新增宠物两分页实取，104网页位置有限闭合

本轮按实时远端main abcf7a09661bde146cc91e3e271e31bb79a63c7e / tree28c7676ad8a1cc1b3b845adedc1399c08dfaa324启动，373分支、0开放PR、同HEAD10项main实际success、无in_progress；无关旧queued37642417333保留。七连续性文件完整CURRENT及历史前缀、最新树/提交/Actions、22域portfolio和首目录/视觉/R14报告重新远端读取并与新origin/main逐字节核对，无AGENTS.md；不以旧聊天进度推当前。

按唯一最高CN20-NEW-PET-CATALOG-FINITE-PAGINATION-01只取两已有真实href正文，未取图像/程序/新出链。阅读器初不可用保留，直接HTTP初请求20011204194619后分别实跳new_pet1.asp的20011023173210（66451B SHA256dfc191c476dc5c968e1957e58070297d048475e3f3f8d8d5e897ccae56ea0c65）与new_pet2.asp的20011023181629（64382B SHA2562c7aea8d0319c2070d5c7590a95bfc892c2463deb76c5b95fca8c281549c76f0）。严格GB18030，页题石器时代2.0/文题新 增 宠 物/导航1-40、41-80、81-104。两新页十月、旧首目录十二月，分时来源拼合不作同日/同构建或捕获顺序=补丁顺序。

41-80实际8×5具名40格，从呼鲁鲁到欧林吉鲁；81-104实际5/5/5/5/4格具名24，从佩露夏到朱利洛斯。末行缺</tr>但4个td完整，解析按起始tr保存，不漏杨格斯/耶普鲁/尤里蛙/朱利洛斯，不补第105格。位置84裘里蛙配104.JPG、位置89砂鲨配87.JPG，原图引用/大小写/HTML声明尺寸按格保存，非文件号=网页序号/客户端ID。新grid SHA分别4f194a8b3bec04b36a37f629751841509bfaa26bbfb9fccee1b230941f01d182、a52bc5cf3b5b8660b29bbcfd5162463d69c986e546733026e55bbe8b97e72818。

永久STONEAGE-WAEI-CN20-NEW-PET-FINITE-CATALOG-R1.json/规格合计104网页位置=98具名+6原占位，本轮新增64具名位置；首40条逐对象保持原派生，重复???不合并/造名，旧目录/视觉报告不重写。阿米朵既有位置007一图仅引用固定Git补充，新图请求0、跨报告其余103图未取；这不是104物种/104新加宠物或原服完整名册。游戏ID/属性/成长/技能/捕获/骑乘/跨地区实体等同仍未知。原HTML/图片/程序不入Git、版权未批准新游戏复用。

工具/17反例及结构测试、独立仅两实际十月原页+固定父/视觉Git metadata、全报告cmp、derived-only工作流已加；35相关本地测试通过。第二次精确网络重取和候选/自身main源job、ZIP实下载/raw全字节/Git blob验收分别按实际记录，未发生不提前称绿。全部初始历史前缀/失败/22域原状态保留。

**唯一最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-15**：本有限三页目录CLOSED_QUALIFIED_THREE_PAGE_WEB_CATALOG_NOT_GAME_ROSTER，停止分页/图像扩取，返回全部官方版本/22域材料队列，选择具名NPC/任务/故事/环境实际正文缺口、真实来源和有限取源/停止条件；不空矩阵、数值公式循环/helper/R79。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79 PAUSED_NON_BLOCKING，无整体百分比。


## 2026-10-19 — 宠物三页实际保管验收，R15转公共设施一正文

三页内容e3008b0367da961999ada7634debccf9d4f1a1b4 / tree0a1177683927b12ed23e16adae624571ddda6f7e的10候选、自身11项main实际全部success；run39240145512/job118018715274独立仅两十月原页+固定父/视觉Git metadata，17反例/完整cmp。artifact12180084942实下载ZIP7302B SHA25695d7b27a15151ae22b0922d975ea9572bc510f88cb315d402cd89ca0492d6fbf，唯一derived.json173510B SHA2568bcda48e9e8e298efe446b02f0039146fa4a81e509ca4d08c4989e6448f59fdb等于永久Git blobf950aa33af0b3ec8693b2867758faf006aee546b。STONEAGE-WAEI-CN20-NEW-PET-FINITE-CATALOG-ACCEPTANCE-R1.json永久保留实际源job、ZIP/raw/Git及精确HEAD的10/11检查；此有限目录闭合不作原服物种/同日全名册。

按最高OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-15复用全部官方版本/22域来源队列，停止宠物分页及图像扩取，选择大陆村落环境/通用NPC服务/经济真实正文。已取new_pet1.asp实际侧栏「公共设施」href /ZHUANQU/stoneage2/sw/facility.asp；旧宠物派生未列此出链，不伪称旧JSON指针。阅读器不可用保留，直接HTTP初请20011023173210实跳20011204213609；73356B SHA256e18f0bced4935358e3be28e328d50a49a6dfbb8c26476a98c211892974e7ba16，严格GB18030，题石器时代2.0/文公共设施。入口十月、正文十二月分时来源，不推补丁顺序。

新增14设施类别tutorials研究记录：村长家、医院、武器店和防具店、道具店、宠物店、肉店、便利商店、竞技场、聊天室、道场、纪录点、长毛象快递、长毛象公车、加美航空；逐行标题/图片引用/HTML声明尺寸/服务段SHA及来源限定转述。服务内容含村长家教学与家族管理、医院医师/护士/药剂师/美容师、5宠携带与寄宠教学、萨尔吉姆/卡鲁它那加工材料和玛丽娜丝/加加料理材料、原票返村、礼堂、南北百人道场不同挑战、贡品/在线人数、快递押金和陆海交通。原文表示每村设施不一，不给每村强配全表。

护理/竞技场免费「10级以下」不推含10阈值；医师等泛称不当具名NPC；5宠/100关/100题不补完整master/题库/奖励；加工重复段不当独立证人；纪录点回顾不补版本日期；快递「早上（太阳出来前）」与天黑限制原样限定转述，不修成日出后/游戏时钟；十分之一押金只页面描述不实现公式。14图全未取，HTML声明尺寸非实际图片元数据；原服NPC个体ID/坐标/库存/收费/任务脚本与跨地区等同未知，原HTML/图像/程序不入Git。

交付STONEAGE-WAEI-CN20-PUBLIC-FACILITIES-R1.json/规格、R15实质复审、13反例测试及已知侧栏+唯一新正文/全cmp/derived-only工作流。设施13+分页17相关本地测试通过；精确第二次网络重取/独立源job及自身main/ZIP/raw/Git保管须按实际另验，不借父11绿。22域原状态与完整初始历史前缀保留，七资料profile不是全部发行清单。

**唯一最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-16**：本设施14行正文有限关闭，返回全官方发行/22域材料队列，优先具名NPC/任务/故事真实正文缺口，选一真实资格入口与有限取源/停止条件；不自动扩14图、服务数字比较、宠物页/数值公式/helper/R79。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79 PAUSED_NON_BLOCKING，无整体百分比。


## 2026-10-19 — 公共设施独立验收与本轮收束

公共设施内容82c1aa6d3a378732ba8bcdf38adcd4c5e69bf078 / tree0f30f74df96a74331b39f178827fcdebc5c593a7的10候选、自身11项main实际全success，无该HEAD失败/重跑。源run39240854129/job118021014559精确重读已知十月侧栏+唯一十二月设施正文，13反例/行段SHA/完整cmp通过；不冒称runner重演初次阅读器错误/跳转。artifact12181666070实下载ZIP4941B SHA25679a01ca15102b0aff681cae13261486dc056e12592c3ed8721db22e759d03436，唯一derived.json26065B SHA25649e48c23b2fc97f5ac64b03ce0b4f2848d04fe722005c5392e778941b33e887b等于永久Git blobfd5fc0e792a1d86b5509aaf663d6d68cf2750fcf。STONEAGE-WAEI-CN20-PUBLIC-FACILITIES-ACCEPTANCE-R1.json永久保留源job/ZIP/raw/Git及精确HEAD的10/11实际检查，CI过期不丢来源保管。

本轮实质：两新分页64具名位置使有限三页目录104位置=98具名+6原占位（非104原服物种/新加物种）；再一官方设施正文14类别和服务描述（非14具名NPC实例）。共3新正文、新图0，48相关本地测试通过；两内容HEAD分别自身11项main实全绿。118研究记录均核七必需字段/19集合合同；旧首40记录、22域原状态与完整初始CURRENT/历史/来源/路线前缀保留，无原HTML/像素/程序入Git，无历史删除。十月/十二月捕获、末行缺tr、图片文件号错位、10级以下含义及快递太阳出来前括注保持来源边界，不造跨地区等同/服务器脚本。

**唯一最高NEXT保持OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-16**：停止宠物三页/14设施扩取，复用全官方发行与22域源索引，优先具名NPC/任务/故事真实正文缺口，选一有真实资格的入口、有限取源与停止条件并实取；不空矩阵、同文数字比较/公式/helper/R79。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79 PAUSED_NON_BLOCKING，无整体百分比。此回执新HEAD必须观察自身Actions，不套用父内容11绿。


## 2026-10-19 — R16五岛世界文字及台湾已开/大陆未开的英雄岛具名攻略

按实时远端main f8f12ebc5e6465cde3e3bda1d04cb32693667913 / tree31bd8fd12a5269d24827e05fa7af64d06ac5afeb启动，375分支、0开放PR、同HEAD10项main实全success；无in_progress，旧无关queued37642417333保留。最新HEAD/tree/提交/Actions、七连续性文件完整CURRENT及历史前缀、22域portfolio/R15/设施派生重新远端读取，Git blob与新origin/main逐项相符；树4647项未截断、无AGENTS.md，不据旧聊天进度推当前。

按唯一最高OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-16停止宠物三页/设施扩取，选择具名任务、NPC及世界时间材料。先探测strategy/index.asp根路径不是实际设施侧栏href，此来历明确保存，不假造资格链；已知设施原文实际「英雄岛」直链/zhuanqu/stoneage2/strategy/hero/1.asp重新核实，旧经验页仅曾列链接不作已读正文。阅读器两次不可用不证历史缺源；直接HTTP初请20011204213609后，根页实20011201212305、69680B SHA2566b29b0115bcc37c4afbbe72e9061ea3ddc13d139a63753919e1a2260bd95e63c（ZHUANQU变zhuanqu），攻略实20011201035642、65205B SHA2561f5ce2dd27e58b9ad3f90b847559bfec1a10667c41c38e23b7c5475de89c198a；严格GB18030/题石器时代2.0。入口设施20011204213609/73356B/e18f0bced4935358e3be28e328d50a49a6dfbb8c26476a98c211892974e7ba16为已知源重取，非第三新正文。精确第二网络重取全报告cmp成功，未重演初次跳转/错误。

根页实际为五岛导航静态隐藏面板，不是具名任务目录：吉鲁岛石/山洞危险、波拉岛英雄萨姆吉尔出生地/龙群占领/借村中小黑猪回50年前、沙姆岛三岛中转海底隧道、塞伊那斯岛尼斯东侧/两村/雕像/海产、加鲁卡岛森林/木文明/加加与卡鲁它那多小岛渔村。五段文字DOM id/长度/原段SHA保留，grid37c1efbe215dcd03f3b1902cf49d60647cb771f733b9d9fa1056bac09a4a7186；50是相对世界年差，非2001减50/任务等级。保留萨姆吉尔村村/英雄萨姆吉尔村字面片段，未静默修正文名。Map_V2.gif仅一主图引用/HTML580×468及五HTML热区，像素/格式/真实尺寸全未取；area坐标非游戏坐标，五目标正文未读、未强配面板与南北岛身份，JavaScript未执行。

攻略原题前往英雄岛，明确「英雄岛在台湾已经开放,大陆目前还没有开放！！」；大陆官方站题2.0≠大陆实装、无署名攻略不证运营商原创/同版服务器执行，台湾精确构建和初发表日期未知。LV80以上/成人礼前置只源描述；日美子萨村村口56.124→送花给鱼村弥生55.93→获不可思议的贝→萨村村內70.40黑乌力对话进入「拨拉岛-英雄岛」。鱼村出生可直接找弥生取贝壳，来源分支[2,3]与其他村[1,2,3]分开，未豁免等级/成人礼。第三步未明写交贝/检查/消耗，不补物品事务。点号定位原样保存，不当原服spawn/地图ID；黑乌力不升宠物物种/模型。

波拉岛/拨拉岛、小黑猪/黑乌力、弥生/旧recovered25彌生、无名花/仙尼亞的花、当前不可思议的贝/未读4.asp不可思议的贝壳均不默认证同实体或同构建；「找寻找孙女」原导航错字保留，2/3/4.asp三正文及北岛交叉引用未取，不因红暴之谜导航推当前宠物奖品。交付STONEAGE-WAEI-CN20-ISLAND-HERO-CONTENT-R1.json/规格和R16复审，maps5描述+quests1攻略+npcs3提及共9研究记录，不是9原服实体；20新反例/与设施共33相关本地测试，独立已知设施+两新正文/全cmp/derived-only工作流。原HTML/图像/程序不入Git，22域/历史前缀保留，独立源job/ZIP/raw/Git及自身main需实际另验，不借父绿。

**唯一最高NEXT CN20-HERO-GUIDE-SOURCE-RELATIONS-01**：只本新报告与既验recovered25花贝配置派生作有限来源关系，核准方向、角色/地点和缺失前置/出生条件的界限；零新原件/图像/攻略/程序请求，不把相似人名/花贝结构当同版同任务，一份有实质关系规格后返回全官方版本队列。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79 PAUSED_NON_BLOCKING，无整体百分比。


## 2026-10-19 — 英雄岛与后代花贝配置六组有限来源关系

岛屿/攻略内容96ed8d94574dfcce50a4a339e8b2e89898cb3d27 / tree20942cea1ef1790d82220e44854f692fe9ec6d2b的10候选检查实全success；源run39242359029/job118025969676实际只已知设施+两原正文、20反例/段落pin/完整cmp。artifact12181014645实下载ZIP4656B SHA256b3edeb7c5e17fc503dedd6435c78c220d8bea44e91908bd4245a7c02ac2022a2，唯一derived.json17457B SHA2564fef4edbb48e837fb49cdcab7faf801040b5d2dfcab7c1ec03e4f8bfc786fe77等于永久Git blob8d95a7b2a64f0aea43b0c25beb8472d1fd114d94。该内容自身main需按实际另验，不能仅套候选10绿。

按当前最高CN20-HERO-GUIDE-SOURCE-RELATIONS-01只两固定Git派生：上述岛屿/攻略报告，及既验STONEAGE-WORLD-NPC-QUEST-CATALOG-R1.json（12778B SHA256ac402f48c7045f431d0e68a48c7c3513d283f19704f3cf6bd90c3d3a773e576e / Git blob5aa29da3b4b62b9f2bf8f2d7ed36c750c3bb8b74）。后者远端精确blob重新读取；后代原bundle/脚本未重新下载或执行，不把旧六事件/两item表当新恢复。零新原件/图像/攻略/程序请求。

六sources关系：大陆站台湾已开/大陆未开攻略与RECOVERED25 profile不当同发行/构建；日美子原56.124 vs后代borncorner57/124、弥生55.93 vs彌生55/92只定位字符串/配置不同，后代亦未证实际spawn，不推一格offset/交互半径/同人物；新攻略无名花→弥生→贝与后代彌生give2414/remove2415方向相似，但贝=不可思議的貝殼2414/花=仙尼亞的花2415和原版ID均不证；鱼村出生可直接取贝与后代give2414/item atoms空记录不合成出生谓词或无条件免费，complete condition仍null，等级/成人礼不被免除；黑乌力第三步超出旧两NPC样本不证整个后代bundle无此角色，也未明写贝消耗/检查；新攻略花→贝→入岛是一个用途链，后代/旧汇编另有反向贝→花，不撤销反向或判补丁/矛盾，也不作完整最终奖励表。所有2414/2415、1000/2000只后代侧，未回填网页。

交付STONEAGE-WAEI-HERO-GUIDE-SOURCE-RELATIONS-R1.json/规格，六条来源关系每条两精确派生pin及可实际解析JSON指针，非六新游戏实体；12反例与独立仅两Git/全cmp/derived-only工作流。45相关本地测试通过（原件20、关系12、设施13），九内容记录/六关系均核七必需字段与19集合合同。完整初始CURRENT/历史/来源/路线前缀及22域状态保留；源job/ZIP/raw/Git与自身main仍须按实际验收，不借父或原件绿灯。

**唯一最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-17**：本六关系有限闭合，返回全官方发行/22域真实材料队列，优先具名任务/故事正文缺口，选一可认证入口与有限交付/停止条件并实取；停止花贝身份/坐标/缺失布尔helper扩张，不盲取未读三攻略/Map2五目标。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79 PAUSED_NON_BLOCKING，无整体百分比。


### R16原件自身main实际验收补记

岛屿/攻略96ed8d94574dfcce50a4a339e8b2e89898cb3d27的自身11项main已实际全部success（含本源工作流与R58）；STONEAGE-WAEI-CN20-ISLAND-HERO-CONTENT-ACCEPTANCE-R1.json保留精确10候选/11main run/HEAD、两原源pin和实下载ZIP/raw/Git链。此为上条待验记录的实际后续，不删除历史待验措辞。关系包新HEAD仍须观察自身检查，不能借本原件11绿；唯一最高NEXT仍OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-17。


## 2026-10-19 — 六关系独立保管验收与本轮收束

关系内容343f69c44b44e8cbda058ee47bc74dd0752abaf3 / tree2a3887e08a1ed0823843687ecd2d344d2423a50a的10候选、自身11项main实际全success，无本HEAD失败/重跑。run39242859389/job118027608853实际只两固定Git报告/12测试/JSON指针解析与完整cmp，零新原件请求。artifact12182300803实下载ZIP3076B SHA256efc34e9209fe165a14e729b060192f688286461b25060dc4e60ea09cb19fb471，唯一derived.json13255B SHA2562fcbe614b13597b8fca7010f344f9db3011b84b20c86d67c54cf4e925274cf00等于永久Git blob0d04d0a697689bf0cfbb0f838aa1deb8eeef46f3。STONEAGE-WAEI-HERO-GUIDE-SOURCE-RELATIONS-ACCEPTANCE-R1.json永久保留实际源job/ZIP/raw/Git、两输入pin、精确HEAD的10/11检查；离线重放非再次取得原网页/客户端或原服执行。

本轮实质为五岛世界/地理文字、台湾开放限定的英雄岛三角色路线/鱼村出生分支，以及六组与后代花贝配置的有限来源关系。共两新正文、一个已知设施重取，新图/原程序0；45相关本地测试通过，两个内容HEAD各自11项main实全绿。九来源内容+六sources关系均核七必需字段/19集合；原件摘要、实际ZIP/raw/Git保管两份回执已永久归档。50年不变绝对年份/前置，波拉/拨拉、小黑猪/黑乌力、弥生/彌生、花贝ID和定位偏移不擅自合并；大陆站转载台湾已开说明不改写为大陆已实装。所有22域原状态、初始完整连续性/历史前缀及失败保留，原HTML/图像/程序不入Git。

**唯一最高NEXT保持OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-17**：停止本岛屿/英雄岛原文和花贝关系扩张，回全官方发行/22域源队列，优先具名任务/故事实正文缺口；选一真实资格入口、有限取源/停止条件并实取，不空矩阵、盲取三攻略/五地图目标、数字/坐标/布尔helper循环或R79。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79 PAUSED_NON_BLOCKING，无整体百分比。此回执新HEAD须观察自身Actions，不套用父内容11绿。


## 2026-10-19 — R17水城心之手环：一个玩家攻略的具名故事与任务关系

按main `01f0075e0118c59bd55f62bf41309130303a4d60` / tree `2312b02af20f57e87869eeb64e2ce35d6048cb44`及完整CURRENT远端原始blob复核，R16英雄岛与花贝关系有限闭合后，依最高`OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-17`返回全官方版本/22域资料队列。选择17173任务首页「石器3.0—伊甸新大陆」真实链接「水城爱情故事——心之手环」，实读`https://news.17173.com/z/stoneage/renwu/sa30_08.htm`一篇（页内署名微笑赢家 多多）；索引和正文读取得到的是**门户托管玩家攻略**，不是官方一方原始公告、原服务器脚本或历史原HTML字节验证，原始刊发日未知。

新资料结构化保留：五前置（成人、转生宠任务、100级以上、金飞航空、携不可思议的贝），四类材料等级（麟11/黏土4/线2/花10不是数量），从伊甸园经尼克斯至水城的玩家路线，四具名NPC喀尔斯/莉娜/麦特/卡蜜儿与11个交接步骤，玩家声称心之手环攻-37/防+37/敏+37/魅+8和与力之手环任务二选一。麦特失踪留信不是第五位NPC；100级边界、贝/花/项链实际消耗、真实NPC ID/坐标/脚本/物品ID及服务器互斥均未知，未读另一任务，无TW1.0回填。新原图片/原始客户端/原服运行0；未声称2026页面代表2002历史快照或二次独立来源。

交付`research/recovered/STONEAGE-CN30-WATERCITY-HEART-BRACELET-GUIDE-R1.json`、`docs/specs/STONEAGE-CN30-WATERCITY-HEART-BRACELET-SOURCE-R1.md`、R17材料评审与专门反例测试/Actions。一个索引真实出链+一正文，有限停机。测试/CI是**机读内容与负面边界验证**，不替代原网页原始字节或原游戏服务器。当前分支新CI/自身main应按实际运行再另记，不提前称绿。原CURRENT所有历史前缀与失败不删，22域原状态、Stage A七PARTIAL二OPEN、Stage B/百科 GATED、R79 PAUSED_NON_BLOCKING保持。

**唯一最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-18`**：返回官方各版本/地区优先一方任务或故事真实原文，选择不同命名内容的一条可认证入口/一实质规格或精确缺源即止；避免在心之手环数值、坐标、疑似同版身份上空转。无总体复原百分比。


### 2026-10-19 — R17有日期校勘补正：2003新浪水城双结局，防混线

前条R17只读17173一篇玩家攻略、明确其时代出处未证。在证据补核中新增一次限定的**2003-06-05 15:23新浪游戏专题《水城的爱情故事》**正文：https://games.sina.com.cn/zhqu/article/2003-06-05/11022.shtml?from=wap，编辑署名新浪游戏，非原服源码/运营方原始脚本。文章实际分A/B：A=喀尔斯挽回卡蜜儿、奖励力之手环；B=喀尔斯与莉娜情感结局、奖励心之手环（两者仅媒体描述，并非一版原服事实）。17173心之手环十一段与新浪B线**近似**，同构建/同任务脚本/来源独立性均未证，不把A/B并成一条线性正史。

八关系分辨：17173由莉娜制花贝项链，新浪A由喀尔斯、B由莉娜（分支而非统一NPC造物功能）；17173喀尔斯55.51/莉娜83.32，新浪54,51/82,33，未证一格偏移规律、真实spawn；17173「100级以上」条件vs新浪「建议115级」不可互换；两处心之手环数值符号类似但新浪属性后带问号，非物品master；新浪称二选一/若不再转生不能重复，原服reset未知。新增相对日期更强的第三方媒体资料，不把媒体转载=运营方直接披露。双方历史原HTML哈希尚无，只有本轮web-rendered段落及URL/行锚。新图/原字节/可执行脚本0。

补充`research/recovered/STONEAGE-CN30-WATERCITY-TWO-SOURCE-STORY-BRANCHES-R1.json`、`docs/specs/STONEAGE-CN30-WATERCITY-TWO-SOURCE-STORY-BRANCHES-R1.md`与八关系反例测试，独立工作流改为同时检查两机读档。历史上一条R17“仅一正文”不删，因为这是**后续有新材料引发的来源补正**；累计两资料正文，1无期17173 + 1明确日期新浪，不给独立执行双证人。验证待自身Actions实际结果，当前未自动宣称主线绿。止点限定两真实正文，不自动扩其它攻略/图片。

**最高NEXT仍`OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-18`**：回全官方版本一方优先的新具名故事、NPC或任务来源。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79 PAUSED_NON_BLOCKING，无百分比。


### 2026-10-19 — R17派生档案精确摘要/原始资料缺失边界收据

本R17研究内容主线`f8eeda0a473bb0c845d22ceb92cd5100e698a0c9`（tree `b2175beaf176a790b2b8a48802fb4aac699b1d2b`）自身11项main SUCCESS、对应候选分支10项SUCCESS；主线源验证run 39254789891/job118067239223离线`Ran 18 tests ... OK`。两永久Git派生JSON分别Git blob`8eddff3a5c493c1c5434417b6d4ef124b22fd2df`（8619 UTF-8字节、SHA256 `becc0ffa445c52183df16e8a5cb1e3ad7432b7b78539915053aabba2759415a6`）和Git blob`2833ca3e9a8c7ad37ac98f22c01c0fd41090e57c`（7205字节、SHA256 `4ef00084fa42e0a968d8ffb7ab9c4c3a8a5b07d5e0ef5d3ff1a646a0364d5cc8`），实际新校验独立cmp/哈希锚点测试；`STONEAGE-CN30-WATERCITY-SOURCE-BOUNDARY-ACCEPTANCE-R1.json`持久留存。**这是源读后的派生字节保管收据，不是历史原网页的取源哈希或原服务器事实验收**。两个外部原网页历史raw SHA、HTTP重放、ZIP/CI源artifact不存在，明确null；该工作流仅本地测试、无ZIP，不能伪造artifact链。后续须取有时代身份的原始网页快照或同构建官方原服证据方可升级原始来源状态。旧记录、过去当时未验注记均保留，由此后续记录补正。此回执新提交自身Actions须重新实际观察，不能借父11绿。最高NEXT仍`OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-18`，Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停，无百分比。


## 2026-10-19 — R18：2003泪之石任务六段故事，后世玄武版本异文分开

本轮从远端main`e648288e0ec8632bfc2564bf03c9f8e3ca03938e`/tree`d4e23d6c2b949fe4f2726cb39b22d0b4c91883c9`重新读完整CURRENT精确blob、README/协议/决策/历史/来源/路线/22域，远端该HEAD 11项main Actions均SUCCESS、无开放PR；最高任务`OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-18`。先查一方华义旧站档案，web.archive当前读取失败；TW8.5雷尔既在repo，不冒充新取；财务PDF不可直接下载，不引推源文。故选可检索全文六步且明确2003-05-21 22:59的新浪游戏《泪之石的任务》`https://games.sina.com.cn/zhqu/sta/sa6/rw/lzs.shtml`为**同期门户托管玩家“网友投稿”**。网页标“华义官方授权新浪石器”仅其专题授权，不升级任务为华义原始官方脚本；原页直开超时、搜索索引六步可见，没有原始HTML/SHA、确证区域/构建或服务器执行，`sta/sa6/rw`只是门户栏目标签。

来源限定新增故事：夕姬请玩家跨海寻找洛林，与杰夫战斗，六段任务含女戒→克林斯首饰→洛林的信→男戒/信→5泪之石，原文报告5颗合计5点基本能力；“鱼鳃草”只旅行提醒不实证强制消耗；夜晚时间不推时钟或具体脚本；16文字路径/5地点候选不认证原地图ID或传送执行；怪鱼“宫本蚊帐”只保留文字，不提升为原宠物ID。后出`https://www.shiqi.club/renwu/page/602.html`现可读、但几乎逐段抄录，不是独立早期实服证人。2025巴哈玩家`夕姬與洛林（玄武任務）`https://forum.gamer.com.tw/C.php?bsn=1571&snA=81769复用了人物/泪之石却增加奇怪瓶子/旧信/生锈钥匙/羽毛、宠物及不同能力生效阶段；仅四组候选异文关系，不从2025回填2003原服，也不强判同任务扩写、改版/支线。新原始程序、图片、原服脚本、证实游戏实体0。

新增`research/recovered/STONEAGE-CN60-TEARSTONE-STORY-SOURCE-R1.json`、`docs/specs/STONEAGE-CN60-TEARSTONE-STORY-SOURCE-R1.md`、R18材料评审、专门负面测试与Actions。一个同期网页索引六步+一非独立重刊+一后世异文索引，明确限度后停，不空转海底坐标helper，不继续R79。测试/CI的离线验证不会证明2003原网页字节或原版游戏执行；自身main/分支门及永久派生保管须后续按实际另记，不借旧绿。保留完整历史前缀、22域原状态、Stage A 7PARTIAL+2OPEN、Stage B/百科GATED，R79暂停，不计算总体百分比。

**唯一最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-19`**：返全官方版本/22域队列，优先有真实一方原运营商历史任务/故事/具名NPC来源或独立同期证据；一个具名实源与有效边界即止，不把重刊算重复新增。


## 2026-10-19 — R19五周年犬人萊福：同期报道+后期资料关系，不混原服实体

本轮起点为GitHub main `a72034baaa02db88969fc8628a4106c41daf4000` tree `8e51c5559b58c762698238354a22ea5ac9cdf197`、同HEAD主线后续按实际查看，协议/README/完整CURRENT/决策/历史/来源/路线/22域portfolio重读；唯一最高任务`OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-19`。停止R18泪之石故事重复，寻找运营归因具名剧情。选择同期2005-04-20 19:26:02 巴哈GNN记者小贤《石器時代》五周年活动，首次有具名犬人「萊福」、儿童「乎契」及其父亲营救、霍爾特村附近PC盗贼团基地、任务委托书与「相棲共生」宠物护主牺牲描述；同期活动报道仅作为**媒体转述运营商宣传**，并非华义第一方原HTML、原服运行或原客户端。报道中的蟲蟲危機包商品另保留，不并入任务奖励。

同一任务可能延伸至2006编辑的巴哈社区`犬人拿法...任務詳解`；后期指南写乎契、拓那哩、乎卓、多格樂以及塔姆塔姆/PC洞/霍村八步与道具加工，但仅保留作为来源候选。九组关系严禁把「萊福」=「多格樂」、乎契之父=乎卓、2005任務委託書=后来GM委托书，也不把后期坐标/材料/犬人一级或战斗血量、合成配方回填2005原服。新闻/指南两页浏览器实际HTTP403，搜索全文相关段落可见；原HTML SHA/图片/程序均未取，版号和2005日界仅媒体报道、不证真正部署或活动持续至2006。精确开放触发需华义当年活动原网页或同构建任务脚本/执行数据。

新增`STONEAGE-TW2005-LAIFU-EVENT-SOURCE-R1.json`、`docs/specs/STONEAGE-TW2005-LAIFU-EVENT-SOURCE-R1.md`、R19评审、9项独立负面合同测试/工作流。各数据作为SOURCE_REPORTED而非原始运营数值；历史前缀/已发现的不足均不覆盖。该候选提交的分支/main CI均须实际验收，不能借前一次成功。22域原系统家族7PARTIAL/2OPEN，Stage B/百科GATED，R79暂停，无总体百分比。

**唯一最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-20`**：停止犬人同文重刊，返回全部官方版本源队列，优先有真实原运营商历史内容/当期具名故事正文，一个限定内容资料包或精确缺源后停，不再扩无源NPC身份/公式。


### 2026-10-19 — R19 派生验收补记

R19 内容主线77b8b06a08ee93aea2e14887fc97de453aa6b19d已检验：候选10与主线11 Actions成功，run39261024329/job118088373092有9项测试成功。派生报告Git blob 3706c4a261ff4a62637e72376828167d0feae95d、UTF-8字节10447、SHA256 fb2b8e473049201e7b4a4e2b98266bc080c5e3edc1d778ef58e06a74fbb2a1b9。外部网页403，2005原始HTML与原服脚本未取，CI无原件ZIP。精确派生保管见STONEAGE-TW2005-LAIFU-DERIVED-CUSTODY-R1.json；新收据本身还需独立CI。最高NEXT R20，Stage A7 PARTIAL+2 OPEN，Stage B/百科GATED，R79暂停。


## 2026-10-19 — R20新浪2004六个早期任务梗概与一个详情链接边界

从远端main `93c76b9e0a33aeccb395b83ab027e4d3073e54a6`/tree`520ffa85204757c92b1f928cdd55d8b509b8a017`启动，前次R19犬人内容及收据已保管且自身main 11 Actions成功；本轮最高NEXT R20按全官方版本/22域转向更早的故事/NPC类内容。新实读2004-02-11 14:10新浪游戏《新任务，新挑战》80行页面：https://games.sina.com.cn/z/sta/2004-02-11/104374.shtml ，6个任务简介为三职业公会就职、九胞胎真相、森林熊患、尊尼/迪克友谊、阿喇吉酿酒和契雷多浪漫送礼，4人名/3职业明确来源限定。沿事实出链64只取2004-02-11 14:40《患难见真情》详情rw4.shtml：网页可见图像引用而无可提取逐步正文，图像0张实取、其余五子页未读。不把简介当原服务器NPC/任务ID、奖励或结局，疑似错字保留，新浪作者与华义公司页脚不推第一方原服脚本；旁侧6.0/7.0链接不证同构建。机读报告 `STONEAGE-CN2004-SIX-QUEST-STORY-VIGNETTES-R1.json`、中文规格、R20评审及源负面测试/CI按实际验收，本次源原始HTML字节/ZIP仍未取得，切勿提前说全绿。旧完整历史和22域状态保留。**唯一最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-21`**，继续不同原版本的有来源任务/世界故事，Stage A7 PARTIAL+2 OPEN，Stage B/百科GATED，R79暂停，无总完成百分比。


### 2026-10-19 — R20新浪2004六任务梗概派生数据永久保管

研究内容main `5ff985459a2022ce1267254d40f1b677324618be` / tree `773af9b10631fd1eaf920fc8adc2599b69542932` 已分别通过候选10项和main自身11项Actions；main专用run39264102119/job118099065594的8项离线测试成功。原派生报告 `STONEAGE-CN2004-SIX-QUEST-STORY-VIGNETTES-R1.json` Git blob `2273b04bc5ee7ea402aeac0169b616ed72ffa4e0`，共6765 UTF-8字节，SHA256 `edf10446a05f8c9d6d4ef597936e1593343486fa5c7ee73bd49bfb0c3f7c4d73`。保管收据 `STONEAGE-CN2004-SIX-QUEST-CUSTODY-R1.json` 将门户源网页与源出链详情原HTML哈希未知、图像0实取、原服务器脚本缺失和无原件ZIP明确保存；此派生报告SHA绝不能替代网页源SHA。新增独立Python哈希和反例3测试，回执新HEAD需再次验证分支/main而非套用父11绿。唯一最高NEXT保持R21，不扩6项未读图文攻略和补造任务奖励。Stage A7 PARTIAL+2 OPEN、Stage B/百科GATED、R79暂停、无全局百分比。


## 2026-10-20 考据补记：日本2008「影の支配者」分章发布

FACT（发布文层）：4Gamer现行页面保留2008-09-22、10-28、11-25的DigiPark发布文；公告分别称9月23日、10月28日、11月25日维护后开始前三章，资格依次≥10、≥25+第一章、≥45+第二章。第一章的两入口互斥及第二三章继承第一章部分选择影响均为公告描述，非实服状态机验收。第三章叙述数年前事件，不能按刊发日期换算虚构年份。原名/来源、当前HTTP与核心摘要及悬念边界见 `docs/specs/STONEAGE-JP2008-SHADOW-CHAPTERS-SOURCE-R1.md`。2008原始HTML、精确build、原服脚本/奖励/结局仍OPEN；不回填早期或跨区域正史。


## 2026-10-20 考据补记：2003大陆7.0朱雀运营归因稿

FACT（来源层）：新浪2003-12-16 14:38正文明确归因华义，标7.0石头就业所，写四神兽技能/神殿封印和朱雀—菲奇亚，附设定/状态两图。现行正文和图链已实取/目视，不等于认证2003原始快照或首发日期。联众2002-2-5的2.5稿另述两王合作抗机器文明、自封、玛蕾菲雅及转生，正文作者归因仍未知；不能据此与7.0两王一战合成唯一先后或判矛盾。单张一级状态截图不证明物种成长，图像亦不绑定原客户端SPR。详细源pin与未知见 `docs/specs/STONEAGE-CN70-SUZAKU-MYTH-VISUAL-SOURCE-R1.md`；无早期版本回填。


### 2003-12-23公告／2003-12-24–26活动 — R23圣诞兑奖员（2026-10-20取证）

FACT_SOURCE_REPORTED：新浪122310574正文明确归因华义，6.0/7.0服务器组四大村五大城具名NPC“圣诞兑奖员”，通过交谈交物取得一份神秘圣诞大礼包；30级以上并成人仪式，每人物同服组一套。20040218034443同期HTML实取且规则/归因/日期/图链一致。同一稿件两表示不是独立来源。OPEN：精确等级边界、地图名称、所需物品/礼包明细、脚本/时钟/重置、精确客户端build与实装执行。所有服务器降雪是另条宣传，不扩大兑换范围。原图当前字节已目视及hash，历史图像字节未证。完整派生链见CN2003-CHRISTMAS报告/后续收据，不回填1999/TW1.0。


### 2003-05-21攻略、2003-12-04存档 — R24海贼王遗迹

FACT_SOURCE_REPORTED：同期新浪指南五段叙述老渔民鱼鳃草、LV130鲨鱼入船、贝克委托杰克森制作人龙钥匙、三宠与石币/伏特加二选一报酬、返海底战鲨/贝克后交谈开箱。100级是推荐，标题“一转做一次”是来源主张，未得reset脚本。一次实际20031204053709 HTML与现核心一致，同稿存档非第二证人；专题授权不是正文一方作者。OPEN：地区/build、地图ID、随机收宠筛选、每种人龙数量、奖励/消耗/时钟/公式。12图片未取，不把海底故事与夕姬/洛林强合。见PIRATE-RELIC-GUIDE报告及规格；非TW1.0或原服执行。


### 2007-11-20日服赤影迷宫公告；2007媒体/2008官方HTML补证（2026-10-20）

FACT_SOURCE_REPORTED：DigiPark发布文与实际旧官方专页述未限定精灵王将赤影角兽分善恶魂封两壶、互相平衡；后来的喷发/地震使连接ジャルガ/サイナス/ギール三岛的海底洞窟出现裂缝与迷宫入口，狩猎团多数未归。O1实际20080220173517官方HTML、H1实际20071223094402媒体HTML，今/旧媒体核心相同，官方文字异文但材料字段相同；同运营传播链非独立实服双证。OPEN：魂壶现世存在/结局、宝物、精确地图/ID/脚本、世界永久变化及地震虚构日期。现媒体四格图实取目视，官方页说截图开发中；未取历史图片字节，不把商业随机券当任务奖励。无大陆两王/早期同人物回填，详情见JP2007-SEKIEI来源规格。


### 2008-07-07报道/7-8预告 — 日服親子の絆（2026-10-20取证）

FACT_SOURCE_REPORTED：媒体标发布文述冰窟幼犬リムフィ、保护者ミデル、寻子亲犬リムファン及完成寻亲任务获同名宠。原引文无公司署名；官方/媒体两个固定URL档案查询空返回，原运营HTML/历史字节未取。OPEN：真实部署/时区/build、亲犬性别、入口对话、跟随机制、影子身份、团聚结局、奖励个体/成长。现图122×99实取目视不认证原SPR或火属性。详见JP2008-RIMFY规格；不回填TW1.0，不与大陆犬人或其它寻亲剧情合成同一任务。


### 2001-12-04大陆官方2.0骑乘正文／2002-04-02分时图片（2026-10-20取证）

FACT_SOURCE_REPORTED：官方目录实链qdragon.asp述四庄园族长家宠物骑师、人物适骑查询、携宠缴费、三课程/等级/忠诚100与骑乘菜单；训练对象是人，更换宠的资格描述不证明宠物技能栏。骑乘近程/远程攻敏来源不同，生命力相加/损血等比例/防御与受击敏在人宠间；精确权重/取整/HP语义仍OPEN。正文实际20011204195948、图片实际20020402014049裸域捕获，两者分时非同构建；图为虎状骑乘场景非NPC对话或物种ID。无功能首次上线/原服执行或TW1.0回填，见CN20-RIDING规格。


### 2026-10-20 R28：2002-12-01已见的4.0标记骑宠与庄园表

新浪现页与20021201125523快照核心一致，捕获日期不是发布日。九庄园/骑宠/服务表首两封闭商店空白、两昵称坏B1字节保留；制作人族长与长老、流浪骑宠师及五转人物条件形成13条记录。门户作者/部署仍未核实，不回填早期2.0。详审查R28及中文规格；NEXT29。


### 2026-10-20 R29：2001官方2.0加工与料理材料

官方三正文实际捕获20011205052725/20011205052908/20011204201517，来源区分加工操作、技能价格、料理五类别、寄放风险、经验推荐与明确附魔传闻，形成14研究记录。两链接GIF实际20020102，不能当同版制作执行。未核首次上线或原服；不回填早期版本。详R29审查与中文规格，NEXT30。


### R29身份限定补记

2001年12月捕获仅是页面存在上界，不是首次推出日；官方域名托管与具名作者/运营商撰文分开，三正文作者仍未知。2002图像与2001文献不视为同构建。初内容候选10、补强候选1/main11为分别实际验收，不合并成一个HEAD的检查数；双ZIP派生永久保管见CUSTODY，原服尚未验证。


### 2026-10-20 R30：2001大陆创建与升级说明

沿“人物创造”真实导航取到20011201045054“人物创建”正文。文献说升级分配3点、四局部能力增量、姓名全角8字、最多两相邻元素、南北各2出生地与原始宠差异；创建总池未写，作者未知，不从日文20/10或玩家建议互填。图实际20011221174011户外场景，不证创建UI或初始宠。12研究条目非12人物类型，原服未执行，详R30规格与审查。NEXT31。


### 2026-10-20 R31：日服2008-11-11进化首批与官方晚捕获

DigiPark媒体发布文标11月11日维护后，官方专题20090217151837快照另写16:00。首批四剑虎进化前标签与四遮盖结果名、進化Gさん试炼/可重复/失败Lv1，官方页另有状态名字初始化/一次一宠。促销11月18结束不等进化撤销，秘宝保障及状态重抽与普通随机独立；2009捕获不证明2008当日部署、原服或完整后续名单。详R31来源规格，NEXT32。


## 2026-10-20 R32日服协力活动、交纳总量与奖励开放期

本轮新读远端main553a7b6501218bb510ceea0e0f060e6afe3fc3fa/tree d42f2db50d5c10b491aa021472a01185c3b27589，406分支/0PR，自身9main/8候选success；八连续性/路线/22域全文固定字节/SHA/blob，旧queued37642417333保留。最高NEXT32回全官方22域，选择日服2008初夏协力内容。一篇4Gamer2008/06/20 22:28媒体明确引文发布资料的协力段，当前280409B/SHA256 70e63e25844c698ef069a0a10b39462d26992ad054ce46755de7a9bf8dcbd056，核心SHA256 3a3d781a9f3151dea50e4c0690b04fa35be11b35b754ffed818dd2122a1d772f；一次真实官方出链availability返回429，不宣称档案全面缺失。

17研究合同/中文规格补出敌恐龙掉精霊の雫—恵みの精霊交换精霊の恵み—给予神秘の大樹，以及族长/泉水、大工/便利店、転送員/聊天房三地方援助。四具名角色为来源叙事关系，不认证实际交物NPC/坐标/外观；マンモスルーム与マンモスホール两标签不强合。五JPEG含一树场景及四奖励表全取/目视；五树门槛2000/5000/8000/30000/35000与三地方3000/3000/10000分别记交纳物，不当个人费用或求和；跨服/单服计数范围未知。收集6/24 16:00–7/15 13:00与奖励7/22起常设或7/22–8/12分开；存档点/寄存NPC/技能追加销售/经验活动/宠物重抽及圣水/商店/转送奖励均未证实际开放。

12本包及相关63测试、六实输入重放与8实际正文改写拒绝通过；人工表格转录不称机器OCR，放大复核キヌイ和再抽選。当前HTML/JPEG非2008捕获；008树图不证地图/SPR，另三场景未取。原HTML/图不进Git，无原服执行/原ID/交换比例/概率/商店表/奖励效果，三倍大工叙事不补玩家倍率，存档点不重开R79。独立CI/ZIP保管按后续实际验收。

最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-33回全官方版本22域另一具名材料；止点为本活动来源规格，不扩活动结果、虎追七章或全图递归。同版原脚本/运营结果/计数表/具名菜单或运行才重开未知。Stage A7 PARTIAL+2 OPEN，B/wiki GATED，R79 PAUSED_NON_BLOCKING，原22域及全部旧历史前缀保持。


## 2026-10-20 R32实际双CI、脚本字节差异定位与永久保管

内容82551e491625911130289936da5dac966a039738/tree926c929e2fc1c700a5eba9a08a08129bedd6f9f8自身候选10/main11全success；source run39408860268/39408954668，job118581376480/118581687625各12测试与一HTML五JPEG实重放。artifact12257659302/12258114013已实下载，ZIP均2107B，SHA256 04631b56259dc04f09dfb40fceeaaab7ec24edf65682eb595346ae057adb344e/97a6d9997ce3d45ba420040f4aa6ce16fbfa40ab6724f789acae7b1c0e1a4308；唯一replay.json均6524B/SHA256 61c34db5a406c8a66913787d4f0c8b070e4a234d4e7905a507bcfd09eee14187，两CI逐字节一致但不等于首次本地JSON。差别仅M1输入字节元数据：CI280349B/SHA256 cb18dd7867ea296cf5e0c94164d14493455cbc35952261b72e06afb921580461；核心/其余全字段和五图一致。补取实际当前页恰与两CI全SHA相同，对比原HTML47个script元素，仅零基26变，去script后完整HTML逐字节一致，因此本轮可定位全部变化在脚本内，不泛称任何未来改动安全。两CI原始JSON分别永久保留。

永久CI-CANDIDATE/CI-MAIN-REPLAY/CUSTODY固定源报告/8真实改写反例及外层meta正例/派生JSON字节、SHA、Git blob，精确HEAD/run/job/artifact/ZIP/raw链及八启动全文前缀。独立远端干净检出63相关测试、另一HTML解析器、五全JPEG解码和八完整前缀通过；追加保管用例后64相关测试另实验。人工奖励表不称独立OCR，条件承诺不称实际奖励，原HTML/JPEG不进Git。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-33返回全官方22域另一材料，停止本活动helper；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停保持。保管提交自身Actions另按实际验收，不套父绿灯。


## 2026-10-20 R33台湾7.5精灵召唤预告、玩家分工与具名图内物品

本轮新读远端mainaf5d63d70cbf62277546818a244ecdbeefb2f87f/tree54bcf0b4fcc846880edbb3cb06772d26560a1c0c，409分支/0PR，八连续性/路线/22域全文固定字节/SHA/blob，旧queued37642417333保留。该文档HEAD自身未触发Actions，不套父45b5aaf的10候选/11main/13源测试。最高NEXT33回22域；两GNN台湾2004线索各403后，重取已认证华义制作人目录P0实际20050612011406/28883B/SHA19661e2acca046bf8c6dc86dc968107fe9935cd58a8f3cd8ce5e1de5aeba7f8b，沿同一表行日期2004-5-28/标题7.5版報導之一：精靈的召喚的真实web键84出链，正文实际跳20051129125915/20368B/SHAb073ac516fd358805e961efb9b5f2746552f1d1e8f11c4a8ffa43ce3b67381ef。两页严格Big5；web键不是任务ID，开发近尾声预告不认证部署。新浪大陆2004浏览线索未并入本来源合同。

十研究合同/中文规格补出未明条件召唤玩家—使者寻找勇者—交付精靈信物—勇者得知使命—完成后两角色获奖，及新老玩家重建信任/共抗魔族的明示目的。两角色不是具名NPC，未补等级/配点/六转/组队资格、奖励数量或相同奖项；精灵不等于精灵王，魔族不强合别区世界线。三真实原JPG实际捕获20041211081705/20041211082942/20041211084443，48080/58587/89797B，均640×480，全取目视并放大I3。目录标注日、2005文和2004图分开，不认证2004-5-28首日像素或同构建。

I1提供确定/取消召唤通知，未取声效或原协议绑定；I2任务目标古瓜、剩余6小时33分，不认证NPC主表/坐标/初始或统一时限；I3局部剩余0小时59分/完成领奖提示，交出精靈勇者信物并收下柳牙之槍；所选同名面板耐久100%、攻+85敏-18、毒霧的精靈Lv6，余额8198620不当奖励。泛称信物与图内标签未证规范别名，图内武器不当全任务固定奖，Lv6不当任务等级，三图不同外观不当同人连续任务或两时钟相减。原ID/消耗/公式/原服执行均未知。

12本包及51相关测试、五实输入离线重放与8真实正文语义改写拒绝通过；独立远端/CI/双ZIP保管按后续实际验收。原HTML/JPEG/放大图不进Git，人工转录不称独立OCR。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-34回全官方版本22域另一具名材料；本预告止点已达，不自动扩六转/庄园续篇/全任务池或helper。只有同版资格表/脚本/菜单或轨迹才重开未知。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING，原22域及全部历史前缀保持。


## 2026-10-20 R33实际双CI与原图/派生永久保管

内容2cde1987abce8a77dda80bc9e8cc7c3fbecf73f0/treeec9d487b9b690ffd5fbc919b16eb6131ef9a2641自身候选10/main11全success后非强制快进；source run39411352610/39411464180，job118589614407/118589982458各实际12测试+两HTML三JPEG实重放。artifact12259765024/12258609744已实际下载，ZIP均1993B/SHA256 eadf9527613f97ccf23865236da139a1545d1c1439c32da0e85f5bf6cfd27f25/45eb606c582f16fd12cdb6b87b56911c96f6994be44ec497c1e0ef599441d45d；唯一replay.json均4126B/SHA256 846cb6dbd57a0ad175f39188edf59667bb8c4510f8ae2b118c7d2541dd6134e5，两支原始JSON逐字节一致且等于本地五实输入派生。两份CI原JSON和CUSTODY永久固定源报告/八真实语义反例/派生的字节、SHA、Git blob及精确HEAD/run/job/artifact/ZIP/raw链；五实输入全字节固定，原HTML/图不进Git。

独立远端干净检出51相关测试、另一HTMLParser重提四段hash、三JPEG完整解码、八完整历史前缀与本地完整JSON逐字节一致通过；追加保管用例后52相关测试另实测通过。CI路径补入实际传递依赖shadow_release，源语义未变；保管提交自身Actions随后实际验收，不套父绿灯。角色/资格/泛称与图内信物、倒计时/初始时限、局部面板/全奖励表、余额/奖金额、2004图/2005文及预告/部署保持分开，未认证原服或原ID。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-34回全官方22域另一具名材料，停止本页/续文helper。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部旧历史保持。


## 2026-10-20 R34大陆2.0八战斗指令、逃离队伍与三类失败描述

本轮新读远端mainb83ab9c19380b81e97874b437c290b8068ec7c2a/treec1605fcbb0265e716e3c9934dbefc824ccc69f4f，412分支/0PR，自身8main/7候选success；八连续性/路线/22域全文固定字节/SHA/blob，旧queued37642417333保留。最高NEXT34回全版本22域，轮换到早期战斗交互。已验N1导航临时原字节按当前仓库69317B/SHA561950fd7bba41e7d39f4a781a671e11e175c7fe08dd1b5481fdf1fd23ba351b复用，不算新发现；沿真实“战斗系统”href请求20011204194619，正文实际跳20011201043456/65573B/SHA944d26d035afc11a6f1af4fd135491a7ef516c20970085b68c84e1c4f7069d83，核心SHA83663010b556ecc64829637e738648e49f48a37f51383505c7facab5e2539dc9。严格GB18030，正文无具名署名，官方托管不认证作者、精确构建或部署。

14合同/中文规格补出上排攻击/咒术/捕获/请求帮助与下排防御/道具/宠物/脱离的相对位置、输入等待—决定或超时—处理—未完再等待、装备附魔、捕获可能失败/转生前5之后增加未定、HELP和队员实际退出即离队/领袖退出即解散。轮流输入不当敏捷执行顺序，未补秒数/像素框/协议枚举/成功率/额外容量/队长转让。待机宠接受指令与某些高忠诚宠挡致命击保留原措辞及原坏句“宠物义何中技能”，无状态ID/忠诚阈值或概率。

单人HP0气绝判败后回场景HP1；团体中一人气绝可继续的原文“或”不强改“且”或形式化布尔；伤害远超现有HP另述旋转打飞至纪录点，无倍数/地图/事务。没有死亡不等于没有惩罚，所有气绝不一律回纪录点，HP1不当百分比/最大HP，纪录点不证明本地存盘R79。唯一原图img/5.gif实际跳裸域20011023202109/119327B/SHA7caf79fb6e27b6189669da2396129a4cd76b5e967fb7dc91fa842b6e053b165e，640×480/1帧，已目视/全解码，是户外骑乘而非八命令战斗界面；英文标签不证语言/地区/同构建，外观不绑定原人物/宠/SPR。

14本包及49相关测试、两HTML一GIF实输入重放和10真实正文语义改写拒绝通过。预检曾发现HP1子串误接HP100，已发布前纠为完整整数，失败未抹去。原HTML/GIF/放大图不进Git，独立CI/双ZIP保管按实际后验。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-35回全官方版本22域另一具名材料；本页止点已达，不扩全魔法/战斗helper，原脚本/配置/具名菜单/轨迹才重开未知。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING，全部原历史/22域保持。


## 2026-10-20 R34实际双CI、图文差异与永久派生保管

内容26b1ce900a732260884161704d8edd69ea397324/treed765be25545e030988bf8d835a87f9dc3d771f3f自身候选10/main11全success后非强制快进；source run39413081347/39413323716，job118595391639/118596204622各实际14测试+两HTML一GIF重放。artifact12259289716/12259992868已实下载，ZIP均2076B/SHA256 9d79accb29e4796589ea3590c07092337aa00b249ee17b6c3609c5504ac78cbd/32871b0fa14866ac138b00a20c8a2a48de1498507f94d8c3fca896f1839afd68；唯一replay.json均4360B/SHA256 f5eabc53cfc4faf6b6e04d3b5c4fd9c36c0b6f61bc375319bac3d1fa8ffaaa0d，候选/main/本地完整原派生JSON逐字节一致。双CI原JSON及CUSTODY永久固定源报告/十实际语义改写反例/派生字节、SHA、Git blob，精确HEAD/run/job/artifact/ZIP/raw链和八启动全文前缀；原HTML/GIF不进Git。

独立远端干净检出49相关测试、另一HTMLParser重算正文核心、Pillow完整GIF解码/1帧与八完整历史前缀通过；追加保管用例后50相关测试另实测。户外骑乘原图不当八按钮战斗界面，托管不当作者，待机状态/转生主体/团体“或”措辞不补原状态ID或可执行判定；HP1整数不误接HP100，三类失败/返回地点分开，原脚本/概率/公式/惩罚仍未知。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-35回全官方22域另一具名材料，停止本战斗helper。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停保持。保管提交自身Actions后续按实际，不套父绿灯。


## 2026-10-20 R35台湾7.5庄园约战计划、九成资格冲突与分配边界

本轮新读远端main9f97ea8dd6bb7285a18ad13c5497d571f24c36be/tree6f444bf285f20f9f437b62e4fc8c3c674c177f6d，415分支/0PR，自身8main/7候选全SUCCESS；八连续性/路线/22域全文固定字节/SHA/blob，旧queued37642417333保留。最高NEXT35回22域，选择家族庄园竞争/经济/排行UI，不扩上轮战斗helper；重新选定官方实际web键89，不自动追R33续篇。重取P0目录实际20050612011406/28883B/SHA19661e2acca046bf8c6dc86dc968107fe9935cd58a8f3cd8ce5e1de5aeba7f8b，同表行标题7.5版報導之二：莊園約戰新規/2004-6-17；P1请求目录时刻实际跳20041206162649/18288B/SHA8109af26dabefab11b4bda949c6580e68ae9d48db158a354ddf380b31e93de41。严格Big5，官方“酷哥打算”计划不认证实际部署；目录日期/网页键/捕获不当补丁上线日或游戏ID。

13合同/中文规格补出气势由人数经运算加前次庄园战后累计声望、百人各5点例式100*100/10+1+5*100=1501，算术单独核对不推广一般人数/取整或五点每天。原“高于守方九成”却允许900挑战1000，严格措辞与相等例保留为UNRESOLVED，不改>=或901。更高气势可顶替既有流浪挑战者；宣战18–22、成功后24h开战、22点确认建议，时区/端点/替换重计未写。两族累计声望战后0不清人物终生值；守庄气势×10000、在线成员按贡献每点5000、余入家族银行，不补贡献定义/重置前后取值/离线或挑战方奖/银行事务。休4天、第5宣战、第6战斗不是每周或精确96h；无人挑战视同守庄奖，不补其重置。取消合成料理声望及排行不当删除两功能。

唯一实际内嵌sa0616.JPG请求正文时刻跳20041207062827/107675B/SHA17189e9f25e8b8e0a8c324df28a0588d4eb53cb3b8d282f188412a6a815244a1，450×338，目视/放大核十大家族氣勢选择框、合成/料理旧排行与自己家族气势排名入口。入口不是榜单数据/宣战或到账，旧入口与取消计划并存不证明已保留或已取消，非原生分辨率/同构建/原NPC/SPR。有限引用已验大陆4.0门户派生D1，完整SHA/Git blob固定前10扩前20/九庄园，地区/来源/版本分开，不给台湾附加前20资格或统一补丁序。

14本包边界测试、12真实正文语义改写拒绝与两HTML一JPEG及一已验派生输入重放通过；首次相关命令误写旧测试模块名，仅本地导入错误，纠正实际文件名后重新验证，不当远端失败或源失败。原HTML/JPEG/放大图不进Git，独立CI/双ZIP保管按后续实际。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-36回全官方22域另一具名材料，本篇/唯一直图/有限对照止点已达，不扩六转/PvP助手/全庄园。原脚本/官方勘误/规则账本或运行才重开未知，特别九成门槛与分配取值时点。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING，原22域与全历史保持。


## 2026-10-20 R35实际双CI、阈值冲突与永久派生保管

内容f2cc9bf71421f5923f15b5691f2824bd33628f56/tree023719bced74982b6d09773ba39ca3c178868ea5自身候选10/main11全SUCCESS后非强制快进；source run39415559453/39415672602，job118603581099/118603954916各实际14测试+两HTML一JPEG及一已验派生重放。artifact12262045696/12261546475已实下载，ZIP均2746B/SHA256 f431321647f4b8ae713130f5999eeaf2368fd7a00acc9146c64b3163f4768de5/32a963dc57c25dac27e99904e2fa58d091276f095a6e252c11ae0785617c212c；唯一replay.json均6049B/SHA256 f944228117f0b487c68e56ca249ef5cd06ae3d12b44360fddbde617192b0fefd，候选/main/本地完整原JSON逐字节一致。双CI原JSON与CUSTODY永久固定本源/十二实际语义反例/大陆既验输入/双派生共五文件字节、SHA、Git blob，精确HEAD/run/job/artifact/ZIP/raw链及八启动完整前缀。原HTML/JPEG不进Git。

独立远端干净检出45相关测试、另一HTMLParser重提八段hash、Pillow全JPEG解码450×338、原生Git blob核D1、1501算例与900/1000恰九成算术及八完整历史前缀通过；追加保管用例后46相关测试另实测。计划/部署、严格九成/相等例、人数算例/一般公式、累计/终生声望、在线贡献/全员发钱、战后重置/奖励取值及菜单旧入口/排行实际保留分别保持。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-36回全官方22域另一具名材料，停止本庄园篇/助手递归。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史保持。保管提交自身Actions随后实际验收，不套父绿灯。


## 2026-10-20 R36台湾2004法师属性修正、相反转伤方向与两瓶新酒计划

本轮新读main66fd324838517fcd496ae5bf3a7aff1f66d5ae4b/treecabf95e4664aad56116c874ce7357f153dd160e6，418分支/0PR/4825项完整tree无AGENTS、自身main8/候选7全SUCCESS；八连续性/路线/22域全文固定SHA/blob，旧queued37642417333保留。最高NEXT36全域重排，选择职业魔法/骑乘伤害/属性调整任务，停止庄园helper。P0同叶行网页键69/解開法師變強之謎？！/2004-4-5；正文请求目录时刻跳20041206160744/18301B/SHA256 6b3b57b574fa1c200c44aa2ea93dfffb9ce229b4e7268679a7ff0319f091300f，严格Big5。正文未编号，不强贴7.5；模板精灵召唤题名不当文章标题，日期不当修正部署。

8派生记录/中文规格：运营方报告法师攻骑乘目标时，人物地水火风与法术火冰雷错配，引发地人较伤/骑金飞较少伤及不定随机现象；不是原代码/概率。拟分物理元素与闇灵能量，两火同字异义；法术相对物理无属性，原则上人宠平分，另以战场属性优势分配。地人骑金飞例施地的精灵把人物伤害移宠，施风的精灵反向；同属性可保持平分，不补无条件半伤/比例/取整/消耗/持续。拟在訐譙龍任务加入两瓶调人物属性点新酒，未名/方向数值/价格步骤/上线均未知；金飞不绑定物种原ID。

缩略图实际跳20150408182032/36917B/SHA74028b94ae5c9ced3cb537f1d44791bfd55d359dcc6dc90d40e6c21c3ade5cdb/300×225；唯一链接大图跳20040408015726/60745B/SHA7afb898b2c5f202b6c810f474c64376f3decbcf3814929f19716647aac1ba463/640×480。目视洞穴蓝水、橘红长颈骑宠/骑手及旁立人物，酷哥聊天标签；不认证同次图/原生分辨率、任务NPC、金飞外观、酒菜单或修正运行。2015缩图非2004字节。两HTML两JPEG实重放、11真实Big5正文改写在绕过全页字节门后语义拒绝；原件不进Git，CI/ZIP保管另按实际。

来源规格止点已达，不扩訐譙龍全任务/全魔法/酒表；原脚本/同版补丁/具名酒表或运行才重开。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-37回全官方版本22域另一具名材料。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING；全历史与22域前缀保持。


## 2026-10-20 R36实际双CI、两火语义与永久派生保管

内容c5bc2aca0eded77a3116d662a057771da1a91469/treeca30661bc367d45c9996bf2d4cc22c0ed6f651c7自身候选10/main11全SUCCESS，source run39417727148/39417830313、job118610729470/118611070986各实际10测试与两HTML两JPEG重放。artifact12262014170/12262345481已实下载，各ZIP2500B/SHA256 dfcff9d55fffe915e4353c6ec4488dfa1b600744228c5ddaf17e9512e09548f4/73be8a972b268f7f39f3b4a9c96c48927d3f18c5f9b0b0e6451aa945b090781d；唯一replay.json5713B/SHA256 1ed24ae3aa2b476f784d8577c1265900dab355ee4b01821de2bfdd19d9712bcf，候选/main/本地完整原始JSON逐字节一致。CI-CANDIDATE/CI-MAIN-REPLAY/CUSTODY永久固定源报告/11真实正文改写/双派生四文件的字节、SHA与原生Git blob及精确HEAD/tree/run/job/artifact/ZIP/raw链，八启动全文前缀固定；原HTML/JPEG不入Git。

独立远端干净检出46相关测试、另一HTMLParser七段正文hash与两实际图片链接、Pillow完整JPEG双解码和八完整原生Git前缀通过。新增保管用例后47相关测试另验。物理火/闇灵火不混同，原则均分不变无条件引擎，地/风相反转伤方向保留；两瓶酒仍计划且未名，图中酷哥聊天不是任务对话，2015缩图不倒填2004。无版本号/部署/原公式/酒表/实服执行，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停。NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-37回全官方22域另一具名材料，停止本魔法/新酒helper。保管提交自身Actions另按实际验收，不套父绿灯。


## 2026-10-20 R37日服2008虎追任务、传承失而复现与官方谜面

新读main eb9287c662656b4dd127d960e3e25b0e934c9a25/tree9d7d6a46a7634f3f7d8d32ae5cea46be8736283f，421分支/0PR/4835项完整tree无AGENTS，自身main8/候选7全SUCCESS，八连续性/路线/22域全文固定SHA/blob，旧queued37642417333保留。最高NEXT37全域重排，选择日服具名任务/地图/故事，不扩台湾魔法helper。重取R32已知媒体URL，只处理新虎追段；新得官方20080929194642捕获5760B/SHAd7f6df9e6370f8e77d09cdd335c23a735448b935588fda66e40a8e4caa65d829，UTF-8 BOM/声明核实，9月非6月上线当日字节。媒体2008/06/20 22:28发布文引文报6/24实施，编辑归运营者DigiPark，不证部署。

10合同/中文规格新增虎追い山/三匹の虎～虎追いの詩～、七章捕虎传承诗与攻略线索；七章是诗结构，不是七任务且全文未取，三匹不当三种/完整宠物主表。诗在ギール岛重唱，不给山定位。ニース异变与生活变化—虎消失—诗被遗忘—某种到来—重唱的文献叙事，不具名来者/异变年代或倒填1999。官方纯水/追虎武具及防具/相逢才知其意仅谜面，非确证物品/奖励/捕获步骤。官方图示可能不同、未来平衡可能变化两限制语保留。核心官方1220B/SHA8787c1edf9cdbdd8d331382e5efe20b5f2d4db006eb10b5879a62f8f7a3238cf，媒体1180B/SHAe55c11ff1dddbbd7674b2f3b8c55f231b9096e5b6a710d7d62b7110fbeee0f01。

官方真实6GIF href按裸域/www原样一次有限请求均404，未盲递归，不泛化档案全面缺失。媒体真实SS/001–004四250×200 JPEG全取/目视红黑条纹虎和队伍/灰岩走廊/另一人影室内/沙地棕榈肋骨，不绑NPC/物种/原图ID、原生分辨率或捕获奖励运行。当前媒体像素不是2008捕获，不替代缺失官方GIF。原HTML/JPEG不入Git。初次编码猜测Shift-JIS严格拒绝后纠正UTF-8；初次反例命中媒体导语而非发布文，审计未生成致本地测试缺文件，限定发布文容器重做13实际改写拒绝与两外层meta正例后50相关测试通过；不是远端失败或源缺失。

独立CI/ZIP保管按后续实际。止点一官方页/一媒体任务段/四图/六精确失败，不扩七章/全地图/捕获攻略。原脚本、官方具名诗章/奖励/任务轨迹或原ID绑定才重开未知。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-38回全官方22域另一具名材料。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING；R32原范围及全部旧历史/22域前缀保持。


## 2026-10-20 R37实际双CI、官方失图声明元数据与永久保管

内容1463429fa2c14eeb0fd6a0d35985b5a280f14128/tree250e2f1dbefb56aa9637e3e0ac6fda822a0ea6dd自身候选10/main11全SUCCESS；source run39421273992/39421452476，job118622527112/118623140519各实际11测试与一现行媒体HTML、一2008官方HTML、四JPEG重放。artifact12264270040/12263706176实下载，各ZIP2047B/SHA256 162c4982fbe40d696e2d12b842e92891a8249cfe2379f23c532ca56a5923b87f/cb1edf00f5c3e34c4522d6e7cc88aeeb06dd3dcca0a6b8405e165944ad902682；唯一replay.json4599B/SHA256 dbfc56df3e1cbdf5d86d2c0c8a7d7d235a155be325b81434eaad43e5871b466c，候选/main/本地完整原JSON逐字节一致。永久CI-CANDIDATE/CI-MAIN-REPLAY/CUSTODY固定源报告/13实际变异及2正例/新声明元数据/双派生共五文件字节、SHA、原生Git blob和精确HEAD/tree/run/job/artifact/ZIP/raw链。

独立干净远端检出50相关测试、另一HTMLParser两个核心、Pillow四全JPEG、13真实改写与两meta正例重做及八完整历史前缀通过。另从同一已验官方HTML补存六失图href/alt/声明尺寸：banner未声明，uta_osa/tora_in声明250×200，tora_map1/2/3声明150×120；非已取像素实测、NPC/地图名或原ID。此补充在内容双CI之后加入，后续源重放逐字段核实六声明，不改变已验派生JSON格式/语义。加声明边界及保管两用例后52相关测试通过，保管提交自身CI另按实际。原HTML/图不入Git，七章全文、三物种、具体奖励、地图坐标和部署均不补。

最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-38回全官方22域另一具名材料，停止本虎追/全图/全诗helper。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING；全历史保持。


### 2008-07-15—07-29：日本版“第200种宠物”直接捕获活动（同期发布文，FACT/边界）

2008-07-15 16:22 刊登的4Gamer运营商发布文（发行来源ガマニアデジタルエンターテインメント，游戏运营方DigiPark）称服务第9年有200种宠物，“フクゥーリ”称第200种。活动公告区间7月15日16:00到7月29日13:00；在游戏内**直接捕获**才计 GASH 外部抽奖，交易等取得不算；每GASH账户一次，拟抽500位各100 GASH点，8月5日约17时计划发放。同期声明不保证当时服务器实际执行及完成分发；没有原宠物master、图号、捕获率或200个姓名。**不得倒填JSS1999/TW1.0或把第200种当原服务器ID。** 原文证据、状态、当前HTML字节SHA见 docs/specs/STONEAGE-JP2008-FUKUURI-CAPTURE-CAMPAIGN-SOURCE-R1.md 和 research/recovered/STONEAGE-JP2008-FUKUURI-CAPTURE-CUSTODY-R1.json。来源 https://www.4gamer.net/games/013/G001377/20080715027/ 。


### 2009-04-28 日服DigiPark公会通信与白炎、经验限时活动（来源事实/非运行认证）

4Gamer同期转载DigiPark发布文称日本版维护时加入Guild系统用于异地多人群聊，同期新增ハクエン、400 Gstone白炎票券与白炎袋/印章，5/10/15印章奖励，5月1～7日限时稀有敌人はぐれシロベアル的15具名场景，以及药师5秘药碎片首次/重复不同人物EXP奖励。白炎袋正文称7种，现可见6具名表项，不补虚构第七项；这是日本2009的公告内容，非JSS1999、台湾大陆家族同构或原服服务器脚本证据。2026现页的完整HTML SHA会变化，但公告核心规范文本SHA保持；双派生保管及精确run/job/ZIP见 research/recovered/STONEAGE-JP2009-GUILD-HAKUEN-CUSTODY-R1.json。来源 https://www.4gamer.net/games/013/G001377/20090428039/ 。


### 2006-03～12 日服GaiaX火山、风谷与水源雨林地理（同期文献）

2006-03-14原运营发行材料称ミライア群島西北发现火山岛「紅炎の地」并计划4月18/5月2分步；2006-05-01材料称第一阶段已结束、中央「炎渦の頂」有多条路及未知条件支路，拟开放上层及火山口Boss。2006-12-07资料宣布12月12日新增两地：「香颯の地」为米莱亚群岛高地风蚀峡谷，「雨祝の森」为ジャルガ島河水源头与终年降雨密林。三源GaiaX运营引文由4Gamer刊载，属于日服2006版本史，初代1999/TW1.0没有对应原始字段证据；上线实际和原地图坐标、野怪物种、Boss身份、特殊入口规则未证。出处 docs/specs/STONEAGE-JP2006-WORLD-GEOGRAPHY-SOURCE-R1.md，永久校验 research/recovered/STONEAGE-JP2006-WORLD-GEOGRAPHY-CUSTODY-R1.json。


### 2007-02-02 日本新手装备与商城入口（同期资料/未认证部署）

GaiaX运营引文描述始まりのこん棒数值与Lv1零气力毒咒，公告2月2日17时恒久设置；同页4Gamer导语报告免费及商城/码/NPC领取。两层分别归因，不把媒体领取路径冒充官方原话，不识别未名属性或倒填初代。出处 https://www.4gamer.net/news/history/2007.02/20070202173939detail.html ，规格 docs/specs/STONEAGE-JP2007-STARTER-CLUB-SOURCE-R1.md。


### 2005-11-29 日本三特殊地图公告与收集任务（文献事实/非执行）

GaiaX引文描述巨獣の島、閉ざされた氷窟、バルツ山の洞窟的三层定位，亲犬收集换幼犬及古代山地遗址叙事，Boss仅可能掉落珍物。同期媒体另报12月2日免费化/门票，评论组队影响仅担忧。2009同名冰窟不证同地图ID，山与洞窟不强并。来源 https://www.4gamer.net/games/013/G001377/20051129193618/ ，规格 docs/specs/STONEAGE-JP2005-SPECIAL-MAPS-SOURCE-R1.md。


### 2003-11-18 华义“2.0”复古服务器分支的扩组预告

新浪转载华义官方消息，回顾9月4日原组开放，拟11月19日上午9时维护后增开2.0(2)、旧组改2.0(1)，并报告新组开放后收费；正文月日未写年份，均以2003刊文语境保留，不认证实际开服/计费。骑宠/较安全交易/交通与家族功能仅来源报告，四庄园只两名，不移植4.0九庄园表或2001原版二进制。出处 https://games.sina.com.cn/newgames/2003/11/11188486.shtml ，规格 docs/specs/STONEAGE-CN2003-CLASSIC20-BRANCH-SOURCE-R1.md。


## 2026-10-21 R44日本2007人物故事与物品行为来源

2007-01-30 GaiaX发布文节录记カルターナ村长宅レン收材料制バレンタインチョコ，约600体力回复我方全队、1月30日维护后至2月27日维护开始。2007-06-12运营发布文回顾情人节/白色情人节恋情、村长孙女レン与ワイト及レン父亲考验；击败特定恐龙取建材交村边ワイト，按建材等级获奖品/点数，指定收集量推动新居扩大。结束日期原写6月27日(火)与2007日历(水)冲突，真意未定。另ディノ・シャルマン三强度香水恢复人物魅力、商城销售；人物魅力较高宠物较易服从，不是宠物忠诚度或保证服从。八记录/两关系见JP2007-REN-HOME来源规格；无最终婚礼、持久房屋、阈值/物种/材料/原ID、同版实服过程，不能回填初代。


## 2026-10-21 R45胜思时期摆摊资料

2011-01-12/2012-12-04新浪胜思具名宣传记左上摆摊入口、物品/宠物→价钱→广告→确认、待售红SELL及四聊天议价渠道。2011预告1月15日不删档封测仅当时计划。两期操作段相同与场景相似不能证明同构建；当前上架窗口样本1000不成标准价/币种，任务费用原词/随处宣传不推全税费零和全地图权限。数字版本、买方结算、原服过程与截图原年未知，详情CN2011-2012-STALL来源规格。


## 2026-10-21 R46独立作品SA2前期养育访谈

同期2006-07-10 TeT报道链接SA2开发陣访谈并明确2006年2月录制，精确访谈刊日未知，页脚发行日不当刊日。遊佐称完整新作/宠物学技能，石川称培养影响AI性格参数、两宠相处产卵/承亲本资质、5匹随行/DEN10—15種類/约20匹总量、寿命/转生与照顾不佳离家、普通E邮件维系离线世界联系；長田称DEN为养宠空间且扩大可增容量。均为受访者前期说明非部署，单位/约数/未知公式原样保留，不能倒填SA1/TW1.0。详见SA2-PET-CARE-INTERVIEW规格。


## 2026-10-21 R47 华义2.0(2)开服后四庄园与家族具名报告

新读main ac389193dbd71e5977975840601404e1fc022134 / tree d0a200343d5701c0e44af580096126b0ae32a060、435分支/0开放PR/4934项完整树无AGENTS、自身main9项全SUCCESS；旧queued37642417333保留。九启动全文与路线/22域索引固定，最高NEXT47进入有限的家族/庄园内容归属审查。

新浪2003-11-20 16:43明确转华义消息的后续报道当前33636B/GB18030，核心SHA d16ab4ca25e051f0c88916df49003cfc46d66c819864be53ae4ec2d457ca8aac；按原顺序：萨姆吉尔/圣战部落光/4524，玛丽娜丝/永远友情/2280，加加/龙族/4079，卡鲁它那/友情岁月/2811。报告11月19日“中午”开机，不推精确12:00/时区/构建。平均同时在线2000人以上、24小时内建族超过200均为运营方报告；“四家族人数超过90”范围不明，不拆每家族90。声望不是门槛，家族不是2026当前占领者。专属骑宠地位表述无名单/规则；挑战/PK为未来时；20日早晨繁忙临调恢复是运营方陈述，非独立执行/uptime/补偿见证。

实际正文一图当前19585B/300×225、SHA ad1f011da8a7c83187e856064e376d011b88114ddf1590136722afa9ecd03c40，原http/requested HTTPS分开，完整Pillow解码/目视；不标庄园家族/宠物ID、拍摄日期、原生分辨率或事件证明。正文外编辑相关链接实际指回R43预告，固定旧契约全文字节/原生Git blob；仅新文补玛丽娜丝/卡鲁它那和占领快照，旧文remaining_manor_names=null保持。09:00维护与“中午”事后报告不合成精确开服，WGS执行/九变四补丁/跨版本规则不证明。

8派生记录、中文规格 docs/specs/STONEAGE-CN2003-GROUP2-MANOR-REPORT-SOURCE-R1.md、真实取源工具/18实际源改写绕过digest门拒绝/外层script正例；独立正则HTML实体重建正文与顺序列表一致。初轮10本包/109相关测试零跳过。原HTML/版权JPEG不入Git；候选/main自身Actions和ZIP永久保管另据实追加。有限包止点一页一图一旧契约，不扩庄园/声望helper；重开需具名规则/原ID/实际过程或有日期原档。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-48回全22域另一具名材料，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史前缀保留。


## 2026-10-21 R47双取源原字节保管与主线独立验收

内容119ba1d8ae75384f6af2fb7ff0fb5ce21fc00e44/treed67e445ca011be4e221aeea3053caa78565458e9候选10项/main11项自身适用Actions全SUCCESS。候选run39550739816/job119059107914/artifact12323665629，主线run39550814576/job119059348025/artifact12323641358各实跑10本包用例零跳过，重新取得33636B页面/19585B实际JPEG、18真实源变更拒绝/外围正例。远端内容干净检出109相关检查，独立正则/实体正文核心及有序名单/数字一致，当前图完整Pillow解码/目视；CI只验证图原字节与SOF尺寸。

实际下载双ZIP各3169B，SHA256候选3fc0a10eea71efcb053af2ba8bd25abdc410c3168d463dd6da7d1cec19ae0b03 / main559545f9b4e4ccf80e5fcea4e060548514724cb593c0995eca1f330457d30a62；各唯一replay.json7654B/SHA256d7eeebad05aa8281e6b557a43532f3c667c87e061a4ad137dbc0c14b56dfc249、原生Git blobd742b10ac5fcf1e6ab35e862ca9aef17c739efd6，候选/main/本地逐字节一致。双raw、十来源/工具/工作流/规格/旧契约/依赖pins、九完整启动历史前缀与21实际workflow永久存research/recovered/STONEAGE-CN2003-GROUP2-MANOR-REPORT-CUSTODY-R1.json；原HTML/版权图不入Git。新增强制收据门后本包11项/110相关检查通过，首轮10项不改写为11项；本保管提交自身Actions须后验，不套父提交成功。

R47有限报告包结束，原文“中午”/精确时分、四家族人数歧义/逐家族数、声望快照/规则门槛、未来赛事/已执行、运营方报告/独立统计、R43预告/本次后文与版权图/生产资产分开。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-48回全22域另一具名材料；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，历史完整。


## 2026-10-21 R48胜思高厨料理采购、宠物制作、交付与荣誉用途

新读main551e93eef582066eef6ffc8540adb41bd4ba2e09/tree6bbbd62a56ef8578284d35938359cc60c7b9798f、436分支/0开放PR/4927项完整树无AGENTS；R47保管提交自身候选10/main11项Actions全SUCCESS，完成前轮收尾核验。九启动全文/原生Git与22域索引重新固定。当前最高NEXT48，轮换生活技能/任务/经济，不扩庄园helper。

新浪2012-02-10 15:51胜思具名宣传https://games.sina.com.cn/o/n/2012-02-10/1551581681.shtml 当前146067B/GB18030，正文规范SHA f7a15a015e8791ed94221d43203f414b43714edff394fc1448bbeacc31111f11；两实际sa.cins.cn链接/自称胜思，未认证原始运营文件或2012原快照。五条版本化记录及规格docs/specs/STONEAGE-CN2012-COOKING-EVENT-SOURCE-R1.md：周一至日19—21点高厨料理，准备料理宠/村庄宠物店可学，向扑满乌力/黑乌力购买，制作两具名蔬菜色拉，交加加村24店大厨换奖励，荣誉值可换宠物/道具/装备。原文或者不改同时，配方/价格/坐标ID/奖励值/次数/时区/端点/首次上线未知。

宣传并列8.5魔域大冒险与2.5精灵王传说，活动适用组null，不推两组共有、不当2002原2.5或TW1/JSS1999；荣誉值不当石币或现金。两实际图115307/125689B、550×410/550×409完整Pillow解码/目视为人群宠物背景，不证料理或交付；第三壁纸只存链接、未取未验。原HTML/版权图不入Git。19真实正文语义改写绕过摘要门拒绝、外围script正例通过；独立核心/流程另核，候选/main自身取源与永久ZIP保管另据实追加。

止于一活动五记录双背景图；重开需同组具名配方奖励表/坐标ID/时区次数说明或原服过程。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-49回全22域另一材料，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，完整历史前缀保留，无分母不报恢复百分比。


## 2026-10-21 R48独立双取源、背景图边界与永久派生保管

内容1a6b5f2ed5f06cb68678b701442df1ef9a144f5f/tree5f6254cc7f2dddafd77d83da0dab2b046ca8a570自身候选10项/main11项适用Actions全SUCCESS；候选run39552068852/job119063286716/artifact12324405541、主线run39552188075/job119063656876/artifact12323439299各实跑9本包用例零跳过，HTTP146067B正文/115307与125689B双JPEG、19真实正文语义改写拒绝/外围script正例。干净远端内容检出119相关测试通过；独立正则/HTML实体核心与采购制作交付次序通过，本地双图完整Pillow解码/目视；CI只验原字节与SOF尺寸，不冒称运行截图。

实际下载双ZIP各2902B，SHA256候选03c818f803def6829c1b6161c91c7a40d4cbee2496a2b7ca1b59d412dbad2cf5 / main3d28bf90c46413359a5a56e2dc24476c0a9406c22f5732556edb1cf4c9860fcb；各唯一replay.json7744B/SHA2567f41ff51711db4d11f82faa6b5cc9c701b756a70063895b8ac43800aa04d003c、原生Git blob33abebf55968f3d2909e224476912079efd8358e，候选/main/本地逐字节一致。双raw、十来源工具依赖/工作流/规格pins、九完整启动前缀和21实际workflow永久存research/recovered/STONEAGE-CN2012-COOKING-EVENT-CUSTODY-R1.json；原HTML/版权图不入Git。新增强制收据门后本包10项/120相关检查据实验收，原9项历史不改写为10项；保管提交自身Actions另后验，不套内容提交绿灯。

两服务器宣传/活动实际适用组、或者/两种必交、荣誉值/石币现金、时段/时区次数、背景人群图/料理执行继续分开；R48有限包结束。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-49回全22域另一材料，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史保存。


## 2026-10-21 R49大陆6.0登录建角、新手村及透明伴随图边界

新读main51bec22420b3ebdef554a6ebaeee3904350002f9/treeaa3dbc5f746a4141b3187a508b0538db8d8cee5f，437分支/0开放PR/4937项完整树无AGENTS，R48保管提交自身main11项Actions全SUCCESS。九启动全文/原生Git与22域索引重读固定，最高NEXT49轮换登录建角，不扩料理/荣誉助手。

新取得新浪6.0新手流程https://games.sina.com.cn/zhqu/sta/liucheng.shtml 当前64286B/GB18030，显示新浪游戏2003-05-30 14:14、投稿入口及2006-10-09重生成注记。投稿入口不证明网友作者，亦未认证华义原版手册；注记不当原刊或拍摄日。所选进入/建角/新手村与图链接核心SHA7530ed367b3deb63486378be93773078bb4e484e5da84506789c496dd62af92e。另新浪2003-06-09 12:15运营口吻分服升级预告https://games.sina.com.cn/newgames/2003/06/06092201.shtml 当前33218B，去广告核心65c6c350d032f4e6d6be5099db28bfaaef09d4be7fcb781f89ffa7d7831723de；预告6月10日中国网通9先升、其他分期并需更新客户端/有新手村，不当实际执行、不替指南和图认证构建。

七条记录与规格docs/specs/STONEAGE-CN2003-ONBOARDING-SOURCE-R1.md：Deeplay/登录说明、插叙角色页、12人物各4配色、8个字符/面部可设、20点经验值原词、四具名出生宠/未名技能、新手村出至萨姆吉尔后不能再入等均保留来源层。字节/汉字数、独立4×4色、EXP或属性点真实语义、技能ID/首发、地图NPC坐标与执行未知；原文乌力乌力不擅改，速度体力建议不当最优公式。

实际十GIF中032/035/038/041/044为五张当前低分辨率画面；033/036/039/042/045各73B全透明，逐一完整Pillow解码alpha[0,0]，不算另外五张恢复画面。五画面目视，尺寸不当原生分辨率/确切构建；原HTML/版权图不进Git。20真实正文语义改写绕过摘要门拒绝、双外层script与重生成注记正例通过；独立核心/数值/有序图链另核。候选/main独立取源与实际ZIP永久保管另据实追加。

有限止点两源选定内容/十图对象；重开需同构建原手册或运行过程、姓名编码/20点规则/技能ID或传送证据。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-50回全22域另一具名材料，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，所有历史前缀完整，无分母不报整体完成百分比。


## 2026-10-21 R49双来源、十GIF角色及永久派生保管

内容2a0826b6cb5a0b34cc9d64140f64fc84863c4277/treeb5cd837d4fe2596711fa8a4dd85caf39e3508c86自身候选10项/main11项适用Actions全SUCCESS。来源候选run39583968290/job119168158494/artifact12337938078，主线run39584279790/job119169193444/artifact12338712148各实跑10本包用例零跳过、重取64286/33218B两正文与十GIF对象，20真实正文语义改写拒绝/双外围script和重生成注记正例通过。远端内容干净检出130相关测试、九完整历史前缀及原生Git核验通过；独立正则/实体双核心与原词数值/有序图链一致，十图完整Pillow解码、五实际画面目视、五占位alpha[0,0]。CI仅比原字节与GIF结构，不冒称原客户端渲染或执行。

双ZIP真实下载，长度候选4442B/main4442B，SHA256分别21b46bd3a31fac7e30c93ca66c84b32375cdf850f7a213c264b595fdb8b793bd / 484ee50524be6c4c67a41e24532e215fa326d4c77289771b43430ce87f7cd735；各唯一replay.json19804B/SHA2568879a3ec6021797d56a9bfd235a2aaa3794f468f72962c9d0497fbcd78b5cff6/原生Git blobde5b40eefcb5fca0775af785914e97e22bb4a455，候选/main/本地逐字节一致。双raw、十来源/工具/依赖/工作流/规格pins、九完整启动前缀和21实际workflow永久置research/recovered/STONEAGE-CN2003-ONBOARDING-CUSTODY-R1.json；原HTML/版权GIF不入Git。

新增强制收据门后本包11项/131相关检查另实验收、删除收据必须失败；首轮10项历史不改写为11项，保管提交自身Actions后验，不套内容绿灯。投稿入口/作者资格、重生成/刊发、八字符/编码、二十点原词/运行时字段、预告/执行、五画面/五透明伴随对象保持分开。R49有限包结束；最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-50回全22域，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史保留。


## 2026-10-21 R50日服2004聊天过滤、探索信息与NPC配置分期

新读main531f15f7f3831300a288e66b8883adfafbb3c9f0/tree8b749c1c0a13648759d36703700cf55cf9feef38，438分支/0开放PR/4947项完整树无AGENTS；R49保管提交自身main11项Actions全SUCCESS，九启动全文/原生Git与22域索引新读固定。最高NEXT50轮换社交交互，不扩R49建角/新手村助手。

4Gamer2004-07-30 23:12署名Kawamura同期报道https://www.4gamer.net/news/history/2004.07/20040730231235detail.html 当前10860B/CP932，正文核心SHA4ea1de1163cd989576c5fd90714eb43644b6a222416ceedad8fd0aa9ab5af506；不是逐字运营发布文或运行见证。HTML meta作者不当正文署名，五正文槽仅一实文四空模板，不认证2004原字节。六记录/规格docs/specs/STONEAGE-JP2004-CHAT-UPDATE-SOURCE-R1.md新增。

报道登记对象聊天过滤，不补UI/容量/频道/身份键/保存、封号或交易阻断；首次大更新仅指报道所称2004年6月正式服务以后，8月1日15—16时为维护计划。新未名岛、サイナス岛/ジャルガ岛各一未名洞窟、マーナ推测秘密均不补地名ID/入口/剧情Boss；部分NPC迁居带ようだ，非执行认证。8月3/6日任务NPC配置及约30分钟维护，与记者推测新任务届时触发分开；无任务条件/实际开放/精确时刻。新用户十日试用不当所有人永久免费。

实际三图按HTML顺序_0/_2/_1，31490/26016/24235B、200×133/170×141/170×141，完整Pillow解码/目视为地图示意、木桥与洞口场景，均无聊天过滤面板，不认证地图/人物身份或原生分辨率。原HTML/版权JPEG不进Git。20真实正文语义改写绕过摘要门拒绝，外层script与meta作者正例通过；独立核心/日程/推断词/图序另核。候选/main独立取源及实际ZIP永久保管另据实追加。

有限止点一报道六记录三图，不扩聊天实现/未名地图/任务助手；重开需同构建官方UI/手册、实际过滤过程、地图名入口或任务开放日志。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-51回全22域另一具名材料，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，历史前缀完整，不报无分母整体百分比。


## 2026-10-21 R50同期报道双取源、图像边界与永久派生保管

内容ba4cb029df19e17e600b8190c91e622d831450e5/tree789916334c019e00db4a0d441a2b5abd33153809自身候选10项/main11项适用Actions全SUCCESS。来源候选run39586280930/job119175869090/artifact12339775719，主线run39586486553/job119176551830/artifact12339479771各实跑10本包用例零跳过，重取10860B正文及31490/26016/24235B三JPEG，20真实语义改写拒绝、外层script/meta作者正例通过。远端内容干净检出141相关测试、九完整历史前缀及原生Git标识核验通过；独立正则/实体核心、日程/约数/推断词与图序一致，三图完整Pillow解码/目视。CI只比原字节与SOF尺寸，不冒称聊天UI或客户端运行。

双ZIP真实下载，候选3435B/main3435B，SHA256分别6668720042822b995a8df522de3ea98ccdc80730edcfa72e724759b6b92ca068 / 9fc374ac7e73316eccfa90e05e98db449afd018c0d0739e88b44d5f7b97225a7；各唯一replay.json9108B/SHA256256f4fa8073b97c077c84518e0af2c3f2f78ddd785fe974c6366f1c85a68f637/原生Git blobaba19db65aafee3fb0cdda6080d129b938739de3，候选/main/本地逐字节一致。双raw、十来源/工具/依赖/工作流/规格pins、九完整启动前缀与21实际workflow永久存research/recovered/STONEAGE-JP2004-CHAT-UPDATE-CUSTODY-R1.json；原HTML/版权JPEG不入Git。

新增强制收据门后本包11项/142相关检查另实跑、删除收据必须失败；初轮10项历史不改写为11项，保管提交自身Actions后验，不套内容绿灯。媒体/运营原文、2004服务阶段/原作首发、维护计划/部署、NPC配置/记者任务推断、约30分/精确时长、聊天过滤/封号、配图/过滤UI与未名地图身份均分开。R50有限包结束；最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-51回全22域，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，历史完整。


## 2026-10-21 R51大陆2.0记录点贡品、原地登出与重入资料

新读main b1b12ebfacdb09580b812dd1fc5a498564145237/tree9f0ac6b72e66c5e8b00eb7cd4f1079c2819805da、439分支/0开放PR/4974项完整树无AGENTS，R50保管提交自身main11项Actions全SUCCESS。九启动全文/原生Git与22域索引重新固定；仅旧run37642417333仍queued，无in_progress，不抹去旧历史。最高NEXT51轮换记录点/位置重入，不扩聊天过滤助手。

从实际华义2.0导航取得基本操作、存储肉位置、公共设施：四精确档案20011204194619/20011204000349/20011204220248/20011204213609，HTML69317/68863/69407/73356B；不是首刊日、具体build或运行证据。运营站承载不认证具名作者/原手册逐字内容；正文“储存”指肉贡品换记录点，不当物品银行。三岛17表行加原地登出/交易YES/纪录点三行为，20记录及规格docs/specs/STONEAGE-CN20-RECORDPOINT-SOURCE-R1.md。

普通注销重入记录点、原地登出回登出地、被打飞回记录点，原地登出/原地注销标签分别保存，不推任何败北/掉线/跨重启；不是本地savedata.dat证明，不重开R79。对纪录点说话取在线人数，统计范围与刷新未知；贡品是否消耗/事务/保存载体未知。基本操作页交易只证接收方YES，不从2010或SA2指南补双OK。

17行北岛7/南岛8/吉鲁岛2，原地名、X/x、多坐标/多肉原样保留。加加/塔姆塔姆重复481，92与426，94、奇喀喀肉不详、191 365/342 466缺逗号均不校正；无地图NPC/物品ID，多坐标意义/多肉AND或OR不补。实际纪录点图片img/image011.jpg按本次正文捕获请求HTTP404，未取得图，不冒称画面恢复或所有档案无图；其余设施/操作图未递归。四HTML/原资产不入Git。

20真实源语义改写移除摘要门仍拒绝、外层script正例通过；独立正则实体表格与重入核心另核，候选/main自身取源与永久派生保管据实另记。有限止点一导航三页选段一失图请求；重开需同构建地图/NPC表、贡品日志/坐标对照或原服重入过程。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-52回全22域，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史前缀保留。


## 2026-10-21 R51四档案双重放与永久派生保管

内容a76e513abf98ea7ce0afc058f2aea43d97875496/treef64a5276fcd11250530b3cf57ba8f69da98a29a1自身候选10/main11项适用Actions全SUCCESS。来源候选run39588403816/job119182947281/artifact12339573656，主线run39588493806/job119183259840/artifact12339878480各实跑10本包用例零跳过、四精确HTML69317/68863/69407/73356B、17表行、20真实源语义改写拒绝与外围script正例。干净远端内容检出126相关测试、九完整启动历史前缀及原生Git标识通过；独立正则/实体重建17行、重复坐标/缺肉及重入核心一致。记录点图404仅为本地实际请求观察，CI没有重取图或解码图，不冒称画面恢复。

双ZIP实际下载，候选3296B/main3296B，SHA256分别6ecb21d9a9f207c9bf27df95eb00b494b3c526f2d8904af2b693d5ac1f4c9888 / 83e2d71ad61af87d851a6921e995adde1ed3f67b2f630320f506269a91482968；各唯一replay.json13283B/SHA256ee53863ce796cda16294efc8f2b60dcbda8daa4d4e5f2e4d9bc9c78ba50a3789/原生Git blob6f23139cee40299ba11b087104aa36f865f5b311，候选/main/本地逐字节一致。双raw、九来源/工具/依赖/工作流/规格pins、九启动完整前缀与21实际workflow永久存research/recovered/STONEAGE-CN20-RECORDPOINT-CUSTODY-R1.json；原HTML/版权图不进Git。

新增永久收据强制门后本包11/127相关检查另实跑、移除收据必须失败；首轮10项不改写为11项。保管提交自身Actions另后验，不套内容绿灯。采集日/首刊、运营主机/作者、记录贡品/银行、来源坐标/可执行NPC点、未知肉/免费、多肉顿号/AND或OR、注销目的地/保存载体、局部404/全部失图保持分开。R51有限包结束，最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-52回全22域；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史完整。


## 2026-10-21 R52大陆2.0三宠物网页外观补充与阿米朵旧对照

新读main47b593b715e25ecb55af2e9b080d92b7a247b182/tree16f697a355ccdf82a07dc4ed038e9688aa4b690f、440分支/0开放PR/4984完整树无AGENTS；R51保管提交自身main11项全SUCCESS。九启动全文/原生Git与22域索引重新固定，仅旧37642417333仍queued，无in_progress。最高NEXT52轮换宠物外观，不扩R51记录点/保存。

选材核对发现104格三页目录已验收，故不重做名录。固定首目录、有限目录和阿米朵视觉报告全文，重取既有20011204194619华义2.0正文69317B/SHA561950fd7bba41e7d39f4a781a671e11e175c7fe08dd1b5481fdf1fd23ba351b。本轮新增网页位置001/004/040三图片像素，007阿米朵仅旧对照；规格docs/specs/STONEAGE-CN20-PET-VISUAL-BATCH-SOURCE-R1.md，三研究记录不当原宠物实体。

001字面???→img/newpet/6.JPG，20011205050022/4196B；004字面??2→2.jpg，实际20011023194345/3785B且最终原主机无www；007阿米朵→7.JPG，20011205051046/4831B旧SHA一致；040呼波波→40.JPG，20011023183116/3520B。四JPEG全Pillow解码RGB83×90单文件帧并原像素目视：绿色四足、蓝圆形轮廓内浅色形象、既有黄褐阿米朵、蓝色直立形象。问号两名不补，呼波波来自源单元格；不推物种ID/技能/SPR/模型/动画。初次从正文档案跳各图，CI只精确取最终捕获，不重演初跳；主机差异不当全站等价。001/004有HTML83×90，007/040未声明，不回填。

旧104位置/98具名/6问号历史报告不变；补充后4引用已取、100未取，本轮新增3/旧对照1、新解名0、新原游戏实体0，不当物种总数或百分比。14实际HTML改写排除digest仍拒绝、4图真实字节反例与外围script正例；独立单元格/实体/路径大小写及JPEG SOF尺寸另核，候选/main实际取源和永久保管据实另记。

止于一既有正文/三新图一旧图/三父Git报告，不自动追100图或helper。重开需明确原名、同构建SPR/原动画/数值表。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-53回全22域，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史前缀完整；原HTML/JPEG不进Git。


## 2026-10-21 R52三新图一旧对照双取源与永久派生保管

内容bbe5302f17e182dddb86a598590cbbe8e38775b0/tree16cd0048f6abb44291fb3850a90882418fe64130自身候选10/main11适用Actions全SUCCESS；来源候选run39590372930/job119189528231/artifact12341830649、主线run39590585725/job119190238811/artifact12341196429各实跑10本包用例零跳过，一69317B已知HTML及4196/3785/4831/3520B四JPEG实际重取并完整像素解码，14真实HTML语义反例、4真实图字节反例和外围script正例通过。干净远端内容检出79相关测试及九完整启动历史前缀/原生Git标识通过；独立四叶单元格名称/路径/大小写、JPEG SOF尺寸一致，四图本地原像素目视。CI不复演人的目视或首次档案跳转。

双ZIP实际下载，候选3289B/main3289B，SHA256分别43ee67d23dc76a9c7904e25ccd91199f0a3ef12f66d020908655cfa6319d43ee / ad4ba2cbf4130491da101b75c45b1d1cd8a8f2e392a313a98f3c23d53b8e78fd；各唯一replay.json11704B/SHA256df992d998a148eecd7e2700b4fae6f0536855858520a5d6086a6d3a0d802ef61/原生Git blob517a955fdb8789f193e30b4b9e1ebbb395cd9847，候选/main/本地逐字节一致。双raw、十三来源/工具/依赖/工作流/规格/父报告pins、九启动完整前缀与21实际workflow永久存research/recovered/STONEAGE-CN20-PET-VISUAL-BATCH-CUSTODY-R1.json；原HTML/JPEG不进Git。

新增强制收据门后本包11/80相关检查另实跑，移除收据及等长改写派生raw一个字节必须失败；首轮10项不改写为11项，保管提交自身Actions另后验。新3/旧对照1、六问号仍未知、104引用中已取4/未取100、网页名/原实体、分时图档/同构建、HTML声明/实测、单JPEG帧/原动画、目视/CI解码、原档主机差异/全站等价继续分开。R52有限包结束；最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-53回全22域，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，所有旧记录完整。


## 2026-10-21 R53大陆2.0回复法术13行、正文目标与数值疑点

新读main7a6042d15f102e18cfb9eec01ef0f6e8e430639a/treeb88673c3d3ea14845fef48a55dda4558090ce344、441分支/0开放PR/4994完整树无AGENTS；R52保管提交自身main11项全SUCCESS。九启动全文/原生Git与22域索引重读，仅旧37642417333仍queued，无in_progress。最高NEXT53轮换战斗回复，不扩R52剩余100图。

既有华义导航真实“回复系”href取得新正文：20011204194619导航69317B，实际回复页20011204210425/67848B/严格GB18030/SHAaa159ec42c9faf663dd726b98d356e4fb56f6903d7a75270fb52c367518e4f80，核心d9e2a259142d981fdc2e4581979ba519b3a0b2f83daa11b8521786efa77c12cf。初请导航时间实际跳正文捕获，CI只取最终精确URL；无署名运营主机指南，不认证作者/首刊/精确build/原服。13等级行+1正文语境均带七字段，规格docs/specs/STONEAGE-CN20-HEALING-SPELLS-SOURCE-R1.md。

原rowspan4/4/3/2为治愈/滋润/恩惠/复活，费用依序5/8/11/14、8/12/16/20、20/30/40、20/35。滋润LV2原+10且耗12，低于LV1+50，疑点保留不补100；表LV不当人物要求/跨版最高等级，耐久力/气力不自动绑定HP/MP原字段。哈鲁仅玩家/表自身、芙蕾雅我方一人或一宠/表单体、提欧全员/表己方全体分层；正文神恩/表恩惠不改名。复活三名希鲁菲尔/雅鲁/哈恩不强配表两等级，也不推顺序升降。主要寄宿衣服铠甲防具不当仅限或全部；宠物昏厥复活建议的少量忠诚下降与经验不当零损/满返公式。

固定旧战斗派生全文/原生Git，CN20-BATTLE-02装备附魔只作定性对照，不重新取旧正文图、不认证同build或执行。18真实源语义改写排除digest仍拒绝/外围script正例；独立13行及疑点/费用/名字另核。内容无图，不抓导航chrome/其它法术页；原HTML/资产不入Git。候选/main自身取源及永久派生保管据实另记。

本地预检曾错误把旧source_reported对象当字符串，首轮10项1项错误/重放拒绝；修正实际meaning读取并建立有效基线。导航反例按真实font嵌套修正，不冒称那轮已通过；非来源变化或远端Actions失败。有限止点一导航一正文一父Git，不实现治疗或扩其它四系；重开需同版配置/ID、原文+10更正或战斗/气力/忠诚经验日志。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-54回全22域，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史前缀完整。


## 2026-10-21 R53回复表双重放与永久派生保管

内容0278ba470b32816aaa072f5e4596d812bb0a5d14/tree2876b1b69b23ac322537011de0ee88a5a533ef12自身候选10/main11项适用Actions全SUCCESS。来源候选run39592464093/job119196561009/artifact12341224452，主线run39592599479/job119197008183/artifact12341743477各实跑10本包用例零跳过，实际重取69317/67848B两HTML、解析rowspan4/4/3/2共13行、18真实源语义改写拒绝及外围script正例。干净远端内容检出59相关测试/九完整启动前缀与原生Git标识通过；独立正则/实体13行效果/费用/名字/限定语、中文表13行逐格一致。图片请求0，旧战斗原正文/图不重取，原客户端/服务器/后代治疗模型不执行。

双ZIP实际下载，候选2686B/main2686B，SHA256分别b44cb0bc2f39b40c5532b7fada8fdab5ba71fede4e8a66c4e256035eecfff293 / 36f7b9c7224c75a3b2a9b65d1c0be795ba7be04c284632b3fcff334d38596df2；各唯一replay.json13077B/SHA2567a7826645bba41ad773fe085fc2b40898aad7066b03b3a6f0df3c23b6c3135cf/原生Git blob4e7aa4114c20e5acbe93b0cc3ebc8093714ca35e，候选/main/本地逐字节一致。双raw、十一来源/工具/依赖/工作流/规格/父报告pins、九启动完整前缀及21实际workflow永久存research/recovered/STONEAGE-CN20-HEALING-SPELLS-CUSTODY-R1.json；原HTML/资产不进Git。

新增永久收据强制门后本包11/60相关检查另实跑，移除收据及等长改写派生raw一字节必须失败；首轮10项历史不改写为11项，保管提交自身Actions另后验。原+10/猜100、正文神恩/表恩惠、自己/玩家/单体/全体、三复活名/两等级、主要防具/仅限或全装备、复活建议/零忠诚满经验、气力耐久力原词/运行字段、同站概念/同构建继续分开。本地首轮父报告层级错误与反例锚点修正历史保持，非远端失败。R53有限包结束，最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-54回全22域；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部历史完整。

## 2026-10-21 R54大陆2003宠物加工与料理同期玩家指南边界

本轮以新读远端main 05f14965b3c87481f2dec104813f624e553b76e6/tree f3ddbc12795a7216f002175c3f6064ed28baae62 为基线；完整当前状态原Git blob、连续性协议及22域组合索引新核，R53主线最近可见11项Actions全SUCCESS、0开放PR。最高NEXT54轮换物品/合成/料理，未继续扩大R53回复法术、R52图鉴余图与暂停的R79。

2026-10-21实际查看两2003年新浪游戏网页可读正文：2003-04-15 22:14《石器初体验》标“网友投稿”(https://games.sina.com.cn/zhqu/sta/xsxl/sqcty.shtml)，2003-04-02 16:03《合成入门》署新浪游戏(https://games.sina.com.cn/zhqu/sta/wphc/wphc_1.shtml)。两页不是原始华义服务器规则、具体客户端build或台湾1.0；没有读取/锁存原始HTTP HTML字节或独立SHA，未重取原图，更没有原商业客户端执行。因此仅作同期来源受限文字结构化，不能借用R53真实双重放等级。

新增规格docs/specs/STONEAGE-CN2003-CRAFTING-GUIDES-SOURCE-R1.md与衍生research/recovered/STONEAGE-CN2003-CRAFTING-GUIDES-SOURCE-R1.json：S2原表18条装备类别/有序材料/列示百分比区间，原弓“木＋？＋丝”保持问号；S1七道新手料理、凯比特“加工”与乌力“料理”示例。关键源级矛盾：S2枪“石＋木”表列40–60%、投掷斧“木＋石”表列30–60%，S1木1/石1称枪；无序材料多重集重叠但**不能**证明服务器忽略顺序、确定产枪、随机双结果或指南成功率是原配置。加工/合成UI用词也不自动合并。原料后缀1/2/3不静默映射数量或等级，NPC/道具/技能ID未知。

候选分支agent/cn2003-crafting-guides-r54-20261021，新增本地派生元数据结构测试及专用Action；检查对象仅Git派生JSON的18+7项、未知位、重叠但不提升运行事实、来源级别，并不联网重取两原网页；原商业图片/二进制未入Git。候选/main Actions应以后验实际结果为准，严禁把提交前检验预先称通过。有限止点两页25项，不扩配方全站、数值公式及后代执行。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-55回全22域另取材料；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，全部旧历史前缀必须保留。


## 2026-10-21 R54加工与料理派生源主线验收及永久收据

R54资料提交2dd1c7a28b8993bebaf141b32b4cd1d4e1a7377c/tree b3fb195f0638443abae575dffe61cdae47375f43，以原main 05f14965b3c87481f2dec104813f624e553b76e6为父；候选分支agent/cn2003-crafting-guides-r54-20261021的10项Actions全部completed/success，主线同SHA的11项Actions全部completed/success，主线通过非强制的fast-forward+expected HEAD安全更新。专用候选run39594725260/job119204095403和主线run39595001302/job119205009874实际日志均显示4项派生数据检查通过、零跳过；其余Actions是现存验证矩阵，不冒称新增网页/原游戏实测。历史原CURRENT-STATE/TIMELINE/ROADMAP/SOURCE-REGISTRY旧Git内容均在R54提交中逐字前缀保留。

本轮另外永久保存research/recovered/STONEAGE-CN2003-CRAFTING-GUIDES-ACCEPTANCE-R1.json，将原派生数据Git blob bb33249f20713199afc488dbf1eee2d9b42907e5、候选/主线运行及工作单元ID、执行范围、原网页字节证据欠缺与非原服事实限制相联。专用回归测试新增必须存在的收据与原派生blob SHA1一致性门，原专用workflow增加收据路径触发；收据提交自身Actions需独立后验，不沿用旧4项绿灯。原始HTML SHA256和独立原客户端执行仍无，永不把派生绿灯提升为原服成功率。R54 25项指南材料有限包结束，下一最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-55轮换22域另取源；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，历史记录不覆盖。

## 2026-10-21 R55早期贝壳送物任务、获取路线与波拉岛入口归属

本轮启动时重新读main 8a0cd2d7f3de81737349250bd042692b07bcc866/tree 0f727a4eadc9c3f6cc48f38f48b81787117515f7，R54上一轮状态及主线验收已保存，最新同HEAD 11项可见Actions全部success/0开放PR，原CURRENT-STATE精确Git blob完整读取。按22域轮换至quest/story/worldline，最高NEXT55，不再重复R54宠物加工或扩R53回复法术。

三同期来源的网页可读正文于2026-10-21核对：2001-12-10 17173《归纳拿不可思议的贝壳的5种方法》署名诗雨玩家投稿；2003-05-29 10:15 新浪《弥生与日美子的友谊》标网友投稿；2003-06-04 18:40 新浪《英雄岛前传》署新浪游戏。未取得原HTTP/HTML字节、源SHA、精确客户端build、原华义服务器脚本或实机运行，不能冒称R53级别的来源双重放。旧2001来源第五条坐标和恐龙名显示损坏原文，保持未解析，不校正。

限定规格docs/specs/STONEAGE-CN2001-2003-SHELL-QUEST-SOURCE-R1.md、衍生research/recovered/STONEAGE-CN2001-2003-SHELL-QUEST-SOURCE-R1.json：2003双方出生地双任务路线Q_A萨姆吉尔/卡鲁它那→日美子送花给弥生→贝壳，Q_B玛丽娜丝/加加→弥生送贝壳给日美子→花；日美子两段局部坐标(56,124)/(57,124)不能自动合并，二村世界坐标不可当NPC局部坐标。2001玩家稿五条贝壳途径只是作者枚举，不当全局穷举：北岛送物、哥亚山/卡鲁它村商人、吉鲁岛小猪爱情、美鲁娜洞窟1000Stone购买、英雄岛饥饿村民食材交换。

**关键新增矛盾**：2001报告弥生→日美子送贝壳得到贝壳，2003同一方向却是贝壳换花。两者分源保留，不擅推版本改动或作者错误。2003说明贝壳宠邮受限、丢地消失、花送贝壳重作损魅力一点；只有玩家指南陈述，非原服道具过滤/忠诚或存档逻辑。2003英雄岛前传说背包持贝壳与萨姆吉尔村黑乌力(71,49)对话进“五十年前的波拉岛”；其80级要求/建议120属于英雄岛前传任务，不上升为传送门自身80级门槛；贝壳是否消耗、服务端时间线与首次原版存在均UNKNOWN。来源只作为未来世界观可选参考，不执行新石器设计。

另有专用衍生记录结构测试/CI，守三个源、双路线、两篇冲突、五条2001作者枚举、文本损坏位置和入口等级限制；CI不能证明HTML源字节与游戏运行。有限止点三页及派生记录，不递归英雄岛全部后续怪/奖励；下一NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-56，从22域另选。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED，全部旧历史前缀必须保留。候选/主线验收以真实Actions后验为准，不能在提交前预先称绿。

## 2026-10-21 R55候选/主线CI真实验收及永久派生收据

内容提交6eada4a406b0d1709b29ad9bb1b0e858b9fe87da/tree085b0d587bcd390ee952591cefcc6756fb7d4ac1已从R54 main8a0cd2d7f3de81737349250bd042692b07bcc866非强制fast-forward、带expected HEAD写入主线。9文件差异是5新增、4历史文件仅追加，Git原有行无删除。候选agent/cn2001-2003-shell-quest-r55-20261021同SHA 10项Actions全completed/success；来源候选专用run39599917007/job119221512082，日志4项派生结构测试成功、零跳过。main同SHA 11项Actions全completed/success；主线专用run39600076749/job119222049029，作业亦success。两run均没有生成/上传ZIP artifact，不捏造artifact ID、ZIP哈希或双次源HTML实时重放。

唯一持久衍生报告research/recovered/STONEAGE-CN2001-2003-SHELL-QUEST-SOURCE-R1.json为原生Git blob7157f1aca0e4f806334bb4892d294d93d106690d、UTF8 7762B、SHA256 411cd1fb8bec4c08e5ac78fa8987fb58f0cd7ee55c41397cbfcc9d0163e91d5f；永久验收收据research/recovered/STONEAGE-CN2001-2003-SHELL-QUEST-ACCEPTANCE-R1.json记候选/main run/job、内容SHA、原来源三URL、正反证据边界及缺失HTTP原字节/原游戏实测。新增收据必须存在+源派生SHA256强制测试，原4项升级为5项后的**收据自身候选/main Actions待后验**，不把早前4项成功写成5项。新工件仅为版权所有无争议的衍生元数据；未取得或存储原网页全文/图片/客户端、构建配置、服务器剧情脚本。

2001弥生→日美子给贝壳/2003同方向给花之矛盾仍OPEN，五途径不是完全集合，2003后续任务80级不是已证黑乌力传送门槛。R55历史材料包完成，下一最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-56回22域轮换；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停。所有过去报告内容保留。


## 2026-10-21 R56宠物技能训练收费、地点与不同网页版本口径

启动新核main 3380fddae94ca94967cb174491a38e8d62f9f552/tree df96f101780232c8aeb693798d0b50ba502ad51d，R55贝壳两提交已整合主线并有永久收据；同HEAD最近可见11项Actions全SUCCESS且0开放PR。最高NEXT56依据22域轮换pet skills / trainer economy，不扩R55英雄岛剧情、R54合成或R79本地存档。

查看新浪2004-02-23 15:24《宠物相关》https://games.sina.com.cn/zhqu/sta/xsxl/cwxg.shtml 和新浪未见可靠文章刊日《宠物资料》https://games.sina.com.cn/zhqu/sta/cwzl/chongwu01.shtml，后者©2006页脚不得当文章发表日。两页均属门户网页文字，不能认证同一个客户端build或初代官方配置。无完整HTML原字节/原SHA、图片下载、原服务端配置或商业原客户端执行；只作可读网页的文献限定派生。

新docs/specs/STONEAGE-CN2004-PET-SKILL-TRAINER-SOURCE-R1.md和research/recovered/STONEAGE-CN2004-PET-SKILL-TRAINER-SOURCE-R1.json：S1可见19行宠物技能名／页面效果／学习地点／列示价格（保留地球一周2399、达那防御例外），S2有界挑11条供语义冲突和后代技能补充。特别保留S1猛毒攻击攻-30%／3回合／4400与S2攻-50%／5回合／4000；一击必杀3倍含模糊“容易被击中”与S2 2.5倍／命中-30%；骑宠课程S1四级与S2下中上三级；旅途／旅程伙伴敌人一人／敌宠一只及学技两村／SBC。不能用S2未定刊期猜改版顺序，不能合并成确定性游戏公式、统一NPC或价格表。

S2宠物邮件笼统称某些落地消失特殊物品不可邮，不具名R55贝壳，故不能当贝壳实际禁邮第二条独立证据。S1忠诚约70/20/10的失控描述仍只是指南，非原服务端阈值；S2九大家族与五转机暴不回填TW1.0。专用派生元数据结构测试/CI只验证19+11行、5组矛盾与版本缺证负边界，不是HTML源双重放或技能实测。候选/main的Actions要按实际结果后验，不预报全绿。本包两页30条有限止点，下一NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-57轮换22域另取，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79继续暂停；旧历史完整保留。


## 2026-10-21 R56技能表候选/主线实跑验收与永久派生收据

内容提交83c8c8279cd5913d9c75eec467c64a965c8cfba1/tree674511414043d78f29b53317d093cac3703a121a由R55主线3380fddae94ca94967cb174491a38e8d62f9f552非强制fast-forward、带expected HEAD写入main；Git compare显示9变动：5新增、4历史文件仅追加/旧行删除0。候选agent/cn2004-pet-skill-trainer-r56-20261021共10个Actions均SUCCESS，主线同内容HEAD共11个Actions均SUCCESS。候选专用run39603382601/job119233280942、主线专用run39603519751/job119233745574各真实执行5项衍生字段/来源边界测试成功、零跳过。双方专用run查得artifact数量均0，不虚构ZIP或初代原客户端重放。

衍生研究research/recovered/STONEAGE-CN2004-PET-SKILL-TRAINER-SOURCE-R1.json原生Git blob b6f42811c23cadc8b80fabb0a53b98a6aa9e8b2f，UTF8长度14778B、派生SHA256 90bc79a7c824ffae88f2e974de692252fb37345eacafa9db26f87bb62bbc9a70，19条S1完整可见学技行＋11条S2对照及5组来源矛盾永久存在Git。新增research/recovered/STONEAGE-CN2004-PET-SKILL-TRAINER-ACCEPTANCE-R1.json记录内容提交/双工作流job/两URL/缺失原HTML与实机证据；测试增加必须存在收据及SHA256原字节逐验门，专用workflow添加收据路径触发。收据**自身提交**的5→6测试与候选/main Actions须完成后另后验，不沿用旧5项绿灯。

2004《宠物相关》与S2未定刊期《宠物资料》同名技能冲突仍不认证任何patch顺序；猛毒攻击效果/费用、一击必杀乘数、骑乘课程3/4级、旅程伙伴对象及训练地分开；宠邮泛指特殊物品不认证R55贝壳过滤器。无原网页HTML SHA/精确build/技能或NPC ID/商业原服测试。本包有限闭合，最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-57回22域另取重要材料；Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停，历史全部前缀保留。


### 2026-10-21 R56永久收据首轮测试路径错误与修复（不改写历史）

首次收据候选7f5dbb1291891ffd27d700d849b9e51ce8038850专用Action run39604156414/job119235960504实际**FAILURE**。本轮静态预检发现测试将派生JSON所在的research/recovered目录作为根，再拼一次research/recovered，导致收据查找路径重复；与网页内容、来源真实性、Git SHA256或客户端规则无关。非强制提交b4f823f1c418b0569a7c938a7dfa99af6a212351仅改测试的仓库根路径为P.parents[2]，对应专用run39604294631同HEAD SUCCESS，首轮失败不称SUCCESS也不从记录中删除。此前来源内容提交83c8c8279cd5913d9c75eec467c64a965c8cfba1的main11项Actions独立全SUCCESS。下一次完整候选/主线Actions将按最终HEAD后验；最高NEXT57不变。


## 2026-10-21 R57 2003年操作、组队交易与原地登出的来源限定取证

新读取main 4e11dc8983cfbe0b1b667e5ee45a3b1ee4a4de6d/tree 5d991edadd52c12dd484dd4c689dc1be6e8127c4、连续性九文件与22域索引，R56候选失败修复历史保留。R57有限审查新浪2003-04-15 23:29网友投稿《游戏操作》（正文多次命名《海贼王遗迹》）及2003-11-18 15:33新浪转述华义《增开服务器组》消息（明确2.0怀旧服）。逐条归档S1指南20项游戏操作与S2公告3项。S1含移动/朝向、面向NPC文字对话、告示牌、背包满/拖地、下7窗/上8键、队长带队、面对对象组队YES、双方交易YES/OK、HELP五人描述、决斗、13动作、原地登出、宠物模式与战斗指令等待等；S2提2003-09-04 2.0服务器组开放、2003-11-19新组及“更安全交易”。两网页都未取得原始HTTP/HTML字节哈希或原商业客户端/服务端执行。

**四项负边界：** (1) S1同页Ctrl+I“所持道具”与Ctrl+L“道具视窗关闭”矛盾并存；(2) S1海贼王遗迹与S2 2003年2.0怀旧服不能合并同build，2003-09-04不是2.0最初发行；(3) 两人OK与“更安全交易”没有服务端原子事务映射；(4) 原地登出／记录点仅网页说明，不证明原TW1.0 savedata字段或商业服务器状态。S1这些操作也不回填初代实机、UI像素、NPC/交易/战斗配置。

新增docs/specs/STONEAGE-CN2003-UI-TEAM-TRADE-SOURCE-R1.md、research/recovered/STONEAGE-CN2003-UI-TEAM-TRADE-SOURCE-R1.json、R57审查页、专用6项派生元数据测试及workflow。来源是2003年具名网页阅读，不冒称原始页面双重放或真实版本运行。研究/候选和main Actions未经验收不得宣称通过；永久派生保管收据应在后验另写。止于两页23个记录；最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-58，Stage A7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，历史旧文本逐字保留。


### 2026-10-21 R57内容提交及双端CI后验，永久派生保管

R57研究提交 72d5dceb03900c7f80a143201bddc11caeb1121d/tree 2a04834f9b930d1716a2b9ca7f6769fc1fdf19b4 从原main4e11dc8983cfbe0b1b667e5ee45a3b1ee4a4de6d建立，仅前进提交；GitHub compare实证9文件、5新增、4只追加、旧历史行删除0。候选分支agent/cn2003-ui-team-trade-r57-20261021该HEAD十项Actions均completed/success；专用run39608021253/job119249213662实际运行6个结构化数据与证据边界测试，零跳过。主线同HEAD十一项Actions均completed/success；专用run39608219457/job119249911845亦success。专用两run均查0 artifact，不捏造ZIP或源HTML独立双重放。

research/recovered/STONEAGE-CN2003-UI-TEAM-TRADE-SOURCE-R1.json源派生Git blob1bac3104c1d6b0d96a65a8c32e901de13a5df53d/UTF8 9904B/SHA256 ef9ee96f478aa9232b1cbb9fb71716ed36302f04dfa885c3cd0eaab29d4d82dd。新增research/recovered/STONEAGE-CN2003-UI-TEAM-TRADE-ACCEPTANCE-R1.json永久收据记录内容提交、双Actions、两个同期网页的来源URL、零artifact、未取得原网页原字节与商业服务端实测。专用CI由6升级至7项，新增收据存在、派生原字节长度和SHA256验收门；收据提交自身的候选/main Actions须另行后验，绝不可把旧6项结果称7项运行。无版权原始HTML/资产入Git。保留快捷键内部矛盾、海贼王遗迹vs2003的2.0怀旧组分期、交易OKvs“更安全”机制未证和原地登出不等于TW10 save原数据。最高NEXT58，Stage A7 PARTIAL+2 OPEN，B/wiki GATED，R79暂停，旧历史全文不改删。


## 2026-10-21 R58 2002年4.0任务前提与机械文明故事线资料（有限归档）

按本轮新读远端main `b94270a19e4ce5d73691e8201d00a03bcf6c8177`/tree `882a4a1c51d507666a0751f0028330507b15a7f6` 与R57实际双端验收继续；从世界/NPC/任务域提取真实游戏内容与世界关系而非空转底层helper。本包审查17173两篇同期玩家文：2002-09-16微笑赢家《石器4.0终极总结》与2002-12-17页面署康志强《石器の机械文明流动攻略》（正文另见不同署名，作者未独立确认）。S1归档12个4.0具名前置条件，S2归档8个精灵王—天空之岛—元素之石—精灵之岛—失踪孩童/动物园剧情节点，均仅“网页指南主张”，并非原服务器任务/奖励脚本。

重大发现与证据边界：天空岛30级+成人礼可接，不得把建议80级/四大洞变为硬门槛；黑虎原91级且金飞与作者所称现101级完成不得合并；里拉拉作者自述4.0前后宠转条件改变但无官方补丁直接证明；2002两页不证同版；同名不可思议的贝壳与R55 2001/2003记录仅作跨文献名称关联，不能当原服同一个道具ID或同时成立的任务条件。S2五转与特殊宠物不回填初代。页面可读文字已核，但原始HTTP HTML SHA、原客户端/原运营服务器实跑均无；版权源/图未入Git。

新增 `docs/specs/STONEAGE-CN2002-QUEST-WORLDLINE-SOURCE-R1.md`、`research/recovered/STONEAGE-CN2002-QUEST-WORLDLINE-SOURCE-R1.json`、R58审查说明、6项结构测试及CI工作流；严格限定二页12+8行和6个歧义。研究/主线Actions及永久派生保管后验，不提前宣称成功。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-59，Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED，历史所有旧记录逐字保留。


### 2026-10-21 R58双端CI完整验收及永久派生来源收据

源研究提交`dd30db0dfc5a3d58706c3220ea8d333aa37ba5cb`/tree `c31abd5cf0bb2c885ff4b99493d6eb6c2e5780ba`，主线由b94270a19e4ce5d73691e8201d00a03bcf6c8177非强制且预期HEAD保护快进。GitHub compare=8变动：5新增、3历史文件仅追加、原历史行删除0。候选agent/cn2002-quest-worldline-r58-20261021同源HEAD实际10项Actions全部completed/success；专用run39612028005/job119263072244日志执行6项派生源/前置条件负边界用例，全部通过零跳过。main同源HEAD实际11项Actions全部completed/success；专用run39612246843/job119263842866 SUCCESS。两专用run各0 artifact，绝不虚称ZIP、raw原HTML SHA或原商业客户端、服务器双重放。

源派生研究 `research/recovered/STONEAGE-CN2002-QUEST-WORLDLINE-SOURCE-R1.json` 原生Git blob5026707c16e0fdc306daf188739dcd75cb79b8b5/UTF8 12868B/SHA256 58b6c1f986e0b0b30ce45cedccfce47395d95b23b905f33da7a4eafb6e909183。新增 `research/recovered/STONEAGE-CN2002-QUEST-WORLDLINE-ACCEPTANCE-R1.json` 永久保管上述内容Git、两个实际source页面URL/刊期与双工作流ID、原始HTTP字节缺证及六项负边界。原网页作者文章/截图/客户端不进Git；结构化源12任务+8故事+6矛盾并不认证官方4.0补丁、同版任务ID或TW1.0内容。新专用测试由6升7项，强制收据必须存在、源原UTF8字节长度与SHA256一致；收据提交自身候选/main Actions必须独立后验，不能将旧6项成功改称新7项通过。下一最高NEXT59；Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停。历史前缀保留。


## 2026-10-21 R59：2003 年 7.0 职业系统和技能门槛（门户网页，不是运行证据）

【SOURCE FACT】新浪游戏 2003-11-19《全新开放的职业系统》和《石器7.0各职业技能表》保留了同期三职业与可见技能、三共通技能及九项明确举例前置条件。S1 陈述就职初始一点技能点、职业升一级增一点、最多16点、学习不可撤销及熟练度示例。两页不是同 build 运营原配置；精确发行时间/服务端执行、TW1.0 成员资格均 OPEN。详见 docs/specs/STONEAGE-CN2003-PROFESSION-DEPENDENCIES-SOURCE-R1.md 和 research/recovered/STONEAGE-CN2003-PROFESSION-DEPENDENCIES-SOURCE-R1.json。

【CONFLICT】一针见血/针针相对、驯服/驯伏、招雷/召雷、以形/移形保持源字面。尸体掠夺职位级别5独立于一般二级门槛。S1/S2列表计数差异不推服务端更新。不得用此项为现代新游戏设定职阶或熟练度公式。

### 2003-04-15 — village / record-point / transport player guides (R60)

**FACT (publication):** Three Sina game portal pages, attributed as reader submissions, display 2003-04-15 times 21:54, 22:14 and 22:43 and discuss earning Stone, village services/record offerings and transportation. Source registry: SRC-CN-2003-SINA-VILLAGE-TRAVEL-R60.

**SOURCE CLAIM, NOT SERVER FACT:** The 22:14 village guide and 22:43 travel guide disagree on named meat quantities at 玛丽那丝渔村 (1/2), 柯奥村 (2/1) and 卡鲁它那村 (1/2); 奇喀喀村 is unknown in S2. Distinct coordinate frames are not matched. Reported bus/air/feather/undersea fares remain player-guide values.

**OPEN:** Actual build(s), first-party source, earliest-version membership, NPC trigger/price/record-point consumption, player persistence and transport map remain unattested. The S2 hero-island age/level narrative does not resolve R55's portal-vs-quest requirement boundary.


### 2003-04-15页面标签／2026-10-22复核：家族形成与庄园服务

**FACT（文献存在及其陈述）**：新浪《游戏操作》网友稿分述申请、三日十人成立、成员/族长退出差异，以及守护兽、光暗精灵、庄园医生和银行。**OPEN**：同页四家族、九庄园、前二十名资格的适用范围；精灵影响方向、声望门槛、计时和原服事务。文中海贼王遗迹标签不能证明各段同build；不是台湾1.0或JSS1999规则。与R57为同一网页，不重复计独立来源。来源与派生见 STONEAGE-CN2003-FAMILY-LIFECYCLE-SOURCE-R1。


### 2.0标签、首刊未定／2026-10-22复核：渔村捕宠委托与地点

**FACT（文献陈述）**：新浪《新鲜速递(三)》两段正文给六份渔村宠物委托及目标出没地、购买/交付角色。**OPEN**：首刊日、原作者、同build、F奖励、保证金退款、坐标框架与真实刷怪表。URL0110与2004页脚不能确定文章日期；19名称/21关系不认证初代物种ID或TW1.0配置。源派生见STONEAGE-CN20-PET-COMMISSION-HABITATS-SOURCE-R1。


### 2003-12-12图集标签／2026-10-22复核：开发中战斗和野外参考

**FACT（出版物及当前图像）**：4Gamer相关公告和图集标2003年12月12日，图库明确开发中；本包当前取得前两张原JPEG并目视战斗目标提示／野外HUD。**OPEN**：真实截图拍摄日、2003当日是否同字节、商业build、物种/NPC/地图ID、指令行为与原生分辨率。640×480仅当前网页图像尺寸，近40张不作核验分母。见STONEAGE-JP2003-BATTLE-FIELD-VISUAL-SOURCE-R1；不回填TW1.0或关闭原音效绑定。


## 2026-10-22 R64：恐龙博士的具名NPC、捕宠培育与分源奖励

新核远端main `099a196d44c5e34b382c31b912962ac94c158ca4`/tree `b352da6dbf506929ccf324484f16d89998cb280c`、458分支、0开放PR、0运行中Actions，同HEAD main9/候选8项实际SUCCESS；旧queued37642417333无关。完整CURRENT 2309305B及九启动原字节/原生Git身份已核，最新NEXT64选早期具名任务域，不继续上一包日本图库或R79。

本包三份当前HTML：既有新浪汇编入口及真实c2#17、2003-05-29 11:37标网友投稿的《恐龙博士》。HTTP200，37893/36563/52445B与SHA256完整记入research/recovered/STONEAGE-EARLY-DINOSAUR-QUEST-SOURCE-R1.json；旧汇编页是已知网页的新选定节结构化，不重复计新独立来源。早期目录2001-01-18、当前页2004-01-06发布注释、S2的2003时间和2026原字节各自保留，无历史同刻/精确build认证。GB18030替换1/2/0，选定业务段全无替换。

新增中文规格docs/specs/STONEAGE-EARLY-DINOSAUR-QUEST-SOURCE-R1.md、R64审查、有限工具与源重放workflow。S1/S2各两段任务＋S2哈鲁/助手吉鲁共六文献归档关系，原ID均null。鲁尼贴斯/鲁尼帖斯、阿西美加/阿西美拉护符1和18档护符说法分源，不能据此称确定改版；S2玩家15/25仅建议，宠物15以上/30另字段，S1布克布克LV1不回填S2。博士与同名治疗精灵哈鲁不合并，入口328,633与研究所11,12不混层。取走多宠/骑乘宠警示不证选槽/实际消费/事件或存档，原始NPC/物种/任务ID仍未知。原HTML/图像/程序不入Git。

本地六测试和12真实输入语义反例＋script正例通过；初检标题误判（前置条件重复名称）及引号跨段误抓已修复并保留过程，未发生对应远端失败。实际候选/main重放、ZIP下载和永久派生保管须另后验，不预报绿。有限止于两任务三HTML，最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-65` 回22域另一材料域，优先可归属音效事件或官方地图/生态；Stage A7 PARTIAL+2 OPEN，B/wiki GATED，R79 PAUSED_NON_BLOCKING，全部旧历史原字节前缀保留。


### 2004-09-17报道／2026-10-22复核：日服封印地域与宠物操作

**FACT（同期媒体陈述）**：4Gamer署Asakura报道称第三弹更新新增两个具名区域，含东侧封印洞窟、沉没穀嶺之地和未名恐龙提示；并述自拾取展示、原地放生及一次一只宠邮。**OPEN**：具体运营构建/原服部署/地图ID与路径/物种、参照岛身份、售款或删除/计时/持久化。7月既有未名地图及2006群岛不自动合并，来源和时间见STONEAGE-JP2004-SEALED-REGION-SOURCE-R1，旧历史保留。


### 2026-10-22 R66工具文献分层归档

新增STA2.53相关玩家文献的版本/发言归属与beta试用边界；见 docs/specs/STONEAGE-STA253-SPEAKER-SOURCE-R1.md。页面发表时间不当软件发布日期，未认证具体官方游戏build或运行；不据冲突编造确定补丁演化。


### 2026-10-22 R67分源料理文献关系

新增有限料理效果与使用场景关系，见docs/specs/STONEAGE-COOKING-EFFECT-SOURCE-R1.md。网页的刊时、模块发布注记和当前取得时间不是确定产品更新时间；未认证原服配方或同build身份，不据同名差异编造补丁演化。


### 2003-05-30页面标签／2026-10-22核验：沙姆岛梦幻洞窟

**文献FACT**：新浪网友攻略给昼夜入口与成人完成后的三次具名装备、以后随机奖励，并说明非成人随机。**OPEN**：原始商业build/地区、任务与地图ID、三村坐标含义、两路线的昼夜归属、随机池与存档。开篇航空安全是传说推测；年度供物与守门者的视角转折按同文关系记录，不写成确定补丁演化。见STONEAGE-CN2003-DREAM-CAVE-SOURCE-R1。


### 2005-09-06发布文标签／2026-10-22核验：日服寻宝两阶段活动

**SOURCE FACT**：4Gamer刊载GaiaX寻宝活动说明，给サムギルの村光の精霊の使徒与3/2种分期收集、第二阶段兑奖、物品转交及重复挑战。**OPEN**：原build/部署、数量/概率/奖品、持久化。媒体导语9月13日金与运营引文火有字面差异，未得官方勘误；原站档案请求429不证明原文不存在。与2008协力仅作源限定机制比较，不建立确定历史演化。详STONEAGE-JP2005-TREASURE-EVENT-SOURCE-R1。


### 3.0专题标签及2003-05-01转引／2026-10-22核验：特殊宠物技能

**SOURCE FACT**：现存专题与玩家转引给七技能的特殊宠资格、捐献状态和原名异文；S1另述GP落马至回合结束的原坐骑限制。**OPEN**：专题首刊、未名杂志、官方同版配置、原ID与执行。作者自述5.0起玩不能作3.0亲历；共同80例和措辞不证明独立佐证或抄袭谱系。见STONEAGE-CN30-SPECIAL-PET-SKILLS-SOURCE-R1，不覆写R56或TW1.0事实。

R70同包定年补证：已真实取得2003-03-24 22:11:24的精确S1历史捕获，所选完整可见文本与现页相同，支持当时已有这些技能/落马文字；不当3.0首发日期、原作者或原服执行。初始查询阶段未取得历史正文的状态由本补证取代。


## 2026-10-22补证：2003五兄弟任务答题与选择奖励

新浪可见2003-06-02 14:22刊时与实际2003-12-04 05:15:08历史捕获分开；当前/历史正文核心全等，捕获不认证首刊或原服执行。新规格补五层答案键、两次对话/水晶通行、战斗中HELP、五成对选择奖励与两地图生态。名称异文、转生重复机制、离开世界/注销/掉线、原ID与同构建全部保留源层或未知。旧早期指南未被覆盖。详docs/specs/STONEAGE-CN2003-FIVE-BROTHERS-SOURCE-R1.md；不据此回填1999/TW1.0服务器。


## 2026-10-22补证：2009日本コクエン限售与成形/重抽兑换

DigiPark发布文可见2009-06-29，所述黑炎袋售期06-23维护后至07-21维护前，站点改版06-25另记。随机袋6类、三类混合总10与两次5票升级；生成回复物的注销/丢弃消失不推广全部物品。原图仅一随机状态展示，不作物种固定初值。详docs/specs/STONEAGE-JP2009-KOKUEN-SOURCE-R1.md；白炎旧异文、原ID/实服/2009原始字节和模型未知未关闭，不回填早期版本。


## 2026-10-22补证：2003琉璃洞窟的宿身叙事和可选分支

可见2003-06-06 14:55刊时与2003-12-04 05:15:40真实捕获分开，当前/历史整篇核心相等但不认证相同HTML原字节。故事区分父亲的死亡说法与后续女神宿身解释、尚未发生的家庭重聚；14年日记/50年宿身轮换不当真实人物年龄或运行计时。主线转生前提与可选随机袋支线分开，成人条件不从另一洞窟奖励规则类推。详docs/specs/STONEAGE-CN2003-LIULI-CAVE-SOURCE-R1.md；初代归属/原脚本/真实持久化均未证。


## 2026-10-22 R74历史材料增补：日本2005市场与公告服务

FACT（同期媒体报道层）：4Gamer2005-06-03文预告GaiaX日本线6月14日将水星聊天地图改市场，官方ニースフリーマーケット6月18日18–20时，GM巡场聊天合照建议。2005-10-21文回述六月举办受欢迎、列第2回11月19日18–22时；回述不当独立服务器执行证据。每月两次官网用户活动公告，本次10月20–25日招募11月1–15日举办的活动，计划10月28日刊登；付费会员且经营粉丝站或Blog只约束公告申请人，不是市场参加资格。三实际原图均人物插画，不恢复地图/UI。

OPEN：精确build/原ID、地图几何入口、市场入场条件、税费/结算/自动摊位、实际刊登及运行保存；2026当前页不认证2005历史字节，现代免费页脚不倒灌付费年代。与JSS2001共享房间、CN2011–12摆摊保持来源/版本隔离。无新游戏采用决策。见R74规格、SOURCE JSON及后续真实CI保管；Stage A/B/wiki状态不变。


## 2026-10-22 R75历史交通增补

FACT（运营商具名宣传刊文层）：新浪2011-12-19 11:08文述长毛象公车找站选线、面向点击加入队伍，普通聊天频道小写go提前发车，退出团队可中途下车。两原链接配图实际为有工具栏、候车空间、长毛象、人物/站牌的静态游戏场景；第二图目标标签可辨萨姆吉尔与玛丽那丝，未证方向边或已完成乘车。

OPEN：文尾8.5/2.5双服务器宣传无法认证具体公车build；车费/容量/常规等待/遇敌/路线/原ID/权限/命令处理及保存未证。JSS2001手册3分钟/4人、CN2003玩家稿20–30石币不倒填2011；旧稿go属航空。第三壁纸未取，当前字节不认证2011历史。无新游戏采用决策，见R75规格及SOURCE/后续真实保管，Stage状态不变。


R75验收前措辞收紧：首候选eca552d814b87f42536175d435dfc699077b22a9的“面向”/FACE_MAMMOTH过强；原文仅“在长毛象面前”，现改为STAND_IN_FRONT_OF_MAMMOTH（站在公车面前），不证明人物朝向检查或方向标志。原候选、六单元工件及其Git历史保留，新内容提交需重新实取验收，不能借前稿绿灯。本次不是源正文或图片变化。


## 2026-10-22 R76官方手游当前人物参考（非PC历史补写）

FACT（第一方当前官网层）：Netmarble日语《ストーンエイジ：放置冒険》默认人物页具名ウッディ，背景称居住サムギル村、保留三性格词，随冒险逐渐显出勇敢与正义感。两相同name标签计一角色；实际相连原PNG为静态全身立绘，不是游戏模型/精灵或动画。观察日2026-10-22，不当原发布日期；CDN目录/关键词年份不认证build/上线时间。

OPEN：本手游精确build、原ID、战斗数值/技能、出生点/剧情触发与可玩动作均未得；不将名字/图像回填2003 Hangame无固定人名的PC12位置，不宣称同一世界线或官方retcon。后期独立手游资料进入隔离参考库，无新游戏采用决策；原HTML/PNG不入Git，见R76规格与SOURCE，Stage状态不变。


## 2026-10-22 R77：小水怪攻略的城市受损与亲代救援叙事

FACT（来源限定攻略描述）：标2003-06-03的新浪文述尼克斯受损、动物园掳幼兽导致水怪报复、还子后和解；A先战水怪再查动物园，B先查动物园救幼兽再还子。两线共同尤里蛙，B另双头叉+75攻/-25敏/滋润Lv5及未量化维修后时机。建议105非已证硬准入，贝壳是听懂动物而非已证入口钥匙；巴克战禁组队不扩整任务。幼兽莫拉司/斯异文、被救幼兽与奖励蛙分开；食物叙事不当捕食AI。

OPEN：单次Availability仅得20160929133108实际捕获，不能认证2003原始字节/官方原稿/build；同一文两包装正文一致不当独立见证，当前两配图不认证历史拍摄。配额/刷新秒数/重解/消耗/HELP/原ID/可捕名录/真实保存未得。旧琉璃家庭、早期贝壳ID不合并，无新游戏采用决策；见R77规格/SOURCE，Stage门禁保持。


## 2007-07-30 — 日本PC运营文的限时商城宠物相对率（2026-10-23核）

FACT_SOURCE_REPORTED：4Gamer刊UTD原文发布文称黒檀のくじ7月27日起售，7月30日18:00至31日13:00两具名宠ギガドラン/ドルーザス出现率各2倍，余四种略降，31日13:00亦售卖结束。1000GStone为商城价格标签，非Stone/GASH；年按刊年关联、时区未写。公告不证实服部署；绝对率/完整奖池/原ID与两插画左右名字未知，不倒填初代/野外遭遇表。详细来源与边界见docs/specs/STONEAGE-JP2007-EBONY-LOTTERY-SOURCE-R1.md；当前HTML与图像字节非认证2007原始数据。


## 2001-12存档 — 大陆运营站操作说明与分时名片配图（2026-10-23核）

FACT_SOURCE_REPORTED：12/4捕获的华义2.0操作页描述五宠物模式、已学骑乘并选择可骑宠的显示条件、四庄园族长邀请函与对应庄园骑宠学习文书权限；22章全文结构化不是首次上线日期/具体build。真实附图实际12/27捕获且去www，呈现名片窗口与四个可视条目、Online/Offline、Mail/Delete；不是四联系人总容量、网络状态/按钮实测或同版断言。两来源时间分别保存，详情docs/specs/STONEAGE-CN20-OPERATION-UI-SOURCE-R1.md。已有同页记录点/交易YES报告仍完整；新归属不向TW1.0/JSS1999或2003攻略条件互填。


### 2005-09-21／计划2005-10（日服PC）——2026-10-23 R80来源补记

FACT（报道存在/安排口径，非事件执行）：4Gamer/aueki20:23报道ガイアックス10月活动。10/4–11グルメマスターに挑戦！全服聊天室起步，全指定料理完成得石器時代フルコース；同窗两村便利店食材半价。10/8火星服昼课14–14:30ジャジャ村、水星服夜课20–20:30マリナス漁村，GM讲菜谱但本文无具体材料表。10/4–18官网秋川柳竞赛最优奖ガーヴィ“世界1匹”是宣传描述；佳作自制合成装备命名笔和增捕获率料理与任务全餐奖分开。10/29 21–22时全服GM多处派变身糖果等，标题仮称仍保留。年份从刊年/下月语境关联，无时区/精确build。

OPEN：角色NPC/GM控制、原任务/配方/物种ID、数量消费/重复、奖品公式持续、实例唯一性与实际履约。插图只是锅旁料理人物不认证具名宠物或NPC。同期报道不是明示原文发布文/已取得官网活动详情；现代页脚免费标签不倒填2005年9月。详见JP2005-AUTUMN-COOKING来源规格/SOURCE，当前HTTP字节和图元数据不当2005已认证原件；大陆料理类别或日服宝藏规则不得移植填空。


### 2003-05-29 17:00（页面标日）——2026-10-23 R81梦德洞窟来源补记

FACT（指南所述，不是商业服执行）：新浪/网友投稿梦德攻略连接卡坦、霍特尔失窃守护石与柯尔克朋友引导，荒漠盗贼部族、霍特尔不祥/卡坦祭典受阻，井口暗号“在卡坦有梦德”、最底层唐悟战后族长交石。归还卡坦再霍特尔后回柯尔克得最终黄色首饰，特别警告前二反序不获该首饰。铠甲防20敏-6/滋润Lv1、勾玉可换2000S、首饰魅5睡眠耐性30分别归属；可售价值非直接现金奖励，推荐60非硬门槛，成人仪式前置按文献记录。

OPEN：原作者/官方build/原IDs、具体楼层、盗物算法、奖励flags/重做/消费/真实发奖保存。世界/局部坐标和三村NPC出现分开，不以相同村姑称谓合身份。实际两JPEG只证当前道具说明画面，非认证2003像素或效果运行；2006页脚/现代专区标题不改源标日或认证1.82。早期柯尔克通路记录点与吉鲁岛贝洛恩生态不反填。本包正文当前HTTP字节与图摘要/规格见CN2003-MENGDE-CAVE-SOURCE-R1。


### 2002-09-13（GNN标日）／2019-08-20捕获——2026-10-23 R82补记

FACT（存档新闻口径，不是实服验证）：狼人平时人形、进入战斗画面才狼形，称月夜變身；报道9/15引狼入室包一宠/限发行一万，360WGS/4.0媒体/30万石币是包内容，不是售价。9/19魔法牌周边，预告萬事俱備包赠地魔兽赫拉克勒斯/火魔兽翟貝里恩，未认证实际发放/媒介；实体牌140张与骰子不作MMO机制。月夜名称不证月相/昼夜门，暴龙比喻/NO.1不供数字主表或独占历史断言。

OPEN：官方作者、原精确地区服/build/ID/成长/元素比例/施法逆转换/资源绑定、实际兑换与原图。台湾市场为新闻/WGS语境推断。当前GNN403未取正文，2019精确捕获不当2002原字节或首刊；当前三张120小图无具名图注，不按颜色合物种、不冒原模型或历史像素。详TW2002-WEREWOLF-FORMS来源规格/SOURCE，后期转载不改原月夜称谓。


## 2026-10-23 R83：强恩一族家庭选择、三口令与来源分域洞窟生态

按新远端main491d43c2b0aad5f9231da806205576f050a21825/tree66f6e049bc5aea45f07296e637024fcaeb5ffc1c启动，489分支/0开放PR/运行中Actions，旧queued37642417333继续单列不动。前轮最终候选10/main11实际completed/success。八启动文件完整UTF8/精确git show/原生Git一致，CURRENT2415368B/SHA256526c37ea41995311f5f4655e1bcda343a0daa5175a6714acc4ac408fb2362f1a，旧全文前缀保留，无AGENTS。读最高NEXT83/22域后转早期具名世界任务，不重开暂停savedataR79。查成人仪式已有规格保持关闭不重复计新成果；强恩/卡娜木笛未有独立规格，未采用现代私服主表。

交付STONEAGE-CN2003-QIANG-EN-FAMILY-SOURCE-CONTRACT-R1及SOURCE/工具/专用工作流。S1新浪《石器时代》任务功略-强恩一族，标2003-05-30 10:17/新浪游戏/网友投稿，无具名作者；https://games.sina.com.cn/zhqu/sta/article/2003-05-30/9898.shtml 当前200无跳转54963B/33b20cfa59c64834592247eb21aad0a457d5dfa65a0dd532f2a108280c3dc60f。S2南岛座标标2003-04-03 14:19，同门户/投稿，https://games.sina.com.cn/zhqu/sta/sqdt/sqdt_2.shtml 71509B/521512039fd1edefd36581e315a52b566f73b90f5673d0211557df6c80f3f727。严格GB18030零替换；非直取运营作者/认证2003原字节/精确build，两同站页不称独立见证或同版。S1业务2143字符/6135UTF8B/a88a3b5b2f3ef45664dd62b2d4f2c5d5f9b9860ad302bec9cf8d5ef165f6c1ee；S2只洞窟主行258字符/402UTF8B/5bc777ad65d017d71fcd1f0935a5d1c0f4097d6e9f0b4e65a200d35a05ca77e5，均独立去标签/实体归一逐字核对。

恢复凯伊（吉德的朋友58,66）给花→村长家深处吉德→未具名儿子给母亲发饰→沙拉→转告强恩女儿选择→给双亲的信回吉德→卡娜木笛的文献任务流。强恩68,7/妻70,8愿尊重女儿，沙拉选择留下养育家庭，不是强制护送回亲生父亲；母亲已亡/信名给双亲不冲掉叙事。16年前绑架、当时四岁、母亲两年后逝为所述相对时间，不推当下年龄/历法。卡那/卡娜、阿尔鲁山南侧/阿鲁姆山字串分别留，不强别名。村140,1007与124,1048不赋入口出口，50为建议、不补成人仪式或无任何前置；羽毛无只本指南栏。

洞口285,926，三层出口4F11,54红色月亮的光芒/5F51,5蓝色山脉即力量/6F8,23白色之风即速度逐层关联。四层以后随机伯恩/玛琼拉/卡鲁德可能掉盗贼秘密文件，明确直接说口令即可、不必有文件；七层固定三人联合战与随机遭遇分开，不补掉率/原实例ID/消费。强恩随机一道具，羽饰只是一次样例；吉德木笛魅+2毒+5石-5眠+5复活精灵Lv2，缩写不补免疫百分比/伤害/已发生效果。原任务flag/ID/重做重置/物品消费/服务器事件仍OPEN。

S1敌Lv31–48/六标签，S2Lv30–40/山贼、59.齐尔格尔顿、72.格鲁西斯分域存；59/72不当原宠ID，格尔顿不强合齐尔格尔顿。S2地上8楼/13条带方向层间坐标保留，不自动反向；S1只列1–7楼及沙拉房图未说共七楼，不宣称已证冲突或房间为8F。与R81北岛梦德仅正文文本关系，不合原阵营/前置/领奖序；琉璃家庭故事不挪入本篇。

20实际全图/缩略对只取009沙拉和012木笛。I1 87716B/5e57c456dd9b0cf648e91eca585f6958a704ef14643c2b1a08c01fa546f941e7、I2 116396B/68a756ea81d19f4cc63d006c2222defa04a8577832cf5ac05dc12ba2da8550d6，均200无跳转JPEG/RGB640×480单帧完整解码/目视。I1石屋床桌人物/沙拉标签，无选择对话；I2物品说明数值吻合且吉德标签，静态图不证明原NPC ID/发奖/效果/历史原像素，原HTML/JPEG不入Git，其余18图不取。

18完整文献目录（任务1、故事NPC6、口令守卫3、战斗组1、地图1、物品流4、屏幕2）七必填/19集合核验，非18原实体。三父报告/共享解析器原字节固定，34去全部指纹门语义改写、隐藏/正文外2+地图行外1反例、两外围script正例。首次本地修改生成后语义摘要校验报错，独立重算磁盘摘要一致后重新运行七单元/原输入回放通过；不抹除该本地失败，远端验收待后验。停止于两指南两图，重开须同版原脚本/ID/认证像素或实服交互证据。

最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-84转另一地区早期具名宠物/生态，或有同版实参的音效资料，避免连续大陆洞窟/helper扩张。Stage A7 PARTIAL+2 OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING，无整体百分比，历史旧全文不删。


### R83双端实源验收与永久派生保管（2026-10-23）

内容64553597373015c99b90c1d2953b31230d3e835b/treec82760bc9c68e592b6099568198bfe9196a69d2d，候选10/main11实际completed/success。九文件原生Git blob及整tree逐一一致，四连续性旧全文前缀完整；新读main旧HEAD后expected_sha非强制快进。专用候选run39902606043/job120247332480/artifact12479626746，主线run39902723105/job120247695519/artifact12479800876，实际日志各七单元、两HTTP正文/两全JPEG实取解码、34去全部指纹门语义改写、隐藏/正文外2+地图行外1反例及两外围script正例通过。

两ZIP各6599B，SHA2563ddcef8c9ca7d5d3b5240a3169f3355e50692af8714c98dc2bc0c5e33561e634 / 1e3812f798ab2f32549a95287ea520b77f56cd935bb48c77b3f9b49d94da51bc分别符合API。唯一replay.json各43717B/SHA25693907315f3d9a34af6899f1a240fc379861486f1c098c09b6fa22d12747a83d8，候选/main/local/保管门后local四份逐字节相等，四实际HTTP输入摘要均同初取；这不认证2003原文/原像素、同build或两独立作者。

双原CI JSON与STONEAGE-CN2003-QIANG-EN-FAMILY-CUSTODY-R1.json永久入Git。七pin固定SOURCE、三父报告、共享解析器和双原报告原字节/SHA256/Git blob。收据保存21真实run、准确双run/job/artifact、ZIP与raw/input初取历史。CLI强制保管，固定完整run清单摘要、实际run/job/artifact和ZIP长度/摘要，拒绝缺失/同长篡改、错HEAD/tree/分支/任务/ID、门遗漏重复或成功门替换、工件复用、虚报输入相等及抬高历史/官方/原服权威。新增第8保管单元，本包8/相关22本地通过，原输出字节不变；内容CI原七单元历史不改称八单元。保管提交自身候选/main另实后验。

本轮交付18条可查询文献记录和家庭选择/口令/可选文件/道具流/分域生态规格；原任务引擎、flag、ID、原模型及实服发奖仍OPEN。保持沙拉自主留下、母亲已亡、羽饰非保证、木笛缩写、两地名/母名异写、三层口令关联、方向坐标与两页敌Lv范围，S1七层截图不当总七楼。下一最高NEXT84转另一地区早期具名宠物/生态或同版实参音效，不连扩本洞窟helper；Stage A7 PARTIAL+2 OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING，旧历史全留。


## 2026-10-23 R84：台湾宠物进化史的融合蛋孵化流程与身份未知

按新远端mainaaf30a6f9753936e85f46ac4181fb1c31a9f6df3/treee492fed4b65f156cb2a6f2100cad4d0c7bc6832b启动，491分支、0开放PR/运行中Actions，仅旧queued37642417333单列不动。前轮最终候选10/main11实际completed/success。八启动文件完整UTF8/精确git show/原生Git核对，CURRENT2422321B/SHA2565607c85245270eae9dd9bd011b1bcf8fc4687624d23d3bd4c7288b49d89bdd0e，22域SOURCE-READY-PORTFOLIO-R2全文15948B/7d50de08f7855cf16dbe54b1747e258f1cc1223de88cc217172fd145f3c704ce，历史前缀全留，无AGENTS。按最高NEXT84转另一地区早期宠物材料，不重开R79或连扩强恩洞窟。初日服/台湾宠物检索未得到同版原物种表，转实际可取的2002台湾融合报道；不把发现级现代私服/编年史当原数据。

新增STONEAGE-TW2002-FUSION-HATCHING-SOURCE-CONTRACT-R1、SOURCE/工具/专用工作流。GNN《許慧欣見證「寵物進化史」》标2002-11-14 21:41:11，GNN记者未具名。https://gnn.gamer.com.tw/detail.php?sn=6751 网页读取器403，未取得当前正文、不预称相等。一次Availability以20021201查询，实际返回20190821163207，取https://web.archive.org/web/20190821163207id_/https://gnn.gamer.com.tw/detail.php?sn=6751 ，200无跳转26265B/c9bbe57924b5f3e8fa69ee1494d53934b07d7181926ef9b24166688629add7a9，严格UTF8。2019捕获不是2002原字节/上线日/build，台湾市场归属是语境判断，非直取运营发布稿。正文四段405字符/1211UTF8B/26ef0acd0cba5a0efcb7cd56eea80c78f4bdd9592ad8eb22840a061a59679206，独立去标签/实体归一逐字一致。

恢复文献链：三只不同的宠物＋特殊药材→一枚宠物蛋→特殊饲料孵化→新第三代宠物。不同不擅定为三物种，也不补性别/等级/转生/亲缘条件；药材/饲料只是原文泛称，无原名/ID/数量/配方。不能捕捉或任务取得仅所述将推出第三代，不扩成全宠；第三代不当第三代血缘，前二代不对应1.0/2.0客户端。正文只具名“石器時代-寵物進化史”、未写数字5.0，不倒填后期编年史。引言推出/细段将推出语气分存，不推部署时刻。输入消耗/失败概率/喂食间隔/孵化总时长/离线计时/蛋槽位交易保存/子代物种继承与组合算法全部OPEN。

柴垣秀樹是文中归属的华义聘日本设定画家、第三代造型设计，不认MMO唯一作者或已得原设定稿。许慧欣与《連接》是代言/广告曲语境，非游戏BGM或融合孵化音效；未提取歌词/音频。不以广告曲重开声音底层。与JP2008进化的试炼、四剑齿虎、失败Lv1、付费保障票分开，与TW2002狼人战斗变形/卡牌两兽不合融合输出；共同画家名字不证明同原资产ID。另发现数字之墙2002宠物日志包企业稿，因商品/SBC/刮卡非本流程证据不纳入规则，也不研究实体光盘。

正文实际8条无图注S图库，取第1/8两张当前120×120照片。I1 12389B/bfa82936606a9207af6484866c20325b5893461233792a13ebdfa02ce56d4b1c，舞台多人持萨克斯；I2 12778B/826855871234f9d260ca58511a269d289c36248a6bc1e7433fa87e50ecd5e6f0，一人与两侧扮装人物。均200无跳转JPEG/RGB单帧完整解码/目视，非宠物模型/游戏画面/融合实录，不按扮装/次序认物种或仅像素认证人名，现像素不认证2002原图。另六图未取、不猜B大图；原HTML/JPEG不入Git。

9完整研究目录=版本1/未具名宠类别1/流程1/泛称材料与蛋3/设计广告边界教程1/照片2，具名新物种0，不当9原实体。七必填/19集合核验，三父报告和共享解析器原字节Git固定；19去全部指纹门真实语义改写、隐藏/正文外2反例和外围script正例，本包七单元/原输入回放通过。工作流复用时旧名称/三图文字未替换，在提交前审查修正，未产生错误远端门。候选/main和永久保管待实际后验。

停止于一存档两照片，重开需同地区版本原材料/宠物主表、具名原画绑定、配置或实服流程。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-85回大陆以外具名世界任务/场景NPC、早期宠物生态/资源身份或同版实参音效，优先具体身份，避免连收无名宣传。Stage A7 PARTIAL+2 OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING，无整体百分比，旧历史全留。


### R84双端实源验收与永久派生保管（2026-10-23）

内容c1bec4061c26d83835757a650673a5b859881e18/tree6706e55c087a6622b2a1fd81177057fd77a30462，候选10/main11实际completed/success。九文件原生Git blob及整tree逐一一致，四连续性旧全文前缀完整；fresh main expected_sha保护非强制快进。专用候选run39903937009/job120251467895/artifact12479469761，主线run39904047488/job120251808268/artifact12479568177，日志实际各七单元、精确2019存档/两当前小JPEG实取完整解码、19去全部指纹门语义改写/隐藏正文外2反例/外围script正例通过。没有重新查Availability或声称已取当前403原文。

实际两ZIP各3839B，SHA256cf8fa208414c3f505502fc09050faaec289990aed415299f42ae5e7f5af7aa9e / 5674174133cda9231d48d934b7ba71f149bcf22ccd7e552e2c24a669e3e7d0f4分别符合API。唯一replay.json各17341B/SHA256d0c47d27314e14c05fa061df96112250cec0abc0b548e969cb6028235b619baf，候选/main/local/保管门后local四份逐字节相等，三实际HTTP输入摘要同初取；不认证2002原字节/照片像素/精确build/实服融合，也不虚称未取当前GNN正文相等。

双原CI JSON和STONEAGE-TW2002-FUSION-HATCHING-CUSTODY-R1.json永久入Git；七pin固定SOURCE、三父报告、共享解析器、双原报告原字节/SHA256/Git blob。收据保存21实际run、准确双run/job/artifact/ZIP/raw/input初取历史。CLI强制保管且固定整清单摘要/实际ID/ZIP长度摘要，拒绝缺失或同长篡改、错内容HEAD/tree/分支/任务、遗漏重复或成功门替换、复用工件、虚报输入相等/捕获即刊时/全图与当前正文已取得。另明确拒绝抬高官方/原服/历史权威，或将未得物种身份、融合公式、游戏音效绑定改成已证。新增第8保管单元，本包8/相关28本地通过，原输出不变；内容CI七单元历史不改称八单元。保管提交自身候选/main另实后验。

成果是具名版本报道下三宠/药材→一蛋→特殊饲料→第三代的文献流程、9研究目录（新具名物种0），不是原融合引擎/成长或组合公式。三只不同不强解为三物种，第三代不当血缘，未来语气不当开服日，柴垣设计/广告曲/扮装照片不补原宠模型或声音调用；日服2008试炼与台湾狼人/卡牌不混。最高NEXT85优先另一地区具名世界任务/场景NPC、早期生态/资源身份或同版实参音效，避免连续无名宣传扩张。Stage A7 PARTIAL+2 OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING，所有旧历史完整保留。


## 2026-10-23 R85：日服GW两层集章任务与具名モモトラ奖励

按新远端main9b59a8cda968bedf699262d0be2c6137e529a60d/tree5073c3c3d1bbfefbcd253dabcd73c9736e9c5131启动，493分支/0开放PR/运行中Actions，仅旧queued37642417333单列不动。前轮最终候选10/main11实际completed/success。八启动文件完整UTF8/精确git show/原生Git核对，CURRENT2429354B/SHA2561ab67e32d86d97e1f909946c06e583ab7fd926df1d18c9582946c3e7cf6547db，22域SOURCE-READY-PORTFOLIO-R2完整重读，原历史前缀全留，无AGENTS。最高NEXT85优先具体身份，选择日服2005集章任务与明确モモトラ奖励；远端规格未有该名/活动，不重复旧成果，不重开R79。

新增STONEAGE-JP2005-GW-STAMP-RALLY-SOURCE-CONTRACT-R1及SOURCE/工具/专用工作流。一篇4Gamer同期报道https://www.4gamer.net/news/history/2005.04/20050415190236detail.html ，可见2005/04/15 19:02/Seirou，点名ガイアックス、移管自ボーステック；非原样运营发布稿、未取原活动详情，当前200无跳转16431B/4e6c10774e52aba19737ca22cd9899c8c066e0fce49022a8a11c645802549f3a，严格Shift_JIS。五模板槽一非空，核心止记者签名389字符/1101UTF8B/b89a6f3a4bfb691928a78855d21b0ae312a195d5408dcdcf3d9f608b9283d470，独立去标签/实体归一逐字一致。当前字节不认证2005原件/精确build/原服执行。

恢复ストーンエイジ・GWスタンプラリー的4/28—5/10计划（2005刊时语境），普通お楽しみ面向所有玩家、访问四未具名村集章，奖励Lv1ペット モモトラ，文本明确粉红虎型/等级1；进阶チャレンジ面向中级以上、游历世界集章，推进须先完成普通任务，奖励未具名GW限定物品。数字等级、四村名/原地图/NPC/坐标/路径、精确印章数或其是否道具、奖励数量/效果/ID/重做重置/消费保存均OPEN。前置不是只访问、仅领奖校验或自动开挑战；所有玩家不补服务免费/无任何原服条件，限定不推过期消失。モモトラ不按中文别名强合初代物种，属性成长技能/元素/原SPR/野生栖息未得。

与JSS2001四村会场对照不因同数字四而搬村名/接待NPC/方向坐标；同年寻宝光精灵/结晶掉落/交易重复规则不挪到集章。现代页尾免费不补2005资格。一实际全/缩略链接只取_0big.jpg，未猜其它序号；I1 200无跳转534047B/455b747ed9f0912672a238101b4e17b5469d40e81cef6ac6cc35e583f544bab6，JPEG/RGB640×480单帧完整解码/目视，是草地石路桥水、多人物/宠物聚会，不是具名モモトラ特写或集章实况。底部七导航标签マップ/ステータス/ペット/アイテム/メール/アルバム/システム仅可见标签，未点开/验证功能；无图注/宠物名/任务字、无发奖证明，不认证原像素/原模型或客户端原生分辨率。原HTML/JPEG不入Git。

6完整研究目录=活动教程1/任务2/具名奖励宠1/未具名物品1/画面1，七必填/19集合核验，不当6原实体。三父报告/解析器原字节Git固定，15去全部指纹门真实HTML语义改写、隐藏正文外2反例/外围script正例，本包七单元/原输入回放通过。初试正文one匹配遇五模板槽失败，改唯一非空；首语义改写用去标签串而原A标签隔开导致失败，改真实HTML锚后通过。两本地失败不抹除、不冒初次已过；尚未产生失败远端Actions，双端取源/保管另后验。

有限止点一文一全图，重开须原活动详情/脚本、四村/NPC、具名宠设定或同版资源/主表/原服轨迹。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-86回早期明确地图/生态或同版实参音效，优先具体身份与世界故事，不连扩节庆/奖励宣传或无名截图。Stage A7 PARTIAL+2 OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING，无整体百分比，旧历史全留。


### R85双端实源验收与永久派生保管（2026-10-23）

内容c323190544a2cd55bcabae410e2cb94aedbe2799/tree27955abc4e53869277a925c142807561b7ea9ad7，候选10/main11实际completed/success。九文件原生Git blob及整tree逐一相符，四连续性旧全文前缀保留，新读main后expected_sha非强制快进。专用候选run39906959724/job120261013195/artifact12481033475，主线run39907102925/job120261458913/artifact12480943950，日志实际各七单元、一篇当前旧报道/一实际全JPEG实取解码、15去正文指纹语义改写/隐藏正文外2反例/外围script正例通过。

两实际ZIP各3013B，SHA256caeef6e0fab43f2e6c52d70dafb8547904fabf7784eb60551d723a214d5f1928 / 97940f9df0d272562412d47a975532d8bb7551bd99cda9f2c0fa192637bc595d分别符合API。唯一replay.json各12118B/SHA25673ec96fecc759e454ec739927c9e9ad9609e87d40e63177e1ea095f779059aa1，候选/main/local/保管门后local四份逐字节相等，两HTTP输入摘要均同初取。当前报道与JPEG相等不是2005原字节/原像素/原服发奖或活动已执行。

双原CI JSON与STONEAGE-JP2005-GW-STAMP-RALLY-CUSTODY-R1.json永久入Git；七pin固定SOURCE、三父报告、共享解析器和双原报告原字节/SHA256/Git blob。收据保留21真实run、准确双run/job/artifact/ZIP/raw/input初取历史；CLI强制保管且固定整清单摘要/准确ID/实际ZIP长度摘要，拒绝缺失/同长篡改、错HEAD/tree/分支/任务、遗漏重复或成功门替换、复用工件/虚报输入相等或提升原服/历史/运营详情来源权威。还明确拒绝将截图认作モモトラ、把导航可见当交互已测或把未得宠物原数值/ID改成已证。第8保管单元加入后本包8/相关28本地通过，输出原字节不变；原内容CI七单元不冒称八单元。保管提交自身候选/main另实后验。

补查现有官方124网页宠目录/研究JSON，无既有本活动/モモトラ规格命中；一次精确名称检索仍仅得到同一4Gamer文章及无关结果，不作全网穷尽证明，也不计迁移ddo主机为第二独立来源。没有新增原设定图/绑定，不以颜色指认截图宠物。

本轮交付两具名任务的完成前置、具名粉红虎型Lv1モモトラ奖励、6文献行和七可见导航标签，原宠表/任务脚本与执行仍OPEN。四村不因数字四强合JSS出生村，中级不补数字等级，挑战未知奖励不改作宠物，图片不证明任务/发奖或交互。最高NEXT86回早期明确地图/生态或同版实参音效、优先身份与世界故事，不连扩节庆/奖励宣传。Stage A7 PARTIAL+2 OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING，旧历史全文完整。


## R86 — 2026-10-23 CN2003 拉多拉／巴那姆／深红地理生态（内容候选，待双分支验收）

FACT：本轮从新读远端 main `a16fde079936e9fd893f68e8b2941162b7b33030`、tree `85386d8acd448bdc9a8619085022e158019ec285` 启动；495个分支、无开放PR及运行中Actions，旧排队run37642417333未触碰。上一轮候选10／main11检查均成功；八份连续性文件完整读取并与fresh checkout逐字节比对。CURRENT旧前缀2435984 bytes，SHA256 `138babb2a3a29f30bbda5edd9a78e3dcecd3e79ae2e98a2b3f3303cd04de228f`。最高优先项 OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-86。

交付：`research/recovered/STONEAGE-CN2003-LADORA-CRIMSON-SOURCE-R1.json`，SHA256 `98cacbd0c24d93fe1f2c8f1a969a678dfd8ab8c237375c01664e84fb15f1f051`；专用工具／测试／Actions：`stoneage_cn2003_ladora_crimson_source`。版本范围 CN_SINA2003_LADORA_CRIMSON_GEOGRAPHY_EXACT_BUILD_UNKNOWN，仅选取同一2003年门户攻略的地理、生态和世界叙事段落，停止于1页＋1张实际链接示意图，不扩大音效helper。

来源：https://games.sina.com.cn/zhqu/sta/article/2003-06-09/11645.shtml ，标题《石器时代》任务功略-深红洞窟，显示2003-06-09 14:03、作者字段新浪游戏、我要投稿链接，未署名原作者，不认证官方脚本。当前GB18030严格解码59256 bytes／SHA256 `684983365e929e42d7987e86f962ca2d7641e6185c98464cd4788023909fe3ae`，HTTP200无重定向。实际图 `https://image2.sina.com.cn/gm/newgames/0303/images/tuxing0610_03.jpg`，22812 bytes／SHA256 `15f3e751a5828d906815e2b3d514e0d9940e87c52cb2f605789dcd7b2183e9ef`，Pillow完整解码JPEG RGB500×236、单帧，已人工查看。

实质新增：四条登顶路线各3条有向边，7条按正文出现位置分开的地理／生态记录；世界坐标、回廊内坐标、巴那姆地下2楼内坐标分别保存。两个巴那姆入口(295,259)/(388,337)，两个深红入口(45,41)/(26,5)，格鲁西／格鲁西斯原样分存。怪物等级和种类仅为攻略陈述，非可捕宠物主表。吉鲁火山、百余年、伊拉祈祷和不死鸟以奇宝形体现身／被发现后换山顶为世界故事与指南描述，非地质模拟或已观测服务端机制。

图像是路线示意图，非游戏运行截图；8个印刷节点含c120302、c120303、c120306、c120305、c120304、c120308、c120307、c120309及10条箭头单独记录。图共用c120309山顶标签与正文“四座不同山顶”并存，原生地图ID、实例数及几何均OPEN。四洞口与四路线不强行一一映射，推荐80级／成人仪式仅保留关联任务表头语境，不提升为全图准入。

10条目录记录满足7必填字段／19合法集合；game_ids空、仅研究元数据非发行授权。三个父规格和共享解析器钉原始bytes／SHA256／Git blob。41项真实HTML语义改写（排除所有指纹）＋2项隐藏／正文外反例＋外围脚本正例；独立regex/entity生态读取一致。初始本地26项关联测试成功，源回放成功。原始HTML和图像留临时目录，Git仅派生JSON。完整两支任务、送水7/7奖励表、其他配图、本服运行、版本号和原始地图／宠物ID均未恢复。

NEXT：内容候选10项成功后以fresh main expected-SHA非强制快进，再核main11项；永久保存原样CI JSON和完整run/job/artifact/ZIP/raw/blob保管链，加入强制缺失／等长损坏／身份替换拒绝测试，再验收保管链候选与main。阶段A仍7PARTIAL＋2OPEN，阶段B/wiki GATED；savedata R79 PAUSED_NON_BLOCKING。之后 OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-87 优先具名宠物／人物原始内容或具体原始UI交互证据，避免连续扩洞窟路线；若找到同版本实际audio调用实参才重开音效依赖。


### R86 内容双分支实际验收与永久保管链 — 2026-10-23

内容提交 `3c0b80a38ad7cdfc2604496681020b4a7ad126f0`，tree `e4be822c5f6e2e594103d896ca7511deb2b73f72`；候选10／main11共21个实际Actions全部completed/success，专用job初始7tests成功。

candidate: run39934221560／job120349672167／artifact12492434392，ZIP4125 bytes `sha256:369e57a355b72c5795201f05ec71b9b53d3448259546739879e4c041894ea998`；原样JSON28147 bytes SHA256 `4c84646a0e36b39fe938ccf08cb07a036d3296cc658176e3a06b9da6467f2fa9`，Git blob `55cf00fe36db65e10a79079a4c92c59e38340c75`。

main: run39934550590／job120350775724／artifact12492594617，ZIP4125 bytes `sha256:46eea10ea08ed5f94b55df2cb8b2a3b7415ee2a07435863536fede12b767b414`；原样JSON28147 bytes SHA256 `4c84646a0e36b39fe938ccf08cb07a036d3296cc658176e3a06b9da6467f2fa9`，Git blob `55cf00fe36db65e10a79079a4c92c59e38340c75`。

两个ZIP均实际下载核对GitHub digest与长度，成员仅replay.json；CI原样JSON与初始本地回放逐字节相同，输入当前原页／JPEG bytes和SHA256一致。永久保存CI-CANDIDATE、CI-MAIN、CUSTODY三个派生JSON（原始HTML/JPEG不入Git）；收据固定全部21run清单摘要、两个真实run/job/artifact、ZIP长度/digest、raw字节SHA256与Git blob、7份永久证据pin。CLI强制校验；第8项测试拒绝缺失／等长破坏／run和job替换／重复清单／ZIP身份变化／原生ID或运行覆盖抬高。保管链候选及主线仍须按实际Actions再验收。

NEXT最高 OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-87：优先具名宠物／人物内容或原始UI交互证据；版本／本服运行／可捕性仍OPEN，阶段B/wiki GATED，savedata R79保持非阻塞暂停。


## R87 — 2026-10-23 JP2005 宠物图鉴的画面登记与两阶段更新

FACT：按新读远端main `cf52a0a35ea7d4f13e24b1ff17abfefd4ebb16a0`／tree `2dd6065ef8fa7c3d44f6540a385893bd3e84c54c` 启动，497分支、0开放PR／运行中Actions，上一轮最终候选10/main11实际全部成功；旧queued37642417333单列不动。八启动文件严格UTF8完整读取并比对fresh checkout原生Git；CURRENT旧全文2441519 bytes／SHA256 `27cc3dadfee0ef9794f3170f0b8645b4cede828dae8ac00d7472e6530240cc18`，无AGENTS，22域索引全文核读。按最高OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-87转具体图鉴交互文献，查JP2004展示宠物和CN2003操作已有规格，不重复计新结果。

交付 `STONEAGE-JP2005-PET-ENCYCLOPEDIA-SOURCE-CONTRACT-R1`、SOURCE JSON、专用工具／测试／工作流 `stoneage_jp2005_pet_encyclopedia_source`。只选2005日本GaiaX运营时期报道，不认证1999／TW1／CN1.82同build，也不把新作StoneAge2的Pal图鉴规则挪入。没有同版audio实参，不重开音效helper或savedataR79。

来源 https://www.4gamer.net/news/history/2005.07/20050705162235detail.html ，标题ガイアックス，「ストーンエイジ」で新ペット恐竜を実装，显示2005/07/05 16:22，署名TET。当前200无跳转17834 bytes／SHA256 `983b11f84dd9c492c4b868bc96921fecbbb582e87a6243c322c9f8ad684f06b9`，SHIFT_JIS严格解码零替换。为同期记者报道，非原样运营公告；当前字节不认证2005原字节，原更新页／脚本／精确客户端未取得。

实质规格：7月5日定期维护后补新宠及同种野外怪物图形、扩充宠物图鉴；7月12日维护后补此前未出现的Lv.1野外恐龙并改部分配置，明确新恐龙实际登场在第二次补丁后。图形存在不等于已在世界启用，不把“此前未出Lv1”扩大成全游戏首次有Lv1，也不补物种数／具体地点／刷新率。两阶段部署与事件仅为所报／所计划，不是实服执行验证。

图鉴正文明确：新宠显示在画面上→该新宠的名字登记于ペット図鑑。此句不以捕获／拥有为触发，不把名字登记当得到宠物或全属性／技能已登记；其它必要条件、全部旧宠适用、精确按钮与版面、持久化、重复处理与存储仍OPEN。7月12日22时前后GM展示为计划与约时，无精确分秒／时区；寻找GM是指南建议，不当只有GM展示才能登记。与CN2.0“曾拥有宠可拍照”的相簿描述、JP官方网页宠物目录分别存，不互补规则／不当同一UI。

实际配图只有正文链接 `/news/image/2005.07/20050705162235_0.jpg`，3371 bytes／SHA256 `81a547ca33684426e6c9b42fcace9850e543955b379d49487d2da6d276383394`，200无跳转，JPEG RGB96×104单帧完整解码／目视：浅蓝甲壳蟹形小插图、黑底，无物种名／图鉴UI；不猜_big图，不认作原SPR／动画／某具名物种，不因一图宣称只新增一宠，不认证历史像素。原HTML/JPEG仅临时保存，Git为派生研究元数据。

5条目录记录：两阶段教程＋登记规则教程＋计划GM展示教程＋未具名插图，7必填／19合法集合、game_ids空／非发行授权。三父报告及共享解析器固定原bytes／SHA256／Git blob。独立regex/entity正文逐字一致，19项真实HTML语义改写排除全部指纹门、2项隐藏／正文外反例及外围script正例通过；初始本包7tests及关联回归、源回放通过。止点一报道一实际小图，重开需原操作视频／同build脚本或具名图像／数值绑定，不靠更多匿名宣传图扩张。

NEXT：候选10/main11实际成功后永久保存双端原样派生JSON与准确run/job/artifact/ZIP/raw/blob收据，强制保管链校验并再验收。最高后续 OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-88 优先早期具名人物/NPC对话或具名宠物属性的原始证据，不连扩匿名插图或奖励宣传。阶段A仍7PARTIAL＋2OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING；无整体完成百分比。


### R87 内容双端实际验收与永久派生保管 — 2026-10-23

内容提交 `7c734e08fc53540045063816409484c8133732df`／tree `8cc44097da5c022ef12e488ec72156411b1b7e7f`，候选10/main11共21个实际Actions全部completed/success，专用日志初始各7tests成功。

candidate: run39935988520／job120355531891／artifact12494111171，ZIP2720 bytes `sha256:0179f8b274a1003612b70f36cab4355ecd3fb257c7d731fcdf8642c8ed8169a4`；原样JSON10170 bytes SHA256 `c1f6ba1456c16a9cd5479deb43456d00e14f03e10c2f352eb13451ea32fdaaa5`，Git blob `b0142336c98750fc831b753179c7a23e5e3d56e1`。

main: run39936177726／job120356148265／artifact12493847454，ZIP2720 bytes `sha256:d65293c7d90e418f886c28c56698424e73bbc5d4d89c3c1fb8ec65f8f5c3815d`；原样JSON10170 bytes SHA256 `c1f6ba1456c16a9cd5479deb43456d00e14f03e10c2f352eb13451ea32fdaaa5`，Git blob `b0142336c98750fc831b753179c7a23e5e3d56e1`。

双ZIP已实际下载核GitHub长度与digest，唯一成员replay.json；候选/main/初始local的原样JSON与两个实际输入bytes/SHA256一致。双原CI派生JSON及CUSTODY永久入Git，原HTML/JPEG不入Git；7份证据pin固定SOURCE、三父、解析器和双原报告bytes/SHA256/Git blob。收据与代码常量锁定完整七pin清单摘要，反例同时改证据与重算receipt pin仍拒绝；收据锁定21真实run清单摘要、准确双run/job/artifact及ZIP摘要；CLI强制保管，拒绝缺失/等长篡改、run/job/artifact替换、遗漏/重复/复用工件、虚报原输入相等及历史/本服权威抬高。第8项专测还拒绝插图指认物种、图鉴实际交互已测、名字登记等于获得宠物。保管候选及main自身仍须实际后验；原内容CI7tests历史不改称8tests。

交付为文献中的画面显示→名字登记与两次更新范围；没有运行原服/完整图鉴数据/宠物原属性或UI画面。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-88优先早期具名人物/NPC对话或具名宠物属性，避免连续匿名插图/奖励宣传。Stage A7PARTIAL+2OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING。

R87保管门本包8项／关联24项本地测试成功；CLI原输入回放与初始输出逐字节不变。完整七pin身份摘要另固定在代码常量中，连同篡改证据后重算收据pin的反例一起通过。


## R88 — 2026-10-23 伊甸动物园：具名NPC条件、拉斯基状态样本与交还顺序

FACT：按新远端main `7b358092650612d506b2a29cd5c8be7715186d53`／tree `47327c3c7d841ceb1ff19101f0ee67cd52bbd1c1` 启动。499分支，无开放PR／运行中Actions；上一轮最终候选10/main11全部completed/success，旧queued37642417333未动。八启动文件完整严格UTF8读取并与fresh checkout精确git show一致，CURRENT旧前缀2447908 bytes／SHA256 `afc036e02ff0f1fbd7199331217400d5751e6869cec3ec0af94134062bc101da`；全tree无AGENTS，22域索引全文读取。最高OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-88转具名NPC／宠物属性证据，网页宠物目录已有同名项但没有本任务规格；不以同名强接原生实体。

交付 `STONEAGE-CN2003-ZOO-RESCUE-SOURCE-CONTRACT-R1`、SOURCE JSON（SHA256 `bf37d19e3f88b711483289dd1b17255925d0bfcdbbbe64bea52f13815f7b2ca6`）、专用工具／7单元／Actions `stoneage_cn2003_zoo_rescue_source`。范围一篇同期攻略＋两张实链全图；完整记录本文所述救援流程，不宣称恢复原任务脚本／原服执行或全部版本动物园。

来源 https://games.sina.com.cn/zhqu/sta/article/2003-06-03/10646.shtml ，《石器时代》任务功略-动物园任务，显示2003-06-03 17:58、作者字段新浪游戏／我要投稿链接，无具名原作者。当前HTTP200无跳转72640 bytes／SHA256 `e92f92126182fb0834f7ec329a615cb1b7629e54da1de1943dd016af828ad046`，GB18030严格解码零替换。门户攻略不是经认证运营脚本、2003原字节或确切build；伊甸与尼斯语境分别保留，不反投TW1.0/CN1.82或混入2024手游复演／私服。

具名流程：沙利斯园长委托找雷尔胖／波波顿／拉斯基；布伊太郎饲料与雷尔胖鉴定，蓝色目标75,170不是任一布伊胖；波波顿170,181仅指南所述等级1，经鲛岛太郎鉴定。一次一种正确饲料为攻略建议，混带“很难遇见”不写成零概率；先打一击建议不变捕获公式。推荐90非硬门槛，完成金飞为本文前置，不展开另一任务。雷尔大人是故事中的园主／宠物主人称谓；贝壳及三出处只是正文关联，不补消费或已完整恢复其余两条支线。

里拉拉22处、伯特5处表格逐行解析，里拉拉末6处室内坐标分别保留，不能并进同一世界坐标；里拉拉81,69／伯特171,72的“服务器重开机”注记只是指南声称。伯特按所列顺序走为描述，无周期秒数／已测重启算法。伯特、铲子、啦啦口令与白萝卜／红萝卜3／柯奥红萝卜4交换上等白萝卜相连；不太差／还不差异写不强原物品别名。保留铲子落地消失及可重领、萝卜落地消失、见兔前丢铲子、带铲子或红萝卜时连上等白萝卜被收走的本任务条件，不泛化全局道具规则。

里拉拉前五次及后续叙事分别存，“再找”不捏造第六个服务端flag；啦啦是里拉拉口令，拉拉是它所述拉斯基别名。林务局是误导线索，项圈→再问南边雷尔大雕像→黑色的服→动物园后方藏身处／4楼黑色的旗→5楼席格逐步关联；不给掉率／保证掉落／原消费flag。席格为塔尔塔战士团寻老团长、乔装救动物的角色叙事，“动物园是驯兽中心”为其怀疑，兔子释放计划不是他们的安排。

四组敌人资料按场景存原标签、以上下界和区间、技能文字。林务局与洞窟格尔希洛不能合一套数值；正文称后者较不凶悍，与各自数字分别保存不强协调。席格两项攻击力500／700照录，防御力未知，不擅改700为防御。洞窟总览0,64与一楼入口20,64并列OPEN，四层各入口／出口不强反向或接原地图ID。

领奖关键顺序：先把救出的拉斯基带给里拉拉报平安，再向园长交还三宠得到一只“刚出生”的布伊胖；随后以咬过白萝卜换铠。遗漏前置报平安会失去铠的提示单列；不将布伊胖“刚出生”推成已证数值Lv1。铠原称防+40敏+10、恩惠的精灵Lv4，实际发奖／精灵效果未测。

26实际全图/缩略对中只取08和020，其余24全图不取。I1 `https://image2.sina.com.cn/gm/newgames/0303/images/dongwu0603_08.jpg` 108055 bytes／SHA256 `3cdfea6514804d9ee9d7a0dd6b72c40df4bc2dafbf5c94654a190360dda82301`，物品窗可见可以挖萝卜的铲子／好用的铲子。I2 `https://image2.sina.com.cn/gm/newgames/0303/images/dongwu0603_020.jpg` 88503 bytes／SHA256 `1afc3b40e06f874c4b5b016bc2c852769ded5bcfa6c04a19bccee75d39425b8c`，状态窗显示“动物园养的拉斯基”：等级1、NEXT2、耐久力17/17、攻击力2、防御力3、敏捷力2、忠诚度100；火／风色条可见，不从像素长度推比例。仅这只显示宠物的静态样本，不当整个物种初值、成长、原SPR/ID/实际交付证明；不把旁边无名字人物指认为原生席格。两图均200无跳转JPEG RGB640×480单帧完整解码／人工查看，不认证原像素。原HTML/JPEG不入Git。

16条文献目录＝任务1／具名行动者或会说话物件7／救援目标3／奖励宠1／任务地图1／铠1／画面2；满足7必填与19集合，原game_ids空，非发行授权。三父与解析器原bytes/SHA256/Git blob固定；49项真实HTML去全部指纹语义改写、隐藏/正文外2反例与外围脚本正例通过，独立regex/entity全文相同。初始20项关联测试成功。补充园主／两场景语义后，快速同尺寸写入摘要导致本地Python缓存仍读旧常量，一次validate及两测试失败；核对磁盘摘要与JSON一致、移除本包缓存后 fresh import／20项测试及源回放通过，保留此失败事实。未产生失败远端Actions，远端验收仍待实际后验。

NEXT：先内容候选10/main11实际验收，再永久保留双原派生CI JSON及真实run/job/artifact/ZIP/raw/blob收据，强制保管与反篡改测试后再次验收。最高后续 OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-89 优先另一地区具名宠物技能／成长／骑乘或早期登录人物视觉的原始资料，避免连续扩本篇伊甸线或通用helper；同版实际audio实参才重开音效。Stage A7PARTIAL+2OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING；无整体完成百分比，旧历史全部保留。


### R88 内容双端实际验收与永久派生保管 — 2026-10-23

内容提交 `34c59aabfbd96b20c41df22dbbe44e8191ac1010`／tree `4a178c2b41cbccf284f5fc9785c7812991bdfee4`，候选10/main11共21个实际Actions全部completed/success，专用日志初始各7tests成功。

candidate: run39938717033／job120364577573／artifact12493839392，ZIP9699 bytes `sha256:212bfa8808e70bad2e49de3a232d43a8ed494274637dcc12b7d02b1d87c0603c`；原样JSON71990 bytes SHA256 `e4f1c8b8e11497ead6beb3f41a5706d7c79472f608c17be7782611e3cfe55d1e`，Git blob `4d8e620cc87dd073ca3ac2fb3f6fdc322a2a39a9`。

main: run39938920735／job120365251773／artifact12495411010，ZIP9699 bytes `sha256:1cc958f7e0ef623e3e18637084c17716b7b3c93758fa132de2597ef851fea071`；原样JSON71990 bytes SHA256 `e4f1c8b8e11497ead6beb3f41a5706d7c79472f608c17be7782611e3cfe55d1e`，Git blob `4d8e620cc87dd073ca3ac2fb3f6fdc322a2a39a9`。

双ZIP实际下载核对GitHub digest与长度，唯一成员replay.json；双端原样JSON与初始local相等，3个HTTP输入bytes/SHA256同初取。双原CI派生JSON及CUSTODY永久入Git，原HTML/JPEG不入Git。7证据pin固定SOURCE、三父、解析器和双原报告bytes/SHA256/Git blob，代码另锁完整7pin清单摘要；同时篡改证据和重算receipt pin仍拒绝。收据固定21真实run清单摘要、准确双run/job/artifact及ZIP长度/摘要；CLI强制保管，拒绝缺失/等长破坏、错HEAD/tree/分支/任务/ID、重复或遗漏门、工件复用、虚报初取相等及历史/运营/运行权威抬高。第8单元还拒绝单只拉斯基截图升物种主表、静态图升任务执行、席格第二攻击力改防御。原内容CI7tests不改称8tests；保管候选/main自身仍须另实际后验。

最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-89：另一地区具名宠物技能/成长/骑乘或早期登录人物视觉，避免连扩本篇伊甸与无名宣传图。新候选分支将使总分支超过500；下轮分支清单须继续分页到不足100条，不能停在固定第5页。Stage A7PARTIAL+2OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING。

R88保管提交前：本包8项／关联21项本地测试成功；原始3输入经强制保管门回放，输出与初始local／双原CI JSON逐字节相同。完整旧历史前缀保持不变。


### R89 报社回刊的2000人物选择记述与早期标题照片 — 2026-10-23

启动以GitHub实际main `5b364c4685e6a1405a9337818cc87ff32715f6f2` / tree `ad8405ea6549de06ed0a0ad67e8cbc0013b54f9e` 为基线；501分支完整读取至第6页，0 open PR、0 in_progress；旧无关queued37642417333不动。HEAD候选10/main11全部completed/success，tree5286条无截断、无AGENTS。八启动文件完整UTF8读取并逐字等于本次Git checkout；CURRENT前缀2456591 bytes/SHA256 `76b9a960f3d168ea0307b4c0ac73d3bd622da47fedf53a8cbd31502da51dadd6`。遵循最高OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-89，补早期人物视觉及人物选择记述，不连扩伊甸。

FACT（限定报社回刊）：报时光／聯合報系2023-04-13 13:22《元祖級Online Game！ 2000年上線的「石器時代」》https://time.udn.com/udntime/story/122835/7095433 明确引用2000-04-11《民生報》37版3C新聞網《網路電玩石器時代上線了》。引文记4種顏色與48種不同造型、自设人物、WGS预付卡扣点对比普通月费，以及面向新人的不喪命／宠物忠诚降低简述。保存原措辞；不乘成192、不分解为12×4、不填原版TW10人物总数/13个创建字段或CN20类型颜色数，不升成完整死亡/复活/扣忠诚公式或收费单位价格。昨日发表来自日本的游戏不是精确服务器开服日。2023外层正文的骑乘及计次非计时不反填至2000引文。

配图图注独立署名2000/02/10 林信昌攝影，写今年3月底將推出（预告而非已执行开服），不混成4月11日或2023发表日期。实际查看可见人在键盘前、CRT上StoneAge字样及中央竖向菜单轮廓，按钮及账号文字不可读；现代報時光水印可见。底层uc.udn直接图URL实取403；页面真实img src的pgw.udn代理实取200无跳转，109235 bytes/SHA256 `7477d5b56427520ede444b5d8f8baa105373a4d004efa2420782ff6e3de11ddc`，JPEG RGB800×450单帧完整解码。照片不是客户端直接截图、原始像素布局、原生800×450分辨率、已操作登录流程、48个可见人物或原图字节鉴真；代理裁切缩放和当前水印不等于2000原件。

初取HTML137674 bytes/SHA256 `44553c4e5c981b8d28534bf250a32f60496d116b84cc42b14071be441682b238`；不是2000原报扫描或原始照片master，也非运营方原脚本。精确build、原报排印与历史像素原件均OPEN。严格固定所选标题/回刊日期/唯一引文/图注/实际图链接；对推荐栏等范围外包装漂移保留各次实际inputs bytes/hash，source_identity如实标明是否等于初取；不以CI哈希覆写初取，不要求不同包装的双原报告字节相等。引文归一化366字符1036 UTF8 bytes SHA256 `7e2ec89c02af77c06da7fee3d8498f816dc9939e065073a879b3053794362a46`；图注109字符305 bytes SHA256 `a669030b71e7b959b9a61d3ac6610e69d0507b510185237a5230c2016a238af6`。

产物：SOURCE、可重放工具、7项单元、专用Actions、内容契约；4条纪录为人物选择数量组/败北简述/支付简述/标题照片，使用19集合及7必需字段，game_ids null，仅研究元数据不获发行授权。三父SOURCE及共享parser bytes/SHA/Git blob固定不改。独立regex/entity归一化与解析器双核对；16语义变异在不依赖全文fingerprint下拒绝、2隐藏/范围外伪修复拒绝、script与外层回顾改写正例保留。测试使用内存合成JPEG，未提交原HTML/JPEG。本地语义键改名后3单元与CLI曾因同秒等长重写残留pyc SHA失配，清除此任务缓存后7项全部通过；失败不抹除，不伪称远端失败或成功。

待双端真实CI与原样派生报告永久保管后验收。下一优先OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-90：另一地区具名宠物技能、成长或骑乘材料，优先具体规则与可辨认宠物，不连续拓展本回刊泛述。Stage A7PARTIAL+2OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING；缺同build真实音频参数不扩音频helper。


### R89 内容双端实际验收及原样派生报告永久保管 — 2026-10-23

内容commit `6c753de234e5fe173b1f312839e272101d6dbb88` / tree `8d7cfe602786543d9d534cd41231d7e2f69baafc`。候选10/main11共21个实际Actions全部completed/success，双专用任务日志均7tests与真实网络重放成功。

candidate实际run39940945771 / job120371931887 / artifact12495304253；ZIP3184 bytes `sha256:ee3f97d59bc297b6058a843e68bd55a9448bb85b4af703a9d231c4142363f77d`；原样JSON11015 bytes SHA256 `1dc1787940c20bbd9627ef06e1498561b6fc84b6cd1d5a7f4746f425582b1b89` / Git blob `a2cc7bab38e292a05e17531d8a1be42d08a36658`。实际HTML137528 bytes / `95df497b74e0415641829eb05a2b4d865fa35b456896fd17742fc2f82582006e`，equals_initial_inputs=false。

main实际run39941078117 / job120372368259 / artifact12496250941；ZIP3184 bytes `sha256:a2ba935c6afe0751204efd4bb766ce83eb61060ca3e2226d51bc28ae38aba6db`；原样JSON11015 bytes SHA256 `de842a9ab4fb1fa74b8b4fc0bae9f64f26da1d65e1daca1529f072cb0f3a4dfb` / Git blob `93bc265dd144affe91a480e95b754e97b1c75e88`。实际HTML137670 bytes / `14137dd92f1529dcf8b0e32de0b779e67b767e18c45adf62e396b0017028f9b3`，equals_initial_inputs=false。

双ZIP真实下载核对API摘要与长度，唯一成员replay.json；原样JSON分别永久入Git，candidate_main_raw_bytes_equal=false。两端所选引文/图注fingerprints、4条内容语义、照片bytes/full decode/视觉观察、父比较、16语义变异及2隐藏反例和双范围外正例严格相等；两次HTML整页均不等于初取且互异，source_identity.full_html_equals_initial_intake=false。保留初取137674/hash44553c…不改写，原件鉴真仍false；网页推荐/广告包装变化不影响选定内容，亦不构成原报或历史像素鉴真。没有把两份不同原样JSON重写成同一份。

保管收据固定SOURCE、三父、parser、双原报告共7证据的bytes/SHA256/Git blob，代码另锁完整7pin清单摘要；同时破坏证据并重算receipt pin仍拒绝。固定21真实run清单摘要、精确内容HEAD/tree/候选分支、双run/job/artifact与ZIP摘要/长度；检查每份schema/实际inputs、是否初取的真实布尔值与source_identity、内容语义和边界。CLI强制检查保管；新增第8项反例覆盖缺失、等长破坏、重算pin、虚报相等、任务/分支/HEAD/ID/ZIP错误、复用工件、冒充原报/服务器执行及数量填原版主表/照片升截图/外层骑乘反填。初始远端日志7项不改称8项；本地最终8项及20项相关父域测试共28项通过，原初取输入重放输出与初始local逐字相等，diff check通过。保管提交候选/main自身仍须远端8项和全门后验。

最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-90：另一地区具名宠物技能、成长或骑乘，要求具体来源和宠物，不连扩回刊泛述或匿名宣传；Stage A7PARTIAL+2OPEN、B/wiki GATED、savedataR79 PAUSED_NON_BLOCKING保持。原HTML/JPEG及原报扫描未入Git；4条研究记录不是48个已恢复原版人物。


### R90 台湾8.0具名骑宠资格、类型装备栏与静态面板 — 2026-10-23

FACT：以本轮GitHub新读main `8c60f9139ff149f4e1f846e74a4f575c73321ee7` / tree `344ec5027bfcd2c59e5a9105c40d8c864f235c8d` 启动；503分支分页至第6页3条，0 open PR/in_progress；HEAD候选10/main11共21实际Actions全success，旧queued37642417333不动。tree5294完整无AGENTS。八启动全文严格UTF8与fresh checkout原生Git逐字一致，当前22域索引15948B/hash7d50de…完整核读；CURRENT旧前缀2463657 bytes/SHA256 `b68540c8adf394fa389e88c92e8110879e3034bea5ad927d9c821b17ff9babb2`。最高OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-90补具名宠物骑乘条件，不连扩回刊/匿名图或无关helper。

查重：JP2008进化公告已有规格，不计新；GNN sn20167原页本次HTTP403，未取得，不规避访问限制。改取已知同文的正常公开新浪衍生转载，不能称两份独立一手证据或本轮首次发现8.0宠物装备。旧 `docs/specs/STONEAGE-PET-80-CONTEMPORARY-RELEASE-EVIDENCE-R1.md` 已保存2005发布意义，完整固定不改；本轮新增实际内容语义、具名骑乘条件、真实图像与可执行重放。不是突破旧PET配对build/opcode127缺口。

来源 https://games.sina.com.cn/o/n/2005-06-09/1552109910.shtml ，可见标题《石器时代8.0》开放全新宠物装备(图)，2005-06-09 15:52，来源巴哈姆特、编辑梁凌；明确台湾地区消息。HTML200无跳转48685 bytes/SHA256 `a67c9ee21070d048c7dae901cf8c505b6ced3c888abd1ebcc190f764c1f7f4d8`，GB18030严格解码。Sina URL日期、转载时间与“今日上线”不单独证台湾6月9日开服，不改旧原GNN6月8日报道日期；原运营稿、2005原字节、精确build未取得。

具体骑乘规格：8.0报道新增骑乘对象2只，水魔鬼鱼史卡鲁、恐龙系罗多克雷；新骑宠不等于新物种。仅史卡鲁被说明为新庄园宠、主要出现泪之海；取得难易为定性，而想骑则需新庄园族长发给骑宠证。证书门只绑定该句的史卡鲁，不扩至罗多克雷；证书原ID/族长名字坐标/领取条件/费用/是否消耗/角色对应/等级/忠诚/骑乘属性未知。与CN2.0四庄园骑师、三课程、忠诚100、人物训练及骑战公式分版，不相互补齐。

装备段依宠物类型给予不同装备字段；七大类＝头/牙/爪/胸/背/翅/脚，脚括注两只脚/四只脚/鱼鳍不是三个额外大类，不推出所有宠物都有七栏。可通过合成制作装备，装备自身有属性，按地水火风关系出现能力增减；无具体宠物身体类型对照、装备数值、叠加/取整/相克倍率或全配方表。相邻合成上限由11到15为报道语境，不当人物等级15或全15级配方已恢复。

真实链接链：正文第6个图文链接指向 https://games.sina.com.cn/o/i/2005-06-09/61677.shtml ，图库标题宠物装备套装／2005-06-09 15:52新浪游戏，35353 bytes/SHA256 `41ae049999094a87ef0a6a1789c2ab9ef55d226093267d9a1a191a883c5b11fc`；真实myImage及点击查看原图均指同一非_c全图。仅将页面明示http同主机同路径改https实取，未猜图名或递归其余5图。全图 https://image2.sina.com.cn/gm/o/n/2005-06-09/U508P115T9D109910F376DT20050609155230.jpg ，200无跳转77930 bytes/SHA256 `3126fbb80a7d379530519840e78563dc850707a17e89764f21ad2b82df52aa23`，JPEG RGB640×480单帧完整Pillow解码并实际目视。搜索打开同图曾超时，本机实际请求成功；不混报下载失败或2005原图鉴真。

可见PET STATUS、黄色鸟形宠、人物位于黄色骑乘形象上、右侧7位置装备栏及图标背包、持物光标和绿色格框。未抄不确定宠名/装备名或状态数字，不把此黄色图认作史卡鲁/罗多克雷；像素条非属性百分比、单体状态非物种初值/成长、静态持物光标非成功穿戴/服务器IO/包127/可用PET宏build。640×480当前图幅不是客户端全局原生布局或原SPR动画。原HTML/JPEG不入Git。

交付SOURCE、5条研究目录（具名骑宠2/类型装备教程1/合成上限语境1/面板参考1）、契约、专用工具7单元及Actions。7必填/19合法集合、game_ids null、非发行授权。两HTML各自实际bytes/hash与初取是否相等如实保留，选定三正文段/图库图注与链接严格固定；初取基线不被CI包装变化覆写，JPEG完整固定。三父（旧CN20骑乘、旧PET80发布规格、内容档案）及parser完整固定。独立regex/entity三段与解析一致；20语义变异移除fingerprint仍拒绝、3图库身份反例、2隐藏/正文外伪修复及外围script正例通过。本地生成器首有正则引号语法错误，继有脚括号内顿号误拆；修正结构分组后，真实反例发现“不能透过合成制作”仍命中子串，收紧肯定完整句后20变异/7项通过。保留预检失败，不冒称已远端验收。

止点：一台湾报道衍生转载＋一实际图库＋一全图，完成具名骑证条件与装备类型资料，不实现骑乘/装备或推原服。候选/main真实CI后保存双原派生报告和收据再验收。最高后续OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-91：优先早期具名NPC对话/交互界面或另一地区具名宠物技能数值来源，避免连扩本报道其它娱乐设施/无名图；Stage A7PARTIAL+2OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING，无整体百分比。


### R90 内容双端实际验收及永久派生保管 — 2026-10-23

内容commit `f2ce09647efd8cbb67994e7f9718b18d3efc8e15` / tree `c5b2d1c9760ff14917fc2f4cee499d87153caf43`，候选10/main11共21实际Actions全completed/success，双专用日志各7tests与真实两HTML一全图取源成功。

candidate: run39943758433 / job120381250855 / artifact12497147418；ZIP3458 bytes `sha256:fc1551cc8a3a904cf00e8c0d36b61eb787c122ce812c55f12defdd4b8be87046`；原样JSON12168 bytes SHA256 `75bb718becb3e152bbe0057988cb355739810351d23c992304456b3cccec41d9` / Git blob `584983c1b8c7137c72b70d64675a1da0ff722801`；equals_initial_inputs=true。

main: run39943895787 / job120381709724 / artifact12496718117；ZIP3458 bytes `sha256:5b12c0a77e9bb6872e01bbfedeff3fef8481188dc408c40d6c371cd09782a028`；原样JSON12168 bytes SHA256 `75bb718becb3e152bbe0057988cb355739810351d23c992304456b3cccec41d9` / Git blob `584983c1b8c7137c72b70d64675a1da0ff722801`；equals_initial_inputs=true。

双ZIP真实下载核API摘要和长度、唯一成员replay.json。双原样JSON与初始local逐字相等，3个实际输入bytes/SHA256一致，candidate_main_raw_bytes_equal=true；S1/S2初取比较均true，如将来包装变化仍各自诚实记录，不覆盖初取。引文三段、图库图注/链接、5纪录、完整解码照片与视觉边界一致。原HTML/JPEG不入Git，永久保留双派生JSON及CUSTODY。

7证据SOURCE、旧CN20骑乘、旧PET80发布规格、内容档案、parser与双原报告按bytes/SHA256/Git blob固定，完整7pin清单摘要另锁代码；证据被改后连receipt pin一起重算仍拒绝。固定21真实run清单摘要、准确内容HEAD/tree/候选分支、双run/job/artifact/ZIP长度与摘要，不接受缺失、等长破坏、漏门/重复/复用工件、虚报初取或双端相等、错任务/分支/HEAD、2005原字节或服务器运行抬高。逐份核schema、两HTML实际identity及初取布尔、全图固定、语义/audit与原件界限。CLI强制保管，第8单元增加所有保管反例及骑证泛化至两宠/七类别变全宠槽位矩阵/静态持物变成功穿戴的拒绝。本地最终8项及关联16项共24通过，原输入强制保管重放输出与初始local逐字相等；独立发布边界工具通过，旧文完整保留。原内容CI7项不改称8项；保管提交候选/main自身仍待实际8项及全门后验。

交付具体收益是把“持有史卡鲁”和“获族长骑乘证”分开，以及宠物类型→可用装备栏、7大类/脚子类型、属性增减的有限资料。没有宠物物种完整数值、技能/成长率、骑证原ID与实际装备事务。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-91：早期具名NPC对话/交互界面或另一地区具名宠物技能数值来源，避免连扩本报道娱乐设施/匿名图。Stage A7PARTIAL+2OPEN、B/wiki GATED、savedataR79 PAUSED_NON_BLOCKING，整体恢复百分比仍null。


### 2003-05-29 (displayed portal publication) — Mainland player guide describes Goya cave pig-letter chain [R91]
- FACT about dated guide text: Sina Games page https://games.sina.com.cn/zhqu/sta/article/2003-05-29/9803.shtml is headed as a pig-letter quest guide and displays 2003-05-29 16:24 and 网友投稿; original contributor unnamed.
- Guide account: cave youth asks for a shell, Karuta merchant gives two, youth describes one pet reward (特洛昆 or 呼拔拔), pig 乌力斯凯 entrusts letter, fourth-floor pig flower shop gives 月光花, 乌力美 takes flower and letter then gives reply on a second contact, 乌力斯凯 exchanges the reply for 红玉的手环 (+2 attack/+2 defense/-2 agility/+1 charm). Cave entrance (99,425) and footer (98,426) conflict and remain separate transcribed claims.
- HYPOTHESIS / OPEN: actual program build, original NPC scripts/word-for-word dialogue, exact runtime rules and UI, item consumption, variable pet draw chance, quest persistence, 2003 HTML byte provenance. Do not project to JSS1999, TW1.0 or worldwide first release. R55 earlier 2001 player source only overlaps the shell/pet route.
- Preservation: R91 source contract, structured seven-node guide-derived JSON and tests; no proprietary binary, screenshot, or source HTML added.


### 2003-01-08（报道页面显示）— 玩家笔下宠物个体范围、版本感受及技能（R92）

FACT **of source statement**：17173《让我来评价石器宠吧》，署名小白虎，https://news.17173.com/z/stoneage/content/2003-1-8/n852_768685.html 。文章在玩家视角区分所谓JSS早期、华义新宠、2.5/4.0叙事，提供葛雷马恩／葛雷基欧／葛雷洛比／吉比／鲁比／扑满乌力／里昂蛙／莫拉斯八具名宠的一级HP、攻、防、敏区间和「成长最高数值」说法；仅为2003玩家文献，不是已认证官方构建/宠物主表/精灵演算或真实运行。作者对4.0的PK强弱、宠物稀有度和发行历史属评价/未经独立认证，不能合并为产品发布时间或世界观正史。

具体缺失必须保留：鲁比HP [41,null]和四成长全部null、扑满乌力HP [null,61]、`10.2以上`、`12.3X`／`2.0X`等非精确数字。作者记吉比「落马」、鲁比「狂暴攻击」攻+100%／防-30%／3–10次、扑满乌力「捐献」之PK偷钱用途，不能反推原技能公式/伤害/货币转移。网页字符损坏不能自恢复宠名。

Sina另存档 https://games.sina.com.cn/zhqu/sta/2/cwzl/index.shtml 显示扑满乌力LV1体力55–61，未认证原网站入库日期与S1同build、两边不可互填或视作双官方独立实测。版本/创作与来源报告分层，不投回JSS1999或TW1.0。详情见 `docs/specs/STONEAGE-CN2003-PET-GROWTH-PLAYER-CLAIMS-SOURCE-R1.md` 与结构数据。原HTML及原宠物图未入Git。


### 日期未确认（当前可访问网页标作7.0）— 17173渔村史比武器收集与NPC对话框图 [R93]
- FACT_OF_SOURCE：当前17173“石器时代7.0-A搜集武器任务（渔村）”网页 https://news.17173.com/z/stoneage/renwu/sa70_05.htm 称史比在玛丽娜丝渔村局部(66,93)，近程五物换双尖枪（攻+53敏-12魅+6混迷的精灵LV4），远程五物换乱射弓（攻+23防-24对象10毒雾的精灵LV4），不证明原官方服务端条件或奖励。
- 内部文本冲突：正文远程“近藏的棍棒”，尾注“进藏的棍棒”；原文“混迷的精灵”保留不纠字。
- 图像观察：关联直接图 https://images.17173cdn.com/stoneage/images/mission/sa70/sa70_05/sa031027_002.jpg 可见有框NPC对话样式、“下一页”绿控件/鼠标指针及底部模式条。图片文件名不得解释为2003日期；未验证HTML内嵌链接、源图时间/原像素、NPC文字或按钮实服动作。
- OPEN：游戏正式版本/构建，原NPC物品ID，物品消费及技能实际施放，真实窗口状态与服务器交互。原HTML/版权画面未入Git；研究材料见R93规格/JSON。


### 2004-03-18 — 日版Hangame《石器时代》衍生宠物Avatar具名 [R94]
- FACT_OF_REPORT：ITmedia/RBB Today https://www.itmedia.co.jp/news/article/0403/18/1040318075/ 发布显示2004-03-18 19:22，称NHN Japan当日提供石器宠物的Hangame头像与背景；仅具名“ゴルシス”“ウポポ”“ミドリガメ”，文本总数为7款宠物Avatar+2背景、200–350日元，可跨其它Hangame游戏使用。
- 可查看的附图 https://www.itmedia.co.jp/news/article/image/0403/18/1040318075/15463/728 是卡通图像与背景拼版；没有原图哈希／原款命名一一绑定，也不是TW1.0/JSS1999原宠物客户端SPR。4款未具名不补全，7件商品不当七个确定物种。

### 2004-05-20（报道）与2004-06-03（预告日服正式服务）— ウポポ实体赠品 [R94]
- FACT_OF_REPORT：4Gamer https://www.4gamer.net/news/history/2004.05/20040520194557detail.html 2004-05-20 19:45转述BOTHTEC日服计划6月3日正式服务、5月20日盒装版开始销售，其中有两张客户端CD-ROM、两张30日票、手册和**一只ウポポ毛绒挂件**。媒体发布与服务器执行/实物拣选分开；2004-06-03不是1999首发。
- 文献性同名跨产品“ウポポ”链接2004-03 Hangame宠物Avatar和2004-05 盒装实物，不建立同游戏数值ID、同造型素材、版权许可或新世界正史。详情 R94 source规格/JSON；原图及二进制不入Git。


### 2003-07-26 至 2003-12-12（媒体页面日期）：日本复活测试版的交易界面与地图/人物计划 [R95]

- **2003-07-26**：4Gamer OGF报道 https://www.4gamer.net/news/history/2003.07/20030726001803detail.html ，采访BOTHTEC称旧JSS1999日本服将以升级形式复活，计划地图、人物和轻微UI改良，β当时预定**11月**；作者对“韩国版＋α”和普通玩家可能骑乘恐龙的评论是猜测而非执行事实。
- **2003-11-25**：4Gamer https://www.4gamer.net/news/history/2003.11/20031125203537detail.html ，BOTHTEC公告将原“11月”预定改为**12月**，报道当时不确定具体日期；不能从后报倒填11月25日已指定16日。
- **2003-12-12**：4Gamer https://www.4gamer.net/news/history/2003.12/20031212000000detail.html ，报道BOTHTEC/NHN宣布该日提供**预先下载**、**12月16日计划公开β**，并将“新增交易窗口”和其他少许UI改良归属复活版；**新增地图/新角色**为β后的另一次更新计划，并非当日已实装。网页时间标签不能强解释为午夜公告。
- OPEN：没有当年原生安装包、交易窗口动作帧/服务器ACK、客户端版本哈希、地图或角色差异原文件；不反推1999 JSS没有交易能力，也不合并台湾1.0与日服2003同build。与已有R63日本2003开发中截图按不同证据类型并列，版权图片不入库。

 
### 显示2001-06-14 — 玩家练功指南四岛／神像记录／四属性洞窟状态 [R96]
- **R96-S1**：17173《石器之练功篇（一）》，作者正伟 https://news.17173.com/z/stoneage/content/2001-6-14/n3_920052.html 。玩家描述南北岛、沙姆岛和吉鲁岛；四出生村在南北两岛。南方与北方两条练功路线汇合于霍特尔村、沙姆奇努伊、吉鲁达那。作者建议路线并非游戏原始地图强制通行顺序或等级限制。
- 该文章称村庄神像首次记录需要该村特定肉，再次不需，并决定下次登入位置。现缺原版服务器记录/背包消费及重登网络ACK，不能把该叙述当自动角色全量存盘规则。
- **属性洞窟的同期文献状态**：深红(火)、玄黄(地)、琉璃(风)在文章中“称已开放”，碧青(水)“称尚未开放”。这是2001日期标签的玩家文章说法，历史首刊原字节及部署时刻均未核实；不能拿它证明后来/更早所有版本的实际开放状态。
- **R96-S2**：17173《石器之练功篇（二）》 https://news.17173.com/z/stoneage/content/2001-6-14/n254_170616.html ，作者未知。称四岛间有三海底通道、霍特尔首次神像记录用两块奇宝肉、沙姆岛有一个村而无记录点；科奥通道需要于卡鲁它那购200stone通行证。未知三通道端点、商人身份、原物品ID；不推其他通道有同pass，也不跨版填原地图/任务数据。两页面当年原始HTML/准确build仍OPEN。


## R97 supplementary source differentiation — 2026-10-23 (currently available web catalog, historical date OPEN)

**FACT (present page text/link only):** 17173's extant `petshow.htm` links the pig-series records 001—008 in `petshow01.htm`. The extant index uses labels 007 “乌力 德” and 008 “乌力固力”; the detailed page instead says 007 “乌力莱德” and 008 “乌力布鲁”, the latter duplicating detailed 004 while reporting different element/HP values. Details 007/008 also cross-link small images `a-008.gif`/`a-007.gif` in reverse numerical order. Sources R97-S1/R97-S2. These are **website inconsistencies**, not proven original game species variants or repaired names.

**FACT (player text as text):** An extant 17173 submission labeled 2001-06-14, by 依波波, describes 乌力布鲁 and 黑乌力 as JSS prize pets. This is a player's report, not a Japanese original award register or game runtime record. Source R97-S3.

**OPEN:** date of the present pet catalog and its earliest archived form, website-to-original-pet identity binding, original image bytes/authenticity, same-build per-species PET master and whether numbering/labels were later revised. Previous independently validated TW1.0 bitmap+SPR **numeric** intersections do not close these historical claims.


### R98 source-bounded Katan handover quest comparison — 2026-10-23

**FACT about surviving guides, not certified runtime:** A current 17173 page labeled 2001-06-14 and credited to 陶陶 narrates two Katan NPC handover sequences: four Lv25 fish (first 加格＋帮恩吉, then 克邦凯斯＋加克拉) to receive a golden 修宝, and four Lv25 birds (first 火鸡＋奇宝, then 克克洛斯＋霍尔克) to receive a golden 朵拉比斯. The two page labels do not certify original build timestamps. [SRC-CN-KATAN-R98-2001-17173-TAOTAO]

**FACT about surviving 2003 player-posted source:** A Sina page labeled 2003-05-29 14:24 narrates the same two-stage paired deliveries and lists multiple illustrated-guide captions, but the accompanying original image bytes, precise client build, native NPC/script and transactional behavior were not authenticated. [SRC-CN-KATAN-R98-2003-SINA-PLAYER]

**OPEN and explicit contradiction:** S1 advises searching Katan along south 198; S2 along south 190 and claims random position, so neither is a unique spawn coordinate. S1 does not name the first fish ring and warns losing it wastes the stage; S2 names 火鸡的戒指 and claims it is reissued. S1 calls the bird-stage ring 火难戒指, S2 calls it 火鸡的戒指; stated +5 effects differ in wording. No implied equivalent original item opcode, fish/animal master, fixed despawn/give-back contract, reissue ACK or repeated task flag. Site captions are not screenshot authentication. The 2001 guide's repeat-bird-only remark includes explicit uncertainty. [SRC-CN-KATAN-R98-2001-17173-TAOTAO; SRC-CN-KATAN-R98-2003-SINA-PLAYER]



### 2026-10-23 台湾1.0早期静态NPC候选号段的资源层连接（R99）

**FACT（仅原盘资源物理层）**：台湾 Waei/JSS v1.0 同一原盘派生的 ADRN 位图和碰撞资源表，在bitmapno5846—5946间完整给出101个独立位图与101个互异map_number的准确映射，每个RD图像块SHA256不同；其资源号并非连续101号，而分两段：前74个位图5846—5919→原资源16000—16073，后27个位图5920—5946→原资源16200—16226。原SPR帧242085项中这101号静态位图的直接引用0项，不能证明它们从未用于静态绘制。[SRC-TW10-R99-ORIGINAL-NPC-CANDIDATE-MAP-RESOURCE]

**OPEN（严禁提升）**：“NPC”是2001玩家对图号段的分类，而非原官方角色选择表；`map_number` 是ADRN资源编号，并非游戏世界楼层/地图ID或NPC实体ID。原NPC人物名字、坐标、互动状态、完整原场景画面与服务端脚本依旧未知；101资源行不等于101个NPC、101个物种或真实可达场景，图像源块哈希不是版权复用许可。


### R100 卡坦具名目标与四鱼请求窗口：两张实际全图补证 — 2026-10-23

从新核GitHub main `8e2ba7f7484a406120fc6292a3578018148ec888` / tree `870b7bbff3a810aff8f1c5cd5c43358f92b5b699` 启动；完整519分支分页至不足100，0开放PR/0 in_progress，旧无关queued37642417333保留；同HEAD候选9/main8合计17个实际Actions全部success。八启动文件完整UTF8与精确checkout Git blob逐字一致；CURRENT旧前缀2517154 bytes / SHA256 `cec7cc606232a09907be8ce7f3b09bd1d74e3d5ec34403f1cba9ab3d61904745`，未依据旧聊天恢复进度。R100缺口是具名NPC实际图像关联，不延长R99静态资源列。

R98新浪S2实际HTML的第一插图表仍含原href与独立缩略图src；本次仅取首两张全图。https://games.sina.com.cn/zhqu/sta/rwgl1_6.shtml 当前53124B / SHA256 `7230667db91cc824fb6fe6b3d0a833611170a1de1e15bc23f367b623240f7b9c`，显示2003-05-29 14:24网友投稿。两个真实全图仅将http升级同主机同路径https，均200无跳转、RGB JPEG640×480单帧完整解码：232图58651B / `ace7096c3866400dd4400be5169dfaa76f73ae902e7bfb3b3bf8e9a2a76420fc`；235图70065B / `fbb31bd1726db8c25ef41005af28abbf76bfb6b6b6988bec504928e2c3a60b24`。原缩略图231/234未冒充全图。

实际逐图查看：图一沙漠、两个人形、目标标记和指针、底栏卡坦、右上MAP和局部坐标显示；图二棕框半透明对话窗、25级四鱼与两空宠物位置、窗口选项和玩家模式标志。建立当前文献图像→卡坦目标/请求对话的有限关联；不是两次独立执行，不证确认/交宠成功或失戒回补。图片尺寸不是原生分辨率认证，文件名时间不是拍摄鉴真；精确地区build、台湾1.0同版、NPC/bitmap/SPR原ID、DAT/floor与原渲染调用保持OPEN。R98五条冲突、旧图片未取历史及R99具名TW10绑定0全部不改。

交付SOURCE/LOCAL-REPLAY原样派生JSON、中文规格、解析/实际网络重放工具、7项负向测试及专用CI；完整图文顺序另以独立regex从真实HTML复核，真实两图CLI全部通过。原HTML/JPEG不入Git。候选/main远端及工件保管须按随后实际结果验收，未提前宣称。

最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-101`：转同版可认证宠物物种—SPR选择或含实体地图DAT；无新源则有限全域缺口复核，不再连续扩卡坦攻略/图组或静态资源列。Stage A7 PARTIAL+2 OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING，整体百分比null。


### R101 原台湾1.0动画槽位选择、回退与帧倒计时 — 2026-10-23

按GitHub新核main `226c3f4763448ad30ef8cc4c896128fa60a8e9bd` / tree `bc614cf032595fe9cd264a1a18c092fd50d2cc2a` 启动；完整520分支至第6页20条，0开放PR/0 in_progress，旧queued37642417333保留。R100当前HEAD候选10/main11共21实际Actions全success；八启动文件完整UTF8与fresh exact Git blob一致，CURRENT旧前缀2521980B / SHA256 `23790aede7ebce00a484d9f13fd39fd38a01c034ba34c890be37cba3d3906a3a`。最高NEXT101转原客户端选择链，不扩大卡坦图组/静态图列。

原IA目录本次元数据200，仅有整盘RAR、包装图/日志，无独立exe或field DAT；DiscMaster精确文件名搜索仍返回广泛近似项，未获得新的同版安装树来源，不把搜索响应大当命中。改直接重取既接纳CD_DIC.rar整842125501B，16并行101合法范围，MD5 b37a4a47f4eb608cac67e4ddf7a1621a与SHA1 b8cf92720b6ec8b3f46ea2e9bfcda986d21e7ded全部重新通过；BIN523449360B/hash905ee6…、exe425984B/hashcdab9e…和SPRADRN5568B/hash275b64…均重新等于旧源。并非新客户端。

实质新规则：原路径写入SPR/地址文件缓冲区→0xe730加载→0x1156cf0运行表→0x3c380对象选择。磁盘12B地址条目转换为8B运行槽，方向/动作配对按顺序取首个匹配，无匹配回退0，空组保留此前位图；动画条目16B、帧12B与磁盘头12B/帧10B分别记录。对象键0x124与最终bitmap0x80分开，尚未证S:K到对象写入路径。原上界比较保留132768含端点，而加载槽数32768；不默修比较、不保证该端点内存安全。

原加载器计时公式对正帧数为max(1,floor(duration/(16*frame_count)))，合成0帧案例保持原duration。原39065动画头零帧0、最大112帧，换算倒计时范围1—75；不是毫秒或已证FPS。10个原指令计时案例与10个选择案例同独立参考结果一致。Unicorn只跑两个限定区域、使用合成内存，明确bitmap助手0xe4e0替换零偏移/返回1、音效字段0；不是完整原客户端、真实绘制或原服。Capstone与objdump对关键分支/地址独立核对。

本地前置下载调用误用了不存在--max-seconds，改为脚本真实--deadline；libarchive因RAR字典不支持失败、apt因当前系统权限失败，改用官网真实出链的独立7-Zip成功解压，未升级权限。初静态扫描遇skipdata伪指令，改显式跳过；算术片段初漏设合成ESI导致未映射读，补齐寄存器模型后通过；加载调用窗口曾截在指令中间而被拒，改在0xd5ed指令边界停止。保留这些本地预检失败，不冒称远端失败或第一次全过。

交付中文规格、原源派生R101 JSON、工具、七项单元及专用原盘CI。本地七项与真实原字节20案例均成功；候选/main及工件保管仍须随后实际验收。原商业程序/光盘/SPR/像素不入Git。宠物/NPC名字—SPR、原包写入、真实场景/调色板、世界DAT及服务器master未获补齐。最高NEXT102 `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-102` 有限全域材料缺口复核，不在无上游身份/画面交付时继续扩渲染/音效helper。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、savedataR79 PAUSED_NON_BLOCKING，整体复原百分比null。


### 2026-10-24 — R102 研究资料整合检查（不是新增历史事件）

冻结远端main3782b518的880份顶层recovered JSON，以七字段记录核1339出现、871研究ID、883正文。12个JP2003人物位置两份正文经旧来源补充builder完全复算，不是人物改名/版本冲突；2006像素不能倒填2003同刻。CN2.0的40首批已在104目录，日服124另版独立，总228版本限定网页位置，不等于物种。26无collection先保留未路由。没有新的历史HTML/像素/原程序/服务器来源，没有改变1999/TW1事实。22领域材料与缺口复核见R102规格；最高NEXT103转早期辅助工具明确版本的新来源，非运行旧软件。


### 2003-06-18（页面所标）／2026-10-24取源 — R103 SACH-MX分版媒体列项

新浪两页分别标15:28的5.00B9会员版与15:32的6.0B1免费版；当前三HTML/双原图实际取得。作者/制作者栏SACH-MX(万宇在线)不是已认证开发者发布；专题明示隐藏工具网址且不提供下载。两页明确共有8功能类别，会员另列不限等和送货脚本；免费“大致相同”不提供逐功能同一性或缺项不存在证据。会员/免费不同收费模式与网页时间不能建立发布顺序、功能新增/删减。两静态图片支持外部工具版号/控件存在，不能倒填原TW1服务端、成功执行、客户端精确兼容或新作已采用。18列项/22研究记录不是原版实体复原计数。详见R103来源契约，2003原HTML与拍摄时点未认证。


### 2001-10-23网页／10-25与26图像存档 — R104具名图鉴视觉引用

旧北京华义CN2.0图鉴81—104页重新实取并等原SHA。原第084裘里蛙实际src104.JPG、第088沙瓦列88.JPG、第089砂鲨87.JPG，三原引用图片现已分别实际取得不同存档时刻的JPEG83×90单帧。网页时点不是发表/游戏上线，图像不是同刻或原SPR、原物种ID；图片编号不自动与网页位置相等。第088/089未声明HTML尺寸不由实测倒填。3独立视觉补充不改变104网页目录或物种分母。2008 GASH公告命名与未标名宣传图的关联被排除，未认证ゴルンフット像素。


### R105 日本2004村庄设施分批公告 — 2026-10-24

官方2004-11-03征名结束页预告11月9日维护后结果/名称反映；2004-12-07保存首页列11月9会话改善与征名结果、11月12卡拉村各设施实装、11月16新设施追加。当前同期GAME Watch11月12周报报道ミライア/カラの村名与巴士8人。计划、官网索引标题、媒体部署记述分层；详情各404，未知设施清单/坐标/旧容量/司机计数/实际运行。两研究记录不计两新地图、不跨台湾1.0或2006地名强合实体。见docs/specs/STONEAGE-JP2004-NAMED-VILLAGE-R105.md及SOURCE-R105.json。


### R106 日服2004官方宠物伴随及技能管理 — 2026-10-24

2004-11-06保存官网手册明确宠物技能不能直接遗忘、允许另一技覆盖、不能重排；原野「おさんぽ」以伴游为目的，低忠诚度/邮件状态禁用，特殊宠物店进入条件未详。定性阻断规则不等于充分可用条件，不能套大陆忠诚度阈值/战斗旅途伙伴或原TW1字段。两研究记录不当全技能名册/实测原服。三图及八映射只有HTML，伴随图请求404，#osanpo无真实锚点。见R106 SOURCE、LOCAL、独立审计与规格。


### R107 2003大陆赛事宠物奖励与华义大财神领奖位置 — 2026-10-24资料补充

**SOURCE / ANNOUNCEMENT:** [Sina 石器时代大赛公告](https://games.sina.com.cn/zhuanqu/sa/gonggao.shtml) 保存「金暴领取通知(4/11)」等当时组委会口吻公告文本；此为媒体托管文献，未认证华义原域字节或2003网页捕获。正文显示2003-04-11开始向符合参赛标准并积极配合的初赛玩家赠送金暴一只，发放场所表述为「每个服务器最后一个星系村长家的华义大财神处」。相应NPC标签/赛事资格/奖励名称分开登记，不证明实际执行、独立原服NPC ID或发行于台湾1.0。

**SOURCE CONFLICT / OPEN:** 两条复赛奖品选择通知分别写截至2003-04-21 09:00与2003-04-22，原文并存且未获运营方更正，不将其静默校正。此复赛白虎/魔法兽二选一的项目不能和初赛金暴领奖合成同一任务；大会实体/现金奖不当游戏奖励。详细机器对象见 `research/recovered/STONEAGE-CN2003-TOURNAMENT-REWARD-R107.json`，来源等级为网页文本展示（原字节SHA null）、所有原游戏ID null。


## 2026-10-24 R108 日本2006跨玩家同服捕宠活动有界证据

以本轮新核远端main `e7ad36ff4862138d0f5fa82e158bf945f21846ec` / tree `4ed6d6ba1c27f14ed82696a601b75cdb493d01e8` 和全部连续性状态为基线，上一R107在主线且已核main近期9项Actions completed/success、无开放PR及in_progress。CURRENT原生Git blob非空，精确sha `87665403d02ddbe9395c4cc98b42ba307e7b31c2`；四长历史全文已读取，未使用旧聊天SHA推断。

按最高NEXT108轮换不同年代/地区。同期2006-05-23 18:16 4Gamer编辑署名noguchi报道日服运营GaiaX举办「GMからの挑戦状 ～ダイノ ゲッターズ～」，计划2006-05-23—06-06在「カルターナの村」由三名**未记姓名**NPC接收指定恐龙并获get points；下級／中級／上級分档捕获难度与分值不同，积分按**同服务器全体玩家**累计，目标达成时有面向该服玩家奖励的报道。这是单服共同贡献激励，不同于CN2003的个人参赛领奖与已入库JP2005集章；严格未认定NPC姓名/原ID、具体恐龙与分值、阈值、真实发奖或服务器实现。

新四条研究资料记录和规格 `docs/specs/STONEAGE-JP2006-DINO-GETTERS-R108.md`，派生 `research/recovered/STONEAGE-JP2006-DINO-GETTERS-R108.json`、元数据验证器、15个变异反例+1正例及专用CI。来源仅当前网页**文本层**可读，执行环境未取得原HTML字节/历史存档/官方原公告，SHA和真实运行证据保持null；新测试即使绿色也不是byte-exact网页重放或原服事务。无版权网页/图像/程序入Git。候选和main远端CI/保管需以真实后验另记，不提前报成功。

有限止于一份2006媒体报道、四记录、无新增原服实体或产线；需档案官网、NPC交互图、同服积分日志或服务端实证才重开细节。**最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-109`** 换另一具名NPC故事或真实交互视觉，不持续挖单服活动猜阈值。Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、TW1同构建NPC/SPR与服务端事务仍OPEN、savedataR79 PAUSED_NON_BLOCKING，整体恢复百分比null。


### 2026-10-24 R109 CN2003/2006金飞航空资料交叉归档

来源S1新浪2003-06-03 17:04 https://games.sina.com.cn/zhqu/sta/article/2003-06-03/10634.shtml 是同期媒体玩家攻略；来源S2 17173署名┗庙街★Tim┓于2006-05-14的自称“8.0”玩家稿 https://news.17173.com/z/stoneage/content/2006-05-14/1147617360.shtml。均仅网页文本可读，无原HTML bytes/hash/历史捕获、同商业build或实际任务日志。S1具名打工名人克拉克、霍特雷敦、PC盗贼团老大、飞龙总教练布鲁斯，罗丽小姐仅图注，原生NPC/地图坐标和视觉身份全null。四飞龙帖拉格恩、洛卡伦恩、加宝格恩、朵拉比斯及布兰恩002按原文保存，不补物种主表/SPR/成长。伊甸寻根/尼斯故乡仅文献叙事，飞龙航空1万旅费、交报告20万石币与转生重解仅S1主张，未验证事务。

同一S1存在交一只/备或需三只互相冲突；S2另一时点玩家文写一只，不能反向裁定S1。S1“80级”与S2“80级以上(不包含80级)”版本对照保留。10项分版研究记录和规格 `docs/specs/STONEAGE-CN2003-2006-DRAGON-FLIGHT-R109.md` 已由候选专用run40048210484 PASS元数据CI，不作HTML字节重放、原服执行或初代故事认证。版权HTML/图片/程序不入Git；Stage A仍7 PARTIAL+2 OPEN，B/wiki GATED，R79暂停，百分比null。

最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-110`：轮换新的第一方具名NPC剧情或带身份交互视觉、早期地图实体源，不持续扩金飞攻略。原候选内容commit `208b2af542cea42fb5f64ccab1c22e881af1c696`，连续性追加另提交，候选/main总CI需真实后验。

### R110 2026-10-24 日本2004圣诞具名NPC/队友误伤规则的来源限定补证

按fresh远端main e928f525f6c6f7a5b0aa4e0bd706405ae8d0f948与历史不缺损原则，选择尚未入库的日本2004季节NPC及战斗防误伤报道，明确区别大陆2003圣诞与日本2005集章。4Gamer S1 <https://www.4gamer.net/news/history/2004.12/20041215210314detail.html> 2004-12-15称圣诞2004-12-20至27/「成人の儀」完成者得礼，新年2005-01-01至07神社抽「おみくじ」、参加无限制但结果影响未知；GAME Watch S2 <https://game.watch.impress.co.jp/docs/20041224/on1224.htm> 于2004-12-18至24周报称「サンタガール」出没マリナス/ジャジャ/カルターナ/サムギル四村，找到可得礼，报道12月20日把自队成员（包括宠物）遭己方攻击通常伤害统一1，混乱例外正常伤害，并称新增圣诞NPC和物品。S2不述成人条件不等于免资格、S1泛称圣诞老人不直接证明S2女圣诞NPC同一原游戏实体。

S1运营者栏ボーステック与S2栏ガマニアデジタルエンターテインメント不同，不能无合约证据归并运营/平台/支付责任或宣称2004-12换运营。S2一方旧URL http://stoneage.to/event/Xmas04.html 当前不能获取原HTML或档案；两报道均是同期媒体转述，不具原运营文bytes、SHA、截图、主表、完整构建或服务器事务证据。任何「四村」不当四张新地图、NPC名字不当原像素SPR、礼品身份/发放次数未知；1伤害只保留条件句，不迁移TW1.0或补自身运行成功。版权原HTML/图片/程序不入Git。

六项研究记录及规格 `docs/specs/STONEAGE-JP2004-XMAS-PARTY-COMBAT-R110.md`、派生JSON/校验器/21单元/独立CI已提交候选，内容与历史候选/主线实际验收以后验为准，不能提前报成功。最高NEXT `OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-111` 返回其它地区/年代的具名故事与真实可归属画面或第一方地图实体，不继续扩节日赠奖/友伤helper。Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、总复原百分比null。


### 2026-10-24 R111 2009-10-19 日本DigiPark十周年第三弹公告中具名NPC「レテ」

4Gamer网页 https://www.4gamer.net/games/013/G001377/20091019025/ 于2009-10-19 19:49刊出“メーカー発表文の内容をそのまま掲載”，署DigiPark；今仅文字网页可读，**无原2009 HTML字节/捕获或发布时同刻像素**，不能称服务器真的按时开。10-20维护后至11-04维护前预告「ミステリーダンジョン」；聊天室NPC「レテ」对话进场、十房答题、错一题送回聊天室并从头、通关有未名奖物、洞内无敌对恐龙；未证十地图DAT、原回答/物品ID、任何其它战斗关闭或早期TW1身份。相邻第一/二弹仅背景不新增本轮系统。4Gamer真实缩略URL TN/002.jpg网页已查看但未下载字节/验图名到具体NPC像素，禁止SPR绑定。6来源记录见 `research/recovered/STONEAGE-JP2009-MYSTERY-DUNGEON-R111.json`，候选内容 `5ee78dc02cac14b407ce099f54ccdc4a8fc6356e` 专用CI run40051427341成功，非原服实测。最高NEXT R112转更早分版一手NPC故事或具名场景。Stage A7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79暂停、总百分比null。


### 2001-02-06/14、02-17（转载所称）— R112大陆华义早期GM聊天室领奖与好友名片跨服风险；2026-10-24登记

**转载层，不是原运营现场记录**：SHIQI.ME于2016-02-12发布的旧闻汇编 <https://www.shiqi.me/pt_25.htm> 转载“华义公告”称2001-02-06情人节报名预告、02-14六服务器聊天室中奖者与GM交换名片经核验领奖（玉之骨/黑玉/深翠及四种纪念品标签），以及02-17按人物等级带迁移世纪互联1→7时可能丢失部分好友名片并称给予1000石币。活动具体聊天室、原文时刻、显示等级表在R112规格逐项锁定。**未取得2001官方原站字节、同时期独立照片/公告、原服事件日志或日期执行核验**，故不是已确认2001实际交付、聊天地图原ID或名片保存语义。中奖者账号及人物昵称不复制。2001大陆运营与1999 JSS/台湾1.0不同版本，且本活动的GM不是2009日服「レテ」NPC。历史事实结论保持“2016转载作出这些2001主张”，原一手事件仍OPEN。


### 2002-05-20玩家记述／2004-07-02媒体旧版本页 — R113 2.5精灵王故事材料（2026-10-24归档）

S2 17173柯南2002-05-20当时玩家稿https://news.17173.com/z/stoneage/content/2002-5-20/n855_771416.html 叙述救新藏、红蛙卡卡金宝、黑蛙王金珠／黑玉交换、玛蕾菲雅与精灵王任务，为独立作者回忆而非原服验证。S1媒体现存2004-07-02《石器时代2.5版 精灵王传说》详解https://news.17173.com/z/stoneage/banben/sa10/39.htm 展示机械文明与双王、失忆精灵救援、天岛与萨姆吉尔／玛丽娜丝、三地形诞生世界史；未取得2002华义原官网HTML或构建。S1的/42.htm人物章节同文不算新独立见证。

内部封印矛盾「黑王自行封印」与「光王封印黑王」并存；“一千五百年前／二千年／十年前／五十年前”为各自叙述参照而非世界公历；S1“凤为信”、S2“风为信”原字并存。新藏兄弟愿藏／原藏、新臧异文不纠错、不与游戏原ID强绑定。2.5时期故事设定不倒填JSS1999/TW1.0初始世界事实，相关版本条目详R113 JSON和中文规格。



### 2026-10-24 R114 — 新浪游戏2003《富商的货物》捕宠与忠诚奖励任务（来源限定）
按远端main 33091550d0a2beed10e2bccfe8d97b0ff765080a/tree b727d344c3546001f869b8b0e13e541873a9fbc2 核验启动，旧R89已归档台湾2000人物报道，本轮选择未入库Sina同期攻略 https://games.sina.com.cn/z/sta/rwgl/fs.shtml?from=wap （新浪游戏、2003-06-30 11:55）。同站较晚目录 https://games.sina.com.cn/z/sta/2004-10-15/180146.shtml?from=wap 把题目列在6.0栏，属后期版本分类不是2003补丁、精确客户端或原服构建证明。2018转载 https://www.shiqiso.com/sq/160.htm 非当年独立目击，不能据其LV55+硬门槛或懒人传送覆盖同期原文。
S1所述：成人礼是条件，55级以上与福尔德/达那羽毛均为建议；沙姆岛奇努伊村「盖落比」(原文「54。76」)给「富商的货物」，去吉鲁岛「5X级小象区」抓LV60「巨大玛恩摩」，正文称抓到后货物消失，回报段写「盖洛比」并得「宠物忠诚肉片」（忠诚度+10），称可重做。HP低于100比较好抓为玩家建议，不是捕获概率原公式。两种NPC写法并存，原ID未知不能默合；原HTML字节/原始九图像素、原NPC/地图/宠物/物品主表和捕获/物品消耗/奖励/保存事务均OPEN；不反填JSS1999/TW1.0，不把文字记录算原游戏实体。
成果 docs/specs/STONEAGE-CN2003-MERCHANT-ELEPHANT-R114.md、research/recovered/STONEAGE-CN2003-MERCHANT-ELEPHANT-R114.json、校验器、28项测试与CI。候选内容commit 0f468798056679a39324975bb6578c3f27e512cb/tree c600685e62bbb6495c5e1751a5eeedd1eed407cd，专用run40055929518 completed/success，仅证明元数据边界测试，非当年HTML重放或原服任务执行。版权所有HTML/图/商业代码不入Git。
最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-115：轮换1999–2003另一地区真正同版具名NPC/宠物视觉原件；否则有限复核22域缺口，不扩大本任务helper。Stage A7 PARTIAL+2 OPEN，B/wiki GATED，R79暂停，整体恢复百分比null。原历史前缀全部保留。



### 2003-09-11 — R115 大陆中秋任务媒体页面「华义」署名（2026-10-24归档）
准确可访问来源为17173《任务攻略:石器时代中秋任务》 <https://news.17173.com/z/stoneage/content/2003-9-11/n631_547722.html>，页面日期2003-09-11、作者栏「华义」。FACT仅到**现存媒体档案署名与正文**，未取得同时刻运营原官网HTML/署名验证/服务端脚本或部署记录；不把本页自动认证为独立一手运营原件。
文献叙事：后羿委托将月饼送嫦娥，下界月兔捉迷藏获取柚子，月宫需字面「**」相关许可与引路（原站脱敏字符不猜恢复）；称可反复完成、随机得到变身镜子lv1（一分钟变成自己的宠物）、宠物技能罐头（字面旅途伙伴2与狂乱暴走，但不知是两罐还是一罐）、爱相随戒指（设好友、10次）或14–16级精灵武器装备的一件。随机概率/独立奖励组合、原ID/地图DAT/动态形象、原服变量与交易全部UNKNOWN；三人物标签不计已定位原NPC；2003节令故事不可回灌JSS1999/TW1.0普遍世界年表。同站“石器中秋任务开放及奖品追加”相关推荐路径不能解析为有证实的第二来源，6.0精确发行标签暂不采纳。导出资料、规格、边界回归见 R115 JSON/MD；本轮只是档案源契约，不称当年成功领取。


### 2026-10-24 — R116资料分档订正，不是历史首发事实
现行main1a5bb8d的924份顶层研究JSON冻结复核，73次任务集合记录投影对应49个研究ID，15运营活动上下文与34起源待考独立检索。赛事领奖、节令任务、协力条件与新年占卜不进入本体任务已证目录；后续常设奖励不改变原活动起源。原六组源级覆层不与记录ID相加，不把同文迁服规则也当情人节NPC任务。没有新增1999/TW1原任务、永久性或首发日期事实；同build脚本、任务ID/地图/NPC资源桥及事务均OPEN。详R116规格与固定源派生报告。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停，总体百分比null。


## 2026-10-24增补 — JSS写于1999–2000年的更新主张与合作活动期限

第一方verup.html的2001年档案保存1999–2000运营更新史，不能把2001捕获当1999实测。R116新增语义归档：1999-10-18ウリウリ取两贝壳缺陷修正；2000-04-10 SJOT相关NPC设定修正、04-17合作SJOT结束；04-24合作寻宝开始且称限一个月，同日玄黄洞窟进程修正；05-08クイズ道場台词修正、05-29内部可继续前进；08-28转生追加。合作寻宝与SJOT归运营活动文献，其他四具名条目仍起源待考，不可当最初版任务或永久任务已证，也不由邻近美容推广/聊天室期限代定属性。

同源13条未名事件追加不构成13任务普查。新读faqquest目的页无任务正文，只有系统/截图说明且体验版问答注释隐藏。限定来源、时序、冲突与源SHA见 docs/specs/STONEAGE-JSS-EARLY-QUEST-ORIGINS-R116.md；原商业服脚本、ID、任务奖品、世界线因果和运行仍OPEN，所有先前历史原文保留。


### 2026-10-24 R117 — 成人礼“文献存在时间”与“发行起源”的区别
既验2001-11-20新浪原快照支持成人任务完整选段最迟当时存在，不证明1999或台湾首发。2000-06-13 Google Groups仅搜索索引候选，本轮open不可用/直接HTTP429，无原消息头/正文/独立定年，仍不认证该日期。日服2004媒体圣诞前置「成人の儀」不把成人任务归为节令活动，也不证跨区同任务/原ID或永久/首发。JSS2000玄黄洞窟修正与成人礼不合并。R117起源仍ORIGIN_UNRESOLVED，原奖励/流程冲突保留，新增本体/永久/原服实体0。旧原件保管与完整历史不变，详R117资格规格。


### 2026-10-24 R117取源日志范围更正（归属结论不变）
复核工具调用顺序：Google Groups直接HTTP实际429后，没有第二次直接HTTP请求；另有一次网页工具open仍不可用。初版“429后不重试”及retry_after_429=false表述过宽，现由R117报告attempt_log_correction明确订正为additional_direct_http_attempts_after_429=0、additional_web_open_after_direct_429=1/UNAVAILABLE。原记录Git历史和四大连续性旧前缀保留；未取得消息头/正文/源字节，未晋级2000日期或本体/永久，原结论不变。


## 2026-10-24 — 已保存客户端字节重新取得（研究操作日期）
FACT：source run40067698285/HEAD2c93130f实际原包下载、摘要校验与台湾383核心/混合桥接2302文件重哈希通过，235台湾文件/237桥接路径完全匹配。唯一派生JSON与完整来源收据永久保管；这不是新的历史发行发现。2.5未获纯净官方认证；本job未重跑旧资源记录级diff，不证明原服务器任务、宠物主表或程序执行。原件临时清理而非持久归档。


## 2026-10-24 — TW8.5后期保存安装器的真实MSI载荷（研究操作，非发行日期）
旧档实际已有六卷/WAYI署名包装器/2007签名时间及Windows ISx的MSI摘要；前轮“只有metadata”描述现订正，原记录保留。新Linux静态解码得到完全相同MSI，再实际解档557文件1808555613B，MSI产品8.50.0000/華義國際/石器時代 魔域大冒險；文件名日期不是发行日，旧签名完整信任链未通过。42数字地图DAT候选与3BGM辅助DAT分开，非45世界地图。完整清单/五表/来源收据永久保存，不证早期任务宠物或1999/TW1本体内容。


## 2026-10-24 — 大陆5.0历史原件载荷范围升级（仅文件字节/安装路径）
FACT / 实物：以既有Stoneage-5档案光盘BYTE/CUE+MSI为输入，2026-10-24新source Actions实际全量读取DATA1.CAB 612,584,670B（SHA256 cb414ad1ef4cc7925ec429ec088d0146892834c72667d1af82c8075d09f1683b），静态提取413条文件共1,211,040,029B，逐项同原CAB目录大小吻合。历史旧发现“仅CAB元数据/有限前缀”描述原前期阶段，并未被删除；此条为有日期的后续增补。
FACT / 比较：MSI File、Component和Directory可使413 CAB键对应413安装路径；对台湾1.0同路径362中361字节同一、StoneAge.exe一条异；对WAEI8.5同路径407条全部字节同一。记录级容器内容、服务器任务、NPC与成长公式未因此获证。见SOURCE-REGISTRY新取证附录及两份永久派生JSON。
OPEN / 原载体出厂鉴真与发行日期、原服内容仍未知；Archive标注和ProductVersion不反推为原盘认证或历史各运营端相同部署。
