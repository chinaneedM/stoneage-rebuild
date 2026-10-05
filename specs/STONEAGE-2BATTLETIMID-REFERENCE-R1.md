# StoneAge PETSKILL_2BattleTimid conditional reference R1

Status: **CLOSED_BOUNDED_RECOVERED25_REFERENCE**
Date: 2026-10-05
Scope: complete recovered25 callback population, exact positive placements,
fixed-descendant callback/dispatcher/post-damage pet recall, and explicit
execution-character-set profiles. Ordered battle runtime remains OPEN.

## Evidence and exact identity

Fixed later descendants:

- gavinlinasd/StoneAge @ `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`;
- iriselia/StoneAge @ `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`;
- BismarckDD/stoneage @ `999ffdf1d220ec6666eb65339180689c9caf1876`.

All three activate `_PETSKILL_2TIMID` and register `PETSKILL_2BattleTimid`.
These are later-descendant sources and preserved recovered25 bridge data;
they do not establish original JSS/Taiwan-v1 membership or build identity.

Verified complete petskill SHA-256:
`f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4`.
The complete callback family contains only **ID636**. Exact row identity is
**FIELD1 / TARGET7 / COST2 / ILLEGAL10000**, with 17 non-NUL, non-ASCII OPTION
bytes and digest
`8e6b5dd952bf3bc81e522f1df382db48473b1aeec13f9ff08c7bb76d2c06f9e5`.
CP950 and Big5 decoding agree, but decoded text alone cannot select the
execution charset. TARGET7 is `PETSKILL_TARGET_WITHOUTMYSELFANDPET`, not
TARGET1 or TARGET6 and not a resolved battle slot.

| TEMPNO | Graphic | Skill slot | ID |
| ---: | ---: | ---: | ---: |
| 178 | 101872 | 3 | 636 |
| 179 | 101873 | 3 | 636 |

Exactly two positive uses / two templates are pinned independently from
population and metadata. Neither raw OPTION nor original source is stored.

## Callback arithmetic and byte profiles

The actor validity check precedes symbolic `BATTLE_COM_S_2TIMID`, target COM2
and C_OK writes. The callback does not reject a player actor. In the accepted
nonnull domain it examines six independent markers, in this order: attack
minus, attack plus, defence minus, defence plus, quick minus, quick plus.
Each matched marker parses a float at the historical fixed **+4 byte**
offset. Parsing must use raw OPTION bytes and the explicitly selected literal
encoding; no implicit transcoding or offset repair is permitted.

A minus marker keeps fixed-stat times the parsed fraction; it does not
subtract that fraction from the stat. A plus marker overwrites with
fixed-stat plus fixed-stat times the fraction, rather than using an earlier
work-power result. Each match divides the shared float by100. A failed scan
retains the already scaled float from an earlier match. Missing markers
preserve incoming work powers. Arithmetic uses native float32 operations
and signed-int truncation. LOW(COM3) receives the skill-array index while
the high packed half is retained. Callback-local RNG is absent.

The post-damage chance parser uses a separate integer initially zero and
the historical **+3 byte** offset. It does not clamp the parsed chance.

Actual verified ID636 parameter outcomes are conditional:

| Literal profile | Attack | Defence | Quick | Chance |
| --- | --- | --- | --- | ---: |
| `utf8_literals` | preserve incoming | preserve incoming | preserve incoming | 0 |
| `big5_literals` | fixed STR * 0.50 | preserve incoming | fixed DEX + fixed DEX * 0.30 | 60 |

For fixed stats1000 and incoming powers900/800/700 the native witnesses
produce **900/800/700/0** versus **500/800/1300/60**. The UTF-8 outcome
does not remove the later positive-damage RNG draw. Synthetic UTF-8 markers
that do match still retain the original byte offsets, including failed
numeric scans; this reference does not normalize their historical parser.

## Ordered source and pet recall

The dispatcher performs ordinary TargetAdjust before specialized AttackDamage
with the packed skill identity. Original-defender damage reactions demote
the event skill before AttackSeq. Nonpositive damage demotes before the
post-damage switch. Those demoted paths own no 2Timid post draw.

For a remaining positive-damage 2Timid event, one `rand()%100` draw occurs
before both the damage>1 and pet-type checks. Damage1 and a nonpet defender
still consume this draw. Chance success plus damage>1 plus a pet target
requests recall; it does not cause player battle exit or party discharge.
The old NoAction/direct PetDefaultExit/BE code in this branch is commented
out and is not executable evidence.

The active call is `BATTLE_PetIn(battleindex, defNo-5)`. In the bounded
normal-pet domain, pet slots5..9 and15..19 align with owner slots0..4 and
10..14. The owner must exist, its selected default-pet identity must refer
to that defender, and no wolf/fox transformation composition is admitted.
Despite its name, this helper withdraws the selected pet:

- If NORETURN is clear, it invokes PetDefaultExit, sets owner DEFAULTPET
  to-1, and emits one BS frame. It does not emit the old BE exit frame.
- If NORETURN is set, it skips that withdrawal/default mutation/BS frame.
- In both cases the outer event sends K status for the prior default pet
  before the helper, then KS for the current default pet after it. Thus a
  blocked recall still has both notifications. The helper returns0 in both
  cases, and the caller does not use that return to distinguish success.

Wolf/fox preparation occurs before NORETURN in the source helper. Those
compositions remain OPEN; gavin/iris and Bismarck also differ in the fox-round
getter. The normal-pet oracle compiles the actual helper with both feature
macros active, using inert image/fox-round states. Its stubs verify default
pet, owner mapping, notifications and frames; they do not execute the full
server PetDefaultExit lifecycle. The modern runtime must audit and model
that lifecycle before removing battle occupancy or changing persistence.

Unlike BattleTimid, 2Timid is absent from the legacy same-side `_SKILLLIMIT`
list. Do not inherit BattleTimid's actor rejection, fixed70/40/80 powers,
fixed15% chance, same-side branch or player-exit effects. An ATTACK-shaped
modern scheduling carrier cannot grant ordinary-counter eligibility.

## Acceptance and handoff

Discovery Action **37308193431 PASS** established the complete population
and placements; its deliberately unpinned identity remained OPEN. Final
exact-data/native Action **37309960471 PASS** uses input
`bf02c6a38cbd1ea221aeee412e445e736f57d66f`, tree
`d4b59ba09918024026a4fde1819c1fef1da157c7`.
Derived report commit: `7255dc2e551ba800f6d892c0a44dda3d04dcb4c8`, tree
`1a8412d1927af5bc9699a02b1bd07fa9be148c50`.

Each of three fixed profiles passes19 source gates. Each of two explicit
charsets per profile compares **88 callback / 8,866 post-recall** witnesses,
including the single actual OPTION at every profile/charset combination:
**528 callback / 53,196 post-recall** comparisons total. The extracted
callback, event case and PetIn body are compiled transiently; reaction and
nonpositive-damage wrapper demotion are textual source gates and controlled
oracle inputs, not a native execution of the complete AttackDamage wrapper.
The first native workflow37309552625 failed on raw preprocessor braces;
the corrected extractor bounds both affected function windows and the
subsequent complete gate above passes. **32 related unit tests PASS**
(13 new reference/probe, plus neighboring BattleTimid and pressure tests).

Reports: `research/recovered/STONEAGE-2BATTLETIMID-SOURCE-AUDIT-R1.txt`
and `research/recovered/STONEAGE-25-2BATTLETIMID-PROBE-R1.txt`.
Reproducers: `tools/stoneage_2battletimid_source_audit.py`,
`tools/stoneage_2battletimid_reference_model.py` and
`tools/stoneage_recovered25_2battletimid_probe.py`.

**TWOBATTLETIMID_REFERENCE_R1 = CLOSED_BOUNDED_RECOVERED25_REFERENCE.**
The three descendants compile command2005 and C_OK3, but DD-019 keeps the
recovered-original numeric COM1, compiler/execution charset and libc PRNG
OPEN. gavin/iris guard NULL while Bismarck compares a string-literal pointer;
null-pointer behavior is outside the accepted raw nonnull domain. Exotic
numeric tokens, nonfinite values, overflow, locale-dependent arithmetic,
transformations and invalid owner/default-pet mappings are not closed.

Executable pressure remains **2457/2486 =98.83%**, with zero unresolved
positive skill IDs at the last accepted pressure gate. This reference adds
no executable positive slot. Ordered/persistent/coordinator runtime is OPEN.

Next: merge the accepted reference into freshly verified main, then start a
fresh 2BattleTimid runtime branch. First audit owner/default-pet/NORETURN and
PetDefaultExit state/occupancy/persistence seams, and attempt one bounded
preserved-executable charset discriminator. If it cannot select an original
build, retain explicit profiles. Bind exact two positive identities and
preserve callback powers, RNG order, reaction demotion and blocked-recall
notifications before ordered, cross-round, coordinator and pressure gates.
Continue WORK under DD-018; engine selection and redesigned content remain
deferred.
