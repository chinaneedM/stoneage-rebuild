# StoneAge Pet Capture Core R1

Status: **strong convergent descendant evidence; exact launch-era constants/data identity remains OPEN**  
Scope: ordinary battle capture gate, probability equation, pet-slot creation and enemy-to-pet state transfer. Version-specific required-item tables and later pet-follow extensions remain separated.

## Purpose

The repository already reconstructs wild encounters/battle and pet growth. Capture is the deterministic transition that connects those systems: a live wild enemy can become a carried pet while preserving substantial current battle state.

The preserved source is unusually explicit, but it also contains traps that should not be normalized away:

- the HP term is not a conventional normalized HP percentage;
- the random comparison is strict `<`, not `<=`;
- the displayed/computed score can reach 99 while the integer roll therefore has only 98 successful outcomes;
- the capture command passes `20` to an MP-down helper whose active implementation is a no-op in all three fixed descendants;
- pet-slot failure occurs **after** a successful probability roll in the server path.

R1 mirrors the executed code rather than correcting it into a more intuitive modern design.

## Evidence set

Fixed source revisions:

- **BismarckDD/stoneage** @ `999ffdf1d220ec6666eb65339180689c9caf1876`
  - `server/gmsv/battle/battle_event.c`
  - `server/gmsv/battle/battle_command.c`
  - `server/gmsv/char/pet.c`
  - `server/gmsv/char/char_base.c`
  - `server/gmsv/char/enemy.c`
  - `server/common/common.h`
- **gavinlinasd/StoneAge** @ `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
  - corresponding `gmsv/src` files
- **iriselia/StoneAge** @ `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
  - corresponding `Source/gmsv` files

## Battle command

**FACT — convergent descendant code**

The player capture command is encoded through the battle command beginning with `T|`. The selected target number is stored as the second battle-command operand and the actor command becomes `BATTLE_COM_CAPTURE`.

All three branches contain:

```c
BATTLE_MpDown(charaindex, 20);
```

after accepting the command.

However, the active `BATTLE_MpDown` implementation at all three fixed revisions immediately returns `0` and changes no MP. gavinlinasd/iriselia keep an older implementation under an inactive `#else`.

Therefore:

- **FACT:** the capture command passes the nominal argument `20`;
- **FACT:** the fixed active descendants do not actually subtract 20 MP through this helper;
- **OPEN:** whether an earlier commercial target version used the inactive MP implementation or another variant.

R1 records the executed active cost as zero and keeps the nominal argument as provenance, not as a gameplay rule.

## Core target gate

`BATTLE_CaptureCheck` is convergent across all three lineages.

A target is rejected unless:

1. it is `CHAR_TYPEENEMY`;
2. its `CHAR_WORK_PETFLG` is nonzero;
3. unless the attacker has `CHAR_PickAllPet == TRUE`, the target level is no more than five levels above the attacker.

In descendant code, `CHAR_PickAllPet` is toggled by an equipment effect commented as the **驯兽戒指** behavior. R1 models the flag as a bypass input rather than asserting a launch-era item identity.

## Probability equation

Let:

- `C` = attacker fixed charm;
- `AL` = attacker level;
- `AD` = attacker fixed dexterity;
- `AK` = attacker fixed luck;
- `DL` = target level;
- `DD` = target fixed dexterity;
- `G` = target `CHAR_WORKMODCAPTUREDEFAULT`;
- `H` = target current HP;
- `M` = target work MAXHP, replaced by 1 if non-positive;
- `T` = attacker's temporary `CHAR_WORKMODCAPTURE`.

The source computes:

```
hp_term    = 10 - H * H / M
level_term = AL / 2 - DL / 2
dex_term   = AD / 15 - DD / 15

WorkGet =
    (hp_term + level_term + dex_term + G + AK)
    * C / 50

WorkGet += T

if target is sleeping:
    WorkGet += 15

if WorkGet > 99:
    WorkGet = 99
```

All working variables are floating-point in the preserved function. There is no lower clamp.

### Important HP semantics

The HP contribution is literally:

```
10 - HP² / MAXHP
```

It is **not**:

```
10 * (1 - HP / MAXHP)
```

and R1 does not rewrite it.

### Default capture value provenance

When an enemy is instantiated, `CHAR_WORKMODCAPTUREDEFAULT` is loaded from the enemy-template `E_T_GET` field. This target-specific value is therefore part of the wild-enemy data layer rather than a universal constant.

### Temporary capture modifier and sleep

The attacker temporary capture modifier is added directly. A sleeping target adds `15`.

After the item/probability checks, `CHAR_WORKMODCAPTURE` is reset to `0` regardless of success or failure.

## Random comparison and effective maximum

The common macro `RAND(1,100)` yields an integer in the inclusive range 1..100.

Capture succeeds only when:

```c
RAND(1,100) < WorkGet
```

The comparison is strict.

Consequences:

- score `54.0` succeeds on rolls 1..53: 53 integer outcomes;
- capped score `99.0` succeeds on rolls 1..98: 98 integer outcomes;
- roll 99 fails even when the score is capped at 99.

Accordingly, R1 distinguishes the source `WorkGet` score from the count of successful discrete rolls.

## Required capture items are versioned data

Before the probability check, `BATTLE_CaptureItemCheck` enforces special item requirements for selected pet IDs.

The preserved descendants contain conditional/versioned tables controlled by macros including:

- `_CAPTURE_FREES`;
- `_DEL_NOT_25_NEED_ITEM`;
- `_WOLF_TAKE_AXE`;
- `_NEED_ITEM_ENEMY`.

For example, the descendants retain an enemy-ID 524 requirement involving item 2456, while later Eden/extension entries and multi-item conditions are controlled by branch/configuration.

R1 therefore does **not** invent one canonical historical required-item table. The deterministic model accepts required item IDs as version-data input.

In the ordinary success path, matching condition items are consumed only after pet creation succeeds. The `_CAPTURE_FREES` success helper iterates all matching slots; this can remove all matching copies rather than a single arbitrary copy.

Some Bismarck later configuration can delete condition items during the check itself; that extension is outside the ordinary R1 transition.

## Five carried-pet slots

**FACT — convergent descendant definitions**

All three branches define:

```
CHAR_MAXPETHAVE = 5
```

The ordinary `CHAR_getCharPetElement` returns the first empty slot 0..4 or `-1` when full.

Bismarck also contains a later `_PETFOLLOW_NEW_` variant that counts follow-pets against the same capacity. R1 keeps that extension separate and models the ordinary five carried slots.

The Bismarck client pre-checks the five-pet limit in its capture UI, but the server is still authoritative because `PET_createPetFromCharaIndex` returns `-1` if no slot exists.

### Ordering matters

The top-level server sequence is:

```
required-item check
  -> target/probability check
  -> reset temporary capture modifier to 0
  -> PET_createPetFromCharaIndex
       -> find first empty carried-pet slot
       -> fail if full
  -> success-only item consumption / counters / enemy exit
```

Thus a server-side capture roll can succeed and the final capture still fail because the pet roster is full.

## Enemy-to-pet state transfer

`PET_createPetFromCharaIndex` is strongly convergent.

It starts from the pet default template (`31010`) and copies the wild enemy's **current** state into a new `CHAR_TYPEPET`.

Common copied fields include:

- base image;
- current HP;
- MP / max MP;
- VITAL / STR / TOUGH / DEX;
- luck;
- fire / water / earth / wind;
- pet skill-slot count / MODAI;
- level;
- poison / paralysis / sleep / stone / drunk / confusion;
- rarity and pet rank;
- pet ID;
- critical / counter;
- all pet-skill slots;
- allocation point;
- display name.

Bismarck additionally copies a later `PETENEMYID` field not present in the same common form in the older two snapshots; R1 leaves that out of the convergent-common model.

The enemy EXP assignment is present only as a commented-out line. Instead the new pet's maximum EXP is recomputed from its copied level.

The new pet is then:

- parameter-complied;
- linked to the player;
- attached to the first empty carried-pet slot;
- assigned owner account/name metadata.

## Success finalization

After successful pet creation, `BATTLE_Capture`:

- records `PETGETLV = current pet level`;
- consumes version-specific capture-condition items;
- increments the player's `GETPETCOUNT`;
- calls `BATTLE_Exit` on the original wild enemy;
- recomputes the new pet;
- sets `VARIABLEAI = 0`;
- performs the preserved fixed-AI correction if necessary;
- emits a capture result command with success flag 1.

If any preceding stage fails, result flag 0 is emitted.

This gives an explicit deterministic bridge:

```
wild enemy current battle state
  -> successful capture
  -> carried pet with copied current state
  -> existing pet growth model
```

## Deterministic model

Repository artifacts:

- `tools/stoneage_pet_capture_model.py`
- `tests/test_stoneage_pet_capture_model.py`
- `.github/workflows/validate-stoneage-pet-capture.yml`

The tests cover:

- enemy/PETFLG/+5-level gates and the `PickAllPet` bypass;
- exact source probability math;
- sleep/temp-mod additions and the 99 cap;
- strict discrete-roll boundary and the 98-outcome maximum at score 99;
- lack of a lower clamp;
- version-data item requirements and all-matching-copy success consumption;
- first-empty-slot / five-slot-full behavior;
- probability success followed by pet-slot failure without condition-item consumption;
- current enemy-state copy into the captured pet;
- nominal `20` MP-down call versus active no-op MP implementation.

## Evidence status

- **FACT:** all three descendants agree on the ordinary capture target gate and formula.
- **FACT:** all three agree on temporary modifier reset, sleep +15, upper cap 99 and strict `RAND(1,100) < WorkGet`.
- **FACT:** all three define five carried-pet slots and make pet creation fail when no empty slot exists.
- **FACT:** all three copy the wild enemy's current core state into the new pet rather than rerolling a fresh species template.
- **FACT:** all three remove the captured enemy from battle only after successful pet creation.
- **FACT:** the fixed active `BATTLE_MpDown` implementation is a no-op despite the command passing 20.
- **FACT:** required-item tables are conditional/versioned and should not be flattened into one historical truth.
- **HYPOTHESIS:** the shared capture equation and enemy-to-pet transfer descend from the early official gameplay core.
- **OPEN:** direct JSS/1999 proof of the exact formula/constants and active MP behavior.
- **OPEN:** exact historical required-item tables by commercial version.
- **OPEN:** exact chronology of `PickAllPet`, `_CAPTURE_FREES`, follow-pet capacity and later capture-item extensions.

## Next technical seam

Capture now closes wild enemy -> battle -> pet roster/growth. The next high-value unmodeled system is **party / formation state**: party creation/join/leave, leader/client modes, carried pet battle-entry coupling, formation slot ordering and how encounter/battle entry projects field-party state into battle sides.
