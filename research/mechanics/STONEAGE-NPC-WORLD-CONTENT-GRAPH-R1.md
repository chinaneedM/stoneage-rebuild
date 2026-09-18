# StoneAge NPC / World-Content Graph R1

Status: **source-verified descendant structural core; recovered 2.5 aggregate probe attached separately**  
Scope: generic server NPC loading and generation pipeline, not the semantic contents of every NPC script/config file.

## Why this seam matters

The recovered server corpus contains thousands of NPC-side files. Treating that directory as one flat data set would mix several different layers:

```
recursive NPC directory
  -> NPCTEMPLATE magic files
  -> NPCCREATE magic files
  -> create block references template by name
  -> create block contributes floor/born/move/time/count + per-reference argument
  -> template contributes graphics/default stats + function dispatch
  -> runtime generator chooses a legal point
  -> CHAR_initCharOneArray runs INITFUNC
  -> NPC-specific callback code interprets the attached argument/config
```

This is the server-authoritative world-content assembly path observed in the fixed descendant source.

## Generic load order

All three fixed descendants preserve the same high-level loader:

1. maps are initialized first;
2. `NPC_readNPCSettingFiles(npcdir, npctemplatenum, npccreatenum)` runs;
3. it recursively discovers files under `npcdir`;
4. it loads every valid template file first;
5. it then loads every valid create file.

This ordering matters because create parsing validates map floor IDs and resolves template references immediately.

## File identity is magic-based, not extension-based

The generic loader does not trust `.template` or `.create` extensions.

A template file is identified by first-line magic:

```
NPCTEMPLATE
```

A create file is identified by:

```
NPCCREATE
```

Backup/temporary names are excluded by the fixed loader checks. Therefore extension counts are useful inventory metadata, but **first-line magic is the authoritative generic format discriminator**.

No generic textual `include` directive was found in these two core parsers. The generic composition relationship is recursive file discovery plus create -> template references. Additional `.arg`, `.conf`, plain files and similar material are secondary, function-specific content surfaces, not files automatically included by the generic template/create parser.

## Template role

A template block can define:

- template identity and displayed name;
- default graphic/type;
- HP/MP/STR/TOUGH ranges;
- flying/no-body/no-see generation flags;
- item/gold payload rows;
- loop interval;
- a `functionset`;
- direct per-event callback names.

The function-set table supplies a bundle of callback names for slots such as:

- init;
- pre/post walk;
- pre/post over;
- watch;
- loop;
- dying;
- talked;
- attacked;
- off/looked/item-put;
- special/window talked.

The generator first copies the selected `functionset`, then copies any non-empty direct callback fields from the template.

Therefore:

> **direct template callback entries override the corresponding function-set slot.**

The static function-set table itself contains both old/common classes and later feature classes. A class being present or even compile-unguarded in a descendant source is **not** sufficient proof that it existed in the 1999/JSS baseline.

## Create role

A create block supplies world-placement and instance policy:

- floor ID;
- born rectangle (center/size or corner/corner form);
- optional movement rectangle;
- direction;
- optional graphic/name overrides;
- respawn time;
- population cap;
- boundary / ignore-invincible flags;
- optional later fields;
- one or more `enemy=TemplateName|Argument` references.

The fixed structure allocates eight template/argument slots per create block.

Template lookup is by case-insensitive template name after hashing. If a reference does not resolve, that reference is skipped. A create block with no surviving template reference is rejected.

Create parsing also rejects a block when:

- its floor ID does not exist in the already loaded map set;
- no born area is defined.

If no movement rectangle is defined, movement bounds default to the born bounds.

## Eight-reference capacity hazard

The fixed create structure contains:

```
templateindex[8]
arg[8]
```

but the old parser checks the incoming index with a `<= arraysizeof(...)` condition rather than a strict `<`.

That means a ninth resolved template reference can pass the source check and attempt an out-of-bounds write.

R1 does **not** emulate memory corruption. The recovered probe instead counts any create block with more than eight resolved references as a source-capacity hazard.

## Runtime construction order

For each eligible create/template pair, the generator:

1. chooses a spawn point inside the create born area under body/visibility/flying constraints;
2. builds a default `Char` from the template type;
3. writes floor/x/y/direction;
4. applies template graphic/name and create-level overrides;
5. copies the function-set callbacks;
6. applies direct callback overrides;
7. attaches the per-reference create argument as `CHAR_NPCARGUMENT`;
8. sets the initial generic which-type field and create-index linkage;
9. creates item/gold payloads where configured;
10. calls `CHAR_initCharOneArray`.

`CHAR_initCharOneArray` resolves the configured INITFUNC name and calls it **before** the character slot is finalized and its runtime function pointers are constructed.

This explains why the generic generator can begin from one generic NPC/enemy-like shell while the INITFUNC specializes the object into Warp, SavePoint, Healer, Shop and other concrete NPC behaviors.

## Generation loop

The create rule also owns:

- desired population cap;
- current generated count;
- respawn interval;
- retry timing.

The ordinary generator loops create rules and their referenced templates and attempts new creation only when the time/population gate passes.

A source-version divergence is preserved:

- gavinlinasd / iriselia reset the create timer before the actual generation attempt;
- the inspected Bismarck revision moves timer reset to the successful-generation branch and adds more explicit failure classification.

A failed no-position/full-array attempt therefore does not necessarily have identical retry timing across descendants.

## Generic graph versus NPC-specific secondary content

The generic graph ends at:

```
create rule
 -> template
 -> function dispatch
 -> opaque NPC argument
 -> generated world object
```

After INITFUNC/TALKED/etc. dispatch, each NPC class can interpret its argument differently and can load/use additional `.arg`, `.conf`, menu, event or plain text files.

Those secondary dependencies must be reconstructed class-by-class. They should **not** be guessed from filename extensions alone.

This creates a clean two-stage archaeology plan:

1. reconstruct the generic world graph deterministically;
2. then resolve secondary content edges for early/core NPC classes only.

## Recovered probe

Artifacts:

- `tools/stoneage_npc_world_graph_probe.py`
- `tests/test_stoneage_npc_world_graph_probe.py`
- `.github/workflows/probe-stoneage-25-npc-world-graph.yml`

The probe scans the hash-pinned recovered bundle transiently and commits only aggregate metadata:

- template/create magic-file counts;
- template/create block counts;
- duplicate template-name counts;
- create -> template reference totals/resolution failures;
- argument-presence counts;
- map-floor validation counts;
- function-set distribution;
- direct callback override-slot counts;
- resolved references per create block;
- more-than-eight-reference hazard count;
- aggregate corpus hash.

It does **not** publish NPC names, dialogue, concrete arguments, coordinates or original rows.

## Recovered 2.5 aggregate result

The hash-pinned preservation specimen produced a structurally coherent generic NPC graph:

- 2,205 files under the recovered NPC directory;
- 49 magic-identified template files containing 131 template blocks;
- 116 unique template-name values, with 8 duplicated names and 15 extra duplicate blocks;
- 187 magic-identified create files containing 4,985 create blocks;
- all 4,985 create blocks define a born area;
- all 4,985 template references resolve;
- all 4,985 create blocks reference exactly one template;
- all 4,985 create floors resolve to the recovered server map-ID set;
- 4,825 create references carry a non-empty NPC argument;
- 633 distinct effective floor candidates are represented;
- no recovered create block exercises the old more-than-eight-reference capacity hazard;
- no recovered template block uses a direct per-event callback override; 130/131 use a function-set token.

This means the recovered generic create -> template -> map linkage is much more internally coherent than the previously observed enemy/group/encounter snapshot mismatch.

### Duplicate-template ambiguity is operational

The duplicate template names are not all inert archive leftovers.

The enhanced probe found:

- 3 duplicated template-name values are actually referenced by create blocks;
- 30 create blocks reference one of those duplicated names.

`NPC_templateGetTemplateIndex` scans the loaded template array from the beginning and returns the first matching name. Therefore these 30 bindings can depend on template load order if the duplicated definitions differ.

R1 does not choose one duplicate as canonical. This is preserved as a **load-order ambiguity / specimen-integrity risk** to resolve against a cleaner comparison artifact.

### Function-set source/data skew

The recovered templates use 58 distinct non-empty function-set tokens.

Cross-checking those tokens against the static `functionSet[]` tables in the three fixed descendant source revisions shows:

- 44/58 recovered tokens are present in each fixed source table;
- 13 recovered tokens are absent from **all three** fixed source tables;
- `Raceman` is present in the gavinlinasd/iriselia source family but absent from the fixed Bismarck table;
- `VipShop` is present in the fixed Bismarck table but absent from the fixed gavinlinasd/iriselia tables.

The 13 all-source-missing tokens are retained in the derived analysis only as an aggregate mismatch class; their presence proves that the recovered NPC data and the three fixed public source snapshots are not one exact source/data build.

This is another **cross-version preservation skew**, not evidence that the missing functions were broken in the historical commercial game and not evidence that any one descendant source is the canonical implementation for this 2.5 data set.

## Evidence boundaries

- **FACT:** generic NPC files are recursively discovered and magic-identified.
- **FACT:** templates load before create records.
- **FACT:** create blocks reference templates by name and attach one argument string per reference.
- **FACT:** map floor existence and born-area presence are create-load gates.
- **FACT:** function-set callbacks are copied before direct callback overrides.
- **FACT:** INITFUNC executes during `CHAR_initCharOneArray`.
- **FACT:** the fixed create structure has eight template/argument slots.
- **SOURCE HAZARD:** the old reference-count guard can admit a ninth resolved reference.
- **VERSIONED:** retry-timer ordering differs in the inspected newer Bismarck branch.
- **OPEN:** exact launch-era NPC content population and which descendant function classes were already present in JSS 1999.
- **SPECIMEN SKEW:** 13 recovered function-set tokens are absent from all three fixed descendant source tables; the data/source snapshots are not one exact build.\n- **LOAD-ORDER RISK:** 30 recovered create blocks reference 3 duplicated template-name values, while lookup returns the first loaded match.\n- **OPEN:** class-specific secondary file dependencies until each early/core NPC class is audited.\n
## Next seam

The generic NPC/world graph is now closed at R1. Preserve the duplicate-name and function-set source/data mismatches as comparison targets.\n\nNext priority: **item / magic / pet-skill effect callback joins** — measure whether function tokens in the recovered active tables resolve in the fixed descendant dispatch tables, without repeating the already completed table-schema probes.\n