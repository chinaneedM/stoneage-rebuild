# O61 — 四村“虎的训练师”原奖励事件链与未配对宠物ID（2026-11-01）

## 为什么这一项值得先做

本轮重新读取远端主线 `eda4d053c0b38fd8f29f7cb54884e9b9a4d0ad9e`、tree `55f3fbabdb0e3e27a995ee4757464418aa6dc844`、最近提交、11/11成功的主线 Actions、协议、README、设计/史料/来源/路线和完整历史 CURRENT Git blob `20050acf279a01555ab06a381dfcdc936bd381a6`（2,708,031原字节）。接 O60 新手导师、O59 两野生宠物捕捉字段后，不再扩抽象工具与宠物店UI，而是找到同保存版带**潜在奖励状态变化**的真实脚本。这与用户高度重视的“第一次骑上宠物”体验有关，但不把原剧本中的“宠物发放”冒充已经骑乘成功。

原保存社区混合2.5 RAR **361,255,180B / SHA256 d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5** 本轮整包重新读SHA一致。两件原文件实际核验并匹配此前 R18 原文件库存、独立 RAR 头CRC32：`npc/sa60/newbie/tiger.create` **714B** / SHA `048c55f59a10c5b9d6ea3a0bdc6ff0c79aacfd69abeb2c18477ca6586c5a887b` / CRC `aa2131b7`；`npc/sa60/newbie/m_tiger` **15,073B** / SHA `0a075f092b3b1e3f3b7c45e5ef18e4eb707392873cd67df1ebd500518f62674e` / CRC `22405aaa`。本轮不是发现新的官方 JSS1999/TW1 商业发布或运行服务端。源版权文件和完整中文对白只在私人原件中。

## 源4个NPC与同一个脚本

原 `tiger.create` 只有四个创建块，均是原名“虎的訓練師”、图形号16354、方向原值6，引用**同一** `npcgen_warpman|file:sa60/newbie/m_tiger`。

| 保存版原 floor | NPC出生坐标 |
|---|---|
| 1040 | (61,43) |
| 2030 | (58,16) |
| 3030 | (52,22) |
| 4030 | (16,32) |

这是创建文件中的**静态四个位置**，不是已执行原服NPC刷新/互动；未实读这四幅地图DAT或原NPC动画，因此不补造场景或原生骑乘图。

## 16条 TALKEVENT 中的12条奖励配置

`m_tiger` 原文含 `NEWWARPMAN`、16条 `TALKEVENT`。**1—12条**每条有 `AddPet`，同时设置 `Event_Now:166`；从原条件行确定这12条均带 `LV>29`、`ENDEV=4`、`NOWEV!=166`、`TRANS=0`，另外按原 `BBI` 数字选择。原 `BBI` 是条件变量字面，不在此臆译为官方人物皮肤或角色身份。

| 源注释颜色标签 | 原 TALKEVENT 段号 | 源 AddPet ID | BBI条件数 |
|---|---|---:|---:|
| 紅虎 | 1、2、3 | 2483 | 23+23+14 |
| 綠虎 | 4、5、6 | 2481 | 23+23+14 |
| 金虎 | 7、8、9 | 2484 | 23+23+14 |
| 黃虎 | 10、11、12 | 2482 | 23+23+14 |

原始四组数值交集核验：每组恰好**60个不重复BBI**，四组之间**没有相交**，12段合计240项恰好覆盖数值 **100000—100239**，没有缺失。这是来源条件覆盖事实，**不是**240名角色测试成功、发宠概率或240种独立宠物。

**13—16条**不是奖励分支：13原条件已是 `NOWEV=166`；14条件 `ENDEV!=4`，15条件 `TRANS!=0`，16条件 `BBI>100999`。原脚本没有在这些分支写 `AddPet`。事件166在源文中是赋值命令，**不等于已证玩家存档、领取限制、永久发放或骑乘解锁**；原 `FREE` 解析、优先级和 NPC 问答流程尚未执行。

## 经额外源检后，四个奖励 ID 已匹配到原实例与模板

原先只核 `enemybase.txt` / `enemybase2.txt` 的 `TEMPNO` 列，发现2481—2484不存在；**这个局部阴性仍属真实，但不足以断言奖励实例无法定位**。继续从新整SHA确认的原 `enemy.txt`（222,463B / SHA `cc7418d3b6726f1c458fef9e44a24696d05f076b67c62a56ed2293e26ae63bb6`，RAR CRC `0d60e57d`）查 `ENEMY_ID`，四个编号**全部精确唯一命中**，并通过同原文件 `ENEMY_TEMPNO` 连接到保存版 `enemybase.txt`。

| 原脚本源标签 | `AddPet` / `enemy.ENEMY_ID` | 同源实例原名 | `enemy.ENEMY_TEMPNO` | 原 `enemybase.IMGNUMBER` |
|---|---:|---|---:|---:|
| 綠虎 | 2481 | 給新手的貝魯卡 | 161 | 100327 |
| 黃虎 | 2482 | 給新手的貝魯伊卡 | 162 | 100328 |
| 紅虎 | 2483 | 給新手的格魯西斯 | 163 | 100329 |
| 金虎 | 2484 | 給新手的金格薩貝魯 | 164 | 100330 |

四条实际 `enemy.txt` 实例行各自原始等级均1—1、`ENEMY_PETFLG=1`，原基础模板行161—164的 `E_T_PETFLG=1`、`GET=5`，各行源字节SHA固定于派生报告。这是**同一保存载体的静态实物连接**，比此前只看 `TEMPNO` 的判断更准确。

另外实际读取的**独立后期整合源码** [BismarckDD/Stoneage 固定提交](https://github.com/BismarckDD/Stoneage/blob/2f736808ff4361f5429ee919b718c88fabb60346/server/gmsv/npc/npc_exchangeman.c) 的 `NPC_EventAddPet`，直接按 `ENEMY_ID` 查找，成功才调用 `ENEMY_createPetFromEnemyIndex`；该文件精确 Git blob `019a9578b122773df90442719ece50ad79fbe1b4`。**但它不是所保管 mixed25 RAR 运行二进制或同构建的直接证明**，也尚未证明 `NEWWARPMAN` 在实际执行时调用的就是这个处理函数、哪个编译分支生效或发宠结果成功持久化。原同版图像实际解码/骑乘动画与原版可玩世界仍未执行。

**候选阶段订正必须留存：**第一版O61分支 `585f38c78edfdb9cdc757ed6e578420b2a69666f` 准确记录四编号不在两份 `TEMPNO` 列，但未继续查看原 `enemy.txt` 的 `ENEMY_ID`。此后同一工作轮补齐真实ID层级，不将“未匹配”作为合并版本的最终结论。

[精确派生收据](../../research/recovered/STONEAGE-O61-FOUR-TIGER-TRAINERS-SOURCE-R1.json)包含原源长度/SHA/CRC、四创建块SHA、事件号、240条件覆盖统计、两张模板表的明确空查、未证项。私人原文/商业游戏素材不公开；完整历史 CURRENT 不截断、不修改。Stage A **7 PARTIAL+2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、总完成率 `null`，原版可玩世界仍未进入。

**NEXT O62：**四个 `AddPet` 已完成同载体原 `enemy.ENEMY_ID`→`ENEMY_TEMPNO`→原图号的静态连接；下一包仅在有新的实物时核 `NEWWARPMAN` 实际解释器、真实养成/拥有状态或跨载体真实原图，禁止虚构原服领取/骑乘执行。不扩训练模拟器。
