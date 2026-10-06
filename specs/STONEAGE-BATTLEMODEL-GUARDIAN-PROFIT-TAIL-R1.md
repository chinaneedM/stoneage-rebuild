# BattleModel same-harness original Guardian profit-tail audit R1

Status: CLOSED_BOUNDED_SAME_HARNESS_ORIGINAL_GUARDIAN_PROFIT_TAIL_NATIVE.

## Purpose

Remove the largest remaining seam in the accepted dispatch-tail splice:
controlled Guardian routing.

The transient C program starts from the accepted exact BattleModel→tail
AddProfit splice and replaces its controlled `BATTLE_AttackSeq` with the same
exact pinned original reduced physical function set used by the separately
accepted physical audit:

`BATTLE_FieldAttAdjust`, `BATTLE_AttrCalc`, `BATTLE_AttrAdjust`,
`BATTLE_DamageCalc`, `BATTLE_GuardAdjust`,
`BATTLE_CriticalCheckPlayer`, `BATTLE_CriticalCheck`,
`BATTLE_CriDamageCalc`, `BATTLE_GuardianCheck`, `BATTLE_DuckCheck`, and
`BATTLE_AttackSeq`.

These bodies execute in the **same transient program** as exact original
`BATTLE_BattleModel`, `BATTLE_BattleModel_ATTACK`, and the exact original
feature-off PvE AddProfit/exit whole-scan bodies.

## Bounded profile

Feature-off, SIDE_OFFSET10, no ride, no equipment, neutral field,
`_BATTLE_NEWPOWER`, controlled external getters/notifications and controlled
`BATTLE_DamageSub`. Status application/presentation remain controlled.
No original source is committed.

Guardian registration is real BattleArray state. The owner entry has a
registered pet guardian, and the guardian carries the original Guardian flag.
The original `BATTLE_GuardianCheck` decides the candidate.

A deliberately sharp two-hit vector keeps source ISDIE false until command-tail
AddProfit. Therefore the original GuardianCheck can still return the zero-HP
guardian on hit two; however BattleModel's own post-AttackSeq TargetCheck sees
that guardian is no longer a live target and directs the actual DamageSub to the
requested owner. This chronology must be observed, not guessed from final HP.

## Acceptance

Three vectors per source profile must pass:

- Guardian, owner HP1, pet HP1: first actual damage pet, second owner, then one
  source-order tail scan processes owner slot0 before pet slot5.
- Guardian, high owner HP, pet HP1: pet dies while owner survives.
- No Guardian, owner HP1: owner takes the first actual damage.

Native post-hit HP is bound to the independently accepted immutable
ProfitExitSnapshot model; ISDIE/death/charm/loyalty state must match. Repeated
AddProfit remains idempotent.

## Nonclaim

This is not full `BATTLE_Battling`, and `BATTLE_DamageSub` is still a
controlled seam even though it is separately native-certified. Lethal638 stays
disabled. The next gate is same-harness exact DamageSub, followed by full
Battling case execution if conditional source context can be retained without
modifying original bodies.

## Remote acceptance — 2026-10-06

Exact input `93bd7fa550eaa99137015109237b78a67815c1fd`, tree `f97009c53238724f362847003976b26595c719d5`, passed settlement
`37436034852/112177967610`. The run contains **653 tests**, **19656**
original PvE profit/exit cases, **19656** immutable scan/model-native
comparisons, **384** bounded Weaken recalculation vectors, **9/9** prior splice
vectors and **9/9** new same-harness original Guardian vectors.

The accepted trace closes the controlled-Guardian seam: the exact original
reduced physical function set through GuardianCheck/AttackSeq now executes in
the same transient program as exact BattleModel/helper and exact tail AddProfit.
It also pins the subtle pre-ISDIE behavior where a zero-HP guardian can still be
returned by GuardianCheck, while BattleModel's post-AttackSeq TargetCheck
decides whether that candidate actually receives DamageSub.

The source battle flags are now imported verbatim from pinned battle.h macros:
Guardian `1<<3`, ABIO `1<<6`, NODUCK `1<<7`. This correction rejects an
earlier transient false-ultimate path caused by synthesizing ABIO as a getter
key.

Next gate: exact original DamageSub in this same harness, then full Battling
case-body execution. Lethal638 remains disabled.

Acceptance receipt:
`research/recovered/STONEAGE-BATTLEMODEL-GUARDIAN-PROFIT-TAIL-ACCEPTANCE-R1.json`.

