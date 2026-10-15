# Taiwan v1.0 R66 — Retained native count consumers and exact tail operand gaps

Evidence class: bounded original-static metadata and a registered-report census.
No original client/media is acquired or executed; no savedata payload is read.
The full earlier R27–R58 corpus preflight is replayed before extension. R65
requalifies immutable R28/R41/R63/R64 source blobs and exact R64 derivation.
The census then covers exactly 34 reports: R27–R58 plus permanent R63/R64.
Each report's complete raw-content Git blob, byte count and matching object
paths are retained in the permanent R66 derived report.

## What the existing operands support

| Conditional instruction path | Bounded static observation |
|---|---|
| 0x4c696 → 0x4c699 → 0x4c69c → 0x4c69e | Read EAX from frame[-12], ADD EAX into frame[-8], CMP EAX,EDI, signed JL to 0x4c6ab |
| 0x4c6fb → 0x4c6fe → 0x4c701 → 0x4c704 | Read EAX from frame[-12], store EDI at frame[+8], assign EAX to frame[-8], JMP toward 0x4c6ad |
| 0x4c6d9 → 0x4c6df → 0x4c6e2 | Opaque slot CALL, store returned-EAX-shaped value to frame[+8], JMP toward 0x4c6ab |
| 0x4c706 → 0x4c70c → 0x4c70f | Opaque slot CALL, store returned-EAX-shaped value to frame[+8], JMP toward 0x4c6ad |
| 0x4c6ad → 0x4c6b0 → 0x4c6b2 | Read EAX from frame[-8], CMP EAX,EDI, JNE target VA0x44c743 (RVA0x4c743) |

The first prefix contains XOR EDI,EDI at 0x4c6ab before the common join. The
second path's JMP to 0x4c6ad bypasses that instruction. Therefore EDI cannot be
declared zero on every rejoin merely from the nearby XOR spelling. R28 already
retains unknown-call barriers for original register values; these are preserved.
The first comparison is signed JL, which must not be silently replaced by an
unsigned byte-count test. No historical count or outcome is evaluated.

The offsets above refer to conditional client stack-frame geometry. They are
not savedata record fields. Equality across native CALLs still needs valid frame
preservation and memory/alias premises. A value stored after an opaque import
CALL is not automatically a proven OS error code. These instructions establish
neither actual output count nor actual caller-visible/native return values.

## Which tail rows are actually missing

The R44 native context retains 13 stack-effect observations at RVAs
0x4c731, 0x4c73b, 0x4c741, 0x4c743, 0x4c746, 0x4c748, 0x4c74f, 0x4c759,
0x4c75c, 0x4c75d, 0x4c75e, 0x4c75f, 0x4c760. Its separately retained decoded
operand records **already include** LEAVE0x4c75f and RET0x4c760 with no explicit
operands. No historical source acquisition is needed for those two shapes.

Across the 34 registered reports, the other 11 positions lack a dictionary that
contains the exact same-site `site_rva`, nonempty `mnemonic` and operand array.
This is a deliberately bounded representation census. It does not establish
absence from all project files, other encodings, original binary or all past
research. Raw site mentions and stack deltas do not supply decoded operands.
The tests distinguish adjacent dictionaries, string addresses, empty mnemonics,
multiple mentions and operand-free RET, and enforce the consumer geometries.

## Next minimal original-static scope

R67: authenticate the original source again only if still necessary after fresh
remote/corpus review, and extract instruction/operand/branch metadata at the
**11 missing** native-tail positions 0x4c731..0x4c75e, with direct successor and
predecessor edges needed to connect them to the accepted count/error joins and
retained LEAVE/RET. Requalify the known epilogue and the prior 139-node/156-edge
root identity; do not describe the epilogue as newly discovered. No raw code,
save payload, proprietary binary, observed native IO or persistence promotion.

Actual returning-CALL behavior, ABI/frame/register/memory identity, realized
branches, BOOL return, transferred bytes, flush/close/disk persistence, original
savedata schema/version/checksum/migration and server authority remain OPEN.
All Stage A families remain PARTIAL/OPEN, and Stage B remains gated.

## Expanded pre-acquisition preflight

Before any R67 original acquisition, the same-object classifier was also run
over **all 127 retained savedata JSON reports** at exact commit
`0694d23f021d547b6271c3ab5517440a5d2ddbc4`. None supplies decoded operand rows at
the 11 target positions in this representation. The permanent
`STONEAGE-TW10-SAVEDATA-R66-EXPANDED-TAIL-PREFLIGHT.json` records every source path,
raw byte count and Git blob. CI independently rehashes all 127 and repeats the
census. The original 34-report canonical R66 result remains unchanged. Other
encodings remain outside the absence claim; no original IO/format assertion is
promoted by the expanded search.
