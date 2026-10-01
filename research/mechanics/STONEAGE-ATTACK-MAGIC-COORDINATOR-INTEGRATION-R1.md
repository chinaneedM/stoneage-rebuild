# StoneAge recovered25 enemy AttackMagic coordinator integration R1

Date: 2026-10-01

## Scope

This layer connects the already-closed recovered enemy-AI `wa[]` selection
through AttackMagic submission and command 2002 into the ordinary persistent
multi-round local battle coordinator.

## Admission

`_build_persistent_enemy_common_batch` recognizes `PETSKILL_AttackMagic` only
when the full common coordinator explicitly enables its closed seam. It calls
`resolve_enemy_ai_attack_magic_submission`, converts the verified COM1/2/3
payload to the round `BattleCommand`, and retains the typed submission beside
the command. Batch validation requires exact equality between command-2002
actors and AttackMagic submissions.

All non-AttackMagic callbacks continue through the pre-existing pet-skill
bridge. Unsupported callbacks remain fail-closed.

## Multi-round magic state

`LocalRuntimeBattleContext` now carries an optional `AttackMagicRoundOverlay`.
The overlay is **never synthesized with zero values**. A caller that intends to
execute enemy AttackMagic must provide authoritative four-element resistance
and training state when promoting the battle to persistent mode.

After each round, `PersistentRoundResult.attack_magic_overlay_after` is written
back to the battle context. Thus defense-magic training and equipment/status
magic modifiers survive into the next round without pretending they already
exist in the player-save schema.

## RNG

The coordinator accepts explicit AttackMagic action rolls and optional
`BATTLE_MultiList` retarget rolls keyed by enemy participant ID. It rejects
rolls for actors that did not select AttackMagic. Whether a selected spell
actually consumes the action RNG remains decided at round execution time,
because an earlier action can kill/alter targets before the spell acts.

## Remaining boundary

This closes recovered25 enemy AttackMagic inside the engine-neutral local
multi-round battle path. The overlay is still battle-local and is not committed
to persistent player/pet storage after settlement; that requires independent
reconstruction of the historical four-element magic-resistance persistence
schema.

Marker: **RECOVERED25_ENEMY_ATTACKMAGIC_COORDINATOR_INTEGRATION_R1 = CANDIDATE**
