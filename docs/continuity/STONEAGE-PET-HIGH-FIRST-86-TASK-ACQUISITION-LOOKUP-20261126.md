# PET-HIGH-FIRST-86｜迪加环岛奖励、任务宠分轨与统一查询（候选）

2026-11-26；起点main `d13b7a10548771b86d80859659a847e6fecf8df1` / tree `4ad2643050395feedca25cc407460eecb9a2851b`。PET85 PR #696候选3/3 Actions通过并合并。历史CURRENT blob c89e0e33537990aa2132b47c40fef49a985a935c / 2,709,173 B 不改。

## 取得字段补证

模板784迪加（图100879，水8火2）：[2003-04-07新浪玩家属性稿](https://games.sina.com.cn/zhqu/sta/cwzl/chongwu03.shtml)与[2003-06-03 EOT E路线攻略](https://games.sina.com.cn/zhqu/sta/article/2003-06-03/10610.shtml)交叉连接，后者记100级限制、完成金飞任务、可重复、12检查站、尼克斯水城终点(61,96)，从五个宠物候选随机给一个，含迪加；[2003-02-17署名稿](https://news.17173.com/z/stoneage/content/2003-2-17/n910_826302.html)亦列环岛奖宠。概率未知；PET49的2002异属性冲突保留；两属性/取得文档不能证同服。未取得原HTML字节。

## 任务模板

[2002-11-06同期玩家攻略](https://news.17173.com/z/stoneage/content/2002-11-6/n782_698433.html?_platform=PC)记布洛多多20级交付、练至50级交回换号角；2003点评称其学名阿米朵，而[EOT F路线](https://games.sina.com.cn/zhqu/sta/article/2003-06-03/10614.shtml)奖池列阿米朵。保存主表1042/813同图100908、元素、base，INITNUM分别26/27，不共享永久获取，不认证任务实际ID。动物园拉斯基交还、古瓜两同名模板未定位、普通蛋与美拉蛋同图而基础参数不同，均保留任务/状态上下文，不关闭余缺。贝沃特/贝恩斯仍仅名+包月，奇肯两名同期泪之海仍缺比例。排除私服、手游及现代复刻线索。

## 统一查询

将PET81–86六批记录接入原 `tools/stoneage_pet_source_lookup.py` 的TW75原位置及原manifest，固定各Git blob；不是另建目录。保留冲突/任务上下文、原记录出处。增加67位置互斥分区、主表散列、元素、逐项链接、否定官服资格检查。工具层实际复算33个不重复位置及34余缺；Python完整回放由现有PET32 CI验收，尚未声称通过。查询示例：`python3 tools/stoneage_pet_source_lookup.py --query 784 --source tw75 --exact --full`。

[机器记录](../../research/pets/PET-HIGH-FIRST-86-TASK-ACQUISITION-BOUNDARIES-R1.json)。累计33/67相容参考，严格67不减，3,015位置不变，原件与官服闭合均0。NEXT：先验收统一查询；剩34若无新原档或精确同期材料，不循环既有空栏，先汇总缺口止点与原PC源可达性，再按PET唯一模块的高版本原始数据优先继续。Stage A 7 PARTIAL+2 OPEN，B/wiki GATED，R79暂停，总体UNKNOWN。
