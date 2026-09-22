# Gamer's Dream / JSS Archive Evidence — R1

Date: 2026-09-18

Purpose: record recoverable first-party/archived evidence from the original Gamer's Dream site that constrains the 1999 JSS retail client, the operating relationship between JSS and NTT Data/Gamer's Dream, and the post-JSS service transition.

## Evidence rule

Wayback captures of original first-party pages are treated as **A-grade archived first-party material** unless a stronger original artifact is recovered. A 2001 capture can preserve product facts about the 1999 release, but it does not automatically prove that every word on the page was unchanged since launch.

## 1. Original Gamer's Dream StoneAge product page

### Source

`SRC-JP-GD-STONEAGE-INTRO-ARCHIVE-01`

Archived URL:

https://web.archive.org/web/20010128123900/http://www.dp.gamersdream.ne.jp/intro/intro_sa.html

Wayback capture date: 2001-01-28

Original host/path: `www.dp.gamersdream.ne.jp/intro/intro_sa.html`

### FACT supported by the archived first-party page

The Gamer's Dream StoneAge product page identifies:

- genre: RPG;
- developer/publisher attribution: Japan System Supply;
- package price: 8,800 yen;
- release date: **1999-10-15**;
- required CPU: MMX Pentium 200 MHz or better;
- required free HDD space: at least 400 MB (plus OS swap space);
- required memory: at least 64 MB;
- required optical drive: 4x-speed or faster CD-ROM drive;
- network requirement: 33.6 Kbps or faster modem / Internet connection;
- video memory: at least 2 MB;
- DirectX 6.1-compatible video and sound hardware;
- mouse and keyboard.

The page instructs prospective players to first purchase the software package and then register for Gamer's Dream service. This is strong evidence that the commercial launch flow was package-based and that an install/client CD-ROM was part of the normal retail path.

### Research consequence

This materially strengthens the retail-media recovery target:

- the first-edition special/bonus CD should **not** be assumed to be the install disc merely because it is a CD-ROM;
- the official system requirements independently require a CD-ROM drive and tell users to buy the software package first;
- therefore the working model should keep at least two possible media roles distinct until original contents are inspected:
  1. the normal retail install/client medium;
  2. the advertised first-edition special/bonus CD.

### Still OPEN

- exact disc count in the standard and initial editions;
- whether the install disc and bonus/special CD are physically separate;
- disc labels and matrix codes;
- product/JAN code;
- install executable filename;
- client executable filename/version resource;
- file tree and hashes.

## 2. Original Gamer's Dream site capture range

### Source

`SRC-JP-GD-INDEX-ARCHIVE-01`

Archived index URL observed through Wayback:

https://web.archive.org/web/20001204061300/http://www.dp.gamersdream.ne.jp/index.html

The Wayback toolbar for this path reports captures beginning **1999-04-22** and continuing into 2002.

### Research consequence

This proves that recoverable snapshots of the Gamer's Dream site exist from before the September beta and October launch period. The current blocker is not absence of any archive, but recovering the correct historical paths/timestamps and linked assets.

Priority archived paths now include:

- `/index.html`
- `/intro/intro_sa.html`
- `/whats_new/`
- StoneAge server/status pages;
- registration pages;
- online shop/package pages;
- any beta/tester announcement or download path linked from August-September 1999 captures.

## 3. JSS / Gamer's Dream operating boundary after JSS failure

### Sources

`SRC-JP-GD-JSS-TRANSITION-2000-01`

Archived Gamer's Dream notice dated 2000-11-10:

https://web.archive.org/web/20010113210300/http://www.dp.gamersdream.ne.jp/whats_new/sa.html

Detailed companion page:

https://web.archive.org/web/20010210200933/http://www.dp.gamersdream.ne.jp/whats_new/sa2.html

Contemporaneous specialist-press corroboration:

https://www.4gamer.net/archive/200010/ripls.html

### FACT / high-confidence operating picture

The archived Gamer's Dream notice explains that JSS had been responsible for the StoneAge game application side, including software work such as defect correction and version updates, while Gamer's Dream handled the server/service operation and billing side.

Following JSS's October 2000 business collapse/bankruptcy, Gamer's Dream could continue server operation only in a reduced form and could no longer provide the same level of JSS-dependent technical support, content/event support, or client version upgrades.

The detailed notice also states that package sales through the Gamer's Dream online shop were stopped and that software version upgrades could no longer continue.

4Gamer contemporaneously reported in October 2000 that JSS had effectively ceased business, that LIFESTORM services/support ended, and that StoneAge support had ended while Gamer's Dream was determining whether service could continue.

### Research consequence

For archaeology, the project should distinguish:

- **JSS client/application artifacts** — executable, data, version upgrades, client-side fixes/content;
- **Gamer's Dream platform/service artifacts** — account registration, billing, server operations, platform pages and service notices.

This distinction matters when classifying recovered files and when deciding whether an archived Gamer's Dream file is part of the actual game client or only service infrastructure.

## 4. September 1999 beta evidence refinement

### Source

`SRC-JP-1999-PLAYONLINE-015`

The September 1999 *Play Online* issue additionally records:

- test period: 1999-09-01 through 1999-09-30;
- 200 reader tester accounts;
- application deadline: **1999-08-20**;
- application through a form, with lottery selection if oversubscribed.

The preserved page visibly contains an application-form URL / game-homepage information block.

### Newly recovered URL evidence — 2026-09-18

Search-index text extracted from the preserved *Play Online* PDF now consistently exposes the beta application host and path tail as:

- host: `www.dp.gamersdream.ne.jp`
- path tail: `PO/sa_apply.html`

The current indexed/OCR rendering places one ambiguous character immediately before `PO`, displaying the printed string approximately as:

`http://www.dp.gamersdream.ne.jp/[OCR-AMBIGUOUS]PO/sa_apply.html`

The same extraction also exposes the period root URLs `http://www.gamersdream.ne.jp/` and `http://www.titan.co.jp/` in the adjacent information block.

### Evidence status

**FACT:** the printed beta-application URL used the Gamer's Dream `www.dp.gamersdream.ne.jp` host and ended in `PO/sa_apply.html`.

**OPEN:** the exact character immediately before `PO` is not reliable in the current OCR/index extraction. It is rendered as a double-quote-like character by the search index. Do **not** silently normalize it into `/`, `~`, `%7E`, or another character until the scan itself or an archived URL record resolves it.

**TESTED SEARCH LEADS, NOT FACT:** the old-style user-directory spelling `/~PO/sa_apply.html`, its `/%7EPO/` encoded form, the plain `/PO/sa_apply.html` form, and corresponding bare-host variants were checked through Wayback Availability on six key dates from 1999-08-01 through 1999-09-30. All **30** requests completed and returned **0 archive captures**. This is an archive-coverage result only; it does not prove that the printed URL was or was not one of those spellings.

The complementary wildcard/index probe records **0 literal `PO/sa_apply.html` matches** on successful 1999 queries, but remains **PARTIAL_NO_MATCH** because several Wayback and host-wide requests failed. Reports:
- `research/recovered/STONEAGE-JSS1999-BETA-APPLY-ARCHIVE-R1.txt`;
- `research/recovered/STONEAGE-JSS1999-BETA-APPLY-CANDIDATES-R1.txt`.

### Research consequence

The beta archive search is now much narrower. The exact character before `PO` remains OPEN, but further blind ASCII-character enumeration is not justified. Priority should move to:

1. a readable scan/page image that resolves the printed glyph;
2. a preserved 1999 Gamer's Dream URL list/index that independently returns the original path;
3. linked tester/download/install pages discovered from other authenticated beta-era material.

Any future archive query can still use the known literal tail `*PO/sa_apply.html`, but a no-capture result must remain separate from a claim about what the magazine actually printed.

The beta recovery window should still include **August 1999**, not only September, especially tester instructions, registration and download paths.

## 5. Current recovery hypotheses to test

### HYPOTHESIS A — package client plus separate bonus disc

The strongest current model is that the retail package contained the normal install/client media and the initial edition additionally included a special/bonus CD. This is plausible because the official Gamer's Dream product page independently describes a package purchase requiring a CD-ROM drive, while separate period advertising and a surviving sealed-package listing refer to an initial-edition special/bonus CD.

This is **not yet FACT** until an original initial-edition package is opened/documented or another first-party contents list is recovered.

### HYPOTHESIS B — beta distribution through Gamer's Dream web/service infrastructure

The beta was recruited through Gamer's Dream/Play Online and likely used Gamer's Dream account/service infrastructure. However, the exact client distribution mechanism (direct download, mailed CD-ROM, magazine media, event media, or another route) remains OPEN.

## 6. Immediate next actions

1. Resolve the one ambiguous character in the printed beta application URL and match `*PO/sa_apply.html` to an August 1999 Wayback capture if one exists.
2. Recover any linked beta installation/download instructions and identify the filename/media.
3. Recover pre-launch/launch captures of `/intro/intro_sa.html`, the online shop, and related package pages.
4. Continue product/JAN/disc-label searches using the now-confirmed hardware/product metadata.
5. Do not merge the normal install/client disc and the initial-edition special CD into one artifact until direct evidence proves they are the same physical medium.
