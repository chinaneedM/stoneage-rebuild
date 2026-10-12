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
