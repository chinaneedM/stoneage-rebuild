# 2026-10-29 — SCENE16 室外落点近邻 NPC 原件资格入口

## 核对起点与证据状态

本轮重查远端 main HEAD `52a44bd9baf6dfe52ee56ff373a99c97117cc1fd`、tree `bfb0e6c351794860f3bdb01e3f96521637154bf9`、最近提交、Actions、协议、完整原生 CURRENT Git blob，读路线、22域、SCENE15、R18 原成员清单。上一轮 SCENE15 已认证一条 **现代离线场景** 1001(10,15) → 1000(63,99)，但原客户端尚未进入世界；本包不能将人工切场景变成原生 NPC 交互。

最高 NEXT 的调查目标为 1000(63,103)，这只是待取证坐标，**不是本轮从原始 NPC 文件新读取的出生位置**。主线完整 R18 原件目录已有 `npc/genout/1000npc_m.create` **4,413B**、SHA256 `c9b000a836b0aae3d88358097039f1beea020d92ba84f6ccc338bb54bc478240` 的单一记录。该目录是原混合保存服务端成员的全量文件级 SHA 见证，不是原文，也不认证官方台湾1.0同服或初代内容。当前可读公开 Git **没有该私有原脚本的正文**，因此本轮不能实际验证 63,103 的 NPC 身份、名字、参数或原图，更不能声称已观察其对白/动作。

## 可执行资格入口

新增 `tools/stoneage_scene16_nearby_npc.py`。不提供私有输入时，它只读 Git 原目录和上轮已验证的出口记录，明确报告 `SOURCE_NOT_SUPPLIED`、`matched_count=null`；不会凭目录/SHA猜出 NPC。

若将来原私人实物可访问，调用：

```sh
python -m tools.stoneage_scene16_nearby_npc --create /private/npc/genout/1000npc_m.create --template /private/npc/genout/npcgen.template
```

工具先校验 **完整原成员长度与 SHA**；模板同样限定原 4,950B/SHA `0c5a58d5e31cafd3b58ccc1fa88fee7d1f95d12c0b87b04db9f06fea3b2a4df3`。然后按原创建块序解析：floor1000 且 borncorner 四数矩形包含(63,103)；返回所有匹配并明示0/1/多候选，不 last-wins；原模板只有**完整精确名匹配且仅一个**才给函数类别。数值/源块 SHA/文件段与姓名原字节 SHA 可出公开派生报告；原文字、脚本、对白/素材默认不公开。周边坐标、邻门、同名/同号、后期混合源的同包关系均不能当作原生可交互资格。

当前工具 **不下载** RAR 原大包，不读取原进程，也不接伪像素到 SCENE15；若私人源缺失，停在精确来源缺口，不再连续扩长全 NPC 或 EXE helper。提交的15个单元测试覆盖：原目录/出口联接、缺件状态、假来源及“仅相同大小”拒绝、相邻坐标/错误楼层拒绝、范围界限、重复字段/残缺块、误模板联接和不发布原姓名。专用 Actions 只测派生资料和合成反例；**CI通过不能当原 NPC 已取证**。实际 CI 结果须在发布后验再写，不能提前自报。

## 复原边界与后续优先级

这是一轮有界取证资格与来源复核，不是新增已恢复 NPC；故本包不递增具名 NPC、任务或可见地图数量，亦不增加总体完成百分比。原 CURRENT 完整历史全文、DD-028四档、Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、总体进度 null 均不改。

**下一优先任务**：若能取得保管中与 R18 SHA 精确相符的 4,413B 原成员，进行一名近邻 NPC 的原块—模板—图号/实际可见互动最小联接；若继续不可得，按协议13的有界止点轮换到22域其他真实材料，不把源资格工具虚报为场景复原。
