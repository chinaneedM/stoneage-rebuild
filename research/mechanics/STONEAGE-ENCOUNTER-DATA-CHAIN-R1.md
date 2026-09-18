# StoneAge Encounter Data Chain R1

Status: **source-verified descendant schema; recovered 2.5 group/encount probe automated**  
Scope: authoritative server `group.txt` and `encount.txt`, linked to `enemy.txt`.

## Authoritative chain

The old server selects a wild encounter through four layers:

```
map floor + coordinate
 -> encount.txt area
 -> weighted group ID
 -> group.txt
 -> weighted enemy ID
 -> enemy.txt concrete variant
 -> TEMPNO
 -> enemybase.txt template
```

This chain is server-side and determines actual enemy composition.

## group.txt schema

The stable row is one name string plus 23 integer fields:

```
GROUP_ID
APPEAR_BY_ITEM_ID
NOT_APPEAR_BY_ITEM_ID
ENEMY_ID1..ENEMY_ID10
CREATEPROB1..CREATEPROB10
```

Blank integer tokens remain at the loader's initialized `-1`.

### References and validation

Each non-`-1` enemy ID is resolved against `enemy.txt:ENEMY_ID`.

If a referenced enemy ID cannot be resolved, that slot is rewritten to `-1`.

A group is rejected if it ends with zero valid enemy references.

The loader also rejects duplicate enemy IDs inside a group.

### Item gates

Before an encounter group is eligible:

- `APPEAR_BY_ITEM_ID != -1` requires the character to possess that item;
- `NOT_APPEAR_BY_ITEM_ID != -1` rejects the group when the character possesses that item.

Thus encounter composition can be conditionally altered by inventory state.

### Enemy weights

For the selected group, the ten `CREATEPROB` values form weighted choices among the corresponding concrete enemy variants.

The server repeatedly draws from that weighted set until the encounter reaches a randomly selected target enemy count or per-variant constraints stop additional copies.

## encount.txt schema

The common base has 30 integer tokens:

```
INDEX
FLOOR
X1
Y1
X2
Y2
ENCOUNT_PROB_MIN
ENCOUNT_PROB_MAX
ENEMY_MAX_NUM
ZORDER
GROUP_ID1..GROUP_ID10
GROUP_PROB1..GROUP_PROB10
```

The later enabled `_ADD_ENCOUNT` extension appends:

```
EVENT_NOW
EVENT_END
EVENT_ENEMY_GROUP
```

for 33 fields total.

All three fixed descendants enable `_ADD_ENCOUNT`, but the probe recognizes both 30- and 33-field forms so older specimens are not forced into a later schema.

## Rectangle normalization and overlap

The loader normalizes the two coordinate corners into:

- minimum x/y origin;
- width = max(x1,x2)-min(x1,x2);
- height = max(y1,y2)-min(y1,y2).

At lookup time only matching regions with `zorder > 0` are considered.

When multiple regions overlap, the region with the higher zorder wins.

Thus encounter geography is not simply "first matching row."

## Encounter-probability bounds

The two probability columns are normalized:

```
stored_min = min(input_min,input_max)
stored_max = max(input_min,input_max)
```

Runtime getters then apply temporary encounter-rate modifiers and clamp each result into 0..100.

These min/max values are copied into character WORK state on login/warp/walk changes; the exact walk-trigger accumulator is a separate movement/battle seam and should not be inferred solely from the table fields.

## Area enemy maximum

`ENEMY_MAX_NUM` is validated at load time:

```
1 <= ENEMY_MAX_NUM <= 10
```

Encounter composition later computes:

```
possible_count = sum(ENEMY_CREATEMAXNUM for available enemy variants)
effective_max = min(area.ENEMY_MAX_NUM, possible_count)
target_count = random integer 1..effective_max
```

The individual enemy's dormant `CREATEMINNUM` is not used here.

## Group selection

For the active encounter area:

1. collect non-`-1` group slots;
2. apply each group's required/forbidden item gates;
3. use the corresponding `GROUP_PROB` values as weights;
4. select one group;
5. build the group's eligible concrete enemy variants;
6. use the group's `CREATEPROB` values as enemy-selection weights.

This establishes two distinct weighting layers:

```
encount GROUP_PROB -> choose group
group CREATEPROB -> choose concrete enemy
```

They must not be merged into one flat spawn probability.

## Big-enemy placement restriction

The selected enemy variants ultimately resolve to `enemybase` templates.

When the template `SIZE` is BIG, the encounter builder limits big enemies to at most five and performs front-position handling so the battle formation remains valid.

This is a template-driven constraint applied after group/enemy weighting.

## Later event override

With `_ADD_ENCOUNT`, event flags can replace the group's enemy row source with `EVENT_ENEMY_GROUP` during encounter construction.

Because source comments place this in a later expansion feature, R1 keeps it as an extension rather than a launch-era assumption.

## Provenance-preserving probe

Artifacts:

- `tools/stoneage_encounter_chain_probe.py`
- `tests/test_stoneage_encounter_chain_probe.py`
- `.github/workflows/probe-stoneage-25-encounter-chain.yml`

The workflow rehydrates the hash-pinned preservation bundle only in CI and emits aggregate metadata:

- file hashes/sizes/row shapes;
- active setup configuration;
- reference integrity counts;
- group slot/weight occupancy;
- item-gate prevalence;
- encounter floor/probability/enemy-max/zorder statistics;
- base vs extended encount schema counts.

It excludes original rows, names and concrete item/enemy/group IDs.

## Evidence status

- **FACT:** group.txt resolves ENEMY_ID references against enemy.txt.
- **FACT:** group rows contain two item gates, ten enemy slots and ten enemy weights.
- **FACT:** duplicate enemy IDs make a group invalid.
- **FACT:** encount.txt maps floor/rectangle regions to up to ten weighted groups.
- **FACT:** overlapping regions are resolved by greater positive zorder.
- **FACT:** encounter probability bounds are normalized and runtime-clamped to 0..100.
- **FACT:** area enemy maximum must be 1..10.
- **FACT:** ENCOUNT group weights and GROUP enemy weights are separate selection stages.
- **FACT:** final enemy count is bounded jointly by area ENEMY_MAX_NUM and enemy CREATEMAXNUM.
- **VERSIONED:** event-triggered alternate enemy group is an `_ADD_ENCOUNT` extension.
- **OPEN:** exact launch-era group/encount rows and expansion chronology.
- **OPEN:** exact historical client-side presentation/cache correspondence to these server tables.

## Next seam

Once the recovered aggregate report is validated, merge the quantitative `enemybase → enemy → group → encount` findings into the gameplay-data inventory and use that complete chain to identify the next unparsed early/core table rather than continuing into later optional content by default.
