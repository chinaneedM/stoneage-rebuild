# PET14｜台湾1.0现存原像素图号与混合2.5两份原宠物主表分源对照（2026-11-06）

## 来源与恢复对象

从本次重新核验的 GitHub `main` HEAD `66c7c4f762f749b68c0eed067a3b9e05b0d97120`、tree `0110070556c053009e3fba6344cac9ab09c406d6` 和完整原 `docs/CURRENT-STATE.md` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 启动，遵循模块优先的宠物工作序列。当前复原 Stage A 不开发新游戏、原网游账号和服务器。

目标是将**此前已实际解码像素的台湾1.0原 SPR 图号样本**与**另一来源、后期社区混合2.5 RAR里的两份原宠物主表**做严格数字交叉索引，展示可审查的源字段而不混合历史种属身份。

- 原 TW1 像素载体：PET07 先前完成的130组SPR及私有原像素目录，原私人 HTML SHA256 `58e8ee4ff5165ed2f61663d67ae1cd0a8183622fa3375c480232784bfce9dc76`；本次复查其整 SHA、130组及2,540个既有PNG候选。固定公开原派生 Git blob `0b5f81b41a642025ab53a12884638fdee887470e`。
- 后代同RAR原源：PET10 mixed25 社区保存RAR 361,255,180B / SHA256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`；旧批原 `enemybase.txt` 988有效行和备选 `enemybase2.txt` 640有效行。私人逐原行 CP950 资料目录 SHA256 `640506addf01417390a7078f70aece167c99feecf4beeca8cb769f32972ff5d3` 已在本次重新回读；公开源数字索引 Git blob `25a37aeb134fb180e322e7dc335029b7374452d8`。
- **本次没有新取得原客户端/原RAR、没有新解码原RD像素，更没有原生客户端或GMSV运行**。原商业像素及原宠物主表全文不入公开Git。

## 真正新增的跨源可查关系

| 仅数值相等关系 | 混合2.5配置主表 | 混合2.5保存备用表 |
| --- | ---: | ---: |
| 原表全部模板行 | 988 | 640 |
| 与PET07 130组图号数值相交的原行 | 309 | 258 |
| 其中原 PETFLG=1 行 | 188 | 142 |
| 其中原 PETFLG=0 行 | 121 | 116 |
| 有任意原行的TW1候选图号组 | 130 | 129 |
| 有 PETFLG=1 原行的TW1候选图号组 | 130 | 124 |
| 不在PET07该130图号样本内的PETFLG=1原行 | 307 | 174 |

备用表没有任何相应行的候选图号为 `100454`；没有 PETFLG=1 行的六图号为 `100015/100018/100401/100432/100451/100454`，其PETFLG=0行及另一表的数据不能丢弃。两表重合的模板同号不可合并成当前生效配置，更不可将130或567推成游戏物种总数。

**私人实际可观察结果**：在完整未变的PET07原像素目录中，为当前选中的图号增加一个显式分源表，保留主/备两表的繁体原名、模板ID、PETFLG、物理行、INITNUM/LVUP字面、四基础数值、四元素和原技能槽号/空位。所有私人原名、原图与浏览器页仅本地封装，不进入Git。私人生成 HTML 大小 15,198,113B、SHA256 `949e1d28a228ecec6435ebdd463ac01804bb054c2578d1de839476e667e3b30f`；本次使用 Chromium/Playwright 实际检查图号100015和100018切换，原图加载、来源表更新，0 JS错误、0外部网络请求。**本次 Library 上传因会话接口失败两次，不能声称已经成功永久云端保存私人新页**；可通过当前工作回话的文件下载保留。原PET07私人页仍保留独立旧保存身份。

公开逐图号数值收据：[PET14 130组跨来源关系](../../research/recovered/STONEAGE-PET-MODULE-14-TW10-MIXED25-SOURCE-SEPARATED-NUMERIC-BRIDGE-R1.json)，配可重复执行的[派生工具](../../tools/stoneage_pet14_tw10_mixed25_source_bridge.py)与[校验用例](../../tests/test_stoneage_pet_module_14_source_bridge.py)。本地私有原件＋公开来源核验、130关系守恒、保留非PETFLG样本和负例已通过；远端CI以实际Actions状态为准。旧完整 CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c` 未动，依协议 §14 本文件是追加式节点。

## 边界及下一优先

所有源数字交集为**静态候选**。PET07台湾1.0原SPR/RD图号无法单凭同号/外观证明混合2.5表的名字、属性、技能就是台湾1.0官方数据或与其同服；PETFLG=1不能证明可捕获，成长/技能原生算法与捕捉成功都未执行。这一批不是原版游戏可玩性闭合。

目前 PET07/PET10 已可用源的此批跨表内容有界闭合，**PET-MODULE-01 SOURCE_BOUNDED_PARTIAL**。PET12台湾8.5六原捕捉候选余下1,568个RD实际原像素，须同包 `real_158.bin` 原载荷可重新合法读取后才动手；WORLD37-R2C原编译捕捉尾段必须完整 SHA/CRC 合格GMSV和隔离x86实验环境，均保持条件OPEN。不展开重复纯索引或私服账号。下一任务按模块总队列检查现存ITEM-EQUIPMENT-SHOP-MODULE-02等来源就绪内容，PET源一旦有实物到位再分源增量重开。Stage A仍7 PARTIAL+2 OPEN，Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、overall_percent=null。

## 2026-11-06 远端验收原始失败及修正（保留全部历史）

本批初次候选提交 `dd5733f13c7ed9a43e7049535e37fab5f2d479b8` 的既有 PET08 综合工作流 [run 42240466125](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42240466125) **failure**，21个测试中20通过、PET14 exact replay失败。原因是公开Python派生器先通过 `defaultdict(list)` 查询缺失图号，导致备用表的空缺键 `100454` 被初始化成空列表，随后用 `set(dict)` 误当真实存在；JSON、原源及私人图像未变，更不能据错误输出宣称该源有记录。修复提交 `3f954e373147a9d76fb2460f9c9947070770d727` 改为显式 `if not indices[table][key]` 判空，保留原来完整不匹配的负证。再次运行的 [run 42240568631](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42240568631) `completed/success`，PET08/09/10/14原派生同仓总计21项成功。两次CI与修复提交均保留，未把首次失败涂改为成功。旧CURRENT 2,709,173B 全Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 仍完全原样保留。
