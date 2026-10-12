# Taiwan 1.0 R7 conditional filename argument prefixes

Input identity and physical stack seed are independently rechecked from the
four original R6 push/CALL pairs. At common callee entry 0x487ba, the direct
CALL's return word is on the stack and the filename label lies at ESP+4.

R7 tracks exact four-byte copies among full registers, ESP/EBP-relative cells,
LEA stack addresses, PUSH/POP and simple frame arithmetic. Partial register
writes remove the full-register label; overlapping stores remove affected
cells. Unknown aliases/stack effects stop the path. Unsupported/global reads
produce unknown values rather than guessed filename provenance. Unmodeled
memory instructions stop, except read-only CMP/TEST; Capstone x87 store access
bits can be incorrect and are never alone treated as a non-write proof. Imported
transfers require an absolute, unsegmented, four-byte IAT memory operand.

Direct calls enter their callee with a fresh return word and the current
physical stack. The caller continuation ALWAYS stops: no callee-saved ABI,
stack cleanup, return-value or memory effects are assumed. Direct conditional
branches enumerate separate states without feasibility proof or merging one
path's label into another. Limits: 2048 states, depth6,64 transfer events,
16 physical stack slots per event. Higher stack slots may include existing
parent-frame cells; they are NOT an inferred argument count or function ABI.
Import tail JMP snapshots skip the existing return word before labeling slot0.

A CreateFileA slot0 candidate denotes a conditional, prefix-local static
filename label; complete runtime or interprocedural correctness is not
admitted. Stopped helper calls require independently verified summaries before
continuing to stream/handle ownership and read/write buffer-length linkage.
A missing API candidate after a stopped CALL is not a global absence proof.

Only offsets, selected provenance labels and bounded counters are emitted.
No original bytes, operand/disassembly listings, assets or real IO are emitted
or executed. The original archive is transiently retrieved only by the scoped
branch workflow, with catalog/hash/extraction gates and mandatory cleanup.
Synthetic CI does not retrieve original media.
