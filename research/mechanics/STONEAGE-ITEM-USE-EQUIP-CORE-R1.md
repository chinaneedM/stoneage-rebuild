# StoneAge Item Use / Equip Core R1

Status: **strong convergent descendant evidence; later equipment-slot and requirement extensions separated**  
Scope: ordinary item-use dispatch, five-slot equipment baseline, inventory/equipment movement, attach/detach callbacks and parameter recomputation.

## Why this seam matters

The project already has reconstructed item data, character parameters and battle behavior. What was missing was the execution bridge that answers:

- when does "use item" mean consume/execute a callback?
- when does it mean equip the item instead?
- how are equipment replacements performed?
- which callbacks run on attach/detach?
- when are derived character parameters recomputed?

The descendant source family is highly convergent on these behaviors.

## Evidence set

Fixed source revisions:

- **BismarckDD/stoneage** @ `999ffdf1d220ec6666eb65339180689c9caf1876`
  - `server/gmsv/include/char_base.h`
  - `server/gmsv/include/item.h`
  - `server/gmsv/char/char_item.c`
  - `server/common/gmsv_server_recv.c`
- **gavinlinasd/StoneAge** @ `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
  - corresponding `gmsv/src` files
- **iriselia/StoneAge** @ `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
  - corresponding `Source/gmsv` files

## Five-slot common equipment baseline

All three `CHAR_EquipPlace` enums begin:

```
CHAR_HEAD
CHAR_BODY
CHAR_ARM
CHAR_DECORATION1
CHAR_DECORATION2
```

Only after those entries do optional macros add later slots such as:

- belt;
- shield;
- shoes;
- glove.

Therefore R1 models the common old baseline as five equipment slots:

```
0 head
1 body
2 arm / weapon
3 decoration 1
4 decoration 2
```

The extension slots are not treated as launch-era facts.

## `CHAR_ItemUse`: use versus equip is type-driven

**FACT — convergent descendant code**

After validating the player/item and rejecting dead users, `CHAR_ItemUse` makes this split:

```c
if (ITEM_TYPE != ITEM_OTHER && ITEM_TYPE != ITEM_DISH) {
    equip item;
    return;
}

usefunc = ITEM_USEFUNC pointer;
if (usefunc) {
    usefunc(user, target, inventory_slot);
} else {
    "nothing happens";
}
```

This has an important reconstruction consequence:

> For ordinary equipment item types, `ITEM_USEFUNC` is not the main "on use" path. Pressing use routes into equipment placement.

Only `ITEM_OTHER` and `ITEM_DISH` proceed to the normal use-function callback path in this core.

Bismarck adds optional Lua routing before the ordinary function-pointer lookup; that is later extensibility rather than a change to the base type split.

## Use-action animation

Outside battle, when the target resolves to a player and the item has a nonnegative `ITEM_USEACTION`, the server emits that action on the target before the item-specific path proceeds.

This is presentation/event behavior, not the source of the actual item effect.

## Direct inventory/equipment movement during battle

The ordinary client move-item receiver rejects `CHAR_moveEquipItem` while `CHAR_WORKBATTLEMODE != NONE`.

Therefore **direct drag/move packets** cannot rearrange equipment/inventory during battle in the preserved branches.

This must not be over-generalized to "CHAR_ItemUse can never be called in battle": battle execution itself calls `CHAR_ItemUse` for battle item commands in the older branches. R1 therefore models only the direct-move packet restriction.

## Equipment placement

### Declared equipment slot

Before an item can enter an equipment slot, `ITEM_getEquipPlace` must resolve a valid declared slot.

For ordinary non-decoration items, the requested destination must equal that declared slot.

### Two decoration slots

Items declaring `CHAR_DECORATION1` may occupy either decoration slot 1 or 2.

However, when the other decoration slot is occupied by an item with the **same ITEM_TYPE**, the new item is rejected.

Thus the two accessory slots are not simply unrestricted duplicates.

`CHAR_ItemUse` contains automatic slot-selection logic that attempts to choose an appropriate decoration slot before calling the movement routine.

## Common level requirement

The three fixed branches preserve:

```c
if (TRANSMIGRATION <= 0) {
    if (ITEM_LEVEL > CHAR_LV)
        reject;
}
```

Thus an un-reborn character must meet the item level requirement.

Once `TRANSMIGRATION > 0`, this particular old level check is bypassed.

Later builds conditionally add requirements such as:

- strength;
- dexterity;
- transmigration count;
- profession;
- rookie-item restrictions;
- transformed-character ranged-weapon restrictions;
- mission/token ownership checks.

R1 does not flatten those conditional additions into the old common core.

## Bag -> equipment replacement

When a valid bag item is equipped into a slot:

1. the incoming bag item is written into the equipment slot;
2. any prior equipped item is written back into the source bag slot;
3. if an old equipped item existed, its detach event runs;
4. the incoming item's attach event runs;
5. the move notification is emitted.

Therefore replacement is a swap between the bag source slot and equipment destination, not deletion of the old equipment.

### Callback order

The stable replacement order is:

```
detach old equipment
attach new equipment
```

The callback functions are sourced from:

- `ITEM_DETACHFUNC`;
- `ITEM_ATTACHFUNC`.

This is distinct from `ITEM_USEFUNC`.

## Equipment -> bag

When moving equipped gear to an empty bag slot:

1. the item moves to the bag;
2. the equipment slot becomes empty;
3. the item's detach callback executes.

When the chosen bag slot is already occupied, the code does something less obvious:

```
CHAR_moveItemFromEquipToItemBox(...)
    -> CHAR_moveItemFromItemBoxToEquip(
           occupied_bag_slot,
           original_equipment_slot)
```

So the occupied bag item is attempted as a replacement for the equipped item.

If that bag item is valid for the equipment slot, the operation becomes an indirect exchange:

```
equipped A + bag B
  -> equipped B + bag A
  -> detach A
  -> attach B
```

If B cannot legally occupy that equipment slot, the exchange fails.

## Equipment -> equipment direct movement

The top-level movement routine does **not** directly move or swap one equipment slot to another equipment slot.

If both source and destination are equipment slots, it emits a rejection path.

Equipment replacement is therefore mediated through the bag/equip path, not arbitrary equipment-slot swapping.

## Bag -> bag

In the common baseline, bag-to-bag movement swaps the two item indices directly.

Later `_ITEM_PILENUMS` code may merge stackable identical item IDs before falling back to the ordinary swap. R1 keeps pile/stack semantics separate because they are macro-controlled extensions.

## Parameter recomputation

After an accepted top-level movement attempt reaches the movement branch, the server calls:

```c
CHAR_complianceParameter(character)
```

and refreshes the character's visible representation.

When an equipment change actually occurred, the player receives refreshed values including:

- HP / max HP;
- MP / max MP;
- attack;
- defense;
- quick;
- charm;
- luck;
- earth / water / fire / wind.

Older gavinlinasd/iriselia code also recomputes carried pets outside battle after equipment changes; Bismarck's fixed current path has diverged here. R1 therefore models the character parameter recomputation as the common invariant and leaves pet-propagation behavior versioned.

This is the key bridge from **equipped item data** into **derived character state**.

## Attach/detach are event hooks, not the whole stat system

`CHAR_sendItemAttachEvent` and `CHAR_sendItemDetachEvent`:

- emit equip/unequip messages;
- invoke the item's attach/detach callback if registered;
- may execute optional later feature cleanup such as metamorph/ride state.

But base equipment stat effects are also reflected through the subsequent parameter-compliance calculation.

Therefore reconstruction should preserve three separate layers:

1. static item fields/data;
2. attach/detach event callbacks;
3. global character parameter recomputation from current state/equipment.

## Deterministic model

Repository artifacts:

- `tools/stoneage_item_use_equip_model.py`
- `tests/test_stoneage_item_use_equip_model.py`
- `.github/workflows/validate-stoneage-item-use-equip.yml`

Regression coverage includes:

- five-slot old equipment baseline;
- OTHER/DISH callback routing versus equipment routing;
- dead/invalid use rejection;
- direct move packet battle restriction;
- old level requirement and rebirth bypass;
- declared equipment-slot enforcement;
- dual-decoration same-type restriction;
- automatic decoration slot choice;
- bag->equip displacement;
- detach-before-attach event order;
- equip->empty-bag detach;
- equip->occupied-bag recursive replacement;
- bag->bag swapping;
- direct equip->equip rejection.

## Evidence status

- **FACT:** all three lineages share the five old equipment slots before optional extension slots.
- **FACT:** ordinary equipment types route `CHAR_ItemUse` into equip logic and return before `ITEM_USEFUNC`.
- **FACT:** only OTHER/DISH reach the ordinary use callback branch in this core.
- **FACT:** direct client inventory/equipment movement is rejected during battle.
- **FACT:** un-reborn characters are blocked when ITEM_LEVEL exceeds character level; that specific check is bypassed after transmigration.
- **FACT:** non-decoration items must match their declared equipment slot.
- **FACT:** the two decoration slots reject two items of the same ITEM_TYPE.
- **FACT:** replacement runs detach(old) before attach(new).
- **FACT:** direct equipment-slot -> equipment-slot movement is rejected.
- **FACT:** equipment changes feed into character parameter recomputation.
- **OPEN:** exact launch-era presence/absence of optional stack, extra equipment-slot, profession/stat-requirement and Lua layers.
- **OPEN:** exact historical item-data population for attach/detach/use callbacks by commercial version.

## Next technical seam

With item execution now connected to character state, the next high-value deterministic seam is **healing/recovery service semantics**. That will close the ordinary loop from battle damage/death/status -> service NPC/payment -> restored character/pet state, after which trading/economy transfer can be reconstructed on top of the now-explicit inventory and item state model.
