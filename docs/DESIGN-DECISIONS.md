# Design Decisions

## DD-001 — Separate archaeology from reconstruction

**Status:** Accepted

Historical StoneAge materials are evidence and specification inputs. The final game will be reimplemented rather than built by modifying an original executable/client.

## DD-002 — Start from the earliest traceable origin

**Status:** Accepted

Research begins with JSS-era 1999 material rather than treating Mainland 1.82 as the absolute origin. 1.82 remains a major classic reference point.

## DD-003 — Later content may be integrated, but must be narratively/world-system coherent

**Status:** Accepted

The final game may contain systems/content from later StoneAge eras, but they should emerge through progression, world development, civilization, exploration, ecology, story, or player growth rather than being enabled indiscriminately from the beginning.

## DD-004 — Preserve emotional milestones

**Status:** Accepted

Features are not judged only by mechanical utility. Important first-time experiences (for example, earning the ability to ride a pet) should retain anticipation, progression, and emotional payoff.

## DD-005 — Repository is the continuity authority

**Status:** Accepted

The latest remote repository state is the authoritative project record across conversations.

## DD-006 — Keep FACT / HYPOTHESIS / DESIGN distinct

**Status:** Accepted

Historical claims, interpretations, and new design choices must not be conflated.

## DD-007 — Copyright-aware production boundary

**Status:** Accepted

Original code/assets are research material. Production implementation should use independently written code and newly created/recreated production assets. Proprietary originals should not be committed to the repository by default.


## DD-008 — No-purchase research constraint

**Status:** Accepted

The StoneAge archaeology work must not depend on the user buying, bidding on, shipping, opening, installing, or personally dumping any physical client, disc, package, collectible, or second-hand listing.

Marketplace and auction pages may still be used as **public evidence surfaces** for photographs, descriptions, product identifiers, package contents, provenance clues, and search leads. They are not acquisition tasks.

Preferred evidence routes are:

- freely accessible official/archived web material;
- preservation sites and public scans;
- publicly retrievable historical binaries or media with provenance;
- public source trees and technical archives;
- public marketplace/auction photographs and catalog metadata;
- files already available to the project or voluntarily provided by others without purchase by the user.

If a provenance-preserving original client/media image becomes publicly available at no cost, it may be analyzed outside the repository and only hashes, metadata, file trees, and derived research findings should be committed by default.

The project must not ask the user to spend money or personal time acquiring original hardware/media in order to continue research.

## DD-009 — Client-first reverse-engineering priority

**Status:** Accepted

The project’s primary reconstruction method is **artifact-first, not history-first**.

The highest-priority target is the earliest StoneAge client that is simultaneously:

- freely/publicly obtainable;
- provenance-preserving enough to evaluate;
- as close as practical to an original operator-distributed build;
- free of known private-server repacking, custom patchers, replaced assets or undocumented modifications.

The absolute historically earliest client remains desirable, but the project must not stall waiting for an unrecoverable 1999 artifact. If the earliest currently recoverable clean specimen is a later regional/version branch, that artifact becomes the **bridge specimen** for immediate reverse engineering. Older clients can be incorporated later through controlled diffing when recovered.

Once a usable specimen exists, technical work outranks general historical research. Priority order is:

1. preserve provenance and hashes;
2. inventory the complete file tree;
3. identify executables, runtime/update components and dependencies;
4. decode resource/container/index formats;
5. reconstruct maps, characters, pets, items, skills, attributes, UI, text/data tables and other deterministic content;
6. compare additional clean clients to recover version evolution;
7. reimplement the resulting specifications with modern code and independently created/recreated production assets.

Historical articles, prices, package identifiers, staff recollections and marketplace material are supporting evidence only when they help authenticate a client, establish lineage, locate bytes, or resolve a technical ambiguity.

## DD-010 — Historical automation and player scripting are a future design track

**Status:** Accepted as a design constraint; implementation decision deferred

The user's long-term first-hand StoneAge play experience identifies a practical characteristic of the historical player experience: late-game progression could become extremely time-consuming when every repeated encounter required the full traditional transition into and execution of the turn-based battle scene. Third-party automation tools, accelerated-battle behavior and community-authored scripts became an important part of how many players actually played for long periods.

This is recorded as **USER EXPERIENCE / DESIGN INPUT**, not as a claim that third-party tools were part of an official clean client.

Project consequences:

- During archaeology and reverse engineering, official client/runtime data and third-party tools/scripts must remain technically separated so the project can identify what belonged to the original game and what belonged to the surrounding player ecosystem.
- Historical use of automation does **not** make a contaminated client executable acceptable as the clean baseline.
- During future reconstruction, do not automatically reproduce the original grind curve and then require an external tool to make the game practical.
- Also do not automatically erase the historical automation experience merely by flattening progression or reducing every experience requirement. Original pacing, repeated combat, convenience tooling and player-created automation should be studied together.
- Candidate modern solutions may include native fast battle, configurable auto-battle, repeat-battle controls, offline/simulation-style progression where appropriate, or an official sandboxed scripting/automation system.
- Historical player-created scripts are especially important as evidence of **emergent player tooling and community creativity**. A future scripting system may be considered as a first-class game feature rather than an uncontrolled external program, but its scope, security model, balance impact and UX are deferred until reconstruction begins.
- Final choices should be made only after recovered client/data analysis exposes the real combat timing, experience curve, encounter frequency, travel friction and progression structure.

No decision is made yet to ship an external-style addon, script engine, auto-combat system, or altered experience curve. The purpose of this decision is to ensure future reconstruction does not optimize away a major part of the historical play experience before it is understood.


## DD-011 — Online-recoverable bytes gate

**Status:** Accepted

The archaeology/recovery program is now constrained by a hard practical rule: **primary recovery work must target artifacts that can be obtained digitally over the internet at no cost and can be inspected or reproduced without requiring the user to acquire physical media.**

Preferred recovery targets are, in order:

1. complete client installers/archives that are directly downloadable;
2. publicly preserved ISO/BIN/CUE/IMG or equivalent optical-media images;
3. downloadable installed-client trees or independently preserved file sets;
4. first-party or preservation-hosted patches/runtime/resource files that can be byte-recovered;
5. exact filenames, historical download URLs, archive identifiers, hashes/checksums or file manifests that directly lead to one of the above.

Physical-only evidence is **non-primary**. Magazines, newspaper articles, auction listings, packaging photographs, disc photographs, product art and collector descriptions must not become open-ended research tracks merely to prove that an object existed, looked a certain way, or was once distributed.

A physical-media or publication lead may be reopened only when it creates a direct bridge to digitally retrievable bytes, for example:

- an exact downloadable filename or URL;
- a public preservation identifier;
- a freely accessible disc image;
- a checksum/hash that locates a public copy;
- a file tree or volume label that identifies a retrievable archive;
- an online mirror/carrier that exposes the client or disc contents.

The project will not buy, bid on, ship, borrow, request seller dumps of, or otherwise depend on physical media. This rule tightens DD-008 and operationalizes DD-009: **client-byte recovery and technical reverse engineering outrank physical provenance archaeology.**

Because an accepted Taiwan/Waei v1.0 clean baseline already exists, the project must not stall while waiting for an unrecoverable Mainland Dec-2000 physical test CD. If no earlier downloadable client can currently be recovered, work proceeds on the accepted v1.0 baseline: file-tree inventory, executable/runtime analysis, resource/container decoding, maps, characters, pets, items, skills, combat, data tables, UI, updater/network behavior and controlled version diffing. Earlier artifacts are integrated later when they become digitally recoverable.


## DD-012 — Early clean baseline as foundation; later official versions as a design library

**Status:** Accepted

The reconstruction project does not aim to freeze the final game at one historical StoneAge version. A sufficiently early, official, clean and technically complete client is used as the **foundation baseline** for understanding the original game's core architecture, data model, rules, content organization and player experience.

Later official StoneAge releases are then treated as a **design/content library**, not as mandatory cumulative upgrades. Their maps, pets, systems, quests, mechanics, convenience features, progression structures, world-building ideas and other content may be studied and selectively incorporated.

Every later-version element must be evaluated before inclusion. It may be:

- retained substantially as-is if it remains coherent and useful;
- adapted to fit the project's single-player architecture and modern pacing;
- redesigned to better fit the reconstructed world, progression and systems;
- merged with earlier concepts where that produces a cleaner design;
- omitted if it creates redundancy, incoherence, excessive grind, technical baggage or conflicts with the intended experience.

Therefore the final game is not defined as a strict clone of v1.0, 1.82 or any later official release. The historical baseline provides **ground truth and design DNA**; later official versions provide **validated source material and evolutionary evidence**; the final implementation is an independently designed modern StoneAge reconstruction guided by project principles.

This decision complements DD-003 and DD-011: recover enough trustworthy official material to understand the game deeply, then use historical versions as inputs to deliberate design rather than as immutable specifications.


## DD-013 — Single-player delivery with MMORPG-style systems and future rights-holder optionality

**Status:** Accepted

The project is developed and used as a **single-player/private game**, not as an unauthorized public online service. This is an intentional product boundary, especially while the work remains an independent reconstruction inspired by historical StoneAge material and before any rights-holder authorization exists.

However, the **gameplay model may deliberately preserve MMORPG-style design**. The single-player implementation may include persistent-character progression, long-form world progression, large content surfaces, repeatable combat, pet collection/growth, economy-like systems, quest chains, staged unlocks, travel friction, equipment/item loops, automation/convenience systems and other mechanics historically associated with an online RPG.

Therefore `single-player` describes the current **deployment and access model**, not a requirement to redesign the game into a short, linear conventional standalone RPG.

Architecture consequences:

- Core deterministic game rules should be separated from presentation and transport/network layers.
- World state, player state, NPC/pet/item data, progression and combat logic should use explicit data models rather than being tightly bound to one local UI process.
- Single-player persistence should be authoritative locally, while internal interfaces should avoid assumptions that make a future authorized client/server split unnecessarily difficult.
- Networking, account services, social systems, anti-cheat, live operations and multiplayer synchronization are **not current implementation requirements** and must not add premature complexity.
- Historical server/network research remains useful where it reveals original rules, authoritative state boundaries, protocol-driven content or data ownership, but the initial reconstructed product remains local-first.

Future optionality: if the project ever reaches a point where the relevant StoneAge rights-holder is willing to discuss authorization, licensing, collaboration or adoption, the reconstructed design and technical specifications should be capable of serving as a credible prototype/foundation for an officially authorized product. This is a possible future path, not an assumption or current claim of authorization.

Until such authorization exists, the project must not present itself as official, imply affiliation, or depend on public operation using protected StoneAge assets/branding. Production code and newly created/recreated assets should continue to follow DD-007's copyright-aware boundary.

## DD-014 — Preserve server-authoritative runtime map materialization semantics without reproducing legacy networking

**Status:** Accepted

The accepted Taiwan/Waei v1.0 runtime proves that ordinary field-map content may be created and updated in a local `map\\%d.dat` cache at runtime through the map `M` / `MC` protocol path rather than being required as preinstalled retail-disc files. Fixed descendant source is consistent with the same semantic boundary: the server owns map tile/object/event state, sends region checks/control, and supplies requested region payloads when the client cache is absent or stale.

The modern reconstruction must preserve this **authoritative map state -> runtime materialization** boundary while following DD-013's local-first deployment model.

Consequences:

- The single-player runtime does **not** need to reproduce sockets, LSSPROTO transport, account services, or a separate online map server merely to preserve historical map behavior.
- Engine-neutral local world data is authoritative at runtime. Historical map-delivery packets are evidence about data ownership and update semantics, not a mandatory production transport architecture.
- A recovered map that exists only on a preserved server surface may be decoded into the internal world-map representation when its provenance and format are sufficiently validated.
- Such content retains its actual provenance. In particular, recovered-2.5 server-only maps remain `LATER_RECOVERED`; the fact that the Taiwan-v1 runtime could download maps does **not** prove that a specific later map existed in Taiwan v1.
- The reconstruction must not fabricate a historical client DAT/MAP artifact in order to make a server-only map look client-native. Any compatibility cache generated for testing or emulation must be explicitly labeled derived/transient rather than original evidence.
- Map delivery should be modeled semantically as region validation, region request, and region materialization so the same deterministic world layer can support the current in-process single-player runtime and a possible future authorized client/server split without changing map provenance.

Evidence closure: `research/mechanics/STONEAGE-MAP-DELIVERY-MATERIALIZATION-R1.md`.



## DD-015 — Version-tagged runtime bootstrap contracts must preserve provenance and gated topology

**Status:** Accepted

Closed reconstruction evidence may be promoted into an engine-neutral runtime bootstrap contract only if the contract preserves its source version and evidence role.

The accepted Taiwan/Waei v1.0 client remains the historical foundation baseline. A recovered25 world/profile may be used as a deterministic implementation scaffold, but its maps, NPCs, items, progression rules and transitions remain `LATER_RECOVERED` unless separate evidence proves Taiwan-v1 membership.

Architecture consequences:

- runtime bootstrap contracts are version-tagged compositions, not flattened “canonical history” files;
- state-gated transports remain explicit conditional transitions and must never be inserted into an unconditional world graph;
- raw recovered identifiers/coordinates may be resolved through provenance-preserving adapters when they should not be copied into the public semantic contract;
- world/player/NPC/pet/item/progression/combat state stays independent of rendering engine and legacy network transport;
- the local-first runtime owns authoritative state; legacy networking is optional compatibility/evidence infrastructure;
- contradictory evidence produces a new/superseding contract version rather than silently changing provenance labels.

R1 implementation contract: `docs/RUNTIME-BOOTSTRAP-CONTRACT-R1.md` and `game/RUNTIME-BOOTSTRAP-RECOVERED25-R1.json`.


## DD-016 — Keep presentation replaceable; use Godot as the first spike candidate, not as runtime authority

**Status:** Accepted

The reconstructed runtime now has a closed semantic boundary above authoritative game state: runtime stack -> session coordinator -> local application facade -> semantic engine adapter. Presentation technology must remain downstream of that boundary.

As of the 2026-09-30 engine requirements audit, Godot 4.7.2 is the **primary presentation spike candidate** because its dedicated 2D tooling, Windows export path, MIT license and .NET option align strongly with this project's requirements. This is an evaluation priority, not a claim that Godot is already the permanent production engine.

Consequences:

- no renderer may become authoritative for world state, collision, save schema, recovered NPC/transition rules or provenance;
- engine code consumes semantic intents/views/results rather than recovered25 raw arguments or coordinates;
- classic Warp, dynamic occupancy and state-gated transition semantics remain in the deterministic runtime below presentation;
- Defold remains a lightweight secondary candidate, Unity a mature C# fallback and MonoGame a high-control baseline;
- engine-specific production work waits until the production runtime language/hosting boundary is closed;
- the Python reconstruction remains an executable evidence/reference surface unless and until a parity-tested production core supersedes individual modules.

Audit record: `docs/PRESENTATION-ENGINE-REQUIREMENTS-AUDIT-R1.md`.


## DD-017 — Separate Python reconstruction/oracle tooling from the future standalone C# production core

**Status:** Accepted

The repository's Python environment is primarily an evidence-recovery and executable-specification system. It must not be treated as a requirement to ship the whole reconstruction toolchain inside the final game.

The durable language boundary is:

- Python remains authoritative for archaeology, extraction, provenance audits and build-time normalization;
- closed Python deterministic models/tests remain the migration oracle;
- the preferred future production deterministic core is a standalone engine-neutral C# library;
- presentation engines consume that core through semantic facade/adapter boundaries and never become authoritative for recovered rules/state.

Raw recovered bundles should be transformed by audited Python tooling into versioned provenance-bearing runtime artifacts before gameplay. Python embedding is not the default shipping strategy.

Any C# replacement must demonstrate parity against versioned cross-language golden fixtures before the corresponding Python reference semantics are considered reproduced.

Architecture record: `docs/PRODUCTION-RUNTIME-LANGUAGE-HOSTING-R1.md`.


## DD-018 — Reconstruction acceptance precedes production-engine selection and redesigned content

**Status:** Accepted

The project follows a strict two-stage product sequence.

Stage A is historical/gameplay reconstruction: recover and validate enough of the original StoneAge client/server/world/gameplay behavior to understand the game as a coherent system, with explicit provenance and explicit unknowns.

Stage B begins only after an agreed reconstruction acceptance point. At that time the project owner and implementation work may choose the final production engine, decide which historical systems/content to retain or redesign, and begin building the new private single-player StoneAge derivative.

Consequences:

- current Godot/C#/engine research is retained as non-binding technical groundwork;
- no production port or engine scene work is on the active critical path while core restoration gaps remain;
- restoration runtime integration is preferred over speculative architecture work;
- later content/design decisions must not be silently mixed into historical reconstruction evidence;
- the recovered25 bridge remains version-tagged and cannot be promoted to Taiwan-v1 historical membership without evidence.

Current restoration integration target: connect the already reconstructed encounter/battle path into the recovered25 local runtime composition before resuming production-language migration.

## DD-019 — Guarded historical battle command numbers require compile-profile evidence

**Status:** Accepted

Macro-gated battle-command enums are not numerically portable historical identifiers. A symbolic command can resolve to different integers when earlier conditional enum members differ across descendant builds.

Consequences:

- preserve the symbolic command identity separately from its numeric COM1 representation;
- assign a historical numeric command only when the relevant compile/profile feature set is evidenced;
- recovered gameplay-data callback names alone do not justify selecting one descendant's enum number;
- when a recovered build profile is unresolved, historical numeric command emission remains fail-closed rather than choosing a convenient descendant value;
- a modern internal semantic token may be used only if it is explicitly distinguished from a claimed historical numeric COM1 value.

The first concrete case is `BATTLE_COM_S_ENEMYREHP`: the pinned gavin/iriselia profiles resolve it to **2014**, while pinned Bismarck resolves it to **2013** because an earlier guarded enum member differs.

Evidence record: `research/mechanics/STONEAGE-ENEMY-REHP-R1.md`.


## DD-020 — Keep pet ownership, default selection, and battle occupancy independent

**Status:** Accepted

The reconstruction must not infer the player's selected/default battle pet from
roster ownership or from the fact that only one allied pet currently exists in a
battle. These are three distinct authoritative states:

- **ownership** — the pet remains in the persistent player roster with its
  persistent HP/growth/identity;
- **default selection** — a nullable persistent roster slot identifies the pet
  selected by the historical DEFAULTPET-style state;
- **battle occupancy** — battle-local participation can end independently
  through recall/exit/death while ownership survives.

Consequences:

- player-death loyalty penalties read explicit default selection rather than
  choosing the first/only retained allied pet;
- a successful recall may clear default selection and active battle occupancy
  without deleting the pet or zeroing its HP;
- a blocked recall leaves both selection and occupancy intact;
- battle-return/save logic persists the selection state independently of the
  owned-pet collection;
- legacy saves that predate explicit selection migrate to **unknown/no selected
  pet**, not to an inferred pet;
- active coordinator battle context remains battle-local; ordinary world save
  persistence does not imply mid-battle disk resume.

This decision is engine-neutral and applies beyond the current 2BattleTimid
case. It prevents future pet skills, player-death rules, UI selection and battle
return from silently reintroducing the old “owned == selected == active”
shortcut.

Evidence/implementation boundary:
`specs/STONEAGE-2BATTLETIMID-RUNTIME-STATE-AUDIT-R1.md` and the accepted
2BattleTimid runtime integration.

## 2026-10-06 — Separate placement capability from actual command reachability

DESIGN: the pressure ledger's static positive skill-slot capability must be
reported separately from recovered natural selection. Any proposed ID638
closure uses an exact two-placement predicate and accepted bounded execution
profile, with identity mutations and exact-data CI. A global BattleModel
callback promotion is disallowed;641/649/650 are not admitted implicitly.
Nonzero ILLEGAL and zero actual wa weights are preserved. No promotion in the
command-entry audit; equipment/other actor paths need separate evidence.

## 2026-10-06 — ID638 placement-criterion review accepted without promotion

The accepted entry audit establishes negative configured-path results while
retaining original build/NPC/script uncertainty. Existing static pressure
closures support evaluating **conditional bounded capability** separately from
natural command-entry reachability. Proceed to an exact two-placement
predicate and complete pressure/native/runtime regression gate; preserve wa0
and actual normal selection0. Predicted2463/20/3 remains unaccepted until that
next gate passes. This audit leaves pressure2461/22/3 and promotes0 slots;
641/649/650 and broader actor/magic execution are not admitted.
