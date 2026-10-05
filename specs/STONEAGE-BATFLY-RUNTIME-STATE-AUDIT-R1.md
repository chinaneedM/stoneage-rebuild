# StoneAge BatFly runtime state audit R1

Status: **CLOSED_FOR_BOUNDED_RUNTIME_INTEGRATION**
Date: 2026-10-05

This audit maps the accepted BatFly reference onto the existing deterministic
single-player battle state before any ID633 runtime coding.

## Existing state already sufficient

The modern battle stack already models the source distinction needed by
BatFly:

- `BattleSession.player` is the player battle entry;
- `BattleSession.allied_pets` are active pet battle entries;
- `BattleSession.ride_pet` is a separately owned pet snapshot and is not
  intended to be an active battle entry;
- `PersistentBattleState.ride_pet_runtime` carries battle-local ride pet HP,
  max HP, defense power, mounted state and PETFALL state;
- `RidePetRuntime` binds explicit `rider_id` and `pet_id`;
- common `ride_pet_lookup_allowed` accepts only rider kind `player`, matching
  recovered `BATTLE_getRidePet` behavior.

No new generalized mount subsystem is required for BatFly R1.

## Persistent-world round trip

At battle exit, the existing single-player settlement projection maps
`state.ride_pet_runtime.hp` back to the ride pet's persistent roster slot.
The existing battle-exit seam clamps terminal pet HP to at least 1; BatFly
runtime must not bypass or redefine that already-accepted exit rule.

Within battle, however, BatFly may reduce the ride pet to 0. The runtime must
preserve that exact battle-local zero HP, clear mounted state and set PETFALL
before ordinary terminal settlement later projects the persistent roster.

## BatFly target projection

For an enemy ID633 actor:

- target membership is all living player-side battle entries;
- dead/HP<=0/removed entries are excluded before the effect;
- the player target may additionally reference the one separate
  `ride_pet_runtime`;
- allied pet entries can never use that player ride lookup and must receive the
  10% unmounted branch;
- the ride pet itself is not separately enumerated as an active target entry,
  so it cannot be double-drained.

For the admitted recovered25 runtime, the BatFly actor is the enemy template
identity TEMPNO1160 / graphic101815 with ID633 in source slot1 or slot4.

## Required fail-closed invariant — implemented

A single owned pet must not simultaneously be represented as:

1. an active `BattleSession.allied_pets` entry, and
2. `BattleSession.ride_pet`.

This is now rejected during `PersistentBattleState` construction, before any
round can execute. Core invariant commit:
`adf00d237d7f9ac25c6359f2587870827d079da1`; regression witness:
`8795f24cd0c169c8c5871d4deca904303af8500f`.

The terminal exit projection retains its existing duplicate-state rejection as
a second line of defense.

## Slot order versus source presentation order

`PersistentBattleState.slots` carries the authoritative battle slot mapping
needed to identify the two sides and to produce deterministic modern event
output.

The source's multi-target presentation uses `qsort(SortLoc)`, but the
preserved side-0 comparator contains an anomalous term and R1 does not claim a
portable original qsort order. Runtime may use a deterministic slot-based
event order while preserving the exact **target set and state transform**.
Such order must be labeled modern deterministic presentation, not recovered
original protocol order.

## RNG ownership contract

BatFly callback and whole-side HP effect own no RNG, but the dispatcher-level
`BATTLE_TargetAdjust` gate can own one draw before the effect:

- live submitted COM2: **0 draws** and any supplied retarget draw is rejected;
- dead/invalid submitted COM2 with N>0 living opposing entries: exactly **one
  explicit 0..N-1 DefaultAttacker draw** is required;
- no living opposing entries: **0 draws**, no-action, and any supplied draw is
  rejected.

The unrelated single-target `BATTLE_MultiList` retarget RNG is still not
reachable from BatFly's whole-side selector. Runtime must expose only the
conditional TargetAdjust draw above and must not fabricate a PRNG stream.

## Runtime implementation requirements

The runtime branch must:

1. add exact ID633 recovered25 admission and an enemy-AI submission bridge;
2. bind TEMPNO1160 / graphic101815 / source slot1-or4 and all exact skill
   metadata, including empty OPTION identity;
3. execute as a special whole-side action rather than ordinary physical
   attack;
4. evaluate only living active opposing battle entries;
5. apply 10% minimum-one drain to ordinary entries;
6. apply player+ride-pet 5%/5% minimum-one split only when a living mounted
   ride pet is present;
7. update `RidePetRuntime` to unmounted+PETFALL when its HP reaches zero;
8. heal the BatFly actor by total drain, preserving the overflow
   reported-heal-zero quirk;
9. preserve exact conditional TargetAdjust draw ownership and consume no RNG
   in the whole-side effect itself;
10. preserve standard persistent battle termination and standard ride-pet
    battle-exit projection;
11. preserve the now-core active-pet/ride-pet identity-overlap rejection;
12. leave 101813/101814 Ler transform/anti-knockout behavior outside ID633.

**BATFLY_RUNTIME_STATE_AUDIT_R1 =
CLOSED_FOR_BOUNDED_RUNTIME_INTEGRATION.**
