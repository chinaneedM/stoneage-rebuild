# BattleModel dispatch-tail profit splice native audit R1

Status: CLOSED_BOUNDED_BATTLEMODEL_DISPATCH_TAIL_PROFIT_SPLICE_NATIVE.

## Purpose

Bridge the gap between the accepted isolated BattleModel hit components and the
accepted isolated whole-scan profit model without overstating a full
`BATTLE_Battling` execution.

The transient C oracle compiles exact pinned original bodies for:

- `BATTLE_BattleModel`;
- `BATTLE_BattleModel_ATTACK`;
- `BATTLE_BadStatusAllClr`, `_BATTLE_Exit`,
  `BATTLE_PetDefaultExit`, `BATTLE_UltimateExtra`,
  `BATTLE_NormalDeadExtra`, `BATTLE_AddExpItem`, and
  `BATTLE_AddProfit`.

It separately verifies the original Battling case contains
`BATTLE_BattleModel(battleindex,attackNo,myside); break;`, verifies the
command-tail `BATTLE_AddProfit(battleindex,aAttackList)` anchor, and verifies
BattleModel itself contains no internal AddProfit.

Because the raw case text is conditionally compiled inside the full
`BATTLE_Battling` function, this splice does **not** transplant or claim to
execute that case body. After the static anchor check, it directly executes the
exact original `BATTLE_BattleModel` body and then the exact original
`BATTLE_AddProfit` body in the source-observed case→tail order. Executing the
full Battling case in its native function context remains a stronger later gate.

## Controlled Guardian seam

This milestone does **not** compile original `BATTLE_AttackSeq` into the same
program. Its guardian output is controlled:

- with Guardian enabled, the first hit requested at owner slot0 redirects to
  occupied pet slot5 while the pet is alive;
- after that pet is killed, the second hit against the same requested target
  resolves to the owner;
- both DamageSub writes therefore occur before the one tail AddProfit scan.

The existing physical native audit independently certifies original
AttackSeq/GuardianCheck selection. Combining the two certificates is useful
evidence, but is not yet a single-harness full command-driver certificate.

## Native/modern comparison

Three controlled vectors per source profile are compared against the already
accepted immutable ProfitExitSnapshot model after the BattleModel hit batch.
The primary multi-victim vector requires damage routing pet→owner, then tail
scan order owner slot0→pet slot5. A repeated AddProfit must not duplicate death
processing.

No original source is committed.

## Completion boundary

This audit may close only the dispatch-tail splice. Full
`BATTLE_Battling` body execution with original GuardianCheck/AttackSeq in the
same harness remains OPEN. Modern lethal638 remains blocked until that stronger
native composition is available and matches the canonical runtime binder.

## Remote acceptance — 2026-10-06

Exact input `da3512edb89877d0761fde7ddbe083f03237dd0e`, tree `16220e2ffa4da9e9bce8321eb3b8c0952fcb6163`, passed settlement
`37433803780/112170605599`. The run reports **653 tests**, **19656**
original PvE profit/exit cases, **19656** immutable scan/model-native
comparisons, **384** bounded Weaken recalculation vectors and **9/9** new
dispatch-tail splice witnesses across the three pinned profiles.

The accepted witness proves that the exact original BattleModel planner/helper
can execute all selected hit effects before the one exact original tail
AddProfit whole scan, including a controlled Guardian pet→owner multi-victim
batch. It also records two source-critical harness corrections:
`BATTLE_TargetCheck(-1)` is a normal absent-Guardian probe, and the
`BCF_*` constants must preserve their original bitmask semantics.

This is not full Battling execution and not same-harness original GuardianCheck.
Those remain the next native gate; lethal638 remains disabled.

Acceptance receipt:
`research/recovered/STONEAGE-BATTLEMODEL-PROFIT-TAIL-SPLICE-ACCEPTANCE-R1.json`.

