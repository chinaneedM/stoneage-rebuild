# Taiwan v1.0 R67/R68 — Native tail operands and conservative return sources

Stage A, original-static evidence only. The accepted original medium was
reauthenticated transiently; the runtime SHA256 is
`cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a`.
R63 was rederived byte-for-byte with SHA256
`91b650db700cf892a7d8c8b2d36a9d49dbeca139be315856d31d59533056c1bd` before
extending its metadata. No original client/Win32 API is executed; no savedata
payload is evaluated. Temporary proprietary source bytes are purged.

## R67 fixed-tail original metadata

The R28 bounded root remains 139 nodes / 156 edges with no frontier or node
cap. Its complete node list exactly matches R44/R45. R67 emits just **21
operand rows**: the 13 fixed tail positions and their exact direct predecessor/
successor neighborhood. Eleven previously missing positions are new evidence;
LEAVE0x4c75f and RET0x4c760 exactly requalify existing R44 evidence.

| Original static position | Decoded syntax |
|---|---|
| 0x4c731 / 0x4c73b | Write literal28 to global displacement24252936; write EDI to displacement24252940 |
| 0x4c741 | JMP0x4c759 |
| 0x4c743 / 0x4c746 | SUB EAX,[EBP-16]; JMP0x4c75c |
| 0x4c748 / 0x4c74f | AND global displacement24252940,0; write literal9 to displacement24252936 |
| 0x4c759 | OR EAX,0xffffffff |
| 0x4c75c–0x4c760 | POP EDI, POP ESI, POP EBX, LEAVE, RET |

The shared global displacement pair, literals9/28, subtraction and all-ones
register syntax do not establish original error names, actual API outcomes,
descriptor ownership, count values, savedata fields or persistence.

Source Action38824599576 at dc60f242a95bb34606e52037adc1efdaaa03b96f:
original-static job116729034463; derived-only artifact12014357270,
ZIP SHA256 `f4a627c9a1700bd8613e75e0d51465d537c9a3973668eca21cb53f8c8f0a3728`.
The independently downloaded ZIP matches that digest. Its sole raw JSON is
14911 bytes / SHA256
`8bb5923de9a630a953de6c62cf9c10463aed9a4066db9a0aa97c7aaff338ab50`.
Independent archive job116729256354 validates source job/artifact/raw identity
and the separately authored numeric guard before permanently storing metadata.
Canonical source Git blob `04162081d346b8c53424295de9fdc6b8f385b011` is byte-equal
to the independently downloaded artifact. The full source-custody receipt is
`STONEAGE-TW10-SAVEDATA-R67-SOURCE-CUSTODY.json`.

Future artifact expiry does not discard the source-authenticated permanent
metadata. The independent gate always requires the exact source run/head/job,
fixed raw SHA256/Git blob and custody receipt. When the temporary ZIP remains
available, it additionally compares its exact raw content; an expired or
unavailable artifact is explicitly reported without claiming a fresh artifact
download. Runtime/native behavior remains unproven in either mode.

## R68 independent EAX return-source audit

Two separately authored algorithms are applied to the exact pinned R67 bytes:
reverse predecessor traversal and forward token-set fixed point. Both use the
complete bounded address graph and 77 decoded rows from R67 plus pinned R63.
Missing instruction rows remain opaque barriers; CALLs kill incoming register
knowledge even when the decoder only lists ESP. Partial-register writes retain
unknown whole-register state. No branch feasibility is solved.

The algorithms agree on these direct EAX candidates before RET0x4c760:

| Candidate origin | Evidence status |
|---|---|
| SUB EAX,[EBP-16] at0x4c743 | Original full-width destination syntax; both arithmetic inputs remain unknown |
| OR EAX,0xffffffff at0x4c759 | Original full-width all-ones syntax; actual historical execution unproven |
| Unknown instruction at0x4c5fe | Explicit missing decoded-row barrier; do not assume zero or reuse an earlier value |

The third route reaches the POP tail through JMP0x4c600. It prevents claiming a
complete original return-value classification. Synthetic controls exercise
calls, missing rows, partial registers, merges, cycles, preserved non-EAX POPs
and entry unknowns. The archived R68 contract is exactly replayable.

## Next scope and unchanged boundary

Highest NEXT R69: first audit all retained savedata report representations for
the exact0x4c5fe row and its necessary incoming value/control context. If it is
still absent, obtain only the justified nonexecuting original-static early
return inventory. Then qualify conditional subtraction/count and all-ones
routes without flattening opaque caller/callee, frame/alias or native effects.
The R67 source already proves the tail; do not reacquire it merely to repeat
that discovery. Preserve full source custody and permanent derived metadata.
The R69 preflight now retains and independently rehashes all 130 savedata JSON
reports at canonical R67 commit87adb881234b9461d55b99fda3c2cafbd90c2e14.
None contains the0x4c5fe same-site mnemonic/operand dictionary; this remains a
bounded representation census, not a claim about all possible encodings.

Actual paths/return values, ABI/register/frame/memory preservation, OS BOOL and
transferred count, flush/close/disk persistence, savedata schema/checksum/
migration and server authority remain OPEN. Stage A families remain PARTIAL/
OPEN and Stage B remains gated. No game design decision is made.
