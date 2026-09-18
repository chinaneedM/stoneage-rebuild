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
  - Cooperative player activity was described as contributing to village growth / richer communal life.
  - A summer 1999 service start was then being targeted.
- Does not support:
  - that every described mechanic shipped unchanged in the September beta or October retail release;
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
- Image evidence: Yahoo Auctions listing images; preserve URLs/archival captures separately if possible
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
