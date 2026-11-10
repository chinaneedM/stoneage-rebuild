# INTEGRATION50｜原房服务参数关系正式发表与主线验收（2026-11-10）

## 主线基线、保存边界和实际变更

按 [连续性协议](../PROJECT-CONTINUITY-PROTOCOL-R1.md) 从远端 main **HEAD `9657ca20cde60445de96f8e56ae7340963cb2414` / tree `dcd185b8ce483fa75757d4209b0d3ee7743ea6aa`** 出发，读取远端分支、最新提交、Actions、README、连续性协议及生效设计/来源/路线/模块队列、INTEGRATION49原件与正式验收。零开放PR。

远端Git树中 `docs/CURRENT-STATE.md` 为**2,709,173字节**，Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`。GitHub文件接口返回空正文、原blob读取接口出错、raw接口因大文件受限；本轮**没有成功取得其完整正文**，不能把空响应当空文件，亦不能谎称全历史逐字节重读。本轮没有改动该文件，后验合并主线树重新核定仍为**同一blob和字节数**。据协议§14另加 `docs/continuity/` 文件、README指针而不做后缀替换或旧历史复写。此读取限制仍需将来有可用全blob读取能力时恢复核验。

## 来源实物和真正新增结果

- 原私人CHAR01社区mixed25 NPC ZIP **995,176B / SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`** 实际整包SHA复核、全部**2,205成员CRC**成功；44条I49 CREATE对应43个唯一原arg完整文件SHA均重新验证，CP950字段严格读取，原版权资料不公开。
- 44条原配置：**32 ItemShop／6 PetShop／6 PetSkillShop**；其中29项原ItemList与既存[ITEM01原参数目录](../../research/recovered/STONEAGE-ITEM-EQUIPMENT-SHOP-MODULE-01-224-SOURCE-ITEMLISTS-191-CREATE-REFERENCES-R1.json)按文件路径与SHA双钥命中；3项参数没有ItemList，不杜撰库存。原类别字段原值/空字面/缺字段严格分列；六宠物菜单费率和池配置、六技能菜单共50项出现位置/15个不同数字ID有源可查，原重复CREATE保留。
- 这批**新增原DAT、新原商业NPC文件、新解码RD均为0**；新增的是之前分开的房间→具体原参数→现有ItemList/宠物技能数字的可重放关系。原版原生买卖/养宠/教学、官方同部署、真实售价和原客户端交互均未证。

细节见[本轮来源和止点](STONEAGE-INTEGRATION50-28-ROOM-SHOP-PET-MENUS-20261110.md)、[纯派生JSON](../../research/recovered/STONEAGE-INTEGRATION50-28-ROOM-SHOP-PET-ARGUMENT-BRIDGE-R1.json)。公开原来源旧blob：I49 `673fd0ebd71a909a5678d919f706bab7a8e5e7cc`；ITEM01 `3bde3b7df43725f28cdac355823667a0ba87e9b1`。本轮新Git blob：JSON `da792e33e97e3fd0c52f24adf7fbc22f9b5b2421`、反例回归 `2e984863f4f70c4779f2acd9596ad902840fd30c`、来源说明 `cdfdb8dc92d63fa87d0348805c70f08559c032d0`；旧CURRENT原blob不变。

## 实际远端发表链和回归

- 起始main基础上新建候选分支 `agent/integration50-room-shop-pet-args-20261110`，HEAD **`8e7878677a0114d68b34678795e2ce66c9f82317`**，tree **`cf10900001bb342fa2961f4689033ceb1488a0ff`**。与原主线比较ahead=5/behind=0，只有五个公开路径：README仅末尾追加；一份原来源说明、一份纯派生JSON、一份测试、一份专项workflow；无私人原DAT/RD/PNG/HTML/原NPC文本或ZIP。
- 候选push的 **27/27** 工作流全部completed/success（其中本包专项 [42838474247](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42838474247) 成功），[PR #318](https://github.com/chinaneedM/stoneage-rebuild/pull/318)的 **19/19** 工作流全部completed/success，本包专项 [42838751559](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42838751559) 成功。所有成功之后才核PR mergeable=true及main仍为起始HEAD。
- PR #318以squash成功合并，内容主线 HEAD **`7320d1a20a2ed5067ee306d2aaa68d9e0291ad8d`**，tree **`cf10900001bb342fa2961f4689033ceb1488a0ff`** 与候选完全相同。合并后main push **27/27** Actions真正completed/success。本包专项 [42838919981](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42838919981)，job **129908516535**，原日志明确 `Ran 10 tests in 0.004s`、`OK`，没有skip/fail。公开CI读的是Git公开派生证据，**不是**私人原件或原native游戏。
- 此验收说明本身在全部通过后加法提交，**不把验收说明提交HEAD自身任何未运行的CI追认为通过**。完整前次失败历史/旧证据均不覆盖。

## 完成本包后的实际NEXT

INTEGRATION50来源限定封包。按最新模块队列选择**不同于这28间既存房间**、能真实读取新原DAT/NPC/物品/宠物/图像且可以形成另一条玩家可见内容关联的下一批；无实物则保持OPEN并换域。别把同室功能字段反复展开成工具、官方原始技能树或已可玩场景。

Stage A **7 PARTIAL + 2 OPEN**；Stage B/wiki **GATED**；R79 **PAUSED_NON_BLOCKING**；overall_percent=null，任何旧Stage A结论均未变。
