# SCENE22：地图1000配置点的一份原对白输入

2026-10-29（Asia/Shanghai）。范围：既有社区混合2.5保存载体，LATER_RECOVERED；不是认证台湾1.0官方同服或原生游戏运行。

这一包把现有地图1000/(63,103)的可见图形候选，连接到真实创建配置所指向的**一份静态原对白文件**。它不是新发现整个村民系统，也不是完成了游戏世界。旧R18已有文件级库存和TownPeople总体统计，SCENE17已有创建位置/模板；本次增量是具体enemy尾部、准确文件正文及其语义/画面查阅整合。

| 原输入 | 完整字节 | 有据内容 |
| --- | ---: | --- |
| npc/genout/1000npc_m.create | 4413 | 块1，[287,450)，1000/(63,103)，图形16048、方向4；enemy精确指定npcgen_man及file:genout/msg_1000_63_103 |
| npc/genout/npcgen.template | 4950 | 唯一同名模板指向TownPeople |
| npc/genout/msg_1000_63_103 | 143 | 单行、末尾一个LF、四个句号；无ASCII逗号、无竖线 |

三原成员逐完整SHA与既有R18每行唯一匹配，父RAR361255180B/SHA d71e2e67…重新实核。系统libarchive实际解出三成员；另一个独立RAR4头解析器遍7952个文件头，全部头CRC与三成员CRC、压缩片段摘要成立。**这是一个解包器加独立头/CRC/旧完整SHA，不是两个解包器通过。** 本轮复用私人保管原件，未重拉公网客户端/分卷；source_action_run_id=null。

正文以CP950严格解码并逐字节往返；Big5同解，独立系统iconv BIG5→UTF8所得214B与Python完全同SHA。公开JSON只存结构/哈希和编辑释义；原文、原姓名、原脚本与私人HTML不进入公开Git。

## 内容合同

四句提示的简体**编辑释义**如下，不当作运行事实：

1. 与村民交谈可收集信息。
2. 同一位村民也可能提供不同信息。
3. 商店提示可使用购买口令。
4. 商店提示可使用出售口令。

已接受的后代TownPeople源码模型用ASCII逗号划分候选，但它不是这一保存服务器的同部署鉴真。该143B文件本身无该分隔符，结构上只有一个候选；文案提及多种信息**不证明这一NPC配置了多个随机分支**。四句提示也不证明买卖触发、价格、库存、成功ACK、任务奖励或持久化，不能把这个普通村民晋升成商店。

私人观察页保留原繁体全文与简体编辑释义，通过显式“查看该NPC原对白文件”打开并定位配置点；它是离线查阅，不假造原服聊天窗口或可操作世界。现有8个完整场景图及model未变，独立HTMLParser回读可见原文等于143B源的严格解码。JavaScript语法检查通过；本地无可用Chromium，未声称原图浏览器执行。远端UI验收只用合成色块/合成文字，须按真实后验记录。

## 有限止点与后续

这一个NPC静态内容输入已闭合。停止继续枚举其他TownPeople、原RAR、驱动、帧调度或原生绘制helper。下一包 **SCENE23-MATERIAL-ROTATION-REVIEW** 先回22域/R102有限查重排序，优先另一项已有原实物且能增加玩家可理解内容的角色创建/宠物或场景交互；有准确源字节才开展，缺件即记录。原客户端可操作世界、官方同服、原生对白执行、音频事件仍OPEN。Stage A 7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79暂停，总体百分比null。

重放：`python -m tools.stoneage_scene22_npc_argument`，相关测试：`python -m unittest -v tests.test_stoneage_scene22_npc_argument tests.test_stoneage_scene17_derived_acceptance tests.test_stoneage_presentation_npc_model`。公开重放只验证派生记录，不读取原脚本。
