# BattleModel bounded post-AttackSeq hit loop R1

Date: 2026-10-06
Status: **LOCAL_TESTED_REMOTE_GATE_PENDING_FULL_RUNTIME_OPEN**

This implementation advances the saved integration plan after exact typed
admission acceptance. It executes a bounded scheduling/helper composition;
the ordinary round, battle state, coordinator and pressure path do not enable
BattleModel through this milestone.

## Required explicit scope

The caller must select `HIT_LOOP_SCOPE_R1`: reduced SIDE_OFFSET10, no mounted
ride, nonthrowing attack, no ItemCrush and gDamageDiv0. These are controlled
execution exclusions, not claims about the recovered original executable.
AttackSeq is a typed injected dependency and owns dodge/critical/damage/guard/
minimum-damage draws and Guardian eligibility. Tests inject controlled
AttackSeq results; they do not verify production physical damage arithmetic.
No numeric original COM1 or raw proprietary OPTION is added.

The helper's source ItemCrush call occurs before status on surviving targets.
Its equipment and possible RNG work remains an integration gate. The explicit
no-ItemCrush scope cannot certify an equipped production battle.

## Implemented state and order

- Immutable entries bind unique participant identity, HP/maxHP, base status,
  paralysis resistance, reaction charges, marker, cleared command and ultimate
  entry flag. The exact submission must match the enemy actor identity.
- Preserve the caller's authoritative initial MultiList order. Four objects
  cover its first targets and recycle across larger lists. Scheduled ordinal
  remains separate from object index, including coverage ordinal4/object0.
- Each excess selection occurs only after the previous AttackSeq and helper
  settlement/status. Selection uses the initial pool even after deaths. Dead
  or explicitly invalid targets skip physical/status/death draws; their reached
  excess selection still consumes its draw. No retarget, combo or counter.
- A strict flat RNG tape binds owner and scheduled ordinal, validates reached
  ranges and rejects missing, extra or misordered draws. The injected physical
  dependency cannot consume target/status/critical-death ownership.
- Recheck a returned physical Guardian candidate's target validity. Route HP,
  wakeup, status and command clear to the actual defender; preserve its marker.
- BattleModel reflection consumes its charge and preserves both HP; positive
  reported damage can wake and apply status. Absorb/vanish suppress wakeup,
  while positive surviving reported damage separately permits status checks.
- Explicit Big5 paralysis uses the shared20-resistance strict comparison,
  configured exact turn1 and immediate cleared-command state. Existing active
  status blocks before RNG. UTF8 unknown status owns no status draw. Unused
  general-status attributes in the paralysis primitive are modern placeholders.
- Critical non-player death consumes its own draw before subsequent selection;
  ABIO bypasses that draw. Raw-threshold ultimate may set a surviving entry
  flag without inventing HP0 or exit. TargetCheck does not itself test that
  ultimate flag; complete round-end flag-to-exit integration remains OPEN.
- A pet pre-hit guard literally reads flattened target+5. Explicit twenty-entry
  flags are required, with mapped-entry consistency. Under reduced offset10,
  pet targets5..9 check opposing entries10..14, independently of owner0..4.
  This does not assert Bismarck's excluded multiplayer offset12 behavior.
- DODGE skips settlement and uses an explicit safe modern pet-presentation
  value0; original uninitialized presentation bytes remain OPEN.

## Validation and next gates

Local81 tests PASS include16 new hit-loop tests, exact admission, conditional
reference, shared reactions/status and actual-data-probe logic. Witnesses cover
N1/2/4/5/10, recycled indices, interleaved ownership, all-target death, reflect
charge exhaustion, absorption/vanish, Guardian routing/death, resistance
boundaries, existing status, ABIO/critical death, all pet guard slots and
immutable state/failures.

The existing transient native settlement reproducer gains an opt-in direct
model comparison:160 physical marker cases/profile,480 comparisons across
the three clean fixed pins. All1920 original native calls still pass. The new
literal pet-guard reproducer adds20 native helper calls/profile,60 total, under
explicit reduced offset10 and controlled shared stubs. This is not a combined
live battle nor original build selection. CI reproduces these counts; remote
gate result remains pending at implementation publication.

Next connect the accepted production AttackSeq path and equipment/ItemCrush
boundary, prepared action execution/command-clear lifetime, persistent state,
coordinator, ultimate exit and excluded mounted compositions. Require golden,
full-region and hash-verified pressure acceptance before promoting ID638's
two positive slots. Existing accepted coverage is unchanged by this seam.
