# TW1.0 R59 — existing-source shared WriteFile root preflight

**Status:** authenticated static-identity bridge preflight ACCEPTED; native
execution, native error meaning, bytes written, flush/close and persistence OPEN.
This is **not** R59 semantic completion and does not change Stage A family
PARTIAL/OPEN gates.

The existing accepted Taiwan v1.0 numeric-only reports suffice for this
scoped preflight. No original media were downloaded, decoded as savedata,
executed, evaluated as native API calls or published anew.

| Prior source | Exact derived JSON SHA256 | Static role |
|---|---|---|
| R28 | `296e5754a3eebafc6360cc45000ba73b6bcf1cc0a5d0ee439aa291eb45e0d645` | CALL-supported `0x4c5b4` root inventory |
| R57 | `3e562ab02a80e0f6516f8a91c93b897eef05f606be62f1df5cb48686d64114e6` | wrapper `0x48c5e` direct caller |
| R58 | `04fb0b586f1fcf87f647b1bc1276bde2505822e195646c4c9058c03c7f558fe8` | shared helper `0x4a683` direct caller |

**FACT (bounded original syntax only):** R57 wrapper CALL `0x48c5e`
and R58 shared helper CALL `0x4a683` both point directly to
`0x4c5b4`. R28 already supplies a **139-node, 156-edge**
768-byte/256-node candidate CFG for that root without frontier/cap, and
the `WriteFile` import-identity shapes at `0x4c68c` and `0x4c6f1`
appear in that candidate graph. R58's postcall `CMP EAX,EDI` at
`0x4a68b` is independently matched by its operand geometry.

**OPEN:** These observations do not establish that an actual R58
runtime call reaches either WriteFile instruction, that arguments/handles
or alias lifetimes match a Windows ABI, or that a native call wrote bytes,
flushed, closed, persisted or returned a particular success/error code.
The bounded R28 graph is a structural candidate; its returning-CALL
continuations are assumptions, not execution traces.

Reproducible tool: `tools/stoneage_tw10_savedata_r59_prior_bridge.py`.
Seven targeted adversarial tests passed on source/branch Action
`38746531921`; immutable derived worksheet artifact
`11978672432`, ZIP SHA256
`c203e89ae68139cbbe55a9c130bd86494e49b2ab6c740224aec3eaab0ec04001`.
The original source digests, changed call roots, changed import names,
altered graph frontiers and changed EAX/EDI comparison each fail closed.

**R59 next:** use existing original numeric graph/operand metadata to
establish conditional path feasibility, subcall argument propagation,
buffer-state writes, register/flag barriers and actual callback/return
limits. Reacquire originals only if a precisely documented missing numeric
inventory is demonstrated. Retain the original close-side
`0x4a53e` indirect-call and native result gaps. The project remains in
Stage A restoration before new-engine co-design.
