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


## 2B. Recovered25 initial NPC occupancy

A verified recovered25 stack now supplies a deterministic initial NPC occupancy manifest to the coordinator instead of leaving the live registry empty.

The manifest composes two separately versioned evidence surfaces:

- recovered25 / LATER_RECOVERED stable-world NPC placement and template projection;
- pinned stable-descendant CHAR_ISOVERED behavior classification.

The audited initial overability profile covers all **3,856** recovered placements:

- **2,264** Warp placements are STATIC_OVERABLE;
- **1,592** remaining placements inherit the stable descendant default CHAR_ISOVERED = 1;
- no current placement is STATIC_BLOCKING, DYNAMIC, UNRESOLVED, or LINEAGE_DIVERGENT.

The existing spawn-integrity boundary is retained. **3,852 / 3,856** placements are eligible to seed the live registry; the existing four quarantined placement rows remain excluded from runtime instantiation rather than being repaired or silently admitted.

Recovered25LocalRuntimeStack carries this manifest, and LocalRuntimeSessionCoordinator seeds it into RuntimeDynamicOccupancyRegistry during coordinator construction. Each seeded object has the stable identity npc-placement:<placement_id>, CHARACTER kind, recovered birth position, explicit overable state, and provenance identifying the overability classification.

This does not merge NPC occupancy into static collision. The movement result continues to expose static routing provenance separately from dynamic occupancy provenance.

The live occupancy lifecycle is now persisted by the separate `stoneage.local-runtime-save.r1` wrapper. Deterministic initial NPC seeds are reconstructed from the versioned runtime stack and only explicit differences from that baseline are serialized. Static collision remains outside mutable save state.

## 2C. Interaction discovery and dispatch

Presentation code does not need recovered NPC argument strings or raw source rectangles to discover interactions. `discover_state_gated_interactions()` returns only interactions whose recovered source area contains the current player coordinate.

Each returned `LocalRuntimeInteraction` contains:

- stable semantic `transition_id`;
- interaction kind;
- current live eligibility and reason;
- version/evidence provenance already carried by the recovered binding;
- `execution_supported`, which is false if a future gate reports a state mutation the coordinator does not yet implement.

The discovery call is non-mutating. It may evaluate current recovered predicates, but it does not move the player or modify inventory/Stone/flags. It deliberately does not expose source rectangles, destinations or legacy NPC argument data as part of its presentation-facing contract.

`dispatch_state_gated_interaction()` accepts the semantic transition id and delegates to the canonical `execute_state_gated_transition()` path. That path independently repeats spatial and live-gate validation, so discovery cannot be used as a stale authorization token.

Classic overlap-Warp remains part of ordinary movement and is not duplicated in the interaction-discovery surface.


## 2D. Movement-side encounter frequency / CEP

The coordinator carries `EncounterFrequencyState` as **transient runtime state**.
This follows the stable-descendant evidence in which CEP is stored on the
connection/runtime object and a new connection initializes it to zero.

CEP is therefore intentionally **not** added to
`stoneage.local-runtime-session.r1` or `stoneage.local-runtime-save.r1`.
`new_game()` and `continue_game()` establish a fresh runtime CEP state at
zero. This is a reconstruction boundary, not a claim about an original retail
save-file field.

`walk_one_cell_with_runtime_collision_and_encounter_frequency()` composes only
already reconstructed layers:

1. unified static + live-occupancy movement;
2. successful-walk check;
3. departure-coordinate encounter-zone lookup;
4. CEP min/max refresh and clamp;
5. caller-supplied explicit roll in the reconstructed modulo-120 domain;
6. Classic-Warp encounter suppression using the canonical walk result;
7. on a real hit, caller-supplied group/enemy/level rolls through the
   versioned encounter runtime.

Blocked movement does not advance CEP. A Classic Warp still performs the CEP
roll: a miss increments toward max; a hit is suppressed without encounter
dispatch and without the normal miss increment. This preserves the
stable-descendant ordering already documented in
`research/mechanics/STONEAGE-ENCOUNTER-FREQUENCY-CEP-R1.md`.

The coordinator does not create RNG and does not infer battle/encounter rolls.
The exact CEP mechanism remains strong descendant evidence; its presence in
JSS 1999 / Taiwan v1.0 is still open and must not be promoted.

## 2E. Transactional local group battle context

The coordinator now owns a transient battle transaction boundary without making
battle state part of the local save contract.

`start_group_battle()` requires an authoritative
`LocalRuntimeSessionState`, a resolved `GroupEncounterRequest`, and explicit
enemy-count/selection/birth rolls. It serializes the current
`PersistentPlayerState` through the existing versioned persistence codec and
immediately decodes that payload into a working clone. The battle domain is
therefore isolated from the caller-owned session state.

Enemy materialization is delegated to the recovered25 stack's
`spawn_group_enemies()` bridge. The coordinator then calls the existing
`begin_group_battle()` shell. It does not choose AI, commands, initiative
randomness, attack rolls, escape/capture rolls, drops, EXP thresholds, or a
battle result.

The returned `LocalRuntimeBattleContext` is transient. It keeps:

- bootstrap/world profile identity;
- hometown ordinal and origin position;
- world flags;
- the versioned persistent-state snapshot;
- the immutable battle shell;
- the concrete spawned-enemy provenance records.

`settle_group_battle()` takes only that context plus an explicit
`BattleOutcome`. It reconstructs a fresh working persistent state from the
snapshot, applies the already validated battle-outcome adapter, and returns a
**new** `LocalRuntimeSessionState` at the same world position. The input
session is never mutated in place.

This boundary is deliberate: active battle state is transient simulation state,
while only the resulting player-owned state becomes eligible for the existing
local save contract after settlement.

Enemy display names may remain unresolved while the recovered25 enemybase
CP950/Big5 two-row ambiguity is open. That affects presentation only; player
and owned-pet names remain mandatory, and no synthetic enemy name is created.

## 2F. Persistent ATTACK/WAIT multi-round battle state

The local battle transaction now exposes a deliberately narrow persistent-round
seam before capture/escape/skill/AI integration.

`begin_persistent_group_battle()` promotes a transient
`LocalRuntimeBattleContext` into the existing
`PersistentBattleState` using an explicit participant-to-slot mapping.

`resolve_persistent_attack_wait_round()` accepts only explicit
`BattleCommand` values whose command code is ATTACK or WAIT. The caller must
also provide:

- initiative random subtracts for every living actor;
- combat profiles;
- attack rolls for attacking actors;
- defense profile;
- optional field attribute/power and tie-break order.

The coordinator delegates the round to the already recovered
`resolve_persistent_ordinary_round()` model. HP, pending EXP, turn number,
status runtime, enemy removal and terminal victory/defeat determination persist
inside the returned immutable battle state. The method returns a new battle
context plus the concrete `PersistentRoundResult`.

No enemy command is synthesized. An enemy WAIT is a caller decision just like a
player ATTACK. Capture, escape, item, skill, guard/combo and automatic AI
commands are rejected at this R1 coordinator seam rather than guessed.

`settle_persistent_group_battle_without_level_crossing()` reconstructs the
original player-owned persistent-state snapshot, runs the existing terminal
battle settlement, and returns a new `LocalRuntimeSessionState`. Below-threshold
EXP and already-buffered battle profit may settle; an unresolved level-up
threshold remains fail-closed and must use the separate progression seam.

The original pre-battle session remains unchanged throughout the transaction.

## 3. State-gated dialogue transitions

The three current recovered25 conditional transitions remain outside the unconditional classic-Warp graph.

Before consulting the live gate evaluator, the coordinator requires:

- binding kind = recovered dialogue WarpMan;
- a normalized recovered source rectangle;
- current floor = binding source floor;
- current coordinate inside the recovered source rectangle.

Only then is the existing state-gate evaluator invoked against the current player state.

If the gate is denied, position is unchanged. If allowed, the binding destination must still be inside the loaded topology before the position is changed.

Current R1 recovered gates report no consumed-state mutation. The current set has exactly three recovered dialogue WarpMan transitions; all are `FREE`-predicate eligibility gates, and the two hometown bridges additionally carry `event_action_side_effect_fields = 0`. Regression tests assert that both allowed and denied evaluator decisions keep `consumed_state` empty. The coordinator rejects any future non-empty `consumed_state` result instead of silently ignoring it; action-stage mutation must be implemented explicitly only if a later recovered binding actually requires it.

## 4. Persistence boundary

`save_game` and `continue_game` now use the versioned `stoneage.local-runtime-save.r1` envelope documented in `docs/LOCAL-RUNTIME-SAVE-R1.md`. It embeds the existing `stoneage.local-runtime-session.r1` payload and adds only baseline-relative live-occupancy deltas.

`continue_game` remains backward compatible with legacy standalone `stoneage.local-runtime-session.r1` payloads; those rehydrate the current deterministic initial occupancy baseline and contain no invented live mutations.

Persistence transport remains a caller-supplied `LocalPersistenceStore`. The existing in-memory store remains a deterministic composition/test implementation. Durable single-player storage is now provided by `LocalFilesystemPersistenceStore` (`tools/stoneage_local_filesystem_persistence.py`): logical keys are SHA-256-mapped inside one configured root, payloads are stored as exact UTF-8 bytes, writes use same-directory temporary files plus `os.replace`, and the storage layer never parses or rewrites the versioned save schema. Regression coverage reconstructs a second coordinator against the same filesystem root and verifies that both session state and live occupancy deltas survive the process-object boundary.

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
