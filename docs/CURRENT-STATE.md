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
- `STONEAGE` was already being publicly exhibited at Tokyo Game Show '99 Spring by **1999-03-19**, in NTT Data's Gamer's Dream booth.
- By May 1999, contemporaneous `Play Online` coverage described the planned game as a relaxed Stone Age RPG emphasizing food/resources, community, and cooperative village development. This is treated as FACT for **published pre-launch design intent**, not automatically as proof of final shipped implementation.
- A beta test ran from **1999-09-01 through 1999-09-30**, supported by contemporaneous `Play Online` issue 015.
- PC Watch reported on 1999-09-17 that the JSS title was scheduled for release on **1999-10-15**.
- A photographed period retail advertisement gives Windows 95/98 as platform, **1999-10-15** as scheduled release date, **8,800 yen before tax** as planned price, and prints the period domains `www.titan.co.jp` and `www.gamersdream.ne.jp`.
- The same advertisement visibly promotes an original mug as a reservation bonus and a `STONEAGE` special CD as an initial-edition bonus/feature.
- A later 4Gamer retrospective states that Japanese service actually started on **1999-10-15**; this date is now the high-confidence working commercial start date.
- Taiwan and Mainland Chinese versions followed later and introduced localization/iteration layers.

Precise claims are tied to records in `SOURCE-REGISTRY.md`. See `research/origin/JSS-1999-ORIGIN-EVIDENCE-R1.md` for the current 1999 evidence pass.

### HYPOTHESIS

- The earliest StoneAge concept may have been much simpler in macro-lore than later versions, even though resource/community/village-life themes are now directly attested in May 1999 design coverage.
- Much of the later macro-lore may have been progressively added to explain and extend an initially simpler world.
- Some mechanics remembered as "core StoneAge" by later players may not have existed for normal players in the earliest Japanese operation.

These remain research hypotheses unless a source record supports a narrower factual statement.

## Highest-priority research questions

1. **Locate and verify the earliest recoverable JSS retail client / retail CD image.**
   - Progress: a concrete surviving `STONEAGE 初回限定版` physical-package lead is recorded as `SRC-JP-1999-RETAIL-MERCARI-01`; period retail advertising is recorded as `SRC-JP-1999-AD-YAHOO-01`.
   - Newly established package clues: Windows 95/98, planned price 8,800 yen before tax, JSS domain `www.titan.co.jp`, Gamer's Dream domain `www.gamersdream.ne.jp`, and an advertised initial-edition special CD.
   - Still missing: provenance-preserving install/client disc image or dump, file tree, hashes, executable/version metadata, disc matrix identifiers, product/JAN code, manual/insert capture.
2. **Determine the identity and contents of the initial-edition `STONEAGE` special CD.**
   - Progress: the special-CD claim is now corroborated by a photographed contemporaneous advertisement rather than only a modern marketplace description.
   - OPEN: whether it is the install/client disc or a separate bonus disc; exact contents; filesystem/audio tracks; identifiers and hashes.
3. **Locate the September 1999 beta client or reliable binary/packaging evidence.**
   - Progress: beta period is bounded to 1999-09-01 through 1999-09-30 by contemporaneous evidence.
   - Still missing: installer filename, distribution method/media, hashes, internal version, beta-to-retail diff.
4. Recover JSS launch manual/box inserts and original world-setting text.
5. Determine the earliest documented appearance of:
   - the name "Nies / ニース / 尼斯";
   - the island-continent geography;
   - elemental/spirit lore;
   - pet riding for normal players;
   - major villages and early map topology.
6. Determine JSS-era internal client version numbering.
7. Locate the earliest Taiwan client/manual/site and compare it with JSS material.
8. Locate a clean Mainland early/1.82 client/data set for later diff archaeology.

## Completed in the latest work pass

- Read and obeyed `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` from the remote repository.
- Verified repository `chinaneedM/stoneage-rebuild`, default branch `main`, and live write access.
- Inspected current remote state and latest commit history before resuming work.
- Added `research/origin/JSS-1999-ORIGIN-EVIDENCE-R1.md` and extended it with March TGS and retail-ad evidence.
- Expanded `docs/SOURCE-REGISTRY.md` with structured records for:
  - 1999-03-19 PC Watch Tokyo Game Show '99 Spring coverage;
  - May 1999 `Play Online` design coverage;
  - September 1999 `Play Online` beta coverage;
  - 1999-09-17 PC Watch Tokyo Game Show '99 Autumn coverage;
  - a photographed period `STONEAGE` / `BLUE SPHERE` retail advertisement;
  - 2009 4Gamer launch-date retrospective;
  - a surviving first-edition physical-package marketplace lead.
- Tightened `docs/HISTORICAL-TIMELINE.md` with sourced 1999 milestones and explicit evidence limits.
- Promoted resource/community/cooperative-village themes from broad hypothesis to FACT only at the narrower level of documented May 1999 pre-launch design intent.
- Established two period web-archive targets from the retail advertisement: `www.titan.co.jp` and `www.gamersdream.ne.jp`.
- Initial indexed-web searches for preserved 1999 StoneAge pages on those two domains did not recover a usable archived product/download page yet.

## Immediate next actions

1. Continue the **physical-media recovery track** for the 1999 JSS initial edition: identify additional surviving package/disc listings, collector archives, product/JAN identifiers, disc-label photographs, and any lawful provenance-preserving image/dump lead.
2. Treat the **initial-edition special CD** as a separate recovery target until evidence proves whether it is or is not the client/install disc.
3. Continue archived-site recovery for `titan.co.jp` and `gamersdream.ne.jp`, prioritizing August-October 1999 product, download, support, beta, and patch pages.
4. Search for **September 1999 beta distribution traces**: installer filenames, magazine CD-ROMs, Gamer's Dream download pages, archived JSS/NTT pages, tester instructions, README files, and old personal download directories/indexes.
5. Capture exact page-level metadata for `Play Online` issues 012 and 015 and add stable archival hashes/notes where legally appropriate.
6. Once any original binary/media is recovered, immediately establish the reproducible client-archaeology pipeline: hashes, PE metadata, file tree, resource inventory, string extraction, asset IDs, and cross-version diff.

## Continuity status

- Repository: `chinaneedM/stoneage-rebuild`
- Default branch: `main`
- Visibility: public
- Authority: latest GitHub remote state is the single source of truth for project continuity.
- Canonical restart protocol: `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`

## Blockers

No repository or workflow blocker.

The substantive blocker is artifact availability: the project still lacks a verified 1999 JSS retail install/client disc image and September 1999 beta binary. Research can continue without them, but executable/file-level archaeology cannot begin until at least one provenance-sufficient binary artifact is recovered.
