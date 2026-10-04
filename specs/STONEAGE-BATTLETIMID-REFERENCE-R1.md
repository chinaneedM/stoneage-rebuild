# StoneAge BattleTimid bounded reference R1

## Evidence role

This is a later-descendant source reference plus a hash-verified recovered25
data probe. It is not an original JSS/Taiwan-v1 source claim and it does not
authorize an ordered executable runtime by itself.

Pinned descendants:

- gavinlinasd/StoneAge @ 1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56
- iriselia/StoneAge @ 9e6c8ce2cd8ed532a7157773acd1c61582c178b5
- BismarckDD/stoneage @ 999ffdf1d220ec6666eb65339180689c9caf1876

## Fixed descendant source facts

All three pinned profiles compile `_PETSKILL_TIMID` and register
`PETSKILL_BattleTimid`. The callback rejects player actors, writes the TIMID
battle command, COM2 target and C_OK mode, packs the skill-array identity into
LOW(COM3), and derives temporary work powers as fixed STR * 0.7, fixed TOUGH *
0.4 and fixed DEX * 0.8.

The compiled descendant command value is 2004 and C_OK mode value is 3 in all
three pinned profiles. Those numeric agreements are corroborating descendant
facts only; they do not prove original binary/compiler identity.

The battle dispatcher performs target adjustment, recovers the skill identity
from LOW(COM3), and enters `BATTLE_S_AttackDamage`. In the TIMID post-damage
branch, one raw `rand()%100` draw is consumed before the condition is tested.
Forced exit occurs only when the reduced draw is below 15 and final damage is
greater than 1.

On forced exit, a pet target is removed through the default-pet exit path and
the owner's `CHAR_DEFAULTPET` is set to -1. A non-pet target takes
`BATTLE_Exit` and party discharge. The hit record is emitted before the exit
gate.

## Compile-profile differences retained

Gavin and iris compile the `_SKILLLIMIT` same-side rejection path. The pinned
Bismarck profile does not compile that gate. R1 therefore admits only
opposite-side targeting as the common executable reference domain.

Gavin and iris guard the OPTION pointer with `pszP == NULL`. The pinned
Bismarck descendant instead compares the pointer with the string literal
`"\\0"`. This is not normalized into equivalent NULL safety.

## Recovered25 data facts

The hash-verified recovered25 `petskill` source has SHA-256
`f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4`.

The full `PETSKILL_BattleTimid` population is exactly one row:

- ID 606
- FIELD 1
- TARGET 6
- COST 2
- ILLEGAL 3000
- OPTION byte length 0
- OPTION SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- OPTION contains no NUL byte
- positive enemybase references: 5 slots across 5 templates

The empty OPTION is a data fact, not permission to model an absent/NULL OPTION
pointer. Any runtime bridge must preserve a present empty field when it reaches
the descendant-style damage path; it may not reinterpret the zero-byte field as
proof that NULL is accepted.

## Safety boundaries

R1 does not generalize same-side targeting, libc `rand()` state or sequence,
original numeric command identity, original compiler behavior, original
JSS/Taiwan-v1 membership, or the Bismarck pointer-literal guard.

The reference model accepts an externally supplied reduced `rand()%100` draw;
it does not claim Python RNG equivalence to the original C runtime.

## Current gate

**BATTLETIMID_FIXED_SOURCE_R1 = CLOSED_OPPOSITE_SIDE_REFERENCE.**

Recovered25 population and exact row are accepted only after the second
hash-verified probe reproduces the pinned row. Ordered runtime integration,
damage settlement coupling, persistent battle/session consequences, and
pressure reclassification remain OPEN until dedicated runtime gates pass.
