# TW1.0 R55 conditional historical writer/read relation

Status: conditional specification from accepted numeric metadata, verified on invented arrays. Original payloads, actual native writes and historical schema remain OPEN.

R54 supplies all129 instruction shapes and143 bounded edges for historical writer candidate0x47010; R51/R52 supply the read processor0x47160 and architecture/source qualification. R53 supplies the previously accepted read model. R55 loads no original executable or save and performs no native CALL. The new numerical model dispatches the26 observed writer mnemonics on fabricated disjoint arrays and a fabricated stack; its compact reference is separately written. R53's read model is unchanged.

## Domain and slots

Let `N` equal the available invented input bytes. The normal reference requires `1 <= N <= 3999`, zero seed, capacity `C` with `N+1 <= C <= 4000`, valid conditional32-bit entry-slot/near-return geometry, mutable input and disjoint input/output/length/stack regions. These ceilings are model bounds, not actual historical I/O size evidence. They avoid signed loop-square overflow and the normal branch's zero divisor. Negative counts/capacities, incompatible aliases and failed memory access remain outside the reference.

Conditional entry slots are +4 input-pointer-shaped, +8 count-shaped, +12 seed-shaped, +16 output-pointer-shaped, +20 output-count-pointer-shaped and +24 capacity-shaped. They correspond to the R54 six physical pushes. Actual original ABI/addresses/register validity remain unknown. The model rejects fabricated argument mutation, count mismatch and input/output or length-cell alias substitution before dispatch.

## Zero-seed relation

For the original invented input `A`, define:

```text
K = sum(A[j], j=0..N-1) mod 256
P(j) = (j mod 5 == 0) OR (j mod 2 == 0)
T[j] = A[j] XOR (255 if P(j) else 0)
W[0] = K
W[j+1] = (T[j] + (((j+1)*(j+1)) mod 7)*K) mod 256
output count = N+1
```

The byte accumulator consumes each input byte before its optional NOT. The input is changed in place to `T`; output is written separately. The key is not chosen arbitrarily. The R53 invented inverse generator matches this conditional writer only when its supplied key equals `sum(A) mod256`.

The R53 read relation subtracts the matching low-byte product from `W[j+1]`, then applies the same byte NOT predicate. Consequently, under the stated domain, its output is `A`. This mathematical cancellation is checked separately against both numerical instruction-shape models on invented data. It is not evidence that any original file was read, transformed or persisted successfully.

One hand vector is `A=[1,2,3]`, `K=6`, `T=[254,2,252]`, `W=[6,4,26,8]`. For every single byte `v`, the invented result is `[v,255]`. These vectors distinguish accumulation before NOT, low-byte wraparound and index/divisor mistakes.

The application's physical count127, seed0 and capacity4000 would satisfy the normal capacity inequality and give modeled128 output bytes. The read model then gives127 bytes. The actual REP copy, stack-helper allocation, opaque open/write/close effects and argument preservation are separate pending obligations. This is not a proven128-byte native write or record schema.

## Capacity and error paths

For `0 <= C < N+1`, the modeled function copies `A[:C]` directly, stores count `C` and leaves the input unchanged. It does not perform the normal transform, so the normal inverse statement does not apply. At `N=0,C=0`, this branch returns empty. At `N=0,C>=1`, the normal path reaches division by zero. The reference reports that error rather than calling it a successful empty encoding.

The local accumulator byte is at conditional entry ESP-1, overlapping the high byte of the first saved ECX word. The model therefore does not require initial ECX preservation. EBX/EBP/ESI/EDI and net near-return ESP are checked. The entry+16 output-pointer slot is overwritten at0x470f5; later memory reads use its current modeled value, not a cached initial pointer.

## Architecture and verification

R55 reuses R53's qualified signed32-bit division, partial-register handling, signed byte IMUL/AX behavior, and width-sensitive arithmetic helpers. It adds ADD, signed JG and direct JMP dispatch. JG uses `!ZF && SF==OF`; ADD computes width-sensitive signed-overflow/sign/zero flags. Undefined divide/multiply flags remain unavailable for a branch. R52/R53's recorded Intel SDM references remain the architecture basis; they do not provide StoneAge runtime values.

- 1292 zero-seed invented fixtures include all256 derived keys at input lengths1/2/3/7/127, additional lengths57/255/3999 and capacity-boundary cases. Seven fixtures use the capacity fallback. Normal outputs, lengths and mutated inputs agree with the independent formula; normal outputs also roundtrip through the R53 numerical read model and compact read relation.
- Ten additional signed/nonzero-seed fixtures roundtrip through both numerical models, retaining generic prefix/divisor3 and suffix/divisor7 paths. A general nonzero-seed reference formula is not admitted.
- Writer/read zero-seed fixtures total3933134 numerical steps; maximum writer fixture164817 steps. The writer fixture union covers126 of129 shapes. The three negative-index repairs0x470a6/0x470a7/0x470aa are retained but skipped because the modeled loop index is nonnegative and below3999. Full inventory is not full execution coverage or formal exhaustive equivalence.
- Forty-six controls cover hand vectors, all single-byte values, high-bit/wraparound keys, mutation and scratch overlap, capacity/zero-count branches, signed JG boundary pairs, argument alias/count rejection, unsupported calls, bounds, custody/report corruption and deliberately incorrect key/divisor/NOT alternatives.

The presence of a key equal to a byte sum does not establish a historical checksum-validation mechanism. The R53 read specification does not assert a comparison of that sum with a decoded payload. Field meanings, tag/version semantics, normalization/migration, actual native persistence, original server authority and cross-version equivalence remain OPEN. All Stage A system-family gates remain unchanged.
