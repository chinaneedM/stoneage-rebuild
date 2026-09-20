# StoneAge Taiwan v1.0 Gameplay / Master-Data Evidence Matrix — R1

Date: 2026-09-20

## Purpose

This document defines the first reconstruction-oriented bridge between:

1. the accepted Taiwan Waei/JSS v1.0 retail client;
2. the early generated LSSPROTO lineage preserved in the pinned descendant client source;
3. the recovered mixed 2.5 server/master-data corpus.

It does **not** assert that the 2.5 server tables are the Taiwan v1.0 server data. The 2.5 corpus is used only to explain later-preserved identities, relationships and server-side schema concepts where the v1.0 client independently proves that a corresponding gameplay surface exists.

## Evidence labels

- **V1 DIRECT** — independently observed in accepted Taiwan v1.0 `sa_3.exe` bytes or the accepted v1.0 retail-disc resource set.
- **EARLY LINEAGE** — semantic names/layout preserved by the pinned generated LSSPROTO source family, especially the generator output dated 2000-06-12. This can explain a V1 DIRECT shape but is not itself original Taiwan runtime proof.
- **2.5 BRIDGE** — recovered later server/master table or fixed descendant server behavior that supplies a plausible authoritative source/schema relationship.
- **VERSIONED / OPEN** — later fields or semantics not independently supported for the v1.0 baseline.

Primary v1 binary evidence:

- `research/recovered/STONEAGE-TW10-GAMEPLAY-PROTOCOL-R1.txt`
- `research/recovered/STONEAGE-TW10-RECEIVE-MAP-JOIN-R1.txt`
- `research/clients/STONEAGE-TW10-LSSPROTO-GENERATOR-LINEAGE-R1.md`

Primary 2.5 bridge evidence:

- `research/recovered/STONEAGE-25-ENEMYBASE-PROBE-R1.txt`
- `research/recovered/STONEAGE-25-ITEMSET-SCHEMA-R1.txt`
- `research/recovered/STONEAGE-25-PETSKILL-PROBE-R1.txt`
- `research/recovered/STONEAGE-25-NPC-WORLD-GRAPH-R1.txt`

Pinned lineage source:

- `BismarckDD/stoneage@999ffdf1d220ec6666eb65339180689c9caf1876`
- registered as `SRC-CODE-DESC-STONEAGE-BISMARCKDD-999FFDF1`

## V1 DIRECT — gameplay protocol surface now independently bounded

The accepted v1 runtime contains a compact generated-protocol send region at RVA `0x18c00..0x19730` and receive-dispatch region at `0x19730..0x1aa8a`.

The deterministic probe resolves:

- **20 unique client-to-server generated builders** in the bounded send region;
- **33 unique server-to-client dispatch branches** in the bounded receive region.

Important exact shape matches between v1 bytes and the early generated lineage include:

| Direction | Message | V1 top-level shape | Reconstruction significance |
| --- | --- | --- | --- |
| C→S | `C` | 1 int | character/object detail request by index |
| S→C | `C` | 1 string | world-object/character description envelope |
| S→C | `CA` | 1 string | character action envelope |
| S→C | `CD` | 1 string | character/object delete envelope |
| S→C | `S` | 1 string | status/state multiplex envelope |
| S→C | `I` | 1 string | item update envelope |
| S→C | `SI` | 2 ints | item-slot swap/move result shape |
| C→S | `KS` | 1 int | pet-related index operation |
| S→C | `KS` | 2 ints | pet-related index + result |
| C→S | `PS` | 3 ints + 1 string | pet-skill execution request |
| S→C | `PS` | 4 ints | pet-skill execution result |
| C→S | `SKUP` | 1 int | skill-up request |
| S→C | `SKUP` | 1 int | skill-up result/point |
| C→S | `WN` | 5 ints + 1 string | NPC/window response |
| S→C | `WN` | 4 ints + 1 string | NPC/window presentation |
| S→C | `PME` | 7 ints + 1 string | pet/message/effect presentation |
| C→S | `M` | 5 ints | map rectangle request |
| S→C | `M` | 5 ints + 1 string | map rectangle payload |
| S→C | `MC` | 8 ints + 1 string | map/checksum/control payload |
| C→S | `CreateNewChar` | 12 ints + 1 string | character creation state |
| S→C | `RS` | 1 string | result/status data envelope |
| S→C | `RD` | 1 string | result/status data envelope |
| S→C | `B` | 1 string | battle-command/state envelope |
| S→C | `D` | 3 ints + 1 string | display/presentation envelope |

The exact helper-call counts and callback RVAs are retained in the derived report.

### Important negative/absence boundary

The bounded v1 generated send region does **not** expose separate builders for lineage-control messages `S` or `MI`, and the bounded receive region does not expose `EF` or `SE`.

This is evidence only about this compiled v1 client surface. It does **not** prove that those logical operations or protocol names never existed elsewhere, because:

- a function may have been eliminated because it was unused;
- the operation may be encoded through another message;
- a later generated control may have added or separated a message.

Therefore these are recorded as **not observed in the bounded v1 generated surface**, not as “absent from StoneAge v1”.

## V1 DIRECT — internal `S` status-category switch

The accepted v1 `S` callback at RVA `0x2f670` now has a directly decoded compact switch.

The binary:

1. reads the first byte of the `S` payload;
2. subtracts ASCII `'C'`;
3. bounds the normalized value to `0x14`, i.e. `C..W`;
4. translates it through the byte lookup table at RVA `0x30d04`;
5. jumps through the dword target table at RVA `0x30cd8`.

The 21-character mapping is direct v1 evidence:

| Category | v1 branch | Early-lineage meaning |
| --- | --- | --- |
| `C` | `0x2f6ae` | map/floor and position state |
| `D` | `0x2f797` | character ID / server-time state |
| `E` | `0x30408` | encounter-percentage range |
| `I` | `0x30922` | full item/inventory state |
| `J` | `0x30445` | magic slot/state |
| `K` | `0x2fe94` | owned-pet state |
| `M` | `0x2fe2e` | compact HP/MP/EXP state |
| `N` | `0x305a4` | party-member state |
| `P` | `0x2f7f0` | player status |
| `W` | `0x30b4f` | owned-pet skill view |
| `F,G,H,L,O,Q,R,S,T,U,V` | shared default `0x30ccb` | not implemented by this compiled v1 switch |

The **category letters and branch RVAs are V1 DIRECT**. The human-readable meanings in the third column remain EARLY LINEAGE until the individual branches are field-by-field matched.

The branch call shapes strongly reproduce the early parser structure:

- `C`: five calls to helper `0x46da0`;
- `D`: two calls to `0x46da0`;
- `E`: two calls to `0x46da0`;
- `M`: three calls to `0x46da0`;
- `J`: four `0x46da0`, two `0x46c70`, two `0x46ff0`;
- `W`: three `0x46da0`, two `0x46c70`, two `0x46ff0`;
- `I`: six `0x46da0`, three `0x46c70`, three `0x46ff0`;
- `P`: 46 `0x46da0`, four `0x46c70`, four `0x46ff0` static callsites across full/partial update paths;
- `K`: 36 `0x46da0`, four `0x46c70`, four `0x46ff0` static callsites across full/partial update paths.

The C/I callback probe independently shows the same three helper RVAs in the same structural roles. Their exact semantic names are still being fingerprinted from the v1 helper bodies/callsites; R1 does not yet label the RVAs themselves as direct `getIntegerToken` / `getStringToken` / unescape symbols.

### Direct version exclusion

This switch provides a stronger boundary than descendant macro names alone.

In the pinned later client source:

- profession-skill status uses category `S`;
- later profession cooldown uses category `G`;
- pet-item status uses category `B`;
- a ride-related extension uses category `X`.

In the accepted v1 binary, `G` and `S` map to the shared default branch, while `B` and `X` lie outside the accepted `C..W` dispatch range. Therefore those specific later `S`-message category implementations are **not present in this compiled Taiwan v1 client**. This does not date every related game concept globally; it establishes a concrete client-version boundary for these protocol implementations.

Canonical derived evidence: `research/recovered/STONEAGE-TW10-GAMEPLAY-CALLBACKS-R1.txt`.

## Character data matrix

### Character creation

**V1 DIRECT:** `CreateNewChar` serializes exactly 12 integers and one string.

**EARLY LINEAGE:** the preserved generated signature names those arguments as:

- data-place number;
- character name;
- image number;
- face image number;
- vital;
- strength;
- toughness;
- dexterity;
- earth;
- water;
- fire;
- wind;
- hometown.

Because the v1 field count/type/order matches the generated control exactly, this is a **strong lineage-supported semantic mapping**.

Reconstruction status:

| Field | Status |
| --- | --- |
| name | V1 DIRECT string position + EARLY LINEAGE meaning |
| body/image identity | V1 DIRECT integer position + EARLY LINEAGE meaning |
| face image identity | V1 DIRECT integer position + EARLY LINEAGE meaning |
| vital / strength / toughness / dexterity | V1 DIRECT integer positions + EARLY LINEAGE meanings |
| earth / water / fire / wind | V1 DIRECT integer positions + EARLY LINEAGE meanings |
| hometown | V1 DIRECT integer position + EARLY LINEAGE meaning |
| later profession/class fields | VERSIONED / not promoted |
| later extra creation customization | VERSIONED / not promoted |

### Runtime player status

**V1 DIRECT:** server-to-client `S` is one encoded string handed to v1 callback RVA `0x2f670`.

**EARLY LINEAGE:** the `S:P` player-status record preserves the old field family:

- HP / max HP;
- MP / max MP;
- vital / strength / toughness / dexterity;
- EXP / max EXP;
- level;
- attack / defense / quick;
- charm / luck;
- earth / water / fire / wind;
- gold;
- identity/name/title-related fields.

These inner subfields remain **EARLY LINEAGE** until the v1 `S` callback's internal parser is independently fingerprinted field-by-field.

### World position

**V1 DIRECT:** the already binary-proven map protocol and `C` / `CA` envelopes establish map/object state delivery.

**EARLY LINEAGE:** the old `S:C` location/status form is:

`floor | maxx | maxy | x | y`.

This is suitable as the reconstruction coordinate model, with inner-field names currently lineage-supported.

## World object / character presentation matrix

**V1 DIRECT:** `C` receive is one encoded string passed to callback RVA `0x31260`; `CA` is one encoded string passed to RVA `0x31910`.

**EARLY LINEAGE:** the principal `C` object record is:

`WHICHTYPE | CHARINDEX | X | Y | DIR | BASEIMG | LEVEL | NAMECOLOR | NAME | SELFTITLE | WALKABLE | HEIGHT | POPUPNAMECOLOR`.

The same generated control distinguishes object kinds including player, enemy, pet, door, box, warp, shop, healer, old-man/town NPC, NPC enemy, action NPC, window NPC, save point, item shop, stone shop, warp man and event-type objects.

Reconstruction consequence:

- a modern world-object layer should retain **object type, runtime object index, X/Y, direction, base graphic, level, display name/title, walkability and presentation-height/color metadata**;
- specific later object-type enum additions must remain versioned until independently found in v1;
- runtime `CHARINDEX` is not the same concept as a server master-table template ID.

**EARLY LINEAGE:** `CA` carries `CHARINDEX|X|Y|ACTION|PARAM...`, supporting an event/action stream separate from persistent object state.

## Pet / enemy state matrix

### Client-visible pet state

**V1 DIRECT:** `S` is the v1 status envelope; pet-skill operation messages `KS`, `PS` and `SKUP` are independently present with exact old field-type shapes.

**EARLY LINEAGE:** old `S:K0..K4` pet status exposes the following stable client-facing concepts:

- pet number/index;
- live state;
- graphic identity;
- HP / max HP;
- MP / max MP;
- EXP / max EXP;
- level;
- attack / defense / quick;
- AI;
- earth / water / fire / wind;
- skill-slot count/state;
- name/status strings.

### 2.5 authoritative-template bridge

Recovered active `enemybase.txt` has 988 rows and preserves server template concepts including:

- `TEMPNO`;
- `INITNUM`, `LVUPPOINT`;
- `BASEVITAL`, `BASESTR`, `BASETGH`, `BASEDEX`;
- `MODAI`;
- `EARTHAT`, `WATERAT`, `FIREAT`, `WINDAT`;
- `SLOT`;
- `IMGNUMBER`;
- pet-skill references;
- `PETFLG`, `SIZE`, `RARE`, `CRITICAL`, `COUNTER` and other later/server-side fields.

Safe R1 mappings are:

| Client-visible concept | 2.5 bridge candidate | Evidence status |
| --- | --- | --- |
| pet graphic identity | `enemybase.IMGNUMBER` | EARLY LINEAGE ↔ 2.5 BRIDGE |
| AI value | `enemybase.MODAI` | EARLY LINEAGE ↔ 2.5 BRIDGE |
| earth/water/fire/wind | corresponding `enemybase.*AT` fields | EARLY LINEAGE ↔ 2.5 BRIDGE |
| skill slots / skill IDs | `SLOT` + pet-skill references | EARLY LINEAGE ↔ 2.5 BRIDGE |
| derived attack/defense/quick | template/growth-derived server state | client-visible, source formula/version remains separate |
| HP/MP/EXP/level | runtime pet state | client-visible, not identical to static template fields |

Not promoted to v1 FACT:

- exact 2.5 `TEMPNO` population;
- `PETFLG`, `RARE`, `SIZE`, `CRITICAL`, `COUNTER`;
- the exact 988-row table;
- later growth/stat formulas;
- any 2.5-only pet template.

## Pet-skill data matrix

**V1 DIRECT:**

- C→S `PS`: 3 ints + 1 string;
- S→C `PS`: 4 ints;
- C→S and S→C `SKUP`: one int each;
- pet-index operation `KS`: one int outbound, two ints inbound.

These prove a slot/index-based pet skill execution and skill-up surface in the accepted v1 client.

**EARLY LINEAGE:**

- `PS` request semantics: owned-pet index, owned-pet-skill slot, target index, data;
- `PS` result semantics: result, pet index, skill slot, target index;
- `S:W0..W4` skill-view records preserve:
  `skillid | field | target | name | comment`;
- old field enum distinguishes ALL / BATTLE / MAP;
- old target enum distinguishes self, other, own side, opposing side, all and non-self variants.

**2.5 BRIDGE:** active `petskill.txt` contains 147 rows and a recovered prefix schema with semantic concepts:

- ID;
- FIELD;
- TARGET;
- COST;
- ILLEGAL;
- names/comments/function tokens.

The strongest bridge is therefore:

`v1 visible skill ID/FIELD/TARGET/name/comment ↔ 2.5 petskill ID/FIELD/TARGET/name/comment`.

`COST`, `ILLEGAL`, callback/function tokens and later extra columns are **2.5 BRIDGE / VERSIONED**, not v1 facts unless separately established.

## Item data matrix

**V1 DIRECT:**

- S→C `I` is a one-string item-update envelope, callback RVA `0x325f0`;
- S→C `SI` carries exactly two integers, matching the old swap-item result shape.

The bounded generated send inventory did not locate an `MI` builder, so R1 does not claim a direct v1 C→S `MI` implementation despite the early lineage control preserving one.

**EARLY LINEAGE:** the old `S:I` status/item representation exposes client-side item concepts including:

- display/secret names;
- graphic/presentation identity;
- field usability class;
- target class;
- use/display flags.

It also preserves early enums for:

- `ITEM_FIELD_ALL / BATTLE / MAP`;
- target self / other / own side / opposing side / all.

**2.5 BRIDGE:** active `itemset.txt` has 13,252 unique IDs and 94 recovered columns. Directly relevant bridge fields include:

- `id`;
- `name`, `secretname`, `effectstring`;
- `imagenumber`;
- `cost`;
- `type`;
- `fieldtype`;
- `target`;
- `level`;
- `useaction`;
- `magicid` and selected presentation/effect relationships.

R1 must **not** promote the complete 94-column itemset schema into v1. In particular, later callback strings, extra stat requirements, stacking/merge/ingredient columns, later status-resistance fields and other extension columns remain 2.5/versioned evidence.

### Reconstruction-safe split

Use two identities:

- **ItemInstance / inventory slot state** — runtime object known to the client;
- **ItemTemplate bridge ID** — authoritative server data identity, initially opaque where v1 does not transmit/prove it.

This prevents later 2.5 template IDs from being mistaken for directly recovered v1 server IDs.

## NPC / world-content matrix

**V1 DIRECT:** `WN` is independently present in both directions:

- S→C: 4 ints + 1 string;
- C→S: 5 ints + 1 string.

**EARLY LINEAGE:** those fields are:

server→client:
- window type;
- button mask/type;
- sequence number;
- object index;
- data.

client→server adds the selection value.

The old window-type family already includes general messages/selections plus pet select, party select, item shop and pet-skill-shop presentations.

This is strong evidence that the v1 client treats NPC interaction as a **server-driven window/session protocol**, not as a client-resident NPC master database.

**2.5 BRIDGE:** the recovered NPC world graph contains:

- 131 template blocks;
- 4,985 resolved create blocks;
- server map/floor linkage;
- function sets including healer, item shop, pet shop, pet-skill shop, save point, warp, town NPC, NPC enemy, action NPC, window NPC and many later systems.

Safe conclusion:

- the 2.5 graph is a useful **server-content implementation bridge** for how NPC templates/create records can generate v1-style world objects and WN sessions;
- exact 2.5 NPC scripts, coordinates, functionsets and later feature NPCs are not v1 content evidence.

## Battle and display surfaces

**V1 DIRECT:** `B` is a one-string battle envelope. `D` is 3 ints + 1 string. `PME` is 7 ints + 1 string.

The early generated control provides extensive battle command subrecords and presentation meanings, but R1 keeps those as lineage-supported until the corresponding v1 callback internals are independently parsed.

This matrix therefore establishes transport/state boundaries without prematurely flattening later battle tables into the v1 server schema.

## Fields explicitly quarantined from the v1 baseline

The following must remain versioned/open unless new original evidence appears:

- the full 94-column 2.5 item schema;
- alchemy/item-atom recipe data;
- later equipment-slot and requirement extensions;
- exact 2.5 pet-template population and all later pet-template flags;
- pet-skill COST/ILLEGAL/function callback columns;
- later/macro-gated pet skill families;
- 2.5 NPC functionsets not independently reflected by the early v1 client surface;
- profession/family/manor/mount/ride and other later systems;
- later protocol messages absent from the bounded v1 generated surface;
- exact v1 server table row counts, IDs and content values.

## Reconstruction-ready R1 schemas

These are evidence-preserving normalization targets, not claims about original C structs.

### CharacterState

- runtime character index
- visual/body ID
- face ID where applicable
- name/title/display metadata
- floor, x, y, direction
- level
- HP/maxHP, MP/maxMP
- vital, strength, toughness, dexterity
- attack, defense, quick
- charm, luck
- earth, water, fire, wind
- EXP/maxEXP
- gold

Each inner status field must retain an evidence tag until v1 callback parsing promotes it beyond EARLY LINEAGE.

### WorldObject

- object type
- runtime object index
- x/y
- direction
- base graphic ID
- level
- name/title
- walkable flag
- display height/color metadata

### PetState

- owned-pet slot/index
- graphic ID
- live state
- name/status
- level
- HP/maxHP, MP/maxMP
- EXP/maxEXP
- attack, defense, quick
- AI
- earth, water, fire, wind
- skill-slot state

### PetSkillView

- skill ID
- field/use-context class
- target class
- name
- comment
- owned-pet slot association

Server behavior callback/formula remains a separate authoritative implementation layer.

### ItemView / ItemInstance

- inventory/equipment slot index
- presentation graphic
- display/secret/effect text
- field/use-context class
- target class
- runtime state
- opaque authoritative template link

### NPCWindowSession

- window type
- button mask
- sequence number
- source object index
- data payload
- client selection/result

## Next verification seam

The highest-value next binary step is no longer broad protocol enumeration. It is **inside the v1 callbacks**:

1. fingerprint `S` callback RVA `0x2f670` and identify its internal P/C/I/S/J/N/K/W category parsers;
2. fingerprint `C` callback RVA `0x31260` and verify the old world-object field count/order;
3. fingerprint `I` callback RVA `0x325f0` for item subrecord layout;
4. fingerprint `WN` callback RVA `0x328c0` for window/session semantics.

Those passes can promote selected inner fields from EARLY LINEAGE to V1 DIRECT without requiring any original server binary.

