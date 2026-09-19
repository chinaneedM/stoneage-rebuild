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

This corroborates the portal family named in the December StoneAge article, but does **not** yet identify StoneAge's exact historical Hananet page or download URL.

### 5. Pre-service Samsung distribution plan

iNews24, 2000-07-04:

- https://www.inews24.com/view/8928
- records Inium's JSS service contract and planned Korean localization;
- states that distribution was planned through Samsung PC purchasers, Samsung PC education centers and elementary-school Internet classrooms.

Classification: **A/B / contemporaneous pre-launch distribution-plan evidence**.

Do not treat every planned channel as proven byte-identical distribution. The later product-launch article independently confirms a large education-center package supply agreement, strengthening the offline preservation track.

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

- `stoneage.enium.co.kr` historical download pages / link dumps;
- Hananet / `game.hananet.net` / GamePlus StoneAge pages around late 2000;
- CNET Korea StoneAge download pages around late 2000;
- Korean software-download catalogs and antivirus/file indexes retaining original filenames;
- magazine / ISP / PC-education-center CD indexes;
- Samsung PC education-center / MenTech package references;
- old personal FTP mirrors, web directories and link collections that copied the original portal filename;
- preservation communities holding pre-Netmarble Inium installations.

Search must prioritize **filename/path recovery** over more general history articles. Once a plausible filename or original mirror URL appears, search by that exact token across archives and mirrors.

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
- What exact StoneAge page/path did Hananet/GamePlus use?
- Which Korean CNET domain/path hosted the 310,000-download mirror?
- Did Hananet/CNET mirror a complete installer or a patch/bootstrapper?
- Did the 60,000 education-center packages use the same client state as the online mirrors?
- Can a surviving Inium installation be dated before later 1.74 updates from executable/resource evidence?