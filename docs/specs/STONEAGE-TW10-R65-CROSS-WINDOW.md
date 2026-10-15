# Taiwan v1.0 R65 — Retained cross-window JE, flags and count-pointer geometry

Stage A original-static metadata only. This work reuses permanently retained
R28/R41/R63/R64 reports; no original medium is downloaded, original code run,
Win32 API invoked, or original save payload evaluated. All four source Git blobs
are pinned by both the derivation and a separately authored numeric verifier.
R41 supplies the original image base `0x400000` with the same runtime identity;
R64 is replayed exactly from R63/R28 before extension.

## Cross-window control evidence

The R63 first window ends before the first JE's target, but the **second** R63
window already contains that target. Missing from one window does not mean
missing from the retained evidence corpus.

| TEST / JE RVAs | JE decoded target VA | Normalized target RVA | Evidence |
|---|---|---|---|
| 0x4c692 / 0x4c694 | 0x44c6d9 | 0x4c6d9 | Target row in second window; branch edge reconstructed from immediate operand |
| 0x4c6f7 / 0x4c6f9 | 0x44c706 | 0x4c706 | Target and branch edge retained in second window |

Both target rows decode indirect CALL through slot `0x5208c`. This report keeps
the call opaque. Its imported function's actual dispatch, result and effects
are unproven. The first target's continuation rejoins `0x4c6ab` through JMP
`0x4c6e2`; second-window JMPs `0x4c704` and `0x4c70f` target `0x4c6ad` in the first
window. Those three cross-window edges are **operand-derived**, not original
edges retained inside either R63 window.

The union contains 60 original decoded rows and 55 retained local edges. The
sole retained direct predecessor of each JE is its TEST EAX,EAX, whose decoder
metadata writes EFLAGS; JE reads EFLAGS. This closes a bounded direct-edge
flag-source question. It does not prove all predecessors of the full original
139-node graph, a feasible executed path, or an actual value of EAX/ZF. The
conditional x86 relation is JE takes its target if ZF=1 after a zero TEST result.

## Count-pointer provenance and temporal alias barrier

| Candidate | Retained prefix | Following frame-local read |
|---|---|---|
| First call | LEA EAX,[EBP-12] 0x4c679 → PUSH 0 at 0x4c67c → PUSH EAX 0x4c67e | MOV EAX,[EBP-12] 0x4c696 |
| Second call | LEA ECX,[EBP-12] 0x4c6e4 → PUSH EDI 0x4c6e7 → PUSH ECX 0x4c6e8 | MOV EAX,[EBP-12] 0x4c6fb |

Each short LEA-to-PUSH chain is an unambiguous retained path with no intervening
write to the pushed register and no intervening CALL. R64 independently binds
the PUSH shape to the conditional pre-CALL ESP+12 candidate. Under unproven
stdcall argument binding, the slot is output-count-pointer-shaped. The two
postcall loads share the **spelling** EBP-12, not a proven original runtime
address. EBP_before_call and EBP_after_call must remain distinct symbols until
frame/callee preservation, memory validity, argument binding and actual API
memory effects are separately qualified. No output count is known.

## Acceptance and next scope

The permanent derived report is replayed exactly; independent validation uses
separate decimal-coordinate assertions and does not import the R65 derivation.
Controls mutate source custody, VA/RVA base, branch target/window classification,
flag predecessors, pointer prefix/register/offset, opaque-call slot, temporal
alias assertions, persistence and phase promotions. Mutation inputs are tests,
not accepted history. Branch and main Actions must pass before final acceptance.

R66 should first audit retained native-context return/count consumers and exact
predicate/return-row coverage, including paths from frame-local count reads and
opaque error-call rejoins. Acquire additional original-static rows only after
an explicit corpus gap. Native execution, actual BOOL/count, valid address and
ABI/alias preservation, flush/close/persistence, savedata fields/schema/version/
checksum/migration and server authority remain OPEN. Stage A family gates remain
PARTIAL/OPEN; Stage B remains gated. No new game design decision is made.
