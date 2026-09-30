# Recovered25 Server Collision Provider R1

## Scope

This runtime component exposes provenance-safe ordinary movement collision
verdicts for the portion of the materializable recovered25 world that is
covered by recovered server LS2MAP plus recovered `mapset.txt` metadata.

Artifacts:

- `tools/stoneage_recovered25_server_collision_provider.py`
- `tools/stoneage_recovered25_server_collision_smoke.py`
- `tests/test_stoneage_recovered25_server_collision_provider.py`

It is composed into `Recovered25LocalRuntimeStack` and consumed by
`LocalRuntimeSessionCoordinator.walk_one_cell_with_server_collision()`.

## Evidence boundary

The provider uses only:

- recovered25 server LS2MAP tile/object planes;
- recovered25 server `mapset.txt` WALKABLE/HAVEHEIGHT metadata;
- the already-closed materializable recovered25 topology.

It does not substitute Taiwan-v1 ADRN collision attributes for uncovered
recovered25 floors.

## Coverage contract

The closed census establishes:

- materializable floors: 826;
- server-collision closed floors: 635;
- explicit uncovered floors: 191;
- no-server-map floors: 189;
- divergent server duplicates: 2 (5540 and 31001);
- dimension mismatches: 0;
- missing recovered mapset metadata: 0.

All 65 resolved supplemental floors are server-collision closed. The remaining
gap is confined to the stable/client-DAT side.

## Fail-closed rules

A floor is usable only when:

1. a recovered server LS2MAP payload exists;
2. all copies for the embedded floor ID are byte-identical, or there is only
   one copy;
3. recovered dimensions match the active runtime topology;
4. every tile/object image ID used by the floor resolves in recovered
   `mapset.txt`.

Divergent duplicate payloads are never selected by path ordering. Uncovered
floors raise an explicit runtime error rather than returning a guessed verdict.

Selected payloads are re-hashed when loaded. Runtime dimension drift is also
rejected.

## Movement semantics

`ordinary_step_verdict()` delegates to the already-established descendant
collision model:

- object WALKABLE mode 0 blocks;
- mode 1 defers to tile WALKABLE;
- mode 2 forces static walkability;
- flying uses HAVEHEIGHT;
- diagonal movement checks orthogonal side cells;
- dynamic destination occupants remain an explicit caller input.

The session coordinator then feeds the resulting verdict into its existing
one-cell movement path, which continues to own classic overlap-Warp behavior.

## Remaining gap

This provider intentionally does not claim complete 826-floor movement
coverage. The 191 uncovered floors require a separately versioned recovered25
client-side collision bridge or additional provenance. That bridge must be
proven against recovered25 client resources/code/data and must not inherit
Taiwan-v1 ADRN semantics merely because both families use three-plane DAT map
caches.
