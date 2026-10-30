# O12 主线完成验收与原源编号歧义永久收据 — 2026-10-31

## 远端唯一事实源与合并身份

- 仓库：`chinaneedM/stoneage-rebuild`，合并 [PR #70](https://github.com/chinaneedM/stoneage-rebuild/pull/70)；启动主线 `4f0c1bfa22ee06795e15ff0fef44bf1490baa9d1`、原 tree `2035f226120e1975d5ece8c4bd9735bcf75be792`。
- 候选 `7395580a69da314e836d34d92887320363aecf90`，tree `857cea30f1204958afb96e8a448133d2b7d53419`；**13/13 GitHub check runs 实际 completed/success**。
- 合并后的主线 `27d39a0baf6ca3f4c86737af1420c4804c68d324`，tree `857cea30f1204958afb96e8a448133d2b7d53419`，两位父提交分别为上述启动主线与候选；**11/11 GitHub main check runs 实际 completed/success**；合并树与候选树相同。
- GitHub main 6,705项 tree 非截断；完整 `docs/CURRENT-STATE.md` **2,708,031B** 原 blob `20050acf279a01555ab06a381dfcdc936bd381a6` 未改。READ​ME仅追加来源索引，无历史删减。
- 本收据后续纯文档提交与已核实的合并提交是**两个不同 HEAD**，不得将上述 11/11 直接冒称该收据自身重跑 11 次。

## O12 原 source-qualified 新贡献

1. 实读台湾 Waei/JSS v1.0 零售保存包中原 `sa_3.exe` 425,984B SHA256 `cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a`、原 `soundaddr_1.txt` 2,873B SHA256 `d8d2bee5e424be75b35cc4b8a1ac10d398f7fd53e98035ba6980e9e4dc9b389f`，不使用其它时间或地区源码冒充。原 EXE 未执行。
2. 原 .data 中113个不同SFX路径、11个不同BGM路径；声源地址表114行，唯一没有出现在上述EXE明文字面量的原表名称是 `sak_98.wav`。这个否证只覆盖静态明文集合，不覆盖动态构造路径或间接读取。
3. 从原机器指令得到 **102 条有精确立即数编号/字符串VA读取/同栈目标地址写入的三联证据**，独立 GNU objdump 102/102 三条指令一致；另11个具体路径使用不同编译生成形式，保留未完全赋号，不借顺序填空。
4. 原 EXE 编译期编号十进制**73→`sae_23.wav`**，其三条原指令VA分别 `0x442B76`、`0x442B0C`、`0x442B1E`。**不同的** `soundaddr_1.txt` 零基第73项为 `sam_18.wav`，一基73项为 `sam_17.wav`。O11 SPR 帧第四字段73进入哪套声音编号、真正有没有声音事件、`10000`语义均仍为OPEN。
5. 私人源 P3H仍仅在用户私人保管及本地工作副本，全部原 EXE、WAV、图片和引擎均不入公共Git。永久派生机器账本Git blob `1d0df7df7fa9d3527407b5282f9304fe507e7f5d`、源验证 `c434078e05d98207bc8be7cb7716f9298fd116b2`、22项测试 `0a882c4915aa4265ddaa0aa16f65f38b900adee2`；工作流 `592641f1c11ebefca2ce58a1da3412408892d54c`。GitHub CI校验**冻结派生摘要而非私人原 EXE**，私有原件静态解析与独立反汇编是本轮本地实测。

## 候选实际成功检查（13/13）

- [source-contract](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146755883/job/124373547520) — `completed/success`
- [verify-o12-native-compiled-audio-numbers](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146755868/job/124373547469) — `completed/success`
- [independent-original-derived](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146742377/job/124373504778) — `completed/success`
- [exact-original-source-negative-gate](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146742258/job/124373504518) — `completed/success`
- [original-native-table-boundaries](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146742330/job/124373504510) — `completed/success`
- [verify-o12-native-compiled-audio-numbers](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146742312/job/124373504462) — `completed/success`
- [full-source-conservation](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146742278/job/124373504437) — `completed/success`
- [original-source-and-boundaries](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146742252/job/124373504277) — `completed/success`
- [bounded-original-map-delta](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146742237/job/124373504122) — `completed/success`
- [bounded-research-review](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146742179/job/124373504075) — `completed/success`
- [acceptance](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146742224/job/124373504048) — `completed/success`
- [immutable-source-and-name-boundaries](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146742197/job/124373504025) — `completed/success`
- [exact-source-report](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146742198/job/124373503992) — `completed/success`

## 主线实际成功检查（11/11）

- [exact-source-report](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146843554/job/124373822240) — `completed/success`
- [full-source-conservation](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146843258/job/124373821362) — `completed/success`
- [exact-original-source-negative-gate](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146843255/job/124373821302) — `completed/success`
- [acceptance](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146843253/job/124373821151) — `completed/success`
- [bounded-research-review](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146843243/job/124373821132) — `completed/success`
- [immutable-source-and-name-boundaries](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146843167/job/124373821064) — `completed/success`
- [bounded-original-map-delta](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146843140/job/124373821003) — `completed/success`
- [independent-original-derived](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146843179/job/124373820983) — `completed/success`
- [original-source-and-boundaries](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146843204/job/124373820958) — `completed/success`
- [verify-o12-native-compiled-audio-numbers](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146843166/job/124373820898) — `completed/success`
- [original-native-table-boundaries](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41146843171/job/124373820836) — `completed/success`

## 继续条件

O12 已有限闭合编译期编号与文件名映射的102条实证，以及与音频地址表的序号分歧。下轮最高O13先查准确**同一原保存版实体主表/客户端事件参数**，不据表项猜宠物/战斗/技能/任务音效；缺件则在22域轮换。原官方客户端可操作世界仍未进入，Stage A 7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED_NONBLOCKING、overall completion percent=null；历史来源所有不可判项继续OPEN。
