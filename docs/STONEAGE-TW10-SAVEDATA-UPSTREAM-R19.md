# TW1.0 R19 second-global write and HeapAlloc-boundary static probe

**Status:** TOOLING CANDIDATE, ORIGINAL R19 ADMISSION OPEN.

Follow accepted R18: `0x49a0c` exactly associates with IAT
`KERNEL32.dll!HeapAlloc`, not a proven allocation. Distinct writable
virtual `.data` at `0x1721878` has two direct static write
candidates (`0x49a14`, `0x4a0d5`) and six read candidates
in a linear `.text` scan, not verified executable paths.

R19 tests actual instruction shapes and source operands at both write
candidates, retains bounded candidate source-graph anchors and CALL
barriers. It identifies syntactic PUSH operations ahead of
`HeapAlloc` in a bounded reachable candidate graph without assigning
them to ABI slots or verifying arguments. It separately checks exact
`0x49e6e` direct CALL target and R8 bounded return gaps and exact
`0x49444`/`0x4945d` calls to the IMUL-root helper.

No native original program executes. All historical bytes stay
transient, are hash-gated against R18 and purged after derivation.
Only derived JSON may be published, with independent immutable-source
run identity, artifact digest and strict schema/no-promotions guard
before accepting any new original results.

Historical call execution, actual heap size/flags/handle, memory
allocation success, pointer/global object ownership, caller ABI,
branch feasibility, filenames/handles/buffer/128-byte native save
format and later-version projection remain OPEN. Restoration first.
