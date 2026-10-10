# Original controlled direct lethal hit — runtime candidate R1

**Status: REMOTE ACCEPTED — bounded direct native lethal hit only.** Build from the accepted complete
real-header nonterminal attack driver and both pinned descendant source profiles.
This candidate preserves original Attack/AttackSeq/DamageSub function bodies
and original seven-actor arena, input, guard, and original Exit controls.
It adds one *direct original BATTLE_Attack call* per encounter after restoring the
nonterminal control baseline. Live enemy actor is read from current allocator
side1 slot and round-tripped via original Index2No/No2Index.

The candidate holds accepted calibrated stats/RNG but changes enemy current HP
from 500 to 60, below 73 guarded damage. It separately checks the original
direct attack HP floor at zero and DAMAGECOUNT increment. All actor/arena/RNG
state is restored before original Exit/Delete reuse. O0/O2 nonrecovering UBSan
byte-equal traces and both source profiles are prerequisites. Regression checks
ensure the prior nonterminal attack and guard controls remain intact.

This is *not* a full BATTLE_Loop terminal round. Original death/ultimate/profit
bookkeeping, winning side, FinishSet, Loop/Finish, GetProfit and positive payout
must each be independently connected and proven. The static source preflight
from the prior milestone is not substitute evidence. Candidate remains OPEN
until CI and original observed effects support it. Never promote partial
execution or source-only calls to runtime FACT.


## Verified remote evidence

Actions 38057154113 (17 tests, ten successful steps) and predecessor
38057154180 both pass. Both original pinned profiles reach HP0 from controlled
HP60 and increment DAMAGECOUNT exactly once under direct BATTLE_Attack;
16 direct native calls total across O0/O2 and arena reuse. O0/O2 complete
output traces are byte-equal by profile. This is not a completed lethal
Loop/Battling turn or a claim about FinishSet, winside or positive rewards.
