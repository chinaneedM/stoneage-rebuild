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
