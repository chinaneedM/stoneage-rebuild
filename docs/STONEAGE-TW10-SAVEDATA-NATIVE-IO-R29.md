# TW1.0 R29 — conditional scalar and shared-address syntax

Exact Taiwan Waei/JSS1.0 original runtime/savedata, static only. Revalidate
exact R28 original JSON SHA256296e5754a3eebafc6360cc45000ba73b6bcf1cc0a5d0ee439aa291eb45e0d645
and strict gate. Use original R28 CALL-supported contexts0x4a8dc/0x4c5b4.

Inspect five unmodeled register definition candidates0x4a8f9/0x4a8fc,
0x4c5d3/0x4c5e0/0x4c617 and their input provenance. A named scalar model
requires exact full-width register destination and supported operand shape;
partial widths, memory destinations and variable shifts stay unqualified.
Conditional scalar results are modular32-bit mathematics only. Actual inputs,
results, flags, branches, index ranges and API roles remain unknown. The
synthetic evaluator never receives original state or runs historical programs.
The general reaching-definition engine remains conservative at unmodeled writes;
new symbolic models are a separate evidence layer.

Architectural reference: Intel official SDM Volume2B, SAL/SAR/SHL/SHR,
printed pages4-584/4-585:32-bit counts use five low bits; SAR sign-fills and
rounds toward negative infinity, SHR zero-fills. No flag model is applied.
https://www.intel.com/content/dam/www/public/us/en/documents/manuals/64-ia-32-architectures-software-developer-vol-2b-manual.pdf

Recheck shared LEA displacement0x1721760+4*EAX syntax and inventory exact
immediate/displacement operands across raw .text, capped32 samples. Indexed
and indirect alias completeness, actual table contents/initialization, effective
addresses and shared file-handle/CRT owner are not inferred. Only bounded
metadata leaves CI; originals are nonexecuting and purged.
READY pending original source and independent exact JSON custody.

## 2026-10-13 independent acceptance supersedes READY

Original source38402348628, artifact11815337939, independent38402645534 exact JSON custody and64 synthetic/adjacent R28 tests38402348702 PASS.

- Exact R28 CALL-supported ReadFile root0x4a8dc and WriteFile root0x4c5b4 revalidated; graphs174/200 and139/156 nodes/edges unchanged within768 bytes/256 nodes, no frontier/node cap. Actual entries/paths/frames and returning-call effects remain unproved.
- Original definitions0x4a8f9/0x4c5d3 are SAR EAX by literal5, and0x4a8fc/0x4c5e0 are SHL ESI by literal3, all full32-bit register destinations. WriteFile0x4c617 is ADD EAX,ESI. Five separate conditional u32 models qualified by exact operand shapes; original values/results/flags/index/API roles never evaluated or admitted.
- ReadFile pre-SAR EAX has MOV EAX,ESI candidate0x4a8f4, fed by ESI memory-load0x4a8e4 [EBP+8]. WriteFile pre-SAR EAX has MOV EAX,ECX candidate0x4c5cf, fed by ECX load0x4c5bd [EBP+8]. EBP candidates come from respective MOV EBP,ESP0x4a8dd/0x4c5b5; ESP/frame/parameter identity unknown, matching offsets do not imply matching actual arguments.
- Pre-SHL ESI remains blocked by unmodeled definitions0x4a8f6/0x4c5d6. Write ADD input EAX comes from MOV [EBX]0x4c615; EBX has shared LEA0x4c5d9 or UNKNOWN_CALL0x4c60d candidates, and ESI has SHL0x4c5e0 or the same unknown call. No memory-value, alias or original address composition promoted.
- LEA EBX at0x4a8ff/0x4c5d9 retains common virtual writable raw-unbacked .data displacement0x1721760 with4*EAX index. Compact input/dependency surfaces5/8 queries have no truncation/limits; general reaching-definition semantics still leave SAR/SHL unmodeled, separate symbolic models do not silently change older evidence.
- Full331776-byte raw .text scan104229 instructions/eight gaps finds25 exact displacement/immediate operand candidates, all within32-sample bound. One matching direct four-byte MOV destination at0x4c9da and one immediate address operand at0x4e77f are identified; Other rows are read/address candidates, including direct and indexed operands. This exact-syntax inventory is not exhaustive alias/write/initialization or table/handle owner proof.

NEXT R30: inspect exact input definition shapes0x4a8f6/0x4c5d6 before SHL to qualify any conditional index/offset composition without asserting actual descriptor values, ranges or ownership. Audit direct MOV-to-shared-global candidate0x4c9da source and acquire coherent boundary/direct CALL support before using its context; immediate-address candidate0x4e77f may aid discovery. Continue native CreateFileA returned-handle capture and filename->handle->buffer/length128 with explicit call/stack/alias gaps; no CRT/table/native schema/persistence promotion. All original runtime/ABI/frame/owner/native-save gaps retained.
