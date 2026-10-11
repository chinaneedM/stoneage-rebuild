# PET carried-item / unique-code source-path orientation — R1

Status: **SOURCE-ONLY AUDIT IN PROGRESS**, not accepted or integrated.
Scope: clean pinned Gavin `1f90cb6` and Bismarck `999ffdf1` late descendants,
not 1999 JSS / Taiwan v1.0 and not a natural gameplay outcome.

## Why this gate exists

The preceding bounded native original battle/factory experiment connected a
released item index8 with a stale synthetic PET2 carry reference to that
physical index. It did **not** demonstrate a player-facing action, a genuine
persisted pet item, or a natural PET alias from ordinary gameplay.

This source-only gate traces the named operations that can read/write a
`Char`'s carried-item array, serialize or parse pet item records, issue
unique codes, and allocate or release global item slots. It may discover
a possible path without proving a real call site or feature macro.

## Observations to test against pinned raw functions

1. `CHAR_addItemToChar` writes an index returned by
   `ITEM_makeItemAndRegist` into `indexOfExistItems`; `CHAR_addItem`
   sets `ITEM_WORKCHARAINDEX` and clears `ITEM_WORKOBJINDEX`.
   `CHAR_addItemSpecificItemIndex` uses an empty-box lookup and
   `CHAR_setItemIndex`, then sets item owner fields. Those function
   bodies have no explicit `CHAR_TYPEPLAYER` / `CHAR_TYPEPET` exclusion.
   **This is not proof that a gameplay caller passes a PET.**
2. `_CHAR_setItemIndex` writes the physical index into the actor's
   slot and, under `_UNIQUE_P_I`, invokes `ITEM_setItemUniCode`.
   The latter obtains time and increments `unique_i` under its
   own predicate. The compile-time macro and first-release uniqueness
   generation conditions require separate verification. The pinned default
   `version.h` headers explicitly define `_UNIQUE_P_I`, but this alone
   does not prove a production binary`s options or item-identity guarantee.
3. Pet item serialization and parsing branches exist in
   `CHAR_makePetStringFromPetIndex` /
   `CHAR_makePetFromStringToArg`, but differ by descendant:
   Gavin gates pet item records under `!_SIMPLIFY_ITEMSTRING` and
   `CHAR_MAXITEMHAVE`; Bismarck gates them under `_PET_ITEM` and
   `CHAR_MAXPETITEMHAVE`. The parser calls the original item
   initializer and writes the new physical index directly into the
   pet's carried-item array. **Actual build flags and save/load caller
   reachability are not proven by raw source existence. **New pinned-header
   finding:** both default `version.h` files define `_SIMPLIFY_ITEMSTRING`,
   neither defines `_PET_ITEM`. Therefore the pet item persistence blocks
   are excluded under these default header definitions (Gavin negative
   simplification branch; Bismarck positive PET_ITEM branch). These are
   default-header facts, not a complete proof of deployed compiler flags.**
4. In both pinned descendants the original `_ITEM_initExistItemsOne`
   scans an inactive candidate's existing-owner *PLAYER* carry refs
   before reuse. `_ITEM_endExistItemsOne` scans the configured
   `CHAR_getPlayerMaxNum` index range before release. This may
   leave a PET alias outside that range in the synthetic fixtures;
   it does not establish naturally produced stale references.

## Acceptance criteria

Pinned Git commit and exact Git blob IDs for eight original files (three C
source files plus `include/version.h` per profile) must match,
the 11 named original function bodies per profile must be found and fingerprinted
without storing source, and all source-only branch assertions must hold in
a 2-profile / 22-function report. Negative Python tests must reject missing,
tampered or overpromoted source-only reports. GitHub Actions must succeed and
the new derived report's ZIP digest must be independently verified.

SOURCE_ONLY must never be reclassified as natural execution FACT by this
gate. Even if all source tests pass, the next runtime question remains
**which real gameplay/persistence callers (if enabled) can create or clear a pet item
reference, with what macro and object owner/unique-code state**.

No changes to original bodies, production assets, or modern-engine design.
Pressure2486=2465 bounded closed +18 OPEN +3 historical UB, no new historical
promotion and no new UB classification.
