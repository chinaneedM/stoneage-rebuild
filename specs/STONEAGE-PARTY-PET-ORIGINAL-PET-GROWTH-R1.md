# Original pet EXP and growth R1 — bounded descendant witness

This gate composes the accepted actual second Loop/Finish/player upgrade/automatic
Exit/Delete flow with unchanged original pet LevelUpCheck, HandleExp, PetLevelUp,
CheckPetDoLimitlevel, PetAddVariableAi, earnFame and compliance. Pinned originals:
Gavin1f90cb6 and Bismarck999ffdf1, original headers, GNU99 O0/O2 nonrecovering UBSan.
Original game bodies/assets stay transient; only extraction/fixtures/oracles,
source hashes and derived observations are committed.

## Fixture and thresholds

All preceding admission, parser, wait, AI, guard, ordinary attack and lethal Loop
controls remain. After actual lethal FinishSet, the fixture explicitly prepares
owned pet2 raw WORKGETEXP1 and preexisting seeded CHAR_EXP near thresholds. This
is a controlled reward-state experiment; natural battle EXP allocation to the
pet is not established. Player0 still runs the preceding four actual upgrade
cases; player1 remains non-upgrading. Complete post-lethal party roster preparation
and later restoration occur as specified in PLAYER-LEVEL-R1, after all oracles.

Gavin payout1 and synthetic10000000 next-level thresholds remain versioned fixtures.
Bismarck pet payout1000000 uses its complete original cumulative table, increments
LV1011345723/LV1021442322. Both pet/player initial LV100 and the same independently
calculated EXP seeds yield levels1/1/2/0 and residual0/17/23/one-below. No dummy
GetExp/LevelUpCheck/growth getter or gameplay payout is substituted.

PetID1 excludes special401/718 and zero-reward1163. LIMITLEVEL0 allows growth;
no transmigration. Primary VITAL/STR/TOUGH/DEX all10000 before snapshots, HP remains
its prepared value. Packed allocation bytes are20/30/40/50. Family leader flag0,
original complete empty family fixture storage and account descriptor0 exclude
clan/account network calls; unexecuted dependencies remain abort-on-call traps.
Gavin owner fame7/momentum9 and pet fame11/momentum13 remain unchanged because
its constant synthetic next-level table yields zero growth feedpoint. This is
not an assertion of natural Gavin growth fame behavior.

| Mode | Pet levels | Rank | Rank roll | VITAL/STR/TOUGH/DEX growth | Variable AI before/after | Owner fame Bismarck | Pet fame Bismarck |
| --- | ---: | ---: | --- | --- | --- | ---: | ---: |
| 0 exact threshold | 1 | 0 | Minimum450 | 103/148/189/234 | 9800/10000 | 69 | 11 |
| 1 residual17 | 1 | 5 | Maximum600 | 138/198/252/312 | 1000/1500 | 136 | 78 |
| 2 two levels+23 | 2 | Invalid6→0 | Minimum450 twice | 206/296/378/468 | 9500/10000 | 280 | 150 |
| 3 one below | 0 | 0 | Untaken | 0/0/0/0 | 1000/1000 | 7 | 11 |

Bismarck HandleExp credits fame to the leveling actor only when remaining EXP
is positive (67 at101,72 at102). Thus pet fame11/78/150/11 is separate from owner
fame. PetLevelUp credits the owner with prior-level threshold/20000 only when the
current-minus-prior threshold is positive: level101 uses1256664/20000=62;
level102 uses1345723/20000=67. Both calls in a two-level settlement see the final
pet LV102, yielding67 twice. Owner final fame adds this to accepted player
HandleExp effects7/74/146/7. Preserve this profile-specific distinction.

## Random sequence and independent state oracle

The original Loop unconditionally discards one rand at entry. It is separately
counted and retains the inherited bounded RNG result. Each original PetLevelUp
then consumes ten attribute-bin draws and one rank-factor draw, exactly11 per
level. The controlled bin sequence0,1,2,3,0,1,2,3,0,1 produces3/3/2/2 extra points.
Original rand integers0/536870912/1073741824/1610612736 select these exact bins.
Rank-factor draw0 selects450; RAND_MAX2147483647 selects600 for rank5. Attribute
float results are truncated by original casts, independently checked with rational
arithmetic. This proves controlled original rand consumption, not natural RNG.

Sixteen native encounters (four per profile/optimization, cursor0,1,2,0) require
12 positive pet-growth encounters,4 one-below controls and16 aggregate pet levels.
Growth draws176 plus16 separate Loop draws; nonupgrade consumes0 growth draws.
Variable AI adds500 per level and caps10000; capped fixed AI100 remains.

| Mode | Fixed vital | Attack/fixed STR | Defense/fixed TOUGH | Quick/fixed DEX | Maximum HP |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 101 | 126 | 127 | 102 | 709 |
| 1 | 101 | 127 | 128 | 103 | 713 |
| 2 | 102 | 128 | 129 | 104 | 719 |
| 3 | 100 | 125 | 125 | 100 | 700 |

Every byte of all seven Char structs and the entire BATTLE struct is independently
compared after original second Loop/Finish. Only declared pet level/residual EXP,
payout WORKGETEXP, primary/derived growth, variable AI and versioned fame plus
accepted player upgrades and Exit effects are admitted. Pet ownership/default
selection/world objects are retained, paired pet modeNONE/index-1, playersFINAL,
enemy released, arena use0/modeNONE and total1→0. No actor/arena restoration or
second manual Exit/Delete substitutes for actual automatic release.

Original reward serialization must include a pet0 row. Positive owner packets:
Gavin -2|1|1,0|1|1,,,,|||; Bismarck -2|1|4c92,0|1|4c92,,,,|||.
Nonupgrade flags are0 in both rows; member packet remains its accepted separate
payout. Generic K0 status occurs once only for positive pet upgrade, zero for
positive-payout/nonupgrade (unlike the earlier zero-pet-reward path). Original
Exit K status and all accepted exact player/party status/broadcast oracles remain.
Descriptor7/output collectors are synthetic presentation, not real network.

Whole O0/O2 stdout must be byte-identical per profile.40 regression/mutation
checks include independent rank/bin boundaries, float truncation, combat-stat
arithmetic, variable-AI caps, versioned packet recipient and frozen source bodies.
Remote receipt records exact tested commit/tree/Actions and independently
verified ZIP/report bytes. Older narrower witnesses are preserved.

## Evidence boundary and next

Bounded positive pet/player settlement only in pinned late descendants. Special
pet IDs, ownership mismatch/limit penalties, natural pet reward allocation,
operator config/RNG, equipment/transmigration/level caps, positive reward items,
gold, watchers/callbacks/real network/Lua/server ABI and JSS1999/Taiwan-v1 executable
historical identity remain OPEN. No pressure or historical promotions:
2486=2465 bounded closed capability+18 OPEN+3 historical UB. No modern-engine phase
transition. Highest next: actual positive reward item ownership, exact inventory
slot/world-item state and empty/full inventory controls through second Loop.
