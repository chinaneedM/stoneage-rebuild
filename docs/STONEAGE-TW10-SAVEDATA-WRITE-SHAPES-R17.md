# TW1.0 R17 static global-write, memory-gap and nested-call frontier

**Status: INDEPENDENTLY ACCEPTED ORIGINAL-DERIVED CONDITIONAL STATIC ONLY; RUNTIME AND OWNERSHIP OPEN.**

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

## Original R17 acceptance — 2026-10-12

Original source commit `5a28f10d4c91adc4a9da45492204396a7223654f`,
Action `38255685702`, job `114833029425`, SUCCESS: synthetic R17/R16
regressions, original pinned download/extraction/hash-chain verification,
nonexecuting analysis, original purging and derived-only artifact upload.
Artifact `11750721082` ZIP digest
`a509ce3e9d29818acb8305d441687b5d0ead83dba8435cf44bfcbd90d130a72e`;
inside JSON **7,738 bytes**, SHA256
`b9d04302615e2a591262270cd7ee88705740a6c6080b20594a90786ae99d0c80`.
Independent source-run/head/artifact/digest/strict semantic guard and exact
committed JSON equality Action `38256121610`, job `114834537103`, SUCCESS.
No original proprietary bytes were published.

The three pinned .data `0x172186c` writes all decode as four-byte `mov`:

- `0x49a2c`: direct source **EAX**. An unverified local anchor
  `0x49a00` produced 16 nodes/15 edges and EAX origin
  **unknown after opaque CALL** at `0x49a0c` (not a value proof).
- `0x49d78`: direct source **ECX**. Unverified local anchor `0x49d40`
  produced 26 nodes/26 edges; the candidate ECX reaching definition at
  `0x49d72` is a four-byte memory load from distinct writable .data
  RVA `0x1721878`. This is a **candidate local source**, not a proven
  function entry, actual global contents or initialization.
- `0x49e88`: direct source **EBX**. The attempted local anchor
  `0x49e40` reaches only one node and **does not reach the write site**.
  No reaching-definition conclusion is admitted.

At `0x484c7`, the earlier conservative R8 `unsupported_memory` gap
decodes as **IMUL** with a four-byte `ESI` register operand and a
four-byte memory read at `[ESP+20]`; decoder marks ESI/EFLAGS written.
This establishes a syntactic multiplier operand, not a verified frame
owner, effective value, complete helper semantics or caller effect.

Nested `0x49900` target `0x4e2a8`: 10 modeled states, one balanced
RET state, unresolved direct CALL to `0x4e2e1`. Target `0x4e2e1`:
40 states, one balanced RET state, two unresolved CALL frontiers
(one indirect), and no admitted summary. Balanced modeled RET cannot
override unmodeled branches/calls.

**Next R18:** resolve the exact CALL barrier for EAX before `0x49a2c`,
identify source and alias/ownership of the distinct `0x1721878` global,
and recover a credible enclosing CFG/path to `0x49e88`, before any
named global initialization; separately model IMUL read source and
nested callee effects. Keep native save/filename/handle/buffer/128-byte
serialization/framing and runtime IO OPEN. Strict restoration-first stage
gate stays in force.
