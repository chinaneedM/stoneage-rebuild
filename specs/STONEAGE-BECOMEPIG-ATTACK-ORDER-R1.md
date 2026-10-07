# BecomePig original attack / Guardian / counter / retarget order source gate R1

Date: 2026-10-07 (UTC+8)
Status: **SOURCE_GATE_PENDING_REMOTE_ACCEPTANCE_ZERO_RUNTIME_PROMOTIONS**

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
3. `BATTLE_Counter`: counter eligibility precedes `BATTLE_AttackSeq`; positive
   counter damage is scaled to 75%; `BATTLE_DamageSub` follows. Between its
   `AttackSeq` and `DamageSub` call sites the counter caller does **not** map
   `Guardian` back to `defindex`.
4. Ordinary `BATTLE_Battling`: target adjustment precedes the main hit;
   per-hit profit work follows; later attack objects/attempts can target-adjust
   again before the counter chain; the counter chain follows the main-hit loop.
5. The BecomePig post-attack branch is after that counter chain. It rechecks
   `BATTLE_TargetCheck(..., defNo)` and resolves the post-effect participant from
   `defNo`, not from the main hit's local Guardian recipient.

The counter distinction is source evidence, not a design recommendation. A
modern reconstruction must not silently normalize it into ordinary-main-hit
Guardian semantics without a separately declared compatibility policy.

## Gate design

`tools/stoneage_becomepig_attack_order_audit.py` reads only clean exact pinned
checkouts and fails on commit drift, missing definitions, reordered required
events, an inserted counter caller Guardian remap, or changed post-BecomePig
target ownership. It emits SHA-256 identities and semantic booleans only.

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
