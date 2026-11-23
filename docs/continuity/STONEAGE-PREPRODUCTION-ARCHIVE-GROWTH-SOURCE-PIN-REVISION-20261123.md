# Preproduction archive historical source-pin review (2026-11-23)

The [2026-10-17 archive](../../research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json) locks an **immutable historical** source-pins map. Its original `research/mechanics/STONEAGE-PET-GROWTH-CORE-R1.md` Git blob is `87cdd063f05f6d6f334007cf3db7a31a8d1654a8`.

On 2026-11-22, PET-DETAIL29 [commit](https://github.com/chinaneedM/stoneage-rebuild/commit/170dcbc49272e6ecadc51c0db027f15dc02d2921) legitimately updated that same human-readable growth research file with a source-backed C float32 correction. Its **current exact file blob** is `568f461f31370a1b537d42791a1d333597672e77`. This is the **only** one of the archive's nine source files whose worktree SHA differs from the original archived pin on main before this repair.

The historical archive JSON is deliberately unchanged. The content validator continues to verify its nine original pins and each current file's Git blob: eight must match the original; the growth research file may match either the original historical blob or **exactly** the accepted later PET-DETAIL29 blob. An unrelated future edit must obtain an explicitly reviewed source revision, not bypass this check. The regression suite includes an adversarial negative test that removes the allowed revision and expects validation failure.

Observed original failure: main `1f2ef1593fff82db90386cb31958d4165c7fd435`, [Action 45119945415](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/45119945415), two validation exceptions for this single later growth-file change. The prior failed run remains in history; only a fresh passing action can demonstrate repair.

No pet-history source or commercial binary was modified; this is **source-archive continuity repair**, not a new official pet identity, source, statistics or module closure. `docs/CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c` preserved. PET remains ACTIVE, Stage A 7 PARTIAL+2 OPEN, B/wiki GATED, overall percent UNKNOWN.
