# PET-MODULE-04：同源宠物技能代码、实例与技能定义的批量联接（2026-11-02）

固定后期社区源码 [2016 Git 原树](https://github.com/pimpcapital/longzoro-sa/tree/57b14e2bb373ba851c14db28a239273e4a8831bb)，项目候选父提交 673cdb88ff3e794ce23cc00a671caf94f898dc85；只做原版资料静态复原，不提前优化游戏或引入官方断言。

从完整原 gmsv/data/skillcode.txt（blob 44c59d8498c42a685bbf2ab0049b2f9cdeef04a2）读取253行：来源第二、第三数字仅按候选实例ID、模板ID同 PET-MODULE-01 已核验实例表作联接。其中160条与当前配置的 enemy1/enemybase1 记录完全匹配；12条实例存在却引用不同模板；81条实例ID不存在。253行内存在250种不同实例数字，3个重复数值对照保留。来源所指模板有171行 PETFLG1、4行只见 PETFLG0、78行当前表找不到。

原文件具有47种原技能码字符串，共拆出79种不同两字母代码。79种均可与本来源实际选用 petskill2.txt 的 PETSKILL_KINDCODE 字段数值/字面对应；其余原技能表中不出现在该文件的代码不被误报为缺失或禁用。原技能表还保留一个非两字母代码字段，不强行按固定语法拆分。

原同仓库源码 npc_freepetskillshop.c 包含条件路径：按 PetId 在 Code_skill 中查找，再检查技能种类码是否为该字符串的一部分。这只证明源码存在该逻辑；尚未验证 Code_skill 运行时内存数组来自本次 skillcode.txt、二进制真的构建执行或原服实际学会技能，不能提升成运行规则的实证。数值模板冲突及实例缺失全部保留，不静默修补。

完整253行派生数值/源行、79种代码对应的技能ID及148个原非空 KINDCODE 行见 [PET-MODULE-04 指数表](../../research/recovered/STONEAGE-PET-MODULE-04-SKILLCODE-CROSSWALK-R1.json)。不在公开Git复制整份原始宠物名称、专有原图或原始技能文本。Stage A 7 PARTIAL+2 OPEN、Stage B gated、R79暂停、总完成率未知。

NEXT PET-MODULE-05：继续宠物模块，优先把已经私人保存的SPR原位图、动画与带版本的宠物候选图号集中呈现；不回NPC/地图或展开新石器设计。988行混合2.5独立原表完整内容仍未获得。
