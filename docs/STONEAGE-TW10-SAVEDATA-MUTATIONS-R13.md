# TW1.0 savedata R13 exact original static mutation candidates

**Status: CONDITIONAL STATIC GEOMETRY only.** This record does not attest
executed paths or native persistence. It supersedes no R12 evidence.

Original source run: 38244549768 at commit
`2cd6da6b5b10c33eb4812d401ad4726670f8a8f0`, successfully completed.
Derived-only artifact: 11744188437; ZIP digest
`cb66dd1cc065f772029042b7e7445579718598ac232cfefca464169e74b137f1`;
inner JSON digest
`f67990caa6da3728acee93e8dca3dbcd9c3b98bb7ab5aec4cef19b6be62287c2`.
R12 original pinned executable/save hashes and the original R12 witness are checked
before this analysis. The original media is not executed, committed, or retained.

The exact six selected four-byte destination candidates are:

| Original instruction RVA | Candidate static operation | Value operand | Target |
| --- | --- | --- | --- |
| 0x49dca | OR (read-modify-write) | immediate 0xFFFFFFFF | EBP-8 |
| 0x49dec | MOV | EBX | EBP+8 |
| 0x4943c | MOV | EAX | absolute .data RVA 0x17228a0 |
| 0x4944a | MOV | EAX | absolute .data RVA 0x1721884 |
| 0x49457 | MOV | ESI | absolute .data RVA 0x17228a0 |
| 0x49463 | MOV | EAX | absolute .data RVA 0x1721884 |

These are instruction operand shapes from the pinned original executable.
The two global destinations fall in writable virtual .data without raw backing.
That alone says nothing about initialization or actual write timing.
The helper's EBP-based offsets are *frame-relative syntactic locations*, not
proof of what caller object, argument, stack slot or save field they mutate.

The 0x49dca–0x49dec linear decode has 13 instruction boundaries and a jump
at 0x49dd1. The 0x4943c–0x49463 linear decode has 15 boundaries and a jump
at 0x49452. Both are bounded **linear windows**, not verified CFG paths,
function boundaries, feasible branches, or execution order.

**Remaining highest NEXT:** recover reaching definitions and intervening CALL
barriers for EBX at 0x49dec and EAX/ESI at all four global writes; isolate
function entry, incoming paths, EBP/ESP frame setup, alias effects, global
initialization and the two linear-window branch predicates. Admit a specialized
mutation summary only if all named effects and path conditions are independently
verified. HeapAlloc size/result/ownership, CreateFileA / ReadFile / WriteFile
handle/buffer linkage, 128-byte schema, checksum, native serialization and
cross-profile semantics remain separate OPEN.
