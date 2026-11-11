# INTEGRATION61｜两地原主厨、三道物品与台湾1.0原RD实图限定关联（2026-11-11）

从GitHub远端main `4090ac47f4ce807d0ab0ed3740a3859f204bb585` / tree `ba07222d9cfe5c8ec10c1b2913dde62a40e8df11` 重新读取连续性协议、完整历史CURRENT原Git blob、README、路线、设计/时间/来源文件及INTEGRATION60验收。依最新NEXT避开已闭合的四村装备店与五诊疗室，针对原料理菜单添加尚未专项固化的**原图像源关系**。

## 真正新增的来源关系

旧[O75原始资料目录](../../research/recovered/STONEAGE-O75-ORIGINAL-COOKING-CRAFTING-NPC-SOURCE-R1.json)已认证后期社区mixed25原CREATE/菜单和原itemset：floor 2009主厨(25,41)链接`menu01.conf`三种菜单文字均非严格同名匹配，原物品ID依然UNKNOWN；floor 3009主厨(25,43)链接`menu02.conf`三条已知同名料理IDs **12607 / 12780 / 12754**。本轮不将旧同名发现算作新的料理，只把其已有两原表一致的整行SHA、原料字段/回调联到已留存的**真实台湾1.0原RD像素**：

| 菜单同名物品ID | 原itemset图像别名 | TW1原ADRN物理位图序号 | 实际保存的原PNG尺寸 | 原RD大小 |
|---|---:|---:|---:|---:|
|12607|24484|6651|28×42|617B|
|12780|24443|6610|44×35|1259B|
|12754|24531|6698|32×34|778B|

**注意别名24484≠物理6651**，不能直接用物品原图号当原RD数组序号。原两表的原回调为`ITEM_useStatusChange`和`ITEM_useRecovery`，源材料raw值21/10/8不是已证实的数量、成功率或料理操作公式。

## 本轮重新核验私人原件

重新获得原保存的ITEM01研究ZIP **5,868,386B / SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`**；ZIP **838/838成员CRC通过**。实际从私人完整版目录核三物品各两套94列原行整SHA、菜单名称严格同名和原图别名；真正从ZIP读取三幅已解原PNG，逐完整SHA、图片尺寸及完整RGBA像素SHA均与既有原RD逐图收据相同。三幅原ADRN整记录、RD原块、原索引像素、PNG、RGBA SHA见[仅含派生数据的公开报告](../../research/recovered/STONEAGE-INTEGRATION61-TWO-CHEFS-THREE-DISHES-TW1-PIXEL-SOURCE-R1.json)。

本次**没有重新读取361MB社区RAR、主厨原菜单文本源文件或原RD二进制**，新增RD解码=0；原物品三图是旧已保存原像素的实物重读。原美术、NPC原文、物品商业全文只在私人研究保管包，公共Git只发布来源散列与可复核数字；专项CI只验证固定派生目录的数值/身份关系，**不能冒充私有原图像在CI中重绘或原游戏运行**。

## 未证及止点

mixed25社区保存的主厨/表与台湾1.0零售图形**不是已认证的同一官方部署**；没有原版客户端主厨画面、宠物料理动作、实际合成/消耗/成功率/图像选择和原服执行。2009三条字面近似料理依然不认定ID。原`docs/CURRENT-STATE.md` 2,709,173B / Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`历史全部原样保留。Stage A **7 PARTIAL+2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、overall_percent=null。

**最高NEXT：** 这条主厨原物品-原图关系已来源限定闭合；换其它确有同源输入的宠物技能/任务道具/服务与原图关系，先查重，缺实物时止点。绝不模拟料理公式、优化历史玩法或转网络/新游戏引擎。Actions以实际后验为准。
