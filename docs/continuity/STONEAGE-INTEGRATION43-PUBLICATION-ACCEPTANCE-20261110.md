# INTEGRATION43｜A路线 A6／终点来源限定发布验收（2026-11-10）

[来源边界](STONEAGE-INTEGRATION43-JARUGA-A6-FINISH-SOURCE-BOUNDARY-20261110.md)；[公开派生索引](../../research/recovered/STONEAGE-INTEGRATION43-JARUGA-A6-FINISH-SOURCE-BOUNDARY-R1.json)；[PR #311](https://github.com/chinaneedM/stoneage-rebuild/pull/311)。

本轮从真正最新远端 main cbf85f91753d7bac449305e506ef9fb12c74a588、tree 776505d9455522da7ec530efcb89542341a76c6a 启动，旧 CURRENT 仍为 2,709,173 字节、Git blob c89e0e33537990aa2132b47c40fef49a985a935c。三份已有私人ZIP实际整包SHA、成员CRC核验，QUEST25四个原NPC成员另逐字节SHA/CRC吻合。只公开原 CREATE、任务源条件、位置、已验旧原像素候选的派生数字/SHA关系，原创商业图、 DAT、对白、脚本正文均未公开。

## 远端 PR 与主线真实结果

- PR 候选 9f587543a88095b4406c9d577b15791c007b1cd2，候选 tree 5eb8ded08cdd0f5c5ca9eedcc1a93d15585aa273；仅 5 个预期路径改动：README、1加法连续性、1派生JSON、1专项测试、1专项Actions工作流。
- 27/27 push Actions 全部 completed/success，含专项 [run 42810459934](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42810459934)；19/19 pull_request Actions 全部 completed/success，含专项 [run 42810490916](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42810490916)、job 129810370036，实际执行 Python unittest 回归通过。
- PR #311 在主线未变化时依原候选头合并；新 main HEAD ced6a11b2ef26b52179c9aa385bbe0bb1f1aac08，tree 5eb8ded08cdd0f5c5ca9eedcc1a93d15585aa273 与候选一致。新派生JSON Git blob e37aa8ea0a866d91dcd9dd0bd22e7369f86b3412。
- 合并内容 HEAD 的 27/27 main push Actions **真实全部 completed/success**，含专项 [run 42810666968](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42810666968)。本验收收据自身若无匹配工作流运行，不能假称已覆盖收据提交。
- 合并后逐 Git 文件接口验证 CURRENT 历史 blob 仍精确 c89e0e33537990aa2132b47c40fef49a985a935c，未整体截断或覆盖。

## 验收关闭范围和下一步

本包只关闭加鲁卡环岛 A6 与 A终点的两条 **已知原 CREATE→地图编号/坐标→脚本/证明石/奖品字面**来源关系，保存同源混合2.5与跨来源台湾1.0外观候选区别。旧 I42 的 4000.dat 全图 8603引用中4处无索引、双窗口131/139是**先前预检**，本轮没有重新取得原4000.DAT、解码地图原RD或实际绘画；原客户端运行／NPC原生表现／同官方运营服／原路线可达性／奖励概率与分支语义均未证。

**最高 NEXT：** 原地图 4000 的完整 DAT（SHA256 9d327505c74ccb27b62bcce7259be246c9c4a0477c6ee0fceb78f921e7a0dfa5）或其它真实可取得的同来源地图/角色材料。找到合格4000原件则补图与两窗口，找不到就停止在本次缺口，轮换有来源的其它原游戏内容；不为完成一个美术画面强造数据。Stage A 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，整体完成比例未知。
