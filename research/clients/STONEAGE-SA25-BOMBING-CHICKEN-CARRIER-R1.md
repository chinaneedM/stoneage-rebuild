# StoneAge 2.5 《轰炸鸡》 cross-promotion carrier — R1

## Scope

A previously omitted source-named StoneAge 2.5 distribution carrier. This record is metadata/provenance only. It does not assert that any recovered foreign `Chicken Shoot` disc contains StoneAge bytes.

## FACT — contemporaneous StoneAge 2.5 distribution records

Two surviving 2002 portal records state that owners of StoneAge 1.X/2.X could obtain the 2.5 software through several named media/products. Both lists include **《轰炸鸡》游戏** as a standalone carrier alongside January/February 2002 magazine discs and StoneAge guide products.

- Sina Games, “《石器时代2.5》升级方法”:
  - https://games.sina.com.cn/newgames/0202/02057854.shtml
  - records the full StoneAge 2.5 package as roughly **575 MB** and the incremental updater as **8.25 MB**;
  - the carrier list says the named media could provide the **full package or incremental updater**. It does not specify which payload variant was on 《轰炸鸡》.
- 17173 StoneAge version page, “《石器2.5--精灵王传说》升级办法”:
  - https://news.17173.com/z/stoneage/banben/sa25-up.htm
  - independently preserves the same carrier list, with the full package rounded to **580 MB** and the incremental updater at **8.25 MB**.

The 575/580 MB discrepancy is treated as source rounding/retelling, not an exact file-size identity.

## FACT — Beijing-Waei later distribution tie

A 2003 Beijing-Waei StoneAge 6.0 product announcement preserved by 17173 describes the “夏日清新包” B combination as:

- one StoneAge ONLINE 《海贼王遗迹》 game disc;
- one **《轰炸鸡》 game disc**.

Source:
- https://news.17173.com/content/2003-6-7/n276_193092.html

The same record describes 《轰炸鸡》 as a light shooting game with support for **four-player online play**. This independently shows that 《轰炸鸡》 was a real game disc circulating through Beijing-Waei StoneAge product channels, not merely an isolated 2002 list typo.

## HYPOTHESIS — 《轰炸鸡》 may be the localized/distributed Chicken Shoot PC title

The period, genre and four-player-network description are consistent with the Windows title **Chicken Shoot**:

- MobyGames records Windows releases in **2000** and **2001** under TopWare/related publishing:
  - https://www.mobygames.com/game/41924/chicken-shoot/releases/
- TopWare's current title page describes a PC action/arcade game for **1–4 players**:
  - https://www.topware.com/en/chicken-shoot.html

This identity is **not promoted to FACT** until a Chinese/Waei package scan, disc label, catalog record, executable metadata or file tree directly binds 《轰炸鸡》 to `Chicken Shoot`.

## CONTROL — foreign Chicken Shoot media are not StoneAge provenance

BetaArchive indexes a **2002 Lithuanian Chicken Shoot CD** as an original MDF/MDS source-media release (364.13 MB):

- https://www.betaarchive.com/database/view_release.php?uuid=0e1ed295-7058-4f0c-bc21-723909eb2c47

That record proves that original physical-media preservation exists for the base title family, but it is a foreign release and provides **no evidence** that its disc includes StoneAge 2.5 material. It must not be used as a StoneAge client source.

## Recovery consequence

1. Add 《轰炸鸡》 as a **20th source-named 2.5 carrier identity** in the exact-carrier preservation probe.
2. Search Chinese/Waei/StoneAge-associated metadata first; foreign `Chicken Shoot` releases are controls only.
3. If a Chinese/Waei disc image or file tree is recovered, inspect it for either:
   - the **8.25 MB incremental updater**, or
   - a full StoneAge 2.5 package,
   without assuming which variant the 2002 source list meant.
4. Do not infer field-map provenance from the carrier name alone; only recovered bytes with carrier provenance can move the pre-June-2003 anchor.

## Status

**OPEN / NEW INDEPENDENT CARRIER LEAD.** The carrier identity is source-attested; the exact Chinese disc identity, package metadata, StoneAge payload variant, filename, hash and bytes remain unrecovered.


## SEARCH-ONLY alias lead — 2026-09-24

A later public optical-disc catalogue preserves a more specific lexical identity for the game family:

- catalogue block: `2001 NEW GAME 093（总第280期）2CD`;
- entry identifier: **`2001C226`**;
- title string: **`哇靠轰炸鸡完美中文版`**;
- publisher string as preserved by that catalogue: **`华议国际`**;
- public catalogue surface:
  - https://oddownload.nuduseng.com/18%E8%80%81%E5%85%89%E7%9B%98%E7%BE%A4%28%E7%BE%A4%E5%8F%B7854318908%29%E7%BE%A4%E5%8F%8B%E5%88%86%E4%BA%AB%E6%B1%87%E6%80%BB%202020%E5%B9%B44%E6%9C%88-5%E6%9C%88/2020-04-30/%E8%97%8F%E7%BB%8F%E9%98%81-%E4%B8%9C%E6%96%B9%E7%8B%82%E9%BE%99/%E8%97%8F%E7%B6%93%E9%96%A3%E7%94%B5%E8%84%91%E6%B8%B8%E6%88%8F%E6%80%BB%E7%9B%AE%E5%BD%95%EF%BC%88001-710%EF%BC%89.pdf

**EVIDENCE BOUNDARY:** this is a later collector/catalogue surface, not a contemporaneous Beijing-Waei product record. The literal `华议国际` string may be an original catalogue spelling, OCR/transcription error, or a different publisher identity; it must **not** be silently normalized to `华义国际`. Likewise, `2001C226` is treated as a catalogue-local identifier unless an independent source proves otherwise.

**Operational use:** `哇靠轰炸鸡`, `哇靠轰炸鸡完美中文版`, and `2001C226` are added only as search tokens. A result containing these tokens alone is emitted as `SEARCH_ONLY_NOT_STRICT`; it cannot qualify as a StoneAge 2.5 carrier without an independent Waei/StoneAge association.


## Refined preservation-index result — 2026-09-24

The exact-carrier probe was rerun after adding the catalogue-only aliases and retry logic.

- total source-named 2.5 carrier targets: **20**;
- 《轰炸鸡》 target queries: eight DiscMaster + eight Internet Archive metadata queries;
- DiscMaster strict hits: **0**;
- Internet Archive strict items: **0**;
- IA interesting carrier files: **0**;
- probe errors: **0**;
- generic IA query for `轰炸鸡`: **18 metadata items**, but **0** carried the independent Waei/StoneAge association required for a strict hit;
- `哇靠轰炸鸡`, `哇靠轰炸鸡 华议国际`, `2001C226 哇靠轰炸鸡`, `Chicken Shoot Waei`, and `Chicken Shoot StoneAge` all returned no strict preserved-carrier result on the tested indexes.

A modern Bilibili search surface labels a video **“经典射鸡老游戏：哇靠轰炸鸡中文版(射鸡英雄传1)”**, while modern game databases use `射鸡英雄传` for `Chicken Shoot`. This is useful only as a search alias/hypothesis because later GBA/Wii releases reuse the same title family and can easily create false positives.

**Operational boundary:** the DiscMaster/IA exact metadata route is now bounded for this carrier. Reopen it only when a new independently sourced Chinese/Waei package identity, installer filename, disc label, checksum, file tree or repost token appears.
