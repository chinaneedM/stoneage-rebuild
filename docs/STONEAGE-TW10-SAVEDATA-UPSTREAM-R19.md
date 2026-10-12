# TW1.0 R19 second-global write and HeapAlloc-boundary static probe

**Status:** INDEPENDENTLY ACCEPTED ORIGINAL-DERIVED CONDITIONAL STATIC; object, runtime and native SAVE remain OPEN.

Follow accepted R18: `0x49a0c` exactly associates with IAT
`KERNEL32.dll!HeapAlloc`, not a proven allocation. Distinct writable
virtual `.data` at `0x1721878` has two direct static write
candidates (`0x49a14`, `0x4a0d5`) and six read candidates
in a linear `.text` scan, not verified executable paths.

R19 tests actual instruction shapes and source operands at both write
candidates, retains bounded candidate source-graph anchors and CALL
barriers. It identifies syntactic PUSH operations ahead of
`HeapAlloc` in a bounded reachable candidate graph without assigning
them to ABI slots or verifying arguments. It separately checks exact
`0x49e6e` direct CALL target and R8 bounded return gaps and exact
`0x49444`/`0x4945d` calls to the IMUL-root helper.

No native original program executes. All historical bytes stay
transient, are hash-gated against R18 and purged after derivation.
Only derived JSON may be published, with independent immutable-source
run identity, artifact digest and strict schema/no-promotions guard
before accepting any new original results.

Historical call execution, actual heap size/flags/handle, memory
allocation success, pointer/global object ownership, caller ABI,
branch feasibility, filenames/handles/buffer/128-byte native save
format and later-version projection remain OPEN. Restoration first.

## Original R19 result and independent acceptance — 2026-10-12

Original analysis source `114d0800c0fda16618f2c292f10713c6bf24e4e2`,
Action `38259495149`, job `114846067239`, SUCCESS; inherited exact
original archive/BIN/sa_3.exe/savedata.dat identity checks re-run before
non-executing probe; originals purged. Derived-only artifact `11752187262`
ZIP SHA256 `ba53ffe7bb14225e7dd3210864ef4d6bbddb2174c039e703b9ade7f86a6bf205`.
Inside JSON exactly **7,321 bytes**, SHA256
`fc442e38aeafcd926810fd6d1ffbc0d50ff305564b248c068eccc45ea132169d`.
Independent immutable source/run/branch, derived-artifact digest, twelve
strict negative tamper controls and bounded schema verification Action
`38260313600` / job `114848826375` SUCCESS. Exact canonical JSON
comparison to committed derived witness is required on integration.

**Conditional STATIC observations:**

- Both writes into independent writable .data RVA `0x1721878` are
  **four-byte MOV of EAX**, at `0x49a14` and `0x4a0d5`.
  Conservative local reaching origins respectively stop at unresolved
  CALL barriers `0x49a0c` (known `KERNEL32.dll!HeapAlloc` IAT association)
  and `0x4a0c4` (not yet target/effect qualified).
  Candidate graph sizes 16 and 51; both reach their named write site
  only within unverified local anchors, not proven function entries.
- A single syntactic PUSH before HeapAlloc, RVA `0x49a06`,
  reads a four-byte memory value from writable .data RVA
  `0x172187c` (distinct from `0x1721878`). This is a **PUSH
  candidate**, not confirmed HeapAlloc argument position, heap size,
  process heap handle, flags, runtime allocation, pointer or object owner.
  Other arguments may be supplied outside the local anchor/caller frame.
- CALL `0x49e6e` is exactly direct to `0x4a14d`. Its R8
  conservative model visits 22 states, has a possible control-flow cycle,
  no qualified returns and unresolved alias write `0x4a17d`.
  Caller EBX resumption is **not accepted**.
- Two exact original caller sites `0x49444` and `0x4945d`
  directly transfer to helper `0x484c0`. Their relation to
  the conditional IMUL entry ESP+8 stack position does **not** prove
  caller argument ownership, return effects or executed paths.

**Highest NEXT R20:** inspect `0x4a0c4` indirect-call target and
the `0x172187c` PUSH source reaching definitions/aliases; independently
bound pre-HeapAlloc register/stack path conditions and `0x4a17d`
alias/cycle effects, with strict no-ABI/no-native promotion.
Filename→CreateFileA, returned handle→ReadFile/WriteFile buffer/length128,
original format/framing/checksum/migrations and actual native save remain OPEN.
No new-game engine or 8.0 retrojection.
