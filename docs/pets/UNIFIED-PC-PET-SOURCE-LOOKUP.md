# 经典 PC 宠物统一来源查询（R1）

一个只读入口访问固定的 Git 来源对象。每项返回可追溯的来源位置、证据等级和独立版本。

```bash
python3 tools/stoneage_pet_source_lookup.py --summary
python3 tools/stoneage_pet_source_lookup.py --query 蒙奇 --exact --full
python3 tools/stoneage_pet_source_lookup.py --query 雷帝斯洛 --variants
python3 tools/stoneage_pet_source_lookup.py --query PET-000001 --exact --source tw10 --full
python3 tools/stoneage_pet_source_lookup.py --query 101501 --exact --source tw85_spr --full
python3 tools/stoneage_pet_source_lookup.py --visual-graphic 100400 --full
python3 tools/stoneage_pet_source_lookup.py --verify
```

## 直接查询的资料

|来源ID|记录单位|内容|
|---|---|---|
|tw10|124份原客户端名／永久研究编号|原图、动作、2001年投稿、2003年大陆目录、后期模板属性|
|cn50|305个保存相簿名槽|图组、头像哈希、2003网页及跨版图像链接|
|tw85_grid|4程序的1889个具名相簿名槽|本地原名、头像别名、原程序区分|
|tw85_spr|550图号的1696个具名程序路径|物理图号、冲突及原帧引用|
|tw75|467个声称7.5宠物模板|元素、技能槽、条件初值成长、后期遇敌来源|
|sina2003 / fusion2003|237网页行／41面板|同名链接、同期样本，不当官服主档|
|hf18 至 hf30_31|分年度来源位置|取得、任务、赠宠、面板、地区、晚期对象角色|

`--full`返回固定源行和关联源行；`--variants`仅使用明确字符映射，不推断同宠；`--source`隔离来源。数字键只精确匹配，不能当跨版本统一ID。所有源定位和独立计数都可重放。[机器清单](../../research/pets/PET-HIGH-FIRST-32-UNIFIED-SOURCE-LOOKUP-MANIFEST-R1.json)。

## 仍不能填入正式历史字段

后期运营授权、同服原生PET ID、真实初值及成长算法、原生技能函数、获取/发行与未取得的晚期客户端，不能由此索引推定。TW1 124个研究档历史全字段认证仍为0。真实物种总数未知。


R34新增固定来源 `hf34`（16个同期字段见闻，原源清单扩为26个对象），[见逐宠补证](CN-2011-2012-PERIOD-FIELD-WITNESSES.md)。


R35新增 `hf35`，27固定源对象；[2013年14来源位置](CN-2013-PERIOD-FIELD-WITNESSES.md)，其中一条仅对话候选，不是物种。


R36新增 `hf36` 固定来源（共28源），35早期字段参考可查询，13未认证晚期服务参考仅存源附件，不纳入查询或队列。[具体字段](PC-2015-2018-FIELD-REFERENCES.md)。

R37将原零售相册、2001华义托管玩家投稿和后期数值参照接到现有124份台湾1.0研究档。普通查询显示属性对照及取得摘要，带 `--full` 可追到投稿序号、页面存档、后期模板与原客户端编译行。[证据和差异](../continuity/STONEAGE-PET-HIGH-FIRST-37-TW10-FIELD-REFERENCES-20261124.md)。

R38在 `PET-000004`、`PET-000017`、`PET-000021` 下增加日本实读照片和保存版服务端案例。使用 `--source tw10 --full` 查看关联来源 `hf38`。[原件核对](../continuity/STONEAGE-PET-HIGH-FIRST-38-THREE-PC-FIELD-CASES-20261124.md)。

R39在现有五个台湾1.0档号下增加 `hf39` 链接：区分同图号非宠模板、后期同一Git blob和2001–2003网页字段。原查询位置和补缺位置不增加；[逐档来源与NEXT](../continuity/STONEAGE-PET-HIGH-FIRST-39-FIVE-PC-FIELD-CASES-20261124.md)。

R40五个既有档案增加 `hf40` 获取链：实际原保存混合2.5 14成员与后期固定源码、原地图数据比较。[取证与续接](../continuity/STONEAGE-PET-HIGH-FIRST-40-PC-ACQUISITION-20261124.md)。

R41新增57个既有档案的保存混合2.5模板/取得候选链接；`--full`可追145模板及3个任务奖励指令，不增加查询位置。[来源及边界](../continuity/STONEAGE-PET-HIGH-FIRST-41-PC-ACQUISITION-20261124.md)。

R42增36个标称7.5模板行精确指纹奖励链接，33个TW1图号候选（31同名、2异名），26原成员实读、36个Lv1双标记实例。39固定源对象；`--source tw75 --query 瑪蕾菲雅 --exact --full` 可追奖励脚本，原正式发行未证。[详档](../continuity/STONEAGE-PET-HIGH-FIRST-42-PC-REWARD-INSTANCE-INDEX-20261124.md)。

R43补17个既有奖励记录与5交换模板来源，40个固定源对象，三个道具原行指纹、条件和列表重复数均可追溯。SOT/JOT同部署窗口执行未证，不当官方概率。[详档](../continuity/STONEAGE-PET-HIGH-FIRST-43-PC-EXCHANGE-SEMANTICS-20261124.md)。


R44追加四原窗口控制记录（41个固定源对象），现有奖励候选可用 `--full` 追19宠物槽与40道具槽及条件；15不同实例，未新增查询位置，不宣称实际发奖。[原件](../continuity/STONEAGE-PET-HIGH-FIRST-44-PC-WINDOW-REWARD-20261124.md)。


R45在467条标称7.5既有记录显示与保存混合2.5的来源比对；123条精确行有正权重路径，118条双宠标记、94条含Lv1。普通查询显示对应楼层、旧地图名候选和各级统计；`--full`包含逐路线楼层/坐标、实例等级、双标记和归一化事件字段。新增2个固定源对象（共43），不新增物种或查询位置；另6条保存版非精确同源模板保留在派生原档，不能借TW75名字合并。[PET45](../continuity/STONEAGE-PET-HIGH-FIRST-45-PC-BULK-ACQUISITION-20261124.md)。


R46在349个无双标记路径的标称7.5档案添加取得参考分类、主备表比较、缺件状态及原证指针（44固定源对象）。13原任务奖励、234其他来源参考、102本批缺合格参考。无新增物种或查询位置；`--full`可追原源记录。[PET46](../continuity/STONEAGE-PET-HIGH-FIRST-46-PC-ACQUISITION-GAP-20261124.md)。


R52 对位置67、144、171、208增加 `hf52` 高版本原图鉴与普通任务／VIP异档对照链接，不增查询位置，严格取得残余67不减。[PET52](../continuity/STONEAGE-PET-HIGH-FIRST-52-NAMED-VISUAL-ACQUISITION-VARIANTS-20261124.md)。


R53 追加位置68、75、144、208的 `hf53` 取得参考，区分2001–2003华义商业红暴、2012胜思熊猫兑换及金蛙未具名活动。严格缺口67不减。[PET53](../continuity/STONEAGE-PET-HIGH-FIRST-53-COMMERCIAL-HONOR-REWARD-REFERENCES-20261124.md)。


R54 追加位置387、453、454的 `hf54` 对象分类及原函数/后续GetEgg分层证据，不能认定孵化结果或新物种。严格缺口67。[PET54](../continuity/STONEAGE-PET-HIGH-FIRST-54-EGG-ROLE-AND-FUNCTION-20261124.md)。


R56 追加十个现有TW75模板位置的角色及原NPC候选指针（55固定源对象），14条原扫描候选及5个后期角色可追溯；12条既有训练奖励、2条未绑定的暂不用VIP数值候选，不增加查询位置或关闭严格缺口。[PET56](../continuity/STONEAGE-PET-HIGH-FIRST-56-SPECIAL-ROLE-PREFLIGHT-20261124.md)。

R57 在 67 个余缺位置添加高版本保存图组、原帧绑定与相册候选。[PET57](../continuity/STONEAGE-PET-HIGH-FIRST-57-RESIDUAL-VISUAL-COVERAGE-20261124.md)。

R58 为其中十个缺同名相册的位置添加角色，另从八个既有同图模板提供反向链接。用 `--query 萊比 --source tw75 --exact --full` 查看莱比角色和同图的乌力莱德模板。[PET58](../continuity/STONEAGE-PET-HIGH-FIRST-58-PC-TASK-ROLE-CROSSWALK-20261125.md)。

R59 的独立像素凭证复算补充了 66 个图组的使用范围。39 组有同保存包的动作取样，7 组在另一保存包有精确 SPR/RD 取样，20 组尚缺所比对凭证的完整取样。[PET59](../continuity/STONEAGE-PET-HIGH-FIRST-59-RESIDUAL-PIXEL-RECEIPTS-20261125.md)。

R60 从同一台湾保存 8.5 原包补齐余下 20 组的完整动作取样，123 个图块均经两套解码器核对。用 `--query 古瓜 --source tw75 --exact --full` 可查两份模板各自的 `hf60` 动作链接。[PET60](../continuity/STONEAGE-PET-HIGH-FIRST-60-TW85-REMAINING-PIXELS-20261125.md)。

R61 为 67 个严格取得余缺的现有模板添加同档技能核查。64 条全行匹配，135 个正数槽可追至原配置的六条定义。用 `--query 烏力王 --source tw75 --exact --full` 查看有证模板的 `hf61` 技能链接。[PET61](../continuity/STONEAGE-PET-HIGH-FIRST-61-RESIDUAL-SKILL-DEFINITIONS-20261125.md)。


R74 接入保存版 TW8.5 的 1,889 个具名程序位置，保留同别名下全部物理肖像候选、原动作覆盖等级及两条未解的非正尺寸记录。`--full` 可追原行、肖像和两版色板文件凭证。标称 TW7.5 按原图号查看候选，台湾 1.0 和大陆 5.0 依图号及完整 SPR 散列查看跨版本对应。用 `--visual-graphic` 可查原 TW8.5 物理图组，包括相册无具名路由的 `100400`，图号与物理组号均属于原资源命名空间。官服身份、实际调色及原客户端渲染仍待证。[取证与续接](../continuity/STONEAGE-PET-HIGH-FIRST-74-UNIFIED-VISUAL-20261125.md)

R76 在标称台湾 7.5 的 467 个现有位置增加保存档主表核查。可查同指纹的出生参数、配置技能名和已有取得配置，也可用模板编号检索同号异行的基础值差异。初值区间与成长增量仍是后期 PC 算法的条件计算，官服实际出生技能和取得待证。[字段核查](../continuity/STONEAGE-PET-HIGH-FIRST-76-SELECTED-MASTER-FIELDS-20261126.md)

```sh
python tools/stoneage_pet_source_lookup.py --source tw75 --query 烏力 --exact --full
python tools/stoneage_pet_source_lookup.py --source tw75 --query 901 --exact --full
```


R88 将21处原保存版技能学习配置按技能ID与主表定义原行SHA-256精确连接到440个已匹配模板的904个正技能槽。带 `--full` 可追原参数路径、楼层、倍率字面及配置列表；这不证明特定宠物可学习或官方运行。[取证与边界](../continuity/STONEAGE-PET-HIGH-FIRST-88-SAVED-SKILLSHOP-LINKS-20261126.md)


R89 将保存版无精确学习点的19种技能、37个技能槽接入同期独立参考；10种技能有同期效果/学习/具名宠参考，另1种仅同名道具上下文，8种仍无合格同期参考。原字段不改，保留地区与数值差异。[取证](../continuity/STONEAGE-PET-HIGH-FIRST-89-SPECIAL-SKILL-PERIOD-REFERENCES-20261126.md)


R90 对2003年41张融合宠一级面板执行同一组出生随机输入的四项联合回放；41张全部条件相容（40个原保存整行匹配、1个异行），并连接后期融合排除表的8个原配置技能槽。修复R89原定义索引误用，逐槽校验ID及原行散列。非原服融合算法或首发证明。[取证](../continuity/STONEAGE-PET-HIGH-FIRST-90-FUSION-PANEL-JOINT-WITNESSES-20261126.md)


R91 对六个同号异基础值模板的29组初末面板，提供53条可回放的条件成长路径（26组双主档均可构造、1组仅找到标称档路径、2组未找到；未找到不等于不可能）。保持原资料等级、原初始等级假设及两条公开算术冲突。没有认证官服原值。[取证](../continuity/STONEAGE-PET-HIGH-FIRST-91-ENDPOINT-GROWTH-WITNESSES-20261126.md)


R92 为标称7.5的255个主档位置挂接2003-04-07同期大陆名录候选，逐条核对保留的5.0编译名、原SPR图号、有限繁简字映射与元素。保留异名、元素冲突及转生标签，不以名录日期充当首次发行日期。[取证](../continuity/STONEAGE-PET-HIGH-FIRST-92-DATED-CATALOGUE-CROSSWALK-20261126.md)


R93 挂接2002、2003、2013三个经典PC同期来源的明确系别标签，38项记载、31个主档位置、32条关联；保留元素冲突、同名多模板和8项未匹配名称。原文分类层级不强制统一，非官服原生系别字段。[取证](../continuity/STONEAGE-PET-HIGH-FIRST-93-DATED-FAMILY-CLAIMS-20261126.md)


R94 为R93未匹配主档的8个名称追加独立资料站详情参考条目，并连接5个现有原8.5相册位置及1个大陆同期记载。资料站区间及2006年兽回忆的元素冲突分开保留，不作为官服主档。新增8个查询来源条目不增加认证物种或原资源位置。[取证](../continuity/STONEAGE-PET-HIGH-FIRST-94-LATE-FAMILY-CATALOGUE-REFERENCES-20261126.md)


## 大陆2012认证原包名称查询（候选）

新增独立来源 `cn85_original`：8.5免费版及2.5收费版两个原程序的相同编译表，521具名位置、513不同字面。原始物理位置、槽、脸号以 `ordinal:`、`slot:`、`face:` 前缀检索，避免混用图号。保留49个未解析记录长度间隔及57个已知空位，不把它们当宠物。既有大陆5.0的305档可查看 `cn85_compiled_crosswalk`；304四字段相同，艾柏瑞/艾比斯保留异位、异名。仅客户端编译字段，未证原生选择器、原图、实际发行或服务端属性。历史3015位置缺件队列暂不变，PET124原件处理验收后再协调增量。

```sh
python tools/stoneage_pet_source_lookup.py --source cn85_original --query 艾柏瑞 --exact --full
python tools/stoneage_pet_source_lookup.py --source cn85_original --query ordinal:314 --exact --full
```


## 整体复审后视觉引用（2026-11-26）

98个固定派生来源对象，5924查询位置不变；当前缺件队列3563来源位置。原入口不变：
```bash
python3 tools/stoneage_pet_source_lookup.py --query 烏力 --source tw75 --exact --full
python3 tools/stoneage_pet_source_lookup.py --query 雷帝斯洛 --source tw75 --exact --full
python3 tools/stoneage_pet_source_lookup.py --query ordinal:228 --source cn85_original --exact --full
python3 tools/stoneage_pet_source_lookup.py --query ordinal:375 --source cn85_original --exact --full
PYTHONPATH=. python3 tools/stoneage_pet_final_review_matrix.py
```
`review_portrait_reference` 467条（424同名同图号唯一参考）；`review_portrait_conflict` 43条保留名称/图号冲突；`review_motion_reference` 131条分别引用61 CN50和70 TW85的原RD与完整SPR段散列证据。带 --full 展开固定的完整来源行。不得将候选作为同版本原头像、原生动作选择器或官服真实发宠；没有新增正式物种认证。七维复审脚本生成派生 JSON 矩阵，尚不表示模块结项。


## PET16 历史分源目录（独立查询模式）
同一个查询命令的 `--legacy-pet16` 模式回到固定旧目录2,792条来源行，保留七个命名空间。与当前5,924位置有交叉，不能相加计物种。社区配置仅技术参考、原SPR不证明物种，日/大陆运营图鉴不证明实际发宠；大陆6个未知名保留。
```sh
python tools/stoneage_pet_source_lookup.py --legacy-pet16 --summary
python tools/stoneage_pet_source_lookup.py --legacy-pet16 --source jp_official_web --query ウーリ --exact --full
python tools/stoneage_pet_source_lookup.py --legacy-pet16 --source cn_official_web --query web_ordinal:1 --exact --full
python tools/stoneage_pet_source_lookup.py --legacy-pet16 --source later2016_templates --query COMMUNITY2016:1 --exact --full
python tools/stoneage_pet_source_lookup.py --legacy-pet16 --source tw10_visual --query graphic:100015 --exact --full
```
[七维验收与历史目录补交](../continuity/STONEAGE-PET16-LEDGER-RECONCILE-20261126.md)。


PET16 图像与缺技能凭证：旧日本网页23个已获图像位置（含父记录）、大陆网页7个已获图像位置，保留失败和未知名称；后期2016选中技能表102缺槽、混合备表12缺槽，可在旧查询的 `supplemental_evidence` 中按原位置追溯。没有新增原生SPR或官服发行认证。[完整七维矩阵](../../research/pets/PET-FINAL-REVIEW-MATRIX-R1.json)。


## 历史文献查询（独立于现行来源位置与PET16）
`--documentary` 直接检索已归档委托/栖息地、技能教学及矛盾、初期玩家取得记载、发行事件和未证线索。原名称的候选链接仅表示字面匹配；不推断同版身份、实际遭遇或原技能效果，不把140文献位置叠加为宠物数量。带 `--full` 展开源证据及版本限定。
```sh
python tools/stoneage_pet_source_lookup.py --documentary --summary
python tools/stoneage_pet_source_lookup.py --documentary --source cn20_commission --query 乌力 --exact --full
python tools/stoneage_pet_source_lookup.py --documentary --source cn2004_trainers --query 猛毒攻击 --exact --full
python tools/stoneage_pet_source_lookup.py --documentary --source pet25_release --query 艾迪希洛 --exact --full
```
[材料对账与限制](../continuity/STONEAGE-PET-HISTORICAL-DOCUMENTARY-20261126.md)。


## 年份／地区／版本历史查阅
`--history` 复用28份固定年度源报告、156个实际地区审查块、12个明确版本日期主张及9个既有PC发行事件子集。1999—2010未单列港澳；2011起六区；2026截至11月20日仍OPEN。原名称及日期类型、来源路径与Git blob／指针可追溯。版本筛选仅命中明确索引标签，非同部署身份或全版本检索；年区报告是上下文。无匹配不等于无宠物，9事件不是全史发行数。带 `--full` 展开匹配原记录（可能含历史排除范围说明，不纳入活跃宠物）。
```sh
python tools/stoneage_pet_source_lookup.py --history --summary
python tools/stoneage_pet_source_lookup.py --history --year 2002 --region CN --full
python tools/stoneage_pet_source_lookup.py --history --year 2026 --region TW --full
python tools/stoneage_pet_source_lookup.py --history --version 2.0
python tools/stoneage_pet_source_lookup.py --history --query ハクエン --exact --full
```
[年区证据接入说明](../continuity/STONEAGE-PET-YEAR-REGION-ACCESS-20261126.md)。
