# INTEGRATION52｜原1021百人道场地图与NPC 300原格源关联：正式发表与主线后验（2026-11-10）

## 远端继续基线、原始资料和唯一新增关系

严格重新检查远端 `chinaneedM/stoneage-rebuild` 原main HEAD **`170ac8e871831d5df038197af64f1101257856ea`**／tree **`f5175fccc02eee4d69fe12f3ebf2272a8ef5e309`**、最新提交/Actions/开放PR（0）和连续性协议及指定文件、模块与离线优先文档、[INTEGRATION51收据](STONEAGE-INTEGRATION51-PUBLICATION-ACCEPTANCE-20261110.md)。大 `docs/CURRENT-STATE.md` 文件接口返回空正文，但Git原blob接口**实际读回完整原文本**，Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`；本轮未覆盖其任一字节，合并主线树后再次认证仍为**2,709,173字节、同一blob**。README仅末尾追加，旧历史完整保留。

本轮从私人旧MAP09观察包 **46,844,444B**／SHA256 `d84d0800dd600798769dfb7251a1d7816588ac061ccc27812ac64a37922d4a8a` 实际重新完整包SHA/4,195 ZIP成员CRC、nested 955原DAT全CRC（内包SHA `c079a1c25bfa11902b69c1f2839058d4fb20f025ef15c93f649f636c7e5f833a`），再读1021、1022、1008三个真实原DAT，逐完整字节及原SHA与此前MAP01/MAP09源资格一致。对已验I51后期社区混合2.5原CREATE的**100个1021对战者/200个独立Warp**的300个坐标逐原DAT复原三平面字面；点互不重复且平面0值均大于99、平面1全为0；保留第三平面不解释。进一步从原TW1已保存PNG/图块校验137个原图别名，重放道场关1/10/51/100、入口1022(1,7)和终点1008(20,20)六幅**私人现代候选局部**，外加100点原创建坐标叠加缩略图。目标格原字面1022(1,7)=`[4085,0,49152]`／1008(20,20)=`[5046,0,49152]`。

这些是**原游戏内容位置×原地图格×旧有原像素候选**的新增精确关系，并非新发现DAT/RD像素、原客户端游戏截图、历史官方同服或真实100关战斗胜利／碰撞／传送执行。地图与NPC载体是保存后期社区mixed25，原图像是台湾1.0独立载体；3021.DAT旧档案CRC读取失败原样保留，绝不以1021代替。具体与全部SHA/格值见[来源与私人画面记录](STONEAGE-INTEGRATION52-DOJO-ORIGINAL-DAT-PIXEL-OBSERVATION-20261110.md)和[公开来源索引](../../research/recovered/STONEAGE-INTEGRATION52-1021-DOJO-ORIGINAL-MAP09-300-CELL-PIXEL-SOURCE-R1.json)。

## 私人原图保存与权限边界

私人 `StoneAge-INTEGRATION52-1021-dojo-map-NPC-source-private.zip` **3,050,639B**／SHA256 **`717a5af82fe66e47d0b929b25546be41f41282889f377beeff3a974703b95563`**，13成员全部CRC通过，Library `/石器时代/`已上传；本轮在上传后**从Library独立实取回包，整SHA/全部字节一致，13成员CRC再次成功**。私人图库JPG亦单独存入Library；含源回放脚本、四关卡、入口、离开地点、100点地图概览和来源收据。商业原资产、原NPC源脚本、原DAT/RD/原PNG、候选私人图像均**未进入公共Git**。公开CI不处理商业私人原包，仅回放来源限定数值与摘要。

## 候选—PR—主线的真实验收链

- 从原main创建候选 `agent/integration52-dojo-source-map-pixels-20261110`，候选HEAD **`d51892a16e5f22d4b3584c456abe0ce4a3070f97`**／tree **`daea9add3e501ffbc835104a0a9833a714976461`**，比较 ahead=5, behind=0，仅五条公开路径：纯数值JSON、12项源码/摘要回归测试、专项Workflow、来源说明、README末尾指针，无原版权文件和历史正文替换。
- 候选push **27/27 completed/success**，I52专项 [run 42847192763](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42847192763) 成功。PR [#320](https://github.com/chinaneedM/stoneage-rebuild/pull/320) **19/19 completed/success**，I52专项 [run 42847748960](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42847748960) 成功。所有PR工作流成功且mergeable=true、clean、main仍原起点时才执行squash合并。
- PR #320合并后的**内容主线** HEAD **`b78018819ef05d07b71510abb761c9e60853aca7`**／tree **`daea9add3e501ffbc835104a0a9833a714976461`**，与候选tree逐对象相同。合并后main push **27/27 completed/success**，专项 [run 42847921028](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42847921028)／job **129940331138** 实际job日志：**`Ran 12 tests in 0.006s`、`OK`**，全部12个用例逐条`ok`、无失败和跳过。成功后才记录本验收收据。
- 本**验收收据自身**是正式成功之后的独立加法提交，不冒称该收据HEAD自身已运行CI；此前PR/主线运行历史不得覆盖。

## 即时止点与NEXT

1021源地图与百关NPC/双传送门的**原始三平面数据和原图候选局部**已完成有界关联；**下一包应转别的游戏区域/可看见的原物品/宠物/NPC/真实任务链**，只接受来源合格且有新增实际玩家可见内容的有限材料。不要因为还有99关可以逐一剪图就继续凑截图数，也不要借旧数字推早期官方物种/原版可玩关卡。证据不足就将缺件标OPEN并切另一模块。

Stage A保持 **7 PARTIAL + 2 OPEN**；Stage B/wiki **GATED**；R79 **PAUSED_NON_BLOCKING**；overall_percent=null，不启动新作引擎/账户/联网方向。
