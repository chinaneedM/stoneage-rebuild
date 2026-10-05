# BattleModel runtime integration plan R1

Date: 2026-10-06
Status: **PREPARATION_ONLY_RUNTIME_OPEN**

The conditional reference and state carriers are accepted. Main is now
`58d4800afb72e4f41f1934395e1cf194133ca75c`, tree
`24702312029248dd46bf72d608864ceac9b6e8a4`. Exact-main replay and the new
native settlement audit must be inspected before a fresh runtime branch.
This plan changes no executable admission or pressure classification.

## Concrete seams

| Seam | Planned change | Required boundary |
| --- | --- | --- |
| New enemy-AI BattleModel bridge | Validate all four callback rows; admit638 only on the two exact slot3 identities | Explicit charset; exact metadata and byte hashes; semantic command only |
| Battle round model | Dedicated BattleModel helper and per-action target/hit RNG bundle | Separate scheduled ordinal from recycled attack-object index |
| Persistent battle state | Forward submissions and RNG; retain HP/status/reaction/ride/ultimate state | Existing schema; independent ownership/default/occupancy |
| Local runtime coordinator | Enable exact callback admission and reject missing/extra actor RNG | Retain ordinary ATTACK only as scheduling carrier |
| Pressure model | Promote two slots after runtime gates and verified data pressure | Reference or native-helper PASS alone cannot promote slots |

## Execution and RNG order

Build one initial opposing living-list snapshot in deterministic slot order,
keeping the original qsort-order caveat. Allocate four attack objects and cycle
101867/101868. This describes scheduling structure, not a permission to move
all random draws before hits. Execute the first min(4,N) hits in order. For each
excess object, consume its RAND(0,N-1) **after prior hit work**, then immediately
execute or skip that selected initial-list target. Coverage passes reuse object
indices but each scheduled helper invocation has its own ordinal/RNG bundle.

Do not rebuild the pool after death, retarget a dead selected target, stop the
remaining selection draws because all targets died, or grant ordinary combo/
counter eligibility. Skipped helper calls own no physical/status draws; an
excess selection still owns its draw even when it selects a now-dead target.
No-live-list entry fails closed instead of inventing RAND(0,-1).

## Post-hit state distinctions

Physical Guardian routing chooses the actual damaged/status recipient. Recheck
target validity before each hit. Restore the BattleModel marker after settlement.
Use reported damage separately from HP loss; consume reflect while preserving
both HP under the accepted base marker branch. Wakeup is independent from the
later surviving-positive-reported-damage status check. Reconcile raw-threshold
ultimate flags on surviving entries using the new settlement audit.

Big5 applies attack70% and paralysis; UTF-8 preserves powers and applies no
matched status. For paralysis, common StatusAttackCheck uses **20-resistance**
with strict roll<probability, despite the caller's hit input30. Existing active
status blocks the shared check before RNG. Use the generic status application
with Range30/scale1/exact turn1. The ordinary physical-status wrapper adds1
turn and uses Range40/scale2, so it cannot be reused unchanged.

Successful paralysis clears the target's remaining-round command immediately.
The ordered round keeps prepared entry commands: writing only command_by_slot
does not necessarily clear that snapshot. Track a semantic cleared-command set
at action execution, following the existing Combined pattern. Test turn1 expiry
before a pending actor acts, and an already-acted target on the following round.

The source pet pre-hit ultimate lookup literally derives side/index from
target+5; it must be audited before using an ordinary owner lookup. A reduced
SIDE_OFFSET10 witness maps submitted pet slots5..9 to opposite entries10..14.
Do not silently normalize that source expression to target-5. Bismarck's
multiplayer offset12 is outside the existing20-slot runtime. Original profile
membership and excluded feature paths remain OPEN.

## Meaningful validation matrix

- Both exact positive templates, wrong row/hash/metadata/graphic/stat/AI/slot,
  unreferenced641/649/650 rejection, and missing explicit charset rejection.
- N1/2/4/5/10 target schedules, action cycling, excess draw/hit chronology,
  first-pass lethal hits followed by skipped sampled targets, owner-flag guard,
  and no-live targets.
- Guardian actual recipient, dead Guardian, dodge/miss/zero damage, critical
  non-player death RNG, defender stone/guard and attacker status setup effects.
- Reflect/absorb/vanish priority and charge exhaustion across repeated hits,
  reported-damage versus HP-loss status eligibility, no-HP-loss ultimate flags,
  rider splits/unmount and subsequent hits.
- Paralysis resistance boundary rolls, preexisting status/no RNG, immediate
  command clearing, later actor tick/turn expiry, already-acted recipient,
  UTF-8 no status RNG, and safe DODGE presentation.
- Persistent settlement, selected/default/owned-pet separation, coordinator
  exact admission, conflicting submissions, extra/missing/unused RNG rejection,
  golden/full-region regression and verified pressure.

Implement after the remaining audit acceptance. Full runtime remains OPEN.


## Settlement acceptance update — 2026-10-06

Supplemental native Action37349075552 completed SUCCESS on33a8e76a.
Its1920 reduced-profile/no-ride calls close only that bounded settlement
contract and supersede the supplemental remote-pending statements above.
Full runtime, mounted composition, literal pet-entry pre-hit guard and
no-HP-loss ultimate flag-to-exit integration remain OPEN.
