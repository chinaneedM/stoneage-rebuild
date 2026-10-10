# Source-profile real-header party + selected-pet negative matrix R1

Status: **REMOTE PENDING**. This gate extends accepted successful
real-header party/pet CreateVsEnemy / Exit / Delete / repeat harness, without
modifying original descendant function bodies or committing source/headers.

Test input is a single original eligible encounter with controlled healthy
leader player0, teammate player1 and allocated owned pet2. Eight distinct
preconditions are applied one at a time to the live original-source
CreateVsEnemy and BATTLE_Exit / ExitAll / DeleteBattle path:

- healthy teammate and selected owned pet;
- teammate busy, not battle-admissible;
- teammate in FINAL mode: Gavin excludes, Bismarck may admit;
- owned pet present but DEFAULTPET = -1;
- DEFAULTPET points to an empty owned slot;
- selected owned pet HP = 0;
- selected owned pet has ISDIE flag;
- allocated pet2 remains live but roster ownership is unlinked.

Expected observations explicitly separate battle occupancy, roster ownership,
default-selection normalization and experience reset. Eight cases per
optimization per pinned source profile; optimization-specific native traces
must match. Full real-header structs, exact pinned descendant code, source
preprocessing, original master-loader and three-slot arena/cursor must remain
in use; all traces generated in a transient Actions job.

This tests bounded synthetic preconditions, *not* natural character lifecycle,
win/loss, profit, original transport, original server bootstrap, other party
size/multi-pet compositions, or JSS 1999 / Taiwan v1.0 identity. Distinct
Gavin/Bismarck gate behavior must not be merged or promoted before remote
evidence supports it. Next stage is original Init/TaskLoop/Finish with
separate full-state and source-profile gates.
