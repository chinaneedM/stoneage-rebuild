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


### 2026-10-05 — BattleTimid fixed-source + recovered25 exact-row closure

- Fixed descendants: gavin `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`, iris `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`, Bismarck `999ffdf1d220ec6666eb65339180689c9caf1876`.
- Reproducible source report: `research/recovered/STONEAGE-BATTLETIMID-SOURCE-AUDIT-R1.txt`; resolution `BATTLETIMID_FIXED_SOURCE_CLOSED_OPPOSITE_SIDE_REFERENCE`.
- Hash-verified recovered25 report: `research/recovered/STONEAGE-25-BATTLETIMID-PROBE-R1.txt`; `petskill` SHA-256 `f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4`.
- Exact callback population: `PETSKILL_BattleTimid` ID **606** only; **5 slot uses / 5 templates**. Exact metadata: FIELD 1, TARGET 6, COST 2, ILLEGAL 3000; OPTION length 0; OPTION SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Exact-pin Action **37220370536 PASS**; derived-report write-back commit `3f49cb44c7e836eb89a249b6d293d7acbc9e79a4`.
- Accepted descendant behavior: callback rejects player actor; writes semantic TIMID command/target/C_OK and LOW(COM3); work powers are 70%/40%/80%; event consumes one raw rand%100 draw; forced exit iff draw<15 and damage>1; pet exit clears default pet while non-pet exit discharges party.
- Boundaries retained: gavin/iris same-side guard active vs fixed Bismarck inactive; gavin/iris NULL OPTION guard vs Bismarck pointer-literal guard; no original numeric COM1/binary/compiler or Taiwan-v1 proof.


### 2026-10-05 — Combined fixed-source + recovered25 exact-row closure

- Fixed later descendants: gavin `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`, iris `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`, Bismarck `999ffdf1d220ec6666eb65339180689c9caf1876`. These are descendant-reference sources, not proof of original JSS/Taiwan-v1 introduction.
- Reproducible source report: `research/recovered/STONEAGE-COMBINED-SOURCE-AUDIT-R1.txt`; resolution `COMBINED_FIXED_SOURCE_CLOSED_WELLFORMED_OPTION_REFERENCE`. Shared bounded facts: command value 2000, declared OPTION count clamp to 10, one raw `rand()%effective_count` draw, selected magic in LOW(COM3), HIGH(COM3)=0, and `MAGIC_DirectUse` dispatch.
- Preserved source divergences: gavin/iris NULL OPTION guard vs Bismarck pointer-literal NUL guard; gavin/iris uninitialized count/kill declaration vs Bismarck zero-initialized count; gavin/iris Combined initiative `WORKQUICK+20-RAND(0,work*0.3)` vs Bismarck `WORKQUICK+20-RAND(0,15)`.
- First corrected bundle gate **37262695753 PASS**; exact-pin gate **37262850204 PASS**. Derived exact report commit `8252a51966450a0b5b515d051e52b3c84d61ae65`; report `research/recovered/STONEAGE-25-COMBINED-PROBE-R1.txt`; full `petskill` SHA-256 `f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4`.
- Exact callback population is **627, 629, 630, 632, 637, 646, 648**. Positive references are only **627=1, 632=2, 637=2**, totaling **5 uses / 5 templates**; 629/630/646/648 are zero-reference data-only rows. All seven OPTION structures are well formed in the verified corpus and all exact row metadata/hashes/counts/magic-ID lists are pinned without storing raw OPTION bytes.
- **CLOSED:** bounded fixed-descendant source reference plus recovered25 full population and exact-row evidence in the well-formed OPTION domain. **OPEN:** ordered runtime, malformed OPTION behavior, original binary/compiler identity, original command-number provenance and earliest historical membership.


### SRC-COMBINED-DIRECT-MAGIC-ITEM-MP-R1 — 2026-10-05

- Fixed descendant pins: gavin `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`, iris `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`, Bismarck `999ffdf1d220ec6666eb65339180689c9caf1876`. Sources are clean pinned trees recovered outside the project; no original source is committed.
- Reproducer: `tools/stoneage_combined_direct_magic_source_audit.py`; derived report: `research/recovered/STONEAGE-COMBINED-DIRECT-MAGIC-AUDIT-R1.txt`; independent reference model: `tools/stoneage_combined_direct_magic_model.py`; boundary spec: `specs/STONEAGE-COMBINED-DIRECT-MAGIC-BOUNDARY-R1.md`.
- Existing verified data supplement: selected-magic exact rows, Action **37263769848 PASS**, report commit `796e31d88d6d0256bb70366ac7ee9ef2e42b6abb`; all 19 choices bind against full magic hash `b3a57b595bd60dfab571fe7af4dd6e2d43a5839c934eb644ba462897b1bcb6bb`. Only the 8 choices of positively referenced 627/632/637 are runtime candidates.
- Native boundary: original ITEM integer getter, DirectUse and Recovery/StatusChange/StatusRecovery/AttReverse wrappers; **4800 local ASan/UBSan witnesses PASS** under preprocessed profile macros, with explicit non-player/no-family/live-battle and stubbed effect seams.
- Accepted local facts: HIGH zero means runtime item index zero, invalid item getter returns -1, ordinary wrappers compare/subtract the forwarded MP, selection precedes Nocast, Recovery discards battle-helper failure. New remote source gate is pending at this record.
- **OPEN:** actual live item-pool state, status OPTION charset/safe scans, ordered mutations/persistence, family modifiers, original compiler/binary and earliest historical membership. Conditional item-state reference closure does not close Combined runtime or advance pressure coverage.


### SRC-COMBINED-DIRECT-MAGIC-ITEM-MP-R1 — remote acceptance supplement

- Input commit `97fb9e5ca78a007f383024b7edc935fd997077e0`, tree `8acf0205a1dc1cef70c5e2984e0309fccddefbfe`.
- **37265053597 PASS**: 36 unit tests; fixed three-source recovery; all 4800 actual-accessor/DirectUse/wrapper witnesses under ASan/UBSan; exact report reproduction.
- **37265053470 PASS**: verified preservation bundle, 19 exact magic rows, eight positive selection choices and unknown/invalid/Nocast item-state checks.
- Conditional direct-wrapper MP/return reference is now remotely accepted. Stubbed battle effects and explicit item-state witnesses remain declared limitations; ordered runtime and pressure closure remain OPEN.


### SRC-COMBINED-ORDINARY-STATUS-MAGIC-BYTE-PARSERS-R1 — 2026-10-05

- Fixed pins: gavin `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`, iris `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`, Bismarck `999ffdf1d220ec6666eb65339180689c9caf1876`; clean sources stay outside the reconstruction repository.
- Source model/audit: `tools/stoneage_combined_status_magic_model.py`, `tools/stoneage_combined_status_magic_source_audit.py`; boundary spec: `specs/STONEAGE-COMBINED-STATUS-MAGIC-REFERENCE-R1.md`. Source hashes, enum/table counts, marker identities and parser cursor/default behavior are checked. Only original parsers/labels are transiently compiled; downstream multi-effect calls are collector seams.
- First actual-byte Action **37266411923 PASS** at `463cc02c2c2fa3087c39548c9c2517cf6de5cfd6`; report `7f50e1ae836485f2c46a5b2bc16e5a4cc2db9362`. Exact-matrix Action **37266742566 PASS** at `4c9974a1b569d08ac1d9b71d4d38c359fd0601c8`; report `93cada6a5de092018391a837c80cd1c55e1839c3`, tree `79de70c9cdb1cd3fad0d0e268660e04a173d1d52`. Both recover the verified bundle and exact magic table before actual-byte native witnesses.
- Source-only 747 defined comparisons / 38 expected ASan/UBSan diagnostics; with real rows 765 / 62. **51 unit tests PASS**. Outcome matrix: 24 unsafe cells, 12 safe FALSE/no-effect cells, six defined iris CP950 dispatches.
- iris CP950 accepted numeric outputs: ID61 wildcard status0; IDs139/159/169/179/189 status1/4/6/5/3, turn5, success offset15. No final chance, actor/target mutation or original build provenance follows from those parser values.
- **CLOSED:** explicit conditional parser and exact 42-cell actual-data outcome reference. **OPEN:** initiative, target/effect RNG and mutation, MP item-pool witness, command/persistence ordering and earliest historical membership. Pressure/ordered runtime remains open.

### SRC-VARY-REFERENCE-RUNTIME-R1 — 2026-10-05

- Fixed descendant pins: gavin `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`, iris `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`, Bismarck `999ffdf1d220ec6666eb65339180689c9caf1876`. They are later-descendant reference sources, not proof of original JSS/Taiwan-v1 introduction.
- Reference outputs: `specs/STONEAGE-VARY-REFERENCE-R1.md`, `research/recovered/STONEAGE-VARY-SOURCE-AUDIT-R1.txt`, `research/recovered/STONEAGE-25-VARY-PROBE-R1.txt`. Exact recovered25 population is ID 600 only, four positive PETSKILL3 uses on TEMPNO 981/982/983/984.
- Executable-profile discriminator: `tools/stoneage_vary_executable_profile_probe.py`, derived report `research/recovered/STONEAGE-25-VARY-EXECUTABLE-PROFILE-R1.txt`, Action **37282101502 PASS**. Bounded result: one 273-byte ELF candidate, no Vary symbol carrier, profile classification **inconclusive_symbol_unavailable**.
- Runtime boundary: `specs/STONEAGE-VARY-RUNTIME-R1.md`; implementation preserves explicit gavin/iris versus Bismarck work-power/visual divergence, ordinary QUICK ordering, semantic no-damage Vary action, six-action persistence and active recast block.
- Acceptance: dedicated Vary **37286463853 PASS**; local coordinator **37286420982 PASS**; runtime golden **37286013147 PASS**; recovered25 full-region **37286420991 PASS**; verified pressure **37286756850 PASS**.
- Pressure outcome: exact Vary = `closed_runtime`, **4 uses / 4 templates**, **2448/2486 = 98.47%** executable positive-slot coverage; next OPEN = **ENEMYSKILL_ReLife / ID500 / 3 uses / 3 templates**.
- **OPEN:** original executable/compiler/profile/charset identity, original numeric Vary COM1, original JSS/Taiwan-v1 membership and excluded cross-system work-power compositions.

### SRC-RELIFE-REFERENCE-R1 — 2026-10-05

- Fixed descendant pins: gavin `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`, iris `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`, Bismarck `999ffdf1d220ec6666eb65339180689c9caf1876`; later-descendant evidence only.
- Reproducer: `tools/stoneage_relife_source_audit.py`; recovered data probe: `tools/stoneage_recovered25_relife_probe.py`; reports `research/recovered/STONEAGE-RELIFE-SOURCE-AUDIT-R1.txt` and `research/recovered/STONEAGE-25-RELIFE-PROBE-R1.txt`; spec `specs/STONEAGE-RELIFE-REFERENCE-R1.md`.
- Exact recovered25 row: ID500 / FIELD1 / TARGET2 / COST2 / ILLEGAL0 / empty OPTION SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; three positive refs on TEMPNO 39 slot5, 909 slot2, 1165 slot4.
- Source facts: callback sets symbolic ENEMYRELIFE command/COM2/C_OK; dispatcher TargetAdjust precedes effect; enemy helper scans slots 10..19 for non-ultimate actionable dead entries; no candidate falls back to physical ATTACK; success owns candidate-selection RNG plus nonzero resurrection-amount RNG; HP is capped and ISDIE cleared.
- Guarded numeric command: gavin/iris **2013**, Bismarck **2012**. No recovered-original numeric command is selected.
- Acceptance: **37288674220 PASS** first pass; **37288913119 PASS** exact row/template pin.
- **OPEN:** original binary/compiler/profile, original numeric COM1, JSS/Taiwan-v1 membership, and runtime dead-entry/coordinator carrier integration.

### SRC-RELIFE-ORDERED-RUNTIME-R1 — 2026-10-05

- Runtime boundary: `specs/STONEAGE-RELIFE-RUNTIME-R1.md`; implementation files include `tools/stoneage_enemy_relife_model.py`, `tools/stoneage_enemy_ai_relife_bridge.py`, shared ordered battle/state models and the local runtime coordinator.
- Exact positive recovered admission remains ID500 / FIELD1 / TARGET2 / COST2 / ILLEGAL0 / empty OPTION, with TEMPNO/graphic/slot identities **39/100370/5**, **909/100071/2**, **1165/101814/4**. Admission rechecks exact template graphic as well as slot/row identity.
- The original numeric ENEMYRELIFE command remains unknown because later descendants disagree (**2013 gavin/iris, 2012 Bismarck**). Runtime uses a typed symbolic submission and ATTACK only as a modern scheduling/COM2/fallback carrier.
- Accepted semantics: prior ordinary TargetAdjust; independent enemy-side dead scan 10..19; one reduced candidate draw; WORKMAXHP/2 base; nonzero 90–110% amount draw; capped HP/death clear; no-dead physical fallback using the same adjusted target and no second retarget draw.
- Persistent state retains only ordinary-dead **enemy-side** battle entries as ReLife candidates. Dead entries do not participate in initiative; successful revival can affect later same-round targeting and restores next-round command participation. Ultimate/BATTLE_Exit entries are excluded. Already-settled death profit is not reversed.
- Acceptance: ReLife **37293702272 PASS**, battle core **37293114252**, coordinator **37293114108**, golden **37293113921**, full region **37293113718**. Verified pressure **37293804945 PASS**, report write-back `420e34a7a29aa06a37ea45e55369afd1b01a80fd`.
- Pressure outcome: ReLife `closed_runtime`, **3 uses / 3 templates**, coverage **2451/2486 = 98.59%**, unresolved positive IDs **0**; next OPEN **PETSKILL_Lighttakeed IDs610/611, 3 uses / 2 templates**.
- **OPEN:** recovered-original binary/compiler/profile, original numeric COM1, JSS/Taiwan-v1 membership, pet-caster and PvP/rescue domains, exact libc PRNG state and unmodeled expansion death-entry interactions.



### SRC-LIGHTTAKEED-REFERENCE-R1

- Date: 2026-10-05. **LATER_RECOVERED + RECOVERED25 DERIVED**, not original JSS/Taiwan-v1 source or executable provenance.
- Fixed descendants: gavinlinasd/StoneAge@`1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`; iriselia/StoneAge@`9e6c8ce2cd8ed532a7157773acd1c61582c178b5`; BismarckDD/stoneage@`999ffdf1d220ec6666eb65339180689c9caf1876`.
- Reproducible source audit closes registration/callback/dispatch/reaction-marker facts: fixed STR*0.7, fixed TOUGH*0.5, no callback OPTION/RNG, TargetAdjust before AttackDamage, VANISH/ABSROB/REFLEC match neutralization. Descendant command value is 2009 and C_OK is 3 in all three pins, but original numeric COM1 remains OPEN under DD-019.
- Material divergence is retained: gavin/iris assign the defender's matching damage-reaction work counter unchanged to the attacker; fixed Bismarck assigns observed value +1. No recovered-original profile is inferred.
- Hash-verified recovered25 petskill SHA-256 `f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4`. Complete callback population = IDs **609/610/611**; all FIELD/TARGET/COST/ILLEGAL = **1/7/2/5000**, six-byte non-NUL OPTIONs. Derived marker/hash identities: 609 ABSROB / `28e420f6e618020e7fdba9f49433a94c5f88cbd6edba2d521104f880b416c5e7` / zero positive refs; 610 REFLEC / `73bef6383b8b2e301ef6860a573f7b7d703c651aa3e90df3e1efe6f1b28fce01` / two refs; 611 VANISH / `a715b2ee62e500775e7eca86facd327f5cdc6501f4064dd322f8fc6e1ddbf96b` / one ref.
- Exact positive templates: TEMPNO 70 / graphic 101550 / slot4 -> 610; TEMPNO 157 / graphic 101283 / slots4,5 -> 610,611. Pressure's earlier IDs 610/611 were therefore positive-reference selection, not the complete callback population.
- Acceptance: workflow **37295790110 attempt 2 PASS**; derived report commit `0d002434a5b86e20505ff8b8fd431b3075374c84`. Reports: `research/recovered/STONEAGE-LIGHTTAKEED-SOURCE-AUDIT-R1.txt`, `research/recovered/STONEAGE-25-LIGHTTAKEED-PROBE-R1.txt`; spec: `specs/STONEAGE-LIGHTTAKEED-REFERENCE-R1.md`.
- **LIGHTTAKEED_REFERENCE_R1 = CLOSED_BOUNDED_RECOVERED25_REFERENCE.** Ordered runtime and recovered-original copy-vs-copy+1 discriminator remain OPEN; pressure coverage stays **2451/2486 = 98.59%** until runtime acceptance.


### SRC-LIGHTTAKEED-ORDERED-RUNTIME-R1 — 2026-10-05

- Evidence role: fixed later descendants plus hash-verified recovered25 data, not original JSS/Taiwan-v1 provenance. Complete family609/610/611; executable positive domain610/611 only, three slots/two templates.
- Executable discriminator report: `research/recovered/STONEAGE-25-LIGHTTAKEED-EXECUTABLE-PROFILE-R1.txt`; one 273-byte ELF/no callback or AttackDamage symbols; copy profile remains inconclusive.
- Lifecycle report: `research/recovered/STONEAGE-LIGHTTAKEED-DAMAGEREACT-LIFECYCLE-R1.txt`; DamageSub re-fetch/consumption, reaction priority, reflection identity redirect, throwing bypass and zero-damage demotion. Sources retain the existing exact gavin/iris/Bismarck pins.
- Runtime boundary: `specs/STONEAGE-LIGHTTAKEED-RUNTIME-R1.md`; pure model, exact admission bridge, ordered battle, persistent state and coordinator. Typed identity hardening at `5bdedd571f2f369f3f196955581589e59eb283dd`; independent multi-round regression added at `15392c6b5d9470789fcdfa8d2bb1f5da69cd2094`.
- Acceptance: dedicated **37299772670**, multi-round **37299752226**, coordinator **37299249647**, golden **37299249686**, full-region **37299249771**, pressure **37299752243 PASS**; final local **258 tests PASS**.
- Derived pressure report commit `26afc10ee71572d09fffce2413ff13dc6c590e72`: Lighttakeed closed_runtime, three positive uses/two templates, zero unresolved positive IDs, coverage **2454/2486 = 98.71%**, next OPEN **PETSKILL_Modifyattack IDs544/545/546, three uses/three templates**.
- OPEN: original executable/compiler/profile, historical numeric COM1, JSS/Taiwan-v1 membership, exact libc PRNG identity and excluded drunk/Weaken/SetMagicPet compositions. ID609 is not promoted to executable enemy use.


### SRC-MODIFYATTACK-REFERENCE-R1 — 2026-10-05

- Evidence role: fixed later descendants and hash-verified recovered25 data; not original JSS/Taiwan-v1 source or executable provenance. gavin `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`, iris `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`, Bismarck `999ffdf1d220ec6666eb65339180689c9caf1876`.
- Reproducer: `tools/stoneage_modifyattack_source_audit.py`, independent bounded helper reference `tools/stoneage_modifyattack_reference_model.py`, and exact data probe `tools/stoneage_recovered25_modifyattack_probe.py`. Native source/functions stay transient; derived reports are `research/recovered/STONEAGE-MODIFYATTACK-SOURCE-AUDIT-R1.txt` and `research/recovered/STONEAGE-25-MODIFYATTACK-PROBE-R1.txt`.
- Complete family544..547, five-byte ASCII parameters/20% base; exact positive uses18/101543/slot4->546,19/101533/slot5->545,20/101532/slot4->544. Full petskill SHA-256 `f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4`; exact OPTION digests are pinned in the probe/spec.
- Discovery37301723985 PASS at dbf59975781649a85a6746747001dbc02835988c; report15e32851e837460a4f9e0032d2fef0e38ee3d78c. Final exact/native37302178741 PASS at6abb4cc17b3426fce0eea39204d2b40f87ddec7e; reporta696cb5f98812600d7a1c898bf400ebe8dc21909. Three profiles:20 callback/2660 helper cases each, all four actual OPTIONs each;32 unit tests PASS.
- Source semantics retain integer random-remainder division, raw defender attribute, pre-DamageSub mutation, reaction demotion, visual ATTDOUBLE and specialized-command counter rejection. Numeric command2029/2027 is descendant-only under DD-019. Null-pointer and undefined arithmetic domains remain outside the reference.
- **MODIFYATTACK_REFERENCE_R1=CLOSED_BOUNDED_RECOVERED25_REFERENCE**. Boundary: `specs/STONEAGE-MODIFYATTACK-REFERENCE-R1.md`. OPEN: ordered/persistent/coordinator runtime, original executable/profile/numeric command/libc PRNG, and original JSS/Taiwan-v1 membership. Pressure unchanged2454/2486=98.71%; do not confuse with Mdfyattack.


### SRC-MODIFYATTACK-ORDERED-RUNTIME-R1 — 2026-10-05

- Evidence role: bounded modern execution based on the accepted fixed-descendant/native reference plus hash-verified recovered25 data; not original JSS/Taiwan-v1 provenance. Existing gavin/iris/Bismarck pins and exact four-row hashes remain authoritative as recorded in SRC-MODIFYATTACK-REFERENCE-R1.
- Runtime: `tools/stoneage_enemy_ai_modifyattack_bridge.py`, shared ordered/state/coordinator seams, `tests/test_stoneage_modifyattack_runtime.py`, `tests/test_stoneage_modifyattack_persistent_runtime.py`, and `specs/STONEAGE-MODIFYATTACK-RUNTIME-R1.md`. Three exact positive template/graphic/slot identities admit IDs544/545/546. ID547 is population/data-only.
- Semantics: ordinary damage first, original-defender reaction demotion, positive matched raw-attribute helper RNG before DamageSub, integer remainder division and float32/int truncation; specialized Guardian settlement; visual ATTDOUBLE; no added hit/counter/combo; no cross-round semantic/power retention.
- Code `a985a4977d790e9706031f30b70bd5bc6362b044`, tree `5ca054ffbfe7d8c565428ae3c4a1d0e34867ef58`. Dedicated99-test **37305538911**, battle core **37305538909**, coordinator **37305538741**, golden **37305538906**, full-region **37305538863 PASS**; all29 relevant workflows PASS. Local450 related tests and golden CLI PASS; updated pressure11 tests PASS.
- Verified pressure **37306407247 PASS** at `7b017f6ca06a00faa22c96269486d95e467518aa`; derived report `a85f25e492402adceec35594936c0608f1295d52`. Closed three uses/three templates, zero unresolved positive IDs; accepted executable coverage **2457/2486 =98.83%**. Next OPEN: **PETSKILL_2BattleTimid / ID636 / 2 uses / 2 templates**.
- **RECOVERED25_MODIFYATTACK_ORDERED_RUNTIME_R1 = CLOSED_BOUNDED_RECOVERED25_ORDERED_RUNTIME.** Original numeric COM1/compiler/libc/PRNG/null-pointer domain/JSS-Taiwan-v1 membership remain OPEN. Whole-repository baseline failures and absent analysis dependencies are explicitly recorded in the runtime specification; they are not represented as a green whole-repository gate.


### SRC-2BATTLETIMID-CONDITIONAL-REFERENCE-R1 — 2026-10-05

- Evidence role: fixed later-descendant source plus hash-verified recovered25 data; not original JSS/Taiwan-v1 provenance. Pins: gavin `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`, iris `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`, Bismarck `999ffdf1d220ec6666eb65339180689c9caf1876`.
- Complete family636 only; exact FIELD/TARGET/COST/ILLEGAL1/7/2/10000. OPTION17 bytes, non-NUL/non-ASCII, SHA-256 `8e6b5dd952bf3bc81e522f1df382db48473b1aeec13f9ff08c7bb76d2c06f9e5`; full petskill SHA-256 `f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4`. Exact positive uses178/101872/slot3 and179/101873/slot3. Raw data/source remain transient.
- Reproducers: `tools/stoneage_recovered25_2battletimid_probe.py`, `tools/stoneage_2battletimid_reference_model.py`, `tools/stoneage_2battletimid_source_audit.py`. Derived reports: `research/recovered/STONEAGE-25-2BATTLETIMID-PROBE-R1.txt` and `research/recovered/STONEAGE-2BATTLETIMID-SOURCE-AUDIT-R1.txt`.
- Discovery37308193431 PASS; exact data/native37309960471 PASS at `bf02c6a38cbd1ea221aeee412e445e736f57d66f`; report `7255dc2e551ba800f6d892c0a44dda3d04dcb4c8`. Six profile/charset native comparisons include actual OPTION, totaling528 callback/53196 post-recall cases. Three profiles each pass19 source gates;32 related tests PASS.
- Actual byte semantics remain conditional: UTF-8 literal profile preserves incoming powers/chance0; Big5 literal profile derives attack50%, quick130%, chance60 and preserves defence. Fixed byte offsets and failed-scan float reuse are retained. Pet-only recall uses owner defNo-5; NORETURN blocks default exit/default mutation/BS but outer K/KS remain. Native PetDefaultExit is a collector stub, not a complete battle-lifecycle execution.
- **TWOBATTLETIMID_REFERENCE_R1=CLOSED_BOUNDED_RECOVERED25_REFERENCE**. Spec `specs/STONEAGE-2BATTLETIMID-REFERENCE-R1.md`. OPEN: ordered runtime, owner/default-pet lifecycle, transformations, original build/execution charset/numeric COM1/libc PRNG and JSS/Taiwan-v1 membership. Pressure unchanged2457/2486=98.83%.


### SRC-2BATTLETIMID-RECALL-STATE-AUDIT-R1 — 2026-10-05

- Same fixed gavin/iris/Bismarck pins as SRC-2BATTLETIMID-CONDITIONAL-REFERENCE-R1. Reproducer `tools/stoneage_2battletimid_recall_lifecycle_source_audit.py`;12 textual gates per profile close player-owner/default-slot lookup, delegation to BATTLE_Exit, matching-entry/escape/FINAL/battleindex mutation and NORETURN-before-exit/default-clear order. Full native server exit and excluded transform/error paths remain OPEN.
- Verified Action37311978479 PASS at `57babd06d8e53faefe59bd47179a8d20d941ee7e`; report commit `126a1362a9d76ce821a883cf47da3a79c96e9ef0`. Derived report `research/recovered/STONEAGE-2BATTLETIMID-RECALL-LIFECYCLE-SOURCE-R1.txt` pins battle/event hashes,36 gates and boundaries.
- Reproducer `tools/stoneage_2battletimid_executable_profile_probe.py`, report `research/recovered/STONEAGE-25-2BATTLETIMID-EXECUTABLE-PROFILE-R1.txt`: one273-byte ELF candidate, SHA-256 `22a786475540dd734e0b0dc1b21219e53aba1462de8be623270f71fa90c22365`; neither required symbol available. Bounded discriminator is inconclusive and does not select an original charset. Two discriminator tests PASS.
- Modern source-tree audit contract: `specs/STONEAGE-2BATTLETIMID-RUNTIME-STATE-AUDIT-R1.md`. Explicit owner/default/NORETURN state and later death/return semantics are still to be implemented. Reference/native profile acceptance remains37309960471 PASS; runtime and pressure unchanged2457/2486=98.83%.


### SRC-BATTLEMODEL-STATUS-PROFILES-R1 — 2026-10-06

- Type: fixed descendant source comparison; technical bridge evidence.
- Exact source commits: gavinlinasd/StoneAge
  `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`, iriselia/StoneAge
  `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`, BismarckDD/stoneage
  `999ffdf1d220ec6666eb65339180689c9caf1876`.
- Source path: each profile's `battle/battle_event.c`, `aszStatus` base prefix.
- Supports: the same base status indices have different literal spellings and
  lengths across descendants; BattleModel compares their first two bytes in
  source index order. Strict Big5 cannot encode some modern simplified
  descendant literals. Original compile charset remains unresolved.
- Reproduction: `tools/stoneage_battlemodel_source_audit.py` now gates each
  profile's exact base-table prefix; local three-profile PASS with 600 native
  target-plan vectors. Remote replacement acceptance remains pending.
- Does not support: original recovered25 compiler/source-table identity,
  JSS/Taiwan-v1 membership or BattleModel runtime completion.


### SRC-BATTLEMODEL-HIT-LIFECYCLE-R1 — 2026-10-06

- Type: transient native extraction of `BATTLE_BattleModel_ATTACK` from the
  same three pinned descendant commits as SRC-BATTLEMODEL-STATUS-PROFILES-R1.
- Reproduction: `tools/stoneage_battlemodel_hit_lifecycle_source_audit.py`.
  Local432 controlled helper vectors per profile,1296 total, PASS.
- Supports: actual-defender versus notification-Guardian distinctions;
  conditional DamageSub/wakeup/status call ordering; marker restoration;
  source DODGE pet-damage presentation initialisation gap.
- Does not support: complete common combat arithmetic, original executable
  membership, exact presentation bytes, or production runtime closure.
- Full boundaries: `specs/STONEAGE-BATTLEMODEL-HIT-LIFECYCLE-AUDIT-R1.md`.


### SRC-BATTLEMODEL-CONDITIONAL-REFERENCE-R1 — 2026-10-06

- Evidence role: hash-verified recovered25 later-data bridge and the same three
  fixed gavin/iris/Bismarck commits as SRC-BATTLEMODEL-STATUS-PROFILES-R1;
  not original JSS/Taiwan-v1 provenance.
- Exact-data37342593141 and three-profile source/native37342593073 SUCCESS
  on input4131a23ce12b4d03e367456f4135988e8e5121b9. Derived report commit
  fb8cabc13a05c8e4188d18fbf774567a20c1f019, tree
  76e56d3a9334ab0db35bfbc5885fb5756fede514.
- Helper37344060042 SUCCESS on be9de3df70d4a872817f55fd484e9a08f4dd1f31,
  job111878092333, artifact11360861465.600 planner/1296 controlled helper
  vectors total. This supersedes remote-pending status in the two source
  records above; common damage/status arithmetic remains stubbed.
- Complete population638/641/649/650; positive638 uses two slot3 identities
  1178/101867 and1179/101868. Full data and exact OPTION hashes, source/charset
  witnesses and placement metadata are in the derived probe/acceptance JSON.
- Contracts: STONEAGE-BATTLEMODEL-REFERENCE-R1.md, runtime-state audit and
  hit-lifecycle audit. Reference CLOSED_BOUNDED_RECOVERED25_CONDITIONAL_REFERENCE;
  state audit CLOSED_FOR_BOUNDED_RUNTIME_INTEGRATION. Explicit Big5 paralysis
  and attack70% versus UTF-8 unmatched-status/unchanged-power profiles remain.
- OPEN: original executable/source/charset/numeric COM1/libc PRNG, original
  qsort presentation, DODGE uninitialised bytes, excluded transformations and
  reactions, ordered runtime and original version membership. Coverage unchanged.


### SRC-BATTLEMODEL-BASE-SETTLEMENT-R1 — 2026-10-06

- Same three fixed pins and battle_event.c hashes as the accepted hit-helper
  audit. Original DamageSub body compiled transiently with reduced base feature
  profile, BattleModel marker gate, no ride, nonthrowing actor, defined state
  getters/setters and stubbed base reaction priority. No raw source committed.
- Reproducer: tools/stoneage_battlemodel_settlement_source_audit.py; derived
  report: research/recovered/STONEAGE-BATTLEMODEL-SETTLEMENT-SOURCE-AUDIT-R1.txt.
  Local640 native calls/profile,1920 total PASS; remote acceptance pending.
- Supports: marker reflect HP preservation, retained positive reported damage,
  reaction/counter priority and exhaustion, sentinel bypass, and raw-threshold
  ultimate2 without HP loss. Does not certify live target checks or complete
  ordered/persistent/coordinator behavior; direct function calls after death
  isolate DamageSub and are not asserted reachable helper calls.
- Correction: previous “damage remains on defender” interpretation is superseded
  by explicit both-HP preservation. Original absent-ride read, active build
  profile, rides/throwing/later gates and flag-to-exit integration remain OPEN.
- Boundary: specs/STONEAGE-BATTLEMODEL-SETTLEMENT-AUDIT-R1.md; prepared runtime
  plan: specs/STONEAGE-BATTLEMODEL-RUNTIME-INTEGRATION-PLAN-R1.md.


#### SRC-BATTLEMODEL-BASE-SETTLEMENT-R1 remote acceptance — 2026-10-06

-37349075552 SUCCESS, exact input33a8e76a988c441629e797defcc8095d77952e86,
 tree1cb9731ed51d82c58e1e8da753afcddbc0d78af1.1920 native calls reproduced.
 The earlier remote-pending entry is superseded; all reduced-profile/stub/no-ride
 and full runtime exclusions remain. Contract CLOSED_BOUNDED_NO_RIDE_NATIVE_SETTLEMENT.


### SRC-RUNTIME-ADMISSION-SLOT-BASE-20261006

- Kind: independently accepted recovered25 derived-data schema plus modern
  reconstruction regression; not an original-client historical source.
- Evidence: `tools/stoneage_recovered25_2battletimid_probe.py` exact rows and
  `research/recovered/STONEAGE-25-2BATTLETIMID-PROBE-R1.txt`; enemybase loader's
  seven-column tuple; corrected `tools/stoneage_enemy_ai_2battletimid_bridge.py`
  and two regression tests derived from the independent report indices.
- FACT: ID636 templates178/179 source column3 maps to runtime index2. Existing
  runtime/spec fixture column4 is erroneous and superseded, with history retained.
- BattleModel evidence: accepted four-row/template probe and report, strict
  bridge and `specs/STONEAGE-BATTLEMODEL-ADMISSION-R1.md`. Its verified-data
  admission probe checks global positive placements and two current-power
  witnesses across explicit descendant/charset profiles, plus corrected636.
- Local140 related and279 core/golden tests PASS; actual-data/regression remote
  acceptance pending publication. No new raw OPTION or proprietary assets are
  added by this milestone. Pure target-plan validation is not ordered runtime
  execution and does not certify original charset/build/JSS membership.


#### SRC-RUNTIME-ADMISSION-SLOT-BASE-20261006 remote acceptance

Exact input5c555bf781b2517d1709a246afd80bc875fb7980,
treefaf8c42007bbec39ea0994de920e033e417af7fa: all27 workflows SUCCESS.
Required actual-data/runtime/core/coordinator/golden/full-region gates:
37353001564 /37353001258 /37353002049 /37353000921 /37353001458 /
37353001229. Job111908266812 and write-back47d3a6a5 prove24 actual conditional
BattleModel admissions and4 corrected real636 admissions. Full petskill hash
and row/template/global placement identities verified. Earlier remote-pending
record superseded; complete BattleModel ordered runtime remains OPEN.


### SRC-BATTLEMODEL-POST-ATTACKSEQ-LOOP-R1

- Type: modern experimental loop implementation plus transient native
  fixed-descendant comparisons; no new original build/version membership.
- Three clean pins remain gavin1f90cb6c /iris9e6c8ce2 /bismarck999ffdf1.
  New pet-guard audit compiles the same original helper bodies/hash identities
  as the accepted helper lifecycle audit. Controlled SIDE_OFFSET10/shared
  stubs prove literal target+5 rather than ordinary owner target-5:60 local
  native cases. Multiplayer offset12 is excluded.
- Settlement audit opt-in `--verify-runtime-model` compares physical marker
  HP/charges/reported damage/ultimate against original native outputs:480
  local comparisons across three profiles; original1920 calls still PASS.
  Direct native calls after death remain function experiments, not reachable
  loop calls. Modern loop rechecks life and skips those actual helper calls.
- Evidence modules: `tools/stoneage_battlemodel_hit_loop.py`,
  `tools/stoneage_battlemodel_pet_guard_source_audit.py`, extended settlement
  source audit; spec `specs/STONEAGE-BATTLEMODEL-HIT-LOOP-R1.md`.
- Local81 tests PASS. Typed injected AttackSeq controls shared arithmetic/RNG;
  it is not production AttackSeq acceptance. No-ride/nonthrowing/no-ItemCrush/
  gDamageDiv0/reduced offset10 scope is mandatory. Equipment ItemCrush precedes
  status in source and remains required for full integration. Remote gate
  pending; ordinary round/state/coordinator/pressure execution unchanged.


#### SRC-BATTLEMODEL-POST-ATTACKSEQ-LOOP-R1 remote acceptance

37355987371 SUCCESS, job111918386052, input
f5568edd37b4c22257717b20bb205d84c57767e1,
tree0ed843a2f667564cfae1001203445ab22fbafdbc. Controlled loop/shared tests,
1920 original native calls,480 physical marker/model comparisons and60
reduced pet-guard witnesses reproduced remotely, derived artifacts uploaded.
Earlier remote-pending status superseded; all explicit experimental exclusions
and complete production AttackSeq/runtime boundaries remain OPEN.


### SRC-BATTLEMODEL-PHYSICAL-ATTACKSEQ-R1

- Type: independent equipment-free experimental adapter with transient native
  physical composition; no original source/payload assets retained.
- Clean source pins: gavin1f90cb6c /iris9e6c8ce2 /bismarck999ffdf1. Event file
  SHA256 respectively9a4607566b7cf6f6a94f2019c5d1dfc7088f7805421037b0a5f0095054b9db1d,
  2437d4fe88f1dd77e14ad5b976402053ddd1e297d471f45b4169c3588310d4db,
  b294f82e2a0b8382b59edd06fa8646fa3e50c00656eba496d8b78fa421c58ecc.
  Bismarck AttrCalc moved to battle/battle_magic.c at the same pin; SHA256
  cceea0c9d30922105904805cc4c18f22944ef1c936b89315625ddd9a83b12018.
- Eleven original functions compile under separately declared newpower/old
  defense profiles: Duck/Guardian/CriticalPlayer/Critical/Damage/CriDamage/
  FieldAttAdjust/AttrCalc/AttrAdjust/GuardAdjust/AttackSeq.232 comparisons per
  profile,696 total verify damage/outcome/Guardian/RNG ranges and order.
  Getters, CanMove, reaction selection and no-ride/equipment remain controlled.
  Synthetic admission fixture changes only evidence identity; no raw assets.
- `tools/stoneage_battlemodel_physical_attackseq.py`,
  `tools/stoneage_battlemodel_physical_source_audit.py`,17 new adapter tests and
  `specs/STONEAGE-BATTLEMODEL-PHYSICAL-ATTACKSEQ-R1.md`;157 local tests PASS.
  Extended settlement CI publication pending. Full runtime/round/coordinator/
  pressure, equipped interactions and exhaustive float32 equality remain OPEN.
- Source inspection also establishes gavin legacy ItemCrushCheck and guarded
  TAKE_ITEMDAMAGE selection consume RNG before any equipment lookup can rule
  out an item. Equipment-free scope must NOT be promoted to no-ItemCrush proof.
  Multi-profile/native ItemCrush acceptance is the next gate.


#### SRC-BATTLEMODEL-PHYSICAL-ATTACKSEQ-R1 remote acceptance

Run37359587030 SUCCESS, job111930531041; input
ce4c7a16dc022e7ce88b314b8cb2845f0012389e,
tree4f5b4f6d2a845f7ea781b0ce5de6b09a59b269db.157 tests/696 physical
comparisons plus1920 settlement/480 marker/60 pet checks reproduced remotely;
derived artifact11366277131 retained. Bounded physical composition accepted;
full runtime/pressure/638 positive slots unchanged. Pending records superseded.
Further source inspection at all three pins confirms ItemCrush RNG preceding
equipment validation. Bismarck has additional guarded pet-equipment and FIX
variants; native/runtime ItemCrush acceptance is still OPEN.


### SRC-BATTLEMODEL-EMPTY-EQUIPMENT-ITEMCRUSH-R1

- Clean pins gavin1f90cb6c /iris9e6c8ce2 /bismarck999ffdf1 unchanged.
  Read battle_event.c Check/Seq/helper, legacy ItemCrush body, battle.c global
  default400000 and reduced char_base.h equipment/pet enums. Event hashes
  are those already recorded for physical AttackSeq. Additional SHA256:
  gavin battle.c a10380b862aee077a798fab359ea89445b98aac4fc809b51a2bc7c682c7eb602,
  header2959c40645149277878661dd49ccffd1653f11fcb55c93f03efe306e6d578d45;
  iris battle.c6cbcf85a2e6533bf0423a71902faffe85d350ae7ad21267643a4884076b701f8,
  headerd53f39efe6f18ad90b668457461624f2a9aef542b24389a4e0e14c6b64f92645;
  bismarck battle.c2346951869d2f25e854ad5390bac1bd91608d91870922d96c84d9172d3d63e18,
  header71bcc04e14959e6c4646759716e034c8d9209c17d8457d94a8b1071b5d4d5fa4.
- Transient native original Check/Seq/helper and legacy empty scan, controlled
  no-equipment getters/physical/status/libc raw values; TAKE mutation traps.
  Two variants each gavin/iris, five bismarck;380 cases/variant,3420 total
  verify lookup identity/order, surviving DODGE/zero reachability and RNG
  before status. Extra equipment slot macros excluded; default5/pet7 declared.
- Independent `tools/stoneage_battlemodel_itemcrush_model.py`,
  `tools/stoneage_battlemodel_itemcrush_source_audit.py`,13 new tests and
  `specs/STONEAGE-BATTLEMODEL-ITEMCRUSH-R1.md`;170 local tests PASS.
  Extended CI publication/acceptance pending. No original payloads retained,
  equipped mutation/full runtime/profile membership/coverage remain OPEN.


#### SRC-BATTLEMODEL-EMPTY-EQUIPMENT-ITEMCRUSH-R1 remote acceptance

37411512720 SUCCESS, job112100761415; exact input
7c7de32d7284eca3ea4dc66b8534f0c04bc14455,
tree8b81bae80313f02aed8295a21a10917c99de97ed. All170 tests/3420
ItemCrush comparisons,696 physical and1920/480/60 settlement/marker/pet
checks reproduce remotely. Derived artifact11389775634 uploaded. Explicit
empty-equipment chronology accepted; equipped/full runtime/profile membership
remains OPEN, no new slot coverage. Previous pending records superseded.


### SRC-BATTLEMODEL-PREPARED-HANDOFF-R1

- Independent engine-neutral experimental handoff; no original source/assets
  retained. Uses accepted fixed-pin physical/ItemCrush loop and existing
  PreparedBattleRound/ordinary resolver as independent continuation witness.
- Source helper already recorded under ItemCrush source event-file hashes:
  successful common status writes actual defender COM1=NONE. Prepared handoff
  retains COM2/COM3 and dynamic work snapshots without guessing numeric638.
  Exact ordered prefix is supplied by caller, not independently reconstructed.
- tools/stoneage_battlemodel_prepared_handoff.py and12 new tests;283 total
  local PASS. Ordinary continuation verifies cancellation after paralysis
  expiry, failed status action, no completed actor/tick replay, fresh guard at
  new preparation, HP/death/Guardian/reflection and strict RNG/identity gates.
- New handoff has no native full-command-loop certificate. Extended existing
  native physical/item/settlement gates reproduce hit machinery only. Remote
  acceptance pending. Actor status clock/rewrite, complete dispatch/state/
  coordinator, profit/ultimate exit, equipped variants and638 coverage OPEN.


#### SRC-BATTLEMODEL-PREPARED-HANDOFF-R1 remote acceptance

37412928360 SUCCESS, job112105158829; input
57d21667464cd39d970c3e70e549fb3febd6d81f,
tree35bea36b05c6440bb800bee8e4992a79cf7deb90.283 tests, including12
new actual ordinary continuation witnesses, and prior696/3420/1920/480/60
native gates reproduced; artifact11389966161. This closes bounded handoff,
not original full command-loop/persistent/coordinator/ultimate acceptance.
Next review includes ordinary player ultimate default-selection semantics
under DD-020. No raw source/payload retained; pending records superseded.


### SRC-BATTLEMODEL-NONLETHAL-ORDINARY-STATE-COORDINATOR-R1

- Independent engine-neutral integration using existing accepted common status
  clock, ordinary driver and fixed-pin physical/ItemCrush helper. Same three
  clean source pins/event hashes; no raw source or proprietary payload retained.
- Typed BattleModelRoundAction and current work binding, explicit semantic
  NONE/source-target carrier, actor tick before dispatch, chronological owned
  RNG, actual Guardian/status cancellation and nonlethal immutable transaction.
  Shared physical binder now reads typed current status work QUICK when supplied
  rather than silently requiring stale setup QUICK after drunk expiry.
-31 new witnesses:24 actual ordinary rounds,3 state and4 coordinator cases.
  428 local tests PASS; existing696 physical/3420 ItemCrush/1920 settlement/
  480 marker/60 pet native reruns PASS. These native gates cover hit machinery;
  no new original full-command-loop certificate is asserted. Explicit opposing
  slot order remains a caller authority; production OPTION identity unchanged.
- Coordinator re-admits from current actual template/loaded runtime/work powers.
  Automatic skill selection, lethal/ultimate/default-selection profit flow,
  equipped/extra slots/wider features, BattleModel-specific golden/region/
pressure and638 positive slots OPEN. Remote exact/all-workflow gates pending.


#### SRC-BATTLEMODEL-NONLETHAL-ORDINARY-STATE-COORDINATOR-R1 remote acceptance

Exact input a03b87813eb1b21a7811d523586102b1701be293, tree
b46bc747ac7e96a33e739878640a3e037175d0ef: all32 triggered Actions SUCCESS.
Settlement37414798897, job112110945349, reproduces428 tests and native
696/3420/1920/480/60 checks. Artifact11390323818; exact baseline golden
37414798930 and full-region37414798987 SUCCESS. Receipt records every run.
Only bounded nonlethal explicit integration accepted; new BattleModel golden,
pressure, full original command loop, lethal/default-pet/automatic AI and638
slots remain OPEN. Pending snapshot superseded; no raw source/payload retained.


### SRC-EXPLICIT-DEFAULT-PET-EXIT-HELPER-R1

- Existing clean fixed pins gavin1f90cb6c/iris9e6c8ce2/bismarck999ffdf1.
  battle.c SHA256 respectively a10380b862aee077a798fab359ea89445b98aac4fc809b51a2bc7c682c7eb602,
  6cbcf85a2e6533bf0423a71902faffe85d350ae7ad21267643a4884076b701f8,
  2346951869d2f25e854ad5390bac1bd91608d91870922d96c84d9172d3d63e18.
- Unmodified BATTLE_PetDefaultExit compiled transiently against controlled
  getters/Exit returns:486 native cases. Exact explicit DEFAULTPET lookup,
  no-selection/type/index short-circuit and source return/selection contract.
  Original source/assets not retained; no complete native cleanup/profit claim.
- Static UltimateExtra/pet-selection and separate Entry[i+5] cleanup anchors
  distinguish ownership/selection/occupancy. Bismarck identifier normalization
  applies only to static anchors; original helper is compiled unchanged.
- Exact b6ca59eb86d2e0d1462fcdf56939d2c1cd7e6f8b,
  tree23f26db6cb082ec75b742ad48f5c5a9f1b633ca1;
  run37415958204/job112114499031 SUCCESS, artifact11391295439.
  Existing428 tests and696/3420/1920/480/60 native checks reproduced.
- Current ordinary/continuation selected-pet inference and pet-ultimate
  chronological selection/profit defects OPEN. Spec/receipt record correction
  contract; no full lethal BattleModel/original build/Taiwan-v1/638 promotion.


### SRC-DEFAULT-PET-ULTIMATE-STATE-CORRECTION-R1

- Independent owner/selection/occupancy authority model and ordinary/shared
  nonbow/persistent integration under DD-020, grounded in already accepted
  three-pin486 helper cases and separately declared static Exit/UltimateExtra
  observations. No original source/assets retained; no full native exit proof.
-22 new actual flow cases: nullable/missing authority, exact selected/paired
  identities, unrelated/multiple/retained/exited pets, dead unprepared occupancy,
  actual Guardian, pet ultimate then player death across actors and hits,
  signed loyalty/selection ordering, failure immutability and terminal return
  without final profit.535 targeted PASS; existing world golden PASS.
- Clean-baseline3523 vs changed3545 broad-discovery failure/error names are
  identical (25 optional probe import errors, two pre-existing fixture failures).
  Local derived receipt preserves limitations; no full-suite PASS claimed.
- Spec STONEAGE-DEFAULT-PET-ULTIMATE-RUNTIME-R1; remote exact/shared/full-region
  gates pending.638 remains nonlethal/unpromoted; full native Exit/profit,
  equipped/wider features, automatic AI and638-specific pressure remain OPEN.


### SRC-EXPLICIT-DEFAULT-PET-ULTIMATE-STATE-R1 — 2026-10-06

- Kind: independent modern DD-020 correction and exact remote regression;
  historical helper/static evidence remains the three clean pins recorded in
  SRC-EXPLICIT-DEFAULT-PET-EXIT-HELPER-R1. No raw source/payload retained.
- Input0a4cecc36e3b36c17d3f032dfd826412801d9679,
  tree97546cab8a298d2e9d850ccee9d70154630324f7: all33 Actions SUCCESS.
  Settlement37417691024/job112119856439:535 tests/22 new, prior native
 486/696/3420/1920/480/60 checks. Full-region37417690927 PASS, no writeback.
- Accepted scope: exact nullable selection, owned roster and paired occupancy,
  pet-ultimate chronological selection/profit-state clear, persistent carried
  cleanup and terminal return. Receipt/spec preserve reduced-profile and
  broad-suite limitations; no lethal638 or full native composition claim.
- Static three-pin preflight metadata:
  research/recovered/STONEAGE-PROFIT-EXIT-COMPOSITION-PREFLIGHT-R1.json.
  PvE AddExpItem side/slot scan and BattleModel command-tail profit establish
  next audit boundaries; zero native composition cases. Full contract:
  specs/STONEAGE-BATTLEMODEL-PROFIT-EXIT-COMPOSITION-PLAN-R1.md.


### SRC-PVE-PROFIT-EXIT-NATIVE-COMPOSITION-R1 — 2026-10-06

- Same clean fixed gavin1f90cb6c/iris9e6c8ce2/bismarck999ffdf1 pins.
  battle.c, battle_event.c and char_base.h/battle.h/battle_event.h hashes,
  seven stripped-function hashes and native counts emitted in
  research/recovered/STONEAGE-PVE-PROFIT-EXIT-NATIVE-R1.txt. No raw source
  retained. Reproducer: tools/stoneage_profit_exit_source_audit.py.
-6552 cases per pin/19656 total LOCAL PASS: source side/slot death scan plus
  actual Exit/helper/normal/ultimate/base-status bodies. Ten-field original
  table and extent verified, including ISDIE clearing. Ordered semantic traces
  and final state/ownership/EXP/counts checked; some injected snapshots are
  controlled function experiments rather than historical Entry witnesses.
- Harness controls getters/field keys, no-item/no-ride and external penalty
  helper deltas/notifications/elder/party/deallocation. It does not execute
  Guardian physical selection or full original Battling/638 driver. Four
  STATIC profit-boundary anchors separately checked; original active build and
  JSS/Taiwan-v1 membership, complete modern638 runtime/pressure remain OPEN.
- Spec: STONEAGE-PVE-PROFIT-EXIT-NATIVE-AUDIT-R1. Extended settlement CI pending
  exact remote acceptance; no positive-slot or overall-percentage promotion.


#### SRC-PVE-PROFIT-EXIT-NATIVE-COMPOSITION-R1 remote acceptance

Inputc1c3209e4bf8a6f9c7193a3be44435f1564b6a23,
tree777d45a00ad13f6fa35a57f6efd2422161b3b092,
run37420393572/job112128219849 SUCCESS.19656 cases at the same three
clean pins and535 regressions/prior native gates reproduced; artifact
11392388401 and STONEAGE-PVE-PROFIT-EXIT-NATIVE-ACCEPTANCE-R1.json record
all profile/header/function hashes. Local-pending statement superseded;
controlled external seams, injected-state/reachability limits, native full
command bridge, modern lethal638/pressure and original version membership
remain explicitly OPEN. No original source/payload committed.


### Immutable PvE profit/exit scan model local witness — 2026-10-06

- Derived model/native report:
  research/recovered/STONEAGE-PVE-PROFIT-EXIT-SCAN-MODEL-R1.txt.
  Spec: specs/STONEAGE-PVE-PROFIT-EXIT-SCAN-MODEL-R1.md.
- Source pins and seven-function/header hashes remain those in the accepted
  STONEAGE-PVE-PROFIT-EXIT-NATIVE-ACCEPTANCE-R1.json. No original source/asset
  is committed.19656 new modern-model comparisons use existing native cases.
- Replay: python -m tools.stoneage_profit_exit_source_audit --verify-scan-model
  with --gavin-dir/--iris-dir/--bismarck-dir clean source checkouts.
  Original dispatcher call-site anchors remain static; full native command
  integration, original build/version and modern lethal638 stay OPEN.


### Isolated immutable PvE scan model exact remote certificate — 2026-10-06

- Input737da28735dc955e3d6a4e5ed2e27649096799fd,
  tree41fc47883d68b877ee9405df454c50496f0a9ade.
  Required run37422202059/job112133821223 SUCCESS. Artifact11393920866.
- Receipt research/recovered/STONEAGE-PVE-PROFIT-EXIT-SCAN-MODEL-ACCEPTANCE-R1.json
  records exact source/function/header and implementation hashes,19656 model/
  native comparisons and560 regressions. Prior native gates also reproduced.
- CLOSED_BOUNDED_ISOLATED_MODEL_NATIVE_MATCH only. Full command-native
  bridge, attribute-recalculation integration, actual Guardian attack-to-profit
  and modern lethal638 remain OPEN. No raw original code/assets committed.


### Actual player Exit late-status local replay — 2026-10-06

- Spec specs/STONEAGE-PLAYER-EXIT-STATUS-RUNTIME-R1.md.
  Derived report research/recovered/STONEAGE-PLAYER-EXIT-WEAKEN-NATIVE-R1.txt.
- Existing tools.stoneage_weaken_source_audit at the three clean source pins
  reproduces384 recalculation vectors under ASan/UBSan. Existing seven-function
  profit/exit audit reproduces19656 model/native comparisons after sharing the
  modern clear primitive. No original source/assets committed or new vectors.
- Runtime/modern baseline restoration is separate from original full
  complianceParameter, build/version or lethal638 acceptance; those stay OPEN.

### SRC-PLAYER-EXIT-LATE-STATUS-RUNTIME-R1 — remote acceptance 2026-10-06

- Modern bounded runtime acceptance only; no original source/assets committed.
  Exact head `0425028d5965c76d34106a427c4a47f4a56f620b`, tree
  `c84d46c6b1e8140579bffdaa950ba12c44505778`.
- Main 33/33 triggered workflows SUCCESS; synchronized
  `agent/player-exit-status-runtime-r1-20261006` 31/31 SUCCESS. Main settlement
  `37425651218/112144564632`: 643 tests, 19656 immutable
  scan/model-native comparisons, 486 DEFAULTPET helper cases and 384 bounded
  Weaken recalculation vectors. Artifact `11395306244`,
  `sha256:005110756a634a0b6fae329c38cef240be8556475d869c8d9f421b58fddcb107`. Golden `37425651031`, Taiwan gameplay
  `37425651183`, region `37425651071` SUCCESS.
- Accepted behavior: actual player ultimate Exit clears the admitted modern late
  overlay/cache for explicit owner plus complete non-mail carried roster and
  restores session-derived work state; independent SetMagicPet prepared powers
  remain separate. Missing owner authority and unknown active status fail closed.
- Receipt:
  `research/recovered/STONEAGE-PLAYER-EXIT-STATUS-RUNTIME-ACCEPTANCE-R1.json`.
  Original full complianceParameter, whole-scan command integration,
  processed-death persistent accounting, actual Guardian-to-profit chronology,
  lethal638 and wider feature/version membership remain OPEN.

### SRC-PROFIT-BOUNDARY-RUNTIME-TRACE-R1 — remote acceptance 2026-10-06

- Modern runtime observation certificate only; no original source/assets or new
  original native vectors committed. Implementation `6d4298c40fca439d1dcf153b5630c24d3b4de0d6`;
  accepted tested input `fe9109a7440caa9c10847eb649c01c28b7348075`, tree `9366032fe3126f062a9cf58d3a5a4b9e1138fec8`.
- Implementation head: 31/31 triggered workflows SUCCESS; settlement
  `37427373309/112149996535`, region `37427373349`; artifact
  `11395384042`,
  `sha256:d014126a5a04de80d24ce5fc9accedd7bf53ccc4f831176efeeb4275a96fd039`.
  Final test-only head: settlement `37427836728/112151449355` SUCCESS,
  646 tests; artifact `11395995441`,
  `sha256:19550e602bb7b6fa2ab337fce14dbb615cc523822a57d830e2a29971e6ea3d36`.
  Existing 19656 immutable scan/model-native comparisons and 384 bounded
  Weaken recalculation vectors replayed.
- Accepted scope: typed pre-AddProfit snapshots, ordinary per-hit versus
  nonlethal638 command-tail separation, pre-Exit player-ultimate occupancy
  witness, and cross-boundary processed-death/ISDIE carry. The current
  counter/BatFly labels remain explicitly modern-driver observations, not
  original chronology certificates.
- Receipt:
  `research/recovered/STONEAGE-PROFIT-BOUNDARY-RUNTIME-TRACE-ACCEPTANCE-R1.json`.
  Persistent processed-death settlement consumption, full original command
  bridge, actual Guardian/multi-victim composition, lethal638, wider profit
  recipients/features and build/version membership remain OPEN.

### SRC-PERSISTENT-PROCESSED-DEATH-STATE-R1 — remote acceptance 2026-10-06

- Modern runtime state certificate only; no original source/assets or new
  original native vectors committed. Exact input `55416079254b542c2c792d2848b6d2a493345335`, tree
  `3a45d85cca0de26cdc597746f49a1d01655b6216`.
- **32/32** triggered workflows SUCCESS. Settlement
  `37428752934/112154374994`: 648 tests, 19656 immutable scan/model-native
  comparisons, 384 bounded Weaken recalculation vectors; artifact
  `11395837824`,
  `sha256:6fe85f8dc911fa2854e1d68d5510effdfce87fd671e63d7f7e6374aa5dd6f372`.
  Recovered25 region `37428752792/112154374696` SUCCESS.
- Accepted scope: persistent all-side processed-death/ISDIE state, cross-round
  carry, ReLife/Exit/capture clearing, and later boundary visibility. ReLife
  eligibility remains a separate enemy-only concept.
- Receipt:
  `research/recovered/STONEAGE-PERSISTENT-PROCESSED-DEATH-STATE-ACCEPTANCE-R1.json`.
  Whole-scan settlement consumption, sparse/source roster mapping, full original
  command chronology, lethal638 and wider recipients/features remain OPEN.

### SRC-PROFIT-SCAN-RUNTIME-BINDER-R1 — remote acceptance 2026-10-06

- Modern runtime integration certificate only; no new original source/assets or
  native vectors committed. Implementation `babf091e66192463cc51ac06a51348b8ef010048`; final tested input
  `f9bc6b1688500987562fda89ab347984ab12a684`, tree `cf8af0a399453487807976c2681bf841cabd5a5e`.
- Implementation head: **31/31** triggered workflows SUCCESS. Settlement
  `37430287171/112159300888`: 653 tests, 19656 immutable scan/model-native
  comparisons, 384 bounded Weaken recalculation vectors; artifact
  `11396209963`,
  `sha256:023a25d6b06f17951decffeb8a531c6854b5f7cf0b98b064769e33794a816f0b`.
  Recovered25 region `37430287204/112159301018` SUCCESS. Final test-only
  settlement `37430504940/112160004965` SUCCESS; artifact
  `11396273753`,
  `sha256:e0c0a89ca66965d2933ce9fe38dc2ec836dd0176791f1b6d48752dafaee7c7ef`.
- Accepted scope: canonical SIDE_OFFSET10 runtime binding, sequential ISDIE,
  scan-based accounting, scan status-clear projection, explicit nonlethal638
  command-tail admission, and the earlier-normal-pet/later-player-ultimate
  chronology regression.
- Static original call-site evidence still shows BattleModel has zero internal
  AddProfit calls and command tail owns the profit call, but the existing
  source audit does **not** compile full Battling/BattleModel. A separate native
  command-driver harness with actual Guardian/multi-victim tail is therefore
  still OPEN and required before lethal638.
- Receipt:
  `research/recovered/STONEAGE-PROFIT-SCAN-RUNTIME-BINDER-ACCEPTANCE-R1.json`.

### SRC-BATTLEMODEL-PROFIT-TAIL-SPLICE-R1 — remote native acceptance 2026-10-06

- Exact input `da3512edb89877d0761fde7ddbe083f03237dd0e`, tree `16220e2ffa4da9e9bce8321eb3b8c0952fcb6163`; no original source or
  assets committed.
- Settlement `37433803780/112170605599` SUCCESS: 653 tests, 19656 original
  PvE profit/exit cases, 19656 immutable scan/model-native comparisons, 384
  bounded Weaken recalculation vectors and **9 native dispatch-tail splice
  cases** across the three clean pins. Artifact `11397488740`,
  `sha256:f28d16bd25e02eaa54b5e9ebaf8e1f5bd654140e426e01f8cffb2bb32a645fa9`.
- Source hashes remain:
  gavin battle `a10380b8…`, event `9a460756…`;
  iris battle `6cbcf85a…`, event `2437d4fe…`;
  bismarck battle `23469518…`, event `b294f82e…`.
- Accepted claim: original BattleModel/helper and original tail AddProfit execute
  in one transient program in the statically verified case→tail chronology;
  multi-victim tail processing and repeat-profit idempotence match the immutable
  scan. BattleModel internal AddProfit count remains zero.
- Boundary: full `BATTLE_Battling` case body and same-harness original
  AttackSeq/GuardianCheck are **not** certified here. Lethal638, original
  build/version and wider runtime remain OPEN.
- Receipt:
  `research/recovered/STONEAGE-BATTLEMODEL-PROFIT-TAIL-SPLICE-ACCEPTANCE-R1.json`.

### SRC-BATTLEMODEL-SAME-HARNESS-GUARDIAN-PROFIT-TAIL-R1 — remote native acceptance 2026-10-06

- Exact input `93bd7fa550eaa99137015109237b78a67815c1fd`, tree `f97009c53238724f362847003976b26595c719d5`; no original source or
  assets committed.
- Settlement `37436034852/112177967610` SUCCESS: 653 tests, 19656 original
  PvE profit/exit cases, 19656 immutable scan/model-native comparisons, 384
  bounded Weaken recalculation vectors, 9 prior dispatch-tail splice cases and
  **9 same-harness original Guardian profit-tail cases**. Artifact
  `11399556875`,
  `sha256:65235a67ee514ff87487d041af8642ac0ee10ef7be5351d2615062b515800278`.
- Exact original physical function count linked in the same program: **11**,
  including `BATTLE_GuardianCheck` and `BATTLE_AttackSeq`. The exact
  BattleModel/helper and exact AddProfit/exit scan remain in the same transient
  executable.
- Original battle flag macros are imported directly from pinned headers:
  Guardian `1<<3`, ABIO `1<<6`, NODUCK `1<<7`; all three pins agree.
- Accepted chronology: a pre-AddProfit zero-HP guardian can remain an original
  GuardianCheck candidate because ISDIE is false, while BattleModel's
  post-AttackSeq TargetCheck controls the final DamageSub target. Multi-victim
  writes precede the single tail scan and repeat AddProfit is idempotent.
- Boundary: DamageSub is still controlled in this same harness, full Battling is
  not executed, lethal638/build-version/wider feature claims remain OPEN.
- Receipt:
  `research/recovered/STONEAGE-BATTLEMODEL-GUARDIAN-PROFIT-TAIL-ACCEPTANCE-R1.json`.

### SRC-BATTLEMODEL-SAME-HARNESS-EXACT-DAMAGESUB-PROFIT-TAIL-R1 — remote native acceptance 2026-10-06

- Exact input `f804d879cc701b0b29c2d3f2adbd1e2b6df1eddc`, tree `d99b472d1f0e97df01518ae9bae184fe0b4584ac`; no original source or
  assets committed.
- Settlement `37437282822/112182088944` SUCCESS: 653 tests, 19656 original
  PvE profit/exit cases, 19656 immutable scan/model-native comparisons, 384
  bounded Weaken recalculation vectors, prior splice 9/9, prior original
  Guardian 9/9 and **9 same-harness exact DamageSub profit-tail cases**.
  Artifact `11399543542`,
  `sha256:f01386a4c5b42a701ed4dd54863e5ed554ea70dafa564a1aad806e3bdf00c6cf`.
- Exact comment-stripped DamageSub hashes:
  gavin/iris
  `c978e7fb82412570086d67b582d0ff6c84a33b72a0481fb327634977ebd3ac9e`;
  bismarck
  `e1dff8b748beba524cd203ac8dd7090df3593cd00692708effff2579cdb582d6`.
- Accepted claim: exact DamageSub HP/ultimate/reaction state machine executes in
  the same process as the already accepted original physical Guardian path,
  exact BattleModel/helper and exact tail AddProfit; gameplay-state chronology
  matches the immutable scan in the bounded no-ride/no-equipment/noncritical
  profile.
- Boundary: the wrapper seeds only the historically undefined BattleModel
  `iPetDamage` input to zero. Presentation/packet bytes and full Battling are
  not certified. Lethal638/build-version/wider features remain OPEN.
- Receipt:
  `research/recovered/STONEAGE-BATTLEMODEL-DAMAGESUB-PROFIT-TAIL-ACCEPTANCE-R1.json`.

### SRC-BATTLEMODEL-FULL-BATTLING-PROFIT-TAIL-R1 — remote native acceptance 2026-10-06

- Exact input `1fd9866556f9cf0ec338e22c804a4354e2f8c3e0`, tree `533c3554a4ade9a49b52f3263c6b6d584d3fe68a`, branch
  `agent/native-full-battling-profit-tail-r1-20261006`; no original source or assets committed.
- Settlement `37441895862/112197395144` SUCCESS: 653 tests, 19656 original
  PvE profit/exit cases, 19656 immutable scan/model-native comparisons, 384
  bounded Weaken recalculation vectors, prior splice/Guardian/exact-DamageSub
  9/9 each and **9 full-`BATTLE_Battling` native cases**. Artifact
  `11401378027`,
  `sha256:31be8e5c965b8658c67d4e7055c2035a54148aff710d86f4f8bc1aa5e5eb38f2`.
- Exact full-body SHA-256:
  gavin `48c648ac8cb66a60ae4a955d08a332d56bb4b4a8dcc6659ff55e6a1b7cfc1f4f`;
  iris `74f51b9d98e5a797c52c3474d0c0603808c95b70bc0c55344afe4375d7a1225b`;
  bismarck `b23e58042695a5fdb9c0cd451604a88d7c9063279b9726860ab9726bd615ea27`.
- Accepted claim: the exact full original `BATTLE_Battling` body executes the
  original BattleModel case and common tail AddProfit in the same process as
  original Guardian/AttackSeq, exact DamageSub and exact BattleModel/helper,
  preserving conditional source context.
- Modern differential: **9/9** identical post-hit boundaries directly match the
  accepted canonical skill638 command-tail runtime binder. This certifies the
  bounded chronology bridge, not universal historical skill identity.
- Controlled seams: `BATTLE_DexCalc`, `EntrySort`, `ComboCheck`,
  `BATTLE_StatusSeq`, `BATTLE_GetAttackCount`, `BATTLE_PetLoyalCheck`,
  `BATTLE_TargetListSet`, `BATTLE_CountAlive`, `BATTLE_CommandSend`.
  Build/version, wider recipients, ride/items, automatic AI, packets and
  lethal638 persistent/coordinator admission remain OPEN.
- Receipt:
  `research/recovered/STONEAGE-BATTLEMODEL-FULL-BATTLING-PROFIT-TAIL-ACCEPTANCE-R1.json`.

### SRC-BATTLEMODEL-ID638-NORMAL-DEATH-PERSISTENT-R1 — remote runtime acceptance 2026-10-06

- Implementation head `6c4032a4d6f3c3ab12b2e2c0c9830033809ba33b`, tree
  `ec14ccbe881f6065ac1afc73466a702758a6eba4`; final tested input
  `89848f2ed92c4aa4c21c70d68356fe52b951ab40`, tree
  `312a842d8d093fa57bb1b4a4200186dcaa63ce1a`. No original source/assets
  committed.
- BattleModel settlement `37443593822/112202958318` SUCCESS: **655 tests**,
  19656 original PvE profit/exit cases, 19656 immutable scan/model-native
  comparisons, full-Battling / exact-DamageSub / Guardian / dispatch-tail
  native witnesses **9/9 each**, and 384 bounded Weaken recalculation vectors.
  Artifact `11401694955`,
  `sha256:d9bae433e4e06df60f2f18f7c6b11a697aff04377be8619fe6862e9ec6b1b41e`.
- Integration evidence at implementation head: coordinator
  `37443283037/112201941097` SUCCESS (**231 tests**), runtime golden
  `37443283236/112201941937` SUCCESS, recovered25 region/runtime-stack
  `37443283255/112201946517` SUCCESS.
- Accepted claim: already accepted recovered ID638 admission now composes with
  one canonical BattleModel command-tail whole-scan boundary for **normal
  death**, and persistent state takes processed-death authority from that scan.
  Coordinator re-admission still validates current template/skill/runtime
  identity before commit.
- Boundary: ultimate flags, BATTLE_UltimateExtra/BATTLE_Exit, multi-victim
  ultimate source-slot ordering, automatic BattleModel AI, ride/equipment,
  wider callbacks, packets and build/version remain OPEN. A later ordinary
  non-BattleModel death cannot borrow this scope.
- Receipt:
  `research/recovered/STONEAGE-BATTLEMODEL-ID638-NORMAL-DEATH-PERSISTENT-ACCEPTANCE-R1.json`.
  Positive slots promoted: **0**.


### SRC-BATTLEMODEL-ID638-ULTIMATE-EXIT-R1 — remote bounded runtime/native acceptance 2026-10-06

- Exact tested input `12f61e06a8e773bf223f37d7be9acc67460571e7`, tree `2b7ef3df20b01801a5d80a758a70c5a22baf35eb`.
- Settlement `37448704545/112219678935` SUCCESS: 661 tests, 48 new full
  original Battling ultimate/native-binder comparisons, prior 19656 original
  PvE profit/exit and 19656 immutable scan comparisons, prior four 9-case
  same-harness gates, and 384 bounded Weaken recalculation vectors.
- Artifact `11405655040`,
  `sha256:6f3b1281ab89609cc7067b9d4d701e44729234b0d3e2ef33bb35c5ba2766df9d`.
- Exact-head coordinator `37448704430/112219678366` SUCCESS (231 tests);
  generic runtime golden `37448704495/112219678442` SUCCESS. Full-region
  verdict and source/function/header hashes are in the receipt.
- Accepted claim: newly lethal ID638 ultimate kinds reach the canonical command
  tail; source slot order determines owner/pet Exit/accounting in the persistent
  coordinator. Native work type5/four objects, actual pre-profit captures and
  repeat-whole-state idempotence are certified in the declared reduced profile.
- Boundary: source C status/presentation OPTION is neutralized; this is not a
  historical active-build/packet certificate. BattleModel-specific full recovered
  payload runtime/golden/region/pressure promotion remains OPEN. 0 slots promoted.
- Receipt: `research/recovered/STONEAGE-BATTLEMODEL-ID638-ULTIMATE-EXIT-ACCEPTANCE-R1.json`.


### SRC-BATTLEMODEL-RECOVERED-RUNTIME-GOLDEN-R1 — exact-head acceptance 2026-10-06

- Exact tested input `24b61a6c3f051d7d6f44efb67df34af1c0eff0c5`, tree `ae66a157b0a791580db7d69b85cab0803ab81e90`.
- Settlement37452535512/112232279318 SUCCESS (666 tests;48 native ultimate,
  19656 profit/exit and19656 immutable scan comparisons); coordinator
  37452535491/112232256552 SUCCESS (236 tests); golden
  37452535501/112232256576 SUCCESS (7 tests); verified region
  37452535455/112232680115 SUCCESS (147 tests and826 materializable floors).
- Derived actual-data markers:60 distinct ID638 persistent/coordinator goldens,
  same60 concrete-stack goldens,12 identity rejections in each suite, and the
  complete pressure ledger2486=2461 closed+22 OPEN+3 historical UB.
- Artifacts11407805107
  (`sha256:afd8ee8abd8c5c147b9d545ec6dbe64ccba68bb9b6d0bb12a4d7fec654ae3b1d`)
  and11408095891
  (`sha256:52365418bc1634daa4a32ae71ce36d857651a27f898e5dd13e29628ad4177d11`).
- Input rows remain transient and hash-verified; report writeback
  `83f04b657fe2db5ec2815533f59075f1a069fc52` contains only two new aggregate stack lines.
  CLI count handoff and shallow/main report-rebase defects are corrected.
- Boundary: controlled work/position/RNG and explicit typed action selection;
  both charset profiles retained. Normal enemy-AI selected dispatch, original
  active build and broader runtime remain OPEN. Promotion decision HOLD,0 slots.
- Full receipt: `research/recovered/STONEAGE-BATTLEMODEL-RECOVERED-RUNTIME-GOLDEN-ACCEPTANCE-R1.json`.


## 2026-10-06 — ID638 selected normal-AI composition gate (PENDING)

- Specification: `specs/STONEAGE-BATTLEMODEL-AI-SELECTION-R1.md`.
- Runtime control gate extends `tools/stoneage_recovered25_battlemodel_runtime_probe.py`
  and the concrete stack; original OPTION/TACTICSOPTION bytes stay transient.
- Active input identities inherited from `STONEAGE-25-ENCOUNT-CHAIN-R1.txt`:
  enemy.txt SHA256 cc7418d3b6726f1c458fef9e44a24696d05f076b67c62a56ed2293e26ae63bb6;
  group1.txt SHA2564a02f2a3fa3d2dcf5589d8a2a560313c35d5a0a7e5e0589cc8df5f7df159ea8f;
  encount.txt SHA25670bbd997d98508a0587df183b5bdd48222ff42db91bf21bea632e0ed6f2fea87.
- Normal control OPTION is independently authored and explicitly labelled.
  Active recovered variant admission/execution and natural encounter provenance
  will be recorded from exact-head CI, not inferred from controls.


## 2026-10-06 — Accepted ID638 conditional selected normal-AI seam

- Tested input `e2f957095a3c5a81133ed720df63dfe11396a2e1`, tree `b872725d72a4967411ef01b2818667c0e8879225`.
  Four core exact-head workflows SUCCESS: settlement37456095056/112243963731
  (674 tests), coordinator37456095209/112243962831 (244), golden37456094952/
  112243963191 (15), region37456095656/112243964801 (155,826 floors).
  Local union850 PASS; initial implementation's27 triggered workflows PASS.
- Native artifact11409193075
  (`sha256:1862e778139c0136c25788ca92a929e1c672dfb9b88c8929cc3807ab3c5c942d`);
  region artifact11408649935
  (`sha256:cfec7c09b47e9d0a5bb8877bdad41d87a532bb97be78ef64d5317c7cc7e6d295`).
  Writeback `2bd37c14199551c42be7ab202bc32fa391abc97c` contains derived aggregate metadata only.
- Exact active census: template1178/enemy2559 and template1179/enemy2560,
  TACTICS1/selector1, rn absent, wa index2 weight0, eligibility0 and actual
  goldens0 per standalone/concrete suite. Decoded OPTION UTF8 SHA256
  `b3cacc228954fa200ec63a59e135c2aa73b58b6ff447b5ce4cb3108d075fc319`.
  This digest labels decoded text; active source file identity is separately
  pinned by the complete enemy.txt SHA256 recorded above.
- Independently authored control AI yields60 cases per suite. It does not
  replace actual recovered configuration, certify natural reachability or
  establish original active-build/Taiwan-v1 membership. Pressure remains
  2486=2461 closed+22 OPEN+3 UB;0 slots promoted.
- Full receipt `research/recovered/STONEAGE-BATTLEMODEL-AI-SELECTION-ACCEPTANCE-R1.json`; next gate `specs/STONEAGE-BATTLEMODEL-ACTUAL-DISPATCH-AUDIT-PLAN-R1.md`.

## 2026-10-06 — BattleModel command-entry audit R1

Derived-only source receipt:
`research/recovered/STONEAGE-BATTLEMODEL-COMMAND-ENTRY-SOURCE-AUDIT-R1.json`.
Auditor pins the same three descendant commits as guard-break2 research,
verifies clean trees and SHA256 of entry/AI/command/battle/enemy/magic/header
files; lists bounded lexical C sites, default-header macro flags and neutral
callback traces. Native2592 default-header +864 Bismarck counterfactual controls.
Exact master-data audit newly configured in region workflow, pending receipt.
Source/native facts do not establish original active-build flags or full
script/gameplay reachability. Spec: command-entry audit R1.

Loader flags include OPTIMUM/CFREE, with ID-indexed storage and final effective
array-bound source gates. Exact data census reports both default ID-indexed
and legacy ordered layouts; no original active-build layout assumption.

## 2026-10-06 — Exact command-entry data and CI acceptance

Source/data derived reports and command-entry acceptance R1 are accepted on
input c26dce336ba59eccc1aca82080c1982ab07ece08; four core Actions PASS and
source receipt equals exact CI. Data writeback c2d3b5dee957060163c1465cc5aa0776e1b8d1bd
adds only622-line derived JSON. Magic wholefile
b3a57b595bd60dfab571fe7af4dd6e2d43a5839c934eb644ba462897b1bcb6bb:
181 rows,0 literal callback candidates; both loader layouts censused.
Exact enemy/group/encount hashes, callback arrays/ILLEGAL, structural refs and
all active pressure rows are included, with no original names/OPTION/data
bytes. Receipt artifact digests pin native and full-region evidence. Original
build/opaque NPC/script/full gameplay paths remain OPEN. Next exact conditional
placement plan is a DESIGN capability gate, not a new historical reachability
claim or pressure promotion.

## 2026-10-06 — ID638 conditional placement capability gate (PENDING)

Uses the accepted command-entry/native/runtime receipts and the same pinned
petskill/enemybase whole-file identities. New factory reparse/semantic binding
and pure predicate store only metadata/digests; no original data/source bytes.
Dedicated pressure and full-region Actions independently recompute all2486
positive slots and preserve actual normal-AI selection0 as a separate axis.
Local878 unique tests PASS; exact-head acceptance pending. Specification:
`specs/STONEAGE-BATTLEMODEL-CONDITIONAL-PLACEMENT-CAPABILITY-R1.md`.


### SRC-BATTLEMODEL-ID638-CONDITIONAL-PLACEMENT-CAPABILITY-R1 — remote exact-head acceptance 2026-10-06

- Exact implementation input `74e5e937884865a561cd55dc0164bd4f029dad12`, tree
  `ae50e33edda6b3e0a8135d60144f21a637956bfc`.
- Required Actions SUCCESS: settlement37463130823/112267407318 (702 tests),
  coordinator37463130720/112267405941 (272), golden37463130586/112267405485
  (43), recovered25 region37463130861/112267406678 (183 plus826 floors), and
  dedicated pressure37463130784/112267406905 (23).
- Independent exact-data and concrete-stack pressure both report
  **2486=2463 closed capability+20 OPEN+3 historical UB**, unresolved IDs0,
  with exactly two `CONDITIONAL_BOUNDED_CAPABILITY` placements:
  (1178,2,638) and (1179,2,638). Next OPEN is BecomeFox ID625 (2 uses/2 templates).
- Actual recovered normal-AI BattleModel cases remain0; wa index2 weights remain0.
  This source therefore supports bounded static/runtime capability only, not
  natural command-entry reachability or original-build/Taiwan-v1 provenance.
- Native/default-header entry guards2592 + counterfactual864, existing native
  profit/exit19656 and immutable scan19656,60 explicit goldens,60 selected-AI
  controls and12 current identity rejects remain accepted.
- Artifacts:11413301367
  (`sha256:ec987508b387b7d2f3d9389c72fab5f5fea7194ec8e6498be0bd17c70eec1b93`)
  and11413686735
  (`sha256:c84759419eee99997dceafbe5fdbd15c3f93e6b59315e749540cbedfdb0ca075`).
- Derived writebacks f4eb651cbe6770c53abf361278996ab0924f7220 and
  d5fe135f738cbb2ac0bc76730b8e3f9a5758d459 touch only aggregate reports.
- Receipt:
  `research/recovered/STONEAGE-BATTLEMODEL-CONDITIONAL-PLACEMENT-ACCEPTANCE-R1.json`.


### SRC-BECOMEFOX-RECOVERED25-REFERENCE-R1 — exact source/data acceptance 2026-10-06

- Exact pinning input a0fed469ce621ce1dba53afd3d608074af144544, tree 73c835d23d670f6d0bc39828fecc525b92d874d8; remote Action
  37467755344/job112282980151 SUCCESS.
- Verified active petskill SHA256
  f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4.
  Complete callback population: only ID625, FIELD1/TARGET1/COST2/ILLEGAL3000,
  empty OPTION,2 positive uses across2 templates.
- Exact placements:148/IMG101743/base32,40,26,30/AI150/slot3 and
  149/IMG101744/base28,45,22,32/AI150/slot3.
- Pinned descendants gavin1f90cb6, iris9e6c8ce and Bismarck999ffdf each pass
  21 structural source gates. Material PetIn accessor divergence is retained.
- Boundary: no native ordered-hit equivalence, persistent FOXROUND runtime,
  original PRNG/build identity or historical membership is claimed; pressure
  promotion remains0.
- Receipt: `research/recovered/STONEAGE-BECOMEFOX-REFERENCE-ACCEPTANCE-R1.json`.


### 2026-10-07 — BecomeFox reviewed runtime acceptance; BecomePig entry observations

- Source class: exact GitHub Actions runtime/native/data evidence and pinned
  descendant source blobs; version scope later recovered25, not original v1.
- Acceptance input698660bc72a1933ec78d28263e5c5a4de324934d, tree
  e7238917a88e34ba0a555ba067b05b02723d995c. All35 workflows SUCCESS; core runs
  37611414633/37611414778/37611414397/37611414719. Full-region independently
  certifies826 floors, complete2465/18/3 pressure and existing concrete stack.
- Exact BecomeFox postattack oracle remains3840 original-block vectors at
  unchanged source/model/auditors; original run37471213887. No new historical
  executable or PetIn/ride/PRNG provenance claim. Acceptance receipt:
  research/recovered/STONEAGE-BECOMEFOX-RUNTIME-ACCEPTANCE-R1.json.
- Next-OPEN BecomePig preliminary record preserves exact commits and callback/
  dispatcher git blob identities for gavinlinasd/StoneAge, iriselia/StoneAge and
  BismarckDD/stoneage. Only derived source observations are stored, including
  player-only eligibility and OPTION divergence. Unchecked parsing and literal
  pointer comparison are not normalized or executed as accepted semantics.
  Record: research/recovered/STONEAGE-BECOMEPIG-PRELIMINARY-SOURCE-OBSERVATION-R1.json.
- Complete BecomePig row/OPTION/placement discovery and independent native
  gates remain OPEN; preliminary entry inspection promotes zero placements.


### SRC-BECOMEPIG-RECOVERED25-REFERENCE-R1 — independent source/data acceptance 2026-10-07

- Verified discovery37616100623/job112774680169 at4e1eedf; independent pinning
  37616438050/job112775782435 at e786dec2783a41a97f0d0c4d33472566d0c57488/tree
  801b402492c18ba8975b9be191580a2568f5b2eb SUCCESS. Eight tooling tests and
  all3 exact source commits24 structural gates each. Both active whole-file
  hashes reverified. Exact callback/dispatcher git blobs retained in receipts.
- Complete callback family628/631/635. Exact metadata/OPTION lengths and digests
  and template170/index2/631 plus1147/index2/635 independently reproduced;
  unused628 retained. Source/data reference only; native/runtime and pressure
  promotion remain OPEN. Receipt STONEAGE-BECOMEPIG-REFERENCE-ACCEPTANCE-R1.json.
- Artifact11480745785 SHA256
  9f471b84195eb3a946854b6360d282923a97ca4d142cfd42df70519bed53ad43;
  report writebackac4a4cae3e5818dcc5b4892bfe9642c8b907a440. No source/OPTION
  bytes or original names/descriptions/assets stored.
- Separate preliminary lifecycle observation pins network/version/getter blobs:
  gavin/iris separate one-second checkT2; Bismarck different10-second/sixth-loop
  sites. Default-header flags and invalid getter return also diverge. These
  observations do not replace original-C witnesses or select original builds.
  STONEAGE-BECOMEPIG-LIFECYCLE-PRELIMINARY-OBSERVATION-R1.json.


### SRC-BECOMEPIG-NATIVE-REFERENCE-R1 — bounded original-C acceptance 2026-10-07

- Source class: three pinned descendant C trees plus independently recovered
  hash-verified later recovered25 data; transient original-C native witnesses
  and exact GitHub Actions artifacts. No original executable selected.
- Discovery Action37618493394/job112782542021 passes input090588e/tree575ca7a;
  independent pinning Action37618923213/job112783971981 passes exact input
  66c466461c5355fc0674c82aacc48d6999e3be91/tree
  8141af46b3cc2c49a6b3c26ee895aa4b9334925b. Both reports unchanged at second
  recovery.16 remote domain/identity tests;24 structural gates/profile.
- Native62720 postattack comparisons and5364 isolated timer/Exit comparisons,
  both O0/O2+nonrecovering UBSan. Valid actual row buffers, controlled draws,
  bounded arithmetic; uninitialized source paths never accepted as deterministic.
- Actual631 has2 conversions,635 has3; gavin/iris30/180 images100250/100388.
  Bismarck valid-buffer else30/60/image100250; empty628 remains unused and its
  gavin/iris postattack is excluded. Clock/Exit claims remain isolated-site scope.
- Artifact11480773914 SHA256
  b337151000d22d641cd736fc67f2ceceb63989443fe43e9d960c3fa107383d3c.
  Report digests and exact profiles in STONEAGE-BECOMEPIG-NATIVE-REFERENCE-ACCEPTANCE-R1.json.
  No original C, raw OPTION, descriptions or assets committed.
- OPEN: whole clock/recipients, Exit/compliance/equipment/ride, attack ordering,
  historical build/PRNG/ordinal and runtime/persistent/coordinator composition.
  Zero capability promotions. Bounded closure supersedes prior native-OPEN only
  within witnessed domains; no feature dating or JSS/Taiwan-v1 inference.


### SRC-BECOMEPIG-CLOCK-CONTROLS-R1 — bounded native ownership acceptance 2026-10-07

- Exact input7e5af49d21be40bd7d75c19c31263e39fd0b6a15/tree
  a591b475fab081fc1f18ae2f5a68b7e6cd47fc0d passes Action37621151399/job
  112791457781.22 tooling regressions and24 structural gates/profile; clean3
  pinned source trees with exact network/retained-control hashes. O0/O2+
  nonrecovering UBSan419904 sequential actor/state/call/clock snapshots.
- gavin/iris original connection loop includes default service exclusions and
  has no character deduplication. Bismarck's original pig sites are owned by
  valid player-array slots and independent of the later connection loop. Exact
  condition/clock sampling/cycle wrap and site order execute in the retained
  control projection. Full unrelated subsystem bodies are omitted; compliance
  is stubbed. Controlled battle/world switch does not execute original Exit.
- Previous isolated timer/Exit report5364 comparisons reproduces unchanged.
  Derived writebackfc1d619294c14b62985509f5e50fd052ee21c842; artifact11481838073
  SHA256d51ae22ba22cd0b231e3b736cb21317209499ad1fd9c91adec630afc0fe5654b.
  Report SHA256 and exact-control hashes: STONEAGE-BECOMEPIG-CLOCK-ACCEPTANCE-R1.json.
- Source C remains transient. No whole-server/executable or original deployment
  configuration claim; no runtime promotions. Full Exit/compliance/equipment/
  ride, cross-subsystem timers and ordered attack composition remain OPEN.


### SRC-BECOMEPIG-RESTORATION-CALLERS-R1 — bounded complete-function acceptance 2026-10-07

- Exact input515fc09b77a36c5c1ea46918c7abc24085c77034/tree
  ce80e0bfa2336d834f1c61e4f5c902849b0dd563 passes Action37624829843/job
  112803823511.29 regression/domain/identity tests;3 source profiles24 structural
  gates each. Complete char/char.c and battle/battle.c hashes plus actual-default
  preprocessed function hashes in STONEAGE-BECOMEPIG-RESTORATION-SOURCE-DOMAINS-R1.json.
- Whole original _CHAR_complianceParameter/_BATTLE_Exit execute, including nested
  original compliance caller, at O0/O2 GNU99+nonrecovering UBSan165900 cases.
  Original source remains transient. Return/state/entry/ordered-call traces agree
  with oracle; previous419904 clock snapshots reproduce unchanged.
- Fixed dependency witnesses, symbolic field/ABI and synthetic static/dynamic
  ride/equipment results remain explicit. This does not execute original helper
  bodies, actual tables or active bad-status systems. Inactive follow/profession/
  mail/ticket and valid live owned pet define the bounded PvE player-exit slice.
- Derived writeback9176fd1e88940f35541412329f30a8afefcebb9b; artifact11483293292
  SHA256949c5a2ce1fdef10e66eb8f8fbcf346798c30fcaae70062dedf883e1e8f013cc.
  Exact acceptance/report digest: STONEAGE-BECOMEPIG-RESTORATION-ACCEPTANCE-R1.json.
  Zero runtime promotions; helper/order/cross-subsystem and broader Exit domains
  remain OPEN. No historical executable, feature date or JSS/Taiwan-v1 inference.


## 2026-10-07 — BecomePig original bad-status dependency domains R1

- DERIVED/SOURCE: same pinned gavin/iris/Bismarck source descendants as accepted
  restoration. Additional identities: battle/battle.c original BadStatusAllClr,
  battle/battle_event.c selected StatusTbl/MagicTbl, include/battle_event.h enum/
  macro limits and include/version.h. SHA256/default-feature metadata in
  research/recovered/STONEAGE-BECOMEPIG-BADSTATUS-SOURCE-DOMAINS-R1.json.
- Bound original function/table execution composed with complete compliance/Exit;
  actual tables default-selected, lengths independently checked against original
  loop limits. Actual BadStatus work/flag/pet-counter writes and property null
  ordering; controlled symbolic ABI/property storage/copy/construct/stat/equipment/
  ride/network dependencies. Original bytes transient only. No runtime promotion.
- OPEN source inspection leads: char/char_data.c equipment lookup has five-column
  rows and category>5 guard, leaving category5 matching-row undefined access.
  char/char_base.c static ride rows and default-active new-ride helpers/tables are
  next bounded batch. No raw table rows committed or historical deploy inferred.
- Spec specs/STONEAGE-BECOMEPIG-BADSTATUS-COMPOSITION-R1.md; gate
  .github/workflows/validate-stoneage-becomepig-badstatus.yml. Remote acceptance
  pending; earlier restoration/clock reports must reproduce byte-for-byte.


## 2026-10-07 — Original bad-status composition R1 remote acceptance

- CLOSED_BOUNDED original default BadStatusAllClr +actual status/magic maps +whole
  original compliance/Exit composition; controlled dependencies retained as in spec.
  Inputfad7a77ad6b9c1286e0ce574eec18e0587ca0a1d/tree53e88906c0710d7886de0c5bfcc774ea76e3a427.
  Action37628605267/job112816717818 SUCCESS;38 tests,24 source gates/profile,
  373272 native comparisons. Prior165900 callers/419904 clock snapshots reproduce.
- Derived writeback50c7cad1be9a0e07232482079a0101de852eec6b/tree
  ffa152fb0e330fc6dd3ef6a2578292152bcbef34. Report SHA256
  417b12b7c95874b481f31371cb8dab8dadc84d08d747e5ed042e14efe9b77e39
  matches local byte-for-byte. Artifact11485057422 SHA256
  cb999a01877eaa39eaabba312e591bbca88a8339205501a385c8e652e9f01d3d.
  Receipt research/recovered/STONEAGE-BECOMEPIG-BADSTATUS-ACCEPTANCE-R1.json.
- Prior pending scope superseded by remote evidence. Actual equipment/ride maps,
  property construction/stat bodies, attacks/timers/ownership/historical builds
  and runtime remain OPEN. Pressure2486 and BecomePig promotions0 unchanged.


## 2026-10-07 — BecomePig actual appearance lookup source domains R1

- DERIVED/SOURCE: same clean pinned gavin/iris/Bismarck descendants. New source
  identities cover char/char_data.c equipment-image map/helper, char/char_base.c
  static/default-active dynamic ride tables/helpers, include/char_base.h,
  include/anim_tbl.h, include/item.h and include/version.h. Receipt:
  research/recovered/STONEAGE-BECOMEPIG-LOOKUP-SOURCE-DOMAINS-R1.json.
- Selected helper and numeric physical-table hashes pin source order, duplicate
  rows, static declared bound and C zero-fill. gavin/iris widths12/10; Bismarck
  _NEW_RIDEPETS false while _RIDE_CF true; inactive branches not executed/promoted.
  Bismarck static296 declaration has104 initializers+192 zero rows. Equipment
 67/67/76 rows and64/64/69 unique keys; duplicate keys currently nonconflicting.
- Bounded original helpers/actual maps compose with complete compliance/Exit and
  BadStatusAllClr/actual status maps. Original bytes remain transient. Symbolic
  ABI/property/stat/item/network/ownership fixtures retain explicit boundaries.
- Original matching-row category5 equipment read remains undefined/excluded;
  source guard unchanged. Spec specs/STONEAGE-BECOMEPIG-LOOKUP-COMPOSITION-R1.md;
  .github/workflows/validate-stoneage-becomepig-lookup.yml remote gate pending,
  requires old badstatus/caller/clock reports byte-for-byte.0 runtime promotions.


## 2026-10-07 — Actual appearance lookup R1 remote acceptance

- CLOSED_BOUNDED original selected equipment/ride helpers/tables and complete
  compliance/Exit/BadStatusAllClr+actual status-map composition. Input
  164b0df7f3effd4667567a460d866ac7adf5a793/tree5619b5c3e67f7347a2f960460c7bf6ab319cc684;
  Action37632716905/job112830873632 SUCCESS,50 tests,24 source gates/profile,
  322872 original lookup/table/composition comparisons O0/O2 GNU99+UBSan.
- Prior373272 badstatus/165900 caller/419904 clock reports reproduce unchanged.
  Writeback3e14ce16be0707b99716b6268770749b7b13a9f1/tree4d00e56529d0cad83230f22b6ff0aebcf1ccaf5f.
  Local/remote report SHA25697c51a7bc9c1afce31511ceb95fcbb556c907ebeef36da7cf9e6e2d917b143a4.
  Artifact11486732542 SHA256d5956cfa8de4051c2e5325ce82dd13f670572e2fb4274f6996479106b52eba5d.
  Receipt research/recovered/STONEAGE-BECOMEPIG-LOOKUP-ACCEPTANCE-R1.json.
- Pending superseded in declared lookup/complete-caller scope only. Actual stat/
  property bodies, broader ownership/feature domains, original attack/timer order
  and historical build/runtime remain OPEN.0 promotions; pressure2486 unchanged.


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


## 2026-10-09 — Original Exit/world/item lifetime source gate LOCAL PASS; remote PENDING

- Same3 clean descendant pins, complete original Exit and accepted lifetime
  helpers, plus original item/item.c validity/end, char/char_base.c player count/
  item accessor/slot guard, char/char.c warp, object.c coordinate accessors and
  map/readmap.c linked-list movement. Derived file/function identities in
  research/recovered/STONEAGE-EXIT-WORLD-ITEM-SOURCE-DOMAINS-R1.json; original
  sources remain transient outside repo. Allocator body is hashed/static-only.
-42,336 comparisons at O0/O2 GNU99+UBSan,99 regressions,12 native mutations;
  previous196,056/55,350/576/263,268 reports byte-identical. New complete report
  SHA25654ab876083faac9e87da83a6ce459b5edaa59fcb03a725aeb131ae9c9b7636ab.
- Proper player/pet/other partitions, valid object index, compatible symbolic
  structs, synthetic maps/floor validity/encounter and network/message collectors.
  Exact Exit destination asserted; cross-floor passes7001/41/6 unchanged;
  same-floor control substitutes floor. FACT limited to executable witness,
  not original map data/build/JSS/Taiwan-v1 or natural enemy state. Item scans
  carried live-player references only; warp success does not imply map success.
- Next exact-input remote acceptance, then template/enemy-init/allocator/reuse
  execution and natural ticket/object provenance. Pressure unchanged,0 promotions.


## 2026-10-09 — Original world/item source gate remote ACCEPTED

- Exact inputfef1abd090fe6804453b7e0af264bdd54921cd9e/tree
  33b767f45e791d77cc8b56e015709f4646a064c6 passes Action37878819171/
  job113653500431:99 regressions,42,336 native comparisons (3 x7,056 xO0/O2
  GNU99+nonrecovering UBSan),84,672 Exit calls,12 native mutations rejected.
  Prior196,056 Exit-ticket,55,350 watch,576 lifecycle and263,268 Exit-mode
  complete reports reproduce unchanged. Full ordered remote report equals local;
  all workflow cmp gates passed. Report SHA256
  54ab876083faac9e87da83a6ce459b5edaa59fcb03a725aeb131ae9c9b7636ab.
  Artifact11593391695 digest
  sha256:ec269f379aba2a165c7c581b5d49ab6e671ecb37ccf91b54d317dc0d9e17b415.
  Receipt research/recovered/STONEAGE-EXIT-WORLD-ITEM-ACCEPTANCE-R1.json.
- FACT within bounded original nonplayer Exit/item/warp/object/map composition:
  item-end protects live-player carried aliases but ignores pool-only/unused-player
  aliases. gavin/iris expired synthetic enemy ticket can move retained object/map
  chain after character invalidation while actor coordinate/encounter writes
  fail. Bismarck Exit guard skips this route. Warp may return true after failed
  map movement with coordinates prewritten. Bismarck old-floor search recovers
  tested misplaced nodes; middle-node removal/tail insertion retain neighbors.
- Original complete item validity/end, item accessor/slot guard, full warp,
  unchecked object accessors and full map movement execute at clean source pins.
  Proper fixed partitions, valid object index, symbolic ABI, synthetic44x8 maps,
  floor/coordinate/encounter/network/message hooks controlled. Cross-floor uses
  original7001/41/6; same-floor controls replace floor only. Synthetic enemy
  tickets/ownership/object state not claimed naturally reachable. Allocator
  zero+template-copy is static-only; retained dead-slot fields do not prove reuse
  inheritance. Direct invalid-object/Bismarck invalid-actor warp not executed.
- Local PENDING superseded only in stated domain; all earlier records preserved.
  Pressure2486=2465 closed capability+18 OPEN+3 historical UB,zero promotions.
  Highest priority next: execute default character template/enemy creation/init
  callbacks/allocator/reuse and establish natural ticket/object provenance. Then
  remaining ownership/stats/property/timer/matched-player/watch creation/multi-
  actor before typed631/635 persistent/coordinator admission. Original map data/
  build/ABI/executable/network/JSS/Taiwan-v1/runtime remain OPEN; no engine/content
  transition. Protocol section10 ongoing authorization covers acceptance writeback.


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


## 2026-10-09 — Actual original default template/table/header layout LOCAL PASS; remote PENDING

- Fresh remote main d35619a78ac266ab0bb28f539ccc98b7e617e478/tree
  46e770c1a371146a592b2897fd67b69bcd7c4c22; latest Action37880212015 success.
  Continued recorded actual-template/enum/layout priority at same3 clean pins.
- Actual defaultPlayer.h, complete53-row default table and original Char/enums/
  feature/animation headers plus unchanged getter execute; no symbolic structure
  or replacement template.228 cases/profile/optimization, two calls/case:
  2,736 getter calls at GNU99 O0/O2+nonrecovering UBSan.116 regressions;
  24 semantic native mutations rejected. Six predecessor full reports required
  byte-identical. Spec STONEAGE-DEFAULT-TEMPLATE-R1.md and source/validation receipts.
- FACT bounded: all table rows share player; matched/fallback image type write
  overwritten by data-prefix copy. Ticket/start/object/callback storage zero from
  all tested dirty destinations; FD-1, chatroom-1 only gavin/iris. Original data
  counts162/159/131; copy boundaries85/84/87; work counts317/316/214.
- Actual compiler preserves8/10 excess initializer warnings gavin/iris. Static
  pig/image values -1/100250 for them,100250/0 Bismarck under active positional
  enum layout; Bismarck comments are not compiled field-position proof. All pig
  fields beyond copy boundary, getter outputs0/0. No released-build defect claim.
- Native comparisons include full object representation against separately built
  expected storage and every data/work/flag element; actual header capacities.
  LP64 host size/offset observations, current source feature configuration and
  controlled destination fills; no original ABI/build claim. No natural object
  ownership/sentinel claim from work0. Original C remains transient outside repo.
- Remote acceptance PENDING. Pressure2486=2465 closed+18 OPEN+3 historical UB;
  zero promotions. Next exact-input Actions, then complete enemy creator/init/
  helper/data/function provenance and natural ticket/object states, followed by
  full Exit-to-reuse. Remaining actor/watcher/typed631/635 and JSS/Taiwan-v1 gates
  OPEN; no engine/content transition. Protocol section10 authorization applies.


## 2026-10-09 — Actual original default template/table/header layout remote ACCEPTED

- Exact input e180903ef2c1d06dfb44241419654d620b5c2c85/tree
  8c130bc9d26a762353cf1d25dd049f50ddad3335 passes Action37881477702/
  job113661909887:116 regressions,2,736 getter calls at GNU99 O0/O2+
  nonrecovering UBSan,24 native semantic mutations rejected. Six predecessor
  complete reports unchanged; all seven cmp gates passed. Complete ordered remote
  report equals local bytes, including per-profile full-stream semantic hashes.
- Actual defaultPlayer/table/Char/enums/features/animation headers and complete
  getter now execute in bounded current-profile LP64 witnesses. Source warnings
  8/10 excess initializers retained; Bismarck positional pig/image100250/0 differs
  from comment labels. Getter zeroes tail pig/image,ticket/start/object/callback
  storage; image-type assignment overwritten by player prefix. Source-profile
  findings only, no original released-build/ABI/JSS/Taiwan-v1 claim.
- Acceptance receipt STONEAGE-DEFAULT-TEMPLATE-ACCEPTANCE-R1.json; report SHA256
  facfe62106ca3be1a9a800b5e33afcc14bf582a65e2dc93d2607d6c0be076c53. Artifact11594461395 digest
  sha256:2217b0c389e897bb15b19195709df88e0d822df17384217d87ed24234df710bc.
  Artifact archive not independently downloaded; ordered job output and successful
  report cmp gates verified. Tested code unchanged; earlier histories preserved.
- Supersedes local PENDING only in this scope. Pressure2486=2465 closed capability
  +18 OPEN+3 historical UB;zero promotions. Highest priority next: full original
  enemy creator/init/helper/data/function provenance and natural ticket/object
  states, then full Exit-to-reuse. Remaining actor/watcher/typed631/635 persistent/
  coordinator and original build/JSS/Taiwan-v1 gates OPEN. No engine/content
  transition. Protocol section10 ongoing authorization covers publication/Actions/
  acceptance integration without repeated confirmation.


## 2026-10-09 — Ordinary enemy creation original-function source gate R1

Same three pinned descendants/current active headers. Derived receipts
STONEAGE-ENEMY-CREATION-SOURCE-DOMAINS-R1.json, VALIDATION-R1.json and NATIVE-R1.txt;
spec STONEAGE-ENEMY-CREATION-R1.md and validate-stoneage-enemy-creation workflow.
Actual creator/template/allocator/empty-name lookup/rank/experience/full stat and
empty-inventory composition execute; all source/function/transitive header hashes
pinned. Synthetic records and scripted Rand/positive partitions/empty registries
are controlled inputs; unexecuted external dependencies abort if reached. Original
source remains transient.27,840 primary calls,126 regressions,24 mutations rejected,
seven previous reports unchanged; local PASS, remote PENDING. Zero ticket/start/
object after ordinary creation is bounded evidence, not natural loaded content or
ownership/sentinel proof. Real loader/registration, special/equipped/callback paths,
Exit-to-reuse, original build/ABI/JSS/Taiwan-v1 remain OPEN;zero promotions.


## 2026-10-09 — Ordinary enemy creation source gate remote ACCEPTED

Exact input a6bcde889b6e4f2279cc6d637662d2f42fab0156/tree
80e9732c997ff82ab39c4cffde12890644c5a300 passes Action37883409372/
job113667962896:126 regressions,27,840 primary calls,24 rejected mutations.
Seven predecessor full reports and complete new ordered report match local bytes;
eight cmp gates pass. Receipt STONEAGE-ENEMY-CREATION-ACCEPTANCE-R1.json;
report SHA2561e4c78ebc12309baa6905eaa63626b21180cdce6e75c17dafb980e39998502d3.
Artifact11594489097 digest sha256:8db2166f71b415fd7a81ea383e7c6b49b2ac01aefa54e691b5fc4d650ffa80e7;
archive not independently downloaded. PENDING superseded only for ordinary
unequipped/synthetic-master/current-profile LP64 domain. Loader/ownership/special/
equipment/callback/full Exit-to-reuse/original build/JSS/Taiwan-v1 stay OPEN;
zero promotions, tested code unchanged and original source remains transient.


## 2026-10-10 — Original master loaders and preserved birth source gate R1

STONEAGE-ENEMY-LOADER source/validation/native receipts and spec/workflow. Same-pin
Gavin setup.cf SHA25613a52f3b66821fd74eacdd848356154139a63b0b68d2cfc4214c9356e106d9b0 selects
complete enemybase1.txt SHA2567ffb17b161c9d66fcbbaa4e8bcf48d1a9a56223b35770074ae9c3401d270f5d7 and
enemy1.txt SHA2567e06e1eff0abdf833c0fba2ce57de25170b9fad508237e3f535f7a40044e01ff.
Actual Gavin loaders and Bismarck callback/file-helper loaders plus original
pool/tokenizer/setter/link/level helpers execute. Bismarck use is cross-profile
input only, not its own historical-data claim; compiled template fields50/49.
Iris original loader/Windows-conversion identities and three-profile object/battle
caller body hashes recorded STATIC/OPEN. Original source/data remain transient.
7,284 template+11,756 enemy full-record comparisons;49,024 selected preserved
ordinary births,139 regressions,12 rejected native mutations; eight old reports
unchanged. Local PASS, remote PENDING. Born ticket/start/object0 is bounded
source-input evidence, not ownership/sentinel/original release/JSS/Taiwan-v1 proof.
Zero runtime promotions; registration/occupied slot0 and full Exit-to-reuse next.


## 2026-10-10 — Original master loader and preserved birth source gate remote ACCEPTED

Exact input1d0c11cd6b7b5134e9cd39014092e9a14a591085/tree
c1fe0c01cd4809c040dd983f0eb6c521bd6deb48 passes Action38021001375/
job114121749879:139 regressions,7,284+11,756 full loaded-record comparisons,
49,024 ordinary births and12 rejected semantic mutations. Eight old full reports
unchanged; full new ordered report matches local bytes; nine cmp gates pass.
Receipt STONEAGE-ENEMY-LOADER-ACCEPTANCE-R1.json; report SHA256
ce1e52eee5169fc123f8b1c71c252908bedd1f42067f87b4772b2d3f7f596538. Artifact11658451381 digest
sha256:8ffca12b92ebff80d0a29ee9d039082bf5baf2269be4ec8fe262cc8e7ebedcf9;
archive not independently downloaded. PENDING superseded only for Gavin own
configured data/Bismarck cross-profile input/current-header LP64 witnesses.
Iris conversion, ownership/occupied slot0/full Exit-to-reuse/original release/
JSS/Taiwan-v1 remain OPEN;zero promotions. Tested code unchanged and original
sources/data remain transient; earlier records preserved.


### 2026-10-10 — Actual object registration beside preserved ordinary births R1

- Tool/spec/derived receipts: stoneage_object_ownership_audit.py,
  STONEAGE-OBJECT-OWNERSHIP-R1.md and SOURCE-DOMAINS/VALIDATION/NATIVE-R1.
- Same fixed descendant pins and Gavin configured preserved bytes as accepted
  loader gate; Bismarck cross-profile witness. Actual world constructor/object
  allocator/owner search/map list helpers/empty-registry Char release execute with
  real original headers. Complete source/body/declaration/header closure hashes
  recorded. No original C/headers/data/assets committed.
- FACT bounded LP64: live slot0 belongs to world0/1; enemy4's zero object work
  is not ownership. Original owner search4=-1. Enemy character reuse preserves
  world object/list state. Char-only world release retains object/list; explicit
  object release unlinks and subsequent reuse appends at tail. Original object
  cursor is retained, alternating owners naturally across controlled cycles.
-49,024 cycles,98,048 births,147,072 world successes,49,024 rollbacks,441,216
  named stages;152 regressions,10 mutations rejected, nine unchanged prior reports.
  Original pool/map list allocation used; detached-node freeMemory collection,
  walk predicate/watch collector are adapters, not original reclaimer/notifications.
  Only five initialized Object fields observed; no all-byte/all-birth-field oracle.
  Remote acceptance PENDING. Actual battle entry/full Exit/reuse, original reclaim/
  bootstrap/Iris conversion/original ABI/JSS/Taiwan-v1 remain OPEN;zero promotions.


### 2026-10-10 — Object registration/nonownership R1 remote acceptance

- Tested adae57319685b272c73ab431d72128fe2a40af3a/tree
  2a8fef42cffafcb6f0e4b03e1192b542fc9fb0bb accepted by Action38022136836/
  job114125208055.152 regressions,441,216 named stages,10 safe mutations;
  nine predecessor full reports unchanged, all ten cmp gates pass. Full ordered
  report matches local7f426e53b44afea3026dd8eefa2d575ba5e2a2b3562caf6c668e1f335528d9bd.
- Receipt STONEAGE-OBJECT-OWNERSHIP-ACCEPTANCE-R1.json records report blob,
  artifact11657904198/digest and exact input. Artifact archive not independently
  downloaded; ordered logs/report cmp gates verified. Tested code unchanged.
  Accepted only bounded descendant/source/header/map/adapter scope; no all-byte/
  all-birth-field/freeMemory/bootstrap/full-entry-Exit/JSS/Taiwan-v1 promotion.


### 2026-10-10 — Actual-header preserved enemy Entry/Exit/reuse source gate R1

- STONEAGE-ENEMY-ENTRY-EXIT source/validation/native receipts and spec/workflow;
  same accepted pinned descendants/Gavin configured bytes, Bismarck cross-profile
  only. Original Entry/complete Exit/bad-status tables/party/checked flag/Char/item
  empty-registry release functions and actual header dependency closure pinned.
- FACT in ordinary enemy composition: real INIT1/FINAL6, slot4 destroyed/reused,
  dead guards error6, world objects/players/map links retained. Gavin postdestroy
  clock/zero-ticket tail vs Bismarck liveness guard preserved. Nonparty/no-equipment/
  empty-callback scope; controlled battle holes/fixed clock plus inherited world
  walk/watch/reclamation adapters; other actor/network/warp/profession paths trap.
-49,104 cycles/98,208 births/196,416 complete work-delta stages/785,664 guard
  rejections;164 regressions,12 mutations,ten unchanged predecessor reports.
  Differential work oracle from captured birth, not all-field birth oracle.
  No original C/headers/data committed. Remote PENDING; higher-level battle
  bootstrap/Finish/other actors/original reclaimer/ABI/JSS/Taiwan-v1 OPEN;0 promotions.


## 2026-10-10 — Enemy Entry/Exit/reuse accepted derived evidence

- STONEAGE-ENEMY-ENTRY-EXIT-ACCEPTANCE-R1.json records tested
  178356adaed50d1bd6c8b170eac297259895d6af/tree
  718b7227d6b72954ae6cbb9ce969077eb3f80778, Action38023653829/
  job114129802080,164 checks,11 complete report cmp gates and ordered-log match.
- Native report SHA2569765e8ebdaa7861e12887fe6ba73a5f4a46eb3d12b92ffe358bd8f0af9cd6f70,
  Git blobfa995217a9fa95f0dc1a5028f9ded776bd72bce4.
  Artifact11659251039 archive independently downloaded and digest verified:
  sha256:1196cbf9c6dc9534e2d86a64e676a28a0b3f8a91795fff646c2922f52bb675f2;
  sole report member equals local bytes. No original C/headers/master data published.
- Existing pinned descendant/source/header/table/input domains and controlled
  adapters unchanged. Accepted ordinary enemy composition; higher-level battle
  creation/bootstrap/Finish, other actors, original reclamation/Iris conversion/
  original ABI/build/JSS/Taiwan-v1 remain OPEN;zero runtime promotions.


## 2026-10-10 — Battle pool/rollback/enemy Finish derived source domains

- STONEAGE-BATTLE-POOL-SOURCE-DOMAINS-R1.json nests accepted actual Entry/Exit
  identity, pins12 complete original battle functions, private counters, RS_LIST,
  exact file-local excluded signatures and transitive original headers.
  Source roots retain existing Gavin/Bismarck pins; same-pin Gavin master specimen
  only, Bismarck cross-profile bytes; Iris Windows conversion OPEN with no adapter.
- Independent tools.stoneage_battle_pool_audit/test/workflow/spec plus validation/
  native receipts. Report SHA256421c5492f6d9352b5be263edd15eb93240c1d5499ec7d5f594c9b2c489c838f7.
  Original C/headers/master files transient; controlled encounter/field/fd/birth
  trace/RNG/clock/inherited world collectors disclosed.174 regressions/10 safe
  mutations;24,528 rollback/24,512 enemy Finish cycles/85,836 births.
- Full original creation/Finish bodies compiled, limited executed paths only;
  successful player/party creation and player/pet profit remain OPEN/trapped.
  Arena bootstrap is not full server bootstrap; original reclaimer/ABI/JSS/
  Taiwan-v1 OPEN. Remote PENDING,0 promotions;11 predecessor report gates required.


## 2026-10-10 — Accepted battle arena/rollback/enemy Finish receipt

- STONEAGE-BATTLE-POOL-ACCEPTANCE-R1.json identifies tested
  8178210c4babe0048a58f2297cc65482f8f3da18/tree
  50875fa70d23025e61375906eb1cc425a510eefe, Action38024968843/
  job114133769164; all21 steps,174 regressions/12 complete cmp gates succeed.
- Report Git blob64810e2fa8d7e4c7356070c8c5bcc394abfeeec9, SHA256
  421c5492f6d9352b5be263edd15eb93240c1d5499ec7d5f594c9b2c489c838f7.
  Artifact11659098098 archive independently downloaded and digest verified:
  sha256:59a25943bf0ae998f81d390ff8eb3eb5d680251b25657368f0c2768a36293a7c.
  Sole report member and complete ordered log equal local bytes.
- Original source/header/master bytes remain transient; accepted source pins,
  harness/workflow/tests/report unchanged. Bounded failed-creation cleanup and
  enemy-only Finish, explicit input/world collectors; successful player/party
  creation and original reclaimer/full-server/ABI/JSS/Taiwan-v1 remain OPEN.


## 2026-10-10 — Derived original solo player successful battle evidence R1 (LOCAL PASS / remote PENDING)

- Source pins Gavin1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56 and
  Bismarck999ffdf1d220ec6666eb65339180689c9caf1876; unchanged preserved Gavin
 1816-template/2935-enemy bytes,1532 selected records/RNG4. Bismarck input is
  cross-profile, not historical local content. Iris encoding remains OPEN.
- tools/stoneage_player_battle_audit.py, tests/test_stoneage_player_battle.py,
  specs/STONEAGE-PLAYER-BATTLE-R1.md; SOURCE-DOMAINS/VALIDATION/NATIVE-R1 derived
  files and validate-stoneage-player-battle workflow. Hashes/actual function and
  header closure/typed collector signatures/abort traps/input receipt; no
  original C/headers/master redistribution. Lua prototype declarations normalized
  only for typed unreachable traps; original FindLua/EquipEffectFunction intact.
- Successful solo CreateVsEnemy/actual player Entry/complete healthy Exit and
  original compliance/enemy cleanup/reuse:24,512 cycles,49,020 enemy births/
  Exits,73,536 player/147,060 enemy work stages;10 safe mutations,184 units,
 13 report gates. Native SHA256 2bd5cbeb7170001e6231f463c031cbdb55bf4072262789d99116829d229c6c01. Remote PENDING.
- Explicit baseline preparation/restoration, descriptor7/network/status/skill/
  monitor/receive-time/watch/time/encounter/field/RNG/world adapters. Original
  Bismarck empty Lua registry guard executes; scripts/nonempty search trap.
  Party members/pets/profit/Init/TaskLoop/nonempty items/watchers/callbacks,
  original reclaimer/server/ABI/Taiwan-v1 remain OPEN; pressure unchanged,
  zero promotions. Supersedes no earlier records.


## 2026-10-10 — Solo player battle evidence R1 REMOTE ACCEPTED

- Tested90c41828c9ba6792981b37600905900746e793ab/tree873c2bf31cf8ee61ab180381af20c4b40d6c166e;
  Action38026431963/job114138142010 all22 steps success,184 unit checks and
 13 full-report cmp gates; prior12 reports unchanged. Accepted solo24,512,
  enemy births/Exits49,020, player/ enemy work stages73,536/147,060, mutations10.
- STONEAGE-PLAYER-BATTLE-ACCEPTANCE-R1.json persists run/job/HEAD/tree/report/
  artifact identity and boundaries; validation/spec accepted. Native SHA256
 2bd5cbeb7170001e6231f463c031cbdb55bf4072262789d99116829d229c6c01;
  artifact11660546530 independently downloaded,963-byte ZIP SHA256
 ef127f6b6d59f2a22c874f0b38c5b1605bbd351bd2a99fb2aa311f26c5223506,
  sole STONEAGE-PLAYER-BATTLE-NATIVE-R1.txt member equals local bytes.
- Source identity links accepted pool pins by canonical hash; original function/
  file/header/Lua declaration/typed collector signatures remain pinned. Tested
  tool/test/workflow/pins/report unchanged; original C/headers/master transient.
  No original network/monitor/reclaimer/full server/actual Lua claim; controlled
  healthy solo baseline restored each case, explicit typed collectors retained.
  Actual party/pet/profit/Init/TaskLoop/Iris/ABI/Taiwan-v1 remain OPEN. Pressure
  unchanged,0 promotions. Earlier source records preserved; protocol10 applies.


## 2026-10-10 — Pinned party/pet battle entry source gate accepted

- Original selected C code examined transiently from exact pinned Gavin and
  Bismarck descendants; preprocessed BATTLE_PetDefaultEntry,
  BATTLE_PartyNewEntry and BATTLE_ClearGetExp source fingerprints and file SHA256
  are produced in derived artifact. Script/test/workflow/spec in branch
  agent/party-pet-preflight-r1-20261010, exact tested commit
  7850d55eb02226e43adbf5b5710c6d6a2f1cac9c/tree
  ab95e66176a2a3297775b0fcafeea11d46a7acaf.
- Action38027458741/job114141235353 success, seven negative/positive unit
  guards and two source-profile checks; artifact11660457492 metadata digest
  sha256:96e6f17f41a939393f1586ca705d4bdd3dc22a9aa43467687060403606e5eef7;
  archive not independently downloaded. No original source is published.
- Bounded source FACT: Gavin fixed party capacity and nonzero battle-mode guard;
  Bismarck dynamic getPartyNum and NONE/FINAL eligibility; selected default-pet
  retrieval/validity/death/HP guards, wrapper zero return independent of
  successful pet slot insertion; GETEXP clears across valid owned pets.
  Requires actual runtime occupancy verification. HYPOTHESIS cannot be promoted
  to original Japanese/Taiwan-v1 semantics merely from descendants.
- Receipt STONEAGE-PARTY-PET-SOURCE-PREFLIGHT-ACCEPTANCE-R1.json.
  Successful populated party/pet admission and Exit, profit, Init/TaskLoop,
  historic ABI/1999-JSS/Taiwan-v1 remain OPEN; no runtime promotion.


## 2026-10-10 — Native execution of three unmodified party/pet entry functions

- Exact pinned Gavin/Bismarck original body trio ClearGetExp,
  PetDefaultEntry and PartyNewEntry is extracted transiently into
  controlled C test doubles with explicit synthetic Char roster, entry
  admission and message flush. Original body raw/file hashes preserved
  in GitHub Actions stdout, no original C/headers/master committed.
- Tested0e3eb5aee2ffb7422eda405d644a64d98a7faa9d/tree
  393a4e9d7f3e6fda22b4b6fa3a0c074cc480d2d3;
  Action38028052045/job114143010060 succeeded with11 unit guards,
  13 scenarios per profile on both O0/O2 nonrecovering UBSan; exact native
  traces agree across optimizations. Artifact11660498546 metadata
  SHA256 173aa43eec1ebf47bda699aa02da90c3299698011dc8b9894f8b0359ba867df7;
  archive not independently downloaded. Earlier Action38028006060 first
  attempt failed during original Bismarck header-path processing; corrected.
- FACT **only** as isolated original-function behavior in controlled
  synthetic actor stubs: leader/party/selected healthy pet call order,
  profile FINAL-mode difference, default selected pet vs owned other pet
  experience clear, invalid/dead/zero HP guards and masked pet entry error.
- Runtime gate receipt STONEAGE-PARTY-PET-ENTRY-FUNCTION-RUNTIME-ACCEPTANCE-R1.json.
  Full real-header integrated populated party/pet CreateVsEnemy, full Exit/
  profit/Init/TaskLoop remain OPEN. No Taiwan-v1/JSS1999/history promotion.


## 2026-10-10 — Real original-header actual party and selected owned pet battle admission

- Action38029828829 job114148235571 success: tested original-body
  2d8e5c90e44589f3475771909231e8c69adfcefc/tree
  2f4f05c2ed352fdb40467f99ea529a072f63d5f0.
  14 regression checks passed. Both exact pinned Gavin1f90cb6 and
  Bismarck999ffdf1 live player0/member1/pet2 CreateVsEnemy O0/O2
  original-header executions with UBSan agree. Original pet
  CHAR_initCharOneArray, actual BATTLE_NewEntry and Index2No confirm
  pet at owner back-row slot5/bid5, original GETEXP and ownership.
- Controlled health/roster/descriptor/watch/world/master/network adapters
  explicitly bounded. No joint original Exit/Finish/profit claim and no
  historic JSS1999/Taiwan-v1 claim. Transient original bytes not
  redistributed. Artifact11662126347 SHA256 metadata
  3570fed9a53d96045f35c076f1dd02df90e74339c1a2c71a3beb0f3918f772be
  (not independently downloaded); receipt
  STONEAGE-PARTY-PET-REALHEADER-ACCEPTANCE-R1.json.


## 2026-10-10 — Real-header descendant battle Init execution gate

Repository evidence:
- CI source/test input1c0c27de29862e56b0d89370069b3c34174954d6,
  tree b38771da8453e8040196c7edab84cfd0c6b89574,
  action38033067497/job114157832582 SUCCESS (10 steps,18 regressions).
- Exact external source commits: Gavin1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56
  and Bismarck999ffdf1d220ec6666eb65339180689c9caf1876.
  Source/headers/master recovered only in CI ephemeral temp checkout.
- Source originals extracted: BATTLE_Init/SurpriseCheck/PreCommandSeq,
  CharaBackUp, IsCharge, AllCharaCWaitSet, TurnParam, AttReverse.
  Four original Init/Exit cycles per profile/optimization, O0/O2 UBSan
  agreeing, no redistribution of original bytes.
- Controlled two outbound packet collectors; no native packet payload
  or transport proof. Bismarck Lua start feature compiled out.
  stdout traces SHA256 Gavin
  362fcd9ee1d3c1536bc1950dd8b7121d53c089ffcd614bfc6ccc0ada5e08bcfe,
  Bismarck4e3acec05e99f92bdff7e606b90e050ced7833b1a495693f4f6be24ce9990807.
  Artifact11663147028 SHA256 metadata only
  2b8ce42870686e0fba254f0db73734ff78d0fe21538d856c2d102f1683f7573a;
  ZIP content not independently downloaded. Acceptance receipt
  STONEAGE-PARTY-PET-ORIGINAL-INIT-ACCEPTANCE-R1.json.
  Historical JSS1999/Taiwan-v1 semantics remain unproven.


## 2026-10-10 — Actual BATTLE_Loop INIT dispatcher source evidence

- Remote tested source/test/workflow SHA
  c1649d27036c8f7e27b680d871989d270b48dec9,
  tree5a3b3563469a7ff3cf9b79249f7dcc0b0da46b21,
  Action38033745806/job114159804380 all10 steps SUCCESS and12 regressions.
- Original pinned descendant Gavin1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56,
  Bismarck999ffdf1d220ec6666eb65339180689c9caf1876,
  exact original BATTLE_Loop and original Init chain with original headers
  GNU99 O0/O2 nonrecovering UBSan. Four INIT-only calls per profile/opt,
  total16, profiles' complete output agrees across O0/O2.
- Trace SHA256 Gavin362fcd9ee1d3c1536bc1950dd8b7121d53c089ffcd614bfc6ccc0ada5e08bcfe;
  Bismarck4e3acec05e99f92bdff7e606b90e050ced7833b1a495693f4f6be24ce9990807.
  Original unvisited Command/Finish/Watch branches remain out of scope;
  bounded Bismarck NETWATCH BATTLE_Init collector added without
  replacing original dispatcher. Source/head/master bytes CI-transient.
  Artifact11663298054 GitHub metadata SHA256
  1ab9b437115567155c985c40c3ddf2dc0ae931121d6ed28537f38341f09f5be9
  not independently verified as ZIP. Receipt
  STONEAGE-PARTY-PET-ORIGINAL-LOOP-ACCEPTANCE-R1.json.
  No 1999 Japanese or Taiwan-v1 historical equivalence.


## 2026-10-10 — Original populated party/pet Command waiting source evidence

- Exact tested input b34f33778209f2968b7ec6fa64392ee186135808, treebf417cf2b2d194d1f8e2ca48a2bc9bdfd38176c4;
  Action38040961426/job114180944923 SUCCESS all10 steps,20 Python tests.
- Pinned Gavin1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56 and
  Bismarck999ffdf1d220ec6666eb65339180689c9caf1876 original headers and
  original BATTLE_CommandWait/TimeOutCheck/Command bodies, unchanged.
  Derived function and battle-file identities emitted; originals transient.
- Four encounters/profile/optimization, three no-timeout ticks/encounter;
  original Exit/Delete retained, arena rotation0,1,2,0. O0/O2 traces
  Gavin150a9e64d445d03c183d248132bcc748dc81e7fc702a6ad3cbc2df77ad1e7566,
  Bismarck8a5edbda2af6435a043ff810367e4a0da74f3ee23dc9b91c907063aea1d0aed0.
- Bismarck zero-input PartTime wall-clock+99 differs from Gavin0. NowTime
  and scoped fixed audit_time1000 remain distinct; raw _BATTLE_TIME source
  block is disabled in actual preprocessing, not a tested dispatcher delta.
- Independently downloaded artifact11665722365 ZIP SHA256
  65314a92254b5ceb228c7565145e0e7661b5ca77077c537065ebd2e87a20ac66;
  sole source-free report equals local bytes. Original AI/actions, expired
  timeout, Finish/rewards/transport/Lua/JSS1999/Taiwan-v1 not established.
  Receipt STONEAGE-PARTY-PET-ORIGINAL-COMMAND-WAIT-ACCEPTANCE-R1.json.


## 2026-10-10 — Original real-header party/pet command-input R1 derived witness

- tools/stoneage_party_pet_command_input_audit.py preserves full original
  battle_command.c parser/helper bodies plus original display-name accessors;
  pinned Gavin1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56,
  Bismarck999ffdf1d220ec6666eb65339180689c9caf1876. Sourcefile/function hashes
  retained in derived report/acceptance receipt. No original source/assets added.
- Tested commit6080641f4db0ac90997691397c79b0091bab1d1a, treea02114846400acd4f9cf22f4805eb199a7c61a2b,
  Action38042176587/job114184444031 SUCCESS,27 checks, O0/O2 UBSan,
  16 encounters/96 parser calls, byte-equal complete native traces.
- Artifact11665409109 independently downloaded ZIP SHA256
  9a736b9a26bbc4fc1276458b7af8b3a95880679a191cd15381fe30a026981779;
  sole stoneage-party-command-input.txt equals local report SHA256
  53b971a307ea50bc6d3207c8a8f0dc0f182a6b6bee1a8486ad79b5aca3540635.
  research/recovered/STONEAGE-PARTY-PET-ORIGINAL-COMMAND-INPUT-ACCEPTANCE-R1.json
  and specs/STONEAGE-PARTY-PET-ORIGINAL-COMMAND-INPUT-R1.md define limits.
- Capability FACT only within bounded late-source admission/readiness fixture.
  Original AI/action/round/Finish/profit, real network/Lua/full server ABI and
  JSS1999/Taiwan-v1 remain OPEN. No pressure promotion or engine phase change.


## 2026-10-10 — Original real-header party/pet AI-decision derived witness R1

- tools/stoneage_party_pet_original_ai_audit.py extracts complete original
  BATTLE_ai_all/BATTLE_ai_normal/GetSubdueAttribute/CanMoveCheck bodies and
  original result/table/enums/NPC option parser/workchar accessor; sourcepins
  Gavin1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56 and
  Bismarck999ffdf1d220ec6666eb65339180689c9caf1876. Sourcefile/body hashes
  emitted. All original bytes transient; no original source/assets committed.
- Tested13da7c46f75d2b1a71ca07fd013d381905310762/tree74fbacc7391da1c527cb9edf162710508cb866e8,
  Action38042867747/job114186442942 SUCCESS,33 checks, GNU99 O0/O2 UBSan,
  16 encounters/128 AI scenarios/48 guards, byte-equal native traces.
- Artifact11665454779 independently downloaded ZIP SHA256
  b7a47baba78a629a6ff0d3c79f66dbff65e0c1f4f31f70c14fe5a20350791e84;
  sole stoneage-party-original-ai.txt equals local report SHA256
  c01f4bd2455e0fc96ccfd603d8e7455a28456a8587450f5ab00685ab145294f1.
  research/recovered/STONEAGE-PARTY-PET-ORIGINAL-AI-ACCEPTANCE-R1.json and
  specs/STONEAGE-PARTY-PET-ORIGINAL-AI-R1.md define explicit fixture limits.
- Controlled attack-only one-enemy decision FACT, not natural selection or
  multi-enemy/guard/escape/magic/skill/attribute execution. Complete original
  Battling/Command/OnlyRescue source-only named-call inventory retained in
  receipt for next work; not executed or complete transitive call graph.
  Action round/Finish/profit, full server/transport/Lua/original ABI and first
  release historical equivalence remain OPEN. Pressure2486/2465/18/3,0 promotions.


## 2026-10-10 — Original real-header party/pet guard-round derived witness R1

- tools/stoneage_party_pet_original_round_audit.py extracts unchanged original
  full Battling and scheduler/status/loyalty/weapon/guard/profit-bookkeeping/
  OnlyRescue helpers from pinned Gavin1f90cb6/Bismarck999ffdf1. Original local
  scheduler types/tables/prototypes and Bismarck strncatsafe retained; file/body
  SHA256 hashes in report/receipt. Original bytes transient, never committed.
- Tested 6b97f7ffb1948a7517ff074cb3146cecde54228e/treefee4ac7b32ba6e83565c614cf2e790a6aa66e1d9,
  Action38044522888/job114191255405 SUCCESS,40 checks;16 GNU99 original-header
  O0/O2 UBSan all-guard rounds, exact complete actor/arena effects, turn1/C_WAIT.
  Original body inclusion is not execution of every branch; untaken calls abort.
- Artifact11667436659 independently downloaded ZIP SHA256
  ae61188b05d026dfed498ec71920bb22d2b47c65f0c62aec555413407cd4b32e; sole
  stoneage-party-original-round.txt equals local report SHA256
  c75674c7626cccb554c26fd21f4d066224015ec1fbb4eb29976a3f690050b148.
  research/recovered/STONEAGE-PARTY-PET-ORIGINAL-GUARD-ROUND-ACCEPTANCE-R1.json and
  specs/STONEAGE-PARTY-PET-ORIGINAL-GUARD-ROUND-R1.md define bounded fixture scope.
- FACT is controlled nonterminal all-guard round, not ordinary damage/death/
  terminal Finish/profit, whole AI, real networking/Lua/server or first-release
  historical equivalence. Pressure2486/2465/18/3,0 promotions; earlier records intact.


## 2026-10-10 — Original real-header ordinary attack-round derived witness R1

- tools/stoneage_party_pet_original_attack_audit.py composes unchanged pinned
  Loop/Command/full Battling with original targeting/AttackSeq/physical/attribute/
  guarded damage/DamageSub/wake-up/item checks and CHAR function-pointer access.
  Gavin1f90cb6/Bismarck999ffdf1 bodies hashed in report/receipt; Bismarck AttrCalc
  from battle_magic.c, ArrangeCheck absent in original configuration. Private
  declarations preserved; no original source/header/table/assets committed.
- Tested c95949be8ea233a2baee39486007934441cdb29f/treed2db8c2b640677cb5583302f58332be5ccfd4248,
  Action38045810852/job114194996158 SUCCESS,47 checks, GNU99 O0/O2 UBSan+libm,
  16 nonterminal attack rounds/16 guard controls; one guarded enemy takes73,
  HP500->427, exact complete seven-actor/arena effects. Controlled base stats,
  dynamic current enemy actor/Index2No target, fixed RNG/tactics0; not natural
  gameplay selection or all helper branches. Presentation transport collected.
- Artifact11667553905 independently downloaded ZIP SHA256
  76a7f27726ab8aa6601fd37cbd019e679e8569401776b85546314fbd40f9ecd7; sole
  stoneage-party-original-attack.txt equals local report SHA256
  cb4696b07951feb3e9bdab47a90884f5eb7e440da5d8332fc17369f1f7cc4502.
  research/recovered/STONEAGE-PARTY-PET-ORIGINAL-ATTACK-ROUND-ACCEPTANCE-R1.json and
  specs/STONEAGE-PARTY-PET-ORIGINAL-ATTACK-ROUND-R1.md preserve exact scope.
  Default compiler-path regressions Action38045567081/38045566999/38045567065
  succeed on identical shared compiler blob; receipt records exact earlier SHA.
- FinishSet/Finish/GetProfit source-only hashes/call inventories guide next gate;
  no terminal death/Finish/positive profit, whole AI/server/transport/Lua/original
  ABI or first-release historical equivalence inferred. Pressure2486/2465/18/3,
  zero promotions. All earlier records remain preserved.


## 2026-10-10 — Bounded original terminal EXP/config source identity R2

- Provenance: Gavin source pin 1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56
  and Bismarck 999ffdf1d220ec6666eb65339180689c9caf1876;
  preflight Action38059963496 SUCCESS,15 tests, code b896456fa0cf6a1559b41f9779d7f8e9bb4f0fc4.
- Original preprocessed BATTLE_GetExp SHA256 Gavin
  52351c2077b18737c59e0c28e308627b17a4a2ff10340c1c997e6e88ea830759,
  Bismarck f0c6d9ae3f32865adb0565f30749ebb3f37104d262a66e3e076acf221074d4a1.
  Frozen original Finish/GetProfit bodies and static chain through
  GetExpGold to GetExp and CHAR_AddMaxExp verified.
- Original raw conditional config getter references Gavin config.battleexp
  via gmsv/src/configfile.c and Bismarck gServerConfig.battleexp via
  server/gmsv/config_file.c. Not proof of active compiler branch or runtime
  multiplier. Exploratory Action38059421285 entered Finish/GetProfit/
  GetExpGold but stopped at BATTLE_GetExp trap; no positive reward claims.
- Acceptance receipt research/recovered/STONEAGE-PARTY-PET-FINISH-EXP-CONFIG-PREFLIGHT-ACCEPTANCE-R2.json.
  GitHub-reported derived artifact11673185532 sha256
  a50012961bec3687a9311c0e12d68151f416eb3f287b5bef5845ea56d70abad9,
  not independently downloaded.


## 2026-10-10 — Original native EXP write witness R1

Pinned original Gavin1f90cb6/Bismarck999ffdf1, gate
tools/stoneage_party_pet_original_exp_audit.py and frozen
research/recovered/STONEAGE-PARTY-PET-ORIGINAL-EXP-SOURCE-R1.json.
Action38061352391/job114240093703 SUCCESS at b770da49,21 tests,144 direct
EXP cases+16 invalid-recipient controls, O0/O2 UBSan, full actor/arena oracles.
Independently downloaded artifact11673262164 ZIP SHA256
e2420d657e6a137f1a59dc3f5dc6012b087bd85d8200614dcfa08cd954deb7d0;
report SHA256 cfba56b03245adfa7eed0e6bd588451a7a7c37de540730dc30c3e5913fb2decb
equals local bytes. Active unsigned getter, Bismarck million floor and different
EXP caps versioned; no original code/assets vendored. Direct GetExp acceptance,
not full Finish/leveling/items/gold/auto-exit or first-release historical fact.
Receipt STONEAGE-PARTY-PET-ORIGINAL-EXP-ACCEPTANCE-R1.json.


## 2026-10-10 — Original second Loop Finish derived witness R3

Action38062576189/job114243661038 SUCCESS at450b6502,27 tests/10 steps,
16 O0/O2 UBSan native second-Loop Finish dispatches and32 reward sends. Whole
seven-actor/arena byte oracles, exact original RS texts and automatic Exit/Delete
verified. Gavin1f90cb6/Bismarck999ffdf1 original function/config/table SHA256
manifest and explicit LV100/no-level-up/empty-item/synthetic-transport scope in
STONEAGE-PARTY-PET-ORIGINAL-FINISH-DISPATCH-ACCEPTANCE-R3.json. Artifact11673702550
independently downloaded ZIP SHA256 dd94e1ea0a2be4381739ca27c1c01638f272f07eb19325bd18293006ba115e34;
report915dc7ad3c72de5c7f6cf72680340952c7faee65ed4c93387a2352bb1a600e4c equals local.
No original source/assets committed; not full leveling/items/gold/network or
first-release equivalence. Pressure/promotions unchanged.


## 2026-10-10 — Original PLAYER level derived witness R1

Action38064186794/job114248381131 SUCCESS ate6f65028b93cefe6d91b99e5201ebfd45e7a309d,33 checks/10 steps.
Tools/spec/source manifest/receipt STONEAGE-PARTY-PET-ORIGINAL-PLAYER-LEVEL-R1:
original Gavin1f90cb6/Bismarck999ffdf1 LevelUpCheck/HandleExp/GetExpGold/compliance,
original PartyUpdate, Bismarck getPartyNum/earnFame body hashes frozen.16 native
O0/O2 UBSan Finish encounters; full seven-actor/arena effects and automatic release.
Artifact11674645724 independently downloaded ZIP SHA256
eaf4f7977bb3842f29d1acb1f0dd72680bd0e69f2046ff7562143c067ecc1f26; report SHA256
65a5d8c94c002c52a25d770e1d3cf83ab449ea8ac6befff6a28c0a3212dcd3e8 equals local19282 bytes. Explicit seededEXP,
Gavin synthetic thresholds, complete post-lethal party roster and typed output
collectors; no original source/assets committed, no historic/pressure promotion.


## 2026-10-10 — Original PET growth derived witness R1

Action38065547933/job114252321832 SUCCESS at5a6f8975b97d4cda9402ae0585fb1b4318bf844f,40 checks/10 steps.
Gate tools/stoneage_party_pet_original_pet_growth_audit.py and R1 spec/source
manifest/receipt. Original Gavin1f90cb6/Bismarck999ffdf1 pet LevelUp/LimitCheck/
VariableAI/earnFame whole-body hashes plus inherited Finish/EXP/player fingerprints.
16 original-header O0/O2 UBSan terminal encounters; complete Char/BATTLE byte
oracles,16 aggregate pet levels,176 growth+16 separate Loop draws. Exact typed
output and automatic release. Artifact11675067390 independently downloaded,
ZIP SHA256 bbddd1e2754835de9b56e2e2157a1685883cfbb110ac6988de24296df7b77b4f; report SHA256
3f98c0954cdc8dcbcb98c0322d3a008e57e58109f28b8a129dd4f6e457c754dd equals local22874 bytes.
Explicit rawEXP1/seededEXP/packed points/ranks/controlledrand/empty-family scope;
no original source/assets vendored or historic/pressure promotion.


## 2026-10-11 — Original reward ITEM ownership derived witness R1

Action38066688918/job114255654462 SUCCESS atc479c172,45 tests/10 steps.
R1 tools/spec/source manifest/receipt STONEAGE-PARTY-PET-ORIGINAL-REWARD-ITEM:
original inventory accessors/add/release/unique-code setter/name/escape and exact
escape-table hashes; complete real ITEM/Char/BATTLE layouts, O0/O2 UBSan.
Artifact11674184219 independently downloaded ZIP8008 bytes SHA256
ec980a57ad0c813d8f1e0a888c2eed8af1ae80d2ec31041ef8d53752ade26450;
report27953 bytes SHA256730e5ab785cb8bd116dcb977dd9025b9f70c71ddb621a47d00cc132723323082
equals local. Explicit prepared unattached item/empty/full/member/stale inputs;
no original source/assets committed and no historical/capability promotion.


## 2026-10-11 — Original shared reward ownership derived witness R1

Action38067486588/job114257981933 SUCCESS atee860140,51 tests/11 steps.
Tool/spec/receipt STONEAGE-PARTY-PET-REWARD-OWNERSHIP-R1 retain exact prior
original item-function/escape-table manifest and complete ITEM/Char/BATTLE layouts.
Strict original warning-output adapter does not change release scan or fields.
Artifact11675600547 ZIP16085 bytes independently verified SHA256
2f2801d80cc7836eee5258216a5f9b7f313aee075f7e421ca67dd9480f3901d7;
new report29043 bytes SHA2565b2c9365b5cf053c8d4c490867f7f56d268f571f4a5bad20132e59e857093992;
retained report27953 bytes SHA256730e5ab785cb8bd116dcb977dd9025b9f70c71ddb621a47d00cc132723323082.
Both reports equal local. Source-only next initializer/table/function/Lua-fallback
hashes distinguished from executed terminal evidence. No original source/assets
vendored, natural drop provenance or historical/capability promotion.


## 2026-10-11 — Original item allocator derived witness R1

Action38068762702/job114261692113 SUCCESS atf5bfbebc,57 regressions/11 steps,
32 native encounters including16 retained ownership. Tool/spec/source manifest/
receipt STONEAGE-ITEM-ALLOCATOR-R1 freeze original Gavin1f90cb6/Bismarck999ffdf1
initializer/table/function construction and Bismarck active empty Lua fallback.
Full original layouts and inherited battle/level/growth/ownership evidence.
Artifact11676102734 ZIP16652 independently downloaded SHA256
1c08eaa972dfda25a6b5be8f73331b1b2366e21f0188673c901e69613f46bbc9;
new report31513 bytes SHA2564f7eba16f68b448a5676c55e1762032d87fb18a2f2a1af43d9148603509e7941;
retained report29043 bytes SHA2565b2c9365b5cf053c8d4c490867f7f56d268f571f4a5bad20132e59e857093992.
Both equal local; retained equals prior accepted report. Original source/assets
stay transient. Source-only factory/drop/enemy leads distinguish future positive
creation from this direct initializer witness; no historical/capability promotion.


## 2026-10-11 — Original same registered item second Finish capacity witness R1

Tool/spec/source-free report/receipt STONEAGE-BATTLE-ORIGINAL-SAME-ITEM-CAPACITY-R1;
Action38107983603/job114377447591 SUCCESS, input875411b76e786ee4dd26e6abd22b6543547cd744,
53 regression/evidence completeness tests and retained original factory native gate.
Pinned Gavin1f90cb6/Bismarck999ffdf1 own original headers and unmodified functions;
source bytes CI/local transient, not redistributed.24 second-Finish calls under
O0/O2 nonrecovering UBSan, complete native item/actor/arena oracles for partial,
full and last-slot input. Local report26059 bytes SHA256
ace3536523f4220eb478a740b367ad6deeb881095691e03ffc1038aa527db4cf.
Artifact metadata/independent verification extent in acceptance receipt. Synthetic
master/RNG/fillers and64 MiB audit stack are explicit. Source-only negative guard
hashes retained as next evidence leads, not runtime acceptance or early history.


## 2026-10-11 — Original exceptional ticket cleanup source witness R1

Tool/spec/derived report/receipt STONEAGE-BATTLE-ORIGINAL-TICKET-CLEANUP-R1;
Action38109922966/job114383177723 SUCCESS at8ac04c40311ec8d71bf4eacc9f2e9d638c5f1cc8,
61 tests, eight negative/duplicate witnesses and six retained capacity witnesses,
GNU99 O0/O2 nonrecovering UBSan plus independent original factory gate.
Source pins Gavin1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56 and
Bismarck999ffdf1d220ec6666eb65339180689c9caf1876. Original BATTLE_DeleteItem/
DeleteBattle bodies matched unchanged per profile; exact body/native connection
hashes in source-free report and receipt. Both original CheckDefBTime bodies
execute without source edits or feature switches. Bismarck original global
const delayTime5 is recovered and hashed; an initial omission in the standalone
harness dependency extraction was corrected before final acceptance.
Complete256 items/seven Char/
BATTLE/eight connection arrays checked;32 new second-Finish calls. Cleanup report
28290 bytes SHA2569d2f5204026cb66068fdac935945f0bc44b8c5c3ada52ea76894a10e76d25cf7.
Artifact11690547978 independently downloaded/digest-verified, reports byte-exact
against local. Original server C/headers/assets remain only transient outside
repository. Synthetic actor/ticket/empty bag/time inputs, differential XP oracle,
late provenance and natural reachability limits preserved. Pressure unchanged.


## 2026-10-11 — Original recipient type and side-type cross-index witness R1

Tool/spec/source-free report/receipt STONEAGE-BATTLE-ORIGINAL-RECIPIENT-SIDE-R1,
Action38110690423/job114385444015 SUCCESS atdbc1755f4c2d9c53ba736e1ac6c30c16e21255b4,
69 tests;16 cross-index witnesses plus14 retained capacity/cleanup witnesses.
64 new original Finish calls, GNU99 O0/O2 nonrecovering UBSan, complete native
256-item/seven Char/BATTLE/eight-connection oracles. Original Finish/GetProfit/
GetExpGold and inherited timer/delete body hashes retained unchanged per pin.
Source pins Gavin1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56 and
Bismarck999ffdf1d220ec6666eb65339180689c9caf1876. Report33800 bytes SHA256
1bf9a54cce0b6895a5fa6b75ff299d0a62b9d4813c0cf3c53a059df9536f4474. Artifact11691409478 ZIP digest independently
verified, both reports byte-exact against local, original factory gate retained.
Original C/headers/assets stay transient. Explicit actor0 OTHERNPC retag and
side-type fixtures do not establish natural creation/entry or early history.
Source-only next ITEM check/release/DeleteItem fingerprints are future invalid
item-ticket leads, not runtime acceptance. Pressure/promotions unchanged.


## 2026-10-11 — Original invalid item ticket bounded source witness R1

Tool/spec/source-free report/receipt STONEAGE-BATTLE-ORIGINAL-INVALID-ITEM-TICKET-R1;
Action38111449268/job114387697755 SUCCESS atc47212ab443601bf7dd37aec564c5219b218eba5,77 evidence/regression checks,
12 new witnesses/48 Finish calls plus30 predecessor witnesses. Pinned Gavin
1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56 and Bismarck
999ffdf1d220ec6666eb65339180689c9caf1876, unchanged native item-check/release/
DeleteItem source body fingerprints now executed in the named bounded matrix.
All256 backing item/seven Char/full BATTLE/eight native connection domains,
O0/O2 nonrecovering UBSan complete-output equality and original timer gate.
Report38064 bytes SHA2566cd63a295651a15330c78cb14b02a50596a05a5e1579b81ea1c24b1b5df6d1f1.
Artifact11692295718 ZIP independently digest-verified, both reports byte-exact
against local; independent factory evidence equals preceding accepted gate.
Explicit logical pool256 and prepared inactive inputs do not prove natural
bad-ticket creation or early history. Original C/headers/assets transient only,
pressure/promotions unchanged, ordered mixed pending slots remain OPEN.


## 2026-10-11 — Original ordered mixed ticket bounded source witness R1

Tool/spec/source-free report/receipt STONEAGE-BATTLE-ORIGINAL-MIXED-ITEM-TICKET-R1;
Action38112051947/job114389462026 SUCCESS at3a65495cb4e79842604bb27da77e57dfc98fffa1,87 regression/evidence checks,
66 new witnesses/264 Finish executions plus42 predecessor witnesses. Source
pins Gavin1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56 and
Bismarck999ffdf1d220ec6666eb65339180689c9caf1876. Whole unchanged GetExpGold/
DeleteItem/DeleteBattle/ITEM_getAppropriateName fingerprints retained; complete
256 item/seven Char/BATTLE/eight connection domains, ordered full RS text and
original timers, O0/O2 nonrecovering UBSan complete-output equality.
Report64054 bytes SHA25625a509b13a471e58f50a27dfb0673ad7865c34e2ec6d2ca607c0eba54a1584ac.
Artifact11692306690 ZIP independently digest-verified and both reports byte-exact
against local, factory report equals preceding accepted gate. Explicit logical
pool256/three-slot ticket inputs and original identification/name profiles do not
prove natural bad-ticket creation, early history or actual client rendering.
Original C/headers/assets transient only; pressure/promotions unchanged.


## 2026-10-11 — Original last-slot competition bounded source witness R1

Tool/spec/source-free report/receipt STONEAGE-BATTLE-ORIGINAL-LAST-SLOT-TICKET-R1;
Action38112978727/job114392200741 SUCCESS atee85e142a4d7fb60e2b63e77871ee194f45b7523,97 checks,132 new witnesses/
528 Finish executions plus108 byte-exact predecessor witnesses. Gavin source
pin1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56 and Bismarck
999ffdf1d220ec6666eb65339180689c9caf1876 retained. Original release/search/add-item
whole body hashes checked; observer forwards unchanged arguments, records54/84
empty teardown baseline and incremental item3/invalid calls. Full256 items,
seven Char/BATTLE/eight connections and exact full RS/original timers checked,
GNU99 O0/O2 nonrecovering UBSan complete-output equality.
Report137748 bytes SHA256c0cd23bafd5f19a393506e0e6750b40ccab4d1a4fc17ceb32025bbacb53b2821.
Artifact11692551246 ZIP independently digest-verified; both reports byte-exact
against local, factory equals preceding accepted gate. Explicit logical256 pool,
synthetic fillers and ordered pending inputs do not prove natural generation,
early server identity or actual client rendering. Original C/headers/assets
transient only; no historical/pressure promotion. Distinct original creation OPEN.


## 2026-10-11 — Original distinct-drop creation and competition source witness R1

Tool/spec/source-free report/receipt STONEAGE-BATTLE-ORIGINAL-DISTINCT-ITEM-TICKET-R1;
Action38113984094/job114395096379 SUCCESS ateb18d164d7ef24d1d91815f37b66c2f023d7fefc,107 checks. Two original-creation
rows plus24 payout rows/96 new Finish executions,240 predecessor rows byte-exact.
Pinned Gavin1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56 and Bismarck
999ffdf1d220ec6666eb65339180689c9caf1876. Complete original creation allocator,
disposal, factory and AddExpItem fingerprints; raw/preprocessed macro forms
separate. Actual enemy4/objects4,5,6/IDs1,2,1 from explicit guaranteed master,
then original assignment. Full256 items/seven Char/BATTLE/eight connections,
per-object releases/typed winner logs/inventory/full RS/original timers checked,
GNU99 O0/O2 nonrecovering UBSan complete-output equality.
Report155342 bytes SHA256611319f6d1a8c76724192ee391a4095721d444195a026ff54260df976ddd2d89.
Artifact11692284898 ZIP independently digest-verified; both reports byte-exact
against local, factory equals preceding accepted gate. Transient Bismarck table
backing3/logical size restored2, synthetic template2/fillers/permutations do not
establish natural recovered master data or early history/client rendering.
Original C/headers/assets transient only, no historical/pressure promotion.
Fourth-drop original pending-slot overflow/replacement remains OPEN.


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

## SRC-LATE-2026-ORIGINAL-RELEASED-SLOT-REUSE-R1 — Controlled original factory after battle replacement

- **Type / confidence:** original late open-source descendant implementations and recorded deterministic native execution (B for preserved source provenance, experimental FACT for precisely specified test fixtures). No verified original JSS1999 or Taiwan1.0 build equivalence.
- **Pinned evidence:** Gavin gavinlinasd/StoneAge at 1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56 and BismarckDD/stoneage at 999ffdf1d220ec6666eb65339180689c9caf1876, no changed original gameplay item/battle bodies.
- **Native witness:** `research/recovered/STONEAGE-BATTLE-ORIGINAL-RELEASED-SLOT-REUSE-R1.txt` and acceptance receipt `research/recovered/STONEAGE-BATTLE-ORIGINAL-RELEASED-SLOT-REUSE-ACCEPTANCE-R1.json`; source-free spec `docs/specs/STONEAGE-BATTLE-ORIGINAL-RELEASED-SLOT-REUSE-R1.md`; GitHub Actions 38140069870 artifact11702686283, SUCCESS, 171 Python regressions, O0/O2.
- **Proof:** historical descendant item8 released by unchanged four-drop assignment, reused as new template ID2 while explicitly retained PET2 alias index8 persists, or protected when carried alias index8 belongs to PLAYER0 within getFdnum2 range; 255 other item records and native actor/arena/connection/table state remain controlled.
- **Does not prove:** actual player/pet alias reachability in early live builds; unique-code generation lifecycle, authentic RNG/pool distribution, early client-side object identity, ownership semantics in production or desirable design behavior.

## SRC-LATE-2026-PET-ITEM-IDENTITY-SOURCE-R1 — Pinned raw PET item/unique-code call paths

- **Type/evidence:** two pinned later open-source descendant source trees and default version.h headers, source-only. This establishes named body fingerprints and conditional branches, not contemporary provenance of the historical 1999/2000 builds.
- **Source identities:** gavinlinasd/StoneAge commit `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`; BismarckDD/stoneage commit `999ffdf1d220ec6666eb65339180689c9caf1876`; eight exact original Git blobs and 22 function SHA256 hashes retained in derived report.
- **Receipt:** `research/recovered/STONEAGE-PET-ITEM-IDENTITY-SOURCE-ACCEPTANCE-R1.json`; `research/recovered/STONEAGE-PET-ITEM-IDENTITY-SOURCE-R1.txt`; workflow38141501893 SUCCESS; artifact11702398957 ZIP2375 bytes SHA256 `2b4ea6a6e5caff528d89495c5f8ba7f47089ad98eb6905a93c72091d5852bfac`; source-only report SHA256 `93ca80e4bb849215eb8a30188584eeb89ae90082b220642e539b8a22ddfb2f3f`.
- **Proves:** conditional PET item save/load code and generic item mutation capabilities exist in later descendant raw source. In pinned default headers Gavin `_SIMPLIFY_ITEMSTRING` is defined, Bismarck `_PET_ITEM` undefined, so those respective PET serialization paths are not enabled under these header defaults; both define `_UNIQUE_P_I`.
- **Does not prove:** real compilation flags, naturally reachable PET item references, stale index dereferences, stable identity under slot reuse, or early JSS/Taiwan build equivalence.


## SRC-LATE-PET-ITEM-DEFAULT-COMPILE-GATE-20261011

- **Source / date / grade:** Bounded derivation from pinned late source descendants Gavin 1f90cb6 and Bismarck 999ffdf1, inspected on 2026-10-11. Source-preserved later descendant evidence, **not** contemporaneous JSS1999/Taiwan v1.0 original proof.
- **Pinned build files:** Gavin root Makefile blob d2be7a699c909c8e9515971b906dbc79586beb73 and char/makefile e1843e9684078d23cc36a93c63f1c1adec90d4e4; Bismarck root makefile 8afd1f288a1d07a5cf0075af04e51e64741dcc81, char/makefile 2c624e29639dc43169dfa5378d28e4086413c663, Windows CMakeLists 1523d12c3543e3d2a8c3a1401f92d79d11d85413. Retained earlier verified char/char_item.c and version.h fingerprints.
- **Evidence:** `research/recovered/STONEAGE-PET-ITEM-BUILD-GATE-R1.txt`, exact Git blob 2d5d55984972975fe769efd6adb5466731499e17, report 1418 bytes SHA256 59f2c994d6d5169553d0c8bd38ca47c2b4fe4ba9e603a49fa05bc86441a8925b. GitHub Action38142524756/job114479121485 SUCCESS; artifact11703790355 ZIP901 bytes SHA256 5db979c903f34f11f1a3c99aab8b24269e858364d4aec962e2ea385d61cf3a67 independently downloaded and checked. 17 Python regressions, reproducible byte equality. Receipt and spec under STONEAGE-PET-ITEM-BUILD-GATE-*R1.
- **Proves:** Effective compiled *checked-in default* macro set has _UNIQUE_P_I=on, _SIMPLIFY_ITEMSTRING=on, _PET_ITEM=off in both profiles; Bismarck optional PET equipment function is not emitted without explicit feature toggle, and 0 direct C callsites occur in recursively scanned Bismarck/Gavin configured C source roots. A synthetic -D_PET_ITEM preprocess reveals its body, not a functional deployed route.
- **Does not prove:** Deployment configurations or actual built executable; absence of generated/indirect/external callbacks; naturally reachable PET equipment/alias and save-load; unique item identity across release; early JSS/Taiwan-version membership.


## SRC-LATE-BISMARCK-PET-PROTOCOL-CROSSMODULE-20261011

- **Pinned Bismarck descendant:** 999ffdf1d220ec6666eb65339180689c9caf1876; server/common/gmsv_server_send.c blob84dd1b2d9fbac10fe39983e6b8984aaebf1b3075; gmsv_server_recv.c blob088db5e38a1bc0dd47b3c3120480af93ab24c4c7; common/makefile blob263ef622f4c0c3ac495d783ff35b078277984d43; gmsv/char/char_item.c blob970b7b3f975965c6c5e77352a2e0382adf943753.
- **Proof and correction:** server/common optional packet decoder calls receive callback, which calls CHAR_movePetItem in GMSV; all under _PET_ITEM. The prior no-caller report was only for GMSV subtree. Default CPP excludes all three and controlled -D_PET_ITEM exposes them, without any proof of deployed binary, client opcode emission, or historical natural reachability.
- **Verification:** Action38143205543/job114481110061 SUCCESS; 24 tests; artifact11703751530 ZIP1053 bytes SHA256 de7cc961a2d5164d0d2c9b0dfce18349bbf60ea2b9886ebbd74aff8837776c73 independently verified. Report STONEAGE-PET-ITEM-PROTOCOL-CROSSMODULE-R1.txt 1710 bytes SHA256 24c2723a3b268f3c0dd9b401edf03d5ead128ec61464b03afabd38a9fea1327e; Git blob2a9316528c30460f8a314862dcf22f57d198190e. The receipt/spec preserve unmodified prior evidence and restrict source-only/1999/Taiwan1.0 claims.


## 2026-10-11 — PET client version/header/emitter pinned source-only orientation

- **Source:** BismarckDD/Stoneage pinned late-descendant Git commit `999ffdf1d220ec6666eb65339180689c9caf1876`; five exact verified Git blobs: `client/resources/version.h` `35bd4446a740a189c1ad9439e30e61fe169d5f46`; `client/stoneage/proto/protocol.h` `bb70087ef1b1915748da23935584eda2c8178cb0`; `client/stoneage/proto/protocol.cpp` `17f1900d8845c15308a4b429905ec009e5fd4c0f`; `server/common/gmsv_server.h` `708fe1b9f73be4952677fda474f10e86d9a56306`; `server/gmsv/include/version.h` `b3fc0c80705973bc8d088287c98a5d66171bb6c2`.
- **Classification:** FACT solely for raw header version condition and optional client/server opcode-127 sender/receiver definitions. Seven read-only source checks PASS. Does not prove full preprocessed client, real call site, actual packet or deployment. Indexed current-head search is not a complete pinned-commit source scan.
- **Derived/source-free record:** `docs/specs/STONEAGE-PET-CLIENT-VERSION-EMITTER-SOURCE-R1.md`, `research/recovered/STONEAGE-PET-CLIENT-VERSION-EMITTER-SOURCE-R1.json`. Original sources not copied.
- **OPEN:** Real alternate 8.0 client compile options, pinned native caller inventory and dispatch, compatible server binary and original JSS/Taiwan-v1 equivalence.


## 2026-10-11 — Complete pinned late Bismarck client PET equipment call path, SOURCE_ONLY ACCEPTED

- **Pinned late source:** BismarckDD/Stoneage commit `999ffdf1d220ec6666eb65339180689c9caf1876`; full tracked `client/` tree `511d9b24376c6858b70ab3015e36f5007bfd565a`; 237 C/C++/header paths, sorted path-Git blob SHA256 inventory `919703b218e8a4a417c5500bf77592bfc763286ca79b0fb47ffca92731ab4175`.
- **Additional anchored file:** `client/stoneage/system/menu.cpp` Git blob `62754fdd0db1b84c358d61418d253012d149e1d4`. Three UI send invocations at lines 14824, 14966, 15333 under _PET_ITEM; declaration and definition at protocol.h:462 and protocol.cpp:2280. Headers client/server conditionally define matching packet127. Client project `client/stoneage.vcxproj` Git blob `373c0699a5df017f53e4ab7a7d64c3d6280a8578`; checked-in Debug/Release _SA_VERSION_SPECIAL macro adds version60, **not** _PET_ITEM; counterfactual version80 exposes the feature.
- **Accepted derived evidence:** `docs/specs/STONEAGE-PET-CLIENT-FULL-CALLGRAPH-R1.md`, `research/recovered/STONEAGE-PET-CLIENT-FULL-CALLGRAPH-R1.txt`, `research/recovered/STONEAGE-PET-CLIENT-FULL-CALLGRAPH-ACCEPTANCE-R1.json`. Workflow run38145213269/job114487010565 SUCCESS with 20 regression checks and byte-exact report validation; artifact11704168980 (GitHub-reported ZIP SHA256 `263a178c4e8f6b5a615a7dc5805aff5946fea39c3070017ccae27797e93af8e9`, not independently downloaded).
- **Limit:** No deployed enabled binary, emitted runtime packet, authenticated natural PET item ownership or JSS1999/Taiwan1.0 linkage. The earlier default-branch keyword result was incomplete; do not mistake its missing menu.cpp callers for genuine absence. No original copyrighted code copied.


## 2026-10-11 — Pinned optional PET packet fields and actor-slot/unique-code source chain

- **Evidence type:** FACT limited to nine pinned original late Bismarck `999ffdf1d220ec6666eb65339180689c9caf1876` Git blobs. Exact paths/SHAs and bounded source statements in `docs/specs/STONEAGE-PET-WIRE-OWNER-SOURCE-R1.md`; six source-function SHA256 fingerprints in `research/recovered/STONEAGE-PET-WIRE-OWNER-SOURCE-R1.txt`. No source bodies or proprietary assets copied.
- **Observed optional chain:** guarded client three menu callers -> encoder five integers plus checksum on opcode127 -> matching guarded server decoder fields2–7/checksum -> CHECKFDANDTIME/connection character/trade/battle checks -> native PET slot exchanges -> guarded item unique-code setter. Code cannot prove real packet or production execution, and a physical actor-slot reference swap is not automatically a proven persistent object owner transfer.
- **Validation:** GitHub Action38145836502/job114488864193 SUCCESS, 18 source-boundary mutation/retained tests, re-generated report byte-identical to archived file, artifact11704498263 with GitHub-reported ZIP SHA256 `a43cd6cba439c11b0cd878180194ee9f391789d838a43fde0c73961804e96322` (no independent download claimed); receipt `research/recovered/STONEAGE-PET-WIRE-OWNER-ACCEPTANCE-R1.json`.
- **OPEN:** real coupled 8.0 build/deployment, live packet, naturally reachable owner/unique-code identity and save/load, earlier JSS/Taiwan1.0 membership. No early-version inference.


## 2026-10-11 — Original checked-in client/server PET build-profile pairing source matrix R1

- **Pinned source:** `BismarckDD/Stoneage` commit `999ffdf1d220ec6666eb65339180689c9caf1876`, tree `a49d8fb8beaf93e07e499d65723f16922ce3ee1f`; ten exact original Git blob SHAs enumerated in `docs/specs/STONEAGE-PET-PAIRED-BUILD-MATRIX-R1.md`: Windows client `stoneage.sln`/`stoneage.vcxproj`/`build-client.ps1`/`resources/version.h` versus server Linux GNU make, Windows CMake, scripts and version header.
- **Version correction and exact negative gate:** Actual solution `VER25_DEBUG`/`VER25_RELEASE` selects `_SA_VERSION_SPECIAL` (not 8.0/PET); script defaults `VER25_Release`. Standalone Debug/Release property groups exist but are not the solution-selected names. GNU server and Windows CMake build definitions do not directly enable `_PET_ITEM` in default source. Forced preprocessor counterfactual on each side can enable the source branch; no real paired binary was compiled or executed by this gate.
- **Original commit artifact inventory:** 950 tracked blobs, zero `.exe` paths, dependency DLL/LIBs exist. Public repository Releases listing empty at this check. Negative limited to these sources; separately archived builds could exist.
- **Evidence:** `research/recovered/STONEAGE-PET-PAIRED-BUILD-MATRIX-R1.txt`, receipt `STONEAGE-PET-PAIRED-BUILD-ACCEPTANCE-R1.json`, reproducible source-only audit and mutation tests. Action38146693748/job114491443906 SUCCESS, 18 tests, archived bytes exact. Artifact11704813091 GitHub-reported zip SHA256 `68b495f3fab2060324a7d25842fe29e15f47bdac2d474acc503c16fc8e5ac1da` (not independently downloaded). Keep actual enabled build pair/runtime/history OPEN; no proprietary code copied.


## SRC-PET-8-2005-CONTEMPORARY-LAUNCH-20261011

- **Primary contemporaneous press:** 巴哈姆特 GNN 2005-06-08 23:04:46 by 小賢, https://gnn.gamer.com.tw/detail.php?sn=20167 ; reports operator 華義's Taiwan 8.0 release and PET equipment feature. **FACT for contemporaneous operator-release reporting only**, not pinned code/binary identity.
- **Derivative press:** 2005-06-09 Sina https://games.sina.com.cn/o/n/2005-06-09/1552109910.shtml republishes GNN; not counted as independent proof.
- **Later game overview:** https://acg.gamer.com.tw/acgDetail.php?s=5326 ; PET equipment description with seven categories; supporting context, not binary provenance.
- **Retrieval leads, no bytes accepted:** 2008 forum https://www.iopq.net/forum.php?mod=viewthread&tid=16508364 lists Wayi-hosted `sa8_8016.rar` but requires unrelated private patches; 2009 forum https://www.lab.welovesa.com/viewthread.php?tid=2 bundles `sa_8002a` and Assa8.0; 2010 custom Yang server https://www.lab.welovesa.com/viewthread.php?tid=575 advertises a community-built pair target; later 2012 recollection https://www.lab.welovesa.com/viewthread.php?tid=1978 . None is here authenticated/downloaded/hashed.
- **Boundary:** Contemporary announcement is stronger historical feature evidence, but neither proves `_PET_ITEM` enabled in checked-in Bismarck default source nor deployed paired binary/opcode127 or original early versions. Spec: `docs/specs/STONEAGE-PET-80-CONTEMPORARY-RELEASE-EVIDENCE-R1.md`. No proprietary assets committed.


## SRC-LATE-CLIENT-REGION-VERSION-CARRIER-GATE-20261011

- **Mainland corporate/domain context (period sources):** https://games.sina.com.cn/zhuanqu/sa/jiazu_9_gzwt6.shtml and https://games.sina.com.cn/z/hd19/2004-09-02/24/63614.shtml name Beijing Waei and `wayi.com.cn`; this is not automatically Taiwanese release identity despite Waei parent linkage.
- **2008 wayi.com.cn link:** https://www.iopq.net/forum.php?mod=viewthread&tid=16508364 cites `http://cdl.wayi.com.cn/sa8_8016.rar` and instructs application of separately downloaded private PET/map/client patches. Unretrieved, unverified; region provenance not Taiwan.
- **2012 six-part claimed Wayi installer (likely later 8.5):** https://www.lab.welovesa.com/viewthread.php?action=printable&tid=1654 includes six exact MediaFire carrier IDs; 2013, 2014 comments interpret it as 8.5; 2024 commenter reports installer displays 8.5, with a repost lead. **Community testimony**, no bytes, not an official 8.0 artifact.
- **Patch-only 2010 `sa_8018.exe` + numbered resource example:** https://lab.welovesa.com/viewthread.php?action=printable&tid=545 ; 2009 client resource renaming recipe https://lab.welovesa.com/viewthread.php?extra=page%3D1&page=1&tid=32 . These are not native clean original data identities. `sa_8002a.exe` appears in a private-server login guide https://lab.welovesa.com/viewthread.php?extra=page%3D1&tid=506 .
- **Derived source-free audit:** `research/recovered/STONEAGE-LATE-CLIENT-CANDIDATE-LEDGER-R1.json`; `docs/specs/STONEAGE-LATE-CLIENT-REGION-VERSION-PROVENANCE-R1.md`; `tools/stoneage_late_client_archive_probe.py` (no original binaries). Closed only the ambiguous regional/version **classification**, not retrieval, byte hashes, actual 8.0 runtime, PET opcode127, original identity or JSS/Taiwan-v1 feature membership.


## SRC-WAYI-TW-85-2006-OFFICIAL-URL-AND-MEDIAFIRE-PART-PAGES-R1

- **2006-08-13 secondary contemporary citation:** https://bbs.comefromchina.com/threads/449920/ directly states `http://download.wayi.com.tw/download/STONEAGE20060616.exe` as Taiwan 8.5 installer; guide otherwise describes an unrelated private server.
- **2008-02-16 independent secondary contemporary citation:** https://www.nakuz.com/thread-3245861-1-1.html repeats exactly that operator-domain file URL and version 8.5; guide separately directs private-server changes.
- **2012 community mirror host pages:** https://www.lab.welovesa.com/viewthread.php?action=printable&tid=1654 cites six numbered MediaFire IDs, confirmed on individually readable public landing pages. Metadata: `research/recovered/STONEAGE-WAYI-85-SIXPART-METADATA-R1.json`; shows five rounded 200MB and one rounded 92.4MB, all upload label dates 2012-04-14; **no payload bytes or exact sizes**.
- **2024 forum recollection:** Same thread says installation reports 8.5, secondary and NOT byte-confirmed.
- **Audit:** `docs/specs/STONEAGE-WAYI-85-ARCHIVE-CHAIN-R1.md`; source-free offline read-only part SHA256 tool + mutation tests. This elaborates the previously accepted `TW-YANG-2012-SIXPART` ledger candidate; it does NOT create a fifth original clean client or reclassify an unverified community mirror as authentic. Do not mix this Taiwan `wayi.com.tw` 8.5 URL with Mainland `cdl.wayi.com.cn/sa8_8016.rar` or 2005 Taiwan 8.0 PET runtime.


## SRC-TW80-2005-INSTALL-UPDATE-SNAPSHOT-SEPARATION-20261011

- **Contemporaneous GNN 2005-06-08:** https://gnn.gamer.com.tw/detail.php?sn=20167 . Operator-attributed 8.0 launch and upgraded physical distribution with update CDs. This establishes announced release/distribution modes, **not** a downloadable publisher sample, original hash or executable.
- **2005-10-08 player-quoted Waei support reply, preserved/edited 2005-11-05:** https://forum.gamer.com.tw/G2.php?bsn=1571&sn=2856 . Says partial graphics and incomplete program update can call for removing and reinstalling client; reproduced by player, no original first-party ticket available. Evidence class CONTEMPORANEOUS_PLAYER_CUSTODY_OF_CLAIMED_OPERATOR_RESPONSE, not directly authenticated first party.
- **2005-11-07 download workaround:** https://forum.gamer.com.tw/G2.php?bsn=1571&sn=2881 . Player recommendations about uninterrupted/resumable downloads; no filename or payload hash in retrieved portion.
- **2005-07-07 period PET-equipment observations:** https://www.gamez.com.tw/t/8-0/170704 . Seven broad equipment types including foot subtypes, pet slot/body restrictions, elemental interaction and reported recipes. Gameplay claim confidence is CONTEMPORANEOUS_PLAYER_REPORT; no actual original data-file version match or native replay established.
- **Later retrospective chronology:** https://forum.gamer.com.tw/G2.php?bsn=1571&sn=4345 . Repeats putative 2005-06-06 VIP 8.0 disc mailing and 2005-09-08 pet-equipment promotion. Not an independently retrieved original operator release note, not a direct internet-download lead.
- **Independent technical gate:** `docs/specs/STONEAGE-TW80-INSTALL-UPDATE-SNAPSHOT-INTAKE-R1.md`; `tools/stoneage_client_snapshot_transition_audit.py` compares two locally provided installed trees with streamed per-file SHA256/deterministic manifest hash, 13 synthetic tests. No 2005 source bytes in repository or CI, no official authenticity or 1999/2000 feature promotion.

## SRC-TW80-TW85-CONTEMPORARY-TIMING-PRESS-GATE-20261011

- **2005-06-08 GNN day-of-release Taiwan8.0:** https://gnn.gamer.com.tw/detail.php?sn=20167 confirms contemporary operator-attributed release reporting and PET equipment feature; **not a recovered deploy binary**.
- **2005-07-07 period-player PET content:** https://www.gamez.com.tw/t/8-0/170704 supports reported gameplay categories but unverified code and recipes.
- **2005-09-08 indexed same-period GNN promotion:** https://acg.gamer.com.tw/search.php?c1=976&c2=3&machine=1%2C0&s=2&type=1 includes miniature pig spokesperson and planned >=20 PET/profession gear card rewards. Original full news page not retrieved; date/index text is a contemporaneous press-index excerpt. Secondary chronicle headline https://forum.gamer.com.tw/G2.php?bsn=1571&sn=4345 is **not a separate confirmation that PET system began in September**.
- **2006-06-21 contemporary Taiwan8.5 release schedule:** https://gnn.gamer.com.tw/detail.php?sn=23856 states test June21-July5, first 蒼龍 production server scheduled July5 and all other servers scheduled from July12. Another period press account https://www.games.idv.tw/news.php?mode=view&nid=615 corroborates reported staging. Dates are operator plans as published, **not authenticated rollout observation or executable version SHA**.
- **Date-token caution:** Community-linked WAYI Taiwan8.5 `STONEAGE20060616.exe` only contains 20060616 in filename; it falls before published 8.5 beta and production schedules and MUST NOT be treated as production build date/8.0 sample without file evidence. Existing six-part mirror metadata remains unverified. Source matrix + 15 mutation-backed checks `docs/specs/STONEAGE-TW80-TW85-RELEASE-TIMELINE-GATE-R1.md`; no binaries in repository.



## SRC-TW80-2007-2016-LOOKALIKE-CARRIER-QUARANTINE-20261011

- **2007-08-17 community blog:** https://blog.sina.com.cn/s/blog_491de9d601000abm.html . Exact quoted historical link `http://220.162.242.159/StoneAge8.0setup.exe` and filename `StoneAge8.0setup.exe` for mainland or private-server compatible clients. The numbered IP, publisher custody and actual binaries are unauthenticated. Do NOT claim that the link is live, dead, original mainland or official Taiwan 2005 distribution.
- **2013-02-17 subsequent community guide:** https://www.iopq.net/thread-16840739-1-1.html . Reuses the same filename for newer mainland 8.x, but demands renamed real/adrn resource numbers and replacement `sa_8001.exe` login + IP. It demonstrates risk of post-install modification. This is NOT a second independent source of a 2007 byte digest or verified 2005 Taiwan operator installer.
- **2016-12-10 SourceForge SA80 directory:** https://sourceforge.net/projects/sa80/files/ . Public community readme and file listing state server GMSV/SAAC and data `Updated-Linux-SA80`; this is not an authenticated original client (and cannot prove original PET paired runtime).
- **Machine gate:** `research/recovered/STONEAGE-TW80-LATE-CARRIER-NEGATIVE-CONTROLS-R1.json`; `tools/stoneage_tw80_late_carrier_quarantine.py`; `tests/test_stoneage_tw80_late_carrier_quarantine.py`; `docs/specs/STONEAGE-TW80-LATE-CARRIER-QUARANTINE-R1.md`; dedicated source-only workflow. All candidate payloads unverified/no hashes; prior four regional leads remain separate. 2486=2465 bounded closed+18 OPEN+3 historical UB unchanged; no JSS/Taiwan 1.0 or PET runtime promotion.


## SRC-TW80-2005-PRELAUNCH-DISC-AND-2006-DLER-MIRROR-R1

- **Press-index-only 2005-06-03 event preview (class A for reported plan):** https://acg.gamer.com.tw/search.php?c1=976&c2=3&machine=1%2C0&s=2&type=1 , 《石器時代》捷運淡水站歡樂大拍賣, says Waei planned 2005-06-04 free 8.0 revision/update discs at Tamsui. Does NOT prove giveaway happened, whether the disc contains a full installer, clean image, or binary identity. Full first-party article not separately retrieved.
- **Contemporaneous 2005-06-08 official-launch coverage (class A for attributed release report):** https://gnn.gamer.com.tw/detail.php?sn=20167 reports 8.0 PET equipment and physical product-package update discs; no original disc image or publisher file checksum. Keep June 4 planned event discs and June 8 product-package discs separated.
- **2006-08-01 player-forum precise filename & quoted third-party mirror (class C/B depending custody; not original):** https://www.nakuz.com/thread-2493728-1-1.html records `http://tcrc.dl.dler.org/Yesterday/v/wayi/Stoneage80.exe` as main program in a private-server/how-to. The instructions mention `sa_7505`, `sa_7507` and changed resource filenames; replies mention `sa_8001`. No inspected archive bytes, source hash, operator handoff, exact executable version or actual PET runtime. Path naming cannot independently certify official 2005 Taiwan distribution. A failed web-reader open is NOT an original HTTP 404.
- **Later DLER catalog context ONLY:** https://dler.com/index.php?o=display%3Bid%3D7143 shows an unrelated 2018 StoneAge catalog entry and its own MD5; never apply that checksum or later product date to the 2006 mirror.
- **Gate and next:** `docs/specs/STONEAGE-TW80-DISC-MIRROR-IDENTITY-R1.md`, `research/recovered/STONEAGE-TW80-DISC-MIRROR-IDENTITY-R1.json`, strict metadata validator + 19 synthetic mutation/negative checks; search archived original Taiwanese 2005 8.0 disc/installer/publisher checksums; keep 2006 candidate version quarantined. Pressure 2486=2465+18+3 and zero JSS/TW1/PET runtime promotions.


## SRC-TW80-2005-MAY16-TEST-AND-OPERATOR-EVENT-URL-R1

- **2005-05-18 Taiwan contemporary publication:** https://www.games.idv.tw/news.php?mode=view&nid=326 directly states announced 2005-05-16 8.0 test-server opening, 5/16–18 promotional events, seven PET equipment families and the linked official Waei URL `http://www.wayi.com.tw/stoneage/actives/940329/page_3.html`. **A** for period reporting of launch/testing claims and existence of quoted URL, not original client image, witnessed PET opcode127, working native paired servers or downloadable publisher release.
- **2005-05-18 mainland 17173 press:** https://news.17173.com/content/2005-5-18/n358_274376.html confirms period reporting *about Taiwan* test / proposed PET equipment, not a mainland native 8.0 binary and not necessarily independent underlying press-release testimony.
- **Dated text preserved by 8591, custody caveat:** https://bbs.8591.com.tw/index.php?action=detail&articleId=33&module=article shows 2005-05-16 credited story but also later account profile date; retain as limited repost-style timestamp, not contemporaneous original site evidence of actual binary.
- **Historical operator-page access limitation:** Current `www.wayi.com.tw/stoneage/actives/940329/page_3.html` resolves a modern corporate site. Original 2005 page not obtained. CDX-only index probe is **metadata**, not page contents; an empty index or network error proves neither missing original page nor missing installer.
- **Reproducibility:** `research/recovered/STONEAGE-TW80-MAY16-OPERATOR-URL-SOURCE-R1.json` and `docs/specs/STONEAGE-TW80-MAY16-OPERATOR-SOURCE-R1.md`, fixed-reference validator, 20 mutation/negative cases and 11 CDX parser tests plus retrospective regression workflow. Pressure 2486=2465+18+3 unchanged. No original 8.0 artifact or PET runtime promoted.


## SRC-TW80-WAYI-2005-ARCHIVE-INDEPENDENT-PROVIDER-LOOKUP-20261012

- **Independent indexed public archive interface:** https://github-wiki-see.page/m/arquivo/pwa-technologies/wiki/Arquivo.pt-API documents Arquivo.pt `https://arquivo.pt/textsearch` original-URL `versionHistory` lookup, archival timestamp field and version list. This establishes *interface capabilities only*, NOT a verified historic Wayi capture.
- **Official archive explanation:** https://sobre.arquivo.pt/en/help/search-2/ makes explicit that archived dates are **capture dates**, not page publication dates; early site coverage may be sparse. 2005–2007 bounded lookups have no guaranteed completeness.
- **Original historical target remains:** `http://www.wayi.com.tw/stoneage/actives/940329/page_3.html` as cited by 2005-05-18 contemporary Taiwan StoneAge 8.0 preview https://www.games.idv.tw/news.php?mode=view&nid=326 . Existing Wayback CDX branch/main Action `TimeoutError` observations are network-indeterminate. Current original URL now renders modern Wayi site, NOT old 2005 page.
- **Probe/regression:** `tools/stoneage_tw80_arquivo_pt_index_probe.py`, 17 synthetic tests and Actions archive-index-only artifact, spec `docs/specs/STONEAGE-TW80-ARQUIVO-PT-INDEX-R1.md`. Any fresh index metadata must be separately verified; index digest is not original installer's file hash. No original game bytes/HTML are fetched or committed. Historical pressure 2486=2465+18+3, first-era/PET membership unchanged.


## SRC-TW80-VIP-DISC-20050606-REPOST-LINEAGE-20261012

- **Claimed dated headline (not original bulletin):** `親愛的石器時代VIP玩家 8.0光碟寄出` assigned to 2005-06-06 in subsequent community chronologies.
- **Earlier-attributed forum source:** `http://bbs.wayi.com.tw/viewthread.php?tid=40940` credited as **Mr.MIC, 2008-09-04** in [Bahamut historical repost](https://forum.gamer.com.tw/G2.php?bsn=1571&sn=1958). The original post is **not retrieved**; this is an attribution from a later copy, not a first-party Wayi 2005 news notice. A Wayi-hosted user forum is not automatically an official publisher voice.
- **Derivative copies, not independent corroboration:** [WeLoveSA historical forum copy](https://www.lab.welovesa.com/viewthread.php?tid=38); [ShiQi TV dated 2016-01-27](https://shiqi.tv/shiqi130.htm); other repeating chronicles. Identical June6 line suggests a single source lineage, not multiple independent 2005 confirmations.
- **Grade:** C, later community chronology claim. **Supports** targeted searching for a possibly separate VIP distribution channel and the *existence of the later dated claim*. **Does NOT support** successful original mailing, exact first-party 2005 text, CD/installer provenance, physical media custody, filename/label/matrix, SHA256, JSS1999/Taiwan1.0 membership or original PET equipment execution.
- **Keep channel identities separated:** 2005-06-04 contemporary *planned* event giveaway [GNN index](https://acg.gamer.com.tw/search.php?c1=976&c2=3&machine=1%2C0&s=2&type=1); 2005-06-06 later VIP headline; 2005-06-08 contemporary [GNN official release reporting](https://gnn.gamer.com.tw/detail.php?sn=20167). No data proves any two media identical.
- **Search-to-evidence gate:** retrieve original 2005 Wayi publisher page or no-cost provenance-preserving original disc image/manifest, followed by file-level verification. JSON `research/recovered/STONEAGE-TW80-VIP-JUNE6-DISC-SOURCE-R1.json`; `tools/stoneage_tw80_vip_june6_source_gate.py` mutation-controlled validator; `docs/specs/STONEAGE-TW80-VIP-JUNE6-SOURCE-GATE-R1.md`. No new original-client hash, no historical feature promotion and no change to pressure `2486=2465+18+3`.


## SRC-WAYI-2005-FIRST-PARTY-ARCHIVE-PAGE-BODIES-20261012

- **Actual archived operator HTML, first-party content with archive custody:** `https://web.archive.org/web/20050615023834id_/http://www.wayi.com.tw/stoneage/` and `https://web.archive.org/web/20050605002608id_/http://www.wayi.com.tw/stoneage/actives/940329/page_3.html`. Locally read Big5 responses 45669 and 9066 bytes; SHA256 and exact links retained in `research/recovered/STONEAGE-WAYI-2005-ARCHIVED-PAGES-R1.json`. Not operator-original executable hashes. Sliced event images not retrieved/interpreted.
- **Official download pointer and dating caveat:** `https://web.archive.org/web/20050405185635id_/http://www.wayi.com.tw/service/download_list1.asp?id=1` is actual destination of June/August replay requests; explicitly 7.5 full-client entry 2004-12-29 with `ftp://download.wayi.com.tw/stoneageinstall.exe`, and separate 2004-11-26 StoneAge2.exe `/download/download.asp?fileid=329`. Binary availability, hash and 8.0 identity OPEN. FTP CDX503 is not original-server404; launcher index302 records are not a recovered executable.
- **First-party developer index and PET preview:** `https://web.archive.org/web/20050612011406id_/http://www.wayi.com.tw/stoneage/producer/producer01.asp` links March3 PET idno109 and May31 8.0 idno121. Retrieved idno109 body capture `20051130002944`, while idno121 redirects to `20100711060206` and is quarantined as outside2005. Index entry date is not body capture date or software build date. Source supports publisher feature planning; not runtime opcode127 or inventory identity.
- **Reproducibility:** `tools/stoneage_wayi_archived_page_inventory.py` offline original-host and final-replay validation, nine functional tests, six real responses inspected. Spec `docs/specs/STONEAGE-WAYI-2005-ARCHIVED-PAGE-RECOVERY-R1.md`. Earlier CDX timeouts/Arquivo empty records remain true bounded search outcomes, not global absence. No original copyrighted bodies/software/assets committed; pressure2486=2465+18+3 unchanged.


### Same-round byte-level follow-through: official updater redirect recovered

Followed the archived November15 2005 fileid329 **302** without reading its body; Location identifies `http://www.wayi.com.tw/download/file/onlineGame/StoneAge2.exe`. Bounded raw replay recovered **113664 bytes**, actual final capture **2006-09-08 11:16:12**, SHA256 `a72a2fa646766f9c3a9a04f4340a3c7a1d76029d0c464bc7613f604a1900820f`. Static file/objdump inspection: PE32 i386 GUI, UPX0/UPX1/.rsrc sections; embedded ProductName SaUpdate, OriginalFilename SaUpdate.EXE, file/product version **1, 0, 0, 5**; COFF header timestamp May18 2005 11:26:56 UTC. No execution or unpacking. This is a real **operator-linked archived updater specimen**, not a recovered full 8.0 client. Archive capture is 2006, PE timestamp/resources are mutable and neither prove first-release version/date nor publisher-original checksum. No PET native execution or pressure change; updater bytes remain outside Git. Earlier same-round statements about unreceived launcher bytes are superseded by this bounded acquisition; original 8.0 installer remains OPEN. Metadata in `STONEAGE-WAYI-2005-ARCHIVED-PAGES-R1.json`.


## 2026-10-12 — Wayi first-party retained8.0 download-chain and static specimens R1

Original first-party URL http://www.wayi.com.tw/service/download_list1.asp?id=1; actual replay https://web.archive.org/web/20060221053354id_/http://www.wayi.com.tw/service/download_list1.asp?id=1 (37478 bytes/SHA25641cce148365b2c7bee1b4c1b2bb2c3efa83a36870108d994b046f120aae2758f). Retains2005 dated8.0 file entries; official FTP Stoneage80.exe pointer no bytes. Source chain335 original redirect at20051127031853 → official sa.exe; actual raw capture20060915184620 on original :80 URL,369152 bytes/SHA2564b5a059b45b589b609ca925d210d76838be1e970b805fab3df863b7d563fbb38. Default:80 origin equivalent without asserting two payloads equal absent hashes. Source333 redirect20050524233131 → adrn_129.rar, rawcapture20060911180132/3983427 bytes/SHA256b077dcc7f1e944c33c6df4fe629d5e37abce9cb4d40f5b8d800cc69d59416e25. Separate archive response/decompressed/tool hashes in derived ledger. Original game NEVER executed; no copyrighted original bytes committed. Official tool source https://github.com/upx/upx/releases/tag/v4.2.4. Page/file pointers authentic operator-origin archived source, exact2005 publisher release-byte equivalence remains OPEN. CDX lengths are archive records, not raw executable byte counts. Full-installer empty-index/404 and manifest404 are bounded retrieval outcomes; FTP503 indeterminate.


## 2026-10-12 — SRC-WAYI-SAUPDATE-8080-ROUTE-STATIC-R1

Static derivative of already accepted official-linked StoneAge2 response20060908111612/packedSHA256a72a2fa646766f9c3a9a04f4340a3c7a1d76029d0c464bc7613f604a1900820f; UPX-outputSHA256d0d9c33acc7eb47c2f625b827d5e30daccd29cb9782ff6c302b730e0a5406b2f. Capstone5.0.7 local decoder, exact hash/length gate, bounded executable windows, no original execution/network/server connection. New derived operand/literal/control metadata supports port8080 plus key-dependent route/local override; not selected runtime configuration. Full query URLs, dates/status/hash in STONEAGE-WAYI-SAUPDATE-MANIFEST-ROUTE-R1.json; replay404/index[] not global absence. Bounded host index includes2006 STONEAGE20060616.exe **404 record** only, no file bytes/version promotion. All original assets/executable bytes/disassembly text excluded.


## 2026-10-12 — SRC-WAYI-COMPILED-PET-SENDER-R1

Static derivative of accepted official fileid335→sa.exe chain, actual20060915184620 capture/packedSHA2564b5a059b45b589b609ca925d210d76838be1e970b805fab3df863b7d563fbb38; UPX-outputSHA2564193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63. Capstone5.0.7 and strict exacthash gate; derived cdecl argument expressions/helper window RVAs/coverage metadata only. Separately pinned BismarckDD/Stoneage999ffdf1d220ec6666eb65339180689c9caf1876 protocol/menu/autil blob identities support semantic comparison, not exactbuild provenance. 13 new functional negative/positive controls plus57 adjacent checks. Source admits compiled logical127 route, three direct callers and riding guard; rejects wire capture/server/owner/save/unique-code execution/exact2005 publisher hash. Originals never executed/committed; raw disassembly excluded. Ledger research/recovered/STONEAGE-WAYI-COMPILED-PET-SENDER-R1.json; spec docs/specs/STONEAGE-WAYI-COMPILED-PET-SENDER-R1.md.


## 2026-10-12 — SRC-WAYI-PET-TRANSPORT-JOIN-R1

Derivedstatic pathmetadata from acceptedoperator-linked20060915184620sa.exe, UPXoutputSHA2564193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63. Capstone5.0.7 strict16alignedwindows. FreshpinnedBismarckDD/Stoneage999ffdf1d220ec6666eb65339180689c9caf1876 autil369f2b35a812535557d55496626ff6a2cac1c56b/lssproto_util25ed992b6b9ba58ee174c2df5c4c6e970ba7ec95/menu62754fdd0db1b84c358d61418d253012d149e1d4/protocol17f1900d8845c15308a4b429905ec009e5fd4c0f/hbb70087ef1b1915748da23935584eda2c8178cb0 comparecompiledsend/receive/guard structure,notexactbuild identity. ObservedWSOCK32ordinal19 name independentlymapped by https://github.com/erocarrera/pefile/blob/v2024.8.26/ordlookup/wsock32.py; importordinalpreserved separately. 12newcontrols+70regressions. Ledger/spec STONEAGE-WAYI-PET-TRANSPORT-JOIN-R1. Nooriginalbytes/disassembly/runtime/serverpair/wirecapture committedorclaimed.


## 2026-10-12 — SRC-WAYI-COMPILED-PET-SB-STATE-R1

StaticderivedS46/Bstate metadata onacceptedoperator-linkedsa.exe archive20060915184620,UPXoutputSHA2564193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63. Capstone5.0.7,strict7alignedwindows/verifiedrawswitchtables/limitedaffineaddressandloopanalysis,14newcontrols+82regressions. FreshcomparisonBismarckDD/Stoneage999ffdf1d220ec6666eb65339180689c9caf1876 client/stoneage/system/netproc.cpp blob0dc677d3cd367ab89ca8d5becbb383bcbbccb3a8(Sline768,B1614..1696),systeminc/pc.h3425a4d7c9a275dc78643448a08d74b33e54cf1b,protocol.cpp17f1900d8845c15308a4b429905ec009e5fd4c0f/hbb70087ef1b1915748da23935584eda2c8178cb0. Semanticfields/sourceguardscomparedonly;expandedUTF8buffersandjigsaw50arenotnative388bytelayout. Clientdisplayrowsnotowner/globalitemidentity. Nooriginalbytes/disassembly/nativepacketexecution orreleasepromotion. Ledger/spec STONEAGE-WAYI-COMPILED-PET-SB-STATE-R1.


## 2026-10-12 — SRC-PET-SB-SERVER-COMPARISON-R1

Fresh publicGitHub BismarckDD/Stoneage HEAD2f736808ff4361f5429ee919b718c88fabb60346 separatelycompared withprior999ffdf1d220ec6666eb65339180689c9caf1876 (ninecommitslater,notoriginaloperatorbuild). Identicalchar_item970b7b3f975965c6c5e77352a2e0382adf943753/item94b00b11d02cc775bab6fe72c9c2ba77d9618712/autilc1f4886c879d6d847017cc53373e9e6ead28ae28; profile-specificchar_base/version/protocolwrapper IDs plus40 dependencyblobsperprofileinledger. GCCpreprocess only; defaultandexplicit-D_PET_ITEM separated, actual13-fieldpopulated/emptyformats andenum7/9 verified. Capturedclient14-fieldledger independentlyaccepted,notreplacedbydescendantcapacities. Originalsource/program/assets/disassembly excluded;18functional/mutationcontrols+96static/archivechecks andCI exactpinnedsource derivation. Source statusstringstrlen checksum/orderedoutputs/occupied-removalrange conflict only,noemittedwire/originalowner/save/provenance claims. Ledger research/recovered/STONEAGE-PET-SB-SERVER-COMPARISON-R1.json;spec docs/specs/STONEAGE-PET-SB-SERVER-COMPARISON-R1.md.


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

## 2026-10-12 — Reproducible TW1.0 savedata derived zero-run geometry R1

SOURCE CLASS: DERIVED secondary calculation from repository-pinned Taiwan v1.0 primary-byte statistical record research/recovered/STONEAGE-TW10-SAVEDATA-R1.txt (savedata SHA256 5b26f54a9723cd2c5275f964457094fdf1fc33ca086cdaf55bb5350dfb04f3f9, 128 bytes). New code tools/stoneage_tw10_savedata_geometry.py, seven tests tests/test_stoneage_tw10_savedata_geometry.py and spec specs/STONEAGE-TW10-SAVEDATA-ZERO-GEOMETRY-R1.md; branch Action38211434475 SUCCESS; main Action38211521969 SUCCESS. Reports seven isolated zero-byte starts 14,28,42,70,84,98,112, gaps 14,14,28,14,14,14 and GCD14; unmarked positive multiples56,126. IMPORTANT EVIDENCE LIMIT: no fresh original byte inspection or semantic mapping; periodic positions alone do not establish historical file layout or runtime IO. Receipt research/recovered/STONEAGE-TW10-SAVEDATA-GEOMETRY-ACCEPTANCE-R1.json. R3 four-address-word original-executable branch remains independently OPEN.

## 2026-10-12 — TW1.0 savedata R3 original acquisition timeout and tooling-only acceptance

OLD CI: Actions38209109437 (branch agent/tw10-savedata-four-words-r3-20261012) cancelled at the original archive.org CD_DIC.rar download step after 35-minute job timeout. 8 synthetic tests succeeded; original executable and savedata SHA256 were never freshly verified by R3; no derived binary-window artifact was generated. NEW CI: branch38212658702 and main38212722657 independently SUCCESS with 10 bounded tests on R1/R2 pinned metadata and synthetic instruction candidates; original gate explicitly NOT_RUN_IN_PUSH_CI. Source commit518a571abb8f4f1d5f53056401dba6be2f3071cc. Bounded workflow tools/stoneage_tw10_savedata_instruction_probe.py and .github/workflows/validate-stoneage-tw10-savedata-instruction.yml. Spec specs/STONEAGE-TW10-SAVEDATA-FOUR-WORDS-R3.md. Receipt research/recovered/STONEAGE-TW10-SAVEDATA-INSTRUCTION-TOOLING-ACCEPTANCE-R1.json. Classification FACT for verified CI/tooling status, OPEN for authentic early executable instruction alignment, savedata read/write behavior, framing and native behavior. Proprietary binaries not committed.

## 2026-10-12 — Taiwan 1.0 original archive transport endpoint experimentally recovered

FACT SOURCE: CI logs/actions 38214333386 (first transport,10tests SUCCESS),38214519509 (validated real storage `dir`,13tests SUCCESS),38214719068 (main independent success). Exact archive.org item metadata GET 200; catalog original CD_DIC.rar size842125501/MD5 b37a4a47f4eb608cac67e4ddf7a1621a/SHA1 b8cf92720b6ec8b3f46ea2e9bfcda986d21e7ded matching prior records; canonical /download HEAD+range HTTP500; catalog server /N/items/.../CD_DIC.rar Range0-4095 HTTP206 with matching Content-Range and 4096-byte read. First server HTTP404 from wrong /download path superseded as a routing error. Expires: server hostname dynamic; reconstruct from fresh archive-owned catalog, never freeze host as permanent provenance link. BOUNDARY: no complete original archive hash or original client verified by transport-only CI. Tool tools/stoneage_tw10_archive_transport_preflight.py, tests/test_stoneage_tw10_archive_transport_preflight.py, source receipt research/recovered/STONEAGE-TW10-ARCHIVE-TRANSPORT-ACCEPTANCE-R1.json. Original pinned acquisition Actions38215067915 pending and independently gated.

## 2026-10-12 — Taiwan v1.0 savedata original archive timed-download gates and R3 report guard

SOURCE/FACT GitHub Actions #38215067915: serial 16MiB ranges 134217728 /842125501 archive bytes completed before deadline540s; conclusion FAILURE; 10 synthetic tests PASS; no whole-archive hash or native instruction evidence. SOURCE/FACT Actions #38216336611: 12 parallel 8MiB ranges 469762048 /842125501 completed before deadline540s; conclusion FAILURE; 20 synthetic tests PASS; original archive hash, BIN extraction, sa_3.exe/savedata.dat SHA256 and native probe not reached. Both removed proprietary partials. Separate branch agent/tw10-savedata-original-gate-20261012 SHA7c944447fb35bbd0a4c2bf086cd50b2d3e825f28 increased parallel bounded 16 workers/acquisition deadline1500s, workflow job33mins: Actions38217343564 PENDING at this checkpoint, NOT accepted original bytes or R3 runtime fact.

SOURCE/ACCEPTED synthetic-only TW1.0 R3 report guard: branch Action38216975235 SUCCESS and main38217039742 SUCCESS (ten tests), commit61009048e6d14fe06ab64a81cbc643310e67afed, tool tools/stoneage_tw10_savedata_r3_report_guard.py and spec specs/STONEAGE-TW10-SAVEDATA-R3-REPORT-GUARD-R1.md. Validates four specific R2 address-word sites and original hash keys, rejects unknown text, wrong bounds and false runtime acceptance. Receipt research/recovered/STONEAGE-TW10-SAVEDATA-R3-REPORT-GUARD-ACCEPTANCE-R1.json. This is a REPORT-FORMAT gate, explicitly NOT evidence of original executable instruction reachability or local save I/O.


## 2026-10-12 — Taiwan 1.0 derived R3 report guard canonicalization (not historical source evidence)

CI/SOURCE: branch GitHub Actions38218339270 SUCCESS at commit9fa8d2677e2063b08cae5fdaa08ad6f44a260575, main Actions38218419412 SUCCESS at commitabf70446e0dd8f2141babe5de1f030a9770e2dd2; main log job114708530426 verifies 18 tests/OK and explicit R3_NATIVE_IO_SEMANTICS=OPEN. Static-report schema now pins exact boundary statement, four ordered word sites, candidate/API order, FILE_APIS allowlist, no repeated API keys/zero counts, numeric domain constraints and exact expected source SHA256 identifiers. This is an independently tested REPORT GRAMMAR fact, not an original-client runtime or provenance-bearing binary verification. Code/spec/tests: tools/stoneage_tw10_savedata_r3_report_guard.py, specs/STONEAGE-TW10-SAVEDATA-R3-REPORT-GUARD-R1.md and tests/test_stoneage_tw10_savedata_r3_report_guard.py. Receipt research/recovered/STONEAGE-TW10-SAVEDATA-R3-GUARD-CANONICAL-R2-ACCEPTANCE-R1.json. Original full-archive CI38217343564 separately pending at checkpoint; do not mistake canonical report shape for historical semantics.


## 2026-10-12 — Original Taiwan 1.0 disc static probe fully hash-verified; derived report independently validated

S-GRADE BYTES/DERIVED CUSTODY: Branch Action38217343564 SUCCESS (job114705061486) retrieved all 842125501 original archive bytes transiently using exact metadata-validated archive.org storage, verified MD5 b37a4a47f4eb608cac67e4ddf7a1621a and SHA1 b8cf92720b6ec8b3f46ea2e9bfcda986d21e7ded; unpacked STONEAGE.bin size523449360 and verified original embedded sa_3.exe SHA256 cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a plus savedata.dat SHA256 5b26f54a9723cd2c5275f964457094fdf1fc33ca086cdaf55bb5350dfb04f3f9. Original files deleted afterward; derived 869-byte zipped artifact ID11732992333 contains static candidates only. R3 rows show word RVAs 0x40065/0x400e5/0x40116/0x402a1, push candidate starts 0x40064/0x400e4/0x40115/0x402a0, no linear starts, no direct incoming edges, no forward64 file APIs. NO proof of native instruction execution, callsite reachability, early 128-byte format or checksum. Separate Action38218913015 (branch) and38218994589 (main) independently validated pinned run identity, exact derived artifact and strict guarded report/caveat; main Action38219152886 20 synthetic downloader tests/OK and no original data retrieval. Source integration main commit7c2bb5a3c1b2dadd0ce97818607ff0bd2a70830c. Receipt research/recovered/STONEAGE-TW10-SAVEDATA-ORIGINAL-R3-STATIC-ACCEPTANCE-R1.json; verifier .github/workflows/verify-stoneage-tw10-original-r3-derived-artifact.yml; acquisition .github/workflows/validate-stoneage-tw10-original-archive-gate.yml; no proprietary original payload archived in Git.


## 2026-10-12 — Taiwan 1.0 savedata R4 bounded entrypoint graph synthetic verifier

SOURCE/PROCESS: branch main integration bafc78d37260866ad770426a64862542bc00d52e, Actions38220633169 and38221329153 (9 bounded x86 graph synthetic tests); Actions38220978486 and38221340174 (13 derived report grammar/false-admission tests); independent main Actions38221434648 and38221434627 all SUCCESS. Eight additive source/spec/workflow/test paths including tools/stoneage_tw10_savedata_entrygraph_r4.py and tools/stoneage_tw10_savedata_entrygraph_r4_guard.py. Neither synthetic gate retrieves original executable bytes nor validates real control flow. Original source branch CI38220734211 pending in distinct 33-minute original static gate, never count as accepted until final report and exact immutable source/run check. Receipt research/recovered/STONEAGE-TW10-SAVEDATA-ENTRYGRAPH-R4-TOOLING-ACCEPTANCE-R1.json. No game assets or proprietary payload published.


## 2026-10-12 — Taiwan 1.0 R4 authentic original PE entrygraph and independent derived-only artifact proof

PRIMARY ARTIFACT/PROCESS: original archived retail CD_DIC.rar fully recovered transiently in Actions38220734211/job114716090868, 842125501 bytes, MD5 b37a4a47f4eb608cac67e4ddf7a1621a, SHA1 b8cf92720b6ec8b3f46ea2e9bfcda986d21e7ded; extracted STONEAGE.bin 523449360 bytes and accepted embedded sa_3.exe / savedata.dat SHA256 verified. Graph from PE entry0x4980a is bounded to .text RVA0x1000/raw331776, observed nodes31665/edges35092/indirect409/no cap; four original push candidates 0x40064/0x400e4/0x40115/0x402a0 each observed with one incoming static graph edge. No dynamic original-client execution. Original data transiently removed; only small derived JSON artifact11734033864 retained. Independent source-run/head verified and exact derived artifact parsed with strict no-runtime-claim R4 guard: Actions38221992415 (branch) and38222071494 (main) SUCCESS. Real savedata CreateFileA/ReadFile/WriteFile callsite+length+buffer still OPEN, and bounded entrypoint traversal cannot guarantee dynamic reachability. Source specs/STONEAGE-TW10-SAVEDATA-ENTRYGRAPH-R4.md; tools/stoneage_tw10_savedata_entrygraph_r4.py and strict guard; receipt research/recovered/STONEAGE-TW10-SAVEDATA-ENTRYGRAPH-R4-ORIGINAL-ACCEPTANCE-R1.json.


## 2026-10-12 — Taiwan v1.0 original R5 static callsite neighborhood acceptance source

SOURCE FACT: Branch Actions38223087375 at SHA9312a2f543fc8cb97b1c89d177050fcb6bebb893 downloaded and verified transient original CD_DIC.rar all842125501 bytes MD5 b37a4a47f4eb608cac67e4ddf7a1621a SHA1 b8cf92720b6ec8b3f46ea2e9bfcda986d21e7ded, BIN size523449360 and embedded sa_3.exe/savedata.dat exact R1 hashes. Source-run R5 extracted derived-only JSON artifact ID11735491592; original data purged. Per-four original sites shortest entrygraph paths226/216/226/259; predecessor edges all sequential; within 2048RVA/256-node direct forward static neighborhoods nodes34/158/73/34 and no recognized direct file APIs. Independent immutable source head/run and JSON schema verification branch Actions38223391602 and main38223493392 SUCCESS, strict/schema branch38223265258 and main38223493631 SUCCESS, graph-synthetic branch38223000995 and main38223493302 SUCCESS. No executable ran, no filename argument or native save IO established. Source tools/stoneage_tw10_savedata_callsite_r5.py and strict guard, spec specs/STONEAGE-TW10-SAVEDATA-CALLSITE-R5.md; receipt research/recovered/STONEAGE-TW10-SAVEDATA-CALLSITE-R5-ORIGINAL-ACCEPTANCE-R1.json. Archive original files and raw disassembly not published. Cross-function/indirect IO remains OPEN.


## 2026-10-12 — Taiwan 1.0 R6 common filename callee and cross-callee static APIs

PRIMARY BYTE CUSTODY: original branch source08d270a68974ada4186184a77310815493d21635, Actions38224760455/job114729428159 SUCCESS, catalog/full archive MD5+SHA1 and embedded original SHA256 verified; original media transient and purged. Derived-only artifact11735900423, zip SHA256 d56f1ec6495e93b1d98dab957d4f81b29835acab450871f2bf01f97137f870b4. Independent branch artifact verification38225088763 and main38225168390 SUCCESS; main synthetic38225168388 SUCCESS (33 R6+31 adjacent tests). Four filename pushes immediately CALL common0x487ba with physical slot0. Depth4 static cross-callee surface observes CreateFileA0x4ed01, ReadFile0x4a960/0x4aa31 and four other file API sites; seven unique sites repeat across four identical callee graphs.967 states/site,23 depth-limit stops, no node cap. No ABI/argument propagation/handle-buffer-length/native execution/128-byte format admitted. Tools/guards/spec and exact derived JSON research/recovered/STONEAGE-TW10-SAVEDATA-DATAFLOW-R6-ORIGINAL.json; acceptance receipt STONEAGE-TW10-SAVEDATA-DATAFLOW-R6-ACCEPTANCE-R1.json. No original bytes or raw disassembly in Git.


## 2026-10-12 — R7 filename argument-prefix tooling, no accepted original R7 result

TOOLING SOURCE: source892c4a229b8b126e14626ebaf21afa87a93d2940, branch synthetic Actions38227356828 and main38227454528 SUCCESS,34 R7 tests plus31 adjacent R4/R5 CI tests. Conservative register/stack filename provenance stops at unsummarized CALL, unknown alias and unmodeled memory. Synthetic Capstone x87 FSTP READ metadata counterexample forced explicit memory-stop hardening; not evidence of any historical FSTP in savedata code. Original source-run38226775676 at earliercf4d3cc07f333b57c4e4f96174d2b8c360f9e165 still downloading at checkpoint, predates hardening and is NOT original R7 evidence acceptance. Require hardened original rederivation plus independently pinned derived artifact. Tool/spec/guard/test/workflows; receipt research/recovered/STONEAGE-TW10-SAVEDATA-ARGTRACE-R7-TOOLING-ACCEPTANCE-R1.json. No original bytes/operand listings/assets or native IO published/executed.


## 2026-10-12 — R7 superseded original provenance and R8 helper effects tooling

SOURCE/PROCESS FACT: earlier original R7 Actions38226775676 SUCCESS (job114736106881), exact original archive/BIN/executable/save identity verified and purged; derived artifact11736099507. Sourcecf4d3cc07f333b57c4e4f96174d2b8c360f9e165 predates memory hardening; provisional149-state/8-CALL output remains superseded, not latest R7 argument evidence. Sequential corrected sourcea258a1097facaeef8ebd78535cbefd161836cc05 run38228357360 is independently IN_PROGRESS at acquisition checkpoint; accept no corrected original result yet. R8 synthetic helper-effect tooling source952b30bc3f08018434d423acd7709354043e4120: branch38229115129/main38229206436 SUCCESS (22 new+34 R7 tests),120 total local checks. Requires return-word/stack/cleanup/reg intersection, excludes cycles/caller-frame writes/unknown calls; no original helper, ABI or native IO admitted. Provisional/acceptance records research/recovered/STONEAGE-TW10-SAVEDATA-ARGTRACE-R7-PREHARDENING-PROVISIONAL.json and STONEAGE-TW10-SAVEDATA-HELPER-EFFECTS-R8-TOOLING-ACCEPTANCE-R1.json.


## 2026-10-12 — Hardened TW1.0 original R7 conditional prefixes accepted with immutable custody

PRIMARY/DERIVED FACT: original38228357360/job114741355427/sourcea258a1097facaeef8ebd78535cbefd161836cc05 SUCCESS; full archive and embedded exact original SHA identities verified, originals purged. Derived-only artifact11737238616 ZIP870/SHA2561ffed7900bc6212abc7fe5e2142ef210c379d014560eb4423f49ef6172a13abd. Independent branch38229857127/main38229979051 SUCCESS via immutable run/head and strict exact downloaded report comparison.136 conditional states/8 CALL rows/no API candidates; explicit unsupported_memory2 added to three alias/nine call-return/two depth/two return gaps. Physical filename stack0 forwarding0x487c4→0x4879a and next helper0x4b8a4 are bounded static observations, no ABI/full filename-to-API/native IO/128-byte structure proof. Pre-hardening149-state output retained as superseded. Receipt/report STONEAGE-TW10-SAVEDATA-ARGTRACE-R7-HARDENED-*.json; original helper returns remain independent and R8 only synthetic tooling accepted.


## 2026-10-12 — Taiwan v1.0 original helper0x4b8a4 bounded R8 diagnostics

PRIMARY/DERIVED SOURCE:575023511998fc4dcba61924504993be0e91fbbe original Actions38231508976/job114751844648 SUCCESS with full archive/BIN/embedded original hashes verified and payload purged. Derived-only artifact11738902238 ZIP862/SHA25628adb68cfea14017b50deafe1f7d2310428577d92e56a2c3e2e14ebe96b3f12c. Independent branch38232149568/main38232296065 SUCCESS via immutable source/run and strict exact downloaded JSON comparison; main synthetic38232296168 SUCCESS. Root0x4b8a4 conditional44-state analysis/two balanced return states at0x4b91b/common EBP-EBX-EDI-ESI, potential abstract cycle and remaining CALL0x4b8e2→0x4918f plus alias store0x4b903. Pure effect qualification FALSE; no historical helper summary/caller resumption/native IO/128-byte format admitted. Model cycle is not real nontermination proof. R8 report/acceptance STONEAGE-TW10-SAVEDATA-HELPER-R8-ORIGINAL*.json; new frontend+strict guard preserve no-payload boundary.


## 2026-10-12 — Original Taiwan1.0 R9 nested/helper-store-loop frontier

PRIMARY/DERIVED SOURCE e888222d95b8b43c13e03dca68e156cea6e98097, Actions38234280963/job114761003324 SUCCESS with original full archive/BIN/embedded hashes verified and proprietary data purged. Derived-only artifact11739214598 ZIP1058/SHA2567e6f69098d32f8d3db3d9429a5fffeeb3ddbddfe8eaf2292cf658196238b4d2b. Independent branch38235091041/main38235207142 SUCCESS; synthetic main38235206991 SUCCESS.0x4918f stops after3 states at CALL0x49199→0x491a1;4-byte store0x4b903 uses ESI with no mapped displacement/effective address/ownership proof. Parent contingent structure50 nodes/55 edges/one returned-CALL assumption;9-node SCC0x4b8c0..0x4b8d2 has JE/JE/JL branches and0 calls. Predicate values, actual runtime loop and object identity not established. R9 report/receipt STONEAGE-TW10-SAVEDATA-HELPER-FRONTIER-R9-*.json;137 adjacent+27 new local tests PASS; no native IO/caller resumption/128-byte format admission.


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


## SRC-TW10-SAVEDATA-UPSTREAM-R23 — 2026-10-13

- Type/confidence: S for hash-pinned original static derivative identity, with conditional interpretation only.
- Original source: Action38387323403/job115262191245, branch agent/tw10-savedata-r23-heap-links-20261013 at b53071fd45fab017704562d17d75bc59563ef01a; complete inherited R22 hash/identity gates, nonexecution and original cleanup PASS.
- Derived-only artifact11807077162, digest sha256:107a3f684e37caf3f544771163bed1ec0ff58484cca939ceac3f60bf240287bd; JSON11257 bytes SHA2568d77cdd314def89e534c725d5db3ffa1e004f3fb64141fe73b66f4ebc19751bc.
- Independent source/head/branch/artifact custody, strict guards and exact report comparison: Action38387607870/job115263140615 SUCCESS; synthetic58 tests Action38387607546 SUCCESS.
- Proves: bounded original syntax connecting three heap import sites with global EAX-store candidates and absolute global PUSH dependencies; conditional final PUSH offsets relative to ESP BEFORE HeapReAlloc.
- Does not prove: ABI argument roles, real entries/paths/values, import runtime execution, allocation success/common heap owner, original alias/caller effects, native save schema/IO or cross-version equivalence.
- Canonical derivative and receipt: research/recovered/STONEAGE-TW10-SAVEDATA-UPSTREAM-R23-ORIGINAL.json and STONEAGE-TW10-SAVEDATA-UPSTREAM-R23-ACCEPTANCE-R1.json.


## SRC-TW10-SAVEDATA-UPSTREAM-R24 — 2026-10-13

- Confidence S for pinned original static identity; all entry/path/value interpretations conditional.
- Original source Action38389572994/job115269723886, branch agent/tw10-savedata-r24-prefix-scalar-flags-20261013 HEAD1348831660debb1e86b4dec6cd270f2dcba3e126; inherited whole-archive/runtime/savedata and exact R23 derivative gates, nonexecution and original purge PASS.
- Derived-only artifact11807971334 ZIP digest sha256:27b0d78b1a80f7d2c8d60f8e4f2081e0311f4dc32b60dc85ca33781196b16e04; JSON14547 bytes SHA25671a781bd740845d388284ea68fa3e271ef5c5b6eac556f4e487d4eaaa0047af1.
- Independent original/head/branch/artifact custody, strict guards and exact JSON equality Action38389832057/job115270597813 SUCCESS; synthetic/adjacent R23 regressions62 tests38389574287 SUCCESS.
- Proves bounded original SETE AL barrier, three HeapAlloc PUSH operands under wider candidate prefixes, conflicting instruction spans between candidate starts, SHL2/LEA EAX input geometry and a comparison-defined JNE candidate.
- Does NOT prove original verified instruction/function entries, feasible paths, EAX upper bits, ABI roles, actual heap size/success/owner, native file/handle/buffer linkage/save IO or cross-version semantics. Earlier alternate-anchor memory-add candidate is not accepted as an original executed store.
- Canonical report/receipt: research/recovered/STONEAGE-TW10-SAVEDATA-UPSTREAM-R24-ORIGINAL.json and STONEAGE-TW10-SAVEDATA-UPSTREAM-R24-ACCEPTANCE-R1.json. Next R25 coherent boundary/caller candidates before any allocator-context or native-IO promotion.


## SRC-TW10-SAVEDATA-UPSTREAM-R25 — 2026-10-13

- S-grade identity for hash-pinned original static derivative; all entry/path/value interpretations conditional.
- Original source Action38392504284/job115279484570, branch agent/tw10-savedata-r25-boundary-callers-20261013 HEAD2437eac2c14bf8e8f983f0891effd055f8cd2940, whole-archive/runtime/savedata and exact R24 report gates rederived, nonexecution and originals purge PASS.
- Derived-only artifact11809322312 ZIP digest sha256:656285d461cd9306d979678ca53fa3dfbdeac886743041d836465648d553dc8a; JSON12484 bytes SHA2563f345e590290eb3f30962e4640f3eec23458fc8fa67c22118b7ef832a5595282.
- Independent source/head/branch/artifact custody, strict tamper limits and exact original-derived JSON equality Action38392864515/job115280700338 SUCCESS;59 synthetic/adjacent R24 tests38392504100 SUCCESS.
- Proves full raw .text candidate spans supporting boundary corrections;19 direct transfer candidates in two bounded windows,6 CALL sites/4 CALL-target candidates; new-start ECX source .data0x1721864; old SETE contexts fail to reach the target under bounded graph rules.
- Does NOT prove executed/complete alignment, true entries/complete callers (677 indirect transfers unresolved), feasible paths, whole EAX/flags/global values, ABI/heap/CRT owner or native save format/IO.
- Canonical report/receipt: research/recovered/STONEAGE-TW10-SAVEDATA-UPSTREAM-R25-ORIGINAL.json and STONEAGE-TW10-SAVEDATA-UPSTREAM-R25-ACCEPTANCE-R1.json. Next R26 use0x499c3/0x4a09c direct CALL-supported candidates before native IO context promotion.


## SRC-TW10-SAVEDATA-UPSTREAM-R26 — 2026-10-13

- S-grade pinned original static identity, all runtime/entry/ABI/ownership interpretations conditional.
- Original source Action38394940020/job115287645291, branch agent/tw10-savedata-r26-call-root-inputs-20261013 HEADe16213cb60a1a560fa31a9d15fad39626e9052e6; complete archive/runtime/savedata and exact R25 JSON gates rederived, nonexecution/static-only and original purge PASS.
- Derived-only artifact11811375871 ZIP digest sha256:6f3c6e8919ec3d7ee2922db1c59bbbf7f6fade1554c6aeef1e9023b26bd69e14; JSON9053 bytes SHA256ff829f3aa6b1ebfaf2f2d251581293ca734ef4837f7276f54000f364085b2122.
- Independent original/head/branch/artifact custody, strict model/tamper limits and exact JSON equality38395234686 SUCCESS;56 synthetic/adjacent R25 tests38394939510 SUCCESS.
- Proves bounded CALL-supported EAX/flag input candidates, conditional partial-register composition, two separate global memory-load sources and unique LEA/SHL conditional u32 arithmetic relation.
- Does NOT prove actual EAX/ZF/ECX/global contents, frame/argument or ABI roles, heap creation/reallocation size/success, CRT/FILE/object/alias ownership, caller effects or native persistence/schema/IO.
- Canonical report/receipt: research/recovered/STONEAGE-TW10-SAVEDATA-UPSTREAM-R26-ORIGINAL.json and STONEAGE-TW10-SAVEDATA-UPSTREAM-R26-ACCEPTANCE-R1.json. Next R27 return to exact original native file-API boundary/caller/argument chain while retaining allocator gaps.


## SRC-TW10-SAVEDATA-NATIVE-IO-R27 — 2026-10-13

- S-grade exact pinned original static identity; runtime/entry/ABI/ownership interpretations conditional.
- Original source Action38398995246/job115301450444 SUCCESS at branch agent/tw10-savedata-r27-native-io-sites-20261013 HEAD51cbe0b354e5865203c48512348dec74ff4521a1; inherited archive/runtime/savedata identity and exact R26 derivative SHA256ff829f3aa6b1ebfaf2f2d251581293ca734ef4837f7276f54000f364085b2122 rederived/strict guard PASS. Derived-only artifact11813083292 ZIP digest sha256:f6d0664760b93e1df84c7509839e2e8a0915cf51525e266005f753f3292871c7; JSON42859 bytes SHA2561c77b3c327a216729c1a66693d8dcb3be1c82205676365198fc5028239a12548. Final56 local and remote R27+R26 synthetic/guard tests Action38398996562/job115301454794 SUCCESS. Independent immutable run/head/branch/artifact custody, strict tamper constraints and EXACT committed-original-derived JSON equality Action38399287798/job115302439528 SUCCESS at HEAD14bfea543f71c64fd1867192f54dd5dc420b2803; local report equals independently logged JSON. Initial source38398758484 failed on a far CALL outside near-import identity scope, then superseded by an explicit near CALL filter and adversarial far CALL test. No original program executed or proprietary bytes/assets/code payload published; all transient originals purged.
- Establishes seven imported API CALL candidates (2 CreateFileA,2 ReadFile,3 WriteFile), five bounded physical PUSH suffixes and14 nearby direct caller candidates. Third WriteFile/early CreateFileA remain inventory-only; unreachable graph at WriteFile0x4c6f1 stays explicit.
- Does NOT establish savedata/API filename link, returned file handle, actual buffer/length128, native schema/persistence, true entry/frame/ABI/CRT/heap/alias owner or external-return effects.
- Canonical report/receipt: research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R27-ORIGINAL.json and STONEAGE-TW10-SAVEDATA-NATIVE-IO-R27-ACCEPTANCE-R1.json. R28: audit direct CALL-supported original contexts0x4eb55 (CreateFileA),0x4a8dc (ReadFile) and0x4c5b4 (WriteFile), with explicit span/path/entry bounds; trace EBP-frame inputs and [EBX]/[EAX+ESI] handle-like syntax as candidates, never actual handle ownership. Correct WriteFile0x4c6f1 unreachable heuristic root before using its sources; extend bounded analysis to third WriteFile0x4e42b if useful. Native savedata filename->returned handle->buffer/length128 remains OPEN.


## SRC-TW10-SAVEDATA-NATIVE-IO-R28 — 2026-10-13

- S-grade original hash-pinned static syntax; actual path/frame/ABI/ownership interpretations conditional.
- Original source Action38400713383/job115307314019 SUCCESS at branch agent/tw10-savedata-r28-call-supported-io-20261013 HEADd33cacc472793a38422d9e9cf60107c585e3edf8; complete inherited archive/runtime/savedata identity and exact R27 original JSON SHA2561c77b3c327a216729c1a66693d8dcb3be1c82205676365198fc5028239a12548 rederived/strict guard PASS. Derived-only artifact11814279564 ZIP digest sha256:348ae91b6727a24a2b3db2685d007aace1c814e98eb5c564f7b91e27ef15d967; JSON56581 bytes SHA256296e5754a3eebafc6360cc45000ba73b6bcf1cc0a5d0ee439aa291eb45e0d645. Final58 local and remote R28+R27 synthetic/guard tests Action38400714689/job115307317417 SUCCESS. Independent immutable original-run/head/branch/artifact custody, strict tamper controls and EXACT committed-original-derived JSON equality Action38400948159/job115308122805 SUCCESS at HEAD7b641d78b893f68a3be4e088b16892f05b777205; local report equals independently disclosed JSON. Initial successful source38400524565 superseded by complete-instruction-inside-byte-window hardening and an adversarial spanning-instruction control. Original programs never executed and proprietary bytes/assets/code payload never published; transient originals fully purged.
- Recovers CALL-supported graphs230/271,174/200,139/156 and five API sites; WriteFile0x4c6f1 reachable from0x4c5b4; shared virtual writable .data displacement0x1721760 with4*EAX index candidates and bounded dependency inputs15/36/29.
- Does NOT establish actual table contents/initialization/index/handle/owner, caller ESP/frame/arguments, original filename/buffer/length128/native save/schema, API returns or callee/register preservation.
- Canonical report/receipt: research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R28-ORIGINAL.json and STONEAGE-TW10-SAVEDATA-NATIVE-IO-R28-ACCEPTANCE-R1.json. R29: inspect exact original operand shapes and conditional scalar input provenance at ReadFile index definition0x4a8f9/ESI0x4a8fc and WriteFile index0x4c5d3/ESI0x4c5e0 plus EAX0x4c617. Qualify the shared0x1721760+4*EAX addressing candidates without evaluating original values or asserting a handle-table owner; audit bounded writes/references if useful. Continue filename/CreateFileA-return/handle/buffer/length128 linkage with explicit opaque-call, cycle, stack-frame and memory-alias gaps. Native schema/persistence remain OPEN.


## SRC-TW10-SAVEDATA-NATIVE-IO-R29 — 2026-10-13

- S-grade original hash-pinned static syntax; runtime/entry/frame/ABI/ownership interpretations conditional.
- Original source Action38402348628/job115312903541 SUCCESS at branch agent/tw10-savedata-r29-scalar-address-20261013 HEADdc54d8d72591437b05e2f30b779e7f5b8f041912; complete inherited archive/runtime/savedata identity gates and exact original R28 JSON SHA256296e5754a3eebafc6360cc45000ba73b6bcf1cc0a5d0ee439aa291eb45e0d645 rederived/strict guard PASS. Derived-only artifact11815337939 ZIP digest sha256:1b9a07e2c076bc7e7642810b13a8b8e40973f2ff362c4b4350a9a2e1eb7903a2; JSON25275 bytes SHA256151b846b843165c0cf5002792f4a43904d7f2b6a3683e1d951ea3d6cf5dbe415. Final64 local and remote R29+R28 synthetic/strict tests Action38402348702/job115312903982 SUCCESS. Independent immutable run/head/branch/artifact custody, strict tamper controls and EXACT committed-original-derived JSON equality Action38402645534/job115313933808 SUCCESS at HEAD3e092080f1475d0e53c40858ed81dc58f03bbde1; local report equals independently disclosed JSON. No original runtime program or original-state arithmetic executed; no proprietary byte/asset/code payload published; transient originals fully purged. Intel official SDM Vol2B SAL/SAR/SHL/SHR printed4-584/4-585 checked for conditional shift mathematics; its architecture semantics do not establish historical original values.
- Establishes two original SAR EAX5, two SHL ESI3 and one ADD EAX,ESI shapes with separate bounded conditional u32 models; two shared LEA displacement/index candidates and25 exact address/displacement operand references (no sample truncation).
- Direct MOV destination0x4c9da and immediate-address0x4e77f are discovery candidates, not proven original initialization/complete writers or function owners.
- Does NOT establish scalar/index/frame values, table contents/owner, caller returns, original filename/handle/buffer/length128, native schema/persistence or cross-version equivalence.
- Architectural reference (not historical runtime evidence): Intel SDM Vol2B SAL/SAR/SHL/SHR, printed4-584/4-585, https://www.intel.com/content/dam/www/public/us/en/documents/manuals/64-ia-32-architectures-software-developer-vol-2b-manual.pdf .
- Canonical report/receipt: research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R29-ORIGINAL.json and STONEAGE-TW10-SAVEDATA-NATIVE-IO-R29-ACCEPTANCE-R1.json. R30: inspect exact input definition shapes0x4a8f6/0x4c5d6 before SHL to qualify any conditional index/offset composition without asserting actual descriptor values, ranges or ownership. Audit direct MOV-to-shared-global candidate0x4c9da source and acquire coherent boundary/direct CALL support before using its context; immediate-address candidate0x4e77f may aid discovery. Continue native CreateFileA returned-handle capture and filename->handle->buffer/length128 with explicit call/stack/alias gaps; no CRT/table/native schema/persistence promotion.


## SRC-TW10-SAVEDATA-NATIVE-IO-R30 — 2026-10-13

- S-grade pinned original static syntax; runtime/path/frame/ABI/ownership interpretations conditional.
- Original source Action38404299461/job115319726044 SUCCESS at branch agent/tw10-savedata-r30-mask-writer-20261013 HEAD724838fa88ebbfc381a0deec73edce4e467a8090; complete inherited archive/runtime/savedata identity gates and exact original R29 JSON SHA256151b846b843165c0cf5002792f4a43904d7f2b6a3683e1d951ea3d6cf5dbe415 rederived/strict guard PASS. Derived-only artifact11818650369 ZIP digest sha256:f49a3be1be1014e8cb9d966540c0dbdd5fcc0654f772b1319293013f3cfccf21; JSON12559 bytes SHA256760730dc57c823a7279b22a0944ffaac588e77d4fb6b0d5f5024265345f0b45a. Final61 local and remote R30+R29 synthetic/strict tests Action38404299604/job115319727392 SUCCESS. Independent immutable run/head/branch/artifact custody, strict tamper controls and EXACT committed-original-derived JSON equality Action38404780799/job115321429623 SUCCESS at HEAD7822838f659f76fc140b991b3524bba2280a913d; local report equals independently disclosed JSON. Original runtime/programs and original-state arithmetic never executed; no proprietary byte/asset/code payload published; transient originals fully purged.
- Establishes two original AND31->SHL3 unique candidate links and conditional u32 composition; eight nearby direct CALL targets, two linear boundary roots, physical ESI store0x4c9da to0x1721760 and143/164 writer-reaching context at0x4c9ba.
- Root0x4c953 graph26/29 does not reach shared-global writer; CreateFileA numeric-continuation CALL0x4ed26->0x4c953 stays a native-return-capture discovery candidate.
- Does NOT establish actual scalar/descriptor/offset/frame values, global initialization/contents/owner, complete aliases/writers, API/callee effects, native filename/handle/buffer/length128/schema/persistence or cross-version equivalence.
- Canonical report/receipt: research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R30-ORIGINAL.json and STONEAGE-TW10-SAVEDATA-NATIVE-IO-R30-ACCEPTANCE-R1.json. R31: return to original CreateFileA0x4ed01 conditional continuation from0x4ed07 and audit direct CALL0x4ed26->0x4c953 (exact R30 scan candidate). Recover physical PUSH/register sources and bounded callee memory-store candidates, with explicit entry/path/return/stack/alias uncertainty; no actual API EAX/handle success or CRT/FILE owner admission. Retain global writer0x4c9ba's opaque calls0x4c9c6/0x4c9d4 as independent initialization gaps, audit their identities only if useful, and do not block the whole native save chain on generic allocator exhaustion. Filename->returned handle->ReadFile/WriteFile buffer/length128/schema/persistence remain OPEN.


## SRC-TW10-SAVEDATA-NATIVE-IO-R31 — 2026-10-13

- S-grade pinned original static syntax; runtime/entry/path/frame/ABI/ownership interpretations conditional.
- Original source Action38406412226/job115327068789 SUCCESS at branch agent/tw10-savedata-r31-create-capture-20261013 HEADe3b2d5b75668b0823573f499b11f9ee46883f6f0; complete inherited archive/runtime/savedata identity gates and exact original R30 JSON SHA256760730dc57c823a7279b22a0944ffaac588e77d4fb6b0d5f5024265345f0b45a rederived/strict guard PASS. Derived-only artifact11816674613 ZIP digest sha256:296aa126d7f52c4bc8c8ca54183eaaf7868ed0d309bca6bd4531c2173c23a075; JSON13684 bytes SHA256af1e1ee0fb61549e89b6e168e82c5c7b58de170e9a1bb7f9ed2968c095cebdcc. Final59 local and remote R31+R30 synthetic/strict tests Action38406413334/job115327073411 SUCCESS. Independent immutable run/head/branch/artifact custody, strict tamper controls and EXACT committed-original-derived JSON equality Action38406921461/job115328837823 SUCCESS at HEAD51182cbed7eac17731f2c3fe173d0e541ddaca39; local report equals independently disclosed JSON. Original runtime/programs never executed; no proprietary byte/asset/code payload published; transient originals fully purged.
- Establishes opaque CreateFileA EAX->ESI copy0x4ed07, distinct UNKNOWN_CALL0x4ed1f source of PUSH EAX0x4ed25 and exact CALL0x4ed26->0x4c953. Earlier numeric continuation discovery does not qualify native-handle argument binding.
- Helper26/29 graph contains five explicit MOV candidates to0x172120c/0x1721208, one [ESP+4] operand, literal13/8/22 and EAX load0x6484c+8*EDX; no actual mapping/index/global/owner facts.
- Does NOT establish actual returned handle/success, caller stack/parameter linkage, helper/CRT identity, complete aliases/writers, native filename/buffer/length128/schema/persistence or cross-version equivalence.
- Canonical report/receipt: research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R31-ORIGINAL.json and STONEAGE-TW10-SAVEDATA-NATIVE-IO-R31-ACCEPTANCE-R1.json. R32: identify original intervening CALL0x4ed1f and the predicate/branch reaching0x4ed26 to qualify the helper's mapping-like role. If justified, audit conditional physical PUSH EAX offset0 -> helper entry [ESP+4] hardware geometry separately from any API return/owner claim. Resume captured ESI0x4ed07 along other candidate parent paths and inspect parent memory-store/call inputs; do not mistake0x4c953's globals for the shared0x1721760 address candidates. Actual filename->CreateFileA result->ReadFile/WriteFile buffer/length128/schema/persistence, alias/frame/return effects and CRT/heap ownership remain OPEN.


## 2026-10-13 — R32 original GetLastError provenance — accepted

- Source type: authenticated nonexecuted Waei/JSS TW1.0 clean retail binary/PE import table and bounded x86 static graph, inherited R31 exact SHA256af1e1ee0fb61549e89b6e168e82c5c7b58de170e9a1bb7f9ed2968c095cebdcc.
- Original Action38409002824/job115336054231 SUCCESS HEAD55bb9c76b4d13215332cffc0a649e869c72d0188. Only derived JSON uploaded: artifact11820641198 ZIP SHA256efa5c1a68f44893654d77c3596afe1bf0f9a4644208c8238013b4bf8ebcfdb46; JSON5153 bytes SHA25624849b161be51b4fbf50fa7fe2c2bb48b6e79a6a83fb012f33ddd961f6336c9c. Native binaries not executed or published, transient originals purged.
- Independent source/run/artifact validation38409252712 SUCCESS; exact original JSON equality with committed research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R32-ORIGINAL.json at38409470522 SUCCESS; strict tamper/negative tests PASS.
- FACT static: CALL0x4ed1f imported KERNEL32.dll!GetLastError through IAT0x5208c; JE0x4ed0b to0x4ed1f and JNE0x4ed16 to0x4ed33 direct branch syntax; prehelper PUSH EAX0x4ed25 to helper [ESP+4]0x4c953 conditional hardware slot only, no caller-callee value binding; second JNE target not structurally reaching helper while modeled fallthrough does.
- HYPOTHESIS mapping/error-path helper; not a demonstrated runtime outcome. OPEN: actual branch/flags, CALL return effects, file handle, CRT/heap/alias owner, native filename/buffer/length128/schema/persistence. NEXT R33 original CALL0x4ed19 and branch predicate/flags. Scope docs/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R32.md.


## 2026-10-13 — R33 original CloseHandle and ZF provenance — accepted

- Source: pinned authenticated nonexecuting Taiwan Waei/JSS StoneAge v1.0 original retail client, full inherited R32 canonical SHA25624849b161be51b4fb50fa7fe2c2bb48b6e79a6a83fb012f33ddd961f6336c9c revalidated against the exact original executable and save data.
- Source Actions run38411584532/job115345021284 SUCCESS HEADf0fe4a5491ac031f2bc941de6c335b85a1273ea4, temporary originals purged and neither executed nor published. Only bounded derivative artifact11822641076 name tw10-r33-original-secondary-call-zf-derived, ZIP SHA256:01286152611e96bc6e9dac874422227336b5b8f84397fcb20b9b4560d54894bc; original-derived JSON4772 bytes SHA2561be7d372b0650b9944a12264b612531d46a5326af3628e12363df365ddab98b5.
- Independent run38411779674/job115345684881 verified run/branch/HEAD/artifact custody, strict semantic guard, tamper tests and disclosed bounded JSON. Run38411925788/job115346184238 verified committed canonical JSON exactly equals independent original-derived JSON. All gates SUCCESS.
- FACT, original static only: memory indirect CALL0x4ed19 associates KERNEL32.dll!CloseHandle at IAT0x520a8, distinct from original GetLastError0x4ed1f and CreateFileA0x4ed01. JE0x4ed0b has single candidate ZF writer CMP ESI,EDI0x4ed09; JNE0x4ed16 has single candidate writer TEST EAX,EAX0x4ed14. No capped/trimmed branch predecessor sample, four register-query surfaces, but no actual input values, path feasibility or branch taken.
- OPEN: EDI sentinel or identity, EAX input, actual CloseHandle argument/return, original CreateFileA handle success, native file/CRT/heap alias/owner, read/write buffer length128/schema/persistence and server-only/cross-region equivalence. R34 next: trace EDI/EAX and pre-CloseHandle PUSH/branch exit. Canonical JSON research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R33-ORIGINAL.json; scope docs/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R33.md.


## 2026-10-13 — R34 original CloseHandle PUSH provenance — accepted

- Source type: pinned authenticated Waei/JSS TW1.0 original retail client, exact previously accepted R33 original JSON SHA256:1be7d372b0650b9944a12264b612531d46a5326af3628e12363df365ddab98b5 rederived and guarded. Original static only; no native executable run.
- Original Actions38413940213/job115353221738 SUCCESS at agent/tw10-savedata-r34-cmp-close-inputs-20261013 HEAD44c96a0a3195fb847b7d443ca4fadb22e8d7e65a. Temporary original archive/client purged, no proprietary binary or artwork/code published. Derived-only artifact11822613944 name tw10-r34-original-cmp-close-inputs-derived, ZIP SHA256:29057dd97c3275122b009c6f205c0585000b49dc0d630460e8ed78a3163d6f4e; original-derived JSON5542 bytes SHA256:e95548eb5e9b60b1f5214ed751c1f3df9b83f27a4d20ebe35a49427cf9b32c34.
- Separate independent artifact/source identity and strict negative controls Action38414131854/job115353899310 SUCCESS; committed original-derived JSON exact equality Action38414279033/job115354415334 SUCCESS. Inherited R33 and R34 synthetic tests PASS.
- FACT bounded original static syntax: CMP ESI,EDI0x4ed09 source ESI <- MOV ESI,EAX0x4ed07 and EDI <- UNKNOWN_CALL0x4ed01 (CreateFileA import). TEST EAX,EAX0x4ed14 source UNKNOWN_CALL0x4ed0e. Single pre-CloseHandle PUSH ESI0x4ed18 at conditional ESP offset0, with ESI <- UNKNOWN_CALL0x4ed0e. There is no proven EDI sentinel, original API success, handle ownership, runtime parameter, branch-taken, file schema or persistence.
- Highest next R35: independently resolve original CALL0x4ed0e identity/input and preserve conservative return/alias uncertainty. Native filename->CreateFileA-result->ReadFile/WriteFile buffer/length128/schema/persistence remain OPEN. Canonical research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R34-ORIGINAL.json; scope docs/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R34.md.


## 2026-10-13 — R35 original GetFileType static import association (accepted, S-level original source)

- Source: authenticated Taiwan Waei/JSS v1.0 original retail binary (pinned clean source), PE import table and bounded x86 nonexecuting static inspection, exact inherited R34 original JSON SHA256 e95548eb5e9b60b1f5214ed751c1f3df9b83f27a4d20ebe35a49427cf9b32c34.
- Original Action https://github.com/chinaneedM/stoneage-rebuild/actions/runs/38418400068, job115368863099, HEADa02fd2464424a1974bcdf954aad0894589052614 SUCCESS. Artifact11824229823 ZIP SHA256 4c5cdd8677641d5588d738aa3286a0931e4c06590405f61fcffbd7901f483f33. JSON5348 bytes SHA256 5052a3d57b89f1d257846df6cef7c513fe544cadeb420e11f0a18468d3908f23.
- Independent immutable source/run/artifact custody, synthetic and tamper controls and strict semantic validator run38418921425/job115370708502 SUCCESS. Committed canonical exact JSON equality run38419262860 SUCCESS. Original executable/media not executed or published; temporary original bytes purged.
- FACT conditional static only: original memory-indirect CALL RVA0x4ed0e IAT0x52160 -> KERNEL32.dll!GetFileType; straight suffix PUSH ESI0x4ed0d at pre-call ESP offset0; ESI source MOV ESI,EAX0x4ed07 candidate with CreateFileA0x4ed01 as opaque predecessor, EAX at TEST0x4ed14 opaque GetFileType CALL, and ESI before CloseHandle0x4ed19 unknown across CALL. Graph230 nodes/271 edges with returning-call structural assumption.
- DOES NOT PROVE: executed call, GetFileType's real argument or returned file type, CreateFileA returned handle success, EDI invalid handle sentinel, branch decision, CloseHandle argument, alias ownership, filename, ReadFile/WriteFile concrete buffers/length128/schema/persistence, equivalent server-side saving or cross-version content. Strict distinctions retained.
- Canonical derived report research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R35-ORIGINAL.json; scope docs/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R35.md. NEXT R36: conditional GetFileType TEST/JNE and original argument/handle candidate linkage, evidence-bounded only.


## SRC-TW10-SAVEDATA-NATIVE-IO-R36 — 2026-10-14

S-grade authenticated nonexecuting TW1.0 retail binary, original PE/operand/topology syntax only; all runtime/ABI/owner interpretations conditional. Original source Action38488978148/job115609407671 SUCCESS HEAD9a0552bf360223eee6bf050da1872ca4e73d81fe with exact R35 canonical SHA2565052a3d57b89f1d257846df6cef7c513fe544cadeb420e11f0a18468d3908f23 rederivation. Derived-only artifact11860393895 ZIP SHA256f86407b7a9489ce783888022d3be9ca3f2eb519203a732cfb97b3febc2e39629; JSON24033 bytes SHA256872dbbf431891c19c27ddb0f6f5e87c466e89231e87e1a615a808aac0288a91c. Independent immutable source/artifact identity, pinned JSON digest/size, strict negative gates and exact canonical equality Action38489210950/job115610153818 SUCCESS. Final81 tests PASS; originals purged/unexecuted/unpublished.

Static230/271 bounded graph, TEST/JNE symbolic zero/nonzero shapes, six structural route corridors, two same-spelling PUSH ESI operands (no value binding), and three continuation MOV-to-memory candidates with low-byte projections and separate address inputs. Sixteen queries, no graph/query/store cap; partial-register writes and all API effects remain unknown. Does not establish successful handles, actual API arguments, branch feasibility, frame/alias/CRT ownership or native filename/buffer/length128/schema/persistence. Canonical report research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R36-ORIGINAL.json; scope docs/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R36.md. R37 queued for continuation helpers and store/address candidate qualification. Stage A only.


## SRC-TW10-SAVEDATA-NATIVE-IO-R37 — 2026-10-14

S-grade authenticated TW1.0 original nonexecuting PE/static operands and bounded graphs; runtime/ABI/owner interpretations conditional. Exact R36 JSON SHA256872dbbf431891c19c27ddb0f6f5e87c466e89231e87e1a615a808aac0288a91c rederived/guarded. Final original Action38491613508/job115617870380 SUCCESS HEADdbc96073e032b2508e00ea23ba684902d8c68aeb; derived-only artifact11861673941 ZIP SHA25680a8bb5ff3233cd13f2a2a86558a228af782cfee9d0192bca18d3135a002cd58; JSON53751 bytes SHA256a16c858a46d502dec5c99fe43528601f0bc89449c671a717198725c95aa496d0. Independent immutable original/artifact custody, pinned digest/size,112 synthetic/tamper gates and exact committed-original JSON equality Action38491820292/job115618544412 SUCCESS. Originals purged, unexecuted and unpublished.

Static direct CALL-supported helpers0x4e80a/0x4c761, candidate linear boundaries,44/49 and51/55 graphs,12/15 memory refs,16/14 input queries, no caps. Both share0x1721760+4*ECX reference syntax; no original table/owner/content admitted. Imported SetStdHandle/SetFilePointer/GetLastError and conditional caller PUSH suffixes do not establish real handles, arguments, results, seek/persistence or CRT identity. Corrects provisional partial-write grouping: OR AL,1 is partial; SAR ECX,5/SHL ESI,3 are full32-bit. Unmodeled inputs and opaque calls remain OPEN. Canonical report research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R37-ORIGINAL.json; scope docs/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R37.md. NEXT R38 stack-prefix/store/source qualification. Stage A only.

Architecture reference (not historical original execution): Intel SDM Vol1 §3.4.1/Figure3-5, printed3-12 / PDF page74, https://www.intel.com/content/dam/www/public/us/en/documents/manuals/64-ia-32-architectures-software-developer-vol-1-manual.pdf ; IA-32 byte/word aliases. R29's official Intel SDM Vol2B scalar instruction references and synthetic u32 models reused for full-width shifts. No original values evaluated.


## SRC-TW10-SAVEDATA-NATIVE-IO-R38 — 2026-10-14

S-grade authenticated TW1.0 retail original nonexecuting PE/operand/topology evidence; stack/ABI/value/owner interpretations conditional. Exact R37 original SHA256a16c858a46d502dec5c99fe43528601f0bc89449c671a717198725c95aa496d0 rederived/guarded. Source Action38492935617/job115622139154 SUCCESS HEAD6b9991cba4b11ebfe7d3abb536b3ddf79e61852b. Derived-only artifact11862821367 ZIP SHA256f57cbd2ab80a50b83cdd60d508c671ec2036476dc83654ecf528b7d342f64a71; JSON22386 bytes SHA256eeecbfcf18b59c9b1198ea8e17a0428ab73a6d604ba36253dee661a65da53099. Independent immutable source/artifact custody, pinned digest/size,139 synthetic/tamper/cycle gates and exact canonical equality Action38493237867/job115623101722 SUCCESS. Originals purged, unexecuted and unpublished.

Static helper44/49 graph,52 bounded ESP updates, two conditional hardware slot candidates (caller offsets0/4), exact four-byte EBX store operand at0x4e862, separate SAR/SHL/LEA/input shapes and explicit opaque CALL/memory-alias limits. Eleven input queries, no cap. No actual stack attribute/content, argument/value/handle binding, table/alias/CRT/heap owner, executed file IO/native schema/persistence or cross-version/server equivalence established. Canonical report research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R38-ORIGINAL.json; scope docs/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R38.md; NEXT R39 mask/stack-token candidates then native ReadFile-context buffer/length recovery. Stage A only.

Architecture references, not historical runtime evidence: Intel SDM Vol2B PUSH printed4-511/4-512, https://www.intel.com/content/dam/www/public/us/en/documents/manuals/64-ia-32-architectures-software-developer-vol-2b-manual.pdf ; Vol2A CALL printed3-126, https://www.intel.com/content/dam/www/public/us/en/documents/manuals/64-ia-32-architectures-software-developer-vol-2a-manual.pdf . Operand-size and stack-address-size requirements are separately retained; no original ABI profile asserted.


## SRC-TW10-SAVEDATA-NATIVE-IO-R39 — 2026-10-14

S-grade authenticated TW1.0 retail original nonexecuting PE/operand/topology evidence; runtime/ABI/value/ownership interpretation conditional. Exact R38 original SHA256eeecbfcf18b59c9b1198ea8e17a0428ab73a6d604ba36253dee661a65da53099 rederived/guarded. Source Action38494750030/job115627853201 SUCCESS HEADccea7d85ccaaf41a5297fab3273be20fcb246947. Derived-only artifact11862418406 ZIP SHA256ffabace982b4e15bf71fb43094fd44db8f3dd567e0625813464408eb5aba89e8; JSON28232 bytes SHA2569e7648bd716b65a3695c1a1b04461d5863474210f083e5a11df6595e8cdbbd44. Independent immutable source/artifact custody, pinned digest/size,162 synthetic/negative gates and exact canonical equality Action38495118066/job115629024886 SUCCESS. Originals purged/unexecuted/unpublished.

Static AND ESI31->SHL3 composition, two bounded conditional register-symbol slot candidates with nonoverlapping modeled prefix pushes, and original CALL0x4edb0->0x4a8dc pre-call PUSH EBX/EAX/immediate1, LEA EAX,[EBP+19] and postcall byte comparison26/0x1A syntax. Caller/helper symbols remain unknown across GetFileType; no actual parameter, handle, buffer, count/return/ABI/frame/table/alias/owner or native128-byte save/persistence proof. End-check interpretation is HYPOTHESIS. Post-call sampling bounds instruction starts within48 bytes; full instructions stay within768-byte parent graph, not claimed fully inside the local start window. Canonical report research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R39-ORIGINAL.json; scope docs/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R39.md. NEXT R40 ReadFile-context parameter/frame and candidate end-check distinction, then savedata-specific payload/filename chain. Stage A only.


## 2026-10-14 — TW1.0 R40 original read-frame and postcall predicate derivative

S-grade authenticated TW1.0 retail original PE/operand/topology evidence; interpretation strictly conditional and nonexecuting. Source Action38569997657/job115872382427 SUCCESS at agent/tw10-savedata-r40-read-frame-endcheck-20261014 HEADb9b347825779a861ea45e8c58b97838dd1e88f76. Exact R39 original SHA2569e7648bd716b65a3695c1a1b04461d5863474210f083e5a11df6595e8cdbbd44 rederived/guarded with authenticated original archive/runtime/save identities. Derived-only artifact11898220647 tw10-r40-original-read-frame-endcheck-derived ZIP SHA256996e46965796c005610aeecdb3ff1a2ee2f5a0597d58bda8a60071dbab42dfd0; raw JSON80338 bytes SHA2560ec7fe47a34a77143b446cb02df088d647f4694174d025039abffd8b35066c2f. Independent immutable run/head/branch/artifact custody, pinned digest/size, strict negative controls and exact canonical parsed JSON equality Action38570582335/job115874400290 SUCCESS at HEAD81974e598687264313f8aafeb7c98d66d7898234. Local derivative equals independently disclosed original-derived JSON;192 local/independent R40–R32 tests PASS (source57 R40/R38 tests PASS). Original executable/media transient, unexecuted, unpublished and unconditionally purged.

ACCEPTED CONDITIONAL ORIGINAL STATIC ONLY: original ReadFile-context root0x4a8dc has174nodes/200edges, no graph cap/frontier. Prolog PUSH EBP0x4a8dc; MOV EBP,ESP0x4a8dd; SUB ESP,12 at0x4a8df; PUSH EBX/ESI/EDI0x4a8e2/0x4a8e3/0x4a8e7. The reused ESP model deliberately leaves SUB/explicit ESP writes and CALL effects unknown. At the earlier EBP establishment, modeled ESP delta is uniquely-4; this does not establish original stack attributes or runtime frame contents. Full graph replay357 updates, no update cap; one frame-definition shape and12 input queries without truncation/query cap.

Five early EBP-memory read candidates include MOV ESI,[EBP+8]0x4a8e4, AND dword[EBP-8],0 at0x4a91b, MOV EDI,[EBP+12]0x4a91f, CMP dword[EBP+16],0 at0x4a922 and DEC dword[EBP+16]0x4a93b. These include RMW/local accesses, not five immutable parameters. The four-byte +8/+12/+16 operands geometrically map to caller-pre-CALL offsets0/4/8 and physical PUSH EBX0x4edaf/EAX0x4edae/immediate1 at0x4edac; the negative local slot has no PUSH match. Requires32-bit stack-address and near-CALL return geometry plus the bounded unique MOV EBP,ESP source. No actual token/value transfer, ABI role, prefix-memory preservation, alias/owner or executed IO binding is admitted. In particular, DEC of the +16 slot prevents reading the caller literal as an immutable downstream API count.

Both original ReadFile import associations0x4a960/0x4aa31 at IAT0x520d8 are independently requalified within this graph, with physical PUSH suffixes5/3 and17 input queries each, no query cap. They remain opaque external calls; no actual handle, buffer, length, API success or return/frame preservation is proved.

Parent230nodes/271edges retains no graph cap/frontier; eight caller input queries, no cap. Precall LEA EAX,[EBP+19]0x4eda9 and postcall byte CMP[EBP+19],0x1A0x4edbc have equal address spelling with different operand widths, NOT proven equal actual effective addresses. EBP source before LEA is UNKNOWN_CALL0x4ed87 and before CMP is UNKNOWN_CALL0x4edb0. Six bounded JE/JNE candidates at0x4edba/0x4edc0/0x4edd0/0x4ede2/0x4edf4/0x4edfa each have one nearest graph-local ZF writer (TEST0x4edb8, CMP0x4edbc/0x4edcc/0x4eddf/0x4edf0, TEST0x4edf6), no backward cap/truncation. No actual flags, feasibility, taken paths or API results are admitted. Local windows select instruction starts; complete instructions fit the broader768-byte graphs.

HYPOTHESIS ONLY: the literal1/local byte/0x1A pattern is consistent with an end-check candidate. Text/EOF/CRT identity and any actual savedata payload role remain OPEN. R40 bounds this candidate; it does not close filename->successful handle->ReadFile/WriteFile buffer/length128, native framing/checksum/migration/schema/persistence, original server authority or cross-version equivalence.

Canonical derivative and acceptance receipt: research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R40-ORIGINAL.json and STONEAGE-TW10-SAVEDATA-NATIVE-IO-R40-ACCEPTANCE-R1.json. Original authenticated archive identity is inherited exactly, no new historical specimen or copyrighted payload published. Architecture assumptions inherit the prior Intel PUSH/CALL references; they do not prove SS.B, ABI or original execution. Highest NEXT R41: return to savedata-specific original filename PUSH/CALL sites0x40064->0x40069,0x400e4->0x400e9,0x40115->0x4011a,0x402a0->0x402a5, all direct targets0x487ba from accepted R4–R7 evidence. Revalidate their exact immediate address0x63634 and physical pre-CALL suffix, then recover bounded caller continuation buffer/count/size operands and downstream direct CALL identities with coherent original boundary/entry support. These are independent conditional caller contexts; do not assume the0x487ba return or register/frame preservation. Seek savedata-specific payload read/write candidates, keeping generic open/end-check paths separate. No global/table/allocator ownership exhaustion; no literal128 schema promotion. All system-family PARTIAL/OPEN states and Stage A restoration before joint future-engine/game review remain binding.


## SRC-TW10-SAVEDATA-NATIVE-IO-R41 — 2026-10-14

S-grade authenticated TW1.0 retail nonexecuting PE/CFG/operand evidence; all runtime/ABI/owner interpretations conditional.

Source Action38572368408/job115880592995 SUCCESS at agent/tw10-savedata-r41-savedata-callers-20261014 HEAD60e22410c5f6f84f6d0ad9f6169ea6b2aa2f5c0b. Authenticated transient retail archive/disc/runtime/save gates and exact hardened R7 derivative SHA25673b965887f0ff391f40abba4649482aa2d832151df5fbb602c4274d356bc71d8 rederived/strict-gated. Derived-only artifact11898143745 tw10-r41-original-savedata-callers-derived ZIP SHA256e7ed8e2afc1f25a6250bafa4622be27613b6e0a6c63f90771c296f3a93e2dbe9; raw JSON120631 bytes SHA2568c8474f75eb6adec5aa3939054f0fce26997152fb8e1f1424e74f18485c2471c. Independent immutable run/head/branch/artifact custody, pinned raw digest/size, strict negative controls and exact committed-original JSON equality Action38572684418 SUCCESS at HEADe0f12565d8cbd3a4503d6428497a0888fef8cf12. Local JSON equals downloaded pinned original-derived JSON.254 local/independent R41-R32 plus hardened R7 tests PASS. Original executables/media unexecuted, unpublished, transient and unconditionally purged.

FACT (original bounded static): four exact savedata filename PUSH/CALL prefixes and their PE-entrypoint CFG boundary support reverified. Separate continuation graphs discover repeated target0x48bbc with four physical PUSH candidates and target0x48660 with literal4000/local address candidates. Open CALLs remain opaque; branch joins retain alternate source candidates. No parameter/handle/buffer/length/schema/persistence or actual runtime execution admitted. HYPOTHESIS: savedata-specific payload write/read wrappers; target bodies and native API links remain for R42.

Canonical original research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R41-ORIGINAL.json; scope docs/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R41.md. Stage A only.


## SRC-TW10-SAVEDATA-NATIVE-IO-R42 — 2026-10-14

S-grade authenticated Taiwan Waei/JSS1.0 retail nonexecuting static PE/CFG/operand evidence; runtime/ABI/owner interpretations conditional.

Source Action38574385118/job115887532644 SUCCESS at agent/tw10-savedata-r42-payload-wrappers-20261014 HEADebd97285d26daaaac51e96115302ea400eee915b. Authenticated transient archive/disc/runtime/save identities and exact R41 original derivative SHA2568c8474f75eb6adec5aa3939054f0fce26997152fb8e1f1424e74f18485c2471c rederived/strict-gated. Derived-only artifact11898767027 tw10-r42-original-payload-wrappers-derived ZIP SHA25610c695b16eb5a1be5d1f3fa8b4852c3c4b3593d6f410317ad0dfccd83da6b501; raw JSON147608 bytes SHA256545901acc97a027fb38a3937e00549b15f45b379c7c059e98ece6133c9541732. Independent immutable source run/head/branch/artifact identity, raw size/digest, negative controls and exact canonical JSON equality Action38574676282 SUCCESS at HEADe0c2dff028af3234fb028b7fa7642b1e92ca9b58.278 local/independent R42-R32 plus hardened R7 tests PASS. Originals transient, unexecuted/unpublished and unconditionally purged; local canonical JSON equals pinned derivative.

FACT (bounded original static): savedata-specific wrappers0x48bbc/0x48660 have coherent direct CFG support and conditional paths to native IO contexts via0x48c5e->0x4c5b4 /0x486f0->0x4a8dc. Four whole stack slots, two IMUL operands and three-slot native-call suffix syntax independently requalified. Opaque CALLs/loop joins block actual frame/owner/value binding; one write-definition shape0x48c93 remains outside the12-row sampler. HYPOTHESIS only: fwrite/fread roles and descriptor-like field. No actual IO/schema/persistence or historical system-family closure.

Canonical original research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R42-ORIGINAL.json; scope docs/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R42.md. Stage A only.


## SRC-TW10-SAVEDATA-NATIVE-IO-R43 — 2026-10-14

S-grade authenticated Taiwan Waei/JSS1.0 retail nonexecuting static operand/CFG evidence; runtime/ABI/alias/owner interpretations conditional.

Source Action38576786023/job115895874751 SUCCESS at agent/tw10-savedata-r43-prefix-product-sources-20261014 HEAD31ee18e7d81077b3b9075c8900c99b8b676b9005. Authenticated transient archive/disc/runtime/save identities and exact R42 derivative SHA256545901acc97a027fb38a3937e00549b15f45b379c7c059e98ece6133c9541732 rederived/strict-gated. Derived-only artifact11899434410 tw10-r43-original-prefix-product-sources-derived ZIP SHA2569f95bae3ada8f5aa74c7e8f9c739be2afd723dd17f20b160f6e8812d77713f86; raw JSON162163 bytes SHA256f5eeaac700c649f92e3fca5e7cbefa465879048f54d84b3896dcdb72115d7b42. Independent immutable source run/head/branch/artifact identity, raw digest/size, negative controls and exact canonical JSON equality Action38577142281 SUCCESS at HEADc63ea157452eecb8eee3b42a5f5a461863d517ee.304 local/independent R43-R32 plus hardened R7 tests PASS. Originals transient, unexecuted/unpublished and unconditionally purged; local canonical JSON equals pinned original derivative.

FACT (original bounded static): the two IMUL instructions have unique early EDI-load sources; bounded prefix/slot audits preserve conditional operand symbols and explicitly record two mutable+8 frame slots. The missing write shape is DEC EBX0x48c93;13/10 native definition shapes are now fully sampled. Loop-region and opaque-CALL alternatives remain distinct from actual input values/effects. Native object/count/buffer/schema/persistence remain OPEN.

Canonical original research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R43-ORIGINAL.json; scope docs/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R43.md. Stage A only.


## SRC-TW10-SAVEDATA-NATIVE-IO-R44 — 2026-10-14

S-grade authenticated Taiwan Waei/JSS1.0 retail nonexecuting static PE/operand/CFG evidence; stack/ABI/alias/owner interpretations conditional.

Final original source Action38579065734/job115903789605 SUCCESS at agent/tw10-savedata-r44-native-slots-mutable-20261014 HEAD8e6df983241cba248ed14e85fd03beb6f4b43171. Authenticated transient archive/disc/runtime/save identities and exact R43 original SHA256f5eeaac700c649f92e3fca5e7cbefa465879048f54d84b3896dcdb72115d7b42 rederived/strict-gated. Derived-only artifact11900549300 tw10-r44-original-native-slots-mutable-derived ZIP SHA25698d01e4a6d28c58dd241241fc9851aa3ddee0fe4e0d14d835714704e086afd14; raw JSON225095 bytes SHA25652c158d5f28f3ea287432e4b8214d306c491f158820808d7c4dd212c0646f5e8. Independent immutable source run/head/branch/artifact identity, raw digest/size, negative controls and exact canonical JSON equality Action38579428156 SUCCESS at HEAD662bb212594d61804db5279c01cffaa97b7d90d4.331 local/independent R44-R32 plus hardened R7 tests PASS. Original executable/media transient, unexecuted/unpublished and unconditionally purged; local canonical JSON equals pinned final derivative.

Preliminary96-byte source Action38578665667 at HEAD315d9866ef95a160abfff9b1ced8a5953bd35a1f, artifact11900693754, JSON155250 bytes SHA256dc9cb1c200416a27ae6976eaeda19963c16fcb927e785b78762053dfa0b00632, is superseded by the final160-byte source above. It omitted the delayed write+12 read from its early scope and is not the final R44 acceptance specimen. No prior historical record deleted.

FACT (bounded original static): native input slot geometry, literal ESP adjustment operands, delayed write buffer-shaped read with opaque CALL barrier, read count-slot DEC-before-PUSH overlap and two different wrapper slot-rewrite source chains independently recovered. Read wrapper EBX->native EDI has only a conditional prefix register-symbol candidate. Third write slot/frame preservation and actual count/descriptor/buffer values remain OPEN; no original IO/schema/persistence accepted.

Canonical original research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R44-ORIGINAL.json; scope docs/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R44.md. Stage A only.


## SRC-TW10-SAVEDATA-NATIVE-IO-R45 — 2026-10-14

S-grade authenticated Taiwan Waei/JSS1.0 retail nonexecuting PE/import/operand/CFG evidence; all runtime/ABI/alias/owner interpretations conditional.

Original source Action38581331803/job115911685844 SUCCESS at agent/tw10-savedata-r45-count-api-inputs-20261014 HEADedf452d6fa218961250f400eb294bf4ab7b43fc5. Authenticated transient archive/disc/runtime/save identities and exact final R44 original SHA25652c158d5f28f3ea287432e4b8214d306c491f158820808d7c4dd212c0646f5e8 rederived/strict-gated. Derived-only artifact11904385284 tw10-r45-original-count-api-inputs-derived ZIP SHA2569d8f3eb3b087dc56008fa0ab4df4535f2131ad6f5b86a6b3cbcf2a77954eb015; raw JSON73217 bytes SHA25677919ef7e23f6a25afc66c2bc54b7b0f7da02df1b618e4a50743cda7ad26c21e. Independent immutable source run/head/branch/artifact identity, raw digest/size, negative controls and exact canonical JSON equality Action38581850803 SUCCESS at HEAD0cb7733529bfc76c368751769d36f96a06d2e3f2.353 local/independent R45-R32 plus hardened R7 tests PASS. Original executable/media transient, unexecuted/unpublished and unconditionally purged; local canonical JSON equals pinned original derivative.

FACT (original bounded static): the DEC has a bounded root-to-PUSH bypass; five ZF-source candidates and both first native API imports/five-slot suffixes independently recovered. Read buffer sources include copy and+1 address forms; write uses a local-frame address candidate. Delayed write CALL targets previously accepted helper0x4c761, but its actual effects and post-CALL frame preservation remain unknown. No actual requested/transferred count, file/handle/buffer/schema/persistence proof.

Canonical original research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R45-ORIGINAL.json; scope docs/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R45.md. R37 helper correlation uses the same pinned runtime, does not re-admit effects. Stage A only.


## SRC-TW10-SAVEDATA-NATIVE-IO-R46 — 2026-10-14

S-grade authenticated Taiwan Waei/JSS1.0 retail nonexecuting PE/operand/import/CFG metadata; runtime/ABI/alias/owner roles conditional.

Final original source Action38585030446/job115924602666 SUCCESS at agent/tw10-savedata-r46-adjustment-helper-slots-20261014 HEAD9f33f148cf7f4f994b435625744e5085c3d975a0. Authenticated transient archive/disc/runtime/save identities and exact R45 derivative SHA25677919ef7e23f6a25afc66c2bc54b7b0f7da02df1b618e4a50743cda7ad26c21e rederived/strict-gated. Independently accepted R37 helper memory/import surface rederived and exactly equal after the established normalized JSON digest a16c858a46d502dec5c99fe43528601f0bc89449c671a717198725c95aa496d0 (committed pretty JSON raw91061 bytes SHA256975e2e6d6014c72e576aa1ba9717843d7f8fc579d9a0d591e18482fe9503acad). Derived-only artifact11905875057 tw10-r46-original-adjustment-helper-slots-derived ZIP SHA2568e815487bdc4715ffb241401a7ddbcf8cdd3ea11fe319ae4c27f349b8e15bcde; raw JSON70648 bytes SHA2569aff27e1dadb33b1df5642e114488b238e83efcb97015a806c9e6527658c560e. Independent immutable source/run/branch/artifact identity, raw size/digest, strict tamper controls and exact canonical JSON equality Action38585353840/job115925764486 SUCCESS at HEAD654c36acf17f1a4f5bf0175f8fff31cc20540b5b.385 local/independent R46-R32 plus hardened R7 tests PASS. Original executable/media transient, unexecuted/unpublished and unconditionally purged.

Preliminary Actions38584671133 (HEAD82cb57bc6a11aba418c12f4cd1b8336245c3dbe6) and38584894289 (HEAD32c07ee465a8be829dc6db47c2763ecf5e019bf1) failed the R37 custody comparison because they compared the accepted normalized-export digest to pretty-printed canonical raw bytes. Neither published an accepted derivative; their cleanup gates succeeded. Final source correctly uses the established normalized JSON digest, then exact parsed helper-surface equality; no R37 source content changed.

FACT (bounded original static): optional count decrement, byte store and buffer+1 appear together on first-ReadFile structural paths or are jointly bypassed. The two bypass branch arms and shared local EDI source independently reproduced. Reused write helper entry matches only conditional caller slot0; later SetFilePointer stack reads remain behind an opaque CALL and unbound. No runtime byte/count/text/seek/frame/owner/schema/persistence FACT admitted.

Canonical derivative/receipt research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R46-ORIGINAL.json and STONEAGE-TW10-SAVEDATA-NATIVE-IO-R46-ACCEPTANCE-R1.json; scope docs/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R46.md. Stage A only.


## SRC-TW10-SAVEDATA-NATIVE-IO-R47 — 2026-10-15

S-grade authenticated Taiwan Waei/JSS1.0 retail nonexecuting PE/operand/import/CFG metadata; actual runtime/alias/ABI/owner roles conditional.

Final original source Action38650978505/job116149395388 SUCCESS at agent/tw10-savedata-r47-byte-result-return-20261015 HEAD672dd89ac2cbf6b28941ac9156ff51330eaa6833. Authenticated transient archive/disc/runtime/save identities and exact R46 derivative SHA2569aff27e1dadb33b1df5642e114488b238e83efcb97015a806c9e6527658c560e rederived/strict-gated. Derived-only artifact11934900787 tw10-r47-original-byte-result-return-derived ZIP SHA256487e2f9ce520abe0eab1887ca84d1c3b89ec9ea86371e871e4e22c027e9d4418; raw JSON109781 bytes SHA256939d7080b61c2e8b3dc873cf0adec45ffc6b2c6154877aee787af6ab03dcf781. Independent immutable source/run/branch/artifact identity, raw digest/size, strict negative controls and exact canonical JSON equality Action38651158810/job116150004912 SUCCESS at HEADa5eabdbe44864096a04cacd824ec784f89452e48.410 R47-R32 plus hardened R7 tests PASS in both source and independent Actions. Local syntax compilation, raw ZIP/JSON custody and exact parsed/byte equality checked; local runtime tests were unavailable because this session lacks capstone/pefile. No claim of local execution of the410 tests. Original executable/media transient, unexecuted/unpublished and always purged.

Preliminary Actions38650770406 (HEADe610bd3d0245da86b34d3f76c81bc333bfb5877d) and38650891045 (HEADf94ec3161ad09d3bdbd86019c412574e68e10c69) failed synthetic gates before original archive retrieval. The inherited late fixture changed instruction boundaries after deriving its prerequisite graph, then needed a two-byte AL comparison after a three-byte invented load. Final fixture regenerates the synthetic graph/branch prerequisite and preserves instruction boundaries. These failed attempts publish no accepted original derivative and are superseded by the final source above.

FACT (original bounded static): the byte load affects only AL and reaches the byte store; later reset-shaped+5 store uses a separate EAX reload. Native local initialization/marker/result-addition and wrapper zero/-1/remaining-slot/buffer-advance shapes independently recovered. Cross-call EBP/EAX sources remain UNKNOWN_CALL, preventing actual alias, transferred-count, total-return or savedata schema/persistence promotion.

Canonical derivative/receipt research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R47-ORIGINAL.json and STONEAGE-TW10-SAVEDATA-NATIVE-IO-R47-ACCEPTANCE-R1.json; scope docs/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R47.md. Stage A only.


## SRC-TW10-SAVEDATA-NATIVE-IO-R48 — 2026-10-15

S-grade authenticated Taiwan Waei/JSS1.0 retail nonexecuting PE/operand/CFG metadata; actual runtime/frame/ABI/alias/owner interpretations conditional.

Final original source Action38652256320/job116153604235 SUCCESS at agent/tw10-savedata-r48-count-return-loop-20261015 HEADf8f052f85b9e61469d946195a779897b7cc47b92. Authenticated transient archive/disc/runtime/save identities and exact R47 original derivative SHA256939d7080b61c2e8b3dc873cf0adec45ffc6b2c6154877aee787af6ab03dcf781 rederived/strict-gated. Derived-only artifact11935740518 tw10-r48-original-count-return-loop-derived ZIP SHA25679b570f938e04745c452990d434af54492a45e706c0630a7f3b184732f9695ac; raw JSON87512 bytes SHA256f92a652b446a5433fa1afaa5708112c91bd39c1ef2c4fff27e69a419f013ccfa. Independent immutable source/run/branch/artifact identity, raw size/digest, strict negative controls and exact canonical JSON equality Action38652409955/job116154111413 SUCCESS at HEADe9fec63a18da9f430b2af6fefc2b9ec2a66565f5.442 R48-R32 plus hardened R7 tests PASS in both final source and independent Actions. Local syntax, raw ZIP/JSON custody and canonical byte equality checked; local runtime tests unavailable because capstone/pefile are absent, and are not claimed. Original executable/media transient, unexecuted/unpublished and always purged.

Earlier440-test original source Action38651895475/job116152419472 at HEADed98875e3c9806d2dbf9f288e6a568863f1ef5bc and independent Action38652082455 at HEADe654272e9c42108590443ee22dd1322521e77164 passed their then-current scope. Artifact11934579327 ZIP SHA2562bf989d3fa0a0267aaafe45f8d41ae97de75e2ed87cdd2b6c239ec110c5c8eb8; raw78594 bytes SHA256c6c92887ec57b8c9b6b16e73fdb1434fa7f0dc70b72e5891e2ff392909a4424e. This variant lacks the final direct division-definition/EDX:EAX qualification and is superseded by the final87512-byte derivative. Exact parsed comparison preserves all earlier native/loop/return fields; final adds division input qualification. Initial Action38651870562 at HEAD500bb5384ba58ec0a93f29d5d06d0a1538f5d894 failed synthetic gates on a fixture PE-section metadata-key mismatch; corrected before any accepted original derivation. No old source or evidence rewritten.

FACT (bounded original static): local count-load/add syntax reaches the local return-load region, whose nearest write candidates also include a distinct EDI overwrite. Native and wrapper RET EAX alternatives are enumerated; wrapper remaining-slot/buffer-advance paths loop structurally to the native CALL. Both distinct DIV input sources and EDX:EAX operand geometry are qualified. Actual byte/count/alias/frame/ABI/quotient/return/schema/persistence remain OPEN.

Canonical derivative/receipt research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R48-ORIGINAL.json and STONEAGE-TW10-SAVEDATA-NATIVE-IO-R48-ACCEPTANCE-R1.json; scope docs/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R48.md. Stage A only.


## SRC-TW10-SAVEDATA-NATIVE-IO-R49 — 2026-10-15

S-grade authenticated Taiwan Waei/JSS1.0 retail nonexecuting PE/operand/CFG metadata; actual runtime/frame/ABI/alias/owner meanings conditional.

Original source Action38683095588/job116251797902 SUCCESS at agent/tw10-savedata-r49-overwrite-temporal-slots-20261015 HEAD4d1828be1c0af1ce003f0fefd4a3330e162f5e88. Authenticated transient archive/disc/runtime/save identities and exact final R48 original derivative SHA256f92a652b446a5433fa1afaa5708112c91bd39c1ef2c4fff27e69a419f013ccfa rederived/strict-gated. Derived-only artifact11949650069 tw10-r49-original-overwrite-temporal-slots-derived ZIP SHA256824c4a5faff0947e55d79a777cdac0ab8912fbe51f15e1fe272fc9e2b614c942; raw JSON140909 bytes SHA256fbb25583fa019e496fd0f4d06ef1b441731547e559dcb818d5244321cc3f0ab6. Independent immutable source/run/branch/artifact identity, raw size/digest, strict negative controls and exact canonical JSON equality Action38683345301/job116252568395 SUCCESS at HEAD1e1b172418179dd11bd5f367529cc3c7858dd26d.468 R49-R32 plus hardened R7 tests PASS in both source and independent Actions. Local syntax, raw ZIP/JSON custody and canonical byte equality checked; local runtime tests unavailable because capstone/pefile are absent, and are not claimed. Original executable/media transient, unexecuted/unpublished and always purged.

FACT (bounded original static): native EDI overwrite is sourced by a final SUB whose inputs retain INC and opaque-CALL alternatives. A TEST/JE branch can bypass that overwrite. The same wrapper[EBP+20] slot is read then overwritten from two field-load sites or literal4096 before comparison/division candidates; final numerator cannot be bound to the initial product across opaque calls. Actual byte/count/ABI/alias/division/schema/persistence remain OPEN. Helper scope is bounded; next work returns to savedata-specific caller consumers.

Canonical derivative/receipt research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R49-ORIGINAL.json and STONEAGE-TW10-SAVEDATA-NATIVE-IO-R49-ACCEPTANCE-R1.json; scope docs/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R49.md. Stage A only.


## SRC-TW10-SAVEDATA-NATIVE-IO-R50 — 2026-10-15

S-grade authenticated retail nonexecuting PE/operand/CFG metadata; execution and semantic roles remain conditional.

Original source Action38684319450/job116255602386 SUCCESS at HEAD49d1f536710facf1142b5218e05304616f11791a, branch agent/tw10-savedata-r50-caller-consumers-20261015. Artifact11948569898 tw10-r50-original-caller-consumers-derived ZIP SHA25687d1833da95abc1a7977db7c395c132ecd89d09b13b5b61ec8bcbc5ba146eec7; raw JSON163325 bytes SHA2560badd1423f403a9e8a246a40518a68ee5a1bd67d380ea7ab3460fc3c607c3e94. Exact R49 and R41 original-derived reports revalidated before extension. Independent Action38684734727 at HEAD498820d86998f2d7b4dcaa2e7a6a85f38e33bee6 authenticates immutable source/run/branch/artifact identity, exact raw size/digest, strict report, canonical byte equality and separately regenerated application-consumer contract. Source494 tests and independent513 tests (494 plus19 metadata-consumer controls) PASS. Local19 metadata tests/syntax/custody PASS; full local runtime tests unavailable because capstone/pefile are absent. No original program executed/published; transient original media purged.

FACT (bounded original static): savedata-specific read caller and processing entry requalified. Postprocessor comparisons57/127, register literals4/5, word checks and byte stores at global base/base+57 are recorded with exact widths. Actual length/tag/migration/alias remain unknown. Processor36 memory/control shapes are sampled to32; the omitted4 are explicit next work. Stage A gates unchanged.


## SRC-TW10-SAVEDATA-NATIVE-IO-R51 — 2026-10-15

S-grade authenticated nonexecuting original PE/CFG/operand metadata; original semantics remain conditional.

Original source Action38719176573/job116369203266 SUCCESS at HEADee32f6d16f3dbfeabbb9d73020b64f83f47924dd, branch agent/tw10-savedata-r51-processor-stack-consumers-20261015. Original archive/disc/runtime/save authenticated transiently; exact accepted R50 derivative rederived. Derived-only artifact11963713395 ZIP SHA2563e02a0c79114b8a3e2817a63ef4c6d280944435f4ad1106a213781484c2b4a8b; raw JSON284533 bytes SHA25615f54e5de8d1d20128fb7d948b54f13a0e3f6cf372eca203cbc7bb8adc473052. Independent Action38719540769/job116370411001 SUCCESS at HEAD26c3fc3698f1f930a0acf8296b145fdbe34fdd0e: immutable run/head/branch/artifact, exact raw size/digest, strict primary replay, canonical byte equality, exact nested R50 canonical bytes, postcall metadata contract regeneration and differential old/new stack-model equality at all115 instruction sites. Source553 tests PASS; independent567 tests PASS. Local36 pure metadata tests plus syntax/custody/prefix checks PASS; local capstone/pefile unavailable, so full local runtime tests are not claimed. Original media/executable never executed or published and always purged.

FACT (bounded original static): processor115-node full instruction inventory and all36 memory/control shapes recovered. Normal RET0x47268 yields conditional net near-CALL ESP change0; the caller ECX/pre-CALL+32 coordinate matches post-CALL load[ESP+32] under that bounded model. All seven signed divisions and final byte NOT/subtraction syntax recorded. Source dependencies remain bounded:39 definitions,19 retained,11 pending expansion; schema/algorithm/value/alias/persistence remain OPEN.


## SRC-TW10-SAVEDATA-NATIVE-IO-R52 — 2026-10-15

Authenticated original-derived numeric metadata with explicit Intel architecture qualification; no historical semantic/value promotion.

R52 source Action38721170772/job116375809931 SUCCESS at HEAD5bdf801831f2a8198ce49c5f91c04d583f03a5ec, branch agent/tw10-savedata-r52-cdq-sources-20261015. It authenticates R51 original Action38719176573/HEADee32f6d16f3dbfeabbb9d73020b64f83f47924dd/artifact11963713395 and its284533-byte SHA25615f54e5de8d1d20128fb7d948b54f13a0e3f6cf372eca203cbc7bb8adc473052 canonical metadata before deriving R52. No original archive/disc/executable or savedata bytes were downloaded or evaluated this round. R52 artifact11964589288 ZIP SHA2560c4346b23854cde9452a0f803bfcb5f5d36335563df0276101c08e8422d35d54; raw canonical252332 bytes SHA25699c9252bf3a982db565ab29f43d27e67b2c34978a44990564d74d75949a15179. Independent Action38721359439 at HEAD9e2e0a7cb0170d9e1804272e6be92d522fd0938f SUCCESS authenticates both immutable R51/R52 run/head/branch/artifact chains, exact source/report sizes and SHA256, strict R51 validation, R52 canonical byte regeneration/equality and reverse-predecessor audit. Source and independent611 tests PASS (567 inherited plus44 R52 controls). Local44 pure metadata tests, syntax, ZIP/raw equality, old-prefix and tree checks PASS; full inherited local runtime tests unavailable because capstone/pefile are absent and are not claimed.

FACT (conditional architecture/source metadata):10 CDQ observations preserved with a separate EAX-preservation/EDX-sign-extension overlay; all7 signed-division source groups and11 legacy-pending register groups close without query caps. All39 legacy definition shapes recovered. Forward/reverse algorithms agree on60 queries; output-store sources, five explicit alias-write barriers and10 processor predicates recorded. Actual memory/arithmetic results, algorithm/schema/tag/migration/persistence remain OPEN.


## SRC-TW10-SAVEDATA-NATIVE-IO-R53 — 2026-10-15

Authenticated original-derived numeric instruction/graph evidence plus explicit architecture and newly authored invented-fixture models; historical runtime/schema meanings remain conditional.

R53 source Action38723269655/job116382826823 SUCCESS at HEAD3b65aaff0d41e8d209c7212eabc1146d97631b96, branch agent/tw10-savedata-r53-conditional-transform-20261015. Authenticates immutable R51 original-derived Action38719176573/artifact11963713395, raw284533-byte SHA25615f54e5de8d1d20128fb7d948b54f13a0e3f6cf372eca203cbc7bb8adc473052; and R52 Action38721170772/artifact11964589288, raw252332-byte SHA25699c9252bf3a982db565ab29f43d27e67b2c34978a44990564d74d75949a15179. R53 artifact11966653083 ZIP SHA2561b6355be01eba8ba96af8c178ee32001770cf9607675482a3e2cc8f18cafd957; canonical spec104275 bytes SHA25626bbdff472638081cd7e26945350598bf89a75a690c5c4205c2d491ad62e8dd5. Independent Action38723447688 at HEAD681c2c76dfe34eec4658ebf11e2f785856765072 SUCCESS verifies all three immutable source/run/head/branch/artifact chains, sizes/digests, exact prior canonical bytes, strict R51/R52 validation and exact R53 reproduction/equality. Source and independent656 tests PASS (611 inherited plus45 R53 controls). Local45 tests, syntax, raw ZIP/spec equality, historical-prefix and tree checks PASS; full inherited local runtime tests unavailable because capstone/pefile are absent and are not claimed. No original archive/executable/save payload retrieved or evaluated this round; only metadata and generated invented fixtures used.

FACT (conditional reference only): zero-seed key selection/removal, shifted output-index subtraction and final NOT relation reconstructed from pinned metadata and verified with1029 invented fixtures plus10 generic-seed numerical fixtures. Both models agree;112 observed instructions exercised and3 negative-index repairs explicitly excluded by the model domain. Actual input/output bytes, schema/tag/migration/writer/persistence remain OPEN; invented inverse is not historical writer evidence.


## SRC-TW10-SAVEDATA-NATIVE-IO-R54 — 2026-10-15

Authenticated nonexecuting original static metadata; conditional geometry only.

Original source Action38724589059/job116387179386 SUCCESS at HEAD660a051f9b58ef596fb2fdf8f27bfc9fd321a7a0, branch agent/tw10-savedata-r54-writer-prefix-20261015. Archive/disc/runtime/save identities authenticated transiently; exact accepted R51 report SHA25615f54e5de8d1d20128fb7d948b54f13a0e3f6cf372eca203cbc7bb8adc473052 rederived and validated before extension. Derived-only artifact11967805220 ZIP SHA256a857094d202033ea378406fc3c5dae5580c984416181a80f497a6540466ffa5c; raw JSON132329 bytes SHA256635e80079eb594218c849facd2ea1ba8b0c9160142fc017182d17ba8f1c62387. Independent Action38725044477/job116388679063 SUCCESS at HEADd064e83ae3e14f4b6fede56b0f52f7ba2e7c8215 authenticates immutable source/run/head/branch/artifact, exact raw size/digest, canonical byte equality, strict inventories and separately regenerated pure writer contract. Legacy R38/R44/R50 and R51 stack algorithms agree at all201 instruction sites. Source664 tests PASS; independent688 tests PASS (656 inherited plus32 R54 controls). Local20 pure metadata tests and syntax/custody checks PASS; local capstone/pefile unavailable, so full local runtime tests are not claimed. Original executable/save payload never executed/evaluated or published; transient original media purged.

FACT (authenticated bounded original instruction metadata and conditional geometry):

- Normalization CALL0x401b6->0x40020 is supported by the original entrygraph, alongside exact R51 requalification and unchanged57/word4/global byte-store syntax. Writer graph55nodes/54edges; prefix direct callees0x49160 graph17nodes/18edges and0x47010 graph129nodes/143edges. All three inventories are complete inside768-byte/256-node bounds, without frontier/node caps. Structural traversal assumes returning calls; no executed path is proved.
- Writer prefix MOV EAX,4132 at0x40020/CALL0x40025->0x49160 is followed by PUSH ESI/EDI, MOV ECX,31 and global-immediate25148844 into ESI. REP MOVSD0x4003e, MOVSW0x4004c and MOVSB0x40059 are distinct numeric observations. The conditional expression31*4+2+1=127 requires valid repeat count/direction/segments/registers/addresses; it is not a measured original copy size. The helper writes ESP from ECX, so its actual frame effect remains unknown.
- CALL0x4005a->0x47010 is the historical transform candidate. The earlier generic suffix scanner correctly stops at MOVSB and reports no physical pushes. A separately bounded straight-line0x40040..0x4005a replay retains six pushes across neutral-to-ESP instructions: pre-CALL offsets0:EDX,4:literal127,8:literal0,12:ECX,16:EAX,20:literal4000. Saved ESI/EDI outside that window are not arguments. Local LEAs0x40036/0x4003a/0x40045/0x40052 have conditional pre-CALL coordinates36/32/164/36. This binds numeric coordinates only, not original addresses or ABI values.
- Processor conditional entry coordinates+4/+8/+12/+16/+20/+24 match those six physical slots. Entry+8 load feeds LEA count+1 at0x4701c; entry+24 is capacity-shaped; normal branch stores count+1 through entry+20 at0x47068. Capacity/error branches remain retained. The processor has no CALL and one normal RET0x47155; conditional numeric PUSH/POP balance is0. ESP-relative slot entry+16 is later overwritten at0x470f5; equal slot spelling after that point cannot reuse the initial pointer value.
- All five IDIV sites0x4707a/0x47097/0x470e2/0x47108/0x47134, byte accumulation ADD0x47090, NOT0x470c2, key-shaped insertion0x47124, byte IMUL and additive paths0x47117/0x47140 are retained. The read processor separately retains count-1, subtraction and later NOT. These jointly support a conditional inverse hypothesis; no numerical writer/read equivalence is admitted this round. The writer mutates its input and has an input-dependent byte accumulator, unlike the arbitrary-key R53 invented inverse fixture generator.
- Existing R41 write/close identities and physical suffixes at0x40090/0x400ac compare exactly to R54; all10 prior continuation rows and prior narrow graph nodes/edges are preserved as subsets. Opaque open/write/close effects and actual returned counts remain unknown. Literal127 and conditional count+1=128 do not prove that an original128-byte write occurred.

HYPOTHESIS: a conditional127-byte application snapshot is transformed into128 bytes and may correspond to the R53 read relation under valid zero-seed arguments. OPEN: actual REP/frame/alias/ABI values, arithmetic/error paths and key relation, original bytes/field/tag meanings, normalization/migration/checksum/schema/persistence, original server authority and cross-version equivalence. All Stage A system-family PARTIAL/OPEN gates unchanged.


## SRC-TW10-SAVEDATA-NATIVE-IO-R55 — 2026-10-15

Authenticated original-derived numeric metadata plus explicitly conditional invented-array arithmetic models.

R55 source Action38728999042/job116401820264 SUCCESS at HEAD230726474ed0ed9dae228f97da389401b7554b4f, branch agent/tw10-savedata-r55-writer-inverse-20261015. Authenticates immutable R51/R52/R53/R54 source runs/artifacts and exact canonical numeric bytes before extension. R54 source132329-byte SHA256635e80079eb594218c849facd2ea1ba8b0c9160142fc017182d17ba8f1c62387 and R53 spec104275-byte SHA25626bbdff472638081cd7e26945350598bf89a75a690c5c4205c2d491ad62e8dd5 pinned. R55 artifact11969477120 tw10-r55-conditional-writer-read-spec ZIP SHA256569d762983ff27fb19078b825f31d444ec6cee5152efc0fccd78613aa1b3933a; raw spec103165 bytes SHA2569f98d60d00600ffea0838aee7962a1811323eedcc97d02715f3dd846b00fc863. Independent Action38729256210/job116402678124 SUCCESS at HEAD05535ed2621690954c4cb7c6264a80f9065f5bc5 authenticates all five immutable source/run/head/branch/artifact chains, exact sizes/digests, prior canonical bytes, strict R54 inventories/independent201-site stack replay, exact R53 regeneration and exact R55 specification reproduction/equality. Source and independent734 tests PASS (688 inherited plus46 R55 controls). Local46 pure-model tests, syntax, ZIP/raw equality and historical-prefix checks PASS; full inherited local runtime tests unavailable because capstone/pefile are absent and are not claimed. No original archive/disc/executable or save payload downloaded or evaluated; only numeric metadata and invented arrays used.

FACT (conditional metadata-derived arithmetic specification, invented fixtures only):

- Complete129-row/143-edge historical writer candidate0x47010 inventory retained. A separately configured numerical writer model dispatches26 observed mnemonics, six fabricated argument slots, mutable invented input, disjoint output/count/stack and explicit capacity. Existing R53 read model remains unchanged. ADD/JG/JMP support is new; width/signed arithmetic helpers remain shared with R53 and are checked by separate hand vectors/flag controls.
- With valid zero seed,1<=N<=3999 and capacity>=N+1<=4000, the key relation is K=sum(original invented input bytes) mod256. Each byte is accumulated before its optional in-place NOT. T[j]=A[j] XOR255 when j mod5==0 OR j mod2==0, otherwise A[j]. Output[0]=K; output[j+1]=(T[j]+(((j+1)*(j+1)) mod7)*K) mod256; stored count=N+1. These are conditional model relations, not evaluated original bytes. The earlier arbitrary-key R53 invented inverse corresponds to the historical writer only when its key equals this input-dependent sum.
- The R53 read subtraction followed by the same NOT cancels the normal zero-seed write relation. Physical127/count,0/seed,4000/capacity therefore give the conditional127->128->127 model equation. Actual application REP/frame/ABI/alias validity, passed native write count and persistence are not proved. A byte-sum key does not establish a historical checksum-validation mechanism or record field schema.
- Capacity fallback0<=C<N+1 copies input[:C], stores C and does not mutate input or transform. N0/C0 returns empty; N0/C>=1 reaches modeled division by zero. Negative counts/capacities, original alias/invalid-memory cases stay excluded. Fabricated alias/count substitutions are rejected. Key scratch at conditional entry ESP-1 overlaps the high byte of saved ECX; ECX is deliberately not required to preserve its initial sentinel. Entry+16 output-pointer slot is overwritten0x470f5 and later reads use current modeled memory.
- 1292 zero-seed fixtures include all256 derived keys at lengths1/2/3/7/127, additional57/255/3999 and capacity boundaries;7 use capacity fallback. Normal output/count/input mutation agree with an independent compact formula; normal outputs roundtrip through both R53 numerical read and compact read formula. Ten additional signed/nonzero-seed fixtures roundtrip numerically; no general nonzero-seed reference formula is admitted.
- Zero-seed writer/read fixtures total3933134 numerical steps; maximum writer fixture164817. Fixture union exercises126 of129 writer shapes. Three negative-index repair shapes0x470a6/0x470a7/0x470aa remain retained and explicitly domain-excluded: the index is nonnegative below3999. No claim of129 executed instructions or exhaustive/formal all-buffer proof. Hand vector[1,2,3]->[6,4,26,8], all256 single-byte[v]->[v,255], high-bit/wrap keys, wrong-key/divisor/missing-NOT counterexamples, signed JG limits, aliases, error and custody/report corruption supplement the fixtures.

OPEN: actual frame/REP/argument/alias validity, opaque native open/write/close and successful returned counts, original bytes/fields/tags/version meanings, normalization/migration/checksum/schema/persistence, original server authority and cross-version equivalence. All Stage A system-family PARTIAL/OPEN gates unchanged.


## SRC-TW10-SAVEDATA-NATIVE-IO-R56 — 2026-10-15

Authenticated original-derived numeric shapes plus conditional hardware/copy/call premises, invented storage/stubs and independent algebra; no original runtime/native execution.

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


## SRC-TW10-SAVEDATA-NATIVE-IO-R57 — 2026-10-15

Authenticated original static instruction/graph evidence plus conditional operand/source/control replay; no original runtime/native output or payload semantics.

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


## SRC-TW10-SAVEDATA-NATIVE-IO-R58 — 2026-10-15

Type: authenticated original Taiwan Waei/JSS v1.0 retail client static helper instruction/CFG evidence; conditional source-return analysis, not original runtime/native I/O observation. Confidence: S for executable identity and bounded static syntax, not for actual behavioral semantics.

Source Action38743841197/job116452160761 SUCCESS at HEADc19e32987bd1bdb847e2a4306983dfe4ffb347d5; prior exact R57 report203899-byte SHA256 3e562ab02a80e0f6516f8a91c93b897eef05f606be62f1df5cb48686d64114e6 revalidated. Derived artifact11976911506 tw10-r58-original-shared-close-helpers-derived ZIP SHA256 37ff56646a708744f9585eb7719fa313a6a053bcea9a9f6c38ac4bf2044601d2, raw124989-byte SHA256 04fb0b586f1fcf87f647b1bc1276bde2505822e195646c4c9058c03c7f558fe8. Independent Action38744746218/job116455318961 SUCCESS,83 tests and12 independently replayed return-source queries. Original proprietary data not published, source purged; only numeric instruction/operand metadata retained.

FACT static: 0x4a657 shared helper has40 nodes/44 edges/5 predicates/4 memory-write shapes and RET0x4a6b2; CALL0x4a683->0x4c5b4, CMP EAX,EDI0x4a68b and MOV EAX,EBX0x4a6ae. 0x4a53e close-path helper has66 nodes/73 edges/8 predicates/3 memory-write shapes and RET0x4a5f0, eight call shapes including two memory-indirect unknown targets. Both bounded graphs have no frontier or node cap. Exact parent caller edges from R57 verified. OPEN actual helper result values, callee/alias preservation, native bytes/write/flush/close/persistence, schema/migration/ownership, server authority/cross-version equivalence. Stage A systems remain PARTIAL/OPEN. Source report research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R58-ORIGINAL.json; reference docs/specs/STONEAGE-TW10-SHARED-CLOSE-HELPERS-R58.md.



## SRC-TW10-SAVEDATA-R59-CFG-BYPASS — 2026-10-15

Type: independent derived-only structural path witness over authenticated original Taiwan Waei/JSS v1.0 client static instruction/CFG metadata already registered as SRC-TW10-SAVEDATA-NATIVE-IO-R58. Evidence confidence S for original static instruction/graph identity and conditional structural paths only; no independent new physical medium or runtime observation.

Accepted canonical source: research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R58-ORIGINAL.json, 124989 bytes SHA256 04fb0b586f1fcf87f647b1bc1276bde2505822e195646c4c9058c03c7f558fe8. Branch Action38747322728/job116464274479 SUCCESS, eight synthetic/adversarial checks, derived-only artifact11978648148 (sha256:84bf7eca1ac682f8447ca22ee33431d6a6ef6750ea375765f271d458a72c0a8a); main integration 0746b727ec854d1e20bce99ef7b9d9e4e3e157c5 and main Action38747593076 SUCCESS. Existing R28/R57/R58 WriteFile root preflight main Actions38746885210/38747479217 SUCCESS.

FACT static: conditional path from root0x4a657 through original CALL0x4a683->0x4c5b4 to RET0x4a6b2 coexists in the 40-node/44-edge bounded graph with a path that omits CALL0x4a683. Conditional path from close-path root0x4a53e to RET0x4a5f0 may omit both memory-indirect call sites0x4a5a3/0x4a5ad or structurally visit them. Search assumes CALL return and does not solve actual branch predicates or values. R28 candidate0x4c5b4 contains139 nodes/156 edges with WriteFile import syntax sites0x4c68c and0x4c6f1; no claim that actual native execution reaches them.

OPEN original dynamic path feasibility, actual handle/buffer/byte/count values, register/stack/alias preservation, native transfer results, flush/close/error and persistence, savedata fields/tags/schema/migration/checksum, original server authority and cross-version semantics. No old executable, client art or save payload was published; purely numerical original-derived data and invented tests were used. The original Stage A subsystem gates remain PARTIAL/OPEN.

## SRC-TW10-SAVEDATA-R59-PRIOR-BRIDGE — 2026-10-15

Evidence class: previously authenticated original-client-derived static numeric metadata, reconciled across exact Git blobs, and separately verified synthetic cross-report controls. No original executable/media was downloaded or executed for this milestone. R28 source Git blob3671661219120d45bd922e05b6df371523b42432 and R58 source blob223b65683d37332546ada0fe034a81550b5e8ed8 (R58 SHA256 04fb0b586f1fcf87f647b1bc1276bde2505822e195646c4c9058c03c7f558fe8) are pinned. Original-root source/independent custody from R58 remains separately documented.

Independent R59 cross-bridge Action38747379693 and main Action38747479217/job116464832718 SUCCESS (15 combined synthetic tests plus original-derived R28/R58 strict guards). The 0x4a657/0x4c5b4 bridge corresponds to two indirect WriteFile import-slot associations, and the 0x4a53e close-path contains CloseHandle/GetLastError import-slot associations. This supports static direct-target/import identity and bounded graph evidence only. It does NOT support executed call paths, actual count/bytes written, flush/close success, return/error convention, resource ownership or persistence, payload structure, original server authority or cross-version equivalence. The unmatched native-return/control semantics remain OPEN for R59 follow-on.


### SRC-TW10-R63-WRITEFILE-POSTCALL — 2026-10-15

- Evidence class: **S-derived original-client static syntax**, not observed runtime behavior.
- Source: authenticated clean TW1.0 client source path used in accepted original-static source Action 38754938642 (HEAD 13468c61b52613c728f8e713548b6e3c0cfd71b4). Runtime SHA256 `cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a`; original client/server/save payload not committed or executed.
- Derived-only artifact: 11983560690, ZIP SHA256 `c6fef52e95757cae6682e3518a279a2ae572f4b86efd0e42c1a39aecd8f7931e`. Exact decoded JSON SHA256 `91b650db700cf892a7d8c8b2d36a9d49dbeca139be315856d31d59533056c1bd`.
- Independent cross-check: branch Action 38755602897/job 116493158697 and main Action 38755871657/job 116494106489 SUCCESS, including strict source run identity, archive artifact digest and decoded data structural/non-promotion checks.
- Proves: static `TEST` mnemonics (two operands each) at post-`WriteFile` RVAs `0x4c692`/`0x4c6f7`, local bounded instruction/edge coverage, import-slot syntax.
- Does NOT prove: executable original call paths, native results and bytes written, API or close success, file ownership, ABI/register/stack/memory aliases, flag outcomes, persistent disk records, schema/checksum/migration, server authority or cross-version identity.


### SRC-TW10-R64-ORIGINAL-STATIC-WRITEFILE-TEST-JE — 2026-10-15

- Type: accepted historical Taiwanese 1.0 original-runtime-derived *static* instruction metadata, with independently replayed source custody and synthetic negative controls.
- Primary source runtime SHA256: `cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a`.
- R28 immutable parent blob: `3671661219120d45bd922e05b6df371523b42432`. R63 exact derived JSON SHA256 `91b650db700cf892a7d8c8b2d36a9d49dbeca139be315856d31d59533056c1bd`, Git blob `3b7c9cea63ed4e2a360ddb6934e7dcd44b9833e7`. R64 exact derived JSON SHA256 `5253b2ebec4a9bfbdda24764ce8af5e0e67fabf9ba8daf7ad0ce22c7b172e43f`, Git blob `57cc0ea45bba16d994bb9fda47af257b6ddbb9df`.
- Reproducibility: R63 source run38754938642; R64 primary run38758669705, independent branch38759123587, main independent38759247758/primary38759247737 and canonical publication38759808251 all SUCCESS. Earlier failed R64 CI attempts remain visible, with corrected synthetic fixture/test assertion failures.
- Proves: Original static TEST EAX,EAX then JE at 0x4c692/0x4c694 and 0x4c6f7/0x4c6f9; five R28/R63 aligned physical PUSH shapes per call; conditional ESP+12 candidate at PUSH0x4c67e(EAX) and PUSH0x4c6e8(ECX); first JE's additional target outside local R63 window remains unqualified.
- Does NOT prove: actual Windows API execution, successful BOOL return, runtime EAX/eflags/branch values, real memory-address/pointer alias, observed byte-count output, caller frame/register preservation, successful flush/close/disk persistence, original savedata format/migration/checksum or server authority. Evidence class S for pinned artifact syntax only; gameplay/execution claims remain OPEN.


### SRC-TW10-R65-R66-RETAINED-NATIVE-COUNT-CONTROL — 2026-10-16

Type: authenticated existing original-runtime-derived static numeric metadata and bounded retained-report coverage census; not new original-source acquisition or execution. R28 blob3671661219120d45bd922e05b6df371523b42432; R41 image-base blob7250a7c5b45a054d5ee8c3e92f14cd32612f3ac8; accepted permanent R63/R64 raw hashes/blobs unchanged. R65 exact replay and separate independent numeric guard pass. Original binary, raw code, assets and savedata payload are absent from this work's publication.

R65 permanent report research/recovered/STONEAGE-TW10-SAVEDATA-R65-CROSS-WINDOW-DERIVED.json:5173 bytes,SHA25605bd87eb333184badc4b97b072a2548ff2c00b1a5493709950f866f46ad35c37,blobaaddc7276796fa034bb565e9710e063eedc25c40. Branch Action38819955397/job116713843586 and main38820017473 SUCCESS;45 tests. Artifact12011633995 ZIP SHA256a6182ce67f34098cec6d8946cff6973220cc7f3af98265b0c5d83a9582892e49. Proves bounded cross-window JE/flag/LEA/PUSH/read syntax; first taken edge and three rejoins are operand-derived, distinguished from retained window edges.

R66 permanent report research/recovered/STONEAGE-TW10-SAVEDATA-R66-COUNT-CONSUMERS-DERIVED.json:33147 bytes,SHA256399c5543731aa51136090cd3a58048f947e2431fac05c8861c07d57d15236113,blob5bb6e37294c7ce4bf8af26afd2d2bb3af1842c53. Branch Action38820370818/job116715214955 and main38820484845 SUCCESS;68 tests. Artifact12012608193 ZIP SHA256d885bd9e1bda66513c4e6f8fd95a0907c37ffe4cf9114e515b1c49b950bd0ad0. Proves conditional consumer shapes and34-source same-site-dictionary census:11 missing tail operand rows,2 previously preserved LEAVE/RET shapes. Absence is scoped to those representations, not all project/source content. Complete receipt STONEAGE-TW10-SAVEDATA-R65-R66-ACCEPTANCE-R1.json.

Does not prove: native dispatch/result/count, runtime pointer/frame/alias/callee preservation, feasible branches, OS errors or savedata fields, successful flush/close/persistence, schema/version/checksum/migration/server authority. Stage A PARTIAL/OPEN; Stage B gated.


### SRC-TW10-R67-R68-ORIGINAL-NATIVE-TAIL-RETURN — 2026-10-16

Type: authenticated original-runtime-derived nonexecuting numeric instruction/CFG metadata with independent artifact/canonical custody, followed by conservative source-only return analysis. Runtime SHA256cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a; exact R63 rederivation SHA25691b650db700cf892a7d8c8b2d36a9d49dbeca139be315856d31d59533056c1bd. No original executable, asset, raw code or savedata payload is published or executed.

Source Action38824599576 atdc60f242a95bb34606e52037adc1efdaaa03b96f; original-static job116729034463 and independent archive116729256354 SUCCESS. Artifact12014357270 ZIP SHA256f4a627c9a1700bd8613e75e0d51465d537c9a3973668eca21cb53f8c8f0a3728 matches independently downloaded ZIP. Sole14911-byte raw JSON SHA2568bb5923de9a630a953de6c62cf9c10463aed9a4066db9a0aa97c7aaff338ab50 matches canonical source Git blob04162081d346b8c53424295de9fdc6b8f385b011 at research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-TAIL-R67-ORIGINAL.json. Custody in STONEAGE-TW10-SAVEDATA-R67-SOURCE-CUSTODY.json.

Proves21 fixed-tail/one-hop operand rows;11 previously missing instructions, existing LEAVE/RET unchanged; node inventory139 and bounded edges156. Original-static global writes/literal9/28/subtraction/all-ones syntax are retained without historical error-name, count-value or persistence promotion. R68 pinned derived report3121 bytes/SHA256dc304db7eba4bd95d5c0ad2945e40b1cdde0ea21e1f261978b493acaa05dfd71/Git blobbbf60f7d20b463eafe241e93d1f343cfa2590104 independently agrees on two full-EAX definitions and one unknown0x4c5fe candidate;130-report preflight scope and hashes permanently recorded.

Does not prove actual execution, complete full-function operand coverage, original returned values, ABI/frame/register/memory aliases, OS BOOL/transferred bytes, successful flush/close/persistence, savedata schema/checksum/migration or server authority. Source guard distinguishes live ZIP replay from permanent pinned-custody fallback after artifact loss. All Stage A families PARTIAL/OPEN; Stage B gated. See STONEAGE-TW10-SAVEDATA-R67-R68-ACCEPTANCE-R1.json and docs/specs/STONEAGE-TW10-R67-R68-NATIVE-TAIL.md for final branch/main run anchors.


### SRC-TW10-R69-R70-ORIGINAL-EARLY-CONDITIONAL-RETURNS — 2026-10-16

FACT (authenticated original-static syntax): R69 retains38 early-return neighborhood rows on the exact139-node/156-edge graph after reproducing R67/R63. The missing0x4c5fe instruction is XOR EAX,EAX, entered from early JNE fallthrough0x4c5fc and late byte26 JE0x4c72b. A133-report preflight bounds the prior absence claim. R70's independent forward/reverse algorithms agree on zero, SUB EAX,frame[-16], and OR EAX,0xffffffff direct return definitions;103 of139 nodes decoded. Conditional uint32 shapes agree across1011 invented-only arithmetic comparisons. Actual branches, inputs, count/ABI/frame/aliases, historical marker/error meanings and persistence are not established.

Source Action38851405164/job116813227130 and artifact12025561162 have independently verified ZIP/raw/canonical Git custody. R69 raw25466 bytes/SHA25626ff9f92d14a4ef385a279501e456b4bf58156209ad4471aef84109f6e16bfbe/blobd5d4924803dc28de8be00f712eecd11cf9003c66; R70 raw2406 bytes/SHA256c59858b8d35be04c8f37efec8c297d346fd57d6df2496973c75424143881d621/blobcd2782a57c7c131bd938ca5fe29406a486cc6823. Permanent reports/custody/acceptance receipt remain in research/recovered. No proprietary code/assets/save payload archived or executed. Full local124 tests pass; exact remote acceptance anchors are recorded separately in STONEAGE-TW10-SAVEDATA-R69-R70-ACCEPTANCE-R1.json.

OPEN: actual native returns/counts, temporal frame/memory identity, feasible paths, flush/close/persistence, original record schema/checksum/migration/server authority. Stage A families PARTIAL/OPEN; Stage B gated. Highest NEXT R71: retained-first adjustment update/count-to-return relation, especially R44 INC frame[-16]0x4c653 and known count accumulation; no redundant original acquisition before proven gap.


### SRC-TW10-R71-R72-ORIGINAL-ADJUSTMENT-CONDITIONAL-COUNTS — 2026-10-16

FACT (authenticated original-static syntax): a138-report retained-first census reuses R44/R45 evidence and identifies11 missing rows in a25-node adjustment-loop focus/29-node one-hop neighborhood. R71 exactly rederives R69/R67/R63 and preserves the139/156 graph. CMP CL,10/JNE qualifies the equality-only frame[-16] increment and extra literal13 store before the shared original-byte store. Input bound uses unsigned JAE; post-store output bound uses signed JL after comparison1024. Decoded graph coverage is128/139, with11 mode/direct-count operand nodes still absent in the registered representations.

Source Action38853018146/original job116818258696 and artifact12026131224 have independent ZIP/raw/permanent-report custody: ZIP3148 bytes/SHA256036e7aa7778d4f8fa778847671ae3dbec57807c26abfa12cecd25c9e7d03d89b; raw21525 bytes/SHA256746c7e64a973b52ca5cf3412342eb68725fcf15dcb5ad4a1e71a8e638ae90af5/blobf2a946ffc93c6a32210f2ebaa9dc9191833aac37. R71 independent branch38853444099 and R72 branch38853447606 SUCCESS; accepted code mainf8138e759c4665427f9680ab83d1acf567e19fd8 has successful R71/R72/R69/R70 Actions. R72 report5600 bytes/SHA256aa21627e0018f2a7d9c01aaa36b6f70f38456f938de31713fee893402070265a/blob94656b8f6c2f830743a6257c1a8abf7aedb00c22. Full local156 tests pass; separate remote suite counts remain41 and110.

R72 invented-only3124 trace-threshold comparisons plus four long cases qualify conditional complete-transfer output-minus-insertions identity. Post-store threshold can produce1025 output units. Partial-write examples disprove a general logical-prefix-count interpretation; no historical native behavior, overflow or memory safety conclusion is claimed. Actual count/BOOL, temporal frame/ABI/aliases, feasible paths, persisted records/schema/checksum/migration/server authority remain OPEN. No original code/assets/payload archived or executed. Stage A families PARTIAL/OPEN; Stage B gated.

Highest NEXT R73: refresh custody, reuse exact142-report/128-node next-gap census in STONEAGE-TW10-SAVEDATA-R73-PREFLIGHT.json, and narrowly resolve the remaining mode/direct-count predicate context. Permanent receipt: STONEAGE-TW10-SAVEDATA-R71-R72-ACCEPTANCE-R1.json; spec: docs/specs/STONEAGE-TW10-R71-R72-ADJUSTMENT-COUNTS.md.


### SRC-TW10-R73-R74-ORIGINAL-MODES-FULL-BOUNDED-OPERANDS — 2026-10-16

FACT (authenticated original-static syntax): refreshed144-report census retains the11 gaps; R73 recovers17 one-hop rows after exact R71/R69/R67/R63 reproduction. Seven-source R74 union now decodes139/139 bounded graph nodes/156 edges. This closes the operand inventory within that intraprocedural candidate, not callees/runtime. Mask32 skips/enters opaque direct helper0x4c761; later mask128 chooses direct-native-prefix versus the qualified byte-expansion prefix. Literal5 equality writes9 and EAX-shaped5 to globals, while inequality invokes opaque0x4c953 before all-ones return. Historical flag/error meanings remain unproven.

Source Action38885251848/job116921375490 and derived-only artifact12039068385 have independent ZIP/raw/permanent custody: ZIP2915 bytes/SHA2567005037bf04b1ff034b12996dd4fae4dd1c4d37750c7d0bfe808ed01a93b974e; raw14043 bytes/SHA2565cf096089f60f8a6afd80fe2923f214f609ac57a92ab3d9d02aeefb04248013d/blob2a90bf654a723da53f7d6a26008ca660cb89b290. R74 report7076 bytes/SHA256cc7b48b139f64a502eb26bc45fbd5754b1bba202484447b625e5f34a28c32c25/bloba29a6a9b38a86d2f33d9e327d73c9d08cc3fb5ad. Independent R73/R74 branch Actions38886167422/38886173283 and six relevant code main Actions SUCCESS atfb7cb654c1c702cb2400bcf224f60fdcff52e18a. Local192 savedata tests PASS; remote suites44/146 are separate.

Forward/reverse reaching-syntax algorithms agree on eight register queries. All six calls remain register/memory barriers; early mode snapshots and table/frame state are not equated across the optional call. Invented65536 snapshot pairs qualify four conditional predicate combinations, without actual values/path/ABI/count/persistence admission. No original program/API or payload executed or archived. Stage A families PARTIAL/OPEN; Stage B gated.

Highest NEXT R75: reuse R46's already retained0x4c761 entry/51-node55-edge helper graph/three decoded rows/native seek context and R37 boundary;48 helper rows lack registered operands, but only material missing effects should be acquired. R30 already records0x4c953 boundary; its decoded entry remains absent in the registered scope. Exact148-source helper preflight blob73d192eec12cd31e67b5b0fc298ab4c3bdb53189 and STONEAGE-TW10-SAVEDATA-R73-R74-ACCEPTANCE-R1.json preserve next-step evidence. Native BOOL/count/position, frame/alias/preservation, actual close/flush/persistence, original schema/checksum/migration/server authority remain OPEN. Legacy queued attempt37642417333 stays queued; separately accepted successor37643425686 and permanent report are requalified in docs/continuity/STONEAGE-STALE-QUEUED-RUN-AUDIT-20261016.json, without claiming the old attempt succeeded.


### SRC-TW10-R75-R76-ORIGINAL-SEEK-HELPER-CONDITIONAL-CONTRACTS — 2026-10-16

FACT (original-static): refreshed150-source census reuses R46/R37's retained helper entry,51/55 graph and three decoded operands;48 missing rows are recovered only to inventory all local caller-visible register/stack/memory/return effects. No descendant call graph or original savedata payload is opened. Runtime/R73 and exact R46/R37 helper surfaces are requalified. Source Action38888448211/job116931879732, artifact12040258731 ZIP2743 bytes/SHA2564cd9097e869802b8bd107f737ac68183c78f42f7a4b9b75a6a639adc3d6e069f; raw25435 bytes/SHA256bcec13f8eb8d0b6182a38aa8b0ba67a7f20ca1d9b33ca1c9a76a1448f62b7d85/blob757c22945d7e18263b154e88f52376d0ab58d42c. Independent download/canonical custody survives artifact expiry.

R76's seven structural paths have conditional EBX/ESI/EDI token restoration and balanced near-return stack under declared call-cleanup and nonaliasing premises; adverse cleanup/clobber controls preserve those limits. EBP, table pointers and intermediate EBX remain opaque across calls. Caller/helper physical argument tokens conditionally reconcile to an opaque handle,0,0,2 at imported SetFilePointer; modern Microsoft API/ABI references support an EOF-request interpretation, without original execution/position/success proof. Local AND253 clears bit2 while preserving masks32/128 on256 invented bytes; whole-table snapshot identity is unproven.

Permanent R76 report7662 bytes/SHA2562a57125d32c3889def89c90d2e99192d94a25bd30b9677d5bfd7b0fd10fa3ead/blob2cdbcb8b95649a0ce610ab93fde5edcd7ef0997b. Local226 savedata tests PASS; remote48/180 are separate. Independent R75/R76 branches38889189883/38889194294 and eight code main gates SUCCESS atcdbb41c9f9b2a25ab7aeb32fbf3eaa666c53f8e4. Receipt STONEAGE-TW10-SAVEDATA-R75-R76-ACCEPTANCE-R1.json and spec docs/specs/STONEAGE-TW10-R75-R76-SEEK-CONTRACTS.md preserve source/contract distinctions. No actual I/O/schema/server-authority admission; Stage A PARTIAL/OPEN, Stage B gated.

Highest NEXT R77: pinned154-report helper-entry census blob38cc620394f21e04ec96c14a883b0510082fca43 separates absent registered decoded entries0x4e8fb/0x4c953 from retained root/numeric references. Prioritize only0x4e8fb handle-source and material caller-visible effects, then0x4c953 where necessary. Preserve ABI/stack/nonaliasing, table/address, native handle/count/position, close/flush/persistence and original record/schema/checksum/migration boundaries.

Conditional contract reference sources (accessed2026-10-16): https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-setfilepointer ; https://learn.microsoft.com/en-us/cpp/cpp/stdcall?view=msvc-170 . Modern documentation only; original ABI compatibility and native outcomes unproven.


## 2026-10-16 — TW1.0 R77 handle-source and R78 conditional table-return contracts

FACT (original-static syntax): refreshed156-report retained-first census at mainb49c0d81ad17dc8c5f691e505a9ca817df2a625d reuses R75's direct0x4c78e->0x4e8fb relation. No registered decoded entry exists at0x4e8fb or0x4c953; root objects and numeric references remain distinct. Independent iterative replay checks every source byte/Git blob and the complete historical Git-tree manifest, not merely a file list. Only0x4e8fb's material handle-source local graph is acquired:16nodes/16edges, no frontier/cap, no CALL. Runtime SHA256cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a and exact R75/inherited source chain are requalified. No original savedata payload is opened by this acquisition; no original program/API executes or proprietary bytes enter Git.

Source Action38891577123 atba49bb5ca0dc27d481dcca9ef0a46bb046586dd8 SUCCESS: synthetic116942077884(50 tests), original-static116942132806, independent archive116942430371. Artifact12041483206 ZIP1751 bytes/SHA2563e860fbfca18edb7b3016ec5fedc5c92b26fc341769ee88cd87a718341ade674 was independently downloaded/hashed locally. Sole9830-byte raw JSON SHA2564944a5037e02c5b88b9424b953bcf93254e67560a217663c73b11e42d2827f48 exactly equals permanent blob870b84cb7968d325b37463ca68de1540960e1f5e. Archive3c3b3226192ffe8deb7c55a92f94475da0c1bc16 retains derived report/custody only. Independent R77 branch38892137407/job116943923623 SUCCESS explicitly verifies live-artifact equality and66 tests; invented API-shaped live/expired/unavailable fixtures separately exercise custody-script branches. Bot archival itself is not independent acceptance.

FACT: helper MOV EAX,[ESP+4], unsigned CMP/JAE against global24254560, AND31 and signed SAR5 select table-pointer geometry rooted at displacement24254304. TEST byte[ECX+EAX*8+4],1 controls the table-dword return; intervening LEA preserves flags. The failure-shaped arm has AND global24252940,0; MOV global24252936,9; OR EAX,0xffffffff, followed by plain near RET. No historical CRT/helper/error names assigned. Local decoder writes are only EAX/ECX/flags and RET's ESP; no explicit EBP/EBX/ESI/EDI/EDX write or CALL. Two explicit memory stores occur on the failure-shaped arm. Valid memory/nonaliasing/external-write assumptions are not proven by those spellings.

R78 qualifies exact widths/base/index/scale/offset/literals/topology, and independently authored forward/reverse queries distinguish the two EAX return definitions.4104 invented-word arithmetic comparisons include signed/wrap boundaries;256 invented bytes qualify bit-value1. SAR is not SHR: high-bit inputs can produce negative bucket indices unless the unknown unsigned bound excludes them. Under normal dword near-call, valid nonaliasing stack and stable valid table-memory premises, caller PUSH EAX supplies helper[ESP+4] and its non-allones table-dword result reaches the R76-qualified SetFilePointer hFile suffix. This is conditional provenance of a handle-shaped token, not proof of an actual valid OS handle, realized API/path/position/success or matching temporal snapshots.

R78 report3854 bytes/SHA2568bdb54c09d3ad038cb9149b1ec6d6c7a240778182fa8c69e545e78823c081c14/blob0d2f061dac847871d05c3d38c4b494d583060117. Full local1935 savedata tests PASS after installing missing capstone/pefile; initial broad discovery's75 dependency-import errors are recorded as a resolved environment failure, not called a passing attempt. R78 branch38892142998/job116943943727 SUCCESS has212 tests; R77's66 and source50 are separate counts. Accepted codede9bb83b585f81e106ce3c45b6afaa8ba7ba1b34/tree058b599be98f54961e58680cc8f5542f4aea91fb followed fresh ahead3/behind0/14-path comparison and expected-head nonforced fast-forward. All ten relevant code main gates SUCCESS. Receipt STONEAGE-TW10-SAVEDATA-R77-R78-ACCEPTANCE-R1.json and spec docs/specs/STONEAGE-TW10-R77-R78-HANDLE-CONTRACTS.md preserve full custody and conditional limits.

Highest NEXT R79: exact160-report census at acceptedde9bb83b585f81e106ce3c45b6afaa8ba7ba1b34 preserves0x4c953's three root objects/29 numeric references and zero registered decoded entries. Preflight36634 bytes/SHA256ccb54ea43a16783e7185bc9150751cf369676d8431f51b4a5bd4be3fd085b2f6/blob725b4ebc9671ce3230c59b646e21a9167ccd606f is independently replayed against the complete source Git tree. First reuse retained boundary/caller evidence, then qualify only material error-helper effects on nonzero-error/literal-five-inequality allones routes. No generic helper exhaustion. Actual handle/count/seek results, realized paths, ABI/cleanup/nonaliasing/global-table stability, flush/close/disk persistence, original schema/version/checksum/migration/server authority remain OPEN. All Stage A families PARTIAL/OPEN; Stage B gated.


### SRC-RESTORATION-PORTFOLIO-R1 — 2026-10-16

Derived planning/source audit at main434e11d6bee5546330d9a6a8e5e96ebf9caf8d78.
research/recovered/STONEAGE-RESTORATION-PORTFOLIO-R1.json pins29 selected existing
anchor files by bytes/SHA256/Git blob and the complete historical continuity
prefixes. This is a non-exhaustive portfolio audit, not newly recovered primary
source content or a certificate of every old CI result. Roadmap R2 separates
nine families, evidence version from model usability, and three persistence
layers.49 existing semantic regressions PASS locally; no original program or
proprietary payload acquisition, new tests or historical promotions.
Highest NEXT PET-STATE-01; deep savedata R79 PAUSED_NON_BLOCKING with exact reopen
conditions. All existing custody receipts remain authoritative in their scope.


### SRC-CAPTURE-STATE-SOURCE-AUDIT-R1 — 2026-10-16

Derived existing-code/model audit at maine88ea2392578fd0fe8b77ac6c437a7060c611184.
research/recovered/STONEAGE-CAPTURE-STATE-SOURCE-AUDIT-R1.json pins ten source
artifacts and records copied/recomputed/unavailable field distinctions.
SpawnedEnemy.birth remains in context; no all-carrier absence claim. Known
name and supplied VARIABLEAI0 get shared direct/round validation. Six invented
lifecycle regressions include modern temporary-disk reload and controlled
growth, not original client/server/save execution. Coordinator280 and separate
domain80 PASS locally, with overlap explicitly retained. The baseline bridge
fixture's missing GET/assert11 failure is reproduced and corrected as fixture
input only; absence still yieldsNone. Exact remote gates and historical prefix
custody are in the acceptance receipt. Full automatic construction remains
OPEN_EVIDENCE_LIMITED_EXPLICIT_STATE_REQUIRED. Highest nextWORLD-01; R79 paused.


### SRC-WORLD01-FOUR-HOMETOWN-FINITE-AUDIT-R1 — 2026-10-16

Derived finite Stage A source-membership and representative gameplay review,
not newly acquired JSS1999/TW1.0 content. Exact branch code head
fcd404554ad9a70c553f9917518d6cc6ef8fdb21,
successful independent Action38907653875 (five tests), failed predecessor
Action38907621482 retained for Git blob NUL test code defect.
Canonical evidence record:
research/recovered/STONEAGE-WORLD01-FOUR-HOMETOWN-ACCEPTANCE-R1.json,
with24 provenance/status/input/gap cells and14 path/blob/byte-size source pins;
spec docs/specs/STONEAGE-WORLD01-FOUR-HOMETOWN-REVIEW-R1.md.

Source classification: LATER_RECOVERED for four normal recovered25 hometowns;
Taiwan1.0/JSS1999 membership OPEN. Recovered route order is
1=COMBAT,2=COMBAT,3=COMBAT>SHOP>WARPMAN,
4=SHOP>COMBAT>WARPMAN. Routes3/4 require item-gated affordable
normal purchase and conditional WarpMan; classic-only routes fail there.
All reward and destination results are existential/legal witnesses, not
universal outcomes. 826 map floors split into761 client DAT three-plane and
65 server LS2MAP two-plane with no server event plane. No raw source maps,
NPC arguments, original dialogue, enemy/item rows, original server binaries
or proprietary contents are committed. The audit does not prove
first-generation map/quest/monster membership, commercial-server reward,
full original save persistence, or a 100% restoration rate.
WORLD-01 finite review closed; Stage A family states remain PARTIAL/OPEN.
Next RULES-01; old TW1.0 client-local savedata R79 remains PAUSED_NON_BLOCKING.


### SRC-RULES01-CROSSSYSTEM-PREFLIGHT-R1 — 2026-10-16

Eight finite ordinary-playflow source/evidence joins with eleven exact
committed report/source path Git blobs and byte-count pins:
`research/recovered/STONEAGE-RULES01-CROSSSYSTEM-PREFLIGHT-R1.json`;
human-readable `docs/specs/STONEAGE-RULES01-PLAYFLOW-ATTRIBUTION-R1.md`.
Independent source-custody/version guard Action38908646966 SUCCESS at
branch ab6e8280d6ec9114e7cc7568c6cf6df2f3ee938d.
This is an audit of prior recorded source material, not recovery of new
JSS1999/TW1.0 commercial server NPC/EXP/quest records, nor a complete
executable gameplay scenario. Item ownership, gated NPC reward, historical
server persistence and original threshold selection remain explicitly OPEN.
It does not change RULES-01/Stage A family status PARTIAL/OPEN.


### SRC-STAGE-A-NPC-CONTENT-BOUNDARY-R1 — 2026-10-16

- Type: derived finite original-client-versus-later-NPC evidence boundary / reusable Stage A review input, **not** a newly recovered historical NPC payload.
- Source baseline: accepted TW1.0 client WN compiled-protocol and retail filename boundary (V1_DIRECT only for those properties); fixed descendant Windowman semantics and recovered25 NPC/create/template/Windowman/dialogue/quest-derived statistics remain LATER_RECOVERED.
- Canonical record: `research/recovered/STONEAGE-STAGE-A-NPC-CONTENT-BOUNDARY-R1.json`; narrative `docs/specs/STONEAGE-STAGE-A-NPC-CONTENT-BOUNDARY-R1.md`. Thirteen pre-existing Git blob and file-size source pins with exact canonical counts, seven content evidence surfaces and six ordinary gameplay checkpoints.
- Source-level derived counts: create refs4985, unambiguous4955/ambiguous30, secondary argument missing files15; TownPeople445/15 missing, SignBoard181; Windowman17/13 resolved/4 missing; NPCEnemy279; WarpMan202 with160 candidate spatial edges.
- Verification: branch 230c0067470c87b33a1100cca6c981ed6d56aafe, corrected independent Action38920853733, job117040079436 SUCCESS (6 tests). Earlier failure38920780534 is preserved; it was a new Python regex test defect, not a source contradiction.
- Does NOT prove: original JSS1999/TW1.0 NPC population, quest texts, server choice/action/award state, commercial save durability, early item/economy values or version membership of recovered25 routes.
- Reopen only upon original-version downloadable/server-verified NPC/script provenance, matching original WN trace, source-resolving later missing configuration, or concrete representative gameplay contradiction. Stage A remains open; savedata R79 paused nonblocking.


### SRC-STAGE-A-BLOCKER-TRIAGE-R1 — 2026-10-16

- Type: cross-family, version-qualified **derived review/priority artifact**, not recovered primary first-generation game content.
- Baseline source main: 05196c8bf2708d6841439835ea97180c6bb9337b. Research report: `research/recovered/STONEAGE-STAGE-A-BLOCKER-TRIAGE-R1.json`; narrative `docs/STAGE-A-REVIEW-BLOCKER-TRIAGE-R1.md`; acceptance `research/recovered/STONEAGE-STAGE-A-BLOCKER-TRIAGE-ACCEPTANCE-R1.json`.
- Input:10 immutable existing Git blob/byte-size pins, Stage A nine-family gates, WORLD-01 four later hometown routes/24 attribution cells, RULES-01 eight seams, capture-state explicit-input gaps, seven NPC evidence surfaces, original TW1.0 input/graphics source boundaries.
- Scoped outcome:7 player-visible flow profiles and5 material blockers with matching re-open requirements; remains9 families PARTIAL/OPEN, Stage A unaccepted, Stage B GATED. No original JSS1999/TW1.0 commercial server NPC/quest/item award/session bytes acquired or rendered playable.
- Independent CI Action38922063102, job117044218968 SUCCESS: five adversarial tests including source pin exact Git object identity, denial of stage promotion, four version-qualified hometown path consistency, blockers and R79 non-blocking status.
- Does not prove: original server save/durability, commercial original quest text/rew ards, exact original EXP/capture state, original UI render selectors, universal model outcomes or overall completion percentage.
- Reopen: authenticated same-era content/trace or concrete representative-playflow contradiction. Historical savedata R79 stays PAUSED_NON_BLOCKING.


### SRC-STAGE-A-CONSOLIDATED-REVIEW-R1 — 2026-10-16

- Type: user-facing derived portfolio review, not a new original historical artifact.
- Baseline: main0d1311e19a090b59d6938b034a2b7f987635f148, tree3ef6275e741a5703176acd7d71888e4474346c0e.
- Narrative: docs/STAGE-A-CONSOLIDATED-REVIEW-R1.md; permanent manifest: research/recovered/STONEAGE-STAGE-A-CONSOLIDATED-REVIEW-R1.json.
- Custody:54 pre-existing source/report/spec/test Git blob, byte-count and SHA256 anchors;8 complete continuity-prefix hashes. Source entry points include player/pet growth, skills, use/equip/shop/trade/storage, riding, audio and current coordinator.
- Scope: nine unchanged family gates, seven representative flows, five original-evidence blockers/reopen conditions.11 replay groups distinguish retained source audits from modern synthetic reference execution and source-shape projection.
- Local acceptance:314 selected pre-existing checks and5 new scope/custody/omission-rejection checks PASS. Remote acceptance is separately recorded after actual success.
- Does not prove: any new early map/quest/master/server payload, original commercial service gameplay, exact early riding/trade chronology, original rendering or original SAAC durability. No original assets or source payloads committed.
- Joint review remains pending; Stage A not accepted, Stage B GATED; ordinary continuation stays within Stage A and only materially useful bounded evidence recovery.


### SRC-EARLY-CONTENT-MANUAL-GUIDE-R1 — 2026-10-17

- First-party: http://www.titan.co.jp/stoneage/manual02.html, actual archive https://web.archive.org/web/20010418083149id_/http://www.titan.co.jp/stoneage/manual02.html . Six named sections, four bounded gameplay contracts; capture date is not1999/build provenance or actual server execution.
- Published guide: https://games.sina.com.cn/handbook/0101/01186091.shtml , _c1.shtml, _c2.shtml and 01186092.shtml; attributed to 游民部落网友松鼠1206. Dated catalog https://games.sina.com.cn/downgames/other/0118654.shtml gives2001-01-18/36K/sqsd-rw3.zip/aid24721; current HTML-byte continuity to2001 remains unproven.
- Later comparison: https://games.sina.com.cn/zhqu/sta/rwgl1_1.shtml (2003-05-29), two delivery directions and distinct repetition/discard operations. Same-title shell is not an original item-ID proof.
- Primary derived report: research/recovered/STONEAGE-EARLY-CONTENT-GUIDE-MANUAL-R1.json; intake has raw SHA/bytes/URL/decoding and full continuity prefix metadata. No source HTML, dialogue, art, binary or server payload committed.
- Failure limits: ZIP502 is not absence; one Availability empty exact URL/date query is not an all-archive negative. GB malformed bytes retained as replacement counts; each business claim has source-token guards.
- Supports four manual rule groups and four guide-level quest contracts only; no early exact release, raw map, quest script, commercial persistence or Stage A final acceptance.


## 2026-10-17 — 成人仪式六源与来源谱系

主报告 research/recovered/STONEAGE-ADULT-CEREMONY-SOURCE-CONTRACT-R1.json 固定六源URL/最终URL/尺寸/hash/解码及选段摘要。新实际快照 https://web.archive.org/web/20011120063019id_/http://games.sina.com.cn:80/handbook/0101/01186091_c1.shtml ，SHA2566338fee011897e9196fec132558bf1a4333b0b22946f026e46d4f284b3d2aeb9；它是新浪原汇编的时间见证，不是独立规则作者。17173 renwu/n10.htm完整任务段与新浪相同，不加独立见证数。17173 content/2001-6-14/n654_570366.html（作者未知）及n730_646156.html（Atron自述四次经验）为文字不同候选，自标日期不认证历史字节或作者独立。新浪zhqu/sta/rwgl1_5.shtml自标2003-05-29，为后期详细对照，敏捷-3与早期-2保留。

INTAKE保存四次精确Availability结果：成人章节/介绍文有具体捕获，旧17173两个URL空集只限定这些请求。另读介绍文20011220004340快照，仍署游民部落，预发布/台湾背景不足以认证成人规则版本，排除为独立见证。2011同文和GBC平台攻略不作初代PC证明。原始HTML只在临时研究和CI读取。六源独立CI派生artifact与永久归档receipt随后记载；不提前声称执行/验收。

成人仪式独立来源Action38991633626/job117275086568通过；artifact12085332759/ZIP SHA256 d0dc207134ae801c21ce7cf2ce35a5525cf423c67b3b52b6a66dab34ca4df91a，永久派生Git blob058225a89962dbcfb49e464f7de999f0f5f81121。详见STONEAGE-ADULT-CEREMONY-ACCEPTANCE-R1.json；原始HTML未入Git，实际商服执行与ID未证。


## 2026-10-17 — 伐木六源、实际捕获与失败边界

报告research/recovered/STONEAGE-LOGGING-SOURCE-CONTRACT-R1.json记录六源原始hash/大小/实际URL/解码及选段摘要。新增实际捕获：详细页 /web/20031205132111id_/http://games.sina.com.cn:80/zhqu/sta/article/2003-05-20/7612.shtml；索引 /web/20040218115426id_/http://games.sina.com.cn:80/zhqu/sta/rwgl.shtml；汇编 /web/20040822040357id_/http://games.sina.com.cn:80/handbook/0101/01186091.shtml。域名均web.archive.org，未把请求日期当最终快照。原始HTML不入Git。

INTAKE保留精确Availability/CDX请求及空集/503；本地17173练功、问答、任务页及带平台参数问答HTTP567，web问答超时；这些不是整个来源不存在。练功文使用旧临时全文时先核对原始hash与永久独立成人来源CI报告blob058225a89962dbcfb49e464f7de999f0f5f81121，不假称新本地网络读取；新CI仍必须重取全部六源。17173任务页可见同文仅排除为重复候选，没有新增字节级比对证明。共享文字/归档不提升独立作者数，现代私服“1.82”标签和后期无限收益不当原版依据。

伐木独立来源CI38992670848/job117278246924全部成功，永久派生blob5d1a98763e41f33e627119eba13c7f2b25de5679与本地字节/六源原始hash相等；artifact12085354353 ZIP hash5c64ca6d2b0142c9a446cd819c0f50343796fcb01718fe10e1f0a47aede8d96d。ACCEPTANCE保存链，MODEL-BINDING固定后代普通掉落两来源，仅说明不能把伐木尾刀限制全局化；不复跑原生深层辅助链。


## 2026-10-17 — QUEST-ITEM-IDENTITY-04 固定保存包与派生候选

沿用旧itemset-schema workflow中分卷与合包hash取得步骤；独立Action38993481443/job117280730238成功，验证master a415e78f9aab2e5ea5ca92ecb7430253f7be1ba7c876d6b0bb6d067b1b466688及6d6d63fda59c6bda2f239fe18c9361b5c9da18c84f678b7cc95bde24544292fb。只留五个候选的数字/标记/行hash/查询编码，不存表全文或程序。artifact12085893496 ZIP hashbb5a6cbedae5f06e2f12c2a51c8a2b259e6899d6757b4f79f517fa7cf258b8e8；永久派生blobd0ac9e5f5d26db5afcee07119295fd05803011b9，ACCEPTANCE保存源HEAD/tree。此前本地405/非JSON失败保持原记录，独立成功仅说明runner路径可用。两修订表不是独立规则作者，不提升初代归属。


## 2026-10-17 — QUEST-NPC-FLOW-LINK-06 后代ExChangeMan事件内关联可复核来源

源为上一轮已固定后代recovered25保存包两分卷哈希7cb7acdecd56617132e6f284c468158917c91d542cad5b2e7b3c7774fb5630d5 / 567e1ec0aeff9ea6a9ada791a339aa8f8bb8ffba83cf762e4b445fc0f1cb16bb，合包hash d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5；严格复用已有ExChangeMan/NPC类型解析及前次永久源报告Git blob7d771b2aa4f39646879659303f4926045ae730cc。实际独立Actions38997164871/job117292136171 SUCCESS，9项事件语法/否证门及源文件读取/比较通过。临时下载、NPC配置原文、对白与原服务程序不入Git/未执行。

派生短期artifact12087945346 ZIP2196字节/SHA256 a824365bfae4f4763192779dac853d431014bdfdc8af3c1785c1da6f71b0b3e3，唯一quest-npc-flow-derived.json15004字节/SHA256 719b6dc071ea9d5946d707ced51798786d7b227d642bb80f009290ca834ad05a，永久Git blob b9f04bd7956a25a249e182fad4db2f0459719327，经独立下载解压及Git blob比对一致。仅27匿名记录的ID/角色/源hash：同一EventEnd的两个后代候选关联2465→2484(2记录)、2478→2481(1记录)，未证任何原版奖励事务、版本归属或整体任务图。来源可追溯矩阵和否证规则：research/recovered/STONEAGE-QUEST-NPC-FLOW-ACCEPTANCE-R1.json、docs/specs/STONEAGE-QUEST-NPC-FLOW-LINK-R1.md。不得将相同图像许可2478与20197同一化，也不得将后代引用推成JSS1999/TW1.0原始服。



## 2026-10-17 — SRC-STAGE-A-EARLY-SOURCE-GAP-TRIAGE-R1

性质：**现存归档来源+公开有限发现检索的缺口可得性审计**，非新取得的原始JSS1999/TW1.0服务器一手数据。五类既有官方2001-04-18村庄服务与TW1.0原始客户端通用消息形状不得拼成同版运行事件；根来源Git blob：
- 早期五服务合同 `research/recovered/STONEAGE-EARLY-VILLAGE-SERVICE-JOURNEY-R1.json` / 7b6c724999e52a421af77d8c8e1e9351288e11ff；
- 原始官方手册派生档 `research/recovered/STONEAGE-EARLY-CONTENT-GUIDE-MANUAL-R1.json` / 54404a8118f125a9a53eabbb8bad8c4a0d07b190；
- Stage A联合审阅入口 `docs/STAGE-A-CONSOLIDATED-REVIEW-R1.md` / 07c9950a40d110d4dabb80b11412db8b4ea64ba9。

本轮发现检索包括日本石器时代1999–2001、长毛象巴士/记录点与titan.co.jp手册地址、2000年中文公车费用关键词；未发现可归属同版并补齐五类具体服务字段的新材料。网页阅读器访问 `https://web.archive.org/web/20010418083149id_/http://www.titan.co.jp/stoneage/manual02.html` 出错，仅为当前访问失败，**不是不存在**。详细搜索词、缺失供品/保存ACK/车费/路线/医疗价格/工作奖励/物品消失时长、重开要求与否证记录见 `research/recovered/STONEAGE-STAGE-A-EARLY-SOURCE-GAP-TRIAGE-R1.json`、`docs/STAGE-A-EARLY-SOURCE-GAP-TRIAGE-R1.md`。不存版权源HTML、商服载荷及游戏资产，未运行原版客户端或原商服；不证明同版服务已经存在或完全消失。来源包独立Action39001916143/job117306453768 SUCCESS仅证明本次证据合同可审计。

五服务因缺失早期原始业务量值仍OPEN_EVIDENCE_LIMITED；不填0价/地图相邻边/掉落秒数/奖励ID。九系统7 PARTIAL+2 OPEN，Stage A终验待用户联合审阅、Stage B GATED、R79 PAUSED_NON_BLOCKING。


## 2026-10-17 — StoneAge经典外挂与后期内挂来源谱系初录（LEGACY-ASSISTANT-HISTORY-AND-PET-COVERAGE-01）

本次新增**以网页正文与可确认发表日期为依据的出处登记**，不是旧外挂二进制/代码验收，也不是所有外挂穷尽名录。规范化每条来源的题名、发文日、关联软件名、支持的具体行为、版本边界与替代解释，详见 `research/recovered/STONEAGE-LEGACY-ASSISTANT-AND-CONTENT-GAP-R1.json` 的S01—S14。

同年代玩家文章（内容为C等级的同期回忆/评论，非开发者发行单）：
- S01 2001-06-15《有感于石器时代的辅助软件》：https://news.17173.com/z/stoneage/content/2001-6-15/n438_354378.html — SADE受到玩家讨论，不证明首发版号。
- S02 2001-08-05《石器时代回忆录》：https://news.17173.com/z/stoneage/content/2001-8-5/n813_729424.html — 变速齿轮、CSS、SADE、SAC和kittygift的当事者回忆；并不逐条认证先后次序、日版来源或具体代码。
- S03 2001-11-11《闭上眼睛说真话》：https://news.17173.com/z/stoneage/content/2001-11-11/n691_607613.html — SaCh1.23使用与复制争议。
- S04 2002-01-19《关于游戏外挂问题之我见》：https://news.17173.com/z/stoneage/content/2002-1-19/n347_263863.html — sade H++ / sach / sta / 变速齿轮的用户对照。
- S05 2002-03-10《Sta2.52新增功能全面解析》：https://news.17173.com/z/stoneage/content/2002-3-10/n974_891060.html — STA2.52缩屏料理、练功、动作条件等用户评测。
- S06 2002-03-21《STA与SACHXP的比较》：https://news.17173.com/z/stoneage/content/2002-3-21/n936_852654.html — 两系的逃跑、自动战斗、脚本与料理差异为当年用户观察。
- S07 2002-08-19《回首往事，我们从外挂中走来》：https://news.17173.com/z/stoneage/content/2002-8-19/n337_253594.html — SADE分版本功能、LiLiCoCo和早期程序员逸事；**文内自称个人杂谈/记忆，不等于JSS一手史料**。
- S08 2002-09-27《轻松搞定石器时代》：https://news.17173.com/z/stoneage/content/2002-9-27/n286_202934.html — 玩家对人宠HP/MP阈值、战斗设定及自动复活的操作偏好，不能反推初代正式设计数值。
- S09 2003-06-18新浪《SachXP++ help》：https://games.sina.com.cn/z/sta/2003-06-18/13369.shtml — 电子攻略帮助文件，须与真正外挂程序区分。

晚期/社区资料（D级年代外推受限，个别为开发者自身发表的对应时代一手用法）：
- S10 2016起发布、后经2026编辑的石器圣手论坛：https://www.play56.net/forum.php?mod=viewthread&tid=1649
- S11 2020起发布、后更新的ASSA辅助面板：https://www.lab.welovesa.com/viewthread.php?tid=3671
- S12 无同年原始署名日期的STW/强者/小明四软件比较转载：https://www.shiqisifu.cc/Article/1/News_89.html
- S13 2023年SaSH项目作者帖：https://www.lovesa.cc/forum.php?mod=viewthread&tid=700
- S14 2026年ASSA脚本命令材料：https://www.zshiqi.com/xindejingyan/5.html

这些晚期网页**不能**证明2001原初1.0、2002大陆1.82已拥有所有脚本、宠物自动筛选或某具体辅助版本。没有取得早期发行包与hash，工具自身可运行性未测试；来源不含需要执行或再分发旧外挂程序的授权。新设计候选由DD-025独立作DESIGN评级。

宠物原版覆盖缺口固定依据原有 `docs/specs/STONEAGE-TW10-UI-RESOURCE-BIND-R1.md`、`research/recovered/STONEAGE-TW10-UI-RESOURCE-BIND-SCOPE-R1.json`、`research/recovered/STONEAGE-25-PET-GROWTH-R1.txt`，其Git blob已在本轮机器清单钉住；没有用上述外挂网页来填补原始宠物实体/成长值。


## 2026-10-17 — 后期资料网站结构与可查任务/宠物目录｜只供研究发现

新增三个**当代访问可用而版本归属不同**的参考网站，不作为1999 JSS原始任务/宠物表；其URL、适用范围、严禁提升判断与同源project Git blob均写入`research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json`：

- `WEB_QUEST_INDEX`：https://data.sa25.com.cn/tasks/index.html 。当前展示1.82—8.5共131个任务目录，页面自己说明131待核验；用于逐条检索有出处的任务候选和网站信息架构。其“1.82”栏目归类并不证明这些任务属于1999日版或台湾1.0商服，没有同版任务脚本的权威证明。
- `WEB_PET_INDEX`：https://www.shiqi.club/renwu/chongsheng/pets 。发布者明确称其Lv1宠物野外/任务地点以“本服资料”为依据；可帮助定义未来网站“宠物—地图—NPC—条件—原始出处”查询视角，**不能**据此导入初代全物种名单或野外坐标。
- `WEB_EARLY_COMMUNITY_LAYOUT`：https://news.17173.com/z/stoneage/newsa/new.shtml 。该页面是8.0时代的玩家资讯栏目/新增内容样式，可见新任务日志、宠物装备等8.0相关说明；不应把后期界面当早年v1.0当代官方画面。

采集所需页面标题、发表时间、旧版网站导航、图片/文本版权归属和首见年代；若页面今日可访问仅认证“目前公开有该页”，**不认证从首发起一直存在或字段与当年服务器完全对应**。不将社区数据库整站抓取进入Git或直接复制未来新作网站。未取得合法可分发许可的原客户端美术及旧运营网页一律只引用可核查元信息/页面链接/指纹，网站正式发布须单独审批授权。


## 2026-10-17 — 早期人物/宠物图片分类及登录交互的新增可核验来源

SRC-SA-20010614-STONEPIC-CATEGORY-01：https://news.17173.com/z/stoneage/content/2001-6-14/n84_511.html 。文章标题《stonepic的图片编号》，作者寻梅子・古月，确定发表日期2001-06-14。来源为同期玩家技术经验，不是JSS/华义原始代码，也未锁定其观察的精确地域、客户端版本。文章提供宠物照片7246—7366、人物照片7367—8566、操作界面9093—9288、人物动作9289—82726、宠物动作95883—125995，以及声称的大陆登录图片126766和后续类别。前16段同号确实属于本项目TW1.0原盘ADRN命名空间，后6段越界；类别只是该玩家用途断言，同版渲染/身份映射还缺证明。当前原TW1.0未被文章归类的图号0、95879—95882保留未知。

SRC-SA-17173-GUIDE14-01：https://news.17173.com/z/stoneage/guide/14.htm 。旧新手指南介绍客户端启动/WGS账号/服务器/角色创建、12造型、调色与朝向、NPC/任务/UI操作，但**页面当前未找到原文发表日期**；并非TW1.0原始同版真实屏幕的证明。

SRC-SA-20010709-CLIENT-FILES-01：https://news.17173.com/z/stoneage/content/2001-7-9/n653_569161.html 。2001-07-09玩家文章记录游戏目录、地图缓存、F12截图存储位置，限玩家当时的安装与使用观察，不能说原版CD自带全部服务器地图。

对应版型/出处/编号逐项确认与否定项见 research/recovered/STONEAGE-EARLY-VISUAL-ID-RANGES-VERIFIED-R1.json。版权图片没有进入Git，原始登陆画面、宠物名字、人物身份的同版准确贴图均未恢复。


## 2026-10-17 — 原版登录/人物来源与JSS建角手册

- 第一方实际快照：https://web.archive.org/web/20010418082314id_/http://www.titan.co.jp/stoneage/manual01.html；10924字节，SHA2565784d9f9e0ddca26240b4c163101759d772cadcc9ef8c81ef24bf99145dbd560。由manual02.html#2015链接去片段后取得，实际日期与请求不同。早期日服说明，非TW1.0/1999对应认证；无原HTML/美术入Git。
- 原台湾1.0零售盘保存包CD_DIC.rar：沿用既有MD5/SHA1及镜像尺寸、sa_3.exe SHA256cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a；本轮新静态调用、参数来源与候选写入为派生元数据。精确Git blob与Actions/artifact链由STONEAGE-TW10-LOGIN-AVATAR-ACCEPTANCE-R1固定；不声称原游戏执行、全部人物图号或真实界面。


## 2026-10-17 — 具名送贝壳NPC/地图/物品来源

- 新见证：https://news.17173.com/z/stoneage/content/2001-12-10/n281_197533.html?_platform=PC ，诗雨，原发表栏2001-12-10；限当前取得的同期署名玩家记录。姓名位置参考与贝壳获取途径有述，未锁具体构建或认证2001网页字节。与新浪01186091_c2.shtml汇编和2003-05-29 rwgl1_1.shtml的丢弃/重复操作分别处理。
- 固定后代保存包d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5，源Action39026390233，具名NPC创建/唯一ExChangeMan参数、地图头、活动itemset2414/2415连接；原始二级脚本、对白及地图没有公开入Git。来源ZIP/raw/派生blob链见STONEAGE-WORLD-NPC-QUEST-ACCEPTANCE-R1。
- 三页实际URL/编码/字节SHA256及事实见WITNESSES-R1；当前日期不等于历史快照认证。指定新浪URL在20011231附近Availability一次空结果不扩大为全网缺席。原台湾1.0商服同版任务、ID和真实运行保持OPEN。


### S05 STA2.52具名版本来源重新取得

https://news.17173.com/z/stoneage/content/2002-3-10/n974_891060.html ，原发表栏2002-03-10、作者☆阿仇☆，用户评测非开发者release notes。来源Action39026963821；当前HTML字节SHA与正文规范摘要、9条类别及ZIP/raw/派生Git blob保管在STONEAGE-LEGACY-STA252-ACCEPTANCE-R1。只归档派生事实和状态，不复制全文或执行旧软件。


## 2026-10-17 — S03/S06/S07/S08早期版本归档加深

源Action39033762316/job117399363842，HEADb4c7f322ac4e4e5db581b2af580e262db1183ef8，四页UTF-8严格解码、原始响应及正文SHA/发表栏/作者分别固定。原始HTML不提交；派生STONEAGE-EARLY-ASSISTANT-VERSIONS-R1.json及ACCEPTANCE-R1.json永久保存，含源ZIP/raw/Git blob和代码凭据。

- S03 https://news.17173.com/z/stoneage/content/2001-11-11/n691_607613.html?_platform=PC — 水银水晶VS炎之天舞，2001-11-11：SaCh1.23提及，不把邻文复制指控绑定具体构建。
- S06 https://news.17173.com/z/stoneage/content/2002-3-21/n936_852654.html?_platform=PC — 地藏乌拉，2002-03-21：STA/SACHXP用户比较7观察面；无精确版号，矛盾/传闻/主观性能不升级。
- S07 https://news.17173.com/z/stoneage/content/2002-8-19/n337_253594.html?_platform=PC — E_skyline，2002-08-19：SADE部分版本回顾，8列表条目另加0.2g变体，不是发布日志。
- S08 https://news.17173.com/z/stoneage/content/2002-9-27/n286_202934.html — 天行，2002-09-27：7配置/经验观察面，原称MX/SAT/阿背/天使，不绑定未知精确版本，运气归因非因果规则。

当前发表栏不认证当年网页字节。额外线索“初试STA2.53bate7的小心得”由S06页相关链接导向异常转义URL，原形式404、清理目标后本次检索不可访问，搜索无结果；本次没有取得正文，不以标题/推荐日期推断功能或发布日期，保留具名待追证。


### 历史资料站来源发现与查询草案（同轮）

当前新浪01186091.shtml可见面包屑、任务分组、页内索引和分页，17173迁移文页有栏目与相关文章；本条只登记当前发现，不认证2001—2002原导航字节/布局。JSS manual01归档URL本次阅读器未取得，已存早期手册正文保管仍有效，不能用读取失败推翻旧证据。实际历史栏目树、运营商改版日期及链接元数据待下一包实取，未完成导航源指纹验收。

STONEAGE-HISTORICAL-WIKI-QUERY-CONTRACT-DRAFT-R1.json引用四个既有派生Git blob，仅作六个跨域查询/未知边界研究夹具，不是原始站点资料或已发布数据库；对应规范STONEAGE-HISTORICAL-SITE-IA-AND-QUERY-CONTRACT-R1.md。


## 2026-10-17 — SRC-JSS-HISTORICAL-NAVIGATION-2001-R1

原域http://www.titan.co.jp/stoneage/，仅限归档响应身份/链接元数据。实取完整URL与实际日期/字节SHA在STONEAGE-HISTORICAL-SITE-NAVIGATION-R1.json及CATALOG；三次派生、ZIP/raw/Git blob、运行HEAD/tree/job见ACCEPTANCE-R1。源Action39035106551初次仅2页；39035257822增加有限回放与图片索引条件5页；39035407893取得具名框架子项后6合格页，历次结果不删。

- manual.html实际https://web.archive.org/web/20010417160918id_/http://www.titan.co.jp/stoneage/manual.html ，3775字节/SHA2567c3f5bbd6ff1d9c689fed08742f729093c4fa9f3187694f2c5451350065db713，47链接。无正文品牌字，原域/日期/两份已认证官方手册出链共同作身份门，不泛化给任意图片页。
- /实际20010425173204、index.html实际20010406012216，均215字节/SHA256c87d79a4c48880d28ebabda7059d4f3fa99cc89d7be78f5d1f837fcfe526ce4d，框架引用menu.html/top.html；不是完整视觉首页或两套内容。
- manual01/02实际20010418082314/20010418083149，原SHA与既有官方手册凭据一致；本包新增真实锚点与链接关系。top.html实际20010414014135，7424字节/15链接。
- menu.html实际20010414013651、2683字节/SHA256b185fbbb0ab0c144b78f0384a91932deadd7eb258313f0b6515124c61909141c，保留15诊断链接但未过正文品牌门；不纳入合格来源图，不称错误页/全网无资料。
- stoneage.17173.com的根、index.shtml、guide/guide.htm、jiaoliu/jiaoliu.shtml本次实际分别20040115054253、20060205112246、20040811084749、20060205112723，全部超1999—2002窗口。响应指纹保留为拒绝倒填证据，不升为同期媒体导航。

64片段引用在已取目标快照中存在，不同日期不认证当时点击与目标内容兼容；标签至22域/19集合只作22条候选研究路由。网页导航不证明原版宠物/地图/任务/数值。原HTML/图片/音效/执行文件未入Git，完整站点恢复仍OPEN。


### 2026-10-17 — 17173年代标签玩家页的旧导航线索（迁移后页面，不是2001快照）

- MEDIA17173_20010614_PET20 | https://news.17173.com/z/stoneage/content/2001-6-14/n37_953148.html | 当前页面显示2001-06-14，作者未知；20条玩家宠物名称/地点候选，正文末明示旧目录http://stoneage.17173.com/jingyan/jingyan.shtml；原年代快照未取得。
- MEDIA17173_20010614_CATCH_GUIDE | https://news.17173.com/z/stoneage/content/2001-6-14/n500_416268.html | 当前页面显示2001-06-14，俄罗斯牛奶；另含旧经验目录URL；玩家捕捉方法不等于原服捕获率规则。
- MEDIA17173_20010614_NORTH_ISLAND | https://news.17173.com/z/stoneage/content/2001-6-14/n781_697151.html | 当前页面显示2001-06-14，帝皇圣者；送货及路线作为玩家见闻，非同版服务器配置。
- MEDIA17173_20010614_PET_GROWTH | https://news.17173.com/z/stoneage/content/2001-6-14/n289_205254.html | 当前页面显示2001-06-14，阿花；成长/隐藏属性是作者分析。
- MEDIA17173_20010911_PET_RECS | https://news.17173.com/z/stoneage/content/2001-9-11/n907_823387.html | 仅查询摘要确认日期栏、作者when1314和宠物推荐主题，本轮直接阅读超时，不冒充全文采集。

所有页面均为当前网页观察、非取得2001原始存档；旧目录自身当前含后期版本内容，不能证明其2001版栏目结构。证据包 docs/STONEAGE-EARLY-MEDIA-CONTENT-BRIDGE-R1.md；机器索引 research/recovered/STONEAGE-EARLY-MEDIA-ARTICLE-PET-SOURCE-R1.json。署名玩家说法只作候选内容，不认证1999/TW1.0原服规则或全宠物名录。



## 2026-10-17 — 17173旧栏目三次Wayback回放／严格晚期来源边界

- 原路径`http://stoneage.17173.com/jingyan/jingyan.shtml`，请求20010614000000/20021231000000，真实返回均为`https://web.archive.org/web/20060115044722id_/http://stoneage.17173.com/jingyan/jingyan.shtml`，11376B，原HTML SHA256 `b6ad1696042cdc3cdfaac671506040505be2b129c0ae9aeb9e3d3dec74753850`；不得归为同期2001原媒体目录。
- 原路径`http://stoneage.17173.com/chongwu/pet.htm`，请求20011231000000，实际返回`https://web.archive.org/web/20040204024948id_/http://stoneage.17173.com/chongwu/pet.htm`，6546B，原HTML SHA256 `54da75bcbd7b703a336f99f00b160701c8ef8cb6c89358f3b6a08a51df052b26`；属于晚期导航线索，并非2001原目录。
- GitHub Action `39038286655`/job`117412434137` SUCCESS，artifact`12102473238`（1094B ZIP SHA256 `ff695f20c4e38d974040ffc73f668ef7f82410193ffdd15af29b68c1819e79fd`）。无版权原HTML入库，只有raw派生3520B SHA256 `e50cf9406ba4f057915adf84536dbb6d268d8bdd3303779a7da7b783cb9d6c57`，Git blob `0d5ff5dcb8532626ff40891ff76e92cff378ec26`，待再查精确旧栏目才可重开。三次Availability HTTP503为接口结果不证全网缺失。

 
## SRC-TW10-ORIGINAL-SPR-PLAYER-RANGE-INTERSECTION-20261018 — 原零售盘图号与帧关联

- **直接事实层 S（TW1.0客户端派生、已固定来源）**：ADRN、SPR-GROUP/ANIMATION/FRAME四份gzip派生与固定源manifest，全部SHA见`tools/stoneage_pet_asset_growth_catalog.py`；项目已验125996位图ID、464 SPR组、39065段动画、242085帧。原元数据不含版权画面，保留来源身份。
- **类别候选层 C（玩家当前迁移网页，非JSS/TW1.0官方分类）**：2001发表栏17173`stonepic的图片编号`，先前已在`STONEAGE-EARLY-VISUAL-ID-RANGES-INPUT/VERIFIED-R1.json`实录及独立原图号存在性验收；本轮不重复算作新原来源。
- **本轮衍生交叉层（仅可复核数值）**：GitHub source HEAD `8aa789eeedc18bef8ba6ce078dbd5ebd92105d5c`/tree `9924c96951e3a5b7d80157fc8d9de2f0ed989495`，run`39076262089`/job`117523936561` SUCCESS；ZIP artifact`12116114738`，ZIP1784B SHA256`fa5ad6bf8f926feb8f8fc54e02c206760dfcaac4dbc28ef814145de7961479ee`；原派生JSON8369B SHA256`e33bdae8c202dcf5a1374746afc505f517d8e1afc557fd07057d2d1811a54fcd`，Git blob`20a82e4d35661785c4e50b44855cf8e8a4e98f3e`。下载与digest独立核验；详见永久机器报告与ACCEPTANCE-R1。
- **只认证**：人物动作区间137508帧引用/240SPR组；宠物动作区间70236帧引用/124SPR组；NPC、两种头像、物品、UI五个静态区间没有被本SPR帧表引用。不会自动认证同版语义、原游戏显示、人物/宠物数量与原服务器任务；静态画像可能走其它资源选择路径，0命中不能解释为“客户端不用”。

 
### 2026-10-18 — SRC-TW10-STATIC-ITEM-BITMAP-MESSAGE-R1

- 原始客户端来源 S：台湾1.0编译接收消息中完整背包 `S:I` callback 0x30922 的第5个整数图号槽位、增量 `I` callback 0x325f0 第6槽位、地面物品 `C` callback 0x31260 第4槽位；结构来自原盘固定schema Git blob `e39a3a6020b578da017ab0bfa9369dc083e0b700` 与原客户端callgraph报告 blob`bdcd7b7ed5295db78b5d8cbdad58d5ce94802f31`。字段名graphic_id来自早期生成通信谱系，位置V1_DIRECT。**没有从原客户端观察到任何真实graphics值/绘制函数与ADRN的1:1同版运行映射**。
- 来源候选 C：2001显示日期的stonepic玩家图号5973—7003标签为装备料理素材，此文章及编号来源已在旧表入册，不算新史料。
- 原始台湾1.0图片物理层 S：ADRN全源meta SHA由`MANIFEST-R1.txt`锁定，本轮源Action39078043125/job117529172357实际SUCCESS。1031项位图候选号物理数据全在原盘，尺寸宽16—64高14—79，1030个不同压缩RD原块SHA256。**6042、6077共享原块哈希**；不解释为相同游戏物品。另四静态对照范围的尺寸、offset、flag与摘要在归档报告中。
- 完整产物：artifact 12117477340 ZIP4474B SHA256 `04900b9b905610a5ae0c7b148ef8c9a12898059683fb0c35efc92fadd0b3f2c9`；raw JSON21307B SHA256`9916bab4e8b94188e8b4dc9c0e5f6cd2537464311f3c3409a6a04d72fffec2b8`、Git blob`1210b0f910c353d58a3d6a4c458dda38f48aba86`。原版权像素、同版原服务器master没有提交。研究规格、永久JSON/验收回执和回归测试相互引用，来源成功不等于早期物品图鉴/商店定价恢复。

 
### SRC-TW10-ORIGINAL-MAP-NUMBER-COLLISION-SOURCE-20261018

原盘`COLLISION-ATTR-R1.tsv.gz`的SHA256 `d26b318ea73833bd7cc68abc8b5798a81b76ef9309cc91b137f7a55c6c8275dc`及原客户端地图缓存图谱Git blob`f8792fb6c7ad22001d8400b293c775304caeb6a0`均为早期S级源。2001玩家图像分类仅C候选区间，原blob`11bb14ef00c2ed354c5f00f510da8783376f1f28`。

新完整交叉表源Action39078746682/job117531202789 SUCCESS，9,286原独立map_number资源属性分别在玩家小地形/大物件/NPC号段关联4571/1271/101，其他3343。hit0/1/2=5929/3295/62为**资源属性而非地图可通行格子计数**。实际成功归档Action39079097177，JSON原blob `7d4d5d2cae224c093b3e85e8ef1bfc49b54c5981`、raw8494B SHA256 `5efa5972fe68d38d0e85aad3c7e13d6c4cd588c0f1b81a5900ba79e8a6711dd9`、ZIP1795B SHA256`8d48e37f0eae58b7659e7315ef83ccffe95c36d8728b6fe76d68d7d0d1dab5a4`。这些不是9286张原版field map、101名NPC或早期服务器内容来源。

 
### 2026-10-18 — SRC-TW10-ORIGINAL-AUDIO-DIRECT-API-CALLSITE-01

原盘声音WAV与容器物理数据由旧来源`STONEAGE-TW10-AUDIO-DATASET-R1.txt` blob`094becbc92397ee8abf72a014deffffabc97a316`固定：114索引SFX、116散音效、11散BGM，107条同名字节相同、1条封装变体、6条PCM不同；这些不是本轮新内容。原编译exe先前IAT报告blob`0054c8c0c2a34652caec4ab89feac5bf821d75f7`已有WINMM/DSOUND导入。

**本轮新增同版原始指令事实**：研究Action`39080460322`/job`117536170852`实际SUCCESS，原exe SHA256 `cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a`，WinMM调用地址8个、DSOUND跳板1个及指向该跳板CALL1处，可查原报告`STONEAGE-TW10-AUDIO-EVENT-GATE-R1.json`。完整独立ZIP原字节1999B SHA256`b5a36f3fa0c42c01dc60fd6cff9f2d3dd21443606e546f6f4da38dbb5a180d4c`、内部JSON11013B SHA256`ce1cd5738dac1a571999eea9ea6ee5ead86341f30bff4f0c4e4610a80f917047`、Git blob`67cc3707d45b6f079432b1db29b043851571b518`独立核对。这个调用源不证明“原游戏第几关播放什么BGM、宠物战斗声音”，仍缺原事件选择参数。无版权声音/程序输入入库。


## SRC-JSS2001-OFFICIAL-INTRO-PET-VISUAL-20261018

- 新正文源：原http://www.titan.co.jp/stoneage/contents.html，由既有官方top真实出链进入，实际https://web.archive.org/web/20010417155051id_/http://www.titan.co.jp/stoneage/contents.html；6426B SHA256 a5553d476ed39deadde296d589d0a9eabe1378e11cbd528f8947f37eb74e4a8b，Shift-JIS严格解码。正文12人物/48含配色外观、5携带宠、5人队、低等级免费治疗（阈值未知）及设施/伙伴说明，只属JSS2001官方描述。
- 15真实截图出链中10原JPEG成功，sakss02/03/04/05/06/07/08/10/13/14，全160×120；每张实际20010618/19时戳、原URL/最终URL、字节数/SHA及原图真正尺寸见STONEAGE-JSS2001-INTRO-SCREENSHOT-SOURCES-R1。未取得01/09/11/12/15；两个有限请求批的错误和2021/2022晚期主页重定向保留在INTRO-SOURCE-ATTEMPTS-R1。不可推缺席，不能用原页4月日期倒标图片。
- 10图逐一实际目视观察：村落概览、医院/肉店/宠物店/武器店外观、图腾、PET STATUS、背包、组队场景、名片窗；不从附近文字自动给未取得图片定性，不从缩图猜全屏坐标、具名宠物物种/SPR或TW1.0身份。像素不入Git。
- 旧正文复用源：manual02实际20010418083149，28434B SHA256 50b9771ec501067136629c8e083a190e979e53dd9ba141903f78b76d43b602cc，与旧来源相同；12节新结构化事实与hash见STONEAGE-JSS2001-PET-MANUAL-CONTRACT-R1，非新增网页。按钮点击/右键原描述不同、未知公式/ID/时长全部保持。
- 派生物与独立重放脚本/测试/Actions纳入仓库；来源实跑、ZIP/raw摘要及分支/main状态只能在实际成功后追加回执。JSS2001不自动认证1999/TW1.0；不公开原HTML、版权图像或旧程序。


## SRC-JSS-OFFICIAL-EVENT-VENUE-20261018

- 起点是此前已验官方top→event真出链；本轮新取event实际20010417155224/1587B/SHA256 f11aa3a19be0dc307ec4580b0c8efa919c6dcaca3a1cac988656bd32ff376fd1，四真实出链分别预告、结果、玩家赞助、会场；本轮未查结果和赞助页。
- eventjss实际20010418090522/4166B/SHA256 51c237c961002d862fcba2a4ea3a10aa67afdf9c87d1e523818cc2db3c7dea93，限两项社交活动预告；年份缺失、联谊集合时间冲突、稀有宠未具名、评论/报名表单注释边界保存。公告不是NPC任务脚本或获奖记录。
- eventmaz实际20010418085855/2652B/SHA256 2a52793ecff532885090d3336bea2cc00c6ed5ecc518f285dc41b47a1b9ec4bf，官方四村聊天室入口坐标和售票/引导角色流程；不补票ID/价格、地图floor、NPC实体或服务器事务。三页Shift-JIS严格解码无替换。
- 原6JPEG mari01/karu01/samu01/chat01/jyajya01/chat02实际均160×125，捕获分别20010701072151/20010630212945/20010701073936/20010630190951/20010630212710/20010630210857；各字节摘要和最终原URL见STONEAGE-JSS2001-OFFICIAL-EVENT-VENUE-R1。逐张目视观察及指纹见CONTENT-CATALOG-R1；红字是官网编辑标注，不证明游戏UI本来含同样文字。4月HTML不认证6—7月图像同刻，JSS截图不认证TW1.0构建。
- 首次抓取、基线1943602字节CURRENT-STATE前缀、原文/可见文本/SHA与来源身份见SOURCE-INTAKE-R1；永久派生报告/负面边界测试和独立源重放工作流已形成。后续Actions、ZIP/raw保管与主线结果必须实际成功后再记录；不保存原版权HTML、JPEG、游戏二进制。


## SRC-JSS-OFFICIAL-FIRST-COMEDY-RESULT-20261018

- eventjsk实际https://web.archive.org/web/20010418085802id_/http://www.titan.co.jp/stoneage/eventjsk.html ，5041B SHA2568287f0bf401201f6931edd53758129e6bb447293d0c1211efc2413247814a541；16目录题目、14详情原链，第一回搞笑行明确eventj09。反馈端点未访问/提交。
- eventj09实际https://web.archive.org/web/20010422015200id_/http://www.titan.co.jp/stoneage/eventj09.html ，2153B SHA256230a804678c4fa21d3df9a574637a921309e25649dbe72e87e895726356724a9；Shift-JIS严格解码无替换。模板横幅与正文不一致保留，4奖项/临时加奖为官方报道，未具名稀有宠不可映射物种/SPR；获奖者栏仅存指纹，不提取成宠物名。
- 误预取eventj07真实回放20010421042208、2002B SHA25696e0fa659c4951dd102aa53da88110221156222a8777c0ae9fe8740a19ff4650，属别的决斗赛。实际错误/纠正路径保存在SOURCE-INTAKE，不列本轮合格结果正文、不抽取其奖励/人物事实、不隐去失误。
- sass0901/02/03三个原JPEG路径本轮回放404；各一次Availability请求均429后停止。未取得像素或实际尺寸可验，仅HTML引用和声明尺寸；不是全网没有副本/历史无图。请求/错误/来源身份全部在STONEAGE-JSS-EVENT-RESULTS-SOURCE-INTAKE-R1，未存原HTML或图像。
- 永久结果派生STONEAGE-JSS-EVENT-RESULTS-PET-ATTRIBUTION-R1，以旧原预告派生报告1fc8ca061330655483cbc931f93043be7c3792a9作上下文，跨届连接明确REJECT_EDITION_MISMATCH，不由奖金额相同认同活动。独立源CI/ZIP/raw/主线接受在真实成功后单记，原服与TW1.0同版身份未认证。


## 2026-10-18 — JSS-FIRST-PARTY-PET-FAQ-01官方来源

- 从原导航报告已认证top实际20010414014135的faqmenu真实URL出发；导航旧源只作已验依赖，不计本轮新取得。两页严格Shift-JIS，0解码替代。
- faqmenu原http://www.titan.co.jp/stoneage/faqmenu.html，实际20010417155624，3356B SHA256`d5ea757e563d0bf86ad96b72dc0081761b447fa3771e00a463919b89b7017f5f`。3详情链接、4题组12/16/4/9共41标题；9项已修正问题只是目录分类，没给修复日期或版本。
- faqgame真实目录链接因明确敌/宠显示问题而选择，实际20010424225131，5155B SHA256`1676093fcccaaeacd234df2dcd7fa05f1c0337c365dc787aea83b3f41fafcf91`，12问答。正文具名任务仍在调查、决斗刷新榜单/窗口256色与时间调色板说明、历史支持建议分开登记。
- faqquest的一般提问标题不能从文件名判成任务攻略，该正文与faqstart、兼容声音档sa_se.lzh未请求。无图片/音效/程序取得；正文/目录快照不当修复时间或同构建。
- 永久派生报告与SOURCE-INTAKE保留各题/答案指纹、归属、原请求/最终响应及完整历史前缀摘要；规格STONEAGE-JSS-FIRST-PARTY-PET-FAQ-R1。原HTML/版权资产不入Git。独立来源CI、ZIP/raw/Git blob及主线接受仅在真实运行后登记。


## 2026-10-18 — JSS-FIRST-PARTY-PATCH-PET-QUEST-01单页更新史

- 旧已验top真实http://www.titan.co.jp/stoneage/verup.html，实际20010417162544，11239B SHA256`ba71d859f34f31261f4293dc61583c53a8e77133898c4a8148c544a452abc3cb`，Shift-JIS严格解码。2001档案中的运营商1999-10-18至2000-09-11自标日期，不是1999档案/部署或构建认证。
- 全40有序日期块只存原日期/星期/正文指纹，含同日两记录及星期冲突；选择7组宠物寄存/技能/邮件语义，不宣称40条完整恢复。FAQ比较源SHA256`38ebbeca6b04d4a3a229da8ac117e76bc083fcd6e03b7ece6db660b58cf153b0`；泛称修复只同功能/缺陷族，不认证具体症状。三具体任务标签未见只是此页结果。
- updater/manual未跟随，无程序/原资产下载。PATCH-HISTORY-SOURCE-INTAKE-R1保请求/最终URL/前置身份，永久派生/规范与独立来源验收分开保管。原HTML不入Git。


## 2026-10-18 — TW-WAYI-OFFICIAL-WORLDLINE-SOURCE-01与22域R4

- 旧认证主页http://www.wayi.com.tw/stoneage/重新取实际20050615023834/45669B SHA256`4a4a7f0667a8d71b1d37ab0b73712793cf2d7e8a6cd7a7a158a487d060657397`，不计新页面。实际HTML href指向game/game01.asp，未执行点击/脚本。
- 新正文http://www.wayi.com.tw/stoneage/game/game01.asp，实际20050614002509/20444B SHA256`c0a2f96c1d0232eb3f94328481ff512c3efed63daeab912fcc5dd0c397f1ba0d`，Big5严格解码，5组/9版本标签及具名大陆/精灵王叙事，不是9客户端或统一正史认证；失落世界身份保持问题。
- 原正文3×3 pic2_1—9.gif八张实取，实际2006-01-05，大小/摘要/格式/实际尺寸/帧数及局部插画观察写WORLDLINE-R1。第7片首次502、一次重试成功；第9片404未取，完整请求在SOURCE-INTAKE，缺角不补，不推全网不存在。原HTML/GIF不入Git。
- R4逐行保留22域原状态，11份来源指纹、7粗profile/9证据上下文、全官方覆盖缺口和下一有限真实详情页来源共同存档。世界故事按台湾2005运营商归属，JSS1999/TW1.0、精确构建与原NPC/任务/宠物表仍OPEN。独立两页/八图CI及ZIP/raw接受须真实运行后记录。


### 2026-10-18 — 官方冰世界详情：12个原地图名与六场景

按远端main `12d45f491ece5aa53a66b8ce17a64ddab7978cd6`、tree`1af86bcfd66c850024e7fd8e462ecd26667e2ad5`重新启动，核338分支、0开放PR、同HEAD9项main SUCCESS及连续性/完整CURRENT等七文件。TW-WAYI-OFFICIAL-INTRO-DETAIL-01沿真实第一出链，只取game01_01.asp正文及其六张原场景图；实际主题为瑞爾亞斯（冰世界），不从编号预设宠物/任务。

正文实际快照20050614003328，26346B SHA256`f7e10861dd9f8ee3bef19c46863c7bc818d17635ffecab41b0189c63ff2b234c`。取得官方12个新地图原名、冰雪/作物生长困难/居民叙事和“第十大莊園”序位；未恢复地图ID、路线、坐标、NPC/任务/遇敌表。六原JPEG全部220×163并逐张目视，实际快照2006-01-05，与2005正文分开记录；图注分别指冰顫通道、议会厅、24小时便利店、庄园专卖店、训练所和武器店，不能提升为真实交易/全天服务/已知NPC/原生分辨率。

正文“瑞爾亞斯”与三图注“薩爾亞斯”原样保留为UNRESOLVED_VARIANT_OR_TYPO_OR_DISTINCT_NAME，不静默纠错、确认别名或合并实体；骑乘外观仅HYPOTHESIS，无宠物种类或规则。精确客户端构建/首发日期及冰世界等于整个失落世界仍未证，不回填JSS1999/TW1.0。按现有19集合归档合同新增19个研究条目（地区描述1、原地图名12、场景6），不是19张地图，不新增npcs/pets/quests实体。原HTML/JPEG/程序不入Git。

永久派生与规格：`research/recovered/STONEAGE-WAYI-OFFICIAL-ICE-REGION-R1.json`、`STONEAGE-WAYI-OFFICIAL-ICE-REGION-CONTENT-CATALOG-R1.json`、`STONEAGE-WAYI-OFFICIAL-ICE-REGION-SOURCE-INTAKE-R1.json`及`docs/specs/STONEAGE-WAYI-OFFICIAL-ICE-REGION-R1.md`。本地19项边界测试通过；新增独立一正文/六图、两JSON逐字节重放工作流，远端结果与ZIP/raw/Git blob保管链须随后实际验收，未提前宣称。

**最高NEXT `TW-WAYI-OFFICIAL-INTRO-DETAIL-02`**：沿既验介绍页第二条真实未读game01_02.asp，最多一正文，先核题名/内容，形成一份具名宠物/人物/故事/环境或玩法合同即止；若重复、空或有限取源失败，记录具体结果并回全官方22域队列，不自动递归第三/四页。Stage A仍7 PARTIAL+2 OPEN，Stage B/百科GATED，R79暂停，无整体百分比。


## 2026-10-18 — 官方game01_02.asp单页宠物装备/导师/任务日志来源
- 入口为此前认证game01.asp真实第二条详情href；原URL http://www.wayi.com.tw/stoneage/game/game01_02.asp；实际重定向快照 https://web.archive.org/web/20050614005428id_/http://www.wayi.com.tw/stoneage/game/game01_02.asp。
- 原响应26414B，SHA256 0868e56a81d7037e434a09fd0824a6eb59747494099087f8d1eaeaaa37fb690c，Big5严格解码；来源重放39121796764 / job117658721531 SUCCESS，源合同4个反例测试通过，报告SHA256 9bd6d626d6b8ba30238ffaedd4b1df50e7db5015ccd01ebda83eeb3946b5e45b，Git blob4fb303eb6f8866b5454f994a0d4fedbf52ea76b0，artifact12134856287、GitHub声明ZIP digest75ddb12a310d08ffa8fb32bcb7915c0a2f95648afc406d6cd790e8e7464e5f08。
- 只存规则派生与接纳票据，不入原HTML/图片/脚本。官方2005介绍不提供确切客户端、改版生效日、原服装备表/导师结算/任务日志实体；同页商品包调查需排除。详细SOURCE-BOUNDARY见STONEAGE-WAYI-OFFICIAL-SYSTEMS-R1.md和机读JSON。


## 2026-10-18 — 8.0 宠物装备／导师／任务日志跨版报道归属与可追踪任务

- **既有一方锚点，不重复算新原页**：台湾华义 https://web.archive.org/web/20050614005428id_/http://www.wayi.com.tw/stoneage/game/game01_02.asp 原26414B SHA256 0868e56a81d7037e434a09fd0824a6eb59747494099087f8d1eaeaaa37fb690c，派生blob4fb303eb6f8866b5454f994a0d4fedbf52ea76b0。原源认证历史独立保留，客户端构建/原服未证明。
- **同期新闻源、字节尚未PIN**：https://gnn.gamer.com.tw/detail.php?sn=20167 ，巴哈姆特记者小贤2005-06-08 23:04:46台湾8.0报道：将失落世界改版与宠物装备、导师、任务日志、新骑宠及合成扩展一起说明。此为出版时报道事实，不等于独立记录服务器实际投产；本轮只经网页检索正文，不宣称原HTML SHA。
- **同文转载不得按第二份新闻独立认证**：https://news.17173.com/content/2005-6-9/n50_966545.html ，页面时间2005-06-09 10:30:41且末尾注明「来源：巴哈姆特」，报道内容同源。转载日期是发布日而不是另一次石器版本发布/新建source-lineage。
- **大陆专区、原发布时间UNKNOWN**：https://news.17173.com/z/stoneage/newsa/new.shtml 与 https://news.17173.com/z/stoneage/newsa/about.shtml ，17173页面标示《新石器时代》8.0/华义开发/金山运营；列出宠物装备合成、导师、任务日志以及具名新任务「爱作画的少女」。文献等级为THIRD_PARTY_GAME_PORTAL_UNDATED，缺页面同期原始快照/精确客户端构建/任务ID；它不是华义台湾 2005-06第一方网页，也不验证TW1.0共用数据。
- 机读source_ids、region、lineage、同源去重、验证层级和11合同见 `research/recovered/STONEAGE-80-SYSTEMS-CROSS-VERSION-EVIDENCE-R1.json`，详细见 `docs/specs/STONEAGE-80-SYSTEMS-CROSS-VERSION-EVIDENCE-R1.md`。源提交4eb3d3de/专用Action39123252107已实际SUCCESS 5项档案结构负例；**不是原网页独立哈希/实际运行确认**。原新闻全文、HTML、图片及游戏资产不入Git。


## 2026-10-18 — CN8《爱作画的少女》玩家任务正文来源与2012异文

- 真实 [17173任务目录](https://news.17173.com/z/stoneage/renwu/renwu.htm) `34236B` SHA256`84a4f0bb593f09d2f5dbd180142870b267d846c2c898f9d78477a3e38b7bba8f`，确切标签→href指向 `https://news.17173.com/z/stoneage/renwu/sa80_05.shtml`。后者`24459B` SHA256`328571c2dbabbb337f27f06a76ecaf3eeae621fdad4a0979d8089e980dfd8e19`，UTF8；独立CI首次两次错误`39124563986`/`39124652068`属工具步骤和坐标括号验证问题，不篡改失败，后续源重放`39124716683`/`39125067564`/`39125258450`成功。
- 页面称8.0任务攻略、有14步骤；来源为`THIRD_PARTY_PLAYER_WALKTHROUGH`，原发布时间和2005同期归档未知，不把当前页面页脚Copyright 2026当任务发布日期。玩家记载的2人、5宠、5色颜料和5幅画像交付序列是逐条已源定位**叙述**，不认证原服脚本/物种ID/奖励物品ID。
- 晚期资料`https://news.17173.com/content/2012-04-10/20120410145731224.shtml`为2012-04-10针对8.5的报道，提到完成「无法逃离的审判」后才能接任务及一幅画像，与8.0无前置描述/五幅结尾分开；原HTML未PIN，不保证一方实施证明。
- 成功源Action`39124716683`/job`117667311744` artifact`12135382985`，独立下载ZIP1757B SHA256`b9458b30b3efcc7854f1a8bd845b8edcf511429201f53c2c520606655824f9b6`，内部`derived.json`4349B SHA256`a8fbd74485e53d3a0e6bab442339947a08102fcfa890fd8ce768803a614fbc74`。永久保管`research/recovered/STONEAGE-CN80-PORTRAIT-QUEST-R1.json`及`-CATALOG-R1.json`，出处、负例、同版与后代边界见`docs/specs/STONEAGE-CN80-PORTRAIT-QUEST-R1.md`。原HTML、美术、音乐、程序不入Git。


### 2026-10-18 — 2005编辑时间的巴哈姆特《無法逃離的審判》文献线索（与画作任务区别）

- https://forum.gamer.com.tw/G2.php?bsn=1571&sn=2340 巴哈姆特石器時代精华区；现网页显示「2005-07-19 02:36:12 編輯」，由玩家/论坛整理，页面末尾称出处OURSA。暂未取精确HTML字节SHA、未经历史版面快照对照，不认证原始发表时间和后续改动版本。
- 文献出现“先完成贝克/黄泉任务、暗灵法师/白狼勇士/追猎者三职业合作”作为**审判任务**自己的条件，还有守卫队长涅齊、搜捕令、沉睡洞窟、研究书等；一切只是此攻略当前文字，非原服NPC/任务ID及服务器事件认证。
- 最关键**该指南没给「审判→爱作画的少女」前置边**。2012关于8.5的宣传文案才有此关系，不能使用独立存在的2005审判任务推出2005画作任务也需完成审判。经有限查证仍OPEN，不扩散到未知同版ID。


### SRC-CN80-JUDGMENT-BAHAMUT-2005-EDIT-01
- URL: https://forum.gamer.com.tw/G2.php?bsn=1571&sn=2340
- Kind/confidence: C; contemporary **edited marker** on a currently available curated player guide, not original operator script. Displays 2005-07-19 02:36:12 編輯; credits 1202/uao1222, editor 重灌郎, maker 天波 and other players, explicitly 「出處OURSA~!」.
- Linked old-source redirection points toward http://pisces.sbun.org/oops/ but this reader received 403; original article/first publication not obtained. No immutable original-page SHA.
- Supports: secondary names/locations/team/claimed prerequisite/item descriptions; does NOT prove release date, actual server code, TW1.0 rule, game IDs, actual reward, or Portrait Quest dependency.

### SRC-CN80-JUDGMENT-17173-PORTAL-01
- URL: https://news.17173.com/z/stoneage/renwu/sa80_06.shtml
- Kind/confidence: C; Mainland 8.0-labeled currently indexed player guide with expanded details; actual original 2005 publication/date/HTML SHA not verified.
- Content overlaps Bahamut guide, adds board clue, thief positions and skill-identification order. Do not count as a second independent original author or as an official first-party source. No proprietary site HTML/art/client binaries committed. Derived facts/negative evidence in `research/recovered/STONEAGE-CN80-JUDGMENT-NAMED-CONTENT-R1.json`.


### SRC-TW85-PERIOD-GNN-20060621-NAMED-STORY-01
- URL: https://gnn.gamer.com.tw/detail.php?sn=23856
- Time: 2006-06-21 21:39:50 (publisher displayed); contemporary Taiwanese GNN report. Confidence A for time-bounded reporting, NOT original Wayi web/manual/server build.
- Claims: 7.5→8.5 promotional background continuation, 雷爾 is 艾巴登's subordinate, 伊甸大陆边境 demon army and tribal mobilization; planned beta/rollout, new map, career skills, recurring personal/family activities. GNN web open gave403 during this review, indexed current article text visible; raw-byte SHA remains UNKNOWN.
- Does not support: any TW1.0 association, 8.0 detailed bridging, original NPC/quest/item IDs, actual server deployment or playable story sequence.

### SRC-TW85-PERIOD-GAMEZONE-20060621-NAMED-QUEST-01
- URL: https://www.games.idv.tw/news.php?mode=view&nid=615
- Time: 2006-06-21. Contemporary period gaming press, overlapping operator-attributed promo paragraphs with GNN; precise common upstream text remains uncertain.
- Distinct claim: names «支援前線» quest and describes daily activities plus the named narrative figures, no original official task code. One-source raw-byte runner probe is `tools/stoneage_tw85_press_replay.py`; the byte hash must be filled only after actual source replay, NOT fabricated. Original site HTML must not be committed.
- Does not support: quest prerequisites, gameplay item/NPC IDs, exact encounter/battle execution, actual 7/5 launch success.

### SRC-TW85-17173-20060622-BAHAMUT-REPRINT-01
- URL: https://news.17173.com/content/2006-06-22/20060622092748047.shtml
- Displayed publication 2006-06-22 09:27:48 and explicit «来源：巴哈姆特». Count within the same public reporting family, not as another independent first-party proof. May bridge Chinese localization language, not actual new server content.
- Research-structural contract: `research/recovered/STONEAGE-TW85-PERIOD-PRESS-WORLDLINE-R1.json`. Original news HTML/images and proprietary game assets excluded.

- **2026-10-18 exact source byte attempt:** GitHub Actions run39132023657/job117688962061 failed (6 boundary tests passed, source fetch HTTP403). No source SHA256 or retained HTML; neither missing-website conclusion nor original-byte provenance can be drawn. Follow-on probe reports `HTTP_ACCESS_DENIED_IN_RUNNER` with null bytes/hash if blocked; a green structural CI is NOT historical source-byte acceptance. This failure is an append-only evidence record.


### SRC-TW85-20060623-BAHAMUT-SUPPORT-FRONT-GUIDE-01
- URL: https://forum.gamer.com.tw/G2.php?bsn=1571&sn=3199
- Contemporary-proximity lead, **C player guide**; current page displays «任務三：支援前線», `2006-06-23 19:00:09 編輯`, poster 1202/uao1222. Date is an edit marker, not first original publication, operator deployment or independently pinned 2006 HTML. No raw-byte SHA.
- Supports as secondary text: five-step description of named 伊秋娜/奏敷/布克瑟, supply delivery, dungeon/map transitions, gift parcel and a reward with no actual item identity. Cave theft/logout remarks are player advice and not official feature confirmation.
- Cannot support: canonical first-party quest ID/flags, floor IDs, original target coordinates, NPC item master tables or verified quest settlement; nor TW1.0 origin.

### SRC-TW85-LATER-BAHAMUT-WIKI-SUPPORT-FRONT-01
- URL: https://wiki2.gamer.com.tw/wiki.php?n=2198%3A8.5+%E9%AD%94%E5%9F%9F%E5%A4%A7%E5%86%92%E9%9A%AA%E4%BB%BB%E5%8B%99
- Undated player/community-curated version of same named guide, **C**. Coordinates differ from dated-editor guide (伊秋娜20,27 vs 21,27; 奏敷302,130 vs 303,130; 布克瑟114,310 vs 114,309); it adds level101 and prior `枕戈待旦` conditions. Contradictions OPEN, not verified official fixes nor independently attested 2006 content.
- Downstream secondary cross-reference only; shared text must not count as independent contemporaneous publisher witnesses. No original website HTML/assets mirrored.

### SRC-TW85-WAYI-2006-SUPPORT-FRONT-FIRSTPARTY-GAP-01
- Historical first-party candidate root: http://www.wayi.com.tw/stoneage/ — prior 2005 original pages in this repo were source qualified. This turn's one dated 2006-06-23 Wayback/availability attempt was inaccessible to the web reader; other targeted named searches did not retrieve an authenticated Wayi 2006 mission page, patch note or original build-linked script. **OPEN_EVIDENCE_LIMITED**, not a claim of global absence or HTTP404.
- Reopen on a source-custodied original operator notice/patch/manual or official-game resource explicitly linking this task. Secondary derived catalog: `research/recovered/STONEAGE-TW85-SUPPORT-FRONT-GUIDE-GATE-R1.json`.


### SRC-TW-WAYI-2005-MARINE-SOCIAL-CRAFTING-01
- First-party Taiwan operator URL: http://www.wayi.com.tw/stoneage/game/game01_03.asp ; genuine third detail href in already authenticated WORLDLINE-R1 parent. Requested parent capture 20050614002509 redirects to actual 20050614005817id_. HTTP200 body 26642B, Big5 strict, SHA256 f021c32b042dbbea480f67aeb3fbc50ba9dfab919de6c04b3240400e5b41c684. Source HTML remains transient, no image or binary acquired.
- Operator document describes planned 8.0 fusion for earlier6.0 marine pets (five classes/twenty pets, only four classes named), social-card capacity and distinct mission-card retention/overwrite/manual exchange, five crafting extensions. Source description is FACT as attribution, not deployment/runtime proof. Capture is not publication/build date. Fifth class, complete roster/recipe, server persistence and quantitative crafting parameters remain UNKNOWN.
- Permanent derivative: research/recovered/STONEAGE-WAYI-MARINE-SOCIAL-CRAFTING-R1.json ; specification and reproducible source classifier share that stem. Ordinary source fetch and exact JSON replay qualified locally; independent Actions must be reported at their actual SHA. No JSS1999/TW1.0 promotion, universal regional equivalence or copied source HTML/assets.


### SRC-JP-2003-HANGAME-174A-INSTALL-CHAIN-01 — 2026-10-18 static navigation supplement
- Exact already-registered setup page reacquired at https://web.archive.org/web/20031214055553id_/http://www.hangame.co.jp/publish/sa/sasetup.asp ;15583B, SHA25676d972f0aac242a03f6bd411a5fedf6f9184cd4e92cd45062cc60f37210c4a21, CP932 strict. Local qualification only; no independent runner replay of this new inspection.
- Nine literal image-button onclick location targets found without executing scripts; include http://www.hangame.co.jp/publish/sa/chara.asp . An anchor-only initial inspection missed them; zero parsed a-hrefs must not be mistaken for absence of site navigation. Target not yet read, no character/pet identity or pixels certified. Setup capture/page is not exact1.74a build evidence. Derived R5 coverage record retains all22 historical statuses and selects one bounded character-source task. Original HTML/images remain out of Git.


### SRC-JP-HANGAME-2003-CHARACTER-PAGE-01
- Original first-party operator page http://www.hangame.co.jp/publish/sa/chara.asp ; real static image-button target in previously qualified R5 parent setup source. Actual capture20031214051427id_,16437B, CP932 strict, SHA25636e1600d1a6192d2613b64750676235fe42010c78b1ca24b43bc38121c9f9e50. Operator explicitly leaves character naming to players; no fixed names given.
- Six-row/four-column DOM grid supports twelve paired web positions,12 illustration refs and12 companion refs; cell adjacency plus source filename ordinal are checked together. This is page attribution, not original client body/face IDs or a complete playable roster. Companion pixels not obtained; source filename com does not prove sprite/comment/color semantics.
- One original illustration URL http://images.hangame.co.jp/_images/game/saj/charapicillust1.gif actually resolves to20060619160353id_,6312B,SHA2569a3d42aca28d67a57d328d33fce57f22adfd0037f064885785c82f6482b1bb39,GIF65x75,one frame. Exact image visually reviewed: human face illustration/light-orange hair/top tuft/smile.2006 image is not same-instant2003 or exact-client proof. Other23 grid image references remain unacquired.
- Derivative STONEAGE-JP2003-CHARACTER-VISUAL-SOURCE-R1.json and corresponding specification retain twelve unnamed positional research records, temporal separation, explicit null game IDs and rights restrictions. Ten source/DOM negative cases and exact-body/GIF replay gate; actual independent Actions custody must be recorded after execution. No original HTML/pixels in Git. Actual pet-tab target chara2.asp is recorded but unread.


### SRC-JP-HANGAME-OFFICIAL-PET-PAGINATION-01 — 2026-10-19
- First-party original root http://www.hangame.co.jp/publish/sa/ ; chara2.asp is the previously authenticated character page's real pet tab. After one-page intake, a separate bounded adjacent package followed only the two actual pagination targets chara2-2.asp and chara2-3.asp, with a single image acquisition for the whole unit. No other tabs/forms/programs/site traversal.
- Actual source bodies, CP932 strict: chara2.asp capture20031214055443,36332B,SHA256a01a2c93d410511b9e08f7a066569d8cec8db883f50047baf0ca3160d50ed0fc; chara2-2.asp capture20031214051259,36343B,SHA25609faee5a55cb09ea8527090fb09fc00166abce94c83ef34322f4cacd4ad65249; chara2-3.asp capture20040220221717,34310B,SHA256b9284c6185fc5a999dd3bf0da3ac9d341e31312dcdf5859ee5a5786eb0cbc9ad. Three actual number/name/image DOM tables support45+45+34 entries, not a single contemporaneous2003 server census.
- Same-column first entry ウーリ references http://images.hangame.co.jp/_images/game/saj/petpicgroup1-1.gif . Sole actual image capture20060604065927,4460B,SHA256593345c3edf78ebcaa2dff0c27a2d10a92b4eefcc4aef4db14aee2efdc5e013f,GIF60x65,one frame, visually reviewed. Other123 image references remain unacquired. Later image bytes do not prove2003 appearance or client sprite identity.
- Durable derived report/spec STONEAGE-JP-OFFICIAL-PET-CATALOG-R1:124 research pet records preserve native labels and individual page/pixel epochs; game IDs, aliases, growth/skills/habitats remain null. Web46 maps to local image2-1 and web91 to image3-1; filenames are not IDs. No original HTML/assets or public-release rights. Source/JSON replay and artifact custody must be accepted at actual run/HEAD.


## 2026-10-19 — 日本官方宠物分页目录独立重取与永久派生保管验收

`STONEAGE-JP-OFFICIAL-PET-CATALOG-ACCEPTANCE-R1.json` 对应内容HEAD0630a7e、候选10绿/主线11绿，run39174344977/job117813809435，独立重取三份精确捕获正文与唯一GIF；10项反例通过，完整派生报告cmp一致。artifact12153219607实际下载ZIP SHA256为7ab3ae97e8f7f18c9e4d11a1b8a6279d497e5db44d320cf15d739b42c4d2f335，唯一derived.json的182129字节及raw SHA256 edf50ec2fe9915db1904992ee2871def9b719fa05e40619019229be21dca413f与永久Git blob85e99d6fd6a7ca27eeaa3987510a6bcc1d701708相同。三页年代2003/2003/2004、唯一图2006保持逐条边界；原始正文/图像不入Git，未取123图及原服数值不提升证明等级。凭据保留各run、attempt、job、source SHA和时效，后续文书提交须另看自身Actions。


## 2026-10-19 — 日本官方宠物具名原图12条有限取源

来源为已验124条目录中三页各四组的既有图像URL，限定网页号2/10/19/28、46/55/64/73、91/100/109/118，非猜名/全站抓取。每图原URL、请求/实际回放URL、实际捕获、SHA256、字节、尺寸、帧数和逐张目视存STONEAGE-JP-OFFICIAL-PET-VISUAL-SAMPLE-SOURCES-R1.json，派生每条自身有页面/图像双出处。12图均60×65单帧GIF，初次HTTP全部成功；实得2003×5、2006×4、2008×2、2016×1，不当图片创作/上线日期，尤其ノガロン图2016不推原游戏运营到2016。原件不入Git，父目录不可变。

34项首次本地回归1失败为漏entity_type，补字段后34项通过，失败留存；修正后独立Actions完整报告cmp和产物保管须按真实结果另记。连此前一图为13引用实得、111未取，不宣称游戏物种覆盖或客户端动画。R6复用22域原状态，下一份一正文来源候选town.asp来自R5安装页真实静态按钮；尚未访问该正文，不以文件名预设聚落内容。


## 2026-10-19 — 日本四具名村落2003正文与2006唯一建筑配图

Hangame town.asp真实导航：实际20031214052752id_正文14371B SHA2565627429482edaad6d24ac5270b53891c227ae394ab10d07f715a336d77c3175a，CP932严格解码，四行名字/描述和原图对应。首图town1-1.gif实际20060618193306id_，27303B SHA2565712fe0554f9daf067970ec102155fa594ee8e14c9e5333d74662180412bc560，GIF200×150单帧已目视；其余三图未取，不推建筑功能、原地图或同刻像素。原日本名字与地区写法保留，最大/整齐及相对方位/海滨/森林/小岛聚落均为源描述而非原服地图运行结果。派生/规格STONEAGE-JP-OFFICIAL-TOWN-SOURCE-R1，8项反例及独立一正文/一图源cmp须实际验收。下一真实按钮town2.asp仅资格待读，不跟随其它栏。

另永久宠物图验收STONEAGE-JP-OFFICIAL-PET-VISUAL-SAMPLE-ACCEPTANCE-R1.json留run39175372360/job117816820477/artifact12154550817、ZIP2f622044ae3a66353d5688f316f77af953558109e816876537205075722519a6、raw fce2492fc51abfae360d189eb6a86319bcabec482cb5f151c5a68250dbd8640e与blob069280bf3fa61be0e08e979672af6864f2b7c616；候选10绿/内容主线11绿，不混用为新村落包验收。


### 2026-10-19 — 日本四村原源独立验收永久回执

STONEAGE-JP-OFFICIAL-TOWN-ACCEPTANCE-R1.json对应内容15c8d55be9985b40cbe4e10f2ef73915e86f1229、10分支/11主线绿，source run39175778360/job117818017266；artifact12154526602实下载ZIP2537B SHA2568825ce689496935e6314d0e680a349882ce824fd7df1ecc40d8788d4b4ff0af3，唯一derived.json10828B SHA256127d7c72de68b4a27b54d088dab74a44bb4189302c87ceaa946a72452ccd97ff与永久blob0945b5c89750cbeb6348252805583cfd9a69d194相同。2003正文/2006唯一图边界、八反例、完整派生cmp实际通过；三图未取、建筑功能/原地图/跨地区别名仍OPEN。文书回执自身检查另验，不更改既有原源/报告。


## 2026-10-19 — Hangame村设施正文：13条服务及首图HTTP404缺口

原URL http://www.hangame.co.jp/publish/sa/town2.asp，实际20031215095512id_，21792B SHA256f719ff0167c32e531f3128e47b31175df6bfc641a6a83728d2fd4370a9ae58b3，CP932严格解码，13行设施名/描述/图引用同列实证。宠物店买入禁止、医院HP但目标未知、村落库存差异、问答等级/入场费、贡献设家点、配送远近薪酬、普通步速/无怪/付费自动巴士、抽奖奖品种类等为一方文字限定，非服务端运行；原ID/阈值/价表/坐标/事务保持UNKNOWN。原名トーテンポール不静默改写，全部设施不推每村都有。

首图 http://images.hangame.co.jp/_images/game/saj/town2-1.gif 两次HTTP404，后续本地独立探测仍404；无像素/目视，不提升旧石头建筑功能，另12图未试。首图无HTML声明尺寸，其余仅声明200×150，全13实得尺寸/时刻/哈希/帧数null；404不是历史不存在证据。永久元数据/规格STONEAGE-JP-OFFICIAL-VILLAGE-FACILITIES-R1；11负例及34本地相关回归通过。独立源Actions、ZIP/raw/Git及自身main结果另据实留存。R7复用22域后轮换到华义原介绍页已验game01_04.asp一正文，先核内容，不爬站、不取原程序。


## 2026-10-19 — 台湾华义8.0正文标签：剧场/魔法牌/宠物转轮三循环

原介绍页真实第四链接game01_04.asp实得20050614011214id_、21308B SHA256afaae72abf0ca60939c7e57a824cc556f0e24a2d8add77eff7f18caacb942a50，Big5严格。剧场藝術值→特殊道具；魔法牌挑战未具名魔王→積分→特殊道具/宠物；宠物转轮买票下注→按描述赔率给对应積分→特殊道具/宠物。三段长度/摘要独立保留，不推同钱包/倍率/费用/概率/原ID或实际运营；站题旧名称与正文8.0标签各存，不推同客户端。演出童话例子不是世界正史，泛称反派不合并旧世界线人物。表单/投票/页脚排除，原件和图片不入Git。派生/规格STONEAGE-WAYI-THEATRE-ARCADES-R1，9负例及相关35本地通过，独立源/产物/main另实际验收。

另日本设施永久回执STONEAGE-JP-OFFICIAL-VILLAGE-FACILITIES-ACCEPTANCE-R1.json对8cd9dc8b的候选10/主线11绿、run39177475418/job117823024354/artifact12154124007 ZIP5059ff8d9befbddf87dde785ae000c57e9d80d12d74d0b4a73654e1e7bfb2d01及raw65ed727327aae1e8b060834c11c33d56685134a6bbd8fb02e250086baf4f5dfb/blob6696402b32f9767f724b7543bb4f477a67dbea6e保管链；首图404不证历史不存在，不混为华义本包验收。


### 2026-10-19 — 华义三场所/积分循环永久独立验收凭据

STONEAGE-WAYI-THEATRE-ARCADES-ACCEPTANCE-R1.json对内容bce32d65afc4b3e3c5a31b263e9da4efc1861770的10候选/11主线success，源run39177816800/job117824021633重取唯一正文及完整派生cmp、9负例通过。artifact12154129532实下载ZIP2242B SHA2562722e0a81c35d63194b66c20514164ce077239e6944e97022f25981364b7622e，唯一derived.json7173B SHA256f76d9008a425cc335706510303ceff96be72c1aeba9ee42a1d7b06c87a248669匹配永久blob a428b3b910e5876f0db5b2abb1977a4164fed017。三段来源及积分/奖励/泛称反派/童话宣传的边界、无原图/程序、无实际原服交易均不提升。该文书提交的自身检查另验；日本设施首图404与其独立回执保留。


## 2026-10-19 — 已知JSS2001手册九节新增行为合同，不增网页数

manual02.html实际20010418083149，28434B SHA25650b9771ec501067136629c8e083a190e979e53dd9ba141903f78b76d43b602cc，Shift-JIS严格；本轮重取字节完全等于已验原件。旧通用JSS-LOGIN-MANUAL-CREATION-CONTRACT已给3070/7010/8030指纹但manual02 creation_contract为null，不将其抹去或声称首次发现。九节3060/3070/7000/7010/7020/8030/8040/8110/8120增量是物品/邮件/社交和共用场所的逐条语义与未知。原有12节宠物及6节服务等既有内容不重计。

核心来源限定：普通邮件/宠物邮件的战斗限制相反；返还与登出、数小时宽限、流浪另时长消失分开；名片交换开关复位非删联系人；斗技免票等级≤9或排名77/777，不把条件合取；医院恢复免费仅斗技场语境。聊天室免费及与斗技相连的票警告不混为所有人付费；票即时消失不推原物品ID或登录恢复票。9记录7tutorials/2maps，派生与规格STONEAGE-JSS2001-MAIL-ITEMS-SHARED-VENUES-R1，原文/图像/程序不入Git。12负例及相关31本地通过，独立源cmp/ZIP/raw/Git和main另据实验收；R8保留22域状态，下一仅基于既有报告做跨年代不可混用关系。


### 2026-10-19 — 九节来源独立验收与八组五报告衔接

STONEAGE-JSS2001-MAIL-ITEMS-SHARED-VENUES-ACCEPTANCE-R1.json对应内容d75d2d7a的11候选/12自身主线success，专用run39199275338/job117888674327；artifact12163560641 ZIP3769B SHA25672eda1af8e1b3042c7de71e230577620bb3495f4cafb2b5e07fdb854c9799b7e，raw16556B SHA2567a586ce0f16a3922c62f711554e9c158e659d143ad158b4cbea184936ac74122匹配永久blob a7c6400aa431bb136e726fd17f1e90df282a10d0。旧JSS通用指纹/原件复用均保留，不当新网页。

相邻STONEAGE-EARLY-SOURCE-MAIL-VENUE-CROSSWALK-R1只派生自新九节、旧2001普通落地、Hangame2003设施、Wayi2005剧场/游乐场及名片五报告，指向四原正文、零新增原URL。8比较各保留输入SHA/JSON指针与原件出处，不增8新原件或游戏实体；省略不证历史改版，计时/票据/场所/费用/同名字分值不自动合并。6负例及相关37本地通过，独立离线报告cmp、ZIP/raw/Git及main另验。新NEXT为同手册3040/8020/8060三节参数/升级/气绝的有限早期合同，不重开存档IO或新游戏。


### 2026-10-19 — 五派生报告八组边界的永久离线保管链

STONEAGE-EARLY-SOURCE-MAIL-VENUE-CROSSWALK-ACCEPTANCE-R1.json对应内容10aa0338的11候选/12自身主线success，专用run39199676876/job117889858707离线五输入/6负例/完整cmp，零新增原源。artifact12163088605实下载ZIP3223B SHA256bdb482c789a3bc0275dc0ad0fdac9cfa29de6063a53271998091a60618fc0122，raw18972B SHA25606138c79d6b5c7b6586b25a88b35f0da7bee192d3745128884f34bf5f1e36e0a匹配永久blob e5cb3b70dd852b7e9161098e040862ca8e4cc1f0。输入来源4个不同原正文不等于4个独立证人；原手册独立下载/字节/语义由先前九节主回执单独证明。未知时间/费用/原ID/实体同一性和运行均不提升；本回执自身CI另验。


### JSS2001已知manual02参数/升级/气绝语义 — 2026-10-19

http://www.titan.co.jp/stoneage/manual02.html，严格重放https://web.archive.org/web/20010418083149id_/http://www.titan.co.jp/stoneage/manual02.html；28434B SHA25650b9771ec501067136629c8e083a190e979e53dd9ba141903f78b76d43b602cc、Shift-JIS。只3040/8020/8060，旧通用目录全部三摘要保留；新增3tutorials记录和19状态表同列绑定，非首次原件/原服字段。局部语义/未知数值见STONEAGE-JSS2001-PLAYER-STATUS-LEVELUP-KNOCKOUT-R1.json及规格；无新出链/图片/程序/原文入Git。本地重取完整cmp通过，独立Actions/ZIP/raw/Git和main必须实际另验，不能借父HEAD绿。


### JSS2001角色原件保管及七组离线衔接 — 2026-10-19

角色内容6b036e05fe87a87a9ac44555726c68e392a6a8ac、源run39200493982/job117892275375，artifact12163272862 ZIP3813B SHA2566e119388e2f1254c49f07fd040756191d3f654ff697ba3544f2c14ced969275a，唯一derived.json11302B SHA25613df1d32a44127f80c3e042c335dc01d9cf926011f5b7908b1b71be77d818277、Git blob4b44c6d022265c62cf2cca1d599deb85e31e1418实际下载比较；11分支/12main均success，见永久ACCEPTANCE-R1回执。

新STONEAGE-JSS2001-PLAYER-PET-CREATION-BOUNDARIES-R1只四份固定报告，原manual01/manual02两正文同运营商而非独立证人；7个sources比较保留输入SHA/JSON指针/原URL捕获摘要，零网络新原源/资产。39相关本地测试通过，专用离线Actions/ZIP/raw/Git/main实际另验；不借父HEAD12绿，原文不入Git。


### 日本Hangame2003世界観分栏 — 2026-10-19

原http://www.hangame.co.jp/publish/sa/game.asp，R5setup真实静态入口。网页阅读器UNAVAILABLE不证历史不存在；直接HTTP初请20031214055553跳实际20031214053427id_，12869B SHA256c3cb0c64811dfd2d83e5ab809119ddcf09b5ce5b709d1e3c8de1e58c3ec91bfb、CP932严格。第二次严格https://web.archive.org/web/20031214053427id_/http://www.hangame.co.jp/publish/sa/game.asp本地全量cmp通过。实际标题ストーンエイジ/分栏世界観，四可见段/5sources记录，非新增具名地图/NPC/物种。学校/石币/100种下界/图鉴与轻松定位的具体未知见永久派生/规格STONEAGE-JP2003-WORLD-PREMISE-R1；原HTML/图像/程序不入Git。独立runner/ZIP/raw/Git/自身main实际另验。真实game2.asp标签ゲームの特徴仅资格，不等于已读正文。


### 日本世界定位正文独立原件与ZIP/raw/Git保管链 — 2026-10-19

内容f04e25581e54cc8e14c35fe6fa9887539f30bb54 / tree8546aba9f05cf365f39c179b431de03ed92491f7的11候选/12自身main检查实际全success，源run39201218785/job117894396161重取精确20031214053427正文并完成7反例/完整报告cmp。artifact12164420061下载ZIP2516B SHA2568d2aaa6d85b73dbc421ce22cf4c8f7442edad4807ff21c44f38ee60999fd5e5f；唯一derived.json9192B SHA2569879a886d17bb5658349085ccf5768f952ab2daf0aed7299a7f66bfd06915313匹配永久blob7d591df2db42ed3fe2a8cd61e224475fa123990c。详见STONEAGE-JP2003-WORLD-PREMISE-ACCEPTANCE-R1.json；原正文SHA、初次阅读器不可用/捕获跳转均保留，未获取任何截图/图像/程序。回执自身新HEAD门另观测。


### 日本Hangame2003游戏特点一正文 — 2026-10-19

真实入口为已验game.asp标签ゲームの特徴，原http://www.hangame.co.jp/publish/sa/game2.asp；初请20031214053427跳实际20031214050618，精确https://web.archive.org/web/20031214050618id_/http://www.hangame.co.jp/publish/sa/game2.asp，17136B SHA2564e92ce95cfb836db9fd78f7b4f64905e60270202d1e2ea0b00cf56b79b6440b0、CP932严格。五可见行5tutorials，引用五tokuchopic图片但全无像素；本地第二次完整cmp及18相关测试通过，独立源门/ZIP/raw/Git/main必须另实际验收。规格/报告STONEAGE-JP2003-GAME-FEATURES-R1保留12×4/5人等数值语境和未知，原HTML/图片/程序不入Git。


### 日本特点原源验收及离线人物参照保管边界 — 2026-10-19

特点内容49a9c5b1b72f79db77eac127b7bf3d14e6311546 / treea7473ab136b0b16bac602533a3cde42533433263，10候选/11自身main门实际全success；源run39201977369/job117896674711、artifact12164037843 ZIP2829B SHA25617096253aaea65117089cdfa661bed78804e77d8ff4090ab6f266ac0fa262f00；唯一derived.json10890B SHA256f74bb9f07cdf02ca7ddb2f2e9bbeac2cd7f90b3ecb977343608e0dde626a6743等于永久blob84355aad2d4c081459c783b86faa4e1814ab1703，已实际下载比较，见特点ACCEPTANCE-R1。

新STONEAGE-JP2003-CREATION-VISUAL-REFERENCE-JOIN-R1只三派生输入，三原正文/一既验2006图元数据，5sources比较与12既有位置索引，零新原件/资产；每条SHA/JSON指针/原URL/捕获可查。独立离线门/ZIP/raw/Git/main实际另验，不借前一HEAD绿，不把引用说成原图重取。


### 日本官方截图一索引/一GIF实际时刻保管 — 2026-10-19

原http://www.hangame.co.jp/publish/sa/game3.asp，真实入边见已验game2.asp原SHA4e92ce95cfb836db9fd78f7b4f64905e60270202d1e2ea0b00cf56b79b6440b0及本次静态标签检查（旧派生报告未单列此入边，不假称已有JSON指针）。实际20031215093733id_，14113B SHA256e2f08e8cb7d5f9469acd158783d343349f31ef1fb4b46a493d00e5441df63a18、CP932。仅引用首http://images.hangame.co.jp/_images/game/saj/screeshot1.gif实取跳20080819022212id_，46583B SHA2560565913532b59e930958bbb04bb347a349e6667e02304426a6aa2197f48340b6、GIF275×200单帧并逐张（仅1）目视。另7引用未试；2008图非2003同刻像素/原生分辨率/精确客户端build。原页与GIF不入Git，永久报告/规格STONEAGE-JP-OFFICIAL-SCREENSHOT-REFERENCE-R1与R10复审记录只保留派生元数据。独立一页一图/全cmp、ZIP/raw/Git及自身main按实际另验，不借前包绿。


### 唯一官方截图界面参照的永久验收保管 — 2026-10-19

内容548f2a12eada40563bd34c7981d0ac40cee515bd / treeb571ac2028ca3b8dbbad0f9a7cd9fae9c624a1e3的10候选/11自身main检查实全success，源run39202736450/job117898974380重取2003索引与2008唯一GIF、8反例/元数据/全派生cmp。artifact12164308218实下载ZIP2255B SHA2562957f6aa7a151e840af930e1bad80a92625e3498824f9baeaabfea16c72bdad3，唯一derived.json11565B SHA256d5ce1b2589a91ddf7ef35abb7b91251adad01ef4b0d993f1cb9460e94730b858匹配永久Git blobb87cdf16b7f0ed4ab7aba78bace83e36136879f1。回执STONEAGE-JP-OFFICIAL-SCREENSHOT-REFERENCE-ACCEPTANCE-R1.json留每原件时刻/SHA与人工目视哈希，不将独立元数据cmp当自动目视或另7图已取，原HTML/GIF不入Git。回执自身新HEAD另验，不套用父门。


### 华义制作人《新手騎寵計劃》两原件 — 2026-10-19

真实主页入口producer/producer01.asp，精确20050612011406、28883B SHA25619661e2acca046bf8c6dc86dc968107fe9935cd58a8f3cd8ce5e1de5aeba7f8b；15标题/日期/链接同行。idno66《新手騎寵計劃》标2003-12-10，精确正文https://web.archive.org/web/20051117143741id_/http://www.wayi.com.tw/stoneage/producer/producer02.asp?idno=66，19964B SHA256b1f2163b80137e2140c36a6675a42e4ac1f2e3cc367e08b2a850cd15a6261790，Big5严格。计划/动机与实际原服奖励分开，5tutorials，无新实体ID/像素/程序。R11元数据保留已知主页重取、五周年错题预取纠正及image/Flash不可读规则、newsid2834单次404；失败无源SHA，不从新闻搜索填奖励。独立runner只重放成功索引与具名文章，不称重演初次本地失败。报告/规格STONEAGE-WAYI2003-NEWBIE-RIDING-PLAN-R1，本地两原件全cmp/8反例通过，ZIP/raw/Git及自身main按实际另验；原件不入Git。


### 华义《新手騎寵計劃（續）》实际一原正文 — 2026-10-19

真实既验索引idno67/2003-12-23，原http://www.wayi.com.tw/stoneage/producer/producer02.asp?idno=67，严格https://web.archive.org/web/20051113145307id_/http://www.wayi.com.tw/stoneage/producer/producer02.asp?idno=67，19686B SHA256caf0ab5a51a87d0ddd6f3f6aea4be77cde4dbaed80b1c6e900f4946da703bea2、Big5。索引复用精确20050612011406；前篇派生SHA b23c0220c58840ddb14ee9eea835687924cc16b42afe091af127f67472580fcd只Git输入，不称重取前篇原文。三记录保存叙事/矿石工角色地理/轶谈边界，两个JPG引用未取。16相关本地测试和两原件第二次完整cmp通过，独立runner/ZIP/raw/Git/main实际另验；原文/图像不入Git。

前篇内容ba781f0c9d9e69ad821e5599dcba853b65d45373、10候选/11自身main实全success；run39203934337/job117902568662、artifact12165057158 ZIP2723B SHA2562087881b57417c81ef64ade218a6a3e61979f3e2274c5ba80c30bec0c92ca36d、唯一derived.json11911B SHA256b23c0220c58840ddb14ee9eea835687924cc16b42afe091af127f67472580fcd、永久blobfb75c57e33a745f41634ef9ea36dfce8da2dfb4d实下载比较，详见骑宠计划ACCEPTANCE-R1，不借此绿灯验续篇。


### 骑宠续篇一方矿石线索的独立验收保管 — 2026-10-19

内容9b00dcfa0fe42cbb36ed5b2d430fd11b1df95a38 / treee6d84148602c6ede03f8b9ef283dc847a5c1c096，10候选/11自身main门实全success；run39204398649/job117903968931重取精确索引/续篇并校验前篇固定Git输入、8负例/全cmp。artifact12164888684实下载ZIP2423B SHA2565fea4df0390e30213aa24eba3cfecfa9b875c22ab5b04fd38fc6f46388d9c362；唯一derived.json7384B SHA256d2c18a33dd56c5aa5ba886ec591b619b3e6b32fcb67385db1e09db8b900b9125匹配永久bloba2e5d0c927d1c53756146ba583532e2c0ab09ec4，详见STONEAGE-WAYI2003-RIDING-SUCCESSOR-ORE-WORK-ACCEPTANCE-R1.json。原件/图像无入Git，不把作者续篇当独立原服验证，赠虎实施/矿工奖励/NPC IDs未知。收尾回执提交自身门另观测。


### 台湾华义职业调整计划一正文 — 2026-10-19

既验官方producer01.asp真实同表行idno64《全民就職計劃》/2003-11-14；已知索引实20050612011406、28883B SHA25619661e2acca046bf8c6dc86dc968107fe9935cd58a8f3cd8ce5e1de5aeba7f8b重取相同，不算新发现。原http://www.wayi.com.tw/stoneage/producer/producer02.asp?idno=64；网页阅读器不可用不证缺源，直接HTTP初请20050612011406跳实20041206141244id_，17678B SHA256cd725562731d4e74f9b90bbefe9c167d499b73511d9fee2d94186ec0b2d2d8a9，Big5严格；本地第二次精确两原件重取全cmp通过。五段指纹、3教程/2来源语境及两未取sa921113001s/b.jpg引用见STONEAGE-WAYI2003-PROFESSION-ACCESS-PLAN-R1；2003索引日期/2004正文/2005索引分开，职业计划非原服实现，原HTML/图像/程序不入Git。10新负例和独立一索引/一正文工作流已交付；实际Actions/ZIP/raw/Git/main须另验，不预称成功。


### 华义职业计划独立保管及大陆2.0经验表一原件 — 2026-10-19

职业内容f5ab2574 / tree53ebeb1f8ce7b5f01101ec8e850f50bd5fa82e0d的10分支/11自身main实全绿；源run39232408651/job117993271245、artifact12178061508实下载ZIP2808B SHA25634ba84683df2fc2d72734c722186634047dbb0e40f7c36c71e2c722ddbf41ce6，唯一derived.json10859B SHA256e435ca9f68d1b4d13162634d8de1b664827864b40b5937ee74448464950c3075等于永久blobf69093d0e14e0e977fe0b0aa75a3c24016ee953c。完整链见STONEAGE-WAYI2003-PROFESSION-ACCESS-PLAN-ACCEPTANCE-R1.json，计划非实施。

R13显式轮换北京华义原http://www.waei.com.cn:80/ZHUANQU/stoneage2/tyro/upgrade.asp，实20011204165711id_、75141B SHA25673fde66ffb3c92261d66715f873fa9b9f54166e4443d5d29924fe137cdcb8d35、GB18030严格，实际标题石器时代2.0。已知原件重取非新源，首次完整结构化82表格数字对、两空对、原行/列组及grid SHA25672d9161343f1ec017fa6aedead769bdc28cc004215e7ae9d0ebe5bc2300caa45见STONEAGE-WAEI-CN20-LEVEL-EXP-TABLE-R1；本地第二次精确重取全cmp通过，9负例和独立只一正文门交付，实际Actions/ZIP/raw/Git/main另验。增量/累计等含义不补、82不认cap，不误作2.5安装器；原HTML/图像/程序不入Git。真实侧栏新入石器→sw/adventure.asp仅合格未读入口，不算已取正文。


### 大陆2.0可见经验表永久派生保管链 — 2026-10-19

内容1813fa6560e9b2d30f1afbd202a44036e2c4ffdc / tree3c50cd316109adf55f2852c28d3f179f9884a5a1的10分支/11自身main门实际success；源run39233233573/job117996018294精确已知20011204165711一正文重取、9负例/原grid/全报告cmp。artifact12177087803 ZIP2895B SHA256acef6fb127fd6bd8328c5b2e4c5c6a8b941c6bf18cc6af97ce3e273d328a2bd0，唯一derived.json18121B SHA256e012249c799f9789e65f13c5fbb6e0ac746966d7660bb30b68bec9a0150d3b87等于永久blobeb30355ade1e87dc734eca3b5b8ddde575dd2c3e，已实际下载/逐字节比较。完整链见STONEAGE-WAEI-CN20-LEVEL-EXP-TABLE-ACCEPTANCE-R1.json；82观察对/两空对不提升cap/原服经验公式，正文非新源、原HTML不入Git，下一页尚未读。回执自身HEAD门另观测。


### 大陆华义新入石器官方托管无署名指南 — 2026-10-19

既验经验表派生SHA256e012249c799f9789e65f13c5fbb6e0ac746966d7660bb30b68bec9a0150d3b87的/qualified_unread_entry真实新入石器→http://www.waei.com.cn:80/ZHUANQU/stoneage2/sw/adventure.asp。网页阅读器不可用不证缺源，直接HTTP初请20011204165711跳实https://web.archive.org/web/20011204212409id_/http://www.waei.com.cn/ZHUANQU/stoneage2/sw/adventure.asp，65653B SHA256ef63a7b33db0a967823af8356bbd2369487b20781a3272e1e2c3b0d1500ec1ab，GB18030严格/题石器时代2.0。官方站托管无署名攻略非运营商作者/原服独立证人。第二次精确重取全cmp通过；新工作流只一正文+固定入口Git输入，不再次取经验原页，不重演首次跳转/阅读器错误。11段指纹、10教程记录、原相对img/adventure/1.gif及1s.gif未取引用见STONEAGE-WAEI-CN20-NEWCOMER-GUIDE-R1；13负例/22相关本地通过，源job/ZIP/raw/Git/main必须实际另验。原HTML/图像/程序不入Git，正文数字/建议不回填早期原服，失败和错字保留。


### 新手正文独立保管与四固定派生离线关系 — 2026-10-19

新手内容1ff1730584de4822102680f19747c6c02ace93cf / treeb421c7b3e63bf6032cb31d1778f6d626b944a06c，10分支/11自身main实全success；源run39235072328/job118002056097、artifact12176994685 ZIP4165B SHA2562d51fe38b5e5657e7487b797539bb473d008eb4d1be4134b6ea82012028dfb04；唯一derived.json19519B SHA256aecc1e18d291d6af8e7fd6e4ca913baf9aedb6e883cabad295f47a842705bed6等于永久blobc85fb48a8263a2d62194fd786da31034e20cd6ae，实下载比较，详新手ACCEPTANCE-R1。官方托管无署名不证运营商原创，初次捕获/端口跳转和阅读器不可用不抹。

新STONEAGE-EARLY-NEWCOMER-PET-CARE-BOUNDARIES-R1只新手/初建/宠物/角色4固定Git报告，3实际原正文，JSSmanual02重复不是独立见证；每条SHA/JSON指针/原URL捕获摘要可追。8sources关系零新原件/图像/程序，明确CN宠物升级与JSS主人升级、20初建/每级、魅力/忠诚/初捕界限/KO时序，原数值不跨版补齐。8新负例、30相关本地通过，离线全cmp/ZIP/raw/Git/main按实际另验。


### 初宠/初建八关系离线原源归属与永久保管 — 2026-10-19

内容2e45613b5683f8485872150de2cec6a71d7f25e7 / tree00594e5884d57ceec5224464b545d3d67df1b9b7的10分支/11自身main实全success。专用run39235760241/job118004305379只4固定Git输入/8反例/全部指针/全cmp；artifact12178752003实下载ZIP2919B SHA2566cb077392b4d9d10c685c1f6b4bd0465f662e982fb42f328e473d63910f09a36，唯一derived.json18670B SHA2563606d42db083bcec622dab8e22a9b3d0c65b7a542825573b2f3082562f20b75f等于永久blob7ef39c9106d26c4082cf39ac6e26d2e86fd7aff7，实逐字节相同。完整回执STONEAGE-EARLY-NEWCOMER-PET-CARE-BOUNDARIES-ACCEPTANCE-R1.json留精确run/HEAD/输入pin与ZIP/raw/Git；3原正文未重新下载，manual02两报告仍同源，8关系非8游戏实体/原服规则。原件不入Git，回执自身HEAD检查另观测。


### 华义大陆新增宠物首目录一新正文 — 2026-10-19

已验新手原正文20011204212409/SHAef63a7b33db0a967823af8356bbd2369487b20781a3272e1e2c3b0d1500ec1ab真实新增宠物href /ZHUANQU/stoneage2/pet/new_pet.asp逐格资格；旧报告未列此出链。网页阅读器不可用不证缺源，初请20011204212409跳实https://web.archive.org/web/20011204194619id_/http://www.waei.com.cn/ZHUANQU/stoneage2/pet/new_pet.asp，69317B SHA256561950fd7bba41e7d39f4a781a671e11e175c7fe08dd1b5481fdf1fd23ba351b，GB18030严格/实际题石器时代2.0。两原件精确本地第二重取全cmp通过；40网页格34名/6占位/40未取图及原grid SHA25699b6274ac6ed8b03755fa940c1172371ea6a037f1c40a0cba63f4410e9fbfa67见STONEAGE-WAEI-CN20-NEW-PET-CATALOG-FIRST-PAGE-R1。10负例/23相关本地通过，独立已知入口+唯一新正文/源job/ZIP/raw/Git及main必须实际另验。两分页未读、源图像/HTML/程序不入Git，不认104原物种/构建/属性。


### 首目录独立保管及阿米朵唯一像素 — 2026-10-19

目录ccd7bbc96f0036329185f9237ff5fae4fc7f31c7 / treec044ca66c5a866bca94044c2845e339303c76f62的10分支/11自身main实际全success；源run39237415071/job118009739669、artifact12179238341 ZIP3726B SHA256db257dc75124afdbcd94a7d828617284bf050df17c3370b06670fec2aaad49b3，唯一derived.json67802B SHA2569a460c23968a714717b375d823308bb5e56848116aaf44880091b75808024df6等于永久blob7c729ee760306af69cb4e0f3a73f5edd6a26c921，已实下载/逐字节比较，详首目录ACCEPTANCE-R1。

仅/records/6真实名阿米朵→http://www.waei.com.cn/ZHUANQU/stoneage2/pet/img/newpet/7.JPG，初请20011204194619跳实20011205051046id_，4831B SHA2567077cef8cfc23d67b34e3ed54ef6c57eca4c1197b44a2c513c4e43dfa1f85b30、JPEG83×90/RGB1帧，精确view_image目视；第二次精确取图/全派生cmp通过，Pillow12.3.0。永久目录Git pin验证名字/位置，独立新job不再次取HTML、不重演人工目视。STONEAGE-WAEI-CN20-AMIDUO-VISUAL-REFERENCE-R1留原图SHA/机器元数据/人工哈希与未知；8新反例/31相关通过，实际源job/ZIP/raw/Git/main另验。原JPEG/HTML/程序不入Git，39首目录图和两分页仍未取，旧报告不回写。


### 阿米朵唯一原图精确主线验收与永久元数据 — 2026-10-19

内容ac66558525e9c81de55abf54ba44c1b63f210af1 / tree20a31ef5274f4c8f7d8de7f67e45eec31a829af3的10分支/11自身main实全success。源run39238029870/job118011774555精确唯一20011205051046图、固定Git目录pin/8负例/实际元数据/全cmp；artifact12180360467实下载ZIP1934B SHA256db3fe4e335df1bd96f19ae7604597e4e0caa0c37043fc813ff920d21b33c2759，唯一derived.json4086B SHA2565ef2cfc5cd7f24229ece5f0fa01c924e932b40716af32417aa0bf4358eeb9cb0等于永久blob1f5a405f5d0dfc4ea72949b4fefb54b91260fe93，实逐字节相同。完整链STONEAGE-WAEI-CN20-AMIDUO-VISUAL-REFERENCE-ACCEPTANCE-R1.json留实际run/HEAD、图原SHA/83×90JPEG元数据/人工哈希与ZIP/raw/Git；不当runner重看图或网页图证明客户端模型/动画。39其它图及两分页未读、旧原报告不改、原件不入Git。文书回执自身HEAD检查另观测。


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


## 2026-10-20 — R21 日本DigiPark「影の支配者」前三章

- S1：https://www.4gamer.net/games/013/G001377/20080922005/ ，刊发2008/09/22 12:24；仅编辑引言后明确标识的发布文作为运营归因范围。
- S2：https://www.4gamer.net/games/013/G001377/20081028007/ ，刊发2008/10/28 12:03，页面明确配信元DigiPark/原样刊登厂商发布文。
- S3：https://www.4gamer.net/games/013/G001377/20081125066/ ，刊发2008/11/25 21:14，同类署名。

三页现行HTTP200实取，完整字节大小/UTC时间/SHA256与归一化核心SHA分别存 `research/recovered/STONEAGE-JP2008-SHADOW-CHAPTERS-SOURCE-R1.json`，原HTML不入Git。媒体托管运营商文稿不等于官方原主机或2008原始快照；官方出链读取失败，历史源SHA仍null。S3重复S2官方URL不更正。CI仅上传派生重放报告，原服执行、同构建NPC/对白/道具ID未证；三章共源，不当独立实服三证。中文规格和R21评审保留有限停止条件，NEXT R22。


R21派生保管补记：源run39336345338/job118346678887与artifact12225748930已实际校验；唯一派生replay.json永久归档于 `research/recovered/STONEAGE-JP2008-SHADOW-CI-REPLAY-R1.json`，ZIP/raw/Git和候选10/main11清单见 `STONEAGE-JP2008-SHADOW-CUSTODY-R1.json`。无原HTML入Git；当前HTTP字节摘要不认证2008历史原件。NEXT R22。


## 2026-10-20 — R22朱雀、神兽封印与2.5故事比较

S1：https://games.sina.com.cn/newgames/2003/12/121610098.shtml ，2003-12-16 14:38，正文明确华义官方消息归因；当前HTTP200/35322B。S2：https://www.ourgame.com/news/db/32/31192.html ，2002-2-5，当前HTTP200/5962B；设计/发行公司标签不等于作者归因。S1两实际图链I1/I2分别400×261和400×299 JPEG，均目视；HTTP升级HTTPS只为传输，不改资源路径。四输入URL、原图注、当前HTTP字节/UTC/SHA与两叙事核心SHA见 `research/recovered/STONEAGE-CN70-SUZAKU-MYTH-VISUAL-SOURCE-R1.json`。历史2002/2003原HTML/图片快照身份仍未认证，原HTML/图像不入Git；没有购买/竞价或原服操作。17173 2.5 raw567与故事超时、Sina12/22后续解码失败保留，不当独立见证。派生保管和自身Actions须另验，NEXT R23。


R22后续补证：Wayback20031225115132的Sina S1原页面回放已实取15189B/SHA25645d4106f945dbf3564bed9ddcab85f2447911291a31dc97406a11c6197eb6c33；归因/刊发/核心和两图链与现页相同，查询和resolved URL见2003-SNAPSHOT报告。旧历史null记录保持取源当时事实，补证仅S1 HTML，不认证原图或华义原服。旧四输入run39338196277的artifact12228020901已实下载并永久保存派生回放/保管收据；新固定历史URL的CI须独立验收。

R22同期补证独立验收：run39338706949/job118354613187、artifact12227931635已实下载ZIP/raw并完整比对；历史HTML+现行两文两图的3524B派生回放已永久归档，详见HISTORICAL-CI-REPLAY与CUSTODY后续段。此前四输入CI及历史未取注记保留为当时checkpoint；原服/历史图片不升级。


### CN2003-CHRISTMAS-NPC-SOURCE-R1 — 华义归因兑奖员公告（2026-10-20）

- S1：https://games.sina.com.cn/newgames/2003/12/122310574.shtml，2003-12-23 15:28，正文明确“来自华义的最新官方消息”，HTTP200/34999B SHA256f4efe819094146604444f4c09d3bd7b1174a4387140a0a265092177f97f84488。
- H1：Wayback20040218034443id_/http://games.sina.com.cn:80/newgames/2003/12/122310574.shtml，实际HTTP200/14942B SHA2568f6337879ad23a9db4fa484f361a44c2a938bdcf3805c5b7dbb7fa0d4c92899e；一次availability查询所得。相同487UTF8字节活动核心SHA256dcef51dd7aa44b4c7030b28ac0b0b3489c08852b2cc1fef09feff9bf523c31a2；同稿非独立证人，非运营原主机或服务器。
- I1：两正文真实img src，https://image2.sina.com.cn/gm/newgames/2003/12/U163P115T9D10574F167DT20031223152817.JPG，仅HTTP传输升级，31703B JPEG450×337 SHA256abde5fd6bfd802578077e4ca3e48a3698fbd954a5332a905887c7767c4e7ae73；已目视树/人物/底部兑奖员标签，未证原sprite、地图、历史图片字节及素材授权。

用途：分版本NPC/兑换前置及一次性限制来源规格。四研究记录满足既有七字段/19集合，原服IDs及物品清单null。原HTML/图片不入Git；工具CI仅输出派生JSON，ZIP/raw/Git保管按后续实际验。缺源重开条件及精确状态见STONEAGE-CN2003-CHRISTMAS-NPC-SOURCE-R1.json与中文规格；Stage A/B/百科门不变。


### PIRATE-RELIC-GUIDE-SOURCE-R1 — 同期指南与历史HTML（2026-10-20）

S1 https://games.sina.com.cn/zhqu/sta/sa6/rw/hzw.shtml，2003-05-21 22:27，现HTTP200/49799B SHA256b4d9f36815b7f099d0f6d0f7915e35ceab2edd8e6ead0658e5649c58ebb031bd；现投稿入口与专题授权，保守门户玩家指南，不认证运营作者或sa6版本。H1 https://web.archive.org/web/20031204053709id_/http://games.sina.com.cn:80/zhqu/sta/sa6/rw/hzw.shtml，HTTP200/29939B SHA2560dbcc96ef5b7a524bd3a228e6f743180195149cf5c9b082306b5790ef9c9a1e8。一次availability后实回放，旧作者栏授权、无当前投稿入口；两者相同1722B核心SHA256ad44dbe63160f4407511d9d1c40855226ad3226c834528ef0520dfbfd31c930a，同稿非独立运行双证。八记录/五段交接，保留素材、报酬二选一和随机收宠警告；12图未取。HTML/资产不入Git，工具只输出派生JSON，独立CI/ZIP/raw/Git保管按实际另验。未取GNN21168两接口403仅为发现失败，不作伊布原文证据。


### JP2007-SEKIEI-WORLD-EVENT-SOURCE-R1（2026-10-20）

S1 https://www.4gamer.net/games/013/G001377/20071120003/，2007/11/20 11:57，明确配信元デジパーク及原样厂商稿，现UTF8 HTTP200/267633B SHA2569094a04a3db86c100e987b404900b1f43b5085703ac107dff077258241b3f41a。H1 https://web.archive.org/web/20071223094402id_/http://www.4gamer.net:80/games/013/G001377/20071120003/，EUC-JP61462B SHA2569e7f0543531dc4838f7ceb8b745afe4fec9a9e1e32a2a90b7e215d8aa6f88cdc。O1 https://web.archive.org/web/20080220173517id_/http://stoneage.to:80/update/20071120_update_08_sekiei.html，真实S1出链主机/路径，UTF8 6511B SHA256bd7c436aeb0bd4d0ac3e0b73a3f3980e63105c19d040dd9403195276d9b85275。两次有界availability/回放均HTTP200，官方页更新标签2007/11/20不是2007首发日捕获；两正文核心1427/1460B分别pin，不删除异文，同语义不算独立两运营来源。

I1正文实际img https://www.4gamer.net/games/013/G001377/20071120003/TN/001.jpg，410×410/159779B SHA256d0c0d7b2a287ade46a87c8278b499206896ef7cc31b2e64e4972f2ba0074be85，目视四格场景；当前媒体图不等于已取历史图片或官方原图字节，官方页面警告开发中截图。用途为神话/世界事件/任务动机与视觉来源规格，不认证地图原ID或壶奖励。8记录、原资产不入Git、CI只派生JSON，实际ZIP/raw/Git按后续收据保管；Stage门不变。


### JP2008-RIMFY-FAMILY-QUEST-SOURCE-R1（2026-10-20）

S1 https://www.4gamer.net/games/013/G001377/20080707020/，2008/07/07 17:25，现HTTP200/267000B SHA256053f7cf040ad9fc0473d8dda7a96459ec450e4301a9737fe594dc049efd76df9；明确发布文分界与官方特页链接，但引文无公司署名，保守“媒体标发布文”非已取原运营HTML。1593B核心SHA256b1acc18afe061c7845acf20beb41ba03178a6d1bbc2d2b8c4931a8728229bf84。两个固定官方/媒体URL availability（20080901）空返回，精确响应/HTTP/SHA见报告，不称全网无档案。I1真实img https://www.4gamer.net/games/013/G001377/20080707020/TN/001.jpg，22218B JPEG122×99 SHA256600909ad41837331067eeeca9f9631f74ed1dabb4d578a7d92ba4e82b8309a42，已目视红橙四足兽；非原SPR/物种master。误001.gif404只记失败，不作源。六记录/原资产不入Git，CI仅派生，ZIP/raw/Git按真实后续验收保管。历史原件、脚本与等级/结局缺失不隐去。


### CN20-RIDING-TRAINER-COMBAT-SOURCE-R1（2026-10-20）

N1 https://web.archive.org/web/20011204194619id_/http://www.waei.com.cn/ZHUANQU/stoneage2/pet/new_pet.asp，69317B SHA256561950fd7bba41e7d39f4a781a671e11e175c7fe08dd1b5481fdf1fd23ba351b，重新读取其“骑乘宠物”实际href。S1 https://web.archive.org/web/20011204195948id_/http://www.waei.com.cn/ZHUANQU/stoneage2/pet/qdragon.asp，66879B SHA256ee59e2c8015d39b58f466943c9cb83ec1dce9894874caa2d539006e28e320a2e，首请求N1时间戳后跳转到此实际捕获；正文2.0标签、核心1212UTF8字节SHA2569fb3fc4b1d5e6d4221564b4f5786363d476c87dff7c9cb1ceecc474a1e7b8528。I1实际相对img/ridepet/1.jpg，最终 https://web.archive.org/web/20020402014049id_/http://waei.com.cn/ZHUANQU/stoneage2/pet/img/ridepet/1.jpg，31680B JPEG400×300 SHA256492e22003f4537dba9468c3f50125063d21db6e4f1d546147a344ebad509459f，已目视；不能称2001图像或同版SPR。三源HTTP200/实际跳转与捕获分别保存，原资产不进Git。用途：骑师服务/学习人与骑乘战斗文献约束；费用/等级上限/权重/脚本未知。独立CI与ZIP/raw/Git按真实后续收据保管。


### R28 新浪4.0标记骑宠证明书/九庄园来源（2026-10-20）

现页 https://games.sina.com.cn/zhuanqu/stoneage3/stoneage4_3.shtml 40475B SHA256 9860beacd990a083b096d7b046d9f59f8f5874db65e01d8c95bb31f6a74ced6b；一次availability固定历史 https://web.archive.org/web/20021201125523id_/http://games.sina.com.cn:80/zhuanqu/stoneage3/stoneage4_3.shtml 20144B SHA256 e27448cb7a6bccd92305126e1516fd2a6bb072f5046290c21c073707d532a7e9。核心各870B/SHA256 54f642c1069de1d775a852c29ba762c0f9b2a30341ad65005eb51ba39815a84a，两坏字节保留、九行列式对应不猜补；门户作者/原服未验证。派生STONEAGE-CN40-RIDING-CERTIFICATE-MANOR-SOURCE-R1.json、runner/test/中文规格；原HTML仅临时重放。R27三实源候选/mainZIP派生重放和保管清单已补。


### R29 华义大陆2.0宠物加工/料理（2026-10-20实取）

从真实导航“合成讲座/料理制作/宠物技能”取得固定快照：
https://web.archive.org/web/20011205052725id_/http://www.waei.com.cn/ZHUANQU/stoneage2/synthesize/course.asp 66409B SHA256 9fbce4e1084747db202e8e24ec4b9993dc3fb2399710b5ce4ee839c6c6bc5cc6；
https://web.archive.org/web/20011205052908id_/http://www.waei.com.cn/ZHUANQU/stoneage2/synthesize/cook.asp 65316B SHA256 e4ebd9244abd0f40daee66aa90a94f9d4d07fc2f4ed2f1d72e2f76bbac318960；
https://web.archive.org/web/20011204201517id_/http://www.waei.com.cn/ZHUANQU/stoneage2/pet/skill.asp 78022B SHA256 3056d727903c56000cdfcd877924efa244967eb8b6407db08c08e60ec7a9b0ee。
两真实原图裸域20020102225909 course/1.gif 122918B SHA256 4ed729712c5a04fb4711ded9ce9c8ab507cb23414b26594b135a5b58c861d042；20020102222833 cook/1.gif 134082B SHA256 1858c2bb6912394c9f48c5cfab0c62b140417080bd13d0c0f2f62c7f061cfd8b，GIF640×480，均已目视，只证界面参考。派生STONEAGE-CN20-PET-CRAFTING-SOURCE-R1.json/NEGATIVE-AUDIT-R1.json、中文规格与六输入runner。原HTML/图不进Git，推荐/传闻不升级原服公式。


### R29取源身份与双ZIP后续验收

三个2001官方站正文均未见具名作者，泛投稿说明不算文章署名；运营商域名/页脚证明托管，未认证运营商撰文或开发者意图。经验/传闻逐项保留。106ac84自身源候选1/main11已success，artifact12242150789/12241821433实际ZIP2635B、唯一派生JSON6524B SHA256 af990b11c3626a2c2a2e97345ec6f1b81185c122cdc04a7b7c0e2941dc79c71f，两支与六实输入本地结果一致。CI-REPLAY/CUSTODY永久固定job/ZIP/raw/Git摘要、初候选与补强候选不同HEAD清单，原HTML/图未提交。


### R30 大陆2.0人物创建/状态（2026-10-20实取）

既有目录实读“人物创造”href /ZHUANQU/stoneage2/tyro/creature.asp，实际正文 https://web.archive.org/web/20011201045054id_/http://www.waei.com.cn/ZHUANQU/stoneage2/tyro/creature.asp 65690B SHA256 cead36699828063607a335b7c3a0458dc7bf91089cc199889070c30091fdd6bb，核心2544B SHA256 04ef969e20bbd91ef1b0d9dea0b179b6f034ec6ea1d560772593e736213c168c。官方站未署名指南，不认证运营商作者/首发/实服。实际原图 https://web.archive.org/web/20011221174011id_/http://waei.com.cn/ZHUANQU/stoneage2/tyro/img/3.gif GIF640×480/114412B SHA256 662076868208bf5587b89daade5d34a5322b3d8ac6405964aebfa175e821f544，已目视户外场景，非创建状态面板。两旧派生报告JSS-LOGIN-MANUAL-CREATION-CONTRACT-R1.json与STONEAGE-WAEI-CN20-NEWCOMER-GUIDE-R1.json只核Git原记录、原网页未重取。新报告STONEAGE-CN20-CREATION-STATUS-SOURCE-R1.json、8实际改写反例、中文规格与固定三输入runner；原HTML/GIF不进Git。


### R31 日服宠物进化发布文/官方专题（2026-10-20）

https://www.4gamer.net/games/013/G001377/20081111023/ 当前269299B SHA256695386fb8ab426a8c6afeccc35d61638a5f5b78635b82c94dd56f49e02b0a76c，明确发布文分界和配信元DigiPark，核心3025B SHA256917dd517af3509ba1e8b4180263dd82bfe54812082f1c98002f44201cfefbd14。真实官方出链的一次availability得 https://web.archive.org/web/20090217151837id_/http://stoneage.to:80/update/20081111_update_ev1.html ，6538B SHA256184017ffb882c21bb4160616d7c75ba63cb016501b171ae6eff83f8c4bf06f8d，核心1506B SHA256f75153dcb4c09aeb7c6033bb3465ebb51f5ef3443f5a2440c72e026192f790ed。媒体20081130固定查询为空，官方image/20081111_ev_02.gif固定捕获请求404，仅记该范围。实际现媒体TN/001.gif、002.gif、003.gif已取/目视，SHA256分别5c331077ecf7f76e9e8bd8dd536b6db59a28d4bf6193c48570bb0e08cb262900、d2703d8e751becd2e51f6ce74ac92d73f562ddbd9ed1019fc1b3272336657a9e、31d7417696c6b56febd8fa117a0106990d77dc1329a624af9d046e088065976e，图为示意不证原SPR/突变。STONEAGE-JP2008-PET-EVOLUTION-SOURCE-R1.json/NEGATIVE-AUDIT与中文规格/五输入runner永久保管派生，原HTML/GIF不进Git；源日期/捕获/当前可读/原服分开。


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
