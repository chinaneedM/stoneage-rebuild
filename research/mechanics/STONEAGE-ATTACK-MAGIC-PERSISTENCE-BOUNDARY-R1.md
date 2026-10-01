# StoneAge AttackMagic persistence boundary R1

Date: 2026-10-01

## Decision

Keep `AttackMagicRoundOverlay` battle-local in the current Taiwan-v1-oriented
local persistence contract.

Do **not** inject descendant AttackMagic fields into `PlayerState.fields` or
`PetActor.state` merely because later fixed servers persist them. Those
engine-facing records currently follow the recovered Taiwan-v1 client gameplay
schema, whose full player/pet status records expose ordinary four-element
attributes but no AttackMagic proficiency/resistance/training fields.

This is a provenance boundary, not a claim that the later fields are transient.

## Fixed-descendant server evidence

Pinned fixed descendants place AttackMagic state in `Char.data[]` under the
AttackMagic compile feature. The convergent layout contains four groups of four
integers:

1. proficiency levels: `CHAR_EARTH_EXP`, `CHAR_WATER_EXP`, `CHAR_FIRE_EXP`,
   `CHAR_WIND_EXP`;
2. resistance levels: `CHAR_EARTH_RESIST`, `CHAR_WATER_RESIST`,
   `CHAR_FIRE_RESIST`, `CHAR_WIND_RESIST`;
3. attack-magic training experience: `CHAR_EARTH_ATTMAGIC_EXP`,
   `CHAR_WATER_ATTMAGIC_EXP`, `CHAR_FIRE_ATTMAGIC_EXP`,
   `CHAR_WIND_ATTMAGIC_EXP`;
4. defense-magic/resistance training experience:
   `CHAR_EARTH_DEFMAGIC_EXP`, `CHAR_WATER_DEFMAGIC_EXP`,
   `CHAR_FIRE_DEFMAGIC_EXP`, `CHAR_WIND_DEFMAGIC_EXP`.

In `gavinlinasd/StoneAge@1f90cb6c`, `CHAR_setintdata` gives matching save keys:
`earth_exp`/`water_exp`/`fire_exp`/`wind_exp`, the four `*_resist` keys, the
four `*_attmagic_exp` keys and the four `*_defmagic_exp` keys. Iriselia and
Bismarck descendants independently retain the same four groups; their
default-player tables initialize them to zero.

## Player save/load evidence

The pinned gavin descendant's `CHAR_makeStringFromCharData` iterates every
`i < CHAR_DATAINTNUM` and serializes `CHAR_setintdata[i]=one->data[i]`.
`CHAR_makeCharFromStringToArg` performs the inverse lookup across every
`CHAR_DATAINTNUM` entry and restores `one->data[i]`.

Therefore, when the AttackMagic feature is compiled into this descendant, the
sixteen fields above belong to the server-side player persistence payload.

## Pet save/load evidence

The same descendant embeds owned pets in the player save through
`CHAR_makePetStringFromPetIndex`. That function also iterates every
`i < CHAR_DATAINTNUM` and serializes the pet integer data by
`CHAR_setintdata`. `CHAR_makePetFromStringToArg` scans that same full table
and restores matching values into `ch->data[i]`.

Thus fixed-descendant server persistence structurally retains the same
AttackMagic fields for pets as well as players.

## Runtime semantics

The fixed magic battle implementation keeps the groups distinct:

- enemy attack proficiency is level-derived;
- non-enemy AttackMagic proficiency reads the four `CHAR_*_EXP` level fields;
- attack training progress uses `CHAR_*_ATTMAGIC_EXP`;
- defense resistance reads `CHAR_*_RESIST`;
- defense training progress uses `CHAR_*_DEFMAGIC_EXP`.

The currently admitted reconstructed **enemy caster** path only needs defender
resistance levels plus defense-training experience. Accordingly:

- `AttackMagicResistanceRuntime.levels` maps semantically to
  `CHAR_{ELEMENT}_RESIST`;
- `AttackMagicResistanceRuntime.exps` maps semantically to
  `CHAR_{ELEMENT}_DEFMAGIC_EXP`;
- equipment values in that runtime are battle modifiers, not replacements for
  the persisted sixteen-field core.

The four proficiency levels and four attack-training experience counters must
be added separately before a trainable player/pet AttackMagic caster is
admitted.

## Taiwan-v1 client schema boundary

`research/clients/STONEAGE-TW10-GAMEPLAY-SCHEMA-R1.json` establishes that
`status_player_full` and `status_pet_full` expose ordinary
`earth/water/fire/wind` attributes but no AttackMagic
proficiency/resistance/training fields.

`PlayerState.from_v1_character` intentionally copies that v1 status view,
while the reconstructed pet bridge builds `PetActor.state` from the v1 pet
view. The local-runtime save wrapper preserves this existing player/session
envelope. Inserting later-descendant server-only fields into those v1 views
would collapse two different provenance layers.

## R1 disposition

Closed facts:

- fixed descendants have a coherent sixteen-field AttackMagic server-state
  layout;
- generic player save/load persists the fields;
- embedded-pet save/load persists the fields;
- the current enemy AttackMagic overlay level/EXP pair is specifically the
  resistance + defense-training subset, not the proficiency + attack-training
  subset.

Still open:

- whether the preserved recovered25 server specimen used exactly the same
  compile-time save layout in the target build;
- whether an earlier Taiwan-v1 server had any analogous hidden fields;
- what versioned migration policy the modern single-player save should use if
  later recovered systems are intentionally imported.

Until a versioned persistence contract is explicitly adopted, battle-local
overlay carry-forward remains the fail-closed behavior.

Markers:

**DESCENDANT_ATTACKMAGIC_16FIELD_SAVE_LAYOUT_R1 = CLOSED**

**RECOVERED25_ATTACKMAGIC_LOCAL_SAVE_MAPPING_R1 = OPEN**
