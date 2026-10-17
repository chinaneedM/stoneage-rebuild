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
