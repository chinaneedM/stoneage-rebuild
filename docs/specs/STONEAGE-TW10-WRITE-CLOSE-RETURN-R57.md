# TW1.0 R57 write/close wrapper return syntax

Status: authenticated nonexecuting original static inventories and conditional source/control specification. Actual native persistence remains OPEN.

The R56 missing-inventory audit justified one authenticated original retrieval. R57 rederives exact R54 original metadata, then expands savedata CALL0x40090->0x48bbc and CALL0x400ac->0x4856c. No original program runs and no original save payload is evaluated. Only numeric instruction/operand/graph/source metadata is published; transient original media is purged.

## Complete bounded inventory

| Context | Nodes | Edges | Returns | Predicates | Memory-write shapes |
|---|---:|---:|---|---:|---:|
| Write wrapper0x48bbc |106|119|0x48cb1|14|12|
| Close wrapper0x4856c |35|38|0x485c1|4|2|

Each fits768 bytes/256 nodes with no frontier or node cap. The write graph,106 original stack effects and every retained R42 operand shape match exactly. Direct caller/target boundaries and edges are supported by the original entrygraph. This is a complete bounded inventory, not proof of actual path feasibility, function ABI or successful native calls.

Forward fixed-point register propagation and independently implemented reverse predecessor search agree on14 write-return queries and6 close-return queries. Both use raw decoder observations, with no CDQ overlay. General-register source closure does not close memory contents, stack aliases or opaque callee effects; every CALL kills register value certainty. The14/6 focused groups have no pending-query cap.

## Write return families

The write prologue PUSH EBP/MOV EBP,ESP gives a conditional frame coordinate EBP=entry ESP-4. Under valid preserved frame/stack/non-alias premises, initial frame operands correspond to:

| Initial slot | Conditional role |
|---|---|
| Entry+4 | Buffer-shaped |
| Entry+8 | Element-size-shaped |
| Entry+12 | Element-count-shaped |
| Entry+16 | Object-shaped; its frame slot is later overwritten with a block quantity |

MOV/IMUL0x48bc3/0x48bc6 supply a low32-bit product stored at EBP-4. This multiplication is syntax and a conditional expression; actual original counts/product are not evaluated.

The single RET has three direct EAX definition candidates:

- XOR EAX,EAX0x48bd9 on the zero-product branch.
- MOV EAX,[EBP+16]0x48caa on normal loop completion: the original count-shaped slot, assuming it remains valid and unchanged.
- DIV dword[EBP+12]0x48cc1 after SUB EAX,EBX0x48cbd and XOR EDX,EDX0x48cbf. The conditional unsigned quotient is `(EAX_snapshot - remaining_EBX) mod2^32 / element_size`, provided the divisor is valid/nonzero and division succeeds. EAX_snapshot can come from the saved product load0x48cb6 or MOV EAX,EDI0x48cbb. Do not collapse EDI to a constant total without proving its value across nested calls/paths.

The native-context CALL0x48c5e->0x4c5b4 is followed by CMP EAX,-1 at0x48c66. A separate unsigned CMP EAX,EDI/JB at0x48c70/0x48c72 checks a short-return-shaped case. These routes reach OR dword[ESI+12],0x20 at0x48cb2 and partial-quotient syntax. The helper0x48c38->0x4a657 and byte helper0x48c81->0x4ae15 have separate return predicates. Their real error conventions, memory effects and preservation remain unknown.

## Full count does not imply a direct native write

A recorded structural path goes through CALL0x48c1a->0x4aae0, then reaches normal count load0x48caa and RET0x48cb1 while excluding the direct native-context call0x48c5e. The preceding memory-copy-shaped inputs and object-field updates support a buffering hypothesis. The path assumes nested calls return and is not an executed original trace.

Consequently, the caller can only be said to receive a count-shaped return under explicit conditions. A full count alone does not prove that the direct native write was called or that bytes reached disk. R56's size1/count128 model equation remains conditional; an error/short path quotient would correspond to progress only under its frame/value/nonzero-divisor premises.

## Close wrapper

The close prefix obtains an input-pointer-shaped value from conditional entry+4 into ESI. It loads dword[ESI+12], tests AL masks0x40 and0x83, and initializes EDI with all-one bits at0x48572. The RET has direct EAX source candidates OR EAX,-1 at0x4857c and MOV EAX,EDI0x485b9.

CALL0x48586->0x4a657 shares its target with the write wrapper's helper. MOV EDI,EAX0x4858c copies that helper-return-shaped value. Later opaque calls0x4858e->0x4a5f1,0x48596->0x4a53e and optional0x485af->0x4853d prevent unqualified register-value propagation. TEST EAX,EAX0x4859e/JGE0x485a0 selects a negative-result-shaped branch that ORs EDI,-1 at0x485a2. An optional object+28 path is followed by clearing that field; object flags at+12 are cleared at0x485bb before return.

These are exact syntax/control observations. They do not prove original FILE/descriptor ownership, flushing/closing semantics or a particular success/error code. Conditional propagation of the first helper's result through EDI requires separate preservation/alias evidence.

The outer savedata application ignores the close-return-shaped EAX and overwrites it with literal1. Its unsigned write-count test therefore cannot certify successful close/flush/persistence. No actual resource leak or historical bug is inferred from the bounded caller's short-return route without a close candidate.

Next: recover the shared0x4a657 and close-path0x4a53e obligations only as needed, using existing metadata first. Do not expand unrelated CRT/allocator ownership. Original payload/fields/tags, schema/checksum/migration/persistence, original server authority and cross-version equivalence remain OPEN; Stage A system-family gates are unchanged.
