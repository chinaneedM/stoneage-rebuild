# SCENE31：一组原台湾1.0人物资源的八方向完整连续帧

2026-10-30（Asia/Shanghai）。加法续接；原CURRENT全文及SCENE26–30记录保留。本包恢复**原body候选100000、动作码2的完整逐帧可视材料**，不是原客户端世界执行或新增游戏设计。

## 启动与有限目标

重新读取 fresh GitHub main `34a826a327b46a63de3eab3a4a21b39fc45e6d27` / tree `f51662a3cc93e3ac8e18d07738e4e23f4a55e7b9`、678远端分支、最近提交/Actions、0开放PR，七启动文件的完整Git字节、R2/22域/R102与SCENE30最高NEXT。SCENE30收据自身40967247790实际success，内容主线11项已验，未沿用聊天SHA推断。CURRENT2708031B / blob `20050acf279a01555ab06a381dfcdc936bd381a6` 完整重读且不改；README旧全文119724B为追加前缀。

在22域中选择 character_sprite_model：SCENE23对十二候选只看每方向第0帧，本轮限其中**一组**的完整序列，不扩十二组全部动作。停止条件是一组八方向全原帧、原图资格、独立像素/画面验证和可私人查阅的离线观察器。原世界DAT路线继续按SCENE30止点，不再下载同一零售盘或扩大安装器/驱动helper。

## 来源、实物与新增范围

来源仍为已验台湾 Waei/JSS 1.0零售Redump104630样本；本轮没有新增版本、服务器资料或原游戏运行。既存P3H372626292B包整SHA256 `3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24` 重新认证。原EXE425984B、SPR2889630B、SPRADRN5568B、ADRN10079680B、REAL315842228B及两SAP708B逐成员完整SHA核同既有原库存。原EXE的R16 body数值窗口仍以全SHA和128B窗口SHA认证；100000只是原body候选数值，不是姓名、官方可选角色数或头像绑定。

原SPR组100000恰在0–6128B，104条动画，整段SHA `14755bb80693c1b22d6f394714d2166da8150f467223bc8595f49456b851fceb`。其中动作码2有唯一八方向，各6个有序原帧，duration原值600；全部48个位置/48个不同bitmap，无重复位置。与SCENE23相交的是8个原首帧，**本次新增实际观察40个后续位置**，不把全部48或过去已知序列当作新发现。源帧四字段、顺序、偏移和整动画段SHA与旧已钉原资源元数据全同。

实读48个原RD共69275B，解得125612个原索引像素。生产解码器与不同RLE实现全索引同一；独立复核程序另从原SPRADRN/SPR直接解析完整104条组、选出八段，不依赖生产选择函数或旧CSV来重造序列。另一个RD实现、两份原SAP BGR变换、倒行和index0透明候选生成的96份RGBA/PNG，及96个240×260完整候选画面，全部逐像素/摘要核同。源图、原RD子集和候选拼图只私人保存。

实际目视两配色候选之一的48帧整张拼图：为红发人形，蓝色衣着，八方向各六姿态，后续姿态逐渐俯身/横卧。这是画面描述，**不认证死亡、受击、行走或其他原动作名称**。原FPS、duration单位、运行时色表/透明/朝向选择、原生锚点和官方人物姓名均仍未知。

## 观察页与浏览器证据分开

私人HTML内嵌96候选PNG，具八方向、两个候选色表、六个原帧位置按钮、上一/下一帧、现代180ms播放/暂停/复位；无外部依赖和音频。frame顺序与原四字段保留。原图PNG已通过独立解码回读、完整画面由独立程序核同；内联JS语法已检查。

**原图页没有浏览器成功记录。** 本轮Cloud Browser打开本地 `file:` 页面时，被URL策略明确拒绝：只允许http/https。没有改用HTTP服务器、其他URL、raw CDP或另一浏览器表面绕过这一拒绝。实际原图浏览器资格保持false，不把尝试说成执行成功。更安全的替代是独立静态原像素/画面核验，以及公开CI只用**全新合成像素**测试相同研究控件。合成浏览器结果须按真实远端后验记录，不能反证原图页曾运行。

14项新来源/顺序/缺帧/同数异图/假FPS/身份晋升反例通过，连同既有SCENE23共38项本地检查通过。源安全公开程序严格重放已钉SPR/ADRN表与冻结的实际原像素收据；`source_action_run_id=null`，公开Actions不读取私人原包，不能称新实源取图。

## 私人成果与永久派生

`SCENE31-private-original-TW1-actor-sequence.zip`，739204B / SHA256 `fdb992cf892c77e57ae88179ddf21a5c0daea5af275a2c99843d8cefa21f7642` 已成功保存并应用版本身份。包内为离线HTML、两张48帧候选拼图、来源/独立验收、RD/SAP私人子集及中文打开说明；不含整客户端或世界地图。保存后未再次下载，不能冒称保存后的第二次耐久SHA。

公开Git只保留：`STONEAGE-SCENE31-ORIGINAL-ACTOR-SEQUENCE-R1.json`、`STONEAGE-SCENE31-INDEPENDENT-ORIGINAL-PIXEL-REPLAY-R1.json`、`STONEAGE-SCENE31-LOCAL-ACCEPTANCE-R1.json`，程序/模板、负例测试和此记录。源派生报告SHA256 `b410371d979c1763e933c5a398087f806777534955e7796e1ac387acef7056e9`；原像素元数据规范化SHA `a8fd5030382f821875fa0f4ff40ead4a5e7303b716f090535c7388033bfd8a0f`。原EXE、RD/SAP、PNG、完整私人HTML不入公开Git。远端提交/tree、Actions和临时合成工件保管按实际验收另记。

**原版可操作世界仍未进入。** 本包不扩大到官方角色目录、全动画、原服规则或全部资源恢复。Stage A 7 PARTIAL + 2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、overall_percent=null保持。

## 最高下一包

**SCENE32-RETAINED-NATIVE-FRAME-QUALIFICATION**：停止继续扩此人物动作。按22域优先复用已有P3H包内的三张**原EXE运行窗口保留画面** `frames/original-frame-0.png`（1122B）、`original-frame-1.png`（1135B）、`original-frame-2.png`（1122B），及private-source-report.json41836B。旧P3H实际运行记录说明原EXE曾在隔离Windows启动、出现640×480窗口并退出，但 `assistant_viewed_original=false`；原图已经保存而其可见内容仍缺实际阅图归属。

下一只核这三张既存原图与原P3H运行记录的完整SHA/原成员身份，实际目视是否为有意义的原界面、空白/异常或无法归属内容；重复画面保留，不能把非均匀像素当作已进入游戏。若有可辨内容，记录其精确可见范围；没有则具名止点回22域，不继续模拟登录、驱动或无限窗口helper。不得把现代SCENE观察器当作原运行截图，也不将这些启动阶段画面称为进入原世界。不重新下载零售盘、不联系已停服历史服务器或使用真实账号。
