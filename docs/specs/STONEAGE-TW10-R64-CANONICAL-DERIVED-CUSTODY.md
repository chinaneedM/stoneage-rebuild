# Permanent R63–R64 derived evidence custody

To prevent GitHub Actions artifact expiry from silently discarding historic work, preserve the two **source-authenticated, nonproprietary** derived JSON reports in Git history. Their source GitHub runs, artifact identities, ZIP SHA256, raw JSON SHA256 and structural-only gates must match the already accepted R63/R64 original-static specifications.

- R63 raw derived: 31,136 bytes, SHA256 `91b650db700cf892a7d8c8b2d36a9d49dbeca139be315856d31d59533056c1bd`.
- R64 raw derived: 7,013 bytes, SHA256 `5253b2ebec4a9bfbdda24764ce8af5e0e67fabf9ba8daf7ad0ce22c7b172e43f`.

Only source-derived JSON is retained, not `sa_3.exe`, `STONEAGE.bin`, original `savedata.dat`, game assets, raw machine-code bytes, or a reconstructed original record. Preserve as Stage A static original evidence. The native Win32 result, count output pointer contents, branch feasibility, ABI alias assumptions, persistence, original format/schema and server authority remain OPEN.

The specialized preservation workflow is intentionally restricted to its own branch, writes exactly the two named files through a non-force push, and never runs original executable code. If the job cannot obtain write permission or a pinned artifact, it must fail closed; never fabricate historical evidence.
