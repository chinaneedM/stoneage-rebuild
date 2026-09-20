# StoneAge Enemy Spawn Count / Birth Orchestration — R1

Date: 2026-09-20

Status: **strong stable-descendant executable reconstruction; Taiwan v1.0/JSS server provenance remains open**

## Scope

This record closes the fixed-descendant encounter composition path between:

encounter area -> selected group -> enemy seat count -> repeated weighted enemy
selection -> enemybase size layout -> per-enemy level and birth-stat creation.

It deliberately separates this from:

- movement-side CEP encounter frequency;
- player/pet command choice;
- enemy battle AI/tactics;
- rewards, drops and victory logic.

## Evidence anchors

Primary fixed descendant:

- gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56
  - gmsv/src/char/enemy.c
  - gmsv/src/include/enemy.h

Independent controls:

- iriselia/StoneAge@9e6c8ce2cd8ed532a7157773acd1c61582c178b5
  - Source/gmsv/char/enemy.c
  - Source/gmsv/include/enemy.h
- BismarckDD/stoneage fixed lineage
  - server/gmsv/char/enemy.c
  - server/gmsv/include/enemy.h

All three preserve the same core CREATEMAXNUM and enemy-size composition
behavior.

## 1. The group is selected before enemy composition

ENEMY_getEnemy first resolves the encounter area and chooses one eligible
group using the area GROUP_PROB weights after item gates.

The enemy list is then built from that selected group's ENEMY_ID / CREATEPROB
slots.

Therefore a historical encounter is not correctly modeled as:

choose one enemy variant -> duplicate it N times.

The fixed core instead performs a new weighted enemy-slot draw for every
enemy seat.

## 2. Effective total enemy-count ceiling

For every defined enemy slot in the selected group, the fixed source adds that
enemy variant's CREATEMAXNUM to createenemynum.

It then computes:

enemyentrymax = min(area ENEMY_MAX_NUM, sum(slot CREATEMAXNUM))

and selects the initial battle count with:

entrymax = RAND(1, enemyentrymax)

Duplicate group slots intentionally contribute CREATEMAXNUM repeatedly.

## 3. CREATEMINNUM is not enforced in this core path

The enemy schema loads both:

- CREATEMAXNUM
- CREATEMINNUM

However, in the inspected ENEMY_getEnemy implementation across all three fixed
lineages, ENEMY_CREATEMINNUM is never read.

This means CREATEMINNUM must remain a declared/source field, but it must not be
silently turned into a minimum encounter count in the reconstructed fixed
core.

This is an important negative fact.

## 4. Every seat re-rolls CREATEPROB

For each seat, the source draws again over the selected group's CREATEPROB
weights.

A selected variant is rejected when its current count reaches:

CREATEMAXNUM * samecount

where samecount is the number of group slots that resolve to that exact enemy
variant.

Therefore repeated identical ENEMY_ID slots are semantically meaningful:
they increase both weighted presence and the allowed count capacity.

Rejected selections consume a loop iteration and the source retries.

## 5. Source retry limit

The fixed loop stops when either:

- the selected count reaches entrymax; or
- loopcounter reaches 100.

The deterministic model preserves the 100-attempt boundary rather than
silently retrying forever.

When deterministic input rolls are exhausted before either source termination
condition, reconstruction raises instead of inventing additional random
outcomes.

## 6. Big-enemy layout rule

enemybase SIZE uses the fixed enum:

- E_T_SIZE_NORMAL = 0
- E_T_SIZE_BIG = 1

For a BIG enemy:

1. at most five BIG enemies are admitted;
2. attempting a sixth BIG enemy decrements entrymax and rejects that draw;
3. if a BIG enemy is selected after the first five output positions, the source
   searches positions 0..4 for a NORMAL enemy;
4. when found, the BIG enemy is moved into that front position and the displaced
   NORMAL enemy occupies the current later position;
5. if no NORMAL enemy is available in the first five positions, that draw is
   rejected and the loop retries.

This is battle-layout orchestration, not a client pet-state field.

## 7. Per-enemy level and birth state

After composition selects concrete enemy variants, each runtime enemy is born
independently.

The already reconstructed descendant birth bridge preserves:

- level RAND within enemy LV_MIN..LV_MAX;
- four independent birth offsets in -2..+2;
- ten independent allocation rolls in 0..3;
- enemybase INITNUM / LVUPPOINT / base growth values;
- derived VITAL / STR / TOUGH / DEX and combat projection.

This means two enemies of the same variant and level can still have different
individualized growth state.

## 8. Executable reconstruction

Artifacts:

- tools/stoneage_enemy_spawn_model.py
- tests/test_stoneage_enemy_spawn_model.py
- tools/stoneage_tw10_25_bridge_model.py
  - PetTemplateBridge now retains optional server-side SIZE as size_class.
- tools/stoneage_singleplayer_battle.py
  - generic enemy_participant_from_spawn_state adapter separates battle
    participant creation from the earlier one-variant EncounterRequest shim.

The spawn model exposes:

- effective_spawn_capacity
- plan_enemy_spawns
- materialize_spawn_plan

All randomness is explicit input.

## 9. Evidence boundary

Strong descendant facts:

- area ENEMY_MAX_NUM caps total encounter size;
- group slot CREATEMAXNUM values contribute to the count ceiling;
- initial count is RAND(1, effective ceiling);
- each seat re-rolls CREATEPROB;
- per-variant count is limited by CREATEMAXNUM times duplicate-slot count;
- generation retries up to 100 attempts;
- CREATEMINNUM is not read by the fixed core generation path;
- BIG enemies are capped at five and preferentially occupy the first five
  battle positions;
- each concrete enemy is born independently.

Bridge/versioned facts:

- recovered mixed 2.5 enemy/group/enemybase rows supply concrete specimen data;
- descendant birth coefficients provide the current executable bridge.

Open:

- exact JSS 1999 / Taiwan v1.0 server composition implementation;
- exact early data rows and SIZE assignments;
- whether any operator build used CREATEMINNUM through a separate code path.

## Consequence

The reconstruction can now represent the actual encounter composition shape:

area
 -> weighted group
 -> random total count
 -> repeated weighted enemy seat selection
 -> CREATEMAXNUM / duplicate-slot capacity
 -> BIG/NORMAL layout
 -> independent level/birth state per enemy
 -> battle participants

This replaces the earlier temporary one-variant-per-EncounterRequest
simplification for full descendant-faithful composition while retaining that
older shim for focused compatibility tests.
