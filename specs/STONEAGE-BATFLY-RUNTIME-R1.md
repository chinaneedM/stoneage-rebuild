# StoneAge BatFly ordered runtime R1

Status: **CLOSED_BOUNDED_RECOVERED25_ORDERED_RUNTIME**
Date: 2026-10-05
Scope: exact recovered25 positive enemy uses of `PETSKILL_BatFly`.

## Evidence and exact admission

The accepted source/reference boundary is
`specs/STONEAGE-BATFLY-REFERENCE-R1.md`; the state preconditions are pinned in
`specs/STONEAGE-BATFLY-RUNTIME-STATE-AUDIT-R1.md`.

The complete recovered25 callback population is exactly **ID633**:
FIELD1 / TARGET3 / COST2 / ILLEGAL5000, with an empty OPTION whose SHA-256 is
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

Only the exact positive placements on the one recovered template can construct
the typed runtime submission:

| TEMPNO | Graphic | Source slot (one-based) | ID |
| --- | ---: | ---: | ---: |
| 1160 | 101815 | 1 | 633 |
| 1160 | 101815 | 4 | 633 |

The exact template base identity is V/S/T/D **300/1/1/30**, AI **100**.
Admission validates the complete seven-slot identity. `ATTACK` is only the
modern action-order carrier; it does not claim the unresolved historical
numeric COM1 and does not inherit ordinary physical combo/counter semantics.

## Dispatcher gate and RNG ownership

The callback itself reads no OPTION and owns no RNG. The only admitted RNG is
the dispatcher-level TargetAdjust gate:

1. a live submitted COM2 target consumes **0 draws**;
2. a dead/invalid submitted COM2 with N living opposing candidates requires
   exactly one explicit reduced draw in **0..N-1**;
3. no living opposing candidate is a no-action path and consumes **0 draws**.

Supplying a draw where none is owned, omitting the required draw, or supplying
an out-of-range draw fails closed. No PRNG stream is fabricated.

After the gate succeeds, BatFly rebuilds the complete living opposing side and
owns no further RNG.

## Whole-side state transform

BatFly executes as a dedicated semantic action, not as ordinary physical
AttackSeq/DamageSub. It therefore does not consume physical dodge, critical,
counter, combo or damage rolls.

For every living opposing battle entry, deterministic modern event output is
ordered by battle slot. This is a state/projection convention only; it does not
claim the preserved descendant qsort presentation order.

Per target:

- ordinary living entry: drain `floor(current_hp / 10)`, minimum 1;
- player with a living mounted ride pet: player drain
  `floor(current_hp / 20)`, minimum 1, and the separate ride pet drains
  `floor(ride_hp / 20)`, minimum 1;
- allied pet entries never perform the player ride lookup and use the 10%
  branch;
- the non-entry ride pet is never enumerated as a second active target, so it
  cannot be double-drained.

One HP transition event is emitted per affected active battle entry. Existing
persistent death/penalty/termination projection consumes those transitions.
The enemy BatFly actor receives no player-side EXP/drop profit.

## Ride-pet and healing semantics

The accepted `BattleSession.ride_pet` / `RidePetRuntime` separation is
reused directly. If BatFly reduces ride-pet HP to zero, battle-local state
becomes unmounted with PETFALL set. The existing terminal settlement later
projects ride-pet HP through the already-accepted persistent roster rule.

The BatFly actor heals exactly once by the sum of all player-side and ride-pet
drain amounts. Actor HP is capped at max HP. The preserved reporting quirk is
kept: if `attacker_hp + total_drain` would exceed max HP, actual HP still caps
normally but source-reported heal is **0** rather than the applied capped
difference.

## State and ordering boundaries

The runtime preserves the audit invariant that one owned pet cannot
simultaneously be an active allied battle entry and the separate ride pet.
That invariant is rejected at persistent battle construction.

Base-status command rewrite remains authoritative. If confusion replaces the
BatFly carrier command, the BatFly semantic action is removed for that actor.
BatFly actors are excluded from ordinary combo rewrite and ordinary counter
inheritance.

Neighboring Ler graphic behavior for 101813/101814 is not imported into
graphic101815/ID633.

## Explicit exclusions

The following remain OPEN:

- original numeric COM1 / guarded enum identity under DD-019;
- original JSS/Taiwan-v1 BatFly membership;
- portable identity of the preserved qsort/SortLoc presentation order;
- original libc PRNG state;
- active-battle disk resume;
- unrelated Ler transform/anti-knockout semantics.

## Acceptance evidence

- Runtime implementation chain starts at
  `12cf7594376ee5ec2e4c54a46efa493154b0a3bc` and reaches the exact-template
  regression at `c1c9e8827ea08519f9ad79659ea204eb00b5c20b`, tree
  `25011d84cbd28466a4c9eaab687fe05d91fb1c27`.
- Dedicated BatFly gate **37334364213 PASS**: **15 tests**, covering reference
  setup/effect, TargetAdjust draw ownership, whole-side runtime, ride-pet
  split/PETFALL, overflow reporting and coordinator routing.
- Full local runtime coordinator **37334363921 PASS** on the same runtime head.
- Representative adjacent runtime gates including 2BattleTimid
  **37334364243 PASS**, AttackMagic coordinator **37334364476 PASS**,
  FallGround **37334364164 PASS**, MpDamage **37334364259 PASS**, Combined
  **37334364440 PASS**, BattleTimid **37334364077 PASS** and Modifyattack
  **37334364521 PASS**.
- Runtime golden contract **37334626700 PASS**.
- Hash-verified pressure **37334620980 PASS**; derived write-back
  `59ece605d56e16f700361f8cb23edac9ff2e7f5b`, tree
  `a902b99c95665a5777ea752838dfb1ec41479e35`.
- Pressure marks ID633 `closed_runtime`, leaves unresolved positive skill IDs
  at zero, and advances accepted executable positive-slot coverage from
  **2459/2486 = 98.91%** to **2461/2486 = 98.99%**.
- The next OPEN callback is mechanically selected as
  **`PETSKILL_BattleModel` / ID638 / 2 uses / 2 templates**.
- Full recovered25 region/runtime stack **37334364405 PASS**: deterministic
  region/runtime tests, verified preservation recovery, all materializable map
  payloads, concrete runtime stack, AttackMagic cross-links, server collision
  audit/provider and client ADRN collision audit all pass.

**RECOVERED25_BATFLY_ORDERED_RUNTIME_R1 =
CLOSED_BOUNDED_RECOVERED25_ORDERED_RUNTIME.**
