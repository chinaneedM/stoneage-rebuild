# INTEGRATION120｜礦石研究者17段原任务×双物品主表×两件真原RD图像（2026-11-15）

**性质：** Stage A 正版《石器时代》游戏内容来源限定整合，不是游戏执行或新玩法开发。此任务起点通过 GitHub 重新核验 main `09e544bce770345772246e99a2dc7bf414b6deee` / tree `754519b04e82ffa7655e085bedfc11d9eade7805`、0开放PR、精确主线Action 1/1 completed/success、完整原历史 CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c`（2,709,173字节）。历史文件不重写，新增覆盖记录。

## 一、本轮实物和真正新增边界

从私人 Library **真正重新读取、整包SHA/2,205 CRC全核**原 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip`（995,176B / SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`）；其同档 `genout/1200npc_m.create` **1,633B / SHA `c1acf84f3210e4d996c1f56e8f3a57e438a9ee66268c56fe530317adfa4cb87f`** 原第0块静态设定：
- **floor=2000**、borncorner `(87,95,87,95)`、graphicname `16209`、名 `礦石研究者`、`enemy=changeevent|file:genout/msg_1200_58_43`。目录名1200不是该NPC当前的原创建楼层号。
- 真原参数 `genout/msg_1200_58_43` **6,304B / SHA `a4d8273078cb60070432cb18339a4973ba531f4f8b0578af1fd01518eef28518`**：17段 TYPE，1 REQUEST（源 `GetItem=2785`）、1 MESSAGE、15 ACCEPT（15条 `GetStone` 和 `DelItem`）；其中14条数量字面 `ITEM=2786*14` 至 `*1`，末条 `ITEM!=2785&ITEM=2786`，金额原有序值 `50000,30000,20000,15000,10000,9000,8000,7000,6000,5000,4000,3000,2000,1000,1000`。数值是源字面，不代表已验掉落、条件匹配顺序、交易与实际支付。

复核旧 [WORLD22 原静态货币证据](../../research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-22-QUEST-CURRENCY-SOURCE-R1.json)中**15/15这些 GetStone 行早已公开**，旧 [QUEST01](../../research/recovered/STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json)也已编入脚本。**新原脚本0、新事件段0、新奖励行0**；本次严格增量是把这17段真实配置、两件同档来源物品、与此前已真读的两幅TW1图形成私人同页可见的来源分离链接，而不是重复声称首次发现内容。

## 二、两张真实来源图与两套原始物品表的逐字节关联

独立从之前已真实核验、此轮再次取回的 [ITEM01 私人图文原件](STONEAGE-ITEM-EQUIPMENT-SHOP-MODULE-01-TWO-SOURCE-TABLES-ORIGINAL-832-RD-20261103.md)（5,868,386B / SHA `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`，838/838 ZIP CRC成功）实读两件物品的两套 `itemset` 私人原行、源 RD 像素复算证明与原候选 PNG。原文字段由个人 Library 私存，不在 GitHub 公开全文。

| 社区源物品ID | 两张原表同一行SHA的事实 | 同档原图号 | 台湾1.0独立原REAL有实RD索引像素 | 历史归属 |
| --- | --- | ---: | --- | --- |
| 2785（指引地圖） | 同原94列SHA `1d9752539f7f8dcb`… | 24222 | **28×39**，原RD SHA `d519e1dbfcf21c`… | 只是跨版数字候选 |
| 2786（奇怪的石頭） | 同原94列SHA `9df6e6fdc886a67c`… | 14659 | **24×23**，原RD SHA `ea6e817c85523fc3`… | 只是跨版数字候选 |

图像源是台湾 Waei/JSS 1.0 已认证零售 P3H ZIP `3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24` 中此前 ITEM01 真读的RD；**本轮重新提取并严格核对两幅私人原像素候选PNG**，但原RD新解码数 **0**，不把复用称为两张全新出土原图。源图在本轮私人可见页是原始索引像素的现代候选显示，**TW1零售图与社区2.5原 NPC/物品表不属于已证明的同一官方运行部署**，不判历史原版实际选择器/配色/透明、角色实际触发或货币入账。

## 三、私人可见资料、可公开数字收据及明确止点

个人 Library `/石器时代/StoneAge-INTEGRATION120-ore-researcher-two-actual-RD-original-quest-private.zip` **8,490B / SHA256 `87cdc57f305e997884f8ef141bddf8702228cddf3f7e1363d6ca2b8bce62cc97`**，6成员（原CREATE字节、原任务字节、两份实际TW1 PNG、私源SHA/条件详情JSON、现代静态无外网HTML）。上传后已**再次独立下载读回整包SHA/6CRC同一**。不含可执行原游戏客户端；本轮HTML**未在浏览器运行测试**。私人源商业原文、商业位图、原RAW二进制不入公开Git。

公开仅本叙述、[派生数值和 SHA 收据](../../research/recovered/STONEAGE-INTEGRATION120-ORE-RESEARCHER-17-BRANCH-2-REAL-RD-R1.json)、独立可运行 unittest 和独立 Actions。GitHub CI只能复核公开历史各索引的守恒及本轮负证，无法在云端重新读私人原包和商业像素。

**NEXT** 转下一条真正有源的 NPC／任务／地图／宠物可见关联；不无限拆相同脚本，不提升跨版本相同数字为初代同服事实。Stage A **7 PARTIAL + 2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、`overall_percent=null`，旧CURRENT、旧失败和旧收据原字节不变。候选与正式主线 Actions 必须以精确 SHA 的实际运行结果分别后验。
