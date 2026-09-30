# Local Application Facade R1

## Status

**DESIGN / IMPLEMENTED.** This is the narrow application boundary intended for a future renderer/input adapter.

Canonical artifacts:

- `tools/stoneage_local_application_facade.py`
- `tests/test_stoneage_local_application_facade.py`

Profile: `STONEAGE_LOCAL_APPLICATION_FACADE_R1`.

## 1. Dependency direction

Presentation code should depend on `LocalApplicationFacade`, not on recovered25-specific world adapters, collision providers, NPC binding parsers, bootstrap derivation tools or save-schema codecs.

The facade itself imports only engine-neutral local runtime/domain types and `LocalRuntimeSessionCoordinator`. Tests assert that its implementation does not import recovered25-specific modules.

This does not erase provenance. The coordinator and runtime stack behind the facade continue to retain the historical/recovered evidence classes.

## 2. Commands and reads

R1 exposes only the commands/read surfaces already closed below it:

- new game from a versioned hometown ordinal;
- continue from a logical save key;
- save the authoritative session;
- read the current materialized region;
- read a combined `LocalApplicationView` of session + current region + spatially available semantic interactions;
- execute one-cell movement through the canonical unified collision/occupancy path;
- discover state-gated dialogue interactions;
- dispatch a selected semantic interaction id.

The facade does not expose raw collision verdict injection, raw recovered source rectangles, legacy NPC argument strings or direct mutable access to runtime internals.

## 3. Movement and interaction authority

`move_one_cell()` always delegates to `walk_one_cell_with_runtime_collision()`. A future renderer cannot mark a destination walkable on its own.

`dispatch_interaction()` delegates to the coordinator's state-gated dispatcher, which repeats source-geometry and live predicate validation. A previously rendered interaction is not treated as an authorization token.

Classic overlap-Warp continues to be resolved by ordinary movement and is not surfaced as a dialogue interaction.

## 4. Engine boundary

No rendering engine, scene graph, input library, window toolkit, audio layer or asset pipeline is selected here.

A future engine adapter may translate keyboard/controller/touch input into facade commands and render facade results, but it must not become authoritative for player position, collision, persistence or recovered transition eligibility.
