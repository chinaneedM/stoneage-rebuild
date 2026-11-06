# WORLD34-R3｜场外回复道具的入口、属性写入和消耗

从 GitHub main `56e4bfb6bc534e15fd7b3087900d0e4c0f1fddce`、tree `0da02699198c822717b55faeaae4905f413e7c5f` 接续。启动时远端树 7,259 项，HEAD 对应 11 项 Actions 全部通过。历史 `docs/CURRENT-STATE.md` 完整 2,709,173 字节，Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`。本页追加当前状态。

## 原件资格

私人保存的社区混合 2.5 RAR 完整 361,255,180 字节，SHA-256 为 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`。从公开 UnRAR 源码提交 `160dcb5c9c1babbbdd3f0f1fc78cf48a7f8150cf` 构建 7.30 beta 1，解出完整 `gmsv/gmsv.exe`。成员 1,897,867 字节、RAR CRC 及完整 SHA-256 `d5b08dbcbf9e8736ba8598e38e5901f123d2bff544a9cae53a9ff88ce1971e00` 均与历史见证相符。配置、选中的物品表、指定主程序路径的客户端也重新核对了成员 SHA、CRC 及原压缩段见证。档内另有同名客户端，SHA 校验拒绝该成员。

完整程序的四个装载段 SHA 与 WORLD34-R2 的四段全部相同。取与 R2 相同长度的 1,835,008 字节前缀，整段 SHA 仍不同。R2 的 libarchive 解档失败记录继续保留。本轮回放使用全文件合格的程序。

## 场外使用结果

从 `lssproto_ID_recv` 输入已解析的命令参数，执行原目标解析、`CHAR_ItemUse`、原函数指针取值、回复回调、人物整数访问器、`CHAR_DelItem` 及物品实例释放。命令中目标 0、1、6 分别取本人、宠物槽 0、队伍槽 0。人物初始体力 100、气力 10，上限 1000／100。以下是随机输入两端的夹具**写入后**数值。

| 原物品 ID | 场景／目标字段 | 客户端场外场景检查 | 本人或队友写入 | 宠物写入 |
| --- | --- | --- | --- | --- |
| 1232 | 1／2 | 拒绝 | 体力 640／760 | 体力 640／760 |
| 12530 | 0／1 | 通过 | 体力 388／452 | 体力 388／452 |
| 12555 | 2／1 | 通过 | 体力 266／303，气力 28／32 | 体力 266／303 |

所有 18 次有效目标与随机端点组合均走过回调并返回命令调用方。原指令写入属性，背包第 7 槽由物品实例 0 清为 `-1`，实例存在位和活动数各由 1 变为 0。场景和目标字段在受测服务端路径未被读取，覆盖物品整数键以及实例内存偏移两种观察。道具 1232 的差异限定为客户端场景检查与直接调用同包服务端入口之间的差异。两个子实验分别执行，未通过客户端发送这一命令。

额外控制组确认，接近上限时封顶并消耗道具。三条原行的 `useaction` 字段为空，夹具分别给整数键 46 值 0 和 `-1`，动作通知调用有差别，回复和消耗结果一致。空背包槽、施用者工作键 64 或战斗模式非零在回复之前返回。回复许可由夹具置否时，已进入回调，随后返回并保留道具。

**无效目标止点。** 输入目标 11、宠物槽空、队伍槽空都将 `-1` 传入 `CHAR_ItemUse`。其场外路径在调用回复回调前使用 `CHAR_getInt(-1, 0x36)`。原 `0x42dba8` 尝试读取角色表之前的地址，受保护夹具在此停止。九次均没有观察到回复或删物，也没有执行到命令返回。原进程中的相邻内存与运行后果仍待证。

## 验收和下一优先

[派生收据](../../research/recovered/STONEAGE-STAGE-A-WORLD34-R3-FIELD-ITEM-REPLAY-R1.json) 固定源成员和指令窗口哈希、夹具输入、45 次轨迹及保护边界。连接身份、位置更新、回复许可、参数重算、随机数、C 库和通知等调用由夹具提供。属性、背包和物品实例变化发生在隔离内存。Unicorn 2.1.4 和 1.0.3 分别重放，派生收据逐字节相同，SHA-256 `4ffffa5e0c585e2e50010e0572ed1ee4c0064d93f9c0730630332577f85b7550`，Git blob `d0f728857a2879e4d9e24856cdbc02f3fa8317b3`。40 项相关本地测试通过。公开测试只核派生结果，原程序和原表留在私人范围。复算命令如下。

```sh
python -m tools.stoneage_world34_field_item_replay /private/preserved.rar /private/extracted
python -m unittest -v tests.test_stoneage_stage_a_world34_r3_field_item_replay
```

**最高 NEXT WORLD35｜捕捉增益道具。** WORLD19 已索引配置选中表中 26 条 `ITEM_useCaptureUp`，历史捕捉核心已有后代源码模型。对照本轮同包原程序，静态预检已定位 `ITEM_useCaptureUp` → `ITEM_useCaptureUp_Battle` → `BATTLE_MultiCaptureUp`，以及后者写角色工作键 `0x20`。下一步核实实际原参数如何变成该字段增量，并在原捕捉函数中确认该字段的消费位置或具体缺口。单独保留最终捕获结果的证据等级。Stage A 仍为 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 暂停，整体完成率未知。

## 主线验收与 WORLD35 预检

- [PR #216](https://github.com/chinaneedM/stoneage-rebuild/pull/216) 候选 `623447450feb767c7de08fb5ac4936cf579344a1` 的 14 项 Actions 全部成功。[候选专项](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42201734535) 及推送专项均实际执行 WORLD34-R3 测试。
- 合并提交 `bbdcbbb3e9a20d1879e4e4692f6486ebd98e5f24` 的完整 tree `731b339d7e9b2244625a03b855a6a259b98864fa` 与候选及本地验收一致。主线 11 项 Actions 全部成功，[主线专项](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42201821618) job `127838689263` 的 WORLD34-R3 步骤通过。完整历史 CURRENT 重新逐字节比较一致。另用本轮认证原件重新生成 WORLD33 派生报告，与原归档逐字节一致。
- WORLD35 同包原 `BATTLE_MultiCaptureUp` 在 `0x54cdae` 读取角色工作键 32，在 `0x54cde1` 累加写回。同包 `BATTLE_Capture` 在 `0x5389ca` 读取施用者同一键并加到已经算好的分数，`0x5381ea` 请求归零。对后半段做五次隔离原指令预检，直接设定基础分，工作字段访问和随机数由夹具供给。随机输入 0 时，基础分 1、增益 0 的比较标志为 0，增益 1 则为 1。基础分 40、增益 12 时分数为 52，目标工作键 43 非零的受测值 1 则为 67。基础分 90、增益 20 时封顶 99，在最大随机输入下比较标志为 0。五例都发出将施用者键 32 写回 0 的请求。两版 Unicorn 结果一致。
- 预检源窗口 SHA-256 为 `0x5389ca..0x538a9e d434e468da730746d14b44371555a8c1584392e17566a56b676966faa4b6f48f`、`0x5381b9..0x5381ef d472fedc95aedf123ad35f4782f48cc8d55888ebc6b803140c800ebdad79c69d`、`0x5a8004..0x5a8018 c2f7adf82fab4f375d301673e7786ac4a0866733eb34a4b6f96fd41e46949e54`。道具增益写入静态窗口 `0x54cd32..0x54cde6` 为 `b10b718c6aed0b1dc2a07a41bb8bbcbda10ad5fe5feff9c278106e4d357619fe`。下一步仍为 WORLD35，重点在 26 条原道具参数经原指令生成键 32 增量的路径。预检在归零调用之后、取得宠物之前停止。

**2026-11-06 加法订正。** 本页原先将动作描述符序号 62 当作物理列，误记三件道具的 `useaction` 为空。原加载器有 15 项双列描述符，实际读取物理零基列 77，原值为 1232 −1、12530 6、12555 7。WORLD35 使用正确动作值重跑 18 个有效用例，动作通知调用有差别，属性、返回和扣物结果逐项一致。[订正与完整核验](STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-35-CAPTURE-ITEM-SOURCE-20261106.md#world34-r3-动作列订正)
