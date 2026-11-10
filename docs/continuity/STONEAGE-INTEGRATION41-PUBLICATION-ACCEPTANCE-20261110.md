# INTEGRATION41｜加鲁卡环岛 B 路线主线验收（2026-11-10）

[来源记录](STONEAGE-INTEGRATION41-JARUGA-ROUTE-B-20261110.md)及[派生索引](../../research/recovered/STONEAGE-INTEGRATION41-JARUGA-ROUTE-B-CHECKPOINTS-SOURCE-R1.json)按 8 份原 DAT 连接报名、12 个检查站与终点。12 个换石事件另按原脚本的 TYPE 段序号独立复核了条件、DelItem 和 GetItem。候选 16027 的 ADRN 记录、RD、索引像素、RGBA 和 PNG 摘要亦逐项与 O25 一致。42 张未标记画布的独立重放一致。报名点剩余三个逻辑图号、四处高值引用仍缺可用像素；其余 13 窗口大于 99 的引用有候选图。浏览器启动权限失败已保留，原生游戏运行未取证。

私人图册最终版本为 15,965,774 字节、413 成员，SHA-256 `17c731bc35eff196ece90709772bda8409d038ce6ac95fa5a06553ad4a846e3c`。保存后按同一版本重新取回，整档 SHA 与全部成员 CRC 均一致。第一版更正了对黑色像素的说明，图块、场景和任务关系没有改动。原图、原 DAT 与私人图册不进 Git。

## 精确 GitHub 验收

- [PR #309](https://github.com/chinaneedM/stoneage-rebuild/pull/309) 的候选 HEAD `f7a7d3e4a09696fb000c0645190b341ae359908c` 有 19/19 pull_request 与 27/27 push Actions completed/success。专项 [PR run 42804857874](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42804857874) 及 [push run 42804853267](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42804853267) 成功。
- 合并内容 HEAD `62a37dfd2b912add43c8c03f2985a6f42af6cad4`、tree `8363bca612709be6db9334eccf2bf5cfbf2d21be`，直接父提交为启动 HEAD `dbbd2161bc99f1c3710cd86fe6270d5192550e0b`。合并 tree 与候选 tree 相同，完整递归树 7,706 项且未截断。仅五个预期文件有差异，逐文件 Git blob 与本地一致。派生索引 blob `785465c422e2af4e7a1778dde332f43bfb5e57c7`。完整历史 CURRENT 仍为 2,709,173 字节和 blob `c89e0e33537990aa2132b47c40fef49a985a935c`。
- 内容主线 27/27 push Actions completed/success。专项 [run 42805032604](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42805032604) 的 job 129791859809 实际成功执行 7 项公开来源契约测试。此验收收据提交的 Actions 单独观察。

**最高 NEXT**：限定复核 24307、24309、24310 在同保存混合 2.5 ADRN/REAL 的原记录和完整 RD。如果无法取得或复验原字节，记录准确缺口并轮换。Stage A 仍 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 暂停，总体百分比未知。
