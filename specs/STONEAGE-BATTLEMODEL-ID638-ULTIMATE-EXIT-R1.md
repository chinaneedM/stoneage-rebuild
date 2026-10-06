# BattleModel ID638 ultimate/Exit command-tail bridge R1

Status: LOCAL_VALIDATED_REMOTE_PENDING (2026-10-06).

## Admitted runtime scope

`lethal_ultimate_exit_profit_base_round_empty_equipment_ID638_R1`

The coordinator still re-admits the typed ID638 submission against the current
template, skill slot, loaded row digest, work powers and participant identity.
The pre-existing nonlethal and normal-death scopes continue to reject ultimate.
Only an ultimate flag attached to a newly lethal ID638 victim is admitted;
living reflected flags and unrelated later ordinary deaths remain rejected.

The round driver carries each hit's `ultimate_kind` into one pre-profit
command-tail boundary. All HP/ultimate writes finish before settlement. Exit
side effects then follow source slots 0..19, independently from hit order.
Persistent accounting comes from the canonical immutable whole scan.

The critical witness writes Guardian pet5 HP before owner0 HP. AddProfit scans
owner0 first, requests default-pet Exit and then player Exit. The player clear
restores dead carried pets to HP1 and removes their occupancy before slot5 can
charge a separate pet death or clear the default selection. The selection stays
at slot0. A standalone pet ultimate instead clears selection to none.

## Exact original full-driver differential

`tools/stoneage_battlemodel_ultimate_profit_tail_source_audit.py` reuses the
accepted exact full Battling / GuardianCheck / AttackSeq / DamageSub /
BattleModel / AddProfit / Exit program. Original function bodies remain
unchanged except mechanical symbol renames for observation wrappers.

The work carrier matches recovered ID638: type5, four objects. Status text,
effect matching and presentation remain neutral controlled seams; the source
planner/helper/physical/HP/death/Exit chronology executes natively. This does
not certify the complete recovered OPTION or historical packets in that C
harness. ID638 OPTION/template identity remains independently gated by the
existing runtime admission.

There are 16 scenarios per pinned profile, 48 overall:

- ordinary deaths, direct ultimate2 and accumulated-overkill ultimate1;
- owner/pet both lethal, mixed normal/ultimate victims, owner-only and pet-only;
- default selection present or absent, and no-risk on/off.

The actual first AddProfit boundary captures pre-profit HP and ultimate flags.
Exactly one profit call must come from full Battling. Its final HP, ISDIE,
death counts, charm, pet variable-AI, default selection, dead-pet count and
occupancy match the direct immutable scan and canonical runtime binder.
Native death and Exit request order also match. A repeated AddProfit must
preserve the entire native character/work/flag/pet/validity/battle state.

The three original full Battling body hashes remain the hashes recorded in
`STONEAGE-BATTLEMODEL-FULL-BATTLING-PROFIT-TAIL-R1.md`. All existing reduced
driver helper seams and the DamageSub wrapper's presentation-input zero seed
remain explicit and unchanged.

## Local validation

- 661 related runtime/unit regressions PASS, including ID638 persistent and
  coordinator player ultimate, Guardian owner-first, standalone pet clearing,
  accumulated ultimate1, and rejection of ordinary deaths outside the scope.
- 48 exact-original full-driver / canonical-binder comparisons PASS across
  gavin, iris and bismarck clean pinned repositories.
- Existing source gates remain mandatory in the settlement workflow.

## Remaining gates

No recovered positive slot is promoted here. The next evaluation must audit
the exact recovered payload and both templates against BattleModel-specific
golden, region, hash-pressure and runtime-stack admission requirements before
promoting either placement. Automatic AI selection, original active build and
version membership, ride/equipment, broader recipients and scheduler/status/
packet history remain OPEN.
