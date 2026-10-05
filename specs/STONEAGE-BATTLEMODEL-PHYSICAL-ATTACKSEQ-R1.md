# BattleModel equipment-free physical AttackSeq adapter R1

Date: 2026-10-06 (UTC+8)
Status: **CLOSED_BOUNDED_EQUIPMENT_FREE_PHYSICAL_ATTACKSEQ_FULL_RUNTIME_OPEN**

## Explicit composition and identity

`execute_battlemodel_physical_loop` connects the accepted shared physical
primitives to the accepted ordered post-AttackSeq loop. No controlled hit
result is injected by this adapter. The exact typed ID638 submission still
binds participant/template/positive slot/OPTION/profile/current work powers.
Attack comes from post-callback `submission.setup.powers[0]`; actor defense
and quick must match the other two work powers. Physical profiles exactly
cover mapped entry identities and are copied into immutable mappings.

Required context `PHYSICAL_SCOPE_R1` declares equipment-free, no bow, no
later features, neutral global dodge/damage modifiers. The caller separately
must select `HIT_LOOP_SCOPE_R1`: reduced offset10/no ride/nonthrowing/
no ItemCrush/gDamageDiv0. These are experimental exclusions, not historical
build selection or proof that an actual recovered battle had no equipment.
Newpower70% and preserved-old mixed defense are explicit separate profiles;
old defense requires fixed vital. Four elements and field state are explicit.
Only neutral/guard defender commands are supported; JYUJYUTU/NOGUARD and later
modifiers are rejected or excluded rather than guessed from numeric COM1.

## Source order and mutable hit state

1. Original target Duck gates: GUARD (including confused GUARD), active damage
   reaction, cannot-move status, NODUCK and ABIO suppress the entire Duck RNG.
   Player defender luck only. Drunk attacker consumes owned20..30 before
   owned1..10000 Duck; comparison is inclusive.
2. Guardian eligibility follows original-target Duck, consumes no RNG and
   reads current HP/status. All shared sleep/confusion/paralysis/stone/barrier/
   flag/self gates apply. Only bounded opposing-side mapped Guardians are
   supported; inherited loop target validity is an explicit additional bound.
3. Critical uses actual defender fixed DEX/type, enemy luck0 and equipment
   critical0. Owned1..10000 comparison is strict. Damage uses actual defender
   profile/status, declared defense variant, piecewise owned draw, elements/
   field and non-bow critical additive term.
4. Actual defender GUARD adjustment consumes owned1..100 only if confusion
   is inactive and its command has not been cleared. Damage below1 consumes
   owned0..1. Zero becomes MISS, Guardian forces NORMAL/damage1, otherwise
   active GUARD becomes ALLGUARD. Global damage multiplier is explicitly1.
5. Existing marker settlement/wakeup/status/command-clear/critical-death and
   lazy target selection continue on the same chronological tape. Later hits
   see paralysis, cleared guard commands, exhausted reactions and dead targets.

The new `attackseq_drunk_dodge` owner cannot consume status/selection/death
draws. Missing, extra, invalid-range or misordered draws remain fail-closed.
No ordinary round, persistent state, coordinator or pressure route is enabled.

## Validation

- 157 local shared/loop/admission/core/Guardian tests pass, including17 new
  physical adapter tests. They exercise real HP deltas, conditional Big5 work
  power, reflection, status-cleared guard, original Duck versus actual Guardian,
  actual Guardian paralysis, strict/inclusive boundaries, source luck rules,
  drunk order, defense variants/stone, field/element arithmetic, minimum/guard/
  Guardian outcome classification and real pet critical-death RNG ordering.
- Native audit compiles11 original functions transiently at each clean fixed
  gavin/iris/bismarck pin: Duck, Guardian, CriticalPlayer/Critical, Damage,
  CriDamage, FieldAttAdjust/AttrCalc/AttrAdjust, GuardAdjust and AttackSeq.
  116 independent controlled cases per defense variant,232/profile,696 total
  compare outcome, damage, Guardian and every RNG range/value/order.
  Getters, CanMove, reaction selection and no-ride/equipment are controlled
  stubs. This is sampled bounded agreement, not exhaustive float32 equivalence.
  Bismarck AttrCalc is read from the same pin's `battle/battle_magic.c`; its
  separate SHA256 is emitted. Original source is never committed.
- Extended settlement CI runs these tests/audit plus the previously accepted
  1920 settlement calls,480 physical marker comparisons and60 pet-guard calls.
  Exact publication input/run is recorded in the derived acceptance receipt.

## ItemCrush remains required even without equipment

**FACT (pinned descendant source):** the helper calls ItemCrush on a surviving
actual defender before status. In gavin's legacy variant, player ItemCrushCheck
draws `RAND(1,gItemCrushRate)` before equipment lookup. With `_TAKE_ITEMDAMAGE`,
defender equipment-slot selection draws `rand()%100` before checking any item;
the attacker weapon lookup follows it. Therefore equipment-free physical
arithmetic alone does not prove a no-ItemCrush helper/RNG path. Neutral enemy
equipment assumptions do not remove the defender draw. This finding supersedes
any inference that an empty equipment map closes ItemCrush chronology.

**OPEN:** reproduce both declared ItemCrush variants, source global rate,
raw-rand ownership and caller reachability across all three pins; bind the
selected equipment-free surviving-target draw before status without inventing
an original feature profile. Equipped mutation/UI/persistence stays separate.
Then prepared-action cancellation, persistent/coordinator propagation and
ultimate exit still require runtime/golden/full-region/verified pressure gates.
ID638's two positive slots remain OPEN; existing coverage is unchanged.


## Remote acceptance — 2026-10-06

37359587030 SUCCESS, job111930531041, exact input
ce4c7a16dc022e7ce88b314b8cb2845f0012389e,
tree4f5b4f6d2a845f7ea781b0ce5de6b09a59b269db. All shared157 tests,696 new
physical native comparisons,1920 original settlement calls,480 marker
comparisons and60 literal pet-guard cases reproduced remotely; derived artifact
11366277131 uploaded. Prior pending records are historical and superseded.
Only this explicitly bounded physical composition is accepted; all full-runtime
exclusions and two638 positive slots remain OPEN. Acceptance receipt is
`research/recovered/STONEAGE-BATTLEMODEL-PHYSICAL-ATTACKSEQ-ACCEPTANCE-R1.json`.

Further fixed-source inspection confirms legacy and TAKE_ITEMDAMAGE checks in
all three pins. Bismarck additionally guards TAKE_ITEMDAMAGE_FOR_PET and
TAKE_ITEMDAMAGE_FIX; the latter draws rand()%equipnum instead of rand()%100.
Those variants must be declared and audited separately, never inferred to be
part of an original executable. This is source inspection, not yet native
ItemCrush acceptance or runtime enablement.
