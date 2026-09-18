# JSS Product Identifier Archaeology — R1

Date: 2026-09-18

Purpose: reconstruct the product-number / JAN space surrounding the original Japan System Supply (JSS) Windows releases so searches for the 1999 `STONEAGE` retail package can be narrowed without inventing a barcode.

This document is a **search-control artifact**. A numeric pattern is not promoted into a StoneAge identifier unless a package, catalog, first-party record, or equivalent source explicitly connects that identifier to StoneAge.

## 1. Why this track exists

The 1999 JSS StoneAge package is currently constrained by first-party manual/advertising evidence and later package photographs, but its product/JAN code remains unresolved.

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

## 4. Structural observation

Across the verified identifiers above, the first seven digits are consistently:

`4909476`

Observed product references then diverge by product family:

| Product | Platform | JAN | 5-digit body after 4909476, before check digit |
| --- | --- | --- | --- |
| LIFESTORM | Windows 95 | 4909476301016 | `30101` |
| LIFESTORM II | Windows 95/98 | **4909476302013** | **`30201`** |
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
- StoneAge has any specific JAN not explicitly recovered from a source.

The pattern is a search-space reducer, not a product assignment.

## 5. Controlled candidate generation

Earlier in this research pass, the `LIFESTORM` online-game body `30101` was used only as a search heuristic to generate check-digit-valid `30201` / `30301` continuations:

- `4909476302013`
- `4909476303010`

The first of those numbers is now independently resolved by the surviving LIFESTORM II package photograph:

- **`4909476302013` = LIFESTORM II — directly evidenced package JAN.**

The second remains:

- **`4909476303010` — HYPOTHESIS / SEARCH CANDIDATE ONLY.**

The fact that LIFESTORM and LIFESTORM II occupy observed bodies `30101` and `30201` makes `30301` a higher-value StoneAge search key than before, but **does not assign it to StoneAge**. Only direct product evidence can make that promotion.

A prior console-sequence candidate, `4909476805019`, remains explicitly **de-prioritized** because the more relevant Windows online-game evidence occupies the `49094763...` range.

## 6. Research consequences

The highest-value identifier search is now:

1. recover the still-missing **LIFESTORM II model/type code** while preserving the now-direct JAN `4909476302013`;
2. compare its model-code pattern with `LIFESTORM = JV02005 / 4909476301016`;
3. use `4909476303010` only as a prioritized StoneAge search key, never as an assigned identifier;
4. recover at least one additional JSS Windows online-game/software model around 1998–1999 if available;
5. verify StoneAge directly from a package back/side photograph, distributor catalog, retail database, JAN database, or original media.

## 7. Immediate targets

Search exact variants:

- `LIFESTORM II`, `LIFESTORM2`, `LIFE STORM Vol.2 光と闇の継承者`
- `ライフストーム2`, `ライフストームII`
- JSS model-code family around `JV02005`
- JAN stem `49094763` with period Windows software
- Japanese distributor/dealer catalogs from 1998–1999
- physical box side/back scans
- old auction snapshots and retailer inventory dumps

For StoneAge, retain the existing physical-media priority: a readable 1999 JSS back box or side label beats every inferred sequence. The newly verified LIFESTORM II JAN makes `4909476303010` a useful exact-string search target, but it remains unassigned until StoneAge-specific evidence is found.
