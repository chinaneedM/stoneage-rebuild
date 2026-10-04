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
  - search extraction has narrowed the printed beta-application URL to host `www.dp.gamersdream.ne.jp` and path tail `PO/sa_apply.html`, while one character immediately before `PO` remains visually/OCR ambiguous and is not normalized as fact;
  - bounded 1999 archive-index probing in `research/recovered/STONEAGE-JSS1999-BETA-APPLY-ARCHIVE-R1.txt` returns **0 literal tail matches** on the successful queries, but the final run is only **PARTIAL_NO_MATCH** because multiple Wayback/host-wide requests time out or fail;
  - a separate exact-candidate Availability pass in `research/recovered/STONEAGE-JSS1999-BETA-APPLY-CANDIDATES-R1.txt` completes **30/30** queries for `/~PO/`, `/%7EPO/`, `/PO/` and bare-host equivalents across six August/September 1999 dates, with **0 archive captures**;
  - those zero-capture results do **not** disprove any printed URL form. They only remove archive-capture support for the tested spellings; the printed character remains OPEN and must not be guessed.
- Independent preservation route:
  - Retromags file record: https://www.retromags.com/files/file/7018-play-online-no015-september-1999/
  - submitted 2023-12-14 by `kitsunebi`;
  - release filename: `Play Online No.015 (September 1999).cbr`;
  - listed file size: **349 MB**;
  - listed MD5: **`e009cc707810c4361c849f26248593af`**;
  - the public download flow resolves to the exact final object `https://seedbox.retromags.com:19918/Retromags%20Collection%202023/Play%20Online%20No.015%20(September%201999).cbr`, giving a concrete second scan-body route rather than merely a catalog entry.
- Current retrieval limitation:
  - on 2026-09-23 the Retromags download page again resolved to that exact seedbox object, but a direct transient-workspace retrieval failed at DNS resolution for `seedbox.retromags.com`;
  - no CBR bytes were obtained, so the listed MD5 has not been independently recomputed and the second scan body has not yet been visually compared with the Kingpin copy.
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
- Retrieval date: 2026-09-18; binary replay/analysis refreshed 2026-09-23
- Language/region: Japanese / Japan
- Source type: archived first-party Japan System Supply page plus archived first-party executable bytes analyzed transiently
- Archived page URL: https://web.archive.org/web/20001204205200/http://www.titan.co.jp/stoneage/updater.html
- Confidence: **A/S** for the first-party filename/path and derived byte-level metadata of the archived 2001 replacement object; not proof of a 1999 retail-disc binary
- Supports:
  - the original JSS-era startup/launcher executable filename was **`stoneage.exe`**;
  - JSS advertised the replacement as **212 KB** and instructed users to overwrite the same-named file in the StoneAge installation directory;
  - the linked original executable path is `http://www.titan.co.jp/stoneage/stoneage.exe`;
  - Wayback CDX exposes binary captures at **2001-05-03 01:38:34 UTC** and **2001-07-09 04:19:51 UTC** with the same archive digest;
  - bounded transient replay recovers the same **217,088-byte** x86 PE from both captures:
    - MD5 `8a5dc8b64f57574ffdd139a762a41aaa`
    - SHA-1 `43d4f038aca05d055b0f59cac26fd7fae4dbc099`
    - SHA-256 `6795d9349168f77aa025d7c4ea05d005c5bbfe33dd4b227eb7731802fa7eb82b`;
  - PE linker timestamp is **2000-02-10 07:58:33 UTC**, entry RVA `0x43b2`, image base `0x400000`, subsystem 2, with four sections `.text/.rdata/.data/.rsrc`;
  - VERSION metadata identifies the internal artifact as **`SaUpdate.EXE`**, FileDescription **`SaUpdate`**, CompanyName **`日本システムサプライ株式会社`**, FileVersion/ProductVersion **`1.0.0.1`**, with `Copyright (C) 1999`;
  - dialog resources title the program **`ＳＴＯＮＥＡＧＥ 起動プログラム Ver 1.01`** and expose the actions **`アップデートして起動`** / **`中断/キャンセル`**;
  - string-table resource ID 103 contains **`Windows ｿｹｯﾄの初期化に失敗しました。`**, directly confirming socket initialization in the updater/startup program;
  - the archived path filename `stoneage.exe` and internal OriginalFilename `SaUpdate.EXE` are therefore recorded separately; the recovered bytes are not promoted to the game-client main executable;
  - the outer PE statically imports only `KERNEL32.dll`, `MSVCRT.dll`, and `USER32.dll`;
  - original binary strings directly expose `update.gamersdream.ne.jp`, `/~stoneage/newest.txt`, `/~stoneage/%s`, `data\\download\\%s`, `(cksum:%u : File : %s)`, `sa_*.exe`, `sa_%d.exe`, and `updated`;
  - generation-numbered resource families for `real`, `adrn`, `spr`, `spradrn`, `battle`, `battletxt`, `sound`, and `soundaddr` are embedded in the same binary.
  - MFC42 HTTP-call topology binds the first-party updater strings to a concrete Internet-session / HTTP request path rather than treating them as unreferenced literals;
  - all 23 direct calls to the generation scanner recover the complete selector set **1–9**, mapped as **1=sa, 2=real, 3=sound, 4=spr, 5=spradrn, 6=adrn, 7=soundaddr, 8=battle, 9=battletxt**;
  - bounded x86 emulation verifies the reusable RVA `0x3c60` token helper as `(source, 1-based token index, destination, maximum length)`, using space/tab/colon delimiters with repeated-delimiter collapsing; this helper is observed in later data parsers and is not by itself proof of `newest.txt` grammar;
  - bounded emulation of RVA `0x3f20` with stubbed `fopen/fgetc/fclose` verifies the file checksum behavior on 8/8 synthetic cases as **`Σ(byte[i] + i)`**, zero-based `i`, in the routine's 32-bit accumulator;
  - final `_execl` launch passes generated `sa_%d.exe`, literal `updated`, `realbin/adrnbin/sprbin/spradrnbin` state strings and two additional launch-control buffers; the extra buffers are associated with code paths containing `IP:1` / `MESSAGE`, but exact labels remain unresolved;
  - selector-7 `soundaddr` and selector-9 `battletxt` update functions have no references to those two extra launch-control buffers.
- Research value:
  - closes the first recovered original-JSS executable bytes;
  - converts updater host, manifest path, remote payload-template path, local staging path and checksum-report shape from descendant hypotheses into first-party binary evidence.
- Still OPEN:
  - whether this 2001 archived replacement is byte-identical to any 1999 launcher state;
  - the exact `newest.txt` record grammar, field meanings and real historical generation/checksum records;
  - the exact semantic roles/formats of the two additional launch-control buffers associated with the `IP:1` / `MESSAGE` path;
  - lower-level socket implementation details beyond the now-recovered MFC HTTP application-layer topology.
- Follow-on archive-index boundary:
  - exact `newest.txt` queries and prefix queries for `update.gamersdream.ne.jp/~stoneage/`, plus the separately labeled source-derived `www.titan.co.jp/~stoneage/` candidate, were tested for 1999–2002;
  - all 6 queries completed with **0 errors**, **0 saturation** and **0 CDX rows**;
  - this does not contradict the updater host/path strings recovered from the binary; it only means no matching Wayback CDX capture is currently indexed on those tested paths.
- Derived reports / final validation:
  - `research/recovered/STONEAGE-JSS-LAUNCHER-ARCHIVE-PROBE-R1.txt`; **35781291855** — success;
  - `research/recovered/STONEAGE-JSS-LAUNCHER-DEEP-PROBE-R1.txt`; **35948368684** — success;
  - `research/recovered/STONEAGE-JSS-SAUPDATE-SEMANTIC-R1.txt`; **35948545627** — success;
  - `research/recovered/STONEAGE-JSS-SAUPDATE-XREF-R1.txt`; **35948787670** — success;
  - `research/recovered/STONEAGE-JSS-SAUPDATE-CALL-ARGS-R1.txt`; parser/core runs **35951460845 / 35951653442** — success;
  - `research/recovered/STONEAGE-JSS-SAUPDATE-HELPER-SEMANTICS-R1.txt`; **35951664729** — success;
  - `research/recovered/STONEAGE-JSS-SAUPDATE-TOKEN-EMULATION-R1.txt`; **35951529320** — success;
  - `research/recovered/STONEAGE-JSS-SAUPDATE-CHECKSUM-EMULATION-R1.txt`; **35951872034** — success, indexed-sum rule matches 8/8 cases;
  - `research/recovered/STONEAGE-JSS-SAUPDATE-LAUNCH-PARAMETERS-R1.txt`; **35951951617** — success;
  - `research/recovered/STONEAGE-JSS-UPDATE-ARCHIVE-PROBE-R1.txt`; **35781723407** — success after parser-test correction.
  - Earlier failed/cancelled setup/test attempts are excluded from evidentiary status.
- Repository safety:
  - executable bytes existed only in the CI runner temporary directory; the workflow's no-EXE retention check passed.

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

### SRC-KR-2003-NETMARBLE-EARLY-VERSION-ETNEWS-01

- Title: `넷마블, ‘스톤에이지’서비스`
- Original publication date: 2003-07-11
- Retrieval/verification date: 2026-09-23
- Language/region: Korean / Korea
- Source type: contemporaneous Korean technology-industry press report of Netmarble's service announcement
- URL: https://www.etnews.com/200307100179
- Confidence: **A/B** for the quoted launch strategy; not a binary-distribution artifact
- Supports:
  - Netmarble announced that it would service StoneAge through its own site;
  - the report says Netmarble planned to begin with the game's **early-development version** (`개발초기 버전`) and then continue upgrading it;
  - this statement predates the 2003-07-21 operator-Q&A preservation that explicitly names the 2003-07-28 launch label as `1.74`.
- Evidence boundary:
  - the report does not name an installer filename, payload URL, file size, checksum, internal build identifier or file tree;
  - `개발초기 버전` is a contemporaneous descriptive phrase, not a byte-level equivalence statement;
  - combining this source with the later `1.74` launch-label source does **not** prove byte identity with an Inium/JSS client carrying the same numerical version label.
- Archaeology significance:
  - independently corroborates that Netmarble intentionally restarted from an early StoneAge state rather than a later feature-rich branch;
  - strengthens the requirement to compare any recovered Korean Netmarble `1.74` artifact byte-for-byte against other regional `1.74`/JSS candidates instead of merging them by version string alone.

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


### SRC-CN-2001-17173-CLIENT-DIRECTORY-01

- Title: `石器游戏目录的秘密`
- Original date: **2001-07-09**
- Retrieval date: 2026-09-24
- Language/region: Simplified Chinese / Mainland China StoneAge community
- Source type: contemporaneous 17173 game-portal technical/player article
- URL: https://news.17173.com/z/stoneage/content/2001-7-9/n653_569161.html
- Confidence: **A** for the contemporaneous client-directory observation; not first-party executable/media evidence
- Supports:
  - the period Waei StoneAge installation path is described as `C:\\Program Files\\Waei\\石器时代\\`;
  - the client `map\\` directory is explicitly described as holding map-display files for areas the player has already traversed;
  - the same period installation is described as containing `data\\`, `data\\bgm\\`, `data\\se\\` and `screenshot\\` client directories.
- Archaeology significance:
  - independently corroborates the Taiwan-v1 binary-derived model in which ordinary field maps are runtime-acquired/local cache material rather than a complete retail-disc field corpus;
  - motivates recovery of contemporaneous installed-directory backups and historical “fully-open map” packs as potential map-cache evidence.
- Does not support:
  - byte identity with the accepted Taiwan Waei/JSS v1.0 Redump disc;
  - the exact version/build of every file present in the article author's installation;
  - any specific `map/<n>.dat` bytes, hashes, dimensions, or map IDs;
  - treating later full-map packs as v1 evidence without independent dating/version provenance.


### SRC-CN-2002-SINA-SA40-FULL-MAP-PATCH-01

- Title: `《石器时代4.0》最新地图补丁`
- Original date: **2002-11-08**
- Retrieval date: 2026-09-24
- Language/region: Simplified Chinese / Mainland China StoneAge distribution
- Source type: contemporaneous Sina Games download-center record
- URL: https://games.sina.com.cn/downgames/updatex/11084599.shtml
- Confidence: **A** for the dated download record and stated package purpose; package bytes remain unrecovered
- Supports:
  - the record identifies Waei as the game company and reports a **3440K** StoneAge 4.0 map patch;
  - the description explicitly states that installation makes all game maps visible and removes the need to read MAP data from the server during play;
  - the Sina local-download link exposes the source-derived filename `shiqi4updatex_02_11_08.zip` and download record id `aid=61620`.
- Archaeology significance:
  - independently corroborates that complete map-cache packages were distributed in the historical client ecosystem;
  - provides a dated descendant map corpus target suitable for controlled diffing if bytes are recovered;\n  - exact filename/stem preservation-carrier searches currently find no DiscMaster/Internet Archive carrier, and 2,149 archived Sina CGI URLs contain no `aid=61620` / basename variant; this is negative search evidence, not proof the package is lost.
- Does not support:
  - Taiwan v1.0 map-byte provenance;
  - byte identity between the 4.0 map pack and any earlier v1/1.82/2.x cache;
  - any map IDs, dimensions, hashes or package contents until the archive itself is recovered.
- Derived archive-index reports:
  - `research/recovered/STONEAGE-HISTORICAL-MAP-PACK-ARCHIVE-R1.txt`;
  - `research/recovered/STONEAGE-HISTORICAL-MAP-PACK-ARCHIVE-FALLBACK-R1.txt`;\n  - `research/recovered/STONEAGE-SA40-MAP-FILENAME-ARCHIVE-R1.txt`;\n  - `research/recovered/STONEAGE-SA40-MAP-CARRIER-R1.txt`;\n  - `research/recovered/STONEAGE-SA40-SINA-AID-61620-R1.txt`.

### SRC-CN-2003-SINA-SA-DOWNLOAD-HUB-01

- Title: `石器时代7.0石头就业所相关下载` / `石器时代ONLINE宠物进化史相关下载`
- Original date: **2003-04-03**
- Retrieval date: 2026-09-24
- Language/region: Simplified Chinese / Mainland China StoneAge distribution
- Source type: contemporaneous Sina Games StoneAge download-hub pages
- URLs:
  - https://games.sina.com.cn/zhqu/sta/download.shtml
  - https://games.sina.com.cn/zhqu/sta/ltxs/sqxz.shtml
- Confidence: **A** for the contemporaneous labels and recovered href targets; version identity of downloadable bytes remains unverified
- Supports:
  - the 5.0 page explicitly exposes a `完整地图档下载` / `MAP` entry;
  - the 6.0 section explicitly exposes a `真正全开MAP地图` entry;
  - the current preserved HTML resolves those map entries to the exact FTP target `ftp://211.90.133.5/dowload/sa/map.exe`, with the 6.0 hub also exposing the mirror `http://www.wuxitianlong.com/sa/map.exe`;
  - the same hub exposes a Sina-labelled `石器时代1.82` installer target `ftp://211.90.133.5/dowload/sa/sa1.82.exe`;
  - the 7.0 section separately offers an already-installed self-extracting package described as containing fully opened maps.
- Archaeology significance:
  - establishes a historical distribution path for complete map-cache material and an exact TARGET-B filename for the Sina-labelled 1.82 client;
  - provides descendant comparison targets without changing the Taiwan-v1 provenance gate.
- Does not support:
  - that `sa1.82.exe` is byte-identical to an original 2001-era 1.82 build; its build identity must be established from recovered bytes;
  - that the 5.0/6.0 `map.exe` bytes are identical merely because the preserved pages resolve to the same URL;
  - using any 4.0/5.0/6.0/7.0 map pack as Taiwan-v1 historical data without controlled version/provenance analysis.
- Derived reports:
  - `research/recovered/STONEAGE-SINA-DOWNLOAD-TARGETS-R1.txt`;
  - `research/recovered/STONEAGE-SINA-182-ARCHIVE-R1.txt`;
  - `research/recovered/STONEAGE-SINA-182-ARCHIVE-FALLBACK-R1.txt`;
  - `research/recovered/STONEAGE-HISTORICAL-MAP-PACK-ARCHIVE-R1.txt`.


### SRC-CN-2003-WUXITIANLONG-MAP-PACK-ARCHIVE-01

- Title/filename: archived `map.exe` full-map package
- Original/archive timestamp: **2003-06-23 23:44:51 UTC**
- Retrieval date: 2026-09-24
- Language/region: Simplified Chinese / Mainland China StoneAge ecosystem
- Source type: preserved historical binary from a contemporaneously linked StoneAge map-download mirror
- Historical URL: `http://www.wuxitianlong.com/sa/map.exe`
- Archive replay: Wayback timestamp `20030623234451`
- SHA-256: `372426e46765a1cf479041bdafc1d3e58fb019117d00d0b43d6a5f796620776e`
- Confidence: **A/S-derived** — the dated mirror relationship is anchored by contemporaneous Sina download pages; the recovered archive bytes themselves are hash-locked preservation evidence, but this is not an original Taiwan-v1/operator-disc artifact.
- Supports:
  - a complete historical StoneAge map-cache package is byte-recoverable from a 2003-06 archive capture of the exact mirror URL exposed by the contemporaneous download hub;
  - the package contains **1,008 numeric DAT map IDs**, of which **995** parse under the strict three-plane map-cache model;
  - comparison with the separately preserved 2.5 map directory finds the same 1,008 numeric IDs, **993 byte-identical** files, **15 changed** files and no one-sided numeric IDs;\n  - a later 2003-12 capture of the same mirror proves that the preserved 2.5 directory is not a simple chronological successor: 295 common maps are June=preserved-2.5 while December alone diverges;
  - direct Taiwan-v1 resource-profile classification of the 995 parseable historical maps yields **773 compatible / 222 incompatible** under the necessary-condition ADRN rule.
- Does not support:
  - that the package is a Taiwan-v1 map corpus;
  - that any asset-compatible map existed unchanged in Taiwan v1;
  - that the historical package is byte-identical to every 5.0/6.0 download endpoint merely because those pages share a filename or mirror path;
  - that the preserved mixed 2.5 client/server bundle is clean as a whole.
- Derived reports:
  - `research/recovered/STONEAGE-HISTORICAL-MAP-CAPTURE-R1.txt`;
  - `research/recovered/STONEAGE-2003-MAP-VS-25-R1.txt`;
  - `research/recovered/STONEAGE-TW10-2003-FIELDMAP-COMPAT-R1.txt`;\n  - `research/recovered/STONEAGE-2003-MAP-TIMELINE-R1.txt`.


### SRC-CN-2003-WUXITIANLONG-MAP-PACK-ARCHIVE-02

- Title/filename: archived `map.exe` full-map package, second preserved state
- Original/archive timestamp: **2003-12-10 09:24:26 UTC**
- Retrieval date: 2026-09-24
- Language/region: Simplified Chinese / Mainland China StoneAge ecosystem
- Source type: preserved historical binary from the same contemporaneously linked StoneAge map-download mirror
- Historical URL: `http://www.wuxitianlong.com/sa/map.exe`
- Archive replay: Wayback timestamp `20031210092426`
- SHA-256: `5f7f58e0d26d596e926a7d551d7c24e8a9a27824d5bdc53be3955b19b0e13abc`
- Confidence: **A/S-derived** for the captured bytes and archive timestamp; not Taiwan-v1/operator-disc provenance
- Supports:
  - the second capture extracts to **1,011 numeric DAT maps**, **998** strict three-plane valid plus **13** parser-invalid;
  - against the June capture, the same 1,008 IDs are shared, **698** are byte-identical, **310** differ, and December adds `8008`, `8100`, `8101`;
  - Taiwan-v1 ADRN necessary-condition classification of parseable December maps is **772 compatible / 226 incompatible**;
  - archive mtimes are preserved at file level; **337** entries carry `2003-10-20` modification dates, including maps 1000/2000/3000/4000;
  - three-corpus comparison shows **698 STABLE_ALL**, **295 DEC_ONLY_DIVERGENCE**, and **15 THREE_DISTINCT** among IDs common to June, December and the separately preserved 2.5 corpus.
- Important limits:
  - archive `Modified` timestamps are filesystem metadata, not guaranteed creation/release dates; values as early as 1997 demonstrate why they cannot be read literally as StoneAge map publication dates;
  - the separately preserved 2.5 map directory is not assigned a chronological position after this December capture merely because it was preserved later;
  - none of these descendant states proves Taiwan-v1 field-map membership.
- Derived reports:
  - `research/recovered/STONEAGE-HISTORICAL-MAP-CAPTURE-R1.txt`;
  - `research/recovered/STONEAGE-2003-MAP-TIMELINE-R1.txt`.


### SRC-CN-2002-17173-SA25-UPGRADE-01

- Title: `《石器2.5--精灵王传说》升级办法`
- Original period: 2002-01/02 rollout context; page states retail launch **2002-01-20**
- Retrieval date: 2026-09-24
- Language/region: Simplified Chinese / Mainland China
- Source type: contemporaneous 17173 StoneAge portal/version guide
- URL: https://news.17173.com/z/stoneage/banben/sa25-up.htm
- Confidence: **A-** for contemporaneous distribution facts; not first-party binary evidence
- Supports:
  - 2.5 retail launch on 2002-01-20 and early-February server migration;
  - complete 2.5 package stated as **580 MB** and updater as **8.25 MB**;
  - Beijing Waei web download plus a named list of Jan/Feb-2002 magazine/guide cover-disc carriers;
  - the complete package is described as a clean full reinstall, while the 8.25 MB updater requires an existing 2.x installation.
- Does not support:
  - the exact historical download URL or filename;
  - byte identity of any later-preserved 2.5 bundle;
  - Taiwan-v1 field-map provenance.

### SRC-CN-2002-SINA-SA25-UPGRADE-01

- Title: `《石器时代2.5》升级方法`
- Original date/context: February 2002; states server upgrade beginning **2002-02-04**
- Retrieval date: 2026-09-24
- Language/region: Simplified Chinese / Mainland China
- Source type: contemporaneous Sina Games news/distribution record
- URL: https://games.sina.com.cn/newgames/0202/02057854.shtml
- Confidence: **A-** for contemporaneous distribution facts; not first-party binary evidence
- Supports:
  - 2.5 retail launch on 2002-01-20 and server migration beginning 2002-02-04;
  - complete package stated as **575 MB** and updater as **8.25 MB**;
  - Beijing Waei web download plus the same periodical/guide distribution pattern.
- Conflict note:
  - 17173 reports the full package as **580 MB**. Preserve both reported sizes until a recoverable package or first-party file listing resolves whether this is rounding, a different build, or editorial variance.
- Does not support:
  - an exact installer filename or historical payload URL;
  - byte identity with any preserved descendant corpus.

### SRC-CN-2001-2002-WAEI-STONEAGE2-UPGRADE-PATH-01

- Title/path: Beijing Waei StoneAge2 `/ZHUANQU/stoneage2/tyro/upgrade.asp`
- Preserved capture: **2001-12-04 16:57:11 UTC**
- Retrieval date: 2026-09-24
- Language/region: Simplified Chinese / Mainland China
- Source type: official Waei page preserved by Wayback; plus February-2002 official Waei inbound links to the same pathname
- Historical URL: `http://www.waei.com.cn:80/ZHUANQU/stoneage2/tyro/upgrade.asp`
- Clean replay SHA-256: `73fde66ffb3c92261d66715f873fa9b9f54166e4443d5d29924fe137cdcb8d35`
- Confidence: **A/S-derived** for the 2001 captured page body and dated official link topology; **OPEN** for the unpreserved February-2002 destination body
- Supports:
  - the `stoneage2` official site tree existed before the 2.5 retail rollout;
  - the preserved 2001 page explicitly identifies **石器时代2.0** and is a **“升级所需经验”** level/experience guide;
  - clean structural extraction yields **99 candidate references and 0 strong payload references**;
  - three preserved February-2002 Waei pages independently link the same pathname.
- Critical semantic correction:
  - `upgrade.asp` in the preserved 2001 site does **not** mean a software updater; `升级` here is character leveling. The path name must not be used as evidence for a 2.5 installer/download target.
- Does not support:
  - that the February-2002 destination body was byte-identical to the 2001 capture;
  - any 2.5 installer filename, payload URL, mirror host, hash, or package size;
  - any field-map byte provenance.
- Derived reports:
  - `research/recovered/STONEAGE-WAEI-SA25-KEYPAGES-R1.txt`;
  - `research/recovered/STONEAGE-WAEI-SA25-UPGRADE-PAGE-R1.txt`;
  - `research/recovered/STONEAGE-WAEI-SA25-TYRO-SUBTREE-R1.txt`;
  - `research/recovered/STONEAGE-WAEI-PRE25-UPGRADE-CAPTURE-R1.txt`;
  - `research/recovered/STONEAGE-WAEI-2002-PAYLOAD-DOMAIN-R1.txt`.



### SRC-CN-2002-POPSOFT-SA25-FEB-SCAN-01

- Contemporary distribution anchor: 17173's surviving `《石器2.5--精灵王传说》升级办法` explicitly names **`《大众软件CD——大众游戏》2002年2月号`** among media from which users could obtain the complete StoneAge 2.5 package or updater.
- Preserved scan-family item: Internet Archive identifier **`popsoft-magazine_202403`**, title `Popsoft 大众软件`.
- Retrieval/research date: **2026-09-27**.
- Source type: public preservation metadata plus original magazine-scan files and transient OCR text; **not a preserved cover-disc image**.
- Exact February-2002 original scan files exposed by IA metadata:
  - `2002/大众软件-2002年02月A.pdf` — 213,906,834 bytes, MD5 `f81361daf9f1998213e191facfd110bc`, SHA-1 `95ce835b9475bfc91bded8f169828d271453cb0e`;
  - `2002/大众软件-2002年02月B.pdf` — 216,402,608 bytes, MD5 `2312310bf26764a76ede6f229abec66a`, SHA-1 `76915aaff249e54a0e5d090ed10172542c015072`.
- File-list boundary:
  - IA metadata exposes **6,809 files** in the scan-family item, including **26** February-2002 A/B derivatives/originals;
  - it exposes **0 optical-image files** for the Popsoft item: no ISO/BIN/CUE/IMG/MDF/MDS/NRG/CCD/SUB object is present in the current file list.
- Transient OCR cross-check:
  - February-A `_djvu.txt` is 784,590 bytes, SHA-256 `71b56a151f692558f022c4e460ab21f1eac9b4f30579e69db8f1fff7d6043c63`, with **5** bounded StoneAge-2.5/Spirit-King proximity hits;
  - February-B `_djvu.txt` is 870,256 bytes, SHA-256 `9614393a5280c27558f7dbc5f017964f318a251cf786ccc2413fbf70dfae3810`, with **0** such strong hits under the same detector.
- False-positive correction:
  - broad IA query `"大众软件" AND year:2002` returns item `start-modem-5600d`, which contains `START_MODEM.iso`;
  - its title/creator identify a **福建实达 5600D modem driver disc**, so its optical image is an unrelated metadata-description collision and must not be promoted as a StoneAge/Popsoft carrier.
- Confidence: **S-derived for the IA file-list/hash/OCR-count observations; A- for the separate contemporaneous 17173 carrier statement; OPEN for the physical February-2002 Popsoft cover-disc bytes**.
- Evidence boundary:
  - the magazine scan proves that the February 2002 paper issues survive publicly and that issue A contains StoneAge-2.5-related text;
  - it does **not** establish that the A issue, rather than B or another `大众游戏` carrier configuration, physically carried the target disc;
  - magazine/PDF bytes are not cover-disc/client bytes and cannot establish installer filename, volume label, file tree, checksum or clean-client provenance.
- Recovery consequence:
  - classify this IA route as **SCAN-ONLY / OPTICAL-RESIDUAL-BOUNDED**;
  - reopen only from an exact cover-disc identifier, disc-face photograph, file listing, checksum, archive/torrent identity or independent preserved `大众游戏` February-2002 optical object.
- Derived evidence:
  - `research/recovered/STONEAGE-SA25-POPSOFT-2002-RESIDUAL-R1.txt`;
  - `research/clients/STONEAGE-SA25-POPSOFT-2002-CARRIER-BOUNDARY-R1.md`.

### SRC-CN-2002-17173-SA25-PRODUCT-01

- Title: `《石器2.5--精灵王传说》产品介绍`
- Retrieval date: 2026-09-24
- Language/region: Simplified Chinese / Mainland China
- Source type: surviving 17173 StoneAge product-description page
- URL: https://news.17173.com/z/stoneage/banben/sa25-cp.htm
- Confidence: **A-** for period product composition as preserved by the contemporaneous StoneAge portal; not a disc dump
- Supports:
  - `石器时代2.5延年益兽包` is described as including a **StoneAge 2.5 client CD** plus WGS/physical extras;
  - `石器时代2.5春满钱坤包` is likewise described as including a **StoneAge 2.5 client CD**;
  - `石器时代2.5新手报到包` existed in three package variants;
  - the surviving page still references three contemporaneous new-user-package-block image assets under the 17173 StoneAge 2.5 tree: `sa03.gif`, `st25_new_02.jpg`, and `st25_new_03.jpg`. Treat these as exact visual-search tokens, not disc identifiers.
- Archaeology significance:
  - identifies official product families that physically carried a 2.5 client disc and can therefore serve as provenance-preserving recovery targets.
- Does not support:
  - any disc hash, file tree, mastering/pressing identity or byte equality between the product families;
  - that a current marketplace disc is authentic without physical verification;
  - Taiwan-v1 field-map provenance.
- Current lead report:
  - `research/recovered/STONEAGE-SA25-LIVE-PHYSICAL-LEADS-R1.md`.


### SRC-CN-SA25-SA25UP-LINK-MIRROR-01

- Title/context: surviving software-download link mirror containing `[下載]石器時代2.5—精靈王傳說`
- Retrieval date: **2026-09-25**
- Language/region: Traditional Chinese / cross-strait player-web download-link ecosystem
- Source type: later-surviving third-party software-link mirror; page header states `from http://pcpc.idv.tw/soft/soft.htm`
- URL: https://www.geocities.ws/kk00000099/link.html
- Exact StoneAge target exposed by the page: `http://202.104.32.168/file/game/maoxian/sa25up.zip`
- Confidence: **C+ for the literal surviving link text; A for the separate identification of the IP as 21CN download infrastructure; OPEN for original publication date, payload size/content and operator provenance**
- Supports:
  - an independently sourced exact filename/path token, `sa25up.zip`, circulated as a StoneAge 2.5 download link;
  - reopening bounded preservation indexes once for this precise token rather than inventing installer/updater filenames.
- Original-source boundary at registration time:
  - this mirror page alone did not establish the payload type from the `up` suffix.
- Superseding native evidence:
  - native 21CN record `20165` now explicitly classifies the exact linked `sa25up.zip` item as a **`客户端升级包`** sized `8473 k` / later `8.27M`, ruling out the 575/580 MB complete package at the catalogue-description level;
  - exact byte identity with the separately reported 8.25 MB operator updater remains unproven because the ZIP body is unrecovered.
- Does not support:
  - that the IP host was Beijing Waei or another official operator;
  - clean-client status, file size, hash, archive members, or byte identity with any preserved 2.5 corpus.
- Follow-up result:
  - metadata-only exact-token probe found **0 hits / 0 errors** across Wayback Availability period anchors, Arquivo.pt exact URL, eight Common Crawl index generations, DiscMaster exact filename indexing and Internet Archive metadata/file lists;
  - tested exact preservation-index route is therefore **BOUNDED** pending a new mirror/hostname/capture/file token.
- Derived report: `research/recovered/STONEAGE-SA25-SA25UP-EXACT-R1.txt`.





### SRC-CN-2001-2002-21CN-DOWNLOAD-HOST-01

- Historical IP: `202.104.32.168`
- Research date: **2026-09-25**
- Source type: dated Wayback replays of the host root and native software-detail pages
- Key captures:
  - **2001-12-27 12:44:46 UTC** — host root, title `21CN.COM - 下载`, SHA-256 `e1bddcbd266109772d63be517e91dc0ba4f65943d6c94bc8574ab203c3a5f5f4`;
  - **2002-02-01 18:03:27 UTC** — `list.php?id=113`, title `Cool Desk 99 - 下载 - 21CN.COM`, SHA-256 `d6a9489cbd4d817d1c565c8c17b1ca199f84efb52da51d2f94ba4a966bdcddf0`;
  - **2002-02-01 19:05:12 UTC** — `list.php?id=1137`, title `PC-Cillin 2002 Pattern 218 - 下载 - 21CN.COM`, SHA-256 `5210302cd7e279c29297d72cbd57bf7d36177eb1997f3cf65e905dfd0b4b5218`.
- Visible/decoded host identity fields:
  - `21CN.COM - 下载`;
  - `download.21cn.com`;
  - `粤ICP证010001`;
  - `世纪龙信息网络有限责任公司版权所有`.
- Confidence: **A for the historical host/site identity; OPEN for the provenance and integrity of the StoneAge payload hosted under that infrastructure**
- Supports:
  - `202.104.32.168` was serving 21CN software-download infrastructure during the relevant 2001–2002 period;
  - the later `sa25up.zip` URL is therefore not evidence of a Beijing-Waei-owned host merely from its IP/path.
- Does not support:
  - that 21CN modified or did not modify the StoneAge file;
  - that the StoneAge file was successfully downloadable at any surviving capture;
  - payload size, checksum, archive contents, build, or clean-client status;
  - a direct operator-to-21CN distribution contract.
- Derived reports:
  - `research/recovered/STONEAGE-SA25-HOST-IDENTITY-R1.txt`;
  - `research/recovered/STONEAGE-SA25-HOST-NEIGHBORHOOD-R1.txt`.
- Follow-up result:
  - **RESOLVED:** native record `list.php?id=20165` has been recovered and independently cross-validated as `石器时代2.5—精灵王传说`; continue from its `downit.php` and mirror topology rather than repeating broad catalogue discovery.




### SRC-CN-2002-21CN-SA25UP-JPG-01

- Historical URL: `http://download.21cn.com:80/file/game/maoxian/sa25up.jpg`
- Wayback timestamp: **2002-05-17 23:58:42 UTC**
- Retrieval/research date: **2026-09-25**
- Source type: recoverable archived 21CN-hosted same-stem JPEG sidecar
- HTTP replay: **200**
- Recovered body size: **9,312 bytes**
- SHA-256: `7b475f1b3613d87e4e5747bb98d68ac186da265518359ac819b97c19b3b8b80e`
- JPEG dimensions: **120 × 169**, 8-bit, 3 components
- JPEG metadata: EXIF present; JFIF 1.02; comment `ACD Systems Digital Imaging`; no ICC or Photoshop segment detected
- Transient visual observation: illustrated game-art panel showing multiple stylised human figures and dinosaur / prehistoric-fantasy creatures; no reliably readable edition/version/operator text at the archived resolution.
- Confidence: **A for URL/timestamp/HTTP status/bytes/hash/dimensions; B for literal broad visual description; OPEN for exact artwork edition and relationship to ZIP contents**
- Supports:
  - a native 21CN `sa25up`-stem game-art asset existed and was successfully archived by May 2002;
  - the `sa25up` object family predates the 2003 archived source-page link and later reposts.
- Does not support:
  - successful archival or current recoverability of `sa25up.zip`;
  - byte integrity or exact byte identity of the ZIP. **Package type is now resolved separately by native record `20165` as a client upgrade package**, ruling out the 575/580 MB full package at the catalogue-description level;
  - official Beijing-Waei provenance, clean-client status, file tree, checksum or byte identity;
  - a direct operator-to-21CN distribution contract.
- Crawl-neighborhood note:
  - `list.php?id=8831` was captured at **2002-05-17 23:12:52 UTC** in the nearest currently indexed two-hour crawl neighborhood;
  - this is only a discovery candidate until an explicit HTML/path relation is recovered.
- Derived reports:
  - `research/recovered/STONEAGE-SA25-21CN-JPG-R1.txt`
  - `research/recovered/STONEAGE-SA25-21CN-CRAWL-NEIGHBORHOOD-R1.txt`
  - `research/clients/STONEAGE-SA25-21CN-SA25UP-JPG-VISUAL-R1.md`



### SRC-CN-2002-21CN-SA25-UPDATER-01

- Native catalogue URL: `http://download.21cn.com/list.php?id=20165`
- Earliest currently recovered archive capture: **2002-02-12 01:05:02 UTC**, HTTP 200
- Earliest replay body: **36,495 bytes**
- Earliest replay SHA-256: `962145dbcd7b8e4c7e627be3787455aa554de7f2ab4d39592255d1a4d19d5d28`
- Catalogue title: **`石器时代2.5—精灵王传说`**
- Catalogue fields:
  - 软件版本: **客户端升级包**
  - 软件类别: 冒险角色
  - 软件性质: 共享 — 21CN catalogue classification only
  - 整理日期: **2002-01-31** — catalogue metadata, not archive timestamp
  - 文件大小: **8473K** in early captures; later **8.27M**
  - 系统平台: Win9x/WinME/WinNT/Win2000/WinXP
  - 软件公司: **北京华义**
- Exact early asset links:
  - `http://download.21cn.com/file/game/maoxian/sa25up.zip`
  - `http://download.21cn.com/file/game/maoxian/sa25up.jpg`
- Preservation depth:
  - **14** archived HTTP-200 catalogue rows from 2002-02-12 through 2005;
  - final bounded probe replayed **10** selected catalogue captures with **0 errors**;
  - 2002-06-13 and 2002-08-12 preserve the same StoneAge 2.5/updater identity;
  - later pages normalize the size to **8.27M**.
- Delivery/router evidence:
  - `downit.php?id=20165&num=0` is archived;
  - **2002-10-17** router replay contains `http://images.21cn.com/download/file/game/maoxian/sa25up.zip`;
  - later pages/router surfaces expose `download.21cn.com/file1/game/maoxian/sa25up.zip`, `dg.download.21cn.com/file1/game/maoxian/sa25up.zip`, `dg.download.21cn.com/file1_21cn/game/maoxian/sa25up.zip`, `dg.download.21cn.com/file1xjy/game/maoxian/sa25up.zip`, and `dg.download.21cn.com/file1xzm/game/maoxian/sa25up.zip`.
- Router behavior:
  - the 2002-10-17 wrapper is HTTP 200 JavaScript and directly executes `window.open("http://images.21cn.com/download/file/game/maoxian/sa25up.zip")`;
  - the 2003-03-18 and 2003-04-22 archived 302 responses contain a database error for product 20165 and redirect back to the 21CN root; they are **not** valid payload redirects;
  - 2004 download pages continue to label the object **`石器时代2.5-精灵王传说客户端升级包 下载 (8.27M)`** while routing through later `dg.download.21cn.com` path generations.
- Exact mirror preservation result:
  - seven evidence-derived 21CN ZIP URL generations were queried through Wayback CDX;
  - result: **0 HTTP-200 ZIP captures / 0 recovered ZIP bodies / 0 probe errors**;
  - the 2002 router-derived `images.21cn.com/download/file/game/maoxian/sa25up.zip` URL has only two HTTP-404 rows from December 2005;
  - Arquivo.pt returns 0 exact rows;
  - a supplemental Common Crawl check is **partial/inconclusive** because five indexes returned HTTP 504, while the successful tested indexes returned 0 rows.
- Operational status: **IDENTITY RESOLVED / BYTE RECOVERY BOUNDED on the tested 21CN mirror family.** Reopen only from a new exact mirror, checksum, P2P/preservation token or archive corpus.
- Confidence:
  - **A for literal native 21CN catalogue fields, capture timestamps, exact page links and router references**;
  - **A for classifying the historical token as the 2.5《精灵王传说》客户端升级包 on 21CN**;
  - **OPEN for ZIP bytes/hash/archive members and byte-identical equivalence to an operator-origin master**.
- Supports:
  - `sa25up.zip` is the ~8.27 MB StoneAge 2.5 Spirit King client updater mirrored by 21CN;
  - the updater is distinct from the separately documented 575/580 MB full client package;
  - Beijing Waei is the software company named on the native catalogue entry.
- Does not support:
  - that 21CN's bytes were unmodified relative to an operator master;
  - any ZIP checksum or internal file tree;
  - any particular field-map/resource delta until the payload bytes are actually recovered.
- Negative controls / disambiguation:
  - 21CN record `22318` is a separate 564K update for a Beijing Netcom 9 free-test server, with page整理日期 2002-07-17;
  - record `8831` is Quick Heal antivirus and is closed as a false crawl-proximity candidate.
- Derived reports:
  - `research/recovered/STONEAGE-SA25-21CN-RANKING-ID-R1.txt`
  - `research/recovered/STONEAGE-SA25-21CN-RECORD-20165-R1.txt`
  - `research/recovered/STONEAGE-SA25-21CN-DOWNIT-20165-R1.txt`
  - `research/recovered/STONEAGE-SA25-21CN-REDIRECT-HEADERS-R1.txt`
  - `research/recovered/STONEAGE-SA25-21CN-MIRROR-RECOVERY-R1.txt`
  - `research/recovered/STONEAGE-SA25-21CN-IMAGES-MIRROR-R1.txt`
  - `research/recovered/STONEAGE-SA25-21CN-JPG-R1.txt`


### SRC-CN-2003-PCPC-SA25UP-SOURCE-ARCHIVE-01

- Title/context: archived legacy software/game download-link page `/soft/soft.htm`
- Archive timestamp: **2003-06-05 10:48:51 UTC**
- Retrieval/research date: **2026-09-25**
- Historical URL: `http://pcpc.idv.tw:80/soft/soft.htm`
- Wayback raw replay: timestamp `20030605104851`
- Replay SHA-256: `604304bd2c931c463ccb575f3920dd096a340441825a58274d9f6e897dc966c5`
- Replayed body size: **406,274 bytes**
- Character evidence: Big5/CP950 byte-level matches directly recover `下載`, `石器時代2.5`, and `精靈王傳說`.
- Literal dated row: `[下載]石器時代2.5—精靈王傳說` -> `http://202.104.32.168/file/game/maoxian/sa25up.zip`
- Confidence: **B+ for the literal archived page body, capture timestamp and href; A for the separate identification of the linked IP as 21CN download infrastructure; OPEN for StoneAge payload/operator provenance and contents**
- Supports:
  - the exact `sa25up.zip` StoneAge 2.5 link text was present on this source page no later than **2003-06-05**;
  - the later Geocities and 2012 PIXNET copies preserve a link already demonstrably present on a 2003 archived source page.
- Does not support:
  - that the linked file returned HTTP 200 or remained downloadable at the capture timestamp;
  - that the file is Beijing-Waei/operator-distributed;
  - by itself, this later page did not establish what `up` meant. **Superseding native 21CN record `20165` now explicitly classifies the same token as a client upgrade package sized 8473K / 8.27M**;
  - the file's hash, archive members, exact byte integrity, cleanliness, or byte relationship to the operator-referenced 8.25 MB updater and recovered mixed 2.5 bridge.
- Cross-check:
  - the same exact row/href is present in successful source-page captures at **2003-12-03** and **2005-01-01**;
  - separate Wayback payload-path records are 404, including malformed/suffixed URL forms indexed in 2002.
- Derived report: `research/recovered/STONEAGE-SA25-PCPC-SOURCE-REPLAY-R1.txt`.

### SRC-CN-2012-PIXNET-SA25UP-REPOST-01

- Title: `U車車軟體分享區1`
- Publication timestamp shown by page: **2012-04-11 18:00**
- Retrieval date: **2026-09-25**
- Language/region: Traditional Chinese / Taiwan-hosted later repost
- URL: https://bunvcudxc.pixnet.net/blog/posts/8022503587
- Source type: later third-party repost of a broad legacy software/game download-link collection
- Confidence: **C+ for literal surviving text and page timestamp; D/OPEN for the original age and provenance of the copied StoneAge link**
- Literal StoneAge row: `[下載]石器時代2.5—精靈王傳說` -> `http://202.104.32.168/file/game/maoxian/sa25up.zip`
- Supports:
  - a second surviving web copy of the same exact `sa25up.zip` URL and StoneAge 2.5 label;
  - the URL was not unique to the Geocities survivor and circulated within copied legacy download-link lists.
- Does not support:
  - that the URL was still live in 2012;
  - that the link list itself originated in 2002;
  - by itself, that `sa25up.zip` was official, clean, or byte-identical to any known specimen. **Native 21CN record `20165` subsequently resolves it as the 8473K / 8.27M client upgrade package, not the 575/580 MB full package.**
- Research consequence:
  - use this as **survival/circulation corroboration only**;
  - this repost is retained only as circulation corroboration. Native 21CN record `20165` now supplies the authoritative catalogue classification; the tested 21CN mirror family is bounded for payload bytes.

### SRC-DERIVED-KR-PAYLOAD-FILENAME-INDEX-R1

- Type: derived preservation-index negative control over source-derived exact Korean StoneAge payload filenames
- Research date: **2026-09-25**
- Derived report: `research/recovered/STONEAGE-KOREA-PAYLOAD-FILENAME-INDEX-R1.txt`
- Exact targets:
  - GameTime formal mirror: `onlStoneAge.zip`
  - GameTime trial: `stone_demo.exe`
  - Hananet formal: `sa.exe`
  - Hananet trial: `sa_demo.exe`
  - Gagamel beta record: `stoneagebeta.zip`
  - CNET formal mirror: `stoneage.zip`
- Preservation surfaces tested:
  - DiscMaster file/path index;
  - Internet Archive advanced item search followed by exact file-list inspection;
  - public old-disc `allseeds.zip` torrent path metadata.
- Result: **0 strict DiscMaster hits / 0 IA items with strict file matches / 0 strict torrent-path hits / 0 errors**.
- False-positive control:
  - `sa.exe` and `stoneage.zip` are ambiguous basenames and are not promoted without the expected 220–300 MB scale or explicit Korean StoneAge/operator context;
  - raw lexical rows therefore do not count as client recovery.
- Confidence: **A for the bounded negative result on the tested index snapshots; no claim about preservation services/corpora not tested**
- Consequence: do not repeat these exact index queries unless a new corpus, checksum, mirror URL, carrier identity, or other precise token changes the search space.


### SRC-DERIVED-SA25-SA25UP-NEIGHBORHOOD-R1

- Type: derived archive-index chronology / neighborhood analysis for the exact StoneAge 2.5 `sa25up.zip` path
- Research date: **2026-09-25**
- Derived report: `research/recovered/STONEAGE-SA25-SA25UP-NEIGHBORHOOD-R1.txt`
- Target path: `http://202.104.32.168/file/game/maoxian/sa25up.zip`
- Attributed source page: `http://pcpc.idv.tw/soft/soft.htm`
- Wayback CDX findings:
  - **2002-07-12 03:14:03 UTC** — `sa25up.zip+`, HTTP **404**;
  - **2002-09-29 10:14:30 UTC** — `sa25up.zip&nbsp`, HTTP **404**;
  - **2003-06-23 11:51:44 UTC** — `sa25up.zip%20`, HTTP **404**;
  - **2006-01-05 11:28:03 UTC** — exact unsuffixed `sa25up.zip`, HTTP **404**.
- Source-page Availability findings:
  - successful archived source-page capture exists at **2003-06-05 10:48:51 UTC**;
  - later successful source captures include **2003-12-03 04:24:12 UTC** and **2005-01-01 01:21:07 UTC**.
- Arquivo.pt: 0 relevant rows on the tested exact/prefix surfaces.
- Common Crawl: **inconclusive** because all 32 tested queries failed with 503/504/timeouts; this is not negative archive evidence.
- Confidence:
  - **A for literal Wayback index timestamps/statuses on the tested records**;
  - **OPEN** for when the link first appeared on the source page and whether the payload was ever live/downloadable.
- Evidence boundary:
  - the 2002 index rows prove only that malformed/suffixed forms of the URL reached the archive crawler and returned 404;
  - they do **not** prove client/update bytes existed at those timestamps;
  - successful source-page capture metadata does not by itself prove the StoneAge row was present in the captured body.
- Next gate: replay the dated source-page bodies and inspect the exact StoneAge row/href before assigning a terminus-ante-quem to the link text.

### SRC-DERIVED-SA25-DISCMASTER-SIGNATURE-CARRIERS-R1

- Type: derived DiscMaster file-index search using filenames verified in the recovered StoneAge 2.5-family bridge
- Research date: **2026-09-25**
- Derived report: `research/recovered/STONEAGE-SA25-DISCMASTER-SIGNATURE-CARRIERS-R1.txt`
- Distinctive resource signatures tested: `adrn_15.bin`, `real_15.bin`, `spradrn_5.bin`.
- Supporting generic signatures tested: `StoneAge.exe`, `Startup.exe`, `UNWISE.EXE`.
- Result:
  - all three distinctive resource names returned **0 exact rows**;
  - generic supporting names produced many unrelated weak rows;
  - **0 candidate carriers / 0 strong carriers / 0 errors**.
- Confidence: **A for the bounded negative result on the tested DiscMaster index snapshot**.
- Evidence boundary:
  - bridge filenames can locate related trees but cannot authenticate a carrier as original/clean even if found;
  - generic runtime/uninstaller filenames are not StoneAge evidence by themselves.
- Consequence: the current DiscMaster filename-signature route is **BOUNDED**; reopen only if a new distinctive verified filename, hash, carrier identity or materially changed index becomes available.

### SRC-CN-2021-BAHAMUT-SA25-DISC-COLLECTOR-01

- Title: `石器時代華義國際石器周邊收藏光碟篇（二）`
- Author/account: **寂寞如風 / stoneage2017**
- Publication timestamp shown by live page: **2021-01-07 10:50:13**
- Retrieval/research date: **2026-09-25**
- URL: https://forum.gamer.com.tw/C.php?bsn=1571&snA=81429
- Source type: modern collector article showing/describing surviving StoneAge physical discs; **not** a contemporaneous 2002 primary source and **not** a disc dump.
- Live-page recovery:
  - HTTP 200;
  - exact article title and author recoverable;
  - body explicitly discusses Mainland/Taiwan 2.0 discs, the Mainland `養羊得益包` disc, a Taiwan magazine disc, and then the StoneAge **2.5《精靈王傳說》** disc pair.
- Literal 2.5 collector description:
  - Mainland: `大陸版用戶端統一圖案的光碟`;
  - Taiwan: `臺版盤`, described as having a laser/reflective appearance.
- Exact 2.5 comparison-image URL by article body order:
  - `https://cos.stoneage.cn/uploads/article/minisnsimg/20201222/5fe128b2e6b0a.jpg`.
- Image-recovery status:
  - the `cos.stoneage.cn` image body is currently unreachable from the CI environment;
  - the corresponding older 2020-12 collector-image mirror family was tested with exact Wayback CDX and produced no recoverable 2.5 photograph body;
  - therefore no image-body hash or pixel-level disc match is claimed.
- Confidence:
  - **A for the literal current Bahamut page title, author, timestamp, text and embedded image URL/order**;
  - **B for the collector's physical-carrier identification as modern collector evidence**;
  - **OPEN for original disc mastering, matrix/IFPI, package-to-disc provenance and bytes**.
- Supports:
  - a modern visual/textual control separating the Mainland 2.5 unified client-disc artwork from the Taiwan 2.5 disc artwork;
  - keeping the Mainland 2.0 exception and `養羊得益包` special disc distinct from the normal Mainland 2.5 disc family;
  - precise future comparison of newly exposed physical-media photographs against a source-labelled collector reference.
- Does not support:
  - disc filesystem contents, ISO/hash, installer build, clean-client status or byte identity;
  - that every surviving disc using similar artwork belongs to the same pressing/master;
  - attribution of a photographed loose disc to a specific retail/gift package without an independent package-to-disc chain.
- Derived reports:
  - `research/recovered/STONEAGE-SA25-BAHAMUT-DISC-PART2-R1.txt`
  - `research/recovered/STONEAGE-SA25-BAHAMUT-DISC-IMAGES-R1.txt`
  - `research/recovered/STONEAGE-SA25-COLLECTOR-ARCHIVE-R1.txt`



### SRC-CN-2020-BAHAMUT-SA25-CLIENT-PACKAGES-01

- Title: `石器時代周邊收藏，石器用戶端禮包篇（六）2.5精靈王傳說版用戶端產包`
- Author/account: **寂寞如風 / stoneage2017**
- Publication timestamp shown by live page: **2020-09-21 11:13:04**
- Retrieval/research date: **2026-09-25**
- URL: `https://forum.gamer.com.tw/C.php?bsn=1571&snA=81400`
- Source type: modern collector article documenting surviving StoneAge 2.5 client-package forms; **not** a contemporaneous 2002 primary source and **not** a disc dump.
- Live-page recovery:
  - HTTP 200;
  - body explicitly states that the 2.5 period had many different-cover **新手包**;
  - separately names **延年益壽包** and **春滿乾坤包** as 2.5-period package lines;
  - states the 2.0 WGS gift box was orange and the 2.5 WGS gift box was **green**;
  - explicitly states there was also a **簡裝版的用戶端包裝**.
- Confidence:
  - **A for literal current page title/author/timestamp/text**;
  - **B for collector identification of the surviving packaging forms**;
  - **OPEN for package-to-disc chain, pressing/mastering identity, filesystem and client bytes**.
- Supports:
  - separating several physical carrier classes within the Mainland 2.5 family rather than treating every 2.5 disc/package photograph as one edition;
  - exact-search tokens `2.5 新手包`, `2.5 綠色 WGS 禮盒`, and `2.5 簡裝版用戶端包裝`.
- Does not support:
  - that all packages contained byte-identical discs;
  - any disc label, matrix/IFPI code, ISO checksum, installer filename, or clean-client status.
- Derived report: `research/recovered/STONEAGE-SA25-BAHAMUT-CLIENT-PACKAGE-R1.txt`.


### SRC-CN-2020-SHIQICLUB-SA25-CLIENT-PACKAGE-MIRROR-01

- Current mirror URL: `https://www.shiqi.club/shiqi2712.html`
- Mirror title: `石器周边收藏客户端礼包篇（六）2.5精灵王传说版`
- Page date shown by current/archived mirror: **2020-07-06**
- Retrieval/research date: **2026-09-25**
- Source type: later independent web mirror/repost of the same collector text, useful for redundant text/image preservation; **not** original 2002 evidence.
- Current live page: HTTP 200 and reproduces the same substantive package wording: many-cover 2.5 new-user packages, the 2.5 green WGS gift box, and simplified client packaging.
- Wayback exact-URL preservation:
  - **2022-01-21 08:08:53 UTC** — HTTP 200, replay body 31,620 bytes, SHA-256 `48874043e3621052fd81fe938dee81522f643f0d30372b12dd45b110b0be1ca6`;
  - additional HTTP-200 rows survive at 2023-02-01, 2023-06-10 and 2023-12-04.
- Article-body image mapping:
  - the article contains **11 verified package photographs** under the contiguous upload family `/zb_users/upload/2020/11/202011152141*.jpg`;
  - the first **7** occur before the literal transition `以上就是2,5时期的新手包了`, so they form the article's 2.5 new-user-package photo group;
  - the next **2** occur before `这俩都介绍过了，不再赘述啦`, corresponding to the two previously discussed 2.5 package examples in article order;
  - the next image follows the orange-2.0 / green-2.5 WGS gift-box statement;
  - the final image follows `同时还有简装版的客户端包装`.
- Exact body-image URLs:
  - `https://www.shiqi.club/zb_users/upload/2020/11/20201115214120_55326.jpg`
  - `https://www.shiqi.club/zb_users/upload/2020/11/20201115214121_50470.jpg`
  - `https://www.shiqi.club/zb_users/upload/2020/11/20201115214122_56010.jpg`
  - `https://www.shiqi.club/zb_users/upload/2020/11/20201115214123_96322.jpg`
  - `https://www.shiqi.club/zb_users/upload/2020/11/20201115214123_30074.jpg`
  - `https://www.shiqi.club/zb_users/upload/2020/11/20201115214124_63308.jpg`
  - `https://www.shiqi.club/zb_users/upload/2020/11/20201115214125_59487.jpg`
  - `https://www.shiqi.club/zb_users/upload/2020/11/20201115214125_40259.jpg`
  - `https://www.shiqi.club/zb_users/upload/2020/11/20201115214126_94169.jpg`
  - `https://www.shiqi.club/zb_users/upload/2020/11/20201115214127_96292.jpg`
  - `https://www.shiqi.club/zb_users/upload/2020/11/20201115214128_85742.jpg`
- Confidence:
  - **A for literal mirror text, exact Wayback rows and exact article-body image URLs/order**;
  - **B for package-category association by immediate article-text ordering**;
  - **OPEN for what is printed on each photograph until image bodies are separately inspected/hash-locked**.
- Evidence boundary:
  - this source materially improves **physical-package visual provenance and search-token precision**;
  - it does **not** establish disc contents, original package-to-disc chain, installer bytes, mastering identity or clean-client provenance.
- Derived reports:
  - `research/recovered/STONEAGE-SA25-SHIQICLUB-PACKAGE-MIRROR-R1.txt`
  - `research/recovered/STONEAGE-SA25-SHIQICLUB-BODY-IMAGES-R1.txt`.





### SRC-CN-2016-SMZDM-SA25-INSTALL-DISCS-01

- Title: `此情可待成追忆：记那些年的石器时代`
- Publication timestamp: **2016-06-20 17:32:33**
- Retrieval/research date: **2026-09-25**
- URL: `https://post.smzdm.com/p/462347/`
- Source type: independent modern collector/player post showing surviving original-era installation media; **not** a disc dump and not contemporaneous 2002 documentation.
- Literal install-disc section:
  - the author says the first purchased StoneAge package was a 2.0 new-user package;
  - then explicitly states that **2.5, 3.0, 4.0, 5.0 and 疯狂原始人 installation discs** were still preserved, while some boxes and the 6.0 disc were no longer present.
- Exact section-photo recovery:
  - **6** image URLs recovered from the install-disc section;
  - all six bodies replayed successfully at **1080×607** with **0 errors**;
  - SHA-256 values:
    - `98ad75b6eb5fa5aca6fa7e37095bd207779321ea4991ccf0754117cfaf3884c3`
    - `7e3a7d614f86fbe719ff29ab152c596ab96b712159f9401108fb3434fd083be9`
    - `9aa2a77e75075a25cc5ea773ec7fd79ce3f085160b3352566aabfeb1299edb34`
    - `6378d9b7159209a112de6e0653f89edc9c4c95f06cf01eb30742c9675ffa7b29`
    - `951aae22e52a55c45a72f4d2c59b13248f7115d5278960f09528e4cc2398a074`
    - `6cbdd069c8482d7f4818238c124e4a44faa4aa680f2dd7be3d7e591d0e0762c7`.
- Cross-source visual test:
  - compared against 11 currently recoverable Ruten 2.5 package/disc photographs;
  - the best automatic local-feature result produced **40 RANSAC inliers / 0.0396 inlier ratio**;
  - this is **not promoted as a same-artwork or same-disc match**.
- Confidence:
  - **A for literal surviving text, exact section-photo URLs, image dimensions and hashes**;
  - **B for the author's identification of the preserved disc sequence as independent collector testimony**;
  - **OPEN for exact package-to-photo position, pressing/mastering, matrix/IFPI and disc contents**.
- Supports:
  - an independent second survival chain showing that a Mainland-era StoneAge 2.5 installation disc remained physically preserved in 2016;
  - future exact-photo or physical-carrier comparison.
- Does not support:
  - ISO/filesystem contents, installer build, clean-client provenance, or byte equivalence to any other 2.5 disc/client.
- New image-order resolution:
  - the install-disc section contains **6** photos;
  - photo 1 follows the explicit 2.0 new-user-package description;
  - the article then lists **2.5, 3.0, 4.0, 5.0, 疯狂原始人** and five remaining photos follow in that HTML order;
  - therefore photo 2, `https://am.zdmimg.com/201606/16/5762764a03643.jpg_e1080.jpg`, is a **high-confidence article-order candidate for the 2.5 installation disc**, not a byte-level identification.
- Evidence boundary for the order mapping:
  - the page/order association can guide visual matching;
  - it does not establish volume label, filesystem, installer build, pressing/mastering identity, matrix/IFPI or clean-client provenance.
- Derived reports:
  - `research/recovered/STONEAGE-SA25-SMZDM-DISC-R1.txt`
  - `research/recovered/STONEAGE-SA25-SMZDM-DISC-ORDER-R1.txt`.
- 2.0 photo-1 cross-check refinement — 2026-09-25:
  - HTML order maps photo 1 directly after the author's `2.0新手报到包` statement; the transient body replays with the previously locked SHA-256 `98ad75b6eb5fa5aca6fa7e37095bd207779321ea4991ccf0754117cfaf3884c3`;
  - a dedicated R2 SIFT/RANSAC pass loaded **9/9** early Mainland Ruten controls with **0 errors**;
  - the top two coherent matches are both from Beijing-Waei/new-user control `22631284715652`: **64 inliers / 0.3902 ratio** and **64 / 0.4324**, both with valid quadrilateral geometry;
  - these signals are stronger than the other tested controls but remain below the project's promotion threshold, so they are recorded as **visual-family evidence only**, not same-disc/same-package proof.
- Supersession note:
  - `STONEAGE-SA20-SMZDM-RUTEN-MATCH-R1.txt` is an environment-failure record (OpenCV absent) and carries no negative historical conclusion;
  - R2 supersedes it for visual-analysis results.
- Derived report:
  - `research/recovered/STONEAGE-SA20-SMZDM-RUTEN-MATCH-R2.txt`

### SRC-CN-2013-XUNLEI-SA25-CLIENT-LEAD-01

- Surviving source page: `https://www.7chaowan.com/55833.html`
- Original-post context shown by surviving page: **2013-08**, with a later `elize.ini` edit dated **2013-08-23**
- Retrieval/research date: **2026-09-25**
- Exact client URL: `http://kuai.xunlei.com/d/DX1fAAJeiQBWT-tR9ee`
- Source type: later community/private-server distribution lead, explicitly separating a StoneAge 2.5 **client download** from the server download.
- Important source caveat:
  - the poster states that the client's `elize.ini` had been modified for a LAN/internal-network address and later supplied a 127.0.0.1 replacement;
  - therefore even recovered bytes would be a **descendant/private-server client specimen**, not authenticated 2002 retail-disc bytes.
- Preservation probe:
  - Wayback exact CDX: **0 rows**;
  - Wayback prefix CDX: **0 rows**;
  - Wayback Availability at 2013-08-01, 2013-08-23, 2013-12-31 and 2014-12-31: **no available snapshots**;
  - Arquivo.pt exact URL: **0 rows**;
  - CI retrieval of the present source page: HTTP 403.
- Operational status: **EXACT TOKEN RECORDED / TESTED ARCHIVE ROUTE BOUNDED**. Reopen only from a new mirror/re-upload, filename, checksum, archived redirect or preservation corpus.
- Confidence: **B for the literal surviving source-page description and exact URL as independently visible on the public web; A for the tested archive-index negative result; OPEN for payload filename, size, hash and contents**.
- Does not support:
  - original Waei distribution provenance;
  - clean-client status;
  - byte equality with the 2002 575/580 MB full package or any physical-disc carrier.
- Derived report: `research/recovered/STONEAGE-SA25-XUNLEI-CLIENT-R1.txt`.


### SRC-CN-2020-BAHAMUT-SA25-YANNIAN-PHYSICAL-01

- Title: `石器時代周邊收藏——用戶端禮包篇（一）延年益壽包`
- Author/account: **寂寞如風 / stoneage2017**
- Publication timestamps:
  - Bahamut forum: **2020-09-01 15:21:31**
  - Bahamut creator page: **2020-09-01 15:19:18**
- Retrieval/research date: **2026-09-25**
- URLs:
  - `https://forum.gamer.com.tw/C.php?bsn=1571&snA=81388`
  - `https://home.gamer.com.tw/artwork.php?sn=4902119`
- Source type: modern collector documentation of a surviving Mainland StoneAge package; **not** a contemporaneous 2002 source and **not** a disc dump.
- Literal high-value observations:
  - the article identifies the package as `延年益壽包`;
  - a photographed item is explicitly labelled `2.5時期的光碟`;
  - the next photographed item is explicitly labelled `2.5版本的說明書`.
- Contemporaneous cross-controls:
  - the 17173 StoneAge 2.5 upgrade page places the 2.5 retail rollout in January/February 2002, identifies the 580 MB full upgrade and 8.25 MB updater, and names `春满钱坤包` / `延年益兽包` as upgrade-acquisition products;
  - a Sina Technology interview dated 2002-02-08 states that 联邦、智冠、华义 would issue a limited `石器时代延年益寿包` on 2002-02-09.
- Name-normalization warning: preserve each source's literal form (`益壽` / `益寿` / `益兽`); spelling variation is not byte provenance.
- Public-byte search status:
  - exact package/title/article-token queries combined with ISO / 光盘镜像 / 光碟 / 客户端 / 下载 returned collector/retrospective material but no verifiable ISO, raw disc image, complete file tree or hash tied to this exact specimen in this pass.
- Corrected exact article-body disc-photo recovery:
  - the initial broad-context forum probe produced a false association with an `延伸閱讀` thumbnail and is **superseded**;
  - R2 restricts extraction to the HTML interval between `2.5時期的光碟` and `2.5版本的說明書`, preferring the Bahamut creator page with forum fallback;
  - both pages resolve the same exact source-labelled photo: `https://truth.bahamut.com.tw/s01/202009/1eabce5c4adf3b26366bebea7d788c74.JPG`;
  - recovered photograph: **160,151 bytes**, **1128×774**, SHA-256 `385071cb52f3e9af540823ff8a1833cfba4dad04ee8ab2ee9beebfa67dadea6a`, dHash `f070e0606068a1c0`;
  - this checksum identifies the **photograph body only**, not the CD/ISO/client bytes.
- Cross-source visual controls:
  - best tested Ruten comparison: carrier `22632305238624` image 3, **112 RANSAC inliers / 0.1181 inlier ratio**;
  - independent SMZDM article-order 2.5 candidate: **10 RANSAC inliers / 0.0111 inlier ratio**;
  - these metrics rank visual follow-up only and do not prove disc identity, pressing/mastering identity, or byte equality.
- Provenance hygiene: do not reuse the superseded extension-thumbnail URL as the 延年益壽 2.5 disc image.
- Confidence:
  - **A for current-page title/author/timestamps and literal collector labels**;
  - **B for physical-carrier classification when cross-read with contemporaneous 2.5 product material**;
  - **OPEN for package-to-disc chain, volume label, matrix/IFPI, filesystem, installer filename, ISO/hash, mastering identity and byte equality**.
- Research consequence:
  - treat this article/specimen as a high-value surviving-physical-carrier identity control;
  - prioritize any future public read/listing/dump that can connect this carrier to a disc file tree and cryptographic hashes;
  - do not infer field-map dates or clean-client bytes from the photographs alone.
- Derived reports:
  - `research/recovered/STONEAGE-SA25-BAHAMUT-YANNIAN-PHYSICAL-R1.txt`
  - `research/recovered/STONEAGE-SA25-BAHAMUT-YANNIAN-DISC-PHOTO-R1.txt`.


### SRC-TW-2026-RUTEN-SA25-PHYSICAL-01

- Retrieval/research date: **2026-09-25**
- Surface: Ruten public search, public product/detail JSON metadata, public item HTML and public seller photographs.
- Source type: modern marketplace survival evidence; **not** a contemporaneous 2002 source, **not** a disc read, and **not** clean-client byte provenance.
- Separately addressable StoneAge 2.5 listing controls:
  - `22632305238624`: boxed **2.5 精靈王傳說新手報到包** with original-package/game-disc wording; listed **2026-08-04**; public metadata exposes **9 full-size photographs**;
  - `21926883918096`: loose **2.5版 精靈王傳說** game-disc listing; listed **2019-06-28**; public page shows used-condition metadata, Taiwan/Kaohsiung and literal tag **`#公司貨`**;
  - `22242541948520`: separate loose **2.5版 精靈王傳說 PC GAME** listing; listed **2022-10-19**;
  - `22615474551866`: **`精靈王傳說 石器時代2.5版 遊戲片+外盒`**; listed **2026-04-11**; used-condition metadata, Taiwan/Kaohsiung, sold quantity 1 / current stock 0; three full-size public image filenames `22615474551866_647.jpg`, `_438.jpg`, `_740.jpg`.
- Important independence boundary:
  - separate listing IDs, dates and sellers make these separately addressable marketplace provenance chains;
  - they do **not** by themselves prove seven independently surviving physical discs, because image reuse/resale/common-source photography remains possible.
- Visual-fingerprint controls:
  - the two loose-disc listing photographs `21926883918096:0` and `22242541948520:0` have a very strong cross-listing match: **743 RANSAC inliers / 0.4831 inlier ratio**. This may reflect the same disc-face artwork, closely related photography, or reused imagery; it is **not** proof of two independent physical specimens.
  - new disc+box image `22615474551866:1` (`_438.jpg`) matches those two loose-disc images at **266 / 0.2323** and **253 / 0.2202** respectively, placing the three images in a strong visual family.
  - other images from the new disc+box listing show weaker but nonzero cross-listing relationships; use them only for carrier-family ranking.
- Corrected Yan-Nian source-labelled disc cross-control:
  - exact Bahamut Yan-Nian disc photograph remains SHA-256 `385071cb52f3e9af540823ff8a1833cfba4dad04ee8ab2ee9beebfa67dadea6a`;
  - its strongest previously tested Ruten match remains boxed carrier `22632305238624` image 3 at **112 / 0.1181**;
  - against the new `22615474551866` images, results are only **11 / 0.0118** (`_438.jpg`), **11 / 0.0120** (`_740.jpg`) and **7 / 0.0091** (`_647.jpg`);
  - therefore the new disc+box visual family must **not** be merged with the Yan-Nian source-labelled disc family on current evidence.
- Regional/artwork interpretation boundary:
  - collector sources independently describe Mainland and Taiwan 2.5 disc artwork as distinct;
  - the visual clustering above is compatible with multiple disc-art families but is **insufficient to label the new Ruten cluster Mainland/Taiwan, identify a pressing, or infer package origin**.
- Marketplace-claim boundary:
  - literal tags such as `#公司貨`, condition fields and seller titles are retained as marketplace claims only and are not operator-disc authentication.
- Public-byte status:
  - no matrix/IFPI, volume label, filesystem, installer hash, ISO/raw image, optical-disc checksum or clean-client bytes are exposed by these listings;
  - exact product IDs/titles and targeted preservation-index searches have not yielded a public disc dump/file tree so far.
- Operational consequence:
  - use all seven listing IDs, exact full-size photograph URLs/filenames and derived image hashes as matching keys for future public preservation reads/dumps;
  - prioritize a future dump only when it can be linked to one of these carriers or another provenance-bearing original disc;
  - do **not** require purchase, seller contact, shipping, or user-performed dumping.
- Derived reports:
  - `research/recovered/STONEAGE-SA25-RUTEN-PHYSICAL-R1.txt`
  - `research/recovered/STONEAGE-SA25-RUTEN-PROVENANCE-METADATA-R1.txt`
  - `research/recovered/STONEAGE-SA25-PHYSICAL-IMAGE-FINGERPRINTS-R4.txt`
  - `research/recovered/STONEAGE-SA25-BAHAMUT-YANNIAN-DISC-PHOTO-R1.txt`.


- Fifth addressable listing / independence correction:
  - product `22445165101247`: `遊戲光碟 石器時代 2.5版 精靈王傳說 全新完整版 PC GAME 電腦遊戲 D80`;
  - same Ruten seller account as `22242541948520` (`alixson7`);
  - raw `post_time=1731002663` and one full-size public image `https://gcs.rimg.com.tw/g1/d/30/bf/22445165101247_815.jpg`;
  - image body: **67,565 bytes**, **800×600**, SHA-256 `f7835bb1c544ee3de89578f5161f5169edc2ee1e495de0368161f8d0dfb9fc78`.
- R4 cross-listing visual result:
  - `22242541948520:0` vs `22445165101247:0`: **1,581 RANSAC inliers / 0.7543 inlier ratio**;
  - `21926883918096:0` vs `22445165101247:0`: **977 / 0.5586**;
  - these are far stronger than ordinary cross-listing background overlap and establish a very tight shared photographic/artwork family, but still do not prove the same physical disc.
- Independence consequence:
  - the Ruten control surface now has **seven separately addressable listing IDs, not seven independently proven physical specimens**;
  - because `22445165101247` and `22242541948520` share the same seller and extremely strong visual overlap, the newer/alternate listing is treated as a **same-seller duplicate-family control**, not additive independent-disc evidence.

- Sixth/seventh public carrier expansion:
  - `22637629794063`: exact listing title **`石器時代2.5，精靈王傳說`**, one full-size public image `22637629794063_117.jpg`, 600×800, SHA-256 `c6d6e985acadb0b9ce1e9f1aad48522b386015d57a17918e8fb8511e48570abe`;
  - `22625938678558`: literal Taiwan collection title **`臺版 石器時代 精靈王傳說 瑪蕾菲雅許願盒 家族開拓史 電腦遊戲光碟 合集（20張不分）收藏`**, with seven full-size public photographs.
- Current visual-fingerprint rerun:
  - the new single-disc image `22637629794063:0` has only low-strength overlap with the previously identified duplicate-family controls (for example **25 / 0.0248** against `22632305238624:0`, **24 / 0.0221** against `22242541948520:0`); it is therefore kept as a **separate visual candidate**, not merged into the old high-overlap cluster;
  - collection image `22625938678558:3` (`_730.jpg`) overlaps `22445165101247:0` at **136 RANSAC inliers / 0.1339**, `22242541948520:0` at **74 / 0.0729**, and `21926883918096:0` at **37 / 0.0364**. This is consistent with the collection photograph containing a carrier/artwork object related to the known loose-disc family, but it does **not** prove the same physical disc, pressing or mastering.
  - all **23** full-size Ruten targets in the expanded seven-listing set loaded successfully; the two visual-probe errors were only the already-known unreachable external source-labelled comparison/collector bodies, not Ruten images.
- CI confirmation:
  - provenance metadata run **36094031445** — success;
  - Ruten physical-media run **36094173065** — success;
  - visual-fingerprint run **36094173076** — success.

### SRC-JP-2008-IPVE-SA174GM-MIRROR-01

- Page: `https://www.ipve.com/bbs/viewthread.php?extra=&page=5&tid=84383`
- Post timestamp shown: **2008-08-07 21:10**
- Author shown: `SmileBoy`
- Retrieval/research date: **2026-09-25**
- Source type: later community repost preserving a Japanese StoneAge service/download URL; not a 2003 first-party launch source.
- Literal identifiers:
  - Japanese official-site label: `http://www.stoneage.to`;
  - exact download URL: `http://file2.gamania.co.jp/sa/sa174gm.exe`;
  - account-registration URL under `stoneage.to`;
  - attribution line says the material was reposted from `石器的天空`.
- Confidence:
  - **A for the literal current page timestamp/text/URL**;
  - **B for this being a historical Japanese-service distribution pointer in 2008**;
  - **OPEN for original introduction date, payload bytes, version/build and equality with `sa174hg.exe`**.
- Supports:
  - treating `sa174gm.exe` and exact `file2.gamania.co.jp/sa/` path as a new precise Japanese-client recovery token.
- Does not support:
  - that the file was unchanged since 2003;
  - that the file was version 1.74a;
  - that `gm` and `hg` packages are byte-identical.
- Derived note: `research/clients/STONEAGE-JAPAN-SA174GM-GAMANIA-RECOVERY-R1.md`.

- Exact/prefix public-preservation probe — R2:
  - Wayback exact HTTP and HTTPS queries normalize to the same single indexed object: **2013-02-10 10:10:13 UTC**, HTTP **503**, MIME `text/html`, length **399**, digest `CSYD2PXMVLZFP376UJSTVBBFRCMOCGUL`; this is not a client payload;
  - Wayback Availability at **2003-12-11**, **2003-12-12**, **2004-01-01** and **2008-01-01** returns no closest snapshot for either exact target;
  - Wayback prefix query for `file2.gamania.co.jp/sa/*`: **0 rows**, therefore no neighboring `sa174gm` capture was exposed on that tested prefix surface;
  - Arquivo.pt exact HTTP query: **0 rows**;
  - Arquivo.pt exact HTTPS query: **0 rows**;
  - Internet Archive advanced search for `sa174gm.exe / sa174gm`: **0 documents**;
  - current direct host lookup failed DNS in the CI runner and is not treated as archival absence;
  - exact/prefix HTTP-200 payload candidates: **0**; no client bytes, hash or file tree recovered.
- Operational status: **IDENTITY RESOLVED / TESTED WAYBACK+ARQUIVO+IA SURFACE BOUNDED FOR BYTES**. Reopen this exact branch only from a new mirror, corpus, checksum, upload token, physical carrier or independently sourced URL/path.
- Derived archive report: `research/recovered/STONEAGE-JAPAN-174A-GAMANIA-MIRROR-R1.txt`.
- Probe resolution: `GAMANIA_SA174GM_PUBLIC_INDEX_SURFACE_BOUNDED`.

### SRC-CN-2020-SHIQILA-SA174GM-ATTACHMENT-01

- Page: `https://shiqi.la/forum.php?mod=viewthread&tid=16671`
- Title: `sa174gm.exe日版石器时代主程式安装档2003年12月11日`
- Post timestamp shown: **2020-06-05 08:16:13**
- Author shown: `shiqila`
- Retrieval/research date: **2026-09-25**
- Source type: later community preservation/re-upload carrier; not a first-party 2003 source.
- Public attachment metadata:
  - installer archive: `sa174gm[解压密码www.shiqi.la].rar`, **194.24 MB**, stable Discuz attachment-id component **675**, displayed upload time **2020-06-05 08:13**, displayed price **10 石币**;
  - installed/portable archive: `Stoneage.rar`, **174.72 MB**, stable attachment-id component **676**, displayed upload time **2020-06-05 08:15**, displayed price **15 石币**.
- Discuz-token stability correction:
  - repeated public page fetches changed the encoded token's embedded hash/timestamp fields;
  - only numeric attachment IDs **675** and **676** are treated as stable attachment identities;
  - the full encoded or decoded Discuz token must not be recorded as a permanent download locator.
- Access boundary:
  - anonymous attachment requests return HTTP 403;
  - no login/payment/access-control bypass is attempted.
- Date boundary:
  - `2003年12月11日` is part of a **2020 thread title**;
  - until independently confirmed by period evidence or authenticated file metadata, it remains an attributed later claim rather than FACT.
- Confidence:
  - **A for visible current page metadata, attachment names/sizes and stable attachment-id components**;
  - **B/C for the uploader's “日本原版” / date attribution**;
  - **OPEN for archive bytes, hashes, members, installer metadata and clean provenance**.
- Does not support:
  - direct version-1.74a attribution;
  - equality with the official Hangame `sa174hg.exe` package;
  - use of the compressed RAR size as a comparison against Hangame's 248 MB display-size token.
- Derived note: `research/clients/STONEAGE-JAPAN-SA174GM-GAMANIA-RECOVERY-R1.md`.


### SRC-CN-2012-WELOVESA-SA25-CLEAN-TID2132-REFRESH-01

- Source surface: WeLoveSA `客戶端程式/工具` public forum index.
- Thread title: `〖2.5纯净〗石器客户端`
- Thread ID: **2132**
- Author: **rayrix**
- Original indexed date: **2012-09-26**
- Refresh/research date: **2026-09-25**
- Public index URL: `https://lab.welovesa.com/forumdisplay.php?fid=40`
- Current public-index state observed:
  - **45 replies / 991 views**;
  - last reply shown as **2026-09-16 01:02** by **mh713**;
  - thread remains labelled `售價 石幣 5`.
- Refresh search:
  - exact title, author, `tid=2132`, page-number, Discuz archiver/WAP forms, and common file-host terms were tested on current public indexes;
  - no publicly indexed client filename, archive filename, download URL, attachment ID, cloud-share ID, size or checksum was recovered in this pass.
- Access boundary:
  - no login, forum-coin purchase, paid-topic access, cookie reuse, or access-control bypass was attempted;
  - `纯净` remains a **source title**, not a verified clean-client conclusion.
- Confidence:
  - **A for current public index title/author/date/reply-view/latest-reply metadata**;
  - **OPEN for payload identity, present payload availability, cleanliness and provenance**.
- Operational consequence:
  - the thread is still an active/live high-value lead but its anonymous public surface remains bounded;
  - reopen only from an independently public repost/mirror, exact filename, share ID, checksum, file-tree evidence, or other new payload token.
- Derived refresh report: `research/recovered/STONEAGE-SA25-PUBLIC-CLEAN-LEADS-REFRESH-R1.txt`.

### SRC-CN-2025-CANGBAOWAN-SA25-BAIDU-01

- Title: `石器时代2.5版，网盘里翻出来的`
- Author: **saiya141**
- Public post timestamp: **2025-09-26 09:11:13**
- Retrieval/research date: **2026-09-25**
- Public post URL: `https://www.cangbaowan.vip/thread-9642-1-1.html`
- Exact public Baidu share:
  - URL: `https://pan.baidu.com/s/1a2cOmPxo5GjFPFfU5Mj2Ug`
  - share ID: **`1a2cOmPxo5GjFPFfU5Mj2Ug`**
- Access boundary:
  - the extraction-code field is behind the forum's 50-coin topic boundary;
  - no purchase, login, code guessing or access-control bypass was attempted.
- Current public-share result:
  - direct anonymous Baidu landing returns HTTP 200 with title **`百度网盘-链接不存在`** and explicit missing/invalid-state text;
  - corrected probe resolution: **`PUBLIC_BAIDU_SHARE_DEAD_OR_MISSING`**;
  - successful Wayback exact/prefix checks on the tested share forms return **0 rows**; one trailing-slash exact request timed out and is not counted as negative evidence;
  - Internet Archive exact share-ID search returns **0 documents**.
- Exact-token public search:
  - the share ID, complete Baidu URL, exact post title and title+author combinations were searched;
  - no independent public repost with extraction code, archive filename, size, checksum or file tree was found.
- Source classification:
  - modern community/cloud-drive recovery lead whose **current direct Baidu route is dead/missing**;
  - not operator-era 2002 provenance and not proof of a clean client.
- Confidence:
  - **A for public post identity, exact share ID and current Baidu missing-link state**;
  - **A for bounded zero-row results on the successful tested archive-index calls**;
  - **OPEN for former payload identity/bytes, cleanliness and relation to known 2.5 corpora**.
- Operational consequence:
  - retain `1a2cOmPxo5GjFPFfU5Mj2Ug`, thread `9642` and author `saiya141` only as mirror/repost recovery keys;
  - do not spend primary recovery effort on the dead direct Baidu route unless a new mirror, extraction-code repost, filename, checksum or file-tree token appears.
- Derived reports:
  - `research/recovered/STONEAGE-SA25-PUBLIC-CLEAN-LEADS-REFRESH-R1.txt`
  - `research/recovered/STONEAGE-SA25-CANGBAOWAN-BAIDU-R1.txt`.

### SRC-CN-2017-JUDINGWAN-SA25-ONECLICK-01

- Source chain:
  - 2017-01-03 public repost: `https://www.80give.com/forum.php?extra=&mod=viewthread&ordertype=1&page=3&tid=1422`
  - later public reposts include the 2022 "最新某宝 所有网游单机版" lists.
- Literal package label: **`〖飓鼎玩〗石器时代 v2.5版`**
- Legacy public share/code: `https://pan.baidu.com/s/1eS9MzOe` / `qnsv`.
- Later public share/code: `https://pan.baidu.com/s/1nu7DLcX` / `ylru`.
- Source-list context:
  - the 2017 list separately labels **`〖飓鼎玩赠品〗石器时代2.5GM工具全套`**;
  - the same distributor list supplies a generic extraction-password marker `http://www.judwan.com` for the package group.
- Public-code verification, no login and no payload download:
  - both the legacy and later share codes verify successfully through Baidu's normal public share flow;
  - both expose the same main object name **`石器时代v2.5一键端.exe`**;
  - both expose the same size **441,183,848 bytes**;
  - both expose the same Baidu file identifier **`fs_id=146116179281676`**;
  - the later share additionally exposes **`【飓鼎玩】石器时代2.5安装教程.rar`**, **17,963,524 bytes**, `fs_id=802517119665785`.
- Interpretation:
  - filename + byte size + identical Baidu `fs_id` across the two share generations establish a stable platform-level identity for the main one-click object across the tested repost chain;
  - this is **not a cryptographic payload hash** and does not establish equality to any original 2002 disc/client.
- Exact public filename/`fs_id`/size search:
  - no operator-era source, original-disc attribution, checksum, or stronger historical mirror was surfaced in this pass.
- Classification:
  - **DESCENDANT / ONE-CLICK INTEGRATION CONTROL**;
  - the one-click EXE packaging, separate installation tutorial and separately distributed GM tools are inconsistent with treating this as an untouched 2002 operator client merely from its "v2.5" label.
- Operational consequence:
  - retain exact filename, sizes, two share IDs and `fs_id` values as descendant/common-corpus comparison tokens;
  - do not spend primary clean-client recovery effort downloading the 441 MB one-click payload unless independent provenance emerges.
- Derived report: `research/recovered/STONEAGE-SA25-BAIDU-SHARE-METADATA-R1.txt`.

### SRC-CN-2022-246SA-SA25-ONECLICK-01

- Source post: `https://www.iopq.net/forum.php?mod=viewthread&tid=17113443`
- Title: `分享一下大神去验证的246SA一键端石器时代2.5大屏版`
- Original post timestamp: **2022-06-09 14:10:07**
- Public source description:
  - explicitly states **客户端与服务端全套**;
  - states that the de-verification modification involves replacing `gmsv`;
  - thread replies discuss one-click/server behavior and note encrypted Lua in the bundle.
- Exact public Baidu share/code:
  - `https://pan.baidu.com/s/1cHlV27B0rckWGC2cH21dGg?pwd=7ck4`
  - code `7ck4`.
- Current public-share result:
  - direct Baidu landing now returns **`百度网盘-链接不存在`**;
  - corrected generic metadata probe classifies it **MISSING**;
  - no file name, size, hash or file tree was recovered before the current dead-link boundary.
- Classification:
  - modern client+server one-click/private-server bundle;
  - descendant engineering control only, not a clean/operator 2.5 client lead.
- Operational consequence:
  - retain the exact share ID/title as a repost search token;
  - current direct share route is bounded/dead and should not receive primary recovery effort without a new mirror.
- Derived report: `research/recovered/STONEAGE-SA25-BAIDU-SHARE-METADATA-R1.txt`.


### SRC-CN-2020-SHIQIBLOG-SA25-DISC-MIRROR-01

- Title: `回忆石器时代2.5游戏光盘`
- Current mirror/source page: `https://blog.shiqi.so/shiqi273.htm`
- Page timestamp shown: **2020-12-22 08:38**
- Retrieval/research date: **2026-09-25**
- Source type: modern collector mirror/article preserving StoneAge disc photographs and literal Mainland/Taiwan labels; **not** a 2002 operator source and **not** a disc dump.
- Literal 2.5 wording:
  - `到2.5精灵王传说版本啦`;
  - `上面是大陆版客户端统一图案的光盘`;
  - `下面是台版盘，有点镭射反光的感觉，很好看`.
- Exact article-order mapping from the R2 between-image parser:
  - image 3: `https://shiqifabu.fszye.com/zb_users/upload/2020/12/20201222082536160859673637393.jpg`;
  - the literal 2.5 Mainland/Taiwan label block occurs **between image 3 and image 4**;
  - image 4 immediately following the label block: `https://shiqifabu.fszye.com/zb_users/upload/2020/12/20201222082537160859673711005.jpg`;
  - the next between-image segment begins the article closing text, so image 4 is the article-order **source-labelled 2.5 Mainland/Taiwan comparison image**.
- Important association boundary:
  - the article-order/text relationship establishes image 4 as the comparison image;
  - without a recoverable image body, the project does **not** independently inspect/verify the pixel-level upper/lower disc arrangement.
- Image-body recovery result:
  - direct CI read of image 4: connection refused;
  - exact Wayback CDX for both HTTPS and HTTP image-4 URLs: **0 rows**, successful CDX responses;
  - corresponding Bahamut/COS exact 2.5 comparison-image URL `https://cos.stoneage.cn/uploads/article/minisnsimg/20201222/5fe128b2e6b0a.jpg`: direct read connection refused; tested CDX requests also failed transport and are therefore **inconclusive**, not negative archive evidence.
- Visual-fingerprint hygiene:
  - R5 now allows only source-qualified collector body images; sidebar/recommendation images are rejected as comparison references;
  - because neither source-labelled comparison image body was recovered, **no Ruten listing is assigned Mainland/Taiwan identity from pixel similarity**.
- Workflow/result:
  - source-labelled recovery run **36091418849** completed successfully;
  - report: `research/recovered/STONEAGE-SA25-SOURCE-LABELLED-COMPARISON-IMAGE-R1.txt`;
  - context report: `research/recovered/STONEAGE-SA25-COLLECTOR-MIRROR-CONTEXT-R1.txt`.
- Confidence:
  - **A for live article text, exact image URL/order and exact between-image association**;
  - **OPEN for image-body hash/pixels, optical-disc pressing/mastering and byte provenance**.
- Operational consequence:
  - preserve the two exact source-labelled comparison-image URLs as visual recovery keys;
  - do not substitute sidebar images or infer Mainland/Taiwan assignment for the current Ruten visual cluster until one of these exact image bodies is publicly recoverable.


### SRC-CN-2011-CANGBAOWAN-SA25-ONECLICK-115-01

- Source thread: `https://www.iopq.net/thread-16731619-1-1.html`
- Author: **5615918**
- Posted: **2011-07-21 08:55:58**
- Edited: **2011-08-04 10:21**
- Retrieval/research date: **2026-09-25**
- Source type: community single-player/private-server engineering distribution; **not** operator-era client provenance.
- Explicit lineage statement:
  - the author thanks **love198959** for the earlier StoneAge 2.5 post, then describes this as a newly assembled one-click installation;
  - the earlier 2009 `love198959` post separately exposes client URL `http://download1.92ysa.com/YSA2.5.8.rar` and separately packaged server/login tooling.
- 2011 engineering layout explicitly names:
  - `石器时代WIN版服务端管理器.exe`;
  - `SACH-MX0.30/STW0.30.exe`;
  - `D:/csa/gmsv/stoneage2.5/sa_2903.exe`.
- Exact public recovery token:
  - `http://u.115.com/file/clnrsbsc`;
  - later `http://115.com/file/clnrsbsc#`;
  - token **`clnrsbsc`**;
  - filename **`石器时代2.5精灵王的传说一键.zip`**.
- Purity/integrity warning:
  - a source-thread reply states that the extracted `GMSV` directory lacked `GMSV.EXE` and that the user copied a 2.5 Windows server executable from another site;
  - the package therefore has direct same-period evidence of incomplete/mixed engineering use and cannot be promoted as a clean client.
- Preservation probe:
  - GitHub Actions run **36092086106** — success;
  - successful Wayback exact/prefix queries: **0 HTTP-200 rows**;
  - successful Arquivo.pt exact queries: **0 rows**;
  - Internet Archive exact token/filename searches: **0 documents**;
  - two Wayback variants timed out and remain inconclusive;
  - no payload bytes, checksum or file tree recovered.
- Current mirror:
  - `https://www.7chaowan.com/52247.html` preserves the same 2011 instructions and 115 token but exposes no independent payload hash or new host.
- Confidence:
  - **A for current source-page text, timestamps, exact 115 token/filename and explicit author credit**;
  - **B for broad descendant-lineage relationship to the earlier community distribution**;
  - **OPEN for byte identity among the 2009 YSA client, 2011 ZIP, recovered 2012 MediaFire bridge or later descendant corpora**.
- Evidence boundary:
  - source relationship is not byte relationship;
  - no claim of original Beijing-Waei disc provenance, clean-client status or pre-2003 map provenance is supported.
- Derived records:
  - `research/recovered/STONEAGE-SA25-115-LINEAGE-PROBE-R1.txt`;
  - `research/clients/STONEAGE-SA25-2009-2011-DESCENDANT-LINEAGE-R1.md`.
- Status: **DESCENDANT LINEAGE CONTROL / TESTED PUBLIC PRESERVATION SURFACE BOUNDED**.

### SRC-TW-2026-RUTEN-EARLY-REGIONAL-CARRIERS-01

- Retrieval/research date: **2026-09-25**
- Source type: current public Ruten marketplace photographs/item metadata used as **surviving physical-carrier evidence**, not as operator-era publication evidence or byte provenance.
- Primary public item IDs:
  - `22625938996449` — Taiwan Traditional-Chinese StoneAge client/package listing; six public images;
  - `22631285251243` — Taiwan client/package control; five public images;
  - `22631285248430` — `晴界包` package control;
  - `22631284715652` — Beijing-Waei/new-user-package control;
  - `22636573895893` — photographed Mainland WAEI/WGS StoneAge retail box;
  - `22638643800877` — photographed boxed StoneAge disc/package.
- Taiwan package evidence:
  - `22625938996449` visibly uses Traditional Chinese and carries a WGS support/billing sticker;
  - the sticker states that StoneAge supports the **WGS billing system** and advertises WGS point-card availability through convenience stores, 3C retailers and chain bookstores;
  - `22631285251243` does **not** add five independent photographs: all five corresponding dHashes are identical, with **3,609–4,702 RANSAC inliers / 0.9904–1.0000**; one pair is SHA-256 byte-identical;
  - therefore those two pages form one reused-photo family for the shared five images.
- Taiwan v1.0 comparison boundary:
  - accepted Redump 104630 remains independently anchored by `P-RPG-0008`, barcode `4710739350098`, and its mastering-ring evidence;
  - no exact `P-RPG-0008` / `4710739350098` identifier has yet been recovered from these Ruten package photographs;
  - no same-edition or same-disc claim is made.
- Mainland package evidence:
  - `22636573895893` visibly carries WAEI/WGS StoneAge branding;
  - its small photographed identifier area was initially transcribed as **`7-900032-57-0` / `9787900032570`**, but both fail their ISBN-10/EAN-13 checksums; if the preceding digits are correct, checksum-consistent final-digit hypotheses are **`7-900032-57-6` / `9787900032577`**;
  - neither final digit is independently confirmed from the current photograph, so the printed identifier remains **OPEN**;
  - `22638643800877` visibly exposes **`www.waei.com.cn`** on the disc face.
- Preservation passes:
  - R1 GitHub Actions run **36096287039**, attempt 2 — **success** — tested the initial transcription strings and context variants;
  - R2 GitHub Actions run **36097696696** — **success** — separately tested checksum-consistent hypotheses `7-900032-57-6` / `7900032576` / `9787900032577` while retaining them as hypotheses only;
  - R2 aggregate across eight initial/hypothesis/context queries: **0 strict DiscMaster hits / 0 strict Internet Archive items / 0 errors**;
  - the hyphenated initial and hypothetical ISBN queries each returned one raw DiscMaster row, but neither passed the strict StoneAge/operator filter and neither is a candidate.
- Confidence:
  - **A for current public Ruten item IDs, image availability/hashes and exact duplicate-photo metrics**;
  - **A for the visible WAEI/WGS branding and other clearly readable current-photo details**;
  - **OPEN for the printed identifier final digit, original release version, disc matrix/IFPI, filesystem, installer hashes and byte relationship to recovered clients**.
- Operational consequence:
  - retain the initial transcription only as a tested photo-reading record, not as a confirmed identifier;
  - checksum-consistent hypotheses have now been tested separately and remain hypotheses only;
  - do not repeat the same DiscMaster/IA passes for either the initial strings or checksum hypotheses absent a new corpus or token;
  - count the two Taiwan listing pages conservatively as one shared photographic source family;
  - prioritize a public read/dump/file tree, matrix/volume label or installer checksum tied to one of these physical carriers.
- Canonical note: `research/clients/STONEAGE-EARLY-RUTEN-REGIONAL-CARRIERS-R1.md`.
- Derived reports:
  - `research/recovered/STONEAGE-EARLY-RUTEN-CARRIERS-R1.txt`;
  - `research/recovered/STONEAGE-EARLY-RUTEN-CARRIER-FINGERPRINTS-R1.txt`;
  - `research/recovered/STONEAGE-MAINLAND-RETAIL-ISBN-PROBE-R1.txt`.
### SRC-CN-2020-SA85-SA20-PACKAGE-MIRROR-01

- Current public mirror: `https://www.sa85.com.cn/shiqi2710.html`
- Mirror title: **`石器时代周边收藏客户端礼包篇（五）2.0版本礼盒`**
- Retrieval/research date: **2026-09-25**
- Source type: later collector mirror preserving package photographs and a literal 2.0-version label; **not** contemporaneous operator publication and **not** byte provenance.
- Recovered visual relationship:
  - collector article image `mirror-20:2` SHA-256 `bf736ab3ba6d860c0faece641ae8a199a35ed5e6616ddc883ad001b5301e6c6f`;
  - Ruten item `22631284715652` images 0–3 produce **400 / 328 / 317 / 129 RANSAC inliers** against that reference;
  - first-three inlier ratios: **0.8403 / 0.8059 / 0.8212**;
  - first-three collector-reference target coverage: **0.9070 / 0.9054 / 0.8793**.
- Interpretation:
  - the overlap is far stronger than ordinary shared StoneAge logo/artwork signal and establishes a **strong shared package/photo-artwork family** relationship;
  - homography sanity remains imperfect (`quad_ok=0` for the four strongest rows, with large projected-area ratios), so the evidence does not prove the same physical box or identical photograph;
  - the mirror's `2.0` label materially narrows the surviving package family but does not independently prove release version, optical-disc contents, pressing/mastering, installer identity or clean-client status.
- 1.x control boundary:
  - public mirror `https://shiqi.ws/post/10248.html` is indexed under `石器时代182时期的端游客户端新手礼包`;
  - follow-up run **36097423535** completed successfully after raw/CSS/escaped-URL discovery was added;
  - the only additional image-like object was `dh_bg.jpg`, a **1×31** plugin background, so no usable 1.x package photograph was recovered from the tested current page surface.
- Confidence:
  - **A for current mirror title, recoverable image hash and computed cross-image metrics**;
  - **B for using the later collector title as a package-generation attribution**;
  - **OPEN for exact original release version and all byte-level relationships**.
- Canonical note: `research/clients/STONEAGE-EARLY-RUTEN-REGIONAL-CARRIERS-R1.md`.
- Derived report: `research/recovered/STONEAGE-MAINLAND-PACKAGE-MIRROR-MATCH-R1.txt`.

### SRC-CN-IA-SA-ARENA-OPTICAL-01

- Public preservation item: Internet Archive identifier `sa-arena`.
- Current catalogue title: `疯狂原始人 Stoneage Arena Online CD-ROM 2002`.
- Retrieval/research date: **2026-09-25**.
- Source type: **publicly preserved full optical BIN/CUE object plus current IA catalogue metadata**.
- Catalogue-boundary warning:
  - current IA `date=2002-05-29` and creator `北京华义联合软件开发有限公司` are uploader/catalog fields;
  - this probe does **not** promote those fields to independently verified contemporaneous publication facts.
- Preserved optical object:
  - `CD [SA_ARENA].bin`: **721,431,312 bytes**, MD5 `f4e7b6ec2b27282d67f6b3982310cc2e`, SHA-1 `f21da5f459db55cc5e09fccadc09f00a7b115177`, CRC32 `bcf893b0`;
  - `CD [SA_ARENA].cue`: **299 bytes**, MD5 `3b6ddb5cf3de1760273d5bd75cc6d7e4`, SHA-1 `5928bffc95d34be28fcce802cced0b2769f625b4`, CRC32 `2d33121f`;
  - one `MODE1/2352` track;
  - ISO9660 volume label **`SA_ARENA`**;
  - root includes `AUTORUN.INF`, `README.TXT`, `SAARENA.EXE`, `SA_ARENA.ICO`, and `DIRECTX8/`.
- Byte-derived product classification:
  - `README.TXT` is **22,009 bytes**, SHA-256 `b4a7145830418692f73030e8b6f6561458bbe272252f23178ec538e107cdd3ab`, decoded as GB18030;
  - it repeatedly identifies the product as **`疯狂原始人`**, including product registration and default installation directory `C:\Program Files\Waei\疯狂原始人\`;
  - it gives WGS/Beijing-Waei URLs and contact identity;
  - critically, it says WGS points may be used for **`《石器时代》、《大法师》、《疯狂原始人》`**, treating StoneAge and 疯狂原始人 as distinct products.
- Classification: **SAME-OPERATOR / SAME-WGS-ECOSYSTEM NEGATIVE CONTROL — NOT A STONEAGE 2.5 CLIENT CANDIDATE**.
- Cross-source consistency:
  - the independent SMZDM survivor list also separately names `2.5 / 3.0 / 4.0 / 5.0 / 疯狂原始人`, consistent with the byte-derived product distinction.
- Operational consequence:
  - remove `sa-arena` from the StoneAge 2.5 recovery candidate queue;
  - retain it only as a Beijing-Waei/WGS optical-layout and vocabulary control;
  - no deeper read of the **599,802,752-byte** `SAARENA.EXE` is justified for the current 2.5 objective.
- Canonical note: `research/clients/STONEAGE-SA-ARENA-NEGATIVE-CONTROL-R1.md`.
- Derived report: `research/recovered/STONEAGE-SA-ARENA-IA-OPTICAL-R1.txt`.
- GitHub Actions verification: run **36098498332** — success.

### SRC-CN-2003-17173-STA5-LAUNCH-01

- Title: 《石器时代5.0:宠物进化史》全新上市
- Original date: 2003-01-16
- Retrieval date: 2026-09-25
- Language/region: Simplified Chinese / Mainland China
- Source type: contemporaneous 17173 game-news / distribution announcement
- URL: https://news.17173.com/content/2003-1-16/n470_387077.html
- Confidence: A for the dated public-distribution claim; it does not identify the hash of the surviving IA disc
- Supports:
  - 石器时代ONLINE宠物进化史 was publicly described as newly on sale by 2003-01-16;
  - the advertised starter pack explicitly included a 完整版客户端;
  - the pet-fusion/egg description matches the product identity exposed by the recovered 5.0 installer and README.
- Does not support:
  - byte identity between the advertised pack and IA item Stoneage-5;
  - a mastering/pressing date for that preserved BIN;
  - DAT/MAP field-cache contents.
- Cross-check: contemporaneous Sina source SRC-CN-2003-SINA-SA-DOWNLOAD-HUB-01 exposes 5.0 client downloads on 2003-04-03.

### SRC-CN-2003-WAEI-STA5-IA-OPTICAL-01

- Title: preserved Stoneage-5 / 石器时代Online 宠物进化史 CD-ROM
- Retrieval date: 2026-09-25
- Language/region: Simplified Chinese / Mainland China
- Source type: preserved optical-image object plus bounded ISO9660/MSI/CAB byte inspection
- Internet Archive identifier: Stoneage-5
- Confidence: A for byte-derived identity and internal structure; B for original pressing/mastering provenance because no independent Redump/ring-code identity is linked yet
- Preserved carrier:
  - CD [STA5].bin: 733,057,248 bytes; MD5 61a8b9f2e7db18c3e3e95c6c12e3674b; SHA1 6053dce3df2723250ddb52a98b3e8cf2552cd791; CRC32 98d6ee68;
  - CD [STA5].cue: 295 bytes; MD5 8cd5e5427248427175392d9632b37bc3; SHA1 4b667f113add8d1ad20dc4ae0eff10a8b97a1203;
  - ISO9660 volume label STA5.
- Installer:
  - STA5.MSI: 782,908 bytes; SHA-256 0ed62503861d4fc3f715c060402d101150020d54e5d294af40a8412232ba4f63;
  - ProductName=石器时代宠物进化史; ProductVersion=5.00.0000; Manufacturer=北京华义联合软件开发有限公司;
  - install root Program Files\Waei\stoneage5.0; 413 MSI File rows.
- Cabinet:
  - DATA1.CAB: 612,584,670 bytes; CAB v1.3; 26 LZX folders / 413 cabinet files;
  - only bounded prefixes and selected early files were read; no full cabinet or proprietary payload was committed.
- Exact battle lineage:
  - 5.0 battle_2.bin: 187,500 bytes; SHA-256 1046a66cbf34088a15f99146263f166be68991c9e01b48dcbbc81d82d1569642;
  - first 185,892 bytes exactly equal Taiwan v1.0 battle_1.bin SHA-256 d99be6475982cf6098b90ff5dfd81ab275ec8c9271fa83daceb95e3fd4bb8859;
  - 1,608-byte tail is exactly two 804-byte records;
  - 5.0 battletxt_2.txt: 5,844 bytes; SHA-256 4f0f1c2f703a2fba95e9966cd7a760ebe168591d89057ddeb2b645ac08942057;
  - first 5,792 bytes exactly equal v1.0 battletxt_1.txt; appended rows are battle218.sab and battle219.sab.
- Internal time evidence:
  - battle_2.bin / battletxt_2.txt: 2001-06-25;
  - real_31.bin / adrn_31.bin: 2002-12-25;
  - sa_5000.exe: 2002-12-26;
  - INSTALL.EXE PE timestamp: 2002-12-27 02:21:08 UTC.
- Boundary:
  - internal timestamps are not independent release-date proof;
  - IA catalogue date/creator remain uploader metadata unless independently corroborated;
  - exact surviving BIN is not independently tied to a pressing/ring-code record;
  - MSI contains no client field-cache .DAT / single-layer .MAP rows, so field-map byte provenance remains open.
- Derived reports:
  - research/recovered/STONEAGE-STONEAGE5-IA-METADATA-R1.txt
  - research/recovered/STONEAGE-STONEAGE5-IA-OPTICAL-R1.txt
  - research/recovered/STONEAGE-STONEAGE5-MSI-INVENTORY-R1.txt
  - research/recovered/STONEAGE-STONEAGE5-CAB-DIRECTORY-R1.txt
  - research/recovered/STONEAGE-STONEAGE5-BATTLE-LINEAGE-R1.txt

#### 2026-09-25 refinement — SRC-CN-2003-WUXITIANLONG-MAP-PACK-ARCHIVE-01

- Preserved HTTP metadata from the exact replay now adds:
  - original content length: **4,223,728 bytes**;
  - origin `Last-Modified: Tue, 10 Jun 2003 10:01:06 GMT`;
  - Wayback memento observation: **2003-06-23 23:44:51 UTC**.
- Full transient extraction identifies the object as a PE32/UPX/RAR SFX containing one `map/` directory and **1,011 DAT files**:
  - 1,008 numeric DATs;
  - BGM0.DAT, BGM1.DAT, BGM2.DAT;
  - 995 strict three-plane-valid normal DATs;
  - 16 special/invalid normal-parser entries.
- Whole-file comparison against the recovered mixed-2.5 map directory:
  - same-name files: **1,011 / 1,011**;
  - one-sided files: **0 / 0**;
  - exact SHA-256 matches: **995**;
  - different whole files: **16**;
  - numeric-only accounting remains **993 exact / 15 different**.
- Layer-level comparison of the 15 differing normal DATs:
  - tile changed cells: **11,500**;
  - parts changed cells: **678**;
  - event changed cells: **4,593**;
  - event low-12 payload changes: **5**;
  - event high read/see-flag changes: **4,588**.
- Independent anomaly controls:
  - `1021.DAT` is exact across both corpora, SHA-256 `92abd0a38c5e876d985c33437a252358d1aaa812ce1da99f18752d0a97c81197`;
  - `817.dat` is exact, SHA-256 `ca29cdf04f9f750712ef9afffe14aebfd571a0c6011eac2c7eff67dfde8cc380`.
- Interpretation boundary:
  - the archived origin Last-Modified materially dates this particular surviving object to June 10, but does not prove identical bytes were served on the earlier 5.0 page;
  - exact `1021` / `817` equality rules out later mutation inside the recovered mixed bundle as their primary anomaly source, but does not establish first historical appearance.
- Additional derived reports:
  - `research/recovered/STONEAGE-HISTORICAL-MAPEXE-WAYBACK-R1.txt`;
  - `research/recovered/STONEAGE-HISTORICAL-MAPEXE-INVENTORY-R1.txt`;
  - `research/recovered/STONEAGE-HISTORICAL-MAPEXE-SA25-LINEAGE-R1.txt`;
  - `research/recovered/STONEAGE-HISTORICAL-MAPEXE-SA25-LAYER-DIFF-R1.txt`.

### SRC-CN-2001-SINA-FULLMAP-01

- Title: `《石器时代》全地图`
- Original date: **2001-11-27**
- Retrieval date: 2026-09-25
- Language/region: Simplified Chinese / Mainland China
- Source type: contemporaneous Sina game-download record with surviving local-download href
- Source page: `https://games.sina.com.cn/downgames/map/11271899.shtml`
- Confidence: **A** for the dated record, displayed size, contributor and compatibility statement; payload identity remains unrecovered
- Surviving record facts:
  - stated size: **1911K**;
  - contributor: `xinhaonanhai`;
  - deployment instruction: unpack into the StoneAge directory;
  - compatibility statement: **“1.X，2.0通用”**.
- Exact local-download token recovered from the source:
  - `col=map`;
  - `aid=43172`;
  - `filename=Estoneage2.0map_1127.exe`;
  - `size=1911`.
- Preservation status:
  - exact/predicted Wayback URL probes: no payload capture found on tested surfaces;
  - Internet Archive exact/stem item search: no exact item;
  - DiscMaster exact/stem search: no exact carrier;
  - contributor-domain Wayback root captures exist at 2001-12-03 and 2002-07-19, but no relevant package href is exposed by the current indexed/replayed surface.
  - The Sina host-alias census exposes **56 archived `col=map` rows** on `games.sina.com.cn` in 2001 but no exact `aid=43172` / `Estoneage2.0map_1127.exe` row. Replayed early-2001 neighbors consistently expose `http://202.106.184.193/downfiles/map_1212/`, but the target filename substituted into that directory has zero CDX rows. This is an early map-server topology control, not a proven November 2001 target path.
  - A bounded scan of **73 live map-page IDs** around `11271899.shtml` recovered the target plus four immediately preceding map records (`aid=43124/43127/43129/43130`). All four are Delta Force packages with `_1119.zip` filenames. A dedicated Wayback prefix/replay pass across both `games1.sina.com.cn` and `games.sina.com.cn` finds **zero archived CGI rows for all four sibling tokens**, so this same-page batch does not currently reveal a late-November-2001 binary directory.
  - Same-contributor/two-generation carrier census R2: Internet Archive alias/title/description searches for `xinhaonanhai` and exact 2001/2002 map-package stems returned **0 directed rows**; a broad Chinese community-map query returned 25 unrelated modern software-metadata rows, all filtered as irrelevant; DiscMaster returned **0 rows** for the alias, both exact filenames, both stems, and `shiqi4updatex`; strict filename rows **0**, errors **0**. This bounds the currently tested IA/DiscMaster contributor-lineage carrier surface; reopen only from a new carrier/path token.
- Supports:
  - existence of a specifically named full-map distribution package in late 2001;
  - a contemporaneous claim that the package was usable by both 1.X and 2.0 client families;
  - an exact high-value recovery token for pre-2002 field-map archaeology.
- Does not support:
  - operator originality or clean-byte status of the package;
  - byte identity with Taiwan v1.0 maps;
  - any map ID/hash/content until the executable itself is recovered.
- Derived reports:
  - `research/recovered/STONEAGE-2001-FULLMAP-PRESERVATION-R1.txt`;
  - `research/recovered/STONEAGE-XINHAONANHAI-ARCHIVE-R1.txt`;
  - `research/recovered/STONEAGE-2001-SINA-HOST-ALIAS-R1.txt`;
  - `research/recovered/STONEAGE-2001-SINA-MAP-TOPOLOGY-R1.txt`;
  - `research/recovered/STONEAGE-2001-SINA-SAMEBATCH-R1.txt`;
  - `research/recovered/STONEAGE-2001-SINA-SAMEBATCH-ROUTE-R1.txt`.

### SRC-CN-2001-SINA-SA20-CLIENT-01

- Title: `石器时代2.0客户端`
- Original date: **2001-11-02**
- Retrieval date: 2026-09-25
- Language/region: Simplified Chinese / Mainland China
- Source type: contemporaneous Sina game-client download record
- Source page: `https://games.sina.com.cn/downgames/demo/1102970.shtml`
- Confidence: **A** for the dated Sina label/record and exact download token; build bytes remain unrecovered
- Surviving record facts:
  - stated size: **524377K**;
  - description identifies it as an upgraded StoneAge client for existing StoneAge users.
- Exact local-download token:
  - `col=demo`;
  - `aid=41967`;
  - `filename=stoneage2.0setup.exe`;
  - `size=524377`.
- Preservation status:
  - current exact Wayback, Internet Archive and DiscMaster probes expose no verified payload body.
  - A dual-host `col=demo` topology probe recovers one archived neighboring executable route, `http://202.108.44.24/demo_1118/monkeybrain.exe` (aid=25443). Substituting `stoneage2.0setup.exe` into that directory has zero CDX rows; the route is only a Sina demo-server control, not target-path proof.
- Supports:
  - an exact historical client filename and download-record identity for the Mainland 2.0 era.
- Does not support:
  - a clean-client classification until recovered bytes are inspected;
  - byte identity with Taiwan/JSS/Korean branches;
  - treating the displayed version label as executable build provenance without binary inspection.
- Derived reports:
  - `research/recovered/STONEAGE-2001-CLIENT-PRESERVATION-R1.txt`;
  - `research/recovered/STONEAGE-2001-SINA-CLIENT-TOPOLOGY-R1.txt`.

### SRC-CN-2000-SINA-FULLMAP-01

- Title: `石器时代！全地图` (decoded from the surviving Sina download-link title parameter)
- Record date: **2000-12-20**
- Retrieval date: 2026-09-25
- Language/region: Simplified Chinese / Mainland China
- Source type: surviving contemporaneous Sina game-download record with exact local-download href
- Source page: `https://games.sina.com.cn/downgames/map/1220492.shtml`
- Confidence: **A** for the surviving page, exact download token, filename and stated size; payload identity remains unrecovered
- Exact local-download token recovered from the source:
  - `col=map`;
  - `aid=23223`;
  - `filename=samap_1220.zip`;
  - `size=1410`;
  - title parameter decodes to `石器时代！全地图`;
  - author parameter decodes to `游民部落`.
- Attribution boundary:
  - contemporaneous Sina pages use `游民部落` as a Sina game-community/editorial label, so this value alone does **not** identify a separate uploader domain or the later user/site `xinhaonanhai`;
  - the 2001-11 package is materially different: its author field explicitly says `游民部落网友` and embeds `http://www.xinhaonanhai.com` around the name `xinhaonanhai`;
  - therefore any 2000→xinhaonanhai lineage remains only a tested weak hypothesis and must not be used as provenance without an independent path/token match.
- Package-content clue from the surviving page:
  - the instructions say to **unzip the package and copy its contents into the StoneAge installation's `map` subdirectory**;
  - the stated effect is that in-game maps become fully visible without manual exploration;
  - this strongly classifies the distribution as a field-map/cache-content package rather than a full client installer, while still not proving the exact file list until bytes are recovered.
- Same-pipeline control discovered:
  - Sina's 2000-12-28 `石器时代—北岛详细地图指南` uses the same local-download backend with `aid=23680`, `filename=northisland_1228.zip`, `size=134`;
  - Sina's 2000-12-28 `石器时代—南岛详细地图指南` likewise uses `aid=23681`, `filename=southisland_1228.zip`, `size=202`;
  - these immediately adjacent StoneAge packages are topology controls for reconstructing the late-2000 Sina redirect/file-server path even if `aid=23223` itself has no archived CGI response; public exact-filename web searches exposed no direct mirror for either control package on the tested search surface.
- Direct historical delivery route recovered from the archived Sina CGI response:
  - archived CGI timestamp: **2001-01-26 07:46:00 UTC**;
  - exact route: `http://202.106.184.193/downfiles/map_1212/samap_1220.zip`;
  - the archived HTML labels the link `石器时代—全地图下载` and repeats the displayed **1410K** size;
  - this is first-party routing evidence from Sina's own archived download CGI, not a synthesized filename/path guess;
  - route proof does **not** establish that a recoverable ZIP snapshot exists or that later bytes at the same URL are identical.
- Preservation status:
  - exact/predicted Wayback payload-path probes: no verified payload capture on the tested surfaces;
  - exact Internet Archive filename/stem searches: no exact carrier;
  - DiscMaster broad `samap` searches return many unrelated files; these are diagnostic noise and are **not** preservation candidates unless the leaf filename exactly matches `samap_1220.zip`;
  - the Sina source page itself has historical Wayback availability, and the `aid=23223` CGI body **has now been recovered** from the `games.sina.com.cn` host alias at timestamp `20010126074600`; that replay is the source of the exact direct IP route above;
  - the archived 2005-11-03 HTTP 302 for the `southisland_1228.zip` control has now been replayed with redirects disabled. Its `Location` points only to `login.games.sina.com.cn/index.php?reurl=...`, wrapping the original download CGI rather than exposing a file-server URL. This is a login-gateway control, not a payload carrier or direct-file topology proof.
  - a bounded Wayback prefix census of the same Sina `download.pl` backend across 2000–2003 recovered 2,652 rows total: **906 in 2002 and 1,746 in 2003**, but no 2000/2001 prefix rows on the tested index. Of those 2,652 rows, only **3** are `col=map`, all in 2003; bounded replay exposes no direct binary URL. This closes broad CGI-corpus mining as a useful route unless a new exact historical token/archive surface appears.
  - The exact direct ZIP URL has **zero Wayback availability** across the tested 2000-12-20 through 2005-11-03 dates and zero exact/prefix CDX rows. Its parent `map_1212` directory is archived with 76 rows, but `samap_1220.zip` is absent and `southisland_1228.zip` survives only as a later 404.
  - A host-wide `202.106.184.193/downfiles/` filename census found no `samap_1220` alias. Related `stoneage`/`1220` rows are sibling topology controls only and are preserved as later 404s.
  - Common Crawl exposes zero target rows on the tested exact filename/direct-URL indexes. Arquivo.pt text searches expose zero rows where reachable; its exact version/CDX endpoints encountered transient network-unreachable errors, so this is recorded as **no current independent-archive hit**, not a proof that every Arquivo surface is permanently empty.
- Supports:
  - existence of a specifically named Mainland StoneAge full-map distribution package by late 2000;
  - an exact recovery token that predates the 2001-11 `Estoneage2.0map_1127.exe` target;
  - a higher-priority route for moving the field-map byte-provenance anchor earlier.
- Does not support:
  - operator originality or clean-byte status of the ZIP;
  - byte identity with Taiwan v1.0 or later map corpora;
  - any map ID/hash/content claim until the ZIP bytes are recovered and extracted.
- Derived reports:
  - `research/recovered/STONEAGE-2000-FULLMAP-PRESERVATION-R1.txt`;
  - `research/recovered/STONEAGE-2000-SINA-AID-23223-R1.txt`;
  - `research/recovered/STONEAGE-2000-SINA-ARCHIVED302-R1.txt`;
  - `research/recovered/STONEAGE-2000-SINA-DIRECT-ROUTE-R1.txt`;
  - `research/recovered/STONEAGE-2000-SINA-DIRECT-RECOVERY-R1.txt`;
  - `research/recovered/STONEAGE-2000-SINA-HOSTWIDE-R1.txt`;
  - `research/recovered/STONEAGE-SINA-DOWNLOAD-CGI-TOPOLOGY-R1.txt`;
  - `research/recovered/STONEAGE-2000-INDEPENDENT-ARCHIVES-R1.txt`.

### SRC-CN-2001-17173-SA20-DISTRIBUTION-01

- Title: `石器时代2.0-家族开拓史 / 升级方法`
- URL: `https://news.17173.com/z/stoneage/banben/sa20-up.htm`
- Retrieval date: 2026-09-25
- Language/region: Simplified Chinese / Mainland China
- Source type: preserved 17173 StoneAge version/upgrade guide
- Dating boundary: the surviving page does not expose an independent publication timestamp in the current HTML, but its operational text is explicitly anchored to the Mainland 2.0 transition beginning **2001-11-01**, the **2001-11-01 to 2001-12-01** compatibility window, and a trial-serial deadline of **2001-12-31**. Treat it as strong period distribution evidence while keeping the exact page-publication timestamp unresolved.
- Distribution statement:
  - Beijing Waei's website offered the `石器时代2.0` **完整升级版** for download;
  - the guide separately states that the same complete upgrade could be obtained free with the following magazines/books/discs:
    1. `PC任我行` 11月号;
    2. `大众软件CD` 11月号;
    3. `电脑` 11月号;
    4. `电脑爱好者光盘――玩游戏` 11月号;
    5. `电脑报――游戏世界` 11月号;
    6. `电脑校园` 11月号;
    7. `晶合秘藏Ⅱ之红宝石`;
    8. `少年电世界` 11月号（光盘版）;
    9. `网上俱乐部――游戏吧` 11月号;
    10. `新游戏人` 11月号;
    11. `游戏原动力` 11月号;
    12. 圣比尔 `石器时代2.0攻略`;
    13. 腾图 `石器时代攻略全集`.
- Recovery consequence:
  - these are concrete **carrier identities** for the Mainland 2.0 complete-upgrade client and are independent of the missing Sina `stoneage2.0setup.exe` payload route;
  - a preserved coverdisc/book-disc may contain the client under a different path or filename, so carrier-level filesystem inspection has higher value than exact-filename-only searching once candidates are identified.
- Preservation census — 2026-09-25:
  - an initial unfielded IA metadata census produced **86 rows**, but manual/refined classification shows those rows were dominated by unrelated description/full-text noise; DiscMaster returned **zero rows** for all 13 carrier search phrases;
  - a refined IA pass restricted to title-field + software-media searches. None of the 13 listed **2001-11** carrier identities was recovered directly, and global `石器时代2.0` / `StoneAge 2.0` software-metadata searches returned zero;
  - `大众软件CD` did expose an authentic preservation namespace of **18 older Popsoft CD items**, all from 1997–1998, with predictable identifiers such as `popsoftcd-1997-12` and `popsoftcd-1998-11`. This creates a concrete preservation-family lead; the namespace is now being enumerated directly for possible 1999–2001 continuation rather than treating older discs as target carriers.
- Derived reports:
  - `research/recovered/STONEAGE-2001-SA20-COVERDISC-CENSUS-R1.txt` (broad/noisy discovery pass);
  - `research/recovered/STONEAGE-2001-SA20-COVERDISC-CENSUS-R2.txt` (title/software refinement).
- Does not support:
  - that every listed carrier contains byte-identical media;
  - that the file on any listed disc is named `stoneage2.0setup.exe`;
  - that any later re-upload is clean without file-level provenance checks.



### SRC-CN-2002-SINA-XINHAONANHAI-COMMUNITY-01

- Title: Sina StoneAge community pages identifying `xinhaonanhai` as an active community member/moderator
- Content time anchors: **2002-09 through 2002-11** (page content dates/events)
- Retrieval date: 2026-09-25
- Language/region: Simplified Chinese / Mainland China
- Source type: contemporaneous Sina Games StoneAge forum/award pages
- URLs:
  - `https://games.sina.com.cn/zhuanqu/stoneage3/zhongjiang0816.shtml`
  - `https://games.sina.com.cn/zhuanqu/stoneage3/mingdan10.shtml`
  - `https://games.sina.com.cn/zhuanqu/stoneage3/mingdan11.shtml`
- Confidence: **A** for the alias occurring on Sina's StoneAge community surface and being explicitly called `斑竹xinhaonanhai` in the November event text; **not identity evidence** beyond the screen name.
- Supports:
  - `xinhaonanhai` was not merely an isolated download-record string; the alias was active on Sina's StoneAge community surface during 2002;
  - November 2002 event text explicitly tells winners to contact `斑竹xinhaonanhai`, establishing a moderator role for that alias on the Sina StoneAge forum surface by then;
  - together with `SRC-CN-2002-SINA-SA40-FULL-MAP-PATCH-01`, the same alias is independently tied to a later StoneAge full-map package of the same functional class as the 2001 target.
- Does not support:
  - civil/legal identity of the person behind the alias;
  - that the 2001 and 2002 packages are byte descendants of one another;
  - operator originality of either community-contributed map package;
  - any map bytes, hashes or file ancestry until payloads are recovered.
- Canonical interpretation note:
  - `research/clients/STONEAGE-2001-XINHAONANHAI-CONTRIBUTOR-LINEAGE-R1.md`


### SRC-CN-2001-POPSOFT-SA20-CARRIER-LIST-01

- Title: `大众软件 2001 年 11 月 B / 2001 第 22 期` — StoneAge 2.0 upgrade-distribution notice
- Original period: **November 2001**
- Retrieval date: 2026-09-25
- Language/region: Simplified Chinese / Mainland China
- Source type: contemporaneous magazine scan preserved as searchable full text
- Preserved source:
  - Internet Archive item family: `popsoft-magazine_202403`
  - issue text path: `2001/大众软件-2001年11月B_djvu.txt`
  - URL: `https://archive.org/stream/popsoft-magazine_202403/2001/%E5%A4%A7%E4%BC%97%E8%BD%AF%E4%BB%B6-2001%E5%B9%B411%E6%9C%88B_djvu.txt`
- Confidence: **A** for the carrier-list text as preserved in the contemporaneous magazine; optical-disc contents remain unrecovered.
- Supports:
  - existing StoneAge 1.X users could obtain a StoneAge 2.0 `完整升级版` through a list of magazines/media;
  - the preserved list includes the previously known November carrier set but additionally names **`《CHIP 新电脑》11月号`**;
  - this creates a new exact carrier identity for the 2001-11-02 client-recovery route;
  - the issue separately corrects an earlier advertisement concerning `《晶合秘藏Ⅱ之红宝石》`, distinguishing an upgrade version from a formally activated retail version, which reinforces the need to separate client bytes from activation entitlement.
- Source-difference note:
  - the currently preserved 17173 upgrade guide lists the same distribution context but omits `《CHIP 新电脑》11月号`;
  - preserve this difference rather than flattening the two lists into one assumed master list.
- Does not support:
  - that a public image of the CHIP November-2001 coverdisc currently survives;
  - that its StoneAge package used the Sina filename `stoneage2.0setup.exe`;
  - byte identity between any magazine-disc package and Sina's labelled client;
  - client cleanliness/provenance until an actual disc filesystem/package is inspected.
- Canonical note:
  - `research/clients/STONEAGE-SA20-CHIP-NEWCOMPUTER-CARRIER-R1.md`
- Preservation follow-up:
  - targeted R2 Internet Archive + DiscMaster carrier probe returned **0 relevant Chinese November-2001 CHIP items**, **0 relevant DiscMaster rows**, and **0 errors**;
  - foreign-language CHIP 2001-11 coverdiscs were explicitly excluded;
  - DiscMaster item `31124` / `新电脑0508.iso` is a **2005 August** Chinese CHIP disc and is a negative date control, not the target.
- Derived report:
  - `research/recovered/STONEAGE-2001-CHIP-NEWCOMPUTER-CARRIER-R2.txt`


### SRC-CN-2001-17173-SA20-PRODUCT-01

- Title: `石器时代2.0-家族开拓史 / 产品介绍`
- Product date stated by page: **2001-11-01**
- Retrieval/research date: 2026-09-25
- Language/region: Simplified Chinese / Mainland China
- Source type: surviving 17173 StoneAge version/product page preserving period product specifications
- URL: `https://news.17173.com/z/stoneage/banben/sa20-cq.htm`
- Confidence: **A** for the preserved product-page statements; this source does not itself provide disc bytes or mastering provenance.
- Supports:
  - `石器时代2.0新手报到包` is stated to contain a **《石器时代2.0》客户端光盘** plus a 300-point WGS serial;
  - `石器时代2.0老手削暴包` is independently stated to contain a **《石器时代2.0》客户端光盘** plus the listed WGS/red-T-rex physical extras;
  - both product entries state **2001-11-01** as launch date on this preserved product surface;
  - therefore the new-user and old-user packages are two exact physical-carrier classes for recovery of a period 2.0 client disc.
- Does not support:
  - that both packages necessarily contain byte-identical pressings;
  - that either optical disc is byte-identical to Sina's `stoneage2.0setup.exe`;
  - exact volume label, matrix/IFPI, installer name, filesystem or clean-client hash.
- Related physical-survival control:
  - the 2016 SMZDM collector source maps its first install-disc photo directly to a `2.0新手报到包`; see `SRC-CN-2016-SMZDM-SA25-INSTALL-DISCS-01`.
- Public-preservation follow-up — 2026-09-25:
  - exact/short product names, the literal client-disc wording and Sina setup filename/stem were probed against Internet Archive metadata and DiscMaster filename indexes;
  - the raw R1 census contains **312 unique IA metadata items**, **0 strict IA candidates**, **0 DiscMaster rows** and **0 strict DiscMaster candidates**; one overly broad `老手削暴包` IA query exceeded the bounded JSON body and is not treated as a completed negative query;
  - a fielded R2 residual pass then tested `老手削暴包`, the full `石器时代2.0老手削暴包` name and `stoneage2.0setup` across title/description/identifier software fields: **0 unique items, 0 strict items, 0 errors**;
  - therefore the currently tested **IA/DiscMaster exact retail-package / setup-name surface is bounded with no preserved client-disc candidate**. This does not prove the discs no longer survive elsewhere.
- Derived reports:
  - `research/recovered/STONEAGE-SA20-RETAIL-CARRIER-CENSUS-R1.txt` (large raw diagnostic);
  - `research/recovered/STONEAGE-SA20-RETAIL-CARRIER-CENSUS-SUMMARY-R1.txt`;
  - `research/recovered/STONEAGE-SA20-RETAIL-CARRIER-RESIDUAL-R2.txt`.


### SRC-CN-2003-WAEI-SECONDARY-GUIDE-CLIENT-CD-WARNING-01

- Title: `《石器时代5.0》假攻略悄然上市` / `石器假攻略悄然上市 众玩家擦亮双眼`
- Original date: **2003-01-28**
- Retrieval date: **2026-09-27**
- Language/region: Simplified Chinese / Mainland China
- Source type: contemporaneous 17173 news item relaying an explicit Beijing-Waei warning
- URLs:
  - https://news.17173.com/content/2003-1-28/n408_324318.html
  - https://news.17173.com/content/2003-1-28/n970_886620.html
- Confidence: **A- for the reported Beijing-Waei warning and literal carrier distinction; not evidence about the separate Wanfang 2.5 disc**
- Supports:
  - a Guangdong publisher was selling a product titled `石器时代5.0官方攻略宝典` bundled with a `石器时代ONLINE宠物进化史` client CD and a card;
  - Beijing Waei stated it had **not authorized** the publisher's StoneAge publication/products;
  - Waei stated the bundled client disc was a **network-download version**, **not an official Waei product disc**.
- Archaeology significance:
  - **payload identity and physical-carrier provenance are separate dimensions**;
  - a secondary guide/book carrier can contain a technically usable client while still failing official physical-media provenance;
  - therefore the presence of a StoneAge client on a disc cannot by itself promote that disc to official Beijing-Waei retail/client-media status.
- Does not support:
  - that the Wanfang StoneAge 2.5 disc was unauthorized;
  - that the Wanfang disc used network-downloaded bytes;
  - byte identity between any secondary-carrier disc and an official Waei client.

### SRC-CN-2005-GAPP-WANFANG-GAME-PUBLICATION-01

- Title/context: 新闻出版总署 2005 illegal/unapproved electronic-game-publication inspection list, reproduced by Sina
- Original date: **2005-01-26**
- Retrieval date: **2026-09-27**
- Source type: government-origin enforcement list reproduced by a contemporary major portal
- URL: https://news.sina.com.cn/c/2005-01-26/15295676769.shtml
- Confidence: **A for the literal listed publisher/title/ISBN fields; not a legitimacy endorsement**
- Relevant row:
  - title: `战神3000`
  - publisher field: **万方数据电子出版社**
  - ISBN: **`7-900096-34-5`**
  - code: `N402`
  - foreign rights field: `INFOGRAMES`
  - domestic-agent field: `北京爱可互动数码科技发展有限公司`
- Supports:
  - 万方数据电子出版社 demonstrably used the **`7-900096-*`** ISBN publisher range on a game/electronic publication;
  - the Wanfang StoneAge 2.5 disc's `7-900096-07-8` number therefore belongs to a publisher-number family that was used for game-related electronic products.
- Critical boundary:
  - the source is an enforcement list for unapproved imported games, so it does **not** authenticate or legitimize the StoneAge item;
  - `7-900096-34-5` does not identify or date `7-900096-07-8`;
  - shared publisher prefix does not establish shared content, carrier class, mastering, or distribution channel.



### SRC-CN-2001-SINA-STONEAGE-MAINLAND-LAUNCH-01

- Title: `《石器时代》火爆上市`
- Source date/context: January 2001 Mainland launch coverage
- Retrieval date: **2026-09-27**
- Language/region: Simplified Chinese / Mainland China
- Source type: contemporaneous Sina Games launch report
- URL: https://games.sina.com.cn/newgames/0101/01113641.shtml
- Confidence: **A- for the contemporaneous launch/distribution statements; not physical-disc byte evidence**
- Supports:
  - Mainland Simplified-Chinese `Stone Age` launched in Beijing on **2001-01-10**;
  - the article identifies the role chain as **Japan JSS production -> Beijing Waei authorization -> Soft-World/Zhiguan Electronics (Beijing) agency -> Guangxi Jinhaiwan Electronic Audio-Visual Publishing House publication/distribution**;
  - the Mainland launch used **four different package designs/variants**;
  - the launch package included 45 hours of free play time.
- Archaeology significance:
  - identifies **广西金海湾电子音像出版社** as a contemporaneous official Mainland publication/distribution identity for the earliest launch period;
  - the four-package statement means package artwork alone cannot be assumed to identify a unique optical pressing.
- Does not support:
  - exact ISBN/ISRC/catalogue number;
  - optical-disc label, volume ID, file tree or hashes;
  - byte identity with Taiwan v1.0, JSS 1999 retail, or any later Mainland client.

### SRC-CN-2002-PKU-STONEAGE-MAINLAND-DISTRIBUTION-01

- Title: `“石器时代”的规则`, 《经济学（季刊）》Vol.1 No.3 (2002)
- Retrieval date: **2026-09-27**
- Source type: academic paper based on contemporaneous Mainland StoneAge observation
- Public PDF: https://www.nsd.pku.edu.cn/attachments/5dd8a996f6b542d1a6c23e18602423e9.pdf
- Confidence: **B+/A- for independent near-contemporaneous corroboration of the distribution roles/date**
- Supports:
  - JSS development;
  - Beijing Zhiguan agency and Waei authorization;
  - **广西金海湾音像出版社正式发行 on 2001-01-10**;
  - Zhiguan technical support and Waei sales/service roles.
- Archaeology significance:
  - independently corroborates the Sina launch chain and date from a different source class.
- Does not support:
  - package contents, ISBN, disc identity, installer bytes, or exact optical pressing.



### SRC-CN-2016-SHIQIME-MAINLAND-CLIENT-DISCS-01

- Title: `我也跟风发一下石器时代留下的回忆`
- Publication date: **2016-05-04**
- Retrieval date: **2026-09-27**
- Source type: later first-person player preservation post with direct photographs of retained physical media
- Page: https://www.shiqi.me/pt_51.htm
- Direct image URLs:
  - early/1.82-labelled client disc: https://www.shiqi.me/zb_users/upload/2016/05/201605041462372233975831.jpg
  - StoneAge 2.0 `家族开拓史` client disc: https://www.shiqi.me/zb_users/upload/2016/05/201605041462372263129465.jpg
  - StoneAge 2.5 `精灵王传说` client disc: https://www.shiqi.me/zb_users/upload/2016/05/201605041462372351521932.jpg
- Confidence:
  - **B for literal visible disc-face fields/logos and direct photograph survival**;
  - **C+/B- for the author's retrospective version/package classification**;
  - **not byte provenance**.
- Supports:
  - the author explicitly labels the first photographed disc as a `石器时代1.82的客户端`;
  - the first disc photograph visibly carries StoneAge branding, **北京华义联合软件开发有限公司**, and **广西金海湾电子音像出版社** text, plus operator/service logos and a physical serial-label sticker;
  - the author explicitly labels the second disc as a StoneAge 2.0 client and states it came from a purchased **老手削暴包**;
  - the second disc face visibly reads **`石器时代2.0 家族开拓史`**;
  - the third disc face visibly reads **`石器时代2.5 精灵王传说`** and carries Waei/operator branding.
- Critical limits:
  - the first disc's exact ISBN/ISRC/catalogue-number small print is **not transcribed** here because the current public image resolution is insufficient for error-free reading;
  - the post does not establish when or where each disc was manufactured, nor byte identity with a January-2001 first pressing;
  - later first-person recollection can mislabel version/package context and therefore must be cross-checked against contemporaneous product records.
- Archaeology significance:
  - independently confirms surviving photographed **Mainland Waei/Jinhaiwan client-disc material** for the early 1.x/1.82 line;
  - provides a direct photographed 2.0 client-disc control consistent with the contemporaneous 17173 statement that `老手削暴包` contained a 2.0 client disc;
  - provides a direct 2.5 client-disc visual control whose printed artwork/operator branding is plainly different from the separately photographed Wanfang `7-900096-07-8/Z.03` disc.
- Does not support:
  - optical volume label, filesystem contents, hashes, matrix/IFPI, installer identity or clean-byte provenance;
  - treating the Wanfang 2.5 disc as byte-different solely because its printed artwork differs.

### SRC-CN-2016-SHIQIME-WANFANG-SA25-DISC-01

- Title/context: `哈哈，找到了这个：石器时代2.5精灵王的传说光碟和点卡`
- Publication date: **2016-02-03**
- Retrieval date: **2026-09-27**
- Page: https://www.shiqi.me/pt_17.htm
- Direct disc image: https://www.shiqi.me/zb_users/upload/2016/02/201602031454475577106602.jpg
- Confidence: **B for visible disc-face fields; not client-byte provenance**
- Visible fields:
  - `永远的石器时代 2.5 精灵王传说`;
  - **万方数据电子出版社出版**;
  - ISBN **`7-900096-07-8/Z.03`**;
  - barcode **`9787900096074`**.
- Comparative significance:
  - the printed artwork/publisher identity is visibly different from the Waei-branded 2.5 client disc photographed in `SRC-CN-2016-SHIQIME-MAINLAND-CLIENT-DISCS-01`;
  - this establishes **different physical carrier identity/artwork**, not different client bytes.
- Classification remains:
  - **OPEN / secondary-carrier or publisher-bundle candidate** until file-level evidence or independent package documentation resolves its payload and provenance.



### SRC-CN-2020-SOHU-EARLY-MAINLAND-DISC-MIRROR-01

- Title: `发一下留下的石器时代回忆`
- Publication date: **2020-07-07**
- Retrieval date: **2026-09-27**
- Source type: later repost/mirror of the same physical-disc photograph family already preserved by SHIQI.ME; **not an independent physical specimen**
- Page: https://www.sohu.com/a/406234981_120099894
- Direct first-disc image: https://p3.itc.cn/q_70/images03/20200707/0b5a52c6c1ce40fea0c95c7662d3cc5b.jpeg
- Visible/retrospective context:
  - the page labels the first photographed disc as `石器时代1.82的客户端`;
  - the image visibly carries StoneAge, Beijing Waei/WAEI and 广西金海湾电子音像出版社 identity.
- **PROVISIONAL VISUAL TRANSCRIPTION** from the publication-number line:
  - `ISBN 7-900323-57-0/TP·026`.
- Confidence:
  - **B for the plainly visible publisher/operator identity and the `7-900323` prefix**;
  - **C+/PROVISIONAL for the full suffix `57-0/TP·026` until independently reproduced by a bibliographic/catalogue record or a higher-resolution package/disc scan**.
- Integrity checks on the provisional number:
  - `7-900323-57-0` passes the ISBN-10 Mod-11 checksum;
  - the corresponding ISBN-13 candidate `978-7-900323-57-6` passes the ISBN-13 checksum.
- Critical limits:
  - checksum validity only shows that the transcription is structurally plausible; it does not independently prove the photograph's small-print suffix;
  - the Sohu page is a mirror/repost, so it must not be counted as a second independent physical observation;
  - the retrospective `1.82客户端` caption remains a source classification, not byte-level build proof.
- Derived probe:
  - `research/recovered/STONEAGE-EARLY-MAINLAND-PROVISIONAL-ISBN-R1.txt`.

### SRC-CN-MCSC-JINHAIWAN-ISBN-PREFIX-01

- Title/context: `ISBN国际标准图书编号` — appendix of electronic-publication publisher codes
- Retrieval date: **2026-09-27**
- Source: 中国音乐著作权协会
- URL: https://www.mcsc.com.cn/knowledge/classroom_16.html
- Confidence: **A- for the literal publisher-code table**
- Supports:
  - `金海湾电子音像出版社 | ISBN 7-900323`.
- Archaeology significance:
  - independently confirms that the publisher prefix visually present on the early Mainland StoneAge disc is consistent with the historically documented Guangxi-Jinhaiwan publisher;
  - materially strengthens the first seven digits of the disc-number transcription without independently validating the item suffix `57-0/TP·026`.
- Does not support:
  - the exact StoneAge title/item number;
  - release date, edition, package variant, disc byte identity or client build.

### SRC-CN-2020-SHIQISO-SA182-NEWBIE-PACK-01

- Title: `石器时代1.82时期的客户端新手礼包`
- Publication date shown by the site index: **2020-09-16**
- Retrieval date: **2026-09-27**
- Source type: later specialist collector article/index excerpt
- Indexed source surfaces:
  - https://blog.shiqi.so/page2.htm
  - https://blog.shiqi.so/sqcy4_2.htm
- Confidence: **C+/B- for later collector composition evidence; not contemporaneous launch documentation**
- Indexed excerpt supports:
  - the 1.82-era new-user package is described as containing a CDK on the back of the manual plus **one installation disc**;
  - the excerpt then begins `下面这四款是最普...`, indicating a set of four commonly shown package variants on that collector surface.
- Cross-source relation:
  - contemporaneous Sina independently states that the Mainland launch had **four different package designs/variants**;
  - the numerical agreement is useful corroboration but **does not prove that the collector's four pictured/common variants are exactly the same four January-2001 launch packages**.
- Does not support:
  - byte identity of the installation discs across the four packages;
  - exact ISBN/ISRC/catalogue number;
  - treating the later `1.82` label as an independently verified executable build/version.



### SRC-CN-2020-GAMER-SA182-PACKAGE-COLLECTOR-01

- Title: `石器時代周邊收藏，石器用戶端禮包篇（四）1.82石器新手用戶端包`
- Publication date: **2020-09-17**
- Retrieval date: **2026-09-27**
- Source: Bahamut StoneAge forum; later physical-media collector post
- URL: https://forum.gamer.com.tw/C.php?bsn=1571&snA=81396
- Confidence: **C+/B- for literal package-composition and same-collection observations; not contemporaneous launch evidence and not byte provenance**
- Supports:
  - the collector describes the 1.82 new-user package as carrying the CDK on the manual back plus **one installation disc**;
  - four common 1.82 package-front variants are shown/described;
  - the collector states that the **backs of those four common packages are identical**;
  - a separate `上网包` variant is distinguished and described as including an internet-access card.
- Archaeology significance:
  - materially increases the value of finding a readable back from **any** of the four ordinary packages, because it may represent a shared back template;
  - requires the `上网包` to remain a separate physical-carrier branch.
- Critical limits:
  - the post is from 2020 and does not authenticate a January-2001 first pressing;
  - it does not prove that the four pictured/common packages are exactly the four launch designs reported by Sina;
  - identical backs do not prove identical optical discs or byte-identical payloads.

### SRC-CN-2021-GAMER-SA182-DISC-COLLECTOR-01

- Title: `石器時代華義國際石器周邊收藏光碟篇（一）`
- Publication date: **2021-01-07**
- Retrieval date: **2026-09-27**
- Source: Bahamut StoneAge forum; later optical-media collector inventory
- URL: https://forum.gamer.com.tw/C.php?bsn=1571&snA=81430
- Confidence: **C+/B- for the collector's physical-disc family classification; not byte provenance**
- Supports:
  - the collector identifies the familiar Beijing-Waei 1.82 client disc as the standard/unified disc used across ordinary Mainland package variants;
  - the collector separately identifies a less-common Mainland `上网包` disc.
- Archaeology significance:
  - supports treating ordinary 1.82 outer-package variation and common disc artwork as separable layers;
  - gives a concrete reason to search package backs and common disc faces across multiple box-front variants rather than assuming each box requires a unique disc identity.
- Critical limits:
  - same artwork/family classification does not prove byte identity across physical specimens;
  - the post does not establish exact manufacturing date, matrix/IFPI, optical file tree, hashes or first-press identity;
  - this source and `SRC-CN-2020-GAMER-SA182-PACKAGE-COLLECTOR-01` are by the same collector and therefore must **not** be counted as independent corroboration.


### SRC-CN-2001-CHINADOTCOM-SA-TRIAL-GIVEAWAY-MIRROR-01

- Original context/date: 中华网游戏频道, `特别推出《石器时代》的邮购服务`, **2001-01-05** with a follow-up notice preserved for **2001-01-11**.
- Retrieval date: **2026-09-27**
- Surviving mirror: https://www.shiqim.com/shiqi5924.html
- Additional preserved compilation: https://www.shiqi.me/pt_25.htm
- Source type: later mirror/transcription of contemporaneous China.com channel content; original live China.com page not recovered in this pass.
- Confidence: **B- for the literal preserved notice; carrier details remain OPEN**
- Supports:
  - the formal retail release was advertised for 2001-01-12 at RMB 29 on this channel;
  - registered users who had participated in an earlier **`《石器时代》试玩版赠送活动`** were offered the formal version for RMB 26 / approximately 10% off;
  - therefore a pre-retail trial-copy giveaway existed on the China.com community/distribution surface.
- Does not support:
  - that the giveaway copy was optical rather than download-only;
  - magazine identity;
  - executable version, file tree, hashes or byte identity;
  - identity with the collector's later-described Mainland 1.0 magazine-insert test manual/disc.

### SRC-CN-2020-GAMER-MAINLAND-SA10-TEST-CARRIER-LEAD-01

- Title/context: `石器時代周邊收藏，石器用戶端禮包篇（四）1.82石器新手用戶端包`
- Publication date: **2020-09-17**
- Retrieval date: **2026-09-27**
- Source: Bahamut StoneAge forum; physical-media collector `stoneage2017 / 寂寞如風`
- URL: https://forum.gamer.com.tw/C.php?bsn=1571&snA=81396
- Confidence: **C+/OPEN for the test-carrier identity; later first-person ownership claim**
- Supports:
  - after distinguishing a rumored boxed 1.0 image as unverified, the collector states that the Mainland 1.0 test item he knows/obtained was a **test manual carrying a disc, distributed with a magazine, without a retail box**.
- Archaeology significance:
  - if authenticated, this could predate the ordinary 1.82/Jinhaiwan retail-disc family and become the earliest Mainland physical client bridge.
- Critical limits:
  - no contemporaneous magazine title/issue is named in the text;
  - no public file tree, hashes, matrix, publication number or byte provenance is supplied;
  - the claim must not be merged with the separate China.com trial-giveaway notice without evidence that they refer to the same distribution event.

### SRC-CN-2001-WAEI-SA-MANUAL-ERRATA-MIRROR-01

- Original announcement date: **2001-03-12**
- Original issuer: 北京华义联合软件开发有限公司
- Preserved title: `北京华义对笔误事件的道歉启事及最终处理办法`
- Retrieval date: **2026-09-27**
- Preserved transcription: https://www.shiqi.me/pt_25.htm
- Source type: later preservation/transcription of an official Beijing-Waei announcement.
- Confidence: **B for the literal preserved announcement; exact original manual line still unresolved**
- Supports:
  - Waei attributes the dispute to a **manual editing error**;
  - players believed 50 hours of game time had been removed;
  - **second-batch newly printed manuals would be corrected**;
  - **first-batch manuals would only receive a web erratum**;
  - products registered before 2001-03-13 09:00 were to receive an additional **300 points = 50 hours**.
- Archaeology significance:
  - proves that first- and second-batch Mainland manuals contain a potentially diagnostic textual difference;
  - creates a physical-print discriminator independent of outer package artwork.
- Does not support:
  - the exact erroneous printed number by itself;
  - disc-byte differences between first and second printings.

### SRC-CN-2001-17173-SA10-CHARGING-01

- Title/context: surviving 17173 StoneAge 1.0 charging page
- Retrieval date: **2026-09-27**
- URL: https://news.17173.com/z/stoneage/banben/sa10/01.htm
- Source type: surviving contemporaneous portal/version page.
- Confidence: **A-/B+ for the displayed charging table**
- Supports:
  - 0.1 WGS point/minute, 6 points/hour;
  - 300 points = 50 hours; 600 points = 100 hours;
  - the displayed product-registration rule is **300 points / 50 hours**.
- Use:
  - independent control for the corrected post-errata registration standard.
- Does not support:
  - what the first-print manual itself said before correction.

### SRC-CN-2003-17173-SA-600-TO-300-RECOLLECTION-01

- Title: `服7-…虎暴族，永恒的回忆`
- Publication date: **2003-03-24**
- Retrieval date: **2026-09-27**
- Source: 17173 player retrospective
- URL: https://news.17173.com/z/stoneage/content/2003-3-24/n496_412682.html
- Confidence: **C+/B- as a near-period first-person recollection; not official documentation**
- Supports:
  - the author recalls buying StoneAge around the start of charging and says that the previously stated **600 points became 300 points**.
- Cross-source interpretation:
  - this is consistent with Waei's official 50-hour manual-error dispute and the corrected 300-point/50-hour standard;
  - it materially strengthens the hypothesis that the erroneous first-print statement involved **600 points / 100 hours**.
- Critical limit:
  - do not promote that exact first-print wording to FACT until a manual scan/photo or contemporaneous report quotes it directly.


## 2026-09-27 source-survival correction: direct China.com legacy pages recovered

The earlier records `SRC-CN-2001-CHINADOTCOM-SA-TRIAL-GIVEAWAY-MIRROR-01` and `SRC-CN-2001-WAEI-SA-MANUAL-ERRATA-MIRROR-01` remain preserved as fallback mirrors/transcriptions. They are **superseded for source quality**, not deleted: direct legacy China.com StoneAge pages are still live and now provide a closer contemporaneous source surface.

### SRC-CN-2000-CHINADOTCOM-SA-TEST-CD-GIVEAWAY-01

- Title/body heading: **`石器时代游戏测试光盘免费大赠送`**
- Original period: **December 2000**
- Retrieval date: **2026-09-27**
- Surviving legacy page: https://game.china.com/hotspot/shiqi/answer/index.html
- Source type: **still-live legacy China.com / 中华网游戏频道 StoneAge activity page**
- Confidence: **A-/B+ for the literal distribution terms and dates shown on the legacy page**
- Supports:
  - the giveaway object is explicitly a **游戏测试光盘**, not merely a generic trial entitlement;
  - Beijing-external participants answered questions and supplied detailed address information to receive the **disc free**, while supplies lasted;
  - **Beijing participants were instructed to collect the disc at 晶合软件 sales points**;
  - activity deadline: **2000-12-31**;
  - official test period: **2000-12-15 through 2001-01-10**.
- Archaeology significance:
  - proves a pre-retail Mainland physical optical carrier existed;
  - creates the earliest currently source-defined Mainland client-disc recovery target;
  - gives a concrete distribution-channel token: **晶合软件**.
- Does not support:
  - exact disc artwork, volume label, filesystem, executable version, publication number, matrix/IFPI or hashes;
  - byte identity with Taiwan v1.0;
  - byte or physical identity with the collector-described magazine-insert test manual/disc.

### SRC-CN-2001-CHINADOTCOM-SA-LEGACY-PRODUCT-01

- Title/context: China.com legacy StoneAge formal product / launch page
- Retrieval date: **2026-09-27**
- URL: https://game.china.com/hotspot/shiqi/news/1.html
- Source type: still-live legacy China.com game-channel page preserving contemporary product information
- Confidence: **A-/B+ for literal product fields**
- Supports:
  - Mainland formal product release: **2001-01-12**;
  - retail price: RMB 29;
  - language: Simplified Chinese;
  - **carrier: 1 CD-ROM**;
  - JSS production, Beijing Waei authorization, Zhiguan Beijing general agency, Guangxi-Jinhaiwan publication/distribution;
  - four different Mainland package designs and a contemporaneous **45-hour** launch-time statement.
- Archaeology significance:
  - gives a direct formal-retail optical-carrier control immediately after the test-CD period;
  - supports treating the December-2000 test CD and January-2001 retail CD as separate recovery objects until byte evidence proves otherwise.

### SRC-CN-2001-CHINADOTCOM-SA-LEGACY-NEWS-ARCHIVE-01

- Context: surviving China.com StoneAge legacy news archive
- Retrieval date: **2026-09-27**
- URL: https://game.china.com/hotspot/shiqi/news/2.html
- Source type: still-live legacy portal archive preserving contemporary China.com and Beijing-Waei notices
- Confidence: **A-/B+ for literal dated notices on the legacy page**
- Supports:
  - **2001-01-11** mail-order follow-up: participants in the earlier StoneAge trial-version giveaway received a discounted formal copy;
  - **2001-02-26** charging notice: 300 points = 50 hours, 600 points = 100 hours, product registration grants 300 points / 50 hours;
  - **2001-03-12** Beijing-Waei manual-errata apology: second-batch printed manuals would be corrected, first-batch manuals would receive web errata, and eligible existing registrants received an additional 300 points = 50 hours.
- Source correction:
  - this page materially upgrades the source surface behind the project's earlier later-mirror records;
  - the garbled character rendering in some modern crawlers is an encoding/replay issue; the dates, numeric tables and page/link structure remain recoverable, while clean secondary mirrors remain useful for Chinese-text control.
- Does not by itself expose the exact erroneous first-print manual line.

### SRC-CN-EARLY-JINGHE-SA-TEST-DISTRIBUTION-01

- Title/context: `晶合软件` / Beijing Jinghe Era Software corporate profile
- Retrieval date: **2026-09-27**
- URL: https://www.ourgame.com/subject/globallink/jinhe.html
- Source type: surviving early corporate/channel profile; exact publication date not exposed on the current page
- Confidence: **B for the literal corporate-history statement**
- Supports:
  - 晶合时代 operated a broad software-sales chain;
  - the company profile explicitly says it organized **`《石器时代》测试版软件的免费发放`**;
  - the same profile identifies close institutional/business ties between Jinghe and `《大众软件》`.
- Cross-source significance:
  - independently coheres with China.com's instruction that Beijing players collect StoneAge test discs from **晶合软件销售点**.
- Critical limit:
  - Jinghe's connection to `《大众软件》` does **not** prove that the collector-described magazine-insert Mainland 1.0 test disc came from a specific Popsoft issue;
  - no exact 2000 Popsoft issue/disc carrier has been resolved in this pass.


### SRC-CN-2002-17173-SA-TEST-CD-BURNED-COPY-RECOLLECTION-01

- Title: `回首往事，我们从外挂中走来~`
- Publication date: **2002-08-19**
- Retrieval date: **2026-09-27**
- Source: 17173 StoneAge player-history article
- URL: https://news.17173.com/z/stoneage/content/2002-8-19/n337_253594.html
- Source type: near-period first-person player retrospective; **not official documentation**
- Confidence: **B-/C+ for the author's own access path; not physical-original provenance**
- Supports:
  - the author explicitly places Mainland public testing in **December 2000**;
  - the author recalls the test-version Christmas period and says he began playing using a **disc burned/copied by a friend**.
- Archaeology significance:
  - independently demonstrates a plausible **player-burned-copy survival class** during the test period;
  - warns that a recovered early disc can carry historically correct test payload while lacking official physical-carrier provenance.
- Does not support:
  - the artwork, label, matrix, volume label or hashes of the official China.com/Jinghe giveaway disc;
  - identity between the friend's burned copy and any later collector-described magazine-insert test disc;
  - byte identity with Taiwan v1.0 or the January-2001 Mainland retail CD.
- Operational rule:
  - authenticate **payload lineage** and **physical-carrier lineage** separately for every future test-client specimen.


### SRC-CN-2000-CHINADOTCOM-SA-GIVEAWAY-RESULT-ARCHIVE-01

- Historical target: China.com article **`63271`**, linked directly from the still-live StoneAge test-CD giveaway page as the post-activity list/results address.
- Original URL: `http://game.china.com/zh_cn/news/news1/444/20001220/63271.html`
- Retrieval/recovery date: **2026-09-27**
- Source type: Wayback CDX + privacy-safe archived HTML replay
- Confidence: **A-/B+ for archive identity and page role**
- Archive metadata:
  - **8 HTTP-200 text/html captures** from 2001-03-09 through 2003-09-01;
  - earliest capture: **20010309223137**;
  - earliest replay body: **44,048 bytes**;
  - replay SHA-256: `a26933f2cdcf2d5e2fcd6c808000ae8c37af4c9999bcb17bda04feac3c68d403`;
  - decoded as GB18030.
- Privacy-safe page-level supports:
  - visible-text token counts include `石器时代` (2), `赠送` (1), `名单` (3), `光盘` (1);
  - the page contains fields consistent with a recipient/contact list.
- Privacy boundary:
  - **participant names, addresses, telephone numbers, email addresses and raw archived HTML are not committed or reproduced**;
  - only page-level classification, hashes, aggregate marker counts and sanitized first-party path topology are retained.
- Asset follow-up:
  - 11 first-party image/background paths parsed;
  - 9 successfully replayed assets are small generic China.com logo/navigation/UI files;
  - 0 large/page-specific candidate image assets;
  - unreplayed residual names are `close.gif` and `chinacom_logo.gif`, both generic UI identities.
- Supports:
  - the live giveaway page's results/list link is historically real and archived;
  - the archived target is a StoneAge test-CD giveaway-results page.
- Does not support:
  - disc artwork, filename, volume label, matrix/IFPI, publication number, filesystem, hashes or build identity.
- Derived reports:
  - `research/recovered/STONEAGE-CHINA2000-TEST-CD-LEGACY-ARCHIVE-R1.txt`;
  - `research/recovered/STONEAGE-CHINA2000-63271-REPLAY-R1.txt`;
  - `research/recovered/STONEAGE-CHINA2000-63271-ASSET-TOPOLOGY-R1.txt`.

### SRC-CN-IA-POPSOFT-2000-LAUNCH-WINDOW-01

- Preservation item: Internet Archive `popsoft-magazine_202403`
- Retrieval date: **2026-09-27**
- Source type: preserved `大众软件 / Popsoft` magazine scan family + transient OCR derivatives
- Confidence: **S/A for the preserved scan metadata; negative/limited for carrier inference**
- Candidate rationale:
  - contemporaneous Jinghe distribution evidence plus Jinghe's institutional relationship with `《大众软件》` made Popsoft a source-driven magazine candidate;
  - a later collector independently says a Mainland 1.0 test manual+disc was distributed with an unspecified magazine.
- Probe scope:
  - OCR derivatives for **2000-11A/B, 2000-12A/B, 2001-01A/B**;
  - no magazine PDF/image body committed;
  - no game/optical payload downloaded.
- Result:
  - **6 OCR issue files** inspected;
  - **0 optical-image files** exposed by current IA metadata;
  - **1 StoneAge anchor** across the six issues: literal `Stone Age` in 2000-12A;
  - **0 strong carrier-context hits** around StoneAge anchors.
- Classification:
  - **EDITORIAL-ONLY SIGNAL / NO TEST-CD CARRIER EVIDENCE in the tested OCR window**.
- Critical limit:
  - OCR can miss stylized text, advertisements or image-only inserts;
  - this does not prove no Popsoft-related carrier ever existed;
  - it is sufficient to stop treating Popsoft as the default/leading magazine identity without a new exact token.
- Derived report: `research/recovered/STONEAGE-POPSOFT-2000-LAUNCH-WINDOW-R1.txt`.


### SRC-CN-2001-17173-WAEI-TRIAL-DOWNLOAD-RECOLLECTION-01

- Title: `我活在石器`
- Publication date: **2001-06-13**
- Source: 17173 StoneAge player diary / first-person chronology
- URL: https://news.17173.com/z/stoneage/content/2001-6-13/n987_903725.html
- Retrieval date: **2026-09-27**
- Confidence: **B-/C+ for the author's own access experience; not preserved payload provenance**
- Supports:
  - diary entry explicitly dated **2001-01-04 18:00**;
  - before the Jan-12 formal release, the author visited the **Waei homepage** and saw a **StoneAge trial version** available for download;
  - the author's download manager reported **“274多兆”** before the author abandoned the download because of telephone cost.
- Archaeology significance:
  - independently establishes an early **online trial-client distribution route** alongside the separately proven physical test-CD route;
  - supplies a useful approximate-size constraint for future filename/archive matching.
- Does not support:
  - exact filename or exact byte length;
  - exact Waei host/path;
  - identity with the China.com/Jinghe test CD, magazine-insert carrier or retail disc;
  - clean-byte provenance.

### SRC-WAEI-2001-SPR1-ARCHIVE-01

- Artifact: `spr_1.bin`
- Historical archive path: Waei.net central download, Big5 `修補程式` directory
- Wayback capture: **20010605174550**
- Retrieval/analysis date: **2026-09-27**
- Source type: archived binary + accepted Taiwan v1.0 controlled structural diff
- Raw original bytes: **transiently analyzed only; not committed**
- Waei archived artifact:
  - bytes: **2,889,630**;
  - SHA-256: `864fa3f6aaeb7d8d2dc9bdee46cecdc7dcee1af0c8f1ed949e09c0526e6aa17e`;
  - SHA-1: `e8073bde417020b52ff48e4f8559c938c90fc9cc`;
  - MD5: `7b40970c8f2a11a523f4a314c78b459e`;
  - Wayback CDX digest `5ADTXXSBOAQLKL7URZHYKWOJHDEQ7SOM` matches the recovered SHA-1/Base32 exactly.
- Accepted Taiwan-v1 control:
  - same filename and **same 2,889,630-byte length**;
  - Taiwan SHA-256 `53d5b2d40453a30fd1569637ebf0db7b3010542b00970ec83af0295a3b3ae31a`;
  - bytes are not identical.
- Structural proof:
  - Waei file parses exactly under the accepted Taiwan v1.0 `spradrn_1.bin`;
  - **464 groups / 39,065 animations / 242,085 frames**;
  - **463 groups are byte-identical**;
  - only group 102 / `spr_no=100102` differs;
  - total difference: **16 bytes in four 4-byte runs**.
- Semantic delta:
  - four `bmp_no` fields change from Taiwan sentinel `0xFFFFFFFF` to **126235, 126236, 126237, 126238**;
  - all four IDs are absent from Taiwan v1.0's `adrn_1.bin`.
- Direct catalogue/route binding:
  - Waei central-download **ID=1** is the `修補程式` category;
  - preserved catalogue title: **`石器隱形人無所遁形修正檔`**;
  - displayed date: **2001/4/26**;
  - displayed size: **2,822 KB**;
  - catalogue instruction: place the file in the StoneAge execution directory, e.g. `C:\\Program Files\\Waei\\石器時代\\data`, overwriting the existing file;
  - download control: **`download.asp?fileid=133`**;
  - archived fileid=133 capture at **20010605174213** returns HTTP 302 with historical target `/download/file/<Big5 修補程式>/spr_1.bin`;
  - the preserved target is captured at **20010605174550** and its recovered **2,889,630 bytes = 2,821.904 KiB**, consistent with the catalogue's rounded 2,822-KB value.
- Classification:
  - **A / direct official Waei StoneAge patch provenance + byte-verified payload**;
  - **FACT:** `spr_1.bin` is the payload of Waei fileid 133 / `石器隱形人無所遁形修正檔`;
  - **OPEN:** exact client version/build and regional branch binding.
- Critical source-quality note:
  - the human-readable StoneAge title association is now direct and no longer rests on generic site-navigation text or container similarity alone;
  - container geometry and the Taiwan-v1 controlled diff remain independent technical corroboration, not the sole basis for product identity.
- Companion-file boundary:
  - exact same-directory archive checks find no captured `spradrn_1.bin`, `adrn_1.bin`, or `real_1.bin`;
  - a companion image-resource update is a strong inference, not a recovered fact.
- Derived reports:
  - `research/recovered/STONEAGE-WAEI-DOWNLOAD-CENTER-INDEX-CENSUS-R1.txt`;
  - `research/recovered/STONEAGE-WAEI-SPR1-BYTE-METADATA-R2.txt`;
  - `research/recovered/STONEAGE-WAEI-VS-TW10-SPR1-DIFF-R1.txt`;
  - `research/recovered/STONEAGE-WAEI-VS-TW10-SPR1-FIELD-DIFF-R2.txt`;
  - `research/recovered/STONEAGE-TW10-BITMAP-126235-126238-R1.txt`;
  - `research/recovered/STONEAGE-WAEI-DOWNLOAD-ID12-R1.txt`;
  - `research/recovered/STONEAGE-WAEI-ID1-PATCH-CONTROLS-R1.txt`;
  - `research/recovered/STONEAGE-WAEI-FILEID133-ROUTE-R1.txt`;
  - `research/recovered/STONEAGE-WAEI-FILEID133-HEADER-R1.txt`.

### SRC-CN-2001-YEGAME-SA-PRODUCT-CATALOG-01

- Source chain:
  - archived `www.jhpop.com` root, capture **2000-12-04 16:03:00 UTC**, directly redirects to `http://www.yegame.com`;
  - archived Yegame pages identify the commerce surface as **晶合软商网 / 晶合商机网**;
  - dedicated historical game catalog path: `/product/game/`.
- Key archive capture: **2001-04-06 01:45:44 UTC**.
- Historical page: `http://yegame.com:80/product/game/prod_secshow.asp?prod_secid=N`.
- Retrieval/analysis date: **2026-09-27**.
- Source type: archived historical commerce catalog HTML.
- Confidence: **A-/B+ for literal catalog fields and product-code association; not client-byte provenance**.
- Directly supports:
  - category: network games;
  - product name: **石器时代**;
  - product detail key: **`EN0ZGKJ0002`**;
  - product medium: **`1-CD`**;
  - catalog field **更新日期: 2001-1-16**;
  - retail price: **¥29.00**;
  - wholesale price: **¥26.00**;
  - separate product **石器时代-WGS620点会员卡**, detail key **`EZ0JHSD0003`**.
- Cross-source interpretation:
  - the **1-CD** medium independently corroborates the surviving China.com formal-product record `载体：1 CD-ROM`;
  - the product code provides a new exact recovery token for cover images, catalog/detail mirrors, and physical-media provenance.
- Critical limits:
  - **do not interpret `2001-1-16` as a release date** without separate evidence; the field is explicitly the catalog's `更新日期`;
  - this does not identify the **2000-12 official test CD**, prove identity with a magazine-insert copy, or recover any executable/disc bytes;
  - retail/wholesale values are catalog metadata and are secondary to artifact recovery.
- Derived evidence:
  - `research/recovered/STONEAGE-JHPOP-2000-ROOT-REPLAY-R2.txt`;
  - `research/recovered/STONEAGE-YEGAME-2000-TEST-CD-ARCHIVE-R1.txt`;
  - `research/recovered/STONEAGE-YEGAME-EXACT-PAGE-REPLAY-R1.txt`;
  - `research/recovered/STONEAGE-YEGAME-GAME-CATALOG-R1.txt`.

### SRC-CN-2001-YEGAME-SA-PRODUCT-DETAIL-01

- Title/surface: Yegame / 晶合商机网 StoneAge product-detail pages.
- Retrieval/analysis date: **2026-09-27**.
- Source type: archived historical commerce HTML + Wayback capture metadata.
- Confidence: **A-/B+ for literal product-detail text and catalog fields; not binary provenance**.
- StoneAge product route:
  - exact key: **`EN0ZGKJ0002`**;
  - route: `product/detail.asp?prodencode=EN0ZGKJ0002`;
  - preserved HTTP-200 captures: **20010415162300**, **20010717235414**, **20010816203529**;
  - successfully replayed capture: **20010816203529**.
- Direct replay supports:
  - product name **石器时代**;
  - code **`EN0ZGKJ0002`**;
  - medium **`1-CD`**;
  - retail **¥29.00**, preferential **¥26.00**;
  - promotional text: **随游戏赠送45小时免费时间，2001年1月至2月期间贺岁免费畅游**;
  - gameplay marketing copy describing capture/growth of pets, more than 100 creatures, 12 base character designs in four colors, and 12 expressive actions;
  - referenced product-image path **`/product_images/EN0ZGKJ0002.jpg`**.
- Minimum-configuration text preserved on the catalog page includes DirectX 6.1 support, 2 MB display memory, 32 MB RAM, 400 MB disk, 33.6k modem and Internet access. The CPU/OS strings contain apparent catalog/transcription oddities, so this page is not promoted over manuals/client evidence for technical requirements.
- WGS-card route:
  - exact key: **`EZ0JHSD0003`**;
  - three HTTP-200 captures: **20010406121011**, **20010616204348**, **20010830173408**;
  - direct text identifies **石器时代-WGS620点会员卡**, **620 points**, medium **单卡**, retail **¥30.00**, preferential **¥27.00**.
- Image preservation boundary:
  - the detail HTML directly references `product_images/EN0ZGKJ0002.jpg` and `product_images/EZ0JHSD0003.jpg`;
  - exact CDX requests for these product images encountered transient connection failures in this run;
  - image existence in HTML is FACT; archived image-body availability remains OPEN.
- Does not support:
  - identity with the **2000-12 Mainland official test CD**;
  - retail-disc hashes/file tree;
  - equivalence with the ~274 MB Waei online trial client;
  - interpreting catalog copy as higher authority than original media/manual bytes.
- Derived report: `research/recovered/STONEAGE-YEGAME-STONEAGE-PRODUCT-DETAIL-R1.txt`.

### SRC-TW-2001-WAEI-SAUPDATE-RUNTIME-BYTES-01

- Historical first-party host: `stoneage.waei.net`.
- Surface: `/saupdate/`, independently embedded in the accepted Taiwan v1.0 `StoneAge.exe` launcher as `/saupdate/newest.txt` and `/saupdate/%s`.
- Retrieval/research date: 2026-09-27.
- Source type: Wayback-preserved first-party Waei update executable payloads, transiently replayed and hashed; raw executables are not committed.
- Confidence: S/A+ for exact archived bytes, hashes and PE metadata; OPEN for exact marketing-build assignment.
- `sa_40.exe`: earliest recovered HTTP-200 capture 2001-10-31 15:57:47 UTC; 528,384 bytes; SHA-256 `d54a6c109644dd4842f61bdd42a95362fda7a16f5e9b9dbd829d6b97c678fde1`; SHA-1 `6eafbf9a886021291cde16b7c9baf22192bae32a`; MD5 `9b9820b6e3e4578a93c20ba34309bd21`; PE timestamp 2001-09-27 08:31:27 UTC.
- `sa_42.exe`: earliest recovered HTTP-200 capture 2001-12-06 18:31:20 UTC; 557,056 bytes; SHA-256 `744fc0557f024930f351ef31b6adac0dbe41968625105d5f0eba45be1a048df6`; SHA-1 `45b0f0a3de4d04961cd0a43c3d70209d35089724`; MD5 `608f5b92c5de42496e839d59d23ad12d`; PE timestamp 2001-11-01 02:54:29 UTC.
- Both are normal PE game runtimes, not installer/SFX wrappers. Version resources identify CompanyName=Waei, FileDescription/InternalName=SaDeb, OriginalFilename=SaDeb.exe, ProductName=Waei SaDeb, version 1.0.0.1.
- Both contain `updated`, `StoneAge.exe` and `yStoneAge.exe`, while updater host/path strings reside in the separate launcher.
- Evolution: both contain battle-map paths through battle219; accepted Taiwan v1.0 `sa_3.exe` reaches battle217; `sa_42` adds `data\\AISetting.dat` and `data\\album_2.dat` relative to `sa_40`.
- Exact first-party generation census: `sa_3` 0 rows; `sa_23` 404 only; `sa_24` 0 rows; `sa_25` 0 rows after dedicated retry; `sa_40` repeated HTTP-200 stable digest; `sa_41` 404 only; `sa_42` repeated HTTP-200 stable digest.
- Critical boundary: filenames `sa_40/sa_42` are not proof of marketing StoneAge 4.0/4.2; use SRC-TW-2003-WAYI-PROSPECTUS-PRODUCT-CHRONOLOGY-01 for the corporate marketing-version chronology.
- Derived reports: `research/recovered/STONEAGE-WAEI-SUBDOMAIN-LAUNCH-CDX-R1.txt`; `research/recovered/STONEAGE-WAEI-SA40-SA42-PAYLOAD-CLASSIFIER-R1.txt`; `research/recovered/STONEAGE-WAEI-SA40-SA42-LINEAGE-R1.txt`; `research/recovered/STONEAGE-WAEI-SAUPDATE-DIRECTORY-R1.txt`; `research/recovered/STONEAGE-WAEI-RUNTIME-GENERATIONS-R1.txt`; `research/recovered/STONEAGE-WAEI-SA25-GENERATION-RESIDUAL-R1.txt`.

### SRC-TW-2003-WAYI-PROSPECTUS-PRODUCT-CHRONOLOGY-01

- Title: `華義國際數位娛樂股份有限公司 公開說明書（股票初次申請為櫃檯買賣用稿本）`.
- Publisher/issuer: 華義國際數位娛樂股份有限公司 / WAYI INTERNATIONAL DIGITAL ENTERTAINMENT CO., LTD.
- Printed date in document: ROC 92-05-20 = 2003-05-20.
- First-party URL: `https://www.wayi.net/service/files/d00074a14a8ff1f472056ede383e7a0f.pdf`.
- Relevant location: PDF page 39, table `開發成功之技術及產品`.
- Retrieval/research date: 2026-09-27.
- Source type: first-party corporate public prospectus.
- Confidence: A+/S for the literal corporate product/date table.
- Directly supports: StoneAge 2.0 家族開拓史 = 2001-08-01; StoneAge 2.5 精靈王傳說 = 2001-11-01; StoneAge 3.0 伊甸新大陸 = 2002-03-01; StoneAge 4.0 新九大家族 = 2002-07-01.
- Archaeology consequence: `sa_40.exe` compiled in September 2001 cannot denote marketing StoneAge 4.0, which Waei dates to July 2002. `sa_42.exe` has a PE timestamp of 2001-11-01, coinciding with Waei's table date for 2.5; this is strong temporal alignment only, because the prospectus does not name `sa_42.exe`.
- Boundary: corporate release dates do not authenticate a client binary; PE linker timestamps are byte metadata, not independent release-date statements.

### SRC-TW-COMMUNITY-SA24-CHRONOLOGY-01

- Context: later StoneAge community chronology preserved by We Love SA and the Bahamut StoneAge archive.
- URLs: `https://www.lab.welovesa.com/viewthread.php?extra=page%3D1&tid=38`; `https://forum.gamer.com.tw/G2.php?bsn=1571&sn=1958`.
- Retrieval/research date: 2026-09-27.
- Source type: later community chronology / historical recollection compilation; not first-party Waei documentation.
- Confidence: B-/C+ for the literal preserved chronology wording; secondary evidence only for 2001 operator events.
- Key literal entry: 2001-04-24 — `更新 SA_24 中增加了交易系統`.
- The We Love SA page also preserves a retrospective topic label `sa_25 全螢幕時代!?`, supporting use of `SA_N` as update/runtime-generation vocabulary.
- Significance: `SA_24` in April 2001 predates Waei's first-party 2.0 marketing date of 2001-08-01, so the suffix cannot be read as a marketing major/minor version. This is consistent with byte-recovered first-party `sa_40/sa_42` representing later runtime generations.
- Limits: no `sa_24.exe` or `sa_25.exe` bytes are preserved by this source; exact first-party Wayback probes currently expose 0 rows for both paths.


### SRC-DESCENDANT-NOCAST-PINNED-PROFILES-R1

- Retrieval/audit date: **2026-10-01**.
- Sources: `gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`, `iriselia/StoneAge@9e6c8ce2cd8ed532a7157773acd1c61582c178b5`, `BismarckDD/stoneage@999ffdf1d220ec6666eb65339180689c9caf1876`.
- Type/confidence: pinned later public descendant source; A for literal handler/profile behavior, not authenticated Taiwan-v1 or recovered25 build identity.
- Audited paths per source root: `battle/pet_skill.c`, `battle/battle.c`, `battle/battle_event.c`, `magic/magic.c`, `include/version.h`, `include/char_base.h`, `include/battle.h`, `include/battle_event.h`.
- Actual preprocessor/header enum checks: gavin/iris compile `_SKILL_NOCAST`, command 2025, status index 10 vs WORKNOCAST 54; pinned Bismarck disables the callback, so its source presence is a textual control only and supplies no compiled Nocast command.
- Supports the sequential byte parser, independent MultiList target expansion, shared status/RNG/resistance ordering, PET exclusion after hit RNG, exact counter write, FALSE-return quirk, direct-magic gating and status-counter/NC-notification timing.
- Derived-only source hashes/profile output: `research/recovered/STONEAGE-NOCAST-SOURCE-AUDIT-R1.txt`; reproducible audit: `tools/stoneage_nocast_source_audit.py`; specification: `research/mechanics/STONEAGE-NOCAST-R1.md`.
- Boundaries: missing turn and unsafe target-list domains remain historical UB; active recovered25 OPTION values need a separate hash-verified preservation-bundle probe; no Taiwan-v1 membership or universal numeric COM1 is asserted.

- Acceptance update: verified bundle workflow **36881045423 = PASS** at `02b443d618d3ed10c617e33d46c26cf309a0e0d9`; derived report `research/recovered/STONEAGE-25-NOCAST-PROBE-R1.txt` committed by `2f461c0a36af906b6514cedd6a1c1fa6c247f47c`.
- Recovered metadata: ID 580, FIELD=1, TARGET=3, COST=2, ILLEGAL=1000; 15 OPTION bytes, SHA-256 `28c465f3106af23dafc91aa2c54c7c7c8ff147dd26d8ee92382ecd4862dd871f`; strict CP950/Big5 parser results turn=3 and Success offset=50; 18 slot uses across 16 templates. This supersedes the pending data gate above, while executable runtime/compile-profile identity remains OPEN.
- Guarded reference/source-profile workflow **36881045171 = PASS** at the same source commit.

### SRC-DESCENDANT-ATTACKCRAZED-PINNED-PROFILES-R1

- Retrieval/audit date: **2026-10-04**.
- Sources: `gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`, `iriselia/StoneAge@9e6c8ce2cd8ed532a7157773acd1c61582c178b5`, `BismarckDD/stoneage@999ffdf1d220ec6666eb65339180689c9caf1876`.
- Type/confidence: pinned public later descendant source; A for literal source/profile behavior, OPEN for recovered25 binary identity and Taiwan-v1 membership.
- Audited paths: `battle/pet_skill.c`, `battle/battle.c`, `include/version.h`, `include/battle.h`, `include/pet_skillinfo.h` under each pinned source root.
- Supports callback 0.8/0.7 work-power writes, LOW array/HIGH atoi count, preselected random target list excluding side slots 9/19, first non-bow hit using the original TargetAdjust, later hits skipping list[0], no AttackCrazed damage division, and post-sequence ordinary counter boundary.
- Profile differences: `_SHOOTCHESTNUT` same-side gate enabled in gavin/iris and disabled in Bismarck; Bismarck's OPTION pointer comparison is not a NULL guard. All three compiled command enums are 2010 and source skill macros are 608; neither identifies recovered row 613's binary COM1.
- Reproducible audit: `tools/stoneage_attack_crazed_source_audit.py`; derived report: `research/recovered/STONEAGE-ATTACKCRAZED-SOURCE-AUDIT-R1.txt`; specification: `research/mechanics/STONEAGE-ATTACKCRAZED-R1.md`.
- Runtime remains OPEN; safe reference domain is non-null OPTION count 1..19. Actual recovered metadata/count requires the separate verified preservation-bundle probe.

- Acceptance update: workflows **37174398691** (reference) and **37174398688** (source + hash-verified preservation data) PASS at `4539d885cf0007cd1b4e50dd311dd3ba397de7b9`; derived report written by `cc896d6b647e91c33675f8c97976e3d6695767bf`.
- Exact recovered ID 613: FIELD=1, TARGET=1, COST=2, ILLEGAL=0; one non-NUL OPTION byte, SHA-256 `4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce`, attack count=3; 9 uses/9 templates reproduced. This supersedes the pending data gate above, while ordered runtime and early-version membership remain OPEN.

- Runtime acceptance update — 2026-10-04: typed enemy-AI/ordered-round/persistent-coordinator execution at `26d47e45402b302822639c524b82396b29b0c6a0` passed dedicated workflow **37175407818**, battle core **37175407825**, coordinator **37175407757** and runtime golden **37175407754**, plus related skill/magic regressions. Local 985-test acceptance includes a two-round persistence witness. Closure is limited to explicit recovered enemy/opposite-side/FIST/count-3; no historical numeric COM1, original skill-array index, or Taiwan-v1 membership is assigned. Verified pressure reranking **37175482501** accounts for the 9 accepted uses and selects `PETSKILL_Mdfyattack` next.


### SRC-DESCENDANT-MDFYATTACK-PINNED-PROFILES-R1

- Retrieval/audit date: **2026-10-04**.
- Sources: `gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`, `iriselia/StoneAge@9e6c8ce2cd8ed532a7157773acd1c61582c178b5`, `BismarckDD/stoneage@999ffdf1d220ec6666eb65339180689c9caf1876`.
- Type/confidence: pinned public later descendant source; A for literal callback/dispatch/attribute/event behavior, OPEN for recovered25 compiled profile and Taiwan-v1 membership.
- Audited surfaces: pet_skill.c, battle.c, battle_event.c, version/battle/event/pet-skill headers; actual delimiter/copy helpers. Bismarck's split helper is server/common/utils/util_string.c with workspace.c copy helpers, and its shared AttrCalc resides in battle_magic.c; the audit uses these live files, not remove_code controls.
- Actual compilation: gavin/iris Mdfyattack command 2030 vs Modifyattack 2029; Bismarck 2028 vs 2027; BCF_MODIFY 2097152. Both callbacks remain distinct. Numeric recovered COM1 remains unassigned.
- Supports exact ASCII code/atoi/COM4 setup, all-five-weight replacement with neutral zero, property/field/AttrCalc ordering, local event cancellation independent from actor COM1, specialized single-hit/no ordinary counter dispatch, and Guardian output not reassigned by the event wrapper.
- Source-profile boundary: property/suit features are enabled in these descendants, but the numerical reference admits their absence only. Bismarck's OPTION pointer comparison is defective and its byte helper differs; no null-pointer/non-ASCII/undefined arithmetic behavior is invented.
- Reproducible audit: `tools/stoneage_mdfyattack_source_audit.py`; report: `research/recovered/STONEAGE-MDFYATTACK-SOURCE-AUDIT-R1.txt`; specification: `research/mechanics/STONEAGE-MDFYATTACK-R1.md`. Local native oracle uses UBSan on transient actual functions and passes 45 callback + 3075 attribute cases. Data population/OPTION requires the separate hash-verified bundle probe; runtime remains OPEN.


- Mdfyattack data acceptance update — 2026-10-04: reference **37176835218** and pinned-source/hash-verified preservation probe **37176835194** PASS at `4140c8ee2c7894b5f4956814e8e51f5c03d6b345`; derived report `743cf5255d5a694556ad3ebae67e886edaae8467`. IDs 548/549/550/551 all have FIELD=1/TARGET=6/COST=2/ILLEGAL=2000, six non-NUL ASCII OPTION bytes, index 0/1/2/3 and amount 100. Population 8 uses / 8 templates. This supersedes the preceding data pending gate. Typed runtime local 1024-test acceptance includes all elements, specialized Guardian/original-target settlement, reaction/event distinction, counter/combo exclusion and two-round persistence; remote runtime acceptance remains pending.


- Mdfyattack runtime acceptance update — 2026-10-04: source `102b308c7c738d64bce00a3a25c89ebd39d89afd` passed dedicated **37177521796**, battle core **37177521656**, coordinator **37177521753**, golden **37177521767**, repeated reference/source-data gates and all related magic/skill/gameplay regressions. Local 1024-test acceptance includes 19 runtime tests and two-round persistence; additional pressure regression passes 3 tests. Accepted execution is recovered base enemy/opposite-side/FIST/amount-100 only, retaining Guardian/original-target, reaction/event and counter/combo boundaries. Pressure **37177629438** accounts for the 8 accepted uses and selects `PETSKILL_Weaken` (575/576, 7 uses / 6 templates). Numeric recovered COM1/skill-array indices and Taiwan-v1 membership remain unassigned.


### SRC-DESCENDANT-WEAKEN-PINNED-PROFILES-R1

- Audit date: **2026-10-04**. Sources: `gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`, `iriselia/StoneAge@9e6c8ce2cd8ed532a7157773acd1c61582c178b5`, `BismarckDD/stoneage@999ffdf1d220ec6666eb65339180689c9caf1876`.
- Type/confidence: pinned later public source; A for literal callback/profile/parser/shared-status behavior, OPEN for recovered25 compiled build and Taiwan-v1 membership.
- Audited paths under source roots: battle/pet_skill.c, battle.c, battle_event.c, battle_magic.c and version/char_base/battle/event/pet_skillinfo headers. Header compilation resolves command 2022/2022/2021, WEAKEN index 7 vs work 51/51/47 and source skill macro 544.
- Supports command-only callback setup, direct COM2 dispatch, two-byte marker/sequential sizeof/sscanf parsing with initialized turn=3, shared MultiList/status RNG/turn+1 including PET, FALSE executor return, no direct work-power mutation and StatusSeq decrement/self/mutual-freeze boundaries.
- Boundaries: Bismarck's pointer/literal guard does not protect NULL; extended gavin/iris marker arrays are shorter than status END, so arbitrary scans remain unsafe. Leading WEAKEN marker only is admitted, with explicit encoding and no extra Lua resistance.
- Reproducible audit: tools/stoneage_weaken_source_audit.py; derived report: research/recovered/STONEAGE-WEAKEN-SOURCE-AUDIT-R1.txt; spec: research/mechanics/STONEAGE-WEAKEN-R1.md. Actual source compiles transiently under UBSan/ASan: 24 callback/executor + 1536 probability/writer cases PASS, injected RAND witness and a single resolved target. Local 124 tests PASS.
- Recovered IDs 575/576 and OPTION metadata require a separate verified preservation-bundle probe; typed ordered-runtime acceptance remains OPEN. No raw source/data/assets committed.


- Weaken expanded seam audit — 2026-10-04: additionally hashes char/char.c and item/item.c and compiles actual Other_DefcharWorkInt. Explicit compliance rebuilds base/equipment before fixed strength/toughness/dexterity * 0.8, decrements positive WEAKEN/BARRIER and copies attack/defense/quick. 384 additional UBSan/ASan native recalculation witnesses PASS; local acceptance 126 tests. This qualifies the preceding callback-only no-power-mutation observation; actual compliance caller scheduling remains OPEN for runtime admission.


- Weaken verified data update — 2026-10-04: expanded reference 37179176714 and source/hash-verified preservation workflow 37179176709 PASS at `d3f1ce58852bcf30fa39974f8a6f3a4340cfddea`; bot report `b78c9fdec393bac5baf513f9eb2e2a17916834a6`. ID 575 FIELD/TARGET/COST/ILLEGAL=1/6/2/3000; ID 576=1/3/2/0. Both 15-byte OPTION hashes `f58b7a4fdfc76fcefd2eca1a688b46a04c3c3e1a4516fc4a1364436f58d4fed6`, CP950/Big5 status 7, turn 3, success 50. Population 7 uses/6 templates. Runtime remains OPEN.
- Weaken schedule closure — 2026-10-04: fresh source gates trace BATTLE_Init and completed BATTLE_Command through BATTLE_PreCommandSeq; compliance occurs before BATTLE_TurnParam and excludes current EARTHROUND0 entries. Normal next-command preparation therefore supplies the counter decrement and new fixed powers distinct from StatusSeq freezing. Local 127-test reference acceptance includes an explicit multi-round composition; final remote scheduling gates pending.


- Weaken final source/data acceptance — 2026-10-04: final reference 37179420593 and source/hash-verified preservation probe 37179420582 PASS at `4a626dbd148d4bcda6665314fcb9b6f9b7b9df90`; 127 reference/regression tests and 24+1536+384 transient UBSan/ASan witnesses PASS. Source scheduling and both exact data rows are closed in the declared safe domain. Typed persistent runtime remains OPEN; the newly audited preparation-stage WEAKEN/BARRIER decrement must be integrated separately from StatusSeq self-freeze before runtime acceptance.


- Weaken runtime implementation update — 2026-10-04: exact two-row/hash typed bridge, existing late-status overlay extension, source-ordered status visits and once-only post-round preparation are connected through the persistent coordinator. Local 1074 tests/109 affected modules PASS, including 24 dedicated tests and four-round coordinator expiry/restoration. Production hash acceptance on seven real-data selected slots is added to the verified bundle probe; synthetic witnesses use an explicitly substituted independent fixture hash. Runtime/real-data Actions remain pending. Original source/data/assets and recovered numeric COM1 are not committed or inferred. Riding/drunk/overlapping callback-power extensions stay fail-closed.


- Weaken runtime acceptance — 2026-10-04: source `b57dcc2adc4ecefdd526cbce3e9d63ad9c8b9506` has all 22 affected Actions PASS, including dedicated 37190143523, real source/bundle/typed-admission 37190143464, coordinator 37190143380, full region 37190143397 and golden 37190143478. Real gate admits seven authoritative uses; report commit `32a80d6164e201a8f784db1374dd0cbc4c742a39`. Local 1074 tests/109 modules include 24 dedicated runtime tests and four-round persistence. Runtime CLOSED in explicit no-extra-modifier domain, including preparation-stage WEAKEN/BARRIER decrement and distinct power snapshots. Coverage 2415/2486; historical enum/date/Taiwan-v1 membership and unsupported riding/drunk/power-override domains remain OPEN.


- Post-Weaken pressure refresh — 2026-10-04: hash-verified preservation workflow 37190672044 PASS at `38c26913525394074291c6a7635697cb7992576b`, report write-back `68eb92975bf0504083c7d91ff2bcb15f5f18b52d`. Derived pressure report marks Weaken CLOSED, total 2486/unresolved 0, accepted 2415 uses, and selects exact WildViolentAttack (positively referenced ID 541, seven uses/seven templates). This ranks the next audit; it does not establish complete callback population, skill semantics, introduction date, Taiwan-v1 membership or recovered binary enum. WildViolentAttack source/data/runtime gates remain OPEN.


## 2026-10-04 — WildViolentAttack conditional audit

- **LATER_RECOVERED:** Clean pinned gavin `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`, iriselia `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`, Bismarck `999ffdf1d220ec6666eb65339180689c9caf1876`. Audit hashes pet_skill.c, battle.c, battle_event.c, battle.h, pet_skillinfo.h and version.h; compiles actual command headers and transient callback/macros/count/division fragments with UBSan under UTF-8 and explicit CP950 execution charsets. The latter is a conditional test build, not original binary provenance.
- Own reference `tools/stoneage_wildviolent_model.py`, audit `tools/stoneage_wildviolent_source_audit.py`, full-family derived probe `tools/stoneage_recovered25_wildviolent_probe.py`; dedicated reference and hash-verified preservation-bundle workflows. The probe enumerates unreferenced rows, keeps full metadata/hash and conditional derived values, and preserves undefined HIGH-domain findings. No raw source, OPTION records or assets are stored. Original charset and runtime remain OPEN pending evidence/acceptance; see the R1 reference spec and latest CURRENT-STATE record.


### 2026-10-04 — WildViolentAttack real-data evidence

Initial Actions 37192280495 (reference) and 37192280455 (source/hash-verified bundle) PASS; derived bot commit `3e9fdb42a46122f7826be4bad8ca1e53698bc244`. Reports: `research/recovered/STONEAGE-WILDVIOLENT-SOURCE-AUDIT-R1.txt` and `research/recovered/STONEAGE-25-WILDVIOLENT-PROBE-R1.txt`. Entire petskill file SHA-256 `f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4`; OPTION hashes for IDs 541/652 are `f63637633ee0e144f8807548d25f51b72f654756f1ec7858e40be0a5f796cb2c` / `9f1b961b626838f19d00f234527f3fd99ca86883befe4204cbdf33ef9bc783b1`. Both conditional parsers converge with defined HIGH shifts. Hardened probe adds exact observed full population, full-file hash and transient actual callbacks against real bytes; original charset and executable runtime remain separately OPEN.


### 2026-10-04 — WildViolentAttack final conditional source/data acceptance

Hardened reference **37192609926 PASS** and pinned-source/full-file/hash-verified preservation/real-byte native **37192610005 PASS**, source commit `e460037c0214fa795efa8c1e041a8a676eb0bb0b`, derived report `ae9bfa7a4596925e49d82731e1528e7a830cf6cb`. Reports preserve the exact two-row/full-file hashes above, 964 generic callback / 6672 float-division / 192 plan witnesses and six expected UB diagnostics; data probe adds 60 actual-byte callback witnesses. Runtime remains OPEN and compiler execution charset remains explicitly unknown. This supersedes prior expanded-native pending status; raw source/OPTION/assets remain outside the repository.


### 2026-10-04 — WildViolentAttack runtime verification supplement

Existing pinned source/data evidence feeds the separately typed conditional CP950 enemy runtime. Dedicated runtime fixtures exercise production metadata/population/parser/slot gates with independent hashes, source-ordered physical/status/reaction/ride/counter seams and Weaken preparation restoration. Coordinator E2E retains the production submission resolver. Local 1123 affected tests PASS; latest runtime/real-bundle Actions remain pending. Original compiler charset and Taiwan-v1 historical membership remain OPEN. See `specs/STONEAGE-WILDVIOLENT-RUNTIME-R1.md` and current-state handoff.


### 2026-10-04 — WildViolentAttack conditional runtime accepted

Corrected source `b60bc052f82f8f0e241762e9f97c44d479bdf3b2` passes all 21 triggered Actions: dedicated 37209088767, real verified data/seven authoritative selection gates 37209088658, full coordinator 37209088790, golden 37209088681 and full region/resource/collision stack 37209088684. Local 1123 affected tests include 24 dedicated witnesses and production-path two-round E2E, with compliance-prepared fixed powers and strict per-hit RNG ownership. Runtime is CLOSED only in the declared conditional CP950 enemy/opposite-side/FIST baseline domain. Original compiler charset, historical numeric COM1 and Taiwan-v1 membership remain OPEN. Raw source/OPTION/assets remain external.


### 2026-10-04 — WildViolentAttack main acceptance and pressure refresh

Main integration `d44e873a380208d192f458659cfcffb0e2d0763c` passes all 24 affected Actions, including dedicated 37209543841, verified source/data/seven-slot/60-native-byte witness probe 37209543750 and full region/resource/collision stack 37209543784. Verified pressure 37209543865 PASS produces report commit `dc51d2f7a5b4bd05d936343502b41316b4342ca9`: total 2486, unresolved 0, accepted 2422 within declared domains, next OPEN exact PETSKILL_Refresh (positive IDs 583/592; six uses/six templates). This selects the next audit; it does not establish full Refresh population or semantics. Original compiler charset and Taiwan-v1 historical membership remain OPEN.


### SRC-DESCENDANT-REFRESH-PINNED-PROFILES-R1

- Date: 2026-10-04. Fixed sources: gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56; iriselia/StoneAge@9e6c8ce2cd8ed532a7157773acd1c61582c178b5; BismarckDD/stoneage@999ffdf1d220ec6666eb65339180689c9caf1876. LATER_RECOVERED, not original binary build or Taiwan-v1 introduction evidence.
- Fresh audit covers pet_skill.c, battle_event.c, battle_magic.c, battle.c, char_base.c plus version/battle/char_base/pet_skillinfo headers. Derived hashes and actual compiled command 2032/2032/2030/source macro575; status END44/44/12, labels32/32/12, CONFUSION work50/50/46. Work-getter invalid element returns -1.
- Own reference and transient actual-function ASan/UBSan audit prove callback/direct dispatch, two-byte scan, actor-dependent return/effect, highest-positive-target status, wrong-namespace wildcard bound, single clear and silence NC/event semantics in a resolved-list domain. Local 9083 defined native witnesses, seven NULL and five short-table expected diagnostics. CP950 compilation only admits the whole iris table; all three support conditional UTF-8/GBK experiments.
- Source model/audit/probe: tools/stoneage_refresh_model.py, tools/stoneage_refresh_source_audit.py, tools/stoneage_recovered25_refresh_probe.py; spec specs/STONEAGE-REFRESH-REFERENCE-R1.md. Dedicated remote reference and hash-verified recovered family gates pending. Full callback population and real OPTION observations must be hardened after actual verified enumeration.
- OPEN: original charset, numeric recovered command, earliest historical membership, live MultiList/dead-target retarget RNG, typed ordered persistent runtime. Accepted pressure classification remains unchanged; no raw source/OPTION/assets are committed.


### 2026-10-04 — Refresh verified source/data acceptance

- Source commit: `ad4b2e0f2e92594eb71cea63b8a5d330ac45254e`; reference Action **37211584308 PASS**; verified preservation/full-family probe Action **37211584354 PASS**; derived report `fc7dfbdb00ca900716e6799794929bd8ef7a74ad`.
- Exact callback population: **583, 584, 591, 592, 593**; positive uses **583=4, 592=2**, others zero. All rows are FIELD=1/COST=2; TARGET=2 for 583/584/592/593 and TARGET=1 for 591. Row-specific ILLEGAL and OPTION SHA-256 values are preserved in `research/recovered/STONEAGE-25-REFRESH-PROBE-R1.txt` without storing raw proprietary rows.
- Conditional iris CP950/Big5 parsed statuses are **10/8/9/0/7**. The source/data evidence closes only a conditional descendant-reference interpretation; the original recovered binary execution charset and historical membership remain OPEN.
- Full petskill hash: `f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4`. Native recovered-byte report records 135 defined witnesses and expected unsafe-build diagnostics. Ordered runtime remains a separate acceptance gate.


### 2026-10-04 — Refresh conditional runtime acceptance

- Runtime source path accepted through `a1d7a884e2a18863348aab07bf9958b6df3af227`; all 17 affected workflows PASS, including dedicated Refresh **37213319829**, coordinator **37213319916**, golden **37213319930** and full recovered region/resource/runtime/collision **37213319811**. Actor-dependent source return/effect supplement **37213476518 PASS**.
- Pressure-classification source `8a21f0a3aa3bbfed1289d577d2a20e43b99787cc` passes dedicated Refresh **37213544347** and verified pressure **37213544358**; report write-back `13faa957cb645c4ccfacbdd3c0d77ac3ae2eae55` marks exact Refresh CLOSED_RUNTIME and selects SetMagicPet next.
- Accepted runtime is bounded to the verified recovered enemy uses and conditional iris CP950 status interpretation. It preserves symbolic command identity, explicit dead-single retarget RNG only, single-highest status clearing, Nocast NC restoration and persistent next-round behavior. Original binary charset, numeric recovered COM1, Taiwan-v1 membership and unmodeled extension statuses remain OPEN.


### SRC-DESCENDANT-SETMAGICPET-PINNED-PROFILES-R1

- Audit date **2026-10-04**. Sources: gavin `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`, iris `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`, Bismarck `999ffdf1d220ec6666eb65339180689c9caf1876`. Type: pinned later descendant source; not original binary/Taiwan-v1 provenance.
- Command enum values **2035/2035/2033**; source skill macro **601** in all profiles. Callback has inert nominal three-use count, direct COM2/LOW dispatch, and no OPTION parsing. Executor parses three pipe fields and branches HP before mutually exclusive STR/TGH/DEX target work state.
- BATTLE_StatusSeq decrements the three stat turn counters. `Other_DefcharWorkInt` uses one saved pre-suit fixed-toughness `mtgh` basis for STR/TGH/DEX percentage increments. This source quirk is part of the reference. Bismarck's NULL guard is defective, so NULL is outside the safe domain.
- Reproducible artifacts: `tools/stoneage_setmagicpet_model.py`, `tools/stoneage_setmagicpet_source_audit.py`, `tools/stoneage_recovered25_setmagicpet_probe.py`, spec `specs/STONEAGE-SETMAGICPET-REFERENCE-R1.md`. Reference **37215723983 PASS**, verified bundle **37215724000 PASS**, derived report `283ff86f6b008453b4f03e7f22b017625c084002`.
- Recovered family **601–604** all FIELD=1/TARGET=2/COST=2/ILLEGAL=2500. Parsed actual OPTIONS: 601 TGH 3/15 (6 uses), 602 HP 3/3000, 603 STR 3/10, 604 DEX 3/15 (latter three unreferenced). Immutable OPTION hashes are recorded in the derived probe without raw rows.
- **CLOSED:** bounded source reference, exact population, exact metadata/hash and recognized three-field OPTION domain. **OPEN:** ordered persistent runtime, original compiler/binary identity, earliest historical membership, and unneeded unreferenced family execution.


### 2026-10-05 — SetMagicPet ordered runtime acceptance supplement

- Typed runtime files: `tools/stoneage_enemy_ai_setmagicpet_bridge.py`, `tools/stoneage_setmagicpet_runtime_state.py`, battle round/state and local coordinator integration, with spec `specs/STONEAGE-SETMAGICPET-RUNTIME-R1.md`.
- Runtime admits only positive recovered ID **601** and rechecks the exact 601–604 family metadata/OPTION hashes before submission. ATTACK is an internal scheduling carrier only; source command identity stays symbolic.
- ID 601 target state is TGH 3/15. MultiList dead-single retarget RNG is explicit; live targets consume none. SetDuck/STR/TGH/DEX mutual exclusion, same-round StatusSeq decrement, persistent expiry, baseline-toughness preparation and SetMagicPet-before-Weaken ordering are tested. Unreferenced HP/STR/DEX family execution remains outside R1.
- Accepted code gate: `234cfb200ccff06bd97cb29009f81c7406e8f373` with SetMagicPet **37217333303 PASS**, coordinator **37217333081 PASS**, full region/runtime stack **37217333016 PASS** plus all affected battle regressions; supplement `8b1cb0fd49f2708eecfe08b67bc97301fbf7e14f` has **37217473190 PASS**.
- **CLOSED:** bounded ID-601 TGH enemy ordered runtime. **OPEN:** pressure-report regeneration (Action 37217793085 queued), unreferenced 602/603/604 execution, original numeric COM1/binary provenance and Taiwan-v1 membership.


### 2026-10-05 — SetMagicPet verified pressure closure

- Pressure fixture corrections only: `ef5f66af8e12467d486048b5d1e04a803b495321` updates the post-Refresh expectation after SetMagicPet closure; `05c6fec3ef27ef5b06acefc19a87712ede3a3348` adds BattleTimid ID 606 to the synthetic next-open fixture. Neither changes the production pressure classifier or runtime.
- Verified pressure Action **37218864011 PASS**: ranking tests, preservation-bundle recovery, real callback ranking and derived report write-back all succeed.
- Derived report commit: `ec46a0248e6c64623096d03c14e5ffc156a1193c`; report path `research/recovered/STONEAGE-25-PETSKILL-PRESSURE-R1.txt`; **2486 positive uses / 0 unresolved IDs**.
- Exact `PETSKILL_SetMagicPet` ID 601 is now `closed_runtime` for **6 uses / 6 templates**. Accepted executable positive-slot coverage is **2434/2486 = 97.91%**.
- Next mechanically selected OPEN callback is `PETSKILL_BattleTimid`, recovered ID **606**, **5 uses / 5 templates**. Any existing BattleTimid notes are pre-audit observations only until fresh pinned-source and verified recovered-data gates close.
