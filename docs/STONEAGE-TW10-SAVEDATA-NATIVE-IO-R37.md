# TW1.0 R37 — continuation helper and descriptor/handle candidate bridge

Status: READY after R36 independent original acceptance. No R37 original FACT admitted.

R36 finds the JNE direct target 0x4ed33 and three bounded continuation MOV-to-memory candidates (0x4ed5f AL, 0x4ed72 AL, 0x4ed92 EAX). AL is a low-byte projection with separate conservative EAX provenance, not a full 32-bit stored value. All destination addresses, alias ownership and original values remain unknown. EAX at the last store is an opaque CALL source at 0x4ed87, syntactically targeting 0x4c761.

Highest task: inspect original CALL 0x4ed49 -> 0x4e80a and CALL 0x4ed87 -> 0x4c761 on this continuation, with bounded pre-call PUSH/register geometry, exact direct target/boundary evidence and independent immutable original derivative custody. Qualify partial-register definitions 0x4ed57/0x4ed59/0x4ed69 (currently unmodeled whole-register writes), and trace source and destination address candidates for the three stores and any qualified helper entry stack/memory shapes. The parent later contains CALL 0x4edb0 -> 0x4a8dc (the accepted ReadFile candidate context); retain it as discovery rather than a demonstrated native-save route.

Never infer WINAPI/CRT ABI, nonvolatile ESI preservation, descriptor or successful handle identity, table initialization or alias ownership from names and numeric proximity. Keep actual filename → CreateFileA-result → ReadFile/WriteFile handle/buffer/length128, native framing/checksum/schema/persistence, server authority and cross-version equivalence OPEN. Original executable/media remain transient, unexecuted and unpublished; only bounded derived metadata may enter the repository. Stage A restoration first.


## 2026-10-14 — implementation ready for pinned original and independent review

The analyzer rederives exact accepted R36 original JSON SHA256872dbbf431891c19c27ddb0f6f5e87c466e89231e87e1a615a808aac0288a91c before inspecting original bytes. Two helpers have separate 768-byte/256-node graphs, 48 memory-reference samples and 24 opaque CALL samples with explicit caps. Original direct CALL support and full-text candidate boundary scans are separate from true entry/runtime alignment. No caller/helper value binding is assumed.

Three partial-register operand shapes have separately recomputed architectural slice geometry and preserved-parent-bit masks only for supported syntactic writes. No original state is evaluated; unknown or unsupported shapes stay unqualified. Stores and helper references have conservative pre-instruction family-register and address queries, including byte/word aliases. Stack/frame spelling, shared displacement0x1721760 and returning CALLs remain conditional candidates.

Tools: tools/stoneage_tw10_savedata_native_io_r37.py and its strict guard; tests/test_stoneage_tw10_savedata_native_io_r37.py; .github/workflows/probe-stoneage-tw10-r37-original.yml. Admit original STATIC facts only after source SUCCESS, immutable artifact custody, pinned derivative digest/size, independent strict negative controls and exact canonical JSON equality. Native handle/schema/persistence remains OPEN.


## Architectural reference and shape classification

Intel SDM Volume1 §3.4.1/Figure3-5 (printed3-12; PDF page74) confirms IA-32 byte/word register slices: https://www.intel.com/content/dam/www/public/us/en/documents/manuals/64-ia-32-architectures-software-developer-vol-1-manual.pdf . This is an architecture reference, not original client runtime evidence. Full-width SAR/SHL conditional u32 semantics reuse the independently tested R29 model, whose official Intel SDM Vol2B instruction reference is already recorded. Original input/state arithmetic is never evaluated.

The candidate sites historically grouped as partial definitions are now inspected separately. The supported byte-slice model and supported full-width u32 model are independently recomputed from exact operands; unqualified classes remain explicit. Static original shapes/architectural geometry do not resolve original register, table, handle or memory values.


## Original static acceptance — 2026-10-14

S-grade authenticated TW1.0 original nonexecuting PE/static operands and bounded graphs; runtime/ABI/owner interpretations conditional. Exact R36 JSON SHA256872dbbf431891c19c27ddb0f6f5e87c466e89231e87e1a615a808aac0288a91c rederived/guarded. Final original Action38491613508/job115617870380 SUCCESS HEADdbc96073e032b2508e00ea23ba684902d8c68aeb; derived-only artifact11861673941 ZIP SHA25680a8bb5ff3233cd13f2a2a86558a228af782cfee9d0192bca18d3135a002cd58; JSON53751 bytes SHA256a16c858a46d502dec5c99fe43528601f0bc89449c671a717198725c95aa496d0. Independent immutable original/artifact custody, pinned digest/size,112 synthetic/tamper gates and exact committed-original JSON equality Action38491820292/job115618544412 SUCCESS. Originals purged, unexecuted and unpublished.

Static direct CALL-supported helpers0x4e80a/0x4c761, candidate linear boundaries,44/49 and51/55 graphs,12/15 memory refs,16/14 input queries, no caps. Both share0x1721760+4*ECX reference syntax; no original table/owner/content admitted. Imported SetStdHandle/SetFilePointer/GetLastError and conditional caller PUSH suffixes do not establish real handles, arguments, results, seek/persistence or CRT identity. Corrects provisional partial-write grouping: OR AL,1 is partial; SAR ECX,5/SHL ESI,3 are full32-bit. Unmodeled inputs and opaque calls remain OPEN. Canonical report research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R37-ORIGINAL.json; scope docs/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R37.md. NEXT R38 stack-prefix/store/source qualification. Stage A only.

Architecture reference (not historical original execution): Intel SDM Vol1 §3.4.1/Figure3-5, printed3-12 / PDF page74, https://www.intel.com/content/dam/www/public/us/en/documents/manuals/64-ia-32-architectures-software-developer-vol-1-manual.pdf ; IA-32 byte/word aliases. R29's official Intel SDM Vol2B scalar instruction references and synthetic u32 models reused for full-width shifts. No original values evaluated.
