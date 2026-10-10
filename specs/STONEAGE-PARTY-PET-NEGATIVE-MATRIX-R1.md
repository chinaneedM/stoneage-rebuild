# Source-profile real-header party + selected-pet negative matrix R1

Status: **REMOTE ACCEPTED — bounded pinned-descendant native execution**
(2026-10-10).

Original pinned Gavin and Bismarck battle/character function bodies execute
with real original headers under GNU99 O0/O2 and nonrecovering UBSan. CI
[run 38032368154](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/38032368154),
job 114155807001 is **SUCCESS** (all ten steps, thirteen Python guards).
Tested commit `f6220d9bd4262c7b07dd48c5a646b6a430e9b56c`, tree
`4d043ac05a23dadae4433c0a87f5c067672b6b8d`.
Eight scenarios per profile and optimization, **32 successful original
CreateVsEnemy→ExitAll/DeleteBattle cycles** in all; battle arena cursor
`0,1,2,0,1,2,0,1`. Per-profile native stdout is byte-identical O0/O2.
The derived receipt pins both trace SHA256 values.

## Controlled original-function observations

| Input state | Gavin teammate | Bismarck teammate | Pet in battle | Default after original entry | Other observed outcome |
| --- | --- | --- | --- | --- | --- |
| Healthy member + selected owned pet | admitted | admitted | yes | 0 | owner0 roster retains pet2 |
| Teammate busy (C_WAIT) | skipped | skipped | yes | 0 | skipped member's GETEXP sentinel is not cleared |
| Teammate FINAL | skipped | admitted | yes | 0 | profile divergence retained |
| DEFAULTPET=-1, pet still owned | admitted | admitted | no | -1 | owned pet GETEXP cleared by owner ClearGetExp |
| Selected slot1 empty, slot0 still owned | admitted | admitted | no | -1 | selection normalized without deleting pet |
| Owned selected pet HP=0 | admitted | admitted | no | -1 | **before Exit HP0, after Exit HP1** in controlled setup |
| Owned selected pet ISDIE true, HP20 | admitted | admitted | no | -1 | **after Exit HP1, ISDIE false** in controlled setup |
| Live pet2 no longer in owned roster | admitted | admitted | no | -1 | allocated pet2 survives; its GETEXP sentinel remains 777 |

In every tested variant, original leader Exit, conditional teammate Exit,
ExitAll and DeleteBattle complete; real arena occupancy is released and
player world objects 0/1 remain registered. The test explicitly separates
battle occupancy, owned roster slot, selected default slot, actor
life status, experience clearing and post-Exit delta. The original pet
allocator and source-profile-specific party admission functions execute.
No proprietary original C files, headers or master records are committed.

## Interpretation restrictions

The constructed ISDIE and HP0 preconditions are deliberately synthetic.
Their observed post-Exit HP floor and flag normalization are **not**
grounds for claiming natural pet resurrection, definitive historical
Taiwan-v1 behavior or correct gameplay design. Nonempty Lua, network
transport, real time/watchers, equipment/items, original reclaimer and
full server bootstrap are still outside the controlled adapter domain.
No arbitrary pet party composition, true battle win/loss, profit, natural
death/selection or full turn execution is established.

Artifact 11663220824 SHA256 *metadata*
`d449acd63285dff7ba1557c9bffbc18b96e5958a93713b66d098e7334b3deb1e`.
Artifact ZIP bytes were not independently downloaded. No generalized runtime
pressure promotion: 2486 = 2465 closed capability + 18 OPEN + 3 historic UB,
zero new promotions. Source provenance remains descendant evidence rather
than an original 1999 JSS or Taiwan 1.0 runtime oracle.

**Next:** pin source-profile BATTLE_Init, surprise check and pre-command
sequence / task loop entry dependencies; then execute actual original
Init/TaskLoop with full state and adapter accounting before advancing to
Finish, victory and profit.
