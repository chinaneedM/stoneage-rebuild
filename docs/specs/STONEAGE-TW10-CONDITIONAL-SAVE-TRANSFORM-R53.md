# TW1.0 R53 conditional savedata transform specification

Status: conditional specification and invented-fixture model; actual original input/output and save-field schema remain OPEN.

The historical input is the authenticated R51 numeric instruction/operand/edge inventory, with R52 architectural source qualification. The newly authored numerical model dispatches only the23 observed mnemonics against fabricated, disjoint byte arrays and a fabricated stack. It has no PE loader, binary execution, CALL/native-I/O support, or interface for loading an original save file. The independent reference uses a compact formula. Neither layer evaluates the original savedata payload.

## Conditional domain

Let `N` be an invented input length, `input` its invented byte array and `L=N-1`. Require `2 <= N <= 4000`, the caller's literal-zero seed interpretation, valid32-bit entry-slot geometry/normal return, input count equal to the available invented bytes, and disjoint source/output/length-cell/stack storage with no alias overwrites. The4000 ceiling is this model's bounded domain, not proof of an original read size. The domain keeps the initial divisor `N-1` nonzero and loop-index square in signed32-bit range. Other invalid-count/divide-error/overflow/alias cases remain excluded rather than assumed successful.

The five physical slots from R51 are used only conditionally: input-pointer-shaped, count-shaped, literal-zero seed, destination-pointer-shaped and length-cell-pointer-shaped. This specification does not independently establish their historical ABI or concrete pointer values.

## Zero-seed relation

With zero seed, the selected key index is zero. Let `K=input[0]`. The key byte is omitted from the output, and source index `i=j+1` supplies output index `j` for `0 <= j < L`:

```text
B[j] = (input[j+1] - (((j+1)*(j+1)) mod 7)*K) mod 256
P[j] = (j mod 5 == 0) OR (j mod 2 == 0)
output[j] = B[j] XOR (255 if P[j] else 0)
```

The first source-loop branch using divisor3 is retained in the full instruction partition; it is unreachable only under the stated zero-seed/valid-count conditions. Nonzero seeds retain distinct key-selection, prefix/suffix and signed-remainder predicates. They are exercised as numerical-model alternatives, without admitting a general reference formula.

`MOV [ESI],ECX` after `LEA ECX,[EAX-1]` supports a conditional length-cell store of `N-1`. The caller's57/127 comparison literals would then correspond to model input lengths58/128. These equations do not establish actual read counts, file lengths, record framing, a field schema or version meanings. The word4/5 comparisons and byte writes remain separately identified application operations; fixture bytes4/5 are invented test choices.

## Width and signedness

- Eight-bit one-operand IMUL uses AL and the source byte and writes AX; its low-byte product feeds the byte subtraction. Signed interpretation is preserved in the numerical model. The compact relation uses arithmetic modulo256, which describes that low byte.
- Signed IDIV truncates its quotient towards zero. The numerical model calculates its signed remainder independently of Python's negative-operand `%` behavior and rejects zero divisors/quotient overflow.
- CDQ preserves the EAX low half and supplies its sign extension in EDX under the R52 architecture overlay. Partial AL/AX/DL writes preserve the other parent-register bits; undefined divide/multiply flags cannot drive a modeled branch.

Primary references: [Intel SDM IDIV](https://cdrdv2-public.intel.com/789581/325383-sdm-vol-2abcd.pdf), IDIV instruction table and signed-division description; [Intel SDM IMUL](https://cdrdv2-public.intel.com/835781/325462-sdm-vol-1-2abcd-3abcd-4.pdf), IMUL one-operand-byte and two-operand forms. R52 retains the CDQ reference. These references qualify architecture, not historical StoneAge values.

## Verification and limits

1029 zero-seed fixtures compare every output byte and length between the numerical model and formula, then compare a newly authored inverse fixture generator. They cover all256 key values at lengths2/3/4/8 plus lengths16/58/128/256/4000. Ten additional signed/nonzero-seed fixtures cover alternative numerical paths without admitting a general formula. Hand-calculated vectors, high-bit byte keys, aliases, signed division, overflow, unsupported control flow, step bounds and deliberate wrong-divisor/NOT counterexamples supplement these checks.

The fixture union covers112 of115 observed instructions. Three negative-index fixup instructions0x4723a/0x4723b/0x4723e are retained but excluded from execution coverage: a nonnegative index below4000 makes the sign test at0x47238 bypass them. This bounded verification is not exhaustive over all input buffers or a formal equivalence proof. The inverse generator creates invented test data; it is not evidence for the original write routine.

Open: original argument validity and preservation, non-alias conditions, actual payload contents, application field semantics, schema/checksum/migration, historical writer correspondence, persistence, original server authority and cross-version equivalence.
