# CHAR08｜原 ExChangeMan 静态脚本与两份物品主表的源限定审计（2026-11-03）

## 事实来源

按 fresh main `7d7453141cdaadd978f0c65cddbc4f5074a2e5a8` / tree `60aecde2cd68a295a670774cdd844c4cdb82615c` 续接 CHAR07，原私人保存的社区混合 2.5 RAR `361255180B`、SHA-256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5` 本轮完整重读。libarchive 实际遍历 7952 成员，取得原 NPC 子树 2205 文件 / 1930332B，全部成功；复查 CHAR07 已登记的 552 条创建源块与其原参数文件源 SHA/字节长度全部吻合。这是混合保存包的静态源，不是台湾 1.0 官方部署。

在原 `gmsv/data/npc/jaruga/event/event.template` 中，`templatename=changeevent` 原记录对应 `functionset=ExChangeMan`。对 4985 份有效原 NPC 创建块，按原 `enemy=changeevent|file:...` 找到 **315 条创建配置 → 295 个不同脚本文件**；全部 295 条文件路径命中实际同 RAR 原字节，原脚本合计 434873B，全数严格 CP950 可解码。315 不等于 NPC 人物数、任务数或可完成任务数。

## 可核的原脚本静态字段

对 295 个不同原脚本逐源 SHA 核算后，字面 `TYPE:` 值：MESSAGE 769、ACCEPT 494、REQUEST 81、CLEAN 5；`EventNo:` 1348 次、`TYPE:` 1349 次、`EVENT:` 1349 次、`EventEnd` 独立行 1347 次，不得悄悄补足或宣称游戏已执行。源 `GetItem:` 420 行、`DelItem:` 442 行。仅对简单数字 `ITEM=...` / `ITEM!=...` 谓词和 `GetItem/DelItem` 明确的数字槽有限抽取，得 **2878 次字面数字引用、380 个不同物品 ID**。其他 1702 个不符合单一数值比较格式的 EVENT 片段及 11 个非普通数字的 GetItem/DelItem 参数槽保留未解读，不以错误逻辑代替原服务器选择器。

另从同 RAR 直接真实解出两份完整物品主表：

- `gmsv/data/itemset.txt`：3392473B / SHA-256 `a415e78f9aab2e5ea5ca92ecb7430253f7be1ba7c876d6b0bb6d067b1b466688`；13254 条唯一物品 ID。
- `gmsv/data/itemset0710.txt`：3668487B / SHA-256 `6d6d63fda59c6bda2f239fe18c9361b5c9da18c84f678b7cc95bde24544292fb`；13915 条唯一物品 ID。

两表原行均为 94 列，**第 16 列（零基）是数字物品 ID**，第 17 列（零基）是图片号，不可混用。两表共 13254 个 ID，其中原整行 SHA 4303 同、8951 异；后一表独有 661 个 ID。“0710”不能据文件名自动视作官方发布日期或现行生效主表。

交叉 380 个脚本所引 ID：**372** 在两表且原行同 SHA，**1** 在两表而原行不同（18340），**5** 仅 `itemset0710.txt` 有（2054、2391、20570、20571、20572），**2** 两份表均无（2744、2745）。缺记录的判断只限本两份候选表，绝不推导历史物品不存在或运行中出现错误。

## 交付与严格界限

完整的 315 原创建块、295 源脚本、380 数字物品 ID、2878 源行引用之公开可发布衍生索引在本轮本地文件 `STONEAGE-CHARACTER-NPC-MODULE-08-EXCHANGEMAN-ITEM-EVENT-CATALOG-R1.json`，338200B、SHA-256 `a6fca2b5fd096add28e5c6a1ad6a9691c086def6d3f8cb8f5930657c7c350dae`。该文件经 12 项本地校验/变异拒绝通过；**本 Git 节点只永久归档经过实读的汇总数据与源哈希**，由于当前本地→远端文件中转接口报 `container_session_expired`，不能伪称 338200B 全目录已经入库。原始 NPC 对话文本、完整游戏脚本与物品原行仅私人保管，不上传公共 Git。

所有 315 条任务起源继续 `ORIGIN_UNRESOLVED`，不因路径中 `event` 或 `EventNo` 就认定节日运营活动或早期常驻任务。实际服务器逻辑执行、真正玩家到达、原服物品转移、TW1 同版 NPC 名称和图像、原始界面与任务脚本字面分支均未证。仍为 Stage A **7 PARTIAL + 2 OPEN**；Stage B/wiki GATED；R79 PAUSED_NON_BLOCKING；总体完成率 null。保留 `docs/CURRENT-STATE.md` 原全部 2709173B/ blob `c89e0e33537990aa2132b47c40fef49a985a935c`，本记录仅为加法续接。

**最高 NEXT `CHARACTER-NPC-MODULE-09`**：优先复用原 RAR 已保存的 NPCEnemy 实际原数据，做有界的源配置→敌方模板/数值关联并排除既有模型重复；如已覆盖/无资格化原件，则闭合人物/NPC 模块的 SOURCE_BOUNDED_PARTIAL，随后按模块顺序进入地图/场景。当前不开发新石器，也不“优化体验”。
