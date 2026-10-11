# Taiwan StoneAge 8.0: install/update separation and snapshot intake R1

**Date:** 2026-10-11. **Gate:** historical source-layer verification plus a read-only, engine-neutral installed-tree comparison. No original Taiwan 8.0 client files were acquired in this gate.

## Contemporary source findings

1. **Official release announcement reported in contemporaneous press:** 2005-06-08 GNN, https://gnn.gamer.com.tw/detail.php?sn=20167 , reports Taiwan Waei 8.0 launched with pet equipment and that updated physical client CDs were included in upgrade packages. This remains product feature/release reporting, NOT certification of a named online installer or underlying executable.
2. **2005-10-08 player-preserved operator-service response, page edited 2005-11-05:** https://forum.gamer.com.tw/G2.php?bsn=1571&sn=2856 . A player quotes a response attributed to 華義客服7號: incomplete game image/display data can be due to incomplete updates; it recommends removing installation, deleting residual game folder/registry material and reinstalling. This is a **user-preserved service quote**, not an independently retrieved original Waei support ticket. Crucially, it gives period evidence of installed-tree drift after updates and warns against treating a partly updated local directory as a full clean version.
3. **2005-11-07 player download guidance:** https://forum.gamer.com.tw/G2.php?bsn=1571&sn=2881 advises downloads uninterrupted and use of resumable download software. **No exact 2005 official filename/hash in the retrieved passage**, so this cannot be converted into a download candidate.
4. **2005-07-07 player equipment description:** https://www.gamez.com.tw/t/8-0/170704 . A contemporary player's repost calls out seven equipment families (head, teeth, claws, chest, back, wing, foot with subtypes), pet-body compatibility and elemental attribute effects, and lists several craft combinations. These are **period player reported mechanics**, not version-pinned client/server tables or directly reproduced recipe outcomes. Do not elevate recipes/stats to official executable truth.
5. **Periodical chronology reproduced later:** https://forum.gamer.com.tw/G2.php?bsn=1571&sn=4345 lists a 2005-06-06 VIP 8.0 disc mailing and 2005-09-08 promotional pet gear release. This is a *later-compiled chronology*, not original mail or installer bytes. It must not be misread as contradicting the contemporaneous 2005-06-08 announcement, or as proof that the entire pet gear feature first began in September.

## Historical identity gates

Separate **(A) distributor release/package**, **(B) unpatched installer / CD tree**, **(C) official patch/update payload**, **(D) fully applied clean installed client**, **(E) third-party/private-server patched tree**, **(F) paired server/runtime evidence**.

The dated Waei service quotation specifically supports **why B/C/D must not be silently merged**. An installer version label or clean publisher domain cannot authenticate a post-install tree. No binary bytes/hashes/provenance for an original Taiwan 2005 8.0 A–D pair have been independently verified in this round. The 2012 six-part 8.5 candidate remains a separate late-version hypothesis and Mainland `sa8_8016.rar` is a separate geographic carrier. Neither proves Taiwan 2005 8.0 original.

### Strict evidence table

| Question | Classification |
| --- | --- |
| Was 8.0 PET equipment reported as launched in 2005-06-08 contemporary press? | FACT_CONFINED_TO_RELEASE_REPORT |
| Are original Waei 2005 8.0 installer and a matching update payload bitwise verified? | OPEN |
| Is a contemporaneous incomplete-update symptom recorded? | PERIOD_SERVICE_QUOTE_WITH_USER_CUSTODY |
| Is the 2005-07 reposted PET recipe/body data a validated executable rule table? | NO |
| Does any current bridge prove native compiled PET packet127 or owner/unique-code lifecycle? | NO |
| Are original 1999 JSS or Taiwan 1.0 features newly proved by these sources? | NO |

## New executable intake tool

`tools/stoneage_client_snapshot_transition_audit.py` accepts two **local** extracted/installed **directory snapshots** through `--before DIR --after DIR`. It walks regular files without following symlinks, checks platform-case-colliding names, streams SHA256 for each file, emits deterministic canonical manifest hashes and sorted added/removed/modified relative file lists. It reports the unchanged file count and exact total bytes per snapshot, but **never executes, downloads, extracts, copies or modifies game files**.

Example once externally supplied authenticated snapshots exist:

```shell
python -m tools.stoneage_client_snapshot_transition_audit --before /path/to/clean-install --after /path/to/post-official-update
```

**Important limitations:** A local file difference only proves that two local snapshots differ. It does not prove that either snapshot is an original operator release, that the update chain is complete, or that PET opcode 127 was executed. The tool deliberately sets each of those status flags to `false`. Do not use a third-party patched installation as the claimed original `--after` snapshot. The tool has no actual original StoneAge bytes in CI; 13 tests use synthetic examples, including symlink, case collision, absent directory, manifest determinism and same-size content mutation.

## Highest next acceptance task

Find **freely digitally obtainable** original Taiwan 2005 8.0 official installer or patch bytes, or contemporaneous full filename + exact checksum + authenticated archive locator. Preserve original source URL and timestamps and the snapshot identity separately; inspect bitwise before making any production/runtime statement. Only with provenance-authenticated installed version/configuration and a compatible original server should optional PET equipment native packet 127, item owner identity, save/load and release behavior be tested.

No proprietary originals are committed. Historical pressure 2486 = 2465 bounded closed +18 OPEN +3 historical UB; zero early/JSS feature promotions; Stage A unchanged.
