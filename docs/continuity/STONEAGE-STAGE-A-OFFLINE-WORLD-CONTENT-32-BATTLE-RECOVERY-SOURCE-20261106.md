# WORLD32｜战斗中单目标体力与气力回复

本轮从 GitHub `main` `6912708f67a71c18380dd6a2bad1d5bf51440fb5`、tree `2e33d16443e1c6caf53079085abae005d85d1ce9` 启动。核对候选 PR #211 的三项成功 Actions 和上一次内容主线的十一项成功 Actions。启动 HEAD 是文档验收收据，主线 Actions 列表未显示它的独立运行。完整读取 2,709,173 字节的历史 `docs/CURRENT-STATE.md`，原 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 以原样保留。本篇接续 WORLD31 另存物品表记录所留的原件缺口。

## 来源与回放

取回项目私人保存的 `stoneage-preserved-mixed25-original.rar`，361,255,180 字节，全档 SHA-256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`。用 UnRAR 7.30 beta 1 解出唯一 `gmsv/gmsv.exe`，1,897,867 字节，全 SHA-256 `d5b08dbcbf9e8736ba8598e38e5901f123d2bff544a9cae53a9ff88ce1971e00`。成员头、压缩段、CRC32 和解出成员 SHA 均与 WORLD31 的见证相同。该保存件为社区混合 2.5 样本，早期官方发行或实际部署的对应关系仍待同版来源。

从该完整映像映射经过核验的原始 x86 函数窗口。沿 `BATTLE_MultiRecovery` 执行 `BATTLE_MultiList`、`BATTLE_TargetCheck`、槽位映射、无骑宠分支、属性请求及战斗缓冲追加，正常样本走到函数返回。人物状态、标志读取、属性写入、`CHAR_CanCureFlg` 结果、随机值与 C 库调用均由夹具提供。战斗缓冲使用原格式串和原追加指令，格式化、内存复制由夹具实现。未启动客户端或 GMSV，也未实扣背包、发送网络通知或观察实服回合。

复用 WORLD31 的物品回调回放，重新取得 116 种普通参数的完整结算入参，对应 583 条物品原行。保持种类、基值、百分比和两项效果字面，换用明确的战斗编号和目标槽位夹具。116 种参数归为 79 组实际结算请求，每组用随机输入 0 与 2,147,483,647 验证，共 158 次结算，另有 18 个边界及代表样本。公开 [派生收据](../../research/recovered/STONEAGE-STAGE-A-WORLD32-BATTLE-RECOVERY-SOURCE-R1.json) 保存源窗口 SHA、夹具与完整观察，原程序和原档留在私人范围。

## 普通单目标结算

- **目标过滤。** 受测目标须有有效角色索引，战斗状态字段非 0 且非 5，标志 8 为 0、标志 1 非 0，体力大于 0。原请求槽位符合条件时保留它。原请求槽位不合格而同侧仍有候选时，原程序用随机值取模 10 访问同侧候选数组，落到空项时重取。两侧分别回放到位置 0 和 10，另验证随机输入 9 落空、10 命中后才调用回复量随机数。
- **体力和气力。** 无骑宠且非百分比的受测路径，体力写角色字段 10、按工作字段 13 封顶，气力写角色字段 11、按工作字段 14 封顶。体力分支先查 `CHAR_CanCureFlg`，拒绝样本保留已追加的效果记录，但没有回复随机数、属性写入或回复量记录。气力分支没有调用该检查。
- **数值与记录。** 这两条分支按相同的 0.9／1.1 常量取随机增量，再对属性写入应用上限。战斗缓冲的 `BD` 数值保留截断前的随机增量。已经满值的样本仍请求写回上限，并追加对应 `BD` 数值。

| 回放请求 | 随机输入 0／最大值时的增量 | 接近上限的实际增量 | 同次记录的增量 |
| --- | --- | --- | --- |
| 体力基值 320 | 288／352 | 980 → 1000，实际 +20 | 288 |
| 气力基值 25 | 22／27 | 95 → 100，实际 +5 | 22 |

**同侧空列表边界。** 目标为 17 号槽，体力为 0，对侧 2 号槽仍有效。原 `BATTLE_MultiList` 返回 `-1` 并走诊断写入，但调用方预置的两个列表字没有被改写。原调用点下一段直接传递列表地址，未检查返回值。本次在调用方使用该列表前停下，后续写入、实服后果仍 OPEN。普通物品回调中的结算调用与其后的删除调用位置保留 WORLD31 证据，WORLD32 未将整条命令、库存和实战状态连起来执行。

## 复核与下一优先

原函数和两个关键属性写入路径另用 `nm`／`objdump` 核对。公开测试用独立算术核对 158 次写入，并检查目标、满值、拒绝和空列表反例。Unicorn 1.0.3 重放两次，报告 SHA-256 均为 `508ac852e1ce694099beb69be84b20e624fbba2ea79fd1de9cdf13d5a72c35f4`。Unicorn 2.1.4 复跑全部观察，除版本字段外报告逐项一致。备齐原档、原程序和 Unicorn 后可重新生成报告。

```bash
python -m tools.stoneage_battle_recovery_source /path/to/preserved.rar /path/to/gmsv.exe
python -m unittest -v tests.test_stoneage_stage_a_world32_battle_recovery_source
```

**最高 NEXT WORLD33**。先核同一保存版的战斗物品命令入口如何读物品表的场景／目标两个字段，优先拿 WORLD31 已有回复物品作为见证。目标是给出一个有实证的允许／拒绝对照，或明确缺少的客户端或服务端判定。WORLD32 的无骑宠普通单目标结算在以上夹具范围内已有原指令证据。骑宠、群体／特殊回复、空列表下游和真实扣物仍待证。Stage A 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，整体完成率未知。

## 主线终验与 WORLD33 预检（2026-11-06）

- [PR #212](https://github.com/chinaneedM/stoneage-rebuild/pull/212) 的候选提交 `a4cd99f21337aeea2e0cae8963d1ece500d64128` 共 14 项 Actions 成功（3 项 PR、11 项 push）。[PR 专项](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42161765497) 的 WORLD32 测试步骤通过。
- 内容已合入主线 `ab253883df2197ac04aedfddd51fee0f6c7a707a`，tree `b64ef8497e0cde1d80067f89a2a89ccf574da452` 与本地和远端候选一致，主线 11 项 Actions 全部成功。[主线专项](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42161887394) job `127709250262` 的 WORLD32 六项公开测试通过。历史 CURRENT 完整字节核同。
- 本地 138 项相关测试通过。另从同一原档重新提取 `setup.cf` 和 `itemset.txt`，与原 EXE 重放整个 WORLD31，结果和其公开收据逐字节相同。公开 Actions 校验派生结果，原件回放在本地。
- WORLD33 预检已从 `ITEM_itemconfentries` 核得原零基列 20／21 为 `fieldtype`／`target`，写编译整数键 4／5。`BattleCommandDispach` 的 `0x54649c` 调用 `ITEM_isTargetValid`，下一条条件分支在返回负值时进入拒绝路径。用 180 个夹具隔离回放该检查：两侧的普通槽 7／17 在受测目标类型 0–4 均返回 0，群体选择值 20／21 受目标类型 2／3 和施用者侧别限制，22 要求目标类型 4，23 返回拒绝。改变 `fieldtype` 0／1／2 时，该函数的结果一致。此范围只及单个检查函数，完整战斗命令、场景字段的其它执行位置与客户端限制仍为 WORLD33 的取证目标。
