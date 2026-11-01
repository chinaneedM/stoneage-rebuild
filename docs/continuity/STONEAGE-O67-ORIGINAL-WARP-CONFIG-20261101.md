# O67 — 同保存档两套传送配置原字节及NPC Warp模板核验（2026-11-01）

远端起点：`main=c92fdaaca4cca80c8a0d740edb33c0fb96863a94`、tree `36a6d0248d51d754db5b67dd5b40ba962b5ad5e6`；上轮O66 PR#124合并，主线Actions **10/10 success**。按连续性协议，已重新读原完整 `CURRENT-STATE.md` blob `20050acf279a01555ab06a381dfcdc936bd381a6`，2,708,031B，继续保留全文不变。README最新NEXT O67为原Warp/行走事件触发字节及实际运行证据，而非新的导航工具。

## 本轮直接新增两份完整原始来源

实际从**私人保存的后代 mixed25 社区合集** `stoneage-preserved-mixed25-original.rar`（361,255,180B，完整SHA256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`）新提取两份完整文件，逐SHA与原RAR头CRC32对应：

- `gmsv/data/map/mapwarp.txt`：**110,674B**，SHA256 `b7b50f42efa8e5a3f740d49a8d0c01cbf994d1bb66151b16ff5b5e7c14e7595c`，CRC32 `6b4da534`，共 **2981** 行、每行五个冒号分隔字段。
- `gmsv/data/npc/genout/npcgen.template`：**4,950B**，SHA256 `0c5a58d5e31cafd3b58ccc1fa88fee7d1f95d12c0b87b04db9f06fea3b2a4df3`，CRC32 `56547578`。其字节SHA与此前存档R18中 `npc/genout/npcgen.template` 的已经收录值**相同**。

原 `mapwarp.txt` 第1392—1395行的4条记录是**唯一这4个具体方向**，每行原长37B含LF，内容为对应源图位三元组；两个前缀皆为 `NONE/NULL`、尾字段 `NULL`，不为它们发明语义：

| 原行 | 静态来源位置 | 静态目的位置 |
|---:|---|---|
| 1392 | floor1000(69,72) | floor1003(16,21) |
| 1393 | floor1003(16,21) | floor1000(69,72) |
| 1394 | floor1000(68,72) | floor1003(15,21) |
| 1395 | floor1003(15,21) | floor1000(68,72) |

这4条**同档第二份** `mapwarp.txt` 的静态对应关系，与O58/O66已完整校验的 `warp_y.create` 里4个 `npcgen_warp` 配置，**坐标和方向完全一致**。源 `npcgen.template` 的唯一确切 `templatename=npcgen_warp`（源行211）在同一模板块里指定 `functionset=Warp`（源行215）；须严格区别另一个 `npcgen_warpman` 的 `WarpMan` 功能，不能混同点击NPC与踩格处理器。四原行/模板SHA见 [O67机器回执](../../research/recovered/STONEAGE-O67-ORIGINAL-WARP-CONFIG-SOURCE-R1.json)。

**这不是新增四条地图道路**，而是对已经O58/O66知道的两对门，找到了**额外一份独立配置文件和明确Warp绑定名称**，缩小后续执行证据需要搜索的范围。不能因同RAR放在一起便声称两个文件都被实际运行服务加载、同商业版本部署，或者知道某个玩家出生在warp格时是否立即被传走。

## 原执行文件的明确失败记录

本轮额外试图从**同一RAR**提取 `gmsv/gmsv.exe`（原目录表1897867B、CRC32 `6e31b63a`）；libarchive读取到 **1835008B** 后报告 `File CRC error`，**未得到完整可核SHA的EXE**。截至本轮不得对其宣称“运行了原服务器、追踪到原生Warp回调或知道踩格触发时机”。失败的部分字节不作为完成原件、没有公开。该解压失败不自动证明整个RAR损坏：上列2份完整文件和O66六份源文件均从实际来源提取、逐SHA和CRC通过。

## 准确止点与下一材料

O66的1003静态地图**71/900格可走**、东门8步、西门9步且西门可避另一个传送格继续成立；但该行走模型由保存档mapset与后代规则推出，**本轮并未实际进入游戏世界，也没有认证Warp触发的具体执行顺序**。未通过证据界线时不生成看似原版的自动传送或登陆模拟器，不扩通用helper。

Stage A 7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、overall百分比null继续。**NEXT O68**：如获可完整核SHA的同代可执行文件/完整源码，直接定位 `Warp` 的进入/出生触发和位置切换；否则回22域选择新的有实物的任务、捕捉、骑宠或地图交互材料，停止同一家店的无源追查。
