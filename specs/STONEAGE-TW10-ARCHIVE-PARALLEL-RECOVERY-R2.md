# Taiwan 1.0 — original-archive parallel range recovery R2

**Design, not native executable acceptance.** Baseline TW1.0 savedata
four-address-word instruction probe remains OPEN until complete original
archive hash verification and exact original executable/data SHA256 succeed.

Branch full-archive download Actions 38215067915 ended FAILURE after the
540-second deadline. It retrieved 134217728 bytes (128 MiB) of the
842125501-byte original, without any observed per-range Content-Range errors,
but single-thread sustained throughput was insufficient. No original
binary/content checksum was completed, and the temporary partial was deleted.
The job's 10 original downloader tests passed; this was not a binary semantic
failure. Old unbounded download and this bounded serial attempt do not justify
repeating the same serial acquisition.

This R2 tool downloads non-overlapping, independently validated HTTP byte
ranges concurrently using at most 12 workers of 8 MiB per range by default.
Accept only **206** with exact expected Content-Range and archive-owned HTTPS
host (no arbitrary cross-host redirect). A worker writes via positional I/O
only inside its assigned region. The whole transient archive MUST match both
catalog-pinned MD5 and SHA1 in a sequential re-read; a missing/repeated/altered
piece, truncated response, bad redirect, invalid source identity, or deadline
failure deletes the file and aborts the R3 native probe.

The CI job has a maximum of 15 minutes; download has a 540-second global
deadline, connection read timeout and limited retries. The original ISO and
binary may only exist transiently in Actions runtime. Neither raw file
segments, compressed image, binaries, scripts from the old client, sprites,
nor raw reverse-engineered disassembly will be uploaded. Only derived
statistics, RVAs, bounded classifications, checksums and accepted identity
claims may enter Git.

Potential fallback if parallel transport remains inadequate: independently
verify a clean directly hosted sa_3.exe/save pair or obtain byte-addressable
publisher-preserved client media. Never weaken hash pins or conflate later
Wayi settings with Taiwan 1.0 to make a gate pass.


## R2 serial/parallel bounded throughput postmortem — 2026-10-12

Branch run 38216336611 (SHA d34e631b75bbb9ad77d44dc0ad00ac165a43f95b)
completed FAILURE at its 540-second original-archive deadline, after
twenty synthetic/unit tests PASS and non-overlapping ranged fetches completed
469762048 bytes (448 MiB) of the 842125501-byte archive. There was no
full-file MD5/SHA1, original-client SHA256, extracted disc or R3 instruction
report; temporary partial bytes were purged. This is a **throughput/deadline**
failure, not an observed original client or historical rules mismatch.

Estimated job throughput (completed segments / ~540s) is ~0.83 MiB/s,
suggesting 800+MiB requires ~17 minutes at that rate, not nine minutes.
The follow-up is deliberately bounded at 25 minutes for complete acquisition
and 33 minutes for the entire job, with 16 independent 8MiB range workers,
limited per-range retries, HTTPS Archive-only source/redirect constraints,
MD5+SHA1 full-archive verification, exact embedded file SHA256 checks, no
binary publication, and mandatory deletion. A bounded retry is now supported
by measured transport progress; repeating short single-threaded attempts is
not. Successful transfer still does not prove actual native runtime paths.
