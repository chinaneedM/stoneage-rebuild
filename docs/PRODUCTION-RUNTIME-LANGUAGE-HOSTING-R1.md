# Production Runtime Language & Hosting Boundary R1

Date: 2026-09-30

## Status

**CLOSED ARCHITECTURE DECISION.**

This document separates the repository's Python reconstruction environment from the future shipped game runtime. It does not delete or deprecate Python work; it assigns each layer a durable role.

## 1. Repository evidence

At the 2026-09-30 main snapshot used for this audit:

- repository Python files: approximately **1,093**;
- Python tests: **546**;
- probe/scan/audit/extract/census/recovery/lineage/usage-style tools by filename: approximately **404**;
- directly local/runtime/single-player/recovered25-runtime-related Python modules by conservative filename filter: approximately **27**.

The repository is therefore primarily a reconstruction/evidence laboratory with a deterministic runtime reference growing inside it. Treating the entire Python codebase as a future client runtime would collapse two fundamentally different responsibilities.

## 2. Four-layer language boundary

### A. Evidence archaeology and build-time extraction — Python remains authoritative tooling

These include:

- client/server file probes and scanners;
- binary/data format recovery;
- version genealogy;
- source/provenance audits;
- historical satisfiability/reachability investigations;
- one-off recovery utilities;
- generators that convert recovered material into normalized versioned manifests.

These tools may depend on recovered bundle layout, source-language quirks and investigative conveniences. They are not shipped as gameplay runtime dependencies.

### B. Executable reference semantics — Python remains the oracle during migration

The closed deterministic Python models and tests remain an executable specification for:

- stable identity/state types;
- world/topology and movement semantics;
- collision routing and live occupancy;
- versioned local session/save behavior;
- recovered state-gated transition evaluation;
- application facade and semantic intent/update behavior.

A production implementation is not accepted merely because it “looks equivalent.” It must match versioned golden behavioral fixtures generated/verified against this Python reference.

### C. Production deterministic core — standalone C# is the preferred target

The preferred production target is a **standalone engine-agnostic C# library**, not scripts embedded directly into a Godot scene hierarchy.

Reasons:

1. Godot .NET can host C# while preserving the current primary engine-spike path.
2. Unity is also C#-native, retaining a mature fallback without rewriting the deterministic core.
3. MonoGame is C#-native, retaining a high-control fallback.
4. Strong static typing is appropriate for the project's many identity classes, immutable state envelopes, versioned schemas and fail-closed boundaries.
5. The core can be tested without launching any renderer.
6. Engine-specific presentation code remains replaceable.

This is a project portability decision, not a claim that C# is intrinsically more correct than Python.

### D. Concrete presentation engine — downstream adapter only

A future Godot .NET spike should depend on the production C# facade/semantic adapter, not on raw recovered parsers.

If a different engine is later selected, the presentation adapter changes while deterministic domain/state rules remain reusable where the host supports the same core.

## 3. What must not ship by default

The production client should not, by default:

- embed a Python interpreter solely to execute reconstruction modules;
- parse raw recovered StoneAge NPC/server/client bundles at gameplay runtime;
- depend on historical probe scripts;
- expose recovered raw coordinates/arguments directly to presentation code;
- make an engine scene graph authoritative for player/world state.

Python embedding could be reconsidered only after a measured prototype demonstrates a material advantage that outweighs packaging, startup, interop, debugging and distribution complexity.

## 4. Build-time normalized data boundary

Recovered source material should flow:

`raw/recovered evidence -> Python audit/extraction -> versioned normalized runtime artifact -> production deterministic core`

The normalized runtime artifact must preserve:

- schema/profile version;
- evidence role/provenance;
- stable semantic identity;
- enough integrity metadata to fail closed on drift;
- no false promotion of later recovered content into Taiwan-v1 history.

This lets the final game use reconstructed data without carrying archaeology parsers into normal gameplay.

## 5. Cross-language parity rule

Before any C# subsystem replaces its Python reference counterpart:

1. define a versioned golden fixture schema;
2. generate or verify fixtures using the current Python reference;
3. include positive and fail-closed cases;
4. implement the C# behavior independently of a renderer;
5. run C# parity tests against those same fixtures;
6. only then connect the subsystem to an engine adapter.

Golden fixtures should prefer semantic inputs/outputs over Python-internal object representations.

Initial golden scope should cover:

- local session encode/decode;
- ordinary one-cell move: allowed and blocked;
- classic overlap-Warp behavior;
- static + dynamic occupancy resolution;
- local save occupancy delta and legacy compatibility;
- semantic application/engine-adapter intent sequencing;
- state-gated interaction discovery/dispatch using synthetic/public-safe fixtures rather than proprietary recovered payloads.

## 6. Migration policy

Python reference and C# production code may coexist for a long period.

The migration is incremental:

- keep archaeology/recovery in Python;
- close a golden contract for one deterministic seam;
- port only that seam to standalone C#;
- prove parity;
- continue upward/downward as needed;
- do not perform a “big bang” rewrite;
- do not remove the Python oracle merely because a C# path exists.

## 7. Next implementation seam

Create `STONEAGE_RUNTIME_GOLDEN_CONTRACT_R1`: a small, copyright-safe, versioned set of semantic vectors generated/validated by Python that can later be consumed unchanged by standalone C# tests.

This is the prerequisite for a production-language port and therefore comes before Godot-specific scene code.
