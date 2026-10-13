# Taiwan v1.0 R32 — opaque intervening CALL, conditional branch and stack-slot geometry

**State:** READY FOR ORIGINAL STATIC PROBE; original R32-derived report has **not yet** been independently accepted.

## Exact prerequisite

The accepted R31 original report is replayed and passed through its strict guard before
R32 output is eligible. Its canonical SHA256 is
`af1e1ee0fb61549e89b6e168e82c5c7b58de170e9a1bb7f9ed2968c095cebdcc`.
The complete original runtime and savedata hash gates continue to apply.
Original binaries remain transient, non-executed and never published.

## Targeted questions

1. Revalidate the original intervening CALL at RVA `0x4ed1f`, after the
   post-CreateFileA EAX->ESI candidate at `0x4ed07`, but before
   `PUSH EAX` at `0x4ed25` and helper CALL at `0x4ed26`.
   Emit direct/indirect target or import association **only** when supported
   by the pinned original instruction, with runtime effects unknown.
2. Record bounded direct-target conditional branch syntax between
   `0x4ed07` and `0x4ed26` when a returning-CALL-assumption graph edge can
   structurally reach the helper call. Independently mark target and fallthrough
   structural reachability. Do not claim feasibility, predicate truth or taken path.
3. Compare conditional physical x86 CALL entry stack offsets:
   `PUSH EAX` at pre-call offset 0 versus the helper's
   `[ESP+4]` first instruction. This qualifies only a *potential hardware
   slot correspondence*. An intervening CALL, any unmodeled stack/path effect,
   and true caller-to-callee ABI/data values still block argument binding.
4. Re-query bounded register provenance for ESI at `0x4ed07`,
   ESI/EAX at the intervening CALL, EAX at the PUSH and ESI before helper
   CALL. The result is graph-local and cannot imply a successful CreateFileA
   handle, a filename role, actual memory mutations or persistent savedata.
5. Do not conflate helper's `.data` address candidates `0x1721208` /
   `0x172120c` with the separate shared address candidate `0x1721760`
   found in ReadFile/WriteFile contexts.

## Scope and reproducibility

Analyzer: `tools/stoneage_tw10_savedata_native_io_r32.py`.
Fail-closed guard: `tools/stoneage_tw10_savedata_native_io_r32_guard.py`.
Synthetic negative controls:
`tests/test_stoneage_tw10_savedata_native_io_r32.py`.

R32 reuses R31's full pinned provenance chain, with candidate graph capped at
768 bytes/256 nodes, up to 24 direct conditional branch candidates,
up to 64 register-source queries and two dependency levels. It exports only
bounded structured metadata; never native machine code, original file bytes,
PII, secrets or assets.

**Not proved:** executed original path, branch predicate, returning-call effects,
API success, actual handle value, stack frame ownership, helper argument
binding, alias/heap/CRT or file ownership, native read/write buffers and 128
byte payload semantics, file schema or persistence. All remain OPEN.

## Acceptance gate

- R32 and R31 synthetic/negative tests PASS.
- R32 original source Actions downloads the exact pinned original, validates
  inherited full identity and strict prior SHA, emits at most 75 KB JSON,
  and purges all original content in an unconditional cleanup step.
- A distinct reviewer workflow fetches the immutable original Action
  artifact, verifies run identity, digest, guard compliance and exact
  equality against a committed canonical JSON witness.
- Only then update `docs/CURRENT-STATE.md`, history and source registry,
  and integrate main by non-destructive ref update.

**NEXT if original passes:** examine actual R32 CALL identity and branch
candidates; assess whether additional graph/path or original machine
instruction evidence meaningfully narrows the native save chain. Do not
advance to engine implementation before Stage A restoration acceptance.
