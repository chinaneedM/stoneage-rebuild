# Original battle released-slot reuse after PET2 carried alias — R1

Status: **REMOTE ACCEPTED BOUNDED**. Action 38140069870 / job 114471937741
SUCCESS at tested branch commit 87f5af8df2873afb1c52589febf5a5a5d2abd431.
All ten validation steps (plus setup/post steps) passed; 171 Python tests;
2 pinned source profiles × O0/O2 × three alias inputs = 12 connected
native executions. 1076 predecessor ACTUAL rows byte-exact; six new rows.
The separately downloaded artifact ZIP (34844 bytes) SHA256
`b6e188a84a274a8278eaadfaa5a5f586a1c7a20e40438b08254fd8a7ec3539e9`
matched GitHub's artifact digest. Full report (643637 bytes) SHA256
`bb0d3d01f1c02373293b649786532a1e54c20a6b6231f444bbeb9252a069c66a`
was recovered from the verified native log with exact Git blob hash
`b7c69c7af9a299bc0b55ece69026fcb5be073e65`; committed source-free.
Independent original item factory report (32466 bytes) SHA256
`ae632bc03bf06ca1661e4ba0d151595f9ccd075d0c1eb67d5b3acb22b5e8ff59`
remains byte-exact with the previously accepted factory gate.

## Question

Can the original item factory allocate into an index that the unchanged original
`BATTLE_AddExpItem` just released despite a stale carried reference in an
owned PET whose index is excluded by the configured `getFdnum()==2` scan?
Compare against the same assignment without an alias, and against an alias in
the in-range PLAYER0 which invokes the original deletion guard.

This composes the accepted, independent facts of original item release,
range-based deletion protection and original allocator slot reuse; the new
claim must be supported by a **single connected native execution**, not by
inference across older fixtures.

## Execution boundary and input construction

- Source profiles: pinned Gavin `1f90cb6` and Bismarck `999ffdf1`;
  GNU99 original bodies under both `-O0` and `-O2`, nonrecovering UBSan.
  Source/preprocessed body equality is mandatory. Original source/assets and
  per-run compiled files are transient only.
- First retain *all* prior original battle assignment, payout, guard and
  independent factory witnesses unchanged.
- Reuse the already executed original enemy6 creation and its actual
  item8..11 objects (ID1,2,1,2), without rebinding or resetting the
  function-static original item allocator cursor.
- Repeat a single `BATTLE_AddExpItem` on the original two eligible
  PLAYER entries0/1, empty pending reward slots, controlled concentrated raw
  RNG to recipient0 and replacement of original item8. Expected pending
  `11,9,10`; exactly six native assignment draws.
- Three independently restored input cases: no alias; owned PET2 carries8
  in its second nonequipment slot; PLAYER0 carries8 in that slot.
  `getFdnum()==2`; `CHAR_playernum==2`; the original actor types and
  PET ownership remain unchanged.
- Only **after** the real original release/guard decision, explicitly mark
  other inactive item records occupied and account for them in the synthetic
  live-item count. This makes index8 the sole available candidate in the
  no-alias/PET cases, rather than attributing a natural allocation sequence
  to the original distribution. Record the number of synthetic blockers.
- Invoke unchanged original `ITEM_makeItemAndRegist(2)` as the second factory
  operation. The old index8 contains ID1 bytes before allocation; new ID2
  content permits differentiation of physical index from item identity.
  No caller writes to the original static cursor.

## Oracles / refusal conditions

The candidate must prove the actual assignment's release call, warning count,
pending tickets and item8 live/owner state in all three cases before factory.
The factory must produce an auditable success/failure index, exact
construction RNG calls, count delta, old/new item identity and owner, and
*unchanged* other 255 item records. All seven Char records (including both
carried references), full arena, eight connection records, original ID and
profile-specific indirect tables remain byte-equal across factory operation;
no extra release or diagnostic is allowed. Synthetic fixture restoration must
be explicit. The raw emitted witness has a strict profile/alias matrix and no
unrecognized or duplicated fields.

All predecessor `ACTUAL` report lines must remain **byte-exact** and
in-order. A pass requires two compiler optimizations and the complete retained
regression gate; independently produced artifact(s) should be downloaded,
digested, and checked before promotion to `REMOTE ACCEPTED`.

If any predicted original result differs, preserve the actual observation
and revise both the oracle and the claim rather than altering original bodies
or weakening complete-state requirements.

## Accepted observed results

| Synthetic alias | Original replacement result | Factory result | Surviving reference | Native diagnostics |
| --- | --- | --- | --- | --- |
| None | item8 released once | new ID2 allocated at index8 | none | 0 |
| Owned PET2 index2 | item8 released once | new ID2 allocated at index8 | PET2 carries stale index8 | 0 |
| In-range PLAYER0 index0 | item8 retained; guard warning1 | full pool, allocation returns -1; original ID1 stays enemy-owned | PLAYER0 still carries8 | Gavin1 / Bismarck2 extra factory diagnostics |

For each original factory run, 244 other previously inactive pool slots were
explicitly occupied as synthetic blockers after actual assignment. The
original static allocator cursor was *not* reset. Factory operation changed
no other item record, no actor or arena state, no connections, and no table.
All complete-state oracles held. Factory-generated full-pool diagnostics
must be distinguished from the original battle deletion-guard diagnostic.

## Evidence classification

- **FACT (already accepted, bounded):** original guard scans a configurable
  character-index range without a raw PLAYER/PET type predicate; at
  `getFdnum()==2` an artificial PET2 carried alias does not prevent
  release of the original displaced item; independent original allocator
  tests showed index reuse under artificial occupancy.
- **FACT (newly accepted, bounded):** released original item8 was reallocated
  as ID2 while PET2 retained index8; PLAYER0 alias instead preserved the
  original ID1 and blocked reallocation, on both tested descendants and
  both compiler modes. Physical index reuse does not establish stable
  item identity. This is a *synthetic adversarial* case, not natural reachability.
- **OPEN:** naturally reachable battle PET carried aliases, natural free-pool
  occupancy/cursor trajectories, actual configuration, callbacks and consumer
  dereferences, generation-aware ownership/unique identity, actual Taiwan-v1/
  JSS build membership, full original transport and real client rendering.
- **DESIGN:** no policy for the modern inventory/ownership engine is set by
  this adversarial test. In particular, preserving a historical stale pointer
  would not automatically be appropriate for a new single-player engine.

Pressure remains 2486 = 2465 bounded closed + 18 OPEN + 3 historical UB.
No first-release historical promotion or new UB classification is authorized.
Next: investigate naturally reachable alias paths, ownership lifecycles and
unique-code / early object identity; remain in original reconstruction.

Execution entry point:
`python -m tools.stoneage_battle_original_released_slot_reuse_audit`
with the same three pinned source directory arguments used by the adjacent
original guard workflow.
