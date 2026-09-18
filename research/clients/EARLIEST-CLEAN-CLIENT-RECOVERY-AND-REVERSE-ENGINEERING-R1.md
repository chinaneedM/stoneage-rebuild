# Earliest Clean Client Recovery & Reverse Engineering Plan — R1

Date: 2026-09-18

## Objective

Recover the earliest **freely/publicly obtainable, provenance-preserving, minimally modified** StoneAge client artifact and use its actual bytes/files as the primary specification source for the modern rebuild.

The target is not "the oldest version we can describe historically." The target is "the oldest trustworthy client we can actually obtain and inspect."

## Candidate ladder

Search all branches in parallel rather than waiting indefinitely for one perfect artifact:

1. 1999 JSS beta / retail / official updater files.
2. Korean 1.74.
3. Japanese revival 1.74a.
4. Earliest Taiwan operator clients.
5. Early Mainland clients, including 1.82.
6. Later clean clients only when needed as technical controls.

The first candidate that passes provenance and contamination checks becomes the bridge specimen.

## Version-label rule

A historical page, server name, archive filename, forum post or launcher label is **not sufficient evidence of the client build contained in the bytes**.

Concrete example: a 2003 Beijing Wayi statement says its anniversary "1.82 server" could be entered using the then-current `宠物进化史` client. Therefore a period page labelled "1.82 client/download" must still be verified from the recovered executable, resource set and file tree before being classified as an original 1.82 build.

Version attribution should use, where available:

- PE/file version resources;
- embedded version strings;
- installer metadata;
- operator/domain configuration;
- file-tree/resource-generation fingerprints;
- comparison with independently recovered copies.

## Clean-client acceptance test

For every candidate record:

- source URL / archive / mirror provenance;
- original archive or installer filename;
- byte size;
- SHA-256 and preferably MD5/SHA-1 when historical databases use them;
- archive timestamps and internal file timestamps;
- complete file tree;
- executable names and PE metadata;
- installer metadata;
- unexpected launchers, injectors, private-server IP/domain patches, custom logos, replaced assets, DLL loaders or patchers;
- version strings and region/operator identifiers;
- comparison against other copies of the same claimed version.

Classification:

- **A — clean/provenance-preserving bridge specimen:** strong evidence of operator/original distribution and no known modification.
- **B — likely clean:** consistent old client with limited provenance; usable only with explicit caveats and cross-copy comparison.
- **C — modified/repacked/unknown:** useful for hints or format archaeology, not a baseline.
- **REJECT:** demonstrated repack, server bundle, injected/customized client, or mismatched claimed version.

## Reverse-engineering sequence after recovery

### 1. Preservation inventory

Produce hashes, file tree, timestamps, archive structure and executable metadata. Original proprietary payload remains outside the repository by default.

### 2. Runtime architecture

Identify launcher/updater/game executable relationships, configuration, dependencies, network endpoints/protocol clues and client/server boundary.

### 3. Resource system

Identify index/data pairs, graphics containers, sprite/animation formats, palettes, compression, audio, fonts and UI resources.

### 4. World data

Recover map formats, map IDs, tiles, collisions, warps, NPC/event placements and location naming.

### 5. Entity/data model

Recover characters, pets, items, equipment, skills, attributes/stat tables, growth data, elemental data, status effects and other deterministic records.

### 6. Gameplay/system reconstruction

Determine what can be reconstructed from client-side data/code and what historically depended on server logic. Do not invent absent server rules; mark them OPEN until another source resolves them.

### 7. Cross-version diffing

As additional clean clients are recovered, diff executables, resources and tables to establish inheritance and additions. This replaces broad historical speculation with artifact-level evolution evidence.

## Repository outputs

Commit only:

- hashes and metadata;
- file-tree inventories;
- format specifications;
- independently written parsers/extractors;
- schema definitions;
- diff reports;
- derived, non-proprietary research findings;
- deterministic tests and legally appropriate tiny fixtures.

Do not commit proprietary original client archives/assets by default.

## De-prioritized work

Do not spend sustained project time on:

- historical retail pricing;
- JAN/model-number reconstruction;
- collector accessories;
- staff biography;
- package completeness;
- general launch chronology;

unless that work directly helps recover/authenticate a client or resolve a technical question.
