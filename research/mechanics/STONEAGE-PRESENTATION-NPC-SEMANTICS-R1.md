# StoneAge Presentation NPC Semantics R1

Status: lightweight registration for SignBoard, TownPeople and Mic.

These classes are intentionally not promoted into large gameplay state machines because their fixed-source common behavior is presentation/broadcast routing rather than inventory, Gold, location, battle, save, pet or persistent-progression mutation.

## Evidence controls

Fixed descendant source revisions:

- gavinlinasd/StoneAge at 1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56
- iriselia/StoneAge at 9e6c8ce2cd8ed532a7157773acd1c61582c178b5
- BismarckDD/stoneage at 999ffdf1d220ec6666eb65339180689c9caf1876

Recovered 2.5 source bundle SHA-256:

d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5

Presentation aggregate SHA-256:

9e5a2919b44412edc812d9b7612346f74dfa8f99f2910d5e9b424083c425fe2f

Real-byte workflow: 35385048916.

## SignBoard

Fixed source behavior is identical across the three descendants.

Looked only responds to a player within distance one.

The NPC argument is rendered inside a message window.

A special %manorid:N% placeholder can read the current manor/family point-list state and substitute the occupying family name, or a no-family phrase when the manor has no valid owner.

This is a dynamic read of family state for display. SignBoard itself does not mutate family state.

The returned WindowTalked callback performs no state operation beyond the distance check.

Recovered 2.5:

- 181 refs;
- all 181 argument files resolve;
- 177 are plain signboards;
- 4 contain the manor placeholder.

Therefore the manor-display integration is active recovered behavior, but only in a small minority of boards.

## TownPeople

Fixed source behavior is identical across the descendants.

Talk only responds to a player that passes the three-grid in-front helper.

The entire NPC argument is treated as comma-separated dialogue. The code counts commas, chooses rand()%token_count and sends the selected token in white.

There is no persistent gameplay mutation.

Recovered 2.5:

- 445 refs total;
- 389 resolved file-backed args;
- 34 inline args;
- 15 referenced argument files are missing;
- 7 refs have no argument.

For the 430 refs whose argument shape is observable, variant counts range from one to twelve. Two variants are the most common recovered shape.

The 15 missing files remain explicit provenance gaps.

### Seven no-argument source defects

NPC_TownPeopleTalked declares a local arg buffer and calls NPC_Util_GetArgStr but does not check its return value.

NPC_Util_GetArgStr returns NULL when CHAR_NPCARGUMENT is absent and does not initialize the destination buffer in that branch.

TownPeople then immediately scans the local array for commas and passes it to the delimiter helper.

Therefore the seven recovered no-argument TownPeople instances have undefined behavior under the literal fixed source. R1 does not normalize them into empty dialogue.

## Mic

The three fixed descendants share the ordinary local-broadcast core.

Init detects FREE and WIND by substring.

When the argument contains pipes, it parses eight positional integer slots. These define a floor, a rectangle from two corners and a family-broadcast flag among the stored work values. Normal work mode remains rectangle-scoped.

Without a pipe, source sets work mode 1.

Talk requires a player. Unless FREE was detected, the player must face the Mic at one grid.

Ordinary recipients must:

- be active players;
- be on the Mic's stored floor;
- when mode is rectangle-scoped, be inside the inclusive rectangle.

Eligible recipients receive ordinary chat.

If WIND is set, a non-battling eligible recipient additionally gets a message window. A battling recipient still receives chat but not the WIND window.

A nonzero family flag can redirect a qualifying family-role talker into the family announcement protocol instead of the local broadcast. The exact role check is version-conditioned and should not be over-unified.

Recovered 2.5:

- 4 refs;
- all 4 files resolve;
- all 4 use exactly eight pipe-separated tokens and rectangle-scoped mode;
- all 4 have family flag zero;
- exactly 1 contains FREE;
- none contains WIND.

Thus the active preserved 2.5 Mic surface is local same-floor rectangle chat, with one Mic allowing talk without the normal facing requirement. WIND and family announcement are dormant in these four configs.

## Evidence status

FACT: SignBoard, TownPeople and Mic do not mutate ordinary player core state in their common presentation paths.

FACT: 4 of 181 recovered SignBoards actively read manor ownership for display.

FACT: recovered TownPeople includes 15 missing argument files and 7 no-argument refs; both remain explicit evidence defects.

FACT: all four recovered Mic configs are eight-token scoped mode with family flag zero.

FACT: one recovered Mic enables FREE; none enables WIND.

SOURCE DEFECT: TownPeople ignores a failed GetArgStr and can read an uninitialized local buffer for no-argument NPCs.

VERSIONED: Mic family-role qualification differs in descendant code and is dormant in recovered 2.5 because family flag is zero.

OPEN: contents of the 15 missing TownPeople argument files.

## Deterministic artifacts

- tools/stoneage_presentation_npc_model.py
- tests/test_stoneage_presentation_npc_model.py
- .github/workflows/validate-stoneage-presentation-npc.yml
- research/recovered/STONEAGE-25-PRESENTATION-NPC-USAGE-R1.txt

Local reference validation: 14 deterministic tests passed.

## Next seam

The ordinary high-volume presentation classes are registered and removed from core-mechanics priority. Re-triage the remaining unresolved classes, with particular attention to Dengon/Duelranking persistence/display boundaries and whether any personal-bank behavior must be split out from the later family Bankman package.
