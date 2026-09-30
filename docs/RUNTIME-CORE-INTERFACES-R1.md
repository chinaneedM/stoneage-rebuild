# Runtime Core Interfaces R1

## Status

**R1 objective:** define the minimum engine-neutral local runtime interfaces that consume `game/RUNTIME-BOOTSTRAP-RECOVERED25-R1.json` while reusing the repository's existing deterministic historical models.

Implementation artifact:

- `tools/stoneage_local_runtime_core.py`

Regression tests:

- `tests/test_stoneage_local_runtime_core.py`

## 1. Reuse before rewrite

The repository already contains substantial engine-independent runtime machinery:

- `stoneage_singleplayer_domain.py` — static/persistent/transient/interaction partitions and typed identities;
- `stoneage_singleplayer_world.py` — map topology, provenance-aware maps and classic overlap Warp;
- `stoneage_singleplayer_runtime.py` — deterministic movement/encounter/battle composition with explicit RNG inputs;
- `stoneage_singleplayer_persistence.py` — versioned player-owned persistent state;
- the existing combat, item, pet, shop, warp, encounter and progression models.

R1 does **not** replace those modules.

It supplies the missing orchestration contracts around them.

## 2. Required ports

### VersionedWorldProfileProvider

Purpose: resolve authoritative world regions for one version-tagged runtime profile.

Input:

- floor/rectangle;
- explicit world profile, currently `recovered25`.

Output:

- materialized engine-neutral region payload;
- provenance metadata.

The provider may decode server-only recovered maps, cached historical maps or future reconstructed maps, but the caller must see provenance.

### TransitionBindingResolver

Purpose: bind a semantic state-gated transition from the bootstrap contract to concrete recovered/reconstructed runtime coordinates and predicate operands.

This is where withheld/raw recovered IDs may be resolved.

The semantic bootstrap contract itself does not need to publish those raw identities.

### TransitionGateEvaluator

Purpose: evaluate a bound conditional transition against authoritative local session state.

It returns an explicit decision and any state that would be consumed/mutated by traversal.

A failed gate never becomes an unconditional graph edge.

### FreshStartFactory

Purpose: create a complete initial player/session seed for one of the four contracted hometown ordinals.

The factory owns versioned content binding for:

- start coordinates;
- initial player state;
- starter inventory/economy values;
- any provenance-bearing initial configuration.

It may not merge all four hometowns into one fake canonical start.

### LocalPersistenceStore

Purpose: persist encoded local runtime session snapshots.

The storage backend may be a local file, database or engine save API. The deterministic session schema must remain backend-independent.

## 3. Runtime bootstrap loader

`load_runtime_bootstrap_contract` validates the machine contract before any content is bound.

R1 rejects:

- any schema other than `stoneage.runtime-bootstrap.r1`;
- historical foundation other than `taiwan-v1.0`;
- runtime world profile other than `recovered25`;
- recovered25 evidence role other than `LATER_RECOVERED`;
- any attempt to mark recovered25 as proven Taiwan-v1 membership;
- missing/duplicate hometown routes;
- hometown sets other than ordinals 1..4;
- non-closed ordered routes;
- state-gated transitions marked unconditional.

This converts provenance constraints into executable architecture rules.

## 4. Local session snapshot

The existing `stoneage_singleplayer_persistence.py` correctly persists only player-owned historical state and intentionally excludes transient world/session state.

A local single-player product also needs to resume the **local runtime session**.

R1 therefore adds a modern DESIGN envelope:

`stoneage.local-runtime-session.r1`

It contains only:

- bootstrap `contract_id`;
- `world_profile`;
- selected hometown ordinal;
- current player map position;
- persistent world/progression flags owned by the local product layer;
- the existing versioned player-owned persistence payload.

It still does **not** persist:

- runtime object IDs;
- active NPC dialog sessions;
- battle sessions;
- renderer state;
- network/account state;
- transient NPC object tables.

This is intentionally stronger/cleaner local persistence than the historical asynchronous SAAC mechanism, while historical save/logout semantics remain documented separately.

## 5. State partitions

The local runtime should keep these partitions separate.

### Static/versioned content

Examples:

- maps/regions;
- NPC templates/placements;
- encounter tables;
- item/pet/enemy templates;
- unconditional classic transitions;
- semantic state-gated transition specs.

### Persistent player state

Existing R3 payload:

- character;
- inventory;
- pets and hidden pet-growth identity.

### Persistent local world/session state

R1 local envelope:

- current location;
- selected bootstrap/profile identity;
- persistent progression/world flags.

### Transient runtime state

Examples:

- runtime object IDs;
- active NPC sessions;
- battle sessions;
- cached materialized regions;
- renderer/audio state;
- ephemeral movement/AI work values.

Transient state is reconstructed after load.

## 6. Transition topology rule

The topology layer has two classes of edge.

### Unconditional classic edge

May be represented in `HistoricalWorldTopology.legacy_warps` after its historical/time ambiguity is resolved.

### State-gated transition

Must remain a separate contract/binding/evaluation path.

Examples in the current bootstrap:

- the recovered progression-gated 811 → 820 ingress;
- hometown 3 selected WarpMan bridge;
- hometown 4 selected WarpMan bridge.

A graph/pathing system may query both layers, but it must not erase the predicate boundary.

## 7. Determinism/RNG

The existing runtime correctly keeps RNG rolls explicit inputs.

R1 preserves that rule.

An engine may own a seeded RNG service, but deterministic mechanics should receive concrete rolls/decisions through the runtime boundary so:

- tests are reproducible;
- replays/debugging are possible;
- historical existential witnesses are not confused with guaranteed outcomes.

## 8. Engine boundary

Nothing in R1 depends on:

- Godot nodes/scenes;
- Unity MonoBehaviours/GameObjects;
- SDL windows;
- sockets;
- an account server;
- an MMO shard process.

A future engine adapter should call the local runtime core and render its resulting state.

## 9. Next implementation seam

After R1 interface validation, the next deterministic implementation seam is:

1. create a provenance-bearing `recovered25` world-profile adapter;
2. materialize the 826-floor world manifest into `HistoricalWorldTopology`/region-provider inputs;
3. bind the two hometown state-gated WarpMan transitions and the 811→820 progression ingress;
4. create the four FreshStartFactory seeds;
5. run an in-process smoke test from bootstrap load → fresh start → region materialization → transition evaluation → local-session save/load.

That seam still does not require a rendering engine.
