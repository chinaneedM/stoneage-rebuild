# PET-HIGH-FIRST-88｜原保存宠物技能学习配置与主档连接（候选）

2026-11-26。起点 main `92959f1a500f9165d7b9d5e325943b2243f1f686` / tree `fffe7c1b90a6b2cda02dbbe9aae3f7f6badc20c8`；PET87 PR #698 候选13/13 Actions成功并已合并。历史 CURRENT blob c89e0e33537990aa2132b47c40fef49a985a935c / 2,709,173 B 保留。依 PET87 止点不重复检索取得空栏，转向宠物技能字段。

## 资料与新增可查询关系

复用已验原保存混合2.5的21份技能商店原参数文件凭证（[原派生记录](../../research/recovered/STONEAGE-GAMEPLAY03-ORIGINAL-21-PET-SKILL-SHOP-SOURCE-R1.json)，Git blob 5735ddc1117a8a6fb2f9417327ec242e4fd06192，原件2,117字节，23种技能ID、150次配置，原NPC全包SHA/CRC此前验明）及 [PET76](STONEAGE-PET-HIGH-FIRST-76-SELECTED-MASTER-FIELDS-20261126.md) 440个整行匹配模板的941个正技能槽。不是再下载或重解码原件。以技能ID AND 原主表技能行SHA-256 精确相同作为连接条件，不以技能名相似代替。19种定义满足条件；904槽有商店配置引用，37槽所对应的其余19种定义在这21份配置中无精确引用。440个模板至少有一条（多为攻击/防御），共6,636个去重后的模板—商店位置链接，不是新宠物或习得能力证明。

保留原路径、楼层号、原技能ID次序、倍率字面、原行散列与主备表候选。商店列技能不代表某宠必可学习、实际消费、默认出生技能、全部技能来源或同服官方运行。原倍率1.0/1.1/1.2不推定价格或成功率。特殊技能如落馬術、嗜血技等只记本批无商店引用，不断言不能学习或必为专属。当前3,015缺口位置及严格取得67不变；无新增官服闭合或原件。

统一查询示例：`python3 tools/stoneage_pet_source_lookup.py --query 烏力 --source tw75 --exact --full`。复用既有 manifest，新增固定源及独立回放断言。工具层复算904槽/440模板/19定义/6636关系，完整Python验收以候选CI为准。

NEXT：先验收PET88；随后对仍无原配置学习路径的19种技能优先查真正新可得高版本PC主档、原脚本或具名同期技能资格文献，已有图鉴及取得空栏不循环。若无合格来源则保留有界未知，继续PET其他实质字段。Stage A 7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79暂停，总体UNKNOWN。
