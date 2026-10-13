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
