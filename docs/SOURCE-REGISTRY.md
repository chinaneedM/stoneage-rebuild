# Source Registry

This is the canonical ledger for historical sources. Entries should record provenance, date, source type, what the source proves, and what it does **not** prove.

## Confidence scale

- **S** — primary original artifact: verified client/binary, manual, packaging, official site/patch file.
- **A** — contemporaneous reputable press or archived first-party material.
- **B** — strong secondary source, later official retrospective, or well-provenanced community preservation.
- **C** — community recollection/repost; useful lead, not sufficient alone for decisive claims.

## Initial leads

### SRC-JP-1999-PRELAUNCH-01

- Type: contemporaneous Japanese magazine / press material
- Period: 1999 pre-launch
- Confidence: A
- Status: needs local archival capture and page-level notes
- Relevance: earliest known concept-stage descriptions, screenshots, intended gameplay emphasis.

### SRC-JP-1999-BETA-01

- Type: contemporaneous Japanese beta announcement/coverage
- Period: 1999-09
- Confidence: A
- Status: client binary not yet recovered
- Relevance: proves existence of a public beta and narrows first recoverable client target.

### SRC-JP-1999-RETAIL-01

- Type: JSS first-edition retail package / CD-ROM evidence
- Period: 1999 launch
- Confidence: S if physical media can be acquired or imaged with provenance; otherwise B/A depending record
- Status: packaging evidence located previously; original verified disc image still missing
- Relevance: top-priority launch artifact.

### SRC-JP-2003-REVIVAL-01

- Type: Japanese revival client / press coverage
- Period: 2003
- Confidence: A/S depending artifact
- Status: historically useful near-relative, but not equivalent to 1999 launch
- Relevance: may preserve substantial earlier code/assets and can become a diff anchor if recovered.

### SRC-TW-2000-EARLY-01

- Type: early Taiwan launch material
- Period: 2000
- Confidence: A/B depending individual artifact
- Status: needs systematic recovery
- Relevance: first major localization/evolution branch to compare against JSS.

### SRC-CN-1.82-01

- Type: Mainland China 1.82 client/data/source candidates
- Period: early Mainland era
- Confidence: unresolved per artifact
- Status: several community references exist; provenance must be checked before treating any package as canonical
- Relevance: childhood/reference baseline and major diff target.

## Required metadata for future entries

Every substantial source should record:

- Source ID
- title/filename
- original date
- archive/download URL or physical provenance
- retrieval date
- language/region
- source type
- checksum if file-based
- confidence grade
- exact claims supported
- exact claims not supported
- notes on alterations/repacking
