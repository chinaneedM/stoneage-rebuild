# Taiwan Waei/JSS v1.0 — 128-byte savedata zero-run geometry

**Status: FACT (arithmetic over previously accepted derived metadata); OPEN (historical format semantics).**

Source custody: \`research/recovered/STONEAGE-TW10-SAVEDATA-R1.txt\`,
generated from the accepted clean Taiwan v1.0 retail disc. File identity is
pinned by SHA256 \`5b26f54a9723cd2c5275f964457094fdf1fc33ca086cdaf55bb5350dfb04f3f9\`.
This note and companion tool never read the actual 128-byte file, disc, client,
or private binary. They operate exclusively on the committed aggregate report.

The 128-byte source has seven recorded one-byte zero runs, starting at
\`14, 28, 42, 70, 84, 98, 112\`. Ordered differences are
\`14, 14, 28, 14, 14, 14\`. Both the greatest common divisor of the
positive starts and the gcd of the consecutive differences equal **14**.
Within [1,127], multiples of 14 unmarked as zero-run starts are **56 and
126**. This is arithmetically reproducible, not an assertion that those bytes
hold any particular value beyond the known aggregate zero/nonzero layout.

**HYPOTHESIS ONLY:** 14-byte alignment could indicate a regularly structured
local state field or delimiter arrangement. It does **not** establish a
14-byte record, a count of records, text encoding, NUL delimiter meaning,
offset-to-setting map, checksum, or read/write path. In particular, the
missing zero at offset 56 breaks a naive uninterrupted 14-byte delimiter
model, and file size 128 is not a multiple of 14. Multiple incompatible
formats could produce identical zero-run positions.

Acceptance gate: unit tests pin the report's known digest, size, bounds and
counts; the derived calculation can be replayed without downloading old
copyrighted media. Historical semantics require separate inspection of the
exact Taiwan 1.0 executable's call paths (four address-word R3 probe)
and independent byte/behavioral evidence. Do not back-port late Wayi
settings codec or migration effects into v1.0. Full framing/checksum
and native original-server pairing remain OPEN.
