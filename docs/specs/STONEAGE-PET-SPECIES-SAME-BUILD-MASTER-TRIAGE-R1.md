# PET-SPECIES-SAME-BUILD-PRIMARY-MASTER-08 — 宠物名称/模板/图形字段原证据门（2026-10-25）

## 目标和本次结果

**目标游戏内容**：在某个已鉴真的、明确地区和构建的原始宠物主表里，把宠物的原名、服务器实体/模板 ID、图形选择 ID 与同一构建的实际客户端图像/动画资源建立可复验的关系；最终才能恢复相应宠物名称、造型和相关成长/获取规则。本轮检索与源码静态审阅的结果是 **OPEN_NO_AUTHENTICATED_SAME_BUILD_PRIMARY_MASTER**，**不是** TW1.0 或 JSS1999 宠物恢复成功。

从 2026-10-25 新读远端 main HEAD `9b2c58ef6d64e2e28dbbbec72900ad07c9e4c342` / tree `71c61243cff90543dd8d7dd43b7444dd9e8f11c1` 启动。原状态文件当前最高NEXT为本任务，CUSTODY-07因私人持久存储不足暂停；本轮未重新下载 TW8.5 1.145GB、mixed2.5 361MB 或 ADRN129 修复档，也未取得可鉴真的早期原服务器完整构建。

## 新的实质性来源：社区 GMSV 代码，严格限于它自己的语义

- 公共仓库 `librae8226/gmsv` 的 master 精确提交 `49928c291c6789013cba56d7c07d389f87cdfb0c`（GitHub commit 标示 2012-05-04），树 `b774ac0b874d8a5465b391524e02335693fb7feb`，没有可直接获取的 `data/enemybase1.txt` 与 `data/enemy1.txt`，仅见源码与 `setup.cf` 指向两文件。提交时间只证明该社区代码快照的 Git 时间，绝不追认任何官方构建/发行年代。
- `setup.cf` Git blob `b79678ddb86daf923f8068509bb6a588638ac5c2` 第 77/79 行将 `enemyfile`、`enemybasefile` 分别指向 `data/enemy1.txt`、`data/enemybase1.txt`。
- `include/enemy.h` Git blob `a0253f6f2d5e36e4a40a37e8399a3a127382932e` 第 7–60 行定义模板整数序及 `E_T_TEMPNO`、`E_T_IMGNUMBER`，这是**该代码的结构定义**。
- `char/enemy.c` Git blob `9e09d3d9b5696ebcd130755607bacef4c8854e50` 第 517–528 行以 `ENEMY_TEMPNO` 对 `E_T_TEMPNO` 做首条模板匹配，存至 `enemytemparray`；第 365–370 行的访问函数返回该关联；第 1138–1140 行的 `ENEMY_createEnemy` 把 `E_T_IMGNUMBER` 写入 `CHAR_BASEBASEIMAGENUMBER` 与 `CHAR_BASEIMAGENUMBER`；第 1580–1608 行的 `ENEMY_createPetFromEnemyIndex` 也沿该已关联模板读取并写入图形基字段。该代码说明可执行的**关联意图**，但本轮没有编译/执行该社区代码，也无原图像像素运行确认。
- 因未取得此提交对应的 master 文本、客户端 build、发布者授权来源证明及与 TW1.0 原 `ADRN/SPR` 的同构建关系，**不得**由 `IMGNUMBER` 数字直接宣称为 TW1.0 bitmap ID / SPR 组，或把它等同玩家工具 `stonepic` 的编号。

来源 URI：
https://github.com/librae8226/gmsv/tree/49928c291c6789013cba56d7c07d389f87cdfb0c
https://github.com/librae8226/gmsv/blob/49928c291c6789013cba56d7c07d389f87cdfb0c/char/enemy.c
https://github.com/librae8226/gmsv/blob/49928c291c6789013cba56d7c07d389f87cdfb0c/include/enemy.h
https://github.com/librae8226/gmsv/blob/49928c291c6789013cba56d7c07d389f87cdfb0c/setup.cf

## 具体的后代玩家/教程候选与反向隔离

现可读取的社区教程 `https://www.shiqisifu.cc/Article/5/News_104.html` 给出一个 **毕可斯** 示范：其自述 `enemy1` 示例编号 2349 引向模板号 90，`enemybase1` 示例使用该模板并含 IMGNUMBER 101621。它只能作为教程作者给出的演示数据，未见该两行所在同一真实游戏发行包、原服务端原字节、源码版本/校验或对应像素，不得与上面的 2012 代码强合并为同构建完整证据。教程将 TEMPNO 和宠物编号区分，提醒不同 ID 命名空间不可机械等同。

当前材料不能证明 (1) 101621 是 TW1.0 某只宠物，(2) 90 是 TW1.0 物种号，(3) 2349 对应某原服出现点或等级成长，(4) 2012 社区代码与本文示例、已归档 Gavin/Bismarck 原始样本存在同一编译和数据树。此处只产一条**明确负边界的示范链**，不增加任何初代具名宠物物种。

社区教程 `https://www.shiqi.me/pt_167.htm` 独立显示后代 `enemybase1` 的第 32 列为 `IMGNUMBER`；2026 年发布的 `https://www.246sa.com/?p=1176` 商业工具说明也声称通过 `enemy1→enemybase1` 查名/预览，但二者是晚近辅助参考，不算同代官方主表，也不另算两份独立实物下载。

## 与仓库既有原始证据去重

- `specs/STONEAGE-ENEMY-LOADER-R1.md` **已**证 Gavin 自己的 `setup.cf` 和同树完整 `enemy1/enemybase1` 原字节经外部原执行器按固定 SHA 驱动：1,816 模板、2,935 成功读取敌人行、49,024 有界普通出生实例；Bismarck 在同输入上的执行仅是跨 profile 比对，不能叫 Bismarck 历史主表。以上是仓库先前成果，**不是本轮新取得的数据**。其中原文件仍非跨会话原字节永久保管，也非 JSS1999/TW1.0 官方原服。
- `docs/STONEAGE-PET-IDENTITY-SAME-BUILD-SOURCE-TRIAGE-R1.md` 已见证 TW1.0 原 ADRN 0—125995 与 SPR 位图引用的实物索引，而原图号存在不等于宠物物种映射；2001 迁移玩家 `stonepic` 与捕捉目录并不提升身份归属。
- `specs/STONEAGE-PARTY-PET-ORIGINAL-PET-GROWTH-R1.md` 的增长验收使用有界后代及合成阈值，不能倒灌 TW1.0 成长参数。本包没有新增原宠物成长数值，也没有新的可用视觉资产或副本。

## 可自动判定的升格门槛与有限止点

一次有效升级为官方同构建物种/图像事实，至少要同时验出：`source_package_sha256`、`region`、`client/server_build_evidence`、逐原始位置 `species_name_raw`、`enemy_id`、`template_id`、`graphics_selection_id`、`client_resource_occurrence`、`original_pixel_or_animation_sha256`，并说明同一版本/资源命名空间证据链。原始重复行/别名应全部保存，不进行 last-wins 覆盖；未验证字段必须为 null。像素 SHA、原服执行和玩家称谓缺一时只可报 **候选关联**，不可报已认证初代宠物。

本包实际停止：上列 Git 源码链已新核，教程只为非官方示例，公开仓库未含两份被配置引用的数据表；此前 Gavin 及 TW1 的独立身份缺口不变。**零个新官方同构建具名宠物映射**。无可取同版原主表前不连续扩大 GMSV 下层 helper；按连续性协议13返回全域，下一主动材料包转向 **`NPC-QUEST-SAME-BUILD-PRIMARY-EVENT-09`**，优先原早期运营手册/原始 NPC 事件与发行基线任务归属，选一条具名原服对象作有界检验。不把节庆活动纳入本体任务：继续 DD-028 的本体／永久版本追加／运营活动／起源待考四档。

**保持**：CUSTODY-07=PAUSED_EXTERNAL_PRIVATE_STORAGE_DEPENDENCY；Stage A=7 PARTIAL+2 OPEN；Stage B/wiki=GATED；R79=PAUSED_NON_BLOCKING；overall restoration percent=null。原版商业二进制、图片和完整外部源码均不进入公开 Git。

