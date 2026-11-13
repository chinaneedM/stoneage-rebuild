# INTEGRATION86｜漆黑洞窟五考古家、兩守護獸、精靈王來源／19幅原二維候選（2026-11-13）

## 完整遠端啟動與去重

從 GitHub `chinaneedM/stoneage-rebuild` 真實遠端 `main=58e182f27a3404c99c32d9c3aaa18e1ecf386a16`、tree `8709843f7297781f01348de0a2a14b9182b708e1` 啟動，最新 HEAD 的 **26/26** Actions 全部成功、0 開放 PR。重新讀 README、完整連續性協議、DESIGN、HISTORICAL-TIMELINE、SOURCE-REGISTRY、roadmap、模組順序與原 `docs/CURRENT-STATE.md` 的 **2,709,173 位元組、blob `c89e0e33537990aa2132b47c40fef49a985a935c`**（非檔案介面的空字串），保持舊歷史不改。前 `INTEGRATION85` 已做四方守護者／31609 勾玉／雙石像，**本包不重複 31609 四勾玉，也不把兩個洞窟守護獸混為該 12 個 NPCEnemy**。漆黑洞窟在舊資料是原始來源索引中的一族；此批第一次限定恢復其五條原考古事件／兩戰鬥守護獸／精靈王指向與確切圖像及原道具負證，而非只增加舊有 TYPE 總數。

真實私有源本輪逐整檔 SHA、ZIP 全成員 CRC **重核**：`StoneAge-CHAR01-mixed25-all-npc-original-private.zip` 995,176B／2,205 CRC／SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`；`StoneAge-ITEM01-private-two-itemsets-832-original-RD-icon-observer.zip` 5,868,386B／838 CRC／SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`；另一**台灣1.0認證零售原來源**私人 PET07 HTML 真原像全集 SHA256 `58e8ee4ff5165ed2f61663d67ae1cd0a8183622fa3375c480232784bfce9dc76` 實讀。原 community mixed25 與台灣1.0不證同一次官方部署；沒有 JSS1999、初代大陆1.82或原版客戶端真實世界運行認證。

## 原NPC：八個洞窟CREATE＋兩守護獸，保持職能分層

- `npc/giiru/event/sikkoku/sikkoku.create` **1,594B**／原 SHA `dbd64c77c643...`：五個 `changeevent` 考古家分別是 `32002 (4,23) graphic100451`、`32006 (46,46) graphic100195`、`32009 (49,20) graphic100190`、`32014 (14,48) graphic100446`、`32016 (31,43) graphic100436`；逐一直接引用 `giiru/event/sikkoku01` … `05`。另 `32021 (31,28) graphic100444` 有一個 `npc_transmigration` 精靈王；`32014 (51,11)` 與 `32007 (27,54)` 各一 `npcgen_winhealer` 護士。合計八筆**原靜態配置**，不等於八個原服已看見的實體。
- **另一原檔** `npc/300/sb_sikkoku.create` **401B**，兩筆 `NPCEnemy` 形態：`32010 graphic100389` 漆黑的守護獸和 `32020 graphic100374` 帖拉所伊朵；原 `sb_sikkoku.template` 實有兩模板，兩個 `.arg` 亦實有原位元組。首者 `enemyno` 五字面值、其原 `warpfl:32011, warpx:56, warpy:36`；後者十字面值、`warpfl:32021,warpx:29,warpy:57`。`dieact:1`、`entype:2`、`onebattle:0` 都只是原配置。**不推定實際組隊、勝利傳送或地圖走通**。
- 每個原 CREATE 位元組區間與完整 SHA 均放[來源限定機器索引](../../research/recovered/STONEAGE-INTEGRATION86-SIKKOKU-SOURCE-2D-R1.json)，逐段原 CP950 往返；沒有把 `{}` 的腳本文本當成原伺服器已生成NPC。

## 五考古家原事件16段：真文字和「16樓」標頭不能當實際座標

五份直接 `file:` 的原 `sikkoku01–05` 共 **16個 EVENT 段**（前四份各2、第五份8）：記錄原 `EventNo`、`TYPE`、`EVENT` 字面條件、`GetItem`／`DelItem`／`EndSetFlg`、每原段位元組區間和 SHA，**原對白全文只在私人包**。前四考古家的字面發放道具依序 **2771／2772／2773／2774**，兩份混合社群物品表同 ID 的四原行都存在，名字分別是「地的寶珠」「水的寶珠」「火的寶珠」「風的寶珠」。對話的「古代高度文明、四大精靈、失落科技、守護獸／轉生」是**本保存載體原稿叙事**；不能直接移植為1999初版史實或官方初代一定存在的完整任務。

**精確負證：五份原事件檔的註釋標頭都寫「16樓講述傳說」，但五個 CREATE 實際是 32002/32006/32009/32014/32016 五個不同 floor**。來源不一致按原樣並列，不「修正」座標、也不把樓層 ID 轉換為已證實的玩法層數。

末份 `sikkoku05` 的 `EventNo:53 TYPE:ACCEPT` 有**確切不一致**：

| 同一原 EVENT 欄位 | 原字面 ID | 有界結論 |
|---|---|---|
| `EVENT` 要求四個 ITEM | 2701、2707、2735、2770 | 源字面檢查條件 |
| `DelItem` 欲刪四個 ITEM | 2701、2702、2703、2704 | 與要求集合**僅交集2701**，其餘三個不匹配 |
| `GetItem` 三候選 | 20570、20571、20572 | 原輸出 ID；**不是**已成功發獎 |

尤其 `2702` 在原物品表是蜂蜜、`2703` 為獵場入場券、`2704` 為麥克風，**不能擅將 DelItem 修成 2707／2735／2770，或把錯配視為獎勵一定成功／一定失敗**。原 parser 的條件優先序、同服部署及是否允許此分支執行均 OPEN。

## 真物品雙表與真正跨來源原像，另保留缺圖

本輪總共鎖定 **19個不同原物品 ID**（四歷史寶珠2771–2774、2701–2704、2707、2735、2770、20570–20572，以及精靈王 `777/ten.arg` 的五個出生地禮品1377–1381），在原 94 欄兩套 `itemset.txt`／`itemset0710.txt` 逐 ID 重新 CP950 拼接實際**35筆原整行 SHA**。不是19件新出土道具。

**三個 20570、20571、20572 在舊主表 A 均不存在行，但在主表 B 有原行**，其名稱為「星光服」「星光帽」「星光爪」；因此不稱它們完全缺失，也不能拿較後 B 的行無條件證 A 時期已可獲得。19 ID 對應 **19個不同 `ImageNumber` 數字**，已保管台灣1.0零售來源中 **16幅 RD 原圖候選**實讀／逐 PNG+RGBA SHA+尺寸核實，另外 **3個別名 20241／24314／24315 在該 TW1 索引無對應像素**，不能補畫。其中20241屬 20572 星光爪；24314/24315則是 `DelItem` 字面來源的獵場券／麥克風。另從保存的 TW1 PET07 原像全集真實取出三幅圖號 `100451`、`100389`、`100374` 的動作0方向0第一原 SPR／RD 候選幀，並與舊[PET07原解析派生證據](../../research/recovered/STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json)中同原bitmap PNG SHA 精確一致（bitmap 92185／105739／122515）。**16原物品+3原SPR=19實圖**，全部之前已有合格解碼；**本輪新增原 RD 解碼0、新美術0**。未取得其餘五位考古家、精靈王和護士之本批真原像匹配，仍 INDEX_ONLY，不能用其他圖代替。

精靈王原 CREATE **確切引用 `npc/777/ten.arg` 4,863B**；私人 `npc/giiru/event/sikkoku/ten.arg` 另有 **4,293B，不同 SHA／內容**，即使同名及共同前段文字也不當成 CREATE 的直接引用。前者確有寵物二次轉生後不可騎乘的原**文字警示**，對騎乘的遊戲設計與歷史版本辨識有價值，但目前沒有原引擎執行、實際二次轉生／騎乘限制可操作認證。兩份原配置原樣私人保留，不混合。

## 私人資料保管、公開反例與續接

原 NPC 腳本、完整兩主表真原行、16幅 TW1 原 RD PNG、三幅原 SPR PNG 及新現代靜態圖文觀察頁／圖卡保存在私人 35 成員 ZIP `StoneAge-INTEGRATION86-Sikkoku-original-source-2D-private.zip`，原始來源不出現在 Git。原可視化顯示數字、來源及圖像，**不是商業遊戲原畫面或原玩法執行**；真原圖位元組未改。私人包 SHA、成員 CRC、個別檔SHA與其後 Library 二次保管結果，以有實際結果的補充收據為準。

公開交付只含[原始完整來源路徑、哈希、位元組界限與負證](../../research/recovered/STONEAGE-INTEGRATION86-SIKKOKU-SOURCE-2D-R1.json)、21項公開派生資料正反契約測試和專用 GitHub workflow，不公開原商用美術、原完整道具欄與腳本文本。當前 Stage A **7 PARTIAL＋2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、overall_percent=null；原世界未進入。

**精確 NEXT：** 漆黑洞窟本次 10 NPC＋5考古事件／兩戰鬥候選／原獎勵+跨版19原像來源已達有界靜態止點；下一批輪換另一個有原始真內容與合格圖像，**且未被之前各專項實質覆蓋**的 NPC／寵物／任務族。只在有新的原腳本解析、實際物品發放、原服載入或可用的純淨同版材料時，重審此處 EVENT/DelItem 不一致、20570–72的可得性和 `777/ten.arg` 寵物轉生騎乘語義。
