# INTEGRATION109 — 72 条候选与正式内容主线 Actions 真验收（2026-11-14）

本验收只描述精确内容提交、实际运行和已完成的私源保管；**本验收归档提交自己的未来 CI 不预支成功**。

- 已合并 [内容 PR #401](https://github.com/chinaneedM/stoneage-rebuild/pull/401)。原候选 HEAD `469fcde7022bc4251c0c2c26444893d0de297eeb`，正式内容主线 squash HEAD `6bc2847c151a636b2b5b96d20246c6cd6949bc7e`；两者 tree 逐原 Git 身份相同，均为 `983a0bc3c33db75ab2013e5e4a1556dae3eb3b43`，0 内容漂移。
- 精确候选 HEAD：**26 条 push + 19 条 pull_request = 45/45** completed/success；正式内容 main：**27/27** completed/success。合计 **72/72 条互不重复的真实运行 ID**，全部名称、事件、精确 HEAD、状态、结果及时间见[永久机器收据](../../research/recovered/STONEAGE-INTEGRATION109-PUBLICATION-ACCEPTANCE-R1.json)。这是新旧测试流程的真实运行总数，不是 72 个新素材或 72 项玩法复原。
- 新专用 workflow 在候选 PR [run #43605839596](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43605839596) / job `132480164960`、正式 main [run #43605947611](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43605947611) / job `132480493629` 均真实 `Ran 6 tests`、`OK`。原来源和负证不会因测试通过升级为官方构建或原生执行。
- 真正原私人 mixed25 NPC ZIP `995176B` / SHA `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`、**2205/2205 CRC**；其中 `npc/genout/kingwarp.create` `36355B` / SHA `33f29f58215d07e139df4cd94b8a9b8bacb87b0acdebba58af704a3174712983` 实字节重核。**309/309** 来源配置段索引与既有 CHAR01 原字节 SHA/起点一致；源目标关联和旧 DAT 几何条件详见[材料报告](STONEAGE-INTEGRATION109-KINGWARP-STATIC-ROUTES-20261114.md)。
- 原完整 `docs/CURRENT-STATE.md` 为 **2,709,173B**、blob `c89e0e33537990aa2132b47c40fef49a985a935c`，内容主线 tree 上逐原 blob 保持；README 只追加新历史，不重写。商用原脚本/图片/原DAT不公开。本轮**新原DAT字节读0、原RD像素新解码0、原客户端可操作世界未进入**。
- Stage A **7 PARTIAL + 2 OPEN**；B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，overall percentage **UNKNOWN/null**。**NEXT** 换另一类未重复、可获得新原实物或真正二维可见图像的宠物／任务／场景材料，停止重复 `kingwarp` 静态图谱；只有新同载体合格 DAT 或原生实际运行才重开9个资格缺口。

本永久收据只核已发生的内容候选与内容主线验收；新收据候选、PR 和合并后的新HEAD自己的 Actions 要单独查，不得把过去的 72/72 自动继承给未来HEAD。
