# TW1.0 R59 — independently bounded structural call/bypass witnesses

Status: derived-only original static graph evidence; actual native output and persistence OPEN.

This check uses the accepted R58 exact 124989-byte derived JSON (SHA256
04fb0b586f1fcf87f647b1bc1276bde2505822e195646c4c9058c03c7f558fe8).
It does not retrieve original binaries or evaluate save payloads.

FACT (bounded original instruction/graph evidence under structural CALL
continuation): 0x4a657 has both a path from its root to RET 0x4a6b2
through CALL 0x4a683 (which syntactically targets 0x4c5b4) and a path
to that same RET without visiting 0x4a683. The original static graph
of 0x4a53e similarly has paths to RET 0x4a5f0 that avoid both
memory-indirect calls 0x4a5a3 and 0x4a5ad, and separate paths that
visit either call. A deterministic graph traversal independently
replays these alternatives with synthetic edge, target, return, and
promotion mutation tests.

OPEN: whether any of these structural paths are dynamically feasible,
whether nested calls return, actual condition flags/registers/aliases,
callee side effects and preservation, real WriteFile invocation/output,
buffer flushing, close result/error conventions, persisted bytes, savedata
field schema/migration/checksum, and server authority. A bounded CFG
witness is NOT a runtime trace or proof of a historical resource leak.

These witnesses complement (rather than replace) the parallel R59
R28/R57/R58 native-root identity preflight. Follow-up should qualify
precise callee/path predicates and return effects using pinned metadata
where sufficient, requesting more original instructions only for a
demonstrated missing inventory. Stage A remains PARTIAL/OPEN. Do not
begin redesign of the new game on this result.
