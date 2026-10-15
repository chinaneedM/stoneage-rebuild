# TW1.0 R51 — application comparisons, global stores and processor inventory

Status: READY; original derivation and independent acceptance pending.

Highest NEXT R51: qualify savedata application CMP EAX,57 at0x40195 and CMP EAX,127 at0x401c9 using exact stack-load/processor-output sources and bounded flag/control routes; separately qualify word comparisons at0x4019f/0x401e4, register literal4/5 definitions, byte stores at0x401a8/0x401af and their relation to global RVA0x13fbdac. Revisit processor0x47160 with all36 memory/control shapes, including the4 excluded by the R50 sample, and bound its input/output/algorithm structure. Do not assume decoded lengths, tag versions, migration, endianness, buffer alias or executed paths from these literals. Keep read/write callers distinct and opaque CALL/frame barriers explicit. Savedata schema/framing/checksum/persistence, original server authority and cross-version equivalence remain OPEN. Stage A restoration precedes joint future-engine/game review; system-family PARTIAL/OPEN gates unchanged.

Require authenticated nonexecuting originals, explicit graph/query/row caps, independent immutable custody, exact canonical derivative and meaningful synthetic/adversarial controls. Do not call 57/127 accepted record lengths or 4/5 schema versions before source binding and alternatives are qualified.


## R50-derived R51 preflight — 2026-10-15

This preflight reads only the accepted163325-byte R50 derivative (SHA2560badd1423f403a9e8a246a40518a68ee5a1bd67d380ea7ab3460fc3c607c3e94). It adds no original-media access and no executed-path claims.

| Branch RVA | Nearest ZF-source shape | Register definition candidate | Target / fallthrough |
| --- | --- | --- | --- |
| 0x4019d JNE | CMP EAX,57 at0x40195 | MOV EAX,[ESP+32] at0x4018e | 0x401c9 / 0x4019f |
| 0x401a6 JNE | CMP word[global0x13fbdac],CX at0x4019f | MOV ECX,4 at0x40198 | 0x401ce / 0x401a8 |
| 0x401cc JE | CMP EAX,127 at0x401c9 | MOV EAX,[ESP+32] at0x4018e | 0x401df / 0x401ce |
| 0x401eb JE | CMP word[global0x13fbdac],AX at0x401e4 | MOV EAX,5 at0x401df | 0x401bb / 0x401ed |

All four flag-source predecessor audits and input-source queries are uncapped in the admitted report. This qualifies graph-local definitions and nearest ZF producers, without evaluating loaded memory, concrete registers or flags. The two EAX comparisons share a load candidate, not a proven original decoded-length value. Word checks and subsequent byte writes have different widths; do not collapse them into a word-sized normalization.

Shortest structural witnesses in the accepted bounded edge set:

- 0x4019f ->0x401a6 ->0x401a8 ->0x401af reaches the two byte stores.
- 0x4019f ->0x401a6 ->0x401ce ->0x401cf reaches the status-byte store.
- 0x401c9 ->0x401cc ->0x401df ->0x401e4 reaches the other word comparison.
- 0x401e4 ->0x401eb ->0x401bb reaches the shared return-shaped suffix.

These are graph witnesses only. Mutually exclusive branch sides are separate alternatives; no route feasibility, success/error interpretation or executed normalization is proven.

Processor reconnaissance: sampled IDIV dword[ESI] sites0x4719f and0x471d6 are distinct and require exact signed EDX:EAX/divisor provenance. Byte loads/stores0x471c2/0x471cc and0x471f6/0x47201 have different address expressions and mutable stack-input candidates. The last retained memory/control row is0x47251; retrieve the missing4 from the same authenticated bounded graph rather than infer their operations. Recover the intervening register-only arithmetic and branch effects before choosing any compression/encryption/permutation description. EBP is loaded from a stack slot at0x47166 and must not automatically be treated as an EBP frame.


## 2026-10-15 — TW1.0 R51 complete processor/conditional caller geometry independently ACCEPTED

Fresh startup verified remote main HEAD1db7dfda81ef72f828fb3a862bc7e008947ef1d3/treed54c170b62607b5e0057c3e4da0a446b96728b43, latest commits/branches/Actions, README/protocol, exact continuity checkout (CURRENT-STATE1659709 bytes/blob2acccfdf9599d73c8f0616c9bf49f6a0c93ddc37), decisions/history/source registry and R51 scope. Prior main R50 and relevant provenance/PET gates SUCCESS. Every earlier continuity prefix preserved. Autonomous work-unit requirement remains at least15 minutes of effective work.

Original source Action38719176573/job116369203266 SUCCESS at HEADee32f6d16f3dbfeabbb9d73020b64f83f47924dd, branch agent/tw10-savedata-r51-processor-stack-consumers-20261015. Original archive/disc/runtime/save authenticated transiently; exact accepted R50 derivative rederived. Derived-only artifact11963713395 ZIP SHA2563e02a0c79114b8a3e2817a63ef4c6d280944435f4ad1106a213781484c2b4a8b; raw JSON284533 bytes SHA25615f54e5de8d1d20128fb7d948b54f13a0e3f6cf372eca203cbc7bb8adc473052. Independent Action38719540769/job116370411001 SUCCESS at HEAD26c3fc3698f1f930a0acf8296b145fdbe34fdd0e: immutable run/head/branch/artifact, exact raw size/digest, strict primary replay, canonical byte equality, exact nested R50 canonical bytes, postcall metadata contract regeneration and differential old/new stack-model equality at all115 instruction sites. Source553 tests PASS; independent567 tests PASS. Local36 pure metadata tests plus syntax/custody/prefix checks PASS; local capstone/pefile unavailable, so full local runtime tests are not claimed. Original media/executable never executed or published and always purged.

FACT (authenticated conditional original static):

- Full processor inventory115 instruction shapes matches R50 graph115nodes/124edges exactly, without graph frontier/node cap. All36 memory/control shapes are now available. The four newly retained rows are MOV DL,byte[ECX+EAX]0x47255; MOV byte[ECX+EAX],DL0x4725a; MOV EAX,dword[ESI]0x4725d; CMP ECX,EAX0x47260. Intervening NOT DL0x47258 is retained in the complete arithmetic inventory. No original register/byte result is evaluated.
- Fourteen ESP-relative operand references have conditional entry coordinates after numeric PUSH/POP/literal-ESP replay. Entry+8 maps to the physical pre-CALL+4 EDI push; entry+12 to pre-CALL+8 literal0; entry+20 to pre-CALL+16 ECX; entry+4 to pre-CALL+0 EDX; entry+16 to pre-CALL+12 global immediate25148844. This is near-CALL hardware geometry, not a proven original ABI or value. MOV[ESP+20],EAX0x47198 mutates the coordinate corresponding to the original first physical slot; later equal-slot spelling cannot be treated as its initial pointer.
- Local caller LEAs0x40177/0x4017b have conditional addresses pre-CALL+32/+36. The bounded processor has one normal RET candidate0x47268; four POPs balance four PUSHes, yielding conditional net near-CALL ESP change0 on normal return. Independent R38/R44/R50 and pure R51 stack models agree at all115 nodes. The post-CALL dword[ESP+32] load0x4018e therefore shares the ECX LEA coordinate under this bounded normal-return model. Actual stack address, successful return, alias, out-length contents and executed path remain unproven.
- Original entry MOV EAX,[ESP+8]0x47160; LEA ECX,[EAX-1]0x4716a; MOV ESI,[ESP+32]0x47173; MOV[ESI],ECX0x4717c are now jointly available with conditional slot mappings. They support an output-length-shaped hypothesis, not a measured read count, decoded payload length or accepted57/127 record schema.
- All seven signed IDIV shapes are retained: ECX0x47170; dword[ESI]0x4719f/0x471d6; EBP0x471b7/0x471ee; EDI0x4721e; EBX0x4722a. Register literal3/7/5 assignments, CDQ, byte IMUL/subtraction and final NOT are separate numeric shapes. Do not label the processor compression/encryption or infer original arithmetic results from these patterns.
- Division-focused source surface has64 queries without pending-query cap,39 candidate definitions,19 retained definition shapes and11 pending expansion definitions after two rounds; its definition sample is truncated. Complete instruction inventory does not establish complete dependency closure. Earlier R50 processor32/36 sampling remains historical and is superseded only for inventory completeness.
- Application four ZF contexts retain the exact57/127 comparisons and word/tag-shaped4/5 definitions from R50. Conditional geometry strengthens a candidate output-pointer correspondence; original field meaning, byte order, migration, successful normalization and persistence remain OPEN.

Initial source Action38718798517 failed synthetic gates on set/list membership, before original retrieval. Action38718948685 passed553 tests and derived originals but failed a new guard assumption that conflated source sampling with pending expansion. Corrected validation follows the already accepted R49 sampling contract; the final source and independent gates pass. No failed derivative admitted or original payload published.

Canonical primary/postcall/receipt: research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R51-ORIGINAL.json, STONEAGE-TW10-SAVEDATA-POSTCALL-R51.json and STONEAGE-TW10-SAVEDATA-NATIVE-IO-R51-ACCEPTANCE-R1.json.

Highest NEXT R52: qualify the seven processor IDIV sites0x47170/0x4719f/0x471b7/0x471d6/0x471ee/0x4721e/0x4722a with exact CDQ EAX-preservation/EDX-sign-extension syntax and bounded register-source expansion, keeping signed dividend, divisor, quotient and remainder distinct. Resolve the11 source-expansion pending definitions and19-of39 source-definition sample limitation using focused groups rather than suppressing caps. Bind only conditional caller ECX/pre-CALL+32 -> processor entry+20 -> ESI store0x4717c and post-CALL load0x4018e, with stack-slot mutation and memory-alias barriers explicit; qualify LEA EAX-1 -> ECX/store syntax and application57/127 checks without evaluating original bytes. Recover subtractive/NOT byte operations and loop predicates as syntax before assigning a historical algorithm/version/schema meaning. Native schema/framing/checksum/migration/persistence, original server authority and cross-version equivalence remain OPEN; Stage A restoration precedes joint future-engine/game design. System-family PARTIAL/OPEN gates unchanged.
