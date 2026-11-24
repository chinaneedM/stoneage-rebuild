# 经典 PC 宠物统一来源查询（R1）

一个只读入口访问32个固定Git源对象。每项返回可追溯的来源位置、证据等级和独立版本。

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
