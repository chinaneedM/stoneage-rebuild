# StoneAge PETSKILL_MpDamage — R1 fixed-source boundary

## Fixed callback

The pinned gavin/iriselia/Bismarck descendants converge on the guarded
`_Skill_MPDAMAGE` callback:

- write symbolic `BATTLE_COM_S_MPDAMAGE`;
- COM2 = submitted target;
- mark command ready;
- LOW(COM3) = selected pet-skill ID;
- parse OPTION field 1;
- compute `(float)(atoi(token1)/100)`, preserving integer division;
- reset WORKATTACKPOWER from FIXSTR using that integer ratio.

The same 1..99 -> 0 quirk seen in the older DamageToHp callback is therefore
also source behavior here.

## Physical execution and MP effect

The battle dispatcher performs ordinary TargetAdjust, then calls the common
`BATTLE_S_AttackDamage` physical path with symbolic MpDamage command identity.

After physical damage settlement, the special helper runs only when:

- physical `damage >= 1`;
- the original adjusted target has no active DamageReact;
- the target is neither ENEMY nor PET;
- the target's current MP is positive.

It parses OPTION field 2 as a floating percentage and computes:

`mp_damage = int(current_target_mp * percent / 100)`

The amount is based on current MP, not on physical HP damage. It is then
subtracted from target MP and the player MP status string is refreshed.

The helper receives physical `damage`, not `damage + petdamage`; ride-pet
damage therefore does not scale the MP percentage. As with DamageToHp, the
specialized BATTLE_S_AttackDamage path keeps the fixed Guardian calculation /
original-defindex settlement quirk.

## Recovered25 gate

The recovered non-common inventory reports **3 referenced callback IDs / 25
positive enemybase slot uses**. A dedicated preservation-bundle probe must
establish the exact three IDs and both consumed numeric OPTION fields before
runtime admission. No guarded numeric COM1 is guessed in this reference layer.


## Recovered25 hard-probe result

The verified preservation bundle closes the referenced recovered25 domain:

| Skill ID | FIELD | TARGET | COST | ILLEGAL | token1 | callback integer ratio | MP damage |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 506 | 1 | 6 | 2 | 2000 | 50 | 0 | 50% |
| 507 | 1 | 6 | 2 | 0 | 50 | 0 | 75% |
| 508 | 1 | 6 | 2 | 0 | 50 | 0 | 100% |

All three OPTIONs are ASCII with exactly two pipe-delimited numeric fields.
There are **25** positive enemybase slot references across **25** templates.

The callback's first-token integer-division quirk is live but numerically
neutral for recovered25: all three use 50/100, which truncates to zero before
the value is assigned to float. The admitted enemy runtime therefore resets
WORKATTACKPOWER from FIXSTR without reducing it.

Hard-probe workflow **36869183326 = PASS** and wrote
`research/recovered/STONEAGE-25-MPDAMAGE-PROBE-R1.txt`.

## Runtime admission

Recovered25 MpDamage is executable through a typed semantic submission without
assigning a speculative guarded numeric COM1.

The admitted path preserves the fixed ordering and target rules:

1. enemy AI selects recovered ID 506/507/508;
2. typed submission carries skill identity, source target and parsed OPTION;
3. ordinary ATTACK is used only as the reconstruction's scheduling and
   physical-resolution carrier;
4. ordinary TargetAdjust executes once;
5. the specialized physical path retains the fixed Guardian
   calculation/original-defindex settlement behavior;
6. pre-existing DamageReact on that original adjusted target suppresses the MP
   effect;
7. otherwise the ordinary physical hit resolves;
8. only PLAYER targets with positive current MP can lose MP; PET and ENEMY
   targets are excluded by the fixed helper;
9. the helper uses post-DamageSub player `damage` only as a positive-hit gate,
   then subtracts 50/75/100 percent of the target's current MP;
10. MP state is updated in action order, so multiple MpDamage actors in one
    round consume the already-reduced current MP rather than the round-start MP.

The round carries a dedicated MP overlay and the local-session coordinator
seeds the player value from the working persistent save. After resolution it
writes the final MP back only to the working clone; the immutable pre-battle
session snapshot is not mutated in place.

Validation at current repaired HEAD
`0e0917d320faa9eda90d4e9f315400713c14a753`:

- MpDamage runtime **36870364373 = PASS** (**67 tests**);
- local runtime coordinator **run 163 = PASS**;
- enemy AttackMagic coordinator **run 8 = PASS**;
- enemy ReHP runtime **run 7 = PASS**;
- DamageToHp runtime **run 4 = PASS**.

The two immediately preceding failures were test-import integration failures
introduced after the runtime commit and are superseded by the corrected import
at the current HEAD; they are not unresolved mechanics failures.

**RECOVERED25_MPDAMAGE_RUNTIME_R1 = CLOSED.**

The next recovered non-common family by recorded positive enemybase slot-use
pressure is `PETSKILL_FallGround`: **1 referenced ID / 23 slot uses**.
