# BattleModel native profit and exit composition plan R1

Status: CLOSED_BOUNDED_FEATURE_OFF_PVE_NATIVE_COMPOSITION; full command bridge and modern lethal638 OPEN.

## Required composition

The accepted native DEFAULTPET helper audit executes only
`BATTLE_PetDefaultExit` with controlled Exit results. The explicit modern
selection correction does not replace the next native composition gate.

The original PvE death scan is in `BATTLE_AddExpItem`, reached through
`BATTLE_AddProfit` when `dpbattle != 1`. Compile the original dispatcher,
death scan, `BATTLE_UltimateExtra`, `BATTLE_NormalDeadExtra`,
`BATTLE_PetDefaultExit` and `_BATTLE_Exit` together in a transient harness.
Include original `BATTLE_BadStatusAllClr` with the explicitly declared base
`StatusTbl` mapping, so status cleanup is executed rather than assumed.
Derive its extent and `BATTLE_ST_END` from the chosen original header profile;
account for unconditional descendant statuses outside the modern six-status
scope instead of silently truncating the source table.
Keep original function bodies, declare a reduced feature profile, and trap
unexpected item/ride/duel/extension calls. Network, parameter recalculation,
elder lookup and party notifications may be controlled external seams; their
effects are not native gameplay certificates. No original source is committed.

Three clean pins are those in the existing helper audit: gavin1f90cb6c,
iris9e6c8ce2 and bismarck999ffdf1. File hashes and comment-stripped function
window hashes are recorded in
`research/recovered/STONEAGE-PROFIT-EXIT-COMPOSITION-PREFLIGHT-R1.json`.
Window hashes identify static inspection ranges, including intervening
preprocessor directives; they are not hashes of compiled function bodies.

## Static chronology that must be tested natively

The original scan visits side0, then side1, and ascending entry indices on
each side. A valid entry is processed only if HP<=0 and ISDIE is false.
ISDIE and DEADCOUNT are written before ultimate/normal extra handling.
Player Exit can remove a paired pet entry and restore dead carried non-mail
pets to HP1. Those mutations can prevent later scan entries from being
processed. Death events cannot simply be replayed in damage-target order.

Ordinary nonbow and counter command loops have per-hit AddProfit calls.
The guarded BattleModel function has no internal AddProfit call; the command
tail invokes AddProfit after dispatch. These are distinct settlement boundaries.
The accepted nonlethal638 driver avoids relying on a guessed lethal boundary.
Before enabling lethal638, reproduce the dispatch-to-tail boundary and the
whole death scan, including actual Guardian entries and surviving entries
with an ultimate flag. HP/liveness and BENT_FLG_ULTIMATE are separate inputs.

| Native witness | Required observation |
| --- | --- |
| Pet ultimate, later player death on a later profit call | Owner DEFAULTPET is cleared before player penalty lookup |
| Player and paired pet both dead before one scan | Player-first entry cleanup affects whether the pet is processed |
| Separate selected and paired identities | Helper selection and independent occupancy cleanup remain distinct |
| Selected pet absent from battle | Exact lookup/Exit result; no replacement selection |
| Carried dead pet absent from Entry | Player exit heals non-mail roster without inventing an entry |
| Dead entry already marked ISDIE | No second death count or penalty |
| Guardian dies instead of requested target | Scan reads actual entry HP and flags |
| Ultimate flag with surviving HP | No death processing from flag alone |
| Enemy ultimate | Earned kill profit, enemy removal and no duplicate scan |
| Repeated profit call after exit | Stable ownership/selection and no repeated penalty |

Track ordered getters/writes/Exit calls, entry identities, HP, ISDIE,
DEADCOUNT, DEADPETCOUNT, DEFAULTPET, charm, pet loyalty, common status,
battle mode/index and pending EXP. Compare modern state to the native trace
at the same declared profit boundary, rather than only comparing final HP.

## Boundaries and completion

The first harness is a declared SIDE_OFFSET10, non-mail, no ride,
empty-item PvE profile. It must not select the original recovered25 compiler,
feature set, numeric COM1, charset, libc PRNG, multiplayer layout or
JSS/Taiwan-v1 membership. Bismarck's additional guarded branches remain
explicitly excluded until separately audited. Static preflight has zero
native cases and does not close any of these gates.

Accept the bounded native composition on an exact remote input/tree with
source pin/hash checks, relevant ordinary/state/coordinator regressions and
existing native hit gates. Only then isolate lethal638 integration with
native scan boundaries. BattleModel-specific golden, full-region actual-data
execution and hash-verified pressure remain required before positive-slot
promotion. Automatic638 AI selection and equipped/wider features stay OPEN.


## 2026-10-06 bounded native local milestone

The required seven-function feature-off PvE composition now passes19656 native
cases locally at the three clean pins. Original ten-field status table/extent
and ISDIE clear are included. This supersedes zero-native-case status within
that declared profile only; exact remote acceptance remains pending.
Contract: STONEAGE-PVE-PROFIT-EXIT-NATIVE-AUDIT-R1.md. The full command-native
attack-to-profit bridge and modern lethal638 integration remain OPEN.


## Next adapter review after bounded native acceptance

The current common runtime exposes six-status BaseBattleStatusRuntime and
separate NocastRoundOverlay counters for Nocast/Barrier/Weaken. Player ultimate
cleanup resets base status and carried HP, while the persistent overlay path
retains exited participant records and skips their next-visit preparation.
The native ten-field clear therefore needs an explicit overlay transition;
base-status reset alone is not a complete source Exit certificate.

Bind an immutable scan snapshot with actual side/slot identities, HP, ISDIE,
BENT ultimate bits, nullable DEFAULTPET, owned non-mail roster and occupancy.
For638, invoke the scan at command tail after all admitted hits, preserving
mutations from earlier scanned entries. Keep ordinary per-hit boundaries.
The existing event-oriented pending-profit walk cannot supply this grouping
without an explicit scan result/chronology adapter. Only native-processed
deaths may drive new death/loyalty accounting; suppressed paired deaths must
not be charged from an earlier damage event.

Map source counter clears to the overlay counters and visit flags, and audit
prepared Weaken powers/recalculation separately. Original complianceParameter
and notification internals are controlled seams in the native certificate;
no attribute recalculation or packet spelling is certified by that stub.
Deep poison is outside the admitted modern status schema and must stay
explicitly rejected rather than erased through an unmodeled-status boolean.
Native EXP fixtures use a single player recipient and three level-gap points;
pet/party recipients, item distribution and rides require additional native
vectors before expanding the adapter domain.


## 2026-10-06 bounded native remote acceptance

Run37420393572/job112128219849 SUCCESS on c1c3209e/tree777d45a0,
19656 cases,535 regressions and all prior native gates. The earlier static-only/
local-pending snapshots are superseded in the declared feature-off PvE domain.
Full native command-driver bridge, modern whole-scan/overlay integration and
lethal638 are still OPEN under the next adapter review above.


## 2026-10-06 isolated immutable scan adapter accepted

STONEAGE-PVE-PROFIT-EXIT-SCAN-MODEL-R1 now has an independently implemented
immutable whole scan and an explicit modern status-clear projection. Exact
input737da287/tree41fc4788, run37422202059/job112133821223 SUCCESS,
19656 model/native comparisons and560 regressions. No new native vectors.
The next adapter review above is partially closed for this isolated model.

The projection invalidates Weaken cached powers and returns required
recalculation IDs; it does not calculate replacement powers or change the
existing command/state drivers. Active deep poison and unmodeled statuses
are rejected. Bind actual snapshots, perform separately certified
recalculation and consume only processed-death accounting at real profit
boundaries. Then execute full original command-native dispatch/hit-to-tail
chronology, actual Guardian victims and multi-victim batches before lethal638
admission. Pet/party profit and sparse source roster mapping need additional
vectors. Specific golden/region/pressure, original build/version and AI remain
OPEN. Main synchronization/replay is recorded separately in the receipt.
