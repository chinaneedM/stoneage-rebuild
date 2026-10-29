# SCENE28｜台湾1.0原版源数据中宠物 action=1 的真实位图像素复原

2026-10-29。**证据等级：真正重新读取经身份确认的台湾Waei/JSS 1.0原客户端资源（不是原游戏画面或运行结果）。** 此次从已私人保管的P3H包重新取得原始图像/动画文件并执行双解码。SCENE26只基于mixed25旧研究报告提供24条动作序列；本次确实补上48个 distinct RD 原始字节的来源/像素校验，不把同帧的80次出现误称80张不同原图。

## 原数据保管与双重身份

原始来源私有ZIP `StoneAge-TW1-original-runtime-and-native-observation-P3H.zip` **372626292 B**、SHA256 `3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24`，来自先前经P3H认证的375个原运行成员。实际整ZIP重新哈希，通过。

本次重新认证：`spr_1.bin` 2889630B SHA `53d5b2d40453a30fd1569637ebf0db7b3010542b00970ec83af0295a3b3ae31a`；`spradrn_1.bin` 5568B SHA `275b64ff55667aec633a7e82e09d65c84141380521f0f2e64c9a28e0d3aa6c25`；`adrn_1.bin` 10079680B SHA `47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8`；`real_1.bin` 315842228B SHA `408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13`；两个708B的Palet_0/1完整SHA在永久数字报告中。

100250/100251/100252三个原 SPR 组处于TW1索引240/241/242，全段字节SHA256与此前mixed25 R40/SCENE26对应**完全一致**：`eb1a87cd4cc8e3b409990783c7bcc3bc463acab4cac7d2d961127d899da047ef`、`073278ba6ae1e623eea969deef11f99fd9be8b995af332506e830bd046c86764`、`eeb2ec4546277c2acdf1b43fff7967c4c0fe5ac5c019bb7d68a901e134691b0a`。此片段同字节不证明整个不同载体属同一商业部署build或宠物同名同身份。

## 真实图像材料的有限结果

|对象|实际数量|检验范围|
|---|---:|---|
|三个组的 action=1 八方向源动画|24|源header/方向、动作码、duration原整数、原10字节逐帧字段|
|动画帧出现位置|80|原重复的帧索引仍保留，32+32+16|
|不同原bitmaps（按ID）|48|**TW1同源ADRN唯一记录、REAL原始RD逐块真实读出**|
|RD图像实解码|48/48|全部原flag1，独立两种RLE实现与原像素索引逐字节相等|
|原非零索引像素数（48张合计）|53932|不是“游戏总像素/不重复画面”|
|候选配色图片|96|48×2原SAP初始化色表候选，原位图内容保持；不代表运行色表|
|私人可交互网页|1|Chromium真实控件/逐帧/方向/候选色/复位测试，JS错误0|

本次本人确实打开了真人类观察者导出的三种棕/红/斑点兽形候选八方向联系图，**不据外观认证物种名称**。原`action=1`不认证具体“待机/攻击”等动作语义；原`duration_word=100`不可解释为100ms/FPS；声字段皆0不能说明原游戏播放静音。原色版、原客户端显示路径/真实伺服器、骑宠与战斗、同服身份仍未知。

## 公开/私人分离与验收

公开永续机读：`research/recovered/STONEAGE-SCENE28-TW10-ACTION1-PIXELS-R1.json`，列出每幅原ADRN完整记录SHA256、原RD SHA256、**实际解码像素索引SHA256**、尺寸、偏移、帧数及负证；**不包含原RD字节、index pixels、原PNG、声音或原游戏二进制**。独立守门 `tools/stoneage_scene28_tw10_action1_verify.py --check` 以Git blob `5e63345a74271ada339b37032e665349d52ec40c`重新读取SCENE26，反检48张影像的完整唯一位图列表及原源身份；本地私有 `--source-dir ... --private-original-zip ...` 可重新校验完整原六文件与48RD来源SHA/像素，不在公网CI执行，CI只检数字证据。11个负例/身份单测均须经远端CI通过后才能入主线。

私人交付 `SCENE28-private-original-TW10-pet-action1-observer.zip` **347996B**，SHA256 `f707d196acb6c449e2b6b11345a02db36ac6726131ce51f9a93587b32c3ad492`，已保存在个人私人Library `/石器时代/`；其中含来源限定的图片预览及操控页，不推公开Git。原始大包同样继续私人保存；本轮**没有运行原商业客户端或进入世界**。

**下一方向：** 将真实同源地图场景/人物/宠物在私人离线观察器中联接起来，形成更直观的可走动观察；仅“模拟标记移动”不可冒充原生人物走动。若具同服服务端与可观察原客户端画面，才考虑重新开启真正进入原商业游戏的运行门；不反复扩低层工具、反复下载已验资源或无界扫截图。Stage A7PARTIAL+2OPEN，B/wiki GATED，R79 PAUSED_NON_BLOCKING，整体百分比保持null。