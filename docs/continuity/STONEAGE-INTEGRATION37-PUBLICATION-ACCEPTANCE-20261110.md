# INTEGRATION37｜GitHub 主线与来源受限验收（2026-11-10）

本记录附属于已合并 [PR #305](https://github.com/chinaneedM/stoneage-rebuild/pull/305)，且是 **2026-11-10 后验**；不是新发现原始图像/脚本，也不修改任何历史状态。

- 起点实测远端 main HEAD：`454a02a0d0c986ec480760589cf353b7a7920a4b`，tree：`259f715e37a4f91064b6479da413c88e42f316a5`。
- 本包工作分支：`agent/stoneage-integration37-goa-uli-20261110`，内容 HEAD：`9a45f370938cba9a58f2136653c92adfecfe4f7a`；对照起点 GitHub compare 恰5处：四个新增（派生源JSON、连续性说明、专用测试、Actions工作流），README 仅尾部追加，无删除。
- 专用候选 push GitHub Actions [run 42783357580](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42783357580) 实测 `completed/success`，源合同 Python unittest 步骤 success。同内容工作分支最后 HEAD 共有 **23/23** 个 push 检查完成成功。
- PR #305 同内容 HEAD 的 **15/15** 个 pull_request 检查均 `completed/success`，包括专用 [run 42783722646](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42783722646)。
- GitHub squash 合并后 `main` 内容 HEAD：`b23d3cffb7b75fee034f7a696c1a941d8eb89a7a`，Git commit 的原生 tree `5200533d311f14535a141621f43beb8fb0983b48`；该内容 HEAD **23/23** 个 push Actions 均完成成功，包括专用 [run 42783817908](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42783817908)，没有把旧提交 CI 当作新提交的结果。
- 合并后完整 tree `7686` 项、`truncated=false`；`docs/CURRENT-STATE.md` **2,709,173 原字节**／Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 不变。 README 为完整历史前缀保留并追加（新 Git blob `0a6e768257932270789ec8d7eaa8bba35e99819c`）。
- 成品派生记录 `research/recovered/STONEAGE-INTEGRATION37-GOA-ULI-LETTERS-MAP-SPR-SCRIPT-SOURCE-R1.json` 内容 Git blob `049c5a8bfbbfbb97928308cdcf302a556f9d6ce8`：10 CREATE、6 DAT地图/原格、2已验证SPR图号、10原脚本/旧16段、5原物品ID，源身份及源校验合并。报告并未取得新原商业资源/原服务端执行或新官方部署证据。
- 私人原图、DAT、完整原商业任务正文和旧ZIP均未写进公开仓库；Stage A 继续 **7 PARTIAL＋2 OPEN**；Stage B/wiki **GATED**；R79 **PAUSED_NON_BLOCKING**；整体进度百分比仍未知。

**续接 NEXT：** 不再重复上述 10 条原 CREATE/16 段旧任务；优先从现存22域/最近 INTEGRATION33–37 已覆盖范围之外，挑具可验原资源增量（同来源地图/SPR/原物品/新脚本）的模块。若只剩旧公开数值重拼则先止点并寻找合格私人原材料；新单机开发/旧网服建设仍不启动。

**回执范围限制：** 本文件是上述主线内容提交的真实后验；本回执提交自身若尚未触发 Actions，不得自动当作已有新的成功 run。
