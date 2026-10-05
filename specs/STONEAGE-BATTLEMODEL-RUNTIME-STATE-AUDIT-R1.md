# StoneAge BattleModel runtime state audit R1

Status: **CLOSED_FOR_BOUNDED_RUNTIME_INTEGRATION**
Date: 2026-10-05

## Accepted state-carrier closure — 2026-10-06

This closure supersedes pending prerequisites in the historical audit below.
Exact-data37342593141, source/native37342593073 and supplemental helper
37344060042 all completed successfully. Their exact inputs and derived facts
are recorded in `STONEAGE-BATTLEMODEL-REFERENCE-R1.md` and
`research/recovered/STONEAGE-BATTLEMODEL-ACCEPTANCE-GATES-R1.json`.

The complete family is638/641/649/650; bounded runtime admission is only
ID638 at TEMPNO1178/1179, graphic101867/101868, skill slot3. Accepted type5,
object count4, turn1, hit30 and action numbers101867/101868 fit existing
action-local scheduling. Big5 witnesses select paralysis/index2 and attack70%;
UTF-8 witnesses select no matched status/modifier. Runtime must require an
explicit conditional profile and must not infer the original compiler.

Paralysis fits the existing six-status carrier and clears the remaining-round
command on success. No new generalized persistent schema is needed. Existing
HP, Guardian, base reactions, ride/death/ultimate and explicit pet ownership,
default selection and battle occupancy remain authoritative. Active-battle
disk resume is not accepted by this state-carrier closure.

The dedicated loop must schedule once, recheck each submitted target without
retarget, use the actual Guardian defender for physical damage/status, restore
the temporary BattleModel marker, consume reflect while suppressing return
damage, and keep wakeup versus status eligibility separate. Shared arithmetic
must be reused only where its accepted contract agrees. Preserve the separate
per-hit RNG requirements and safe DODGE presentation. Trap/acupuncture and
later transformation states remain structurally excluded.

**BATTLEMODEL_RUNTIME_STATE_AUDIT_R1 =
CLOSED_FOR_BOUNDED_RUNTIME_INTEGRATION.** Runtime implementation and pressure
promotion remain OPEN and belong on a fresh branch after main acceptance.

This audit maps the bounded PETSKILL_BattleModel fixed-descendant reference onto the existing deterministic single-player battle state. It is a state-carrier audit only and does not authorize runtime integration until the recovered25 exact OPTION/profile gate and the source/native reference gates are accepted.

## Existing persistent state is structurally sufficient

The current battle stack already carries participant HP/slots/commands, command setup effects, fixed combat profiles, BaseBattleStatusRuntime, common BaseDamageReactState, Guardian registrations, RidePetRuntime, ultimate/death/exited-entry state and the normal persistent settlement projection.

No new generalized persistent BattleModel object is required merely to hold the attack-object schedule. The schedule is action-local and belongs in a typed semantic submission and explicit action-time RNG bundle.

## Dedicated BattleModel hit loop required

The existing ContinuationAttack / AttackCrazed / WildViolent multihit loop cannot be reused unchanged. BattleModel builds an attack-object schedule before individual hits; each scheduled hit calls BATTLE_TargetCheck and skips an invalid/dead target without continuation-style retarget; Guardian redirect is honored only for type bit 0x4; nonphysical BattleModel passes reaction sentinel -1 to DamageSub; the actual defender is temporarily marked BATTLE_COM_S_BATTLE_MODEL around DamageSub; status is evaluated independently after each surviving positive-damage hit; and field7 action numbers belong to attack-object indices.

Runtime therefore needs a dedicated semantic loop that reuses already-accepted low-level ordinary attack primitives only where their contracts match.

## Target scheduling and source hazard

The opposing living target set can be derived from authoritative battle slots and current HP/exited state. The preserved BATTLE_MultiList/qsort presentation order is not claimed portable because of the known SortLoc anomaly; R1 may use deterministic battle-slot order as a modern presentation witness while preserving target-set and state-transform semantics.

If object count is positive while the opposing living list is empty, the preserved effect can reach RAND(0,-1). Modern R1 must fail closed/no-action for that source hazard rather than invent a random-domain result.

## RNG ownership

- configured field2 count <= 0: exactly one RAND(1,10);
- positive field2 count: no callback count draw; values above 10 clamp to 10;
- object count greater than living-target count: one RAND(0,N-1) per excess attack object, with replacement;
- otherwise: no target-selection draw;
- each executed AttackSeq/DamageSub hit owns only the ordinary hit RNG actually reached;
- each eligible status check owns its own RAND(1,100);
- skipped scheduled targets consume no hit/status RNG.

## Guardian and physical/nonphysical split

Existing GuardianRegistration state is sufficient. For type bit 0x4 physical hits, a live Guardian may become the actual damage/status target. For nonphysical hits, the BattleModel Guardian redirect branch is not used and reaction sentinel -1 bypasses DamageReact selection. This recovered type bit is unrelated to the unresolved historical numeric COM1 identity guarded by DD-019.

## Base status carrier

The generic status probability primitive can express BattleModel's caller-selected status/effect-hit, level range 30, level scale 1.0 and exact turn write. DRUNK halving can also be represented.

However the current common persistent status carrier includes only poison, paralysis, sleep, stone, drunk and confusion. Fixed descendants contain later/gated status families too. Runtime admission therefore remains blocked until the exact positive ID638 OPTION field3 is mapped by source-order byte identity. If ID638 resolves outside the six represented base statuses, this audit remains open until that state family is reconstructed or an evidence-backed narrower runtime scope is defined.

## Damage reaction boundary

Current BaseDamageReactState models VANISH / ABSORB / REFLECT / NONE. Physical BattleModel REFLECT cannot use ordinary reflect settlement unchanged: it consumes the defender reflect charge while suppressing reflected return damage, so damage remains on the defender. ABSORB and VANISH retain their shared semantics. Nonphysical BattleModel bypasses reaction selection entirely.

Fixed descendants also contain BattleModel exceptions for gated TRAP and ACUPUNCTURE families. The current modern damage-react model explicitly excludes those states. A bounded BattleModel R1 may execute only while trap/acupuncture state is structurally absent; it must not claim those later families are restored.

## Ride pet, death and settlement

The accepted ordinary DamageSub stack already supplies ride split, PETFALL, death/ultimate and persistent settlement semantics required by BattleModel. The dedicated loop should reuse those primitives and emit one authoritative HP-transition event per executed hit against the actual defender.

## Closure prerequisites

Before this audit can close, the reference branch must prove: exact callback population and ID638 identity; exact TEMPNO1178/1179 placement; derived field1 type and field2 object count; source-order field3 status; field4 turn and field5 effect-hit; field6 two-byte parser compatibility; field7 action numbers; fixed descendant source audit; and native target-planner equivalence.

If those semantics fit the carriers above, this audit can move to CLOSED_FOR_BOUNDED_RUNTIME_INTEGRATION without adding a new persistent-state schema. Runtime coding must then occur on a fresh runtime branch after reference acceptance.

**BATTLEMODEL_RUNTIME_STATE_AUDIT_R1 = OPEN_PENDING_RECOVERED25_OPTION_PROFILE_ACCEPTANCE.**
