# PET126I｜2006年玩家已记录的八个宠物名：2019活动不可误作全球首次

**日期：2026-11-21；唯一活动 PET，限定原经典 2D PC。** 新会话远端基准 `e2ba4c7538642a7e849f9006cf9de277571a5df1` / tree `56f91a9c5711a60428829b77d38d686ebec3d89f`，原 `docs/CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c` 保持不变。本轮先确认上一批 PET126H 27/27 主线 CI 已成功，然后对两个未合并宠物 PR 和原客户端来源重新分层。本记录为[机读收据](../../research/recovered/STONEAGE-PET126I-2006-2019-EIGHT-NAME-RECONCILIATION-R1.json)的文字说明。

## 2006 到 2019 的实质早年来源关系

未合并 [PR #532](https://github.com/chinaneedM/stoneage-rebuild/pull/532) 保留一个主线尚未整合的证据：2006年11月29日台湾玩家在[《第二代聖獸活動》配方回复](https://forum.gamer.com.tw/G2.php?bsn=1571&sn=3132)中列肥龙／海怪各四个名字，与既存主线 [PET116 的2019玩家暑假攻略](STONEAGE-PET116-TW2019-SUMMER-MIDAUTUMN-PLAYER-EVIDENCE-20261118.md)及[原帖子](https://forum.gamer.com.tw/C.php?bsn=1571&snA=81239)同名字。两网页本轮直开均 403；对照依当前搜索索引以及PR#532中已登记文字，不冒称本轮取得原完整HTML。

| 2006玩家分类 | 文字相同的四个名字 | 2019玩家分类 |
|---|---|---|
| 肥龍 | 奧普薩斯、利普多爾、邦克普斯、拉佛洛斯 | 端午活动回述「肥龍」 |
| 海怪 | 畢格艾斯、裘比斯、阿卡西斯、洛可洛斯 | 暑期活动「海龍」 |

**确定的是“玩家文字首次可见年份不能写成2019”**：8/8个字面名称在2006玩家材料已见。2019说“当次新增”不能被当成这八种宠物全球首次推出；2006的「海怪」和2019的「海龍」也不能仅凭类目文字不同认定为改名/变种/同种。**不能确定的是** 2006融合配方实际执行、2006官方实服发行、两个年份同一原生 PET ID、图像SPR、成长、技能、奖励或真正首次开放日期。用户要求只整理官方真正发行的宠物，故上述八行**仅为待原端复核的已有名称历史来源，新增已认证官方物种为0**。

## 历史PR和原客户端下载来源的实际限度

- 旧 PR #532 曾在2019年度审核尚未完成时写 `2019=NOT_YEAR_AUDITED` 并建议下一项PET117；**不能整体合并该分支**，否则会回退目前主线已经通过的 PET118 六区年度审查。只带入上述2006名称反证，以主线 `2019=SOURCE_BOUNDED_REVIEWED`、`historically_complete=false` 为准。
- 韩国论坛 `NetmarbleStoneAge120` 的游客访问要求登录，且旧 [R27](../../docs/specs/STONEAGE-KR-NETMARBLE120-R27.md) 已核为原客户端资格未明的阻断来源，不请求登录/付费、不算取得韩服2000原包。
- 2003华义中国原版客户端下载页面仍可读历史入口，仓库 [SINA下载目标报告](../../research/recovered/STONEAGE-SINA-DOWNLOAD-TARGETS-R1.txt) 早已记录准确FTP文件名和失败检查，本轮没有新的原安装包/补丁成功下载，不重新计成果。

**验收状态与NEXT：** 新可验证客户端下载字节0、同构建原PET主档ID/SPR/技能0、官方实服新发宠认证0；本轮新增的只是避免2019历史宠名误归年的可追溯旧证据。2026仍 `NOT_YEAR_AUDITED`，PET仍 `SOURCE_BOUNDED_PARTIAL`，Stage A 7 PARTIAL+2 OPEN，B/wiki GATED，R79 PAUSED_NON_BLOCKING，总体百分比 UNKNOWN。下一 PET126J 审理旧 PR #545 的 TW1 CP950 精确文字来源与已有 PET126D/E 是否重复，先验证再决定取舍；PC官方真正原件仍是最高内容来源优先级。
