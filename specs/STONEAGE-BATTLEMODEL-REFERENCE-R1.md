# StoneAge BattleModel reference R1

Status: **CLOSED_BOUNDED_RECOVERED25_CONDITIONAL_REFERENCE**
Date: 2026-10-05
Scope: next pressure-selected recovered25 enemy callback
`PETSKILL_BattleModel`.

## Accepted closure — 2026-10-06

Subsequent integration preparation directly audited the native no-ride
DamageSub marker branch. Reflect consumes its charge **without HP loss to
either participant**, while positive reported damage can still reach wakeup
and status. Raw-threshold ultimate flags can occur without HP loss. These
refinements and the invalid absent-ride read boundary are recorded in
`STONEAGE-BATTLEMODEL-SETTLEMENT-AUDIT-R1.md`. Its remote gate is pending;
runtime integration remains OPEN. The existing conditional reference facts
remain accepted, with these explicit settlement refinements.

This dated closure supersedes the pending statements in the historical sections
below; those sections remain as evidence of the discovery and correction path.

- Exact recovered25 data Action **37342593141 SUCCESS** and three-profile
  source/native Action **37342593073 SUCCESS** both accepted input
  `4131a23ce12b4d03e367456f4135988e8e5121b9`.
- Exact report write-back: `fb8cabc13a05c8e4188d18fbf774567a20c1f019`,
  tree `76e56d3a9334ab0db35bfbc5885fb5756fede514`.
- Supplemental helper Action **37344060042 SUCCESS** accepted input
  `be9de3df70d4a872817f55fd484e9a08f4dd1f31`: 432 controlled native
  helper cases per pinned profile, 1296 total. The core source gate separately
  covers 200 native target-plan cases per profile, 600 total.
- Full petskill SHA-256:
  `f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4`.
  Complete callback population is **638/641/649/650**. Only638 has positive
  recovered25 enemy references. Other rows remain data/reference-only.

ID638 has FIELD/TARGET/COST/ILLEGAL **1/3/3/10000**, 32 non-NUL OPTION
bytes, SHA-256
`690101963c1d05be1151cc54644e453c5a96c4e03eaf6b8dd6cbfd406d9a50a4`.
Derived fields: type5 (cover bit1 and physical bit4), object count4, status
turn1, hit input30, action numbers101867/101868. Callback count RNG is absent.
The status token is2 bytes, SHA-256
`fc84ea411bd02914ae6224a2d2d9d791c441d9e22aa8d98fcc3cf86ca873f428`;
field6 is6 bytes, SHA-256
`d45477b1b516ad1ec7b23ff1ca22bb433c16636acb4fde6404974ba311759a84`.

| TEMPNO | Graphic | Skill slot | ID | Vital/strength/toughness/dexterity | AI |
| --- | --- | --- | --- | --- | --- |
| 1178 | 101867 | 3 | 638 | 38/40/15/37 | 150 |
| 1179 | 101868 | 3 | 638 | 42/35/20/34 | 150 |

All three explicit Big5 source witnesses classify ID638 as **paralysis,
index2**. All three UTF-8 witnesses leave the actual recovered status token
**unknown**, so that conditional runtime applies no matched status. Under
Big5 field6 derives attack70% with integer/float32 truncation, preserving
defence/quick; witnesses100/80/60 ->70/80/60 and137/91/53 ->96/91/53.
UTF-8 literals do not match that recovered attack modifier and preserve powers.
Neither condition is selected as the original recovered build.

Runtime integration is authorized only for these exact positive identities,
with an explicit charset condition. It requires the dedicated hit loop and
state boundaries in `STONEAGE-BATTLEMODEL-RUNTIME-STATE-AUDIT-R1.md`.
Per-hit ordinary physical RNG, eligible status RNG and reached critical
non-player ultimate RNG remain separately owned; skipped targets own none.
Physical reflect consumes its charge while suppressing return damage.
ABSORB/VANISH suppress wakeup, while status eligibility separately reads
surviving HP and positive reported damage. The helper audit stubs common
arithmetic and does not recertify that arithmetic.

**OPEN:** original compiler/charset/source profile, numeric COM1, libc PRNG,
portable original qsort order, DODGE's uninitialised presentation field,
TRAP/ACUPUNCTURE and later transformations, complete runtime integration,
and JSS/Taiwan-v1 membership. Empty living-target lists fail closed in modern
execution. This acceptance changes no executable coverage: **2461/2486**.

**RECOVERED25_BATTLEMODEL_REFERENCE_R1 =
CLOSED_BOUNDED_RECOVERED25_CONDITIONAL_REFERENCE.**

## Starting provenance

This reference branch was created from exact accepted main
`d2b309c750049c1585543b4f76514cf8eca19826`, tree
`ff764e45470698514d728aa401e2ef17aba5c2ff`.

The hash-verified pet-skill pressure report selects:

- callback: `PETSKILL_BattleModel`
- referenced positive ID: **638**
- positive enemy skill-slot uses: **2**
- positive enemy templates: **2**
- status before this reference work: **open**

Those pressure counts are accepted. Complete callback population, exact row
metadata, OPTION identity and exact positive template identities are **not yet
accepted** until the dedicated recovered25 probe succeeds.

## Fixed-descendant callback facts already source-checked

Three pinned descendant profiles expose the same BattleModel callback structure:

- gavin `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
- iris `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
- bismarck `999ffdf1d220ec6666eb65339180689c9caf1876`

All three enable `_PETSKILL_BATTLE_MODEL` and register
`PETSKILL_BattleModel`.

The callback parses OPTION field 1 as attack type and field 2 as attack-object
count. A non-positive object count consumes `RAND(1,10)`; a count above 10 is
clamped to 10.

OPTION field 6 optionally rewrites attack/defence/quick work powers. The source
contains a material quirk which must not be normalized away: each matching
attack/defence/quick token first reads **CHAR_WORKATTACKPOWER** into the
calculation baseline, then writes the result to the corresponding
attack/defence/quick destination.

The callback writes C_OK, the symbolic
`BATTLE_COM_S_BATTLE_MODEL`, LOW(COM2)=type, HIGH(COM2)=object count and
COM3=the pet-skill array.

The descendant numeric command value is profile evidence only; it is not
accepted as original JSS/Taiwan-v1 identity under DD-019.

## Fixed-descendant dispatcher/effect facts

The battle dispatcher calls `BATTLE_BattleModel(battleindex,attackNo,myside)`
directly. Unlike ordinary ATTACK and BatFly's execution gate, this dispatcher
case does **not** call TargetAdjust.

The effect rereads OPTION through COM3:

- field 3: status token, matched against `aszStatus[]` using only the first
  two source bytes;
- field 4: status turn;
- field 5: status hit input;
- field 7: one to four client action/graphic numbers.

It rebuilds the living opposing side through `BATTLE_MultiList`, and reads
type/object count from packed COM2.

Target scheduling is source-shaped:

1. If object count is at least the current living-target count, each listed
   living target is attacked once in list order. Remaining attack objects each
   consume one `RAND(0, living_count-1)` and choose with replacement.
2. If object count is below living-target count, the first object-count targets
   are attacked once. If `type & 0x1` is true, attack objects cycle across the
   remaining targets until coverage is complete. Otherwise no coverage pass is
   added.
3. Action/graphic numbers cycle across attack objects.

The helper `BATTLE_BattleModel_ATTACK` rechecks each target, calls
`BATTLE_AttackSeq`, marks DamageSub with the BattleModel command identity and
then enters `BATTLE_DamageSub`. `type & 0x4` controls the explicitly physical
Guardian-redirection branch.

Positive damage runs DamageWakeUp before post-hit status application. Status is
only considered on a surviving target with positive damage, through
`BATTLE_StatusAttackCheck(..., effectHit, 30, 1.0, ...)`. Successful status
writes the configured turn. Paralysis/sleep/stone/barrier immediately clear the
target command for the remaining round.

A critical death of a non-player target can consume `RAND(1,100)` for the
ultimate/knockout branch. DamageSub contains BattleModel-specific suppression
paths for reaction mechanics such as reflection/trap/acupuncture; these are
part of the source boundary and must be audited before runtime closure.

## Charset/status boundary

The source compares only two bytes of the status token. The pinned source trees
are represented in modern repository encodings, while recovered25 pet-skill
OPTION data is byte-preserved and has already shown Big5-family material in
other callbacks. Therefore a modern Unicode string comparison is not an
accepted substitute.

R1 must keep these concepts separate:

- recovered OPTION byte identity;
- explicit decoding/profile if decoding is required;
- semantic status index;
- descendant source-token presentation.

No status mapping is accepted merely because a later public data table uses a
visually similar Chinese label.

## Unaccepted external hypothesis

Later public StoneAge-derived data contains a row labelled ID638 and suggests a
specific seven-field BattleModel OPTION plus metadata. This is useful only as a
cross-check hypothesis. It is **not** part of the accepted reconstruction until
the hash-verified recovered25 probe independently reproduces the same facts.

No raw later-table names/descriptions/OPTION payload are stored in this
reference contract.

## Required closure gates

Before this reference can close:

1. hash-verified recovered25 discovery must prove complete callback population;
2. ID638 exact FIELD/TARGET/COST/ILLEGAL and OPTION byte length/SHA-256 must be
   pinned;
3. all positive TEMPNO/graphic/base-stat/AI/slot placements must be pinned;
4. pinned descendant source audit must pass on all three exact commits;
5. recovered OPTION fields must be parsed only after their byte/profile identity
   is established;
6. RNG ownership must be enumerated separately for callback object-count
   randomization, excess-object target selection, physical attack resolution,
   status checking, critical ultimate and any admitted reaction branch;
7. runtime coding remains blocked until the reference and runtime-state audit
   are both closed.

**RECOVERED25_BATTLEMODEL_REFERENCE_R1 = OPEN_PENDING_EVIDENCE.**

## 2026-10-06 profile-classifier correction

Local acceptance reproduction found four test errors in the pending branch:
the assumed common status table included modern simplified literals that cannot
be encoded by strict Big5. The three pinned source tables are not identical:
gavin uses short simplified literals, iris short traditional literals, and
Bismarck longer status words. Their source index order is now an explicit gate
in every pinned source audit.

OPTION inspection retains separate source/charset witnesses for all three
profiles crossed with Big5/UTF-8. The legacy status summary is explicitly the
iris/Big5 witness; it does not identify the original recovered executable.
Unrepresentable source literals remain unsupported in that charset, without
transliteration or replacement bytes. Unknown tokens remain unknown. First
matching two-byte source prefix wins, including UTF-8 prefix collisions.

The unreferenced-population fixture now uses a valid OPTION. A separate
regression requires malformed OPTION to fail closed rather than silently
dropping the callback row. Local evidence: 24 tests PASS; all three pinned
source audits PASS, 200 native target-plan vectors per profile (600 total).
This local evidence does not replace hash-verified recovered25 remote
acceptance. Reference and runtime-state statuses remain pending.

## 2026-10-06 supplementary hit-helper audit

Native helper branch/call-order witnesses now cover432 cases per pinned
profile,1296 total. They refine the earlier positive-damage wake statement:
ABSORB/VANISH suppress wakeup, while a surviving positive reported-damage
status check is not independently suppressed by those reaction identities.
Nonphysical hits keep the original actual defender but can retain a Guardian
candidate in notification fields. DODGE can leave the source pet-damage
presentation value uninitialised; historical bytes for that field remain OPEN.

Contract: `specs/STONEAGE-BATTLEMODEL-HIT-LIFECYCLE-AUDIT-R1.md`. This
stubbed-helper audit does not certify common damage/status arithmetic or
replace the pending exact-data/source remote gates.
