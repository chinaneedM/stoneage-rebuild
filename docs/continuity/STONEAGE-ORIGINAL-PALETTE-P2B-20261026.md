# 2026-10-26 — 原TW1初始化调色板与彩色动画观察 P2B

加法连续性覆层。fresh远端main `a46098597bce9d7fd13557d640506cb26ba36b15`、tree
`ff95448cb2fa1a04f1d8fcc64e57a334c6f42992`及最新提交/Actions重新读取；同HEAD
P2A收据运行40238250020实际success。0开放PR、0运行中，旧10-07 queued37642417333保留。
原生Git读取七启动文件、路线、材料portfolio、P2A日期覆层并核其完整字节；CURRENT
2680510B/blob `031c76a5a8e431f646853909bb2f2e11e6328cd2`、SHA256
`f02f85b837fc09973cb2eca33f7daf4db547a77cb35a81a9576c6308f70142c0`完整保留。
不以旧聊天SHA或巨大CURRENT末条的过时NEXT16覆盖较新日期记录。

## 玩家可观察交付与来源范围

将原TW1 SPR三序列的灰度索引预览扩为**同版Palet_0初始化色预览**：25帧位置、16不同位图
仍沿P2A原数值/原像素，新增颜色表来自原程序的初始化规则。可离线前后帧、播放/暂停、调整
人为预览节拍，页面明确显示颜色来源和场景选色未知。原程序全客户端尚未启动；没有助手
亲眼看到原版世界、听到原声或鉴真人物/宠物身份。

本包不是用后代源码猜BGR。认证原 `sa_3.exe`425984B/SHA256
`cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a`，
原 `Palet_0.sap`708B/SHA256
`89709d906bbd9cd9f5c2b8e0bd993e2897a1c9136ada2e211109983bb3b06cbf`。
既有16个SAP文件数量/摘要是旧事实，未当新客户端版本或新增16套已验证场景。

## 三次有限源任务及首轮不足

1. 源40240708206/job121311676734，HEAD `3d9c32e4df5fd32e87f79f75e56a62fe09dc130c`，
   实际success，但直接字符串xref只有RVA0xafb1的`cmp ebp,0x4561e4`。
   这是前一绘制循环的表尾恰好等于下一路径字符串起点，**不能作为调色板读取器**。
   首轮原样JSON保留，historical_color_proven=false不改写。
2. 修订源40240851952/job121312104842，HEAD `6cd151c5b8736b105e48cb32390696738573bc62`，
   实际success，核到16个真实路径指针槽RVA0x56178..0x561b4，顺序Palet_1..15、0。
   原初始化0x96c0通过最后一槽读取Palet_0；0x9b20通过带索引的同表另走目标/渐变路径。
   本包只落地初始化，不扩大到完整渐变、昼夜、地图或战斗选色。
3. 内容源40241350181/job121313616909，HEAD `b0e17c99df96d60c0301f505eac2e06743ff46ed`，
   实际success。除原exe/SAP，核P2A四完整原资源SHA；在显式FILE桩和合成栈/内存下，
   限定执行原0x96c0到0x9a3e（COM前停止），对照参考实现，再实际导出三份私人彩色HTML。

三次均重取同一既认证842125501B `CD_DIC.rar`，原MD5/SHA1校验后提取；这是本包定位纠正、
间接指针资格及像素集成的三次新证据任务，不是三客户端版本，不是无源哈希重复验收。
全部原载荷/嵌图HTML于always清理，公开Git和工件仅保留派生指令/数值/指纹。
原始大包仍没有跨会话私人长期保管，不宣称已永久存有全部官方客户端。

## 已证的原初始化规则

原原生全局表起点VA0x49f5d0，单条四字节。源代码指令/PALETTEENTRY ABI相交的解释如下：

| 范围/条件 | 原字节或指令事实 | 本工具采用的有限规则 |
|---|---|---|
| 索引0..15、240..255 | 0x96c0..0x9924填32个栈上固定项，随后两复制循环写两端 | 从源指令派生32个RGB常量；独立元数据解释器与原指令执行互验 |
| 初始缓存标志=0 | 0x99d3从最后路径槽取Palet_0；二进制模式打开 | 只接受原708B Palet_0的完整SHA |
| 索引16..239 | ESI从0x49f611起，三次读字节写ESI+1/ESI/ESI−1，再加4，止于0x49f991 | 224组B/G/R转RGB，恰用672B |
| SAP尾36B | 此循环未读取 | 不用于着色，原件身份仍核完整708B，不丢尾部证据 |
| 索引168 | 0x9a29/30/37将0x49f872/71/70置0 | 初始化后的168号强制黑色，不使用SAP该位置原值 |
| 缓存标志非0 | 0x99d1跳过读SAP，但仍初始化两端并置168黑 | 不能把每次调用解释成从头重读Palet_0 |
| 表交付 | 原0x9a4c推表地址，0x9a54调用COM槽+0x14；此前参数4 | 静态调用形态符合DirectDraw CreatePalette；本包不执行COM/GPU或声称显示成功 |

字段色名的外部ABI依据：Microsoft [PALETTEENTRY](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-paletteentry)
声明顺序为red/green/blue/flags；[原IDirectDraw CreatePalette接口说明](https://learn.microsoft.com/en-us/previous-versions/ms785027(v=vs.85))
说明其输入为PALETTEENTRY数组。外部API文档不是TW1客户端自身来源；原路径/位移/循环/交付
位置仍由原程序验证。表结构命名有此ABI对应，不把现代Direct3D的alpha用法回填原游戏。

原件PAL0与合成SAP各执行4239条原指令；合成缓存已置位案例执行417条。FILE打开/逐字节读/
关闭被显式桩替代，不代表原系统真实文件IO成功，更不是完整客户端启动。三案原指令结果与
参考RGB逐字节一致；合成SAP含非零168号颜色，能拒绝漏掉强制黑规则。缓存案例原中间项
合成填0xa5，除168外保持旧值，读数0，证明条件不能省略。

原PAL0初始化256色RGB768B摘要：
`e02d929c63d9edce15891c28748758ef8da90d28fed5f525fd86ec73d34364e3`。
32固定RGB96B摘要：`6d145e46e9b7aeadaea6f45babaf4712869071c871314cac6c3fa22d8b4f084a`。
不公布原完整SAP或原图。PNG用索引色PLTE保留原索引，不加透明表；透明色/行方向仍未知。
声音字段不播放；人工预览速率仍不是历史FPS。索引168初始化强制黑也不等于画面上168永远黑。

## 派生保管与代码入口

三个原样派生分别永久保存：

| 派生文件（research/recovered/下） | 原样字节 | SHA256 | Git blob |
|---|---:|---|---|
| STONEAGE-TW10-PALETTE-P2B-INITIAL-TRIAGE-R1.json | 22146 | 0b42d83670d0e951372c6a043066665a97ca9616b4504adbc2163ce01da002c3 | 51485bf1471a3ba3ccfcb5604faa2c246a970dab |
| STONEAGE-TW10-PALETTE-P2B-POINTER-SOURCE-R1.json | 151989 | 9686bdd0a1ee280fcc03873c411027358b3d7a7f34f204cf7ceccfd045b2e6ce | 1cfe121559c172ab7b5e764eb9dbf90dace87edb |
| STONEAGE-TW10-PALETTE-P2B-ACTUAL-COLOR-SOURCE-R1.json | 10821 | 3521274ecb0cc861623c9a8ccc43ec95c2b7c7719f2949e5e611be80a36a4977 | 4569af739f7a54e4a5c0241c894ea5e26cb421fc |

三工件ID12615938664/12616748192/12616784210，ZIP2636/12215/3760B，本轮均实际下载、
校验API ZIP摘要并核唯一成员；ZIP SHA256依次
`e387f9b64050939d2fa1e3592e0e057082b2e6965140c6bb96957800b7d08d2c`、
`8152eebefe0ddd9cb0fa2d08f56a5f67b9e30544bad454a5b5eb367a78f0533d`、
`865698fbe89bf3b76ee9eb7d33b3d60e5794dab47cf864ef16450915b35a648d`。
短期工件过期不丢原样派生证据。实际彩色导出的16张位图，其ADRN/RD/解码索引SHA与P2A
逐项相等，仅显示调色板改变；25个帧出现位置及源偏移不变。

在仓库根目录、私人输出目录已存在时，可提供同版原件：

```bash
python -m tools.stoneage_tw10_palette --original-dir /private/TW1/StoneAge/data --palette /private/TW1/StoneAge/data/pal/Palet_0.sap --spr-no 100000 --direction 0 --action 6 --output /private/observations/tw1-initial-color.html
```

四原图/动画文件和SAP均须完整SHA匹配；输出拒绝公开仓库路径与覆盖既有证据。CLI私人
预览只需标准库，不要求Unicorn或执行原exe；Unicorn仅用于独立源验收。未核SHA的现代资源
不得代替原件。原P2A灰度默认路径与报告保持兼容。

本地35个不同单元（曾有一次导入测试类导致8项重复装载，已修正，不将重复作为新增测试）；
元数据语义反例另核通道、路径槽、固定色、SAP字节预算/缓存、源像素及原程序/COM/场景
过度声明。候选/主线与浏览器结果随后按实际后验登记，不预写成功。

## 本包止点和最高NEXT

P2B在原初始化色表和三序列真实彩色导出处停止，不连扩9b20渐变/昼夜/全部场景helper。
**最高观察NEXT `ORIGINAL-GAME-OBSERVATION-P3-ISOLATED-BOOT-PREFLIGHT`**：先核隔离
Windows兼容环境、32位执行/DirectDraw/显示截图能力，再尝试原SHA程序启动与第一屏取证。
保持原exe网络隔离，不安装旧内核驱动；无资源、兼容失败、登录/原服不可达须分别记录。
有屏幕/输入日志后才能称实际运行；后续mock服务器与原服历史行为分开。本包彩色预览
不证明已进入原世界，也不以像素/测试/耗时给总体完成百分比。

独立内容线`EARLY-OFFICIAL-WORLD-ENTITY-SOURCE-20`仍OPEN，同版名字—实体ID—SPR
新增0；DD-028本体/永久新增/运营活动/起源待考四档不混合。Stage A7 PARTIAL+2 OPEN、
Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、overall percent=null。

## 本轮真实主线终验

内容main `d3e9c141f0fb4db652cf1630a97e82e8a18d083c`、tree
`8ef449ed0716e53fa556a32cf7cea11a6b6e1732`已非强制快进发布。最终候选五项、同HEAD
主线七项Actions均实际completed/success。专用候选40241783089/job121314933439及主线
40241851198/job121315143242通过35项不同检查、原指令/像素源guard与Chrome双模式
像素/自动换帧/暂停/零网络验证；主线P2A40241851186/job121315143054也通过旧灰度
兼容和原P2A源保管链检查。其余R16/R17/R18、P1观察台、Stage A均成功。
主线不重取版权源，也未执行完整客户端。本地35+30项不同测试通过。

15个内容改动路径、全部远端tree与本地逐字节一致；五历史文件完整保留。
永久[发布收据](../../research/recovered/STONEAGE-TW10-PALETTE-P2B-PUBLICATION-R1.json)
记录三原源作业/三ZIP实下校验/三个原样派生blob、全部候选/main运行及15内容文件指纹。
本后验收据自身CI仍需实际观察，不能预写成功；最高NEXT P3隔离启动预检与全部未知边界不变。
