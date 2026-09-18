# StoneAge Janken Core R1

Status: fixed-descendant common core plus verified recovered 2.5 active surface.

## Evidence controls

Fixed descendant source revisions:

- gavinlinasd/StoneAge at 1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56
- iriselia/StoneAge at 9e6c8ce2cd8ed532a7157773acd1c61582c178b5
- BismarckDD/stoneage at 999ffdf1d220ec6666eb65339180689c9caf1876

Recovered specimen:

- source bundle SHA-256 d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5
- Janken argument aggregate SHA-256 491e3784ca8476649788cbbb3c93e13e85af1d0b2af8605e913552515071059c
- real-byte probe workflow 35382078973: success
- nine Janken refs, all nine resolved file-backed

## Recovered active shape

Every one of the nine recovered configurations contains:

- MainMsg;
- EntryItem;
- NoItem;
- WinWarp;
- LoseWarp.

Every EntryItem expression is exactly one starred token with quantity 1.

Every WinWarp and LoseWarp is a valid three-field floor,x,y tuple.

No recovered configuration contains WinItem or LoseItem. Reward-item grant code therefore exists in the descendant sources but is dormant in the preserved 2.5 Janken corpus.

## Interaction start

Talk only reacts to a player within distance one and opens the initial Yes/No window.

If the player chooses Yes, case 1 processes EntryItem before showing the rock/scissors/paper selection.

The item scan covers the full item slot domain used by the descendant, including equipment slots.

## EntryItem check and deletion are separate

NPC_JankenEntryItemCheck validates every comma token against the current inventory without mutating it.

A plain item token requires at least one matching item.

A starred item*count token requires that many matching slots.

Because every token rechecks the original inventory, duplicate requirements can reuse the same physical item during the validation phase.

NPC_JankenEntryItemDel then performs mutation in a separate pass.

For a plain token, source scans every item slot and deletes every matching copy because it does not break after the first deletion.

For a starred token, source deletes matching items until the requested count is reached. If fewer copies exist, it deletes all copies it can find and still returns true.

Bismarck uses CheckCharMaxItem under _NEW_ITEM_ while the other fixed descendants use CHAR_MAXITEMHAVE. This changes slot capacity, not the common control-flow semantics.

## Critical failed-check fallthrough

The main historical defect is in selectWindow case 1.

If EntryItem check fails, source calls the NoItem window, but it does not return.

It immediately calls NPC_JankenEntryItemDel and then continues to send the normal Janken selection window.

Therefore EntryItem is not a hard server-side gate.

This defect is directly relevant to the recovered 2.5 data because all nine configs use EntryItem.

The recovered shape is item*1, so its concrete behavior is:

- if the player has the configured item, one copy is deleted and the game proceeds;
- if the player does not have it, NoItem is sent, deletion removes nothing, and the game still proceeds.

The more destructive plain-token behavior and multi-count partial deletion are fixed-source capabilities but dormant in the recovered nine configs.

## Round and result

Player selections map as:

- 3 -> rock;
- 5 -> scissors;
- 7 -> paper.

The NPC independently selects rand()%3.

Normal rock/scissors/paper comparison determines win or lose. Equal hands are a tie.

Other selection integers can leave the player hand at -1 and fall into the tie path.

A tie sends the tie selection window and returns. It does not re-run EntryItem processing, so repeated ties do not charge the entry item again.

## Win / lose mutation order

On win:

1. attempt WinItem reward if configured;
2. parse WinWarp;
3. warp player;
4. set pleasure action;
5. send result window.

On loss the same order uses LoseItem, LoseWarp and sad action.

NPC_JankenItemGet delegates to NPC_EventAddItem and the judge ignores the reward result. A reward failure therefore does not block the later warp.

The recovered 2.5 configs have no WinItem/LoseItem, so the active preserved path is simply result -> Win/Lose warp -> result action/window.

All nine recovered win and lose warps have the expected three fields, so the source's unsafe missing-warp behavior is not needed to replay the preserved data.

## Deterministic artifacts

- tools/stoneage_janken_core_model.py
- tests/test_stoneage_janken_core_model.py
- .github/workflows/validate-stoneage-janken-core.yml
- research/recovered/STONEAGE-25-JANKEN-USAGE-R1.txt

Local validation: 20 deterministic tests passed.

## Evidence status

FACT: all nine recovered Janken configs are resolved file-backed secondary arguments.

FACT: all nine use exactly one EntryItem token with starred quantity 1.

FACT: all nine have valid WinWarp and LoseWarp triples.

FACT: no recovered Janken config uses WinItem or LoseItem.

SOURCE QUIRK, ACTIVE SHAPE: failed EntryItem validation does not stop the game.

SOURCE QUIRK, DORMANT SHAPE: plain EntryItem deletes all copies of that ID.

SOURCE QUIRK, DORMANT SHAPE: insufficient starred deletion can partially consume available copies.

SOURCE QUIRK: ties do not repeat the entry-item phase.

VERSIONED: Bismarck _NEW_ITEM_ expands the item-slot limit but does not change common Janken control flow.

OPEN: exact JSS-era Janken configuration and behavior until earlier clean data is recovered.

## Next seam

Janken R1 is closed for fixed-descendant common behavior and recovered 2.5 active data. Re-run the remaining state-changing secondary-argument triage rather than selecting by raw reference count.
