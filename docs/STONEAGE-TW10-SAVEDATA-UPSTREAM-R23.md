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

## 2026-10-13 independent original acceptance supersedes READY status above

Original source38387323403 at b53071fd45fab017704562d17d75bc59563ef01a,
artifact11807077162 and independent exact-report custody38387607870 PASS.
Final synthetic+R22 regression58 tests38387607546 PASS. See the R23 receipt.

Three imported CALLs lead structurally to EAX global stores while every EAX
source remains UNKNOWN_CALL. HeapAlloc reads candidate global0x172187c;
HeapReAlloc reads both0x1721878 and0x172187c. The last four HeapReAlloc
PUSH inputs correspond conditionally to pre-CALL ESP+0/+4/+8/+12:
global0x172187c, EDI, global0x1721878, EAX. No actual argument roles inferred.
Create/Alloc suffixes stop at unqualified stack/memory/unmodeled barriers;
ReAlloc suffix stops at a control transfer. This is conditional original static
acceptance only; all native-save and runtime heap-owner gaps remain OPEN.

NEXT R24: stopping prefixes/caller entry and stack uncertainty, EAX definition
at0x4a0b3 and branch predicates, with no Windows ABI or runtime promotion.
