# StoneAge combat-profile provenance bridge — R1

Date: 2026-09-20

Status: **stable-descendant evidence bridge / reconstruction-safe adapter; exact JSS-1999 server work-stat provenance remains OPEN**

## Purpose

The ordinary battle resolver needs fixed DEX, fixed LUCK, four fixed elemental
values and weapon critical. Earlier reconstruction stages deliberately kept
those values explicit rather than equating them with similarly named
client-facing fields.

This R1 closes only mappings supported by the preserved status/work-stat and
pet-birth lineage. It also records where provenance is still insufficient.

## 1. Player mapping

The stable descendant status producer exposes the player dexterity display as
the same numeric projection produced for `WORKFIXDEX` by the corresponding
work-stat initialization path.

The bridge therefore accepts the v1 player status `dexterity` value as the
numeric fixed-DEX projection.

The stable status path exposes fixed LUCK and the four fixed elemental work
values directly, so the bridge maps:

- `luck` -> fixed LUCK;
- `earth`, `water`, `fire`, `wind` -> fixed elemental values.

Missing required fields fail explicitly.

Weapon critical remains an explicit caller input because it belongs to the
equipment/combat context rather than the base player status record.

## 2. Pet/enemy fixed DEX must come from birth provenance

For reconstructed pets and spawned enemies the bridge uses preserved
`PetBirthBridgeState.internal_dexterity` and the work-stat projection:

`fixed_dex = int(internal_dexterity * 0.01)`

A generic persisted/client-facing pet `quick` value is not treated as fixed
DEX. That field represents current QUICK and can diverge from the original
fixed-Dex source.

Consequently:

- allied-pet combat profiles require a provenance-bearing
  `ReconstructedPetBridgeState`;
- enemy combat profiles require their concrete `SpawnedEnemy` record;
- participant/template/variant identity must match the battle session.

This prevents a later presentation/runtime mutation from silently rewriting
the underlying combat-profile provenance.

## 3. Fixed elemental projection from birth state

The reconstructed birth source preserves raw earth/water/fire/wind values.

The bridge mirrors the stable work-stat initialization ordering: for each
positive element in source order, the opposite element is assigned the
negative value, after which the battle attribute path clamps negative values to
zero.

The ordering matters when source values contain mixed positive entries; R1
therefore preserves the overwrite behavior rather than replacing it with a
cleaner symmetric normalization.

## 4. Runtime group bridge

Implementation:

- `tools/stoneage_combat_profile_bridge.py`
- `SinglePlayerHistoricalRuntime.build_group_battle_combat_profiles()`

For one `BattleSession`, the group bridge requires provenance-bearing inputs
for every player-side pet and every spawned enemy and then checks that the
resulting profile map covers exactly all battle participants.

No missing profile is synthesized from display QUICK or another convenient
lookalike field.

## 5. Regression correction

Commit `124f382826fff48842afa6526478c9741565a8a0` changed the group-runtime
test to use the new provenance bridge, but the test then mutated an enemy
participant's `quick` to 40 and incorrectly expected the birth-derived
`fixed_dex` to become 40.

The actual provenance-derived value remained 26. Commit
`0fa2fc22133dddf41686053079a53adf5d75df31` corrected the assertion to pin
the desired behavior:

- fixed DEX remains tied to the spawn/birth source;
- mutating the participant display/runtime QUICK does not retroactively change
  the combat profile.

## Validation

Relevant regression coverage:

- `tests/test_stoneage_combat_profile_bridge.py`
- `tests/test_stoneage_group_battle_runtime.py`

Remote validation:

- **35513757842** — success.

## Evidence boundary

This bridge is sufficiently constrained for reconstruction use, but it does
not promote descendant server internals to byte-proven JSS-1999 facts.

In particular, any future original server/client evidence that changes the
fixed-stat mapping must supersede this bridge through an explicit versioned
profile rather than silently changing the historical record.
