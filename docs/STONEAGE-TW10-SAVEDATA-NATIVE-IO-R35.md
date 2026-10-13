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


## 2026-10-13 — R35 original static evidence independently accepted

The pinned nonexecuting original source Action [38418400068](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/38418400068), job `115368863099`, succeeded at source head `a02fd2464424a1974bcdf954aad0894589052614` and rederived exact accepted R34 digest `e95548eb5e9b60b1f5214ed751c1f3df9b83f27a4d20ebe35a49427cf9b32c34`. Original source was never executed; temporary archives and original executables were purged. Only derived JSON artifact `11824229823`, ZIP SHA256 `4c5cdd8677641d5588d738aa3286a0931e4c06590405f61fcffbd7901f483f33`, and JSON 5348 bytes SHA256 `5052a3d57b89f1d257846df6cef7c513fe544cadeb420e11f0a18468d3908f23`, was published.

Independent original source/artifact custody, strict semantic/tamper controls: [38418921425](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/38418921425) SUCCESS. Independent exact canonical JSON equality: [38419262860](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/38419262860) SUCCESS.

**FACT — original static only:** `CALL 0x4ed0e` is an indirect memory call linked to the original `KERNEL32.dll!GetFileType` import at IAT RVA `0x52160`. Pre-call straight suffix contains `PUSH ESI 0x4ed0d` at conditional ESP offset 0; its ESI may-source is `MOV ESI,EAX 0x4ed07`, whose EAX is conservatively unknown across `CreateFileA 0x4ed01`. At `TEST EAX,EAX 0x4ed14` the EAX source is opaque `GetFileType 0x4ed0e`; ESI at pre-`CloseHandle 0x4ed19` remains unknown across the same opaque CALL. These are graph-local syntactic candidates, not runtime values or proven callee preservation.

**OPEN:** actual API invocation, stack/ABI binding, real argument and return, successful handle, EDI sentinel, branch predicates, ownership and native filename → ReadFile/WriteFile concrete handle/buffer/length128/schema/persistence. Next R36 records path/branch candidate limits; Stage A only.
