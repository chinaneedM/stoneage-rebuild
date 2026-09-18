# stoneage-rebuild

A long-term research and development project to reconstruct the origins, evolution, and core experience of **StoneAge / 石器时代**, then rebuild it as a modern single-player 2D turn-based RPG.

## Project intent

This project is **not** a binary patch, private-server repack, or direct copy of an old client. The historical clients, manuals, screenshots, magazines, websites, videos, and later regional versions are treated as research evidence.

The development goal is to:

1. Recover the **earliest freely/publicly obtainable clean StoneAge client** (or the earliest trustworthy bridge client if the absolute original is unavailable).
2. Verify provenance and inventory the real client at file level.
3. Reverse engineer its executable/runtime structure, resource formats, maps, characters, pets, attributes, skills, items, UI, text/data tables and other deterministic systems.
4. Diff additional clean versions to reconstruct how the game evolved across JSS, Taiwan, Korea, Mainland China and later branches.
5. Reimplement the resulting specifications with a modern engine, modern rendering/input/save architecture, and independently created/recreated production assets.
6. Preserve the emotional milestones of the original experience while integrating later systems coherently rather than copying a single historical build blindly.

## Current phase

**Phase 0 — Earliest Clean Client Recovery & Reverse Engineering**

Primary targets:

- recover the earliest trustworthy client/installer/file tree available at zero acquisition cost;
- reject private-server repacks and modified clients through provenance and file-level checks;
- create hashes and full inventories;
- reverse engineer resource/container formats and deterministic game data;
- use additional clean versions as controlled diff anchors;
- keep historical research secondary unless it directly helps artifact recovery or technical interpretation.

See [`docs/CURRENT-STATE.md`](docs/CURRENT-STATE.md).

## Continuity

Every new ChatGPT conversation must start from the repository rather than chat memory.

Read [`docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`](docs/PROJECT-CONTINUITY-PROTOCOL-R1.md) first.

Recommended restart message:

> 继续《石器时代》项目。按仓库 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 启动，以 GitHub 远端最新状态为唯一事实源。先读取连续性协议、`docs/CURRENT-STATE.md` 和最新提交，然后从最高优先级未完成事项继续推进。

## Repository layout

- `docs/` — project vision, continuity, historical timeline, decisions, current state.
- `research/origin/` — JSS-era origin research.
- `research/clients/` — client/version archaeology and future diff reports.
- `research/sources/` — source notes and archival metadata.
- `game/` — future modern game implementation.
- `tools/` — archaeology/parsing/diff tooling.
- `tests/` — future deterministic tests.

## Copyright boundary

Do not commit copyrighted original game binaries, ripped art, music, sound effects, manuals, or other proprietary assets unless their legal status and repository policy explicitly allow it. Prefer storing metadata, hashes, filenames, observations, and research notes. The rebuilt game should use independently implemented code and newly created/recreated assets.
