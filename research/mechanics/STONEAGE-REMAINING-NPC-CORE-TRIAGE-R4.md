# StoneAge Remaining NPC Core Triage R4

Status: **fresh residual triage after Dengon/Duelranking and personal-bank closure**

This replaces R3 as the current prioritization layer. R3 remains historical record of an earlier queue.

## Inputs

Recovered 2.5 function-set distribution:

- research/recovered/STONEAGE-25-NPC-WORLD-GRAPH-R1.txt
- verified preservation bundle SHA-256 d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5

Fixed descendant function-set tables:

- gavinlinasd/StoneAge @ 1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56
- iriselia/StoneAge @ 9e6c8ce2cd8ed532a7157773acd1c61582c178b5
- BismarckDD/stoneage @ 999ffdf1d220ec6666eb65339180689c9caf1876

Comparison is case-insensitive because the template lookup path is not a case-sensitive historical identity claim. In particular, recovered lowercase transmigration is not counted as an all-source-missing class merely because fixed-source capitalization differs.

## Already closed / do not reopen

The current core sweep already has dedicated closure records for Warp/WarpMan, SavePoint/Oldman, shops, Healer/WindowHealer, ExChangeMan, NPCEnemy, Bus/Airplane, Janken, Charm, Riderman, TimeMan, Windowman, Action, SignBoard/TownPeople/Mic, Dengon/ordinary Duelranking, personal Bankman CHAR_BANKGOLD persistence, and player transmigration.

These classes remain reopenable only if contradictory evidence appears.

## Data/source skew: do not invent implementations

Thirteen recovered 2.5 function-set tokens have no corresponding entry in **any** of the three fixed descendant functionSet tables:

- BlackSmith
- Box
- Class01
- Doorman
- Gun
- Identifier
- Keyman
- Movewall
- Msg2
- RoomAdmin
- Ship
- StepSwitch
- Temple

This is an active preservation/source-lineage mismatch, not evidence that those commercial classes were broken or absent.

Some public source trees still contain implementation files or templates bearing related names—for example npc_doorman.c, npc_roomadminnew.c, and a Bismarck npc_ship.c. That does **not** repair the function-set join for the pinned source snapshots.

**Rule:** do not reconstruct these thirteen by guessing which later/unused implementation corresponds to the recovered 2.5 token. They remain OPEN until a matching source/data lineage or executable-level dispatch evidence is recovered.

## Versioned function-set classes

- Raceman: present in gavinlinasd/iriselia but absent from fixed Bismarck table.
- VipShop: present in fixed Bismarck but absent from gavinlinasd/iriselia tables.

Both remain later/versioned package work.

## Common residual classes after previous closures

| Class | Recovered refs | Active effect surface | R4 classification |
| --- | ---: | --- | --- |
| Quiz | 4 | entry item/Stone consumption, item reward, score-band warp | **next core seam** |
| LuckyMan | 1 | Stone charge plus randomized result presentation | economy mutation, below Quiz |
| Door | 3 | runtime open/close/overability/key checks | ordinary world-state seam, no direct player persistence in npc_door.c |
| BodyLan | 2 | transient event state plus party warp | event wrapper over already-modeled warp primitive |
| CheckMan | 3 | window/pagination work state | read/presentation |
| Msg | 1 | looked-at message | presentation |
| TranserMan | 2 | compile-gated _TRANSER_MAN transport/event menu | enabled in fixed descendants but later feature-coded; below ordinary Quiz |
| WarpMan | 1 | dialogue/group warp plus later extensions | already covered by Warp / Map Transition R1 |

### Quiz

Quiz is the strongest unresolved ordinary-core candidate because all three fixed descendants expose the same key families and the class directly changes player state.

Common source keys include EntryItem, EntryStone, GetItem, Border, Warp, Quiznum, Type, Answer and Level.

The source can validate and consume entry items, validate and deduct carried Stone, choose questions from the global question.txt table, score answers, grant one reward item from a configured candidate set, and choose a destination from score thresholds before warping the player.

Recovered 2.5 has four Quiz refs. Therefore R4 promotes a payload-free real-byte Quiz usage probe as the immediate next task.

### LuckyMan

LuckyMan is not presentation-only: accepting the service deducts configured Stone and then displays a randomized configured result. The inspected fixed core does not grant a reward item, change progression, or perform travel, so it is a narrower economy sink than Quiz.

### Door

npc_door.c changes NPC-local runtime door state, graphic/overability and key/pass conditions. It does not directly write ordinary player progression in the inspected common path.

The separate npc_doorman.c can charge player Gold, but recovered Doorman is one of the thirteen function-set tokens that does not join to any pinned fixed functionSet table. Do not silently merge Doorman toll behavior into recovered Door.

### BodyLan

BodyLan maintains transient event/work state and can warp the participant/party. The authoritative warp primitive and party projection semantics are already reconstructed. Unless recovered configuration reveals a new persistent state field, BodyLan is an event wrapper rather than a foundational unmodeled mechanic.

### CheckMan / Msg

The inspected fixed callbacks mutate only temporary window/pagination state or display text. They remain presentation-level.

### TranserMan

All three fixed descendants compile _TRANSER_MAN, but the source labels it as a separately enabled transport feature and its path is event-menu/transport oriented. It remains below the more ordinary Quiz seam until recovered data shows a unique persistent mutation not already represented by warp/event-action mechanics.

## Family and later packages remain deferred

Familyman, FmDengon, FmHealer, FmLetter, FMPKCallMan, FMPKMan, FMWarpMan, ManorSman, Raceman, Scheduleman and VipShop remain deferred. The personal Bankman account has already been separated from this package.

## Immediate action

1. Run the recovered 2.5 Quiz probe against the four refs and global question table without retaining questions, answer text, item IDs, coordinates or dialogue.
2. Reconstruct only the active recovered Quiz mutation shape plus stable common fixed-source control flow.
3. Then re-evaluate LuckyMan and Door. If neither exposes a material core gap beyond Stone sink / transient world-door state, close the residual ordinary NPC sweep and return priority to clean-client recovery plus any concrete combat/data gaps.

## Evidence status

- **FACT:** Quiz is common to all three pinned fixed function-set tables and has four recovered 2.5 refs.
- **FACT:** common Quiz source can consume items/Stone, grant item rewards and warp by score threshold.
- **FACT:** thirteen recovered 2.5 tokens do not join to any of the three pinned fixed function-set tables.
- **FACT:** LuckyMan deducts Stone in its accepted fixed-source service path.
- **FACT:** Door mutates runtime NPC/world-door state rather than ordinary player progression in its own inspected core.
- **FACT:** CheckMan and Msg do not expose ordinary persistent-player mutation in their inspected common callbacks.
- **VERSIONED:** Raceman / VipShop function-set availability differs across pinned source lineages.
- **OPEN:** implementations for the thirteen all-source-missing recovered tokens.
- **OPEN:** whether an earlier/cleaner source lineage will prove BlackSmith, Identifier, Box or other missing tokens to be historically central mechanics.