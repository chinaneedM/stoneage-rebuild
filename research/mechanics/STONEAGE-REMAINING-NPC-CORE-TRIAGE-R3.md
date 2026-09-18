# StoneAge Remaining NPC Core Triage R3

Status: prioritization after Janken and Charm closure.

This is a decision layer, not a replacement for the empirical recovered queue.

## Already closed / do not reopen

- Healer + WindowHealer: already closed by STONEAGE-HEALER-RECOVERY-CORE-R1.
- ExChangeMan, NPCEnemy, Bus/Air, Janken, Charm: closed for their current fixed-descendant/recovered scope.
- Warp, ItemShop, PetShop, PetSkillShop, PoolItemShop, SavePoint/Oldman: closed in earlier archaeology passes.

## Next priority: Riderman

Recovered queue: four refs, all with inline secondary arguments that point through conff to class-specific configuration.

Riderman is materially state-changing:

- charges Stone tuition;
- writes persistent CHAR_LEARNRIDE thresholds;
- checks player image and carried pets against ridePetTable;
- contains item-letter checks/deletion;
- has family/village revenue side effects layered around the personal riding state.

The next pass should first measure the recovered conff surfaces without retaining item IDs, filenames or dialogue, then separate the personal riding core from family/village revenue extensions.

## Defer Windowman

Windowman parses a class-specific conff file and supports item-presence/item-absence branches between windows.

Although its structs contain takeitem/giveitem/warp/battle fields, the inspected fixed window callback does not execute those state-changing fields. The active callback only chooses another window based on item presence and displays it.

Classification: presentation/conditional UI. Defer unless recovered configuration reveals a source mismatch.

## Defer Bankman to family/economy package

Bankman opens the bank/family client protocol and reads CHAR_BANKGOLD, but personal-bank mutation is handled in the family protocol path, not in the ordinary NPC callback.

Its access logic and adjacent family-account/leave actions are strongly coupled to the family system.

Classification: persistent economy, but family-package coupled. Defer until the family/bank protocol seam is intentionally opened.

## Defer Raceman

Raceman is guarded by _RACEMAN, absent as a common fixed Bismarck NPC source in the inspected lineage, and is heavily coupled to family leadership, race records, prize/ticket state and race server persistence.

Classification: later race/family package.

## Defer Action / TimeMan / Windowman

Action is message/action presentation. TimeMan switches NPC image/message by StoneAge time. Windowman is conditional UI.

Classification: deterministic presentation state; below personal persistent-state seams.

## Queue principle

Prefer personal persistent state and ordinary economy/travel/battle mechanics before family/race packages or presentation-only classes.

## Immediate action

Probe and reconstruct Riderman, beginning with its recovered conff shape and the persistent CHAR_LEARNRIDE tuition progression.
