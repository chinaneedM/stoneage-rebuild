# Immutable bounded PvE profit/exit scan model R1

Status: LOCAL_VALIDATED; exact remote input acceptance pending.

## Scope and evidence

The prior seven-function native certificate is
STONEAGE-PVE-PROFIT-EXIT-NATIVE-AUDIT-R1. This independently implemented
adapter is tools/stoneage_profit_exit_scan_model.py. It neither imports native
source nor calls the audit expectation. Original C stays transient. The
--verify-scan-model audit compares all recorded chronological writes and final
native fields to both the existing independent witness and this new adapter.
Local19656 model/native comparisons pass,6552/profile at the same clean pins.
No new original C cases are claimed: these are new model comparisons against
the already accepted19656 injected native snapshots.24 new unit tests plus
prior535 related regressions pass (559 total).

The model admits feature-off PvE dpbattle0 SIDE_OFFSET10, one explicit player
owner, a complete ordered contiguous non-mail pet roster (up to five original
slots), no ride/items and a single valid occupied non-pet profit recipient.
Party, pet profit recipients, mail and extension configurations have no input
schema and are not admitted. The native comparison matrix uses two pets, one
enemy, owner positions0/4, both sides, two risk modes, selected absent/paired/
carried identities, normal/ultimate/prior ISDIE/alive cases and three single-
player enemy EXP level points. Broader combinations are not native-certified.
Roster ordering preserves original slot indices within this contiguous domain;
sparse original pet-slot arrays need a distinct mapping before admission.
All character/status arithmetic is bounded int32; overflow is rejected.

## Contract

ProfitExitSnapshot freezes character and authority maps. Each character binds
actual occupancy, HP, separate ISDIE/ultimate bits, counts, pending EXP and ten
explicit status counters. Selection is nullable and independent of paired
occupancy. ProfitExitCharacter uses semantic battle modes, not original numeric
ABI. Delta fields are helper requests, not final clamped loyalty/charm values.
A caller supplies a controlled elder destination or absence; the result emits
warp requests and performs no external warp or network action.

resolve_profit_exit_scan settles exactly one caller-chosen profit boundary.
It reads side0 then side1, ascending slots, with earlier writes visible to later
entries. It emits processed_death_ids, status_cleared_ids and ordered effects.
Only processed deaths increment counters or request penalties. Owner exit
removes paired occupancy, heals/clears the non-mail carried roster and may
suppress later pet deaths. Pet ultimate clears current owner selection before
a later player's penalty lookup. Repeated scans preserve pending EXP without
new death effects. Player-selected helper exits, independent paired removal
and roster cleanup remain separate operations. A live ultimate flag is not a
death event. An already marked death is not processed again.

Caller identity is an explicit actual entry. The adapter does not infer an
attack target, Guardian target or recipient from damage events. Ordinary per-
hit and BattleModel command-tail boundaries remain caller responsibilities.
No existing ordinary/continuation/state/coordinator driver imports this model;
the current nonlethal638 guards and event-oriented pending-profit path remain.

## Modern status projection

project_profit_exit_status_clear checks the boundary snapshot against complete
base/late runtimes for the cleared owner and carried pets, including inactive
pets. It rejects active deep poison (original field8) and unmodeled active
statuses. Missing/mismatched base or overlay records fail closed. It clears
six base counters plus Weaken/Barrier/Nocast counters, late visit flags and
prepared Weaken powers. Other records are preserved. Native snapshot clearing
includes all ten statuses and ISDIE; modern projection has no deep-poison schema
and never treats an unmodeled-status boolean as permission to erase it.

The projection emits recalculation_required_ids. It preserves work_quick and
other work inputs until a separately bound recalculation occurs; it cannot be
used to certify a command-ready state. NC notification state is preserved,
because the feature-off certificate supplies no feature-on packet semantics.
Visit-flag/cache invalidation is a modern DESIGN consequence of clearing the
source counters, not a claim about original field/packet layout.

## Remaining gates

Wire explicit recalculation and the immutable scan into real command boundaries,
then replace damage-event death charging with processed-death accounting.
Execute original dispatch/hit-to-profit chronology, actual Guardian victim
state and multi-victim command-tail snapshots before lethal638 admission.
Pet/party profit recipients, sparse roster mappings, mail, riding/items,
original build/version membership and penalty helper clamps remain OPEN.
BattleModel-specific golden/full-region/hash-verified pressure and automatic
AI admission remain OPEN. No positive slot or overall percentage is promoted.
