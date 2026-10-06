# BattleModel same-harness exact DamageSub profit-tail audit R1

Status: CLOSED_BOUNDED_SAME_HARNESS_EXACT_DAMAGESUB_PROFIT_TAIL_NATIVE.

## Purpose

Remove the controlled DamageSub gameplay-state seam from the accepted
same-harness original Guardian → BattleModel → tail AddProfit witness.

The transient program links, in one process:

- the exact pinned reduced physical function set through
  `BATTLE_GuardianCheck` / `BATTLE_AttackSeq`;
- exact `BATTLE_DamageSub`;
- exact `BATTLE_BattleModel_ATTACK` and `BATTLE_BattleModel`;
- exact feature-off PvE AddProfit/exit whole-scan bodies.

The original Battling case/tail source anchors remain statically verified.
Full `BATTLE_Battling` execution is still a later gate.

## Undefined presentation input

The source BattleModel helper declares `iPetDamage` without initialization and
passes its address to DamageSub. DamageSub reads `*pPetDamage` immediately,
although in the admitted no-ride normal-damage path that initial value does not
determine HP, ISDIE, death penalties or whole-scan ordering.

To make the transient C execution deterministic without modifying the exact
DamageSub body, the harness mechanically renames that body and places a wrapper
at the call boundary. The wrapper seeds only `*pPetDamage=0`, increments an
observation counter, then calls the exact body. This is the same deterministic
input used by the separately accepted native DamageSub audit.

Therefore this milestone is a gameplay-state certificate, not a packet or
historical undefined-value certificate.

## Admitted profile

Feature-off, SIDE_OFFSET10, `_BATTLE_NEWPOWER`, no ride, no equipment,
no active damage reaction, neutral field and a deliberately noncritical DEX
profile. Status/presentation/notifications/getters remain controlled.

All participants use a coherent maxHP and zero overkill accumulator so this
baseline stays non-ultimate. Lethal/ultimate638 is not enabled by this audit.

## Acceptance

Three vectors per pinned profile:

- Guardian, owner HP1, pet HP1: exact DamageSub writes pet HP first, then owner
  HP, and only after both writes does tail AddProfit set ISDIE/death state.
- Guardian, owner HP1000, pet HP1: pet dies, owner survives.
- No Guardian, owner HP1: owner receives the first exact DamageSub write.

Final HP is fed to the accepted immutable ProfitExitSnapshot model and the
native ISDIE/death/charm/loyalty state must match. Repeat AddProfit remains
idempotent.

## Next gate

After exact remote acceptance, attempt the full original BattleModel case inside
`BATTLE_Battling` with the already-closed same-harness physical/DamageSub/tail
components. The undefined iPetDamage presentation value stays explicitly
outside historical certification. Lethal638 remains blocked until full
command-driver chronology is native and matches the canonical runtime binder.

## Remote acceptance — 2026-10-06

Exact input `f804d879cc701b0b29c2d3f2adbd1e2b6df1eddc`, tree `d99b472d1f0e97df01518ae9bae184fe0b4584ac`, passed settlement
`37437282822/112182088944`: **653 tests**, **19656** original PvE
profit/exit cases, **19656** immutable scan/model-native comparisons, **384**
bounded Weaken recalculation vectors and **9/9** same-harness exact DamageSub
profit-tail witnesses. Artifact `11399543542`, digest
`sha256:f01386a4c5b42a701ed4dd54863e5ed554ea70dafa564a1aad806e3bdf00c6cf`.

The exact DamageSub body is unchanged after mechanical symbol rename. Only the
undefined BattleModel `iPetDamage` input is seeded to zero at the wrapper
boundary; this remains outside packet/presentation historical certification.

Next gate: execute the original BattleModel case through the full
`BATTLE_Battling` body in the same transient program, preserving original
conditional context. Lethal638 remains blocked until that full command-driver
chronology matches the canonical runtime binder.

Acceptance receipt:
`research/recovered/STONEAGE-BATTLEMODEL-DAMAGESUB-PROFIT-TAIL-ACCEPTANCE-R1.json`.

