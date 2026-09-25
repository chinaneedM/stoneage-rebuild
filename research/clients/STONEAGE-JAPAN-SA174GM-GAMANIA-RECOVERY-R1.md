# StoneAge Japan `sa174gm.exe` Gamania Mirror Recovery — R1

Research date: 2026-09-25

## Scope

This note records a newly resolved Japanese StoneAge client filename/distribution branch:
`sa174gm.exe`.

It is deliberately kept separate from the already recovered Hangame launch-window
identity `sa174hg.exe`. No equality, rename relationship, version equality, or
byte identity is asserted without recovered bytes.

## Source 1 — 2008 IPvE post preserving a Gamania download URL

Public page:
- https://www.ipve.com/bbs/viewthread.php?extra=&page=5&tid=84383

Literal post metadata/content:
- author shown: `SmileBoy`
- timestamp shown: **2008-08-07 21:10**
- the post identifies the Japanese StoneAge official site as:
  `http://www.stoneage.to`
- it gives the download address:
  `http://file2.gamania.co.jp/sa/sa174gm.exe`
- it gives the account-registration path under `stoneage.to`
- it says the material was reposted from `石器的天空`.

Classification:
- **FACT**: by 2008 this public community post associated the Japanese official
  StoneAge service with the exact Gamania-hosted `sa174gm.exe` URL.
- **OPEN**: when that exact Gamania URL first entered service, what build it
  contained, whether it changed in place between 2003 and 2008, and whether the
  2008 payload was byte-identical to any 2003 launch client.

## Source 2 — 2017 Japanese player survival testimony

Current indexed 5ch thread:
- thread title: `【復活】StoneAge ストーンエイジ 第50記【日本】`
- indexed thread ID: `1360616745`

Search-indexed posts include:
- a player reporting that an old HDD still contained the StoneAge client under
  the `SA174gm` identity and that it could still be installed;
- a later indexed post asking whether to upload `sa174gm.exe` somewhere.

Classification:
- **MODERN COMMUNITY CORROBORATION** only.
- This independently supports that `SA174gm / sa174gm.exe` was a real
  remembered/stored Japanese-client filename rather than a 2020 naming invention.
- No surviving re-upload URL, checksum, size, or provenance-preserving copy was
  recovered in the indexed search pass.

## Source 3 — 2020 shiqi.la surviving attachment carrier

Public thread:
- https://shiqi.la/forum.php?mod=viewthread&tid=16671
- title:
  `sa174gm.exe日版石器时代主程式安装档2003年12月11日`
- post timestamp: **2020-06-05 08:16:13**
- author: `shiqila`

Visible thread text calls it a Japanese original StoneAge installer and exposes
two attachment metadata records:

1. Installer archive
   - visible filename: `sa174gm[解压密码www.shiqi.la].rar`
   - visible size: **194.24 MB**
   - upload timestamp shown: **2020-06-05 08:13**
   - visible price/access control: **10 石币**
   - current Discuz token decodes to:
     `675|a66473d6|1790135737|0|16671`
   - therefore the stable attachment-id component is **675**.

2. Installed/portable tree archive
   - visible filename: `Stoneage.rar`
   - visible size: **174.72 MB**
   - upload timestamp shown: **2020-06-05 08:15**
   - visible price/access control: **15 石币**
   - current Discuz token decodes to:
     `676|6f16f0f4|1790135737|0|16671`
   - stable attachment-id component: **676**.

Anonymous attachment requests currently return HTTP 403. No login, payment,
token-forging, or access-control bypass is attempted by this project.

### Important date boundary

The thread title contains **2003-12-11**, but the page itself is a 2020 community
upload. Until a contemporaneous 2003 first-party page, file timestamp from
authenticated bytes, archived original directory listing, or other independent
period source confirms that date, **2003-12-11 remains an attributed later claim,
not a project FACT**.

## Relationship to the recovered Hangame launch identity

Already established first-party evidence in this repository:
- archived official Hangame download page, replay timestamp
  **2003-12-14 05:10:53 UTC**;
- exact launch-client URL:
  `http://hangame.gamania.co.jp/stoneage/sa174hg.exe`;
- official page display-size token: **248 MB**;
- independent contemporaneous Mado no Mori metadata identifies the Japanese
  beta client as version **1.74a**, date field **2003-12-12**.

New identity:
- `http://file2.gamania.co.jp/sa/sa174gm.exe`

### HYPOTHESIS only

The suffixes and hostnames make a distribution-channel interpretation plausible:
- `hg` may designate the Hangame-distributed package;
- `gm` may designate a Gamania-distributed package.

This is **not a FACT**. Filename morphology cannot establish:
- same executable/client build;
- same archive members;
- same installer technology;
- same release date;
- same bytes;
- whether one is a later replacement of the other.

Only recovered payloads can close that question.

## Public recovery pass

General current-web exact searches were run for:
- `sa174gm.exe`
- exact Gamania URL
- `SA174gm`
- RAR/ZIP/upload/mirror/P2P variants
- exact shiqi.la attachment filename
- Archive.org/DiscMaster-oriented exact queries.

Results:
- the 2008 Gamania URL record, 2017 Japanese-player survival references, and
  2020 shiqi.la attachment carrier were recovered;
- no independently indexed public ISO/EXE/RAR payload or surviving 2017
  re-upload URL was recovered in this pass.

A dedicated CI probe has been added:
- `tools/stoneage_japan174a_gamania_mirror_probe.py`
- `.github/workflows/probe-stoneage-japan174a-gamania-mirror.yml`

The probe checks exact Wayback/Availability/Arquivo/Internet Archive surfaces and
may transiently stream one exact public Wayback object for hash/size only if a
public HTTP-200 capture exists. It never commits client bytes.

## Evidence classification

- **FACT**: `sa174gm.exe` is independently attested by a 2008 Japanese-service
  download post and later Japanese player recollection.
- **FACT**: the 2008 post supplies exact historical URL
  `http://file2.gamania.co.jp/sa/sa174gm.exe`.
- **FACT**: a 2020 community archive carrier exposes an installer RAR labelled
  `sa174gm`, 194.24 MB, attachment ID 675, plus a 174.72 MB installed-tree
  archive, attachment ID 676.
- **OPEN**: archive bytes/hashes/file tree; the current access-controlled
  attachments are not anonymously recoverable.
- **OPEN**: whether `sa174gm.exe` is version 1.74a specifically.
- **OPEN**: whether the later claimed 2003-12-11 date is authentic.
- **OPEN**: any byte relationship between `sa174gm.exe` and official
  `sa174hg.exe`.

## Operational consequence

The Japanese bridge search now has two exact client identities instead of one:
1. first-party launch-window Hangame `sa174hg.exe` / 248 MB display anchor;
2. Gamania-hosted `sa174gm.exe`, corroborated by a 2008 URL and a later
   surviving attachment carrier.

Future recovery must search both names independently and compare recovered bytes
before merging the lineages.

Canonical proposed source IDs:
- `SRC-JP-2008-IPVE-SA174GM-MIRROR-01`
- `SRC-CN-2020-SHIQILA-SA174GM-ATTACHMENT-01`
