# StoneAge NPC Secondary-Argument Queue Decision R2

Status: prioritization layer after ExChangeMan, NPCEnemy and Bus/Air closure.

This document does not replace the empirical queue in research/recovered/STONEAGE-25-NPC-SECONDARY-ARG-QUEUE-R1.txt. It classifies remaining classes by whether their secondary arguments materially affect early/core deterministic game state.

## Immediate next class: Janken

Recovered queue:

- Janken refs: 9
- argument refs: 9
- file-backed: 9
- missing secondary files: 0

The three fixed descendant source lineages all expose the same state-changing argument families in npc_janken.c:

- EntryItem gate
- WinWarp / LoseWarp
- WinItem / LoseItem
- item deletion path

Janken therefore combines item prerequisites, deterministic inventory mutation and travel after a random/choice outcome. It is a materially state-changing seam and is the next priority.

The next implementation step should begin with a payload-free recovered Janken usage probe, then model only the active common result/item/warp paths.

## De-prioritized classes

### Action

Recovered refs: 8, all file-backed.

Across all three fixed descendants, the ordinary Action class uses secondary arguments for message/action-trigger presentation, including msgcol and message text. The inspected common core does not expose the same economy/travel/inventory mutation surface as Janken.

Classification: deterministic but presentation-level; defer.

### TimeMan

Recovered refs: 34, all file-backed.

Across all three fixed descendants, common keys include time, change_no, main_msg and change_msg. The class switches NPC graphics/mode and displayed message according to StoneAge time.

Classification: world-presentation/time-state behavior, useful later but lower than state-changing Janken.

### Scheduleman and family packages

Scheduleman is tied to family PK scheduling, challenge/setting timeouts and family battle state. FMPK/FMWarp/Family classes are likewise later family-system packages.

Classification: later package; do not promote into the early/core queue without independent earlier evidence.

### TownPeople / SignBoard / ordinary message classes

These dominate raw reference counts but are primarily dialogue/presentation. TownPeople also contains the current set of missing secondary files in the recovered bundle.

Classification: missing-file provenance remains worth tracking, but raw reference count alone does not make these higher priority than state-changing classes.

## Queue principle

Priority is not determined by number of refs. Prefer unresolved classes whose active secondary arguments can alter:

1. inventory/economy;
2. travel/location;
3. battle entry/result;
4. save/return state;
5. pet state;
6. other persistent deterministic progression.

Presentation-only and later family/event packages remain below those seams.

## Next action

Probe the nine recovered Janken secondary files without retaining dialogue, coordinates or concrete item IDs. Measure active entry-item, result-item, deletion and warp shapes, then reconstruct the fixed-descendant common Janken core.
