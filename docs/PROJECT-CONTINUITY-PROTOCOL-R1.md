# Project Continuity Protocol R1

## 1. Purpose

This protocol exists so the StoneAge project can continue across new conversations without relying on transient chat context.

The **GitHub remote repository state is the single source of truth** for project progress, research status, design decisions, and next actions.

Chat memory may help orientation, but it must never override the repository.

## 2. Startup procedure for every new conversation

When the user sends the restart message, the assistant must:

1. Identify the `stoneage-rebuild` repository owned by the user.
2. Read the latest remote default branch state.
3. Read, in this order:
   - `README.md`
   - `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`
   - `docs/CURRENT-STATE.md`
   - `docs/DESIGN-DECISIONS.md`
   - `docs/HISTORICAL-TIMELINE.md`
   - `docs/SOURCE-REGISTRY.md`
4. Inspect recent commits to determine what changed most recently.
5. Resume from the highest-priority unfinished item in `docs/CURRENT-STATE.md` unless the user gives a new priority.
6. Do not ask the user to restate already-recorded project history.

## 3. Canonical restart message

> 继续《石器时代》项目。按仓库 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 启动，以 GitHub 远端最新状态为唯一事实源。先读取连续性协议、`docs/CURRENT-STATE.md` 和最新提交，然后从最高优先级未完成事项继续推进。

A shorter equivalent is acceptable if it explicitly names the protocol and says the latest GitHub remote state is authoritative.

## 4. Evidence taxonomy

Every important claim must be tagged conceptually as one of:

- **FACT** — supported by evidence currently considered reliable enough to state as fact.
- **HYPOTHESIS** — plausible interpretation or inference that still requires confirmation.
- **DESIGN** — a decision for our rebuilt game; not a historical claim.
- **OPEN** — unresolved research question.

Do not silently promote HYPOTHESIS to FACT.

## 5. Source hierarchy

Prefer evidence in this order:

1. Contemporaneous official material: original client, manual, official site, patch notes, packaging.
2. Contemporaneous press and magazines.
3. Preserved binaries, source trees, data files, videos, screenshots with provenance.
4. First-party developer/staff recollections.
5. Later official retrospectives.
6. Contemporary player guides and archives.
7. Later player recollections / community reposts.

Conflicts must be recorded rather than flattened.

## 6. Documentation discipline

At meaningful milestones:

- Update `docs/CURRENT-STATE.md`.
- Add new historical claims and uncertainty to `docs/HISTORICAL-TIMELINE.md`.
- Add sources to `docs/SOURCE-REGISTRY.md`.
- Record irreversible/high-impact design choices in `docs/DESIGN-DECISIONS.md`.
- Commit with a message describing the milestone.

Before ending a long work session or when context limits are approaching, update `docs/CURRENT-STATE.md` so the next conversation can resume without reconstruction.

## 7. Development discipline

Historical reconstruction and modern game implementation are separate layers.

- Research material informs specifications.
- Specifications inform the modern implementation.
- Original technical debt is not inherited merely for historical fidelity.
- Historical assets are not automatically production assets.
- Later-version content may be adopted only through explicit design decisions and coherent world integration.

## 8. Repository safety

Do not place copyrighted proprietary binaries/assets into the repository by default. Store hashes, metadata, filenames, screenshots only where legally appropriate, and research notes instead.

Do not rewrite or delete historical evidence records to make a later theory look cleaner; supersede them with dated corrections.

## 9. Large continuity-file retrieval

An empty file-interface response does not establish that a repository file is
empty. Resolve the fresh remote HEAD, tree and path metadata before interpreting
an empty response. If metadata reports a nonzero size, retrieve the exact Git
blob SHA from that tree with the Git blob interface. A clean checkout fetched
from the same exact remote commit and `git show <commit>:<path>` is also a valid
fallback. Do not fall back to an earlier chat's file content or progress.

Before appending or publishing, validate that the retrieved text preserves the
existing file; compare the resulting remote tree with the locally verified tree.
Never publish a suffix-only replacement after an empty interface response.

Observed on 2026-10-07 at main0fa1e733dfd021a45de63150249c14af9e6fc436:
`docs/CURRENT-STATE.md` has1050607 bytes, blob
`a9377a2e1b2c080167fc1ab7af088cc497fbcf33`. The file-read interface returned
empty content for this nonempty file; the exact Git blob interface returns the
complete current-state text. All earlier continuity records remain preserved.


## 10. Ongoing project publication authorization — 2026-10-09 (Asia/Shanghai)

The user explicitly authorized publishing this turn's commits to
`chinaneedM/stoneage-rebuild`, running Actions, and writing back to main after
acceptance, then granted ongoing authorization for all similar work:

> 我授权将本轮提交推送到 chinaneedM/stoneage-rebuild，执行 Actions，验收通过后写回主线。 今后所有类似内容 全部授权给你

Within this project's established scope, research/development changes, tests,
workflows, derived evidence and continuity records may therefore be submitted
for remote validation and integrated after the relevant gates pass without
asking the user to repeat this authorization. Preserve bounded evidence status
and all unresolved historical/runtime distinctions. Use non-destructive ref
updates; inspect a freshly changed main before integration. This records the
user's project-specific instruction and does not grant authority over unrelated
repositories or unrelated external publication.
