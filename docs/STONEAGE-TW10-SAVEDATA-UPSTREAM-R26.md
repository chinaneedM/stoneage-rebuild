# TW1.0 R26 — CALL-supported contexts and conditional expressions

Exact Taiwan Waei/JSS1.0 original runtime/savedata, static only.
R25 exact derivative/hash and strict gate rederived before R26; direct CALL
syntax must independently match0x49864->0x499c3 and0x49e5f->0x4a09c.
No original program or original-state expression is executed or published.

Recover SETE AL flags plus EAX before partial write/PUSH from0x499c3,
retaining entry/path/opaque CALL uncertainty. Formal low-byte composition
preserves upper24 bits; only a unique full-width zero assignment in the
candidate graph permits conditional possible EAX values0/1, never an actual
runtime value, ABI heap flag or successful call result.

Recover ReAlloc EAX/ECX comparison, LEA and SHL inputs from0x4a09c.
An affine expression requires unique LEA->SHL candidate provenance and exact
full-width/register/operand shape. It stays modulo32-bit arithmetic, with
original ECX/result/argument size, heap owner and actual paths unknown.

TOOLING/SYNTHETIC READY; original-derived report and immutable independent
source/head/artifact/exact JSON custody required before static acceptance.
Native filename/handle/buffer/schema/persistence and CRT/heap/alias ownership
remain OPEN. Restoration-first gate remains binding.

## 2026-10-13 independent acceptance supersedes READY status

Original source38394940020 at e16213cb60a1a560fa31a9d15fad39626e9052e6,
derived-only artifact11811375871, independent38395234686 exact JSON custody,
and56 synthetic/adjacent R25 tests38394939510 all PASS.

Create candidate root0x499c3 has20nodes/20edges, reaches SETE/PUSH, EAX unique
conditional zero definition0x499c3 and CMP0x499c7 flag source ([ESP+8] vs EAX,
four-byte operands). Conditional SETE composition permits EAX0/1 under this
candidate link. No actual frame/ZF/full-EAX or HeapCreate ABI role admitted.

ReAlloc candidate root0x4a09c has53nodes/56edges: EAX comparison source is
virtual .data0x1721874 and ECX comparison/LEA source is separate0x1721864,
both four-byte loads, original contents unknown. Unique LEA0x4a0af->SHL0x4a0b3
link gives conditional20*ECX+320 modulo2^32. No original result/actual allocation
size/ABI/heap/CRT owner follows. Existing alias/caller-return gaps retained.

NEXT R27: return to exact original CreateFileA0x4ed01 and ReadFile/WriteFile
boundary/direct-caller/physical argument evidence, with new boundary methods
and independent original custody. Allocator/class/owner and caller-frame gaps
remain explicit while native file IO is investigated. Native save OPEN.
