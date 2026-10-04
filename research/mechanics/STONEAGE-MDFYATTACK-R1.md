# Mdfyattack fixed-source reference — R1

Evidence date: 2026-10-04. This is a version-tagged later-descendant reference,
not a Taiwan-v1 membership claim or recovered25 binary command mapping.

## Identity and evidence

**FACT:** `PETSKILL_Mdfyattack` and `PETSKILL_Modifyattack` are separately
registered callbacks. Verified callback pressure selects the former, recovered
IDs 548/549/550/551, with 8 positive enemybase slot uses across 8 templates.
Modifyattack IDs 544/545/546 remain a separate open family.

The reproducible audit pins:

| Profile | Repository commit | Source root | Mdfyattack COM1 | Modifyattack COM1 |
| --- | --- | --- | --- | --- |
| gavin | `gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56` | `gmsv/src` | 2030 | 2029 |
| iris | `iriselia/StoneAge@9e6c8ce2cd8ed532a7157773acd1c61582c178b5` | `Source/gmsv` | 2030 | 2029 |
| Bismarck | `BismarckDD/stoneage@999ffdf1d220ec6666eb65339180689c9caf1876` | `server/gmsv` | 2028 | 2027 |

**FACT:** actual header/preprocessor checks enable `_PSKILL_MDFYATTACK` in
all three profiles. Their differing enum values cannot identify recovered25
COM1. No source pet-skill numeric macro is assigned to this callback here.

Tools: `tools/stoneage_mdfyattack_source_audit.py`,
`tools/stoneage_mdfyattack_model.py`,
`tools/stoneage_recovered25_mdfyattack_probe.py`.
Derived report: `research/recovered/STONEAGE-MDFYATTACK-SOURCE-AUDIT-R1.txt`.

## Callback and OPTION

**FACT:** before fetching OPTION, the callback writes symbolic COM1, submitted
COM2, C_OK mode and skill-array LOW(COM3). It does not reject PLAYER actors and
does not modify attack/defense work powers. An invalid OPTION can therefore
leave partial native work writes; the safe reference's refusal is not a claim
of native atomic rollback.

The first pipe-delimited field must exactly equal one of EA, WA, FI, WI,
mapped to indices 0, 1, 2, 3 (earth, water, fire, wind). No case folding or
whitespace trim applies to that field. The code writes its index to LOW(COM4),
then requests the second field and writes C-atoi's result to HIGH(COM4).
Subsequent fields are ignored. Each native destination buffer holds 256 bytes,
so at most 255 payload bytes affect the copied token. A present empty/nonnumeric
second field yields zero; a missing second field fails.

**PROFILE LIMIT:** gavin/iris test a NULL OPTION pointer. Bismarck compares the
pointer with an empty string literal, which is not a NULL guard. The reference
requires non-null, NUL-free ASCII bytes. Bismarck uses GeneralSplitImpl and
workspace copy helpers; gavin/iris use the older two-byte-aware delimiter
helper. Their admitted ASCII cases converge, but non-ASCII scanning is not
claimed equivalent.

**SAFE DOMAIN:** amount 0..32767 preserves defined nonnegative signed-C
left-shift packing. Negative values, larger amounts and overflowing arithmetic
remain outside admission, rather than receiving guessed wraparound semantics.

## Attribute stage

**FACT:** the override is controlled by the attacker's current symbolic COM1,
not by the local AttackSeq opt or the event wrapper's possibly cancelled skill
type. After GetAttr, AttrAdjust clears all five attack weights, writes the
selected amount, and explicitly sets the neutral fifth weight to zero.

This is a replacement, not an addition to the character's original attributes.
For EA amount 60 the vector is `(60, 0, 0, 0, 0)`, not a vector with neutral 40.
At pre-attribute damage 100 against a neutral defender, the specialized result
is 90; ordinary four-element normalization would incorrectly produce 130.
Amount zero produces zero attribute-stage damage. Values above 100 are not
automatically clamped in the audited override.

**FACT:** replacement precedes attacker/defender property hooks, field scalars,
damage-weight multiplication, AttrCalc and field-ratio multiplication. The
field scalars and division/product use C float rounding; integer assignments
truncate toward zero. The reference preserves those binary32 boundaries and
checks intermediate signed-C overflow.

All pinned profiles enable property and suit features. **REFERENCE LIMIT:**
the numerical reference isolates the no-property-hook/no-suit-bonus domain;
it does not execute arbitrary descendant hooks or later profession effects.
Defender base element weights and field power are explicitly constrained to
0..100. This is an attribute-stage function, not a full AttackSeq/critical/
guard/ride/reaction execution model.

## Specialized dispatch and event boundary

**FACT:** dispatch uses ordinary TargetAdjust and then one specialized
AttackDamage call with LOW(COM3). It retains the symbolic Mdfyattack command;
it does not enter the ordinary multihit/counter branch.

The wrapper checks the defender's damageReact before AttackSeq and can cancel
its local skill type. That does not clear the attacker's COM1 or erase the
attribute override. DamageSub and wake-up/death handling follow AttackSeq.
Positive final damage without cancelled skill type emits BCF_MODIFY (the
compiled flag is 2097152) and a skill-array witness. Non-positive damage cancels
the special event mark; Modifyattack's post-damage transform is not applied.

**FACT / QUIRK:** AttackSeq receives a Guardian output pointer, but this
specialized wrapper does not reassign the defender to that Guardian. Runtime
integration must inspect and preserve this boundary rather than inheriting
ordinary Attack's full Guardian settlement by convenience.

## Verification and current gate

Local 78 tests pass, including 17 new parser/attribute/data-probe tests and
existing battle-core/pressure regressions. The source audit compiles actual
callback, delimiter and attribute functions transiently with undefined-
behavior sanitization: 15 callback cases and 1025 attribute cases per profile,
45 callback + 3075 attribute witnesses in total, all matching.

**MDFYATTACK_FIXED_SOURCE_R1 = LOCAL_PASS_SAFE_REFERENCE_REMOTE_PENDING.**
**RECOVERED25_MDFYATTACK_POPULATION_R1 = OPEN_PENDING_VERIFIED_BUNDLE_PROBE.**
**RECOVERED25_MDFYATTACK_OPTION_DOMAIN_R1 = OPEN_PENDING_VERIFIED_BUNDLE_PROBE.**
**RECOVERED25_MDFYATTACK_RUNTIME_R1 = OPEN.**

Next: close exact four-row metadata/OPTION from the hash-verified bundle probe,
then implement typed AI -> ordered specialized physical action -> persistent
coordinator acceptance within an explicitly supported actor/weapon/extension
domain. These 8 uses do not increase executable coverage before runtime E2E
acceptance; do not advance to another callback yet.
