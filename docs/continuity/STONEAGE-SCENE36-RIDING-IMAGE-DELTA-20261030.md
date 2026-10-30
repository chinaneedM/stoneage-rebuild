# 2026-10-30 — SCENE36：骑宠旧材料查重，一处未取图像引用的实际增量

从fresh main `9134642b24c5a87ed9ec785161ecc581cb6bcb18` / tree `eb20d110203710555ac52a15131e6cc16542a3d3` 启动，重新核默认/分支HEAD、完整6580项tree、最新五提交、0开放PR、最新收据41006768562实际completed/success，读取协议、七启动文件、路线/22域/R102及SCENE35最新覆层。完整CURRENT2708031B / blob `20050acf279a01555ab06a381dfcdc936bd381a6` 与fresh Git原字节相同，README旧124313B完整保留为追加前缀。本覆层依协议14追加，旧捕获时状态与历史结论不回写。

**结果：新增骑宠资格/规则0，新增官方原网页的一处图像引用关系及两份实际JPEG资源。图像实际为室内NPC对话窗参考，不能称新手赠骑已兑现、骑师资格UI或原游戏执行。** 不是首次取得任何NPC窗口图；既有WN/卡坦等来源的有限结果保持。

## 五份已有骑宠材料不重复计数

| 已有来源 | 当前已存内容 | 本轮处理/来源等级 |
| --- | --- | --- |
| 大陆2.0骑师/骑乘战斗 | 适骑查询、人物课程、忠诚100、骑乘入口和有限属性叙述 | 2001运营商旧页，规则已有，不补费用/等级上限/权重 |
| 大陆4.0证明书/庄园 | 证明书、流浪骑师、九庄园服务表与坏字节 | 新浪门户材料，运营商原作者未认证，不冒充独立官方原文 |
| Wayi新手骑宠计划 | 栏目索引标2003-12-10，实际2005捕获；弱虎/易忠诚为计划 | 官方运营商栏目，计划不等于实装，两个图片URL当时未取得 |
| Wayi计划续篇 | 索引标2003-12-23，矿石研究者工作线索与叙事 | 官方栏目，未证明赠虎的具体实施，不继续翻所有专栏 |
| 台湾8.0证明书/装备 | 两具名骑宠、分类装备、一张状态窗参考 | 新浪转引巴哈，未认证官方作者；图片已阅，不把它当本轮新增 |

五原报告逐整SHA绑定于新机器报告。它们是五份已存研究输入，不是五项新增历史发现或五个独立原服见证。22域第15域仍PARTIAL_DESCENDANT，早期骑宠成员、资格全表、同构建人物动作绑定和真实事务不因此闭合。

## 原网页与新增图像的精确来源

复取已认证的[官方栏目原页归档](https://web.archive.org/web/20051117143741id_/http://www.wayi.com.tw/stoneage/producer/producer02.asp?idno=66)，19964B / SHA `b1f2163b80137e2140c36a6675a42e4ac1f2e3cc367e08b2a850cd15a6261790` 与旧报告完全相同；实际正文捕获20051117143741，不把索引所标2003-12-10认作这些字节或图片的生成日期。网页工具返回不可访问错误后，普通HTTP读取成功；不是安全拒绝后的绕行，也没有浏览器页面或原HTML脚本执行。

原HTML只在一处实际链接结构中出现这两个目标：外层a.href=`http://www.wayi.com.tw/images02/sa1210-1.jpg`，内部img.src=`http://www.wayi.com.tw/images02/sa1210-2.jpg`。所以是**一处anchor/inline关系、两个资源位置**，不能计成两篇独立来源或两幅独立原生观察。

| 角色 | 请求策略与真正返回捕获 | 原字节 / SHA256 | 实际尺寸 |
| --- | --- | --- | --- |
| a链接目标sa1210-1.jpg | 先请求正文20051117143741，实际转至[20061022095340](https://web.archive.org/web/20061022095340id_/http://www.wayi.com.tw/images02/sa1210-1.jpg) | 91133 / f96377883b93a5b12f10a78167b97f2e1a98c4651ad8aa3754161fa05a7ad9f7 | 640×480 |
| img页内资源sa1210-2.jpg | 同样先请求正文时点，实际转至[20040611050307](https://web.archive.org/web/20040611050307id_/http://www.wayi.com.tw/images02/sa1210-2.jpg) | 44719 / ad370b462462769dcfc8bc9430b648f6faf990101cdfec3c71e94871be7ac06f | 300×225 |

捕获时间码按实际resolved URL记录，不把请求的2005时间码、文件名sa1210或栏目2003日期替换进去，也不称已找到最早捕获。页内图与大图视觉构图相近，但尚未证明是同一母像素的缩放/重压缩；两个不同整文件SHA、两个捕获位置均保留，不去重丢其一，更不认证同日/同构建或2003原始像素。

## 实际目视与不能随图建立的事实

两原JPEG均真正打开查看。640×480图可辨室内石墙/木梁等布置，以及覆盖场景的半透明NPC对话窗，按钮标签为“確定”“取消”；300×225图保留相似构图。没有做整段对白转录、坐标测量或角色/物种识别；被对话窗遮挡部分的骑乘状态不作判断。

新分类为 `INDOOR_NPC_DIALOGUE_WINDOW_REFERENCE`。未建立骑宠资格界面、新手虎发放、适骑对应、忠诚/等级数值、具体NPC/任务ID、任务奖励/旗标或对话已执行。不能把旧文章“计划”和“跳30级”叙述投到这张图上充当实际交付/奖励证明，也不能和SCENE35社区包NPC坐标/对白混成同一构建。新增骑乘规则仍为0。

旧报告 `unacquired_image_refs` 和coverage=0保留为2026-10-19当时事实；本日期覆层明确记录后来取得这两份资源，不通过把旧0改成2来抹平历史。没有因旧未取得标记而忽略后来实物，也没有借新增图像倒证过去的运行。

## 字节、图像与交付核验

三份实际HTTP源共155816B；网页19964B严格Big5且整SHA同旧。两个JPEG均HTTP200/image/jpeg，原SOI/EOI/SOF独立标准库头读取与Pillow尺寸/分量/精度相同，实际解码RGB摘要分别：

- 链接目标：`3f243591b9ed0755a20c15521b8b74313c8cdc4105bc40cec4db80f71b7aca05`。
- 页内资源：`006eb1e5f74a4f8cc9bdf6c039803b98762bae4db115a36266d28986759a3b07`。

这是独立头元数据核对加一套实际像素解码，**不是两个独立完整像素解码器**。初次本地探针对Pillow JPEG对象读取不存在的n_frames属性，打包前停止；改为JPEG格式限定及getattr单帧缺省后重跑，不改原图、不重取载体，不把失败写作图像损坏。

私人交付 `SCENE36-private-Wayi-dialogue-image-reference.zip` **248813B / SHA `2180dde3e1d346ba1fba48cd3affa72f80d9ae66bb73c27de8a50496acc27506`** 已保存，最新身份元数据已应用；保存后未二次回读，不声称耐久副本二次SHA。含现代静态reader、两原JPEG（共135852B）、来源摘要和派生报告，共六成员。交付不附整篇原HTML；它只在本轮本地源分析中读取。两原图未重绘、裁切、补字或图生图；reader嵌入字节逐件与原JPEG全等，无JS或外部请求依赖。未进行浏览器执行认证，不绕过此前本地文件URL的浏览器止点，也不把静态查阅当原客户端运行。

原JPEG、整页原HTML和私人reader/ZIP不入公开Git。公开为 `STONEAGE-SCENE36-RIDING-IMAGE-REFERENCE-R1.json`、`STONEAGE-SCENE36-PRIVATE-IMAGE-AUDIT-R1.json`、范围说明/工具/反例。29项新检查和28项SCENE35回归本地通过；公开CI仅核派生、合成JPEG头和合成载荷，不取得原图片/页面、不浏览原资源或运行游戏，source_action_run_id=null。候选/主线Actions按真实后验另记。

## 下一最高与停止条件

本包到此停止，不继续扩图像缩放/帧工具、两篇专栏剩余图片或骑宠helper。新手赠骑实施重开仍需精确版本的官方任务规则/客户端实物桥或原运行证据，这两JPEG不提供该桥。五份旧骑宠规则保持各自地区/版本/来源等级，不把全部说成官方原文。

**最高下一：SCENE37-QUEST-MATERIAL-DELTA-REVIEW。** 回22域第8域，先读已有 `STONEAGE-ADULT-CEREMONY-SOURCE-CONTRACT-R1.md`、`STONEAGE-ADULT-QUEST-ORIGIN-QUALIFICATION-R117.md`、`STONEAGE-CN-KATAN-QUEST-SOURCE-CONFLICTS-R98.md` 及其源记录，并查长毛象货运/入门任务资料是否已有相同交付。只选一条具名任务中尚未保存的资格/步骤/奖励原文增量，优先同期官方；若使用同期署名玩家稿，必须单列其等级与冲突，不升级为官方原服事实。明确区分本体任务、永久版本任务、运营活动与来源未定；源不足则具名止步并轮换，不从截图补脚本/ID/奖励，不重跑出生地模型或R79。

原SAAC/GMSV启动仍 `BLOCKED_PRIVATE_INPUT_CHANNEL`，没有新私有输入能力；原世界未进入。Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、overall_percent=null全部保持。

## GitHub实际后验验收

[PR #51](https://github.com/chinaneedM/stoneage-rebuild/pull/51)候选`e516c1c377256d430d2d47455dd92648985c6836`的12项Actions全部completed/success；临时合并`8d3e30fb379bdea40eeaff17f54a472574f176a1`的tree与本地`cdc88b70cba0c12804a69050b34ed1dad550b61e`相同。fresh main仍原启动HEAD后，按协议既有授权合并为`4eba384481de6a9d1a856e04d418456de1fb7916`，实际merge tree再次相同；其11项主线Actions也全部completed/success。专用PR run41010540896/job123915173793和main run41010656600/job123915531634日志均实际见29tests及new_riding_rules=0/original_world_entered=false，不能拿CI派生报告测试充当原图HTTP/像素取得或游戏运行见证。

完整23run、7文件整SHA/Git blob、原网页/两原图分时摘要和248813B私人包身份见`research/recovered/STONEAGE-SCENE36-PUBLICATION-R1.json`。额外一次本地回归复跑误写不存在的模块名而import失败；改用实际SCENE35模块后57项全过，未改源/用例，失败不冒写成功。本收据提交自己的后续CI尚未在此预先认定；NEXT37与所有证据边界不变。
