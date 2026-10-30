# 《石器时代》单机原资源优先复原方向 R1（2026-10-30）

## 用户确认与项目决策

用户再次明确：**不以旧客户端联网兼容/恢复原服务器为目标或前置条件**；未来的新《石器时代》为**单机**，保留网游式长期成长体验，但不做网游运营。历史复原的第一阶段以已获得并认证的原始客户端资源为事实基础，先让原地图、场景、人物、宠物、SPR动画、WAV能够离线被看、听、浏览，再追证任务/属性/触发。由项目侧自主设计解码与现代观察路径，减少反复向用户确认。之前所有历史来源与失败证据保留，不重标为已复原世界。

**权益边界**：不对外运营、单机自用可能改变实际风险情境，但**不等于原图片、角色、地图、音乐、商标、名称或原代码已获复用授权**。当前观察包只是私人研究；原商业素材、原完整客户端、导出PNG/WAV/HTML留私人目录，不推送公开Git/网站/发行版。未来独立新作即使离线也必须单独做版权授权或重新创作/替换的资产清单，不能默认将原资源直接发行。

## 核查过的既有可执行能力，不重复建设

| 既存工具 | 已实现 | 不能错误认证 |
|---|---|---|
| `stoneage_original_animation_lab.py` | 原TW1已哈希原件SPR/ADRN/RD解码、帧序核验、私人动画HTML | 原游戏内帧率/场景选择/宠物身份 |
| `stoneage_private_sprite_frame_export_r1.py` | 将上述经过验证的帧导出私有PNG与逐帧SHA manifest | 全物种目录/授权分发 |
| `modern-observation-viewer.html` | 简体本地地图PNG/人物/宠物帧、来源清单验证、键盘人工移动/WAV试听 | 真实服务器碰撞/战斗/NPC触发 |
| `scene-room-shop-viewer-r14.html` 等 | 后期mixed25一个原Room/NPC/物品图片的私人组合观察 | TW1相同世界、原生UI、真实交易 |
| 原TW1 P3/P3H/P3I | 原客户端曾真启动，有登录原画见证，Win原程序窗口/退出得到认证 | 原地图世界进入、全部素材正确渲染 |
| SCENE33/34 | modified 2.5的服务端配置静态配对，有限自编Windows联网隔离资格 | 真实SAAC/GMSV handshake或与官方原TW1同服 |

今后停止为“看见原世界”反复追逐外部玩家截图、兼容驱动、私服握手、全套网页图鉴；这些只在能验证**具体原客户端资源映射缺口**时辅助。未取证的原游戏交互不得靠自建模拟反推成史实。

## 当前可运行的第一阶段入口

新增 `tools/stoneage_singleplayer_observation_kit.py`：只读经固定SHA验证的TW1数据目录的原四文件与历史元数据，用已有真实解码器把一个数字SPR帧组一键导出到**用户自行指定的公开仓库外空白私人目录**，输出：
- `index.html` 简体入口；本地选一个链接即可观看真正原客户端资源解析的 `animation-original.html`。
- `frames/frame-###.png` 和 `frames/source-manifest.json` 有据原帧及逐字节指纹（复制到相邻 `modern-observation-viewer.html` 需由用户手动选择，无法声称自动绑定地图）。
- `animation-original.json`、`kit-receipt.json` 保留原四文件和帧出处、配色未证、原程序/服务器未运行。
- 不请求网络、不启动旧exe、不连接任何服务器、不下载任何原图、不触碰公开Git受版权资源。

用户的**私人本机**存在已认证TW1原件时从仓库根目录执行：

```sh
mkdir -p /private/stoneage-observation/first-sample
python3 -m tools.stoneage_singleplayer_observation_kit \
  --original-dir /private/TW1/StoneAge/data \
  --output-dir /private/stoneage-observation/first-sample \
  --spr-no 100000 --direction 0 --action 6
```

打开 `/private/stoneage-observation/first-sample/index.html`。这只是路径示例，不证明本对话环境已具备该原件目录。首次真实私有输出需要现场源路径与全部四原文件SHA吻合；本次公开CI只跑合成负例和冻结历史索引验证，**不得说已经在本轮生成/看过新的原游戏画面**。样本数码非物种身份；工具未内置私有图片。

## 以“可见原资源场景”替代无限研究目录的验收次序

1. **O1 单机原帧样本闭环**：同一认证版本本地目录 → 原SPR/ADRN/RD全文件及块哈希 →真实frame PNG/私人动画HTML→ 实际浏览器目视与导出回读。该样本只算原资源观察，不叫完整游戏或某只宠物。
2. **O2 首张可漫游真实场景**：补足一张同版原地图的索引/图块/遮挡/调色板，按原图块位置在现代观察台拼合，人物帧独立标注显示；坐标、碰撞、投影/音效触发逐项标证，未经资格不得宣称原服行为。禁止用合成网格冒充原村庄。
3. **O3 人物及宠物场景动作**：一条同载体的 `entity/name ↔ graphic/SPR ↔ frame` 经源证明再联接，不以外观相像或网页格号猜物种，缺原主表的未知项保留编号。
4. **O4 单机交互研究样机**：在标有现代研究模拟的环境中加入地图移动、切场景、宠物展示、声音选择，**不连接原服**。此处的人工机制与原版历史事实必须有明显区隔。
5. **O5 进入新石器设计阶段**：只有核心体验和可见场景研究闭合后，另评估现代引擎/商业素材授权和自创替代品；全部用户界面为简体中文，后续单机运行、无账号服务器要求。

**当前最高NEXT：`OFFLINE-CLIENT-SAME-SOURCE-MAP-SCENE-O2`**，在有限一张地图内解决原map→tile→原图→本地可视组合。除非O2缺确切同版原图或实体来源，才去历史官方网页有限查证；不要再按SCENE44网页截图目录的路子继续扩大。O1工具完成只意味着一键入口具备代码、不是原始场景已生成。

状态不作无证晋升：Stage A 7 PARTIAL + 2 OPEN；Stage B及公开百科生产GATED；savedata R79 PAUSED_NON_BLOCKING；original playable world=OPEN；overall_percent=null。关闭PR#58是**优先级取舍**，并不是否认网页截图历史价值，其分支及CI可备后证据交叉核验。

## PR #59 主线真实验收（2026-10-30）

源已核PR #59 merge SHA `9ac2de6d9bc0370f6fe62aee254dd7883666ca52` / tree `870d5be2a4ae7a9d740affafe31763aa451f0d19`，候选`43f99fddf2bbc3bbdf6c54ea69bc5d3f02433a2a`同tree。**候选17项Actions与合并主线16项**经逐项remote检查全部 `completed/success`，专用runner `41056724406`/job`124066001869` 与主线 `41056840649`/job`124066398315` 原日志各实见9项否证测试OK以及旧TW1原SPR历史元数据 `TW1_ANIMATION_TIMELINE_EXACT_REPLAY=PASS; ORIGINAL_COLOR_AND_GAME_RUNTIME=OPEN`。这仅为**代码+旧冻结资料的合成验证**，没有再取TW1完整原客户端，没有生成/打开本轮新真实原图，不冒称实现了原地图/客户端真实世界。期间外部图片索引PR#58基于用户最新优先权实际关闭未合并，保留其源证据分支。

全部33次候选/主线Action ID、文件Git blob、认证与测试边界永久收据位于`research/recovered/STONEAGE-SINGLEPLAYER-ASSET-FIRST-PUBLICATION-R1.json`。原完整CURRENT Git blob `20050acf279a01555ab06a381dfcdc936bd381a6` 保持原样。此收据提交自己的新CI不提前预记成功。

下一O2必须优先从已认证客户端的**同一源地图数据与真实瓦片**做可浏览场景，若缺同版本图块和正确坐标证据则明确停，不准拿合成彩色网格直接说成原版村庄。未来单机游戏设计和公开版权授权审查独立于此离线研究工具。
