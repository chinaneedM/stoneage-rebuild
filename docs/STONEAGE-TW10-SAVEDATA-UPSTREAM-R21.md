# TW1.0 R21 third-global writer, HeapReAlloc and EAX alias audit

**Status: R21 ORIGINAL DERIVATION NOT YET ACCEPTED.** Native save remains OPEN.

The independently accepted R20 original static sample identifies exactly one
direct linear .text write candidate to the virtual writable .data global
0x172187c at 0x499dc, a KERNEL32.dll!HeapReAlloc imported CALL at 0x4a0c4,
and a four-byte MOV [EAX+8], EAX alias gap at 0x4a17d.

R21 inspects three bounded static frontiers separately:

1. At 0x499dc: store geometry, source operand class and graph-local source
   candidates, with no executed path, register value or initialization claim.
2. Before 0x4a0c4: bounded PUSH operand shapes and selected pre-CALL register
   candidates. No positional ABI mapping, heap flags/size, successful
   reallocation, return EAX or object ownership is inferred.
3. At 0x4a17d: same-register destination-address/value syntax with separate
   candidate local EAX source; no effective object or caller return effect.

All graph anchors are heuristics rather than verified function starts.
Original bytes are decoded statically only after the inherited hash gates.
The original disc/archive/executable are transient and purged; no proprietary
bytes or disassembly are published. Synthetic test success is not evidence
acceptance. An independently pinned successful original run, immutable
artifact/digest, strict negative controls and exact JSON comparison are
required before the CURRENT-STATE history may describe R21 as accepted.

Actual native file IO, filename -> CreateFileA, handle -> ReadFile/WriteFile
buffer/length128, save framing/checksum/migrations, persistence, path
feasibility, original server data and cross-version equivalence remain OPEN.

This work is Stage A historical reconstruction, not new-game production.


## 2026-10-12 independently accepted original R21 static results

Status advanced to **ORIGINAL-DERIVED CONDITIONAL STATIC INDEPENDENTLY
ACCEPTED** after immutable original source Action 38265173589 / job
114865410591, source HEAD 0601a246c123eb6c390a141c7b377f3af71aaa03,
derived artifact 11753958380 (ZIP digest
sha256:eb6c03f9f832c4b35967212162c9613b8fd5806e34a7a2b365a4fb909c3190ea).
Derived JSON 8,095 bytes / SHA256
397569c44575dc752e5b857c1ea358528dbbbdc4089c065be91b54ca9bab1a2e.
47 synthetic/adjacent controls PASS on 38265620986. Independent original
run/branch/artifact pin, strict negative guards and exact canonical JSON
equality Action 38265936276 / job 114867976555 PASS.

The 0x499dc original writer is a four-byte MOV from EAX to the absolute
writable virtual .data 0x172187c. Among heuristic candidate anchors,
0x499d0 reaches the store via a 16-node/16-edge graph; the local EAX input
frontier contains an unknown CALL 0x499d4. No function entry, call effect,
runtime value or actual store execution is established.

Before the imported HeapReAlloc 0x4a0c4, the 0x4a0a0 candidate graph
(51 nodes/54 edges) contains four PUSH candidates: EAX at 0x4a0b6,
four-byte .data 0x1721878 at 0x4a0b7, EDI at 0x4a0bd,
and four-byte .data 0x172187c at 0x4a0be. They are *not* verified
HeapReAlloc parameter slots. Pre-CALL EAX has an unmodeled write
candidate 0x4a0b3; ECX/EDX are unresolved at the artificial graph anchor.
No post-CALL EAX return value, heap allocation success, ownership or
effective 0x4a0d5 global write can be deduced.

At 0x4a17d, MOV [EAX+8], EAX has 62-node/65-edge bounded
candidate graph from 0x4a14d; local EAX source candidates include
0x4a173 (address calculation) and 0x4a183 (offset adjustment via a
cycle). A syntactically later RVA can be a reaching candidate through
a cycle; neither linear execution nor effective alias ownership follows.
The R8 unsummarized alias-write gap persists. No caller return effect.

**NEXT R22:** investigate the identity/effects of opaque CALL 0x499d4,
the value source for the third-global write, pre-ReAlloc register/stack
candidate feasibility, and the cyclic EAX aliases/unknown callee returns;
retain filename/handle/buffer/length128 and all native-save semantics OPEN.
The Stage A restoration gate remains binding.
