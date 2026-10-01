# StoneAge recovered25 AttackMagic runtime admission R1

Date: 2026-10-01

## Closed prerequisites

The runtime index is built only after four independent closures:

- recovered25 skill/magic/item/IDX cross-link;
- fixed-descendant AttackMagic damage core;
- fixed-descendant 3x5 footprint geometry;
- recovered25 real-matrix footprint coverage.

Coverage run **36847455747 = PASS** measured 250 fully alive enemy-to-player
scenarios: **110 source-sort portable** and **140 nonportable**. The split is
exactly the recovered single-target versus multi-target split for that state.
The implementation nevertheless evaluates portability dynamically, because a
multi-target magic can become exact when current living-target membership
collapses to a strict-order set.

## Non-player item token

The recovered options contain configuration item IDs 19647..19671 and those
rows cross-link 25/25 to magic IDs 301..325 with magicusemp=5. The old
gavin/iris handler writes that token into HIGH(COM3); Bismarck does not.

A deeper source trace shows that these numbers must not be reinterpreted as
authoritative dynamic item-instance indexes:

1. existing-item instances are allocated through a rotating free-slot Sindex;
2. non-player DirectUse passes HIGH(COM3) to ITEM_getInt as an existing-item index;
3. invalid lookup yields negative MP but does not abort DirectUse;
4. MAGIC_AttMagic skips MP check/deduction for non-player casters;
5. MAGIC_AttMagic_Battle never uses mp.

Therefore the reconstructed non-player runtime retains item IDs for provenance
and structural cross-link validation only. It does not fabricate a matching
existing-item instance.

Marker: **RECOVERED25_ATTACKMAGIC_NONPLAYER_ITEM_TOKEN = CONFIG_CROSSLINK_ONLY_MP_EXECUTION_DEAD**

## Runtime index

`tools/stoneage_recovered25_attack_magic_runtime.py` loads and verifies:

- exactly 25 recovered PETSKILL_AttackMagic rows;
- exact magic population 301..325;
- MAGIC_AttMagic callback identity and valid IDX for every row;
- strict CP950/Big5-equal element/power/level grammar;
- paired active item configuration and matching magicid;
- item magicusemp;
- both adjacent attmagic side matrices for every IDX.

For the current local runtime orientation, player slots are 0..9 and enemy
slots 10..19. Enemy AttackMagic therefore uses the even IDX*2 side record.
The runtime first applies the fixed magic-ID selector rewrite, then historical
dead-target/row fallback, then 3x5 footprint expansion. It exposes membership
even when ordering is nonportable, but exact execution raises unless SortLoc
defines a strict ordering for the concrete living target set.

## Admission policy

No magic ID is globally admitted or rejected solely by its normal full-side
shape. Admission is state-dependent:

- exact source order available -> eligible for damage-core composition;
- target membership known but SortLoc/qsort nonportable -> fail closed;
- no valid target -> no fabricated target.

This preserves historical evidence while allowing a multi-target spell to
become exact when only one applicable target remains.

Validation: fixed preservation-bundle workflow **36850584056 = PASS**. The
runtime smoke closed all 25 entries, reproduced the 110/140 full-side
portable/nonportable split, retained item tokens as execution-dead non-player
MP provenance, and proved dynamic portability with magic 305 at one living
player target. Report write-back advanced `main` to
`99a6fa36b9c916696b3791618866377b17baa998`.

Marker: **RECOVERED25_ATTACKMAGIC_RUNTIME_INDEX_R1 = CLOSED**
