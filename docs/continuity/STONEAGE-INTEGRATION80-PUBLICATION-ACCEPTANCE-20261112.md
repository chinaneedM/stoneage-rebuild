# INTEGRATION80｜dungeon03 13条静态原传送、五原DAT与正式主线验收（2026-11-12）

## 来源内容与已发布范围

按 [原RAR／五DAT／地图格源限定恢复](STONEAGE-INTEGRATION80-DUNGEON03-ORIGINAL-WARP-FIVE-DAT-20261112.md) 和 [13条逐块SHA、格原值、负证](../../research/recovered/STONEAGE-INTEGRATION80-DUNGEON03-NPC-WARP-DAT-SOURCE-R1.json) 执行。正式启动main为 `9d058513e2b8f85018d4ffa5d82a7ed5f33fcef6`，tree `f0935bdde1cb26d3d3109bcfd8c652de353de0f3`，其准确HEAD **26/26 Actions completed/success**。原始 `docs/CURRENT-STATE.md` 是2,709,173字节 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`，没有删减或覆盖。

从私人源实际核对361,255,180字节社区mixed25原RAR整SHA、1,621字节原 `dungeon03.create` 的CRC/整SHA、五份同包原DAT与此前MAP09保管原DAT的全字节一致。13条原 `npcgen_warp` 创建配置，5对静态反向字面联接；5地图内有9个原起点／9个目标有精确原三平面格值，其中5条双端有原DAT原字节。4张已有来源有界台湾1.0图块+mixed25地图的现代二维场景候选已私人目视。新增原RD解码**0**、新原美术**0**，不能据此认定原服实际传送、路径碰撞、同官方版本部署、原生窗口或原客户端真实画面。

## PR、主线Actions与专项运行

[PR #355](https://github.com/chinaneedM/stoneage-rebuild/pull/355) 候选 `853a7279c17cfe50f2355a309417f6e7aa1bd818`／tree `70d850346bc10051dea85119662fdf00cf0b3be2` 已经 **45/45 Actions真正completed/success**（push **26/26**，pull_request **19/19**）。新增专项 PR [run 43149210998](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43149210998)，job `130954137614`，真实日志包含 `Ran 14 tests` 与 `OK`，不能仅以本地结果代替该验收。

PR已 **squash合并**。正式内容主线 `7d793560d4a8b112484091d77bb0cffa9a80d210`／**同tree**，其 **27/27 push Actions** 全部completed/success；新增专项主线 [run 43149392591](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43149392591)，job `130954721836`，实际日志同为 `Ran 14 tests`、`OK`。本批45条候选与27条正式主线的确切run ID、HEAD、事件、结果、时间戳及来源摘要永久存[机器验收](../../research/recovered/STONEAGE-INTEGRATION80-PUBLICATION-ACCEPTANCE-R1.json)。**本验收收据自身后续HEAD的CI不属于上述内容主线27/27，需另作后验。**

## 私人来源二次保管与下一项

原始版权资料包 `StoneAge-INTEGRATION80-dungeon03-five-original-DAT-private.zip`：**105,583字节／11成员／SHA256 `b7f2b95ac75250faeba975e3f68a43bcdc426363d2deabbbdb700ed40b4de25e`**。包含实读原 NPC 创建配置、五份原DAT、四张此前已保存的**现代合成候选场景缩略图**及私人来源manifest；后四项不是当年原客户端截图。已上传用户个人Library `/石器时代/`，再独立重新取回，**全包字节及SHA一致、11/11 ZIP CRC和10/10源／缩略图成员SHA均通过**；没有将原脚本、原DAT、原图、私人观察内容公开上传GitHub。

旧 `CURRENT-STATE` 全历史原样保留，Stage A **7 PARTIAL+2 OPEN**、Stage B/wiki **GATED**、savedata R79 **PAUSED_NON_BLOCKING**、总体完成百分比未知。**NEXT**：按项目模块队列轮换其他有真实原件的非重复二维宠物、地图、装备或任务内容。若无同源原生触发证据，不再次扩写 `dungeon03` 传送路线，也不建设新服端或引擎。
