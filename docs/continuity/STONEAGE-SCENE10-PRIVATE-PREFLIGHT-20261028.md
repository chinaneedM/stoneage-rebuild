# 2026-10-28 — SCENE10 私人候选帧阶段独立预检（非原EXE认证）

## 新远端起点和优先事项
以 GitHub main `3b79a2aed14b7922e8f4d2284029a1313763c428` / tree `2d85430e5ab8dab6f7f7261ac5e94cc6caf15002` 为唯一事实源，完整 tree 6336 项且 `truncated=false`。重新读 README、连续性协议、CURRENT 的原生 blob 元数据（2680510B, `031c76a5a8e431f646853909bb2f2e11e6328cd2`）、设计/历史/来源、R2 路线和 R9 日期覆层。最新 R9 收据专用 Actions `40694227056` 实际 completed/success。CURRENT 全文及历史六件未重写。本轮目标承接 R9 的 `SCENE10-SAME-CARRIER-FRAME-PHASE-ORDER`，验证受控“演员先入队”的帧内阶段顺序，而非开展新的大型逆向树。

## 新取得的实际材料与限定
从项目私人 Library 取得既有 `stoneage-room-r10-phase-observer.html` 候选，1150992B、完整 SHA256 `00e7565587e009c3e44bcffa1523ab4018886d637aaef1e04749dc01637628d4`。它不在本轮 GitHub 主线，属于**待独立认证的私有观察候选**；公开库只保留数字/来源指纹，绝不包含原源 PNG、原 EXE、原服务器或私人文件 ID。

本轮在本地解析该 HTML 的内嵌结构化元数据，验证四组记录的 callsite 单调性、边界、五个关键直接调用的目标序列、与 R9 既有 48 个实验用例和 30 个地图放置/218 幅来源图的一致性。四组起始 VA 分别为 `4494410/4495313/4495615/4495953`，共同候选序列为 `4368676→4198711→4508177→4356772→4506787`（按候选分别代表清链表、对象处理、对象直接队列、地图扫描、排序阶段）；四条路径尚有 `8/5/4/6` 个中间调用未重放，共 23 个。

**证据边界（关键）**：本执行环境没有供独立复核的混合2.5 `sa_2903.exe` 原字节；以上 callsite 和 96 用例仅来自私人候选报告，尚未对原机器码重新核验，更未执行四条完整外层路径。此处通过的只是结构一致性/否证门槛，而不是“原游戏已证明该帧序”。R10 候选的 `+1` 地图 X 修正、额外 kind1 请求均须原字节或可重复执行出链；不能把 96 个自报用例当本轮真实重放数。原客户端可操作世界、GPU遮挡、同构建官方物种/服务端、原完整帧仍 OPEN。

## 可复用交付及测试
- `research/recovered/STONEAGE-SCENE10-STRUCTURAL-PREFLIGHT-R1.json`：四条候选五段 callsite、来源/私人候选全文哈希、未执行的中间调用计数和不晋升条件。
- `tools/stoneage_scene10_preflight_guard.py`：只读校验，不打开私有素材、不运行原程序。
- `tests/test_stoneage_scene10_preflight.py`：10 个固定范围/负例用例；本地全过，含交换调用、篡改目标、删路径、抹去23个缺口和假装完成原帧/进世界的拒绝。
- 专用 CI 只读取公开派生 JSON 与合成负例；不下载游戏或上传源资源。CI 结果必须实际后验，不预支 success。

## NEXT 与止点
`SCENE10-SAME-CARRIER-ORIGINAL-EXE-CALLSITE-REPLAY-GATE`：当可独立取得与所声明 SHA 完整一致的原 `sa_2903.exe` 时，限四处外层调用、逐指令字节/分支/内存依赖、clear→actor→map→sort 的因果资格；有未知回调则列精确 VA/触发条件后停止，不补造真实原帧。不重拉整客户端、不扩通用 WinXP/渲染器/服务端。若原件无法在本轮独立保管，停止对同一候选空转，回更有材料结果的现代观察域。DD-028任务四档、DD-030简体UTF8、Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总体 percent=null 不变。

此为协议14允许的加法 checkpoint；不替代 CURRENT，也不改任何历史失败或已验 R9 事实。

## 主线验收后验（2026-10-28，同次候选证据，不晋升历史事实）

候选 `da3d1f8f866da2d77efab8475ab67af7cc835f43`/tree `782b36243caf62b18f46bda627588d8143f0946b` 专用 Action `40698221165` / job `122850615823` `completed/success`，实际日志显示 `python -m tools.stoneage_scene10_preflight_guard`通过及10/10 unittest成功。主线PR #25常规合并 `3b151393e5e526b804940b0aff4a0e9225a9abe5`，专用 Action `40698543024` / job `122851748824` 同样 `completed/success`，两边只验公开数值/否证门槛，没有读取原EXE、原像素或私有文件。

5件预检新增文件与旧 `CURRENT` blob `031c76a5a8e431f646853909bb2f2e11e6328cd2` 在主线 tree 完整核对；README和本日期覆层保留原完整内容并在此加法后验记录。报告来源层级仍为私人候选，不能伪造原source run。收据：`research/recovered/STONEAGE-SCENE10-PUBLICATION-R1.json`。本收据提交的自身CI不预先记为成功，下一轮单独核对。
