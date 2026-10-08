# BecomePig bounded PvP / WATCH-typed / enemy Exit composition R1

Status: ACCEPTED bounded scope, 2026-10-09 (Asia/Shanghai).
263268 native comparisons and 62 regression checks passed locally and in
Actions run37811014229/job113427551605 at exact inputf56089259f6d53d27ebde3687be02f0494075c2f.
Complete report bytes match; prior HP/death semantic digests preserved. Zero
runtime promotions. Prior publication block resolved by explicit user authorization.

The accepted three pinned descendant default profiles are reused without editing
original C. Complete `_BATTLE_Exit`, compliance, BadStatusAllClr, actual accepted
equipment/ride/status tables and helpers execute in transient native harnesses.
Inputs independently cross actor kind (player/pet/enemy), battle type
(PvE/PvP/WATCH), safe entry positions on both sides/no membership, HP/death,
pig/fox state, property pointer mask and controlled ownership. All 512 nine-flag
combinations are checked for each battle type and both representative sides.
Invalid actor/battle and unused battle paths remain separate witnesses.

Player slots are restricted to 0..4 because the original caller reads i+5;
nonplayer slots cover 0..9. One membership and at most one owned companion are
modeled. No invalid rider, duplicate membership, ticket expiration, oblivion,
multi-pet topology or actual memory release is admitted.

Independent oracle checks all previously tracked appearance/HP/MP/flags/work,
entry/escape/property/status fields and ordered helper traces, adding all nine
FS input/output flags. Separate invariants require an enemy destruction hook
only for a matched enemy, FS only for a matched PvP player, and no player cleanup
for nonplayers. Native execution uses O0/O2 GNU99 and nonrecovering UBSan.

Accepted bounded facts:

- PvP player clears DUEL before FS and XYD. gavin/iris compose nine flags;
  Bismarck composes four, so five additional flags are retained as state but
  omitted from its packet witness.
- WATCH-typed Exit runs player cleanup without PvP FS. This is not acceptance of
  watch creation/link/unlink/Finish caller lifecycle or full watch restoration.
- Matched enemy calls CHAR_endCharOneArray; matched pet does not. Neither
  performs player badstatus/compliance/HP normalization or network cleanup.
- Pig restoration is player-specific; fox cleanup precedes use/membership for
  valid actor/battle even for nonplayers. Error guards keep their original order.

Enemy deletion is a trace-only retained-slot hook: it does not mark storage
invalid or reproduce deallocation. Subsequent PartyUpdate/ticket checks cannot
establish safe original lifetime. Actual enemy destruction and post-destroy
read validity are OPEN, as are actual stats/work initialization, property
construct, ownership/follow, network/timing, WATCH link/Finish, original
executable/build/ABI/PRNG/JSS/Taiwan-v1 and typed631/635 runtime admission.

Tool: `tools/stoneage_becomepig_exit_modes_audit.py`.
Pressure unchanged: 2486 = 2465 closed capability + 18 OPEN + 3 historical UB.

Acceptance receipt: `research/recovered/STONEAGE-BECOMEPIG-EXIT-MODES-ACCEPTANCE-R1.json`.
