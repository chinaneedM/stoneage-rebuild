# Source Registry Supplement — JSS Physical Media R1

Date: 2026-09-18

Purpose: register later photographic preservation relevant to the 1999 JSS retail package without silently promoting community captions or collector attribution to first-party fact.

The canonical research analysis for this source group is `research/clients/JSS-RETAIL-PACKAGE-PHOTO-EVIDENCE-R1.md`.

## Evidence rule

- A later collector photograph can support **what is visibly present in the photograph**, but does not by itself establish complete package provenance, original bundling, disc contents, or date.
- Collector captions are separate claims from the photographed artifact and receive lower weight when they conflict with visible publisher/branding evidence.
- The 1999 JSS retail-media model must continue to distinguish the normal game/install CD from the separately advertised initial-edition bonus/special CD until a provenance-preserving original package inspection or first-party contents list establishes the exact layout.
- Proprietary disc images/binaries are not to be committed to this repository; if recovered, store only hashes, metadata, file-tree/PE analysis and derived findings unless repository policy changes.

## SRC-JP-1999-RETAIL-COLLECTOR-PHOTO-01

- Title: `石器时代，石器周边收藏——日版客户端礼盒` / mirrored collector article
- Collector-post lineage: at least July-August 2020; exact first publication in the repost chain remains unresolved
- Retrieval date: 2026-09-18
- Language/region: Chinese-language community preservation / photographed Japanese package
- Source type: later collector photographs and community narrative
- Accessible mirror: https://blog.shiqim.com/shiqi2559.html
- Related Bahamut repost: https://forum.gamer.com.tw/C.php?bsn=1571&snA=81377
- Image URLs used:
  - JSS box/front and manual: https://www.shiqi.club/zb_users/upload/2020/08/20200804212101_44439.jpg
  - JSS package contents spread: https://www.shiqi.club/zb_users/upload/2020/08/20200804212101_44867.jpg
  - period initial-edition advertisement image: https://www.shiqi.club/zb_users/upload/2020/08/20200804212102_40031.jpg
- Confidence: **C overall** for historical package provenance/bundling; useful photographic corroboration for literal visible details
- Visible artifact observations:
  - a JSS/Gamer's Dream-era `STONEAGE` Windows 95/98 box and matching manual are shown;
  - the contents-spread photograph shows **two physically distinct optical discs** alongside the box/manual and registration-related paper items;
  - one disc uses the illustrated StoneAge game-package visual treatment, while the second disc has a visibly different yellow/blue label design;
  - the associated advertisement image states `99年10月15日発売!!`, Windows 95/98, price 8,800 yen, and `初回限定「STONEAGEボーナスCD」付き!!（限定5000本）`.
- Cross-corroboration already present in the repository:
  - the archived first-party JSS manual independently says the normal retail install used a StoneAge **game CD**;
  - the contemporaneous retail advertisement independently advertises an initial-edition **bonus/special CD**;
  - the surviving Mercari first-edition listing independently claims that an unopened initial limited edition contains a bonus CD-ROM.
- Research consequence:
  - the working model of a normal game/install CD **plus a separate initial-edition bonus CD** is now materially stronger than before because a later physical-package photograph depicts two separate discs next to the early JSS box/manual;
  - this is still **not S-grade proof** of exact original package layout because the project has not directly inspected the pictured object or established an unbroken provenance chain.
- Does not establish:
  - that every pictured loose item originated from the same sealed retail box;
  - exact disc count for every standard or initial-edition production run;
  - exact label/matrix identifiers of either disc;
  - filesystem contents, audio tracks, hashes or executable versions;
  - product/JAN code;
  - exact identity/content of the yellow/blue disc beyond its being a visibly separate optical disc in the photograph.
- Promotion criterion:
  - direct provenance-preserving inspection of an original 1999 JSS package, first-party package-contents documentation, or a verified dump/photo set exposing labels, matrix identifiers and package/back-box identifiers.

## SRC-JP-1999-RETAIL-MERCARI-IMAGE-SET-01

- Parent listing: `SRC-JP-1999-RETAIL-MERCARI-01`
- Listing title: `日本システムサプライ STONEAGE 初回限定版 マグカップ マウスパッド`
- Listing URL: https://jp.mercari.com/item/m44997025885
- Retrieval date: 2026-09-18
- Source type: marketplace listing plus enumerated original-image href targets
- Current listing state: **sold**; the page exposes `1 / 13`, i.e. thirteen listing photographs.
- Seller text preserved by the live listing states:
  - the `STONEAGE` package is an unopened initial limited edition;
  - an initial-edition bonus CD-ROM is inside;
  - the seller speculates that BGM might still be listenable from that disc; this is explicitly treated as **seller speculation**, not evidence that the disc is audio-only, contains specific BGM tracks, or has any particular session/layout;
  - the accompanying mouse pad is attributed by the seller to Tokyo Game Show 1999;
  - the mug is attributed by the seller to a visit to the company.
- Confidence: **C** for seller provenance/bundling claims; potentially high visual value if the original photo bodies can be preserved and inspected.
- Exact original-image hrefs exposed by the listing page:
  1. `https://static.mercdn.net/item/detail/orig/photos/m44997025885_1.jpg?1745193251=`
  2. `https://static.mercdn.net/item/detail/orig/photos/m44997025885_2.jpg?1745193251=`
  3. `https://static.mercdn.net/item/detail/orig/photos/m44997025885_3.jpg?1745193251=`
  4. `https://static.mercdn.net/item/detail/orig/photos/m44997025885_4.jpg?1745193251=`
  5. `https://static.mercdn.net/item/detail/orig/photos/m44997025885_5.jpg?1745193251=`
  6. `https://static.mercdn.net/item/detail/orig/photos/m44997025885_6.jpg?1745193251=`
  7. `https://static.mercdn.net/item/detail/orig/photos/m44997025885_7.jpg?1745193251=`
  8. `https://static.mercdn.net/item/detail/orig/photos/m44997025885_8.jpg?1745193251=`
  9. `https://static.mercdn.net/item/detail/orig/photos/m44997025885_9.jpg?1745193251=`
  10. `https://static.mercdn.net/item/detail/orig/photos/m44997025885_10.jpg?1745193251=`
  11. `https://static.mercdn.net/item/detail/orig/photos/m44997025885_11.jpg?1745193251=`
  12. `https://static.mercdn.net/item/detail/orig/photos/m44997025885_12.jpg?1745193251=`
  13. `https://static.mercdn.net/item/detail/orig/photos/m44997025885_13.jpg?1745193251=`
- Retrieval limitation in the current environment:
  - the listing page exposes the exact original-image URLs;
  - each of the thirteen direct original-image requests currently returns **HTTP 403 Forbidden** through the available extraction path;
  - therefore no additional model/type code, disc label or matrix code has been read from these thirteen images in this pass.
- Research consequence:
  - this sold listing is no longer an active acquisition route, but it is now a concrete **photo-preservation target set** rather than a generic inaccessible marketplace lead;
  - future work should attempt preservation through another browser/archive/network path before the static image objects disappear;
  - if a public cache/mirror of any of the thirteen photographs exposes a back box, disc face or package side at readable resolution, it could still reveal the missing model/type code, disc label or matrix fields without requiring the physical object; the retail JAN itself is already resolved independently.
- Does not establish:
  - authenticity of every listed accessory association;
  - exact sealed-box contents without opening/direct inspection;
  - that the seller's bonus-CD statement identifies which photographed disc is the bonus disc;
  - any filesystem, binary, checksum or matrix-code fact.

## SRC-JP-1999-RETAIL-YAHOO-UNOPENED-01

- Title: `未開封 ストーンエイジ`
- Auction ID: `k1131932809`
- Listing URL: https://auctions.yahoo.co.jp/jp/auction/k1131932809
- Listing period: 2024-04-09 through 2024-04-13
- Retrieval date: 2026-09-18
- Source type: preserved Yahoo! Auctions photographs of a seller-described unopened early JSS StoneAge package
- Confidence: **B for literal visible package fields; C for seller provenance/unopened-status claim**
- Visible observations:
  - front/side/back photographs show the early JSS/Gamer's Dream `STONEAGE` Windows 95/98 package;
  - the front visibly carries initial-edition promotional marking;
  - the back carries Japan System Supply branding and a readable retail barcode;
  - the barcode reads **`4909476303010`**.
- Original image URLs:
  1. side: https://auctions.c.yimg.jp/images.auctions.yahoo.co.jp/image/dr000/auc0504/users/93c224e074220661380e6f1f93b2056799fea6be/i-img640x480-1712642690euuwgk18923.jpg
  2. front: https://auctions.c.yimg.jp/images.auctions.yahoo.co.jp/image/dr000/auc0504/users/93c224e074220661380e6f1f93b2056799fea6be/i-img640x480-1712642690ufdbie13619.jpg
  3. back/barcode: https://auctions.c.yimg.jp/images.auctions.yahoo.co.jp/image/dr000/auc0504/users/93c224e074220661380e6f1f93b2056799fea6be/i-img640x480-1712642690dlqgj723.jpg
- Research consequence:
  - the direct StoneAge retail JAN is now **`4909476303010`**, replacing the prior state in which this number existed only as an inferred search candidate;
  - this public back-box image closes the product/JAN sub-question without requiring acquisition of the physical object.
- Does not establish:
  - package model/type code;
  - the exact contents of the sealed package;
  - disc label/matrix identifiers or which optical disc is the normal game CD versus bonus CD;
  - filesystem contents, hashes, PE metadata or S-grade chain of custody.

## SRC-JP-2003-BOTHTEC-PACKAGE-COLLECTOR-PHOTO-01

- Title: later Japanese `STONEAGE` revival package shown in the same collector article
- Artifact period: post-JSS Japanese revival; visible publisher branding identifies Bothtec / DigiPark
- Retrieval date: 2026-09-18
- Source type: later collector photographs
- Image URLs used:
  - package front: https://www.shiqi.club/zb_users/upload/2020/08/20200804212102_55304.jpg
  - package back: https://www.shiqi.club/zb_users/upload/2020/08/20200804212103_81869.jpg
  - game-ticket/disc photo: https://www.shiqi.club/zb_users/upload/2020/08/20200804212111_77118.jpg
- Confidence: **B for visible publisher/product-label details; C for the collector narrative around it**
- Visible artifact observations:
  - package front visibly carries **BOTHTEC** and DigiPark branding, not Japan System Supply branding;
  - supported OS list is Windows 98SE/Me/2000/XP, which is incompatible with treating this box as a 1999 JSS launch artifact;
  - the back shows product code `WR-04156` and barcode `4988609011565`;
  - the package-back contents panel explicitly lists **2 game CDs**, **2 game tickets**, a manual and a plush strap;
  - the publicly replayable disc photograph independently carries `STONEAGE`, `CD-ROM`, Windows 98SE/Me/2000/XP, DigiPark, BOTHTEC and **`WR-04156` on the disc face itself**;
  - no reliable Disc 1/Disc 2 ordinal, matrix/mastering string or IFPI code is readable in the current photograph, so the two included CDs must not be assumed byte-identical or content-identical;
  - the adjacent photographed 30-day ticket contains an activation credential; that credential is intentionally not transcribed into the repository because it is irrelevant to media identification.
- Source-quality warning:
  - the community article describes its two Japanese packages as JSS-issued packages, but the second package is visibly a **Bothtec/DigiPark** product.
  - Therefore the article's captions cannot be treated as authoritative provenance; each photographed artifact must be classified from its own visible evidence.
- Relevance to the 1999 track:
  - this package is **not** evidence for the 1999 JSS retail disc layout;
  - it is useful mainly as a control showing why later collector narratives must be decomposed into artifact-level evidence.

## Source-group conclusion

**HYPOTHESIS — strongly corroborated, not yet S-grade:** the 1999 JSS initial-edition retail package contained a normal game/install CD and a separate bonus/special CD.

Support now comes from three independent evidence types:

1. first-party archived JSS manual: normal installation from a **game CD**;
2. contemporaneous advertising: initial-edition **STONEAGE bonus CD**;
3. later physical-package photography: two visibly separate optical discs shown with the early JSS box/manual.

The remaining gap is no longer merely whether a second disc probably existed. The high-value unresolved questions are now the exact identity, label/matrix code and contents of each disc; the package model/type code; and a provenance-preserving publicly obtainable dump/file tree of the actual 1999 game disc.


## SRC-CN-2002-SA25-WANFANG-DISC-PHOTO-01

- Title visible on disc: `永远的石器时代 2.5 精灵王传说`
- Publisher imprint visible on disc: **万方数据电子出版社**
- Visible ISBN: **`7-900096-07-8/Z.03`**
- Visible barcode: **`9787900096074`**
- Public collector image/source surface: https://www.shiqi.me/pt_17.htm
- Retrieval/research date: 2026-09-24
- Source type: later public collector photograph of physical optical media
- Confidence: **B for literal visible disc-face fields; D for exact payload/provenance beyond the photograph**
- Corroborating survival evidence:
  - a separate collector article states that the author retained StoneAge installation discs for versions 2.5, 3.0, 4.0 and 5.0: https://post.smzdm.com/p/462347/
- Exact preservation-index result:
  - DiscMaster / Internet Archive queries using ISBN, barcode, title and publisher variants produced **0 strict preservation hits** and **0 interesting media-file hits**, with **0 probe errors**;
  - one raw DiscMaster ISBN result was inspected and is an unrelated Brockhaus Multimedia 2007 update file, not StoneAge media.
- Does **not** establish:
  - that this is the client CD included in Beijing-Waei's `新手报到包`, `春满钱坤包` or `延年益兽包`;
  - that the disc contains the full 575/580 MB client rather than the 8.25 MB updater, guide/multimedia content, or another composition;
  - any filesystem tree, volume label, installer filename, binary hash or map-cache provenance.
- Promotion criterion:
  - a provenance-preserving disc image/read-only file tree, or independent package documentation tying the same ISBN/barcode disc to a specific Beijing-Waei distribution package.
- Derived evidence record: `research/clients/STONEAGE-SA25-WANFANG-DISC-R1.md`
- Derived index report: `research/recovered/STONEAGE-SA25-WANFANG-DISC-PROBE-R1.txt`

## SRC-CN-2001-BOMBING-CHICKEN-COLLECTOR-CATALOG-01

- Later collector-catalogue entry: **`2001C226 哇靠轰炸鸡完美中文版`**
- Preserved catalogue attributes: approximately **210M**, shooting genre, literal publisher string **`华议国际`**
- Confidence: **C for literal later-catalogue metadata; D for StoneAge/Waei payload provenance**
- Evidence boundary:
  - `华议国际` is retained literally and is **not** silently normalized to `华义国际`;
  - the catalogue-local ID `2001C226` is not an official publisher/product code unless independently proven;
  - expanded CHM/RTF scanning found no StoneAge Online / `精灵王传说` / `StoneAge` catalogue item on the tested surface.
- Torrent-metadata crosscheck:
  - public `allseeds.zip` contained **89** torrent metadata entries;
  - corrected target-identity R2 classification produced **0 exact target strong hits / 81 weak catalogue-neighborhood hits / 0 errors**;
  - the R1 `总第280期` strong result was an unrelated `读者` magazine issue and is explicitly rejected as a false positive;
  - a separate signature scan produced **0 exact client/resource signature paths / 0 multi-exact client candidates / 5 lexical paths / 0 errors**;
  - those lexical paths do not identify a client: they include historical-era material, a same-name mini-game and the secondary-documentation filename `大软石器时代特刊纪念册.pdf`.
- Operational consequence:
  - the tested collector catalogue/torrent surface is bounded for client-media recovery under the current exact identities/signatures;
  - reopen only from a new exact image filename, checksum, catalogue record, package identity, installed-tree signature or independent repost.
- Derived reports:
  - `research/recovered/STONEAGE-SA25-OLD-DISC-CATALOG-NEIGHBORHOOD-R4.txt`
  - `research/recovered/STONEAGE-SA25-OLD-DISC-TORRENTS-R2.txt`
  - `research/recovered/STONEAGE-OLD-DISC-TORRENT-SIGNATURES-R1.txt`

## SRC-CN-COLLECTOR-SA25-DISC-CLASSIFICATION-01

- Source family: StoneAge collector posts by `stoneage2017 / 寂寞如風`, preserving photographs and source-type descriptions for mainland/Taiwan client, magazine and guide-book discs.
- Primary pages:
  - `https://forum.gamer.com.tw/C.php?bsn=1571&snA=81429` — `石器時代華義國際石器周邊收藏光碟篇（二）`, 2021-01-07;
  - `https://forum.gamer.com.tw/C.php?bsn=1571&snA=81428` — `光碟篇（三）`, 2021-01-07;
  - `https://forum.gamer.com.tw/C.php?bsn=1571&snA=81388` — `延年益壽包`, 2020 collector post;
  - `https://forum.gamer.com.tw/C.php?bsn=1571&snA=81400` — `2.5精靈王傳說版用戶端產包`, 2020-09-21.
- Source type: later specialist collector photography + first-hand collection classification, not contemporaneous operator documentation.
- Confidence: **C+ for collector source-type classification; B for literal claims tied to the photographed items as described; not S/A provenance for client bytes.**
- Supports:
  - the collector explicitly separates StoneAge optical media into **official client discs, magazine-gift discs and strategy-book-gift discs**, with mainland/Taiwan variants;
  - for the **2.5 精靈王傳說** segment, the collector identifies the upper pictured disc as the **mainland client unified-artwork disc** and the lower pictured disc as the Taiwan version;
  - the collector states mainland versions generally reused a standardized client-disc presentation, with 2.0 as a noted exception in that collection;
  - the `延年益壽包` post independently shows/labels a **2.5-period disc** and a 2.5 manual;
  - the 2.5 client-package post records multiple Waei-era new-user-package cover variants plus the `延年益壽包` and `春滿乾坤包` families;
  - a separate collector post states some mainland strategy-book discs are still simply **client installer packages**, while retaining a different provenance class from official boxed-client media.
- Archaeology consequence:
  - physical-media recovery now requires a **carrier-class field** before clean-client promotion: official boxed client / magazine-gift / strategy-book-gift / other publisher / unknown;
  - non-official carrier class does **not** make the bytes technically useless: a magazine/guide disc may still preserve an unmodified installer, but its provenance grade is lower and must be compared against an official/operator anchor before promotion;
  - the Wanfang ISBN/barcode disc cannot be called an official Beijing-Waei 2.5 client merely from its 2.5 title. Its artwork/carrier relation must be matched against the collector's mainland unified-client-disc baseline or tied independently to a specific Waei package.
- Does not establish:
  - byte identity between any photographed discs;
  - the Wanfang disc's carrier class;
  - filesystem contents, hashes, mastering/matrix identifiers, or whether a secondary carrier contains the 575/580 MB full client versus the 8.25 MB updater.


## SRC-CN-2026-SA25-PHYSICAL-IMAGE-LINEAGE-01

- Source type: derived visual-fingerprint analysis over public marketplace/collector photographs; image bodies read transiently, metrics only retained.
- Retrieval/research date: 2026-09-24.
- Derived report: `research/recovered/STONEAGE-SA25-PHYSICAL-IMAGE-FINGERPRINTS-R2.txt`.
- Canonical interpretation: `research/clients/STONEAGE-SA25-PHYSICAL-IMAGE-LINEAGE-R1.md`.
- Evidence set:
  - Ruten boxed/new-user-package item `22632305238624` — 9 full-size images;
  - Ruten standalone-disc items `21926883918096`, `22242541948520` — 1 full-size image each;
  - Wanfang collector page `https://www.shiqi.me/pt_17.htm` — 3 large recoverable images.
- Strong deduplication result:
  - standalone Ruten item images have different file hashes but match at **1,605 ORB / 1,538 good<=64 / 743 RANSAC inliers / 0.4831 inlier ratio**;
  - operational classification: **one visual-source cluster**, not two independent physical-media observations.
- Other tested relations:
  - best boxed-vs-standalone whole-frame match: **50 inliers / 0.0472**;
  - best Ruten-vs-Wanfang whole-frame match: **27 inliers / 0.0322**.
- Evidence boundary:
  - a weak whole-frame match cannot prove different disc artwork because packaging/crop/occlusion can suppress feature overlap;
  - a strong photograph-level match does not prove byte identity or that two sellers held the same physical object;
  - Wanfang remains OPEN / UNCLASSIFIED-CARRIER;
  - the known mainland unified-client reference was not recoverable during R2 and therefore has no match conclusion.
- Archaeology consequence:
  - marketplace URLs must be deduplicated by visual-source lineage before being counted as independent survival evidence;
  - next visual step is crop/local-region comparison and restoration of a usable official/mainland collector reference.



## SRC-CN-2026-SA25-DISC-REGION-MATCH-01

- Source type: derived local-region visual comparison over public Ruten/Wanfang/collector photographs; image bodies transient only.
- Research date: 2026-09-24.
- Derived report: `research/recovered/STONEAGE-SA25-DISC-REGION-MATCH-R1.txt`.
- Positive-control relation:
  - the two standalone Ruten disc images yield **231 SIFT/RANSAC inliers / 0.7966 inlier ratio**, with broad inlier coverage and a sane homography.
- Boxed-package relation:
  - strongest standalone-to-boxed image pair yields **32 inliers / 0.3107**, but only **0.0747** query coverage / **0.0394** target coverage;
  - another query direction yields **22 inliers / 0.2619** with broader coverage.
  - classification: **shared local visual features, insufficient for same-disc-artwork promotion**.
- Wanfang relation:
  - best standalone-to-Wanfang row reaches **21 inliers / 0.2727**, but query coverage is **0.0030** with an invalid/exploded projected homography;
  - classification: **no robust local artwork linkage established**.
- Collector false-positive guard:
  - apparent 95–99-inlier rows with near-zero target coverage and invalid quadrilaterals are explicitly rejected as degenerate local-feature matches.
- Archaeology consequence:
  - whole-frame and local-region metrics agree that the two standalone listings are one visual cluster;
  - the boxed new-user package cannot yet be promoted into that cluster;
  - Wanfang remains an independent visual-source / unclassified-carrier lead.
- Does not establish disc-byte identity, mastering identity, exact carrier provenance, filesystem contents or clean-client status.


## SRC-CN-2002-POPSOFT-SA25-COVERDISC-BOUNDARY-01

- Contemporaneous named carrier: **`《大众软件CD——大众游戏》2002年2月号`**, from the surviving 17173 StoneAge 2.5 upgrade/distribution page.
- Public preservation object inspected: Internet Archive `popsoft-magazine_202403`.
- Research date: **2026-09-27**.
- Classification: **SCAN-ONLY / OPTICAL-RESIDUAL-BOUNDED**.
- Preserved evidence:
  - February 2002 A/B magazine PDFs are present with fixed IA metadata hashes;
  - February-A OCR has five StoneAge-2.5/Spirit-King proximity hits under the project's bounded detector;
  - the item exposes **0 optical-image files**, so no cover-disc filesystem or client bytes are present on this current IA file surface.
- Rejected false positive:
  - IA's only broad 2002 `大众软件` software result is `start-modem-5600d`; its `START_MODEM.iso` is a Fujian Start/实达 modem driver CD and is unrelated to the target carrier.
- Critical limit:
  - the existence/content of the paper magazine does not identify which A/B issue or disc pressing supplied StoneAge 2.5;
  - no inference from magazine OCR to disc-byte identity is permitted.
- Reopen trigger:
  - exact `大众游戏` February-2002 disc identifier/image, disc-face scan, ISO/BIN/CUE/file tree, checksum, torrent/archive member list, or independent mirror.
- Canonical detail: `research/clients/STONEAGE-SA25-POPSOFT-2002-CARRIER-BOUNDARY-R1.md`.
- Derived report: `research/recovered/STONEAGE-SA25-POPSOFT-2002-RESIDUAL-R1.txt`.


## SRC-CN-2026-HNSHZY-ZHONGXUESHENGDIANNAO-CATALOGUE-01

- Source type: current institutional catalogue/search-index lead on the official domain of 湖南石油化工职业技术学院.
- Research date: **2026-09-27**.
- Same-title electronic-media holdings publicly observed for `中学生电脑` / publisher `课堂内外杂志社出版` include at least:
  - `TP3-794/12.2`, `.3`, `.5`, `.8`, `.9`, `.10`, `.12`, `.13`, `.14`.
- The catalogue publication-date field for these observed rows is **blank / `.`**.
- Call-number correction:
  - the decimal suffix is not a recovered month/issue number;
  - a neighboring same-class record `TP3-794/20.14` is explicitly `《电脑迷》2009年第7月号下配刊光盘` with publication date `2009.7`, proving a suffix such as `.14` cannot be read directly as a calendar month.
- Contemporary relevance:
  - 17173/Sina's 2002 StoneAge 2.5 distribution list names **`《中学生电脑》2002年攻略特刊`** as a possible complete-package/updater carrier.
- Confidence: **B for literal public catalogue rows; OPEN for year/issue/media identity of the target special**.
- Recovery consequence:
  - retain `TP3-794/12.*` only as institutional catalogue tokens;
  - do **not** infer 2002 or issue chronology from the suffix.
- Public old-disc Directory-Lister cross-check:
  - **5,173** directory pages / **97,708** links / **38,826** file links inspected;
  - **0** `中学生电脑` matches, **0** StoneAge target-name matches, **0** errors, **0** frontier remaining;
  - classification: **current public filename/path route BOUNDED**.
- Reopen only from an exact OPAC/accession join, issue/disc photo, optical image/file tree/checksum, torrent/archive-member record or independent mirror.
- Canonical note: `research/clients/STONEAGE-SA25-ZHONGXUESHENGDIANNAO-LIBRARY-LEAD-R1.md`.
- Derived directory report: `research/recovered/STONEAGE-SA25-OLD-DISC-DIRECTORY-R1.txt`.


## SRC-CN-2026-OLD-DISC-DIRECTORY-SA25-NAME-SWEEP-01

- Surface: public Directory Lister `https://oddownload.nuduseng.com/`, limited to top-level roots whose names contain `老光盘群`.
- Research date: **2026-09-27**.
- Method: bounded concurrent traversal of directory HTML and file names only; **no optical/archive executable payload bodies downloaded**.
- Completed R2 inventory:
  - 29 old-disc roots;
  - 5,173 pages;
  - 97,708 links;
  - 38,190 directory links;
  - 38,826 file links;
  - 0 target matches;
  - 0 errors;
  - 0 remaining frontier.
- Search identities included `中学生电脑`, `课堂内外`, `攻略特刊`, `石器时代2.5`, `精灵王传说` and orthographic/English variants.
- Classification: **BOUNDED for current public path/filename metadata**.
- Important limit: zero filename/path matches do not prove absence of a target object hidden behind generic filenames or outside this current public directory tree.
- Derived report: `research/recovered/STONEAGE-SA25-OLD-DISC-DIRECTORY-R1.txt`.


## SRC-CN-2026-SA25-WANFANG-CARRIER-CONTEXT-01

- Research date: **2026-09-27**.
- Target remains the photographed disc:
  - `永远的石器时代 2.5 精灵王传说`;
  - `万方数据电子出版社出版`;
  - ISBN `7-900096-07-8/Z.03`;
  - barcode `9787900096074`.
- New publisher-context evidence:
  - a 2005 新闻出版总署 enforcement list records **万方数据电子出版社** on the game/electronic publication `战神3000`, ISBN **`7-900096-34-5`**;
  - this proves that `7-900096-*` was a Wanfang game/electronic-publication number family, but does not identify the `07-8` item.
- Current-market search lead only:
  - a current JD index exposes a seller-generated title string `石器时代3.0攻略宝典年甸新大陆 万方数据电子出版`, alongside other Wanfang game-guide/strategy titles;
  - this is **not bibliographic authority** and the literal seller text is retained without silently correcting its wording.
- Contemporaneous provenance control:
  - Beijing Waei's 2003 warning about a different StoneAge 5.0 strategy-guide product states that its bundled client CD was a **network-download version rather than an official Waei product disc**.
- Classification consequence:
  - the Wanfang 2.5 object remains **OPEN / UNCLASSIFIED-CARRIER**;
  - the **secondary publication / guide / publisher-bundle hypothesis is strengthened as a search direction, not promoted to fact**;
  - even if future file-tree evidence shows a complete client installer, the disc must keep a separate carrier-provenance grade until an operator/official package chain is established.
- Exact bibliographic search boundary:
  - the 2026-09-27 targeted public-web pass over exact forms `7-900096-07-8`, `7-900096-07-8/Z.03`, `7900096078`, `9787900096074` and the exact visible title recovered **no exact independent bibliographic record**;
  - targeted searches across major indexed bibliographic/commercial surfaces likewise yielded no exact ISBN hit;
  - this is a search-result boundary only, not proof that no catalogue record exists.
- Next decisive evidence:
  - exact CIP/library catalogue record for `7-900096-07-8/Z.03`;
  - package/book/disc photographs linking the ISBN to a guide or Waei product;
  - read-only optical image/file tree with hashes.
- Canonical analysis: `research/clients/STONEAGE-SA25-WANFANG-DISC-R1.md`.
- Related provenance control: `SRC-CN-2003-WAEI-SECONDARY-GUIDE-CLIENT-CD-WARNING-01`.
- Publisher-family control: `SRC-CN-2005-GAPP-WANFANG-GAME-PUBLICATION-01`.



## SRC-CN-2026-JD-STONEAGE-JINHAIWAN-SURVIVAL-LEAD-01

- Research date: **2026-09-27**.
- Source type: current public shopping/search-index title strings; survival/search lead only, not authenticated provenance.
- Current indexed title strings include:
  - `二手9成新 石器时代网络游戏 广西金海湾电子音像出版社`;
  - `STONEAGE 石器时代 北京华义联合软件开发有限公司 广西金海湾电子音像...`.
- Public index surfaces:
  - https://www.jd.com/book/670a5d579c7edcad77f.html
  - https://www.jd.com/zuozhe/171326824345d6c79c30.html
- Historical control:
  - contemporaneous Sina identifies 广西金海湾电子音像出版社 as the publication/distribution party for the **2001-01-10 Mainland launch** and states that four package variants were issued;
  - an independent 2002 Peking University paper corroborates the 2001-01-10 publication relationship.
- Confidence: **C for the current seller/index strings; A-/B+ for the separate historical role/date controls**.
- Supports:
  - physical material labelled with the historically correct Mainland launch publisher identity appears to survive in the present secondary-market index;
  - the literal title strings create new exact search tokens for public scans, mirrors, preservation catalogues and cached images.
- Does not establish:
  - that any current listing is an original January-2001 first pressing;
  - which of the four launch package variants it represents;
  - ISBN/ISRC/catalogue number, disc-face identity, mastering, file tree or client bytes;
  - seller wording such as `正版` as an authentication result.
- Priority:
  - **HIGH / EARLY MAINLAND OFFICIAL-CARRIER ROUTE** because successful public recovery could provide an operator-era Mainland specimen chronologically much closer to the JSS/Taiwan baseline than the 2.5 Wanfang carrier.
- Reopen/promote only from:
  - readable package/disc photos;
  - exact publisher/catalogue/ISBN/ISRC identifier;
  - publicly obtainable read-only optical image/file tree with hashes.
- Canonical research note: `research/clients/STONEAGE-2001-MAINLAND-LAUNCH-PHYSICAL-R1.md`.



## SRC-CN-2016-SHIQIME-EARLY-MAINLAND-CLIENT-DISC-PHOTOS-01

- Page: https://www.shiqi.me/pt_51.htm
- Research date: **2026-09-27**.
- Source class: later first-person player preservation photographs.
- Direct photographed sequence:
  1. author-labelled `石器时代1.82的客户端`:
     - https://www.shiqi.me/zb_users/upload/2016/05/201605041462372233975831.jpg
     - disc visibly carries **北京华义联合软件开发有限公司** and **广西金海湾电子音像出版社** text;
     - a physical serial-label sticker is present on the disc face;
     - exact small-print ISBN/ISRC is not transcribed at current image resolution.
  2. author-labelled `石器时代2.0客户端`, stated by the author to have been bought in an **老手削暴包**:
     - https://www.shiqi.me/zb_users/upload/2016/05/201605041462372263129465.jpg
     - disc face visibly reads **`石器时代2.0 家族开拓史`**.
  3. author-labelled `石器时代2.5客户端`:
     - https://www.shiqi.me/zb_users/upload/2016/05/201605041462372351521932.jpg
     - disc face visibly reads **`石器时代2.5 精灵王传说`** and carries Waei/operator branding.
- Cross-source control:
  - contemporaneous 17173 independently states that `石器时代2.0老手削暴包` contained a **2.0 client disc**, making the author's package recollection coherent with a period product description.
- Archaeology consequence:
  - this closes the question of whether **photographed early Mainland Waei/Jinhaiwan client-disc material survives publicly**: yes, at photograph level;
  - it does **not** close byte recovery.
- Priority:
  - the 1.x/1.82 photographed disc is now a **HIGH-value exact visual carrier lead** for an early Mainland specimen;
  - next target is a higher-resolution disc/package back image exposing exact ISBN/ISRC/catalogue identifiers, followed by public optical-image/file-tree recovery.
- Byte boundary:
  - no ISO/BIN/CUE/file tree, matrix/IFPI, volume label or hash is established by these photographs.

## SRC-CN-2026-MAINLAND-JINHAIWAN-PRESERVATION-INDEX-BOUNDARY-01

- Derived report: `research/recovered/STONEAGE-2001-MAINLAND-JINHAIWAN-PRESERVATION-R1.txt`.
- Research date: **2026-09-27**.
- Scope: exact Internet Archive + DiscMaster metadata queries over five source-derived combinations of:
  - `石器时代`;
  - `广西金海湾电子音像出版社`;
  - `北京华义`;
  - `STONEAGE`;
  - `石器时代网络游戏`.
- Result:
  - **5 query identities**;
  - **0 strict Internet Archive items**;
  - **0 strict DiscMaster hits**;
  - **0 interesting IA media files**;
  - **0 errors**.
- Classification: **tested exact IA/DiscMaster publisher-title route BOUNDED**.
- Important limit:
  - zero indexed preservation hits do not negate the direct photographed physical-media survival evidence;
  - reopen from new exact ISBN/ISRC/catalogue/matrix/disc-image/file-tree tokens rather than repeating these same broad identity combinations.



## SRC-CN-2026-EARLY-MAINLAND-PROVISIONAL-PUBLICATION-ID-01

- Research date: **2026-09-27**.
- Physical target: the same early Mainland Waei/Jinhaiwan client disc photographed in `SRC-CN-2016-SHIQIME-EARLY-MAINLAND-CLIENT-DISC-PHOTOS-01`.
- Higher-clarity mirror/control:
  - Sohu page: https://www.sohu.com/a/406234981_120099894
  - image: https://p3.itc.cn/q_70/images03/20200707/0b5a52c6c1ce40fea0c95c7662d3cc5b.jpeg
- **Provisional visual transcription:** `ISBN 7-900323-57-0/TP·026`.
- Independently confirmed component:
  - 中国音乐著作权协会 publisher-code table assigns **`ISBN 7-900323` to 金海湾电子音像出版社**.
- Structural validation:
  - candidate ISBN-10 `7-900323-57-0` passes Mod-11;
  - derived ISBN-13 `978-7-900323-57-6` passes its checksum.
- Preservation-index follow-up:
  - exact IA/DiscMaster probe over `7-900323-57-0`, compact ISBN-10, ISBN-13, StoneAge/publisher combinations and `TP026` returned **0 strict IA items / 0 strict DiscMaster hits / 0 errors**.
- Classification:
  - **publisher prefix = independently corroborated FACT**;
  - **full item suffix `57-0/TP·026` = PROVISIONAL VISUAL TRANSCRIPTION**, not yet promoted to bibliographic fact.
- Reopen/promotion trigger:
  - an independent library/CIP/catalogue record;
  - higher-resolution disc/package back with unambiguous number;
  - another independent physical specimen exposing the same number;
  - public optical image/file tree tied to the number.
- Derived report: `research/recovered/STONEAGE-EARLY-MAINLAND-PROVISIONAL-ISBN-R1.txt`.

