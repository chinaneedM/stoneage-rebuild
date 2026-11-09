# INTEGRATION22｜三村六間原商店，十份 CREATE、原裝備類型與真 DAT／圖像候選

## 續接、來源及範圍

依 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 從遠端 `main` HEAD `b817f7bca97e921c76714882890e4e091afc156d`、tree `05135c8f13c4439a836ce764126fcf7ec4684efb` 重新啟動；同 HEAD 12/12 Actions 全部成功，當時沒有未合併 PR。從 Git blob 直接重讀完整 `docs/CURRENT-STATE.md` 2,709,173 B、blob `c89e0e33537990aa2132b47c40fef49a985a935c`，本輪**保持歷史全文不變**，只作日期追加。

從已保存的 community mixed25 原 RAR **361,255,180 B、SHA-256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`** 實取 10 個 CP950 商店參數檔及 6 份 LS2MAP 原字節，原成員 CRC、檔案 SHA/欄位檢核成功；另從已驗原 `shop_m.create` 與 `mapwarp.txt` 取完整來源，經分塊／原行 SHA 限定個別 CREATE 和方向。私人 MAP09 46,844,444 B、955 DAT 內包、ITEM01 5,868,386 B 與 INTEGRATION17 原件按原 SHA/全成員 CRC 認證，實讀 6 張原三平面 DAT 與 2 個後續村外 DAT，並重用台灣 1.0 零售候選 RD 畫素。這些來源**分屬不同版本／載體**：後期社群服配置不冒充早期官方原服，台灣 1.0 來源畫素不等於同構建 NPC 原生選圖。

本批優先結案實物俱在且尚未整合的 **ITEM／EQUIPMENT／SHOP → NPC／MAP** 玩家可觀察原內容；舊 INTEGRATION18 的 16122／16127 NPC 真像素封裝雖有前次取證，當前 RAR 解壓器不支持其巨型 REAL/ADRN 區段、未取得合格本輪原 RD，精確缺口保留，不擴 RAR 解壓器工程、不造人物。

## 六個室內地圖、十個原 NPC／服務配置

| 原房間 floor | 本次 `shop_m.create` 原 CREATE | 原用途欄 | 此次原 LS2MAP 第二層 vs 客戶端 DAT 不同格 | 候選原圖塊放置 |
| --- | ---: | --- | ---: | ---: |
| 柯奧 1101 | 2 | OFFENCE、DEFENCE | 31 | 158 |
| 柯奧 1102 | 2 | ACCESSORY、另列素材屋 | 31 | 156 |
| 柯爾克 1201 | 2 | OFFENCE、DEFENCE | 88 | 162 |
| 柯爾克 1202 | 1 | ACCESSORY | 88 | 160 |
| 瑪麗娜絲 2001 | 2 | OFFENCE、DEFENCE | 32 | 132 |
| 瑪麗娜絲 2002 | 1 | ACCESSORY | 60 | 156 |

九個常規原參數的 `LimitItemType` 分成各 3 個 `OFFENCE`、`DEFENCE`、`ACCESSORY`；三村 `sell_rate` 的原字串各為 `0.19`、`0.16`、`0.20`。原欄是分類依據，不等於遊戲內原生購買成功或折價計算已實測。

**新核的第十筆**：`shop_m.create` #106 在 1102 `(14,14)` 的「素材屋」另連 `genout/ss_1102_14_14`／原整 SHA `243f728b0ca876cb0bd964bd2039923701fe6be89960685db3f9dcfabe6a7b3f`。它的 `LimitItemType` **空白**，`ItemList` 與 `LimitItemNo` 均寫兩個來源範圍 token `11960-11967,11970-11977`，`buy_rate=1.0`、`sell_rate=0.5`。保留**兩個原字面範圍**；按閉區間只得到 16 個**候選** ID，不能改稱原件直接明列 16 行，更不能認證原服實際上架。ITEM01 的 224 個參數底稿另有 `ss_1102_18_16`，本批**只核 `shop_m.create` 在這六房可指向的十筆**，不宣稱所有副本／商店人口已窮盡。

九份常規原 `ItemList` 累計 **108 個明列項次**；加上素材屋兩個 token 的 16 個假設展開，共 **124 個可比對項次、120 個不同物品 ID**。選定 124 項在 mixed25 同保存兩套 itemset 原表都有整行 SHA 一致的各自行，**不等於官方跨服主表相同**。89 個不同 `imagenumber` 可對已保留台灣1.0 RD 的真候選 PNG/RGBA SHA，不把同號認作同服實際商店圖標選擇。6 張 30×30 原 DAT 的 125 個不同原圖塊來源候選連成完整場景；每一張 1889×1425 整圖按 DAT 圖號、ADRN 位移及原真圖以 Pillow / NumPy **獨立逐 RGBA 字節核同** MAP09 已有哈希。私有 HTML 顯示六間場景、現代 NPC 座標標記、原物品與圖候選，素材屋的 16 個只標記「範圍假設」，**不是原遊戲或瀏覽器原生操作驗收**。

來源 LS2MAP 首層與 DAT 首層均一致；第二層差值只記錄伺服器 2 對客戶端 0，不將 2 稱為已證的碰撞、遮擋或可通行。

## 23 條有向出口與精確缺件

完整原 `mapwarp.txt`（SHA-256 `b7b50f42efa8e5a3f740d49a8d0c01cbf994d1bb66151b16ff5b5e7c14e7595c`）在這六房指向的端點共有 **23 條有向原行**，其中 22 條具有**明列相反方向**，而 `1101 (16,21) → 1100 (52,72)` 的逆向**未列**。不能以相鄰同一出口或資料圖構造第 24 條。六張室內 DAT 每個端點均有原三格 u16；1200、2000 室外完整原 DAT 也從 955 來源包讀取並附 SHA。

**1100 例外：** 955 原 DAT 內包沒有可讀 `1100.dat`，本輪凡涉及 1100 室外端點的三格 u16 明確置為 `null`，只保留有來源的 warp 起止座標及房內三格。此處的 `null` 是**本次選定保存來源缺件**，不是宣稱原遊戲沒有地圖或無法走通，更不能以假格值完成玩家路線。

## 交付、驗收及 NEXT

完整衍生原始來源索引：[INTEGRATION22 公開來源目錄](../../research/recovered/STONEAGE-INTEGRATION22-THREE-VILLAGE-TEN-SHOPS-SOURCE-R1.json)。公開 [test_stoneage_integration_module_22.py](../../tests/test_stoneage_integration_module_22.py) 以 ITEM01、MAP09 整 Git blob 鎖定原參數 SHA／六張 DAT 與全 RGBA 候選指紋，並測假範圍上架、虛構 1100 室外格、亂改用途／傳送方向或跨版原生宣稱會被拒絕。GitHub CI 只重放**公開派生 SHA／數值與反例**，不說成重新解原商業圖或原服運行。原商品名稱、圖、腳本正文、DAT、LS2MAP 與現代觀察頁只入私人 Library，不進 Git。

私人實物：`/石器时代/StoneAge-INTEGRATION22-three-villages-ten-original-shops-private.zip`，**6,134,890 B，SHA-256 `12239bcab57215586fe4ca755a9503900daaa91be7abdecb6e21621db9d6b92d`，131 成員 CRC 全過**。已上傳個人 Library 並獨立下載，整包 SHA 及 131 CRC 再核完全相同。私人 6 圖由 Pillow/NumPy 與已存 MAP09 原 RGBA SHA 核對，**未啟動歷史原客戶端、沒有驗交易、NPC 動作、碰撞或行走，也沒有在本輪執行 HTML 瀏覽器測試**。

**NEXT：** 這六房及原 10 CREATE 的資料已達 SOURCE_BOUNDED_PARTIAL，停止重畫；下一包按模組順序挑能提供真來源且尚未合流的物品／裝備、NPC 或永久任務內容。1100 室外只在合格 DAT 原字節復得時增加原格，16122／16127 只在可重驗 RD/PNG 真字節時補人物，不擴原商服、帳號或新引擎。Stage A 保留 **7 PARTIAL + 2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、總進度百分比 `null`。
