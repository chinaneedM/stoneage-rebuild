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
- unresolved:
  - JAN
  - model/type code
  - package barcode

## Source-group conclusion

The shared `4909476` stem is now empirically observed across multiple JSS-associated physical products, but the following product-reference ranges differ between Windows titles and console titles.

This **invalidates the earlier shortcut of treating the console `49094768...` series as the direct StoneAge sequence**.

The next promotion target is a direct LIFESTORM II identifier, followed by a direct StoneAge package/catalog identifier.
