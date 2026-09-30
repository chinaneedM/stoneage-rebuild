# Recovered25 World-Profile Adapter R1

## Status

This layer binds the closed recovered25 world profile to the engine-neutral local runtime interfaces without promoting later recovered content into Taiwan-v1 history.

Artifacts:

- `tools/stoneage_recovered25_world_profile_adapter.py`
- `tools/stoneage_recovered25_runtime_bundle_smoke.py`
- `tests/test_stoneage_recovered25_world_profile_adapter.py`

## 1. World topology

The adapter consumes the already-closed ordered materializable runtime topology.

Repository-derived facts used directly:

- materializable map definitions: **826**;
- ordered active classic Warp edges: **2724**;
- every concrete map definition carries structured provenance;
- every current recovered25 map remains `LATER_RECOVERED`;
- unresolved floor-130 version fork remains outside the default 826-floor materializable set.

The adapter does not parse proprietary map payload bytes merely to construct the topology.

## 2. Region materialization boundary

`materialize_region` currently returns a provenance-bearing engine-neutral **region descriptor**:

- floor and rectangle;
- map dimensions;
- payload SHA-256;
- content/resource role;
- source versions;
- evidence references.

This is intentionally not a fabricated historical `map\\%d.dat` cache and not yet a decoded tile/object/event plane payload.

A future concrete map-payload source can attach decoded region planes behind the same `VersionedWorldProfileProvider` boundary without changing the bootstrap contract.

## 3. Fresh starts

The adapter exposes the four fixed-descendant normal hometown positions as ordinals 1..4 and validates that every start lies inside the 826-floor topology.

`Recovered25FreshStartFactory` deliberately requires a caller-supplied `PersistentPlayerState` factory.

Reason: the world adapter owns **where/version/provenance** a start occurs; it must not invent player name, stat allocation, unresolved starter-item instances or other character-creation choices merely to make a convenient default.

The existing player creation/birth/economy models remain the source for those separate semantics.

## 4. State-gated transition binding

The public bootstrap contract contains only semantic gated-transition identities.

Concrete recovered WarpMan operands are bound only when a verified recovered25 preservation bundle is present.

`derive_recovered25_transition_bindings` derives, in memory:

- hometown 3 selected WarpMan bridge;
- hometown 4 selected WarpMan bridge;
- the closed shadowed-branch progression ingress.

For hometown 3/4, the selected bridge must still be exactly one WarpMan edge with one `ITEM = ...` requirement.

For the shadowed branch, the progression report fixes source/destination floors and the bundle must expose exactly one concrete WarpMan binding for that ingress.

Raw coordinates, item IDs, filenames, arguments and dialogue are not emitted by the smoke report and are not copied into the public JSON contract.

## 5. Gate evaluation

R1 supports two implementation-level gate forms.

### ITEM_EQ

Used by the two fresh-start bridge WarpMan transitions.

The evaluator checks the authoritative local player's inventory template identities.

The check does not consume the item because the selected recovered WarpMan action stage is already proven inert and no item-removal side effect is promoted.

### WORLD_FLAG

Used by the 811→820 shadowed-branch ingress at this orchestration layer.

The historical/recovered progression proof is already closed separately. The local runtime represents completion of that compound progression state with an explicit persistent world flag:

`transition:shadowed_branch_ingress:progression_unlocked`

This does not erase the underlying historical prerequisites; it is the local product's durable state projection of the closed compound witness.

## 6. Smoke-test chain

The bundle-backed smoke test exercises:

1. load `stoneage.runtime-bootstrap.r1`;
2. load the 826-floor ordered recovered25 world topology;
3. expose all four fresh-start seeds;
4. materialize provenance-bearing region descriptors;
5. derive all three current gated transition bindings from the verified bundle;
6. evaluate the two item gates and the progression flag gate;
7. encode and decode the local runtime-session envelope.

Its committed report contains only aggregate counts and provenance labels.

## 7. Boundary

This R1 adapter does **not** yet decode actual map tile/object/event planes for production rendering/pathing.

It also does not choose an engine.

The next seam after this adapter closes is the concrete recovered25 region payload source: decode authoritative recovered map payloads into an engine-neutral tile/object/event region representation behind the existing provider boundary.
