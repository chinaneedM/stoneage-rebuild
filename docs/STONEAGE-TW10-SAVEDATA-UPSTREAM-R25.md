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
