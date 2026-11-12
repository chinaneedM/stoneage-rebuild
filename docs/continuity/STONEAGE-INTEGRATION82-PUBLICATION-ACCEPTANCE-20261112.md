# INTEGRATION82｜九张猜拳原DAT三平面来源保管与远端发布验收（2026-11-12）

## 原件与本轮新增的独立复核

从远端 `main=c29bcaf8cae8465e8e23860ef8e4cf56bff8dcfd`／tree `18d2e7407c431d8926f60d16f810d5145ea3dc32` 起步，重读协议、README、历史路线和完整旧 `docs/CURRENT-STATE.md` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`（2,709,173B；接口空响应没有被解释为文件为空）。旧CURRENT仍完整保存，本回执不覆写任何历史正文。

本轮独立从个人Library取回私人 `StoneAge-INTEGRATION81-janken-nine-partial-original-2D-private.zip`，全包16,080,715B，SHA256 `3a53d45971e23699be58d4f3b52812e0027aa2f8353dad6f66e44d5ecc162fa3`，ZIP 76成员全部CRC通过。从包内直接解析原 `private-original-DAT/{802,804,807,822,824,827,842,844,847}.dat` 九份，每份原长15,008B，头8B均为小端50×50，后续3个各2500格uint16原平面。逐5000B原平面重算完整SHA256，得到第一平面2种（六图与三图）、第二/第三各9种；以802→807为代表，第一平面恰有13/2500格不同。与已合并 [INTEGRATION82静态差异说明](STONEAGE-INTEGRATION82-JANKEN-DAT-PLANE-DELTAS-20261112.md) 中逐格(x,y)、原值、新值全部相符。额外永久留下 [九份原DAT的整文件与三平面完整SHA、13格坐标公开派生机器收据](../../research/recovered/STONEAGE-INTEGRATION82-JANKEN-DAT-PLANE-CUSTODY-R1.json)，供未来不重复私有原件提取时使用。

## GitHub准确后验（不得用旧成功冒充新CI）

[PR #357](https://github.com/chinaneedM/stoneage-rebuild/pull/357) 本体候选HEAD `0d80fda413e7f2894904ab2cda9458f939163120`、base `c29bcaf8cae8465e8e23860ef8e4cf56bff8dcfd`，实际只有**2条**关联的 `pull_request` Actions（O11/O12），均为 completed/success。没有46项候选CI的本轮证据，不称46/46。审阅一份21行源限定文档后，依用户持续授权及本轮原件实际独立字节复核，以squash方式合并为正式内容主线 `4fe800a44433bf0565b2a47ece34a43868697eb8`、tree `d1a6be09a8619bc4fe4de6e357ca2fad240cf2dc`。合并后查询该HEAD在Actions API返回**0条**新运行，表示未观察到本提交新增CI，而非“0/0全成功”。上一个验收回执主线 `c29bcaf8` 的26/26、INTEGRATION81内容 `8381be0c` 的27/27是真实旧SHA的运行，不借给本HEAD。此续接收据与机器SHA清单提交后如果触发CI，只按它自己的实际运行另验收。

## 证据止点与下一优先

这属于**社区mixed25载体九份原DAT的静态图层原字节事实**，不等于TW1/JSS1999官方同版、原生图层显示/遮挡/碰撞/行走/猜拳执行或客户端游戏场景已完整复原。独立台湾1.0旧RD候选仍缺后期9420–9423、10940真实原像素，本次新原RD解码0。私人DAT、商业图块、原NPC脚本/对白及观察图未写入公开Git，公开只留哈希、原格整数、负证与来源链。Stage A 7 PARTIAL＋2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，整体完成率未知。

**NEXT：** 本次DAT静态差异及三平面哈希归档已经止点；轮换另一个确有已保存合格原物的、尚未重复的宠物／物品／任务原二维内容关联。若没有新增真实原件/像素/语义，只做有界缺源记录；不扩Janken、原服联网、原版规则猜测或新游戏引擎。


## 正式主线后验补记（2026-11-12，归档时真实观察）

在上述带三平面原SHA清单的 [PR #358](https://github.com/chinaneedM/stoneage-rebuild/pull/358) 中，候选HEAD `4ced6a4d1148492604ef61b20fb150aaf5f078f4`／tree `3cc01cb32be9562c316d78d8c38ed9ee39952c0b` 的GitHub **26/26 push＋18/18 pull_request Actions，全44/44 completed/success**。此后squash合并至 `main=465d7fa7cc847ee80eef5ea47ef6f43598bf84ba`／**同tree**，正式内容主线 **26/26 push Actions completed/success**。再合计PR #357当时实际2/2 PR Actions，共**72条**当轮观察到的、分别绑定各自准确提交的成功run（2＋44＋26），真实run ID、事件、workflow名称、SHA与时间见 [机器验收回执](../../research/recovered/STONEAGE-INTEGRATION82-PUBLICATION-ACTIONS-R1.json)。此后验追加本身的新提交可能另起CI，不包含在上述72条中；不得把元数据CI称作原商业DAT再次执行或原客户端运行。
