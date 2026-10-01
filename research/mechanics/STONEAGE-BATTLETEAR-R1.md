# StoneAge PETSKILL_BattleTearDamage — R1 fixed-source boundary

## Callback

The pinned gavin/iriselia/Bismarck descendants converge on guarded
`_PETSKILL_TEAR`.

The callback rejects PLAYER actors, then writes symbolic
`BATTLE_COM_S_PETSKILLTEAR`, the submitted target, and command-ready mode.
It does **not** parse OPTION. Instead it immediately mutates work powers:

- WORKATTACKPOWER = `int(FIXSTR * 0.9)`;
- WORKDEFENCEPOWER = `int(FIXTOUGH * 0.8)`;
- LOW(COM3) = callback `array`.

All three pinned descendants enable `_PETSKILL_OPTIMUM`, whose active table
layout makes this recovered array identity directly addressable by pet-skill ID.

## Physical executor

The battle dispatcher TargetAdjusts once, reads LOW(COM3), and enters the
generic `BATTLE_S_AttackDamage` helper with TEAR as `skill_type`.

The TEAR-specific mutation occurs after AttackSeq and before DamageSub:

1. DamageReact is inspected before AttackSeq. Any active ordinary DamageReact
   changes `skill_type` away from TEAR, so the wound augmentation is skipped.
2. AttackSeq performs ordinary dodge, Guardian, critical, guard/minimum damage
   and common physical modifiers.
3. If TEAR remains active and the result is not DODGE, compute the original
   adjusted target's missing HP: `MAXHP - HP`.
4. If that original target is PLAYER and has a ride pet, add the ride pet's
   missing HP too.
5. Parse OPTION with plain C `atoi`, divide by 100 as float, and truncate
   `missing_hp * ratio` back to int.
6. If that wound amount is positive, add it to the AttackSeq damage.
7. If that wound amount is zero or negative, set the entire damage value to
   zero. The original physical damage is **not** retained.
8. DamageSub then receives the original adjusted target, even if AttackSeq used
   a Guardian for physical calculation.

This produces the same Guardian/original-target quirk seen in several later
special physical skills: Guardian can affect AttackSeq's physical calculation,
while TEAR's wound basis and DamageSub settlement still use the original
adjusted target.

gavin/iriselia compile `_PREVENT_TEAMATTACK` and skip the TEAR augmentation
on a same-side target; pinned Bismarck does not compile that branch. Recovered
enemy -> player ordinary targeting is opposite-side and therefore lies in the
cross-descendant intersection.

## Recovered25 gate

The pressure inventory proves **2 referenced IDs (615/616) / 19 positive
enemybase slot uses across 19 templates**. Runtime admission requires the
preservation bundle to close both OPTION rows under the source's actual
`atoi` grammar before any command is made executable.


## Recovered25 hard-probe and runtime admission

The preservation bundle closes the exact active recovered25 data domain:

- skill IDs **615** and **616** only;
- **19** positive enemybase slot references across **19** templates;
- both rows are FIELD=1, TARGET=1, COST=2, ILLEGAL=10000;
- both OPTIONs are two-byte strict ASCII leading integers;
- ID 615 -> `atoi(OPTION)=20`;
- ID 616 -> `atoi(OPTION)=50`.

Bundle probe workflow **36876535217 = PASS**.

Recovered enemy execution is admitted through a typed semantic submission rather
than assigning a guarded numeric `BATTLE_COM_S_PETSKILLTEAR` value. Ordinary
ATTACK is an internal scheduling / physical-resolution carrier only.

The admitted execution preserves the fixed ordering:

1. enemy AI resolves the exact recovered wa[] slot;
2. callback-time work state is written before execution:
   `WORKATTACKPOWER=int(FIXSTR*0.9)` and
   `WORKDEFENCEPOWER=int(FIXTOUGH*0.8)`;
3. TargetAdjust runs once;
4. ordinary AttackSeq performs dodge, Guardian, critical, guard and minimum
   physical-damage handling;
5. active DamageReact disables the TEAR-specific wound mutation;
6. otherwise the wound basis is the **original adjusted target's** missing HP,
   plus that player's mounted ride-pet missing HP when present;
7. recovered OPTION 20/50 percent is applied with the source's float multiply
   followed by integer truncation;
8. positive wound damage is added to AttackSeq damage;
9. a zero/non-positive wound result sets the **entire** outgoing damage to zero
   rather than retaining the physical component;
10. DamageSub settles against the original adjusted target even when Guardian
    was used by AttackSeq for physical calculation.

This preserves the source's non-obvious full-HP behavior: a full-HP target with
no wounded ride pet can turn an otherwise positive physical TEAR hit into zero
damage. The reconstruction also keeps the Guardian/original-target split rather
than flattening the skill into a generic damage bonus.

Validation at
`f2c166540b11a8f722e82fbec27e57622f2a7ec1`:

- BattleTear runtime **36877818507 = PASS** (**73 tests**);
- battle core **36877818319 = PASS**;
- local runtime coordinator **36877818261 = PASS**;
- stable pet-skill core **36877818294 = PASS**;
- runtime golden contract **36877818581 = PASS**;
- Taiwan-v1 gameplay **36877818853 = PASS**;
- FallGround **36877819026 = PASS**;
- DamageToHp **36877818298 = PASS**;
- MpDamage **36877818333 = PASS**;
- enemy ReHP **36877818356 = PASS**;
- enemy AttackMagic coordinator **36877818526 = PASS**;
- AttackMagic round execution **36877818555 = PASS**;
- AttackMagic state adapter **36877819266 = PASS**.

The recovered25 region/runtime-stack workflow had already passed its
deterministic tests, bundle recovery and all materializable-map validation when
this closure was recorded; its remaining long aggregate stages are orthogonal
to the BattleTear mechanic and remain independently visible in Actions.

**RECOVERED25_BATTLETEAR_RUNTIME_R1 = CLOSED.**
