# TW1.0 R33 — Secondary CALL identity and two conditional-branch ZF sources

**State:** READY for pinned original static probe and independent custody, not yet
historically accepted. This is within restoration Stage A.

## Evidence target

- Revalidate exact R32 original JSON SHA256
  `24849b161be51b4fbf50fa7fe2c2bb48b6e79a6a83fb012f33ddd961f6336c9c`
  by rederiving it from the same pinned TW1.0 retail image and applying R32's
  strict guard before any new conclusion.
- Inspect the additional original CALL at RVA `0x4ed19` independently of
  CreateFileA `0x4ed01` and GetLastError `0x4ed1f`. Imported DLL/name/IAT
  association is permitted only from the verified PE import table and an exact
  CALL instruction; actual invocation, return value and callee side effects
  are not established.
- For conditional JE `0x4ed0b` and JNE `0x4ed16`, recover all bounded,
  predecessor-graph may-def ZF sources where a ZF-writing instruction or
  unknown returning CALL stops backward traversal. Preserve uncertainty over
  unknown callee effects, unreachable/indirect paths and branch joins.
- Emit only operand geometry, source register references, import identity and
  bounded control-flow provenance, not original code bytes/strings/resources.
  A test/cmp flag-writing source does not prove any original operand's value
  or whether JE/JNE was taken.
- Do not infer the later helper `0x4c953` gets a CreateFileA handle, or
  that any GetLastError/CALL route implements persistent native saving.

## Reproducibility and limits

`tools/stoneage_tw10_savedata_native_io_r33.py` uses the inherited pinned
client/archive/runtime/savedata SHA checks and exact R32 derivative equality.
Parent graph is limited to 768 bytes / 256 nodes with CALL fallthrough modeled
as a structural-only assumption. Per branch predecessor walk is capped at 256
nodes, 24 source samples, and 32 initial register-source queries total, then
reuses the R28 64-query/two-dependency-level bound.

`tools/stoneage_tw10_savedata_native_io_r33_guard.py` bans promotion of
branch values, actual calls, API results, successful handles, native file
persistence, ABI/alias ownership or executable source. Synthetic and negative
controls in `tests/test_stoneage_tw10_savedata_native_io_r33.py`.

Only JSON-derived metadata <=80,000 bytes may leave Actions; original disc
and executables are downloaded temporarily without execution and removed
unconditionally.

## Acceptance requirements

1. R33 + inherited R32 synthetic and tamper tests PASS.
2. Pinned-original R33 source/guard PASS, transient archive purged, JSON
   artifact identity and full run/head captured.
3. A distinct independent Actions workflow verifies immutable run identity
   and artifact ZIP digest, runs all strict tests and discloses a canonical
   R33-derived JSON witness.
4. Commit exactly the independently disclosed JSON and rerun equality gate.
5. Update full CURRENT-STATE, timeline and source registry without
   truncation; fast-forward main only after comparing remote HEAD.

**OPEN:** actual caller/entry/flag values and branch outcomes; original
filename, API return/handle, ReadFile/WriteFile buffers/length128, native save
schema/persistence, CRT/heap/alias ownership, server-only content and
cross-version equivalence. No new-game production.
