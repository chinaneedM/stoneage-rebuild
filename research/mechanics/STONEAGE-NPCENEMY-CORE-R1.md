# StoneAge NPCEnemy Core R1

Status: active recovered-data-driven deterministic reconstruction.

Scope: common NPCEnemy secondary-argument paths that are source-stable and materially reachable in the hash-pinned recovered 2.5 specimen. General combat formulas remain delegated to the already closed battle layer.

## Evidence controls

Fixed descendant source revisions:

- gavinlinasd/StoneAge at 1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56
- iriselia/StoneAge at 9e6c8ce2cd8ed532a7157773acd1c61582c178b5
- BismarckDD/stoneage at 999ffdf1d220ec6666eb65339180689c9caf1876

Recovered specimen:

- bundle SHA-256 d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5
- NPCEnemy argument aggregate SHA-256 7ad24c5b0ebd38ed4ef2e3efbdaaa61ea61be6e19cf40fac65d7765f590e0379
- real-byte usage workflow run 35379672528: success
- 279 NPCEnemy create refs, all 279 file-backed and resolved

## Recovered active surface

The specimen splits into 200 gym-mode blocks and 79 normal-mode blocks.

All 279 normalize to entype=2, so both walking collision and direct talk are accepted by recovered configuration even though source supports narrower modes.

dieact normalizes to 1 in 250 blocks and to 0 in 29 blocks. onebattle is present in 23 blocks but only 10 normalize to the exclusive value 1.

Other active surfaces include 78 askbattle prompt blocks, 18 item-gate blocks, one steal block, 20 explicit revival-time blocks, 250 start-message blocks and 7 end-message blocks.

Two blocks contain NEWNPCENEMY. They contain five non-empty OVER segments and three NEWEVENT segments; all three NEWEVENT segments carry FREE and WARP. Recovered FREE terms use only ENDEV, EQUIT, LV and NOWEV. No recovered CHECKPARTY or NEW_ACTION mutation key was observed.

The recovered corpus has no active noitem, B_evend, B_evnow, REPLACEMENT, sktype or herobattlefield key.

## Encounter trigger semantics

NPC_NPCEnemy_Encount rejects a hidden NPC whose base image is zero.

entype 0 means walk/event collision only, 1 means talk only, and 2 accepts either path.

The item gate requires every configured item ID to be found somewhere in the player's item slots. Each configured requirement performs a fresh full scan, so duplicate requirement IDs could reuse the same physical item rather than requiring multiple copies. Recovered item lists contain no duplicates, so this quirk is dormant there.

onebattle=1 scans active battles and rejects entry when another battle createindex equals this NPC.

Party clients have a notable source behavior: after all gates pass, the function skips the entire prompt/BattleIn block when CHAR_WORKPARTYMODE is CHAR_PARTY_CLIENT, yet returns the still-true local flag. The party leader is expected to drive actual battle entry.

If askbattlemsg1 exists for a non-client path, the NPC sends the Yes/No prompt and returns false without starting battle. A later Yes window callback invokes BattleIn.

## Normal enemy-group construction

Non-gym battles call NPC_Util_getEnemy.

Only the first ten enemyno tokens are parsed. Invalid enemy IDs are skipped.

Large enemies are capped at five. If a large enemy arrives after the first five insertion positions, source searches the first five entries for a normal enemy, moves that normal enemy to the current insertion slot and puts the large enemy into the freed front slot. If the first five are already all large, the later large enemy is skipped.

Recovered normal-mode lists never exceed ten entries.

## Gym / dojo construction

gym>0 calls BATTLE_CreateVsEnemy mode 2 instead of mode 1.

Doujyou_GetEnemy accepts up to 64 enemyno candidates, filters invalid entries and randomly selects exactly one main enemy. If enemypetno exists, it independently selects exactly one companion enemy. The result is one or two enemy templates, not the whole configured pool.

The gym value becomes baselevel for ENEMY_createEnemy. The battle receives norisk=1. The first created enemy has its image and name overwritten from the NPC before parameter recomputation.

This matches recovered data: all 200 gym blocks have 17 enemyno candidates and all 200 have enemypetno lists of 34 or 36 candidates.

## Battle entry and steal timing

After BATTLE_CreateVsEnemy succeeds, NPCEnemy installs NPC_NPCEnemy_Dying as WinFunc and may emit startmsg.

steal=0 deletes configured item targets immediately after successful battle creation. steal=1 invokes the same deletion routine after victory.

The deletion routine scans all item slots, including equipment, and deletes the first matching instance for each target ID.

Historical quirk: its found counter is cumulative and is never reset for each requested ID. If the first target is missing, deletion stops. After any earlier item was found, a later missing target no longer triggers the intended stop condition. Recovered item lists are single-value and only one block uses steal, so this multi-token defect is dormant in the preserved specimen.

## dieact=0 hide / revive

On victory, dieact=0 sets NPC image to zero, changes event type away from enemy encounter, installs NPCEnemyLoop at 5000 ms and records death time.

Missing time normalizes to 120 seconds.

NPCEnemyLoop restores image and enemy event type only when current time is strictly greater than death_time + revival_time. Equality does not revive.

Bismarck adds an extra BattleIn revival-deadline guard; pinned gavin and iriselia do not show that guard at the same location. It is versioned, not common R1 behavior.

## dieact=1 old warp

Without NEWNPCENEMY, each valid winning player entry is discharged from its party and warped to the stored floor/x/y destination.

The recovered probe reports 250 dieact=1 blocks and zero old-warp blocks missing coordinates.

## NEWNPCENEMY warp

All three pinned builds enable _NEW_WARPMAN.

The win callback scans OVER segments through NPC_NPCEnemy_CheckFree. A usable segment contains NEWEVENT, passes FREE through generic NPC_ActionPassCheck, and provides WARP. One of up to 15 semicolon-separated destinations is selected.

Recovered FREE families are ENDEV, EQUIT, LV and NOWEV. Comma is OR and ampersand is AND. ENDEV/NOWEV less-than and greater-than collapse to bit presence in the underlying generic helper; != negates equality/presence.

If the selected WARP entry has non-positive floor, source falls back to entry zero.

CHECKPARTY containing FALSE would suppress per-player event action and make a party leader warp the whole party, returning early. No recovered CHECKPARTY exists, so the preserved 2.5 path keeps Party true: individual winner discharge + warp, with Action_RunDoEventAction called. The probe found no state-changing NEW_ACTION key inside these segments.

## Compile-boundary exclusions

gavin and iriselia enable _EMENY_CHANCEMAN while Bismarck does not. That extension is not three-lineage common and is excluded.

_NEW_ITEM_ is enabled in Bismarck but not the other two fixed builds. The model therefore parameterizes item slots rather than hard-coding one descendant's expanded inventory.

_ADD_NOITEM_BATTLE and _NPC_REPLACEMENT are enabled in fixed descendants, but recovered NPCEnemy data has no active noitem or REPLACEMENT key, so those branches are not expanded in this recovered-data-driven R1.

## Deterministic artifacts

- tools/stoneage_npcenemy_core_model.py
- tests/test_stoneage_npcenemy_core_model.py
- .github/workflows/validate-stoneage-npcenemy-core.yml

Local validation: 25 deterministic tests passed.

## Evidence status

FACT: recovered 2.5 contains 279 resolved file-backed NPCEnemy refs, split 200 gym / 79 normal.

FACT: normal NPCEnemy uses the first-ten enemy builder; gym uses the 64-candidate dojo selector and yields one main plus optional one companion.

FACT: recovered entype normalizes to dual walk/talk on all 279 blocks.

FACT: recovered dieact reaches both old warp and hide/revive paths.

FACT: NEWNPCENEMY is live but small: two blocks and three FREE+WARP NEWEVENT segments.

SOURCE QUIRK: party-client encounter routing can return true without starting battle itself.

SOURCE QUIRK: duplicate item-gate IDs can reuse one physical item.

SOURCE QUIRK: steal found is cumulative across target IDs.

SOURCE QUIRK: revival uses strict greater-than at the deadline.

VERSIONED: Bismarck's extra BattleIn revival guard is not common to the other two fixed descendants.

OPEN: exact JSS-era NPCEnemy behavior and data until an earlier clean artifact is recovered.

## Next seam

NPCEnemy R1 is closed for recovered 2.5 active surface plus fixed-descendant common core. Advance to shared Bus + Airplane travel/economy seam.
