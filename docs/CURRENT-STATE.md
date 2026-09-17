# Current State

Last updated: 2026-09-18

## Current phase

**Phase 0 — StoneAge Origin Archaeology**

The independent GitHub repository has been created and the continuity scaffold is now being established on the remote `main` branch.

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
- Public material exists from 1999 before launch.
- A public beta existed in September 1999.
- Japanese commercial service launched in 1999.
- Taiwan and Mainland Chinese versions followed later and introduced localization/iteration layers.

Exact dates, version numbering, and feature ownership must remain tied to source records in `SOURCE-REGISTRY.md` and should be tightened as primary material is recovered.

### HYPOTHESIS

- The earliest StoneAge concept may have been much simpler in lore than later versions, centered on living in a Stone Age world with people, prehistoric creatures/pets, community, survival/resource activities, exploration, and lighthearted interaction.
- Much of the later macro-lore may have been progressively added to explain and extend an initially simpler world.
- Some mechanics remembered as "core StoneAge" by later players may not have existed for normal players in the earliest Japanese operation.

These are research hypotheses, not final historical conclusions.

## Highest-priority research questions

1. Locate and verify the earliest recoverable JSS client or retail CD image.
2. Locate the September 1999 beta client or reliable binary/packaging evidence.
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

## Immediate next actions

- Complete the initial remote documentation scaffold and verify the repository is readable/writable through the GitHub connection.
- Continue primary-source research on 1999 JSS materials.
- Expand the structured source ledger with URLs, provenance, exact claims, and confidence grades.
- When binaries become available, build a reproducible client-archaeology pipeline (hashes, PE metadata, file tree, resource inventory, string extraction, asset IDs, and cross-version diff).

## Continuity status

- Repository: `chinaneedM/stoneage-rebuild`
- Default branch: `main`
- Visibility: public
- Authority: latest GitHub remote state is the single source of truth for project continuity.
- Canonical restart protocol: `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`

## Blockers

No project-level blocker at present. The next workstream is historical-source recovery and verification.
