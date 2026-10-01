# StoneAge PETSKILL_FallGround — R1 fixed-source boundary

## Callback

The pinned gavin/iriselia/Bismarck descendants converge on guarded
`_PSKILL_FALLGROUND`:

- COM1 = symbolic `BATTLE_COM_S_FALLRIDE`;
- COM2 = submitted target;
- command mode is marked ready;
- unlike DamageToHp/MpDamage, no skill ID is written into COM3;
- OPTION is searched for the two-byte Big5/CP950 character plus percent marker
  `攻%`;
- the following value is scanned as float;
- WORKATTACKPOWER becomes
  `FIXSTR + int(FIXSTR * (attack_percent / 100))`.

The handler returns TRUE even if the marker is absent. If the marker exists but
float scanning fails, fixed C code keeps the initialized `fPer=0.01`, then
divides it by 100 before applying the tiny additive term.

## Dedicated battle executor

The dispatcher runs TargetAdjust once, then calls the dedicated
`BATTLE_S_FallGround` function. This function uses the ordinary AttackSeq and
DamageSub primitives but is not the generic `BATTLE_S_AttackDamage` wrapper.

Important source behavior:

- DamageReact is read from the original adjusted target before AttackSeq.
- AttackSeq may use a Guardian for damage calculation, while DamageSub is still
  called with the original adjusted target index.
- the fall side effect is considered only when post-DamageSub player
  `damage > 0` and `react == 0`;
- when that gate passes, `RAND(0,100)` is consumed even if the target is not
  mounted;
- success is strict `roll > threshold`;
- gavin/iriselia compile `_EQUIT_RESIST`, making threshold
  `50 + CHAR_WORKEQUITFALLRIDE`;
- pinned Bismarck does not compile that resistance branch, making threshold 50;
- gavin/iriselia compile `_PREVENT_TEAMATTACK`; pinned Bismarck does not;
- all three compile `_ENEMY_FALLGROUND`;
- none of the three pinned descendants defines `_FIXPETFALL`, so PLAYER
  unmount uses the historical strict test `CHAR_RIDEPET > 0`, not `>= 0`.

Thus a player riding pet slot/index 0 can pass the fall RNG but remain mounted
in all three pinned source trees. The reconstruction must not silently repair
that bug inside the archaeology layer.

Enemy-target fall has an additional active branch in all three pinned trees:
a mounted enemy is unmounted, petfall is set, STR/TOUGH/VITAL are multiplied by
0.7 and parameters are recomputed. That branch must remain separate from the
enemy-AI -> player-target admission path unless same-side execution is proven.

## Recovered25 gate

The non-common inventory records **1 referenced FallGround ID / 23 positive
enemybase slot uses**. Before runtime admission the preservation bundle must
prove the exact row, OPTION encoding and attack-percent marker/value.

Because equipment fall resistance differs across pinned compile profiles, a
recovered25 runtime must not invent a nonzero resistance value or silently
choose one descendant profile. The shared zero-resistance behavior is
convergent; nonzero resistance requires an explicit profile/state boundary.


## Recovered25 hard-probe and runtime admission

The preservation-bundle hard probe closes the active recovered25 row:

- callback population: exactly **1** row, skill ID **210**;
- FIELD=1, TARGET=6, COST=2, ILLEGAL=3000;
- OPTION is **6 bytes** and strict CP950/Big5 decoding agrees;
- the required `攻%` marker is present with numeric value **-30.0**;
- the callback therefore sets battle work attack power to
  `FIXSTR + int(FIXSTR * -0.30)`, i.e. 70% for positive integral FIXSTR;
- enemybase pressure is **23** positive slot uses across **23** templates.

Bundle probe workflow **36871586479 = PASS**.

Recovered enemy execution is admitted through a typed semantic submission. No
guarded numeric `BATTLE_COM_S_FALLRIDE` value is assigned to recovered25.
Ordinary ATTACK is only the reconstructed ordering / physical-resolution
carrier.

The admitted runtime preserves the dedicated FallGround source behavior:

1. one ordinary TargetAdjust-shaped target resolution;
2. callback attack-power setup must exactly match the recovered -30% OPTION;
3. ordinary AttackSeq / DamageSub physical settlement is reused;
4. DamageReact blocks the fall side effect and consumes no fall RNG;
5. otherwise positive post-DamageSub player damage consumes explicit
   `RAND(0,100)`;
6. the cross-descendant zero-resistance admission uses strict
   `roll > 50`;
7. nonzero equipment fall resistance remains fail-closed because the pinned
   compile profiles disagree on `_EQUIT_RESIST`;
8. player ride-pet source-slot provenance is consumed only when FallGround is
   actually present;
9. the pinned historical `CHAR_RIDEPET > 0` bug is preserved: source pet
   slot 0 can pass the roll but remains mounted;
10. a successful nonzero source slot unmounts the ride pet and sets PETFALL in
    persistent battle-local ride state.

The first FallGround integration commits exposed two reconstruction-only
ordering/interface regressions: setup effects were validated before
initialization, and FallGround source-slot provenance was initially made
mandatory for unrelated ride-pet rounds. Both were corrected without changing
the historical mechanic. At repaired commit
`e62c938fe782e24eedad80c575ba034752312f96`:

- FallGround runtime **36874842586 = PASS**;
- battle core **36874842626 = PASS**;
- local runtime coordinator **36874842540 = PASS**;
- DamageToHp runtime **36874842608 = PASS**;
- MpDamage runtime **36874842676 = PASS**;
- enemy ReHP runtime **36874842571 = PASS**;
- enemy AttackMagic coordinator **36874842524 = PASS**;
- AttackMagic round execution **36874842784 = PASS**;
- Taiwan-v1 gameplay **36874842624 = PASS**;
- recovered25 region/runtime stack **36874842303 = PASS**.

**RECOVERED25_FALLGROUND_RUNTIME_R1 = CLOSED.**
