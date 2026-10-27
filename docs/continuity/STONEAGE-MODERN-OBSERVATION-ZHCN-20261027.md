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
