# Original object registration and preserved enemy nonownership R1

Status: bounded native LOCAL PASS / REMOTE ACCEPTED at exact tested input
adae57319685b272c73ab431d72128fe2a40af3a; Actions38022136836 success. This is a
descendant-source research gate, not original JSS/Taiwan-v1 runtime admission.

## Question and executed evidence

The accepted loader gate established zero ticket/start/object work fields after
ordinary enemy creation from preserved master bytes. That alone did not establish
whether zero was an invalid object sentinel or a world-object ownership relation.

This gate executes the complete original `CHAR_createCharacter`, object-array
initializer/allocator/accessors/owner search/release, map floor lookup/list
get/append/add/remove helpers, and original empty-registry character/item-release
path beside the accepted master loader and ordinary enemy creator. Actual original
`Char`, `Object`, `MAP_Map`, `MAP_Objlink`, enums and transitive headers are used.
Complete preprocessed body/file/header/private-declaration hashes are pinned.
No original source, headers, master records or assets are copied into this repo.

FACT within this bounded configuration:

- Two world players occupy character slots0/1 and object slots0/1. Both objects
  are linked to the same map cell. The original persistent allocation cursor
  alternates the two owners across cycles; slot0 is valid and live, owned by
  world player0 or1. No cursor reset is injected into the original allocator.
- An ordinary enemy born into character slot4 still has object work0. Reading
  object0's owner returns0 or1; original owner search for character4 returns-1.
  Enemy creation and subsequent character-slot4 release/recreation do not change
  either world object's named fields or the map links. Zero work does not prove
  ownership or an invalid sentinel in this execution.
- A full object table rejects a third direct allocation without replacing either
  owner. After player0's character-only release, its object and map link remain.
  A world-constructor retry against that full table rolls the newly allocated
  character back through actual character/item-release helpers.
- Explicit `endObjectOne` on player0's object unlinks the map node and marks the
  object unused, retaining its other named fields. A subsequent world constructor
  reuses that slot and appends its map link at the tail: `[0,1]` becomes `[1,0]`
  or `[1,0]` becomes `[0,1]` after remove/reuse, depending on the original cursor.
  Explicit object release and character-only release are separate operations.

These facts establish concrete nonownership of the preserved ordinary enemy in
the tested occupied-slot0 state. They do not establish what every higher-level
battle caller, watcher, Exit branch or original allocator/reclaimer does.

## Inputs, adapters and field coverage

Gavin uses its own same-pin setup-selected unmodified enemybase1.txt/enemy1.txt
bytes. Bismarck executes its original loaders on those bytes as a cross-profile
input witness, not proof of its own historical content. Each loads1,816 templates
and2,935 variants;1,532 ordinary eligible variants are selected without rewriting
records, at controlled levels1/20 and four raw Rand modes. Iris's original Windows
conversion remains unexecuted OPEN; no replacement converter is supplied.

Positive character partitions2/2/3, object capacity2, floor1 with a2x2 map,
original16MiB pool dimensions and scripted RNG are controlled. `MAP_walkAble`
uses an explicit bounded-coordinate predicate. `CHAR_sendWatchEvent` is a
collector, not execution of notification traversal/networking.

Actual original map list allocation/add/remove executes, but detached-node
`freeMemory` is an explicit collector adapter. It verifies nonnull, distinct
detached node calls within a cycle and does not recycle pool blocks. Pool storage
is released through original `memEnd`. This does not validate original
`freeMemory`, free-list reuse, full map bootstrap or original LP64 ABI safety.

The independent Python oracle checks all five named initialized object fields,
all four cell-list contents/order, original owner-search results, character use
flags, raw initialized world object-work fields, watch/walk/reclamation counts,
nine ordered stages, and named birth identity/stats/HP/experience/ticket/start/
object work/RNG/sequence fields. It does not claim an independent oracle for all
birth fields or all object bytes. The original constructor leaves additional
Object fields/padding unspecified; they are neither read nor included in output
hashes. O0/O2 complete ordered named streams must match byte-for-byte.

## Validation and acceptance

Run the new unit regressions together with the nine predecessor gates. Execute:

```sh
python -m tools.stoneage_object_ownership_audit \
  --gavin-dir /tmp/pinned/gavin --iris-dir /tmp/pinned/iris \
  --bismarck-dir /tmp/pinned/bismarck
```

Expected49,024 cycles,98,048 preserved enemy births,147,072 successful world
constructors,49,024 full-object constructor rollbacks and441,216 named stage
comparisons across two profiles and O0/O2 GNU99 `-fgnu89-inline` with nonrecovering
UBSan. Ten compiling, safely executing semantic mutations must fail the oracle:
world object-work write, object-owner copy, detached map-node collection call,
owner search and enemy object-work, per profile. Mutation map reclamation checks
the adapter call, not the original reclaimer body. Nine predecessor complete
reports must reproduce unchanged. Acceptance requires exact-input Actions and
complete report comparison, followed by continuity/receipt write-back.

## Remaining priority

Execute actual battle entry and complete creation-to-Exit/destruction/reuse with
these actual storage/header domains. Preserve caller/type/lifetime distinctions;
do not substitute this bounded ownership result for that composition. Original
reclamation/bootstrap, Iris encoding, special/equipped/nonempty callbacks,
remaining actor/watcher/typed631/635 and original build/ABI/JSS/Taiwan-v1 stay OPEN.
Pressure remains2486=2465 closed capability+18 OPEN+3 historical UB;zero runtime
promotions. No engine/content transition or modern design change is implied.
