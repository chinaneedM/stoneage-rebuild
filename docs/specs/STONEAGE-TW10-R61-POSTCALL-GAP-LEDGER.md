# Taiwan 1.0 R61 — Exact native WriteFile postcall evidence-gap ledger

**Status:** bounded preflight from original-derived static metadata; NOT native execution, savedata byte output, flush, close, or durable persistence.

## Source custody

Reuses immutable original-derived reports R28 (`3671661219120d45bd922e05b6df371523b42432`), R44 (`39c1c0f673747fb560cc285d627490e5cd38047a`) and R45 (`1e7fb71cec336c1b4fc531d4f4a6933c9f66d415`). Only derived JSON is processed. The accepted TW1.0 client and original save bytes are neither executed nor released.

## FACT and evidence limits

- R28 bounds candidate root `0x4c5b4` at 139 nodes / 156 edges. The two `WriteFile` import sites `0x4c68c` and `0x4c6f1` have EAX probes at `0x4c692` and `0x4c6f7`. Both are sole `unknown_call` sources; neither is evidence for return values or bytes written.
- Prior heuristic graph reachability applies to the first WriteFile site, not the second; the later bounded graph contains both. This distinction is enforced independently.
- R44 already supplies **139 structural stack-effect candidates** for this native context. Those are not caller-to-callee argument values or proof of frame/register/memory preservation.
- R45 supplies **nine original-derived direct register-definition shapes before the first WriteFile call**, plus a bounded native context. These are valuable **pre-call** observations; they do not decode the post-call EAX/flags or establish the second site's actual execution.
- The absence asserted by this gate is explicitly scoped to these three pinned report surfaces; a source outside them must be separately audited before claiming an original instruction is unavailable.

## Exact remaining R62 inventory request

First recheck all retained original-derived static evidence for the post-call rows `0x4c692` and `0x4c6f7`, branch predicates and flag definitions through `0x4c5b4`. Independently qualify the caller boundaries `0x4a683 -> 0x4c5b4` and `0x48c5e -> 0x4c5b4`, stack/ABI register/memory clobbers and any transfer into the native number-of-bytes-written pointer. Only if no existing accepted inventory resolves the exact gap should a **narrow original-derived non-executing static probe** be acquired. Do not confuse a Win32 BOOL-shaped EAX return with the buffer/write-count pointer, a CRT count, a flushed byte count, or actual persisted bytes.

Code: `tools/stoneage_tw10_savedata_r61_gap_ledger.py`; adversarial mutations: `tests/test_stoneage_tw10_savedata_r61_gap_ledger.py`; gated CI: `.github/workflows/verify-stoneage-tw10-r61-gap-ledger.yml`. Historical FACT/HYPOTHESIS/DESIGN boundaries and Stage A restore-before-redesign gate unchanged.
