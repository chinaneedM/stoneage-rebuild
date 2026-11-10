# INTEGRATION40｜成人与四大洞原文件对照、floor2000局部原像素及主线验收（2026-11-10）

性质：**原文件静态证据与私有像素观察的来源限定收据，不是原生游戏或服务器运行见证。** 从 fresh GitHub main `8485c542850aedbee1e8a7c1ba7a41fad03bcf64`／tree `d83d3a2fc556c323cec071540316aa4aeea80248` 启动；完整核验当前分支／HEAD／最新提交／Actions、协议、README、设计/历史/来源登记、路线与模块规则，并通过 Git blob 重新实读原 `docs/CURRENT-STATE.md`。原史料 blob `c89e0e33537990aa2132b47c40fef49a985a935c`／**2,709,173B** 完全保留，不以空接口返回覆盖、截断旧档。

## 原始资料与新增可观察事实

1. 重新从个人 Library 真正取回并完整验源：CHAR01 私有 NPC ZIP **995,176B**，SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，2,205成员/全CRC成功；MAP09 私有原场景 ZIP **46,844,444B**，SHA256 `d84d0800dd600798769dfb7251a1d7816588ac061ccc27812ac64a37922d4a8a`，4,195成员/全CRC成功，内嵌原 955 DAT ZIP SHA256 `c079a1c25bfa11902b69c1f2839058d4fb20f025ef15c93f649f636c7e5f833a`；MAP04 私有TW1.0原RD图候选 ZIP **35,673,334B**，SHA256 `e9c43222797c7ebcddfcb1ccab6dbeba205b972bbbff4e1f29c14b3ece320d37`，4,169成员全CRC。三原包本轮均完成整包SHA与所有ZIP成员CRC复验。
2. 从同保存社区 mixed25 的 **真实原脚本字节**核对成年 `EVENT:LV>29` → `EndSetFlg:4`，四名使者 `LV>139` → 39、40、42、46；它们原文明确提及跳过四大洞任务，只有该后期来源身份，**不等于初期官方进阶/转生政策或原生效果**。重新扫描原NPC 2,205成员，精确 `EndSetFlg:4/39/40/42/46` 各恰两份脚本；另一条来源分别用原道具/前置事件条件与 `DelItem/GetItem` 字面设置相同标志。这里比较的是保存文件内静态替代路径，不是原世界已执行、四大洞完全复原或原始时间线。原脚本旧QUEST01已在之前编目，本轮不是发现10个新商业文件。
3. 真正从私有源内层读取 `2000.dat` 全部 **135,008B**／SHA256 `d75231434c69118a518a8d5dd34f266264b8551fe4f2d55a20cdfa11b46584b3`／CRC `35bf728a`、150×150/三u16平面，重读六个原NPC配置坐标对应的三平面原数值。地图2000原文件早在MAP04目录已登记，但上轮I39仅知道“MAP09完整画面未达资格”；本次由完整原DAT实际核格，避免误认地图不存在。再从私人TW1.0原图候选包实际重读五个不同图号的原PNG全SHA、像素和尺寸；它们是**不同来源载体**的可见候选。
4. floor2000中(42,44)至(59,62)的 **342原格**，两图形平面共有 **353次大于99的资源号引用，353/353均有可核TW1原RD图像候选**。另60次1–99低值仍无原渲染语义资格。完整150×150 floor2000仍有 **14次高号引用／11图号**未合格，不能把局部100%高号候选变成整地图像/原版图层/碰撞/人物出生证明。
5. 私有增量交付 `StoneAge-INTEGRATION40-private-source-cells-and-flag-comparison.zip` **48,395B**／SHA256 `36e75793b0a48702b7f47a60f21a9003dbe8f5209d80fefa56606c0ea54de253`、8成员（包含5张原源跨载体候选图与现代六格资料图），已成功保存于个人 Library 的`/石器时代/`，并再次下载，整包SHA及全部CRC相同。私人图文未进Git。现代拼排只是观察工具，不是游戏原画面。

## GitHub 真实后验

- 内容分支 `agent/stoneage-integration40-four-caves-floor2000-20261110`，初提交 `de24fd67a86a74f92d1a0f3bccd4d35bb83bd673`，第二次微调说明链接提交 `cc576c48dec27c9ba5b5886a03bc5c933bc2970b`；不影响原商业来源或数据。最终与起点diff为**仅4新增文件＋README追加1文件**：一份派生数字/哈希索引、一份日期来源说明、一份精确回归测试、一份专用CI。提交无原脚本正文、原商业图、原DAT或原ZIP。
- PR [#308](https://github.com/chinaneedM/stoneage-rebuild/pull/308) 于主线仍为`8485c542850aedbee1e8a7c1ba7a41fad03bcf64`时由精确预期HEAD安全 squash 合并。修订后候选HEAD `cc576c48dec27c9ba5b5886a03bc5c933bc2970b` 的 **18/18 pull_request Actions＋1/1 push Actions全部 completed/success**，其中专用 [PR run 42802141840](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42802141840) 与 [push run 42802133412](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42802133412) 均成功。
- 内容主线合并 HEAD `184a048c6fd6b01e269a6fa51d0ff6fe64a60066`，原生 commit tree `ba6c3356e0f65b61f0d11812384270b60b4d619b`，完整 tree **7701项**、`truncated=false`。该精确内容 HEAD 触发的 **26/26 push Actions全部 completed/success**；专用 [main run 42802261266](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42802261266) 成功。没有拿候选或旧版 CI 替代主线检查。公开原源索引 [INTEGRATION40](../../research/recovered/STONEAGE-INTEGRATION40-FOUR-CAVE-FLAG-BYPASS-FLOOR2000-SOURCE-R1.json) Git blob `63db0b971c3d03a8eddc5a3790bcc17baff8c44c`。
- 旧 `CURRENT-STATE.md` 仍相同 blob 与字节数；新增的本条验收收据自身形成新 main HEAD 后，**其 Actions 不预支为已通过**，仅前述内容HEAD有真实26/26成功。

## 证据止点与下一项

保存社区2.5里的四洞省略入口是文件事实，**不是**初代原版玩法、原客户端执行或未来单机应采纳的规则。原生玩家/宠物转生实际重置、原服出入/交换、四洞完整同源运行链与真正同一部署仍待证。地图低值图形/原图层选择/碰撞/实际操作仍未知；整个地图原像素未闭合。保持 Stage A 7 PARTIAL＋2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、overall_percent=null。

当前来源闭合后**最高NEXT**：从已有原资料中轮换至另一组尚未兑现的可见地图、宠物/NPC、物品或真实任务关系。优先完整原载体或新的跨模块实际内容，不能只重算目录数量或重复39/40事件号。成人/四洞只有当有新同版官方来源、原执行见证或补足原地图图层时再重开；不开始Stage B、联网服务或体验改造。
