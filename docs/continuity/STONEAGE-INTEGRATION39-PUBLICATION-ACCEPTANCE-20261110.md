# INTEGRATION39｜原目录成年／转生配置—事件号跨表整合和 GitHub 验收（2026-11-10）

**这是 GitHub 后验与保留原始史料范围的加法记录，不是原商业游戏运行见证。** 本轮由 fresh 远端 main `d527443507ab66234199e5ab70584af11bafdba9`／原生 tree `0c71823ae26be018fb46e51b3db2f0511d3f5acd` 启动。按协议重新读 README、连续性协议、完整 `docs/CURRENT-STATE.md` Git blob、设计决策、历史时间线、来源登记、复原路线/模块优先指令、最新 INTEGRATION38 来源与后验及远端 Actions。原 `CURRENT-STATE.md` **2,709,173B**／blob `c89e0e33537990aa2132b47c40fef49a985a935c` 完全保留，Git 普通文件接口空返回已按协议由真实原 Git blob 文本核实，无截断覆写。

## 此次游戏内容关系（已知事实与待证边界）

复用保存混合社区2.5原档先前实际取证所得的 QUEST01 `52db8b4b6cd43cd2afa4a8d2e8460f214933f5e2`、CHAR01 `a088b61a3212f7049e7793f587123ffb29bebad7`、QUEST32 `a2f907b7d8c1293c9e15f1bfc2afbc4b1fa3f35e` 和 MAP09 `137580e7c25aadf3d679b6ebfb5080b79912cc4f` 原生 Git 派生索引，精确联接 `my/chengren`／`my/zhuansheng` 五个 CHANGE EVENT CREATE 配置与五个原脚本SHA、六个原TYPE段、地图数值2000的五原坐标、源图形号和原字面标志4／39／40／42／46。另将同 `zhuans.create` 第4、5块的 `sb_dou` 和 `npcgen_petshop` 功能类别独立，不伪合并为转生事件。QUEST32先前已列这五原脚本未进入QUEST08–31所选范围；**这次成果是新的可重放跨表关系，不是新拿到五份商业原文件**。

本轮没有重新打开私人原RAR或认证新的原像素；未取得完整LV阈值、原生状态改变语义、原版执行的成年/转生仪式、早期官方同服归属，亦未补得2000楼层的合格原场景图。源目录名只作静态文本证据。原商业对白、原图、脚本源正文、原MAP/DAT、原媒体均未公开。详见 [内容记录](STONEAGE-INTEGRATION39-ADULT-REBIRTH-SOURCE-20261110.md) 与 [不可变派生 JSON](../../research/recovered/STONEAGE-INTEGRATION39-ADULT-REBIRTH-EVENT-CREATE-SOURCE-R1.json)，Git blob `5bfdb4d9734b73e769924d0dc0229dc9bf3ab510`。

## 候选、失败、修复与主线后验

- 工作分支 `agent/stoneage-integration39-adult-rebirth-source-20261110`；首提交 `140e8e34da9238ea286705982d37504273b70a71` 的专用 PR 检查 [42796915455](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42796915455) **失败**：测试构造 Git blob 头时把 NUL 分隔符误写成两个可打印字节，日志见 `AssertionError: quest01`。此失败不可追认成功或删除历史。
- 原研究证据不改，仅修正测试分隔符；修复后的候选 HEAD `c55a9b8749aa6852310daab390992c7d9cb4ec79`：该提交的 PR Actions **17/17** 均 `completed/success`，分支 Push **1/1** 成功；其中专用 [PR run 42796988688](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42796988688) 与 [Push run 42796979140](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42796979140) 均真实成功。
- PR [#307](https://github.com/chinaneedM/stoneage-rebuild/pull/307) 用精确 expected head SHA 安全合并；合并前再次确认主线仍为初始 HEAD、PR 可合并。主线内容 HEAD `7205e2a5f0fb720adc67f1e2b66fdad7872cfeb4`，原生 tree `27507eb505eefb30b76339b5dd13c28c9c2c62bd`，完整树 **7696项**、`truncated=false`，相对于起点仅新增四文件与README追加，不触动CURRENT。
- **本内容主线 HEAD 的 25/25 项 Push Actions 全部 `completed/success`**，不存在 pending/failure；专用 [主线 run 42797131940](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42797131940) 已实际成功。这不代表原生 StoneAge 客户端/商业服务端已经运行。此次收据提交自身若形成新的 HEAD，不能自动继承前述25/25的检查结果；仅记录已验证内容HEAD。

**状态不变：** Stage A 7 PARTIAL＋2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，overall_percent=null。继续仅做 Stage A 有证据的原版资料复原，不启动新单机引擎／网络服务／现代玩法优化。最高 NEXT 是从其它现有实物中挑一组真正未接通的静态机制／宠物／NPC／地图／任务或新原像素材料；同目录成人/转生须完整限定原脚本/可核原运行才重开阈值与效果，2000地图须新合格DAT／像素来源才重开可见场景。
