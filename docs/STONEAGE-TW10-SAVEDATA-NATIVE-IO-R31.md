# TW1.0 R31 — CreateFileA opaque-value capture and helper stores

Exact Taiwan Waei/JSS1.0 original runtime/savedata, static only. Revalidate
R30 exact original JSON SHA256760730dc57c823a7279b22a0944ffaac588e77d4fb6b0d5f5024265345f0b45a
and strict gate, including original CALL0x4ed26->0x4c953 candidate.
Recheck parent CALL0x4b873->0x4eb55 and CreateFileA imported identity0x4ed01.
The parent candidate graph must reach API, conditional continuation0x4ed07,
and helper CALL; entry/frame/path/returning-CALL assumptions remain explicit.

Recover at most8 full-width register-copy candidates and24 local PUSH rows
before helper CALL. Physical offsets reference conditional ESP before CALL,
not a parameter signature. A unique UNKNOWN_CALL token at CreateFileA may
qualify as an opaque input candidate to a copy, never a known returned handle,
successful CreateFileA result or actual runtime effect. All value provenance
queries remain bounded64 rows/24 candidates/two dependency levels.

Explore helper0x4c953 in768 bytes/256 nodes. Collect at most12 recognized
explicit unsegmented integer memory-store candidates and16 ESP/EBP-relative
operand candidates. Implicit/segmented/other writes and aliases are not complete.
Record write values/address register sources, retaining returning-call, partial
register, memory-value, alias/owner and frame uncertainty. Caller PUSH-to-callee
parameter binding is not admitted in R31. No executed file/CRT/heap ownership,
native schema, persistence or filename/handle/buffer/length128 claim follows.

Only bounded metadata leaves CI; originals are nonexecuting and purged.
READY pending original source and independent exact JSON custody.

## 2026-10-13 independent acceptance supersedes READY

Original source38406412226, artifact11816674613, independent38406921461 exact JSON custody and59 synthetic/adjacent R30 tests38406413334 PASS.

- Original direct CALL syntax0x4b873->0x4eb55 and0x4ed26->0x4c953 independently rechecked; CreateFileA0x4ed01 import/IAT0x520a0 exact association. Parent candidate graph230/271 reaches API,0x4ed07 and helper CALL; no frontier/node cap, but actual entry/path/frame/callee-return effects remain unknown.
- Single full-width MOV ESI,EAX0x4ed07 has unique opaque source UNKNOWN_CALL0x4ed01 at its EAX input. This establishes a graph-local API-token copy candidate only, never a successful actual CreateFileA returned handle/value. The caller source surface has7 queries/no truncation.
- Before helper CALL0x4ed26 the conditional local suffix contains only PUSH EAX0x4ed25 at pre-CALL ESP offset0, stopping at intervening CALL0x4ed1f. EAX before PUSH/CALL is UNKNOWN_CALL0x4ed1f; all sampled pre-call registers conservatively carry that opaque barrier. R30's numeric continuation/helper discovery must not be promoted into direct CreateFileA-handle-to-helper argument linkage.
- Helper0x4c953 graph26/29 contains five recognized explicit unsegmented four-byte MOV store candidates, no sample truncation. ECX from entry-relative [ESP+4]0x4c953 feeds MOV0x4c959 to virtual writable .data0x172120c. Single ESP-relative operand is syntax, not an admitted caller PUSH/parameter binding.
- Other four helper stores target separate virtual writable .data0x1721208: MOV0x4c97d literal13, MOV0x4c98f EAX, MOV0x4c9a3 literal8 and MOV0x4c9af literal22. EAX store source is memory-load0x4c988 from raw-backed writable .data displacement0x6484c with EDX index scale8; EDX has zero-definition0x4c957 and INC0x4c96b loop candidates. No original loop index/table values, meaning or evaluated mapping admitted.
- Helper compact sources4 queries/no truncation/caps. Implicit/segmented/other memory writers and aliases are not complete. Actual memory mutations/global ownership/CRT identity/native save schema remain OPEN; helper's mapping-like syntax is a discovery hypothesis pending intervening CALL identity and branch evidence.

NEXT R32: identify original intervening CALL0x4ed1f and the predicate/branch reaching0x4ed26 to qualify the helper's mapping-like role. If justified, audit conditional physical PUSH EAX offset0 -> helper entry [ESP+4] hardware geometry separately from any API return/owner claim. Resume captured ESI0x4ed07 along other candidate parent paths and inspect parent memory-store/call inputs; do not mistake0x4c953's globals for the shared0x1721760 address candidates. Actual filename->CreateFileA result->ReadFile/WriteFile buffer/length128/schema/persistence, alias/frame/return effects and CRT/heap ownership remain OPEN. All actual runtime/ABI/owner/native-save gaps retained.
