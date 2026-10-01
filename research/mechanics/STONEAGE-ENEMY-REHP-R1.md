# StoneAge guarded enemy ReHP boundary R1

Status: **CLOSED_REFERENCE_MODEL_ONLY**

This note closes the deterministic fixed-source boundary for the recovered non-common callback `ENEMYSKILL_ReHP`. It does **not** yet admit the callback into the recovered25 enemy-AI runtime because the numeric value of its macro-gated battle command is build-profile dependent.

## Recovered25 pressure

The repository's preservation-bundle callback census records one referenced `ENEMYSKILL_ReHP` skill ID and 31 positive `enemybase` skill-slot uses. That makes it the highest-frequency still-unexecuted non-common family after AttackMagic.

The recovered census establishes use pressure only. It does not identify the exact server compilation profile that produced the preserved gameplay data.

## Pinned fixed-source evidence

The callback and effect were re-audited at the repository-pinned revisions:

- `gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
- `iriselia/StoneAge@9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
- `BismarckDD/stoneage@999ffdf1d220ec6666eb65339180689c9caf1876`

Relevant fixed files are `pet_skill.c`, `battle_event.c`, `battle.c`, `battle_magic.c`, `battle.h`, `version.h`, and `util.h` in the corresponding server trees.

All three builds compile `_PRO_BATTLEENEMYSKILL` and converge on the callback body: `ENEMYSKILL_ReHP` ignores the pet-skill OPTION/data argument, writes symbolic command `BATTLE_COM_S_ENEMYREHP`, copies the submitted target to COM2, marks the actor `C_OK`, and returns TRUE. No OPTION grammar is required for the handler itself.

## Dispatcher and fallback

The battle dispatcher first runs `BATTLE_TargetAdjust` on COM2. If the submitted opponent target is invalid/dead, the ordinary default-opponent retarget seam runs before ReHP and may consume its own RNG. If no opponent target exists, the actor performs no action and never enters the ReHP effect.

After a successful target adjustment, `BATTLE_E_ENEMYREHP` is called. If that effect returns FALSE, the dispatcher falls back to ordinary `BATTLE_Attack` against the already-adjusted opponent target. Therefore a failed heal is **not** equivalent to WAIT/NONE.

## Enemy-caster heal semantics

For an enemy caster, the fixed effect scans enemy-side slots 10..19 in ascending slot order and admits only valid entries satisfying:

`HP > 0 && HP < floor(MAX_HP * 2 / 3)`

The comparison is strict. A unit at exactly two-thirds max HP is not eligible.

If no eligible ally exists, the effect returns FALSE without consuming any ReHP-specific RNG, which activates the ordinary-attack fallback described above.

If at least one ally is eligible, source RNG consumption is:

1. `RAND(0, eligible_count - 1)` chooses one eligible ally by ascending-slot list index.
2. `RAND(100, target_max_hp)` chooses the base recovery power.
3. `BATTLE_MultiRecovery` consumes another `RAND(power * 0.9, power * 1.1)` for the reported HP recovery amount.

The common `RAND` macro is inclusive at both integer endpoints. All three pinned builds also define `_MAGIC_REHPAI`, so the active HP branch bypasses the ordinary percentage scaling and `GetRecoveryRate` multiplier. HP is capped at `WORKMAXHP`; the battle message still reports the pre-cap `UpPoint`.

The new reference model intentionally rejects a target with max HP below 100 instead of inventing semantics for the fixed macro's reversed `RAND(100,max_hp)` range. Recovered25 admission must prove that this edge is absent or otherwise close it from evidence.

## Guarded command-number divergence

`BATTLE_COM_S_ENEMYREHP` is not numerically portable because it sits after multiple conditional enum entries.

For the pinned gavin/iriselia profiles, `_SHOOTCHESTNUT` is enabled and the command resolves to **2014**. For pinned Bismarck, `_SHOOTCHESTNUT` is not enabled, so the same symbolic command resolves to **2013**.

This is a real compile-profile divergence, not a cosmetic source-format difference. The reconstruction must never write a guessed 2013/2014 COM1 value for recovered25 merely because the symbolic callback name matches.

## R1 implementation boundary

`tools/stoneage_enemy_rehp_model.py` now provides:

- explicit pinned command profiles with fail-closed unknown-profile handling;
- exact strict two-thirds eligibility;
- ascending enemy-slot candidate construction;
- explicit source-order RNG witnesses;
- HP cap plus separate reported/effective healing;
- exact no-eligible / inactive-caster ordinary-attack fallback signal.

The model starts **after** successful `BATTLE_TargetAdjust`, so caller-side retarget RNG remains separately observable and ordered before ReHP RNG.

Still open before recovered25 runtime admission:

- hard-probe the single recovered ReHP row and all 31 referencing slots;
- prove the referenced target/max-HP domain does not exercise the unresolved reversed RAND edge;
- either identify the recovered server compile profile strongly enough to choose a historical COM1 number, or carry the guarded command identity explicitly without pretending a numeric historical value is known;
- integrate the effect/fallback into the recovered enemy-AI round/coordinator with exact RNG ordering.

No Taiwan-v1 historical membership is implied. This remains a `LATER_RECOVERED`, macro-gated descendant layer.


## Recovered25 hard-probe closure

The preservation-bundle ReHP probe closed the remaining data-domain question
without projecting later source assumptions into Taiwan v1:

- one recovered ReHP skill row, hard-probed as skill ID **501**;
- **31** positive enemybase slot references across **31** templates;
- **28** runtime caster variants in **2** reachable encounter groups;
- **7** potential same-group heal-target variants;
- minimum possible reachable target max HP **602** over the recovered birth
  domain.

Therefore the fixed `RAND(100,target_max_hp)` lower bound is never reversed
inside the currently admitted recovered25 encounter graph.  Dedicated bundle
probe **36862737415 = PASS**.  The generated report is
`research/recovered/STONEAGE-25-ENEMY-REHP-PROBE-R1.txt`.

## Recovered25 runtime admission

Recovered25 ReHP is now executable without inventing a guarded historical
numeric COM1:

- `tools/stoneage_enemy_ai_rehp_bridge.py` binds the recovered one-row
  population to skill ID 501 and emits a typed semantic submission;
- ordinary `ATTACK` is used only as an internal initiative/order carrier.
  It is intercepted before physical execution and is **not** asserted to be
  the historical ReHP COM1 value;
- the round executor performs source-order `BATTLE_TargetAdjust` first;
- successful ReHP then consumes only the explicit three-stage effect RNG and
  updates the selected enemy-side HP with max-HP capping;
- no eligible heal target emits the semantic fallback phase and then performs
  ordinary physical `BATTLE_Attack` against the already-adjusted opponent;
- that fallback rejects a second retarget roll, preserving the source's single
  TargetAdjust consumption;
- status suppression/confusion remains ordered ahead of the semantic ReHP
  intercept, and unused ReHP RNG is rejected;
- persistent battle state and the local runtime coordinator carry the resulting
  HP across rounds with no special persistence side channel.

Validation:

- recovered25 ReHP semantic runtime **36865350487 = PASS**;
- battle core **36865230127 = PASS**;
- local runtime session coordinator **36865229998 = PASS**;
- Taiwan-v1 gameplay regression **36865230219 = PASS**;
- runtime golden contract **36865230075 = PASS**.

The guarded numeric divergence remains deliberately unresolved for recovered25:
2013 and 2014 are still descendant-profile facts only.  Runtime admission does
not require choosing between them.

**RECOVERED25_ENEMY_REHP_RUNTIME_R1 = CLOSED.**

The next non-common callback by positive recovered enemybase slot-use pressure
is `PETSKILL_DamageToHp` (**3 referenced IDs / 30 slot uses**).
