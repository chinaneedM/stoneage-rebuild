# JSS 1999 Origin Evidence — R1

Date: 2026-09-18

Purpose: record the first structured pass over contemporaneous 1999 Japanese evidence for the JSS origin period of `STONEAGE`, while keeping launch artifacts, beta artifacts, design intent, and later retrospectives distinct.

## Evidence classification rule

- **FACT** — directly supported by the cited source, at the level stated.
- **HYPOTHESIS** — plausible inference requiring more evidence.
- **OPEN** — unresolved recovery/verification task.

A contemporaneous description of a planned system proves design intent at that date; it does **not** by itself prove the feature shipped unchanged in the retail client.

## 1. March 1999 — public exhibition

### Source

`SRC-JP-1999-PCWATCH-TGS-SPRING`

PC Watch, Tokyo Game Show '99 Spring report, published 1999-03-19:

https://pc.watch.impress.co.jp/docs/article/990319/tgs.htm

### FACT

PC Watch reports `STONEAGE` being prominently exhibited in NTT Data's `Gamer's Dream` booth as that platform's third title, describing it as a somewhat comical game set in a prehistoric era.

### What this proves

- the title was in public promotion by 1999-03-19;
- `STONEAGE` was already positioned within the Gamer's Dream lineup before the May magazine feature and September beta.

### What remains OPEN

- the exact build shown at the event;
- whether it was playable there;
- surviving event-specific screenshots/video/demo media with provenance.

## 2. May 1999 — pre-launch design intent

### Source

`SRC-JP-1999-PLAYONLINE-012`

Preserved scan of *Play Online*, issue 012 (May 1999):

https://www.kingpin.info/download/kingpin/media/magazine/Play_Online_Issue_012_%28Japanese%29_1999-05.pdf

### FACT

The contemporaneous article identifies `STONEAGE` as a Japan System Supply title then targeting a summer 1999 service start.

The article describes the intended experience as a comparatively relaxed Stone Age RPG rather than a war-centered game, explicitly emphasizing food/resources and community. It also describes player cooperation contributing to village growth and richer communal life.

### What this proves

By May 1999, the published design pitch already included:

- food/resource concerns;
- community-oriented play;
- cooperative village development;
- a deliberately relaxed, socially accessible tone.

### What this does not prove

It does not prove that every described system survived unchanged into the September beta or October retail launch.

### Research consequence

The earlier project hypothesis that resource/community/village-life ideas may belong to the original JSS conception is now partially promoted: these themes are **FACT as documented pre-launch design intent**. Their exact implementation in the shipping 1999 client remains OPEN.

## 3. September 1999 — beta test window

### Source

`SRC-JP-1999-PLAYONLINE-015`

Preserved scan of *Play Online*, issue 015 (September 1999):

https://www.kingpin.info/download/kingpin/media/magazine/Play_Online_Issue_015_%28Japanese%29_1999-09.pdf

### FACT

The magazine states that the `STONEAGE` beta test ran from **1999-09-01 through 1999-09-30** and that *Play Online* readers were allocated 200 tester accounts.

### What this proves

- a public/recruited beta existed before the commercial launch;
- the beta window can be bounded to September 1999 by contemporaneous evidence;
- a period-correct beta client necessarily existed in some distributable form.

### What remains OPEN

- beta installer/client filename;
- distribution mechanism;
- file size and checksums;
- executable/internal version number;
- whether beta media was download-only or also distributed on physical media;
- exact differences from the October retail client.

## 4. 1999-09-17 — launch-date evidence at Tokyo Game Show

### Source

`SRC-JP-1999-PCWATCH-TGS-AUTUMN`

PC Watch, Tokyo Game Show '99 Autumn report, published 1999-09-17:

https://pc.watch.impress.co.jp/docs/article/990917/game02.htm

### FACT

PC Watch reported `STONEAGE`, published by Japan System Supply and shown in the Gamer's Dream booth, as scheduled for release on **1999-10-15**.

The report describes players living as inhabitants of a Stone Age setting, hunting dinosaurs, chatting with other players, and adventuring with companions in a deliberately gentle atmosphere.

### Limitation

This article establishes the contemporaneous scheduled release date, not by itself that the schedule was actually met.

## 5. Period retail advertisement

### Source

`SRC-JP-1999-AD-YAHOO-01`

Yahoo Auctions listing preserving photographs of a period magazine advertisement:

https://auctions.yahoo.co.jp/jp/auction/k1223621478

### FACT from visible advertisement text

The advertisement shows:

- Windows 95/98;
- scheduled release **1999-10-15**;
- planned price **8,800 yen before tax**;
- JSS URL `http://www.titan.co.jp/`;
- Gamer's Dream URL `http://www.gamersdream.ne.jp/`;
- an original mug as a reservation bonus;
- an initial-edition `STONEAGE` special CD as an advertised initial bonus/feature.

### Research consequence

This source materially strengthens the physical-media recovery track because the special-CD claim is no longer dependent only on a modern seller description. It also provides exact period domains to target in web-archive recovery.

### What remains OPEN

- original magazine title/issue/page;
- contents and purpose of the special CD;
- whether that CD is separate from the install/client disc;
- product/JAN code and disc matrix identifiers;
- archived 1999 snapshots of the two printed domains containing download, support, patch, or beta distribution pages.

## 6. Later confirmation of commercial start date

### Source

`SRC-JP-2009-4GAMER-10TH`

4Gamer retrospective/service-end announcement, 2009-11-26:

https://www.4gamer.net/games/013/G001377/20091126051/

### FACT / later retrospective

4Gamer states that `STONEAGE` service started on **1999-10-15** and had reached its tenth anniversary in October 2009.

### Research consequence

Combined with the contemporaneous 1999-09-17 PC Watch report and period retail advertisement, this supports treating **1999-10-15** as the JSS commercial service start date unless contradictory primary material is later recovered.

## 7. Physical first-edition retail lead

### Source

`SRC-JP-1999-RETAIL-MERCARI-01`

Mercari listing:

https://jp.mercari.com/item/m44997025885

The listing photographs/describes an unopened `日本システムサプライ STONEAGE 初回限定版` and states that the package contains a first-edition bonus CD-ROM. The seller also associates included promotional material with Tokyo Game Show 1999.

### Status

**Acquisition/recovery lead, not yet S-grade evidence.**

The listing is useful because it demonstrates a surviving physical first-edition package candidate and gives us a concrete object to seek from collectors/secondary markets. The contemporaneous advertisement independently corroborates that a special CD was advertised for the initial edition, but neither source tells us the disc's exact contents.

### What would promote this lead to S grade

Acquire or obtain a provenance-preserving dump/photo set of an original package and record:

- full box front/back/spine photography;
- manual and insert photography/scans;
- disc label photography;
- exact disc count;
- pressed-disc identifiers / matrix text;
- full file tree;
- SHA-256 (and preferably SHA-1/MD5 for cross-archive matching) of disc image and key executables;
- PE metadata and embedded version resources;
- README/patch/version strings;
- packaging product code, JAN code, price, supported OS and network requirements.

## 8. Current highest-priority recovery target

The project still does **not** possess a verified 1999 JSS beta client or retail disc image.

Priority order after this evidence pass:

1. Recover a verifiable 1999 JSS retail CD / initial-edition package or provenance-preserving disc image.
2. Determine the identity and contents of the advertisement's initial-edition `STONEAGE` special CD.
3. Recover the September 1999 beta client or identify its exact distribution filename/media.
4. Recover archived August-October 1999 pages from `titan.co.jp` and `gamersdream.ne.jp`, prioritizing download, support, beta, patch, and product pages.
5. Capture page-level archival copies of the May and September 1999 *Play Online* evidence and record issue/page metadata.
6. Use recovered retail/beta artifacts to establish JSS internal version numbering and a reproducible file-level archaeology baseline.
