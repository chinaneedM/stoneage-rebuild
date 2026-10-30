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

## 2026-10-06 — Placement-aware conditional capability status

Use closed_conditional_runtime for exact ID638 slots, separately from existing
closed_runtime. Complete closed-capability totals include both; every
conditional row declares its bounded scope and reachability not inferred.
Generic callback classification remains OPEN. Factory-verified complete file/
loaded-object identity is required to qualify either placement; incomplete
identity cannot become a callback-wide closure. Current evaluation PENDING.


## 2026-10-06 — ID638 capability and reachability remain separate acceptance axes

The exact recovered25 placements (1178,2,638) and (1179,2,638) may be counted as
**CONDITIONAL_BOUNDED_CAPABILITY** only when the verified whole-file/semantic
certificate and the named enemy-only explicit-selected empty-equipment R1 scope
are present. This closes those two static capability placements without asserting
that the recovered game naturally selects or exposes the command. Global
BattleModel callback closure is forbidden; natural AI/PET/magic/NPC/script and
original-build reachability remain independent evidence gates. Accepted pressure
is 2486=2463 closed capability+20 OPEN+3 historical UB; next OPEN is BecomeFox
ID625. Receipt: `STONEAGE-BATTLEMODEL-CONDITIONAL-PLACEMENT-ACCEPTANCE-R1.json`.


## 2026-10-06 — BecomeFox reference must preserve source-profile state-access divergence

BecomeFox's exact recovered25 data identity is closed independently from runtime
semantics. The modern implementation must not flatten the pinned descendant
PetIn disagreement: gavin/iris use ordinary integer accessors for FOXROUND while
Bismarck uses work-state accessors. Until executable evidence resolves which
profile matches the recovered binary, ordered/runtime work must model this as an
explicit versioned boundary. Exact recovered25 ID625/placements alone are not a
runtime-pressure promotion.

## DD-021 — Finish evidence-bounded original reconstruction before jointly designing the new StoneAge

**Status:** Accepted — explicitly reaffirmed by the user on 2026-10-12.

The two stages are sequential rather than parallel production efforts.

**Stage A: Historical restoration and independent acceptance.** Recover all
reasonably retrievable early StoneAge clients, datasets and mechanics that
materially bear on original authenticity and the future game's core design.
Treat the Taiwan Waei/JSS v1.0 clean disc as the working foundation; trace
the JSS origin, Mainland 1.82 and other version branches without imputing a
later mechanic to v1.0. Audit maps/world/server-only content, NPCs, quests,
players, pets, battle, growth, items, skills, economy, UI, graphics, audio,
network protocol, runtime, state and native persistence. Preserve every
important unresolved or historically inaccessible element explicitly as OPEN
rather than fabricating full restoration. Tests and engine-neutral executable
golden models used to verify recovered specifications remain within Stage A.

**Stage B: Collaborative new-game architecture and content design.** Only
after Stage A's auditable restoration gate is reviewed do the user and assistant
jointly decide the new game's engine, systems, narrative progression, assets,
UI and production roadmap. No historical discovery automatically authorizes
copying a later version's gameplay into the new game. The eventual result
remains a locally operated, modern single-player game.

No ungrounded completion percentage constitutes Stage A acceptance. Technical
closure must be measured by subsystem coverage, source provenance, cross-system
verification, explicitly bounded unknowns and a version-separated acceptance
matrix. Unrecoverable server-only content may close as a documented
evidence-limited historical gap, not as a fictional FACT.

Gate record: `docs/RESTORATION-PHASE-GATE-R1.md`. The immediate work order
remains TW1.0 R14 original static provenance; this decision does not replace it.


## DD-022 — Plan restoration by gameplay outcomes and bounded evidence value

**Status:** Adopted research work order — 2026-10-16, following the user's
explicit request that the assistant plan and judge the necessity of recovery.
This is not a new-game engine/content design decision. DD-021 still binds.

A restoration work package must identify a game behavior/content deliverable,
material evidence gap, source/version scope and stopping condition. Technical
helpers are dependencies only where they affect that deliverable. Consecutive
work without a domain result triggers portfolio reassessment after two units;
R/test counts do not measure whole-game recovery.

Use `docs/RESTORATION-ROADMAP-R2.md` and the latest CURRENT-STATE. Begin PET-STATE-01
using the current capture/bridge/coordinator field-source gap. WORLD-01 reuses
the four closed hometown routes only for a later finite24-cell review.
Pause further deep client-local savedata helper expansion (old NEXT R79) as
non-blocking. Preserve all existing evidence and explicit unknowns. Reopen only
for new business-field evidence, a concrete core-rule contradiction or the
smallest necessary dependency blocking a named integration specification.
Original client-local state, descendant server character saves and modern
reference local persistence are separate evidence layers. No subsystem family
is closed by this reordering. Stage A remains before joint Stage B review.


## DD-023 — Early first-party player-service scope before further late NPC scanning

**Adopted for Stage A research on 2026-10-17**. On current evidence, the 2001-04-18 first-party JSS manual offers five source-bounded early player service classes, while the accepted TW1.0 client offers separately sourced generic state/window/position message carriers. They are not one authenticated version-matched service transaction. Prioritize `EARLY-VILLAGE-SERVICE-JOURNEY-01`, a finite action/precondition/observable-state/missing-original-server-input contract, over further recovered25 NPC parameter scans. Carry late NPC EventEnd joins only as descendant evidence; preserve missing original NPC/world/ACK and runtime client visuals as OPEN. Park R79. If two consecutive work units yield no new game behavior, source attribution or material integration evidence, return to portfolio review. No new game design or Stage B.


## DD-024 — Accept an evidence-limited Stage A research checkpoint and prepare collaborative Stage B design

**Status:** Accepted as a user-delegated *research-stage disposition* on
2026-10-17; **not** a claim that the authentic original StoneAge game is
fully recovered and **not** approval to start Stage B production.

The user authorized the assistant to choose the best of the proposed Stage A
decisions, explicitly allowing later correction: “按照你认为的最优解选择就行 哪怕后续出现错误需要补充改正我们还可以改 我相信你的选择”.
The selected option is **B** from the existing nine-system
`STAGE-A-JOINT-REVIEW-DECISION-01`:
preserve the auditable, version-bounded historical research and label the
currently unobtainable server-only fields OPEN_EVIDENCE_LIMITED instead of
endlessly broadening late-source helper research.

This supersedes earlier Stage A acceptance *pending* status at the current
decision time, **without rewriting the pre-decision review documents**.
The verified historical system statuses remain **7 PARTIAL + 2 OPEN**, not
CLOSED or 100%. TW1.0 and JSS1999 original commercial world/NPC/event/save
execution cannot be inferred from descendant assets, later C code, or modern
synthetic replay. Savedata R79 remains PAUSED_NON_BLOCKING.

The project may now **prepare a joint Stage B new-game design discussion**,
consistent with DD-016/017/018/021: original feeling first, then selectively
absorb later elements via separate, explicitly versioned DESIGN decisions.
Godot remains a presentation spike *candidate*, standalone C# deterministic
core an architecture *preference*, and Python an archaeology/oracle system;
none is a locked shipping configuration. No productive engine work, new
copyrighted assets or plot/quest production is authorized by this limited
stage decision. First substantial next milestone is
`STAGE-B-JOINT-DESIGN-DIRECTION-01`: agree on gameplay pillars, early
world narrative and scope, pet/battle progression, first ride milestone,
asset policy, and staged technical prototype criteria.

New authenticated source or a material rule contradiction reopens the
smallest named Stage A area through recorded revision rather than
discarding the Stage A archive. The acceptance document, source-gate manifest,
machine-verifiable continuity and CI acceptance are controlling. Any older
“highest NEXT” referring to deeper recovered NPC or R79 work is historical,
not currently operative.


## DD-025 — Treat legacy automation and full pet-content crosswalk as required new-game design inputs

**Status:** Research/input priority accepted on 2026-10-17 in response to
the user's explicit clarification that classic StoneAge external helpers were
crucial to its historical experience, should be studied across generations
and selectively adapted into a *built-in* new-game assistant. This is
**not** authorization to start Stage B production or to clone any old cheat.

Record the classic versus late-assistant genealogy separately, with earliest
documented date, regional/client compatibility, release version, behavior,
history/quality-of-life versus exploit category, and first-party versus
reprint confidence. Positive native candidates: pet growth/IV history,
auto-heal with real consumables, legal navigation, repeat-crafting convenience,
battle preferences, statistics, and contextual encyclopedia. Historically
document duplication, packet tampering, illegitimate teleports and
server privilege bypass only for cultural/technical context. Unbounded
auto-play or scripted behavior remains gated by later explicit joint design
decision and must never bypass authoritative game-state rules.

The user's explicit question about all old pets, art, animated models,
growth and quests reopens a *named finite content coverage review* before
ratifying an all-pet new-game database. Original v1 direct sprite/bitmap
containers, server-delivered original world, later recovered25 enemybase,
modern rule fixtures, and new-game content must remain separate source
layers. The classic visuals are primarily **2D sprites**, not an established
inventory of per-pet 3D models. A decoded picture-count is not a pet species
count. A later enemybase row is not an original TW1.0 pet identity.
Even a descendant pet growth algorithm cannot assert every original
same-build growth value or 1999 coefficient.

The prior Stage A *evidence-limited review decision* remains valid as a
historical milestone, but does not foreclose new named archival/content
crosswalk work when the user identifies material missing design inputs.
**Highest NEXT PET-ASSET-GROWTH-CATALOG-MATRIX-02** with auxiliary
`LEGACY-ASSISTANT-PROVENANCE-EXPANSION-02`. These are research/coverage
deliverables, NOT production-game asset imports. Before a comprehensive
pet roster or in-game automation is implemented, the applicable source
matrices and new-game design gates must be reviewed.


## DD-026 — Complete a versioned historical content archive before new game and future guide-site production

**Status:** User-directed preparation requirement accepted on 2026-10-17.
The project owner reinforced that the historic content itself—the original
NPCs/quests, full pet data and graphics/growth, login and creation screens,
character 2D sprite "models", dialogue, map, items and every documented
legacy helper function—is a **first-class design source**. Finish the
reasonably source-recoverable preparation coverage and record exact gaps
**before starting production design/build**, rather than equating a Stage A
bounded historical literature checkpoint with a complete original-game
content database.

A future standalone game may also need a **player reference website** for
quests, pet encyclopedia, maps, historical and new-game skills and other
player-facing knowledge similar in utility to early publisher sites.
This is an **eventual product option**, not current approval to launch a
website, register a domain, reproduce publisher copyrighted text/images
or host public assets. A common provenance-bearing record layer now
supports both future game content derivation and rights-cleared wiki export,
with distinct source version, evidence quality, UNKNOWN fields, record
revision and copyright/publication approval.

Legacy cheat/helper archives should attempt to enumerate **all historically
evidenced versions and functions** before adoption discussions, including
features that will likely be rejected. Preserve period, first evidence,
inputs, intended behavior, what was actually observed, source code/binary
custody where lawful, and exact unsourced claims. This is archival
**functional specification**, not blanket permission to execute unsafe
unknown programs or re-create historical exploits against third-party
servers. Keep positive convenience functions separated from duping,
unauthorized teleport, packet-bypass and cheating.

Adopt `docs/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.md` and its
machine manifest as current research architecture: 22 source-content
domains, seven version profiles, fifteen necessary cross-system
evidence links, future data model with nineteen search collections, and
the five bounded preparation work packages. Follow the highest
`PET-ASSET-GROWTH-CATALOG-MATRIX-02` first; do not add another
purely conceptual R number without an actual verifiable table/source
connection. DD-024's Stage A evidence-limited historical milestone
remains on record and DD-025's tool and pet completeness emphasis
remains active. Stage B production and public wiki publication remain
gated by subsequent collaborative choices.


## DD-027 — Archive all source-recoverable official versions as a future design reference library

**Status:** Accepted user direction on 2026-10-18. The owner explicitly proposed
collecting the pets, quests, other content, models and gameplay of all official
versions so they can inform the new StoneAge even when ultimately unused.
This clarifies and broadens DD-003/025/026's practical collection scope.

Maintain two connected research tracks: an early historical restoration
baseline, and a broad official-version reference library. Later official
content is eligible for collection on its own merits without first proving
it belonged to JSS1999 or Taiwan1.0. Early-build identity remains required
only for claims specifically attributed to those builds. No earlier baseline
record or unresolved original-server gap is overwritten by this scope change.

The library covers authenticated official product releases, patches, regional
operator branches, temporary events and subsequently changed/retired features.
Official IP derivatives or different products may be useful references but
receive separate product/lineage records; they do not automatically share
entities, resources or rules. Community/private-server modifications and
legacy external helpers keep their existing separate provenance categories.

Collect pet species/variants, stats/growth/capture/locations/skills/riding;
NPCs, dialogue, quest prerequisites/steps/rewards and events; world/maps;
characters, 2D sprites or authenticated 3D models, animations and UI; items,
crafting/economy, battle, social/progression systems and official assistance
features where evidenced. A count of pictures or source rows is not a species
or fully recovered-content count. Do not assume every release used 3D assets.

Every record carries product/operator/region/language, version/build or explicit
UNKNOWN, source and observed dates, entity identity, actual content/behavior,
visual/resource reference, evidence quality and completeness. Record changes,
renames, additions/removals and conflicts with exact source boundaries. Shared
names or numeric IDs alone cannot establish cross-version entity identity.
Preserve unknown fields instead of copying another version's values.

Archive useful and unused content alike; adoption, adaptation or rejection
for the new game is a later joint DESIGN decision. Reference eligibility
does not grant production asset reuse or permission to republish originals.
Existing copyright/custody, source-only claims, Stage B and wiki gates apply.

The coverage ambition is all source-recoverable official versions. Execute
finite packages ranked by design value, source recoverability and current
gaps: maintain a release/source inventory, derive content tables and visual
references, then compare material changes while deduplicating unchanged
records. Do not require exhaustive recovery of every release before useful
review can occur. Explicit missing releases/content remain in the coverage
ledger. The next22-domain review must include this broad official-version
coverage and choose a concrete content source, rather than restricting every
new package to early-build identity or adding more low-level helper analysis.


### DD-027 supplement — Official world history, story continuity and proactive coverage

On2026-10-18 the owner clarified that official-version development, world
history and stories should inform the future world's construction, and asked
the assistant to identify missing dimensions proactively. Extend the archive
from isolated content lists to source-qualified relationships among stories,
places, peoples, pets and mechanics. This is archival preparation; the new
world's actual canon and production remain later joint DESIGN decisions.

Keep two separate chronologies: real product/operator releases and the
fictional world's internal sequence. Store narrative continuation, prequel,
parallel/regional branch, translation/name variation, retcon/contradiction,
mechanics-only change, and UNKNOWN as distinct relation types. An official
update date alone does not establish an in-world year or a single continuous
universal canon. Claimed links require named sources and version identity.

Source-supported coverage includes geography and travel; ecology/habitats
and the role of pets; settlements, peoples, factions and relationships;
myths, beliefs, civilization and technology; named characters' motives and
quest consequences; events' persistent or temporary world changes; everyday
life/economy; and player/pet progression and emotional milestones. Questions
with no evidence remain research prompts, not invented ancient lore.

For each substantial system, record its earliest supported version, later
changes, documented narrative context, player-facing purpose and experiential
tradeoffs where evidenced. Original developer intent needs a source; an
analyst's interpretation is HYPOTHESIS. A proposed future explanation—such
as a new civilization or domestication arc—is DESIGN, never backfilled into
historical canon. Retain discarded and contradictory source ideas for review.

The assistant owns proactive gap discovery and finite source prioritization
across these dimensions. Use existing22-domain categories and add narrative
relationship annotations rather than treating a new checklist as recovered
content or letting planning replace material-source acquisition. Protect
the early StoneAge emotional arc, including earning the first pet ride,
when later joint design chooses among the collected references.


## DD-028 — Separate base-game quests from operator events and permanent version additions (2026-10-24)

**Status:** Accepted, direct owner direction. The owner explicitly requires activities created by individual operating companies for festivals or special dates to be kept separate from the game's original/core quests. This is a research/archive classification decision, not adoption of any future new-game quest.

The canonical classification contract is `docs/QUEST-ORIGIN-TAXONOMY-R1.md`; source-pinned correction overlay is `research/recovered/STONEAGE-QUEST-ORIGIN-SEPARATION-R1.json`. All quest discoveries must enter exactly one of `BASE_GAME_QUEST`, `PERMANENT_VERSION_QUEST`, `OPERATOR_EVENT_QUEST`, `ORIGIN_UNRESOLVED`. Keep operator, region, original version and whether introduced at launch vs as a permanent patch separate; no named quest in an old guide is automatically part of the original game's core.

Seasonal/anniversary/one-off activities (including non-quest GM reward ceremonies) are maintained in independent operator-event archives, never merged with the base-game quest list. Distinguish `EVENT_ACTIVITY_CLAIM` from an actual scripted `EVENT_QUEST_CLAIM`. Published announcement, actual server execution, event duration, recurring return and post-event permanent feature retention are independent facts. Festival identity alone does not establish exact close date. Operator identity without authenticated attribution remains explicitly qualified.

Prior source records and accepted custody are immutable. R115 Mid-Autumn 2003, R110 JP Christmas 2004, R111 JP 2009 anniversary and R112 CN 2001 Valentine's GM campaign are separated into the operator-event overlay; R114 merchant-elephant and R113 Spirit King version narratives remain `ORIGIN_UNRESOLVED` until positive original/base, permanent-version or event evidence is found. No currently reviewed item is promoted to a verified original JSS1999/TW1.0 base quest. Corrections use dated overlays, not edits to original blobs or retrospective source confidence inflation.

## DD-029 — Artifact-first multi-version official client acquisition and lossless deduplication

**Status:** Accepted — user priority change on 2026-10-24.

Prioritize authentic preserved bytes of every publicly recoverable official StoneAge client, update package and regional build over speculative reconstruction from later web/forum descriptions. Exact distribution provenance, declared versus independently observed version, operator, region and modification risk must be recorded separately; a community client/server bundle is not automatically an official clean client.

Retain original packages and complete source custody without deleting apparent duplicates. SHA-256-equal extracted files may be stored/processed once through a content-addressed index while their full per-version occurrences remain. De-duplicate container records separately using format-aware parsing. File hash equality proves neither pet species equivalence nor identical NPC/quest/server scripts. Contradictory versions and translation variations remain traceable.

The first priority is to reconnect previously acquired Taiwan 1.0 and preserved 2.5 bytes; the older TW1/2.5 resource-prefix evidence and new 383-vs-2302 file SHA join are valid derived inventory evidence but not newly downloaded binaries. Continue early Japanese/Korean and mainland/regional clean official clients as source availability allows. Client-only data gaps require actual server/master sources rather than fabricated formulas.

All archive downloads must be lawful and malware-aware, inspected offline where possible, and proprietary executable/art/sound payloads kept outside the public Git repository by default. Event quests must remain separate from base/long-lived quests under DD-028. This changes the research work order, not the closed Stage A evidence-limited review or gated game-production status.

## DD-030 — Simplified Chinese production and dual-track original-experience reconstruction

**Status:** Accepted — user instruction on 2026-10-27.

The user's remembered experience is the Mainland Chinese version. The **future new single-player StoneAge must use Simplified Chinese (zh-CN / zh-Hans-CN) as its default and authoritative presentation locale**: interface, tutorials, quest dialogue, system names, item/pet/UI labels, error and accessibility messages, and documentation seen by the player. New production text will be UTF-8 Unicode; no CP950/Shift-JIS/GBK runtime dependency is permitted in the modern game. Localization support may be added later, but must not displace Simplified Chinese as the default.

This is a **future-game design choice**, not a claim that JSS Japan 1999, Taiwan Waei v1.0, Korean releases and Mainland editions used the same build, content, chronology or language. Originals retain immutable (where available) raw bytes, file hashes, build/region/operator/date qualifiers, original string decoding with per-source evidence, and source-local identifiers. Do not automatically convert Traditional-to-Simplified and overwrite the original or collapse two historically distinct terms. An explicit curated, versioned text map will later connect verified source terms to Simplified Chinese product terms, recording ambiguity/conflicts and original quest-vs-event provenance under DD-028. Taiwan-v1 remains an evidence foundation; Mainland experience is a prioritized **user-experience reference** where evidenced.

**Restoration observation now follows two complementary paths, with neither allowed to masquerade as the other:**

- **Original executable observation**: isolate old Windows/Wine client and (where evidence permits) a loopback-only local experimental server. A genuinely observed original-client frame, input response and sound may qualify only with actual native process/source/record provenance. This path may be blocked by system locale, 8-bit palette, extinct original server or storage and must not block all progress indefinitely.
- **Modern offline resource-experience observer**: use existing SHA-qualified original/descendant image, animation, map and WAV parsers as inputs to a clean current-platform observation surface. It can display, animate and move an **artificial observation marker** and play a user-selected WAV, with explicit version/build/evidence labels. Its synthetic movement, color assignment, scene layout and event mappings are **not evidence** of original gameplay; only externally authenticated local asset bytes can be discussed as original. This is an archaeology instrument, not premature production-engine selection or the new game's content.
  
Order: connect verified same-source PNG/timeline and map/locale assets to the modern observer and collect reproducible observation/coverage gaps; continue authentic legacy client startup only when a qualified isolated environment becomes available. If source art cannot be accessed, show a clearly marked synthetic grid rather than fabricate original screenshots. No proprietary images/audio/binaries in public Git or automatic upload.

Original world entry, battle, riding, audio-to-event mapping, official NPC/quest identities and overall restoration percentage remain unproven until individually accepted. The priority changes; no earlier R1–R46 result is erased.


## DD-OFFLINE-20261030 — 单机原素材观察成为当前最高执行优先级

用户于2026-10-30明确复申：原客户端不需要联网/重建原网服，未来新石器单机，项目侧自主决定原素材还原步骤。**阶段一仍是原资料复原，现代离线工具只是观察手段而不是新游戏上线。** 强制优先从已经校验的官方客户端原始地图/图像/SPR/WAV出发，做可重复的本地观察与有限场景拼合；旧服务器运行、账号、数据库、网络兼容变为非阻塞研究支线，只在能直接解决素材/场景认证缺口时重开。网页、玩家截图、各版图库仅作为版本对照和缺件旁证，不得取代能解码的已拥有客户端原资源。

实现止点、首个私人一键原帧工具及O1—O5次序见 `docs/continuity/STONEAGE-SINGLEPLAYER-ASSET-FIRST-20261030.md`。只读原件/private output、源SHA、无客户端/服务端执行、不过度宣称实体ID/原世界已进入是硬门槛。用户的版权动机不构成免许可：未获明确授权时原商业素材不得从私有研究包转入公开仓库或未来游戏分发。此条决策不回写原CURRENT旧事实、不同地区/年代不可混号、任务活动/常驻不可混类、Stage A/B/wiki/R79以及总体未知均维持。
