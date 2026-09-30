# Local Engine Adapter Contract R1

## Status

**DESIGN / IMPLEMENTED.** This contract defines semantic input intents and output updates above the engine-neutral local application facade. It is not a Godot, Unity, SDL, web, or desktop implementation.

Canonical artifacts:

- `tools/stoneage_local_engine_adapter.py`
- `tests/test_stoneage_local_engine_adapter.py`

Profile: `STONEAGE_LOCAL_ENGINE_ADAPTER_CONTRACT_R1`.

## 1. Input intents

A future concrete input adapter maps keyboard/controller/touch/UI actions into a small semantic command set:

- `NewGameIntent(hometown_ordinal)`
- `ContinueGameIntent(save_key)`
- `SaveGameIntent(save_key)`
- `MoveIntent(dx, dy)`
- `DispatchInteractionIntent(transition_id)`
- `RefreshViewIntent()`

`MoveIntent` is a one-cell direction delta rather than an authoritative destination. The semantic adapter derives the destination from the current authoritative session before delegating to the facade.

## 2. Output update

Every accepted intent returns `LocalEngineUpdate` containing:

- a semantic `event_kind`;
- a fresh `LocalApplicationView`;
- the detailed walk result when the intent was movement;
- the detailed transition result when the intent dispatched an interaction;
- the logical save key when relevant.

A renderer may use the view/update to redraw or animate, but does not mutate player position, collision state or transition eligibility itself.

## 3. Session ownership

`LocalEngineAdapter` keeps the current immutable `LocalRuntimeSessionState` reference for presentation flow. New game/continue replace it; movement/interaction replace it with the canonical result returned by the facade.

Save and refresh require an active session. Commands issued before new game/continue fail closed.

## 4. Dependency boundary

The adapter imports no recovered25-specific module and no rendering/input framework. Recovered provenance, collision routing, dynamic occupancy, interaction geometry/gates and persistence schemas remain behind the facade/coordinator/runtime stack.

This means future engine evaluation can compare presentation technologies without changing deterministic core semantics.
