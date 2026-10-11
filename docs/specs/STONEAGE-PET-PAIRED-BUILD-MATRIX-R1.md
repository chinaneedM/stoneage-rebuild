# Original late-descendant PET equipment: paired build configuration evidence R1

## Scope

**SOURCE_ONLY_BUILD_ENTRYPOINTS_NEGATIVE_GATE**, original pinned `BismarckDD/Stoneage` commit `999ffdf1d220ec6666eb65339180689c9caf1876`. This audit verifies **which source macros the checked-in build scripts and selected project configurations imply**. It does not build either game program, run a real two-process connection, or assert any feature existed in Japan 1999 / Taiwan 1.0.

The previous source audit's shorthand “Debug and Release” was **imprecise**: these names appear as extra groups in `client/stoneage.vcxproj`, but the `client/stoneage.sln` **actual SolutionConfigurationPlatforms** selects `VER25_DEBUG|Win32` and `VER25_RELEASE|Win32`. The selected groups use `_SA_VERSION_SPECIAL`; the `client/build-client.ps1` default is **`VER25_Release`**, with no option for a version-80 profile in its accepted configuration set.

## Exact primary pinned files

| File path in original descendant | Git blob |
|---|---|
| client/build-client.ps1 | `7045da30a9e54a3ffba997069bb32cc2f9112e18` |
| client/stoneage.sln | `7dd2bf48f50aa3bd3439a6b1848088934cc0a9db` |
| client/stoneage.vcxproj | `373c0699a5df017f53e4ab7a7d64c3d6280a8578` |
| client/resources/version.h | `35bd4446a740a189c1ad9439e30e61fe169d5f46` |
| server/CMakeLists.txt | `1523d12c3543e3d2a8c3a1401f92d79d11d85413` |
| server/scripts/build-linux.sh | `17a6c21ad76634a4141383960549121bf76a1724` |
| server/scripts/build-windows.ps1 | `b9357b25a1cb5a0fd041d4c8a1b55ec53c2978ca` |
| server/gmsv/makefile | `8afd1f288a1d07a5cf0075af04e51e64741dcc81` |
| server/common/makefile | `263ef622f4c0c3ac495d783ff35b078277984d43` |
| server/gmsv/include/version.h | `b3fc0c80705973bc8d088287c98a5d66171bb6c2` |

## Verified matrix

| Source profile | PET macro after preprocessing | Meaning |
|---|---:|---|
| Client `version.h` by itself | Off | Header selects `_SA_VERSION_25` |
| Solution-selected VER25 build, `-D_SA_VERSION_SPECIAL` | Off | Defines version60, not version80 |
| Client **counterfactual** `-D_SA_VERSION_SPECIAL -D_SA_VERSION_80` | On | Header emits `_PET_ITEM` only inside optional version80 block |
| Server original `version.h` without external feature define | Off | Default does not define `_PET_ITEM` |
| Server **counterfactual** `-D_PET_ITEM` | On | Explicit override makes optional code visible |

The checked-in GNU make `CFLAGS`, Windows CMake `STONEAGE_WINDOWS_DEFINITIONS`, and their respective Linux/Windows wrapper scripts contain no direct `_PET_ITEM` override. The server's `version.h` declaring `_VERSION_80` is **not** the same as the PET flag; do not infer that it enables `_PET_ITEM`.

**Important limitations:** These results are a precise comparison of selected build configuration *sources*, not a successful compilation, linking, executable feature test, server deployment or actual client/server compatibility test. Environment/user-supplied compiler flag overrides and other unobserved build pipelines are unknown.

### Additional runtime artifact check

Read-only Git tree enumeration at pinned original commit `999ffdf1` (root tree `a49d8fb8beaf93e07e499d65723f16922ce3ee1f`) reported **950 tracked blobs**, **no tracked `.exe`**, but did list third-party libraries, including `shared/lua51/lua51.dll`. The public GitHub Releases collection for this repository returned zero entries during this check. These observations do **not** prove there is no independently archived executable or a compiled historical client/server pair elsewhere.

## Automatic evidence and classification

- Source-free reproducible audit: `tools/stoneage_pet_paired_build_matrix_audit.py`.
- Strict negative tests: `tests/test_stoneage_pet_paired_build_matrix.py` (combined with the prior source-only checks).
- `research/recovered/STONEAGE-PET-PAIRED-BUILD-MATRIX-R1.txt` and receipt `research/recovered/STONEAGE-PET-PAIRED-BUILD-ACCEPTANCE-R1.json`.
- Workflow `.github/workflows/validate-stoneage-pet-paired-build-matrix.yml`: Action `38146693748` / job `114491443906`, **SUCCESS**, 18 tests, exact reproduction of archived report bytes. Initial run `38146553529` failed because the server version header's dependency include paths were missing in the test harness; rerunning with checked-in gmsv/common include directories corrected the **test environment**, not the source evidence.

**FACT:** Default checked-in build entrypoint macro matrix is PET-off, with counterfactual preprocessing showing opt-in source visibility.

**OPEN:** Real feature-enabled matching binaries, build/deploy provenance, actual UI-to-server opcode127 traffic, item ownership/unique-code persistence, and JSS1999/Taiwan1.0 membership.

**DESIGN:** No approval to add later optional PET equipment to the reconstructed game. Historical pressure remains 2486=2465 bounded closed+18 OPEN+3 historical UB; no first-version promotion. Next investigation should seek verifiable external binary/client+server provenance rather than inventing a runnable 8.0 build from flags alone.
