# Taiwan v1.0 — R3 derived-report custody and format guard R1

**Gate only; not historical runtime acceptance.** The independent R3
executable probe is expected to output four \`WORD\` rows for the original
address-word RVAs 0x40065 / 0x400e5 / 0x40116 / 0x402a1.
The parser verifies exact source hashes, the recognized original savedata
string/target, row/key cardinality, bounded numeric fields, candidate
instruction windows and optional imported-file-API counts.

Unexpected rows, raw byte dumps, missing caveats, semantic promotion to
runtime facts, misordered/duplicate sites, malformed operand windows and
incorrect aggregate counts are rejected. Only the numerical aggregate JSON
and carefully verified derived report can be published after the *separate*
original archive and embedded sa_3.exe / savedata.dat SHA256 gates succeed.
Even a structurally perfect report is not evidence of actual code reachability.

Synthetic tests are independent from the archive.org 842 MB download and
have no access to proprietary image, client, or save payload. Original R3
four-site instruction alignment, save/load callers, historical 128-byte
semantics, checksum, and late client equivalence stay OPEN.
