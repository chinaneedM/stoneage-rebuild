# INTEGRATION57｜吉鲁两族31205原人物配置、原地图与同载体144幅真实RD：独立实物复验（2026-11-11）

## 目标与来源顺序

按最新正式[INTEGRATION56验收](STONEAGE-INTEGRATION56-PUBLICATION-ACCEPTANCE-20261111.md)的NEXT，本工作离开梦幻洞窟、恐龙牧场、矿工、三龙和道场，审查原`QUEST11`“两族误会”中原`31205`相邻两角色的实际视觉来源。**原游戏内容仅限历史复原 Stage A**，不扩引擎、网络账号、合成交易或原版玩法优化。

远端基线main `e66f847cfcf32865a4b1acb1d5da8039bef09d20`，tree `ba1d840b3e7d878da7c48069bd1b84725ee85879`，按协议重新读取默认分支/提交/Actions、七启动文件、完整原`CURRENT-STATE` Git blob及最新验收与组合队列。原`CURRENT-STATE` **2,709,173B／blob `c89e0e33537990aa2132b47c40fef49a985a935c`完整不改**。

## 实物回读：比同数字跨版本候选更强，但仍不是同部署执行

- **任务/地图原件**：私人`StoneAge-QUEST11-two-tribes-original-private.zip` **264,869B/SHA256 `99002423db31754c514863da018b112adcb7252eabce17cb112c42b815150a49`**，**56/56成员CRC**。内部`source-evidence.json`与正式Git blob `d1248d3a1976332f57eab46d7a09d854075c3805`一致。真正重读原`garunaev1.create` **1,983B/SHA256 `014b99bdb836d775f56fc7e84a3f8ff400cdb3d58eb1792d49877a440929be35`**；序号2/5的完整源块SHA复核，以及原`garunaev3`、`garunaev6`分别13/15原TYPE静态段。
- **地图DAT真格**：同包`original-DAT/31205.dat` **3,758B／25×25**，SHA256 `5fb967a40557cb185ee9402beb35e2b2e51e56a356dec6c6285cc0a101c2ed3d`。按文件头8字节宽高+三组不交错小端uint16平面重新取值：美鲁原创建`100250`于(12,11)为`4015/0/49152`，加洛`100252`于(12,12)为`4003/0/49152`。这是原保留字节与原NPC配置点，不证明真正站立、碰撞或绘制。
- **同一社区混合载体的图形素材**：私人SCENE13动作0原包**975,186B／SHA256 `21b56fe9a49357f0d7815698bd1db67f72076759a2528348888fe06444868238`，6/6 CRC且原内嵌208RD子ZIP可读，原派生报告与Git blob `85b20adf2af267fb0433c50f4172fec554cf0aa5`完全一致。原图形100250/100252在SCENE13/R40/CHAR05已验全SPR段散列分别为`eb1a87cd4cc8e3b409990783c7bcc3bc463acab4cac7d2d961127d899da047ef`与`eeb2ec4546277c2acdf1b43fff7967c4c0fe5ac5c019bb7d68a901e134691b0a`。本轮不重新打开混合RAR原完整SPR本体，而是精确复读已保存R13源RD和内联原PNG。
- **原像素数值**：100250的8方向共有72源帧位置／64不同bitmap；100252的8方向共有208位置／80不同bitmap，合计**16方向序列、280出现位置、144不同原RD/PNG**。144份原RD原字节SHA、PNG整文件SHA、RGBA像素SHA及尺寸**144/144逐项一致**；原重复位置不丢弃、不把源duration字解释为真实毫秒/帧率。本轮无新RD重新解码（新解码0），是重新实读旧合格完整来源并第一次关联该具名任务角色与图形及原场景。
- **私人资料可观察性**：独立打包`StoneAge-INTEGRATION57-Giiru-two-tribes-same-carrier-motion-private.zip` **869,340B／SHA256 `f43c0bd3a7ff16a2a580ec9a7d024bceb58ab20e31175618a9f174b727306a99`**、297成员：原DAT、两原脚本、源CREATE、144RD+144PNG、现代原资料对照HTML及逐SHA来源清单。实际上传**个人Library /石器时代/** 后独立重新下载，整包字节SHA和所有297 CRC、144 RD/PNG/RGBA源SHA匹配。Chrome/Chromium本地16个原方向切换及真实图像载入成功，0脚本错误、0外网请求。**现代资料页不是原商业游戏截图/原生交互**。

## 同源资格与不可晋升事实

这比前轮台湾1.0跨样本同数图更进一步：NPC文本、地图原DAT、R13宠物动画源已记录在**同一份混合2.5社区保存RAR**内。但文件共存并不证明它们曾在同一个原官方服务器部署运行，亦不证明引擎一定用该图播放NPC动作。这套保存资料**不是已认证官方原版**，不能回填JSS1999、台湾1.0或大陆1.82。两CREATE不等于两官方NPC身份，144位图不等于144种宠物，280帧引用不等于280不同图；`garunaev3/6`中命令、海螺/矿石/手环与任务标志均只是静态原脚本，真实选择、结算、奖励及接触行为未运行。

原著作权图片、DAT和脚本字节只在私人Library，公开Git仅[源限定数字/位图SHA/原帧序](../../research/recovered/STONEAGE-INTEGRATION57-GIIRU-TWO-TRIBES-31205-ORIGINAL-RD-SOURCE-R1.json)、回归及本连续性覆层。阶段仍为 **Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING、overall_percent=null**。

**NEXT：** 结束31205和图号100250/252这一来源闭环。下一包优先别处尚未整合的**原地图+具名原NPC功能/任务+实际有源视觉图块**；若没有原商业字节，留出精确缺口并转另一来源充足内容模块。不再扩本角色原动作、模拟原战斗/传送、重做观察器或为新游戏做设计。

本包候选及主线Actions是否成功必须按真实GitHub结果另记，不能用私人原图验证替代公开CI验收。
