# StoneAge 2BattleTimid ordered runtime R1

**2026-10-06 correction:** the earlier source-slot table below is superseded
by the dated correction at the end. Historical runtime acceptance did not
detect a bridge/fixture slot-base regression. The corrected exact admission
requires renewed remote actual-data and regression acceptance.

Status: **CLOSED_BOUNDED_RECOVERED25_ORDERED_RUNTIME**
Date: 2026-10-05
Scope: exact recovered25 positive enemy uses of `PETSKILL_2BattleTimid`.

## Evidence and exact admission

The accepted reference is
`specs/STONEAGE-2BATTLETIMID-REFERENCE-R1.md`; owner/default-pet/recall
state preconditions are pinned in
`specs/STONEAGE-2BATTLETIMID-RUNTIME-STATE-AUDIT-R1.md`.

The complete recovered25 callback population is exactly **ID636**:
FIELD1 / TARGET7 / COST2 / ILLEGAL10000, with a 17-byte non-NUL OPTION
whose SHA-256 is
`8e6b5dd952bf3bc81e522f1df382db48473b1aeec13f9ff08c7bb76d2c06f9e5`.

Only the two exact positive placements can construct the typed runtime
submission:

| TEMPNO | Graphic | Source slot (one-based) | ID |
| --- | ---: | ---: | ---: |
| 178 | 101872 | 4 | 636 |
| 179 | 101873 | 4 | 636 |

The submission binds participant, exact template/graphic/seven-slot identity,
ID636, callback, source target, raw OPTION identity and an explicit execution
charset profile. `ATTACK` is only the modern ordering carrier. It does not
claim the original numeric COM1 and does not grant ordinary combo/counter
semantics.

Because the preserved executable does not discriminate the original callback
charset, both accepted conditional profiles remain explicit:

- `utf8_literals`: actual recovered OPTION does not match the guarded markers;
  setup powers remain unchanged and recall chance is 0;
- `big5_literals`: attack becomes fixed attack minus 50%, defence remains
  unchanged, quick becomes fixed quick plus 30%, and recall chance is 60.

No original compiler/executable/charset profile is selected.

## Authoritative pet state

DD-020 applies. Ownership, default selection and active battle occupancy are
independent.

Persistent player state now carries nullable `default_pet_slot`. Persistence
schema advances to `stoneage.singleplayer.persistence.r4`; r1/r2/r3 payloads
migrate without inventing a selected pet. A missing historical selection is
therefore represented as no authoritative selection, not inferred from the
first or only owned pet.

Persistent battle state carries:

- the selected roster slot independently of the allied-pet collection;
- battle-local `NORETURN` state, supplied explicitly and validated against
  allied pet identity;
- retained battle-exit identity independently of owned-pet persistence.

For a pet target, R1 admission requires the target to be the explicitly
selected default pet, to retain its source roster slot, and to occupy the
normal owner-aligned battle slot (`owner slot + 5`). The NORETURN witness is
mandatory. Invalid/missing owner/default/NORETURN state fails closed.

World save persists the selected roster state, but active coordinator battle
context is still not a disk-resume contract. This runtime does not claim
mid-battle save/restore.

## Ordered setup, damage and RNG

The callback setup is applied before initiative/order using the selected
conditional profile. Prepared Weaken composition and mounted ride composition
remain outside R1 and fail closed. The semantic actor is excluded from ordinary
combo rewriting and ordinary counter inheritance.

The effect is evaluated only after the ordinary specialized physical damage
path reaches the post-damage seam. Target substitution and Guardian redirect
compositions that are not closed by the accepted reference fail closed.

Source ordering is preserved:

1. zero/nonpositive damage and an already-active original defender reaction
   demote the post effect;
2. a remaining positive event owns exactly one explicit reduced
   `rand()%100` draw;
3. the draw occurs before the `damage > 1` and pet-type checks, matching the
   accepted descendant ordering;
4. player/non-pet targets can therefore consume the owned draw but cannot
   recall a pet;
5. successful selected-pet recall calls the semantic PetIn/PetDefaultExit
   lifecycle; NORETURN blocks withdrawal/default clear but does not suppress
   the two outer status notifications.

Missing, extra, invalid or unowned draws fail closed. No libc PRNG stream is
fabricated.

## Recall, death and persistence semantics

A successful recall:

- clears the selected default roster slot;
- marks the pet battle entry exited for later actions/rounds;
- preserves the owned pet object and its HP;
- emits the accepted recall/BS semantics;
- does not convert recall into pet death.

A NORETURN-blocked recall:

- keeps the selected roster slot;
- keeps the pet battle entry active;
- emits the outer notifications but no withdrawal BS;
- remains active in the next round.

Event ordering is authoritative inside the round. If a successful recall
occurs before a later player death, the later player-death loyalty penalty sees
no selected default pet and cannot penalize the recalled pet. Existing death
fixtures were changed to state DEFAULTPET explicitly rather than restoring the
old “only allied pet == default pet” inference.

Battle settlement writes the terminal default selection into persistent player
state. End-to-end coordinator tests then save and continue the world session:
the recalled pet remains owned while selection stays cleared; the
NORETURN-blocked pet remains owned and selected.

## Explicit exclusions

The following remain OPEN and are not silently normalized:

- original numeric COM1 / guarded enum identity (descendant command 2005 does
  not close the original build under DD-019);
- original compiler/executable/charset and libc PRNG state;
- prepared-Weaken, mounted ride and unresolved Guardian redirect compositions;
- invalid owner/default-pet mappings and exotic non-owner-aligned recall
  layouts;
- original JSS/Taiwan-v1 membership;
- active-battle disk resume.

## Acceptance evidence

- Production integration culminates at
  `3e243db19b398d5382b63d5e48e7bf7abd252c89`, tree
  `e771cf74249c108ac0dc1bccc4f0dca631f8bd42`.
- Final cross-round NORETURN witness is
  `f421f673e6c5a988f314ca8b7c3904b8709f69c5`, tree
  `8581e827d07568e24821e40e88fc124217f4fd0f`.
- Dedicated 2BattleTimid gate **37321077390 PASS**: **25 tests**, including
  conditional reference behavior, successful/blocked recall, true next-round
  NORETURN persistence, player-target draw ownership, later player-death
  selection, persistence migration and coordinator settlement/save/continue.
- Full local runtime session coordinator **37320486287 PASS**.
- Battle core regression **37319322994 PASS** after legacy death fixtures were
  made explicit about DEFAULTPET.
- Runtime golden contract **37319726838 PASS** with persistence schema r4.
- Full recovered25 region/runtime stack **37320486193 PASS**: deterministic
  region/runtime tests, verified preservation bundle, materializable map
  payloads, concrete runtime stack, AttackMagic cross-links, server collision
  audit/provider and client ADRN collision audit all pass.
- Hash-verified pressure **37320722163 PASS**; derived report write-back
  `392e26d39210ac2a8583fc0d07559a0f0af9f173`, tree
  `6921e42ee8de68533fb815be0effa00a41b37a93`.
- Pressure report marks exact ID636 **closed_runtime**, **2 uses / 2
  templates**, with unresolved positive skill IDs still zero. Accepted
  executable positive-slot coverage advances from **2457/2486 = 98.83%** to
  **2459/2486 = 98.91%**. This is a recovered25 enemy skill-slot metric, not
  whole-game reconstruction completion.
- The next OPEN callback is mechanically selected as
  **`PETSKILL_BatFly` / ID633 / 2 uses / 1 template**.

**RECOVERED25_2BATTLETIMID_ORDERED_RUNTIME_R1 =
CLOSED_BOUNDED_RECOVERED25_ORDERED_RUNTIME.**

## Exact admission slot-base correction — 2026-10-06

**FACT:** the independently accepted recovered25 probe and derived report
identify ID636 in source skill column **3**, for both TEMPNO178 and179.
`Recovered25EnemyBaseTemplate.skill_slot_ids` retains all seven columns as a
zero-based tuple. Consequently the runtime selected index must be **2**.
The earlier table's source column4 and the bridge/test index3 were wrong;
the original evidence record above is retained and explicitly superseded.

| TEMPNO | Graphic | Source column (one-based) | Runtime index (zero-based) | ID |
| --- | ---: | ---: | ---: | ---: |
| 178 | 101872 | 3 | 2 | 636 |
| 179 | 101873 | 3 | 2 | 636 |

The bridge now rejects the shifted fourth column and duplicate positive
placements. Typed submissions also require index2. Regression tests derive
the index from the independent exact-data probe, and coordinator fixtures
place the skill and AI weight in the real third column. The hash-verified
BattleModel admission probe additionally checks both real ID636 templates
under both explicit charset profiles.

**OPEN:** renewed remote actual-data, dedicated runtime, coordinator, core,
golden and full-region acceptance. This correction does not change the
accepted conditional recall semantics, pet lifecycle or persistence schema.
Historical pressure percentages above are not fresh certification of this
repaired admission path.
