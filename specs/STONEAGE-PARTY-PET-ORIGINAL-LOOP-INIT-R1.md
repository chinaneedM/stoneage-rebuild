# Bounded original descendant BATTLE_Loop INIT dispatch R1

**Status: REMOTE PENDING.** Extract the actual BATTLE_Loop original
function from both exact pinned descendants and insert it into the
previously accepted original battle CreateVsEnemy / Init / Exit/Delete harness.
The driver calls BATTLE_Loop once per battle rather than Init directly.

Only BATTLE_MODE_INIT is in scope. Command, finish, stop and watching
branches are out of scope with fail-closed test doubles and must not
be interpreted as completed combat or actual gameplay loops.

Gate: real-header original battle pool with exactly one live INIT arena;
call original BATTLE_Loop and assert return1; mode becomes BATTLE,
original Init/PreCommand state and own-pet ownership are preserved,
followed by successful original Exit/Delete and pool cursor0,1,2,0.
Two pinned profiles, O0/O2 and nonrecovering UBSan.

Bismarck's BATTLE_CHECKINDEX and optional NETWATCH/BATTLE_TIME are profile
specific. Inherited bounded network packet sinks and disabled optional Lua
battle start callback remain explicit limitations. Full BATTLE_Command,
Finish, victory, profit, network payload, JSS1999/Taiwan-v1 equivalence OPEN.
