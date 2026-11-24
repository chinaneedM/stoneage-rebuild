# PET-HIGH-FIRST-50｜原件取得分流预检（未验收）

基于 main 666b8c0206cc407cfe62ef7aa9a7503402ba6e09 / tree 53b96ba7f76aded47cf930667573320931783271，PET49 PR #660 已合并，主线39/39 Actions成功，历史CURRENT不动。

对剩余67个位置直接用已验PET10表指纹、实例指向核查：选中表65个有实例（62个且模板全行精确，3个同号不同全行），2个只有主档模板（993史奈克特、994葛利斯奈）。备用成对主表及实例表只有854动物园养的拉斯基同时满足精确行和实例存在。存在实例不是取得。

本次发现保存档NPC创建索引含三份vip宠物商店参数原件及四村petmaster创建引用；另有未被CREATE引用的vippetshop5及骑宠相关m_tiger。限定提取12份原件：setup、encount、group1、group、enemy、enemy2及上述6份NPC参数。选中/未选中四种表组合分轨；按原SHA和CRC核验，复放PET45选中链，另查正权重、双标记、Lv1与无路线实例，并只公布目标数字字段和散列。NPC数值匹配仅作待证线索，GetPet单独分级，未证明任何原服实际发放。禁止用备用表补造选中配置。

源运行尚待完成。NEXT 先验收该分支原件运行与工件/日志，再按实际结果独立复验、归档派生JSON，确认新增取得参考/保留缺件，必要时查对应后期VIP宠商店代码的参数命名空间。失败记录保留。未获得新官方客户端，未减少67缺件，PET唯一，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、总体UNKNOWN。完整CURRENT blob c89e0e33537990aa2132b47c40fef49a985a935c不改。

## 源执行纠错

首次[45457133731](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/45457133731)已进入原件解析但失败：备用enemy2.txt首行被误按选中表34列读取。PET10固定原件索引明确记录enemy2.txt为1494行、每行33列；enemy.txt为2087行、34列。更正为分别严格验原宽度及行数，不跳过、不补列、不改原件。首次失败无派生工件，保留失败记录。修正后重新执行；实际结果仍待证。

第二次[45457842476](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/45457842476)通过宽度阶段，发现备用实例表第6行以旧ID列误读为重复2。根据固定PET10行序全量反核：选中表ID/模板列（从0计）3/4，备用候选2/3；新程序要求1494及2087个原行ID/模板全量对应，不能只凭少数样例推断。备用表后续等级/宠物标志的字段语义尚未核实，本轮留null，正权重路径与双标志资格分开；第二次失败保留且无派生工件。新程序另区分明确GetPet/AddPet数值字段与一般词法命中。后期独立代码对照（非同部署）：pimpcapital/longzoro-sa@57b14e2bb373ba851c14db28a239273e4a8831bb，gmsv/src/npc/npc_vipshop.c blob 7f571bab0a612b7b3f684f2702b43c13b9bfe5b3，188–205行，菜单确认调用ActionNpc_CheckMenuFree；gavinlinasd/StoneAge@1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56，gmsv/src/npc/npc_eventaction.c blob 85010d54104dfff9d386b30c2ba33dbe26d1e4e6，133–157行FREE条件与动作调用，940–975行AddPet按ENEMY_ID解析而不是ENEMY_TEMPNO。原件菜单字段须实读才可关联，不证明同部署或实际兑换。

## 归档验收

[原件派生报告](../../research/pets/PET-HIGH-FIRST-50-ORIGINAL-ACQUISITION-R1.json)与[独立重取及 VIP 菜单派生报告](../../research/pets/PET-HIGH-FIRST-50-VIP-MENU-R1.json)分别按下载的 ZIP、原 JSON 和 Actions 日志核验。原运行遍历 7,954 个 RAR 头，读取 184 个 HTTP 206 区间，共 12,013,836 字节，由 unar 解出 12 份成员。独立运行按已确认的原偏移只重取 7 段共 458,752 字节，由 libarchive 逐份解包。7 段散列、12 个原头及压缩区散列、12 份成员长度/SHA-256/CRC32 全部相同。67 个模板、两对实例表、两个群组表与六份 NPC 参数的完整派生投影也一致。完整分卷此次未重哈希。

| 来源 | 固定 Git HEAD | 运行、作业、工件 ID | ZIP 字节数与 SHA-256 | JSON 字节数、SHA-256 与 Git blob |
|---|---|---|---|---|
| 首次成功原件复放 | `fb204735b221ee7e7d5fb4d19552f6dd6d61fc17` | [45458262853](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/45458262853) / 138673481783 / 14950253126 | 23,671 · `ac513a71258260c3b50baef502be9e89e99a69512e928432f77380099fa8234f` | 243,336 · `0f57d7a41e57d22080fc72e4a871063c389da162ca262a59e20f8603fcdcb52e` · `4d0b31a7fa196cf8f227a7b0b1aea7183d9598f0` |
| 独立复放及 VIP 参数 | `51fb64185f4f872c9862332f6c151130b77c92c1` | [45460556181](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/45460556181) / 138681637719 / 14952667213 | 2,922 · `7a26a469fc3c2be234d34879dc31af16f142ce86f7e65788c557552647d833f3` | 23,872 · `fe70ac60bb2d112f1ba66ebbc47d2caa692df817a76e96698f85921859ce5579` · `322436e8978166e0f5f9d4f005ccbe4febbd3adf` |

独立运行 [45459998568](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/45459998568) 和 [45460278120](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/45460278120) 均通过 12 份原件及完整投影复验，分别停在 VIP 首字段过窄的语法断言和菜单块一一配对断言。最终报告按原文件物理行保留字段和值散列，对未解释首字段保留空值，菜单排列与原运行加载关系待证。两次失败均未产出派生工件。

### 67 个模板位置逐项结论

- 选中实例表可连通 65 个位置，其中 62 个有完整模板行指纹，3 个同号异行。模板 993 史奈克特、994 葛利斯奈无选中实例。备用表仅 854 动物园养的拉斯基同时具有精确模板和实例。备用实例表的等级与宠物标记仍未知。
- 四组表组合均无正权重遇敌路径。奇肯沃、奇肯克奈、薩德迪比、薩德斯凱、瑞里西爾共五个位置存在正权重群组成员，但这些群组没有正权重地区入口。是否由脚本直接进入战斗仍待源文件验证。
- 四只有精确模板行的新手虎可连至保存档的训练师配置。实例 2481–2484 分别指向模板 161–164，均 Lv1，模板和实例宠物标记均为 1。四个创建块共用 `m_tiger`，12 条 `AddPet` 各实例出现三次。原脚本先前已由 [O61](STONEAGE-O61-FOUR-TIGER-TRAINERS-20261101.md) 查实，本次增量是把该证据接入标称 7.5 的四个确定模板，以及统一查询。后期解释器调用链见 [O62](STONEAGE-O62-TIGER-ADDPET-CALLCHAIN-20261101.md)。
- 四份 VIP 参数共 42 个 `VipPet` 字段，前三份分别有 7、19、9 项并各有一个创建引用，第四份 7 项没有创建引用。12 个数字栏位解析到 6 个不同模板 755、777、901–904，模板整行均与标称 7.5 异指纹。另有两处 `MM3` 条件别名、28 个首字段未解释。12 个数字栏位保留原点数及实例物理行。没有 VIP 栏位能用已核实的模板整行连接到这批 67 个位置。
- 后期参考源码 `pimpcapital/longzoro-sa@57b14e2bb373ba851c14db28a239273e4a8831bb`。菜单确认见 [npc_vipshop.c](https://github.com/pimpcapital/longzoro-sa/blob/57b14e2bb373ba851c14db28a239273e4a8831bb/gmsv/src/npc/npc_vipshop.c#L188-L205)（blob `7f571bab0a612b7b3f684f2702b43c13b9bfe5b3`），分隔字段见 [npcutil.c](https://github.com/pimpcapital/longzoro-sa/blob/57b14e2bb373ba851c14db28a239273e4a8831bb/gmsv/src/npc/npcutil.c#L1032-L1057)（blob `bbd3aeebeedd0fd9b050ed66b0b56f5f09ea9021`）。[npc_eventaction.c](https://github.com/pimpcapital/longzoro-sa/blob/57b14e2bb373ba851c14db28a239273e4a8831bb/gmsv/src/npc/npc_eventaction.c#L1355-L1408)（blob `38a73f776cbc4a5bccb5f81d95fcaa2dd11003ba`）按实例编号取宠，并另外检查点数、空栏及是否有条件别名宏。没有同部署代码或实际兑换记录。

统一查询现关联 PET47–49 的 70 条取得参考与上下文链接、PET50 的 67 条原件记录和 4 条训练师脚本链接。现有 467 条标称 7.5 模板的查询位置数保持。PET49 的 67 个缺正式取得参考位置保留，四个训练师脚本候选可独立查到。本轮确认官服实际发放 0 项，未新增官方物种或新客户端，发行年份和原服取得未知。历史 CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c` 完整保留。PET 唯一活动模块，Stage A 7 PARTIAL + 2 OPEN、Stage B/wiki GATED、R79 暂停，总体 UNKNOWN。

**NEXT PET-HIGH-FIRST-51**。在现有经典 PC 保存档与已认证历史资料中，优先核查是否有任务脚本直接调用上述五个有群组成员但没有地区入口的模板，或是否存在可解释 28 个 VIP 首字段的同部署定义。只有源文件和命名空间直接对上才升级。缺少同部署证据时，保留这两项明确重开条件，转向可取得的高版原件和具名官方发布记录。
