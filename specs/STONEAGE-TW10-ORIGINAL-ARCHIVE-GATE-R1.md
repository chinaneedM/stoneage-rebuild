# Taiwan v1.0 original archive recovery R1 — bounded native static gate

**Status:** DESIGN until independent Actions verification; full original binary
instructions remain OPEN.

2026-10-12 transient runner observations: Archive.org catalog metadata responds
HTTP 200 with exact CD_DIC.rar length **842125501** and MD5/SHA1 pins matching
historical records. The canonical \`/download/\` HEAD/range endpoints returned
HTTP 500, while a catalog-validated \`/N/items/stoneage_tw_2000_win/CD_DIC.rar\`
path on an Archive-owned storage host returned HTTP **206**, exactly
\`Content-Range: bytes 0-4095/842125501\`, in 294 ms. Branch Actions
38214333386 and 38214519509 both SUCCESS (10/13 synthetic tests), plus
independent main Actions 38214719068. No original artifact SHA was checked
in these preflight jobs.

This stage downloads archive bytes ONLY transiently on GitHub Actions into
/tmp/CD_DIC.rar, using a metadata-pinned, allowlisted host and directory.
Every request must return 206 and exact Content-Range. Resume by checked byte
offset for truncated chunks and enforce a 540-second deadline, at most three
consecutive transport errors. MD5 **b37a4a47f4eb608cac67e4ddf7a1621a**
and SHA1 **b8cf92720b6ec8b3f46ea2e9bfcda986d21e7ded** must both match
the entire 842125501-byte archive before extracting the 523449360-byte disc
image. Then the existing R3 static probe must verify original sa_3.exe and
data/savedata.dat SHA256 before any four-word instruction output is accepted.
Run is limited to 15 minutes. On all outcomes, proprietary files are deleted.
Only derived numerical/code-reference evidence may be uploaded.

Possible exact x86 instruction starts do **not** establish reachability,
actual native read/write/save/load, file layout, checksum, or late Wayi codec
equivalence. Any failed retrieval is an acquisition error, not evidence of
different original client semantics.
