# Stage A｜WORLD08：NPCEnemy 地图外观不等于战斗敌人图号（2026-11-04）

## 新发现与来源

从实时核验的主线 `fdff536d514d906c03eed578d0e44a800a3ba044` / tree `e59c8198f897227e19dd10e4614beef57c828114` 接续 WORLD07，历史 `docs/CURRENT-STATE.md` 2709173B / Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 保持**完整原样**。

本批不重复解压商业原包。直接复用已实际读取、按原 RAR CRC/SHA 资格化的 [CHAR09 NPCEnemy 原配置/敌人索引](../../research/recovered/STONEAGE-CHARACTER-NPC-MODULE-09-ORIGINAL-NPCENEMY-ROSTER-BRIDGE-R1.json)（固定 Git blob `3d827b98d00c3caa6e779f34a36d28bd70945b75`，原保存 RAR SHA256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`），并直接读取**另一份独立后期社区 C 源码** [`npc_npcenemy.c`](https://github.com/pimpcapital/longzoro-sa/blob/57b14e2bb373ba851c14db28a239273e4a8831bb/gmsv/src/npc/npc_npcenemy.c)（固定提交 `57b14e2bb373ba851c14db28a239273e4a8831bb`、Git blob `45c95d9df8b1e3e9d41443ca12f6ac8f4c105fc4`）。源码的确切 C 函数与行区间见[来源限定派生目录](../../research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-08-NPCENEMY-APPEARANCE-OUTCOME-R1.json)。

两个来源**没有认证为同一服务器实际构建**；静态代码为来源明确的后期行为候选，不是 JSS1999、台湾 1.0、2001 大陆 1.82 原版事实，也不是实际战斗录像或进服观察。

## 279 条原创建配置的逐来源复核

| 已有原创建引用（不是NPC种数） | 真实归并结果 |
| --- | ---: |
| `NPCEnemy` CREATE 引用 / 不同原 ARG 文件 | **279 / 260** |
| `gym>0` / 无 `gym` 的 CREATE 引用 | **200 / 79** |
| `gym` 正整数 | **1–100**，每级恰 2 条 CREATE 引用 |
| 原参数 `dieact=1` / `dieact=0` | **250 / 29** |
| 原参数 `entype=2` | **279** |
| `onebattle=1` / `0` / 未设置 | **10 / 13 / 256** |
| 原字面 `NEWNPCENEMY` 标记 | **2** |
| `dieact=1` 缺静态 warp 三数字的 CREATE | **0** |
| 已有敌人 SPR 数值图号候选 / 本轮新原像素 | **117 / 0** |

所有计数按原 279 个 CREATE 引用展开 260 原 ARG，并逐引用比对保存的 ARG SHA；未把复用同一 ARG 的不同创建记录合并掉。特别保留两条 `NEWNPCENEMY` 记录及其原始 warp 数字，防止以普通 `dieact` 默认分支强行覆盖该标记。

## 固定后期 C 实现直接可见的规则及正确界限

1. `NPC_NPCEnemyInit` 将 `enemyno` 字面数字经 `ENEMY_getEnemyArrayFromId` 解析；随后 `gym>0` 的 NPC 会用 `gymbody[]` **48 个符号外观之一**通过 `RAND` 覆盖 `CHAR_BASEBASEIMAGENUMBER` 和 `CHAR_BASEIMAGENUMBER`，并将 `CHAR_LV` 赋为 `gym` 数字。**因此，CHAR09 的 117 个敌人 SPR 候选图号不能被当作这 200 条 `gym` 创建的地图 NPC 外观。** 48 个符号不是已认证的 48 张地图原像素或 48 种怪物。
2. `NPC_NPCEnemy_BattleIn` 对 `gym>0` 调用 `BATTLE_CreateVsEnemy(...,2,...)`，其他 NPCEnemy 为 `(...,1,...)`；成功创建战斗才注册 `NPC_NPCEnemy_Dying` 为胜利回调。未证明实际创建成功、遇敌可达、战斗结束或原商业客户端动画。
3. 在**该后期源码**的胜利回调里，`dieact=0` 进入 NPC 图像隐藏与 `NPCEnemyLoop` 复现分支（当 `time=-1` 才以默认值 `120` 填入原工作字段，未认证其现实时间单位）；`dieact=1` 进入角色传送分支。实际传送坐标资格、队伍处理及 `_NEW_WARPMAN` / `NEWNPCENEMY` 条件改变分支，不可把 250 条静态配置说成 250 次已成功战斗和传送。
4. `onebattle=1` 在进入战斗前查找是否已有当前 NPC 的战斗创建项；这是静态条件门，不能认为 10 条原配置已经实测限制并行挑战。

**新增可用规格**是“地图 NPC 外观”和“战斗敌人模板”分开建证据字段，并为胜利后隐藏/复现或传送保留来源限定条件。这纠正了将敌人 SPR 索引误当地图外观的潜在错误；未产生新原美术、可玩的原世界、原色图或已执行事件。

## 止点与下一项

公开 Git 仅提交 C 源码 SHA、派生原数字统计、原 ARG 来源哈希索引引用、回归测试和本说明；不提交商业原 ARG、完整第三方 C 原文、原人物/宠物素材。专项 CI 可从固定提交取回**这一份** C 原文件核真实 Git blob 和关键条件；CI 通过不等于运行原商业服务端。

**WORLD08 SOURCE_BOUNDED_PARTIAL 止点。最高 NEXT WORLD09：** 转向已有真实原文件可复核的另一组物品/任务/玩法内容关系，不继续挖 NPCEnemy/GETPET 的同一条件树，不开历史网游账号/网络服务、不做新石器设计。仍为 Stage A **7 PARTIAL+2 OPEN**，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，总体完成百分比未知。
