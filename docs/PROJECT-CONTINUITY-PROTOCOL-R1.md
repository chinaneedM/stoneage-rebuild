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


## 11. Autonomous work-unit duration — 2026-10-15

The user reaffirmed: “我们还是按照当初定好的 单次任务量最少15分钟为节点 你自己规划 要不然效率太慢”. Each continuation should therefore comprise at least15 minutes of effective sustained project work, planned autonomously. A small passing check is not a stopping point: combine adjacent authorized research, implementation, adversarial verification, independent acceptance and continuity/publication work into a useful unit. Brief progress updates do not end that unit. Do not inflate elapsed time through artificial waiting or unrelated work. Record the completed outcome and remaining highest-priority task; do not require repeated “继续” for each small subtask. Existing publication authorization and evidence boundaries remain in force.


## 12. Durable provenance before short-lived CI artifact expiry — 2026-10-15

For each material source-derived historical milestone, inspect whether the verified artifact is only retained temporarily by GitHub Actions. Where lawful and copyright-safe, permanently commit the **derived metadata/report only** after independent source SHA, artifact ZIP digest, raw JSON hash, negative evidence-boundary guards, and exact semantic replay. Keep original proprietary client binaries, save payloads, music, sprites and other assets out of Git by default. Preserve the original run ID, HEAD, job, artifact ID, ZIP digest, raw-content digest and derived Git blob SHA in a versioned acceptance receipt. If a derived report cannot legally be retained, record its provenance, unavailable status and precise missing evidence; never silently claim full coverage.

Treat the archived derived report and source-custody receipt as complementary. An expired CI artifact cannot automatically invalidate previously verified research when a matching immutable derived Git blob and full chain of custody survive, but source runtime execution, actual IO success or original server-only values remain unproven until separately demonstrated. Every continuation must verify the current remote HEAD/tree, any incomplete branches/Actions, and the full current-state historical prefix before resuming. Prior failed Actions and corrections remain historically visible and must never be rewritten as successful attempts.


## 13. Outcome-driven restoration planning — 2026-10-16

The user reaffirmed that the assistant owns overall restoration planning and
necessary-work judgments. After CURRENT-STATE, read
`docs/RESTORATION-ROADMAP-R2.md` and its current portfolio index. A previous
local NEXT does not outrank a newer portfolio-level supersession.

Before starting a work package, name the game behavior/content being restored,
its material evidence gap, expected deliverable, version/source scope and stop
condition. Expand a low-level dependency only when it changes that deliverable.
After at most two consecutive work units without a new domain specification,
content attribution or material integration result, stop expanding the branch
and reassess the whole-system queue. A family remaining OPEN is not a mandate
to exhaust every helper before another family can advance.

Preserve bounded unknowns and define precise reopening triggers. Never replace
missing original server content with invented facts. Tests, R numbers, decoded
nodes and elapsed time are verification/work measures, not overall restoration
completion. Existing15-minute effective-work and publication rules continue;
do not use repetition, irrelevant checks or artificial waiting to fill time.

Current supersession: PET-STATE-01 is highest. TW1.0 client-local savedata R79 is
PAUSED_NON_BLOCKING pending a named material game-rule/state dependency.
Historical R1–R78 and R79 preflight are retained, not revoked or called complete.
