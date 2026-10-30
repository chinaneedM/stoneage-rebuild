# SCENE42 — 新浪 2003标签下载列表里的四个早期辅助工具名字和八条原下载地址

## 本轮原材料范围

来源 https://games.sina.com.cn/zhqu/sta/ltxs/sqxz.shtml 已作为`SRC-CN-2003-SINA-SA-DOWNLOAD-HUB-01`于2026-09-24在资料册登记（当时主要取MAP/客户端路径）；**本次新增的是原页“石器时代外挂下载”表的四个程序标识与八个同排链**，不是一个新网址、不构成八个软件下载或四个程序镜像独立作者见证。

实际原网页现时HTTP200，无重定向，**69464B**/SHA256`812b32be4c9e9df45b956826c5a2a566d644ee8ef9acff5cfb69ab962a1b6a1d`，GB18030严格完整解码。真实原表为四行并列，单行包含所列工具名与两项下载href，未请求八个目标URL。原页面署新浪游戏/2003-04-03 15:38，但正文同时列出“4月6日”武道大会成绩/场次，说明**署期不构成其完整内容当日历史字节见证**。尚无可认证当日快照、该版首次发布日期、下载文件SHA或开发者自证。

## 逐行保留历史版号与地址，拒绝字节等同升级

| 页内标签 | 下载点一（FTP原href） | 下载点二（原HTTP href） |
|---|---|---|
| `SACHXP++5042` | `ftp://211.90.133.5/dowload/sa/sachxp%2B%2B5042.exe` | `http://www.wuxitianlong.com/sa/sachxp%2B%2B5042.exe` |
| `SACHMX5.00B8` | `ftp://211.90.133.5/dowload/sa/sach-mx5.00b8.exe` | `http://www.wuxitianlong.com/sa/sach-mx5.00b8.exe` |
| `SACHMX5.00FREEB1` | `ftp://211.90.133.5/dowload/sa/sachmx5.00freeb1.exe` | `http://www.wuxitianlong.com/sa/sachmx5.00freeb1.exe` |
| `小明蓝暴自动猜谜器` | `ftp://211.90.133.5/dowload/sa/xiaoming.exe` | `http://www.wuxitianlong.com/sa/xiaoming.exe` |

这8条是**网页里的原字面历史指针**，不是经过存活检查/安全审计的现在可执行文件下载推荐。没有主动访问任何exe或获得代码；路径`%2B%2B`原样保留不能静默改成加号甚至别的程序。FTP和HTTP镜像声明并不证明二者有相同文件体或安全性，也不能称双方当年真实可访问。

已完成[旧R103 SACHMX版本资料](STONEAGE-SACHMX-VERSION-VISUAL-R103.md)确认新浪另两篇自标2003-06-18，会员版写`SACH-MX5.00B9`，免费版写`6.0B1`，该两页当时实际核了两张全尺寸UI图片、18次不同版别列项。这里5.00B8和5.00FREEB1仅为新来源**字面版本名**；它们与六月篇的5.00B9/6.0B1，不保证版本后继、免费功能继承、发布时间序、同一可执行程序或对应官方游戏build。

`SACHXP++5042`与`SACH-MX`只记录互异标签，不能把同代名字相似抬成相同产品/作者；`小明蓝暴自动猜谜器`的用途仅由下载名称所声称，既不验证题库、正确率也不说明当时原服接受过自动回答。2003新浪`SachXP++ help beta 1.2`为电子攻略帮助文档，不能和`5042.exe`程序等同。2002 SADE早期分版、STA2.52、STA2.53及R103旧资料均未记录本次四行的具体文件名；这是新**版本/文件名归属**而非功能首创或原游戏行为。

## 真实核验和保管

已完成专用 Github PR #56 初次源 run`41050466902` job`124044938887` **completed/success**，9个原结构边界与误归类测试通过；原源完整字节结果固定。下载派生 artifact`12973893129` ZIP1221B/SHA256`c06d533adfbda783aefde830fcf6e17641ce73407fc18f6f163ad925f9650767`，全部CRC通过，内JSON3153B/SHA256`6b5b9a3f9b91a17ee8546936e588db81de8c09248040a3fafeaa09e7150539c3`。永久机器文件是`research/recovered/STONEAGE-SCENE42-SINA-HELPER-DOWNLOAD-LIST-R1.json`，其Git blob独立回读后验补记；HTML/程序未入Git。

冻结重放器`tools/stoneage_scene42_sina_helper_listing.py`、边界单测`tests/test_stoneage_scene42_sina_helper_listing.py`、专用workflow仅在 PR 重取此一页面并校对已有派生报告，不去取可执行文件。主线同版源复取不重复；若原网站发生变化，拒绝自动更新同身份的旧数据。旧图像和WAV资产不复制。

## 正式止点与下一项

这次仅关闭22域19中**一页已知下载源的4行可核名单与8原href**，没有补全16家族目录、没有实际游戏内挂能力执行、没有恢复游戏世界、没有新生产程序、没有总体完成百分比。Stage A 7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，原客户端boot仍`BLOCKED_PRIVATE_INPUT_CHANNEL`。

下一`SCENE43-OFFICIAL-PET-NAMED-IMAGE-SOURCE-REVIEW`：从22域9/10的具名官方宠物图像，先排除R97/R104已核栏目、跨版本网页序号重复与旧源图，限**一条**可追溯名字→原图片链接与确切网页归属；若无原图或同构建来源则记录缺口，不延伸某个外挂的低层功能树或收集所有客户端。
