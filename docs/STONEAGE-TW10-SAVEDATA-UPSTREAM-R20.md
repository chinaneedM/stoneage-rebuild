# TW1.0 R20 indirect CALL, third-global and alias frontiers

**Status:** ORIGINAL-DERIVED CONDITIONAL STATIC INDEPENDENTLY ACCEPTED; runtime save and object ownership OPEN.

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

## 2026-10-12 original R20 static finding and custody acceptance

Pinned original-only probe source `fc95c33f3877d7182359334885ce8ed47f8bcb12`,
Action `38262025327` job `114854677906`, SUCCESS after original
archive catalog outage, three-attempt bounded retry without relaxing original
MD5/SHA1, runtime/savedata hash chain and cleanup. The original executable
was never run and no proprietary payload entered repository.
Derived-only artifact `11752812909`, ZIP SHA256
`729d80b700b83cf5e5e9cca8b01a36867fee02aa021a499fa5db0fa2c71babbe`.
Inner JSON exactly **5,071 bytes**, SHA256
`f669ca334d6d5bfa120496fde1990afa03f2394fd7366ea0a465b996a90a034a`.
Independent immutable original run HEAD/branch/artifact custody, strict
13-test no-promotion guard and canonical original-derived JSON check:
Action `38262869071` job `114857568530` SUCCESS.

**Accepted original static facts — no runtime effect admitted:**

- Exact `0x4a0c4` is indirect memory CALL through the imported
  `KERNEL32.dll!HeapReAlloc` slot RVA `0x520dc`. Candidate
  local graph anchored `0x4a0a0` contains 51 nodes/54 edges, no
  graph node-cap hit; all CALL continuations remain structural.
  The association proves neither HeapReAlloc execution nor return,
  parameters, actual object reallocation, or EAX value at subsequent
  candidate store `0x4a0d5`.
- Virtual writable .data `0x172187c` has **one direct write
  candidate `0x499dc` and eleven direct read candidates** in
  the full 331,776-byte linear .text scan (104,229 decoded instructions,
  eight decode-gap bytes, no reference sample cap). Indirect aliases
  and effective initialization remain unresolved.
- `0x49a06` is a syntactic four-byte memory PUSH from
  `0x172187c` inside a four-instruction conditional linear prefix
  before `KERNEL32.dll!HeapAlloc` at `0x49a0c`.
  Neither HeapAlloc ABI position, heap size, flags nor actual
  allocation result is established.
- `0x4a17d` is a four-byte `MOV [EAX+8], EAX` syntax candidate
  in the `0x4a14d` EBX callee. A bounded 51-node/52-edge graph
  reaches it conditionally with outside-window frontiers;
  the original R8 alias-write gap and control-flow cycle remain.
  No original effective EAX address/object owner or caller
  continuation may be promoted.

**Highest NEXT R21:** bound the single direct writer of `0x172187c`
at `0x499dc`, the candidate HeapReAlloc argument stack/return effects
around `0x4a0c4`, and aliases into `[EAX+8]` around `0x4a17d`.
Keep source/stack/calling convention/path gaps explicit before
considering object ownership; native save filename/file handle/buffer/128,
framing/checksum/migration and runtime IO remain OPEN. Restoration first.
