# SCENE40：一页新浪玩家物品目录的原字节取得门槛

2026-10-30。前序 SCENE39 已有限止步并转向第17域 item/equipment/economy。在公开网页阅读中找到一条此前未归档的玩家投稿：《石器时代》物品大全，署名“游民部落网友本田太郎提供”，真实出链 `https://games.sina.com.cn/handbook/0101/01186086_c1.shtml`。网页可读三条斧头价格与已保存SCENE14/24混合2.5原商店数值相合，**但这是玩家资料而不是官方运营配置**；不认证台湾1.0／JSS1999同构建，不据URL `0101` 推出首发日期。新浪页面2026可读状态≠历史原版字节已取证。

原混合保存版商店ID0小斧頭成本65、ID4萊伊卡Lv1斧頭成本105、ID10普通普通的斧頭成本260，是SCENE14/24已有事实；不能算本包新物品、新价格、新原图。新增候选仅是一个可能独立于后代保存原表的、具名玩家投稿**物品名称／标价／购买地**的交叉文献；准确HTML体量、整SHA及原作者日期在远端独立取源前保持UNKNOWN。

本候选只提交专用一次性源验证workflow：通过HTTPS要求精确URL、完整200响应、GB18030无损解码、显式署名及三条名字/属性/价目/购买地的一致性后，输出仅派生JSON（原HTML不放Git）。失败就记录真正HTTP/解析错误，不伪装新证据、不得合并为历史定论。原客户端／SAAC／GMSV没执行，Stage A7 PARTIAL+2 OPEN／Stage B/wiki GATED／R79暂停／总百分比null与SCENE34私有源通道阻塞保持。


## 独立源回放的真实结果、原始失败与本包止点

实际PR #54 首轮源run41045491149/job124028435974 failure：36KB原文包含非法GB18030字节，严格解码止于原偏移24995。按失败实情修为surrogateescape保留10个非法字节，不修改网页、不以替换字符伪装无损。再次运行41045626824/job124028879852 success：精确最终URL，实际回放原文 **36312B**，SHA `d1fbdacdb50b9b31c0068e270d7026550ea6764f577cc9df3641d20df3432bfb`；三目标行0编码异常、字段验证全过。首次失败与原源没有倒写。

实际下载唯一派生工件artifact12972795452：ZIP922B/SHA `9ad3e6b5e56ba8d05475e638f21be5773b4f3e860fe87094b05649da425d74ce`，独立CRC通过，JSON1980B/SHA `7b011d43ffde2a3104fe1e219b1d5312c296493ec8d7434706ea3fa1676c0f86`。详情见[新内容合同](../specs/STONEAGE-SCENE40-SINA-AXE-PLAYER-CROSSSOURCE-R1.md)、`research/recovered/STONEAGE-SCENE40-SINA-AXE-PLAYER-REPLAY-R1.json`与`STONEAGE-SCENE40-SOURCE-CUSTODY-R1.json`。原HTML与商业保存原行不在公开Git。

新源是当前可取的**玩家投稿**，不是当年官站/同构建服务器证据。三个旧物品和旧成本没有“再次发现”，新增只为该玩家文献当前正文及其购买地点说法的有界归属。没有实物买卖、战斗、登录或原世界。下一`SCENE41-AUDIO-EVENT-SOURCE-DELTA-REVIEW`，22域18；仅查未保存的真实声音→事件绑定，不继续扩全商店与声卡helper。保留Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、overall_percent=null、原boot具名阻塞。新候选CI与最终主线合并须后验确认，不预填成功。
