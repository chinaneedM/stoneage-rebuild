# QUEST32｜任务模块源脚本查重与有界收口（2026-11-08）

## 新远端起点与对象

依连续性协议从 main `d579fff4138a997eb9fd0594b5497c31fb26f413`／tree `0c28ed4c33b71bf583dbbe2977e5e2280cf376fe` 启动，并通过 Git 原生 blob 读取保存的完整 `docs/CURRENT-STATE.md`（2,709,173 B，blob `c89e0e33537990aa2132b47c40fef49a985a935c`）。最新 QUEST31 原件与候选/合并后 14/14、11/11 已见通过，主线最新 HEAD 10项 Actions completed/success；0 开放 PR。原大 CURRENT 不作覆盖。

**历史内容对象：** 复核 QUEST08–31 各专项恢复的真实 `ExChangeMan` 来源脚本是否重复、有没有超出原 QUEST01 CREATE引用目录，以及剩余多少脚本未逐项审查。目的是给任务模块一个有证据的阶段止点，而不是重复解析剧情、扩大辅助工具、宣称原任务可玩。

## 已由远端原派生 Git 数据复核的结果

原 QUEST01 是 315 个创建引用→**295 个不同来源脚本／1,349 个 TYPE 段**的目录，Git blob `52db8b4b6cd43cd2afa4a8d2e8460f214933f5e2`。其分母只代表这份后期混合载体、所选创建函数的源目录，绝非历史游戏任务总数。

| 范围 | 精确值 | 不能理解为 |
|---|---:|---|
| QUEST08–31 专项 | 24 份 | 24 个新发现、独立、可通关任务 |
| 各报告所选脚本记录累计 | 236 次 | 236 个不同脚本 |
| 按精确路径去重 | 235 路径 | 235 个官方任务 |
| 与 QUEST01 路径+原文件 SHA 同时一致 | **233** | 233 个初版官方脚本 |
| 不属于 QUEST01 创建引用目录的原保存脚本 | **2** | 后期材料不存在于游戏 |
| QUEST01 目录尚未被这24份专项逐份选择 | **62** | 原内容缺失／无可研究来源 |

跨报告唯一一次重复是 `king/event69_1`，QUEST10 与 QUEST29 均引用同一原文件 SHA，不能累计为两个新脚本。QUEST10 保存的 `giiru/event/event30_5` 与 `giiru/event/event30_5.old` 不在此前仅收有 CREATE 引用的 QUEST01 295份目录中；这是**目录范围差异**，不是把旧 QUEST01 判为错误，也不证明两文件曾被商业服装载。

尚未逐份选中的 **62** 份按原文件目录分布：chatroom 10、extra/event 5、genout 3、giiru/event 10、jaruga/event 6、my/chengren 1、my/zhuansheng 4、poru 3、quiz 6、sa60/newbie 2、sainasu/event 12。原目录中的 king、giiru/event/sink、seimu/event 在本次所定义的脚本路径层面均已覆盖；不是运行、分支或剧情完整性证明。

此检查明确按 **原路径和同一 SHA** 联接，保留 REPORT 的原脚本记录重复，不拿事件编号、NPC编号、宠物图号或道具数字当作同源身份。未来获得新同版官方资料前，剩余62份的“专项未覆盖”不能转写为“全部任务已恢复”“已经排除任务价值”或不存在；这62份的精确名字与可能关联可由当前 QUEST01 Git 索引继续查询。

## 交付与证据止点

[可机读审查快照](../../research/recovered/STONEAGE-QUEST32-MODULE-DEDUPE-AUDIT-R1.json)与[只使用已公开派生索引的重算程序](../../tools/stoneage_quest32_module_audit.py)以 **24个真实源报告→原文件路径+SHA→295目录** 做守恒核对，五项单测覆盖次数、重复、未收录变体、62条剩余和全量重算。CI只核公开派生 Git 证据，不重新读取私人RAR/NPC原文/原图，不验证原程序运行或原运营服任务执行。校验失败不可据此删除早期记录或伪造原始资料。

按源就绪批次审查后将任务模块定为 **SOURCE_BOUNDED_PARTIAL（本批阶段性收口，不是完全恢复）**。本次真实内容增量是**任务源清单的跨专项保真去重及缺口定量**，没有新原NPC对白、DAT实绘、宠物领取、任务运行链或原图。Stage A仍7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，整体百分比未知。

**下一优先 INTEGRATION06**：优先用已有同来源证据选择一个真正影响玩家内容的 NPC／地图／物品／宠物跨模块关联，严格核原文件路径、SHA、地图资格与版本来源；若找不到新的可判定关系，则转综合阶段审阅，不扩TASK小编号。对上述62份，仅在新原字节或已有脚本数值确实改变游戏内容关系时有界重开；不为脚本目录分母穷举、开发网服、引擎、自动化战斗或新单机体验方案。

> 本文记录候选改动的源核验；PR、Actions、合并后真实验收与主线HEAD须后验填写，不能以本段提前宣称发布成功。


## 7. 实际 GitHub 合并、主线 Actions 与保存验收

**真实后验**：[PR #272](https://github.com/chinaneedM/stoneage-rebuild/pull/272) 已以 squash 合并；候选最终提交 `9622b8e746f2d9a0ea57ca31701aea754d677552`，接受主线 `40e0d31d4dc60108b371f19e8fe1e9607a3c7f78`／tree `2fef7d5b6bd3bbd5af7b9cfaf67029d0ba5546e8`。候选同 SHA push 专项 run 42490982958、pull_request 专项 run 42491000171、PR原 O11 运行42491000116、O12运行42491000098，**4/4** 实际 `completed/success`。最初候选 `ef701038...` 曾有 Git blob NUL 分隔符的反斜杠错误，后续候选提交 `9622b8e...` 正确改为 `b"\\0"`（代码中转义是字面展示）并通过真实验收；两次提交历史都保留。

合并主线 `40e0d31d4dc60108b371f19e8fe1e9607a3c7f78` 的 **11/11** Actions 全部 `completed/success`，包括 QUEST32 专项 run [42491217829](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42491217829)、job 128763807893，确证五项新 unittest 运行步骤与公开重算程序步骤均成功。六份已发表文件实际 Git blob及各 11 项 workflow ID详见[不可混淆的验收收据](../../research/recovered/STONEAGE-QUEST32-PUBLICATION-ACCEPTANCE-R1.json)。原 `docs/CURRENT-STATE.md` 的完整历史 blob `c89e0e33537990aa2132b47c40fef49a985a935c` 与首次核查相同，未追加截断、替换或删除。这个补录提交**自身** CI 需按新实际远端状态另行观察，绝不能反过来把此前验收认作补录后运行。Stage A 与下一任务仍按第6节保留。
