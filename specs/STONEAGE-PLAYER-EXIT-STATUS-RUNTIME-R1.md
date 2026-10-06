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
