# INTEGRATION110｜正式来源、候选与主线 72 项 Actions 真实验收（2026-11-14）

此收据仅为**已经发生**的 INTEGRATION110 内容提交作证；**验收收据本身的新分支/新HEAD的 CI 不得预记成功**。

- [内容 PR #403](https://github.com/chinaneedM/stoneage-rebuild/pull/403) 已实际 squash 合并。内容候选 `b5356ea33f4697b406532ba350b3fbaacd005324`；正式内容main `dc17be8630bb174b31a9995a8d81e40000a680e9`。二者Git tree同为 `f3805940bbe6fdc30b621057f14341eab4349db9`，内容没有漂移。合并前main `422a5d067b61997c92d534c0687eca4262a5dbba`。
- 精确候选HEAD：**26 push + 19 pull_request = 45/45** 条真实 `completed/success`；正式内容main **27/27 push** 同结果。共 **72/72 个不同 Actions run ID**，原名、event、HEAD、运行时间、status、conclusion及URL全部入[机器验收收据](../../research/recovered/STONEAGE-INTEGRATION110-PUBLICATION-ACCEPTANCE-R1.json)。这些是CI运行，不是72种恢复出的游戏内容。
- 专用测试候选PR真实 [run 43608042395](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43608042395) / job `132486814560` 和内容main [run 43608183909](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43608183909) / job `132487238355` 均实际日志 `Ran 8 tests / OK`。测试覆盖22段相对既有CHAR01全源SHA、9原文件的SHA/CRC/尺寸、七已验DAT来源尺寸、12严格反向/2缺反向、入口一格异文和3例故意篡改拒绝。
- 本轮真正重读私人后期community mixed25 NPC ZIP **995,176B / 2,205 CRC / SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`**；`11100npc.create` 1,481B／8原配置及 `11101d.create` 1,737B／14原配置、7原外参，均和之前源索引吻合。未把它们称为本轮首次找回22新文件；原商业对话和图像保持私人。唯一新增的内容关联为夢德族短名/短文本→同源NPC配置→11101–11107七DAT旧来源尺寸及静态路由；**100(443,127)→11101(33,29) 与 11101(33,28)→100(442,127)不是精确逆向**。
- `docs/CURRENT-STATE.md` 原 **2,709,173B**、Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 保留全文；README仅尾部追加。原DAT新读取0B、原RD新解码0、原版商业客户端与服务器没有真正启动、原碰撞/可通行及初代TW1同服仍不可证。

Stage A仍 **7 PARTIAL + 2 OPEN**；Stage B/wiki **GATED**；R79 **PAUSED_NON_BLOCKING**；总完成率 `null`。**NEXT** 独立材料来源下真正新的宠物/任务/二维可见场景内容；停止扩同一静态路由或重新编造已验内容。本验收归档PR、它自己的CI、合并后main新HEAD再依实际核验，不把72/72预先继承。
