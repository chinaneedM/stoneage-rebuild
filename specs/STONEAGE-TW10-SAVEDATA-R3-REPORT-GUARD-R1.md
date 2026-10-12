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


## 2026-10-12 — canonical emitter hardening (R2)

The grammar gate now requires the **entire** exact non-runtime BOUNDARY line,
not merely its initial words. It preserves the producer's row order:
identity and path; each of four ordered word sites followed only by its
numbered candidates and those candidates' API rows; then the total count.
Reordered rows cannot be interpreted as a valid original R3 artifact.

A four-byte target can overlap at most four non-overlapping linear-sweep
instructions, with at most one whole-word instruction. At most 15 candidate
starts fit the x86 maximum instruction length for a single word site.
A candidate's forward 64-byte region cannot generate more than 64 imported
file-API instruction mentions. API names must belong to the pinned original
probe's FILE_APIS allowlist; duplicate DLL/name summary rows and zero counts
are rejected. Tests retain positive zero/one-candidate reports and add
counterexamples for all these bounds.

**Evidence boundary:** this hardening is a report-integrity check on synthetic
metadata. It does not retrieve, hash or execute the old original archive and
cannot close native instruction reachability, savedata encoding or actual IO.
