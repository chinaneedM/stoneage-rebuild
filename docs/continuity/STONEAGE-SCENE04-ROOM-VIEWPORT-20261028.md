# SCENE04 — 可实际操作的房间原素材观察视口（2026-10-28）

类别：日期加法连续性检查点。**这不是原版游戏世界进入验收，也不是原始客户端的实际游戏截图。**

## 新一轮事实基线与取舍

本轮启动重新取 GitHub 远端 main `40827828202336eb60905e348d65f9d4f904cfc4`、tree `68519fce4245be916046a6675cdd52f01c1a318f`、最新提交、Actions、README、协议、DESIGN-DECISIONS、HISTORICAL-TIMELINE、SOURCE-REGISTRY、RESTORATION-ROADMAP-R2，及原生 Git blob 的完整历史 CURRENT（blob `031c76a5a8e431f646853909bb2f2e11e6328cd2`，远端元数据报告2680510B）。普通文件读取返回空，但 Git blob 正常读回；**未覆盖、截断或重写 CURRENT。** 前一轮 SCENE03 已于 PR #15 / 主线验收通过，本轮最高任务是 `SCENE-ROOM-OBSERVATION-04`。独立 `agent/scene-room-browser-runtime-r4-20261028` / Actions 40597637636 成功只代表 Playwright/Chromium 运行环境与合成按钮测试可用，不是实际场景验收。

## 实际私有原件、地图和图层实证

从用户私有 Library 实际重新取得 `stoneage-preserved-mixed25-original.rar`（361255180B，SHA256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`）、SCENE02 原图观察包及 SCENE03 颜色排列包；全部全文件 SHA256 与历史来源收据一致，不再次网络下载原商用载体。原版本角色是社区混合2.5保存材料，不认证为纯净官方 TW1.0。

以 SCENE03 私有观察包3356562B/SHA256 `fa296ad8e5afb9065fd8a7894fed4f783ad6f393901509f8491383c56a9ee285` 为输入，重新核原 `map/1001.dat`（5408B/SHA256 `62dbef1614ede0ba032ca9c69cbfdc3d43938e45baba78701885790937b86b90`）30×30三平面、同保存 `Palet_1.sap` 708B/SHA256 `32870080c47537a59beaf770b6df7bd79820fd52a23825058460900494f0b4b0`，八幅已来源验证的原索引图/PNG/SAP RGB，及同 R3 已证明的 3×3 12次序、三幅 199×166 RGBA 地面/构件/合成逐字节相同。所有新观测均限定此前原引用、SHA和派生像素；未声称历史运行时选色或完整同建绘制顺序。

本轮将地图1001观察范围扩为 **原坐标[13,13]—[17,17]，5×5格**：从原DAT实际得25次 tile 和5次 parts，合计30次引用；其中28次引用指向既有8幅实际源图。图号 **5009、5015** 两处尚无本轮原RD/PNG配对，画面以明确虚线「缺源」标注，**未用其他图像猜测或补画**。两次缺失仅表示当前被审计的私有观察包尚未收录该原像素，不代表原客户端缺图或游戏地图错误。所有30次编号、位置、后代源码候选32/24投影、ADRN有符号偏移的标准化序列摘要 `8df674d2c72a7891f42123ac4c45b4e13acaaa43c76f8319de593e7fe8240d55`。

## 真正浏览器交互及交付

生成离线、简体中文 UTF-8 的 **私有** 独立HTML观察器：具备鼠标/触摸拖动镜头、按钮及滚轮缩放、键盘平移、地面/构件独立开关、缺源标记开关和复位；所有交互只是现代观察镜头，不是人物走动。实际在 Chromium 144.0.7559.96 下执行了真实像素/点击交互测试：8/8实际图像载入、30/30原引用处理、图层关闭造成像素变化、重新开启恢复、缩放/鼠标/键盘/重置成功，JS异常0。该真实浏览器测试与前述独立环境准备 Actions 是不同事件，不可相互冒认。原游戏exe从未在本次浏览器中执行，原游戏世界未进入、原服NPC/战斗/声音及同建镜头遮挡全部OPEN。

以下三件已上传到**私人Library**且之后重新整件取回并独立比对SHA256（不是仅凭上传成功回执）：

| 私人文件 | 字节 | SHA256 |
| --- | ---: | --- |
| `stoneage-room-r4-private-observation.zip` | 289096 | `b3492c2f95d116f921d6133f3b1aeeceef6743d769a47938d8330b88bbb7a4fe` |
| `stoneage-room-r4-private-observer.html` | 61440 | `470659ed72efdb1d4f4ae73464a80c2d9542fb9ce7177c4efb63e4cb5effbbdb` |
| `stoneage-room-r4-browser-observation.png` | 243525 | `716e2fb00cf554d5d2c5604e64a4f6c2b41db66a72a0564ca931c4ed56985792` |

ZIP保存离线页面、截图、校验收据、私人重建脚本及实际浏览器交互测试源码，不包含整份361MB RAR。原图和用于播放的嵌入式版权像素只存在**私有**HTML/ZIP，公开Git只存本连续性文字和安全派生metadata，不发布原游戏图片、EXE、音频、真实原图PNG、RD、SAP或原DAT。

新增离线源门槛 `stoneage_room_source_gate_r4.py` 在本轮本地从真正的SCENE03私有包执行：6项合成测试通过，8源图身份、R3旧12位置及R4新30位置全量重放一致；派生 `STONEAGE-SCENE04-ROOM-ACCEPTANCE-R4.json` 只保留可公开来源摘要。源门槛脚本、6项合成测试和纯元数据回执另保存为私人Library `stoneage-room-r4-source-gate-private.zip`（4639B/SHA256 `c8a1a5440874b37203fc66b060edc7855e1a901be1cbc8e4e342882812da702b`），并已独立整件下载回读比对通过；它**不是**旧的289096B观察包的成员。旧观察ZIP保存的是HTML/截图/观察重建脚本/浏览器交互测试等。公开Git不要求CI具备版权私件。该源门槛成功不能证明新的5009/5015原RD数据已取得。

## 诚实记录的止点与下一NEXT

本轮已尝试从保管原RAR中定位同原客户端 `real_15.bin`，确认其目录存在，但当前隔离运行环境的libarchive RAR解流返回 `Invalid symbol`，0B原REAL有效正文，故没有这两幅新增原字节，也**不把解码器失败判断成原游戏素材损坏**。拒绝为了补两个未知图号重新下载已持有的整个原载体；下一有限包 **SCENE-ROOM-TWO-MISSING-REAL-BITMAPS-05**，应利用现有已保管原载体，在有资格的unar/兼容隔离提取环境只补5009与5015两个对应原ADRN/RD/PNG，并复核源SHA、重复编号候选，完成5×5真实像素缺口后重新观察。若证据或环境不具备，明确登记缺口并停止无限解包helper。之后仍独立推进原TW1.EXE在ACP950/8bpp可靠环境中的真实可操作世界进入，不能以本私有观察器替代。

保持DD-030简体中文新作、DD-028本体／运营活动／新增内容分档、Stage A七PARTIAL/二OPEN、Stage B及wiki GATED、客户端savedata R79暂停与总体恢复百分比 `null`。本提交候选/主线Actions结果**需要实际后验**，这里不预先填写SUCCESS。
