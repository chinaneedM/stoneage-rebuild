# TW1.0 R23 — original heap-call/global candidate links

Scope: Taiwan Waei/JSS 1.0 exact accepted executable/savedata identities.
R22 original gate is re-derived and strictly validated before R23 analysis.
No historical executable is run; only bounded derivative JSON is published.

R23 connects each exact imported HeapCreate/HeapAlloc/HeapReAlloc CALL to
its candidate EAX global-store source, identifies syntactic global PUSH
operands, and bounds a straight decoded PUSH suffix relative to ESP immediately
before CALL. No Windows argument signature is applied. Branches, opaque calls,
ESP changes, partial-width pushes and unqualified memory stores stop the suffix.
Function entries, all incoming edges, actual path feasibility and stack values
remain unknown. Matching global addresses do not prove common heap identity,
allocation success, object ownership or return values. Original alias cycles
remain unsummarized under the accepted R22 boundary.

Status: TOOLING/SYNTHETIC READY; original specimen derivation and independent
immutable-run/artifact/exact-report custody required before FACT acceptance.
Native filename/handle/buffer linkage, serialization, framing/checksum,
migrations and persistence remain OPEN. Restoration-first gate remains binding.
