# StoneAge PETSKILL_Lighttakeed bounded reference R1

Status: **CLOSED_BOUNDED_RECOVERED25_REFERENCE**  
Date: 2026-10-05  
Scope: complete recovered25 callback population plus the positively referenced
enemy uses of `PETSKILL_Lighttakeed`.

## 1. Evidence role

This reference combines a hash-verified recovered25 data probe with three
fixed later-descendant source profiles. It is not original JSS/Taiwan-v1
source or executable provenance, and it does not authorize an ordered runtime
by itself.

Pinned descendants:

- gavinlinasd/StoneAge @
  `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`;
- iriselia/StoneAge @
  `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`;
- BismarckDD/stoneage @
  `999ffdf1d220ec6666eb65339180689c9caf1876`.

## 2. Recovered25 callback population and exact rows

The verified recovered25 `petskill` file has SHA-256
`f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4`.

The complete `PETSKILL_Lighttakeed` callback population is exactly three
rows: **609 / 610 / 611**. All three have **FIELD 1 / TARGET 7 / COST 2 /
ILLEGAL 5000**, a six-byte OPTION payload, and no NUL byte.

Derived OPTION identities are retained without storing raw table rows:

- **609**: OPTION SHA-256
  `28e420f6e618020e7fdba9f49433a94c5f88cbd6edba2d521104f880b416c5e7`;
  marker classification = **ABSROB**; positive enemybase references = **0**.
- **610**: OPTION SHA-256
  `73bef6383b8b2e301ef6860a573f7b7d703c651aa3e90df3e1efe6f1b28fce01`;
  marker classification = **REFLEC**; positive enemybase references = **2**.
- **611**: OPTION SHA-256
  `a715b2ee62e500775e7eca86facd327f5cdc6501f4064dd322f8fc6e1ddbf96b`;
  marker classification = **VANISH**; positive enemybase references = **1**.

The pressure classifier correctly selected only IDs **610/611**, because
pressure ranks positively referenced rows. ID **609** is nevertheless part of
the complete callback population and must remain in reference/data admission
checks.

## 3. Exact positive enemybase references

There are exactly **3 positive slot uses / 2 templates**:

- TEMPNO **70**, graphic **101550**, skill slot **4** -> ID **610**;
- TEMPNO **157**, graphic **101283**, skill slots **4 / 5** ->
  IDs **610 / 611**.

No positive enemybase slot uses ID 609 in the verified recovered25 dataset.

## 4. Fixed descendant callback and dispatch facts

All three pinned profiles compile `_BATTLE_LIGHTTAKE` and register
`PETSKILL_Lighttakeed`.

The callback:

- rejects a player actor;
- writes symbolic `BATTLE_COM_S_LIGHTTAKE`;
- copies the supplied target carrier into COM2;
- marks `BATTLE_CHARMODE_C_OK`;
- sets temporary attack power to **fixed STR * 0.7**;
- sets temporary defence power to **fixed TOUGH * 0.5**;
- stores the skill-array identity in LOW(COM3);
- does not read OPTION;
- consumes no callback-local RNG.

A QUICK adjustment appears only as commented source and is therefore not part
of the executable callback reference.

The battle dispatcher first performs `BATTLE_TargetAdjust`. An invalid target
produces NoAction. A valid target recovers the skill identity from LOW(COM3)
and enters `BATTLE_S_AttackDamage` with symbolic
`BATTLE_COM_S_LIGHTTAKE`.

## 5. Damage-reaction marker semantics

Inside the fixed `BATTLE_S_AttackDamage` path, OPTION is read before the
ordinary attack sequence. If the defender currently has a damage reaction,
Lighttakeed classifies the OPTION marker in this order:

1. `VANISH`;
2. else `ABSROB`;
3. else `REFLEC`.

If the active defender reaction matches the classified marker, the local
`react` value is neutralized to zero before `BATTLE_AttackSeq`. If it does
not match, the Lighttakeed `skill_type` is demoted to ordinary/non-Lighttake
handling.

The Lighttake-specific post-damage branch then emits the ordinary BH hit frame.
That branch consumes no RNG of its own. This does **not** claim that the shared
ordinary attack/damage machinery is RNG-free; only the Lighttake-specific
callback and post-damage branch are closed here.

## 6. Material descendant divergence retained

The three pinned profiles agree on command value **2009** and C_OK mode value
**3**, but those are later-descendant compile facts only and do not prove the
recovered original numeric COM1.

More importantly, they diverge in the Lighttake-specific attacker counter
assignment after a matching reaction:

- gavin / iris: attacker receives the defender's corresponding
  `CHAR_WORKDAMAGEVANISH`, `CHAR_WORKDAMAGEABSROB`, or
  `CHAR_WORKDAMAGEREFLEC` value unchanged;
- Bismarck: attacker receives that observed value **plus one**.

The reference therefore records two explicit semantic profiles:
`copy` and `copy_plus_one`. It does not choose one as the recovered
original behavior.

## 7. Explicitly open runtime boundaries

This reference does not close:

- recovered original executable/compiler/profile identity;
- recovered original numeric COM1 despite the three descendant values agreeing;
- which counter-assignment profile (`copy` vs `copy_plus_one`) belongs to
  the recovered25 executable;
- complete shared `BATTLE_AttackSeq` / damage / reaction RNG ordering and
  state mutation needed for an ordered runtime;
- persistence/lifetime semantics of the VANISH/ABSROB/REFLEC work counters
  beyond the audited Lighttake-specific reads/writes;
- original JSS/Taiwan-v1 membership or introduction date.

A runtime implementation must first attempt a bounded executable/profile
discriminator. If that remains inconclusive, it must expose the source
divergence explicitly instead of silently selecting a descendant.

## 8. Acceptance

- exact source + preservation-bundle workflow:
  **37295790110 attempt 2 PASS**;
- derived report write-back:
  **0d002434a5b86e20505ff8b8fd431b3075374c84**;
- fixed-source report:
  `research/recovered/STONEAGE-LIGHTTAKEED-SOURCE-AUDIT-R1.txt`;
- exact recovered25 report:
  `research/recovered/STONEAGE-25-LIGHTTAKEED-PROBE-R1.txt`.

**LIGHTTAKEED_FIXED_SOURCE_R1 =
CLOSED_CONDITIONAL_REFERENCE.**

**LIGHTTAKEED_REFERENCE_R1 =
CLOSED_BOUNDED_RECOVERED25_REFERENCE.**

Pressure remains **2451/2486 = 98.59%** until ordered Lighttakeed runtime
acceptance and a verified pressure refresh.
