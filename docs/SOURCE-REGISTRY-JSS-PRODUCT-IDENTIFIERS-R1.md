# Source Registry Supplement — JSS Product Identifiers R1

Date: 2026-09-18

Purpose: register catalog and period-advertising evidence used to constrain JSS physical product identifiers around the original StoneAge release.

Canonical analysis: `research/clients/JSS-PRODUCT-IDENTIFIER-ARCHAEOLOGY-R1.md`.

## Evidence rule

- Retail/catalog databases can support literal product fields they preserve, but remain later secondary preservation unless matched to a primary package.
- Numerical adjacency is never product identity.
- EAN/JAN check-digit validity proves only syntactic validity, not that a product ever used the number.
- Physical package labels, first-party/distributor catalogs, and provenance-preserving scans outrank inferred numbering patterns.

## SRC-JP-JSS-LIFESTORM-SURUGA-ID-01

- title: Suruga-ya LIFESTORM catalog record
- URL: https://www.suruga-ya.jp/kaitori/kaitori_detail/145002458
- retrieval date: 2026-09-18
- source type: modern Japanese retailer catalog
- confidence: **B for literal catalog fields**
- supports:
  - Windows 95 CD software `LIFESTORM`
  - manufacturer 日本システムサプライ
  - model/type `JV02005`
  - JAN `4909476301016`
- limitation: not a first-party 1998 package scan.

## SRC-JP-JSS-KOTO-KYOTO-SURUGA-ID-01

- title: Suruga-ya `古都の旅 京都` catalog row
- URL: https://www.suruga-ya.jp/kaitori/search_buy?category=65204&page=5734&search_word=
- retrieval date: 2026-09-18
- source type: modern retailer catalog
- confidence: **B/C**
- supports:
  - Windows 3.1/95 CD title `古都の旅 京都`
  - JAN `4909476502031`
  - Suruga management ID `145061045`
- attribution note: company/developer lineage is established separately; this row is used here for the literal identifier.

## SRC-JP-JSS-TOUGENKYOU-RAKUTEN-ID-01

- title: Rakuten Product Navigator `四柱推命入門 しゃべる桃源郷`
- URL: https://product.rakuten.co.jp/product/-/aa73b804d7b8bd41b9aa5f3d579f2b7c/
- retrieval date: 2026-09-18
- source type: modern retailer/product database
- confidence: **B/C**
- supports:
  - Windows 3.1/95 CD software
  - manufacturer 日本システムサプライ
  - JAN `4909476603011`

## SRC-JP-JSS-CHALVO55-MEDIAWORLD-ID-01

- title: MediaWorld `チャルボ55`
- URL: https://mediaworld.co.jp/products/10188652003
- retrieval date: 2026-09-18
- source type: modern game retailer catalog
- confidence: **B**
- supports:
  - release 1997-02-21
  - model `DMG-A2SJ`
  - JAN/EAN `4909476802018`

## SRC-JP-JSS-CHAMELEON1-RAKUTEN-ID-01

- title: Rakuten/Suruga-ya `カメレオンツイスト`
- URL: https://item.rakuten.co.jp/surugaya-a-too/163469-1/
- retrieval date: 2026-09-18
- source type: modern retailer listing
- confidence: **B**
- supports:
  - release 1997-12-12
  - model `NUS-P-NCTJ`
  - JAN `4909476803015`

## SRC-JP-JSS-CHAMELEON2-SURUGA-ID-01

- title: Suruga-ya `カメレオンツイスト2`
- URL: https://www.suruga-ya.jp/kaitori/kaitori_detail/147000204
- retrieval date: 2026-09-18
- source type: modern retailer catalog
- confidence: **B**
- supports:
  - release 1998-12-25
  - model `NUS-NV2J-JPN`
  - JAN `4909476804012`

## SRC-JP-JSS-LIFESTORM2-RETROMAGS-AD-01

- title: `Lifestorm II (Japan) (April 1999)`
- URL: https://www.retromags.com/gallery/image/34988-lifestorm-ii-japan-april-1999/
- uploader: kitsunebi
- preservation post date: 2020-02-06
- source type: later preservation of period advertisement
- confidence: **B for visible printed advertisement facts; C for scan provenance beyond the preserved page**
- visible facts:
  - Windows 95/98
  - release date printed as `1999年2月20日`
  - price `8,800円` before tax
  - JSS / titan.co.jp context
- unresolved from this advertisement itself:
  - JAN
  - model/type code
  - package barcode
- cross-reference: the JAN is now independently resolved by `SRC-JP-JSS-LIFESTORM2-YAHOO-AUCTION-ID-01`; the advertisement remains useful as period release/price evidence rather than identifier evidence.

## SRC-JP-JSS-LIFESTORM2-YAHOO-AUCTION-ID-01

- title: `LIFESTORM Ⅱ ～光と闇の継承者～` surviving package/CD auction
- auction ID: `v1234885585`
- listing URL: https://auctions.yahoo.co.jp/jp/auction/v1234885585
- retrieval date: 2026-09-18
- source type: current Japanese marketplace photographs of a surviving JSS retail package and game disc
- confidence: **B for literal visible package/disc fields; C for seller provenance**
- seller/listing scope:
  - the listing states that only the CD-ROM and package are included;
  - no claim is made here that the pictured copy is complete beyond those visible objects.
- directly visible package facts:
  - title `LIFESTORM II ～光と闇の継承者～`;
  - Windows 95/98;
  - ©1999 JAPAN SYSTEM SUPPLY;
  - price `8,800円(税別)`;
  - JSS / `http://www.titan.co.jp/` branding;
  - back-box JAN/barcode **`4909476302013`**.
- directly visible disc fact:
  - the photographed optical disc carries matching `LIFESTORM II` artwork/branding beside the package.
- original image targets exposed by Yahoo:
  1. https://auctions.c.yimg.jp/images.auctions.yahoo.co.jp/image/dr000/auc0206/user/e659419a2817be9367483a4d3ec7660c61f895515cd4978e4f1701151861a988/i-img1200x1200-17824404959388dk1udu7794.jpg
  2. https://auctions.c.yimg.jp/images.auctions.yahoo.co.jp/image/dr000/auc0206/user/e659419a2817be9367483a4d3ec7660c61f895515cd4978e4f1701151861a988/i-img1200x1200-17824404958785mdyu027794.jpg
  3. https://auctions.c.yimg.jp/images.auctions.yahoo.co.jp/image/dr000/auc0206/user/e659419a2817be9367483a4d3ec7660c61f895515cd4978e4f1701151861a988/i-img1200x1200-17824404959065fuqfns7794.jpg
- research consequence:
  - the previously unassigned check-digit-valid search candidate `4909476302013` is now **directly bound to LIFESTORM II by a readable package-back barcode photograph** and is promoted from search candidate to observed retail JAN;
  - the observed JSS online-RPG Windows sequence now includes `LIFESTORM = 4909476301016` and `LIFESTORM II = 4909476302013`.
- does not establish:
  - the LIFESTORM II model/type code;
  - StoneAge's JAN/model;
  - a general rule that the next numerical body must belong to StoneAge;
  - disc matrix text, filesystem contents, hashes or executable version.

## SRC-JP-JSS-LIFESTORM2-YAHOO-HIRES-01

- title: `【新品】Windows～LIFE STORMⅡ　光と闇の継承者～`
- auction ID: `c771109001`
- listing URL: https://auctions.yahoo.co.jp/jp/auction/c771109001
- listing period: 2023-03-23 through 2023-03-30
- retrieval date: 2026-09-18
- source type: preserved Yahoo! Auctions photographs of a surviving LIFESTORM II package, manual and optical disc
- confidence: **B for literal visible artifact fields; C for seller provenance**
- visual value:
  - the preserved images are substantially higher resolution than several other package leads;
  - one photograph shows the package side/back together with the manual and the actual LIFESTORM II optical disc;
  - another shows the package front/manual artwork;
  - the full back-box photograph independently confirms Windows 95/98, price `8,800円`, JSS branding and JAN **`4909476302013`**.
- original image targets:
  1. package side/back + manual + disc: Yahoo original image associated with auction `c771109001`
  2. package/manual front: Yahoo original image associated with auction `c771109001`
  3. full package back: Yahoo original image associated with auction `c771109001`
- negative observation:
  - despite the improved resolution, no model/type code can be read with sufficient confidence from the visible package fields;
  - no disc matrix text is readable.
- research consequence:
  - independently corroborates the already promoted LIFESTORM II JAN without relying on the newer auction;
  - provides a higher-resolution surviving-disc reference for later label/layout comparison;
  - the LIFESTORM II model/type code remains **OPEN** rather than being inferred from LIFESTORM's `JV02005`.

## SRC-JP-1999-RETAIL-YAHOO-UNOPENED-01

- title: `未開封 ストーンエイジ`
- auction ID: `k1131932809`
- listing URL: https://auctions.yahoo.co.jp/jp/auction/k1131932809
- listing period: 2024-04-09 through 2024-04-13
- retrieval date: 2026-09-18
- source type: preserved Yahoo! Auctions photographs of a seller-described unopened JSS StoneAge retail package
- confidence: **B for literal visible package fields; C for seller provenance / unopened-status claim**
- visible package observations:
  - the front is the early JSS/Gamer's Dream `STONEAGE` Windows 95/98 package design;
  - the package carries initial-edition promotional marking on the front;
  - the back shows Japan System Supply branding and the known early retail presentation;
  - the back-box JAN/barcode is directly readable as **`4909476303010`**.
- Yahoo original-image targets:
  1. side: https://auctions.c.yimg.jp/images.auctions.yahoo.co.jp/image/dr000/auc0504/users/93c224e074220661380e6f1f93b2056799fea6be/i-img640x480-1712642690euuwgk18923.jpg
  2. front: https://auctions.c.yimg.jp/images.auctions.yahoo.co.jp/image/dr000/auc0504/users/93c224e074220661380e6f1f93b2056799fea6be/i-img640x480-1712642690ufdbie13619.jpg
  3. back/barcode: https://auctions.c.yimg.jp/images.auctions.yahoo.co.jp/image/dr000/auc0504/users/93c224e074220661380e6f1f93b2056799fea6be/i-img640x480-1712642690dlqgj723.jpg
- research consequence:
  - **`4909476303010` is promoted from numerical search candidate to directly observed StoneAge retail-package JAN**;
  - the three directly observed JSS online-RPG JANs now form:
    - LIFESTORM — `4909476301016`
    - LIFESTORM II — `4909476302013`
    - STONEAGE — `4909476303010`
- does not establish:
  - StoneAge model/type code;
  - exact contents of the sealed package;
  - disc label/matrix identifiers, filesystem contents, hashes or executable metadata;
  - S-grade provenance or chain of custody for the photographed object.

## SRC-JP-JSS-STONEAGE-SURUGA-CATALOG-LEAD-01

- title: Suruga-ya indexed `ストーンエイジ[初回版]` catalog lead
- discovery URL: https://www.suruga-ya.jp/kaitori/kaitori_detail/145002458
- retrieval date: 2026-09-18
- source type: current retailer search-index / cross-catalog discovery lead
- confidence: **C as a discovery lead only; not yet a direct StoneAge product record**
- observed:
  - the current indexed snippet for Suruga-ya's JSS `LIFESTORM` record exposes a related catalog item named **`ストーンエイジ[初回版]`**;
  - the snippet classifies that related item as **`Windows95/98 CDソフト`**;
  - the directly opened LIFESTORM record confirms Suruga's catalog schema carries literal JAN, manufacturer and model/type fields for JSS Windows software.
- current limitation:
  - the available extraction path does not expose the direct StoneAge detail URL or its record body;
  - no StoneAge model/type code, Suruga management ID or additional identifier is therefore promoted from this lead.
- resolution update:
  - the direct StoneAge record was subsequently recovered at Suruga management number `145026779`; this discovery lead is therefore superseded by `SRC-JP-JSS-STONEAGE-SURUGA-DIRECT-01` below.
- research consequence:
  - do **not** infer StoneAge's model/type from LIFESTORM's `JV02005` or from numerical adjacency.

## SRC-JP-JSS-STONEAGE-SURUGA-DIRECT-01

- title: Suruga-ya `ストーンエイジ[初回版]` direct product record
- product archive URL: https://www.suruga-ya.jp/product_archives/19991015_1
- direct product URL: https://www.suruga-ya.jp/product/detail/145026779
- retrieval date: 2026-09-18
- source type: current Japanese retailer catalog / product archive
- confidence: **B for literal current catalog fields; not primary 1999 package evidence**
- directly observed:
  - Suruga's 1999-10-15 product archive lists **`Windows95/98 CDソフト/ストーンエイジ[初回版]`**;
  - the direct product record identifies manufacturer **日本システムサプライ**;
  - Suruga management number: **`145026779`**;
  - release date field: **1999-10-15**;
  - displayed list price field: **9,680円**;
  - media note: **`Windowsソフト　メディア：CD`**.
- important field boundary:
  - the direct product page does **not** expose a `型番` field for StoneAge;
  - **`145026779` is Suruga's 管理番号 and must not be treated as the StoneAge model/type code**;
  - the current product image resolves to Suruga's no-photo placeholder, so this record contributes no new package/disc visual evidence.
- price-display interpretation:
  - contemporaneous StoneAge advertising and the archived Gamer's Dream product record support **8,800円**; the photographed period advertisement explicitly prints **8,800円（税別）**;
  - Suruga's current catalog displays **定価 9,680円** and separately warns that tax display may differ between online and physical-store presentation;
  - two JSS comparison products show the same exact current-catalog arithmetic:
    - `チャルボ55`: historical **3,800円（税別）** / **3,800円＋税** (period/catalog preservation) versus current Suruga **4,180円**;
    - `カメレオンツイスト`: contemporaneous **6,980円（税別）** versus current Suruga **7,678円**;
  - all three current Suruga values equal the historical tax-exclusive amount multiplied by **1.10**: 3,800→4,180; 6,980→7,678; 8,800→9,680.
  - classification: **strong catalog-presentation interpretation, not a documented Suruga internal-policy statement**. The evidence indicates that the current Suruga `定価` field is very likely presenting these older JSS prices in a modern tax-inclusive normalized form.
  - research consequence: **9,680円 must not be treated as independent evidence that StoneAge's original 1999 pre-tax MSRP differed from 8,800円**; the period 8,800円（税別） record remains the historical baseline.
  - comparison URLs:
    - current Suruga `チャルボ55`: https://www.suruga-ya.jp/product/detail/165000649
    - historical `チャルボ55` price preservation: https://www.famitsu.com/game/title/21022/reviews
    - current Suruga `カメレオンツイスト`: https://www.suruga-ya.jp/product/detail/147000043
    - contemporaneous `カメレオンツイスト` price page: https://elibrary.arcade-museum.com/magazines/j-coj/coin-op-journal--1997-12--22-12/coin-op-journal--1997-12--22-12-376.pdf
- research consequence:
  - the direct Suruga catalog recovery objective is complete;
  - StoneAge's model/type code remains **OPEN** and must be pursued through a buy-side record, distributor/dealer database, period catalog, clearer package side/back image, or another source that explicitly exposes the model field.

## Source-group conclusion

The shared `4909476` stem is empirically observed across multiple JSS-associated physical products. More importantly, public package photographs now directly bind three consecutive JSS Windows online-RPG retail JANs:

- **LIFESTORM — `4909476301016`**
- **LIFESTORM II — `4909476302013`**
- **STONEAGE — `4909476303010`**

The StoneAge assignment is **no longer a numbering inference**: it is visible on a surviving early retail box-back photograph. Numerical sequence remains useful only for locating related artifacts and must not be generalized beyond directly observed products.

The next identifier targets are the unresolved LIFESTORM II and StoneAge model/type codes, followed by readable StoneAge disc-label/matrix identifiers.
