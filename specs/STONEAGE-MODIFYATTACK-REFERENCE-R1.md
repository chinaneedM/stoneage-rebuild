# StoneAge PETSKILL_Modifyattack bounded reference R1

Status: **CLOSED_BOUNDED_RECOVERED25_REFERENCE**
Date: 2026-10-05
Scope: complete recovered25 callback population and its positive enemy uses;
fixed-descendant callback, dispatcher and post-AttackSeq helper reference.
Ordered battle runtime is not closed by this document.

## Evidence and identity

Fixed later descendants:

- gavinlinasd/StoneAge @ `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`;
- iriselia/StoneAge @ `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`;
- BismarckDD/stoneage @ `999ffdf1d220ec6666eb65339180689c9caf1876`.

All three activate `_PSKILL_MODIFY` and independently register
`PETSKILL_Modifyattack`. This is distinct from the already accepted
`PETSKILL_Mdfyattack` / `_PSKILL_MDFYATTACK` attribute-vector rewrite.
These are later-descendant sources and recovered25 bridge data, not evidence
of original JSS or Taiwan-v1 membership or an original executable profile.

The preserved petskill table SHA-256 is
`f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4`.
Complete population: **544 / 545 / 546 / 547**. Each row has
**FIELD 1 / TARGET 6 / COST 2 / ILLEGAL 2000**, five non-NUL ASCII OPTION
bytes, and a derived percent value **20**.
TARGET6 is `PETSKILL_TARGET_OTHERWITHOUTMYSELF` at the fixed profiles; it
must not be interpreted as the resolved battle-slot target.

| ID | Derived element | Positive slots | OPTION SHA-256 |
| --- | --- | ---: | --- |
| 544 | earth | 1 | `e79be7ef6b11e25c71965987e582b22aab53b623d828e8171bc27419cdec36dc` |
| 545 | water | 1 | `7e6949f73fcc809a89ca3d656e6c0fdb982a4785534d00d2f19f33f8b449a888` |
| 546 | fire | 1 | `b70d75132313c7f16aba7c6ccfdb6f59c86e7d7dacb05287555b3445aac18167` |
| 547 | wind | 0 | `f62fc526c64dc1092508e5c2d9b3dc21896889101abc7e8f62e59c562df5e203` |

| TEMPNO | Graphic | Skill slot | ID |
| ---: | ---: | ---: | ---: |
| 18 | 101543 | 4 | 546 |
| 19 | 101533 | 5 | 545 |
| 20 | 101532 | 4 | 544 |

There are exactly **three positive slots / three templates**. ID547 is
population/data evidence only; its inclusion does not add executable enemy
coverage. No original display text or raw table rows are stored.

## Callback and ordered source seam

The callback writes symbolic `BATTLE_COM_S_MODIFYATT`, copies toNo into COM2,
sets C_OK, and writes the skill-array identity into LOW(COM3), preserving the
upper packed half. It has no actor-type rejection, OPTION read, RNG draw,
or attack/defense power mutation. Its commented power reduction is inactive.

The dispatcher performs ordinary TargetAdjust first. Failure produces
NoAction. Success reads LOW(COM3) and calls the specialized single-hit
AttackDamage wrapper. It does not invoke a second strike or a counter.

Within that wrapper:

1. An active defender damage reaction demotes Modifyattack's event skill
   type before AttackSeq. The Modify helper and visual skill marker then do
   not execute. This does not rewrite the actor's historical COM1 into a
   native ordinary-attack command or grant ordinary-counter eligibility.
2. AttackSeq computes physical/elemental damage using its existing rules.
3. If the event skill remains Modifyattack and damage is positive, the
   Modify helper changes that damage before DamageSub.
4. DamageSub owns reactions, HP/riding settlement and subsequent death
   processing. The wrapper does not redirect to a returned Guardian index.
5. Positive final damage retains the skill-bearing event and
   `BCF_ATTDOUBLE`; nonpositive final damage demotes it. ATTDOUBLE is a
   protocol/visual flag in this path, not evidence of two attacks.

## Helper arithmetic and RNG ownership

The helper reads two delimiter fields into 256-byte buffers. It scans only
four exact codes (earth/water/fire/wind). An ALL entry exists in its table
but is outside the four-entry loop and therefore cannot match. Unknown,
case-changed or whitespace-altered codes do not match. A missing second
field returns without changing damage; an empty or nonnumeric numeric field
has atoi's zero value. Trailing fields are ignored in the bounded ASCII
reference.

The raw CHAR elemental attribute on the current defender is inspected, not
an attacker override vector. A matching attribute of zero produces no
change and owns no helper RNG. A positive matched attribute M owns exactly
one raw libc `rand()` draw R, with no extra success draw:

- base fraction is native float32 `atoi(percent) / 100`;
- random increment is **integer** `(R % (M + 5)) / 100`, then cast to float;
- damage compound addition uses float32 multiply/add and truncates the final
  sum into signed int.

For bounded attributes 1..95 every remainder is below 100, so the random
increment is zero even though the RNG draw is consumed. For 96..100 a
remainder of 100..104 (where attainable) contributes **1.0**, not 1%.
With the recovered 20% parameter, damage137 becomes164 at remainder99,
and301 at remainder100. The helper does not modify any actor attribute,
command or HP itself.

## Native acceptance and remaining work

The audit transiently compiles the actual callback, helper, packed macro
and delimiter functions. Collector stubs provide explicit work/stat values,
OPTION and a supplied raw rand result. These stubs are not a complete server
or the historical libc PRNG. Each profile compares 20 callback witnesses
and 2,660 helper cases, including all four verified actual OPTIONs, under
UBSan. Independent tests cover integer thresholds, no-RNG branches, parser
boundaries, complete population and row/graphic/slot identity drift.

First verified discovery: Action **37301723985 PASS**, input
`dbf59975781649a85a6746747001dbc02835988c`, report write-back
`15e32851e837460a4f9e0032d2fef0e38ee3d78c`. This first pass deliberately left
population/exact identity OPEN until the rows were pinned.

Final exact-data native gate: **37302178741 PASS**, input commit
`6abb4cc17b3426fce0eea39204d2b40f87ddec7e`, tree
`325629ab5f2d709037503dc62223aa7bc89487cc`; report write-back `a696cb5f98812600d7a1c898bf400ebe8dc21909`.
All population/row/template resolutions are CLOSED. **32 related unit tests
PASS**. Across three profiles: 60 callback and 7,980 helper comparisons;
all 12 profile-by-actual-OPTION combinations are included.

**MODIFYATTACK_REFERENCE_R1 = CLOSED_BOUNDED_RECOVERED25_REFERENCE.**

Numeric commands differ: **2029 gavin/iris**, **2027 Bismarck**;
Mdfyattack's neighboring values are2030/2028. All fixed profiles have
C_OK3 and ATTDOUBLE65536. Under DD-019 none establishes the recovered
original numeric COM1. Null OPTION is outside this reference: gavin/iris
check NULL, whereas Bismarck compares to a string-literal pointer.

OPEN: original executable/compiler/profile, original numeric COM1 and libc
PRNG identity, JSS/Taiwan-v1 membership, ordered/persistent/coordinator
admission and complete AttackSeq/target/reaction/Guardian composition.
Undefined signed overflow or float-to-int conversion is refused by the
reference. No property/profession or later extension composition is newly
claimed. Positive executable pressure remains **2454/2486 = 98.71%**.

Next: accept this reference on main; create a fresh Modifyattack runtime
branch; bind exact positive identities, retain semantic command ownership,
and verify helper RNG between AttackSeq and DamageSub before pressure closure.
Continue WORK under DD-018; production engine/redesigned content is deferred.
