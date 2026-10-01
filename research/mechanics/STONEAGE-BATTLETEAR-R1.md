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
