# Original battle released-slot reuse after PET2 carried alias — R1

Status: **REMOTE VALIDATION PENDING**. Source-free native audit and strict witness
validator are on branch `agent/original-released-slot-reuse-r1-20261011`.
Do not classify this as a proved historical runtime result until Actions,
derived artifact byte checks, independent oracle review and main integration pass.

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

## Evidence classification

- **FACT (already accepted, bounded):** original guard scans a configurable
  character-index range without a raw PLAYER/PET type predicate; at
  `getFdnum()==2` an artificial PET2 carried alias does not prevent
  release of the original displaced item; independent original allocator
  tests showed index reuse under artificial occupancy.
- **HYPOTHESIS (this new connected test):** released original item8 can be
  reallocated as new ID2 while PET2 still carries index8; the same original
  guard should prevent release and reuse when PLAYER0 carries8.
- **OPEN:** naturally reachable battle PET carried aliases, natural free-pool
  occupancy/cursor trajectories, actual configuration, callbacks and consumer
  dereferences, generation-aware ownership/unique identity, actual Taiwan-v1/
  JSS build membership, full original transport and real client rendering.
- **DESIGN:** no policy for the modern inventory/ownership engine is set by
  this adversarial test. In particular, preserving a historical stale pointer
  would not automatically be appropriate for a new single-player engine.

Pressure remains at the previously accepted 2486 = 2465 bounded closed +
18 OPEN + 3 historical UB. No semantic promotion or new historical UB
classification is authorized on the basis of this pending probe.

Execution entry point:
`python -m tools.stoneage_battle_original_released_slot_reuse_audit`
with the same three pinned source directory arguments used by the adjacent
original guard workflow.
