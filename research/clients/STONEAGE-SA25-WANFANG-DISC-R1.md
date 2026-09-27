# StoneAge 2.5 photographed Wanfang disc lead — R1

## Scope

This record captures a newly recovered **physical-disc identity** for StoneAge 2.5. It is a provenance/search lead, not an assertion that the disc is byte-identical to Beijing-Waei's official retail client CD.

## FACT — visible disc fields

A public collector photograph shows a pressed/printed optical disc whose visible face reads:

- **永远的石器时代 2.5 精灵王传说**
- **万方数据电子出版社出版**
- **ISBN 7-900096-07-8/Z.03**
- barcode digits visibly read as **9787900096074**

Primary public image/source surface:
- https://www.shiqi.me/pt_17.htm

A separate 2016 collector article independently states that its author still possessed StoneAge installation discs for versions **2.5, 3.0, 4.0 and 5.0**, providing additional evidence that original-era mainland installation media survive in private collections:
- https://post.smzdm.com/p/462347/

## EVIDENCE BOUNDARY

- The photographed Wanfang disc is **not yet proven** to be the same client CD included in Beijing-Waei's `新手报到包`, `春满钱坤包` or `延年益兽包`.
- The disc face does not by itself establish whether it contains the full 575/580 MB client, the 8.25 MB updater, a guide/multimedia collection, or some combination.
- The publisher imprint must not be silently converted into Beijing-Waei provenance.
- Only a read-only disc image/file tree plus hashes can establish contents and relationship to the 2002 client lineage.

## Recovery consequence

The visible ISBN/barcode/title/publisher combination creates a new exact search surface that did not exist in the prior 20-carrier name-only pass.

Priority identifiers:

1. `7-900096-07-8`
2. `7900096078`
3. `9787900096074`
4. `永远的石器时代 2.5 精灵王传说`
5. `万方数据电子出版社 石器时代2.5`

If preservation metadata or media bytes are recovered, inspect for:

- disc volume label and filesystem timestamps;
- installer filenames and size;
- `StoneAge.exe` / `sa_*.exe`;
- resource generations;
- `map/*.dat` caches;
- any 2.5 updater payload;
- README/setup metadata binding the media to Waei or another distributor.

## Status

**OPEN / NEW EXACT PHYSICAL-MEDIA LEAD.**

## Collector comparison baseline — 2026-09-24

A later specialist collector series provides a materially stronger **media-classification baseline** than title text alone:

- `石器時代華義國際石器周邊收藏光碟篇（二）` explicitly labels the 2.5 segment's upper disc as the **mainland client unified-artwork disc**, with a Taiwan-version disc below it:
  - https://forum.gamer.com.tw/C.php?bsn=1571&snA=81429
- The collector's broader disc taxonomy separates **official client discs / magazine-gift discs / strategy-book-gift discs** and mainland/Taiwan variants:
  - https://forum.gamer.com.tw/C.php?bsn=1571&snA=81430
- `光碟篇（三）` states that some mainland strategy-book gift discs are nevertheless just **client installer packages**, despite their secondary carrier provenance:
  - https://forum.gamer.com.tw/C.php?bsn=1571&snA=81428
- The collector's `延年益壽包` post separately identifies a **2.5-period disc**, while the 2.5 client-package post documents multiple Waei-era 2.5 package variants:
  - https://forum.gamer.com.tw/C.php?bsn=1571&snA=81388
  - https://forum.gamer.com.tw/C.php?bsn=1571&snA=81400

### Classification consequence

The Wanfang disc remains **OPEN / UNCLASSIFIED-CARRIER** rather than being promoted or rejected.

The next decisive question is no longer merely “does the disc say StoneAge 2.5?” but:

1. does its artwork/printed identity match the known **mainland unified official client-disc** family;
2. if not, can it be tied to a magazine, strategy book, publisher bundle or other secondary carrier;
3. if it is a secondary carrier, does a read-only file tree show an unchanged official full client installer or only the 8.25 MB updater / multimedia material.

A secondary carrier can still be technically valuable, but it must not inherit official Beijing-Waei provenance by implication.


## Visual-source lineage update — 2026-09-24

R2 transient visual fingerprinting recovered three large images from the Wanfang collector page and compared them against all 11 full-size Ruten physical-media images.

- No Ruten-vs-Wanfang pair approaches the strong near-duplicate signal observed between the two standalone Ruten listings.
- Strongest Ruten-vs-Wanfang pair: **27 RANSAC inliers / 0.0322 inlier ratio**.
- By contrast, the two standalone Ruten disc images produce **743 inliers / 0.4831**, showing what a strong shared visual-source signal looks like in the same run.

**Interpretation:** the Wanfang photograph set is currently treated as an **independent visual-source cluster**. This does not establish different disc bytes, different build, or different carrier artwork. Wanfang remains **OPEN / UNCLASSIFIED-CARRIER** until readable carrier linkage or file-level evidence resolves it.

Derived analysis: `research/clients/STONEAGE-SA25-PHYSICAL-IMAGE-LINEAGE-R1.md`.



## Publisher / secondary-carrier context update — 2026-09-27

### FACT — Wanfang's `7-900096-*` range was used on game electronic publications

A 2005 新闻出版总署 enforcement list reproduced by Sina records:

- `战神3000`;
- publisher field: **万方数据电子出版社**;
- ISBN **`7-900096-34-5`**;
- code `N402`.

This does **not** identify the StoneAge disc, but it establishes that the same publisher prefix visible on `7-900096-07-8` was used by Wanfang for game/electronic publication material.

Source:
- https://news.sina.com.cn/c/2005-01-26/15295676769.shtml

### SEARCH LEAD — Wanfang and StoneAge guide publishing

A current JD aggregation/index page exposes the seller-generated title string:

- `石器时代3.0攻略宝典年甸新大陆 万方数据电子出版`

and also lists multiple other Wanfang game/strategy-guide titles. This is a **modern marketplace/index clue only**. It is not accepted as a period bibliographic record and the literal wording is not normalized.

Source:
- https://www.jd.com/jiage/137657b3435d5fce82139.html

### CONTEMPORANEOUS PROVENANCE CONTROL — a client-bearing guide disc need not be an official Waei disc

On 2003-01-28, 17173 carried Beijing Waei's warning about a different product titled `石器时代5.0官方攻略宝典`. The warning said the publisher was not authorized by Waei and that the bundled `石器时代ONLINE宠物进化史` client CD was a **network-download version**, not an official Waei product disc.

Sources:
- https://news.17173.com/content/2003-1-28/n408_324318.html
- https://news.17173.com/content/2003-1-28/n970_886620.html

This creates an important archaeology rule:

> **client payload present ≠ official physical-client carrier**

A secondary book/guide/publisher disc may still preserve technically useful client bytes. If so, payload ancestry must be analyzed independently from carrier provenance.

### Exact ISBN/title search result

A fresh exact public-web pass over:

- `7-900096-07-8`
- `7-900096-07-8/Z.03`
- `7900096078`
- `9787900096074`
- `永远的石器时代 2.5 精灵王传说`

did not recover an independent exact bibliographic/CIP record. Additional exact-ISBN searches on currently indexed WorldCat/Google Books/Douban/Bookschina/Dangdang/JD/Tmall surfaces also returned no exact record in this pass.

This is **not evidence that the publication record never existed**. It only means the current indexed exact-ISBN route remains unresolved.

## Updated classification

**OPEN / UNCLASSIFIED-CARRIER.**

The evidence now makes a **secondary publication / strategy-guide / publisher-bundle carrier** a materially stronger hypothesis to test, but it is not a fact.

Do not promote the Wanfang disc to:

- official Beijing-Waei client disc;
- strategy-book gift disc;
- full 575/580 MB client;
- 8.25 MB updater;

until independent carrier documentation or file-level evidence resolves those questions.

The two-dimensional classification is now mandatory:

1. **carrier provenance** — official boxed client / magazine / strategy guide / publisher bundle / unknown;
2. **payload identity** — official installer bytes / network-downloaded installer / updater / multimedia / mixed / unknown.

