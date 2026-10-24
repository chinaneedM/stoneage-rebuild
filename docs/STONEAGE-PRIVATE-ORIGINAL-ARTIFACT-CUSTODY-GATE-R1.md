# CLIENT-ORIGINAL-ARTIFACT-PRIVATE-CUSTODY-07 — original-byte retention gate (2026-10-25)

## Target and actual result

**RESTORATION TARGET:** preserve the lawfully obtainable, previously inspected official/mixed client carriers and their full per-version occurrences across sessions before conducting further byte-level reconstruction. This is original-byte custody, not a new game subsystem.

**Current result: BLOCKED_PRIVATE_STORAGE_NOT_PROVISIONED.** At fresh main `9dbc0c5a971d48805bb220330ec5850a923850b5` (tree `bebd37ab83a5c77baf1e74d5c0bbe313795de279`), the original-client SHA chains and derived Git metadata are retained, but the uncompressed proprietary source carriers were obtained on transient source runners, not independently demonstrated as surviving in a durable *private* object store. This session's 30 GiB apparent local free space is an ephemeral execution overlay; the container cannot reach public Git via DNS and is not evidence of permanent private custody. GitHub Actions artifacts are time-limited; the public Git repository is not an appropriate destination for proprietary binaries.

Do not download the 1,145,465,184-byte TW8.5 transport package, the 361,255,180-byte mixed2.5 package, or the 3,983,427-byte ADRN129 patch again merely to rehash them. Previously source-run evidence remains qualified and permanently published *as derived metadata only*. Do not mark original container bytes as stored after a runner exits.

## Required storage gate (must be observed, not guessed)

1. Choose an explicitly authorized private durable target (operator-managed encrypted drive/object storage, for example), verify access rights and proprietary research material policy. Record provider/account-controlled storage ID in **private** custody only, not in public Git.
2. Verify available **persistent** free capacity with safety margin, maximum single-object size, transfer limits and encryption/backups. A merely writable runner disk or temporary CI artifact is insufficient. Existing six-volume transport and extracted REAL of 1,607,321,502 bytes are distinct files; reserve enough for originals, not only derived tables. The 2.5 source remains a *mixed community bridge*, never relabel it as clean official.
3. On a fresh future acquisition when durable storage is ready, freeze source evidence IDs and known original file sizes/digests, copy **without executing installers**. Preserve every source path/version occurrence; content-addressed chunk deduplication never deletes logical occurrences, and a matching file hash does not establish pet/NPC identity or identical server tables.
4. After copying, read every chunk back, validate its SHA-256 and reconstruct the full original hash and byte length; obtain a **separate later-session re-read** and durable provider retention/access attestation before declaring long-term custody. Record immutable source run, original package digest, copies/volume count, archive receipt digest, failure and correction history.
5. Keep all original binaries, art and audio outside public Git; publish only non-sensitive hashes, status and a bounded evidence receipt after access boundaries pass. A copied archive is not proof of a legitimate official build, server-side data or actual gameplay.

## Offline helper delivered

`tools/stoneage_private_archive_custody.py` supplies a **future** private-target copying and readback aid, without networking or automatic client download. It is safe to test with only synthetic data. Its result status is always local copy/readback; it **never** claims provider durability from a single run.

Example input format (paths are illustrative, not claims of present files):

```json
{
  "schema": "stoneage.private_original_archive_input_r1",
  "archive_id": "TW85-REAL-example",
  "files": [{
    "asset_id": "TW85-original-real",
    "source_path": "/private-staging/real_158.bin",
    "expected_bytes": 1607321502,
    "expected_sha256": "e0f9c0d20fd3d9daae0701d8a872c9842e27d3da1be4d449d558c9c76d1c5f5b",
    "occurrences": [{"sample_id": "TW85", "relative_path": "real_158.bin"}]
  }]
}
```

```sh
python -m tools.stoneage_private_archive_custody archive --manifest private-input.json --root /durable-private-archive --private-target-confirmed --chunk-bytes 8388608
python -m tools.stoneage_private_archive_custody verify --receipt /durable-private-archive/receipts/TW85-REAL-example.json --root /durable-private-archive
python -m unittest tests.test_stoneage_private_archive_custody -v
```

The `--private-target-confirmed` flag asserts the caller has independently checked its target; no code can infer provider retention from this flag. Test-only bytes cannot demonstrate genuine carrier source custody, original pixel decoding or source origin. Empty/wrong hash, overwrite, symlink, traversal, duplicate ID, chunk corruption and single-object-limit scenarios have negative guards.

## Exit decision and next substantive restoration item

- **CUSTODY-07:** PAUSED_EXTERNAL_PRIVATE_STORAGE_DEPENDENCY, not COMPLETE; exact trigger to reopen: a private durable target with observable capacity, max object size, legal permission, and later re-read workflow.
- **Next active source domain:** `PET-SPECIES-SAME-BUILD-PRIMARY-MASTER-08`: look for one *authenticated* version-matched official pet roster/master ID with an independently verifiable name-to-graphic join to an actual original bitmap/SPR path. If no named real source is available, record the bounded missing carrier and rotate to NPC/quest source; do not conflate 416,220 resource records with species. No inferred map place names, creature stats, event/base quest mixing, or new-game production.
- Evidence state remains Stage A seven PARTIAL + two OPEN; Stage B and public wiki GATED; client-local savedata R79 PAUSED; overall completion `null`.

This finite gate satisfies the protocol's “no repeated original bytes without durable retention” stop condition and returns research to material gameplay coverage rather than expanding redundant low-level helpers.
