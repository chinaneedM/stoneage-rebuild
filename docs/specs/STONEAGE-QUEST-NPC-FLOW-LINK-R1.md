# QUEST-NPC-FLOW-LINK-06 — 五件伐木物品在同一NPC事件记录中的来源限定关联

日期：2026-10-17。类别：Stage A历史复原／后代资料参考，不是新石器引擎开发，不是原始台湾1.0商业服NPC复活。

## 目标、证据边界与交付条件

上一任务`QUEST-NPC-ITEM-BINDING-05`在固定来源的recovered25 NPC参数中发现五项后代模板（2465交差斧、2478採伐許可證、2481杉的手環、2484折斷的斧頭、20197伐木許可證）共49次具有字段语法的引用。但仅按模板ID统计，无法证明多件物品在同一条件、收回或发放事件里相连。

本任务仅检查`ExChangeMan`的`EventEnd`分隔记录内，五个ID的`GetItem`、`DelItem`及`EVENT:ITEM`是否共现。每次发现给出匿名记录hash、精确角色组合、相同记录实例数，不导出NPC名称/模板、对白、坐标、原参数/脚本、完整行或保存包。不得把`ItemShop`销售、`FREE`或纯数字出现当做任务；ID20197与2478相同图像不能合并，名称标签不是初代原物身份。

## 技术限定

沿用上轮原数据的两个分卷／合包SHA256核对和NPC参数解析；只允许后代`NPCTEMPLATE`和`NPCCREATE`有唯一函数类别的引用，依照既有file/inline来源读取。函数只能在`ExChangeMan`同一`EventEnd`分隔记录内提取完整项语法（不匹配`12465`或伪字段），并与已认证`STONEAGE-QUEST-NPC-ITEM-CI-DERIVED-R1.json`逐类逐次数匹配，包括49总引用与旧模板歧义30／缺文件15，不许悄悄扩展抽样或隐瞒不一致。持久化输出最多100个匿名被命中记录。格式、边界均由合成否证测试覆盖。

同一记录中存在条件、收回及发放，仍**不能**证明条件可满足、动作实际执行、NPC坐标/任务可达、玩家背包交易原子性、真实日志、同一原始台湾1.0版服端实现或最终任务奖励。两个记录分开的字段不可跨`EventEnd`缝成一个事务。相同匿名记录hash重复实例只能作为后代配置重用次数，不推出独立作者或服务器版本。

## 独立审计及停止规则

`tools/stoneage_quest_npc_flow_link_probe.py`、`tests/test_stoneage_quest_npc_flow_link_probe.py`、`.github/workflows/validate-stoneage-quest-npc-flow-link.yml`构成来源核验。CI首先在一个**独立环境**验证两个固定下载分卷和合包，再作实际NPC参数探测；仅上传短期派生JSON供独立ZIP/raw digest比较，之后保存无版权风险的派生报告与完整保管凭据到Git。

若只有单字段零散命中、无法取原参数、出现hash/语法/旧49引用不一致，保留UNKNOWN并结束本有限研究，不反复索取资料包、不全量扫描各版本NPC、不根据后代模型重写现代原版规则。Stage A九系统7 PARTIAL+2 OPEN；正式联合审阅尚待用户，Stage B GATED，R79 PAUSED_NON_BLOCKING。

## 验收入口

```bash
python -m unittest tests.test_stoneage_quest_npc_flow_link_probe -v
python -m tools.stoneage_quest_npc_flow_link_probe --npc-dir /temporary/SA2.5服務端/gmsv/data/npc --output /tmp/quest-npc-flow-derived.json
```

完整来源验收与永久归档应记录源HEAD/tree、Action/job/artifact ID、ZIP/raw SHA256及永久Git blob；本规格提交时不预先声明真实来源成功。

## 2026-10-17 实际同事件来源结果及独立链

首次数据来源Action38997164871/job117292136171成功：两个固定分卷与合包来源hash真实读取及匹配，9项合成事件分隔/错误晋级检查通过，从保存包的NPC参数独立生成派生JSON。基准上一包49次字段引用与本包精确一致；4,985条create NPC引用、30项歧义模板、15项缺失二级参数，差异为零。原始商业服务端没有执行。

27条有目标物品引用的匿名`EventEnd`记录（每条只有一处实例），共49字段引用。其中19条具有多种字段角色，3条为至少两种不同目标物品共现。**具体有界发现：**

| 同一条EventEnd记录内可核对的角色组合 | 记录数 | 可证明 | 不可证明 |
|---|---:|---|---|
| ITEM条件引用2465，DelItem2465，GetItem2484 | 2 | 后代参数中有两条「交差斧收回／断斧发放」候选记录 | 任务步骤先后、实际交换、改造斧攻33 |
| ITEM条件引用2478，DelItem2478，GetItem2481 | 1 | 后代参数中有一条「采伐许可收回／手环发放」候选记录 | 等于伐木全流程、限定原版1.0、旧指南手环魅+5/-5 |
| 单ID同记录多字段（以2478为主） | 16 | 同一参数记录存在条件和删除等角色 | 所有条件在执行时成立 |
| 其余只含单ID单角色 | 8 | 只属零散参数痕迹 | 多个记录之间是同一个任务 |

ID20197在合格字段角色中没有命中；2478与20197两许可证既不相同也不应按同图像合并。另无任何`2465`与`2478`在同一EventEnd记录共现；**不能**因为同源档案有两条候选关系就拼成一个从许可到斧头到手环的原始任务链。

来源派生`research/recovered/STONEAGE-QUEST-NPC-FLOW-CI-DERIVED-R1.json`原字节15,004、SHA256 `719b6dc071ea9d5946d707ced51798786d7b227d642bb80f009290ca834ad05a`、永久Git blob `b9f04bd7956a25a249e182fad4db2f0459719327`。独立下载的artifact12087945346 ZIP 2,196字节 SHA256 `a824365bfae4f4763192779dac853d431014bdfdc8af3c1785c1da6f71b0b3e3`，单一成员raw与Git blob字节相同；原文件、NPC文本、对话、脚本均不入仓库。完整来源HEAD/tree/run/job/ZIP/raw/blob在`STONEAGE-QUEST-NPC-FLOW-ACCEPTANCE-R1.json`。

### 关闭条件与下一项

`QUEST-NPC-FLOW-LINK-06`已完成限定目标：存在两种不同物品同事件候选关系，但**没有**完整伐木任务的原服身份或状态事务证据。下一轮不继续在后代NPC helper上自动加R编号；先进行`STAGE-A-PORTFOLIO-CHECKPOINT-02`，以九系统实际资料阻塞、最早JSS/台湾1.0证据、地区归属及用户正式验收需求重新排序下一项实体复原。未来只有出现原始官方任务脚本／定年独立资料、或明确核心规则冲突才重开同一事件分析。

Stage A仍九系统7 PARTIAL+2 OPEN；Stage B GATED；R79 PAUSED_NON_BLOCKING，现有玩家交互模型不是初代服务器运行的证明。
