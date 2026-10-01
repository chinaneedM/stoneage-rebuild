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


## Recovered25 hard-probe result

The preservation bundle closes the older-handler OPTION domain exactly:

| Skill ID | FIELD | TARGET | COST | ILLEGAL | token1 | callback integer ratio | recovery |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 503 | 1 | 6 | 2 | 2000 | 30 | 0 | 50% |
| 504 | 1 | 6 | 2 | 0 | 20 | 0 | 70% |
| 505 | 1 | 6 | 2 | 0 | 10 | 0 | 100% |

All three OPTION values are ASCII, have exactly two pipe fields, and have
decimal prefixes in both consumed positions. There are **30** positive
enemybase slot references across **30** templates.

The first-token integer-division quirk is therefore live but numerically
neutral in recovered25: 30/100, 20/100 and 10/100 all truncate to zero before
assignment to float. For the admitted enemy runtime, the callback consequently
resets WORKATTACKPOWER to FIXSTR without applying a percentage reduction.

Probe workflow **36866862704 = PASS**. The derived report is
`research/recovered/STONEAGE-25-DAMAGETOHP-PROBE-R1.txt`.

## Runtime admission

Recovered25 DamageToHp is now executable through a typed semantic submission
without choosing a speculative guarded COM1 integer.

The admitted round path preserves the fixed ordering:

1. enemy AI selects one of recovered IDs 503/504/505;
2. a typed submission carries skill identity, source target and parsed OPTION;
3. ordinary ATTACK is used only as a modern ordering/physical-resolution
   carrier;
4. ordinary TargetAdjust runs once;
5. Guardian retains the specialized source quirk: AttackSeq can calculate
   against the Guardian while BATTLE_S_AttackDamage still passes the original
   adjusted defindex to DamageSub;
6. any DamageReact already active on that original adjusted target demotes the
   special effect before attack resolution, so no HP conversion occurs;
7. otherwise the normal physical hit resolves;
8. post-hit recovery uses the source-returned `damage + petdamage` basis.
   For mounted targets this is explicitly the rider split amount plus ride-pet
   split amount, not only the visible rider damage;
9. recovery is truncated and capped to the attacker's missing HP before
   persistent round state is committed.

The implementation remains enemy-runtime scoped; it does not claim player/pet
input-menu semantics or a recovered numeric command enum.

Validation at source commit `59e85a8a9531206ce1465ba7ce805f408571716f`:

- DamageToHp runtime **36868357706 = PASS**;
- battle core **36868357723 = PASS**;
- stable pet-skill core **36868357938 = PASS**;
- local runtime coordinator **36868357914 = PASS**;
- runtime golden **36868357741 = PASS**;
- Taiwan-v1 gameplay **36868357811 = PASS**;
- enemy ReHP regression **36868357788 = PASS**;
- enemy AttackMagic coordinator **36868357860 = PASS**;
- AttackMagic round-state adapter **36868357946 = PASS**.

**RECOVERED25_DAMAGETOHP_RUNTIME_R1 = CLOSED.**

The next recovered non-common family by positive enemybase slot-use pressure is
`PETSKILL_MpDamage`: **3 referenced IDs / 25 slot uses**.
