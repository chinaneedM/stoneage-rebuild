# INTEGRATION64｜四属性宝珠／结晶石／月光手镯原来源联接：正式验收（2026-11-11）

## 真实主线、原历史与私人源保管

从新远端 `main` `c149209bebf22e45f99929c01400b742f0748ab8`／tree `1b1ed88e1ecfddfb8d2ee7db6b609a6210ae16ec` 及仓库连续性协议重新核对。本轮基点原主线 `9c1208d0ea9deed4a420e1d34ba9817e58b2309d`／tree `4356fbcb66ecca441e67c6f1152b1fa6920bc131`。现已按 PR [#332](https://github.com/chinaneedM/stoneage-rebuild/pull/332) **squash 合并**原候选，主线原 tree 精确等于候选 tree，五个公开改动文件已核；原大 `docs/CURRENT-STATE.md` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 未动。

原始来源 SHA/ID、4 个 TYPE、5 件源条件物品→1 件源奖励、分离的 REQUEST 结晶石、4 个传送数字、6 张另一载体真实 RD 候选、来源 UNKNOWN 和旧 QUEST01/ITEM01/MAP09 交叉证据，详见[本轮源文档](STONEAGE-INTEGRATION64-HOUGYOKU-SOURCE-20261111.md)和[永久派生数据](../../research/recovered/STONEAGE-INTEGRATION64-HOUGYOKU-SIX-ITEMS-ORIGINAL-SOURCE-R1.json)（blob `e30d42ef610f76b427777318bdc41261e663f7a7`）。原NPC和原 itemset 的两份私人来源 ZIP 本轮确实读取及全 CRC；原出处不冒充早期官方同版本部署，未运行原客户端、服务器、NPC 或传送。私人 21 成员新包在 Library `/石器时代/StoneAge-INTEGRATION64-Hougyoku-original-source-private.zip`，长度 **15,469B**、SHA256 `ef6ed11dc1b25c13e41190d08d3910fc5adbdeb37231d1b5d5c8bfdccd3afa94`，**已从独立 Library 路径重新读回、全 SHA 相等、21/21 CRC 通过**。原商业文本、原物品行、原图全为私人，不入公开 Git。

## GitHub 实际 Actions／主线合并后验

| 固定验收对象 | 观察到的远端事实 |
|---|---|
| 候选分支 | `agent/stoneage-integration64-hougyoku-20261111` |
| 最终候选 HEAD | `3a2314a8b82b47ac82214415daf532d2a9d5308b` |
| 最终候选 tree | `1b1ed88e1ecfddfb8d2ee7db6b609a6210ae16ec` |
| 同 HEAD 候选 Actions | **46/46 completed/success**；push 27/27、PR 19/19，实际逐一核对 |
| 候选专项 push | [run 42984347067](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42984347067) / job 130401858024，成功 |
| 候选专项 PR | [run 42984371151](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42984371151)，成功 |
| PR #332 | 合并时原 base SHA 未变、mergeable=true、mergeable_state=clean，五项合法公开改动 |
| squash 合并 main HEAD | **`c149209bebf22e45f99929c01400b742f0748ab8`** |
| 合并 main tree | **`1b1ed88e1ecfddfb8d2ee7db6b609a6210ae16ec`**（与候选完全相同） |
| 合并后 main Actions | **27/27 completed/success**，不是拿候选结果替代 |
| 本轮主线专项 | [run 42984499374](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42984499374)，成功 |

完整 **46+27** 个具体成功 run ID 已另存[机器回执](../../research/recovered/STONEAGE-INTEGRATION64-PUBLICATION-ACCEPTANCE-R1.json)，不能把此前的 I63 成功、旧 SHA 或另一提交 Action 计入。本轮新测试文件共有 8 项，其中旧 QUEST01 脚本/CREATE 来源及 TYPE、ITEM01 两表行 SHA、MAP09 目录边界在公开 CI 验证；**CI 不访问私人原脚本和原 RD**，私有源 SHA/CRC 的证明在独立私人实读环节，两个证据级别不能混用。

## 状态／下一任务

原 `CURRENT` 整文件原封不动。Stage A **7 PARTIAL+2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，overall_percent **null**。本轮的 NPC、六件物品及独立图候选**静态关联 SOURCE_BOUNDED_STATIC**，原游戏任务完成、掉落/消耗、实际触发和四目标 Warp 执行仍 OPEN，不能宣布实机复原完成。

**最高 NEXT：** 对 22 域重新做真实源查重，只选其他原 NPC/地图/任务物品/宠物中确有可重放原字节、又尚未被 O/QUEST/INTEGRATION 专项完成的游戏内容，避免重复本次宝珠链、I63 水壶、O70/O74 委托等；不转新单机引擎、网络服务或体验开发。**本验收回执本身的新提交的 Actions 尚未观察，不能预称通过。**
