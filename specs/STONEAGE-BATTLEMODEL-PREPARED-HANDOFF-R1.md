# BattleModel prepared handoff R1

Status: LOCAL_VALIDATED; remote exact-input gate pending.

## Scope and identity

`tools/stoneage_battlemodel_prepared_handoff.py` connects the accepted
equipment-free physical/ItemCrush hit loop to existing `PreparedBattleRound`
work snapshots. Required scope is
`base_commands_prepared_empty_equipment_ID638_R1`. ID638 admission, explicit
source/charset/defense/item variants, reduced offset10/no ride/nonthrowing/
gDamageDiv0 and all physical exclusions remain mandatory.

The next actor is identified by a typed BattleModel submission. Its prepared
NONE is an **internal carrier**, not a historical BattleModel COM1 number.
No ordinary AI dispatcher consumes this seam yet. Base ATTACK/GUARD/WAIT/NONE
commands alone are supported; combos and other callbacks are rejected.

## Ordered handoff

The caller supplies the exact already-executed ordered prefix and current
entries at that cursor. Entries, prepared participants and slots must have
exact identity/kind/max-HP/side coverage. Current HP is authoritative; prepared
HP may be stale after preceding hits. No initiative recalculation or sorting.
Actor status processing/rewrite is outside this seam: an actor with any active
base status, cleared command, incomplete input or nonliving entry is rejected.

Prepared commands override physical context command labels. Successful status
clears COM1 to NONE, retains COM2/COM3/input readiness, removes guarding, and
updates even an already-executed target's current work. It cannot undo that
target's earlier action. Guardian identity receives HP/status/clearing. The
existing loop continues to consume physical/item/status/target draws in order.

The handoff exposes current entries, commands, HP-refreshed prepared actors,
status/reaction/overkill maps, twenty source flags and completed prefix.
`ordinary_continuation()` disables completed actors' input without removing
their slots or re-sorting. The caller must use the exposed current runtime maps
with the existing ordinary resolver. It refuses any ultimate flag or new
BattleModel death until exit/profit scheduling is integrated. A living ultimate
flag remains a flag; no HP loss or removal is invented.

## Round boundary and acceptance limits

`reset_battlemodel_round_flags()` is an explicit **new preparation** boundary:
it clears command-cleared/ultimate flags only and retains HP, status, damage
count, reaction charges, marker, overkill and target eligibility. It does not
settle exits/profit or reactivate removed participants. Fresh commands must be
prepared normally. No round-local cancellation is written to persistent state.

Twelve independent witnesses include actual ordinary continuation after a
one-turn paralysis expires (no attack RNG/action), failed status allowing an
ordinary attack, no repeated actor/status tick, current HP death, Guardian
routing, reflection charges/damage count, fresh GUARD after new preparation,
and failed identity/scope/prefix/actor/RNG boundaries. All283 tests pass locally:
12 new +101 existing ordinary round +170 accepted loop/shared tests.

CI repeats these tests and existing696 physical/3420 ItemCrush/1920 settlement/
480 marker/60 pet native comparisons. Those native gates cover the existing
hit machinery; the new handoff is tested against the independent existing
ordinary resolver, **not** certified as an original full command loop.

OPEN: actor status clock/confusion rewrite and initiative work, full ordinary
BattleModel dispatch, persistent/coordinator transaction, ultimate death/exit/
profit, equipped mutations/extra slots/wider features, golden/full-region and
hash-verified pressure. No ID638 positive slot or overall coverage promotion.
DD-018 restoration-first and DD-019 original numeric-profile ambiguity remain.
