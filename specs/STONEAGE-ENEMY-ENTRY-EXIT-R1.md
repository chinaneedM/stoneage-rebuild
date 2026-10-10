# Actual-header preserved enemy Entry / Exit / destruction / reuse R1

Status: bounded remote acceptance at tested HEAD
178356adaed50d1bd6c8b170eac297259895d6af, Action38023653829/job114129802080.
164 regressions and11 full report cmp gates pass; ordered logs and independently
downloaded artifact match. Evidence applies to two pinned descendant sources and
their current compile profiles, not original released builds or JSS/Taiwan-v1
runtime admission. Receipt: STONEAGE-ENEMY-ENTRY-EXIT-ACCEPTANCE-R1.json.

## Executed composition

The accepted real-loader and object-registration gates are composed with complete
original `BATTLE_NewEntry`, `EntryInit`, `BATTLE_BadStatusAllClr`, `_BATTLE_Exit`,
party update, checked flag accessors and actual empty-registry character/item
destruction. Actual original Char/Object/BATTLE/BATTLE_ENTRY/map headers and
transitive include closure are used. Gavin's complete profession initializer is
linked; the executed enemy-type guard returns before player profession handling.
Original StatusTbl/MagicTbl bodies, functions, headers and file hashes are pinned.
Original source, headers and configured master data remain transient outside repo.

Two original world-player constructors register object0/1 and the original map
list `[0,1]`. They remain alive while preserved ordinary enemy4 is created,
entered, exited/destroyed, rejected by dead-slot guards, and recreated in slot4
with original sequence progression. The second enemy repeats Entry/Exit.

FACT within the tested configuration:

- Original Entry takes the first empty position on either enemy-configured side,
  sets bid=`position+side*10`, clears its getitem/escape fields, sets character
  battle index/mode/side/command fields and invokes original bad-status clearing.
  Actual compiled INIT is1 and FINAL is6. Prior symbolic-fixture mode ordinals
  remain fixture labels; they are not substituted for these actual enum values.
- Complete enemy Exit removes its entry, clears escape, stores FINAL6/index-1,
  releases original carried/pool item slots through empty-registry guards, and
  invalidates the character slot. Repeated Exit and Entry on the dead slot return
  original CHARAINDEX error6. Rebirth reuses slot4 and restores the accepted birth
  work/flags, with the next original sequence number.
- Enemy object/ticket/start work remain0 after original Entry and Exit. Original
  owner search stays-1. The two world players, named world object fields and all
  four map cells remain unchanged. No enemy world registration is inferred.
- Gavin executes the post-destruction nonparty/ticket tail, including one fixed
  clock call per successful enemy Exit; stale ticket work reads0, so no warp is
  reached. Bismarck's explicit liveness guards skip that tail and clock entirely.
  The two source behaviors are preserved rather than normalized.

## Controlled inputs and observable coverage

Gavin reads its same-pin setup-selected unmodified master bytes. Bismarck reads
those bytes with its own original loaders as cross-profile input only. Both use
the accepted1,532 ordinary unequipped variants, levels1/20 and four raw Rand modes.
Natural cases deterministically cover both sides/all ten entry positions. Another
20 cases/profile/optimization seed positive values in fields expected to clear,
and set die/attacked flags, after observing the original birth. These are separate
controlled dirty-status cases, not naturally loaded combat state.

Positive character partitions2/2/3, a live single battle, initialized entry holes/
occupant markers, floor1/2x2 map and original16MiB pool dimensions are controlled.
Actual full encounter/battle-array bootstrap/`BATTLE_CreateVsEnemy` is not invoked.
The existing walk/watch/detached-node reclamation adapters remain declared. Clock
uses a fixed1000 collector. Original freeMemory/free-list reuse is not executed.

Unreachable player/pet/party/notification/warp/profession dependencies have exact
original-header-compatible aborting definitions. Unexpected traversal fails the
probe. Their existence does not validate those excluded branches. The complete
original Entry/Exit bodies are compiled and execute through the ordinary enemy
path; this does not claim execution of every actor or branch of those bodies.

The independent oracle checks named birth stats/identity/HP/exp/ticket/object,
birth sequence/RNG, original flags, six rejection guards per birth and dead-slot
guards, selected entry fields, unchanged battle neighbors/world players/map cells,
all initialized character data/string retention, and complete ordered work deltas
over captured birth vectors. Native scans every work field; sparse records retain
zero-valued changes and reject duplicate/out-of-range indexes. All other work
fields must remain unchanged. Recreated birth work/flags must equal the first.
This differential oracle is not an independent all-field birth oracle. Only five
initialized Object fields are read; unspecified constructor fields/padding remain
unobserved. Full named streams must match between O0/O2.

## Gate

Run `tools.stoneage_enemy_entry_exit_audit` with the same three fixed source roots.
Expected49,024 natural+80 dirty cycles,98,208 births/successful Entries/successful
Exits,196,416 complete work-delta/stage comparisons and785,664 rejection-guard
calls across two profiles and O0/O2 GNU99 `-fgnu89-inline` nonrecovering UBSan.
Twelve safely executing semantic mutations must fail the oracle: Entry bid/object,
status clearing, Exit mode/entry removal and character-slot invalidation. Ten
predecessor complete reports must reproduce unchanged. Accept exact-input Actions,
compare complete ordered reports and append continuity/acceptance records before
integrating. No original C or data is published.

## Remaining scope

Actual higher-level `BATTLE_CreateVsEnemy`, battle-array bootstrap/Finish and
player/pet/special/party/watcher compositions remain OPEN. So do original
reclamation/bootstrap, Iris Windows encoding, nonempty callbacks/equipment,
remaining actor/watcher/typed631/635 and original ABI/build/JSS/Taiwan-v1.
Pressure stays2486=2465 closed capability+18 OPEN+3 historical UB;zero runtime
promotions. This gate does not begin modern engine/content implementation.
