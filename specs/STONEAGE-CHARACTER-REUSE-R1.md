# Original default-character construction and allocator reuse R1

Status: REMOTE ACCEPTED. Exact tested input a543758d8d061646b810935503a1095181f0d9aa / tree 6b8a68ace1677287ef8d4b3a1360711e5dce6ff1. Action37880212015 / job113657937185 succeeded. Acceptance metadata only; tested code unchanged.
Evidence class: FACT bounded to three pinned descendant source profiles. No
original executable/JSS/Taiwan-v1 equivalence, no runtime-pressure promotion.

The previous world/item gate only inspected allocator zero-and-copy. This gate
executes the complete original `CHAR_getDefaultChar`, `CHAR_initCharOneArray`
and `CHAR_constructFunctable` functional bodies. The Bismarck allocator's
cpp-expanded diagnostic is replaced with a logging event; the original function
hash is retained. Original C remains transient outside this repository.

## Domain and adapters

4,224 ordered cases per profile/optimization, three profiles at GNU99 O0/O2
with nonrecovering UBSan: 25,344 native comparisons and 50,688 allocation calls.
Each case calls allocation twice, optionally releasing the first returned slot
by a controlled direct use=false write. This is not complete Exit/reuse execution.
Static sequence numbering advances across the entire ordered stream and is
independently tracked; wraparound is outside the domain.

Player/pet/other partitions have positive capacities 2/2/3. Every within-partition
occupancy mask and starting cursor executes; both player/pet, enemy and generic
other types are covered. Zero-size partitions are excluded. Cursor-zero cases
also exercise original lazy counter initialization. All witness array fields,
function identities, sequence, copied opaque marker and all seven slots are
compared after each allocation, together with lookup/callback/log order.

Compatible witness structures and symbolic field ordinals are explicit adapters,
not historical ABI. Carried item capacities retain 24/54 source-profile values;
other small witness arrays are controlled cardinalities. Union storage is shared.
The original getter uses a controlled two-entry default table with dirty source
work/callback/opaque values, matching and unmatched image selection. Actual
original default-table membership and defaultPlayer initializer are not executed.
A dirty supplied-template control and absent/success/failure/state-writing init
callbacks distinguish old-slot retention from input/callback-origin state.
Lookup and char-function getters are adapters; constructor loop is original.

## Bounded findings

- The original default getter resets ticket/start/object work fields to zero,
  irrespective of controlled source-template work fields. Its explicit FD value
  is -1; gavin/iris also set chatroom -1, Bismarck leaves it zero. It copies only
  the declared early data prefix and flags; inventories are initialized empty.
  This demonstrates getter behavior, not a world-object allocation or no-object
  sentinel interpretation: object work value zero alone proves neither.
- Allocation searches only the requested partition, wraps at its end and fails
  when that partition is full. Available slots in other partitions are ignored.
- An unused destination is completely replaced from the supplied Char before
  init lookup/callback. Dirty input or a callback can supply ticket/object fields;
  retained dead-slot values are not themselves inherited through the tested
  independent input templates. Aliasing the input to the destination is excluded.
- Callback sees the copied use/state before the allocator forces success live.
  Failure leaves a copied unused slot, leaves cursor and global sequence unchanged,
  and skips function-table construction. A later successful attempt can reuse it.
- Success forces use=true, executes original function-table construction,
  advances partition cursor and assigns the next creation sequence. Controlled
  direct release plus reallocation replaces callback-origin work and function
  state with fresh input and gives a new sequence.
- Static complete `ENEMY_createEnemy` inspection pins the call to default image
  31010 followed by allocator; no direct CHAR_WORKTICKETTIME/START or
  CHAR_WORKOBJINDEX symbol appears in that preprocessed body. This is a lexical
  bounded source finding, not a transitive helper/callback proof. The entire
  creator is hashed, not executed.

18 native semantic mutations (copy removal, ignoring callback failure, changing
work zero initialization across every profile/optimization) must be rejected.
108 regression checks and all five predecessor complete reports are required.
Remote acceptance requires exact source HEAD/tree, successful job, all report cmp
gates and complete remote ordered report equality, with a derived receipt.

## Remaining work

Execute the actual original default-table/defaultPlayer initialization with
profile/enum/layout provenance, then full enemy creation, its init and other
helpers and ticket/object provenance. Compose actual Exit and allocator reuse
before making any naturally reachable state claim. Input/destination aliasing,
zero-size partitions, sequence wrap, original build/ABI/PRNG/maps/network and
JSS/Taiwan-v1 parity remain OPEN. Remaining actor ownership/stat/property/timer,
matched-player/watch creation/multi-actor and typed631/635 persistent/coordinator
boundaries remain separate gates. No engine/content-design transition.

Pressure unchanged: 2486 = 2465 closed capability + 18 OPEN + 3 historical UB;
zero runtime promotions. Receipt: STONEAGE-CHARACTER-REUSE-VALIDATION-R1.json.

Remote complete ordered report equals local bytes; every workflow cmp gate passes.
Receipt: research/recovered/STONEAGE-CHARACTER-REUSE-ACCEPTANCE-R1.json.
Report SHA256 cbebb27b3923817c7804545cfedb882d90f4a89423ee05dd32bf6eb1b0f9da5a.
Artifact11593249623 digest sha256:cd38d68dee6e7bdbabba8d0372947b2ab59ead340fdb3c881ebfb77cf2ef9261
is GitHub metadata; archive bytes were not independently downloaded.
