# WORLD31 附加原表差异｜另存回复道具候选不等于实际结算（2026-11-06）

## 接续位置

本包从远端 `main` `4633e4ad6c68013496c3d4ba32d543e1c74c68a6`、tree `2015025649de83468f4d73093bb5fda6bc0aa907` 启动；已重新读取协议、历史 `CURRENT-STATE.md`、README、设计决定、历史来源与最新 WORLD31。WORLD32 仍是最高优先：同保存原 GMSV `BATTLE_MultiRecovery` 普通单目标体力／气力实际结算与目标过滤，不得用静态模型替代 x86 回放。历史 CURRENT 原 blob `c89e0e33537990aa2132b47c40fef49a985a935c`（2,709,173 字节）保持原样。

## 本包实际新增的原资料关系

复用此前已经按原源 SHA 验收的个人私有 `StoneAge-ITEM01-private-two-itemsets-832-original-RD-icon-observer.zip`（ZIP SHA-256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`）中的原始表**派生**目录 `private-full-catalog.json`（SHA-256 `0438c4fc9bf945223d46c24e9d374de436f2ac981c23fa282776281c2e772e60`）。对实际 ZIP 成员进行全 CRC 与完整 SHA 校验；目录保留每 ID、每版本 94 个原字段、原来源行号及行 SHA。两个原物品表的整文件 SHA 与先前 ITEM01／WORLD31 记录相符。此包不是重新取得原 `gmsv.exe`，也不冒称本轮直接重解原 RAR 内两份物品表。

- **配置选中 `itemset.txt`**：`ITEM_useRecovery` 原物理记录 644，严格普通 `體` 389、`氣` 147、`體氣` 48、其它 60。与 WORLD31 的 644 分类完全一致。
- **另存 `itemset0710.txt`**：同名回调 663，普通 `體` 395、`氣` 149、`體氣` 48、其它 71。
- **同 ID 真差异**：共有 644 个同 ID 回调，两源各 94 个原字段逐列完全相同；选中表独有 0，另存表独有 **19 个原 ID**，其中严格体力参数 6、气力 2、其它 11。19 条完整保留原行 SHA、选项 SHA、原场景／目标数值及原物理行号，仅以版权安全派生字段公开。相同的回调名称或 ID 不证明当时的加载、使用或发布。
- **语义反例**：11 条其它参数含非普通属性标识、带空格的数值、等级调整语法及空选项；不能将全部 19 条表行算作新增可用治疗物品，更不能把它们加入配置选中表或当作战斗结算的证据。

公开范围：`research/recovered/STONEAGE-STAGE-A-WORLD31-ITEMSET-VARIANT-R1.json`、来源限定复核器、无私有文件依赖的测试与工作流。本包复核器若有**确切**上述私有 ZIP 可以直接重算派生索引；公开 Actions 只验证其受限摘要及 WORLD31 已存收据，不会下载/执行原件。没有原始物品表全文、游戏资源、程序或私有 ZIP 进入 Git。

## WORLD32 原始结算仍 OPEN

本次会话可访问的原件及私人资料里未取得 WORLD31 所用保存 RAR 或其中完整、SHA 合格的 `gmsv.exe`。WORLD31 的首次属性写入预检仍不足以证明 `BATTLE_MultiRecovery` 最终增量、目标存活条件、通知或扣物。缺源止点为**同一原 `gmsv.exe` SHA-256 `d5b08dbcbf9e8736ba8598e38e5901f123d2bff544a9cae53a9ff88ce1971e00`**；恢复可核的原字节之后，才可沿已定位 `0x548eb0` 和 `0x5185e0` 的有限窗口完成原 x86 单目标体力/气力两条路径。这个具体缺件不构成 WORLD32 已完成或永久不可能完成。

项目状态保持 Stage A 7 PARTIAL + 2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、整体完成率未知；无原程序执行、无真实游戏结算、无台湾 1.0／大陆 1.82 同版对应证明。下一最高仍为 **WORLD32**，有合格原件才继续；在等待来源期间，只推进其他有真实原资料增量的机制内容，不扩大账号／网服／新引擎或体验优化。
