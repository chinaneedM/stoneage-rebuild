# StoneAge Korea physical-carrier holder leads — R1

Retrieval date: 2026-09-19

## Purpose

This record tracks concrete surviving physical-media / collector lanes that could recover Korean 2000–2001 client bytes when original download endpoints and web archives fail. No carrier bytes are committed here.

## Lead A — active Korean classic-CD collector

A public DCInside post mirrored into the realtime-best board on 2025-12-04 documents an active collector using the public handle `Baram (stem1228)`. The post states that the collector physically extracted classic CDs, including magazine supplement discs and old online-game clients, and was considering how to share the extracted files.

Public post:
https://gall.dcinside.com/board/view/?id=dcbest&no=385548

The published inventory explicitly includes both supplement discs from **NetPower 2000-10**. Their listed online-game contents include Lineage, Dark Saver, Game Everland, Hellbreath, Millennium, Destiny, Last Kingdom 1/2, Mir의 전설, 행복동, Tactical Commanders, 유리도시, Gadius, RedMoon, WarBible, JoyCity, Majesty, Metin, Millennium Meeting, Shaiya, Slayers, Fortress 2 and 영웅문. **StoneAge is not listed on those two 2000-10 discs.**

This is still a high-value acquisition lead because the same holder demonstrably preserves the exact publication family and adjacent date range we need.

## Lead B — exact NetPower StoneAge issue targets

The surviving NetPower contents index / GameMeca magazine archive places StoneAge in these issues:

- **2000-09** — game feature, p.87.
- **2000-11** — preview, p.99.
- **2000-12** — review, p.173.
- **2001-01** — preview, p.185.
- **2001-02** — online-game feature, p.189.

Public index:
https://bihon.tistory.com/entry/Net-POWER-%EC%A0%84%EC%B2%B4-%EB%AA%A9%EC%B0%A8-%EB%B0%9C%ED%96%89%EC%88%9C-2020-05-19-%EA%B8%B0%EC%A4%80

GameMeca exposes surviving scanned magazine issues, including 2000-12 and 2001-02:
https://m.gamemeca.com/magazine.php?mgz=netpower&ym=2000_12
https://m.gamemeca.com/magazine.php?mgz=netpower&ym=2001_2

The article presence does **not** prove the supplement CD contains a StoneAge installer. Each supplement disc must be independently inventoried.


## Public Internet Archive carrier resolution — 2026-09-19

Uploader-neighborhood enumeration of the already-known Korean magazine-disc preservation corpus exposed exact public NetPower items for three of the StoneAge-adjacent issues:

- `netpower_cd_2000_09`
- `netpower_cd_2000_11`
- `netpower_cd_2001_02`

Each item contains two disc volumes represented in both IMG and ISO form. The repository's bounded HTTP-Range scanner recursively enumerated both ISO-9660 and Joliet directory namespaces without downloading complete images.

Results:

- **2000-09:** 4 image representations scanned, 0 errors, 0 truncation, 0 StoneAge-path hits.
- **2000-11:** 4 image representations scanned, 0 errors, 0 truncation, 0 StoneAge-path hits.
- **2001-02:** 4 image representations scanned, 0 errors, 0 truncation, 0 StoneAge-path hits.
- Existing **2001.12** control: 2 public ISO images scanned, likewise 0 StoneAge-path hits.

These results apply to the exact preserved carrier images only. They do not prove that no alternate pressing, replacement disc, private collector copy, or different distribution channel carried StoneAge.

A corrected metadata-only R2 probe then searched the two known preservation-uploader neighborhoods plus exact global Internet Archive identifier/title/description forms for **NetPower 2000-12** and **2001-01**. Both returned **0 exact carrier items with 0 query errors**. Treat this as a current IA-route negative, not a global absence claim.

Derived evidence:

- `research/recovered/STONEAGE-NETPOWER-2000-09-DISC-SCAN-R1.txt`
- `research/recovered/STONEAGE-NETPOWER-EXACT-TARGET-DISC-SCAN-R1.txt`
- `research/recovered/STONEAGE-NETPOWER-IA-UPLOADER-NEIGHBORHOOD-R2.txt`

## Lead C — broader Korean game-media preservation corpus

A 2026-08-31 Lost Media Gallery recovery post for another Korean online game reports that its researcher had already inspected:

- 33 NetPower supplement CDs;
- 49 GamePia / PC Game Magazine supplement CDs;
- seven Korean-game preservation accounts on Archive.org, totaling more than 70,000 items.

Public post:
https://gall.dcinside.com/mgallery/board/view/?id=lostmedia&no=80066

The post does not identify all 33 NetPower issue dates or the seven Archive.org account names, so it is evidence that a broader preservation corpus exists, **not** evidence that a StoneAge carrier has already been checked.

## Lead D — GameTime StoneAge guide disc

YES24's surviving bibliographic/product record for the GameTime `StoneAge Perfect Guide` (ISBN13 `9788995182123`, published 2001-04-30) explicitly describes **one included CD** and says the supplement contains a StoneAge installation program / demo-game CD.

Public record:
https://www.yes24.com/product/goods/199761

This is a direct physical-carrier recovery target. A surviving copy with its original disc can potentially bypass lost Hananet/GameTime web downloads.

## Acquisition / verification order

1. Do **not** reacquire or rescan the exact public NetPower 2000-09 / 2000-11 / 2001-02 carrier images unless a new technical question requires byte-level comparison; their directory-level StoneAge search is closed.
2. Determine whether **NetPower 2000-12 or 2001-01** supplement media survives in the active collector/community corpus or in a preservation account not exposed by the current IA metadata searches.
3. Locate an intact **GameTime StoneAge Perfect Guide** copy with the original supplement CD and image that disc losslessly; this remains the strongest physical-carrier target because the product record explicitly describes StoneAge install/demo content.
4. On any newly recovered carrier, search exact known distribution tokens first:
   - `stoneage.zip`
   - `sa.exe`
   - `sa_demo.exe`
   - `stone_demo.exe`
   - `onlStoneAge.zip`
   - `stoneagebeta.zip`
5. If a candidate installer/client is recovered, immediately run the repository clean-client acceptance workflow: provenance, hashes, full tree, executable metadata, server endpoints, resources and contamination analysis.

## Evidence status

**OPEN / HIGH-VALUE PHYSICAL-MEDIA RECOVERY LANE.**

No 2000–2001 StoneAge client bytes were recovered by this pass. The public NetPower 2000-09 / 2000-11 / 2001-02 carriers are now closed as exact directory-level negatives, while 2000-12 / 2001-01 remain unresolved outside the current IA metadata surface. The living collector/preservation ecosystem and the GameTime guide CD therefore remain active acquisition paths.
