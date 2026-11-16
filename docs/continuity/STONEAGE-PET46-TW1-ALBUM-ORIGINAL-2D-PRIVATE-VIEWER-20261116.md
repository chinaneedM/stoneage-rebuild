# PET46 — 台湾1.0客户端原宠名与私人原2D动作的同源实物交付

日期：2026-11-16。连续性事实基线 main 01e2fcc774c62c6a8439bd3cf45e488f11383823。仅PET模块；2000官方历史审查OPEN。

## 这次的真实交付

已从私人Library实际取回此前PET07原SPR观察HTML（15,123,277 bytes；SHA256 58e8ee4ff5165ed2f61663d67ae1cd0a8183622fa3375c480232784bfce9dc76），不是把已有索引统计伪装成像素。原私有文件含130个台湾1.0原SPR图号、451条已保留动作/方向序列、3817个帧出现位置、2540项已保管PNG data URI。PET07旧工作此前实际解码2176原RD块（其余2块异常），2540 PNG是累积画面缓存数量，不等于本轮新解码。

将PET39从同一认证台湾1.0零售客户端真正读取的124条相册宠名逐一与PET07台湾1.0原SPR核对：124组不仅图号一致，源物理组index及完整原SPR段SHA也124/124一致。此次没有新发现宠物名字，增加的是实际可查、可浏览的原名字→原图和动作关联，仍为CLIENT_PET_IDENTITY_CANDIDATE，不是同版官服实际投放证明。

PET07其余六原SPR图号：100015、100018、100401、100432、100451、100454。PET39内置相册窗口原图号为100250–100430；其中100401是原表显式占位（不得当具名宠物），其余五号不在原相册窗口。不能将六组全都称为独立官方宠物。

生成私人单文件离线图鉴 StoneAge-PET46-TW1-original-pet-album-private.html，15,136,729 bytes，SHA256 321d366313dc30d71fe1f3aa0bb7f9feb63e5a6c1e0aa5411b4975adf9f3afe9。支持原名/图号筛选、124具名/6未具名切换、动作/方向选择、逐帧及现代180ms观察播放。源HTML内2540 PNG数据和451条动作序列列表字节对应信息未改。已在Chromium直接载入HTML内容，130卡显示、默认124具名、检索烏力出现5卡、6号未具名筛选准确、真实像素naturalWidth正常、0 JS页面错误。本执行环境file://被管理员策略阻挡；测试通过浏览器set_content载入，不宣称file://在本环境通过。

私人HTML含原商业美术衍生图像，仅向用户的对话沙箱交付，绝对不提交公共Git。公有机读来源核对清单：research/recovered/STONEAGE-PET46-TW1-ALBUM-NAME-2D-CROSSWALK-R1.json。逐130组保留PET07源原SPR图号/index/SHA及三动作有限记录，PET39原名、相册原行SHA/offset、占位状态、私有HTML交付sha，便于日后再审。

## 边界与NEXT

新解码原图数0；新识别其他客户端原宠名0；新实证正式官服投放0；全球历史物种总数UNKNOWN；同版原服务端野生/任务奖励/商业发放与属性技能仍需独立证据。NEXT PET47 优先2000年份官方实际获取/发放正本、早期日韩客户端和更晚同构建名字↔图形原始表；绝不再因仅有SPR索引无限累加未确认物种。

历史 docs/CURRENT-STATE.md 原Git blob c89e0e33537990aa2132b47c40fef49a985a935c 及2,709,173字节不动。Stage A 7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，整体完成率未知。人物/NPC未解锁。
