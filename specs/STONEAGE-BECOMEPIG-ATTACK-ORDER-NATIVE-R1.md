# BecomePig main-hit / Guardian / counter / retarget native composition R1

Date: 2026-10-07 (UTC+8)
Status: **NATIVE_COMPOSITION_GATE_PENDING_REMOTE_ACCEPTANCE_ZERO_RUNTIME_PROMOTIONS**

## Purpose

Strengthen the accepted static source-order gate by executing the relevant
ownership transitions in one transient native C program. This gate composes
already accepted exact reduced-profile physical `BATTLE_AttackSeq` /
`BATTLE_GuardianCheck` and exact `BATTLE_DamageSub` with exact pinned
`BATTLE_Attack`, `BATTLE_Counter`, `BATTLE_TargetAdjust` and the exact
BecomePig post-attack conditional.

No original source bytes are committed. Exact pinned source files exist only in
the CI working directory; repository evidence is limited to independent tooling,
hashes, semantic counts and derived reports.

## Native witnesses

Each of the three pinned descendant profiles runs the same three ownership
scenarios at both `-O0` and `-O2` under nonrecovering UBSan:

1. **ordinary main-hit Guardian** — exact GuardianCheck returns slot5; exact
   ordinary `BATTLE_Attack` maps that result before exact DamageSub, so the
   Guardian character receives the physical HP write. The later BecomePig
   post-effect still resolves the requested/final `defNo`, so the requested
   player transforms and the Guardian does not.
2. **dead requested target → retarget → post-effect** — an exact ordinary hit
   kills the requested slot0 target; exact `BATTLE_TargetAdjust` invokes a
   controlled first-live default selector and stores slot1; the exact BecomePig
   post-effect then transforms slot1, not the dead former target.
3. **counter Guardian distinction** — exact Counter AttackSeq selects a live
   Guardian at slot15. A transparent recorder around the unchanged exact
   GuardianCheck proves that selection. Exact Counter nevertheless passes its
   original `defindex` to exact DamageSub; therefore the original defender
   receives the HP write while the selected Guardian remains unchanged.

Scenario 3 deliberately protects a source quirk. It is not authorization to
"fix" counter Guardian handling by normalizing it to ordinary main-hit behavior.

## Controlled seams

This is a reduced feature profile. Counter probability is forced through a
controlled `BATTLE_CounterCheck`; `BATTLE_DefaultAttacker` is a deterministic
first-live selector used only to exercise the exact TargetAdjust caller; packet,
presentation and item/status side effects remain neutral. The BecomePig
post-effect uses a controlled valid option string and controlled successful
mod-100 draw because actual OPTION parsing and postattack short-circuit semantics
are separately native-certified.

The original historical PRNG, exact executable/compiler/ABI, wider optional
feature set, item/NPC/map timers, persistent coordinator, and JSS/Taiwan-v1
membership remain outside this gate.

## Acceptance

Remote acceptance requires all three exact source pins, 18 native comparisons
(3 scenarios × 2 optimization levels × 3 profiles), source-order regression
tests, no UBSan diagnostic, identical O0/O2 semantic rows, and the resolution:

`BECOMEPIG_MAIN_GUARDIAN_COUNTER_RETARGET_NATIVE_COMPOSITION_PASS_ZERO_RUNTIME_PROMOTIONS`.

Passing closes only this bounded ownership composition. BecomePig runtime slots
remain at zero. The next priority is item/NPC/map timer composition and remaining
stat/property/ownership/death/follow/PvP/watch/enemy paths before typed631/635
persistent/coordinator admission.
