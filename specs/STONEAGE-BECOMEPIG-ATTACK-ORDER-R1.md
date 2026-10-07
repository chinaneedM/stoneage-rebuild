# BecomePig original attack / Guardian / counter / retarget order source gate R1

Date: 2026-10-07 (UTC+8)
Status: **CLOSED_BOUNDED_CORRECTED_PINNED_DESCENDANT_SOURCE_ORDER_ZERO_RUNTIME_PROMOTIONS**

## Scope

This gate records only the observable control-flow order in the three already
pinned descendant server sources used by the project. It does not identify an
original JSS/Taiwan executable, ABI, compiler, PRNG, feature date, or deployable
runtime. Original source files are transient CI inputs; the repository stores
only independent audit code, tests, hashes, booleans and derived reports.

Profiles and exact commits remain the shared `PINNED` / `LAYOUTS` identities in
`tools/stoneage_guard_break2_source_audit.py`.

## Required ordered facts

For each pinned profile the gate must independently establish all of the
following from real C definitions, with comments and string literals excluded
from token matching:

1. `BATTLE_AttackSeq`: Duck is evaluated before Guardian; a successful Guardian
   changes the function-local defender before critical/damage arithmetic.
2. Ordinary `BATTLE_Attack`: `BATTLE_AttackSeq` returns first, then the caller
   maps a nonnegative Guardian to the authoritative defender, then
   `BATTLE_DamageSub` applies the main hit.
3. `BATTLE_AttackSeq` only invokes `BATTLE_GuardianCheck` when the caller
   supplies `*pGuardian == -1`. Ordinary `BATTLE_Attack` initializes that
   sentinel to `-1`, but `BATTLE_Counter` initializes `Guardian = -2`.
   Therefore the counter path bypasses GuardianCheck entirely before applying
   its 75% positive-damage scale and calling `BATTLE_DamageSub` on the original
   defender. The absence of a counter caller remap is secondary; no Guardian was
   selected in the first place.
4. Ordinary `BATTLE_Battling`: target adjustment precedes the main hit;
   per-hit profit work follows; later attack objects/attempts can target-adjust
   again before the counter chain; the counter chain follows the main-hit loop.
5. The BecomePig post-attack branch is after that counter chain. It rechecks
   `BATTLE_TargetCheck(..., defNo)` and resolves the post-effect participant from
   `defNo`, not from the main hit's local Guardian recipient.

The counter `-2` sentinel distinction is source evidence, not a design
recommendation. A modern reconstruction must not silently normalize counter
handling into ordinary-main-hit Guardian semantics without a separately
declared compatibility policy.

## Gate design

`tools/stoneage_becomepig_attack_order_audit.py` reads only clean exact pinned
checkouts and fails on commit drift, missing definitions, reordered required
events, loss/change of the ordinary `-1` versus counter `-2` Guardian sentinel,
an inserted counter caller Guardian remap, or changed post-BecomePig target
ownership. It emits SHA-256 identities and semantic booleans only.

`tests/test_stoneage_becomepig_attack_order.py` uses independent synthetic
fixtures to prove the detector rejects main Guardian reordering and post-effect
reordering, and explicitly detects a counter caller Guardian remap instead of
silently accepting it.

## Boundary

Passing this gate closes only a **pinned-descendant source-order fact**. It does
not yet prove native execution equivalence for the combined main-hit/counter
chain, random target selection values, equipment/reaction/status side effects,
or persistent/coordinator behavior. No BecomePig runtime promotion is allowed.

After remote acceptance, the next gate is a controlled native composition of
the same order and ownership distinctions, followed by item/NPC/map timer
composition and the remaining stat/property/ownership paths.


## Remote acceptance

- Gate input: `8aa218c0b86f41ece267b3d73b92da470099b0ec`.
- GitHub Actions: run `37636720951`, job `112844768574`, **success**.
- Derived report commit: `68e77d8cc3624904bd419d5862d3512c13ab46ce`.
- Artifact: `11490360820`, digest `sha256:810941e1fb71b1271ea7d7306fa279f4cda01fd1e8a79edb3fc02a7b71d77908`.
- Resolution: `BECOMEPIG_ORIGINAL_MAIN_GUARDIAN_COUNTER_RETARGET_ORDER_SOURCE_PASS_ZERO_RUNTIME_PROMOTIONS`.


## Semantic correction discovered by native composition

The initial accepted wording described Counter as computing through a local
Guardian and merely omitting the caller remap. Controlled native composition
proved that wording too weak and materially misleading: Counter supplies
`Guardian=-2`, while `BATTLE_AttackSeq` gates GuardianCheck on exactly `-1`.
Thus Counter bypasses GuardianCheck. The earlier report remains historical
evidence of the first audit iteration, but its Guardian interpretation is
superseded. This corrected source gate passed remotely and supersedes the initial Guardian interpretation.


## Corrected remote re-acceptance

- Corrected gate input: `c8c57b5a0475d6505b46aad8c9d085bac4f26c50`, tree `60e25f5f7de706475ca4d31585585931f8861d0e`.
- GitHub Actions run `37640049824`, job `112856277061`: **success**.
- Artifact `11491361919`, digest `sha256:a0db883dde384f92471e61a1197572e3ee634b22472d16eedbd5e2f157cd3179`.
- Derived corrected report commit `98c34f705d09141a58969daac1a461b4ce3f6b4d`, blob `fcf719083455b301fd789c1a326fbd3530c30d1a`.
- The initial `8aa218c0...` acceptance remains historical audit evidence but its Counter/Guardian interpretation is superseded by this corrected acceptance.
