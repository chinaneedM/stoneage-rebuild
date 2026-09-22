# Source Registry

This is the canonical ledger for historical sources. Entries should record provenance, date, source type, what the source proves, and what it does **not** prove.

## Confidence scale

- **S** — primary original artifact: verified client/binary, manual, packaging, official site/patch file.
- **A** — contemporaneous reputable press or archived first-party material.
- **B** — strong secondary source, later official retrospective, or well-provenanced community preservation.
- **C** — community recollection/repost; useful lead, not sufficient alone for decisive claims.

## Initial leads

### SRC-JP-1999-PRELAUNCH-01

- Type: contemporaneous Japanese magazine / press material
- Period: 1999 pre-launch
- Confidence: A
- Status: partially resolved into specific records below; page-level archival capture still needed
- Relevance: earliest known concept-stage descriptions, screenshots, intended gameplay emphasis.

### SRC-JP-1999-BETA-01

- Type: contemporaneous Japanese beta announcement/coverage
- Period: 1999-09
- Confidence: A
- Status: beta dates and 1999-08-20 application deadline now supported by `SRC-JP-1999-PLAYONLINE-015`; client binary still not recovered
- Relevance: proves existence of a public/recruited beta and narrows first recoverable client target.

### SRC-JP-1999-RETAIL-01

- Type: JSS first-edition retail package / CD-ROM evidence
- Period: 1999 launch
- Confidence: S if physical media can be acquired or imaged with provenance; otherwise B/A/C depending record
- Status: concrete surviving first-edition package lead recorded as `SRC-JP-1999-RETAIL-MERCARI-01`; contemporaneous retail advertisement evidence recorded as `SRC-JP-1999-AD-YAHOO-01`; archived official Gamer's Dream product page recorded as `SRC-JP-GD-STONEAGE-INTRO-ARCHIVE-01`; archived JSS manual now independently confirms normal game-CD installation and a CD NUMBER card; original verified game-disc image still missing
- Relevance: top-priority launch artifact.

### SRC-JP-2003-REVIVAL-01

- Type: Japanese revival client / press coverage
- Period: 2003
- Confidence: A/S depending artifact
- Status: historically useful near-relative, but not equivalent to 1999 launch
- Relevance: may preserve substantial earlier code/assets and can become a diff anchor if recovered.

### SRC-TW-2000-EARLY-01

- Type: early Taiwan launch material
- Period: 2000
- Confidence: A/B depending individual artifact
- Status: needs systematic recovery
- Relevance: first major localization/evolution branch to compare against JSS.

### SRC-CN-1.82-01

- Type: Mainland China 1.82 client/data/source candidates
- Period: early Mainland era
- Confidence: unresolved per artifact
- Status: several community references exist; provenance must be checked before treating any package as canonical
- Relevance: childhood/reference baseline and major diff target.

## Structured source records — 2026-09-18 pass

### SRC-JP-1999-PCWATCH-TGS-SPRING

- Title: `東京ゲームショウ'99春　レポート`
- Original date: 1999-03-19
- Retrieval date: 2026-09-18
- Language/region: Japanese / Japan
- Source type: contemporaneous PC Watch press report
- URL: https://pc.watch.impress.co.jp/docs/article/990319/tgs.htm
- Confidence: **A**
- Supports:
  - `STONEAGE` was already being publicly exhibited by Tokyo Game Show '99 Spring;
  - PC Watch described it as the third Gamer's Dream title and as a somewhat comical game set in a prehistoric era;
  - Gamer's Dream was an NTT Data booth/platform context at that event.
- Does not support:
  - exact client build/version shown at the booth;
  - whether the exhibited build was distributed outside the event;
  - final retail contents.

### SRC-JP-1999-PLAYONLINE-012

- Title: `Play Online`, Issue 012 (May 1999), Gamer's Dream / STONEAGE coverage
- Original date: 1999-05
- Retrieval date: 2026-09-18
- Language/region: Japanese / Japan
- Source type: contemporaneous magazine scan, preserved on a third-party host
- URL: https://www.kingpin.info/download/kingpin/media/magazine/Play_Online_Issue_012_%28Japanese%29_1999-05.pdf
- Confidence: **A** for the contemporaneous printed content; host provenance still needs archival notes
- Supports:
  - Japan System Supply was developing `STONEAGE` by May 1999.
  - The published pre-launch concept emphasized a relaxed Stone Age RPG rather than war-centered play.
  - Food/resources and community were explicitly part of the published design description.
  - The scan's indexed contemporaneous text describes **village growth / community formation** as a central player activity.
  - It names **hunting, gathering and farming** as intended life/resource activities used to secure food/resources and support village development.
  - It describes player cooperation and differing roles within the community as part of the intended play structure.
  - It explicitly frames the design as trying to minimize the usual network-game emphasis on **fighting, destroying and taking from others**, reinforcing the cooperative/non-destructive pre-launch design target.
  - A summer 1999 service start was then being targeted.
- Evidence interpretation:
  - these are **published May-1999 design intentions**, valuable for reconstructing the original concept and for testing recovered beta/retail builds;
  - each mechanic must be verified separately against September beta, October retail and JSS update-state evidence before being labeled a shipped gameplay feature.
- Does not support:
  - that hunting/gathering/farming, village-development systems or role mechanics shipped unchanged—or at all—in the September beta or October retail release;
  - that a design goal of minimizing fighting/destruction meant combat was absent;
  - exact executable/client version numbers;
  - final retail package contents.
- Follow-up: capture exact page number(s), scan metadata, and stable archival copy/hash where legally appropriate.

### SRC-JP-1999-PLAYONLINE-015

- Title: `Play Online`, Issue 015 (September 1999), STONEAGE beta tester coverage
- Original date: 1999-09
- Retrieval date: 2026-09-18
- Language/region: Japanese / Japan
- Source type: contemporaneous magazine scan, preserved on a third-party host
- URL: https://www.kingpin.info/download/kingpin/media/magazine/Play_Online_Issue_015_%28Japanese%29_1999-09.pdf
- Confidence: **A** for the contemporaneous printed content; host provenance still needs archival notes
- Supports:
  - a `STONEAGE` beta test period from **1999-09-01 through 1999-09-30**;
  - *Play Online* readers being allocated 200 tester accounts;
  - beta application deadline **1999-08-20**;
  - application via a form and lottery selection when oversubscribed;
  - existence of a distributable beta-era client before commercial launch.
- Page-level recovery note:
  - the preserved page includes an application-form / game-homepage information block;
  - search extraction has narrowed the printed beta-application URL to host `www.dp.gamersdream.ne.jp` and path tail `PO/sa_apply.html`, while one character immediately before `PO` remains visually/OCR ambiguous and is not normalized as fact.
- Independent preservation route:
  - Retromags file record: https://www.retromags.com/files/file/7018-play-online-no015-september-1999/
  - submitted 2023-12-14 by `kitsunebi`;
  - release filename: `Play Online No.015 (September 1999).cbr`;
  - listed file size: **349 MB**;
  - listed MD5: **`e009cc707810c4361c849f26248593af`**;
  - the public download flow resolves to a Retromags seedbox copy, giving a concrete second scan-body route rather than merely a catalog entry.
- Current retrieval limitation:
  - this environment can reach the Retromags file/download pages and resolve the final seedbox target, but cannot resolve the seedbox host itself; therefore the second scan body has not yet been visually compared with the Kingpin copy.
- Does not support yet:
  - beta installer filename;
  - exact client distribution mechanism/media;
  - checksums or internal version number;
  - exact beta-to-retail differences.
- Follow-up: prioritize August 1999 Gamer's Dream/JSS archive captures, recover the printed application/game URLs, then recover beta client/media or contemporaneous install instructions.

### SRC-JP-1999-PCWATCH-TGS-AUTUMN

- Title: `東京ゲームショウ '99秋レポート　PCゲーム編`
- Original date: 1999-09-17
- Retrieval date: 2026-09-18
- Language/region: Japanese / Japan
- Source type: contemporaneous PC Watch press report
- URL: https://pc.watch.impress.co.jp/docs/article/990917/game02.htm
- Confidence: **A**
- Supports:
  - `STONEAGE` was shown at the Gamer's Dream booth at Tokyo Game Show '99 Autumn;
  - Japan System Supply was the publisher named in the report;
  - **1999-10-15** was the stated scheduled release date;
  - the contemporary pitch included living as a Stone Age inhabitant, hunting dinosaurs, chatting with players, and adventuring with companions in a gentle atmosphere.
- Does not support:
  - by itself, that the scheduled date was actually met;
  - retail disc contents/version metadata.

### SRC-JP-1999-AD-YAHOO-01

- Title: `当時物 PC ストーンエイジ StoneAge ブルースフィア BLUE SPHERE 雑誌 広告`
- Original artifact period: 1999; photographed advertisement is contemporaneous in content
- Retrieval date: 2026-09-18
- Language/region: Japanese / Japan
- Source type: marketplace photographs of a period magazine advertisement
- Listing URL: https://auctions.yahoo.co.jp/jp/auction/k1223621478
- Preserved original-image targets exposed by the listing:
  1. https://auctions.c.yimg.jp/images.auctions.yahoo.co.jp/image/dr000/auc0203/user/fee46e07a796172ff30e16da835b56acd5220ffd85dfadd54285b067cf6812d6/i-img1200x780-17739912563485qf7usl8048.jpg
  2. https://auctions.c.yimg.jp/images.auctions.yahoo.co.jp/image/dr000/auc0203/user/fee46e07a796172ff30e16da835b56acd5220ffd85dfadd54285b067cf6812d6/i-img1200x764-177399125637239rvonr8048.jpg
- Image evidence: the Yahoo Auctions photographs preserve the period advertisement at approximately 1200-pixel width, reducing dependence on the marketplace page renderer itself
- Confidence: **B** for the legible contemporaneous advertisement content shown in photographs; not S because the project has not directly inspected/archived the original publication page
- Supports directly from visible advertisement text:
  - Windows 95/98 as the advertised platform;
  - **1999-10-15** as the scheduled release date;
  - planned retail price **8,800 yen before tax**;
  - Japan System Supply's period web address `http://www.titan.co.jp/`;
  - Gamer's Dream's period web address `http://www.gamersdream.ne.jp/`;
  - an original mug was advertised as a reservation bonus;
  - an initial-edition `STONEAGE` special CD was advertised as an initial bonus/feature.
- Research value:
  - independently corroborates the first-edition bonus-CD lead seen in `SRC-JP-1999-RETAIL-MERCARI-01`;
  - supplies exact period domains for archived-site recovery attempts;
  - narrows package identification through platform and price metadata.
- Does not support:
  - exact contents of the special CD;
  - whether the special CD is the game client disc or an additional bonus disc;
  - executable version, hashes, disc matrix identifiers, or final package layout.
- Follow-up:
  - locate the original magazine issue/page if possible;
  - recover archived snapshots of `titan.co.jp` and `gamersdream.ne.jp` around August-October 1999;
  - search surviving first-edition packages for the advertised special CD and establish its relationship to the install/client media.

### SRC-JP-GD-INDEX-ARCHIVE-01

- Title: Gamer's Dream archived index
- Original site period: 1999-2001
- Retrieval date: 2026-09-18
- Language/region: Japanese / Japan
- Source type: Internet Archive Wayback capture of original NTT Data Gamer's Dream site
- Archived URL: https://web.archive.org/web/20001204061300/http://www.dp.gamersdream.ne.jp/index.html
- Confidence: **A**
- Supports:
  - the original Gamer's Dream site was archived under the host `www.dp.gamersdream.ne.jp`;
  - Wayback reports captures for the index path beginning **1999-04-22**, before the StoneAge beta and commercial launch;
  - later preserved site navigation includes StoneAge-specific service/status, title-introduction, special/article and account/service paths.
- Research value:
  - proves that pre-beta/pre-launch Gamer's Dream snapshots exist in the archive and should be mined path-by-path rather than assuming the 1999 web material is completely lost.
- Does not support by itself:
  - content of a particular 1999 capture;
  - the beta installer filename or download mechanism.

### SRC-JP-GD-STONEAGE-INTRO-ARCHIVE-01

- Title: archived Gamer's Dream `STONEAGE` title introduction/product page
- Wayback capture date: 2001-01-28
- Original page period: page describes the JSS 1999 commercial product; exact first publication date not yet established
- Retrieval date: 2026-09-18
- Language/region: Japanese / Japan
- Source type: archived first-party NTT Data/Gamer's Dream page
- Archived URL: https://web.archive.org/web/20010128123900/http://www.dp.gamersdream.ne.jp/intro/intro_sa.html
- Confidence: **A**
- Supports directly:
  - genre: RPG;
  - Japan System Supply attribution;
  - package price: 8,800 yen;
  - release date: **1999-10-15**;
  - CPU: MMX Pentium 200 MHz or better;
  - HDD free space: at least 400 MB, separate from OS swap needs;
  - memory: at least 64 MB;
  - 4x-speed or faster CD-ROM drive;
  - 33.6 Kbps or faster modem / Internet connection;
  - VRAM at least 2 MB;
  - DirectX 6.1-compatible video and sound hardware;
  - mouse and keyboard;
  - the normal acquisition flow instructed the user to purchase the software package first and then register for Gamer's Dream service.
- Research consequence:
  - materially strengthens the conclusion that the normal commercial product had package-based install/client media;
  - the initial-edition special/bonus CD must remain a separate artifact hypothesis until direct package contents prove whether it was or was not the install disc.
- Does not support:
  - exact standard/initial-edition disc count;
  - product/JAN code;
  - disc matrix identifiers;
  - client executable filename/version;
  - filesystem or hashes.

### SRC-JP-GD-JSS-TRANSITION-2000-01

- Title: archived Gamer's Dream notice on future `STONEAGE` service following JSS failure
- Notice date: 2000-11-10
- Wayback captures used: 2001-01-13 and 2001-02-10
- Retrieval date: 2026-09-18
- Language/region: Japanese / Japan
- Source type: archived first-party NTT Data/Gamer's Dream service notice
- Archived URLs:
  - https://web.archive.org/web/20010113210300/http://www.dp.gamersdream.ne.jp/whats_new/sa.html
  - https://web.archive.org/web/20010210200933/http://www.dp.gamersdream.ne.jp/whats_new/sa2.html
- Confidence: **A**
- Supports:
  - JSS was responsible for the StoneAge game-application side, including client/software correction and version-up work;
  - Gamer's Dream was responsible for server operation/service and billing;
  - after JSS's October 2000 failure, Gamer's Dream could continue only a reduced service and could no longer provide the same JSS-dependent technical support/content-event support/version upgrades;
  - package sales through the Gamer's Dream online shop were stopped;
  - planned/ongoing software version upgrades could no longer continue under the same arrangement.
- Archaeology significance:
  - recovered executable/data/version-update artifacts should be classified primarily as JSS client/application lineage unless evidence shows they are platform-side infrastructure;
  - Gamer's Dream pages/account/billing/server notices should be treated as service-platform evidence, not automatically as game-client artifacts.
- Does not support:
  - exact 1999 client version number;
  - exact server source code ownership/implementation boundaries;
  - any unrecovered patch filename.

### SRC-JP-JSS-STONEAGE-VERUP-ARCHIVE-01

- Title: archived JSS `STONEAGE` version-up information page
- Original site period: JSS service era; archived capture used is 2000-12-04
- Retrieval date: 2026-09-18
- Language/region: Japanese / Japan
- Source type: archived first-party Japan System Supply page
- Archived URL: https://web.archive.org/web/20001204205900/http://www.titan.co.jp/stoneage/verup.html
- Confidence: **A**
- Supports:
  - JSS maintained an official StoneAge version-up/update information page;
  - the preserved automatic version-up history extends back to **1999-10-18**, three days after commercial launch;
  - the original service received frequent application/content changes including events, bug fixes, map/NPC/item/pet/UI changes and other updates;
  - the page links to a manual launcher-replacement/update procedure.
- Archaeology significance:
  - a retail CD is a launch baseline, not a complete representation of the 1999 JSS client state;
  - client archaeology should distinguish beta, retail-disc baseline, post-launch patched states and later pre-collapse states.
- Does not support yet:
  - numeric/internal version identifiers for the dated update states;
  - update manifest/package filenames or protocol;
  - exact file-level delta for each dated entry.

### SRC-JP-JSS-STONEAGE-LAUNCHER-ARCHIVE-01

- Title: archived JSS `STONEAGE` launcher replacement page and executable path
- Original JSS page: `http://www.titan.co.jp/stoneage/updater.html`
- Wayback capture used: 2000-12-04
- Retrieval date: 2026-09-18
- Language/region: Japanese / Japan
- Source type: archived first-party Japan System Supply page plus archived binary-path evidence
- Archived page URL: https://web.archive.org/web/20001204205200/http://www.titan.co.jp/stoneage/updater.html
- Confidence: **A** for filename, advertised size, installation relationship and purpose; binary bytes remain unverified locally
- Supports:
  - the original JSS-era StoneAge startup/launcher executable filename was **`stoneage.exe`**;
  - JSS offered a replacement `stoneage.exe` advertised as **212 KB**;
  - users were instructed to overwrite/copy it into the existing StoneAge installation directory, replacing the same-named file;
  - the replacement addressed startup network errors, version-up errors and failure to transition to the new program after updating;
  - the linked original executable path was `http://www.titan.co.jp/stoneage/stoneage.exe`;
  - Wayback reports two captures of that executable path, and following the archived object through the available extractor returns `application/octet-stream`, consistent with a preserved binary body.
- Research value:
  - provides the project's first confirmed original-JSS client executable filename and a high-value file-tree/search anchor.
- Does not support yet:
  - checksum, exact byte size, PE timestamp, imports, strings or version-resource values of the archived executable;
  - whether the archived 2001 binary is byte-identical to a 1999 launcher state.
- Repository safety:
  - if bytes are later recovered, record hashes and analysis but do not commit the proprietary executable by default.

### SRC-JP-JSS-STONEAGE-MANUAL-ARCHIVE-01

- Title: archived JSS `STONEAGE` official manual / installation and game-start page
- Original JSS manual index: `http://www.titan.co.jp/stoneage/manual.html`
- Wayback installation/start capture used: 2001-01-19
- Retrieval date: 2026-09-18
- Language/region: Japanese / Japan
- Source type: archived first-party Japan System Supply manual
- Archived page URL: https://web.archive.org/web/20010119071900/http://www.titan.co.jp/stoneage/manual01.html
- Confidence: **A**
- Supports:
  - DirectX 6.1 was required and included on the StoneAge **game CD**;
  - installation began by inserting the game CD, with an automatically starting installer;
  - install modes were standard (StoneAge + DirectX), minimum (StoneAge only), and custom;
  - the `map` component could be deselected as an installation workaround;
  - Windows Start-menu path `[Stoneage]` -> `[stoneage]`;
  - Gamer's Dream registration/service used an ID NUMBER/password after agreement;
  - a physical **CD NUMBER card** carried the CD NUMBER required for Gamer's Dream contract/registration;
  - F12 saved screenshots under a `screenshot` subdirectory beneath the StoneAge folder;
  - Alt+Enter provided window mode, documented with a 256-color support limitation.
- Research value:
  - independently confirms a normal game-CD install path and a separate registration artifact (CD NUMBER card);
  - gives concrete install/component/path anchors for future disc and client-tree archaeology.
- Does not support:
  - exact total disc count in standard or initial editions;
  - whether the separately advertised initial-edition special CD was or was not the game CD;
  - product/JAN code;
  - readable names for server labels damaged by archived-text mojibake.

### SRC-JP-JSS-STONEAGE-FAQ-ARCHIVE-01

- Title: archived JSS `STONEAGE` startup/install/update FAQ
- Wayback capture used: 2001-02-15
- Retrieval date: 2026-09-18
- Language/region: Japanese / Japan
- Source type: archived first-party Japan System Supply support/FAQ page
- Archived page URL: https://web.archive.org/web/20010215222514/http://www.titan.co.jp/stoneage/faqstart.html
- Confidence: **A**
- Supports:
  - startup troubleshooting references `MFC42.DLL`;
  - reinstall instructions refer to reinstalling StoneAge from the CD;
  - version-up/network troubleshooting tells users to delete files from the StoneAge installation's **`data\download`** directory and clear Windows `Temporary Internet Files` before retrying;
  - update failures include repeated file downloads, save failures, and a download error containing **`cksum:xxxxxxxxx`**;
  - proxy configuration is discussed in the update troubleshooting context;
  - cleanup of data from an earlier StoneAge test instructs users to uninstall and completely remove **`ProgramFiles\jss\stoneage`** before installing the retail product;
  - CD NUMBER is entered when contracting/registering with Gamer's Dream;
  - install workarounds include custom installation with `MAP` unchecked;
  - physical-CD troubleshooting tells users to inspect/clean the readable side of the StoneAge CD.
- Archaeology significance:
  - exposes concrete client/update anchors: `ProgramFiles\jss\stoneage`, `data\download`, `cksum:xxxxxxxxx`, `MFC42.DLL`, Windows Temporary Internet Files and proxy settings;
  - supports a model in which the updater downloaded individual files into a staging/cache area and performed checksum-related validation, while the exact algorithm/protocol remains unresolved.
- Does not support yet:
  - checksum algorithm;
  - update manifest filename/format;
  - update-server hostname/path;
  - payload filenames/extensions;
  - whether WinINet/IE APIs were used directly;
  - exact Japanese name/label of the earlier test referenced in damaged archive text.

### SRC-JP-2000-4GAMER-JSS-STOP

- Title: `R.I.P. LIFESTORM`
- Original date: 2000-10-16
- Retrieval date: 2026-09-18
- Language/region: Japanese / Japan
- Source type: contemporaneous specialist-press report
- URL: https://www.4gamer.net/archive/200010/ripls.html
- Confidence: **A**
- Supports:
  - JSS had effectively ceased business by 2000-10-16;
  - LIFESTORM/LIFESTORM2 service and support ended;
  - StoneAge support had ended, while Gamer's Dream was still checking whether StoneAge service itself could continue.
- Value:
  - contemporaneously corroborates the operating disruption later documented in the archived Gamer's Dream first-party notice.

### SRC-JP-2009-4GAMER-10TH

- Title: `1999年サービス開始の老舗MMORPG「ストーンエイジ」が，2010年2月にサービス終了`
- Original date: 2009-11-26
- Retrieval date: 2026-09-18
- Language/region: Japanese / Japan
- Source type: later specialist-press retrospective / service-end news
- URL: https://www.4gamer.net/games/013/G001377/20091126051/
- Confidence: **B**
- Supports:
  - retrospective statement that Japanese `STONEAGE` service started on **1999-10-15**;
  - the service had reached its tenth anniversary by October 2009.
- Does not support:
  - JSS executable/client version number;
  - original retail media layout.
- Note: used together with the contemporaneous PC Watch scheduled-release report and archived Gamer's Dream product page, this is sufficient for the working timeline to treat 1999-10-15 as the commercial service start unless conflicting primary evidence appears.

### SRC-JP-1999-RETAIL-MERCARI-01

- Title: `日本システムサプライ STONEAGE 初回限定版 マグカップ マウスパッド`
- Original artifact period: 1999 (seller attribution; package itself requires direct verification)
- Retrieval date: 2026-09-18
- Language/region: Japanese / Japan
- Source type: marketplace listing with photographs of a purported surviving unopened first-edition package and related promotional material
- URL: https://jp.mercari.com/item/m44997025885
- Confidence: **C** as historical proof; high-value acquisition/recovery lead
- Supports:
  - existence of a concrete surviving physical-package candidate labeled/described as a Japan System Supply `STONEAGE` initial limited edition;
  - a plausible route to obtaining package/disc photography or a provenance-preserving media dump.
- Seller states:
  - the package is an unopened first limited edition;
  - a bonus CD-ROM is included;
  - included promotional material is associated with Tokyo Game Show 1999.
- Does not support without direct inspection:
  - authenticity of every item/association;
  - exact game-disc contents;
  - checksums;
  - internal version number;
  - whether the listed bonus CD is distinct from the game install/client disc.
- Promotion criterion: upgrade relevant artifact evidence to **S** only after direct provenance-preserving inspection/imaging/dumping of original media/package.

### SRC-JP-2003-4GAMER-OGF-REVIVAL-01

- Title: `［OGF＃06］ボーステックが「Stone Age」（ストーンエイジ）を復活`
- Original date: 2003-07-26
- Retrieval date: 2026-09-18
- Language/region: Japanese / Japan
- Source type: specialist-press revival announcement with direct post-announcement questioning of Bothtec; near-contemporaneous retrospective on the earlier Japanese service
- URL: https://www.4gamer.net/news/history/2003.07/20030726001803detail.html
- Confidence: **B for retrospective description of the former Japanese StoneAge service; A/B for the 2003 revival announcement itself**
- Supports:
  - the former Japanese StoneAge is described as having monster capture/pets, turn-based combat, and parties of up to five players;
  - Bothtec told 4Gamer that the revived product would be a version-up rather than a byte-identical re-release, with additions/changes involving maps, characters and some UI;
  - the reporter explicitly states that in the former Japanese operation **only GMs could ride dinosaurs**, making normal-player pet riding absent from the earlier Japanese-service baseline represented by this report.
- Evidence boundary:
  - the GM-only riding statement is a 2003 specialist-journalist retrospective, not a recovered 1999 JSS manual/patch note;
  - it does not identify the exact build/date at which riding existed for GMs or the underlying client/server implementation;
  - the article's speculation about using a contemporary Korean build is explicitly the author's speculation and is not registered as fact.
- Archaeology significance:
  - normal-player riding must not be assumed to belong to the JSS Japanese baseline merely because it became iconic in later regional StoneAge versions;
  - riding should remain a later-layer feature unless an earlier primary artifact contradicts this evidence.

### SRC-JP-2003-4GAMER-TGS-REVIVAL-01

- Title: `［TGS2003 ＃13］ボーステック「銀河英雄伝説VII」＆「ストーンエイジ」の2タイトルを展示`
- Original date: 2003-09-27
- Retrieval date: 2026-09-18
- Language/region: Japanese / Japan
- Source type: specialist-press hands-on report plus direct on-site staff comments during the Japanese StoneAge revival
- URL: https://www.4gamer.net/news/history/2003.09/20030927063935detail.html
- Confidence: **B/A for the directly reported 2003 staff comments and visible revival state; B for retrospective comparison to the original**
- Supports:
  - when 4Gamer asked whether the revival was exactly the same as the former game, on-site staff answered that it was **basically the same**, with the immediate effort focused on restoration and bug fixing;
  - staff said roughly four major updates were planned after the open beta, including map expansion and additional characters;
  - the report identifies a dedicated **item trade window as a minor change that the original did not have**;
  - the article describes the old exchange practice in the context of putting items on the ground, explaining the theft risk that the new trade window addressed.
- Evidence boundary:
  - this does not prove every 2003-beta data file was unchanged from the final JSS build;
  - it does not identify exactly which JSS-era client revision served as the revival base;
  - the article is evidence for a feature boundary, not proof of the exact packet/server implementation of item exchange.
- Archaeology significance:
  - a reconstructed JSS baseline should not automatically include the later dedicated item-trade window;
  - any 2003 revival client recovered in the future can be used as a near-descendant diff anchor, but its UI additions must be separated from the earlier baseline.

### SRC-KR-2003-NETMARBLE-174-ANNOUNCE-01

- Title: `◈ 스톤에이지 서비스 일정 및 버전안내 ◈`
- Original post date: 2003-07-21
- Retrieval date: 2026-09-18
- Language/region: Korean / Korea
- Source type: same-period GameMeca community-board preservation quoting a Netmarble StoneAge homepage Q&A answer
- URL: https://www.gamemeca.com/fam.php?gcode=fam_scarecrow&gid=133954&rts=board
- Confidence: **B**
- Supports:
  - Netmarble's planned public service date was 2003-07-28;
  - the quoted Netmarble answer explicitly names the launch version as **`1.74`**;
  - the operator planned later regular updates.
- Evidence limit:
  - the accessible page is a same-period repost of the operator answer rather than the original Netmarble page;
  - it does not establish any binary hash, installer filename or relationship to JSS's internal version numbering.
- Archaeology significance:
  - `1.74` was a real public Korean service-version label, not merely a later private-server convention;
  - exact `1.74` artifacts are now controlled recovery targets.

- Derived recovery-status record:
  - `research/recovered/STONEAGE-KOREA-174-ARCHIVE-CLIENT-PROBE-R1.txt`;
  - corrected R2 semantics record **0 launch-window / 0 total 2003–2004 root snapshots** and keep the 2006 Netmarble download routes as later candidate clues only.
- This bounded archive result does not weaken the contemporaneous evidence that the launch label was `1.74`; it only means the original 2003 client path/bytes remain unrecovered on the tested archive surfaces.

### SRC-KR-2001-INIUM-174-TO-20-PRESERVED-01

- Title: `봉두 가족이 생기다^^* - 2001년11월14일`
- Original material date stated by preservation: 2001-11-14
- Retrieval date: 2026-09-18
- Language/region: Korean / Korea
- Source type: later Pooya's preservation of dated Inium-era StoneAge text/screenshots
- URL: https://pooyas.com/index.php?document_srl=166300&mid=screenshot
- Confidence: **C/B**
- Supports:
  - the preservation explicitly frames the material as an Inium StoneAge **post-1.74 preview of the 2.0 update**;
  - the preserved text/screenshots discuss the 2.0 family system and pet-riding capability.
- Evidence limit:
  - the current preservation page is not the original 2001 Inium host;
  - it does not prove which exact 1.74 executable/data build immediately preceded the preview.
- Archaeology significance:
  - supplies an independent version-transition clue `1.74 -> 2.0`;
  - reinforces the value of locating an authentic Inium 1.74 client.

### SRC-JP-2003-MADONOMORI-174A-01

- Title: `石器時代をモチーフにしたMMORPG「STONE AGE」のオープンβテストがスタート`
- Original date: 2003-12-17
- Client date field: 2003-12-12
- Retrieval date: 2026-09-18
- Language/region: Japanese / Japan
- Source type: contemporaneous specialist software-release report
- URL: https://forest.watch.impress.co.jp/article/2003/12/17/stoneage.html
- Confidence: **A**
- Supports:
  - the revived Japanese open-beta client was Windows 98/Me/2000/XP beta freeware;
  - the software metadata explicitly records version **`1.74a`**;
  - the metadata date is **2003-12-12**;
  - the report identifies official `stoneage.to` and Hangame as download surfaces.
- Does not support:
  - installer filename, checksum or file tree;
  - byte identity with Korean `1.74`;
  - direct identity with the last JSS client.
- Archaeology significance:
  - gives a precise near-descendant client version target;
  - the numeric proximity to Korean `1.74` is recorded as a **lineage hypothesis only**, pending artifact comparison.

### SRC-JP-2003-HANGAME-174A-INSTALL-CHAIN-01

- Title/artifact: Hangame StoneAge 1.74a launch-window installation chain
- Original period: 2003-12-14 to 2003-12-15 launch window; later CAB captures in 2004
- Retrieval/verification date: 2026-09-22
- Language/region: Japanese / Japan
- Source type: official Hangame pages and archived official CAB metadata/body prefix, recovered through Wayback CDX/Availability
- Official paths:
  - `http://www.hangame.co.jp/publish/sa/sasetup.asp`
  - `http://www.hangame.co.jp/publish/sa/sasetup2.asp`
  - `http://www.hangame.co.jp/publish/sa/sadl.asp`
  - `http://www.hangame.co.jp/publish/sa/HgSA.cab`
  - **launch-client URL:** `http://hangame.gamania.co.jp/stoneage/sa174hg.exe`
- Confidence: **A** for the official page/path relationship and recovered launch-window page timestamps; **B/A** for the later archived CAB representing the same Hangame control lineage
- Supports:
  - `sasetup.asp` is preserved at **2003-12-14 05:55:53 UTC** and links to both `sasetup2.asp` and the official StoneAge download page `sadl.asp`;
  - `sasetup2.asp` is preserved at **2003-12-15 09:53:20 UTC** and links back to `sasetup.asp`, establishing a two-step official install/startup instruction chain during the 1.74a open-beta launch window;
  - the exact Hangame control path `HgSA.cab` has preserved 2004 captures with one stable Wayback digest (`UYG45A3V3FPUJZIRQAI6SB22R4HALKOF`);
  - a successful bounded replay of that CAB exposes two members: `HgSA.dll` (38,400 bytes, DOS timestamp **2003-12-14 21:20:46**) and `HgSA.inf` (233 bytes, DOS timestamp **2003-12-14 21:05:14**);
  - the CAB header identifies a small one-folder/two-file control package, so `HgSA.cab` is **not** the full StoneAge client payload;
  - the official `sadl.asp` page is independently preserved at **2003-12-14 05:10:53 UTC**, inside the 1.74a launch window, and directly references **`http://hangame.gamania.co.jp/stoneage/sa174hg.exe`**;
  - a prose-free structured pass over that same archived page derives a **248MB** package-size token, **2** occurrences of `sa174hg.exe`, **1** occurrence of `stoneage.exe`, and normalized visible-text SHA-256 `990aec04c1a078ac4255bb4cc9a5eed69fda2cff3329ccfc9ed110e6b9a9f92b`;
  - the page's normalized visible text contains no explicit version token, so **1.74a** continues to come from the independent contemporaneous Mado no Mori release record rather than filename interpretation;
  - the relative executable token `stoneage.exe` is retained as a secondary search trait, not promoted to the full-package identity.
- Does not support:
  - archived byte availability, exact byte length, checksum or file tree of `sa174hg.exe`; the **248MB** figure is an official launch-page display-size token, not a recovered binary byte count;
  - that the later 2004 archived CAB bytes are byte-identical to any unarchived 2003-12 CAB response, despite the member timestamps falling in the launch window;
  - byte identity with Korean 1.74 or JSS 1999.
- Derived records:
  - `research/recovered/STONEAGE-JAPAN-174A-EXACT-INSTALL-CHAIN-R1.txt`
  - `research/recovered/STONEAGE-JAPAN-174A-SADL-PROBE-R1.txt`
- Archaeology significance:
  - the Japanese 1.74a client search no longer requires installer-name or rough-size guessing: the launch-window official download page has recovered the exact client URL `sa174hg.exe` and a **248MB** displayed size;
  - bounded exact-payload checks currently find **0 TimeMap mementos**, **0 Arquivo exact results**, **0 Internet Archive exact-target/file-name hits**, while the Common Crawl run is **INCONCLUSIVE** because every request failed with 503/timeouts;
  - the next evidence step is therefore historical mirror/carrier recovery using the exact filename, URL and 248MB display-size anchors, followed by transient byte-level extraction only if a preserved payload is actually available.

### SRC-JP-2004-4GAMER-RETAIL-PACKAGE-01

- Title: `ほのぼのMMORPG「ストーンエイジ」正式サービス開始日決定`
- Original date: 2004-05-20
- Retrieval/verification date: 2026-09-22
- Language/region: Japanese / Japan
- Source type: contemporaneous specialist game-industry report
- URL: https://www.4gamer.net/news/history/2004.05/20040520194557detail.html
- Confidence: **A**
- Supports:
  - Japanese formal service was announced for 2004-06-03;
  - the retail package began sale on **2004-05-20**;
  - the package contained **two CD-ROMs carrying the game client**, two 30-day tickets, an installation/game-guide manual and an Upopo dinosaur strap;
  - the report's retailer link targets the official `http://stoneage.to/package.html` page.
- Does not support **by itself**:
  - package JAN/model code, disc hashes/file trees or matrix identifiers;
  - byte identity with the December 2003 `1.74a` client;
  - which exact post-beta patch level was pressed onto either disc.
- Follow-up note:
  - the article's exact official `package.html` link has since been recovered independently; that separate official-page source closes JAN/model identity as recorded in `SRC-JP-2004-STONEAGE-PACKAGE-PAGE-01`.
- Archaeology significance:
  - establishes a concrete original physical carrier for the same Japanese revival lineage only five months after the 1.74a beta;
  - gives the project a disc-recovery route that is independent of the missing `sa174hg.exe` web payload.
- Dedicated derived probe target:
  - `research/recovered/STONEAGE-JAPAN-2004-PACKAGE-PROBE-R1.txt` once the bounded workflow produces it.

### SRC-JP-2004-STONEAGE-PACKAGE-PAGE-01

- Title: official Japanese StoneAge retail-package page `package.html`
- Original period: retail package on sale from 2004-05-20; archived page snapshot 2004-06-04 19:21:09 UTC
- Retrieval/verification date: 2026-09-22
- Language/region: Japanese / Japan
- Source type: archived official operator product page, reached from the contemporaneous 4Gamer retailer-link target
- Original URL: `http://stoneage.to/package.html`
- Preserved snapshot: Wayback timestamp `20040604192109`
- Confidence: **A/S** for product identity fields emitted from the recovered official page; not a disc-byte source
- Supports:
  - JAN/EAN-13 **`4988609011565`**;
  - package/model code **`WR-04156`**;
  - the page describes CD-ROM media, an Upopo bonus item and two 30-day tokens in normalized visible text;
  - period retailer target **Item City `product_id=423`**;
  - package-art asset path `/image/package/illust_01.jpg`;
  - normalized visible-text SHA-256 `4a1187b9aa876442e99828437836a5dec3e0b7185f6785c4faaf6b66f1802f39`.
- Does not support:
  - either retail CD's byte content, hashes, volume labels, matrix/mastering codes or file tree;
  - byte identity with the December 2003 `1.74a` launch client `sa174hg.exe`;
  - which exact post-beta patch level was pressed on either disc;
  - that every physical copy/pressing had byte-identical media.
- Derived records:
  - `research/recovered/STONEAGE-JAPAN-2004-PACKAGE-PROBE-R1.txt`
  - `research/recovered/STONEAGE-JAPAN-2004-ITEMCITY-PROBE-R1.txt`
- Archaeology significance:
  - converts the 2004 Japanese package from a generic product mention into a uniquely searchable physical-carrier target;
  - gives artifact recovery exact JAN/model/retailer anchors independent of the missing 2003-12 web payload;
  - a recovered disc remains a near-descendant comparison artifact and must not be promoted to a 1.74a byte baseline without direct comparison.

### SRC-KR-NETPOWER-CONTENTS-INDEX-01

- Title: `Net POWER 전체 목차 발행순`
- Original compilation date: later retrospective index (page updated through 2020-era preservation)
- Retrieval date: 2026-09-19
- Language/region: Korean / Korea
- Source type: later community-preserved magazine contents index
- URL: https://bihon.tistory.com/entry/Net-POWER-%EC%A0%84%EC%B2%B4-%EB%AA%A9%EC%B0%A8-%EB%B0%9C%ED%96%89%EC%88%9C-2020-05-19-%EA%B8%B0%EC%A4%80
- Confidence: **C/B** for issue/page targeting
- Supports:
  - StoneAge is indexed in NetPower 2000-09 p.87, 2000-11 p.99, 2000-12 p.173, 2001-01 p.185 and 2001-02 p.189;
  - these issue dates are rational supplement-CD recovery targets.
- Does not support:
  - that any corresponding supplement CD contained a StoneAge installer;
  - client filename, version, checksum or byte identity.
- Archaeology significance:
  - provides a bounded carrier-search schedule;
  - article presence must remain separate from carrier-content evidence.

### SRC-KR-NETPOWER-IA-CARRIER-SET-01

- Titles/items:
  - `netpower_cd_2000_09` — NetPower 2000-09 CD
  - `netpower_cd_2000_11` — NetPower 2000-11 CD
  - `netpower_cd_2001_02` — NetPower 2001-02 CD
- Retrieval/scan date: 2026-09-19
- Language/region: Korean / Korea
- Source type: public preserved magazine supplement-disc images plus derived recursive directory metadata
- URLs:
  - https://archive.org/details/netpower_cd_2000_09
  - https://archive.org/details/netpower_cd_2000_11
  - https://archive.org/details/netpower_cd_2001_02
- Confidence: **B** for provenance; direct for the exact preserved image file trees/hashes
- Supports:
  - each item exposes two disc volumes represented as IMG + ISO;
  - all twelve image representations were completely enumerated at ISO-9660/Joliet directory level with 0 scan errors and 0 truncation;
  - the exact preserved carriers contain 0 StoneAge-path matches under the repository's bounded target-token set.
- Does not support:
  - that every historical pressing or replacement copy was byte-identical;
  - that StoneAge was absent from all NetPower supplements or from other Korean distribution media.
- Derived records:
  - `research/recovered/STONEAGE-NETPOWER-2000-09-DISC-SCAN-R1.txt`
  - `research/recovered/STONEAGE-NETPOWER-EXACT-TARGET-DISC-SCAN-R1.txt`

### SRC-KR-NETPOWER-IA-MISSING-ISSUES-R2-01

- Title: precise Internet Archive NetPower 2000-12 / 2001-01 metadata probe
- Retrieval date: 2026-09-19
- Language/region: Korean / Korea
- Source type: Internet Archive advanced-search + item/file-list metadata
- Confidence: **B** for the bounded archive-service result
- Supports:
  - two known Korean magazine-disc preservation uploader neighborhoods were enumerated;
  - exact global identifier/title/description searches for NetPower 2000-12 and 2001-01 completed with 0 query errors;
  - no exact carrier item for either month was found on that current metadata surface.
- Does not support:
  - global nonexistence of either disc;
  - absence from private collections, unindexed IA items, or other preservation services.
- Derived record:
  - `research/recovered/STONEAGE-NETPOWER-IA-UPLOADER-NEIGHBORHOOD-R2.txt`

### SRC-TW-2000-WAEI-V10-REDUMP-104630

- Title/artifact: `Shiqi Shidai / 石器時代 / StoneAge` Taiwan retail CD, Redump disc 104630
- Original period: 2000 Taiwan release branch
- Preservation dump date: DiscImageCreator 2023-03-09 tooling; archive member timestamps 2023-05-21
- Retrieval/verification date: 2026-09-19
- Language/region: Traditional Chinese / Taiwan
- Source type: original retail optical media preservation, packaging/disc photographs, Redump record and byte-verified DiscImageCreator image
- Public preservation surfaces:
  - https://archive.org/details/stoneage_tw_2000_win
  - http://redump.org/disc/104630/
- Confidence: **S** for the exact preserved media identity, hashes, ring code and file tree
- Physical/media identifiers:
  - mastering ring: `華義國際股份有限公司 石器時代 V1.0 P-RPG-0008`
  - mastering SID: `IFPI LE92`
  - mould SID: `IFPI·9W10`
  - barcode: `4 710739 350098`
  - volume label: `STONEAGE`
  - one MODE1/2352 track
- Preservation archive:
  - `CD_DIC.rar`
  - size 842,125,501
  - MD5 `b37a4a47f4eb608cac67e4ddf7a1621a`
  - SHA1 `b8cf92720b6ec8b3f46ea2e9bfcda986d21e7ded`
- Verified disc track:
  - `STONEAGE.bin`, 523,449,360 bytes
  - CRC32 `e4638c81`
  - MD5 `b477bfc2b62527b255ab9f822349dc14`
  - SHA1 `d0f270163772eb587185a65e24a3f7e565263f2f`
  - SHA256 `905ee6ad89b8ca7f55a5c1132eede99a15ee7cb1b868f9b0b398fb0c76cfd159`
- Supports:
  - an original Waei/JSS Taiwan **v1.0 / Original** retail disc survives publicly with provenance-preserving dump metadata;
  - Redump and the recovered public copy agree at track-hash level;
  - the disc contains a complete directly readable StoneAge client tree;
  - the early branch contains `StoneAge.exe` and `sa_3.exe`, early `*_1.bin` resource generations and Waei operator host strings;
  - DiscImageCreator reports 0 disc errors and no copy protection found.
- Does not support:
  - byte identity with the 1999 Japanese JSS beta/retail client;
  - equivalence with Korean Inium/Hananet/CNET builds;
  - server-side rules/data absent from the client;
  - treating the separately bundled `人在江湖` and music-preview directories as StoneAge client content.
- Canonical derived records:
  - `research/recovered/STONEAGE-IA-EXACT-ARTIFACT-AUDIT-R1.txt`
  - `research/recovered/STONEAGE-TW2000-PRESERVATION-R1.txt`
  - `research/recovered/STONEAGE-TW2000-CLEAN-CLIENT-ACCEPTANCE-R1.txt`
- Archaeology significance:
  - first accepted early clean retail client baseline in the repository;
  - activates direct runtime/resource reverse engineering while JSS 1999 and Korean 2000 recovery continue as lineage-comparison tracks.
- Derived technical validation (2026-09-19):
  - `StoneAge.exe` is the Waei update/launch front-end: verified WinINet imports, `CreateProcessA`, updater paths/host and generation-pattern code references;
  - `sa_3.exe` is the game runtime: DirectDraw/DirectInput/DirectSound/WinMM plus a verified static `WSOCK32.dll` import table (15 Winsock functions including `connect`, `send`, `recv`, `gethostbyname` and `inet_addr`), `ClientLogin` / `CharLogin` code references, battle-map and resource paths;
  - existing 2.5 REAL/ADRN and SPR/SPRADRN parsers consume the v1.0 generation unchanged, establishing format-schema continuity;
  - `battle_1.bin` is a 233-record exact concatenation of the loose battle-map files;
  - `sound_1.bin` is structurally valid but seven loose WAV counterparts are variant payloads.
  - canonical reports: `research/recovered/STONEAGE-TW10-TECHNICAL-PROBE-R1.txt`, `research/recovered/STONEAGE-TW10-RUNTIME-DEEP-R1.txt`, `research/recovered/STONEAGE-TW10-RUNTIME-SOUND-R1.txt`.
  - direct v1.0 protocol-to-socket handoff is now binary-proven: `0x1b3f0` calls through function-pointer slot `0x598e0`; init helper `0x1ac10` receives callback `0x2eca0`; that callback updates pending-length state `0x13ede20`; the unique socket flush at `0x2eb33` consumes the same length with buffer `0x13f1e34`, socket `0x13ede24`, flags 0, and reaches WSOCK32 `send` through thunk `0x48466` / IAT `0x52254`. Canonical report: `research/recovered/STONEAGE-TW10-PROTOCOL-HANDOFF-R1.txt`.
  - v1.0 server-selection provenance is now binary-proven through the runtime startup path: WinMain-shaped RVA `0x1c4c0` stores its third incoming argument as the shared command-line source `0x139b758`; the same source feeds `realbin:/adrnbin:/sprbin:/spradrnbin:/windowmode/nodelay` parsing and the sole server-table writer `0x2e890`, which parses repeated `IP:` records into a 10 x 193-byte host/port table. Selected entries flow through `0x2e950` to the unique `socket/htons/inet_addr/gethostbyname/connect` game connection path. The disc's `StoneAge.exe` independently has one `CreateProcessA` site and builds the matching resource/startup command family before launching `sa_%d.exe`. The exact operator-era upstream provider of the dynamic `IP:` fragment remains open, but runtime endpoint delivery is established as launcher/process-command-line handoff. Canonical records: `research/recovered/STONEAGE-TW10-SERVER-SELECTION-R1.txt` and `research/clients/STONEAGE-TW10-SERVER-SELECTION-LINEAGE-R1.md`.
  - direct v1.0→2.5 diff: all 125,996 v1.0 ADRN records and all referenced REAL payloads are retained byte-for-byte; the entire 315,842,228-byte `real_1.bin` is a prefix of `real_15.bin`; all 464 v1.0 SPRADRN records/segments and the complete 2,889,630-byte `spr_1.bin` are likewise exact prefixes of the preserved 2.5 resources. Canonical report: `research/recovered/STONEAGE-TW10-VS-25-RESOURCE-DIFF-R1.txt`.

### SRC-CODE-DESC-STONEAGE-BISMARCKDD-999FFDF1

- Title/source: preserved later StoneAge client/server source tree (`BismarckDD/stoneage`)
- Pinned commit: `999ffdf1d220ec6666eb65339180689c9caf1876`
- Retrieval date: 2026-09-19
- Language/region: mixed Chinese / later community-preserved StoneAge lineage
- Source type: descendant source-code control corpus
- URL: https://github.com/BismarckDD/stoneage/tree/999ffdf1d220ec6666eb65339180689c9caf1876
- Confidence: **B for descendant implementation; not historical v1.0 provenance**
- Relevant files:
  - `client/stoneage/proto/protocol.h`
  - `client/stoneage/proto/lssproto_cli.cpp`
  - `client/stoneage/proto/lssproto_util.cpp`
  - `client/stoneage/system/map.cpp`
  - `client/stoneage/system/netproc.cpp`
  - `client/stoneage/system/netmain.cpp`
  - `client/stoneage/game/main.cpp`
  - `client/stoneage/wgs/common.cpp`
- Supports:
  - later LSSPROTO numbering/order and generated send-builder structure;
  - later implementations of `CreateHeader`, `strcatsafe`, `mkstr_int`, `mkstr_string`, and `Send`;
  - later `lssproto_Send` hands bytes to an indirect `lssproto.write_func` callback;
  - later map cache uses `map\\%d.dat` with width/height + tile/parts/event layers and receives server map rectangles through map protocol handlers;
  - later client lineage assigns WinMain `lpCmdLine` to a shared `CmdLine` pointer and parses the same `realbin:/adrnbin:/sprbin:/spradrnbin:/windowmode/nodelay` token family; this is a structural control for the independently recovered v1.0 startup parser, not proof of v1.0 addresses;
  - later `GameServer`/`getServerInfo` and WGS code provide semantic comparison for host/port table roles, while exact v1.0 table dimensions and endpoint provenance remain established only from the retail binary.
- Does not support by itself:
  - that any specific function address or behavior existed in Taiwan v1.0;
  - byte identity with the accepted 2000 retail binary;
  - unobserved server-side behavior.
- Archaeology significance:
  - when predictions from this tree are independently reproduced by exact Taiwan v1.0 binary counts/order, it becomes a strong lineage/control source without replacing the retail binary as primary evidence.


## Required metadata for future entries

Every substantial source should record:

- Source ID
- title/filename
- original date
- archive/download URL or physical provenance
- retrieval date
- language/region
- source type
- checksum if file-based
- confidence grade
- exact claims supported
- exact claims not supported
- notes on alterations/repacking
