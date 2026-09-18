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
