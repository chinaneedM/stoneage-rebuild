# Native original party/pet command-wait gate R1

Status **PENDING REMOTE**. This extends the previously accepted exact original
BATTLE_Loop INIT dispatcher with a second tick in BATTLE_MODE_BATTLE.
The actual original BATTLE_Command and its original BATTLE_CommandWait
and BATTLE_TimeOutCheck bodies are extracted intact from the pinned
Gavin and Bismarck descendants. Original source files, header files and
master bytes remain transient in CI.

The two actual live players and selected live owned pet remain in original
C_WAIT mode after Init. The original enemy-side CommandWait returns early,
and the original no-timeout condition must block battle AI/actions.

Pass conditions: four full CreateVsEnemy→Loop INIT→three Loop Command WAIT→
ExitAll/Delete and battle arena reuse (cursor 0,1,2,0) in each profile
and O0/O2; nonrecovering UBSan; the three controlled tick offsets are zero,
original BATTLE_TIME_LIMIT minus one, and exactly BATTLE_TIME_LIMIT.
Equality must still wait under the unchanged original strict greater-than
timeout condition. The synthetic NowTime clock is restored before Exit.
Complete BATTLE snapshots must match an exact expected delta after each
tick: Bismarck CommandWait arms PartTime to fixed synthetic wall-clock1000
plus99 even with BeOk zero; it stays1099 through these waiting ticks.
Gavin retains PartTime zero. Every other arena byte and all three Char
object snapshots remain byte-equal. This is a pinned descendant difference.
The new original Command body extraction explicitly binds time(NULL) to
the inherited synthetic audit_time adapter, fixed1000 independently of NowTime;
these tests cover the separate NowTime timeout equality, not wall-clock
PartTime expiration. The initial raw-source _BATTLE_TIME interpretation was
rejected: that block is disabled in the actual preprocessed tested source.
The predecessor's time macro had already been undefined before these newly
extracted Command bodies. A local whole-arena comparison exposed that clock
scope; this gate restores the explicit bounded time macro only around the
three unchanged original Command functions, then undefines it again.
No turn increment, no new Init packet sends,
no actor index/party/pet ownership changes. All original potential
AI/Battling/rescue/timeout transport dependencies are fail-closed
boundary adapters, not proof of actual battle action execution.
Bismarck NETWATCH BATTLE_Command stage is explicitly admitted
only for a live arena; original Bismarck time and offline-profile
branches remain source-specific.

The prior candidate a514ec48 failed during linking, before execution:
CHAR_DischargeParty, lssproto_B_send, szAllBattleString and
BATTLE_OnlyRescue were unresolved. The function-body detector incorrectly
classified an if-condition function call as a definition. This candidate
adds anchored C return-type definition detection, typed aborting adapters
for the two newly exposed timeout dependencies, and source-sized watcher
buffer storage. No original Command body was changed. Original file and
preprocessed extracted function hashes are emitted as derived provenance.

Next gates: actual submitted player/pet commands, enemy AI target/intent,
time-outs, full attack round, death, Finish and profit. This gate does
not assert any victory/reward or first-party JSS/Taiwan-v1 equivalence.
