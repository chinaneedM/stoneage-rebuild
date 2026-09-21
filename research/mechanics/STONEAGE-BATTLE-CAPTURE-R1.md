# StoneAge battle capture R1

Status: **strong stable-descendant mechanics reconstruction; exact JSS-1999 provenance remains open**

## Scope

This note reconstructs the ordinary battle capture path separately from kill rewards, escape, death penalties and recovery. The implementation deliberately preserves capture as a non-kill transition: a successful target leaves the battle and becomes an owned pet without first becoming a zero-HP reward corpse.

## Evidence anchors

Primary pinned descendant:

- repository: \`gavinlinasd/StoneAge\`
- commit: \`1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56\`
- relevant files:
  - \`gmsv/src/battle/battle.c\`
  - \`gmsv/src/battle/battle_event.c\`
  - \`gmsv/src/char/enemy.c\`
  - \`gmsv/src/char/pet.c\`
  - \`gmsv/src/char/char_base.c\`
  - \`gmsv/src/include/battle.h\`
  - \`gmsv/src/include/version.h\`

Independent control descendant:

- repository: \`iriselia/StoneAge\`
- commit: \`9e6c8ce2cd8ed532a7157773acd1c61582c178b5\`

The core \`BATTLE_CaptureCheck()\` arithmetic and the pet-copy path converge across these descendants.

## Command and target adjustment

**FACT (stable descendant):**

- \`BATTLE_COM_CAPTURE\` is command code 3.
- the player command wire path uses \`T|<hex target>\`;
- battle dispatch calls \`BATTLE_TargetAdjust()\` before \`BATTLE_Capture()\`;
- \`BATTLE_TargetAdjust()\` retains the submitted target when \`BATTLE_TargetCheck()\` says it is still valid, otherwise it chooses a random valid target from the opposite side with \`BATTLE_DefaultAttacker()\`;
- \`BATTLE_TargetCheck()\` itself checks battle validity/live/attackable state and does not impose the capture-specific enemy/PETFLG gates. Those are applied later by \`BATTLE_CaptureCheck()\`.

The current status-free reconstruction models the live-target/retarget portion explicitly. Status flags such as the source \`ISATTACKED\` and rescue-mode exclusions remain part of the broader status/rescue seam rather than being guessed here.

## Capture eligibility

After any target adjustment, the base capture check rejects the attempt before consuming its capture RNG when:

1. the target is not \`CHAR_TYPEENEMY\`;
2. target \`CHAR_WORK_PETFLG == 0\`;
3. \`CHAR_PickAllPet != TRUE\` and \`attacker_level + 5 < target_level\`.

\`CHAR_PickAllPet\` therefore bypasses the level gate only. It does not make a non-enemy or PETFLG=0 target capturable.

Special required-item checking occurs before the probability check. The pinned Gavin/iriselia builds both enable \`_CAPTURE_FREES\`, which expands later hard-coded required-item conditions. Those quest/private-era tables are kept outside the base formula and represented as an explicit required-item gate; they are not promoted to JSS-1999 rules.

## Probability formula

The stable source reads:

- attacker fixed charm: \`CHAR_WORKFIXCHARM\`
- attacker level
- attacker fixed dexterity: \`CHAR_WORKFIXDEX\`
- attacker fixed luck: \`CHAR_WORKFIXLUCK\`
- target level
- target current HP
- target \`WORKMAXHP\`
- target fixed dexterity
- target base capture value: \`CHAR_WORKMODCAPTUREDEFAULT\`
- attacker's temporary \`CHAR_WORKMODCAPTURE\`
- target sleep state.

Enemy creation initializes \`CHAR_WORKMODCAPTUREDEFAULT\` from enemy-template \`E_T_GET\`. The reconstruction bridge now preserves this source field as \`PetTemplateBridge.capture_default\`.

With \`max_hp <= 0\` normalized to 1, the source computes:

\`\`\`text
hp_term    = 10 - (target_hp * target_hp) / target_max_hp
level_term = attacker_level / 2 - target_level / 2
dex_term   = attacker_fixed_dex / 15 - target_fixed_dex / 15

WorkGet =
    (hp_term
     + level_term
     + dex_term
     + target_capture_default
     + attacker_fixed_luck)
    * attacker_fixed_charm / 50

WorkGet += temporary_capture_modifier

if target_sleep > 0:
    WorkGet += 15

if WorkGet > 99:
    WorkGet = 99
\`\`\`

There is no lower clamp in this function.

The success test is strictly:

\`\`\`c
RAND(1,100) < WorkGet
\`\`\`

Because the comparison is strict, \`WorkGet == 99\` accepts rolls 1 through 98, not 99.

After the attempt path, \`CHAR_WORKMODCAPTURE\` is reset to zero.

## Pet-slot capacity and call order

**FACT (stable descendant):** the capture probability can succeed before the server discovers that the owner has no pet slot.

\`PET_createPetFromCharaIndex()\` calls \`CHAR_getCharPetElement()\`. That function scans the five carried-pet slots in ascending order 0..4 and returns the first empty slot. If all five are occupied, it returns -1; pet creation then fails and the target stays in battle.

Therefore the source order is:

1. item eligibility;
2. target/type/PETFLG/level eligibility;
3. capture RNG;
4. first-empty pet-slot lookup;
5. pet creation.

The reconstruction keeps pet-slot failure after RNG rather than pre-validating capacity and changing random-consumption behavior.

## Successful capture is not a kill

On a successful copy:

- \`PET_createPetFromCharaIndex()\` creates an owned \`CHAR_TYPEPET\`;
- the source copies the enemy's current HP/MP/MAXMP, VITAL/STR/TOUGH/DEX, luck, elements, slot, MODAI, level, status fields, rare, PETRANK, PETID, critical/counter, pet skills, ALLOCPOINT, image and name into the new pet path;
- max EXP is initialized from the captured level;
- owner identity and first-empty pet slot are attached;
- \`CHAR_PETGETLV\` records the capture level;
- capture count increments;
- \`BATTLE_Exit(defindex,battleindex)\` removes the original enemy entry and destroys that enemy battle character;
- pet compliance / AI normalization then runs.

Crucially, the captured enemy is **removed**, not reduced to HP 0. Therefore ordinary kill-profit scanning must not award its EXP or held-item drops.

The current single-player runtime requires a complete provenance-bearing \`PetActor\` at the persistence boundary instead of inventing unresolved copied MP, skill-view, EXP-threshold or AI/compliance values. It validates source variant/template identity plus level/current HP/max HP before atomically installing the pet.

## Implemented deterministic seams

- \`d832b32741ecf6d097be5f4640c55d4dfd4a3720\`
  - stable capture gates;
  - exact formula;
  - strict random boundary;
  - first-empty five-slot behavior;
  - \`enemybase.GET\` bridge;
  - battle-core Action \`35549443783\` success;
  - gameplay Action \`35549443834\` success.

- \`7d321792543a537ea9318eb14b504c147518a843\`
  - explicit persistent capture transition;
  - successful target exits battle without kill EXP/drop;
  - standalone runtime persistence of a complete captured \`PetActor\`;
  - battle-core Action \`35549610051\` success;
  - gameplay Action \`35549610032\` success.

- \`882a124471bda8ae31a22dfa6f75c3998afd4aaa\`
  - capture executes in ordinary action order with target adjustment/exited-target tracking;
  - corrected local round-test fixture;
  - battle-core Action \`35549871944\` success;
  - gameplay Action \`35549871985\` success.

- \`cb7d57cbc6488f9c815c0043c72c99dce9672a4c\`
  - ordinary-round successful capture now validates and atomically persists the supplied complete pet;
  - missing/extra captured-pet mappings fail before persistent pet mutation;
  - gameplay Action \`35549951206\` success.

## Confidence boundary

**CLOSED for the strong stable-descendant mechanics profile and current single-player runtime:**

- capture command identity;
- live target adjustment seam;
- target/PETFLG/level gates;
- exact stable probability arithmetic;
- sleep +15;
- 99 upper cap and strict \`RAND(1,100) < WorkGet\`;
- temporary capture-modifier reset;
- five-slot first-empty capacity ordering;
- successful enemy exit as a non-kill;
- no capture EXP/drop profit;
- atomic installation of a complete source-identified captured pet.

**OPEN / profile-specific:**

- byte-level confirmation that every one of these details is identical to the 1999 JSS server;
- whether the later \`_CAPTURE_FREES\` hard-coded required-item table belongs to any early target build;
- full status/rescue \`BATTLE_TargetCheck()\` behavior beyond the current status-free battle seam;
- exact original visible-AI/compliance result after the captured pet copy;
- production construction of every copied pet field from an original early-server dataset when that provenance becomes available.
