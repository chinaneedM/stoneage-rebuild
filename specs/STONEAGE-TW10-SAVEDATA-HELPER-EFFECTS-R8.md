# TW1.0 R8 helper effects: bounded pure-return summaries

This tooling prepares independently checked helper summaries before R7 may
resume a caller after a CALL. No original helper has been admitted by this
synthetic-only milestone; a source hash, original callsite/root, full bounded
analysis and independently validated derived report are required later.

Seven x86 general registers receive distinct symbolic initial values. ESP is
a relative stack pointer and the entry return word receives its own label.
Supported R7 copies/stack-frame operations preserve identity; unaligned stores
invalidate overlapping cells and partial register writes destroy full identity.
Each ordinary RET records pre-RET stack delta, cleanup immediate, return-word
identity and the preserved-register set. EFLAGS/FPU/SIMD/external device state
are outside this summary and never declared preserved.

An effects summary qualifies only with at least one RET, no analysis gaps,
no state/return cap, no reachable state-graph cycle, zero pre-RET stack delta,
preserved return word on every return path and identical RET cleanup bytes.
All branch outcomes are conditional; common preserved registers are the
intersection over return paths. Unknown CALLs, indirect tail jumps, alias
stores, writes overlapping the caller region at entry ESP+4 or above,
unmodeled memory, far returns, traps and system/port transfers prevent
qualification. A possible terminating branch does not close a looping branch.

At most2048 states/32 unique return summaries. Qualification describes the
modeled seven-register/stack/return effects, not a historical ABI, actual
execution, file ownership, filename-to-CreateFileA connection, handle/buffer
provenance or128-byte serialization. No original byte/disassembly payload,
old executable execution or actual IO is involved in these tests.
