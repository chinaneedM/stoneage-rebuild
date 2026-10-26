# R32终验记录：原始地图110真实三格变化已安全合入

日期：2026-10-26。本文件只为追加的最终CI证据，不代替原2,680,510B的 `docs/CURRENT-STATE.md`；也不重写旧失败历史。

- 从本轮fresh main `05eb85bb59b2abcaba13b9614dedb37a27f3ca16` 起步，内容main `cffeea30c25f6b33d3c465fe7ce457edf8437a76` / tree `5c7472c159f15e3100d39bb4df84cb363c681a79` 经真实候选7项和同HEAD主线7项Actions全部SUCCESS；11内容改动路径无删除旧文件，CURRENT blob始终 `031c76a5a8e431f646853909bb2f2e11e6328cd2`。
- 原件来源：最初run40335438563 12月SFX 7z失败，修正run40335682973/job121616477087实际完整双源SHA、静态解包、取得并验证46×45地图110第三层 flat positions1/2/3 的16384→49152原值；旧失败保留。两旧平面完全相同，第三仅3处，三处均只增加二进制标志位0x8000，**位意义仍未验证**。源ZIP独立下载hash与API一致，完整派生JSON永久Git blob `a3fac4f5c08d1b0660f302f95901a7d7fb2bee18`。
- 引入独立验收工作流时因报告尚未入库发生run40336190397失败；报告补齐后candidate+main七项真实绿灯。其后第一份发布收据额外触发run40337484100/job121622844296：仅`*MAP110*`文件数量上限2过紧导致版权白名单检查失败，源/数据反例两步仍通过。修正为三份专有派生JSON精确白名单，并非放宽商用二进制限制。
- 最终正确主线 `086da782e1c7733b2d9cda88d99c4021eacb5a13` / tree `f2b0c6a0cb2817621d76e4e2476b3df0f778e911`，专用run[40337713382](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40337713382) / job121623660847实际 **completed/success**。源码/反例、历史文本blob/派生报告及三份JSON保管均绿。终验数据另见 `research/recovered/STONEAGE-R32-FINAL-CI-20261026.json`，该文件仅是后验记录，不重启取源。

下一主动最高 `ORIGINAL_SPR_RD_PALETTE_SAME_CARRIER_33`：明确R30八帧原索引图与同保存样本调色板RGB选择证据，有限止点；无同build色板就保留灰阶研究观察与未定原色。Stage A 7PARTIAL+2OPEN、B/wiki GATED、R79暂停、P3E环境阻塞、原服具名宠物/NPC/任务未认证、总体百分比null均不变。
