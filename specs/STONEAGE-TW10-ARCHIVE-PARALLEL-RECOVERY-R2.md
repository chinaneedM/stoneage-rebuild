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
