# Stage A｜WORLD21 原任务领宠条件、原始奖励实例与野外来源反例（2026-11-05）

**工作目标与止点：** 将已经作为数字目录登记的 `GetPet` 任务指令真正恢复为有原件和逐行 SHA 的 **条件→物品交付/赠予→宠物实例号→模板/图号** 静态分支，并与 WORLD20 的整批野外遇敌配置对照。初始远端 GitHub `main` HEAD `b7fe68faa7175a58f1a1693e3d4c4a0bca4f7282`，Git tree `e34fe62a0d07da94e52d1538f28f325a14ebcd71`；WORLD20 主线 11 项 Actions 全部成功。协议、README、模块工作序与完整历史 CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c` 已实取；CURRENT 保留不改。

## 1. 本轮实际真读的原件

- 用户私人 Library `StoneAge-CHAR01-mixed25-all-npc-original-private.zip`：**995,176 B，SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`**；完整打开 2,205 个原文件/1,930,332 B，每个 ZIP CRC 全部成功。`GetPet` 29 行及其整段原 `EVENT`、`TYPE`、`DelItem/GetItem/GetRandItem/EndSetFlg` 等字段本轮逐原字节重新解析，源文件 SHA、指令行 SHA、原行号再次与 [GAMEPLAY07](../../research/recovered/STONEAGE-GAMEPLAY07-GETPET-NPCENEMY-ORIGINAL-SKILL-SOURCE-R1.json) 先前独立原目录交叉核验。
- 同原保存档以前实取、本轮完整复核 SHA 的原 `gmsv/data/enemy.txt`（222,463 B / SHA `cc7418d3b6726f1c458fef9e44a24696d05f076b67c62a56ed2293e26ae63bb6`）与 `enemybase.txt`（147,750 B / SHA `1be7d5226798f7abaabe1f1e74aa1533fcd10e3eaf43f6497d63afa91df3e8b7`）。二者 2,087 / 988 条有效原完整记录，分别以敌人实例 ID（零基第3列）/模板 ID（第6列）建唯一主表。用 `enemy` 的模板外键第4列联接，不能用 `GetPet` 数字直接碰巧命中的 `enemybase` 同号行替代。
- 保存原 RAR 父档既有源资格：361,255,180 B / SHA `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`。**这轮没有再次整体 SHA 重读父 RAR**，不冒称本轮完成同包原服务器启动，也不把后期社区混合2.5保存包称为台湾1.0、JSS1999、大陆1.82官方同服。

## 2. 全量任务条件新恢复

27 份原脚本中 29 条 `GetPet` 指令；原数字出现 44 次，36 个不同敌人实例数字。29 个来源脚本事件块各有原 `EVENT` 条件：**25条 `TYPE:ACCEPT` / 4条 `TYPE:MESSAGE`**；22条同块 `DelItem`、7条 `GetItem`、4条 `GetRandItem`、24条 `EndSetFlg`。同时保留行/字段顺序及条件原文本，而**不把原文本条件或行序当实际脚本引擎执行结果**。原 `GetPet` 参数多值及重复位置保留。

- **原五种仪式选择：** `giiru/event/ev28_ed1` 至 `ev28_ed5` 的 `EVENT=ENDEV=28&NOWEV=31&ITEM=2517`，分别列 `GetPet` **54 / 57 / 55 / 56 / 481**，每条包含 `DelItem 2517` 与不同 `GetItem` 数字、`EndSetFlg=31`。这是五个原保存脚本分支，不等于原游戏验证过任选五只宠物。
- **另一原条件的奖励：** `giiru/event/event30_5` 的 `GetPet=355`、`DelItem=2547`、`EndSetFlg=54`；另存 `.old` 文件具有相同宠物数字但源文件字节不同，严格列作命名备份，**不重算为一个独立已运营任务**。
- **同包任务道具的新增交叉链：** `poru/team03` 原 `EVENT=NOWEV=64&NOWEV=57&PET=33-721&ITEM=2432`，在该分支原序列写 `GetItem=18559`、`GetPet=333`、`DelItem=2432`、`EndSetFlg=57`。物品 **2432** 与已验证 WORLD13/14 钓竿制作产物共用同一保存档 ID，属**新的跨任务原数字联接**；并不证明任务之间的原生执行前后关系、`PET=33-721` 含义或历史角色达到条件。
- **保留重复奖励选项：** `jaruga/event/oev_edb` 的原 `GetPet` 数字按序为 **`338,360,366,482,482,78`**，同块 `GetRandItem`、`DelItem=2564`，`TYPE:MESSAGE`。`482` 出现两次的原字节事实不可擅自去重或推算随机概率。
- **原猜谜脚本与备份的差异：** `quiz/equiz_04` 现存路径写 `GetPet=351`，另存 `quiz/equiz_04.BAK` 写 `352`，不能用备份覆盖原路径或混淆成一次奖励；另一 `giiru/event/sink/equiz_04` 保存路径亦写 `352`，但先前 CREATE 静态目录无直接引用。27份含两份 `.old/.BAK` 命名备份；之前 GAMEPLAY07 只在23份脚本中发现24条 CREATE 静态引用，本轮没有把未直接引用伪称可达或不可达。

## 3. 与 WORLD20 原野外遇敌的精确关系

36 个 `GetPet` 数值 **36/36** 实际在本保存包的完整 `enemy.txt` 有原行、经外键 36/36 到 `enemybase.txt` 有模板、图号与 `PETFLG` 原字段。与先前 WORLD05 两份候选表结论交叉核对，保留实例号 `54→模板91` 的反例（不可把数字54直接当模板54），保留 1479/1481/1483 对应模板718/719/720的双候选 PETFLG 1／0 冲突。

WORLD20 原 `setup.cf` 指定的 `encount.txt→group1.txt→enemy.txt` 闭合链中，719个有组引用的不同敌人实例号，与这36个来源 `GetPet` 实例号：**实际交集 0**。这只说明**在当前同包选用的该份遇敌区／组配置**中没有直接引用它们；完整 `enemy.txt` 主表本身仍有原行。它既**不能证明这些奖励宠物永远不在野外出现**，也不能证明活动任务原服实际发放、概率、可捕资格或原客户端表现。

## 4. 可查看的真正私人原任务文字与验收

已将原 27 份源文件的 CP950 候选解码全文与所有源行 SHA/分支条件、36条同包实例/模板原名，放入**用户私人离线三成员 ZIP**（包含 `index.html`、原源文字与数值说明）。除非确实可无误解码，否则保留替换字标记并记录字节源哈希；不猜历史字形。该网页不需账号和网络，可按任务文件、GetPet 实例、条件、原模板名检索，展开原繁体文字；不是原客户端、可玩剧情或原服任务完成。

本轮已在本地 Chromium 真正通过 `page.set_content(原 HTML 字节)` 执行：初始29张分支卡片、检索 355 得3条、按 `PET=` 可查询、展开原文有效，**0 JavaScript 错误 / 0 外部网络请求**。并未验证宿主 `file://` 直接打开或官方客户端。版权 NPC 原文、原资源图、原RAR及私人 HTML 不上传公开 Git。公开[WORLD21 逐源数值/行SHA完整收据](../../research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-21-GETPET-QUEST-BRANCHES-R1.json)及专项11项交叉/反例测试仅验证派生与已签收的公众数据；CI **不能代替原商业字节在CI重新解包，不能代替原生运行**。

**NEXT WORLD22：** 此批原任务→领宠静态链与现有野外链已达来源范围止点。根据有证原件继续下一组 NPC／任务／道具的实质新内容，**不重复**为这36个领宠数值扩建工具/模拟概率，也不搞账号、网游服务器、新引擎或体验优化。Stage A 保持 **7 PARTIAL + 2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，全项目整体百分比未知。
