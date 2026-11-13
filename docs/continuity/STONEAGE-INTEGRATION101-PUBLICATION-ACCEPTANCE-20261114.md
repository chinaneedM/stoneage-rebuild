# INTEGRATION101｜加特洛／美魯娜原居民和原对白正式来源/CI验收（2026-11-14）

## GitHub精确候选与正式主线

- 真正内容 [PR #385](https://github.com/chinaneedM/stoneage-rebuild/pull/385) 合并。候选 HEAD `fc2ebede449831cfdaa02fbd21c83b0e3a59cd85`／tree `e4bd005c9cec4e0737e43ce7093033ca2c980785`，原主线 `990dbb33545bcf28a9fff3baa92a92b51cb6fb42`。合并产生正式主线 `1012c30050855341554e1722e017b452c4f76541`，与内容候选 **Git tree完全一致**。
- 候选同SHA实际 **3/3 Actions completed/success**：专项 PR [43462904898](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43462904898)、O11 [43462904559](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43462904559)、O12 [43462904512](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43462904512)。专项 job `132014230588` 实际日志 **`Ran 7 tests / OK`**。本次没有候选push对应专项run，不能凭空补一条。
- 主线独立 push [43463111176](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43463111176) **1/1 completed/success**，真实job `132014980609` 日志 **`Ran 7 tests / OK`**。候选成功不混作主线成功。
- [永久机器收据](../../research/recovered/STONEAGE-INTEGRATION101-PUBLICATION-ACCEPTANCE-R1.json)保存全部4条精确run ID、原HEAD/事件、三个既有/专项名、两个专项job及日志、4个本批公开内容Git blob及两个原公共索引blob。**本收据本身的CI必须按其后续实际SHA独立验证，不能提前宣布通过。**

## 原始历史内容真实保管，不是原版运行

- 私人已保管后期社区mixed2.5 NPC ZIP **995,176B/SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，2,205/2,205 CRC 成功**；重新真实读到 `npc/genout/garunaev1.create` **4,992B SHA256 `7c742b85fafda010df235b09660265668210ca0f6e57030c98801394f4d895da`**。源CREATE逐真实byte-window SHA **28/28**与旧CHAR01 Git记录同；**27/27份原对白处理文件**（1,941原字节）逐完整SHA和CP950往返同；额外1条原CREATE内联字面独立哈希。另一同名 `npc/giiru/event/garunaev1.create`是不同路径/1,983B原文件，不重计。
- 四原楼层 **31001/31002/31101/31102** 旧MAP04 DAT各具50×50原文件SHA/头部记录，28源NPC座标在尺寸范围；原DAT本轮没有重新读出字节或测试碰撞，**不称四张原地图实际运行**。28条配置的26个图号仅是数字别名，不是26幅新解码原2D图。
- 原商业源和27份原文、私人只读研究HTML（28张原对白资料卡）一并存于私人 Library **11,102B ZIP / SHA256 `cb2cc53c4d7a42ea386e6f69761460f953cb3066b9584b81e181db9b5d74b45e`**，上传后从Library**独立取回全字节相同，30/30 CRC**。HTML静态结构已验；本轮本环境浏览器没有可用Chromium可执行文件，**不宣称浏览器成功运行**。公开Git只放数字/来源SHA、说明与公开测试，不发布商业原对话、原CREATE、原图、原DAT。
- 仅能判定社区后期保存源有NPC居民、住宅、矿石相关文本，不能上升为早期官方TW1/大陆1.82/JSS1999部署、真实NPC发言、采矿掉落规则或可玩复原世界。

旧 `docs/CURRENT-STATE.md` 保留原样 **2,709,173B Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`**。Stage A **7 PARTIAL + 2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、overall百分比未知。

## 止点和 NEXT

INTEGRATION101 **SOURCE_BOUNDED_ACCEPTED**，不等于GAMEPLAY_VERIFIED。停止对已认证28条居民反复细拆，后续转另一具有实物新字节或源2D内容的宠物／NPC／地图／任务家族，只有获得对应原生运行或真正更早版本源证时才重开相应结论。
