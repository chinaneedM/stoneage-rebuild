# StoneAge ExChangeMan Condition / Secondary-Argument Core R1

Status: fixed-descendant deterministic reconstruction; recovered-use distribution still to be measured.

Scope: the common ExChangeMan secondary argument loader, EVENT condition language, stable condition atoms, cost calculation, and NpcWarp destination selection. Reward/deletion/accept mutation semantics are deliberately deferred to the next seam.

## Why this is a real secondary configuration edge

The generic NPC graph ends with NPCCREATE attaching an opaque CHAR_NPCARGUMENT. ExChangeMan interprets that secondary payload as a small event language.

The pinned descendants establish this chain:

NPCCREATE enemy=Template|file:path/to/file.arg
-> CHAR_NPCARGUMENT contains file:...
-> NPC_Util_CheckAssignArgFile finds the first argument token containing file
-> NPC_Util_MargeStrFromArgFile reads npcdir/path/to/file.arg
-> line endings are removed and lines are joined by pipe separators
-> NPC_Util_GetArgStr returns the merged text
-> ExChangeMan parses EventEnd blocks and EVENT expressions

If no file token is found, NPC_Util_GetArgStr returns the inline CHAR_NPCARGUMENT instead.

Therefore .arg is not promoted here as a universal data format. It is a class-consumed secondary configuration edge reached through the common NPC argument helper.

## Fixed-source controls

The common core was checked against the three pinned descendant revisions already used by this project:

- gavinlinasd/StoneAge at 1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56
- iriselia/StoneAge at 9e6c8ce2cd8ed532a7157773acd1c61582c178b5
- BismarckDD/stoneage at 999ffdf1d220ec6666eb65339180689c9caf1876

Primary surfaces are npcutil.c, npc_exchangeman.c and npctemplate.c. Later compile-gated mission, profession and extended-event additions are excluded from R1.

## Argument lookup behavior

NPC_Util_GetStrFromStrWithDelim splits by pipe, takes the first token for which substring search finds the requested key, then splits that token by colon and returns the second field.

This is not exact-key parsing. A longer key containing the requested text can shadow a later exact key. The reference model preserves that behavior.

## EVENT expression structure

NPC_ExChangeManEventCheck treats comma-separated branches as OR. Ampersand-separated terms inside one comma branch are AND. It returns the one-based index of the first satisfied comma branch, not merely true or false. Later mutation code can reuse that selected branch index.

Before later compile-gated extensions, the stable condition dispatcher recognizes LV, ITEM, ENDEV, NOWEV, SP, TIME, IMAGE and PET/PETEV terms.

## Item slot domains

Simple ITEM equality scans only carried inventory slots starting at CHAR_STARTITEMARRAY, so equipped slots are excluded. ITEM=N succeeds if a carried item has N. ITEM!=N succeeds only when no carried item has N, including an empty carried inventory.

The less-than and greater-than ITEM paths never have a final success return; ITEM<N and ITEM>N therefore cannot become true in the observed core.

Under the equality branch, any expression containing an asterisk is diverted to NPC_EventReduce. The right side is parsed as item_id*required_count. This path scans item slots from zero, so it includes equipment, and it counts ITEM_USEPILENUMS when nonzero, otherwise one.

The old dispatch tests the asterisk before validating the left token, so OTHER=50*2 also reaches the item-quantity routine. R1 preserves this source behavior.

## PET / PETEV conditions

PET terms are dispatched whenever PET occurs in the term. The helper expects a level expression followed by hyphen, then pet ID and optional required count. EV anywhere in the term selects pets whose CHAR_ENDEVENT is one; otherwise zero.

Matching requires pet base ID, event mode, level relation, optional use-name equality when Pet_Name checking is enabled, and the requested number of pets.

The PET helper checks less-than, then greater-than, then equality. It has no distinct not-equal branch, so a PET term containing != reaches equality handling.

## Event flags, save point, level and image quirks

ENDEV=N checks the completed-event bit and ENDEV!=N is its normal negation. SP=N checks save-point bit N and SP!=N checks absence. For ENDEV and SP, less-than and greater-than collapse to ordinary bit-presence behavior rather than numeric comparison.

NOWEV has a source defect: NOWEV!=N returns true whether the current-event bit is set or clear.

NPC_EventLevelCheck reverses the shared not-equal result again. Consequently LV!=N succeeds when the current level equals N and fails when it differs.

NPC_ImageCheck passes its operands to the shared comparison helper in reverse order. Equality is normal, but IMAGE<N succeeds when the current image value is greater than N, while IMAGE>N succeeds when it is less than N.

TIME uses the current game LSTIME value and the ordinary comparison helper.

## Cost and NpcWarp

NPC_EventGetCost treats any cost text containing LV as level times the multiplier after an asterisk; otherwise it uses ordinary integer conversion.

NpcWarp is a comma-separated list of floor.x.y destinations. CHAR_WORK_EVENTWARP is a one-based NPC-local cursor. Successful selection stores the next position; a later call wraps to the first entry after the end. Malformed entries are skipped.

A critical implementation detail is preserved: the inspected fixed sources call CHAR_warpToSpecificPoint with meindex, the ExChangeMan NPC index, not the talking player index. R1 therefore records this as NPC-object warp behavior in the inspected source. It must not be silently rewritten into player teleport semantics without separate evidence.

## Deterministic artifacts

- tools/stoneage_exchangeman_condition_model.py
- tests/test_stoneage_exchangeman_condition_model.py
- .github/workflows/validate-stoneage-exchangeman-condition.yml

The suite covers secondary argument-file merge, substring field lookup, OR/AND branch selection, level and item conditions, pile/equipment quantity checks, event/save-point bits, the NOWEV defect, reversed IMAGE relations, PET/PETEV count/name behavior, level-scaled costs and round-robin NpcWarp selection.

## Recovered 2.5 usage closure

The hash-pinned 2.5 preservation specimen confirms that ExChangeMan is heavily active rather than merely source-capable:

- 315 unambiguous ExChangeMan create references, all 315 using resolved secondary argument files;
- 1,429 non-empty EventEnd blocks, of which 1,424 contain EVENT conditions;
- 298 condition blocks use comma-separated OR and 6,434 condition terms occur inside ampersand-AND branches;
- active condition-family blocks include ITEM 1,002, LV 697, ENDEV 484, NOWEV 358, PET 78, TIME 20 and SP 4;
- the specimen contains **2 ITEM relational (< or >) terms**, so the source's never-success ITEM relational bug is live data behavior;
- it contains **1 NOWEV!= term**, so the source's tautological NOWEV-not-equal bug is also live;
- it contains zero LV!=, zero PET!= and zero IMAGE relational terms, so those source quirks are dormant in this recovered ExChangeMan corpus;
- the ExChangeMan argument corpus aggregate is `e87df922d8172bb11d9f41d42011f26028f536c0032a592f155c5da38af67901`.

The aggregate report is `research/recovered/STONEAGE-25-EXCHANGEMAN-USAGE-R1.txt`; it retains no NPC names, dialogue, concrete IDs, paths, coordinates or original argument rows. Probe run `35378522791` completed successfully.

This closes the common ExChangeMan condition seam for the fixed descendants plus the recovered 2.5 specimen. Exact 1999/JSS behavior remains separately open pending an earlier clean artifact.

## Evidence status

FACT (fixed descendants): file-based secondary NPC arguments are merged into pipe-delimited text before class parsing.

FACT (fixed descendants): ExChangeMan EVENT uses comma OR, ampersand AND, and returns the first matching one-based branch index.

FACT (fixed descendants): the stable condition set contains LV, ITEM, ENDEV, NOWEV, SP, TIME, IMAGE and PET/PETEV behavior.

SOURCE QUIRK: LV!=N behaves as level equality.

SOURCE QUIRK: NOWEV!=N is always true.

SOURCE QUIRK: ITEM<N and ITEM>N never succeed.

SOURCE QUIRK: IMAGE less-than/greater-than semantics are reversed by operand order.

SOURCE QUIRK: PET != falls through to equality handling.

SOURCE QUIRK: NpcWarp calls the warp primitive with the NPC index.

VERSIONED: later compile-gated mission, profession and extended predicates are not part of the common R1 core.

FACT (recovered 2.5): ITEM relational and NOWEV-not-equal source quirks are exercised by the preserved corpus; LV-not-equal, PET-not-equal and IMAGE relational quirks are not exercised there.

OPEN: exact 1999/JSS presence and content until cleaner early data is recovered.

## Next seam

ExChangeMan R1 is closed for the fixed descendant core plus the recovered 2.5 usage surface. The next data-driven secondary-argument target is NPCEnemy, whose recovered unambiguous queue contains 279 file-backed create references and directly bridges event conditions, item gates, battle creation and post-battle state/warp behavior.
