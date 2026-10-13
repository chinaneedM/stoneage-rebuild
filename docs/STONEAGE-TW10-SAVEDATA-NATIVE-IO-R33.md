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


## 2026-10-13 — R33 original static evidence independently rederived

Original source Action [38411584532](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/38411584532)
job `115345021284` SUCCESS, branch head
`f0fe4a5491ac031f2bc941de6c335b85a1273ea4`.
Full inherited pinned original identity gates and exact R32 digest passed.
The original runtime was **never executed**, source was purged, and only
derived JSON metadata was uploaded as artifact `11822641076`,
`tw10-r33-original-secondary-call-zf-derived`. ZIP digest
`sha256:01286152611e96bc6e9dac874422227336b5b8f84397fcb20b9b4560d54894bc`.
Original-derived JSON is 4772 bytes, SHA256
`1be7d372b0650b9944a12264b612531d46a5326af3628e12363df365ddab98b5`.

Independent custody and static/tamper validations Action
[38411779674](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/38411779674)
job `115345684881` SUCCESS. The complete derived JSON was independently
disclosed for comparison to the canonical repository witness
`research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R33-ORIGINAL.json`.

FACT — pinned original instruction/import/operand syntax only:

- Original indirect CALL `0x4ed19` resolves by PE import slot
  RVA `0x520a8` to `KERNEL32.dll!CloseHandle`. R32's
  `0x4ed1f` maps separately to `GetLastError`; the earlier
  `0x4ed01` imported `CreateFileA`.
- ZF may-definition before JE `0x4ed0b` has one candidate:
  `CMP ESI,EDI` at `0x4ed09`. Both are full-width 32-bit
  register read operands; actual values and predicate are unproved.
- ZF may-definition before JNE `0x4ed16` has one candidate:
  `TEST EAX,EAX` at `0x4ed14`. No original EAX value, return
  provenance or actual branch result is admitted.
- Bounded predecessor walks have no 256-node cap hit and
  neither branch has source-candidate truncation. This is *graph-local
  candidate uniqueness*, not proof that the original runtime
  took any path.
- The may-definition register input surface has four bounded queries;
  all actual register values remain unknown.

HYPOTHESIS only: `CMP ESI,EDI` could participate in an
invalid-handle check, and the `CloseHandle`/`GetLastError`
sequence could be an error/cleanup path. Neither a sentinel value,
successful CreateFileA call nor a native save execution has been proved.
All runtime effects, actual caller ABI, real handles, file schema and
persistence remain OPEN. No proprietary original machine-code bytes
published.

NEXT R34: investigate EDI's reaching definitions at
`0x4ed09`, EAX sources at `0x4ed14`, and
`CloseHandle` pre-CALL argument PUSH chain. Establish bounded
provenance of the synthetic-appearing invalid-handle comparison
without assuming its value; trace conditional branch exits and
whether this path could return to native ReadFile/WriteFile.
Keep actual filename -> CreateFileA return -> handle/buffer/length128
and original native save schema OPEN.
