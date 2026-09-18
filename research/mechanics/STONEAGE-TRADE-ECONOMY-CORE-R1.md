# StoneAge Direct Trade / Economy Transfer Core R1

Status: **strong descendant evidence; request/lock protocol and several restrictions are versioned**  
Scope: direct player-to-player trade, not market stalls. Covers eligibility, offer freezing, structured item/pet/gold offers, preflight capacity, transfer order, cancellation and version differences.

## Why this seam matters

The repository now models carried gold, item inventory/equipment and pet rosters. Direct trade is the mechanism that transfers those three asset classes between players.

The source also corrects an easy modern assumption: this is **not a rollback-backed atomic transaction**. It is a preflight-validated sequence of destructive mutations. Reconstruction must preserve that distinction.

## Evidence set

Fixed revisions:

- **BismarckDD/stoneage** @ `999ffdf1d220ec6666eb65339180689c9caf1876`
  - `server/gmsv/char/trade.c`
  - `server/gmsv/include/char_base.h`
  - `server/gmsv/include/version.h`
- **gavinlinasd/StoneAge** @ `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
  - corresponding `gmsv/src` files
- **iriselia/StoneAge** @ `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
  - corresponding `Source/gmsv` files

The preserved comments date the player-trade implementation to CoolFish 2001-04-18/19. Therefore this note does **not** claim direct trade existed in the 1999 launch build.

## Trade modes

All three lineages share:

```
CHAR_TRADE_FREE    = 0
CHAR_TRADE_SENDING = 1
CHAR_TRADE_TRADING = 2
CHAR_TRADE_LOCK    = 3
```

The enum retains SENDING, but in the fixed active paths the assignment to SENDING is commented out. With the ordinary request-confirm macro disabled, a valid trade search transitions both players directly into TRADING.

SENDING should therefore be preserved as historical/protocol state, not assumed to be exercised by every configuration.

## Starting a direct trade

The initiator search rejects ordinary starts when the initiator is:

- already TRADING or LOCK;
- in a party;
- in battle.

The server examines the tile one step in front of the initiator.

A candidate must be:

- a player;
- not self;
- not in battle;
- not in a party;
- configured to accept trades through `CHAR_ISTRADE`;
- currently `CHAR_TRADE_FREE`;
- backed by a live connection.

If exactly one eligible player is found, both sides enter TRADING, their per-connection confirmation flags are reset FALSE and the trade visual state is enabled.

Multiple eligible players on the target tile are rejected as ambiguous.

Later street-vendor/security-lock restrictions are configuration-specific additions.

## Trade protocol versions

### Structured/newer path in gavinlinasd / iriselia

Their fixed `version.h` enables both:

- `_ITEM_PILEFORTRADE`;
- `_TRADESYSTEM2`.

The server allocates a two-side `TradeList` record containing per side:

- up to 15 item source slots and offered quantities;
- up to 5 pet source slots;
- one gold amount;
- character/fd identity.

The record is bound to both connection descriptors and later used to re-resolve the counterparty.

### Bismarck fixed server configuration

Bismarck retains both code paths but its fixed server `version.h` does not define those two macros. Its active path therefore remains closer to the older message-buffer protocol.

R1 models the shared transaction semantics and explicitly versions the lock choreography. The 15-item structured-list capacity is **not** asserted as a launch-era universal.

## Offer changes and confirmation freeze

Item, pet and gold handlers all reject changes if either condition is true for that sender:

- sender is not in TRADING;
- sender's connection confirmation flag is already TRUE.

Therefore confirmation freezes **that side's own offer**. The other side may still edit until it independently confirms.

This is a real server invariant, not only a client UI behavior.

## Gold offer

The source parses a nonnegative amount and rejects it if it exceeds the player's current carried gold at offer time.

In the structured path, setting gold replaces that side's stored offer amount; it is not cumulative.

Maximum final carried gold is resolved through `CHAR_getMaxHaveGold`, so R1 keeps max-gold as a state/config input instead of hardcoding the UI message's "one million" wording.

## Item offers

In the structured path:

- offered source slot must be in the carried-item range;
- item must still exist;
- `ITEM_VANISHATDROP == 1` is rejected;
- up to 15 offer entries are stored;
- stackable items can increase the quantity associated with an already-offered source slot, limited by both the character and item pile limits.

Bismarck adds later `FreeTradeItem` and binding restrictions. Those are not common old-core facts.

## Pet offers

Structured pet offers:

- reference one of five carried-pet slots;
- require the pet still to exist;
- reject duplicate offered pet slots;
- reject family guardian pets (`CHAR_PETFAMILY == 1`);
- are limited to five entries.

The older gavinlinasd/iriselia care-level rule is:

```
if receiver is not PickAllPet
and receiver is un-reborn:
    reject when pet level > receiver level + 5
```

Bismarck's later fixed code changes this trade-specific delta to **+20** and adds additional free-trade/binding checks.

R1 therefore exposes the level delta as a version parameter and uses +5 for the older two-lineage rule.

## Confirmation and final lock

There are two preserved choreographies.

### `_TRADESYSTEM2` path

With both sides in TRADING:

1. each side sends confirmation; its `CONNECT_confirm` becomes TRUE;
2. once confirmed, that side can no longer edit its offer;
3. after **both confirmation flags are TRUE**, each side separately performs the final lock action;
4. first lock changes that player to `CHAR_TRADE_LOCK` and returns because the counterparty is not yet LOCK;
5. second lock changes the second player to LOCK;
6. because the counterparty is now also LOCK, the server enters `TRADE_SwapItem`.

Thus this path is effectively:

```
edit
 -> confirm/freeze A
 -> confirm/freeze B
 -> lock A
 -> lock B
 -> preflight + exchange
```

### Older/simplified path

Bismarck's current non-`_TRADESYSTEM2` case allows the lock action itself to set a missing confirmation. Once both confirmation flags are TRUE, the next lock sets the sender to LOCK and immediately invokes swap without requiring the other character mode to already be LOCK.

The state enum is shared; the final UI/protocol choreography is not.

## Cancellation

Trade close/cancel:

- notifies the other side when reachable;
- returns participant trade modes to FREE;
- clears temporary trade message/list state;
- clears confirmation flags;
- removes the trade visual effect;
- refreshes inventory/pet status.

The structured trade-list record is reset after cancellation.

There is no asset transfer merely from placing something in the trade window; ownership changes only at swap execution.

## Structured preflight

Before destructive transfer, `TRADE_CheckTradeList` validates projected capacity.

### Item slots

For each player:

```
available_after_outgoing =
    current_empty_inventory_slots
    + count(outgoing stacks offered in full)
```

A partially offered stack does not free its original slot.

For each incoming offer entry, required slots are computed against the receiver's maximum pile size.

The source literally uses:

```c
if (quantity > maxPile)
    needs += quantity / maxPile + 1;
else
    needs += 1;
```

This has a preserved off-by-one property:

- quantity 10, maxPile 10 -> 1 slot;
- quantity 11, maxPile 10 -> 2 slots;
- quantity 20, maxPile 10 -> **3 slots**, even though two physical stacks could suffice.

R1 mirrors the source check rather than "fixing" it.

The preflight also conservatively counts incoming entries rather than proving they can merge into compatible existing partial stacks.

### Pet slots

Projected pet capacity is:

```
current empty pet slots + outgoing offered pets
```

Incoming pet count must fit that projected capacity.

### Gold capacity

For player A receiving B's gold:

```
room_after_A_outgoing =
    max_gold - current_gold + A_offer_gold

require:
    room_after_A_outgoing >= B_offer_gold
```

The symmetric check is applied to B.

This is equivalent to checking projected final carried gold against the cap, assuming offered amounts remain available.

## Execution order

After successful preflight, the structured path performs:

```
remove A items
remove B items
remove A pets
remove B pets
subtract A gold
subtract B gold
add B items to A
add A items to B
add B pets to A
add A pets to B
add B gold to A
add A gold to B
```

Pet additions update:

- `CHAR_WORKPLAYERINDEX`;
- owner account/CD key;
- owner character name;
- pet compliance parameters.

The first available pet slot is used.

## Not transactionally atomic

This is the most important implementation caveat.

There is no rollback journal or transactional snapshot around the mutation sequence.

Several helper calls can return failure **after prior mutations have already occurred**. Examples include:

- item deletion/split allocation failure after an earlier offered item was removed;
- pet addition failure after items/gold have already been removed;
- other unexpected state changes between preflight and mutation.

The design relies on:

1. freezing offers after confirmation;
2. blocking many unrelated actions during trade;
3. validating projected capacity before mutation;

to make failures unlikely.

That is **preflight-guarded mutation**, not strong atomic commit.

A modern reconstruction can later improve this by applying the same visible rules through a true transaction/snapshot layer, but that would be an intentional engineering improvement, not a statement about the old server.

## Stack transfer behavior

When only part of a stack is transferred, the structured path:

- decrements the original source stack;
- creates a new item instance from the same ITEM_ID;
- assigns the transferred quantity;
- may split again according to the receiver's maximum pile limit.

This is another reason the data model should distinguish a concrete item instance from an item template/ID.

## Evidence status

- **FACT:** three lineages share FREE/SENDING/TRADING/LOCK trade modes.
- **FACT:** ordinary direct trade requires standalone, non-battle players and an enabled/free target directly in front.
- **FACT:** active fixed paths normally enter TRADING directly; SENDING is dormant unless the optional request-confirm path is enabled.
- **FACT:** once a side confirms, its item/pet/gold offer handlers reject further edits.
- **FACT:** direct trade supports items, pets and carried gold.
- **FACT:** structured trade preflights item slots, pet slots and final gold capacity before destructive transfer.
- **FACT:** outgoing full item stacks and outgoing pets are counted as space that will be freed.
- **FACT:** the item-slot preflight has the exact-multiple over-count behavior described above.
- **FACT:** execution removes both sides' offered assets before adding incoming assets.
- **FACT:** no general rollback transaction surrounds the mutation sequence.
- **FACT:** transferred pets receive the new owner identity and are parameter-recomputed.
- **FACT:** family guardian pets are rejected in the structured old-core path.
- **VERSIONED:** older gavinlinasd/iriselia use recipient level +5 for ordinary un-reborn pet care; Bismarck later uses +20.
- **VERSIONED:** gavinlinasd/iriselia fixed builds enable structured pile trade and TRADESYSTEM2; Bismarck fixed server config retains older/simpler active protocol.
- **OPEN:** exact commercial chronology of the two-step confirm/lock UI.
- **OPEN:** exact launch/1.x availability of player-to-player direct trade; preserved code comments date this implementation to April 2001.
- **OPEN:** which anti-trade/binding restrictions belonged to each commercial release.

## Deterministic model

Repository artifacts:

- `tools/stoneage_trade_economy_model.py`
- `tests/test_stoneage_trade_economy_model.py`
- `.github/workflows/validate-stoneage-trade-economy.yml`

The model covers the common state machine, offer freeze, two lock protocols, gold/pet offer validation, source-faithful capacity calculation, gold netting, mutation ordering and pet ownership transfer.

## Next technical seam

Direct trade now closes player-to-player transfer of the three major carried asset classes. The next priority should be a fresh gap audit of the ordinary deterministic loop, with likely high-value candidates being **item shop buy/sell pricing and inventory transfer**, **pet shop/deposit semantics**, or **save/logout persistence boundaries**. The choice should favor the subsystem that closes the largest remaining economy/persistence loop without drifting into later optional content.
