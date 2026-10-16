# Taiwan v1.0 R69/R70 — Early-return predicates and three conditional return shapes

Stage A original-static metadata and invented arithmetic only. Neither the
original client/Win32 APIs nor original save payloads are executed/evaluated.

## R69 source and bounded scope

A fresh 133-report census at main93ce004cceb5b46eec557b7fde091e2fe78e088a found
no decoded0x4c5fe row in six registered address-key / three operand-array-key
dictionary representations. Text address search found JSON/Markdown references
but no research text-dump instruction at that address. This is a bounded search,
not a claim about every possible encoding or all original content.

R69 reauthenticates the original runtime SHA256
`cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a`, then
rederives exact R67 raw SHA256
`8bb5923de9a630a953de6c62cf9c10463aed9a4066db9a0aa97c7aaff338ab50` before
extending it. The same139-node/156-edge bounded graph is retained exactly.
The focus is32 nodes in the root prefix through0x4c600 and late predicate
0x4c71c..0x4c72b. Exact one-hop incidence gives **38 decoded rows**. Original
overlaps with R63/R67 are compared exactly; proprietary source bytes are purged.

The formerly unknown0x4c5fe instruction is **XOR EAX,EAX**. Its two direct
predecessors are0x4c5fc and0x4c72b, both explicitly retained.

| Conditional structural route | Original syntax and limitation |
|---|---|
| Early frame-cell comparison | XOR EDI,EDI0x4c5f1; CMP[EBP+16],EDI0x4c5f3; flag-neutral initialization of frame[-8]/[-16]; JNE0x4c5fc fallthrough to zeroing EAX |
| Late pointer-shaped comparison | MOV EAX,[EBP+12]0x4c725; CMP byte[EAX],26 at0x4c728; JE0x4c72b to zeroing EAX |
| Common zero-tail exit | XOR EAX,EAX0x4c5fe; JMP0x4c600 to known POP/LEAVE/RET tail |

The late branch follows an outer TEST of byte memory with mask64. Its pointer,
memory validity and actual path are unproven. Neither the byte26 comparison nor
frame-slot geometry establishes a savedata field, authoritative argument role,
actual marker meaning, native count or successful write.

Source Action38851405164 at e33b38747ab0ca324e4a07a844b68c371a03c7c9:
original-static job116813227130; derived-only artifact12025561162, ZIP SHA256
`fc32c491277adb1bedeb8cbbf49fe8c72f86f68e42f00764b6e321896e205b1c`.
An independent download confirms the ZIP digest, sole25466-byte raw JSON,
SHA256 `26ff9f92d14a4ef385a279501e456b4bf58156209ad4471aef84109f6e16bfbe`,
and exact equality to permanent canonical Git blob
`d5d4924803dc28de8be00f712eecd11cf9003c66`.
Source-custody receipt: `STONEAGE-TW10-SAVEDATA-R69-SOURCE-CUSTODY.json`.
The independent CI guard requires the original source run/head/job, exact
raw hash/blob and custody, and compares the live ZIP when available. Expired/
unavailable artifacts are explicitly distinguished from a fresh ZIP replay.

## R70 direct-source closure is conditional, not runtime closure

Merge the exact R69/R67/R63 operand rows:103 of139 bounded nodes have decoded
metadata. Independently authored forward fixed-point and reverse predecessor
algorithms now agree on three full-EAX destination definitions before RET:

| Direct definition | Conditional architectural expression |
|---|---|
| XOR EAX,EAX0x4c5fe | 0 |
| SUB EAX,[EBP-16]0x4c743 | (incoming EAX − frame[-16]) modulo2^32 |
| OR EAX,0xffffffff0x4c759 | 0xffffffff |

The former **direct-return-source** unknown barrier is closed. This does not
decode the remaining36 function nodes, validate actual arithmetic inputs,
solve path feasibility, prove frame/callee/memory aliases or establish native
success/error conventions. Unknown middle instructions and calls remain opaque.

An instruction-shape arithmetic model and separately written formula are
compared on337 invented uint32 pairs per shape (1011 comparisons), including
zero, high-bit and wraparound cases plus deterministic invented samples. No
original memory or savedata values enter that model. Controls enforce full
register widths, exact literals/frame offsets, both entrances, flag-neutral
intervening stores, source hashes and nonpromotion fields.

Highest NEXT R71: first reuse retained R44/R69 evidence for initialization of
frame[-8]/[-16], INC frame[-16]0x4c653 and native output-count accumulation.
Determine the exact update/control and return-unit relationships only with
qualified operands/predicates and explicit frame/alias/callee assumptions;
acquire originals only for an identified remaining gap. Actual API return and
memory-output count, flush/close/persistence, savedata format/schema/checksum/
migration and server authority remain OPEN. Stage A families PARTIAL/OPEN;
Stage B remains gated. No game design decision is made.
