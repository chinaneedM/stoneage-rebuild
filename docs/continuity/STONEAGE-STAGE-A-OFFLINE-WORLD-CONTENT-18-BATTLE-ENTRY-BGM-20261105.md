# Stage A｜WORLD18 战斗入口选曲与 EN 原字段（2026-11-05）

接续 WORLD17 主线 `e3ff80bec96b1d701af4fa9ab0e25ac1aef35285`、tree `22be0ecab7ddde6ba1f42f3208fa1e5d2895825f`。WORLD17 的 PR 13 项、主线 11 项 Actions 全通过。完整历史 CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c` 保留。

重新核对认证台湾 1.0 原 `sa_3.exe` 及保存版两个 `sa_2903` 原程序的对应窗口。两版都把原字面消息 `EN` 的第一个结果整数送入战斗状态处理，第二个参数另行处理。在该处理接受正值、进入所核起始分支并读取这组标记的条件下，结果 **1 选择槽 5／sabgm_b0.wav**，结果 **2 选择槽 6／sabgm_b1.wav**。台湾 1.0 对结果 2 同时写入两个参与判断的标记。混合保存版还比较第三个标记，结果 2 写入的这组三项为 1、1、0，仍选槽 6。结果 6 只会满足部分条件。网通变体的相关区段逐字节一致。

从同一混合保存档用 UnRAR 真正重取 `gmsv.exe`，1,897,867 字节，原 CRC 和整 SHA 匹配先前独立恢复记录。原符号 **BATTLE_CreateVsEnemy** 在已核成功分支把类型字段写为 1，再由 `lssproto_EN_send` 发该字段。普通遇敌与已核 NPCEnemy 入口均调用该创建函数。原符号 **BATTLE_CreateVsPlayer** 把相同字段写为 2，并在两个发送位置从该字段取值，原 `DU` 请求与 `ITEM_BattlePK` 都可进入此函数。由此同包可实证已核对怪路径对应 b0、玩家对战路径对应 b1。旧玩家资料把 b1 解释为魔王战或 PK。本次得到的是保存版玩家对战的编译原件证据，其他魔王或特殊战路径尚未穷尽。台湾 1.0 此处已证客户端分支，缺对应官方服务端实物来认证当年类型来源。未运行原客户端、服务端或播放场景。

[公开派生收据](../../research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-18-BATTLE-ENTRY-BGM-SOURCE-R1.json)保留两类客户端窗口、服务器符号及原调用位置，以及与 WORLD17 曲目路径的关系。公开测试只使用数值、文件名和摘要。

**NEXT WORLD19**：音频的地图和战斗入口已各形成一条证据链，轮换到另一个有实物的内容缺口。优先核常用物品的原使用字段和同包函数表，能连到具体玩法才推进。Stage A 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，整体百分比未知。
