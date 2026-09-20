# StoneAge battle drop settlement R1

Status: **stable-descendant mechanics reconstruction; not a claim of byte-identical JSS 1999 server behavior**

## Scope

This note isolates item drops from EXP, money, capture, escape, death penalties and recovery. The purpose is to preserve the old server's source-shaped item lifecycle rather than replace it with a modern "roll a loot table at victory" abstraction.

## Evidence anchors

Primary pinned descendant:

- repository: \`gavinlinasd/StoneAge\`
- commit: \`1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56\`
- files:
  - \`gmsv/src/char/enemy.c\`
  - \`gmsv/src/battle/battle.c\`
  - \`gmsv/src/char/char_item.c\`
  - \`gmsv/src/include/battle.h\`
  - \`gmsv/src/include/version.h\`

Independent control descendant:

- repository: \`iriselia/StoneAge\`
- commit: \`9e6c8ce2cd8ed532a7157773acd1c61582c178b5\`
- the corresponding \`enemy.c\`, \`battle.c\` and \`battle.h\` retain the same base item-drop path.

## Reconstructed lifecycle

### 1. Enemy-held items are created at enemy spawn

**FACT (stable descendant):** \`enemy.c\` iterates ten ITEM/ITEMPROB pairs. A non-zero probability performs a random comparison; on success \`ITEM_makeItemAndRegist()\` creates a real item object and the item index is attached to the enemy's carried-item array.

This means the base mechanic is not "choose an item after victory." The candidate item already exists on the enemy before the later kill-profit transfer.

The pinned Gavin build has \`_FIX_ITEMPROB\` enabled in \`version.h\`, selecting:

\`RAND(0,999) < ITEMPROB\`

The preserved alternative branch is:

\`RAND(0,99) < ITEMPROB\`

**OPEN:** which scale the unrecovered 1999 JSS server used is not established. The implementation therefore keeps the two profiles explicit and does not label the thousand-scale fix as an original-JSS fact.

### 2. Kill profit transfers enemy-held items into a battle reward buffer

**FACT (strong multi-descendant convergence):**

- \`battle.h\` defines \`GETITEM_MAX 3\`.
- \`BATTLE_AddExpItem()\` scans every not-yet-processed dead battle entry.
- For a reward enemy, it removes each valid carried item from the enemy.
- One entry from the *current attack list* is selected with \`RAND(0, allnum-1)\`.
- If that attack-list member is a pet, the item target is mapped to the corresponding player battle entry.
- Therefore attack-list entries are random-selection tickets; they are not deduplicated by owner before the draw.

Each player battle entry has three pending item slots. The first free slot receives the item.

If all three are occupied:

1. \`RAND(0,1)\` decides whether the new item survives.
2. false: the new item is destroyed.
3. true: \`RAND(0,2)\` chooses one old pending slot, the new item replaces it, and the displaced item is destroyed after the source safeguard check.

This overflow behavior occurs at the **battle reward buffer**, before persistent inventory capacity is checked.

### 3. Battle finish transfers pending items to the persistent bag

**FACT (stable descendant):** \`BATTLE_GetExpGold()\` walks the player's pending \`getitem[3]\` slots. For each item it calls \`CHAR_findEmptyItemBox()\`.

\`CHAR_findEmptyItemBoxFromChar()\` scans carried-item slots in ascending order and returns the first empty slot. If an empty slot exists, the already-created item object is attached to the player. If no empty slot exists, the pending item object is destroyed.

A dead player returns before this settlement path. Any remaining battle-held items are later destroyed by battle cleanup.

## Important ownership consequence

Drop ownership follows the same source-shaped *current profit trigger* concept as EXP scanning, but the random attack-list ticket adds a second allocation step. A pet attacker can therefore win the random ticket while the actual item is credited to its owning player entry. Combo/member duplication must not be silently normalized away.

## Implementation boundary

Commit \`82692a51e05f1ca607178e901abd296bd84fa87b\` adds deterministic primitives to \`tools/stoneage_battle_core_model.py\` for:

- fixed-thousand versus preserved-hundred ITEMPROB profiles;
- explicit no-RNG consumption for zero probability;
- already-instantiated drop identity;
- attack-list ticket to player-entry allocation;
- three-slot pending reward buffer;
- full-buffer discard/replacement behavior;
- first-empty persistent-bag settlement and overflow destruction;
- dead-player no-settlement behavior.

Validation:

- battle core Action \`35517467464\`: success
- Taiwan v1.0 gameplay Action \`35517467477\`: success

The encounter bridge also preserves all ten raw \`ITEMn / ITEMPROBn\` pairs on \`EnemyVariantBridge\`; this is bridge evidence, not Taiwan-v1 server provenance.

## Still open

- byte-level JSS-1999 confirmation of ITEMPROB scale;
- carrying concrete reconstructed item-instance state through the single-player persistent battle state;
- capture, money, escape, death penalties and recovery;
- later private-server drop-rate extensions, which are intentionally excluded from the base model.
