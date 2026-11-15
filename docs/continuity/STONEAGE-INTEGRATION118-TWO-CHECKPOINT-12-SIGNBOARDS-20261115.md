# INTEGRATION118｜两组各十二份原检查点告示：同载体实字节、旧目录查重与地图证据边界（2026-11-15）

**性质：** Stage A 后期保存版原游戏内容考据，不是初代官方服的完成路径、答案钥匙、原客户端可操作玩法或单机新引擎。重新核验起点 GitHub `main=7ee059d98084d42f5934870a881e116d0e010a4b` / tree `66f9235e2ff9a192aa190da70b9f392873eea6f4`、精确 HEAD Actions 1/1 completed/success、0 开放 PR。协议与全文 `docs/CURRENT-STATE.md` 已从原生 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`（2,709,173B）复核；本轮不改旧历史，采用加法记录。

## 1. 拒绝一批完全重复的传送关系，改为真正可用的原文成组联系

先从已保存的社区混合 2.5 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` 实取四份 `genout/10402d.create` / `10701d.create` / `11101d.create` / `20801d.create`，模板与原成员字节、源位置、CRC 得 71 条静态 Warp 配置。然而将其源／目标楼层坐标六元组与已归档 `STONEAGE-25-MATERIALIZABLE-WORLD-WARP-GEOMETRY-R1.txt` 逐条核对，**71/71 已经存在**。因此本轮没有把 71 条关系记作新发现、没有重画重复的地牢路径。四文件仅私人留存作审查材料；不增加公开重复目录。

然后选择 `genout/oev2.create` 中源顺序的告示配置及其 24 份真实 `genout/signb_*` 文字。需特别区分：**CHAR07 早已公开收录这24份的源路径、CREATE 块 SHA、参数 SHA 和尺寸**；本轮新增的是以同一原始 CREATE 的物理顺序和真实 CP950 正文识别两组连续的检查点编号、正文重复关系，并对同源空间位置作已保存地图目录的边界复核。**新增原告示文件发现数为0**，不是重新声称找到了24份新文本，也不是将24条配置计为24项任务或24名NPC。

## 2. 实读与最小内容增量

父载体源身份：社区 mixed25 原 RAR 361,255,180B、SHA256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`，已有私人 NPC 子包 **995,176B**、SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，本轮整 ZIP SHA 与 2,205/2,205 CRC 再核。原 `npc/genout/oev2.create` **4,289B** / SHA256 `0b12db5f4fac9ad32094445cf3251244696b975f9841990f5948c8cc47f7aa10`。原 `npcgen.template` SHA256 `0c5a58d5e31cafd3b58ccc1fa88fee7d1f95d12c0b87b04db9f06fea3b2a4df3`，被引用模板 `npcgen_signboard` 的源函数确实是 `SignBoard`。独立花括号字节解析和逐行字段解析对齐全部 24 个原配置，原参数 `file:` 指向的24份原文件全能读取，**1,560B**，每份原 CP950 解码／回编码逐字节一致。

| 实际证据 | 本轮结果 | 不可推论 |
|---|---:|---|
| 原 CREATE 配置／文件引用 | 24／24有原文件 | 24个不同人物、已经触发的答题事件 |
| 原文检查点头编号 | 原配置位置0–11为1–12；12–23再次1–12 | 真实玩家经过顺序、两次不同历史活动 |
| 去编号后正文 SHA 去重 | 22 种；位置6↔13、11↔23 重合 | 正确答案、原算法或概率 |
| 有原始 `floorid` 数字 | 19个不同值 | 19张新地图、已达到的全部地牢 |
| 位置匹配旧 MAP04 原 DAT 目录且在尺寸内 | 16/24 | 本轮重新提取了16份DAT或游戏已显示告示 |
| 本次所用旧 MAP04 目录没有同 floor 的记录 | 8/24：100×5、1000／1100／1300各1 | 历史客户端缺这四幅地图 |

**来源界限：** 这批的 `SignBoard`、`floorid`、坐标、`graphicname` 和静态问句属于 **后期社区保存版的原文件**，不能提升为 JSS1999／台湾 Waei/JSS1.0／大陆原始1.82 官方同部署。文本包含检查点式标题，只说明**原文写了这些标识**；是否真有规则要求按编号通关、是否原版问答系统、原答案位于何处，以及选项解析、事件开闭/出生位置，均保持 OPEN。已另外研究的 `question.txt` 150条与 `racequiz.txt` 82行不能在没有同源加载器证据时强行合并。

## 3. 私人保管、公开验收与下一项

私有精确交付 `StoneAge-INTEGRATION118-24-checkpoints-private.zip`：**11,440B** / SHA256 `931cedccfbfcdd9d46a0ce467b6af3fb7e28d5f3af83eed644677bf4eb3aafb3`、**28/28成员CRC**。已保存到私人 Library `/石器时代/` 并独立再次取回，比对完整ZIP SHA、大小、逐成员 CRC 相同。包含原 CREATE、原模板、24份原文字节、无损私人目录以及一个现代静态离线原文查看页。静态 HTML 是现代资料查阅而非原版 NPC 对话窗口，**本次没有原商业客户端游戏运行或浏览器 UI 自动化测试**。未经授权的原商业文本、图片、压缩包未写入公开 Git。

公开仅保留[逐24源散列与负证 JSON](../../research/recovered/STONEAGE-INTEGRATION118-TWO-SETS-OF-12-ORIGINAL-CHECKPOINT-SIGNBOARDS-R1.json)、本报告、与既有 CHAR07／MAP04 原 Git blob 独立交叉核验的正反回归和 CI。公开 CI 不能复读私人版权原字节；源 ZIP 的实际字节验证与 CI 的派生重放是两层证据。已旧有的历史失败与全部 `CURRENT-STATE.md` 字节不覆盖。任何候选、PR、主线 Actions 成功只能后验确认。

**止点：** 本次24份原字节与两组检查点的静态来源语义已可审阅，仍不是原答题规则证据。后续不围绕 `oev2` 无限加程序/猜答案，不再重复71 Warp；下一步选有新原材料的任务－地图／原宠物出现－原行为关联或原始同版内容实物。Stage A仍 **7 PARTIAL + 2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、`overall_percent=null`。
