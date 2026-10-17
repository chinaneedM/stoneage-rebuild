# QUEST-NPC-ITEM-BINDING-05：五个伐木候选的NPC参数角色核验

日期：2026-10-17（Asia/Shanghai）。阶段：Stage A，历史资料复原。目标不是开发新游戏或穷举NPC，而是判断五个已独立来源认证的后代物品模板，能否在同一套recovered25 NPC配置中找到**带语法角色**的发放、收回或条件引用。

## 已有确定边界

基础来源固定为 `research/recovered/STONEAGE-QUEST-ITEM-CI-DERIVED-R1.json` 与 `STONEAGE-QUEST-ITEM-ACCEPTANCE-R1.json`。五个候选ID是2465、2478、2481、2484、20197；其中2478採伐許可證与20197伐木許可證即使图像/部分标记相同也不得合并。它们属于recovered25后代模板，而非台湾1.0已经证明的物品身份。

资料包使用原两分卷SHA256（001：`7cb7acdecd56617132e6f284c468158917c91d542cad5b2e7b3c7774fb5630d5`；002：`567e1ec0aeff9ea6a9ada791a339aa8f8bb8ffba83cf762e4b445fc0f1cb16bb`）与合包`d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`；源包仅在Actions临时环境取得并读取，不执行原服务端程序，不提交NPC原文、对白、脚本、地图或其他商业资产。

## 证据链算法和误判禁止

`tools/stoneage_quest_npc_item_binding_probe.py`使用已有`NPCTEMPLATE`与`NPCCREATE`键值块解析和二级参数file/inline读取；重复或不明模板只能记缺口。仅对五个ID检测完整项语法，`12465`、`2465text`等数字片段不能命中。`EventEnd`划分ExChangeMan候选记录，只有该FunctionSet里的`GetItem`/`DelItem`分别列为**发放候选／收回候选**，`EVENT:ITEM=...`或`ITEM!=...`列为**条件候选**，绝非成功执行证书。

后代固定源码里已证明部分`Action_RunDoEventAction`的FunctionSet仅以`AddItem`**候选**记录，不推定必然可达。`ItemShop`只可列目录存在，不是任务奖励；`FREE`与任意字段里的纯数字不能用作发奖。其他未知FunctionSet里的GetItem/DelItem/AddItem一律列**未资格化结构字段**，直到具体源代码语义核实为止。

所有来源的原始字节保留在CI临时环境。只产出项目内五个已公开的后代ID、语义分组、聚合出现次数、匿名哈希计数、缺参数/歧义覆盖和**不晋级**布尔门。限制最多250分组；不保存NPC名称、模板名、坐标、原对话、原始参数值和整个文件。后代源码类比不等于台湾1.0原始商业服事务，更不能假定真实任务分支、奖励成功、撤回执行或登录持久性。

## 验收路径和停止条件

```bash
python -m unittest tests.test_stoneage_quest_npc_item_binding_probe -v
python -m tools.stoneage_quest_npc_item_binding_probe --npc-dir /temporary/SA2.5服務端/gmsv/data/npc --output /tmp/quest-npc-item-derived.json
```

CI `.github/workflows/validate-stoneage-quest-npc-item-binding.yml`是唯一对原始包作本轮新取得声明的入口，需先全部两分卷、合包哈希检查，再读取固定目录；合成测试成功不等于NPC源抽取成功。Actions产出短期`quest-npc-item-derived`，取得成功后必须独立核对来源HEAD/tree、run/job、artifact ZIP/raw JSON哈希，并将合法派生报告永久归档，记录验收链。未通过不得宣称成功。

若有限扫描没有显式绑定，按`UNKNOWN`或“该保存包未发现有资格绑定”关闭这一有界问题，而不是编造原始NPC交付关系、泛扫所有攻略或开启R79。无论结果如何，九系统维持7 PARTIAL+2 OPEN，Stage A未终验，Stage B GATED，新石器设计不得据此启动。
## 实际认证来源结果与边界（2026-10-17）

第一次独立源CI（Action38996169729）9项语法用例有1项失败，原因是ItemShop的FREE与普通字段范围误归类；该失败不可抹去。严格限定ItemShop物品目录字段后的源提交`c4474916add4ed3d4e867ba13d14c47e76dca86b`、tree`74e1aaa958d5776894245b923a3475919c51d39b`获得[Action38996224450](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/38996224450) / job117289269018 **SUCCESS**：9项合成语法试验、两分卷与合包hash以及实际NPC参数读取成功。原服务端程序未执行。

对后代`NPCCREATE`引用的有界检查：总计4,985条；模板歧义30、缺参数文件15；参数来源文件1,758、inline 3,182。只在`ExChangeMan`中取得49次具有规则字段语法的引用，汇总如下；它们是后代技术候选，**绝非已执行的伐木任务事务**。

| 后代模板ID | GetItem发放候选 | DelItem收回候选 | EVENT ITEM条件候选 |
|---|---:|---:|---:|
| 2465 交差斧 | 1 | 2 | 4 |
| 2478 採伐許可證 | 1 | 16 | 20 |
| 2481 杉的手環 | 1 | 0 | 0 |
| 2484 折斷的斧頭 | 2 | 1 | 1 |
| 20197 伐木許可證 | 0 | 0 | 0 |

这10个类型分组总和49；20197在本次限定语法与可解析NPC参数中**没有已资格化命中**，不能进一步说游戏不存在该许可。对2478既有发放又有收回及条件引用，也不能靠分布次数推断这些动作在同一NPC、相同事件分支或真实玩家执行链中。缺失的15份参数及30条歧义模板依旧是覆盖限制。

永久来源交付由`research/recovered/STONEAGE-QUEST-NPC-ITEM-CI-DERIVED-R1.json`记录，4546字节、SHA256 `901e835c921557da9dae7380b70aac0522fe4ff251c888de4289c91fb0da34f6`、Git blob `7d771b2aa4f39646879659303f4926045ae730cc`；独立下载的artifact12087620874 ZIP960字节、SHA256 `3c4774d955c155af0d426f419ce672dba0d2321caa81a27232d4ab2353225cd2`。`STONEAGE-QUEST-NPC-ITEM-ACCEPTANCE-R1.json`记录完整源HEAD/tree/Action/job和ZIP/raw/blob保管链。之后的持续CI只重放这个永久派生JSON和防晋级用例；不把归档重放说成再次取得原始NPC字节。

**有限任务交付**：完成后代五物品的“物品表ID—NPC字段角色”来源合格对照。未确认具体伐木任务真实函数调用、相同事件分支依赖、NPC身份或台湾v1.0原始ID；不能提交现代奖励规则作为历史结论。

**下一项优先级 QUEST-NPC-FLOW-LINK-06（有界可选）**：复用本次已认证来源，仅确认2478/2484/2465/2481是否在**同一个ExChangeMan EventEnd事件记录**中具有确切GetItem/DelItem/条件的共现结构，再判断是否形成局部后代任务模型；至多检查已命中记录、不泛扫全世界。无法取得同记录证明则止于UNKNOWN。这个后代模式仍不能补写台湾1.0原始NPC/任务/服端事务。Stage A仍7 PARTIAL+2 OPEN，Stage B GATED，R79继续暂停。
