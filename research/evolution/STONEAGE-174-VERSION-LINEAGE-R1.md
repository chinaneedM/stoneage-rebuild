# StoneAge 1.74 / 1.74a Version-Lineage Archaeology — R1

Date: 2026-09-18

Purpose: isolate the historically important `1.74` / `1.74a` version labels that recur in Korean and 2003 Japanese StoneAge evidence, and turn them into controlled client-recovery targets without assuming that numerically similar labels identify the same binary or content state.

## Evidence rule

- A matching version number is not by itself proof of identical client bytes, identical regional data, or direct branch ancestry.
- Contemporary operator/media evidence outranks later community recollection.
- The 2003 Japanese revival remains a **near-descendant control**, not a substitute for the 1999 JSS retail/beta client.
- The project's primary target remains the earliest recoverable JSS client/media. `1.74` artifacts are secondary bridge targets that may help reconstruct the path toward that baseline.

## 1. Contemporary Korean 1.74 anchor — Netmarble, July 2003

A 2003-07-21 GameMeca community-board preservation reproduces an answer identified as coming from Netmarble's StoneAge homepage Q&A.

URL:

https://www.gamemeca.com/fam.php?gcode=fam_scarecrow&gid=133954&rts=board

The preserved answer says:

- service planned for **2003-07-28**;
- the version to be served is explicitly **`1.74`**;
- future updates would follow.

Classification: **B / contemporaneous preserved operator-answer evidence**.

Reason for B rather than A: the currently accessible object is a same-period repost quoting Netmarble's own answer rather than the still-live original Netmarble page.

Research consequence: Korean `1.74` is not merely a later private-server label; it was publicly named as the service version at Netmarble's July 2003 launch.

## 2. Older Korean continuity — Inium 1.74 before 2.0

A preserved community archive at Pooya's StoneAge reproduces a post dated **2001-11-14** describing a preview of the upcoming `2.0` family/riding update and explicitly labels the context as **Inium StoneAge after 1.74**.

URL:

https://pooyas.com/index.php?document_srl=166300&mid=screenshot

The preserved text discusses:

- the `2.0` family system;
- obtaining riding capability in the new family/riding context;
- screenshots preserved with the post.

Classification: **C/B / later preservation of dated operator-era material**.

This supports the existence of an Inium-era `1.74 -> 2.0` transition, but the current preservation page is not itself the original 2001 host.

## 3. Contemporary Japanese revival anchor — 1.74a

Mado no Mori / Impress reported the revived Japanese open-beta client on **2003-12-17** and records the software metadata:

- beta freeware;
- Windows 98/Me/2000/XP;
- **version `1.74a`**;
- date field **2003-12-12**.

URL:

https://forest.watch.impress.co.jp/article/2003/12/17/stoneage.html

Classification: **A / contemporary specialist software-release metadata**.

This is currently the strongest direct version-number evidence for the 2003 Japanese revival client.

## 4. Japanese revival distribution dates

Contemporary Japanese reporting independently states that the revival client became available for advance download on **2003-12-12**, ahead of the open beta beginning **2003-12-16**.

Sources:

- 4Gamer: https://www.4gamer.net/news/history/2003.12/20031212000000detail.html
- GAME Watch: https://game.watch.impress.co.jp/docs/20031212/sa.htm
- official site named in period coverage: `http://stoneage.to/`
- Hangame was a second download surface.

Classification: **A for the 2003 distribution event**.

Current limitation: public search has not recovered the installer filename, file size, checksum or a still-downloadable original `1.74a` package.

## 5. What the number match means — and does not mean

Observed:

- Korean Netmarble launch: **`1.74`**, July 2003.
- Japanese revival beta: **`1.74a`**, December 2003.
- Preserved Inium-era material independently places **`1.74` before `2.0`**.

This makes a shared or related version-number lineage a **high-value hypothesis**.

It does **not** yet establish that:

- Japanese `1.74a` is the Korean `1.74` client plus a trivial suffix;
- either 2003 client is byte-identical to an Inium 1.74 build;
- `1.74` was the final JSS internal numeric version;
- the JSS 1999 retail client used a `1.xx` public/internal version label at all;
- Korean/Taiwan/Japanese assets, quests, maps, UI, server rules or executables were identical at the same visible version number.

## 6. Why this bridge matters to the reconstruction project

If an authenticated or well-provenanced `1.74` / `1.74a` client is recovered publicly, it can be used to:

1. inventory a much earlier client file tree than the later 1.82–8.x branches commonly preserved today;
2. fingerprint executable names, PE resources and launcher/runtime architecture;
3. inventory `REAL/ADRN/SPR/SPRADRN` resource generations and compare record/block formats;
4. recover map/character/pet/item/UI data near the old baseline;
5. compare the dedicated trade-window addition against the JSS-era no-trade-window boundary;
6. test GM-only versus normal-player riding assets/code;
7. compare asset IDs and data layout with later 1.82 source/data;
8. provide a bridge toward any future recovered JSS retail/beta client.

The bridge is valuable even if later shown not to be direct JSS ancestry: a negative diff would date regional divergence.

## 7. Search results in this pass

Exact public-web and GitHub searches were run for combinations including:

- `StoneAge 1.74`
- `StoneAge 1.74a`
- Korean `스톤에이지 1.74 클라이언트`
- `sa.exe`
- `StoneAge.exe`
- `real.bin`
- `adrn.bin`

Result:

- contemporary/preserved version references were recovered;
- **no provenance-preserving downloadable 1.74/1.74a client, installer filename, file tree or binary hash was recovered in this pass**;
- GitHub code search produced no credible 1.74 client artifact;
- a 2024 Korean Lost Media request independently shows that the Inium client itself was still being actively sought, with the poster reporting only low-resolution surviving screenshots rather than a client copy. This is preservation-status evidence, not proof of permanent loss;
- GameZone's search index still exposes a separate attachment named `sa_182_code.rar` (403.4 KB) advertised as 1.82 client source, but the attachment bytes are not retrievable through the current path and its provenance is unverified.

## 8. Controlled next targets

1. Recover the 2003 Japanese `1.74a` installer filename from old `stoneage.to`, Hangame, download portals, antivirus catalogs, magazine CD indexes or cached link pages.
2. Recover a Korean Inium/Netmarble `1.74` installation package or file tree from a public preservation source; explicitly search lost-media communities, old Korean file boards and magazine/software archives because a 2024 preservation request still lacked the client.
3. Attempt recovery of the indexed `sa_182_code.rar` attachment as a **secondary source-lineage control**; authenticate its age/content before using it and never substitute it for a 1.74 or JSS artifact.
4. On any recovered artifact, record hashes externally and keep proprietary bytes out of this repository.
5. Compare:
   - executable names/resources;
   - `REAL/ADRN/SPR/SPRADRN` filenames and generations;
   - map files;
   - pet/character asset IDs;
   - trade UI;
   - riding assets/flags;
   - server-list/update configuration.
6. Only after byte/data comparison decide whether `1.74` and `1.74a` share a direct client branch.
7. Continue treating the 1999 JSS retail disc and September beta as the primary archaeological targets.
