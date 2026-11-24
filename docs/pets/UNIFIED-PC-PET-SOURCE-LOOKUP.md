# 经典 PC 宠物统一来源查询（R1）

一个只读入口访问25个固定Git源对象。**每项返回来源位置，不合并成物种，也不提升为官方发行。** 同名、多地区、多程序和不同时期各自保留；后期声称主档计算值与早期官方数值分开。没有引入手游、双端或私服物种。

```bash
python3 tools/stoneage_pet_source_lookup.py --summary
python3 tools/stoneage_pet_source_lookup.py --query 蒙奇 --exact --full
python3 tools/stoneage_pet_source_lookup.py --query 雷帝斯洛 --variants
python3 tools/stoneage_pet_source_lookup.py --query PET-000001 --exact --source tw10
python3 tools/stoneage_pet_source_lookup.py --query 101501 --exact --source tw85_spr --full
python3 tools/stoneage_pet_source_lookup.py --verify
```

## 直接查询的资料

|来源ID|记录单位|内容|
|---|---|---|
|tw10|124份原客户端名／永久研究编号|原图、动作及缺口|
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
