# PET-DETAIL29｜PC宠物成长算法：四套后期源码、精度复原与出生模型（2026-11-22）

## 本轮启动与来源

重新核验GitHub远端main及最近提交、tree完整列表、Actions、连续性协议及完整原docs/CURRENT-STATE.md Git blob（2,709,173字节，SHA c89e0e33537990aa2132b47c40fef49a985a935c，未改）。用户明确要求把重点从玩家攻略成长率转向客户端和服务端代码，本轮据此优先核可执行算法，不扩大玩家文章。

实读以下**四个有固定提交ID**的经典2D PC**社区后代源码**，而非官方1999—2002年原部署服务端。四者有明显共同代码祖源，**不能当作四套互不相关的官服独立证据**。

| PC源码仓库 | 固定提交 | 出生和Rank | 升级 |
|---|---|---|---|
| [BismarckDD/stoneage](https://github.com/BismarckDD/stoneage/tree/999ffdf1d220ec6666eb65339180689c9caf1876) | 999ffdf1… | server/gmsv/char/enemy.c, blob 7ac00643… | server/gmsv/char/char_data.c, blob a8190b44… |
| [gavinlinasd/StoneAge](https://github.com/gavinlinasd/StoneAge/tree/1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56) | 1f90cb6c… | gmsv/src/char/enemy.c, blob 65e5a2e3… | gmsv/src/char/char_data.c, blob 924238fa… |
| [iriselia/StoneAge](https://github.com/iriselia/StoneAge/tree/9e6c8ce2cd8ed532a7157773acd1c61582c178b5) | 9e6c8ce2… | Source/gmsv/char/enemy.c, blob 58662133… | Source/gmsv/char/char_data.c, blob 2b578280… |
| [pimpcapital/longzoro-sa](https://github.com/pimpcapital/longzoro-sa/tree/57b14e2bb373ba851c14db28a239273e4a8831bb) | 57b14e2b… | gmsv/src/char/enemy.c, blob 72e43f44… | gmsv/src/char/char_data.c, blob f12bee31… |

## 源码直接规定的顺序

- `ENEMY_getRank`：先以模板四BASE原和，按100/95/90/85/80归入六档0—5。这里的Rank不是宠物所有者可见的一条官方成长率。
- `ENEMY_createEnemy`：按实例等级，四项BASE分别随机偏移-2至+2，先把偏移后的个体成长基础打包到`CHAR_ALLOCPOINT`；之后再投掷十次0—3分配**出生当时**能力。每项内部出生能力为`((level-1)*LVUPPOINT+INITNUM)*(BASE+offset+十点中该项分配数)`。
- `CHAR_PetLevelUp`：升级独立再投十次0—3，按Rank的对应区间取450—600间的整数，乘以0.01得到浮点倍率；四BASE从原存储`CHAR_ALLOCPOINT`解包，不在升级时重新产生出生偏移。实际C每项分别做两次float32乘、一次float32加，最后转int截断。
- 捕获子程序保留敌人实体的`CHAR_PETRANK`和`CHAR_ALLOCPOINT`，并非捕到时生成全新个体成长基础。图形/主表/技能/实际可抓标志以及源后的面板投影都另需版本和条件限定。

## 发现并修复的精度缺陷

此前`tools/stoneage_pet_growth_model.py`用Python binary64一次算`int((BASE+奖励点)*(roll*0.01))`。这在非整数边界通常近似正确，但并非C源码实际运算语义。

| 源输入 | 独立编译C结果 | 旧Python模型 | 校正后的Python模型 |
|---|---:|---:|---:|
| BASE17+本级3点，roll470 | 93 | 94 | 93 |
| BASE20+本级5点，roll472 | 117 | 118 | 117 |
| BASE22+本级3点，roll508 | 126 | 127 | 126 |
| BASE20+本级0点，roll500 | 100 | 100 | 100 |

全量有界计算对256个可能的存储基础字节×11个独立项目分配点数×151个倍率整数，共425216项进行逐项比较，**1636项**与旧模型有差异。它只是代码算术笛卡尔积，绝非原版425216只宠物或真实出现概率。独立C源码片段由本仓库新测试在CI内用gcc编译后作为校验；这不是原服务端完整构建、实际服务器实战或官方版本验证。对特定平台编译器/优化器/ABI的bit-exact结论仍OPEN。

## 新增可实际调用的出生投影

`project_pet_birth`现接受真实后期模板的四BASE、INITNUM、LVUPPOINT、具体等级、四个指定偏移及出生十次骰值；返回Rank、个体成长基础、打包值、独立出生分配计数和四内部能力。举例：**2016后期社区模板1同图号100250**的BASE20/12/15/25、INITNUM10，假设偏移(-2,+1,+2,0)、出生十次点(3/2/2/3)，对应Rank5、保存18/13/17/25、Lv1内部能力210/150/190/280。这不是台湾1.0「乌力」官方出生数，更不是可见HP/攻击/防御/敏捷。界面面板须经过不同版本`CHAR_complianceParameter`，在装备与其他环境因素尚未排除前不得冒称实际显示四围。

有些后期分支包含`_BT_PET`出生数值倍率、`_LEVELUP_RECOVERY`升级回血和特定玩家NPC/家族声望侧支。通用核心模型仅覆盖**这些可选宏关闭、正常非负基础属性、正常宠物类型**的共通片段；不得把可选编译分支或后期改动强制推广到原官服。

## 官方证据边界与下一个行动

目前仍没有实得1999 JSS、台湾1.0或大陆1.82同部署官方服务端源码和真实Pet主表，因此**只修复已取得PC后代源码的数学复现能力，不提升早年官服认证等级**。早期TW1 124份具名图形观察档、120份原头像、0份全字段官方档案不变，未修改任何早期官服宠物属性/成长/捕获/技能资料；PET唯一活跃，StageA 7PARTIAL+2OPEN、StageB/wiki GATED、R79暂停，整体完成率UNKNOWN。原完整CURRENT历史大文件不动。

[NEXT PET-DETAIL30]：优先在**同一个2016 PC提交和模板版本**内，把模板→出生→升级→`CHAR_complianceParameter`基础面板演示计算链真正接通、明确装备/状态不确定性；若得到可合法直接读取的原PC同部署服务端则立即重审对应早期数值，不因玩家推算替代。机读源表： [PET-DETAIL29](../../research/pets/PET-DETAIL-EVIDENCE29-PC-GROWTH-SOURCE-FLOAT32-R1.json)。

## Stage A历史源码哈希与本次模型更新的兼容验收

Stage A早期审阅包`research/recovered/STONEAGE-STAGE-A-CONSOLIDATED-REVIEW-R2.json`固定引用旧`research/mechanics/STONEAGE-PET-GROWTH-CORE-R1.md`：8969字节、SHA256`891c0ef3…`、原Git Blob`87cdd063…`。本轮修改说明文档后，该旧钉死哈希触发`source custody: pet_growth`失败，属于历史审阅包跟当前源版本不一致，并非源资料缺失。已将历史原pin逐字段保留在`source_pin_refresh_detail29.previous_pet_growth_pin`，当前`source_pins.pet_growth`精确改为10577字节、SHA256`33bf9abfe479f4f9ceb51d4b29d8745eb79b74b594426f6b626b7f35646b2cd2`、Git Blob`568f461f...`。**没有修改验证器或绕过任何哈希比较**；新值和原值分别可审，旧CURRENT状态Blob、StageA门槛及官方证据边界不变。
