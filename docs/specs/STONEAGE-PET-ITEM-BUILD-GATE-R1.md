# Default PET item build gates and equipment caller inventory — R1

Status: **REMOTE VALIDATION PENDING**. This is the next bounded historical
technical-evidence gate after the source-only PET item identity report and
native released-slot reuse report. It is **not** a production configuration or
1999 JSS / Taiwan-v1.0 identity claim.

## Question and provenance

Given exact pinned late descendant sources (Gavin
`1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`; Bismarck
`999ffdf1d220ec6666eb65339180689c9caf1876`), determine whether
PET-item equipment and persistence is compiled under the *checked-in default*
make/header setup and locate the raw C call sites (not inferred gameplay
reachability) for Bismarck `CHAR_movePetItem`.

### Source orientation

- Both default `include/version.h` headers define `_UNIQUE_P_I` and
  `_SIMPLIFY_ITEMSTRING`; neither defines `_PET_ITEM`. Previous audit
  directly fingerprinted eight source/header blobs, 22 native function
  bodies and found their default PET persistence branches inactive.
- Gavin `char/char_base.c` PET save branch is under
  `#ifndef _SIMPLIFY_ITEMSTRING`, which its default header disables.
- Bismarck `char/char_item.c` contains a real
  `CHAR_movePetItem` body under `#ifdef _PET_ITEM`, with
  `CHAR_setItemIndex(char_index,...)` and
  `CHAR_setItemIndex(petindex,...)` exchanging physical global indices.
  There is a PET send body and `pet.c` call sites under
  `_PET_ITEM`. **Their raw presence is not compiled-path evidence.**
- Gavin checked-in `gmsv/src/Makefile` and `char/makefile` and
  Bismarck Linux `server/gmsv/makefile`, `char/makefile`, and Windows
  `server/CMakeLists.txt` must be read and SHA-pinned to distinguish
  declared default compile flags from production/deployment configuration.

## Reproducibility gates

1. Reconstruct pinned sources transiently in GitHub Actions, verify source
   identity, and verify checked-in build-script Git blobs exactly.
2. Invoke GNU GCC preprocessing with checked-in build include search paths;
   inspect actual macro-set output, not a guessed feature list. Require
   `_UNIQUE_P_I`/simplification on and `_PET_ITEM` off.
3. Confirm that the Bismarck `CHAR_movePetItem` function does not appear
   in default `char_item.c` preprocessed C, and *does* appear only in an
   explicitly labeled counterfactual `-D_PET_ITEM` run. The latter
   does not represent historical deployment or user-facing reachability.
4. Confirm Bismarck default `pet.c` excludes PET item send calls;
   confirm Gavin default excludes the gated PET persistence path.
5. Recursively inventory exact source C occurrences of `CHAR_movePetItem`;
   label definitions separately from other occurrences. Only provenance
   paths, counts and digests—not source bodies or proprietary assets—may
   be committed.
6. Require strict negative tests that reject claims of default enablement,
   live deployment, natural alias reachability or first-build equivalence.
   Archive the reproducible report, digest-check Actions artifact, and
   maintain historical chronology if the gate passes.

## Evidence classification and limitation

**FACT (source-only):** Raw Bismarck `CHAR_movePetItem` implements
a compile-conditional PET equipment swap; default header does not define
the macro. A real `#ifdef` branch is a possible feature, not proof it
was enabled. Build-path preprocessing is a stronger bounded check but
cannot certify alternate make invocations, binary compile flags or actual
client/runtime protocol entry.

**OPEN:** Exact real call sites under active compiled dispatcher;
reachable PET equip requests, whether a PET can carry the specific former
enemy drop index from ordinary gameplay; physical-index-to-unique-code
lifecycle after login/save/release; earliest Taiwan/JSS provenance.

**DESIGN:** Do not import historical stale-pointer behavior into the modern
single-player inventory system without a separate design decision.

No new pressure promotions: 2486 = 2465 bounded closed + 18 OPEN + 3
historical UB. This gate cannot close natural reachability or first-release
identity.

Execution: `python -m tools.stoneage_pet_item_build_gate_audit` with
`--gavin-dir` and `--bismarck-dir` pointing to exact pinned checkouts.
