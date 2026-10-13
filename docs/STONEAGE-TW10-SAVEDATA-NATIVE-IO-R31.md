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
