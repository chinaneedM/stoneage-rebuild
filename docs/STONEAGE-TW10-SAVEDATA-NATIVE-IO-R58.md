# TW1.0 R58 — shared write/close helper and close-result obligations

Status: READY; R57 full wrapper metadata accepted, nested helper effects OPEN.

Highest NEXT R58: qualify the shared write/close helper0x4a657 (write CALL0x48c38; close CALL0x48586) and close-path helper0x4a53e (CALL0x48596), focusing on return predicates, deferred/native output and close-result propagation needed by R57. Audit existing metadata first: mere rows in an overlapping address window are not a function inventory and no row at either target root was found in the R57 preflight. Retrieve authenticated originals only for missing bounded root/callee/entrygraph evidence. Keep other cleanup helpers0x4a5f1/0x4853d opaque unless their effects are required for a specific live value; avoid generic CRT/allocator ownership exhaustion. Separate conditional full-count/buffer-copy returns from actual native output, shared-helper result and close/flush success. Preserve frame/EDI/ESI/EBP/alias/callee barriers, no original payload evaluation or client execution. Actual persisted bytes, record/tag/version/checksum/migration/schema, original server authority and cross-version equivalence remain OPEN. Stage A restoration before joint new-game design; all system-family PARTIAL/OPEN gates unchanged.

Preflight: a scoped union of113 savedata JSON reports (largest284533 bytes) contains no operand-bearing instruction at either0x4a657 or0x4a53e root. Thirty-six rows fall somewhere in the overlapping0x4a657..0x4a957 address window, which is not evidence for a graph rooted at0x4a657. The0x4a53e window has no such rows. Verify rooted contexts before deciding exact new original retrieval scope. Keep R57 full-count-without-native-call witness and caller ignored-close result as the concrete obligations.


### R57 main integration verification and R58 rooted-context audit

Milestone integrated at76daf076e3183a9525f2aee8154a35de76a0e729/treeb07b2887aa995ebe69a6b4f613c003e0118f467e. Main independent Action38741132645/job116442817255 SUCCESS:826 tests, exact original-report/contract custody and20 independent reverse return-source queries. Main PET38741133252/late-provenance38741132447 SUCCESS; branch independent38741126250/PET38741126623/late-provenance38741126477 SUCCESS. Exact checkout, raw/contract size and SHA, and every earlier continuity prefix verified.

R58 readiness audit searched all114 savedata JSON reports for integer-valued root-named keys equal to0x4a657/0x4a53e and found no rooted context. This complements the earlier no-root-instruction audit; nearby overlapping address-window rows are not treated as helper coverage. R57 verification path filters now include its producer/analyzer/primary guard dependencies so subsequent edits trigger independent acceptance. Highest NEXT remains R58; actual helper/native persistence semantics stay OPEN.


## R58 independently accepted branch evidence — 2026-10-15

Original source Action38743841197/job116452160761 SUCCESS (68 tests) with immutable derived-only artifact11976911506, ZIP SHA256 37ff56646a708744f9585eb7719fa313a6a053bcea9a9f6c38ac4bf2044601d2; raw124989-byte SHA256 04fb0b586f1fcf87f647b1bc1276bde2505822e195646c4c9058c03c7f558fe8. Independent Action38744746218/job116455318961 SUCCESS (83 tests), including exact source/artifact custody and12 reverse-register query matches. The first synthetic test Action38743718808 failed a test-list selector before source access; it was corrected and not accepted as an original source.

The shared helper root0x4a657 now has a40-node/44-edge complete CFG,5 predicates,4 memory writes, CALL0x4a683->0x4c5b4 and RET0x4a6b2 with direct EAX source MOV EAX,EBX0x4a6ae. The close helper root0x4a53e has66nodes/73edges,8 predicates,3 memory writes,8 calls (including2 memory-indirect) and RET0x4a5f0. Original direct wrapper/entrygraph bridges are confirmed. Both graphs have no frontier/cap and remain static-only.

NEXT R59: pursue 0x4a657->0x4c5b4 specific result/flush obligations and 0x4a53e close-path indirect-callee/return barriers using retained metadata first. Actual WriteFile/flush/close, saved bytes, schema/checksum/migration/server authority remain OPEN. The modern game phase does not begin from this evidence.
