# INTEGRATION106｜shop_m3 四十原 NPC 创建配置与台湾零售 30 组原二维候选实际联接（2026-11-14）

## 启动和本轮止点

按远端 `main c27d7ecd45ec3ff3a9bab1afd9ba48dc79f7dc00`／tree `26a97b62cf31965850d6660efb45ad9e8fd7f381` 启动；原 `docs/CURRENT-STATE.md` 完整 2,709,173B／Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 原样保留；当前 HEAD 26/26 Actions completed/success、0 开放 PR。完整 README、连续性协议、设计决策、历史与来源登记、R2 路线、模块优先级和最新原始来源索引均已核对。**本任务只恢复可静态读出和可实际观察的游戏内容，不运行商用客户端/服务器、不开发新引擎。**

上一包 INTEGRATION105 剩余 floor300 不是「原档不存在」：旧 MAP01 原 RAR 完整清单已定位 `300.DAT` 2,160,008B、原 CRC，但原有解包器仅输出262,144B并报 `Parsing filters is unsupported`，同名 `300.MAP` 也未 CRC 合格；本轮私人保存的原 RAR `361,255,180B`／SHA256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5` 再验一致，受限环境无法取得独立支持该过滤器的解码器。原 floor300 和相关16/16个源/目标坐标仍为 **OPEN／UNQUALIFIED**，不得将旧部分输出视作新原 DAT 或借尺寸补地图。详情以前的 MAP01／2026-11-04 解包失败报告为准，不重复无源解包辅助工程。

因此轮换到此前 CHAR01 全目录已有字节、但尚未形成完整可见关联的 `npc/genout/shop_m3.create`。与已有 INTEGRATION100–105／ITEM01 的商店库／PET07 原图逐一查重：本轮**不是**首次发现13间商店、40个历史独立 NPC、30个新原图或认证一个官方同部署 build。新增内容是完整40原源配置／28原参数 SHA 与已保存原 TW1 二维像素候选的可实际查阅联接。

## 实际原始来源与游戏内容

- 私人后期 community mixed25 NPC 源 ZIP `StoneAge-CHAR01-mixed25-all-npc-original-private.zip`：995,176B／SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`；完整 **2,205/2,205 成员 CRC**。真正解出 `npc/genout/shop_m3.create` **7,139B**／SHA256 `ae3d1b1939e31f61f3a5273f36e90961d25d8d236ddefef2dc850e0035e5b958`，逐 40 个原 `NPCCREATE` 的字节窗口 SHA、出生坐标、楼层、原功能模板与既有 CHAR01 全源公有索引准确一致。真正读到 **28份不同**被其引用的原参数／村民文件，逐完整 SHA 和 CP950 核实，商业原文未进 Git。
- 40 创建位置跨14个来源楼层：`npcgen_shop` **13**、`npcgen_man` **8**、`npcgen_mugon` **6**、`npcgen_limitshop` **3**、`npcgen_winhealer` **3**、`npcgen_dengon` **3**、`npcgen_petshop` **2**、`npcgen_petskillshop` **2**。这只是原保存配置的功能名，不是商业服已真实加载或商店交易成功。13个 `npcgen_shop` 的原参数已在既有 ITEM01 224 来源 ItemList／191 CREATE 关联目录中有数值登记，本轮不重复统计为13新商店或新物品。
- 静态坐标与旧 MAP04 真验 955 DAT 原目录交叉：**38/40 创建点**在旧有资格的12个楼层 DAT 宽高界内。`floor 5000` 的第12条 `(50,23)`、`floor 6000` 的第38条 `(45,73)` **缺同源已资格 DAT**，绝不因缺表写成越界、补坐标或宣称原始碰撞／世界可达。另有保留的重要字面不一致：第24条原 CREATE 为 **floor5105 (22,8)**，实参文件名却是 **`ss_5105_24_10`**；两者均与原 SHA 一致，不能以命名猜原创建点应为(24,10)。
- 另一独立来源台湾 Waei/JSS 1.0 **零售原客户端** P3H ZIP 372,626,292B／SHA256 `3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24`；全 **379/379 CRC** 通过，原 ADRN、REAL、Palet_1、SPRADRN、SPR 成员各自完整 SHA 认证。40原配置引用 **30个不同图号**；其中 **24** 在原 TW1 ADRN 找到唯一静态别名 RD，**6** (`100252/100279/100288/100291/100351/100367`) 在原 TW1 SPR 找到唯一组，限定选择原 `action=0/direction=0` 首帧真实 RD。原30RD全实际取出、独立两 RD 解码实现索引像素完全相同；Palet_1 **仅候选**配色的30PNG经 Pillow 独立回读完整 RGBA 全相同，均已目视。旧 PET07 已见这6个原 SPR 群组的原位图 SHA，旧 CHAR03 等曾观察部分静态图，**新增独立历史原图发现量不冒称为30**。

## 真正私人观察、保管及远端可核证据

- 使用上述 **30 组实际原 PNG** 制作私人现代离线资料页，40条原配置按楼层／功能过滤，图像重复引用仍保留所有原位置。原页面保留后期社区源繁体原文字／原图真实字节，只私人存档，绝不作为原生游戏内截图。
- 真 `Chromium` 按原图片字节验证 **40/40 图片节点加载**、30不同图、初始40卡、楼层5001筛为3卡、`npcgen_shop`筛为13卡、清空后40卡，**0 JS error／0外网请求**。当前测试宿主阻止 `file://` 导航，浏览器测试通过 `page.set_content` 内嵌相同 PNG 字节；不能声称原始本地 `file://` 导航成功、原商业客户端画面或原生角色动作。现代 PNG／调色板候选并非原渲染选择证明。
- 私人 ZIP `StoneAge-INTEGRATION106-shop-m3-40-NPC-original-2D-private.zip` **215,924B／92成员**，整SHA256 `308e4a6a0cd00af200a7f9208adf9e630413ed5cb53a3cb15e1cf7b10efcb7c8`，包含真正原 CREATE、28文本、30原 RD 及30候选 PNG 和现代页。已上传个人 Library `/石器时代/`，**再用独立 Library 文件 ID 完整取回、逐字节 SHA 一致及92/92 CRC 成功**；版权原文、原 RD、PNG、浏览器页皆未放公开 Git。
- 公开 [SOURCE/PNG逐SHA及40坐标负证派生JSON](../../research/recovered/STONEAGE-INTEGRATION106-SHOP-M3-40-SOURCE-TW1-ORIGINAL-2D-R1.json)、10项正反公开来源守卫和专用 GitHub Actions 只能反证元数据的来源一致性；**公开 CI 没有重新读取私人原商业原字节或运行真正原客户端**。PR、候选及正式主线 CI 只在实际完成后记录。

**SOURCE_BOUNDED_PARTIAL，不是 GAMEPLAY_VERIFIED。** 完整 CURRENT 原 Git blob 不动；Stage A 7 PARTIAL＋2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，overall_percent=null；独立保留 floor300/5000/6000 的原 DAT 不可读资格。**NEXT** 选择下一组未重复且有真原件／可见二维/宠物/任务的来源，或仅在新同源原 DAT 完整字节和 CRC 可验证时重开上述坐标；不扩大缺源工具或新引擎、MMO 工作。
