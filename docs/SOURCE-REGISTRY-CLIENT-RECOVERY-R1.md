# Source Registry Supplement — Clean Client Recovery R1

Date: 2026-09-18

Purpose: track **actual client-byte recovery targets** under DD-009. This ledger is intentionally narrower than the historical source registry. A version description, screenshot or article is not a recovered client.

## Acceptance states

- **RECOVERED-A** — bytes obtained from a strong operator/period distribution path; hashes/file tree recorded; no known modification.
- **RECOVERED-B** — bytes obtained and plausibly old/clean, but provenance or modification history is incomplete.
- **TARGET-A** — period/operator or reputable contemporary download evidence exists, but bytes have not yet been recovered.
- **TARGET-B** — credible preservation lead, but distribution provenance is weaker.
- **REJECT** — demonstrated repack, server bundle, modified client, custom patcher/injector, or mismatched version.

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

## Current recovery order

1. Recover the **Korean 1.74** operator-era installer identity/bytes.
2. Recover the **Japanese 1.74a** official/free beta installer identity/bytes from archived operator/Hangame/software mirrors.
3. Continue JSS original executable/full-client recovery in parallel.
4. Recover the Sina "1.82" href/bytes as an **unverified version-label candidate** and identify its actual build from the bytes rather than the page label.
5. Continue earliest Taiwan operator-client recovery in parallel.
6. As soon as any candidate bytes are obtained, stop broad searching long enough to perform the clean-client acceptance test and build the first full inventory.
