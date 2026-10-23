# CN2003 拉多拉与深红地理生态 R86


## R86 — 2026-10-23 CN2003 拉多拉／巴那姆／深红地理生态（内容候选，待双分支验收）

FACT：本轮从新读远端 main `a16fde079936e9fd893f68e8b2941162b7b33030`、tree `85386d8acd448bdc9a8619085022e158019ec285` 启动；495个分支、无开放PR及运行中Actions，旧排队run37642417333未触碰。上一轮候选10／main11检查均成功；八份连续性文件完整读取并与fresh checkout逐字节比对。CURRENT旧前缀2435984 bytes，SHA256 `138babb2a3a29f30bbda5edd9a78e3dcecd3e79ae2e98a2b3f3303cd04de228f`。最高优先项 OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-86。

交付：`research/recovered/STONEAGE-CN2003-LADORA-CRIMSON-SOURCE-R1.json`，SHA256 `98cacbd0c24d93fe1f2c8f1a969a678dfd8ab8c237375c01664e84fb15f1f051`；专用工具／测试／Actions：`stoneage_cn2003_ladora_crimson_source`。版本范围 CN_SINA2003_LADORA_CRIMSON_GEOGRAPHY_EXACT_BUILD_UNKNOWN，仅选取同一2003年门户攻略的地理、生态和世界叙事段落，停止于1页＋1张实际链接示意图，不扩大音效helper。

来源：https://games.sina.com.cn/zhqu/sta/article/2003-06-09/11645.shtml ，标题《石器时代》任务功略-深红洞窟，显示2003-06-09 14:03、作者字段新浪游戏、我要投稿链接，未署名原作者，不认证官方脚本。当前GB18030严格解码59256 bytes／SHA256 `684983365e929e42d7987e86f962ca2d7641e6185c98464cd4788023909fe3ae`，HTTP200无重定向。实际图 `https://image2.sina.com.cn/gm/newgames/0303/images/tuxing0610_03.jpg`，22812 bytes／SHA256 `15f3e751a5828d906815e2b3d514e0d9940e87c52cb2f605789dcd7b2183e9ef`，Pillow完整解码JPEG RGB500×236、单帧，已人工查看。

实质新增：四条登顶路线各3条有向边，7条按正文出现位置分开的地理／生态记录；世界坐标、回廊内坐标、巴那姆地下2楼内坐标分别保存。两个巴那姆入口(295,259)/(388,337)，两个深红入口(45,41)/(26,5)，格鲁西／格鲁西斯原样分存。怪物等级和种类仅为攻略陈述，非可捕宠物主表。吉鲁火山、百余年、伊拉祈祷和不死鸟以奇宝形体现身／被发现后换山顶为世界故事与指南描述，非地质模拟或已观测服务端机制。

图像是路线示意图，非游戏运行截图；8个印刷节点含c120302、c120303、c120306、c120305、c120304、c120308、c120307、c120309及10条箭头单独记录。图共用c120309山顶标签与正文“四座不同山顶”并存，原生地图ID、实例数及几何均OPEN。四洞口与四路线不强行一一映射，推荐80级／成人仪式仅保留关联任务表头语境，不提升为全图准入。

10条目录记录满足7必填字段／19合法集合；game_ids空、仅研究元数据非发行授权。三个父规格和共享解析器钉原始bytes／SHA256／Git blob。41项真实HTML语义改写（排除所有指纹）＋2项隐藏／正文外反例＋外围脚本正例；独立regex/entity生态读取一致。初始本地26项关联测试成功，源回放成功。原始HTML和图像留临时目录，Git仅派生JSON。完整两支任务、送水7/7奖励表、其他配图、本服运行、版本号和原始地图／宠物ID均未恢复。

NEXT：内容候选10项成功后以fresh main expected-SHA非强制快进，再核main11项；永久保存原样CI JSON和完整run/job/artifact/ZIP/raw/blob保管链，加入强制缺失／等长损坏／身份替换拒绝测试，再验收保管链候选与main。阶段A仍7PARTIAL＋2OPEN，阶段B/wiki GATED；savedata R79 PAUSED_NON_BLOCKING。之后 OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-87 优先具名宠物／人物原始内容或具体原始UI交互证据，避免连续扩洞窟路线；若找到同版本实际audio调用实参才重开音效依赖。


### R86 内容双分支实际验收与永久保管链 — 2026-10-23

内容提交 `3c0b80a38ad7cdfc2604496681020b4a7ad126f0`，tree `e4be822c5f6e2e594103d896ca7511deb2b73f72`；候选10／main11共21个实际Actions全部completed/success，专用job初始7tests成功。

candidate: run39934221560／job120349672167／artifact12492434392，ZIP4125 bytes `sha256:369e57a355b72c5795201f05ec71b9b53d3448259546739879e4c041894ea998`；原样JSON28147 bytes SHA256 `4c84646a0e36b39fe938ccf08cb07a036d3296cc658176e3a06b9da6467f2fa9`，Git blob `55cf00fe36db65e10a79079a4c92c59e38340c75`。

main: run39934550590／job120350775724／artifact12492594617，ZIP4125 bytes `sha256:46eea10ea08ed5f94b55df2cb8b2a3b7415ee2a07435863536fede12b767b414`；原样JSON28147 bytes SHA256 `4c84646a0e36b39fe938ccf08cb07a036d3296cc658176e3a06b9da6467f2fa9`，Git blob `55cf00fe36db65e10a79079a4c92c59e38340c75`。

两个ZIP均实际下载核对GitHub digest与长度，成员仅replay.json；CI原样JSON与初始本地回放逐字节相同，输入当前原页／JPEG bytes和SHA256一致。永久保存CI-CANDIDATE、CI-MAIN、CUSTODY三个派生JSON（原始HTML/JPEG不入Git）；收据固定全部21run清单摘要、两个真实run/job/artifact、ZIP长度/digest、raw字节SHA256与Git blob、7份永久证据pin。CLI强制校验；第8项测试拒绝缺失／等长破坏／run和job替换／重复清单／ZIP身份变化／原生ID或运行覆盖抬高。保管链候选及主线仍须按实际Actions再验收。

NEXT最高 OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-87：优先具名宠物／人物内容或原始UI交互证据；版本／本服运行／可捕性仍OPEN，阶段B/wiki GATED，savedata R79保持非阻塞暂停。
