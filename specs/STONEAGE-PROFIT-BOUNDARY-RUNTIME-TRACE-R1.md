# Profit-boundary runtime trace R1

Status: IMPLEMENTED_ON_ISOLATED_BRANCH; REMOTE_VALIDATION_PENDING; settlement consumption OPEN.

## Purpose

The accepted immutable PvE profit/exit scan cannot be driven from final round
HP or damage-event order. The modern round driver must expose the state that
exists immediately before each candidate AddProfit boundary, while keeping
ordinary per-hit and BattleModel command-tail grouping distinct.

This trace is observation only. It does not authorize death/charm/loyalty
charges, does not alter the existing persistent pending-profit walk, and does
not admit lethal ID638.

## Typed snapshot

`OrdinaryProfitBoundarySnapshot` records:

- the modern driver boundary kind and chronological trigger-event indexes;
- HP by battle slot and actual non-exited occupancy by slot;
- round-local BENT ultimate bits, separate from HP;
- the explicit set representing already processed death/ISDIE chronology;
- exact `DefaultPetExitAuthority` owner/selection/roster/occupancy state;
- current base-status runtime and the late Nocast/Barrier/Weaken overlay.

Snapshots are copied/frozen at capture time. Player ultimate boundaries are
captured after BENT flag writes but before the existing immediate Exit mutation,
so the future whole-scan adapter can observe the dead owner and still-occupied
paired pet exactly at the boundary.

## Grouping

The existing ordinary single-hit path is labeled `ordinary_per_hit`.
BattleModel ID638 records one `battlemodel_command_tail` snapshot after all
admitted callback hits, matching the accepted static fact that BattleModel has
no internal AddProfit and the command driver invokes AddProfit after dispatch.

Current counter and BatFly grouping are deliberately labeled
`*_current_driver`; those labels are not a native chronology certificate.
Combo is recorded as one command-tail group. Full original command-driver
composition is still required before any unsupported grouping becomes
settlement authority.

## Next gate

Bind each supported snapshot to a `ProfitExitSnapshot` built from persistent
session/roster state, carry source ISDIE across profit calls, execute
`resolve_profit_exit_scan`, project admitted status clears/recalculation, and
replace new death/loyalty charges with `processed_death_ids`. Fail closed on
unsupported boundary kinds or state/occupancy mismatches. Only after original
dispatch/hit-to-profit chronology, actual Guardian victims and multi-victim
command-tail witnesses pass may lethal638 be enabled.
