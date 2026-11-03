# 按内容模块集中复原：执行顺序与宠物优先（2026-11-02）

**性质：** 原版《石器时代》历史复原工作的执行调整，不是新石器设计。起点远端 `main` `3bce6086a913bbb4e67999b028cd55801df33a37` / tree `bad7556a90d5ba2187c2c9faddc0dfceed3d2dd5`。历史主体 `docs/CURRENT-STATE.md` Git blob `20050acf279a01555ab06a381dfcdc936bd381a6` 不重写。现有22域审计、原9系统7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、总体完成率未知均保留。

## 为什么调整

之前技术任务按原SPR某组、NPC一名、地图一个窗口、任务一个文本不断跳转，各自可证但缺少「这个模块到底恢复了多少实际游戏内容、可连续查到什么、哪些真实图片和数值已成套」的累积交付。今后以整个内容模块为**持续主线**，单轮小核查只作为该模块的必要步骤。没有真实原内容增量的抽象、报告与脚手架不得算复原进度。

## 复原顺序与交付面

| 次序 | 模块 | 至少整理的内容 |
|---|---|---|
| 1（现在） | **宠物** | 已取各版本候选宠物的2D原位图/SPR动画、动作/方向、名称别名、原服务器模板/实例、基础属性/成长/技能/捕捉或获取途径（有证才填）、版本和来源/负证 |
| 2 | 人物与NPC | 原人物形象与动作、NPC图形、坐标、配置、功能、对白，保留原实物与同构建界限 |
| 3 | 地图与场景 | 地图文件、分层/贴图、障碍、地标、入口/出口，原NPC或宠物配置作跨模块引用 |
| 4 | 物品、装备、商店 | 原图、ID、属性、效果、配方、售价与各版独立配置 |
| 5 | 任务与剧情 | 常驻本体任务和节日/时点活动任务**严格分开**，原触发、步骤、地图/人物/奖励关联 |
| 6 | 玩法机制与界面声效 | 捕捉/回合战斗/成长/技能/骑宠/精灵/合成/存档/音效/UI，按原版实际可验行为 |
| 7 | 历史整合与观察 | 宠物↔地图↔NPC↔物品↔任务↔机制的来源限定关联、原世界可观察性与真正运行缺口 |

顺序是工作集中原则，并非数据隔离。宠物在特定地图出现时，先在宠物条目保存**源证据指向地图的引用**，不因此切走复原整张地图。宠物涉及捕捉技能时记录关联，不因此提前开发全部战斗。即使完成全资源目录也**不等于**原游戏可执行：还须地图连接、原交互、状态、系统行为与跨模块核验。

## PET-MODULE-01：实际下一批，不再单点轮换到 O96-NPC

**1. 全量盘点现有可读取载体。** 重用已归档台湾Waei/JSS1.0（认证零售样本）、大陆5.0候选、台湾8.5候选、混合2.5社区保存版和有来源的后期社区服务端宠物表，以及历史资料中确有证据的其它正式版本；源身份逐条注明。**不把这四份保留客户端叫作「四个纯净官方版本」；大陆1.82纯净完整客户端目前尚未认证，1999日本JSS原始同部署服务端未取得。** 后续找到原版载体随时追加，不要求当前一次获取「史上所有客户端」才能开始。

**2. 按批量资源而非逐只猜测重组。** 复用 `research/recovered/tw10-resource-metadata/`、`cn50-resource-metadata/`、`tw85-spr137-r28/`、`STONEAGE-PRESERVED-PET-SPR-SOURCE-R40.json`、`STONEAGE-O93...`、`STONEAGE-O94...`、`STONEAGE-O95...` 等已验物理索引/表；为*可由原本源证认定*的宠物建立一条版本明确的记录。未知名称的SPR组仍叫候选动画组，**464 / 1185 / 1739 / 847是各样本动画组数量，绝不能称为宠物种数**。同名不同版、同号不同文件、同源相同SHA均分别保留并审查，而非无条件合并。名称不同或模板/实例不同不强行统一。

**3. 真正恢复可看的东西。** 在合法私人研究环境中批量由实际位图、SPR、索引和配色渲染宠物原图及动作，重用已存在的解码器/观察器；对能从真实服务器数据找到模板、数值、技能与获取途径的补齐数值。每个可识别条目在实际资料中至少区分「原图可观察／原动画有据／属性有据／技能有据／原生运行已观察」五个不同维度。公开Git只保留可分发的派生元数据、名称、SHA及方法，不直接发布受版权约束的图像与二进制。

**4. 给出成体系的宠物资料目录。** 最先交付的不是第N份单宠分析，而是当前来源范围内可连续查阅的**全部有源宠物候选/已识别宠物索引及来源覆盖**，附同载体去重/跨版继承、每个条目缺什么、可打开哪份私有原图观察资料。以一个集中入口持续扩充，不制造新复杂框架或重做旧项目。

**5. 宠物模块的阶段性止点。** 已取得的可读取源批量处理并清点、可证明的名称↔图/动作↔原数值关系接通，未获资格的同构建关联与官方宠物数量保留UNKNOWN，不再无限单个文件搜索；随后进入人物/NPC模块。若之后获得真正新官方客户端/服务端资料，增量重开受影响宠物记录。**已覆盖已取得的材料 ≠ 还原了全历史所有版本的宠物。**

## 可直接复用的旧成果与当前缺口

- O93/O94 已把一份2016后期社区服务端 `enemy1.txt` / `enemybase1.txt` 的**2958条实例和1816条模板**有限联接，出生发宠与数值可查，但不是初代官方名单或完整历史宠物数量。
- O95 已按**六个实际后期服务端图号**检查四份保存客户端的实际SPR组：前四组在TW1/CN5/TW85完整动画段SHA一致，第五组在CN5/TW85一致，第六组在TW85有组；这仅是极少数样本，不等于宠物模块全量整理。
- 原台湾1.0宠物画像/原SPR及相关视觉复原、混合2.5保留服务端宠物技能、原地图宠物店等此前工作照样保留，以精确来源回填宠物综合目录；不重跑已验SHA以充任务量。
- **最大真实缺口：** 原生宠物物种身份与SPR的同版关联、原服务器完整主数据、早年官方大陆1.82等精确版载体、真实宠物获取/培养/战斗运行。不应在未得原件时编造或抬升后代资料。

**即时最高 NEXT：`PET-MODULE-01 SOURCE-BATCH-CENSUS`。** 先盘点可用原宠物主表与原图／动画载体，产出一个可核的大批量综合索引和可观察输出；已存在的物理SPR组计数不得复用成「新发现宠物数」。不先修与此无关的NPC、地图、交易或设计新石器；当宠物批处理证据不足并完成明确阶段性结论时才转换模块。旧 O96 的零散世界/NPC轮换作为历史计划保留，但不是现行首要任务。


## PET-MODULE-03 同源技能联接进展（2026-11-02）

[同源技能批量报告](continuity/STONEAGE-PET-MODULE-03-SAME-SOURCE-SKILL-JOIN-20261102.md)已将2016后期社区固定源码的1024宠物候选模板与宏配置下282条petskill2技能定义按真实ID核对；正数槽2886次，2784可定位、102无定义，原20负值槽与4262空槽保留。来源不同于TW1/JSS商业同部署；988行独立混合2.5原表本轮未取到，不虚称比完。**下一优先 PET-MODULE-04**：仍集中宠物，查同源skillcode实例/模板外键或将已存原动画观察整合，不启动其它模块。


## PET-MODULE-04 — 2016 same-source skillcode numeric/skill-token crosswalk (2026-11-02)

[PET04 source comparison](continuity/STONEAGE-PET-MODULE-04-SKILLCODE-CROSSWALK-20261102.md) records 253 original skillcode rows against current 2016 source enemy tables: 160 exact, 12 conflicting template IDs, 81 absent instance IDs. All 79 two-letter code tokens match the separately selected skills table KINDCODE string. Conditional source checks PetId and token but actual Code_skill initialization, skill training, commercial server execution are OPEN. Original 988 mixed25 rows still missing, no images re-rendered in this round. NEXT PET-MODULE-05: actual retained private pet image/frame/action observation integration, still pet module only.


## PET-MODULE-05 完成的私人原图/动作集中观察目录（2026-11-02）

[源限定完整覆盖报告](continuity/STONEAGE-PET-MODULE-05-PRIVATE-VISUAL-CATALOG-20261102.md)及[598图号/1024模板综合索引](../research/recovered/STONEAGE-PET-MODULE-05-CONSOLIDATED-VISUAL-COVERAGE-R1.json)：从私人 O11/SCENE28/R10/O65 已保管原像素回放数据构成单一私有离线观察目录，实际7图号、76源动画/方向序列、718有序帧位置、440原图候选PNG逐源SHA通过；Chromium144全部76序列选择及图片载入通过，0 JS错误/0外部网络请求，file://在本环境被安全策略阻断、原游戏未启动。公开只留数字/来源哈希/覆盖索引，无原图。2016社区1024宠物候选模板中22行同数字图号可连接本私人观察目录，不得晋升成初版官方物种。**NEXT PET-MODULE-06**集中增加已取得原图的来源合格批次并补齐模块索引，暂不轮换其它内容模块。


## PET-MODULE-06 两组已保管TW1原像素加入单一宠物观察目录（2026-11-02）

[PET06实物与边界](continuity/STONEAGE-PET-MODULE-06-TWO-MORE-SPR-20261102.md)及[更新后的598图号/1024模板全索引](../research/recovered/STONEAGE-PET-MODULE-06-CONSOLIDATED-VISUAL-COVERAGE-R1.json)：从私人已归档的O28独立ZIP重读100297/100298两组真实台湾1.0图，逐52帧位置PNG SHA核对，39个不同原bitmap，6条实际动作0/1/2但仅方向0；复用PET05唯一私有观察器，现合计9图号、82动作方向序列、770帧位置、479实际来源PNG，Chromium144实证82个序列选择与加载、0JS错误/0网络。对2016社区PETFLG1全部1024模板行，25行同数字可到私人预览、589图号尚不在本预览；不论当代官方名字及同部署均UNKNOWN。**NEXT PET-MODULE-07**仍集中原宠物图像批量归档，停止无实体增量的单点helper。



### 2026-11-02 — PET-MODULE-07 台湾1.0完整原客户端批量宠物图形实际像素

[PET07批量实物报告](continuity/STONEAGE-PET-MODULE-07-TW10-130-REAL-PIXEL-BATCH-20261102.md)及[源限定130组/2176块可解码原图证据](../research/recovered/STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json)：重新取用户私人原 P3H 原始包并全SHA固定，对2016后期宠物模板图号与台湾1.0原SPR取130组数值交集，原7568条SPR动作头全组核验，选原动作0/1/2方向0的390源动画/3255帧，原REAL实际重解码2176个RD块，两个真实越界坏源保留负例。私人统一观察器（不公开商业图片）已覆盖130组/451动作方向/3817按原序帧位/2540候选PNG，Chromium144全部451段可切换/下一帧、0JS/0请求。仅跨版数字参考，非TW1官方130种物种。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、整体完成率未知。**NEXT PET-MODULE-08**：在这一单一宠物目录连接已保管技能数值，但严格分源；余下468个图号继续查已保管不同版本实际像素，不扩无谓查看器。


### 2026-11-02 — PET-MODULE-08 图形/属性/技能严格分源综合目录

[PET08可核的598图号×1024后期模板目录](../research/recovered/STONEAGE-PET-MODULE-08-VISUAL-STATS-SKILLS-SOURCE-CATALOG-R1.json)与[PET08实施及证据边界](continuity/STONEAGE-PET-MODULE-08-SOURCE-SEPARATED-CATALOG-20261102.md)：完整联接PET01/03/06/07现有派生证据。130图号存在TW1原图私人可视数据的**跨年代数字候选**，对应201社区模板行；468未进PET07图像批次（412后期有索引/56四载体均无索引）。2,886正数技能槽=2,784后期同源定义+102缺定义；20负值、4,262空槽完整保持。既有私人PET07原图HTML不改、不公开；无新版官方命名或同服运行证明。**NEXT PET-MODULE-09：**有限查已有CN5/TW85私人原像素补齐后期候选，缺原件即记录止点并按模块顺序转人物/NPC。阶段A/B/wiki/R79、总进度未知不变。


### 2026-11-02 — PET-MODULE-09 原SPR跨版验证与八帧TW85既有原像素归位，宠物阶段性有界止点

[PET09完整598图号来源分级](../research/recovered/STONEAGE-PET-MODULE-09-CROSSCARRIER-ORIGINAL-MATERIAL-RECEIPTS-R1.json)及[本轮源证/止点](continuity/STONEAGE-PET-MODULE-09-CROSSCARRIER-PIXEL-BOUNDARY-20261102.md)：130图号在PET07先前有TW1原像素；214图号CN5与TW85原SPR整个动画段已证完全一致但不认证RD像素相同；198仅有TW85索引，其中图号101501早在R30已有源验证8帧原RD索引像素/私人PNG收据，本轮与后期社区模板物理行843/1184仅做**跨年代同号链接**，未重新读取私人像素；另外197仍只有索引，56四载体没有图形号索引。累计按图号有131项**先前有真实原像素证据**，并不是131个官方物种。CN5/TW85整批原商业文件本轮不可直接读取，不能把源索引当已解码图；记录材料阻塞后不重复下载大包。**宠物模块现 SOURCE_BOUNDED_PARTIAL**，继续历史复原下一模块 `CHARACTER-NPC-MODULE-01`。原CURRENT不变、Stage A/B/wiki/R79和overall_percent=null不变。


### 2026-11-02 — PET-MODULE-10：混合2.5原始RAR内988行宠物主表/实例/技能完整实物回读

[PET10原8成员完整数值索引与SHA/CRC](../research/recovered/STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json)及[实物与来源边界](continuity/STONEAGE-PET-MODULE-10-PRIVATE-SERVER-MATERIAL-20261102.md)：用户Library现存原RAR361255180B全SHA本轮实际重校，libarchive真取8原成员。主表enemybase.txt有效988行/56字段，PETFLG1有495行、424图号；另一份640行/316宠物候选。2087/1494实例分别与对应模板全数ID匹配；主表147原技能定义支持1050正数宠物槽全部定义，备选56技能定义支持661正数槽中的649，12缺。与原RAR同载体847条SPR索引按数值关联，主表495宠物标记行302命中、234不同图号。私人原CP950全字段目录和无网可查HTML已保管，不向公开Git提供原名/原表正文/版权图。原SPR主体本轮受libarchive解压限制未完整取出，不称动画像素新恢复。PET09此前CN5/TW85大包不可读止点照旧；**PET10额外找回同包服务器实物**。宠物模块保持历史部分/来源限定阶段性闭合，**NEXT CHARACTER-NPC-MODULE-01**；无需替用户再要「继续」。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总体percent=null。


### 2026-11-03 — CHARACTER/NPC-MODULE-01 完整原NPC目录源批量恢复

[CHAR01精确来源与有限结果](continuity/STONEAGE-CHARACTER-NPC-MODULE-01-MIXED25-NPC-BATCH-20261103.md)及[公开源计数/资格收据](../research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-MIXED25-SOURCE-RECEIPT-R1.json)：从私人mixed25原RAR本轮真实解出完整NPC目录2205个原文件/1930332B，原RAR目录7952项逐遍历，2205份原大小、SHA、CRC全部通过。189份NPCCREATE含4985静态创建块，46份NPCTEMPLATE含119原块；配置关联4131同目录唯一+853同RAR他目录唯一+1歧义，1803个原file:引用中1788同目录树有源文件、15缺。源可观察私人HTML已本地Chromium实测，原全目录ZIP成功私有Library保存。**这些是配置条目而不是4985个NPC/人物**，无官方版本/原运行晋级；TW1先前12人物SPR与101静态类NPC图元独立保留。大行级公开索引仅当前会话可取，远端只固定其SHA和源统计，禁止冒称已持久Git。**NEXT CHARACTER-NPC-MODULE-02**：TW1人物12组及静态101候选原帧像素批量归档。原CURRENT及Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停/总体percent=null不变。


### 2026-11-03 — CHARACTER/NPC-MODULE-02 台湾1.0十二组人物候选原动作2全帧恢复

[CHAR02来源限定真实原像素/动作完整批次](../research/recovered/STONEAGE-CHARACTER-NPC-MODULE-02-TW1-12-ACTOR-ACTION2-RECEIPT-R1.json)及[恢复说明](continuity/STONEAGE-CHARACTER-NPC-MODULE-02-TW1-12-ACTOR-PIXELS-20261103.md)：从已认证TW1原零售P3H私人源包逐全原件SHA重核EXE/SPR/ADRN/REAL/双SAP；12图形候选组（100000～100220每20一组）的完整原SPR段SHA与旧SCENE23逐个一致；动作码2的8方向96条原序列共有728源帧位置/576不同原位图，原REAL实际解出576/576块、严格RD失败0，旧SCENE23的96源首帧像素SHA全部一致。私人完整262602B逐帧证据表与6578861B原图HTML只作当前会话可下载，不在Git上传原商美术；Chrome本地实际96段读图/帧和候选配色、0 JS/0网络。原商业游戏未进入、12个候选并非官方认证角色数、动作/真实颜色/FPS未知。**NEXT CHARACTER-NPC-MODULE-03：TW1源静态NPC-like 101图块原像素批量验收**，源R99里101个源bitmap不能当101 NPC。保留原CURRENT和全部历史边界不变。


### 2026-11-03 — CHAR03：台湾1.0 NPC-like 101原静态图实际RD像素批量复原

[原101图原始RD像素收据](../research/recovered/STONEAGE-CHARACTER-NPC-MODULE-03-TW1-101-STATIC-RD-RECEIPT-R1.json)及[本轮源边界说明](continuity/STONEAGE-CHARACTER-NPC-MODULE-03-TW1-101-STATIC-RD-20261103.md)：TW1原P3H同源ADRN/REAL及双SAP实际逐完整SHA核实，5846～5946编号101源原RD块逐原像素实际解码101/101成功、0失败，逐源哈希与原R99全部101项吻合。私人原RGB候选原图联系表及浏览器101图（两配色101/101已载入、0JS/0请求）保存为本轮可取文件，原艺术品不公开Git。**101是静态图像数，并非101个官方NPC**：目视混有人形和床铺、钱袋等物件；原`map_number`不是楼层、后期mixed25 NPC姓名不与早期TW1强行绑定。**NEXT CHAR04**审核人物/NPC同源身份绑定，未得同版主表保持UNKNOWN。原CURRENT及Stage A/B/wiki/R79和overall_percent=null不变。


### 2026-11-03 — CHAR04 人物/NPC创建原件→模板功能→同RAR原SPR图号的全量来源关联

[CHAR04真实原件关联及差异审查](continuity/STONEAGE-CHARACTER-NPC-MODULE-04-STATIC-GRAPHIC-FUNCTION-20261103.md)及[CHAR04全量图号×原模板功能×SPR索引](../research/recovered/STONEAGE-CHARACTER-NPC-MODULE-04-SAME-CARRIER-GRAPHIC-FUNCTION-JOIN-R1.json)：从用户私人保存的mixed25原NPC目录ZIP全量核2205原文件、4985创建源块、119模板源块SHA全部吻合；把此前只在用户私人资料/会话保存的[CHAR01 4985行无正文源证](../research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json)正式永久入Git，字段仅数值/来源位置/散列及文件引用。原功能Warp配置2904（非2904人），模板唯一定位4984/4985。创建原图号有2482条，其中617条/108不同图号命中同原RAR客户端SPR索引；1865条/146不同图号无本索引；35条原模板type与创建graphicname数值不一致，逐条保留；3个既往R40原完整SPR段号100250/251/252可联30条原创建配置。仅同RAR数值关联，**不是**原运行服同部署、同原图可视像素、官方人物或TW1 NPC姓名身份证明。下一优先CHAR05有源批量原SPR/像素及NPC原用途关系，不重复造图及引擎。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总percent=null；原CURRENT保持原字节。


### 2026-11-03 — CHAR05 已验来源重用（此前CURRENT已有）

[CHAR05三组原SPR像素与30份NPC创建配置联接](continuity/STONEAGE-CHARACTER-NPC-MODULE-05-SAME-RAR-ORIGINAL-MOTION-20261103.md)已恢复并验证：同RAR 100250/251/252 三组动作0、24方向序列、352帧位置/208既有真实RD图；30条静态创建配置引用。剩余105图号/587配置依然只有SPR索引，历史身份证明不能由同图号推出。本节只是把CURRENT已有的CHAR05指向补入集中模块入口，不算重新恢复。

### 2026-11-03 — CHAR06 同载体NPC服务原文与静态参数（47条）

[CHAR06原字节、解包止点及来源边界](continuity/STONEAGE-CHARACTER-NPC-MODULE-06-SERVICE-SOURCE-20261103.md)与[逐行源SHA/路径/数值目录](../research/recovered/STONEAGE-CHARACTER-NPC-MODULE-06-SERVICE-SOURCE-RECEIPT-R1.json)：从私人mixed25原RAR完整SHA复核并成功提取2205份原NPC文本，逐成员大小/CRC/SHA通过。剩余105组同RAR图号的原SPR/REAL实际提取遇到libarchive不支持或报错，只有未经完整资格确认的SPR前缀，不可宣称获得原像素，仍105图号/587配置INDEX_ONLY。转而恢复同RAR NPCCREATE→NPCTEMPLATE(functionset)→file:原参数文件：SavePoint21、Bus7、PetShop16、PetSkillShop3，共47条来源限定原关联，含原记录点ID/出生坐标、7组公车路线点列、宠物店费率/寄养字段、宠技参数。另生成私人自包含原文观察页，未把商业原对白上传Git、也没运行商业原客户端或服务器。47不等于NPC数量，时间单位/价款/运行选择不能从静态定义直接确证，mixed25也非纯净官方同部署身份。**NEXT CHAR07**：仍集中人物/NPC，对已得2205原文本扩展TownPeople/告示及其它功能原文来源与类别批量索引；达到有界止点再转地图模块。Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、overall_percent=null，CURRENT历史前缀不变。


### 2026-11-03 — CHAR07 原NPC村民对白与告示文字552条原文件实物联接

[CHAR07完整来源/界限](continuity/STONEAGE-CHARACTER-NPC-MODULE-07-TOWNPEOPLE-SIGNBOARD-ORIGINAL-TEXT-20261103.md)及[CHAR07逐567源配置引用与15缺件目录](../research/recovered/STONEAGE-CHARACTER-NPC-MODULE-07-TOWNPEOPLE-SIGNBOARD-SOURCE-CATALOG-R1.json)：直接复用已实际解出的mixed25 NPC完整2205源文件，用原create/template/functionset逐源块关联TownPeople387引用、SignBoard180引用；其中TownPeople372有原文/15缺、SignBoard180全部有原文。全部552实际原文CP950解码无替换字，按原SHA/CRC/文件大小核；缺15文件在同RAR全7952成员查无路径/同尾文件名，不能抬为整个历史发行缺失。原文本字面逗号/\\n只是源字节，尚无运行分支/行规证据。私人自包含观察器现已实际由Chromium144校验552原文及两类筛选、0脚本错误/外部请求，原版权对白未进入Git。567是配置引用数，不是NPC人物数；原商业世界未进入，同服/官方TW1身份未知。**NEXT CHAR08**集中有原件的任务交换NPC源条件/物品参数关系，任务原产地分类严格保留UNKNOWN；若有界材料已用尽，再按既定模块顺序转地图。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停及overall_percent=null不变。


### 2026-11-03 — CHAR08 同 RAR ExChangeMan 原脚本与两份 itemset 原数值关联

[CHAR08 原始脚本/双物品表的有界证据](continuity/STONEAGE-CHARACTER-NPC-MODULE-08-EXCHANGEMAN-ITEM-EVENT-20261103.md)和[可远端重放的源统计收据](../research/recovered/STONEAGE-CHARACTER-NPC-MODULE-08-STATIC-SOURCE-SUMMARY-R1.json)由私人已验混合 2.5 原 RAR 重新实读：315 条 NPC ExChangeMan 创建配置真实指向 295 份不同原脚本，全部 295 份实物可取；源 TYPE=1349（MESSAGE769、ACCEPT494、REQUEST81、CLEAN5），EVENT=1349、EventNo=1348，未擅自补齐不齐字段。原实际双 itemset 13254/13915 唯一 ID（零基列16，列17原图号），后一份独有 661 ID；380 不同源脚本物品数字 ID 中 372 两表原行同 SHA、1 原行异（18340）、5 仅后表有、2 两表均缺。全部仍静态源候选，未证明源脚本执行、同时生效部署、TW1 原服、任务常驻/运营活动来源；315 条起源均 ORIGIN_UNRESOLVED。源 RAR 全 SHA、2205 原 NPC 文件及 CHAR07 552 原文本块重复核验成功。完整 338200B 无版权正文逐行目录 SHA 已固定在收据，**当前文件桥失效未入 Git，不能伪称已发布**，公开仓库仅保留汇总收据/测试/本源边界。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、整体percent=null；原 CURRENT 字节完整保留。**NEXT CHAR09：** 同原 RAR NPCEnemy 实物关系的有界批量调查，然后人物/NPC SOURCE_BOUNDED_PARTIAL 止点再转地图模块。

### 2026-11-03 — CHAR09 原 NPCEnemy 279 创建配置到 230 敌人实例 / 214 模板 / 117 原 SPR 图号

[CHAR09 同原包静态源关系与止点](continuity/STONEAGE-CHARACTER-NPC-MODULE-09-NPCENEMY-SOURCE-20261103.md)和[完整来源限定 JSON](../research/recovered/STONEAGE-CHARACTER-NPC-MODULE-09-ORIGINAL-NPCENEMY-ROSTER-BRIDGE-R1.json)：私人混合 2.5 RAR 完整 SHA 固定，从原 2205 NPC 子树及 4 份敌人实例/模板表、原 spradrn_5.bin 真正校验源字节。279 个 NPCEnemy 原创建配置均可联原 .arg，共 260 不同原参数；引用的 230 个不同实例 ID 在同包两套 enemy 表全都存在，分别可联 214 个模板 ID、117 个图号，117 个全部在同包 847 条 SPR 索引中有**唯一**源记录。整 SPR 索引仍保留 5 个重复键/6 个额外记录，与本批图号不相交。两实例表同 ID 的 230 原行 SHA 都不同，模板行仅 145 个 SHA 相同；同号/同模板/同图号不等于相同原服部署。此前 NPCEnemy 200 gym/79 普通的基础规则旧资料保留，不算本轮新发现。没有新原像素、真实原战斗或 TW1 官方身份，105 早前图号/15 原村民缺件仍未补；Stage A 7 PARTIAL+2 OPEN、B/wiki GATED、R79 暂停，overall_percent=null。

**人物与 NPC 模块当前状态 SOURCE_BOUNDED_PARTIAL。最高 NEXT MAP-SCENE-MODULE-01：** 按既定模块顺序批量归并已获原地图/贴图/建筑/出入口的实际源文件与可观察范围，优先复用已有实物，不重复写单点工具或再把旧地图数量当新成果；原 RAR/官方不全或缺原资源时明确保留差距。旧 CHAR08 NEXT 保留历史，不再为当前优先级。

### 2026-11-03 — MAP-SCENE-MODULE-01：批量源地图真实字节与跨目录差异

[MAP01 来源 / 受限边界报告](continuity/STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-MAP-SOURCE-20261103.md)和[2990条实际CRC/SHA验原地图文件、63条读取负证 JSON](../research/recovered/STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json)：私人已验混合2.5 RAR 选3053份原客户端 MAP/DAT、附带工具 MAP及3份服务器地图配置；2990份实际全解包且大小/RAR CRC/新SHA一致，63份libarchive读取失败、不提升为原包损坏。客户端MAP1019、DAT971、附带工具MAP997、服务器原表3；数字地图宽高与源字节公式有2971个核验。965份MAP/DAT都可读，953对同宽高且有非空DAT、12对DAT是实存零字节。996对同名源 MAP 两子树有898逐字节相同、98实际不同（非真实发行变更因果）。两源mapset有20157/16803行，共同16803个ID中16802行一致、1行ID10230不同；主表额外3354 ID，不是3354地图新增。mapwarp源2981完整数字端点引用，其中500条源/目标都不在这一份mapset。原游戏画面/碰撞/原服务器真实选图与运行仍未验证；整RAR和各目录不认证官方同部署，原美术不公开。

**MAP01 当前状态 SOURCE_BOUNDED_PARTIAL；最高 NEXT MAP-SCENE-MODULE-02：** 只对已真实SHA/CRC核的地图原字节，批量梳理地图格/层/原图号到既存可见原素材的关系；优先处理实际不同或未观察材料，来源未解码的63项维持UNVERIFIED，绝不以生成图冒充原画面。Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、overall_percent=null、原大CURRENT全部保留。


### 2026-11-03 — MAP-SCENE-MODULE-02：三张原 DAT 及 780 份台湾1.0 原图块实际解码

[MAP02 来源/止点报告](continuity/STONEAGE-MAP-SCENE-MODULE-02-THREE-DAT-ORIGINAL-PIXEL-BATCH-20261103.md)与[逐792图号源SHA/图块元数据](../research/recovered/STONEAGE-MAP-SCENE-MODULE-02-THREE-ORIGINAL-DAT-FLOOR-IMAGE-JOIN-R1.json)：独立实际读取保存的原1000/1001/1003.DAT整文件，160×160+30×30+30×30共27400原格；三平面原字节SHA均固定。1000有752原图号，其中740在真正台湾1.0原ADRN/REAL中唯一命中并实际RD解码，12个无该原载体图号（严格缺件）。三图源图号联合792、真实原RD解码780/失败0，私人780PNG索引包单独保存，版权图片不公开。旧O54已实绘198图号逐完整原RD和RGBA SHA复核一致，1000新增相对O54的原像素可见图号542；此处不宣称历史首次发现。1001/1003相同30×30，却有三原平面8/51/84格不同，禁止静默共用场景。MAP01对1000.DAT原RAR解包63失败项中的一项保持失败，只由先前已验的O31完整原DAT ZIP得到独立数据，不追认旧失败。TW1图片来源和社区混合2.5地图属于两个来源，之前的整前缀证据可支持共用图块原字节，但不证明同一官方运行服。公开专项6项元数据/资格负例本地PASS，CI须实际后验。Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null；仍**MAP/SCENE SOURCE_BOUNDED_PARTIAL**。

**最高 NEXT MAP-SCENE-MODULE-03**：优先寻找12个缺图号同源有资格原字节及98同名不同MAP的真实两侧地图原件；缺件保留来源止点，不借相邻图号猜补或加引擎、任务、体验优化。当前原可操作历史世界依然未进入，CURRENT旧历史继续保留。


### 2026-11-03 — MAP-SCENE-MODULE-03：98组双目录原地图实字节差异及12缺图号来源分级

[MAP03逐原件差异与缺图边界](continuity/STONEAGE-MAP-SCENE-MODULE-03-98-SOURCE-MAPS-AND-12-LATE-INDEX-20261103.md)、[完整无原地图正文公开派生索引](../research/recovered/STONEAGE-MAP-SCENE-MODULE-03-98-ORIGINAL-MAP-SOURCE-AND-12-INDEX-R1.json)：私人原社区混合2.5 RAR完整SHA再核，MAP01已知98双目录差异的**196原 MAP 文件**本轮实际全部真读，长度/CRC/完整SHA与MAP01逐一一致。95组同尺寸 MAP 的505769对位格中6212个原数值不同；512、5376、59904三组两侧原宽高不同。按双端SHA成对去重为**94独立内容差异**；重复别名256/2816/29952、512/5376、60102/60103仍全部保留，不能当6个不相干历史版本。

1000.DAT全源字节重读确认MAP02的12个未见于TW1 ADRN图号共出现14次、只在图形平面1的x85–90/y85–89集中区域。原RAR内adrn_15.bin本轮直接解包因RAR过滤器不支持而失败，未当成功；另已保存SCENE03的完整同名原索引18765120B按真实RAR声明大小及CRC核同，再按234564个原记录扫描：**11个图号各有一条后期源索引**且所有索引及候选REAL偏移在TW1正式保存资源范围外，**22413仍无后期同样索引**；后期real_15.bin全像素不可读，本批新增这12图的实际原像素=0，不能宣传已复原12图。私有196原文件/全文来源及代码打包ZIP333310B，已存个人Library并原样回读SHA/CRC；公开无商美术/原MAP正文，8项本地派生证据/负例通过；GitHub Actions仅待实际后验。

MAP/SCENE维持**SOURCE_BOUNDED_PARTIAL**，历史 CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c` 不改。保持Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null。**最高NEXT MAP-SCENE-MODULE-04**：按模块原则复用MAP01已真读全量源，批量计算真正可读取原 DAT 地图格及与已保管台湾1.0原图索引的来源覆盖；超出来源/解压能力必须明确止点，然后才按模块顺序转物品。严禁凭编号猜像素、历史同服、原生碰撞或玩法改善。


### 2026-11-03 — MAP-SCENE-MODULE-04：955份原DAT与4166个真正原RD图块来源批量联接

[MAP04原实物和不确定边界](continuity/STONEAGE-MAP-SCENE-MODULE-04-955-DAT-REAL-RD-PIXEL-BATCH-20261103.md)及[955原DAT×4166原RD源限定索引](../research/recovered/STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json)：已保存社区混合2.5 RAR原DAT文件971份真实取出并全部与MAP01原CRC/SHA核同，其中955份具有标准8+6×格三原平面结构、2852551原格；13原零字节和3份二字节BGM文件不计为完整地图。候选两图形平面3082072次非零引用共5291不同图号，已认证TW1零售ADRN唯一对应4166且全部从原REAL实际RD索引像素解码成功，像素SHA去重4063；1125个无TW1索引仅85后期索引唯一、2后期索引多重、1038尚无任何两保存索引匹配，后期REAL仍未解码。相对MAP02新观察范围含3402原RD图号；旧780图中764重叠项RD、RGBA、PNG哈希一致，16以前有证但本次DAT没有引用的旧RD继续保留。私人4166 PNG候选及可搜图集 35673334B/SHA e9c43222797c7ebcddfcb1ccab6dbeba205b972bbbff4e1f29c14b3ece320d37 已保存Library、回读全SHA/4169成员CRC成功。源图片和原DAT/REAL不公开。MAP01旧63次失败与CURRENT原blob c89e0e33537990aa2132b47c40fef49a985a935c继续原样保留，Stage A 7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、overall_percent=null，地图SOURCE_BOUNDED_PARTIAL。最高NEXT MAP-SCENE-MODULE-05：只在实际已有原图、原DAT、历史场景拼接材料上有限做场景原图组合与可见覆盖，按真实来源留原生层序/碰撞/同服未知；受限止点后转物品装备商店模块，不扩新引擎或优化体验。
