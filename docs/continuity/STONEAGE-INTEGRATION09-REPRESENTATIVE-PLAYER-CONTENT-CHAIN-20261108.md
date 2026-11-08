# INTEGRATION09｜代表性玩家内容链的原始材料联合审查（2026-11-08）

## 来源及审查目标

启动时重新读取GitHub main `a5950c17296fee3c421f44124b7c742c5ecd4468`／tree `37fb4dbc49dda2b276fe09a4943503b1ab13ffaf`，旧 `docs/CURRENT-STATE.md` 原Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` / 2,709,173B 未改。复用已发布的SCENE15、SCENE22、INTEGRATION08、QUEST25、QUEST26、INTEGRATION06/07七份公开来源派生报告，各自Git blob严格固定于[可重算来源索引](../../research/recovered/STONEAGE-INTEGRATION09-REPRESENTATIVE-PLAYER-CONTENT-CHAIN-R1.json)。所有关系限于**后期社区混合2.5保存载体**；台湾1.0/JSS1999/大陆1.82官方同版并未认证。本轮没有重新解原商业RAR、读取原客户端程序、生成原图或运行原游戏。

本包不把几个任务配置拼成虚构可玩攻略。目标是判断一个玩家从房屋进入野外、附近看到提示人物、接触任务节点的**静态内容关联中，哪些确有原字节证据、哪些依赖原生运行**。

## 可证的原始文件内容节点

| 资料节点 | 已认证的来源关系 | 不能据此升级的结论 |
|---|---|---|
| 1001室内 ↔ 1000室外 | SCENE15原`warp_y.create`第1/0块是1001(10,15)→1000(63,99)及反向；1001原DAT 30×30，1000原DAT 160×160，原完整SHA与INTEGRATION08的1000.DAT一致 | 原生走路、触发、门禁、镜头或碰撞未重放 |
| 1000(63,103)村民 | SCENE22另一个原`1000npc_m.create`的TownPeople块明确引用143字节已验原信息/商店口令提示；位置相对室外原落点坐标差(0,+4) | 坐标接近不等于可走通、实际刷出、触发对白或商店交易 |
| 1000的QUEST05特殊创建子集 | INTEGRATION08的19条有源SHA、原楼层、对应原参数，分7 ExChangeMan、2 Warp、10 Timeman | **63,103村民不在此19条子集中**，因为其来源是另一类原CREATE；19不等于地图总NPC人口 |
| 1000的环岛路线C/D原脚本 | QUEST25的C/D报名配置都在1000，C终点仍在1000、D终点在2000，各12站原证明石链及明确原脚本SHA | 不证明这些检查点沿地图真实可达、完整执行或发奖；不能从源列表画步行路线 |
| 1000(57,124) / 2000(55,92)互送内容 | QUEST26的两处`event02_2`/`event02_1`创建与INTEGRATION08对应一条相同来源原块；保留原2414/2415及旗标2条件 | CLEAN、条件逗号、ENDEV2实际解释及交易结果未实证，不能等同环岛通关 |
| 1000(108,28)源GetPet节点 | QUEST25与INTEGRATION05/08同一`oev_edc`原块，保留4个GetPet字面数字48/94/350/482 | 原生领取了宠物/数量/随机机制未实证 |
| 1300原地图与六CREATE | INTEGRATION06两份20,008B原MAP同SHA；四条ExChangeMan、两条Timeman配置；INTEGRATION07保留原DAT索引和CRC读取错误 | **1300.DAT可信完整字节未取得**，不能画原DAT场景、断言NPC生成或原可玩通路 |


### 路线C/D实际检查站对地图失读的影响（24个原位置）

在QUEST25的C/D各12条原检查站中，逐条取原`source.floor`与INTEGRATION07已证14个未匹配楼层的实际DAT读取记录比较，得到**7个“当前DAT读取失败”检查站位置**，而非抽象“整岛没图”：C路线第2站floor1100及第9站floor1300各1条；D路线第1、2、5、7、12站均在floor100、共5条。三个楼层均有源存档中的DAT成员记录但原先读取失败，**不是DAT不存在或已证明原包损坏**。其余17条没有落在此三类失败记录上，**并不意味着已见原像素、地图连通或原生可用**。这比仅罗列任务报名/终点更精确地限定了玩家路线的素材证据缺口。

## 审查的新关联与实际止点

最有用的正向结果是：**同一受限保存载体的两张完整DAT、有源块的双向传送关系和近距离原村民内容输入，形成了单个可追溯的“室内—室外—村民提示”证据链**。它比只有数字地图ID更具体，但仍是文件层的原内容，而非原生游戏演示。原村民并非QUEST05所选19条特殊CREATE之一，不能往“19个NPC”中简单加1并称人口20；两集合不是同一统计总体。

QUEST25/26与GetPet给该1000场景带来更多可按脚本/格坐标检索的内容，**不构成证明了可走路线**。1300是另一种缺口：原MAP与原CREATE存在但DAT提取失败。旧失败必须保留，不能用MAP头/公式合成所谓恢复的DAT，也不能把未匹配955 DAT称为原游戏没地图。

止点：本轮不建设旧账号服务器、不扩脚本解释器、不做现代角色步行仿真。只有合格完整1300.DAT原字节及全CRC/SHA可重新定级地图；原生动作/任务效果需精确版本原生执行或同等直接实证。未拥有资料的缺口保留OPEN，下一包回到**仍有合格原内容输入、且能产生新玩家可见材料的优先事项**，不要围绕本链重复加helper。

本次[JSON证据及8项新来源回归](../../tests/test_stoneage_integration_module_09.py)仅运行公开派生文件，不包含商业原稿、地图原字节、人物图或对话正文。原历史CURRENT完整保留；Stage A 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79暂停，整体完成率未知。候选、主线Actions和正式合并结果必须见GitHub实际后验，不提前宣称通过。


## 实际GitHub出版与主线验收后验

[PR #276](https://github.com/chinaneedM/stoneage-rebuild/pull/276)最终候选`a8177b3712f06d2a99284366509a2d7810d874aa`／tree `58d0be99a639ba47e247db6704dcd7cb6f9b2180` 按squash正式合并，主线合并HEAD `8acd13400999b79b2eedf381e7790746a567d156`／tree同一，原`CURRENT-STATE.md`仍为2,709,173B、blob `c89e0e33537990aa2132b47c40fef49a985a935c`。最终候选 **14/14** Actions completed/success，含push专项[run42496223627](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42496223627)和PR专项[run42496227613](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42496227613)/job128779058473，日志实际为8项公开派生单测通过。合并后内容main **11/11** Actions completed/success，含[INTEGRATION09专项run42496406428](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42496406428)/job128779593630，执行Python unittest成功。原先中间候选与早期排队历史不抹除、不当最终成功记录。完整运行ID、Git文件SHA及来源否定边界见[正式出版验收收据](../../research/recovered/STONEAGE-INTEGRATION09-PUBLICATION-ACCEPTANCE-R1.json)。本收据自身提交的Actions不能预先宣称通过。最高NEXT仍是另一个有真正原素材增量的玩家可见Stage A内容缺口，当前无原生可玩地图/任务或早期官方同部署证明。
