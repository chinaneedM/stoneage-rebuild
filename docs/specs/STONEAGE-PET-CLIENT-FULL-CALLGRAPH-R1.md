# Pinned Bismarck client PET sender — complete source inventory and guarded UI callers R1

Status: **FULL_PINNED_CLIENT_SOURCE_ONLY_GATE**. This is a bounded late-descendant source evidence record, **not** an original Taiwan v1.0 or JSS1999 feature attribution and **not** a deployed runtime packet proof.

## Exact provenance and coverage

- Original repository: `BismarckDD/Stoneage`, fixed commit `999ffdf1d220ec6666eb65339180689c9caf1876`, entire original `client/` tree `511d9b24376c6858b70ab3015e36f5007bfd565a`.
- Transient clean checkout on GitHub Actions, whole pinned tracked `client/` recursive C/C++/header inventory: **237** files, content identity digest (sorted path + Git blob): `919703b218e8a4a417c5500bf77592bfc763286ca79b0fb47ffca92731ab4175`.
- Exact source-only report: `research/recovered/STONEAGE-PET-CLIENT-FULL-CALLGRAPH-R1.txt`; reproducible scanner `tools/stoneage_pet_client_full_callgraph_audit.py`; strict mutation controls `tests/test_stoneage_pet_client_full_callgraph.py`; GitHub Actions `validate-stoneage-pet-client-full-callgraph.yml`.
- Original file identity pins: `client/resources/version.h` `35bd4446a740a189c1ad9439e30e61fe169d5f46`; `client/stoneage.vcxproj` `373c0699a5df017f53e4ab7a7d64c3d6280a8578`; `client/stoneage/proto/protocol.h` `bb70087ef1b1915748da23935584eda2c8178cb0`; `client/stoneage/proto/protocol.cpp` `17f1900d8845c15308a4b429905ec009e5fd4c0f`; `client/stoneage/system/menu.cpp` `62754fdd0db1b84c358d61418d253012d149e1d4`; `server/common/gmsv_server.h` `708fe1b9f73be4952677fda474f10e86d9a56306`; `server/gmsv/include/version.h` `b3fc0c80705973bc8d088287c98a5d66171bb6c2`.

## Actual bounded source findings

1. **Version profile:** pinned `client/resources/version.h` selects `_SA_VERSION_25`. Both checked-in Visual Studio project Debug and Release definitions additionally set `_SA_VERSION_SPECIAL`; GCC header preprocessing with this flag enables `_SA_VERSION_60` but does **not** enable `_SA_VERSION_80` or `_PET_ITEM`. `_PET_ITEM` is under the 8.0 version conditional. Explicit **counterfactual** `-D_SA_VERSION_80` enables it. No claim is made about unobserved production overrides or a fully built Windows binary.
2. **Protocol:** under `_PET_ITEM`, `client/stoneage/proto/protocol.h:462` declares `lssproto_PetItemEquip_send`; `client/stoneage/proto/protocol.cpp:2280` defines it, encoding the five PET item arguments/checksum and sending optional **127**. The optional server receive opcode is **127**, and an earlier separately accepted source gate follows decoder → `GmsvServer_PETITEM_recv` → `CHAR_movePetItem`.
3. **Three real lexical calls in original pinned UI source** (missing from the previous GitHub master-indexed search): `client/stoneage/system/menu.cpp:14824` on item drag/drop within the PET equipment window, with selected PET and mounted-PET restrictions; `:14966` on double-click of a PET-target item, with warp and riding constraints, passing `-1` target slot; `:15333` on drag out from the PET equipment window, passing `-2`. Every found call is situated within a local `#ifdef _PET_ITEM` region.
4. **Full lexical inventory:** exactly five sites across 237 tracked client source/header files: one declaration, one definition and **three guarded UI call sites**; source scan is not runtime coverage. The first workflow correctly failed a mistaken expectation of zero callers and forced an evidence correction rather than falsely accepting the narrower indexed search.

## Classification and exclusions

**FACT (late pinned source only):** Exact pinned UI caller source paths and compile-conditional packet semantics above.

**OPEN:** Effective deployed _PET_ITEM client/server compiler flags; whether a production 8.0 client/server pair actually built and executed these paths; genuine UI-originating request and server-side actor/item owner identity transition; save/load/unique-code state, early Taiwan v1.0/JSS1999 equivalent.

**DESIGN:** No decision to reproduce an optional later pet-equipment feature in the new game. Do not add it merely because a late-source branch exists.

The source-only report supersedes **only** the previous inference from GitHub indexed search that declaration/definition were the only client references. It preserves earlier verified server-source findings and negative compile gates. Proprietary source/files/assets are not copied to the project repository.

Historical pressure unchanged: 2486 total = 2465 bounded closed + 18 OPEN + 3 historical UB; zero early historical promotions. Current highest NEXT is compile-approved, client-authenticated packet/handler reachability in a late descendant followed by a *non-synthetic* owner/unique-code lifecycle witness, only where provenance supports it.
