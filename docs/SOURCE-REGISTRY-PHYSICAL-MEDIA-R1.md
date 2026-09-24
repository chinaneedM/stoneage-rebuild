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

