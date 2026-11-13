# INTEGRATION91 — 正式原來源／私人2D圖／GitHub Actions 验收（2026-11-13）

## 原素材與跨來源連接的真实范围

按遠端 `main=6a6a4ffc196afffd37ee25fa45361d6dc6f86bb1`、tree `ed3cd0869b2da88536fb48972cf85714a0803685` 启动，26/26同SHA Actions successful，0开放PR，完整原 `CURRENT-STATE.md` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` **2,709,173B 原样保留**。

私人原 mixed25 NPC ZIP 995176B／SHA `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f` 真实重读全2205CRC；以前 O86 已恢复的35个 Bus 路线／向导／站牌小源（共14116B）全部重读 SHA；**6個原 CREATE 精确 byte-window SHA 与 CHAR01 公共记录 6/6 一致**，全部 graphic 100355、floor100/200各3，六原路线 **300个原坐标出现**。原403/2403第二禁带数值差异、CP950原坏字节、floor3000缺对应Bus及不同向导地名全部保留，非Bug修复或native Bus运行。

另一来源台湾 Waei/JSS 正式零售 1.0 的源100355 SPR 原段SHA `409081b2ead88925b44eeccca02005ff3de59906b8736ae6d2cdc3bcdcf070a3`；全部 **56动画、640帧位置、248不同原RD图号**来源于已验 PET11，之前全部248/248原RD严格解码过。此次重新读取私人PET11原ZIP和实际 PNG：**248张原候选彩色+248张原索引灰度都逐PNG SHA复核一致**；本轮未解新RD。属于跨来源同数字候选，**不能据此认定TW1原本有這六辆巴士、官方同服运行、原配色/动画速度/正确乘客/扣Stone或路线移动**。

私人 observer ZIP **2,530,925B SHA256 `a0bf3d9875a9aee50e35a21c7154c45f2c39fd0d9bf5eed8d4ce3af1b692d878`**，37成员原巴士来源小文与真原PNG离线查阅、私人清单，已保存在个人 Library `/石器时代/StoneAge-INTEGRATION91-Mammoth-Bus-six-routes-TW1-original-2D-private.zip`，再从 Library 独立取回全 SHA 和37/37CRC合格。Chromium144 实测6条原坐标路线切换，56方向×动作两候选色盘共112图片载入，56次下一帧＋1次上一帧，0JS错误、0外网。路线SVG为现代数值折线，不是游戏原地图/实际NPC移动；使用 page.set_content，并未证明原本 file:// 成功。原商用图片和原完整台词没有公开发布。

[来源派生索引](../../research/recovered/STONEAGE-INTEGRATION91-MAMMOTH-BUS-ORIGINAL-2D-R1.json)及[本轮内容报告](STONEAGE-INTEGRATION91-MAMMOTH-BUS-2D-20261113.md)。

## 实际失败、修正及最后验收；历史不能改写

[PR #367](https://github.com/chinaneedM/stoneage-rebuild/pull/367) 已 squash merged。**首次候选 `661e294aaa33a489b9e1a24fe4085f5eac20d65b` 共46条 Actions中44 success、2 failure**：专用 push `43415151265`／job `131851054703` 与专用 PR `43415156621` 同时为 failure；真实原因为**测试字段名错误 `source_original_SPR_index_12byte_SHA256`，公开报告正确字段是 `original_source_SPR_index_12byte_SHA256`**。没有修改商业原数据或补造缺图，只增加一个修复commit `98568cc33f36d0302217325beb0162be7daa657b`，原两个失败 run 永远保留，不倒称通过。

修正末候选 `98568cc33f36d0302217325beb0162be7daa657b`／tree `a4d99484ace607b7e29d1cc3a28d569b61f435c8` 共 **20/20 真正 completed/success**。专用 push `43415329573` job `131851652798`、PR `43415334355` job `131851671211` 各有实际日誌 `Ran 12 tests / OK`。正式合併的**内容主线 `0a7b03e4adba4faf6e0a74a5de276c8af770e475`／同tree `a4d99484ace607b7e29d1cc3a28d569b61f435c8`**，本SHA **27/27 Actions completed/success**；专用 main push `43415492380` job `131852205123` 真实日誌 `Ran 12 tests / OK`。逐run/head/event/status、原私包SHA、源Git blob请参阅[机器验收收据](../../research/recovered/STONEAGE-INTEGRATION91-PUBLICATION-ACCEPTANCE-R1.json)。

**验收收据这次的新提交自身 Actions 不能预支**：后续按新 HEAD 真核。Stage A 7PARTIAL+2OPEN，B/wiki GATED，R79暂停，overall_percent=null。下一最高优先另一个真正原二维内容家族，Bus静态已止点，不扩原MMO/新引擎。
