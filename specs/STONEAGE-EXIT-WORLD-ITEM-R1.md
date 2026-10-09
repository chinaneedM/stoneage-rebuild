# Original Exit, item lifetime and world object movement R1

Status: REMOTE ACCEPTED. Exact tested input fef1abd090fe6804453b7e0af264bdd54921cd9e / tree 33b767f45e791d77cc8b56e015709f4646a064c6. Action37878819171, job113653500431; acceptance metadata appended without changing tested code.

Evidence class: FACT only within the controlled pinned descendant source domain.
No Taiwan/Waei v1.0 or JSS executable equivalence and no runtime promotion.

The preceding gate executed complete nonplayer Exit with actual character
invalidation but collected item-end and warp calls. This gate executes original
item-end, warp, object accessors and map-link movement under the same complete
unchanged Exit body. Original source stays outside the repository.

## Executed and controlled boundaries

| Surface | Evidence |
| --- | --- |
| Complete Exit, CHECKINDEX, integer/work setters/getters, party, character end/remove helpers | Original bodies; prior identity receipt reproduced |
| ITEM_CHECKARRAYINDEX/CHECKINDEX/endExistItemsOne | Original bodies and compatible fixed item arrays; use/counter/owner observed |
| Player maximum, item getter and its slot guard | Original bodies; two player slots, one pet slot, one other slot |
| warpToSpecificPoint | Complete original default-header body; nonplayer paths only |
| Object type/coordinate getters and coordinate setters | Original bodies; valid object index 0, retained fixed object storage |
| MAP_objmove | Complete original body; actual linked lists and two synthetic 44x8 maps |
| Map floor lookup/coordinate validity, encounter values | Controlled adapters, not original map data/table resolution |
| Ticket warp destination | Exit's call to7001/41/6 asserted. Ordinary cases pass these coordinates unchanged. Same-floor controls substitute floor7000 only; invalid-destination controls force coordinate validation false |
| Network/talk/map broadcasts, descriptor, logging | Controlled collectors; unused player-only dependencies abort |
| CHAR_initCharOneArray | Hashed and structurally inspected; not executed in this gate |

The three clean source pins are inherited from
`STONEAGE-EXIT-DESTROY-TICKET-SOURCE-DOMAINS-R1.json`. New function/file identities
are in `STONEAGE-EXIT-WORLD-ITEM-SOURCE-DOMAINS-R1.json`.

## Domain and oracle

7,056 cases per profile and optimization; three profiles at GNU99 O0/O2 with
nonrecovering UBSan:42,336 native comparisons, each calling Exit twice. Symbolic
field ordinals/compatible witness structs are not an original ABI claim.
Players occupy0/1, pet2 and enemy3; matched player cleanup is excluded. Pet/enemy
membership absent or slot9 on either side, pointer failure, empty/sparse/full
items, item use states and live carried/pool/dead/duplicate peer references.
Ticket boundaries-1/0/999/1000/1001 at controlled now1000. Correct, missing,
misplaced and middle-of-chain old map links; existing destination neighbors;
invalid/same/cross-floor destinations; encounter-1/17 and object type0/1.

Independent Python state transitions compare both returns, actor use, actual
item-end invocation count, cleared slots, stale reads/rejected writes, global
item count, all item use/owner values, actor/object coordinates, work fields,
all20 battle membership/escape slots and every occupied map cell/ordered chain.
Complete ordered trace compares item-end, lifetime, ticket, warp, move result and
broadcast hooks. All map cells are scanned in the native snapshot, not sampled.
99 regression checks;12 semantic native mutations rejected (item reference
protection and object coordinate write at each profile/optimization).

## Bounded facts

1. Original character cleanup unlinks each subject item slot before item-end and
   marks actor unused after both carried/pool loops. Item-end scans only live
   players' carried slots. A live player's carried alias (including duplicate
   aliases) keeps item use, owner and count. Pool-only or unused-player aliases
   do not protect item use. An unused item or index-1 does not decrement count;
   empty subject slots still invoke item-end. This is historical behavior, not
   proof of valid natural ownership for the synthetic alias cases.
2. In gavin/iris expired synthetic enemy tickets can reach actual warp after
   actor invalidation. Retained valid object index allows original object setters
   and MAP_objmove to move the object and chain to7001/41/6 while actor coordinate
   and encounter writes are rejected. Ticket/start remain uncleared. Bismarck's
   Exit guard skips this post-destruction warp; its direct invalid-actor warp
   path is not run because a guarded work getter would return object index-1.
3. Warp sets actor/object coordinates before MAP_objmove. A missing old link
   returns false from map movement but warp still returns true, without rollback.
   Live ticket consumption precedes even a false warp due to invalid destination.
4. Gavin/iris leave a misplaced old-floor link where it was and fail movement.
   Bismarck's original map helper scans the old floor, detaches the found node
   and appends it at destination. Middle-node removal retains neighbors;
   insertion appends after existing destination nodes. This is bounded to valid
   acyclic fixed lists, not a general corrupt-world repair claim.
5. Static original allocator inspection finds zeroing followed by copying the
   supplied complete Char template. Dead-slot retention alone does not establish
   ticket inheritance through reuse. Template producers, init callbacks and
   actual allocator/reuse execution are still OPEN.

## Acceptance and continuity

The workflow reproduces the complete new native report and prior196,056 Exit
destruction/ticket,55,350 watcher,576 lifecycle and263,268 Exit-mode reports.
Acceptance requires exact tested HEAD/tree, successful Actions job, full ordered
remote report equality, all cmp gates and a derived acceptance receipt.

Pressure remains2486=2465 closed capability+18 OPEN+3 historical UB. Zero runtime
promotions. Prior evidence is preserved and this gate supersedes only the
explicit item-end/warp collector boundary within the stated domain.

Next priority: execute original default template/enemy creation/allocator/reuse
to establish natural ticket/object provenance. Then remaining actor ownership,
stats/property/timer, matched-player helper composition and watcher creation/
multi-actor boundaries before typed631/635 persistent/coordinator admission.
Invalid object indices, original map data, original binaries/build/ABI/network,
concurrency, JSS/Taiwan v1.0 and runtime admission remain OPEN. No engine/content
design transition.


Remote acceptance receipt:
`research/recovered/STONEAGE-EXIT-WORLD-ITEM-ACCEPTANCE-R1.json`.
Complete remote ordered report matches staged local bytes; all workflow cmp
checks passed. Report SHA25654ab876083faac9e87da83a6ce459b5edaa59fcb03a725aeb131ae9c9b7636ab.
Artifact11593391695 digest
sha256:ec269f379aba2a165c7c581b5d49ab6e671ecb37ccf91b54d317dc0d9e17b415
is GitHub metadata; archive bytes were not independently downloaded.
