# Canonical SIDE_OFFSET10 profit-scan runtime binder R1

Status: CLOSED_BOUNDED_CANONICAL_PROFIT_SCAN_RUNTIME_BINDER.

## Accepted input candidate

The binder is intentionally narrower than the modern battle engine. It may run
only when every observed profit boundary is already classified as either:

- ordinary single-hit per-profit boundary; or
- nonlethal BattleModel ID638 command-tail boundary.

It additionally requires one explicit owner on player entry0..4, all occupied
owned pets on entry5..9, enemies on the opposite SIDE_OFFSET10 half, the exact
complete non-mail owned roster, no ride pet, no item-bearing enemies, no
pre-existing battle/ultimate exits, and one occupied non-pet profit recipient.

Pet/party recipients, Combo/counter/BatFly grouping, sparse/noncanonical modern
pet slots, ride/items and lethal638 remain outside the binder.

## Runtime composition

For each supported boundary the adapter:

1. merges the immutable boundary HP/occupancy/ultimate/authority/status evidence
   with persistent all-roster state;
2. reconstructs all ten status counters in the admitted schema;
3. requires boundary `prior_processed_death_ids` to match the sequential
   source-ISDIE state from the preceding whole scan;
4. binds a `ProfitExitSnapshot` and executes `resolve_profit_exit_scan()`;
5. runs `project_profit_exit_status_clear()` for any scan-driven exit clear;
6. carries the scan's still-valid occupied ISDIE entries to the next boundary;
7. exposes the settlement on `PersistentRoundResult.profit_scan_settlement`.

For the initial integration gate, canonical rounds also execute the legacy
pending-profit calculation as a differential oracle. Exact equality is required
only for the deliberately equivalent subset: one profit boundary, no ultimate
flag and no scan-driven status clear. Multi-boundary or ultimate composition is
allowed to diverge because that is exactly where round-wide event-order metadata
can misclassify an earlier death. Persistent accounting is sourced from the
whole-scan result whenever the binder is admitted. Unsupported rounds remain
explicitly on the legacy path and expose `profit_scan_settlement=None`.

This differential gate is temporary safety pressure, not a claim that event
order is authoritative.

## Next gate

After remote validation, add canonical multi-boundary normal-death/ultimate
witnesses and actual Guardian victims, then widen only where original
dispatch-to-profit chronology is independently certified. Lethal638 remains
blocked until a multi-victim command-tail whole-scan witness passes.

## Remote acceptance — 2026-10-06

Implementation `babf091e66192463cc51ac06a51348b8ef010048` passed **31/31** triggered workflows, including
settlement `37430287171/112159300888` and recovered25 region
`37430287204/112159301018`. Settlement ran **653 tests**, replayed **19656**
immutable scan/model-native comparisons and **384** bounded Weaken
recalculation vectors. Final test-only input `f9bc6b1688500987562fda89ab347984ab12a684`, tree
`cf8af0a399453487807976c2681bf841cabd5a5e`, passed settlement `37430504940/112160004965`.

The accepted integration uses whole-scan results as persistent accounting
authority only inside the declared canonical subset. A dedicated regression
locks the source-shaped chronology where an earlier normal pet death must stay
normal even if a later player ultimate removes that pet in the same round.
This intentionally differs from the old round-wide event-order interpretation.

The next gate is original execution evidence: compile a new command-driver
harness covering `BATTLE_Battling` dispatch, BattleModel, actual Guardian
victim resolution and command-tail `BATTLE_AddProfit`, with a multi-victim
tail. Lethal638 remains blocked until that native chronology agrees with the
modern binder.

Acceptance receipt:
`research/recovered/STONEAGE-PROFIT-SCAN-RUNTIME-BINDER-ACCEPTANCE-R1.json`.

