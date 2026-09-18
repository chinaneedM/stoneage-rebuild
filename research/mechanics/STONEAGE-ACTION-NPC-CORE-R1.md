# StoneAge Action NPC Core R1

Status: fixed-descendant common trigger/message behavior plus verified recovered 2.5 usage.

## Evidence controls

Fixed descendant source revisions:

- gavinlinasd/StoneAge at 1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56
- iriselia/StoneAge at 9e6c8ce2cd8ed532a7157773acd1c61582c178b5
- BismarckDD/stoneage at 999ffdf1d220ec6666eb65339180689c9caf1876

The three npc_action.c implementations are behaviorally convergent.

Recovered specimen:

- source bundle SHA-256 d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5
- Action argument aggregate SHA-256 720f1e31ff060c0053e3db70e2f660c822b0a3b4f135e83b82f586c7aa442eed
- real-byte workflow 35384705409: success
- 8 Action refs, all 8 resolved file-backed

## Action NPC role

This class is a reactive presentation NPC.

It does not change inventory, Gold, location, battle state, save state, pet state or persistent progression.

Its deterministic core is:

- direct talk -> optional normal response;
- nearby face-to-face player action -> optional response keyed by the exact action.

## Talk route

NPC_ActionTalked only responds when:

- talker is a player;
- player is in front of the Action NPC within the helper's one-grid constraint;
- normal exists in the argument string.

If those checks pass, normal is sent through CHAR_talkToCli.

No state mutation accompanies the response.

## Watch action table

NPC_ActionWatch first requires:

- watched object type is character;
- watched character is a player;
- NPC and player are face-to-face at one grid.

It then searches a fixed table of 11 actions in order:

- attack
- damage
- down
- sit
- hand
- pleasure
- angry
- sad
- guard
- nod
- throw

If the current action matches a table entry and that response key exists, the configured response is sent.

Unsupported actions are silent.

## Comment versus implementation

The source comments describe normal as the reply for ordinary talk or an invalid action.

The implementation does not use normal as a Watch fallback.

normal is only read by NPC_ActionTalked.

A Watch action not present in the 11-entry table, or a supported action whose configured key is missing, produces no reply.

R1 follows executable behavior rather than the comment.

## Recovered 2.5 active surface

All 8 recovered configs contain every response key:

- normal
- all 11 Watch action keys

All 8 also contain msgcol=1.

Message payloads are not retained by the aggregate report. The probe only records byte-length distributions.

Thus the recovered 2.5 Action NPCs are fully populated reactive-message configurations rather than sparse per-action special cases.

## msgcol initialization defect

The fixed source contains a significant initialization bug.

NPC_ActionInit declares:

char argstr[NPC_UTIL_GETARGSTR_BUFSIZE];

but does not call NPC_Util_GetArgStr before executing:

NPC_Util_GetNumFromStrWithDelim(argstr, "msgcol")

NPC_Util_GetNumFromStrWithDelim treats its first pointer as an already initialized pipe-delimited C string and repeatedly scans it.

Therefore the literal fixed source reads uninitialized stack memory while trying to determine msgcol.

Although all 8 recovered configs contain msgcol=1, the fixed source does not deterministically read that value during initialization.

The subsequent fallback to the default yellow constant only occurs if the undefined scan happens to return -1. It does not repair the undefined behavior.

R1 therefore records:

- configured msgcol value: FACT, 1 in all 8 recovered configs;
- final runtime message color from literal fixed source: UNDEFINED / not safely reconstructible solely from this code.

A later clean implementation may intentionally fix this defect, but that belongs to redesign/compatibility policy rather than archaeology.

## Evidence status

FACT: all 8 recovered Action refs resolve to file-backed configs.

FACT: all 8 recovered configs contain normal plus all 11 Watch response keys.

FACT: all 8 recovered configs contain msgcol=1.

FACT: Talk uses normal; Watch uses only the exact 11-entry action table.

FACT: Action has no gameplay-state mutation in the inspected common core.

SOURCE DEFECT: NPC_ActionInit reads uninitialized argstr when initializing msgcol.

SOURCE/COMMENT MISMATCH: unsupported Watch actions do not fall back to normal.

OPEN: whether an earlier commercial build initialized argstr correctly, and what runtime color behavior users actually observed.

## Deterministic artifacts

- tools/stoneage_action_core_model.py
- tests/test_stoneage_action_core_model.py
- .github/workflows/validate-stoneage-action-core.yml
- research/recovered/STONEAGE-25-ACTION-USAGE-R1.txt

Local reference validation: 10 deterministic tests passed.

## Next seam

Action R1 is closed. The remaining high-reference ordinary classes SignBoard, TownPeople and Mic are presentation/broadcast classes in the fixed source and should be handled as lightweight semantic registrations rather than promoted into state-machine reconstruction. Re-triage after those registrations before entering family/race/VIP packages.
