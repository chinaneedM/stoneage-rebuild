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

