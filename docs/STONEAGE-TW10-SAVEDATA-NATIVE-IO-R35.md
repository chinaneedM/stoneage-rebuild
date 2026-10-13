# TW1.0 R35 — original opaque CALL at 0x4ed0e and conditional input provenance

**Status:** RESEARCH READY; no R35 original FACT admitted prior to original Actions success, independent immutable-artifact custody, and exact canonical JSON equality.

## Prerequisites

- Authenticated Taiwan Waei/JSS TW1.0 clean retail baseline, nonexecuting.
- R34 original report canonical SHA256 `e95548eb5e9b60b1f5214ed751c1f3df9b83f27a4d20ebe35a49427cf9b32c34` rederived by the same executable and save sample.
- Retain R34's exact legacy record and historical ledger without destructive replacement.

## Highest-priority R35 question

Resolve the syntactic original CALL at RVA `0x4ed0e` in the CreateFileA continuation, distinguishing an original direct target, register-indirect call, memory-indirect target, or exact PE IAT import-slot association.

Bounded pre-CALL instructions are decoded from `0x4ed07` to `0x4ed0e`; a suffix of qualifying PUSH operands and ESP offsets is reported **conditional on this path**, never as an executed Windows ABI argument list. Examine EAX, ESI, EDI before that CALL, EAX at TEST `0x4ed14`, and ESI before CloseHandle `0x4ed19`; the opaque CALL conservatively blocks all claimed callee-preservation or returned-value conclusions.

## Evidence rules

A successful original probe can promote only original x86 opcode/operand form, bounded graph locality, and import-table association (if any) to **FACT (static)**. Do not infer runtime call, actual API parameters, branch outcomes, returned handle, EDI sentinel, error status, ownership or aliases. In particular, neither one physical PUSH nor one Windows import name establishes native save persistence or recovered schema.

Original archive and executable must not run or be uploaded. GitHub Actions may temporarily download/extract the pinned source with unconditional cleanup and upload only bounded derived JSON metadata (no instruction bytes, original strings or proprietary assets).

## Files and acceptance

- Analyzer: `tools/stoneage_tw10_savedata_native_io_r35.py`
- Strict provenance gate: `tools/stoneage_tw10_savedata_native_io_r35_guard.py`
- Invented synthetic negative controls: `tests/test_stoneage_tw10_savedata_native_io_r35.py`
- Original derived-only probe: `.github/workflows/probe-stoneage-tw10-r35-original.yml`

**Acceptance gates:** tests pass; original source run succeeds with R34 exact digest; independently verify immutable source run/artifact identity/digest, independently replay strict negative controls and canonical equality. Then append rather than overwrite full `docs/CURRENT-STATE.md`, timeline and source registry, and integrate only with a freshly verified main.

**OPEN:** filename → successful CreateFileA returned handle → ReadFile/WriteFile concrete handles, buffer, length 128, schema and persistence; object/heap lifetime, server-only content and cross-version equivalence. Continue Stage A restoration, not redesign.
