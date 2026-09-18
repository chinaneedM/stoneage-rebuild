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
  - the package states that a game CD and two game tickets are enclosed, and the photographed disc also bears BOTHTEC/DigiPark-era branding.
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
