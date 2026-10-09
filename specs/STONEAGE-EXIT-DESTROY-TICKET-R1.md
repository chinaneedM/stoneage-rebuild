# Complete nonplayer Exit with actual slot invalidation and ticket lifetime R1

Status: LOCAL PASS; remote exact-input acceptance PENDING. Zero runtime promotions.

This gate executes the entire unchanged default _BATTLE_Exit body at all three
pinned descendant commits. It replaces the former trace-only enemy destruction
hook with original end-one/end-data/carried/pool removal bodies, original integer
and work getters/setters, original CHECKINDEX, PartyUpdate and battle validity.
Compatible symbolic structs/handles remain controlled; original C stays transient.

## Domain

32,676 cases per profile/optimization; 196,056 native comparisons across three
profiles and O0/O2 GNU99 with nonrecovering UBSan. Each case invokes complete
Exit twice, so there are392,112 complete caller invocations. 86 tooling/domain/
regression checks;12 native semantic mutations must be rejected. The complete
accepted55,350 watch-cleanup,576 lifecycle and263,268 Exit-mode reports are
reproduced byte-for-byte. New report equality is checked against staged bytes.

Cases include pet/enemy membership on both sides at every slot0..9 or absent,
live/dead actor guards, invalid/unused battle guards, controlled pointer failure,
three party modes, valid/invalid owner slots, ticket times-1/0/999/1000/1001 at a
fixed now1000, start0/900, empty/head-and-tail/full item patterns, Fox state-1/2,
and representative PvE/PvP/WATCH types. Live unmatched players provide a positive
ticket control. Matched player cleanup is excluded here; its earlier bounded
gates remain separate. No claim is made that synthetic enemy party/ticket state
is naturally reachable in the recovered historical game.

Every return code, actor use, item-hook/cleared-slot count, independent unlink/
live-before-item-hook invariant, retained appearance/work/ticket state, all20
membership/escape slots and ordered destruction/item/party/message/warp/stale
read/rejected-write events are checked against an independent state oracle.

## Bounded observations

- Matched enemy Exit unlinks membership, updates FINAL/battleindex, executes
  original item cleanup and marks the character slot use=false. The fixed slot
  is retained; the next complete Exit returns CHARAINDEX. A controlled missing
  pointer leaves the slot live. Pet Exit does not destroy its character slot.
- Each carried/pool slot is set-1 before its controlled item-end call, including
  initially empty slots. Capacities are24+30 for gavin/iris and54+30 for Bismarck.
  Calling item-end with-1 is not a claim that an actual item is destroyed.
- Gavin/iris ordinary reads still consume retained work values after destruction.
  PartyUpdate can notify controlled party peers from that stale state. With an
  expired positive ticket, Exit can invoke message and warp hooks with use=false.
  Both attempted ticket-clear writes are rejected by actual setter liveness
  guards, leaving the retained expired time/start unchanged.
- Bismarck's PartyUpdate and Exit ticket subject guards skip the invalid actor.
  Its independent party owner guard rejects an invalid owner even if the subject
  is live. All three profiles' integer/work setters require a live subject.
- Ticket processing uses strict0<ticket<now; equality/future/zero/negative times
  do not invoke the expiry hooks. Live pet/unmatched-player controls clear their
  ticket before the one warp invocation; repeat Exit does not repeat that expiry.
- Original Bismarck BATTLE_CHECKINDEX rejects unused battles before Fox restore;
  gavin/iris bounds-only validity permits restore before the later NOUSE return.
  This is more specific than the earlier controlled validity-adapter gate, not
  a claim that the prior report tested this actual validity body.

Mutations alter only transient generated witness C: remove end-data invalidation
in all profiles; bypass gavin/iris work-setter liveness or Bismarck's ticket
subject guard. The independent oracle must reject each at both optimizations.
No patched original code is published or used as the accepted source.

## Boundaries and next work

Controlled: fixed three-character array, symbolic ABI/field bounds, character
pointer availability, time1000, item-end internals, party size5 and notification,
talk/network hooks and warp collector. Unused matched-player cleanup dependencies
abort if reached. Warp hook proves invocation to7001/41/6 with the recorded live
flag; it does NOT prove successful world/object movement or original warp safety.
Original item-end internals are not executed. No freed-pointer/reuse/concurrency
or original executable/compiler/ABI/PRNG/JSS/Taiwan-v1 equivalence is inferred.

OPEN: actual warp/object/item-end composition; initialization/reuse and natural
reachability of stale enemy party/tickets; multi-membership/multi-actor/follow/
ownership/stat/property/timer construction; matched-player composition with
these actual helpers; watcher creation/multi-actor and typed631/635 persistent/
coordinator runtime admission. Pressure remains2486=2465 closed capability+18 OPEN
+3 historical UB;0 promotions. Next audit original warp/object and item-end with
initialization/reuse provenance, then remaining actor-state/runtime boundaries.
