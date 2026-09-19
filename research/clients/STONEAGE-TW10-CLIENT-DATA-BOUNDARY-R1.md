# StoneAge Taiwan v1.0 deterministic client-data boundary — R1

Date: 2026-09-19  
Primary specimen: accepted Taiwan Waei/JSS StoneAge v1.0 retail disc, Redump 104630  
Primary derived inventory: `research/recovered/STONEAGE-TW10-CLIENT-INVENTORY-R1.txt`

## Result

The accepted Taiwan v1.0 retail client now has a reconstruction-oriented file boundary rather than only a raw disc tree.

At the current evidence level, the client cleanly separates into disc-resident deterministic resources, runtime-created/downloaded field-map cache data, executable-embedded code/resources, and game/master data whose historical source remains unresolved. This boundary is sufficient to begin semantic dataset construction without continuing obsolete operator-network archaeology.

## FACT — core disc boundary

The chosen Joliet filesystem namespace contains 411 files. Of those, 383 files are classified as the core StoneAge client, totaling 373,564,663 bytes.

The remaining current inventory boundary records 19 separately bundled files under the non-StoneAge bonus-content prefixes and 9 files outside the core `StoneAge/` client tree.

Core-client categories are:

| Category | Files | Bytes |
| --- | ---: | ---: |
| graphics_world | 2 | 325,921,908 |
| sprite_animation | 2 | 2,895,198 |
| battle_map | 220 | 366,956 |
| palette | 16 | 11,328 |
| audio_bgm | 11 | 34,056,186 |
| audio_sfx | 118 | 7,651,683 |
| runtime_executable | 2 | 835,584 |
| branding_ui_shell | 3 | 790,124 |
| local_state | 1 | 128 |
| installer_support | 8 | 1,035,568 |

Every core file has a SHA-256 recorded in the derived inventory. Those hashes, not path names alone, are the stable v1.0 file-level provenance anchors for future comparison.

## FACT — ordinary field maps are not disc-resident

There are zero ordinary field-map/cache files in the accepted retail disc tree.

The independently recovered v1.0 runtime uses `map\\%d.dat`, creates the map directory at runtime, and the exact receive path joins server `M` / `MC` protocol handling to writable/readable map-cache functions. Therefore the ordinary field-map payload belongs to the runtime-generated/downloaded side of the original client boundary rather than to the retail-disc resource set.

Battle maps are a separate subsystem and are disc-resident.

## FACT — battle container is maps plus battle palettes, not 233 maps

`battletxt_1.txt` contains 233 address-table records with 233 unique names and no duplicate references. All 233 names resolve to files on the accepted disc, but they split into two resource kinds:

- 218 records resolve to `StoneAge/data/battlemap/battle00.sab` through `battle217.sab`.
- 15 records resolve to `StoneAge/data/pal/Palet_1.sap` through `Palet_15.sap`.
- `Palet_0.sap` is disc-resident but is not one of those 233 address-table names.

The size identity closes the container composition exactly:

- 218 battle-map files × 804 bytes = 175,272 bytes.
- 15 battle palettes × 708 bytes = 10,620 bytes.
- 175,272 + 10,620 = 185,892 bytes = the exact size of `battle_1.bin`.

Therefore the earlier 233-record container count must not be interpreted as 233 distinct battle maps. The reconstruction boundary is 218 battle-map records plus 15 battle-palette records.

## FACT — sound address table and loose audio boundary

`soundaddr_1.txt` contains 114 address-table records, all with unique names, and all 114 names resolve inside `StoneAge/data/se/`.

The disc contains 116 loose SFX WAV files. The two loose files outside the 114-name address-table set are `sak_91.wav` and `sak_92.wav`.

Independent container diagnostics establish 114 records in `sound_1.bin`: 107 match their loose WAV counterparts exactly, while 7 are variant payloads/RIFF structures. The container and loose WAV directory therefore must remain separate provenance surfaces rather than being flattened into one assumed-identical audio set.

The BGM subsystem is separately disc-resident as 11 WAV files.

## FACT — graphics and animation anchors

The v1.0 graphics pair is:

- `adrn_1.bin`: 125,996 fixed 80-byte records, no duplicate bitmap numbers.
- `real_1.bin`: 315,842,228 bytes, fully covered by the ADRN record stream with no unreferenced tail.

The v1.0 animation pair is:

- `spradrn_1.bin`: 464 records.
- `spr_1.bin`: 2,889,630 bytes.
- recovered aggregate structure: 39,065 animations and 242,085 frames.

The complete v1.0 REAL payload and all v1.0 ADRN records are exact prefixes of the preserved 2.5 bridge resources. The complete v1.0 SPR payload and all 464 v1.0 SPRADRN records are likewise exact prefixes. This makes the v1.0 IDs stable ancestral comparison anchors, while later appended data remains later-lineage evidence rather than v1.0 fact.

## FACT — executables, shell assets and local state

The core runtime/launcher pair is:

- `StoneAge.exe` — updater/launcher.
- `sa_3.exe` — game runtime.

The disc also contains three explicit shell/branding files (`logo.bmp`, `waei.bmp`, `man.ico`) and one 128-byte `data/savedata.dat` local-state seed.

PE code, string tables and resource sections are executable-embedded evidence. Their presence does not by itself establish a separate historical character/pet/item/skill/NPC master table.

## OPEN — character, pet, item, skill and NPC/master data

The deterministic filename scan finds zero standalone core files whose paths contain the bounded master-table terms `pet`, `item`, `skill`, `magic`, `npc`, `enemy`, `quest` or `shop`.

This is filename-level evidence only. It supports the narrower statement that no obvious separately named master-table file is present in the retail tree. It does **not** prove those data are wholly server-side, because records may still be embedded in executable/resource containers or delivered through protocol traffic.

The next reconstruction step must therefore correlate protocol-visible character/pet/item/skill fields with the preserved 2.5 server-data bridge and descendant source controls, while keeping any later-only fields explicitly separated from v1.0 FACT.

## Reconstruction consequence

The file-boundary phase is complete enough to move from inventory to semantic datasets.

Highest-priority dataset work is now:

1. build an explicit battle-scene crosswalk for 218 SAB layouts + 15 indexed battle palettes + the non-indexed `Palet_0.sap`;
2. export stable REAL/ADRN bitmap metadata and SPR/SPRADRN animation metadata keyed by v1.0 IDs;
3. build the audio crosswalk that preserves the distinction among 114 indexed container records, 116 loose SFX WAVs and 11 BGM WAVs;
4. correlate protocol-visible character/pet/item/skill/NPC fields against the 2.5 bridge without promoting later data to v1.0 fact.

No historical proprietary payload bytes are added to the repository by this record.
