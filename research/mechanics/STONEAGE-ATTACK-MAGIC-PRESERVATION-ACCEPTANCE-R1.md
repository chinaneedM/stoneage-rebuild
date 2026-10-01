# StoneAge recovered25 AttackMagic preservation-bundle acceptance R1

Date: 2026-10-01

## Purpose

The deterministic unit/integration chain already closes recovered25 enemy
AttackMagic from `wa[]` AI selection through command 2002 and persistent round
execution. This acceptance adds a bundle-backed witness using the recovered
runtime data itself.

## Witness selection

The local-runtime smoke does not hard-code an enemy ID. It scans recovered
encounter/group/enemybase/petskill data and requires one candidate that:

- belongs to a stable encounter area without unresolved positive group refs;
- is reachable by a group eligible with the empty witness inventory;
- has TACTICS=1 without the unresolved `rn` extension;
- has a positive `wa[]` weight on a real `PETSKILL_AttackMagic` slot;
- resolves that AI choice against the player target;
- produces an exact portable one-target AttackMagic footprint at execution.

The smoke derives the corresponding group roll, enemy selection roll and AI
mode roll from the recovered weights, spawns the actual recovered enemy, then
passes it through `LocalRuntimeSessionCoordinator`.

## Battle-state boundary

The witness supplies an explicit battle-local zeroed `AttackMagicRoundOverlay`
only as test input; the coordinator never synthesizes it. This is intentional:
the current player-save model still lacks a reconstructed authoritative mapping
for the four magic-resistance levels and **defense-magic experience** counters
consumed by the enemy-attack path. Later fixed descendants additionally persist
four attack-magic proficiency levels and four attack-magic experience counters;
those are a separate future player/pet caster seam.

The acceptance requires a real command-2002 target event and verifies that the
overlay returned by the persistent round is carried into the next battle
context.

Expected report marker:

`ATTACKMAGIC_ENEMY_AI_ROUND_WITNESS|1|portable=1|target_events=1|overlay_carried=1|round_turn=1`

Validation: preservation-bundle workflow **36856905249 = PASS**. The verified
bundle was recovered successfully, all materializable maps passed, the concrete
runtime-stack witness passed, AttackMagic cross-links passed, both server and
client collision audits passed, and the workflow committed the derived report
as `11cb491b2f97876cd4fb88b837226a5b717f9401`.

The generated report contains the exact marker:

`ATTACKMAGIC_ENEMY_AI_ROUND_WITNESS|1|portable=1|target_events=1|overlay_carried=1|round_turn=1`

Marker: **RECOVERED25_ATTACKMAGIC_PRESERVATION_BUNDLE_ACCEPTANCE_R1 = CLOSED**
