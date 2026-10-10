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
tick: with original _BATTLE_TIME enabled, dispatcher tv_sec/tv_usec equal
the current NowTime, while every other byte is preserved. With that feature
disabled every byte is unchanged. All three Char object snapshots remain
byte-equal. A strengthened local assertion exposed this Bismarck dispatcher
clock update; it is retained and asserted, not removed from original code.
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
