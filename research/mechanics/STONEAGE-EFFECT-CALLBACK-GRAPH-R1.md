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

## Recovered 2.5 coverage result

The hash-pinned active recovered tables produce three materially different coherence profiles.

### Item callbacks

Active `itemset.txt` contains 13,252 rows.

The callback columns are sparse and sharply concentrated in use-time behavior:

- INIT / PREOVER / POSTOVER / WATCH: no non-empty recovered tokens;
- USE: 957 row uses, 52 unique tokens;
- ATTACH: 51 row uses, 5 unique tokens;
- DETACH: 51 row uses, 5 unique tokens;
- DROP: 40 row uses, 3 unique tokens;
- PICKUP: 2 row uses, 1 unique token;
- RELIFE: 3 row uses, 1 unique token.

Every non-USE callback token resolves in **all three** fixed descendant global dispatch tables.

USE is fully explainable by the inspected source family but is versioned:

- 36 / 52 unique USE tokens are declared in all three fixed source tables;
- 16 / 52 are present in only some fixed descendants;
- 0 / 52 are absent from all three;
- 904 / 957 USE rows use an all-three token;
- 53 / 957 USE rows use a branch-specific token.

Per fixed source snapshot, declared-source USE coverage is:

- Bismarck: 51 / 52 unique tokens, 956 / 957 row uses;
- gavinlinasd: 44 / 52 unique tokens, 930 / 957 row uses;
- iriselia: 37 / 52 unique tokens, 905 / 957 row uses.

This makes item-use behavior a **version-diff problem**, not an unresolved-data problem.

### Item USE guard + body classification

The final item pass now separates registry presence from executable common semantics.

Active recovered USE callbacks:

- 17 unique tokens / 818 rows are unguarded in all three fixed dispatch tables;
- 19 / 86 are guarded in all three;
- 16 / 53 have partial source-lineage coverage.

The 17 unguarded-dispatch candidates refine by function body to:

- **15 stable-body tokens / 816 rows**;
- **2 profession macro-shell tokens / 2 rows**;
- 0 mixed-body;
- 0 partial-body-source.

The macro shells demonstrate why registry presence alone cannot define a common core.

Stable active USE families include battle recovery/status/capture/resurrection/field attribute, warp, encounter controls, pet follow, mic toggle, rename, ordinary skill-up point, pet-owner release and ToHelos work-state effects.

The complete deterministic semantics are documented in `STONEAGE-ITEM-EFFECT-CORE-R1.md`.

### Item non-USE boundary

The active non-USE callback layer is also guard/body classified:

- ATTACH: 2 unguarded stable tokens / 5 rows; 3 guarded tokens / 46 rows.
- DETACH: 2 unguarded stable / 5; 3 guarded / 46.
- DROP: 2 unguarded stable / 5; 1 guarded / 35.
- PICKUP: 1 unguarded stable / 2; no guarded rows.
- RELIFE: 0 unguarded; 1 all-three guarded token / 3 rows.

The stable non-USE families are equipment encounter control, PickAllPet attach/detach, microphone cleanup, and dice drop/pickup state.

### Magic callbacks

Active `magic.txt` contains:

- 181 rows;
- 17 unique function tokens.

All 17 tokens and all 181 row uses resolve in **all three** fixed descendant magic dispatch tables.

This is the strongest callback-coherence result in the recovered effect layer and makes ordinary magic the best next semantic reconstruction target.

### Magic guard classification

The active recovered magic layer splits exactly along the three-source preprocessor boundary:

- 9 unique tokens / 130 rows are unguarded in all three;
- 7 unique tokens / 46 rows are guarded in all three;
- 1 unique token / 5 rows has partial source-lineage coverage;
- 0 mixed-guard tokens;
- 0 missing-all-three tokens.

The partial-source family is `MAGIC_AttSkill`: its entries are commented out in the fixed gavin/iriselia dispatch tables and macro-gated in the fixed Bismarck table. The nine unguarded callbacks remain the basis for the separate ordinary-magic semantic model in `STONEAGE-MAGIC-EFFECT-CORE-R1.md`.

### Pet-skill callbacks

Active `petskill.txt` contains:

- 147 rows;
- 69 unique function tokens.

Textual fixed-source coverage:

- 65 unique tokens / 143 rows resolve in all three fixed source tables;
- 4 unique tokens / 4 rows resolve in none of the three fixed source tables;
- no active token is merely branch-specific in this comparison.

After comment-aware dispatch-guard classification:

- **15 unique tokens / 33 rows** are unguarded in all three fixed source lineages;
- **50 tokens / 110 rows** are guarded in all three;
- 0 mixed-guard;
- 0 partial-source;
- 4 all-source-missing / 4 rows.

Substantive body classification of the 15 unguarded candidates is equally clean:

- **15 stable-body tokens / 33 rows**;
- 0 macro shells;
- 0 mixed-body;
- 0 partial-body-source.

The stable active families are:

- none / ordinary attack / ordinary guard;
- continuation attack;
- charge attack;
- guardian;
- power balance;
- mighty;
- ordinary status change;
- earth round;
- guard break;
- abduct;
- steal;
- merge;
- no-guard.

Therefore the former “65 all-three matches” figure is a **source-coverage fact, not a common-core boundary**. The deterministic semantic target is the 15-token / 33-row stable subset.

The four unmatched recovered pet-skill records remain classified as **recovered-data / inspected-source skew** until another source snapshot explains them. They are not assigned invented behavior and are not promoted into the historical baseline.

### Resulting work order

The callback join itself is now closed at R1.

Semantic reverse engineering should proceed in evidence-quality order:

1. ordinary magic effect families — reconstructed for the nine all-three unguarded callbacks;
2. common item effects — reconstructed for 15 stable active USE callbacks plus all stable non-USE hooks, with two profession macro-shell USE rows kept versioned;
3. pet-skill callbacks — dispatch/body boundary now closed at 15 stable active tokens / 33 rows; reconstruct these 15 before any guarded extension;
4. quarantine the four all-source-missing pet-skill records until a matching source/client lineage is recovered.

## Evidence boundaries

- **FACT:** item callback strings resolve through the global function registry.
- **FACT:** item use/equip/pickup paths consume the resolved item callback slots.
- **FACT:** recovered active item -> magic-ID references already resolve completely into the recovered active magic table.
- **FACT:** magic function strings resolve through `MAGIC_functbl[]`; unresolved ordinary magic dispatch returns FALSE.
- **FACT:** pet-skill function strings resolve through `PETSKILL_functbl[]`; unresolved pet-skill dispatch returns FALSE.
- **FACT:** recovered active pet-skill IDs cover the active enemybase skill-ID domain.
- **BOUNDARY:** source-table token presence is declared-source coverage, not compiled-active proof.
- **FACT:** recovered active magic callback coverage is complete across all three fixed source tables.
- **VERSIONED:** recovered item USE callbacks include 16 tokens present in only a subset of the fixed source lineages; none is absent from all three.
- **SPECIMEN SKEW:** four recovered active pet-skill function tokens, each used by one row, are absent from all three fixed source tables.
- **OPEN:** exact launch/JSS callback inventory until an earlier clean source/binary/data specimen is recovered.

## Next seam

Coverage classification is now complete. Next priority: reconstruct the **ordinary magic effect core** first, because all 17 recovered magic callback tokens resolve across all three fixed source tables. Then proceed to common item effects and common pet-skill effects, keeping branch-only item USE callbacks and the four unresolved pet-skill rows explicitly versioned/quarantined.
