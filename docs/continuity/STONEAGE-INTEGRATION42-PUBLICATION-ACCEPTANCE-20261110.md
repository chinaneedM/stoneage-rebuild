# INTEGRATION42｜报名点补图与地图 3000 全图主线验收（2026-11-10）

[来源记录](STONEAGE-INTEGRATION42-JARUGA-REGISTRATION-ORIGINAL-TILES-20261110.md)与[公开派生索引](../../research/recovered/STONEAGE-INTEGRATION42-JARUGA-REGISTRATION-ORIGINAL-TILES-R1.json)记录了三个真实混合 2.5 RD 和报名窗口四处原引用。窗口高值图块从 122/126 到 126/126。9,569×7,185 全图的两套画布重放一致，实际覆盖 10,851/10,853 处高值引用。再次独立全表扫描时，22413 在逻辑号字段无记录。同号物理记录实际存在且可双解码，其逻辑字段为 0、原 RD SHA-256 为 `06937ebee20ac8505f87a9966192d28b688c767043e582055a30c4790d6d3e83`，没有将其套给两个原格。原生层序、实际调色、碰撞和任务运行仍待证。

私人补证包 23,537,054 字节，23 成员，SHA-256 `df4b41a084483024fda035b05a31cd6940e1c28c883d53039ee6abc2f148dcff`。第二次完整重放的 ZIP 和派生报告逐字节一致。保存后回读整包 SHA、23 个 CRC 及两张主图尺寸一致。12 处本地图片或链接通过静态检查，云端浏览器限制本地 file URL，浏览器显示未实测。原商业图、原 DAT、原 RD 与观察包未入公开 Git。

## 远端后验

- [PR #310](https://github.com/chinaneedM/stoneage-rebuild/pull/310) 候选 `3d7afb22985b034b2678c9c993c27ea29438db72` 的 19/19 pull_request 与 27/27 push Actions 全部 completed/success。专项 [PR run 42806935890](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42806935890) 与 [push run 42806931939](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42806931939) 实际通过。
- 合并内容提交 `95e808657bd07cc6c3808357a4905a2e070af121`，tree `b7a5409c4c46f916a49def7a7537d55395c868a5` 与候选相同，完整树 7,711 项且未截断。仅五个预期文件发生变化，逐文件 Git blob 与本地一致。公开派生索引 blob `f87b5187dee37facaacd35f63132346986f9e1f9`，历史 CURRENT 仍为 2,709,173 字节、blob `c89e0e33537990aa2132b47c40fef49a985a935c`。
- 内容主线 27/27 push Actions 全部 completed/success。专项 [run 42807124423](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42807124423) 的 job 129798992281 实际执行七项公开测试。收据提交自身的运行情况单独观察。

**最高 NEXT**：地图 4000 与 A 路线 A6、终点。已从同 RAR 直接核原 DAT、CREATE 及两脚本。A6 位于 (63,66)，终点位于 (54,47)，两窗口高值引用分别 131、139 次。已按唯一逻辑索引预验联合 136 种地图图块及人物候选 16068、16027 的原 RD 双解码，可接着制作场景和原任务资料。地图 4000 全图另有 4 处待证引用。Stage A 维持 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 暂停，总体百分比未知。
