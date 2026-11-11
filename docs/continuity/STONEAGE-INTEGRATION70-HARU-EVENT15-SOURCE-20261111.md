# INTEGRATION70｜恐龙博士哈鲁两阶段原NPC—宠物—八道具—原二维图像来源联接（2026-11-11）

## 实物与成果
从主线 `443cbaae4f287fc609523784231b568e84ec1660`／tree `12a71e7809bd20ef42a7eb70b1e1db78c37bab7f`、26/26 完成成功 Actions、完整历史 CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c`（2,709,173B 未改）重新核验；最新 INTEGRATION69 之后选**不同**内容。真正重读私人后期社区 mixed25 原 NPC ZIP（995,176B，全 2205 CRC）；原 `sainasu/event/event15.create`（341B）、两原脚本 `event15_1`（2,234B）和 `event15_2`（299B）均校完整 SHA/原字节。原两 NPC 配置在 floor **11006**、(11,11)/(11,7)、图号16024/16046，绑定各自原脚本；`changeevent` 源模板在旧 CHAR01 已联接，不等于客户端实际交互。

原脚本两组有序 **ACCEPT**：事件15字面 `NOWEV=15&PET>14-74`，`DelPet:PET>14-74*1`、`GetRandItem:1350,1351,1352,1354,700,1455,1102,1122`、`EndSetFlg:15`；事件16字面 `ENDEV=15&NOWEV=16&PET>29-191`，`DelPet:PET>29-191*1`、`GetPet:95`、`EndSetFlg:16`。辅助 NPC 另有一段 `NOWEV=15` MESSAGE。所有原条件连字符与大小写原样保留；不能从字面发明原版 PET 语法、随机权重、奖励 95 的实际物种、触发优先级或成功交换。

原 QUEST01 **已经**收录两脚本 8 TYPE 段；故本批新发现脚本0、原 TYPE0。真正新增的是两条 CREATE → 原两阶段脚本 → **八件同保存版原94栏物品行 → 另一载体台湾1.0已验真 RD 候选**的完整、可查来源关系。八件 ID 顺序见 [公开数值和原SHA](../../research/recovered/STONEAGE-INTEGRATION70-HARU-EVENT15-TWO-STAGE-NPC-EIGHT-ITEM-TW1-PIXEL-SOURCE-R1.json)；八行两套物品表完整源行 SHA 各自相同，原图别名 **不是**物理位图编号。源图号经已保存台湾1.0原 ADRN +76 别名候选分别为 **6477/6475/6483/6468/6235/6480/6340/6335**。本批逐私人保存 PNG 字节 SHA 与 RGBA 源散列重核 **8/8 一致**，**新从REAL解码原RD=0**，不宣传八幅新发现的图。MAP09 旧 floor 11006 DAT 有原 50×50 / SHA `fbf61337a1b397db8a2abcf6b2d804f926e384f240000d2301636ee4a17ce403`，但本批不重读地图、不能冒充 NPC 原版显示／动画／移动／对话。

## 跨来源与私人保管的边界
后期社区混合 2.5 NPC/物品服务端静态文本**不同于**认证零售 TW1.0 ADRN/REAL 来源；名称、图号与旧真实图像散列相连是**候选映射**，不是同一官方早期服务器部署、游戏实际选择器、Palet1原运行配色或已进入原世界。此次 ITEM01 ZIP 5,868,386B/838 CRC 实读，原物品94栏字段来自之前已验父 RAR 派生目录，**不冒称本轮重新解开361MB父RAR**。亦没有本轮重开372MB零售 P3H 父包；使用的是之前严格解码且本轮再次验 PNG/RGBA 的 8 张原二维候选。

本轮私人 12 成员源／图 ZIP **15,265B / SHA256 `d20d40ad6bdf3aab60fb96b222a059c018dbf2d042a6baa761465986f89922fd`** 已存个人 Library `/石器时代/StoneAge-INTEGRATION70-Haru-event15-original-source-private.zip`，再从独立路径下载，与原副本逐字节、整 SHA 及 **12/12 CRC** 一致。原商业脚本全文、源画像 PNG、原 RD、完整原物品文本**未**提交公开 Git；仅派生号码/散列/有限释义以及源守卫测试。无新增原生运行或玩家实际交付行为。

阶段 **Stage A 7 PARTIAL + 2 OPEN**、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、总体完成率 null。最高 NEXT 转其它尚未专题整理的**真正原字节**地图／人物／宠物／道具来源关系；不得重复本 event15 或 event13、做网络账号、新引擎、现代玩法优化。所有候选／主线 Actions 必须以真实运行回执另验，此文件不预支成功。
