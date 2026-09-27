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
