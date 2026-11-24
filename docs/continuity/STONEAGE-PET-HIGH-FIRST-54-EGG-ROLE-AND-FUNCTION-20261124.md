# PET-HIGH-FIRST-54｜宠物蛋对象及原程序加蛋入口（原档与后续代码分层）

基于 main 765a44b668330a3d54acb120f62fa98be22d0f22（PET53主线3/3 PASS），原CURRENT 2,709,173B / c89e0e33537990aa2132b47c40fef49a985a935c 不改。PET54预检、原档扫描与静态函数取证已完成；实际CI来源见[固定报告](../../research/pets/PET-HIGH-FIRST-54-EGG-ROLE-AND-FUNCTION-ACCEPTED-R1.json)。本候选最终验收另验，不称已经合并。

## 对象与原档

位置387宠物蛋模板1045/实例2055、位置454美拉蛋1145/2479，同图101489、不同字段；位置453美拉1140/2474、图101760，选中同号模板指纹不同。三条均Lv1双标记、零正权重组路径。四台湾8.5原程序图鉴具名宠物蛋、美拉，无同名美拉蛋。不能把蛋当独立官方物种或由名字直接指定孵化产物。

实际原扫描2205 NPC + 两表共2300545B，7954头、184范围、12013836B；765候选行，730合成、1融合、1饲料，33编号碰撞，0结构化目标ID、0 ASCII egg类命中、0蛋／美拉／孵化具名词。扫描语法有界，不是所有历史服或任意编码的阴性证明。两原作业、ZIP、JSON及原始blob独立核对；原扫描JSON与后续ZIP中副本逐字节一致。派生原报告427240B及静态报告49994B已原样入候选Git，原NPC/EXE不发布。

## 原程序与后续实现独立证据

固定原gmsv.exe SHA256 d5b08dbcbf9e8736ba8598e38e5901f123d2bff544a9cae53a9ff88ce1971e00。_NPC_EventAddEgg 起点4896128，下一text符号 _NPC_EventAddPet 4897696；区间409条指令，49直接调用，来向 _NPC_EventAdd（4905870）/_NPC_AcceptDel（4918854）。内部rand、分隔参数读取、atoi、ENEMY查询和创建宠物、角色宠物槽、经验上限、LogPet；无目标模板/实例编号的立即数候选。仅静态函数区间，不声称完整间接控制流或原服实际执行，不把生成蛋函数当孵化完成函数。

固定后续比较源 [npc_exchangeman.c](https://github.com/gavinlinasd/StoneAge/blob/1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56/gmsv/src/npc/npc_exchangeman.c#L3480-L3609) blob 5d74290ed6f27163e0698b4375d5dc5e187c77c4：两调用分支GetEgg，三段参数为蛋实例ID、产物实例ID、饲养次数；查询产物实例转模板，创建蛋对象，记录FUSIONBEIT/CODE/RAISE/INDEX/TIMELIMIT状态。存在逗号随机候选分支，但未复原概率、输入异常或孵化时序。后续源码语义与原程序调用轮廓相容，**不倒填为同一编译版本的精确字段或参数布局**。无原同包GetEgg配置绑定三个目标；不证明美拉蛋孵出美拉。2002台湾三宠＋药材→蛋→饲料→新宠的同期文献仍独立，不等于任务给蛋路径。

统一查询追加3个既有位置对象/函数边界链接，不增加物种或关闭取得。67严格缺口不减，0实际官服发放。Stage A 7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、整体UNKNOWN。

**NEXT PET-HIGH-FIRST-55**：验收本候选后，优先固定后续比较源码 gmsv/src/npc/npc_petfusion.c、gmsv/src/item/item_event.c、gmsv/src/char/{char,pet,pet_event}.c 中FUSION字段消费/饲养/孵化路径及对应配置，先做一次有界源读、与原gmsv同名符号及字段偏移区分；不为无来源公式反复搜索。若不能建立原同部署桥，保留独立后续机制参考，转余67内其他特殊宠物（如动物园对象、古瓜、雷帝斯洛）分类，继续PET唯一模块。
