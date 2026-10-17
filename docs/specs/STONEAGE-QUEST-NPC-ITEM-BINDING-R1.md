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