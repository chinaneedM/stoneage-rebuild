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

The shared parser helpers are now structurally fingerprinted from the v1 binary:

- `0x46c70` is the v1 **string-token extraction role**. C/I callsites supply the delimiter `'|'`, token index and output-buffer bound; the helper itself contains DBCS-aware scanning through `IsDBCSLeadByte`.
- `0x46da0` is the v1 **decimal-integer-token role**. It has the shorter source/delimiter/index calling shape and directly calls `0x46c70` before an integer-conversion path. The later symbolic name `getIntegerToken` is lineage terminology, not a recovered v1 symbol.
- `0x46e70` is the v1 **base-62-integer-token role** used for the bitmask/kubun fields in `P`, `K` and `N`. It directly calls `0x46c70` and a distinct conversion helper. The later symbolic name `getInteger62Token` remains lineage terminology.
- `0x46ff0` is the v1 **escape-decoding role**: one pointer argument, paired immediately after extracted string fields, with its own decode helper.

This makes the following branch structure direct v1 evidence:

| S category | Direct v1 token structure |
| --- | --- |
| `C` | decimal integer tokens 1..5 |
| `D` | decimal integer tokens 1..2 |
| `E` | decimal integer tokens 1..2 |
| `M` | decimal integer tokens 1..3 |
| `J` | decimal integers 1..4; escaped strings 5..6 |
| `N` | base-62 mask token 1; decimal integers 2..6; escaped string 7 on the full-update path |
| `P` | base-62 mask token 1; decimal integers 2..24; escaped strings 25..26 on the full-update path |
| `K` | base-62 mask token 1; decimal integers 2..19; escaped strings 20..21 on the full-update path |
| `W` | loop body contains three decimal-token roles + two escaped-string roles per static record path; exact stride is being independently fingerprinted |
| `I` | loop body contains six decimal-token roles + three escaped-string roles per static record path; exact stride is being independently fingerprinted |

The early 2000 generated protocol assigns meanings that match these direct shapes exactly for the fixed-layout categories:

- `C`: floor, max X, max Y, X, Y;
- `D`: character/runtime ID and server-time value;
- `E`: minimum and maximum encounter percentages;
- `M`: HP, MP and EXP;
- `J`: magic use/kind, MP, field, target, name, comment;
- `N`: party member ID, level, max HP, HP, MP, name after the update mask;
- `P`: old player-state sequence ending with gold, title/index and duel-point-like integer state, then name/free-name;
- `K`: old pet-state sequence ending with skill-slot count and rename flag, then name/free-name.

The **positions/counts are V1 DIRECT**; the human-readable field names remain semantic mappings supported by the early generated lineage unless independently tied to v1 storage/use sites.

### Direct version exclusion

This switch provides a stronger boundary than descendant macro names alone.

In the pinned later client source:

- profession-skill status uses category `S`;
- later profession cooldown uses category `G`;
- pet-item status uses category `B`;
- a ride-related extension uses category `X`.

In the accepted v1 binary, `G` and `S` map to the shared default branch, while `B` and `X` lie outside the accepted `C..W` dispatch range. Therefore those specific later `S`-message category implementations are **not present in this compiled Taiwan v1 client**. This does not date every related game concept globally; it establishes a concrete client-version boundary for these protocol implementations.

Two additional packet-layout boundaries are now binary-direct:

- the v1 full `S:P` path reads decimal fields only through token **24**, then immediately reads the two escaped strings at tokens **25 and 26**. The later descendant additions for player transmigration/ride/base-graphic state therefore are **not present in this v1 full-status layout**;
- the v1 full `S:K` path reads decimal fields only through token **19**, then immediately reads the two escaped strings at tokens **20 and 21**. The later descendant pet-transmigration/fusion/ride/bless extensions therefore are **not present in this v1 full pet-status layout**.

These statements are specific to the compiled v1 status protocol layout; they do not claim that every related gameplay concept was impossible elsewhere in the product lineage.

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

### V1 DIRECT — `C` object-record parser

The accepted v1 `C` callback at RVA `0x31260` is now field-bounded directly from the original binary.

It first splits the incoming `C` envelope into comma-separated records. For each record, the legacy object classifier uses field-presence tests and then follows one of three directly observed layouts:

**Character/object record — 12 fields in this v1 binary**

| Token | Direct v1 parse role | Early-lineage semantic mapping |
| ---: | --- | --- |
| 1 | decimal token | character/object type |
| 2 | string token → base-62 conversion | runtime character/object index |
| 3 | string token → decimal conversion | X |
| 4 | string token → decimal conversion | Y |
| 5 | string token → decimal conversion | direction |
| 6 | string token → decimal conversion | base graphic |
| 7 | string token → decimal conversion | level |
| 8 | decimal token | name color |
| 9 | escaped string | name |
| 10 | escaped string | self/free title |
| 11 | string token → decimal conversion | walkable |
| 12 | string token → decimal conversion | height |

The v1 character branch contains **no token-13 extraction** before control leaves the main character-record path. The later generated control's `POPUPNAMECOLOR` field therefore must remain a later/versioned extension relative to this accepted v1 binary.

**Ground item record — 6 fields**

The v1 callback directly tests for a sixth token and then parses:

1. base-62 runtime object ID;
2. X;
3. Y;
4. graphic ID;
5. integer class/type value;
6. escaped information string.

The human-readable names are lineage mappings; the six-position parse shape and conversion roles are V1 DIRECT.

**Ground money record — 4 fields**

If the sixth token is absent but a fourth token is present, the v1 callback parses:

1. base-62 runtime object ID;
2. X;
3. Y;
4. money amount.

The later descendant source independently preserves the same three-way legacy parser, including presentation-only money graphics chosen client-side by amount. Those presentation constants remain lineage support unless separately fingerprinted in v1.

Reconstruction consequence:

- v1 world-state transport distinguishes runtime **character/object**, **ground-item** and **ground-money** records inside the same `C` envelope;
- the accepted v1 character record is a 12-field layout, not the later 13+ field descendants;
- runtime object IDs remain separate from server template IDs.

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

### V1 DIRECT — `WN` forwarding boundary

The accepted v1 `WN` callback at RVA `0x328c0` contains no token parser of its own. Its only direct business call is target RVA `0x12930`.

The bounded call prelude shows five incoming callback arguments pushed onward to that target without an intervening transformation. Combined with the already direct top-level receive shape (**4 integers + 1 string**), this establishes an original-client boundary in which the generated protocol decoder supplies a five-value window/session tuple and the `WN` callback forwards it to the client window subsystem.

The early generated lineage names the tuple:

`window type | button mask/type | sequence number | source object index | data`.

Those semantic labels remain lineage names, but the five-value forwarding boundary and target RVA are V1 DIRECT.

Reconstruction consequence: model NPC/window interaction as a **server-driven window session** with a decoded transport tuple forwarded into a client presentation subsystem. Do not model the client as owning authoritative NPC dialog/shop master data merely because later server bundles contain it.

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

