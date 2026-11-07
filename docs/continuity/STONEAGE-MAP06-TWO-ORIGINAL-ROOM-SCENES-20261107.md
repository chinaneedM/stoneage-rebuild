# MAP06｜两份原DAT与既有原RD的室内场景候选（2026-11-07）

## 启动与原件

fresh main c5ba9f265c8a4e59f87095a23d0fe75973ee391f / tree 28c0f852229fdef34959f117fffda94161ec9f6f，882远端分支、0开放PR、7337项完整树、无AGENTS.md。最新HEAD为文档提交且无该SHA的Actions，上一内容合入8685d2b00851e81bdb5dda512c28d34c995f2cc5的11项Actions实际全成功，不冒称新HEAD的运行。README/协议/完整CURRENT/决策/历史/来源/路线/22域/模块/离线优先与CHAR11最新NEXT均重读，全文与同一fresh HEAD的Git对象相同。CURRENT原2,709,173B / blob c89e0e33537990aa2132b47c40fef49a985a935c不改，本篇为加法覆层。

最高NEXT MAP06从人物转回地图，对1005/1006取真实DAT再组合原像素。已查重MAP05的1000/1001窗口及R34的1005/1006源文件/分层差异，**不称原DAT首次发现**；新交付是完整原格范围的候选组合。

本环境POST取源接口返回HTTP405，普通下载页方式未找到载荷链接，0B原包未取到，失败不追认为成功。复用既有CMS私密取回方式，私钥不入Git：源run42343333770 / job128315618638 / HEAD f6130a01a3f27a01995a577ed0df170cc5a3e2d4实际completed/success，真实两分卷及整包361,255,180B / SHA256 d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5核同。只取两份原DAT，原大小/SHA/CRC合格后加密传回，无原EXE/网服运行。

工件13562762335已独立下载：3070B ZIP / API及本地SHA256 766ff28035ac23a06c9867076239f4445af1e63cf509f052baea505eb606d194 / 全成员CRC通过。1461B密文SHA ed9feaff62bf2434f340bb2a0a77bc915acf8e7ec54396a34066569d034fe0ca；解密后880B原DAT ZIP / SHA d23288fd459091c32e808b48737f103624f3dbdccb922392af5d4bcde0a19265及成员CRC相同。[原始派生源回执](../../research/recovered/STONEAGE-MAP06-ORIGINAL-DAT-SOURCE-RECEIPT-R1.json)原1337B / SHA256 f4d65986089c9dfcbc7ba6611bb63de7b6a109103f3afe8b40695fd063ac8f65 / Git blob 7fcea665027e347d90870fb02be6093f47071644永久保留；无可读原DAT或私钥进入公开Git/工件。

## 实际图像观察

| 原DAT | 原尺寸 | 原两平面非零引用 | 大于99候选绘图位置 | 原1–99非零值，不绘图 | 使用原图号 |
|---|---:|---:|---:|---:|---:|
| 1005 | 30×30 | 975 | 218 | 757 | 41 |
| 1006 | 30×40 | 1284 | 246 | 1038 | 44 |

1005原5408B/SHA a6c9d1e43223a8afc515e37367d58cfcc6c301909e9e060d4c80d35fcb87c7c9/CRC340d1d6a；1006原7208B/SHA aa2e7d2bdb138545a3efa30f9482d563b1781810a856b4a91c12ce83eb08ab4a/CRC17acbe19。三原平面保留，第三平面不猜任务/碰撞含义。同MAP01/MAP04/R34原源相符，不反推TW1官方服。

重新取得MAP04原PNG包35,673,334B / SHA e9c43222797c7ebcddfcb1ccab6dbeba205b972bbbff4e1f29c14b3ece320d37，4169成员全CRC通过。两个原图形平面联合55不同大于99图号，逐一核MAP04原ADRN位置/压缩RD与索引像素指纹、原PNG/RGBA SHA、尺寸及TW1 ADRN元数据。**新RD像素解码0**；本轮是两原地图与既有真实像素的新组合。原PNG字节直接保留，不补图或丢弃1–99源值。

复用SCENE21已有渲染函数，原ADRN偏移及现代候选投影(x+y)×32、(y−x)×24，按既有对角顺序候选叠图。两个平面单独和合并各一张，共6图；1005画布1889×1425，1006为2209×1665，包含完整原格范围与构件边界。原生层序、投影选择、色盘/透明、低数字、碰撞和同服部署仍OPEN。实际打开两张合图，见岩壁、地板、床/台面与器物候选，**不是原客户端截图或可玩世界**。

另一程序独立从DAT按对角线读全部464候选位置，以NumPy逐像素覆盖而非主Pillow实现，55原PNG/RGBA与6完整画布均相同。六个HTML内嵌PNG与ZIP原PNG逐字节相同，JS语法通过；无私人原图浏览器运行认证。未交付试制包曾重新编码PNG，保存前已改为原PNG逐字节复制，仅以最终包摘要为准。

## 私人交付与NEXT

StoneAge-MAP06-two-original-room-scene-candidates-private.zip已成功保存：6,151,435B / SHA256 232ee5bc6f987fcb79fb1e7b24dfab85be5c59e9db7b472909ffaf939682ee47，65成员全CRC成功，含两原DAT、55原PNG、6图、无外网依赖MAP06.html与私人位置表。原件在同一私人包，可在清理环境后重演这两场景。公开仅[受限派生报告](../../research/recovered/STONEAGE-MAP06-TWO-ORIGINAL-DAT-SCENE-CANDIDATES-R1.json)、代码和反例测试；公共CI没有原商业图，不称CI重绘商业场景。

**MAP06 SOURCE_BOUNDED_PARTIAL；最高NEXT MAP07：** 继续地图模块，优先复用私人原DAT/像素，查重后批量观察其余有合格原件的场景。如需再次取同大载体，优先一次保管合格原DAT源批，避免逐图重下大包。取得原DAT后才承诺画面，不把691旧覆盖行算新地图，不扩引擎/网服/NPC玩法或体验优化。原世界未进入、Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、overall_percent=null保持。远端内容验收按实际后验另记。



## 首次内容CI失败保留

候选7715ccb4ece36e4879fca1c883ed71b998263367的MAP05–06 push run42343922563 / job128317423348及PR run42343925010实际failure：新增模块顶层复用SCENE21渲染函数，其间接导入Pillow，纯公共元数据CI未装Pillow而在测试导入时报ModuleNotFoundError。没有源DAT/原图资格失败。修正为仅在私人实际渲染时加载该已有函数；不增加公共图像依赖、不改源数据或已交付PNG。修正后的14测试另在python -S无第三方site-packages模式通过；远端改正验收按后验记录，不追认旧失败。
