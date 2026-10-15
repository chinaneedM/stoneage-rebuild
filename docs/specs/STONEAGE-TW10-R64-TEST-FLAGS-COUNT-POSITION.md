# Taiwan v1.0 R64 — Post-WriteFile TEST and output-count pointer boundary

Stage: **Stage A original-static evidence**; not native-success or durable-persistence acceptance.

## Inputs and exact custody

R63 authenticated derived-only source: GitHub original probe Action `38754938642`, artifact `11983560690`, ZIP SHA256 `c6fef52e95757cae6682e3518a279a2ae572f4b86efd0e42c1a39aecd8f7931e`, raw derived JSON SHA256 `91b650db700cf892a7d8c8b2d36a9d49dbeca139be315856d31d59533056c1bd`. R28 original-derived immutable Git blob `3671661219120d45bd922e05b6df371523b42432`.

This is **source-free** work: no client media download, original program execution, Win32 API invocation or savedata payload read.

## Scope

Reconstruct both `0x4c68c -> TEST 0x4c692` and `0x4c6f1 -> TEST 0x4c6f7` windows, including the exact two `TEST` operand shapes, EFLAGS-writer identity, the first structural successor and its conditional branches when locally represented. Match each of five decoded local PUSH operands to R28's distinct physical conditional pre-CALL stack offsets 0, 4, 8, 12 and 16. The conditional 12-byte ESP slot may **only** be described as the `lpNumberOfBytesWritten` pointer-position *candidate* under the separate Win32 x86 calling convention/frame assumptions; it is not a validated pointer, an observed OS output, or an actual byte count.

The native `WriteFile` BOOL-shaped EAX return remains an opaque external-call value independent of the possibly written number-of-bytes-through-memory. `TEST EAX,EAX`, if identified, is still only original instruction syntax, not a realized return or taken branch. Conditional PUSH offsets are not proof of argument binding, stack-frame identity or preservation through other calls.

Acceptance requires independent source-authenticated branch CI, adversarial mutations, exact derived replay and explicit non-promotion on both sites. The entire original filename/handle/buffer/byte length, native return, flush/close and persisted record/migration/checksum chain stays OPEN; Stage B remains gated.
