# Bounded original descendant BATTLE_Loop INIT dispatch R1

**Status: REMOTE ACCEPTED (bounded INIT-only dispatcher).** Extract the actual BATTLE_Loop original
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

## Original native evidence — 2026-10-10

GitHub Actions [38033745806](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/38033745806), job114159804380 SUCCESS; 10 workflow steps and 12 Python regressions. Exact native test input `c1649d27036c8f7e27b680d871989d270b48dec9`, tree `5a3b3563469a7ff3cf9b79249f7dcc0b0da46b21`. Original BATTLE_Loop source (no edited dispatcher body) runs four isolated INIT dispatches per profile per O0/O2; 16 original dispatches total. Per-profile output equals accepted direct-Init trace byte for byte across O0/O2: Gavin `362fcd9ee1d3c1536bc1950dd8b7121d53c089ffcd614bfc6ccc0ada5e08bcfe`; Bismarck `4e3acec05e99f92bdff7e606b90e050ced7833b1a495693f4f6be24ce9990807`.

Gavin's original active arena use gate and Bismarck's original BATTLE_CHECKINDEX were retained. Bismarck original NETWATCH stage BATTLE_Init is admitted in a narrow predecessor watch collector; no real monitor/server is claimed. No BATTLE_Command call: its branch was NOT exercised. Inactive arms stay fail-closed (or retain existing predecessor originals without a caller). No real attack rounds, Finish, victory, profit or open-ended server loop acceptance. Source/headers remain ephemeral.

Accepted receipt: `research/recovered/STONEAGE-PARTY-PET-ORIGINAL-LOOP-ACCEPTANCE-R1.json`. Derived artifact11663298054, GitHub metadata SHA256 `1ab9b437115567155c985c40c3ddf2dc0ae931121d6ed28537f38341f09f5be9`; ZIP not independently downloaded.
