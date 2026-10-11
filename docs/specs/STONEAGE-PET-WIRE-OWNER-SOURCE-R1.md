# Optional PET equipment protocol wire -> actor slot -> unique hook (source only) R1

## Evidence status and provenance

**SOURCE_ONLY_OPTIONAL_PET_WIRE_OWNER_CHAIN**: late Bismarck descendant `BismarckDD/Stoneage` commit `999ffdf1d220ec6666eb65339180689c9caf1876`. No evidence of a deployed feature-enabled client/server binary pair, no demonstrated live UI request, and no historical proof about JSS1999/Taiwan1.0.

The reproducible source-free audit `tools/stoneage_pet_wire_owner_source_audit.py` re-fetches a pinned checkout transiently, verifies nine original Git blob IDs, and checks a strict sequence and predicate matrix without committing any original proprietary source or assets. Test harness `tests/test_stoneage_pet_wire_owner_source.py` rejects inflated runtime claims. Report: `research/recovered/STONEAGE-PET-WIRE-OWNER-SOURCE-R1.txt`; receipt: `research/recovered/STONEAGE-PET-WIRE-OWNER-ACCEPTANCE-R1.json`.

Pinned inputs:

| Original pinned file | Git blob |
|---|---|
| `client/stoneage/system/menu.cpp` | `62754fdd0db1b84c358d61418d253012d149e1d4` |
| `client/stoneage/proto/protocol.cpp` | `17f1900d8845c15308a4b429905ec009e5fd4c0f` |
| `client/stoneage/proto/protocol.h` | `bb70087ef1b1915748da23935584eda2c8178cb0` |
| `server/common/gmsv_server.h` | `708fe1b9f73be4952677fda474f10e86d9a56306` |
| `server/common/gmsv_server_send.c` | `84dd1b2d9fbac10fe39983e6b8984aaebf1b3075` |
| `server/common/gmsv_server_recv.c` | `088db5e38a1bc0dd47b3c3120480af93ab24c4c7` |
| `server/gmsv/char/char_item.c` | `970b7b3f975965c6c5e77352a2e0382adf943753` |
| `server/gmsv/char/char_base.c` | `5f646eba671b39f5e90f53e3a95cbcc70ff56975` |
| `server/gmsv/include/version.h` | `b3fc0c80705973bc8d088287c98a5d66171bb6c2` |

## Bounded source findings

1. Client UI contains three `_PET_ITEM`-guarded calls in `menu.cpp` at lines **14824** (drag/drop: destination slot), **14966** (double-click: destination **-1**, automatic slot resolution), and **15333** (drag outside: destination **-2**). This is actual late *source placement*, not an executed packet.
2. Client sender `lssproto_PetItemEquip_send` encodes **five ordered integer arguments**: player X, player Y, selected pet number, source item slot, destination slot, followed by the **additive checksum**. Conditional client opcode is **127**.
3. Server conditional PET decoder for opcode **127** reads the corresponding five integers from positions 2–6, the checksum at 7, checks equality, and only then calls `GmsvServer_PETITEM_recv` before discarding the decoded message. This is a static serializer/decoder field-order match, not a wire-capture proof.
4. Callback source resolves the active character via `CONNECT_getCharaindex(fd)`, performs `CHECKFDANDTIME`, rejects incompatible trade/battle modes, and conditionally enforces item lock before dispatching to `CHAR_movePetItem`. Positional x/y arguments appear in callback signature but do not independently establish player-location verification in this function; do **not** infer that such validation occurred.
5. Native `CHAR_movePetItem` validates the player and alive state, resolves the selected pet via `CHAR_getCharPet`, distinguishes destination `-1` (item-type-derived equipment slot), `-2` (drop path; worn pet item rejected), and ordinary item index exchanges. It applies tameness/type/level restrictions and calls **four distinct `CHAR_setItemIndex` statements** representing the two directions of player ↔ pet slot exchange. Follow-up item/pet updates and parameter recalculation are present. Four source statements are not four mutations per request.
6. The original `_CHAR_setItemIndex` body stores a **physical global item index** in an actor's slot array and, behind `_UNIQUE_P_I`, optionally calls `ITEM_setItemUniCode`. The latter source function generates a new code only when its code-string test matches *empty* or contains an underscore. That conditional hook is **not** evidence that every exchange changes the unique code, nor that the persistent object owner, pre/post release identity, or naturally reachable PET aliases have been executed.

## Strict limitations

- **FACT** is restricted to the nine pinned late-source blobs and ordered original source statements.
- **HYPOTHESIS/OPEN:** Whether the original checked-in optional 8.0 client and server can be jointly built, packaged, connected, and driven through the real UI to a persistent PET owner/item lifecycle; whether index reuse can occur naturally after genuine slot movement; whether unique identity changes over save/load.
- **NOT PROVEN:** Deployment flags, opcode127 packet captured over an actual connection, original native executable behavior, binary equivalence, default v2.5 enablement, JSS1999 or Taiwan1.0 feature membership.
- **DESIGN:** The modern rebuild does not inherit native global index aliasing or enable post-v1 pet-equipment features without an independent documented product decision.

Historical pressure remains **2486 = 2465 bounded closed + 18 OPEN + 3 historical UB**, with zero early-version promotions. Higher-priority next work: actual paired enabled 8.0 client/server executable validation or binary provenance, followed only then by non-synthetic owner/unique identity lifecycle testing. If no verified enabled pair can be recovered, mark runtime reachability **OPEN**, not FACT.
