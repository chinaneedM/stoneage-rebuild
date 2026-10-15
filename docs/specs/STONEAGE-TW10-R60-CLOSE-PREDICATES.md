# TW1.0 R60 — Native WriteFile return uncertainty and close/error path topology

Status: **original-derived static syntax only**. Stage A historical restoration; no original code, save payload or Win32 API executed.

## Custody and audit scope

R28 original-derived static JSON is pinned to Git blob `3671661219120d45bd922e05b6df371523b42432`; R58 to Git blob `223b65683d37332546ada0fe034a81550b5e8ed8` and SHA256 `04fb0b586f1fcf87f647b1bc1276bde2505822e195646c4c9058c03c7f558fe8` (124989 bytes). Neither the authenticated original Taiwanese executable nor original savedata payload is read or executed. This audit does not substitute a later version's CRT/runtime semantics.

## FACT — native-context return source remains opaque

Within R28's 139-node / 156-edge WriteFile candidate root `0x4c5b4`, both import calls (`0x4c68c` and `0x4c6f1`, slot `0x520a4`) have corresponding post-call EAX probes (`0x4c692`, `0x4c6f7`). The original-derived reaching-source inventory classifies each EAX as `unknown_call`, with actual value unknown and external return unproven. The second call site is present in the bounded graph but **not** reached in the earlier prior graph; these distinct coverage claims must remain separate. There is no accepted written-byte count, successful native call, or persistence witness.

## FACT — bounded close helper static branch topology

The R58 `0x4a53e` bounded root has 66 nodes and 73 edges; two memory-indirect sites match `CloseHandle` (`0x4a5a3` / IAT `0x520a8`) and `GetLastError` (`0x4a5ad` / IAT `0x5208c`). Four independent shortest structural witness families reach RET `0x4a5f0`, under the explicit **returning CALL and unconstrained branch** assumptions:

1. An early range-guard branch bypasses both OS-call sites, visits global write shapes `0x4a5d8`/`0x4a5df`, and reaches `OR EAX,0xffffffff` at `0x4a5e9`.
2. A path visits `CloseHandle`, tests `EAX` at `0x4a5a9`, takes the `JNE` successor at `0x4a5ab` to `0x4a5b7` (setting EBP to zero), bypasses `GetLastError`, and reaches `XOR EAX,EAX` at `0x4a5d4`.
3. A path visits `CloseHandle` and `GetLastError`, copies EAX to EBP at `0x4a5b3`, takes the `JE` successor at `0x4a5c9`, then reaches the same zero-shaped result.
4. A parallel `GetLastError` path takes the other `0x4a5c9` successor, visits opaque call `0x4a5cc`, then reaches the all-ones-shaped result.

Only the original static operand spellings and structurally allowed edges are demonstrated. Conditional native return values, handle identity/ownership, callee clobber, error attribution, register preservation, branch feasibility, actual flush/close completion and disk persistence remain **OPEN**. The all-ones/zero register patterns are **not** licensed as original error/success conventions.

## Acceptance and next gate

`tools/stoneage_tw10_savedata_r60_close_predicates.py` validates immutable source Git blob and SHA256 custody, exact return-source and import-slot identities, complete bounded graph rows, critical branch successors and operand shapes; a deterministic BFS derives the four witness families. Mutation tests reject forged postcall values, branch deletion, register changes, import swaps and false runtime claims. GitHub Actions separately executes the R28/R58 original-derived guards, R60 and inherited R59 tests, and derives/replays the exact output without executing original binaries.

**NEXT R61:** Identify the exact missing R28 `0x4c5b4` postcall operand/control rows and the cross-function call/ABI/frame/register effects needed before any native-result interpretation. If no already-pinned source supplies those rows, seek only the precisely delimited original evidence rather than broad re-extraction. Do not promote static return/branch shape to persisted savedata or begin Stage B game redesign.
