# Original same registered item: second Finish inventory-capacity gate R1

Classification: bounded later-descendant source execution. Remote acceptance
is recorded separately in the acceptance receipt after Actions succeeds.

The unchanged pinned Gavin `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56` and
Bismarck `999ffdf1d220ec6666eb65339180689c9caf1876` functions create registered
item3 from a synthetic ID1 ten-pair enemy master, retain enemy6 as its owner,
and queue it for player0 through actual original BATTLE_AddExpItem. The same
item then traverses actual BATTLE_Loop (FINISH), BATTLE_Finish, BATTLE_GetProfit,
BATTLE_GetExpGold and original inventory/release and battle Exit/Delete helpers.

| Capacity case | Source-predicted item effect | Presentation |
| --- | --- | --- |
| Existing first empty slot | Item3 remains live, owner becomes player0, first empty slot receives3 | Pickup log/item data; Bismarck also single-slot update |
| Full active player inventory | Item3 released, use0, owner -1, live counter decreases1, no carried reference remains | No pickup log/item data |
| Only final active slot empty | Final active bag slot receives3; item stays live, owner0 | Same as ordinary pickup |

Fillers are explicitly synthetic live unused records beginning at index20,
inside the 256-record native pool. Bismarck active capacity is obtained from
the inherited original-profile CheckCharMaxItem getter; Gavin uses its native
CHAR_MAXITEMHAVE. The fixture checks capacity against the actual Char array.
Equipment and pre-existing live carried slots are preserved. Invalid/stale
carried references in the saved fixture are replaced with valid fillers when
preparing full/last-slot input, rather than mistaken for occupied capacity.
This input preparation is not proof of natural stale-reference reachability.
Unused filler records
are not claimed as naturally created historical objects.

Each capacity runs a no-loot original second-Finish control followed by the
with-loot replay from identical complete fixture snapshots. The entire native
256-item table, all seven Char records and complete BATTLE bytes are compared.
Independent expected mutations are limited to bag slot/owner on acquisition,
or use/owner/live counter on full-bag release. The no-loot control must preserve
the entire input item pool. Every real Finish must release the arena, set mode
NONE and return Total_BattleNum to0. Full-bag carried references are scanned.
The comparison retains actual EXP/level/pet/status/Exit effects; it does not
constitute an independently derived EXP formula.

GNU99 O0/O2 nonrecovering UBSan must agree on complete output for both profiles.
The source-free report must contain exactly six distinct capacity witnesses,
one paired optimization record per profile and the capacity resolution marker.
The report validator rejects missing/duplicate rows, inconsistent ownership,
missing whole-domain/dispatch checks and invalid pickup counts. Prior factory
native execution and 53 Python regression/evidence-validation checks remain
required. Only harness snapshot storage and a documented 64 MiB native stack
budget are adapted; original gameplay function bodies are not rewritten.

No first-release historical identity, natural enemy/item master or probability,
original transport, real clients, unique-code/time generation, callbacks or
modern-game implementation is established by this gate. Pressure remains
2486 = 2465 bounded closed + 18 OPEN + 3 historical UB, zero promotions.

Next: dead/invalid/non-player/duplicate pending reward boundaries in the same
second-Finish chain; retain distinct original release/reference behavior and
source-profile differences before making modern ownership design decisions.
