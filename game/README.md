# Game

Production engine implementation is still intentionally deferred. The project now has an engine-neutral runtime bootstrap boundary that can be consumed before selecting Godot, Unity, or another engine.

Current implementation-facing contract:

- `RUNTIME-BOOTSTRAP-RECOVERED25-R1.json`
- `../docs/RUNTIME-BOOTSTRAP-CONTRACT-R1.md`

The contract is a **version-tagged reconstruction scaffold**. Taiwan/Waei v1.0 remains the historical foundation baseline; recovered25 world content remains `LATER_RECOVERED` and is not relabelled as Taiwan-v1 historical membership.

Next implementation work should target deterministic runtime interfaces/data models behind this contract, not UI polish or legacy MMO services.

Runtime-core interface layer:

- `../docs/RUNTIME-CORE-INTERFACES-R1.md`
- `../tools/stoneage_local_runtime_core.py`

This layer reuses the existing single-player domain/world/runtime/persistence models and adds typed bootstrap loading, state-gated transition ports, region materialization ports, fresh-start factory boundaries and a versioned local session envelope.

Recovered25 concrete profile adapter:

- `../docs/RECOVERED25-WORLD-PROFILE-ADAPTER-R1.md`
- `../tools/stoneage_recovered25_world_profile_adapter.py`

It loads the closed 826-floor provenance-bearing topology, exposes the four hometown starts, and binds state-gated WarpMan transitions only from a verified recovered25 evidence bundle. Raw binding operands are not promoted into the public bootstrap contract.

Concrete recovered25 region payload source:

- `../docs/RECOVERED25-REGION-PAYLOAD-SOURCE-R1.md`
- `../tools/stoneage_recovered25_region_payload.py`

It preserves the real format split: 761 client DAT three-plane floors and 65 supplemental server LS2MAP two-plane floors. Server-only event planes remain absent rather than being synthesized.


Concrete recovered25 local runtime stack:

- `../tools/stoneage_recovered25_local_runtime_stack.py`
- `../tools/stoneage_recovered25_local_runtime_stack_smoke.py`

This composes the closed profile adapter with the real recovered DAT/LS2MAP payload source, all four fresh starts, the three current dynamic state-gated transition bindings and the local session envelope.

Local runtime session coordinator:

- `../docs/LOCAL-RUNTIME-SESSION-COORDINATOR-R1.md`
- `../tools/stoneage_local_runtime_session_coordinator.py`

The coordinator is the intended engine-facing application boundary for new game, continue/save, current-region materialization, ordinary one-cell movement, classic overlap Warp and recovered state-gated dialogue transitions. Ordinary movement still requires an explicit verdict from a validated collision provider; raw recovered map IDs are never treated as self-describing collision metadata.

Current implementation seam: audit and then bind provenance-safe recovered25 collision verdict coverage for the 826-floor materializable runtime world. Rendering-engine selection remains deferred.
