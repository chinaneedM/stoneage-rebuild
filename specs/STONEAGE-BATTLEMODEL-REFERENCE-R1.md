# StoneAge BattleModel reference R1

Status: **PENDING_RECOVERED25_DATA_AND_PINNED_SOURCE_ACCEPTANCE**
Date: 2026-10-05
Scope: next pressure-selected recovered25 enemy callback
`PETSKILL_BattleModel`.

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
