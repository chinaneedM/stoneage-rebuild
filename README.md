# stoneage-rebuild

A long-term research and development project to reconstruct the origins, evolution, and core experience of **StoneAge / 石器时代**, then rebuild it as a modern single-player 2D turn-based RPG.

## Project intent

This project is **not** a binary patch, private-server repack, or direct copy of an old client. The historical clients, manuals, screenshots, magazines, websites, videos, and later regional versions are treated as research evidence.

The development goal is to:

1. Trace the earliest JSS-era StoneAge concept and launch content.
2. Reconstruct the historical evolution from Japan to Taiwan, Mainland China, and later versions.
3. Separate historical facts from hypotheses and from our own design decisions.
4. Reimplement the game with a modern engine, modern rendering, modern input, modern save architecture, and newly created/recreated assets.
5. Preserve the emotional milestones of the original experience while allowing later systems and richer worldbuilding to be integrated coherently.

## Current phase

**Phase 0 — StoneAge Origin Archaeology**

Primary research targets:

- 1999 JSS concept-stage material.
- 1999-09 Beta client evidence.
- 1999-10-15 JSS launch client / retail CD-ROM.
- Early JSS world-setting and story text.
- Taiwan 2000 early client and localization changes.
- Mainland early/1.82 client and content differences.

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
