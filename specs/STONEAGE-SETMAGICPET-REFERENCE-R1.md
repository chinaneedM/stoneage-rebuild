# StoneAge SetMagicPet bounded reference R1

## Evidence role

This is a later-descendant source reference plus recovered25 data probe. It is
not an original JSS/Taiwan-v1 source claim and it does not yet authorize an
ordered executable runtime.

Pinned descendants:

- gavinlinasd/StoneAge @ 1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56
- iriselia/StoneAge @ 9e6c8ce2cd8ed532a7157773acd1c61582c178b5
- BismarckDD/Stoneage @ 999ffdf1d220ec6666eb65339180689c9caf1876

## Fixed source facts

The callback writes symbolic SETMAGICPET command, COM2 target, C_OK mode and
LOW(COM3) skill-array identity.  It reads CHAR_MAGICPETMP and rejects values
>=3, but writes the same value back without incrementing it. Across the pinned
trees the work value is reset to zero at battle initialization and no increment
site has been established. Therefore the source text's user-facing 'three uses
per battle' message is not treated as an effective counter mechanism.

The executor reads exactly three pipe-delimited OPTION fields: turn, numeric
amount and a type marker. HP is checked first; the non-HP branch constructs a
MultiList and admits STR, TGH or DEX. A target already carrying SetDuck or any
of the three magic-pet turn counters is skipped.

STR/TGH/DEX storage is temporary battle work state. BATTLE_StatusSeq decrements
positive turn counters. Attribute recalculation later applies the stored power.
All three branches use the same saved `mtgh` value (pre-suit fixed toughness)
as the percentage basis, including STR and DEX. R1 preserves this source quirk
instead of replacing it with per-stat percentage arithmetic.

The source petskill symbol is 601 in all three pinned descendants. That numeric
agreement is corroborating later-source evidence only; it does not independently
prove original binary build identity or earliest historical membership.

## Safety boundaries

R1 requires a non-NULL, non-NUL OPTION with three fields. Gavin/iris have an
explicit NULL guard; the pinned Bismarck descendant compares the pointer to the
string literal "\0", so NULL behavior is not admitted.

Unknown third-field markers are not executable runtime candidates even though
the source function can return TRUE after emitting a kind-zero display record.
Multiple simultaneous STR/TGH/DEX counters are outside the bounded arithmetic
model because the executor itself prevents that overlap.

Target-list construction, HP MultiRecovery settlement, interaction with
Weaken/Barrier/Nocast and ordered persistent runtime remain OPEN until the
verified recovered row and target metadata are known.

## Current gate

Fixed-source reference can close independently. Recovered25 full callback
population, exact metadata/OPTION hashes and ordered runtime remain separate
acceptance gates.
