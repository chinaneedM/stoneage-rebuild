# INTEGRATION92 — 五兄弟地下城 30 原NPC、五奖励角色与台湾1.0 原二维图（2026-11-13）

## 启动与内容增量

重新读取远端 `072604a3620bb2da2f7666d7895059baa86ed349` / tree `fe8ded71b96bb0386bb78a17350920608195b48e`、Actions **26/26 success**、0 PR、连续性协议与原 `CURRENT-STATE.md` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` **2,709,173B**，历史原文保持不变。源限定后期社区混合2.5 NPC/脚本与另一来源已认证台湾1.0原SPR，不能推同一官方部署或 JSS1999/初代1.82 玩法。

QUEST20 先前已恢复 `giiru/event/ev28.create` 30个原静态NPC位置、30份不同原事件脚本、六原DAT尺寸与五组 GetPet/WORLD21 既有关系；本轮**不是发现新任务或五种新宠物**，新交付是把30原静态点位和5角色原SPR方向0动作0/2/1的**86张经原RD解码的既有真实PNG**集中到私人浏览器并逐张字节SHA严格重验，使玩家可见的源证据真正对应旧数值关系。

## 原始文件和五个奖励原数值关系

原私人NPC ZIP 995176B/SHA `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f` 2205/2205 CRC真核。后期原 `npc/giiru/event/ev28.create` 5199B SHA `35616eedb62b5fe5fa8c04a9d978bee7c0808ed092ce3fb6040f78e076ad74ce`，30原 byte-spans 每段各自SHA，串联全SHA `631de481048dc198297defb8f4648c9f13144e7bdb3c02281dacefc8a87535d9`；30不同脚本共30333B逐源SHA/CRC，按路径排序sha链 `25fc014b4b4aca9e5688325aca27a0233a866370e01004471413b74e32520134`。公开CI只复用既有QUEST20派生源记录核其可见部分，不伪称公开仓有完整原文件。

六楼 NPC静态创建数 **6、3、5、5、6、5**；原几何为前四层50×50、第五层50×70、第六层50×80，均为旧QUEST20实际核过的DAT尺寸，**本轮没有新读原DAT各格，也没有恢复原地形、碰撞或实际玩家路线**。原五层选物静态要求2507/2509/2511/2513/2515与原任务异常按QUEST20保留。第六层配置关联：

| 原NPC | 图形原数值 | GetPet敌人实例→模板 | GetItem |
|---|---:|---|---:|
| 利諾恩 |100287|54→91|2518|
| 吉諾 |100290|57→94|2519|
| 奇洛斯 |100288|55→92|2520|
| 浦洛斯 |100289|56→93|2526|
| 浦魯德 |100394|481→95|2525|

这些 GetPet 和 enemybase 数值是旧WORLD21/QUEST20已经存在的后期同源证据，数字相等**不证明台湾1.0同服任务已经领奖，也不认证早期官方物种**。

## 独立台湾1.0实物二维与负证

再次实际读取已有私人 PET07 原图库 HTML 15123277B SHA `58e8ee4ff5165ed2f61663d67ae1cd0a8183622fa3375c480232784bfce9dc76`、真实RD逐原块收据报告1617404B SHA `b5ad2e58930afbe90604a1d72e3c17ab0adea446e7c118be775e3973315e6cb4`，五组原SPR完整段的原 SHA 与[公开PET07数值表](../../research/recovered/STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json)严格一致。五组各有**56源动画头，共280头元数据**，但这里只选择每组方向0/动作0/2/1 **15段可视帧**，原123帧位置、86张不同源位图，不谎称280段已经本轮逐帧可看。

本轮把既存原PNG嵌入源页逐张 decode 成真实PNG byte，再与PET07原RD导出的候选PNG SHA对核：**86/86一致**。源86 PNG SHA按bitmap号串联链 `507f4209bfb226566970887ac397eb6554467d40b807d17510954b11e7fac0cb`、86源 RD 块 SHA串联链 `b22b2f65bf582abe0617797437a40c68be5531e1773ac4dae3deaf7485ee2a6c`；**新原RD解码0**。原色盘选择/原播放时序和原音效仍未知。

## 私人可见观察包与浏览器实际验收

私人ZIP **660522B** SHA `b734904c42a8228e6b3127997d33440a39a5446dfa4a1360f5eee4c55e880d50`，**36/36 CRC通过**，内含30份源脚本完整私有副本、源CREATE、完整私源hash清单、HTML内86既有原像PNG、非原生坐标图与浏览器实测的现代观察页截图；保存于个人Library `/石器时代/StoneAge-INTEGRATION92-Five-Brothers-six-floors-five-original-2D-private.zip`，已独立回下载 **同660522B／全SHA相同／36/36 CRC通过**。原 HTML **553221B** SHA `a97967788e73cdbad598a9ba132112e2b7a306aa3cfac1032e2754682e9b4b73`。Chromium 144 真实 page.set_content 测六楼6/3/5/5/6/5个静态点位、5图形×3原动作共15可加载源图、15下一帧，0JS错误／0外部请求；不假称file://已直接打开或客户端原生游戏执行。

原商用截图、原RD像素、完整 NPC正文、玩家原版可操作图与私人HTML均**不进入Git公仓**；仅派生数值/位图ID/ SHA链可公开复核。 Stage A依旧7PARTIAL+2OPEN，Stage B/wiki GATED，R79暂停，overall_percent=null。最高NEXT换另一类真源二维游戏内容；原生任务执行与同服资格保持OPEN。
