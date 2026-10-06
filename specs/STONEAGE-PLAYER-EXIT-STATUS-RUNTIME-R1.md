# Player ultimate Exit late-status runtime bridge R1

Status: LOCAL_VALIDATED; exact remote runtime acceptance pending.

## Concrete correction

The accepted ordinary and continuation player-ultimate paths reset six base
statuses and carried HP, while NocastRoundOverlay retained Nocast/Barrier/Weaken
counters, visit flags and prepared Weaken powers. Persistent precommand
preparation skips exited entries, so this storage could remain indefinitely.
The earlier isolated scan model did not change those drivers.

NocastParticipantRuntime.after_player_exit_status_clear now implements the
shared admitted late-counter/cache projection used by both the native-matched
scan model and real runtime Exit. NocastRoundOverlay.after_player_exit binds
an explicit owner and full non-mail carried roster; selection and occupancy
are not substitutes for ownership. It rejects missing roster records and
unmodeled active statuses, and preserves NC notification state.

The ordinary register_ultimate_exits path applies this projection at actual
player Exit before any later prepared actor. The outer continuation consumer
applies it from actual player exits returned by the multihit resolver before
later prepared actors. Existing internal multihit base/HP handling is retained.
This is not a native certificate of all late-status interactions inside the
continuation's hit loop. Pet-only ultimate and normal player death do not
trigger the player-wide clear. Unrelated character overlays remain intact.

## Persistent attributes and carried state

The persistent boundary clears the complete owned roster, including dead
pets absent from preparation and retained exited selected pets. It rebuilds
work_quick using preserved session baseline powers through the accepted
resolve_weaken_recalculation(counter0,barrier0) seam. It never treats a
prepared participant's previous Weaken-reduced powers as the new baseline.
Cached Weaken powers are removed, so participant_snapshot restores its original
session attack/defense/quick or its independent SetMagicPet/Vary view. Existing
SetMagicPet prepared powers are preserved; this bridge does not certify their
full Exit-time complianceParameter reconstruction or any expiry/cache overlap.

This is modern DESIGN using the accepted baseline and narrow recalculation
model. Original CHAR_complianceParameter internals, equipment/suit/ride and
other status/power interactions are not newly certified. The native scan
certificate clears all ten statuses and ISDIE; the modern schema still excludes
active deep poison/unmodeled statuses and fails closed on the latter.

## Validation

15 new actual ordinary/persistent/continuation regression tests cover clear
visibility before a later actor, both selected and unselected rosters, inactive
and retained pets, cached attribute restoration, preserved independent buff,
pet-only ultimate/normal death non-clears, missing roster and immutable failure.
643 exact settlement/shared status regressions PASS locally. The existing
19656 scan/model native comparisons PASS. The existing Weaken source audit
reproduces128 original Other_DefcharWorkInt recalculation vectors per pin,
384 total, plus its callback/probability gates under ASan/UBSan. These are
replays of existing native cases, not a new full-command bridge.
Required settlement CI now reproduces all these gates and uploads both reports.

## Remaining work

The whole-scan resolver is still isolated: no damage-event penalty path was
replaced by this correction. Next bind actual HP/ISDIE/entry/roster snapshots
and processed-death accounting at ordinary per-hit and638 command-tail
boundaries. Execute original full dispatch/hit-to-profit chronology, actual
Guardian victims and multi-victim batches before lethal638 admission.
Original build/version membership, pet/party EXP, sparse profit roster mapping,
items/ride/wider features, automatic638 AI and specific golden/region/pressure
remain OPEN. No new positive slot or overall percentage is promoted.

## Remote acceptance — 2026-10-06

Exact accepted head `0425028d5965c76d34106a427c4a47f4a56f620b`, tree
`c84d46c6b1e8140579bffdaa950ba12c44505778`.
All triggered gates passed: main **33/33 SUCCESS**, synchronized work branch
**31/31 SUCCESS**. Main settlement `37425651218/112144564632` ran 643 tests,
replayed 19656 immutable-scan/model-native comparisons and 384 bounded Weaken
recalculation vectors. Golden `37425651031`, Taiwan gameplay
`37425651183`, and recovered25 region `37425651071` also passed.

Status is **CLOSED_BOUNDED_ACTUAL_PLAYER_EXIT_LATE_STATUS_RUNTIME_BRIDGE**.
This does not widen the historical/native claim. The next runtime boundary is
the accepted whole-scan model itself: capture the actual ordinary per-hit and
BattleModel command-tail state, then settle new death/charm/loyalty changes only
from scan `processed_death_ids`. The existing event-order pending-profit walk
must not be used to authorize lethal638. Full command-native chronology,
actual Guardian/multi-victim witnesses, pet/party recipients, sparse original
roster mapping and wider features remain OPEN.

Acceptance receipt:
`research/recovered/STONEAGE-PLAYER-EXIT-STATUS-RUNTIME-ACCEPTANCE-R1.json`.

