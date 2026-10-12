# TW1.0 R20 indirect CALL, third-global and alias frontiers

**Status:** original evidence probe pending; synthetic static controls alone do not establish historical facts.

R19 found two EAX-sourced candidate stores to writable virtual .data RVA
`0x1721878`, one preceded by unknown CALL `0x4a0c4`. R19 also found
a syntactic pre-HeapAlloc PUSH `0x49a06` reading four bytes from separate
virtual .data RVA `0x172187c`, and an EBX callee
`0x4a14d` with opaque alias-write gap `0x4a17d`.

This probe pins the original CALL operand/import identity at `0x4a0c4`,
scans linear .text reference candidates for `0x172187c`,
characterizes a strictly *linear* and incomplete HeapAlloc prefix,
and records operand/memory shapes at `0x4a17d`. It keeps graph
boundaries, uncertain branch feasibility, callee effects and aliases
visible rather than converting candidate syntax into effective values.

The original PE is never executed. Archived original media is fetched
transiently with existing hash checks, and all original payload is purged.
Only bounded metadata, tests, and evidence receipts enter this repository.

Do not conclude actual allocation, native save, argument ABI/size,
pointer ownership, executed branches, or historical cross-version identity
from the probe. A separate immutable-run/artifact, strict anti-promotion
guard and exact JSON equality must complete before declaring original
R20 evidence accepted.
