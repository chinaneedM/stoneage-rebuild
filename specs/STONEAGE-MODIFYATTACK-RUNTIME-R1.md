# StoneAge Modifyattack ordered runtime R1

Status: **IMPLEMENTED_PENDING_REMOTE_ACCEPTANCE**
Date: 2026-10-05
Scope: recovered25 positive enemy uses of `PETSKILL_Modifyattack`.

## Evidence and admission

The accepted reference is `STONEAGE-MODIFYATTACK-REFERENCE-R1.md`.
Complete population 544/545/546/547 is checked against exact FIELD1/TARGET6/
COST2/ILLEGAL2000 and five-byte non-NUL OPTION hashes, including unselected
ID547. Only these positive placements can construct a typed submission:

| TEMPNO | Graphic | Source slot (one-based) | ID | Element |
| --- | --- | --- | --- | --- |
| 18 | 101543 | 4 | 546 | fire |
| 19 | 101533 | 5 | 545 | water |
| 20 | 101532 | 4 | 544 | earth |

ID547 wind remains population/data-only. `PETSKILL_Mdfyattack` is a distinct
callback and retains its separate attribute-vector semantics.

The typed identity binds participant, template, graphic, selected authoritative
seven-slot placement, skill ID, player-side source target and symbolic
`BATTLE_COM_S_MODIFYATT`. ATTACK is solely a modern scheduling carrier. It
does not supply historical numeric COM1 or ordinary counter/combo eligibility.
This runtime admits enemy FIST actors; unsupported weapons and nondefault
callback work-power setup fail closed.

## Ordered damage and RNG

Ordinary live TargetAdjust precedes the single specialized attack. Sleep and
other action suppression cannot execute the helper; confusion rewrites to the
ordinary command and removes the semantic effect. Dodge and no target cannot
execute it. Active original-defender reaction demotes the effect before
AttackSeq, keeping ordinary damage/reaction handling without the helper or
ATTDOUBLE marker.

AttackSeq retains ordinary physical, attribute/field, critical, guard and
minimum-damage arithmetic. Only its positive damage enters Modify helper,
before DamageSub. The helper observes the adjusted original defender's raw
four-element attributes. A Guardian can calculate the ordinary damage, but
the specialized wrapper keeps both the helper's attribute lookup and HP
settlement on the original target.

A positive selected attribute owns exactly one explicit raw libc `rand()`
result. Zero selected attribute owns none. Every submitted actor must have a
matching RNG-map entry: raw nonnegative signed-int for an executed matching
helper, explicit `None` otherwise. Missing, extra, invalid and unowned RNG
inputs fail closed. No PRNG stream is fabricated.

The shared native-accepted reference helper preserves float32 base20% and
integer `(raw_rand % (matched_attribute + 5)) / 100` before the cast. Attributes
1..95 still consume the draw even though the random increment is zero;
attributes96..100 can add a whole1.0. Final float32 addition/multiplication
then signed-int truncation are unchanged. ATTDOUBLE is an event marker,
never a second hit. Positive zero-match damage still retains the marker.

## Persistence and acceptance boundary

Semantic submissions and helper draws belong to the current action. They do
not persist command numbers, skill slots, element overrides or work powers.
Cross-round tests prove the next ordinary hit uses the pre-helper damage and
keeps base attack/defense. Persistent combo preparation excludes the semantic
actor both as starter and partner. Counter exclusion is maintained before and
after its own action, including dodge and reaction demotion.

Exact identity, all four population rows, the three executable IDs, RNG
ownership, M95/96/100 boundaries, retarget, Guardian, status, reactions,
counter, combo, cross-round lifetime and coordinator dispatch have local
witnesses. Remote runtime/core/coordinator/golden/full-region gates and the
hash-verified pressure report must pass before accepted coverage advances.
Until then accepted coverage remains **2454/2486 = 98.71%**.

Original COM1 (2029 versus2027 in descendants), compiler/libc/PRNG profile,
null-pointer divergence and original JSS/Taiwan-v1 membership remain OPEN.
This bounded recovered25 enemy-use result does not establish whole-game
completion or an original executable profile.
