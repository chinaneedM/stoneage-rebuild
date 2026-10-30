# SCENE43 — 大陆2.0原运营宠物网格第85、86格的具名图像来源

2026-10-30。fresh GitHub main `46c3421e21764c83c4a9eaa1e2c703b7fbac0d51` / tree `fc4c32675358289602152917b901e862c00e1cea`、最新Actions成功，0开放PR。按 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 重新取全部启动文件；CURRENT完整Git blob `20050acf279a01555ab06a381dfcdc936bd381a6` 2317179个字符重读、保留原前缀；路线/22域索引/R102、SCENE42主线收据及旧CN2.0/JPN图像R25/R52/R97/R104已查重。阶段一仍为历史复原。

有限目标：**具名大陆官方2.0页面已有名字与图片src的两个未取像素引用，核实当次可复得的2001档案JPEG字节**。来源限定[原华义CN2.0图鉴81—104](https://web.archive.org/web/20011023181629id_/http://www.waei.com.cn/ZHUANQU/stoneage2/pet/new_pet2.asp)：页已在旧R104实得64382B/sha `2c7aea8d0319c2070d5c7590a95bfc892c2463deb76c5b95fca8c281549c76f0`，页来源旧见证不算本轮新发现。旧R104第84/88/89格已真实取得图像；本包**不重复三张**，只选第85格瑞德宝→`img/newpet/84.JPG`、第86格瑞里西尔→`img/newpet/85.JPG`，原同页一行/跨行关系必须严格重播。网页格号不是图文件号，也绝不是原版物种ID。

真实源workflow将只取一个已核2001档案HTML与这两条由旧原父目录锁定的历史引用，记录各次HTTP状态/重定向/实际档案时间、SHA和可解码JPEG元数据；来源不可取则明确记录unavailable而不捏造图片。原网页、原商用JPEG、原游戏程序一概不入公开Git，不认定日本1999/TW1同构建，也不将网页插画算成SPR/实际模型/骑乘动作。

独立代码、8个负例、本次Actions/派生工件与主线验收须真实回读才计成功。若图像有确切字节则永久收据；下一`SCENE44-CROSS-DOMAIN-MATERIAL-ROTATION`停止连续补整批图鉴，优先更直接的可操作世界/明确内容证据，不能把补网页图片数充作整体完成度。原世界尚未进入，Stage A 7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79暂停，overall_percent=null。

## 首次真实源任务后验（2026-10-30）

CI 专项PR `41053616995/job124055513362` 成功，8个合成源错误用例真实通过；原页64,382B完整SHA不变，两幅原JPEG各成功获取、完整解码。来源派生工件artifact `12975293536` 独立ZIP下载，ZIP1560B/SHA `7c3c7e0fdfc0414f44754000858bff60841c7c0d789f29c5c87531957c90b34b`，所有CRC通过；派生JSON4252B/SHA `88cd240e6fa707ebde61c857caf84f3704c95848950200dc1918b2df87536a24`，已另核源页、捕获时间、URL和图像元数据。该zip仅有派生JSON，无原HTML/JPEG。原网页/原图片的视觉人工观察、同版ID和游戏真正运行仍未完成。后续PR主线Actions和最终收据仅按真实结果写入，不提前宣称成功。

## 最终 GitHub PR / 主线验收（2026-10-30）

[PR #57](https://github.com/chinaneedM/stoneage-rebuild/pull/57) 已实际合并；候选HEAD `216a94987e3dbca8a7303a41d2a13bd68a90b7c0` 与主线合并SHA `baf227d63bbef306072bac1b7432277c03ccb06f` tree 均为 `410cc62bc5d782be5d6996366ce72acc8d7454e3`。候选共12项（含一PR独立真实原页与两张JPEG字节重取）、主线11项，远端各次核实全部 `completed/success`；主线SCENE43仅本地已冻结来源与11项负例，不能说主线又实时取原JPEG。

首次专用source run41053616995/job124055513362：8项测试、原页64,382B SHA和两份JPEG实际完整取得/解码。第二次PR run41054000185/job124056809214：11项回归与完全相同原网页SHA/两图片SHA再次成功；第85/86格最终仍为3753B/4494B、实际取档时间20011026013455与20011026013052（两张均不同于页存档20011023181629）。

两份实际下载CI派生ZIP大小皆1560B，artifact12975293536 ZIP SHA `7c3c7e0fdfc0414f44754000858bff60841c7c0d789f29c5c87531957c90b34b`；artifact12975507343 ZIP SHA `9356bbd323d5b3c3b973ff7b4689da2b863b420f43eeb6f32966cd783459302b`。两ZIP CRC全部通过，内部唯一派生JSON均4252B/SHA `88cd240e6fa707ebde61c857caf84f3704c95848950200dc1918b2df87536a24` 原字节逐一相等，永久Git blob `a1d76135462d1fad58e612caea48e3e99bec175f`。ZIP封装变化不代表来源变化。真正原HTML/JPEG依然未入Git。

每个Git文件SHA与23个候选/主线实际Action后验、两个原图片/解码摘要和两source ZIP都永久归档于`research/recovered/STONEAGE-SCENE43-PUBLICATION-R1.json`。本收据自身的Actions需另后验，不在提交前预报通过。NEXT `SCENE44-CROSS-DOMAIN-MATERIAL-ROTATION`，不再连续追查大批网页图片，转可实际理解/进入游戏的上游材料及具名游戏内容来源。Stage A7 PARTIAL+2 OPEN/B/wiki GATED/R79暂停、original world OPEN、percent null 保持。
