# Stage A | Offline game content first (2026-11-04)

**User-approved operational direction (DESIGN):** Restore the actual historical StoneAge game content for an eventual standalone, single-player game. During Stage A, faithfully investigate original maps, pets, NPCs, images, animation, items, tasks, sound, and mechanics. Do not reconstruct historical MMO registration, account login, gateways, network handshake, multiplayer synchronization, or live server infrastructure as a prerequisite.

Original client AND server files remain essential **data sources**. Read their original NPC, map, pet, quest and rules files directly. Starting an original commercial server is not a content-restoration requirement. Existing GMSV/SAAC startup, original socket configuration and native warp research remain preserved historical evidence, but the previously proposed GMSV-to-SAAC authenticated handshake, NPC creation through a networked startup, and original account login are **not the active highest priority**. Their native execution status remains OPEN; removing a work prerequisite does not establish a historical fact.

## What to do now

1. Reuse the already source-qualified local offline sprite/map/animation observers and verified client/server files. First recover visible and testable original game content, with exact carrier and historical version labels.
2. Create new offline observation output only for a specific content gap; do not build another generalized viewer, engine, login or server. Keep native historical movement, colors, collisions, dialogue triggers, combat and route behavior unverified until actual evidence.
3. Keep TW1 official-client evidence separate from the later preserved community mixed25 server source. Do not turn same-number cross-version candidates into official same-deployment claims.
4. This remains restoration, not the new game's development. Future local saves, engine, combat changes, UX improvements and newly designed gameplay are deferred. Original proprietary assets stay private; the public repository receives only derived, source-bound metadata.

## Reverified existing no-account offline scene, not a new game

Retrieved the existing private Library file StoneAge-O68-private-source-1003-walk-observer.zip, size 1,037,642 bytes. Complete SHA-256: 5bfdc54f330df78c2ef0ec3c22c01f03516814a2a0af57a487301a970441e59c. All four ZIP members passed CRC. The original embedded HTML is 713,710 bytes; SHA-256: 0d166e52dc4b4350e860a51308b7952759081537e7cc8c0901b18ef7b3e1fdcd, matching the permanently archived [O68 source receipt](../../research/recovered/STONEAGE-O68-PRIVATE-OFFLINE-PETSHOP-WALK-R1.json).

Replayed the exact local HTML in Chromium/Playwright on 2026-11-04. The embedded image loaded at 2040 by 1559 pixels. Original source-bound static 1003 pet-shop observer: eastern entrance (16,21) to (19,16) via eight actual keyboard actions; western entrance (15,21) to (19,16) via nine; the SVG route line also rendered. JavaScript errors 0; external HTTP/network requests 0. The testing host blocked direct file URL navigation with ERR_BLOCKED_BY_ADMINISTRATOR; tests therefore loaded the **same HTML bytes** via page.set_content. Do not report a successful direct file URL browser navigation in this host.

This is not the original client: mixed25 preserved map/collision, TW1 original images and a modern observation marker have distinct provenance and do not prove official same-server deployment, original palette, actual NPC conversation, or native movement. Original HTML, images and screenshot remain outside public Git.

## Exact state and next task

Fresh starting main: 366e9e6c1a25488e7548509d962c90368c3addb6, Git tree d2f913d28bda147e551d197562c440a0c2d7bbd8. Read and preserve the entire original 2,709,173-byte docs/CURRENT-STATE.md (Git blob c89e0e33537990aa2132b47c40fef49a985a935c). No change to its original bytes. Stage A remains 7 PARTIAL and 2 OPEN; Stage B and wiki GATED; R79 PAUSED_NON_BLOCKING; no defensible overall completion percentage.

**Highest NEXT: STAGE-A-OFFLINE-WORLD-CONTENT-01.** Reuse qualified prior original 1000 / 3021 / 3022 MAP/DAT, recovered original image blocks and existing offline viewers to produce one **additional actual source-qualified visible scene or NPC/pet content connection**. Prefer actual image and game-content progress, not a new socket service, account subsystem, redundant viewer or synthetic original-game claims. Stop at the qualified source boundary and move to the next original-content module when no new material is available.
