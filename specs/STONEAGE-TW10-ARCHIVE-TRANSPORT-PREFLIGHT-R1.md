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
