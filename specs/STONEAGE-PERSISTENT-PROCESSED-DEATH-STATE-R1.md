# Persistent processed-death / ISDIE state R1

Status: IMPLEMENTED_ON_ISOLATED_BRANCH; REMOTE_VALIDATION_PENDING.

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
