# PET-DETAIL35｜2002—2003具名宠物史料与保存5.0 PC相簿的七项精确联接（2026-11-23）

## 问题、材料和边界

PET模块仍是唯一活动模块。最高待解问题为早期官服同部署**宠物主档、出生/成长、技能、真实获得与同构建原图像关联**；本轮未取得新的可核早期原服务端字节，按照协议§24从已保存较晚的原PC资源进行有界追溯，**不重复计算此前已取得的来源为新证据**。

本轮启动主线 `2706d5e64b70a5d98efe2bc53a25051a6a386e82`、tree `e41bbe210422ac3e6b460426d89ad3b6772b75a4`；检查该HEAD最新12项Actions均成功、未合并PR零，重新读取协议与项目工作记录。原大型 `docs/CURRENT-STATE.md` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 原样保留。

- [PET61 2002年四项年兽玩家具名](../../research/recovered/STONEAGE-PET61-CN2002-SA30-SA40-OPERATOR-PLAYER-PET-EVIDENCE-R1.json)：Git blob `1c0bcbfc64c5cbfdaaef7bbd65f27c80dcbd8692`；同一来源单列玩家报告，未证四个运营方独立物种。
- [PET25 2002机豹艾迪希洛和2003蒙奇发行文献](../../research/recovered/STONEAGE-PET25-OFFICIAL-RELEASE-ROSTER-R1.json)：Git blob `168e3fd24000ac02e2c2d02cdbb6a03850570df5`，运营产品文案/发行活动，与原生个体到帐不同层次。
- [PET66 2003-12-17大陆7.0朱雀菲奇亚竞拍预告](../../research/recovered/STONEAGE-PET66-2003-TW6-CN7-PET-SOURCE-R1.json)：Git blob `5772982b59c8082b60712e66c8b79c15940019c5`；竞拍公告不等于已交付。
- [PET126R 后期保存大陆5.0 PC原编译相簿](../../research/recovered/STONEAGE-PET126R-CN50-PC-ORIGINAL-ALBUM-FULL-362-SLOT-SOURCE-CATALOGUE-R1.json)：Git blob `8b1058a43c267dfeaa298d4c2c472209cebd24d9`；362行来自保存CAB的原EXE派生读取，**保存包本身尚非已独立认证的当年原样官方发行压盘**。

## 精确同名，不能当作同宠身份

| 较早记录年 | 同源字面 | 该年证据资格 | 保存CN5相簿原槽（0基） | 实际可升级的资格 |
|---|---|---|---:|---|
| 2002 | 葛雷吉鲁 | PLAYER_NAME_CLAIM | 283 | 原生Pet ID／图形未证 |
| 2002 | 葛雷洛比 | PLAYER_NAME_CLAIM | 282 | 原生Pet ID／图形未证 |
| 2002 | 葛雷马恩 | PLAYER_NAME_CLAIM | 284 | 原生Pet ID／图形未证 |
| 2002 | 葛雷基欧 | PLAYER_NAME_CLAIM | 281 | 原生Pet ID／图形未证 |
| 2002 | 艾迪希洛 | OPERATOR_RELEASE_DOCUMENT_EVENT | 296 | 原生Pet ID／图形未证 |
| 2003 | 蒙奇 | OPERATOR_RELEASE_DOCUMENT_EVENT | 294 | 原生Pet ID／图形未证 |
| 2003 | 菲奇亚 | CN70_AUCTION_PRELAUNCH_NOT_DELIVERY | 295 | 原生Pet ID／图形未证 |

完整原记录偏移、原行SHA-256、相簿内部数值及各历史网页由[机器七项桥接](../../research/pets/PET-DETAIL-EVIDENCE35-CN2002-2003-NAME-TO-CN50-ALBUM-BRIDGE-R1.json)保存。7/7具名行逐字匹配，**0/7具有可证原生姓名→SPR映射或原官服Pet ID**。那七槽用旧“台湾1.0序号公式”在同CAB均找不到对应SPR组，**只否定这个公式的候选连接**，不能推导宠物缺图或从未发行。

特别的历史版别张力：`菲奇亚`在这份标签为“保存大陆5.0”的本地名单中出现，但可核的同期运营宣传属于**2003大陆7.0朱雀竞拍**。并不能据此推断5.0已经实发、原保存包后期被改过，或原7.0是它首次出现；需要官方同构建压包、原EXE日期/来源及原生选择器链的独立核证。

## 原索引守恒与下一项

保存CN5原编译相簿总数为**362槽／305具名／57空**。后181槽均具名且内部不重复，假设SPR存在仅66、未命中115，均不构成原服物种数；槽353「宠物蛋」是“有名字≠活宠”的直接反例。台湾1.0永久 `PET-000001—000124` 档号不变，不发放无依据的新永久号。新获官方同服主档/技能/初值/成长/捕捉为0；项目整体完成率UNKNOWN。

专项回归检查验证七项逐字、正确原行SHA及四个独立历史来源对象、181/66/115守恒、七条假设SPR未命中、蛋类负控、运营发行/玩家传闻/预告各层严格分离。原创商业客户端、图像和服务端字节没有写入公开Git。

**下一最高优先 PET-DETAIL36**：只对可免费合法读取的原PC 3.0/4.0/5.0/7.0官方客户端、补丁、服务器宠物主档或后版同构建原生姓名→SPR/ADRN选择器进行定点查证；已认证或可核验材料优先。仍不可获得则保留缺口及重启条件，不扩无关模块，不复写后期私服配方作原规则。PET ACTIVE；Stage A 7 PARTIAL + 2 OPEN，B/wiki GATED，R79 PAUSED_NON_BLOCKING。
