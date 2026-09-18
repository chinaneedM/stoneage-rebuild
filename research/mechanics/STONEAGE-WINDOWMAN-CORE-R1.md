# StoneAge Windowman Core R1

Status: fixed-descendant conditional-window routing core plus partially recovered 2.5 configuration surface.

## Evidence controls

Fixed descendant source revisions:

- gavinlinasd/StoneAge at 1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56
- iriselia/StoneAge at 9e6c8ce2cd8ed532a7157773acd1c61582c178b5
- BismarckDD/stoneage at 999ffdf1d220ec6666eb65339180689c9caf1876

Recovered specimen:

- source bundle SHA-256 d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5
- resolved Windowman conff aggregate SHA-256 5115e8544aa95014ded26646fbe75c1dbfa25e0aa48dfd10d4eadb29706e2b80
- real-byte workflow 35384359937: success
- 17 Windowman refs
- 13 resolved conff files
- 4 referenced conff files missing from the recovered 2.5 bundle
- 8 distinct resolved conff contents

The four missing conff files remain an explicit evidence gap. R1 does not infer their behavior from the 13 surviving files.

## What the source actually executes

Windowman is a generic multi-window dialogue router.

The fixed descendants share the same active callback semantics.

Interaction opens window 1 for a player in front of the NPC. Window callbacks reject a player farther than one grid.

For SELECT windows:

button = atoi(data) + 5

and button values above 12 are rejected.

For ordinary message windows, the source checks OK, CANCEL, YES, NO, PREV and NEXT flag bits in that order and maps them to button indexes 0 through 5.

Only buttons marked use=true are processed.

## Active route order

For a used button:

1. newwin starts at -1.
2. If checkhaveitem is configured, the player's item slots are scanned for the configured item ID.
   - missing -> callback returns immediately;
   - present -> newwin becomes haveitemgotowin.
3. If checkdonthaveitem is configured, the item slots are scanned again.
   - present -> callback returns immediately;
   - absent -> newwin becomes donthaveitemgotowin.
4. If newwin is still -1, source uses gotowin.
5. Source reads the target window from the conff and sends it.

If both conditions are configured and both pass, the second don't-have branch overwrites the target selected by the first have-item branch.

No item is deleted or granted by these checks.

Bismarck can vary the number of item slots through later inventory extensions, but the routing semantics are the same.

## Parsed fields that do not mutate state

The window struct contains takeitem and giveitem, and the conff parser recognizes both fields.

However the fixed Windowman callback never applies either value.

They are therefore parser/data capability without an execution path in this NPC implementation.

The button struct also contains warp and battle integer fields, but the fixed Windowman conff parser has no branches that assign either field. They remain initialized to -1 and have no runtime use in the inspected callback.

R1 explicitly does not reinterpret these names as functioning item transfer, warp or battle mechanics.

## Recovered 2.5 active surface

Among the 13 resolved conff files:

- every config contains ordinary gotowin routing;
- none contains checkhaveitem;
- none contains haveitemgotowin;
- none contains checkdonthaveitem;
- none contains donthaveitemgotowin;
- none contains takeitem;
- none contains giveitem;
- none contains warp;
- none contains battle.

Therefore the surviving recovered 2.5 Windowman configurations are pure deterministic window graphs with no item-condition routing and no state mutation.

Recovered windows span ordinary low-numbered sequences plus 1000/2000/3000 families. Those numbers are routing identifiers only; R1 does not infer gameplay semantics from their numeric ranges.

## Structural validation

At endbutton, source accepts a button definition if:

- gotowin is present; or
- a complete checkhaveitem + haveitemgotowin pair exists; or
- a complete checkdonthaveitem + donthaveitemgotowin pair exists.

An incomplete conditional definition with no gotowin causes configuration validation failure.

## Evidence status

FACT: all three fixed descendants use the same Windowman routing callback.

FACT: 13 of 17 recovered Windowman conff references resolve; four are missing from the recovered bundle.

FACT: the 13 surviving configs contain gotowin but none of the item-condition fields.

FACT: the 13 surviving configs contain no takeitem/giveitem/warp/battle key.

FACT: fixed source parses takeitem/giveitem but never executes those fields in the Windowman callback.

FACT: fixed source has warp/battle struct placeholders but no Windowman conff parser branch or callback execution for them.

SOURCE QUIRK: if both item conditions are configured and pass, the later don't-have target overwrites the earlier have-item target.

OPEN: the four missing recovered conff files could contain fields absent from the surviving 13 and must remain unresolved until recovered.

OPEN: exact launch/JSS Windowman configuration and whether earlier builds executed now-inert fields.

## Deterministic artifacts

- tools/stoneage_windowman_core_model.py
- tests/test_stoneage_windowman_core_model.py
- .github/workflows/validate-stoneage-windowman-core.yml
- research/recovered/STONEAGE-25-WINDOWMAN-USAGE-R1.txt

Local reference validation: 16 deterministic tests passed.

## Next seam

Windowman R1 is closed for fixed-descendant routing semantics and the 13 surviving recovered 2.5 configs, with four conff files explicitly unresolved. Advance to Action as the next lightweight common presentation/action-message seam.
