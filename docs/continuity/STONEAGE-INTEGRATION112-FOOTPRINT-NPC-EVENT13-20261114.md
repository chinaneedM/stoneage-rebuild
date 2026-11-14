# INTEGRATION112｜盗贼洞窟三处原NPC与三家宝任务13足迹线索来源联接（2026-11-14）

## 精确启动和实际取证

本次重新从 GitHub 远端 `main=c64a8a4ca7e70aaf61d0aa02a75a5c436c016e47`／tree `fd50c067cc71785832df4ac1126d4efcdc3827db` 启动，精确 HEAD 的 26/26 Actions 已完成成功、0开放PR。按连续性协议读取 README、协议、原生 CURRENT Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`（2,709,173B）、设计、时间线、来源、路线、模块顺序与最新INTEGRATION111收据；保留全部旧记录和最近72条独立内容验收事实。

**目标：** 将现存后期社区 mixed25 原NPC资料中尚未专项研究的三处盗贼洞窟NPC，与同一历史保存来源的事件13「盗贼足迹」物品号建立可复核的内容关系；不是增加三张新官方早期图片、编造掉落机制、重新下载整RAR或开发任务引擎。

本轮从个人Library实际回读既存私人 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip`：**995,176B、SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`、2,205/2,205成员CRC通过**。真正读取 `npc/100/sb_nusu.create`、`sb_nusu.template`、`sb_nusu1.arg`、`sb_nusu2.arg`、`sb_nusu3.arg` 五原文件，每份完整SHA/CRC与旧 `STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json` 逐项相符；三个原CREATE块的起止字节和SHA亦实际对原二进制切片再算同一。另从同私人源实读 `npc/sainasu/event/event13_1` 与 `event13_2`，SHA/原命令与先前INTEGRATION33/69一致。旧原源文件已在全目录出现，**新增出土原文件0份**，新增的是此前未归档的三条原游戏内容数字来源联接。

## 三处配置与具体内容

| 原来源楼层 | 坐标 | 原 `graphicname` | 模板 | 原 `enemyno` | 参数字面 |
|---|---|---:|---|---|---|
| 10701 盗贼洞窟地下1楼 | (23,51) | 100405 | `sb_n1` | 513,516 | `entype:2; item:2431; time:300; dieact:0` |
| 10703 地下3楼 | (6,63) | 100436 | `sb_n2` | 514,518 | 同一 `item:2431` 等字面 |
| 10705 地下5楼 | (44,41) | 100230 | `sb_n3` | 515,519 | 同一 `item:2431` 等字面 |

创建函数引用三组 `sb_n1/2/3`，由同原文件中的独立模板段精确关联 `functionset=NPCEnemy`；各有对应一份 `100/sb_nusu[1-3].arg` 原参数文件。原文本包含足迹相关的对话与战斗请求，但商业原对白不公开；仅记录消息条数3/2/3及参数。**不能因 `item:2431` 就认定赢得战斗后必掉落该物品，或其数量、概率、触发规则、原服务器是否部署。** `enemyno` 和 `time` 亦只保留原字面，未执行业务逻辑。

早已核实的同一后期保存来源事件13脚本 `sainasu/event/event13_1` 的 REQUEST 段有 `LV>15`／`GetItem:2431*1`；MESSAGE 有 `NOWEV=13&ITEM!=2431`／`GetItem:2431`；ACCEPT 为 `NOWEV=13&ITEM=2428&ITEM=2429&ITEM=2430`、`DelItem:2428,2429,2430,2431`、`GetItem:2450`。既存原两份94列物品表均确认物品2431为「盜賊們的足跡」，原整行SHA `e98e9a026ed64d978fa7d3f3cf5b9d15338ec419e70a644f9bba4ea09a8450bf`。这是**同保存载体NPC参数—物品号—已有任务条件的三条静态数值边**，不是原生任务流程已实际通关或奖励/扣除成功。

旧保存地图派生目录已提供10701/10703/10705各80×80、38,408B原DAT的来源SHA、地图名；三坐标全部在界内。本轮新读DAT **0B**，未画原图、未执行原世界/寻路/碰撞。台湾1.0、JSS1999与大陆早期1.82的相同任务部署 **OPEN**。原NPC图号不能因整数相同就冒认官方早期人设或已观察的像素。

## 验收与后续

[永久派生数值／原文件SHA／原块字节窗](../../research/recovered/STONEAGE-INTEGRATION112-FOOTPRINT-NPC-EVENT13-SOURCE-R1.json)可对现存CHAR01、INTEGRATION33/69与旧DAT元数据重放；新的测试只验证可公开的数字与负证，**不代替本轮实际私有原文件全SHA/CRC回读**。公开Git不包含原脚本、对白、原RD、图片或私包。原 `CURRENT` 全体历史字节保持不变，README只尾部加法。

Stage A **7 PARTIAL＋2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，整体百分比 `null`。候选／PR／合并后主线 Actions 仅以真实精确HEAD执行结果验收，不预支成功。

**NEXT：** 轮换确有独立原材料、尚未完成可见二维或实质宠物／任务内容的其他家族；本三NPC与足迹参数已有来源限定止点，不继续扩NPCEnemy推测掉落引擎。
