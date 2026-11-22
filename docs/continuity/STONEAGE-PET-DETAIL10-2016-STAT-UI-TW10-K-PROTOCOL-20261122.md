# PET-DETAIL10｜2016年后期PC源码的四项基础面板属性投影与台湾1.0原K接收协议对照

日期：2026-11-22。现阶段严格经典2D PC-only，PET唯一活动模块。用户要求先从已经掌握的真实程序和服务端资料恢复宠物数据，而不是无限次引用玩家攻略。

## 远端最新状态启动及事实源

本轮重新获取远端 `chinaneedM/stoneage-rebuild` 默认main HEAD `b42a8ef4806d7fcf548ee5909f54353ab9a47ec1`、对应**真实根tree** `b625e8c2b0ec70f6f96b60c2337991e660009eed`（由GitHub git/commits对象获取，而非猜测）、两个父提交、近期提交和原合并PET09；重新读取连续性协议§26、README、宠物目录、模块约束、设计决定、此前PET09收据及完整原 `docs/CURRENT-STATE.md` Git Blob `c89e0e33537990aa2132b47c40fef49a985a935c`（原2,709,173字节；contents file接口大文件返回空，使用Git blob读全文、未重写），原PET09候选Actions已21/21通过、无开放PR。此前资料和SHA只是入口，启动本次以上述远端事实为准。

## 本次真正新增的源码与跨源数值内容

再次直接读取**后期2016社区PC服务端固定提交** `pimpcapital/longzoro-sa@57b14e2bb373ba851c14db28a239273e4a8831bb` 的 `gmsv/src/char/char.c`，源Git Blob `5a044dc68bb76758b2a757a8e83c10b93578be31`；在 `CHAR_initcharWorkInt` 与 `_CHAR_complianceParameter` 处追到内部能力换成基础`WORKMAXHP/WORKATTACKPOWER/WORKDEFENCEPOWER/WORKQUICK`的真正C语句，结合上轮已核验同提交`enemy.c` `ENEMY_createPetFromEnemyIndex`四BASE与十点随机分配，为全部TW1来源124份同图数字对应的**195条后期2016候选模板**计算**780个单项的有理数理论上下界**（各4种属性）。每条保留原模板ID/行号、后期原数值、原2016同提交来源索引SHA、源公式系数及最终字段缺证flag，方便逐宠查看。

公式均为**2016后期PC源码数学基线**，V/S/T/D为之前已核出生的`CHAR_VITAL/STR/TOUGH/DEX`内部整数、非玩家直接可见值：
- 基础最大HP：整数截断`(4V+S+T+D)/100`；
- 基础攻击：整数截断`(20S+2T+2V+D)/2000`；
- 基础防御：整数截断`(20T+2S+2V+D)/2000`；
- 基础敏捷：整数截断`D/100`。

本轮为每一个指标独立取随机偏移最小/最大值以及共10点按最小/最大系数分配；**4个指标不能同时各取最大值**；C源码包含浮点常数，HP还有`float`中转，当前数学有理数结果尚非位级确定的原C编译程序上下界，且`ITEM_equipEffect`和`Other_DefcharWorkInt`等作用未证对所有原生宠物无影响；绝不称其为已验证实际出生面板HP／攻击／防御／敏捷。举例后期模板1同图号`100250`四BASE `20/12/15/25`、INITNUM=10，模型四单项范围`MAXHP 12–18`、`ATK 1–2`、`DEF 1–3`、`QUICK 2–3`，**不是**早期台湾1.0乌力的官方数据。

## 原台湾1.0客户端与2016后期PC服务器协议的新关键隔离

读取前轮早期本机审计 `research/recovered/STONEAGE-PET126E-TW10-K-STATUS-CAPTURE-STATIC-R1.json`（原`sa_3.exe` SHA-256 `cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a`、20字段本机偏移直接验证）并直接读取2016 `char.c` 的 `CHAR_makeStatusString case 'k'` 服务端发送程序。

- 早期客户端收`K<slot>|1|`的20字段原`token2..21`；其中token2..19这18个数值字段图形、HP、MAXHP、MP、MAXMP、EXP、NEXTEXP、等级、攻击、防御、敏捷、忠诚、4元素、技能槽、改名标记与2016后期服务端发送顺序相符。前18项位置属于独立代码边界，不能由此推断原数值也相同。
- **token20** TW1本机接收期望宠物**名称文本**，而2016后期PC服务器`case 'k'`实际在token20插入了`CHAR_TRANSMIGRATION`的**整数**；后期`token21`是原名、`token22`是玩家自定义名。若开启`_SHOW_FUSION`，转生后又插一融合标志，名称再后移。**不能宣称2016后期K整包与TW1原客户端兼容、不能用这个后期端“直接运行台湾1.0官服玩法”。**
- 这只是两个各自原代码源级静态比较，原TW1客户端未在本轮运行，也没有早期TW1同构建官方服务器K发送程序，所以原官方原始K格式的服务端实现仍OPEN。保留早期客户端结构和后期服务器行为各自来源。

## 产出、拒绝推定与下一步

[124份逐宠后期属性数值参考和协议对照](../pets/TW10-124-2016-BASE-UI-STATS-AND-K-PROTOCOL-CROSSWALK.md)；[机读780条候选范围／早期K20字段对应证据](../../research/pets/PET-DETAIL-EVIDENCE10-LATER2016-124-HP-ATK-DEF-QUICK-AND-TW10-K-BOUNDARY-R1.json)；新独立回归测试逐一复核124×195原输入及数学式，首只样例对286个十点分配组合×16组偏移极限做穷举确认，保持历史CURRENT Blob及永久PET档案不变；现有PET CI合并前验收。此工作没有引入新原版官服服务器、没有给早期TW1同版起始范围／成长／自带技能／抓捕地做认证、没有新增官方宠物物种或新原商业二进制。

**当前状态**：124份原TW1具名图形来源档案全部PARTIAL、完整历史验收0，2026 PC年表仍`NOT_YEAR_AUDITED`；PET唯一活动、StageA 7PARTIAL + 2OPEN、StageB/wiki GATED、R79 PAUSED_NON_BLOCKING，整体完成率UNKNOWN。原CURRENT不动。**NEXT PET-DETAIL11**：继续免费公开、合法可取的1999–2002原PC同构建官服pet master／真实出生值或原K服务端发送程序调查；找不到时停止过度解释，不以2016可算数学值冒充初代官服；先补原TW1客户端有据静态收包/画面连接，再视新实物推进。不涉手游、私服专属、收费卖盘，不切NPC/装备。
