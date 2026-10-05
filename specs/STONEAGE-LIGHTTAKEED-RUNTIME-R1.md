# StoneAge Lighttakeed ordered runtime R1

Status: **CLOSED_BOUNDED_RECOVERED25_ORDERED_RUNTIME**
Date: 2026-10-05  
Scope: recovered25 positive enemy uses of `PETSKILL_Lighttakeed`.

## Evidence and admission

The complete callback population is 609/610/611. Runtime admission is limited
to positive IDs610/611: TEMPNO70, graphic101550, slot4 -> 610; TEMPNO157,
graphic101283, slots4/5 -> 610/611. Zero-reference ID609 remains part of the
data/population check without becoming an executable enemy use.

Admission validates exact FIELD/TARGET/COST/ILLEGAL 1/7/2/5000, six-byte
non-NUL OPTION hashes, template/graphic/slot identity and explicit source
profile. Typed submissions independently bind skill610 to REFLEC/slot4 and
skill611 to VANISH/slot5, so direct runtime callers cannot relabel an effect.

The executable discriminator remains inconclusive: the preserved tree exposed
one 273-byte ELF candidate with neither the Lighttakeed callback nor
AttackDamage symbol. It cannot identify original counter-copy behavior.

## Commands and preparation

`EnemyAiLighttakeedSubmission` preserves symbolic `BATTLE_COM_S_LIGHTTAKE`.
ATTACK is a modern scheduling/target carrier, not historical numeric COM1.
Agreement among descendant numeric command values does not close DD-019.

The callback has no local RNG and snapshots attack to fixed STR*0.7 and
defense to fixed TOUGH*0.5. It does not modify QUICK. Those work powers are
action preparation state; persistent base participant attributes are retained.
The carrier does not give the caster ordinary ATTACK counter/combo eligibility.

The ordinary TargetAdjust/attack machinery owns retarget, dodge, critical,
damage and any eligible counter witnesses. There is no added Lighttakeed
effect draw. No valid target cannot perform a transfer. A dodge enters the
zero-damage result and neither consumes nor transfers a reaction charge.

## Reaction transaction

Active reaction priority is VANISH, ABSROB, REFLEC. A matching Lighttakeed
marker neutralizes the outer local reaction; positive damage still enters
DamageSub, which re-fetches and consumes the ordinary active reaction.
An active marker mismatch demotes the Lighttakeed effect to ordinary handling.
Zero damage is also demoted before the post-damage switch.

The post branch observes the state after DamageSub:

- VANISH/ABSROB consume one defender charge; transfer observes the remainder.
- Non-throwing REFLEC consumes one defender charge and redirects the outer
  defender identity to the attacker; transfer consequently reads the attacker's
  own reflect count.
- Throwing REFLEC bypasses reflection and charge consumption; the pure reference
  seam reads the unchanged defender count. This is a conditional helper witness,
  not additional positive enemy-use provenance.

Source profiles are caller-selected and remain separate:

| Profile | Attacker counter assignment |
| --- | --- |
| `gavin_iris_copy` | Observed counter value |
| `bismarck_copy_plus_one` | Observed counter value plus one |

In particular, non-throwing REFLEC is a self-copy for gavin/iris and an increment
of the attacker count for Bismarck. The reference-only phrase “copy defender
counter” must not flatten this post-DamageSub identity change.

## Persistence and bounded exclusions

Battle-local `BaseDamageReactState` carries mutated counts between rounds.
Later ordinary hits consume transferred charges through the shared reaction
model. Exhausted VANISH stops protecting on the next hit. The next round does
not replay the previous Lighttakeed semantic submission.

The independent persistent witness starts with two defender VANISH charges,
then proves one transferred charge under copy and two under copy+1, their
subsequent exhaustion, resumed HP damage and retained base attack/defense.

Persistent Lighttakeed rejects inactive actors, overlapping semantic skills,
drunk work-power state and prepared Weaken/SetMagicPet powers. Those excluded
compositions are not silently treated as baseline stats.

Original compiler/profile, libc PRNG identity, original numeric COM1 and
JSS/Taiwan-v1 membership remain OPEN. This later recovered25 closure cannot
establish whole-game restoration or the earliest historical implementation.

## Acceptance evidence

- Model/admission/ordered/coordinator gate after skill-identity hardening:
  **37299772670 PASS**.
- Integrated cross-round gate: **37299752226 PASS**; independent acceptance
  branch gate **37299497150 PASS**.
- Coordinator after dispatch correction: **37299249647 PASS**.
- Runtime golden contract: **37299249686 PASS**.
- Local related regression before final identity hardening: **247 tests PASS**;
  golden-contract CLI PASS. The final hardening plus pressure fixture is covered
  by the subsequent **258-test** local regression.
- Verified preservation pressure: **37299752243 PASS**; report commit
  `26afc10ee71572d09fffce2413ff13dc6c590e72`.

The pressure report classifies Lighttakeed closed for three uses/two templates,
with zero unresolved positive skill IDs. It mechanically selects
`PETSKILL_Modifyattack`, IDs544/545/546, three uses/three templates next.

Final **37299249771 full-region/runtime-stack PASS** accepts the production
settlement/coordinator correction at `f419837b6625a7a23567f8d961039848a496dd33`.
The later typed identity guard is independently accepted by dedicated
**37299772670 PASS**; it tightens admission without changing accepted effects.
The subsequent pressure and multi-round tests are separately pinned above.

Accepted executable positive-slot coverage advances from
2451/2486 = 98.59% to **2454/2486 = 98.71%**. This is a recovered25 enemy
skill-use metric, not a whole-game completion percentage.

**RECOVERED25_LIGHTTAKEED_ORDERED_RUNTIME_R1 =
CLOSED_BOUNDED_RECOVERED25_ORDERED_RUNTIME.**
