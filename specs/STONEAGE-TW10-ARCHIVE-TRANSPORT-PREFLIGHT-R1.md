# Taiwan v1.0: bounded source-transport preflight R1

**Classification:** DESIGN/tooling to unblock original-client acquisition.
The first R3 archival-download action 38209109437 was cancelled after
35 minutes without archiving a verified original file; R3 original instruction
interpretation therefore remains **OPEN**.

The preflight tests *transport only*:
1. Item metadata endpoint \`https://archive.org/metadata/stoneage_tw_2000_win\`,
   searching for \`CD_DIC.rar\` by exact name and comparing catalog MD5/SHA1
   to the earlier accepted archive identity.
2. A HEAD request to the canonical download path.
3. A GET with \`Range: bytes=0-4095\` to the canonical download path.
4. If the catalog exposes a valid Archive-owned hostname, a similarly capped
   sample to the dynamic server. Hosts are strictly validated and never
   used as permanent citations or evidence identifiers.

Every operation has a 12-second socket timeout; GET reads at most its
configured cap plus one byte and closes even if the server ignores Range.
Only metadata flags, HTTP statuses, timing, declared content length and
range behavior are published. Source bodies, original files, binary bytes,
redirect tokens, archives and game assets are never written to Git.

**Gate:** an HTTP response or matching catalog checksum is a transport or
catalog signal, not independent hash verification of acquired original bytes.
Successful preflight Actions must not be mislabeled as successful R3 original
executable analysis. A future full original gate must read a complete original
artifact and verify exact hashes before reporting instruction candidates.

## 2026-10-12 verified first preflight (transport-only)

Branch Action 38214333386 passed 10 tests. Its original metadata GET returned
HTTP 200 with an 842125501-byte file entry and catalog MD5/SHA1 matching the
accepted original reference. Canonical HEAD and range GET both returned HTTP
500; the first per-storage test returned HTTP 404 because it incorrectly used
the canonical `/download/ITEM/FILE` route on an `iaNNNN...us.archive.org`
storage host. R1 revision now validates the catalog-provided `dir` path
(`/N/items/stoneage_tw_2000_win`) and uses the proper storage-file route;
only a fresh result can determine whether that succeeds. Neither observation
confirms a complete original artifact or recovered instruction semantics.
