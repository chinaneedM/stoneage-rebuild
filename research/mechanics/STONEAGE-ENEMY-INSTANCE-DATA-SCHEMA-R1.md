# StoneAge Enemy Instance Data Schema R1

Status: **source-verified descendant schema; recovered 2.5 specimen to be probed by CI**  
Scope: server `enemy.txt` / `enemy2.txt` as concrete enemy-instance definitions and their link to `enemybase.txt`.

## Data-layer role

The preserved server has three distinct encounter data layers:

```
enemybase.txt
  template/species stats, growth, elements, pet skills
        ↓ TEMPNO
enemy.txt
  concrete enemy variant: level range, AI, EXP/drop/capture/style overrides
        ↓ ENEMY_ID
group.txt
  weighted composition of up to 10 enemy variants
        ↓ GROUP_ID
encount.txt
  map/coordinate encounter areas and weighted groups
```

This is a server-authoritative chain. Client battle-map assets are presentation/input-side data and must not replace it.

## Source-verified enemy row schema

Across the fixed BismarckDD, gavinlinasd and iriselia descendants, the common integer fields are:

```
ID
TEMPNO
LV_MIN
LV_MAX
CREATEMAXNUM
CREATEMINNUM
TACTICS
EXP
DUELPOINT
STYLE
PETFLG
ITEM1..ITEM10
ITEMPROB1..ITEMPROB10
```

That is 31 integers.

The common prefix has two strings:

1. enemy name;
2. tactics option string.

When `_BATTLENPC_WARP_PLAYER` is enabled, a third string `ACT_CONDITION` is inserted before the integer fields. All three fixed inspected descendants enable this macro, so their active schema expects 34 CSV fields rather than the 33-field common base.

The probe supports both layouts so it can classify preservation specimens without forcing a later extension onto earlier data.

## TEMPNO resolves to enemybase

During `ENEMY_initEnemy`, every accepted row resolves `ENEMY_TEMPNO` against `enemybase.txt:E_T_TEMPNO`.

If no template exists, that enemy row is rejected from the effective loaded table.

Therefore `enemy.txt` is not an independent species table. It is a variant/instance configuration over the base template.

## Level normalization

The loader applies:

```
if LV_MIN == 0:
    LV_MIN = LV_MAX

stored_min = min(LV_MIN, LV_MAX)
stored_max = max(LV_MIN, LV_MAX)
```

Thus reversed nonzero ranges are normalized rather than rejected, and zero minimum means a fixed level equal to the maximum.

## Encounter-count fields

`CREATEMAXNUM` is actively read by `ENEMY_getEnemy`.

It contributes to the total possible enemy count for the chosen group and caps how many copies of that concrete enemy variant can occupy one generated encounter.

By contrast, this audit found `CREATEMINNUM` declared and loaded in all three fixed lineages but no runtime read outside the table definition. It is therefore recorded as a **declared/dormant field** rather than being asserted to enforce a minimum spawn count.

## AI fields

On concrete enemy creation:

```
CHAR_WORKTACTICS = ENEMY_TACTICS
CHAR_WORKBATTLE_TACTICSOPTION = ENEMY_TACTICSOPTION
```

and the optional action-condition string is copied to its battle WORK field.

The battle AI reads these runtime fields. Thus AI configuration belongs to the concrete enemy variant layer, not the base pet template.

## EXP and duel point

The created enemy receives:

```
CHAR_DUELPOINT = ENEMY_DUELPOINT
```

When `ENEMY_DUELPOINT <= 0`:

- if `ENEMY_EXP != -1`, that value directly becomes `CHAR_EXP`;
- otherwise the server calculates EXP from level/template rank using the enemy EXP formula.

This confirms the existing progression bridge:

```
enemy.txt EXP override/default calculation
 -> spawned CHAR_EXP
 -> battle level-gap reward adjustment
 -> accumulated progression
```

`DUELPOINT` therefore changes the reward mode boundary and should not be treated as another EXP column.

## STYLE

`ENEMY_STYLE` selects an equipment-style weapon template when the enemy object is created.

The fixed code maps style codes 1..7 to weapon item template numbers, equips the item in `CHAR_ARM`, and then runs character parameter compliance.

Therefore STYLE can affect both rendered equipment and derived combat parameters. R1 records it as an enemy-instance equipment style code; exact historical item-template meanings remain version/data dependent.

## Capture flag

`ENEMY_PETFLG` is copied to the spawned enemy's `CHAR_WORK_PETFLG`.

This is the concrete encounter's "may become/capture as pet" gate, distinct from the base template's own `E_T_PETFLG` validity/holdability field.

The rebuild must keep those two gates separate.

## Drops

Each row has up to 10 item slots paired with 10 probability fields.

The drop routine iterates the pairs and, in the fixed `_FIX_ITEMPROB` path, tests:

```
RAND(0, 999) < ITEMPROB
```

before creating the configured item.

Therefore a probability domain of 0..1000 is expected for that path; the recovered probe reports aggregate out-of-range counts without publishing item IDs.

Later drop restrictions/modifiers remain separate.

## Group relationship

`group.txt` references `enemy.txt` by `ENEMY_ID`, not by TEMPNO.

The group loader resolves each of up to 10 enemy IDs to an enemy-array row, rejects a group with no valid enemies, and rejects duplicate enemy IDs within a group.

At encounter generation, group CREATEPROB values are weights for choosing among the resolved enemy variants. `CREATEMAXNUM` then limits repeated concrete variants.

This makes the correct identity chain:

```
enemybase TEMPNO <- enemy TEMPNO
enemy ID <- group enemy slots
group ID <- encount group slots
```

## Provenance-preserving recovered probe

Artifacts:

- `tools/stoneage_enemy_instance_probe.py`
- `tests/test_stoneage_enemy_instance_probe.py`
- `.github/workflows/probe-stoneage-25-enemy-instances.yml`

The workflow re-fetches the already-verified preservation bundle by pinned hashes, extracts it ephemerally, and commits only a derived report.

The report deliberately excludes:

- enemy names;
- tactics strings;
- action-condition strings;
- item IDs;
- original table rows.

It emits hashes, row/field counts, numeric ranges/distributions, template-reference integrity and drop-slot aggregate statistics.

## Evidence status

- **FACT:** enemy.txt is loaded by the game server and is authoritative for concrete enemy variants.
- **FACT:** 31 common integer fields are stable across all three fixed descendant headers.
- **FACT:** common schema is two strings + 31 integers; the enabled warp-NPC extension adds one string before the integers.
- **FACT:** TEMPNO must resolve to an enemybase template or the row is rejected.
- **FACT:** level ranges are normalized as described above.
- **FACT:** CREATEMAXNUM is used to constrain encounter multiplicity.
- **FACT:** no runtime use of CREATEMINNUM was found in the three fixed lineages.
- **FACT:** TACTICS and TACTICSOPTION are copied into battle AI runtime state.
- **FACT:** EXP can explicitly override calculated enemy EXP when DUELPOINT <= 0.
- **FACT:** STYLE can equip a weapon template before parameter recomputation.
- **FACT:** PETFLG is copied to the spawned enemy's capture gate.
- **FACT:** ten drop item/probability pairs exist.
- **OPEN:** exact JSS-1999 enemy table contents and whether the third action-condition string existed.
- **OPEN:** historical meaning/intended use of the loaded-but-unread CREATEMINNUM field.
- **OPEN:** exact commercial chronology of style/drop/AI extensions.

## Next seam

After the recovered enemy-instance report is generated, analyze `group.txt` and then `encount.txt` so the entire authoritative chain from map coordinate to concrete spawned enemy can be reconstructed quantitatively.
