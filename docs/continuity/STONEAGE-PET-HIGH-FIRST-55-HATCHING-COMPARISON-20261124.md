# PET-HIGH-FIRST-55｜后期融合、喂养、孵化路径；原程序符号独立复核（候选）

基于 main 664b4f8ddcef476304ead8bc648f1e15dd8605b3（PET54精确HEAD四项相关Actions均成功）。历史CURRENT保持2,709,173B / c89e0e33537990aa2132b47c40fef49a985a935c。仅经典PC、PET唯一活动模块。此次为固定后期源码的实际文本阅读和候选原字节重演，未声称CI已通过。

## 后期比较源

固定 [gavinlinasd/StoneAge@1f90cb6](https://github.com/gavinlinasd/StoneAge/tree/1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56) 17个源文件/数据blob，详见[机读证据](../../research/pets/PET-HIGH-FIRST-55-LATER-FUSION-HATCHING-R1.json)。不是经认证的原官服部署。NPC_DoPetFusion 选择主/副宠、融合表查输出，删除输入后调用PETFUSION_AddEgg，再设置蛋；不是PET54任务GetEgg同一入口。后者指定raise参数，普通融合SetNewEgg则设置40；不能统一为所有历史宠蛋40次。

- 后期同提交petfusion.arg有重复ADDEGGID，2055、1045。AddEgg按ENEMY_ID而非模板号查找。后期enemy1第1599/1991/1992行分别为2055→1045、2474→1140、2479→1145；enemybase第828/915/916行分别宠物蛋/美拉/美拉蛋，图101489/101760/101489。仅2055与宠物蛋实例直接相容；重复键解析未证，不把1045误作模板参数，不把美拉蛋指为美拉的已证配方。融合师配置三floor 2000/4000/7000，非官服出现证明。
- 后期ITEM_useFusionEditBase以蛋旗标和剩余次数判定；通常PETFEEDTIME=3600秒，消化药可调时间；喂养更新四项EVOLUTIONBASE并减剩余次数，至零走EVOLUTION_createPetFromEnemyIndex。该函数按FUSIONINDEX选择ENEMY_TEMPNO，再取实例和模板、筛15个禁遗传技能、读取融合基础值及加十个随机点，成功产物旗标仍1而次数为0。仅后期比较语义，不等于官方成长公式。
- 该提交version.h启用_USER_CHARLOOPS等五开关；注册60,000毫秒检查间隔，超2.5倍喂养间隔的分支增加剩余次数、四个ALLOCPOINT分量各减6且下限0；无_USER_CHARLOOPS的互斥分支是2倍/减5。另有池中蛋重设和携带蛋时间重设，调用/部署条件尚不定。不能忽略分支差异或把配置常量当历史原服实测。
- char_base.h五个FUSION字段仅是后期条件枚举顺序。原gmsv.exe尚仅PET54确证_NPC_EventAddEgg，不能移植枚举偏移。本候选脚本复读固定原gmsv SHA256，收集十个目标精确text符号、区间、直接调用及调用前立即数候选窗口。不存在的符号只作本二进制符号表阴性，不能认定功能不存在；候选立即数不等于已证字段索引或偏移。原二进制和商业数据不发布，不运行。

## 关口和NEXT

67严格取得缺口不变，0官服取得关闭，0新增官服实发证明；Stage A 7 PARTIAL+2 OPEN，B/wiki GATED、R79暂停、整体UNKNOWN。候选先核17个外部blob及原gmsv派生报告；原字节未复读前不宣称新原符号。接续先检查候选精确SHA Actions及派生JSON，核原程序是否同名/调用轮廓、保留原始收据；无法建立同部署桥时不反复挖融合，转PET55余67特殊对象（动物园、古瓜、雷帝斯洛）分类与具体原证。保留PET54原记录及2002台湾同期三宠＋药材→蛋→饲料→新宠报道的独立来源层。
