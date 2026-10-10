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

Pass conditions: four full CreateVsEnemy→Loop INIT→Loop Command WAIT→
ExitAll/Delete and battle arena reuse (cursor 0,1,2,0) in each profile
and O0/O2; nonrecovering UBSan; no turn increment, no new packet sends,
no actor index/party/pet ownership changes. All original potential
AI/Battling/rescue/timeout transport dependencies are fail-closed
boundary adapters, not proof of actual battle action execution.
Bismarck NETWATCH BATTLE_Command stage is explicitly admitted
only for a live arena; original Bismarck time and offline-profile
branches remain source-specific.

Next gates: actual submitted player/pet commands, enemy AI target/intent,
time-outs, full attack round, death, Finish and profit. This gate does
not assert any victory/reward or first-party JSS/Taiwan-v1 equivalence.
