# TW1.0 R18 original upstream CALL / distinct global / CFG frontiers

**Stage:** original probe pending; synthetic-only tools are not historical acceptance.

Pinned R17 recorded a four-byte source-EAX global write at `0x49a2c`, a
source-ECX global write at `0x49d78`, and a source-EBX global write
at `0x49e88`. These are static write candidates into `0x172186c`.
No original runtime value, function entry, call return, ownership, save
format or native operation is proven.

R18 source analysis examines the exact `0x49a0c` CALL that blocks the
EAX source, preserving the distinction between exact transfer target
and *qualified* callee return/effect. It scans full linear `.text`
candidate references to independent writable virtual global
`0x1721878` which is the candidate input at `0x49d72`, with
unknown aliases and execution. It reuses R14's bounded `0x49d93`
CFG to seek `0x49e88` EBX definitions; the bounded CFG anchor is not
a function entry and CALL fallthrough is structural. Finally it
symbolically follows the short original `0x484c0` to IMUL `0x484c7`
prefix in a model-only stack frame; no actual stack address or caller
argument ownership is inferred.

The original probe checks inherited exact archive, executable and
savedata identity, emits non-executing limited JSON evidence and
purges all originals. Independently pin original workflow source/head,
artifact digest, JSON shape/no-promotions and exact copied report
**before** promoting an R18 conditional static evidence receipt.

Original save filename→CreateFileA, handle→ReadFile/WriteFile buffer
and 128-byte length, serialization/framing/checksum/migrations, global
runtime initialization, server-side ownership and version equivalence
remain OPEN. No new-game construction or later-release promotion.
