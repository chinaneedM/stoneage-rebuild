# INTEGRATION91｜长毛象客运六条原路线 × 台湾 1.0 真二维图形候选（2026-11-13）

## 目标与未重复的内容

按连续性协议重新读取远端 main `6a6a4ffc196afffd37ee25fa45361d6dc6f86bb1`、tree `ed3cd0869b2da88536fb48972cf85714a0803685`、最新提交、Actions **26/26 completed/success**、零开放 PR、七启动文件、完整原 `CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c` **2,709,173B，原样保留**，并复核 INTEGRATION90 的永久验收。

此次不重做波鲁龙王殿、恐龙牧场，也不重复 O86 已完成的单独交通脚本数字总结。**新交付是把 O86 已存后期社区原六车六路线，与另一来源的台湾零售 1.0 真正完整 SPR 二维帧来源联系为一个可手动核查的私有原图/路线观察界面，并把跨来源证据与反例固定到公共源码索引。**

## 后期社区 mixed25 六条真正原车辆 CREATE 与 35 源件

私有 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` 原包 **995,176B** SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f` 重新完整读取；原 **2,205/2,205** ZIP 成员 CRC 合格；O86 先前保管原 **35份共14,116B** 原巴士/指示牌/人员文本在同私有 ZIP 中再逐源读取全 SHA / CRC，非首次发现新路线。

原 `npc/chatroom/bus.create` **1,228B** SHA256 `18c31c8ae40b9c5250bddbb0455ab524c52c1491d505574ec2e288286f5c97a6` 内六个原 CREATE，逐原 byte start/end/exact SHA 与既有 CHAR01 公共索引一致，都是 `graphicname=100355`、模板 token `bus`，其中原 floor100 三条、floor200 三条；原模板静态函数 `Bus`、type 100401。不宣称六种生物，也不认定服端产生了六辆可乘车型。

六条同源原 `routeto1` 共 **300 个按原序 (x,y) 路径坐标**，六份原 route 字节 SHA 均在公共 JSON 保存，原 `needstone` 依原 CREATE 顺序 **50、25、30、50、20、40**，`waittime` 全为180；该数字是原脚本文字不是实际结算或计时原生执行。O86 先前确认的六站及26条告示/人员原文件与这六车在同一原保存包相连，但不把地面单元本身当已实走地图。

**原始反例绝不修补：** bus.arg 的第二禁带物品号字面 **403**，其余五份 **2403**；bus.create 与 bus2.arg 整文件 **CP950 不能完整往返**，因此不能对坏字节强译原名；一站原向导地名和附近路牌异文保留；floor3000另两静态牌/向导没有同创建清单对应车辆，不能造第七站。上述问题的父 source 仍归 O86，非本次新发现的服端BUG。

## 台湾 1.0 真正原二维 SPR：独立来源，不是同服身份证明

原 `StoneAge-PET11-private-TW1-two-capture-linked-SPR-groups-496-original-bitmaps.zip` 完整私包 **4,618,141B** SHA256 `d6f7c1e832833bf7bc00c5c870ba76debddbd447c52ca546cb4fcc72a45dbd5f` 重新实读，并核 ZIP 3/3 CRC、原私有清单、HTML 原嵌入真正 PNG byte SHA。该源所保存经认证台湾 Waei/JSS 零售 1.0 资源图形 **100355** 在 TW1 原 SPRADRN 第325位置具有独立源段 **7,072B** SHA `409081b2ead88925b44eeccca02005ff3de59906b8736ae6d2cdc3bcdcf070a3`：源 **56条方向/动作动画**、原 8 方向 × 动作码0/1/2/3/4/9/10、共 **640 个按序帧位置、248 不同 RD 图块**。私有 PET11 上轮确实已经将此组 **248/248 原 RD** 严格解码成功，本轮不再解原 RD：**新原块解码0**。本轮实际重读并逐原 JPEG? **无 JPEG**，而是 248 张现存候选 PNG 彩色及另248张索引灰度 PNG 的完整嵌入字节，**248/248 彩色、248/248 灰度 SHA** 均吻合 PET11 私人源清单；公共源中保存原 248 ADRN/RD/index SHA 的拼接总哈希供独立重放，不公开原 PNG。本源另一图号100329的坏 RD 不属于100355，不借它降低或提高该组结论。

重要身份边界：后期混合2.5另有将100355数字连到一条模板候选 `PETFLG=0` 以及编译捕捉输入 `key53=8` 的记录，与六条巴士 NPC 原 `graphicname` 有数值交集。这**既不认证台湾1.0官方载客长毛象实体、也不等于 PETFLG0 是已认证宠物**；即便两来源 SPRADRN 的原12B索引恰好相同，也不证明整个服务器部署一致。原商业客户端的色盘选择、角度/FPS/音效以及是否实际乘坐均 OPEN。

## 私有观察成功与永久保管

私有离线 ZIP **2,530,925B**／SHA256 `a0bf3d9875a9aee50e35a21c7154c45f2c39fd0d9bf5eed8d4ce3af1b692d878`，37成员含35原商用小文本、独立自包含 HTML、逐源摘要私有完整清单。已上传到用户个人 Library `/石器时代/StoneAge-INTEGRATION91-Mammoth-Bus-six-routes-TW1-original-2D-private.zip`，并从 Library 新位置重新独立取回原 ZIP，完整SHA一致、**37/37 CRC**通过。

现代私有 HTML **3,539,016B** SHA256 `cc2a1d84441f4956ef31dbe8b3b85b1dfcb483b0bb5e4cd6747736db3979ca7c`，实际系统 Chromium 144.0.7559.96：6/6原数字路线选择、56动作方向组合两调色模式图片加载（112加载）、56次下一帧+1次上一帧、0 JS错误／0外部HTTP请求。因本环境策略，不声称 file:// 已成功直接打开；采用 `page.set_content` 装载相同原私有 HTML 字节。路线 SVG 是**现代原数值折线，并非商服原地图、运行移动或同一原客户端真实截图**。

公开 Git 仅来源编号/计数、每个原 CREATE span SHA、原路线字符串哈希、原来源 35 文件 SHA、原 SPR 来源摘要及浏览器验收资格，不上传原文件、原整300点表、原 PNG、音乐或 EXE。

仍为 Stage A 7 PARTIAL+2 OPEN，B/wiki GATED，R79 PAUSED_NON_BLOCKING，整体完成率null。NEXT 轮换另一类有真正原图与真实配置可进展的内容；Bus原生计费/载客/路线运行须新的同构建handler或真执行实物才重开。
