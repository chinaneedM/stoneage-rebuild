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
