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
