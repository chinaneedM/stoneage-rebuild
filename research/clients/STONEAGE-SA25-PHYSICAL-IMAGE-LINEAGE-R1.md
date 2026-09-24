# StoneAge 2.5 physical-media image-lineage analysis — R1

## Scope

Derived visual-evidence analysis only. Public seller/collector image bodies were read transiently by GitHub Actions; no seller photographs or proprietary game/media bytes are committed to the repository.

Primary derived report:

- `research/recovered/STONEAGE-SA25-PHYSICAL-IMAGE-FINGERPRINTS-R2.txt`

## Evidence set

R2 successfully loaded:

- **11 full-size Ruten images** from three public StoneAge 2.5 physical-media listings:
  - `22632305238624` — boxed/new-user-package listing, 9 full-size images;
  - `21926883918096` — standalone StoneAge 2.5 disc listing, 1 image;
  - `22242541948520` — standalone StoneAge 2.5 disc listing, 1 image.
- **3 large images** from the Wanfang-disc collector page `https://www.shiqi.me/pt_17.htm`.

The known collector-reference image at `cos.stoneage.cn` remained connection-refused in this run, and two additional collector-mirror index hosts failed TLS verification. Those failures are missing-reference conditions, not negative visual evidence.

## FACT — the two standalone Ruten disc images are not independent visual evidence

The two standalone-listing images have different file hashes:

- item `21926883918096`: SHA-256 `86c69ca6ac3cbd3079becee6b5c4686d2cd6bb47a7e61d4adff295194af49579`;
- item `22242541948520`: SHA-256 `d3bdc123fa2495f2fa7f278cf1b2c931f52e9543d8cb0cb9372f5fa7fee21426`.

However, feature geometry shows a very strong shared visual-source signal:

- ORB matches: **1,605**;
- matches with Hamming distance <=64: **1,538**;
- RANSAC homography inliers: **743**;
- inlier ratio: **0.4831**.

This is far stronger than every other cross-listing pair in the same run.

### Evidence consequence

Until independent provenance proves otherwise, the two standalone listings must be treated as **one visual-source cluster**, not as two independent surviving-disc observations. Possible explanations include reuse/re-encoding/cropping of the same source photograph or very closely related imagery of the same printed surface. The metric does **not** prove that the two sellers possessed the same physical disc, and it says nothing about disc bytes.

## FACT — boxed-listing images are not near-duplicate with the standalone source cluster at whole-frame level

The strongest boxed-new-user-package versus standalone-disc comparison produced:

- RANSAC inliers: **50**;
- inlier ratio: **0.0472**.

Other boxed-vs-standalone pairs were lower. This is materially below the 743 / 0.4831 standalone-to-standalone near-duplicate signal.

### Evidence boundary

Whole-frame matching is sensitive to crop, scale, packaging, reflections, occlusion and the disc occupying only part of a seller photograph. Therefore this run does **not** prove that the boxed listing contains a different disc artwork or carrier family. It only shows that the boxed photographs are not simple near-duplicates of the standalone source image.

A disc-localized/crop-aware pass is the correct next test if the boxed listing must be related to the standalone disc family.

## FACT — Wanfang collector images form no near-duplicate match with the Ruten source cluster

The Wanfang page yielded three large recoverable images. Across Ruten-vs-Wanfang comparisons, the strongest result was:

- RANSAC inliers: **27**;
- inlier ratio: **0.0322**.

The standalone Ruten discs versus Wanfang images were likewise low (maximum 19 inliers in this run).

### Evidence consequence

No Wanfang image is a near-duplicate of the Ruten standalone visual source under the tested whole-frame metrics. This supports treating the Wanfang photographs as an **independent visual-source cluster**.

It does **not** prove different disc contents, different client builds, or even different printed carrier artwork; those require readable face/package identifiers or file-level evidence.

## Current classification

- Ruten standalone items `21926883918096` + `22242541948520`: **ONE VISUAL-SOURCE CLUSTER / not independent evidence**.
- Ruten boxed item `22632305238624`: **independent listing/photo set; carrier relation unresolved**.
- Wanfang ISBN/barcode collector set: **independent visual-source cluster; carrier class remains OPEN / UNCLASSIFIED-CARRIER**.
- Official-mainland collector reference: **not loaded in R2; no comparison conclusion**.

## Next technical step

1. Recover a working copy/mirror of the known mainland unified-client-disc reference image, or explicitly allow legacy TLS only for the already identified public collector-mirror hosts.
2. Add crop/local-region matching for boxed seller photographs so a disc occupying only part of a frame can be compared against standalone-disc references.
3. Preserve evidence independence: multiple marketplace URLs must not be counted as multiple specimens when their images collapse into the same visual-source cluster.
4. If any actual disc/file-tree bytes become publicly recoverable, stop image archaeology and perform file-level provenance/hashing immediately.
