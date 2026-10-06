# Persistent processed-death / ISDIE state R1

Status: CLOSED_BOUNDED_PERSISTENT_PROCESSED_DEATH_STATE.

## Reason

The accepted whole-scan model gates each death on `HP <= 0 && ISDIE == false`.
The existing persistent runtime retained enemy ReLife eligibility, but that is
not equivalent to source `ISDIE`: normal player and pet deaths can also remain
in the battle array after a profit scan, and a later AddProfit must not charge
them again.

## Bounded runtime state

`PersistentBattleState.profit_processed_death_ids` is the modern semantic
projection of entries whose source `ISDIE` is already set. It is independent
from `revivable_dead_participant_ids`.

The state:

- may reference any player/pet/enemy still present in the battle session;
- requires HP == 0;
- rejects ordinary/ultimate battle-exited entries;
- survives ordinary round boundaries and capture removes a captured identity;
- is passed explicitly into `resolve_ordinary_round`;
- is copied into every later profit-boundary snapshot as prior processed death;
- adds newly dead occupied entries only after an observed profit boundary;
- removes identities when ReLife revives them or an ultimate/Exit removes them.

Player Exit also clears this state for an owned pet removed by exact authority
even when that pet was not a prepared round entry.

## Nonclaim

This state does not itself authorize persistent death/charm/loyalty settlement.
The existing event-order pending-profit walk remains unchanged in this
milestone. The next gate is to build source-shaped `ProfitExitSnapshot`
instances for supported canonical SIDE_OFFSET10 boundaries, run the accepted
immutable scan sequentially, and replace supported death penalties with effects
derived only from `processed_death_ids`. Sparse/noncanonical roster mapping
and unsupported command grouping remain fail-closed for that adapter.

## Remote acceptance — 2026-10-06

Exact input `55416079254b542c2c792d2848b6d2a493345335`, tree `3a45d85cca0de26cdc597746f49a1d01655b6216`, passed all
**32/32** triggered workflows. Settlement `37428752934/112154374994` reports
**648 tests**, **19656** immutable scan/model-native comparisons and **384**
bounded Weaken recalculation vectors. Recovered25 region
`37428752792/112154374696` also passed. Artifact `11395837824`, digest
`sha256:6fe85f8dc911fa2854e1d68d5510effdfce87fd671e63d7f7e6374aa5dd6f372`.

The next gate is not another state field. It is a fail-closed binder from actual
canonical SIDE_OFFSET10 profit-boundary snapshots to `ProfitExitSnapshot`,
followed by sequential `resolve_profit_exit_scan()` calls and persistent
accounting derived only from newly returned `processed_death_ids`. Unsupported
layout/grouping must not be silently coerced into the native-shaped adapter.

Acceptance receipt:
`research/recovered/STONEAGE-PERSISTENT-PROCESSED-DEATH-STATE-ACCEPTANCE-R1.json`.

