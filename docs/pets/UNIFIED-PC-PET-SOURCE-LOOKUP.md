# 经典 PC 宠物统一来源查询（R1）

一个只读入口访问36个固定Git源对象。每项返回可追溯的来源位置、证据等级和独立版本。

```bash
python3 tools/stoneage_pet_source_lookup.py --summary
python3 tools/stoneage_pet_source_lookup.py --query 蒙奇 --exact --full
python3 tools/stoneage_pet_source_lookup.py --query 雷帝斯洛 --variants
python3 tools/stoneage_pet_source_lookup.py --query PET-000001 --exact --source tw10 --full
python3 tools/stoneage_pet_source_lookup.py --query 101501 --exact --source tw85_spr --full
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
