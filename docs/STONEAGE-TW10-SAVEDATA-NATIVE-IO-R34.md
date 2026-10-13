# TW1.0 R34 — CMP/TEST operands, CloseHandle caller PUSH and static input provenance

**Status:** READY for pinned-original derived-only static probe; no original R34 FACT admitted before independent artifact custody and canonical equality.

## Exact prerequisite and objectives

Recreate the accepted R33 original report from the pinned Waei/JSS TW1.0 retail disc and independently guard its SHA256 `1be7d372b0650b9944a12264b612531d46a5326af3628e12363df365ddab98b5`.

The R34 probe investigates the previously accepted original original-static sites:

- `CMP ESI,EDI` at `0x4ed09`; recover graph-local reaching candidates for ESI and EDI, not actual values or a claimed invalid-handle sentinel.
- `TEST EAX,EAX` at `0x4ed14`; recover EAX reaching candidates without assuming Windows success or failure.
- Imported `CloseHandle` at `0x4ed19`, pinned to `KERNEL32.dll` IAT `0x520a8`; decode bounded linear pre-CALL PUSH suffix and input registers with conditional ESP offsets. A structural PUSH is not a proven Windows API parameter, handle or executed call.
- Recheck ESI and EAX at CloseHandle CALL. A returning-CALL candidate graph does not establish actual caller execution, branch feasible paths, object/alias lifetimes, or API semantics.

## Static bounds and exclusions

Uses the existing R28 candidate parent graph (768 bytes/256 nodes), up to 24 local PUSH rows and 64 register/dependency queries limited to two levels. Original binaries and imported functions are not executed. Only bounded JSON metadata of operand shapes and syntactic register definitions leaves CI. No executable bytes/assets, original strings or proprietary code are published.

Semantic guard prohibits promoting any real EDI sentinel, actual Handle, CloseHandle input/effect, branch predicate or outcome, native filename->CreateFileA returned handle->ReadFile/WriteFile buffer/length128, file schema, persistence or heap/CRT/alias owner. The helper globals at `0x1721208/0x172120c` remain separate from the `0x1721760` address candidate.

Analyzer: `tools/stoneage_tw10_savedata_native_io_r34.py`
Guard: `tools/stoneage_tw10_savedata_native_io_r34_guard.py`
Negative controls: `tests/test_stoneage_tw10_savedata_native_io_r34.py`

## Acceptance

Synthetic and strict inherited R33 tests PASS; original R34 derived-only Action PASS with pinned original identity and unconditional purge; independent reviewer verifies immutable source run and artifact digest, replays strict tests and exact canonical JSON equality. Only then append full continuity/history/source documents and fast-forward main after fresh remote compare.

The next question is whichever original bounded source path remains open after R34. No production engine/game work begins until Stage A restoration acceptance.


## 2026-10-13 — Independently verified R34 original static candidate results

Pinned original source [Actions 38413940213](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/38413940213)
job `115353221738` SUCCESS at head
`44c96a0a3195fb847b7d443ca4fadb22e8d7e65a`.
Full inherited original TW1.0 retail client/runtime/savedata checks and
R33 exact SHA256
`1be7d372b0650b9944a12264b612531d46a5326af3628e12363df365ddab98b5`
rederived/strict-gated. Only derived evidence artifact
`11822613944` (name `tw10-r34-original-cmp-close-inputs-derived`,
ZIP digest `sha256:29057dd97c3275122b009c6f205c0585000b49dc0d630460e8ed78a3163d6f4e`)
uploaded. Original binary not executed or published; transient original
content purged. JSON 5542 bytes SHA256
`e95548eb5e9b60b1f5214ed751c1f3df9b83f27a4d20ebe35a49427cf9b32c34`.
Independent source/artifact custody run
[38414131854](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/38414131854),
job `115353899310` SUCCESS. Committed independent JSON equality is
verified by the subsequent independent reviewer run; this must succeed
before main integration.

**FACT — pinned-original static only:**

- `CMP ESI,EDI` at `0x4ed09` reads two full-width registers.
  Graph-local ESI candidate is `MOV ESI,EAX` at `0x4ed07`;
  earlier EAX at `0x4ed07` is opaque CALL `0x4ed01` (CreateFileA import).
  EDI at CMP is also conservatively `UNKNOWN_CALL 0x4ed01`.
  This **does not** identify an EDI sentinel, actual original values
  or an evaluated branch.
- `TEST EAX,EAX` at `0x4ed14` has graph-local EAX provenance
  `UNKNOWN_CALL 0x4ed0e`; the returned value, branch outcome
  and callee effect are unknown.
- The original straight local suffix contains exactly one
  `PUSH ESI` at `0x4ed18`, conditional pre-`CloseHandle`
  ESP offset `0`, stopping at an earlier control transfer.
  Its `ESI` source is conservatively `UNKNOWN_CALL 0x4ed0e`.
  Same unknown CALL affects ESI/EAX immediately before
  `CloseHandle` at `0x4ed19`. This is **not** proof of
  `CloseHandle` runtime argument binding, successful handle
  use or the return value.
- Original `CloseHandle` IAT remains `0x520a8`,
  independently distinguished from `CreateFileA` and
  `GetLastError`. Five primary query sites produced seven bounded
  input rows including dependencies; no actual register contents
  were inferred.

**HYPOTHESIS:** file-handle validation/cleanup sequence is plausible,
but the opaque `0x4ed0e` CALL is a critical boundary. Do not silently
connect original CreateFileA output to the CloseHandle input.
**OPEN:** original branches/paths, true EDI sentinel, EAX test value,
real API arguments/returns, native file read/write/length128/schema/persistence.

**NEXT R35:** identify pinned original CALL `0x4ed0e` through direct
target or IAT association and recover its conditional push/register inputs
without assuming effects; assess whether the gap can be narrowed before
any filename->returned handle->ReadFile/WriteFile claim. Stage A only.
