# TW1.0 savedata R6: first-transfer stack and cross-callee surfaces

R5's zero API occurrences were local to a 2048-RVA region. R6 follows the
first direct transfer after each of the four pinned filename pushes across
raw .text functions without that radius, with depth 4, 4096 instruction/depth
states and 64 unique API sites. A CALL's fallthrough assumes it returns;
RET ends a callee path. Branch conditions and unresolved indirect transfers
remain gaps. API events are lexical static candidates, not filename/handle
ownership, buffer provenance, read/write sizes, native execution or absence
proof. Depth and node truncation are reported independently.

The pre-transfer stack tracker reports only a physical four-byte stack slot
before the first CALL. Extra pushes/pops of registers are accounted for;
16-bit stack operations, arbitrary ESP writes and any explicit memory write
invalidate the slot. It stops on branches, returns, traps or 64 instruction
starts. A slot is not an ABI parameter index or interprocedural taint proof.
Register-indirect calls remain unresolved; no guessed targets are followed.
Only absolute memory-indirect CALL/JMP operands identify IAT imports; a direct
immediate target equal to an IAT address is not counted as an imported call.

Original-data mode independently checks sa_3.exe and savedata.dat SHA256,
all four address words, the accepted R4 graph totals and candidate membership.
It emits offsets, bounded counts and file-API names only. It never emits
original executable bytes, operand listings, assets or credentials. The
branch-only original gate retrieves the full archive transiently with existing
catalog/hash/deadline controls, removes it even on failure, and uploads only
derived JSON. Main/push synthetic CI does not download original media.

All five native/format/publication admission flags remain false. Separate
handle-to-buffer-to-size tracking, wrapper ABI recovery and authentic runtime
observations are required before historical savedata IO can be closed.
