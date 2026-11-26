# PET-HIGH-FIRST-80｜后期原PC下载入口身份与访问止点（候选）

2026-11-26。基于 main `b39f159e563788ca46f88ee8d499d4ac4c4cf79b` / tree `5d0ef6cb4249f4ef660a48d9a135036e40d68c84`；精确HEAD Actions 9/9 success，开放PR 0。历史 CURRENT blob `c89e0e33537990aa2132b47c40fef49a985a935c`、2,709,173 B 与已验归档一致（本轮验证身份，不声称全文复读）。承接 [PET79](STONEAGE-PET-HIGH-FIRST-79-CATALOGUE-PANEL-SCREEN-20261126.md)；原始后期客户端、补丁及同部署主档优先，不重复将无日期玩家投稿用于官服数值裁决。

## 直接公开入口实查

| 区域/原载体 | 原始分发证据 | 本轮访问观察 | 边界 |
|---|---|---|---|
| CN 胜思 2011 石灰封测8.5 | [2011-01-13同期公告](https://news.17173.com/content/2011-01-13/20110113105215673.shtml) 的下载链接 http(s)://download.17173.com/27/ | 网页读取重定向 https://newgame.17173.com/game-info-27.html，内容已变成2026-12-04拟公测的新复刻产品 | HISTORICAL_ROUTE_REUSED；禁止以现页面或新包冒充2011原包；未下载 |
| CN 胜思2012公测 V1.200.012 | [新浪下载页](https://games.sina.com.cn/z/sqsd/download.shtml)，内列2012-10-09、1.34GB、MD5 2a1743e07e4f97f1b2e337048918da6a，页面头时间却为2010-11-19 | 从同页点击成都电信1（url_id=38669）、上海电信1（38670）、北京网通1（38666），三个 rd.games.sina.com.cn/redirect.php 入口均502 | HTTP_TOOL_502；仅抽样3个分流，不声称全部失效；MD5未重算，不能把页面头时间当包发布日期 |
| KR Netmarble 2011-08-06 | [同期玩家贴正文](https://lab.welovesa.com/viewthread.php?extra=page%3D2&tid=1326)明确链接 http://nmgame.cdn.netmarble.net/Stoneage/NetmarbleStoneAge120.exe，作者说明用于取得补丁 | 点击原路径，网页读取工具尝试HTTPS后502 | 已知120路径的独立公开帖子见证；不是新版本样本；无原文件、无法核内部版本或官服宠物 |
| TW 后期陶朱 | [2015玩家指南](https://forum.gamer.com.tw/G2.php?bsn=1571&sn=4326)、[2014 PTT帖](https://www.ptt.cc/bbs/StoneAge/M.1410200955.A.AB2.html)、[2016巴哈帖](https://forum.gamer.com.tw/Co.php?bsn=01571&sn=283215)索引摘要 | 原帖本轮403（包括另一个2013安装包指南页面 https://forum.gamer.com.tw/G2.php?bsn=1571&sn=4156）；https://www.stoneage.tw/download.php 与 ?c=1 均不可通过网页工具读取 | 仅索引线索：Sa_Free_installation、Launch、199/205版本称呼均不作认证；无直接安装包 |
| 未定地区/2022 repost | [公开转载正文](https://lab.welovesa.com/viewthread.php?extra=page%3D2&tid=3826)只称官方客户端，链接 http://pan.baidu.com/s/1gfFzDb9 | 点击后不可打开 | 未验发行商/地区/版本；不能并入陶朱或原官服 |
| JP 2003 1.74a | [2003-12-17窓の杜](https://forest.watch.impress.co.jp/article/2003/12/17/stoneage.html)，[2003-12-12 4Gamer](https://www.4gamer.net/news/history/2003.12/20031212000000detail.html)已有分发报道 | 本机尝试 stoneage.to 和已登记 file2.gamania.co.jp/sa/sa174gm.exe，分别DNS失败和解析超时 | 既有来源，非新样本；本机访问环境问题不能证明外部原件灭失 |
| KR早期 GameTime | 已登记 http://www.gametime.co.kr/images/Online/pds/2001/02/onlStoneAge.zip | 本机DNS失败 | 不重开已穷尽的早期CDX支线 |

网页工具访问错误与本机DNS失败分层保留；没有原HTTP响应体或SHA可用于新的原件收据，没有运行任何下载程序。新浪三条入口共享同一重定向服务，不能计作独立三个客户端。原载体不存在与本次访问受阻是不同命题。未新增原客户端字节、原宠主档、同部署实际发放或正式字段；3,015位置与67取得余缺口径不变。没有把任何新复刻、手游、私服专属内容或未认证转发纳入历史名录。

**NEXT** 暂停上述入口的重复访问，只有明确可读取原文件或新的独立保存入口才重开。优先查后期陶朱官方公开可读的更新包/原始文件清单、同期具名实际取得证据，或已有私人合法保管的后期载体中尚未提取的同源主档，先查原件可达性再做字段回填。若没有新原件，推进既有67项取得余缺中有具体同期运营来源的记录，不重复无版本投稿筛查。PET唯一活动模块，2026历史游标OPEN；Stage A 7 PARTIAL+2 OPEN，B/wiki GATED，R79暂停，总体UNKNOWN。候选需实际CI验收，不预称主线已接受。


## 2026-11-26 独立复核与更正（PET80B，优先于上表）

原候选502ed7cfb4255a8609864ec5f8b0fe3e2b0f1a2c两项Actions均成功（45766822806、45766822829），但任务分别为O12音频和O11源合同，不能验历史网页。独立重新打开2011-01-13 17173公告正文并点击原下载链接，实得403 Forbidden；本次不能重现上文跳转新作的说法，故将该项更正为HTTP_TOOL_403，**不采纳已跳转的结论**。新浪2012包页面正文复核，成都38669和上海38670实得502；第三分流及上表未在此次独立复核复现的台湾、日本、本机DNS等观察一律保留为未独立重验的前轮记录，不作为新验收依据。韩国2011-08-06原帖正文与NetmarbleStoneAge120.exe链接复核，点击为502。无需再轮询这些地址。

## 两项具名取得参考（不改严格缺口）

直接读取2012-02-09 [胜思运营材料新浪全文](https://games.sina.com.cn/o/n/2012-02-09/1338581086.shtml) 可见正文251–264：胖达利、胖达多以参与日常活动累计荣誉值后在荣誉商城兑换；公告称胖达利风火，胖达多水火，未给精确比例或兑换所需荣誉数量。正文273同时述8.5及2.5服务器，未独立确定兑换功能所在服号。非实际兑换日志。

对照固定PET15主表 Git blob fec03646d7c7e4e287f9347c306119cc626d6abf，PET49剩余队列及PET46映射：

| 队列位置 | 模板 | 图号 | 保存主表地水火风 | 原行SHA256 |
| --- | --- | --- | --- | --- |
| 68 | 108 胖達利 | 101719 | 0/0/50/50 | e7617d882dc1b8e84a198540be6f31712ccec19f7c58ae871d8d54277501da42 |
| 75 | 115 胖達多 | 101720 | 0/50/50/0 | c55e86429f8a24e687eadfe681e7ef3ddd24fd19125605531445367767d69f41 |

两者与保存TW85四程序原名/图号均相合；历史运营文章只支持元素类别及荣誉兑换宣称，不支持比例或同部署身份。证据级别 PERIOD_OPERATOR_ACQUISITION_CATEGORY_COMPATIBLE_RATIO_UNKNOWN。两位置仍在67严格余缺中，不改变PET49精确元素比例门槛。不得向早期版本倒填荣誉商城。2003新浪7.0玩家资料70750.shtml以及17173 sa70_11.htm的奇肯沃/奇肯克奈泪之海Lv1说法无元素比例，PET49已有同类上下文，非新增合格取得。原HTML字节/散列未取得，来源为实际可见网页正文。零新原件、零正式字段闭合，队列3015不变。

NEXT：优先按已具名同期来源核对剩余67模板的精确元素及取得证据，尤其2005年玩家对旧图鉴的引用与原运营公告交叉验证；已取得原载体可访问时优先同源主档。不要重复未取得的链接或无比例投稿。PET唯一；候选修订须验收，不预称已合并。
