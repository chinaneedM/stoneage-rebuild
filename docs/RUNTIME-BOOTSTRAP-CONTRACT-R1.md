# Runtime Bootstrap Contract R1

## Status

**R1 contract target:** the closed recovered25 world/start/progression semantics are promoted into an **engine-neutral local-first runtime bootstrap contract** without being relabelled as Taiwan v1.0 historical content.

Machine-readable contract:

- `game/RUNTIME-BOOTSTRAP-RECOVERED25-R1.json`

Validation:

- `tests/test_stoneage_runtime_bootstrap_contract.py`
- `.github/workflows/validate-stoneage-runtime-bootstrap-contract.yml`

## 1. Why this contract exists

The archaeology layer has now closed a deterministic recovered25 world surface in which all four normal fresh-start hometowns have at least one legal ordered progression into the full materializable world.

That result is useful for implementation, but it must not collapse two separate questions:

1. **historical foundation:** what the accepted Taiwan/Waei v1.0 client directly proves;
2. **runtime bootstrap surface:** what later recovered25 data and pinned descendant semantics let us reconstruct deterministically enough to exercise a complete local world.

The contract is therefore an implementation boundary, not a historical-merger declaration.

## 2. Version and provenance boundary

The runtime must carry both identities simultaneously:

- `historical_foundation = taiwan-v1.0`
- `runtime_world_profile = recovered25`
- `runtime_world_profile.evidence_role = LATER_RECOVERED`
- `historical_membership_in_taiwan_v1 = UNPROVEN`

No recovered25 map, NPC, item, route or transition becomes Taiwan-v1 content merely because it is usable by the reconstruction runtime.

The Taiwan-v1 gameplay schema remains the foundation for client/runtime state interpretation. The Taiwan-v1→2.5 bridge remains the controlled mapping layer where later master data is used to reconstruct runtime state.

## 3. Deployment boundary

R1 assumes:

- local-first single-player execution;
- local authoritative world/player/NPC/pet/item/progression/combat state;
- no account server requirement;
- no legacy socket/LSSPROTO requirement;
- no engine commitment;
- internal semantics that could later be separated behind an authorized client/server boundary without changing rule meaning.

This follows DD-013 and DD-014. Historical network behavior is retained as evidence about authority and materialization, not as mandatory production topology.

## 4. Map/world bootstrap semantics

The world bootstrap is version-tagged `recovered25`.

Closed R1 world facts:

- materializable floors: **826**;
- fresh-start state-gated reachable floors: **826**;
- remaining unreachable floors: **0**.

Map handling is semantic:

1. authoritative world region exists in the local world model;
2. runtime validates whether a region is materialized;
3. runtime requests/loads the authoritative region representation;
4. renderer/pathing consumes the materialized region.

Any generated compatibility DAT/cache is transient implementation output, never historical evidence.

## 5. Fresh-start bootstrap

The contract exposes **4** normal hometown choices.

Two hometowns use a classic coordinate route to the award chain. Two require a recovered state-gated `WarpMan` bridge.

The runtime must not flatten those four starts into one generic unconditional connectivity graph.

Ordered R1 route classes:

| Hometown ordinal | Route class | Required ordered milestones |
| --- | --- | --- |
| 1 | classic | COMBAT |
| 2 | classic | COMBAT |
| 3 | state-gated WarpMan | COMBAT → SHOP → WARPMAN |
| 4 | state-gated WarpMan | SHOP → COMBAT → WARPMAN |

The order is part of the contract, not presentation metadata.

## 6. Starter state and economy

Pinned bootstrap constraints:

- item capacity = **15**;
- positive configured starter items = **13**;
- guaranteed empty item slots = **2**;
- starting Stone is positive;
- starting Stone covers the minimum valid award fee;
- on both bridged hometown routes, starting Stone covers the bridge-item purchase plus the later award fee.

Amounts and raw item identities may remain in provenance-preserving derived data. The engine contract consumes the semantic predicates rather than inventing replacement values.

## 7. Leveling/combat boundary

Birth level alone is not sufficient for the award/gate joint state.

A valid fresh-start runtime path therefore requires finite repeatable positive-EXP progression.

R1 closes existence, not balance:

- repeatable positive-EXP source exists;
- legal fresh-character combat-victory witnesses exist;
- finite repetition can reach the required joint progression state;
- no claim is made about efficient leveling;
- no guaranteed RNG claim is made;
- no final pacing decision is made.

A production balancing layer may later change pacing only through an explicit design decision, not by silently rewriting this evidence contract.

## 8. State-gated transitions

State-gated edges are first-class runtime objects.

They must contain:

- transition identity;
- version/provenance identity;
- source/destination binding;
- explicit predicates;
- fee state;
- schedule/party gates if present;
- action side effects;
- RNG/existential scope.

They must **not** be inserted into the unconditional map graph.

R1 contains:

1. the already closed shadowed-branch ingress `811 → 820`, gated by the closed progression witness;
2. one selected recovered WarpMan bridge for hometown 3;
3. one selected recovered WarpMan bridge for hometown 4.

For the two hometown bridges:

- FREE grammar is one `ITEM = ...` atom;
- fee is disabled;
- schedule gate is absent;
- party gate is absent;
- `FreeMsg` is present;
- action-stage side-effect fields = **0**;
- a normal affordable ItemShop acquisition route is required.

Raw bridge coordinates/item IDs remain bound through the derived recovered-data adapter rather than copied into this public semantic contract.

## 9. Runtime loading sequence

An implementation conforming to R1 should conceptually perform:

1. load this bootstrap contract;
2. load the Taiwan-v1 runtime/gameplay foundation schema;
3. attach the recovered25 world profile as `LATER_RECOVERED`;
4. construct authoritative world/map region data;
5. register unconditional classic transitions;
6. register state-gated transitions separately;
7. create fresh player state for the selected hometown;
8. apply starter inventory/economy constraints;
9. evaluate progression/interaction predicates during play;
10. materialize only the world regions needed by runtime presentation/pathing;
11. persist authoritative local state independently of the rendering engine.

## 10. Non-goals

R1 does not choose Godot, Unity or another engine.

R1 does not define rendering, input, UI, audio, asset replacement, save-file format, scripting API or final balance.

R1 does not claim that recovered25 world membership equals Taiwan v1.0 world membership.

R1 does not turn existential combat or WarpMan outcomes into guaranteed outcomes.

## 11. Acceptance invariants

The machine-readable contract and CI must keep these invariants true:

- 826 materializable / 826 reachable / 0 unreachable;
- 4 normal hometowns;
- 2 classic + 2 state-gated hometown routes;
- all 4 ordered routes closed;
- bridged starts preserve SHOP/WARPMAN state ordering;
- state-gated edges remain conditional;
- Taiwan v1 foundation and recovered25 world provenance remain distinct;
- legacy networking remains optional implementation detail, not a rule dependency.

If later evidence contradicts these facts, the contract is superseded by a new version rather than silently edited into a different historical claim.
