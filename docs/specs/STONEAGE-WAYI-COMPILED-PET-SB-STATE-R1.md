# Wayi compiled PET S/B display-state receiver R1

Status: **STATIC COMPILED CLIENT DISPLAY STATE**. Native owner/save/drop/unique-code and matching-server gates remain OPEN. Accepted actual20060915184620 operator-linked sa.exe response369152 bytes/packedSHA2564b5a059b45b589b609ca925d210d76838be1e970b805fab3df863b7d563fbb38; UPX output921600 bytes/SHA2564193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63. Original never executed or committed; mutable2005 header is not original2005 release identity.

## Receive chain

At0x912c8 the compiled dispatcher compares logical46. String field2 is decoded by0x90860 at0x912d4; checksum field3 by0x90740 at0x912e2. Mismatch0x912f0 bypasses callback. Helper0x65480 is an immediate RET; successfulcall0x9130d reaches callback0x60090.

Callback examines signed data[0], subtracts0x42(B), bounds index0..22 and uses byte-index table0x620d0 plus address table0x62094. Resolving those raw tables yields **B→0x61d0b**, with all23 category/default rows preserved in metadata. B body reads signeddata[1]-48 and advancesdata2 bytes. No digit/pet-range comparison appears within the observed B body; this does not prove absence of every upstream check. No malformed native packet was generated or executed.

This is a separate incoming **S46/B** state path. Send127 does not imply a127 acknowledgement, and causal correspondence between a sent equipment operation and this state update remains unobserved.

## Seven slots, fourteen fields, fixed native layout

Token-loop starts2, adds14, compares against100 and branches signedJL to0x61d2a:values2,16,30,44,58,72,86. Name extraction usesloopvalue-1, so each slot consumes14 fields. Byte-slot offset advances **0x184=388**. Empty name clears97 DWORDs, also388 bytes. Nonempty name sets WORDuseFlag1 atoffset220.

Affine interpretation of aligned0x61d88..0x61d9a yields `pet_index*2840 + slot_byte_offset`; slot_byte_offset advances388. RecordoriginRVA0x430def4. Therefore observed displayrow address is `0x430def4 + pet_index*2840 + slot_index*388`. The petstride is0xb18; do not infer exact complete C header layout from this alone.

| Field within slot | Semantic name from pinned source | Record offset | Compiled write/storage observation |
| --- | --- | --- | --- |
| 1 | name | 230 /0xe6 | copy only length<=28 |
| 2 | name2 | 259 /0x103 | copy only length<=16 |
| 3 | color | 0 | DWORD, negativeclamped0 |
| 4 | memo | 276 /0x114 | copy only length<=84 |
| 5 | graNo | 4 | DWORD |
| 6 | field | 222 /0xde | WORD |
| 7 | target | 224 /0xe0 | WORD, signed>=100 normalization |
| 8 | level | 8 | DWORD |
| 9 | sendFlag | 228 /0xe4 | WORD |
| 10 | damage | 361 /0x169 | copy only length<=16 |
| 11 | pile | 12 | DWORD |
| 12 | alch | 16 | stringcopy, no analogous guard in observed sequence |
| 13 | type | 377 /0x179 | BYTE |
| 14 | jigsaw | 378 /0x17a | stringcopy, no analogous guard in observed sequence |

UseFlag220/0xdc and deadTargetFlag226/0xe2 are derived fields, not separate payload tokens. Target signed16bit>=100 yields remainder100 anddeadflag1; other branchdeadflag0. Store widths reflect native truncation; payload values/type ranges are not server authorization proof. Stringdestinations/guards are observed, not declarations of C array capacity. In particulardamagecopy at361 andlater typebyte377 must remain distinct ordered writes; do not infer modern safe boundaries from offsets alone.

## UI join and source differences

Existing PET pickup at0x523bf comparesWORD `[slot_component + pet_component + 0x430dfd0]`; this equals the receiverorigin+useFlagoffset220. Its pet component uses the same2840stride arithmetic. This connects the received displaystate to the already locatedPET UI read, while complete runtime values/reachability remain unobserved.

Fresh comparison BismarckDD/Stoneage999ffdf1d220ec6666eb65339180689c9caf1876: netproc.cpp0dc677d3cd367ab89ca8d5becbb383bcbbccb3a8 (S callbackline768,Bcase1614..1696),pc.h3425a4d7c9a275dc78643448a08d74b33e54cf1b,protocol17f1900d8845c15308a4b429905ec009e5fd4c0f/protocol.hbb70087ef1b1915748da23935584eda2c8178cb0. DescendantBcase is_PET_ITEM and has a14field_ITEM_JIGSAW path; semantic field names match. Its expandedUTF8buffers/jigsaw50 differ from this388byte native record. **Do not apply descendant sizeofITEM or claim exact source-to-build identity.**

## Validation and remaining work

`python -m tools.stoneage_wayi_pet_state_probe LOCAL_DECOMPRESSED_CLIENT`, Capstone5.0.7. Strict hash/length, executable-raw switchtarget checks, seven aligned windows, limited affine address interpretation.14 new controls coverrawRVA/virtualtail/truncation,switchbounds/duplicatecategorytargets/byteoverflow,affineLEAscales/shift/sub/stack-symbol contracts,unknown/partial/nonlinear rejection,exclusive7slotloop,badloop andwronghash. Plus82 existing transport/sender/updater/PE/archive regressions:96 checks. CI uses synthetic instruction/layout samples only; no original binary assets.

These are client displayrecords, not authoritativephysicalglobalitem IDs/owners/unique codes. Pressure2486=2465 bounded closed+18 OPEN+3 historical UB unchanged. Matchingserver, exact2005publisherhash, native PET owner/save/drop/unique lifecycle andearly-era membership OPEN. NEXT: compare server-side S/B state serializer and movePetItem follow-up calls with this exact14field client layout, retaining source-only versus originalpaired-runtime boundaries. Officialfullpackage/manifest remains opportunistic; no engine transition.
