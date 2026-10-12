# TW1.0 original savedata R15 upstream/frame/CALL geometry

**Status: ORIGINAL-DERIVED STATIC ONLY — no executable path, function ABI,
global initialization, ownership or native save admitted.**

The accepted original report derives from pinned original workflow
`38249248524`, source commit `cf8e4b7afc5d7eecece7562f1da495b0b316a2c6`,
derived-only artifact `11747531788` (ZIP SHA256
`faff383d7b8e321e69c122e3ce88163b36971cb18d1fe3e9a867a6991c9d435b`,
JSON length 5,821 bytes, SHA256
`cb246c688e6ef3b348456229f4bb458d7cd316b543d459a72a9981a2cb856bc2`).
The original archive and executable were extracted temporarily only;
no original bytes were executed, retained or published.

## Bounded original results

- EAX before the EBX copy at `0x49de8` reaches a four-byte memory-load
  definition at `0x49de3` from writable virtual .data RVA `0x172186c`.
  **The value remains UNKNOWN**: this global is distinct from both earlier
  0x1721884 and 0x17228a0 candidates.
- EBP before writes `0x49dca` and `0x49dec` reaches register copy
  **EBP ← ESP at 0x49d94**. ESP before `0x49dec` has one syntactic
  reaching-definition site `0x49da9`, but its numerical stack offset and
  caller/local object ownership remain UNKNOWN. Entry anchor 0x49d93 itself
  is not independently proven a complete function entry.
- Five original direct CALL instruction/target pairs are confirmed:
  `0x49444→0x484c0`, `0x4945d→0x484c0`,
  `0x4946f→0x49900`, `0x49e5f→0x4a09c`,
  `0x49e6e→0x4a14d`.
  They are **direct original transfer syntax only**. Identical CALL targets
  at 0x49444/0x4945d do not prove the callee returns identical values or
  effects for their possibly different argument contexts.
- Helper bounded R14 graph retains 139 nodes and 3 external edges; globals
  graph retains 48 nodes and no within-window exterior gaps. No data here
  establishes function entry coverage or feasible runtime branches.

Next R16: examine 0x172186c initialization and recursive EAX provenance,
and bounded effects/ABI for the common 0x484c0 callee; separately inspect
0x49900, 0x4a09c and 0x4a14d before any caller/global effect admission.
Continue to require the distinct filename/CreateFileA and handle/ReadFile/
WriteFile argument evidence and original native framing/checksum when available.
All historical native save claims remain OPEN. The priority remains original
restoration, not later 8.0 or modern engine construction.
