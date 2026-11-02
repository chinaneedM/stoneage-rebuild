# O94 — 后期社区原源码人物创建发宠链与同包配置异常（2026-11-02）

## 目标与证据层级

从当前远端 `main` 的 O93 独立服务端源继续，只补齐可改变宠物出生恢复判断的**真实人物创建调用链**。起点 `e13bb3940ce60372ed3fa40b55cf1f747e963f67` / tree `f8441f44e7aa03aab928708662e934c290ea9a54`；`CURRENT-STATE.md` 原生 Git blob `20050acf279a01555ab06a381dfcdc936bd381a6` 已完整读取，不改写。严格**SOURCE_STATIC / LATER_COMMUNITY**：不代表日本 JSS 1999、台湾 1.0、大陆 1.82 或任何原商业服的实际编译运行。

固定来源 [pimpcapital/longzoro-sa @ 57b14e2bb373ba851c14db28a239273e4a8831bb](https://github.com/pimpcapital/longzoro-sa/tree/57b14e2bb373ba851c14db28a239273e4a8831bb)。本包复核同树七份文件，Git blob见 [派生JSON](../../research/recovered/STONEAGE-O94-NEW-CHARACTER-PET-GRANT-R1.json)，完整原源码/商业原表由其来源保留，**未复制进此公开项目**。

## 真实函数、条件与归属链

1. [`version.h`](https://github.com/pimpcapital/longzoro-sa/blob/57b14e2bb373ba851c14db28a239273e4a8831bb/gmsv/src/include/version.h#L411) 行411声明 `_NEW_PLAYER_CF`；[`char.c`](https://github.com/pimpcapital/longzoro-sa/blob/57b14e2bb373ba851c14db28a239273e4a8831bb/gmsv/src/char/char.c#L225-L445) 行225起的 `CHAR_createNewChar` 在该条件段中执行。源码宏定义存在不等于实际发布服编译启用。
2. 行370–379检查 `getNewplayergivepet(0)==-1`，以 `CHAR_LASTTALKELDER` 1→实例2、2→3、3→4、其他→1写回**同一全局** `config.newplayergivepet[0]`。这些编号在同源 `enemy1.txt` 第一组确实分别对应凯比、克克尔、威伯、乌力乌力；这是**静态候选村落连接**，不是原服实际发送与存档见证。
3. 行384–402遍历**五槽0–4**，经 `ENEMY_getEnemyArrayFromId` 取实例，`ENEMY_createPetFromEnemyIndex` 创建；[`enemy.c`](https://github.com/pimpcapital/longzoro-sa/blob/57b14e2bb373ba851c14db28a239273e4a8831bb/gmsv/src/char/enemy.c#L1468-L1575) 通过模板设置图形/宠物ID，写入玩家宠物格、主人标识，返回宠物索引；[`char.c`](https://github.com/pimpcapital/longzoro-sa/blob/57b14e2bb373ba851c14db28a239273e4a8831bb/gmsv/src/char/char.c#L431-L445) 随后调用人物保存。保存**函数调用**有据，不宣称服务端保存成功或登录后持久化成功。
4. 同树 [`setup.cf`](https://github.com/pimpcapital/longzoro-sa/blob/57b14e2bb373ba851c14db28a239273e4a8831bb/gmsv/setup.cf#L186-L215) 实际配置 `PET1=2665`、`PET2=2744`、`PET3/4`空、`PETLV=1`；[`configfile.c`](https://github.com/pimpcapital/longzoro-sa/blob/57b14e2bb373ba851c14db28a239273e4a8831bb/gmsv/src/configfile.c#L417-L445) 仅把 `PET1..4`映射槽1–4，而不是槽0。因此**四出生候选以外还有两只明确的配置实例**，不能将O93的四只称为此配置的完整出生宠物集合。

## 同一原树中6个实号的两层身份（保留差异）

| 创建来源 | 原实例ID/原行 | 实例原名 | 模板ID/原行 | 模板名称 | 图号 | 实例Lv |
|---|---:|---|---:|---|---:|---|
| 槽0村落候选 | 1 / 1 | 初期拥有的乌力乌力 | 2 / 2 | 乌力乌力 | 100251 | 1–1 |
| 槽0村落候选 | 2 / 2 | 初期拥有的凯比 | 112 / 108 | 凯比 | 100296 | 1–1 |
| 槽0村落候选 | 3 / 3 | 初期拥有的克克尔 | 102 / 98 | 克克尔 | 100292 | 1–1 |
| 槽0村落候选 | 4 / 4 | 初期拥有的威伯 | 34 / 34 | 威伯 | 100266 | 1–1 |
| 配置PET1 | 2665 / 2150 | 青龙 | 1275 / 1030 | 凯恩 | 101180 | 1–1 |
| 配置PET2 | 2744 / 2230 | 葛多雷诺 | 1354 / 1110 | 葛多雷诺 | 101951 | 150–160 |

注意PET1实例**青龙**与模板名**凯恩**并不相同，源码按模板生成宠物名；不能自行将名字统一为原游戏物种。PET2实例原Lv范围**150–160**；`PETLV=1` 的代码只按目标与现等级差执行升级循环，**不会把Lv150–160降回Lv1**。这只是静态语义；随机等级、实际发放、真实存档尚未执行。

## 两项限定的静态风险／反例（不判历史BUG）

- `getNewplayergivepet(0)` 读取的是**进程级 `Config config` 全局槽**，`setNewplayergivepet(0,...)` 在出生判断中修改它；同一函数内无每次创建前重置。若首次访问使槽0变正值，后续人物建角不会再依据自己的 `CHAR_LASTTALKELDER` 走分支。这是**可能的跨角色污染路径**，不是已观察的部署事故；是否存在其它外部重设、线程状态及实际运作仍未知。
- `getNewplayergivepet` 对零/负数**返回-1**，然而 `char.c` 的循环只写 `==0` 时跳过，所以空槽可能继续查实例-1。原 `ENEMY_getEnemyArrayFromId(-1)` 未找到时返回-1，`ENEMY_createPetFromEnemyIndex` 首先检查 `ENEMY_CHECKINDEX` 并拒绝。**静态失败分支有边界，不能据此宣称发宠失败或发生崩溃。**

另须保留：O93已证第二组实例2112–2115各1–3级，但本新角色创建段使用的槽0默认实例1–4，**不能把第二组误认成该代码段直接调用的对象**；是否另有发放路径未穷尽。

## 验收、止点和后续

本轮直接重读7份同Git提交源，对指定宏、创建/归属/保存调用、全局槽写入、空槽异常、`PETLV`只升不降、六个实例→唯一模板及图号、配置行逐项做固定源码断言（见JSON布尔结果），所有指定断言为true。**没有编译、运行原GMSV、启动客户端、解码本源图像或获取同构建SPR/REAL/ADRN**；不将此前不同客户端上相同数字图号证明为同部署。

O94完成的是**一条真实后代数据表+出生发放源码+配置的有界静态合同**，不是初代发宠最终恢复。下一最高 `O95`：优先查已有可验证原客户端是否有与这组图号**同构建**关系的真实SPR/ADRN/REAL及原观察帧，或者出现真正独立的原服创建运行输入；若没有，则及时轮换到地图/NPC/本体任务有实际原件的内容，禁止连续扩社区助手、网页猜测或新游戏体验优化。原 Stage A **7 PARTIAL + 2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、整体百分比 `null`，均未晋级。
