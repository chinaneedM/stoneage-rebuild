# StoneAge Ordinary Item / Pet Pool Storage R1

Status: **fixed-descendant deterministic reconstruction; original 1999 chronology remains open**
Scope: ordinary character-embedded item/pet pools, pet-shop deposit/withdraw transitions, pool capacity, persistence boundary, and separation from later account-shared Depot warehouses.

## Evidence controls

Fixed source revisions:

- `gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
- `iriselia/StoneAge@9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
- `BismarckDD/stoneage@999ffdf1d220ec6666eb65339180689c9caf1876`

Primary files:

- `gmsv/src/npc/npc_petshop.c` and fixed equivalents;
- `gmsv/src/npc/npc_poolitemshop.c` and fixed equivalents;
- `gmsv/src/char/char_base.c` and fixed equivalents;
- `gmsv/src/include/char_base.h` and fixed equivalents;
- version headers for optional Depot feature boundaries.

The fixed descendants are later than the target launch era. This report reconstructs their deterministic mechanics without promoting them to 1999/JSS historical fact.

## Critical terminology correction: Pool != Depot

Two storage layers coexist in the preserved code and must not be conflated.

### Ordinary Pool storage

The character object owns fixed arrays:

- `indexOfExistPoolItems[CHAR_MAXPOOLITEMHAVE]`;
- `indexOfPoolPet[CHAR_MAXPOOLPETHAVE]`.

These arrays are present without the later `_CHAR_POOLITEM` / `_CHAR_POOLPET` Depot guards.

The core character serializer writes them directly as:

- `poolitemN=...`;
- `poolpetN=...`.

The normal character parser reconstructs them directly on login.

Therefore, in the inspected fixed descendants:

> ordinary Pool items and Pool pets are part of the character's own save payload.

### Later shared Depot warehouse

Separate pointers and persistence functions are guarded by later feature macros such as:

- `_CHAR_POOLITEM` / `_NPC_DEPOTITEM`;
- `_CHAR_POOLPET` / `_NPC_DEPOTPET`.

Those use separate `DepotitemN` / `DepotpetN` representations and separate SAAC get/save messages. The preserved version annotations identify the shared pet warehouse as a later extension.

Therefore:

- ordinary **Pool** = character-inline storage;
- later **Depot** = separate account/shared warehouse path.

The earlier save/logout report has been corrected to preserve this distinction.

## Ordinary capacities

### Carried pets

The fixed character limit is:

```
CHAR_MAXPETHAVE = 5
```

### Pet Pool

The usable ordinary Pool prefix is:

```
5 + 2 * transmigration
```

clamped to `CHAR_MAXPOOLPETHAVE`.

In the ordinary fixed configuration inspected here, `CHAR_MAXPOOLPETHAVE = 10`; a later compile-time branch can raise it.

### Item Pool

The usable ordinary Pool prefix is:

```
10 + 4 * transmigration
```

clamped to `CHAR_MAXPOOLITEMHAVE`.

In the ordinary fixed configuration inspected here, `CHAR_MAXPOOLITEMHAVE = 20`; later compile-time branches can raise it.

This is a gameplay-visible capacity rule in these descendants, but exact launch-era availability remains OPEN.

## Pet-shop Pool activation

The pet shop reads `pool_flg`.

When disabled, the ordinary menu does not expose pet deposit/withdraw.

When enabled, the ordinary path includes:

- deposit a carried pet into Pool;
- withdraw a Pool pet into a carried slot;
- sell a carried pet.

Later shared Depot access may add another menu branch, but that is not part of the ordinary Pool state.

## Pet deposit

The inspected ordinary deposit flow uses:

```
cost = 50 + player_level * 4
```

The window handler checks that:

- Pool service is enabled;
- the player has enough current gold.

The transfer function then:

1. resolves the selected carried pet;
2. rejects the currently ridden pet in the fixed source;
3. finds the first empty Pool slot within the transmigration-dependent capacity;
4. if the deposited pet is the default battle pet, clears `CHAR_DEFAULTPET`;
5. places the same runtime pet object/index into the Pool slot;
6. clears the carried pet slot;
7. deducts the Pool cost;
8. sends state/status updates and logs the transfer.

This is a move, not a clone.

## Pet withdrawal

Withdrawal:

1. resolves the selected Pool pet;
2. finds the first empty carried-pet slot;
3. moves the same pet object/index to that carried slot;
4. clears the selected Pool slot;
5. compacts remaining Pool pets toward the front;
6. sends state/status updates and logs the transfer.

No ordinary withdrawal fee is observed in this path.

Later guardian/family/fusion branches can modify pet state on withdrawal. Those branches are versioned and are not promoted into the ordinary R1 rule set.

## Item Pool deposit

The Pool item shop has a configurable `cost`; absent configuration, the fixed default is:

```
200
```

The ordinary UI identifies items as non-poolable when any are true:

- `ITEM_DROPATLOGOUT`;
- `ITEM_VANISHATDROP`;
- `!ITEM_CANPETMAIL`.

However, the authoritative ordinary transfer function `NPC_PoolItemShop_PoolItem` does **not** repeat that item-property validation.

Its core transition is:

1. find the first empty Pool item slot inside the transmigration-dependent usable prefix;
2. validate that the selected carried item object exists;
3. call `CHAR_DelGold(cost)`;
4. move the item index into the Pool slot;
5. clear the carried slot;
6. send status updates and log the transfer.

### Historical server-side payment weakness

`CHAR_DelGold` returns 0 without changing gold when the player lacks enough currency.

The ordinary Pool item handler ignores that return value.

Therefore the fixed source admits this state transition at the handler level:

```
insufficient gold
 -> debit fails
 -> item still moves into Pool
```

This is documented as a source defect, not a desired gameplay rule.

Likewise, because the item-property restriction is only represented in the normal UI construction and is not rechecked in this transfer function, the server-side handler is weaker than the client-facing flow.

The reconstruction records this behavior to understand the original architecture. A modern rebuild should validate permissions and payment transactionally on the authoritative side.

## Item Pool withdrawal

Withdrawal:

1. requires an empty carried inventory slot;
2. resolves the selected Pool item;
3. moves the item to the first empty carried slot;
4. clears the selected Pool slot;
5. compacts remaining Pool items toward the front;
6. updates client state and logs the transfer.

No withdrawal fee is observed.

## Why later Depot code is useful comparative evidence

The later shared Depot item path is stricter than the ordinary Pool handler:

- it rechecks the item restrictions server-side;
- it checks the return value of `CHAR_DelGold`;
- it refuses the transfer if payment fails.

That contrast is strong evidence that the ordinary Pool weakness is real implementation behavior rather than merely a misunderstanding of `CHAR_DelGold`.

The later fix must still remain versioned; it is not back-projected into the ordinary Pool implementation.

## Persistence closure

The save/logout reconstruction now joins directly to these storage transitions.

Ordinary Pool items and pets:

```
carried
  <-> ordinary Pool
  -> CHAR_makeStringFromCharData
  -> poolitemN / poolpetN
  -> SAAC character save
  -> login parser
  -> reconstructed Pool state
```

Later Depot storage uses a separate persistence channel.

This closes the fixed-descendant ordinary storage loop at the state-model level.

## Deterministic artifacts

- `tools/stoneage_pool_storage_model.py`
- `tests/test_stoneage_pool_storage_model.py`
- `.github/workflows/validate-stoneage-pool-storage.yml`

Regression coverage includes:

- pet Pool capacity growth and cap;
- item Pool capacity growth and cap;
- level-scaled pet deposit cost;
- pet move semantics;
- default-pet clearing;
- ridden-pet rejection;
- insufficient-gold pet-deposit rejection at the window path;
- locked Pool-prefix capacity behavior;
- pet withdrawal and Pool compaction;
- item UI restriction classification;
- ordinary item handler's ignored debit failure;
- absence of server-side item-restriction recheck in the ordinary transfer primitive;
- item withdrawal and compaction;
- later Depot server-side restriction/payment checks;
- persistence-domain separation between ordinary Pool and later Depot.

## Evidence status

- **FACT:** ordinary Pool item and pet arrays are embedded in the fixed character object.
- **FACT:** ordinary `poolitemN` and `poolpetN` are serialized/deserialized in the fixed core character save.
- **FACT:** fixed pet Pool usable capacity is `5 + 2 * transmigration`, capped by compiled maximum.
- **FACT:** fixed item Pool usable capacity is `10 + 4 * transmigration`, capped by compiled maximum.
- **FACT:** carried pet capacity is five in the inspected ordinary configuration.
- **FACT:** pet Pool deposit cost is `50 + player level * 4`.
- **FACT:** ordinary pet deposit moves one carried pet into the first usable empty Pool slot and can clear the default-pet selection.
- **FACT:** fixed source rejects depositing the currently ridden pet.
- **FACT:** pet withdrawal moves into the first empty carried slot and compacts Pool storage.
- **FACT:** ordinary Pool item shop defaults its deposit cost to 200 when no cost is configured.
- **FACT:** ordinary item UI marks DROPATLOGOUT / VANISHATDROP / !CANPETMAIL items as unavailable.
- **FACT:** ordinary item transfer primitive does not recheck those flags.
- **FACT:** ordinary item transfer primitive ignores failed `CHAR_DelGold` and can still complete the move.
- **FACT:** item withdrawal has no observed fee and compacts Pool storage.
- **VERSIONED:** later account-shared Depot item/pet warehouses and their separate persistence channels.
- **VERSIONED:** later guardian/riding/fusion/shared-warehouse extensions surrounding these functions.
- **OPEN:** whether and in what exact form ordinary Pool storage existed in the 1999/JSS baseline.
- **OPEN:** exact commercial-version capacity chronology before the fixed descendants.
- **OPEN:** original operator content configuration for which pet shops enabled `pool_flg` and which Pool-item shops overrode the default cost.

## Next seam

With ordinary character storage connected to persistence, the next highest-priority deterministic world-state gap is:

**field warp / portal / map-transition authority**

The next pass should reconstruct destination resolution, trigger authority, party propagation, invalid-destination handling, and interactions with non-resumable/no-exit maps before moving on to the full NPC/world-content graph.
