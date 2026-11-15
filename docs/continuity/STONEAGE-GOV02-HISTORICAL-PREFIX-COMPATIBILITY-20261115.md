# GOV02 — Frozen Stage A historical protocol prefix compatibility repair (2026-11-15)

PR #437 merged a project-wide two-axis historical/module governance policy onto main 207d246ca4e2cda75da3a2822c897f3afd76cd90.
PR candidate SHA had 7/7 successful Actions, but post-merge Stage A validation run 43703327104 failed: historical prefix changed: docs/PROJECT-CONTINUITY-PROTOCOL-R1.md.
Cause: GOV01 inserted extra startup paths into §2 before the historical immutable prefix whose original bytes and SHA256 are pinned in tools/stoneage_stage_a_review_packet.py.

Forward-only correction: preserve the entire exact §1–21 source bytes from previous main e3519cfbc13ba82739fb473a9ca42cfed9ea066c; append the complete GOV01 §22 policy unchanged, then a §22 supplemental manifest of the precise seven mandatory startup file paths.
The new mandatory boot order remains valid in §22. Do not weaken any old Stage A historical prefix SHA, source pin, or negative test.
The old Stage A CI failure remains in history; new candidate and new main HEAD checks must pass independently.
Active module PET and provisional 1999–2000 chronology remain unchanged; copyrighted original media stays private. CURRENT blob c89e0e33537990aa2132b47c40fef49a985a935c is untouched, Stage A 7 PARTIAL + 2 OPEN, Stage B/wiki GATED, R79 paused, overall percent unknown.
