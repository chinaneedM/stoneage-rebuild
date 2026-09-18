# StoneAge Riderman Core R1

Status: fixed-descendant common personal riding core plus verified recovered 2.5 trainer configuration.

## Evidence controls

Fixed descendant source revisions:

- gavinlinasd/StoneAge at 1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56
- iriselia/StoneAge at 9e6c8ce2cd8ed532a7157773acd1c61582c178b5
- BismarckDD/stoneage at 999ffdf1d220ec6666eb65339180689c9caf1876

Recovered specimen:

- source bundle SHA-256 d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5
- Riderman conff aggregate SHA-256 20c87aa00cb82aeb7bde861d900f1dc159f9794a2f9693065186578b6b2a7009
- real-byte usage workflow 35383566011: success
- four recovered Riderman refs, all four inline args with resolved conff
- all four resolve to one identical conff content

## Recovered 2.5 trainer configuration

The shared configuration has the four tuition windows:

- winno 110 -> takegold 5000 -> gotowin 6
- winno 120 -> takegold 10000 -> gotowin 7
- winno 130 -> takegold 15000 -> gotowin 8
- winno 140 -> takegold 20000 -> gotowin 9

Those target actions are hard-coded by npc_riderman.c as:

- action 6 -> CHAR_LEARNRIDE = 40
- action 7 -> CHAR_LEARNRIDE = 80
- action 8 -> CHAR_LEARNRIDE = 120
- action 9 -> CHAR_LEARNRIDE = 200

Therefore the recovered 2.5 tuition ladder is exactly:

5000 -> 40
10000 -> 80
15000 -> 120
20000 -> 200

The same conff also contains letter1, letter2, letter3 and letter4 in every tuition window.

It contains no recovered takeitem, giveitem, checkhaveitem or checkdonthaveitem control key.

## Letter / pet prerequisites are dormant source remnants

In gavin and iriselia, the trainer code still contains blocks that would:

- require a manor/family letter;
- search carried pets for a character/pet ridePetTable match;
- consume the letter.

However the entire prerequisite block is wrapped in #if 0 for every training tier.

Bismarck's fixed Riderman source has removed the dead call block from the active training path.

The letter1..4 fields remain parseable, and the recovered 2.5 conff still carries them, but the active trainer does not consult or delete those items.

This is a useful archaeology distinction: the data preserves an earlier design intent after the server behavior stopped enforcing it.

The generic takeitem/giveitem/checkhaveitem fields are likewise parser capability, not recovered active Riderman behavior.

## Training progression

The first three tiers are common across all fixed descendants.

### Beginner / action 6

If CHAR_LEARNRIDE >= 40, training is rejected as already learned.

Otherwise there is no lower training prerequisite.

If carried Stone is below the current window takegold value, training is rejected with no mutation.

On success:

1. deduct tuition;
2. set CHAR_LEARNRIDE to 40;
3. refresh Gold status;
4. refresh riding-training status;
5. optionally credit manor-family revenue.

### Intermediate / action 7

Requires:

40 <= CHAR_LEARNRIDE < 80

Successful training deducts tuition then writes 80.

### Advanced / action 8

Requires:

80 <= CHAR_LEARNRIDE < 120

Successful training deducts tuition then writes 120.

## Special-class lineage divergence

The final tier is not identical across the fixed descendants.

gavin and iriselia:

- reject when CHAR_LEARNRIDE > 120;
- reject when CHAR_LEARNRIDE < 120;
- therefore only exactly 120 can buy the final class;
- success writes 200.

Bismarck:

- reject only when CHAR_LEARNRIDE > 200;
- reject when CHAR_LEARNRIDE < 120;
- therefore every value from 120 through 200 inclusive can buy the final class;
- success writes 200.

This produces a Bismarck-specific quirk: a character already at exactly 200 can pay the final tuition repeatedly and remain at 200.

R1 preserves the split rather than choosing one as historically authoritative.

## Tuition and family revenue

Tuition is checked before mutation.

If current Gold < takegold, no Gold or training state changes.

On success CHAR_DelGold runs before CHAR_LEARNRIDE is written.

After each successful class, the fixed sources compute:

takegold / 5

using C integer division and, when the trainer NPC's village/family mapping resolves, send that amount to the manor-family account through the family server protocol.

This is a post-success family-economy extension. It is recorded here because it is triggered by Riderman, but family-account persistence remains outside the personal riding core.

For the recovered tuition ladder the nominal shares are 1000, 2000, 3000 and 4000 Stone.

## What CHAR_LEARNRIDE actually controls

The native riding path compares training directly against target pet level:

CHAR_LEARNRIDE < pet level -> reject ride

So the trainer thresholds are real mount-level ceilings, not display-only progression.

The fixed descendant common riding intersection also rejects when:

- the character is invalid;
- the character is in battle;
- the requested pet slot is invalid;
- the player is already riding;
- pet fixed-AI / loyalty is below 100;
- pet level exceeds player level + 5;
- no direct player-base-image + pet-base-image mapping exists in ridePetTable.

On success the rider slot is stored in CHAR_RIDEPET, the player's current base image becomes the ride image, parameters are recomputed, the change is broadcast, and ride status is refreshed.

Dismount sets CHAR_RIDEPET=-1, restores CHAR_BASEBASEIMAGENUMBER, recomputes parameters and refreshes nearby/status state.

## Riding-runtime version boundaries

Do not over-unify later riding extensions.

gavin and iriselia enable _NEW_RIDEPETS; Bismarck's fixed version.h does not.

All inspected lineages contain _PET_2TRANS-related logic, but the accepted pet-transmigration threshold is not stable across the fixed descendants.

Bismarck also contains additional fork-specific riding checks such as trade-mode rejection and other modernized gates.

The direct base player/pet ridePetTable path, training ceiling, loyalty gate and ordinary level-gap gate are the stable R1 intersection.

## Persistence across transmigration

In the fixed transmigration source, the line that would reset CHAR_LEARNRIDE is commented out.

Transmigration dismounts the current ride but does not reset learned riding proficiency.

R1 therefore treats CHAR_LEARNRIDE as persistent personal progression across ordinary transmigration.

## Deterministic artifacts

- tools/stoneage_riderman_core_model.py
- tests/test_stoneage_riderman_core_model.py
- .github/workflows/validate-stoneage-riderman-core.yml
- research/recovered/STONEAGE-25-RIDERMAN-USAGE-R1.txt

Local reference validation: 19 deterministic tests passed.

## Evidence status

FACT: all four recovered Riderman refs resolve to one identical conff content.

FACT: recovered tuition is 5000 / 10000 / 15000 / 20000 Stone for targets 40 / 80 / 120 / 200.

FACT: recovered conff preserves letter1..4 on all four tuition windows.

FACT: active fixed-source trainer code does not enforce or delete the letter and does not require a ride-compatible pet before training.

FACT: CHAR_LEARNRIDE is directly checked against pet level when mounting.

FACT: training is not reset by the fixed transmigration path.

VERSIONED: final-tier already-learned guard is >120 in gavin/iriselia but >200 in Bismarck.

VERSIONED: later riding extensions (_NEW_RIDEPETS, pet-transmigration limits, trade-mode gates and similar checks) are not a three-lineage common core.

OPEN: exact JSS-era riding-school progression and whether the letter/pet prerequisite was active in earlier commercial builds.

## Next seam

Riderman R1 is closed for the recovered 2.5 trainer data plus the fixed-descendant common personal riding core. With ordinary personal persistent-state NPC seams now exhausted, advance to the common TimeMan world-time presentation/state seam while keeping Bankman/Raceman/Scheduleman in later family/race packages.
