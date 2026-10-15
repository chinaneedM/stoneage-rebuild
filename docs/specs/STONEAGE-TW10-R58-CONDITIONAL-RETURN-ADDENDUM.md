# TW1.0 R58 — independently pinned conditional return bitpatterns

Evidence category: FACT for verified original **instruction syntax** only; OPEN for native call effects, return-value meanings, and persistence.

This addendum is scoped to authenticated Taiwan 1.0 nonexecuting static report
`research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R58-ORIGINAL.json`,
124989 bytes, SHA256 `04fb0b586f1fcf87f647b1bc1276bde2505822e195646c4c9058c03c7f558fe8`.
The original report is itself validated against the immutable R58 source
Action 38743841197 and independent source custody Action 38745267637.

The shared write/close helper root `0x4a657` contains `XOR EBX,EBX` at
`0x4a65d`, `OR EBX,0xffffffff` at `0x4a6a1`, and
`MOV EAX,EBX` at `0x4a6ae`, before RET `0x4a6b2`.
A contained CALL `0x4a683 -> 0x4c5b4` is followed by
`CMP EAX,EDI` `0x4a68b`. Thus zero/all-ones EBX **definition shapes**
exist, but any interpretation of returned EAX through opaque CALL and memory
barriers requires independently proven preservation/path conditions. The
comparison does not prove native bytes transferred.

The close-path root `0x4a53e` contains `XOR EAX,EAX` at
`0x4a5d4` and `OR EAX,0xffffffff` at `0x4a5e9`, before
RET `0x4a5f0`. The two memory-indirect CALL sites
`0x4a5a3` and `0x4a5ad` remain opaque. Literal bitpattern choices
are not verified OS/native success/error semantics or proof of flush, close,
file ownership, write completion, or persistence.

The deterministic pinned-spec tool
`tools/stoneage_tw10_savedata_r58_syntax_contract.py` fails closed when
its source byte digest or exact operand/target spellings change. Synthetic
negative controls mutate source registers, immediates and mnemonics.
Independent branch Actions 38744416744 and 38745294891 passed source custody,
reverse register traces and conditional-return checks. No original client
program or native I/O was executed.

R58 bounded root inventories remain accepted; **R59 is still highest NEXT**:
qualify the `0x4a683 -> 0x4c5b4` conditional output path against
existing authenticated R28/R57 evidence, then only the necessary close-path
indirect barriers. Do not convert static count/flag patterns into assertions
about persisted savedata bytes or historical error conventions.
