# JSS Product Identifier Archaeology — R1

Date: 2026-09-18

Purpose: reconstruct the product-number / JAN space surrounding the original Japan System Supply (JSS) Windows releases so searches for the 1999 `STONEAGE` retail package can be narrowed without inventing a barcode.

This document is a **search-control artifact**. A numeric pattern is not promoted into a StoneAge identifier unless a package, catalog, first-party record, or equivalent source explicitly connects that identifier to StoneAge.

## 1. Why this track exists

The 1999 JSS StoneAge package is constrained by first-party manual/advertising evidence and later package photographs. Its retail JAN is now directly resolved as **`4909476303010`** from a surviving package-back photograph; the remaining identifier gap is the exact model/type code and media-level label/matrix identifiers.

A tempting early shortcut was to extrapolate from JSS console barcodes:

- Game Boy `チャルボ55` — `4909476802018`
- N64 `カメレオンツイスト` — `4909476803015`
- N64 `カメレオンツイスト2` — `4909476804012`

Those three numbers form an apparent sequence. However, more relevant **Windows boxed-software evidence disproves the assumption that StoneAge should simply be the next `49094768...` item**.

## 2. Verified JSS-family identifiers

### A. Windows 95 — LIFESTORM

Modern Japanese retailer database:

https://www.suruga-ya.jp/kaitori/kaitori_detail/145002458

Fields preserved by Suruga-ya:

- title: `LIFESTORM`
- media/platform: Windows 95 CD software
- manufacturer: 日本システムサプライ
- model/type: **`JV02005`**
- JAN: **`4909476301016`**
- management ID: `145002458`

Classification: **B for the literal catalog fields; not a first-party package scan.**

A current Yahoo! Flea Market physical listing independently depicts a surviving JSS LIFESTORM package:

https://paypayfleamarket.yahoo.co.jp/item/z535473608

The marketplace listing is not used to authenticate the JAN by itself, but it confirms that surviving physical retail copies remain in circulation.

### B. Windows 3.1/95 — 古都の旅 京都

Suruga-ya catalog/search record:

https://www.suruga-ya.jp/kaitori/search_buy?category=65204&page=5734&search_word=

Preserved fields:

- title: `古都の旅 京都`
- platform: Windows 3.1/95 CD software
- JAN: **`4909476502031`**
- management ID: `145061045`

JSS/Nanken-Kobo attribution is independently represented in the project’s company-lineage research; the Suruga row itself is used here only for the literal product identifier.

Classification: **B/C catalog evidence**.

### C. Windows 3.1/95 — 四柱推命入門 しゃべる桃源郷

Rakuten Product Navigator:

https://product.rakuten.co.jp/product/-/aa73b804d7b8bd41b9aa5f3d579f2b7c/

Preserved fields:

- title: `四柱推命入門 しゃべる桃源郷`
- platform: Windows 3.1/95 CD software
- manufacturer: 日本システムサプライ
- JAN: **`4909476603011`**

Classification: **B/C catalog evidence**.

### D. Game Boy — チャルボ55

MediaWorld:

https://mediaworld.co.jp/products/10188652003

Preserved fields:

- release: 1997-02-21
- product code: `DMG-A2SJ`
- JAN/EAN: **`4909476802018`**

Classification: **B catalog evidence**.

### E. Nintendo 64 — カメレオンツイスト

Rakuten / Suruga-ya listing:

https://item.rakuten.co.jp/surugaya-a-too/163469-1/

Preserved fields:

- release: 1997-12-12
- product code: `NUS-P-NCTJ`
- JAN: **`4909476803015`**

Classification: **B catalog evidence**.

### F. Nintendo 64 — カメレオンツイスト2

Suruga-ya:

https://www.suruga-ya.jp/kaitori/kaitori_detail/147000204

Preserved fields:

- release: 1998-12-25
- product code: `NUS-NV2J-JPN`
- JAN: **`4909476804012`**

Classification: **B catalog evidence**.

## 3. Period LIFESTORM II bridge

Retromags preserves a scan of a period Japanese `LIFESTORM II` advertisement:

https://www.retromags.com/gallery/image/34988-lifestorm-ii-japan-april-1999/

Visible advertisement facts:

- Windows 95/98
- `1999年2月20日発売`
- price `8,800円` before tax
- JSS / `www.titan.co.jp` context

The advertisement does **not** expose a readable JAN/model number in the currently accessible image/extraction path.

A current Yahoo! Auctions listing now supplies the missing direct package identifier evidence:

https://auctions.yahoo.co.jp/jp/auction/v1234885585

The listing exposes three full-resolution photographs of a surviving `LIFESTORM II ～光と闇の継承者～` package and CD-ROM. The back-box photograph visibly shows:

- Windows 95/98;
- JSS / `http://www.titan.co.jp/` branding;
- price `8,800円(税別)`;
- JAN/barcode **`4909476302013`**.

Classification: **B for literal visible package fields; C for seller provenance**.

Research consequence: **`4909476302013` is no longer an unassigned candidate. It is directly evidenced as the LIFESTORM II retail JAN.** The model/type code remains unresolved.

This title is chronologically and commercially valuable because it sits immediately before StoneAge in JSS's Windows online-RPG lineage.


### StoneAge package-back resolution

A preserved Yahoo! Auctions listing for a seller-described unopened StoneAge package provides the corresponding direct StoneAge identifier:

https://auctions.yahoo.co.jp/jp/auction/k1131932809

The surviving back-box photograph visibly prints **JAN `4909476303010`**. The photographed front/side/back packaging matches the early JSS/Gamer's Dream Windows 95/98 retail presentation.

Classification: **B for literal visible package fields; C for seller provenance/unopened-status claim**.

This closes the previous gap between the numerical `30301` search candidate and a StoneAge-specific artifact. The StoneAge model/type code remains unresolved.

### Suruga direct catalog record recovered

The Suruga discovery lead has now been resolved through its dated product archive:

- archive: `https://www.suruga-ya.jp/product_archives/19991015_1`
- direct product: `https://www.suruga-ya.jp/product/detail/145026779`

The dated archive explicitly lists **`Windows95/98 CDソフト/ストーンエイジ[初回版]`** on 1999-10-15. The direct product page identifies **日本システムサプライ**, Suruga management number **`145026779`**, release date **1999-10-15**, displayed list price **9,680円**, and media **CD**.

Crucially, the direct page does **not** expose a `型番` field. Therefore:

- `145026779` is retained only as Suruga's **management number**, not a StoneAge product model;
- StoneAge's model/type code remains **OPEN**;
- no model value is inferred from LIFESTORM's `JV02005`.

The product image currently resolves to a Suruga no-photo placeholder, so this source does not improve disc-label or package-side resolution.

The apparent **8,800円 vs 9,680円** price discrepancy is now better classified as a catalog-display effect, not contradictory historical price evidence. The period StoneAge advertisement explicitly prints **8,800円（税別）**. Suruga currently displays **9,680円** and warns that tax display may differ. Two JSS controls show the same exact transformation: `チャルボ55` is historically 3,800円 before tax but Suruga displays 4,180円; `カメレオンツイスト` is contemporaneously 6,980円 before tax but Suruga displays 7,678円. Each current Suruga value is exactly the historical tax-exclusive price ×1.10.

This is recorded as a **strong catalog-presentation interpretation**, not as an undocumented statement about Suruga's internal normalization policy. Operationally, the current 9,680円 field is not independent evidence for a different 1999 StoneAge MSRP; **8,800円（税別） remains the historical baseline**.

## 4. Structural observation

Across the verified identifiers above, the first seven digits are consistently:

`4909476`

Observed product references then diverge by product family:

| Product | Platform | JAN | 5-digit body after 4909476, before check digit |
| --- | --- | --- | --- |
| LIFESTORM | Windows 95 | 4909476301016 | `30101` |
| LIFESTORM II | Windows 95/98 | **4909476302013** | **`30201`** |
| STONEAGE | Windows 95/98 | **4909476303010** | **`30301`** |
| 古都の旅 京都 | Windows 3.1/95 | 4909476502031 | `50203` |
| 四柱推命入門 しゃべる桃源郷 | Windows 3.1/95 | 4909476603011 | `60301` |
| チャルボ55 | Game Boy | 4909476802018 | `80201` |
| カメレオンツイスト | N64 | 4909476803015 | `80301` |
| カメレオンツイスト2 | N64 | 4909476804012 | `80401` |

### What this supports

**FACT / observation:** multiple JSS-associated physical products share the stem `4909476`, while different product families occupy different following number ranges.

### What this does not support

Do **not** claim from these records alone that:

- `4909476` has been independently verified as the exact GS1 company-prefix allocation length;
- the first two digits of the five-digit body are a formally documented platform/category code;
- all Windows games use `30xxx`;
- LIFESTORM II or StoneAge follows a simple numerical increment;
- any StoneAge JAN candidate not explicitly bound to StoneAge by a source.

The pattern is a search-space reducer, not a product assignment.

## 5. Controlled candidate generation

Earlier in this research pass, the `LIFESTORM` online-game body `30101` was used only as a search heuristic to generate check-digit-valid `30201` / `30301` continuations:

- `4909476302013`
- `4909476303010`

The first of those numbers is now independently resolved by the surviving LIFESTORM II package photograph:

- **`4909476302013` = LIFESTORM II — directly evidenced package JAN.**

The second candidate is now also independently resolved by a surviving StoneAge package photograph:

- **`4909476303010` = STONEAGE — directly observed back-box JAN.**

The decisive source is Yahoo! Auctions listing `k1131932809`, whose preserved back-package image visibly prints the barcode. This promotion is based on **artifact photography**, not on the numerical sequence.

The observed online-RPG sequence is therefore now:

1. LIFESTORM — `4909476301016` / body `30101`
2. LIFESTORM II — `4909476302013` / body `30201`
3. STONEAGE — `4909476303010` / body `30301`

This three-item sequence is an observation about these products, not a license to infer unobserved JSS identifiers.

A prior console-sequence candidate, `4909476805019`, remains explicitly rejected as a StoneAge lead because the directly observed StoneAge package now supplies the actual JAN.

## 6. Research consequences

The highest-value identifier search is now:

1. recover a **StoneAge model/type-bearing record** for JAN `4909476303010` from Suruga's buy-side index, another retailer/distributor database, a period catalog, or readable package-side/back evidence;
2. recover the still-missing **LIFESTORM II model/type code** for JAN `4909476302013`;
3. preserve higher-resolution StoneAge box/disc imagery that may expose model, disc-label or matrix identifiers;
4. recover at least one additional JSS Windows online-game/software model around 1998–1999 if it helps decode the `JV...` model family;
5. keep all further numerical extrapolation subordinate to direct package/catalog/media evidence.

## 7. Immediate targets

Search exact variants:

- `LIFESTORM II`, `LIFESTORM2`, `LIFE STORM Vol.2 光と闇の継承者`
- `ライフストーム2`, `ライフストームII`
- JSS model-code family around `JV02005`
- JAN stem `49094763` with period Windows software
- Suruga buy-side/search rows or cached variants for management number `145026779` / title `ストーンエイジ[初回版]` that explicitly expose a `型番` field
- Japanese distributor/dealer catalogs from 1998–1999
- physical box side/back scans
- old auction snapshots and retailer inventory dumps

For StoneAge, the package-back target has succeeded: Yahoo! Auctions listing `k1131932809` directly exposes JAN **`4909476303010`**. The direct Suruga initial-edition product record is now also recovered, but it exposes only Suruga management number `145026779`, not a model/type field. The identifier priority therefore narrows to a model-bearing catalog/package source, in parallel with higher-resolution side/back/disc evidence for disc labels and matrix identifiers, then a provenance-preserving publicly obtainable disc image or file tree.
