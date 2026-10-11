# Original invalid pending item tickets R1

Classification: bounded pinned later-descendant execution, with remote acceptance
recorded separately. Original gameplay functions remain unchanged. Zero historical
or pressure promotion; this is not a modern ownership design decision.

The accepted original enemy6/item3 factory and AddExpItem chain runs first.
New explicit pending-ticket inputs then traverse a separate actual
BATTLE_Loop(FINISH)/Finish/GetProfit/GetExpGold/Exit/DeleteBattle. Whole original
_ITEM_CHECKINDEX, _ITEM_endExistItemsOne and BATTLE_DeleteItem bodies are matched
against each pinned profile's preprocessed source and hashed. Prior capacity,
exceptional recipient/duplicate and actor/side controls remain required.

| Case | Ticket index | Explicit input |
| --- | --- | --- |
| 0 | 249 | Unused inactive pool record; original check rejects it |
| 1 | 3 | Actual original release of registered item3 before queuing its stale index |
| 2 | 256 | First index beyond the complete 256-record pool |
| 3 | 2147483647 | INT_MAX |
| 4 | -2 | Negative below sentinel -1 |
| 5 | -2147483648 | INT_MIN |

The inherited factory phase has logical pool size8 despite its256-record backing
array. These new cases explicitly set logical size256 in BOTH replays, then
restore the inherited size;249 is therefore in range and inactive,256 is the
first out-of-range index. An initial audit assertion caught this fixture-size
assumption before remote publication; no original source defect is claimed.

Each input runs a no-ticket control and a with-ticket replay from identical
complete snapshots. Case1 executes the actual release function in BOTH replays;
its use0/owner-1/count decrement belongs to input preparation, not settlement.
The prepared whole pool is snapshotted after release. Settlement must leave all
256 item records and the live count unchanged, match all seven complete Char
records and complete BATTLE bytes against its original no-ticket control, produce
zero pickup logs/aggregate/single-slot sends and zero carried references to the
invalid ticket index. All actor equipment and bag slots are scanned. Every arena
must release, mode NONE/Total_BattleNum0, and all pending tickets become -1.
The negative indices are cleared by EntryInit even though deletion only considers
nonnegative tickets. No unchecked array access is introduced into the fixture.

Actor0 is alive PLAYER, PLAYER-type side index0, empty carried bag, GETEXP0;
enemy6 opposite, accepted winner sentinel/null callbacks. Original Exit timers
and all eight native connection records retain fixed time1000/rand0 and
CreateTime900/duration0: one timer/draw, Gavin BDTime1000, Bismarck1005 with its
unchanged original delayTime5 and typed NU(fd7,0) once. Typed transport observes
arguments/counts only. Differential EXP/Exit is not an independent XP formula.

Two source profiles, six cases, two replays and O0/O2 nonrecovering UBSan yield
48 NEW Finish executions:24 controls and24 ticket replays. Retained capacity24,
cleanup32 and actor/side64 executions also run. Complete output equality across
optimizations is required. The report validator requires12 new unique witnesses,
all30 predecessor witnesses, paired optimization records and every resolution.
77 Python evidence-completeness/regression checks and an independent original
item-factory native run remain required. The 64 MiB audit stack affects audit
execution only. Original source/headers/assets are transient and never committed.

Pressure remains2486=2465 bounded closed+18 OPEN+3 historical UB. Natural stale
or out-of-range ticket generation, masters/probability, early JSS1999/Taiwan1.0
server identity, positive gold/config, unique/time callbacks and actual transport
remain OPEN. These invalid-ticket cases establish rejection and eventual clear,
not naturally reachable bad states or arbitrary-pointer safety.

Highest NEXT: ordered mixed valid/invalid ticket sequences and pending-slot
positions through original second Finish: verify that invalid slots do not block
later valid pickups, preserve duplicate/alias outcomes and complete domains.
Special NPC variants remain a separate OPEN source domain.
