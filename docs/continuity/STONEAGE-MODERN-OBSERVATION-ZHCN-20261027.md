# 2026-10-27｜现代离线资源体验观察 + 新游戏简体中文为默认

**性质**：用户明确设计要求和 P3F 后技术路径纠偏；是 DD-030 的加法连续性记录。不能凭观察台的像素、动作、地图、声音推断已经连接原商服或真实体验到原游戏。

## 本轮依据

Fresh GitHub main `ca385a3b864554d3667caafdf72aa7939f647485` / tree `e6885d1b8286b3f3c8763f8427976f412daf6890`；完整`docs/CURRENT-STATE.md` Git blob `031c76a5a8e431f646853909bb2f2e11e6328cd2`（2680510字节）已经真实读取，原文件保留不修改。旧持续记录、R46与P3F Actions已重新核；P3F三实跑只通过自编程序取证，没有ACP950+真8bpp资格，更没入世界。

用户纠正：为了做适合现代技术的新石器，不能把原版Win32 256色、服务器消失、台湾繁体ACP等旧实现依赖当成长期硬障碍；用户记忆中的原作主要是**大陆简体中文版**。要求最终新游戏默认**简体中文**，但历史考据应同时涵盖台湾、日本、韩国与大陆版本，不能混认版本与翻译。

## 现成可复用实物与两路径决策

仓库已有严格核源的台湾1.0`adrn_1.bin`/`real_1.bin` RD索引解码、SPR组/帧序/合成偏移验证、Palet_0初始化色路径、WAV格式审计，及独立的后期826张世界地图语义模型。这些是很好的现代显示数据底座，但**地图拓扑模型/同版索引 ≠ 原游戏截图；Palet_0初始色 ≠ 任一场景实际调色板；帧序 ≠ 已证动作语义/帧率**。

- 路A：继续保留原`sa_3.exe`隔离实机取证（已真实看到登录页、未进入世界）。需要持久Windows/XP兼容环境、色彩/输入与完整断外网门槛、必要时本机回环契约。但该环境缺失不能无限阻塞路B。
- **路B优先：立即可在现代浏览器打开的本地观察台**：`tools/modern-observation-viewer.html`，加载用户电脑本地实际地图PNG/人物帧PNG/宠物帧PNG和原WAV，自主观察动画、像素比例、画面叠合和声音。现代平台把UTF-8/Unicode当默认，不沿用老版图形API。人工移动、宠物偏置、地图缩放与180毫秒/帧均明确是**示意参数，非游戏真实机制**；原图尚未选择时是**合成方格**。仅供研究，不代表正式新引擎选型。
- 额外`tools/stoneage_modern_observation_manifest.py`：本地只读SHA256/尺寸/音频格式，拒绝未知版本、错误后缀/超大像素、同槽重复与假“已登录/已进世界”字段；输出`private`目录的纯元信息JSON，不会复制或发布原图/原声音；尚未核对每个资源与官方原载体，故均标`USER_LOCAL_FILES_REQUIRE_INDEPENDENT_ORIGINAL_SOURCE_ATTESTATION`。

### 未来新游戏文本原则

默认显示语言 `zh-CN`，文字和构建流程为Unicode UTF-8。**原版文本仍需按来源独立保存**：台湾原字节/繁体、日本原字节/日文、韩国原字节/韩文、大陆原字节/简体及各自已核编码。不能由于目前源客户端是台湾1.0就让未来新游戏必须使用繁体；也不能将大陆玩家记忆倒写为台湾1.0的历史事实。

正式文本系统后续需用稳定的`concept_id`+来源版本/原文本+审校后的简体产品文案三层映射，保留同名歧义和运营活动任务/本体任务区分（DD-028）。无需现在挑选完整生产引擎或先行制作内容。

## 使用与验收

直接通过现代浏览器**本地打开**`tools/modern-observation-viewer.html`：缺资源可先观察合成网格的输入响应；加载由现有严格鉴真的TW1 RD/SPR私有提取工具导出的PNG时，才可能看到真正源像素或帧序，归属取决于源核验；加载大陆或日本、韩国版本素材必须各自标清版别和证据。音频点击由用户自行触发，不假定历史游戏事件。公开repo只有观察台源码和合成测试，没有任何商业原图、BGM、客户端或任务对白。

私人纯元数据记录示例（原图须由私人原包解码工具产生，路径示意而不是项目内真实原始文件）：

```bash
python -m tools.stoneage_modern_observation_manifest \
  --profile TW_WAEI_1_0 \
  --map /private/tw1/map.png \
  --character /private/tw1/frame-0.png \
  --pet /private/tw1/pet-0.png \
  --wav /private/tw1/sample.wav \
  --output /private/observation/source-metadata.json
```

**本轮验收**：CLI/Python合成边界单测与CI、HTML本地控制和简体UI静态安全检查。GitHub runner没有私人可用的全部原版图资源；如仅通过合成测试，应如实说明“**现代观察台代码就绪，尚无真实原游戏世界场景画面/声音可认证**”。不因本轮UI本地化或现代技术选型而提高 Stage A7 PARTIAL+2 OPEN、Stage B GATED、savedata R79 PAUSED或整体百分比。高优先级NEXT是**用同构建已验证地图原图块+SPR+Palet_0实际导出的私人素材组合出第一组可观察、来源限定场景**；地图坐标及原游戏完整玩法仍单独OPEN。若私有持久原料依赖缺失，则先完整记录阻塞/只读导出路径，再以有限资源规格组装，不返回无限NPC表小取证。

## 已连接已证原SPR帧 -> 私人PNG源序列导出接缝

除手动本地图之外，新增`tools/stoneage_private_sprite_frame_export_r1.py`：直接调用已验收`tools.stoneage_original_animation_lab.timeline/preview`，要求四个原TW1文件完整哈希、SPRADRN/SPR分组与RD逐块哈希全部通过；再从**已认证原帧包的内存JSON**逐帧导出私有PNG和纯元数据清单。可传入同原盘的`Palet_0.sap`来显示程序初始化色，但这仍非游戏场景真实调色板。原素材只写到**仓库外事先建好的空私人文件夹**，默认无网络、不自动提交仓库；动图帧文件按`frame-000.png`等排序，可直接通过观察台人物/宠物帧多选框载入。没有原盘实体时工具不会假生成实际动画，测试只用合成PNG。

```bash
mkdir -p /private/observations/character
python -m tools.stoneage_private_sprite_frame_export_r1 \
  --original-dir /private/TW1/StoneAge/data \
  --spr-no 100000 --direction 0 --action 6 \
  --output-dir /private/observations/character
```

选择目录中的`frame-*.png`载入现代观察台。源校验生成的`source-manifest.json`保留时序及逐帧哈希；本地显示界面人工播放节拍180毫秒，**不会认作源真实FPS、角色身份、场景或游戏服务端事件**。下一步接同版已验证的地图原图块布局，而非随意将外来照片标注为当年村庄。

## 2026-10-27｜远端并行提交的保留与复核

此候选最初以 main `ca385a3b864554d3667caafdf72aa7939f647485` 为父本；检查时远端 main 已另提交 `565cec85e9dd8139e97b2df4b1d754d103930491`，独立接受 DD-030。此次用双父提交非破坏性合并两路：**保留该主线 README 的完整语言决策和设计决策文档不变**，仅修改旧的「Windows VM 最高NEXT」表述为已批准的现代资源观察并行路径。原大 CURRENT 全字节未改、全部旧事实与负面原客户端资格仍保留。

候选观察台只读本地PNG/WAV；帧源工具实际调用已存在的四原文件和每个RD/SPR摘要检查接口，输出始终在非公共的本机目录。观察网格、移动、默认动画节拍、自动缩放与Palet_0初始色皆为**研究演示，不证明原游戏真实场景、坐标、FPS或声音事件**。只有兼具同来源图块布局／场景调色板与原客户端画面校验才可进一步晋升历史场景证据。

候选 Actions [40510803375](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40510803375) 在检查时仍 queued（网页展示地址中的仓库用户名若有变动，以实际GitHub作业ID为准）；候选尚未获得完整主线验收。本节点仍不算原图场景已目视、用户已实际进入原游戏。下一优先为同构建原图的私人地图装配及独立可视观察证据，非漫无边际扩NPC表。

## 追补：第一张真实可见场景为何不能只靠TW1原盘

现已重新核对`docs/STONEAGE-TW10-MAP-CONTENT-COLLISION-R1.md`及完整地图来源：**TW1零售盘的原服field场景文件为0**，它由早年商业服M/MC下发，不能指望现代观察台从该零售盘直接导出`台湾1.0完整村庄`。后代826层可物化地图为`LATER_RECOVERED`，可成为现代观察的实物参考，但必须在同来源、来源实有的tile/parts图形联接成立后显示，并保持与台湾1.0/大陆玩家体验的不同证据等级。具体单场景源/图号/图层/私人可看验收见`docs/specs/STONEAGE-SCENE-OBSERVATION-CARRIER-PRIORITY-R1.md`。此记录不冒充本轮已取得整张地图、已运行后代客户端或已观察到真实战斗。

## 地图单元编号→私人可视诊断（非历史像素）

新增 `tools/stoneage_private_region_diagnostic_r1.py`，**真正接通之前已完成的`Recovered25RegionPayloadSource.materialize_region`认证链**。它在用户已有后代版本 DAT/LS2MAP 私人原字节与目录的前提下，根据经仓库权威拓扑清单与原文件SHA校验的指定floor/局部矩形，导出最多64×64单元的PNG诊断图和逐格ID、事件层是否存在、地图来源SHA、裁剪范围的本地JSON。客户端DAT需要tile/object/event三层，LS2MAP只有tile/object且event明确`null`，不准伪造全零事件层。

**画面警戒**：PNG只是原始地图`tile_id`经合成哈希分配的颜色，黄色表示非零object_id、粉色表示客户端真实存在的非零event_id；像素中嵌有`NOT ORIGINAL STONEAGE GAME PIXELS`声明。地图坐标、编号、源指纹可供下一轮准确索取对应图像，**纹理、地形、场景摆放、宠物战斗、台版首发归属、原版实际游戏画面全部尚未复现**。此类图不能作为原版村庄证据，但能在取得真实私人DAT/LS2MAP时减少盲查ID。

使用方式（需要在持有相应原源目录的隔离本机运行，文件路径和地板编号是使用者真实输入）：

```bash
mkdir -p /private/observations/map-cells
python -m tools.stoneage_private_region_diagnostic_r1 \\
  --client-dat-dir /private/recovered25/client-map \\
  --server-map-root /private/recovered25/server-maps \\
  --floor "\u0024{FLOOR_ID}" --x1 0 --y1 0 --x2 15 --y2 15 \\
  --output-dir /private/observations/map-cells
```

将私人生成的`tile-id-diagnostic.png`载入现代观察台地图输入框，只能作为**真实map单元数据的编号和对象/事件分布诊断**。GitHub本身并无当前轮持久挂载的完整商业地图载体，本轮9项独立合成负例测试不等于已经利用真实私有地图作出首张原场景图。下一阶段仍必须建立逻辑ID→同版原位图原图像及真实绘制规则的SHA级联接（见`docs/specs/STONEAGE-SCENE-OBSERVATION-CARRIER-PRIORITY-R1.md`）。

## 私人地图诊断图可点击查询（PNG与JSON必须同源）

本地浏览器选择`tile-id-diagnostic.png`作为地图，再选择它同目录的`source-manifest.json`作为地图诊断清单；代码校验schema、`LATER_RECOVERED`、窗口坐标、逐格 uint16 地形/物件/事件编号以及LS2MAP事件层确实为`null`，并使用浏览器 WebCrypto 校验**选择的PNG字节SHA256**与清单一致，失败直接拒绝绑定。验证通过后，点击画布显示所指单元`x/y/tile_id/object_id/event_id`并画出框选位置。更改地图文件或手工改地区标签会取消绑定。

这里的本地SHA一致只说明 **PNG 与其诊断清单匹配**，不是SHA单独证明商业原载体来源；真实地图源资格来自CLI上一阶段的`Recovered25RegionPayloadSource`全源SHA校验。用户本机未加载原盘与地图时，只能测试合成数据及PNG/元数据检查，不能声称完成原本场景实拍或真实客户端操控。

## 2026-10-27｜现代观察器逐帧SHA绑定与异步换源拒绝（候选追加）

本轮按最新远端main `565cec85e9dd8139e97b2df4b1d754d103930491` /
tree `6da3843732494d8a4696e372bf6ab603d8611404` 重新核对了完整
`CURRENT-STATE.md` Git blob `031c76a5a8e431f646853909bb2f2e11e6328cd2`，
保留2680510原字节的大型历史文件，未写入或裁剪。现代观察候选在这个main之上，
初读分支HEAD `1e9959aaf4800773ada3343224bd532097ca9ef9`，领先7个提交；
原版客户端仍未进入世界。读取主线P3F、DD-030、地图场景载体缺口及现代工具实际源码后，
把**观察界面中PNG帧是否仍对应经认证导出**作为这一有限改进的对象，而非回去扩任意NPC表。

先前只有工具端 `stoneage_private_sprite_frame_export_r1.py` 为每帧导出名称/全长/SHA，
但现代浏览器仅手动读取PNG，不读取导出清单；混选、替换和错序的PNG仍能显示，
无法分清「源工具生成」和「浏览器实际看到」是否是同一组素材。本追加在
`tools/modern-observation-viewer.html` 增加人物和宠物**独立**`source-manifest.json`
导入框：以真实导出schema、台湾TW1来源、四原文件存在、帧序长度、导出编号、
唯一文件名、逐PNG文件长度及浏览器WebCrypto SHA256核对。帧替换清除当前绑定，
人工改变来源标签会撤销不适用的证明，文件更换或地区切换期间异步哈希的旧回调也不能
覆盖新状态。后代地图诊断与TW1帧同屏时必须明确提示「跨版本人工拼合」；
地图SHA绑定和原DAT/LS2MAP事件层缺失边界保持不变。这个界面绝不自动拉外网数据。

**证据限界**：本机PNG与清单逐SHA匹配并不自动证明清单本身由原盘可靠导出；
那仍依赖CLI的TW1四原文件/RD/SPR源字节鉴真，须另保留原始输出报告。
地图诊断由后代实际载体派生，既没有早期原服地图、同版纹理对应关系，也没有
可以被当作游戏实拍的原画。浏览器加载真实私人原图、人工实际目视、原游戏内声画同步、
登陆/选角/战斗，**本轮全部未发生或未验证**。实际Windows隔离来宾仍阻塞；
现代观察器的成功不得晋升`AUTHENTIC_GAMEPLAY`。

独立快速检查：真实GitHub候选HTML最新版本由V8语法解析成功；采用**模拟**
DOM、文件对象及WebCrypto摘要的JS执行，正向帧清单绑定通过、修改PNG摘要的负向
拒绝通过（这些不是实际浏览器像素观察，更不是真实原盘样本测试）。
`tests/test_stoneage_modern_observation_r1.py` 增加SHA绑定、历史主张禁升、跨版本
标记及异步换源守卫的静态回归。**GitHub Actions当前仍有queued作业，不能预报
CI成功或主线已验收。**

实际私有目录使用次序：先以原始TW1四文件通过导出器输出`frame-000.png`等
及同目录`source-manifest.json`；浏览器先选择该目录全部`frame-*.png`作为
人物或宠物帧，再选择相应的帧清单（两槽分开）。展示的人工运动、缩放及180ms节拍
仍非原始游戏实测；不做文件上传。无原盘和原图时，只能运行合成测试/查看研究网格。

**剩余最高优先级**：先取得至少一个可用、同一后期保存载体中的实际map字节、
tile/object ID→**同版**真正原图形内容与选图语义、必要的局部绘制投影/颜色证据，
制作最多一个小区域的私人实源观察工件，并由观察者实际检查；
拿不到这些字节或图号绑定就报告准确缺源，不自动伪造村庄/宠物/战斗。
同时保留真实原EXE在持久隔离ACP950/8bpp/输入/无外连来宾的独立路径。
DD-028、DD-030、Stage A7 PARTIAL+2 OPEN、Stage B GATED、R79暂停及
总体恢复百分比未知均保持。
