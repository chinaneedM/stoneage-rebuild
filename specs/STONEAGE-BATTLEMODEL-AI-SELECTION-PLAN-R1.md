# ID638 normal enemy-AI composition plan R1

Date: 2026-10-06. Status: DESIGN / NEXT_GATE, implementation OPEN.

The recovered-data runtime golden gate demonstrates explicit typed action
execution on both positive templates. It does not demonstrate normal enemy-AI
selection reaching that action. The latter is a concrete executable gap, not
a remaining archaeology question.

## Current boundary

In `tools/stoneage_local_runtime_session_coordinator.py`,
`EnemyAiCommonCommandBatch` contains no BattleModel submission/action carrier.
`_build_persistent_enemy_common_batch` has no BattleModel-selected callback
branch; its fallback remains `resolve_enemy_ai_supported_petskill_command`.
The explicit `resolve_persistent_attack_wait_round` accepts a typed
`battlemodel_actions_by_participant_id` map and independently re-admits each
submission against the current spawned template, skill population and work.

Do not promote the two placements merely by adding the callback to the global
pressure classifier while this normal-AI composition remains absent.

## Bounded next implementation

1. Add an explicit opt-in ID638 selection seam to the existing normal enemy-AI
   batch/coordinator, preserving source skill column3/runtime index2.
2. Bind selected actors to current recovered templates/OPTION/work and declared
   charset/source profile. Keep the symbolic command and explicit physical/
   ItemCrush/RNG/death scope carriers; no numeric source command invention.
3. Consume hit RNG only for actors that selected this skill. Reject missing,
   extra and unused profile/RNG inputs, as well as unsupported callback IDs,
   grouping or equipment. Existing ordinary skill selection stays unchanged.
4. Exercise selected AI → typed dispatch → persistent command-tail whole scan
   on both exact templates and both charset profiles. Carry the same source
   ordering, status-before-player-clock and default-pet Exit witnesses through
   the real-data concrete stack.
5. Rerun exact-head native, coordinator, golden, region and complete verified
   pressure. Only then evaluate narrowly scoped promotion of the two uses.

Original active build membership, historical packet/presentation, wider
recipients, ride/items and unsupported scheduler compositions remain OPEN.
This plan does not select an engine or introduce MMO services.


## 2026-10-06 implementation checkpoint

The missing carrier/selected dispatch is implemented in the normal common batch
and a bounded opt-in coordinator method. Remote exact-head acceptance is PENDING.
See `STONEAGE-BATTLEMODEL-AI-SELECTION-R1.md`. The former missing-carrier statement
above is retained as the dated starting boundary; it no longer describes code.
Actual active variant census/execution is separate from control AI evidence.
