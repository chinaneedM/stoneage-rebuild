# BattleModel dispatch-tail profit splice native audit R1

Status: IMPLEMENTED_ON_ISOLATED_BRANCH; REMOTE_NATIVE_VALIDATION_PENDING.

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

The harness then executes that dispatch case followed by one command-tail
AddProfit in the source-observed order.

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
