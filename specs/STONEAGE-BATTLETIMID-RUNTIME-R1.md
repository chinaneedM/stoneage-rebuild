# StoneAge BattleTimid runtime R1

## Scope

This runtime accepts only the recovered25 enemy-AI `PETSKILL_BattleTimid`
population already closed by the reference audit: exact external skill ID 606,
five positive enemybase uses / five templates, FIELD 1, TARGET 6, COST 2,
ILLEGAL 3000 and a present zero-byte OPTION field.

The runtime does not assign an original historical numeric COM1 or assert that
external ID 606 equals the descendant LOW(COM3) pet-skill array index.

## Typed submission

The enemy-AI bridge requires:

- exact callback population `(606,)`;
- exact selected seven-slot identity;
- opposite-side player battle slots 0..9;
- exact recovered row metadata and empty OPTION;
- descendant callback work setup from the current command's FIX powers.

The semantic callback setup applies the fixed descendant work mutations:

- attack power = FIXSTR * 0.7;
- defense power = FIXTOUGH * 0.4;
- WORKQUICK = FIXDEX * 0.8.

If SetMagicPet has prepared current-command powers, those values are the FIX
inputs. Prepared Weaken powers remain outside this first accepted combination.

## Round ordering and RNG

`BATTLE_COM_ATTACK` is only an internal scheduling carrier. BattleTimid
remains a semantic non-normal-attack actor for combo/counter eligibility.

After target adjustment, an executing BattleTimid action requires one explicit
reduced `rand()%100` witness in 0..99. The draw is consumed even when the
physical attack dodges or settles to damage <=1. If sleep/confusion/no-target
suppresses the BattleTimid semantic action before its event path, the caller
must supply `None` rather than an unused draw.

Forced exit occurs only for:

`draw < 15 && final TIMID event damage > 1`.

A successful forced exit is written immediately into the existing ordinary
round exited-slot / exited-participant sets, which prevents later same-round
activity and persists into subsequent rounds.

## Target-kind consequences

For a player target, the battle-local consequence is player battle exit; the
persistent battle therefore terminates as defeat when no non-pet player-side
fighter remains.

For an allied-pet target, the battle-local consequence is pet exit and the
event records the source fact that the owner's default-pet selection must be
cleared. The current single-player persistence schema has no authoritative
`CHAR_DEFAULTPET` equivalent, so R1 does not claim battle-external default-pet
selection persistence.

## Initiative boundary

The source `CHAR_WORKQUICK` mutation is applied only to the current-round
participant snapshot used by initiative ordering. Dodge, critical and counter
probability continue to use the unchanged FIXDEX combat profile, matching the
fixed descendant source split between WORKQUICK and WORKFIXDEX.

## Explicit open boundaries

R1 fails closed for:

- same-side targeting;
- active target DamageReact, including reflect;
- mounted-ride execution;
- BattleTimid combined with prepared Weaken powers;
- forced-exit overlap with lethal physical damage;
- historical libc `rand()` state reproduction;
- original numeric COM1 and original LOW(COM3) array-index identity;
- battle-external owner default-pet selection persistence.

These boundaries are not interpreted as game-design choices. They remain open
because the current evidence/runtime state is insufficient for exact
integration.

## Acceptance gates

The dedicated BattleTimid workflow must pass the bounded model, exact recovered
row probe, typed bridge, ordinary/persistent round tests, and coordinator
end-to-end tests. The ordinary/persistent shared models must also retain all
existing cross-skill regressions. Full recovered25 region and runtime golden
contract gates are required before pressure reclassification.

**BATTLETIMID_RUNTIME_R1 = OPEN_PENDING_FINAL_CROSS_GATES.**
