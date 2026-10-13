# TW1.0 R25 — boundary/caller candidates and partial-input provenance

Hash-pinned original Taiwan Waei/JSS1.0 runtime/savedata, static only.
Re-derive exact accepted R24 JSON and strict guard before this probe.
No historical executable runs and no original proprietary payload is exported.

Audit full raw .text linear candidate spans at conflicting starts and nearby
SET/LEA/SHL sites. Record candidate direct CALL/JMP/conditional targets within
two small windows, bounded samples, bytewise decode gaps and unresolved indirect
transfers. A direct CALL target is a useful entry candidate, never proof of an
executed/complete function or caller universe. Raw linear decoding alone does
not establish complete original instruction alignment.

Probe candidate starts0x499ff/0x4a0a1 and retain opaque CALL/branch/frame gaps.
Inspect SETE AL flag sources plus EAX before the partial write/next PUSH, without
composing a known whole-EAX value. Recover new-anchor EAX/ECX inputs at the
ReAlloc comparison and LEA, retaining unknown values and memory ownership.

TOOLING/SYNTHETIC READY. Original-only derived report, independent immutable
source/head/artifact and exact JSON custody required before FACT acceptance.
Native file/handle/buffer/schema/persistence, ABI/heap/CRT ownership and true
function-entry/actual-path closure remain OPEN. Restoration-first gate binding.

## 2026-10-13 independent acceptance supersedes READY status

Original source38392504284 at2437eac2c14bf8e8f983f0891effd055f8cd2940,
derived-only artifact11809322312, independent38392864515 exact JSON custody,
and59 synthetic/adjacent R24 tests38392504100 all PASS.

Full raw .text331776 bytes/104229 decoded instructions/eight gap bytes supports
scan boundaries0x499ff/0x4a0a1/0x499d0/0x4a0af/0x4a0b3, and interior offsets
0x49a00/0x4a0a0. Two windows yield19 transfers (6 CALL/2 JMP/11 conditional),
with4 direct CALL-target candidates0x499a8/0x499c3/0x499ff/0x4a09c. Whole-text
scan leaves677 indirect transfers unresolved. No executed-entry/all-caller claim.

Candidate graphs0x499ff/0x4a0a1 have15/14 and52/55 nodes/edges and reach the
heap CALLs. ECX before ReAlloc comparison/LEA loads four-byte virtual .data
0x1721864 at0x4a0a1; EAX input remains entry unknown. Old SETE roots0x499b0/
0x499c0 do not reach SETE/PUSH in their bounded graphs; empty source sets are
not proof that original sources are absent. Full EAX/flags/ABI/heap and all
native save/persistence still OPEN.

NEXT R26: direct CALL-supported0x499c3/0x4a09c candidate contexts for SETE
flag/EAX and ReAlloc comparison inputs; only qualified contexts can feed
future original filename/file-IO tracing. Preserve actual path/ownership gaps.
