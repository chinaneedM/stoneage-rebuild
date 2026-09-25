# StoneAge early Ruten regional physical carriers — R1

## Scope

This note records a 2026 public Ruten physical-package control set that helps distinguish Taiwan and Mainland StoneAge carrier families and provides exact recovery identifiers. It is **carrier/provenance research**, not a claim that any current marketplace item is a clean client or byte-identical to an operator-era release.

Canonical derived reports:

- `research/recovered/STONEAGE-EARLY-RUTEN-CARRIERS-R1.txt`
- `research/recovered/STONEAGE-EARLY-RUTEN-CARRIER-FINGERPRINTS-R1.txt`
- `research/recovered/STONEAGE-MAINLAND-RETAIL-ISBN-PROBE-R1.txt`
- `research/recovered/STONEAGE-MAINLAND-PACKAGE-MIRROR-MATCH-R1.txt`

## FACT — Taiwan package control

Ruten item `22625938996449` exposes six public full-size photographs for a Traditional-Chinese StoneAge package. The visible front/package sticker states that StoneAge supports the **WGS billing system** and advertises WGS point-card availability through convenience stores, 3C retailers and chain bookstores.

A second current listing, `22631285251243`, does **not** provide an independent five-photo specimen:

- corresponding images 0–4 have identical dHash values;
- one pair is byte-identical by SHA-256;
- the other corresponding pairs produce 3,609–4,702 RANSAC inliers with 0.9904–1.0000 inlier ratios.

Therefore these two listings are treated as a **reused-photo family**, not two independent physical-carrier observations. The sixth image present on `22625938996449` remains additional material from that source set.

The package has **not** been equated to the accepted Taiwan Waei/JSS v1.0 Redump 104630 baseline. The Redump baseline remains independently anchored by:

- model/mastering token `P-RPG-0008`;
- barcode `4710739350098`;
- mastering ring `華義國際股份有限公司 石器時代 V1.0 P-RPG-0008`.

No exact `P-RPG-0008` or `4710739350098` identifier has yet been recovered from the Ruten Taiwan-package photographs.

## FACT — Mainland package controls

Ruten item `22636573895893` exposes a Simplified-Chinese StoneAge retail box with visible WAEI/WGS branding. The small photographed back-panel identifier area was initially transcribed as **`7-900032-57-0` / `9787900032570`**, but that reading is now explicitly **UNCONFIRMED**:

- the transcribed 10-digit value fails the ISBN-10 checksum;
- the transcribed 13-digit value fails the EAN-13 checksum;
- if the preceding photographed digits were read correctly, checksum-consistent final-digit hypotheses would be **`7-900032-57-6` / `9787900032577`**;
- neither final digit is independently readable/confirmed enough from the current photograph to promote either pair as FACT.

Therefore the printed identifier remains an **OPEN photo-reading question**, not an exact package identity. This candidate is separate from the previously recorded Wanfang StoneAge 2.5 disc ISBN/barcode and must not be conflated with it.

Ruten item `22638643800877` exposes a boxed StoneAge disc/package photograph whose disc face visibly includes **`www.waei.com.cn`**. This is useful Mainland/Beijing-Waei carrier context, but the photograph does not establish disc filesystem contents, mastering, or version.

Item `22631284715652` is retained as a Beijing-Waei/new-user-package visual control only. Marketplace wording such as “正版”, “原版軟體”, “新手包” or “全版本” remains a seller claim unless independently authenticated.

## FACT — 2.0-labelled mirror relationship for the Beijing-Waei newbie control

A later public collector mirror at `https://www.sa85.com.cn/shiqi2710.html` is explicitly titled **`石器时代周边收藏客户端礼包篇（五）2.0版本礼盒`**. It is a later collector source, not contemporaneous operator evidence.

Its first article-body package photograph (`mirror-20:2`, SHA-256 `bf736ab3ba6d860c0faece641ae8a199a35ed5e6616ddc883ad001b5301e6c6f`) produces unusually strong SIFT/RANSAC overlap against all four photographs from Ruten item `22631284715652`:

- image 0: **400 inliers / 0.8403**, target coverage **0.9070**;
- image 1: **328 / 0.8059**, target coverage **0.9054**;
- image 2: **317 / 0.8212**, target coverage **0.8793**;
- image 3: **129 / 0.6386**, target coverage **0.2838**.

The first three matches cover almost the full collector reference image while occupying only a smaller region of the larger Ruten photographs. This is materially stronger than ordinary shared-logo/artwork overlap and supports a **strong shared package/photo-artwork family** relationship.

The geometry is not treated as proof of the same physical box or same photograph: the homography sanity flag is false for these four rows and the projected area ratios are large, consistent with crop/embedding/perspective differences. Therefore the correct historical status is:

- **FACT:** the current Ruten `22631284715652` photo family strongly overlaps the package pictured by a later source explicitly labelled as a 2.0-version gift box;
- **HYPOTHESIS / BOUNDARY:** this increases the plausibility that the surviving package belongs to the 2.0-era package family, but does **not** independently prove its original release version, disc contents, pressing, installer bytes or clean-client status.

The current 1.x comparison mirror at `https://shiqi.ws/post/10248.html` is publicly readable in CI but still does not expose a usable package photograph. Follow-up run **36097423535** completed successfully after adding raw HTML/CSS/escaped-URL discovery; it found only `https://shiqi.ws//zb_users/plugin/MoreLinksGame/img/dh_bg.jpg`, a **1×31** plugin background that was correctly skipped. Therefore the tested current page surface is **bounded for usable 1.x package images**. Reopen this visual-control route only from an alternate mirror, explicit article-image URL, archived page body, or another source-labelled 1.x package photograph.

## Preservation probe for the initial transcription and checksum-consistent hypotheses

GitHub Actions run `36096287039`, attempt 2, completed successfully.

The R1 probe tested the **initial photo transcription**:

- `7-900032-57-0`
- `7900032570`
- `9787900032570`
- `石器时代 网络游戏 华义`
- `StoneAge 北京华义 WAEI`

against DiscMaster and Internet Archive metadata. These queries remain valid records of what was tested, but the first three strings must not be described as confirmed printed identifiers.

Result:

- strict DiscMaster hits: **0**
- strict Internet Archive items: **0**
- probe errors: **0**

The one raw DiscMaster row returned for the hyphenated ISBN failed the strict StoneAge/operator identifier test and is not promoted as a candidate.

R2 then tested the checksum-consistent hypotheses **`7-900032-57-6` / `7900032576` / `9787900032577`** separately. GitHub Actions run **36097696696** completed successfully. Across all eight R2 queries (initial transcriptions, checksum hypotheses and Waei/StoneAge context):

- strict DiscMaster hits: **0**
- strict Internet Archive items: **0**
- probe errors: **0**

The hyphenated initial and hypothetical ISBN strings each produced one raw DiscMaster row, but neither row passed the strict StoneAge/operator filter and neither is a candidate.

Operational consequence: the tested DiscMaster/IA surfaces are now **bounded for both the initial transcription and the checksum-consistent hypotheses**. Neither string family is promoted as the printed identifier. Reopen this identifier-reading route only from a clearer photograph, independent catalogue record, new preservation corpus, disc/file token, checksum, volume label, or public media dump.

## Visual-evidence boundary

The early-carrier fingerprint run recovered **25/25** target images with **0 errors**.

Very high one-to-one similarity between the two Taiwan marketplace listings is sufficient to identify reused photographs. Lower cross-package feature matches are expected because StoneAge boxes reuse characters, logos and artwork; they are not evidence of the same physical disc/package.

No current visual result establishes:

- same physical carrier;
- same optical pressing/mastering;
- same installer/client bytes;
- exact release version;
- clean-client status.

## Status

**ACTIVE REGIONAL CARRIER CONTROL SET / MAINLAND PRINTED IDENTIFIER FINAL DIGIT OPEN.**

Next high-value evidence remains a provenance-preserving public read/dump/file tree or exact matrix/volume/installer identifier tied to one of the surviving physical carriers.
