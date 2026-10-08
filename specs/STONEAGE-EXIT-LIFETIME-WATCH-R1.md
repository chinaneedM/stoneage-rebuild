# Enemy slot validity and watcher chain lifecycle R1

Status: LOCAL PASS, remote exact-input acceptance PENDING. Zero runtime promotions.

This gate executes original default-profile character end-data/end-one,
item-removal, integer/work getters and PartyUpdate bodies, plus original
WatchLink/WatchUnLink/DeleteBattle/Finish. It preserves all three pinned
descendant identities. Original C remains transient; only hashes and derived
semantic results are committed.

## Character-slot witnesses

Twelve cases per profile cross initial live/dead slot, controlled pointer
availability, and no-party/leader/member state. Actual item cardinalities are
derived from default headers: gavin/iris24 carried slots, Bismarck54; all have30
pool slots. Bismarck's original item-limit helper executes with those constants.
Original removal functions set each slot to -1 before the controlled item-end
hook. The hook independently checks that unlink has already happened and that
the character is still live during item cleanup. End-data then sets use=false.
The fixed character slot is not freed or zeroed by that body.

Native retained-slot witnesses preserve a concrete profile difference:
gavin/iris ordinary getters still read retained integer/work values after the
slot becomes invalid; their PartyUpdate reads retained party mode and can send
controlled party notifications. Bismarck getters return -1 and PartyUpdate
guards the invalid subject. Original Exit source separately shows its post-party
ticket block is liveness guarded only in Bismarck. Actual ticket/warp execution
through the full Exit caller is not accepted by this helper gate.

## Watcher chain witnesses

Eighty-four cases per profile cover zero through three watcher nodes, Link into
a detached node, UnLink/Delete at every head/middle/tail, and Finish of a PvE
root. Representative entry positions0/4/9 use controlled generic Exit/Profit
hooks, not the original player i+5 restore branch. The exact original
Link/UnLink/Delete/Finish bodies execute with valid pointers into one five-slot
array and an acyclic chain. All use/link/counter/entry state and Profit/Exit/
DeleteItem node masks are checked by an independent oracle.

Observed historical defect within this domain: Finish exits all linked watcher
actors but its deletion loop deletes only the first watcher before deleting
the root. DeleteBattle calls UnLink, which clears the current node's pNext;
the loop then reads that cleared pNext and stops. With two or three watchers,
later nodes remain used, with a residual relinked chain. This proves immediate
post-Finish occupancy, not a permanent resource leak or the absence of later
task/Stop cleanup. No corrected original source is substituted.

## Validation boundary

576 comparisons =3 profiles x(84 watch +12 character cases) xO0/O2 GNU99 with
nonrecovering UBSan. 68 tooling/domain/regression checks; prior accepted
263268 Exit-mode comparisons must reproduce the complete stored report.
Source contracts and file/function/default-header identities remain pinned.
Exact-name function extraction rejects Strict-style prefix collisions.

Symbolic ABI/compatible structs, property pointer availability, item destruction,
network/logging, generic Exit/Profit, EntryInit and party size are controlled.
Full original Exit+actual destruction composition, item-end internals, watcher
creation/Stop/task cleanup, cycles/invalid addresses, concurrency/reuse, original
compiler/executable/ABI/PRNG/JSS/Taiwan-v1 and modern runtime remain OPEN.
Pressure unchanged2486=2465 closed capability+18 OPEN+3 historical UB.
