# Source Registry Supplement — Clean Client Recovery R1

Date: 2026-09-18

Purpose: track **actual client-byte recovery targets** under DD-009. This ledger is intentionally narrower than the historical source registry. A version description, screenshot or article is not a recovered client.

## Acceptance states

- **RECOVERED-A** — bytes obtained from a strong operator/period distribution path; hashes/file tree recorded; no known modification.
- **RECOVERED-B** — bytes obtained and plausibly old/clean, but provenance or modification history is incomplete.
- **TARGET-A** — period/operator or reputable contemporary download evidence exists, but bytes have not yet been recovered.
- **TARGET-B** — credible preservation lead, but distribution provenance is weaker.
- **REJECT** — demonstrated repack, server bundle, modified client, custom patcher/injector, or mismatched version.

## TARGET-A — Mainland China StoneAge 1.82 — Sina historical download mirror

- Source page: https://games.sina.com.cn/zhqu/sta/download.shtml
- Source type: contemporaneous Sina Games StoneAge download page / portal mirror
- Current indexed page date: 2003-04-03
- Current indexed text explicitly contains:
  - `石器时代1.82客户端下载`
  - `石器时代1.82`
  - `安装包`
- Operational value:
  - this is currently the strongest public period-mirror lead to a Mainland 1.82 client installer;
  - the page also distinguishes install packages, installed-file packages and virtual-disc images for later versions, which makes the 1.82 `安装包` label materially more useful than a later private-server repost.
- Current blocker:
  - the present extraction path can index the page text but times out when opening the page body;
  - the historical 1.82 anchor href, filename, size and bytes have not yet been extracted;
  - therefore **no hash, file tree or purity claim is made**.
- Next action:
  - recover the original href/filename through search caches, archived HTML, period mirrors, or any surviving Sina download host;
  - only after bytes are obtained run the clean-client acceptance test.
- Status: **TARGET-A**.

## TARGET-A — Japanese revival StoneAge 1.74a — official free beta distribution

- Contemporary report: https://forest.watch.impress.co.jp/article/2003/12/17/stoneage.html
- Source type: contemporaneous Impress / Mado no Mori software-release report
- Report facts:
  - `STONE AGE` was distributed as a **β版フリーソフト**;
  - version **1.74a**;
  - client date field **2003-12-12**;
  - supported Windows 98/Me/2000/XP;
  - downloads were available from the operator's official `stoneage.to` site and Hangame.
- Operational value:
  - this is direct period evidence of a freely distributed client and therefore a strong clean-client recovery target;
  - it is a useful near-descendant bridge even though it is not a 1999 JSS build.
- Current blocker:
  - no surviving installer filename, file size, checksum, mirror body or complete file tree has yet been recovered;
  - current search confirms distribution, not bytes.
- Next action:
  - recover archived `stoneage.to` / Hangame download-page paths, old software-catalog mirrors, magazine-CD indexes, or preserved installer references.
- Status: **TARGET-A**.

## TARGET-A/B — Korean StoneAge 1.74

- Historical version evidence is already registered separately.
- Current state:
  - the version label `1.74` is independently documented for Korean service;
  - current exact download/client searches have not yet produced a provenance-preserving installer, mirror, filename, size or hash.
- Operational value:
  - if recovered, Korean 1.74 may be an especially useful bridge because it predates the Japanese 1.74a revival label and can be compared directly.
- Status: **TARGET-A for version identity / not-yet-located artifact**.

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

1. Extract the actual Sina 1.82 installer href/filename/bytes.
2. Recover Japanese 1.74a installer identity/bytes from archived operator/Hangame/software mirrors.
3. Continue Korean 1.74 installer recovery.
4. Continue JSS original executable/full-client recovery in parallel.
5. As soon as any candidate bytes are obtained, stop broad historical searching long enough to perform the clean-client acceptance test and build the first full inventory.
