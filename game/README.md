# Game

Production engine implementation is still intentionally deferred. The project now has an engine-neutral runtime bootstrap boundary that can be consumed before selecting Godot, Unity, or another engine.

Current implementation-facing contract:

- `RUNTIME-BOOTSTRAP-RECOVERED25-R1.json`
- `../docs/RUNTIME-BOOTSTRAP-CONTRACT-R1.md`

The contract is a **version-tagged reconstruction scaffold**. Taiwan/Waei v1.0 remains the historical foundation baseline; recovered25 world content remains `LATER_RECOVERED` and is not relabelled as Taiwan-v1 historical membership.

Next implementation work should target deterministic runtime interfaces/data models behind this contract, not UI polish or legacy MMO services.
