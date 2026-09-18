# StoneAge Player Birth / Hometown Core R1

Status: **strong descendant-code reconstruction; exact launch-era identity remains OPEN**  
Scope: original four-hometown creation linkage, with later unified-spawn and configurable-starter-pet branches kept separate.

## Purpose

The creation model already recovers attribute and element allocation. This note closes the remaining ordinary birth-side seam: how the creation packet's `hometown` value links the initial village/spawn, elder/savepoint state, and starter-pet selection.

## Evidence set

Fixed source revisions:

- **BismarckDD/stoneage** @ `999ffdf1d220ec6666eb65339180689c9caf1876`
  - `server/gmsv/char/char_data.c`
  - `server/gmsv/char/char.c`
  - `client/stoneage/system/netproc.cpp`
- **gavinlinasd/StoneAge** @ `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
  - `gmsv/src/char/char_data.c`
  - `gmsv/src/char/char.c`
- **iriselia/StoneAge** @ `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
  - `Source/gmsv/char/char_data.c`
  - `Source/gmsv/char/char.c`

## Hometown is part of the creation contract

**FACT**

The create-new-character protocol carries an integer `hometown`. The ordinary elder-position function accepts only `0..3`.

In the common four-village path:

```
initial elder index = hometown
savepoint bit       = 1 << hometown
```

The stable elder coordinate table is:

| hometown | floor | x | y |
|---:|---:|---:|---:|
| 0 | 1006 | 15 | 22 |
| 1 | 2006 | 20 | 16 |
| 2 | 3006 | 21 | 16 |
| 3 | 4006 | 14 | 20 |

Bismarck client code independently renders the same four indices as:

| hometown | village |
|---:|---|
| 0 | 萨姆吉尔村 |
| 1 | 玛丽娜丝村 |
| 2 | 加加村 |
| 3 | 卡鲁它那村 |

This gives a direct numeric bridge from creation-packet value to visible village name and server spawn coordinates.

## Starter-pet linkage

**FACT — preserved ordinary path in gavinlinasd / iriselia**

The ordinary creation code selects:

```c
enemyarray = ENEMY_getEnemyArrayFromId(hometown + 1);
petindex = ENEMY_createPetFromEnemyIndex(charaindex, enemyarray);
CHAR_setMaxExpFromLevel(petindex, 1);
```

Therefore the stable numeric linkage is:

| hometown | starter enemy ID |
|---:|---:|
| 0 | 1 |
| 1 | 2 |
| 2 | 3 |
| 3 | 4 |

The same descendant source family contains an explicit hometown-to-pet comment/mapping in its test-server branch:

- default / elder 0 -> ID 1 -> 乌力
- elder 1 / 玛丽娜丝 -> ID 2 -> 凯比
- elder 2 / 加加 -> ID 3 -> 克克尔
- elder 3 / 卡鲁它那 -> ID 4 -> 威伯

R1 treats the **numeric ID mapping as the stronger fact**. The Chinese pet names are retained as source-name hints because they are supplied by later descendant comments rather than independently resolved here from an authoritative launch enemy table.

## Later variants are not baseline rules

### Bismarck `_UNIFIDE_MALINASI`

Bismarck's current descendant branch can force:

```
initial elder index = 1
```

while still setting the origin/savepoint bit from the incoming `hometown`.

This is modeled only as a later location override. It is not used to rewrite the ordinary four-village baseline.

### 6.0 `_DELBORNPLACE`

gavinlinasd / iriselia explicitly label a branch:

```
Syu ADD 6.0 统一出生於新手村
```

That path keeps a separate `BornPet` copy of the incoming hometown and can redirect the player into later newbie/museum coordinates while selecting a different starter-pet ID range (`BornPet + 2076`).

The code itself therefore marks this as a later version transformation rather than evidence for the original four-village path.

### `_NEW_PLAYER_CF`

Bismarck's newer branch makes starter pets configurable. If the first configured starter pet is unset, it seeds the same logical hometown mapping:

```
elder 1 -> 2
elder 2 -> 3
elder 3 -> 4
else    -> 1
```

It then reads the configured IDs and starter-pet level. This is useful continuity evidence for the old relationship, but the configurable layer is not part of the R1 historical baseline.

## Deterministic model

- `tools/stoneage_player_birth_model.py`
- `tests/test_stoneage_player_birth_model.py`
- `.github/workflows/validate-stoneage-player-birth.yml`

The model contains:

- ordinary four-village birth state;
- spawn coordinates;
- `LASTTALKELDER`;
- origin savepoint bit;
- starter enemy ID = `hometown + 1`;
- level-1 starter-pet expectation;
- a separately named later `_UNIFIDE_MALINASI` location override.

The six regression tests cover all four mappings, coordinates, savepoint state, invalid inputs, starter ID linkage and the later unified-Malinasi override.

## Connected creation/progression chain

```
hometown selection
  -> village / elder / savepoint
  -> starter pet
  -> 20 player base-stat creation points
  -> 10 elemental creation points
  -> level-1 player growth
  -> encounter / battle / rewards
  -> level-up point spending
  -> transmigration
```

The reconstructed gameplay core now has a deterministic path beginning at the ordinary character-creation packet rather than starting mid-progression.

## Evidence status

- **FACT:** creation carries `hometown`; ordinary server validation is `0..3`.
- **FACT:** the four stable elder coordinates are 1006/2006/3006/4006 with the listed x/y values.
- **FACT:** Bismarck client code maps indices 0..3 to 萨姆吉尔、玛丽娜丝、加加、卡鲁它那.
- **FACT:** gavinlinasd and iriselia ordinary creation paths select starter enemy ID `hometown + 1` and initialize the pet for level 1.
- **FACT:** later source branches explicitly introduce unified-newbie-village and configurable-starter-pet behavior.
- **HYPOTHESIS:** the common four-village / IDs 1..4 linkage descends from the early official creation design.
- **OPEN:** direct JSS/1999 executable/data proof that these exact four spawn coordinates and enemy IDs are launch-era values.
- **OPEN:** authoritative launch enemy-table resolution of IDs 1..4 to display names.
- **OPEN:** exact chronology and commercial-version boundaries of `_UNIFIDE_MALINASI`, `_DELBORNPLACE`, museum and configurable-new-player variants.

## Next technical seam

Creation -> growth -> battle -> transmigration is now connected. The next highest-value gameplay seam should be chosen from the remaining unmodeled deterministic state transitions in the recovered 2.5/source-family corpus, with priority on systems that close an end-to-end loop rather than isolated content lists. Candidate seams include **death/revival/savepoint handling**, **capture/taming**, and **party/formation state**, after checking existing repository coverage to avoid duplicate work.
