# StoneAge Korea 2000 Public-Distribution Recovery R1

Status: **TARGET-A / operator-era mass-distribution client lead; bytes not yet recovered**

Date: 2026-09-19

## Why this target changes the recovery order

The project priority is the earliest freely/publicly obtainable, provenance-preserving StoneAge client that can actually be recovered.

Contemporary Korean press now establishes a much earlier public distribution surface than the 2003 Korean 1.74 / Japanese 1.74a bridge targets:

- Inium completed Korean localization/server work and announced free StoneAge service through its own `stoneage.enium.co.kr` site in October 2000.
- By late October, contemporaneous reporting said downloads had already exceeded 200,000.
- By 2000-12-28, GameMeca reported StoneAge download counts through **Hananet and CNET** of approximately **400,000 and 310,000 respectively**.
- A contemporaneous product-launch report also records a distribution agreement for roughly **60,000 sale packages** through the operator of Samsung PC education centers, plus nationwide PC-game retail distribution.

This does not recover bytes yet, but it materially improves preservation odds: the 2000 Korean client was not distributed through one fragile operator URL only; it had multiple independent online and offline replication channels.

## Contemporary evidence

### 0. Trial-service start versus later free-service reporting

DailyGame, 2000-10-12:

- https://www.dailygame.co.kr/view.php?ud=200010121149020000950_26
- reports that Inium imported JSS StoneAge and had begun **trial service on 2000-10-04**.

This date must be kept distinct from the 2000-10-13/14 Electronic Times coverage that describes the Korean localization/server work and free-service site. The evidence therefore supports a chronology of:

- **2000-10-04:** trial service already underway, per contemporary DailyGame reporting;
- **2000-10-13/14:** contemporaneous Electronic Times coverage of free Korean service through the Inium StoneAge site.

Do not collapse these into one “launch date”; the labels and reporting events differ.

### 1. Inium official free-service site

Electronic Times, 2000-10-13:

- https://www.etnews.com/200010120085
- reports that Inium finished Korean localization and server construction;
- states that free service had begun through `http://www.stoneage.enium.co.kr`;
- attributes the original game to JSS.

Classification: **A / contemporary operator-era distribution evidence**.

Evidence boundary: the article confirms the official service/distribution surface, not the exact installer filename, version label, checksum or byte identity.

### 2. More than 200,000 downloads within the first weeks

Electronic Times, 2000-10-28:

- https://m.etnews.com/200010270015
- reports that after the free-service launch, download users had reached about 200,000 within roughly two weeks.

DailyGame / product-presentation coverage, 2000-10-27:

- https://www.dailygame.co.kr/view.php?ud=200010271416380001837_26
- independently reports more than 200,000 downloads;
- also records a supply agreement for about 60,000 sale packages through the Samsung PC-education-center operator and planned distribution through PC-game retailers.

Classification: **A/B / contemporary distribution-scale evidence**.

### 3. Hananet and CNET mirror counts

GameMeca, 2000-12-28:

- https://www.gamemeca.com/view.php?gid=5963
- reports that Hananet StoneAge downloads had passed about **400,000**;
- reports that CNET StoneAge downloads had passed about **310,000**;
- says service through Hananet GamePlus would begin on 2000-12-29.

Classification: **A / contemporary named-mirror evidence**.

This is the strongest current recovery clue because it proves at least two high-volume third-party portal distribution paths existed in addition to the Inium site.

### 4. Hananet GamePlus infrastructure

Korea Economic Daily, 2000-04-27:

- https://www.hankyung.com/article/2000042732051
- identifies Hananet as `www.hananet.net`;
- identifies its game-content surface as `http://game.hananet.net`;
- describes the GamePlus online-game service launching in 2000.

This corroborates the portal family named in the December StoneAge article. Archive recovery has now resolved a concrete StoneAge-specific GamePlus path chain:

- a preserved 2001-01-18 GamePlus main page contains **`[게임Plus]스톤에이지 게임Plus 신규 오픈`**;
- that entry points to `/gamenet/sitemap/map/mapstoneage.html`;
- the sitemap page frames `/gamenet/newframe/frstoneage.html`;
- that frame in turn loads both `/gamenet/newframe/contents/stoneage.html` and the dedicated host **`http://stoneage.hananet.net/main.htm`**;
- the dedicated homepage is preserved and exposes menu paths `1.htm`, `2.htm`, `2_2.htm`, `2_3.htm`, `2_4.htm`, and `2_5.htm`, while also linking back to `http://stoneage.enium.co.kr`.

The dedicated menu chain is now materially recovered:

- `1.htm` contains StoneAge descriptive text;
- `2.htm` (archived 2001-02-26) explicitly tells users to insert the **StoneAge CD into the CD-ROM**, after which the installation menu starts automatically; it also instructs users to follow Setup, choose the standard setup mode in normal cases, and states that DirectX 6.1 is required;
- `2_2.htm`, `2_3.htm`, and `2_4.htm` are also replayed;
- `2_5.htm` was recovered identically across five tested replay timestamps (14,455 bytes, SHA-256 `1cd6ed9ce3a943e629358b614fa358f22a84e53dbb988792441658548b171408`) and exposes three Hananet board codes: `GAM2:STAD`, `STAF`, and `STAN`.

The archived **STAD 자료실** page then supplies the strongest Hananet file-level catalog metadata recovered so far. It explicitly says that game-data downloads should be made from the corresponding GameNet game page and lists two StoneAge records, both dated **2001-02-10**:

- record **8119** — `온라인게임 스톤에이지 정식 버전` — **260 M**;
- record **8120** — `온라인게임 스톤에이지 체험 버전` — **240 M**.

The same preserved list snapshot shows view counts of 60,319 for the full-version record and 227,882 for the trial-version record at capture time. The individual record pages currently replay as HTTP 404, so their attachment filenames and final download URLs remain unrecovered. The 260 M full-version entry is close to CNET's 257MB `stoneage.zip`, but the project must not infer byte identity, compression equality, or even identical packaging from approximate size alone.

A separate Hananet PDS H01-detail enumeration extracted 33 catalog record IDs from the archived index, but every detail-page replay failed with HTTP 404 or connection refusal. That path is therefore **archive/capture-inconclusive**, not a negative finding about StoneAge content.

Derived evidence:

- `research/recovered/STONEAGE-HANANET-FRAME-PATHS-R1.txt`;
- `research/recovered/STONEAGE-HANANET-MENU-AVAILABILITY-R1.txt`;
- `research/recovered/STONEAGE-HANANET-MENU-PAGES-R1.txt`;
- `research/recovered/STONEAGE-HANANET-BOARDS-R1.txt`;
- `research/recovered/STONEAGE-HANANET-BOARD-RECORDS-R1.txt`;
- `research/recovered/STONEAGE-HANANET-STAD-ROWS-R1.txt`;
- `research/recovered/STONEAGE-HANANET-PDS-H01-DETAILS-R1.txt`.

### 4a. Exact historical download-root narrowing

Contemporary independent web references now narrow two of the mass-distribution surfaces to exact historical roots:

- **CNET Korea download root:** `http://korea.cnet.com/downloads/`
  - a 2000-04-21 Korean Mac-news post announces the Korean Download.com/CNET service and gives this exact URL;
  - November 2000 site rankings independently list CNet Korea's software-download service at the same root.
- **Hananet software repository root:** `http://pds.hananet.net`
  - November 2000 software-site rankings list the Hanaro/Hananet download repository at this exact root.

These roots are contemporaneous infrastructure evidence. Subsequent archive recovery has now resolved CNET's StoneAge child record and payload path plus Hananet's dedicated StoneAge site and full/trial catalog records; the remaining Hananet gap is the concrete attachment/file URL, while CNET's remaining gap is surviving payload bytes.

### 4a.1. Exact CNET Korea StoneAge download-record identity recovered

A preserved CNET Korea download-index snapshot dated **2000-11-10** contains a direct StoneAge entry:

- label: `Stoneage(스톤에이지)`;
- detail path: `/downloads/File.asp?Platform_Id=1&Software_Id=200009263856`;
- exact record identifier: **`Software_Id=200009263856`**.

A second preserved CNET Korea snapshot dated **2001-01-24** independently lists the same record ID as `스톤에이지(Stoneage)`, confirming that the identifier is stable across at least those two archived index states.

This is the project's first exact child-record identity for one of the named 2000 mass-distribution portals. It upgrades the CNET branch from root-level evidence to a concrete historical software record.

The archived detail record has now resolved two additional payload facts:

- file-size label: **`257MB`**;
- download target parameter: **`/pc/games/online/stoneage.zip`**.

The same detail page links the maker homepage to `http://stoneage.enium.co.kr`. Multiple preserved detail snapshots from 2000-12 through 2001-04 repeat the same payload path and size label. The CNET download counter rises from 234,187 on the 2000-12-01 snapshot to 271,192 on the 2000-12-11 snapshot, independently fitting the contemporary reporting that CNET distribution was already at very large scale by late December.

An exact Wayback Availability probe against both `korea.cnet.com/pc/games/online/stoneage.zip` and the `www` host variant across key 2000-2001 dates returned **zero available payload snapshots** with zero request errors. This is a negative result only for those exact Wayback URL queries; it does not prove the 257MB ZIP is globally lost.

Search caution: `stoneage.zip` is also a common filename for an unrelated 1991 arcade/MAME bootleg. Any future hit must therefore be validated by **257MB-scale size, Korean CNET/Inium provenance, the `/pc/games/online/` path, internal StoneAge client structure, or equivalent file-level evidence** rather than filename alone.

Derived evidence:

- `research/recovered/STONEAGE-KOREA-2000-WAYBACK-AVAILABLE-R1.txt`;
- `research/recovered/STONEAGE-KOREA-2000-WAYBACK-SNAPSHOT-LINKS-R1.txt`.

### 4b. NetPower September/November 2000 scan corroboration

GameMeca's public NetPower scan viewer supplies near-period page images that were probed with transient OCR; only sparse Latin recovery tokens were committed.

September 2000 StoneAge feature, pages 87-96:

- page 92 independently yields `www.hananet.net` in both OCR segmentation modes;
- the same page also yields contemporaneous Korean broadband-provider domains;
- no `.exe`, `.zip`, `.cab`, installer filename or reliable client-size token was recovered.

November 2000 StoneAge preview, pages 99-102:

- page 99 yields `enium` and `Stone Age` / `stoneage` in all three OCR modes;
- one OCR mode yields the partial URL token `http://stoneage`, consistent with the independently documented Inium operator host;
- no installer filename was recovered;
- a single-mode `32MB` token is retained only as OCR evidence and is **not** classified as client size.

Derived reports:

- `research/recovered/STONEAGE-NETPOWER-2000-09-LATIN-TOKENS-R1.txt`
- `research/recovered/STONEAGE-NETPOWER-2000-11-LATIN-TOKENS-R1.txt`

These magazine scans strengthen period attribution of the Inium/Hananet surfaces, but they do not yet advance the project from domain-level to file-token recovery.

### 4c. Follow-up NetPower StoneAge page probes — negative file-token controls

Three later near-period StoneAge article ranges were scanned with the same transient OCR / sparse-token pipeline:

- **NetPower 2000-12, pp.173–176** (StoneAge review): only the cross-PSM title token `Stone Age` was recovered; no URL, domain, archive/installer filename or size token survived.
- **NetPower 2001-01, pp.185–190** (StoneAge preview): no StoneAge URL/archive/installer token was recovered; `32MB` appears in only one OCR mode and remains semantically unresolved, while `titaepowerzine.com` is treated as OCR noise rather than a recovery surface.
- **NetPower 2001-02, pp.189–194** (StoneAge online-travel article): the only stable Latin domain is the magazine-side `powerzine.com`; no Inium/Hananet/CNET or installer/archive token was recovered.

Derived reports:

- `research/recovered/STONEAGE-NETPOWER-2000-12-LATIN-TOKENS-R1.txt`
- `research/recovered/STONEAGE-NETPOWER-2001-01-LATIN-TOKENS-R1.txt`
- `research/recovered/STONEAGE-NETPOWER-2001-02-LATIN-TOKENS-R1.txt`

Operational consequence: these exact article ranges are now low-value repeat targets. Re-run only if a materially better OCR/layout method or a specific visible token justifies it; otherwise return effort to Inium/Hananet/CNET directory/file-name recovery and preserved installation media.

### 5. Pre-service Samsung distribution plan

iNews24, 2000-07-04:

- https://www.inews24.com/view/8928
- records Inium's JSS service contract and planned Korean localization;
- states that distribution was planned through Samsung PC purchasers, Samsung PC education centers and elementary-school Internet classrooms.

Classification: **A/B / contemporaneous pre-launch distribution-plan evidence**.

Do not treat every planned channel as proven byte-identical distribution. The later product-launch article independently confirms a large education-center package supply agreement, strengthening the offline preservation track.


## 2001 near-period installation-media lead — GameTime guide bonus CD

A concrete physical installation-program carrier is independently cataloged by major Korean booksellers:

- title: `스톤에이지 퍼펙트 가이드` / StoneAge Perfect Guide
- publisher/imprint: GameTime
- YES24 publication date: **2001-04-30**
- ISBN-13: **9788995182123**
- ISBN-10: **8995182121**
- media: **CD 1**
- YES24 catalog: https://www.yes24.com/product/goods/199761
- Aladin catalog: https://www.aladin.co.kr/shop/wproduct.aspx?itemid=282190

YES24's surviving catalog description explicitly states that the bonus CD contains:

- a StoneAge installation program; and
- demo-game CD content.

This is stronger than a generic strategy-guide or package lead because the surviving catalog directly identifies an installation program on the included disc.

Evidence boundary:

- the CD contents have not been recovered;
- no installer filename, size, version string, checksum or file tree is known;
- the 2001 guide date does not prove that the installer is identical to the October/December 2000 Inium download;
- the disc may reflect a later patched Korean client state and may contain unrelated demo software alongside StoneAge.

Recovery use:

- search the exact title, ISBNs and `부록 CD` / `설치프로그램` tokens in public ISO/CD preservation catalogs, old Korean magazine/software-CD indexes and library/digital-preservation collections;
- if an image is recovered, inventory only through the standard clean-client acceptance pipeline;
- compare its StoneAge payload against any future Inium/Hananet/CNET copy rather than assuming equality.

Classification: **TARGET-A/B near-period installation-media sub-track**. It is later than the 2000 public-download target but much earlier and more provenance-specific than the 2003 1.74 bridge.

### Public union-library confirmation — RISS / National Library of Korea

RISS now provides a formal bibliographic record for the same GameTime volume:

- RISS permanent link: `https://www.riss.kr/link?id=M10029631`;
- RISS control number: `9b505f870e768aa6ffe0bdc3ef48d419`;
- title: `스톤 에이지 = Stone age`;
- publisher/year: GameTime, Seoul, 2001;
- ISBN-10: `8995182121`;
- physical description: **318 pages + 1 compact disc (12 cm)**;
- series: `퍼펙트 가이드; vol.5`;
- listed holding institution: **National Library of Korea (국립중앙도서관)**;
- table of contents begins with a dedicated `설치하기` / installation section.

This upgrades the bonus-CD lead from retailer-only marketing metadata to a formal public-library bibliographic object. It does **not** yet prove that the accompanying disc is presently intact, independently cataloged, digitized, or publicly downloadable at the holding institution.

### Catalog-date normalization

The known commercial catalogs disagree on the date while identifying the same physical book:

- Aladin: `2001-01-01`, 318 pages, ISBN-13 `9788995182123`;
- YES24: `2001-04-30`, 318 pages, ISBN-13 `9788995182123`, CD 1;
- RISS: year `2001`, ISBN-10 `8995182121`, 318 pages + 1 compact disc.

Because the identifiers and pagination converge, these are treated as **catalog-date variants for one bibliographic object**, not evidence for two separate StoneAge guides or two different bonus CDs.

Recovery consequence:

- stop branching the search into a hypothetical January edition versus April edition unless a genuinely different ISBN/edition statement appears;
- prioritize public National Library / union-catalog metadata for the accompanying disc: accession/control fields, call number, supplementary-material status, disc-label images or a distinct non-book record;
- continue public preservation searches by ISBN and RISS control identifiers, but do not contact institutions or make physical acquisition a project dependency.

### GameTime CD public-archive metadata probe

A reproducible Internet Archive metadata-only probe queried:

- both ISBNs;
- Korean and English title variants;
- GameTime + StoneAge title/description combinations;
- `StoneAge Perfect Guide` variants.

Result: all five queries returned **0 items** at the time of the probe.

Derived report:

- `research/recovered/STONEAGE-GAMETIME-2001-CD-ARCHIVE-METADATA-R1.txt`.

Interpretation:

- this is a valid negative result for those exact **Internet Archive metadata queries**;
- it is **not** evidence that the physical CD no longer survives or that no unindexed/private-to-public preservation copy exists;
- do not repeat the same IA metadata queries unless new title/identifier/file tokens are discovered.

## Provenance interpretation

### What can be claimed

- A Korean StoneAge client was publicly distributed by the licensed local operator in 2000.
- The official Inium site was one distribution/service surface.
- Hananet and CNET were high-volume download surfaces by December 2000.
- Physical/package distribution also existed at material scale.
- This target predates the currently tracked Korean 1.74 / Japanese 1.74a targets by roughly three years.

### What cannot yet be claimed

- exact public version number of the 2000 client;
- installer filename, file size, hash or complete file tree;
- exact historical Hananet or CNET StoneAge URL;
- byte identity between the Inium, Hananet, CNET and packaged copies;
- byte identity with JSS Japan;
- absence of Korean localization/operator changes.

## Clean-client classification

Operational status: **TARGET-A**.

Rationale:

- licensed operator-era distribution is directly attested;
- public/free distribution is directly attested;
- multiple contemporary mirror channels are directly attested;
- distribution volume was extremely high, increasing the probability of surviving copies;
- no recovered bytes are currently available, so the target cannot yet be graded RECOVERED-A/B.

The Korean localization is not a purity defect by itself. If an operator-distributed Korean 2000 client is recovered intact, it can be a clean Korean bridge specimen while still being distinct from the JSS Japanese baseline.

## Recovery search keys

Highest-value exact search surfaces now are:

- `www.stoneage.enium.co.kr` historical download pages / link dumps;
- Hananet / `game.hananet.net` / GamePlus plus the exact software repository root `http://pds.hananet.net` around late 2000;
- CNET Korea exact download root `http://korea.cnet.com/downloads/`, then any surviving StoneAge child path/file token;
- Korean software-download catalogs and antivirus/file indexes retaining original filenames;
- magazine / ISP / PC-education-center CD indexes;
- Samsung PC education-center / MenTech package references;
- old personal FTP mirrors, web directories and link collections that copied the original portal filename;
- preservation communities holding pre-Netmarble Inium installations.

Search must prioritize **filename/path recovery** over more general history articles. Once a plausible filename or original mirror URL appears, search by that exact token across archives and mirrors.

## Inium archived-root resource boundary

The preserved Inium root snapshot explicitly embeds **`main.swf`**, making that SWF a concrete historical site-resource path. However:

- Wayback Availability returns zero snapshots for both bare and `www` `main.swf` URL variants across the tested 2000-2001 dates;
- direct replay at the known root-page timestamps **2000-11-09 15:31:00** and **2001-02-01 07:28:00** returns HTTP 404 for both host variants;
- no SWF bytes or embedded download tokens were recovered.

Therefore the root HTML proves the historical `main.swf` reference, but the SWF itself is currently **unrecovered** and should not be treated as an available archive asset.

Derived evidence: `research/recovered/STONEAGE-INIUM-MAIN-SWF-TOKENS-R1.txt`.

## Archive-probe interpretation

Two automated metadata-only probes were run against public web archives:

- Internet Archive / Wayback CDX: `research/recovered/STONEAGE-KOREA-2000-ARCHIVE-PATH-PROBE-R1.txt`;
- Arquivo.pt: `research/recovered/STONEAGE-KOREA-2000-ARQUIVOPT-PROBE-R1.txt`.

Both currently return zero usable records **only after request-level timeout/network errors**. The zero counts are therefore **INCONCLUSIVE**, not evidence that the sites were never archived.

Operational rule:

- do not cite either zero count as a negative preservation result;
- retry through other archive endpoints/environments only when useful;
- meanwhile prioritize indexed historical pages, filename tokens, magazine/software-CD catalogs and surviving mirror references.

## Acceptance test if bytes are recovered

Immediately stop broad searching long enough to record:

1. source URL / archive chain and retrieval provenance;
2. archive/installer SHA-256 and size;
3. full file tree and per-file hashes;
4. PE timestamps/resources/version strings for executables;
5. operator/server/update endpoints;
6. launcher/updater structure;
7. REAL/ADRN/SPR/SPRADRN generations;
8. map/resource formats;
9. contamination indicators such as private-server endpoints, injected launchers or later patchers;
10. cross-copy hashes if more than one Inium/Hananet/CNET/package copy is found.

Only byte comparison can determine whether the parallel distribution channels carried one identical client image or different update states.

## Relation to other targets

- **JSS 1999 beta/retail:** remains the historical origin target, but current public byte recovery is blocked.
- **Korean Inium 2000:** now the highest-priority operational clean-client bridge search because it is early, officially distributed and massively replicated.
- **Korean 1.74 (2003):** remains an exact-version TARGET-A, useful if 2000 bytes remain unavailable.
- **Japanese 1.74a (2003):** remains a strong official free-beta TARGET-A.
- **2.5 pure-client preservation thread:** remains a useful later clean-client lead, but is later than the 2000 Inium target.
- **mixed recovered 2.5 bundle:** remains a resource-format bridge only, not a clean runtime baseline.

## Open questions

- What exact filename did Inium distribute from its official site in October/December 2000?
- What exact StoneAge page/path or file token did Hananet/GamePlus / `pds.hananet.net` use?
- What StoneAge child path/file token existed beneath the now-resolved CNET Korea root `http://korea.cnet.com/downloads/`?
- Did Hananet/CNET mirror a complete installer or a patch/bootstrapper?
- Did the 60,000 education-center packages use the same client state as the online mirrors?
- Can a surviving Inium installation be dated before later 1.74 updates from executable/resource evidence?