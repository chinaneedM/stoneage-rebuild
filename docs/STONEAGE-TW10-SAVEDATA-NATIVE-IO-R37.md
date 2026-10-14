# TW1.0 R37 — continuation helper and descriptor/handle candidate bridge

Status: READY after R36 independent original acceptance. No R37 original FACT admitted.

R36 finds the JNE direct target 0x4ed33 and three bounded continuation MOV-to-memory candidates (0x4ed5f AL, 0x4ed72 AL, 0x4ed92 EAX). AL is a low-byte projection with separate conservative EAX provenance, not a full 32-bit stored value. All destination addresses, alias ownership and original values remain unknown. EAX at the last store is an opaque CALL source at 0x4ed87, syntactically targeting 0x4c761.

Highest task: inspect original CALL 0x4ed49 -> 0x4e80a and CALL 0x4ed87 -> 0x4c761 on this continuation, with bounded pre-call PUSH/register geometry, exact direct target/boundary evidence and independent immutable original derivative custody. Qualify partial-register definitions 0x4ed57/0x4ed59/0x4ed69 (currently unmodeled whole-register writes), and trace source and destination address candidates for the three stores and any qualified helper entry stack/memory shapes. The parent later contains CALL 0x4edb0 -> 0x4a8dc (the accepted ReadFile candidate context); retain it as discovery rather than a demonstrated native-save route.

Never infer WINAPI/CRT ABI, nonvolatile ESI preservation, descriptor or successful handle identity, table initialization or alias ownership from names and numeric proximity. Keep actual filename → CreateFileA-result → ReadFile/WriteFile handle/buffer/length128, native framing/checksum/schema/persistence, server authority and cross-version equivalence OPEN. Original executable/media remain transient, unexecuted and unpublished; only bounded derived metadata may enter the repository. Stage A restoration first.


## 2026-10-14 — implementation ready for pinned original and independent review

The analyzer rederives exact accepted R36 original JSON SHA256872dbbf431891c19c27ddb0f6f5e87c466e89231e87e1a615a808aac0288a91c before inspecting original bytes. Two helpers have separate 768-byte/256-node graphs, 48 memory-reference samples and 24 opaque CALL samples with explicit caps. Original direct CALL support and full-text candidate boundary scans are separate from true entry/runtime alignment. No caller/helper value binding is assumed.

Three partial-register operand shapes have separately recomputed architectural slice geometry and preserved-parent-bit masks only for supported syntactic writes. No original state is evaluated; unknown or unsupported shapes stay unqualified. Stores and helper references have conservative pre-instruction family-register and address queries, including byte/word aliases. Stack/frame spelling, shared displacement0x1721760 and returning CALLs remain conditional candidates.

Tools: tools/stoneage_tw10_savedata_native_io_r37.py and its strict guard; tests/test_stoneage_tw10_savedata_native_io_r37.py; .github/workflows/probe-stoneage-tw10-r37-original.yml. Admit original STATIC facts only after source SUCCESS, immutable artifact custody, pinned derivative digest/size, independent strict negative controls and exact canonical JSON equality. Native handle/schema/persistence remains OPEN.
