# Default PET item build gates and equipment caller inventory — R1

Status: **SOURCE_ONLY_DEFAULT_BUILD_GATE_ACCEPTED**. Actions
38142524756/job114479121485 SUCCESS at tested commit
a6d3415e7d09ecf30002e37f2c62cef64f0436e4; all validation steps
green, 17 Python tests. Independently downloaded ZIP901 bytes SHA256
`5db979c903f34f11f1a3c99aab8b24269e858364d4aec962e2ea385d61cf3a67`.
Derived report1418 bytes SHA256
`59f2c994d6d5169553d0c8bd38ca47c2b4fe4ba9e603a49fa05bc86441a8925b`,
Git blob `2d5d55984972975fe769efd6adb5466731499e17`; byte-exact with
the committed report. This is the next bounded historical technical-evidence
gate after the source-only PET item identity report and native reuse report. It is **not** a production configuration or
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

## Accepted result

GCC preprocessing using pinned default include paths reports
`_UNIQUE_P_I=defined`, `_SIMPLIFY_ITEMSTRING=defined`, and
`_PET_ITEM=absent` in both source profiles. Both checked-in Linux GNU
make recipes have no explicit `-D_PET_ITEM` default; Bismarck's Windows
CMake target definition list also has no `_PET_ITEM`. Under these
defaults, the actual preprocessed Bismarck `char_item.c` has no
`CHAR_movePetItem` body or `CHAR_sendPetItemData` body, and
`char/pet.c` emits no `CHAR_sendPetItemData` calls. Counterfactual
`-D_PET_ITEM` enables the original raw equipment body, whose source
contains physical-index swaps via `CHAR_setItemIndex`.

The recursive scan of the configured source C directory finds exactly
one Bismarck `CHAR_movePetItem` occurrence: its **definition at
`char/char_item.c:2655`**; it finds **zero syntactic direct C call
sites**. Gavin has no such definition or call site in its scanned C
directory. This is stronger than only observing a `#ifdef`, but does
not exclude a generated entry, dynamic call, alternate source tree,
other languages, or deployment flags.

The Gavin preprocessor proof inspects the precise
`CHAR_makePetStringFromPetIndex` body and finds no gated item
serialization call in its default form; it does not rely on the raw
macro name surviving preprocessing.

**FACT:** Default checked-in build recipe PET equipment excluded in
tested late source profiles. **OPEN:** Production binaries; enabled
other-version protocol dispatch; naturally reachable PET-held item;
whether actual object unique-code survives or regenerates after
release/reuse. Do not promote this to evidence about Taiwan1.0/JSS1999
or treat the original broken-index synthetic experiment as normal play.

Receipt:
`research/recovered/STONEAGE-PET-ITEM-BUILD-GATE-ACCEPTANCE-R1.json`.
