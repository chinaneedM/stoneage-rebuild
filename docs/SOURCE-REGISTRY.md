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
- Status: beta dates now supported by `SRC-JP-1999-PLAYONLINE-015`; client binary still not recovered
- Relevance: proves existence of a public/recruited beta and narrows first recoverable client target.

### SRC-JP-1999-RETAIL-01

- Type: JSS first-edition retail package / CD-ROM evidence
- Period: 1999 launch
- Confidence: S if physical media can be acquired or imaged with provenance; otherwise B/A/C depending record
- Status: concrete surviving first-edition package lead now recorded as `SRC-JP-1999-RETAIL-MERCARI-01`; original verified game-disc image still missing
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
  - existence of a distributable beta-era client before commercial launch.
- Does not support:
  - beta installer filename;
  - exact distribution mechanism;
  - checksums or internal version number;
  - exact beta-to-retail differences.
- Follow-up: recover beta client/media or contemporaneous download/install instructions; capture exact page number(s).

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
- Note: used together with the contemporaneous PC Watch scheduled-release report, this is sufficient for the working timeline to treat 1999-10-15 as the commercial service start unless conflicting primary evidence appears.

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
  - whether the listed bonus CD is distinct from the game client disc in a particular way.
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
