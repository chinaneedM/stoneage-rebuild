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
- **OPEN:** class-specific secondary file dependencies until each early/core NPC class is audited.

## Next seam

After the recovered graph aggregate is available, use its active function-set distribution to prioritize **early/core secondary content edges** rather than parsing every later event/profession/family subsystem.

Then proceed to remaining item/skill effect callback joins.
