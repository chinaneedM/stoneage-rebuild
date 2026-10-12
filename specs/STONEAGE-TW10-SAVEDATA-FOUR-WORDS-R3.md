# Taiwan v1.0 savedata four address-word instruction probe — R3

**Status:** DESIGN / verification gate pending; not historical behavior acceptance.

The accepted clean Taiwan Waei/JSS v1.0 retail disc yields sa_3.exe
(SHA256 cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a)
and data/savedata.dat (128 bytes; SHA256
5b26f54a9723cd2c5275f964457094fdf1fc33ca086cdaf55bb5350dfb04f3f9).
The string data\savedata.dat occurs at RVA 0x63634. Existing R2 metadata
records four matching address words at RVAs 0x40065, 0x400e5, 0x40116,
and 0x402a1 in .text with no linear-sweep direct string or slot xref.

R3 independently checks exact original hashes and all four raw-backed
little-endian address words. A bounded x86-32 decoder tries possible
instruction starts within the 15-byte x86 maximum length before each word;
a candidate must cover all four bytes *in one decoded instruction* and
resolve to the exact string VA as an immediate or absolute memory operand.
It reports candidate instruction RVA, size, mnemonic, linear-sweep alignment,
linear-sweep direct incoming edges, and at most 64 bytes of candidate-local
file-API scan, never raw payload or operand disassembly.

These are **static alignment possibilities**, not verified executed instruction
boundaries, control-flow entry, persistence semantics, string use, or file IO.
Especially, zero direct incoming edges does not rule out fallthrough or
indirect callers; a forward lexical API scan does not prove reachable calls.
R3 cannot infer that late Wayi 2006 settings codec/checksum/migration logic
existed in Taiwan v1.0. A historical runtime claim still requires real
control-flow and independent source/behavior validation.

Next if all four word sites validate: reconcile alternative starts against
actual function boundaries/branch reachability, inspect string-table
registration vs read/write APIs, and establish 128-byte format boundaries.
Cross-version framing/checksum, authentic matching server and native
paired execution stay separate admission gates. Proprietary binaries,
savedata bytes, disassembly operand strings and game assets are excluded
from publication.

## R3 gate repair — 2026-10-12

The first R3 branch job #38209109437 ended **cancelled**, not passed:
eight synthetic tests were successful, but its single download of the
Internet Archive \`CD_DIC.rar\` occupied the full 35-minute job deadline
(05:42:29–06:17:36 UTC) and its four-word executable probe never ran.
This is a documented **acquisition timeout**, not evidence for or against
the original four x86 instruction contexts.

R3's workflow is split into always-on, low-cost metadata/synthetic CI and
an explicitly opt-in \`workflow_dispatch\` native-artifact gate. The latter
uses connection, total-duration and stalled-transfer limits and refuses to
analyze anything unless the existing archive MD5/SHA1 and the extracted
binary/save SHA256 pins pass. Neither CI success for the synthetic stage nor
the preexisting R1/R2 metadata promotes possible alignments to executable
control-flow FACT. The original gate must produce a report and be evaluated
independently before R3 runtime acceptance.
