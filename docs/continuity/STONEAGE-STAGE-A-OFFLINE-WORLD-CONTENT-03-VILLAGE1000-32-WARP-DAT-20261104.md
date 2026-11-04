# Stage A — 村庄1000原始全32传送CREATE与DAT格值证据闭环（2026-11-04）

远端新轮起点：main `d7efe4567fc1bd1f3fdf4b1455c98d652f7a7928` / tree `cb20146abb3edde0a6f0053a8e94092d690aca8c`。原巨大 `docs/CURRENT-STATE.md` 2,709,173B Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 不改变；上一WORLD02 NPC坐标图谱已通过CI。

## 本轮重新读取的真实原文件（私人，不入公开Git）

完整验证了既有CHAR01原NPC ZIP（995176B、SHA `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`）2205成员CRC；原O31 ZIP（2295731B、SHA `f14ee7c362e74bb82fabb867bee08729b41f9744208642fd689bf2730d10548f`）8成员CRC。原1000.DAT整件153608B、SHA `94b19cb59d72b7b48da70d2741ba68516caad970297fd48ed11ef720fa3ea97e`；原warp_y.create 24588B、SHA `859ff2ed23baadb20382508874cd3a63e603b84c7205c6f5d8998229f4f4c8b1`。原CREATE块的完整SHA按包括末尾LF的半开区间同先前CHAR01/WORLD02逐行匹配。原始数据版本属于 **后期社区mixed25保存包**，不等于JSS1999、台湾1.0、大陆1.82正式原服。

从18个floor1000源CREATE文件的78条有效配置中筛出`npcgen_warp` **32条**，恰为 `genout/warp_y.create`22、`genout/100warp.create`9、`poru/dragon_warp.create`1。逐一读取原地图160×160小端三平面对应格值，32格object均0。

**全图事件层25600格的原U16值计数**：49152=24148、0=1280、16384=140、49155=30、49158=1、49159=1；事件层SHA `a950dcd6a7e9d94edb4b241d1b491cc153bbba5ca542dc4c26a538801a117d1d`。**全DAT中事件代码49155/49158/49159的32个坐标集合，与同保存载体中这32条CREATE的中心坐标集合完全相等**。不是据单个已知格推全图，亦不是所有其他地图/官方版的通用事件码证明。

两特殊原字面1000(63,117)→1011(10,15)附`M`/DAT事件49158、1000(63,118)→1014(10,16)附`A`/DAT事件49159；保留原值，不猜M/A实际触发机制。旧O31五条门和O41两特殊点已用当时原报告核对，不冒充本轮新发现这些旧点。本轮新增的是**全32原源点的闭合集合**和13目标地图覆盖。

32个原配置指向13个独立目标楼层编号（目标100：9；1001、1002：各3；1003、1004、1005、1006、1009、1012、1020：各2；1011、1013、1014：各1）。目标13份原DAT文件完整尺寸与SHA已在更早MAP01源清单（12份）和独立RAR恢复报告（100.DAT）中查证；本轮核实所有32条坐标都在这些原地图尺寸内。**目标DAT正文没有全部在本轮重新私人读盘，不宣称再次从原RAR完整提取它们，更不宣称历史部署或游戏实际到达。**

## 私人可见内容与验收

私人 `StoneAge-World03-private-village1000-original-warp-atlas.zip` 2,033,376B、SHA `a4e14423bf1b729ae40a3921d31885f0416fd322581f239ce444ec3f14fc9ee8`。四成员CRC通过，包含纯本地32条配置/13目标选择、DAT原U16数值和来源哈希索引以及原样未修改的既有O34局部原画观察HTML。新画的彩色坐标点是现代资料示意，绝非原游戏真实画面/碰撞/行走/触发。Chromium Playwright按同字节HTML的`page.set_content`检验32全量、100目标9条、1011/1014各1条、M/A与原事件码及按钮；JS错误0、网络HTTP请求0。未认证直接file URL打开、原客户端世界进入或原服务器运行。

公开[来源与数值原格收据](../../research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-03-VILLAGE1000-32-WARP-DAT-SOURCE-R1.json)只含出处、原始CREATE块和文件SHA、坐标、原DAT格数值、目标文件已有资格及不确定边界，不含原DAT/CREATE正文、商用美术、私人HTML。Actions只验证已有公开派生报告相互守恒，不会读取私人商业原盘。

## 后续最优包

**NEXT STAGE-A-OFFLINE-WORLD-CONTENT-04**：本村庄1000和道场3021静态资料批次到此止点；改从已合法取得的原实物里恢复另一类更有实际内容价值的宠物、NPC、任务、地图或原动作材料，不再重做静态索引/网络登录/服务器框架。Stage A仍7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，整体百分比null。未来单机新石器引擎、UX优化与新内容仍未开始。
