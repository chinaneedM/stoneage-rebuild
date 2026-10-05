# BattleModel hit-helper lifecycle source audit R1

Date: 2026-10-06
Status: **CLOSED_BOUNDED_FIXED_DESCENDANT_HELPER_LIFECYCLE**

## Remote acceptance — 2026-10-06

Action **37344060042 SUCCESS** on input
`be9de3df70d4a872817f55fd484e9a08f4dd1f31` independently reproduces
the three pinned profiles and1296 controlled helper witnesses. Its audit job
111878092333 completed all steps successfully and uploaded artifact
11360861465, `battlemodel-hit-lifecycle`. The historical pending statements
below are superseded by this receipt. Both core reference gates also succeeded;
this acceptance retains every stub/exclusion/presentation limit below.

This is a supplementary fixed-descendant source audit, not runtime integration
and not recovered25 OPTION acceptance. The three source commits and file hashes
are recorded in the derived report
`research/recovered/STONEAGE-BATTLEMODEL-HIT-LIFECYCLE-SOURCE-AUDIT-R1.txt`.

## Native evidence and limits

The audit extracts the original `BATTLE_BattleModel_ATTACK` definition from
each clean pinned source checkout. Each profile executes432 controlled helper
vectors, **1296 total**. The source helper is compiled with stubs for common
AttackSeq/DamageSub/status arithmetic and presentation. The audit verifies
branch ownership, authoritative target selection, marker restoration and call
counts. It does not re-certify the stubbed shared arithmetic.

The matrix includes physical/nonphysical type, live/dead submitted target,
absent/dead/live Guardian candidate, surviving/lethal controlled damage,
MISS/DODGE/NORMAL outcome, NONE/ABSORB/VANISH reaction and failed/successful
paralysis status application. Some stub input combinations deliberately isolate
helper control flow; they are not asserted to be jointly reachable from a real
AttackSeq calculation. In particular, the MISS witness establishes ordering,
not a claim that an ordinary historical missed attack removes HP.

## Required runtime distinctions

- A dead submitted target skips AttackSeq, DamageSub, status and presentation.
- Physical type bit4 validates a Guardian candidate and may change the actual
  defender. A dead candidate is cleared. The defender's BattleModel marker is
  installed around the hit and restored afterward.
- Nonphysical hits keep the original actual defender and pass reaction sentinel
  -1 into DamageSub. The helper can still retain the Guardian candidate set by
  AttackSeq in protocol/status-notification fields. That notification identity
  must not be mistaken for the authoritative damaged/status recipient.
- DODGE skips DamageSub. MISS sets reported damage to0 after the DamageSub
  call site. Both suppress subsequent positive-damage wake/status branches.
- Positive damage calls DamageWakeUp only if the reaction is neither ABSORB
  nor VANISH. Those two reactions do **not** independently suppress the later
  status check: the source checks surviving defender HP and reported positive
  damage. Runtime must use the actual common DamageSub result for that check.
- Successful paralysis sets the configured turn and clears the actual
  defender's remaining-round command.

## Source presentation hazard

The helper declares `iPetDamage` without initialisation. The DODGE branch skips
DamageSub, then can pass `iPetDamage` into `snprintf`. No exact historical
presentation value is accepted for that path.

The native lifecycle harness suppresses `snprintf` argument evaluation so it
does not read this undefined source value. It records only whether the protocol
site is reached. A future modern adapter must use an explicit safe presentation
value, clearly separated from a claimed original wire-byte identity.

## Remaining gates

Recovered25 exact OPTION/profile identity and the two existing remote reference
gates remain pending. The new supplementary workflow reproduces this audit but
does not cancel or substitute those gates. This audit excludes pet-owner-ultimate
mapping, critical non-player knockout RNG, gated Ler transformations, item
crush arithmetic, complete ride/death persistence and status probability
arithmetic. Those remain governed by their separate source/runtime contracts.
