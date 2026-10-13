# TW1.0 R36 — GetFileType return-predicate and candidate handle-path audit

**Status:** READY for bounded synthetic and pinned-original nonexecuting static work; no R36 original FACT or runtime conclusion admitted.

## Primary historical question

R35 independently associated original RVA `0x4ed0e` with `KERNEL32.dll!GetFileType`, IAT RVA `0x52160`, with preceding `PUSH ESI 0x4ed0d`. R34/R35 established the syntactic `TEST EAX,EAX 0x4ed14`, `JNE 0x4ed16`, and conditional `PUSH ESI 0x4ed18` before `CloseHandle 0x4ed19`.

R36 should recover a bounded original candidate edge/path and EAX/ESI operand chain across these blocks while **keeping calls opaque**. Map conditional branch targets and branch-local stack geometry. Do not assume the original Windows ABI was followed, that ESI survived an intervening CALL, that GetFileType ran, or that a GetFileType return actually determined the JNE.

## Prerequisite and probe constraints

Reverify exact canonical R35 original JSON as a prerequisite (source 5348 bytes SHA256 `5052a3d57b89f1d257846df6cef7c513fe544cadeb420e11f0a18468d3908f23`). Original source always nonexecuting and transient. Bound path nodes/edges, flag writer candidates, conditional PUSH geometry and branch root contexts. Treat indirect call/return/callee register survival/stack aliases as unknown. No proprietary bytes, original strings or assets in outputs. Add synthetic negative controls and independent strict original artifact equality before promotion.

## Unclosed dependencies

Original native filename → verified CreateFileA returned handle → concrete GetFileType/CloseHandle and ReadFile/WriteFile handle → buffer/length128/schema/persistence remains OPEN. Do not connect separate global addresses or infer original server-side state from client-only candidates. No engine redesign while restoration Stage A is open.
