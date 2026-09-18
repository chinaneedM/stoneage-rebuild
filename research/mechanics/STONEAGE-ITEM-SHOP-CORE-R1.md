# StoneAge NPC Item Shop Core R1

Status: **strong convergent descendant evidence; concrete NPC inventories/rates and later manor/tax extensions remain version-data**  
Scope: ordinary `npc_itemshop.c` purchase/sale semantics, not player stalls, auctions, pool shops or simple-shop variants.

## Purpose

Direct trade now explains player-to-player asset transfer. The ordinary item shop closes the other basic economy path:

```
ITEM table cost
  -> NPC buy/sell configuration
  -> player inventory capacity
  -> carried STONE
  -> item instance creation/deletion
```

The source exposes several behaviors that should not be normalized into modern assumptions:

- requested purchase quantity is silently reduced to the number of empty inventory slots;
- newly purchased units are created as individual item instances through the empty-slot allocator;
- purchase gold is deducted only **after** all item creation/insertion calls finish;
- player-sale eligibility is a whitelist, not "every item can be sold";
- the sale rate is NPC configuration, not a universal 20%;
- a special sale entry defaults to 1.2× when `special_rate` is absent;
- a sale that would make carried gold exactly equal to the max is rejected because the source uses `>=`.

## Evidence set

Fixed source revisions:

- **BismarckDD/stoneage** @ `999ffdf1d220ec6666eb65339180689c9caf1876`
  - `server/gmsv/npc/npc_itemshop.c`
  - `server/gmsv/npc/npc_eventaction.c`
  - `server/gmsv/char/char_item.c`
  - `server/gmsv/include/version.h`
- **gavinlinasd/StoneAge** @ `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
  - corresponding `gmsv/src` files
- **iriselia/StoneAge** @ `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
  - corresponding `Source/gmsv` files

## Shop configuration is data-driven

The ordinary shop reads NPC arguments including:

- `ItemList`;
- `buy_rate`;
- `LimitItemType`;
- `LimitItemNo`;
- `sell_rate`;
- `special_item`;
- `special_rate`;
- messages/UI strings.

Later branches add manor-law/fame/changed-price/tax configuration. R1 separates those additions from the common price/inventory transition.

Therefore this model does not invent one global buy price or sell ratio. Concrete commercial NPC configurations belong in the recovered NPC-data layer.

## Shop inventory selection

`ItemList` accepts:

- individual item IDs;
- inclusive ranges such as `15-25`.

Only item IDs that resolve to an item-table cost/name participate in the buy list.

The user-facing selected row is later resolved back through this configured list before purchase.

R1 assumes normal ascending configured ranges. The old parser contains slightly different ordering of range normalization between listing and selection code for reversed ranges; reversed-range behavior should be treated as a configuration edge case rather than canonical content.

## Buy price

The old common path uses:

```
unit_cost = ITEM table cost
unit_price = int(unit_cost * buy_rate)
```

If `buy_rate` is absent, the local default is `1.0`.

The cast occurs after multiplication, so fractional results are truncated toward zero for normal nonnegative prices.

Bismarck and the later manor-law branches can override the base item cost and add fame/tax rules. Those are versioned extensions.

## Purchase quantity is capped by empty slots

`NPC_SetNewItem`:

1. parses selected item and requested quantity;
2. rejects quantity <= 0;
3. counts currently empty carried-item slots;
4. if requested quantity exceeds empty-slot count, replaces it with the empty-slot count;
5. rejects when there are zero empty slots;
6. only then resolves the selected shop item and enters the buy transaction.

This is a **silent server-side clamp**, not merely a client display rule.

### No automatic merge in the insertion helper

`CHAR_addItemSpecificItemIndex`:

- calls `CHAR_findEmptyItemBox`;
- inserts the concrete item instance into that empty slot;
- does not search existing stacks or merge quantities.

Thus this shop buy path's empty-slot count corresponds to real insertion behavior even when later builds carry `_ITEM_PILENUMS`.

One requested unit creates one item instance in this path.

## Purchase money check and mutation order

`NPC_AddItemBuy` computes:

```
total = unit_price * quantity
```

and rejects when:

```
current_gold < total
```

If affordable, it then loops quantity times:

```
ITEM_makeItemAndRegist(itemID)
CHAR_addItemSpecificItemIndex(player, item)
send item update
```

Only **after every loop iteration succeeds** does it call:

```
CHAR_DelGold(player, total)
```

Therefore the executed order is:

```
check total gold
 -> create/add item 1
 -> create/add item 2
 -> ...
 -> create/add item N
 -> deduct total STONE
```

### Not rollback-atomic

There is no transaction snapshot around this sequence.

If an unexpected allocation/registration failure occurs after earlier units have already been inserted:

- the function returns FALSE;
- previously inserted units are not rolled back;
- total gold has not yet been deducted.

Normal inventory-full failure is largely prevented by the prior empty-slot clamp, but allocator/object failures can still expose the ordering.

A modern rebuild may intentionally make this transaction atomic while preserving visible successful behavior, but that would be an engineering improvement.

## What the shop will buy from a player

The ordinary sale code uses `LimitItemType` and `LimitItemNo` as a **whitelist**.

An inventory item is eligible if it matches at least one configured:

- allowed item type label;
- allowed item ID;
- allowed inclusive item-ID range.

The type table also supports grouped labels:

- `ACCESSORY` -> types 8..15;
- `OFFENCE` -> types 0..4 and 17..19;
- `DEFENCE` -> types 5..7.

If an actual sale request does not match the limit whitelist, `NPC_GetLimtItemList` returns `-1` for that request.

Thus absence of a whitelist does not mean "buy everything."

## Ordinary sell price

For an eligible ordinary item:

```
sell_price = int(ITEM_COST * sell_rate)
```

But `sell_rate` must actually be present in the NPC arguments for the ordinary branch to return a price.

The local variable is initialized to `0.2`, yet if neither special pricing nor a configured `sell_rate` branch executes, the function returns its initial `cost = -1`.

Therefore R1 does **not** call 20% a universal fallback resale ratio.

## Special resale pricing

If the item ID matches `special_item`:

- configured `special_rate` is used when present;
- if `special_rate` is absent, the source sets the rate to **1.2**.

This special path is checked before ordinary `sell_rate`.

Therefore a special item can have a resale value above its base ITEM_COST by default.

## Sale stack quantity

In fixed gavinlinasd/iriselia and Bismarck, `_ITEM_PILENUMS` is enabled.

The sale request can include a quantity from the selected item stack.

`NPC_DelItem`:

- rejects an invalid item;
- rejects when stack quantity < requested sale quantity;
- subtracts the requested count;
- deletes the item instance if the remainder is <= 0;
- otherwise writes the reduced stack count.

Gold is added only after `NPC_DelItem` succeeds.

## Gold-cap boundary

Before deleting the item, `NPC_SellNewItem` rejects when:

```
(cost * sell_quantity) + current_gold >= max_gold
```

The comparison is **greater-than-or-equal**.

Consequences:

- projected gold below max -> allowed;
- projected gold exactly max -> rejected;
- projected gold above max -> rejected.

This differs from the direct-trade preflight, which effectively allows a final balance equal to the maximum.

R1 preserves this subsystem-specific boundary.

## Sale mutation order

After whitelist/price/item/gold-cap validation:

```
delete or decrement item
 -> add sale proceeds to player gold
 -> refresh gold status
```

This is a simpler destructive sequence than direct trade. The gold-cap check occurs first, and the item-delete helper must succeed before gold is added.

There is still no general rollback transaction, but the post-delete operation is a direct gold increment whose capacity has already been checked.

## Later extensions kept separate

The fixed source family contains later features including:

- `_NEW_MANOR_LAW` fame requirements and per-item changed cost;
- family/manor tax;
- larger Bismarck inventories;
- `_NPC_SHOPALTER01` alternate graphical-shop protocol;
- express/delivery shop modes;
- security locks;
- expanded item-type tables.

gavinlinasd/iriselia fixed configs enable `_NEW_MANOR_LAW` and `_ITEM_PILENUMS`, while their `_NPC_SHOPALTER01` and family-tax defines are commented out. Bismarck enables new inventory and pile-number support and has later manor/fame behavior integrated in its current file.

R1 isolates the convergent buy/sell core and treats these additions as version/config layers.

## Deterministic model

Repository artifacts:

- `tools/stoneage_item_shop_model.py`
- `tests/test_stoneage_item_shop_model.py`
- `.github/workflows/validate-stoneage-item-shop.yml`

Regression coverage checks:

- buy-rate truncation;
- optional cost override ordering;
- server-side quantity clamp to empty slots;
- total-gold precheck;
- item-create/insert-before-gold-deduction ordering;
- no rollback after injected mid-purchase failure;
- type/ID/range sale whitelisting;
- grouped ACCESSORY/OFFENCE/DEFENCE categories;
- ordinary configured sell-rate requirement;
- special-item 1.2 fallback;
- strict `projected_gold < max_gold` sale boundary;
- partial/full stack deletion;
- delete-item-before-add-gold ordering.

## Evidence status

- **FACT:** all three lineages use ITEM_COST × configured buy rate with integer truncation for the ordinary buy price.
- **FACT:** requested buy quantity is capped to current empty carried-item slots.
- **FACT:** the concrete insertion helper uses an empty slot and does not merge existing stacks.
- **FACT:** total affordability is checked before creation, but gold is deducted only after all requested items have been created/inserted.
- **FACT:** no rollback transaction surrounds the buy loop.
- **FACT:** player sales require the item to match configured LimitItemType/LimitItemNo eligibility.
- **FACT:** ordinary sale price uses configured sell_rate; 0.2 is not an unconditional fallback.
- **FACT:** a matched special_item defaults to 1.2× ITEM_COST when special_rate is absent.
- **FACT:** stack sale quantity cannot exceed the selected stack count.
- **FACT:** a sale is rejected when projected carried gold is equal to or above the maximum.
- **FACT:** sale mutation deletes/decrements the item before adding proceeds.
- **OPEN:** exact buy/sell rates, item inventories and whitelists for each historical commercial shop NPC.
- **OPEN:** launch-era shop data and whether every later helper existed in the 1999/early-1.x server.
- **OPEN:** chronology of pile-number, manor/fame/tax and alternate-shop protocol additions.

## Next technical seam

The ordinary item economy now closes NPC purchase and resale. The next highest-value deterministic gap should be chosen between **pet storage/pet shop** and **save/logout persistence boundaries**. Pet storage would close the five-carried-pet roster lifecycle; persistence would establish which reconstructed runtime states survive logout/reconnect. Re-audit both before selecting the next seam.
