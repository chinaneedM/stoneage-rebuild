# TW1.0 R38 — caller/helper stack geometry and shared-store source qualification

Status: READY after R37 independent original acceptance. No R38 original FACT admitted.

R37 separates OR AL,1 at0x4ed57 from full-width SAR ECX,5 at0x4ed59 and SHL ESI,3 at0x4ed69. Earlier grouped partial-write terminology was provisional: the latter two are 32-bit shifts, not partial-register writes. Their operand/model evidence never evaluates original inputs. Parent EAX input before OR remains unmodeled0x4ed4f; ECX before SAR copies EBX0x4ed55; ESI before SHL has unmodeled0x4ed5c input. Preserve these gaps.

Highest next: qualify the first helper0x4e80a physical caller PUSH ESI0x4ed47/PUSH EBX0x4ed48 and helper entry [ESP+4]0x4e80a/later [ESP+20]0x4e83c with explicit stack-prefix changes, branch joins, CALL and memory-alias barriers. Reproduce any hardware slot correspondence separately from actual parameter values or ownership. Audit helper write destination0x4e862 [EAX+ESI] (EBX is a queried input family); recover its exact source operand width/shape, entry/data-address inputs and competing opaque SetStdHandle0x4e85a source. Recover scalar shapes at0x4e81c/0x4e829 and the shared0x1721760+4*ECX LEA0x4e822, using direct-CALL-supported candidate boundaries only.

Second helper0x4c761 shares LEA0x4c77a and has SetFilePointer0x4c7b0/GetLastError0x4c7bd imports plus byte RMW0x4c7d6. If relevant, inspect its ESP-relative PUSH geometry and scalar/address inputs without admitting original seek outcome, descriptor owner, CRT identity or caller-return effects. Keep parent original ReadFile-context CALL0x4edb0->0x4a8dc as independent discovery until linked by qualifying evidence.

Authenticated original source remains transient and unexecuted; publish only bounded derivative metadata with strict synthetic/tamper tests, immutable artifact custody and exact canonical equality. Actual filename → successful CreateFileA handle → ReadFile/WriteFile buffers/length128/schema/persistence, frame/alias/heap/CRT ownership and cross-version/server equivalence stay OPEN. Stage A restoration first.


## 2026-10-14 — bounded ESP model and exact source audit implemented

Exact accepted R37 derivative SHA256a16c858a46d502dec5c99fe43528601f0bc89449c671a717198725c95aa496d0 is rederived/guarded before original inspection. First helper has a separate bounded graph and replayable abstract ESP effects/edges. PUSH/POP widths are explicit; CALLs and other ESP writes are unknown, not guessed ABI cleanup. Branch offset joins, cycles, state/barrier/delta/update bounds, and unreachable query cases stay explicit. Geometry requires a 32-bit stack-address attribute and 32-bit near-CALL return slot; actual original stack attributes/contents are not established. Explicit memory writes remain alias/content gaps, independent of syntactic ESP arithmetic.

Two helper stack-read shapes are compared with prior physical PUSH suffixes using separately recomputed entry-relative/caller-relative offsets. No hardware slot candidate establishes real parameter/value/ownership binding. Exact store operands and scalar/LEA/source queries are emitted; no original state is evaluated.

Analyzer/guard: tools/stoneage_tw10_savedata_native_io_r38.py and corresponding strict gate. Synthetic/tamper/cycle tests: tests/test_stoneage_tw10_savedata_native_io_r38.py. Original probe: .github/workflows/probe-stoneage-tw10-r38-original.yml. Original STATIC acceptance awaits source SUCCESS, independent immutable custody, strict negative controls and exact canonical JSON equality. Native handle/schema/persistence remains OPEN; Stage A only.
