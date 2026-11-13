# INTEGRATION97｜四家族庄园原商店/13守卫条件：永久验收（2026-11-13）

## 正式内容入主线及 GitHub Actions

- 本批原件内容 [PR #377](https://github.com/chinaneedM/stoneage-rebuild/pull/377)，原候选 HEAD `0184b1d28edeab3cee8f56f4c5631f04158d24cf` / tree `aa8fc5582dafb41ff926acc7437c7ebbcdff4f78`，base 主线 `ad282efef9643b0080be1f7e846934bc11dbb637`。
- 候选精确SHA **4/4 Actions completed/success**：push [43444704278](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43444704278)、PR [43444780663](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43444780663)、PR [43444780628](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43444780628)、PR [43444780862](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43444780862)。专用源测试 push job `131951000531` 和 PR job `131951270317` 真实日志分别 **Ran 10 tests / OK**。
- 合并前 fresh main 与PR exact head/base均不变、无冲突且四Actions全成，squash merge 得到正式内容主线 **`6dab36c60051b4c8f53aba1d551301e9dd5ef16b`**，tree 与候选完全一致。
- 精确正式主线 SHA 的 [push run 43444984808](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43444984808) 实际 **1/1 completed/success**；job `131951968763` 真实日志 **Ran 10 tests / OK**。不以候选通过冒充主线通过。
- [永久机器验收收据](../../research/recovered/STONEAGE-INTEGRATION97-PUBLICATION-ACCEPTANCE-R1.json) 包括全部5条真实run identity、专用job、exact HEAD/tree、四个新Git blob、来源实物边界和故障勘误。**这份收据提交自身的 Actions 尚需另外按新SHA后验，不预支。**

## 实际原件与有界增量

重新取回私人源 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` **995,176B/SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，2,205/2,205 CRC**，只在私人环境解析原配置，未重新取父361MB RAR。4个正式命名 `.create` 文件 33条原配置，含旧ITEM01已登记的20商店参数及本批新整合13原守卫处理文件。5个 `.create.bak` 源文件单独标记，绝不宣称原服已加载或官方没有后续庄园。

本批真正增量是13原守卫文件43个 `NEWWARPMAN/TALKEVENT` 字面段，与四组家族 `MANOR=0..3`、邀请函 `19001..19004`、通行证 `19330..19333` 的同源商店 `ItemList` 静态条件接合。43段中13个 `WARP:0,0,0` 不能说是真实出口，30个非零目标静态段中包含17条 `DelItem` 字面记录。旧MAP04 21个DAT头部坐标尺寸吻合，但本轮真正原DAT/像素新读0。离线观察并非商业原服执行。

独立验收从早已公开归档的 CHAR01/ITEM01/MAP04 三套原源派生机器索引，重新核对 **334/334**：33个CREATE窗口及字段共231项，42个原文件全SHA/字节数，20个旧商店关系×2＝40项，21个旧DAT身份。首次内部SHA核验失败：本轮初版解析遗漏原CREATE闭合括号后换行，造成33组窗口/哈希不符；在公开提交前拒绝该版本并修正。历史修订保留，现与旧索引逐SHA同一、0剩余失配。公开原数据、测试和来源限定见 [INTEGRATION97专项报告](STONEAGE-INTEGRATION97-FOUR-MANOR-SHOPS-ORIGINAL-ITEM-GATES-20261113.md)。

## 止点

**SOURCE_BOUNDED_ACCEPTED（非GAMEPLAY_VERIFIED）**。保存混合2.5社区载体不等于已认证初代官方同部署。没有原生家族门禁、队伍状态、商店交易、`DelItem` 实际执行、NPC对白交互、地图碰撞等运行证据；私人商业NPC文案/脚本/原图未进公开Git。完整历史 `docs/CURRENT-STATE.md` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` / **2,709,173B** 原样保留；Stage A **7 PARTIAL+2 OPEN**、B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**，总进度百分比未知。

**NEXT：** 另选不重复、拥有实际原文件字节的NPC对白/任务/物品源关系，不再扩家族商店静态矩阵，不开展MMO账号、原网服或未来引擎新玩法开发。
