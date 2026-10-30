# SCENE42 — 已知新浪5.0下载页的早期辅助程序版号行核验

2026-10-30。启动 fresh main `3863ab795454505337235ff3907e1dc00097ade7` / tree `2c774d0c8ae17ac4af7e4c70a457b78ca7eeac10`，最新SCENE41 source+合并后验已独立成功，0开放PR；README/协议/当前完整 blob `20050acf279a01555ab06a381dfcdc936bd381a6`、设计/年表/资源册、路线、R102、R103及旧STA2.52/2.53与SADE来源均已核。SCENE42领域19只取一份有确切标签的辅助工具历史版本索引，不下载执行工具/不设计内挂。

原证据页面 `https://games.sina.com.cn/zhqu/sta/ltxs/sqxz.shtml` **并非新发现页面**：已于2026-09-24按 `SRC-CN-2003-SINA-SA-DOWNLOAD-HUB-01` 登记，过去重心是地图包及客户端入口。此次新缺口是原网页“石器时代外挂下载”表中的四个具名标签及真实同表链，先严格核材料而非再造整个站点。网站自标2003-04-03 15:38，但如今正文还有4月6日比赛场次，故日期只属网页可见标签，**不能证明表格于4月3日已经存在或程序在该日发布**。

待现场核验四原标签：`SACHXP++5042`、`SACHMX5.00B8`、`SACHMX5.00FREEB1`、`小明蓝暴自动猜谜器`。与R103经两篇2003-06-18新浪页实际核的`SACH-MX5.00B9会员版`做“不同标签”对照，不自证B8→B9升级日期、程序同字节、软件供应方身份、可操作功能或与TW1/大陆1.82同构建兼容。最后一项仅是下载标签，不能证明猜谜任务自动通过或任何题库内容。PDF/攻略帮助文件SachXP++ help beta1.2与此程序名完全不同。

专用 workflow 只取同一个HTTPS网页，UTF8/GB18030唯一严格解码、日期/来源区、四行同一真实table及原同排锚点逐条核对，输出派生JSON，不访问历史FTP或任何可执行文件。若表格不符/源错误须如实保存失败，不能以阅读网页的解释代替原字节。原游戏尚未进入，Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING、overall_percent=null。若有限核验通过则转22域宠物具名官方图像来源；本轮所涉外链与先前研究不会被误称原官方游戏。

## 首次真实 source Action 与历史字节的准确发现

2026-10-30，PR`#56`最初专用源Action `41050466902/job124044938887` 已完成SUCCESS。Sina页面实际GB18030严格解码69464B/SHA`812b32be4c9e9df45b956826c5a2a566d644ee8ef9acff5cfb69ab962a1b6a1d`，四标签确实在**一张原HTML table的四行**，各两条原链接（历史FTP+HTTP镜像），未访问任一程序。9项语义边界单测成功；派生JSON3153B/SHA`6b5b9a3f9b91a17ee8546936e588db81de8c09248040a3fafeaa09e7150539c3`，独立下载ZIP1221B/SHA`c06d533adfbda783aefde830fcf6e17641ce73407fc18f6f163ad925f9650767` CRC全过；下载项原字面包括`%2B%2B`不可改写成其他命名。

[正式来源合同](../specs/STONEAGE-SCENE42-2003-HELPER-DOWNLOAD-LABELS-R1.md)及`research/recovered/STONEAGE-SCENE42-SINA-HELPER-DOWNLOAD-LIST-R1.json`按精确报告冻结。待合并main的PR新源重取、候选+主线Actions及最终收据必须以实际结果为准，当前不预报全部成功。下一`SCENE43-OFFICIAL-PET-NAMED-IMAGE-SOURCE-REVIEW`；Stage A/B/wiki/R79及原boot事实不变。

## PR #56 主线终验与来源永久保管（2026-10-30）

[PR #56](https://github.com/chinaneedM/stoneage-rebuild/pull/56) 已经合并；最终候选`140c721f6c6beeab44c806b63cadeab503e2ace2`和主线merge`e00bc5a22f15dda67d32d99d8ad52390ed098057`的tree完全相同`a4ff6be3354c72eafad545ebaca05f3f57dce322`。候选12项相关Actions全 completed/success，主线11项全部success。首次真实源`41050466902/job124044938887` 9项验收通过；最终PR源重跑`41050958313`的12项负例和源HTML完整SHA、四原表行/8同排href通过；主线只验证保存派生/反例，不冒称当时又实时访问可执行文件。

首包与最终包ZIP皆1221B，分别 SHA `c06d533adfbda783aefde830fcf6e17641ce73407fc18f6f163ad925f9650767`（artifact12973893129）与 `315f2a5dd39ac835f6d7ac8407837d988c937dd7626df17e3bc3d4f0d04b37bc`（artifact12973873600）。两个工件均独立下载验全部CRC：内部3153B派生JSON/SHA `6b5b9a3f9b91a17ee8546936e588db81de8c09248040a3fafeaa09e7150539c3`，逐字节一致，Git blob `b270c9106e4ded5e236e68f12301e03c5fc403e2` 与已发布远端文件完全同一。ZIP壳摘要变化不意味着原网页/派生JSON内容变化。

[完整23项主线+候选验收、8条文件blob和原来源保管](../../research/recovered/STONEAGE-SCENE42-PUBLICATION-R1.json)永久入库，原HTML及任何外部可执行程序0B入Git、exe未请求/未运行、原游戏没有进入。后验收据自身提交的Actions不可提前预言，另据后续实际状态。新增4行8址/不同版号旁证，绝非原已发布时间或作弊功能真实可用的确认。

下一最高`SCENE43-OFFICIAL-PET-NAMED-IMAGE-SOURCE-REVIEW`，回官方宠物名称→来源图像证据；Stage A7PARTIAL+2OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING、原boot blocked、总体percent=null原样保留。
