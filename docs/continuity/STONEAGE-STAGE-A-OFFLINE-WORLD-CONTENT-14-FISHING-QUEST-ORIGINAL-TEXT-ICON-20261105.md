# Stage A｜WORLD14：钓竿制作/交付原文与原像私人观察（2026-11-05）

从全新主线 `ad3ee18d6bf6e86fe2eacd784a7a815eafe42eb7` / Git tree `51d945eb91cdfbf6f449f032cda2b63572cf383c` 继续。WORLD13 已合并且主线11项后验 Actions 实际全部成功。原 `docs/CURRENT-STATE.md` 保持 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 不变。当前任务仍只做历史复原、未来单机，无账号/网服/体验优化。

## 实读的两份私人保存资料

个人 Library 原 QUEST01 私人 295脚本 HTML/ZIP SHA256 `920e431fd972c58b2f94aba2997ce9415f77d71baf14d6e07fd26914b9729818` 与 ITEM01 私人两原主表/832 RD 图 ZIP SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa` 均重新实取，整ZIP SHA匹配、全部成员 CRC 通过；实际读取前者已保留的两份 `sainasu/event/nevent01_*` 原繁体文本与后者16个原物品行、13张候选PNG，并逐原 PNG SHA 和格式核对。**本轮并未重新解原社区RAR或零售REAL**；读取的是此前从源文件实读导出的私人包。源脚本与两套物品表来自保存的社区混合2.5材料，原RD图来自认证台湾1.0零售客户端，**无同一官方部署证明**。

## 现在真正恢复的内容

- `nevent01_2` 有9条原 `ACCEPT` 条件：三类竿材数字ID2569/2570/2571与三类线材数字ID2572/2573/2574组成九种组合，原字段各 `DelItem` 两份材料 `*1`，产生2432/2433/2434三种不同钓竿。原条件均 `LV>0` 加两项 `ITEM` 与 `TIME!=0`。任务原文确实描述木材与钓线、白天制作钓竿；不以 `TIME!=0` 猜测现实小时范围。
- `nevent01_1` 有3条原 `ACCEPT`，接收不同钓竿，原 `GetItem` **字面顺序**分别为 `2437,11872*2,11863`、`2436,11873,11863`、`2435,11874,11863`。另有1条 `MESSAGE` 条件 `LV>0&TIME!=0`、无 `GetItem`。交付的3条 ACCEPT **没有TIME字面**，不可把 MESSAGE 的条件套给它们。
- **重要修正：** WORLD13 的前一轮静态数字目录保留奖励ID集合，但部分列出顺序**并非原脚本原字面顺序**，且此前未保留 `11872*2` 的明确数量字段。WORLD14 用实际保存源文本核对原顺序与乘数，同时仅以旧目录核对ID集合和来源 SHA。保留旧来源记录，不倒改原历史。
- 两份原 `itemset` 中16条共同ID的原行SHA分别均完全相同，原名包括三种釣竿、三种魚、贝壳和六种材料。16个ID仅有13种同源数字图别名，均已在旧私人台湾1.0原RD候选图包实绘。不能将这份原像暗示为已验该社区任务在台湾1.0官方服存在。

## 离线可观察成果和证据范围

私人本地交付 `StoneAge-WORLD14-private-original-fishing-rod-quest-observer.zip`，**25693字节 / SHA256 `08782b29b9f743b8b886a757448298edc46e919786ba99fd85446d01bdd4586b`**，ZIP三成员CRC通过。自包含 `index.html` SHA256 `d5eb67ff6743602972794cb2b5b7a63619d1c04842fc65da2e5edac79bd7c7fe`，能切换13原条件分支、原物品名与候选图、原字面数量，查看两份完整原繁体源脚本。版权原图和商业原脚本全文**不入公开Git**。

新HTML的JS第一次静态检查发现Python模板转义导致的换行语法错误，改为raw字符串后在 Node `--check` PASS。Playwright 默认缺少 headless-shell；切换到已安装的 `/usr/bin/chromium` 真正运行 `page.set_content(同HTML字节)`，检查13按钮、16原图全部加载、点击第10交付分支恢复 `11872*2` 字面、原文切换可见，**JS错误0、外部请求0**。并未运行商业旧客户端，也未声称用户机器 file:// 原件已验。

[公开派生记录](../../research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-14-ORIGINAL-FISHING-QUEST-SOURCE-REPLAY-R1.json)仅有条件/数字/数量、极短原物品名、SHA和源边界。公开单测通过旧WORLD13同源数字目录检验13段映射，**不能**替代私人原文的重新读取或证明历史运行。

**NEXT WORLD15：** 一次源限定的钓竿资料链已闭合，换下一个有来源的真实宠物/人物/场景/物品/任务内容缺口；不继续堆同一两脚本、网游基础设施或引擎。Stage A 7 PARTIAL + 2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、总体完成率仍未知。
