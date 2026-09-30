# Recovered25 Encounter Runtime Integration R1

## Status

**CLOSED / REMOTE BUNDLE VALIDATED.**

This integration closes the composition gap between the already reconstructed
versioned encounter/master-data model and the concrete recovered25 local
runtime stack.

## Evidence boundary

Historical foundation remains Taiwan Waei/JSS v1.0.

The encounter rows, groups and enemy variants used here are from the verified
recovered25 preservation specimen and remain explicitly
`LATER_RECOVERED`. They are a version-tagged runtime bridge, not evidence that
the same concrete rows existed in Taiwan v1.0 or JSS 1999.

No missing group/enemy reference is repaired.

## Runtime loader

`tools/stoneage_recovered25_encounter_runtime.py` composes only already
validated layers:

- the stable-later map lineage manifest;
- recovered25 stable-world semantic coverage;
- versioned world geometry;
- the active server `encount/group/enemy` files selected by `setup.cf`;
- the existing strict `EncounterAreaBridge`, `GroupBridge` and
  `EnemyVariantBridge` models;
- `VersionedEncounterRuntimeAdapter`.

The loader mirrors the existing audit probe's source selection rules. The
verified specimen's duplicate GROUP_ID is handled exactly as in the audit:
first loaded identity is retained for the runtime existence join; no merge is
invented.

## Stack contract

The full `Recovered25LocalRuntimeStack.from_verified_bundle()` composition may
supply the verified server data directory and then loads the encounter adapter
alongside maps, collision, Warp, state-gated WarpMan and initial NPC occupancy.
Subsystem-only smokes may omit `server_data_dir`; in that case encounter runtime
is intentionally absent rather than synthesized.

The stack exposes:

- `historical_domain_for_session(session)`;
- `request_encounter_group(session, group_roll=...)`;
- `request_encounter(session, group_roll=..., enemy_roll=..., level_roll=...)`.

The methods rebuild an engine-neutral historical domain at the authoritative
session position and reuse the existing strict encounter resolver. They do not
generate random numbers internally.

## Known specimen defects

The committed aggregate audit for the stable world contains:

- 402 stable encounter areas;
- 23 positive unresolved group references;
- 19 affected encounter areas;
- 469 referenced groups;
- zero missing enemy references among the stable referenced groups that do
  resolve.

Affected areas remain fail-closed. A runtime request that selects a positive
missing group continues to raise rather than silently skipping or substituting
content.

## Validation

The bundle-backed recovered25 runtime smoke is extended to require:

- 402 stable encounter areas;
- 23 unresolved positive group references;
- 19 affected encounter areas;
- at least one legal group-resolution witness;
- at least one legal enemy-variant/level-resolution witness.

This validation uses the transient hash-pinned preservation bundle; raw rows,
names and proprietary payloads are not committed by this integration.

## Next restoration seam

After bundle CI closure, connect movement-side encounter frequency/CEP to the
local session coordinator so a successful ordinary walk can produce a
versioned encounter request using explicit deterministic rolls.

Only after that bridge is closed should the existing deterministic battle shell
be attached to the coordinator. Battle AI/RNG remains explicit and must not be
invented during this restoration step.


## Remote closure

GitHub Actions `36745555249` completed successfully against the hash-pinned
preservation bundle. The concrete local-runtime smoke proved the 402/23/19
encounter boundary and produced both group-resolution and enemy-variant/level
runtime witnesses while the existing server/client collision validations also
remained green.
