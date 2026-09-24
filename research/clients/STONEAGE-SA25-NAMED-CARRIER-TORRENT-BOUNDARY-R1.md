# StoneAge 2.5 source-named carrier torrent boundary — R1

## Purpose

Close the ambiguity between a **lexically similar old-disc image** and the exact January/February 2002 physical-media issues explicitly named by contemporaneous StoneAge 2.5 upgrade instructions.

This record concerns carrier identity only. It does not infer client payloads from magazine/disc titles.

## Primary period evidence

Two contemporaneous StoneAge distribution pages independently preserve the same carrier list:

- Sina Games, `《石器时代2.5》升级方法`: https://games.sina.com.cn/newgames/0202/02057854.shtml
- 17173, `《石器2.5--精灵王传说》升级办法`: https://news.17173.com/z/stoneage/banben/sa25-up.htm

The issue-specific media are:

- `《电脑报——游戏世界》2002年2月号`
- `《游戏王》2002年2月号`
- `《家庭电脑世界》2002年2月号`
- `《PC任我行》2002年2月号`
- `《电脑爱好者光盘——玩游戏》2002年2月号`
- `《软件时尚》光盘刊 2002年2月号`
- `《水晶宝合——锐》2002年2月号`
- `《大众软件CD——大众游戏》2002年2月号`
- `《CHIP新电脑》2002年2月号`
- `《网上俱乐部——游戏吧》2002年2月号`
- `《大众电脑光盘版——网吧乐园》2002年2月号`
- `《计算机与航空》2002年1月号`
- `《中学生电脑》2002年攻略特刊`

The same sources separately name `《轰炸鸡》`, 腾图/圣比尔 StoneAge 2.5 guides, 网迷 `《网络游戏介绍》`, and the Beijing-Waei 2.5 retail packs.

## Old-disc torrent cross-scan result

The public 老光盘群 `allseeds.zip` snapshot (89 torrent metadata entries) was re-scanned with **issue-specific date gating**, not generic magazine-name matching.

Result:

- strict target torrents: **0**
- strict target paths: **0**
- strict carrier labels: **0**
- lexical-neighborhood torrents: **12**
- lexical-neighborhood paths: **37**
- errors: **0**

Important rejected near-neighbors include:

- `电脑报配套光盘之游戏世界200201.iso` — January 2002, while the StoneAge carrier is explicitly **February 2002**;
- `电脑报配套光盘之游戏世界200112.iso` — December 2001;
- `家庭电脑世界 2001年4月 ... .iso` — wrong year/month;
- generic `游戏王` discs without the explicit February-2002 issue identity.

The tested torrent snapshot therefore contains **no exact source-named magazine/periodical carrier** for StoneAge 2.5.

## Search-engine follow-up

Exact public-web searches were also run for the source-attested issue names plus `ISO` / `光盘` / product terms. The tested search surface returned the contemporaneous distribution pages and later retrospective/package pages, but no exact February-2002 magazine-disc image or January-2002 `计算机与航空` disc image suitable for payload inspection.

This is a bounded search result, not proof that the media are lost.

## Evidence boundary and next trigger

Do **not** promote a nearby month, generic magazine title, later compilation, or same-name disc to a StoneAge 2.5 carrier.

Reopen this route only when at least one of the following appears:

- exact issue/date + disc image filename;
- exact issue/date + ISO/IMG/NRG/CUE/BIN carrier;
- disc photo exposing issue/date or publisher identity;
- contemporaneous table of contents/file list naming StoneAge 2.5;
- independently preserved repost with a checksum or original filename.

Derived scanner output:

- `research/recovered/STONEAGE-SA25-NAMED-CARRIER-TORRENTS-R1.txt`

Status: **BOUNDED ON CURRENT OLD-DISC TORRENT SNAPSHOT / OPEN GLOBALLY.**


## Adjacent preserved issue anchor

A modern preservation/catalog surface independently exposes the immediately preceding issue:

- title: `电脑报配套光盘之游戏世界 2002 年01月 (配套光盘)`
- preserved filename: **`GAMEWORLD200201.iso`**
- size: **657,821,696 bytes (627.3 MB)**
- SHA1: **`6241658796F0DF05199F39154E2F4E8D18330837`**
- public metadata page: https://www.shopmsdn.com/detail-%E7%94%B5%E8%84%91%E6%8A%A5%E9%85%8D%E5%A5%97%E5%85%89%E7%9B%98%E4%B9%8B%E6%B8%B8%E6%88%8F%E4%B8%96%E7%95%8C2002%E5%B9%B401%E6%9C%88%28%E9%85%8D%E5%A5%97%E5%85%89%E7%9B%98%29-4210.html

This independently corroborates the old-disc torrent path `电脑报配套光盘之游戏世界200201.iso` as a real preserved January-2002 issue family.

### Inferred search token only

Because the verified January image uses `GAMEWORLD200201.iso`, the adjacent February token **`GAMEWORLD200202.iso`** is a high-value *search hypothesis*. It is **not** promoted to a historical filename fact until an independent February issue record or carrier exposes that filename.

Operational consequence: the generic 89-torrent rescan remains closed, but exact preservation-index searches may be reopened once for `GAMEWORLD200202` / the compact February issue token. If those exact searches are negative, do not continue generating month/filename guesses without new evidence.


### Adjacent-token preservation-index closure

A bounded metadata-only probe tested the inferred February token family against DiscMaster and Internet Archive:

- `GAMEWORLD200202`
- `GAMEWORLD200202.iso`
- `电脑报配套光盘之游戏世界200202`
- `电脑报 游戏世界 2002年2月`

Result:

- DiscMaster candidate hits: **0**
- Internet Archive metadata items: **0**
- Internet Archive candidate files: **0**
- errors: **0**

Derived report: `research/recovered/STONEAGE-SA25-GAMEWORLD-200202-PROBE-R1.txt`.

**Operational boundary:** `GAMEWORLD200202.iso` remains an inferred search token only. Do not continue generating adjacent filename guesses (for example `GAMECD0202`) without an independent source that supplies a new exact token. Reopen only from an exact February-2002 issue record, checksum, file listing, disc photograph, mirror URL, or preserved media entry.
