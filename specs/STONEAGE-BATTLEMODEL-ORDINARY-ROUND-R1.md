# BattleModel ordinary round/state/coordinator R1

Status: LOCAL_VALIDATED; exact remote input/gates pending.

## Declared scope

`nonlethal_base_round_empty_equipment_ID638_R1` is an explicit opt-in to the
existing `resolve_ordinary_round`, `resolve_persistent_ordinary_round` and
coordinator `resolve_persistent_attack_wait_round` APIs. A typed
`BattleModelRoundAction` owns the admitted submission, physical/ItemCrush
contexts, authoritative opposing slot order, exact resistance map and ordered
draw tuple. Physical profiles/defense/field/Guardian/work powers/levels must
agree with current round participants and equipment-free item bindings.

Only base ATTACK/GUARD/WAIT/NONE commands, equipment-free/fist/zero weapon
critical/no NO_DUCK and accepted reduced-offset10 physical/ItemCrush scopes
are allowed. Other callbacks, combo/counter, ride and late overlays are
excluded. Persistent Vary metadata is excluded except an empty overlay.
**Every** new death/ultimate composition, including ordinary attacks elsewhere
in the round, is rejected. No returned transaction can use the unresolved
player ultimate default-pet projection from the prior handoff review.

## Timing and semantic dispatch

The existing prepared order is retained. The actor's common status tick runs
once before symbolic dispatch. Poison changes current HP. Paralysis/sleep/
stone suppression remains cancellation even if its one-turn counter expires.
Confusion may replace the symbolic skill with an ordinary attack and its own
ordinary attack rolls; the BattleModel draw tape must then be empty. Incomplete,
dead or otherwise suppressed actors also require empty action RNG.

Drunk expiration changes current work QUICK without re-sorting already
prepared initiative. The shared physical binder now accepts the current typed
status-runtime QUICK when provided, otherwise retaining callback setup QUICK.
The typed admission and post-setup attack/defense remain unchanged; setup is
not applied again after the tick. Dynamic defender QUICK also reaches the
physical defense formula. Surviving drunk tick owns drunk-Duck RNG before
Duck, in the same helper tape as later item/status/selection work.

Dispatch reads current HP/status/reactions/overkill/round flags and guarding
from the ordinary loop. Opposing slot order is explicitly supplied; it is
filtered by current liveness/occupancy at that actor's visit, not before the
round. No-target actions consume no RNG. All mapped source flags are reset
round-locally by the existing driver. Literal pet +5 guards remain in the loop.

Each helper hit is emitted as a version-tagged BattleModel event, with actual
Guardian routing/current HP/status and reaction resolution. An action event
retains the complete typed loop including consumed RNG. Successful common
status writes round-local COM1 NONE, removes guarding and cancels later
prepared actions; COM2/COM3 are preserved in current work. Already executed
actors never repeat their action/status tick. Multiple BattleModel actors read
intervening actors' current status. Round result exposes cleared identities.

NONE/source-target is an explicit **internal semantic carrier**, not a claimed
historical numeric BattleModel COM1. Automatic enemy-AI selection is unchanged
and general ID638 admission remains OPEN.

## Persistent/coordinator transaction

The existing state transaction commits nonlethal HP/status/reaction/overkill
and increments turn only after successful ordinary resolution. Cancellations
are not carried as permanent commands. Fresh next-round commands are prepared
normally. Any draw drift/death/ultimate failure leaves the immutable before
state unchanged; no death profit is claimed in this scope.

The explicit coordinator path re-admits each submission against its actual
current spawned template, the loaded skill runtime, and current pre-callback
work powers before creating setup effects. It rejects missing/duplicate actors,
template/OPTION/work drift and AttackMagic overlay; then returns a new battle
context with the accepted state. World payload/ownership/default selection are
not rewritten by this nonlethal battle-local transaction. It does not choose
the skill automatically or implement mid-battle disk resume.

## Validation and remaining gates

31 new witnesses:24 real ordinary rounds,3 state transactions and4 coordinator
transactions. Total428 tests PASS:31 new +283 prior handoff/shared/ordinary
+39 state +75 coordinator regressions. Three clean-pin native reruns also
PASS696 physical/3420 ItemCrush/1920 settlement/480 marker/60 pet checks.
CI reproduces these, and shared-file change workflows must be inspected before
main acceptance. Existing native comparisons verify hit machinery, not a new
original full-command-loop certificate. Synthetic fixtures patch only expected
OPTION byte identity; production admission rules retain exact pinned identity.

OPEN: automatic AI selection, full lethal/ultimate/profit flow, DD-020 explicit
default-pet exit correction, native full command-loop composition, equipped/
extra-slot/wider features, BattleModel golden/full-region/hash-verified pressure,
and the two ID638 positive slots. Baseline golden/region replays alone do not
certify new BattleModel scenarios. DD-018 restoration-first remains in force.
