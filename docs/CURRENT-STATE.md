# Current State

Last updated: 2026-09-18

## Current phase

**Phase 0 — StoneAge Origin Archaeology**

The independent GitHub repository and continuity scaffold are established on remote `main`, and GitHub read/write continuity has been verified through live documentation commits.

## Confirmed project direction

- Single-player game, not a commercial MMORPG operation.
- Historical clients and materials are research samples, not code/assets to copy directly into the new game.
- Start from the earliest traceable JSS-era StoneAge rather than assuming Mainland China 1.82 is the absolute origin.
- Mainland 1.82 remains a major reference point because it is close to the user's childhood experience and is commonly remembered as a classic early form.
- Later systems/content may ultimately be integrated, but through coherent progression rather than a feature dump.
- Emotional milestones such as first pet capture, first ride, first major exploration, etc. are part of the design target.

## Current historical working picture

### FACT / high-confidence working facts

- StoneAge was developed by Japan System Supply (JSS).
- Public exhibition material exists by Tokyo Game Show '99 Spring.
- By May 1999, contemporaneous `Play Online` coverage described the planned game as a relaxed Stone Age RPG emphasizing food/resources, community, and cooperative village development. This is now treated as FACT for **published pre-launch design intent**, not automatically as proof of final shipped implementation.
- A beta test ran from **1999-09-01 through 1999-09-30**, supported by contemporaneous `Play Online` issue 015.
- PC Watch reported on 1999-09-17 that the JSS title was scheduled for release on **1999-10-15**.
- A later 4Gamer retrospective states that Japanese service actually started on **1999-10-15**; this date is now the high-confidence working commercial start date.
- Taiwan and Mainland Chinese versions followed later and introduced localization/iteration layers.

Precise claims remain tied to records in `SOURCE-REGISTRY.md`. See `research/origin/JSS-1999-ORIGIN-EVIDENCE-R1.md` for the current 1999 evidence pass.

### HYPOTHESIS

- The earliest StoneAge concept may have been much simpler in macro-lore than later versions, even though resource/community/village-life themes are now directly attested in May 1999 design coverage.
- Much of the later macro-lore may have been progressively added to explain and extend an initially simpler world.
- Some mechanics remembered as "core StoneAge" by later players may not have existed for normal players in the earliest Japanese operation.

These remain research hypotheses unless a source record supports a narrower factual statement.

## Highest-priority research questions

1. **Locate and verify the earliest recoverable JSS retail client / retail CD image.**
   - Progress: a concrete surviving `STONEAGE 初回限定版` physical-package lead has been located and recorded as `SRC-JP-1999-RETAIL-MERCARI-01`.
   - Still missing: provenance-preserving disc image/dump, file tree, hashes, executable/version metadata, manual/insert capture.
2. **Locate the September 1999 beta client or reliable binary/packaging evidence.**
   - Progress: beta period is now bounded to 1999-09-01 through 1999-09-30 by contemporaneous evidence.
   - Still missing: installer filename, distribution method/media, hashes, internal version, beta-to-retail diff.
3. Recover JSS launch manual/box inserts and original world-setting text.
4. Determine the earliest documented appearance of:
   - the name "Nies / ニース / 尼斯";
   - the island-continent geography;
   - elemental/spirit lore;
   - pet riding for normal players;
   - major villages and early map topology.
5. Determine JSS-era internal client version numbering.
6. Locate the earliest Taiwan client/manual/site and compare it with JSS material.
7. Locate a clean Mainland early/1.82 client/data set for later diff archaeology.

## Completed in the latest work pass

- Read and obeyed `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` from the remote repository.
- Verified repository `chinaneedM/stoneage-rebuild`, default branch `main`, and live write access.
- Inspected current remote state and latest commit history before resuming work.
- Added `research/origin/JSS-1999-ORIGIN-EVIDENCE-R1.md`.
- Expanded `docs/SOURCE-REGISTRY.md` with structured records for:
  - May 1999 `Play Online` design coverage;
  - September 1999 `Play Online` beta coverage;
  - 1999-09-17 PC Watch Tokyo Game Show report;
  - 2009 4Gamer launch-date retrospective;
  - surviving first-edition physical-package marketplace lead.
- Tightened `docs/HISTORICAL-TIMELINE.md` with sourced 1999 milestones and explicit evidence limits.
- Promoted resource/community/cooperative-village themes from broad hypothesis to FACT only at the narrower level of documented May 1999 pre-launch design intent.

## Immediate next actions

1. Continue the **physical-media recovery track** for the 1999 JSS initial edition: identify additional surviving package/disc listings, collector archives, product identifiers, disc-label photographs, and any lawful provenance-preserving image/dump lead.
2. In parallel, search for **September 1999 beta distribution traces**: installer filenames, magazine CD-ROMs, Gamer's Dream download pages, archived JSS/NTT pages, tester instructions, README files, and old personal download directories/indexes.
3. Capture exact page-level metadata for `Play Online` issues 012 and 015 and add stable archival hashes/notes where legally appropriate.
4. Once any original binary/media is recovered, immediately establish the reproducible client-archaeology pipeline: hashes, PE metadata, file tree, resource inventory, string extraction, asset IDs, and cross-version diff.

## Continuity status

- Repository: `chinaneedM/stoneage-rebuild`
- Default branch: `main`
- Visibility: public
- Authority: latest GitHub remote state is the single source of truth for project continuity.
- Canonical restart protocol: `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`

## Blockers

No repository or workflow blocker.

The substantive blocker is artifact availability: the project still lacks a verified 1999 JSS retail disc image/client and September 1999 beta binary. Research can continue without them, but executable/file-level archaeology cannot begin until at least one provenance-sufficient binary artifact is recovered.
