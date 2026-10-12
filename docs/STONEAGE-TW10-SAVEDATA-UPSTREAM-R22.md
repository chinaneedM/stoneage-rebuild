# TW1.0 R22: opaque writer CALL / realloc PUSH / EAX cycle

**Status: ORIGINAL-DERIVED PENDING independent custody and acceptance.**

R21 accepted a four-byte writer to .data 0x172187c at RVA 0x499dc
with EAX blocked by a CALL candidate at 0x499d4. R21 also identified
four syntactic PUSH operands upstream of imported HeapReAlloc at 0x4a0c4
and two EAX source candidates in a cyclic graph at 0x4a17d.

R22 adds a bounded direct/indirect CALL-operand identity probe for 0x499d4.
Its call-to-writer graph path is explicitly conditional on structural
return-to-fallthrough. Even if a direct target is statically resolved, no
executed callee, actual return, modified EAX or global value follows.

The HeapReAlloc subprobe constructs bounded predecessor/successor graph
candidate paths for each pre-call PUSH. This is **not** a symbolic
stack trace; prior branches, stack delta, argument position, ABI validity
and actual heap result remain unverified. Register operands gain explicit
local reaching-source candidates that may themselves terminate at other
CALL barriers.

For the EAX alias write, backward graph edges are recorded separately
from actual execution, and local reaching-definition candidates whose
instruction RVAs exceed the target are preserved with a cycle caution.
This must not close R8's alias-write gap or claim original object
ownership, caller return effects or function identity.

Original analysis runs exclusively as static decoding against the
original-v1.0 hash-verified ephemeral archive; full file and runtime/savedata
identity gates from R21 remain in force. No original program is executed,
and no proprietary bytes/disassembly/assets are exported. Derivation,
synthetic CI, independently pinned run/artifact digest, strict guard,
exact JSON comparison and continuity update are separate gates.

Original filename→CreateFileA, handle/stream→ReadFile/WriteFile
buffer/length128, actual native save framing/checksum/migrations/runtime
IO and cross-version equivalence remain OPEN. R22 is part of historical
restoration Stage A and must not trigger new-game engine production.


## 2026-10-12 — R22 original bounded static evidence independently accepted

Pinned original source run 38267287871/job114872523381 at exact source HEAD
82c186fcf2cd74c876b016fb1aa74872793ced0f SUCCESS; pinned historical
archive and runtime/savedata hashes preserved, temporary original bytes purged
after nonexecuting static inspection. Derived-only artifact 11756110734,
ZIP digest sha256:31d06d772e7525128d7288f38ed48664c0ba05d3a0c0296e1ea0f1f45c680b70.
JSON exactly 7,221 bytes, SHA256
a0e05f372b52fc49c7bfda0d08603fb82e5e8f8e6821dc852921f86f04da14e5.
Independent pinned-run/head/branch/artifact custody, wrong-import semantic guard,
18 R22 tamper controls, and canonical original-derived JSON equality:
Action 38268755166/job114877486168 SUCCESS. R22+adjacent R21 50 tests:
Action 38268754905/job114877485681 SUCCESS.

**Accepted conditional ORIGINAL STATIC findings, not runtime facts:**

- Exact CALL at RVA 0x499d4 resolves syntactically through the imported
  KERNEL32.dll!HeapCreate slot at IAT RVA 0x520e8 (memory-indirect).
  The R22 heuristic anchor 0x499d0 has 16 graph nodes/16 edges with a
  structural CALL-to-writer continuation at 0x499dc. This does not prove
  heap creation, HeapCreate arguments/return, EAX value, effective
  writable-global contents or a path actually executed.
- The HeapReAlloc 0x4a0c4 anchor graph contains 51 nodes/54 edges.
  Four pre-CALL PUSH candidates each have syntactic paths to the call:
  EAX at 0x4a0b6, memory global .data 0x1721878 at 0x4a0b7,
  EDI at 0x4a0bd and memory global .data 0x172187c at 0x4a0be.
  Candidate EDI local input originates at a constant-assignment site
  0x4a0a9, but actual EDI value/branch state is not verified.
  None of these PUSHes is an independently established ABI slot.
- In the 0x4a14d candidate alias graph (62 nodes/65 edges), recorded
  backward edges are 0x4a166→0x4a15f, 0x4a187→0x4a17d,
  0x4a1f4→0x4a1bd. The later-RVA EAX source candidate at 0x4a183
  cannot be interpreted as earlier linear execution without a feasible
  cycle. The four-byte MOV [EAX+8], EAX and R8 alias-write gap stay
  unsummarized; no ownership, caller return or runtime path admitted.

**Highest NEXT R23:** boundedly correlate the HeapCreate return/handle
candidate and original globals with HeapAlloc and HeapReAlloc, recovering
local input definitions and stack effects only where original static
evidence supports them; preserve all CALL barriers and cycle ambiguity.
Native filename→CreateFileA, handle/buffer/length128→ReadFile/WriteFile,
serialization/framing/checksum/migration, actual native IO and
cross-version correspondence remain OPEN. No Stage B/new-engine work.
