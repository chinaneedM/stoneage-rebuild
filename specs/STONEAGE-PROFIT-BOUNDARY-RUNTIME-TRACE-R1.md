# Profit-boundary runtime trace R1

Status: CLOSED_BOUNDED_PRE_SETTLEMENT_PROFIT_BOUNDARY_TRACE; settlement consumption OPEN.

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

## Remote acceptance — 2026-10-06

Implementation `6d4298c40fca439d1dcf153b5630c24d3b4de0d6` passed all **31/31** triggered workflows,
including settlement `37427373309/112149996535` and recovered25 region
`37427373349`. Final test-only input `fe9109a7440caa9c10847eb649c01c28b7348075`, tree
`9366032fe3126f062a9cf58d3a5a4b9e1138fec8`, passed required settlement
`37427836728/112151449355`: **646 tests**, **19656** immutable
scan/model-native comparisons and **384** bounded Weaken recalculation vectors.
Final artifact `11395995441`, digest
`sha256:19550e602bb7b6fa2ab337fce14dbb615cc523822a57d830e2a29971e6ea3d36`.

This closes the **pre-settlement trace** only. It does not convert the current
event-order persistent pending-profit walk into source-shaped settlement
authority, does not certify `*_current_driver` counter/BatFly grouping against
the original command driver, and does not enable lethal638. The next accepted
change must bind supported snapshots to the immutable whole-scan adapter and
derive new death/charm/loyalty accounting exclusively from
`processed_death_ids`, failing closed everywhere the original grouping or
roster mapping is not yet certified.

Acceptance receipt:
`research/recovered/STONEAGE-PROFIT-BOUNDARY-RUNTIME-TRACE-ACCEPTANCE-R1.json`.

