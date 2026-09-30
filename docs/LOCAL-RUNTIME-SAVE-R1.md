# Local Runtime Save R1

## Status

**DESIGN / IMPLEMENTED.** This document defines the versioned single-player save envelope used above the engine-neutral local runtime session coordinator.

Canonical implementation:

- `tools/stoneage_local_runtime_save.py`
- `tools/stoneage_local_runtime_session_coordinator.py`
- `tests/test_stoneage_local_runtime_save.py`
- `tests/test_stoneage_local_runtime_session_coordinator.py`

Schema id: `stoneage.local-runtime-save.r1`.

## 1. Boundary

The save contract preserves two different state classes without flattening provenance:

1. **session state** — the existing `stoneage.local-runtime-session.r1` payload containing contract/profile identity, hometown ordinal, player position, persistent player state and world flags;
2. **live dynamic occupancy delta** — explicit runtime object differences relative to the deterministic initial occupancy profile supplied by the current versioned runtime stack.

Static map collision is not mutable session state and is never serialized by this contract.

## 2. Occupancy baseline and delta

The recovered25 runtime stack supplies `RECOVERED25_INITIAL_NPC_OCCUPANCY_R1` as its deterministic baseline. On save, a fresh registry is reconstructed from that baseline and compared by stable object identity with the live registry.

The occupancy sub-envelope records:

- `base_profile_id` — exact deterministic initial-occupancy profile expected during restore;
- `registry_profile_id` — exact live registry semantic profile;
- `removed_base_object_ids` — baseline objects explicitly absent in the live state;
- `upserts` — new or changed live objects.

Each upsert stores only explicit live-object state: object id, object kind, floor/x/y position, overability and provenance.

Unchanged baseline objects are omitted. For the real recovered25 initial population, all **3,852** seedable NPC rows therefore produce an empty delta.

## 3. Restore semantics

Restore is deterministic:

1. validate the outer save schema;
2. validate and load the embedded session payload against expected contract/world-profile identity;
3. reconstruct the deterministic initial occupancy baseline from the current runtime stack;
4. require the saved `base_profile_id` to match that baseline exactly;
5. remove explicitly removed baseline objects;
6. apply explicit upserts by stable object id;
7. revalidate all restored live-object positions against the runtime topology before the coordinator accepts the registry.

The decoder rejects malformed shape, profile drift, duplicate removal identities, duplicate upsert identities, remove/upsert identity overlap and attempts to remove objects that do not exist in the deterministic base.

## 4. Lifecycle

- `new_game()` resets live occupancy to the deterministic initial baseline.
- `save_game()` stores current session state plus the baseline-relative occupancy delta.
- `continue_game()` rebuilds the baseline and reapplies the saved delta.

Behavior-driven NPC motion, despawn schedules, item-drop generation and other future simulation rules are not inferred by the save layer. The save layer only persists explicit state already present in the live registry.

## 5. Backward compatibility

The coordinator still accepts legacy standalone `stoneage.local-runtime-session.r1` saves.

A legacy save contains no occupancy delta, so loading it restores the session and reconstructs the current deterministic initial occupancy baseline. No historical live-object mutation is fabricated.

## 6. Provenance boundary

The wrapper does not promote evidence classes:

- recovered25 deterministic initial NPC placement remains `LATER_RECOVERED`;
- descendant overability semantics retain their separately audited provenance;
- client-DAT fallback collision retains `RECOVERED25_DESCENDANT_STABLE_CLIENT_HITMAP_R1` reconstruction status;
- server LS2MAP collision retains its recovered server provenance.

The save contract serializes mutable runtime state, not historical claims.

## 7. Storage boundary

This schema is independent of the persistence transport. `LocalPersistenceStore` stores opaque UTF-8 payload text; schema dispatch remains the coordinator's responsibility.

R1 closes the save-state contract. Durable filesystem storage is a separate engine-neutral seam.
