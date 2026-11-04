# Stage A | WORLD07：来源限定 GETPET 参数命名空间（2026-11-04）

## 新证据与目标

本轮从 fresh GitHub `main aefb65e192b16ff40985e14d785529356644d768` / tree `6e9c158610ce917ae82a3950ba32c152d6b79595`，完整历史CURRENT保留 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`。只追一条会影响历史任务/宠物身份正确性的尚未闭合规则：`GetPet` 原参数到底是敌人实例号还是直接模板号。**不做联网账号、原服启动、体验优化、新引擎或新宠物设计**。

独立实读固定提交 [`pimpcapital/longzoro-sa@57b14e2bb373ba851c14db28a239273e4a8831bb`](https://github.com/pimpcapital/longzoro-sa/tree/57b14e2bb373ba851c14db28a239273e4a8831bb) 的3个源码原文件：
- [`gmsv/src/npc/npc_exchangeman.c`](https://github.com/pimpcapital/longzoro-sa/blob/57b14e2bb373ba851c14db28a239273e4a8831bb/gmsv/src/npc/npc_exchangeman.c#L3331-L3418)，Git blob `7a9cc7ea6d76bfdae367c580db4ce6fcb42d7d15`：`NPC_EventAddPet`，另原`GetPet`请求分支在2508行、接受分支3140行；
- [`gmsv/src/char/enemy.c`](https://github.com/pimpcapital/longzoro-sa/blob/57b14e2bb373ba851c14db28a239273e4a8831bb/gmsv/src/char/enemy.c#L1468-L1576)，Git blob `72e43f44a76db4baa23dfcea568f16d54d3bf620`：`ENEMY_initEnemy`、`ENEMYTEMP_getEnemyTempArray`、`ENEMY_createPetFromEnemyIndex`；
- [`gmsv/setup.cf`](https://github.com/pimpcapital/longzoro-sa/blob/57b14e2bb373ba851c14db28a239273e4a8831bb/gmsv/setup.cf)，Git blob `9d5992bfb1065d6c405ebe4a0677acb7be0de5f9`：此另一个独立源码仓库配置`enemy1.txt` / `enemybase1.txt`，**不是**已有社区混合2.5资料保存包的同部署选择凭证。

## 该固定后期源码的**直接静态事实**

`NPC_EventAddPet`先检查`CHAR_MAXPETHAVE`携带栏、把单个`GetPet`参数用`atoi`转成`enemyid`；如果参数含逗号则选其中一项，但代码复用此前检查栏位的循环变量`i`，不能未经执行证明任何列表位置的实际概率分布。随后遍历`ENEMY_getEnemyNum()`，比较`ENEMY_getInt(i, ENEMY_ID)`与该`enemyid`，无匹配即返回失败。匹配时传的是**敌人实例表下标**给`ENEMY_createPetFromEnemyIndex`，不是直接以`GetPet`数字索引`enemybase`模板。

另一源码`ENEMY_initEnemy`将实例字段`ENEMY_TEMPNO`关联到模板数组下标，`ENEMY_createPetFromEnemyIndex`再取模板图号、等级、数值、技能及宠物栏。源处理函数`mode=0`在成功后设置`CHAR_ENDEVENT`，`mode=1`不走这一步。这是**该后期保存程序的静态控制流**，非已观察任务运行、真实给宠、保存落盘或同服官方规则。

## 与已经真实读盘的混合2.5资料如何对照

先前[GAMEPLAY07](../../research/recovered/STONEAGE-GAMEPLAY07-GETPET-NPCENEMY-ORIGINAL-SKILL-SOURCE-R1.json)在私人原NPC树真正重新读出27份脚本/29条`GetPet`命令/44次数值/36个不同实例数字，其中4行含多数字、2份为`.old`/`.BAK`备份。23份脚本被CREATE直接静态引用（24个引用）；`jaruga/event/oev_edb`中的`482,482`重复数字不去重。先前[WORLD05](../../research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-05-GETPET-INSTANCE-TEMPLATE-SPR-R1.json)已证明该保存包两候选`enemy`实例表中36项均存在，沿实例外键能联到各自模板/SPR候选，**26个数字也恰与另一模板号相同却不应直接相连**。本轮新增的是**独立固定后期服务端真实源代码的解释链**，不会把旧数值索引重新包装成新宠物发现或假装再次重读私人原RAR。

## 历史适用范围与后续

[完整派生索引](../../research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-07-GETPET-HANDLER-SOURCE-SEMANTICS-R1.json)只记录源码Git blob、函数/行位置、原任务数值及SHA，不发表第三方完整原源码，也不公开私人的商业原脚本/素材。新增专项CI会从**固定提交**只读取上述三个源文件，核对原Git blob身份、原函数控制流及仓库已验数字关系；但**CI不是游戏二进制实际运行**。

该`pimpcapital/longzoro-sa`源码与混合2.5私人归档不在已认证同一运行构建，故从它得到的`GetPet`参数解释为**跨保存件候选机制证据**；未证该混合2.5原EXE以完全同样的命令实现，更不能转称JSS1999、台湾1.0或大陆1.82原始官方行为。保留三项模板PETFLG冲突、发宠成功/失败、奖励存档、名单随机分布、官方任务常驻/活动来源等原UNKNOWN。

保持Stage A **7 PARTIAL + 2 OPEN**、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、overall_percent=null。

**最高NEXT WORLD08：** 仅以新可取得的原始可复验文件推动另外一项尚未闭合的游戏内容/玩法关系；不重复`GETPET`图号、抓宠模拟、查看器或网游账号工程。
