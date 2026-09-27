# StoneAge Taiwan v1.0 Foundation Baseline Acceptance — R1

Date: 2026-09-27

## Decision

**FOUNDATION_BASELINE = ACCEPTED**

The accepted Taiwan Waei/JSS StoneAge v1.0 retail-disc specimen (Redump 104630) is sufficient to serve as the project's historical **foundation client baseline** for technical reconstruction and modern single-player reimplementation.

This acceptance does **not** claim that the retail client disc contains every byte that existed in the historical MMO service. The original game intentionally split state/content across the retail client, runtime-created/downloaded map cache, protocol-delivered state and server-side master/world data.

The project therefore distinguishes two questions:

| Question | Result |
| --- | --- |
| Is Taiwan v1.0 sufficiently early, official/clean, complete and technically rich to anchor reconstruction? | **PASS** |
| Is this retail disc alone a complete archival image of the historical online service, including all server/world/master data? | **NO — not expected and not required** |

## Acceptance rationale

### 1. Provenance and deterministic inventory — PASS

Primary specimen:

- Taiwan Waei/JSS StoneAge v1.0 retail disc;
- Redump identifier: **104630**;
- accepted by the project as the clean early retail-client specimen.

The deterministic inventory establishes:

- Joliet filesystem: **411 files**;
- classified core StoneAge client: **383 files**;
- core-client bytes: **373,564,663**;
- every core file has a recorded SHA-256 provenance anchor.

Primary evidence:

- `research/recovered/STONEAGE-TW10-CLIENT-INVENTORY-R1.txt`
- `research/clients/STONEAGE-TW10-CLIENT-DATA-BOUNDARY-R1.md`

### 2. Core graphics / animation identity layer — PASS

The baseline exposes a large stable visual-resource namespace:

- `adrn_1.bin`: **125,996** fixed records;
- `real_1.bin`: **315,842,228 bytes**, fully covered by the ADRN stream;
- `spradrn_1.bin`: **464** sprite groups;
- `spr_1.bin`: **2,889,630 bytes**;
- recovered aggregate animation structure: **39,065 animations / 242,085 frames**.

Derived metadata exports already exist for ADRN, collision attributes, sprite groups, animations and frames without committing proprietary payload imagery.

Primary evidence:

- `research/recovered/tw10-resource-metadata/MANIFEST-R1.txt`
- `research/mechanics/STONEAGE-TW10-ADRN-COLLISION-R1.md`

### 3. Battle-resource boundary — PASS

The v1.0 client provides a closed deterministic battle-resource corpus:

- **218** battle SAB layouts;
- **15** indexed battle palettes;
- `Palet_0.sap` as an additional disc-resident palette;
- exact battle-container composition is closed at byte level.

All 218 SAB resources share the fixed historical 804-byte envelope. Their 20×20 graphic-grid interpretation has strong lineage support; remaining low-level semantic details can continue to be promoted independently without blocking reconstruction.

Primary evidence:

- `research/clients/STONEAGE-TW10-BATTLE-RESOURCE-FORMAT-R1.md`
- `research/recovered/STONEAGE-TW10-BATTLE-DATASET-R1.txt`

### 4. Audio-resource boundary — PASS

The v1.0 audio namespace is reconstructed sufficiently for implementation work:

- **114** indexed `sound_1.bin` records;
- **116** loose SFX WAV files;
- **11** independent BGM WAV files;
- indexed/loose byte identity and variant relationships are explicitly preserved.

Primary evidence:

- `research/clients/STONEAGE-TW10-AUDIO-PROVENANCE-R1.md`
- `research/recovered/STONEAGE-TW10-AUDIO-DATASET-R1.txt`

### 5. Executable / updater / runtime architecture — PASS

The original client architecture is directly recoverable:

- `StoneAge.exe` = launcher/updater layer;
- `sa_3.exe` = game runtime;
- v1.0 runtime SHA-256:
  `cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a`;
- updater host/path grammar and later first-party runtime lineage have already been recovered;
- executable strings, PE resources and runtime call paths provide direct implementation evidence.

This is sufficient to understand the original split while allowing the modern game to replace it with a local-first architecture.

### 6. Gameplay/protocol state model — PASS FOR FOUNDATION

The accepted v1 runtime independently exposes a substantial original gameplay surface.

Bounded generated-protocol analysis identifies:

- **20 unique client→server builders**;
- **33 unique server→client dispatch branches**.

Direct v1 shapes cover major reconstruction domains including:

- character/object state;
- character actions and deletion;
- status/state multiplexing;
- items and inventory operations;
- owned-pet operations;
- pet-skill execution and skill-up;
- NPC/window interaction;
- map rectangle/cache transfer;
- character creation;
- battle/state envelopes.

The repository already contains reconstruction-oriented runtime schemas for:

- `CharacterState`;
- `WorldObject`;
- `PetState`;
- `PetSkillView`;
- `ItemInstance` / `ItemView`;
- `NPCWindowSession`.

Primary evidence:

- `research/clients/STONEAGE-TW10-GAMEPLAY-DATA-MATRIX-R1.md`
- `research/clients/STONEAGE-TW10-GAMEPLAY-SCHEMA-R1.json`
- `research/recovered/STONEAGE-TW10-GAMEPLAY-PROTOCOL-R1.txt`

### 7. Ordinary field maps — KNOWN EXTERNAL CONTENT, NOT A BASELINE FAILURE

The retail disc contains **zero ordinary field-map/cache files**.

This is not treated as a damaged or incomplete retail specimen. Original `sa_3.exe` evidence shows that the runtime:

- uses `map\\%d.dat`;
- creates the map directory at runtime;
- receives map content through the original `M` / `MC` protocol path;
- reads/writes the resulting local map cache.

Therefore ordinary field maps belonged to the online/runtime-delivered side of the historical product boundary.

For the modern single-player rebuild, the project must reconstruct its world-map corpus from recoverable historical/later-version evidence and deliberate design. Exact v1 server delivery is useful evidence, not a prerequisite for beginning implementation.

### 8. Pet / item / NPC / quest authoritative master data — KNOWN SERVER-SIDE GAP, NOT A BASELINE FAILURE

No obvious separately named standalone pet/item/skill/magic/NPC/enemy/quest/shop master table exists in the v1 retail client tree.

The project already has a controlled 2.5 bridge for understanding server/master-data concepts including:

- pet/enemy templates;
- pet skills;
- item templates;
- NPC/world graph;
- encounter chains.

Critical evidence discipline remains:

- v1 runtime/wire fields remain the early baseline authority;
- 2.5 master data is a **BRIDGE**, not retroactively renamed as v1 fact;
- runtime identity must remain separate from template identity;
- later-only fields must remain version-tagged.

Primary evidence:

- `research/clients/STONEAGE-TW10-25-GAMEPLAY-BRIDGE-R1.json`
- related 2.5 master-data reports under `research/recovered/`.

### 9. Local state / savedata — NON-BLOCKING OPEN DETAIL

The accepted disc contains a 128-byte `data/savedata.dat` seed.

R1 runtime analysis confirms:

- exact 128-byte artifact and hashes;
- one `data\\savedata.dat` string in `sa_3.exe`;
- no direct text xref was recovered;
- likely pointer/table indirection remains to be analyzed.

This affects low-level historical local-state semantics, not the decision to use v1.0 as the reconstruction foundation.

Primary evidence:

- `research/recovered/STONEAGE-TW10-SAVEDATA-R1.txt`.

## Acceptance boundary

The phrase **foundation baseline** means:

> an early, trustworthy official client that exposes enough original resource identity, runtime behavior, data organization and gameplay-state structure to anchor independent reconstruction.

It does **not** mean:

> a frozen requirement that every future system/content choice reproduce Taiwan v1.0 exactly.

Per DD-012, later official versions are a design/content library and evolutionary record. Their content may be retained, adapted, merged, redesigned or rejected.

Per DD-013, the current product is local/private single-player in deployment while preserving MMORPG-style depth and a clean separation between deterministic game logic and future transport/network concerns.

## Research-policy consequence

Open-ended hunting for an absolute-earliest client is no longer on the critical path.

From this acceptance forward:

1. Taiwan v1.0 is the historical foundation client baseline.
2. Earlier clean clients remain opportunistic discoveries for controlled diffing.
3. Later official clients/resources/master data are structured comparison and design inputs.
4. Physical-only provenance research remains non-primary under DD-011.
5. Technical reconstruction/specification outranks further general version archaeology.

## Next reconstruction priority

The next critical path is **semantic/system closure**, not more baseline hunting:

1. close the remaining v1 runtime state semantics that materially affect game rules;
2. define version-tagged world/map/content datasets using recoverable evidence;
3. consolidate character/pet/item/skill/NPC/battle/encounter specifications into engine-neutral deterministic models;
4. separate historical facts from design substitutions where original server content is missing;
5. then implement the local-first modern runtime against those specifications.

## Final classification

**TAIWAN_V1_FOUNDATION_BASELINE_R1 = ACCEPTED**

**EARLIEST_CLIENT_HUNT = NON_BLOCKING**

**FULL_HISTORICAL_SERVER_CONTENT_FROM_V1_DISC = NOT_EXPECTED**

**TECHNICAL_RECONSTRUCTION_CRITICAL_PATH = ACTIVE**
