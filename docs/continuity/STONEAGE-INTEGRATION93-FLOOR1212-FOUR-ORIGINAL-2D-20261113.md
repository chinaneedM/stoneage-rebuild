# INTEGRATION93｜floor1212四原 NPC 配置与台湾1.0真原二维候选（2026-11-13）

## 新材料与启动

从重新核验的正式远端main `991d2ba643fd5155165f3ebc99ab3cec183b07c9`、tree `b290cc7f6ae2e4d9c7ac2eac0791a0a8ff36b20d`、零开放PR、协议与完整原 `CURRENT-STATE.md` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` (2,709,173B) 启动。此前INTEGRATION92已PR #368合并；此轮改为不同楼层内容，不重做五兄弟或公车。旧主线最后收据的HEAD本身Actions尚未另获有效新run证明，不偷算通过。

后期社区mixed25原 `genout/nevent_03.create` 9,673B、SHA256 `a949036b3b3080591378a67e08a7c82330158020c3be48d6188a84657c6c4c59`，来自先前已验CHAR01原CREATE索引；本轮未再读此商业CREATE的原始字节，**仅依已验源字节span SHA及数据作新的来源关系**。floor1212原ordinal14–17四个`npcgen_man`，源点(12,19)、(14,19)、(16,20)、(18,19)，图号100326/100265/100259/100294。floor1212真实DAT本轮未读取，不制假底图。

另一真实原始来源台湾 Waei/JSS v1.0 零售客户端，原PET07私人图库15,123,277B SHA256 `58e8ee4ff5165ed2f61663d67ae1cd0a8183622fa3375c480232784bfce9dc76` 本轮重新实际取回并整SHA核验。四原SPR每组有56动画，仅方向0源动作0/2/1所选3段：**共12源序列、96源帧位置、70张不同原RD候选PNG**，每张原PNG完整SHA256与PET07保存的原RD来源收据70/70一致，RGBA图尺寸亦核实；本轮新RD解码=0，不宣称新发现70张图片。原duration raw word不可擅定毫秒或帧率。

## 私人验收与Git公开边界

私人文件 `StoneAge-INTEGRATION93-floor1212-four-original-TW1-2D-source-only-private.zip` 474,219B、SHA256 `ffcee80fc069ec364af35422bdb54b1c951091c7129637f373f356e81686ca50`，内含70原PNG、四组真图的现代纯离线动作查看HTML、说明共72个成员，独立ZIP CRC及全成员读回均通过。使用Chromium的`page.set_content`实际载入**相同HTML内容**、成功显示四真图，对四卡各点击下一帧／切换动作／上一帧共12操作，JS错误0、外网请求0。`file://`和本地HTTP导航受测试宿主政策拦截，不能冒称成功导航；这个页面并不是原版客户端。私人ZIP未传公有Git，也未上传Library；只在本会话作为私人交付。

公开[元数据JSON](../../research/recovered/STONEAGE-INTEGRATION93-FLOOR1212-ORIGINAL-2D-R1.json)保存四原CREATE source byte-range SHA、四原SPR整组及12序列摘要、70真实原RD/PNG SHA与证据等级。公开[7项测试](../../tests/test_stoneage_integration93_floor1212_2d.py)仅重放已公示来源摘要，不能代替私人原图重新解码或原版玩法测试。

**不能晋级的结论**：两独立版本同号图形≠台湾1.0原服NPC身份/坐标/剧情；无同服商服部署证据、原native人物站位与通行/碰撞证据、原调色板/帧率或NPC脚本执行。原始商用图/字节文本均不进公有仓库。Stage A **7PARTIAL+2OPEN**，Stage B/wiki **GATED**，R79暂停，整体完成百分比未知。

**NEXT**另选不同具真正原二维图、能补玩家可见原内容的历史家族；不扩新引擎、账号/M MMO或重复此四图；候选及合并后Actions真验收后另记，绝不预支。
