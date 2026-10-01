# StoneAge enemy AttackMagic action composer R1

Date: 2026-10-01

## Scope

This layer composes the already-closed recovered25 footprint plan with the
already-closed fixed `_FIX_MAGICDAMAGE` core for **enemy AttackMagic**.
It intentionally remains outside `BattleCommand` / ordinary round execution.

The composer models source-visible combat state that the ordinary physical
profile does not carry: elemental magic resistance/training, magic dodge
equipment values, magic-defense percentage, sleep, and ride-pet elemental
attributes.

## Exact RNG contract

The fixed source consumes randomness in this order:

1. one `rand()%100` true-magic proficiency roll per cast;
2. in historical sorted target order, one `rand()%100+1` dodge roll;
3. only when that target does not dodge, one `rand()%20` damage random.

A dodged target therefore consumes no damage random, receives no defense
training, receives no HP damage, and is not entered into the later sleep-clear
set.

## Elemental state and riding

`BATTLE_GetAttr` is reconstructed independently from the physical battle
profile. Without a ride pet it uses fixed earth/water/fire/wind attributes.
With a resolved ride pet it integer-averages rider and pet fixed attributes
element by element, then recomputes the no-element remainder.

AttackMagic ride damage remains the dedicated historical branch:

- ratio comes from **pure** rider/pet attributes, not the averaged damage attrs;
- raw post-penalty magic damage drives defense training before HP sharing;
- the rider-overkill negative-share quirk remains preserved in the closed
  damage core;
- pet HP landing exactly on zero does not unmount in this branch;
- pet HP crossing below zero unmounts and sets PETFALL.

## Fail-closed boundary

The composer requires a `Recovered25EnemyAttackMagicPlan` whose historical
`SortLoc/qsort` order is portable and explicit. Membership-only nonportable
plans are rejected before any RNG/damage execution.

Not yet integrated here:

- command code 2002 admission into `BattleCommand`;
- enemy-AI callback dispatch;
- ordinary round action/event ordering;
- `BATTLE_AddProfit`;
- player death-flag writes and later death settlement.

Those remain the next adapter seam after dedicated composer CI acceptance.

Validation: dedicated workflow **36852504553 = PASS** at
`316ae9a78869acf2cbcf852804ea1d539e0b92b1`. The closed damage-core,
footprint, runtime-index and action-composer tests passed in the same job.

Marker: **RECOVERED25_ENEMY_ATTACKMAGIC_ACTION_COMPOSER_R1 = CLOSED**

## Command-submission seam

The pre-existing `stoneage_attack_magic_model.py` remains the sole owner of
command code 2002 and COM2/COM3 encoding. A new enemy-AI submission bridge
projects an authoritative recovered seven-slot skill selection into that
existing envelope and cross-checks magic/item provenance against the runtime
index. It intentionally does not coerce command 2002 into ordinary
`BattleCommand` yet.
