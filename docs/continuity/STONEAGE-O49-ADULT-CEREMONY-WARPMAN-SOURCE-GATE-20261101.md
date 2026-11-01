# O49 — 成人仪式事件状态与两个世界入口的原文件关联（2026-11-01）

## 来源、实际结果

重新核验远端 main `7663196e8a226f3e7bacc57a9fcd1680b27c93db`、tree `07f9c9fe103dfe5a4ee6d76b97329069633ce8cc`、原完整 CURRENT blob `20050acf279a01555ab06a381dfcdc936bd381a6`（2,708,031B）、协议与 O48 主线十项成功 Actions。O49 是此前因发布检查中断后，对已保留本地证据的正式续交；不将当时未完成的远端操作写成成功。

私有父来源为已保管的后期混合社区2.5服务端 RAR，361,255,180B / SHA256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`。本轮重新逐字节校验完整 RAR；5份原文本与此前 R18 全源清单的整文件SHA一致、各成员实际CRC32与独立RAR头一致。原文保留私人库，公开仅派生数字、关联和哈希。

| 原成员（gmsv/data 相对路径） | 字节 | 原件SHA256 |
|---|---:|---|
| jobdaily.txt | 7929 | `5a1cb35c35b09ce78f83934a3ec5782918f2dc5cb5c9fa572618b2ecb36613bd` |
| npc/genout/genou.create | 7451 | `47e6dea94ea14a7900381b69e4c9ee0959456b325c3f580d58dd516f0bbd8586` |
| npc/genout/npcgen.template | 4950 | `0c5a58d5e31cafd3b58ccc1fa88fee7d1f95d12c0b87b04db9f06fea3b2a4df3` |
| npc/genout/wpm_200_358_671 | 337 | `ee3ad55ae6da677f37e357fda8a2f1189a2677c5815495e94d40a459f0b5c4ee` |
| npc/genout/wpm_200_359_671 | 337 | `ee3ad55ae6da677f37e357fda8a2f1189a2677c5815495e94d40a459f0b5c4ee` |

原任务日志第1条“成人仪式”的两个原状态字段分别是 `ENDEV=4` 与 `NOWEV=4`。独立的原 `genou.create` 两条创建块各唯一引用了一个实际原行为文件：

- 原地图200、坐标 (358,671)，创建块SHA256 `980a331e8b86e03cbacec875c4eab85351ddcdce4fe4849d365c900e382c8e14`。
- 原地图200、坐标 (359,671)，创建块SHA256 `78e100456f4226d39cbee5df5a2122dd83da67463b024c7d79b50f516c5b3a4f`。

两个创建块均属 `npcgen_warpman`、图号16202；唯一的模板块有 `functionset=WarpMan`。两份不同文件名的原行为文件内容完全相同：`WARP` 指向 floor21001 的 (4,3)，`FREE` 字面是 `LV>64&ENDEV=4`，`MONEY` 字面是 -1。保存版**任务数字4→两处NPC配置→同一目标坐标**成为可复核的静态来源链。原状态条目ID不可与事件数字4混同。

**不证实**：完成状态4的动态写入、条件语法的实际解释或等级判定、玩家原生行走/传送、关卡碰撞、原服部署、JSS1999或台湾1.0最初版本具有同一规则。无需由此创建新客户端、联机模拟、NPC UI 或武断填补任务状态机。

## 明确止点

原始脚本、任务原文、原图及服务端均未放入Git。派生回执：[`STONEAGE-O49-ADULT-CEREMONY-WARPMAN-SOURCE-GATE-R1.json`](../../research/recovered/STONEAGE-O49-ADULT-CEREMONY-WARPMAN-SOURCE-GATE-R1.json)。本轮沿用旧巨大 CURRENT 历史原样保全策略。Stage A 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，overall_percent=null。真实原版世界仍未运行。

**NEXT O50**：这一任务→守门点的静态来源链到此闭合。轮换到一项能补实际游戏规则/内容的宠物、移动或世界交互输入；有精确来源才扩展，避免继续制作该NPC的派生UI和重复索引。
