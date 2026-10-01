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
