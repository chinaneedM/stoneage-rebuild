# TW1.0 R59 — Shared helper paths do not imply native save

Status: bounded original-derived static syntax; *not* a runtime, I/O or persistence acceptance.

Source: exact original-derived R58 static metadata (124989 bytes, SHA256
`04fb0b586f1fcf87f647b1bc1276bde2505822e195646c4c9058c03c7f558fe8`);
its original runtime evidence had already been authenticated under R58.
No new original-media retrieval is required for this focused R59 graph audit.

The shared helper at 0x4a657 has a complete 40-node/44-edge bounded graph.
An independently generated path witness proves a **structural candidate route**
from entry to RET0x4a6b2 that *does not contain* the nested CALL0x4a683
(to R28's 0x4c5b4 native-context candidate). A second structural route contains
CALL0x4a683 and returns without visiting OR[ESI+12],0x20 at0x4a69d.
A third visits both the nested CALL and that OR write, then sets EBX all-ones
at0x4a6a1 and uses MOV EAX,EBX at0x4a6ae.

The candidate native-call route is guarded by original static branches:
JNE0x4a66b, JE0x4a671, JLE0x4a67c. If a nested CALL structurally
returns, CMP EAX,EDI at0x4a68b and JNE0x4a68d distinguish a conditional
path to the error-flag shape. The initial XOR EBX,EBX at0x4a65d
and all-ones OR at0x4a6a1 explain distinct *syntactic* return bit patterns,
not a proven original success/error convention.

The R28 preflight separately identifies WriteFile-associated import sites
0x4c68c and0x4c6f1 in the 139-node/156-edge root; the graph route above
is **not** a cross-function execution trace. Memory aliasing, EDI preservation,
native return/error semantics, actual WriteFile dispatch and persisted savedata
remain OPEN. Neither a full-count wrapper return nor a shared-helper zero-shaped
return proves disk storage. No original application, OS API or save payload is
executed. This evidence remains Phase 1 / Stage A, not new game development.

Automated controls reject altered shared-call target, changed post-call compare,
changed flag mask, missing early bypass branch, changed result register, and
nonempty graph frontier. The accepted R59 preflight and this route audit should
be combined as independent gates, not collapsed into a native-success claim.
