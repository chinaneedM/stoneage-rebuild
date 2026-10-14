# TW1.0 R36 — GetFileType return-predicate and candidate handle-path audit

**Status:** READY for bounded synthetic and pinned-original nonexecuting static work; no R36 original FACT or runtime conclusion admitted.

## Primary historical question

R35 independently associated original RVA `0x4ed0e` with `KERNEL32.dll!GetFileType`, IAT RVA `0x52160`, with preceding `PUSH ESI 0x4ed0d`. R34/R35 established the syntactic `TEST EAX,EAX 0x4ed14`, `JNE 0x4ed16`, and conditional `PUSH ESI 0x4ed18` before `CloseHandle 0x4ed19`.

R36 should recover a bounded original candidate edge/path and EAX/ESI operand chain across these blocks while **keeping calls opaque**. Map conditional branch targets and branch-local stack geometry. Do not assume the original Windows ABI was followed, that ESI survived an intervening CALL, that GetFileType ran, or that a GetFileType return actually determined the JNE.

## Prerequisite and probe constraints

Reverify exact canonical R35 original JSON as a prerequisite (source 5348 bytes SHA256 `5052a3d57b89f1d257846df6cef7c513fe544cadeb420e11f0a18468d3908f23`). Original source always nonexecuting and transient. Bound path nodes/edges, flag writer candidates, conditional PUSH geometry and branch root contexts. Treat indirect call/return/callee register survival/stack aliases as unknown. No proprietary bytes, original strings or assets in outputs. Add synthetic negative controls and independent strict original artifact equality before promotion.

## Unclosed dependencies

Original native filename → verified CreateFileA returned handle → concrete GetFileType/CloseHandle and ReadFile/WriteFile handle → buffer/length128/schema/persistence remains OPEN. Do not connect separate global addresses or infer original server-side state from client-only candidates. No engine redesign while restoration Stage A is open.


## 2026-10-14 — R36 implemented bounded audit


Status: RESEARCH READY. Original static facts await a successful pinned original probe, immutable source/artifact verification, strict negative controls and exact canonical JSON equality.

R35 canonical derivative SHA256 `5052a3d57b89f1d257846df6cef7c513fe544cadeb420e11f0a18468d3908f23` must be exactly rederived from the authenticated Waei/JSS TW1.0 original retail executable and save sample. No historical executable or original-state arithmetic runs; transient source is unconditionally purged. Only bounded derived metadata may be published.

R36 jointly examines the original TEST EAX,EAX at 0x4ed14, JNE at 0x4ed16, structural routes to CloseHandle/GetLastError and the 0x4ed33 continuation. Route corridors and opaque CALL barriers are recomputed from a complete bounded topology (maximum 256 nodes/768 bytes), with explicit frontier and structural-return assumptions. Symbolic zero/nonzero conditions never evaluate original EAX or assert a real GetFileType result. Empty routes mean no route in this bounded graph, not absence of original behavior.

Compare physical pre-call PUSH operands at 0x4ed0d/0x4ed18 separately from value/ABI binding. Trace post-branch MOV-to-memory candidates and their conservative register sources to support the next handle-capture investigation. Same ESI spelling, reachable stores and PE import names do not establish actual preservation, handle identity, owners, successful IO or native save.

Files: tools/stoneage_tw10_savedata_native_io_r36.py; corresponding strict guard; tests/test_stoneage_tw10_savedata_native_io_r36.py; .github/workflows/probe-stoneage-tw10-r36-original.yml. Acceptance requires local synthetic/adversarial gates plus original-source and independent derivative custody gates before integration.

OPEN: actual filename → CreateFileA returned handle → ReadFile/WriteFile buffer/length128, framing/checksum/schema/persistence; true entry/frame/ABI, alias/global initialization/heap/CRT ownership, server and cross-version equivalence. Stage A restoration first; engine and redesigned game remain deferred.
