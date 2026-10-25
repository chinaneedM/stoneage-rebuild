# WAYI官方路径sa.exe：实际资源目录与登录画面缺口（11）

2026-10-25（Asia/Shanghai）。有限目标：直接从已验小型官方路径程序读取PE资源内容，确认能否恢复登录菜单、对话框或标签。结果：**8个资源声明、解压后8个载荷可核；没有取得登录画面或界面标签**。不继续扩驱动/通用PE分析。

## 载荷与来源边界

实际一次取得 https://web.archive.org/web/20060915184620id_/http://www.wayi.com.tw:80/download/file/onlineGame/sa.exe ，369152B、SHA256 `4b5a059b45b589b609ca925d210d76838be1e970b805fab3df863b7d563fbb38`，与既有官方fileid335出链完整证据相同。这是已知原件重取，不是新版本发现；2005-07-06列表与2006-09-15捕获分离，目录出链不认证数字签名/完整纯净客户端或TW1/JSS1999版本。

UPX4.2.4工具档590272B/SHA `75cab4e57ab72fb4585ee45ff36388d280c7afd72aa03e8d4b9c3cbddb474193`、实际工具SHA `746af4b1b8c230641d772d6a1ba645f606ac1e7a43951247477f239f29346fad`逐一校验，只解压，不执行游戏或内嵌程序。解压后921600B/SHA `4193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63`亦与既有记录同一。没有下载大客户端或任何原资产包。

## 实际目录及载荷

压缩输入资源目录RVA79409152、长度2112；解压后RVA79388672、长度5352。两者资源(type,id,language)/声明长度完全同一。

| 类型 | ID | language字段 | 声明字节数 | 压缩输入状态 | 解压后状态 |
|---|---:|---:|---:|---|---|
| 1 CURSOR | 3 | 1028 | 308 | UPX1，载荷未资格化 | .rsrc原字节可核 |
| 3 ICON | 1 | 1028 | 744 | .rsrc原字节可核 | .rsrc，SHA不变 |
| 3 ICON | 2 | 1028 | 744 | UPX1，载荷未资格化 | .rsrc原字节可核 |
| 10 RCDATA | 156 | 1028 | 2142 | UPX1，载荷未资格化 | .rsrc原字节可核 |
| 12 GROUP_CURSOR | 104 | 1028 | 20 | UPX1，载荷未资格化 | .rsrc原字节可核 |
| 14 GROUP_ICON | 109 | 1028 | 20 | .rsrc原字节可核 | .rsrc，SHA不变 |
| 14 GROUP_ICON | 112 | 1028 | 20 | UPX1，载荷未资格化 | .rsrc原字节可核 |
| 16 VERSION | 1 | 1028 | 792 | .rsrc原字节可核 | .rsrc，SHA不变 |

压缩区即使能按RVA算出一个有界文件偏移，也不能把那个压缩后片段当原资源；报告对此5条不给载荷offset/SHA。解压后8条各有准确offset/SHA，原来3条直接资源均不变。language1028只按原字段保存，不据此认证运营地区。完整派生报告 `STONEAGE-WAYI-SAEXE-RESOURCE-CONTENT-R1.json` 不含图像/原程序字节。

RCDATA156并非已恢复的登录窗口：其2142B原载荷SHA `0055f1abb78fa42bd706cd8d86eb171c892a5edf4a6aef5b69c3e68e67df8230` 是可静态解析的i386 PE32、5节，并有PortTalk PDB路径片段/NT内核导入名。仅登记格式与标记；不证明驱动加载、运行、功能或历史版本，不扩其调用树。没有导出或提交内嵌程序。

两输入资源目录都没有MENU(4)/DIALOG(5)/STRING(6)声明，**这不证明程序没有游戏UI**：UI可能由游戏自身资源/绘制逻辑或别处数据提供。本包新增界面标签0、登录背景绑定0、原运行画面0。图标/鼠标有字节摘要不当画面恢复；未渲染原版权图。

## 独立验证与接续

有界解析拒绝循环、越界、错误层深、重复键、零长/保留字段、来源错SHA、打包目录及压缩区伪载荷摘要；9项新测试，含既有PE和NPC验收共27项。另以GNU objdump独立比对8组目录声明与长度；其扫描目录长度之外尾数据的告警不当原件损坏证明。源CI仅下载370KB原程序和590KB工具，重放解压/双报告并cmp永久JSON，原程序不上传工件。Actions结果必须按实际后验记录。

最高NEXT **OFFICIAL-CLIENT-LOGIN-SCENE-ASSET-BINDING-12**：只找这个已定SHA程序中ClientLogin所用的明确背景/按钮/图像ID或同构建原始画面证据，复用既有真实资源索引；缺原像素或确切引用就记录缺口，不能从Win32资源目录无菜单推导无UI。最多再一个有界UI单元，之后回22域队列，不展开通用PE/驱动helper。原大包私人保管仍暂停，NPC10官方同构建缺口仍OPEN，DD-028四档、Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、总体百分比null不变。


## 实际发布终验

内容主线3f69733196ed5dad255eed5069c51e4dc02b7aa2/tree384769b51691b20eaa1363f7ee73ee8b6da77082，候选11项、主线12项Actions全部completed/success。候选source40161301931/job121073247479及主线source40161334845/job121073349069均实际下载固定小样本、验工具、解压、解析与cmp永久报告成功；不是只跑合成测试。本地57项相关测试、GNU objdump双输入8声明及所有有资格载荷哈希独立一致。完整报告8094B/SHA1b58005f0d87069ede9469f65fa87ec26a571d704adf990f1e575485e82a39e1/Git blob7f2b154ec95e298508344f56d4edcb9908b8bbe2。未创建原件或ZIP工件，不伪报ZIP摘要；原程序删除，永久Git仅派生元数据。逐运行后验见research/recovered/STONEAGE-NPC10-UI11-PUBLICATION-R1.json；此后验收据提交自身Actions另据实观察。NEXT12及全部未知边界不变。
