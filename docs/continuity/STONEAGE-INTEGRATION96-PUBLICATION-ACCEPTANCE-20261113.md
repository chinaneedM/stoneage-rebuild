# INTEGRATION96｜7条原地下城守门人配置：正式主线验收（2026-11-13）

## GitHub 正式事实

- 内容提交：**[PR #375](https://github.com/chinaneedM/stoneage-rebuild/pull/375)**，候选 HEAD `9894ee59414e6341bea8edf6b5e1e7474c8377b5`，原始父 main `3d78f646b11d9e4109cfa0d4cb1be4091c04d495`。
- 合并前同候选 SHA 的 Actions **4/4 completed/success**：push [43438794412](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43438794412)、PR [43438878289](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43438878289)、PR [43438878362](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43438878362)、PR [43438878477](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43438878477)。专用 push job `131930684055` / PR job `131930968558` 真实日志均为 **Ran 8 tests / OK**。
- 预先独立核 main 没有前移、PR 无冲突且 exact head/base 未变后，squash 合并至 main **`a8b8d38483005a4bc08b0fb89fae34ed9227f2c0`**，内容 tree **`bfc1c536875dc4278c7e4b00ae53b47244c01c4e`** 与候选完全相同。
- 合并后以此精确 main SHA 查询到 **1/1 Actions completed/success**；[run 43439165136](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43439165136) / job `131931953680`，真实日志 **Ran 8 tests / OK**。这些是内容合并后的 run，不是假借候选 run。
- [永久机器化验收收据](../../research/recovered/STONEAGE-INTEGRATION96-PUBLICATION-ACCEPTANCE-R1.json) 保留完整五个 run ID、来源头 SHA、event/status/conclusion、三个专用 job 和 Git tree/blob 身份。**本验收记录自身提交的 Actions 尚未发生，不能在本文预先宣称成功。**

## 原始来源范围与独立核对

私人 Library 中的 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` 本轮实际下载核验 **995,176B／SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`、2,205/2,205 ZIP CRC**。其中原 `npc/genout/dungeon01.create` **30,712B／SHA256 `541ce646794e6c0c3e2414657567cbf6cb662d18b28049f4e3cd691071304169`**，257条原 CREATE 中 250 静态 warp、7 条 warpman；7个独立原处理文件的全SHA与先前 CHAR01 索引逐项吻合。原文本与完整对白留在私人原包，不进入公开Git。

新增的七组「创建源位置→真实处理文件→字面 FREE 条件→WARP 目标」由[原来源限定报告](STONEAGE-INTEGRATION96-DUNGEON01-SEVEN-ORIGINAL-GUARDIANS-20261113.md)、[公开派生 JSON](../../research/recovered/STONEAGE-INTEGRATION96-DUNGEON01-SEVEN-WARPMAN-ORIGINAL-SOURCE-R1.json)和 8 项公开回归守护。另用先前接受的 CHAR01 与 MAP04 完整公开 Git blob 独立按键逐行再核 **70个条件全部相符、0不符**。源/目标坐标 14个端点中 8个有旧 DAT 尺寸且在范围内，6个缺本次旧DAT资格；本轮没有实际重取这些DAT原字节。

## 证据止点与后续优先项

本次工作状态 **SOURCE_BOUNDED_ACCEPTED，不等于 GAMEPLAY_VERIFIED**。该混合后期社区保存包非已认证台湾1.0或大陆1.82官方同部署；`FREE` 表达式未在原服/原客户端执行，传送成功、对话、队伍限制、金币/物品实际消费与碰撞状态均未证明。不得根据现代归档、测试或相同数字补造原玩法。

完整旧 `docs/CURRENT-STATE.md` 保留 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`、**2,709,173B**，全部早前失败/修订保留；Stage A **7 PARTIAL+2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、整体完成率仍未知。

**最高 NEXT：** 再选一组真实原字节可复核、与既有仓库不重复的地下城／任务／NPC对白／道具条件关系，优先具体可见原游戏内容和来源身份；不得机械延长这组静态数字图，不做网服、网络账号或新引擎。只有同部署原始运行/服务端证据，才可能将字面门槛升格为实测历史玩法。
