# Source Registry Supplement — Clean Client Recovery R1

Date: 2026-09-19

Purpose: track **actual client-byte recovery targets** under DD-009. This ledger is intentionally narrower than the historical source registry. A version description, screenshot or article is not a recovered client.

## Acceptance states

- **RECOVERED-A** — bytes obtained from a strong operator/period distribution path; hashes/file tree recorded; no known modification.
- **RECOVERED-B** — bytes obtained and plausibly old/clean, but provenance or modification history is incomplete.
- **TARGET-A** — period/operator or reputable contemporary download evidence exists, but bytes have not yet been recovered.
- **TARGET-B** — credible preservation lead, but distribution provenance is weaker.
- **REJECT** — demonstrated repack, server bundle, modified client, custom patcher/injector, or mismatched version.

## TARGET-A — Korean Inium StoneAge 2000 — mass public/operator distribution

- Trial-service chronology:
  - DailyGame, 2000-10-12: https://www.dailygame.co.kr/view.php?ud=200010121149020000950_26
  - reports that Inium had begun StoneAge **trial service on 2000-10-04**;
  - keep this distinct from later 2000-10-13/14 reporting of the free-service site.
- Primary official-distribution evidence:
  - Electronic Times, 2000-10-13: https://www.etnews.com/200010120085
  - reports that Inium completed Korean localization/server work and began free service through `http://www.stoneage.enium.co.kr`.
- Distribution-scale corroboration:
  - Electronic Times, 2000-10-28: https://m.etnews.com/200010270015
  - reports roughly 200,000 downloads within the first weeks of free service.
- Named mirror evidence:
  - GameMeca, 2000-12-28: https://www.gamemeca.com/view.php?gid=5963
  - reports Hananet downloads above approximately **400,000** and CNET downloads above approximately **310,000**;
  - also says Hananet GamePlus service would begin on 2000-12-29.
- Exact CNET child-record / payload evidence:
  - preserved CNET Korea download-index snapshots dated **2000-11-10** and **2001-01-24** both identify StoneAge with `Software_Id=200009263856`;
  - detail-record path: `/downloads/File.asp?Platform_Id=1&Software_Id=200009263856`;
  - archived detail pages identify the file-size label as **257MB** and encode the download target as **`/pc/games/online/stoneage.zip`**;
  - the detail record links the maker homepage to `http://stoneage.enium.co.kr`;
  - exact Wayback Availability probes of both CNET host variants for the ZIP path returned zero available snapshots with zero request errors; bytes remain unrecovered.
- Hananet infrastructure corroboration:
  - Korea Economic Daily, 2000-04-27: https://www.hankyung.com/article/2000042732051
  - identifies `www.hananet.net`, its game-content surface `http://game.hananet.net`, and the 2000 GamePlus service.
- Exact Hananet StoneAge service/distribution evidence:
  - preserved GamePlus material links `[게임Plus]스톤에이지 게임Plus 신규 오픈` through `/gamenet/sitemap/map/mapstoneage.html` and `/gamenet/newframe/frstoneage.html` to the dedicated host `http://stoneage.hananet.net/main.htm`;
  - all exposed menu paths `1.htm`, `2.htm`, `2_2.htm`, `2_3.htm`, `2_4.htm`, `2_5.htm` have now been replayed; `2.htm` explicitly documents StoneAge CD-ROM installation, automatic install-menu startup, standard Setup mode and DirectX 6.1;
  - recovered `2_5.htm` exposes the Hananet boards `GAM2:STAD`, `STAF`, `STAN`;
  - the archived STAD 자료실 page says game-data downloads should be made from the corresponding GameNet game page and lists **record 8119**, `온라인게임 스톤에이지 정식 버전`, **260 M**, dated **2001-02-10**, plus **record 8120**, `온라인게임 스톤에이지 체험 버전`, **240 M**, also dated **2001-02-10**;
  - bounded inspection of that same archived STAD HTML source recovers disabled/commented direct-file rows that explicitly map **8120 / trial / 240 M → `http://stoneage.hananet.net/down/sa_demo.exe`** and **8119 / formal / 260 M → `http://stoneage.hananet.net/down/sa.exe`**; because those rows are inside an HTML comment block in the 2001-08-14 capture, they prove historical mapping but not that the buttons were visibly active at that snapshot;
  - the individual 8119/8120 record bodies still replay as HTTP 404;
  - the 260 M full-version record is close in nominal size to CNET's 257MB `stoneage.zip`, but no equality claim is made without byte/hash evidence.
- Exact Inium official-download mirror evidence:
  - archived Inium `down.htm` on **2000-11-09** links CNET `Software_Id=200009263856` and Hananet through `flashlinks.cgi` to exact PDS record **`view.asp?app_id=20001031524596220&type=C03`**;
  - archived 2001-04 `down.htm` explicitly says the listed StoneAge programs are **formal-version** downloads and directs trial users to a separate trial menu;
  - by 2001-06 the same official page links Gagamel **`/web_data/download/stoneagebeta.zip`** and GameTime **`download.asp?GW_IDX=9&GW_Name=Online`** alongside Hananet;
  - by 2001-08 the official page exposes Hananet direct path **`http://stoneage.hananet.net/down/sa.exe`**;
  - the Gagamel `stoneagebeta.zip` filename must not be classified as a trial build by name alone because Inium's page classifies the listed mirrors as formal-version downloads.
- Exact mirror archive boundary:
  - Wayback preserves the Hananet `flashlinks.cgi` wrapper and its frame target to PDS app ID `20001031524596220`;
  - six normalized direct-replay variants of the inner PDS record return HTTP 404 at the known wrapper timestamps;
  - exact Availability checks for Hananet **formal `sa.exe` (260 M)** and **trial `sa_demo.exe` (240 M)** produced 24 zero-error queries and zero available snapshots; direct replay of bare/`www` host variants at the known 2001-08-14 STAD timestamp returned HTTP 404 for both files;
  - earlier exact Availability/direct-prefix checks for Gagamel `stoneagebeta.zip` likewise yielded no recoverable binary snapshot;
  - these are Wayback-specific negative results and do not establish global loss.
- Offline replication evidence:
  - the 2001 GameTime `스톤 에이지 = Stone age` guide is a concrete near-period install-media carrier: RISS `M10029631` records **318 pages + one 12cm compact disc** and exposes National Library local bib number `KMO200119860`; KOLIS resolves edition key `24118251`, work number `UW20191223432` and `bibKey=10041033`, whose holding endpoint identifies exactly **2 libraries**: National Library of Korea (`recKey=1`, code `011001`) and Seogwipo Eastern Library (`recKey=12909233`, code `149013`). KOLIS MARC further gives `001=UB20011039873`, `012=KMO200119860`, `035=(011001)KMO200119860`, with field `300` explicitly recording one 12cm compact disc; the linked contents record includes `설치하기 = 8`. This proves the book+disc bibliographic object and two holdings, not current physical-disc integrity or availability. Catalog-layer searching is closed unless holder-level accession/supplement status or a public disc copy appears. Derived metadata: `research/recovered/STONEAGE-GAMETIME-2001-LIBRARY-SUPPLEMENT-R1.txt` and `research/recovered/STONEAGE-GAMETIME-2001-KOLIS-HOLDINGS-R1.txt`.
  - iNews24, 2000-07-04: https://www.inews24.com/view/8928 records the planned Samsung PC / education-center distribution;
  - DailyGame, 2000-10-27: https://www.dailygame.co.kr/view.php?ud=200010271416380001837_26 reports a later package-supply agreement of roughly 60,000 units through the Samsung PC-education-center operator plus PC-game retail distribution.
- Operational value:
  - this is substantially earlier than the 2003 Korean 1.74 / Japanese 1.74a targets;
  - the client was replicated across an official site, at least two high-volume download portals, and material offline/package channels;
  - these independent distribution surfaces materially improve the chance that a provenance-preserving copy survives.
- Evidence boundary:
  - no exact 2000 client version label has been recovered;
  - CNET's payload filename/path and nominal size are recovered (`/pc/games/online/stoneage.zip`, 257MB); Hananet now has exact mappings **formal `sa.exe` / 260 M** and **trial `sa_demo.exe` / 240 M**, plus early PDS app ID `20001031524596220`; checksums, complete file tree and all client bytes remain unknown;
  - byte identity between Inium, Hananet, CNET and packaged copies is unproven;
  - an intact Korean operator client would be a clean **Korean bridge specimen**, not automatic proof of JSS-Japan byte identity.
- Archive-probe boundary:
  - older broad Wayback CDX / Arquivo.pt probes encountered request timeouts / network-unreachable errors and remain inconclusive;
  - the latest exact-URL Arquivo.pt CDX pass covers **14 known mirror targets**, 2000–2005, with **0 request errors and 0 indexed captures**; those 14 successful zero-result queries are Arquivo.pt-specific exact-URL negative controls only. The older broad/text-oriented Arquivo probe had transport failures and remains separately inconclusive.
  - final Inium trial-menu probe R5 issued 45 Wayback Availability queries against the known sitemap/main-menu surface: 34 unique snapshots were reported available, 20 raw `id_` pages replayed successfully, 14 seed replays still failed, and the 20 successful raw pages yielded zero trial/demo/download-token hits; Wayback toolbar links were explicitly excluded. This is a **partial** negative control only and does not close the unreadable snapshots or prove that no separate trial menu existed.
  - Common Crawl mirror-neighborhood probe R3 issued 88 exact/prefix queries across the eight oldest listed indexes, but 83 ended in HTTP 503 or transport/SSL timeouts. Its zero recovered rows are therefore **inconclusive**, not a Common Crawl negative control; retry only under a healthy index service.
- Magazine-scan token boundary:
  - NetPower 2000-12 pp.173–176, 2001-01 pp.185–190 and 2001-02 pp.189–194 have now been probed with transient OCR and sparse-token extraction;
  - none produced an Inium/Hananet/CNET URL or installer/archive filename; 2001-02 only recovered the magazine-side `powerzine.com`, while isolated `32MB` / OCR-noise strings remain non-evidence for client size or filename;
  - treat these exact page ranges as closed low-value repeat targets unless a materially better extraction method appears.
- Canonical research note:
  - `research/clients/STONEAGE-KOREA-2000-PUBLIC-DISTRIBUTION-RECOVERY-R1.md`.
  - derived probes: `research/recovered/STONEAGE-INIUM-TRIAL-MENU-R1.txt`, `research/recovered/STONEAGE-COMMONCRAWL-EXACT-PAYLOADS-R1.txt`.
- Next action:
  - recover a surviving copy/mirror from the exact token set: CNET `/pc/games/online/stoneage.zip` (257MB), Hananet PDS `app_id=20001031524596220&type=C03`, Hananet formal `stoneage.hananet.net/down/sa.exe` (260 M), Hananet trial `stoneage.hananet.net/down/sa_demo.exe` (240 M), Gagamel `stoneagebeta.zip`, GameTime `GW_IDX=9`, and STAD records 8119/8120;
  - compare CNET/Hananet/Gagamel/GameTime candidates only at byte/hash and internal-file-tree level; do not infer equality from size or filename;
  - if bytes appear, immediately perform the clean-client acceptance test before further broad searching.
- Status: **TARGET-A / highest-priority operational pre-1.74 bridge search; bytes not yet located**.

## TARGET-A/B — Korean GameTime StoneAge Perfect Guide bonus CD — 2001

- YES24 catalog: https://www.yes24.com/product/goods/199761
- Aladin catalog: https://www.aladin.co.kr/shop/wproduct.aspx?itemid=282190
- Exact title: `스톤에이지 퍼펙트 가이드`
- ISBN-13: `9788995182123`
- ISBN-10: `8995182121`
- Catalog dates differ but refer to the same identified volume:
  - Aladin: **2001-01-01**;
  - YES24: **2001-04-30**;
  - RISS: **2001**;
  - all converge on the same ISBN family and 318-page book, so the dates are treated as catalog variants rather than separate editions.
- Media:
  - YES24: **CD 1**;
  - RISS formal physical description: **318p + compact disc 1 (12cm)**.
- RISS permanent record: `https://www.riss.kr/link?id=M10029631`.
- RISS lists **National Library of Korea (국립중앙도서관)** as a holding institution.
- Critical catalog fact:
  - YES24 explicitly says the bonus CD contains the **StoneAge installation program** plus demo-game CD content.
- Operational value:
  - this is a concrete early Korean installation-program carrier rather than a version-name recollection;
  - it is later than the 2000 Inium/Hananet/CNET mass-download target, but earlier than the 2003 1.74 bridge and can provide an independent near-period client specimen.
- Evidence boundary:
  - disc bytes, installer filename, size, version and hashes are not recovered;
  - do not assume the CD equals the 2000 online client;
  - any public CD image must be compared at file level against other Korean copies.
- Recovery method:
  - prioritize National Library / union-catalog supplementary-material metadata, accession/control fields, disc-label images and any distinct non-book record;
  - continue exact title/ISBN plus `부록 CD`, `설치프로그램`, ISO and preservation-catalog searches outside the already exhausted Internet Archive metadata queries;
  - use only public/preservation recovery paths; do not make purchase/manual acquisition a project dependency.
- Status: **TARGET-A/B / concrete 2001 install-media lead; bytes not yet located**.

## TARGET-B — Mainland China StoneAge "1.82" — Sina historical download label requiring byte verification

- Source page: https://games.sina.com.cn/zhqu/sta/download.shtml
- Source type: contemporaneous Sina Games StoneAge download page / portal mirror
- Current indexed page date: 2003-04-03
- Current indexed text explicitly contains:
  - `石器时代1.82客户端下载`
  - `石器时代1.82`
  - `安装包`
- Critical version-label caveat:
  - a contemporaneous Beijing Wayi statement dated 2003-03-21 says the anniversary **1.82 server** could be entered using the then-current **石器时代-宠物进化史** client, with compatibility for other client versions to be added;
  - therefore a 2003 page/button labelled `1.82` or `1.82 安装包` is **not sufficient proof that the linked bytes are an original historical 1.82 client build**.
  - source: https://news.17173.com/content/2003-3-21/n48_964760.html
- Operational value:
  - Sina remains a valuable period-mirror lead and may still resolve to a genuine old installer;
  - however its label must be treated as a recovery key only until executable/resource/file-tree evidence identifies the actual client generation.
- Current blocker:
  - the historical 1.82 anchor href, filename, size and bytes have not yet been extracted;
  - therefore **no hash, file tree, exact client-version attribution or purity claim is made**.
- Next action:
  - recover the original href/filename through search caches, archived HTML, period mirrors, or any surviving Sina download host;
  - if bytes are recovered, verify PE/resource/version strings, file tree and contamination before assigning a client version.
- Status: **TARGET-B / unverified version-label candidate**.

## TARGET-A — Japanese revival StoneAge 1.74a — official free beta distribution

- Contemporary report: https://forest.watch.impress.co.jp/article/2003/12/17/stoneage.html
- Source type: contemporaneous Impress / Mado no Mori software-release report
- Report facts:
  - `STONE AGE` was distributed as a **β版フリーソフト**;
  - version **1.74a**;
  - client date field **2003-12-12**;
  - supported Windows 98/Me/2000/XP;
  - downloads were available from the operator's official `stoneage.to` site and Hangame.
- Independent contemporary corroboration:
  - 4Gamer's 2003-12-12 report says client **先行ダウンロード** began that day on the official site before the open beta, and that Hangame would also provide the client;
  - source: https://www.4gamer.net/news/history/2003.12/20031212000000detail.html
- Operational value:
  - this is direct period evidence of a freely distributed client and therefore a strong clean-client recovery target;
  - it is a useful near-descendant bridge even though it is not a 1999 JSS build.
- Current blocker:
  - no surviving installer filename, file size, checksum, mirror body or complete file tree has yet been recovered;
  - current search confirms distribution, not bytes.
- Next action:
  - recover archived `stoneage.to` / Hangame download-page paths, old software-catalog mirrors, magazine-CD indexes, or preserved installer references.
- Status: **TARGET-A**.

## TARGET-A — Korean StoneAge 1.74 — Netmarble service baseline

- Contemporary preserved notice:
  - https://www.gamemeca.com/fam.php?gcode=fam_scarecrow&gid=133954&rts=board
- Current state:
  - a dated 2003-07-21 preserved response identifies the Netmarble StoneAge service start as **2003-07-28** and the service version as **`1.74`**;
  - the response also says the service would be provided free to members;
  - current exact download/client searches still have not produced a provenance-preserving installer, mirror, filename, size or hash.
- Operational value:
  - this is a concrete operator-era version anchor rather than a later private-server label;
  - if its original installer is recovered, Korean 1.74 is currently one of the strongest candidates for the first clean bridge specimen.
- Evidence boundary:
  - the dated version statement does not itself prove byte identity with any JSS build;
  - installer provenance and file-level analysis are still required.
- Status: **TARGET-A / exact operator-era version identity, bytes not yet located**.

## TARGET-A — JSS original launcher object

- Known first-party path: `http://www.titan.co.jp/stoneage/stoneage.exe`
- Known JSS description: replacement startup program, advertised as 212 KB.
- Value:
  - not a full client, but authentic JSS executable bytes would immediately improve executable/updater lineage analysis.
- Current blocker:
  - Wayback path is known but binary bytes remain inaccessible from the current environment.
- Status: **TARGET-A (partial-client executable)**.

## REJECT / LOW-VALUE controls

- Later private-server packs whose titles contain `1.82` but instruct users to use a 2.5 client are **not** 1.82 client evidence.
- "all-in-one" client+server+database packages that explicitly say they were adapted/matched for many versions are modified engineering bundles, not clean baseline clients.
- Community source-code archives may be useful for format clues, but they do not substitute for a clean historical runtime client.



## TARGET-B/C — StoneAge 2.5 preserved client/server/login bundle

- Public preservation thread: https://www.lab.welovesa.com/viewthread.php?extra=&page=1&tid=219
- First posted: 2009-08-29; download links were later refreshed.
- Preserved public MediaFire IDs:
  - `ev7l29fw77891go`
  - `ytaa168o5jih0lx`
- Preserved archive layout:
  - `SA2.5主程式`
  - `SA2.5外掛及登錄器`
    - `salogin_dat`
  - `SA2.5服務端`
    - `gmsv`
    - `saac`
- Historical availability / host lineage:
  - a 2012-02-26 reply explicitly says the earlier copy had been on **Megaupload** before that service disappeared;
  - on 2012-04-08 the administrator said the download would be restored;
  - on 2012-04-13 a forum user explicitly confirmed that the **two MediaFire files** were present after re-upload;
  - by 2012-12-03 a later reply again reported the download point unavailable.
- Recovery consequence:
  - there are at least two historical public-host generations for the same forum bundle (Megaupload -> two-part MediaFire);
  - search both host generations and reposts by the bundle title / `SA2.5主程式`, rather than assuming the preserved MediaFire IDs are the only possible byte path.
- Purity warning:
  - this is a **combined engineering bundle**, not an operator-origin installer;
  - the same thread contains a user remark that they had been trying to find an "original/plain" copy but commonly encountered modified packages;
  - therefore the bundle as a whole is **not a clean baseline**.
- Operational use:
  - if the two parts or mirrors can be recovered, isolate `SA2.5主程式`;
  - hash and inventory it separately;
  - check executables/config/resources for private-server endpoints, injected launchers, patched binaries and custom data before assigning any clean-client grade.
- Current byte status:
  - the old MediaFire URLs are preserved but are not directly accessible through the current web extraction interface;
  - exact-ID searches have not yet surfaced an independent live mirror.
- Recovery update:
  - both MediaFire parts are currently recoverable and were successfully downloaded, hash-verified, concatenated and extracted by GitHub Actions;
  - the derived inventory is committed at `research/recovered/STONEAGE-25-PRESERVED-BUNDLE-STATIC-INVENTORY-R1.txt`;
  - runtime assessment finds mixed/modified executable variants, while the large REAL/ADRN resource corpus remains technically valuable;
  - map provenance has been corrected: `stoneage2.5/map` contains **1,030 MAP + 1,011 DAT**, and 905 same-name MAP files are byte-identical to the bundled `SACH-MX0.30/MAP` corpus. The single-layer MAP family is therefore retained as external-tool-coupled evidence, while DAT is the descendant-source-corroborated client runtime map-cache format.
- Status: **RECOVERED-C runtime / B-grade resource bridge** — not a clean runtime baseline, but usable for resource-format reverse engineering.

## TARGET-A/B — `〖2.5纯净〗石器客户端` preservation thread

- Public index: https://lab.welovesa.com/forumdisplay.php?fid=40
- Thread title: **`〖2.5纯净〗石器客户端`**
- Thread id: **`2132`**
- First indexed date: 2012-09-26.
- Value:
  - the explicit `纯净` label makes this the highest-value current 2.5 preservation lead;
  - unlike the combined 2.5 client/server/login bundle, this thread is specifically cataloged as a client.
- Limitation:
  - the thread/download body is access-restricted in the current route;
  - no public filename, size, hash or download URL has yet been extracted;
  - `纯净` remains the forum label, not a verified cleanliness conclusion.
- Next action:
  - recover indexed/printable/archived snippets, reposts or mirrors for thread `tid=2132`;
  - if bytes are found, run the same clean-client acceptance test before promotion.
- Status: **TARGET-A/B — high-value 2.5 clean-client lead, bytes not yet recovered**.

## CLEAN-CLIENT CONTROL — version/login fingerprints are multi-factor, not single-key proof

- Primary technical discussion: https://www.lab.welovesa.com/viewthread.php?action=printable&tid=501
- Later reuse/corroboration discussion: https://www.shiqi.la/forum.php?extra=page%3D1&mobile=no&mod=viewthread&tid=13339
- Contradiction/control discussion: https://www.lab.welovesa.com/redirect.php?goto=lastpost&tid=3175
- Observed community technical claims:
  - a 2010 post labels `_DEFAULT_PKEY = "ttttttttt"` and `_RUNNING_KEY = "20041215"` as **原始2.5版本**;
  - the same post distinguishes other community branches such as `12345678/12345678` and `cary/cary`;
  - a 2015 thread shows a different source tree where the same `ttttttttt / 20041215` pair is commented as **7.5**, proving the pair is not a unique version identity;
  - the 2015 technical reply explicitly notes that different client versions also differ in **login-packet format**, not only key values.
- Evidence boundary:
  - these are community/source-lineage technical records, not operator documentation;
  - **PKEY/RUNKEY must not be used alone to declare a recovered client 2.5 or clean.**
- Operational validation rule:
  - use key strings only as one contamination/lineage fingerprint among executable metadata, version strings, packet behavior, file tree, timestamps, launcher/updater structure, REAL/ADRN/resource generations, network endpoints and cross-copy hashes.
- Status: **CONTROL-A/B — high-value false-positive guard, not a version oracle**.

## CONTROL-A/B — Wayi official StoneAge 8.5 installer preservation set

- Public preservation thread: https://www.lab.welovesa.com/viewthread.php?action=printable&tid=1654
- Title: `華義石器時代主程式安裝檔`
- Six preserved MediaFire IDs:
  - `l5i274801ov19w7`
  - `g9b3g3hjmwwttg3`
  - `e859n1nm1tk12j8`
  - `69vrzm3nox8f0v9`
  - `clbwjkcqqhxq6k9`
  - `42uy5b9abbcu4qr`
- The poster explicitly described installing it as a clean main program.
- Later discussion identifies the package as the official Wayi **8.5 / 魔域大冒險** client.
- Role:
  - too late to be the preferred earliest bridge specimen;
  - valuable as a known-official later comparison/control client if its parts or a mirror are recovered.
- Status: **CONTROL-A/B — later official-client preservation target**.

## CONTROL-B — Korean `NetmarbleStoneAge120` preserved-client token

- Public forum index: https://lab.welovesa.com/forumdisplay.php?fid=40&page=2
- Indexed title: `韩国石器客户端NetmarbleStoneAge120`
- Thread id: **`2117`**, first indexed 2012-09-22.
- Independent forum usage evidence later refers to downloading and installing `NetmarbleStoneAge120`.
- Value:
  - supplies an exact package/search token for a preserved Korean client line;
  - potentially useful to reconstruct Netmarble-era packaging/resource evolution.
- Limitation:
  - version identity, original operator distribution path and cleanliness are not established;
  - this is not evidence that the package is Korean 1.74.
- Status: **CONTROL-B / later Korean preservation lead**.

## CONTROL / LEAD — Korean 2000–2001 public-media corpus

- Canonical derived record:
  - `research/clients/STONEAGE-KOREA-2000-2001-PUBLIC-MEDIA-CORPUS-R1.md`
- Public carrier directory scans:
  - PC Game Magazine: **21 images**, 2000-09 through 2001-12, complete directory walks, 0 scan errors, 0 truncation, 0 StoneAge-path hits;
  - GamePia No.58–64: **12 images**, complete directory walks, 0 scan errors, 0 truncation, 0 StoneAge-path hits;
  - NetPower 2001.12: **2 images**, complete directory walks, 0 StoneAge-path hits.
- Internet Archive exact-token reverse search:
  - **216** item metadata/file-list records checked with 0 request errors;
  - exact historical keys included `sa_demo.exe`, `stoneagebeta.zip`, `20001031524596220`, `200009263856`, `GW_IDX=9` and `/pc/games/online/stoneage.zip`;
  - **0 exact target filename matches**; nine file candidates were size-only false positives.
- Wayback CDX 2000–2002 distribution-prefix census:
  - 12 prefix queries, 0 request errors, 362 rows / 181 unique URLs;
  - exact Hananet `stoneage.hananet.net/down/` and CNET `korea.cnet.com/pc/games/online/` prefixes return 0 rows for tested bare/www variants;
  - Gagamel, GameTime and Inium prefixes return real records, making those Hananet/CNET zero-row results archive-specific directory-level negative controls rather than evidence of probe failure.
- New GameTime recovery lead:
  - Wayback CDX preserves `http://www.gametime.co.kr/data/data_list.asp?search_word=%bd%ba%c5%e6%bf%a1%c0%cc%c1%f6&category=online` at **2001-07-01 05:34:12 UTC**;
  - the CP949/EUC-KR search term decodes to **`스톤에이지`**;
  - this provides a concrete archived StoneAge result surface from which to recover record IDs/detail/download endpoints and test the independently preserved `GW_IDX=9` identity.
- Evidence boundary:
  - all no-hit statements above apply only to the exact carrier/prefix/query corpus;
  - no early Korean clean-client bytes are recovered by these negative controls.
- Status: **CONTROL-A/B + ACTIVE LEAD — broad public-media surfaces narrowed; GameTime archived result chain is active.**

## Current recovery order

1. **Korean Inium 2000 public client:** recover the original installer filename/path/bytes through the Inium site, Hananet/GamePlus, CNET and period offline/software archives. It is now the strongest operational early bridge because operator-era free distribution and massive replication are directly attested.
2. **JSS 1999 beta/retail/launcher:** continue in parallel as the historical origin target; do not lower its evidentiary importance merely because Korean 2000 may be easier to recover.
3. Resolve the **archived 2001-07-01 GameTime `스톤에이지` search/result chain** and its relation to `GW_IDX=9`; keep the 2001 Perfect Guide bonus CD as a separate near-period installation-media target, but do not repeat closed ISBN/title/union-catalog searches unless new supplementary-disc evidence appears.
4. Continue recovery of the dedicated **`〖2.5纯净〗` thread** behind `tid=2132`; compare any recovered bytes against the mixed 2.5 resource bridge.
5. Continue recovery of the **Korean 1.74** exact-version operator-era installer identity/bytes.
6. Continue recovery of the **Japanese 1.74a** official/free beta installer identity/bytes from archived operator/Hangame/software mirrors.
7. Treat the recovered mixed 2.5 bundle as a **resource-format bridge only**; do not spend primary recovery effort extending its modified runtime surface while earlier clean-client targets remain open.
8. Recover the Sina "1.82" href/bytes only as an **unverified version-label candidate** and identify its actual build from the bytes rather than the page label.
9. Keep the Wayi official 8.5 package and `NetmarbleStoneAge120` as later controls, not substitutes for an early clean baseline.
10. For any newly recovered candidate bytes, stop broad searching immediately and perform the clean-client acceptance test plus first full inventory.
