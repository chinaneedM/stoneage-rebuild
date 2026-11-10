# INTEGRATION49｜28间原DAT房间、139个原配置的主线正式验收（2026-11-10）

[实际重新读取与来源边界](STONEAGE-INTEGRATION49-28-ROOM-NPC-WARP-20261110.md)；[永久公开纯派生关系及数值索引](../../research/recovered/STONEAGE-INTEGRATION49-28-ORIGINAL-ROOM-NPC-WARP-SOURCE-ATLAS-R1.json)；[PR #317](https://github.com/chinaneedM/stoneage-rebuild/pull/317)。

## 启动远端事实与历史保存

按协议从真正远端 `main` HEAD `106139d793a635809ea09c1ad0b390e2c3f211b3` / tree `b2d6ff0502fd850116230ae00e69ed47820236a3` 启动；重读最新分支、HEAD/tree、提交、Actions、完整协议、README、设计决定、史料、来源注册、路线、模块顺序、旧INTEGRATION48收据及全历史 `docs/CURRENT-STATE.md`。历史CURRENT原生Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` / **2,709,173B** 完整读取并在候选及合并主线继续保持**完全相同**，没有被截断、重建或覆盖。启动时零开放PR，所有相关前次内容主线Actions已成功。

## 原物证与新的跨模块整合

真实从用户私人Library获取并核对：

- `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` **995,176B / SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`**，2205项原成员CRC全部通过；其中12个实际相关原源文件整SHA/CRC以及139条NPC/Warp源CREATE字节区间SHA与之前公开CHAR01 Git blob `a088b61a3212f7049e7793f587123ffb29bebad7`逐段一致。
- `StoneAge-MAP07-private-28-original-room-scene-candidates.zip` **34,044,818B / SHA256 `2b356fefa1f5c634a2a64837b20904e124ab9839ad6a4e3b9a642e3c05df29a2`**，351成员完整CRC通过；真正重新打开28张已存原DAT，逐SHA/CRC、尺寸、U16第三事件平面、旧MAP07公开Git blob `f2cba278f4b5a15e50e905a1e6591958fd09dba5`的来源28室对照一致。234既有TW1零售候选图逐PNG/RGBA复核，28张整幅合层候选场景重新独立源像素拼合并与旧整画布RGBA逐字节同一。
- **139条**源配置分别有原CREATE路径/块序数/块SHA/原坐标（如有）/原图形别名/模板功能/参数SHA；**136**有源CREATE字面坐标，**3**条ExChangeMan无字面出生坐标，属于1003/2003/3003，不为研究图伪造NPC位置或运行时出生机制。
- **56条**房间端Warp来自28原DAT、创建块及原参数，源DAT出口格第三平面实值全为`49155`；根据字面的**目标父地图**建立有源层级：1000→3、1100→5、1200→5、1300→5、2000→5、3000→5。每房间端目标同坐标存在一个父地图来源CREATE块；独立父配置去重50个，其中**50条**精确回原房间同格、**6条**返回同房间相邻格（1101、2005、3001、3002、3003、3005）。这不是证明原native碰撞或真正可双向传送。旧MAP09缺1100、1300样本记录为历史限定，**INTEGRATION10已实回收这两主图原DAT**；本轮没有把先前缺件继续误记为原版缺图，也没有重复宣称新读取父图DAT。
- 这28地图及原配置原本已分别保管，本轮真正新增的是跨原件的139条逐房间来源关系和可检验的六组父图分类、56个源出口、6条特殊返程与三无坐标来源负证。**本轮新增原DAT原文件=0、新发现NPC原文件=0、新原RD解码=0**，不得把139称为新增游戏人口。

### 私人像素观察保管

28张现代来源坐标标注图仅用于研究，图层标记是现代叠加，不代表原生NPC像素或运行时发生：`StoneAge-INTEGRATION49-28-room-NPC-source-markers-private.zip` **16,857,395B / SHA256 `76e8f0999f5bae8241e74e724a5614964ecd1594cd0976b623167c27fb113b3d`**，29成员（28 PNG +1私人收据）。已实际上传个人Library并重新materialize下载完整ZIP，整包SHA、29 CRC、28逐图SHA均与原本完全一致；原DAT/脚本/图像和带图像包不上传公共Git。少数标点在现代复原可见场景区域外，已保留为未解释现象而非更改原CREATE。

## GitHub 发布链实际后验

- 候选分支 `agent/integration49-original-room-npc-warp-atlas-20261110`，HEAD **`bed6e6a286a1005e0277e0ddda8df038498d4a4a`**，tree **`a922f69c044019acf03361880fd2e4a45bdea6a6`**。相对远端启动HEAD仅5条路径：README增加、来源说明增加、公开派生JSON、原源数值反例测试、专项CI工作流。公开四份新文件SHA分别：JSON `673fd0ebd71a909a5678d919f706bab7a8e5e7cc`；测试 `51511d9a9f0d973daf905725dbf29969088eb06a`；文档 `39bd07a7c33e342478fa985900df822ba302bb6b`；工作流 `f7a496b99bf3d3a03503fc928e12b09eb56bd605`。所有Blob与本地Git hash-object结果逐个完全一致。
- 候选 `push` **27/27 completed/success**，专项 [run42833636277](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42833636277)/job **129889926688**，实际日志为`Ran 18 tests in 0.023s`和`OK`、无skip；PR #317 `pull_request` **19/19 completed/success**，专项 [run42833711630](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42833711630)/job **129890195356**成功。所有检查真正完成后才验PR clean、唯一父HEAD仍为启动HEAD，保护原CURRENT，提交无版权资产。
- [PR #317](https://github.com/chinaneedM/stoneage-rebuild/pull/317) `squash merged`到内容主线 **`684fae273e03d07c53a93ba492dfab1730653bf3`**，tree **`a922f69c044019acf03361880fd2e4a45bdea6a6`**，与候选逐对象同SHA，parent `106139d793a635809ea09c1ad0b390e2c3f211b3`。
- 内容合并后的独立main `push` **27/27 completed/success**；专项 [run42833875018](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42833875018)/job **129890761624**同18项源数值/旧索引交叉和负例测试实际成功，其他 Stage A 现有工作流无失败。本收据提交自身如无新Actions，不追认自身已经测试。
- **公开CI只读取公开派生JSON/历史旧Git索引**，没有私人原DAT/原NPC字节/真实商用客户端输入；本轮私人原件ZIP、图像、CREATE区间验收是独立本地操作，不以18项CI代替原运行或真实市场交易验证。

## 版本与下一包门槛

本包原地图/NPC来源为保存的**社区mixed25**，图像是分别保存的**台湾1.0零售资源候选**，没有证明同一官方部署或首版NPC/村庄归属。原生绘制、阴影、碰撞、NPC生成/对话、传送、宠物商店交易、旧游戏客户端运行全**OPEN**。地图6组仅由字面传送目标的父地板ID构建，不自称官方地理、南岛/北岛或初版布局。

**NEXT**：此28房间批次已在来源限定条件下封包，按路线与22域找**其他仍有真正可读取原DAT/可见图/NPC或宠物/物品实物、且未覆盖的内容模块**；若无新实质材料就明示缺件，避免再重复目录检查或从静态标点虚构人物/可玩地图。未来再取得原任务加载/同部署父图真实行为证据才按路径重开。Stage A继续 **7 PARTIAL + 2 OPEN**；Stage B/wiki GATED；R79 PAUSED_NON_BLOCKING；overall_percent=null。
