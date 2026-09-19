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
- Hananet infrastructure corroboration:
  - Korea Economic Daily, 2000-04-27: https://www.hankyung.com/article/2000042732051
  - identifies `www.hananet.net`, its game-content surface `http://game.hananet.net`, and the 2000 GamePlus service.
- Offline replication evidence:
  - iNews24, 2000-07-04: https://www.inews24.com/view/8928 records the planned Samsung PC / education-center distribution;
  - DailyGame, 2000-10-27: https://www.dailygame.co.kr/view.php?ud=200010271416380001837_26 reports a later package-supply agreement of roughly 60,000 units through the Samsung PC-education-center operator plus PC-game retail distribution.
- Operational value:
  - this is substantially earlier than the 2003 Korean 1.74 / Japanese 1.74a targets;
  - the client was replicated across an official site, at least two high-volume download portals, and material offline/package channels;
  - these independent distribution surfaces materially improve the chance that a provenance-preserving copy survives.
- Evidence boundary:
  - no exact 2000 client version label has been recovered;
  - installer filename, size, checksum, complete file tree and exact Hananet/CNET StoneAge URLs remain unknown;
  - byte identity between Inium, Hananet, CNET and packaged copies is unproven;
  - an intact Korean operator client would be a clean **Korean bridge specimen**, not automatic proof of JSS-Japan byte identity.
- Canonical research note:
  - `research/clients/STONEAGE-KOREA-2000-PUBLIC-DISTRIBUTION-RECOVERY-R1.md`.
- Next action:
  - prioritize filename/path recovery from `stoneage.enium.co.kr`, Hananet/GamePlus, CNET Korea, period software catalogs, magazine/ISP CDs and preserved Inium installations;
  - if bytes appear, immediately perform the clean-client acceptance test before further broad searching.
- Status: **TARGET-A / highest-priority operational pre-1.74 bridge search; bytes not yet located**.

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

## Current recovery order

1. **Korean Inium 2000 public client:** recover the original installer filename/path/bytes through the Inium site, Hananet/GamePlus, CNET and period offline/software archives. It is now the strongest operational early bridge because operator-era free distribution and massive replication are directly attested.
2. **JSS 1999 beta/retail/launcher:** continue in parallel as the historical origin target; do not lower its evidentiary importance merely because Korean 2000 may be easier to recover.
3. Continue recovery of the dedicated **`〖2.5纯净〗` thread** behind `tid=2132`; compare any recovered bytes against the mixed 2.5 resource bridge.
4. Continue recovery of the **Korean 1.74** exact-version operator-era installer identity/bytes.
5. Continue recovery of the **Japanese 1.74a** official/free beta installer identity/bytes from archived operator/Hangame/software mirrors.
6. Treat the recovered mixed 2.5 bundle as a **resource-format bridge only**; do not spend primary recovery effort extending its modified runtime surface while earlier clean-client targets remain open.
7. Recover the Sina "1.82" href/bytes only as an **unverified version-label candidate** and identify its actual build from the bytes rather than the page label.
8. Keep the Wayi official 8.5 package and `NetmarbleStoneAge120` as later controls, not substitutes for an early clean baseline.
9. For any newly recovered candidate bytes, stop broad searching immediately and perform the clean-client acceptance test plus first full inventory.
