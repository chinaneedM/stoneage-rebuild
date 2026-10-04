# StoneAge Refresh ordered runtime R1

## Scope

This runtime is a conditional descendant-reference execution domain over the
verified recovered25 callback population. It does **not** assign an original
binary command number, original compiler charset, Taiwan-v1 membership, or a
historical skill-array index.

The verified callback population is IDs 583/584/591/592/593. Only IDs 583 and
592 have positive recovered enemy slot references (4 + 2 = 6 uses), therefore
only those two IDs can become executable.

## Admission

All five callback rows must be present with exact FIELD/TARGET/COST/ILLEGAL,
two-byte OPTION hashes and conditional iris CP950 parse results. ID 591 is the
one TARGET=1 row; 583/584/592/593 are TARGET=2.

The ordered bridge admits enemy actors selected through their authoritative
seven-slot template only. ID 583 selects status index 10 (silence/Nocast);
ID 592 selects status index 0, the source wildcard branch. The fixed-source
command remains symbolic as BATTLE_COM_S_REFRESH while BATTLE_COM_ATTACK is an
internal scheduling carrier only.

## Ordered behavior

The callback itself owns no RNG. The executor uses direct COM2/LOW dispatch.
For a live single target, no target RNG is consumed. If that target has died
before Refresh executes, the admitted gavin/iris MultiList seam consumes
explicit rand()%10 witnesses until it resolves a living same-side target.

Recovery inspects the target's highest positive status index and clears exactly
one status when it matches the requested index. The status-zero wildcard keeps
the source's wrong-namespace CONFUSION bound, which admits all active indices
in the pinned iris table. It still clears only the single highest state.

The reconstructed complete target domain contains base statuses 1..6, Weaken
7, Barrier 9 and Nocast/silence 10. Any target carrying an unmodeled active
status (including index 8 or later extensions) is fail-closed because the true
highest index is unknown. Clearing silence also writes NC=0. Clearing Weaken
keeps already-prepared current-command powers until normal post-round
preparation restores baseline; clearing Barrier removes its current counter.

Refresh does not execute ordinary physical damage, ordinary counters, or base
combo membership. Native confusion rewrites discard the semantic Refresh
command and restore ordinary attack behavior. Sleep/paralysis/stone and Barrier
suppression consume no Refresh target RNG.

## Persistence

Base status and late-status overlay mutations flow through the existing
persistent battle state. The next round therefore observes silence eligibility
restored after ID 583, and the wildcard-cleared highest status absent after ID
592. No Taiwan-v1 save field is added.

## Open boundaries

Original compiler/execution charset, original recovered numeric COM1, historical
introduction/membership, unmodeled extension statuses, and unsupported original
target-list domains remain OPEN. This R1 may be classified executable only
after dedicated runtime, coordinator, source/data and cross-regression Actions
all pass.
