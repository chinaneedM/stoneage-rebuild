# TW1.0 R17 static global-write, memory-gap and nested-call frontier

**Status: TOOLING CANDIDATE; ORIGINAL PROBE/INDEPENDENT CUSTODY NOT YET ACCEPTED.**

This analysis continues the independently accepted R16 exact original-derived
references. The three write **candidates** to virtual `.data` RVA
`0x172186c` are `0x49a2c`, `0x49d78` and `0x49e88`;
the read candidate is `0x49de3`. R16 does not prove effective initialized
content, executed paths, object identity or original save behavior.

R17 adds hash-gated, non-executing examination of:

- exact destination operand, width, integer instruction class and direct source
  operand kind at all three original write candidates;
- optional bounded register-definition frontiers beginning at deliberately
  **unverified synthetic instruction anchors**; these may fail to reach the
  write sites and never establish a complete function or all incoming paths;
- original callee `0x484c0` memory gap at `0x484c7`, preserving operand width,
  base/index/relative displacement and decoder access flags, not effective
  memory address or caller ownership;
- both previously unresolved nested targets of `0x49900`:
  `0x4e2a8` and `0x4e2e1`, bounded by the conservative R8 effect model.

All memory and register observations are static candidate geometry. Any
conditional modeled return is **not** a runtime effect/ABI or a legal basis
to resume the calling function. The original PE must never execute, and the
archive, BIN and extracted executable are purged after probe completion.

The attached workflow first runs synthetic tests, recovers the already pinned
original archive temporarily, repeats full R16 hash/identity verification,
then uploads **derived-only JSON**. This workflow by itself does not constitute
historical acceptance. Admission requires a separate job verifying immutable
source head, successful original-run identity, artifact integrity, strict
field/flag semantics and byte-for-byte or normalized JSON equality against
an independently recorded report.

**Open after this scope:** concrete initialization values, alias and
branch reachability, helper memory semantics and caller input/output ownership;
filename to CreateFileA, returned handle/stream to ReadFile/WriteFile buffers
and length 128, original save layout/framing/checksum/migration/runtime IO,
and cross-version equivalence. No later 8.0 behavior is promoted to TW1.0,
and no new-game engine or design phase is authorized.
