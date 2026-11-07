# QUEST07｜后期社区保管的原新手NPC备份：26条候选、9个真实原DAT、5间可视房间（2026-11-07）

以远端 `main=468b2b7087ec81ab066a9545002254bb74500073` / tree `96e6cf86066484200994e949c4c6a848a340ff34` 开始，先对旧QUEST01–06/CHAR01–09/地图范围查重。**源发现来自真正保管的361,255,180B RAR**（完整SHA256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`、总7952成员），而非把旧 Q05 的现行CREATE复制成新任务。首次单独逐原字节读取 `npc/sa60/newbie/newbie.create.bak`（6190B/SHA `fa83b8f14e355c757a2a27d2173d34941713c14b853886ea4aeff976d431d06d`）与现行 `newbie.create`（1548B/SHA `761dc3d1ed885fb76b22af446331e5a0db6cf3e59a27cf2ab136a62a88d81d0b`）；原RAR成员CRC分别为 `1a6f79b2` 和 `3f411954`。

## 可恢复的新手系统候选
旧备份34条NPC CREATE，现行8条，其中8条**字段字典逐项一致**（4个战斗指导与4个宠物常识指导位置）；其余**26条只存在于备份文本**，分布9个原楼层。其中10条 `sb_dou` 竞技/对战模板，另有治疗/药店/肉店、宠物技能/宠物店/宠物解说、入门/加工/料理/组队指导、传送/存档等候选原NPC功能。此为后期保存社区源内的**停用备份候选**：不证明任何官方版曾启用它们、不同数据载体同部署或真实原 NPC 任务运行。

| 原楼层 | 备份独有CREATE数 | 同保存版原DAT实际几何 | 已有来源合格的现代地图可视候选 |
|---:|---:|---|---|
| 815 | 4 | 80×70 | 否 |
| 816 | 1 | 180×180 | 否 |
| 8018 | 3 | 30×30 | 是 |
| 8019 | 2 | 30×30 | 是 |
| 8020 | 2 | 30×30 | 是 |
| 8021 | 11 | 60×50 | 否 |
| 8022 | 1 | 30×30 | 是 |
| 8023 | 1 | 30×30 | 是 |
| 8024 | 1 | 30×30 | 否 |

**9份原DAT均已实读原字节**（源RAR各成员CRC与整SHA），且从此前独立保管的MAP09内层955件原DAT ZIP再次逐件实读，九份完整SHA和CRC全部相同；不是9个新发现的游戏地图或新版图。每条备份原NPC坐标均在对应DAT矩阵内，真实逐原文件读取原点三张u16平面各一个数值，记录在 [QUEST07源派生报告](../../research/recovered/STONEAGE-QUEST07-INACTIVE-NEWBIE-BACKUP-26-CREATE-NINE-ORIGINAL-DAT-R1.json)。不解释这些格为可通行、障碍、事件或原NPC原生绘制位置。

**缺口关键：** 26条备份独有CREATE中24条引用同 `sa60/newbie/` 目录的外部参数脚本，真正存在的只有1条 `petmaster`；23条所引用的原始脚本在保存RAR的12件当前该目录成员中缺失。另2条直接带内联参数、没有文件引用。原始函数/文件缺失不可据此补造技能、交易、剧情或奖励，更不能将这份备份判为“当前启用”。

## 私人实物交付与来源限制
从旧MAP09私人691场景保存目录实际提取已有五间可视房间的来源候选缩略图，叠加备份NPC原CREATE坐标黄圈，得到9处位置标记，**没有伪造旧NPC精灵**。私人横向对照图 `/石器时代/StoneAge-QUEST07-five-backup-NPC-rooms-private-contact.jpg`，121442B/SHA `76b9e763da7fb72e457aa9ee0347046aa215f4f9730b643ded7480983de7962c`。两份原CREATE、9份原DAT、5张标记场景、私人对照图和派生源索引存 `/石器时代/StoneAge-QUEST07-newbie-backup-original-private.zip`，220401B/SHA `9b6da49d88c9e06f9128bc0b56de967301baaaf2c3a74400881298c4c84d0b77`，18成员全CRC通过；三项保管材料上传个人Library后再次实际取回整SHA全部一致。原DAT、原CP950全文、原像素均不入公开Git。

公开仅[来源锚点、26条分层数字和未证边界](../../research/recovered/STONEAGE-QUEST07-INACTIVE-NEWBIE-BACKUP-26-CREATE-NINE-ORIGINAL-DAT-R1.json)、[来源/计数/不合法晋升的负例](../../tests/test_stoneage_quest07_inactive_newbie_backup_original_source.py)和本加法收据。CI不能获得私人原RAR/原图，因而**不声称CI重解码了完整DAT/画面**；会核对原源报告及跨MAP09已存在的五图SHA/统计。原 `docs/CURRENT-STATE.md` 超大Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 原样保留，Stage A仍7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、overall_percent=null。

**NEXT：** 此备份26条已形成明确止点：只有发现该来源相匹配的23份缺失原脚本或官方版本/运行证据才可升级任务行为；真实视觉需补815/816/8021/8024的有资格原RD。不要为此扩大通用脚手架或补造任务；优先转已经实际保存的其他原版任务/玩法文件。
