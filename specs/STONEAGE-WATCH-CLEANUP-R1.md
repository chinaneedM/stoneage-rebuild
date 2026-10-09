# Original watcher Stop and task-loop cleanup R1

Status: LOCAL PASS; exact remote acceptance PENDING. Zero runtime promotions.

This gate extends the accepted enemy-slot/watch-list gate with original default
BATTLE_WatchStop, Stop/StopSet, FinishSet, CountAlive and Loop bodies at the same
three pinned descendant commits. Original Finish, DeleteBattle and WatchUnLink
remain unchanged, including the first-only watcher deletion defect. Original C
stays transient; repository artifacts contain derived hashes/results only.

## Domain and independent witness

9,225 cases per profile/optimization cross all 205 ordered physical placements
of one root plus zero through three watchers in five fixed slots, three watcher
actor states (live player, dead-flagged player, pet), representative entry slots
0/4/9 and five actions: direct root Finish, schedule root Finish, schedule root
Stop, WatchStop last actor, WatchStop all watcher actors. Three snapshots record
immediate state and two subsequent original Loop scans. Every use/mode/link,
entry, actor work index/mode/watch type, battle count, processed count and ordered
Profit/Exit/DeleteItem/discharge/message trace is compared to an independent
Python list/state oracle. This does not establish legal full-Exit player slot9.

55,350 native comparisons =3 profiles x9,225 cases xO0/O2 GNU99 with
nonrecovering UBSan. 76 tooling/domain/regression checks. Twelve transient native
mutations (skip empty-watch Finish scheduling; skip WatchStop Exit, each profile
and optimization) must be detected by the oracle. Original source trees remain
clean. The prior complete 576 lifecycle and 263,268 Exit-mode reports must be
reproduced byte-for-byte; the new report must match its staged local bytes.

## Bounded facts

- Direct root Finish still leaves an immediate residual chain with at least two
  watchers. Original Loop subsequently detects the now-empty watcher slots,
  schedules Finish, dispatches it in the same slot visit and deletes those nodes.
  One subsequent scan suffices in this domain.
- If root Finish runs inside an ascending physical-array scan, empty residual
  watcher slots already visited remain until the next scan. All tested empty
  residues are cleared by the end of the second scan. This is a task-scan bound,
  not a wall-clock timing or permanent-resource-leak claim.
- WatchStop calls Exit, party discharge, message and BU send without deleting or
  unlinking the battle node. An emptied watch node is reclaimed by later Loop.
  Bismarck additionally clears CHAR_WATCHBATTLETYPE; gavin/iris do not.
- Root Stop exits/profits its own actors and deletes its own node; it does not
  traverse and exit linked watch actors. Living player watchers remain used in
  this controlled state. Dead-flagged/pet-only watchers are empty for CountAlive
  and are reclaimed. No claim is made that living watchers persist forever.

These extend the earlier immediate-residue observation rather than correcting
or deleting it. The preserved original Finish traversal remains defective; the
tested task loop provides a separate later empty-node cleanup path.

## Controlled dependencies and OPEN boundaries

Symbolic constants/ABI, compatible structs, fixed five-slot arrays and valid
acyclic pointers; one actor per node; controlled character identity/type/death
getters; generic Exit removes the actor entry, sets FINAL and work battleindex=-1;
Profit, item cleanup, party discharge, network/logging and rand are controlled.
The WatchBC dependency returns0; unrelated active battle/watch modes abort if
unexpectedly reached. Full original Exit is NOT executed in this new gate.

OPEN: full Exit with actual end-data/item-end and post-destroy ticket/warp;
watch creation and failures; multi-actor party/follow/ownership; other modes;
slot reuse, corrupt pointers/cycles, concurrency and real scheduler timing;
original executable/build/ABI/PRNG/JSS/Taiwan-v1 equivalence; persistent runtime
and typed631/635 coordinator admission. Pressure stays2486=2465 closed capability
+18 OPEN+3 historical UB;0 promotions. Next priority is complete original Exit
with actual character lifetime guards, then remaining ownership/stat/property/
timer interactions and watcher creation/multi-actor admission.
