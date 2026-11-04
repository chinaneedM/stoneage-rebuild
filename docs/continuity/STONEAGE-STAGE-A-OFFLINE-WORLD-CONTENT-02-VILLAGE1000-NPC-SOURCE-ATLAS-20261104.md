# Stage A | 1000村庄原NPC源配置 × 已有离线村庄原图观察窗口（2026-11-04）

**状态：** STAGE-A-OFFLINE-WORLD-CONTENT-02 来源限定静态整合，未进入原版游戏；仅历史复原，不开展新游戏引擎、体验优化、网游账号或登录网络。

本轮以远端 main `6f6e4041e61725906ca00c5c4cbd7eff1282a64e` / tree `79bc566b9acca1187a8159129802c6150d380d5c`、`docs/CURRENT-STATE.md` 完整原 blob `c89e0e33537990aa2132b47c40fef49a985a935c` 为起点，依据前批离线道场的 CURRENT02 NEXT 开展。巨大 CURRENT 历史前缀未改，以本文件追加检查点。

## 原实物工作与新增结果

1. 从已在私人 Library 留存的混合2.5社区服务器NPC完整源 ZIP，实际重新读取全部2,205个原成员、通过全 ZIP CRC（ZIP 995,176B, SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`），从18份原 CREATE 文件读取并筛出 **1000楼层78条有效创建块**。被注释的配置不当有效。每条原块带单独SHA，全部78条与前次已入Git的 `STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json` 行身份、文件SHA和配置地面号交叉核对。
2. 记录来源定义的原 `graphicname`、源创建定位字段、NPC模板函数token、原名称摘要、同包 `file:` 原引用及SHA。78条里确有32条 `npcgen_warp`、16条 `npcgen_man`；**不是**32次真实传送或16个已经显示的NPC。39个 `file:` 路径在该私人原包内均找到真实源成员，只有私人观察器查源文案，不将完整商业对白放入公开Git。
3. 现存O34原场景观察器 ZIP SHA `0c9c38817f6b4c7838a7be0ec122f7dbe274b52a0153b6c7a23c27365fd1dbe2`，其原 HTML SHA `9e34d958d8897e2f740de83eafda517cdfbd4dbdd1a0bcc7fd917f45e807cdfb`。原村庄尺寸160×160，已有源限定原图片观察窗口 **x48–72/y92–132**，该窗口可覆盖原 CREATE 的**18个坐标锚点**，其余60个在窗口之外，不宣称该处已实绘。原图源来源历史前缀与后期地图不能自动推出官方同服。
4. 在旧CHAR01派生索引中两份CREATE的 `borncenter` 位置为空；从原CREATE全文确认 `my/tiancai/transfer.create`的(94,102)及`sa60/newbie/newbie.create`的(48,62)，**原索引不改**，在本批源限定索引单列实读补正。其原配置块SHA仍与既有索引一致。
5. 私人交付 `StoneAge-1000-village-NPC-source-atlas-private.zip`，2,683,249B、SHA256 `5c4fbd5103b1f7ad309345a1f5c86fdb86d06c849fec371651dfbcc5bbf53433`。包内为新的本地原配置索引HTML，附同一字节、**原样不变**的O34旧观察页。新页显示整张160×160**人工坐标标记**、18位置窗口筛选、原函数类别和同包原文本，并引用早已保管的O34场景图；没有新造原始画面。私人素材不上传公开Git。
6. Headless Chromium实际把**同一HTML字节**通过 Playwright `page.set_content` 载入，查得78默认项/18窗口项/32 warp项；按(63,103)检索得到精确 `genout/msg_1000_63_103` 原引用、可点击原坐标，O34旧图片宽1550，**0 JS错误 / 0 外部HTTP请求**。在执行环境尝试直接打开 `file://` 被管理员阻断，**不宣称**已完成原HTML本地file URL导航；不影响同字节HTML控件运行证据。

公开数值索引：[`STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-02-VILLAGE1000-NPC-SOURCE-BRIDGE-R1.json`](../../research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-02-VILLAGE1000-NPC-SOURCE-BRIDGE-R1.json)。独立源行/位置/缺失反例见新增测试，CI需读取实际结果后才能标通过。

## 仍然OPEN与后续优先级

该来源是 **LATER_PRESERVED_COMMUNITY_MIXED25**，非认证的JSS1999、台湾1.0或大陆1.82原服；`graphicname` 不等于已验证原像素身份。原版NPC真正出现、对白/任务触发、真实地图走路碰撞、商店交易、战斗/传送、原声时序及进入游戏世界仍OPEN。现代离线页不是原客户端，也不是未来新游戏。

**NEXT STAGE-A-OFFLINE-WORLD-CONTENT-03：** 按模块第一原则，在已有合法原字节载体里继续找能对应原图、原NPC/宠物/任务具体功能的另一批内容关系，优先可实际观察的来源结果，找不到就记录止点并切换模块。不重复扩展1000静态图谱，不研究原网游登录网络或为核验而做新引擎。Stage A维持 **7 PARTIAL + 2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，总体完成率未知。
