# StoneAge PETSKILL_DamageToHp — R1 fixed-source boundary

## Scope

This note covers the older macro-gated `_SKILL_DAMAGETOHP`
`PETSKILL_DamageToHp` callback only. The later
`_PETSKILL_DAMAGETOHP` / `PETSKILL_DamageToHp2` variant is a separate
descendant feature and is not merged into recovered25 unless the recovered
callback data says so.

## Convergent fixed-descendant behavior

The pinned gavin/iriselia/Bismarck descendants agree on the older callback
shape:

1. submit symbolic `BATTLE_COM_S_DAMAGETOHP`;
2. copy the selected opponent target to COM2;
3. mark the actor command-ready;
4. store the pet-skill array/ID in the low COM3 half;
5. parse OPTION field 1 and rewrite WORKATTACKPOWER;
6. after TargetAdjust, execute the ordinary physical
   `BATTLE_S_AttackDamage` path;
7. if the resulting target damage is positive and the target has no active
   DamageReact, parse OPTION field 2 and convert a percentage of
   `damage + petdamage` into attacker HP.

The callback's first percentage contains a real C arithmetic quirk:
`atoi(token1) / 100` is integer division before assignment to float.
Consequently values 1..99 produce ratio 0; 100..199 produce ratio 1, etc.
The reconstruction preserves this rather than silently changing it to
floating-point percent math.

The recovery percentage does use floating-point division:
`((float)atoi(token2))/100`. Recovery is truncated to int, then capped to
the attacker's missing HP.

If `Damage < 1` or `BATTLE_GetDamageReact(defindex) > 0`, the recovery
helper returns zero and leaves attacker HP unchanged.

## Later DamageToHp2 separation

The later `PETSKILL_DamageToHp2` callback is not equivalent:

- it writes a distinct symbolic command;
- its callback-side attack-power rewrite is commented out;
- its recovery helper parses the whole OPTION as one integer percentage;
- the later command also receives dedicated initiative/critical behavior in
  descendant code.

Those semantics are kept outside this R1 boundary.

## Recovered25 admission gate

The recovered callback census reports **3 referenced IDs / 30 positive
enemybase slot uses** for `PETSKILL_DamageToHp`. Before runtime admission,
the preservation bundle must prove all three recovered OPTION rows are ASCII
and contain the two delimiter positions consumed by the older handler. The
hard probe records only derived numeric mechanics and does not persist raw
OPTION or display text.

The guarded numeric COM1 is not assigned here. Runtime integration, if the
hard probe closes, should use a typed semantic submission/overlay in the same
spirit as recovered ReHP rather than guessing a descendant compile-profile
enum value.
