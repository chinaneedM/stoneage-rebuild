# StoneAge AttackMagic fixed damage core R1

Date: 2026-10-01

## Status and evidence role

This layer reconstructs the guarded attack-magic damage path shared by three
pinned descendant source trees:

- gavinlinasd/StoneAge @ 1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56
- iriselia/StoneAge @ 9e6c8ce2cd8ed532a7157773acd1c61582c178b5
- BismarckDD/stoneage @ 999ffdf1d220ec6666eb65339180689c9caf1876

It is descendant implementation evidence, not a claim of launch-era Taiwan 1.0
behavior.

All three pinned builds define their attack-magic guard plus
\`_EQUIT_DEFMAGIC\`, \`_FIX_MAGICDAMAGE\`, and \`_MAGIC_DEFMAGICATT\`.
The R1 model therefore follows the actually enabled fixed-damage branch.

## Recovered25 cross-link closure

Full preservation-bundle validation run **36844577483 = PASS**. Its report
write-back advanced \`main\` to
\`ded5d20debde9ccde2ffd3254be9f7f9c6afbb5d\`.

The recovered25 AttackMagic population now closes structurally end-to-end:

- 25 AttackMagic skill rows / 25 numeric magic-item pairs;
- all 25 magic IDs resolve to \`MAGIC_AttMagic\`;
- all 25 carry a valid attack-magic IDX;
- IDX values are exactly 25 distinct values in **2..26**;
- recovered attack-magic attributes: earth 6, water 6, fire 7, wind 6;
- recovered power range **100..350**, 7 distinct;
- recovered magic levels **1..5**, 5 distinct;
- all 25 explicit item IDs exist in active \`itemset.txt\`;
- all 25 item \`magicid\` values match the paired magic ID;
- all 25 item \`magicusemp\` values are **5**;
- \`attmagic.bin\` has 54 raw records / 27 effective magic indices and all 25
  recovered IDX values have valid adjacent record pairs.

Marker: **RECOVERED25_ATTACKMAGIC_CROSSLINK_R1 = CLOSED**

## Convergent fixed-source execution

The primary AttackMagic path converges across all three pinned descendants.

### Attacker proficiency and cast check

- player: stored elemental magic proficiency;
- enemy: \`int(level * 0.9)\`;
- non-player/non-enemy source branch (commented PET): stored elemental magic
  proficiency and treated as trainable under \`_FIX_MAGICDAMAGE\`;
- one \`rand()%100\` check is made per cast;
- source success condition is \`roll <= proficiency\`;
- a failed cast is still executed, but final damage is multiplied by **0.7**.

### Defender resistance and dodge

Damage resistance:

- player: stored elemental resistance + equipment elemental magic resistance;
- enemy: \`int(level * 0.5)\`;
- PET branch: stored elemental resistance;
- when \`_MAGIC_DEFMAGICATT\` is active and the current resistance is positive,
  the shared magic-defense percentage increases that resistance before the
  Kmagic calculation.

Dodge is a separate per-target random check:

- player threshold =
  \`int(luck*3 + base_resistance*0.15 + equipment_quimagic*0.9)\`;
- every non-player threshold = \`min(int(level*0.2), 30)\`;
- source \`rand()%100 + 1\` dodges when roll <= threshold.

The dodge helper uses the player's base resistance field, not the already
equipment/status-adjusted damage resistance. R1 keeps those two inputs
separate.

### Base fixed damage

For every non-dodged target:

\`\`\`text
Kmagic = proficiency*1.4 - effective_resistance
Kmagic = max(Kmagic, 0)
Mmagic = max(proficiency, 1)
Amagic = (Kmagic^2 / Mmagic^2) + (rand()%20)/100
APower = int(Power * (1 + MagicLv/10) * Amagic)
\`\`\`

The \`rand()%20\` value is consumed only after the target failed its dodge
check.

### Element traction and field adjustment

\`BATTLE_getMagicAdjustInt\` then:

1. reads attacker attributes;
2. multiplies \`MagicLv\` by 10;
3. retains only the selected elemental attack component, with
   \`selected = MagicLv10 + MagicLv10 * (attacker_element / 50)\`;
4. the \`/50\` is integer division;
5. the other elemental slots are zeroed, while the source leaves the no-element
   slot untouched;
6. applies \`BATTLE_FieldAttAdjust\` to attacker and defender;
7. runs the fixed four-element \`BATTLE_AttrCalc\`;
8. multiplies by attacker-field-power / defender-field-power.

The field helper is:

\`0.5 + matching_element * field_att_pow * 0.01 * 0.01 * 0.5\`

or 0.5 when the battlefield has no elemental field.

### Failure attenuation, defense training and sleep

After attribute/field adjustment, a failed cast performs integer
\`damage *= 0.7\`.

For trainable defenders (player plus the source PET branch), defense training
is computed from this post-penalty damage. Hits below 200 damage do not train
resistance.

Only non-dodged targets enter \`def_be_hit\`; those targets later have SLEEP
cleared even when their computed damage is zero.

### Riding damage branch

AttackMagic does not use the ordinary physical ride split.

The rider share is derived from rider/pet pure attributes against the magic
element, then clamped to **2..8 tenths**. The exact source branch contains two
quirks that R1 preserves rather than silently repairing:

- if intended rider damage overkills the rider, the already-negative HP value
  is reused as the temporary rider share before pet damage is calculated;
  pet damage can therefore exceed raw damage;
- pet unmount/PETFALL occurs only when the post-subtraction pet HP is **< 0**;
  landing on exactly 0 does not unmount in this branch.

### Training transitions

Attack-side training runs only when the cast proficiency check failed and the
attacker is in a source trainable branch. The target count is the number of
non-dodged targets. The current element gains \`MagicLv*3*target_count\` exp;
the opposed \`(element+1)%4\` branch loses half that value.

Defense-side training requires damage >= 200. It gains
\`(damage/20)*(MagicLv*2)\` using integer division; the opposed resistance exp
loses 2.

Both functions use strict \`> 100\`, not \`>= 100\`, for the level-up reset.

## Deterministic reconstruction policy

\`tools/stoneage_attack_magic_damage_model.py\` contains pure functions and
requires RNG values from the caller. This exposes source RNG ordering instead
of hiding it behind Python randomness:

1. one cast proficiency roll (0..99);
2. for each target, one dodge roll (1..100);
3. only for non-dodged targets, one damage roll (0..19).

No AttackMagic enemy-AI runtime admission is made in this milestone.

## Remaining boundary

The next execution seam is the \`attmagic.bin\` footprint geometry:
\`BATTLE_MultiAttMagic\` selects IDX*2 or IDX*2+1 by attacker side and expands
single/row/side selectors through each record's 3x5 field matrix. That target
footprint must be modeled and tested before recovered25 enemy-AI runtime can
safely invoke this damage core.
