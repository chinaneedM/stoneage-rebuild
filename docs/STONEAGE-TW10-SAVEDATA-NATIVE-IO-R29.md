# TW1.0 R29 — conditional scalar and shared-address syntax

Exact Taiwan Waei/JSS1.0 original runtime/savedata, static only. Revalidate
exact R28 original JSON SHA256296e5754a3eebafc6360cc45000ba73b6bcf1cc0a5d0ee439aa291eb45e0d645
and strict gate. Use original R28 CALL-supported contexts0x4a8dc/0x4c5b4.

Inspect five unmodeled register definition candidates0x4a8f9/0x4a8fc,
0x4c5d3/0x4c5e0/0x4c617 and their input provenance. A named scalar model
requires exact full-width register destination and supported operand shape;
partial widths, memory destinations and variable shifts stay unqualified.
Conditional scalar results are modular32-bit mathematics only. Actual inputs,
results, flags, branches, index ranges and API roles remain unknown. The
synthetic evaluator never receives original state or runs historical programs.
The general reaching-definition engine remains conservative at unmodeled writes;
new symbolic models are a separate evidence layer.

Architectural reference: Intel official SDM Volume2B, SAL/SAR/SHL/SHR,
printed pages4-584/4-585:32-bit counts use five low bits; SAR sign-fills and
rounds toward negative infinity, SHR zero-fills. No flag model is applied.
https://www.intel.com/content/dam/www/public/us/en/documents/manuals/64-ia-32-architectures-software-developer-vol-2b-manual.pdf

Recheck shared LEA displacement0x1721760+4*EAX syntax and inventory exact
immediate/displacement operands across raw .text, capped32 samples. Indexed
and indirect alias completeness, actual table contents/initialization, effective
addresses and shared file-handle/CRT owner are not inferred. Only bounded
metadata leaves CI; originals are nonexecuting and purged.
READY pending original source and independent exact JSON custody.
