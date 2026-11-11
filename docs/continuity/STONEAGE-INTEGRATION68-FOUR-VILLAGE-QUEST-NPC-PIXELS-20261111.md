# INTEGRATION68｜四村保护石任务四名NPC与台湾1.0真实二维原图候选（2026-11-11）

## 远端续接、实际增量与来源边界

按 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 从实时 GitHub `main=9af43766f0e8f54d106ae47ec486540697ddecc4`、tree `3987b6a90d0c5295a1dbba1a1e334bba22bad4ee` 启动，读取主分支、最新提交、26/26已实际成功的 Actions、README、协议、原生 `docs/CURRENT-STATE.md`、历史、设计、来源登记、路线和模块优先级及 INTEGRATION67 后验。旧完整 `docs/CURRENT-STATE.md` **2,709,173B / blob `c89e0e33537990aa2132b47c40fef49a985a935c`** 不改写。上一个精灵王 3 GetPet 真原像包到来源止点，本轮换到**QUEST31四村保护石任务中有创建/事件但没有专项角色真像的4处NPC**。

原任务配置属于**后期社区混合 mixed25 保存来源**；可读图片属于**独立认证的台湾 Waei/JSS 1.0 零售客户端**。本次只建立两个不同来源间的 `graphic_alias` →原ADRN尾部别名→真实原RD候选像素对照。跨版本同号不是同官方服务器/客户端部署，也不是原游戏选图例程已执行、NPC物种/角色定名或商业任务在台湾1.0存在的证明。

## 独立真实原字节核验

- QUEST31 **27,565B** 私人原任务包 SHA256 `796682fd3621a2bfecab03e7e199ca16936f95cad75f6a7842e6517f1e04dd42` 完整实读；内原 `sainasu/event/event09-12.create` **692B / SHA256 `1f55bbd59aa01c3aeaf1a70d5eb7b29f6c77f0dfd3549f082419c6e465a107e5`**，4 CREATE 的 ordinal、原四整数 borncorner、图号、原块SHA、事件脚本及地图资格逐条与既有[QUEST31精确公共原件关系](../../research/recovered/STONEAGE-QUEST31-FOUR-VILLAGE-EVENT09-12-SOURCE-R1.json)对齐；后者完整 Git blob `0a17857fc55fd5884963d1c00ffeb292ebc9f59b` 已独立回读。新增 NPC CREATE 或任务 TYPE **0**。
- TW1 原 P3H ZIP **372,626,292B / SHA256 `3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24`** 本次完整整SHA重读；原 `adrn_1.bin` 10,079,680B / SHA256 `47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8`，`real_1.bin` 315,842,228B / SHA256 `408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13`，原 `Palet_1.sap` 708B / SHA256 `32870080c47537a59beaf770b6df7bd79820fd52a23825058460900494f0b4b0`，各自实际完整SHA与旧已验源一致。
- **逐一扫描125,996条原80B ADRN记录的 +76 处 uint32 别名字段**，4项均唯一；直接按记录内实际物理bitmapno/REAL偏移/长度取 `RD` 全块，4/4 原文件flag1；两种独立RLE解码与逐索引像素SHA完全一致，4/4 实际原像素 PNG 已生成并目视检查，绝非仅有编号或推测的美术。

| mixed25原CREATE（floor／坐标前两数） | 源 `graphic_alias` | TW1唯一原ADRN物理bitmapno | 本轮真正解码原RD尺寸 |
|---|---:|---:|---|
| event09 /1200 (97,75) | **16205** | **5925** | 40×93 |
| event10 /1300 (65,65) | **16206** | **5926** | 36×94 |
| event11 /1400 (71,76) | **16203** | **5923** | 32×87 |
| event12 /11107 (24,6) | **16057** | **5903** | 36×66 |

每项有完整80B原ADRN、原RD整SHA、实际索引像素SHA、原源偏移与大小、现代 Palet1 颜色候选 PNG/RGBA SHA。四图原索引均只使用0或16—239已记录颜色索引。**反例：** 若把 `graphic_alias=16205/16206/16203/16057` 直接当原ADRN的**物理图块序号**，四处实际取得的记录 +76 别名都为0，且四张原索引像素SHA与本次资格图全不相同；不能混淆数字命名空间。所有详细数值及负证见[公开派生报告](../../research/recovered/STONEAGE-INTEGRATION68-FOUR-VILLAGE-QUEST-NPC-FOUR-TW1-ORIGINAL-PIXELS-R1.json)。原始RD/RGBA/PNG绝不进Git。

## 私人源像保管和可验证性分层

新私人 `StoneAge-INTEGRATION68-four-village-quest-four-NPC-TW1-original-pixels-private.zip`：**24,425B / SHA256 `e3b18f6b43d749bdda3fbbdf20e745e1c9c0da338c4d4cd446dbd4f4263ed0c0` / 11成员**，保存了4个真实原RD、4幅原像现代配色候选PNG、来源原CREATE、仅供私人目视的离线HTML及完整个人原件验收摘要。已真实上传用户个人 Library `/石器时代/`，随后**通过另一次文件回取**核得同一24,425B、完整SHA以及**11/11 ZIP成员CRC**一致。私人页面只是静态图像查看页；没有原游戏客户端启动、NPC原生动作/对话或网页登录。候选调色板、像素上下翻行、透明0均为现代研究显示设定，不认证原版实际运行配色/朝向/遮挡。

Git只包含数字、哈希和负证测试。新**10项专项公开测试**本地真实通过，分别锁定原 QUEST31 Git blob、四份源CREATE、四别名/物理号、四张原RD/像素/PNG身份、独立保管和异常反例。公开 GitHub Actions **无法重读私人 P3H 或游戏原图**，只可按数字来源重放；候选、PR、正式main Actions需实际运行后另记，**不预支通过**。

## 严格止点和继续优先级

四NPC的来源限定视觉接缝现已闭合：旧 QUEST31 的1200、1400、11107三floor已有独立原DAT来源资格记录，**不是**本轮重新绘制场景或实测NPC；1300未在先前955份有资格DAT中匹配，不能据此断言该图在游戏里不存在。本轮新增原原生NPC实际渲染、事件/旗标执行、商业服对话、跨版本真实同部署及原地图移动均为**0／OPEN**。不借某种角色服饰自行确认「村姑」「族长」真像身份；名称与外形仍只维持静态跨载体候选。

Stage A **7 PARTIAL + 2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、`overall_percent=null` 保持。**NEXT** 换另一项已保存而未专项补全的地图／宠物／道具／技能真原字节可见关系，先查重；本4图不再反复加索引或假动作。没有合格原件就记缺口、转模块，不构造账号、服务器、网络、引擎或所谓初代流畅化优化。
