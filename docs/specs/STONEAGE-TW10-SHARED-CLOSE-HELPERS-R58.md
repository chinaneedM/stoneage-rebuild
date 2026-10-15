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
