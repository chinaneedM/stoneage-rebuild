# Local Runtime Session Coordinator R1

## Status

This DESIGN layer is the minimal application-service boundary above the closed recovered25 local runtime stack.

Artifacts:

- `tools/stoneage_local_runtime_session_coordinator.py`
- `tests/test_stoneage_local_runtime_session_coordinator.py`

It does **not** select a rendering engine, recreate legacy MMO transport, add an account service, or invent unresolved historical collision semantics.

## 1. Session lifecycle

`LocalRuntimeSessionCoordinator` owns the ordering of:

1. new-game creation from one of the four versioned fresh-start seeds;
2. validation of contract/profile/topology identity;
3. current-region materialization;
4. ordinary movement commands;
5. classic overlap-Warp resolution;
6. dialogue/state-gated transition execution;
7. local save and continue through the `LocalPersistenceStore` port.

The authoritative application state remains `LocalRuntimeSessionState`.

## 2. Ordinary movement boundary

`walk_one_cell` accepts only a same-floor, non-zero, one-cell destination.

It deliberately requires an explicit `entry_allowed` verdict. The coordinator does not infer collision from raw DAT/LS2MAP tile or object identifiers.

This preserves the evidence boundary already established by the collision models: a selected validated collision adapter must supply the verdict.

After that verdict is supplied, classic overlap-Warp behavior is delegated to the existing `resolve_player_walk` historical world implementation. The coordinator does not create a second Warp implementation.



## 2A. Unified recovered25 collision and live occupancy

The canonical recovered25 movement entry point is `walk_one_cell_with_runtime_collision()`.

It preserves two independent gates and their provenance:

1. **static routed collision** — selected per floor by the recovered25 collision router:
   - recovered server LS2MAP + recovered mapset where that evidence is closed;
   - recovered client DAT + ADRN under the explicitly labelled descendant-stable reconstruction profile for server gaps;
2. **dynamic live-object occupancy** — evaluated only after static entry succeeds using the stable-descendant target-cell overability rule.

The live occupancy gate accepts explicit `DynamicOccupant` values for the destination cell:

- non-overable character -> blocked;
- non-overable item -> blocked;
- gold -> does not block in the inspected switch;
- overable character/item -> does not block.

A dynamic occupant can never override a static collision denial. Conversely, static walkability does not imply that the destination is free of live blockers.

The returned `LocalRuntimeWalkResult` retains both evidence surfaces separately:

- static collision provider kind / evidence class / semantic profile / exact-binary-proof flag;
- static collision decision;
- dynamic collision decision;
- dynamic occupancy profile and evidence class.

This keeps recovered client hit-map semantics distinct from descendant live-object overlap semantics rather than merging them into a synthetic collision model.

## 3. State-gated dialogue transitions

The three current recovered25 conditional transitions remain outside the unconditional classic-Warp graph.

Before consulting the live gate evaluator, the coordinator requires:

- binding kind = recovered dialogue WarpMan;
- a normalized recovered source rectangle;
- current floor = binding source floor;
- current coordinate inside the recovered source rectangle.

Only then is the existing state-gate evaluator invoked against the current player state.

If the gate is denied, position is unchanged. If allowed, the binding destination must still be inside the loaded topology before the position is changed.

Current R1 recovered gates report no consumed-state mutation. The coordinator rejects any future non-empty `consumed_state` result instead of silently ignoring it; action-stage mutation must be implemented explicitly before such a transition can execute.

## 4. Persistence boundary

`save_game` and `continue_game` use the existing versioned `stoneage.local-runtime-session.r1` envelope and a caller-supplied `LocalPersistenceStore`.

An in-memory store is included only as a deterministic composition/test implementation. Durable filesystem storage remains a separate implementation seam.

## 5. Engine boundary

A future Godot/Unity/other presentation layer should send commands to this coordinator rather than mutate world/player state directly.

The renderer may display the materialized region and session state, but it does not become authoritative for:

- player position;
- classic Warp;
- recovered conditional transitions;
- persistent player/world flags;
- bootstrap/profile identity.

## 6. Provenance

The coordinator does not change provenance classification.

- historical foundation: Taiwan/Waei v1.0;
- runtime world: recovered25;
- recovered25 evidence role: `LATER_RECOVERED`.

No recovered25 content is relabelled as Taiwan-v1 historical membership.
