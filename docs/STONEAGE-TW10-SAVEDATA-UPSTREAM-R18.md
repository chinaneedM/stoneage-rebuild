# TW1.0 R18 original upstream CALL / distinct global / CFG frontiers

**Status:** original R18 conditional STATIC independently accepted after strict custody; original native effects, ownership and file persistence remain OPEN.

Pinned R17 recorded a four-byte source-EAX global write at `0x49a2c`, a
source-ECX global write at `0x49d78`, and a source-EBX global write
at `0x49e88`. These are static write candidates into `0x172186c`.
No original runtime value, function entry, call return, ownership, save
format or native operation is proven.

R18 source analysis examines the exact `0x49a0c` CALL that blocks the
EAX source, preserving the distinction between exact transfer target
and *qualified* callee return/effect. It scans full linear `.text`
candidate references to independent writable virtual global
`0x1721878` which is the candidate input at `0x49d72`, with
unknown aliases and execution. It reuses R14's bounded `0x49d93`
CFG to seek `0x49e88` EBX definitions; the bounded CFG anchor is not
a function entry and CALL fallthrough is structural. Finally it
symbolically follows the short original `0x484c0` to IMUL `0x484c7`
prefix in a model-only stack frame; no actual stack address or caller
argument ownership is inferred.

The original probe checks inherited exact archive, executable and
savedata identity, emits non-executing limited JSON evidence and
purges all originals. Independently pin original workflow source/head,
artifact digest, JSON shape/no-promotions and exact copied report
**before** promoting an R18 conditional static evidence receipt.

Original save filename→CreateFileA, handle→ReadFile/WriteFile buffer
and 128-byte length, serialization/framing/checksum/migrations, global
runtime initialization, server-side ownership and version equivalence
remain OPEN. No new-game construction or later-release promotion.

## R18 original-derived acceptance — 2026-10-12

Original pinned source commit `f02afc054b8263a471617db3f7a43f0bf299765e`;
Action `38257682689`, job `114839871876`, SUCCESS. Temporary full
historical archive, BIN and embedded pinned executable/savedata digests
rechecked by inherited R17/R16 gates; original executable not run,
all original bytes purged. Derived-only artifact `11750734113`, ZIP
SHA256 `42ac88466914bfb7cac3a9a312acf742791f69b2bb5ced99a4176db365233fae`.
Inside JSON 5,051 bytes SHA256
`2710fe1b2367c863b06706ee445db7f0decf96509da29b635c896d2bd810e6b8`.
Independent source-run/head/branch, artifact SHA, strict twelve-test
anti-promotion guard, and exact derived/committed JSON comparison:
Action `38258094341`, job `114841274904`, SUCCESS.

- CALL `0x49a0c` is an **indirect memory CALL through an exact
  `KERNEL32.dll!HeapAlloc` import slot at RVA `0x520f8`**.
  This is an exact import association, not proof of runtime call,
  argument flags/size, successful allocation, returned pointer
  or ownership of the `0x172186c` write at `0x49a2c`.
  Candidate local CFG: 16 nodes/15 edges, all CALL effects opaque.
- Separate writable virtual `.data` RVA `0x1721878` is a candidate
  source of ECX loaded at `0x49d72`. Linear .text scope of
  331,776 bytes, 104,229 instructions and eight decode-gap bytes:
  **two write candidates** at `0x49a14`, `0x4a0d5`;
  **six read candidates** at `0x49a45`, `0x49d37`,
  `0x49d72`, `0x49d9e`, `0x4a0b7`, `0x4a0df`.
  No sample truncation. These do not cover indirect aliases
  or prove actual initialization/value or a unique owner.
- Original R14 bounded graph anchored `0x49d93` **does** contain the
  `0x49e88` EBX write: 139 nodes/158 edges/3 outside-window edges,
  without node cap. Five conservative reaching-source tokens include
  register copies/adjustments and **an unknown CALL at `0x49e6e`**.
  These are branch-conservative tokens, not effective values,
  verified complete incoming control flow or a function entry.
- Short linear original `0x484c0 → 0x484c7` prefix has four
  modeled preceding instruction sites. At IMUL `0x484c7`, the
  memory operand `[ESP+20]` resolves to **symbolic entry ESP+8**
  under that one-path stack model. Actual caller argument ownership,
  branch feasibility, multiplication value and summary remain OPEN.

**Highest NEXT R19:** decode exact operand/value/branch geometry for
the two `0x1721878` write candidates and HeapAlloc call site
argument pushes/result-to-global path, qualifying no values until
CALL effects and stack ownership are justified. Separately isolate
`0x49e6e` unknown callee effects and paths towards `0x49e88`,
and verify the IMUL caller-frame relation without treating a
synthetic stack offset as ABI proof. Original native save filename,
handle, buffer, 128-byte length, framing/checksum/migration,
runtime IO and ownership remain OPEN. No engine work.
