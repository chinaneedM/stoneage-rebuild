# TW1.0 R24 — prefix barriers, EAX scalar and pre-call branch flags

Scope: hash-pinned Taiwan Waei/JSS 1.0 original runtime/savedata.
Re-derive R23 and require its exact accepted derivative SHA256 before R24.
Static only: never execute a historical program or publish original bytes.

Diagnose R23 suffix stopping instructions by operand shape and register writes.
Compare bounded candidate anchors without asserting verified instruction
alignment, complete incoming paths or real function entries. Recover EAX
at0x4a0b3 and its immediate register inputs; model a full-width constant left
shift only if original syntax qualifies, with unknown input/result and no
allocation-size/ABI role. Collect bounded pre-HeapReAlloc conditional branch
flag sources, including opaque CALL barriers and unknown outcomes.

TOOLING/SYNTHETIC READY. Original source and independently pinned exact report
custody are required for static FACT acceptance. Native file/handle/buffer,
serialization/framing/checksum/migrations/persistence and heap-owner gates OPEN.
Original client/library component ownership is not inferred from these heap
helpers. Restoration-first order remains binding.

## 2026-10-13 independent acceptance supersedes READY above

Original source38389572994 at1348831660debb1e86b4dec6cd270f2dcba3e126,
derived-only artifact11807971334, independent38389832057 exact committed
report equality and62-test synthetic38389574287 all PASS.

Important refinement: competing anchors can fall INSIDE a decoded instruction
from an earlier candidate start. HeapAlloc0x49a00 is inside[0x499ff,0x49a04)
under0x499e0/0x499f0; HeapAlloc0x499f0 is inside[0x499ed,0x499f2) under0x499e0;
ReAlloc0x4a0a0 is inside[0x4a09c,0x4a0a1) under0x4a090. No candidate is
selected as a true entry. The earlier0x49a00 memory-add shape is an alternate
decode diagnostic, not an accepted original memory-store fact.

HeapCreate stops at SETE AL0x499d0; flags and upper EAX bits unknown. Wider
HeapAlloc prefixes produce three final PUSH inputs (global0x172187c,0,320)
with conditional pre-CALL offsets0/4/8, stopping at RET0x499fe; no executed
path across RET, ABI arguments or allocation size is proved. EAX0x4a0b3 is
SHL2 with bounded LEA0x4a0af input ECX+4*ECX+80; JNE0x4a0ad compares32-bit
EAX vs ECX through flag-source0x4a0ab. Actual input/result/outcome/owner OPEN.

NEXT R25: coherent boundary/direct caller candidates near0x499ff/0x4a0a1,
SETE flag/upper-EAX and shifted ECX input gaps before native filename/IO
context can be qualified. Original native persistence remains OPEN.
