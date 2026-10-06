# BattleModel same-harness exact DamageSub profit-tail audit R1

Status: IMPLEMENTED_ON_ISOLATED_BRANCH; REMOTE_NATIVE_VALIDATION_PENDING.

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
