# StoneAge Item / Magic / Pet-Skill Effect Callback Graph R1

Status: **fixed-descendant dispatch architecture verified; recovered-token coverage probed separately**  
Scope: joins from recovered item/magic/pet-skill records to executable callback dispatch. This report does not re-derive the already completed table schemas.

## Purpose

The recovered tables already establish:

- itemset record structure and item -> magic-ID joins;
- magic record structure;
- pet-skill record structure and enemybase -> pet-skill-ID coverage.

The remaining deterministic question is different:

> when an active data record names an effect function, does that token resolve to executable behavior in the fixed descendant source tables?

R1 therefore models three callback surfaces separately.

## Item callbacks

The recovered 94-column item schema contains callback-string columns for:

- init;
- pre-over;
- post-over;
- watch;
- use;
- attach;
- detach;
- drop;
- pickup;
- relife.

Concrete item creation copies those strings into the item instance and resolves INITFUNC through the global `getFunctionPointerFromName` table.

`ITEM_constructFunctable` then resolves every ordinary item callback slot through that same global string -> pointer registry.

Observed runtime users include:

- `CHAR_ItemUse` -> `ITEM_USEFUNC`;
- equipment attach -> `ITEM_ATTACHFUNC`;
- equipment detach -> `ITEM_DETACHFUNC`;
- item pickup -> `ITEM_PICKUPFUNC`;
- corresponding drop/watch/over paths use their own resolved slots.

If an item callback token is absent from the global registry, its stored pointer is NULL and the caller-specific behavior determines the resulting no-op/failure path.

This is different from magic and pet-skill dispatch: items share the broad global function registry that also contains NPC/core callbacks.

## Item -> magic join

Items can also carry `ITEM_MAGICID`.

The existing real-byte schema probe already established that, in active recovered `itemset.txt`:

- 8,015 item rows carry a parsed magic reference;
- 146 distinct magic IDs are referenced;
- all 146 resolve into the recovered active magic table.

Thus R1 does not repeat magic-ID referential-integrity work. It begins at the magic record's function token.

## Magic callbacks

`MAGIC_initMagic` loads the textual function token stored in each magic record.

Magic execution performs:

```
item -> ITEM_MAGICID
     -> MAGIC_getMagicArray
     -> MAGIC_FUNCNAME
     -> MAGIC_getMagicFuncPointer
     -> effect callback
```

`MAGIC_getMagicFuncPointer` uses a dedicated static `MAGIC_functbl[]` with hash + exact string comparison.

If the function token does not resolve, ordinary `MAGIC_Use` returns FALSE rather than inventing a fallback effect.

The magic callback registry is therefore an authoritative executable join distinct from the item global callback registry.

## Pet-skill callbacks

Pet skills use another dedicated dispatch table, `PETSKILL_functbl[]`.

The runtime path is:

```
pet's learned skill ID
 -> PETSKILL_getPetskillArray
 -> PETSKILL_FUNCNAME
 -> PETSKILL_getPetskillFuncPointer
 -> pet-skill effect callback
```

Lookup again uses hash + exact string comparison.

If the function token cannot be resolved, `PETSKILL_Use` returns FALSE.

The previously recovered active `petskill.txt` covers all 111 pet-skill IDs referenced by active `enemybase.txt`; R1 measures the next join, from those data records to declared executable callbacks.

## Why source-table coverage is version evidence, not compiled-runtime proof

The three pinned public descendant revisions contain compile-time feature guards around many dispatch entries.

The R1 coverage probe intentionally parses **declared table entries in the fixed source text**. Therefore:

- token present in all three source tables = strong descendant-lineage coverage;
- token present in only some = explicit source-version divergence;
- token absent from all three = recovered-data / inspected-source mismatch;
- token textually present behind a disabled macro is still only declared-source evidence, not proof that the fixed binary would contain it.

This conservative boundary avoids pretending that unbuilt source branches are active runtime behavior.

## Probe design

Artifacts:

- `tools/stoneage_effect_callback_coverage_probe.py`
- `tests/test_stoneage_effect_callback_coverage_probe.py`
- `.github/workflows/probe-stoneage-25-effect-callback-coverage.yml`

The workflow transiently combines:

1. the hash-pinned recovered 2.5 server data;
2. fixed gavinlinasd source revision;
3. fixed iriselia source revision;
4. fixed Bismarck source revision.

For each callback surface it records only aggregate counts:

- non-empty callback row uses;
- unique data tokens;
- tokens covered by all three source tables;
- tokens covered by some but not all;
- tokens covered by none;
- per-lineage matched-token/use counts;
- SHA-256 of the hidden token-to-coverage classification.

It does **not** publish original item/magic/pet-skill names, callback tokens, descriptions, options, or data rows.

## Evidence boundaries

- **FACT:** item callback strings resolve through the global function registry.
- **FACT:** item use/equip/pickup paths consume the resolved item callback slots.
- **FACT:** recovered active item -> magic-ID references already resolve completely into the recovered active magic table.
- **FACT:** magic function strings resolve through `MAGIC_functbl[]`; unresolved ordinary magic dispatch returns FALSE.
- **FACT:** pet-skill function strings resolve through `PETSKILL_functbl[]`; unresolved pet-skill dispatch returns FALSE.
- **FACT:** recovered active pet-skill IDs cover the active enemybase skill-ID domain.
- **BOUNDARY:** source-table token presence is declared-source coverage, not compiled-active proof.
- **OPEN:** exact launch/JSS callback inventory until an earlier clean source/binary/data specimen is recovered.

## Next seam

Use the real-byte callback coverage result to separate:

1. coherent early/core callback families that can now be analyzed semantically;
2. branch-specific later callback families;
3. data/source mismatches that must remain provenance defects rather than reconstructed rules.

Only after that classification should detailed item/magic/pet-skill effect formulas be expanded.
