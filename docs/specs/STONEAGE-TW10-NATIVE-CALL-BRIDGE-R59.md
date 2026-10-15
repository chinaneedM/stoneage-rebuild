# TW1.0 R59 — Existing-metadata native-call bridge preflight

Status: **PREFLIGHT / conditional static syntax**, not native persistence acceptance.

This milestone cross-links only immutable pre-existing R28 and R58 original-derived
numeric reports. The R28 original WriteFile candidate root `0x4c5b4` has a
bounded 139-node / 156-edge graph, no graph frontier, and two
memory-indirect `WriteFile` import identities at `0x4c68c` and `0x4c6f1`
(both IAT `0x520a4`). R28 separately records write-wrapper
`0x48c5e -> 0x4c5b4`. R58 records shared write/close helper
`0x4a683 -> 0x4c5b4`. These are two syntactic caller routes into
the same bounded native-context candidate, **not** proven executed paths.

The R58 close-path helper `0x4a53e` contains memory-indirect import-slot
identities `0x4a5a3 -> CloseHandle` (IAT `0x520a8`) and
`0x4a5ad -> GetLastError` (IAT `0x5208c`). This is stronger than
an anonymous indirect-call observation but does not prove any OS API ran,
which handle was supplied, actual call returns, ownership, close/flush or disk
persistence. R28 reports the second WriteFile site was not reached in its
earlier prior graph despite being in the current bounded graph; do not
silently equalize this historical coverage distinction.

`tools/stoneage_tw10_savedata_bridge_r59.py` rechecks the exact original
Git blob identities, R58 SHA256, cross-report source identities, R57 wrapper
bridges, direct callee target, imported-name/IAT pairs, scoped graph closure
and every essential non-promotion flag. Its synthetic adversarial tests reject
incorrect target/slot identities, unresolved graph frontiers and native-success
promotions. All output is derived JSON, no original client/download/execution.

**Highest NEXT (R59 follow-on)** after independent CI acceptance: trace specific
`0x4c5b4` native-context post-call return/count paths and close helper
`0x4a53e` branch/indirect-callee result barriers using existing pinned
evidence first; recover authenticated originals only for a precise missing
instruction scope. Preserve conditional buffer-count returns versus actual
savedata write/flush/close; payload, version/schema/checksum/migration,
original server authority and cross-version equivalence remain OPEN.
