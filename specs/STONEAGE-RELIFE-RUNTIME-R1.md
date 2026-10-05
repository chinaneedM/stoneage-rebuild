# StoneAge ENEMYSKILL_ReLife ordered runtime R1

Status: **CLOSED_BOUNDED_RECOVERED25_ORDERED_RUNTIME**  
Date: 2026-10-05  
Scope: recovered25 positive enemy uses of `ENEMYSKILL_ReLife` / ID 500 only.

## 1. Accepted reference boundary

This runtime is downstream of `specs/STONEAGE-RELIFE-REFERENCE-R1.md`.

Recovered25 admission is exact:

- callback population: ID **500** only;
- FIELD **1**, TARGET **2 = PETSKILL_TARGET_ALLMYSIDE**;
- COST **2**, ILLEGAL **0**, empty OPTION;
- empty OPTION SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- exactly **3 positive uses / 3 templates**:
  - TEMPNO 39 / graphic 100370 / PETSKILL5;
  - TEMPNO 909 / graphic 100071 / PETSKILL2;
  - TEMPNO 1165 / graphic 101814 / PETSKILL4.

The runtime admission bridge rechecks TEMPNO, graphic identity, exact skill
slot, exact ID and exact row metadata. A same-number synthetic template is not
accepted.

## 2. Symbolic command and COM2 carrier

The recovered original numeric `BATTLE_COM_S_ENEMYRELIFE` is not known.
Later descendants disagree: gavin/iris compile 2013 while fixed Bismarck
compiles 2012.

R1 therefore never assigns a historical numeric ReLife COM1.

The common enemy AI still performs its ordinary target selection on living
player-side slots 0..9. The resulting target is preserved as a modern internal
ATTACK scheduling/COM2 carrier only. It has two source-shaped roles:

1. it is adjusted by the ordinary TargetAdjust path before ReLife may execute;
2. if ReLife finds no eligible dead ally, the already-adjusted carrier becomes
   the target of the physical ATTACK fallback.

It is **not** interpreted as the resurrection target.

## 3. Active actors versus retained battle entries

The runtime now distinguishes two concepts that the fixed battle array already
separates:

- **active actors**: living entries that own a command, initiative value and
  action position;
- **retained battle entries**: dead enemy entries that still occupy their
  original battle slot and may be inspected by ReLife.

A retained dead entry does not receive a command and does not re-enter
initiative merely because it remains addressable.

The bounded R1 revivable domain is enemy-side only. Player-side deaths are not
placed in ReLife state. This matches the accepted enemy-caster helper, whose
candidate scan is slots 10..19.

Ordinary enemy death can remain revivable only while the entry stays in the
battle identity/slot graph. Ultimate removal and admitted BATTLE_Exit paths
remove that eligibility.

## 4. TargetAdjust and no-target ordering

Before the semantic ReLife helper is entered, the ATTACK carrier runs the same
ordinary target adjustment used by the fixed dispatcher.

- live valid COM2: consumes no retarget draw;
- dead/invalid COM2 with living opposing candidates: consumes the existing
  ordinary retarget witness;
- no living opposing target: emits `enemy_relife_no_target`, consumes no
  ReLife effect RNG, performs no resurrection and performs no physical
  fallback.

This last case is distinct from "TargetAdjust succeeded but there is no dead
ally".

## 5. Dead-entry selection

After TargetAdjust succeeds, the ReLife effect independently scans enemy slots
**10..19 in ascending order**.

An R1 candidate is a retained ordinary-dead enemy entry representing the fixed
source conditions:

- valid battle entry;
- HP 0;
- dead/attacked/actionable state;
- not rescue mode;
- not ultimate-exited;
- not otherwise battle-exited.

No candidate:

- consumes no ReLife target-selection draw;
- consumes no ReLife amount draw;
- returns the semantic fallback result.

One or more candidates:

- consumes exactly one explicit reduced
  `RAND(0, candidate_count - 1)` witness;
- the source call is retained even when candidate_count is one.

## 6. Resurrection amount and mutation

For the selected target:

`base_power = target.max_hp // 2`

mirrors positive C integer division of WORKMAXHP by two.

For nonzero base power, the next explicit witness is bounded by the fixed
source conversion of the 90–110% RAND endpoints:

- lower = floor(base_power * 0.9);
- upper = floor(base_power * 1.1).

The resolved recovery amount is at least one, target HP is capped at max HP,
and the dead flag is semantically cleared.

The successful action:

- writes the revived HP into the working round state;
- removes the target from the revivable-dead set;
- consumes no ordinary physical attack RNG;
- leaves the revived entry available as a target for later actions in the
  same round;
- makes it an ordinary living actor again on the next command round.

## 7. Failed effect and physical fallback

If TargetAdjust succeeded but no eligible dead enemy exists, the effect returns
FALSE and the dispatcher falls back to ordinary physical ATTACK.

R1 preserves the fixed ordering:

- the fallback attacks the **already-adjusted** COM2 target;
- there is no second fallback retarget draw;
- ReLife target/amount RNG must be empty on this path;
- ordinary attack dodge/critical/damage/counter behavior remains owned by the
  existing base attack resolver.

## 8. Same-round and persistent behavior

The ordered resolver records an ordinary non-ultimate enemy death as a retained
revivable entry immediately. A later ReLife actor in the same round may revive
it.

Persistent state carries those retained enemy identities across rounds while
their HP remains zero and the battle entry remains present.

A successful later-round ReLife removes the identity from that set and restores
positive HP. The following round therefore requires a command/initiative input
for the revived enemy again.

Death-profit timing is not rolled back by resurrection. Existing pending EXP
or other already-applied AddProfit-equivalent bookkeeping remains intact after
the unit is revived.

A late regression exposed an important bound: player-side pet death must not
enter this enemy ReLife set. The final implementation and validation enforce
enemy-side revivability explicitly.

## 9. Recovered enemy-AI admission

The local runtime coordinator admits ReLife only when recovered normal enemy
AI selects the exact positive `wa[]` slot of an accepted ID-500 template.

The coordinator returns a typed `EnemyAiReLifeSubmission`, plus the ordinary
ATTACK scheduling carrier. Numeric ReLife COM1 is absent from that type.

ReLife effect RNG and TargetAdjust RNG are caller-owned explicit inputs whose
actor keys must exactly match selected ReLife actors; surplus, missing or
wrong-type inputs fail closed.

## 10. Explicitly open boundaries

R1 does **not** establish:

- recovered original executable/compiler/profile identity;
- original numeric ReLife COM1;
- original JSS/Taiwan-v1 introduction or membership;
- the pet-caster defNo branch;
- PvP player resurrection behavior beyond the documented shared-helper
  exclusion;
- rescue-mode resurrection;
- exact libc PRNG internal-state identity;
- every possible later expansion interaction that can manufacture a dead
  battle entry outside the accepted ordinary runtime graph.

These are not inferred from the recovered25 positive enemy-use closure.

## 11. Acceptance gates

Reference gates:

- fixed-source + first preservation probe: **37288674220 PASS**;
- exact recovered row/template pin: **37288913119 PASS**.

Runtime gates:

- final dedicated ReLife model/admission/ordered/persistent/coordinator gate:
  **37293702272 PASS**;
- battle-core regression after enemy-side revivable correction:
  **37293114252 PASS**;
- local runtime coordinator: **37293114108 PASS**;
- runtime golden contract: **37293113921 PASS**;
- Taiwan-v1 gameplay aggregate: **37293114173 PASS**;
- AttackMagic round execution aggregate: **37293113816 PASS**;
- recovered25 full-region/runtime-stack: **37293113718 PASS**.

The source-affecting correction commit passed all **26** triggered relevant
workflows with zero failures.

Final pressure acceptance:

- verified preservation-bundle pressure workflow: **37293804945 PASS**;
- derived report write-back commit:
  `420e34a7a29aa06a37ea45e55369afd1b01a80fd`;
- `ENEMYSKILL_ReLife` = **closed_runtime**, ID500,
  **3 uses / 3 templates**;
- unresolved positive skill IDs = **0**;
- accepted executable positive-slot coverage advances from
  **2448/2486 = 98.47%** to **2451/2486 = 98.59%**.

The verified report mechanically selects the next OPEN family:
**PETSKILL_Lighttakeed / IDs 610,611 / 3 uses / 2 templates**.

**RECOVERED25_RELIFE_ORDERED_RUNTIME_R1 =
CLOSED_BOUNDED_RECOVERED25_ORDERED_RUNTIME.**
