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

**RESEARCH CONSEQUENCE:** Exact named cover-disc issues and contemporaneous installed-tree/cache backups now outrank broad Waei-domain filename searches as the next Mainland 2001–2002 recovery surface.




### 2002-01-20 onward — Mainland 2.5 physical client carriers

**FACT / contemporaneous product surface:** The 17173 2.5 product page identifies **延年益兽包** and **春满钱坤包** as products containing a **StoneAge 2.5 client CD**, and states that the **2.5新手报到包** existed in **three package variants**. Combined with the contemporaneous 17173/Sina rollout records placing retail launch on **2002-01-20**, these are concrete operator-era physical-carrier classes for complete-client recovery. [`SRC-CN-2002-17173-SA25-PRODUCT-01`] [`SRC-CN-2002-17173-SA25-UPGRADE-01`] [`SRC-CN-2002-SINA-SA25-UPGRADE-01`]

**MODERN COLLECTOR CONTROL:** A surviving 2020 Bahamut collector article documents the same 2.5 package family, including many new-user cover variants, a green WGS gift box and a simplified client package. This is useful for visual identification of surviving media but is not contemporaneous proof of disc bytes. [`SRC-CN-2020-BAHAMUT-SA25-CLIENT-PACKAGES-01`]

**RECOVERY CONSEQUENCE:** Prioritize public read-only ISO/file-tree recovery from these source-named client-CD package families. Package artwork alone cannot establish pressing identity or byte equivalence.

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

**RECOVERY STATUS:** the source page survives and historical page captures are known, but the exact CGI response/payload body is not indexed on the tested Wayback route. Exact Internet Archive filename/stem searches expose no carrier. DiscMaster broad `samap` hits are overwhelmingly unrelated; only an exact leaf-name match to `samap_1220.zip` is now allowed to count as a strict preservation candidate.

**RESEARCH CONSEQUENCE:** this target is earlier than the 2001-11-27 `Estoneage2.0map_1127.exe` package and therefore becomes the first recovery attempt for moving the field-map byte-provenance anchor earlier. If recovered, its archive contents must be hashed and compared directly against Taiwan v1.0, the 2001 package if later recovered, the June-2003 historical corpus, and the mixed-2.5 corpus before any equivalence claim is made.

**EVIDENCE BOUNDARY:** the surviving Sina record proves the distribution token and package label, not the byte identity, cleanliness, operator authorship, or actual map contents of the ZIP.

## 2001-11 — Mainland Sina full-map and 2.0-client recovery tokens

**FACT / 2001-11-02 client record:** Sina's surviving download page identifies `石器时代2.0客户端`, dated **2001-11-02**, with stated size **524377K** and text describing it as an upgraded StoneAge client for existing users. The surviving local-download href resolves to the exact token `col=demo&aid=41967&filename=stoneage2.0setup.exe&size=524377`. [SRC-CN-2001-SINA-SA20-CLIENT-01]

**FACT / 2001-11-27 complete-map record:** Sina's surviving page identifies `《石器时代》全地图`, dated **2001-11-27**, size **1911K**, contributed by `xinhaonanhai`. It instructs users to place the unpacked files under the StoneAge directory and explicitly states **“1.X，2.0通用”**. The surviving download href resolves to `col=map&aid=43172&filename=Estoneage2.0map_1127.exe&size=1911`. [SRC-CN-2001-SINA-FULLMAP-01]

**RECOVERY STATUS:** the exact filenames and CGI identities are now recovered, but no verified payload body has yet been found in tested Wayback, Internet Archive, DiscMaster, or contributor-domain surfaces. Therefore this is a precise **TARGET-A recovery token**, not yet a byte-provenance anchor.

**RESEARCH CONSEQUENCE:** this 2001 full-map target supersedes the 2002-11-08 4.0 map package as the earliest concrete complete-map recovery lead. If recovered, its DAT corpus must be compared directly against Taiwan v1.0, June-2003 and mixed-2.5 states before any historical equivalence is asserted.
