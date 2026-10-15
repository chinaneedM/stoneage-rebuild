# TW1.0 R58 — rooted shared-write/close and close-path helpers

Status: IN PROGRESS; R57 accepted; real helper effects and native persistence OPEN.

This bounded source experiment requalifies the **exact original R57 report**
(SHA256 `3e562ab02a80e0f6516f8a91c93b897eef05f606be62f1df5cb48686d64114e6`)
before adding only two missing root contexts:

- Shared helper `0x4a657`, direct wrapper CALLs `0x48c38` and `0x48586`.
- Close-path helper `0x4a53e`, direct wrapper CALL `0x48596`.

Source authenticity, bounded CFG/operand shapes, predicates, opaque calls and
register-return sources are separately checked; a 768-byte / 256-node graph
bound must be **recorded**, not silently treated as full closure if exceeded.
The original client is never executed; media are transient and purged.
Neither an original file payload nor source binary belongs in committed output.

The R57 buffering-shaped success return and outer caller's ignored close result
are the concrete questions. Syntax/conditional register analysis cannot certify
native output, flush, close, persisted bytes, ABI, frame alias invariants,
record version, schema, checksum, server state or cross-version equivalence.

Acceptance requires (1) source Action success and derived metadata,
(2) independent immutable source/artifact verification and strict graph/return
replay, (3) canonical receipts and continuity, (4) passing main Actions.
Until then Stage A remains PARTIAL/OPEN and R58 is not accepted.


## R58 authenticated original and independent findings

Source Action38743841197 (68 tests) and independent Action38744746218 (83 tests) are SUCCESS. Source artifact11976911506 is pinned to ZIP SHA256 37ff56646a708744f9585eb7719fa313a6a053bcea9a9f6c38ac4bf2044601d2, canonical static report124989 bytes SHA256 04fb0b586f1fcf87f647b1bc1276bde2505822e195646c4c9058c03c7f558fe8. Independent reverse-predecessor algorithm agrees on12 R58 register-source queries. Recovered original assets were never published.

FACT: shared 0x4a657:40 nodes/44 edges,5 predicates,4 explicit memory-write shapes, bounded RET0x4a6b2, direct CALL0x4a683->0x4c5b4; CMP EAX,EDI at0x4a68b and MOV EAX,EBX at0x4a6ae. Close-path 0x4a53e:66 nodes/73 edges,8 predicates,3 memory-write shapes,8 call shapes of which2 are memory-indirect, RET0x4a5f0. Both complete in the bounded original static CFG, without limits/frontiers. They do not establish actual native transfer, success/error values, close/flush/persistence or frame alias preservation.

Highest NEXT R59: resolve only native-context/close-result chains needed for original savedata semantics; preserve opaque native/indirect calls and all Stage A PARTIAL/OPEN gates.
